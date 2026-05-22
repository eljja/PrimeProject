from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


DECISION_PROTOCOL_SCHEMA = "primeproject.decision-protocol.v1"


@dataclass(frozen=True)
class DecisionRule:
    decision_id: str
    title: str
    track: str
    claim_id: str
    required_gates: tuple[str, ...]
    required_artifacts: tuple[str, ...]
    required_lineage_reproducible: bool
    threshold: str
    allowed_statement: str
    blocked_statement: str


DECISION_RULES: tuple[DecisionRule, ...] = (
    DecisionRule(
        decision_id="publish_public_demo",
        title="Publish public demo and exploratory visualizations",
        track="publication",
        claim_id="prime_measure_visualization",
        required_gates=("sensitive_publication_gate", "reproducibility_gate"),
        required_artifacts=("snapshot_manifest",),
        required_lineage_reproducible=True,
        threshold="No sensitive material, at least three checksummed artifacts, and acyclic lineage.",
        allowed_statement="Public demo language is allowed when labelled as exploratory visualization.",
        blocked_statement="Do not publish the demo if sensitive material or stale checksums are present.",
    ),
    DecisionRule(
        decision_id="report_controlled_synthetic_signal",
        title="Report controlled synthetic generator signal",
        track="controlled-validation",
        claim_id="synthetic_generator_attribution",
        required_gates=("controlled_signal_gate", "reproducibility_gate"),
        required_artifacts=("attribution_grid",),
        required_lineage_reproducible=True,
        threshold="Controlled attribution grid is present and at least one profile survives bit-length control.",
        allowed_statement="Controlled synthetic attribution may be reported with confound limits attached.",
        blocked_statement="Do not describe synthetic attribution as robust until controlled grid evidence exists.",
    ),
    DecisionRule(
        decision_id="promote_real_world_generator_attribution",
        title="Promote real-world generator attribution claim",
        track="sim-to-real",
        claim_id="real_world_generator_attribution",
        required_gates=(
            "real_baseline_gate",
            "classifier_gate",
            "provenance_gate",
            "provenance_audit_gate",
            "baseline_acceptance_gate",
        ),
        required_artifacts=("manifest", "readiness", "baseline_acceptance"),
        required_lineage_reproducible=True,
        threshold=(
            "At least two accepted RSA library baselines, complete provenance, labelled classifier "
            "vectors across at least three labels, and matching evidence-pack checksums."
        ),
        allowed_statement="Cautious real-world generator attribution experiments may be reported.",
        blocked_statement="Real-world generator attribution must remain a blocked claim.",
    ),
    DecisionRule(
        decision_id="promote_bitcoin_nonce_risk_attribution",
        title="Promote Bitcoin wallet/library nonce-risk attribution claim",
        track="bitcoin",
        claim_id="bitcoin_nonce_risk_attribution",
        required_gates=("bitcoin_integration_gate",),
        required_artifacts=("bitcoin_risk_report",),
        required_lineage_reproducible=True,
        threshold="A bundled Bitcoin nonce-risk report exists and is linked to wallet/library baseline metadata.",
        allowed_statement="Bitcoin nonce-risk attribution may be reported with public or owned metadata limits attached.",
        blocked_statement="Bitcoin attribution must stay blocked until nonce-risk evidence is bundled.",
    ),
)


