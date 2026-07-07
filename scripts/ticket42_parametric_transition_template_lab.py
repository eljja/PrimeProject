from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from typing import Any

from ticket30_potential_synthesis_lab import LOG2_3, ROOT, find_attempt, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, round_float, transition_label


GENERATED_AT = "2026-07-08T18:05:00+09:00"
SCHEMA = "primeproject.ticket42-parametric-transition-template-lab.v1"


def word_tuple(certificate: dict[str, Any]) -> tuple[int, ...]:
    return tuple(int(value) for value in certificate.get("prefix_word", []))


def debt(certificate: dict[str, Any]) -> float:
    return LOG2_3 * int(certificate.get("prefix_length", 0)) - int(certificate.get("consumed_bits", 0))


def clipped(value: int, cap: int) -> int | str:
    return value if value < cap else f">={cap}"


def template_key(certificate: dict[str, Any], family: str) -> tuple[Any, ...]:
    bits = int(certificate.get("modulus_bits", 0))
    residue = int(certificate.get("residue", 0))
    next_valuation = int(certificate.get("next_valuation", 0))
    word = word_tuple(certificate)
    phase = bits % 16

    if family == "phase16_tail2_residue64_v8":
        return (phase, word[-2:], residue % 64, clipped(next_valuation, 8))
    if family == "phase16_tail3_residue128_v12":
        return (phase, word[-3:], residue % 128, clipped(next_valuation, 12))
    if family == "phase16_tail4_residue256_v16":
        return (phase, word[-4:], residue % 256, clipped(next_valuation, 16))
    if family == "phase16_tail4_residue256_vexact":
        return (phase, word[-4:], residue % 256, next_valuation)
    raise ValueError(family)


def stringify_key(key: tuple[Any, ...], limit: int = 180) -> str:
    text = json.dumps(key, ensure_ascii=False, separators=(",", ":"))
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def edge_delta(parent: dict[str, Any], child: dict[str, Any]) -> dict[str, Any]:
    parent_prefix = int(parent.get("prefix_length", 0))
    child_prefix = int(child.get("prefix_length", 0))
    parent_consumed = int(parent.get("consumed_bits", 0))
    child_consumed = int(child.get("consumed_bits", 0))
    delta_prefix = child_prefix - parent_prefix
    delta_consumed = child_consumed - parent_consumed
    return {
        "delta_prefix": delta_prefix,
        "delta_consumed": delta_consumed,
        "delta_next_valuation": int(child.get("next_valuation", 0)) - int(parent.get("next_valuation", 0)),
        "delta_debt": round_float(delta_prefix * LOG2_3 - delta_consumed),
    }


@dataclass
class EdgeStats:
    count: int = 0
    min_delta_debt: float = 0.0
    max_delta_debt: float = 0.0
    delta_signature_counts: Counter[tuple[int, int]] = field(default_factory=Counter)
    example: dict[str, Any] | None = None
    max_debt_example: dict[str, Any] | None = None

    def add(self, delta: dict[str, Any], example: dict[str, Any]) -> None:
        value = float(delta["delta_debt"])
        signature = (int(delta["delta_prefix"]), int(delta["delta_consumed"]))
        if self.count == 0:
            self.min_delta_debt = value
            self.max_delta_debt = value
            self.example = example
            self.max_debt_example = example
        else:
            self.min_delta_debt = min(self.min_delta_debt, value)
            if value > self.max_delta_debt:
                self.max_delta_debt = value
                self.max_debt_example = example
        self.delta_signature_counts[signature] += 1
        self.count += 1


