from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
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
from ticket44_feature_measure_counteredge_lab import round_float


GENERATED_AT = "2026-07-08T23:55:00+09:00"
SCHEMA = "primeproject.ticket45-symbolic-rank-clause-lab.v1"


ClauseKey = tuple[int, ...]
ClauseMap = Callable[[tuple[Any, ...]], ClauseKey]


@dataclass(frozen=True)
class ClauseFamily:
    name: str
    description: str
    clause_map: ClauseMap
    proof_intent: str


@dataclass
class ClauseEdgeStats:
    count: int = 0
    max_delta_debt: float = float("-inf")
    example: dict[str, Any] | None = None

    def add(self, template_stats: Any) -> None:
        value = float(template_stats.max_delta_debt)
        if self.count == 0 or value > self.max_delta_debt:
            self.max_delta_debt = value
            self.example = template_stats.max_debt_example or template_stats.example
        self.count += int(template_stats.count)


def tail4(template: tuple[Any, ...]) -> tuple[int, int, int, int]:
    word = tuple(int(value) for value in template[1])
    padded = (0, 0, 0, 0) + word[-4:]
    return tuple(padded[-4:])


def clipped(value: int, cap: int) -> int:
    return value if value < cap else cap


def phase_only(template: tuple[Any, ...]) -> ClauseKey:
    return (int(template[0]),)


def phase_tail_mass_vbucket(template: tuple[Any, ...]) -> ClauseKey:
    tail = tail4(template)
    return (
        int(template[0]),
        clipped(sum(tail), 16),
        clipped(max(tail), 8),
        clipped(int(template[3]), 8),
    )


def phase_tail_residue16_vbucket(template: tuple[Any, ...]) -> ClauseKey:
    tail = tail4(template)
    return (int(template[0]), *tail, int(template[2]) % 16, clipped(int(template[3]), 16))


def phase_tail_residue64_vbucket(template: tuple[Any, ...]) -> ClauseKey:
    tail = tail4(template)
    return (int(template[0]), *tail, int(template[2]) % 64, clipped(int(template[3]), 16))


def phase_tail_residue256_vexact(template: tuple[Any, ...]) -> ClauseKey:
    tail = tail4(template)
    return (int(template[0]), *tail, int(template[2]), int(template[3]))


CLAUSE_FAMILIES = [
    ClauseFamily(
        name="phase_only",
        description="One rank clause per phase modulo 16.",
        clause_map=phase_only,
        proof_intent="Test whether phase alone can define a horizon-independent rank.",
    ),
    ClauseFamily(
        name="phase_tail_mass_vbucket",
        description="Phase plus coarse valuation-tail mass and clipped next-valuation.",
        clause_map=phase_tail_mass_vbucket,
        proof_intent="Test a small symbolic rank family that ignores residue identity.",
    ),
    ClauseFamily(
        name="phase_tail_residue16_vbucket",
        description="Phase, exact four-symbol valuation tail, residue modulo 16, clipped next-valuation.",
        clause_map=phase_tail_residue16_vbucket,
        proof_intent="Test whether low residue classes break the pressure cycles.",
    ),
    ClauseFamily(
        name="phase_tail_residue64_vbucket",
        description="Phase, exact four-symbol valuation tail, residue modulo 64, clipped next-valuation.",
        clause_map=phase_tail_residue64_vbucket,
        proof_intent="Test whether a medium residue quotient is enough for a symbolic rank.",
    ),
    ClauseFamily(
        name="phase_tail_residue256_vexact",
        description="The observed 26-bit template identity used by TICKET43.",
        clause_map=phase_tail_residue256_vexact,
        proof_intent=(
            "Use the observed template table as a ceiling control: it may certify the bounded sample, but it is "
            "not a horizon-independent theorem."
        ),
    ),
]


def encode_key(key: ClauseKey) -> str:
    return json.dumps(list(key), separators=(",", ":"))


def compact_example(example: dict[str, Any] | None) -> dict[str, Any] | None:
    if not example:
        return None
    keep = (
        "bits",
        "direction",
        "label",
        "parent_template",
        "child_template",
        "delta_prefix",
        "delta_consumed",
        "delta_debt",
    )
    return {key: example[key] for key in keep if key in example}


