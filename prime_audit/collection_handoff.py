from __future__ import annotations

from typing import Any


COLLECTION_HANDOFF_SCHEMA = "primeproject.collection-handoff.v1"


def build_collection_handoff(
    *,
    manifest: dict[str, Any],
    matrix: dict[str, Any],
    power: dict[str, Any],
    provenance_requirements: dict[str, Any],
    provenance_audit: dict[str, Any],
    baseline_acceptance: dict[str, Any],
    promotion_plan: dict[str, Any],
    classifier_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    entries = {entry.get("baseline_id"): entry for entry in manifest.get("entries", [])}
    power_rows = {
        _power_key(row.get("library"), row.get("object_type"), row.get("bit_length")): row
        for row in power.get("rows", [])
    }
    requirements = {row.get("baseline_id"): row for row in provenance_requirements.get("rows", [])}
    audit_rows = {row.get("baseline_id"): row for row in provenance_audit.get("rows", [])}
    acceptance_rows = {
        _target_key(row.get("baseline_id"), row.get("bit_length"), row.get("object_type")): row
        for row in baseline_acceptance.get("rows", [])
    }
    promotion_targets = {
        _target_key(row.get("baseline_id"), row.get("bit_length"), row.get("object_type"))
        for row in promotion_plan.get("minimal_unlock_targets", [])
    }

    rows = []
    for collection_row in matrix.get("rows", []):
        for target in collection_row.get("targets", []):
            rows.append(
                handoff_row(
                    collection_row=collection_row,
                    target=target,
                    entry=entries.get(collection_row.get("baseline_id"), {}),
                    power=power_rows.get(
                        _power_key(collection_row.get("library"), target.get("object_type"), target.get("bit_length")),
                        {},
                    ),
                    requirement=requirements.get(collection_row.get("baseline_id"), {}),
                    audit=audit_rows.get(collection_row.get("baseline_id"), {}),
                    acceptance=acceptance_rows.get(
                        _target_key(collection_row.get("baseline_id"), target.get("bit_length"), target.get("object_type")),
                        {},
                    ),
                    is_minimal_unlock=_target_key(
                        collection_row.get("baseline_id"), target.get("bit_length"), target.get("object_type")
                    )
                    in promotion_targets,
                )
            )

    rows.sort(key=handoff_sort_key)
    classifier_scope = (classifier_report or {}).get("claim_scope", "missing")
    classifier_label_count = int((classifier_report or {}).get("label_count") or 0)
    p0_rows = [row for row in rows if row["priority"] == "P0"]
    return {
        "schema": COLLECTION_HANDOFF_SCHEMA,
        "source_schemas": {
            "manifest": manifest.get("schema"),
            "collection_matrix": matrix.get("schema"),
            "collection_power": power.get("schema"),
            "provenance_requirements": provenance_requirements.get("schema"),
            "provenance_audit": provenance_audit.get("schema"),
            "baseline_acceptance": baseline_acceptance.get("schema"),
            "baseline_promotion_plan": promotion_plan.get("schema"),
            "classifier_report": (classifier_report or {}).get("schema"),
        },
        "summary": handoff_summary(rows, p0_rows, classifier_scope, classifier_label_count),
        "claim_gate": {
            "status": "open"
            if baseline_acceptance.get("claim_gate", {}).get("status") == "open"
            and classifier_scope == "real_world"
            and classifier_label_count >= 3
            else "blocked",
            "message": (
                "Real-world collection handoff is claim-ready."
                if baseline_acceptance.get("claim_gate", {}).get("status") == "open"
                and classifier_scope == "real_world"
                and classifier_label_count >= 3
                else "Handoff is ready for collection execution, but real-world attribution claims remain blocked."
            ),
        },
        "public_artifact_contract": {
            "publish_private_material": False,
            "publish_raw_private_primes": False,
            "publish_wallet_seeds": False,
            "required_public_outputs": [
                "aggregate fingerprint JSON",
                "baseline JSON",
                "feature vector JSON",
                "provenance record JSON",
                "SHA-256 checksum",
            ],
        },
        "rows": rows,
        "execution_order": [
            "collect raw material locally",
            "derive aggregate fingerprint",
            "write provenance record",
            "audit provenance",
            "export feature vector",
            "rerun classifier/readiness/evidence-pack",
        ],
    }


def handoff_row(
    *,
    collection_row: dict[str, Any],
    target: dict[str, Any],
    entry: dict[str, Any],
    power: dict[str, Any],
    requirement: dict[str, Any],
    audit: dict[str, Any],
    acceptance: dict[str, Any],
    is_minimal_unlock: bool,
) -> dict[str, Any]:
    object_type = target.get("object_type")
    current_samples = int(entry.get("sample_count") or 0)
    planned_samples = int(target.get("sample_target") or 0)
    target_samples_for_10pct = int(power.get("min_samples_for_10pct_tv") or planned_samples)
    if object_type in {"ecdsa-signature", "schnorr-signature"}:
        target_samples_for_10pct = planned_samples
    remaining_to_plan = max(0, planned_samples - current_samples)
    remaining_to_10pct = max(0, target_samples_for_10pct - current_samples)
    priority = priority_for_target(is_minimal_unlock, collection_row, target, acceptance)
    missing_fields = list(audit.get("missing_required_fields") or requirement.get("missing_required_fields") or [])
    return {
        "task_id": f"{collection_row.get('baseline_id')}:{target.get('bit_length')}:{object_type}",
        "priority": priority,
        "library": collection_row.get("library"),
        "baseline_id": collection_row.get("baseline_id"),
        "track": collection_row.get("track"),
        "object_type": object_type,
        "bit_length": target.get("bit_length"),
        "current_samples": current_samples,
        "planned_sample_target": planned_samples,
        "target_samples_for_10pct_tv": target_samples_for_10pct,
        "remaining_samples_to_plan": remaining_to_plan,
        "remaining_samples_to_10pct_tv": remaining_to_10pct,
        "power_tier": power.get("power_tier", "unknown"),
        "acceptance": acceptance.get("acceptance", "blocked"),
        "blocking_reasons": list(acceptance.get("blocking_reasons") or ["not_evaluated"]),
        "provenance_status": audit.get("status", "blocked"),
        "missing_provenance_fields": missing_fields,
        "public_output": target.get("public_output"),
        "raw_material_policy": (requirement.get("template") or {}).get(
            "raw_material_policy",
            "raw private material stays local; publish aggregate artifacts only",
        ),
        "collector_contract": collector_contract(collection_row, target),
    }


def priority_for_target(
    is_minimal_unlock: bool,
    collection_row: dict[str, Any],
    target: dict[str, Any],
    acceptance: dict[str, Any],
) -> str:
    if acceptance.get("acceptance") in {"accepted", "screening_only"}:
        return "P2"
    if is_minimal_unlock:
        return "P0"
    if collection_row.get("track") == "rsa-prime-generation" and target.get("bit_length") == 2048:
        return "P1"
    if collection_row.get("track") == "signature-nonce-metadata":
        return "P1"
    return "P2"


def collector_contract(collection_row: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    track = collection_row.get("track")
    if track == "rsa-prime-generation":
        return {
            "local_input": "owned generated RSA private material",
            "public_input": "none",
            "public_output": "aggregate RSA-prime fingerprint and feature vector",
            "minimum_replicates": 3,
            "must_not_publish": ["private_key", "private_prime", "raw_key_file"],
        }
    if track == "signature-nonce-metadata":
        return {
            "local_input": "owned wallet signatures or public-chain signature metadata",
            "public_input": "signature r/s/z metadata only",
            "public_output": "nonce-risk summary and distribution fingerprint",
            "minimum_replicates": 1,
            "must_not_publish": ["wallet_seed", "private_key", "raw_signature_owner"],
        }
    return {
        "local_input": "controlled artifact",
        "public_input": "public aggregate metadata",
        "public_output": target.get("public_output"),
        "minimum_replicates": 1,
        "must_not_publish": [],
    }


def handoff_summary(
    rows: list[dict[str, Any]],
    p0_rows: list[dict[str, Any]],
    classifier_scope: str,
    classifier_label_count: int,
) -> dict[str, Any]:
    remaining_p0_samples = sum(int(row.get("remaining_samples_to_10pct_tv") or 0) for row in p0_rows)
    blocked_rows = [row for row in rows if row.get("acceptance") == "blocked"]
    missing_fields = sum(len(row.get("missing_provenance_fields") or []) for row in rows)
    return {
        "task_count": len(rows),
        "p0_count": len(p0_rows),
        "blocked_count": len(blocked_rows),
        "remaining_p0_samples_for_10pct_tv": remaining_p0_samples,
        "missing_provenance_field_count": missing_fields,
        "classifier_scope": classifier_scope,
        "classifier_label_count": classifier_label_count,
        "next_unlock": "collect OpenSSL 2048-bit and BoringSSL 2048-bit aggregate RSA-prime baselines with complete provenance",
    }


def handoff_sort_key(row: dict[str, Any]) -> tuple[int, str, int]:
    priority_rank = {"P0": 0, "P1": 1, "P2": 2}
    return (
        priority_rank.get(str(row.get("priority")), 9),
        str(row.get("library") or ""),
        int(row.get("bit_length") or 0),
    )


def _power_key(library: Any, object_type: Any, bit_length: Any) -> tuple[Any, Any, Any]:
    return (library, object_type, bit_length)


def _target_key(baseline_id: Any, bit_length: Any, object_type: Any) -> tuple[Any, Any, Any]:
    return (baseline_id, bit_length, object_type)
