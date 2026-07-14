from __future__ import annotations

import bisect
import gc
import math
from collections import defaultdict
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import mobius_values
from ticket100_extended_residual_vaughan_audit import lambda_values, vaughan_components
from ticket102_twin_dyadic_vaughan_holdout import cutoff_schedule
from ticket108_twin_joint_equivalence_smoothing import dyadic_bump
from ticket109_twin_spectral_phase_audit import next_power_of_two
from ticket110_twin_rational_arc_budget import rational_major_mask
from ticket111_twin_typeii_minor_phase_audit import (
    CALIBRATION_HORIZONS as PRIOR_CALIBRATION_HORIZONS,
    DENOMINATOR_CUTOFF,
    HOLDOUT_HORIZON as PRIOR_HOLDOUT_HORIZON,
)
from ticket112_twin_farey_endpoint_abel_audit import connected_components


GENERATED_AT = "2026-07-14T13:20:00+09:00"
SCHEMA = "primeproject.ticket113-twin-farey-denominator-endpoint-audit.v1"
CALIBRATION_HORIZONS = (*PRIOR_CALIBRATION_HORIZONS, PRIOR_HOLDOUT_HORIZON)
HOLDOUT_HORIZON = 4_194_304
HELFGOTT_SOURCE = "https://arxiv.org/abs/1205.5252"
GRIMMELT_TERAVAINEN_SOURCE = "https://arxiv.org/abs/2207.08805"


