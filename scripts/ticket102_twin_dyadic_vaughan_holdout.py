from __future__ import annotations

import gc
import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import mobius_values
from ticket100_extended_residual_vaughan_audit import SCREEN_START, lambda_values, vaughan_components
from ticket101_vaughan_cutoff_energy_audit import build_external_main_arrays


GENERATED_AT = "2026-07-13T09:20:00+09:00"
SCHEMA = "primeproject.ticket102-twin-dyadic-vaughan-holdout.v1"
HORIZONS = (125_000, 250_000, 500_000, 1_000_000, 2_000_000, 4_000_000)
CALIBRATION_MAXIMUM = 1_000_000
CUTOFF_RATIO = 0.84
STRUCTURED_BUDGET = 1.40
TYPE_II_BUDGET = 0.18
RESCUE_HORIZON = 8_000_000
RESCUE_STRUCTURED_BUDGET = 4.0
RESCUE_TYPE_II_BUDGET = 1.0
MINIMUM_TYPE_II_SUPPORT_FRACTION = 0.01


def cutoff_schedule(horizon: int, ratio: float = CUTOFF_RATIO) -> tuple[int, int]:
    """Pre-registered scale-local cutoffs; no observed correlation enters this rule."""
    u = max(2, round(horizon ** (1 / 3)))
    v = max(2, round(ratio * u))
    return u, v


def _maximum_row(numbers: np.ndarray, contribution: np.ndarray, main: np.ndarray) -> dict[str, Any]:
    required = np.maximum(0.0, -contribution / main) * np.log(numbers)
    position = int(np.argmax(required))
    return {
        "x": int(numbers[position]),
        "required_log_envelope_constant": float(required[position]),
        "contribution_over_external_main": float(contribution[position] / main[position]),
    }