def build_clause_graph(
    snapshot: LiftSnapshot,
    family: ClauseFamily,
) -> tuple[
    set[ClauseKey],
    dict[tuple[ClauseKey, ClauseKey], ClauseEdgeStats],
    dict[ClauseKey, set[ClauseKey]],
]:
    clause_nodes = {family.clause_map(node) for node in snapshot.nodes}
    clause_edges: dict[tuple[ClauseKey, ClauseKey], ClauseEdgeStats] = {}
    pressure_adjacency: dict[ClauseKey, set[ClauseKey]] = defaultdict(set)
    for (parent, child), stats in snapshot.edges.items():
        parent_key = family.clause_map(parent)
        child_key = family.clause_map(child)
        edge_key = (parent_key, child_key)
        clause_edges.setdefault(edge_key, ClauseEdgeStats()).add(stats)
    for (parent_key, child_key), stats in clause_edges.items():
        if stats.max_delta_debt >= 0:
            pressure_adjacency[parent_key].add(child_key)
    return clause_nodes, clause_edges, pressure_adjacency


def scale_interval_for_clause_rank(
    clause_edges: dict[tuple[ClauseKey, ClauseKey], ClauseEdgeStats],
    clause_rank: dict[ClauseKey, int],
) -> dict[str, Any]:
    low_exclusive = 0.0
    high_exclusive = float("inf")
    impossible_rows: list[dict[str, Any]] = []
    worst_at_scale: dict[str, Any] | None = None

    for (parent_key, child_key), stats in clause_edges.items():
        gap = int(clause_rank.get(parent_key, 0)) - int(clause_rank.get(child_key, 0))
        bound = float(stats.max_delta_debt)
        if gap > 0:
            low_exclusive = max(low_exclusive, bound / gap)
        elif gap == 0:
            if bound >= 0:
                impossible_rows.append(
                    {
                        "reason": "same_clause_nonnegative_pressure",
                        "parent_clause": encode_key(parent_key),
                        "child_clause": encode_key(child_key),
                        "rank_gap": gap,
                        "max_delta_debt": round_float(bound),
                        "example": compact_example(stats.example),
                    }
                )
        else:
            high_exclusive = min(high_exclusive, bound / gap)

    min_integer_scale = max(1, math.floor(low_exclusive) + 1)
    if math.isinf(high_exclusive):
        max_integer_scale: int | None = None
    else:
        max_integer_scale = math.ceil(high_exclusive) - 1

    feasible = not impossible_rows and (max_integer_scale is None or min_integer_scale <= max_integer_scale)
    selected_scale = min_integer_scale if feasible else None
    min_margin = float("inf")
    violating_edges = 0
    if selected_scale is not None:
        for (parent_key, child_key), stats in clause_edges.items():
            gap = int(clause_rank.get(parent_key, 0)) - int(clause_rank.get(child_key, 0))
            margin = selected_scale * gap - float(stats.max_delta_debt)
            if margin <= 0:
                violating_edges += 1
            if worst_at_scale is None or margin < float(worst_at_scale["margin"]):
                worst_at_scale = {
                    "parent_clause": encode_key(parent_key),
                    "child_clause": encode_key(child_key),
                    "rank_gap": gap,
                    "max_delta_debt": round_float(stats.max_delta_debt),
                    "margin": round_float(margin),
                    "example": compact_example(stats.example),
                }
            min_margin = min(min_margin, margin)

    if impossible_rows:
        interval_status = "same_clause_counteredge_blocks_rank_measure"
    elif not feasible:
        interval_status = "opposing_scale_bounds_block_rank_measure"
    else:
        interval_status = "scale_interval_feasible"

    return {
        "status": interval_status,
        "low_exclusive": round_float(low_exclusive),
        "high_exclusive": "infinity" if math.isinf(high_exclusive) else round_float(high_exclusive),
        "min_integer_scale": min_integer_scale,
        "max_integer_scale": max_integer_scale,
        "selected_scale": selected_scale,
        "min_margin_at_selected_scale": (
            round_float(min_margin) if selected_scale is not None and min_margin != float("inf") else None
        ),
        "violating_clause_edge_count_at_selected_scale": violating_edges,
        "impossible_rows": impossible_rows[:8],
        "worst_at_selected_scale": worst_at_scale,
    }


