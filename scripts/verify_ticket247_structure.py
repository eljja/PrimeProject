from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket247-hilbert-hensel-lipschitz-primepower.v1"
AUDIT_KEY = "hilbert_hensel_lipschitz_primepower_audit"
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


def verify_ticket247_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket247-hilbert-hensel-lipschitz-primepower.json"
    if not integrated.exists():
        return "missing TICKET-247 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-247 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-247 completion boundary changed"
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
        "deep_focus_problem": "riemann",
        "stagnated_problem_count": 0,
        "riemann_legendre_certificate_count": 10,
        "collatz_hensel_prime_count": 1_226,
        "goldbach_arc_row_count": 27,
        "twin_scale_count": 7,
        "total_failure_count": 0,
    }
    for key, expected_value in expected_machine.items():
        if machine.get(key) != expected_value:
            return f"TICKET-247 machine field changed: {key}"

    expected = {
        "riemann": (
            "riemann",
            "HilbertSchmidtInfiniteMomentCoercivityNoGo",
            "exact_no_go",
            "NonHilbertSchmidtArithmeticWeilCoercivityOnAdmissibleClosure",
        ),
        "collatz": (
            "collatz",
            "FormalHenselBranchNoGoForValuationDomination",
            "exact_no_go",
            "ArithmeticFermatQuotientExclusionOfPqHenselBranch",
        ),
        "goldbach": (
            "goldbach",
            "RationalCenterArcLipschitzBridgeAndCenterOnlyNoGo",
            "partial_theorem",
            "UniformSignedResidueVarianceAndFirstMomentSavingOnQuarterTorus",
        ),
        "twin_prime": (
            "twin-prime",
            "SharpOddPrimePowerContaminationBound",
            "partial_theorem",
            "ScaleLocalTypeIILowerBoundBeyondSharpPrimePowerContamination",
        ),
    }
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-247-hilbert-schmidt-moment-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-247-hensel-polynomial-countermodels.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-247-rational-arc-lipschitz.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-247-sharp-prime-power-contamination.json",
    }
    for key, (problem_id, theorem_name, classification, next_lemma) in expected.items():
        section = root.get(key, {})
        if section.get("problem_id") != problem_id:
            return f"TICKET-247 problem_id changed: {key}"
        if section.get("theorem_name") != theorem_name:
            return f"TICKET-247 theorem changed: {key}"
        if section.get("result_classification") != classification:
            return f"TICKET-247 classification changed: {key}"
        if section.get("problem_status") != "open_not_proven":
            return f"TICKET-247 problem status changed: {key}"
        if section.get("route_decision", {}).get("next_single_lemma") != next_lemma:
            return f"TICKET-247 next lemma changed: {key}"
        if section.get("stagnation_count") != 0:
            return f"TICKET-247 stagnation count changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED_NODE_STATUSES for node in nodes):
            return f"TICKET-247 proof DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-247 open frontier count changed: {key}"
        if not dag_is_acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-247 proof DAG is cyclic or malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-247 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem_name:
            return f"TICKET-247 track JSON changed: {key}"

    rh = root["riemann"]["reproducible_computation"]
    if (
        rh.get("transcript_sha256")
        != "6f96be5ca5ceffa5ed645e2eb17758ae151b079799bf89baaa00c605cce871a5"
        or len(rh.get("exact_legendre_certificates", [])) != 10
        or rh.get("exact_legendre_certificates", [])[-1]
        .get("dyadic_weight_feature_tail_upper_bound", {})
        .get("exact")
        != "1/1064960"
    ):
        return "TICKET-247 RH Hilbert-Schmidt certificate changed"
    co = root["collatz"]["reproducible_computation"]
    if (
        co.get("transcript_sha256")
        != "bcb089ee91757f792ae7151212331f811f48a1cc771eea1386d4d4349ba04156"
        or co.get("exact_modular_replay", {}).get("primes_checked") != 1_226
        or not co.get("exact_modular_replay", {}).get("all_lifts_verified")
    ):
        return "TICKET-247 Collatz Hensel certificate changed"
    gb = root["goldbach"]["reproducible_computation"]
    if (
        gb.get("transcript_sha256")
        != "314c9f28ab175a59fce98474b249cf6e8fbc9fb811f2258d8c344d1b113a89b4"
        or len(gb.get("exact_selected_arc_rows", [])) != 27
        or gb.get("center_only_uniformity_counterfamily", [])[-1].get(
            "exact_abs_F_N_beta"
        )
        != 2
    ):
        return "TICKET-247 Goldbach arc certificate changed"
    tp = root["twin_prime"]["reproducible_computation"]
    rows = tp.get("exact_sharp_contamination_rows", [])
    if (
        tp.get("transcript_sha256")
        != "7b336b5638d06b913ebee11fc89308a7a186953083f85cfe772a8a4971410d87"
        or len(rows) != 7
        or rows[-1].get("limit_X") != 10_000_000
        or rows[-1].get("composite_prime_power_contamination") != 149
        or rows[-1].get("exact_odd_composite_prime_powers_N") != 533
    ):
        return "TICKET-247 Twin sharp contamination certificate changed"

    state_path = ROOT / "data/open-problem/four-problem-research-state.json"
    if not state_path.exists():
        return "missing persistent four-problem research state"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    ticket = state.get("ticket")
    retained_theorems = {
        "riemann": "HilbertSchmidtInfiniteMomentCoercivityNoGo",
        "collatz": "FormalHenselBranchNoGoForValuationDomination",
        "goldbach": "RationalCenterArcLipschitzBridgeAndCenterOnlyNoGo",
        "twin_prime": "SharpOddPrimePowerContaminationBound",
    }
    if (
        not isinstance(ticket, int)
        or ticket < 247
        or state.get("parent_ticket") != ticket - 1
        or any(
            theorem not in state.get("problems", {}).get(problem, {}).get("established_results", [])
            for problem, theorem in retained_theorems.items()
        )
    ):
        return "TICKET-247 persistent research state changed"
    if (
        state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
        or (ticket == 247 and state.get("deep_focus_problem") != "riemann")
    ):
        return "TICKET-247 resolution boundary changed"
    for report in (
        ROOT / "docs/hilbert-hensel-lipschitz-primepower.md",
        ROOT / "docs/hilbert-hensel-lipschitz-primepower.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-247 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket247_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-247 structure verification passed")
