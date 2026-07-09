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
TICKET31_SCHEMA = "primeproject.ticket31-feature-stutter-lab.v1"
TICKET32_SCHEMA = "primeproject.ticket32-stateful-measure-lab.v1"
TICKET33_SCHEMA = "primeproject.ticket33-global-measure-lab.v1"
TICKET34_SCHEMA = "primeproject.ticket34-high-branch-automaton-lab.v1"
TICKET35_SCHEMA = "primeproject.ticket35-limsup-mass-refinement-lab.v1"
TICKET36_SCHEMA = "primeproject.ticket36-null-frontier-arithmetic-lab.v1"
TICKET37_SCHEMA = "primeproject.ticket37-pointwise-rank-synthesis-lab.v1"
TICKET38_SCHEMA = "primeproject.ticket38-symbolic-frontier-extension-lab.v1"
TICKET39_SCHEMA = "primeproject.ticket39-phase-state-potential-lab.v1"
TICKET40_SCHEMA = "primeproject.ticket40-transition-closure-lab.v1"
TICKET41_SCHEMA = "primeproject.ticket41-rank-escape-normalization-lab.v1"
TICKET42_SCHEMA = "primeproject.ticket42-parametric-transition-template-lab.v1"
TICKET43_SCHEMA = "primeproject.ticket43-lift-constraint-measure-lab.v1"
TICKET44_SCHEMA = "primeproject.ticket44-feature-measure-counteredge-lab.v1"
TICKET45_SCHEMA = "primeproject.ticket45-symbolic-rank-clause-lab.v1"
TICKET46_SCHEMA = "primeproject.ticket46-stable-clause-grammar-lab.v1"
TICKET47_SCHEMA = "primeproject.ticket47-periodic-state-lasso-lab.v1"
TICKET48_SCHEMA = "primeproject.ticket48-automaton-reachability-lab.v1"
TICKET49_SCHEMA = "primeproject.ticket49-symbolic-preimage-obstruction-lab.v1"
TICKET50_SCHEMA = "primeproject.ticket50-phase-lift-exception-lab.v1"
TICKET51_SCHEMA = "primeproject.ticket51-phase15-terminal-lift-lab.v1"
TICKET52_SCHEMA = "primeproject.ticket52-frontier-budget-lab.v1"
TICKET53_SCHEMA = "primeproject.ticket53-symbolic-terminal-theorem-lab.v1"
TICKET54_SCHEMA = "primeproject.ticket54-new-template-family-lab.v1"
TICKET55_SCHEMA = "primeproject.ticket55-phase5-valuation-gate-lab.v1"
TICKET56_SCHEMA = "primeproject.ticket56-pre-gate-projection-escape-lab.v1"
TICKET57_SCHEMA = "primeproject.ticket57-parametric-template-automaton-lab.v1"
TICKET58_SCHEMA = "primeproject.ticket58-affine-boundary-lift-lab.v1"
TICKET59_SCHEMA = "primeproject.ticket59-symbolic-lift-mismatch-lab.v1"
TICKET60_SCHEMA = "primeproject.ticket60-mixed-cylinder-separator-lab.v1"
TICKET61_SCHEMA = "primeproject.ticket61-symbolic-failure-offset-lab.v1"
TICKET62_SCHEMA = "primeproject.ticket62-mod16-transition-cover-lab.v1"
TICKET63_SCHEMA = "primeproject.ticket63-mod16-automaton-cover-lab.v1"
TICKET64_SCHEMA = "primeproject.ticket64-symbolic-mod16-transition-lab.v1"
TICKET65_SCHEMA = "primeproject.ticket65-start-template-chain-extinction-lab.v1"
TICKET66_SCHEMA = "primeproject.ticket66-complement-cover-lab.v1"
TICKET67_SCHEMA = "primeproject.ticket67-open-template-rank-lab.v1"
TICKET68_SCHEMA = "primeproject.ticket68-cycle-scc-refinement-lab.v1"
TICKET69_SCHEMA = "primeproject.ticket69-prefix-consumed-rank-lab.v1"


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

    ticket31_path = Path("data/open-problem/ticket31-feature-stutter-lab.json")
    if not ticket31_path.exists():
        return fail("missing ticket31 feature stutter artifact")
    ticket31 = read_json(ticket31_path)
    if ticket31.get("schema") != TICKET31_SCHEMA:
        return fail("ticket31 feature stutter artifact has unexpected schema")
    if ticket31.get("status") != "feature_stutter_open_no_resolution":
        return fail("ticket31 feature stutter overstates resolution")
    ticket31_attempts = ticket31.get("attempts", [])
    if not isinstance(ticket31_attempts, list):
        return fail("ticket31 attempts must be a list")
    ticket31_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket31_attempts if isinstance(attempt, dict)}
    missing_ticket31 = EXPECTED_PROBLEMS - set(ticket31_by_id)
    if missing_ticket31:
        return fail("ticket31 attempts missing problems: " + ", ".join(sorted(missing_ticket31)))
    ticket31_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-31-finite-stress-stutter.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-31-feature-stutter-obstruction.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-31-cutoff-ledger-stutter.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-31-parity-selector-stutter.json"),
    }
    for problem_id, attempt in ticket31_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket31 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket31 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket31 claim boundary is too weak")
        path = ticket31_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket31 per-problem artifact")

    collatz_ticket31 = ticket31_by_id.get("collatz", {})
    collatz31_bounded = collatz_ticket31.get("bounded_result", {})
    if not isinstance(collatz31_bounded, dict):
        return fail("collatz ticket31 bounded result must be an object")
    stutter31 = collatz31_bounded.get("feature_stutter_cegis", {})
    if not isinstance(stutter31, dict):
        return fail("collatz ticket31 feature stutter result missing")
    if stutter31.get("feature_only_obstruction_status") != "feature_stutter_blocks_all_strict_local_potentials":
        return fail("collatz ticket31 must record the feature-only obstruction")
    if int(stutter31.get("parent_edge_count", 0)) <= 0:
        return fail("collatz ticket31 must process adaptive parent edges")
    impossible31 = stutter31.get("strict_descent_impossibility", {})
    if not isinstance(impossible31, dict):
        return fail("collatz ticket31 strict descent impossibility missing")
    if int(impossible31.get("base_four_indistinguishable_edges", 0)) <= 0:
        return fail("collatz ticket31 must find base feature stutter edges")
    if int(impossible31.get("prefix_and_low_residue_indistinguishable_edges", 0)) <= 0:
        return fail("collatz ticket31 must find prefix-and-residue stutter edges")
    families31 = stutter31.get("feature_families", [])
    if not isinstance(families31, list) or len(families31) < 6:
        return fail("collatz ticket31 must compare multiple feature families")
    family_by_name31 = {str(row.get("family")): row for row in families31 if isinstance(row, dict)}
    for family_name in ("base_plus_modulus_bits", "base_plus_cylinder_mass"):
        row = family_by_name31.get(family_name)
        if row is None or int(row.get("indistinguishable_open_edges", -1)) != 0:
            return fail(f"collatz ticket31 scale family {family_name} must separate tested stutters")

    ticket32_path = Path("data/open-problem/ticket32-stateful-measure-lab.json")
    if not ticket32_path.exists():
        return fail("missing ticket32 stateful measure artifact")
    ticket32 = read_json(ticket32_path)
    if ticket32.get("schema") != TICKET32_SCHEMA:
        return fail("ticket32 stateful measure artifact has unexpected schema")
    if ticket32.get("status") != "stateful_measure_open_no_resolution":
        return fail("ticket32 stateful measure overstates resolution")
    ticket32_attempts = ticket32.get("attempts", [])
    if not isinstance(ticket32_attempts, list):
        return fail("ticket32 attempts must be a list")
    ticket32_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket32_attempts if isinstance(attempt, dict)}
    missing_ticket32 = EXPECTED_PROBLEMS - set(ticket32_by_id)
    if missing_ticket32:
        return fail("ticket32 attempts missing problems: " + ", ".join(sorted(missing_ticket32)))
    ticket32_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-32-stateful-tail-certificate.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-32-stateful-measure-descent.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-32-stateful-cutoff-ledger.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-32-stateful-parity-selector.json"),
    }
    for problem_id, attempt in ticket32_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket32 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket32 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket32 claim boundary is too weak")
        path = ticket32_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket32 per-problem artifact")

    collatz_ticket32 = ticket32_by_id.get("collatz", {})
    collatz32_bounded = collatz_ticket32.get("bounded_result", {})
    if not isinstance(collatz32_bounded, dict):
        return fail("collatz ticket32 bounded result must be an object")
    audit32 = collatz32_bounded.get("stateful_measure_audit", {})
    if not isinstance(audit32, dict):
        return fail("collatz ticket32 stateful measure audit missing")
    if int(audit32.get("stutter_edge_count", 0)) <= 0:
        return fail("collatz ticket32 must audit stutter edges")
    if int(audit32.get("max_same_signature_steps", 0)) <= 0:
        return fail("collatz ticket32 must record nonzero stutter budget")
    budget32 = audit32.get("stateful_budget_certificate", {})
    if not isinstance(budget32, dict):
        return fail("collatz ticket32 stateful budget certificate missing")
    if budget32.get("status") != "bounded_certificate_found":
        return fail("collatz ticket32 must find a bounded stutter budget certificate")
    if int(budget32.get("unresolved_stutter_edges", -1)) != 0:
        return fail("collatz ticket32 must have zero unresolved stutter edges")
    outcomes32 = audit32.get("chain_outcome_counts", {})
    if not isinstance(outcomes32, dict) or int(outcomes32.get("terminal", 0)) <= 0:
        return fail("collatz ticket32 must include terminal stutter chains")
    if int(outcomes32.get("signature_changed", 0)) <= 0:
        return fail("collatz ticket32 must include signature-changing stutter chains")

    ticket33_path = Path("data/open-problem/ticket33-global-measure-lab.json")
    if not ticket33_path.exists():
        return fail("missing ticket33 global measure artifact")
    ticket33 = read_json(ticket33_path)
    if ticket33.get("schema") != TICKET33_SCHEMA:
        return fail("ticket33 global measure artifact has unexpected schema")
    if ticket33.get("status") != "global_measure_open_no_resolution":
        return fail("ticket33 global measure overstates resolution")
    ticket33_attempts = ticket33.get("attempts", [])
    if not isinstance(ticket33_attempts, list):
        return fail("ticket33 attempts must be a list")
    ticket33_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket33_attempts if isinstance(attempt, dict)}
    missing_ticket33 = EXPECTED_PROBLEMS - set(ticket33_by_id)
    if missing_ticket33:
        return fail("ticket33 attempts missing problems: " + ", ".join(sorted(missing_ticket33)))
    ticket33_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-33-global-tail-compactness.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-33-global-measure-compactness.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-33-global-cutoff-compactness.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-33-global-parity-compactness.json"),
    }
    for problem_id, attempt in ticket33_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket33 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket33 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket33 claim boundary is too weak")
        path = ticket33_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket33 per-problem artifact")

    collatz_ticket33 = ticket33_by_id.get("collatz", {})
    collatz33_bounded = collatz_ticket33.get("bounded_result", {})
    if not isinstance(collatz33_bounded, dict):
        return fail("collatz ticket33 bounded result must be an object")
    audit33 = collatz33_bounded.get("global_measure_audit", {})
    if not isinstance(audit33, dict):
        return fail("collatz ticket33 global measure audit missing")
    if not audit33.get("monotone_open_mass_decrease"):
        return fail("collatz ticket33 must observe monotone open mass decrease")
    if float(audit33.get("final_open_frontier_mass", 0.0)) <= 0:
        return fail("collatz ticket33 must keep a positive final open frontier mass")
    measure33 = audit33.get("measure_certificate", {})
    if not isinstance(measure33, dict):
        return fail("collatz ticket33 measure certificate missing")
    if measure33.get("status") != "bounded_measure_decay_observed":
        return fail("collatz ticket33 must record bounded measure decay")
    if measure33.get("compactness_status") != "open_no_global_compactness_theorem":
        return fail("collatz ticket33 must keep compactness theorem open")
    high33 = audit33.get("high_branch_obstruction", {})
    if not isinstance(high33, dict):
        return fail("collatz ticket33 high branch obstruction missing")
    if int(high33.get("high_open_child_edges", 0)) <= 0:
        return fail("collatz ticket33 must find open high-child edges")
    if int(high33.get("high_only_open_child_edges", 0)) <= 0:
        return fail("collatz ticket33 must find high-only open child edges")

    ticket34_path = Path("data/open-problem/ticket34-high-branch-automaton-lab.json")
    if not ticket34_path.exists():
        return fail("missing ticket34 high-branch automaton artifact")
    ticket34 = read_json(ticket34_path)
    if ticket34.get("schema") != TICKET34_SCHEMA:
        return fail("ticket34 high-branch automaton artifact has unexpected schema")
    if ticket34.get("status") != "high_branch_automaton_open_no_resolution":
        return fail("ticket34 high-branch automaton overstates resolution")
    ticket34_attempts = ticket34.get("attempts", [])
    if not isinstance(ticket34_attempts, list):
        return fail("ticket34 attempts must be a list")
    ticket34_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket34_attempts if isinstance(attempt, dict)}
    missing_ticket34 = EXPECTED_PROBLEMS - set(ticket34_by_id)
    if missing_ticket34:
        return fail("ticket34 attempts missing problems: " + ", ".join(sorted(missing_ticket34)))
    ticket34_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-34-tail-automaton-limit.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-34-high-branch-automaton.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-34-cutoff-automaton-limit.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-34-parity-automaton-limit.json"),
    }
    for problem_id, attempt in ticket34_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket34 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket34 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket34 claim boundary is too weak")
        path = ticket34_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket34 per-problem artifact")

    collatz_ticket34 = ticket34_by_id.get("collatz", {})
    collatz34_bounded = collatz_ticket34.get("bounded_result", {})
    if not isinstance(collatz34_bounded, dict):
        return fail("collatz ticket34 bounded result must be an object")
    audit34 = collatz34_bounded.get("high_branch_automaton_audit", {})
    if not isinstance(audit34, dict):
        return fail("collatz ticket34 high-branch automaton audit missing")
    if int(audit34.get("transition_parent_count", 0)) <= 0:
        return fail("collatz ticket34 must audit transition parents")
    if int(audit34.get("high_open_child_parent_count", 0)) <= 0:
        return fail("collatz ticket34 must retain high-open obstruction")
    if int(audit34.get("high_only_parent_count", 0)) <= 0:
        return fail("collatz ticket34 must retain high-only obstruction")
    if not audit34.get("pointwise_contraction_blocked"):
        return fail("collatz ticket34 must block pointwise contraction shortcut")
    max_ratio34 = audit34.get("max_mass_ratio_to_next")
    if max_ratio34 is None or float(max_ratio34) >= 1.0:
        return fail("collatz ticket34 must record bounded aggregate mass pressure below one")
    certificate34 = audit34.get("automaton_certificate", {})
    if not isinstance(certificate34, dict):
        return fail("collatz ticket34 automaton certificate missing")
    if certificate34.get("status") != "no_finite_automaton_closure_found":
        return fail("collatz ticket34 must not claim finite automaton closure")
    if certificate34.get("mass_limit_status") != "finite_aggregate_pressure_only":
        return fail("collatz ticket34 must keep mass-limit theorem open")
    families34 = audit34.get("automaton_families", [])
    if not isinstance(families34, list) or len(families34) < 5:
        return fail("collatz ticket34 must compare multiple automaton families")
    if not any(int(row.get("ambiguous_state_count", 0)) > 0 for row in families34 if isinstance(row, dict)):
        return fail("collatz ticket34 must expose automaton state collisions")
    if not any(
        isinstance(row, dict)
        and isinstance(row.get("aggregate_spectral_pressure"), dict)
        and float(row["aggregate_spectral_pressure"].get("estimated_radius", 1.0)) < 1.0
        for row in families34
    ):
        return fail("collatz ticket34 must record finite aggregate spectral pressure")

    ticket35_path = Path("data/open-problem/ticket35-limsup-mass-refinement-lab.json")
    if not ticket35_path.exists():
        return fail("missing ticket35 limsup mass refinement artifact")
    ticket35 = read_json(ticket35_path)
    if ticket35.get("schema") != TICKET35_SCHEMA:
        return fail("ticket35 limsup mass refinement artifact has unexpected schema")
    if ticket35.get("status") != "limsup_mass_refinement_open_no_resolution":
        return fail("ticket35 limsup mass refinement overstates resolution")
    ticket35_attempts = ticket35.get("attempts", [])
    if not isinstance(ticket35_attempts, list):
        return fail("ticket35 attempts must be a list")
    ticket35_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket35_attempts if isinstance(attempt, dict)}
    missing_ticket35 = EXPECTED_PROBLEMS - set(ticket35_by_id)
    if missing_ticket35:
        return fail("ticket35 attempts missing problems: " + ", ".join(sorted(missing_ticket35)))
    ticket35_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-35-tail-nullset-exclusion.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-35-limsup-mass-refinement.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-35-exceptional-set-elimination.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-35-exact-gap-nullset.json"),
    }
    for problem_id, attempt in ticket35_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket35 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket35 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket35 claim boundary is too weak")
        path = ticket35_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket35 per-problem artifact")

    collatz_ticket35 = ticket35_by_id.get("collatz", {})
    collatz35_bounded = collatz_ticket35.get("bounded_result", {})
    if not isinstance(collatz35_bounded, dict):
        return fail("collatz ticket35 bounded result must be an object")
    audit35 = collatz35_bounded.get("limsup_mass_refinement_audit", {})
    if not isinstance(audit35, dict):
        return fail("collatz ticket35 limsup mass refinement audit missing")
    mass35 = audit35.get("mass_envelope_audit", {})
    if not isinstance(mass35, dict):
        return fail("collatz ticket35 mass envelope missing")
    if float(mass35.get("max_mass_ratio_to_next", 1.0)) >= 1.0:
        return fail("collatz ticket35 must keep finite mass ratios below one")
    if float(mass35.get("final_open_mass", 0.0)) <= 0.0:
        return fail("collatz ticket35 must keep positive finite final open mass")
    if not mass35.get("tail_window_candidate_epsilon"):
        return fail("collatz ticket35 must record finite tail epsilon")
    null35 = audit35.get("null_set_gap", {})
    if not isinstance(null35, dict):
        return fail("collatz ticket35 null-set gap missing")
    if null35.get("status") != "mass_zero_not_pointwise_proof":
        return fail("collatz ticket35 must not treat mass-zero as pointwise proof")
    route35 = audit35.get("route_decision", {})
    if not isinstance(route35, dict):
        return fail("collatz ticket35 route decision missing")
    discard35 = " ".join(str(item) for item in route35.get("discard", []))
    if "mass-only" not in discard35 or "finite-feature" not in discard35:
        return fail("collatz ticket35 must discard weak mass-only and finite-feature routes")
    refinement35 = audit35.get("state_refinement_audit", {})
    if not isinstance(refinement35, dict):
        return fail("collatz ticket35 state refinement audit missing")
    if refinement35.get("refinement_status") != "bounded_refinements_still_blocked_identity_state_not_uniform":
        return fail("collatz ticket35 must keep refinement route open")
    rows35 = refinement35.get("refinement_rows", [])
    if not isinstance(rows35, list) or len(rows35) < 4:
        return fail("collatz ticket35 must compare multiple state refinements")
    identity_rows35 = [row for row in rows35 if isinstance(row, dict) and row.get("family") == "exact_residue_and_bits"]
    if not identity_rows35 or identity_rows35[0].get("finite_uniform_candidate") is not False:
        return fail("collatz ticket35 must reject exact identity state as finite uniform proof")
    if not any(isinstance(row, dict) and int(row.get("pointwise_noncontracting_state_count", 0)) > 0 for row in rows35):
        return fail("collatz ticket35 must retain pointwise noncontraction obstruction")

    ticket36_path = Path("data/open-problem/ticket36-null-frontier-arithmetic-lab.json")
    if not ticket36_path.exists():
        return fail("missing ticket36 null-frontier arithmetic artifact")
    ticket36 = read_json(ticket36_path)
    if ticket36.get("schema") != TICKET36_SCHEMA:
        return fail("ticket36 null-frontier arithmetic artifact has unexpected schema")
    if ticket36.get("status") != "null_frontier_arithmetic_open_no_resolution":
        return fail("ticket36 null-frontier arithmetic overstates resolution")
    ticket36_attempts = ticket36.get("attempts", [])
    if not isinstance(ticket36_attempts, list):
        return fail("ticket36 attempts must be a list")
    ticket36_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket36_attempts if isinstance(attempt, dict)}
    missing_ticket36 = EXPECTED_PROBLEMS - set(ticket36_by_id)
    if missing_ticket36:
        return fail("ticket36 attempts missing problems: " + ", ".join(sorted(missing_ticket36)))
    ticket36_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-36-offcritical-null-exclusion.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-36-natural-null-frontier.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-36-sparse-exception-exclusion.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-36-sparse-gap-exclusion.json"),
    }
    for problem_id, attempt in ticket36_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket36 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket36 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket36 claim boundary is too weak")
        path = ticket36_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket36 per-problem artifact")

    collatz_ticket36 = ticket36_by_id.get("collatz", {})
    collatz36_bounded = collatz_ticket36.get("bounded_result", {})
    if not isinstance(collatz36_bounded, dict):
        return fail("collatz ticket36 bounded result must be an object")
    audit36 = collatz36_bounded.get("natural_null_frontier_audit", {})
    if not isinstance(audit36, dict):
        return fail("collatz ticket36 natural null-frontier audit missing")
    if int(audit36.get("tested_odd_integer_count", 0)) < 50_000:
        return fail("collatz ticket36 must test the intended natural integer sample")
    if int(audit36.get("shallow_unresolved_count", 0)) <= 0:
        return fail("collatz ticket36 must expose shallow natural frontier survivors")
    if int(audit36.get("deep_unresolved_count", 1)) != 0:
        return fail("collatz ticket36 bounded deep probe must resolve tested natural survivors")
    if int(audit36.get("max_exit_bits", 0)) < 100:
        return fail("collatz ticket36 must retain long natural exit-depth obstruction")
    if int(audit36.get("max_exit_slack_over_bit_length", 0)) < 100:
        return fail("collatz ticket36 must reject shallow bit-length slack proofs")
    slack_tests36 = audit36.get("candidate_bit_length_slack_tests", [])
    if not isinstance(slack_tests36, list) or not any(
        isinstance(row, dict) and "112" in str(row.get("candidate_bound")) and int(row.get("violations", 0)) > 0
        for row in slack_tests36
    ):
        return fail("collatz ticket36 must record violations of large constant slack bounds")
    route36 = collatz36_bounded.get("route_decision", {})
    if not isinstance(route36, dict):
        return fail("collatz ticket36 route decision missing")
    discard36 = " ".join(str(item) for item in route36.get("discard", []))
    retain36 = " ".join(str(item) for item in route36.get("retain", []))
    if "measure-zero" not in discard36 or "stopping-time proxy" not in discard36:
        return fail("collatz ticket36 must discard non-pointwise and circular routes")
    if "well-founded rank" not in retain36:
        return fail("collatz ticket36 must retain the uniform rank route")

    ticket37_path = Path("data/open-problem/ticket37-pointwise-rank-synthesis-lab.json")
    if not ticket37_path.exists():
        return fail("missing ticket37 pointwise rank synthesis artifact")
    ticket37 = read_json(ticket37_path)
    if ticket37.get("schema") != TICKET37_SCHEMA:
        return fail("ticket37 pointwise rank synthesis artifact has unexpected schema")
    if ticket37.get("status") != "pointwise_rank_synthesis_open_no_resolution":
        return fail("ticket37 pointwise rank synthesis overstates resolution")
    ticket37_attempts = ticket37.get("attempts", [])
    if not isinstance(ticket37_attempts, list):
        return fail("ticket37 attempts must be a list")
    ticket37_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket37_attempts if isinstance(attempt, dict)}
    missing_ticket37 = EXPECTED_PROBLEMS - set(ticket37_by_id)
    if missing_ticket37:
        return fail("ticket37 attempts missing problems: " + ", ".join(sorted(missing_ticket37)))
    ticket37_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-37-pointwise-zero-rank.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-37-pointwise-rank-synthesis.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-37-pointwise-cutoff-rank.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-37-exact-gap-rank.json"),
    }
    for problem_id, attempt in ticket37_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket37 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket37 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket37 claim boundary is too weak")
        path = ticket37_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket37 per-problem artifact")

    collatz_ticket37 = ticket37_by_id.get("collatz", {})
    collatz37_bounded = collatz_ticket37.get("bounded_result", {})
    if not isinstance(collatz37_bounded, dict):
        return fail("collatz ticket37 bounded result must be an object")
    probe37 = collatz37_bounded.get("pointwise_rank_probe", {})
    if not isinstance(probe37, dict):
        return fail("collatz ticket37 pointwise rank probe missing")
    if int(probe37.get("tested_odd_integer_count", 0)) < 2_500_000:
        return fail("collatz ticket37 must test the extended rank sample")
    if int(probe37.get("unresolved_count", 1)) != 0:
        return fail("collatz ticket37 bounded probe must resolve tested natural integers")
    if int(probe37.get("max_exit_bits", 0)) < 200:
        return fail("collatz ticket37 must retain deep exit examples")
    if float(probe37.get("max_exit_ratio_to_bit_length", 0.0)) < 10.0:
        return fail("collatz ticket37 must retain high exit-ratio stress cases")
    rank_tests37 = probe37.get("linear_rank_tests", [])
    if not isinstance(rank_tests37, list) or len(rank_tests37) < 5:
        return fail("collatz ticket37 must compare multiple linear rank candidates")
    rank_by_bound37 = {str(row.get("candidate_bound")): row for row in rank_tests37 if isinstance(row, dict)}
    for alpha in (8, 9, 10, 11):
        row = rank_by_bound37.get(f"exit_bits <= {alpha} * bit_length(n)")
        if not row or int(row.get("violations", 0)) <= 0 or row.get("bounded_status") != "sample_refuted":
            return fail(f"collatz ticket37 must refute {alpha}x bit-length rank in sample")
    alpha12 = rank_by_bound37.get("exit_bits <= 12 * bit_length(n)")
    if not alpha12 or int(alpha12.get("violations", -1)) != 0 or alpha12.get("bounded_status") != "sample_holds":
        return fail("collatz ticket37 must preserve but not prove the 12x bounded rank candidate")
    piecewise37 = probe37.get("candidate_piecewise_linear_rank", {})
    if not isinstance(piecewise37, dict):
        return fail("collatz ticket37 piecewise rank candidate missing")
    if piecewise37.get("sample_status") != "supported_in_bounded_sample_not_proved":
        return fail("collatz ticket37 must not overstate the piecewise rank candidate")
    if "not a Collatz proof" not in str(probe37.get("proof_boundary", "")):
        return fail("collatz ticket37 proof boundary must block proof overclaim")
    route37 = collatz37_bounded.get("route_decision", {})
    if not isinstance(route37, dict):
        return fail("collatz ticket37 route decision missing")
    discard37 = " ".join(str(item) for item in route37.get("discard", []))
    retain37 = " ".join(str(item) for item in route37.get("retain", []))
    if "10 * bit_length" not in discard37 or "11 * bit_length" not in discard37:
        return fail("collatz ticket37 must discard weak linear rank candidates")
    if "symbolic extension lemma" not in retain37:
        return fail("collatz ticket37 must retain the symbolic extension theorem route")

    ticket38_path = Path("data/open-problem/ticket38-symbolic-frontier-extension-lab.json")
    if not ticket38_path.exists():
        return fail("missing ticket38 symbolic frontier extension artifact")
    ticket38 = read_json(ticket38_path)
    if ticket38.get("schema") != TICKET38_SCHEMA:
        return fail("ticket38 symbolic frontier extension artifact has unexpected schema")
    if ticket38.get("status") != "symbolic_frontier_extension_open_no_resolution":
        return fail("ticket38 symbolic frontier extension overstates resolution")
    ticket38_attempts = ticket38.get("attempts", [])
    if not isinstance(ticket38_attempts, list):
        return fail("ticket38 attempts must be a list")
    ticket38_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket38_attempts if isinstance(attempt, dict)}
    missing_ticket38 = EXPECTED_PROBLEMS - set(ticket38_by_id)
    if missing_ticket38:
        return fail("ticket38 attempts missing problems: " + ", ".join(sorted(missing_ticket38)))
    ticket38_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-38-symbolic-zero-extension.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-38-symbolic-frontier-extension.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-38-symbolic-cutoff-extension.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-38-symbolic-gap-extension.json"),
    }
    for problem_id, attempt in ticket38_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket38 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket38 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket38 claim boundary is too weak")
        path = ticket38_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket38 per-problem artifact")

    collatz_ticket38 = ticket38_by_id.get("collatz", {})
    collatz38_bounded = collatz_ticket38.get("bounded_result", {})
    if not isinstance(collatz38_bounded, dict):
        return fail("collatz ticket38 bounded result must be an object")
    audit38 = collatz38_bounded.get("symbolic_frontier_extension_audit", {})
    if not isinstance(audit38, dict):
        return fail("collatz ticket38 symbolic frontier audit missing")
    if int(audit38.get("open_edge_count", 0)) < 700_000:
        return fail("collatz ticket38 must retain a large symbolic open-edge stress set")
    if int(audit38.get("final_frontier_count", 0)) <= 0:
        return fail("collatz ticket38 must retain surviving symbolic frontier cylinders")
    if float(audit38.get("max_survival_ratio", 0.0)) < 0.9:
        return fail("collatz ticket38 must record near-persistent frontier survival")
    lambda_rows38 = audit38.get("lambda_potential_rows", [])
    if not isinstance(lambda_rows38, list) or len(lambda_rows38) < 5:
        return fail("collatz ticket38 must test multiple scalar debt potentials")
    if not all(isinstance(row, dict) and row.get("status") == "scalar_debt_descent_refuted" for row in lambda_rows38):
        return fail("collatz ticket38 must refute every tested scalar debt potential")
    if not any(isinstance(row, dict) and int(row.get("nondecreasing_open_edges", 0)) > 400_000 for row in lambda_rows38):
        return fail("collatz ticket38 must expose many nondecreasing scalar-debt edges")
    extension_tests38 = audit38.get("simple_extension_tests", [])
    if not isinstance(extension_tests38, list):
        return fail("collatz ticket38 simple extension tests missing")
    extension_statuses38 = {str(row.get("status")) for row in extension_tests38 if isinstance(row, dict)}
    for required_status in (
        "refuted_by_surviving_frontier",
        "refuted_for_all_tested_lambdas",
        "insufficient_even_when_mass_ratio_below_one",
    ):
        if required_status not in extension_statuses38:
            return fail(f"collatz ticket38 must record {required_status}")
    if "does not prove Collatz" not in str(audit38.get("proof_boundary", "")):
        return fail("collatz ticket38 proof boundary must block proof overclaim")
    route38 = collatz38_bounded.get("route_decision", {})
    if not isinstance(route38, dict):
        return fail("collatz ticket38 route decision missing")
    discard38 = " ".join(str(item) for item in route38.get("discard", []))
    retain38 = " ".join(str(item) for item in route38.get("retain", []))
    if "scalar debt" not in discard38 or "aggregate mass" not in discard38:
        return fail("collatz ticket38 must discard scalar-debt and aggregate-mass shortcuts")
    if "phase/state" not in retain38:
        return fail("collatz ticket38 must retain the phase/state-dependent potential route")

    ticket39_path = Path("data/open-problem/ticket39-phase-state-potential-lab.json")
    if not ticket39_path.exists():
        return fail("missing ticket39 phase/state potential artifact")
    ticket39 = read_json(ticket39_path)
    if ticket39.get("schema") != TICKET39_SCHEMA:
        return fail("ticket39 phase/state potential artifact has unexpected schema")
    if ticket39.get("status") != "phase_state_potential_open_no_resolution":
        return fail("ticket39 phase/state potential overstates resolution")
    ticket39_attempts = ticket39.get("attempts", [])
    if not isinstance(ticket39_attempts, list):
        return fail("ticket39 attempts must be a list")
    ticket39_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket39_attempts if isinstance(attempt, dict)}
    missing_ticket39 = EXPECTED_PROBLEMS - set(ticket39_by_id)
    if missing_ticket39:
        return fail("ticket39 attempts missing problems: " + ", ".join(sorted(missing_ticket39)))
    ticket39_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-39-phase-state-zero-potential.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-39-phase-state-potential.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-39-state-cone-potential.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-39-gap-leakage-potential.json"),
    }
    for problem_id, attempt in ticket39_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket39 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket39 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket39 claim boundary is too weak")
        path = ticket39_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket39 per-problem artifact")

    collatz_ticket39 = ticket39_by_id.get("collatz", {})
    collatz39_bounded = collatz_ticket39.get("bounded_result", {})
    if not isinstance(collatz39_bounded, dict):
        return fail("collatz ticket39 bounded result must be an object")
    audit39 = collatz39_bounded.get("phase_state_potential_audit", {})
    if not isinstance(audit39, dict):
        return fail("collatz ticket39 phase/state audit missing")
    if int(audit39.get("open_edge_count", 0)) < 700_000:
        return fail("collatz ticket39 must reuse the large symbolic edge set")
    family_rows39 = audit39.get("family_rows", [])
    if not isinstance(family_rows39, list) or len(family_rows39) < 5:
        return fail("collatz ticket39 must compare multiple state families")
    family_by_name39 = {str(row.get("family")): row for row in family_rows39 if isinstance(row, dict)}
    coarse39 = family_by_name39.get("phase_mod8_tail4_residue64", {})
    coarse_topo39 = coarse39.get("topological_potential", {}) if isinstance(coarse39, dict) else {}
    if coarse39.get("status") != "blocked_by_phase_state_cycle":
        return fail("collatz ticket39 must reject the coarse phase/state quotient")
    if not isinstance(coarse_topo39, dict) or int(coarse_topo39.get("cyclic_core_node_count", 0)) <= 0:
        return fail("collatz ticket39 coarse quotient must expose a cyclic core")
    candidate39 = family_by_name39.get("phase_mod16_tail4_residue256", {})
    candidate_topo39 = candidate39.get("topological_potential", {}) if isinstance(candidate39, dict) else {}
    if candidate39.get("status") != "finite_window_dag_rank_candidate":
        return fail("collatz ticket39 must retain the phase_mod16 finite DAG candidate")
    if not isinstance(candidate_topo39, dict) or candidate_topo39.get("cycle_detected") is not False:
        return fail("collatz ticket39 phase_mod16 candidate must be acyclic in the finite window")
    if int(candidate_topo39.get("max_topological_rank", 0)) < 12:
        return fail("collatz ticket39 phase_mod16 candidate must synthesize a nontrivial rank")
    if int(candidate_topo39.get("rank_edge_violations", -1)) != 0:
        return fail("collatz ticket39 finite DAG rank must have no sampled edge violations")
    deep39 = audit39.get("deep_wrap_probe", {})
    if not isinstance(deep39, dict):
        return fail("collatz ticket39 deep wrap probe missing")
    if int(deep39.get("max_bits", 0)) < 28 or int(deep39.get("open_edge_count", 0)) < 7_000_000:
        return fail("collatz ticket39 must include the deeper phase-wrap stress probe")
    deep_topo39 = deep39.get("topological_potential", {})
    if not isinstance(deep_topo39, dict) or deep_topo39.get("cycle_detected") is not False:
        return fail("collatz ticket39 deep wrap probe must remain acyclic in the sampled quotient")
    if int(deep_topo39.get("rank_edge_violations", -1)) != 0:
        return fail("collatz ticket39 deep wrap rank must have no sampled edge violations")
    route39 = collatz39_bounded.get("route_decision", {})
    if not isinstance(route39, dict):
        return fail("collatz ticket39 route decision missing")
    discard39 = " ".join(str(item) for item in route39.get("discard", []))
    retain39 = " ".join(str(item) for item in route39.get("retain", []))
    if "finite-window DAG" not in discard39:
        return fail("collatz ticket39 must reject finite-window DAG overclaiming")
    if "transition-closure theorem" not in retain39:
        return fail("collatz ticket39 must retain transition closure as the next theorem target")

    ticket40_path = Path("data/open-problem/ticket40-transition-closure-lab.json")
    if not ticket40_path.exists():
        return fail("missing ticket40 transition closure artifact")
    ticket40 = read_json(ticket40_path)
    if ticket40.get("schema") != TICKET40_SCHEMA:
        return fail("ticket40 transition closure artifact has unexpected schema")
    if ticket40.get("status") != "transition_closure_open_no_resolution":
        return fail("ticket40 transition closure overstates resolution")
    ticket40_attempts = ticket40.get("attempts", [])
    if not isinstance(ticket40_attempts, list):
        return fail("ticket40 attempts must be a list")
    ticket40_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket40_attempts if isinstance(attempt, dict)}
    missing_ticket40 = EXPECTED_PROBLEMS - set(ticket40_by_id)
    if missing_ticket40:
        return fail("ticket40 attempts missing problems: " + ", ".join(sorted(missing_ticket40)))
    ticket40_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-40-zero-transition-closure.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-40-transition-closure.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-40-error-cone-transition-closure.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-40-gap-leakage-transition-closure.json"),
    }
    for problem_id, attempt in ticket40_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket40 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket40 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket40 claim boundary is too weak")
        path = ticket40_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket40 per-problem artifact")

    collatz_ticket40 = ticket40_by_id.get("collatz", {})
    collatz40_bounded = collatz_ticket40.get("bounded_result", {})
    if not isinstance(collatz40_bounded, dict):
        return fail("collatz ticket40 bounded result must be an object")
    audit40 = collatz40_bounded.get("transition_closure_audit", {})
    if not isinstance(audit40, dict):
        return fail("collatz ticket40 transition closure audit missing")
    primary40 = audit40.get("primary_window", {})
    extension40 = audit40.get("extension_probe", {})
    if not isinstance(primary40, dict) or not isinstance(extension40, dict):
        return fail("collatz ticket40 primary and extension windows must be objects")
    if int(primary40.get("max_bits", 0)) < 24 or int(extension40.get("max_bits", 0)) < 26:
        return fail("collatz ticket40 must include primary and extension transition windows")
    if int(primary40.get("parent_instance_count", 0)) < 380_000:
        return fail("collatz ticket40 primary window must reuse the large phase/state frontier")
    if int(extension40.get("parent_instance_count", 0)) < 1_200_000:
        return fail("collatz ticket40 extension probe must stress more than one million parent instances")
    if int(primary40.get("ambiguous_label_state_count", -1)) != 0:
        return fail("collatz ticket40 should preserve the sampled label-level closure fact")
    if int(primary40.get("ambiguous_child_signature_state_count", 0)) < 30_000:
        return fail("collatz ticket40 must refute deterministic child-state closure in the primary window")
    if int(extension40.get("ambiguous_child_signature_state_count", 0)) < 90_000:
        return fail("collatz ticket40 must show deterministic child-state collisions persist in the extension probe")
    deterministic40 = primary40.get("deterministic_transition_closure", {})
    if not isinstance(deterministic40, dict):
        return fail("collatz ticket40 deterministic closure result missing")
    if deterministic40.get("status") != "refuted_by_child_state_signature_collision":
        return fail("collatz ticket40 must reject deterministic exact-child transition closure")
    if not deterministic40.get("ambiguous_examples"):
        return fail("collatz ticket40 must include ambiguous transition examples")
    nondeterministic40 = extension40.get("nondeterministic_transition_relation", {})
    if not isinstance(nondeterministic40, dict):
        return fail("collatz ticket40 nondeterministic relation result missing")
    topo40 = nondeterministic40.get("topological_potential", {})
    if not isinstance(topo40, dict) or topo40.get("cycle_detected") is not False:
        return fail("collatz ticket40 extension probe must remain acyclic in the sampled nondeterministic relation")
    if int(topo40.get("rank_edge_violations", -1)) != 0:
        return fail("collatz ticket40 sampled nondeterministic rank must have no edge violations")
    if int(topo40.get("max_topological_rank", 0)) < 14:
        return fail("collatz ticket40 extension probe must retain a nontrivial rank")
    closure_tests40 = audit40.get("closure_tests", [])
    if not isinstance(closure_tests40, list):
        return fail("collatz ticket40 closure tests missing")
    closure_status40 = " ".join(str(row.get("status")) for row in closure_tests40 if isinstance(row, dict))
    if "refuted_by_child_state_signature_collision" not in closure_status40:
        return fail("collatz ticket40 closure tests must record deterministic refutation")
    route40 = collatz40_bounded.get("route_decision", {})
    if not isinstance(route40, dict):
        return fail("collatz ticket40 route decision missing")
    discard40 = " ".join(str(item) for item in route40.get("discard", []))
    retain40 = " ".join(str(item) for item in route40.get("retain", []))
    if "deterministic exact-child" not in discard40 or "finite-window acyclic rank" not in discard40:
        return fail("collatz ticket40 must discard deterministic closure and finite-window overclaims")
    if "nondeterministic acyclic transition relation" not in retain40 or "cycle" not in retain40:
        return fail("collatz ticket40 must retain nondeterministic closure and cycle search")
    if "not a Collatz proof" not in str(audit40.get("proof_boundary", "")):
        return fail("collatz ticket40 proof boundary must block proof overclaim")

    ticket41_path = Path("data/open-problem/ticket41-rank-escape-normalization-lab.json")
    if not ticket41_path.exists():
        return fail("missing ticket41 rank escape normalization artifact")
    ticket41 = read_json(ticket41_path)
    if ticket41.get("schema") != TICKET41_SCHEMA:
        return fail("ticket41 rank escape normalization artifact has unexpected schema")
    if ticket41.get("status") != "rank_escape_normalization_open_no_resolution":
        return fail("ticket41 rank escape normalization overstates resolution")
    ticket41_attempts = ticket41.get("attempts", [])
    if not isinstance(ticket41_attempts, list):
        return fail("ticket41 attempts must be a list")
    ticket41_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket41_attempts if isinstance(attempt, dict)}
    missing_ticket41 = EXPECTED_PROBLEMS - set(ticket41_by_id)
    if missing_ticket41:
        return fail("ticket41 attempts missing problems: " + ", ".join(sorted(missing_ticket41)))
    ticket41_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-41-parametric-zero-state-normalization.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-41-rank-escape-normalization.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-41-parametric-error-cone-normalization.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-41-parametric-gap-leakage-normalization.json"),
    }
    for problem_id, attempt in ticket41_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket41 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket41 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket41 claim boundary is too weak")
        path = ticket41_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket41 per-problem artifact")

    collatz_ticket41 = ticket41_by_id.get("collatz", {})
    collatz41_bounded = collatz_ticket41.get("bounded_result", {})
    if not isinstance(collatz41_bounded, dict):
        return fail("collatz ticket41 bounded result must be an object")
    audit41 = collatz41_bounded.get("rank_escape_normalization_audit", {})
    if not isinstance(audit41, dict):
        return fail("collatz ticket41 rank escape audit missing")
    snapshots41 = audit41.get("snapshots", [])
    if not isinstance(snapshots41, list) or len(snapshots41) < 3:
        return fail("collatz ticket41 must include 24, 25, and 26 bit snapshots")
    by_bits41 = {int(row.get("max_bits", 0)): row for row in snapshots41 if isinstance(row, dict)}
    for bits in (24, 25, 26):
        if bits not in by_bits41:
            return fail(f"collatz ticket41 missing {bits}-bit snapshot")
    if int(by_bits41[26].get("state_edge_count", 0)) < 1_000_000:
        return fail("collatz ticket41 26-bit snapshot must retain the large relation")
    topo41 = by_bits41[26].get("topological_potential", {})
    if not isinstance(topo41, dict) or topo41.get("cycle_detected") is not False:
        return fail("collatz ticket41 sampled relation must remain acyclic through 26 bits")
    if int(topo41.get("rank_edge_violations", -1)) != 0:
        return fail("collatz ticket41 sampled rank must keep zero edge violations")
    comparisons41 = audit41.get("extension_comparisons", [])
    if not isinstance(comparisons41, list) or len(comparisons41) < 2:
        return fail("collatz ticket41 must compare successive horizon extensions")
    first41, second41 = comparisons41[0], comparisons41[1]
    if int(first41.get("new_state_edge_count", 0)) < 200_000:
        return fail("collatz ticket41 24->25 must expose many new edges")
    if int(first41.get("previous_sink_reopened_count", 0)) < 80_000:
        return fail("collatz ticket41 24->25 must expose many reopened previous sinks")
    if int(second41.get("new_state_edge_count", 0)) < 300_000:
        return fail("collatz ticket41 25->26 must expose many new edges")
    if int(second41.get("previous_sink_reopened_count", 0)) < 120_000:
        return fail("collatz ticket41 25->26 must expose many reopened previous sinks")
    if first41.get("closure_status") != "refuted_for_fixed_window_relation":
        return fail("collatz ticket41 must reject fixed 24-bit relation closure")
    if second41.get("closure_status") != "refuted_for_fixed_window_relation":
        return fail("collatz ticket41 must reject fixed 25-bit relation closure")
    growth41 = audit41.get("coordinate_growth_after_primary", {})
    if not isinstance(growth41, dict) or int(growth41.get("distinct_coordinate_delta", 0)) < 300:
        return fail("collatz ticket41 must expose unbounded coordinate growth pressure")
    fixed_tests41 = audit41.get("fixed_relation_tests", [])
    if not isinstance(fixed_tests41, list):
        return fail("collatz ticket41 fixed relation tests missing")
    fixed_status41 = " ".join(str(row.get("status")) for row in fixed_tests41 if isinstance(row, dict))
    if "refuted_by_unbounded_window_coordinates" not in fixed_status41:
        return fail("collatz ticket41 must refute the global finite quotient shortcut")
    route41 = collatz41_bounded.get("route_decision", {})
    if not isinstance(route41, dict):
        return fail("collatz ticket41 route decision missing")
    discard41 = " ".join(str(item) for item in route41.get("discard", []))
    retain41 = " ".join(str(item) for item in route41.get("retain", []))
    if "fixed finite-window DAG" not in discard41 or "global finite quotient" not in discard41:
        return fail("collatz ticket41 must discard fixed-window and finite-quotient overclaims")
    if "parametric symbolic transition schema" not in retain41 or "counterexample search" not in retain41:
        return fail("collatz ticket41 must retain parametric symbolic closure and counterexample search")
    if "not a Collatz proof" not in str(audit41.get("proof_boundary", "")):
        return fail("collatz ticket41 proof boundary must block proof overclaim")

    ticket42_path = Path("data/open-problem/ticket42-parametric-transition-template-lab.json")
    if not ticket42_path.exists():
        return fail("missing ticket42 parametric transition template artifact")
    ticket42 = read_json(ticket42_path)
    if ticket42.get("schema") != TICKET42_SCHEMA:
        return fail("ticket42 parametric transition template artifact has unexpected schema")
    if ticket42.get("status") != "parametric_template_open_no_resolution":
        return fail("ticket42 parametric transition template overstates resolution")
    ticket42_attempts = ticket42.get("attempts", [])
    if not isinstance(ticket42_attempts, list):
        return fail("ticket42 attempts must be a list")
    ticket42_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket42_attempts if isinstance(attempt, dict)}
    missing_ticket42 = EXPECTED_PROBLEMS - set(ticket42_by_id)
    if missing_ticket42:
        return fail("ticket42 attempts missing problems: " + ", ".join(sorted(missing_ticket42)))
    ticket42_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-42-parametric-zero-template.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-42-parametric-transition-template.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-42-parametric-error-template.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-42-parametric-gap-template.json"),
    }
    for problem_id, attempt in ticket42_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket42 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket42 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket42 claim boundary is too weak")
        path = ticket42_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket42 per-problem artifact")

    collatz_ticket42 = ticket42_by_id.get("collatz", {})
    collatz42_bounded = collatz_ticket42.get("bounded_result", {})
    if not isinstance(collatz42_bounded, dict):
        return fail("collatz ticket42 bounded result must be an object")
    audit42 = collatz42_bounded.get("parametric_transition_template_audit", {})
    if not isinstance(audit42, dict):
        return fail("collatz ticket42 template audit missing")
    if int(audit42.get("base_bits", 0)) != 12 or int(audit42.get("max_bits", 0)) != 26:
        return fail("collatz ticket42 must audit the 12..26 frontier")
    if audit42.get("cycle_search_status") != "no_sampled_template_cycle_found_through_26_bits":
        return fail("collatz ticket42 must not invent a sampled template cycle")
    if audit42.get("sharp_family_status") != "not_refuted_in_sampled_template_graph":
        return fail("collatz ticket42 must preserve the bounded template-rank route")
    if int(audit42.get("total_ambiguous_template_edge_count", 0)) < 25_000:
        return fail("collatz ticket42 must expose ambiguous coordinate-delta pressure")
    family_rows42 = audit42.get("family_rows", [])
    if not isinstance(family_rows42, list) or len(family_rows42) < 4:
        return fail("collatz ticket42 must include all template families")
    sharp42 = family_rows42[-1]
    if sharp42.get("family") != "phase16_tail4_residue256_vexact":
        return fail("collatz ticket42 sharp template family mismatch")
    if int(sharp42.get("template_node_count", 0)) < 160_000:
        return fail("collatz ticket42 sharp family must retain a large template graph")
    if int(sharp42.get("template_edge_count", 0)) < 700_000:
        return fail("collatz ticket42 sharp family must retain many template edges")
    if int(sharp42.get("raw_open_edge_count", 0)) < 2_300_000:
        return fail("collatz ticket42 must process the full raw open-edge frontier")
    if int(sharp42.get("raw_nondecreasing_debt_edge_count", 0)) < 1_500_000:
        return fail("collatz ticket42 must expose raw nondecreasing debt pressure")
    if int(sharp42.get("cyclic_component_count", -1)) != 0:
        return fail("collatz ticket42 sharp family must report no sampled cycle")
    if sharp42.get("strict_template_rank_status") != "not_refuted_in_sampled_template_graph":
        return fail("collatz ticket42 sharp family status must avoid overclaim")
    if int(sharp42.get("ambiguous_template_edge_count", 0)) < 5_000:
        return fail("collatz ticket42 sharp family must expose ambiguous template deltas")
    schema42 = audit42.get("parametric_schema", {})
    if not isinstance(schema42, dict):
        return fail("collatz ticket42 parametric schema missing")
    schema_text42 = " ".join(str(item) for item in schema42.get("template_update", []))
    if "debt'" not in schema_text42 or "delta_prefix" not in schema_text42:
        return fail("collatz ticket42 schema must include debt and delta updates")
    route42 = audit42.get("route_decision", {})
    if not isinstance(route42, dict):
        return fail("collatz ticket42 route decision missing")
    discard42 = " ".join(str(item) for item in route42.get("discard", []))
    retain42 = " ".join(str(item) for item in route42.get("retain", []))
    if "absence of sampled template cycles" not in discard42 or "finite template edge" not in discard42:
        return fail("collatz ticket42 must block acyclicity and deterministic-edge overclaims")
    if "parametric transition schema" not in retain42 or "cycle-lift search" not in retain42 or "well-founded measure" not in retain42:
        return fail("collatz ticket42 must retain lift, cycle, and well-founded proof routes")
    if "not a Collatz proof" not in str(audit42.get("proof_boundary", "")):
        return fail("collatz ticket42 proof boundary must block proof overclaim")

    ticket43_path = Path("data/open-problem/ticket43-lift-constraint-measure-lab.json")
    if not ticket43_path.exists():
        return fail("missing ticket43 lift constraint measure artifact")
    ticket43 = read_json(ticket43_path)
    if ticket43.get("schema") != TICKET43_SCHEMA:
        return fail("ticket43 lift constraint measure artifact has unexpected schema")
    if ticket43.get("status") != "lift_constraint_measure_open_no_resolution":
        return fail("ticket43 lift constraint measure overstates resolution")
    ticket43_attempts = ticket43.get("attempts", [])
    if not isinstance(ticket43_attempts, list):
        return fail("ticket43 attempts must be a list")
    ticket43_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket43_attempts if isinstance(attempt, dict)}
    missing_ticket43 = EXPECTED_PROBLEMS - set(ticket43_by_id)
    if missing_ticket43:
        return fail("ticket43 attempts missing problems: " + ", ".join(sorted(missing_ticket43)))
    ticket43_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-43-zero-lift-measure.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-43-lift-constraint-measure.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-43-error-lift-measure.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-43-gap-lift-measure.json"),
    }
    for problem_id, attempt in ticket43_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket43 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket43 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket43 claim boundary is too weak")
        path = ticket43_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket43 per-problem artifact")

    collatz_ticket43 = ticket43_by_id.get("collatz", {})
    collatz43_bounded = collatz_ticket43.get("bounded_result", {})
    if not isinstance(collatz43_bounded, dict):
        return fail("collatz ticket43 bounded result must be an object")
    audit43 = collatz43_bounded.get("lift_constraint_measure_audit", {})
    if not isinstance(audit43, dict):
        return fail("collatz ticket43 lift measure audit missing")
    snapshots43 = audit43.get("snapshots", [])
    if not isinstance(snapshots43, list) or [row.get("max_bits") for row in snapshots43] != [24, 25, 26]:
        return fail("collatz ticket43 must audit the 24,25,26 lift snapshots")
    final43 = snapshots43[-1]
    if int(final43.get("template_node_count", 0)) < 160_000:
        return fail("collatz ticket43 final snapshot must retain a large template graph")
    if int(final43.get("template_edge_count", 0)) < 700_000:
        return fail("collatz ticket43 final snapshot must retain many template edges")
    if int(final43.get("raw_open_edge_count", 0)) < 2_300_000:
        return fail("collatz ticket43 final snapshot must process the full raw open-edge frontier")
    rank43 = final43.get("topological_template_rank", {})
    if not isinstance(rank43, dict):
        return fail("collatz ticket43 final rank summary missing")
    if rank43.get("cycle_detected") is not False or int(rank43.get("rank_edge_violations", -1)) != 0:
        return fail("collatz ticket43 final sampled rank must be acyclic with no rank violations")
    if int(rank43.get("max_topological_rank", 0)) < 14:
        return fail("collatz ticket43 final sampled rank unexpectedly shallow")
    measure43 = final43.get("sampled_rank_debt_measure", {})
    if not isinstance(measure43, dict):
        return fail("collatz ticket43 sampled measure missing")
    if measure43.get("status") != "sampled_measure_decreases_on_all_template_edges":
        return fail("collatz ticket43 sampled measure must decrease on all sampled template edges")
    if int(measure43.get("scale", 0)) < 1 or float(measure43.get("min_margin", 0.0)) <= 0.0:
        return fail("collatz ticket43 sampled measure must have positive scale and margin")
    if int(measure43.get("invalid_rank_gap_edges", -1)) != 0:
        return fail("collatz ticket43 sampled measure must have no invalid rank-gap edges")
    comparisons43 = audit43.get("extension_comparisons", [])
    if not isinstance(comparisons43, list) or len(comparisons43) != 2:
        return fail("collatz ticket43 must compare 24->25 and 25->26 extensions")
    latest43 = comparisons43[-1]
    if int(latest43.get("new_template_edge_count", 0)) < 200_000:
        return fail("collatz ticket43 must expose substantial new template edges under horizon extension")
    if int(latest43.get("rank_changed_previous_node_count", 0)) < 100_000:
        return fail("collatz ticket43 must expose previous-rank instability under horizon extension")
    if int(latest43.get("old_measure_unknown_rank_edges", 0)) < 200_000:
        return fail("collatz ticket43 must expose old-measure unknown edges under horizon extension")
    if latest43.get("closure_status") != "rank_lift_not_closed_under_horizon_extension":
        return fail("collatz ticket43 must keep lift closure open")
    route43 = audit43.get("route_decision", {})
    if not isinstance(route43, dict):
        return fail("collatz ticket43 route decision missing")
    discard43 = " ".join(str(item) for item in route43.get("discard", []))
    retain43 = " ".join(str(item) for item in route43.get("retain", []))
    if "debt-only descent" not in discard43 or "previous horizon topological rank" not in discard43:
        return fail("collatz ticket43 must discard debt-only and previous-rank overclaims")
    if "sampled scale*rank+debt" not in discard43:
        return fail("collatz ticket43 must block treating sampled measure as theorem")
    if "sampled scale*template_rank+debt measure" not in retain43 or "parametric lift constraints" not in retain43:
        return fail("collatz ticket43 must retain sampled measure and parametric lift constraints")
    if "not a Collatz proof" not in str(audit43.get("proof_boundary", "")):
        return fail("collatz ticket43 proof boundary must block proof overclaim")

    ticket44_path = Path("data/open-problem/ticket44-feature-measure-counteredge-lab.json")
    if not ticket44_path.exists():
        return fail("missing ticket44 feature measure counteredge artifact")
    ticket44 = read_json(ticket44_path)
    if ticket44.get("schema") != TICKET44_SCHEMA:
        return fail("ticket44 feature measure counteredge artifact has unexpected schema")
    if ticket44.get("status") != "feature_measure_counteredge_open_no_resolution":
        return fail("ticket44 feature measure counteredge overstates resolution")
    ticket44_attempts = ticket44.get("attempts", [])
    if not isinstance(ticket44_attempts, list):
        return fail("ticket44 attempts must be a list")
    ticket44_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket44_attempts if isinstance(attempt, dict)}
    missing_ticket44 = EXPECTED_PROBLEMS - set(ticket44_by_id)
    if missing_ticket44:
        return fail("ticket44 attempts missing problems: " + ", ".join(sorted(missing_ticket44)))
    ticket44_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-44-zero-feature-counteredge.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-44-feature-measure-counteredge.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-44-margin-feature-counteredge.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-44-gap-feature-counteredge.json"),
    }
    for problem_id, attempt in ticket44_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket44 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket44 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket44 claim boundary is too weak")
        path = ticket44_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket44 per-problem artifact")

    collatz_ticket44 = ticket44_by_id.get("collatz", {})
    collatz44_bounded = collatz_ticket44.get("bounded_result", {})
    if not isinstance(collatz44_bounded, dict):
        return fail("collatz ticket44 bounded result must be an object")
    audit44 = collatz44_bounded.get("feature_measure_counteredge_audit", {})
    if not isinstance(audit44, dict):
        return fail("collatz ticket44 feature measure audit missing")
    if int(audit44.get("template_node_count", 0)) < 160_000:
        return fail("collatz ticket44 must retain a large template graph")
    if int(audit44.get("template_edge_count", 0)) < 700_000:
        return fail("collatz ticket44 must retain many template edges")
    if int(audit44.get("raw_open_edge_count", 0)) < 2_300_000:
        return fail("collatz ticket44 must process the full raw open-edge frontier")
    if int(audit44.get("exactly_refuted_feature_family_count", 0)) < 1:
        return fail("collatz ticket44 must exactly refute at least one weak feature family")
    feature_trials44 = audit44.get("feature_trials", [])
    if not isinstance(feature_trials44, list) or len(feature_trials44) < 5:
        return fail("collatz ticket44 must include the debt control and richer feature trials")
    trial44_by_name = {str(trial.get("feature_family")): trial for trial in feature_trials44 if isinstance(trial, dict)}
    debt_trial44 = trial44_by_name.get("debt_only_constant", {})
    if debt_trial44.get("status") != "exact_zero_delta_counteredge_refutes_feature_measure":
        return fail("collatz ticket44 must exactly refute debt-only descent")
    if int(debt_trial44.get("zero_delta_refuter_count", 0)) < 300_000:
        return fail("collatz ticket44 debt-only refuter count unexpectedly small")
    rich_trial44 = trial44_by_name.get("phase_residue_onehot_tail_numeric", {})
    rich_search44 = rich_trial44.get("sampled_affine_search", {}) if isinstance(rich_trial44, dict) else {}
    if rich_trial44.get("status") != "not_certified_by_bounded_affine_search":
        return fail("collatz ticket44 rich feature family must remain unproved")
    if int(rich_search44.get("violating_unique_constraints", 0)) < 1:
        return fail("collatz ticket44 rich affine search must expose unresolved constraints")
    rank_baseline44 = audit44.get("rank_table_baseline", {})
    if not isinstance(rank_baseline44, dict):
        return fail("collatz ticket44 rank table baseline missing")
    measure44 = rank_baseline44.get("sampled_rank_debt_measure", {})
    if not isinstance(measure44, dict) or measure44.get("status") != "sampled_measure_decreases_on_all_template_edges":
        return fail("collatz ticket44 must preserve the bounded rank-table certificate")
    extension44 = audit44.get("horizon_extension_gate", {})
    if not isinstance(extension44, dict):
        return fail("collatz ticket44 horizon extension gate missing")
    if int(extension44.get("new_template_edge_count", 0)) < 200_000:
        return fail("collatz ticket44 must preserve the TICKET43 new-edge obstruction")
    if extension44.get("closure_status") != "rank_lift_not_closed_under_horizon_extension":
        return fail("collatz ticket44 must keep horizon closure open")
    route44 = audit44.get("route_decision", {})
    if not isinstance(route44, dict):
        return fail("collatz ticket44 route decision missing")
    discard44 = " ".join(str(item) for item in route44.get("discard", []))
    retain44 = " ".join(str(item) for item in route44.get("retain", []))
    if "debt-only" not in discard44 or "observed-node rank table" not in discard44:
        return fail("collatz ticket44 must discard debt-only and observed rank-table overclaims")
    if "exact counteredge extraction" not in retain44 or "horizon-independent symbolic rank" not in retain44:
        return fail("collatz ticket44 must retain counteredge extraction and symbolic-rank route")
    if "No Collatz proof" not in str(audit44.get("proof_boundary", "")):
        return fail("collatz ticket44 proof boundary must block proof overclaim")

    ticket45_path = Path("data/open-problem/ticket45-symbolic-rank-clause-lab.json")
    if not ticket45_path.exists():
        return fail("missing ticket45 symbolic rank clause artifact")
    ticket45 = read_json(ticket45_path)
    if ticket45.get("schema") != TICKET45_SCHEMA:
        return fail("ticket45 symbolic rank clause artifact has unexpected schema")
    if ticket45.get("status") != "symbolic_rank_clause_open_no_resolution":
        return fail("ticket45 symbolic rank clause overstates resolution")
    ticket45_attempts = ticket45.get("attempts", [])
    if not isinstance(ticket45_attempts, list):
        return fail("ticket45 attempts must be a list")
    ticket45_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket45_attempts if isinstance(attempt, dict)}
    missing_ticket45 = EXPECTED_PROBLEMS - set(ticket45_by_id)
    if missing_ticket45:
        return fail("ticket45 attempts missing problems: " + ", ".join(sorted(missing_ticket45)))
    ticket45_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-45-symbolic-zero-clause.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-45-symbolic-rank-clause.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-45-symbolic-margin-clause.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-45-symbolic-gap-clause.json"),
    }
    for problem_id, attempt in ticket45_by_id.items():
        if attempt.get("status") != "proof_pressure_open":
            return fail(f"{problem_id}: ticket45 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket45 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket45 claim boundary is too weak")
        path = ticket45_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket45 per-problem artifact")

    collatz_ticket45 = ticket45_by_id.get("collatz", {})
    collatz45_bounded = collatz_ticket45.get("bounded_result", {})
    if not isinstance(collatz45_bounded, dict):
        return fail("collatz ticket45 bounded result must be an object")
    audit45 = collatz45_bounded.get("symbolic_rank_clause_audit", {})
    if not isinstance(audit45, dict):
        return fail("collatz ticket45 symbolic rank audit missing")
    if int(audit45.get("template_node_count", 0)) < 160_000:
        return fail("collatz ticket45 must retain a large template graph")
    if int(audit45.get("template_edge_count", 0)) < 700_000:
        return fail("collatz ticket45 must retain many template edges")
    if int(audit45.get("raw_open_edge_count", 0)) < 2_300_000:
        return fail("collatz ticket45 must process the full raw open-edge frontier")
    if int(audit45.get("future_refuted_clause_family_count", 0)) < 1:
        return fail("collatz ticket45 must refute a future symbolic clause family")
    clause_trials45 = audit45.get("clause_trials", [])
    if not isinstance(clause_trials45, list) or len(clause_trials45) < 5:
        return fail("collatz ticket45 must include all symbolic clause trials")
    trial45_by_name = {str(trial.get("clause_family")): trial for trial in clause_trials45 if isinstance(trial, dict)}
    phase45 = trial45_by_name.get("phase_only", {})
    if phase45.get("status") != "sampled_symbolic_clause_rank_found_not_proof":
        return fail("collatz ticket45 phase-only 26-bit precursor status changed")
    phase45_interval = phase45.get("scale_interval", {}) if isinstance(phase45, dict) else {}
    if int(phase45_interval.get("selected_scale", 0)) != 11:
        return fail("collatz ticket45 phase-only precursor must use scale 11")
    if float(phase45_interval.get("min_margin_at_selected_scale", 0.0)) <= 0.0:
        return fail("collatz ticket45 phase-only precursor must have positive bounded margin")
    exact45 = trial45_by_name.get("phase_tail_residue256_vexact", {})
    if exact45.get("status") != "not_certified_by_symbolic_clause_scale_interval":
        return fail("collatz ticket45 exact-template pressure-rank interval must remain uncertified")
    wrap45 = audit45.get("phase_wrap_probe_28", {})
    if not isinstance(wrap45, dict):
        return fail("collatz ticket45 phase-wrap probe missing")
    wrap_analysis45 = wrap45.get("analysis", {})
    wrap_extension45 = wrap45.get("extension", {})
    if wrap_analysis45.get("status") != "pressure_cycle_counterexample_refutes_clause_rank":
        return fail("collatz ticket45 must refute phase-only rank by pressure cycle")
    if int(wrap_extension45.get("from_max_bits", 0)) != 27 or int(wrap_extension45.get("to_max_bits", 0)) != 28:
        return fail("collatz ticket45 phase-wrap probe must audit 27->28")
    if int(wrap_extension45.get("new_pressure_clause_edge_count", 0)) < 1:
        return fail("collatz ticket45 phase-wrap probe must expose a new pressure edge")
    wrap_examples45 = wrap_extension45.get("new_pressure_examples", [])
    if not isinstance(wrap_examples45, list) or not wrap_examples45:
        return fail("collatz ticket45 phase-wrap probe missing pressure example")
    first_wrap45 = wrap_examples45[0]
    if first_wrap45.get("parent_clause") != "[11]" or first_wrap45.get("child_clause") != "[12]":
        return fail("collatz ticket45 phase-wrap counteredge must close 11->12")
    if float(first_wrap45.get("max_delta_debt", 0.0)) <= 7.0:
        return fail("collatz ticket45 phase-wrap counteredge unexpectedly weak")
    if int(first_wrap45.get("count", 0)) < 3_000_000:
        return fail("collatz ticket45 phase-wrap counteredge count unexpectedly small")
    if int(audit45.get("exact_template_new_pressure_edge_count_25_to_26", 0)) < 100_000:
        return fail("collatz ticket45 must preserve exact-template horizon pressure")
    route45 = audit45.get("route_decision", {})
    if not isinstance(route45, dict):
        return fail("collatz ticket45 route decision missing")
    discard45 = " ".join(str(item) for item in route45.get("discard", []))
    retain45 = " ".join(str(item) for item in route45.get("retain", []))
    if "phase-only rank" not in discard45 or "observed exact-template rank table" not in discard45:
        return fail("collatz ticket45 must discard phase-only and observed-rank overclaims")
    if "pressure-cycle extraction" not in retain45 or "future symbolic family" not in retain45:
        return fail("collatz ticket45 must retain pressure-cycle and stable symbolic-family routes")
    if "No Collatz proof" not in str(audit45.get("proof_boundary", "")):
        return fail("collatz ticket45 proof boundary must block proof overclaim")

    ticket46_path = Path("data/open-problem/ticket46-stable-clause-grammar-lab.json")
    if not ticket46_path.exists():
        return fail("missing ticket46 stable clause grammar artifact")
    ticket46 = read_json(ticket46_path)
    if ticket46.get("schema") != TICKET46_SCHEMA:
        return fail("ticket46 stable clause grammar artifact has unexpected schema")
    if ticket46.get("status") != "stable_clause_grammar_restricted_no_go_open_no_resolution":
        return fail("ticket46 stable clause grammar overstates resolution")
    ticket46_attempts = ticket46.get("attempts", [])
    if not isinstance(ticket46_attempts, list):
        return fail("ticket46 attempts must be a list")
    ticket46_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket46_attempts if isinstance(attempt, dict)}
    missing_ticket46 = EXPECTED_PROBLEMS - set(ticket46_by_id)
    if missing_ticket46:
        return fail("ticket46 attempts missing problems: " + ", ".join(sorted(missing_ticket46)))
    ticket46_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-46-stable-zero-grammar.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-46-stable-clause-grammar.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-46-stable-margin-grammar.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-46-stable-gap-grammar.json"),
    }
    for problem_id, attempt in ticket46_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "restricted_proof_route_refuted_open_problem_open",
        }:
            return fail(f"{problem_id}: ticket46 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket46 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket46 claim boundary is too weak")
        path = ticket46_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket46 per-problem artifact")

    collatz_ticket46 = ticket46_by_id.get("collatz", {})
    collatz46_bounded = collatz_ticket46.get("bounded_result", {})
    if not isinstance(collatz46_bounded, dict):
        return fail("collatz ticket46 bounded result must be an object")
    audit46 = collatz46_bounded.get("stable_clause_grammar_audit", {})
    if not isinstance(audit46, dict):
        return fail("collatz ticket46 stable clause grammar audit missing")
    if int(audit46.get("template_node_count_28", 0)) < 260_000:
        return fail("collatz ticket46 must retain the 28-bit template graph")
    if int(audit46.get("template_edge_count_28", 0)) < 1_300_000:
        return fail("collatz ticket46 must retain the 28-bit template edge set")
    if int(audit46.get("raw_open_edge_count_28", 0)) < 7_000_000:
        return fail("collatz ticket46 must process the 28-bit raw open-edge frontier")
    if int(audit46.get("tested_clause_family_count", 0)) != 5:
        return fail("collatz ticket46 must test all TICKET45 clause families")
    if int(audit46.get("refuted_clause_family_count_28", 0)) != 5:
        return fail("collatz ticket46 must refute all tested 28-bit scalar clause families")
    if int(audit46.get("stable_clause_family_count_28", 1)) != 0:
        return fail("collatz ticket46 must not report a stable scalar clause family")
    stability46 = audit46.get("stability_summary", [])
    if not isinstance(stability46, list) or len(stability46) != 5:
        return fail("collatz ticket46 stability summary must include five families")
    stability46_by_name = {str(row.get("clause_family")): row for row in stability46 if isinstance(row, dict)}
    for family_name, row in stability46_by_name.items():
        if row.get("status") != "pressure_cycle_counterexample_refutes_clause_rank":
            return fail(f"collatz ticket46 {family_name} must be pressure-cycle refuted")
        if row.get("cycle_detected_28") is not True:
            return fail(f"collatz ticket46 {family_name} must expose a 28-bit pressure cycle")
    exact46 = stability46_by_name.get("phase_tail_residue256_vexact", {})
    if int(exact46.get("new_pressure_edge_count_27_to_28", 0)) < 180_000:
        return fail("collatz ticket46 exact-template grammar must expose large new 27->28 pressure")
    first_wrap46 = audit46.get("first_phase_wrap_pressure_edge", {})
    if not isinstance(first_wrap46, dict):
        return fail("collatz ticket46 first phase-wrap edge missing")
    if first_wrap46.get("parent_clause") != "[11]" or first_wrap46.get("child_clause") != "[12]":
        return fail("collatz ticket46 phase-wrap edge must close 11->12")
    if float(first_wrap46.get("max_delta_debt", 0.0)) <= 7.0:
        return fail("collatz ticket46 phase-wrap edge unexpectedly weak")
    if int(first_wrap46.get("count", 0)) < 3_000_000:
        return fail("collatz ticket46 phase-wrap edge count unexpectedly small")
    escape46 = audit46.get("escape_coordinate_audit", [])
    if not isinstance(escape46, list) or len(escape46) < 3:
        return fail("collatz ticket46 escape-coordinate audit missing")
    escape46_text = " ".join(str(row) for row in escape46)
    if "not_template_local" not in escape46_text or "horizon_dependent_escape_coordinate" not in escape46_text:
        return fail("collatz ticket46 must reject horizon-dependent escape coordinates")
    if "restricted no-go" not in str(audit46.get("proof_boundary", "")) and "restricted no-go" not in str(
        audit46.get("restricted_no_go_statement", "")
    ):
        return fail("collatz ticket46 must state only a restricted no-go result")
    if "No Collatz proof" not in str(audit46.get("proof_boundary", "")):
        return fail("collatz ticket46 proof boundary must block proof overclaim")

    ticket47_path = Path("data/open-problem/ticket47-periodic-state-lasso-lab.json")
    if not ticket47_path.exists():
        return fail("missing ticket47 periodic state lasso artifact")
    ticket47 = read_json(ticket47_path)
    if ticket47.get("schema") != TICKET47_SCHEMA:
        return fail("ticket47 periodic state lasso artifact has unexpected schema")
    if ticket47.get("status") != "periodic_state_lasso_restricted_no_go_open_no_resolution":
        return fail("ticket47 periodic state lasso overstates resolution")
    ticket47_attempts = ticket47.get("attempts", [])
    if not isinstance(ticket47_attempts, list):
        return fail("ticket47 attempts must be a list")
    ticket47_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket47_attempts if isinstance(attempt, dict)}
    missing_ticket47 = EXPECTED_PROBLEMS - set(ticket47_by_id)
    if missing_ticket47:
        return fail("ticket47 attempts missing problems: " + ", ".join(sorted(missing_ticket47)))
    ticket47_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-47-zero-lasso-automaton.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-47-periodic-state-lasso.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-47-margin-lasso-automaton.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-47-gap-lasso-automaton.json"),
    }
    for problem_id, attempt in ticket47_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "bounded_suffix_stateful_routes_refuted_open_problem_open",
        }:
            return fail(f"{problem_id}: ticket47 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket47 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket47 claim boundary is too weak")
        path = ticket47_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket47 per-problem artifact")

    collatz_ticket47 = ticket47_by_id.get("collatz", {})
    collatz47_bounded = collatz_ticket47.get("bounded_result", {})
    if not isinstance(collatz47_bounded, dict):
        return fail("collatz ticket47 bounded result must be an object")
    audit47 = collatz47_bounded.get("periodic_state_lasso_audit", {})
    if not isinstance(audit47, dict):
        return fail("collatz ticket47 periodic state lasso audit missing")
    if int(audit47.get("template_node_count_28", 0)) < 260_000:
        return fail("collatz ticket47 must retain the 28-bit template graph")
    if int(audit47.get("pressure_edge_count_28", 0)) < 700_000:
        return fail("collatz ticket47 must retain the 28-bit pressure edge set")
    cycle47 = audit47.get("cycle_summary", {})
    if not isinstance(cycle47, dict):
        return fail("collatz ticket47 cycle summary missing")
    if int(cycle47.get("cycle_edge_count", 0)) < 2:
        return fail("collatz ticket47 must expose a nontrivial pressure cycle")
    if float(cycle47.get("total_max_delta_debt", 0.0)) <= 0.0:
        return fail("collatz ticket47 lasso must have positive period debt")
    if cycle47.get("has_positive_period_debt") is not True:
        return fail("collatz ticket47 lasso must mark positive period debt")
    if int(audit47.get("tested_memory_automaton_count", 0)) < 5:
        return fail("collatz ticket47 must test bounded suffix-memory automata")
    if int(audit47.get("refuted_memory_automaton_count", 0)) != int(audit47.get("tested_memory_automaton_count", -1)):
        return fail("collatz ticket47 must refute every tested bounded suffix-memory automaton")
    memory47 = audit47.get("memory_automata", [])
    if not isinstance(memory47, list) or len(memory47) < 5:
        return fail("collatz ticket47 memory automata table missing")
    for row in memory47:
        if not isinstance(row, dict):
            return fail("collatz ticket47 memory automata rows must be objects")
        if row.get("periodic_lasso_status") != "refuted_by_periodic_pressure_lasso":
            return fail("collatz ticket47 memory automaton must be lasso-refuted")
        if row.get("returns_to_same_state_after_one_period") is not True:
            return fail("collatz ticket47 memory automaton must return after one lasso period")
    if "bounded suffix-memory" not in str(audit47.get("restricted_no_go_statement", "")):
        return fail("collatz ticket47 must state the bounded suffix-memory no-go boundary")
    if "No Collatz proof" not in str(audit47.get("proof_boundary", "")):
        return fail("collatz ticket47 proof boundary must block proof overclaim")
    if "does not prove that the cycle is a single reachable Collatz orbit" not in str(audit47.get("proof_boundary", "")):
        return fail("collatz ticket47 must preserve reachability boundary")

    ticket48_path = Path("data/open-problem/ticket48-automaton-reachability-lab.json")
    if not ticket48_path.exists():
        return fail("missing ticket48 automaton reachability artifact")
    ticket48 = read_json(ticket48_path)
    if ticket48.get("schema") != TICKET48_SCHEMA:
        return fail("ticket48 automaton reachability artifact has unexpected schema")
    if ticket48.get("status") != "automaton_reachability_split_open_no_resolution":
        return fail("ticket48 automaton reachability overstates resolution")
    ticket48_attempts = ticket48.get("attempts", [])
    if not isinstance(ticket48_attempts, list):
        return fail("ticket48 attempts must be a list")
    ticket48_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket48_attempts if isinstance(attempt, dict)}
    missing_ticket48 = EXPECTED_PROBLEMS - set(ticket48_by_id)
    if missing_ticket48:
        return fail("ticket48 attempts missing problems: " + ", ".join(sorted(missing_ticket48)))
    ticket48_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-48-kernel-period-map.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-48-automaton-reachability.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-48-margin-period-map.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-48-gap-period-map.json"),
    }
    for problem_id, attempt in ticket48_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "finite_state_abstract_no_go_reachability_open",
        }:
            return fail(f"{problem_id}: ticket48 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket48 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket48 claim boundary is too weak")
        path = ticket48_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket48 per-problem artifact")

    collatz_ticket48 = ticket48_by_id.get("collatz", {})
    collatz48_bounded = collatz_ticket48.get("bounded_result", {})
    if not isinstance(collatz48_bounded, dict):
        return fail("collatz ticket48 bounded result must be an object")
    audit48 = collatz48_bounded.get("automaton_reachability_audit", {})
    if not isinstance(audit48, dict):
        return fail("collatz ticket48 automaton reachability audit missing")
    if int(audit48.get("template_node_count_28", 0)) < 260_000:
        return fail("collatz ticket48 must retain the 28-bit template graph")
    if int(audit48.get("pressure_edge_count_28", 0)) < 700_000:
        return fail("collatz ticket48 must retain the 28-bit pressure edge set")
    cycle48 = audit48.get("cycle_summary", {})
    if not isinstance(cycle48, dict):
        return fail("collatz ticket48 cycle summary missing")
    if int(cycle48.get("cycle_edge_count", 0)) != 16:
        return fail("collatz ticket48 must retain the 16-edge pressure lasso")
    if float(cycle48.get("total_max_delta_debt", 0.0)) <= 0.0:
        return fail("collatz ticket48 lasso must retain positive period debt")
    finite48 = audit48.get("finite_state_period_map", {})
    if not isinstance(finite48, dict):
        return fail("collatz ticket48 finite-state period-map audit missing")
    if finite48.get("status") != "abstract_total_finite_state_repairs_refuted_conditional_on_lasso_relation":
        return fail("collatz ticket48 finite-state audit must remain abstract conditional no-go")
    state_rows48 = finite48.get("state_rows", [])
    if not isinstance(state_rows48, list) or len(state_rows48) < 8:
        return fail("collatz ticket48 finite-state table too small")
    for row in state_rows48:
        if not isinstance(row, dict):
            return fail("collatz ticket48 finite-state rows must be objects")
        if row.get("status") != "abstract_lasso_refutes_total_finite_state_descent":
            return fail("collatz ticket48 finite-state row must be lasso-refuted")
        if int(row.get("period_map_cycle_bound", 0)) != int(row.get("finite_state_count", -2)) + 1:
            return fail("collatz ticket48 period-map bound changed")
    reach48 = audit48.get("reachability_probe", {})
    if not isinstance(reach48, dict):
        return fail("collatz ticket48 reachability probe missing")
    if reach48.get("status") != "no_bounded_concrete_positive_pressure_lasso_realization_found":
        return fail("collatz ticket48 bounded reachability result changed")
    if int(reach48.get("tested_start_candidate_count", 0)) != 4:
        return fail("collatz ticket48 must record the four bounded start candidates")
    if int(reach48.get("completed_steps", 0)) != 3:
        return fail("collatz ticket48 must stop at the third concrete lasso step")
    if int(reach48.get("best_partial_depth", 0)) != 2:
        return fail("collatz ticket48 best partial path depth changed")
    start48 = audit48.get("start_candidate_scan", {})
    if not isinstance(start48, dict):
        return fail("collatz ticket48 start candidate scan missing")
    if int(start48.get("total_start_template_matches", 0)) != 4:
        return fail("collatz ticket48 start-template match count changed")
    if start48.get("store_truncated") is not False:
        return fail("collatz ticket48 start candidate scan must not be truncated")
    if "No Collatz proof" not in str(audit48.get("proof_boundary", "")):
        return fail("collatz ticket48 proof boundary must block proof overclaim")
    if "unreachable in the true lift system" not in str(audit48.get("proof_boundary", "")):
        return fail("collatz ticket48 must preserve true reachability boundary")

    ticket49_path = Path("data/open-problem/ticket49-symbolic-preimage-obstruction-lab.json")
    if not ticket49_path.exists():
        return fail("missing ticket49 symbolic preimage obstruction artifact")
    ticket49 = read_json(ticket49_path)
    if ticket49.get("schema") != TICKET49_SCHEMA:
        return fail("ticket49 symbolic preimage obstruction artifact has unexpected schema")
    if ticket49.get("status") != "symbolic_preimage_obstruction_open_no_resolution":
        return fail("ticket49 symbolic preimage obstruction overstates resolution")
    ticket49_attempts = ticket49.get("attempts", [])
    if not isinstance(ticket49_attempts, list):
        return fail("ticket49 attempts must be a list")
    ticket49_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket49_attempts if isinstance(attempt, dict)}
    missing_ticket49 = EXPECTED_PROBLEMS - set(ticket49_by_id)
    if missing_ticket49:
        return fail("ticket49 attempts missing problems: " + ", ".join(sorted(missing_ticket49)))
    ticket49_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-49-zero-kernel-preimage.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-49-symbolic-preimage-obstruction.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-49-residue-margin-preimage.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-49-gap-selector-preimage.json"),
    }
    for problem_id, attempt in ticket49_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "minimal_preimage_obstruction_found_open_problem_open",
        }:
            return fail(f"{problem_id}: ticket49 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket49 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket49 claim boundary is too weak")
        path = ticket49_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket49 per-problem artifact")

    collatz_ticket49 = ticket49_by_id.get("collatz", {})
    collatz49_bounded = collatz_ticket49.get("bounded_result", {})
    if not isinstance(collatz49_bounded, dict):
        return fail("collatz ticket49 bounded result must be an object")
    audit49 = collatz49_bounded.get("symbolic_preimage_obstruction_audit", {})
    if not isinstance(audit49, dict):
        return fail("collatz ticket49 symbolic preimage audit missing")
    forced49 = audit49.get("forced_low_prefix", {})
    if not isinstance(forced49, dict):
        return fail("collatz ticket49 forced-low prefix audit missing")
    if int(forced49.get("best_partial_depth", 0)) != 2:
        return fail("collatz ticket49 must preserve the two-step concrete partial path")
    starts49 = forced49.get("start_candidates", [])
    if not isinstance(starts49, list) or starts49 != [26471, 28007, 34919, 48743]:
        return fail("collatz ticket49 start candidates changed")
    rows49 = forced49.get("rows", [])
    if not isinstance(rows49, list) or len(rows49) != 3:
        return fail("collatz ticket49 forced-low rows must expose three prefix steps")
    expected_survivors49 = [2, 1, 0]
    for row, expected_survivors in zip(rows49, expected_survivors49):
        if int(row.get("surviving_states", -1)) != expected_survivors:
            return fail("collatz ticket49 survivor sequence changed")
        if "next_valuation" not in str(row.get("mismatch_counts", {})):
            return fail("collatz ticket49 must classify failures by next_valuation")
    minimal49 = audit49.get("minimal_obstruction", {})
    if not isinstance(minimal49, dict):
        return fail("collatz ticket49 minimal obstruction missing")
    if int(minimal49.get("dead_step", 0)) != 3:
        return fail("collatz ticket49 dead step changed")
    if minimal49.get("obstruction_coordinate") != "next_valuation":
        return fail("collatz ticket49 obstruction coordinate must be next_valuation")
    if "No Collatz proof" not in str(audit49.get("proof_boundary", "")):
        return fail("collatz ticket49 proof boundary must block proof overclaim")
    if "does not prove the same next_valuation obstruction for every future phase-compatible modulus" not in str(
        audit49.get("proof_boundary", "")
    ):
        return fail("collatz ticket49 must preserve all-future phase-compatible boundary")

    ticket50_path = Path("data/open-problem/ticket50-phase-lift-exception-lab.json")
    if not ticket50_path.exists():
        return fail("missing ticket50 phase-lift exception artifact")
    ticket50 = read_json(ticket50_path)
    if ticket50.get("schema") != TICKET50_SCHEMA:
        return fail("ticket50 phase-lift exception artifact has unexpected schema")
    if ticket50.get("status") != "phase_lift_exception_open_no_resolution":
        return fail("ticket50 phase-lift exception overstates resolution")
    ticket50_attempts = ticket50.get("attempts", [])
    if not isinstance(ticket50_attempts, list):
        return fail("ticket50 attempts must be a list")
    ticket50_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket50_attempts if isinstance(attempt, dict)}
    missing_ticket50 = EXPECTED_PROBLEMS - set(ticket50_by_id)
    if missing_ticket50:
        return fail("ticket50 attempts missing problems: " + ", ".join(sorted(missing_ticket50)))
    ticket50_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-50-zero-kernel-exception.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-50-phase-lift-exception.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-50-residue-margin-exception.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-50-gap-selector-exception.json"),
    }
    for problem_id, attempt in ticket50_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "candidate_obstruction_refuted_new_near_lasso_frontier_open",
        }:
            return fail(f"{problem_id}: ticket50 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket50 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket50 claim boundary is too weak")
        path = ticket50_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket50 per-problem artifact")

    collatz_ticket50 = ticket50_by_id.get("collatz", {})
    audit50 = collatz_ticket50.get("bounded_result", {}).get("phase_lift_exception_audit", {})
    if not isinstance(audit50, dict):
        return fail("collatz ticket50 phase-lift exception audit missing")
    scans50 = audit50.get("phase_scans", [])
    if not isinstance(scans50, list) or len(scans50) != 2:
        return fail("collatz ticket50 must expose 16-bit and 32-bit phase scans")
    scans50_by_bits = {int(scan.get("bits", -1)): scan for scan in scans50 if isinstance(scan, dict)}
    scan16 = scans50_by_bits.get(16, {})
    scan32 = scans50_by_bits.get(32, {})
    if int(scan16.get("start_template_match_count", -1)) != 4:
        return fail("collatz ticket50 must reproduce four 16-bit start-template matches")
    if int(scan16.get("four_consecutive_one_exception_count", -1)) != 0:
        return fail("collatz ticket50 16-bit scan must preserve no four-one exception")
    if int(scan16.get("max_lasso_prefix_depth", -1)) != 3:
        return fail("collatz ticket50 16-bit max lasso depth changed")
    if int(scan32.get("start_template_match_count", -1)) != 69092:
        return fail("collatz ticket50 32-bit start-template match count changed")
    if int(scan32.get("four_consecutive_one_exception_count", -1)) != 8684:
        return fail("collatz ticket50 32-bit four-one exception count changed")
    if int(scan32.get("max_lasso_prefix_depth", -1)) != 15:
        return fail("collatz ticket50 32-bit max lasso depth changed")
    if str(audit50.get("ticket49_candidate_theorem_status")) != "refuted_by_32bit_phase_compatible_exception":
        return fail("collatz ticket50 must refute the ticket49 all-phase candidate theorem")
    if "No Collatz proof" not in str(audit50.get("proof_boundary", "")):
        return fail("collatz ticket50 proof boundary must block proof overclaim")
    if "no periodic Collatz orbit" not in str(audit50.get("proof_boundary", "")):
        return fail("collatz ticket50 must preserve no-counterexample boundary")

    ticket51_path = Path("data/open-problem/ticket51-phase15-terminal-lift-lab.json")
    if not ticket51_path.exists():
        return fail("missing ticket51 phase15 terminal lift artifact")
    ticket51 = read_json(ticket51_path)
    if ticket51.get("schema") != TICKET51_SCHEMA:
        return fail("ticket51 phase15 terminal lift artifact has unexpected schema")
    if ticket51.get("status") != "phase15_terminal_lift_closed_open_no_resolution":
        return fail("ticket51 phase15 terminal lift overstates resolution")
    ticket51_attempts = ticket51.get("attempts", [])
    if not isinstance(ticket51_attempts, list):
        return fail("ticket51 attempts must be a list")
    ticket51_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket51_attempts if isinstance(attempt, dict)}
    missing_ticket51 = EXPECTED_PROBLEMS - set(ticket51_by_id)
    if missing_ticket51:
        return fail("ticket51 attempts missing problems: " + ", ".join(sorted(missing_ticket51)))
    ticket51_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-51-terminal-witness-closure.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-51-phase15-terminal-lift.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-51-terminal-witness-closure.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-51-terminal-witness-closure.json"),
    }
    for problem_id, attempt in ticket51_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "known_depth15_roots_terminally_closed_open_problem_open",
        }:
            return fail(f"{problem_id}: ticket51 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket51 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket51 claim boundary is too weak")
        path = ticket51_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket51 per-problem artifact")

    collatz_ticket51 = ticket51_by_id.get("collatz", {})
    audit51 = collatz_ticket51.get("bounded_result", {}).get("phase15_terminal_lift_audit", {})
    if not isinstance(audit51, dict):
        return fail("collatz ticket51 terminal lift audit missing")
    if audit51.get("source_roots") != [1471663463, 3206130791]:
        return fail("collatz ticket51 source roots changed")
    if int(audit51.get("terminal_step", -1)) != 15:
        return fail("collatz ticket51 terminal step changed")
    if int(audit51.get("final_surviving_states", -1)) != 0:
        return fail("collatz ticket51 must close the two-root terminal lift tree")
    if int(audit51.get("full_lasso_completion_count", -1)) != 0:
        return fail("collatz ticket51 must not report a full lasso completion")
    if int(audit51.get("best_template_depth", -1)) != 15:
        return fail("collatz ticket51 best template depth changed")
    terminal51 = audit51.get("terminal_mismatch_counts", {})
    if terminal51.get("all_lift_descent") != 2 or terminal51.get("tail_word+next_valuation") != 2:
        return fail("collatz ticket51 terminal mismatch classification changed")
    if "No Collatz proof" not in str(audit51.get("proof_boundary", "")):
        return fail("collatz ticket51 proof boundary must block proof overclaim")
    if "does not exclude new 48-bit roots outside this ancestry" not in str(audit51.get("proof_boundary", "")):
        return fail("collatz ticket51 must preserve outside-ancestry boundary")

    ticket52_path = Path("data/open-problem/ticket52-frontier-budget-lab.json")
    if not ticket52_path.exists():
        return fail("missing ticket52 frontier budget artifact")
    ticket52 = read_json(ticket52_path)
    if ticket52.get("schema") != TICKET52_SCHEMA:
        return fail("ticket52 frontier budget artifact has unexpected schema")
    if ticket52.get("status") != "frontier_budget_open_no_resolution":
        return fail("ticket52 frontier budget overstates resolution")
    ticket52_attempts = ticket52.get("attempts", [])
    if not isinstance(ticket52_attempts, list):
        return fail("ticket52 attempts must be a list")
    ticket52_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket52_attempts if isinstance(attempt, dict)}
    missing_ticket52 = EXPECTED_PROBLEMS - set(ticket52_by_id)
    if missing_ticket52:
        return fail("ticket52 attempts missing problems: " + ", ".join(sorted(missing_ticket52)))
    ticket52_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-52-frontier-budget-contract.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-52-frontier-budget-sample-closure.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-52-frontier-budget-contract.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-52-frontier-budget-contract.json"),
    }
    for problem_id, attempt in ticket52_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "new_48bit_near_lasso_witness_terminally_closed_open_problem_open",
        }:
            return fail(f"{problem_id}: ticket52 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket52 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket52 claim boundary is too weak")
        path = ticket52_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket52 per-problem artifact")

    collatz_ticket52 = ticket52_by_id.get("collatz", {})
    audit52 = collatz_ticket52.get("bounded_result", {}).get("frontier_budget_audit", {})
    if not isinstance(audit52, dict):
        return fail("collatz ticket52 frontier budget audit missing")
    counts52 = audit52.get("exact_open_word_counts", [])
    if not isinstance(counts52, list):
        return fail("collatz ticket52 exact word counts missing")
    counts52_by_bits = {int(row.get("bits", -1)): int(row.get("open_valuation_words_with_tail", -1)) for row in counts52 if isinstance(row, dict)}
    if counts52_by_bits.get(48) != 83401400116:
        return fail("collatz ticket52 48-bit frontier count changed")
    if counts52_by_bits.get(64) != 2216134944775156:
        return fail("collatz ticket52 64-bit frontier count changed")
    sample52 = audit52.get("sampled_48bit_frontier", {})
    if not isinstance(sample52, dict):
        return fail("collatz ticket52 sampled frontier missing")
    if int(sample52.get("sample_count", -1)) != 200000 or int(sample52.get("sample_seed", -1)) != 20260709:
        return fail("collatz ticket52 sample contract changed")
    stats52 = sample52.get("statistics", {})
    if not isinstance(stats52, dict):
        return fail("collatz ticket52 sample statistics missing")
    if int(stats52.get("verified_open_word", -1)) != 100026:
        return fail("collatz ticket52 verified sample count changed")
    if int(stats52.get("start_template_match", -1)) != 3184:
        return fail("collatz ticket52 start-template sample count changed")
    depth52 = sample52.get("lasso_prefix_depth_counts", {})
    if not isinstance(depth52, dict) or int(depth52.get("15", -1)) != 1:
        return fail("collatz ticket52 must preserve the sampled depth-15 witness")
    if int(sample52.get("max_sampled_lasso_prefix_depth", -1)) != 15:
        return fail("collatz ticket52 max sampled depth changed")
    roots52 = sample52.get("new_depth15_roots", [])
    if not isinstance(roots52, list) or len(roots52) != 1:
        return fail("collatz ticket52 must expose exactly one sampled depth-15 root")
    root52 = roots52[0]
    if int(root52.get("residue", -1)) != 171308122831719:
        return fail("collatz ticket52 sampled depth-15 root changed")
    projection52 = root52.get("projection32", {})
    if not isinstance(projection52, dict):
        return fail("collatz ticket52 projection audit missing")
    if int(projection52.get("residue", -1)) != 3352230759:
        return fail("collatz ticket52 projection residue changed")
    if projection52.get("template") != "[0,[1,2,1,1],103,2]":
        return fail("collatz ticket52 projection template must show non-ancestry root")
    terminal52 = sample52.get("terminal_lift_audit", {})
    if not isinstance(terminal52, dict):
        return fail("collatz ticket52 terminal lift audit missing")
    if int(terminal52.get("base_bits", -1)) != 48:
        return fail("collatz ticket52 terminal audit must use base bits 48")
    if int(terminal52.get("terminal_step", -1)) != 15:
        return fail("collatz ticket52 terminal step changed")
    if int(terminal52.get("final_surviving_states", -1)) != 0:
        return fail("collatz ticket52 terminal audit must close sampled witness")
    if int(terminal52.get("full_lasso_completion_count", -1)) != 0:
        return fail("collatz ticket52 must not report a full lasso completion")
    terminal_mismatch52 = terminal52.get("terminal_mismatch_counts", {})
    if not isinstance(terminal_mismatch52, dict) or terminal_mismatch52.get("tail_word+next_valuation") != 2:
        return fail("collatz ticket52 terminal mismatch classification changed")
    if "No Collatz proof" not in str(audit52.get("proof_boundary", "")):
        return fail("collatz ticket52 proof boundary must block proof overclaim")
    if "not exhaustive" not in str(audit52.get("proof_boundary", "")):
        return fail("collatz ticket52 must preserve sampler boundary")

    ticket53_path = Path("data/open-problem/ticket53-symbolic-terminal-theorem-lab.json")
    if not ticket53_path.exists():
        return fail("missing ticket53 symbolic terminal theorem artifact")
    ticket53 = read_json(ticket53_path)
    if ticket53.get("schema") != TICKET53_SCHEMA:
        return fail("ticket53 symbolic terminal theorem artifact has unexpected schema")
    if ticket53.get("status") != "symbolic_terminal_theorem_open_no_resolution":
        return fail("ticket53 symbolic terminal theorem overstates resolution")
    ticket53_attempts = ticket53.get("attempts", [])
    if not isinstance(ticket53_attempts, list):
        return fail("ticket53 attempts must be a list")
    ticket53_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket53_attempts if isinstance(attempt, dict)}
    missing_ticket53 = EXPECTED_PROBLEMS - set(ticket53_by_id)
    if missing_ticket53:
        return fail("ticket53 attempts missing problems: " + ", ".join(sorted(missing_ticket53)))
    ticket53_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-53-terminal-no-go-theorem.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-53-symbolic-terminal-theorem.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-53-terminal-no-go-theorem.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-53-terminal-no-go-theorem.json"),
    }
    for problem_id, attempt in ticket53_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "extracted_lasso_family_terminally_refuted_open_problem_open",
        }:
            return fail(f"{problem_id}: ticket53 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket53 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket53 claim boundary is too weak")
        path = ticket53_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket53 per-problem artifact")

    collatz_ticket53 = ticket53_by_id.get("collatz", {})
    audit53 = collatz_ticket53.get("bounded_result", {}).get("symbolic_terminal_theorem_audit", {})
    if not isinstance(audit53, dict):
        return fail("collatz ticket53 symbolic terminal theorem audit missing")
    if audit53.get("theorem_name") != "Phase15TerminalMismatchForExtractedLasso":
        return fail("collatz ticket53 theorem name changed")
    if not audit53.get("all_checked_roots_satisfy_parent_premise"):
        return fail("collatz ticket53 parent premise must hold for checked roots")
    if int(audit53.get("terminal_target_match_count", -1)) != 0:
        return fail("collatz ticket53 must refute terminal target for checked roots")
    roots53 = audit53.get("machine_checked_roots", [])
    if not isinstance(roots53, list) or len(roots53) != 3:
        return fail("collatz ticket53 must check three known near-lasso roots")
    expected_roots53 = {(32, 1471663463), (32, 3206130791), (48, 171308122831719)}
    observed_roots53 = {(int(row.get("base_bits", -1)), int(row.get("residue", -1))) for row in roots53 if isinstance(row, dict)}
    if observed_roots53 != expected_roots53:
        return fail("collatz ticket53 checked root set changed")
    for row in roots53:
        if row.get("parent_template") != "[14,[1,1,1,1],103,10]":
            return fail("collatz ticket53 parent template changed")
        if int(row.get("low_next_valuation_before_terminal", -1)) != 10:
            return fail("collatz ticket53 low branch valuation lemma changed")
        if int(row.get("high_next_valuation_before_terminal", -1)) != 9:
            return fail("collatz ticket53 high branch valuation lemma changed")
        if row.get("terminal_target_matched"):
            return fail("collatz ticket53 terminal target unexpectedly matched")
    if "No Collatz proof" not in str(audit53.get("proof_boundary", "")):
        return fail("collatz ticket53 proof boundary must block proof overclaim")
    if "does not prove global Collatz descent" not in str(audit53.get("terminal_theorem_scope", "")):
        return fail("collatz ticket53 must preserve local theorem scope")

    ticket54_path = Path("data/open-problem/ticket54-new-template-family-lab.json")
    if not ticket54_path.exists():
        return fail("missing ticket54 new template family artifact")
    ticket54 = read_json(ticket54_path)
    if ticket54.get("schema") != TICKET54_SCHEMA:
        return fail("ticket54 new template family artifact has unexpected schema")
    if ticket54.get("status") != "new_template_family_extracted_open_no_resolution":
        return fail("ticket54 new template family artifact overstates resolution")
    ticket54_attempts = ticket54.get("attempts", [])
    if not isinstance(ticket54_attempts, list):
        return fail("ticket54 attempts must be a list")
    ticket54_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket54_attempts if isinstance(attempt, dict)}
    missing_ticket54 = EXPECTED_PROBLEMS - set(ticket54_by_id)
    if missing_ticket54:
        return fail("ticket54 attempts missing problems: " + ", ".join(sorted(missing_ticket54)))
    ticket54_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-54-post-nogo-family-triage.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-54-new-template-family.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-54-post-nogo-family-triage.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-54-post-nogo-family-triage.json"),
    }
    for problem_id, attempt in ticket54_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "post_terminal_family_pruned_new_gate_family_open_problem_open",
        }:
            return fail(f"{problem_id}: ticket54 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket54 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket54 claim boundary is too weak")
        path = ticket54_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket54 per-problem artifact")

    collatz_ticket54 = ticket54_by_id.get("collatz", {})
    audit54 = collatz_ticket54.get("bounded_result", {}).get("new_template_family_audit", {})
    if not isinstance(audit54, dict):
        return fail("collatz ticket54 new template family audit missing")
    discarded54 = audit54.get("discarded_family", {})
    if not isinstance(discarded54, dict) or discarded54.get("source_theorem") != "Phase15TerminalMismatchForExtractedLasso":
        return fail("collatz ticket54 must inherit the ticket53 discarded theorem")
    if int(discarded54.get("terminal_target_match_count", -1)) != 0:
        return fail("collatz ticket54 must preserve ticket53 terminal mismatch")
    exact54 = audit54.get("exact_32bit_post_terminal_reaudit", {})
    if not isinstance(exact54, dict):
        return fail("collatz ticket54 exact 32-bit reaudit missing")
    if int(exact54.get("exact_start_template_matches", -1)) != 69092:
        return fail("collatz ticket54 exact 32-bit start count changed")
    if int(exact54.get("discarded_depth15_family_count", -1)) != 2:
        return fail("collatz ticket54 must discard the two exact 32-bit depth-15 roots")
    if exact54.get("discarded_depth15_family_roots") != [1471663463, 3206130791]:
        return fail("collatz ticket54 discarded 32-bit root set changed")
    depth54 = exact54.get("depth_counts", {})
    if not isinstance(depth54, dict) or int(depth54.get("15", -1)) != 2 or int(depth54.get("5", -1)) != 4372:
        return fail("collatz ticket54 exact depth counts changed")
    if int(exact54.get("remaining_after_ticket53_discard", -1)) != 69090:
        return fail("collatz ticket54 remaining exact frontier count changed")
    if int(exact54.get("max_remaining_depth_after_ticket53_discard", -1)) != 5:
        return fail("collatz ticket54 post-discard max depth must be 5")
    if int(exact54.get("phase5_gate_count", -1)) != 4372:
        return fail("collatz ticket54 phase5 gate count changed")
    if int(exact54.get("phase5_exact_next10_failure_count", -1)) != 0:
        return fail("collatz ticket54 phase5 failures must not include next valuation 10")
    phase5_counts54 = exact54.get("phase5_next_valuation_counts", {})
    if not isinstance(phase5_counts54, dict) or int(phase5_counts54.get("1", -1)) != 2160:
        return fail("collatz ticket54 phase5 next valuation distribution changed")
    top_phase5_54 = exact54.get("top_phase5_gate_templates", [])
    if not isinstance(top_phase5_54, list) or not top_phase5_54:
        return fail("collatz ticket54 phase5 templates missing")
    if top_phase5_54[0].get("observed_template") != "[5,[1,1,1,1],103,1]":
        return fail("collatz ticket54 top phase5 template changed")
    sample54 = audit54.get("sampled_48bit_post_terminal_summary", {})
    if not isinstance(sample54, dict):
        return fail("collatz ticket54 sampled 48-bit summary missing")
    if int(sample54.get("sample_count", -1)) != 200000 or int(sample54.get("sample_seed", -1)) != 20260709:
        return fail("collatz ticket54 sample contract changed")
    if int(sample54.get("discarded_depth15_sample_count", -1)) != 1:
        return fail("collatz ticket54 must discard one sampled depth-15 root")
    if int(sample54.get("max_remaining_depth_after_ticket53_discard", -1)) != 5:
        return fail("collatz ticket54 sampled post-discard max depth must be 5")
    if int(sample54.get("phase5_gate_sample_count", -1)) != 175:
        return fail("collatz ticket54 sampled phase5 gate count changed")
    candidate54 = audit54.get("new_candidate_family", {})
    if not isinstance(candidate54, dict) or candidate54.get("name") != "Phase5ValuationGate":
        return fail("collatz ticket54 must extract Phase5ValuationGate")
    if "No Collatz proof" not in str(audit54.get("proof_boundary", "")):
        return fail("collatz ticket54 proof boundary must block proof overclaim")

    ticket55_path = Path("data/open-problem/ticket55-phase5-valuation-gate-lab.json")
    if not ticket55_path.exists():
        return fail("missing ticket55 phase5 valuation gate artifact")
    ticket55 = read_json(ticket55_path)
    if ticket55.get("schema") != TICKET55_SCHEMA:
        return fail("ticket55 phase5 valuation gate artifact has unexpected schema")
    if ticket55.get("status") != "phase5_gate_tunnel_open_no_resolution":
        return fail("ticket55 phase5 valuation gate artifact overstates resolution")
    ticket55_attempts = ticket55.get("attempts", [])
    if not isinstance(ticket55_attempts, list):
        return fail("ticket55 attempts must be a list")
    ticket55_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket55_attempts if isinstance(attempt, dict)}
    missing_ticket55 = EXPECTED_PROBLEMS - set(ticket55_by_id)
    if missing_ticket55:
        return fail("ticket55 attempts missing problems: " + ", ".join(sorted(missing_ticket55)))
    ticket55_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-55-gate-terminal-tunnel.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-55-phase5-gate-tunnel.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-55-gate-terminal-tunnel.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-55-gate-terminal-tunnel.json"),
    }
    for problem_id, attempt in ticket55_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "local_phase5_gate_tunnel_closed_open_problem_open",
        }:
            return fail(f"{problem_id}: ticket55 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket55 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket55 claim boundary is too weak")
        path = ticket55_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket55 per-problem artifact")

    collatz_ticket55 = ticket55_by_id.get("collatz", {})
    audit55 = collatz_ticket55.get("bounded_result", {}).get("phase5_gate_tunnel_audit", {})
    if not isinstance(audit55, dict):
        return fail("collatz ticket55 phase5 gate tunnel audit missing")
    if audit55.get("theorem_name") != "Phase5GateToTerminalTunnel":
        return fail("collatz ticket55 theorem name changed")
    if int(audit55.get("gate_match_count", -1)) != 3:
        return fail("collatz ticket55 gate match count changed")
    if int(audit55.get("tunnel_match_count", -1)) != 3:
        return fail("collatz ticket55 tunnel match count changed")
    if int(audit55.get("same_pending_certificate_count", -1)) != 3:
        return fail("collatz ticket55 pending-certificate count changed")
    if int(audit55.get("terminal_target_match_count", -1)) != 0:
        return fail("collatz ticket55 terminal target unexpectedly matched")
    if not audit55.get("all_gate_roots_tunnel_to_terminal_no_go"):
        return fail("collatz ticket55 must close every known gate crosser locally")
    roots55 = audit55.get("machine_checked_roots", [])
    if not isinstance(roots55, list) or len(roots55) != 3:
        return fail("collatz ticket55 must check three known gate-crossing roots")
    expected_roots55 = {(32, 1471663463), (32, 3206130791), (48, 171308122831719)}
    observed_roots55 = {(int(row.get("base_bits", -1)), int(row.get("residue", -1))) for row in roots55 if isinstance(row, dict)}
    if observed_roots55 != expected_roots55:
        return fail("collatz ticket55 checked root set changed")
    for row in roots55:
        if not row.get("gate_matches"):
            return fail("collatz ticket55 gate crosser no longer matches gate")
        if not row.get("gate_consumed_equals_gate_bits"):
            return fail("collatz ticket55 gate consumed-bits premise changed")
        if not row.get("gate_next_reaches_terminal_bits"):
            return fail("collatz ticket55 gate next valuation no longer reaches terminal")
        if not row.get("tunnel_all_offsets_match"):
            return fail("collatz ticket55 tunnel match changed")
        if not row.get("tunnel_all_offsets_same_pending_certificate"):
            return fail("collatz ticket55 pending tunnel changed")
        if row.get("terminal_target_matched"):
            return fail("collatz ticket55 terminal target unexpectedly matched")
    bounded32_55 = audit55.get("bounded_32bit_closure", {})
    if not isinstance(bounded32_55, dict):
        return fail("collatz ticket55 bounded 32-bit closure missing")
    if int(bounded32_55.get("exact_start_template_matches", -1)) != 69092:
        return fail("collatz ticket55 exact 32-bit start count changed")
    if int(bounded32_55.get("failed_before_or_at_phase5", -1)) != 69090:
        return fail("collatz ticket55 pre-gate/gate failure count changed")
    if int(bounded32_55.get("gate_crossers", -1)) != 2:
        return fail("collatz ticket55 exact gate crosser count changed")
    if int(bounded32_55.get("gate_crossers_terminally_closed", -1)) != 2:
        return fail("collatz ticket55 exact gate crossers must close terminally")
    sample55 = audit55.get("sampled_48bit_closure", {})
    if not isinstance(sample55, dict):
        return fail("collatz ticket55 sampled 48-bit closure missing")
    if int(sample55.get("sample_count", -1)) != 200000:
        return fail("collatz ticket55 sample count changed")
    if int(sample55.get("post_discard_max_depth", -1)) != 5:
        return fail("collatz ticket55 sampled post-discard depth changed")
    if int(sample55.get("phase5_gate_sample_count", -1)) != 175:
        return fail("collatz ticket55 sampled phase5 gate count changed")
    if int(sample55.get("gate_crossers_terminally_closed", -1)) != 1:
        return fail("collatz ticket55 sampled gate crosser must close terminally")
    if "No Collatz proof" not in str(audit55.get("proof_boundary", "")):
        return fail("collatz ticket55 proof boundary must block proof overclaim")

    ticket56_path = Path("data/open-problem/ticket56-pre-gate-projection-escape-lab.json")
    if not ticket56_path.exists():
        return fail("missing ticket56 pre-gate projection escape artifact")
    ticket56 = read_json(ticket56_path)
    if ticket56.get("schema") != TICKET56_SCHEMA:
        return fail("ticket56 pre-gate projection escape artifact has unexpected schema")
    if ticket56.get("status") != "pre_gate_projection_escape_open_no_resolution":
        return fail("ticket56 pre-gate projection escape artifact overstates resolution")
    ticket56_attempts = ticket56.get("attempts", [])
    if not isinstance(ticket56_attempts, list):
        return fail("ticket56 attempts must be a list")
    ticket56_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket56_attempts if isinstance(attempt, dict)}
    missing_ticket56 = EXPECTED_PROBLEMS - set(ticket56_by_id)
    if missing_ticket56:
        return fail("ticket56 attempts missing problems: " + ", ".join(sorted(missing_ticket56)))
    ticket56_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-56-projection-escape-frontier.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-56-pre-gate-projection-escape.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-56-lift-escape-frontier.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-56-lift-escape-frontier.json"),
    }
    for problem_id, attempt in ticket56_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "exact32_lasso_route_closed_projection_escape_blocks_globalization",
        }:
            return fail(f"{problem_id}: ticket56 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket56 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket56 claim boundary is too weak")
        path = ticket56_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket56 per-problem artifact")

    collatz_ticket56 = ticket56_by_id.get("collatz", {})
    audit56 = collatz_ticket56.get("bounded_result", {}).get("pre_gate_projection_escape_audit", {})
    if not isinstance(audit56, dict):
        return fail("collatz ticket56 pre-gate projection escape audit missing")
    if audit56.get("local_theorem_name") != "Exact32StartTemplateLassoPartition":
        return fail("collatz ticket56 local theorem name changed")
    exact32_56 = audit56.get("exact32_pre_gate_partition", {})
    if not isinstance(exact32_56, dict):
        return fail("collatz ticket56 exact32 partition missing")
    if int(exact32_56.get("exact_start_template_matches", -1)) != 69092:
        return fail("collatz ticket56 exact32 start count changed")
    if int(exact32_56.get("pre_gate_failure_count", -1)) != 69090:
        return fail("collatz ticket56 pre-gate failure count changed")
    expected_offsets56 = {"1": 34458, "2": 17301, "3": 8649, "4": 4310, "5": 4372}
    observed_offsets56 = {
        str(key): int(value)
        for key, value in exact32_56.get("pre_gate_failure_offsets", {}).items()
    }
    if observed_offsets56 != expected_offsets56:
        return fail("collatz ticket56 pre-gate offset partition changed")
    if not exact32_56.get("all_pre_gate_failures_are_offsets_1_to_5"):
        return fail("collatz ticket56 pre-gate offsets must be exactly 1..5")
    if not exact32_56.get("all_pre_gate_failures_are_next_valuation_mismatch"):
        return fail("collatz ticket56 failures must all be next-valuation mismatches")
    if int(exact32_56.get("phase5_observed_next10_count", -1)) != 0:
        return fail("collatz ticket56 phase5 next valuation 10 unexpectedly observed")
    if int(exact32_56.get("phase5_gate_crosser_count", -1)) != 2:
        return fail("collatz ticket56 gate crosser count changed")
    if [int(value) for value in exact32_56.get("phase5_gate_crossers", [])] != [1471663463, 3206130791]:
        return fail("collatz ticket56 gate crosser roots changed")
    if int(exact32_56.get("partition_sum", -1)) != 69092:
        return fail("collatz ticket56 exact32 partition sum changed")
    if not exact32_56.get("partition_is_complete_for_exact32_start_template"):
        return fail("collatz ticket56 exact32 partition must be complete")
    projection56 = audit56.get("projection_escape_audit", {})
    if not isinstance(projection56, dict):
        return fail("collatz ticket56 projection escape audit missing")
    if int(projection56.get("sample_count", -1)) != 200000:
        return fail("collatz ticket56 sample count changed")
    if int(projection56.get("sample_start_template_matches", -1)) != 3184:
        return fail("collatz ticket56 48-bit sample start count changed")
    if projection56.get("simple_projection_closure_status") != "refuted_by_sampled_48bit_depth15_witness":
        return fail("collatz ticket56 must refute simple projection closure")
    escapes56 = projection56.get("escape_witnesses", [])
    if not isinstance(escapes56, list) or len(escapes56) != 1:
        return fail("collatz ticket56 must record one projection escape witness")
    escape56 = escapes56[0]
    if int(escape56.get("residue", -1)) != 171308122831719:
        return fail("collatz ticket56 escape witness residue changed")
    if int(escape56.get("lasso_prefix_depth", -1)) != 15:
        return fail("collatz ticket56 escape witness depth changed")
    reused55 = projection56.get("ticket55_gate_tunnel_reused", {})
    if reused55.get("theorem_name") != "Phase5GateToTerminalTunnel":
        return fail("collatz ticket56 must reuse ticket55 gate tunnel")
    if int(reused55.get("terminal_target_match_count", -1)) != 0:
        return fail("collatz ticket56 reused ticket55 tunnel must have no terminal target match")
    if "No Collatz proof" not in str(audit56.get("proof_boundary", "")):
        return fail("collatz ticket56 proof boundary must block proof overclaim")

    ticket57_path = Path("data/open-problem/ticket57-parametric-template-automaton-lab.json")
    if not ticket57_path.exists():
        return fail("missing ticket57 parametric template automaton artifact")
    ticket57 = read_json(ticket57_path)
    if ticket57.get("schema") != TICKET57_SCHEMA:
        return fail("ticket57 parametric template automaton artifact has unexpected schema")
    if ticket57.get("status") != "parametric_boundary_state_open_no_resolution":
        return fail("ticket57 parametric template automaton artifact overstates resolution")
    ticket57_attempts = ticket57.get("attempts", [])
    if not isinstance(ticket57_attempts, list):
        return fail("ticket57 attempts must be a list")
    ticket57_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket57_attempts if isinstance(attempt, dict)}
    missing_ticket57 = EXPECTED_PROBLEMS - set(ticket57_by_id)
    if missing_ticket57:
        return fail("ticket57 attempts missing problems: " + ", ".join(sorted(missing_ticket57)))
    ticket57_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-57-boundary-state-model.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-57-parametric-template-automaton.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-57-boundary-margin-model.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-57-boundary-sieve-model.json"),
    }
    for problem_id, attempt in ticket57_by_id.items():
        if attempt.get("status") not in {"proof_pressure_open", "parametric_state_obstruction_open_no_resolution"}:
            return fail(f"{problem_id}: ticket57 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket57 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket57 claim boundary is too weak")
        path = ticket57_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket57 per-problem artifact")

    collatz_ticket57 = ticket57_by_id.get("collatz", {})
    audit57 = collatz_ticket57.get("bounded_result", {}).get("parametric_template_automaton_audit", {})
    if not isinstance(audit57, dict):
        return fail("collatz ticket57 parametric template automaton audit missing")
    if audit57.get("theorem_name") != "AffineBoundaryTemplateStateOrEscapeCycle":
        return fail("collatz ticket57 theorem name changed")
    summary57 = audit57.get("exact32_outcome_summary", {})
    if int(summary57.get("total", -1)) != 69092:
        return fail("collatz ticket57 exact32 total changed")
    expected_outcomes57 = {
        "fail_offset_1": 34458,
        "fail_offset_2": 17301,
        "fail_offset_3": 8649,
        "fail_offset_4": 4310,
        "fail_offset_5": 4372,
        "phase5_gate_terminal_tunnel": 2,
    }
    observed_outcomes57 = {
        str(key): int(value)
        for key, value in summary57.get("coarse_outcome_counts", {}).items()
    }
    if observed_outcomes57 != expected_outcomes57:
        return fail("collatz ticket57 exact32 outcome partition changed")
    determinism57 = audit57.get("exact32_state_determinism", {})
    if int(determinism57.get("first_deterministic_low_bits", -1)) != 28:
        return fail("collatz ticket57 first deterministic boundary width changed")
    ladder57 = determinism57.get("ladder", [])
    if not isinstance(ladder57, list) or len(ladder57) < 10:
        return fail("collatz ticket57 determinism ladder too small")
    template_only57 = next((row for row in ladder57 if row.get("abstraction") == "template_only"), None)
    if not isinstance(template_only57, dict) or int(template_only57.get("max_outcomes_per_state", -1)) != 6:
        return fail("collatz ticket57 template-only abstraction must remain nondeterministic")
    low26_57 = next(
        (row for row in ladder57 if row.get("abstraction") == "template_plus_prefix_length_residue_mod_2^26"),
        None,
    )
    if not isinstance(low26_57, dict) or int(low26_57.get("collision_group_count", -1)) != 92:
        return fail("collatz ticket57 26-bit boundary collision count changed")
    low28_57 = next(
        (row for row in ladder57 if row.get("abstraction") == "template_plus_prefix_length_residue_mod_2^28"),
        None,
    )
    if not isinstance(low28_57, dict) or int(low28_57.get("collision_group_count", -1)) != 0:
        return fail("collatz ticket57 28-bit boundary should be deterministic for exact32")
    projection57 = audit57.get("projection_escape_carry_forward", {})
    if projection57.get("simple_projection_closure_status") != "refuted_by_sampled_48bit_depth15_witness":
        return fail("collatz ticket57 must carry forward projection escape")
    if int(projection57.get("escape_witness_count", -1)) != 1:
        return fail("collatz ticket57 escape witness count changed")
    replay57 = audit57.get("known_root_replay_audit", {})
    if int(replay57.get("known_root_count", -1)) != 3:
        return fail("collatz ticket57 known root replay count changed")
    if int(replay57.get("max_replayed_prefix_depth", -1)) != 15:
        return fail("collatz ticket57 max replayed prefix depth changed")
    if int(replay57.get("full_lasso_period_replay_count", -1)) != 0:
        return fail("collatz ticket57 must not find a full lasso replay")
    if replay57.get("cycle_status") != "no_known_root_replays_full_lasso_period":
        return fail("collatz ticket57 cycle status changed")
    if "No Collatz proof" not in str(audit57.get("proof_boundary", "")):
        return fail("collatz ticket57 proof boundary must block proof overclaim")

    ticket58_path = Path("data/open-problem/ticket58-affine-boundary-lift-lab.json")
    if not ticket58_path.exists():
        return fail("missing ticket58 affine boundary lift artifact")
    ticket58 = read_json(ticket58_path)
    if ticket58.get("schema") != TICKET58_SCHEMA:
        return fail("ticket58 affine boundary lift artifact has unexpected schema")
    if ticket58.get("status") != "affine_boundary_lift_open_no_resolution":
        return fail("ticket58 affine boundary lift artifact overstates resolution")
    ticket58_attempts = ticket58.get("attempts", [])
    if not isinstance(ticket58_attempts, list):
        return fail("ticket58 attempts must be a list")
    ticket58_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket58_attempts if isinstance(attempt, dict)}
    missing_ticket58 = EXPECTED_PROBLEMS - set(ticket58_by_id)
    if missing_ticket58:
        return fail("ticket58 attempts missing problems: " + ", ".join(sorted(missing_ticket58)))
    ticket58_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-58-zero-kernel-lift-stability.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-58-affine-boundary-lift.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-58-margin-lift-stability.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-58-sieve-boundary-lift.json"),
    }
    for problem_id, attempt in ticket58_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "sampled_affine_boundary_lift_obstruction_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket58 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket58 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket58 claim boundary is too weak")
        path = ticket58_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket58 per-problem artifact")

    collatz_ticket58 = ticket58_by_id.get("collatz", {})
    audit58 = collatz_ticket58.get("bounded_result", {}).get("affine_boundary_lift_audit", {})
    if not isinstance(audit58, dict):
        return fail("collatz ticket58 affine boundary lift audit missing")
    if audit58.get("theorem_name") != "AffineBoundaryLiftStabilityOrFullPeriodEscape":
        return fail("collatz ticket58 theorem name changed")
    exact58 = audit58.get("exact32_boundary", {})
    if int(exact58.get("low_bits", -1)) != 28:
        return fail("collatz ticket58 boundary width changed")
    if int(exact58.get("row_count", -1)) != 69092:
        return fail("collatz ticket58 exact32 row count changed")
    if int(exact58.get("boundary_state_count", -1)) != 69092:
        return fail("collatz ticket58 boundary state count changed")
    if int(exact58.get("collision_count", -1)) != 0:
        return fail("collatz ticket58 exact32 boundary must remain deterministic")
    sample58 = audit58.get("sampled_48bit_lift_stability", {})
    if int(sample58.get("sample_count", -1)) != 200000:
        return fail("collatz ticket58 sample count changed")
    stats58 = sample58.get("statistics", {})
    expected_stats58 = {
        "verified_open_word": 100027,
        "unverified_canonical_word": 99973,
        "start_template_match": 3184,
        "projection_escape": 3086,
        "projection_target": 98,
        "boundary_prediction_match": 28,
        "boundary_prediction_mismatch": 70,
    }
    observed_stats58 = {str(key): int(stats58.get(key, -1)) for key in expected_stats58}
    if observed_stats58 != expected_stats58:
        return fail("collatz ticket58 replayed sample statistics changed")
    expected_depth58 = {"1": 1650, "2": 763, "3": 406, "4": 189, "5": 175, "15": 1}
    observed_depth58 = {
        str(key): int(value)
        for key, value in sample58.get("depth_counts", {}).items()
    }
    if observed_depth58 != expected_depth58:
        return fail("collatz ticket58 depth counts changed")
    if sample58.get("lift_stability_status") != "refuted_by_sampled_boundary_prediction_mismatch":
        return fail("collatz ticket58 must refute sampled exact32 boundary lift stability")
    if sample58.get("full_period_escape_status") != "no_sampled_full_period_escape_found":
        return fail("collatz ticket58 full-period escape status changed")
    if int(sample58.get("sampled_boundary_collision_group_count", -1)) != 0:
        return fail("collatz ticket58 projection-target boundary should be deterministic in sample")
    mismatch_examples58 = sample58.get("boundary_prediction_mismatch_examples", [])
    if not isinstance(mismatch_examples58, list) or len(mismatch_examples58) == 0:
        return fail("collatz ticket58 must include boundary prediction mismatch examples")
    if "No Collatz proof" not in str(audit58.get("proof_boundary", "")):
        return fail("collatz ticket58 proof boundary must block proof overclaim")

    ticket59_path = Path("data/open-problem/ticket59-symbolic-lift-mismatch-lab.json")
    if not ticket59_path.exists():
        return fail("missing ticket59 symbolic lift mismatch artifact")
    ticket59 = read_json(ticket59_path)
    if ticket59.get("schema") != TICKET59_SCHEMA:
        return fail("ticket59 symbolic lift mismatch artifact has unexpected schema")
    if ticket59.get("status") != "symbolic_lift_mismatch_open_no_resolution":
        return fail("ticket59 symbolic lift mismatch artifact overstates resolution")
    ticket59_attempts = ticket59.get("attempts", [])
    if not isinstance(ticket59_attempts, list):
        return fail("ticket59 attempts must be a list")
    ticket59_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket59_attempts if isinstance(attempt, dict)}
    missing_ticket59 = EXPECTED_PROBLEMS - set(ticket59_by_id)
    if missing_ticket59:
        return fail("ticket59 attempts missing problems: " + ", ".join(sorted(missing_ticket59)))
    ticket59_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-59-counted-lift-cylinder.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-59-symbolic-lift-mismatch.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-59-counted-margin-cylinder.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-59-counted-sieve-cylinder.json"),
    }
    for problem_id, attempt in ticket59_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "selected_cylinder_cover_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket59 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket59 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket59 claim boundary is too weak")
        path = ticket59_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket59 per-problem artifact")

    collatz_ticket59 = ticket59_by_id.get("collatz", {})
    cover59 = collatz_ticket59.get("bounded_result", {}).get("selected_low40_cylinder_cover", {})
    if not isinstance(cover59, dict):
        return fail("collatz ticket59 selected low40 cylinder cover missing")
    if cover59.get("theorem_name") != "SymbolicLiftMismatchCylinderOrCounted40BitCover":
        return fail("collatz ticket59 theorem name changed")
    if int(cover59.get("cylinder_low_bits", -1)) != 40:
        return fail("collatz ticket59 low-cylinder width changed")
    if int(cover59.get("cylinder_extension_bits", -1)) != 8:
        return fail("collatz ticket59 extension width changed")
    if int(cover59.get("selected_cylinder_count", -1)) != 162:
        return fail("collatz ticket59 selected cylinder count changed")
    expected_replay59 = {
        "verified_open_word": 100027,
        "unverified_canonical_word": 99973,
        "start_template_match": 3184,
        "projection_escape": 3086,
        "projection_target": 98,
        "boundary_prediction_match": 28,
        "boundary_prediction_mismatch": 70,
    }
    replay59 = cover59.get("replayed_sample_statistics", {})
    observed_replay59 = {str(key): int(replay59.get(key, -1)) for key in expected_replay59}
    if observed_replay59 != expected_replay59:
        return fail("collatz ticket59 replayed sample statistics changed")
    expected_aggregate59 = {
        "tested_48bit_extensions": 41472,
        "non_start_template_lift": 40937,
        "start_template_match": 535,
        "projection_escape": 207,
        "projection_target": 328,
        "boundary_prediction_match": 104,
        "boundary_prediction_mismatch": 224,
    }
    aggregate59 = cover59.get("aggregate_cylinder_statistics", {})
    observed_aggregate59 = {str(key): int(aggregate59.get(key, -1)) for key in expected_aggregate59}
    if observed_aggregate59 != expected_aggregate59:
        return fail("collatz ticket59 aggregate cylinder statistics changed")
    expected_status59 = {
        "mixed_outcome_cylinder": 58,
        "projection_escape_only_cylinder": 64,
        "uniform_boundary_match_cylinder": 5,
        "uniform_boundary_mismatch_cylinder": 35,
    }
    observed_status59 = {
        str(key): int(value)
        for key, value in cover59.get("cylinder_status_counts", {}).items()
    }
    if observed_status59 != expected_status59:
        return fail("collatz ticket59 cylinder status counts changed")
    if int(cover59.get("boundary_mismatch_seed_cylinders", -1)) != 70:
        return fail("collatz ticket59 mismatch seed cylinder count changed")
    if int(cover59.get("boundary_mismatch_seed_cylinders_uniform", -1)) != 35:
        return fail("collatz ticket59 uniform mismatch cylinder count changed")
    if int(cover59.get("mixed_or_unstable_cylinder_count", -1)) != 58:
        return fail("collatz ticket59 mixed cylinder count changed")
    if int(cover59.get("full_period_escape_count", -1)) != 0:
        return fail("collatz ticket59 must not find a full-period escape")
    if "does not prove Collatz" not in str(cover59.get("proof_boundary", "")):
        return fail("collatz ticket59 proof boundary must block proof overclaim")

    ticket60_path = Path("data/open-problem/ticket60-mixed-cylinder-separator-lab.json")
    if not ticket60_path.exists():
        return fail("missing ticket60 mixed cylinder separator artifact")
    ticket60 = read_json(ticket60_path)
    if ticket60.get("schema") != TICKET60_SCHEMA:
        return fail("ticket60 mixed cylinder separator artifact has unexpected schema")
    if ticket60.get("status") != "mixed_cylinder_separator_open_no_resolution":
        return fail("ticket60 mixed cylinder separator artifact overstates resolution")
    ticket60_attempts = ticket60.get("attempts", [])
    if not isinstance(ticket60_attempts, list):
        return fail("ticket60 attempts must be a list")
    ticket60_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket60_attempts if isinstance(attempt, dict)}
    missing_ticket60 = EXPECTED_PROBLEMS - set(ticket60_by_id)
    if missing_ticket60:
        return fail("ticket60 attempts missing problems: " + ", ".join(sorted(missing_ticket60)))
    ticket60_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-60-mixed-cylinder-separator.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-60-mixed-cylinder-separator.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-60-mixed-margin-separator.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-60-mixed-sieve-separator.json"),
    }
    for problem_id, attempt in ticket60_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "mixed_cylinder_separator_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket60 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket60 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket60 claim boundary is too weak")
        path = ticket60_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket60 per-problem artifact")

    collatz_ticket60 = ticket60_by_id.get("collatz", {})
    audit60 = collatz_ticket60.get("bounded_result", {}).get("mixed_cylinder_separator_audit", {})
    if not isinstance(audit60, dict):
        return fail("collatz ticket60 mixed cylinder separator audit missing")
    if audit60.get("theorem_name") != "MixedCylinderSeparatorOrAutomatonCountedCover":
        return fail("collatz ticket60 theorem name changed")
    expected_core60 = {
        "selected_low40_cylinder_count": 162,
        "selected_start_template_lift_count": 535,
        "mixed_cylinder_count": 58,
        "mixed_start_template_lift_count": 210,
    }
    observed_core60 = {str(key): int(audit60.get(key, -1)) for key in expected_core60}
    if observed_core60 != expected_core60:
        return fail("collatz ticket60 core counts changed")
    expected_status60 = {
        "mixed_outcome_cylinder": 58,
        "projection_escape_only_cylinder": 64,
        "uniform_boundary_match_cylinder": 5,
        "uniform_boundary_mismatch_cylinder": 35,
    }
    observed_status60 = {
        str(key): int(value)
        for key, value in audit60.get("cylinder_status_counts", {}).items()
    }
    if observed_status60 != expected_status60:
        return fail("collatz ticket60 cylinder status counts changed")
    expected_outcome60 = {
        "fail_offset_1": 269,
        "fail_offset_2": 144,
        "fail_offset_3": 60,
        "fail_offset_4": 35,
        "fail_offset_5": 27,
    }
    observed_outcome60 = {
        str(key): int(value)
        for key, value in audit60.get("outcome_counts", {}).items()
    }
    if observed_outcome60 != expected_outcome60:
        return fail("collatz ticket60 outcome counts changed")
    expected_prediction60 = {
        "boundary_match": 104,
        "boundary_mismatch": 224,
        "projection_escape": 207,
    }
    observed_prediction60 = {
        str(key): int(value)
        for key, value in audit60.get("prediction_counts", {}).items()
    }
    if observed_prediction60 != expected_prediction60:
        return fail("collatz ticket60 prediction counts changed")
    mixed_ladder60 = audit60.get("mixed_cylinder_separator_ladder", {})
    if mixed_ladder60.get("first_joint_deterministic_separator") != "low40_plus_failure_offset":
        return fail("collatz ticket60 first joint separator changed")
    outcome_ladder60 = mixed_ladder60.get("outcome_ladder", [])
    if not isinstance(outcome_ladder60, list) or len(outcome_ladder60) < 10:
        return fail("collatz ticket60 missing outcome separator ladder")
    low40_only60 = next((row for row in outcome_ladder60 if row.get("separator") == "low40_only"), None)
    if not isinstance(low40_only60, dict) or int(low40_only60.get("collision_group_count", -1)) != 58:
        return fail("collatz ticket60 low40-only collision count changed")
    prefix60 = next((row for row in outcome_ladder60 if row.get("separator") == "low40_plus_certificate_prefix_length"), None)
    if not isinstance(prefix60, dict) or int(prefix60.get("collision_group_count", -1)) != 36:
        return fail("collatz ticket60 prefix-length collision count changed")
    failure_offset60 = next((row for row in outcome_ladder60 if row.get("separator") == "low40_plus_failure_offset"), None)
    if not isinstance(failure_offset60, dict) or not failure_offset60.get("deterministic"):
        return fail("collatz ticket60 failure-offset separator must be deterministic")
    if "does not prove Collatz" not in str(audit60.get("proof_boundary", "")):
        return fail("collatz ticket60 proof boundary must block proof overclaim")

    ticket61_path = Path("data/open-problem/ticket61-symbolic-failure-offset-lab.json")
    if not ticket61_path.exists():
        return fail("missing ticket61 symbolic failure-offset artifact")
    ticket61 = read_json(ticket61_path)
    if ticket61.get("schema") != TICKET61_SCHEMA:
        return fail("ticket61 symbolic failure-offset artifact has unexpected schema")
    if ticket61.get("status") != "symbolic_failure_offset_open_no_resolution":
        return fail("ticket61 symbolic failure-offset artifact overstates resolution")
    ticket61_attempts = ticket61.get("attempts", [])
    if not isinstance(ticket61_attempts, list):
        return fail("ticket61 attempts must be a list")
    ticket61_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket61_attempts if isinstance(attempt, dict)}
    missing_ticket61 = EXPECTED_PROBLEMS - set(ticket61_by_id)
    if missing_ticket61:
        return fail("ticket61 attempts missing problems: " + ", ".join(sorted(missing_ticket61)))
    ticket61_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-61-symbolic-separator.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-61-symbolic-failure-offset.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-61-symbolic-margin-separator.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-61-symbolic-sieve-separator.json"),
    }
    for problem_id, attempt in ticket61_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "symbolic_failure_offset_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket61 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket61 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket61 claim boundary is too weak")
        path = ticket61_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket61 per-problem artifact")

    collatz_ticket61 = ticket61_by_id.get("collatz", {})
    audit61 = collatz_ticket61.get("bounded_result", {}).get("symbolic_failure_offset_audit", {})
    if not isinstance(audit61, dict):
        return fail("collatz ticket61 symbolic failure-offset audit missing")
    if audit61.get("theorem_name") != "SymbolicFailureOffsetPredictorOrCountedCover":
        return fail("collatz ticket61 theorem name changed")
    expected_core61 = {
        "selected_low40_cylinder_count": 162,
        "selected_start_template_lift_count": 535,
        "mixed_cylinder_count": 58,
        "mixed_start_template_lift_count": 210,
    }
    observed_core61 = {str(key): int(audit61.get(key, -1)) for key in expected_core61}
    if observed_core61 != expected_core61:
        return fail("collatz ticket61 core counts changed")
    mixed_ladder61 = audit61.get("mixed_pre_replay_separator_ladder", {})
    if mixed_ladder61.get("first_joint_deterministic_separator") != "low40_plus_high_extension_mod_2^4":
        return fail("collatz ticket61 first mixed pre-replay joint separator changed")
    if mixed_ladder61.get("first_top_bit_joint_deterministic_separator") != "low40_plus_high_extension_top_6_bits":
        return fail("collatz ticket61 top-bit separator changed")
    all_ladder61 = audit61.get("all_selected_pre_replay_separator_ladder", {})
    if all_ladder61.get("first_joint_deterministic_separator") != "low40_plus_high_extension_mod_2^4":
        return fail("collatz ticket61 first all-selected pre-replay joint separator changed")
    failure_ladder61 = mixed_ladder61.get("failure_offset_ladder", [])
    if not isinstance(failure_ladder61, list) or len(failure_ladder61) < 10:
        return fail("collatz ticket61 missing failure-offset separator ladder")
    low40_only61 = next((row for row in failure_ladder61 if row.get("separator") == "low40_only"), None)
    if not isinstance(low40_only61, dict) or int(low40_only61.get("collision_group_count", -1)) != 58:
        return fail("collatz ticket61 low40-only failure collision count changed")
    prefix61 = next((row for row in failure_ladder61 if row.get("separator") == "low40_plus_certificate_prefix_length"), None)
    if (
        not isinstance(prefix61, dict)
        or int(prefix61.get("collision_group_count", -1)) != 36
        or int(prefix61.get("ambiguous_row_count", -1)) != 81
    ):
        return fail("collatz ticket61 prefix-length failure collision count changed")
    mod16_61 = next((row for row in failure_ladder61 if row.get("separator") == "low40_plus_high_extension_mod_2^4"), None)
    if not isinstance(mod16_61, dict) or not mod16_61.get("deterministic"):
        return fail("collatz ticket61 mod16 failure separator must be deterministic")
    joint_mod16 = audit61.get("mod16_mixed_joint_row", {})
    if not isinstance(joint_mod16, dict) or not joint_mod16.get("deterministic_for_all_labels"):
        return fail("collatz ticket61 mod16 joint row must be deterministic")
    if audit61.get("next_theorem_target") != "Mod16FailureOffsetTransitionOrAutomatonCountedCover":
        return fail("collatz ticket61 next theorem target changed")
    if "does not prove Collatz" not in str(audit61.get("proof_boundary", "")):
        return fail("collatz ticket61 proof boundary must block proof overclaim")

    ticket62_path = Path("data/open-problem/ticket62-mod16-transition-cover-lab.json")
    if not ticket62_path.exists():
        return fail("missing ticket62 mod16 transition cover artifact")
    ticket62 = read_json(ticket62_path)
    if ticket62.get("schema") != TICKET62_SCHEMA:
        return fail("ticket62 mod16 transition cover artifact has unexpected schema")
    if ticket62.get("status") != "mod16_transition_cover_open_no_resolution":
        return fail("ticket62 mod16 transition cover artifact overstates resolution")
    ticket62_attempts = ticket62.get("attempts", [])
    if not isinstance(ticket62_attempts, list):
        return fail("ticket62 attempts must be a list")
    ticket62_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket62_attempts if isinstance(attempt, dict)}
    missing_ticket62 = EXPECTED_PROBLEMS - set(ticket62_by_id)
    if missing_ticket62:
        return fail("ticket62 attempts missing problems: " + ", ".join(sorted(missing_ticket62)))
    ticket62_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-62-transition-closure.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-62-mod16-transition-cover.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-62-margin-transition.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-62-sieve-transition.json"),
    }
    for problem_id, attempt in ticket62_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "bounded_mod16_transition_survives_open_no_resolution",
            "mod16_lift_obstruction_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket62 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket62 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket62 claim boundary is too weak")
        path = ticket62_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket62 per-problem artifact")

    collatz_ticket62 = ticket62_by_id.get("collatz", {})
    audit62 = collatz_ticket62.get("bounded_result", {}).get("mod16_transition_cover_audit", {})
    if not isinstance(audit62, dict):
        return fail("collatz ticket62 mod16 transition cover audit missing")
    if audit62.get("theorem_name") != "Mod16FailureOffsetTransitionOrAutomatonCountedCover":
        return fail("collatz ticket62 theorem name changed")
    if int(audit62.get("base_mixed_cylinder_count", -1)) != 58:
        return fail("collatz ticket62 base mixed cylinder count changed")
    if int(audit62.get("base_mixed_start_template_lift_count", -1)) != 210:
        return fail("collatz ticket62 base mixed lift count changed")
    if [int(value) for value in audit62.get("tested_lift_bits", [])] != [52, 56]:
        return fail("collatz ticket62 tested lift bits changed")
    if int(audit62.get("obstruction_count", -1)) != 0:
        return fail("collatz ticket62 should not report a mod16 obstruction in current audit")
    if int(audit62.get("full_period_escape_count", -1)) != 0:
        return fail("collatz ticket62 must not find a full-period escape")
    lift_audits62 = audit62.get("lift_audits", [])
    if not isinstance(lift_audits62, list) or len(lift_audits62) != 2:
        return fail("collatz ticket62 lift audits missing")
    expected_lifts62 = {
        52: {
            "tested_lifts": 3360,
            "start_template_lift": 55,
            "non_start_template_lift": 3305,
            "base_rows_with_start_template_extension": 55,
        },
        56: {
            "tested_lifts": 53760,
            "start_template_lift": 824,
            "non_start_template_lift": 52936,
            "base_rows_with_start_template_extension": 199,
        },
    }
    for lift_audit in lift_audits62:
        bits = int(lift_audit.get("bits", -1))
        expected = expected_lifts62.get(bits)
        if expected is None:
            return fail("collatz ticket62 unexpected lift bit audit")
        stats = lift_audit.get("statistics", {})
        for key in ("tested_lifts", "start_template_lift", "non_start_template_lift"):
            if int(stats.get(key, -1)) != expected[key]:
                return fail(f"collatz ticket62 {bits}-bit {key} changed")
        if int(lift_audit.get("base_rows_with_start_template_extension", -1)) != expected["base_rows_with_start_template_extension"]:
            return fail(f"collatz ticket62 {bits}-bit base extension count changed")
        mod16_row = lift_audit.get("base_mod16_joint_row", {})
        if not isinstance(mod16_row, dict) or not mod16_row.get("deterministic_for_all_labels"):
            return fail(f"collatz ticket62 {bits}-bit mod16 joint row must be deterministic")
        collisions = mod16_row.get("collision_groups", {})
        if any(int(collisions.get(field, -1)) != 0 for field in ("failure_offset", "outcome_label", "prediction_label", "transition_label")):
            return fail(f"collatz ticket62 {bits}-bit mod16 collision count changed")
        if lift_audit.get("first_joint_deterministic_separator") != "low40_plus_base_mod16":
            return fail(f"collatz ticket62 {bits}-bit first joint separator changed")
    if audit62.get("next_theorem_target") != "Mod16AutomatonCoverOrLiftCollision":
        return fail("collatz ticket62 next theorem target changed")
    if "does not prove Collatz" not in str(audit62.get("proof_boundary", "")):
        return fail("collatz ticket62 proof boundary must block proof overclaim")

    ticket63_path = Path("data/open-problem/ticket63-mod16-automaton-cover-lab.json")
    if not ticket63_path.exists():
        return fail("missing ticket63 mod16 automaton cover artifact")
    ticket63 = read_json(ticket63_path)
    if ticket63.get("schema") != TICKET63_SCHEMA:
        return fail("ticket63 mod16 automaton cover artifact has unexpected schema")
    if ticket63.get("status") != "mod16_automaton_cover_open_no_resolution":
        return fail("ticket63 mod16 automaton cover artifact overstates resolution")
    ticket63_attempts = ticket63.get("attempts", [])
    if not isinstance(ticket63_attempts, list):
        return fail("ticket63 attempts must be a list")
    ticket63_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket63_attempts if isinstance(attempt, dict)}
    missing_ticket63 = EXPECTED_PROBLEMS - set(ticket63_by_id)
    if missing_ticket63:
        return fail("ticket63 attempts missing problems: " + ", ".join(sorted(missing_ticket63)))
    ticket63_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-63-automaton-cover.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-63-mod16-automaton-cover.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-63-margin-automaton.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-63-sieve-automaton.json"),
    }
    for problem_id, attempt in ticket63_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "mod16_automaton_candidate_open_no_resolution",
            "mod16_automaton_collision_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket63 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket63 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket63 claim boundary is too weak")
        path = ticket63_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket63 per-problem artifact")

    collatz_ticket63 = ticket63_by_id.get("collatz", {})
    audit63 = collatz_ticket63.get("bounded_result", {}).get("mod16_automaton_cover_audit", {})
    if not isinstance(audit63, dict):
        return fail("collatz ticket63 mod16 automaton cover audit missing")
    if audit63.get("theorem_name") != "Mod16AutomatonCoverOrLiftCollision":
        return fail("collatz ticket63 theorem name changed")
    if int(audit63.get("base_mixed_cylinder_count", -1)) != 58:
        return fail("collatz ticket63 base mixed cylinder count changed")
    if int(audit63.get("base_mixed_start_template_lift_count", -1)) != 210:
        return fail("collatz ticket63 base mixed lift count changed")
    if int(audit63.get("chain_parent_rows", -1)) != 824:
        return fail("collatz ticket63 chain parent row count changed")
    if int(audit63.get("chain_target_rows", -1)) != 209:
        return fail("collatz ticket63 chain target row count changed")
    if int(audit63.get("chain_parent_rows_with_start_template_lift", -1)) != 209:
        return fail("collatz ticket63 chain parent survivor count changed")
    chain_stats63 = audit63.get("chain_lift_statistics", {})
    expected_chain63 = {
        "tested_chain_lifts": 13184,
        "start_template_chain_lift": 209,
        "non_start_template_chain_lift": 12975,
        "boundary_mismatch": 209,
    }
    for key, expected in expected_chain63.items():
        if int(chain_stats63.get(key, -1)) != expected:
            return fail(f"collatz ticket63 chain statistic {key} changed")
    if int(audit63.get("collision_audit_count", -1)) != 0:
        return fail("collatz ticket63 should not report automaton collisions in current audit")
    if int(audit63.get("full_period_escape_count", -1)) != 0:
        return fail("collatz ticket63 must not find a full-period escape")
    row_audits63 = audit63.get("row_audits", [])
    if not isinstance(row_audits63, list) or len(row_audits63) != 3:
        return fail("collatz ticket63 row audits missing")
    row_by_label63 = {str(row.get("label")): row for row in row_audits63 if isinstance(row, dict)}
    expected_rows63 = {
        "52_bit_direct_lift": {
            "row_count": 55,
            "state_count": 55,
            "first_quotient_separator": "low40_mod_2^16_plus_base_mod16",
        },
        "56_bit_direct_lift": {
            "row_count": 824,
            "state_count": 199,
            "first_quotient_separator": "low40_mod_2^20_plus_base_mod16",
        },
        "60_bit_chained_from_56_survivors": {
            "row_count": 209,
            "state_count": 145,
            "first_quotient_separator": "low40_mod_2^20_plus_base_mod16",
        },
    }
    for label, expected in expected_rows63.items():
        row = row_by_label63.get(label)
        if not isinstance(row, dict):
            return fail(f"collatz ticket63 missing row audit {label}")
        if int(row.get("row_count", -1)) != expected["row_count"]:
            return fail(f"collatz ticket63 row count changed for {label}")
        table = row.get("state_table", {})
        if not isinstance(table, dict) or not table.get("deterministic"):
            return fail(f"collatz ticket63 state table must be deterministic for {label}")
        if int(table.get("state_count", -1)) != expected["state_count"]:
            return fail(f"collatz ticket63 state count changed for {label}")
        if int(table.get("collision_state_count", -1)) != 0:
            return fail(f"collatz ticket63 collision count changed for {label}")
        if row.get("first_quotient_separator") != expected["first_quotient_separator"]:
            return fail(f"collatz ticket63 first quotient separator changed for {label}")
    if audit63.get("next_theorem_target") != "SymbolicMod16AutomatonTransitionProof":
        return fail("collatz ticket63 next theorem target changed")
    if "does not prove Collatz" not in str(audit63.get("proof_boundary", "")):
        return fail("collatz ticket63 proof boundary must block proof overclaim")

    ticket64_path = Path("data/open-problem/ticket64-symbolic-mod16-transition-lab.json")
    if not ticket64_path.exists():
        return fail("missing ticket64 symbolic mod16 transition artifact")
    ticket64 = read_json(ticket64_path)
    if ticket64.get("schema") != TICKET64_SCHEMA:
        return fail("ticket64 symbolic mod16 transition artifact has unexpected schema")
    if ticket64.get("status") != "symbolic_mod16_transition_open_no_resolution":
        return fail("ticket64 symbolic mod16 transition artifact overstates resolution")
    ticket64_attempts = ticket64.get("attempts", [])
    if not isinstance(ticket64_attempts, list):
        return fail("ticket64 attempts must be a list")
    ticket64_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket64_attempts if isinstance(attempt, dict)}
    missing_ticket64 = EXPECTED_PROBLEMS - set(ticket64_by_id)
    if missing_ticket64:
        return fail("ticket64 attempts missing problems: " + ", ".join(sorted(missing_ticket64)))
    ticket64_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-64-gate-predicate.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-64-symbolic-mod16-transition.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-64-cutoff-gate.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-64-parity-gate.json"),
    }
    for problem_id, attempt in ticket64_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "symbolic_transition_candidate_open_no_resolution",
            "symbolic_transition_gate_and_formula_obstruction_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket64 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket64 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket64 claim boundary is too weak")
        path = ticket64_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket64 per-problem artifact")

    collatz_ticket64 = ticket64_by_id.get("collatz", {})
    audit64 = collatz_ticket64.get("bounded_result", {}).get("symbolic_mod16_transition_audit", {})
    if not isinstance(audit64, dict):
        return fail("collatz ticket64 symbolic mod16 transition audit missing")
    if audit64.get("theorem_name") != "SymbolicMod16AutomatonTransitionProof":
        return fail("collatz ticket64 theorem name changed")
    if int(audit64.get("parent_60_rows", -1)) != 209:
        return fail("collatz ticket64 parent row count changed")
    if int(audit64.get("target_64_rows", -1)) != 42:
        return fail("collatz ticket64 target row count changed")
    if int(audit64.get("candidate_child_rows", -1)) != 3344:
        return fail("collatz ticket64 candidate child row count changed")
    expected_stats64 = {
        "tested_chain_lifts": 3344,
        "start_template_chain_lift": 42,
        "non_start_template_chain_lift": 3302,
        "boundary_match": 17,
        "boundary_mismatch": 25,
    }
    stats64 = audit64.get("chain_64_statistics", {})
    for key, expected in expected_stats64.items():
        if int(stats64.get(key, -1)) != expected:
            return fail(f"collatz ticket64 chain statistic {key} changed")
    if int(audit64.get("chain_64_parent_rows_with_start_template_lift", -1)) != 42:
        return fail("collatz ticket64 parent survivor count changed")
    gate64 = audit64.get("gate_ladder", {})
    if int(gate64.get("start_template_count", -1)) != 42:
        return fail("collatz ticket64 gate start count changed")
    if int(gate64.get("non_start_template_count", -1)) != 3302:
        return fail("collatz ticket64 gate non-start count changed")
    if gate64.get("first_gate_deterministic_separator") is not None:
        return fail("collatz ticket64 should not report a deterministic gate separator")
    state20_gate = gate64.get("state20_gate_row", {})
    if int(state20_gate.get("collision_group_count", -1)) != 42:
        return fail("collatz ticket64 state20 gate collision count changed")
    if int(state20_gate.get("ambiguous_row_count", -1)) != 1168:
        return fail("collatz ticket64 state20 gate ambiguous row count changed")
    state20_top4_gate = gate64.get("state20_top4_gate_row", {})
    if int(state20_top4_gate.get("collision_group_count", -1)) != 24:
        return fail("collatz ticket64 state20+top4 gate collision count changed")
    if int(state20_top4_gate.get("ambiguous_row_count", -1)) != 55:
        return fail("collatz ticket64 state20+top4 ambiguous row count changed")
    admitted64 = audit64.get("admitted_child_audit", {})
    if admitted64.get("label") != "64_bit_chained_from_60_survivors":
        return fail("collatz ticket64 admitted-child audit label changed")
    if int(admitted64.get("row_count", -1)) != 42:
        return fail("collatz ticket64 admitted-child row count changed")
    if admitted64.get("first_quotient_separator") != "low40_mod_2^16_plus_base_mod16":
        return fail("collatz ticket64 first admitted-child quotient changed")
    table64 = admitted64.get("state_table", {})
    if not isinstance(table64, dict) or not table64.get("deterministic"):
        return fail("collatz ticket64 admitted-child state table must remain deterministic")
    if int(table64.get("state_count", -1)) != 42:
        return fail("collatz ticket64 admitted-child state count changed")
    if int(table64.get("collision_state_count", -1)) != 0:
        return fail("collatz ticket64 admitted-child collision count changed")
    expected_transitions64 = {"0->1": 20, "0->2": 11, "0->3": 5, "0->5": 3, "0->4": 3}
    transition_counts64 = table64.get("transition_label_counts", {})
    for key, expected in expected_transitions64.items():
        if int(transition_counts64.get(key, -1)) != expected:
            return fail(f"collatz ticket64 transition count {key} changed")
    formula64 = audit64.get("symbolic_formula_pressure", {})
    if formula64.get("admitted_child_formula_holds"):
        return fail("collatz ticket64 must refute the optimistic 0->0 admitted-child formula")
    if not formula64.get("admitted_child_formula_fails"):
        return fail("collatz ticket64 formula obstruction flag missing")
    if not audit64.get("state20_gate_obstruction"):
        return fail("collatz ticket64 state20 gate obstruction flag missing")
    if not audit64.get("admitted_child_formula_obstruction"):
        return fail("collatz ticket64 admitted-child formula obstruction flag missing")
    if audit64.get("next_theorem_target") != "SymbolicStartTemplateGateAndOffsetTransition":
        return fail("collatz ticket64 next theorem target changed")
    if "does not prove Collatz" not in str(audit64.get("proof_boundary", "")):
        return fail("collatz ticket64 proof boundary must block proof overclaim")

    ticket65_path = Path("data/open-problem/ticket65-start-template-chain-extinction-lab.json")
    if not ticket65_path.exists():
        return fail("missing ticket65 start-template chain extinction artifact")
    ticket65 = read_json(ticket65_path)
    if ticket65.get("schema") != TICKET65_SCHEMA:
        return fail("ticket65 start-template chain extinction artifact has unexpected schema")
    if ticket65.get("status") != "start_template_chain_extinction_open_no_resolution":
        return fail("ticket65 start-template chain extinction artifact overstates resolution")
    ticket65_attempts = ticket65.get("attempts", [])
    if not isinstance(ticket65_attempts, list):
        return fail("ticket65 attempts must be a list")
    ticket65_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket65_attempts if isinstance(attempt, dict)}
    missing_ticket65 = EXPECTED_PROBLEMS - set(ticket65_by_id)
    if missing_ticket65:
        return fail("ticket65 attempts missing problems: " + ", ".join(sorted(missing_ticket65)))
    ticket65_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-65-branch-extinction.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-65-start-template-chain-extinction.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-65-cutoff-complement.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-65-parity-complement.json"),
    }
    for problem_id, attempt in ticket65_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "targeted_start_template_chain_extinct_global_open_no_resolution",
            "targeted_start_template_chain_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket65 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket65 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket65 claim boundary is too weak")
        path = ticket65_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket65 per-problem artifact")

    collatz_ticket65 = ticket65_by_id.get("collatz", {})
    audit65 = collatz_ticket65.get("bounded_result", {}).get("start_template_chain_extinction_audit", {})
    if not isinstance(audit65, dict):
        return fail("collatz ticket65 start-template chain extinction audit missing")
    if audit65.get("theorem_name") != "SymbolicStartTemplateGateAndOffsetTransition":
        return fail("collatz ticket65 theorem name changed")
    expected_sequence65 = [
        {"bits": 56, "rows": 824},
        {"bits": 60, "rows": 209},
        {"bits": 64, "rows": 42},
        {"bits": 68, "rows": 12},
        {"bits": 72, "rows": 3},
        {"bits": 76, "rows": 1},
        {"bits": 80, "rows": 0},
    ]
    if audit65.get("survivor_sequence") != expected_sequence65:
        return fail("collatz ticket65 survivor sequence changed")
    if not audit65.get("extinction_observed"):
        return fail("collatz ticket65 extinction flag missing")
    if int(audit65.get("extinction_at_bits", -1)) != 80:
        return fail("collatz ticket65 extinction bit changed")
    if int(audit65.get("last_nonempty_bits", -1)) != 76 or int(audit65.get("last_nonempty_rows", -1)) != 1:
        return fail("collatz ticket65 last nonempty state changed")
    if int(audit65.get("full_lasso_period_replay_count", -1)) != 0:
        return fail("collatz ticket65 full-period replay count changed")
    if not audit65.get("bounded_branch_closed"):
        return fail("collatz ticket65 bounded branch should be closed")
    if not audit65.get("gate_compression_obstruction"):
        return fail("collatz ticket65 gate-compression obstruction flag missing")
    expected_steps65 = [
        (56, 60, 824, 13184, 209, 12975, 0, 209),
        (60, 64, 209, 3344, 42, 3302, 17, 25),
        (64, 68, 42, 672, 12, 660, 0, 12),
        (68, 72, 12, 192, 3, 189, 0, 3),
        (72, 76, 3, 48, 1, 47, 0, 1),
        (76, 80, 1, 16, 0, 16, 0, 0),
    ]
    steps65 = audit65.get("chain_steps", [])
    if not isinstance(steps65, list) or len(steps65) != len(expected_steps65):
        return fail("collatz ticket65 chain step count changed")
    for row, expected in zip(steps65, expected_steps65):
        parent_bits, target_bits, parents, tested, starts, nonstarts, matches, mismatches = expected
        if int(row.get("parent_bits", -1)) != parent_bits or int(row.get("target_bits", -1)) != target_bits:
            return fail("collatz ticket65 chain step bit range changed")
        if int(row.get("parent_rows", -1)) != parents:
            return fail(f"collatz ticket65 parent rows changed for {parent_bits}->{target_bits}")
        if int(row.get("tested_chain_lifts", -1)) != tested:
            return fail(f"collatz ticket65 tested lifts changed for {parent_bits}->{target_bits}")
        if int(row.get("start_template_chain_lift", -1)) != starts:
            return fail(f"collatz ticket65 start-template count changed for {parent_bits}->{target_bits}")
        if int(row.get("non_start_template_chain_lift", -1)) != nonstarts:
            return fail(f"collatz ticket65 non-start count changed for {parent_bits}->{target_bits}")
        if int(row.get("boundary_match", -1)) != matches:
            return fail(f"collatz ticket65 boundary match count changed for {parent_bits}->{target_bits}")
        if int(row.get("boundary_mismatch", -1)) != mismatches:
            return fail(f"collatz ticket65 boundary mismatch count changed for {parent_bits}->{target_bits}")
        if int(row.get("full_lasso_period_replay", -1)) != 0:
            return fail(f"collatz ticket65 full-period replay appeared for {parent_bits}->{target_bits}")
    gate_audits65 = audit65.get("gate_audits", [])
    if not isinstance(gate_audits65, list) or len(gate_audits65) != 2:
        return fail("collatz ticket65 gate audit count changed")
    gate64_65, gate68_65 = gate_audits65
    expected_gates65 = [
        (gate64_65, 60, 64, 3344, 42, 3302, "low40_parent_top_parent_high10_child_top4", "low40_parent_high10_child_top4", 3, 6),
        (gate68_65, 64, 68, 672, 12, 660, "state20_base_mod16_child_top4", "low40_parent_high2_child_top4", 1, 2),
    ]
    for gate, parent_bits, target_bits, candidates, starts, nonstarts, row_unique, near_label, near_collisions, near_ambiguous in expected_gates65:
        if int(gate.get("parent_bits", -1)) != parent_bits or int(gate.get("target_bits", -1)) != target_bits:
            return fail("collatz ticket65 gate audit bit range changed")
        if int(gate.get("candidate_child_rows", -1)) != candidates:
            return fail(f"collatz ticket65 gate candidate count changed for {parent_bits}->{target_bits}")
        if int(gate.get("start_template_count", -1)) != starts:
            return fail(f"collatz ticket65 gate start count changed for {parent_bits}->{target_bits}")
        if int(gate.get("non_start_template_count", -1)) != nonstarts:
            return fail(f"collatz ticket65 gate non-start count changed for {parent_bits}->{target_bits}")
        if gate.get("compressed_gate_found"):
            return fail(f"collatz ticket65 should not find a compressed gate for {parent_bits}->{target_bits}")
        if not gate.get("row_unique_gate_only"):
            return fail(f"collatz ticket65 should report row-unique gate only for {parent_bits}->{target_bits}")
        summary = gate.get("pre_replay_summary", {})
        if summary.get("first_compressed_deterministic_separator") is not None:
            return fail(f"collatz ticket65 compressed separator should stay absent for {parent_bits}->{target_bits}")
        if summary.get("first_row_unique_deterministic_separator") != row_unique:
            return fail(f"collatz ticket65 row-unique separator changed for {parent_bits}->{target_bits}")
        near = summary.get("best_compressed_near_miss", {})
        if near.get("separator") != near_label:
            return fail(f"collatz ticket65 near-miss separator changed for {parent_bits}->{target_bits}")
        if int(near.get("collision_group_count", -1)) != near_collisions:
            return fail(f"collatz ticket65 near-miss collision count changed for {parent_bits}->{target_bits}")
        if int(near.get("ambiguous_row_count", -1)) != near_ambiguous:
            return fail(f"collatz ticket65 near-miss ambiguous row count changed for {parent_bits}->{target_bits}")
    if audit65.get("next_theorem_target") != "StartTemplateChainExtinctionOrComplementCover":
        return fail("collatz ticket65 next theorem target changed")
    if "does not prove Collatz" not in str(audit65.get("proof_boundary", "")):
        return fail("collatz ticket65 proof boundary must block proof overclaim")

    ticket66_path = Path("data/open-problem/ticket66-complement-cover-lab.json")
    if not ticket66_path.exists():
        return fail("missing ticket66 complement-cover artifact")
    ticket66 = read_json(ticket66_path)
    if ticket66.get("schema") != TICKET66_SCHEMA:
        return fail("ticket66 complement-cover artifact has unexpected schema")
    if ticket66.get("status") != "complement_cover_open_no_resolution":
        return fail("ticket66 complement-cover artifact overstates resolution")
    ticket66_attempts = ticket66.get("attempts", [])
    if not isinstance(ticket66_attempts, list):
        return fail("ticket66 attempts must be a list")
    ticket66_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket66_attempts if isinstance(attempt, dict)}
    missing_ticket66 = EXPECTED_PROBLEMS - set(ticket66_by_id)
    if missing_ticket66:
        return fail("ticket66 attempts missing problems: " + ", ".join(sorted(missing_ticket66)))
    ticket66_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-66-complement-cover.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-66-complement-cover.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-66-complement-cover.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-66-complement-cover.json"),
    }
    for problem_id, attempt in ticket66_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "complement_cover_failed_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket66 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket66 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket66 claim boundary is too weak")
        path = ticket66_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket66 per-problem artifact")

    collatz_ticket66 = ticket66_by_id.get("collatz", {})
    audit66 = collatz_ticket66.get("bounded_result", {}).get("complement_cover_audit", {})
    if not isinstance(audit66, dict):
        return fail("collatz ticket66 complement-cover audit missing")
    if audit66.get("theorem_name") != "ComplementCoverForStartTemplateExit":
        return fail("collatz ticket66 theorem name changed")
    if int(audit66.get("total_non_start_template_candidates", -1)) != 17189:
        return fail("collatz ticket66 total complement count changed")
    if int(audit66.get("descent_closed_count", -1)) != 55:
        return fail("collatz ticket66 descent-closed count changed")
    if int(audit66.get("open_needs_split_count", -1)) != 17134:
        return fail("collatz ticket66 open needs_split count changed")
    if int(audit66.get("unique_open_template_count", -1)) != 491:
        return fail("collatz ticket66 open template family count changed")
    if audit66.get("complement_cover_status") != "open_complement_not_covered":
        return fail("collatz ticket66 complement-cover status changed")
    if audit66.get("next_theorem_target") != "OpenTemplateFamilyRankOrComplementCounterexample":
        return fail("collatz ticket66 next theorem target changed")
    expected_reasons66 = {
        "open_wrong_tail_target_residue_mod_256": 14244,
        "open_target_tail_wrong_next_valuation": 2890,
        "closed_all_lift_descent": 55,
    }
    reason66 = audit66.get("global_reason_counts", {})
    for key, expected in expected_reasons66.items():
        if int(reason66.get(key, -1)) != expected:
            return fail(f"collatz ticket66 reason count {key} changed")
    largest66 = audit66.get("largest_open_template_family", {})
    if largest66.get("key") != "[12,[1,1,1,1],103,5]" or int(largest66.get("count", -1)) != 432:
        return fail("collatz ticket66 largest open template changed")
    expected_steps66 = [
        (56, 60, 13184, 209, 12975, 12920, 55, 188),
        (60, 64, 3344, 42, 3302, 3302, 0, 135),
        (64, 68, 672, 12, 660, 660, 0, 98),
        (68, 72, 192, 3, 189, 189, 0, 70),
        (72, 76, 48, 1, 47, 47, 0, 34),
        (76, 80, 16, 0, 16, 16, 0, 15),
    ]
    steps66 = audit66.get("per_lift", [])
    if not isinstance(steps66, list) or len(steps66) != len(expected_steps66):
        return fail("collatz ticket66 per-lift step count changed")
    for row, expected in zip(steps66, expected_steps66):
        parent_bits, target_bits, candidates, starts, nonstarts, needs_split, descent, families = expected
        if int(row.get("parent_bits", -1)) != parent_bits or int(row.get("target_bits", -1)) != target_bits:
            return fail("collatz ticket66 per-lift bit range changed")
        if int(row.get("candidate_child_rows", -1)) != candidates:
            return fail(f"collatz ticket66 candidate count changed for {parent_bits}->{target_bits}")
        if int(row.get("start_template_count", -1)) != starts:
            return fail(f"collatz ticket66 start count changed for {parent_bits}->{target_bits}")
        if int(row.get("non_start_template_count", -1)) != nonstarts:
            return fail(f"collatz ticket66 non-start count changed for {parent_bits}->{target_bits}")
        status_counts = row.get("status_counts", {})
        if int(status_counts.get("needs_split", 0)) != needs_split:
            return fail(f"collatz ticket66 needs_split count changed for {parent_bits}->{target_bits}")
        if int(status_counts.get("all_lift_descent", 0)) != descent:
            return fail(f"collatz ticket66 descent count changed for {parent_bits}->{target_bits}")
        if int(row.get("unique_open_templates", -1)) != families:
            return fail(f"collatz ticket66 unique family count changed for {parent_bits}->{target_bits}")
    if "does not prove Collatz" not in str(audit66.get("proof_boundary", "")):
        return fail("collatz ticket66 proof boundary must block proof overclaim")

    ticket67_path = Path("data/open-problem/ticket67-open-template-rank-lab.json")
    if not ticket67_path.exists():
        return fail("missing ticket67 open-template rank artifact")
    ticket67 = read_json(ticket67_path)
    if ticket67.get("schema") != TICKET67_SCHEMA:
        return fail("ticket67 open-template rank artifact has unexpected schema")
    if ticket67.get("status") != "rank_cycle_frontier_open_no_resolution":
        return fail("ticket67 open-template rank artifact overstates resolution")
    ticket67_attempts = ticket67.get("attempts", [])
    if not isinstance(ticket67_attempts, list):
        return fail("ticket67 attempts must be a list")
    ticket67_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket67_attempts if isinstance(attempt, dict)}
    missing_ticket67 = EXPECTED_PROBLEMS - set(ticket67_by_id)
    if missing_ticket67:
        return fail("ticket67 attempts missing problems: " + ", ".join(sorted(missing_ticket67)))
    ticket67_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-67-rank-cycle-frontier.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-67-open-template-rank.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-67-rank-cycle-frontier.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-67-rank-cycle-frontier.json"),
    }
    for problem_id, attempt in ticket67_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "rank_candidate_refuted_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket67 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket67 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket67 claim boundary is too weak")
        path = ticket67_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket67 per-problem artifact")

    collatz_ticket67 = ticket67_by_id.get("collatz", {})
    audit67 = collatz_ticket67.get("bounded_result", {}).get("open_template_rank_audit", {})
    if not isinstance(audit67, dict):
        return fail("collatz ticket67 open-template rank audit missing")
    if audit67.get("theorem_name") != "OpenTemplateFamilyRankOrComplementCounterexample":
        return fail("collatz ticket67 theorem name changed")
    expected_counts67 = {
        "source_open_instances": 17134,
        "source_open_template_families": 491,
        "child_lift_rows": 274144,
        "closed_source_instances_after_one_split": 13,
        "open_source_instances_after_one_split": 17121,
        "open_transition_edge_count": 45665,
        "open_transition_edge_weight": 265812,
        "transition_node_count": 5100,
        "child_open_template_families": 5056,
    }
    for key, expected in expected_counts67.items():
        if int(audit67.get(key, -1)) != expected:
            return fail(f"collatz ticket67 {key} changed")
    child_status67 = audit67.get("child_status_counts", {})
    if int(child_status67.get("needs_split", -1)) != 265812:
        return fail("collatz ticket67 child needs_split count changed")
    if int(child_status67.get("all_lift_descent", -1)) != 8332:
        return fail("collatz ticket67 child descent count changed")
    graph67 = audit67.get("graph_cycle_summary", {})
    if graph67.get("strict_template_rank_status") != "refuted_by_template_transition_cycle":
        return fail("collatz ticket67 graph cycle status changed")
    if int(graph67.get("cyclic_component_count", -1)) != 1:
        return fail("collatz ticket67 cyclic component count changed")
    if int(graph67.get("cyclic_node_count", -1)) != 429:
        return fail("collatz ticket67 cyclic node count changed")
    if int(graph67.get("largest_cyclic_component_size", -1)) != 429:
        return fail("collatz ticket67 largest cyclic component changed")
    if int(graph67.get("cycle_edge_weight", -1)) != 89222:
        return fail("collatz ticket67 cycle edge weight changed")
    if int(graph67.get("source_families_reaching_cycle", -1)) != 458:
        return fail("collatz ticket67 source family reachability changed")
    debt67 = audit67.get("debt_rank_summary", {})
    if debt67.get("scalar_debt_rank_status") != "refuted_by_nondecreasing_debt_edges":
        return fail("collatz ticket67 debt rank status changed")
    if int(debt67.get("nondecreasing_debt_edges", -1)) != 96433:
        return fail("collatz ticket67 nondecreasing debt edge count changed")
    delta67 = debt67.get("debt_delta_counts", {})
    expected_delta67 = {"negative": 169379, "positive": 87840, "zero": 8593}
    for key, expected in expected_delta67.items():
        if int(delta67.get(key, -1)) != expected:
            return fail(f"collatz ticket67 debt delta {key} changed")
    top_source67 = audit67.get("top_source_families", [{}])[0]
    if top_source67.get("family") != "[12,[1,1,1,1],103,5]":
        return fail("collatz ticket67 top source family changed")
    if int(top_source67.get("open_child_edge_weight", -1)) != 6638:
        return fail("collatz ticket67 top source edge weight changed")
    if audit67.get("next_theorem_target") != "CycleSCCRefinementOrInfiniteLiftExclusion":
        return fail("collatz ticket67 next theorem target changed")
    if "does not prove Collatz" not in str(audit67.get("proof_boundary", "")):
        return fail("collatz ticket67 proof boundary must block proof overclaim")

    ticket68_path = Path("data/open-problem/ticket68-cycle-scc-refinement-lab.json")
    if not ticket68_path.exists():
        return fail("missing ticket68 cycle-SCC refinement artifact")
    ticket68 = read_json(ticket68_path)
    if ticket68.get("schema") != TICKET68_SCHEMA:
        return fail("ticket68 cycle-SCC refinement artifact has unexpected schema")
    if ticket68.get("status") != "cycle_scc_refined_open_no_resolution":
        return fail("ticket68 cycle-SCC refinement artifact overstates resolution")
    ticket68_attempts = ticket68.get("attempts", [])
    if not isinstance(ticket68_attempts, list):
        return fail("ticket68 attempts must be a list")
    ticket68_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket68_attempts if isinstance(attempt, dict)}
    missing_ticket68 = EXPECTED_PROBLEMS - set(ticket68_by_id)
    if missing_ticket68:
        return fail("ticket68 attempts missing problems: " + ", ".join(sorted(missing_ticket68)))
    ticket68_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-68-frontier-refinement.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-68-cycle-scc-refinement.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-68-frontier-refinement.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-68-frontier-refinement.json"),
    }
    for problem_id, attempt in ticket68_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "bounded_refinement_breaks_observed_scc_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket68 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket68 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket68 claim boundary is too weak")
        path = ticket68_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket68 per-problem artifact")

    collatz_ticket68 = ticket68_by_id.get("collatz", {})
    audit68 = collatz_ticket68.get("bounded_result", {}).get("cycle_scc_refinement_audit", {})
    if not isinstance(audit68, dict):
        return fail("collatz ticket68 cycle-SCC refinement audit missing")
    if audit68.get("theorem_name") != "CycleSCCRefinementOrInfiniteLiftExclusion":
        return fail("collatz ticket68 theorem name changed")
    source68 = audit68.get("source_cycle_summary", {})
    expected_source68 = {
        "base_transition_nodes": 5100,
        "base_transition_edges": 45665,
        "base_transition_weight": 265812,
        "cyclic_component_count": 1,
        "cyclic_node_count": 429,
        "largest_cyclic_component_size": 429,
        "cycle_edge_weight": 89222,
    }
    for key, expected in expected_source68.items():
        if int(source68.get(key, -1)) != expected:
            return fail(f"collatz ticket68 source cycle {key} changed")
    if int(audit68.get("source_internal_cycle_transition_weight", -1)) != 89222:
        return fail("collatz ticket68 internal cycle transition weight changed")
    if int(audit68.get("source_open_exits_from_cycle_weight", -1)) != 174589:
        return fail("collatz ticket68 open exits from cycle changed")
    if int(audit68.get("tested_refinement_family_count", -1)) != 7:
        return fail("collatz ticket68 refinement family count changed")
    if audit68.get("refinement_status") != "bounded_prefix_consumed_refinement_breaks_observed_scc":
        return fail("collatz ticket68 refinement status changed")
    strongest68 = audit68.get("strongest_acyclic_refinement", {})
    if strongest68.get("family_id") != "base_prefix_consumed":
        return fail("collatz ticket68 strongest acyclic family changed")
    if int(strongest68.get("state_count", -1)) != 9616:
        return fail("collatz ticket68 strongest state count changed")
    if int(strongest68.get("edge_count", -1)) != 41283:
        return fail("collatz ticket68 strongest edge count changed")
    if int(strongest68.get("max_observed_topological_rank", -1)) != 5:
        return fail("collatz ticket68 topological rank changed")
    tail68 = audit68.get("strongest_tail_residue_refinement_without_prefix_consumed", {})
    if tail68.get("family_id") != "tail8_res4096_vexact":
        return fail("collatz ticket68 strongest tail/residue family changed")
    if int(tail68.get("cyclic_node_count", -1)) != 26:
        return fail("collatz ticket68 tail/residue cyclic node count changed")
    if int(tail68.get("cyclic_edge_weight", -1)) != 129:
        return fail("collatz ticket68 tail/residue cyclic weight changed")
    rows68 = audit68.get("refinement_rows", [])
    if len(rows68) != 7:
        return fail("collatz ticket68 refinement rows changed")
    by_family68 = {str(row.get("family_id")): row for row in rows68 if isinstance(row, dict)}
    expected_families68 = {
        "base_template": (429, 10596, 429, 1, 429, 89222),
        "base_prefix_consumed": (9616, 41283, 0, 0, 0, 0),
        "tail5_res512_vexact": (2311, 19896, 502, 2, 320, 37708),
        "tail6_res1024_vexact": (6902, 34622, 383, 4, 154, 8519),
        "tail8_res4096_vexact": (25967, 72341, 26, 2, 14, 129),
        "tail8_res4096_prefix_consumed": (68637, 86171, 0, 0, 0, 0),
        "full_word_res4096_vexact": (105031, 89222, 0, 0, 0, 0),
    }
    for family, expected in expected_families68.items():
        row = by_family68.get(family)
        if row is None:
            return fail(f"collatz ticket68 missing refinement family {family}")
        keys = (
            "state_count",
            "edge_count",
            "cyclic_node_count",
            "cyclic_component_count",
            "largest_cyclic_component_size",
            "cyclic_edge_weight",
        )
        for key, expected_value in zip(keys, expected):
            if int(row.get(key, -1)) != expected_value:
                return fail(f"collatz ticket68 {family} {key} changed")
    if audit68.get("next_theorem_target") != "PrefixConsumedDAGCompletenessOrPersistentRefinedCycle":
        return fail("collatz ticket68 next theorem target changed")
    if "does not prove Collatz" not in str(audit68.get("proof_boundary", "")):
        return fail("collatz ticket68 proof boundary must block proof overclaim")

    ticket69_path = Path("data/open-problem/ticket69-prefix-consumed-rank-lab.json")
    if not ticket69_path.exists():
        return fail("missing ticket69 prefix/consumed rank artifact")
    ticket69 = read_json(ticket69_path)
    if ticket69.get("schema") != TICKET69_SCHEMA:
        return fail("ticket69 prefix/consumed rank artifact has unexpected schema")
    if ticket69.get("status") != "prefix_consumed_rank_frontier_open_no_resolution":
        return fail("ticket69 prefix/consumed rank artifact overstates resolution")
    ticket69_attempts = ticket69.get("attempts", [])
    if not isinstance(ticket69_attempts, list):
        return fail("ticket69 attempts must be a list")
    ticket69_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket69_attempts if isinstance(attempt, dict)}
    missing_ticket69 = EXPECTED_PROBLEMS - set(ticket69_by_id)
    if missing_ticket69:
        return fail("ticket69 attempts missing problems: " + ", ".join(sorted(missing_ticket69)))
    ticket69_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-69-rank-completeness.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-69-prefix-consumed-rank.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-69-rank-completeness.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-69-rank-completeness.json"),
    }
    for problem_id, attempt in ticket69_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "rank_descent_valid_unexpanded_frontier_open_no_resolution",
        }:
            return fail(f"{problem_id}: ticket69 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket69 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket69 claim boundary is too weak")
        path = ticket69_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket69 per-problem artifact")

    collatz_ticket69 = ticket69_by_id.get("collatz", {})
    audit69 = collatz_ticket69.get("bounded_result", {}).get("prefix_consumed_rank_audit", {})
    if not isinstance(audit69, dict):
        return fail("collatz ticket69 prefix/consumed rank audit missing")
    if audit69.get("theorem_name") != "PrefixConsumedDAGCompletenessOrPersistentRefinedCycle":
        return fail("collatz ticket69 theorem name changed")
    if audit69.get("coordinate_family") != "base_prefix_consumed":
        return fail("collatz ticket69 coordinate family changed")
    if int(audit69.get("source_base_cycle_nodes", -1)) != 429:
        return fail("collatz ticket69 base cycle node count changed")
    if int(audit69.get("source_internal_transition_weight", -1)) != 89222:
        return fail("collatz ticket69 internal transition weight changed")
    rank69 = audit69.get("rank_summary", {})
    if rank69.get("status") != "observed_dag_rank_constructed":
        return fail("collatz ticket69 rank status changed")
    expected_rank69 = {
        "rank_map_state_count": 9616,
        "source_state_count": 1577,
        "sink_state_count": 6733,
        "max_rank": 5,
    }
    for key, expected in expected_rank69.items():
        if int(rank69.get(key, -1)) != expected:
            return fail(f"collatz ticket69 rank summary {key} changed")
    rank_level_counts69 = rank69.get("rank_level_state_counts", {})
    expected_rank_levels69 = {"0": 6733, "1": 1506, "2": 224, "3": 388, "4": 467, "5": 298}
    for key, expected in expected_rank_levels69.items():
        if int(rank_level_counts69.get(key, -1)) != expected:
            return fail(f"collatz ticket69 rank level {key} changed")
    if int(audit69.get("distinct_refined_edge_count", -1)) != 41283:
        return fail("collatz ticket69 refined edge count changed")
    if int(audit69.get("rank_edge_weight", -1)) != 89222:
        return fail("collatz ticket69 rank edge weight changed")
    delta69 = audit69.get("rank_edge_delta_counts", {})
    expected_delta69 = {"1": 32432, "2": 16891, "3": 18111, "4": 16006, "5": 5782}
    for key, expected in expected_delta69.items():
        if int(delta69.get(key, -1)) != expected:
            return fail(f"collatz ticket69 rank delta {key} changed")
    if int(audit69.get("rank_nondecreasing_edge_count", -1)) != 0:
        return fail("collatz ticket69 nondecreasing edge count changed")
    if int(audit69.get("rank_nondecreasing_edge_weight", -1)) != 0:
        return fail("collatz ticket69 nondecreasing edge weight changed")
    if int(audit69.get("source_instances_in_base_cycle", -1)) != 16967:
        return fail("collatz ticket69 source instance count changed")
    outcomes69 = audit69.get("child_outcome_counts", {})
    expected_outcomes69 = {
        "open_base_cycle_exit": 174589,
        "internal_rank_descent": 89222,
        "closed_or_terminal_all_lift_descent": 7661,
    }
    for key, expected in expected_outcomes69.items():
        if int(outcomes69.get(key, -1)) != expected:
            return fail(f"collatz ticket69 child outcome {key} changed")
    expected_state_counts69 = {
        "internal_edge_source_state_count": 2883,
        "source_expanded_state_count": 3025,
        "source_and_child_state_count": 1390,
        "source_only_state_count": 1635,
        "child_only_unexpanded_state_count": 6649,
    }
    for key, expected in expected_state_counts69.items():
        if int(audit69.get(key, -1)) != expected:
            return fail(f"collatz ticket69 {key} changed")
    frontier_rank69 = audit69.get("child_only_unexpanded_rank_counts", {})
    if int(frontier_rank69.get("0", -1)) != 6649:
        return fail("collatz ticket69 unexpanded rank-0 count changed")
    if audit69.get("rank_certificate_status") != "bounded_rank_descent_valid_but_unexpanded_frontier_open":
        return fail("collatz ticket69 rank certificate status changed")
    if audit69.get("next_theorem_target") != "PrefixConsumedRankCompletenessOrFrontierCycle":
        return fail("collatz ticket69 next theorem target changed")
    if "does not prove Collatz" not in str(audit69.get("proof_boundary", "")):
        return fail("collatz ticket69 proof boundary must block proof overclaim")

    print("open problem structure verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
