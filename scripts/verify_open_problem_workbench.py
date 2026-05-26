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
