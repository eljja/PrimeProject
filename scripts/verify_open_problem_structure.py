from __future__ import annotations

import json
import sys
from pathlib import Path


FORBIDDEN_FORMAL_TOKENS = ["sorry", "admit", "axiom "]
EXPECTED_PROBLEMS = {"riemann", "collatz", "goldbach", "twin-prime"}
EXPECTED_TARGET_VERDICT = "not_proved_by_primeproject"
EXPECTED_GATE_STATUS = "blocked_open_infinite_obligation"
PROOF_OR_COUNTEREXAMPLE_SCHEMA = "primeproject.proof-or-counterexample-lab.v1"
TICKET17_SCHEMA = "primeproject.ticket17-breakthrough-attempts.v1"
TICKET18_SCHEMA = "primeproject.ticket18-reduction-lab.v1"
TICKET19_SCHEMA = "primeproject.ticket19-proof-pressure-lab.v1"
TICKET20_SCHEMA = "primeproject.ticket20-valuation-prefix-lab.v1"
TICKET21_SCHEMA = "primeproject.ticket21-two-adic-branch-lab.v1"
TICKET22_SCHEMA = "primeproject.ticket22-negation-pressure-lab.v1"


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

    ticket17_path = Path("data/open-problem/ticket17-breakthrough-attempts.json")
    if not ticket17_path.exists():
        return fail("missing ticket17 breakthrough attempts artifact")
    ticket17 = read_json(ticket17_path)
    if ticket17.get("schema") != TICKET17_SCHEMA:
        return fail("ticket17 breakthrough attempts artifact has unexpected schema")
    if ticket17.get("status") != "breakthrough_attempts_open_no_resolution":
        return fail("ticket17 breakthrough attempts overstate resolution")
    attempts = ticket17.get("attempts", [])
    if not isinstance(attempts, list):
        return fail("ticket17 attempts must be a list")
    attempts_by_id = {str(attempt.get("problem_id")): attempt for attempt in attempts if isinstance(attempt, dict)}
    missing_attempts = EXPECTED_PROBLEMS - set(attempts_by_id)
    if missing_attempts:
        return fail("ticket17 attempts missing problems: " + ", ".join(sorted(missing_attempts)))
    ticket17_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-17-uniform-offcritical-detector.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-17-residue-debt-automaton-lift.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-17-residue-profile-explicit-cutoff.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-17-exact-gap-two-projection.json"),
    }
    for problem_id, attempt in attempts_by_id.items():
        if attempt.get("status") != "breakthrough_attempt_open":
            return fail(f"{problem_id}: ticket17 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket17 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket17 claim boundary is too weak")
        path = ticket17_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket17 per-problem artifact")

    ticket18_path = Path("data/open-problem/ticket18-reduction-lab.json")
    if not ticket18_path.exists():
        return fail("missing ticket18 reduction lab artifact")
    ticket18 = read_json(ticket18_path)
    if ticket18.get("schema") != TICKET18_SCHEMA:
        return fail("ticket18 reduction lab artifact has unexpected schema")
    if ticket18.get("status") != "reduction_attempts_open_no_resolution":
        return fail("ticket18 reduction lab overstates resolution")
    reductions = ticket18.get("attempts", [])
    if not isinstance(reductions, list):
        return fail("ticket18 attempts must be a list")
    reductions_by_id = {str(attempt.get("problem_id")): attempt for attempt in reductions if isinstance(attempt, dict)}
    missing_reductions = EXPECTED_PROBLEMS - set(reductions_by_id)
    if missing_reductions:
        return fail("ticket18 attempts missing problems: " + ", ".join(sorted(missing_reductions)))
    ticket18_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-18-finite-prefix-camouflage.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-18-valuation-branch-cover.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-18-explicit-error-budget.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-18-bounded-gap-countermodel.json"),
    }
    for problem_id, attempt in reductions_by_id.items():
        if attempt.get("status") != "reduction_attempt_open":
            return fail(f"{problem_id}: ticket18 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket18 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket18 claim boundary is too weak")
        path = ticket18_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket18 per-problem artifact")

    ticket19_path = Path("data/open-problem/ticket19-proof-pressure-lab.json")
    if not ticket19_path.exists():
        return fail("missing ticket19 proof pressure lab artifact")
    ticket19 = read_json(ticket19_path)
    if ticket19.get("schema") != TICKET19_SCHEMA:
        return fail("ticket19 proof pressure lab artifact has unexpected schema")
    if ticket19.get("status") != "proof_pressure_open_no_resolution":
        return fail("ticket19 proof pressure lab overstates resolution")
    pressure_attempts = ticket19.get("attempts", [])
    if not isinstance(pressure_attempts, list):
        return fail("ticket19 attempts must be a list")
    pressure_by_id = {str(attempt.get("problem_id")): attempt for attempt in pressure_attempts if isinstance(attempt, dict)}
    missing_pressure = EXPECTED_PROBLEMS - set(pressure_by_id)
    if missing_pressure:
        return fail("ticket19 attempts missing problems: " + ", ".join(sorted(missing_pressure)))
    ticket19_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-19-tail-uniformity-pressure.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-19-branch-graph-rank-search.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-19-local-obstruction-elimination.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-19-admissibility-vs-exact-gap.json"),
    }
    for problem_id, attempt in pressure_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket19 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket19 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket19 claim boundary is too weak")
        path = ticket19_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket19 per-problem artifact")

    ticket20_path = Path("data/open-problem/ticket20-valuation-prefix-lab.json")
    if not ticket20_path.exists():
        return fail("missing ticket20 valuation-prefix lab artifact")
    ticket20 = read_json(ticket20_path)
    if ticket20.get("schema") != TICKET20_SCHEMA:
        return fail("ticket20 valuation-prefix lab artifact has unexpected schema")
    if ticket20.get("status") != "proof_pressure_open_no_resolution":
        return fail("ticket20 valuation-prefix lab overstates resolution")
    ticket20_attempts = ticket20.get("attempts", [])
    if not isinstance(ticket20_attempts, list):
        return fail("ticket20 attempts must be a list")
    ticket20_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket20_attempts if isinstance(attempt, dict)}
    missing_ticket20 = EXPECTED_PROBLEMS - set(ticket20_by_id)
    if missing_ticket20:
        return fail("ticket20 attempts missing problems: " + ", ".join(sorted(missing_ticket20)))
    ticket20_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-20-uniform-tail-contract.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-20-valuation-prefix-rank-cegis.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-20-local-multiplicity-barrier.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-20-admissibility-constant-vs-deletion.json"),
    }
    for problem_id, attempt in ticket20_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket20 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket20 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket20 claim boundary is too weak")
        path = ticket20_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket20 per-problem artifact")

    ticket21_path = Path("data/open-problem/ticket21-two-adic-branch-lab.json")
    if not ticket21_path.exists():
        return fail("missing ticket21 two-adic branch lab artifact")
    ticket21 = read_json(ticket21_path)
    if ticket21.get("schema") != TICKET21_SCHEMA:
        return fail("ticket21 two-adic branch lab artifact has unexpected schema")
    if ticket21.get("status") != "proof_pressure_open_no_resolution":
        return fail("ticket21 two-adic branch lab overstates resolution")
    ticket21_attempts = ticket21.get("attempts", [])
    if not isinstance(ticket21_attempts, list):
        return fail("ticket21 attempts must be a list")
    ticket21_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket21_attempts if isinstance(attempt, dict)}
    missing_ticket21 = EXPECTED_PROBLEMS - set(ticket21_by_id)
    if missing_ticket21:
        return fail("ticket21 attempts missing problems: " + ", ".join(sorted(missing_ticket21)))
    ticket21_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-21-prefix-evasion-quantifier.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-21-two-adic-branch-exclusion.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-21-witness-spectrum.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-21-deletion-persistence-ladder.json"),
    }
    for problem_id, attempt in ticket21_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket21 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket21 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket21 claim boundary is too weak")
        path = ticket21_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket21 per-problem artifact")

    ticket22_path = Path("data/open-problem/ticket22-negation-pressure-lab.json")
    if not ticket22_path.exists():
        return fail("missing ticket22 negation pressure lab artifact")
    ticket22 = read_json(ticket22_path)
    if ticket22.get("schema") != TICKET22_SCHEMA:
        return fail("ticket22 negation pressure lab artifact has unexpected schema")
    if ticket22.get("status") != "negation_pressure_open_no_resolution":
        return fail("ticket22 negation pressure lab overstates resolution")
    ticket22_attempts = ticket22.get("attempts", [])
    if not isinstance(ticket22_attempts, list):
        return fail("ticket22 attempts must be a list")
    ticket22_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket22_attempts if isinstance(attempt, dict)}
    missing_ticket22 = EXPECTED_PROBLEMS - set(ticket22_by_id)
    if missing_ticket22:
        return fail("ticket22 attempts missing problems: " + ", ".join(sorted(missing_ticket22)))
    ticket22_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-22-li-detector-horizon.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-22-mixed-two-adic-cylinder-rank.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-22-residue-deletion-obstruction.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-22-exact-gap-projection.json"),
    }
    for problem_id, attempt in ticket22_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket22 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket22 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket22 claim boundary is too weak")
        path = ticket22_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket22 per-problem artifact")

    print("open problem structure verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