class TemplateAuditor:
    def __init__(self, family: str) -> None:
        self.family = family
        self.nodes: set[tuple[Any, ...]] = set()
        self.edges: dict[tuple[tuple[Any, ...], tuple[Any, ...]], EdgeStats] = {}
        self.adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]] = defaultdict(set)
        self.raw_edge_count = 0
        self.raw_nondecreasing_debt_edges = 0
        self.nondecreasing_examples: list[dict[str, Any]] = []
        self.delta_signature_totals: Counter[tuple[int, int]] = Counter()

    def add_edge(
        self,
        parent: dict[str, Any],
        child: dict[str, Any],
        *,
        bits: int,
        direction: str,
        label: str,
    ) -> None:
        parent_key = template_key(parent, self.family)
        child_key = template_key(child, self.family)
        delta = edge_delta(parent, child)
        example = {
            "bits": bits,
            "direction": direction,
            "label": label,
            "parent_residue": parent.get("residue"),
            "child_residue": child.get("residue"),
            "parent_template": stringify_key(parent_key),
            "child_template": stringify_key(child_key),
            **delta,
        }
        self.nodes.add(parent_key)
        self.nodes.add(child_key)
        self.adjacency[parent_key].add(child_key)
        stats = self.edges.setdefault((parent_key, child_key), EdgeStats())
        stats.add(delta, example)
        self.raw_edge_count += 1
        self.delta_signature_totals[(int(delta["delta_prefix"]), int(delta["delta_consumed"]))] += 1
        if float(delta["delta_debt"]) >= 0.0:
            self.raw_nondecreasing_debt_edges += 1
            if len(self.nondecreasing_examples) < 8:
                self.nondecreasing_examples.append(example)

    def graph_summary(self) -> dict[str, Any]:
        scc = strongly_connected_components(self.nodes, self.adjacency)
        cyclic_components = [
            component
            for component in scc
            if len(component) > 1 or any(child == component[0] for child in self.adjacency.get(component[0], set()))
        ]
        largest = max((len(component) for component in cyclic_components), default=0)
        cyclic_node_count = sum(len(component) for component in cyclic_components)
        cycle = first_cycle_example(cyclic_components, self.adjacency, self.edges)
        greedy = greedy_nondecreasing_cycle(self.nodes, self.adjacency, self.edges)
        ambiguous_pairs = [
            (edge, stats)
            for edge, stats in self.edges.items()
            if len(stats.delta_signature_counts) > 1
            or round_float(stats.max_delta_debt - stats.min_delta_debt) > 0.0
        ]
        return {
            "family": self.family,
            "template_node_count": len(self.nodes),
            "template_edge_count": len(self.edges),
            "raw_open_edge_count": self.raw_edge_count,
            "raw_nondecreasing_debt_edge_count": self.raw_nondecreasing_debt_edges,
            "raw_nondecreasing_debt_rate": round_float(self.raw_nondecreasing_debt_edges / max(self.raw_edge_count, 1)),
            "delta_signature_totals": {
                f"dp={signature[0]},dc={signature[1]}": count
                for signature, count in sorted(self.delta_signature_totals.items())
            },
            "scc_count": len(scc),
            "cyclic_component_count": len(cyclic_components),
            "cyclic_template_node_count": cyclic_node_count,
            "largest_cyclic_component_size": largest,
            "strict_template_rank_status": (
                "refuted_by_template_cycle"
                if cyclic_components
                else "not_refuted_in_sampled_template_graph"
            ),
            "ambiguous_template_edge_count": len(ambiguous_pairs),
            "ambiguous_template_edge_examples": [
                {
                    "parent_template": stringify_key(edge[0]),
                    "child_template": stringify_key(edge[1]),
                    "count": stats.count,
                    "min_delta_debt": round_float(stats.min_delta_debt),
                    "max_delta_debt": round_float(stats.max_delta_debt),
                    "delta_signatures": {
                        f"dp={signature[0]},dc={signature[1]}": count
                        for signature, count in sorted(stats.delta_signature_counts.items())
                    },
                    "example": stats.example,
                    "max_debt_example": stats.max_debt_example,
                }
                for edge, stats in ambiguous_pairs[:6]
            ],
            "cycle_example": cycle,
            "greedy_nondecreasing_cycle_probe": greedy,
            "nondecreasing_debt_examples": self.nondecreasing_examples,
            "interpretation": (
                "A strict rank on this finite template quotient is blocked by a directed template cycle. "
                "The cycle is not a Collatz counterexample unless a compatible infinite lift is proved."
                if cyclic_components
                else "No directed cycle was seen in this sampled template quotient, but unseen parametric lifts remain open."
            ),
        }


