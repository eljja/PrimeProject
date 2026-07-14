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
from ticket116_twin_mobius_sign_cyclotomic_audit import (
    endpoint_groups_for_layer,
)


GENERATED_AT = "2026-07-15T09:10:00+09:00"
SCHEMA = "primeproject.ticket117-twin-dyadic-mobius-endpoint-gram-audit.v1"
HORIZONS = (*CALIBRATION_HORIZONS, HOLDOUT_HORIZON)
HELFGOTT_SOURCE = "https://arxiv.org/abs/1501.05438"
LICHTMAN_SOURCE = "https://arxiv.org/abs/2009.08969"
FORD_MAYNARD_SOURCE = "https://arxiv.org/abs/2407.14368"


def dyadic_outer_blocks(
    minimum_divisor: int,
    maximum_divisor: int,
) -> list[dict[str, int | str]]:
    blocks: list[dict[str, int | str]] = []
    lower = minimum_divisor
    while lower <= maximum_divisor:
        shell_lower = 1 << (lower.bit_length() - 1)
        shell_upper = 2 * shell_lower - 1
        upper = min(shell_upper, maximum_divisor)
        blocks.append(
            {
                "block_index": len(blocks),
                "label": f"D{shell_lower}",
                "shell_lower": shell_lower,
                "shell_upper": shell_upper,
                "actual_lower": lower,
                "actual_upper": upper,
            }
        )
        lower = upper + 1
    return blocks


def contiguous_partitions(
    block_count: int,
    maximum_group_width: int | None = None,
    minimum_group_count: int = 2,
) -> list[list[tuple[int, int]]]:
    partitions: list[list[tuple[int, int]]] = []
    for cut_mask in range(1 << max(block_count - 1, 0)):
        groups: list[tuple[int, int]] = []
        start = 0
        for boundary in range(block_count - 1):
            if cut_mask & (1 << boundary):
                groups.append((start, boundary + 1))
                start = boundary + 1
        groups.append((start, block_count))
        if len(groups) < minimum_group_count:
            continue
        if maximum_group_width is not None and any(
            end - start > maximum_group_width for start, end in groups
        ):
            continue
        partitions.append(groups)
    return partitions


