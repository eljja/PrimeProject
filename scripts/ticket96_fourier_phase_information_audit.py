from __future__ import annotations

import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import prime_sieve, von_mangoldt_values
from ticket94_signed_remainder_and_goldbach_bridge import goldbach_row
from ticket95_sharp_contamination_and_equivalence_audit import (
    proper_prime_power_mass_prefix,
    sharp_goldbach_contamination_bound,
    sharp_twin_contamination_bound,
)


GENERATED_AT = "2026-07-12T22:10:00+09:00"
SCHEMA = "primeproject.ticket96-fourier-phase-information-audit.v1"
CHECKPOINTS = (10_000, 100_000)
DENOMINATOR_LIMITS = (2, 4, 8, 16, 32, 64)
HALF_WIDTH_BINS = (1, 2, 4, 8, 16, 32)
SPARSE_MASK_DENSITY = 0.10


def next_power_of_two_above(value: int) -> int:
    result = 1
    while result <= value:
        result *= 2
    return result


def farey_major_mask(transform_size: int, denominator_limit: int, half_width_bins: int) -> np.ndarray:
    mask = np.zeros(transform_size, dtype=np.bool_)
    for denominator in range(1, denominator_limit + 1):
        for numerator in range(denominator):
            if math.gcd(numerator, denominator) != 1:
                continue
            center = int(round(transform_size * numerator / denominator)) % transform_size
            for offset in range(-half_width_bins, half_width_bins + 1):
                mask[(center + offset) % transform_size] = True
    return mask


def _checkpoint_fourier_audit(
    target: int,
    is_prime: bytearray,
    mangoldt: dict[int, float],
    mass_prefix: list[float],
) -> dict[str, Any]:
    transform_size = next_power_of_two_above(2 * (target + 2))
    weights = np.zeros(transform_size, dtype=np.float64)
    for value, weight in mangoldt.items():
        if value <= target + 2:
            weights[value] = weight
    transform = np.fft.fft(weights)
    frequencies = np.arange(transform_size, dtype=np.float64)
    goldbach_terms = transform * transform * np.exp(2j * np.pi * frequencies * target / transform_size) / transform_size
    twin_terms = np.abs(transform) ** 2 * np.exp(2j * np.pi * frequencies * 2 / transform_size) / transform_size

    exact_goldbach = float(goldbach_terms.sum().real)
    exact_twin = float(twin_terms.sum().real)
    direct_goldbach = float(goldbach_row(target, is_prime, mangoldt)["lambda_additive_correlation"])
    direct_twin = sum(mangoldt.get(value, 0.0) * mangoldt.get(value + 2, 0.0) for value in range(2, target + 1))
    goldbach_budget = sharp_goldbach_contamination_bound(target, mass_prefix)
    twin_budget = sharp_twin_contamination_bound(target, mass_prefix)
    rows: list[dict[str, Any]] = []

    for denominator_limit in DENOMINATOR_LIMITS:
        for half_width in HALF_WIDTH_BINS:
            mask = farey_major_mask(transform_size, denominator_limit, half_width)
            minor_mask = ~mask
            minor_energy = float((np.abs(transform[minor_mask]) ** 2).sum() / transform_size)
            goldbach_major = float(goldbach_terms[mask].sum().real)
            goldbach_minor = float(goldbach_terms[minor_mask].sum().real)
            twin_major = float(twin_terms[mask].sum().real)
            twin_minor = float(twin_terms[minor_mask].sum().real)
            goldbach_lower = goldbach_major - minor_energy
            twin_lower = twin_major - minor_energy
            rows.append(
                {
                    "denominator_limit": denominator_limit,
                    "half_width_bins": half_width,
                    "major_bin_count": int(mask.sum()),
                    "major_density": float(mask.mean()),
                    "minor_energy": minor_energy,
                    "goldbach_major_real": goldbach_major,
                    "goldbach_minor_signed_real": goldbach_minor,
                    "goldbach_energy_only_lower_bound": goldbach_lower,
                    "goldbach_sharp_budget": goldbach_budget,
                    "goldbach_certified": goldbach_lower > goldbach_budget,
                    "goldbach_reconstruction_error": abs(exact_goldbach - goldbach_major - goldbach_minor),
                    "twin_major_real": twin_major,
                    "twin_minor_signed_real": twin_minor,
                    "twin_energy_only_lower_bound": twin_lower,
                    "twin_sharp_budget": twin_budget,
                    "twin_certified": twin_lower > twin_budget,
                    "twin_reconstruction_error": abs(exact_twin - twin_major - twin_minor),
                }
            )

    sparse_rows = [row for row in rows if float(row["major_density"]) <= SPARSE_MASK_DENSITY]
    best_goldbach = max(sparse_rows, key=lambda row: float(row["goldbach_energy_only_lower_bound"]) - goldbach_budget)
    best_twin = max(sparse_rows, key=lambda row: float(row["twin_energy_only_lower_bound"]) - twin_budget)
    return {
        "target": target,
        "transform_size": transform_size,
        "exact_goldbach_correlation": exact_goldbach,
        "direct_goldbach_correlation": direct_goldbach,
        "goldbach_dft_error": abs(exact_goldbach - direct_goldbach),
        "exact_twin_correlation": exact_twin,
        "direct_twin_correlation": direct_twin,
        "twin_dft_error": abs(exact_twin - direct_twin),
        "goldbach_sharp_budget": goldbach_budget,
        "twin_sharp_budget": twin_budget,
        "configuration_count": len(rows),
        "sparse_configuration_count": len(sparse_rows),
        "sparse_goldbach_certificate_count": sum(int(bool(row["goldbach_certified"])) for row in sparse_rows),
        "sparse_twin_certificate_count": sum(int(bool(row["twin_certified"])) for row in sparse_rows),
        "best_sparse_goldbach_row": best_goldbach,
        "best_sparse_twin_row": best_twin,
        "rows": rows,
    }


