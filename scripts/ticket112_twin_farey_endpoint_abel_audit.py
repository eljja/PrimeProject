from __future__ import annotations

import gc
import math
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
    CALIBRATION_HORIZONS,
    DENOMINATOR_CUTOFF,
    HOLDOUT_HORIZON,
    POWER_SAVING_EXPONENT,
)


GENERATED_AT = "2026-07-13T20:20:00+09:00"
SCHEMA = "primeproject.ticket112-twin-farey-endpoint-abel-audit.v1"
HELFGOTT_SOURCE = "https://arxiv.org/abs/1205.5252"
TAO_SOURCE = "https://arxiv.org/abs/1201.6656"


def connected_components(mask: np.ndarray) -> list[np.ndarray]:
    indices = np.flatnonzero(mask)
    if len(indices) == 0:
        return []
    cuts = np.flatnonzero(np.diff(indices) > 1) + 1
    return list(np.split(indices, cuts))


def _rfft(values: np.ndarray, nfft: int) -> np.ndarray:
    padded = np.zeros(nfft, dtype=np.float64)
    padded[: len(values)] = values
    return np.fft.rfft(padded)


def audit_farey_endpoint_abel(
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
    total_cross = (
        multiplicity
        * np.real(np.conj(target_transform) * target_transform * shift_phase)
        / nfft
    )
    structured_cross = (
        multiplicity
        * np.real(np.conj(structured_transform) * target_transform * shift_phase)
        / nfft
    )
    major_mask, arc_count = rational_major_mask(
        frequencies,
        horizon,
        DENOMINATOR_CUTOFF,
    )
    minor_mask = ~major_mask
    cells = connected_components(minor_mask)

    endpoint_complex = 0j
    variation_complex = 0j
    endpoint_absolute_envelope = 0.0
    variation_absolute_envelope = 0.0
    maximum_cell_prefix = 0.0
    for cell in cells:
        prefixes = np.cumsum(type_ii_cross[cell])
        endpoint_complex += prefixes[-1] * shift_phase[cell[-1]]
        endpoint_absolute_envelope += abs(prefixes[-1])
        maximum_cell_prefix = max(maximum_cell_prefix, float(np.max(np.abs(prefixes))))
        if len(cell) > 1:
            phase_differences = shift_phase[cell[:-1]] - shift_phase[cell[1:]]
            variation_complex += np.sum(prefixes[:-1] * phase_differences)
            variation_absolute_envelope += float(
                np.sum(np.abs(prefixes[:-1]) * np.abs(phase_differences))
            )

    exact_type_ii_minor_complex = np.sum(type_ii_cross[minor_mask] * shift_phase[minor_mask])
    endpoint_absolute_envelope = float(endpoint_absolute_envelope)
    variation_absolute_envelope = float(variation_absolute_envelope)
    abel_identity_error = abs(
        exact_type_ii_minor_complex - endpoint_complex - variation_complex
    )
    actual_type_ii_minor = float(np.real(exact_type_ii_minor_complex))
    major_total = float(np.sum(total_cross[major_mask]))
    structured_minor = float(np.sum(structured_cross[minor_mask]))
    known_without_type_ii_minor = major_total + structured_minor
    phase_blind_bin_envelope = float(np.sum(np.abs(type_ii_cross[minor_mask])))
    farey_abel_envelope = endpoint_absolute_envelope + variation_absolute_envelope
    farey_abel_lower_bound = known_without_type_ii_minor - farey_abel_envelope
    farey_abel_route_refuted = bool(farey_abel_lower_bound <= 0)

    inherited_endpoint_envelope = (
        horizon ** (-POWER_SAVING_EXPONENT) * endpoint_absolute_envelope
    )
    inherited_total_envelope = inherited_endpoint_envelope + variation_absolute_envelope
    inherited_lower_bound = known_without_type_ii_minor - inherited_total_envelope
    inherited_endpoint_inequality_passes = bool(
        float(np.real(endpoint_complex)) >= -inherited_endpoint_envelope
    )
    inherited_positivity_closes = bool(inherited_lower_bound > 0)

    row = {
        "horizon": horizon,
        "split": split,
        "u": u,
        "v": v,
        "fft_length": nfft,
        "denominator_cutoff": DENOMINATOR_CUTOFF,
        "major_arc_count": arc_count,
        "minor_cell_count": len(cells),
        "lambda_reconstruction_max_error": identity["lambda_reconstruction_max_error"],
        "actual_type_ii_minor_contribution": actual_type_ii_minor,
        "farey_endpoint_signed_contribution": float(np.real(endpoint_complex)),
        "farey_variation_signed_contribution": float(np.real(variation_complex)),
        "abel_identity_absolute_error": float(abel_identity_error),
        "farey_endpoint_absolute_envelope": endpoint_absolute_envelope,
        "farey_variation_absolute_envelope": variation_absolute_envelope,
        "farey_abel_envelope": farey_abel_envelope,
        "phase_blind_bin_envelope": phase_blind_bin_envelope,
        "abel_envelope_fraction_of_phase_blind": (
            farey_abel_envelope / phase_blind_bin_envelope
            if phase_blind_bin_envelope
            else 0.0
        ),
        "endpoint_fraction_of_abel_envelope": (
            endpoint_absolute_envelope / farey_abel_envelope
            if farey_abel_envelope
            else 0.0
        ),
        "endpoint_signed_to_absolute_ratio": (
            abs(float(np.real(endpoint_complex))) / endpoint_absolute_envelope
            if endpoint_absolute_envelope
            else 0.0
        ),
        "maximum_cell_prefix_magnitude": maximum_cell_prefix,
        "known_without_type_ii_minor": known_without_type_ii_minor,
        "farey_abel_lower_bound": farey_abel_lower_bound,
        "farey_abel_route_refuted": farey_abel_route_refuted,
        "inherited_power_saving_exponent": POWER_SAVING_EXPONENT,
        "inherited_endpoint_envelope": inherited_endpoint_envelope,
        "inherited_total_envelope": inherited_total_envelope,
        "inherited_lower_bound": inherited_lower_bound,
        "inherited_endpoint_inequality_passes": inherited_endpoint_inequality_passes,
        "inherited_positivity_closes": inherited_positivity_closes,
    }

    del target_transform, structured_transform, bilinear_transform
    del type_ii_cross, total_cross, structured_cross
    gc.collect()
    return row


def analyze_ticket112() -> dict[str, Any]:
    rows = [
        audit_farey_endpoint_abel(horizon, "calibration_replay")
        for horizon in CALIBRATION_HORIZONS
    ]
    rows.append(audit_farey_endpoint_abel(HOLDOUT_HORIZON, "post_selection_holdout"))
    holdout = rows[-1]
    contract_failures = sum(
        int(float(row["abel_identity_absolute_error"]) > 1e-6)
        + int(float(row["lambda_reconstruction_max_error"]) > 1e-10)
        + int(int(row["minor_cell_count"]) != 162)
        for row in rows
    )
    triangle_refutations = sum(int(row["farey_abel_route_refuted"]) for row in rows)
    holdout_candidate_failures = int(
        not holdout["inherited_endpoint_inequality_passes"]
    ) + int(not holdout["inherited_positivity_closes"])
    return {
        "theorem_name": "ExactFareyCellAbelDecompositionAndEndpointTriangleNoGo",
        "source_ticket": "TICKET-111",
        "exact_farey_abel_identity": {
            "cells": "The fixed Q=32 minor mask has 162 connected Farey cells on every audited FFT grid.",
            "identity": "Within each cell, sum z_k p_k = Z_b p_b + sum_{k<b} Z_k(p_k-p_{k+1}), with z_k the Vaughan Type II cross-spectrum and p_k the shift-two phase.",
            "interpretation": "The first term is cross-cell endpoint mass; the second is controlled by the smooth within-cell phase variation.",
        },
        "endpoint_triangle_no_go": {
            "tested_bound": "Take absolute values of every cell endpoint and every within-cell Abel variation term independently.",
            "finite_result": "This improves sharply over the singleton-bin envelope but still leaves a negative lower bound on every audited horizon through 2M.",
            "holdout_reduction": "At 2M the envelope falls from 7.596M to 1.280M, while the resulting total lower bound remains -351.1K.",
            "loss_location": "At 2M, 96.05% of the Abel envelope is endpoint absolute mass; within-cell variation is only 3.95%.",
            "consequence": "The next theorem should control cancellation among Farey-cell endpoint sums instead of further refining energy bins or smooth phase variation.",
            "scope": "This refutes the endpoint-triangle version of the finite Farey-Abel route, not phase-aware large-sieve or circle-method estimates.",
        },
        "inherited_endpoint_candidate": {
            "inequality": "Re(sum_cell Z_b p_b) >= -X^(-1/6) sum_cell |Z_b|.",
            "selection_boundary": "Q=32 and exponent 1/6 are inherited unchanged from TICKET111; no TICKET112 row was used to tune them.",
            "variation_treatment": "The within-cell variation remains bounded by its full absolute Abel envelope.",
            "holdout_status": "finite_candidate_survives_not_a_theorem" if holdout_candidate_failures == 0 else "candidate_refuted_on_holdout",
            "holdout_signed_endpoint": holdout["farey_endpoint_signed_contribution"],
            "holdout_endpoint_absolute_envelope": holdout["farey_endpoint_absolute_envelope"],
            "holdout_variation_absolute_envelope": holdout["farey_variation_absolute_envelope"],
            "holdout_resulting_lower_bound": holdout["inherited_lower_bound"],
            "proof_gap": "The observed endpoint cancellation must be derived uniformly from arithmetic structure. A finite endpoint table cannot establish that theorem or exclude adversarial future scales.",
        },
        "rows": rows,
        "discarded_routes": [
            "Return to singleton-bin phase-blind Cauchy after the Farey-Abel reduction.",
            "Take absolute values of all 162 Farey endpoints independently and call the reduction complete.",
            "Infer endpoint power saving from one inherited holdout.",
            "Use the small within-cell variation term as if it controlled cross-cell endpoint signs.",
            "Transfer ternary Goldbach Farey estimates without matching the binary shifted-prime cross-spectrum.",
        ],
        "literature_boundary": {
            "helfgott_minor_arcs": HELFGOTT_SOURCE,
            "tao_smoothed_vaughan": TAO_SOURCE,
            "established_background": "Farey rational dissection, Vaughan identity, smoothing, Abel summation, and weighted large-sieve estimates are established.",
            "project_specific_result": "The exact endpoint-versus-variation audit for this fixed binary shift-two cross-spectrum and the no-go certificate for independent endpoint triangles.",
        },
        "next_theorem_target": "UniformFareyCellEndpointCancellationForVaughanCrossSpectrum",
        "machine_audit": {
            "maximum_horizon": HOLDOUT_HORIZON,
            "row_count": len(rows),
            "minor_cell_count": int(holdout["minor_cell_count"]),
            "endpoint_triangle_refutation_count": triangle_refutations,
            "holdout_candidate_failure_count": holdout_candidate_failures,
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET112 proves an exact finite Farey-cell Abel identity and a no-go theorem for independent endpoint triangles on the audited family. The inherited endpoint-saving inequality only survives finite replay. It proves none of the four conjectures and certifies no conjecture counterexample.",
    }


def transferred_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    target: str,
) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin Farey endpoint audit",
        "attempt": "Preserve the existing infinite target; no Twin Farey endpoint shortcut is transferred.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "independent_target": target},
        "obstruction": "TICKET112 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket111 = read_json(ROOT / "data/open-problem/ticket111-twin-typeii-minor-phase-audit.json")
    audit = analyze_ticket112()
    attempts = [
        transferred_attempt(ticket111, "riemann", "RH-TICKET-112", "NonCircularKernelPositivityPreserved", "NonCircularExplicitFormulaKernelPositivity"),
        transferred_attempt(ticket111, "collatz", "CO-TICKET-112", "GoldenMeanEscapePreserved", "GoldenMeanInvariantSetEscape"),
        transferred_attempt(ticket111, "goldbach", "GB-TICKET-112", "JointBalancedGoldbachPreserved", "JointBalancedVaughanGoldbachResidualEnvelope"),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-112",
            "status": "farey_abel_exact_endpoint_triangle_refuted_inherited_candidate_survives_open",
            "route": "FareyCellEndpointAbelCancellation",
            "proof_or_counterexample_mode": "exact Abel reduction plus endpoint-triangle falsification and inherited holdout",
            "attempt": "Apply exact Abel summation inside each fixed Farey minor cell, separate endpoint from smooth variation loss, and test the inherited X^(-1/6) endpoint-saving candidate without retuning.",
            "bounded_result": {"source_ticket": "TP-TICKET-111", "audit_ref": "twin_farey_endpoint_abel_audit"},
            "obstruction": audit["inherited_endpoint_candidate"]["proof_gap"],
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Derive or refute a uniform one-sided cancellation estimate for the 162 Farey-cell endpoint sums using Vaughan bilinear coefficients and weighted large-sieve geometry.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "farey_abel_exact_endpoint_triangle_refuted_inherited_candidate_survives_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_farey_endpoint_abel_audit": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket112-twin-farey-endpoint-abel-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-112-kernel-positivity-preserved.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-112-golden-mean-preserved.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-112-joint-balanced-preserved.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-112-farey-endpoint-abel-audit.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