def evaluate_partition(
    partition: list[tuple[int, int]],
    denominator_profiles: list[dict[str, Any]],
    block_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    mean_budget = 0.0
    centered_budget = 0.0
    group_mean_budgets = np.zeros(len(partition), dtype=np.float64)
    group_centered_budgets = np.zeros(len(partition), dtype=np.float64)
    for profile in denominator_profiles:
        means = np.asarray(
            profile["block_mean_signed_contributions"],
            dtype=np.float64,
        )
        gram = np.asarray(profile["real_gram_matrix"], dtype=np.float64)
        geometry_norm = float(profile["projected_phase_l2_norm"])
        for group_index, (start, end) in enumerate(partition):
            mean_cost = abs(float(np.sum(means[start:end])))
            energy = float(np.sum(gram[start:end, start:end]))
            centered_cost = math.sqrt(max(energy, 0.0)) * geometry_norm
            mean_budget += mean_cost
            centered_budget += centered_cost
            group_mean_budgets[group_index] += mean_cost
            group_centered_budgets[group_index] += centered_cost
    groups = [
        {
            "first_block": block_rows[start]["label"],
            "last_block": block_rows[end - 1]["label"],
            "block_count": end - start,
            "actual_lower": block_rows[start]["actual_lower"],
            "actual_upper": block_rows[end - 1]["actual_upper"],
            "mean_envelope": float(group_mean_budgets[group_index]),
            "centered_envelope": float(
                group_centered_budgets[group_index]
            ),
            "numerator_budget": float(
                group_mean_budgets[group_index]
                + group_centered_budgets[group_index]
            ),
        }
        for group_index, (start, end) in enumerate(partition)
    ]
    return {
        "group_count": len(partition),
        "maximum_group_width": max(end - start for start, end in partition),
        "groups": groups,
        "mean_envelope": mean_budget,
        "centered_envelope": centered_budget,
        "numerator_budget": mean_budget + centered_budget,
    }


def signed_dyadic_endpoint_groups(
    horizon: int,
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[int, list[tuple[complex, complex, int]]]],
]:
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

    limit = len(values) - 1
    maximum_outer_divisor = limit // (v + 1)
    blocks = dyadic_outer_blocks(u + 1, maximum_outer_divisor)
    large_lambda = sorted(
        (number, weight)
        for number, weight in mangoldt.items()
        if number > v
    )
    reconstructed = np.zeros_like(values)
    group_rows: list[
        dict[int, list[tuple[complex, complex, int]]]
    ] = []
    block_rows: list[dict[str, Any]] = []
    total_pair_count = 0

    for block in blocks:
        layer = np.zeros_like(values)
        divisor_count = 0
        positive_divisor_count = 0
        negative_divisor_count = 0
        pair_count = 0
        for divisor in range(
            int(block["actual_lower"]),
            int(block["actual_upper"]) + 1,
        ):
            sign = mu[divisor]
            if sign == 0:
                continue
            divisor_count += 1
            positive_divisor_count += int(sign > 0)
            negative_divisor_count += int(sign < 0)
            for number, weight in large_lambda:
                step = divisor * number
                if step > limit:
                    break
                layer[step::step] += sign * weight
                pair_count += 1
        reconstructed += layer
        group_rows.append(
            endpoint_groups_for_layer(
                layer,
                root_bump,
                target_transform,
                nfft,
                multiplicity,
                cells,
                labels,
            )
        )
        block_rows.append(
            {
                **block,
                "nonzero_mobius_divisor_count": divisor_count,
                "positive_mobius_divisor_count": positive_divisor_count,
                "negative_mobius_divisor_count": negative_divisor_count,
                "outer_pair_count": pair_count,
                "time_domain_l2_norm": float(np.linalg.norm(layer)),
                "time_domain_nonzero_count": int(np.count_nonzero(layer)),
            }
        )
        total_pair_count += pair_count
        del layer
        gc.collect()

    reconstruction_error = float(
        np.max(np.abs(reconstructed - signed_type_ii))
    )
    metadata = {
        "horizon": horizon,
        "u": u,
        "v": v,
        "fft_length": nfft,
        "maximum_outer_divisor": maximum_outer_divisor,
        "dyadic_block_count": len(blocks),
        "outer_pair_count": total_pair_count,
        "major_arc_count": arc_count,
        "minor_cell_count": len(cells),
        "farey_adjacency_failure_count": adjacency_failures,
        "lambda_reconstruction_max_error": identity[
            "lambda_reconstruction_max_error"
        ],
        "time_domain_dyadic_reconstruction_max_error": reconstruction_error,
    }
    del values, signed_type_ii, reconstructed, target, target_transform
    del frequencies, multiplicity, major_mask
    gc.collect()
    return metadata, block_rows, group_rows


