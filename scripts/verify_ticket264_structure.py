from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket264-asymmetric-threshold-fixed2adic-head.v1"
AUDIT_KEY = "asymmetric_threshold_fixed2adic_head_audit"
ALLOWED = {"proved", "disproved", "computed_finite", "external_theorem", "assumption", "heuristic", "open"}


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


def verify_ticket264_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket264-asymmetric-threshold-fixed2adic-head.json"
    if not integrated.exists():
        return "missing TICKET-264 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-264 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-264 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    machine_expected = {
        "exact_theorem_count": 4, "new_partial_theorem_count": 3,
        "exact_no_go_count": 1, "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0, "proof_dag_count": 4,
        "next_single_lemma_count": 4, "deep_focus_problem": "riemann",
        "stagnated_problem_count": 0, "riemann_replay_case_count": 192,
        "collatz_grid_replay_count": 6, "collatz_harmonic_threshold_case_count": 252,
        "goldbach_phase_period_replay_count": 16,
        "goldbach_fixed_modulus_countermodel_count": 242,
        "twin_head_certificate_row_count": 39, "twin_subthreshold_convergent_count": 38,
        "twin_first_above_threshold_term_index": 38, "total_failure_count": 0,
    }
    if root.get("machine_audit") != machine_expected:
        return "TICKET-264 machine boundary changed"
    expected = {
        "riemann": ("riemann", "AsymmetricReciprocalEnvelopeForScaledJumpMargin", "partial_theorem", "ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit", "6e19883f2161d8c5b312d882bd9b273885f7a6a70acb2045d979b1796623099a"),
        "collatz": ("collatz", "PointwiseWeylCancellationIffExplicitThresholdCutoffDiverges", "partial_theorem", "CanonicalFermatQuotientThresholdCutoffDiverges", "eff593194a2fdaa1dc70665a18cfe69598bde8468da4135f2d41e6195e5902eb"),
        "goldbach": ("goldbach", "EveryFixedTwoAdicTieSignatureHasNonTieCountModels", "exact_no_go", "Q3SpecialPrimeRaceAbsoluteGapAtLeastTwo", "2e35b078945a1ddc732a322fb6aa44941ad6d3706f374991f62f2d64b0d5c3fb"),
        "twin_prime": ("twin-prime", "AllSubthresholdUniqueRootConvergentsAreUnitFree", "partial_theorem", "NoLaterUniqueRootConvergentSatisfiesJointNinthOrderCongruences", "53b7d19352a60fad2e2c26ec11b6f4d9cf5b3e3a879620251b024171657ccaf6"),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-264-asymmetric-reciprocal-envelope.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-264-explicit-threshold-cutoff.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-264-fixed-two-adic-no-go.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-264-subthreshold-head.json",
    }
    for key, (problem_id, theorem, classification, next_lemma, digest) in expected.items():
        item = root.get(key, {})
        boundary = (
            item.get("problem_id"), item.get("theorem_name"), item.get("result_classification"),
            item.get("problem_status"), item.get("route_decision", {}).get("next_single_lemma"),
            item.get("reproducible_computation", {}).get("transcript_sha256"),
        )
        if boundary != (problem_id, theorem, classification, "open_not_proven", next_lemma, digest):
            return f"TICKET-264 problem boundary changed: {key}"
        dag = item.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-264 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1 or not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-264 DAG malformed: {key}"
        if not paths[key].exists():
            return f"missing TICKET-264 track JSON: {key}"
    state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
    ticket = state.get("ticket")
    if (
        not isinstance(ticket, int)
        or ticket < 264
        or state.get("parent_ticket") != ticket - 1
        or state.get("deep_focus_problem") not in state.get("problems", {})
        or state.get("resolved_count") != 0
        or state.get("candidate_resolution_count") != 0
        or state.get("program_complete") is not False
    ):
        return "TICKET-264 persistent state changed"
    for report in (ROOT / "docs/asymmetric-threshold-fixed2adic-head.md", ROOT / "docs/asymmetric-threshold-fixed2adic-head.ko.md"):
        if not report.exists():
            return "missing TICKET-264 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket264_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-264 structure verification passed")
