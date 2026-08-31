from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket262-limsup-finiteharmonic-mod8-thirdorder.v1"
AUDIT_KEY = "limsup_finiteharmonic_mod8_thirdorder_audit"
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


def verify_ticket262_structure() -> str | None:
    integrated = (
        ROOT / "data/open-problem/ticket262-limsup-finiteharmonic-mod8-thirdorder.json"
    )
    if not integrated.exists():
        return "missing TICKET-262 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-262 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-262 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    machine = {
        "exact_theorem_count": 4,
        "new_partial_theorem_count": 3,
        "exact_no_go_count": 1,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "collatz",
        "stagnated_problem_count": 0,
        "riemann_strict_boundary_case_count": 64,
        "riemann_critical_boundary_case_count": 12,
        "collatz_harmonic_cutoff_replay_count": 5,
        "collatz_total_phase_case_count": 1152,
        "goldbach_actual_mod8_certificate_count": 3,
        "goldbach_sharpness_countermodel_count": 16,
        "twin_convergent_count": 1024,
        "twin_joint_third_order_pass_count": 0,
        "twin_maximum_denominator_digit_count": 519,
        "total_failure_count": 0,
    }
    for key, expected_value in machine.items():
        if root.get("machine_audit", {}).get(key) != expected_value:
            return f"TICKET-262 machine field changed: {key}"
    expected = {
        "riemann": (
            "riemann",
            "PacketLagMarginIffScaledSignedJumpLimsupBelowLimit",
            "partial_theorem",
            "ActualWeilPacketScaledDownwardJumpLimsupBelowLimit",
            "1d0e796a1808951ac38617fabf4e338df387ff4653b8c1f9461e2e211b2c2e95",
        ),
        "collatz": (
            "collatz",
            "EveryFixedFiniteWeylCutoffAngularDiscrepancyNoGo",
            "exact_no_go",
            "CanonicalFermatQuotientWeylSumsVanishForEveryNonzeroH",
            "fc9aa7f31e40f14a0005fe7d75fc732aca63add7bee8ff6fa258f4e733f4d023",
        ),
        "goldbach": (
            "goldbach",
            "Q3TieForcesMinusCountFourModuloEight",
            "partial_theorem",
            "Q3SpecialMinusOneResidueCountNeverFourModuloEight",
            "7c60dd5c0e26f01fcd138fba2088f29872ee60b43e25efe5fc6dbad0cce5e00f",
        ),
        "twin_prime": (
            "twin-prime",
            "BidirectionalThirdOrderCongruenceAnd1024ConvergentCertificate",
            "partial_theorem",
            "NoUniqueRootConvergentSatisfiesBothThirdOrderCongruences",
            "50287b950ca162a0f762bbe7b4ba0d0898871947e950e7e1f52168d4f5e197cd",
        ),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-262-limsup-criterion.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-262-finite-harmonic-cutoff-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-262-mod8-tie-obstruction.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-262-bidirectional-third-order.json",
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
            return f"TICKET-262 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-262 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-262 DAG open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-262 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-262 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-262 track JSON changed: {key}"
    collatz = root["collatz"]["reproducible_computation"]
    if [
        case.get("harmonic_cutoff_H")
        for case in collatz.get("exact_finite_harmonic_cutoff_cases", [])
    ] != [1, 2, 4, 8, 16]:
        return "TICKET-262 finite-harmonic replay changed"
    goldbach = root["goldbach"]["reproducible_computation"]
    if [
        row.get("minus_one_residue_count_mod_8")
        for row in goldbach.get("exact_q3_mod8_certificate_rows", [])
    ] != [7, 1, 7]:
        return "TICKET-262 q=3 modulo-eight witnesses changed"
    twin = root["twin_prime"]["reproducible_computation"]
    if (
        twin.get("denominator_third_order_nontrivial_passes") != []
        or twin.get("numerator_third_order_nontrivial_passes") != []
        or twin.get("joint_third_order_passes") != []
    ):
        return "TICKET-262 third-order certificate changed"
    state = json.loads(
        (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
            encoding="utf-8"
        )
    )
    if (
        state.get("ticket", 0) < 262
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
    ):
        return "TICKET-262 persistent research state changed"
    if state.get("ticket") == 262 and (
        state.get("parent_ticket") != 261
        or state.get("deep_focus_problem") != "collatz"
    ):
        return "TICKET-262 persistent research state changed"
    for key, (_, theorem, _, _, _) in expected.items():
        if theorem not in state.get("problems", {}).get(key, {}).get(
            "established_results", []
        ):
            return f"TICKET-262 theorem missing from successor state: {key}"
    for report in (
        ROOT / "docs/limsup-finiteharmonic-mod8-thirdorder.md",
        ROOT / "docs/limsup-finiteharmonic-mod8-thirdorder.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-262 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket262_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-262 structure verification passed")
