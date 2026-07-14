from __future__ import annotations

import gc
import math
from collections import defaultdict
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import mobius_values
from ticket100_extended_residual_vaughan_audit import (
    lambda_values,
    vaughan_components,
)
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
from ticket115_twin_complex_cyclotomic_dispersion_audit import (
    audit_complex_cyclotomic_dispersion,
    complex_centered_support_envelope,
)


GENERATED_AT = "2026-07-14T23:20:00+09:00"
SCHEMA = "primeproject.ticket116-twin-mobius-sign-cyclotomic-audit.v1"
HORIZONS = (*CALIBRATION_HORIZONS, HOLDOUT_HORIZON)
HELFGOTT_SOURCE = "https://arxiv.org/abs/1501.05438"
LICHTMAN_SOURCE = "https://arxiv.org/abs/2009.08969"
FORD_MAYNARD_SOURCE = "https://arxiv.org/abs/2407.14368"


def vaughan_mobius_sign_layers(
    horizon: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, Any]]:
    """Build the positive and negative outer-Mobius Type-II layers exactly."""
    values, mangoldt = lambda_values(horizon + 2)
    mu = mobius_values(horizon + 2)
    u, v = cutoff_schedule(horizon)
    _, signed_type_ii, identity = vaughan_components(
        values,
        mangoldt,
        mu,
        u,
        v,
        0,
    )
    positive = np.zeros_like(values)
    negative = np.zeros_like(values)
    large_lambda = sorted(
        (number, weight)
        for number, weight in mangoldt.items()
        if number > v
    )
    limit = len(values) - 1
    maximum_outer_divisor = limit // (v + 1)
    outer_pair_count = 0
    positive_outer_divisor_count = 0
    negative_outer_divisor_count = 0

    for divisor in range(u + 1, maximum_outer_divisor + 1):
        sign = mu[divisor]
        if sign == 0:
            continue
        target = positive if sign > 0 else negative
        if sign > 0:
            positive_outer_divisor_count += 1
        else:
            negative_outer_divisor_count += 1
        for number, weight in large_lambda:
            step = divisor * number
            if step > limit:
                break
            target[step::step] += weight
            outer_pair_count += 1

    reconstruction_error = float(
        np.max(np.abs(positive - negative - signed_type_ii))
    )
    return values, positive, negative, {
        "horizon": horizon,
        "u": u,
        "v": v,
        "maximum_outer_divisor": maximum_outer_divisor,
        "outer_pair_count": outer_pair_count,
        "positive_outer_divisor_count": positive_outer_divisor_count,
        "negative_outer_divisor_count": negative_outer_divisor_count,
        "positive_layer_nonzero_count": int(np.count_nonzero(positive)),
        "negative_layer_nonzero_count": int(np.count_nonzero(negative)),
        "time_domain_sign_layer_reconstruction_max_error": (
            reconstruction_error
        ),
        "lambda_reconstruction_max_error": identity[
            "lambda_reconstruction_max_error"
        ],
    }


def endpoint_groups_for_layer(
    layer: np.ndarray,
    root_bump: np.ndarray,
    target_transform: np.ndarray,
    nfft: int,
    multiplicity: np.ndarray,
    cells: list[np.ndarray],
    labels: list[dict[str, int]],
) -> dict[int, list[tuple[complex, complex, int]]]:
    layer_transform = _rfft(root_bump * layer, nfft)
    cross_spectrum = (
        multiplicity
        * np.conj(layer_transform)
        * target_transform
        / nfft
    )
    groups: defaultdict[int, list[tuple[complex, complex, int]]] = (
        defaultdict(list)
    )
    for cell, label in zip(cells, labels, strict=True):
        coefficient = complex(np.sum(cross_spectrum[cell]))
        rational_phase = np.exp(
            4j
            * math.pi
            * label["right_numerator"]
            / label["right_denominator"]
        )
        groups[label["right_denominator"]].append(
            (
                coefficient,
                complex(rational_phase),
                label["right_numerator"],
            )
        )
    del layer_transform, cross_spectrum
    gc.collect()
    return dict(groups)