def audit_dyadic_mobius_endpoint_gram(
    horizon: int,
    independent_sign_budget: float,
    split: str = "historical_replay",
) -> dict[str, Any]:
    base_row = audit_complex_cyclotomic_dispersion(horizon, split)
    metadata, block_rows, block_groups = signed_dyadic_endpoint_groups(
        horizon
    )
    base_profiles = {
        int(profile["right_denominator"]): profile
        for profile in base_row["complex_denominator_profile"]
    }
    base_row.pop("complex_denominator_profile")

    block_count = len(block_rows)
    aggregate_gram = np.zeros((block_count, block_count), dtype=np.float64)
    geometry_weighted_gram = np.zeros(
        (block_count, block_count), dtype=np.float64
    )
    block_mean_costs = np.zeros(block_count, dtype=np.float64)
    block_centered_costs = np.zeros(block_count, dtype=np.float64)
    block_signed_mean = np.zeros(block_count, dtype=np.float64)
    signed_mean_envelope = 0.0
    signed_centered_envelope = 0.0
    maximum_profile_error = 0.0
    maximum_gram_identity_error = 0.0
    maximum_support_error = 0.0
    positive_cross_pair_count = 0
    negative_cross_pair_count = 0
    denominator_profiles: list[dict[str, Any]] = []

    for denominator in sorted(base_profiles):
        records_by_block = [groups[denominator] for groups in block_groups]
        reference_numerators = [
            record[2] for record in records_by_block[0]
        ]
        coefficient_rows: list[np.ndarray] = []
        centered_rows: list[np.ndarray] = []
        support_rows: list[dict[str, float]] = []
        phases: np.ndarray | None = None
        for records in records_by_block:
            if [record[2] for record in records] != reference_numerators:
                raise ValueError("Dyadic blocks have incompatible Farey support")
            coefficients = np.asarray(
                [record[0] for record in records],
                dtype=np.complex128,
            )
            block_phases = np.asarray(
                [record[1] for record in records],
                dtype=np.complex128,
            )
            if phases is None:
                phases = block_phases
            else:
                maximum_support_error = max(
                    maximum_support_error,
                    float(np.max(np.abs(phases - block_phases))),
                )
            support = complex_centered_support_envelope(
                coefficients,
                block_phases,
            )
            coefficient_rows.append(coefficients)
            centered_rows.append(coefficients - np.mean(coefficients))
            support_rows.append(support)
        if phases is None:
            raise ValueError("Missing Farey phases")

        total_coefficients = np.sum(coefficient_rows, axis=0)
        total_support = complex_centered_support_envelope(
            total_coefficients,
            phases,
        )
        base_profile = base_profiles[denominator]
        profile_error = max(
            abs(
                float(total_support[key]) - float(base_profile[key])
            )
            for key in (
                "coefficient_mean_real",
                "coefficient_mean_imaginary",
                "complex_mean_signed_contribution",
                "complex_centered_signed_contribution",
                "complex_centered_coefficient_l2_norm",
            )
        )
        maximum_profile_error = max(maximum_profile_error, profile_error)

        gram = np.asarray(
            [
                [float(np.real(np.vdot(left, right))) for right in centered_rows]
                for left in centered_rows
            ],
            dtype=np.float64,
        )
        aggregate_gram += gram
        total_centered = np.sum(centered_rows, axis=0)
        total_energy = float(np.linalg.norm(total_centered) ** 2)
        gram_energy = float(np.sum(gram))
        gram_identity_error = abs(total_energy - gram_energy)
        maximum_gram_identity_error = max(
            maximum_gram_identity_error,
            gram_identity_error,
        )
        diagonal_energy = float(np.trace(gram))
        off_diagonal_energy = gram_energy - diagonal_energy
        geometry_norm = float(
            total_support["complex_projected_phase_l2_norm"]
        )
        geometry_weighted_gram += gram * geometry_norm**2
        block_norms = np.sqrt(np.maximum(np.diag(gram), 0.0))
        mean_costs = np.asarray(
            [
                abs(float(support["complex_mean_signed_contribution"]))
                for support in support_rows
            ],
            dtype=np.float64,
        )
        centered_costs = block_norms * geometry_norm
        signed_mean_cost = abs(
            float(total_support["complex_mean_signed_contribution"])
        )
        signed_centered_cost = math.sqrt(max(total_energy, 0.0)) * geometry_norm
        signed_mean_envelope += signed_mean_cost
        signed_centered_envelope += signed_centered_cost
        block_mean_costs += mean_costs
        block_centered_costs += centered_costs
        block_signed_mean += np.asarray(
            [
                float(support["complex_mean_signed_contribution"])
                for support in support_rows
            ]
        )
        upper_triangle = gram[np.triu_indices(block_count, 1)]
        positive_cross_pair_count += int(np.count_nonzero(upper_triangle > 0))
        negative_cross_pair_count += int(np.count_nonzero(upper_triangle < 0))
        denominator_profiles.append(
            {
                "right_denominator": denominator,
                "numerator_count": len(reference_numerators),
                "signed_mean_envelope": signed_mean_cost,
                "independent_dyadic_mean_envelope": float(np.sum(mean_costs)),
                "block_mean_signed_contributions": [
                    float(support["complex_mean_signed_contribution"])
                    for support in support_rows
                ],
                "signed_centered_envelope": signed_centered_cost,
                "independent_dyadic_centered_envelope": float(
                    np.sum(centered_costs)
                ),
                "diagonal_centered_energy": diagonal_energy,
                "off_diagonal_centered_energy": off_diagonal_energy,
                "signed_centered_energy": total_energy,
                "projected_phase_l2_norm": geometry_norm,
                "geometry_weighted_off_diagonal_energy": (
                    off_diagonal_energy * geometry_norm**2
                ),
                "cross_cancellation_fraction": (
                    -off_diagonal_energy / diagonal_energy
                    if diagonal_energy
                    else 0.0
                ),
                "gram_identity_error": gram_identity_error,
                "real_gram_matrix": gram.tolist(),
            }
        )

    signed_budget = signed_mean_envelope + signed_centered_envelope
    dyadic_mean_budget = float(np.sum(block_mean_costs))
    dyadic_centered_budget = float(np.sum(block_centered_costs))
    dyadic_budget = dyadic_mean_budget + dyadic_centered_budget
    inherited_signed_budget = float(
        base_row["complex_scalar_centered_numerator_budget"]
    )
    boundary_and_variation = (
        float(base_row["boundary_phase_lipschitz_envelope"])
        + float(base_row["variation_absolute_envelope"])
    )
    dyadic_adverse_budget = dyadic_budget + boundary_and_variation
    dyadic_lower_bound = (
        float(base_row["known_without_type_ii_minor"])
        - dyadic_adverse_budget
    )
    aggregate_total_energy = float(np.sum(aggregate_gram))
    aggregate_diagonal_energy = float(np.trace(aggregate_gram))
    aggregate_off_diagonal_energy = (
        aggregate_total_energy - aggregate_diagonal_energy
    )
    weighted_total_energy = float(np.sum(geometry_weighted_gram))
    weighted_diagonal_energy = float(np.trace(geometry_weighted_gram))
    weighted_off_diagonal_energy = (
        weighted_total_energy - weighted_diagonal_energy
    )
    denominator_count = len(denominator_profiles)
    denominator_cauchy_centered_envelope = math.sqrt(
        denominator_count
        * sum(
            float(profile["signed_centered_envelope"]) ** 2
            for profile in denominator_profiles
        )
    )
    denominator_cauchy_numerator_budget = (
        signed_mean_envelope + denominator_cauchy_centered_envelope
    )
    denominator_cauchy_adverse_budget = (
        denominator_cauchy_numerator_budget + boundary_and_variation
    )
    denominator_cauchy_lower_bound = (
        float(base_row["known_without_type_ii_minor"])
        - denominator_cauchy_adverse_budget
    )
    all_nontrivial_partitions = [
        evaluate_partition(partition, denominator_profiles, block_rows)
        for partition in contiguous_partitions(block_count)
    ]
    width_two_partitions = [
        evaluate_partition(partition, denominator_profiles, block_rows)
        for partition in contiguous_partitions(
            block_count,
            maximum_group_width=2,
        )
    ]
    all_nontrivial_partitions.sort(
        key=lambda profile: float(profile["numerator_budget"])
    )
    width_two_partitions.sort(
        key=lambda profile: float(profile["numerator_budget"])
    )
    best_nontrivial_partition = all_nontrivial_partitions[0]
    best_width_two_partition = width_two_partitions[0]
    for profile in (
        best_nontrivial_partition,
        best_width_two_partition,
    ):
        profile["budget_ratio_to_signed"] = (
            float(profile["numerator_budget"]) / signed_budget
            if signed_budget
            else math.inf
        )
        profile["adverse_budget"] = (
            float(profile["numerator_budget"]) + boundary_and_variation
        )
        profile["lower_bound"] = (
            float(base_row["known_without_type_ii_minor"])
            - float(profile["adverse_budget"])
        )
        profile["closes_finite"] = bool(float(profile["lower_bound"]) > 0)
    pair_profiles: list[dict[str, Any]] = []
    for left in range(block_count):
        for right in range(left + 1, block_count):
            interaction = 2.0 * float(
                geometry_weighted_gram[left, right]
            )
            pair_profiles.append(
                {
                    "left_block": block_rows[left]["label"],
                    "right_block": block_rows[right]["label"],
                    "geometry_weighted_interaction_energy": interaction,
                    "effect": "adverse_reinforcement"
                    if interaction > 0
                    else "favorable_cancellation"
                    if interaction < 0
                    else "neutral",
                }
            )
    pair_profiles.sort(
        key=lambda profile: abs(
            float(profile["geometry_weighted_interaction_energy"])
        ),
        reverse=True,
    )
    block_profiles = []
    for block, mean_cost, centered_cost, signed_mean in zip(
        block_rows,
        block_mean_costs,
        block_centered_costs,
        block_signed_mean,
        strict=True,
    ):
        block_profiles.append(
            {
                **block,
                "denominator_summed_mean_envelope": float(mean_cost),
                "denominator_summed_centered_envelope": float(centered_cost),
                "denominator_summed_budget": float(mean_cost + centered_cost),
                "denominator_summed_signed_mean_contribution": float(
                    signed_mean
                ),
            }
        )

    return {
        **base_row,
        **metadata,
        "signed_mean_envelope_reconstructed": signed_mean_envelope,
        "signed_centered_envelope_reconstructed": signed_centered_envelope,
        "signed_numerator_budget_reconstructed": signed_budget,
        "inherited_signed_numerator_budget": inherited_signed_budget,
        "inherited_signed_budget_reconstruction_error": abs(
            signed_budget - inherited_signed_budget
        ),
        "independent_dyadic_mean_envelope": dyadic_mean_budget,
        "independent_dyadic_centered_envelope": dyadic_centered_budget,
        "independent_dyadic_numerator_budget": dyadic_budget,
        "independent_dyadic_budget_ratio": (
            dyadic_budget / signed_budget if signed_budget else math.inf
        ),
        "independent_sign_numerator_budget": independent_sign_budget,
        "dyadic_to_sign_budget_ratio": (
            dyadic_budget / independent_sign_budget
            if independent_sign_budget
            else math.inf
        ),
        "dyadic_adverse_budget": dyadic_adverse_budget,
        "dyadic_lower_bound": dyadic_lower_bound,
        "dyadic_closes_finite": bool(dyadic_lower_bound > 0),
        "denominator_cauchy_centered_envelope": (
            denominator_cauchy_centered_envelope
        ),
        "denominator_cauchy_numerator_budget": (
            denominator_cauchy_numerator_budget
        ),
        "denominator_cauchy_adverse_budget": (
            denominator_cauchy_adverse_budget
        ),
        "denominator_cauchy_lower_bound": denominator_cauchy_lower_bound,
        "denominator_cauchy_closes_finite": bool(
            denominator_cauchy_lower_bound > 0
        ),
        "denominator_cauchy_bound_slack": (
            denominator_cauchy_centered_envelope
            - signed_centered_envelope
        ),
        "best_nontrivial_contiguous_partition": (
            best_nontrivial_partition
        ),
        "best_width_two_contiguous_partition": (
            best_width_two_partition
        ),
        "signed_lower_bound": float(base_row["complex_sign_free_lower_bound"]),
        "aggregate_diagonal_centered_energy": aggregate_diagonal_energy,
        "aggregate_off_diagonal_centered_energy": aggregate_off_diagonal_energy,
        "aggregate_signed_centered_energy": aggregate_total_energy,
        "aggregate_cross_cancellation_fraction": (
            -aggregate_off_diagonal_energy / aggregate_diagonal_energy
            if aggregate_diagonal_energy
            else 0.0
        ),
        "geometry_weighted_diagonal_energy": weighted_diagonal_energy,
        "geometry_weighted_off_diagonal_energy": (
            weighted_off_diagonal_energy
        ),
        "geometry_weighted_signed_energy": weighted_total_energy,
        "geometry_weighted_cross_cancellation_fraction": (
            -weighted_off_diagonal_energy / weighted_diagonal_energy
            if weighted_diagonal_energy
            else 0.0
        ),
        "positive_cross_pair_count": positive_cross_pair_count,
        "negative_cross_pair_count": negative_cross_pair_count,
        "maximum_profile_reconstruction_error": maximum_profile_error,
        "maximum_gram_identity_error": maximum_gram_identity_error,
        "maximum_layer_phase_error": maximum_support_error,
        "dyadic_block_profile": block_profiles,
        "aggregate_real_gram_matrix": aggregate_gram.tolist(),
        "geometry_weighted_real_gram_matrix": (
            geometry_weighted_gram.tolist()
        ),
        "geometry_weighted_block_pair_profile": pair_profiles,
        "dyadic_denominator_profile": denominator_profiles,
    }


