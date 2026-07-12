from __future__ import annotations

import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import contamination_weight_bound, prime_sieve
from ticket100_extended_residual_vaughan_audit import lambda_values
from ticket108_twin_joint_equivalence_smoothing import dyadic_bump


GENERATED_AT = "2026-07-12T22:20:00+09:00"
SCHEMA = "primeproject.ticket109-twin-spectral-phase-audit.v1"
HORIZONS = (4_096, 32_768, 262_144, 1_048_576)
LOW_FREQUENCY_CUTOFFS = (1 / 128, 1 / 64, 1 / 32, 1 / 16, 1 / 12, 1 / 8)
HELFGOTT_SOURCE = "https://arxiv.org/abs/1501.05438"


def next_power_of_two(value: int) -> int:
    return 1 << (value - 1).bit_length()


def audit_spectral_phase(horizon: int) -> dict[str, Any]:
    values, _ = lambda_values(horizon + 2)
    positions = np.arange(horizon + 3, dtype=np.int64)
    weights = dyadic_bump(positions, horizon)
    sequence = np.sqrt(weights) * values
    nfft = next_power_of_two(2 * len(sequence))
    padded = np.zeros(nfft, dtype=np.float64)
    padded[: len(sequence)] = sequence

    direct = float(np.dot(sequence[:-2], sequence[2:]))
    transform = np.fft.rfft(padded)
    power = np.abs(transform) ** 2 / nfft
    multiplicity = np.full(len(power), 2.0, dtype=np.float64)
    multiplicity[0] = 1.0
    multiplicity[-1] = 1.0
    frequencies = np.arange(len(power), dtype=np.float64) / nfft
    phase = np.cos(4.0 * math.pi * frequencies)
    contributions = multiplicity * power * phase
    spectral = float(np.sum(contributions))
    total_energy = float(np.sum(multiplicity * power))
    positive_phase = float(np.sum(contributions[phase >= 0]))
    negative_phase = float(np.sum(contributions[phase < 0]))

    band_rows: list[dict[str, Any]] = []
    for cutoff in LOW_FREQUENCY_CUTOFFS:
        mask = frequencies <= cutoff + 1e-15
        low_energy = float(np.sum((multiplicity * power)[mask]))
        outside_energy = total_energy - low_energy
        minimum_phase = math.cos(4.0 * math.pi * cutoff)
        lower_bound = minimum_phase * low_energy - outside_energy
        band_rows.append(
            {
                "cutoff_fraction": cutoff,
                "minimum_in_band_phase": minimum_phase,
                "low_frequency_energy": low_energy,
                "outside_energy": outside_energy,
                "rigorous_correlation_lower_bound": lower_bound,
                "lower_bound_is_positive": lower_bound > 0,
            }
        )
    best_band = max(band_rows, key=lambda row: float(row["rigorous_correlation_lower_bound"]))

    lower = horizon // 2 + 1
    numbers = np.arange(lower, horizon + 1, dtype=np.int64)
    pair_weights = np.sqrt(dyadic_bump(numbers, horizon) * dyadic_bump(numbers + 2, horizon))
    exact_terms = values[lower : horizon + 1] * values[lower + 2 : horizon + 3]
    is_prime, _ = prime_sieve(horizon + 2)
    prime_pair_mask = np.fromiter(
        (bool(is_prime[int(number)] and is_prime[int(number) + 2]) for number in numbers),
        dtype=np.bool_,
        count=len(numbers),
    )
    twin_weight = float(np.dot(pair_weights[prime_pair_mask], exact_terms[prime_pair_mask]))
    contamination = direct - twin_weight
    bound = contamination_weight_bound(horizon)
    cancellation_denominator = positive_phase + abs(negative_phase)

    return {
        "horizon": horizon,
        "fft_length": nfft,
        "symmetric_bump_correlation": direct,
        "spectral_correlation": spectral,
        "spectral_identity_absolute_error": abs(direct - spectral),
        "total_spectral_energy": total_energy,
        "positive_phase_contribution": positive_phase,
        "negative_phase_contribution": negative_phase,
        "phase_cancellation_ratio": direct / cancellation_denominator if cancellation_denominator else 0.0,
        "twin_prime_weight": twin_weight,
        "proper_prime_power_contamination": contamination,
        "contamination_bound": bound,
        "contamination_bound_holds": contamination <= bound + 1e-9,
        "contamination_decomposition_absolute_error": abs(direct - twin_weight - contamination),
        "band_rows": band_rows,
        "best_low_frequency_cutoff": best_band["cutoff_fraction"],
        "best_low_frequency_lower_bound": best_band["rigorous_correlation_lower_bound"],
        "low_frequency_only_route_refuted": float(best_band["rigorous_correlation_lower_bound"]) <= 0 < direct,
    }


