from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


FALSIFICATION_BATTERY_SCHEMA = "primeproject.falsification-battery.v1"


def build_falsification_battery(
    *,
    attribution_grid: dict[str, Any],
    decision_protocol: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    random_baseline = float(attribution_grid.get("random_baseline_accuracy", 0.0) or 0.0)
    profiles = attribution_grid.get("summary", {}).get("profiles", {}) or {}
    rows = attribution_grid.get("rows", []) or []
    decisions = {
        decision.get("decision_id"): decision
        for decision in decision_protocol.get("decisions", [])
    }
    checks = [
        paired_control_presence(rows),
        controlled_signal_above_random(profiles, random_baseline),
        bit_length_confound_guard(profiles, random_baseline),
        negative_control_floor(profiles, random_baseline),
        claim_promotion_guard(decisions),
    ]
    counts: dict[str, int] = {}
    for check in checks:
        counts[check["status"]] = counts.get(check["status"], 0) + 1
    fail_count = counts.get("fail", 0)
    warn_count = counts.get("warn", 0)
    claim_floor = "do_not_promote" if fail_count else "controlled_synthetic_only"
    return {
        "schema": FALSIFICATION_BATTERY_SCHEMA,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "source": {
            "attribution_grid_schema": attribution_grid.get("schema"),
            "decision_protocol_schema": decision_protocol.get("schema"),
            "random_baseline_accuracy": random_baseline,
            "controlled_profiles": robust_controlled_profiles(profiles),
        },
        "summary": {
            "check_count": len(checks),
            "pass_count": counts.get("pass", 0),
            "warn_count": warn_count,
            "fail_count": fail_count,
            "claim_floor": claim_floor,
            "interpretation": interpretation_for(claim_floor, warn_count),
        },
        "downgrade_triggers": [
            "missing_paired_controls",
            "bit_length_only_survives_control",
            "negative_controls_exceed_floor",
            "decision_protocol_promotes_blocked_claim",
            "real_world_or_bitcoin_claim_without_bundled_evidence",
        ],
        "checks": checks,
    }


def paired_control_presence(rows: list[dict[str, Any]]) -> dict[str, Any]:
    control_modes = sorted({str(row.get("control_mode", "none")) for row in rows})
    required = {"none", "bit_length"}
    present = required.issubset(set(control_modes))
    return check_result(
        "paired_control_presence",
        "pass" if present else "fail",
        "critical",
        "Paired uncontrolled and bit-length-controlled attribution rows are present."
        if present
        else "Attribution grid is missing paired uncontrolled or bit-length-controlled rows.",
        {"control_modes": control_modes, "required": sorted(required)},
    )


def controlled_signal_above_random(
    profiles: dict[str, Any],
    random_baseline: float,
) -> dict[str, Any]:
    robust_profiles = [
        {
            "profile": profile,
            "mean_controlled_accuracy": round_float(summary.get("mean_controlled_accuracy")),
            "robust_interpretation": summary.get("robust_interpretation"),
        }
        for profile, summary in profiles.items()
        if is_profile_above_random(summary, random_baseline)
        and "survives" in str(summary.get("robust_interpretation", ""))
    ]
    status = "pass" if robust_profiles else "warn"
    return check_result(
        "controlled_signal_above_random",
        status,
        "high",
        "At least one nontrivial profile remains above random after bit-length control."
        if robust_profiles
        else "No controlled profile is clearly above the random baseline; keep claims exploratory.",
        {
            "random_baseline_accuracy": round_float(random_baseline),
            "minimum_lift": 0.10,
            "profiles": robust_profiles,
        },
    )


def bit_length_confound_guard(profiles: dict[str, Any], random_baseline: float) -> dict[str, Any]:
    profile = profiles.get("bit_length_only", {}) or {}
    controlled = float(profile.get("mean_controlled_accuracy", 0.0) or 0.0)
    interpretation = str(profile.get("robust_interpretation", ""))
    passes = controlled <= random_baseline + 0.05 and "survives" not in interpretation
    return check_result(
        "bit_length_confound_guard",
        "pass" if passes else "fail",
        "critical",
        "The bit-length-only profile collapses near random after control."
        if passes
        else "Bit-length-only signal survives control; attribution is likely dominated by range leakage.",
        {
            "random_baseline_accuracy": round_float(random_baseline),
            "bit_length_only_controlled_accuracy": round_float(controlled),
            "robust_interpretation": interpretation or "missing",
        },
    )


def negative_control_floor(profiles: dict[str, Any], random_baseline: float) -> dict[str, Any]:
    negative_names = ("low_bits_only", "residue_only")
    floor = random_baseline + 0.20
    controls = []
    exceeding = []
    for name in negative_names:
        profile = profiles.get(name, {}) or {}
        controlled = float(profile.get("mean_controlled_accuracy", 0.0) or 0.0)
        entry = {
            "profile": name,
            "mean_controlled_accuracy": round_float(controlled),
            "robust_interpretation": profile.get("robust_interpretation", "missing"),
        }
        controls.append(entry)
        if controlled > floor:
            exceeding.append(entry)
    return check_result(
        "negative_control_floor",
        "pass" if not exceeding else "warn",
        "medium",
        "Low-bit and residue-only controls remain near the random floor."
        if not exceeding
        else "One or more negative controls exceeds the configured floor; downgrade feature-level claims.",
        {
            "random_baseline_accuracy": round_float(random_baseline),
            "floor": round_float(floor),
            "controls": controls,
            "exceeding": exceeding,
        },
    )


def claim_promotion_guard(decisions: dict[str | None, dict[str, Any]]) -> dict[str, Any]:
    blocked_required = (
        "promote_real_world_generator_attribution",
        "promote_bitcoin_nonce_risk_attribution",
    )
    promoted = [
        decision_id
        for decision_id in blocked_required
        if decisions.get(decision_id, {}).get("status") != "blocked"
    ]
    return check_result(
        "claim_promotion_guard",
        "pass" if not promoted else "fail",
        "critical",
        "Real-world and Bitcoin attribution promotion remain blocked until required evidence exists."
        if not promoted
        else "A high-risk claim promotion is not blocked by the decision protocol.",
        {
            "required_blocked_decisions": list(blocked_required),
            "unexpectedly_promoted": promoted,
        },
    )


def robust_controlled_profiles(profiles: dict[str, Any]) -> list[str]:
    return sorted(
        profile
        for profile, summary in profiles.items()
        if "survives" in str(summary.get("robust_interpretation", ""))
    )


def is_profile_above_random(summary: dict[str, Any], random_baseline: float) -> bool:
    controlled = float(summary.get("mean_controlled_accuracy", 0.0) or 0.0)
    return controlled >= random_baseline + 0.10


def interpretation_for(claim_floor: str, warn_count: int) -> str:
    if claim_floor == "do_not_promote":
        return "One or more critical falsification checks failed; do not promote attribution claims."
    if warn_count:
        return "Controlled synthetic reporting is possible, but warnings require visible limitations."
    return "Falsification battery supports controlled synthetic reporting only; real-world promotion stays blocked."


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


def round_float(value: Any) -> float:
    try:
        return round(float(value), 6)
    except (TypeError, ValueError):
        return 0.0
