from __future__ import annotations

import json
import math
from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import (
    ROOT,
    collatz_prefix_certificate,
    find_attempt,
    read_json,
    write_json,
)


GENERATED_AT = "2026-07-07T01:00:00+09:00"
SCHEMA = "primeproject.ticket33-global-measure-lab.v1"


def cylinder_mass(bits: int) -> float:
    return 2.0 ** (1 - bits)


def transition_label(low_open: bool, high_open: bool) -> str:
    if low_open and high_open:
        return "both_open"
    if low_open:
        return "low_only_open"
    if high_open:
        return "high_only_open"
    return "both_closed"


def round_float(value: float) -> float:
    return round(value, 12)


def linear_fit(points: list[tuple[int, float]]) -> dict[str, Any]:
    if len(points) < 2:
        return {"status": "insufficient_points"}
    xs = [float(x) for x, _ in points]
    ys = [math.log2(y) for _, y in points if y > 0]
    if len(ys) != len(xs):
        return {"status": "nonpositive_mass"}
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    denominator = sum((x - x_mean) ** 2 for x in xs)
    slope = numerator / denominator if denominator else 0.0
    intercept = y_mean - slope * x_mean
    return {
        "status": "fit_computed",
        "log2_mass_slope_per_bit": round_float(slope),
        "per_bit_factor": round_float(2.0**slope),
        "intercept": round_float(intercept),
        "point_count": len(points),
        "interpretation": (
            "A negative finite-range slope is evidence of pressure on the open frontier, not a proof that the "
            "frontier mass tends to zero for every future bit length."
        ),
    }


