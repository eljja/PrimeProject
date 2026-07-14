from __future__ import annotations

import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket113_twin_farey_denominator_endpoint_audit import (
    CALIBRATION_HORIZONS,
    HOLDOUT_HORIZON,
)
from ticket114_twin_ramanujan_numerator_dispersion_audit import (
    audit_ramanujan_numerator_dispersion,
    ramanujan_sum,
)


GENERATED_AT = "2026-07-14T21:20:00+09:00"
SCHEMA = "primeproject.ticket115-twin-complex-cyclotomic-dispersion-audit.v1"
HORIZONS = (*CALIBRATION_HORIZONS, HOLDOUT_HORIZON)
HELFGOTT_SOURCE = "https://arxiv.org/abs/1205.5252"
MAYNARD_SOURCE = "https://arxiv.org/abs/2006.07088"
LICHTMAN_SOURCE = "https://arxiv.org/abs/2309.08522"


def complex_centered_support_envelope(
    coefficients: np.ndarray,
    rational_phases: np.ndarray,
) -> dict[str, float]:
    coefficient_mean = complex(np.mean(coefficients))
    phase_mean = complex(np.mean(rational_phases))
    centered_coefficients = coefficients - coefficient_mean
    projected_phases = rational_phases - phase_mean
    coefficient_norm = float(np.linalg.norm(centered_coefficients))
    geometry_norm = float(np.linalg.norm(projected_phases))
    envelope = coefficient_norm * geometry_norm
    centered_signed = float(
        np.real(np.sum(centered_coefficients * rational_phases))
    )
    phase_sum = complex(np.sum(rational_phases))
    mean_signed = float(np.real(coefficient_mean * phase_sum))
    mean_scalar_absolute_contribution = abs(mean_signed)
    mean_orientation_free_envelope = abs(coefficient_mean) * abs(phase_sum)
    geometry_identity_error = abs(
        geometry_norm**2
        - (
            len(rational_phases)
            - abs(phase_sum) ** 2 / len(rational_phases)
        )
    )
    return {
        "coefficient_mean_real": float(np.real(coefficient_mean)),
        "coefficient_mean_imaginary": float(np.imag(coefficient_mean)),
        "coefficient_mean_magnitude": abs(coefficient_mean),
        "phase_mean_real": float(np.real(phase_mean)),
        "phase_mean_imaginary": float(np.imag(phase_mean)),
        "half_farey_phase_sum_real": float(np.real(phase_sum)),
        "half_farey_phase_sum_imaginary": float(np.imag(phase_sum)),
        "half_farey_phase_sum_magnitude": abs(phase_sum),
        "complex_centered_coefficient_l2_norm": coefficient_norm,
        "complex_projected_phase_l2_norm": geometry_norm,
        "complex_centered_signed_contribution": centered_signed,
        "complex_centered_support_envelope": envelope,
        "complex_mean_signed_contribution": mean_signed,
        "complex_mean_scalar_absolute_contribution": (
            mean_scalar_absolute_contribution
        ),
        "complex_mean_orientation_free_envelope": (
            mean_orientation_free_envelope
        ),
        "support_utilization": abs(centered_signed) / envelope if envelope else 0.0,
        "geometry_identity_error": geometry_identity_error,
    }


