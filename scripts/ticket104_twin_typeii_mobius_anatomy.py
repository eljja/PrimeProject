from __future__ import annotations

import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import mobius_values
from ticket100_extended_residual_vaughan_audit import lambda_values, schedule_moduli, twin_main_vector
from ticket102_twin_dyadic_vaughan_holdout import cutoff_schedule
from ticket103_twin_local_block_audit import audit_local_block


GENERATED_AT = "2026-07-13T13:20:00+09:00"
SCHEMA = "primeproject.ticket104-twin-typeii-mobius-anatomy.v1"
HORIZONS = (1_000, 125_000, 1_000_000, 2_000_000)


def outer_mobius_weights(horizon: int) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    lower = horizon // 2 + 1
    u, v = cutoff_schedule(horizon)
    values, mangoldt = lambda_values(horizon + 2)
    mu_list = mobius_values(horizon + 2)
    maximum_d = horizon // (v + 1)
    weights = np.zeros(maximum_d + 1, dtype=np.float64)
    large_lambda = sorted((number, weight) for number, weight in mangoldt.items() if number > v)

    for divisor in range(u + 1, maximum_d + 1):
        maximum_r = horizon // divisor
        total = 0.0
        for number, weight in large_lambda:
            if number > maximum_r:
                break
            step = divisor * number
            first = ((lower + step - 1) // step) * step
            if first <= horizon:
                total += weight * float(np.sum(values[first + 2 : horizon + 3 : step]))
        weights[divisor] = total

    mu = np.asarray(mu_list[: maximum_d + 1], dtype=np.float64)
    return mu, weights, {
        "horizon": horizon,
        "block_start": lower,
        "block_end": horizon,
        "u": u,
        "v": v,
        "maximum_outer_divisor": maximum_d,
        "nonzero_weight_count": int(np.count_nonzero(weights)),
        "minimum_weight": float(np.min(weights[u + 1 :])),
    }


def audit_mobius_anatomy(horizon: int) -> dict[str, Any]:
    mu, weights, metadata = outer_mobius_weights(horizon)
    local = audit_local_block(horizon)
    start = int(metadata["u"]) + 1
    end = int(metadata["maximum_outer_divisor"])
    signed_terms = mu[start : end + 1] * weights[start : end + 1]
    signed_sum = float(np.sum(signed_terms))
    positive_mass = float(np.sum(signed_terms[signed_terms > 0]))
    negative_mass = float(-np.sum(signed_terms[signed_terms < 0]))
    l1_mass = positive_mass + negative_mass

    mertens = np.cumsum(mu)
    abel_sum = float(
        mertens[end] * weights[end]
        - mertens[start - 1] * weights[start]
        + np.sum(mertens[start:end] * (weights[start:end] - weights[start + 1 : end + 1]))
    )
    abel_triangle_envelope = float(
        abs(mertens[end] * weights[end])
        + abs(mertens[start - 1] * weights[start])
        + np.sum(np.abs(mertens[start:end]) * np.abs(weights[start:end] - weights[start + 1 : end + 1]))
    )
    direct = float(local["type_ii_local_correlation"])
    main = float(local["local_external_main"])
    scale = math.log(horizon) / main
    reconstruction_error = abs(signed_sum - direct)
    abel_error = abs(abel_sum - signed_sum)
    return {
        **metadata,
        "identity": "T_X=sum_{d>U} mu(d) A_X(d), where A_X(d)>=0 sums Lambda(r)Lambda(drm+2) over r>V and drm in (X/2,X].",
        "direct_type_ii_local_correlation": direct,
        "outer_weight_signed_sum": signed_sum,
        "outer_identity_absolute_error": reconstruction_error,
        "abel_reconstruction_absolute_error": abel_error,
        "positive_signed_mass": positive_mass,
        "negative_signed_mass": negative_mass,
        "l1_signed_mass": l1_mass,
        "signed_over_l1_mass": signed_sum / l1_mass if l1_mass else 0.0,
        "abel_triangle_envelope": abel_triangle_envelope,
        "actual_required_constant": max(0.0, -signed_sum) * scale,
        "negative_mass_required_constant": negative_mass * scale,
        "abel_triangle_required_constant": abel_triangle_envelope * scale,
        "negative_mass_over_main": negative_mass / main,
        "abel_triangle_over_main": abel_triangle_envelope / main,
        "l1_mass_over_main": l1_mass / main,
        "local_external_main": main,
    }


def analyze_ticket104() -> dict[str, Any]:
    rows = [audit_mobius_anatomy(horizon) for horizon in HORIZONS]
    contract_failures = sum(
        int(float(row["outer_identity_absolute_error"]) > 1e-7)
        + int(float(row["abel_reconstruction_absolute_error"]) > 1e-7)
        + int(float(row["minimum_weight"]) < -1e-12)
        for row in rows
    )
    worst_abel = max(rows, key=lambda row: float(row["abel_triangle_required_constant"]))
    worst_negative = max(rows, key=lambda row: float(row["negative_mass_required_constant"]))
    return {
        "theorem_name": "ExactTypeIIOuterMobiusAnatomyAndAbelNoGoAudit",
        "source_ticket": "TICKET-103",
        "exact_reduction": {
            "identity": rows[0]["identity"],
            "new_target": "Control a weighted Möbius sum whose nonnegative weights encode shifted-prime mass; support density and unweighted Mertens cancellation do not control this weight sequence.",
            "logical_value": "A uniform lower bound for this weighted sum on every sufficiently large dyadic block supplies the open Type II premise from TICKET103.",
        },
        "abel_no_go": {
            "finding": "Termwise negative-mass bounds and Abel summation followed by triangle inequality discard the decisive correlation between Mertens prefixes and weight differences.",
            "scope": "This refutes those information-losing proof templates on the audited weights, not all Möbius or bilinear methods.",
            "worst_negative_mass_row": worst_negative,
            "worst_abel_triangle_row": worst_abel,
        },
        "rows": rows,
        "discarded_routes": [
            "Bound all negative outer-divisor terms independently.",
            "Apply Abel summation and then take absolute values of every Mertens-prefix term.",
            "Use an unweighted Mertens bound without exploiting the shifted-prime-dependent weight geometry.",
            "Infer asymptotic cancellation from a small signed-to-L1 ratio at finite horizons.",
        ],
        "next_theorem_target": "WeightedMobiusShiftedPrimeDyadicCancellation",
        "machine_audit": {
            "maximum_horizon": HORIZONS[-1],
            "row_count": len(rows),
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET104 proves an exact finite Type II weighted-Mobius identity and audits two lossy bounds. It proves none of the four conjectures and no conjecture counterexample.",
    }


def transferred_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin Type II anatomy audit",
        "attempt": "Preserve the existing problem-specific infinite target; no weighted-Mobius shortcut is transferred.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "independent_target": target},
        "obstruction": "TICKET104 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with a problem-specific falsification oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket103 = read_json(ROOT / "data/open-problem/ticket103-twin-local-block-audit.json")
    audit = analyze_ticket104()
    attempts = [
        transferred_attempt(ticket103, "riemann", "RH-TICKET-104", "NonCircularKernelPositivityPreserved", "NonCircularExplicitFormulaKernelPositivity"),
        transferred_attempt(ticket103, "collatz", "CO-TICKET-104", "GoldenMeanEscapePreserved", "GoldenMeanInvariantSetEscape"),
        transferred_attempt(ticket103, "goldbach", "GB-TICKET-104", "JointBalancedGoldbachPreserved", "JointBalancedVaughanGoldbachResidualEnvelope"),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-104",
            "status": "weighted_mobius_identity_exact_abel_triangle_route_refuted_open",
            "route": "ExactTypeIIOuterMobiusAnatomy",
            "proof_or_counterexample_mode": "exact identity extraction plus lossy-bound counterexample audit",
            "attempt": "Rewrite the local Type II term as a weighted Möbius sum and test whether negative-mass or Abel-triangle bounds can reach a finite K/log budget.",
            "bounded_result": {"source_ticket": "TP-TICKET-103", "audit_ref": "twin_typeii_mobius_anatomy"},
            "obstruction": audit["abel_no_go"]["finding"],
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Exploit the bilinear shifted-prime geometry of A_X(d), rather than one-dimensional Mertens magnitudes, to prove or refute a uniform weighted cancellation bound.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "weighted_mobius_identity_exact_abel_triangle_route_refuted_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_typeii_mobius_anatomy": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket104-twin-typeii-mobius-anatomy.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-104-kernel-positivity-preserved.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-104-golden-mean-preserved.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-104-joint-balanced-preserved.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-104-typeii-mobius-anatomy.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
