from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket250-multiplier-lift-galois-evenright.v1"
AUDIT_KEY = "multiplier_lift_galois_evenright_audit"
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


def verify_ticket250_structure() -> str | None:
    integrated_path = (
        ROOT / "data/open-problem/ticket250-multiplier-lift-galois-evenright.json"
    )
    if not integrated_path.exists():
        return "missing TICKET-250 integrated audit"
    payload = json.loads(integrated_path.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-250 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-250 completion boundary changed"
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
        "deep_focus_problem": "goldbach",
        "stagnated_problem_count": 0,
        "riemann_legendre_case_count": 9,
        "riemann_concentration_case_count": 12,
        "collatz_lift_pair_count": 73_901,
        "goldbach_prime_count_norm_case_count": 35,
        "goldbach_boundary_countermodel_count": 2,
        "twin_active_scale_count": 9,
        "total_failure_count": 0,
    }
    for key, expected in expected_machine.items():
        if machine.get(key) != expected:
            return f"TICKET-250 machine field changed: {key}"

    expected = {
        "riemann": (
            "riemann",
            "NoncompactMultiplierLegendreEscapeInsufficiencyNoGo",
            "exact_no_go",
            "ArithmeticWeilFormCoercivityAgainstOscillationAndConcentrationEscapes",
            "20099dd1cab1cbcfa5ef4863e9f3c115c9f59af2da902d05bdbe029b5a8c507b",
        ),
        "collatz": (
            "collatz",
            "LocalFermatQuotientLiftTransitivityNoGo",
            "exact_no_go",
            "CanonicalRepresentativeFermatQuotientDistributionBeyondLiftTransitivity",
            "08ee2ee2080e127c58f7120621b39d20213ce2f6cf71987aaf01c7099ad528c2",
        ),
        "goldbach": (
            "goldbach",
            "PrimeModulusRationalFourierFullSupportAndNormBarrier",
            "partial_theorem",
            "QuantitativePrimeCountFourierEnergyAntiConcentrationAtPrimeModuli",
            "684fea0b7645dea69f080eddb985918605ef6db23fde35646689556c8cf5c5a1",
        ),
        "twin_prime": (
            "twin-prime",
            "AllBaseEvenLeftRightActiveClassification",
            "partial_theorem",
            "ScaleLocalOddLeftRightActiveContaminationBound",
            "0cf8bd40771dca2cc7e0da725f6bffbaefb50d81c3d73d72731917568fa4dcda",
        ),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-250-noncompact-multiplier-escape.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-250-lift-transitivity.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-250-galois-full-support.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-250-even-left-right-classification.json",
    }
    for key, (problem_id, theorem, classification, next_lemma, digest) in expected.items():
        section = root.get(key, {})
        if (
            section.get("problem_id") != problem_id
            or section.get("theorem_name") != theorem
            or section.get("result_classification") != classification
            or section.get("problem_status") != "open_not_proven"
            or section.get("route_decision", {}).get("next_single_lemma") != next_lemma
            or section.get("reproducible_computation", {}).get("transcript_sha256")
            != digest
        ):
            return f"TICKET-250 problem boundary changed: {key}"
        dag = section.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-250 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1:
            return f"TICKET-250 open frontier changed: {key}"
        if not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-250 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-250 track JSON: {key}"
        track = json.loads(paths[key].read_text(encoding="utf-8"))
        if track.get("schema") != SCHEMA or track.get("theorem_name") != theorem:
            return f"TICKET-250 track JSON changed: {key}"

    if len(root["riemann"]["reproducible_computation"]["exact_legendre_multiplier_rows"]) != 9:
        return "TICKET-250 RH Legendre replay changed"
    if len(root["riemann"]["reproducible_computation"]["exact_concentration_escape_rows"]) != 12:
        return "TICKET-250 RH concentration replay changed"
    if sum(row["lift_pairs_checked"] for row in root["collatz"]["reproducible_computation"]["exact_lift_field_rows"]) != 73_901:
        return "TICKET-250 Collatz lift replay changed"
    if len(root["goldbach"]["reproducible_computation"]["exact_prime_count_norm_rows"]) != 35:
        return "TICKET-250 Goldbach norm replay changed"
    twin_rows = root["twin_prime"]["reproducible_computation"]["exact_scale_rows"]
    if len(twin_rows) != 9 or twin_rows[-1]["right_active_composite_pairs_R"] != 136:
        return "TICKET-250 Twin replay changed"
    if sum(
        node.get("status") == "external_theorem"
        for node in root["twin_prime"]["proof_dag"]["nodes"]
    ) != 1:
        return "TICKET-250 Twin external theorem boundary changed"

    state = json.loads(
        (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
            encoding="utf-8"
        )
    )
    if (
        state.get("ticket") != 250
        or state.get("parent_ticket") != 249
        or state.get("deep_focus_problem") != "goldbach"
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete")
    ):
        return "TICKET-250 persistent research state changed"
    for report in (
        ROOT / "docs/multiplier-lift-galois-evenright.md",
        ROOT / "docs/multiplier-lift-galois-evenright.ko.md",
    ):
        if not report.exists():
            return "missing TICKET-250 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket250_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-250 structure verification passed")
