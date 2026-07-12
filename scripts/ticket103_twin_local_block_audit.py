from __future__ import annotations

import gc
import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import mobius_values
from ticket100_extended_residual_vaughan_audit import (
    lambda_values,
    schedule_moduli,
    twin_main_vector,
    vaughan_components,
)
from ticket102_twin_dyadic_vaughan_holdout import cutoff_schedule


GENERATED_AT = "2026-07-13T11:10:00+09:00"
SCHEMA = "primeproject.ticket103-twin-local-block-audit.v1"
HORIZONS = (125_000, 250_000, 500_000, 1_000_000, 2_000_000, 4_000_000, 8_000_000)
SMALL_SIGN_PROBES = (1_000, 2_000, 4_000, 8_000, 16_000, 32_000, 64_000)
MINIMUM_TYPE_II_SUPPORT_FRACTION = 0.01


def audit_local_block(horizon: int) -> dict[str, Any]:
    if horizon < 4:
        raise ValueError("horizon must define a nonempty upper-half block")
    lower = horizon // 2 + 1
    u, v = cutoff_schedule(horizon)
    values, mangoldt = lambda_values(horizon + 2)
    mu = mobius_values(horizon + 2)
    type_i, type_ii, identity = vaughan_components(values, mangoldt, mu, u, v, 0)
    modulus = schedule_moduli(horizon)[-1]
    endpoints = np.array([lower - 1, horizon], dtype=np.int64)
    endpoint_main = twin_main_vector(endpoints, modulus)
    local_main = float(endpoint_main[1] - endpoint_main[0])
    if local_main <= 0:
        raise ValueError("local external main must be positive")

    shifted = values[lower + 2 : horizon + 3]
    exact = float(np.dot(values[lower : horizon + 1], shifted))
    structured_correlation = float(np.dot(type_i[lower : horizon + 1], shifted))
    type_ii_correlation = float(np.dot(type_ii[lower : horizon + 1], shifted))
    structured_residual = structured_correlation - local_main
    reconstruction_error = abs(exact - structured_correlation - type_ii_correlation)
    reconstruction_relative_error = reconstruction_error / max(1.0, abs(exact))
    support_count = int(np.count_nonzero(np.abs(type_ii[lower : horizon + 1]) > 1e-12))
    block_length = horizon - lower + 1
    support_fraction = support_count / block_length

    return {
        "horizon": horizon,
        "block_start": lower,
        "block_end": horizon,
        "block_length": block_length,
        "u": u,
        "v": v,
        "modulus": modulus,
        "local_external_main": local_main,
        "exact_local_correlation": exact,
        "structured_local_correlation": structured_correlation,
        "structured_residual": structured_residual,
        "type_ii_local_correlation": type_ii_correlation,
        "structured_required_constant": max(0.0, -structured_residual / local_main) * math.log(horizon),
        "type_ii_required_constant": max(0.0, -type_ii_correlation / local_main) * math.log(horizon),
        "joint_required_constant": max(
            0.0,
            -(structured_residual + type_ii_correlation) / local_main,
        )
        * math.log(horizon),
        "type_ii_is_nonnegative": type_ii_correlation >= 0,
        "type_ii_support_count": support_count,
        "type_ii_support_fraction": support_fraction,
        "noncollapse_contract_passes": support_fraction >= MINIMUM_TYPE_II_SUPPORT_FRACTION,
        "reconstruction_absolute_error": reconstruction_error,
        "reconstruction_relative_error": reconstruction_relative_error,
        "lambda_reconstruction_max_error": identity["lambda_reconstruction_max_error"],
    }


def audit_local_blocks(horizons: tuple[int, ...] = HORIZONS) -> dict[str, Any]:
    if any(right != 2 * left for left, right in zip(horizons, horizons[1:])):
        raise ValueError("horizons must form a doubling schedule")
    rows: list[dict[str, Any]] = []
    for horizon in horizons:
        rows.append(audit_local_block(horizon))
        gc.collect()
    negative_rows = [row for row in rows if not row["type_ii_is_nonnegative"]]
    contract_failures = sum(
        int(float(row["reconstruction_relative_error"]) > 1e-12)
        + int(float(row["lambda_reconstruction_max_error"]) > 1e-10)
        + int(not row["noncollapse_contract_passes"])
        for row in rows
    )
    return {
        "definition": "For each dyadic X, decompose only the exact shift-two correlation on n in (X/2,X] and subtract a fixed-W external main on the same block.",
        "why_local": "Cumulative 0..x component sums can hide a negative current-block contribution behind earlier positive mass; local blocks match standard dyadic analytic estimates.",
        "row_count": len(rows),
        "evaluated_integer_count": sum(int(row["block_length"]) for row in rows),
        "negative_type_ii_block_count": len(negative_rows),
        "contract_failure_count": contract_failures,
        "maximum_structured_required_constant": max(float(row["structured_required_constant"]) for row in rows),
        "maximum_type_ii_required_constant": max(float(row["type_ii_required_constant"]) for row in rows),
        "maximum_joint_required_constant": max(float(row["joint_required_constant"]) for row in rows),
        "first_negative_type_ii_row": negative_rows[0] if negative_rows else None,
        "rows": rows,
    }