def frontier_measure_audit(base_bits: int = 12, max_bits: int = 28) -> dict[str, Any]:
    frontier = [residue for residue in range(1, 1 << base_bits, 2)]
    rows: list[dict[str, Any]] = []
    total_transition_counts: Counter[str] = Counter()
    high_examples: list[dict[str, Any]] = []
    high_only_examples: list[dict[str, Any]] = []

    for bits in range(base_bits, max_bits + 1):
        open_mass = len(frontier) * cylinder_mass(bits)
        row: dict[str, Any] = {
            "bits": bits,
            "open_frontier_count": len(frontier),
            "open_frontier_mass": round_float(open_mass),
        }
        rows.append(row)
        if bits == max_bits:
            break

        transition_counts: Counter[str] = Counter()
        next_frontier: list[int] = []
        low_open_count = 0
        high_open_count = 0
        for residue in frontier:
            low = collatz_prefix_certificate(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = collatz_prefix_certificate(high_residue, bits + 1)
            low_open = low.get("status") == "needs_split"
            high_open = high.get("status") == "needs_split"
            label = transition_label(low_open, high_open)
            transition_counts[label] += 1
            total_transition_counts[label] += 1
            if low_open:
                low_open_count += 1
                next_frontier.append(residue)
            if high_open:
                high_open_count += 1
                next_frontier.append(high_residue)
                if len(high_examples) < 8:
                    high_examples.append(
                        {
                            "parent_residue": residue,
                            "parent_bits": bits,
                            "high_child_residue": high_residue,
                            "child_bits": bits + 1,
                            "low_status": low.get("status"),
                            "high_status": high.get("status"),
                            "high_prefix_length": high.get("prefix_length"),
                            "high_consumed_bits": high.get("consumed_bits"),
                            "high_next_valuation": high.get("next_valuation"),
                        }
                    )
                if not low_open and len(high_only_examples) < 8:
                    high_only_examples.append(
                        {
                            "parent_residue": residue,
                            "parent_bits": bits,
                            "high_child_residue": high_residue,
                            "child_bits": bits + 1,
                            "low_status": low.get("status"),
                            "high_status": high.get("status"),
                            "high_prefix_length": high.get("prefix_length"),
                            "high_consumed_bits": high.get("consumed_bits"),
                            "high_next_valuation": high.get("next_valuation"),
                        }
                    )

        next_mass = len(next_frontier) * cylinder_mass(bits + 1)
        row["transition_counts"] = dict(sorted(transition_counts.items()))
        row["low_open_child_count"] = low_open_count
        row["high_open_child_count"] = high_open_count
        row["low_open_child_mass"] = round_float(low_open_count * cylinder_mass(bits + 1))
        row["high_open_child_mass"] = round_float(high_open_count * cylinder_mass(bits + 1))
        row["next_open_frontier_count"] = len(next_frontier)
        row["next_open_frontier_mass"] = round_float(next_mass)
        row["mass_ratio_to_next"] = round_float(next_mass / open_mass) if open_mass else None
        frontier = next_frontier

    final_row = rows[-1]
    ratios = [row.get("mass_ratio_to_next") for row in rows if row.get("mass_ratio_to_next") is not None]
    monotone = all(rows[index + 1]["open_frontier_mass"] <= rows[index]["open_frontier_mass"] for index in range(len(rows) - 1))
    tail_points = [(row["bits"], row["open_frontier_mass"]) for row in rows[-8:]]
    high_open_total = total_transition_counts["both_open"] + total_transition_counts["high_only_open"]
    high_only_total = total_transition_counts["high_only_open"]
    return {
        "base_modulus_bits": base_bits,
        "max_modulus_bits": max_bits,
        "frontier_rows": rows,
        "initial_open_frontier_mass": rows[0]["open_frontier_mass"],
        "final_open_frontier_count": final_row["open_frontier_count"],
        "final_open_frontier_mass": final_row["open_frontier_mass"],
        "monotone_open_mass_decrease": monotone,
        "min_mass_ratio_to_next": round_float(min(ratios)) if ratios else None,
        "max_mass_ratio_to_next": round_float(max(ratios)) if ratios else None,
        "tail_log2_mass_fit": linear_fit(tail_points),
        "transition_totals": dict(sorted(total_transition_counts.items())),
        "high_branch_obstruction": {
            "high_open_child_edges": high_open_total,
            "high_only_open_child_edges": high_only_total,
            "status": "high_branches_remain_open_in_bounded_frontier" if high_open_total else "no_high_open_edges_seen",
            "high_open_examples": high_examples,
            "high_only_examples": high_only_examples,
            "refuted_shortcut": (
                "High children do not automatically close in the tested frontier; some parents have a closed low "
                "child and an open high child."
            ),
        },
        "measure_certificate": {
            "status": "bounded_measure_decay_observed",
            "closed_partial_theorem": (
                "In the tested adaptive Collatz frontier, normalized open cylinder mass decreases from the base "
                "level to the recorded maximum bit length."
            ),
            "compactness_status": "open_no_global_compactness_theorem",
            "proof_boundary": (
                "Finite monotone mass decrease and a negative fitted slope do not prove that open mass tends to "
                "zero. A full proof needs a global compactness theorem or a well-founded high-branch closure argument."
            ),
        },
        "next_candidate": "CO-TICKET-34 HighBranchAutomatonOrMassLimitTheorem",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    obstruction: str,
    candidate_theorem: str,
    next_experiment: str,
) -> dict[str, Any]:
    source_attempt = find_attempt(source, problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "global_compactness_refinement",
        "attempt": (
            "Move from bounded stateful certificates to global compactness pressure: finite decreasing quantities "
            "matter only if they can be upgraded into a theorem that rules out all infinite obstruction paths."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "frontier_status": "open_infinite_bridge",
            "ticket33_transfer": route,
        },
        "obstruction": obstruction,
        "candidate_theorem": candidate_theorem,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket32-stateful-measure-lab.json")
    collatz_attempt = {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-33",
        "status": "proof_pressure_open",
        "route": "GlobalMeasureCompactnessOrHighBranchClosure",
        "proof_or_counterexample_mode": "global_measure_counterexample_guided_synthesis",
        "attempt": (
            "Test whether the adaptive exact-cylinder frontier supports a global measure argument, and whether "
            "high-child branches close automatically after Ticket 32 handles same-signature low-child stutter."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-32",
            "global_measure_audit": frontier_measure_audit(),
        },
        "obstruction": (
            "Normalized open frontier mass decreases on the tested range, but the final frontier mass is still "
            "positive and high-child branches remain open. A finite decay fit is not a compactness theorem."
        ),
        "candidate_theorem": (
            "Prove either that normalized open cylinder mass tends to zero under adaptive splitting, or that every "
            "high-child obstruction is absorbed by a finite automaton/rank argument compatible with low-child stutter budgets."
        ),
        "next_experiment": "Synthesize a high-branch automaton and separately test a rigorous mass-limit theorem template.",
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-33",
            "GlobalTailCompactness",
            "A bounded tail state certificate still needs a compactness theorem controlling infinitely many zero contributions.",
            "A global tail compactness theorem makes any off-critical zero produce a finite positivity failure.",
            "Search admissible kernel families whose tail bounds are monotone and independently replayable.",
        ),
        collatz_attempt,
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-33",
            "GlobalCutoffCompactness",
            "A finite cutoff ledger still needs a theorem that no error term reopens beyond the cutoff.",
            "A global cutoff compactness theorem proves every ledger state beyond N0 has positive representation count.",
            "Audit whether major/minor arc error states form a monotone cone under increasing n.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-33",
            "GlobalParityCompactness",
            "A parity selector state machine still needs a compactness theorem preventing exact-gap mass from leaking into wider gaps.",
            "A global parity compactness theorem keeps exact gap-2 mass positive at arbitrarily large scale.",
            "Stress exact-gap selector states against wider-gap leakage and parity countermodels.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "global_measure_open_no_resolution",
        "claim_boundary": (
            "Ticket 33 observes bounded Collatz frontier mass decay and high-branch obstruction. It does not prove "
            "or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket33-global-measure-lab.json"
    write_json(aggregate_path, payload)
    for attempt in payload["attempts"]:
        problem_id = attempt["problem_id"]
        if problem_id == "riemann":
            path = ROOT / "data/open-problem/riemann/rh-ticket-33-global-tail-compactness.json"
        elif problem_id == "collatz":
            path = ROOT / "data/open-problem/collatz/co-ticket-33-global-measure-compactness.json"
        elif problem_id == "goldbach":
            path = ROOT / "data/open-problem/goldbach/gb-ticket-33-global-cutoff-compactness.json"
        elif problem_id == "twin-prime":
            path = ROOT / "data/open-problem/twin-prime/tp-ticket-33-global-parity-compactness.json"
        else:
            raise ValueError(problem_id)
        write_json(path, attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
