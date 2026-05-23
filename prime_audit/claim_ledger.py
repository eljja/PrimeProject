from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


CLAIM_LEDGER_SCHEMA = "primeproject.claim-ledger.v1"


@dataclass(frozen=True)
class ClaimSpec:
    claim_id: str
    title: str
    category: str
    claim_level: str
    public_statement: str
    required_gates: tuple[str, ...]
    required_artifacts: tuple[str, ...]
    advisory_gates: tuple[str, ...] = ()
    blocked_statement: str = "Do not publish this as a supported conclusion yet."


CLAIM_SPECS: tuple[ClaimSpec, ...] = (
    ClaimSpec(
        claim_id="prime_measure_visualization",
        title="Prime-measure visualization is reproducible enough for public demo use",
        category="visualization",
        claim_level="visual_demo",
        public_statement=(
            "The GitHub Pages visualizations may be described as reproducible exploratory "
            "views over bundled/live prime-measure experiments."
        ),
        required_gates=("reproducibility_gate",),
        required_artifacts=("snapshot_manifest",),
        advisory_gates=("sensitive_publication_gate",),
    ),
    ClaimSpec(
        claim_id="synthetic_generator_attribution",
        title="Controlled synthetic generator fingerprints are observable",
        category="controlled_validation",
        claim_level="controlled_synthetic",
        public_statement=(
            "Synthetic generator families can be compared under controlled experiments, "
            "with bit-length confounds explicitly reported."
        ),
        required_gates=("controlled_signal_gate",),
        required_artifacts=("attribution_grid",),
        advisory_gates=("reproducibility_gate",),
    ),
    ClaimSpec(
        claim_id="real_world_generator_attribution",
        title="Real-world library generator attribution is supported",
        category="sim_to_real",
        claim_level="real_world_candidate",
        public_statement=(
            "Real-world OpenSSL/BoringSSL/Go-style attribution may be described only after "
            "baseline, provenance, classifier, and acceptance gates pass."
        ),
        required_gates=(
            "real_baseline_gate",
            "classifier_gate",
            "provenance_gate",
            "provenance_audit_gate",
            "baseline_acceptance_gate",
            "collection_intake_gate",
        ),
        required_artifacts=("manifest", "readiness", "baseline_acceptance", "collection_intake"),
        advisory_gates=("promotion_plan_gate",),
        blocked_statement=(
            "Do not claim real-world generator attribution. Current evidence is a scaffold "
            "and planning system, not accepted attribution evidence."
        ),
    ),
    ClaimSpec(
        claim_id="bitcoin_nonce_risk_attribution",
        title="Bitcoin wallet/library nonce-risk attribution is supported",
        category="bitcoin",
        claim_level="wallet_nonce_candidate",
        public_statement=(
            "Bitcoin nonce-risk attribution may be discussed only with a bundled risk report "
            "and linked wallet/library baseline evidence."
        ),
        required_gates=("bitcoin_integration_gate",),
        required_artifacts=("bitcoin_risk_report",),
        advisory_gates=("real_baseline_gate", "provenance_gate"),
        blocked_statement=(
            "Do not claim Bitcoin wallet/library attribution. Public secp256k1 constants are "
            "not the risk surface; nonce metadata evidence is still missing."
        ),
    ),
    ClaimSpec(
        claim_id="public_safety_and_reproducibility",
        title="Public artifact bundle is safe enough to inspect",
        category="publication",
        claim_level="publication_scaffold",
        public_statement=(
            "The public bundle can be inspected as a defensive research scaffold with private "
            "key material and sensitive prime samples excluded."
        ),
        required_gates=("sensitive_publication_gate", "reproducibility_gate"),
        required_artifacts=("manifest", "readiness", "project_evolution"),
        advisory_gates=("provenance_gate", "provenance_audit_gate", "promotion_plan_gate"),
    ),
)


def build_claim_ledger(
    evidence_pack: dict[str, Any],
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    gates = {gate.get("code"): gate for gate in evidence_pack.get("publication_gates", [])}
    artifacts = {artifact.get("role"): artifact for artifact in evidence_pack.get("artifacts", [])}
    claims = [_evaluate_claim(spec, gates, artifacts) for spec in CLAIM_SPECS]
    status_counts: dict[str, int] = {}
    for claim in claims:
        status_counts[claim["status"]] = status_counts.get(claim["status"], 0) + 1

    blocked = [claim for claim in claims if claim["status"] == "blocked"]
    return {
        "schema": CLAIM_LEDGER_SCHEMA,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "source": {
            "schema": evidence_pack.get("schema"),
            "claim_level": evidence_pack.get("claim_level", {}).get("level"),
            "failed_gate_count": evidence_pack.get("claim_level", {}).get("failed_gate_count", 0),
        },
        "summary": {
            "claim_count": len(claims),
            "allowed_count": status_counts.get("allowed", 0),
            "qualified_count": status_counts.get("qualified", 0),
            "blocked_count": status_counts.get("blocked", 0),
            "public_claim_ceiling": evidence_pack.get("claim_level", {}).get("level", "unknown"),
        },
        "publication_policy": {
            "blocked_claims_must_not_be_conclusions": True,
            "qualified_claims_need_limitations_attached": True,
            "allowed_claims_remain_scoped_to_their_claim_level": True,
            "review_note": (
                "The ledger derives from the evidence pack and is intentionally kept outside "
                "that pack's checksum list to avoid circular artifact hashing."
            ),
        },
        "claims": claims,
        "blocked_claim_ids": [claim["claim_id"] for claim in blocked],
    }


def _evaluate_claim(
    spec: ClaimSpec,
    gates: dict[str | None, dict[str, Any]],
    artifacts: dict[str | None, dict[str, Any]],
) -> dict[str, Any]:
    gate_rows = [_gate_status(code, gates.get(code)) for code in spec.required_gates]
    advisory_rows = [_gate_status(code, gates.get(code)) for code in spec.advisory_gates]
    artifact_rows = [_artifact_status(role, artifacts.get(role)) for role in spec.required_artifacts]
    failed_required_gates = [row["code"] for row in gate_rows if not row["passed"]]
    missing_required_artifacts = [row["role"] for row in artifact_rows if not row["present"]]
    failed_advisory_gates = [row["code"] for row in advisory_rows if not row["passed"]]

    if failed_required_gates or missing_required_artifacts:
        status = "blocked"
        statement = spec.blocked_statement
    elif failed_advisory_gates:
        status = "qualified"
        statement = spec.public_statement
    else:
        status = "allowed"
        statement = spec.public_statement

    return {
        "claim_id": spec.claim_id,
        "title": spec.title,
        "category": spec.category,
        "claim_level": spec.claim_level,
        "status": status,
        "public_statement": statement,
        "required_gates": gate_rows,
        "advisory_gates": advisory_rows,
        "required_artifacts": artifact_rows,
        "failed_required_gates": failed_required_gates,
        "failed_advisory_gates": failed_advisory_gates,
        "missing_required_artifacts": missing_required_artifacts,
    }


def _gate_status(code: str, gate_item: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "code": code,
        "present": gate_item is not None,
        "passed": bool(gate_item and gate_item.get("passed")),
        "severity": gate_item.get("severity") if gate_item else "missing",
    }


def _artifact_status(role: str, artifact: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "role": role,
        "present": bool(artifact and artifact.get("exists", True) and artifact.get("sha256")),
        "schema": artifact.get("schema") if artifact else None,
        "sha256": artifact.get("sha256") if artifact else None,
    }
