from __future__ import annotations

from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import prime_sieve, von_mangoldt_values
from ticket95_sharp_contamination_and_equivalence_audit import (
    proper_prime_power_mass_prefix,
    sharp_goldbach_contamination_bound,
    sharp_twin_contamination_bound,
)


GENERATED_AT = "2026-07-13T00:05:00+09:00"
SCHEMA = "primeproject.ticket97-periodic-projection-residual-audit.v1"
CHECKPOINTS = (10_000, 100_000)
MODULI = (2, 6, 30, 210, 2_310)


def optimal_periodic_projection(values: np.ndarray, modulus: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    residues = np.arange(len(values)) % modulus
    counts = np.bincount(residues, minlength=modulus)
    sums = np.bincount(residues, weights=values, minlength=modulus)
    means = sums / counts
    projection = means[residues]
    return projection, values - projection, means


def additive_coefficient(left: np.ndarray, right: np.ndarray, target: int) -> float:
    return float(np.dot(left[: target + 1], right[target::-1]))


def shift_two_coefficient(left: np.ndarray, right: np.ndarray, target: int) -> float:
    return float(np.dot(left[: target + 1], right[2 : target + 3]))


def audit_zero_residue_mean_countermodel() -> dict[str, Any]:
    residual = np.array([1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, 1.0])
    modulus = 2
    residue_sums = [float(residual[residue::modulus].sum()) for residue in range(modulus)]
    goldbach_target = 3
    goldbach_coefficient = additive_coefficient(residual, residual, goldbach_target)
    twin_coefficient = shift_two_coefficient(residual, residual, 5)
    failures = (
        sum(int(abs(value) > 1e-12) for value in residue_sums)
        + int(goldbach_coefficient >= 0)
        + int(twin_coefficient >= 0)
    )
    return {
        "modulus": modulus,
        "residual_sequence": residual.tolist(),
        "residue_sums": residue_sums,
        "goldbach_target": goldbach_target,
        "goldbach_additive_coefficient": goldbach_coefficient,
        "twin_shift_two_coefficient": twin_coefficient,
        "energy": float(np.dot(residual, residual)),
        "failure_count": failures,
        "scope": "The sequence is a signed real residual countermodel, not a von Mangoldt or prime sequence.",
    }


def _checkpoint_audit(
    target: int,
    is_prime: bytearray,
    mangoldt: dict[int, float],
    mass_prefix: list[float],
) -> dict[str, Any]:
    values = np.zeros(target + 3, dtype=np.float64)
    for value, weight in mangoldt.items():
        if value <= target + 2:
            values[value] = weight
    exact_energy = float(np.dot(values, values))
    exact_goldbach = additive_coefficient(values, values, target)
    exact_twin = shift_two_coefficient(values, values, target)
    goldbach_budget = sharp_goldbach_contamination_bound(target, mass_prefix)
    twin_budget = sharp_twin_contamination_bound(target, mass_prefix)
    rows: list[dict[str, Any]] = []

    for modulus in MODULI:
        projection, residual, means = optimal_periodic_projection(values, modulus)
        residues = np.arange(len(values)) % modulus
        residue_residual_sums = np.bincount(residues, weights=residual, minlength=modulus)
        projection_energy = float(np.dot(projection, projection))
        residual_energy = float(np.dot(residual, residual))
        orthogonality = float(np.dot(projection, residual))

        goldbach_main = additive_coefficient(projection, projection, target)
        goldbach_cross_left = additive_coefficient(projection, residual, target)
        goldbach_cross_right = additive_coefficient(residual, projection, target)
        goldbach_residual = additive_coefficient(residual, residual, target)
        goldbach_reconstructed = goldbach_main + goldbach_cross_left + goldbach_cross_right + goldbach_residual
        projection_goldbach_norm = float(np.linalg.norm(projection[: target + 1]))
        residual_goldbach_norm = float(np.linalg.norm(residual[: target + 1]))
        goldbach_norm_lower = (
            goldbach_main
            - 2 * projection_goldbach_norm * residual_goldbach_norm
            - residual_goldbach_norm * residual_goldbach_norm
        )

        twin_main = shift_two_coefficient(projection, projection, target)
        twin_cross_left = shift_two_coefficient(projection, residual, target)
        twin_cross_right = shift_two_coefficient(residual, projection, target)
        twin_residual = shift_two_coefficient(residual, residual, target)
        twin_reconstructed = twin_main + twin_cross_left + twin_cross_right + twin_residual
        p_left = float(np.linalg.norm(projection[: target + 1]))
        p_right = float(np.linalg.norm(projection[2 : target + 3]))
        e_left = float(np.linalg.norm(residual[: target + 1]))
        e_right = float(np.linalg.norm(residual[2 : target + 3]))
        twin_norm_lower = twin_main - p_left * e_right - e_left * p_right - e_left * e_right

        rows.append(
            {
                "modulus": modulus,
                "residue_mean_count": len(means),
                "maximum_absolute_residue_residual_sum": float(np.max(np.abs(residue_residual_sums))),
                "orthogonality_error": abs(orthogonality),
                "energy_decomposition_error": abs(exact_energy - projection_energy - residual_energy),
                "relative_residual_norm": (residual_energy / exact_energy) ** 0.5,
                "goldbach_periodic_main": goldbach_main,
                "goldbach_signed_cross": goldbach_cross_left + goldbach_cross_right,
                "goldbach_signed_residual": goldbach_residual,
                "goldbach_reconstruction_error": abs(exact_goldbach - goldbach_reconstructed),
                "goldbach_norm_only_lower_bound": goldbach_norm_lower,
                "goldbach_sharp_budget": goldbach_budget,
                "goldbach_certified": goldbach_norm_lower > goldbach_budget,
                "twin_periodic_main": twin_main,
                "twin_signed_cross": twin_cross_left + twin_cross_right,
                "twin_signed_residual": twin_residual,
                "twin_reconstruction_error": abs(exact_twin - twin_reconstructed),
                "twin_norm_only_lower_bound": twin_norm_lower,
                "twin_sharp_budget": twin_budget,
                "twin_certified": twin_norm_lower > twin_budget,
            }
        )

    return {
        "target": target,
        "exact_goldbach_correlation": exact_goldbach,
        "exact_twin_correlation": exact_twin,
        "goldbach_sharp_budget": goldbach_budget,
        "twin_sharp_budget": twin_budget,
        "modulus_count": len(rows),
        "goldbach_certificate_count": sum(int(bool(row["goldbach_certified"])) for row in rows),
        "twin_certificate_count": sum(int(bool(row["twin_certified"])) for row in rows),
        "rows": rows,
    }


def analyze_periodic_projection_residuals(
    checkpoints: tuple[int, ...] = CHECKPOINTS,
) -> dict[str, Any]:
    maximum = max(checkpoints)
    is_prime, primes = prime_sieve(maximum + 2)
    mangoldt = von_mangoldt_values(maximum + 2, primes)
    mass_prefix = proper_prime_power_mass_prefix(maximum + 2, is_prime, mangoldt)
    checkpoints_rows = [_checkpoint_audit(target, is_prime, mangoldt, mass_prefix) for target in checkpoints]
    countermodel = audit_zero_residue_mean_countermodel()
    projection_failures = 0
    for checkpoint in checkpoints_rows:
        for row in checkpoint["rows"]:
            projection_failures += int(float(row["maximum_absolute_residue_residual_sum"]) > 1e-6)
            projection_failures += int(float(row["orthogonality_error"]) > 1e-6)
            projection_failures += int(float(row["energy_decomposition_error"]) > 1e-6)
            projection_failures += int(float(row["goldbach_reconstruction_error"]) > 1e-6)
            projection_failures += int(float(row["twin_reconstruction_error"]) > 1e-6)
    goldbach_certificates = sum(int(row["goldbach_certificate_count"]) for row in checkpoints_rows)
    twin_certificates = sum(int(row["twin_certificate_count"]) for row in checkpoints_rows)
    total_failures = projection_failures + int(countermodel["failure_count"])
    return {
        "theorem_name": "OptimalFiniteModulusProjectionAndResidualSignNoGoAudit",
        "source_ticket": "TICKET-96",
        "projection_theorem": {
            "definition": "P_W Lambda(n) is the mean of Lambda over the audited interval in the residue class n mod W.",
            "optimality": "P_W is the unique L2 minimizer among W-periodic functions on the finite interval.",
            "orthogonality": "E_W=Lambda-P_W Lambda has zero sum in every residue class and is orthogonal to every W-periodic function.",
            "exact_split": "Both additive and shift-two correlations split exactly into periodic main, two signed cross terms, and a signed residual correlation.",
        },
        "fixed_modulus_no_go": {
            "finding": "Every tested L2-optimal periodic projection reconstructs the exact correlation, but its separate norm-only lower bound remains negative and certifies neither sharp budget.",
            "countermodel": "A signed length-eight residual has zero mean in both mod-2 classes while its Goldbach-type coefficient is -4 and shift-two coefficient is -2.",
            "logical_scope": "Residue-class means alone do not determine binary correlation signs, even when all fixed-modulus one-point constraints are exact.",
            "consequence": "A useful proof needs growing-modulus uniformity plus signed bilinear or higher-order control of the residual.",
        },
        "countermodel_audit": countermodel,
        "machine_audit": {
            "checkpoint_count": len(checkpoints_rows),
            "maximum_checkpoint": maximum,
            "moduli": list(MODULI),
            "modulus_count_per_checkpoint": len(MODULI),
            "goldbach_certificate_count": goldbach_certificates,
            "twin_certificate_count": twin_certificates,
            "projection_failure_count": projection_failures,
            "countermodel_failure_count": countermodel["failure_count"],
            "total_failure_count": total_failures,
            "checkpoint_rows": checkpoints_rows,
        },
        "theorem_status": "optimal_periodic_projection_and_fixed_modulus_sign_no_go_proved_no_resolution" if total_failures == 0 else "ticket97_periodic_projection_audit_inconclusive_no_resolution",
        "discarded_routes": [
            "Treat exact fixed-modulus residue means as if they determined binary prime correlations.",
            "Use L2 optimality of the periodic model as a one-sided correlation estimate.",
            "Promote data-fitted finite residue means to an all-scale arithmetic theorem.",
        ],
        "goldbach_next_theorem_target": "GrowingModulusBinaryResidualCancellation",
        "twin_next_theorem_target": "GrowingModulusShiftTwoResidualCancellation",
        "retained_route": "Let W grow with scale under independently proved distribution estimates, and control the signed residual correlation by Type II or higher-order uniformity rather than separate norms.",
        "proof_boundary": "TICKET97 proves finite projection optimality checks and a fixed-modulus information no-go. It does not prove growing-modulus residual cancellation, Goldbach, or Twin Prime.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "finite_modulus_information_gate_open",
        "route": route,
        "proof_or_counterexample_mode": "optimal periodic projection and residual-sign countermodel transfer",
        "attempt": "Project onto exact finite residue-class information and test whether the orthogonal residual can still reverse the target sign.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket97_transfer": route, "independent_target": target},
        "obstruction": "No target-specific growing-modulus residual theorem was proved in TICKET97.",
        "candidate_theorem": target,
        "next_experiment": "Specify a scale-dependent modulus and falsify the proposed residual bound against zero-mean signed countermodels.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket96 = read_json(ROOT / "data/open-problem/ticket96-fourier-phase-information-audit.json")
    audit = analyze_periodic_projection_residuals()
    attempts = [
        transfer_attempt(ticket96, "riemann", "RH-TICKET-97", "FiniteModulusKernelProjectionGate", "GrowingConductorKernelResidualControl"),
        transfer_attempt(ticket96, "collatz", "CO-TICKET-97", "FiniteResidueOrbitProjectionGate", "GrowingResidueNaturalOrbitResidualControl"),
        {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-97",
            "route": "OptimalFiniteModulusGoldbachProjectionAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "L2-optimal residue projection plus signed residual countermodel",
            "attempt": "Add exact finite-modulus arithmetic structure to TICKET96 and test whether it determines the binary additive sign.",
            "bounded_result": {"source_ticket": "GB-TICKET-96", "audit_ref": "periodic_projection_residual_audit"},
            "obstruction": audit["retained_route"],
            "candidate_theorem": audit["goldbach_next_theorem_target"],
            "next_experiment": "Test a growing primorial projection with independently sourced progression-error budgets and signed residual convolution bounds.",
            "claim_boundary": "No Goldbach proof and no certified Goldbach counterexample.",
        },
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-97",
            "route": "OptimalFiniteModulusTwinProjectionAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "L2-optimal residue projection plus shift-two residual countermodel",
            "attempt": "Add exact finite-modulus arithmetic structure to TICKET96 and test whether it determines the shift-two sign.",
            "bounded_result": {"source_ticket": "TP-TICKET-96", "audit_ref": "periodic_projection_residual_audit"},
            "obstruction": audit["retained_route"],
            "candidate_theorem": audit["twin_next_theorem_target"],
            "next_experiment": "Test growing-modulus Type II constraints against zero-residue-mean shift-two countermodels.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "optimal_periodic_projection_fixed_modulus_routes_blocked_no_resolution",
        "claim_boundary": "TICKET97 proves finite L2 projection contracts and fixed-modulus information no-go results. It solves none of the four open problems.",
        "periodic_projection_residual_audit": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket97-periodic-projection-residual-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-97-finite-modulus-gate.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-97-finite-residue-gate.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-97-periodic-projection.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-97-periodic-projection.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
