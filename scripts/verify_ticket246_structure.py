from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket246-moment-alldepth-parseval-primepower.v1"
AUDIT_KEY = "moment_alldepth_parseval_primepower_audit"
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
    if None in ids or any(len(edge) != 2 for edge in edges):
        return False
    adjacency = {node_id: [] for node_id in ids}
    indegree = {node_id: 0 for node_id in ids}
    for left, right in edges:
        if left not in ids or right not in ids:
            return False
        adjacency[left].append(right)
        indegree[right] += 1
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


def verify_ticket246_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket246-moment-alldepth-parseval-primepower.json"
    if not integrated.exists():
        return "missing TICKET-246 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-246 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-246 completion boundary changed"
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
        "deep_focus_problem": "collatz",
        "stagnated_problem_count": 0,
        "moment_certificate_count": 9,
        "collatz_replay_prime_count": 17_981,
        "goldbach_residue_row_count": 27,
        "twin_scale_count": 6,
        "total_failure_count": 0,
    }
    for key, expected_value in expected_machine.items():
        if machine.get(key) != expected_value:
            return f"TICKET-246 machine field changed: {key}"

    expected = {
        "riemann": (
            "riemann",
            "FiniteEvenMomentAnnihilatorNoGo",
            "exact_no_go",
            "InfiniteFeatureCoercivityOnNormalizedAdmissibleWeilClosure",
        ),
        "collatz": (
            "collatz",
            "AllDepthFixedBaseFermatPolynomialIdentity",
            "partial_theorem",
            "FixedBaseAllPrimeValuationDominationForPqByUqMinusVq",
        ),
        "goldbach": (
            "goldbach",
            "RationalCenterResidueParsevalBridge",
            "partial_theorem",
            "UniformQuarterTorusResidueVarianceDecayWithArcStability",
        ),
        "twin_prime": (
            "twin-prime",
            "PrimePowerPairProxyContaminationBound",
            "partial_theorem",
            "ScaleLocalTypeIILowerBoundBeyondPrimePowerContamination",
        ),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-246-finite-moment-annihilator.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-246-all-depth-fermat-polynomial.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-246-rational-center-parseval.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-246-prime-power-contamination.json",
    }
    for key, (problem_id, theorem_name, classification, next_lemma) in expected.items():
        section = root.get(key, {})
        if section.get("problem_id") != problem_id:
            return f"TICKET-246 problem_id changed: {key}"
        if section.get("theorem_name") != theorem_name:
            return f"TICKET-246 theorem changed: {key}"
        if section.get("result_classification") != classification:
            return f"TICKET-246 classification changed: {key}"
        if section.get("problem_status") != "open_not_proven":
            return f"TICKET-246 problem status changed: {key}"
        if section.get("route_decision", {}).get("next_single_lemma") != next_lemma:
            return f"TICKET-246 next lemma changed: {key}"
        if section.get("stagnation_count") != 0:
            return f"TICKET-246 stagnation count changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED_NODE_STATUSES for node in nodes):
            return f"TICKET-246 proof DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-246 open frontier count changed: {key}"
        if not dag_is_acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-246 proof DAG is cyclic or malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-246 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem_name:
            return f"TICKET-246 track JSON changed: {key}"

    rh = root["riemann"]["reproducible_computation"]
    if (
        rh.get("transcript_sha256")
        != "b69bddb4b9317df798192eb20375e83c87132c4804c1cdb57fe71723a8667765"
        or len(rh.get("exact_finite_difference_moment_rows", [])) != 9
        or rh.get("exact_finite_difference_moment_rows", [])[-1].get("unnormalized_L2_norm_squared")
        != 32_247_603_683_100
    ):
        return "TICKET-246 RH moment certificate changed"
    co = root["collatz"]["reproducible_computation"]
    replay = co.get("exact_modular_replay", {})
    if (
        co.get("transcript_sha256")
        != "7c570287e63987c481e1b978c549ff1889b3dcc058ef859fe5c1befb32456269"
        or replay.get("primes_scanned") != 17_981
        or replay.get("bad_difference_valuation_counts") != {"1": 17_981}
        or replay.get("comparison_difference_valuation_counts") != {"1": 17_980, "2": 1}
    ):
        return "TICKET-246 Collatz all-depth certificate changed"
    gb = root["goldbach"]["reproducible_computation"]
    if (
        gb.get("transcript_sha256")
        != "36eb596f31cf8cc962d8f1bb069323d36d8e8478dd095922c64ad5a529a67e10"
        or len(gb.get("exact_selected_residue_variance_rows", [])) != 27
        or gb.get("exhaustive_denominator_summaries", [])[-1]
        .get("maximum_relative_variance", {})
        .get("exact")
        != "37003/215654912"
    ):
        return "TICKET-246 Goldbach Parseval certificate changed"
    tp = root["twin_prime"]["reproducible_computation"]
    rows = tp.get("exact_prime_power_proxy_rows", [])
    if (
        tp.get("transcript_sha256")
        != "9b1df6145208e9fe91b48bca1b3a3f09be2de3bec22beaff05c0bd40ae0ecb1a"
        or len(rows) != 6
        or tp.get("minimal_false_proxy_pair", {}).get("n") != 7
        or rows[-1].get("composite_prime_power_contamination") != 122
    ):
        return "TICKET-246 Twin prime-power certificate changed"

    state_path = ROOT / "data/open-problem/four-problem-research-state.json"
    if not state_path.exists():
        return "missing persistent four-problem research state"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    ticket = state.get("ticket")
    retained_theorems = {
        "riemann": "FiniteEvenMomentAnnihilatorNoGo",
        "collatz": "AllDepthFixedBaseFermatPolynomialIdentity",
        "goldbach": "RationalCenterResidueParsevalBridge",
        "twin_prime": "PrimePowerPairProxyContaminationBound",
    }
    if (
        not isinstance(ticket, int)
        or ticket < 246
        or state.get("parent_ticket") != ticket - 1
        or any(
            theorem
            not in state.get("problems", {})
            .get(problem, {})
            .get("established_results", [])
            for problem, theorem in retained_theorems.items()
        )
    ):
        return "TICKET-246 persistent research state changed"
    if (
        state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
        or (ticket == 246 and state.get("deep_focus_problem") != "collatz")
    ):
        return "TICKET-246 resolution boundary changed"
    for report in (
        ROOT / "docs/moment-alldepth-parseval-primepower.md",
        ROOT / "docs/moment-alldepth-parseval-primepower.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-246 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket246_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-246 structure verification passed")