def derive_complex_cyclotomic_row(base_row: dict[str, Any]) -> dict[str, Any]:
    raw_groups = base_row.pop("_raw_numerator_groups")
    old_profiles = {
        int(row["right_denominator"]): row
        for row in base_row.pop("denominator_profile")
    }
    complex_mean_signed = 0.0
    complex_mean_scalar_absolute_envelope = 0.0
    complex_mean_orientation_free_envelope = 0.0
    complex_centered_signed = 0.0
    complex_centered_l2_support_envelope = 0.0
    maximum_half_ramanujan_real_error = 0.0
    maximum_complex_decomposition_error = 0.0
    maximum_geometry_identity_error = 0.0
    complex_support_bound_failures = 0
    denominator_profile: list[dict[str, Any]] = []

    for denominator, records in sorted(raw_groups.items()):
        coefficients = np.asarray(
            [record[0] for record in records],
            dtype=np.complex128,
        )
        rational_phases = np.asarray(
            [record[1] for record in records],
            dtype=np.complex128,
        )
        support = complex_centered_support_envelope(
            coefficients,
            rational_phases,
        )
        ramanujan = ramanujan_sum(denominator, 2)
        expected_real = float(
            ramanujan if denominator == 2 else ramanujan / 2
        )
        real_error = abs(
            support["half_farey_phase_sum_real"] - expected_real
        )
        direct = float(np.real(np.sum(coefficients * rational_phases)))
        reconstructed = (
            support["complex_mean_signed_contribution"]
            + support["complex_centered_signed_contribution"]
        )
        decomposition_error = abs(direct - reconstructed)
        maximum_half_ramanujan_real_error = max(
            maximum_half_ramanujan_real_error,
            real_error,
        )
        maximum_complex_decomposition_error = max(
            maximum_complex_decomposition_error,
            decomposition_error,
        )
        maximum_geometry_identity_error = max(
            maximum_geometry_identity_error,
            support["geometry_identity_error"],
        )
        complex_support_bound_failures += int(
            abs(support["complex_centered_signed_contribution"])
            > support["complex_centered_support_envelope"] + 1e-7
        )
        complex_mean_signed += support["complex_mean_signed_contribution"]
        complex_mean_scalar_absolute_envelope += support[
            "complex_mean_scalar_absolute_contribution"
        ]
        complex_mean_orientation_free_envelope += support[
            "complex_mean_orientation_free_envelope"
        ]
        complex_centered_signed += support[
            "complex_centered_signed_contribution"
        ]
        complex_centered_l2_support_envelope += support[
            "complex_centered_support_envelope"
        ]
        denominator_profile.append(
            {
                "right_denominator": denominator,
                "numerator_count": len(records),
                "ramanujan_sum_shift_two": ramanujan,
                "old_real_centered_denominator_budget": (
                    abs(
                        float(
                            old_profiles[denominator][
                                "ramanujan_mean_signed_contribution"
                            ]
                        )
                    )
                    + float(
                        old_profiles[denominator][
                            "centered_support_envelope"
                        ]
                    )
                ),
                **support,
                "half_ramanujan_real_error": real_error,
                "complex_decomposition_error": decomposition_error,
            }
        )

    old_numerator_budget = (
        float(base_row["ramanujan_mean_absolute_envelope"])
        + float(base_row["centered_l2_support_envelope"])
    )
    complex_scalar_numerator_budget = (
        complex_mean_scalar_absolute_envelope
        + complex_centered_l2_support_envelope
    )
    complex_orientation_free_numerator_budget = (
        complex_mean_orientation_free_envelope
        + complex_centered_l2_support_envelope
    )
    boundary_and_variation = (
        float(base_row["boundary_phase_lipschitz_envelope"])
        + float(base_row["variation_absolute_envelope"])
    )
    complex_signed_mean_adverse_budget = (
        complex_centered_l2_support_envelope + boundary_and_variation
    )
    complex_signed_mean_lower_bound = (
        float(base_row["known_without_type_ii_minor"])
        + complex_mean_signed
        - complex_signed_mean_adverse_budget
    )
    complex_sign_free_adverse_budget = (
        complex_scalar_numerator_budget + boundary_and_variation
    )
    complex_sign_free_lower_bound = (
        float(base_row["known_without_type_ii_minor"])
        - complex_sign_free_adverse_budget
    )
    orientation_free_adverse_budget = (
        complex_orientation_free_numerator_budget + boundary_and_variation
    )
    orientation_free_lower_bound = (
        float(base_row["known_without_type_ii_minor"])
        - orientation_free_adverse_budget
    )
    aggregate_decomposition_error = abs(
        float(base_row["rational_boundary_signed_contribution"])
        - complex_mean_signed
        - complex_centered_signed
    )

    base_row.update(
        {
            "complex_mean_signed_contribution": complex_mean_signed,
            "complex_mean_scalar_absolute_envelope": (
                complex_mean_scalar_absolute_envelope
            ),
            "complex_mean_orientation_free_envelope": (
                complex_mean_orientation_free_envelope
            ),
            "complex_centered_signed_contribution": complex_centered_signed,
            "complex_centered_l2_support_envelope": (
                complex_centered_l2_support_envelope
            ),
            "old_real_centered_numerator_budget": old_numerator_budget,
            "complex_scalar_centered_numerator_budget": (
                complex_scalar_numerator_budget
            ),
            "complex_scalar_centering_budget_reduction": (
                old_numerator_budget - complex_scalar_numerator_budget
            ),
            "complex_scalar_centering_budget_retained_fraction": (
                complex_scalar_numerator_budget / old_numerator_budget
                if old_numerator_budget
                else 0.0
            ),
            "complex_orientation_free_numerator_budget": (
                complex_orientation_free_numerator_budget
            ),
            "complex_orientation_free_budget_increase": (
                complex_orientation_free_numerator_budget - old_numerator_budget
            ),
            "complex_orientation_free_budget_retained_fraction": (
                complex_orientation_free_numerator_budget / old_numerator_budget
                if old_numerator_budget
                else 0.0
            ),
            "complex_signed_mean_adverse_budget": (
                complex_signed_mean_adverse_budget
            ),
            "complex_signed_mean_lower_bound": complex_signed_mean_lower_bound,
            "complex_signed_mean_closes_finite": bool(
                complex_signed_mean_lower_bound > 0
            ),
            "complex_sign_free_adverse_budget": complex_sign_free_adverse_budget,
            "complex_sign_free_lower_bound": complex_sign_free_lower_bound,
            "complex_sign_free_closes_finite": bool(
                complex_sign_free_lower_bound > 0
            ),
            "complex_sign_free_budget_to_known_ratio": (
                complex_sign_free_adverse_budget
                / float(base_row["known_without_type_ii_minor"])
                if base_row["known_without_type_ii_minor"]
                else float("inf")
            ),
            "orientation_free_adverse_budget": orientation_free_adverse_budget,
            "orientation_free_lower_bound": orientation_free_lower_bound,
            "orientation_free_closes_finite": bool(
                orientation_free_lower_bound > 0
            ),
            "orientation_free_budget_to_known_ratio": (
                orientation_free_adverse_budget
                / float(base_row["known_without_type_ii_minor"])
                if base_row["known_without_type_ii_minor"]
                else float("inf")
            ),
            "maximum_half_ramanujan_real_error": (
                maximum_half_ramanujan_real_error
            ),
            "maximum_complex_decomposition_error": (
                maximum_complex_decomposition_error
            ),
            "aggregate_complex_decomposition_error": (
                aggregate_decomposition_error
            ),
            "maximum_complex_geometry_identity_error": (
                maximum_geometry_identity_error
            ),
            "complex_support_bound_failure_count": (
                complex_support_bound_failures
            ),
            "complex_denominator_profile": denominator_profile,
        }
    )
    return base_row


