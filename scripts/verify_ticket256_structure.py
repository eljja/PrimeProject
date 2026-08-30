from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket256-cesaro-kernel-qdiv-gl2.v1"
AUDIT_KEY = "cesaro_kernel_qdiv_gl2_audit"
ALLOWED = {
    "proved",
    "disproved",
    "computed_finite",
    "external_theorem",
    "assumption",
    "heuristic",
    "open",
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


def verify_ticket256_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket256-cesaro-kernel-qdiv-gl2.json"
    if not integrated.exists():
        return "missing TICKET-256 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-256 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-256 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    expected_machine = {
        "exact_theorem_count": 4,
        "new_partial_theorem_count": 4,
        "exact_no_go_count": 0,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "twin_prime",
        "stagnated_problem_count": 0,
        "riemann_packet_case_count": 12,
        "collatz_prime_case_count": 22,
        "goldbach_q_divisible_scan_count": 97,
        "goldbach_bounded_certificate_count": 2,
        "twin_exact_grid_case_count": 16641,
        "twin_independent_surviving_branch_count": 1,
        "total_failure_count": 0,
    }
    for key, expected in expected_machine.items():
        if root.get("machine_audit", {}).get(key) != expected:
            return f"TICKET-256 machine field changed: {key}"
    expected = {
        "riemann": (
            "riemann",
            "ToeplitzPacketCesaroLagPartialSumCriterion",
            "ActualWeilSymmetricLagPartialSumsHaveUniformLowerBound",
            "a4d61abe3161c28b13f5f333e2fae644f2c9171107dde94d92e38adc6b8615d1",
        ),
        "collatz": (
            "collatz",
            "SharpIncompleteKernelErrorAndDecayOnlyPrimeAverage",
            "RenormalizedCanonicalSlopePhasesHaveNontrivialCrossPrimeCancellation",
            "e50be6fa63328562b64c1fa1023ad706493a60e47d84705d24aebec05d412de3",
        ),
        "goldbach": (
            "goldbach",
            "QDivisibleReflectionAsymmetryPrimePrefixExclusion",
            "EveryQDivisibleCompatibleEvenTailHasPrimePrefixReflectionAsymmetry",
            "6ded0f179c955a164110a035c40971e60b948905edbb9c3377af7ac985ef8619",
        ),
        "twin_prime": (
            "twin-prime",
            "SurvivingTwistGL2EquivalenceAndSingleAbsoluteBranchReduction",
            "SingleCoefficientOneBranchHasNoNegativeNormIntegralPoint",
            "b16cc63924090d6e214ecdaaa8c47018fced6bae337cc3445ed9cbd3a85eb7a9",
        ),
    }
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-256-cesaro-lag-criterion.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-256-sharp-incomplete-kernel.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-256-qdiv-reflection-exclusion.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-256-gl2-survivor-reduction.json",
    }
    for key, (problem_id, theorem, next_lemma, digest) in expected.items():
        section = root.get(key, {})
        if (
            section.get("problem_id") != problem_id
            or section.get("theorem_name") != theorem
            or section.get("result_classification") != "partial_theorem"
            or section.get("problem_status") != "open_not_proven"
            or section.get("route_decision", {}).get("next_single_lemma") != next_lemma
            or section.get("reproducible_computation", {}).get("transcript_sha256")
            != digest
        ):
            return f"TICKET-256 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-256 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-256 open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-256 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-256 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-256 track JSON changed: {key}"
    state = json.loads(
        (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
            encoding="utf-8"
        )
    )
    if (
        state.get("ticket", 0) < 256
        or state.get("parent_ticket") != state.get("ticket", 0) - 1
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
    ):
        return "TICKET-256 persistent research history changed"
    if state.get("ticket") == 256 and state.get("deep_focus_problem") != "twin_prime":
        return "TICKET-256 deep-focus boundary changed"
    for key, (_, theorem, _, _) in expected.items():
        if theorem not in state.get("problems", {}).get(key, {}).get("established_results", []):
            return f"TICKET-256 result missing from persistent history: {key}"
    for report in (
        ROOT / "docs/cesaro-kernel-qdiv-gl2.md",
        ROOT / "docs/cesaro-kernel-qdiv-gl2.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-256 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket256_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-256 structure verification passed")
