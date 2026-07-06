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
TICKET23_SCHEMA = "primeproject.ticket23-cegis-rank-lab.v1"
TICKET24_SCHEMA = "primeproject.ticket24-bridge-weight-lab.v1"
TICKET25_SCHEMA = "primeproject.ticket25-formal-lemma-kernel.v1"
TICKET26_SCHEMA = "primeproject.ticket26-micro-lemma-closure.v1"
TICKET27_SCHEMA = "primeproject.ticket27-rank-frontier-lab.v1"
TICKET28_SCHEMA = "primeproject.ticket28-trichotomy-descent-lab.v1"
TICKET29_SCHEMA = "primeproject.ticket29-adaptive-frontier-lab.v1"
TICKET30_SCHEMA = "primeproject.ticket30-potential-synthesis-lab.v1"


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

    ticket23_path = Path("data/open-problem/ticket23-cegis-rank-lab.json")
    if not ticket23_path.exists():
        return fail("missing ticket23 CEGIS rank lab artifact")
    ticket23 = read_json(ticket23_path)
    if ticket23.get("schema") != TICKET23_SCHEMA:
        return fail("ticket23 CEGIS rank lab artifact has unexpected schema")
    if ticket23.get("status") != "cegis_rank_open_no_resolution":
        return fail("ticket23 CEGIS rank lab overstates resolution")
    ticket23_attempts = ticket23.get("attempts", [])
    if not isinstance(ticket23_attempts, list):
        return fail("ticket23 attempts must be a list")
    ticket23_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket23_attempts if isinstance(attempt, dict)}
    missing_ticket23 = EXPECTED_PROBLEMS - set(ticket23_by_id)
    if missing_ticket23:
        return fail("ticket23 attempts missing problems: " + ", ".join(sorted(missing_ticket23)))
    ticket23_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-23-detector-bound-cegis.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-23-cylinder-rank-cegis.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-23-exceptional-set-cegis.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-23-parity-projection-cegis.json"),
    }
    for problem_id, attempt in ticket23_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket23 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket23 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket23 claim boundary is too weak")
        path = ticket23_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket23 per-problem artifact")

    ticket24_path = Path("data/open-problem/ticket24-bridge-weight-lab.json")
    if not ticket24_path.exists():
        return fail("missing ticket24 bridge-weight lab artifact")
    ticket24 = read_json(ticket24_path)
    if ticket24.get("schema") != TICKET24_SCHEMA:
        return fail("ticket24 bridge-weight lab artifact has unexpected schema")
    if ticket24.get("status") != "bridge_weight_open_no_resolution":
        return fail("ticket24 bridge-weight lab overstates resolution")
    ticket24_attempts = ticket24.get("attempts", [])
    if not isinstance(ticket24_attempts, list):
        return fail("ticket24 attempts must be a list")
    ticket24_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket24_attempts if isinstance(attempt, dict)}
    missing_ticket24 = EXPECTED_PROBLEMS - set(ticket24_by_id)
    if missing_ticket24:
        return fail("ticket24 attempts missing problems: " + ", ".join(sorted(missing_ticket24)))
    ticket24_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-24-uniform-detector-budget.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-24-lift-aware-rank-probe.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-24-explicit-window-budget.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-24-exact-gap-weight-search.json"),
    }
    for problem_id, attempt in ticket24_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket24 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket24 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket24 claim boundary is too weak")
        path = ticket24_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket24 per-problem artifact")

    ticket25_path = Path("data/open-problem/ticket25-formal-lemma-kernel.json")
    if not ticket25_path.exists():
        return fail("missing ticket25 formal lemma kernel artifact")
    ticket25 = read_json(ticket25_path)
    if ticket25.get("schema") != TICKET25_SCHEMA:
        return fail("ticket25 formal lemma kernel artifact has unexpected schema")
    if ticket25.get("status") != "formal_kernel_open_no_resolution":
        return fail("ticket25 formal lemma kernel overstates resolution")
    ticket25_attempts = ticket25.get("attempts", [])
    if not isinstance(ticket25_attempts, list):
        return fail("ticket25 attempts must be a list")
    ticket25_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket25_attempts if isinstance(attempt, dict)}
    missing_ticket25 = EXPECTED_PROBLEMS - set(ticket25_by_id)
    if missing_ticket25:
        return fail("ticket25 attempts missing problems: " + ", ".join(sorted(missing_ticket25)))
    ticket25_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-25-finite-prefix-kernel.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-25-affine-lift-lemma.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-25-finite-exception-kernel.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-25-bounded-gap-counterkernel.json"),
    }
    for problem_id, attempt in ticket25_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket25 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket25 missing {field}")
        if not attempt.get("formal_kernel_statement"):
            return fail(f"{problem_id}: ticket25 missing formal kernel statement")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket25 claim boundary is too weak")
        path = ticket25_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket25 per-problem artifact")

    ticket26_path = Path("data/open-problem/ticket26-micro-lemma-closure.json")
    if not ticket26_path.exists():
        return fail("missing ticket26 micro-lemma closure artifact")
    ticket26 = read_json(ticket26_path)
    if ticket26.get("schema") != TICKET26_SCHEMA:
        return fail("ticket26 micro-lemma closure artifact has unexpected schema")
    if ticket26.get("status") != "micro_lemma_closed_full_conjectures_open":
        return fail("ticket26 micro-lemma closure overstates resolution")
    ticket26_attempts = ticket26.get("attempts", [])
    if not isinstance(ticket26_attempts, list):
        return fail("ticket26 attempts must be a list")
    ticket26_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket26_attempts if isinstance(attempt, dict)}
    missing_ticket26 = EXPECTED_PROBLEMS - set(ticket26_by_id)
    if missing_ticket26:
        return fail("ticket26 attempts missing problems: " + ", ".join(sorted(missing_ticket26)))
    ticket26_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-26-finite-universal-gap.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-26-affine-fixed-point-proof.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-26-finite-window-gap.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-26-bounded-gap-model-separation.json"),
    }
    for problem_id, attempt in ticket26_by_id.items():
        if attempt.get("status") != "micro_lemma_closed_target_open":
            return fail(f"{problem_id}: ticket26 attempt overstates proof status")
        if attempt.get("target_status") != "open_not_proven":
            return fail(f"{problem_id}: ticket26 target status must remain open")
        for field in (
            "route",
            "attempt",
            "formal_micro_lemma_statement",
            "micro_lemma_certificate",
            "closed_obligation",
            "remaining_obligation",
            "claim_boundary",
        ):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket26 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket26 claim boundary is too weak")
        path = ticket26_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket26 per-problem artifact")
    collatz_ticket26 = ticket26_by_id.get("collatz", {})
    collatz_certificate = collatz_ticket26.get("micro_lemma_certificate", {})
    if not isinstance(collatz_certificate, dict):
        return fail("collatz ticket26 certificate must be an object")
    if collatz_certificate.get("eliminated_false_cycle_count") != collatz_certificate.get("independent_recomputed_false_cycle_count"):
        return fail("collatz ticket26 did not eliminate every recomputed false cycle")
    if collatz_certificate.get("known_cycle_status") != "valid_positive_cycle":
        return fail("collatz ticket26 positive control did not validate the known cycle")

    ticket27_path = Path("data/open-problem/ticket27-rank-frontier-lab.json")
    if not ticket27_path.exists():
        return fail("missing ticket27 rank frontier artifact")
    ticket27 = read_json(ticket27_path)
    if ticket27.get("schema") != TICKET27_SCHEMA:
        return fail("ticket27 rank frontier artifact has unexpected schema")
    if ticket27.get("status") != "rank_frontier_open_no_resolution":
        return fail("ticket27 rank frontier overstates resolution")
    ticket27_attempts = ticket27.get("attempts", [])
    if not isinstance(ticket27_attempts, list):
        return fail("ticket27 attempts must be a list")
    ticket27_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket27_attempts if isinstance(attempt, dict)}
    missing_ticket27 = EXPECTED_PROBLEMS - set(ticket27_by_id)
    if missing_ticket27:
        return fail("ticket27 attempts missing problems: " + ", ".join(sorted(missing_ticket27)))
    ticket27_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-27-tail-uniformity-frontier.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-27-lift-aware-noncyclic-rank.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-27-tail-cutoff-frontier.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-27-exact-gap-rank-frontier.json"),
    }
    for problem_id, attempt in ticket27_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket27 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket27 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket27 claim boundary is too weak")
        path = ticket27_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket27 per-problem artifact")
    collatz_ticket27 = ticket27_by_id.get("collatz", {})
    collatz27_bounded = collatz_ticket27.get("bounded_result", {})
    if not isinstance(collatz27_bounded, dict):
        return fail("collatz ticket27 bounded result must be an object")
    if not collatz27_bounded.get("all_clean_rows_refute_quotient_rank_lift"):
        return fail("collatz ticket27 must refute quotient rank lift on clean rows")
    rows27 = collatz27_bounded.get("rank_frontier_rows", [])
    if not isinstance(rows27, list) or not rows27:
        return fail("collatz ticket27 rank frontier rows missing")
    if not any(row.get("sampled_lift_rank_violations_excluding_residue_one", 0) > 0 for row in rows27):
        return fail("collatz ticket27 lacks non-1 lift rank counterexamples")

    ticket28_path = Path("data/open-problem/ticket28-trichotomy-descent-lab.json")
    if not ticket28_path.exists():
        return fail("missing ticket28 trichotomy descent artifact")
    ticket28 = read_json(ticket28_path)
    if ticket28.get("schema") != TICKET28_SCHEMA:
        return fail("ticket28 trichotomy descent artifact has unexpected schema")
    if ticket28.get("status") != "trichotomy_descent_open_no_resolution":
        return fail("ticket28 trichotomy descent overstates resolution")
    ticket28_attempts = ticket28.get("attempts", [])
    if not isinstance(ticket28_attempts, list):
        return fail("ticket28 attempts must be a list")
    ticket28_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket28_attempts if isinstance(attempt, dict)}
    missing_ticket28 = EXPECTED_PROBLEMS - set(ticket28_by_id)
    if missing_ticket28:
        return fail("ticket28 attempts missing problems: " + ", ".join(sorted(missing_ticket28)))
    ticket28_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-28-mertens-tail-trichotomy.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-28-lift-coordinate-debt-rank-cegis.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-28-witness-cutoff-trichotomy.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-28-exact-gap-tail-trichotomy.json"),
    }
    for problem_id, attempt in ticket28_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket28 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket28 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket28 claim boundary is too weak")
        path = ticket28_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket28 per-problem artifact")
        bounded28 = attempt.get("bounded_result", {})
        routes28 = bounded28.get("trichotomy_routes", []) if isinstance(bounded28, dict) else []
        if not isinstance(routes28, list) or len(routes28) != 3:
            return fail(f"{problem_id}: ticket28 must expose exactly three proof routes")

    collatz_ticket28 = ticket28_by_id.get("collatz", {})
    collatz28_bounded = collatz_ticket28.get("bounded_result", {})
    if not isinstance(collatz28_bounded, dict):
        return fail("collatz ticket28 bounded result must be an object")
    stopping28 = collatz28_bounded.get("stopping_scan", {})
    if not isinstance(stopping28, dict) or not stopping28.get("no_stopping_counterexample_leq_limit"):
        return fail("collatz ticket28 must record no finite stopping counterexample in its scan")
    cylinder28 = collatz28_bounded.get("cylinder_descent", {})
    if not isinstance(cylinder28, dict):
        return fail("collatz ticket28 cylinder descent result missing")
    max_row28 = cylinder28.get("max_bits_row", {})
    if not isinstance(max_row28, dict) or max_row28.get("needs_split_count", 0) <= 0:
        return fail("collatz ticket28 must keep the global proof blocked by needs_split cylinders")
    if cylinder28.get("all_nontrivial_cylinders_closed_at_max_bits"):
        return fail("collatz ticket28 overstates cylinder closure")

    goldbach_ticket28 = ticket28_by_id.get("goldbach", {})
    goldbach28_scan = goldbach_ticket28.get("bounded_result", {}).get("finite_witness_scan", {})
    if not isinstance(goldbach28_scan, dict) or not goldbach28_scan.get("no_counterexample_leq_limit"):
        return fail("goldbach ticket28 finite witness scan must find no bounded counterexample")

    twin_ticket28 = ticket28_by_id.get("twin-prime", {})
    twin28_scan = twin_ticket28.get("bounded_result", {}).get("finite_exact_gap_scan", {})
    if not isinstance(twin28_scan, dict) or int(twin28_scan.get("twin_pair_count", 0)) <= 0:
        return fail("twin-prime ticket28 must record finite exact-gap pairs")

    ticket29_path = Path("data/open-problem/ticket29-adaptive-frontier-lab.json")
    if not ticket29_path.exists():
        return fail("missing ticket29 adaptive frontier artifact")
    ticket29 = read_json(ticket29_path)
    if ticket29.get("schema") != TICKET29_SCHEMA:
        return fail("ticket29 adaptive frontier artifact has unexpected schema")
    if ticket29.get("status") != "adaptive_frontier_open_no_resolution":
        return fail("ticket29 adaptive frontier overstates resolution")
    ticket29_attempts = ticket29.get("attempts", [])
    if not isinstance(ticket29_attempts, list):
        return fail("ticket29 attempts must be a list")
    ticket29_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket29_attempts if isinstance(attempt, dict)}
    missing_ticket29 = EXPECTED_PROBLEMS - set(ticket29_by_id)
    if missing_ticket29:
        return fail("ticket29 attempts missing problems: " + ", ".join(sorted(missing_ticket29)))
    ticket29_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-29-tail-bridge-frontier.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-29-adaptive-cylinder-split.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-29-least-counterexample-cutoff.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-29-exact-gap-tail-pressure.json"),
    }
    for problem_id, attempt in ticket29_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket29 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket29 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket29 claim boundary is too weak")
        path = ticket29_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket29 per-problem artifact")

    collatz_ticket29 = ticket29_by_id.get("collatz", {})
    collatz29_bounded = collatz_ticket29.get("bounded_result", {})
    if not isinstance(collatz29_bounded, dict):
        return fail("collatz ticket29 bounded result must be an object")
    adaptive29 = collatz29_bounded.get("adaptive_cylinder_split", {})
    if not isinstance(adaptive29, dict):
        return fail("collatz ticket29 adaptive split result missing")
    if int(adaptive29.get("processed_state_count", 0)) <= 0:
        return fail("collatz ticket29 processed no adaptive states")
    if int(adaptive29.get("open_frontier_count_at_max_bits", 0)) <= 0:
        return fail("collatz ticket29 must keep the proof blocked by an open frontier")
    if adaptive29.get("naive_termination_verdict") != "not_supported_by_ticket29":
        return fail("collatz ticket29 must reject naive adaptive termination")

    riemann_ticket29 = ticket29_by_id.get("riemann", {})
    riemann29_stress = riemann_ticket29.get("bounded_result", {}).get("mertens_stress", {})
    if not isinstance(riemann29_stress, dict) or int(riemann29_stress.get("limit", 0)) < 10_000_000:
        return fail("riemann ticket29 must include the expanded Mertens stress limit")

    goldbach_ticket29 = ticket29_by_id.get("goldbach", {})
    goldbach29_scan = goldbach_ticket29.get("bounded_result", {}).get("finite_witness_scan", {})
    if not isinstance(goldbach29_scan, dict) or not goldbach29_scan.get("no_counterexample_leq_limit"):
        return fail("goldbach ticket29 finite witness scan must find no bounded counterexample")
    if int(goldbach29_scan.get("even_limit", 0)) < 5_000_000:
        return fail("goldbach ticket29 must extend the finite witness scan")

    twin_ticket29 = ticket29_by_id.get("twin-prime", {})
    twin29_scan = twin_ticket29.get("bounded_result", {}).get("finite_exact_gap_scan", {})
    if not isinstance(twin29_scan, dict) or int(twin29_scan.get("twin_pair_count", 0)) <= 0:
        return fail("twin-prime ticket29 must record finite exact-gap pairs")
    if int(twin29_scan.get("prime_limit", 0)) < 20_000_000:
        return fail("twin-prime ticket29 must extend the exact-gap scan")

    ticket30_path = Path("data/open-problem/ticket30-potential-synthesis-lab.json")
    if not ticket30_path.exists():
        return fail("missing ticket30 potential synthesis artifact")
    ticket30 = read_json(ticket30_path)
    if ticket30.get("schema") != TICKET30_SCHEMA:
        return fail("ticket30 potential synthesis artifact has unexpected schema")
    if ticket30.get("status") != "potential_synthesis_open_no_resolution":
        return fail("ticket30 potential synthesis overstates resolution")
    ticket30_attempts = ticket30.get("attempts", [])
    if not isinstance(ticket30_attempts, list):
        return fail("ticket30 attempts must be a list")
    ticket30_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket30_attempts if isinstance(attempt, dict)}
    missing_ticket30 = EXPECTED_PROBLEMS - set(ticket30_by_id)
    if missing_ticket30:
        return fail("ticket30 attempts missing problems: " + ", ".join(sorted(missing_ticket30)))
    ticket30_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-30-tail-majorant-synthesis.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-30-valuation-debt-potential.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-30-explicit-constant-ledger.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-30-exact-gap-functional.json"),
    }
    for problem_id, attempt in ticket30_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket30 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket30 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket30 claim boundary is too weak")
        path = ticket30_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket30 per-problem artifact")

    collatz_ticket30 = ticket30_by_id.get("collatz", {})
    collatz30_bounded = collatz_ticket30.get("bounded_result", {})
    if not isinstance(collatz30_bounded, dict):
        return fail("collatz ticket30 bounded result must be an object")
    potential30 = collatz30_bounded.get("potential_cegis", {})
    if not isinstance(potential30, dict):
        return fail("collatz ticket30 potential CEGIS result missing")
    if potential30.get("linear_potential_status") != "no_tested_linear_potential_survives":
        return fail("collatz ticket30 must reject the tested linear potential family")
    if int(potential30.get("valid_grid_weight_count", -1)) != 0:
        return fail("collatz ticket30 grid search must have zero surviving weights")
    best30 = potential30.get("best_grid_results", [])
    if not isinstance(best30, list) or not best30 or int(best30[0].get("violation_count", 0)) <= 0:
        return fail("collatz ticket30 must keep potential synthesis blocked by violations")

    print("open problem structure verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
