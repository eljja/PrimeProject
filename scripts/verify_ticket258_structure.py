from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket258-variation-character-convergent.v1"
AUDIT_KEY = "variation_character_convergent_audit"
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


def verify_ticket258_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket258-variation-character-convergent.json"
    if not integrated.exists():
        return "missing TICKET-258 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-258 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-258 completion boundary changed"
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
        "riemann_spike_case_count": 12,
        "collatz_prime_case_count": 166,
        "collatz_trivial_phase_count": 0,
        "goldbach_modulus_case_count": 6,
        "goldbach_blind_vector_count": 4,
        "twin_convergent_count": 128,
        "twin_maximum_excluded_denominator": "67076610336720215425112731771403002965838278844687475228751003",
        "total_failure_count": 0,
    }
    for key, expected in expected_machine.items():
        if root.get("machine_audit", {}).get(key) != expected:
            return f"TICKET-258 machine field changed: {key}"
    expected = {
        "riemann": (
            "riemann", "BoundedTotalVariationPacketEnergyLagNoGo", "exact_no_go",
            "ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation",
            "38b8848a883363638d20c80bab9be204bfde0d9fabd6e0c2d17f34244845215b",
        ),
        "collatz": (
            "collatz", "DistinctPrimeCyclotomicPhaseRationalIndependence", "exact_no_go",
            "CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude",
            "7314b839d426d6ba0b5fdfbf9d259d9c585f2a7f9f06510d8f325fb060b72dd1",
        ),
        "goldbach": (
            "goldbach", "PrimitiveOddCharacterCompletenessClassification", "partial_theorem",
            "EveryCompatibleEvenQDivisiblePrimePrefixHasNonzeroOddCharacterMoment",
            "6067f098366c338c9b8387b32f532cb54c58e2d6a838e9e29a2704c3fb657570",
        ),
        "twin_prime": (
            "twin-prime", "UnitCoefficientSolutionsAreRootConvergents", "partial_theorem",
            "EveryUniqueRootConvergentMissesUnitCoefficient",
            "317333a17662c51bd54e8fe174948df0548dfb1c43a1f41af389c2b02df3dd1d",
        ),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-258-bounded-variation-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-258-rational-independence.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-258-character-completeness.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-258-root-convergents.json",
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
            return f"TICKET-258 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-258 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-258 open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-258 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-258 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-258 track JSON changed: {key}"
    state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
    if (
        state.get("ticket", 0) < 258
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
    ):
        return "TICKET-258 persistent research state changed"
    if state.get("ticket") == 258 and (
        state.get("parent_ticket") != 257
        or state.get("deep_focus_problem") != "twin_prime"
    ):
        return "TICKET-258 persistent research state changed"
    for report in (
        ROOT / "docs/variation-character-convergent.md",
        ROOT / "docs/variation-character-convergent.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-258 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket258_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-258 structure verification passed")