def analyze_ticket103() -> dict[str, Any]:
    local = audit_local_blocks()
    small_rows = [audit_local_block(horizon) for horizon in SMALL_SIGN_PROBES]
    small_negative_rows = [row for row in small_rows if not row["type_ii_is_nonnegative"]]
    type_ii_nonnegativity_refuted = bool(small_negative_rows)
    return {
        "theorem_name": "DyadicLocalVaughanTwinBlockAudit",
        "source_ticket": "TICKET-102",
        "local_block_audit": local,
        "small_scale_sign_oracle": {
            "purpose": "Determine whether local Type II nonnegativity is an algebraic consequence before treating the large-block sign pattern as a theorem candidate.",
            "probe_count": len(small_rows),
            "negative_block_count": len(small_negative_rows),
            "first_counterexample": small_negative_rows[0] if small_negative_rows else None,
            "rows": small_rows,
        },
        "cumulative_to_local_verdict": "universal_local_type_ii_nonnegativity_refuted_eventual_finite_bound_open" if type_ii_nonnegativity_refuted else "no_local_negative_type_ii_block_found_finitely",
        "conditional_bridge": {
            "premise": "There exist fixed finite K_S,K_II such that every sufficiently large dyadic block has structured residual >= -K_S M_X/log X and Type II correlation >= -K_II M_X/log X.",
            "conclusion": "The exact Lambda shift-two mass is positive linear on every sufficiently large block; after o(X) prime-power contamination, each block contains genuine twin-prime weight.",
            "status": "exact sufficient implication; uniform component premises remain open",
        },
        "discarded_routes": [
            "Use cumulative Type II nonnegativity as evidence for a local bilinear estimate.",
            "Claim local Type II nonnegativity as an identity; X=1000 is an exact finite counterexample.",
            "Let the local model modulus change inside one block.",
            "Call support density an analytic Type II bound.",
            "Promote the maximum observed finite constants to uniform constants.",
        ],
        "next_theorem_target": "UniformDyadicLocalVaughanTwinBlockBudgets",
        "machine_audit": {
            "maximum_horizon": HORIZONS[-1],
            "evaluated_integer_count": local["evaluated_integer_count"],
            "negative_type_ii_block_count": local["negative_type_ii_block_count"],
            "small_sign_negative_block_count": len(small_negative_rows),
            "contract_failure_count": local["contract_failure_count"],
        },
        "proof_boundary": "TICKET103 audits exact local dyadic decompositions and may refute a cumulative-to-local proof shortcut. It proves neither Twin Prime nor any other conjecture and certifies no conjecture counterexample.",
    }


def transferred_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target while Twin local-block audit advances",
        "attempt": "Preserve the problem-specific infinite target; TICKET103 adds no cross-problem energy shortcut.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "independent_target": target},
        "obstruction": "No new target-specific infinite theorem is supplied for this problem in TICKET103.",
        "candidate_theorem": target,
        "next_experiment": f"Continue the independent target {target} with its own falsification oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket102 = read_json(ROOT / "data/open-problem/ticket102-twin-dyadic-vaughan-holdout.json")
    audit = analyze_ticket103()
    attempts = [
        transferred_attempt(ticket102, "riemann", "RH-TICKET-103", "NonCircularKernelPositivityPreserved", "NonCircularExplicitFormulaKernelPositivity"),
        transferred_attempt(ticket102, "collatz", "CO-TICKET-103", "GoldenMeanEscapePreserved", "GoldenMeanInvariantSetEscape"),
        transferred_attempt(ticket102, "goldbach", "GB-TICKET-103", "JointBalancedGoldbachPreserved", "JointBalancedVaughanGoldbachResidualEnvelope"),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-103",
            "status": audit["cumulative_to_local_verdict"],
            "route": "DyadicLocalVaughanTwinBlockAudit",
            "proof_or_counterexample_mode": "exact local-block counterexample search",
            "attempt": "Replace cumulative component traces by exact fixed-model correlations on each upper-half dyadic block.",
            "bounded_result": {"source_ticket": "TP-TICKET-102", "audit_ref": "twin_local_block_audit"},
            "obstruction": "Finite local constants and support counts do not prove uniform Type II estimates.",
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Derive or refute fixed finite local component bounds using genuine bilinear estimates, not cumulative mass.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": audit["cumulative_to_local_verdict"],
        "claim_boundary": audit["proof_boundary"],
        "twin_local_block_audit": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket103-twin-local-block-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-103-kernel-positivity-preserved.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-103-golden-mean-preserved.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-103-joint-balanced-preserved.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-103-local-block-audit.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
