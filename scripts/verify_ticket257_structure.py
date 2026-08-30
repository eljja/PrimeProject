from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket257-spike-cyclotomic-character-root.v1"
AUDIT_KEY = "spike_cyclotomic_character_root_audit"
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


def verify_ticket257_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket257-spike-cyclotomic-character-root.json"
    if not integrated.exists():
        return "missing TICKET-257 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-257 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-257 completion boundary changed"
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
        "riemann_spike_case_count": 8,
        "collatz_prime_case_count": 22,
        "goldbach_character_row_count": 3,
        "goldbach_maximum_prime_prefix_length": 7_759_741,
        "goldbach_new_q11_certificate_count": 1,
        "twin_root_neighbor_candidate_count": 400_399,
        "twin_denominator_limit": 200_000,
        "total_failure_count": 0,
    }
    for key, expected in expected_machine.items():
        if root.get("machine_audit", {}).get(key) != expected:
            return f"TICKET-257 machine field changed: {key}"
    expected = {
        "riemann": (
            "riemann",
            "PositiveConvergentPacketEnergyLagPartialSumNoGo",
            "exact_no_go",
            "ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation",
            "2654791b7d15314396158a2a60a103f76cb57f74a2ee477bf32d47213a767f56",
        ),
        "collatz": (
            "collatz",
            "DistinctPrimeCyclotomicPhaseExactCancellationNoGo",
            "exact_no_go",
            "CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude",
            "627c0da86ba9bd0f734d01ace2f1fb18df1778244c975655a877f52ca7ecf9a5",
        ),
        "goldbach": (
            "goldbach",
            "QuadraticCharacterReflectionObstructionAndNextPrefixExclusion",
            "partial_theorem",
            "EveryCompatibleEvenQDivisiblePrimePrefixHasNonzeroOddCharacterMoment",
            "b294b8571a28f6988cdb0fd7d0353f683eb02d8aeae4b42b031ab4801f4b022f",
        ),
        "twin_prime": (
            "twin-prime",
            "UniqueRealRootNeighborReductionAndBoundedExclusion",
            "partial_theorem",
            "EveryNonzeroDenominatorUniqueRootNeighborMissesCoefficientOne",
            "70e6d98d1a8476ac6ea9db6eb2bc27895a7a84622e256f3cdd12d8881f92e5b1",
        ),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-257-positive-convergent-spike-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-257-cyclotomic-exact-cancellation-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-257-character-prefix-exclusion.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-257-unique-root-neighbor.json",
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
            return f"TICKET-257 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-257 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-257 open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-257 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-257 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-257 track JSON changed: {key}"
    state = json.loads(
        (ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8")
    )
    if (
        state.get("ticket") != 257
        or state.get("parent_ticket") != 256
        or state.get("deep_focus_problem") != "goldbach"
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
    ):
        return "TICKET-257 persistent research state changed"
    for report in (
        ROOT / "docs/spike-cyclotomic-character-root.md",
        ROOT / "docs/spike-cyclotomic-character-root.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-257 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket257_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-257 structure verification passed")