def strongly_connected_components(
    nodes: set[tuple[Any, ...]],
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]],
) -> list[list[tuple[Any, ...]]]:
    visited: set[tuple[Any, ...]] = set()
    order: list[tuple[Any, ...]] = []

    for start in nodes:
        if start in visited:
            continue
        stack: list[tuple[tuple[Any, ...], bool]] = [(start, False)]
        while stack:
            node, expanded = stack.pop()
            if expanded:
                order.append(node)
                continue
            if node in visited:
                continue
            visited.add(node)
            stack.append((node, True))
            for child in adjacency.get(node, set()):
                if child not in visited:
                    stack.append((child, False))

    reverse: dict[tuple[Any, ...], set[tuple[Any, ...]]] = defaultdict(set)
    for parent, children in adjacency.items():
        for child in children:
            reverse[child].add(parent)

    components: list[list[tuple[Any, ...]]] = []
    assigned: set[tuple[Any, ...]] = set()
    for start in reversed(order):
        if start in assigned:
            continue
        component: list[tuple[Any, ...]] = []
        stack = [start]
        assigned.add(start)
        while stack:
            node = stack.pop()
            component.append(node)
            for parent in reverse.get(node, set()):
                if parent not in assigned:
                    assigned.add(parent)
                    stack.append(parent)
        components.append(component)
    return components


def first_cycle_example(
    cyclic_components: list[list[tuple[Any, ...]]],
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]],
    edges: dict[tuple[tuple[Any, ...], tuple[Any, ...]], EdgeStats],
) -> dict[str, Any]:
    for component in sorted(cyclic_components, key=len):
        component_set = set(component)
        for parent in component:
            for child in adjacency.get(parent, set()):
                if child not in component_set:
                    continue
                path = path_within_component(child, parent, component_set, adjacency, max_seen=50_000)
                if path:
                    cycle_nodes = [parent] + path
                    return summarize_cycle(cycle_nodes, edges, "directed_template_cycle")
    return {"status": "no_cycle_example_found"}


def path_within_component(
    start: tuple[Any, ...],
    target: tuple[Any, ...],
    component: set[tuple[Any, ...]],
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]],
    max_seen: int,
) -> list[tuple[Any, ...]]:
    queue: deque[tuple[Any, ...]] = deque([start])
    parent: dict[tuple[Any, ...], tuple[Any, ...] | None] = {start: None}
    while queue and len(parent) <= max_seen:
        node = queue.popleft()
        if node == target:
            out: list[tuple[Any, ...]] = []
            current: tuple[Any, ...] | None = node
            while current is not None:
                out.append(current)
                current = parent[current]
            return list(reversed(out))
        for child in adjacency.get(node, set()):
            if child not in component or child in parent:
                continue
            parent[child] = node
            queue.append(child)
    return []