def audit_adversarial_spectral_countermodels() -> dict[str, Any]:
    transform_size = 64
    amplitude = 3.0
    goldbach_target = 10
    goldbach_frequency = 7
    phase = (math.pi - 2 * math.pi * goldbach_frequency * goldbach_target / transform_size) / 2
    positive_frequency = amplitude * np.exp(1j * phase)
    negative_frequency = np.conjugate(positive_frequency)
    goldbach_pair_coefficient = float(
        (
            positive_frequency**2 * np.exp(2j * math.pi * goldbach_frequency * goldbach_target / transform_size)
            + negative_frequency**2 * np.exp(-2j * math.pi * goldbach_frequency * goldbach_target / transform_size)
        ).real
        / transform_size
    )
    goldbach_pair_energy = 2 * amplitude * amplitude / transform_size

    twin_shift = 2
    twin_frequency = transform_size // 4
    twin_pair_coefficient = float(
        (
            amplitude**2 * np.exp(2j * math.pi * twin_frequency * twin_shift / transform_size)
            + amplitude**2 * np.exp(-2j * math.pi * twin_frequency * twin_shift / transform_size)
        ).real
        / transform_size
    )
    twin_pair_energy = 2 * amplitude * amplitude / transform_size
    goldbach_error = abs(goldbach_pair_coefficient + goldbach_pair_energy)
    twin_error = abs(twin_pair_coefficient + twin_pair_energy)
    return {
        "transform_size": transform_size,
        "amplitude": amplitude,
        "goldbach": {
            "target": goldbach_target,
            "frequency_pair": [goldbach_frequency, transform_size - goldbach_frequency],
            "conjugate_symmetric": True,
            "pair_energy": goldbach_pair_energy,
            "target_coefficient": goldbach_pair_coefficient,
            "negative_energy_envelope_error": goldbach_error,
        },
        "twin": {
            "shift": twin_shift,
            "frequency_pair": [twin_frequency, transform_size - twin_frequency],
            "conjugate_symmetric": True,
            "pair_energy": twin_pair_energy,
            "target_coefficient": twin_pair_coefficient,
            "negative_energy_envelope_error": twin_error,
        },
        "failure_count": int(goldbach_error > 1e-12) + int(twin_error > 1e-12),
        "scope": "The inverse DFT is real because the spectra are conjugate symmetric; no nonnegativity or prime support is claimed.",
    }