def pressure_cycle_examples(
    clause_edges: dict[tuple[ClauseKey, ClauseKey], ClauseEdgeStats],
    limit: int = 8,
) -> list[dict[str, Any]]:
    rows = []
    for (parent_key, child_key), stats in clause_edges.items():
        if stats.max_delta_debt < 0:
            continue
        if parent_key == child_key:
            rows.append(
                {
                    "kind": "same_clause_pressure_loop",
                    "parent_clause": encode_key(parent_key),
                    "child_clause": encode_key(child_key),
                    "max_delta_debt": round_float(stats.max_delta_debt),
                    "count": stats.count,
                    "example": compact_example(stats.example),
                }
            )
    rows.sort(key=lambda row: (-float(row["max_delta_debt"]), -int(row["count"])))
    return rows[:limit]


def analyze_clause_family(snapshot: LiftSnapshot, family: ClauseFamily) -> dict[str, Any]:
    clause_nodes, clause_edges, pressure_adjacency = build_clause_graph(snapshot, family)
    pressure_edges = {
        edge: stats
        for edge, stats in clause_edges.items()
        if stats.max_delta_debt >= 0
    }
    pressure_topology, pressure_rank = topological_rank(pressure_adjacency, clause_nodes)
    same_clause_pressure = pressure_cycle_examples(clause_edges)
    if pressure_topology.get("cycle_detected"):
        status = "pressure_cycle_counterexample_refutes_clause_rank"
        scale_interval = {
            "status": "not_attempted_pressure_graph_cyclic",
            "proof_boundary": "A nonnegative-pressure cycle in the clause graph blocks any scalar rank on this clause family.",
        }
    else:
        scale_interval = scale_interval_for_clause_rank(clause_edges, pressure_rank)
        if scale_interval["status"] == "scale_interval_feasible":
            status = (
                "sampled_exact_template_clause_rank_found_not_horizon_independent"
                if family.name == "phase_tail_residue256_vexact"
                else "sampled_symbolic_clause_rank_found_not_proof"
            )
        elif scale_interval["status"] == "same_clause_counteredge_blocks_rank_measure":
            status = "same_clause_counteredge_refutes_clause_rank"
        else:
            status = "not_certified_by_symbolic_clause_scale_interval"

    return {
        "clause_family": family.name,
        "description": family.description,
        "proof_intent": family.proof_intent,
        "status": status,
        "clause_count": len(clause_nodes),
        "clause_edge_count": len(clause_edges),
        "pressure_clause_edge_count": len(pressure_edges),
        "same_clause_pressure_loop_count": sum(1 for edge in pressure_edges if edge[0] == edge[1]),
        "pressure_topology": pressure_topology,
        "scale_interval": scale_interval,
        "same_clause_pressure_examples": same_clause_pressure,
        "interpretation": (
            "This refutes or supports only the named symbolic clause family on the bounded template graph. It is "
            "not a proof or disproof of Collatz."
        ),
    }


def compare_clause_extension(
    previous: LiftSnapshot,
    current: LiftSnapshot,
    family: ClauseFamily,
) -> dict[str, Any]:
    prev_nodes, prev_edges, prev_pressure = build_clause_graph(previous, family)
    curr_nodes, curr_edges, curr_pressure = build_clause_graph(current, family)
    prev_pressure_edges = {
        edge
        for edge, stats in prev_edges.items()
        if stats.max_delta_debt >= 0
    }
    curr_pressure_edges = {
        edge
        for edge, stats in curr_edges.items()
        if stats.max_delta_debt >= 0
    }
    new_clause_edges = set(curr_edges) - set(prev_edges)
    new_pressure_edges = curr_pressure_edges - prev_pressure_edges
    new_same_clause_pressure = [
        edge
        for edge in new_pressure_edges
        if edge[0] == edge[1]
    ]
    return {
        "clause_family": family.name,
        "from_max_bits": previous.max_bits,
        "to_max_bits": current.max_bits,
        "previous_clause_count": len(prev_nodes),
        "current_clause_count": len(curr_nodes),
        "new_clause_count": len(curr_nodes - prev_nodes),
        "previous_clause_edge_count": len(prev_edges),
        "current_clause_edge_count": len(curr_edges),
        "new_clause_edge_count": len(new_clause_edges),
        "previous_pressure_clause_edge_count": sum(len(children) for children in prev_pressure.values()),
        "current_pressure_clause_edge_count": sum(len(children) for children in curr_pressure.values()),
        "new_pressure_clause_edge_count": len(new_pressure_edges),
        "new_same_clause_pressure_edge_count": len(new_same_clause_pressure),
        "closure_status": (
            "symbolic_clause_relation_changes_under_horizon_extension"
            if new_clause_edges or new_pressure_edges or (curr_nodes - prev_nodes)
            else "not_refuted_in_this_extension"
        ),
        "new_pressure_examples": [
            {
                "parent_clause": encode_key(edge[0]),
                "child_clause": encode_key(edge[1]),
                "max_delta_debt": round_float(curr_edges[edge].max_delta_debt),
                "count": curr_edges[edge].count,
                "example": compact_example(curr_edges[edge].example),
            }
            for edge in sorted(
                new_pressure_edges,
                key=lambda edge: curr_edges[edge].max_delta_debt,
                reverse=True,
            )[:8]
        ],
    }


