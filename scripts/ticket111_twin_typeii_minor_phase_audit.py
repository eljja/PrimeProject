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


GENERATED_AT = "2026-07-13T18:30:00+09:00"
SCHEMA = "primeproject.ticket111-twin-typeii-minor-phase-audit.v1"
CALIBRATION_HORIZONS = (4_096, 32_768, 262_144, 1_048_576)
HOLDOUT_HORIZON = 2_097_152
DENOMINATOR_CUTOFF = 32
POWER_SAVING_EXPONENT = 1 / 6
HELFGOTT_MINOR_SOURCE = "https://arxiv.org/abs/1205.5252"
FORD_MAYNARD_SOURCE = "https://arxiv.org/abs/2407.14368"


def _rfft(values: np.ndarray, nfft: int) -> np.ndarray:
    padded = np.zeros(nfft, dtype=np.float64)
    padded[: len(values)] = values
    return np.fft.rfft(padded)


def audit_typeii_minor_phase(horizon: int, split: str = "calibration_replay") -> dict[str, Any]:
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

    def cross_contribution(source: np.ndarray) -> np.ndarray:
        return (
            multiplicity
            * np.real(np.conj(source) * target_transform * shift_phase)
            / nfft
        )

    total_cross = cross_contribution(target_transform)
    structured_cross = cross_contribution(structured_transform)
    bilinear_cross = cross_contribution(bilinear_transform)
    major_mask, arc_count = rational_major_mask(
        frequencies,
        horizon,
        DENOMINATOR_CUTOFF,
    )
    minor_mask = ~major_mask

    exact_correlation = float(np.sum(total_cross))
    structured_correlation = float(np.sum(structured_cross))
    bilinear_correlation = float(np.sum(bilinear_cross))
    component_reconstruction_error = abs(
        exact_correlation - structured_correlation - bilinear_correlation
    )

    major_total = float(np.sum(total_cross[major_mask]))
    minor_total = float(np.sum(total_cross[minor_mask]))
    structured_minor = float(np.sum(structured_cross[minor_mask]))
    bilinear_minor = float(np.sum(bilinear_cross[minor_mask]))
    minor_component_reconstruction_error = abs(
        minor_total - structured_minor - bilinear_minor
    )
    known_without_bilinear_minor = major_total + structured_minor

    minor_bilinear_energy = float(
        np.sum(
            multiplicity[minor_mask]
            * np.abs(bilinear_transform[minor_mask]) ** 2
            / nfft
        )
    )
    minor_target_energy = float(
        np.sum(
            multiplicity[minor_mask]
            * np.abs(target_transform[minor_mask]) ** 2
            / nfft
        )
    )
    global_cauchy_envelope = math.sqrt(minor_bilinear_energy * minor_target_energy)
    per_bin_amplitude = (
        multiplicity
        * np.abs(np.conj(bilinear_transform) * target_transform)
        / nfft
    )
    phase_blind_bin_envelope = float(np.sum(per_bin_amplitude[minor_mask]))
    phase_blind_lower_bound = known_without_bilinear_minor - phase_blind_bin_envelope
    phase_blind_route_refuted = phase_blind_lower_bound <= 0 < exact_correlation

    registered_envelope = phase_blind_bin_envelope * horizon ** (-POWER_SAVING_EXPONENT)
    registered_lower_bound = known_without_bilinear_minor - registered_envelope
    registered_lower_inequality_passes = bilinear_minor >= -registered_envelope
    registered_positivity_closes = registered_lower_bound > 0

    row = {
        "horizon": horizon,
        "split": split,
        "u": u,
        "v": v,
        "fft_length": nfft,
        "denominator_cutoff": DENOMINATOR_CUTOFF,
        "major_arc_count": arc_count,
        "exact_symmetric_correlation": exact_correlation,
        "structured_total_correlation": structured_correlation,
        "type_ii_total_correlation": bilinear_correlation,
        "component_reconstruction_error": component_reconstruction_error,
        "lambda_reconstruction_max_error": identity["lambda_reconstruction_max_error"],
        "major_total_contribution": major_total,
        "minor_total_contribution": minor_total,
        "structured_minor_contribution": structured_minor,
        "type_ii_minor_contribution": bilinear_minor,
        "minor_component_reconstruction_error": minor_component_reconstruction_error,
        "known_without_type_ii_minor": known_without_bilinear_minor,
        "minor_type_ii_energy": minor_bilinear_energy,
        "minor_target_energy": minor_target_energy,
        "global_cauchy_envelope": global_cauchy_envelope,
        "phase_blind_bin_envelope": phase_blind_bin_envelope,
        "phase_blind_lower_bound": phase_blind_lower_bound,
        "phase_blind_route_refuted": phase_blind_route_refuted,
        "required_saving_factor_over_bin_envelope": (
            phase_blind_bin_envelope / known_without_bilinear_minor
            if known_without_bilinear_minor > 0
            else math.inf
        ),
        "observed_signed_to_bin_envelope_ratio": (
            bilinear_minor / phase_blind_bin_envelope
            if phase_blind_bin_envelope
            else 0.0
        ),
        "registered_power_saving_exponent": POWER_SAVING_EXPONENT,
        "registered_power_saving_envelope": registered_envelope,
        "registered_power_saving_lower_bound": registered_lower_bound,
        "registered_lower_inequality_passes": registered_lower_inequality_passes,
        "registered_positivity_closes": registered_positivity_closes,
    }

    del target_transform, structured_transform, bilinear_transform
    del total_cross, structured_cross, bilinear_cross, per_bin_amplitude
    gc.collect()
    return row


