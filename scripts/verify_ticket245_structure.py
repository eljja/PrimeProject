from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket245-closure-second-order-klein-linnik.v1"
AUDIT_KEY = "closure_second_order_klein_linnik_audit"
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


def verify_ticket245_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket245-closure-second-order-klein-linnik.json"
    if not integrated.exists():
        return "missing TICKET-245 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-245 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-245 completion boundary changed"
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
        "first_layer_scan_limit": 20_000_000,
        "second_order_scan_limit": 50_000,
        "farey_denominator_limit": 128,
        "twin_witness_count": 5,
        "total_failure_count": 0,
    }
    for key, expected_value in expected_machine.items():
        if machine.get(key) != expected_value:
            return f"TICKET-245 machine field changed: {key}"

    expected = {
        "riemann": ("riemann", "ClosureZeroSetObstructionToUniformWeilMargin", "exact_no_go", "ZeroFreeClosureSeparationForNormalizedAdmissibleWeilFunctional"),
        "collatz": ("collatz", "SecondOrderFixedBaseFermatDigitCriterion", "partial_theorem", "FixedBaseAllPrimeRationalWieferichDepthDomination"),
        "goldbach": ("goldbach", "KleinFourOrbitReductionForEvenGoldbachArcs", "partial_theorem", "UniformRepresentativeArcAsymptoticAndSignedResidualSavingOnQuarterTorus"),
        "twin_prime": ("twin-prime", "PolynomialHeightPeriodicMimicryFromLinnik", "exact_no_go", "ScaleLocalNonperiodicTypeIICancellationBeyondPeriodicHeightBarriers"),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-245-closure-zero-margin.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-245-second-order-fermat-digit.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-245-klein-rational-arc-orbits.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-245-linnik-polynomial-height-mimicry.json",
    }
    for key, (problem_id, theorem_name, classification, next_lemma) in expected.items():
        section = root.get(key, {})
        if section.get("problem_id") != problem_id:
            return f"TICKET-245 problem_id changed: {key}"
        if section.get("theorem_name") != theorem_name:
            return f"TICKET-245 theorem changed: {key}"
        if section.get("result_classification") != classification:
            return f"TICKET-245 classification changed: {key}"
        if section.get("problem_status") != "open_not_proven":
            return f"TICKET-245 problem status changed: {key}"
        if section.get("route_decision", {}).get("next_single_lemma") != next_lemma:
            return f"TICKET-245 next lemma changed: {key}"
        if section.get("stagnation_count") != 0:
            return f"TICKET-245 stagnation count changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED_NODE_STATUSES for node in nodes):
            return f"TICKET-245 proof DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-245 open frontier count changed: {key}"
        if not dag_is_acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-245 proof DAG is cyclic or malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-245 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem_name:
            return f"TICKET-245 track JSON changed: {key}"

    rh = root["riemann"]["reproducible_computation"]
    if rh.get("transcript_sha256") != "5e329477cb0a2f420f406b1b9f94483f36d9026bb1ef22542c31b68ac139cbb1" or len(rh.get("exact_exhaustion_margin_rows", [])) != 6:
        return "TICKET-245 RH margin certificate changed"
    co = root["collatz"]["reproducible_computation"]
    if co.get("transcript_sha256") != "26b7da7bc74a887b9b954122bc61dfc4277277cbde99e063505e8d6ebbd1423f" or co.get("adversarial_first_layer_scan", {}).get("primes_scanned") != 1_270_604 or co.get("adversarial_first_layer_scan", {}).get("bad_line_prime_count") != 0:
        return "TICKET-245 Collatz second-order certificate changed"
    gb = root["goldbach"]["reproducible_computation"]
    if gb.get("transcript_sha256") != "92774e213632ee5eb153236bafe3c0b03ec914994db4b4b668b22224c52d6639" or gb.get("exact_rational_center_orbit_rows", [])[-1].get("canonical_quarter_torus_orbit_count") != 1882:
        return "TICKET-245 Goldbach orbit certificate changed"
    tp = root["twin_prime"]["reproducible_computation"]
    if tp.get("transcript_sha256") != "9c40a7487d40b111bb2e9ebc9c4bc9cbcf4edaf9ed73d931632d5df78bd32e98" or len(tp.get("exact_polynomial_height_witness_rows", [])) != 5:
        return "TICKET-245 Twin Linnik certificate changed"

    state_path = ROOT / "data/open-problem/four-problem-research-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    ticket = state.get("ticket")
    if (
        not isinstance(ticket, int)
        or ticket < 245
        or state.get("parent_ticket") != ticket - 1
    ):
        return "TICKET-245 persistent research state changed"
    if state.get("resolved_count") != 0 or state.get("candidate_resolution_count") != 0 or state.get("program_complete"):
        return "TICKET-245 resolution boundary changed"
    for report in (
        ROOT / "docs/closure-second-order-klein-linnik.md",
        ROOT / "docs/closure-second-order-klein-linnik.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-245 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket245_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-245 structure verification passed")
