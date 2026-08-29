from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket254-diagonal-weighted-reflection-thue.v1"
AUDIT_KEY = "diagonal_weighted_reflection_thue_audit"
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


def verify_ticket254_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket254-diagonal-weighted-reflection-thue.json"
    if not integrated.exists():
        return "missing TICKET-254 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-254 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-254 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    expected_machine = {
        "exact_theorem_count": 4,
        "new_partial_theorem_count": 2,
        "exact_no_go_count": 2,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "goldbach",
        "stagnated_problem_count": 0,
        "riemann_block_case_count": 8,
        "collatz_detector_case_count": 48,
        "collatz_weighted_case_count": 12,
        "goldbach_reflection_certificate_count": 50,
        "twin_thue_polynomial_count": 17,
        "twin_thue_grid_case_count": 10608,
        "total_failure_count": 0,
    }
    for key, expected_value in expected_machine.items():
        if root.get("machine_audit", {}).get(key) != expected_value:
            return f"TICKET-254 machine field changed: {key}"
    expected = {
        "riemann": ("riemann", "PositiveDiagonalDirichletPacketDominationNoGo", "exact_no_go", "ActualWeilDirichletBlocksHaveUniformStrictDiagonalDominance", "0be64af7360d626405108d0fee5944f6132fdb6065fd57690c657f3e160df05c"),
        "collatz": ("collatz", "NonnegativeCrossPrimeCompleteDetectorAverageNoGo", "exact_no_go", "IncompleteSlopeCharacterKernelHasSignedRecoveryAndCrossPrimeCancellation", "6ce9f4399b2372016d2c0bb7d9aa02e8bc14b7b5ee124687ba55c6f76638be46"),
        "goldbach": ("goldbach", "EvenCyclotomicReflectionPrimePrefixExclusion", "partial_theorem", "OddOrQDivisibleCompatibleTailPrimePrefixExclusion", "253518284e5b939aa42449fd309978e3fe0c7bda7d83944ee96217eed38394f6"),
        "twin_prime": ("twin-prime", "ExponentSeventeenUnitTwistedThueReduction", "partial_theorem", "AllSeventeenUnitTwistedCoefficientOneThueEquationsHaveNoAdmissibleIntegralPoint", "1cc60a2de6cbf63644bb1751a558602cdf696651b181a1a14606b62ec457fcf3"),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-254-positive-diagonal-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-254-weighted-complete-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-254-even-reflection-exclusion.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-254-exponent17-thue.json",
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
            return f"TICKET-254 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-254 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-254 open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-254 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-254 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-254 track JSON changed: {key}"
    state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
    if (
        state.get("ticket") != 254
        or state.get("parent_ticket") != 253
        or state.get("deep_focus_problem") != "goldbach"
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
    ):
        return "TICKET-254 persistent research state changed"
    for report in (
        ROOT / "docs/diagonal-weighted-reflection-thue.md",
        ROOT / "docs/diagonal-weighted-reflection-thue.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-254 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket254_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-254 structure verification passed")