def analyze_ticket109() -> dict[str, Any]:
    rows = [audit_spectral_phase(horizon) for horizon in HORIZONS]
    contract_failures = sum(
        int(float(row["spectral_identity_absolute_error"]) > 1e-6)
        + int(float(row["contamination_decomposition_absolute_error"]) > 1e-7)
        + int(not row["contamination_bound_holds"])
        + int(not row["low_frequency_only_route_refuted"])
        for row in rows
    )
    return {
        "theorem_name": "SymmetricBumpSpectralPhaseAndLowFrequencyNoGo",
        "source_ticket": "TICKET-108",
        "exact_spectral_identity": {
            "sequence": "f_X(n)=sqrt(W(n/X)) Lambda(n), zero-padded beyond the dyadic support.",
            "correlation": "S_sym(X)=sum_n f_X(n)f_X(n+2).",
            "fourier": "S_sym(X)=N^(-1) sum_k |F_X(k)|^2 cos(4 pi k/N).",
            "novelty_boundary": "The full Fourier identity is exactly equivalent to the correlation and is not itself a lower-bound theorem.",
        },
        "low_frequency_no_go": {
            "tested_family": "For |k|/N<=delta, use cos(4 pi k/N)>=cos(4 pi delta), and bound every outside phase by -1.",
            "result": "Every tested single-origin low-frequency lower bound is negative while the exact symmetric correlation is positive.",
            "reason": "Prime spectral mass is arithmetic and distributed near rational frequencies; a single band around zero discards the Ramanujan/singular-series structure.",
            "scope": "This refutes the tested sufficient inequality family, not all Fourier or circle-method approaches.",
        },
        "rows": rows,
        "discarded_routes": [
            "Present the exact full-spectrum autocorrelation identity as a new reduction.",
            "Use only a single low-frequency band around zero and replace every outside phase by its worst value.",
            "Infer an asymptotic phase margin from finite positive exact correlations.",
            "Use positive spectral energy without retaining the shift-two cosine phase.",
        ],
        "literature_boundary": {
            "established_background": "Major/minor arc decompositions and smoothed Type II sums are established circle-method tools; PrimeProject does not claim them as new.",
            "source": HELFGOTT_SOURCE,
            "project_specific_target": "Build a replayable rational-arc phase budget for the fixed bump and reject any budget that imports the target correlation through an unproved remainder.",
        },
        "next_theorem_target": "RamanujanMajorArcPhaseMarginWithMinorArcControl",
        "machine_audit": {
            "maximum_horizon": HORIZONS[-1],
            "row_count": len(rows),
            "low_frequency_refutation_count": sum(int(row["low_frequency_only_route_refuted"]) for row in rows),
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET109 proves exact finite spectral identities and refutes one single-origin low-frequency sufficient-bound family on every audited horizon. It proves none of the four conjectures and no conjecture counterexample.",
    }


def transferred_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin spectral-phase audit",
        "attempt": "Preserve the existing infinite target; no Twin spectral shortcut is transferred.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "independent_target": target},
        "obstruction": "TICKET109 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket108 = read_json(ROOT / "data/open-problem/ticket108-twin-joint-equivalence-smoothing.json")
    audit = analyze_ticket109()
    attempts = [
        transferred_attempt(ticket108, "riemann", "RH-TICKET-109", "NonCircularKernelPositivityPreserved", "NonCircularExplicitFormulaKernelPositivity"),
        transferred_attempt(ticket108, "collatz", "CO-TICKET-109", "GoldenMeanEscapePreserved", "GoldenMeanInvariantSetEscape"),
        transferred_attempt(ticket108, "goldbach", "GB-TICKET-109", "JointBalancedGoldbachPreserved", "JointBalancedVaughanGoldbachResidualEnvelope"),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-109",
            "status": "spectral_identity_exact_low_frequency_route_refuted_rational_arc_theorem_open",
            "route": "SymmetricBumpSpectralPhaseAudit",
            "proof_or_counterexample_mode": "exact Fourier identity plus low-frequency sufficient-bound falsification",
            "attempt": "Convert the fixed bump to a zero-padded autocorrelation spectrum, preserve the shift-two phase, and test whether a single origin-centered band supplies a rigorous lower bound.",
            "bounded_result": {"source_ticket": "TP-TICKET-108", "audit_ref": "twin_spectral_phase_audit"},
            "obstruction": audit["low_frequency_no_go"]["reason"],
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Construct rational major-arc masks with explicit Ramanujan coefficients and a separately audited minor-arc Type II remainder.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "spectral_identity_exact_low_frequency_route_refuted_rational_arc_theorem_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_spectral_phase_audit": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket109-twin-spectral-phase-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-109-kernel-positivity-preserved.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-109-golden-mean-preserved.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-109-joint-balanced-preserved.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-109-spectral-phase-audit.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
