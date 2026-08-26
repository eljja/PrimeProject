from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket248-unweighted-wieferich-jet-active.v1"
AUDIT_KEY = "unweighted_wieferich_jet_active_audit"
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


def verify_ticket248_structure() -> str | None:
    integrated = (
        ROOT / "data/open-problem/ticket248-unweighted-wieferich-jet-active.json"
    )
    if not integrated.exists():
        return "missing TICKET-248 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-248 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-248 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    machine = root.get("machine_audit", {})
    expected_machine = {
        "exact_theorem_count": 4,
        "new_partial_theorem_count": 3,
        "exact_no_go_count": 1,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "goldbach",
        "stagnated_problem_count": 0,
        "riemann_unweighted_certificate_count": 8,
        "collatz_wieferich_prime_count": 78_495,
        "goldbach_first_jet_row_count": 36,
        "twin_active_scale_count": 7,
        "total_failure_count": 0,
    }
    for key, expected_value in expected_machine.items():
        if machine.get(key) != expected_value:
            return f"TICKET-248 machine field changed: {key}"

    expected = {
        "riemann": (
            "riemann",
            "UnweightedInfiniteMomentCoercivityNoGo",
            "exact_no_go",
            "ArithmeticOffDiagonalWeilCoercivityOnAdmissibleClosure",
        ),
        "collatz": (
            "collatz",
            "ActualBadBranchGeneralizedWieferichSeparation",
            "partial_theorem",
            "ExistenceOfSeparatedGeneralizedWieferichPrimeFor32Over27Against2Over3",
        ),
        "goldbach": (
            "goldbach",
            "CenteredFirstJetParsevalArcBridge",
            "partial_theorem",
            "UniformReducedNumeratorCenteredFirstJetSavingOnQuarterTorus",
        ),
        "twin_prime": (
            "twin-prime",
            "ExactActivePrimePowerContaminationIdentity",
            "partial_theorem",
            "ScaleLocalTypeIILowerBoundBeyondActivePrimePowerContamination",
        ),
    }
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-248-unweighted-moment-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-248-generalized-wieferich-separation.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-248-centered-first-jet-parseval.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-248-active-contamination-identity.json",
    }
    for key, (problem_id, theorem_name, classification, next_lemma) in expected.items():
        section = root.get(key, {})
        if section.get("problem_id") != problem_id:
            return f"TICKET-248 problem_id changed: {key}"
        if section.get("theorem_name") != theorem_name:
            return f"TICKET-248 theorem changed: {key}"
        if section.get("result_classification") != classification:
            return f"TICKET-248 classification changed: {key}"
        if section.get("problem_status") != "open_not_proven":
            return f"TICKET-248 problem status changed: {key}"
        if section.get("route_decision", {}).get("next_single_lemma") != next_lemma:
            return f"TICKET-248 next lemma changed: {key}"
        if section.get("stagnation_count") != 0:
            return f"TICKET-248 stagnation count changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED_NODE_STATUSES for node in nodes):
            return f"TICKET-248 proof DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-248 open frontier count changed: {key}"
        if not dag_is_acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-248 proof DAG is cyclic or malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-248 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem_name:
            return f"TICKET-248 track JSON changed: {key}"

    rh = root["riemann"]["reproducible_computation"]
    if (
        rh.get("transcript_sha256")
        != "faaba3834a933146319b810147b5d58136ae13d23bd6599297b292d2ba33c1bd"
        or len(rh.get("exact_legendre_rows", [])) != 8
        or rh.get("exact_legendre_rows", [])[-1]
        .get("proved_all_tail_energy_bound", {})
        .get("exact")
        != "11/128"
    ):
        return "TICKET-248 RH unweighted moment certificate changed"
    co = root["collatz"]["reproducible_computation"]
    scan = co.get("exact_modular_scan", {})
    if (
        co.get("transcript_sha256")
        != "444834a2768b3e94e21d0f968aef0e93fd87f08c540ca52af08756480b6d2d25"
        or scan.get("primes_checked") != 78_495
        or scan.get("W_32_27_zero_primes") != []
        or scan.get("W_2_3_zero_primes") != [23]
        or scan.get("separated_bad_primes") != []
    ):
        return "TICKET-248 Collatz Wieferich certificate changed"
    gb = root["goldbach"]["reproducible_computation"]
    gb_rows = gb.get("exact_selected_first_jet_rows", [])
    if (
        gb.get("transcript_sha256")
        != "49d39cfb54e21607b0ad1e39ddf0734d30d646bab71b90b82fb746a3f80cc18a"
        or len(gb_rows) != 36
        or gb_rows[-1].get("phi_times_first_moment_variance")
        != 22_529_726_453_345_020
    ):
        return "TICKET-248 Goldbach first-jet certificate changed"
    tp = root["twin_prime"]["reproducible_computation"]
    tp_rows = tp.get("exact_active_contamination_rows", [])
    if (
        tp.get("transcript_sha256")
        != "85f69edcdb7bc23ce3a41d770918c5a4589b4b50a4e003145c47874fa2bd1741"
        or len(tp_rows) != 7
        or tp_rows[-1].get("exact_contamination_A2_minus_pi2") != 149
        or tp_rows[-1].get("active_union_bound_L_plus_R") != 150
    ):
        return "TICKET-248 Twin active contamination certificate changed"

    state_path = ROOT / "data/open-problem/four-problem-research-state.json"
    if not state_path.exists():
        return "missing persistent four-problem research state"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    ticket = state.get("ticket")
    retained_theorems = {
        "riemann": "UnweightedInfiniteMomentCoercivityNoGo",
        "collatz": "ActualBadBranchGeneralizedWieferichSeparation",
        "goldbach": "CenteredFirstJetParsevalArcBridge",
        "twin_prime": "ExactActivePrimePowerContaminationIdentity",
    }
    if (
        not isinstance(ticket, int)
        or ticket < 248
        or state.get("parent_ticket") != ticket - 1
        or any(
            theorem not in state.get("problems", {}).get(problem, {}).get("established_results", [])
            for problem, theorem in retained_theorems.items()
        )
    ):
        return "TICKET-248 persistent research state changed"
    if (
        state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
        or (ticket == 248 and state.get("deep_focus_problem") != "goldbach")
    ):
        return "TICKET-248 resolution boundary changed"
    for report in (
        ROOT / "docs/unweighted-wieferich-jet-active.md",
        ROOT / "docs/unweighted-wieferich-jet-active.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-248 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket248_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-248 structure verification passed")
