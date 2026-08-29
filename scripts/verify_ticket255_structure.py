from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket255-aggregate-incomplete-odd-local.v1"
AUDIT_KEY = "aggregate_incomplete_odd_local_audit"
ALLOWED = {
    "proved", "disproved", "computed_finite", "external_theorem",
    "assumption", "heuristic", "open",
}


def acyclic(nodes: list[dict], edges: list[list[str]]) -> bool:
    ids = {node.get("id") for node in nodes}
    if None in ids or len(ids) != len(nodes):
        return False
    graph = {node_id: [] for node_id in ids}
    indegree = {node_id: 0 for node_id in ids}
    for source, target in edges:
        if source not in ids or target not in ids:
            return False
        graph[source].append(target)
        indegree[target] += 1
    queue = [node_id for node_id, degree in indegree.items() if degree == 0]
    visited = 0
    while queue:
        source = queue.pop()
        visited += 1
        for target in graph[source]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return visited == len(ids)


def verify_ticket255_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket255-aggregate-incomplete-odd-local.json"
    if not integrated.exists():
        return "missing TICKET-255 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-255 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-255 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    expected_machine = {
        "exact_theorem_count": 4,
        "new_partial_theorem_count": 2,
        "exact_no_go_count": 2,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "twin_prime",
        "stagnated_problem_count": 0,
        "riemann_block_case_count": 8,
        "collatz_missing_coefficient_case_count": 48,
        "goldbach_odd_reflection_certificate_count": 4,
        "twin_local_prime_count": 3,
        "twin_locally_excluded_twist_count": 15,
        "twin_surviving_twist_count": 2,
        "total_failure_count": 0,
    }
    for key, expected in expected_machine.items():
        if root.get("machine_audit", {}).get(key) != expected:
            return f"TICKET-255 machine field changed: {key}"
    expected = {
        "riemann": ("riemann", "StrictDiagonalDominanceNecessityNoGo", "exact_no_go", "ActualWeilDirichletPacketAggregateRowSumHasRequiredLowerBound", "2ba4e6b1090ad6d74f803dc96b1762f0e0cf5057bd0f11f12ee81036d8b99493"),
        "collatz": ("collatz", "IncompleteAdditiveCharacterExactRecoveryNoGo", "exact_no_go", "SignedIncompleteSlopeKernelHasControlledCanonicalErrorAndCrossPrimeCancellation", "cc49768b5030292430f99a91e8eef1047ac66704a68a859ea1e06cd4b86a9293"),
        "goldbach": ("goldbach", "OddCyclotomicReflectionPrimePrefixExclusion", "partial_theorem", "QDivisibleCompatibleTailPrimePrefixExclusion", "ab8cb879f9a4dbdc1825584e054a56687f770fc0b6c3a40f939be7f06dc2b3fb"),
        "twin_prime": ("twin-prime", "ThreePrimeLocalObstructionReducesSeventeenTwistsToTwo", "partial_theorem", "TwoSurvivingUnitTwistsHaveNoAdmissibleIntegralPoint", "3d89ca8e3ca658a6bff44a8e532a441a2be41ac89c5d8d46b2af84d8c84a6a63"),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-255-strict-dominance-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-255-incomplete-recovery-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-255-odd-reflection-exclusion.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-255-three-prime-local-obstruction.json",
    }
    for key, (problem_id, theorem, classification, next_lemma, digest) in expected.items():
        section = root.get(key, {})
        if (
            section.get("problem_id") != problem_id
            or section.get("theorem_name") != theorem
            or section.get("result_classification") != classification
            or section.get("problem_status") != "open_not_proven"
            or section.get("route_decision", {}).get("next_single_lemma") != next_lemma
            or section.get("reproducible_computation", {}).get("transcript_sha256") != digest
        ):
            return f"TICKET-255 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-255 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-255 open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-255 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-255 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-255 track JSON changed: {key}"
    state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
    if (
        state.get("ticket") != 255
        or state.get("parent_ticket") != 254
        or state.get("deep_focus_problem") != "twin_prime"
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
    ):
        return "TICKET-255 persistent research state changed"
    for report in (
        ROOT / "docs/aggregate-incomplete-odd-local.md",
        ROOT / "docs/aggregate-incomplete-odd-local.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-255 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket255_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-255 structure verification passed")
