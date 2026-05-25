from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


PUBLICATION_CONSISTENCY_SCHEMA = "primeproject.publication-consistency.v1"

HIGH_RISK_CLAIMS = (
    "real_world_generator_attribution",
    "bitcoin_nonce_risk_attribution",
)

HIGH_RISK_DECISIONS = (
    "promote_real_world_generator_attribution",
    "promote_bitcoin_nonce_risk_attribution",
)


def build_publication_consistency_report(
    *,
    evidence_pack: dict[str, Any],
    claim_ledger: dict[str, Any],
    decision_protocol: dict[str, Any],
    falsification_battery: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    gates = {gate.get("code"): gate for gate in evidence_pack.get("publication_gates", [])}
    required = {
        item.get("item"): item
        for item in evidence_pack.get("required_evidence", [])
    }
    claims = {
        claim.get("claim_id"): claim
        for claim in claim_ledger.get("claims", [])
    }
    decisions = {
        decision.get("decision_id"): decision
        for decision in decision_protocol.get("decisions", [])
    }
    falsification_checks = {
        check.get("check"): check
        for check in falsification_battery.get("checks", [])
    }

    checks = [
        real_world_boundary_check(gates, required, claims, decisions),
        bitcoin_boundary_check(gates, required, claims, decisions),
        decision_claim_alignment_check(claims, decisions),
        falsification_guard_alignment_check(decisions, falsification_checks),
        required_evidence_covers_blockers_check(gates, required),
    ]
    counts: dict[str, int] = {}
    for check in checks:
        counts[check["status"]] = counts.get(check["status"], 0) + 1
    fail_count = counts.get("fail", 0)
    warn_count = counts.get("warn", 0)
    status = "fail" if fail_count else "warn" if warn_count else "pass"
    return {
        "schema": PUBLICATION_CONSISTENCY_SCHEMA,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "source": {
            "evidence_pack_schema": evidence_pack.get("schema"),
            "claim_ledger_schema": claim_ledger.get("schema"),
            "decision_protocol_schema": decision_protocol.get("schema"),
            "falsification_battery_schema": falsification_battery.get("schema"),
            "claim_level": evidence_pack.get("claim_level", {}).get("level"),
            "falsification_claim_floor": falsification_battery.get("summary", {}).get("claim_floor"),
        },
        "summary": {
            "status": status,
            "check_count": len(checks),
            "pass_count": counts.get("pass", 0),
            "warn_count": warn_count,
            "fail_count": fail_count,
            "high_risk_claims_blocked": all(
                claims.get(claim_id, {}).get("status") == "blocked"
                for claim_id in HIGH_RISK_CLAIMS
            ),
            "high_risk_decisions_blocked": all(
                decisions.get(decision_id, {}).get("status") == "blocked"
                for decision_id in HIGH_RISK_DECISIONS
            ),
        },
        "policy": {
            "post_pack_audit": True,
            "reason": (
                "This consistency report consumes the evidence pack, claim ledger, "
                "decision protocol, and falsification battery. It is generated after "
                "those artifacts to catch claim-boundary drift without creating "
                "circular evidence-pack hashes."
            ),
            "allowed_failure_interpretation": "A fail means public claim language and promotion gates disagree.",
        },
        "checks": checks,
    }


def real_world_boundary_check(
    gates: dict[str | None, dict[str, Any]],
    required: dict[str | None, dict[str, Any]],
    claims: dict[str | None, dict[str, Any]],
    decisions: dict[str | None, dict[str, Any]],
) -> dict[str, Any]:
    failed_gates = [
        "real_baseline_gate",
        "classifier_gate",
        "baseline_acceptance_gate",
        "collection_intake_gate",
    ]
    missing_required = [
        "two_available_real_baselines",
        "real_world_labelled_feature_vectors",
        "two_accepted_real_baselines",
        "accepted_collection_intake",
    ]
    passes = (
        all(not bool(gates.get(code, {}).get("passed")) for code in failed_gates)
        and claim_status(claims, "real_world_generator_attribution") == "blocked"
        and decision_status(decisions, "promote_real_world_generator_attribution") == "blocked"
        and all(required_status(required, item) == "missing" for item in missing_required)
    )
    return check_result(
        "real_world_boundary_consistent",
        "pass" if passes else "fail",
        "critical",
        "Real-world attribution is blocked by matching evidence, ledger, decision, and missing-evidence signals."
        if passes
        else "Real-world attribution boundary disagrees across publication artifacts.",
        {
            "failed_gates": missing_or_false_gates(gates, failed_gates),
            "claim_status": claim_status(claims, "real_world_generator_attribution"),
            "decision_status": decision_status(decisions, "promote_real_world_generator_attribution"),
            "missing_required_evidence": missing_required_items(required, missing_required),
        },
    )


def bitcoin_boundary_check(
    gates: dict[str | None, dict[str, Any]],
    required: dict[str | None, dict[str, Any]],
    claims: dict[str | None, dict[str, Any]],
    decisions: dict[str | None, dict[str, Any]],
) -> dict[str, Any]:
    decision = decisions.get("promote_bitcoin_nonce_risk_attribution", {})
    blocking_items = set(decision.get("blocking_items", []))
    passes = (
        not bool(gates.get("bitcoin_integration_gate", {}).get("passed"))
        and claim_status(claims, "bitcoin_nonce_risk_attribution") == "blocked"
        and decision_status(decisions, "promote_bitcoin_nonce_risk_attribution") == "blocked"
        and "artifact:bitcoin_risk_report" in blocking_items
        and required_status(required, "bitcoin_nonce_risk_report") == "missing"
    )
    return check_result(
        "bitcoin_boundary_consistent",
        "pass" if passes else "fail",
        "critical",
        "Bitcoin nonce-risk attribution is blocked consistently until a bundled risk report exists."
        if passes
        else "Bitcoin nonce-risk attribution boundary disagrees across publication artifacts.",
        {
            "bitcoin_gate_passed": bool(gates.get("bitcoin_integration_gate", {}).get("passed")),
            "claim_status": claim_status(claims, "bitcoin_nonce_risk_attribution"),
            "decision_status": decision_status(decisions, "promote_bitcoin_nonce_risk_attribution"),
            "blocking_items": sorted(blocking_items),
            "required_evidence_status": required_status(required, "bitcoin_nonce_risk_report"),
        },
    )


def decision_claim_alignment_check(
    claims: dict[str | None, dict[str, Any]],
    decisions: dict[str | None, dict[str, Any]],
) -> dict[str, Any]:
    contradictions = []
    for decision in decisions.values():
        claim_id = decision.get("claim_id")
        if not claim_id:
            continue
        if decision.get("status") == "allowed" and claims.get(claim_id, {}).get("status") == "blocked":
            contradictions.append(
                {
                    "decision_id": decision.get("decision_id"),
                    "claim_id": claim_id,
                    "claim_status": "blocked",
                    "decision_status": "allowed",
                }
            )
    return check_result(
        "decision_claim_alignment",
        "pass" if not contradictions else "fail",
        "critical",
        "No decision promotes a claim that the claim ledger blocks."
        if not contradictions
        else "A decision promotes a blocked claim.",
        {"contradictions": contradictions},
    )


def falsification_guard_alignment_check(
    decisions: dict[str | None, dict[str, Any]],
    falsification_checks: dict[str | None, dict[str, Any]],
) -> dict[str, Any]:
    guard = falsification_checks.get("claim_promotion_guard", {})
    promoted = [
        decision_id
        for decision_id in HIGH_RISK_DECISIONS
        if decisions.get(decision_id, {}).get("status") != "blocked"
    ]
    passes = guard.get("status") == "pass" and not promoted
    return check_result(
        "falsification_guard_alignment",
        "pass" if passes else "fail",
        "critical",
        "The falsification guard agrees that high-risk attribution decisions remain blocked."
        if passes
        else "The falsification guard and decision protocol disagree on high-risk claim promotion.",
        {
            "claim_promotion_guard_status": guard.get("status", "missing"),
            "unexpectedly_promoted_decisions": promoted,
        },
    )


def required_evidence_covers_blockers_check(
    gates: dict[str | None, dict[str, Any]],
    required: dict[str | None, dict[str, Any]],
) -> dict[str, Any]:
    blocker_to_required = {
        "real_baseline_gate": "two_available_real_baselines",
        "classifier_gate": "real_world_labelled_feature_vectors",
        "baseline_acceptance_gate": "two_accepted_real_baselines",
        "collection_intake_gate": "accepted_collection_intake",
        "bitcoin_integration_gate": "bitcoin_nonce_risk_report",
    }
    failed_gate_codes = [
        code
        for code, item in gates.items()
        if code in blocker_to_required and not bool(item.get("passed"))
    ]
    missing_explanations = [
        {"failed_gate": code, "required_evidence": blocker_to_required[code]}
        for code in failed_gate_codes
        if blocker_to_required[code] not in required
    ]
    return check_result(
        "required_evidence_covers_blockers",
        "pass" if not missing_explanations else "fail",
        "high",
        "Every high-risk failed gate has a matching required-evidence item."
        if not missing_explanations
        else "One or more failed gates lacks a matching required-evidence item.",
        {
            "failed_gate_codes": failed_gate_codes,
            "missing_explanations": missing_explanations,
        },
    )


def claim_status(claims: dict[str | None, dict[str, Any]], claim_id: str) -> str:
    return str(claims.get(claim_id, {}).get("status", "missing"))


def decision_status(decisions: dict[str | None, dict[str, Any]], decision_id: str) -> str:
    return str(decisions.get(decision_id, {}).get("status", "missing"))


def required_status(required: dict[str | None, dict[str, Any]], item: str) -> str:
    return str(required.get(item, {}).get("status", "missing"))


def missing_or_false_gates(gates: dict[str | None, dict[str, Any]], codes: list[str]) -> list[str]:
    return [code for code in codes if not bool(gates.get(code, {}).get("passed"))]


def missing_required_items(required: dict[str | None, dict[str, Any]], items: list[str]) -> list[str]:
    return [item for item in items if required_status(required, item) == "missing"]


def check_result(
    check: str,
    status: str,
    severity: str,
    message: str,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "check": check,
        "status": status,
        "severity": severity,
        "message": message,
        "evidence": evidence,
    }
