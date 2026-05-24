from __future__ import annotations

from typing import Any


BASELINE_ACCEPTANCE_SCHEMA = "primeproject.baseline-acceptance.v1"


def build_baseline_acceptance(
    *,
    manifest: dict[str, Any],
    matrix: dict[str, Any],
    power: dict[str, Any],
    provenance_audit: dict[str, Any],
) -> dict[str, Any]:
    entries = {entry.get("baseline_id"): entry for entry in manifest.get("entries", [])}
    power_rows = {
        power_key(row.get("library"), row.get("object_type"), row.get("bit_length")): row
        for row in power.get("rows", [])
    }
    audit_rows = {row.get("baseline_id"): row for row in provenance_audit.get("rows", [])}
    rows = [
        acceptance_row(collection_row, target, entries, power_rows, audit_rows)
        for collection_row in matrix.get("rows", [])
        for target in collection_row.get("targets", [])
    ]
    accepted = [row for row in rows if row["acceptance"] == "accepted"]
    screening = [row for row in rows if row["acceptance"] == "screening_only"]
    blocked = [row for row in rows if row["acceptance"] == "blocked"]
    accepted_rsa_libraries = sorted(
        {
            row["library"]
            for row in accepted
            if row.get("object_type") == "rsa-prime" and row.get("track") == "rsa-prime-generation"
        }
    )
    return {
        "schema": BASELINE_ACCEPTANCE_SCHEMA,
        "row_count": len(rows),
        "accepted_count": len(accepted),
        "screening_only_count": len(screening),
        "blocked_count": len(blocked),
        "summary": {
            "accepted_rsa_library_count": len(accepted_rsa_libraries),
            "accepted_rsa_libraries": accepted_rsa_libraries,
            "minimum_rsa_libraries": 2,
            "public_safe": bool(provenance_audit.get("summary", {}).get("public_safe", False)),
            "dominant_blockers": dominant_blockers(rows),
        },
        "rows": rows,
        "claim_gate": {
            "status": "open" if len(accepted_rsa_libraries) >= 2 else "blocked",
            "message": (
                "At least two accepted RSA library baselines are ready for cautious attribution experiments."
                if len(accepted_rsa_libraries) >= 2
                else "Real-world attribution remains blocked until at least two RSA libraries pass availability, provenance, and power gates."
            ),
        },
        "next_actions": next_actions(rows),
    }


def acceptance_row(
    collection_row: dict[str, Any],
    target: dict[str, Any],
    entries: dict[Any, dict[str, Any]],
    power_rows: dict[tuple[Any, Any, Any], dict[str, Any]],
    audit_rows: dict[Any, dict[str, Any]],
) -> dict[str, Any]:
    baseline_id = collection_row.get("baseline_id")
    entry = entries.get(baseline_id, {})
    power = power_rows.get(power_key(collection_row.get("library"), target.get("object_type"), target.get("bit_length")), {})
    audit = audit_rows.get(baseline_id, {})
    blockers = blocking_reasons(entry, target, power, audit)
    power_tier = power.get("power_tier") or "unknown"
    if blockers:
        acceptance = "blocked"
    elif power_tier == "coarse":
        acceptance = "screening_only"
    else:
        acceptance = "accepted"
    return {
        "baseline_id": baseline_id,
        "library": collection_row.get("library"),
        "track": collection_row.get("track"),
        "object_type": target.get("object_type"),
        "bit_length": target.get("bit_length"),
        "sample_count": entry.get("sample_count", 0),
        "sample_target": target.get("sample_target", 0),
        "target_status": target.get("status", "planned"),
        "manifest_status": entry.get("status", "missing"),
        "provenance_status": audit.get("status", "missing"),
        "power_tier": power_tier,
        "interval_label": power.get("interval_label"),
        "conservative_tv_floor_interval": power.get("conservative_tv_floor_interval"),
        "conservative_tv_floor_95": power.get("conservative_tv_floor_95"),
        "acceptance": acceptance,
        "blocking_reasons": blockers,
    }


def blocking_reasons(
    entry: dict[str, Any],
    target: dict[str, Any],
    power: dict[str, Any],
    audit: dict[str, Any],
) -> list[str]:
    reasons = []
    if entry.get("status") != "available":
        reasons.append("manifest_not_available")
    if target.get("status") != "available":
        reasons.append("target_not_available")
    if audit.get("status") != "pass":
        reasons.append("provenance_not_passed")
    if audit.get("forbidden_public_fields"):
        reasons.append("forbidden_public_fields")
    if not power:
        reasons.append("missing_power_row")
    return reasons


def dominant_blockers(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for row in rows:
        for reason in row.get("blocking_reasons", []):
            counts[reason] = counts.get(reason, 0) + 1
    return [
        {"reason": reason, "count": count}
        for reason, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def next_actions(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blockers = dominant_blockers(rows)
    actions = []
    for blocker in blockers[:3]:
        reason = blocker["reason"]
        if reason == "provenance_not_passed":
            action = "Complete provenance records and aggregate artifact hashes before promoting any real-world baseline."
        elif reason in {"manifest_not_available", "target_not_available"}:
            action = "Generate local aggregate fingerprints for planned OpenSSL, BoringSSL, Go, and Bitcoin metadata targets."
        elif reason == "forbidden_public_fields":
            action = "Remove forbidden sensitive fields from public records and publish only aggregate artifacts."
        else:
            action = "Regenerate collection power and acceptance reports after baseline artifacts are added."
        actions.append({"priority": "P0", "blocker": reason, "count": blocker["count"], "action": action})
    return actions


def power_key(library: Any, object_type: Any, bit_length: Any) -> tuple[Any, Any, Any]:
    return (library, object_type, bit_length)
