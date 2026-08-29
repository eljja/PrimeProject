from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket252-sparse-marginal-zeroresidue-local.v1"
AUDIT_KEY = "sparse_marginal_zeroresidue_local_audit"
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


def verify_ticket252_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket252-sparse-marginal-zeroresidue-local.json"
    if not integrated.exists():
        return "missing TICKET-252 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-252 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-252 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    expected_machine = {
        "exact_theorem_count": 4,
        "new_partial_theorem_count": 1,
        "exact_no_go_count": 3,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "goldbach",
        "stagnated_problem_count": 0,
        "riemann_sparse_projection_case_count": 12,
        "collatz_marginal_countermodel_case_count": 11,
        "goldbach_zero_residue_case_count": 68,
        "twin_finite_modulus_case_count": 8,
        "total_failure_count": 0,
    }
    for key, expected in expected_machine.items():
        if root.get("machine_audit", {}).get(key) != expected:
            return f"TICKET-252 machine field changed: {key}"
    expected = {
        "riemann": ("riemann", "SparseFourierProjectionInteriorConcentrationNoGo", "exact_no_go", "ActualWeilKernelHasPositiveDensityAgainstEveryInteriorWavePacket", "3e7c26600452d330e977e7880ca71b028709cad8966df6c63c41be6a1e910294"),
        "collatz": ("collatz", "UniformMarginalsCannotDetectProjectiveFermatSlopeNoGo", "exact_no_go", "JointFermatQuotientCharacterCancellationAtSlopeThreeFifths", "d134c93741ae3151e80bc4443e7abbbbab5ba578292ade37cef147e17cfb324c"),
        "goldbach": ("goldbach", "PrimeCountZeroResidueCyclotomicCompatibilityCriterion", "partial_theorem", "ActualPrimeOrderingExcludesZeroResidueCompatibleCyclotomicTail", "5c95a4a8bf5019dc499a4fc45abcd82b1c10ede06659f59d0d28ee036eb06717"),
        "twin_prime": ("twin-prime", "FiniteCongruenceLocalSolubilityNoGoForRightEvenPrimePowers", "exact_no_go", "QuadraticUnitCoefficientOneExcludesOddPrimeExponents", "079a60fde7d3f69814681f455edadebbe8b8d0aaf199e7821a0dad94d3ee02b4"),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-252-sparse-fourier-projection.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-252-marginal-joint-slope.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-252-zero-residue-compatibility.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-252-finite-congruence-local-solubility.json",
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
            return f"TICKET-252 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-252 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-252 open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-252 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-252 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-252 track JSON changed: {key}"
    if sum(node.get("status") == "external_theorem" for node in root["twin_prime"]["proof_dag"]["nodes"]) != 1:
        return "TICKET-252 Twin Dirichlet dependency boundary changed"
    if any(
        node.get("status") == "external_theorem"
        for key in ("riemann", "collatz", "goldbach")
        for node in root[key]["proof_dag"]["nodes"]
    ):
        return "TICKET-252 unexpected external dependency"
    state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
    if (
        state.get("ticket") != 252
        or state.get("parent_ticket") != 251
        or state.get("deep_focus_problem") != "goldbach"
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
    ):
        return "TICKET-252 persistent research state changed"
    for report in (
        ROOT / "docs/sparse-marginal-zeroresidue-local.md",
        ROOT / "docs/sparse-marginal-zeroresidue-local.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-252 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket252_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-252 structure verification passed")
