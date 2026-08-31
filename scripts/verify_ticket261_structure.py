from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket261-sharpness-weyl-ties-dualcongruence.v1"
AUDIT_KEY = "sharpness_weyl_ties_dualcongruence_audit"
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


def verify_ticket261_structure() -> str | None:
    integrated = (
        ROOT / "data/open-problem/ticket261-sharpness-weyl-ties-dualcongruence.json"
    )
    if not integrated.exists():
        return "missing TICKET-261 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-261 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-261 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    machine = {
        "exact_theorem_count": 4,
        "new_partial_theorem_count": 2,
        "exact_no_go_count": 2,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "twin_prime",
        "stagnated_problem_count": 0,
        "riemann_reciprocal_tail_case_count": 128,
        "collatz_countermodel_phase_case_count": 128,
        "collatz_canonical_prefix_count": 16_384,
        "collatz_canonical_dyadic_row_count": 12,
        "goldbach_actual_parity_certificate_count": 3,
        "goldbach_abstract_tie_replay_count": 16,
        "twin_convergent_count": 1024,
        "twin_denominator_first_order_pass_count": 2,
        "twin_numerator_first_order_nontrivial_pass_count": 1,
        "twin_joint_second_order_pass_count": 0,
        "twin_maximum_denominator_digit_count": 519,
        "total_failure_count": 0,
    }
    for key, expected_value in machine.items():
        if root.get("machine_audit", {}).get(key) != expected_value:
            return f"TICKET-261 machine field changed: {key}"
    expected = {
        "riemann": (
            "riemann",
            "SummableScaledVariationNecessityNoGo",
            "exact_no_go",
            "ActualWeilPacketScaledDownwardJumpLimsupBelowLimit",
            "8242a67f0d5c2c2b451cef1cb2c48100ffaa008fa05b402ac6274da8a88b670b",
        ),
        "collatz": (
            "collatz",
            "FirstHarmonicCancellationAngularDiscrepancyNoGo",
            "exact_no_go",
            "CanonicalFermatQuotientWeylSumsVanishForEveryNonzeroH",
            "35619c4243f9a4fa6ba7eff5764787d0ee3212d8f9decca0e85938e01b2de750",
        ),
        "goldbach": (
            "goldbach",
            "Q3PrimePrefixProductParityObstruction",
            "partial_theorem",
            "Q3SpecialPrimePrefixProductIsMinusOneModuloThree",
            "7c01ec5d388159c3ba032b8f87459f71cbd4bc339f2f181ef6bc6113075d810c",
        ),
        "twin_prime": (
            "twin-prime",
            "BidirectionalSecondOrderCongruenceAnd1024ConvergentCertificate",
            "partial_theorem",
            "NoUniqueRootConvergentSatisfiesBothSecondOrderCongruences",
            "3327f229884ca78a1b95a3b2336cc245e4e99cbfff8f2020a24db3299754b70e",
        ),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-261-summability-necessity-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-261-first-harmonic-discrepancy-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-261-q3-product-parity.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-261-bidirectional-second-order.json",
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
            return f"TICKET-261 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-261 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-261 DAG open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-261 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-261 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-261 track JSON changed: {key}"
    canonical = root["collatz"]["reproducible_computation"]
    increased = [
        row.get("canonical_prime_prefix_count")
        for row in canonical.get("exact_canonical_star_discrepancy_rows", [])
        if row.get("increased_from_previous_dyadic_prefix")
    ]
    if increased != [4096, 16384]:
        return "TICKET-261 canonical discrepancy witnesses changed"
    goldbach = root["goldbach"]["reproducible_computation"]
    if any(
        row.get("prime_prefix_product_mod_3_excluding_prime_3") != 2
        or not row.get("minus_one_product_excludes_tie")
        for row in goldbach.get("exact_q3_product_parity_certificate_rows", [])
    ):
        return "TICKET-261 q=3 parity certificates changed"
    twin = root["twin_prime"]["reproducible_computation"]
    denominator_first = [
        (row.get("term_index"), row.get("epsilon"), int(row.get("denominator", 0)))
        for row in twin.get("denominator_first_order_nontrivial_passes", [])
    ]
    numerator_first = [
        (row.get("term_index"), row.get("epsilon"), int(row.get("numerator", 0)), int(row.get("denominator", 0)))
        for row in twin.get("numerator_first_order_nontrivial_passes", [])
    ]
    if denominator_first != [(2, -1, 13), (3, -1, 14)]:
        return "TICKET-261 denominator first-order witnesses changed"
    if numerator_first != [(5, -1, -3, 41)]:
        return "TICKET-261 numerator first-order witness changed"
    if twin.get("joint_second_order_passes") != []:
        return "TICKET-261 joint second-order certificate changed"
    state = json.loads(
        (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
            encoding="utf-8"
        )
    )
    boundary = (
        state.get("ticket"),
        state.get("parent_ticket"),
        state.get("deep_focus_problem"),
        state.get("resolved_count"),
        state.get("candidate_resolution_count"),
        state.get("program_complete"),
    )
    if boundary != (261, 260, "twin_prime", 0, 0, False):
        return "TICKET-261 persistent research state changed"
    for report in (
        ROOT / "docs/sharpness-weyl-ties-dualcongruence.md",
        ROOT / "docs/sharpness-weyl-ties-dualcongruence.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-261 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket261_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-261 structure verification passed")
