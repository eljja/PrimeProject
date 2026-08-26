from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket249-compact-projective-parseval-lebesgue.v1"
AUDIT_KEY = "compact_projective_parseval_lebesgue_audit"
ALLOWED_NODE_STATUSES = {
    "proved",
    "disproved",
    "computed_finite",
    "external_theorem",
    "assumption",
    "heuristic",
    "open",
}


def dag_is_acyclic(nodes: list[dict], edges: list[list[str]]) -> bool:
    ids = {node.get("id") for node in nodes}
    if None in ids or len(ids) != len(nodes):
        return False
    adjacency = {node_id: [] for node_id in ids}
    indegree = {node_id: 0 for node_id in ids}
    for edge in edges:
        if len(edge) != 2 or edge[0] not in ids or edge[1] not in ids:
            return False
        adjacency[edge[0]].append(edge[1])
        indegree[edge[1]] += 1
    queue = [node_id for node_id, degree in indegree.items() if degree == 0]
    visited = 0
    while queue:
        current = queue.pop()
        visited += 1
        for successor in adjacency[current]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                queue.append(successor)
    return visited == len(ids)


def verify_ticket249_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket249-compact-projective-parseval-lebesgue.json"
    if not integrated.exists():
        return "missing TICKET-249 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-249 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-249 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    machine = root.get("machine_audit", {})
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
        "riemann_compact_model_count": 8,
        "collatz_wieferich_prime_count": 664_576,
        "collatz_field_case_count": 10_900,
        "goldbach_spike_case_count": 5_020,
        "twin_active_scale_count": 7,
        "total_failure_count": 0,
    }
    for key, expected_value in expected_machine.items():
        if machine.get(key) != expected_value:
            return f"TICKET-249 machine field changed: {key}"

    expected = {
        "riemann": ("riemann", "CompactOffDiagonalMomentCoercivityNoGo", "exact_no_go", "NoncompactArithmeticWeilFormOrLegendreExclusion"),
        "collatz": ("collatz", "SeparatedWieferichProjectiveSlopeCriterion", "partial_theorem", "OccurrenceOrAvoidanceOfProjectiveFermatQuotientSlopeThreeFifths"),
        "goldbach": ("goldbach", "CenteredJetParsevalSpikeNoGo", "exact_no_go", "PrimeSpecificReducedNumeratorJetAntiConcentration"),
        "twin_prime": ("twin-prime", "EvenExponentLeftActiveContaminationClassification", "partial_theorem", "ScaleLocalRightActivePrimePowerContaminationBound"),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-249-compact-offdiagonal-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-249-projective-slope.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-249-parseval-spike-no-go.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-249-even-left-classification.json",
    }
    for key, (problem_id, theorem_name, classification, next_lemma) in expected.items():
        section = root.get(key, {})
        if section.get("problem_id") != problem_id:
            return f"TICKET-249 problem_id changed: {key}"
        if section.get("theorem_name") != theorem_name:
            return f"TICKET-249 theorem changed: {key}"
        if section.get("result_classification") != classification:
            return f"TICKET-249 classification changed: {key}"
        if section.get("problem_status") != "open_not_proven":
            return f"TICKET-249 problem status changed: {key}"
        if section.get("route_decision", {}).get("next_single_lemma") != next_lemma:
            return f"TICKET-249 next lemma changed: {key}"
        if section.get("stagnation_count") != 0:
            return f"TICKET-249 stagnation count changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED_NODE_STATUSES for node in nodes):
            return f"TICKET-249 proof DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-249 open frontier count changed: {key}"
        if not dag_is_acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-249 proof DAG is cyclic or malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-249 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem_name:
            return f"TICKET-249 track JSON changed: {key}"

    rh = root["riemann"]["reproducible_computation"]
    if (
        rh.get("transcript_sha256") != "eaaa5e2eccd9fa1fcb32504240f86c5ecff7d815eb4d218a5eb22e9248bb999a"
        or len(rh.get("exact_finite_rank_rows", [])) != 8
        or rh.get("exact_finite_rank_rows", [])[-1].get("exact_projection_energy", {}).get("exact") != "0/1"
    ):
        return "TICKET-249 RH compact certificate changed"
    co = root["collatz"]["reproducible_computation"]
    scan = co.get("exact_modular_scan", {})
    if (
        co.get("transcript_sha256") != "db860c5bef6ae1b016d468346b1b9941eac90c375f93d4f7c4f67c8ee8e881b7"
        or scan.get("primes_checked") != 664_576
        or scan.get("W_32_27_zero_primes") != []
        or scan.get("W_2_3_zero_primes") != [23]
        or scan.get("separated_bad_primes") != []
    ):
        return "TICKET-249 Collatz projective certificate changed"
    gb = root["goldbach"]["reproducible_computation"]
    if (
        gb.get("transcript_sha256") != "439a6562998de91c99533ceacb5ac53d177af9e48165ee51c4eed6ec782d59fe"
        or gb.get("exact_group_ring_replay", {}).get("reduced_frequency_cases") != 5_020
        or any(row.get("spike_to_total_ratio_squared", {}).get("exact") != "1/2" for row in gb.get("exact_selected_spike_rows", []))
    ):
        return "TICKET-249 Goldbach spike certificate changed"
    tp = root["twin_prime"]["reproducible_computation"]
    rows = tp.get("exact_scale_rows", [])
    if (
        tp.get("transcript_sha256") != "6df796f1387e44725a337fc60d5fe44a94e2521496caf1cdc39e30bba96f6fd9"
        or len(rows) != 7
        or rows[-1].get("left_even_exponent_base_not_3") != 1
        or rows[-1].get("right_active_composite_pairs_R") != 136
    ):
        return "TICKET-249 Twin classification certificate changed"

    state_path = ROOT / "data/open-problem/four-problem-research-state.json"
    if not state_path.exists():
        return "missing persistent four-problem research state"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("ticket") != 249 or state.get("parent_ticket") != 248:
        return "TICKET-249 persistent research state changed"
    if (
        state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
        or state.get("deep_focus_problem") != "twin_prime"
    ):
        return "TICKET-249 resolution boundary changed"
    if sum(node.get("status") == "external_theorem" for node in root["twin_prime"]["proof_dag"]["nodes"]) != 1:
        return "TICKET-249 Twin external theorem boundary changed"
    for report in (
        ROOT / "docs/compact-projective-parseval-lebesgue.md",
        ROOT / "docs/compact-projective-parseval-lebesgue.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-249 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket249_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-249 structure verification passed")
