from __future__ import annotations

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
from ticket111_twin_typeii_minor_phase_audit import DENOMINATOR_CUTOFF
from ticket112_twin_farey_endpoint_abel_audit import connected_components
from ticket113_twin_farey_denominator_endpoint_audit import (
    CALIBRATION_HORIZONS,
    HOLDOUT_HORIZON,
    _rfft,
    right_boundary_labels,
)


GENERATED_AT = "2026-07-14T18:10:00+09:00"
SCHEMA = "primeproject.ticket114-twin-ramanujan-numerator-dispersion-audit.v1"
HORIZONS = (*CALIBRATION_HORIZONS, HOLDOUT_HORIZON)
HELFGOTT_SOURCE = "https://arxiv.org/abs/1205.5252"
MAYNARD_SOURCE = "https://arxiv.org/abs/2006.07088"
LICHTMAN_SOURCE = "https://arxiv.org/abs/2309.08522"


def integer_mobius(value: int) -> int:
    if value < 1:
        raise ValueError("Mobius input must be positive")
    remaining = value
    result = 1
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            result = -result
            if remaining % prime == 0:
                return 0
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        result = -result
    return result


def ramanujan_sum(denominator: int, shift: int) -> int:
    if denominator < 1:
        raise ValueError("Ramanujan denominator must be positive")
    common = math.gcd(denominator, shift)
    return sum(
        divisor * integer_mobius(denominator // divisor)
        for divisor in range(1, common + 1)
        if common % divisor == 0
    )


def centered_support_envelope(
    coefficients: np.ndarray,
    rational_phases: np.ndarray,
) -> dict[str, float]:
    real = np.real(coefficients)
    imaginary = np.imag(coefficients)
    cosine = np.real(rational_phases)
    sine = np.imag(rational_phases)
    mean_real = float(np.mean(real))
    mean_cosine = float(np.mean(cosine))
    centered_real = real - mean_real
    coefficient_norm = float(
        np.sqrt(np.sum(centered_real**2 + imaginary**2))
    )
    geometry_norm = float(
        np.sqrt(np.sum((cosine - mean_cosine) ** 2 + sine**2))
    )
    envelope = coefficient_norm * geometry_norm
    signed = float(np.sum(centered_real * cosine - imaginary * sine))
    return {
        "mean_real": mean_real,
        "mean_cosine": mean_cosine,
        "coefficient_l2_norm": coefficient_norm,
        "projected_phase_l2_norm": geometry_norm,
        "centered_signed_contribution": signed,
        "centered_support_envelope": envelope,
        "support_utilization": abs(signed) / envelope if envelope else 0.0,
    }


def audit_ramanujan_numerator_dispersion(
    horizon: int,
    split: str = "historical_replay",
    include_raw_groups: bool = False,
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

    groups: defaultdict[int, list[dict[str, Any]]] = defaultdict(list)
    endpoint_signed = 0.0
    endpoint_complex = 0j
    endpoint_absolute_envelope = 0.0
    variation_signed = 0.0
    variation_complex = 0j
    variation_absolute_envelope = 0.0
    boundary_phase_error_signed = 0.0
    boundary_phase_chord_envelope = 0.0
    boundary_phase_lipschitz_envelope = 0.0
    chord_lipschitz_failures = 0
    denominator_endpoint_sums: defaultdict[int, complex] = defaultdict(complex)
    for cell, label in zip(cells, labels, strict=True):
        prefixes = np.cumsum(type_ii_cross[cell])
        coefficient = prefixes[-1]
        endpoint_frequency = float(frequencies[cell[-1]])
        rational_frequency = (
            label["right_numerator"] / label["right_denominator"]
        )
        rational_phase = np.exp(4j * math.pi * rational_frequency)
        endpoint_phase = shift_phase[cell[-1]]
        endpoint = coefficient * endpoint_phase
        endpoint_complex += endpoint
        endpoint_signed += float(np.real(endpoint))
        endpoint_absolute_envelope += abs(endpoint)
        denominator_endpoint_sums[label["right_denominator"]] += endpoint

        phase_difference = endpoint_phase - rational_phase
        boundary_phase_error_signed += float(
            np.real(coefficient * phase_difference)
        )
        chord_bound = abs(coefficient) * abs(phase_difference)
        lipschitz_bound = (
            abs(coefficient)
            * 4.0
            * math.pi
            * abs(endpoint_frequency - rational_frequency)
        )
        boundary_phase_chord_envelope += chord_bound
        boundary_phase_lipschitz_envelope += lipschitz_bound
        chord_lipschitz_failures += int(chord_bound > lipschitz_bound + 1e-8)
        groups[label["right_denominator"]].append(
            {
                "coefficient": coefficient,
                "rational_phase": rational_phase,
                "right_numerator": label["right_numerator"],
            }
        )
        if len(cell) > 1:
            phase_differences = (
                shift_phase[cell[:-1]] - shift_phase[cell[1:]]
            )
            variation = np.sum(prefixes[:-1] * phase_differences)
            variation_complex += variation
            variation_signed += float(np.real(variation))
            variation_absolute_envelope += float(
                np.sum(np.abs(prefixes[:-1]) * np.abs(phase_differences))
            )

    ramanujan_mean_signed = 0.0
    ramanujan_mean_absolute_envelope = 0.0
    centered_signed = 0.0
    centered_l2_support_envelope = 0.0
    rational_boundary_signed = 0.0
    maximum_ramanujan_contract_error = 0.0
    maximum_rational_boundary_decomposition_error = 0.0
    support_bound_failures = 0
    denominator_profile: list[dict[str, Any]] = []
    for denominator, records in sorted(groups.items()):
        coefficients = np.asarray(
            [record["coefficient"] for record in records],
            dtype=np.complex128,
        )
        rational_phases = np.asarray(
            [record["rational_phase"] for record in records],
            dtype=np.complex128,
        )
        support = centered_support_envelope(coefficients, rational_phases)
        cosine_sum = float(np.sum(np.real(rational_phases)))
        ramanujan = ramanujan_sum(denominator, 2)
        expected_cosine_sum = float(ramanujan if denominator == 2 else ramanujan / 2)
        ramanujan_error = abs(cosine_sum - expected_cosine_sum)
        maximum_ramanujan_contract_error = max(
            maximum_ramanujan_contract_error,
            ramanujan_error,
        )
        mean_signed = support["mean_real"] * cosine_sum
        rational_signed = mean_signed + support["centered_signed_contribution"]
        direct_rational_signed = float(
            np.real(np.sum(coefficients * rational_phases))
        )
        decomposition_error = abs(rational_signed - direct_rational_signed)
        maximum_rational_boundary_decomposition_error = max(
            maximum_rational_boundary_decomposition_error,
            decomposition_error,
        )
        support_bound_failures += int(
            abs(support["centered_signed_contribution"])
            > support["centered_support_envelope"] + 1e-7
        )
        ramanujan_mean_signed += mean_signed
        ramanujan_mean_absolute_envelope += abs(mean_signed)
        centered_signed += support["centered_signed_contribution"]
        centered_l2_support_envelope += support["centered_support_envelope"]
        rational_boundary_signed += direct_rational_signed
        denominator_profile.append(
            {
                "right_denominator": denominator,
                "numerator_count": len(records),
                "ramanujan_sum_shift_two": ramanujan,
                "half_cosine_sum": cosine_sum,
                "ramanujan_contract_error": ramanujan_error,
                "mean_real_coefficient": support["mean_real"],
                "ramanujan_mean_signed_contribution": mean_signed,
                "centered_signed_contribution": support[
                    "centered_signed_contribution"
                ],
                "centered_coefficient_l2_norm": support["coefficient_l2_norm"],
                "projected_phase_l2_norm": support["projected_phase_l2_norm"],
                "centered_support_envelope": support[
                    "centered_support_envelope"
                ],
                "support_utilization": support["support_utilization"],
                "rational_boundary_decomposition_error": decomposition_error,
            }
        )

    exact_type_ii_minor_complex = np.sum(
        type_ii_cross[minor_mask] * shift_phase[minor_mask]
    )
    exact_type_ii_minor_signed = float(np.real(exact_type_ii_minor_complex))
    type_ii_abel_identity_error = abs(
        exact_type_ii_minor_complex - endpoint_complex - variation_complex
    )
    endpoint_ramanujan_identity_error = abs(
        endpoint_signed
        - ramanujan_mean_signed
        - centered_signed
        - boundary_phase_error_signed
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
    denominator_group_envelope = float(
        sum(abs(value) for value in denominator_endpoint_sums.values())
    )
    signed_mean_adverse_budget = (
        centered_l2_support_envelope
        + boundary_phase_lipschitz_envelope
        + variation_absolute_envelope
    )
    signed_mean_l2_lower_bound = (
        known_without_type_ii_minor
        + ramanujan_mean_signed
        - signed_mean_adverse_budget
    )
    sign_free_adverse_budget = (
        ramanujan_mean_absolute_envelope + signed_mean_adverse_budget
    )
    sign_free_l2_lower_bound = known_without_type_ii_minor - sign_free_adverse_budget

    row = {
        "horizon": horizon,
        "split": split,
        "u": u,
        "v": v,
        "fft_length": nfft,
        "denominator_cutoff": DENOMINATOR_CUTOFF,
        "major_arc_count": arc_count,
        "minor_cell_count": len(cells),
        "right_denominator_group_count": len(groups),
        "farey_adjacency_failure_count": adjacency_failures,
        "lambda_reconstruction_max_error": identity["lambda_reconstruction_max_error"],
        "maximum_ramanujan_contract_error": maximum_ramanujan_contract_error,
        "maximum_rational_boundary_decomposition_error": (
            maximum_rational_boundary_decomposition_error
        ),
        "type_ii_abel_identity_absolute_error": float(type_ii_abel_identity_error),
        "endpoint_ramanujan_identity_absolute_error": endpoint_ramanujan_identity_error,
        "chord_lipschitz_failure_count": chord_lipschitz_failures,
        "support_bound_failure_count": support_bound_failures,
        "actual_type_ii_minor_contribution": exact_type_ii_minor_signed,
        "endpoint_signed_contribution": endpoint_signed,
        "endpoint_absolute_envelope": float(endpoint_absolute_envelope),
        "rational_boundary_signed_contribution": rational_boundary_signed,
        "ramanujan_mean_signed_contribution": ramanujan_mean_signed,
        "ramanujan_mean_absolute_envelope": ramanujan_mean_absolute_envelope,
        "centered_numerator_signed_contribution": centered_signed,
        "centered_l2_support_envelope": centered_l2_support_envelope,
        "boundary_phase_error_signed_contribution": boundary_phase_error_signed,
        "boundary_phase_chord_envelope": boundary_phase_chord_envelope,
        "boundary_phase_lipschitz_envelope": boundary_phase_lipschitz_envelope,
        "variation_signed_contribution": variation_signed,
        "variation_absolute_envelope": variation_absolute_envelope,
        "known_without_type_ii_minor": known_without_type_ii_minor,
        "denominator_group_envelope": denominator_group_envelope,
        "signed_mean_adverse_budget": signed_mean_adverse_budget,
        "signed_mean_l2_lower_bound": signed_mean_l2_lower_bound,
        "signed_mean_l2_closes_finite": bool(signed_mean_l2_lower_bound > 0),
        "signed_mean_budget_to_known_ratio": (
            signed_mean_adverse_budget / known_without_type_ii_minor
            if known_without_type_ii_minor
            else float("inf")
        ),
        "sign_free_adverse_budget": sign_free_adverse_budget,
        "sign_free_l2_lower_bound": sign_free_l2_lower_bound,
        "sign_free_l2_closes_finite": bool(sign_free_l2_lower_bound > 0),
        "sign_free_budget_to_known_ratio": (
            sign_free_adverse_budget / known_without_type_ii_minor
            if known_without_type_ii_minor
            else float("inf")
        ),
        "denominator_profile": denominator_profile,
    }
    if include_raw_groups:
        row["_raw_numerator_groups"] = {
            denominator: tuple(
                (
                    complex(record["coefficient"]),
                    complex(record["rational_phase"]),
                    int(record["right_numerator"]),
                )
                for record in records
            )
            for denominator, records in groups.items()
        }

    del target_transform, structured_transform, bilinear_transform
    del type_ii_cross, target_power, shift_phase, frequencies
    gc.collect()
    return row


def analyze_ticket114() -> dict[str, Any]:
    rows = [
        audit_ramanujan_numerator_dispersion(
            horizon,
            "endpoint_statistic_holdout_replay"
            if horizon == HOLDOUT_HORIZON
            else "historical_replay",
        )
        for horizon in HORIZONS
    ]
    frontier = rows[-1]
    contract_failures = sum(
        int(float(row["maximum_ramanujan_contract_error"]) > 1e-9)
        + int(
            float(row["maximum_rational_boundary_decomposition_error"])
            > 1e-7
        )
        + int(float(row["type_ii_abel_identity_absolute_error"]) > 1e-5)
        + int(float(row["endpoint_ramanujan_identity_absolute_error"]) > 1e-5)
        + int(float(row["lambda_reconstruction_max_error"]) > 1e-10)
        + int(int(row["farey_adjacency_failure_count"]) != 0)
        + int(int(row["chord_lipschitz_failure_count"]) != 0)
        + int(int(row["support_bound_failure_count"]) != 0)
        for row in rows
    )
    signed_mean_closure_count = sum(
        int(row["signed_mean_l2_closes_finite"]) for row in rows
    )
    sign_free_closure_count = sum(
        int(row["sign_free_l2_closes_finite"]) for row in rows
    )
    return {
        "theorem_name": "ExactRamanujanMeanCenteredNumeratorDecompositionAndSharpL2SupportBound",
        "source_ticket": "TICKET-113",
        "exact_ramanujan_decomposition": {
            "coefficient": "P_{q,a} is the unphased Abel endpoint coefficient for the cell immediately left of reduced a/q.",
            "boundary_transfer": "Replace the cell endpoint phase by exp(4*pi*i*a/q); the signed transfer error is retained exactly and bounded by 4*pi*|alpha-a/q|*|P_{q,a}|.",
            "mean": "Write Re(P_{q,a})=m_q+x_{q,a} with sum_a x_{q,a}=0. The mean contribution is m_q times the half reduced-residue cosine sum.",
            "ramanujan_identity": "For q>2 the half cosine sum is c_q(2)/2; for q=2 it is c_2(2).",
            "centered_remainder": "The remaining rational-boundary term is sum_a[x_{q,a} cos(4*pi*a/q)-Im(P_{q,a}) sin(4*pi*a/q)].",
        },
        "sharp_centered_support_theorem": {
            "bound": "For each q, |centered remainder| <= ||(x,Im P)||_2 * ||(cos-mean(cos),-sin)||_2.",
            "sharpness": "Under only sum x=0 and the centered L2 norm, equality is attained by choosing (x,Im P) opposite to the projected phase vector.",
            "logical_scope": "This is an exact finite-dimensional support theorem. The extremizer is an abstract coefficient vector and is not claimed to satisfy Vaughan convolution identities.",
            "consequence": "Any improvement must add arithmetic information coupling numerator phases to Vaughan coefficients, or prove a smaller uniform centered norm from that arithmetic structure.",
        },
        "finite_frontier": {
            "maximum_horizon": frontier["horizon"],
            "ramanujan_mean_signed": frontier[
                "ramanujan_mean_signed_contribution"
            ],
            "centered_l2_support_envelope": frontier[
                "centered_l2_support_envelope"
            ],
            "boundary_phase_lipschitz_envelope": frontier[
                "boundary_phase_lipschitz_envelope"
            ],
            "variation_envelope": frontier["variation_absolute_envelope"],
            "signed_mean_lower_bound": frontier["signed_mean_l2_lower_bound"],
            "sign_free_lower_bound": frontier["sign_free_l2_lower_bound"],
            "sign_free_budget_to_known_ratio": frontier[
                "sign_free_budget_to_known_ratio"
            ],
            "interpretation": "These use measured finite coefficient norms. Positivity is not a uniform estimate in X.",
        },
        "retained_asymptotic_criterion": {
            "statement": "Prove that there exist X0 and delta>0 such that, for every X>=X0, the sign-free Ramanujan-mean envelope plus centered projected-L2 envelope, rational-boundary Lipschitz envelope, and Abel variation envelope is at most (1-delta) times the known major-plus-Type-I-minor contribution.",
            "why_sufficient": "The deterministic support inequality would then make the fixed-bump shift-two correlation positive for every sufficiently large X, which feeds the existing exact contamination and infinitude bridge.",
            "finite_evidence": "The sign-free lower expression is positive only on the last three audited scales, from 1M through 4M; this terminal run is evidence for selecting the theorem, not evidence that it is true.",
            "proof_obligation": "Derive the centered coefficient norms and mean envelope uniformly from the Möbius/divisor bilinear structure, with constants strong enough to leave a fixed positive margin.",
        },
        "rows": rows,
        "discarded_routes": [
            "Explain TICKET113 solely by the scalar Ramanujan sum c_q(2); numerator-dependent endpoint coefficients leave a centered remainder.",
            "Take absolute values of the centered numerator coefficients individually; the projected L2 support theorem is strictly stronger and optimal under its contract.",
            "Use the observed finite centered norms as if a weighted large-sieve theorem had already bounded them uniformly.",
            "Call the abstract projected-phase extremizer Vaughan-realizable without satisfying its Möbius/divisor convolution identities.",
            "Treat the 4M replay as globally unseen data; only the TICKET113 endpoint statistic was held out from its selection step.",
        ],
        "literature_boundary": {
            "helfgott_minor_arcs": HELFGOTT_SOURCE,
            "maynard_well_factorable": MAYNARD_SOURCE,
            "lichtman_large_moduli": LICHTMAN_SOURCE,
            "established_background": "Ramanujan sums, Vaughan Type I/II decompositions, rational-arc geometry, and weighted large-sieve estimates are established.",
            "project_specific_result": "The exact half-Farey Ramanujan/centered decomposition and sharp projected L2 support audit for the fixed shift-two endpoint coefficients.",
            "non_transfer": "The cited work does not provide the exact uniform centered-numerator endpoint budget required by this binary shift-two decomposition.",
        },
        "next_theorem_target": "EventuallySubcriticalVaughanCenteredFareyNumeratorDispersionBudget",
        "machine_audit": {
            "maximum_horizon": int(frontier["horizon"]),
            "row_count": len(rows),
            "minor_cell_count": int(frontier["minor_cell_count"]),
            "right_denominator_group_count": int(
                frontier["right_denominator_group_count"]
            ),
            "signed_mean_finite_closure_count": signed_mean_closure_count,
            "sign_free_finite_closure_count": sign_free_closure_count,
            "sign_free_terminal_run_start_horizon": 1_048_576,
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET114 proves exact finite decomposition identities in the implemented algebra and a sharp finite-dimensional L2 support theorem for an explicitly stated weak coefficient contract. Its scale rows use measured floating-point norms and do not prove a uniform Vaughan estimate. It proves none of the four conjectures and certifies no conjecture counterexample.",
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
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin Ramanujan numerator audit",
        "attempt": "Preserve the existing infinite target; no Twin Ramanujan/dispersion shortcut is transferred.",
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "independent_target": target,
        },
        "obstruction": "TICKET114 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket113 = read_json(
        ROOT / "data/open-problem/ticket113-twin-farey-denominator-endpoint-audit.json"
    )
    audit = analyze_ticket114()
    attempts = [
        transferred_attempt(
            ticket113,
            "riemann",
            "RH-TICKET-114",
            "NonCircularKernelPositivityPreserved",
            "NonCircularExplicitFormulaKernelPositivity",
        ),
        transferred_attempt(
            ticket113,
            "collatz",
            "CO-TICKET-114",
            "GoldenMeanEscapePreserved",
            "GoldenMeanInvariantSetEscape",
        ),
        transferred_attempt(
            ticket113,
            "goldbach",
            "GB-TICKET-114",
            "JointBalancedGoldbachPreserved",
            "JointBalancedVaughanGoldbachResidualEnvelope",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-114",
            "status": "ramanujan_centered_decomposition_exact_sharp_l2_support_audited_open",
            "route": "RamanujanMeanAndCenteredFareyNumeratorDispersion",
            "proof_or_counterexample_mode": "exact decomposition, optimal weak-contract adversary, and finite norm audit",
            "attempt": "Decompose every right-denominator endpoint block into a Ramanujan mean, centered numerator dispersion, rational-boundary transfer error, and Abel variation; then compute the sharp L2 support bound.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-113",
                "audit_ref": "twin_ramanujan_numerator_dispersion_audit",
            },
            "obstruction": "The centered norms are measured finite quantities. A proof requires a uniform weighted large-sieve or dispersion estimate derived from the actual Vaughan coefficients.",
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Expand P_{q,a} back into its Möbius/divisor bilinear coefficients and prove a uniform centered-numerator second-moment budget, or construct a Vaughan-realizable extremizer.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "ramanujan_centered_decomposition_exact_sharp_l2_support_audited_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_ramanujan_numerator_dispersion_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket114-twin-ramanujan-numerator-dispersion-audit.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-114-kernel-positivity-preserved.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-114-golden-mean-preserved.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-114-joint-balanced-preserved.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-114-ramanujan-numerator-dispersion-audit.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