def audit_complex_cyclotomic_dispersion(
    horizon: int,
    split: str = "historical_replay",
) -> dict[str, Any]:
    base_row = audit_ramanujan_numerator_dispersion(
        horizon,
        split,
        include_raw_groups=True,
    )
    return derive_complex_cyclotomic_row(base_row)


def analyze_ticket115() -> dict[str, Any]:
    rows = [
        audit_complex_cyclotomic_dispersion(
            horizon,
            "complex_centering_holdout_replay"
            if horizon == HOLDOUT_HORIZON
            else "historical_replay",
        )
        for horizon in HORIZONS
    ]
    frontier = rows[-1]
    contract_failures = sum(
        int(float(row["maximum_half_ramanujan_real_error"]) > 1e-9)
        + int(float(row["maximum_complex_decomposition_error"]) > 1e-7)
        + int(float(row["aggregate_complex_decomposition_error"]) > 1e-6)
        + int(float(row["maximum_complex_geometry_identity_error"]) > 1e-9)
        + int(int(row["complex_support_bound_failure_count"]) != 0)
        + int(int(row["farey_adjacency_failure_count"]) != 0)
        + int(int(row["chord_lipschitz_failure_count"]) != 0)
        for row in rows
    )
    return {
        "theorem_name": "ExactHalfFareyCyclotomicComplexMeanDecompositionSharpCenteredL2AndOrientationFreeNoGo",
        "source_ticket": "TICKET-114",
        "exact_complex_decomposition": {
            "coefficient_mean": "For every q, write P_{q,a}=M_q+Z_{q,a} with complex M_q=mean_a P_{q,a} and sum_a Z_{q,a}=0 in both real and imaginary coordinates.",
            "half_farey_sum": "Let H_q=sum_a exp(4*pi*i*a/q) over reduced 0<a<=q/2. Its real part is c_q(2)/2 for q>2 and c_2(2) for q=2; its imaginary part is retained as an explicit cyclotomic sum.",
            "identity": "Re sum_a P_{q,a}rho_{q,a}=Re(M_q H_q)+Re sum_a Z_{q,a}(rho_{q,a}-mean rho_q).",
            "geometry": "The projected phase norm satisfies ||rho-mean rho||_2^2=n_q-|H_q|^2/n_q exactly.",
        },
        "sharp_complex_support_theorem": {
            "bound": "For each q, |Re sum_a Z_{q,a}(rho_{q,a}-mean rho_q)| <= ||Z_q||_2 ||rho_q-mean rho_q||_2.",
            "sharpness": "Under only complex zero mean and a fixed L2 norm, equality is attained by Z proportional to the negative complex conjugate of the projected phase vector.",
            "scope": "The extremizer is an abstract complex coefficient vector. It is not claimed to satisfy Vaughan Mobius/divisor convolution identities.",
            "consequence": "Any further improvement must control the actual complex-centered Vaughan coefficient norm or its correlation with the projected cyclotomic phase.",
        },
        "orientation_free_no_go": {
            "weak_contract": "If the complex mean direction is discarded, its contribution costs |M_q||H_q| instead of the coefficient-aware scalar |Re(M_q H_q)|.",
            "finite_result": "The orientation-free complex budget is larger than the TICKET114 real-centered budget on all six audited scales and loses the 1M finite closure.",
            "logical_result": "Complex constant-mode extraction is not by itself a stronger proof contract; a useful theorem must retain or arithmetically control the scalar mean orientation.",
        },
        "finite_frontier": {
            "maximum_horizon": frontier["horizon"],
            "old_real_centered_numerator_budget": frontier[
                "old_real_centered_numerator_budget"
            ],
            "complex_scalar_centered_numerator_budget": frontier[
                "complex_scalar_centered_numerator_budget"
            ],
            "complex_scalar_centering_budget_retained_fraction": frontier[
                "complex_scalar_centering_budget_retained_fraction"
            ],
            "complex_orientation_free_numerator_budget": frontier[
                "complex_orientation_free_numerator_budget"
            ],
            "complex_orientation_free_budget_retained_fraction": frontier[
                "complex_orientation_free_budget_retained_fraction"
            ],
            "complex_sign_free_lower_bound": frontier[
                "complex_sign_free_lower_bound"
            ],
            "complex_sign_free_budget_to_known_ratio": frontier[
                "complex_sign_free_budget_to_known_ratio"
            ],
            "interpretation": "All quantities use measured finite Vaughan endpoint coefficients and do not constitute a uniform estimate in X.",
        },
        "retained_asymptotic_criterion": {
            "statement": "Prove that for some X0 and delta>0, every X>=X0 has the denominatorwise scalar cyclotomic mean envelope sum_q |Re(M_q H_q)| plus complex-centered projected-L2 envelope, boundary transfer, and Abel variation at most (1-delta) times the major-plus-Type-I-minor contribution.",
            "additional_obligation": "The comparison theorem itself must establish a positive major-plus-Type-I-minor lower scale; finite measured positivity cannot be imported as a premise.",
            "proof_route": "Expand M_q and Z_{q,a} into the actual Mobius/divisor Type-II coefficients, retain the scalar orientation Re(M_q H_q), then seek a weighted large-sieve or dispersion estimate after projecting away the full complex constant mode.",
            "counterexample_route": "Construct a Vaughan-realizable coefficient family whose complex-centered projection saturates the adverse phase support or whose mean envelope destroys every fixed margin.",
        },
        "rows": rows,
        "discarded_routes": [
            "Keep the entire imaginary coefficient mean inside the centered budget; it is an avoidable deterministic loss.",
            "Replace the half-Farey phase sum by its real Ramanujan part; its imaginary cyclotomic component contributes to the complex coefficient mean.",
            "Bound the extracted complex mean by |M_q||H_q| and call it an improvement; this orientation-free contract is worse on all six audited scales.",
            "Infer an all-scale theorem from a terminal finite run of positive lower expressions.",
            "Treat the sharp abstract complex extremizer as Vaughan-realizable without enforcing convolution identities.",
        ],
        "literature_boundary": {
            "helfgott_minor_arcs": HELFGOTT_SOURCE,
            "maynard_well_factorable": MAYNARD_SOURCE,
            "lichtman_large_moduli": LICHTMAN_SOURCE,
            "established_background": "Farey rational geometry, Vaughan Type I/II decompositions, Ramanujan sums, and weighted large-sieve or dispersion methods are established.",
            "project_specific_result": "The full complex constant-mode extraction for these half-Farey endpoint coefficients and its finite six-scale audit are project-specific.",
            "non_transfer": "The cited work does not state the exact all-scale complex-centered endpoint budget required here.",
        },
        "next_theorem_target": "EventuallySubcriticalVaughanCyclotomicMeanAndComplexCenteredNumeratorBudget",
        "machine_audit": {
            "maximum_horizon": int(frontier["horizon"]),
            "row_count": len(rows),
            "minor_cell_count": int(frontier["minor_cell_count"]),
            "right_denominator_group_count": int(
                frontier["right_denominator_group_count"]
            ),
            "complex_scalar_centering_reduces_budget_count": sum(
                int(
                    float(row["complex_scalar_centering_budget_reduction"])
                    > 0
                )
                for row in rows
            ),
            "orientation_free_worsens_budget_count": sum(
                int(
                    float(row["complex_orientation_free_budget_increase"])
                    > 0
                )
                for row in rows
            ),
            "complex_signed_mean_finite_closure_count": sum(
                int(row["complex_signed_mean_closes_finite"])
                for row in rows
            ),
            "complex_sign_free_finite_closure_count": sum(
                int(row["complex_sign_free_closes_finite"])
                for row in rows
            ),
            "orientation_free_finite_closure_count": sum(
                int(row["orientation_free_closes_finite"])
                for row in rows
            ),
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET115 proves exact finite complex decompositions and a sharp finite-dimensional support theorem under an explicit weak contract. It uses measured floating-point Vaughan coefficients at six finite scales, proves no uniform analytic estimate, proves none of the four conjectures, and certifies no conjecture counterexample.",
    }


def transferred_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    target: str,
) -> dict[str, Any]:
    prior = next(
        attempt for attempt in source["attempts"]
        if attempt["problem_id"] == problem_id
    )
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin complex-centering audit",
        "attempt": "Preserve the existing infinite target; no Twin complex-centering shortcut is transferred.",
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "independent_target": target,
        },
        "obstruction": "TICKET115 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket114 = read_json(
        ROOT
        / "data/open-problem/ticket114-twin-ramanujan-numerator-dispersion-audit.json"
    )
    audit = analyze_ticket115()
    attempts = [
        transferred_attempt(
            ticket114,
            "riemann",
            "RH-TICKET-115",
            "NonCircularKernelPositivityPreserved",
            "NonCircularExplicitFormulaKernelPositivity",
        ),
        transferred_attempt(
            ticket114,
            "collatz",
            "CO-TICKET-115",
            "GoldenMeanEscapePreserved",
            "GoldenMeanInvariantSetEscape",
        ),
        transferred_attempt(
            ticket114,
            "goldbach",
            "GB-TICKET-115",
            "JointBalancedGoldbachPreserved",
            "JointBalancedVaughanGoldbachResidualEnvelope",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-115",
            "status": "complex_cyclotomic_mean_exact_sharp_centered_l2_audited_open",
            "route": "HalfFareyCyclotomicComplexMeanAndCenteredDispersion",
            "proof_or_counterexample_mode": "exact complex decomposition, optimal weak-contract adversary, and finite norm audit",
            "attempt": "Extract the full complex constant mode from every numerator block, retain the half-Farey cyclotomic phase sum, and apply the sharp complex-centered L2 support theorem.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-114",
                "audit_ref": "twin_complex_cyclotomic_dispersion_audit",
            },
            "obstruction": "The improved complex-centered norms are still measured finite quantities; the required uniform Vaughan dispersion estimate remains open.",
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Expand complex-centered P_{q,a} into Mobius/divisor coefficients and prove a uniform projected second moment, or construct a Vaughan-realizable saturating family.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "complex_cyclotomic_mean_exact_sharp_centered_l2_audited_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_complex_cyclotomic_dispersion_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket115-twin-complex-cyclotomic-dispersion-audit.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-115-kernel-positivity-preserved.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-115-golden-mean-preserved.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-115-joint-balanced-preserved.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-115-complex-cyclotomic-dispersion-audit.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