def collatz_attempt() -> dict[str, Any]:
    snapshots = build_lift_snapshots(base_bits=12, max_bits=28, checkpoints=(25, 26, 27, 28))
    previous = snapshots[25]
    current = snapshots[26]
    phase_wrap_previous = snapshots[27]
    phase_wrap_current = snapshots[28]
    topology, template_rank = topological_rank(current.adjacency, current.nodes)
    rank_measure = synthesize_rank_debt_measure(current, template_rank) if template_rank else {"status": "no_rank"}
    clause_trials = [analyze_clause_family(current, family) for family in CLAUSE_FAMILIES]
    extension_rows = [compare_clause_extension(previous, current, family) for family in CLAUSE_FAMILIES]
    phase_family = CLAUSE_FAMILIES[0]
    phase_wrap_trial = analyze_clause_family(phase_wrap_current, phase_family)
    phase_wrap_extension = compare_clause_extension(phase_wrap_previous, phase_wrap_current, phase_family)
    phase_wrap_probe = {
        "purpose": "Test the tempting phase-only rank after the modulo-16 phase wrap becomes visible.",
        "from_max_bits": phase_wrap_previous.max_bits,
        "to_max_bits": phase_wrap_current.max_bits,
        "analysis": phase_wrap_trial,
        "extension": phase_wrap_extension,
        "interpretation": (
            "Phase-only rank is a useful trap: it passes through 26 and 27 bits, but the 28-bit edge from phase 11 "
            "back to phase 12 closes a nonnegative-pressure cycle and refutes phase-only scalar rank."
        ),
    }
    refuted = [row for row in clause_trials if "refutes" in row["status"]]
    future_refuted = 1 if "refutes" in phase_wrap_trial["status"] else 0
    sampled = [row for row in clause_trials if "found_not" in row["status"]]
    exact_template = next(row for row in clause_trials if row["clause_family"] == "phase_tail_residue256_vexact")
    exact_extension = next(row for row in extension_rows if row["clause_family"] == "phase_tail_residue256_vexact")
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-45",
        "route": "SymbolicRankClauseOrFutureCounteredge",
        "status": "proof_pressure_open",
        "proof_or_counterexample_mode": "symbolic-clause rank cegis",
        "attempt": (
            "Replace the horizon-specific rank table with explicit symbolic clause families. A family is discarded "
            "when nonnegative-pressure edges force a same-clause loop or a pressure cycle; it is retained only if "
            "a bounded rank-plus-debt certificate survives the sampled edges."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-44",
            "symbolic_rank_clause_audit": {
                "family": FAMILY,
                "max_bits": current.max_bits,
                "template_node_count": len(current.nodes),
                "template_edge_count": len(current.edges),
                "raw_open_edge_count": current.raw_open_edge_count,
                "template_rank_baseline": {
                    "topological_rank": topology,
                    "sampled_rank_debt_measure": rank_measure,
                },
                "clause_trials": clause_trials,
                "extension_comparisons": extension_rows,
                "phase_wrap_probe_28": phase_wrap_probe,
                "exactly_refuted_clause_family_count": len(refuted),
                "future_refuted_clause_family_count": future_refuted,
                "sampled_clause_candidate_count": len(sampled),
                "exact_template_clause_status": exact_template["status"],
                "exact_template_new_clause_count_25_to_26": exact_extension["new_clause_count"],
                "exact_template_new_pressure_edge_count_25_to_26": exact_extension["new_pressure_clause_edge_count"],
                "route_decision": {
                    "discard": [
                        "phase-only rank as a Collatz proof measure after the 28-bit phase-wrap pressure cycle appears",
                        "coarse feature clauses as Collatz proof measures when scale intervals are empty or unstable",
                        "any symbolic quotient with same-clause nonnegative-pressure loops",
                        "the observed exact-template rank table as an infinite theorem without future-clause closure",
                    ],
                    "retain": [
                        "pressure-cycle extraction as a fast refuter for proposed symbolic clauses",
                        "exact observed-template rank as a bounded ceiling certificate",
                        "a future symbolic family whose pressure graph is acyclic and stable under horizon extension",
                    ],
                },
                "closed_bounded_statement": (
                    "Phase-only rank passes the sampled rank-plus-debt interval through 26 and 27 bits, then is "
                    "refuted at 28 bits when the phase-wrap edge closes a nonnegative-pressure cycle. Richer finite "
                    "clause families remain uncertified at 26 bits, while the observed template rank remains a "
                    "bounded ceiling certificate only."
                ),
                "proof_boundary": (
                    "No Collatz proof and no Collatz counterexample. TICKET45 refutes several symbolic clause "
                    "abstractions and preserves only the need for a stable future symbolic rank or a future edge "
                    "that refutes it."
                ),
            },
        },
        "obstruction": (
            f"The tempting phase-only symbolic rank is refuted by the {phase_wrap_extension['from_max_bits']}->"
            f"{phase_wrap_extension['to_max_bits']} wrap edge; the exact observed-template clause family has "
            f"status {exact_template['status']} and the 25->26 extension still adds "
            f"{exact_extension['new_clause_count']} clauses plus "
            f"{exact_extension['new_pressure_clause_edge_count']} nonnegative-pressure clause edges."
        ),
        "candidate_theorem": (
            "There exists a finite symbolic clause family, stable under all future lifts, whose nonnegative-pressure "
            "graph is acyclic and whose rank-plus-debt scale interval is nonempty for every lifted edge."
        ),
        "next_experiment": (
            "Generate TICKET46 by searching for a parametric clause grammar that is stable from 25->26 and then "
            "testing whether the pressure graph remains acyclic at 27 bits or yields a new counteredge."
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
        "proof_or_counterexample_mode": "symbolic-clause counteredge transfer",
        "attempt": (
            "Transfer TICKET45's rule: a visual, numerical, or quotient pattern may be promoted only after its "
            "symbolic clauses survive same-clause pressure loops, pressure-cycle extraction, and future-lift closure."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior["route"],
            "discarded_shortcut": discarded_shortcut,
            "retained_target": retained_target,
            "counterexample_target": counterexample_target,
            "ticket45_transfer": route,
        },
        "obstruction": (
            "The current artifact gives a sharper falsification protocol for proof candidates, but it does not close "
            "the infinite theorem and it does not produce a certified counterexample."
        ),
        "candidate_theorem": retained_target,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket44-feature-measure-counteredge-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-45",
            "SymbolicZeroClauseOrOffCriticalCounteredge",
            "finite zero-feature quotient treated as RH",
            "A stable symbolic zero-clause grammar has no off-critical pressure cycle and yields a positive-kernel margin.",
            "an off-critical zero-lift pressure cycle or same-clause nonpositive kernel loop",
            "Search symbolic zero clauses for pressure cycles before promoting any kernel-rank candidate.",
        ),
        collatz_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-45",
            "SymbolicMarginClauseOrExceptionalCounteredge",
            "finite margin quotient treated as Goldbach",
            "A stable symbolic margin-clause grammar keeps every large even-integer pressure edge in an acyclic positive cone.",
            "an exceptional-residue pressure cycle or same-clause margin loop",
            "Search margin clauses for pressure cycles before promoting any explicit cutoff candidate.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-45",
            "SymbolicExactGapClauseOrLeakageCounteredge",
            "finite exact-gap quotient treated as twin-prime infinitude",
            "A stable exact-gap symbolic grammar separates gap-2 mass from wider-gap leakage without pressure cycles.",
            "a leakage pressure cycle or same-clause exact-gap loss loop",
            "Search exact-gap clauses for pressure cycles before promoting any gap-selector candidate.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "symbolic_rank_clause_open_no_resolution",
        "claim_boundary": (
            "Ticket 45 refutes weak symbolic clause families and preserves only stable-clause theorem targets. It "
            "does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket45-symbolic-rank-clause-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-45-symbolic-zero-clause.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-45-symbolic-rank-clause.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-45-symbolic-margin-clause.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-45-symbolic-gap-clause.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