def build_decision_protocol(
    *,
    evidence_pack: dict[str, Any],
    claim_ledger: dict[str, Any],
    artifact_lineage: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    gates = {gate.get("code"): gate for gate in evidence_pack.get("publication_gates", [])}
    artifacts = {artifact.get("role"): artifact for artifact in evidence_pack.get("artifacts", [])}
    claims = {claim.get("claim_id"): claim for claim in claim_ledger.get("claims", [])}
    decisions = [
        evaluate_decision(rule, gates=gates, artifacts=artifacts, claims=claims, lineage=artifact_lineage)
        for rule in DECISION_RULES
    ]
    counts: dict[str, int] = {}
    for decision in decisions:
        counts[decision["status"]] = counts.get(decision["status"], 0) + 1
    return {
        "schema": DECISION_PROTOCOL_SCHEMA,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "source": {
            "evidence_pack_schema": evidence_pack.get("schema"),
            "claim_ledger_schema": claim_ledger.get("schema"),
            "artifact_lineage_schema": artifact_lineage.get("schema"),
            "claim_level": evidence_pack.get("claim_level", {}).get("level"),
            "lineage_reproducible": artifact_lineage.get("summary", {}).get("reproducible"),
        },
        "summary": {
            "decision_count": len(decisions),
            "allowed_count": counts.get("allowed", 0),
            "blocked_count": counts.get("blocked", 0),
            "qualified_count": counts.get("qualified", 0),
            "public_claim_ceiling": evidence_pack.get("claim_level", {}).get("level", "unknown"),
        },
        "protocol_policy": {
            "pre_registered_before_claim_promotion": True,
            "blocked_decisions_must_not_be_reworded_as_conclusions": True,
            "decision_protocol_is_post_pack": True,
            "reason": "This protocol consumes the evidence pack, claim ledger, and lineage audit, so it is generated after them.",
        },
        "decisions": decisions,
    }


def evaluate_decision(
    rule: DecisionRule,
    *,
    gates: dict[str | None, dict[str, Any]],
    artifacts: dict[str | None, dict[str, Any]],
    claims: dict[str | None, dict[str, Any]],
    lineage: dict[str, Any],
) -> dict[str, Any]:
    failed_gates = [code for code in rule.required_gates if not bool(gates.get(code, {}).get("passed"))]
    missing_artifacts = [
        role
        for role in rule.required_artifacts
        if not (artifacts.get(role) and artifacts.get(role, {}).get("exists", True) and artifacts.get(role, {}).get("sha256"))
    ]
    claim = claims.get(rule.claim_id, {})
    claim_status = claim.get("status", "missing")
    lineage_ok = bool(lineage.get("summary", {}).get("reproducible"))
    lineage_blocked = rule.required_lineage_reproducible and not lineage_ok
    blocking_items = [
        *[f"gate:{code}" for code in failed_gates],
        *[f"artifact:{role}" for role in missing_artifacts],
        *([] if claim_status == "allowed" else [f"claim:{rule.claim_id}:{claim_status}"]),
        *([] if not lineage_blocked else ["lineage:not_reproducible"]),
    ]
    status = "allowed" if not blocking_items else "blocked"
    return {
        "decision_id": rule.decision_id,
        "title": rule.title,
        "track": rule.track,
        "claim_id": rule.claim_id,
        "status": status,
        "threshold": rule.threshold,
        "statement": rule.allowed_statement if status == "allowed" else rule.blocked_statement,
        "blocking_items": blocking_items,
        "required_gates": [
            {
                "code": code,
                "passed": bool(gates.get(code, {}).get("passed")),
                "severity": gates.get(code, {}).get("severity", "missing"),
            }
            for code in rule.required_gates
        ],
        "required_artifacts": [
            {
                "role": role,
                "present": bool(
                    artifacts.get(role)
                    and artifacts.get(role, {}).get("exists", True)
                    and artifacts.get(role, {}).get("sha256")
                ),
            }
            for role in rule.required_artifacts
        ],
        "lineage_reproducible": lineage_ok,
        "next_action": next_action_for(rule.decision_id, blocking_items),
    }


def next_action_for(decision_id: str, blocking_items: list[str]) -> str:
    if not blocking_items:
        return "Keep limitations attached and preserve current evidence snapshots."
    if decision_id == "promote_real_world_generator_attribution":
        return "Collect accepted OpenSSL/BoringSSL aggregate baselines, complete provenance, and export labelled classifier vectors."
    if decision_id == "promote_bitcoin_nonce_risk_attribution":
        return "Bundle a public-safe Bitcoin nonce-risk report from owned or public metadata summaries."
    if any(item.startswith("lineage:") for item in blocking_items):
        return "Regenerate evidence pack, claim ledger, and artifact lineage before publishing."
    return "Regenerate missing evidence artifacts and rerun publication gates."