def analyze_ticket111() -> dict[str, Any]:
    rows = [
        audit_typeii_minor_phase(horizon, "calibration_replay")
        for horizon in CALIBRATION_HORIZONS
    ]
    rows.append(audit_typeii_minor_phase(HOLDOUT_HORIZON, "post_selection_holdout"))
    holdout = rows[-1]
    contract_failures = sum(
        int(float(row["component_reconstruction_error"]) > 1e-6)
        + int(float(row["minor_component_reconstruction_error"]) > 1e-6)
        + int(float(row["lambda_reconstruction_max_error"]) > 1e-10)
        for row in rows
    )
    phase_blind_refutations = sum(int(row["phase_blind_route_refuted"]) for row in rows)
    holdout_candidate_failures = int(not holdout["registered_lower_inequality_passes"]) + int(
        not holdout["registered_positivity_closes"]
    )
    return {
        "theorem_name": "ExactVaughanMinorCrossSpectrumAndPhaseBlindPartitionNoGo",
        "source_ticket": "TICKET-110",
        "exact_cross_spectrum": {
            "identity": "The fixed-bump shift-two correlation equals the sum of its Vaughan Type I and Type II cross-spectra against the shifted full von Mangoldt target.",
            "minor_identity": "On the fixed Q=32 minor mask, minor_total=structured_minor+type_ii_minor exactly up to floating-point audit tolerance.",
            "logical_value": "The missing signed estimate is isolated on the Type II cross-spectrum instead of charging the whole minor spectral energy.",
        },
        "phase_blind_partition_no_go": {
            "class": "Partition the fixed minor bins arbitrarily, apply Cauchy-Schwarz on each cell, and retain no complex phase information.",
            "lower_envelope": "Every such partition envelope is at least sum_k m_k |II_hat(k)||Lambda_hat(k)|/N, the singleton-bin envelope.",
            "finite_result": "Even the singleton-bin envelope leaves a negative total lower bound on every audited horizon through the fresh 2M holdout.",
            "consequence": "Refining frequency cells or optimizing an energy partition cannot close this route; a phase-aware bilinear estimate is necessary.",
            "scope": "This is an exact finite no-go for the stated phase-blind partition-Cauchy class, not a no-go for the circle method or Type II estimates.",
        },
        "registered_power_saving_candidate": {
            "inequality": "TypeII_minor(X) >= -X^(-1/6) sum_minor m_k |II_hat(k)||Lambda_hat(k)|/N.",
            "motivation": "U(X) is of order X^(1/3); square-root cancellation over that outer scale suggests the test exponent 1/6.",
            "selection_boundary": "The exponent and Q=32 were frozen after exploratory rows at or below 1,048,576; 2,097,152 is the first post-selection holdout.",
            "holdout_status": "finite_candidate_survives_not_a_theorem" if holdout_candidate_failures == 0 else "candidate_refuted_on_holdout",
            "holdout_actual_type_ii_minor": holdout["type_ii_minor_contribution"],
            "holdout_candidate_envelope": holdout["registered_power_saving_envelope"],
            "holdout_resulting_lower_bound": holdout["registered_power_saving_lower_bound"],
            "proof_gap": "Finite survival does not establish a uniform inequality, an asymptotic major-arc formula, or the parity-breaking input required for twin-prime infinitude.",
        },
        "rows": rows,
        "discarded_routes": [
            "Charge the whole minor spectral energy after Vaughan decomposition.",
            "Refine minor arcs into favorable energy cells while discarding all complex phase.",
            "Infer a uniform X^(-1/6) theorem from one post-selection holdout.",
            "Treat the observed Type II sign as fixed across scales.",
            "Transfer ternary Goldbach minor-arc bounds directly to the binary twin correlation without a proved reduction.",
        ],
        "literature_boundary": {
            "helfgott_minor_arcs": HELFGOTT_MINOR_SOURCE,
            "ford_maynard_type_information": FORD_MAYNARD_SOURCE,
            "established_background": "Vaughan Type II bilinear sums, rational major/minor arcs, smoothing, and large-sieve estimates are established tools.",
            "project_specific_result": "The exact fixed-bump Type II cross-spectrum bridge, the phase-blind partition-Cauchy no-go certificate, and the explicitly labeled 2M holdout.",
        },
        "next_theorem_target": "PhaseAwareVaughanTypeIIMinorArcPowerSaving",
        "machine_audit": {
            "maximum_horizon": HOLDOUT_HORIZON,
            "row_count": len(rows),
            "calibration_row_count": len(CALIBRATION_HORIZONS),
            "holdout_row_count": 1,
            "phase_blind_refutation_count": phase_blind_refutations,
            "holdout_candidate_failure_count": holdout_candidate_failures,
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET111 proves finite exact spectral identities and a no-go theorem for a specified phase-blind partition-Cauchy class. The X^(-1/6) inequality only survives one finite holdout. It proves none of the four conjectures and certifies no conjecture counterexample.",
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
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin Type II phase audit",
        "attempt": "Preserve the existing infinite target; no Twin cross-spectrum shortcut is transferred.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "independent_target": target},
        "obstruction": "TICKET111 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket110 = read_json(ROOT / "data/open-problem/ticket110-twin-rational-arc-budget.json")
    audit = analyze_ticket111()
    attempts = [
        transferred_attempt(ticket110, "riemann", "RH-TICKET-111", "NonCircularKernelPositivityPreserved", "NonCircularExplicitFormulaKernelPositivity"),
        transferred_attempt(ticket110, "collatz", "CO-TICKET-111", "GoldenMeanEscapePreserved", "GoldenMeanInvariantSetEscape"),
        transferred_attempt(ticket110, "goldbach", "GB-TICKET-111", "JointBalancedGoldbachPreserved", "JointBalancedVaughanGoldbachResidualEnvelope"),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-111",
            "status": "typeii_cross_spectrum_exact_phase_blind_partition_refuted_candidate_survives_holdout_open",
            "route": "VaughanTypeIIMinorCrossSpectrum",
            "proof_or_counterexample_mode": "exact component spectrum plus phase-blind no-go and post-selection holdout",
            "attempt": "Decompose the fixed-bump correlation into exact Vaughan Type I and Type II cross-spectra, refute every phase-blind partition-Cauchy refinement, and test a frozen X^(-1/6) lower-envelope candidate at 2M.",
            "bounded_result": {"source_ticket": "TP-TICKET-110", "audit_ref": "twin_typeii_minor_phase_audit"},
            "obstruction": audit["registered_power_saving_candidate"]["proof_gap"],
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Derive the phase-aware bilinear inequality uniformly in X from Vaughan coefficients and rational frequency separation, or construct an adversarial coefficient model that refutes it.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "typeii_cross_spectrum_exact_phase_blind_partition_refuted_candidate_survives_holdout_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_typeii_minor_phase_audit": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket111-twin-typeii-minor-phase-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-111-kernel-positivity-preserved.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-111-golden-mean-preserved.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-111-joint-balanced-preserved.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-111-typeii-minor-phase-audit.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
