from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket265-sparse-cutoff-growing2adic-mod32.v1"
AUDIT_KEY = "sparse_cutoff_growing2adic_mod32_audit"
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


def verify_ticket265_structure() -> str | None:
    integrated = ROOT / "data/open-problem/ticket265-sparse-cutoff-growing2adic-mod32.json"
    if not integrated.exists():
        return "missing TICKET-265 integrated audit"
    payload = json.loads(integrated.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA or payload.get("status") != "open_not_proven":
        return "TICKET-265 schema or status changed"
    if not payload.get("iteration_complete") or payload.get("program_complete"):
        return "TICKET-265 completion boundary changed"
    root = payload.get(AUDIT_KEY, {})
    machine = root.get("machine_audit", {})
    required_machine = {
        "exact_theorem_count": 4,
        "new_partial_theorem_count": 2,
        "exact_no_go_count": 2,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "collatz",
        "total_failure_count": 0,
    }
    if any(machine.get(key) != value for key, value in required_machine.items()):
        return "TICKET-265 machine boundary changed"
    expected = {
        "riemann": ("riemann", "DensityOneReciprocalControlCannotReplaceLimsupEnvelope", "exact_no_go", "ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit"),
        "collatz": ("collatz", "UnboundedExplicitThresholdCutoffDoesNotImplyDivergence", "exact_no_go", "CanonicalFermatQuotientThresholdCutoffHasNoBoundedSubsequence"),
        "goldbach": ("goldbach", "GrowingTwoAdicTieSignatureIsSharpAndDecisive", "partial_theorem", "Q3ActualMinusCountAvoidsLeastDecisiveTwoAdicTieResidue"),
        "twin_prime": ("twin-prime", "PrimitiveTwinUnitSolutionsObeyMod32DiagonalFilter", "partial_theorem", "EveryLaterMod32FilterPassFailsJointNinthOrderCongruences"),
    }
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-265-density-one-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-265-unbounded-cutoff-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-265-growing-two-adic-threshold.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-265-mod32-diagonal-filter.json",
    }
    for key, boundary in expected.items():
        item = root.get(key, {})
        actual = (
            item.get("problem_id"), item.get("theorem_name"), item.get("result_classification"),
            item.get("route_decision", {}).get("next_single_lemma"),
        )
        if actual != boundary or item.get("problem_status") != "open_not_proven":
            return f"TICKET-265 problem boundary changed: {key}"
        dag = item.get("proof_dag", {})
        nodes = dag.get("nodes", [])
        if any(node.get("status") not in ALLOWED for node in nodes):
            return f"TICKET-265 DAG status changed: {key}"
        if sum(node.get("status") == "open" for node in nodes) != 1 or not acyclic(nodes, dag.get("edges", [])):
            return f"TICKET-265 DAG malformed: {key}"
        track_payload = json.loads(paths[key].read_text(encoding="utf-8")) if paths[key].exists() else None
        if not track_payload or track_payload.get("theorem_name") != boundary[1]:
            return f"missing or stale TICKET-265 track JSON: {key}"
    state = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
    state_boundary = (
        state.get("ticket"), state.get("parent_ticket"), state.get("deep_focus_problem"),
        state.get("resolved_count"), state.get("candidate_resolution_count"), state.get("program_complete"),
    )
    if state_boundary != (265, 264, "collatz", 0, 0, False):
        return "TICKET-265 persistent state changed"
    for report in (ROOT / "docs/sparse-cutoff-growing2adic-mod32.md", ROOT / "docs/sparse-cutoff-growing2adic-mod32.ko.md"):
        if not report.exists():
            return "missing TICKET-265 bilingual report"
    return None


if __name__ == "__main__":
    error = verify_ticket265_structure()
    if error:
        raise SystemExit(error)
    print("TICKET-265 structure verification passed")
