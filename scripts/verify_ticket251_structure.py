from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket251-interior-crt-cyclotomic-righteven.v1"
AUDIT_KEY = "interior_crt_cyclotomic_righteven_audit"
ALLOWED = {"proved", "disproved", "computed_finite", "external_theorem", "assumption", "heuristic", "open"}


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


def verify_ticket251_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket251-interior-crt-cyclotomic-righteven.json"
    if not integrated.exists():
        return "missing TICKET-251 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-251 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-251 completion boundary changed"
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
        "riemann_concentration_case_count": 11,
        "collatz_CRT_case_count": 4,
        "goldbach_cyclotomic_case_count": 32,
        "twin_active_scale_count": 7,
        "twin_right_even_witness_count": 124,
        "total_failure_count": 0,
    }
    for key, expected in expected_machine.items():
        if root.get("machine_audit", {}).get(key) != expected:
            return f"TICKET-251 machine field changed: {key}"
    expected = {
        "riemann": ("riemann", "InteriorZeroLocalMultiplierCoercivityNoGo", "exact_no_go", "NonlocalArithmeticWeilKernelExcludesInteriorConcentration", "e79a0c6278dedf06d33bbd79125d059adf86c1f2ae1f252afbae78daf5d3ffcd"),
        "collatz": ("collatz", "FinitePrimeCanonicalLiftPatternCRTInterpolationNoGo", "exact_no_go", "CanonicalRepresentativeFermatQuotientDistributionBeyondFiniteCRTInterpolation", "c184a69eaebae32ffdc9e9043ca4864bf7615e5933a225721616dcda732e2fdc"),
        "goldbach": ("goldbach", "CyclotomicUnitFullSupportEnergyConcentrationNoGo", "exact_no_go", "ActualPrimeCountResidueVectorsExcludeCyclotomicUnitConcentration", "e3c9e81aab8500e964f265aa6ba8bd91105d40f67e1f5c7938f63bb88bcaa857"),
        "twin_prime": ("twin-prime", "RightEvenModuloEightConstraintAndSharpness", "partial_theorem", "NoPositivePrimePowerSolutionsOfXSquareMinusTwoEqualsYOddPower", "2881e5c20c714c52c8502ea5ec74617bed8bbc110c35069c488e960a4d711e85"),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-251-interior-zero-local-multiplier.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-251-finite-prime-crt-interpolation.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-251-cyclotomic-unit-concentration.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-251-right-even-classification.json",
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
            return f"TICKET-251 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-251 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-251 open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-251 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-251 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-251 track JSON changed: {key}"
    if len(root["riemann"]["reproducible_computation"]["exact_interior_concentration_rows"]) != 11:
        return "TICKET-251 RH replay changed"
    if len(root["collatz"]["reproducible_computation"]["exact_CRT_interpolation_rows"]) != 4:
        return "TICKET-251 Collatz replay changed"
    if len(root["goldbach"]["reproducible_computation"]["exact_cyclotomic_unit_rows"]) != 32:
        return "TICKET-251 Goldbach replay changed"
    twin = root["twin_prime"]["reproducible_computation"]
    if len(twin["exact_scale_rows"]) != 7 or len(twin["selected_witnesses"]) != 124:
        return "TICKET-251 Twin replay changed"
    if sum(node.get("status") == "external_theorem" for node in root["twin_prime"]["proof_dag"]["nodes"]) != 0:
        return "TICKET-251 Twin unexpectedly depends on an external theorem"
    source_audit = twin.get("withdrawn_source_audit", {})
    if source_audit.get("status") != "withdrawn_major_mistake" or source_audit.get("used_as_dependency") is not False:
        return "TICKET-251 Twin withdrawn-source boundary changed"
    state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
    if (
        state.get("ticket") != 251
        or state.get("parent_ticket") != 250
        or state.get("deep_focus_problem") != "goldbach"
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
    ):
        return "TICKET-251 persistent research state changed"
    for report in (
        ROOT / "docs/interior-crt-cyclotomic-righteven.md",
        ROOT / "docs/interior-crt-cyclotomic-righteven.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-251 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket251_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-251 structure verification passed")
