from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from typing import Any, Callable

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket42_parametric_transition_template_lab import stringify_key
from ticket43_lift_constraint_measure_lab import (
    FAMILY,
    LiftSnapshot,
    build_lift_snapshots,
    synthesize_rank_debt_measure,
    topological_rank,
)


GENERATED_AT = "2026-07-08T23:20:00+09:00"
SCHEMA = "primeproject.ticket44-feature-measure-counteredge-lab.v1"


FeatureMap = Callable[[tuple[Any, ...]], tuple[float, ...]]


@dataclass(frozen=True)
class FeatureTrial:
    name: str
    description: str
    feature_map: FeatureMap
    proof_intent: str


def tail_values(template: tuple[Any, ...]) -> tuple[int, int, int, int]:
    word = tuple(int(value) for value in template[1])
    padded = (0, 0, 0, 0) + word[-4:]
    return tuple(padded[-4:])


def clipped(value: int, cap: int) -> int:
    return value if value < cap else cap


def phase_tail_scalar(template: tuple[Any, ...]) -> tuple[float, ...]:
    phase = int(template[0])
    tail = tail_values(template)
    residue = int(template[2])
    next_v = int(template[3])
    return (
        float(phase),
        float(sum(tail)),
        float(tail[-1]),
        float(max(tail)),
        float(residue % 16),
        float(bin(residue).count("1")),
        float(clipped(next_v, 16)),
    )


def debt_only_constant(_: tuple[Any, ...]) -> tuple[float, ...]:
    return (0.0,)


def numeric_template_coordinates(template: tuple[Any, ...]) -> tuple[float, ...]:
    phase = int(template[0])
    tail = tail_values(template)
    residue = int(template[2])
    next_v = int(template[3])
    return tuple(float(value) for value in (phase, *tail, residue, next_v))


def residue_binary_coordinates(template: tuple[Any, ...]) -> tuple[float, ...]:
    phase = int(template[0])
    tail = tail_values(template)
    residue = int(template[2])
    next_v = int(template[3])
    residue_bits = tuple(float((residue >> bit) & 1) for bit in range(8))
    return tuple(float(value) for value in (phase, *tail, clipped(next_v, 24))) + residue_bits


def phase_residue_onehot_tail_numeric(template: tuple[Any, ...]) -> tuple[float, ...]:
    phase = int(template[0])
    tail = tail_values(template)
    residue = int(template[2])
    next_v = int(template[3])
    phase_bits = tuple(1.0 if phase == value else 0.0 for value in range(16))
    residue_low_bits = tuple(1.0 if residue % 16 == value else 0.0 for value in range(16))
    return phase_bits + residue_low_bits + tuple(float(value) for value in (*tail, clipped(next_v, 24)))


FEATURE_TRIALS = [
    FeatureTrial(
        name="debt_only_constant",
        description="No template feature at all; this is the pure debt-only descent route.",
        feature_map=debt_only_constant,
        proof_intent=(
            "This is the weakest possible measure. It is included as a control because TICKET42/TICKET43 already "
            "showed that debt alone cannot prove Collatz descent."
        ),
    ),
    FeatureTrial(
        name="phase_tail_scalar",
        description="Small explicit scalar features: phase, tail summaries, residue bucket, popcount, clipped next valuation.",
        feature_map=phase_tail_scalar,
        proof_intent=(
            "If this worked, Collatz descent could be expressed by a compact closed-form feature measure rather than "
            "a horizon-specific rank table."
        ),
    ),
    FeatureTrial(
        name="numeric_template_coordinates",
        description="Direct numeric coordinates of the template: phase, four tail valuations, residue mod 256, next valuation.",
        feature_map=numeric_template_coordinates,
        proof_intent=(
            "If this worked, the observed template rank might be replaceable by a simple affine formula over the "
            "template coordinates."
        ),
    ),
    FeatureTrial(
        name="residue_binary_coordinates",
        description="Phase, four tail valuations, clipped next valuation, and the eight residue bits separately.",
        feature_map=residue_binary_coordinates,
        proof_intent=(
            "This tests whether the residue obstruction is an artifact of treating residue as a scalar coordinate."
        ),
    ),
    FeatureTrial(
        name="phase_residue_onehot_tail_numeric",
        description="One-hot phase, one-hot residue mod 16, numeric tail, and clipped next valuation.",
        feature_map=phase_residue_onehot_tail_numeric,
        proof_intent=(
            "This is a richer but still horizon-independent feature dictionary. It is intentionally weaker than a "
            "one-hot table over every observed template node."
        ),
    ),
]