def audit_horizon(
    horizon: int,
    ratio: float = CUTOFF_RATIO,
    structured_budget: float = STRUCTURED_BUDGET,
    type_ii_budget: float = TYPE_II_BUDGET,
) -> dict[str, Any]:
    if horizon < 2 * SCREEN_START:
        raise ValueError("horizon must leave a nonempty scheduled holdout block")
    u, v = cutoff_schedule(horizon, ratio)
    values, mangoldt = lambda_values(horizon + 2)
    mu = mobius_values(horizon + 2)
    type_i, type_ii, identity = vaughan_components(values, mangoldt, mu, u, v, 0)
    exact = np.cumsum(values[: horizon + 1] * values[2 : horizon + 3])
    structured_correlation = np.cumsum(type_i[: horizon + 1] * values[2 : horizon + 3])
    type_ii_correlation = np.cumsum(type_ii[: horizon + 1] * values[2 : horizon + 3])
    _, twin_main, _, twin_mask = build_external_main_arrays(horizon)
    lower = max(SCREEN_START, horizon // 2 + 1)
    numbers = np.flatnonzero(twin_mask & (np.arange(horizon + 1) >= lower))
    if len(numbers) == 0:
        raise ValueError("scheduled holdout block is empty")
    main = twin_main[numbers]
    structured = structured_correlation[numbers] - main
    type_ii_part = type_ii_correlation[numbers]
    structured_required = np.maximum(0.0, -structured / main) * np.log(numbers)
    type_ii_required = np.maximum(0.0, -type_ii_part / main) * np.log(numbers)
    joint = structured + type_ii_part
    reconstruction_delta = np.abs((joint + main) - exact[numbers])
    reconstruction_error = float(np.max(reconstruction_delta))
    reconstruction_relative_error = float(
        np.max(reconstruction_delta / np.maximum(1.0, np.abs(exact[numbers])))
    )
    support_count = int(np.count_nonzero(np.abs(type_ii[: horizon + 1]) > 1e-12))
    support_fraction = support_count / (horizon + 1)
    structured_failures = int(np.count_nonzero(structured_required > structured_budget + 1e-12))
    type_ii_failures = int(np.count_nonzero(type_ii_required > type_ii_budget + 1e-12))
    return {
        "horizon": horizon,
        "holdout_start": int(numbers[0]),
        "holdout_end": int(numbers[-1]),
        "evaluated_count": len(numbers),
        "u": u,
        "v": v,
        "cutoff_ratio": ratio,
        "uv_over_horizon": u * v / horizon,
        "type_ii_support_count": support_count,
        "type_ii_support_fraction": support_fraction,
        "noncollapse_contract_passes": support_fraction >= MINIMUM_TYPE_II_SUPPORT_FRACTION,
        "structured": {
            "budget": structured_budget,
            "failure_count": structured_failures,
            "maximum_row": _maximum_row(numbers, structured, main),
        },
        "type_ii": {
            "budget": type_ii_budget,
            "failure_count": type_ii_failures,
            "maximum_row": _maximum_row(numbers, type_ii_part, main),
        },
        "separate_budget_sum": structured_budget + type_ii_budget,
        "observed_maximum_sum": float(np.max(structured_required)) + float(np.max(type_ii_required)),
        "joint_reconstruction_max_absolute_error": reconstruction_error,
        "joint_reconstruction_max_relative_error": reconstruction_relative_error,
        "lambda_reconstruction_max_error": identity["lambda_reconstruction_max_error"],
    }


def audit_dyadic_holdouts(horizons: tuple[int, ...] = HORIZONS) -> dict[str, Any]:
    if any(right != 2 * left for left, right in zip(horizons, horizons[1:])):
        raise ValueError("horizons must double so their half-open holdout blocks cover a tail")
    rows: list[dict[str, Any]] = []
    for horizon in horizons:
        row = audit_horizon(horizon)
        row["split"] = "calibration_replay" if horizon <= CALIBRATION_MAXIMUM else "post_selection_holdout"
        rows.append(row)
        gc.collect()
    holdout_rows = [row for row in rows if row["split"] == "post_selection_holdout"]
    structured_failures = sum(int(row["structured"]["failure_count"]) for row in holdout_rows)
    type_ii_failures = sum(int(row["type_ii"]["failure_count"]) for row in holdout_rows)
    noncollapse_failures = sum(int(not row["noncollapse_contract_passes"]) for row in rows)
    reconstruction_failures = sum(
        int(float(row["joint_reconstruction_max_relative_error"]) > 1e-12)
        + int(float(row["lambda_reconstruction_max_error"]) > 1e-10)
        for row in rows
    )
    worst_structured = max(rows, key=lambda row: float(row["structured"]["maximum_row"]["required_log_envelope_constant"]))
    worst_type_ii = max(rows, key=lambda row: float(row["type_ii"]["maximum_row"]["required_log_envelope_constant"]))
    return {
        "schedule": "X doubles; U(X)=round(X^(1/3)); V(X)=round(0.84 U(X)); audit every x in (X/2,X]",
        "selection_boundary": "The ratio 0.84 and budgets 1.40/0.18 were selected at or below 1M; only horizons above 1M are post-selection holdouts.",
        "tail_coverage_start": horizons[0] // 2 + 1,
        "tail_coverage_end": horizons[-1],
        "row_count": len(rows),
        "calibration_row_count": len(rows) - len(holdout_rows),
        "holdout_row_count": len(holdout_rows),
        "holdout_evaluated_count": sum(int(row["evaluated_count"]) for row in holdout_rows),
        "holdout_structured_failure_count": structured_failures,
        "holdout_type_ii_failure_count": type_ii_failures,
        "noncollapse_failure_count": noncollapse_failures,
        "reconstruction_failure_count": reconstruction_failures,
        "worst_structured_row": worst_structured,
        "worst_type_ii_row": worst_type_ii,
        "rows": rows,
    }


def analyze_ticket102() -> dict[str, Any]:
    dyadic = audit_dyadic_holdouts()
    registered_candidate_refuted = bool(
        dyadic["holdout_structured_failure_count"]
        or dyadic["holdout_type_ii_failure_count"]
        or dyadic["noncollapse_failure_count"]
    )
    rescue = audit_horizon(
        RESCUE_HORIZON,
        structured_budget=RESCUE_STRUCTURED_BUDGET,
        type_ii_budget=RESCUE_TYPE_II_BUDGET,
    )
    rescue_failures = (
        int(rescue["structured"]["failure_count"])
        + int(rescue["type_ii"]["failure_count"])
        + int(not rescue["noncollapse_contract_passes"])
    )
    contract_failures = int(dyadic["reconstruction_failure_count"]) + int(
        float(rescue["joint_reconstruction_max_relative_error"]) > 1e-12
        or float(rescue["lambda_reconstruction_max_error"]) > 1e-10
    )
    return {
        "theorem_name": "DyadicScaleLocalSeparatedVaughanTwinBudgetAudit",
        "source_ticket": "TICKET-101",
        "dyadic_holdout_audit": dyadic,
        "registered_candidate_status": "finite_1p40_plus_0p18_candidate_refuted_on_post_selection_holdout" if registered_candidate_refuted else "finite_1p40_plus_0p18_candidate_survives_post_selection_holdout_not_a_theorem",
        "fresh_rescue_holdout": {
            "selection_rule": "After the 1.40 budget failed by requiring 1.953 below 4M, pre-register coarse finite budgets K_S=4 and K_II=1, then evaluate the previously unseen 8M block.",
            "row": rescue,
            "failure_count": rescue_failures,
            "status": "coarse_finite_budget_survives_fresh_8m_holdout_not_a_theorem" if rescue_failures == 0 else "coarse_finite_budget_refuted_on_fresh_8m_holdout",
        },
        "constant_threshold_correction": {
            "finding": "The former K=1.6 cutoff was a finite calibration threshold, not a mathematical sufficiency threshold.",
            "exact_implication": "If structured >= -K_S M/log(x) and TypeII >= -K_II M/log(x) for any fixed finite K_S,K_II, then C_2(x)>=M(x)(1-(K_S+K_II)/log(x)).",
            "why_sufficient": "The external local main is linear up to a lower-order modulus loss, while proper-prime-power contamination is o(x); hence any fixed finite K_S+K_II leaves genuine twin weight eventually positive and unbounded.",
            "consequence": "Retire optimization against 1.6 as a proof gate. The real theorem asks for horizon-uniform finite constants with a noncollapsed Type II range.",
        },
        "logical_upgrade": {
            "sufficient_all_scale_statement": "There exist fixed finite K_S,K_II such that for every sufficiently large dyadic X and every x in (X/2,X], the scale-local structured and Type II residuals satisfy their K/log bounds.",
            "coverage": "The dyadic blocks cover every sufficiently large integer x; an all-scale theorem plus the exact TICKET93 contamination bridge would imply twin-prime infinitude.",
            "missing": "A finite holdout does not prove either uniform component inequality or break the parity barrier.",
        },
        "literature_boundary": {
            "ford_maynard": "Substantial Type II information is necessary in general prime-producing lower-bound sieves; finite component traces are not such an estimate.",
            "green_tao": "Finite-complexity transference excludes affinely related binary forms such as n and n+2, so it does not supply this target.",
        },
        "discarded_routes": [
            "Treat the 1M-selected cutoff ratio as independent validation.",
            "Audit only the terminal horizon instead of every x in a covering dyadic block.",
            "Allow Type II support to collapse while calling the split a bilinear estimate.",
            "Require K_S+K_II<=1.6 even though every fixed finite sum is asymptotically sufficient.",
            "Infer a uniform theorem from stable finite constants.",
        ],
        "next_theorem_target": "UniformFiniteDyadicSeparatedVaughanTwinBudgets",
        "machine_audit": {
            "maximum_horizon": RESCUE_HORIZON,
            "holdout_evaluated_count": dyadic["holdout_evaluated_count"],
            "holdout_structured_failure_count": dyadic["holdout_structured_failure_count"],
            "holdout_type_ii_failure_count": dyadic["holdout_type_ii_failure_count"],
            "fresh_rescue_evaluated_count": rescue["evaluated_count"],
            "fresh_rescue_failure_count": rescue_failures,
            "noncollapse_failure_count": dyadic["noncollapse_failure_count"],
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET102 is an out-of-selection finite falsification audit. It proves neither Twin Prime nor any of the other three conjectures and certifies no conjecture counterexample.",
    }


def transferred_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str, correction: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_priority_corrected_open",
        "route": route,
        "proof_or_counterexample_mode": "problem-specific priority correction after Twin holdout audit",
        "attempt": correction,
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "independent_target": target},
        "obstruction": "TICKET102 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": correction,
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket101 = read_json(ROOT / "data/open-problem/ticket101-vaughan-cutoff-energy-audit.json")
    audit = analyze_ticket102()
    attempts = [
        transferred_attempt(
            ticket101,
            "riemann",
            "RH-TICKET-102",
            "IndependentKernelPositivityBeforeEnergyRewrite",
            "NonCircularExplicitFormulaKernelPositivity",
            "Formalize one exact Weil/explicit-formula criterion and seek positivity not algebraically equivalent to RH.",
        ),
        transferred_attempt(
            ticket101,
            "collatz",
            "CO-TICKET-102",
            "GoldenMeanInvariantSetEscapePriorityCorrection",
            "GoldenMeanInvariantSetEscape",
            "Restore the TICKET91 problem-specific target: prove escape of the exact 2-adic logarithm tail orbit from the no-00 subshift, or realize a compatible infinite avoiding path.",
        ),
        transferred_attempt(
            ticket101,
            "goldbach",
            "GB-TICKET-102",
            "JointBalancedVaughanGoldbachPriority",
            "JointBalancedVaughanGoldbachResidualEnvelope",
            "Keep signed structured-plus-Type-II compensation and derive a uniform joint estimate with explicit cutoff; separated budgets remain refuted.",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-102",
            "status": audit["registered_candidate_status"],
            "route": "DyadicScaleLocalSeparatedVaughanTwinBudgetAudit",
            "proof_or_counterexample_mode": "post-selection dyadic exhaustive counterexample search",
            "attempt": "Freeze the TICKET101 cutoff rule and component budgets before evaluating every x in unseen dyadic blocks above 1M.",
            "bounded_result": {"source_ticket": "TP-TICKET-101", "audit_ref": "twin_dyadic_vaughan_holdout"},
            "obstruction": audit["logical_upgrade"]["missing"],
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Retire the 1.40/0.18 thresholds, preserve the fresh K_S=4,K_II=1 falsification record, and derive any fixed finite analytic component bounds uniform on dyadic blocks.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": audit["registered_candidate_status"],
        "claim_boundary": audit["proof_boundary"],
        "twin_dyadic_vaughan_holdout": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket102-twin-dyadic-vaughan-holdout.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-102-kernel-positivity-priority.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-102-golden-mean-priority.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-102-joint-balanced-priority.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-102-dyadic-vaughan-holdout.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
