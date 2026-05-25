from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


EVIDENCE_PACK_SCHEMA = "primeproject.evidence-pack.v1"


def build_evidence_pack(
    *,
    manifest: dict[str, Any],
    readiness: dict[str, Any],
    attribution_grid: dict[str, Any] | None = None,
    classifier_report: dict[str, Any] | None = None,
    bitcoin_risk_report: dict[str, Any] | None = None,
    baseline_acceptance: dict[str, Any] | None = None,
    collection_intake: dict[str, Any] | None = None,
    file_paths: dict[str, str | Path] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    artifacts = artifact_summaries(file_paths or {})
    gates = publication_gates(
        manifest=manifest,
        readiness=readiness,
        attribution_grid=attribution_grid or {},
        classifier_report=classifier_report or {},
        bitcoin_risk_report=bitcoin_risk_report or {},
        baseline_acceptance=baseline_acceptance or {},
        collection_intake=collection_intake or {},
        artifacts=artifacts,
    )
    return {
        "schema": EVIDENCE_PACK_SCHEMA,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "claim_level": claim_level(readiness, gates),
        "publication_gates": gates,
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
        "evidence_summary": evidence_summary(
            manifest=manifest,
            readiness=readiness,
            attribution_grid=attribution_grid or {},
            classifier_report=classifier_report or {},
            bitcoin_risk_report=bitcoin_risk_report or {},
            baseline_acceptance=baseline_acceptance or {},
            collection_intake=collection_intake or {},
        ),
        "required_evidence": required_evidence(readiness),
        "local_collection_protocols": local_collection_protocols(),
    }


def artifact_summaries(file_paths: dict[str, str | Path]) -> list[dict[str, Any]]:
    artifacts = []
    for role, path_value in sorted(file_paths.items()):
        path = Path(path_value)
        if not path.exists():
            artifacts.append(
                {
                    "role": role,
                    "path": str(path),
                    "exists": False,
                    "sha256": None,
                    "schema": None,
                    "bytes": 0,
                }
            )
            continue
        data = path.read_bytes()
        schema = None
        payload_summary: dict[str, Any] = {}
        try:
            payload = json.loads(data.decode("utf-8"))
            if isinstance(payload, dict):
                schema = payload.get("schema")
                payload_summary = artifact_semantics(role, payload)
        except (UnicodeDecodeError, json.JSONDecodeError):
            schema = None
        artifacts.append(
            {
                "role": role,
                "path": str(path).replace("\\", "/"),
                "exists": True,
                "sha256": hashlib.sha256(data).hexdigest(),
                "schema": schema,
                "bytes": len(data),
                **payload_summary,
            }
        )
    return artifacts


def artifact_semantics(role: str, payload: dict[str, Any]) -> dict[str, Any]:
    if role == "collection_fixture_audit":
        summary = payload.get("summary") or {}
        quality_gate = payload.get("quality_gate") or {}
        return {
            "quality_gate_status": quality_gate.get("status"),
            "fixture_count": summary.get("fixture_count"),
            "failed_expectation_count": summary.get("failed_expectation_count"),
            "public_safe_fixture_count": summary.get("public_safe_fixture_count"),
        }
    return {}


def publication_gates(
    *,
    manifest: dict[str, Any],
    readiness: dict[str, Any],
    attribution_grid: dict[str, Any],
    classifier_report: dict[str, Any],
    bitcoin_risk_report: dict[str, Any],
    baseline_acceptance: dict[str, Any],
    collection_intake: dict[str, Any],
    artifacts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    dimensions = readiness.get("dimensions", {})
    sim_to_real = dimensions.get("sim_to_real", {})
    attribution = dimensions.get("attribution_validation", {})
    classifier = dimensions.get("classifier", {})
    bitcoin = dimensions.get("bitcoin_integration", {})
    artifact_by_role = {artifact.get("role"): artifact for artifact in artifacts}
    fixture_audit = artifact_by_role.get("collection_fixture_audit", {})
    fixture_count = int(fixture_audit.get("fixture_count") or 0)
    public_safe_fixture_count = int(fixture_audit.get("public_safe_fixture_count") or 0)
    fixture_failed_count = int(fixture_audit.get("failed_expectation_count") or 0)
    fixture_audit_passed = (
        fixture_audit.get("exists")
        and fixture_audit.get("schema") == "primeproject.collection-fixture-audit.v1"
        and fixture_audit.get("quality_gate_status") == "pass"
        and fixture_count > 0
        and public_safe_fixture_count == fixture_count
        and fixture_failed_count == 0
    )
    sensitive_available = [
        entry.get("baseline_id")
        for entry in manifest.get("entries", [])
        if entry.get("sensitive") and entry.get("status") == "available"
    ]
    gates = [
        gate(
            "sensitive_publication_gate",
            not sensitive_available and not manifest.get("handling_policy", {}).get("publish_sensitive_material", False),
            "Public bundle must not expose private primes, seeds, or sensitive owned samples.",
            {"sensitive_available": sensitive_available},
            severity="critical",
        ),
        gate(
            "real_baseline_gate",
            int(sim_to_real.get("available_count") or 0) >= 2,
            "Real-world attribution needs at least two available aggregate baselines.",
            {"available_count": sim_to_real.get("available_count", 0)},
        ),
        gate(
            "controlled_signal_gate",
            bool(attribution.get("robust_profiles")),
            "At least one profile should survive bit-length control before using the signal.",
            {"robust_profiles": attribution.get("robust_profiles", [])},
        ),
        gate(
            "classifier_gate",
            classifier.get("real_world_claim_ready") is True
            and int(classifier.get("label_count") or 0) >= 3
            and int(classifier.get("vector_count") or 0) >= 12,
            "Classifier claims need real-world labelled feature vectors across at least three labels.",
            {
                "label_count": classifier.get("label_count", 0),
                "vector_count": classifier.get("vector_count", 0),
                "claim_scope": classifier.get("claim_scope"),
            },
        ),
        gate(
            "bitcoin_integration_gate",
            bool(bitcoin_risk_report) or float(bitcoin.get("score") or 0.0) >= 0.7,
            "Bitcoin claims need a bundled nonce-risk report or a completed integration score.",
            {"risk_level": bitcoin_risk_report.get("risk_level") if bitcoin_risk_report else None},
            severity="medium",
        ),
        gate(
            "reproducibility_gate",
            len([artifact for artifact in artifacts if artifact.get("exists") and artifact.get("sha256")]) >= 3,
            "Published evidence should include checksummed source JSON artifacts.",
            {"artifact_count": len(artifacts)},
            severity="medium",
        ),
        gate(
            "provenance_gate",
            any(
                artifact.get("role") == "provenance_requirements"
                and artifact.get("exists")
                and artifact.get("schema") == "primeproject.provenance-requirements.v1"
                for artifact in artifacts
            ),
            "Real-world collection claims need a checksummed provenance requirements artifact.",
            {
                "has_provenance_requirements": any(
                    artifact.get("role") == "provenance_requirements" and artifact.get("exists")
                    for artifact in artifacts
                )
            },
            severity="medium",
        ),
        gate(
            "provenance_audit_gate",
            any(
                artifact.get("role") == "provenance_audit"
                and artifact.get("exists")
                and artifact.get("schema") == "primeproject.provenance-audit.v1"
                for artifact in artifacts
            ),
            "Real-world collection claims need a checksummed provenance audit artifact.",
            {
                "has_provenance_audit": any(
                    artifact.get("role") == "provenance_audit" and artifact.get("exists")
                    for artifact in artifacts
                )
            },
            severity="medium",
        ),
        gate(
            "collection_submission_contract_gate",
            any(
                artifact.get("role") == "collection_submission_contract"
                and artifact.get("exists")
                and artifact.get("schema") == "primeproject.collection-submission-contract.v1"
                for artifact in artifacts
            ),
            "Real-world collection claims need a public submission contract before intake records are accepted.",
            {
                "has_collection_submission_contract": any(
                    artifact.get("role") == "collection_submission_contract" and artifact.get("exists")
                    for artifact in artifacts
                )
            },
            severity="medium",
        ),
        gate(
            "collection_submission_lint_gate",
            any(
                artifact.get("role") == "collection_submission_lint"
                and artifact.get("exists")
                and artifact.get("schema") == "primeproject.collection-submission-lint.v1"
                for artifact in artifacts
            ),
            "Real-world collection claims need a pre-intake submission lint report for public contract failures.",
            {
                "has_collection_submission_lint": any(
                    artifact.get("role") == "collection_submission_lint" and artifact.get("exists")
                    for artifact in artifacts
                )
            },
            severity="medium",
        ),
        gate(
            "collection_fixture_audit_gate",
            bool(fixture_audit_passed),
            "Real-world collection tooling needs passing public-safe fixtures that prove lint pass/warn/block behavior before live submissions.",
            {
                "has_collection_fixture_audit": bool(fixture_audit.get("exists")),
                "quality_gate_status": fixture_audit.get("quality_gate_status"),
                "fixture_count": fixture_count,
                "failed_expectation_count": fixture_failed_count,
                "public_safe_fixture_count": public_safe_fixture_count,
            },
            severity="medium",
        ),
        gate(
            "baseline_acceptance_gate",
            baseline_acceptance.get("claim_gate", {}).get("status") == "open",
            "Real-world attribution claims need at least two accepted RSA library baselines.",
            {
                "accepted_count": baseline_acceptance.get("accepted_count", 0),
                "accepted_rsa_library_count": baseline_acceptance.get("summary", {}).get("accepted_rsa_library_count", 0),
                "claim_gate": baseline_acceptance.get("claim_gate", {}).get("status"),
            },
            severity="high",
        ),
        gate(
            "collection_intake_gate",
            collection_intake.get("claim_gate", {}).get("status") == "open",
            "Submitted aggregate artifacts must pass collection intake before real-world attribution claims.",
            {
                "submitted_count": collection_intake.get("summary", {}).get("submitted_count", 0),
                "accepted_count": collection_intake.get("summary", {}).get("accepted_count", 0),
                "accepted_rsa_library_count": collection_intake.get("summary", {}).get(
                    "accepted_rsa_library_count", 0
                ),
                "p0_blocked_count": collection_intake.get("summary", {}).get("p0_blocked_count", 0),
                "forbidden_public_field_count": collection_intake.get("summary", {}).get(
                    "forbidden_public_field_count", 0
                ),
                "feature_vector_contract_blocked_count": collection_intake.get("summary", {}).get(
                    "feature_vector_contract_blocked_count", 0
                ),
                "duplicate_submission_count": collection_intake.get("summary", {}).get(
                    "duplicate_submission_count", 0
                ),
                "reused_aggregate_hash_count": collection_intake.get("summary", {}).get(
                    "reused_aggregate_hash_count", 0
                ),
                "claim_gate": collection_intake.get("claim_gate", {}).get("status"),
            },
            severity="high",
        ),
        gate(
            "promotion_plan_gate",
            any(
                artifact.get("role") == "baseline_promotion_plan"
                and artifact.get("exists")
                and artifact.get("schema") == "primeproject.baseline-promotion-plan.v1"
                for artifact in artifacts
            ),
            "Blocked real-world baselines should publish a concrete promotion plan.",
            {
                "has_promotion_plan": any(
                    artifact.get("role") == "baseline_promotion_plan" and artifact.get("exists")
                    for artifact in artifacts
                )
            },
            severity="medium",
        ),
    ]
    if not attribution_grid:
        gates.append(
            gate(
                "attribution_grid_presence_gate",
                False,
                "Evidence pack is missing paired attribution-grid data.",
                {},
                severity="medium",
            )
        )
    return gates


def evidence_summary(
    *,
    manifest: dict[str, Any],
    readiness: dict[str, Any],
    attribution_grid: dict[str, Any],
    classifier_report: dict[str, Any],
    bitcoin_risk_report: dict[str, Any],
    baseline_acceptance: dict[str, Any],
    collection_intake: dict[str, Any],
) -> dict[str, Any]:
    return {
        "manifest": {
            "entry_count": manifest.get("entry_count", len(manifest.get("entries", []))),
            "status_counts": manifest.get("status_counts", {}),
            "validation_passed": manifest.get("validation", {}).get("passed"),
        },
        "readiness": readiness.get("overall", {}),
        "attribution": {
            "rows": len(attribution_grid.get("rows", [])),
            "repeats": attribution_grid.get("repeats"),
            "profiles": sorted((attribution_grid.get("summary", {}).get("profiles") or {}).keys()),
        },
        "classifier": {
            "present": bool(classifier_report),
            "label_count": classifier_report.get("label_count") if classifier_report else 0,
            "vector_count": classifier_report.get("usable_vector_count") if classifier_report else 0,
            "accuracy": classifier_report.get("accuracy") if classifier_report else None,
        },
        "bitcoin": {
            "present": bool(bitcoin_risk_report),
            "risk_level": bitcoin_risk_report.get("risk_level") if bitcoin_risk_report else None,
        },
        "baseline_acceptance": {
            "present": bool(baseline_acceptance),
            "accepted_count": baseline_acceptance.get("accepted_count", 0) if baseline_acceptance else 0,
            "screening_only_count": baseline_acceptance.get("screening_only_count", 0) if baseline_acceptance else 0,
            "blocked_count": baseline_acceptance.get("blocked_count", 0) if baseline_acceptance else 0,
        },
        "collection_intake": {
            "present": bool(collection_intake),
            "submitted_count": collection_intake.get("summary", {}).get("submitted_count", 0)
            if collection_intake
            else 0,
            "accepted_count": collection_intake.get("summary", {}).get("accepted_count", 0)
            if collection_intake
            else 0,
            "blocked_count": collection_intake.get("summary", {}).get("blocked_count", 0)
            if collection_intake
            else 0,
            "forbidden_public_field_count": collection_intake.get("summary", {}).get(
                "forbidden_public_field_count", 0
            )
            if collection_intake
            else 0,
            "feature_vector_contract_blocked_count": collection_intake.get("summary", {}).get(
                "feature_vector_contract_blocked_count", 0
            )
            if collection_intake
            else 0,
            "duplicate_submission_count": collection_intake.get("summary", {}).get(
                "duplicate_submission_count", 0
            )
            if collection_intake
            else 0,
            "reused_aggregate_hash_count": collection_intake.get("summary", {}).get(
                "reused_aggregate_hash_count", 0
            )
            if collection_intake
            else 0,
        },
    }


def required_evidence(readiness: dict[str, Any]) -> list[dict[str, Any]]:
    dimensions = readiness.get("dimensions", {})
    sim = dimensions.get("sim_to_real", {})
    classifier = dimensions.get("classifier", {})
    bitcoin = dimensions.get("bitcoin_integration", {})
    classifier_ready = (
        classifier.get("real_world_claim_ready") is True
        and int(classifier.get("label_count") or 0) >= 3
        and int(classifier.get("vector_count") or 0) >= 12
    )
    return [
        {
            "item": "two_available_real_baselines",
            "status": "complete" if int(sim.get("available_count") or 0) >= 2 else "missing",
            "reason": "Needed to compare suspicious objects against more than one real generator family.",
        },
        {
            "item": "real_world_labelled_feature_vectors",
            "status": "complete" if classifier_ready else "missing",
            "reason": "Needed before classifier output can support real-world attribution, not just controlled synthetic validation.",
        },
        {
            "item": "bitcoin_nonce_risk_report",
            "status": "complete" if float(bitcoin.get("score") or 0.0) >= 0.7 else "missing",
            "reason": "Needed for wallet/library nonce fingerprint claims.",
        },
    ]


def local_collection_protocols() -> list[dict[str, Any]]:
    return [
        {
            "track": "openssl-rsa",
            "sample_target": ">=500 p/q prime values per bit length, aggregate only",
            "public_output": "fingerprint JSON, baseline JSON, feature vectors",
            "private_output": "raw private keys and primes stay local",
        },
        {
            "track": "boringssl-rsa",
            "sample_target": "match OpenSSL bit lengths and sample counts",
            "public_output": "aggregate fingerprint and baseline distance only",
            "private_output": "raw generated key material stays local",
        },
        {
            "track": "go-crypto-rsa",
            "sample_target": "match OpenSSL/BoringSSL matrix",
            "public_output": "aggregate fingerprint and feature vectors",
            "private_output": "raw generated key material stays local",
        },
        {
            "track": "bitcoin-wallet-signature",
            "sample_target": "signature metadata grouped by wallet/library/version when lawful and owned/public",
            "public_output": "nonce-risk summary and distribution fingerprint",
            "private_output": "seeds, private keys, and deanonymizing metadata stay local",
        },
    ]


def claim_level(readiness: dict[str, Any], gates: list[dict[str, Any]]) -> dict[str, Any]:
    failed_high = [item for item in gates if not item["passed"] and item["severity"] in {"high", "critical"}]
    failed_any = [item for item in gates if not item["passed"]]
    score = float(readiness.get("overall", {}).get("score") or 0.0)
    if failed_high:
        level = "public_demo_only"
        statement = "Safe to publish as a research scaffold, not as real-world attribution evidence."
    elif failed_any or score < 0.8:
        level = "prototype_research"
        statement = "Useful for controlled research, with limitations explicitly attached."
    else:
        level = "real_world_research_candidate"
        statement = "Evidence gates support cautious real-world generator attribution experiments."
    return {
        "level": level,
        "statement": statement,
        "failed_gate_count": len(failed_any),
        "failed_high_gate_count": len(failed_high),
    }


def gate(
    code: str,
    passed: bool,
    message: str,
    evidence: dict[str, Any],
    *,
    severity: str = "high",
) -> dict[str, Any]:
    return {
        "code": code,
        "passed": bool(passed),
        "severity": severity,
        "message": message,
        "evidence": evidence,
    }