def greedy_nondecreasing_cycle(
    nodes: set[tuple[Any, ...]],
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]],
    edges: dict[tuple[tuple[Any, ...], tuple[Any, ...]], EdgeStats],
) -> dict[str, Any]:
    outgoing_best = {
        node: sorted(
            adjacency.get(node, set()),
            key=lambda child: edges[(node, child)].max_delta_debt,
            reverse=True,
        )
        for node in nodes
    }
    starts = sorted(
        (node for node in nodes if outgoing_best.get(node)),
        key=lambda node: edges[(node, outgoing_best[node][0])].max_delta_debt,
        reverse=True,
    )
    best_cycle: dict[str, Any] | None = None
    for start in starts[:5000]:
        seen: dict[tuple[Any, ...], int] = {}
        path: list[tuple[Any, ...]] = []
        node = start
        for _ in range(128):
            if node in seen:
                cycle_nodes = path[seen[node] :] + [node]
                summary = summarize_cycle(cycle_nodes, edges, "greedy_max_debt_template_cycle")
                if best_cycle is None or float(summary.get("total_delta_debt", -9999.0)) > float(best_cycle.get("total_delta_debt", -9999.0)):
                    best_cycle = summary
                if float(summary.get("total_delta_debt", -9999.0)) >= 0.0:
                    summary["status"] = "nondecreasing_template_cycle_found"
                    return summary
                break
            choices = outgoing_best.get(node)
            if not choices:
                break
            seen[node] = len(path)
            path.append(node)
            node = choices[0]
    if best_cycle is not None:
        best_cycle["status"] = "cycle_found_but_total_debt_decreases_in_probe"
        return best_cycle
    return {"status": "no_cycle_found_by_greedy_probe"}


