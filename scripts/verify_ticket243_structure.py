from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket243-bandlimit-principal-unit-half-arc-dyadic-mimicry.v1"
AUDIT_KEY = "bandlimit_principal_unit_half_arc_dyadic_mimicry_audit"
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


def verify_ticket243_structure() -> str | None:
    integrated = (
        ROOT
        / "data/open-problem/ticket243-bandlimit-principal-unit-half-arc-dyadic-mimicry.json"
    )
    if not integrated.exists():
        return "missing TICKET-243 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-243 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-243 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    machine = root.get("machine_audit", {})
    expected_machine = {
        "exact_theorem_count": 4,
        "partial_theorem_count": 1,
        "exact_no_go_count": 3,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "collatz",
        "stagnated_problem_count": 0,
        "local_model_scan_limit": 50_000,
        "total_failure_count": 0,
    }
    for key, expected_value in expected_machine.items():
        if machine.get(key) != expected_value:
            return f"TICKET-243 machine field changed: {key}"

    expected = {
        "riemann": (
            "riemann",
            "BandlimitedEvenTestFamilyNoncompactnessAndFrequencyTightnessNoGo",
            "exact_no_go",
            "JointPhysicalFrequencyTightnessAndUniformSignedGuinandWeilTailWithPositiveMargin",
        ),
        "collatz": (
            "collatz",
            "UnboundedOrderPrincipalUnitTransferCountermodels",
            "exact_no_go",
            "FixedBaseRationalWieferichExclusionFor32Over27OnAllPrimeOrderCores",
        ),
        "goldbach": (
            "goldbach",
            "OmittedHalfFrequencyArcCarriesNaturalBinaryEnergy",
            "exact_no_go",
            "CompleteSmallDenominatorMajorArcCoverageAndSignedResidualBinaryCoefficientSaving",
        ),
        "twin_prime": (
            "twin-prime",
            "FixedPeriodicMimicryInEverySufficientlyLargeDyadicBlock",
            "partial_theorem",
            "ScaleLocalGrowingModulusTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass",
        ),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-243-bandlimit-noncompactness.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-243-principal-unit-transfer-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-243-half-arc-energy.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-243-dyadic-fixed-period-mimicry.json",
    }
    for key, (problem_id, theorem, classification, next_lemma) in expected.items():
        track = root.get(key, {})
        if track.get("problem_id") != problem_id:
            return f"TICKET-243 problem_id changed: {key}"
        if track.get("theorem_name") != theorem:
            return f"TICKET-243 theorem changed: {key}"
        if track.get("result_classification") != classification:
            return f"TICKET-243 result classification changed: {key}"
        if track.get("problem_status") != "open_not_proven":
            return f"TICKET-243 problem status changed: {key}"
        if track.get("stagnation_count") != 0:
            return f"TICKET-243 stagnation count changed: {key}"
        if track.get("route_decision", {}).get("next_single_lemma") != next_lemma:
            return f"TICKET-243 next lemma changed: {key}"
        nodes = track.get("proof_dag", {}).get("nodes", [])
        edges = track.get("proof_dag", {}).get("edges", [])
        if not nodes or any(node.get("status") not in ALLOWED_NODE_STATUSES for node in nodes):
            return f"TICKET-243 proof DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-243 open frontier count changed: {key}"
        if not dag_is_acyclic(nodes, edges):
            return f"TICKET-243 proof DAG is cyclic or malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-243 track JSON: {key}"
        track_payload = json.loads(paths[key].read_text(encoding="utf-8"))
        if track_payload.get("schema") != SCHEMA:
            return f"TICKET-243 track schema changed: {key}"

    riemann = root["riemann"]["reproducible_computation"]
    if len(riemann.get("exact_cosine_gram_rows", [])) != 5 or riemann.get("transcript_sha256") != "6b52e81598d394e05fffe373733e2a7638a9de662610abd8f1b63c59e46e90cf":
        return "TICKET-243 RH bandlimit certificate changed"
    collatz = root["collatz"]["reproducible_computation"]
    scan = collatz.get("bounded_universal_model_replay", {})
    if scan.get("primes_scanned") != 5_130 or scan.get("failure_count") != 0 or scan.get("largest_countermodel_order") != 24_999:
        return "TICKET-243 Collatz local-model replay changed"
    goldbach = root["goldbach"]["reproducible_computation"]
    if len(goldbach.get("exact_half_frequency_rows", [])) != 7:
        return "TICKET-243 Goldbach half-arc rows changed"
    twin = root["twin_prime"]["reproducible_computation"]
    rows = twin.get("finite_dyadic_witness_rows", [])
    if len(rows) != 16 or any(not row.get("certificate_verified") for row in rows):
        return "TICKET-243 Twin dyadic witness rows changed"

    attempts = payload.get("attempts", [])
    if [attempt.get("problem_id") for attempt in attempts] != ["riemann", "collatz", "goldbach", "twin-prime"] or any(attempt.get("status") != "open_not_proven" for attempt in attempts) or any(attempt.get("stagnation_count") != 0 for attempt in attempts):
        return "TICKET-243 attempt boundary changed"

    state_path = ROOT / "data/open-problem/four-problem-research-state.json"
    if not state_path.exists():
        return "missing persistent four-problem research state"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    ticket = state.get("ticket")
    retained_theorems = {
        "riemann": "BandlimitedEvenTestFamilyNoncompactnessAndFrequencyTightnessNoGo",
        "collatz": "UnboundedOrderPrincipalUnitTransferCountermodels",
        "goldbach": "OmittedHalfFrequencyArcCarriesNaturalBinaryEnergy",
        "twin_prime": "FixedPeriodicMimicryInEverySufficientlyLargeDyadicBlock",
    }
    if not isinstance(ticket, int) or ticket < 243 or state.get("resolved_count") != 0 or state.get("candidate_resolution_count") != 0 or state.get("program_complete") or any(
        theorem not in state.get("problems", {}).get(problem, {}).get("established_results", [])
        for problem, theorem in retained_theorems.items()
    ):
        return "TICKET-243 persistent research state changed"

    required_docs = (
        ROOT / "docs/bandlimit-principal-unit-half-arc-dyadic-mimicry.md",
        ROOT / "docs/bandlimit-principal-unit-half-arc-dyadic-mimicry.ko.md",
    )
    if any(not path.exists() for path in required_docs):
        return "missing TICKET-243 bilingual report"
    return None


def main() -> int:
    error = verify_ticket243_structure()
    if error:
        print(error)
        return 1
    print("TICKET-243 structure verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