def round_float(value: float, digits: int = 12) -> float:
    return round(float(value), digits)


def dot(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(left, right))


def vector_subtract(parent: tuple[float, ...], child: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(round_float(a - b, 10) for a, b in zip(parent, child))


def vector_neg(vector: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(round_float(-value, 10) for value in vector)


def compact_vector(vector: tuple[float, ...], limit: int = 14) -> list[float]:
    values = [round_float(value, 6) for value in vector]
    if len(values) <= limit:
        return values
    return values[:limit] + ["..."]  # type: ignore[list-item]


def edge_example(parent: tuple[Any, ...], child: tuple[Any, ...], stats: Any) -> dict[str, Any]:
    return {
        "parent_template": stringify_key(parent),
        "child_template": stringify_key(child),
        "count": stats.count,
        "max_delta_debt": round_float(stats.max_delta_debt),
        "min_delta_debt": round_float(stats.min_delta_debt),
        "example": stats.max_debt_example or stats.example,
    }


def analyze_feature_trial(snapshot: LiftSnapshot, trial: FeatureTrial) -> dict[str, Any]:
    constraints: dict[tuple[float, ...], dict[str, Any]] = {}
    zero_delta_refuters: list[dict[str, Any]] = []
    zero_delta_refuter_count = 0
    positive_bound_count = 0

    for (parent, child), stats in snapshot.edges.items():
        parent_features = trial.feature_map(parent)
        child_features = trial.feature_map(child)
        delta = vector_subtract(parent_features, child_features)
        max_debt = float(stats.max_delta_debt)
        if max_debt >= 0:
            positive_bound_count += 1
        if all(value == 0 for value in delta) and max_debt >= 0:
            zero_delta_refuter_count += 1
            if len(zero_delta_refuters) < 8:
                zero_delta_refuters.append(
                    {
                        **edge_example(parent, child, stats),
                        "feature_delta": compact_vector(delta),
                        "reason": "same feature vector but nonnegative debt pressure",
                    }
                )
        row = constraints.setdefault(
            delta,
            {
                "delta": delta,
                "max_bound": max_debt,
                "count": 0,
                "edge_count": 0,
                "example": edge_example(parent, child, stats),
            },
        )
        row["count"] += int(stats.count)
        row["edge_count"] += 1
        if max_debt > float(row["max_bound"]):
            row["max_bound"] = max_debt
            row["example"] = edge_example(parent, child, stats)

    reverse_conflicts: list[dict[str, Any]] = []
    seen: set[tuple[float, ...]] = set()
    for delta, row in constraints.items():
        if delta in seen or all(value == 0 for value in delta):
            continue
        opposite = vector_neg(delta)
        other = constraints.get(opposite)
        if other is None:
            continue
        seen.add(delta)
        seen.add(opposite)
        combined_bound = float(row["max_bound"]) + float(other["max_bound"])
        if combined_bound >= 0:
            reverse_conflicts.append(
                {
                    "feature_delta": compact_vector(delta),
                    "opposite_feature_delta": compact_vector(opposite),
                    "combined_required_bound": round_float(combined_bound),
                    "forward": row["example"],
                    "reverse": other["example"],
                    "reason": "w·d > a and w·(-d) > b force 0 > a+b, impossible when a+b >= 0",
                }
            )
    reverse_conflicts.sort(key=lambda row: float(row["combined_required_bound"]), reverse=True)

    affine_search = sampled_affine_search(list(constraints.values()))
    if zero_delta_refuter_count:
        status = "exact_zero_delta_counteredge_refutes_feature_measure"
    elif reverse_conflicts:
        status = "reverse_constraint_counteredges_refute_feature_measure"
    elif affine_search["status"] == "sampled_affine_measure_found":
        status = "sampled_affine_feature_measure_found_not_proof"
    else:
        status = "not_certified_by_bounded_affine_search"

    return {
        "feature_family": trial.name,
        "description": trial.description,
        "proof_intent": trial.proof_intent,
        "status": status,
        "feature_dimension": len(trial.feature_map(next(iter(snapshot.nodes)))),
        "template_edge_count": len(snapshot.edges),
        "unique_constraint_count": len(constraints),
        "positive_debt_pressure_edge_count": positive_bound_count,
        "zero_delta_refuter_count": zero_delta_refuter_count,
        "reverse_conflict_count": len(reverse_conflicts),
        "zero_delta_refuters": zero_delta_refuters[:8],
        "reverse_conflicts": reverse_conflicts[:8],
        "sampled_affine_search": affine_search,
        "claim_boundary": (
            "A refuted feature family is not a Collatz counterexample; it only rejects that proposed proof measure. "
            "A found sampled affine measure would still require a theorem covering all future lifts."
        ),
    }


def sampled_affine_search(rows: list[dict[str, Any]], passes: int = 6) -> dict[str, Any]:
    if not rows:
        return {"status": "no_constraints"}
    dimension = len(rows[0]["delta"])
    weights = [0.0] * dimension
    margin = 1e-6
    updates = 0
    worst: dict[str, Any] | None = None

    ordered = sorted(rows, key=lambda row: float(row["max_bound"]), reverse=True)
    for _ in range(passes):
        changed = False
        worst = None
        for row in ordered:
            delta = tuple(float(value) for value in row["delta"])
            bound = float(row["max_bound"])
            score = sum(weight * value for weight, value in zip(weights, delta))
            gap = score - bound
            if worst is None or gap < float(worst["gap"]):
                worst = {
                    "gap": round_float(gap),
                    "score": round_float(score),
                    "required_bound": round_float(bound),
                    "feature_delta": compact_vector(delta),
                    "example": row["example"],
                }
            if gap <= margin:
                norm_sq = sum(value * value for value in delta)
                if norm_sq == 0:
                    continue
                step = (bound + 1.0 - score) / norm_sq
                for index, value in enumerate(delta):
                    weights[index] += step * value
                updates += 1
                changed = True
        if not changed:
            break

    violations = 0
    worst = None
    for row in ordered:
        delta = tuple(float(value) for value in row["delta"])
        bound = float(row["max_bound"])
        score = sum(weight * value for weight, value in zip(weights, delta))
        gap = score - bound
        if gap <= 0:
            violations += 1
        if worst is None or gap < float(worst["gap"]):
            worst = {
                "gap": round_float(gap),
                "score": round_float(score),
                "required_bound": round_float(bound),
                "feature_delta": compact_vector(delta),
                "example": row["example"],
            }

    return {
        "status": "sampled_affine_measure_found" if violations == 0 else "sampled_affine_search_failed",
        "passes": passes,
        "updates": updates,
        "violating_unique_constraints": violations,
        "weight_l2": round_float(sum(weight * weight for weight in weights) ** 0.5),
        "weight_preview": [round_float(value, 6) for value in weights[:18]],
        "worst_constraint": worst,
        "proof_boundary": (
            "This is a bounded numerical search over a chosen feature family. Failure is not a mathematical "
            "impossibility unless an exact zero-delta or reverse-constraint certificate is present."
        ),
    }


def rank_table_baseline(snapshot: LiftSnapshot) -> dict[str, Any]:
    topo, rank = topological_rank(snapshot.adjacency, snapshot.nodes)
    measure = synthesize_rank_debt_measure(snapshot, rank) if rank else {"status": "no_rank_available"}
    return {
        "status": "bounded_rank_table_available_not_horizon_independent",
        "topological_rank": topo,
        "sampled_rank_debt_measure": measure,
        "interpretation": (
            "The observed template table can rank the sampled DAG, but it assigns values to observed nodes only. "
            "It does not define ranks for future templates introduced by larger horizons."
        ),
    }


def compare_rank_extension_from_ticket43() -> dict[str, Any]:
    ticket43 = read_json(ROOT / "data/open-problem/ticket43-lift-constraint-measure-lab.json")
    collatz = next(attempt for attempt in ticket43["attempts"] if attempt["problem_id"] == "collatz")
    audit = collatz["bounded_result"]["lift_constraint_measure_audit"]
    latest = audit["extension_comparisons"][-1]
    return {
        "source_ticket": "CO-TICKET-43",
        "from_max_bits": latest["from_max_bits"],
        "to_max_bits": latest["to_max_bits"],
        "new_template_edge_count": latest["new_template_edge_count"],
        "rank_changed_previous_node_count": latest["rank_changed_previous_node_count"],
        "old_measure_unknown_rank_edges": latest["old_measure_unknown_rank_edges"],
        "closure_status": latest["closure_status"],
        "interpretation": (
            "Any rank table over observed nodes must explain how new future nodes and edges receive compatible "
            "ranks. TICKET43 showed that this is the current infinite bridge."
        ),
    }


def collatz_attempt() -> dict[str, Any]:
    snapshots = build_lift_snapshots(base_bits=12, max_bits=26, checkpoints=(26,))
    snapshot = snapshots[26]
    trials = [analyze_feature_trial(snapshot, trial) for trial in FEATURE_TRIALS]
    rank_baseline = rank_table_baseline(snapshot)
    extension_gate = compare_rank_extension_from_ticket43()
    exact_refuted = [trial for trial in trials if "refute" in trial["status"]]
    open_or_failed = [trial for trial in trials if "refute" not in trial["status"]]
    strongest_counteredges = [
        {
            "feature_family": trial["feature_family"],
            "status": trial["status"],
            "zero_delta_refuter_count": trial["zero_delta_refuter_count"],
            "reverse_conflict_count": trial["reverse_conflict_count"],
            "first_zero_delta_refuter": (trial["zero_delta_refuters"] or [None])[0],
            "first_reverse_conflict": (trial["reverse_conflicts"] or [None])[0],
        }
        for trial in trials
    ]
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-44",
        "route": "HorizonIndependentFeatureMeasureOrCounteredge",
        "status": "proof_pressure_open",
        "proof_or_counterexample_mode": "feature-measure cegis plus counteredge extraction",
        "attempt": (
            "Try to replace the TICKET43 horizon-specific rank table with explicit feature measures. If a feature "
            "family cannot work, record exact counteredges so the proof route is discarded rather than repeated."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-43",
            "feature_measure_counteredge_audit": {
                "family": FAMILY,
                "max_bits": 26,
                "template_node_count": len(snapshot.nodes),
                "template_edge_count": len(snapshot.edges),
                "raw_open_edge_count": snapshot.raw_open_edge_count,
                "rank_table_baseline": rank_baseline,
                "horizon_extension_gate": extension_gate,
                "feature_trials": trials,
                "exactly_refuted_feature_family_count": len(exact_refuted),
                "not_certified_or_open_feature_family_count": len(open_or_failed),
                "strongest_counteredges": strongest_counteredges,
                "route_decision": {
                    "discard": [
                        "debt-only or low-dimensional scalar feature measure as a Collatz proof",
                        "numeric template-coordinate affine measure without counteredge clearance",
                        "observed-node rank table treated as a horizon-independent theorem",
                    ],
                    "retain": [
                        "exact counteredge extraction for every proposed feature measure",
                        "horizon-independent symbolic rank or lift theorem as the decisive proof target",
                        "future-edge search that violates every finite-rank extension as the disproof target",
                    ],
                },
                "closed_bounded_statement": (
                    "Debt-only descent is exactly refuted on the 26-bit sampled template graph. Richer compact "
                    "affine feature families were not certified by the bounded search, while the observed rank table "
                    "remains a bounded certificate only."
                ),
                "proof_boundary": (
                    "No Collatz proof and no Collatz counterexample. TICKET44 only prunes weak measure families and "
                    "sharpens the next theorem: a horizon-independent symbolic rank or an explicit future counteredge."
                ),
            },
        },
        "obstruction": (
            "A compact explicit feature measure must survive exact counteredges and also assign compatible ranks to "
            f"{extension_gate['new_template_edge_count']} new 25->26 template edges. The current rank table does not."
        ),
        "candidate_theorem": (
            "There exists a horizon-independent symbolic rank R(template) and scale c such that "
            "c*(R(parent)-R(child)) + debt(parent)-debt(child) is positive for every future lifted template edge."
        ),
        "next_experiment": (
            "Generate TICKET45 by synthesizing symbolic rank clauses instead of numeric affine features, and search "
            "for the first future edge that violates every clause extension."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    discarded_shortcut: str,
    retained_target: str,
    counterexample_target: str,
    next_experiment: str,
) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "route": route,
        "status": "proof_pressure_open",
        "proof_or_counterexample_mode": "feature-measure counteredge transfer",
        "attempt": (
            "Transfer TICKET44's lesson: a bounded numerical or visual pattern is useful only after the proposed "
            "feature measure survives exact counteredge extraction and a future-lift theorem."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior["route"],
            "discarded_shortcut": discarded_shortcut,
            "retained_target": retained_target,
            "counterexample_target": counterexample_target,
            "ticket44_transfer": route,
        },
        "obstruction": (
            "The current artifact names a better proof target, but it does not close the infinite theorem or produce "
            "a certified counterexample."
        ),
        "candidate_theorem": retained_target,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket43-lift-constraint-measure-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-44",
            "ZeroFeatureMeasureOrOffCriticalCounteredge",
            "finite zero-template feature score treated as RH",
            "A horizon-independent positive-kernel feature measure excludes every off-critical zero lift.",
            "an off-critical lift that has identical feature score or a reverse positive-kernel constraint",
            "Extract zero-template feature counteredges before promoting any kernel-measure candidate.",
        ),
        collatz_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-44",
            "GoldbachMarginFeatureMeasureOrExceptionCounteredge",
            "finite explicit-margin feature score treated as Goldbach",
            "A horizon-independent margin feature measure stays positive for every future even-integer lift.",
            "a future even-integer lift whose feature score is unchanged while margin pressure is nonpositive",
            "Extract margin-feature counteredges before promoting any explicit cutoff measure.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-44",
            "ExactGapFeatureMeasureOrLeakageCounteredge",
            "bounded exact-gap feature score treated as twin-prime infinitude",
            "A horizon-independent exact-gap feature measure prevents gap-2 mass from leaking to wider gaps.",
            "a leakage lift with identical exact-gap features or reverse leakage constraints",
            "Extract exact-gap feature counteredges before promoting any gap-selector measure.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "feature_measure_counteredge_open_no_resolution",
        "claim_boundary": (
            "Ticket 44 prunes weak horizon-independent feature measures and extracts exact counteredges where "
            "available. It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket44-feature-measure-counteredge-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-44-zero-feature-counteredge.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-44-feature-measure-counteredge.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-44-margin-feature-counteredge.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-44-gap-feature-counteredge.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
