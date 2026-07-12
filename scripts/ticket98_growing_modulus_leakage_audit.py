from __future__ import annotations

import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import prime_sieve, von_mangoldt_values
from ticket95_sharp_contamination_and_equivalence_audit import (
    proper_prime_power_mass_prefix,
    sharp_goldbach_contamination_bound,
    sharp_twin_contamination_bound,
)
from ticket97_periodic_projection_residual_audit import (
    additive_coefficient,
    optimal_periodic_projection,
    shift_two_coefficient,
)


GENERATED_AT = "2026-07-13T01:20:00+09:00"
SCHEMA = "primeproject.ticket98-growing-modulus-leakage-audit.v1"
CHECKPOINTS = (10_000, 100_000, 1_000_000)
PRIMORIAL_MODULI = (2, 6, 30, 210, 2_310, 30_030, 510_510, 9_699_690)


def occupancy_summary(domain_length: int, modulus: int) -> dict[str, Any]:
    occupied = min(domain_length, modulus)
    quotient, remainder = divmod(domain_length, modulus)
    if modulus >= domain_length:
        singleton_residues = domain_length
        maximum = 1
        minimum = 1
    else:
        singleton_residues = modulus - remainder if quotient == 1 else 0
        maximum = quotient + int(remainder > 0)
        minimum = quotient
    return {
        "domain_length": domain_length,
        "occupied_residue_count": occupied,
        "average_samples_per_occupied_residue": domain_length / occupied,
        "minimum_samples_per_occupied_residue": minimum,
        "maximum_samples_per_occupied_residue": maximum,
        "singleton_residue_count": singleton_residues,
        "singleton_observation_fraction": singleton_residues / domain_length,
        "row_unique_leakage": modulus >= domain_length,
        "at_most_two_samples_per_residue": maximum <= 2,
    }