def centered_layer_data(
    records: list[tuple[complex, complex, int]],
) -> tuple[dict[str, float], np.ndarray, np.ndarray]:
    coefficients = np.asarray(
        [record[0] for record in records],
        dtype=np.complex128,
    )
    phases = np.asarray(
        [record[1] for record in records],
        dtype=np.complex128,
    )
    support = complex_centered_support_envelope(coefficients, phases)
    return support, coefficients - np.mean(coefficients), phases


def audit_mobius_sign_cyclotomic(
    horizon: int,
    split: str = "historical_replay",
) -> dict[str, Any]:
    base_row = audit_complex_cyclotomic_dispersion(horizon, split)
    values, positive, negative, metadata = vaughan_mobius_sign_layers(horizon)
    positions = np.arange(horizon + 3, dtype=np.int64)
    root_bump = np.sqrt(dyadic_bump(positions, horizon))
    target = root_bump * values
    nfft = next_power_of_two(2 * len(target))
    target_transform = _rfft(target, nfft)
    frequencies = np.arange(len(target_transform), dtype=np.float64) / nfft
    multiplicity = np.full(len(target_transform), 2.0, dtype=np.float64)
    multiplicity[0] = 1.0
    multiplicity[-1] = 1.0
    major_mask, arc_count = rational_major_mask(
        frequencies,
        horizon,
        DENOMINATOR_CUTOFF,
    )
    cells = connected_components(~major_mask)
    labels, adjacency_failures = right_boundary_labels(
        cells,
        frequencies,
        DENOMINATOR_CUTOFF,
    )
    positive_groups = endpoint_groups_for_layer(
        positive,
        root_bump,
        target_transform,
        nfft,
        multiplicity,
        cells,
        labels,
    )
    negative_groups = endpoint_groups_for_layer(
        negative,
        root_bump,
        target_transform,
        nfft,
        multiplicity,
        cells,
        labels,
    )
    base_profiles = {
        int(profile["right_denominator"]): profile
        for profile in base_row["complex_denominator_profile"]
    }
    base_row.pop("complex_denominator_profile")

    independent_mean_envelope = 0.0
    independent_centered_envelope = 0.0
    signed_mean_envelope = 0.0
    signed_centered_envelope = 0.0
    aggregate_cross_covariance = 0.0
    aggregate_polarization_cancellation_energy = 0.0
    maximum_profile_reconstruction_error = 0.0
    maximum_polarization_identity_error = 0.0
    maximum_layer_phase_error = 0.0
    denominator_profiles: list[dict[str, Any]] = []

    for denominator in sorted(positive_groups):
        positive_records = positive_groups[denominator]
        negative_records = negative_groups[denominator]
        positive_numerators = [record[2] for record in positive_records]
        negative_numerators = [record[2] for record in negative_records]
        if positive_numerators != negative_numerators:
            raise ValueError("Mobius sign layers have incompatible Farey support")

        positive_support, positive_centered, phases = centered_layer_data(
            positive_records
        )
        negative_support, negative_centered, negative_phases = (
            centered_layer_data(negative_records)
        )
        maximum_layer_phase_error = max(
            maximum_layer_phase_error,
            float(np.max(np.abs(phases - negative_phases))),
        )
        signed_coefficients = np.asarray(
            [
                positive_record[0] - negative_record[0]
                for positive_record, negative_record in zip(
                    positive_records,
                    negative_records,
                    strict=True,
                )
            ],
            dtype=np.complex128,
        )
        signed_support = complex_centered_support_envelope(
            signed_coefficients,
            phases,
        )
        base_profile = base_profiles[denominator]
        profile_errors = (
            abs(
                signed_support["coefficient_mean_real"]
                - float(base_profile["coefficient_mean_real"])
            ),
            abs(
                signed_support["coefficient_mean_imaginary"]
                - float(base_profile["coefficient_mean_imaginary"])
            ),
            abs(
                signed_support["complex_mean_signed_contribution"]
                - float(base_profile["complex_mean_signed_contribution"])
            ),
            abs(
                signed_support["complex_centered_signed_contribution"]
                - float(base_profile["complex_centered_signed_contribution"])
            ),
            abs(
                signed_support["complex_centered_coefficient_l2_norm"]
                - float(
                    base_profile[
                        "complex_centered_coefficient_l2_norm"
                    ]
                )
            ),
        )
        profile_reconstruction_error = max(profile_errors)
        maximum_profile_reconstruction_error = max(
            maximum_profile_reconstruction_error,
            profile_reconstruction_error,
        )

        positive_norm = float(np.linalg.norm(positive_centered))
        negative_norm = float(np.linalg.norm(negative_centered))
        signed_centered = positive_centered - negative_centered
        signed_norm = float(np.linalg.norm(signed_centered))
        cross_covariance = float(
            np.real(np.vdot(positive_centered, negative_centered))
        )
        polarization_rhs = (
            positive_norm**2
            + negative_norm**2
            - 2.0 * cross_covariance
        )
        polarization_identity_error = abs(
            signed_norm**2 - polarization_rhs
        )
        maximum_polarization_identity_error = max(
            maximum_polarization_identity_error,
            polarization_identity_error,
        )
        geometry_norm = float(
            signed_support["complex_projected_phase_l2_norm"]
        )
        positive_mean_cost = abs(
            float(positive_support["complex_mean_signed_contribution"])
        )
        negative_mean_cost = abs(
            float(negative_support["complex_mean_signed_contribution"])
        )
        total_mean_cost = abs(
            float(signed_support["complex_mean_signed_contribution"])
        )
        separated_centered_cost = (
            positive_norm + negative_norm
        ) * geometry_norm
        total_centered_cost = signed_norm * geometry_norm

        independent_mean_envelope += positive_mean_cost + negative_mean_cost
        independent_centered_envelope += separated_centered_cost
        signed_mean_envelope += total_mean_cost
        signed_centered_envelope += total_centered_cost
        aggregate_cross_covariance += cross_covariance
        aggregate_polarization_cancellation_energy += 2.0 * cross_covariance
        denominator_profiles.append(
            {
                "right_denominator": denominator,
                "numerator_count": len(positive_records),
                "positive_mean_signed_contribution": positive_support[
                    "complex_mean_signed_contribution"
                ],
                "negative_mean_signed_contribution": negative_support[
                    "complex_mean_signed_contribution"
                ],
                "signed_mean_contribution": signed_support[
                    "complex_mean_signed_contribution"
                ],
                "positive_centered_l2_norm": positive_norm,
                "negative_centered_l2_norm": negative_norm,
                "signed_centered_l2_norm": signed_norm,
                "centered_cross_covariance": cross_covariance,
                "centered_cross_cosine": (
                    cross_covariance / (positive_norm * negative_norm)
                    if positive_norm and negative_norm
                    else 0.0
                ),
                "polarization_cancellation_energy": 2.0
                * cross_covariance,
                "polarization_identity_error": (
                    polarization_identity_error
                ),
                "signed_mean_envelope": total_mean_cost,
                "independent_sign_mean_envelope": (
                    positive_mean_cost + negative_mean_cost
                ),
                "signed_centered_support_envelope": (
                    total_centered_cost
                ),
                "independent_sign_centered_envelope": (
                    separated_centered_cost
                ),
                "mean_triangle_loss": (
                    positive_mean_cost
                    + negative_mean_cost
                    - total_mean_cost
                ),
                "centered_triangle_loss": (
                    separated_centered_cost - total_centered_cost
                ),
                "profile_reconstruction_error": (
                    profile_reconstruction_error
                ),
            }
        )

    signed_numerator_budget = signed_mean_envelope + signed_centered_envelope
    independent_sign_numerator_budget = (
        independent_mean_envelope + independent_centered_envelope
    )
    inherited_signed_budget = float(
        base_row["complex_scalar_centered_numerator_budget"]
    )
    inherited_budget_error = abs(
        signed_numerator_budget - inherited_signed_budget
    )
    boundary_and_variation = (
        float(base_row["boundary_phase_lipschitz_envelope"])
        + float(base_row["variation_absolute_envelope"])
    )
    independent_sign_adverse_budget = (
        independent_sign_numerator_budget + boundary_and_variation
    )
    independent_sign_lower_bound = (
        float(base_row["known_without_type_ii_minor"])
        - independent_sign_adverse_budget
    )
    signed_lower_bound = float(base_row["complex_sign_free_lower_bound"])

    row = {
        **base_row,
        **metadata,
        "mobius_sign_major_arc_count": arc_count,
        "mobius_sign_minor_cell_count": len(cells),
        "mobius_sign_farey_adjacency_failure_count": (
            adjacency_failures
        ),
        "signed_mean_envelope_reconstructed": signed_mean_envelope,
        "independent_sign_mean_envelope": independent_mean_envelope,
        "signed_centered_envelope_reconstructed": signed_centered_envelope,
        "independent_sign_centered_envelope": (
            independent_centered_envelope
        ),
        "signed_numerator_budget_reconstructed": signed_numerator_budget,
        "inherited_signed_numerator_budget": inherited_signed_budget,
        "inherited_signed_budget_reconstruction_error": (
            inherited_budget_error
        ),
        "independent_sign_numerator_budget": (
            independent_sign_numerator_budget
        ),
        "independent_sign_budget_inflation": (
            independent_sign_numerator_budget - signed_numerator_budget
        ),
        "independent_sign_budget_ratio": (
            independent_sign_numerator_budget / signed_numerator_budget
            if signed_numerator_budget
            else math.inf
        ),
        "independent_sign_adverse_budget": independent_sign_adverse_budget,
        "independent_sign_lower_bound": independent_sign_lower_bound,
        "independent_sign_closes_finite": bool(
            independent_sign_lower_bound > 0
        ),
        "signed_lower_bound": signed_lower_bound,
        "aggregate_centered_cross_covariance": (
            aggregate_cross_covariance
        ),
        "aggregate_polarization_cancellation_energy": (
            aggregate_polarization_cancellation_energy
        ),
        "maximum_profile_reconstruction_error": (
            maximum_profile_reconstruction_error
        ),
        "maximum_polarization_identity_error": (
            maximum_polarization_identity_error
        ),
        "maximum_layer_phase_error": maximum_layer_phase_error,
        "mobius_sign_denominator_profile": denominator_profiles,
    }

    del values, positive, negative, target, target_transform
    del frequencies, multiplicity, major_mask
    gc.collect()
    return row


