from __future__ import annotations

import json
import sys
from pathlib import Path


FORBIDDEN_FORMAL_TOKENS = ["sorry", "admit", "axiom "]
EXPECTED_PROBLEMS = {"riemann", "collatz", "goldbach", "twin-prime"}
EXPECTED_TARGET_VERDICT = "not_proved_by_primeproject"
EXPECTED_GATE_STATUS = "blocked_open_infinite_obligation"
PROOF_OR_COUNTEREXAMPLE_SCHEMA = "primeproject.proof-or-counterexample-lab.v1"


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    payload_path = Path("data/open_problem_workbench.json")
    if not payload_path.exists():
        return fail("missing data/open_problem_workbench.json")

    payload = read_json(payload_path)
    problems = payload.get("problems", [])
    if not isinstance(problems, list):
        return fail("workbench problems must be a list")

    by_id = {str(problem.get("id")): problem for problem in problems if isinstance(problem, dict)}
    missing = EXPECTED_PROBLEMS - set(by_id)
    if missing:
        return fail("missing open-problem pages: " + ", ".join(sorted(missing)))

    summary = payload.get("proof_status_gate_summary", {})
    if not isinstance(summary, dict) or summary.get("status") != "all_full_proof_claims_blocked":
        return fail("global proof-status gate must block all full-proof claims")

    for problem_id in sorted(EXPECTED_PROBLEMS):
        problem = by_id[problem_id]
        gate = problem.get("proof_status_gate", {})
        verdict = problem.get("proof_verdict", {})
        skeleton = problem.get("formal_skeleton_audit", {})
        frontier = problem.get("ai_proof_forge", {})

        if not isinstance(gate, dict) or gate.get("promotion_status") != EXPECTED_GATE_STATUS:
            return fail(f"{problem_id}: proof gate is not blocked")
        if not isinstance(verdict, dict) or verdict.get("target_verdict") != EXPECTED_TARGET_VERDICT:
            return fail(f"{problem_id}: proof verdict overclaims target")
        if not isinstance(skeleton, dict) or skeleton.get("forbidden_hit_count") != 0:
            return fail(f"{problem_id}: formal skeleton contains forbidden tokens")
        if not isinstance(frontier, dict) or frontier.get("status") != "active_unsolved_proof_forge":
            return fail(f"{problem_id}: AI proof forge status must remain unsolved")

        replay = problem.get("formal_replay_package", {})
        files = replay.get("candidate_files", []) if isinstance(replay, dict) else []
        if not files:
            return fail(f"{problem_id}: missing formal replay files")
        for file_name in files:
            path = Path(str(file_name))
            if not path.exists():
                return fail(f"{problem_id}: missing formal replay file {path}")
            text = path.read_text(encoding="utf-8")
            for token in FORBIDDEN_FORMAL_TOKENS:
                if token in text:
                    return fail(f"{problem_id}: forbidden formal token {token!r} in {path}")

        lab = problem.get("decisive_lemma_lab", {})
        gap_taxonomy = lab.get("proof_gap_taxonomy", {}) if isinstance(lab, dict) else {}
        gaps = gap_taxonomy.get("gaps", []) if isinstance(gap_taxonomy, dict) else []
        if not isinstance(gaps, list) or not gaps:
            return fail(f"{problem_id}: missing proof gaps")
        for gap in gaps:
            if not isinstance(gap, dict):
                return fail(f"{problem_id}: malformed proof gap")
            artifact = gap.get("required_artifact")
            if isinstance(artifact, str) and artifact.startswith("data/") and not Path(artifact).exists():
                return fail(f"{problem_id}: missing required artifact {artifact}")

    lab_path = Path("data/open-problem/proof-or-counterexample-lab.json")
    if not lab_path.exists():
        return fail("missing proof-or-counterexample lab artifact")
    lab = read_json(lab_path)
    if lab.get("schema") != PROOF_OR_COUNTEREXAMPLE_SCHEMA:
        return fail("proof-or-counterexample lab has unexpected schema")
    if lab.get("status") != "attempted_no_full_resolution":
        return fail("proof-or-counterexample lab overstates resolution")
    lab_problems = lab.get("problems", [])
    if not isinstance(lab_problems, list):
        return fail("proof-or-counterexample problems must be a list")
    lab_by_id = {str(problem.get("problem_id")): problem for problem in lab_problems if isinstance(problem, dict)}
    missing_lab = EXPECTED_PROBLEMS - set(lab_by_id)
    if missing_lab:
        return fail("proof-or-counterexample lab missing problems: " + ", ".join(sorted(missing_lab)))
    ticket_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-16-proof-or-counterexample.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-16-proof-or-counterexample.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-16-proof-or-counterexample.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-16-proof-or-counterexample.json"),
    }
    for problem_id, problem in lab_by_id.items():
        if problem.get("status") != "attempted_no_full_resolution":
            return fail(f"{problem_id}: proof-or-counterexample ticket overstates resolution")
        if not problem.get("direct_counterexample"):
            return fail(f"{problem_id}: missing direct counterexample section")
        if not problem.get("candidate_counterexamples_found"):
            return fail(f"{problem_id}: missing candidate counterexample section")
        if not problem.get("contrapositive_route"):
            return fail(f"{problem_id}: missing contrapositive route")
        if not problem.get("missing_infinite_bridge") or not problem.get("next_theorem_to_attempt"):
            return fail(f"{problem_id}: missing bridge or next theorem")
        if "No " not in str(problem.get("claim_boundary", "")):
            return fail(f"{problem_id}: proof-or-counterexample claim boundary is too weak")
        path = ticket_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket-16 artifact")

    print("open problem structure verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