def analyze_fourier_phase_information(
    checkpoints: tuple[int, ...] = CHECKPOINTS,
) -> dict[str, Any]:
    maximum = max(checkpoints)
    is_prime, primes = prime_sieve(maximum + 2)
    mangoldt = von_mangoldt_values(maximum + 2, primes)
    mass_prefix = proper_prime_power_mass_prefix(maximum + 2, is_prime, mangoldt)
    rows = [_checkpoint_fourier_audit(target, is_prime, mangoldt, mass_prefix) for target in checkpoints]
    reconstruction_failures = sum(
        int(float(row["goldbach_dft_error"]) > 1e-6)
        + int(float(row["twin_dft_error"]) > 1e-6)
        + sum(
            int(float(config["goldbach_reconstruction_error"]) > 1e-6)
            + int(float(config["twin_reconstruction_error"]) > 1e-6)
            for config in row["rows"]
        )
        for row in rows
    )
    sparse_goldbach_certificates = sum(int(row["sparse_goldbach_certificate_count"]) for row in rows)
    sparse_twin_certificates = sum(int(row["sparse_twin_certificate_count"]) for row in rows)
    countermodels = audit_adversarial_spectral_countermodels()
    total_failures = reconstruction_failures + int(countermodels["failure_count"])
    return {
        "theorem_name": "DiscreteFourierPhaseInformationAndEnergyOnlyNoGoAudit",
        "source_ticket": "TICKET-95",
        "exact_fourier_bridges": {
            "goldbach": "G(N) is the N-th coefficient of F(z)^2 and equals the exact M-point inverse DFT when M>2(N+2).",
            "twin": "C_2(x) is the shift-two coefficient of |F|^2 and equals the exact M-point inverse DFT after zero padding.",
            "split": "For any frequency mask, target coefficient = major signed contribution + minor signed contribution.",
            "energy_bound": "The phase-blind inequality uses |minor signed contribution|<=minor Parseval energy.",
        },
        "information_no_go": {
            "goldbach_countermodel": "Keeping every minor magnitude |F_k| fixed, conjugate-symmetric phases can align F_k^2 exp(2 pi i kN/M) negatively, attaining the energy lower envelope in the unrestricted real-sequence class.",
            "twin_countermodel": "Knowing only total minor energy permits conjugate-symmetric energy concentration near frequencies with cos(4 pi k/M)=-1, attaining a negative shift-two coefficient.",
            "scope": "These are information-theoretic countermodels for phase-blind premises, not counterexamples made from primes.",
            "consequence": "A proof must add arithmetic phase rigidity, frequency localization, or signed Type II cancellation; total energy alone cannot do so.",
        },
        "countermodel_audit": countermodels,
        "machine_audit": {
            "checkpoint_count": len(rows),
            "maximum_checkpoint": maximum,
            "configuration_count_per_checkpoint": len(DENOMINATOR_LIMITS) * len(HALF_WIDTH_BINS),
            "sparse_mask_density_ceiling": SPARSE_MASK_DENSITY,
            "sparse_goldbach_certificate_count": sparse_goldbach_certificates,
            "sparse_twin_certificate_count": sparse_twin_certificates,
            "reconstruction_failure_count": reconstruction_failures,
            "countermodel_failure_count": countermodels["failure_count"],
            "total_failure_count": total_failures,
            "checkpoint_rows": rows,
        },
        "theorem_status": "exact_dft_bridges_and_phase_blind_information_no_go_proved_no_open_problem_resolution" if total_failures == 0 else "ticket96_fourier_audit_inconclusive_no_resolution",
        "discarded_routes": [
            "Use total minor Parseval energy as if it contained signed cancellation.",
            "Treat a data-dependent dense frequency mask as an asymptotic major-arc theorem.",
            "Count exact DFT reconstruction from sampled primes as an independent lower bound.",
        ],
        "retained_goldbach_route": "Prove arithmetic phase cancellation on the binary minor arcs strong enough that major_real-|minor_signed| exceeds 2 log(N)H(N) uniformly.",
        "retained_twin_route": "Prove signed shift-two Type II cancellation or spectral localization that excludes adversarial energy placement.",
        "goldbach_next_theorem_target": "ArithmeticMinorArcPhaseCancellation",
        "twin_next_theorem_target": "ShiftTwoSpectralLocalizationOrTypeIICancellation",
        "proof_boundary": "TICKET96 proves exact finite Fourier identities and phase-blind information no-go statements. It does not prove a prime-specific phase theorem, Goldbach, or Twin Prime.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "spectral_independent_information_gate_open",
        "route": route,
        "proof_or_counterexample_mode": "phase-blind countermodel transfer discipline",
        "attempt": "Test whether norm or energy data can determine the required signed coefficient; reject the route when an adversarial phase or frequency placement preserves the premise.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket96_transfer": route, "independent_target": target},
        "obstruction": "No target-specific arithmetic phase-rigidity theorem was proved in TICKET96.",
        "candidate_theorem": target,
        "next_experiment": "Construct a target-specific signed spectral observable and search for a countermodel preserving all proposed premises.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket95 = read_json(ROOT / "data/open-problem/ticket95-sharp-contamination-and-equivalence-audit.json")
    audit = analyze_fourier_phase_information()
    attempts = [
        transfer_attempt(ticket95, "riemann", "RH-TICKET-96", "ExplicitFormulaSpectralPhaseGate", "ArithmeticKernelPhaseRigidity"),
        transfer_attempt(ticket95, "collatz", "CO-TICKET-96", "TransitionSpectrumPlacementGate", "NaturalOrbitSpectralPlacementConstraint"),
        {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-96",
            "route": "BinaryGoldbachFourierPhaseInformationAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "exact DFT split plus adversarial phase countermodel",
            "attempt": "Test whether the sharp TICKET95 budget can be closed by a Farey major mask and phase-blind minor Parseval energy.",
            "bounded_result": {"source_ticket": "GB-TICKET-95", "audit_ref": "fourier_phase_information_audit"},
            "obstruction": audit["retained_goldbach_route"],
            "candidate_theorem": audit["goldbach_next_theorem_target"],
            "next_experiment": "Introduce arithmetic phase constraints from Vaughan-type bilinear decompositions and test the resulting signed minor-arc budget.",
            "claim_boundary": "No Goldbach proof and no certified Goldbach counterexample.",
        },
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-96",
            "route": "TwinShiftTwoFourierEnergyPlacementAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "exact DFT split plus adversarial frequency-placement countermodel",
            "attempt": "Test whether the sharp TICKET95 budget can be closed by a Farey major mask and phase-blind minor Parseval energy.",
            "bounded_result": {"source_ticket": "TP-TICKET-95", "audit_ref": "fourier_phase_information_audit"},
            "obstruction": audit["retained_twin_route"],
            "candidate_theorem": audit["twin_next_theorem_target"],
            "next_experiment": "Introduce signed Type II localization constraints and reject any model that can concentrate minor energy at negative shift-two frequencies.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "exact_fourier_bridges_phase_blind_routes_blocked_no_resolution",
        "claim_boundary": "TICKET96 proves exact finite Fourier bridges and information-theoretic no-go results for phase-blind premises. It solves none of the four open problems.",
        "fourier_phase_information_audit": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket96-fourier-phase-information-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-96-spectral-phase-gate.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-96-spectrum-placement-gate.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-96-fourier-phase-audit.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-96-fourier-energy-audit.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
