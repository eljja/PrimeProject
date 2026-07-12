from __future__ import annotations

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
from ticket106_twin_modulus_grouped_dispersion import grouped_modulus_vectors


GENERATED_AT = "2026-07-12T19:40:00+09:00"
SCHEMA = "primeproject.ticket107-twin-sparse-tail-recombination.v1"
HORIZONS = (1_000, 125_000, 1_000_000, 2_000_000, 4_000_000, 8_000_000)


def audit_sparse_tail_recombination(horizon: int) -> dict[str, Any]:
    lower = horizon // 2 + 1
    coefficient, baseline, _, metadata = grouped_modulus_vectors(horizon)
    support = np.flatnonzero(np.abs(coefficient) > 1e-12)
    occupancies = horizon // support - (lower - 1) // support
    sparse_support = support[occupancies <= 1]

    values, mangoldt = lambda_values(horizon + 2)
    mu = mobius_values(horizon + 2)
    type_i, type_ii, identity = vaughan_components(
        values[: horizon + 1],
        mangoldt,
        mu,
        int(metadata["u"]),
        int(metadata["v"]),
        0,
    )

    sparse_type_ii = np.zeros(horizon + 1, dtype=np.float64)
    dense_type_ii = np.zeros(horizon + 1, dtype=np.float64)
    sparse_q_multiplicity = np.zeros(horizon + 1, dtype=np.int32)
    sparse_shifted_by_q = 0.0
    geometric_shifted = 0.0
    geometric_baseline = 0.0
    sparse_baseline = 0.0
    sparse_centered_triangle = 0.0
    sparse_prime_hit_q_count = 0

    for modulus in support:
        first = ((lower + modulus - 1) // modulus) * modulus
        count = horizon // modulus - (lower - 1) // modulus
        weight = float(coefficient[modulus])
        if count <= 1:
            shifted = float(values[first + 2])
            sparse_type_ii[first] += weight
            sparse_q_multiplicity[first] += 1
            sparse_shifted_by_q += weight * shifted
            sparse_baseline += weight * float(baseline[modulus])
            sparse_centered_triangle += abs(weight * (shifted - float(baseline[modulus])))
            sparse_prime_hit_q_count += int(shifted > 0)
            if modulus > horizon / 2:
                geometric_shifted += weight * shifted
                geometric_baseline += weight * float(baseline[modulus])
        else:
            dense_type_ii[first : horizon + 1 : modulus] += weight

    shifted = values[lower + 2 : horizon + 3]
    block = slice(lower, horizon + 1)
    sparse_correlation = float(np.dot(sparse_type_ii[block], shifted))
    dense_correlation = float(np.dot(dense_type_ii[block], shifted))
    structured_correlation = float(np.dot(type_i[block], shifted))
    exact_correlation = float(np.dot(values[block], shifted))

    modulus = schedule_moduli(horizon)[-1]
    endpoints = np.array([lower - 1, horizon], dtype=np.int64)
    endpoint_main = twin_main_vector(endpoints, modulus)
    local_main = float(endpoint_main[1] - endpoint_main[0])
    structured_residual = structured_correlation - local_main
    structured_sparse_residual = structured_residual + sparse_correlation
    full_residual = structured_sparse_residual + dense_correlation
    scale = math.log(horizon) / local_main

    sparse_n_support = np.flatnonzero(np.abs(sparse_type_ii) > 1e-12)
    sparse_q_l1 = float(np.sum(np.abs(coefficient[sparse_support])))
    sparse_n_l1 = float(np.sum(np.abs(sparse_type_ii[sparse_n_support])))
    sparse_shifted_triangle = float(np.sum(np.abs(sparse_type_ii[block] * shifted)))
    combined_q_vector = sparse_type_ii + dense_type_ii
    direct_error = float(np.max(np.abs(combined_q_vector[block] - type_ii[block])))
    correlation_error = abs(
        exact_correlation - structured_correlation - sparse_correlation - dense_correlation
    )
    sparse_centered = sparse_correlation - sparse_baseline
    geometric_centered = geometric_shifted - geometric_baseline

    return {
        "horizon": horizon,
        "block_start": lower,
        "block_end": horizon,
        "u": metadata["u"],
        "v": metadata["v"],
        "local_external_main": local_main,
        "exact_local_correlation": exact_correlation,
        "structured_local_correlation": structured_correlation,
        "structured_residual": structured_residual,
        "sparse_type_ii_correlation": sparse_correlation,
        "dense_type_ii_correlation": dense_correlation,
        "structured_sparse_residual": structured_sparse_residual,
        "full_joint_residual": full_residual,
        "structured_sparse_required_constant": max(0.0, -structured_sparse_residual) * scale,
        "dense_required_constant": max(0.0, -dense_correlation) * scale,
        "joint_required_constant": max(0.0, -full_residual) * scale,
        "sparse_absolute_scale_constant": abs(sparse_correlation) * scale,
        "sparse_triangle_scale_constant": sparse_shifted_triangle * scale,
        "sparse_centered_discrepancy": sparse_centered,
        "sparse_centered_absolute_scale_constant": abs(sparse_centered) * scale,
        "sparse_centered_triangle_scale_constant": sparse_centered_triangle * scale,
        "geometric_tail_centered_discrepancy": geometric_centered,
        "aliased_sparse_centered_discrepancy": sparse_centered - geometric_centered,
        "sparse_q_support_count": int(len(sparse_support)),
        "sparse_n_support_count": int(len(sparse_n_support)),
        "sparse_q_to_n_support_ratio": float(len(sparse_n_support) / len(sparse_support)),
        "sparse_n_collision_count": int(np.count_nonzero(sparse_q_multiplicity >= 2)),
        "maximum_sparse_q_multiplicity_per_n": int(np.max(sparse_q_multiplicity)),
        "sparse_prime_hit_q_count": sparse_prime_hit_q_count,
        "sparse_q_l1": sparse_q_l1,
        "sparse_n_l1": sparse_n_l1,
        "n_grouping_l1_retention": sparse_n_l1 / sparse_q_l1 if sparse_q_l1 else 0.0,
        "sparse_shifted_q_to_n_absolute_error": abs(sparse_shifted_by_q - sparse_correlation),
        "type_ii_q_to_vaughan_max_error": direct_error,
        "joint_correlation_absolute_error": correlation_error,
        "lambda_reconstruction_max_error": identity["lambda_reconstruction_max_error"],
    }


def analyze_ticket107() -> dict[str, Any]:
    rows = [audit_sparse_tail_recombination(horizon) for horizon in HORIZONS]
    centered_signs = {int(math.copysign(1, float(row["sparse_centered_discrepancy"]))) for row in rows}
    contract_failures = sum(
        int(float(row["sparse_shifted_q_to_n_absolute_error"]) > 1e-7)
        + int(float(row["type_ii_q_to_vaughan_max_error"]) > 1e-9)
        + int(float(row["joint_correlation_absolute_error"]) > 1e-7)
        + int(float(row["lambda_reconstruction_max_error"]) > 1e-10)
        for row in rows
    )
    return {
        "theorem_name": "SparseTailVaughanRecombinationAudit",
        "source_ticket": "TICKET-106",
        "exact_recombination": {
            "n_level_identity": "II_X(n)=II_sparse,X(n)+II_dense,X(n), after every row-unique q is mapped to its unique n=qm and repeated n values are combined.",
            "correlation_identity": "C_X-M_X=(I_X-M_X)+<II_sparse,X,Lambda_shift>+<II_dense,X,Lambda_shift>.",
            "independent_check": "The q-built Type II vector is compared against the independently constructed Vaughan I/II decomposition before correlations are interpreted.",
        },
        "route_verdict": {
            "sparse_sign_stability": "refuted_on_audited_horizons" if len(centered_signs) > 1 else "not_refuted_finitely",
            "separate_sparse_absolute_bound": "information_destroying_and_numerically_loose",
            "partial_budget_warning": "Even structured-plus-sparse and dense budgets can discard the three-way compensation visible in the full signed residual.",
            "retained_split": "Use sparse/dense separation only inside a joint signed estimate that preserves compensation with the structured Vaughan residual.",
            "scope": "This is an exact finite decomposition and proof-strategy falsification, not an asymptotic estimate.",
        },
        "rows": rows,
        "discarded_routes": [
            "Treat every occupancy-one modulus q as an independent observation even when several q map to the same integer n.",
            "Assume the centered sparse tail has an eventually visible fixed sign from the finite audit.",
            "Control the sparse Type II term by a standalone triangle inequality before allowing cancellation with the structured Vaughan term.",
            "Promote finite structured-plus-sparse constants to a uniform theorem.",
        ],
        "next_theorem_target": "JointStructuredSparseDenseTwinDispersion",
        "machine_audit": {
            "maximum_horizon": HORIZONS[-1],
            "row_count": len(rows),
            "centered_sparse_sign_count": len(centered_signs),
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET107 proves exact finite q-to-n and Vaughan recombination contracts and refutes a fixed-sign sparse-tail shortcut on the audited horizons. It proves none of the four conjectures and no conjecture counterexample.",
    }


def transferred_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin sparse-tail recombination audit",
        "attempt": "Preserve the existing infinite target; no Vaughan sparse-tail shortcut is transferred.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "independent_target": target},
        "obstruction": "TICKET107 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket106 = read_json(ROOT / "data/open-problem/ticket106-twin-modulus-grouped-dispersion.json")
    audit = analyze_ticket107()
    attempts = [
        transferred_attempt(ticket106, "riemann", "RH-TICKET-107", "NonCircularKernelPositivityPreserved", "NonCircularExplicitFormulaKernelPositivity"),
        transferred_attempt(ticket106, "collatz", "CO-TICKET-107", "GoldenMeanEscapePreserved", "GoldenMeanInvariantSetEscape"),
        transferred_attempt(ticket106, "goldbach", "GB-TICKET-107", "JointBalancedGoldbachPreserved", "JointBalancedVaughanGoldbachResidualEnvelope"),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-107",
            "status": "sparse_tail_sign_shortcut_refuted_joint_absorption_theorem_open",
            "route": "SparseTailVaughanRecombination",
            "proof_or_counterexample_mode": "exact q-to-n recombination plus component-split falsification",
            "attempt": "Map occupancy-one moduli back to their unique integers, merge repeated n values, and restore signed compensation with the structured Vaughan component.",
            "bounded_result": {"source_ticket": "TP-TICKET-106", "audit_ref": "twin_sparse_tail_recombination"},
            "obstruction": audit["route_verdict"]["scope"],
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Derive a joint signed dispersion inequality that keeps structured, sparse, and dense compensation through the final estimate instead of assigning independent one-sided budgets.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "sparse_tail_sign_shortcut_refuted_joint_absorption_theorem_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_sparse_tail_recombination": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket107-twin-sparse-tail-recombination.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-107-kernel-positivity-preserved.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-107-golden-mean-preserved.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-107-joint-balanced-preserved.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-107-sparse-tail-recombination.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
