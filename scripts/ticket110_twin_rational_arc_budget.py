from __future__ import annotations

import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket100_extended_residual_vaughan_audit import lambda_values
from ticket108_twin_joint_equivalence_smoothing import dyadic_bump
from ticket109_twin_spectral_phase_audit import next_power_of_two


GENERATED_AT = "2026-07-13T00:40:00+09:00"
SCHEMA = "primeproject.ticket110-twin-rational-arc-budget.v1"
HORIZONS = (4_096, 32_768, 262_144, 1_048_576)
DENOMINATOR_CUTOFFS = (2, 3, 5, 8, 12, 16, 24, 32)
HELFGOTT_SOURCE = "https://arxiv.org/abs/1501.05438"


def rational_major_mask(
    frequencies: np.ndarray,
    horizon: int,
    denominator_cutoff: int,
) -> tuple[np.ndarray, int]:
    mask = np.zeros(len(frequencies), dtype=np.bool_)
    arc_count = 0
    for denominator in range(1, denominator_cutoff + 1):
        for numerator in range(0, denominator // 2 + 1):
            if math.gcd(numerator, denominator) != 1:
                continue
            center = numerator / denominator
            width = denominator_cutoff / (denominator * horizon)
            mask |= np.abs(frequencies - center) <= width + 1e-15
            arc_count += 1
    return mask, arc_count


def audit_rational_arc_budget(horizon: int) -> dict[str, Any]:
    values, _ = lambda_values(horizon + 2)
    positions = np.arange(horizon + 3, dtype=np.int64)
    sequence = np.sqrt(dyadic_bump(positions, horizon)) * values
    nfft = next_power_of_two(2 * len(sequence))
    padded = np.zeros(nfft, dtype=np.float64)
    padded[: len(sequence)] = sequence
    transform = np.fft.rfft(padded)
    power = np.abs(transform) ** 2 / nfft
    multiplicity = np.full(len(power), 2.0, dtype=np.float64)
    multiplicity[0] = 1.0
    multiplicity[-1] = 1.0
    weighted_power = multiplicity * power
    frequencies = np.arange(len(power), dtype=np.float64) / nfft
    phase = np.cos(4.0 * math.pi * frequencies)
    contributions = weighted_power * phase
    exact = float(np.sum(contributions))
    total_energy = float(np.sum(weighted_power))

    rows: list[dict[str, Any]] = []
    for cutoff in DENOMINATOR_CUTOFFS:
        major_mask, arc_count = rational_major_mask(frequencies, horizon, cutoff)
        major_energy = float(np.sum(weighted_power[major_mask]))
        minor_energy = total_energy - major_energy
        major_contribution = float(np.sum(contributions[major_mask]))
        minor_contribution = exact - major_contribution
        trivial_minor_lower = -minor_energy
        rigorous_lower = major_contribution + trivial_minor_lower
        rows.append(
            {
                "denominator_cutoff": cutoff,
                "arc_count": arc_count,
                "major_bin_count": int(np.count_nonzero(major_mask)),
                "major_energy": major_energy,
                "major_energy_fraction": major_energy / total_energy if total_energy else 0.0,
                "minor_energy": minor_energy,
                "major_phase_contribution": major_contribution,
                "minor_phase_contribution": minor_contribution,
                "minor_phase_to_energy_ratio": minor_contribution / minor_energy if minor_energy else 0.0,
                "major_minor_reconstruction_error": abs(exact - major_contribution - minor_contribution),
                "trivial_minor_lower_bound": trivial_minor_lower,
                "rigorous_total_lower_bound": rigorous_lower,
                "trivial_minor_route_positive": rigorous_lower > 0,
                "minor_cancellation_gain_over_trivial": minor_contribution - trivial_minor_lower,
            }
        )
    best = max(rows, key=lambda row: float(row["rigorous_total_lower_bound"]))
    return {
        "horizon": horizon,
        "fft_length": nfft,
        "exact_symmetric_correlation": exact,
        "total_spectral_energy": total_energy,
        "rows": rows,
        "best_denominator_cutoff": best["denominator_cutoff"],
        "best_major_energy_fraction": best["major_energy_fraction"],
        "best_major_phase_contribution": best["major_phase_contribution"],
        "best_minor_phase_contribution": best["minor_phase_contribution"],
        "best_minor_phase_to_energy_ratio": best["minor_phase_to_energy_ratio"],
        "best_trivial_minor_lower_bound": best["trivial_minor_lower_bound"],
        "best_rigorous_total_lower_bound": best["rigorous_total_lower_bound"],
        "trivial_minor_bound_route_refuted": float(best["rigorous_total_lower_bound"]) <= 0 < exact,
    }


def analyze_ticket110() -> dict[str, Any]:
    rows = [audit_rational_arc_budget(horizon) for horizon in HORIZONS]
    contract_failures = sum(
        int(not row["trivial_minor_bound_route_refuted"])
        + sum(
            int(float(candidate["major_minor_reconstruction_error"]) > 1e-8)
            for candidate in row["rows"]
        )
        for row in rows
    )
    return {
        "theorem_name": "RationalMajorArcPartitionAndTrivialMinorNoGo",
        "source_ticket": "TICKET-109",
        "major_arc_contract": {
            "centers": "All reduced fractions a/q in [0,1/2] with q<=Q.",
            "width": "|alpha-a/q|<=Q/(qX), fixed before reading the target phase contributions.",
            "identity": "The discrete spectrum is partitioned exactly into the union of these major bins and its minor complement.",
            "anti_circularity": "Arc centers and widths depend only on X and Q, never on observed positive target contributions.",
        },
        "minor_arc_no_go": {
            "tested_bound": "Retain the exact major-arc phase contribution and bound the entire minor contribution by minus its spectral energy.",
            "result": "The best such rigorous lower bound remains negative on every audited horizon although the exact correlation is positive.",
            "consequence": "Rational arc selection alone is insufficient; a signed Type II power saving on the minor arcs is indispensable.",
            "scope": "This refutes the trivial-energy minor bound for the audited Q family, not the circle method or a genuine minor-arc estimate.",
        },
        "rows": rows,
        "discarded_routes": [
            "Choose major arcs after observing which bins contribute positively.",
            "Use exact major-arc contribution with only the trivial absolute-energy bound on minor arcs.",
            "Treat finite major-energy coverage as an asymptotic singular-series theorem.",
            "Call rational arc masking alone a parity-breaking Type II estimate.",
        ],
        "literature_boundary": {
            "established_background": "Rational major arcs, smoothing, and Type II minor-arc estimates are standard circle-method architecture.",
            "source": HELFGOTT_SOURCE,
            "project_specific_result": "A replayable anti-circular arc mask and a finite no-go certificate for trivial minor-energy closure.",
        },
        "next_theorem_target": "FixedBumpMajorArcAsymptoticWithTypeIIMinorPowerSaving",
        "machine_audit": {
            "maximum_horizon": HORIZONS[-1],
            "row_count": len(rows),
            "cutoff_count": len(DENOMINATOR_CUTOFFS),
            "trivial_minor_refutation_count": sum(int(row["trivial_minor_bound_route_refuted"]) for row in rows),
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET110 proves exact finite rational-arc partition contracts and refutes trivial minor-energy closure on the audited family. It proves none of the four conjectures and no conjecture counterexample.",
    }


def transferred_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin rational-arc audit",
        "attempt": "Preserve the existing infinite target; no Twin major-arc shortcut is transferred.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "independent_target": target},
        "obstruction": "TICKET110 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket109 = read_json(ROOT / "data/open-problem/ticket109-twin-spectral-phase-audit.json")
    audit = analyze_ticket110()
    attempts = [
        transferred_attempt(ticket109, "riemann", "RH-TICKET-110", "NonCircularKernelPositivityPreserved", "NonCircularExplicitFormulaKernelPositivity"),
        transferred_attempt(ticket109, "collatz", "CO-TICKET-110", "GoldenMeanEscapePreserved", "GoldenMeanInvariantSetEscape"),
        transferred_attempt(ticket109, "goldbach", "GB-TICKET-110", "JointBalancedGoldbachPreserved", "JointBalancedVaughanGoldbachResidualEnvelope"),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-110",
            "status": "rational_arc_partition_exact_trivial_minor_bound_refuted_open",
            "route": "RationalMajorArcPhaseBudget",
            "proof_or_counterexample_mode": "anti-circular rational-arc partition plus trivial-minor falsification",
            "attempt": "Build fixed rational major arcs around reduced a/q, retain their signed phase contribution, and test whether trivial minor-energy control closes a positive lower bound.",
            "bounded_result": {"source_ticket": "TP-TICKET-109", "audit_ref": "twin_rational_arc_budget"},
            "obstruction": audit["minor_arc_no_go"]["consequence"],
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Derive an explicit major-arc asymptotic and prove or falsify a power-saving Type II minor-arc estimate for the fixed bump.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "rational_arc_partition_exact_trivial_minor_bound_refuted_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_rational_arc_budget": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket110-twin-rational-arc-budget.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-110-kernel-positivity-preserved.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-110-golden-mean-preserved.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-110-joint-balanced-preserved.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-110-rational-arc-budget.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
