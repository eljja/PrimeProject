from __future__ import annotations

import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import mobius_values
from ticket97_periodic_projection_residual_audit import additive_coefficient, shift_two_coefficient
from ticket100_extended_residual_vaughan_audit import (
    CANDIDATE_K,
    _segment_bounds,
    goldbach_main_vector,
    lambda_values,
    schedule_moduli,
    transform_size,
    twin_main_vector,
    vaughan_components,
)


GENERATED_AT = "2026-07-13T07:05:00+09:00"
SCHEMA = "primeproject.ticket101-vaughan-cutoff-energy-audit.v1"
LIMIT = 1_000_000
BALANCED_VALUES = (32, 48, 64, 80, 100)
REFINED_TWIN_PAIRS = ((96, 84), (100, 80), (100, 84), (100, 88))
NEAR_COLLAPSE_CUTOFFS = (800, 840, 880, 900, 920, 940, 960, 980, 990, 999, 1_000)


def build_external_main_arrays(limit: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    goldbach_main = np.zeros(limit + 1, dtype=np.float64)
    twin_main = np.zeros(limit + 1, dtype=np.float64)
    goldbach_mask = np.zeros(limit + 1, dtype=bool)
    twin_mask = np.zeros(limit + 1, dtype=bool)
    moduli = schedule_moduli(limit)
    for index, modulus in enumerate(moduli):
        lower, upper = _segment_bounds(moduli, index, limit)
        if lower > upper:
            continue
        even_numbers = np.arange(lower + lower % 2, upper + 1, 2, dtype=np.int64)
        all_numbers = np.arange(lower, upper + 1, dtype=np.int64)
        if len(even_numbers):
            goldbach_main[even_numbers] = goldbach_main_vector(even_numbers, modulus)
            goldbach_mask[even_numbers] = True
        if len(all_numbers):
            twin_main[all_numbers] = twin_main_vector(all_numbers, modulus)
            twin_mask[all_numbers] = True
    return goldbach_main, twin_main, goldbach_mask, twin_mask


def _maximum_component_row(
    numbers: np.ndarray,
    contribution: np.ndarray,
    main: np.ndarray,
) -> dict[str, Any]:
    required = np.maximum(0.0, -contribution / main) * np.log(numbers)
    position = int(np.argmax(required))
    return {
        "number": int(numbers[position]),
        "required_log_envelope_constant": float(required[position]),
        "contribution_over_external_main": float(contribution[position] / main[position]),
    }


def audit_cutoff_frontier(
    limit: int = LIMIT,
    balanced_pairs: tuple[tuple[int, int], ...] | None = None,
    near_cutoffs: tuple[int, ...] = NEAR_COLLAPSE_CUTOFFS,
) -> dict[str, Any]:
    cubic_cutoff = round(limit ** (1 / 3))
    if balanced_pairs is None:
        balanced_pairs = tuple((u, v) for u in BALANCED_VALUES for v in BALANCED_VALUES) + REFINED_TWIN_PAIRS
    all_pairs = tuple(dict.fromkeys(balanced_pairs + tuple((cutoff, cutoff) for cutoff in near_cutoffs)))
    values, mangoldt = lambda_values(limit + 2)
    mu = mobius_values(limit + 2)
    goldbach_main, twin_main, goldbach_mask, twin_mask = build_external_main_arrays(limit)
    goldbach_numbers = np.flatnonzero(goldbach_mask)
    twin_numbers = np.flatnonzero(twin_mask)
    size = transform_size(limit + 1)
    lambda_transform = np.fft.rfft(values[: limit + 1], size)
    rows: list[dict[str, Any]] = []

    for u, v in all_pairs:
        type_i, type_ii, _ = vaughan_components(values, mangoldt, mu, u, v, 0)
        structured_goldbach = (
            np.fft.irfft(np.fft.rfft(type_i[: limit + 1], size) * lambda_transform, size)[: limit + 1]
            - goldbach_main
        )
        type_ii_goldbach = np.fft.irfft(
            np.fft.rfft(type_ii[: limit + 1], size) * lambda_transform,
            size,
        )[: limit + 1]
        structured_twin = np.cumsum(type_i[: limit + 1] * values[2 : limit + 3]) - twin_main
        type_ii_twin = np.cumsum(type_ii[: limit + 1] * values[2 : limit + 3])

        goldbach_structured = _maximum_component_row(
            goldbach_numbers,
            structured_goldbach[goldbach_numbers],
            goldbach_main[goldbach_numbers],
        )
        goldbach_type_ii = _maximum_component_row(
            goldbach_numbers,
            type_ii_goldbach[goldbach_numbers],
            goldbach_main[goldbach_numbers],
        )
        twin_structured = _maximum_component_row(
            twin_numbers,
            structured_twin[twin_numbers],
            twin_main[twin_numbers],
        )
        twin_type_ii = _maximum_component_row(
            twin_numbers,
            type_ii_twin[twin_numbers],
            twin_main[twin_numbers],
        )
        support_count = int(np.count_nonzero(np.abs(type_ii) > 1e-12))
        rows.append(
            {
                "u": u,
                "v": v,
                "balanced_cubic_range": u <= cubic_cutoff and v <= cubic_cutoff,
                "uv_over_limit": u * v / limit,
                "type_ii_support_count": support_count,
                "type_ii_support_fraction": support_count / len(type_ii),
                "goldbach": {
                    "structured": goldbach_structured,
                    "type_ii": goldbach_type_ii,
                    "separate_budget_sum": goldbach_structured["required_log_envelope_constant"]
                    + goldbach_type_ii["required_log_envelope_constant"],
                },
                "twin": {
                    "structured": twin_structured,
                    "type_ii": twin_type_ii,
                    "separate_budget_sum": twin_structured["required_log_envelope_constant"]
                    + twin_type_ii["required_log_envelope_constant"],
                },
            }
        )

    balanced_rows = [row for row in rows if row["balanced_cubic_range"]]
    best_goldbach = min(balanced_rows, key=lambda row: float(row["goldbach"]["separate_budget_sum"]))
    best_twin = min(balanced_rows, key=lambda row: float(row["twin"]["separate_budget_sum"]))
    near_rows = [row for row in rows if row["u"] == row["v"] and row["u"] in near_cutoffs]
    near_survivors = [row for row in near_rows if float(row["goldbach"]["separate_budget_sum"]) <= CANDIDATE_K]
    first_near_survivor = min(near_survivors, key=lambda row: int(row["u"])) if near_survivors else None
    collapse_row = next((row for row in near_rows if int(row["u"]) ** 2 >= limit), None)
    return {
        "limit": limit,
        "cubic_cutoff": cubic_cutoff,
        "candidate_constant": CANDIDATE_K,
        "evaluated_pair_count": len(rows),
        "balanced_pair_count": len(balanced_rows),
        "balanced_goldbach_survivor_count": sum(
            int(float(row["goldbach"]["separate_budget_sum"]) <= CANDIDATE_K) for row in balanced_rows
        ),
        "balanced_twin_survivor_count": sum(
            int(float(row["twin"]["separate_budget_sum"]) <= CANDIDATE_K) for row in balanced_rows
        ),
        "best_balanced_goldbach_row": best_goldbach,
        "best_balanced_twin_row": best_twin,
        "first_tested_near_collapse_goldbach_survivor": first_near_survivor,
        "full_collapse_row": collapse_row,
        "near_collapse_rows": near_rows,
    }


def audit_energy_equivalences(
    checkpoints: tuple[int, ...] = (10_000, 100_000, 1_000_000),
) -> dict[str, Any]:
    maximum = max(checkpoints)
    values, _ = lambda_values(maximum + 2)
    rows: list[dict[str, Any]] = []
    failures = 0
    moduli = schedule_moduli(maximum)
    for target in checkpoints:
        modulus = max(modulus for modulus in moduli if modulus * modulus <= target)
        goldbach_main = float(goldbach_main_vector(np.array([target], dtype=np.int64), modulus)[0])
        twin_main = float(twin_main_vector(np.array([target], dtype=np.int64), modulus)[0])
        goldbach_exact = additive_coefficient(values, values, target)
        twin_exact = shift_two_coefficient(values, values, target)

        goldbach_left = values[: target + 1]
        goldbach_right = values[target::-1]
        goldbach_energy = float(np.dot(goldbach_left, goldbach_left))
        goldbach_mismatch = float(np.dot(goldbach_left - goldbach_right, goldbach_left - goldbach_right))
        goldbach_identity = goldbach_energy - 0.5 * goldbach_mismatch
        goldbach_lower_target = goldbach_main * (1 - CANDIDATE_K / math.log(target))
        goldbach_equivalence_error = abs(
            (2 * (goldbach_energy - goldbach_lower_target) - goldbach_mismatch)
            - 2 * (goldbach_exact - goldbach_lower_target)
        )

        twin_left = values[: target + 1]
        twin_right = values[2 : target + 3]
        twin_left_energy = float(np.dot(twin_left, twin_left))
        twin_right_energy = float(np.dot(twin_right, twin_right))
        twin_mismatch = float(np.dot(twin_left - twin_right, twin_left - twin_right))
        twin_identity = 0.5 * (twin_left_energy + twin_right_energy - twin_mismatch)
        twin_lower_target = twin_main * (1 - CANDIDATE_K / math.log(target))
        twin_equivalence_error = abs(
            (twin_left_energy + twin_right_energy - 2 * twin_lower_target - twin_mismatch)
            - 2 * (twin_exact - twin_lower_target)
        )
        failures += int(abs(goldbach_exact - goldbach_identity) > 1e-7)
        failures += int(abs(twin_exact - twin_identity) > 1e-7)
        failures += int(goldbach_equivalence_error > 1e-7)
        failures += int(twin_equivalence_error > 1e-7)
        rows.append(
            {
                "target": target,
                "modulus": modulus,
                "goldbach_identity_error": abs(goldbach_exact - goldbach_identity),
                "goldbach_target_equivalence_error": goldbach_equivalence_error,
                "goldbach_mismatch_over_twice_energy": goldbach_mismatch / (2 * goldbach_energy),
                "twin_identity_error": abs(twin_exact - twin_identity),
                "twin_target_equivalence_error": twin_equivalence_error,
                "twin_mismatch_over_total_energy": twin_mismatch / (twin_left_energy + twin_right_energy),
            }
        )
    return {
        "identities": {
            "goldbach": "C_G(N)=||Lambda||_2^2-(1/2)||Lambda-J_N Lambda||_2^2.",
            "twin": "2C_2(x)=||Lambda_left||_2^2+||Lambda_shift2||_2^2-||Lambda_left-Lambda_shift2||_2^2.",
        },
        "novelty_verdict": "The mismatch-energy inequalities are algebraically equivalent to the target correlation lower bounds, not weaker reductions.",
        "independent_use": "They become useful only if an external theorem controls reflection or shift mismatch without importing the target correlation.",
        "failure_count": failures,
        "checkpoint_rows": rows,
    }


def analyze_vaughan_cutoff_energy() -> dict[str, Any]:
    frontier = audit_cutoff_frontier()
    energy = audit_energy_equivalences()
    best_goldbach = frontier["best_balanced_goldbach_row"]
    best_twin = frontier["best_balanced_twin_row"]
    near = frontier["first_tested_near_collapse_goldbach_survivor"]
    collapse = frontier["full_collapse_row"]
    failures = (
        int(frontier["balanced_goldbach_survivor_count"] != 0)
        + int(frontier["balanced_twin_survivor_count"] <= 0)
        + int(near is None)
        + int(collapse is None or int(collapse["type_ii_support_count"]) != 0)
        + int(energy["failure_count"])
    )
    return {
        "theorem_name": "VaughanCutoffParetoAndEnergyEquivalenceAudit",
        "source_ticket": "TICKET-100",
        "cutoff_frontier": frontier,
        "problem_split": {
            "goldbach": {
                "finding": "No balanced U,V<=N^(1/3) grid point has separate structured-plus-Type-II budget at most K=1.6.",
                "best_row": best_goldbach,
                "near_collapse_warning": "A finite Goldbach split first survives only near U=V=0.96 sqrt(N), where Type II support has nearly collapsed; U=V=sqrt(N) makes Type II identically zero.",
                "next_target": "JointBalancedVaughanGoldbachResidualEnvelope",
            },
            "twin": {
                "finding": "A balanced noncollapsed componentwise candidate survives at U=100,V=84.",
                "best_row": best_twin,
                "rounded_candidate": "Prove structured >= -1.40 M/log(x) and TypeII >= -0.18 M/log(x); the sum K=1.58 remains below 1.6.",
                "next_target": "SeparatedBalancedVaughanTwinBudgets",
            },
        },
        "energy_equivalence_audit": energy,
        "contrapositive_boundary": {
            "valid": "A conjecture counterexample forces near-maximal reflection or shift mismatch, so an independently proved mismatch deficit can rule it out.",
            "not_new": "Rewriting correlation as an energy deficit is exactly equivalent and supplies no estimate by itself.",
        },
        "discarded_routes": [
            "Generalize the U=V=100 Goldbach componentwise counterexample to Twin Prime without cutoff optimization.",
            "Accept U,V near sqrt(N) as a useful Type I/II split when the Type II support is almost or exactly empty.",
            "Present reflection or shift energy identities as weaker theorems than the original correlation targets.",
        ],
        "goldbach_next_theorem_target": "JointBalancedVaughanGoldbachResidualEnvelope",
        "twin_next_theorem_target": "SeparatedBalancedVaughanTwinBudgets",
        "machine_audit": {
            "limit": LIMIT,
            "candidate_constant": CANDIDATE_K,
            "balanced_pair_count": frontier["balanced_pair_count"],
            "balanced_goldbach_survivor_count": frontier["balanced_goldbach_survivor_count"],
            "balanced_twin_survivor_count": frontier["balanced_twin_survivor_count"],
            "energy_failure_count": energy["failure_count"],
            "total_failure_count": failures,
        },
        "theorem_status": "goldbach_joint_required_twin_separate_candidate_survives_energy_rewrite_equivalent_no_resolution" if failures == 0 else "ticket101_audit_inconclusive_no_resolution",
        "proof_boundary": "TICKET101 proves cutoff-grid and energy-equivalence audit results. It proves none of the four conjectures and no conjecture counterexample.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "cutoff_and_energy_novelty_gate_open",
        "route": route,
        "proof_or_counterexample_mode": "parameter frontier plus energy-equivalence novelty transfer",
        "attempt": "Optimize decomposition parameters before generalizing a componentwise no-go, and reject energy rewrites that are only algebraic equivalences.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket101_transfer": route, "independent_target": target},
        "obstruction": "No target-specific independent mismatch or signed-component theorem was proved in TICKET101.",
        "candidate_theorem": target,
        "next_experiment": "Search the nondegenerate parameter frontier and demand an estimate independent of the target identity.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket100 = read_json(ROOT / "data/open-problem/ticket100-extended-residual-vaughan-audit.json")
    audit = analyze_vaughan_cutoff_energy()
    attempts = [
        transfer_attempt(ticket100, "riemann", "RH-TICKET-101", "KernelParameterAndEnergyNoveltyGate", "IndependentKernelMismatchDeficit"),
        transfer_attempt(ticket100, "collatz", "CO-TICKET-101", "OrbitParameterAndEnergyNoveltyGate", "IndependentOrbitMismatchDeficit"),
        {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-101",
            "route": "BalancedVaughanGoldbachParetoAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "balanced cutoff frontier plus near-collapse leakage audit",
            "attempt": "Test whether any nondegenerate Vaughan cutoff rescues separate Goldbach component budgets before retaining the joint target.",
            "bounded_result": {"source_ticket": "GB-TICKET-100", "audit_ref": "vaughan_cutoff_energy_audit"},
            "obstruction": audit["problem_split"]["goldbach"]["near_collapse_warning"],
            "candidate_theorem": audit["goldbach_next_theorem_target"],
            "next_experiment": "Prove a joint balanced-range dispersion estimate; near-sqrt cutoff collapse is not admissible progress.",
            "claim_boundary": "No Goldbach proof and no certified Goldbach counterexample.",
        },
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-101",
            "route": "BalancedVaughanTwinParetoAudit",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "balanced cutoff frontier plus separated component candidate",
            "attempt": "Search for a noncollapsed Vaughan cutoff whose separate structured and Type II budgets sum below K=1.6.",
            "bounded_result": {"source_ticket": "TP-TICKET-100", "audit_ref": "vaughan_cutoff_energy_audit"},
            "obstruction": "The U=100,V=84 finite candidate still needs independent all-scale component estimates.",
            "candidate_theorem": audit["twin_next_theorem_target"],
            "next_experiment": "Attack the rounded K_S=1.40 and K_II=0.18 component bounds independently and falsify them beyond 1M.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "cutoff_frontier_splits_goldbach_joint_and_twin_separate_routes_energy_rewrite_equivalent_no_resolution",
        "claim_boundary": "TICKET101 refines proof routes by cutoff optimization and equivalence auditing; it solves none of the four open problems.",
        "vaughan_cutoff_energy_audit": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket101-vaughan-cutoff-energy-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-101-parameter-energy-gate.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-101-parameter-energy-gate.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-101-balanced-vaughan-frontier.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-101-balanced-vaughan-frontier.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
