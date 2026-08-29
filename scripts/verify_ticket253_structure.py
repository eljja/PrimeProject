from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket253-density-character-prefix-lebesgue.v1"
AUDIT_KEY = "density_character_prefix_lebesgue_audit"
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


def verify_ticket253_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket253-density-character-prefix-lebesgue.json"
    if not integrated.exists():
        return "missing TICKET-253 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-253 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-253 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    expected_machine = {
        "exact_theorem_count": 4,
        "new_partial_theorem_count": 3,
        "exact_no_go_count": 1,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "twin_prime",
        "stagnated_problem_count": 0,
        "riemann_density_packet_case_count": 11,
        "collatz_character_case_count": 12,
        "goldbach_prime_prefix_case_count": 10,
        "twin_remaining_prime_exponent_count": 84,
        "total_failure_count": 0,
    }
    for key, expected in expected_machine.items():
        if root.get("machine_audit", {}).get(key) != expected:
            return f"TICKET-253 machine field changed: {key}"
    expected = {
        "riemann": ("riemann", "DirichletPacketSpectralDensityLimit", "partial_theorem", "ActualWeilFormDominatesPositiveDensityProjectionOnDirichletPackets", "00bebb686b3544d67b49612c512f28feee544d678ceab6c5fa269f64e9e16299"),
        "collatz": ("collatz", "CompleteSlopeCharacterSumDichotomyNoGo", "exact_no_go", "CrossPrimeCanonicalSlopeCharacterAverageCancellation", "455240ed72e4017bfbc63ba310348eb9e2618370d829ee093253e1d66e6883c2"),
        "goldbach": ("goldbach", "PrimeOrderingUniquePrefixRealizabilityCriterion", "partial_theorem", "UniformPrimePrefixDiscrepancyExcludesEveryCompatibleCyclotomicTail", "a14b831094b7733f9186b166b2346c3e295617c705ded50c46ef38a62994e0ff"),
        "twin_prime": ("twin-prime", "RightEvenContaminationReducesToEightyFourLebesgueNagellExponents", "partial_theorem", "LebesgueNagellExponent17HasNoPositiveSolution", "b98e7851ac77f39a65148a17da8a40600d25774928d13483a1fcef4d4b7b8bb6"),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-253-density-packet.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-253-complete-character-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-253-prime-prefix-criterion.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-253-lebesgue-nagell-reduction.json",
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
            return f"TICKET-253 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-253 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-253 open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-253 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-253 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-253 track JSON changed: {key}"
    if sum(node.get("status") == "external_theorem" for node in root["twin_prime"]["proof_dag"]["nodes"]) != 1:
        return "TICKET-253 Twin external dependency boundary changed"
    if any(
        node.get("status") == "external_theorem"
        for key in ("riemann", "collatz", "goldbach")
        for node in root[key]["proof_dag"]["nodes"]
    ):
        return "TICKET-253 unexpected external dependency"
    state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
    if (
        state.get("ticket", 0) < 253
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
    ):
        return "TICKET-253 persistent research state changed"
    for key, (_, theorem, _, _, _) in expected.items():
        if theorem not in state.get("problems", {}).get(key, {}).get("established_results", []):
            return f"TICKET-253 result missing from persistent history: {key}"
    for report in (
        ROOT / "docs/density-character-prefix-lebesgue.md",
        ROOT / "docs/density-character-prefix-lebesgue.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-253 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket253_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-253 structure verification passed")
