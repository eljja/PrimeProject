from __future__ import annotations

import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import mobius_values
from ticket100_extended_residual_vaughan_audit import lambda_values
from ticket102_twin_dyadic_vaughan_holdout import cutoff_schedule
from ticket104_twin_typeii_mobius_anatomy import HORIZONS
from ticket105_twin_centered_progression_discrepancy import audit_centered_discrepancy, totient_values


GENERATED_AT = "2026-07-13T17:10:00+09:00"
SCHEMA = "primeproject.ticket106-twin-modulus-grouped-dispersion.v1"
BUCKET_EDGES = (0.0, 0.1, 0.25, 0.5, 1.0000001)


def grouped_modulus_vectors(horizon: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, Any]]:
    lower = horizon // 2 + 1
    u, v = cutoff_schedule(horizon)
    values, mangoldt = lambda_values(horizon + 2)
    mu = mobius_values(horizon + 2)
    coefficient = np.zeros(horizon + 1, dtype=np.float64)
    large_lambda = sorted((number, weight) for number, weight in mangoldt.items() if number > v)
    for divisor in range(u + 1, horizon // (v + 1) + 1):
        if mu[divisor] == 0:
            continue
        maximum_r = horizon // divisor
        for number, weight in large_lambda:
            if number > maximum_r:
                break
            coefficient[divisor * number] += mu[divisor] * weight

    phi = totient_values(horizon)
    discrepancy = np.zeros(horizon + 1, dtype=np.float64)
    baseline = np.zeros(horizon + 1, dtype=np.float64)
    support = np.flatnonzero(np.abs(coefficient) > 1e-12)
    for modulus in support:
        first = ((lower + modulus - 1) // modulus) * modulus
        shifted_mass = float(np.sum(values[first + 2 : horizon + 3 : modulus])) if first <= horizon else 0.0
        count = horizon // modulus - (lower - 1) // modulus
        expected = count * modulus / int(phi[modulus]) if modulus % 2 == 1 else 0.0
        baseline[modulus] = expected
        discrepancy[modulus] = shifted_mass - expected
    return coefficient, baseline, discrepancy, {
        "horizon": horizon,
        "block_start": lower,
        "block_end": horizon,
        "u": u,
        "v": v,
        "support_count": len(support),
        "minimum_supported_modulus": int(support[0]) if len(support) else None,
        "maximum_supported_modulus": int(support[-1]) if len(support) else None,
    }


def audit_grouped_dispersion(horizon: int) -> dict[str, Any]:
    coefficient, baseline, discrepancy, metadata = grouped_modulus_vectors(horizon)
    support = np.flatnonzero(np.abs(coefficient) > 1e-12)
    contributions = coefficient[support] * discrepancy[support]
    centered = float(np.sum(contributions))
    baseline_component = float(np.dot(coefficient[support], baseline[support]))
    prior = audit_centered_discrepancy(horizon)
    identity_error = abs(centered - float(prior["centered_progression_discrepancy"]))
    baseline_error = abs(baseline_component - float(prior["progression_baseline_component"]))
    coefficient_norm = float(np.linalg.norm(coefficient[support]))
    discrepancy_norm = float(np.linalg.norm(discrepancy[support]))
    cauchy_envelope = coefficient_norm * discrepancy_norm
    negative_mass = float(-np.sum(contributions[contributions < 0]))
    scale = math.log(horizon) / float(prior["local_external_main"])
    occupancies = horizon // support - (metadata["block_start"] - 1) // support
    occupancy_rows: list[dict[str, Any]] = []
    for maximum_occupancy in (1, 2, 4, 8, 16):
        sparse_mask = occupancies <= maximum_occupancy
        sparse_contribution = float(np.sum(contributions[sparse_mask]))
        occupancy_rows.append(
            {
                "maximum_occupancy": maximum_occupancy,
                "support_count": int(np.count_nonzero(sparse_mask)),
                "support_fraction": float(np.count_nonzero(sparse_mask) / len(support)),
                "signed_contribution": sparse_contribution,
                "complement_signed_contribution": centered - sparse_contribution,
            }
        )
    row_unique = occupancy_rows[0]
    bucket_rows: list[dict[str, Any]] = []
    for left, right in zip(BUCKET_EDGES, BUCKET_EDGES[1:]):
        mask = (support / horizon >= left) & (support / horizon < right)
        bucket_support = support[mask]
        bucket_contributions = coefficient[bucket_support] * discrepancy[bucket_support]
        bucket_rows.append(
            {
                "left_fraction": left,
                "right_fraction": min(right, 1.0),
                "support_count": len(bucket_support),
                "signed_contribution": float(np.sum(bucket_contributions)),
                "negative_mass": float(-np.sum(bucket_contributions[bucket_contributions < 0])),
                "coefficient_l2": float(np.linalg.norm(coefficient[bucket_support])),
                "discrepancy_l2": float(np.linalg.norm(discrepancy[bucket_support])),
            }
        )
    denominator = coefficient_norm * discrepancy_norm
    return {
        **metadata,
        "identity": "Centered Type II = sum_q c_X(q) Delta_X(q), after all q=dr representations are grouped before taking norms.",
        "grouped_centered_discrepancy": centered,
        "grouped_progression_baseline": baseline_component,
        "centered_identity_absolute_error": identity_error,
        "baseline_identity_absolute_error": baseline_error,
        "coefficient_l2": coefficient_norm,
        "discrepancy_l2": discrepancy_norm,
        "grouped_cauchy_required_constant": cauchy_envelope * scale,
        "grouped_negative_mass_required_constant": negative_mass * scale,
        "actual_centered_required_constant": max(0.0, -centered) * scale,
        "coefficient_discrepancy_cosine": centered / denominator if denominator else 0.0,
        "outer_d_cauchy_required_constant": prior["cauchy_centered_required_constant"],
        "outer_d_negative_mass_required_constant": prior["negative_centered_mass_required_constant"],
        "row_unique_support_count": row_unique["support_count"],
        "row_unique_support_fraction": row_unique["support_fraction"],
        "row_unique_signed_contribution": row_unique["signed_contribution"],
        "non_row_unique_signed_contribution": row_unique["complement_signed_contribution"],
        "non_row_unique_required_constant": max(0.0, -row_unique["complement_signed_contribution"]) * scale,
        "occupancy_rows": occupancy_rows,
        "bucket_rows": bucket_rows,
    }


def analyze_ticket106() -> dict[str, Any]:
    rows = [audit_grouped_dispersion(horizon) for horizon in HORIZONS]
    contract_failures = sum(
        int(float(row["centered_identity_absolute_error"]) > 1e-7)
        + int(float(row["baseline_identity_absolute_error"]) > 1e-7)
        for row in rows
    )
    return {
        "theorem_name": "GroupedModulusCenteredDispersionAudit",
        "source_ticket": "TICKET-105",
        "exact_grouping": {
            "identity": rows[0]["identity"],
            "coefficient": "c_X(q)=sum_{d|q,d>U,q/d>V} mu(d)Lambda(q/d).",
            "discrepancy": "Delta_X(q)=sum_{qm in (X/2,X]}(Lambda(qm+2)-q/phi(q)) for odd q, with zero baseline for even q.",
        },
        "dispersion_boundary": {
            "finding": "Grouping repeated factorizations by the actual modulus is mandatory before a large-sieve or dispersion norm is interpreted.",
            "sparse_leakage": "Moduli with at most one block sample can replay individual shifted-prime rows; their positive contribution must not be confused with a dense progression theorem.",
            "remaining_gap": "Split dense-modulus dispersion from a separately justified sparse tail; a finite grouped L2 envelope over row-unique moduli is not a uniform theorem.",
        },
        "rows": rows,
        "discarded_routes": [
            "Apply d-vector Cauchy before combining repeated q=dr representations.",
            "Treat one residue class per large modulus as if classical averaged progression estimates directly supplied the needed range.",
            "Use the positive q>X/2 contribution as evidence for a dense progression estimate; those cells have at most one sample.",
            "Infer a uniform dispersion theorem from finite grouped cosines or bucket signs.",
        ],
        "next_theorem_target": "NonSparseModulusTwinDispersionWithSparseTailControl",
        "machine_audit": {
            "maximum_horizon": HORIZONS[-1],
            "row_count": len(rows),
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET106 proves an exact finite modulus-grouped identity and audits its norm geometry. It proves none of the four conjectures and no conjecture counterexample.",
    }


def transferred_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin grouped-dispersion audit",
        "attempt": "Preserve the existing infinite target; no grouped-modulus shortcut is transferred.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "independent_target": target},
        "obstruction": "TICKET106 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket105 = read_json(ROOT / "data/open-problem/ticket105-twin-centered-progression-discrepancy.json")
    audit = analyze_ticket106()
    attempts = [
        transferred_attempt(ticket105, "riemann", "RH-TICKET-106", "NonCircularKernelPositivityPreserved", "NonCircularExplicitFormulaKernelPositivity"),
        transferred_attempt(ticket105, "collatz", "CO-TICKET-106", "GoldenMeanEscapePreserved", "GoldenMeanInvariantSetEscape"),
        transferred_attempt(ticket105, "goldbach", "GB-TICKET-106", "JointBalancedGoldbachPreserved", "JointBalancedVaughanGoldbachResidualEnvelope"),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-106",
            "status": "modulus_grouping_exact_dispersion_theorem_open",
            "route": "GroupedModulusCenteredTwinDispersion",
            "proof_or_counterexample_mode": "exact q-grouping plus range-bucket dispersion audit",
            "attempt": "Combine every q=dr representation before applying norms to the centered prime-progression discrepancy.",
            "bounded_result": {"source_ticket": "TP-TICKET-105", "audit_ref": "twin_modulus_grouped_dispersion"},
            "obstruction": audit["dispersion_boundary"]["remaining_gap"],
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Prove or refute a large-modulus bilinear dispersion estimate for the grouped coefficient-discrepancy vectors.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "modulus_grouping_exact_dispersion_theorem_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_modulus_grouped_dispersion": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket106-twin-modulus-grouped-dispersion.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-106-kernel-positivity-preserved.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-106-golden-mean-preserved.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-106-joint-balanced-preserved.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-106-modulus-grouped-dispersion.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
