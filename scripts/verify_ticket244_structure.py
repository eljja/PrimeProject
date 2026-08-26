from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket244-joint-tightness-harmonic-parity-fold-polylog-mimicry.v1"
AUDIT_KEY = "joint_tightness_harmonic_parity_fold_polylog_mimicry_audit"
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


def verify_ticket244_structure() -> str | None:
    integrated = ROOT / (
        "data/open-problem/ticket244-joint-tightness-harmonic-parity-fold-"
        "polylog-mimicry.json"
    )
    if not integrated.exists():
        return "missing TICKET-244 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-244 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-244 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    machine = root.get("machine_audit", {})
    expected_machine = {
        "exact_theorem_count": 4,
        "partial_theorem_count": 3,
        "exact_no_go_count": 1,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "twin_prime",
        "stagnated_problem_count": 0,
        "harmonic_scan_limit": 20_000,
        "goldbach_finite_limit": 10_000,
        "twin_witness_count": 4,
        "total_failure_count": 0,
    }
    for key, expected_value in expected_machine.items():
        if machine.get(key) != expected_value:
            return f"TICKET-244 machine field changed: {key}"

    expected = {
        "riemann": (
            "riemann",
            "JointPhysicalFrequencyTightnessCharacterizesL2Precompactness",
            "partial_theorem",
            "UniformSignedGuinandWeilTailWithPositiveMarginOnExhaustiveJointlyTightAdmissibleClasses",
        ),
        "collatz": (
            "collatz",
            "FixedBaseBadLineHarmonicSumEquivalence",
            "partial_theorem",
            "FixedBaseHarmonicBadLineNonvanishingForEveryPrime",
        ),
        "goldbach": (
            "goldbach",
            "ExactParityArcFoldingForEvenBinaryGoldbach",
            "partial_theorem",
            "CompleteDenominatorAtLeastThreeMajorArcExtractionAndSignedResidualSavingAfterParityFolding",
        ),
        "twin_prime": (
            "twin-prime",
            "PolylogarithmicGrowingPeriodMimicryInEveryLargeDyadicBlock",
            "exact_no_go",
            "SuperPolylogarithmicScaleLocalTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass",
        ),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-244-joint-tightness-compactness.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-244-harmonic-bad-line-reduction.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-244-parity-arc-folding.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-244-polylog-periodic-mimicry.json",
    }
    for key, (problem_id, theorem, classification, next_lemma) in expected.items():
        track = root.get(key, {})
        if track.get("problem_id") != problem_id:
            return f"TICKET-244 problem_id changed: {key}"
        if track.get("theorem_name") != theorem:
            return f"TICKET-244 theorem changed: {key}"
        if track.get("result_classification") != classification:
            return f"TICKET-244 result classification changed: {key}"
        if track.get("problem_status") != "open_not_proven":
            return f"TICKET-244 problem status changed: {key}"
        if track.get("stagnation_count") != 0:
            return f"TICKET-244 stagnation count changed: {key}"
        if track.get("route_decision", {}).get("next_single_lemma") != next_lemma:
            return f"TICKET-244 next lemma changed: {key}"
        nodes = track.get("proof_dag", {}).get("nodes", [])
        edges = track.get("proof_dag", {}).get("edges", [])
        if not nodes or any(
            node.get("status") not in ALLOWED_NODE_STATUSES for node in nodes
        ):
            return f"TICKET-244 proof DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-244 open frontier count changed: {key}"
        if not dag_is_acyclic(nodes, edges):
            return f"TICKET-244 proof DAG is cyclic or malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-244 track JSON: {key}"
        track_payload = json.loads(paths[key].read_text(encoding="utf-8"))
        if track_payload.get("schema") != SCHEMA:
            return f"TICKET-244 track schema changed: {key}"

    riemann = root["riemann"]["reproducible_computation"]
    if (
        len(riemann.get("physical_only_counterfamily_gram_rows", [])) != 5
        or len(riemann.get("exact_translation_bound_rows", [])) != 5
        or riemann.get("transcript_sha256")
        != "ba395b597b5ad65a2e1542934cb1781646c445f36e3b2828931e423fde04b07b"
    ):
        return "TICKET-244 RH compactness certificate changed"
    collatz = root["collatz"]["reproducible_computation"]
    replay = collatz.get("bounded_harmonic_replay", {})
    if (
        replay.get("primes_scanned") != 2_259
        or replay.get("bad_line_count") != 0
        or replay.get("failure_count") != 0
    ):
        return "TICKET-244 Collatz harmonic replay changed"
    goldbach = root["goldbach"]["reproducible_computation"]
    if (
        len(goldbach.get("exact_parity_fold_rows", [])) != 5
        or goldbach.get("aggregate", {}).get("finite_even_targets_checked") != 8_290
    ):
        return "TICKET-244 Goldbach parity-fold rows changed"
    twin = root["twin_prime"]["reproducible_computation"]
    twin_rows = twin.get("finite_polylog_period_witness_rows", [])
    if len(twin_rows) != 4 or any(
        not row.get("certificate_verified") for row in twin_rows
    ):
        return "TICKET-244 Twin polylog witness rows changed"

    state_path = ROOT / "data/open-problem/four-problem-research-state.json"
    if not state_path.exists():
        return "missing persistent four-problem research state"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    ticket = state.get("ticket")
    retained_theorems = {
        "riemann": "JointPhysicalFrequencyTightnessCharacterizesL2Precompactness",
        "collatz": "FixedBaseBadLineHarmonicSumEquivalence",
        "goldbach": "ExactParityArcFoldingForEvenBinaryGoldbach",
        "twin_prime": "PolylogarithmicGrowingPeriodMimicryInEveryLargeDyadicBlock",
    }
    if (
        not isinstance(ticket, int)
        or ticket < 244
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
        or any(
            theorem
            not in state.get("problems", {})
            .get(problem, {})
            .get("established_results", [])
            for problem, theorem in retained_theorems.items()
        )
    ):
        return "TICKET-244 persistent research state changed"

    required_docs = (
        ROOT / "docs/joint-tightness-harmonic-parity-fold-polylog-mimicry.md",
        ROOT / "docs/joint-tightness-harmonic-parity-fold-polylog-mimicry.ko.md",
    )
    if any(not path.exists() for path in required_docs):
        return "missing TICKET-244 bilingual report"
    return None


def main() -> int:
    error = verify_ticket244_structure()
    if error:
        print(error)
        return 1
    print("TICKET-244 structure verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