def reduced_farey_centers(cutoff: int) -> list[tuple[float, int, int]]:
    fractions: list[tuple[float, int, int]] = []
    for denominator in range(1, cutoff + 1):
        for numerator in range(denominator // 2 + 1):
            if math.gcd(numerator, denominator) == 1:
                fractions.append((numerator / denominator, numerator, denominator))
    return sorted(fractions)


def right_boundary_labels(
    cells: list[np.ndarray],
    frequencies: np.ndarray,
    cutoff: int,
) -> tuple[list[dict[str, int]], int]:
    fractions = reduced_farey_centers(cutoff)
    centers = [fraction[0] for fraction in fractions]
    labels: list[dict[str, int]] = []
    adjacency_failures = 0
    for cell in cells:
        endpoint_frequency = float(frequencies[cell[-1]])
        right_index = bisect.bisect_right(centers, endpoint_frequency)
        if right_index == 0 or right_index >= len(fractions):
            raise ValueError("minor-cell endpoint has no two-sided Farey boundary")
        _, left_numerator, left_denominator = fractions[right_index - 1]
        _, right_numerator, right_denominator = fractions[right_index]
        determinant = (
            right_numerator * left_denominator
            - left_numerator * right_denominator
        )
        adjacency_failures += int(determinant != 1)
        labels.append(
            {
                "left_numerator": left_numerator,
                "left_denominator": left_denominator,
                "right_numerator": right_numerator,
                "right_denominator": right_denominator,
                "farey_determinant": determinant,
            }
        )
    return labels, adjacency_failures


def _rfft(values: np.ndarray, nfft: int) -> np.ndarray:
    padded = np.zeros(nfft, dtype=np.float64)
    padded[: len(values)] = values
    return np.fft.rfft(padded)


def audit_farey_denominator_endpoints(
    horizon: int,
    split: str = "calibration_replay",
) -> dict[str, Any]:
    values, mangoldt = lambda_values(horizon + 2)
    mu = mobius_values(horizon + 2)
    u, v = cutoff_schedule(horizon)
    type_i, type_ii, identity = vaughan_components(values, mangoldt, mu, u, v, 0)

    positions = np.arange(horizon + 3, dtype=np.int64)
    root_bump = np.sqrt(dyadic_bump(positions, horizon))
    target = root_bump * values
    structured = root_bump * type_i
    bilinear = root_bump * type_ii
    nfft = next_power_of_two(2 * len(target))
    target_transform = _rfft(target, nfft)
    structured_transform = _rfft(structured, nfft)
    bilinear_transform = _rfft(bilinear, nfft)

    frequencies = np.arange(len(target_transform), dtype=np.float64) / nfft
    multiplicity = np.full(len(target_transform), 2.0, dtype=np.float64)
    multiplicity[0] = 1.0
    multiplicity[-1] = 1.0
    shift_phase = np.exp(4j * math.pi * frequencies)
    type_ii_cross = multiplicity * np.conj(bilinear_transform) * target_transform / nfft
    major_mask, arc_count = rational_major_mask(
        frequencies,
        horizon,
        DENOMINATOR_CUTOFF,
    )
    minor_mask = ~major_mask
    cells = connected_components(minor_mask)
    labels, adjacency_failures = right_boundary_labels(
        cells,
        frequencies,
        DENOMINATOR_CUTOFF,
    )

    endpoint_complex = 0j
    variation_complex = 0j
    endpoint_absolute_envelope = 0.0
    variation_absolute_envelope = 0.0
    denominator_sums: defaultdict[int, complex] = defaultdict(complex)
    denominator_counts: defaultdict[int, int] = defaultdict(int)
    for cell, label in zip(cells, labels, strict=True):
        prefixes = np.cumsum(type_ii_cross[cell])
        endpoint = prefixes[-1] * shift_phase[cell[-1]]
        endpoint_complex += endpoint
        endpoint_absolute_envelope += abs(endpoint)
        right_denominator = label["right_denominator"]
        denominator_sums[right_denominator] += endpoint
        denominator_counts[right_denominator] += 1
        if len(cell) > 1:
            phase_differences = shift_phase[cell[:-1]] - shift_phase[cell[1:]]
            variation_complex += np.sum(prefixes[:-1] * phase_differences)
            variation_absolute_envelope += float(
                np.sum(np.abs(prefixes[:-1]) * np.abs(phase_differences))
            )

    grouped_endpoint_complex = sum(denominator_sums.values(), 0j)
    denominator_group_envelope = float(
        sum(abs(value) for value in denominator_sums.values())
    )
    endpoint_absolute_envelope = float(endpoint_absolute_envelope)
    variation_absolute_envelope = float(variation_absolute_envelope)
    exact_type_ii_minor_complex = np.sum(
        type_ii_cross[minor_mask] * shift_phase[minor_mask]
    )
    abel_identity_error = abs(
        exact_type_ii_minor_complex - endpoint_complex - variation_complex
    )
    denominator_group_identity_error = abs(
        endpoint_complex - grouped_endpoint_complex
    )

    target_power = multiplicity * np.abs(target_transform) ** 2 / nfft
    major_total = float(
        np.sum(target_power[major_mask] * np.real(shift_phase[major_mask]))
    )
    structured_minor = float(
        np.sum(
            multiplicity[minor_mask]
            * np.real(
                np.conj(structured_transform[minor_mask])
                * target_transform[minor_mask]
                * shift_phase[minor_mask]
            )
            / nfft
        )
    )
    known_without_type_ii_minor = major_total + structured_minor
    grouped_total_envelope = denominator_group_envelope + variation_absolute_envelope
    grouped_lower_bound = known_without_type_ii_minor - grouped_total_envelope
    independent_endpoint_lower_bound = (
        known_without_type_ii_minor
        - endpoint_absolute_envelope
        - variation_absolute_envelope
    )
    denominator_profile = [
        {
            "right_denominator": denominator,
            "cell_count": denominator_counts[denominator],
            "signed_real": float(np.real(denominator_sums[denominator])),
            "signed_imaginary": float(np.imag(denominator_sums[denominator])),
            "magnitude": float(abs(denominator_sums[denominator])),
        }
        for denominator in sorted(denominator_sums)
    ]

    row = {
        "horizon": horizon,
        "split": split,
        "u": u,
        "v": v,
        "fft_length": nfft,
        "denominator_cutoff": DENOMINATOR_CUTOFF,
        "major_arc_count": arc_count,
        "minor_cell_count": len(cells),
        "right_denominator_group_count": len(denominator_sums),
        "farey_adjacency_failure_count": adjacency_failures,
        "lambda_reconstruction_max_error": identity["lambda_reconstruction_max_error"],
        "abel_identity_absolute_error": float(abel_identity_error),
        "denominator_group_identity_absolute_error": float(
            denominator_group_identity_error
        ),
        "actual_type_ii_minor_contribution": float(
            np.real(exact_type_ii_minor_complex)
        ),
        "endpoint_signed_contribution": float(np.real(endpoint_complex)),
        "endpoint_absolute_envelope": endpoint_absolute_envelope,
        "variation_signed_contribution": float(np.real(variation_complex)),
        "variation_absolute_envelope": variation_absolute_envelope,
        "right_denominator_group_envelope": denominator_group_envelope,
        "grouped_total_envelope": grouped_total_envelope,
        "grouped_endpoint_fraction_of_independent": (
            denominator_group_envelope / endpoint_absolute_envelope
            if endpoint_absolute_envelope
            else 0.0
        ),
        "known_without_type_ii_minor": known_without_type_ii_minor,
        "grouped_lower_bound": grouped_lower_bound,
        "grouped_triangle_closes_finite": bool(grouped_lower_bound > 0),
        "independent_endpoint_lower_bound": independent_endpoint_lower_bound,
        "magnitude_label_adversary_refutes_closure": bool(
            independent_endpoint_lower_bound <= 0
        ),
        "denominator_profile": denominator_profile,
    }

    del target_transform, structured_transform, bilinear_transform
    del type_ii_cross, target_power, shift_phase, frequencies
    gc.collect()
    return row


def analyze_ticket113() -> dict[str, Any]:
    rows = [
        audit_farey_denominator_endpoints(horizon, "calibration_replay")
        for horizon in CALIBRATION_HORIZONS
    ]
    rows.append(
        audit_farey_denominator_endpoints(HOLDOUT_HORIZON, "post_selection_holdout")
    )
    holdout = rows[-1]
    contract_failures = sum(
        int(float(row["abel_identity_absolute_error"]) > 1e-5)
        + int(float(row["denominator_group_identity_absolute_error"]) > 1e-5)
        + int(float(row["lambda_reconstruction_max_error"]) > 1e-10)
        + int(int(row["minor_cell_count"]) != 162)
        + int(int(row["right_denominator_group_count"]) != 31)
        + int(int(row["farey_adjacency_failure_count"]) != 0)
        for row in rows
    )
    finite_closure_count = sum(
        int(row["grouped_triangle_closes_finite"]) for row in rows
    )
    adversary_refutation_count = sum(
        int(row["magnitude_label_adversary_refutes_closure"]) for row in rows
    )
    return {
        "theorem_name": "ExactRightFareyDenominatorEndpointGroupingAndMagnitudeLabelNoGo",
        "source_ticket": "TICKET-112",
        "selection_contract": {
            "exploratory_scale": 262_144,
            "frozen_rule": "Attach every minor-cell endpoint to the denominator q of its immediate right Farey boundary; then sum endpoints sharing q.",
            "rule_reason": "The Abel endpoint lies immediately before that major arc, so the right boundary is canonical and does not depend on the endpoint sign.",
            "endpoint_statistic_holdout": HOLDOUT_HORIZON,
            "holdout_scope": "The 4M scale appeared in earlier project tracks, but its 31-block right-denominator endpoint statistic was not inspected when this rule was frozen.",
            "anti_tuning": "No denominator subset, sign, weight, or exponent is fitted. All q=2,...,32 are retained.",
        },
        "exact_denominator_grouping": {
            "farey_contract": "All 162 minor cells lie between adjacent reduced fractions a/q with q<=32 and determinant one.",
            "identity": "If E_C is the Abel endpoint for cell C and q_R(C) its right-boundary denominator, D_q=sum_{q_R(C)=q} E_C and sum_C E_C=sum_{q=2}^{32} D_q exactly.",
            "finite_bound": "Re(sum_q D_q)>=-sum_q |D_q|; adding the unchanged within-cell variation envelope yields a replayable finite lower bound.",
            "information_gain": "This retains cancellation among endpoint phases that share a canonical denominator instead of taking 162 independent absolute values.",
        },
        "magnitude_label_no_go": {
            "countermodel": "Replace each endpoint E_C by -|E_C| while preserving its cell, right-denominator label, per-cell magnitude, group counts, and all magnitude-only norms.",
            "result": "The adversary restores the independent endpoint envelope and leaves a nonpositive lower bound on every audited scale.",
            "logical_scope": "Therefore Farey labels plus endpoint magnitudes cannot imply denominator cancellation. A proof must use phase relations forced by the Vaughan bilinear coefficients; the countermodel is not claimed to be Vaughan-realizable.",
        },
        "holdout_result": {
            "status": "finite_grouped_triangle_survives_new_holdout"
            if holdout["grouped_triangle_closes_finite"]
            else "grouped_triangle_refuted_on_new_holdout",
            "right_denominator_groups": holdout["right_denominator_group_count"],
            "endpoint_envelope": holdout["endpoint_absolute_envelope"],
            "grouped_endpoint_envelope": holdout["right_denominator_group_envelope"],
            "variation_envelope": holdout["variation_absolute_envelope"],
            "grouped_lower_bound": holdout["grouped_lower_bound"],
            "proof_gap": "A finite FFT audit, even at the first post-selection evaluation of this statistic, supplies no uniform estimate in X and no exact interval certificate for floating-point rounding.",
        },
        "rows": rows,
        "discarded_routes": [
            "Use unordered pairs of adjacent Farey denominators: at 262K all 162 pairs are distinct, so the envelope does not shrink.",
            "Use reflection-orbit grouping: the exploratory envelope remains 98.84% of the independent endpoint envelope.",
            "Select the numerically smaller left-boundary-denominator envelope (25.85% at 262K): the Abel endpoint is oriented toward the right boundary, so selecting left after comparison would add a tuning degree of freedom.",
            "Infer a theorem from the right-denominator holdout without a uniform Vaughan-coefficient estimate.",
            "Claim denominator labels alone force phase cancellation; the magnitude-label adversary refutes that implication.",
            "Treat floating-point FFT positivity as a formally certified finite theorem.",
        ],
        "literature_boundary": {
            "helfgott_minor_arcs": HELFGOTT_SOURCE,
            "grimmelt_teravainen": GRIMMELT_TERAVAINEN_SOURCE,
            "established_background": "Vaughan Type I/II decompositions, rational-arc geometry, large-sieve estimates, and circle-method power savings are established.",
            "project_specific_result": "The canonical right-boundary-denominator endpoint identity, its new 4M holdout audit, and the magnitude-label countermodel for this fixed shift-two cross-spectrum.",
            "non_transfer": "The cited results do not state the uniform one-sided D_q budget required here for the binary exact-gap-two correlation.",
        },
        "next_theorem_target": "UniformRightFareyDenominatorEndpointBudgetForVaughanCrossSpectrum",
        "machine_audit": {
            "maximum_horizon": HOLDOUT_HORIZON,
            "row_count": len(rows),
            "calibration_row_count": len(CALIBRATION_HORIZONS),
            "holdout_row_count": 1,
            "minor_cell_count": int(holdout["minor_cell_count"]),
            "right_denominator_group_count": int(
                holdout["right_denominator_group_count"]
            ),
            "finite_closure_count": finite_closure_count,
            "magnitude_label_adversary_refutation_count": adversary_refutation_count,
            "holdout_closure_failure_count": int(
                not holdout["grouped_triangle_closes_finite"]
            ),
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET113 proves exact finite decomposition identities in the implemented algebra and constructs an abstract no-go countermodel for magnitude-and-label-only reasoning. The positive grouped bounds are floating-point finite audits, not a uniform theorem. It proves none of the four conjectures and certifies no conjecture counterexample.",
    }


def transferred_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    target: str,
) -> dict[str, Any]:
    prior = next(
        attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id
    )
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin Farey denominator audit",
        "attempt": "Preserve the existing infinite target; no Twin denominator-grouping shortcut is transferred.",
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "independent_target": target,
        },
        "obstruction": "TICKET113 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket112 = read_json(
        ROOT / "data/open-problem/ticket112-twin-farey-endpoint-abel-audit.json"
    )
    audit = analyze_ticket113()
    attempts = [
        transferred_attempt(
            ticket112,
            "riemann",
            "RH-TICKET-113",
            "NonCircularKernelPositivityPreserved",
            "NonCircularExplicitFormulaKernelPositivity",
        ),
        transferred_attempt(
            ticket112,
            "collatz",
            "CO-TICKET-113",
            "GoldenMeanEscapePreserved",
            "GoldenMeanInvariantSetEscape",
        ),
        transferred_attempt(
            ticket112,
            "goldbach",
            "GB-TICKET-113",
            "JointBalancedGoldbachPreserved",
            "JointBalancedVaughanGoldbachResidualEnvelope",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-113",
            "status": "right_denominator_grouping_exact_new_holdout_finite_closure_open",
            "route": "RightFareyDenominatorEndpointBudget",
            "proof_or_counterexample_mode": "exact denominator grouping, new holdout, and magnitude-label adversary",
            "attempt": "Group the 162 exact Farey-cell endpoints by their canonical right-boundary denominator, test the frozen rule at 4M, and falsify any inference based only on labels and magnitudes.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-112",
                "audit_ref": "twin_farey_denominator_endpoint_audit",
            },
            "obstruction": audit["holdout_result"]["proof_gap"],
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Derive a uniform one-sided bound for the 31 denominator blocks from the Vaughan bilinear coefficient phases, or construct a Vaughan-realizable adversarial sequence.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "right_denominator_grouping_exact_new_holdout_finite_closure_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_farey_denominator_endpoint_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket113-twin-farey-denominator-endpoint-audit.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-113-kernel-positivity-preserved.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-113-golden-mean-preserved.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-113-joint-balanced-preserved.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-113-farey-denominator-endpoint-audit.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