def _checkpoint_audit(
    target: int,
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

    for modulus in PRIMORIAL_MODULI:
        occupancy = occupancy_summary(len(values), modulus)
        if occupancy["row_unique_leakage"]:
            projection = values.copy()
            residual = np.zeros_like(values)
            maximum_residue_error = 0.0
        else:
            projection, residual, _ = optimal_periodic_projection(values, modulus)
            residues = np.arange(len(values)) % modulus
            residue_errors = np.bincount(residues, weights=residual, minlength=modulus)
            maximum_residue_error = float(np.max(np.abs(residue_errors)))

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
        projection_left_norm = float(np.linalg.norm(projection[: target + 1]))
        projection_right_norm = float(np.linalg.norm(projection[2 : target + 3]))
        residual_left_norm = float(np.linalg.norm(residual[: target + 1]))
        residual_right_norm = float(np.linalg.norm(residual[2 : target + 3]))
        twin_norm_lower = (
            twin_main
            - projection_left_norm * residual_right_norm
            - residual_left_norm * projection_right_norm
            - residual_left_norm * residual_right_norm
        )

        scale = max(1.0, exact_energy)
        row = {
            "modulus": modulus,
            **occupancy,
            "maximum_absolute_residue_residual_sum": maximum_residue_error,
            "relative_orthogonality_error": abs(orthogonality) / scale,
            "relative_energy_decomposition_error": abs(exact_energy - projection_energy - residual_energy) / scale,
            "relative_residual_norm": math.sqrt(residual_energy / exact_energy),
            "goldbach_norm_only_lower_bound": goldbach_norm_lower,
            "goldbach_sharp_budget": goldbach_budget,
            "goldbach_certified": goldbach_norm_lower > goldbach_budget,
            "goldbach_reconstruction_relative_error": abs(exact_goldbach - goldbach_reconstructed) / max(1.0, abs(exact_goldbach)),
            "twin_norm_only_lower_bound": twin_norm_lower,
            "twin_sharp_budget": twin_budget,
            "twin_certified": twin_norm_lower > twin_budget,
            "twin_reconstruction_relative_error": abs(exact_twin - twin_reconstructed) / max(1.0, abs(exact_twin)),
            "certificate_interpretation": (
                "exact_data_replay_not_independent_arithmetic_bound"
                if occupancy["row_unique_leakage"]
                else "non_row_unique_projection_test"
            ),
        }
        rows.append(row)

    first_goldbach = next((row for row in rows if row["goldbach_certified"]), None)
    first_twin = next((row for row in rows if row["twin_certified"]), None)
    first_row_unique = next((row for row in rows if row["row_unique_leakage"]), None)
    return {
        "target": target,
        "domain_length": len(values),
        "exact_goldbach_correlation": exact_goldbach,
        "exact_twin_correlation": exact_twin,
        "goldbach_sharp_budget": goldbach_budget,
        "twin_sharp_budget": twin_budget,
        "first_goldbach_certificate_modulus": first_goldbach["modulus"] if first_goldbach else None,
        "first_twin_certificate_modulus": first_twin["modulus"] if first_twin else None,
        "first_row_unique_modulus": first_row_unique["modulus"] if first_row_unique else None,
        "goldbach_first_certificate_is_row_unique": bool(first_goldbach and first_goldbach["row_unique_leakage"]),
        "twin_first_certificate_is_row_unique": bool(first_twin and first_twin["row_unique_leakage"]),
        "non_row_unique_goldbach_certificate_count": sum(
            int(row["goldbach_certified"] and not row["row_unique_leakage"]) for row in rows
        ),
        "non_row_unique_twin_certificate_count": sum(
            int(row["twin_certified"] and not row["row_unique_leakage"]) for row in rows
        ),
        "rows": rows,
    }


def analyze_growing_modulus_leakage(
    checkpoints: tuple[int, ...] = CHECKPOINTS,
) -> dict[str, Any]:
    maximum = max(checkpoints)
    is_prime, primes = prime_sieve(maximum + 2)
    mangoldt = von_mangoldt_values(maximum + 2, primes)
    mass_prefix = proper_prime_power_mass_prefix(maximum + 2, is_prime, mangoldt)
    checkpoint_rows = [_checkpoint_audit(target, mangoldt, mass_prefix) for target in checkpoints]

    contract_failures = 0
    for checkpoint in checkpoint_rows:
        for row in checkpoint["rows"]:
            contract_failures += int(row["maximum_absolute_residue_residual_sum"] > 1e-6)
            contract_failures += int(row["relative_orthogonality_error"] > 1e-12)
            contract_failures += int(row["relative_energy_decomposition_error"] > 1e-12)
            contract_failures += int(row["goldbach_reconstruction_relative_error"] > 1e-12)
            contract_failures += int(row["twin_reconstruction_relative_error"] > 1e-12)
            if row["row_unique_leakage"]:
                contract_failures += int(row["relative_residual_norm"] != 0.0)

    non_row_unique_goldbach = sum(row["non_row_unique_goldbach_certificate_count"] for row in checkpoint_rows)
    non_row_unique_twin = sum(row["non_row_unique_twin_certificate_count"] for row in checkpoint_rows)
    first_certificate_mismatches = sum(
        int(row["first_goldbach_certificate_modulus"] != row["first_row_unique_modulus"])
        + int(row["first_twin_certificate_modulus"] != row["first_row_unique_modulus"])
        for row in checkpoint_rows
    )
    total_failures = contract_failures + first_certificate_mismatches
    return {
        "theorem_name": "GrowingModulusRowUniqueLeakageAudit",
        "source_ticket": "TICKET-97",
        "row_unique_identity_theorem": {
            "statement": "For a finite indexed dataset x on I={0,...,L-1}, if W>=L then n maps injectively to n mod W, so every occupied residue-class conditional mean equals x_n. Hence P_W x=x and E_W=x-P_W x=0.",
            "proof_steps": [
                "If 0<=m<n<L<=W, then 0<n-m<W, so W cannot divide n-m and m mod W differs from n mod W.",
                "Each occupied residue class therefore contains exactly one index.",
                "Its fitted conditional mean is that index's observed value, proving P_W x=x and E_W=0.",
                "Every norm-only correlation lower bound then equals the exact observed correlation; it contains no out-of-sample residual estimate.",
            ],
            "scope": "Exact finite-dimensional algebra for any real dataset; no prime-distribution assumption is used.",
        },
        "leakage_finding": {
            "finding": "Across the audited primorial chain, the first Goldbach and Twin certificates occur exactly at the first row-unique modulus for every checkpoint.",
            "interpretation": "The apparent certificate is exact target-data replay, not a growing-modulus arithmetic theorem.",
            "non_row_unique_result": "No tested non-row-unique projection certifies either sharp prime-power contamination budget, including W=510510 at N=1000000 where every occupied residue has at most two samples.",
            "logical_consequence": "A valid continuation must bound a projection chosen or estimated independently of the target correlation and retain many observations per arithmetic cell, or prove signed Type II/higher-order cancellation directly.",
        },
        "machine_audit": {
            "checkpoint_count": len(checkpoint_rows),
            "maximum_checkpoint": maximum,
            "primorial_moduli": list(PRIMORIAL_MODULI),
            "modulus_count_per_checkpoint": len(PRIMORIAL_MODULI),
            "non_row_unique_goldbach_certificate_count": non_row_unique_goldbach,
            "non_row_unique_twin_certificate_count": non_row_unique_twin,
            "row_unique_goldbach_certificate_count": sum(
                int(row["goldbach_first_certificate_is_row_unique"]) for row in checkpoint_rows
            ),
            "row_unique_twin_certificate_count": sum(
                int(row["twin_first_certificate_is_row_unique"]) for row in checkpoint_rows
            ),
            "first_certificate_mismatch_count": first_certificate_mismatches,
            "contract_failure_count": contract_failures,
            "total_failure_count": total_failures,
            "checkpoint_rows": checkpoint_rows,
        },
        "theorem_status": (
            "row_unique_leakage_theorem_proved_tested_growing_modulus_certificates_rejected_no_resolution"
            if total_failures == 0
            else "ticket98_growing_modulus_audit_inconclusive_no_resolution"
        ),
        "discarded_routes": [
            "Increase a data-fitted modulus until each observation receives its own residue class.",
            "Treat a zero residual caused by row uniqueness as independently proved cancellation.",
            "Promote endpoint-specific exact-correlation replay to a uniform all-scale theorem.",
        ],
        "goldbach_next_theorem_target": "OutOfSampleGrowingModulusBinaryResidualCancellation",
        "twin_next_theorem_target": "OutOfSampleGrowingModulusShiftTwoResidualCancellation",
        "retained_route": "Use sample splitting or an external progression theorem to choose and estimate P_W without target leakage, require a nondegenerate occupancy regime, and prove a signed binary residual estimate uniform in scale.",
        "proof_boundary": "TICKET98 proves a finite-data leakage theorem and audits three endpoint correlations. It does not prove Goldbach, Twin Prime, RH, Collatz, or a counterexample to any of them.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "growing_partition_leakage_gate_open",
        "route": route,
        "proof_or_counterexample_mode": "row-unique fitted-partition leakage theorem transfer",
        "attempt": "Reject scale-growing fitted partitions that become injective on the audited data before treating their zero residual as a theorem.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket98_transfer": route, "independent_target": target},
        "obstruction": "No target-specific out-of-sample growing-partition residual theorem was proved in TICKET98.",
        "candidate_theorem": target,
        "next_experiment": "Specify a nondegenerate occupancy regime and an independently estimated residual bound before computing the target statistic.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket97 = read_json(ROOT / "data/open-problem/ticket97-periodic-projection-residual-audit.json")
    audit = analyze_growing_modulus_leakage()
    attempts = [
        transfer_attempt(ticket97, "riemann", "RH-TICKET-98", "GrowingConductorPartitionLeakageGate", "ExternallyBoundedGrowingConductorKernelResidual"),
        transfer_attempt(ticket97, "collatz", "CO-TICKET-98", "GrowingResidueOrbitLeakageGate", "OutOfSampleGrowingResidueNaturalOrbitControl"),
        {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-98",
            "route": "GrowingModulusGoldbachLeakageAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "primorial occupancy audit plus row-unique identity theorem",
            "attempt": "Grow the TICKET97 modulus and test whether the first norm certificate precedes exact-data identification.",
            "bounded_result": {"source_ticket": "GB-TICKET-97", "audit_ref": "growing_modulus_leakage_audit"},
            "obstruction": audit["retained_route"],
            "candidate_theorem": audit["goldbach_next_theorem_target"],
            "next_experiment": "Cross-fit residue means on disjoint intervals and seek a uniform signed convolution residual theorem before evaluating even targets.",
            "claim_boundary": "No Goldbach proof and no certified Goldbach counterexample.",
        },
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-98",
            "route": "GrowingModulusTwinLeakageAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "primorial occupancy audit plus row-unique identity theorem",
            "attempt": "Grow the TICKET97 modulus and test whether the first shift-two norm certificate precedes exact-data identification.",
            "bounded_result": {"source_ticket": "TP-TICKET-97", "audit_ref": "growing_modulus_leakage_audit"},
            "obstruction": audit["retained_route"],
            "candidate_theorem": audit["twin_next_theorem_target"],
            "next_experiment": "Cross-fit residue means and prove an independent signed shift-two residual estimate uniform in scale.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "growing_modulus_certificates_rejected_as_row_unique_replay_no_resolution",
        "claim_boundary": "TICKET98 rejects fitted growing-modulus certificates that arise only after row uniqueness. It solves none of the four open problems.",
        "growing_modulus_leakage_audit": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket98-growing-modulus-leakage-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-98-growing-partition-leakage.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-98-growing-residue-leakage.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-98-growing-modulus-leakage.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-98-growing-modulus-leakage.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
