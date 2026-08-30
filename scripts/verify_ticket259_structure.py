from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket259-critical-alignment-compatibility-local.v1"
AUDIT_KEY = "critical_alignment_compatibility_local_audit"
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


def verify_ticket259_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket259-critical-alignment-compatibility-local.json"
    if not integrated.exists():
        return "missing TICKET-259 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-259 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-259 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    machine = {
        "exact_theorem_count": 4, "new_partial_theorem_count": 1,
        "exact_no_go_count": 3, "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0, "proof_dag_count": 4,
        "next_single_lemma_count": 4, "deep_focus_problem": "goldbach",
        "stagnated_problem_count": 0, "riemann_critical_case_count": 12,
        "collatz_alignment_case_count": 166,
        "goldbach_compatibility_case_count": 208,
        "goldbach_q13_prefix_length": 135_207_787,
        "goldbach_q13_last_prime": 2_798_637_773,
        "goldbach_independent_algorithm_count": 2,
        "twin_local_modulus_case_count": 30, "total_failure_count": 0,
    }
    for key, expected in machine.items():
        if root.get("machine_audit", {}).get(key) != expected:
            return f"TICKET-259 machine field changed: {key}"
    expected = {
        "riemann": ("riemann", "CriticalScaledDownwardJumpEqualityNoGo", "exact_no_go", "ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation", "aa676e636fbf50546075b2cd12b026a73f9f3a3a12554032b7323a229cc38441"),
        "collatz": ("collatz", "DistinctPrimePhaseAlignmentLinearGrowthNoGo", "exact_no_go", "CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude", "1ee64aea8a3265150d2928074b69d57a931be3e9426e0252750c7d15a46ae73c"),
        "goldbach": ("goldbach", "QDivisibleCompatibilityIffTwoModuloFourAndQ13Certificate", "partial_theorem", "EveryTwoModuloFourQDivisiblePrimePrefixHasNonzeroOddCharacterMoment", "d20605cd3390770e05234eab2c4a433b023457ac354ab2cd16a4ad87d18caf84"),
        "twin_prime": ("twin-prime", "FiniteCongruenceFixedRootWindowNoGo", "exact_no_go", "EveryUniqueRootConvergentMissesUnitCoefficient", "8d11c60fee0923ead2f28e5ec4e2f422ff1d8014f42a3b7ea19d24a7475f992d"),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-259-critical-scaled-drop-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-259-aligned-phase-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-259-compatibility-q13-certificate.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-259-fixed-local-window-no-go.json",
    }
    for key, (problem_id, theorem, classification, next_lemma, digest) in expected.items():
        section = root.get(key, {})
        values = (
            section.get("problem_id"), section.get("theorem_name"),
            section.get("result_classification"), section.get("problem_status"),
            section.get("route_decision", {}).get("next_single_lemma"),
            section.get("reproducible_computation", {}).get("transcript_sha256"),
        )
        if values != (problem_id, theorem, classification, "open_not_proven", next_lemma, digest):
            return f"TICKET-259 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-259 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1 or not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-259 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-259 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-259 track JSON changed: {key}"
    q13 = root["goldbach"]["reproducible_computation"]["q13_m26_exact_prime_prefix_certificate"]
    if (
        q13.get("actual_first_T_prime_residue_counts") != q13.get("independent_direct_segmented_counts")
        or q13.get("primitive_odd_character_moment_remainder") != [-958, 1746, -64, -121]
        or not q13.get("certificate_verified")
    ):
        return "TICKET-259 q=13 independent certificate changed"
    state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
    boundary = (
        state.get("ticket"), state.get("parent_ticket"),
        state.get("deep_focus_problem"), state.get("resolved_count"),
        state.get("candidate_resolution_count"), state.get("program_complete"),
    )
    if boundary != (259, 258, "goldbach", 0, 0, False):
        return "TICKET-259 persistent research state changed"
    for report in (
        ROOT / "docs/critical-alignment-compatibility-local.md",
        ROOT / "docs/critical-alignment-compatibility-local.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-259 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket259_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-259 structure verification passed")