def analyze_ticket116() -> dict[str, Any]:
    rows = [
        audit_mobius_sign_cyclotomic(
            horizon,
            "mobius_sign_holdout_replay"
            if horizon == HOLDOUT_HORIZON
            else "historical_replay",
        )
        for horizon in HORIZONS
    ]
    frontier = rows[-1]
    contract_failures = sum(
        int(
            float(
                row[
                    "time_domain_sign_layer_reconstruction_max_error"
                ]
            )
            > 1e-9
        )
        + int(
            float(row["maximum_profile_reconstruction_error"]) > 1e-6
        )
        + int(
            float(row["inherited_signed_budget_reconstruction_error"])
            > 1e-5
        )
        + int(
            float(row["maximum_polarization_identity_error"]) > 1e-5
        )
        + int(float(row["maximum_layer_phase_error"]) > 1e-12)
        + int(
            int(row["mobius_sign_farey_adjacency_failure_count"]) != 0
        )
        for row in rows
    )
    return {
        "theorem_name": "ExactVaughanMobiusSignLayerCyclotomicLiftPolarizationIdentityAndIndependentTriangleNoGo",
        "source_ticket": "TICKET-115",
        "exact_mobius_sign_lift": {
            "type_ii_identity": "For the actual Vaughan cutoffs, II(n)=II_plus(n)-II_minus(n), where II_plus and II_minus separately sum the outer divisors with mu(d)=+1 and mu(d)=-1.",
            "endpoint_identity": "Linearity of the DFT, minor-cell prefix sum, and Farey endpoint map gives P_{q,a}=P^+_{q,a}-P^-_{q,a} exactly.",
            "mean_identity": "M_q=M_q^+-M_q^- and Re(M_q H_q)=Re(M_q^+ H_q)-Re(M_q^- H_q).",
            "centered_identity": "Z_q=Z_q^+-Z_q^- after the full complex constant mode is removed in every sign layer.",
        },
        "polarization_theorem": {
            "identity": "||Z_q||_2^2=||Z_q^+||_2^2+||Z_q^-||_2^2-2 Re<Z_q^+,Z_q^->.",
            "meaning": "The effect of the Mobius-sign interaction is represented exactly by the cross term before any norm is applied. Positive covariance reduces the signed norm and negative covariance enlarges it; either effect disappears from an independent triangle bound.",
            "scope": "This is an exact finite-dimensional identity for the actual finite Vaughan layers, not a uniform lower bound for the covariance.",
        },
        "independent_sign_triangle_no_go": {
            "tested_contract": "Pay |Re(M_q^+H_q)|+|Re(M_q^-H_q)| and (||Z_q^+||_2+||Z_q^-||_2)||rho_q-mean rho_q||_2 independently for every q.",
            "deterministic_order": "The independent-sign budget is always at least the signed TICKET115 budget by the scalar and vector triangle inequalities.",
            "finite_result": "The independent-sign contract worsens the numerator budget on all six audited scales and does not close any audited finite scale.",
            "logical_result": "Expanding into Mobius sign layers and then taking separate absolute values cannot prove the retained TICKET115 budget. A proof must preserve signed Mobius interaction or prove a positive cross-layer covariance estimate.",
        },
        "finite_frontier": {
            "maximum_horizon": frontier["horizon"],
            "signed_numerator_budget": frontier[
                "signed_numerator_budget_reconstructed"
            ],
            "independent_sign_numerator_budget": frontier[
                "independent_sign_numerator_budget"
            ],
            "independent_sign_budget_ratio": frontier[
                "independent_sign_budget_ratio"
            ],
            "signed_lower_bound": frontier["signed_lower_bound"],
            "independent_sign_lower_bound": frontier[
                "independent_sign_lower_bound"
            ],
            "aggregate_centered_cross_covariance": frontier[
                "aggregate_centered_cross_covariance"
            ],
            "interpretation": "The row uses measured finite transforms and supplies no asymptotic covariance theorem.",
        },
        "retained_asymptotic_criterion": {
            "statement": "Derive the scalar mean and centered endpoint estimate from the signed outer-Mobius Vaughan sum before applying norms, or prove a denominator-summed lower bound for Re<Z_q^+,Z_q^-> strong enough to keep the combined budget below the independently established positive comparison scale.",
            "positive_scale_obligation": "The major-plus-Type-I-minor comparison term must be proved positive on the same all-sufficiently-large-X range.",
            "counterexample_route": "Construct actual Vaughan sign layers for an unbounded scale sequence whose scalar cancellation and centered covariance fail every fixed subcritical margin.",
        },
        "rows": rows,
        "discarded_routes": [
            "Bound the mu-positive and mu-negative Type-II layers independently after the Farey transform.",
            "Use only ||Z_q^+|| and ||Z_q^-|| while discarding their polarization term.",
            "Infer a uniform positive covariance theorem from the six measured rows.",
            "Treat an abstract favorable pair of sign layers as Vaughan-realizable without the divisor-convolution identity.",
            "Transfer averaged shifted-Mobius results directly to the fixed shift-two binary correlation.",
        ],
        "literature_boundary": {
            "helfgott_type_ii": HELFGOTT_SOURCE,
            "lichtman_shifted_mobius": LICHTMAN_SOURCE,
            "ford_maynard_type_information": FORD_MAYNARD_SOURCE,
            "established_background": "Vaughan Type-II identities, bilinear large-sieve estimates, and averaged Mobius cancellation on shifted primes are established.",
            "project_specific_result": "The exact mu-sign lift through this half-Farey endpoint map, its polarization ledger, and the six-scale independent-sign no-go audit are project-specific.",
            "non_transfer": "The cited results do not provide the fixed-shift, denominator-summed signed covariance or endpoint budget required here.",
        },
        "next_theorem_target": "EventuallySubcriticalSignedVaughanMobiusCyclotomicDispersionBudget",
        "machine_audit": {
            "maximum_horizon": int(frontier["horizon"]),
            "row_count": len(rows),
            "minor_cell_count": int(
                frontier["mobius_sign_minor_cell_count"]
            ),
            "right_denominator_group_count": len(
                frontier["mobius_sign_denominator_profile"]
            ),
            "outer_pair_count": int(frontier["outer_pair_count"]),
            "independent_sign_budget_worsens_count": sum(
                int(float(row["independent_sign_budget_inflation"]) > 0)
                for row in rows
            ),
            "independent_sign_finite_closure_count": sum(
                int(row["independent_sign_closes_finite"])
                for row in rows
            ),
            "positive_aggregate_covariance_count": sum(
                int(
                    float(row["aggregate_centered_cross_covariance"])
                    > 0
                )
                for row in rows
            ),
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET116 proves an exact finite Mobius-sign lift and polarization identity and rejects an independent-sign triangle contract on six finite rows. It does not prove a uniform signed Vaughan estimate, any of the four conjectures, or a conjecture counterexample.",
    }


def transferred_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    target: str,
) -> dict[str, Any]:
    prior = next(
        attempt
        for attempt in source["attempts"]
        if attempt["problem_id"] == problem_id
    )
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin Mobius-sign audit",
        "attempt": "Preserve the existing infinite target; no Twin Mobius-sign shortcut is transferred.",
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "independent_target": target,
        },
        "obstruction": "TICKET116 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket115 = read_json(
        ROOT
        / "data/open-problem/ticket115-twin-complex-cyclotomic-dispersion-audit.json"
    )
    audit = analyze_ticket116()
    attempts = [
        transferred_attempt(
            ticket115,
            "riemann",
            "RH-TICKET-116",
            "NonCircularKernelPositivityPreserved",
            "NonCircularExplicitFormulaKernelPositivity",
        ),
        transferred_attempt(
            ticket115,
            "collatz",
            "CO-TICKET-116",
            "GoldenMeanEscapePreserved",
            "GoldenMeanInvariantSetEscape",
        ),
        transferred_attempt(
            ticket115,
            "goldbach",
            "GB-TICKET-116",
            "JointBalancedGoldbachPreserved",
            "JointBalancedVaughanGoldbachResidualEnvelope",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-116",
            "status": "mobius_sign_lift_exact_polarization_audited_independent_triangle_refuted_open",
            "route": "SignedVaughanMobiusCyclotomicDispersion",
            "proof_or_counterexample_mode": "exact Mobius-sign lift, polarization identity, and independent-sign no-go",
            "attempt": "Lift every half-Farey endpoint coefficient into the actual mu-positive and mu-negative Vaughan layers, retain their scalar difference and centered cross covariance, and test independent sign-layer bounds.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-115",
                "audit_ref": "twin_mobius_sign_cyclotomic_audit",
            },
            "obstruction": "Mean cancellation and the centered cross covariance are measured finite quantities, and the covariance changes sign across the audit; no uniform Vaughan estimate controls their combined effect yet.",
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Expand the signed endpoint functional by dyadic outer-divisor blocks and prove a denominator-summed bilinear dispersion bound, or construct an unbounded Vaughan-realizable margin failure.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "mobius_sign_lift_exact_polarization_audited_independent_triangle_refuted_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_mobius_sign_cyclotomic_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket116-twin-mobius-sign-cyclotomic-audit.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-116-kernel-positivity-preserved.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-116-golden-mean-preserved.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-116-joint-balanced-preserved.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-116-mobius-sign-cyclotomic-audit.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
