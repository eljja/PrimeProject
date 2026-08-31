from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket260-weighted-equidistribution-primerace-variablemod.v1"
AUDIT_KEY = "weighted_equidistribution_primerace_variablemod_audit"
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


def verify_ticket260_structure() -> str | None:
    integrated = (
        ROOT
        / "data/open-problem/ticket260-weighted-equidistribution-primerace-variablemod.json"
    )
    if not integrated.exists():
        return "missing TICKET-260 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-260 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-260 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    machine = {
        "exact_theorem_count": 4,
        "new_partial_theorem_count": 3,
        "exact_no_go_count": 1,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "twin_prime",
        "stagnated_problem_count": 0,
        "riemann_weighted_variation_case_count": 16,
        "collatz_phase_case_count": 64,
        "collatz_fixed_modulus_case_count": 15,
        "goldbach_q3_level_count": 3,
        "goldbach_maximum_prefix_length": 28_697_817,
        "goldbach_maximum_endpoint": 547_035_959,
        "goldbach_independent_algorithm_count": 2,
        "twin_convergent_count": 256,
        "twin_first_order_nontrivial_pass_count": 2,
        "twin_second_order_nontrivial_pass_count": 0,
        "twin_maximum_denominator_digit_count": 121,
        "total_failure_count": 0,
    }
    for key, expected_value in machine.items():
        if root.get("machine_audit", {}).get(key) != expected_value:
            return f"TICKET-260 machine field changed: {key}"
    expected = {
        "riemann": (
            "riemann",
            "SummableScaledDownwardVariationForcesEventualLagPositivity",
            "partial_theorem",
            "ActualWeilPacketScaledDownwardVariationIsSummable",
            "1fcbc1bb15fcd64f8ce04cd99c19d98ad6dad73dced2e79eb60ed5f19f41beeb",
        ),
        "collatz": (
            "collatz",
            "FixedModulusExponentEquidistributionPhaseAlignmentNoGo",
            "exact_no_go",
            "CanonicalFermatQuotientAngularDiscrepancyTendsToZero",
            "044392f39a7829cd995fade3f2b9644d524a989631a3f9ce10a908c6fb984d15",
        ),
        "goldbach": (
            "goldbach",
            "Q3CompatibleFamilyPrimeRaceEquivalence",
            "partial_theorem",
            "Q3SpecialPrimeRaceNeverTiesAtSixTimesPowerOfThreePlusThree",
            "bd6146858e8e5587274d75e799d05983d0bf67a2a6ca625fe132e7e52b33c625",
        ),
        "twin_prime": (
            "twin-prime",
            "SecondOrderDenominatorCongruenceAnd256ConvergentCertificate",
            "partial_theorem",
            "NoUniqueRootConvergentSatisfiesSecondOrderDenominatorCongruence",
            "822878ce37c68575312588bd75639f736d9dccf9252b148fcd2170c31ac9c9e8",
        ),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-260-summable-scaled-variation.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-260-fixed-modulus-equidistribution-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-260-q3-prime-race-reduction.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-260-variable-denominator-congruence.json",
    }
    for key, (problem_id, theorem, classification, next_lemma, digest) in expected.items():
        section = root.get(key, {})
        values = (
            section.get("problem_id"),
            section.get("theorem_name"),
            section.get("result_classification"),
            section.get("problem_status"),
            section.get("route_decision", {}).get("next_single_lemma"),
            section.get("reproducible_computation", {}).get("transcript_sha256"),
        )
        if values != (
            problem_id,
            theorem,
            classification,
            "open_not_proven",
            next_lemma,
            digest,
        ):
            return f"TICKET-260 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-260 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-260 DAG open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-260 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-260 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-260 track JSON changed: {key}"
    q3 = root["goldbach"]["reproducible_computation"]
    rows = q3.get("exact_q3_prime_race_certificate_rows", [])
    if (
        [row.get("mod_3_prime_race_difference_N1_minus_N2") for row in rows]
        != [-6, -42, -2118]
        or any(
            row.get("actual_residue_counts")
            != row.get("independent_segmented_residue_counts")
            for row in rows
        )
        or not all(row.get("certificate_verified") for row in rows)
    ):
        return "TICKET-260 q=3 independent certificates changed"
    twin = root["twin_prime"]["reproducible_computation"]
    first = [
        (row.get("term_index"), row.get("epsilon"), int(row.get("denominator", 0)))
        for row in twin.get("first_order_nontrivial_passes", [])
    ]
    if first != [(2, -1, 13), (3, -1, 14)]:
        return "TICKET-260 first-order Twin counterexamples changed"
    if twin.get("second_order_nontrivial_passes") != []:
        return "TICKET-260 second-order Twin certificate changed"
    state = json.loads(
        (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
            encoding="utf-8"
        )
    )
    if (
        state.get("ticket", 0) < 260
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
    ):
        return "TICKET-260 persistent research state changed"
    if state.get("ticket") == 260 and (
        state.get("parent_ticket") != 259
        or state.get("deep_focus_problem") != "twin_prime"
    ):
        return "TICKET-260 persistent research state changed"
    for key, (_, theorem, _, _, _) in expected.items():
        if theorem not in state.get("problems", {}).get(key, {}).get(
            "established_results", []
        ):
            return f"TICKET-260 theorem missing from successor state: {key}"
    for report in (
        ROOT / "docs/weighted-equidistribution-primerace-variablemod.md",
        ROOT / "docs/weighted-equidistribution-primerace-variablemod.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-260 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket260_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-260 structure verification passed")