def summarize_cycle(
    cycle_nodes: list[tuple[Any, ...]],
    edges: dict[tuple[tuple[Any, ...], tuple[Any, ...]], EdgeStats],
    status: str,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    total_prefix = 0
    total_consumed = 0
    total_debt = 0.0
    for left, right in zip(cycle_nodes, cycle_nodes[1:]):
        stats = edges.get((left, right))
        if stats is None:
            continue
        example = stats.max_debt_example or stats.example or {}
        total_prefix += int(example.get("delta_prefix", 0))
        total_consumed += int(example.get("delta_consumed", 0))
        total_debt += float(example.get("delta_debt", 0.0))
        rows.append(
            {
                "parent_template": stringify_key(left),
                "child_template": stringify_key(right),
                "max_delta_debt": round_float(stats.max_delta_debt),
                "count": stats.count,
                "example": example,
            }
        )
    return {
        "status": status,
        "cycle_length": len(rows),
        "total_delta_prefix": total_prefix,
        "total_delta_consumed": total_consumed,
        "total_delta_debt": round_float(total_debt),
        "mean_delta_debt": round_float(total_debt / max(len(rows), 1)),
        "nodes": [stringify_key(node) for node in cycle_nodes[:18]],
        "edges": rows[:18],
        "proof_boundary": (
            "This is a cycle in an abstract template quotient, not a verified infinite Collatz trajectory. "
            "It blocks a proof that ranks only these finite templates; a real counterexample would require a "
            "compatible infinite lift of the cycle."
        ),
    }


def template_audit(base_bits: int = 12, max_bits: int = 26) -> dict[str, Any]:
    families = [
        "phase16_tail2_residue64_v8",
        "phase16_tail3_residue128_v12",
        "phase16_tail4_residue256_v16",
        "phase16_tail4_residue256_vexact",
    ]
    auditors = [TemplateAuditor(family) for family in families]
    frontier = [residue for residue in range(1, 1 << base_bits, 2)]
    level_rows: list[dict[str, Any]] = []
    transition_totals: Counter[str] = Counter()

    for bits in range(base_bits, max_bits):
        next_frontier: list[int] = []
        level_counts: Counter[str] = Counter()
        for residue in frontier:
            parent = cert(residue, bits)
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            low_open = low.get("status") == "needs_split"
            high_open = high.get("status") == "needs_split"
            label = transition_label(low_open, high_open)
            transition_totals[label] += 1
            level_counts[label] += 1
            for direction, child_residue, child in (("low", residue, low), ("high", high_residue, high)):
                if child.get("status") != "needs_split":
                    continue
                next_frontier.append(child_residue)
                for auditor in auditors:
                    auditor.add_edge(parent, child, bits=bits, direction=direction, label=label)
        level_rows.append(
            {
                "bits": bits,
                "parent_frontier_count": len(frontier),
                "next_frontier_count": len(next_frontier),
                "transition_counts": dict(sorted(level_counts.items())),
                "survival_ratio": round_float(len(next_frontier) / max(2 * len(frontier), 1)),
            }
        )
        frontier = next_frontier

    family_rows = [auditor.graph_summary() for auditor in auditors]
    sharp = family_rows[-1]
    any_cycle = any(row.get("cyclic_component_count", 0) for row in family_rows)
    total_ambiguous = sum(int(row.get("ambiguous_template_edge_count", 0)) for row in family_rows)
    return {
        "base_bits": base_bits,
        "max_bits": max_bits,
        "template_families": families,
        "transition_totals": dict(sorted(transition_totals.items())),
        "tail_level_rows": level_rows[-5:],
        "family_rows": family_rows,
        "parametric_schema": {
            "state_variables": [
                "phase = bits mod 16",
                "tail valuation word",
                "residue modulo 2^m",
                "next 2-adic valuation",
                "prefix_length",
                "consumed_bits",
                "debt = prefix_length * log2(3) - consumed_bits",
            ],
            "template_update": [
                "phase' = phase + 1 mod 16",
                "prefix_length' = prefix_length + delta_prefix",
                "consumed_bits' = consumed_bits + delta_consumed",
                "debt' = debt + delta_prefix * log2(3) - delta_consumed",
                "tail' = suffix(tail plus newly consumed valuation word)",
            ],
            "missing_lift_theorem": (
                "For every abstract template edge, prove exactly which larger cylinders instantiate it, or reject "
                "the edge as a quotient artifact."
            ),
        },
        "route_decision": {
            "discard": [
                "absence of sampled template cycles treated as a Collatz proof",
                "template cycle interpreted directly as a Collatz counterexample without a compatible lift",
                "finite template edge treated as deterministic without delta guards for prefix, consumed bits, and debt",
                "larger bounded horizon treated as a substitute for parametric lift closure",
            ],
            "retain": [
                "parametric transition schema with prefix_length, consumed_bits, and debt deltas",
                "cycle-lift search for a compatible infinite nondecreasing template ray",
                "well-founded measure that uses growth coordinates, not only the finite template node",
            ],
        },
        "closed_bounded_statement": (
            "Through the sampled 26-bit frontier, no directed cycle was found in the tested template quotients. "
            "This keeps the template-rank route alive as bounded evidence, but it is not a proof because future "
            "lift closure and ambiguous coordinate deltas remain unproved."
        ),
        "cycle_search_status": (
            "sampled_template_cycle_found"
            if any_cycle
            else "no_sampled_template_cycle_found_through_26_bits"
        ),
        "total_ambiguous_template_edge_count": total_ambiguous,
        "sharp_family_status": sharp["strict_template_rank_status"],
        "proof_boundary": (
            "This is not a Collatz proof and not a Collatz counterexample. It preserves a useful proof route "
            "because no sampled template cycle was found, but it rejects the shortcut from bounded acyclicity to "
            "truth. A proof now needs a parametric lift theorem plus a well-founded measure, while a disproof "
            "attempt needs a compatible infinite lift of a nondecreasing cycle."
        ),
    }


def collatz_attempt() -> dict[str, Any]:
    audit = template_audit()
    sharp = audit["family_rows"][-1]
    greedy = sharp.get("greedy_nondecreasing_cycle_probe", {})
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-42",
        "status": "proof_pressure_open",
        "route": "ParametricTransitionTemplateOrNondecreasingCycle",
        "proof_or_counterexample_mode": "template_rank_refutation_and_cycle_lift_search",
        "attempt": (
            "Continue from Ticket 41 by replacing fixed-window state graphs with finite transition templates. "
            "Then attack the proposed proof route: if a template quotient cycles, no strict rank can depend only "
            "on that finite template node. If a nondecreasing cycle also has a compatible infinite lift, it becomes "
            "a real counterexample target."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-41",
            "parametric_transition_template_audit": audit,
        },
        "obstruction": (
            f"The sharp sampled family has {sharp['template_node_count']} template nodes, "
            f"{sharp['template_edge_count']} template edges, and status {sharp['strict_template_rank_status']}. "
            f"No template cycle was found by the sampled probe, but {sharp['ambiguous_template_edge_count']} sharp "
            "template edges have multiple coordinate deltas. The proof route therefore moves from finite acyclicity "
            f"to parametric lift closure; the greedy cycle probe reports {greedy.get('status')}."
        ),
        "candidate_theorem": (
            "Every reachable open-frontier transition is an instance of a parametric template edge and there exists "
            "a well-founded measure on template plus growth coordinates that strictly decreases on every instance; "
            "otherwise a compatible infinite nondecreasing template cycle is the counterexample target."
        ),
        "next_experiment": (
            "No sampled template cycle was found through the audited horizon. The next step is therefore not "
            "cycle lifting, but lift-closure plus a well-founded measure: prove that every future cylinder lift "
            "preserves the template rank/debt descent, or find a future lift that breaks every such measure."
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
    source_attempt = find_attempt(source, problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "parametric_template_or_counterexample_transfer",
        "attempt": (
            "Transfer Ticket 42's lesson: finite template probes are useful, but neither cycle absence nor bounded "
            "acyclicity proves the target while growth coordinates remain unclosed. The useful object is either a "
            "parametric lift theorem with a well-founded measure, or a compatible escaping cycle that becomes a "
            "counterexample target."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "discarded_shortcut": discarded_shortcut,
            "retained_target": retained_target,
            "counterexample_target": counterexample_target,
        },
        "obstruction": (
            "The template layer can contain cycles after finite coordinates are hidden. This blocks any proof that "
            "uses only the finite quotient, but it does not produce a counterexample until the cycle is lifted to "
            "a compatible infinite object."
        ),
        "candidate_theorem": retained_target,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket41-rank-escape-normalization-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-42",
            "ParametricZeroTemplateOrOffCriticalCycle",
            "finite zero-state template rank without height/tail growth coordinates",
            (
                "Every off-critical zero configuration has a parametric explicit-formula template lift whose "
                "positivity measure decreases across all height extensions."
            ),
            "a compatible off-critical zero-template cycle with nondecreasing positivity deficit",
            "Lift zero-state template cycles into explicit-formula kernel constraints and test whether any cycle can remain off the critical line.",
        ),
        collatz_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-42",
            "ParametricErrorTemplateOrExceptionalCycle",
            "finite error-cone template rank without cutoff-growth coordinates",
            (
                "Every sufficiently large even integer has a parametric major/minor-arc error template whose "
                "certified margin is forced positive by a well-founded measure."
            ),
            "a compatible exceptional even-integer cycle whose normalized margin stays nonpositive",
            "Lift error-cone template cycles into explicit cutoff constraints and test whether the margin can stay nonpositive.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-42",
            "ParametricGapTemplateOrLeakageCycle",
            "finite exact-gap template rank without scale/leakage growth coordinates",
            (
                "Every large scale has a parametric exact-gap template whose leakage measure leaves positive "
                "gap-2 mass after subtracting wider admissible gaps."
            ),
            "a compatible leakage cycle that absorbs exact gap-2 mass into wider gaps at every scale",
            "Lift exact-gap template cycles into parity-sensitive sieve constraints and test whether gap-2 mass can be preserved.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "parametric_template_open_no_resolution",
        "claim_boundary": (
            "Ticket 42 keeps finite template ranks as bounded candidates, rejects the shortcut from sampled "
            "acyclicity to proof, and converts the next proof/disproof target into a parametric lift problem. "
            "It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket42-parametric-transition-template-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-42-parametric-zero-template.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-42-parametric-transition-template.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-42-parametric-error-template.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-42-parametric-gap-template.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