def analyze_ticket117() -> dict[str, Any]:
    ticket116 = read_json(
        ROOT
        / "data/open-problem/ticket116-twin-mobius-sign-cyclotomic-audit.json"
    )
    sign_rows = {
        int(row["horizon"]): row
        for row in ticket116["twin_mobius_sign_cyclotomic_audit"]["rows"]
    }
    rows = [
        audit_dyadic_mobius_endpoint_gram(
            horizon,
            float(sign_rows[horizon]["independent_sign_numerator_budget"]),
            "dyadic_mobius_holdout_replay"
            if horizon == HOLDOUT_HORIZON
            else "historical_replay",
        )
        for horizon in HORIZONS
    ]
    frontier = rows[-1]
    contract_failures = sum(
        int(float(row["time_domain_dyadic_reconstruction_max_error"]) > 1e-9)
        + int(float(row["maximum_profile_reconstruction_error"]) > 1e-6)
        + int(float(row["inherited_signed_budget_reconstruction_error"]) > 1e-5)
        + int(float(row["maximum_gram_identity_error"]) > 1e-4)
        + int(float(row["maximum_layer_phase_error"]) > 1e-12)
        + int(int(row["farey_adjacency_failure_count"]) != 0)
        for row in rows
    )
    return {
        "theorem_name": "ExactSignedVaughanDyadicEndpointGramIdentityAndIndependentBlockTriangleAudit",
        "source_ticket": "TICKET-116",
        "exact_dyadic_lift": {
            "time_identity": "II(n)=sum_B II_B(n), where B runs over the actual truncated dyadic outer-divisor shells and II_B retains mu(d) inside the block.",
            "endpoint_identity": "P_{q,a}=sum_B P_{q,a}^{(B)} by linearity of the DFT, minor-cell sum, and Farey endpoint map.",
            "mean_identity": "M_q=sum_B M_q^{(B)} before any absolute value is taken.",
            "centered_identity": "Z_q=sum_B Z_q^{(B)} after complex centering in the same numerator space.",
        },
        "gram_identity": {
            "identity": "||Z_q||_2^2=sum_{B,C} Re<Z_q^{(B)},Z_q^{(C)}>.",
            "meaning": "The real Gram matrix retains every within-block norm and cross-block cancellation or reinforcement exactly.",
            "scope": "This is an exact finite-dimensional identity, not a denominator-summed asymptotic dispersion estimate.",
        },
        "independent_block_triangle_audit": {
            "tested_contract": "Pay sum_B |Re(M_q^{(B)}H_q)| and sum_B ||Z_q^{(B)}||_2 ||rho_q-mean rho_q||_2 for every q.",
            "deterministic_order": "The independent-block budget is at least the fully signed budget by scalar and vector triangle inequalities.",
            "finite_result": "Singleton dyadic blocks worsen the fully signed budget on every row and close none. Adjacent width-two grouping recovers most of the loss and is only 1,236.3 above finite closure at 4M, but still closes no audited row.",
        },
        "adjacent_pair_frontier": {
            "restriction": "Use one fixed contiguous partition per horizon and place at most two adjacent dyadic shells in each group; never optimize by denominator.",
            "frontier_partition": frontier[
                "best_width_two_contiguous_partition"
            ]["groups"],
            "numerator_budget": frontier[
                "best_width_two_contiguous_partition"
            ]["numerator_budget"],
            "ratio_to_fully_signed_budget": frontier[
                "best_width_two_contiguous_partition"
            ]["budget_ratio_to_signed"],
            "finite_lower_bound": frontier[
                "best_width_two_contiguous_partition"
            ]["lower_bound"],
            "closure_shortfall": max(
                0.0,
                -float(
                    frontier["best_width_two_contiguous_partition"][
                        "lower_bound"
                    ]
                ),
            ),
            "stability_observation": "The same adjacent-pair pattern is selected at 2M and 4M. This is finite evidence only and is not promoted to an eventual-stability theorem.",
        },
        "finite_frontier": {
            "maximum_horizon": frontier["horizon"],
            "dyadic_block_count": frontier["dyadic_block_count"],
            "signed_numerator_budget": frontier[
                "signed_numerator_budget_reconstructed"
            ],
            "independent_dyadic_numerator_budget": frontier[
                "independent_dyadic_numerator_budget"
            ],
            "independent_sign_numerator_budget": frontier[
                "independent_sign_numerator_budget"
            ],
            "dyadic_budget_ratio": frontier["independent_dyadic_budget_ratio"],
            "dyadic_to_sign_budget_ratio": frontier[
                "dyadic_to_sign_budget_ratio"
            ],
            "dyadic_lower_bound": frontier["dyadic_lower_bound"],
            "denominator_cauchy_numerator_budget": frontier[
                "denominator_cauchy_numerator_budget"
            ],
            "denominator_cauchy_lower_bound": frontier[
                "denominator_cauchy_lower_bound"
            ],
            "best_width_two_partition_budget": frontier[
                "best_width_two_contiguous_partition"
            ]["numerator_budget"],
            "best_width_two_partition_lower_bound": frontier[
                "best_width_two_contiguous_partition"
            ]["lower_bound"],
            "aggregate_cross_cancellation_fraction": frontier[
                "aggregate_cross_cancellation_fraction"
            ],
            "geometry_weighted_cross_cancellation_fraction": frontier[
                "geometry_weighted_cross_cancellation_fraction"
            ],
            "interpretation": "All values are finite measured transforms and do not establish a uniform-in-X theorem.",
        },
        "rows": rows,
        "retained_asymptotic_criterion": {
            "statement": "Prove a denominator-summed signed adjacent-dyadic-pair endpoint estimate that controls scalar means and within-pair Gram interactions with a fixed all-sufficiently-large-X margin.",
            "positive_scale_obligation": "Prove positivity of the same major-plus-Type-I comparison scale on the identical X range.",
            "counterexample_route": "Construct an unbounded sequence of Vaughan-realizable dyadic endpoint Gram matrices whose independent-block inflation or adverse off-diagonal energy defeats every fixed subcritical margin.",
        },
        "discarded_routes": [
            "Replace signed dyadic blocks by separate mu-positive and mu-negative layers.",
            "Delete the off-diagonal Gram entries before testing their sign and magnitude.",
            "Infer a uniform cross-block covariance sign from finitely many horizons.",
            "Treat finite closure as a Twin Prime proof.",
        ],
        "literature_boundary": {
            "helfgott_type_ii": HELFGOTT_SOURCE,
            "lichtman_shifted_mobius": LICHTMAN_SOURCE,
            "ford_maynard_type_information": FORD_MAYNARD_SOURCE,
            "established_background": "Dyadic Type-II decomposition, bilinear estimates, and averaged shifted-Mobius cancellation are established tools.",
            "project_specific_result": "The exact signed dyadic lift through this endpoint map and its finite real-Gram ledger are project-specific.",
            "non_transfer": "The cited works do not supply the fixed-shift, denominator-summed endpoint Gram estimate required here.",
        },
        "next_theorem_target": "EventuallySubcriticalAdjacentDyadicPairVaughanEndpointBudget",
        "machine_audit": {
            "maximum_horizon": int(frontier["horizon"]),
            "row_count": len(rows),
            "minor_cell_count": int(frontier["minor_cell_count"]),
            "dyadic_block_count": int(frontier["dyadic_block_count"]),
            "right_denominator_group_count": len(
                frontier["dyadic_denominator_profile"]
            ),
            "outer_pair_count": int(frontier["outer_pair_count"]),
            "dyadic_budget_worsens_count": sum(
                int(float(row["independent_dyadic_budget_ratio"]) > 1.0)
                for row in rows
            ),
            "dyadic_improves_sign_count": sum(
                int(float(row["dyadic_to_sign_budget_ratio"]) < 1.0)
                for row in rows
            ),
            "dyadic_finite_closure_count": sum(
                int(row["dyadic_closes_finite"]) for row in rows
            ),
            "positive_aggregate_cross_cancellation_count": sum(
                int(float(row["aggregate_cross_cancellation_fraction"]) > 0)
                for row in rows
            ),
            "denominator_cauchy_finite_closure_count": sum(
                int(row["denominator_cauchy_closes_finite"])
                for row in rows
            ),
            "denominator_cauchy_violation_count": sum(
                int(
                    float(row["denominator_cauchy_bound_slack"])
                    < -1e-7
                )
                for row in rows
            ),
            "width_two_partition_finite_closure_count": sum(
                int(
                    row["best_width_two_contiguous_partition"][
                        "closes_finite"
                    ]
                )
                for row in rows
            ),
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET117 proves exact finite signed-dyadic endpoint and Gram identities and audits an independent-block contract. It does not prove the required uniform bilinear estimate, any of the four conjectures, or a conjecture counterexample.",
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
        "proof_or_counterexample_mode": "preserve the independent target during the Twin dyadic-Gram audit",
        "attempt": "Preserve the existing infinite target; no Twin endpoint-Gram shortcut is transferred.",
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "independent_target": target,
        },
        "obstruction": "TICKET117 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket116 = read_json(
        ROOT
        / "data/open-problem/ticket116-twin-mobius-sign-cyclotomic-audit.json"
    )
    audit = analyze_ticket117()
    attempts = [
        transferred_attempt(
            ticket116,
            "riemann",
            "RH-TICKET-117",
            "NonCircularKernelPositivityPreserved",
            "NonCircularExplicitFormulaKernelPositivity",
        ),
        transferred_attempt(
            ticket116,
            "collatz",
            "CO-TICKET-117",
            "GoldenMeanEscapePreserved",
            "GoldenMeanInvariantSetEscape",
        ),
        transferred_attempt(
            ticket116,
            "goldbach",
            "GB-TICKET-117",
            "JointBalancedGoldbachPreserved",
            "JointBalancedVaughanGoldbachResidualEnvelope",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-117",
            "status": "signed_dyadic_endpoint_gram_exact_independent_block_audited_open",
            "route": "SignedDyadicVaughanEndpointGramBudget",
            "proof_or_counterexample_mode": "exact signed dyadic lift, real-Gram ledger, and independent-block audit",
            "attempt": "Keep mu(d) inside actual dyadic outer-divisor blocks, map every block to the same Farey endpoints, and retain all cross-block Gram entries before testing a blockwise bound.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-116",
                "audit_ref": "twin_dyadic_mobius_endpoint_gram_audit",
            },
            "obstruction": "The measured block cancellation remains finite data; no uniform denominator-summed signed bilinear estimate controls the full endpoint Gram contribution yet.",
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Localize the adverse Gram mass by dyadic block pair and denominator, then prove a large-sieve/dispersion bound for the retained signed pairs or construct an unbounded Vaughan-realizable margin failure.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "signed_dyadic_endpoint_gram_exact_independent_block_audited_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_dyadic_mobius_endpoint_gram_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket117-twin-dyadic-mobius-endpoint-gram-audit.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-117-kernel-positivity-preserved.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-117-golden-mean-preserved.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-117-joint-balanced-preserved.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-117-dyadic-mobius-endpoint-gram-audit.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
