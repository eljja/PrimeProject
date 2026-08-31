from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket263-sharp-envelope-diagonal-mod32-ninthorder.v1"
AUDIT_KEY = "sharp_envelope_diagonal_mod32_ninthorder_audit"
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


def verify_ticket263_structure() -> str | None:
    integrated = (
        ROOT
        / "data/open-problem/ticket263-sharp-envelope-diagonal-mod32-ninthorder.json"
    )
    if not integrated.exists():
        return "missing TICKET-263 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-263 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-263 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    machine = {
        "exact_theorem_count": 4,
        "new_partial_theorem_count": 4,
        "exact_no_go_count": 0,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "twin_prime",
        "stagnated_problem_count": 0,
        "riemann_replay_case_count": 192,
        "collatz_grid_replay_count": 5,
        "collatz_harmonic_case_count": 119,
        "goldbach_actual_mod32_certificate_count": 3,
        "goldbach_mod32_countermodel_count": 15,
        "twin_convergent_count": 1024,
        "twin_tail_exactness_applicable_count": 986,
        "twin_first_tail_exactness_term_index": 38,
        "twin_joint_ninth_order_pass_count": 0,
        "twin_maximum_denominator_digit_count": 519,
        "total_failure_count": 0,
    }
    for key, expected_value in machine.items():
        if root.get("machine_audit", {}).get(key) != expected_value:
            return f"TICKET-263 machine field changed: {key}"
    expected = {
        "riemann": (
            "riemann",
            "SharpReciprocalEnvelopeForScaledJumpMargin",
            "ActualWeilPacketReciprocalEnvelopeBelowHalfLimit",
            "419e873421db459aa17b81d92e6436b160c67faf03604f4d70f999a606c40fc1",
        ),
        "collatz": (
            "collatz",
            "PointwiseWeylCancellationIffSomeGrowingCutoffUniformCancellation",
            "CanonicalFermatQuotientGrowingCutoffUniformWeylCancellation",
            "22e5034bb28e5a95a31566c5c5d2b39817d88920c3cdb56add478f8b4364707e",
        ),
        "goldbach": (
            "goldbach",
            "Q3TieForcesLevelPhasedModuloThirtyTwo",
            "Q3SpecialMinusOneResidueCountAvoidsLevelPhasedModuloThirtyTwo",
            "56e7343267be9727182a5823af00472ac99896a1cdda8a6a381005135aebfd42",
        ),
        "twin_prime": (
            "twin-prime",
            "NinthOrderJointCongruenceExactOnRootCone",
            "NoUniqueRootConvergentSatisfiesJointNinthOrderCongruences",
            "fc07b6910a4ad7e83a0df7b467e2b864a9d35c342d6628c97365bfa43fc1352e",
        ),
    }
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-263-sharp-reciprocal-envelope.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-263-diagonal-weyl-uniformization.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-263-mod32-tie-phase.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-263-ninth-order-exactness.json",
    }
    for key, (problem_id, theorem, next_lemma, digest) in expected.items():
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
            "partial_theorem",
            "open_not_proven",
            next_lemma,
            digest,
        ):
            return f"TICKET-263 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-263 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-263 DAG open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-263 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-263 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-263 track JSON changed: {key}"
    riemann = root["riemann"]["reproducible_computation"]
    if [
        row.get("regime")
        for row in riemann.get("exact_alternating_reciprocal_envelope_families", [])
    ] != ["strict", "critical", "supercritical"]:
        return "TICKET-263 RH sharpness families changed"
    collatz = root["collatz"]["reproducible_computation"]
    if [
        row.get("grid_modulus_M")
        for row in collatz.get("exact_complete_grid_replays", [])
    ] != [4, 8, 16, 32, 64]:
        return "TICKET-263 Collatz grid replay changed"
    goldbach = root["goldbach"]["reproducible_computation"]
    if [
        row.get("tie_forced_mod_32")
        for row in goldbach.get("exact_actual_q3_mod32_certificate_rows", [])
    ] != [28, 4, 12]:
        return "TICKET-263 Goldbach modulo-32 witnesses changed"
    twin = root["twin_prime"]["reproducible_computation"]
    if (
        twin.get("absolute_coefficient_sum_A") != 2744210
        or twin.get("ninth_order_exactness_threshold_V_0")
        != "188580743973175296"
        or twin.get("joint_ninth_order_passes") != []
        or len(twin.get("degenerate_modulus_one_joint_ninth_order_passes", []))
        != 2
    ):
        return "TICKET-263 Twin ninth-order boundary changed"
    state = json.loads(
        (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
            encoding="utf-8"
        )
    )
    if (
        state.get("ticket", 0) < 263
        or state.get("parent_ticket", 0) < 262
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete") is not False
    ):
        return "TICKET-263 persistent research state changed"
    for key, (_, theorem, _, _) in expected.items():
        if theorem not in state.get("problems", {}).get(key, {}).get(
            "established_results", []
        ):
            return f"TICKET-263 theorem missing from research state: {key}"
    for report in (
        ROOT / "docs/sharp-envelope-diagonal-mod32-ninthorder.md",
        ROOT / "docs/sharp-envelope-diagonal-mod32-ninthorder.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-263 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket263_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-263 structure verification passed")
