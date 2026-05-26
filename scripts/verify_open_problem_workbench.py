from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generate_open_problem_workbench import build_payload, hash_leaf


def canonical(payload: dict[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Recompute and verify open problem bounded certificates.")
    parser.add_argument("--input", type=Path, default=Path("data/open_problem_workbench.json"))
    args = parser.parse_args()

    public_payload = json.loads(args.input.read_text(encoding="utf-8"))
    rebuilt = build_payload(
        int(public_payload["search_limit"]),
        generated_at=str(public_payload["generated_at"]),
    )

    if canonical(public_payload) != canonical(rebuilt):
        public_by_id = {problem["id"]: problem for problem in public_payload.get("problems", [])}
        rebuilt_by_id = {problem["id"]: problem for problem in rebuilt.get("problems", [])}
        mismatches = []
        for problem_id, problem in rebuilt_by_id.items():
            if canonical(public_by_id.get(problem_id, {})) != canonical(problem):
                mismatches.append(problem_id)
        print(
            "Open problem workbench reproduction failed: "
            + (", ".join(mismatches) if mismatches else "top-level metadata"),
            file=sys.stderr,
        )
        return 1

    summary = rebuilt.get("proof_status_gate_summary", {})
    if summary.get("status") != "all_full_proof_claims_blocked":
        print("Open problem proof status gate is not blocking full-proof claims.", file=sys.stderr)
        return 1
    for problem in rebuilt.get("problems", []):
        gate = problem.get("proof_status_gate", {})
        if gate.get("promotion_status") != "blocked_open_infinite_obligation":
            print(f"{problem.get('id')} proof promotion gate is not blocked.", file=sys.stderr)
            return 1
        if not gate.get("open_obligations") or not gate.get("open_attack_graph_links"):
            print(f"{problem.get('id')} proof promotion gate is missing open blockers.", file=sys.stderr)
            return 1
        contract = problem.get("formal_proof_contract", {})
        if contract.get("status") != "not_formalized_open":
            print(f"{problem.get('id')} formal proof contract status is not open.", file=sys.stderr)
            return 1
        if "sorry" not in " ".join(contract.get("acceptance_rules", [])):
            print(f"{problem.get('id')} formal proof contract does not ban unchecked proof holes.", file=sys.stderr)
            return 1
        queue = problem.get("proof_milestone_queue", {})
        milestones = queue.get("milestones", [])
        if queue.get("status") != "bounded_only_infinite_proof_open":
            print(f"{problem.get('id')} proof milestone queue has unexpected status.", file=sys.stderr)
            return 1
        if len(milestones) < 5 or queue.get("completed_count") != 1 or queue.get("open_count", 0) < 3:
            print(f"{problem.get('id')} proof milestone queue does not expose the expected open work.", file=sys.stderr)
            return 1
        lab = problem.get("decisive_lemma_lab", {})
        if lab.get("status") != "active_not_proven":
            print(f"{problem.get('id')} decisive lemma lab has unexpected status.", file=sys.stderr)
            return 1
        if not lab.get("proof_obligation") or not lab.get("falsification_test"):
            print(f"{problem.get('id')} decisive lemma lab is missing proof or falsification terms.", file=sys.stderr)
            return 1
        if not lab.get("closes_milestones") or not lab.get("finite_probe"):
            print(f"{problem.get('id')} decisive lemma lab is not tied to milestones and finite probes.", file=sys.stderr)
            return 1
        probe = lab.get("automated_falsification_probe", {})
        if probe.get("result_status") != "bounded_probe_passed_proof_open":
            print(f"{problem.get('id')} decisive lemma falsification probe has unexpected status.", file=sys.stderr)
            return 1
        if not probe.get("pass_condition") or not probe.get("proof_gap"):
            print(f"{problem.get('id')} decisive lemma falsification probe is missing pass/gap terms.", file=sys.stderr)
            return 1
        certificate = probe.get("probe_certificate", {})
        if certificate.get("status") != "probe_payload_certified":
            print(f"{problem.get('id')} decisive lemma probe certificate has unexpected status.", file=sys.stderr)
            return 1
        uncertified_probe = dict(probe)
        uncertified_probe.pop("probe_certificate", None)
        expected_hash = hash_leaf(json.dumps(uncertified_probe, sort_keys=True, separators=(",", ":")))
        if certificate.get("payload_sha256") != expected_hash or certificate.get("merkle_root") != expected_hash:
            print(f"{problem.get('id')} decisive lemma probe certificate hash mismatch.", file=sys.stderr)
            return 1
        taxonomy = lab.get("proof_gap_taxonomy", {})
        gaps = taxonomy.get("gaps", [])
        if taxonomy.get("status") != "proof_gaps_open":
            print(f"{problem.get('id')} proof gap taxonomy has unexpected status.", file=sys.stderr)
            return 1
        if len(gaps) < 4 or taxonomy.get("open_gap_count", 0) < 3:
            print(f"{problem.get('id')} proof gap taxonomy is missing open proof gaps.", file=sys.stderr)
            return 1
        if not all(gap.get("required_artifact") for gap in gaps):
            print(f"{problem.get('id')} proof gap taxonomy is missing required artifacts.", file=sys.stderr)
            return 1
        if not all(gap.get("next_experiment") and gap.get("failure_signal") for gap in gaps):
            print(f"{problem.get('id')} proof gap taxonomy is missing work-order fields.", file=sys.stderr)
            return 1
        protocol = problem.get("proof_execution_protocol", {})
        stages = protocol.get("stages", []) if isinstance(protocol, dict) else []
        if protocol.get("status") != "blocked_before_full_proof":
            print(f"{problem.get('id')} proof execution protocol has unexpected status.", file=sys.stderr)
            return 1
        if len(stages) < 5 or not protocol.get("primary_next_experiment") or not protocol.get("primary_failure_signal"):
            print(f"{problem.get('id')} proof execution protocol is missing execution steps.", file=sys.stderr)
            return 1
        if not any(stage.get("status") == "complete" for stage in stages):
            print(f"{problem.get('id')} proof execution protocol is missing the bounded complete stage.", file=sys.stderr)
            return 1
        if not any(stage.get("status") == "blocked_open_infinite_obligation" for stage in stages):
            print(f"{problem.get('id')} proof execution protocol is missing the full-proof gate stage.", file=sys.stderr)
            return 1
        frontier = problem.get("proof_frontier_probe", {})
        if frontier.get("status") != "finite_probe_not_proof":
            print(f"{problem.get('id')} proof frontier probe has unexpected status.", file=sys.stderr)
            return 1
        if not frontier.get("metrics") or not frontier.get("observations"):
            print(f"{problem.get('id')} proof frontier probe is missing metrics or observations.", file=sys.stderr)
            return 1
        if not frontier.get("proof_pressure") or not frontier.get("failure_signal"):
            print(f"{problem.get('id')} proof frontier probe is missing pressure or failure terms.", file=sys.stderr)
            return 1
        barrier_audit = problem.get("known_barrier_audit", {})
        barriers = barrier_audit.get("barriers", []) if isinstance(barrier_audit, dict) else []
        if barrier_audit.get("status") != "barriers_not_cleared":
            print(f"{problem.get('id')} known barrier audit has unexpected status.", file=sys.stderr)
            return 1
        if len(barriers) < 4 or barrier_audit.get("open_count", 0) < 4:
            print(f"{problem.get('id')} known barrier audit is missing open barriers.", file=sys.stderr)
            return 1
        if not all(barrier.get("why_it_matters") and barrier.get("required_clearance") for barrier in barriers):
            print(f"{problem.get('id')} known barrier audit is missing barrier clearance terms.", file=sys.stderr)
            return 1
        replay = problem.get("formal_replay_package", {})
        if replay.get("status") != "not_replayable_until_barriers_clear":
            print(f"{problem.get('id')} formal replay package has unexpected status.", file=sys.stderr)
            return 1
        if len(replay.get("candidate_files", [])) < 4 or len(replay.get("replay_commands", [])) < 4:
            print(f"{problem.get('id')} formal replay package is missing files or commands.", file=sys.stderr)
            return 1
        if not replay.get("required_artifacts") or not replay.get("forbidden_tokens"):
            print(f"{problem.get('id')} formal replay package is missing artifacts or forbidden tokens.", file=sys.stderr)
            return 1
        docket = problem.get("proof_review_docket", {})
        verdicts = docket.get("verdicts", []) if isinstance(docket, dict) else []
        if docket.get("status") != "full_proof_not_accepted":
            print(f"{problem.get('id')} proof review docket has unexpected status.", file=sys.stderr)
            return 1
        if len(verdicts) < 4 or not any(item.get("verdict") == "accepted_for_committed_limit" for item in verdicts):
            print(f"{problem.get('id')} proof review docket is missing bounded acceptance.", file=sys.stderr)
            return 1
        if not any(item.get("verdict") == "rejected_currently" for item in verdicts):
            print(f"{problem.get('id')} proof review docket is missing full-proof rejection.", file=sys.stderr)
            return 1
        if not docket.get("minimum_acceptance_conditions") or not docket.get("rejection_rule"):
            print(f"{problem.get('id')} proof review docket is missing review rules.", file=sys.stderr)
            return 1
        reduction = problem.get("proof_reduction_contract", {})
        if reduction.get("status") != "target_reduction_open":
            print(f"{problem.get('id')} proof reduction contract has unexpected status.", file=sys.stderr)
            return 1
        if reduction.get("bridge_status") != "open_missing_infinite_bridge":
            print(f"{problem.get('id')} proof reduction contract is missing an open bridge.", file=sys.stderr)
            return 1
        if not reduction.get("decisive_reduction") or len(reduction.get("accepted_partial_results", [])) < 2:
            print(f"{problem.get('id')} proof reduction contract is missing reduction details.", file=sys.stderr)
            return 1
        if len(reduction.get("forbidden_shortcuts", [])) < 3 or len(reduction.get("review_questions", [])) < 3:
            print(f"{problem.get('id')} proof reduction contract is missing review guardrails.", file=sys.stderr)
            return 1
        if "open_not_proven" not in reduction.get("promotion_test", ""):
            print(f"{problem.get('id')} proof reduction contract is missing the promotion gate.", file=sys.stderr)
            return 1
        intake = problem.get("proof_candidate_intake", {})
        if intake.get("status") != "no_candidate_accepted":
            print(f"{problem.get('id')} proof candidate intake has unexpected status.", file=sys.stderr)
            return 1
        if intake.get("intake_stage") != "candidate_required":
            print(f"{problem.get('id')} proof candidate intake has unexpected stage.", file=sys.stderr)
            return 1
        if len(intake.get("required_submission", [])) < 4 or len(intake.get("first_executable_tests", [])) < 2:
            print(f"{problem.get('id')} proof candidate intake is missing required tests.", file=sys.stderr)
            return 1
        if len(intake.get("automatic_rejection_rules", [])) < 4:
            print(f"{problem.get('id')} proof candidate intake is missing rejection rules.", file=sys.stderr)
            return 1
        if "does not certify" not in intake.get("claim_boundary", ""):
            print(f"{problem.get('id')} proof candidate intake is missing claim boundary.", file=sys.stderr)
            return 1
        execution_log = problem.get("proof_attempt_execution_log", {})
        attempts = execution_log.get("attempts", []) if isinstance(execution_log, dict) else []
        if execution_log.get("status") != "attempts_executed_no_full_proof":
            print(f"{problem.get('id')} proof attempt execution log has unexpected status.", file=sys.stderr)
            return 1
        if len(attempts) < 2:
            print(f"{problem.get('id')} proof attempt execution log is missing attempts.", file=sys.stderr)
            return 1
        if not all(attempt.get("failure_reason") and attempt.get("next_artifact") for attempt in attempts):
            print(f"{problem.get('id')} proof attempt execution log is missing failure details.", file=sys.stderr)
            return 1
        if "infinite bridge" not in execution_log.get("machine_verdict", ""):
            print(f"{problem.get('id')} proof attempt execution log is missing the infinite bridge verdict.", file=sys.stderr)
            return 1
        dag = problem.get("proof_obligation_dag", {})
        nodes = dag.get("nodes", []) if isinstance(dag, dict) else []
        edges = dag.get("edges", []) if isinstance(dag, dict) else []
        if dag.get("status") != "open_obligation_graph":
            print(f"{problem.get('id')} proof obligation DAG has unexpected status.", file=sys.stderr)
            return 1
        if len(nodes) < 10 or len(edges) < 10 or dag.get("open_node_count", 0) < 5:
            print(f"{problem.get('id')} proof obligation DAG is missing graph coverage.", file=sys.stderr)
            return 1
        if not any(node.get("type") == "target" and node.get("status") == "open_not_proven" for node in nodes):
            print(f"{problem.get('id')} proof obligation DAG is missing open target node.", file=sys.stderr)
            return 1
        if not dag.get("critical_path") or "formal artifact" not in dag.get("machine_rule", ""):
            print(f"{problem.get('id')} proof obligation DAG is missing machine rule.", file=sys.stderr)
            return 1

    certificate_roots = {
        problem["id"]: problem["certificate"]["merkle_root"]
        for problem in rebuilt["problems"]
    }
    print(
        "Open problem bounded certificates reproduce exactly: "
        + ", ".join(f"{key}={value[:12]}" for key, value in certificate_roots.items())
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
