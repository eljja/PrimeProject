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
TICKET70_SCHEMA = "primeproject.ticket70-prefix-frontier-expansion-lab.v1"
TICKET71_SCHEMA = "primeproject.ticket71-stronger-frontier-coordinate-lab.v1"
TICKET72_SCHEMA = "primeproject.ticket72-infinite-frontier-lift-closure-lab.v1"
TICKET73_SCHEMA = "primeproject.ticket73-lineage-pressure-forest-lab.v1"
TICKET74_SCHEMA = "primeproject.ticket74-coverage-leakage-escape-forest-lab.v1"
TICKET75_SCHEMA = "primeproject.ticket75-escape-coordinate-closure-lab.v1"
TICKET76_SCHEMA = "primeproject.ticket76-symbolic-boundary-recurrence-lab.v1"
TICKET77_SCHEMA = "primeproject.ticket77-fixed-prefix-boundary-orbit-lab.v1"
TICKET78_SCHEMA = "primeproject.ticket78-finite-cylinder-admissibility-no-go-lab.v1"
TICKET79_SCHEMA = "primeproject.ticket79-archimedean-two-adic-rank-no-go-lab.v1"
TICKET80_SCHEMA = "primeproject.ticket80-least-counterexample-compactness-no-go-lab.v1"
TICKET81_SCHEMA = "primeproject.ticket81-mersenne-post-compensation-no-go-lab.v1"
TICKET82_SCHEMA = "primeproject.ticket82-fixed-mersenne-compensation-window-no-go-lab.v1"
TICKET83_SCHEMA = "primeproject.ticket83-mersenne-log-window-lower-bound-lab.v1"
TICKET84_SCHEMA = "primeproject.ticket84-two-adic-cycle-log-delay-lab.v1"
TICKET85_SCHEMA = "primeproject.ticket85-accessible-cycle-supremum-lab.v1"
TICKET86_SCHEMA = "primeproject.ticket86-coefficient-one-boundary-lab.v1"
TICKET87_SCHEMA = "primeproject.ticket87-two-adic-digit-run-boundary-lab.v1"
TICKET88_SCHEMA = "primeproject.ticket88-run-length-two-no-go-lab.v1"
TICKET89_SCHEMA = "primeproject.ticket89-fixed-log-golden-mean-reduction-lab.v1"
TICKET90_SCHEMA = "primeproject.ticket90-normalized-error-ghost-lasso-lab.v1"
TICKET91_SCHEMA = "primeproject.ticket91-error-tail-invariant-set-lab.v1"
TICKET92_SCHEMA = "primeproject.ticket92-scale-sensitive-threshold-audit.v1"
TICKET93_SCHEMA = "primeproject.ticket93-twin-correlation-excess-bridge.v1"
TICKET94_SCHEMA = "primeproject.ticket94-signed-remainder-and-goldbach-bridge.v1"
TICKET95_SCHEMA = "primeproject.ticket95-sharp-contamination-and-equivalence-audit.v1"
TICKET96_SCHEMA = "primeproject.ticket96-fourier-phase-information-audit.v1"
TICKET97_SCHEMA = "primeproject.ticket97-periodic-projection-residual-audit.v1"
TICKET98_SCHEMA = "primeproject.ticket98-growing-modulus-leakage-audit.v1"
TICKET99_SCHEMA = "primeproject.ticket99-out-of-sample-local-model-audit.v1"
TICKET100_SCHEMA = "primeproject.ticket100-extended-residual-vaughan-audit.v1"
TICKET101_SCHEMA = "primeproject.ticket101-vaughan-cutoff-energy-audit.v1"
TICKET102_SCHEMA = "primeproject.ticket102-twin-dyadic-vaughan-holdout.v1"
TICKET103_SCHEMA = "primeproject.ticket103-twin-local-block-audit.v1"
TICKET104_SCHEMA = "primeproject.ticket104-twin-typeii-mobius-anatomy.v1"
TICKET105_SCHEMA = "primeproject.ticket105-twin-centered-progression-discrepancy.v1"
TICKET106_SCHEMA = "primeproject.ticket106-twin-modulus-grouped-dispersion.v1"
TICKET107_SCHEMA = "primeproject.ticket107-twin-sparse-tail-recombination.v1"
TICKET108_SCHEMA = "primeproject.ticket108-twin-joint-equivalence-smoothing.v1"
TICKET109_SCHEMA = "primeproject.ticket109-twin-spectral-phase-audit.v1"
TICKET110_SCHEMA = "primeproject.ticket110-twin-rational-arc-budget.v1"
TICKET111_SCHEMA = "primeproject.ticket111-twin-typeii-minor-phase-audit.v1"
TICKET112_SCHEMA = "primeproject.ticket112-twin-farey-endpoint-abel-audit.v1"
TICKET113_SCHEMA = "primeproject.ticket113-twin-farey-denominator-endpoint-audit.v1"
TICKET114_SCHEMA = "primeproject.ticket114-twin-ramanujan-numerator-dispersion-audit.v1"
TICKET115_SCHEMA = "primeproject.ticket115-twin-complex-cyclotomic-dispersion-audit.v1"


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

    ticket70_path = Path("data/open-problem/ticket70-prefix-frontier-expansion-lab.json")
    if not ticket70_path.exists():
        return fail("missing ticket70 prefix frontier expansion artifact")
    ticket70 = read_json(ticket70_path)
    if ticket70.get("schema") != TICKET70_SCHEMA:
        return fail("ticket70 prefix frontier expansion artifact has unexpected schema")
    if ticket70.get("status") != "prefix_frontier_expansion_open_no_resolution":
        return fail("ticket70 prefix frontier expansion artifact overstates resolution")
    ticket70_attempts = ticket70.get("attempts", [])
    if not isinstance(ticket70_attempts, list):
        return fail("ticket70 attempts must be a list")
    ticket70_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket70_attempts if isinstance(attempt, dict)}
    missing_ticket70 = EXPECTED_PROBLEMS - set(ticket70_by_id)
    if missing_ticket70:
        return fail("ticket70 attempts missing problems: " + ", ".join(sorted(missing_ticket70)))
    ticket70_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-70-frontier-expansion.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-70-prefix-frontier-expansion.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-70-frontier-expansion.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-70-frontier-expansion.json"),
    }
    for problem_id, attempt in ticket70_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "frontier_expansion_refutes_direct_rank_closure_open_no_resolution",
            "frontier_expansion_finds_refined_cycle_candidates_no_resolution",
            "frontier_representatives_exit_or_close_but_infinite_bridge_open",
        }:
            return fail(f"{problem_id}: ticket70 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket70 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket70 claim boundary is too weak")
        path = ticket70_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket70 per-problem artifact")

    collatz_ticket70 = ticket70_by_id.get("collatz", {})
    audit70 = collatz_ticket70.get("bounded_result", {}).get("prefix_frontier_expansion_audit", {})
    if not isinstance(audit70, dict):
        return fail("collatz ticket70 prefix frontier expansion audit missing")
    if audit70.get("theorem_name") != "PrefixConsumedFrontierExpansionOrCycle":
        return fail("collatz ticket70 theorem name changed")
    if audit70.get("coordinate_family") != "base_prefix_consumed":
        return fail("collatz ticket70 coordinate family changed")
    expected_ticket70_counts = {
        "source_child_only_frontier_states": 6649,
        "frontier_representative_count": 49504,
        "frontier_observed_child_representative_weight": 49504,
        "expansion_edge_weight": 792064,
        "frontier_internal_edge_weight": 214770,
        "known_rank_nondecreasing_edge_count": 155321,
        "known_rank_increase_edge_count": 31918,
        "known_rank_equal_edge_count": 123403,
        "new_unranked_internal_edge_count": 59449,
        "frontier_state_nondeterminism_count": 3537,
    }
    for key, expected in expected_ticket70_counts.items():
        if int(audit70.get(key, -1)) != expected:
            return fail(f"collatz ticket70 {key} changed")
    outcomes70 = audit70.get("outcome_counts", {})
    expected_outcomes70 = {
        "open_base_cycle_exit": 516176,
        "internal_rank_equal_frontier_cycle_pressure": 123403,
        "closed_or_terminal_all_lift_descent": 61118,
        "internal_new_unranked_state": 59449,
        "internal_rank_increase_frontier_cycle_pressure": 31918,
    }
    for key, expected in expected_outcomes70.items():
        if int(outcomes70.get(key, -1)) != expected:
            return fail(f"collatz ticket70 outcome {key} changed")
    state_classes70 = audit70.get("state_class_counts", {})
    expected_state_classes70 = {
        "rank0_frontier_reenters_ranked_dag": 4498,
        "rank0_frontier_enters_new_unranked_state": 1125,
        "rank0_frontier_exits_or_closes": 1026,
    }
    for key, expected in expected_state_classes70.items():
        if int(state_classes70.get(key, -1)) != expected:
            return fail(f"collatz ticket70 state class {key} changed")
    delta70 = audit70.get("rank_delta_counts", {})
    expected_delta70 = {"-4": 5, "-3": 829, "-2": 6419, "-1": 24665, "0": 123403}
    for key, expected in expected_delta70.items():
        if int(delta70.get(key, -1)) != expected:
            return fail(f"collatz ticket70 rank delta {key} changed")
    cycle70 = audit70.get("combined_graph_cycle_summary", {})
    if int(cycle70.get("cyclic_component_count", -1)) != 0:
        return fail("collatz ticket70 one-step cycle component count changed")
    if int(audit70.get("frontier_nodes_in_combined_cycles", -1)) != 0:
        return fail("collatz ticket70 frontier cycle node count changed")
    if audit70.get("frontier_expansion_status") != "frontier_expansion_refutes_direct_rank_closure_open_no_resolution":
        return fail("collatz ticket70 frontier expansion status changed")
    if audit70.get("next_theorem_target") != "StrongerFrontierCoordinateOrPersistentLiftCycle":
        return fail("collatz ticket70 next theorem target changed")
    if "does not prove Collatz" not in str(audit70.get("proof_boundary", "")):
        return fail("collatz ticket70 proof boundary must block proof overclaim")

    ticket71_path = Path("data/open-problem/ticket71-stronger-frontier-coordinate-lab.json")
    if not ticket71_path.exists():
        return fail("missing ticket71 stronger frontier coordinate artifact")
    ticket71 = read_json(ticket71_path)
    if ticket71.get("schema") != TICKET71_SCHEMA:
        return fail("ticket71 stronger frontier coordinate artifact has unexpected schema")
    if ticket71.get("status") != "stronger_frontier_coordinate_open_no_resolution":
        return fail("ticket71 stronger frontier coordinate artifact overstates resolution")
    ticket71_attempts = ticket71.get("attempts", [])
    if not isinstance(ticket71_attempts, list):
        return fail("ticket71 attempts must be a list")
    ticket71_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket71_attempts if isinstance(attempt, dict)}
    missing_ticket71 = EXPECTED_PROBLEMS - set(ticket71_by_id)
    if missing_ticket71:
        return fail("ticket71 attempts missing problems: " + ", ".join(sorted(missing_ticket71)))
    ticket71_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-71-stronger-frontier-coordinate.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-71-stronger-frontier-coordinate.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-71-stronger-frontier-coordinate.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-71-stronger-frontier-coordinate.json"),
    }
    for problem_id, attempt in ticket71_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "bounded_transition_separator_found_but_infinite_bridge_open",
        }:
            return fail(f"{problem_id}: ticket71 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket71 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket71 claim boundary is too weak")
        path = ticket71_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket71 per-problem artifact")

    collatz_ticket71 = ticket71_by_id.get("collatz", {})
    audit71 = collatz_ticket71.get("bounded_result", {}).get("stronger_frontier_coordinate_audit", {})
    if not isinstance(audit71, dict):
        return fail("collatz ticket71 stronger frontier coordinate audit missing")
    if audit71.get("theorem_name") != "StrongerFrontierCoordinateOrPersistentLiftCycle":
        return fail("collatz ticket71 theorem name changed")
    expected_ticket71_counts = {
        "frontier_source_state_count": 6649,
        "frontier_representative_count": 49504,
        "frontier_branch_weight": 792064,
        "tested_coordinate_family_count": 6,
    }
    for key, expected in expected_ticket71_counts.items():
        if int(audit71.get(key, -1)) != expected:
            return fail(f"collatz ticket71 {key} changed")
    outcomes71 = audit71.get("outcome_class_counts", {})
    expected_outcomes71 = {
        "safe_base_cycle_exit": 516176,
        "pressure_rank_equal": 123403,
        "safe_closed_or_terminal": 61118,
        "pressure_new_unranked_internal": 59449,
        "pressure_rank_increase": 31918,
    }
    for key, expected in expected_outcomes71.items():
        if int(outcomes71.get(key, -1)) != expected:
            return fail(f"collatz ticket71 outcome {key} changed")
    pressure71 = audit71.get("pressure_outcome_counts", {})
    expected_pressure71 = {
        "pressure_rank_equal": 123403,
        "pressure_new_unranked_internal": 59449,
        "pressure_rank_increase": 31918,
    }
    for key, expected in expected_pressure71.items():
        if int(pressure71.get(key, -1)) != expected:
            return fail(f"collatz ticket71 pressure outcome {key} changed")
    rows71 = audit71.get("coordinate_rows", [])
    if not isinstance(rows71, list) or len(rows71) != 6:
        return fail("collatz ticket71 coordinate rows changed")
    expected_rows71 = {
        "base_prefix_consumed": {
            "state_count": 17686,
            "edge_count": 109232,
            "child_only_after_expansion_state_count": 8055,
            "transition_key_count": 106384,
            "mixed_transition_key_count": 22219,
            "pressure_transition_key_count": 36584,
        },
        "base_residue4096": {
            "state_count": 82162,
            "edge_count": 236984,
            "child_only_after_expansion_state_count": 47859,
            "transition_key_count": 393216,
            "mixed_transition_key_count": 48101,
            "pressure_transition_key_count": 110566,
        },
        "base_residue65536": {
            "state_count": 138745,
            "edge_count": 273429,
            "child_only_after_expansion_state_count": 90110,
            "transition_key_count": 566496,
            "mixed_transition_key_count": 40545,
            "pressure_transition_key_count": 150056,
        },
        "base_tail8_residue4096": {
            "state_count": 220454,
            "edge_count": 280512,
            "child_only_after_expansion_state_count": 170574,
            "transition_key_count": 574688,
            "mixed_transition_key_count": 39374,
            "pressure_transition_key_count": 160587,
        },
        "base_tail12_residue65536": {
            "state_count": 300624,
            "edge_count": 299598,
            "child_only_after_expansion_state_count": 237903,
            "transition_key_count": 751104,
            "mixed_transition_key_count": 6899,
            "pressure_transition_key_count": 205323,
        },
        "base_fullword_residue65536": {
            "state_count": 319801,
            "edge_count": 303992,
            "child_only_after_expansion_state_count": 254488,
            "transition_key_count": 792064,
            "mixed_transition_key_count": 0,
            "pressure_transition_key_count": 214770,
        },
    }
    rows71_by_family = {str(row.get("family_id")): row for row in rows71 if isinstance(row, dict)}
    for family, expected_values in expected_rows71.items():
        row = rows71_by_family.get(family)
        if not row:
            return fail(f"collatz ticket71 missing coordinate family {family}")
        for key, expected in expected_values.items():
            if int(row.get(key, -1)) != expected:
                return fail(f"collatz ticket71 {family} {key} changed")
        rank_summary = row.get("rank_summary", {})
        if not isinstance(rank_summary, dict) or rank_summary.get("status") != "observed_dag_rank_constructed":
            return fail(f"collatz ticket71 {family} rank status changed")
    best_separator71 = audit71.get("best_transition_separator", {})
    if best_separator71.get("family_id") != "base_fullword_residue65536":
        return fail("collatz ticket71 best separator family changed")
    if int(best_separator71.get("mixed_transition_key_count", -1)) != 0:
        return fail("collatz ticket71 best separator mixed-key count changed")
    if int(best_separator71.get("transition_key_count", -1)) != 792064:
        return fail("collatz ticket71 best separator transition-key count changed")
    best_frontier71 = audit71.get("best_frontier_reduction", {})
    if best_frontier71.get("family_id") != "base_prefix_consumed":
        return fail("collatz ticket71 compact frontier family changed")
    if int(best_frontier71.get("child_only_after_expansion_state_count", -1)) != 8055:
        return fail("collatz ticket71 compact child-only frontier count changed")
    if int(best_frontier71.get("mixed_transition_key_count", -1)) != 22219:
        return fail("collatz ticket71 compact mixed-key count changed")
    if audit71.get("frontier_coordinate_status") != "bounded_transition_separator_found_but_infinite_bridge_open":
        return fail("collatz ticket71 frontier coordinate status changed")
    if audit71.get("next_theorem_target") != "InfiniteFrontierCoordinateLiftClosureOrChain":
        return fail("collatz ticket71 next theorem target changed")
    if "does not prove Collatz" not in str(audit71.get("proof_boundary", "")):
        return fail("collatz ticket71 proof boundary must block proof overclaim")

    ticket72_path = Path("data/open-problem/ticket72-infinite-frontier-lift-closure-lab.json")
    if not ticket72_path.exists():
        return fail("missing ticket72 infinite frontier lift closure artifact")
    ticket72 = read_json(ticket72_path)
    if ticket72.get("schema") != TICKET72_SCHEMA:
        return fail("ticket72 infinite frontier lift closure artifact has unexpected schema")
    if ticket72.get("status") != "infinite_frontier_lift_closure_open_no_resolution":
        return fail("ticket72 infinite frontier lift closure artifact overstates resolution")
    ticket72_attempts = ticket72.get("attempts", [])
    if not isinstance(ticket72_attempts, list):
        return fail("ticket72 attempts must be a list")
    ticket72_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket72_attempts if isinstance(attempt, dict)}
    missing_ticket72 = EXPECTED_PROBLEMS - set(ticket72_by_id)
    if missing_ticket72:
        return fail("ticket72 attempts missing problems: " + ", ".join(sorted(missing_ticket72)))
    ticket72_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-72-infinite-frontier-lift-closure.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-72-infinite-frontier-lift-closure.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-72-infinite-frontier-lift-closure.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-72-infinite-frontier-lift-closure.json"),
    }
    for problem_id, attempt in ticket72_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "persistent_mixed_key_lift_chain_pressure_observed_no_resolution",
        }:
            return fail(f"{problem_id}: ticket72 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket72 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket72 claim boundary is too weak")
        path = ticket72_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket72 per-problem artifact")

    collatz_ticket72 = ticket72_by_id.get("collatz", {})
    audit72 = collatz_ticket72.get("bounded_result", {}).get("infinite_frontier_lift_closure_audit", {})
    if not isinstance(audit72, dict):
        return fail("collatz ticket72 infinite frontier lift closure audit missing")
    if audit72.get("theorem_name") != "InfiniteFrontierCoordinateLiftClosureOrChain":
        return fail("collatz ticket72 theorem name changed")
    if audit72.get("source_ticket") != "CO-TICKET-71":
        return fail("collatz ticket72 source ticket changed")
    expected_ticket72_counts = {
        "reconstructed_frontier_branch_weight": 792064,
        "reconstructed_mixed_transition_key_count": 22219,
        "reconstructed_pressure_mixed_transition_key_count": 20752,
        "selected_top_mixed_key_count": 8,
        "selected_first_layer_rows": 2512,
        "selected_first_layer_pressure_rows": 2303,
        "selected_second_layer_rows": 36848,
        "selected_second_layer_open_pressure_rows": 6857,
        "selected_second_layer_rank_descent_rows": 2021,
        "selected_second_layer_mixed_key_reentry_count": 9584,
        "selected_second_layer_open_pressure_mixed_key_reentry_count": 4142,
        "selected_second_layer_selected_key_reentry_count": 0,
        "third_probe_source_count": 2048,
        "third_probe_row_count": 32768,
        "third_probe_open_pressure_rows": 12300,
        "third_probe_rank_descent_rows": 342,
        "third_probe_mixed_key_reentry_count": 11455,
        "third_probe_open_pressure_mixed_key_reentry_count": 6448,
    }
    for key, expected in expected_ticket72_counts.items():
        if int(audit72.get(key, -1)) != expected:
            return fail(f"collatz ticket72 {key} changed")
    second_outcomes72 = audit72.get("selected_second_layer_outcome_counts", {})
    expected_second_outcomes72 = {
        "safe_base_cycle_exit": 27913,
        "pressure_rank_equal": 3394,
        "pressure_new_unranked_internal": 3232,
        "pressure_rank_descent": 2021,
        "pressure_rank_increase": 231,
        "safe_closed_or_terminal": 57,
    }
    for key, expected in expected_second_outcomes72.items():
        if int(second_outcomes72.get(key, -1)) != expected:
            return fail(f"collatz ticket72 second outcome {key} changed")
    third_outcomes72 = audit72.get("third_probe_outcome_counts", {})
    expected_third_outcomes72 = {
        "safe_base_cycle_exit": 20112,
        "pressure_new_unranked_internal": 9246,
        "pressure_rank_equal": 3054,
        "pressure_rank_descent": 342,
        "safe_closed_or_terminal": 14,
    }
    for key, expected in expected_third_outcomes72.items():
        if int(third_outcomes72.get(key, -1)) != expected:
            return fail(f"collatz ticket72 third outcome {key} changed")
    rows72 = audit72.get("candidate_coordinate_rows", [])
    if not isinstance(rows72, list) or len(rows72) != 11:
        return fail("collatz ticket72 coordinate rows changed")
    expected_rows72 = {
        "base_prefix_consumed": (156, 2496, 1013, 1209),
        "base_next_valuation": (156, 2496, 1013, 1209),
        "base_tail4": (156, 2496, 1013, 1209),
        "base_tail8": (927, 14832, 2715, 3851),
        "base_residue16": (156, 2496, 1013, 1209),
        "base_residue256": (156, 2496, 1013, 1209),
        "base_residue4096": (1084, 17344, 3045, 4795),
        "base_tail4_residue256": (156, 2496, 1013, 1209),
        "base_tail8_residue4096": (1968, 31488, 1509, 6234),
        "base_tail12_residue65536": (2194, 35104, 540, 6729),
        "base_fullword_residue65536": (2303, 36848, 0, 6857),
    }
    rows72_by_family = {str(row.get("family_id")): row for row in rows72 if isinstance(row, dict)}
    for family, (state_count, transition_keys, mixed_keys, pressure_keys) in expected_rows72.items():
        row = rows72_by_family.get(family)
        if not row:
            return fail(f"collatz ticket72 missing coordinate family {family}")
        checks = {
            "state_count": state_count,
            "transition_key_count": transition_keys,
            "mixed_transition_key_count": mixed_keys,
            "pressure_transition_key_count": pressure_keys,
        }
        for key, expected in checks.items():
            if int(row.get(key, -1)) != expected:
                return fail(f"collatz ticket72 {family} {key} changed")
    best_candidate72 = audit72.get("best_candidate_coordinate", {})
    if best_candidate72.get("family_id") != "base_fullword_residue65536":
        return fail("collatz ticket72 best candidate family changed")
    if best_candidate72.get("scope") != "overfit_guard":
        return fail("collatz ticket72 best candidate scope changed")
    if int(best_candidate72.get("mixed_transition_key_count", -1)) != 0:
        return fail("collatz ticket72 best candidate mixed-key count changed")
    best_compact72 = audit72.get("best_compact_candidate_coordinate", {})
    if best_compact72.get("family_id") != "base_tail12_residue65536":
        return fail("collatz ticket72 best compact family changed")
    if int(best_compact72.get("state_count", -1)) != 2194:
        return fail("collatz ticket72 best compact state count changed")
    if int(best_compact72.get("mixed_transition_key_count", -1)) != 540:
        return fail("collatz ticket72 best compact mixed-key count changed")
    examples72 = audit72.get("examples", {})
    if not isinstance(examples72, dict) or not examples72.get("second_layer_open_pressure_mixed_reentry"):
        return fail("collatz ticket72 re-entry examples missing")
    if audit72.get("lift_closure_status") != "persistent_mixed_key_lift_chain_pressure_observed_no_resolution":
        return fail("collatz ticket72 lift closure status changed")
    if audit72.get("next_theorem_target") != "CompactMixedKeyInvariantOrPersistentLiftChain":
        return fail("collatz ticket72 next theorem target changed")
    if "does not prove Collatz" not in str(audit72.get("proof_boundary", "")):
        return fail("collatz ticket72 proof boundary must block proof overclaim")

    ticket73_path = Path("data/open-problem/ticket73-lineage-pressure-forest-lab.json")
    if not ticket73_path.exists():
        return fail("missing ticket73 lineage pressure forest artifact")
    ticket73 = read_json(ticket73_path)
    if ticket73.get("schema") != TICKET73_SCHEMA:
        return fail("ticket73 lineage pressure forest artifact has unexpected schema")
    if ticket73.get("status") != "finite_lineage_pressure_audit_open_no_resolution":
        return fail("ticket73 lineage pressure forest artifact overstates resolution")
    ticket73_attempts = ticket73.get("attempts", [])
    if not isinstance(ticket73_attempts, list):
        return fail("ticket73 attempts must be a list")
    ticket73_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket73_attempts if isinstance(attempt, dict)}
    missing_ticket73 = EXPECTED_PROBLEMS - set(ticket73_by_id)
    if missing_ticket73:
        return fail("ticket73 attempts missing problems: " + ", ".join(sorted(missing_ticket73)))
    ticket73_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-73-lineage-pressure-forest.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-73-lineage-pressure-forest.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-73-lineage-pressure-forest.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-73-lineage-pressure-forest.json"),
    }
    for problem_id, attempt in ticket73_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "strict_reentry_tree_extinct_at_fifth_lift_for_selected_roots_no_global_conclusion",
        }:
            return fail(f"{problem_id}: ticket73 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket73 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket73 claim boundary is too weak")
        path = ticket73_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket73 per-problem artifact")

    collatz_ticket73 = ticket73_by_id.get("collatz", {})
    audit73 = collatz_ticket73.get("bounded_result", {}).get("lineage_pressure_forest_audit", {})
    if not isinstance(audit73, dict):
        return fail("collatz ticket73 lineage pressure forest audit missing")
    if audit73.get("theorem_name") != "FiniteRootReentryTreeExtinctionOrKonigWitness":
        return fail("collatz ticket73 theorem name changed")
    if audit73.get("source_ticket") != "CO-TICKET-72":
        return fail("collatz ticket73 source ticket changed")
    expected_ticket73_counts = {
        "reconstructed_frontier_branch_weight": 792064,
        "reconstructed_mixed_transition_key_count": 22219,
        "reconstructed_pressure_mixed_transition_key_count": 20752,
        "selected_top_mixed_key_count": 8,
        "reconstructed_second_layer_open_pressure_mixed_root_count": 4142,
    }
    for key, expected in expected_ticket73_counts.items():
        if int(audit73.get(key, -1)) != expected:
            return fail(f"collatz ticket73 {key} changed")
    expected_layers73 = {
        "third_all_source_reentry_audit": (4142, 66272, 27247, 21816, 12911, 1835),
        "fourth_reentry_audit": (12911, 206576, 80629, 4884, 2873, 614),
        "fifth_reentry_audit": (2873, 45968, 15696, 0, 0, 0),
    }
    for layer, expected_values in expected_layers73.items():
        layer_audit = audit73.get(layer, {})
        if not isinstance(layer_audit, dict):
            return fail(f"collatz ticket73 {layer} missing")
        keys = (
            "source_count",
            "row_count",
            "open_pressure_rows",
            "mixed_key_reentry_count",
            "open_pressure_mixed_key_reentry_count",
            "root_with_open_pressure_mixed_reentry_count",
        )
        for key, expected in zip(keys, expected_values):
            if int(layer_audit.get(key, -1)) != expected:
                return fail(f"collatz ticket73 {layer} {key} changed")
    survival73 = audit73.get("root_survival_counts", {})
    if survival73 != {"through_third_lift": 1835, "through_fourth_lift": 614, "through_fifth_lift": 0}:
        return fail("collatz ticket73 root survival counts changed")
    witness73 = audit73.get("witness_pressure_reentry_spine", {})
    if not isinstance(witness73, dict) or witness73.get("last_lift_depth") != 4:
        return fail("collatz ticket73 finite witness changed")
    if witness73.get("all_edges_are_exact_congruence_extensions") is not True:
        return fail("collatz ticket73 witness compatibility changed")
    logic73 = audit73.get("logical_boundary_audit", {})
    if int(logic73.get("tested_last_modulus_bits", -1)) != 84:
        return fail("collatz ticket73 last tested modulus changed")
    if int(logic73.get("fifth_layer_reentry_survivor_count", -1)) != 0:
        return fail("collatz ticket73 fifth-layer extinction changed")
    if "exact_finite_extinction" not in str(logic73.get("strict_reentry_chain_decision", "")):
        return fail("collatz ticket73 strict-chain decision missing")
    if audit73.get("lineage_tree_status") != "strict_reentry_tree_extinct_at_fifth_lift_for_selected_roots_no_global_conclusion":
        return fail("collatz ticket73 lineage tree status changed")
    if audit73.get("next_theorem_target") != "CoverageCertificateAndAllDepthReentryTreeDecision":
        return fail("collatz ticket73 next theorem target changed")
    if "neither proves Collatz" not in str(audit73.get("proof_boundary", "")):
        return fail("collatz ticket73 proof boundary must block proof overclaim")

    ticket74_path = Path("data/open-problem/ticket74-coverage-leakage-escape-forest-lab.json")
    if not ticket74_path.exists():
        return fail("missing ticket74 coverage leakage escape forest artifact")
    ticket74 = read_json(ticket74_path)
    if ticket74.get("schema") != TICKET74_SCHEMA:
        return fail("ticket74 coverage leakage escape forest artifact has unexpected schema")
    if ticket74.get("status") != "coverage_leakage_escape_forest_open_no_resolution":
        return fail("ticket74 coverage leakage escape forest artifact overstates resolution")
    ticket74_attempts = ticket74.get("attempts", [])
    if not isinstance(ticket74_attempts, list):
        return fail("ticket74 attempts must be a list")
    ticket74_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket74_attempts if isinstance(attempt, dict)}
    missing_ticket74 = EXPECTED_PROBLEMS - set(ticket74_by_id)
    if missing_ticket74:
        return fail("ticket74 attempts missing problems: " + ", ".join(sorted(missing_ticket74)))
    ticket74_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-74-coverage-leakage-escape-forest.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-74-coverage-leakage-escape-forest.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-74-coverage-leakage-escape-forest.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-74-coverage-leakage-escape-forest.json"),
    }
    for problem_id, attempt in ticket74_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "strict_cover_leakage_and_sixth_pressure_persistence_observed_no_global_resolution",
        }:
            return fail(f"{problem_id}: ticket74 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket74 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket74 claim boundary is too weak")
        path = ticket74_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket74 per-problem artifact")

    collatz_ticket74 = ticket74_by_id.get("collatz", {})
    audit74 = collatz_ticket74.get("bounded_result", {}).get("coverage_leakage_escape_forest_audit", {})
    if not isinstance(audit74, dict):
        return fail("collatz ticket74 coverage leakage audit missing")
    if audit74.get("theorem_name") != "FiniteRootCoverageLeakageOrEscapingPressureForest":
        return fail("collatz ticket74 theorem name changed")
    if audit74.get("source_ticket") != "CO-TICKET-73":
        return fail("collatz ticket74 source ticket changed")
    if int(audit74.get("reconstructed_frontier_branch_weight", -1)) != 792064:
        return fail("collatz ticket74 frontier branch count changed")
    if int(audit74.get("reconstructed_pressure_mixed_transition_key_count", -1)) != 20752:
        return fail("collatz ticket74 pressure mixed key count changed")
    coverage74 = audit74.get("coverage_audit", {})
    expected_coverage74 = {
        "selected_top_mixed_key_coverage": (8, 20752),
        "selected_first_layer_row_coverage": (2512, 371343),
        "selected_first_layer_open_pressure_coverage": (2303, 180385),
        "fifth_open_pressure_escape_ratio": (15696, 15696),
        "fifth_new_unranked_share_of_open_pressure": (15593, 15696),
    }
    for name, (numerator, denominator) in expected_coverage74.items():
        value = coverage74.get(name, {})
        if int(value.get("numerator", -1)) != numerator or int(value.get("denominator", -1)) != denominator:
            return fail(f"collatz ticket74 {name} changed")
    if int(coverage74.get("selected_root_count", -1)) != 4142:
        return fail("collatz ticket74 selected root count changed")
    if int(coverage74.get("third_strict_reentry_root_count", -1)) != 1835:
        return fail("collatz ticket74 third root count changed")
    if int(coverage74.get("fourth_strict_reentry_root_count", -1)) != 614:
        return fail("collatz ticket74 fourth root count changed")
    expected_escape_layers74 = {
        "fifth_open_pressure_escape_audit": (2873, 45968, 15696, 0, 15593, 103, 595, 0),
        "sixth_escape_pressure_audit": (15696, 251136, 78315, 5, 78315, 0, 588, 0),
    }
    for layer, expected_values in expected_escape_layers74.items():
        layer_audit = audit74.get(layer, {})
        if not isinstance(layer_audit, dict):
            return fail(f"collatz ticket74 {layer} missing")
        keys = (
            "source_count",
            "row_count",
            "open_pressure_count",
            "open_pressure_original_mixed_reentry_count",
            "new_unranked_internal_count",
            "rank_equal_count",
            "surviving_root_count",
            "exact_extension_failure_count",
        )
        for key, expected in zip(keys, expected_values):
            if int(layer_audit.get(key, -1)) != expected:
                return fail(f"collatz ticket74 {layer} {key} changed")
        if not layer_audit.get("examples"):
            return fail(f"collatz ticket74 {layer} examples missing")
    if audit74.get("coverage_leakage_status") != "strict_cover_leakage_and_sixth_pressure_persistence_observed_no_global_resolution":
        return fail("collatz ticket74 leakage status changed")
    if audit74.get("next_theorem_target") != "GlobalCoverageCertificateOrEscapingPressureForestDecision":
        return fail("collatz ticket74 next theorem target changed")
    if "does not prove Collatz" not in str(audit74.get("proof_boundary", "")):
        return fail("collatz ticket74 proof boundary must block proof overclaim")

    ticket75_path = Path("data/open-problem/ticket75-escape-coordinate-closure-lab.json")
    if not ticket75_path.exists():
        return fail("missing ticket75 escape coordinate closure artifact")
    ticket75 = read_json(ticket75_path)
    if ticket75.get("schema") != TICKET75_SCHEMA:
        return fail("ticket75 escape coordinate closure artifact has unexpected schema")
    if ticket75.get("status") != "fixed_coordinate_closure_audit_open_no_resolution":
        return fail("ticket75 escape coordinate closure artifact overstates resolution")
    ticket75_attempts = ticket75.get("attempts", [])
    if not isinstance(ticket75_attempts, list):
        return fail("ticket75 attempts must be a list")
    ticket75_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket75_attempts if isinstance(attempt, dict)}
    missing_ticket75 = EXPECTED_PROBLEMS - set(ticket75_by_id)
    if missing_ticket75:
        return fail("ticket75 attempts missing problems: " + ", ".join(sorted(missing_ticket75)))
    ticket75_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-75-escape-coordinate-closure.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-75-escape-coordinate-closure.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-75-escape-coordinate-closure.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-75-escape-coordinate-closure.json"),
    }
    for problem_id, attempt in ticket75_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "all_tested_finite_preoutcome_coordinates_leak_or_cycle_no_global_resolution",
        }:
            return fail(f"{problem_id}: ticket75 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket75 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket75 claim boundary is too weak")
        path = ticket75_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket75 per-problem artifact")

    collatz_ticket75 = ticket75_by_id.get("collatz", {})
    audit75 = collatz_ticket75.get("bounded_result", {}).get("escape_coordinate_closure_audit", {})
    if not isinstance(audit75, dict):
        return fail("collatz ticket75 coordinate closure audit missing")
    if audit75.get("theorem_name") != "FiniteEscapeCoordinateClosureOrNovelClassGrowth":
        return fail("collatz ticket75 theorem name changed")
    if audit75.get("source_ticket") != "CO-TICKET-74":
        return fail("collatz ticket75 source ticket changed")
    replay75 = audit75.get("replay_audit", {})
    expected_replay75 = {
        "fifth_open_pressure_row_count": 15696,
        "sixth_open_pressure_row_count": 78315,
        "source_identity_failure_count": 0,
        "exact_extension_failure_count": 0,
    }
    for key, expected in expected_replay75.items():
        if int(replay75.get(key, -1)) != expected:
            return fail(f"collatz ticket75 replay {key} changed")
    if replay75.get("ticket74_count_match") is not True:
        return fail("collatz ticket75 no longer matches ticket74")
    families75 = audit75.get("coordinate_family_results", [])
    if not isinstance(families75, list) or len(families75) != 8:
        return fail("collatz ticket75 coordinate family count changed")
    if audit75.get("two_layer_gate_passing_family_ids") != []:
        return fail("collatz ticket75 passing-family gate changed")
    if any(family.get("coordinate_is_fixed_finite") is not True for family in families75):
        return fail("collatz ticket75 includes a non-finite candidate family")
    if any(family.get("two_layer_finite_closure_gate_passed") is not False for family in families75):
        return fail("collatz ticket75 candidate unexpectedly passed")
    family75_by_id = {str(family.get("family_id")): family for family in families75}
    coarse75 = family75_by_id.get("tail2clip8_res64_next8", {})
    rich75 = family75_by_id.get("tail12clip32_res65536_next32_pcmod16", {})
    if int(coarse75.get("novel_sixth_open_row_count", -1)) != 11:
        return fail("collatz ticket75 coarse novelty count changed")
    if int(coarse75.get("observed_pressure_graph", {}).get("cyclic_node_count", -1)) != 66:
        return fail("collatz ticket75 coarse cyclic-node count changed")
    if int(coarse75.get("observed_pressure_graph", {}).get("mixed_pressure_outcome_key_count", -1)) != 59:
        return fail("collatz ticket75 coarse mixed-key count changed")
    if int(rich75.get("novel_sixth_open_row_count", -1)) != 77998:
        return fail("collatz ticket75 rich novelty count changed")
    if int(rich75.get("observed_pressure_graph", {}).get("mixed_pressure_outcome_key_count", -1)) != 4:
        return fail("collatz ticket75 rich mixed-key count changed")
    reference75 = audit75.get("unbounded_reference_coordinate", {})
    if reference75.get("coordinate_is_fixed_finite") is not False or reference75.get("promotion_blocked") is not True:
        return fail("collatz ticket75 unbounded reference must remain blocked")
    if audit75.get("coordinate_closure_status") != "all_tested_finite_preoutcome_coordinates_leak_or_cycle_no_global_resolution":
        return fail("collatz ticket75 closure status changed")
    if audit75.get("next_theorem_target") != "SymbolicSuccessorClosureWithWellFoundedRankOrAllDepthPressurePath":
        return fail("collatz ticket75 next theorem target changed")
    if "proves neither Collatz" not in str(audit75.get("proof_boundary", "")):
        return fail("collatz ticket75 proof boundary must block proof overclaim")

    ticket76_path = Path("data/open-problem/ticket76-symbolic-boundary-recurrence-lab.json")
    if not ticket76_path.exists():
        return fail("missing ticket76 symbolic boundary recurrence artifact")
    ticket76 = read_json(ticket76_path)
    if ticket76.get("schema") != TICKET76_SCHEMA:
        return fail("ticket76 symbolic boundary recurrence artifact has unexpected schema")
    if ticket76.get("status") != "symbolic_boundary_recurrence_open_no_resolution":
        return fail("ticket76 symbolic boundary recurrence artifact overstates resolution")
    ticket76_attempts = ticket76.get("attempts", [])
    if not isinstance(ticket76_attempts, list):
        return fail("ticket76 attempts must be a list")
    ticket76_by_id = {str(attempt.get("problem_id")): attempt for attempt in ticket76_attempts if isinstance(attempt, dict)}
    missing_ticket76 = EXPECTED_PROBLEMS - set(ticket76_by_id)
    if missing_ticket76:
        return fail("ticket76 attempts missing problems: " + ", ".join(sorted(missing_ticket76)))
    ticket76_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-76-symbolic-boundary-recurrence.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-76-symbolic-boundary-recurrence.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-76-symbolic-boundary-recurrence.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-76-symbolic-boundary-recurrence.json"),
    }
    for problem_id, attempt in ticket76_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "symbolic_formula_verified_fixed_precision_closure_refuted_on_tested_precisions_no_global_resolution",
        }:
            return fail(f"{problem_id}: ticket76 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket76 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket76 claim boundary is too weak")
        path = ticket76_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket76 per-problem artifact")

    collatz_ticket76 = ticket76_by_id.get("collatz", {})
    audit76 = collatz_ticket76.get("bounded_result", {}).get("symbolic_boundary_recurrence_audit", {})
    if not isinstance(audit76, dict):
        return fail("collatz ticket76 symbolic recurrence audit missing")
    if audit76.get("theorem_name") != "FourBitBoundaryQuotientRecurrenceAndFixedPrecisionLoss":
        return fail("collatz ticket76 theorem name changed")
    if audit76.get("source_ticket") != "CO-TICKET-75":
        return fail("collatz ticket76 source ticket changed")
    if int(audit76.get("combined_formula_row_count", -1)) != 297104:
        return fail("collatz ticket76 formula row count changed")
    if int(audit76.get("combined_formula_failure_count", -1)) != 0:
        return fail("collatz ticket76 formula failures detected")
    expected_layers76 = {
        "fifth_formula_audit": (2873, 45968, 1398, 44570),
        "sixth_formula_audit": (15696, 251136, 7751, 243385),
    }
    zero_fields76 = (
        "source_replay_mismatch_count",
        "source_valuation_identity_failure_count",
        "old_prefix_lift_mismatch_count",
        "affine_current_identity_failure_count",
        "first_new_valuation_failure_count",
        "formula_failure_count",
    )
    for layer, expected in expected_layers76.items():
        value = audit76.get(layer, {})
        keys = (
            "source_count",
            "row_count",
            "unresolved_same_prefix_child_count",
            "resolved_boundary_child_count",
        )
        for key, expected_count in zip(keys, expected):
            if int(value.get(key, -1)) != expected_count:
                return fail(f"collatz ticket76 {layer} {key} changed")
        if any(int(value.get(key, -1)) != 0 for key in zero_fields76):
            return fail(f"collatz ticket76 {layer} identity audit failed")
    precision76 = audit76.get("precision_closure_audits", [])
    expected_precision76 = {5: 165, 9: 1536, 13: 1235, 17: 106, 21: 15}
    if not isinstance(precision76, list) or len(precision76) != len(expected_precision76):
        return fail("collatz ticket76 precision audit count changed")
    for item in precision76:
        precision = int(item.get("precision_bits", -1))
        if int(item.get("fixed_precision_collision_key_count", -1)) != expected_precision76.get(precision, -2):
            return fail(f"collatz ticket76 q={precision} collision count changed")
        if int(item.get("lookahead_precision_bits", -1)) != precision + 4:
            return fail(f"collatz ticket76 q={precision} lookahead changed")
        if int(item.get("lookahead_collision_key_count", -1)) != 0:
            return fail(f"collatz ticket76 q={precision} lookahead collision detected")
        if item.get("fixed_precision_successor_sufficient_on_observed_rows") is not False:
            return fail(f"collatz ticket76 q={precision} fixed precision unexpectedly sufficient")
        if item.get("four_extra_bits_successor_sufficient_on_observed_rows") is not True:
            return fail(f"collatz ticket76 q={precision} four-bit lookahead no longer sufficient")
        if not item.get("collision_examples"):
            return fail(f"collatz ticket76 q={precision} collision witness missing")
    if audit76.get("fixed_precision_collision_precisions") != [5, 9, 13, 17, 21]:
        return fail("collatz ticket76 refuted precision list changed")
    if audit76.get("lookahead_failure_precisions") != []:
        return fail("collatz ticket76 lookahead failures changed")
    if audit76.get("symbolic_recurrence_status") != "symbolic_formula_verified_fixed_precision_closure_refuted_on_tested_precisions_no_global_resolution":
        return fail("collatz ticket76 recurrence status changed")
    if audit76.get("next_theorem_target") != "ReachableBoundaryRestrictionOrTwoAdicPressurePath":
        return fail("collatz ticket76 next theorem target changed")
    if "does not prove Collatz" not in str(audit76.get("proof_boundary", "")):
        return fail("collatz ticket76 proof boundary must block proof overclaim")

    ticket77_path = Path("data/open-problem/ticket77-fixed-prefix-boundary-orbit-lab.json")
    if not ticket77_path.exists():
        return fail("missing ticket77 fixed-prefix boundary orbit artifact")
    ticket77 = read_json(ticket77_path)
    if ticket77.get("schema") != TICKET77_SCHEMA:
        return fail("ticket77 fixed-prefix boundary orbit artifact has unexpected schema")
    if ticket77.get("status") != "fixed_prefix_boundary_orbit_open_no_collatz_resolution":
        return fail("ticket77 top-level status overstates Collatz resolution")
    ticket77_attempts = ticket77.get("attempts", [])
    if not isinstance(ticket77_attempts, list):
        return fail("ticket77 attempts must be a list")
    ticket77_by_id = {
        str(attempt.get("problem_id")): attempt
        for attempt in ticket77_attempts
        if isinstance(attempt, dict)
    }
    missing_ticket77 = EXPECTED_PROBLEMS - set(ticket77_by_id)
    if missing_ticket77:
        return fail("ticket77 attempts missing problems: " + ", ".join(sorted(missing_ticket77)))
    ticket77_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-77-fixed-prefix-boundary-orbit.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-77-fixed-prefix-boundary-orbit.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-77-fixed-prefix-boundary-orbit.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-77-fixed-prefix-boundary-orbit.json"),
    }
    for problem_id, attempt in ticket77_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "fixed_prefix_boundary_orbit_classified_no_collatz_resolution",
        }:
            return fail(f"{problem_id}: ticket77 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket77 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket77 claim boundary is too weak")
        path = ticket77_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket77 per-problem artifact")

    collatz_ticket77 = ticket77_by_id.get("collatz", {})
    audit77 = collatz_ticket77.get("bounded_result", {}).get("fixed_prefix_boundary_orbit_audit", {})
    if not isinstance(audit77, dict):
        return fail("collatz ticket77 fixed-prefix boundary orbit audit missing")
    if audit77.get("theorem_name") != "FixedStablePrefixBoundaryOrbitAndTwoAdicGhostClassification":
        return fail("collatz ticket77 theorem name changed")
    if audit77.get("source_ticket") != "CO-TICKET-76":
        return fail("collatz ticket77 source ticket changed")
    if audit77.get("theorem_status") != "fixed_prefix_boundary_orbit_classified_no_collatz_resolution":
        return fail("collatz ticket77 theorem status changed")
    if int(audit77.get("computational_failure_count", -1)) != 0:
        return fail("collatz ticket77 computational failures detected")
    observed77 = audit77.get("observed_source_audit", {})
    expected_observed77 = {
        "source_count": 18569,
        "unique_boundary_state_count": 18569,
        "strict_pressure_equality_boundary_count": 18569,
        "two_adic_fixed_cycle_count": 0,
        "unexpected_strict_cycle_count": 0,
        "trace_guard_failure_count": 0,
        "prerequisite_failure_count": 0,
        "one_step_identity_failure_count": 0,
        "max_strict_pressure_step_count": 15,
    }
    for key, expected in expected_observed77.items():
        if int(observed77.get(key, -1)) != expected:
            return fail(f"collatz ticket77 observed {key} changed")
    prefix_distribution77 = observed77.get("prefix_length_distribution", [])
    if sum(int(row.get("source_count", 0)) for row in prefix_distribution77) != 18569:
        return fail("collatz ticket77 prefix distribution total changed")
    if [int(row.get("prefix_length", -1)) for row in prefix_distribution77] != list(range(53, 65)):
        return fail("collatz ticket77 observed prefix range changed")
    orbit77 = audit77.get("orbit_identity", {})
    if orbit77.get("formula") != "ord_(3^(m+1))(16) = 3^m":
        return fail("collatz ticket77 orbit formula changed")
    if int(orbit77.get("audit_failure_count", -1)) != 0:
        return fail("collatz ticket77 orbit audit failures detected")
    if int(orbit77.get("nonexceptional_parity_failure_count", -1)) != 0:
        return fail("collatz ticket77 nonexceptional parity audit failed")
    orbit_audits77 = orbit77.get("audits", [])
    if not isinstance(orbit_audits77, list) or len(orbit_audits77) != 11:
        return fail("collatz ticket77 orbit audit range changed")
    for item in orbit_audits77:
        if item.get("order_identity_holds") is not True or item.get("order_minimality_holds") is not True:
            return fail("collatz ticket77 multiplicative-order audit failed")
        for row in item.get("class_audits", []):
            if row.get("covers_residue_class") is not True or row.get("returns_to_start") is not True:
                return fail("collatz ticket77 residue-class orbit audit failed")
    exceptional77 = orbit77.get("exceptional_zero_odd_rows", [])
    if len(exceptional77) != 1 or int(exceptional77[0].get("residue_class_mod_3", -1)) != 2:
        return fail("collatz ticket77 two-adic exception classification changed")
    if audit77.get("next_theorem_target") != "ChangingPrefixNaturalAdmissibilityRank":
        return fail("collatz ticket77 next theorem target changed")
    if "does not exclude" not in str(audit77.get("proof_boundary", "")):
        return fail("collatz ticket77 proof boundary must block Collatz overclaim")
    if "equality" not in str(audit77.get("discarded_route", "")) or "roll that step back" not in str(audit77.get("discarded_route", "")):
        return fail("collatz ticket77 must retain the equality-rollback correction")

    ticket78_path = Path("data/open-problem/ticket78-finite-cylinder-admissibility-no-go-lab.json")
    if not ticket78_path.exists():
        return fail("missing ticket78 finite-cylinder admissibility no-go artifact")
    ticket78 = read_json(ticket78_path)
    if ticket78.get("schema") != TICKET78_SCHEMA:
        return fail("ticket78 finite-cylinder artifact has unexpected schema")
    if ticket78.get("status") != "finite_cylinder_admissibility_no_go_open_no_collatz_resolution":
        return fail("ticket78 top-level status overstates resolution")
    ticket78_attempts = ticket78.get("attempts", [])
    if not isinstance(ticket78_attempts, list):
        return fail("ticket78 attempts must be a list")
    ticket78_by_id = {
        str(attempt.get("problem_id")): attempt
        for attempt in ticket78_attempts
        if isinstance(attempt, dict)
    }
    missing_ticket78 = EXPECTED_PROBLEMS - set(ticket78_by_id)
    if missing_ticket78:
        return fail("ticket78 attempts missing problems: " + ", ".join(sorted(missing_ticket78)))
    ticket78_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-78-finite-cylinder-admissibility-no-go.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-78-finite-cylinder-admissibility-no-go.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-78-finite-cylinder-admissibility-no-go.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-78-finite-cylinder-admissibility-no-go.json"),
    }
    for problem_id, attempt in ticket78_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "finite_two_adic_natural_separator_refuted_exactly_no_collatz_resolution",
        }:
            return fail(f"{problem_id}: ticket78 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket78 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket78 claim boundary is too weak")
        path = ticket78_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket78 per-problem artifact")

    collatz_ticket78 = ticket78_by_id.get("collatz", {})
    audit78 = collatz_ticket78.get("bounded_result", {}).get("finite_cylinder_no_go_audit", {})
    if not isinstance(audit78, dict):
        return fail("collatz ticket78 finite-cylinder audit missing")
    if audit78.get("theorem_name") != "FiniteValuationCylinderNaturalDensityNoGo":
        return fail("collatz ticket78 theorem name changed")
    if audit78.get("source_ticket") != "CO-TICKET-77":
        return fail("collatz ticket78 source ticket changed")
    if audit78.get("theorem_status") != "finite_two_adic_natural_separator_refuted_exactly_no_collatz_resolution":
        return fail("collatz ticket78 theorem status changed")
    if int(audit78.get("computational_failure_count", -1)) != 0:
        return fail("collatz ticket78 computational failures detected")
    machine78 = audit78.get("machine_audit", {})
    expected_machine78 = {
        "max_total_valuation": 16,
        "total_word_count": 65535,
        "expected_total_word_count": 65535,
        "shifted_representatives_per_word": 4,
        "total_positive_representative_count": 262140,
        "residue_collision_count": 0,
        "formula_failure_count": 0,
        "representative_replay_failure_count": 0,
        "count_identity_failure_count": 0,
    }
    for key, expected in expected_machine78.items():
        if int(machine78.get(key, -1)) != expected:
            return fail(f"collatz ticket78 machine audit {key} changed")
    per_total78 = machine78.get("per_total_valuation", [])
    if not isinstance(per_total78, list) or len(per_total78) != 16:
        return fail("collatz ticket78 per-total audit range changed")
    for row in per_total78:
        total = int(row.get("total_valuation", -1))
        expected_count = 1 << (total - 1)
        if total < 1 or total > 16:
            return fail("collatz ticket78 invalid total valuation")
        if int(row.get("word_count", -1)) != expected_count:
            return fail(f"collatz ticket78 S={total} word count changed")
        if int(row.get("unique_residue_count", -1)) != expected_count:
            return fail(f"collatz ticket78 S={total} residue uniqueness changed")
        if int(row.get("shifted_positive_representative_count", -1)) != 4 * expected_count:
            return fail(f"collatz ticket78 S={total} representative count changed")
        if row.get("count_identity_holds") is not True:
            return fail(f"collatz ticket78 S={total} count identity failed")
        if any(
            int(row.get(key, -1)) != 0
            for key in ("residue_collision_count", "formula_failure_count", "representative_replay_failure_count")
        ):
            return fail(f"collatz ticket78 S={total} exact audit failed")
    rejected78 = audit78.get("rejected_candidate_families", [])
    expected_families78 = {
        "fixed_residue_bits",
        "finite_accelerated_valuation_word",
        "continuous_two_adic_natural_classifier",
    }
    if {str(row.get("family")) for row in rejected78} != expected_families78:
        return fail("collatz ticket78 rejected family set changed")
    literature78 = " ".join(str(row.get("citation", "")) for row in audit78.get("literature_context", []))
    if "Bernstein" not in literature78 or "Lagarias" not in literature78 or "Rozier" not in literature78:
        return fail("collatz ticket78 literature boundary missing")
    novelty78 = str(audit78.get("novelty_boundary", ""))
    if "established mathematics" not in novelty78 or "claims only" not in novelty78:
        return fail("collatz ticket78 novelty boundary weakened")
    if audit78.get("next_theorem_target") != "ArchimedeanTwoAdicCoupledDescent":
        return fail("collatz ticket78 next theorem target changed")
    if "does not prove Collatz" not in str(audit78.get("proof_boundary", "")):
        return fail("collatz ticket78 proof boundary must block Collatz overclaim")

    ticket79_path = Path("data/open-problem/ticket79-archimedean-two-adic-rank-no-go-lab.json")
    if not ticket79_path.exists():
        return fail("missing ticket79 Archimedean-two-adic rank no-go artifact")
    ticket79 = read_json(ticket79_path)
    if ticket79.get("schema") != TICKET79_SCHEMA:
        return fail("ticket79 rank no-go artifact has unexpected schema")
    if ticket79.get("status") != "archimedean_two_adic_rank_no_go_open_no_collatz_resolution":
        return fail("ticket79 top-level status overstates resolution")
    ticket79_attempts = ticket79.get("attempts", [])
    if not isinstance(ticket79_attempts, list):
        return fail("ticket79 attempts must be a list")
    ticket79_by_id = {
        str(attempt.get("problem_id")): attempt
        for attempt in ticket79_attempts
        if isinstance(attempt, dict)
    }
    missing_ticket79 = EXPECTED_PROBLEMS - set(ticket79_by_id)
    if missing_ticket79:
        return fail("ticket79 attempts missing problems: " + ", ".join(sorted(missing_ticket79)))
    ticket79_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-79-archimedean-two-adic-rank-no-go.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-79-archimedean-two-adic-rank-no-go.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-79-archimedean-two-adic-rank-no-go.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-79-archimedean-two-adic-rank-no-go.json"),
    }
    for problem_id, attempt in ticket79_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "bounded_archimedean_two_adic_one_step_rank_refuted_exactly_no_collatz_resolution",
        }:
            return fail(f"{problem_id}: ticket79 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket79 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket79 claim boundary is too weak")
        path = ticket79_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket79 per-problem artifact")

    collatz_ticket79 = ticket79_by_id.get("collatz", {})
    audit79 = collatz_ticket79.get("bounded_result", {}).get("archimedean_two_adic_rank_no_go_audit", {})
    if not isinstance(audit79, dict):
        return fail("collatz ticket79 rank no-go audit missing")
    if audit79.get("theorem_name") != "BoundedTwoAdicCorrectionOneStepRankNoGo":
        return fail("collatz ticket79 theorem name changed")
    if audit79.get("source_ticket") != "CO-TICKET-78":
        return fail("collatz ticket79 source ticket changed")
    if audit79.get("theorem_status") != "bounded_archimedean_two_adic_one_step_rank_refuted_exactly_no_collatz_resolution":
        return fail("collatz ticket79 theorem status changed")
    if int(audit79.get("computational_failure_count", -1)) != 0:
        return fail("collatz ticket79 computational failures detected")
    machine79 = audit79.get("machine_audit", {})
    families79 = machine79.get("exact_families", {})
    expected_families79 = {
        "max_expansion_depth": 256,
        "expansion_family_case_count": 1024,
        "expansion_step_replay_count": 131584,
        "expansion_formula_failure_count": 0,
        "expansion_valuation_failure_count": 0,
        "expansion_growth_failure_count": 0,
        "max_contraction_depth": 128,
        "contraction_family_case_count": 128,
        "contraction_formula_failure_count": 0,
        "contraction_replay_failure_count": 0,
        "exact_family_failure_count": 0,
    }
    for key, expected in expected_families79.items():
        if int(families79.get(key, -1)) != expected:
            return fail(f"collatz ticket79 exact-family audit {key} changed")
    thresholds79 = machine79.get("rank_thresholds", {})
    expected_thresholds79 = {
        "positive_alpha_certificate_count": 15,
        "negative_alpha_certificate_count": 15,
        "zero_alpha_certificate_count": 5,
        "threshold_failure_count": 0,
    }
    for key, expected in expected_thresholds79.items():
        if int(thresholds79.get(key, -1)) != expected:
            return fail(f"collatz ticket79 threshold audit {key} changed")
    rejected79 = audit79.get("rejected_candidate_families", [])
    expected_rejected79 = {
        "positive_log_height_plus_bounded_two_adic_correction",
        "negative_log_height_plus_bounded_two_adic_correction",
        "zero_log_finite_state_correction",
    }
    if {str(row.get("family")) for row in rejected79} != expected_rejected79:
        return fail("collatz ticket79 rejected family set changed")
    if audit79.get("next_theorem_target") != "MinimalCounterexampleValuationSurplusContradiction":
        return fail("collatz ticket79 next theorem target changed")
    if "equivalent to Collatz" not in str(audit79.get("equivalence_warning", "")):
        return fail("collatz ticket79 equivalence warning missing")
    if "neither proves" not in str(audit79.get("proof_boundary", "")):
        return fail("collatz ticket79 proof boundary must block Collatz overclaim")

    ticket80_path = Path("data/open-problem/ticket80-least-counterexample-compactness-no-go-lab.json")
    if not ticket80_path.exists():
        return fail("missing ticket80 least-counterexample compactness no-go artifact")
    ticket80 = read_json(ticket80_path)
    if ticket80.get("schema") != TICKET80_SCHEMA:
        return fail("ticket80 compactness no-go artifact has unexpected schema")
    if ticket80.get("status") != "least_counterexample_compactness_no_go_open_no_collatz_resolution":
        return fail("ticket80 top-level status overstates resolution")
    ticket80_attempts = ticket80.get("attempts", [])
    if not isinstance(ticket80_attempts, list):
        return fail("ticket80 attempts must be a list")
    ticket80_by_id = {
        str(attempt.get("problem_id")): attempt
        for attempt in ticket80_attempts
        if isinstance(attempt, dict)
    }
    missing_ticket80 = EXPECTED_PROBLEMS - set(ticket80_by_id)
    if missing_ticket80:
        return fail("ticket80 attempts missing problems: " + ", ".join(sorted(missing_ticket80)))
    ticket80_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-80-least-counterexample-compactness-no-go.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-80-least-counterexample-compactness-no-go.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-80-least-counterexample-compactness-no-go.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-80-least-counterexample-compactness-no-go.json"),
    }
    for problem_id, attempt in ticket80_by_id.items():
        if attempt.get("status") not in {
            "proof_pressure_open",
            "least_counterexample_finite_prefix_compactness_refuted_exactly_no_collatz_resolution",
        }:
            return fail(f"{problem_id}: ticket80 attempt overstates proof status")
        for field in ("route", "attempt", "bounded_result", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket80 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket80 claim boundary is too weak")
        path = ticket80_paths.get(problem_id)
        if path is None or not path.exists():
            return fail(f"{problem_id}: missing ticket80 per-problem artifact")

    collatz_ticket80 = ticket80_by_id.get("collatz", {})
    audit80 = collatz_ticket80.get("bounded_result", {}).get("least_counterexample_compactness_no_go_audit", {})
    if not isinstance(audit80, dict):
        return fail("collatz ticket80 compactness no-go audit missing")
    if audit80.get("theorem_name") != "FiniteLeastCounterexamplePrefixCompactnessNoGo":
        return fail("collatz ticket80 theorem name changed")
    if audit80.get("source_ticket") != "CO-TICKET-79":
        return fail("collatz ticket80 source ticket changed")
    if audit80.get("theorem_status") != "least_counterexample_finite_prefix_compactness_refuted_exactly_no_collatz_resolution":
        return fail("collatz ticket80 theorem status changed")
    if int(audit80.get("computational_failure_count", -1)) != 0:
        return fail("collatz ticket80 computational failures detected")
    machine80 = audit80.get("machine_audit", {})
    finite80 = machine80.get("finite_witnesses", {})
    expected_finite80 = {
        "max_horizon": 512,
        "lower_bound_count": 5,
        "finite_witness_case_count": 2560,
        "accelerated_step_replay_count": 656640,
        "lower_bound_failure_count": 0,
        "residue_failure_count": 0,
        "formula_failure_count": 0,
        "valuation_failure_count": 0,
        "strict_non_descent_failure_count": 0,
        "affine_inequality_failure_count": 0,
        "finite_witness_failure_count": 0,
    }
    for key, expected in expected_finite80.items():
        if int(finite80.get(key, -1)) != expected:
            return fail(f"collatz ticket80 finite witness audit {key} changed")
    dual80 = machine80.get("dual_topology_escape", {})
    if int(dual80.get("two_adic_limit", 0)) != -1 or int(dual80.get("limit_accelerated_image", 0)) != -1:
        return fail("collatz ticket80 two-adic limit changed")
    if dual80.get("limit_is_positive_integer") is not False:
        return fail("collatz ticket80 ghost was misclassified as positive")
    if int(dual80.get("dual_topology_failure_count", -1)) != 0:
        return fail("collatz ticket80 dual-topology failures detected")
    rejected80 = audit80.get("rejected_candidate_families", [])
    expected_rejected80 = {
        "finite_non_descent_prefix_contradiction",
        "two_adic_compactness_to_positive_counterexample",
        "finite_verified_lower_bound_plus_prefix_search",
    }
    if {str(row.get("family")) for row in rejected80} != expected_rejected80:
        return fail("collatz ticket80 rejected family set changed")
    criterion80 = audit80.get("positive_integer_cylinder_stabilization_criterion", {})
    if "eventually stabilize" not in str(criterion80.get("statement", "")):
        return fail("collatz ticket80 positive-integer stabilization criterion missing")
    if audit80.get("next_theorem_target") != "LeastCounterexampleUniformHeightBound":
        return fail("collatz ticket80 next theorem target changed")
    if "neither proves nor disproves Collatz" not in str(audit80.get("proof_boundary", "")):
        return fail("collatz ticket80 proof boundary must block Collatz overclaim")

    ticket81_path = Path("data/open-problem/ticket81-mersenne-post-compensation-no-go-lab.json")
    if not ticket81_path.exists():
        return fail("missing ticket81 Mersenne post-compensation no-go artifact")
    ticket81 = read_json(ticket81_path)
    if ticket81.get("schema") != TICKET81_SCHEMA:
        return fail("ticket81 Mersenne no-go artifact has unexpected schema")
    if ticket81.get("status") != "mersenne_post_compensation_no_go_open_no_collatz_resolution":
        return fail("ticket81 top-level status overstates resolution")
    ticket81_attempts = ticket81.get("attempts", [])
    if not isinstance(ticket81_attempts, list):
        return fail("ticket81 attempts must be a list")
    ticket81_by_id = {
        str(attempt.get("problem_id")): attempt
        for attempt in ticket81_attempts
        if isinstance(attempt, dict)
    }
    missing_ticket81 = EXPECTED_PROBLEMS - set(ticket81_by_id)
    if missing_ticket81:
        return fail("ticket81 attempts missing problems: " + ", ".join(sorted(missing_ticket81)))
    ticket81_paths = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-81-mersenne-post-compensation-no-go.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-81-mersenne-post-compensation-no-go.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-81-mersenne-post-compensation-no-go.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-81-mersenne-post-compensation-no-go.json"),
    }
    for problem_id, attempt in ticket81_by_id.items():
        if "proved" in str(attempt.get("status", "")).lower():
            return fail(f"{problem_id}: ticket81 attempt overstates proof status")
        for field in ("route", "attempt", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket81 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket81 claim boundary is too weak")
        if not ticket81_paths[problem_id].exists():
            return fail(f"{problem_id}: missing ticket81 per-problem artifact")

    collatz_ticket81 = ticket81_by_id.get("collatz", {})
    audit81 = collatz_ticket81.get("bounded_result", {}).get("mersenne_post_compensation_no_go_audit", {})
    if not isinstance(audit81, dict):
        return fail("collatz ticket81 Mersenne no-go audit missing")
    if audit81.get("theorem_name") != "MersenneFirstPostCompensationDescentNoGo":
        return fail("collatz ticket81 theorem name changed")
    if audit81.get("source_ticket") != "CO-TICKET-80":
        return fail("collatz ticket81 source ticket changed")
    if audit81.get("theorem_status") != "mersenne_first_post_compensation_descent_refuted_exactly_no_collatz_resolution":
        return fail("collatz ticket81 theorem status changed")
    if int(audit81.get("computational_failure_count", -1)) != 0:
        return fail("collatz ticket81 computational failures detected")
    machine81 = audit81.get("machine_audit", {})
    expected_machine81 = {
        "min_k": 2,
        "max_k": 1024,
        "mersenne_case_count": 1023,
        "initial_step_replay_count": 523776,
        "odd_k_count": 511,
        "even_k_count": 512,
        "post_compensation_non_descent_count": 1020,
        "descent_exception_count": 3,
        "total_failure_count": 0,
    }
    for key, expected in expected_machine81.items():
        if int(machine81.get(key, -1)) != expected:
            return fail(f"collatz ticket81 machine audit {key} changed")
    if machine81.get("descent_exception_k") != [2, 4, 8]:
        return fail("collatz ticket81 exact descent exception set changed")
    expected_formula81 = {
        "initial_block": "A^j(N_k)=3^j*2^(k-j)-1 for 0<=j<=k-1",
        "post_block": "A^k(N_k)=oddpart(3^k-1)",
        "post_valuation": "a_k=2 for odd k; a_k=3+v2(k) for even k",
    }
    formula81 = audit81.get("exact_formula", {})
    for key, expected in expected_formula81.items():
        if formula81.get(key) != expected:
            return fail(f"collatz ticket81 exact formula {key} changed")
    expected_rejected81 = {
        "first_post_expansion_valuation_forces_descent",
        "positive_residue_stabilization_implies_near_term_descent",
        "single_lte_burst_repays_linear_valuation_debt",
    }
    rejected81 = audit81.get("rejected_candidate_families", [])
    if {str(row.get("family")) for row in rejected81} != expected_rejected81:
        return fail("collatz ticket81 rejected family set changed")
    if audit81.get("next_theorem_target") != "MersenneAdaptiveCompensationWindow":
        return fail("collatz ticket81 next theorem target changed")
    if "neither proves nor disproves Collatz" not in str(audit81.get("proof_boundary", "")):
        return fail("collatz ticket81 proof boundary must block Collatz overclaim")

    ticket82_path = Path("data/open-problem/ticket82-fixed-mersenne-compensation-window-no-go-lab.json")
    if not ticket82_path.exists():
        return fail("missing ticket82 fixed Mersenne window no-go artifact")
    ticket82 = read_json(ticket82_path)
    if ticket82.get("schema") != TICKET82_SCHEMA:
        return fail("ticket82 fixed-window artifact has unexpected schema")
    if ticket82.get("status") != "fixed_mersenne_window_no_go_open_no_collatz_resolution":
        return fail("ticket82 top-level status overstates resolution")
    attempts82 = ticket82.get("attempts", [])
    if not isinstance(attempts82, list):
        return fail("ticket82 attempts must be a list")
    by_id82 = {str(row.get("problem_id")): row for row in attempts82 if isinstance(row, dict)}
    if EXPECTED_PROBLEMS - set(by_id82):
        return fail("ticket82 attempts missing problems")
    paths82 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-82-fixed-mersenne-compensation-window-no-go.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-82-fixed-mersenne-compensation-window-no-go.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-82-fixed-mersenne-compensation-window-no-go.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-82-fixed-mersenne-compensation-window-no-go.json"),
    }
    for problem_id, attempt in by_id82.items():
        if "proved" in str(attempt.get("status", "")).lower():
            return fail(f"{problem_id}: ticket82 overstates proof status")
        for field in ("route", "attempt", "obstruction", "candidate_theorem", "claim_boundary"):
            if not attempt.get(field):
                return fail(f"{problem_id}: ticket82 missing {field}")
        if "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket82 claim boundary is too weak")
        if not paths82[problem_id].exists():
            return fail(f"{problem_id}: missing ticket82 per-problem artifact")

    audit82 = by_id82.get("collatz", {}).get("bounded_result", {}).get("fixed_mersenne_compensation_window_no_go_audit", {})
    if not isinstance(audit82, dict):
        return fail("collatz ticket82 fixed-window audit missing")
    if audit82.get("theorem_name") != "FixedMersenneCompensationWindowNoGo":
        return fail("collatz ticket82 theorem name changed")
    if audit82.get("theorem_status") != "fixed_mersenne_compensation_window_refuted_exactly_no_collatz_resolution":
        return fail("collatz ticket82 theorem status changed")
    machine82 = audit82.get("machine_audit", {})
    expected82 = {
        "max_horizon": 128,
        "horizon_case_count": 129,
        "symbolic_state_count": 8385,
        "transition_condition_count": 8256,
        "total_failure_count": 0,
    }
    for key, expected in expected82.items():
        if int(machine82.get(key, -1)) != expected:
            return fail(f"collatz ticket82 machine audit {key} changed")
    symbolic82 = audit82.get("exact_symbolic_family", {})
    if symbolic82.get("reference_post_word") != "b_1=3, b_2=4, and b_t=2 for every t>=3":
        return fail("collatz ticket82 reference valuation word changed")
    progressions82 = audit82.get("explicit_progressions", {})
    if progressions82.get("horizon_at_least_2") != "k congruent to 3 modulo 2^(2H+3)":
        return fail("collatz ticket82 explicit exponent progression changed")
    rejected82 = {str(row.get("family")) for row in audit82.get("rejected_candidate_families", [])}
    if rejected82 != {
        "constant_post_expansion_compensation_window",
        "finite_parity_prefix_implies_uniform_mersenne_descent",
        "bounded_lookahead_least_counterexample_contradiction",
    }:
        return fail("collatz ticket82 rejected family set changed")
    if audit82.get("next_theorem_target") != "MersenneGrowingWindowDescent":
        return fail("collatz ticket82 next theorem target changed")
    if "neither constructs a divergent orbit" not in str(audit82.get("proof_boundary", "")):
        return fail("collatz ticket82 proof boundary must block divergence overclaim")

    path83 = Path("data/open-problem/ticket83-mersenne-log-window-lower-bound-lab.json")
    if not path83.exists():
        return fail("missing ticket83 Mersenne log-window artifact")
    ticket83 = read_json(path83)
    if ticket83.get("schema") != TICKET83_SCHEMA or ticket83.get("status") != "mersenne_log_window_lower_bound_open_no_collatz_resolution":
        return fail("ticket83 schema or status changed")
    attempts83 = ticket83.get("attempts", [])
    by_id83 = {str(row.get("problem_id")): row for row in attempts83 if isinstance(row, dict)} if isinstance(attempts83, list) else {}
    if set(by_id83) != EXPECTED_PROBLEMS:
        return fail("ticket83 attempts missing problems")
    paths83 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-83-mersenne-log-window-lower-bound.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-83-mersenne-log-window-lower-bound.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-83-mersenne-log-window-lower-bound.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-83-mersenne-log-window-lower-bound.json"),
    }
    for problem_id, attempt in by_id83.items():
        if not paths83[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket83 artifact or claim boundary missing")
    audit83 = by_id83["collatz"].get("bounded_result", {}).get("mersenne_log_window_lower_bound_audit", {})
    if audit83.get("theorem_name") != "MersenneHalfLogDelayLowerBound":
        return fail("collatz ticket83 theorem name changed")
    if audit83.get("theorem_status") != "mersenne_sub_half_log_window_refuted_exactly_no_collatz_resolution":
        return fail("collatz ticket83 theorem status changed")
    machine83 = audit83.get("machine_audit", {})
    for key, expected in {"min_horizon": 2, "max_horizon": 256, "horizon_case_count": 255, "symbolic_state_count": 33150, "total_failure_count": 0}.items():
        if int(machine83.get(key, -1)) != expected:
            return fail(f"collatz ticket83 metric {key} changed")
    if audit83.get("explicit_sequence") != "k_H=3+2^(2H+3), H>=2":
        return fail("collatz ticket83 explicit sequence changed")
    if audit83.get("next_theorem_target") != "MersenneLogWindowDichotomy":
        return fail("collatz ticket83 next target changed")
    if "neither a divergent Collatz orbit" not in str(audit83.get("proof_boundary", "")):
        return fail("collatz ticket83 divergence boundary missing")

    path84 = Path("data/open-problem/ticket84-two-adic-cycle-log-delay-lab.json")
    if not path84.exists():
        return fail("missing ticket84 two-adic cycle artifact")
    ticket84 = read_json(path84)
    if ticket84.get("schema") != TICKET84_SCHEMA or ticket84.get("status") != "two_adic_cycle_log_delay_open_no_collatz_resolution":
        return fail("ticket84 schema or status changed")
    attempts84 = ticket84.get("attempts", [])
    by_id84 = {str(row.get("problem_id")): row for row in attempts84 if isinstance(row, dict)} if isinstance(attempts84, list) else {}
    if set(by_id84) != EXPECTED_PROBLEMS:
        return fail("ticket84 attempts missing problems")
    paths84 = {"riemann": Path("data/open-problem/riemann/rh-ticket-84-two-adic-cycle-log-delay.json"), "collatz": Path("data/open-problem/collatz/co-ticket-84-two-adic-cycle-log-delay.json"), "goldbach": Path("data/open-problem/goldbach/gb-ticket-84-two-adic-cycle-log-delay.json"), "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-84-two-adic-cycle-log-delay.json")}
    for problem_id, attempt in by_id84.items():
        if not paths84[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket84 artifact or boundary missing")
    audit84 = by_id84["collatz"].get("bounded_result", {}).get("two_adic_cycle_log_delay_audit", {})
    if audit84.get("theorem_name") != "MersenneTwoThirdsLogDelayLowerBound" or audit84.get("theorem_status") != "mersenne_two_thirds_log_window_refuted_exactly_no_collatz_resolution":
        return fail("collatz ticket84 theorem contract changed")
    machine84 = audit84.get("machine_audit", {})
    for key, expected in {"horizon_case_count": 255, "hensel_precision_count": 384, "maximum_precision": 386, "symbolic_state_count": 33150, "total_failure_count": 0}.items():
        if int(machine84.get(key, -1)) != expected:
            return fail(f"collatz ticket84 metric {key} changed")
    if audit84.get("next_theorem_target") != "AccessibleCycleCoefficientSupremum" or "neither divergence" not in str(audit84.get("proof_boundary", "")):
        return fail("collatz ticket84 next target or proof boundary changed")

    path85 = Path("data/open-problem/ticket85-accessible-cycle-supremum-lab.json")
    if not path85.exists():
        return fail("missing ticket85 cycle supremum artifact")
    ticket85 = read_json(path85)
    if ticket85.get("schema") != TICKET85_SCHEMA or ticket85.get("status") != "accessible_cycle_supremum_open_no_collatz_resolution":
        return fail("ticket85 schema or status changed")
    attempts85 = ticket85.get("attempts", [])
    by_id85 = {str(row.get("problem_id")): row for row in attempts85 if isinstance(row, dict)} if isinstance(attempts85, list) else {}
    if set(by_id85) != EXPECTED_PROBLEMS:
        return fail("ticket85 attempts missing problems")
    paths85 = {"riemann": Path("data/open-problem/riemann/rh-ticket-85-accessible-cycle-supremum.json"), "collatz": Path("data/open-problem/collatz/co-ticket-85-accessible-cycle-supremum.json"), "goldbach": Path("data/open-problem/goldbach/gb-ticket-85-accessible-cycle-supremum.json"), "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-85-accessible-cycle-supremum.json")}
    for problem_id, attempt in by_id85.items():
        if not paths85[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket85 artifact or boundary missing")
    audit85 = by_id85["collatz"].get("bounded_result", {}).get("accessible_cycle_supremum_audit", {})
    if audit85.get("theorem_name") != "AccessibleCycleCoefficientSupremumOne" or audit85.get("theorem_status") != "accessible_cycle_supremum_one_proved_no_collatz_resolution":
        return fail("collatz ticket85 theorem contract changed")
    machine85 = audit85.get("machine_audit", {})
    for key, expected in {"horizon_case_count": 255, "hensel_lift_count": 32895, "maximum_precision": 259, "symbolic_state_count": 33150, "total_failure_count": 0}.items():
        if int(machine85.get(key, -1)) != expected:
            return fail(f"collatz ticket85 metric {key} changed")
    if audit85.get("next_theorem_target") != "CoefficientOneBoundary" or "constructs no divergent orbit" not in str(audit85.get("proof_boundary", "")):
        return fail("collatz ticket85 next target or boundary changed")

    path86 = Path("data/open-problem/ticket86-coefficient-one-boundary-lab.json")
    if not path86.exists():
        return fail("missing ticket86 coefficient-one boundary artifact")
    ticket86 = read_json(path86)
    if ticket86.get("schema") != TICKET86_SCHEMA or ticket86.get("status") != "coefficient_one_boundary_open_no_collatz_resolution":
        return fail("ticket86 schema or status changed")
    attempts86 = ticket86.get("attempts", [])
    by_id86 = {str(row.get("problem_id")): row for row in attempts86 if isinstance(row, dict)} if isinstance(attempts86, list) else {}
    if set(by_id86) != EXPECTED_PROBLEMS:
        return fail("ticket86 attempts missing problems")
    paths86 = {"riemann": Path("data/open-problem/riemann/rh-ticket-86-coefficient-one-boundary.json"), "collatz": Path("data/open-problem/collatz/co-ticket-86-coefficient-one-boundary.json"), "goldbach": Path("data/open-problem/goldbach/gb-ticket-86-coefficient-one-boundary.json"), "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-86-coefficient-one-boundary.json")}
    for problem_id, attempt in by_id86.items():
        if not paths86[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket86 artifact or boundary missing")
    audit86 = by_id86["collatz"].get("bounded_result", {}).get("coefficient_one_boundary_audit", {})
    if audit86.get("theorem_name") != "InfiniteCoefficientOneMersenneDelay" or audit86.get("theorem_status") != "restricted_coefficient_one_delay_proved_no_collatz_resolution":
        return fail("collatz ticket86 theorem contract changed")
    machine86 = audit86.get("machine_audit", {})
    for key, expected in {"prefix_case_count": 1023, "top_bit_case_count": 499, "zero_bit_case_count": 524, "longest_observed_zero_run": 13, "maximum_precision": 1027, "symbolic_jump_case_count": 124, "symbolic_state_count": 16877, "total_failure_count": 0}.items():
        if int(machine86.get(key, -1)) != expected:
            return fail(f"collatz ticket86 metric {key} changed")
    if audit86.get("next_theorem_target") != "TwoAdicDigitRunBoundary" or "neither Collatz convergence nor divergence" not in str(audit86.get("proof_boundary", "")):
        return fail("collatz ticket86 next target or proof boundary changed")

    path87 = Path("data/open-problem/ticket87-two-adic-digit-run-boundary-lab.json")
    if not path87.exists():
        return fail("missing ticket87 digit-run boundary artifact")
    ticket87 = read_json(path87)
    if ticket87.get("schema") != TICKET87_SCHEMA or ticket87.get("status") != "two_adic_digit_run_boundary_open_no_collatz_resolution":
        return fail("ticket87 schema or status changed")
    attempts87 = ticket87.get("attempts", [])
    by_id87 = {str(row.get("problem_id")): row for row in attempts87 if isinstance(row, dict)} if isinstance(attempts87, list) else {}
    if set(by_id87) != EXPECTED_PROBLEMS:
        return fail("ticket87 attempts missing problems")
    paths87 = {"riemann": Path("data/open-problem/riemann/rh-ticket-87-two-adic-digit-run-boundary.json"), "collatz": Path("data/open-problem/collatz/co-ticket-87-two-adic-digit-run-boundary.json"), "goldbach": Path("data/open-problem/goldbach/gb-ticket-87-two-adic-digit-run-boundary.json"), "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-87-two-adic-digit-run-boundary.json")}
    for problem_id, attempt in by_id87.items():
        if not paths87[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket87 artifact or boundary missing")
    audit87 = by_id87["collatz"].get("bounded_result", {}).get("two_adic_digit_run_audit", {})
    if audit87.get("theorem_name") != "InfiniteAdditiveOneMersenneDelay" or audit87.get("theorem_status") != "restricted_additive_one_delay_proved_no_collatz_resolution":
        return fail("collatz ticket87 theorem contract changed")
    machine87 = audit87.get("machine_audit", {})
    for key, expected in {"prefix_bit_count": 262143, "top_bit_count": 131307, "zero_bit_count": 130836, "complete_run_count": 131306, "positive_zero_run_count": 65368, "longest_observed_zero_run": 16, "hensel_crosscheck_horizon": 1024, "total_failure_count": 0}.items():
        if int(machine87.get(key, -1)) != expected:
            return fail(f"collatz ticket87 metric {key} changed")
    if audit87.get("next_theorem_target") != "TwoAdicRunLengthTwoInfinitude" or "neither Collatz convergence nor divergence" not in str(audit87.get("proof_boundary", "")):
        return fail("collatz ticket87 next target or proof boundary changed")

    path88 = Path("data/open-problem/ticket88-run-length-two-no-go-lab.json")
    if not path88.exists():
        return fail("missing ticket88 run-length-two no-go artifact")
    ticket88 = read_json(path88)
    if ticket88.get("schema") != TICKET88_SCHEMA or ticket88.get("status") != "run_length_two_no_go_open_no_collatz_resolution":
        return fail("ticket88 schema or status changed")
    attempts88 = ticket88.get("attempts", [])
    by_id88 = {str(row.get("problem_id")): row for row in attempts88 if isinstance(row, dict)} if isinstance(attempts88, list) else {}
    if set(by_id88) != EXPECTED_PROBLEMS:
        return fail("ticket88 attempts missing problems")
    paths88 = {"riemann": Path("data/open-problem/riemann/rh-ticket-88-run-length-two-no-go.json"), "collatz": Path("data/open-problem/collatz/co-ticket-88-run-length-two-no-go.json"), "goldbach": Path("data/open-problem/goldbach/gb-ticket-88-run-length-two-no-go.json"), "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-88-run-length-two-no-go.json")}
    for problem_id, attempt in by_id88.items():
        if not paths88[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket88 artifact or boundary missing")
    audit88 = by_id88["collatz"].get("bounded_result", {}).get("run_length_two_no_go_audit", {})
    if audit88.get("theorem_name") != "TwoSidedDigitInfinitudeDoesNotForceRunLengthTwo" or audit88.get("theorem_status") != "run_length_two_inference_refuted_exactly_no_collatz_resolution":
        return fail("collatz ticket88 theorem contract changed")
    machine88 = audit88.get("machine_audit", {})
    for key, expected in {"countermodel_horizon": 4096, "countermodel_zero_count": 63, "countermodel_one_count": 4034, "countermodel_adjacent_zero_count": 0, "complement_horizon": 4096, "complement_failure_count": 0, "observed_run_length_two_or_more_count": 32753, "total_failure_count": 0}.items():
        if int(machine88.get(key, -1)) != expected:
            return fail(f"collatz ticket88 metric {key} changed")
    if audit88.get("next_theorem_target") != "FixedLogGoldenMeanExclusion" or "no additive-two infinite subsequence" not in str(audit88.get("proof_boundary", "")):
        return fail("collatz ticket88 next target or proof boundary changed")

    path89 = Path("data/open-problem/ticket89-fixed-log-golden-mean-reduction-lab.json")
    if not path89.exists():
        return fail("missing ticket89 fixed-log reduction artifact")
    ticket89 = read_json(path89)
    if ticket89.get("schema") != TICKET89_SCHEMA or ticket89.get("status") != "fixed_log_golden_mean_reduction_open_no_collatz_resolution":
        return fail("ticket89 schema or status changed")
    attempts89 = ticket89.get("attempts", [])
    by_id89 = {str(row.get("problem_id")): row for row in attempts89 if isinstance(row, dict)} if isinstance(attempts89, list) else {}
    if set(by_id89) != EXPECTED_PROBLEMS:
        return fail("ticket89 attempts missing problems")
    paths89 = {"riemann": Path("data/open-problem/riemann/rh-ticket-89-fixed-log-golden-mean-reduction.json"), "collatz": Path("data/open-problem/collatz/co-ticket-89-fixed-log-golden-mean-reduction.json"), "goldbach": Path("data/open-problem/goldbach/gb-ticket-89-fixed-log-golden-mean-reduction.json"), "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-89-fixed-log-golden-mean-reduction.json")}
    for problem_id, attempt in by_id89.items():
        if not paths89[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket89 artifact or boundary missing")
    audit89 = by_id89["collatz"].get("bounded_result", {}).get("fixed_log_golden_mean_reduction_audit", {})
    if audit89.get("theorem_name") != "FixedLogGoldenMeanValuationEquivalence" or audit89.get("theorem_status") != "fixed_log_golden_mean_reduced_exactly_no_collatz_resolution":
        return fail("collatz ticket89 theorem contract changed")
    machine89 = audit89.get("machine_audit", {})
    for key, expected in {"max_horizon": 65536, "top_bit_count": 32728, "complete_jump_pair_count": 32727, "valuation_excess_at_least_five_count": 8159, "maximum_zero_run": 16, "maximum_valuation_excess": 19, "direct_check_horizon": 1024, "total_failure_count": 0}.items():
        if int(machine89.get(key, -1)) != expected:
            return fail(f"collatz ticket89 metric {key} changed")
    if audit89.get("next_theorem_target") != "FixedLogValuationExcessFiveInfinitude" or "no additive-two infinite subsequence" not in str(audit89.get("proof_boundary", "")):
        return fail("collatz ticket89 next target or proof boundary changed")

    path90 = Path("data/open-problem/ticket90-normalized-error-ghost-lasso-lab.json")
    if not path90.exists():
        return fail("missing ticket90 normalized-error artifact")
    ticket90 = read_json(path90)
    if ticket90.get("schema") != TICKET90_SCHEMA or ticket90.get("status") != "normalized_error_ghost_lasso_open_no_collatz_resolution":
        return fail("ticket90 schema or status changed")
    attempts90 = ticket90.get("attempts", [])
    by_id90 = {str(row.get("problem_id")): row for row in attempts90 if isinstance(row, dict)} if isinstance(attempts90, list) else {}
    if set(by_id90) != EXPECTED_PROBLEMS:
        return fail("ticket90 attempts missing problems")
    paths90 = {"riemann": Path("data/open-problem/riemann/rh-ticket-90-normalized-error-ghost-lasso.json"), "collatz": Path("data/open-problem/collatz/co-ticket-90-normalized-error-ghost-lasso.json"), "goldbach": Path("data/open-problem/goldbach/gb-ticket-90-normalized-error-ghost-lasso.json"), "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-90-normalized-error-ghost-lasso.json")}
    for problem_id, attempt in by_id90.items():
        if not paths90[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket90 artifact or boundary missing")
    audit90 = by_id90["collatz"].get("bounded_result", {}).get("normalized_error_ghost_lasso_audit", {})
    if audit90.get("theorem_name") != "FixedPrecisionNormalizedErrorGhostLassoNoGo" or audit90.get("theorem_status") != "fixed_precision_error_lasso_no_go_proved_no_collatz_resolution":
        return fail("collatz ticket90 theorem contract changed")
    machine90 = audit90.get("machine_audit", {})
    for key, expected in {"max_audit_horizon": 256, "audited_transition_count": 254, "error_bits": 20, "lasso_precision_count": 63, "maximum_lasso_precision": 64, "beta_low_20": 976981, "total_failure_count": 0}.items():
        if int(machine90.get(key, -1)) != expected:
            return fail(f"collatz ticket90 metric {key} changed")
    if audit90.get("next_theorem_target") != "GrowingPrecisionErrorGhostSeparation" or "does not prove valuation-excess-five" not in str(audit90.get("proof_boundary", "")):
        return fail("collatz ticket90 next target or proof boundary changed")

    path91 = Path("data/open-problem/ticket91-error-tail-invariant-set-lab.json")
    if not path91.exists():
        return fail("missing ticket91 error-tail invariant-set artifact")
    ticket91 = read_json(path91)
    if ticket91.get("schema") != TICKET91_SCHEMA or ticket91.get("status") != "error_tail_invariant_set_open_no_collatz_resolution":
        return fail("ticket91 schema or status changed")
    attempts91 = ticket91.get("attempts", [])
    by_id91 = {str(row.get("problem_id")): row for row in attempts91 if isinstance(row, dict)} if isinstance(attempts91, list) else {}
    if set(by_id91) != EXPECTED_PROBLEMS:
        return fail("ticket91 attempts missing problems")
    paths91 = {"riemann": Path("data/open-problem/riemann/rh-ticket-91-error-tail-invariant-set.json"), "collatz": Path("data/open-problem/collatz/co-ticket-91-error-tail-invariant-set.json"), "goldbach": Path("data/open-problem/goldbach/gb-ticket-91-error-tail-invariant-set.json"), "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-91-error-tail-invariant-set.json")}
    for problem_id, attempt in by_id91.items():
        if not paths91[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket91 artifact or boundary missing")
    audit91 = by_id91["collatz"].get("bounded_result", {}).get("error_tail_invariant_set_audit", {})
    if audit91.get("theorem_name") != "NormalizedErrorTailConjugacyAndSingleGhostNoGo" or audit91.get("theorem_status") != "error_tail_conjugacy_and_single_ghost_no_go_proved_no_collatz_resolution":
        return fail("collatz ticket91 theorem contract changed")
    machine91 = audit91.get("machine_audit", {})
    for key, expected in {"max_audit_horizon": 256, "audited_horizon_count": 255, "audited_tail_transition_count": 254, "tail_bits": 20, "conjugacy_bits": 12, "conjugacy_state_count": 4096, "golden_mean_word_count": 377, "golden_mean_image_count": 377, "gamma_low_20": 71595, "beta_low_20": 976981, "total_failure_count": 0}.items():
        if int(machine91.get(key, -1)) != expected:
            return fail(f"collatz ticket91 metric {key} changed")
    if audit91.get("next_theorem_target") != "GoldenMeanInvariantSetEscape" or "does not prove 00 recurrence" not in str(audit91.get("proof_boundary", "")):
        return fail("collatz ticket91 next target or proof boundary changed")

    path92 = Path("data/open-problem/ticket92-scale-sensitive-threshold-audit.json")
    if not path92.exists():
        return fail("missing ticket92 scale-sensitive threshold artifact")
    ticket92 = read_json(path92)
    if ticket92.get("schema") != TICKET92_SCHEMA or ticket92.get("status") != "scale_sensitive_thresholds_open_no_open_problem_resolution":
        return fail("ticket92 schema or status changed")
    attempts92 = ticket92.get("attempts", [])
    by_id92 = {str(row.get("problem_id")): row for row in attempts92 if isinstance(row, dict)} if isinstance(attempts92, list) else {}
    if set(by_id92) != EXPECTED_PROBLEMS:
        return fail("ticket92 attempts missing problems")
    paths92 = {"riemann": Path("data/open-problem/riemann/rh-ticket-92-scale-sensitive-threshold.json"), "collatz": Path("data/open-problem/collatz/co-ticket-92-scale-sensitive-threshold.json"), "goldbach": Path("data/open-problem/goldbach/gb-ticket-92-scale-sensitive-threshold.json"), "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-92-scale-sensitive-threshold.json")}
    for problem_id, attempt in by_id92.items():
        if not paths92[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket92 artifact or boundary missing")
    collatz92 = by_id92["collatz"].get("bounded_result", {}).get("second_order_defect_audit", {})
    if collatz92.get("theorem_name") != "ConstantAdditiveDigitEventRequiresSecondOrderPadicDefect" or collatz92.get("theorem_status") != "second_order_defect_equivalence_and_first_order_no_go_proved_no_collatz_resolution":
        return fail("collatz ticket92 theorem contract changed")
    machine_c92 = collatz92.get("machine_audit", {})
    for key, expected in {"max_horizon": 262144, "top_bit_count": 131307, "complete_jump_pair_count": 131306, "second_order_target_event_count": 32753, "maximum_floor_defect": 17, "countermodel_bits": 4096, "countermodel_adjacent_zero_count": 0, "countermodel_maximum_defect": 2, "total_failure_count": 0}.items():
        if int(machine_c92.get(key, -1)) != expected:
            return fail(f"collatz ticket92 metric {key} changed")
    if collatz92.get("next_theorem_target") != "FixedLogSecondOrderDefectRecurrence" or "does not prove Delta_H>=3 infinitely often" not in str(collatz92.get("proof_boundary", "")):
        return fail("collatz ticket92 next target or proof boundary changed")
    twin92 = by_id92["twin-prime"].get("bounded_result", {}).get("maynard_threshold_correction", {})
    if twin92.get("theorem_name") != "MaynardCriterionThresholdAndGapPromotionCorrection" or twin92.get("theorem_status") != "maynard_threshold_misclassification_corrected_no_twin_prime_resolution":
        return fail("twin-prime ticket92 theorem contract changed")
    machine_t92 = twin92.get("machine_audit", {})
    for key, expected in {"corrected_row_count": 17, "legacy_false_gap_promotion_count": 17, "certified_M_k_row_count": 0, "certified_two_prime_row_count": 0, "remaining_implied_gap_count": 0, "total_failure_count": 0}.items():
        if int(machine_t92.get(key, -1)) != expected:
            return fail(f"twin-prime ticket92 metric {key} changed")
    if twin92.get("next_theorem_target") != "ParityBreakingExactPairCorrelationLowerBound" or "no Twin Prime result" not in str(twin92.get("proof_boundary", "")):
        return fail("twin-prime ticket92 next target or proof boundary changed")
    corrected14 = read_json(Path("data/open-problem/twin-prime/tp-cegis-14-maynard-sieve-weight.json"))
    if corrected14.get("schema") != "primeproject.twin-prime.maynard-sieve-weight-certificate.v2" or corrected14.get("smallest_bounded_gap") is not None:
        return fail("twin-prime Maynard artifact correction changed")
    maynard_rows = corrected14.get("maynard_weight_values", [])
    if not isinstance(maynard_rows, list) or any(row.get("implied_bounded_gap") is not None or row.get("maynard_two_prime_criterion_certified") for row in maynard_rows if isinstance(row, dict)):
        return fail("twin-prime Maynard artifact still promotes an uncertified gap")

    path93 = Path("data/open-problem/ticket93-twin-correlation-excess-bridge.json")
    if not path93.exists():
        return fail("missing ticket93 twin-correlation artifact")
    ticket93 = read_json(path93)
    if ticket93.get("schema") != TICKET93_SCHEMA or ticket93.get("status") != "twin_correlation_excess_open_no_twin_prime_resolution":
        return fail("ticket93 schema or status changed")
    attempts93 = ticket93.get("attempts", [])
    by_id93 = {str(row.get("problem_id")): row for row in attempts93 if isinstance(row, dict)} if isinstance(attempts93, list) else {}
    if set(by_id93) != EXPECTED_PROBLEMS:
        return fail("ticket93 attempts missing problems")
    paths93 = {"riemann": Path("data/open-problem/riemann/rh-ticket-93-correlation-excess.json"), "collatz": Path("data/open-problem/collatz/co-ticket-93-correlation-excess.json"), "goldbach": Path("data/open-problem/goldbach/gb-ticket-93-correlation-excess.json"), "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-93-correlation-excess.json")}
    for problem_id, attempt in by_id93.items():
        if not paths93[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket93 artifact or boundary missing")
    twin93 = by_id93["twin-prime"].get("bounded_result", {}).get("twin_correlation_excess_audit", {})
    if twin93.get("theorem_name") != "TwinPrimeLambdaCorrelationExcessSufficiencyAndSurrogateNoGo" or twin93.get("theorem_status") != "exact_correlation_excess_bridge_and_surrogate_no_go_proved_no_twin_prime_resolution":
        return fail("twin-prime ticket93 theorem contract changed")
    machine93 = twin93.get("machine_audit", {})
    for key, expected in {"correlation_limit": 2000000, "surrogate_limit": 200000, "checkpoint_count": 5, "final_twin_pair_count": 14871, "final_proper_prime_power_pair_count": 94, "truncation_count": 4, "decomposition_failure_count": 0, "surrogate_no_go_failure_count": 0, "total_failure_count": 0}.items():
        if int(machine93.get(key, -1)) != expected:
            return fail(f"twin-prime ticket93 metric {key} changed")
    if float(machine93.get("final_contamination", -1)) <= 0 or float(machine93.get("final_correlation_minus_bound", 1)) >= 0:
        return fail("twin-prime ticket93 finite evidence boundary changed")
    surrogate93 = twin93.get("surrogate_no_go", {})
    rows93 = surrogate93.get("rows", [])
    if not isinstance(rows93, list) or len(rows93) != 4 or any(int(row.get("pointwise_minorant_violation_count", 0)) <= 0 or int(row.get("pair_false_positive_count", 0)) <= 0 or not row.get("positive_surrogate_is_not_lower_bound") for row in rows93 if isinstance(row, dict)):
        return fail("twin-prime ticket93 surrogate no-go changed")
    if twin93.get("next_theorem_target") != "ShiftTwoTypeIICorrelationExcess" or "does not prove the required correlation lower bound" not in str(twin93.get("proof_boundary", "")):
        return fail("twin-prime ticket93 next target or proof boundary changed")

    path94 = Path("data/open-problem/ticket94-signed-remainder-and-goldbach-bridge.json")
    if not path94.exists():
        return fail("missing ticket94 signed-remainder artifact")
    ticket94 = read_json(path94)
    if ticket94.get("schema") != TICKET94_SCHEMA or ticket94.get("status") != "signed_remainder_and_goldbach_bridges_open_no_resolution":
        return fail("ticket94 schema or status changed")
    attempts94 = ticket94.get("attempts", [])
    by_id94 = {str(row.get("problem_id")): row for row in attempts94 if isinstance(row, dict)} if isinstance(attempts94, list) else {}
    if set(by_id94) != EXPECTED_PROBLEMS:
        return fail("ticket94 attempts missing problems")
    paths94 = {"riemann": Path("data/open-problem/riemann/rh-ticket-94-signed-remainder.json"), "collatz": Path("data/open-problem/collatz/co-ticket-94-signed-remainder.json"), "goldbach": Path("data/open-problem/goldbach/gb-ticket-94-signed-remainder.json"), "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-94-signed-remainder.json")}
    for problem_id, attempt in by_id94.items():
        if not paths94[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket94 artifact or boundary missing")
    twin94 = by_id94["twin-prime"].get("bounded_result", {}).get("twin_signed_remainder_audit", {})
    if twin94.get("theorem_name") != "TwinShiftTwoSignedRemainderIdentityAndNormOnlyNoGo" or twin94.get("theorem_status") != "signed_remainder_identity_and_norm_only_no_go_proved_no_twin_prime_resolution":
        return fail("twin-prime ticket94 theorem contract changed")
    machine_t94 = twin94.get("machine_audit", {})
    for key, expected in {"limit": 200000, "truncation_count": 4, "positive_norm_lower_bound_count": 0, "decomposition_failure_count": 0, "norm_route_failure_count": 0, "total_failure_count": 0}.items():
        if int(machine_t94.get(key, -1)) != expected:
            return fail(f"twin-prime ticket94 metric {key} changed")
    rows_t94 = machine_t94.get("rows", [])
    if not isinstance(rows_t94, list) or len(rows_t94) != 4 or any(float(row.get("norm_only_lower_bound", 0)) >= 0 or not row.get("norm_only_route_blocked") for row in rows_t94 if isinstance(row, dict)):
        return fail("twin-prime ticket94 norm-only no-go changed")
    if twin94.get("next_theorem_target") != "JointShiftTwoSignedRemainderLowerBound" or "does not prove the signed remainder lower bound" not in str(twin94.get("proof_boundary", "")):
        return fail("twin-prime ticket94 next target or proof boundary changed")
    gold94 = by_id94["goldbach"].get("bounded_result", {}).get("goldbach_correlation_bridge_audit", {})
    if gold94.get("theorem_name") != "GoldbachLambdaCorrelationPrimePowerContaminationBridge" or gold94.get("theorem_status") != "goldbach_correlation_contamination_bridge_proved_no_goldbach_resolution":
        return fail("goldbach ticket94 theorem contract changed")
    machine_g94 = gold94.get("machine_audit", {})
    for key, expected in {"checkpoint_count": 4, "maximum_checkpoint": 100000, "positive_certified_margin_count": 0, "decomposition_failure_count": 0, "total_failure_count": 0}.items():
        if int(machine_g94.get(key, -1)) != expected:
            return fail(f"goldbach ticket94 metric {key} changed")
    if gold94.get("next_theorem_target") != "UniformBinaryLambdaCorrelationExcess" or "does not prove the uniform lower bound" not in str(gold94.get("proof_boundary", "")):
        return fail("goldbach ticket94 next target or proof boundary changed")

    path95 = Path("data/open-problem/ticket95-sharp-contamination-and-equivalence-audit.json")
    if not path95.exists():
        return fail("missing ticket95 sharp-contamination artifact")
    ticket95 = read_json(path95)
    if ticket95.get("schema") != TICKET95_SCHEMA or ticket95.get("status") != "sharp_contamination_bridges_and_equivalence_gate_open_no_resolution":
        return fail("ticket95 schema or status changed")
    attempts95 = ticket95.get("attempts", [])
    by_id95 = {str(row.get("problem_id")): row for row in attempts95 if isinstance(row, dict)} if isinstance(attempts95, list) else {}
    if set(by_id95) != EXPECTED_PROBLEMS:
        return fail("ticket95 attempts missing problems")
    paths95 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-95-logical-novelty-gate.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-95-logical-novelty-gate.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-95-sharp-contamination.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-95-equivalence-audit.json"),
    }
    for problem_id, attempt in by_id95.items():
        if not paths95[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket95 artifact or boundary missing")

    twin95 = by_id95["twin-prime"].get("bounded_result", {}).get("twin_ticket95_audit", {})
    if twin95.get("theorem_name") != "TwinPrimePowerMassBudgetAndRemainderEquivalenceAudit" or twin95.get("theorem_status") != "sharp_prime_power_budget_and_equivalence_no_reduction_proved_no_twin_prime_resolution":
        return fail("twin-prime ticket95 theorem contract changed")
    machine_t95 = twin95.get("machine_audit", {})
    for key, expected in {"checkpoint_count": 5, "maximum_checkpoint": 200000, "budget_failure_count": 0, "equivalence_failure_count": 0, "total_failure_count": 0}.items():
        if int(machine_t95.get(key, -1)) != expected:
            return fail(f"twin-prime ticket95 metric {key} changed")
    checkpoint_t95 = machine_t95.get("checkpoint_rows", [])
    equivalence_t95 = machine_t95.get("equivalence_rows", [])
    if not isinstance(checkpoint_t95, list) or len(checkpoint_t95) != 5 or any(not row.get("sharp_bound_holds") or float(row.get("bound_improvement_factor", 0)) <= 1 for row in checkpoint_t95 if isinstance(row, dict)):
        return fail("twin-prime ticket95 sharp budget changed")
    if not isinstance(equivalence_t95, list) or len(equivalence_t95) != 4 or any(float(row.get("target_equivalence_error", 1)) > 1e-6 for row in equivalence_t95 if isinstance(row, dict)):
        return fail("twin-prime ticket95 equivalence replay changed")
    if twin95.get("next_theorem_target") != "IndependentShiftTwoCorrelationExcess" or "does not prove Twin Prime" not in str(twin95.get("proof_boundary", "")):
        return fail("twin-prime ticket95 target or boundary changed")

    gold95 = by_id95["goldbach"].get("bounded_result", {}).get("goldbach_sharp_budget_audit", {})
    if gold95.get("theorem_name") != "GoldbachProperPrimePowerMassContaminationBridge" or gold95.get("theorem_status") != "sharp_goldbach_contamination_bridge_proved_uniform_lower_bound_open":
        return fail("goldbach ticket95 theorem contract changed")
    machine_g95 = gold95.get("machine_audit", {})
    for key, expected in {"checkpoint_count": 5, "maximum_checkpoint": 1000000, "positive_sharp_margin_count": 5, "total_failure_count": 0}.items():
        if int(machine_g95.get(key, -1)) != expected:
            return fail(f"goldbach ticket95 metric {key} changed")
    screen95 = machine_g95.get("all_even_screen", {})
    for key, expected in {"screen_limit": 1000000, "even_target_count": 499999, "nonpositive_margin_count": 10, "last_nonpositive_margin_target": 38, "observed_positive_suffix_start": 40}.items():
        if int(screen95.get(key, -1)) != expected:
            return fail(f"goldbach ticket95 screen metric {key} changed")
    if not screen95.get("all_nonpositive_cases_have_goldbach_witness") or float(screen95.get("maximum_fft_direct_error", 1)) > 1e-6 or screen95.get("proof_status") != "numerical_screen_not_interval_or_symbolic_proof":
        return fail("goldbach ticket95 numerical boundary changed")
    if gold95.get("next_theorem_target") != "UniformBinaryMinorArcDominance" or "does not prove" not in str(gold95.get("proof_boundary", "")):
        return fail("goldbach ticket95 target or boundary changed")

    path96 = Path("data/open-problem/ticket96-fourier-phase-information-audit.json")
    if not path96.exists():
        return fail("missing ticket96 Fourier phase artifact")
    ticket96 = read_json(path96)
    if ticket96.get("schema") != TICKET96_SCHEMA or ticket96.get("status") != "exact_fourier_bridges_phase_blind_routes_blocked_no_resolution":
        return fail("ticket96 schema or status changed")
    attempts96 = ticket96.get("attempts", [])
    by_id96 = {str(row.get("problem_id")): row for row in attempts96 if isinstance(row, dict)} if isinstance(attempts96, list) else {}
    if set(by_id96) != EXPECTED_PROBLEMS:
        return fail("ticket96 attempts missing problems")
    paths96 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-96-spectral-phase-gate.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-96-spectrum-placement-gate.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-96-fourier-phase-audit.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-96-fourier-energy-audit.json"),
    }
    for problem_id, attempt in by_id96.items():
        if not paths96[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket96 artifact or boundary missing")
    if by_id96["goldbach"].get("bounded_result", {}).get("audit_ref") != "fourier_phase_information_audit" or by_id96["twin-prime"].get("bounded_result", {}).get("audit_ref") != "fourier_phase_information_audit":
        return fail("ticket96 shared Fourier audit references changed")
    audit96 = ticket96.get("fourier_phase_information_audit", {})
    if audit96.get("theorem_name") != "DiscreteFourierPhaseInformationAndEnergyOnlyNoGoAudit" or audit96.get("theorem_status") != "exact_dft_bridges_and_phase_blind_information_no_go_proved_no_open_problem_resolution":
        return fail("ticket96 theorem contract changed")
    machine96 = audit96.get("machine_audit", {})
    for key, expected in {"checkpoint_count": 2, "maximum_checkpoint": 100000, "configuration_count_per_checkpoint": 36, "sparse_goldbach_certificate_count": 0, "sparse_twin_certificate_count": 0, "reconstruction_failure_count": 0, "countermodel_failure_count": 0, "total_failure_count": 0}.items():
        if int(machine96.get(key, -1)) != expected:
            return fail(f"ticket96 metric {key} changed")
    if abs(float(machine96.get("sparse_mask_density_ceiling", -1)) - 0.1) > 1e-12:
        return fail("ticket96 sparse density ceiling changed")
    rows96 = machine96.get("checkpoint_rows", [])
    if not isinstance(rows96, list) or [int(row.get("target", -1)) for row in rows96 if isinstance(row, dict)] != [10000, 100000]:
        return fail("ticket96 checkpoint scales changed")
    for row in rows96:
        if not isinstance(row, dict) or int(row.get("configuration_count", -1)) != 36 or int(row.get("sparse_goldbach_certificate_count", -1)) != 0 or int(row.get("sparse_twin_certificate_count", -1)) != 0:
            return fail("ticket96 checkpoint certificate counts changed")
        if float(row.get("goldbach_dft_error", 1)) > 1e-6 or float(row.get("twin_dft_error", 1)) > 1e-6:
            return fail("ticket96 DFT reconstruction changed")
        for best_key, lower_key in (("best_sparse_goldbach_row", "goldbach_energy_only_lower_bound"), ("best_sparse_twin_row", "twin_energy_only_lower_bound")):
            best = row.get(best_key, {})
            if float(best.get("major_density", 1)) > 0.1 or float(best.get(lower_key, 0)) >= 0:
                return fail("ticket96 sparse energy no-go changed")
    countermodels96 = audit96.get("countermodel_audit", {})
    if int(countermodels96.get("failure_count", -1)) != 0:
        return fail("ticket96 countermodel audit changed")
    for problem_id in ("goldbach", "twin"):
        countermodel = countermodels96.get(problem_id, {})
        if not countermodel.get("conjugate_symmetric") or abs(float(countermodel.get("target_coefficient", 0)) + float(countermodel.get("pair_energy", 1))) > 1e-12:
            return fail(f"ticket96 {problem_id} negative-energy envelope changed")
    if audit96.get("goldbach_next_theorem_target") != "ArithmeticMinorArcPhaseCancellation" or audit96.get("twin_next_theorem_target") != "ShiftTwoSpectralLocalizationOrTypeIICancellation" or "does not prove" not in str(audit96.get("proof_boundary", "")):
        return fail("ticket96 targets or proof boundary changed")

    path97 = Path("data/open-problem/ticket97-periodic-projection-residual-audit.json")
    if not path97.exists():
        return fail("missing ticket97 periodic projection artifact")
    ticket97 = read_json(path97)
    if ticket97.get("schema") != TICKET97_SCHEMA or ticket97.get("status") != "optimal_periodic_projection_fixed_modulus_routes_blocked_no_resolution":
        return fail("ticket97 schema or status changed")
    attempts97 = ticket97.get("attempts", [])
    by_id97 = {str(row.get("problem_id")): row for row in attempts97 if isinstance(row, dict)} if isinstance(attempts97, list) else {}
    if set(by_id97) != EXPECTED_PROBLEMS:
        return fail("ticket97 attempts missing problems")
    paths97 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-97-finite-modulus-gate.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-97-finite-residue-gate.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-97-periodic-projection.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-97-periodic-projection.json"),
    }
    for problem_id, attempt in by_id97.items():
        if not paths97[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket97 artifact or boundary missing")
    if by_id97["goldbach"].get("bounded_result", {}).get("audit_ref") != "periodic_projection_residual_audit" or by_id97["twin-prime"].get("bounded_result", {}).get("audit_ref") != "periodic_projection_residual_audit":
        return fail("ticket97 shared audit references changed")
    audit97 = ticket97.get("periodic_projection_residual_audit", {})
    if audit97.get("theorem_name") != "OptimalFiniteModulusProjectionAndResidualSignNoGoAudit" or audit97.get("theorem_status") != "optimal_periodic_projection_and_fixed_modulus_sign_no_go_proved_no_resolution":
        return fail("ticket97 theorem contract changed")
    machine97 = audit97.get("machine_audit", {})
    for key, expected in {"checkpoint_count": 2, "maximum_checkpoint": 100000, "modulus_count_per_checkpoint": 5, "goldbach_certificate_count": 0, "twin_certificate_count": 0, "projection_failure_count": 0, "countermodel_failure_count": 0, "total_failure_count": 0}.items():
        if int(machine97.get(key, -1)) != expected:
            return fail(f"ticket97 metric {key} changed")
    if machine97.get("moduli") != [2, 6, 30, 210, 2310]:
        return fail("ticket97 moduli changed")
    rows97 = machine97.get("checkpoint_rows", [])
    if not isinstance(rows97, list) or [int(row.get("target", -1)) for row in rows97 if isinstance(row, dict)] != [10000, 100000]:
        return fail("ticket97 checkpoint scales changed")
    for checkpoint in rows97:
        rows = checkpoint.get("rows", [])
        if not isinstance(rows, list) or len(rows) != 5:
            return fail("ticket97 projection row count changed")
        for row in rows:
            for key in ("maximum_absolute_residue_residual_sum", "orthogonality_error", "energy_decomposition_error", "goldbach_reconstruction_error", "twin_reconstruction_error"):
                if float(row.get(key, 1)) > 1e-6:
                    return fail(f"ticket97 projection contract {key} changed")
            if float(row.get("goldbach_norm_only_lower_bound", 0)) >= 0 or float(row.get("twin_norm_only_lower_bound", 0)) >= 0 or row.get("goldbach_certified") or row.get("twin_certified"):
                return fail("ticket97 fixed-modulus no-go changed")
    countermodel97 = audit97.get("countermodel_audit", {})
    if int(countermodel97.get("failure_count", -1)) != 0 or countermodel97.get("residue_sums") != [0.0, 0.0] or float(countermodel97.get("goldbach_additive_coefficient", 0)) != -4.0 or float(countermodel97.get("twin_shift_two_coefficient", 0)) != -2.0:
        return fail("ticket97 zero-residue countermodel changed")
    if audit97.get("goldbach_next_theorem_target") != "GrowingModulusBinaryResidualCancellation" or audit97.get("twin_next_theorem_target") != "GrowingModulusShiftTwoResidualCancellation" or "does not prove" not in str(audit97.get("proof_boundary", "")):
        return fail("ticket97 targets or proof boundary changed")

    path98 = Path("data/open-problem/ticket98-growing-modulus-leakage-audit.json")
    if not path98.exists():
        return fail("missing ticket98 growing modulus leakage artifact")
    ticket98 = read_json(path98)
    if ticket98.get("schema") != TICKET98_SCHEMA or ticket98.get("status") != "growing_modulus_certificates_rejected_as_row_unique_replay_no_resolution":
        return fail("ticket98 schema or status changed")
    attempts98 = ticket98.get("attempts", [])
    by_id98 = {str(row.get("problem_id")): row for row in attempts98 if isinstance(row, dict)} if isinstance(attempts98, list) else {}
    if set(by_id98) != EXPECTED_PROBLEMS:
        return fail("ticket98 attempts missing problems")
    paths98 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-98-growing-partition-leakage.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-98-growing-residue-leakage.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-98-growing-modulus-leakage.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-98-growing-modulus-leakage.json"),
    }
    for problem_id, attempt in by_id98.items():
        if not paths98[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket98 artifact or boundary missing")
    if by_id98["goldbach"].get("bounded_result", {}).get("audit_ref") != "growing_modulus_leakage_audit" or by_id98["twin-prime"].get("bounded_result", {}).get("audit_ref") != "growing_modulus_leakage_audit":
        return fail("ticket98 shared audit references changed")
    audit98 = ticket98.get("growing_modulus_leakage_audit", {})
    if audit98.get("theorem_name") != "GrowingModulusRowUniqueLeakageAudit" or audit98.get("theorem_status") != "row_unique_leakage_theorem_proved_tested_growing_modulus_certificates_rejected_no_resolution":
        return fail("ticket98 theorem contract changed")
    identity98 = audit98.get("row_unique_identity_theorem", {})
    if "P_W x=x" not in str(identity98.get("statement", "")) or len(identity98.get("proof_steps", [])) != 4:
        return fail("ticket98 row-unique identity theorem changed")
    machine98 = audit98.get("machine_audit", {})
    for key, expected in {"checkpoint_count": 3, "maximum_checkpoint": 1000000, "modulus_count_per_checkpoint": 8, "non_row_unique_goldbach_certificate_count": 0, "non_row_unique_twin_certificate_count": 0, "row_unique_goldbach_certificate_count": 3, "row_unique_twin_certificate_count": 3, "first_certificate_mismatch_count": 0, "contract_failure_count": 0, "total_failure_count": 0}.items():
        if int(machine98.get(key, -1)) != expected:
            return fail(f"ticket98 metric {key} changed")
    if machine98.get("primorial_moduli") != [2, 6, 30, 210, 2310, 30030, 510510, 9699690]:
        return fail("ticket98 primorial chain changed")
    rows98 = machine98.get("checkpoint_rows", [])
    if not isinstance(rows98, list) or [int(row.get("target", -1)) for row in rows98 if isinstance(row, dict)] != [10000, 100000, 1000000]:
        return fail("ticket98 checkpoint scales changed")
    expected_first98 = {10000: 30030, 100000: 510510, 1000000: 9699690}
    for checkpoint in rows98:
        target = int(checkpoint.get("target", -1))
        expected_first = expected_first98.get(target)
        if checkpoint.get("first_row_unique_modulus") != expected_first or checkpoint.get("first_goldbach_certificate_modulus") != expected_first or checkpoint.get("first_twin_certificate_modulus") != expected_first:
            return fail("ticket98 first certificate no longer equals row-unique boundary")
        if int(checkpoint.get("non_row_unique_goldbach_certificate_count", -1)) != 0 or int(checkpoint.get("non_row_unique_twin_certificate_count", -1)) != 0:
            return fail("ticket98 pre-leak certificate count changed")
        rows = checkpoint.get("rows", [])
        if not isinstance(rows, list) or len(rows) != 8:
            return fail("ticket98 projection row count changed")
        for row in rows:
            for key in ("relative_orthogonality_error", "relative_energy_decomposition_error", "goldbach_reconstruction_relative_error", "twin_reconstruction_relative_error"):
                if float(row.get(key, 1)) > 1e-12:
                    return fail(f"ticket98 projection contract {key} changed")
            if row.get("row_unique_leakage") and (float(row.get("relative_residual_norm", 1)) != 0 or row.get("certificate_interpretation") != "exact_data_replay_not_independent_arithmetic_bound"):
                return fail("ticket98 row-unique replay classification changed")
    million_rows98 = next(row for row in rows98 if int(row.get("target", -1)) == 1000000).get("rows", [])
    near_unique98 = next((row for row in million_rows98 if int(row.get("modulus", -1)) == 510510), {})
    if int(near_unique98.get("maximum_samples_per_occupied_residue", -1)) != 2 or near_unique98.get("goldbach_certified") or near_unique98.get("twin_certified"):
        return fail("ticket98 near-row-unique no-certificate boundary changed")
    if audit98.get("goldbach_next_theorem_target") != "OutOfSampleGrowingModulusBinaryResidualCancellation" or audit98.get("twin_next_theorem_target") != "OutOfSampleGrowingModulusShiftTwoResidualCancellation" or "does not prove" not in str(audit98.get("proof_boundary", "")):
        return fail("ticket98 targets or proof boundary changed")

    path99 = Path("data/open-problem/ticket99-out-of-sample-local-model-audit.json")
    if not path99.exists():
        return fail("missing ticket99 out-of-sample local model artifact")
    ticket99 = read_json(path99)
    if ticket99.get("schema") != TICKET99_SCHEMA or ticket99.get("status") != "out_of_sample_and_external_local_models_audited_signed_residual_theorem_open_no_resolution":
        return fail("ticket99 schema or status changed")
    attempts99 = ticket99.get("attempts", [])
    by_id99 = {str(row.get("problem_id")): row for row in attempts99 if isinstance(row, dict)} if isinstance(attempts99, list) else {}
    if set(by_id99) != EXPECTED_PROBLEMS:
        return fail("ticket99 attempts missing problems")
    paths99 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-99-external-kernel-residual.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-99-out-of-sample-drift.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-99-external-local-residual.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-99-external-local-residual.json"),
    }
    for problem_id, attempt in by_id99.items():
        if not paths99[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket99 artifact or boundary missing")
    if by_id99["goldbach"].get("bounded_result", {}).get("audit_ref") != "out_of_sample_local_model_audit" or by_id99["twin-prime"].get("bounded_result", {}).get("audit_ref") != "out_of_sample_local_model_audit":
        return fail("ticket99 shared audit references changed")
    audit99 = ticket99.get("out_of_sample_local_model_audit", {})
    if audit99.get("theorem_name") != "OutOfSampleAndExternalLocalModelResidualAudit" or audit99.get("theorem_status") != "data_separation_and_external_local_main_proved_finite_residual_candidate_survived_no_resolution":
        return fail("ticket99 theorem contract changed")
    local99 = audit99.get("external_local_main_theorem", {})
    if "A_W(n)" not in str(local99.get("model", "")) or "d_W" not in str(local99.get("density", "")) or "CRT" not in str(local99.get("proof", "")):
        return fail("ticket99 external local-main theorem changed")
    machine99 = audit99.get("machine_audit", {})
    for key, expected in {"checkpoint_count": 3, "maximum_checkpoint": 1000000, "cross_fit_configuration_count": 120, "cross_fit_goldbach_certificate_count": 0, "cross_fit_twin_certificate_count": 0, "external_goldbach_norm_certificate_count": 0, "external_twin_norm_certificate_count": 0, "cross_fit_failure_count": 0, "external_main_failure_count": 0, "envelope_validation_failure_count": 0, "total_failure_count": 0}.items():
        if int(machine99.get(key, -1)) != expected:
            return fail(f"ticket99 metric {key} changed")
    cross99 = machine99.get("cross_fit_checkpoint_rows", [])
    if not isinstance(cross99, list) or [int(row.get("target", -1)) for row in cross99] != [10000, 100000, 1000000]:
        return fail("ticket99 cross-fit checkpoints changed")
    expected_nonempty99 = {10000: 22, 100000: 27, 1000000: 31}
    for checkpoint in cross99:
        target = int(checkpoint.get("target", -1))
        if int(checkpoint.get("configuration_count", -1)) != 40 or int(checkpoint.get("nonempty_configuration_count", -1)) != expected_nonempty99[target]:
            return fail("ticket99 cross-fit occupancy grid changed")
        for best_key in ("best_nonempty_goldbach_row", "best_nonempty_twin_row"):
            best = checkpoint.get(best_key, {})
            if int(best.get("evaluation_count", 0)) <= 0 or int(best.get("train_evaluation_overlap_count", -1)) != 0:
                return fail("ticket99 disjoint cross-fit contract changed")
    external99 = machine99.get("external_checkpoint_rows", [])
    if not isinstance(external99, list) or [int(row.get("row_count", -1)) for row in external99] != [5, 6, 7]:
        return fail("ticket99 external checkpoint grid changed")
    envelope99 = machine99.get("finite_residual_envelope_screen", {})
    if abs(float(envelope99.get("candidate_log_envelope_constant", 0)) - 1.6) > 1e-12 or envelope99.get("schedule_moduli_reached") != [2, 6, 30, 210]:
        return fail("ticket99 finite residual candidate changed")
    if int(envelope99.get("goldbach_validation_failure_count", -1)) != 0 or int(envelope99.get("twin_validation_failure_count", -1)) != 0 or float(envelope99.get("maximum_fft_direct_error", 1)) > 1e-6:
        return fail("ticket99 envelope validation changed")
    if int(envelope99.get("goldbach", {}).get("calibration_maximum_row", {}).get("number", -1)) != 2804 or int(envelope99.get("twin", {}).get("calibration_maximum_row", {}).get("number", -1)) != 1018:
        return fail("ticket99 calibration extrema changed")
    if "not_an_asymptotic_theorem" not in str(envelope99.get("status", "")):
        return fail("ticket99 finite-screen boundary changed")
    if audit99.get("goldbach_next_theorem_target") != "UniformExternalLocalModelGoldbachResidualDecay" or audit99.get("twin_next_theorem_target") != "UniformExternalLocalModelShiftTwoResidualDecay" or "does not prove" not in str(audit99.get("proof_boundary", "")):
        return fail("ticket99 targets or proof boundary changed")

    path100 = Path("data/open-problem/ticket100-extended-residual-vaughan-audit.json")
    if not path100.exists():
        return fail("missing ticket100 extended residual Vaughan artifact")
    ticket100 = read_json(path100)
    if ticket100.get("schema") != TICKET100_SCHEMA or ticket100.get("status") != "extended_residual_candidate_survived_componentwise_typeii_strategy_refuted_no_resolution":
        return fail("ticket100 schema or status changed")
    attempts100 = ticket100.get("attempts", [])
    by_id100 = {str(row.get("problem_id")): row for row in attempts100 if isinstance(row, dict)} if isinstance(attempts100, list) else {}
    if set(by_id100) != EXPECTED_PROBLEMS:
        return fail("ticket100 attempts missing problems")
    paths100 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-100-joint-component-gate.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-100-joint-drift-gate.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-100-joint-vaughan-residual.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-100-joint-vaughan-residual.json"),
    }
    for problem_id, attempt in by_id100.items():
        if not paths100[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket100 artifact or boundary missing")
    if by_id100["goldbach"].get("bounded_result", {}).get("audit_ref") != "extended_residual_vaughan_audit" or by_id100["twin-prime"].get("bounded_result", {}).get("audit_ref") != "extended_residual_vaughan_audit":
        return fail("ticket100 shared audit references changed")
    audit100 = ticket100.get("extended_residual_vaughan_audit", {})
    if audit100.get("theorem_name") != "ExtendedResidualScreenAndVaughanJointCancellationAudit" or audit100.get("theorem_status") != "extended_candidate_survived_componentwise_typeii_route_refuted_joint_theorem_open_no_resolution":
        return fail("ticket100 theorem contract changed")
    machine100 = audit100.get("machine_audit", {})
    for key, expected in {"goldbach_screen_limit": 6000000, "twin_screen_limit": 10000000, "vaughan_limit": 1000000, "total_failure_count": 0}.items():
        if int(machine100.get(key, -1)) != expected:
            return fail(f"ticket100 metric {key} changed")
    if abs(float(machine100.get("candidate_constant", 0)) - 1.6) > 1e-12:
        return fail("ticket100 candidate constant changed")
    extended100 = audit100.get("extended_counterexample_search", {})
    gold100 = extended100.get("goldbach", {})
    twin100 = extended100.get("twin", {})
    if int(gold100.get("candidate_failure_count", -1)) != 0 or int(twin100.get("candidate_failure_count", -1)) != 0:
        return fail("ticket100 extended finite candidate failed")
    if gold100.get("schedule_moduli_reached") != [2, 6, 30, 210, 2310] or twin100.get("schedule_moduli_reached") != [2, 6, 30, 210, 2310]:
        return fail("ticket100 schedule transition coverage changed")
    if int(gold100.get("overall_maximum_row", {}).get("even_target", -1)) != 2804 or int(twin100.get("overall_maximum_row", {}).get("x", -1)) != 1018 or float(gold100.get("maximum_fft_direct_error", 1)) > 1e-6:
        return fail("ticket100 extended screen extrema changed")
    vaughan100 = audit100.get("vaughan_joint_cancellation_audit", {})
    identity100 = vaughan100.get("identity", {})
    if int(identity100.get("u", -1)) != 100 or int(identity100.get("v", -1)) != 100 or float(identity100.get("direct_type_ii_max_error", 1)) > 1e-10:
        return fail("ticket100 Vaughan identity replay changed")
    gold_v100 = vaughan100.get("goldbach", {})
    twin_v100 = vaughan100.get("twin", {})
    counter100 = vaughan100.get("componentwise_no_go", {}).get("counterexample_row", {})
    if int(counter100.get("number", -1)) != 930930 or abs(float(counter100.get("required_log_envelope_constant", 0)) - 7.909937398184027) > 1e-9:
        return fail("ticket100 componentwise Type II counterexample changed")
    if not gold_v100.get("componentwise_candidate_refuted") or not gold_v100.get("joint_candidate_survives") or not twin_v100.get("joint_candidate_survives"):
        return fail("ticket100 joint/componentwise verdict changed")
    if audit100.get("goldbach_next_theorem_target") != "JointVaughanGoldbachResidualEnvelope" or audit100.get("twin_next_theorem_target") != "JointVaughanShiftTwoResidualEnvelope" or "proves none" not in str(audit100.get("proof_boundary", "")):
        return fail("ticket100 targets or proof boundary changed")

    path101 = Path("data/open-problem/ticket101-vaughan-cutoff-energy-audit.json")
    if not path101.exists():
        return fail("missing ticket101 Vaughan cutoff energy artifact")
    ticket101 = read_json(path101)
    expected_status101 = "cutoff_frontier_splits_goldbach_joint_and_twin_separate_routes_energy_rewrite_equivalent_no_resolution"
    if ticket101.get("schema") != TICKET101_SCHEMA or ticket101.get("status") != expected_status101:
        return fail("ticket101 schema or status changed")
    attempts101 = ticket101.get("attempts", [])
    by_id101 = {str(row.get("problem_id")): row for row in attempts101 if isinstance(row, dict)} if isinstance(attempts101, list) else {}
    if set(by_id101) != EXPECTED_PROBLEMS:
        return fail("ticket101 attempts missing problems")
    paths101 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-101-parameter-energy-gate.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-101-parameter-energy-gate.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-101-balanced-vaughan-frontier.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-101-balanced-vaughan-frontier.json"),
    }
    for problem_id, attempt in by_id101.items():
        if not paths101[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket101 artifact or proof boundary missing")
    if by_id101["goldbach"].get("bounded_result", {}).get("audit_ref") != "vaughan_cutoff_energy_audit" or by_id101["twin-prime"].get("bounded_result", {}).get("audit_ref") != "vaughan_cutoff_energy_audit":
        return fail("ticket101 shared audit references changed")
    audit101 = ticket101.get("vaughan_cutoff_energy_audit", {})
    if audit101.get("theorem_name") != "VaughanCutoffParetoAndEnergyEquivalenceAudit" or audit101.get("theorem_status") != "goldbach_joint_required_twin_separate_candidate_survives_energy_rewrite_equivalent_no_resolution":
        return fail("ticket101 theorem contract changed")
    machine101 = audit101.get("machine_audit", {})
    expected_metrics101 = {
        "limit": 1000000,
        "balanced_pair_count": 28,
        "balanced_goldbach_survivor_count": 0,
        "balanced_twin_survivor_count": 4,
        "energy_failure_count": 0,
        "total_failure_count": 0,
    }
    for key, expected in expected_metrics101.items():
        if int(machine101.get(key, -1)) != expected:
            return fail(f"ticket101 metric {key} changed")
    if abs(float(machine101.get("candidate_constant", 0)) - 1.6) > 1e-12:
        return fail("ticket101 candidate constant changed")
    frontier101 = audit101.get("cutoff_frontier", {})
    gold_best101 = frontier101.get("best_balanced_goldbach_row", {})
    twin_best101 = frontier101.get("best_balanced_twin_row", {})
    near101 = frontier101.get("first_tested_near_collapse_goldbach_survivor", {})
    collapse101 = frontier101.get("full_collapse_row", {})
    if (int(gold_best101.get("u", -1)), int(gold_best101.get("v", -1))) != (100, 100) or abs(float(gold_best101.get("goldbach", {}).get("separate_budget_sum", 0)) - 9.488989403518667) > 1e-9:
        return fail("ticket101 Goldbach balanced frontier changed")
    if (int(twin_best101.get("u", -1)), int(twin_best101.get("v", -1))) != (100, 84) or int(twin_best101.get("type_ii_support_count", -1)) != 244204 or abs(float(twin_best101.get("twin", {}).get("separate_budget_sum", 0)) - 1.5600494712890165) > 1e-9:
        return fail("ticket101 Twin balanced frontier changed")
    if (int(near101.get("u", -1)), int(near101.get("type_ii_support_count", -1))) != (960, 314) or int(collapse101.get("type_ii_support_count", -1)) != 0:
        return fail("ticket101 decomposition-collapse boundary changed")
    energy101 = audit101.get("energy_equivalence_audit", {})
    checkpoints101 = energy101.get("checkpoint_rows", [])
    if int(energy101.get("failure_count", -1)) != 0 or [int(row.get("target", -1)) for row in checkpoints101] != [10000, 100000, 1000000]:
        return fail("ticket101 energy replay changed")
    if "algebraically equivalent" not in str(energy101.get("novelty_verdict", "")):
        return fail("ticket101 equivalence boundary changed")
    if audit101.get("goldbach_next_theorem_target") != "JointBalancedVaughanGoldbachResidualEnvelope" or audit101.get("twin_next_theorem_target") != "SeparatedBalancedVaughanTwinBudgets" or "proves none" not in str(audit101.get("proof_boundary", "")):
        return fail("ticket101 targets or proof boundary changed")

    path102 = Path("data/open-problem/ticket102-twin-dyadic-vaughan-holdout.json")
    if not path102.exists():
        return fail("missing ticket102 Twin dyadic holdout artifact")
    ticket102 = read_json(path102)
    expected_status102 = "finite_1p40_plus_0p18_candidate_refuted_on_post_selection_holdout"
    if ticket102.get("schema") != TICKET102_SCHEMA or ticket102.get("status") != expected_status102:
        return fail("ticket102 schema or status changed")
    attempts102 = ticket102.get("attempts", [])
    by_id102 = {str(row.get("problem_id")): row for row in attempts102 if isinstance(row, dict)} if isinstance(attempts102, list) else {}
    if set(by_id102) != EXPECTED_PROBLEMS:
        return fail("ticket102 attempts missing problems")
    paths102 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-102-kernel-positivity-priority.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-102-golden-mean-priority.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-102-joint-balanced-priority.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-102-dyadic-vaughan-holdout.json"),
    }
    for problem_id, attempt in by_id102.items():
        if not paths102[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket102 artifact or proof boundary missing")
    if by_id102["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_dyadic_vaughan_holdout":
        return fail("ticket102 shared audit reference changed")
    audit102 = ticket102.get("twin_dyadic_vaughan_holdout", {})
    if audit102.get("theorem_name") != "DyadicScaleLocalSeparatedVaughanTwinBudgetAudit" or audit102.get("registered_candidate_status") != expected_status102:
        return fail("ticket102 theorem contract changed")
    machine102 = audit102.get("machine_audit", {})
    expected_metrics102 = {
        "maximum_horizon": 8000000,
        "holdout_evaluated_count": 3000000,
        "holdout_structured_failure_count": 1000000,
        "holdout_type_ii_failure_count": 0,
        "fresh_rescue_evaluated_count": 4000000,
        "fresh_rescue_failure_count": 0,
        "noncollapse_failure_count": 0,
        "contract_failure_count": 0,
    }
    for key, expected in expected_metrics102.items():
        if int(machine102.get(key, -1)) != expected:
            return fail(f"ticket102 metric {key} changed")
    dyadic102 = audit102.get("dyadic_holdout_audit", {})
    rows102 = dyadic102.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows102] != [125000, 250000, 500000, 1000000, 2000000, 4000000]:
        return fail("ticket102 dyadic schedule changed")
    row2m102 = next((row for row in rows102 if int(row.get("horizon", -1)) == 2000000), {})
    if int(row2m102.get("structured", {}).get("failure_count", -1)) != 1000000 or abs(float(row2m102.get("structured", {}).get("maximum_row", {}).get("required_log_envelope_constant", 0)) - 1.9531717027269588) > 1e-9:
        return fail("ticket102 registered-budget counterexample changed")
    rescue102 = audit102.get("fresh_rescue_holdout", {})
    rescue_row102 = rescue102.get("row", {})
    if rescue102.get("status") != "coarse_finite_budget_survives_fresh_8m_holdout_not_a_theorem" or int(rescue102.get("failure_count", -1)) != 0:
        return fail("ticket102 fresh rescue verdict changed")
    if abs(float(rescue_row102.get("structured", {}).get("maximum_row", {}).get("required_log_envelope_constant", 0)) - 3.3067939659717025) > 1e-9 or abs(float(rescue_row102.get("type_ii_support_fraction", 0)) - 0.2431389696076288) > 1e-12:
        return fail("ticket102 fresh rescue extrema changed")
    correction102 = audit102.get("constant_threshold_correction", {})
    if "not a mathematical sufficiency threshold" not in str(correction102.get("finding", "")) or "any fixed finite" not in str(correction102.get("exact_implication", "")):
        return fail("ticket102 finite-constant correction changed")
    if audit102.get("next_theorem_target") != "UniformFiniteDyadicSeparatedVaughanTwinBudgets" or "proves neither" not in str(audit102.get("proof_boundary", "")):
        return fail("ticket102 target or proof boundary changed")

    path103 = Path("data/open-problem/ticket103-twin-local-block-audit.json")
    if not path103.exists():
        return fail("missing ticket103 Twin local-block artifact")
    ticket103 = read_json(path103)
    expected_status103 = "universal_local_type_ii_nonnegativity_refuted_eventual_finite_bound_open"
    if ticket103.get("schema") != TICKET103_SCHEMA or ticket103.get("status") != expected_status103:
        return fail("ticket103 schema or status changed")
    attempts103 = ticket103.get("attempts", [])
    by_id103 = {str(row.get("problem_id")): row for row in attempts103 if isinstance(row, dict)} if isinstance(attempts103, list) else {}
    if set(by_id103) != EXPECTED_PROBLEMS:
        return fail("ticket103 attempts missing problems")
    paths103 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-103-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-103-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-103-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-103-local-block-audit.json"),
    }
    for problem_id, attempt in by_id103.items():
        if not paths103[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket103 artifact or proof boundary missing")
    if by_id103["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_local_block_audit":
        return fail("ticket103 shared audit reference changed")
    audit103 = ticket103.get("twin_local_block_audit", {})
    if audit103.get("theorem_name") != "DyadicLocalVaughanTwinBlockAudit" or audit103.get("cumulative_to_local_verdict") != expected_status103:
        return fail("ticket103 theorem contract changed")
    machine103 = audit103.get("machine_audit", {})
    expected_metrics103 = {
        "maximum_horizon": 8000000,
        "evaluated_integer_count": 7937500,
        "negative_type_ii_block_count": 0,
        "small_sign_negative_block_count": 1,
        "contract_failure_count": 0,
    }
    for key, expected in expected_metrics103.items():
        if int(machine103.get(key, -1)) != expected:
            return fail(f"ticket103 metric {key} changed")
    local103 = audit103.get("local_block_audit", {})
    rows103 = local103.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows103] != [125000, 250000, 500000, 1000000, 2000000, 4000000, 8000000]:
        return fail("ticket103 principal block schedule changed")
    if abs(float(local103.get("maximum_structured_required_constant", 0)) - 3.761663395991693) > 1e-9 or abs(float(local103.get("maximum_joint_required_constant", 0)) - 0.6429809026661759) > 1e-9:
        return fail("ticket103 principal block extrema changed")
    oracle103 = audit103.get("small_scale_sign_oracle", {})
    counter103 = oracle103.get("first_counterexample", {})
    if int(oracle103.get("negative_block_count", -1)) != 1 or int(counter103.get("horizon", -1)) != 1000:
        return fail("ticket103 Type II sign counterexample changed")
    if abs(float(counter103.get("type_ii_local_correlation", 0)) + 174.71647147792515) > 1e-9 or abs(float(counter103.get("type_ii_required_constant", 0)) - 1.7515082132270579) > 1e-9:
        return fail("ticket103 Type II counterexample values changed")
    if audit103.get("next_theorem_target") != "UniformDyadicLocalVaughanTwinBlockBudgets" or "proves neither" not in str(audit103.get("proof_boundary", "")):
        return fail("ticket103 target or proof boundary changed")

    path104 = Path("data/open-problem/ticket104-twin-typeii-mobius-anatomy.json")
    if not path104.exists():
        return fail("missing ticket104 Twin Type II anatomy artifact")
    ticket104 = read_json(path104)
    expected_status104 = "weighted_mobius_identity_exact_abel_triangle_route_refuted_open"
    if ticket104.get("schema") != TICKET104_SCHEMA or ticket104.get("status") != expected_status104:
        return fail("ticket104 schema or status changed")
    attempts104 = ticket104.get("attempts", [])
    by_id104 = {str(row.get("problem_id")): row for row in attempts104 if isinstance(row, dict)} if isinstance(attempts104, list) else {}
    if set(by_id104) != EXPECTED_PROBLEMS:
        return fail("ticket104 attempts missing problems")
    paths104 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-104-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-104-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-104-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-104-typeii-mobius-anatomy.json"),
    }
    for problem_id, attempt in by_id104.items():
        if not paths104[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket104 artifact or proof boundary missing")
    if by_id104["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_typeii_mobius_anatomy":
        return fail("ticket104 shared audit reference changed")
    audit104 = ticket104.get("twin_typeii_mobius_anatomy", {})
    if audit104.get("theorem_name") != "ExactTypeIIOuterMobiusAnatomyAndAbelNoGoAudit":
        return fail("ticket104 theorem contract changed")
    machine104 = audit104.get("machine_audit", {})
    if {key: int(machine104.get(key, -1)) for key in ("maximum_horizon", "row_count", "contract_failure_count")} != {"maximum_horizon": 2000000, "row_count": 4, "contract_failure_count": 0}:
        return fail("ticket104 machine metrics changed")
    rows104 = audit104.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows104] != [1000, 125000, 1000000, 2000000]:
        return fail("ticket104 horizon schedule changed")
    if max(float(row.get("outer_identity_absolute_error", 1)) for row in rows104) > 1e-7 or max(float(row.get("abel_reconstruction_absolute_error", 1)) for row in rows104) > 1e-7:
        return fail("ticket104 exact identities changed")
    row1000_104 = rows104[0]
    row2m_104 = rows104[-1]
    if abs(float(row1000_104.get("actual_required_constant", 0)) - 1.751508213227058) > 1e-9 or abs(float(row1000_104.get("abel_triangle_required_constant", 0)) - 61.82892746681642) > 1e-9:
        return fail("ticket104 small negative row changed")
    if abs(float(row2m_104.get("negative_mass_required_constant", 0)) - 39.91812891132201) > 1e-9 or abs(float(row2m_104.get("abel_triangle_required_constant", 0)) - 1088.1498317605888) > 1e-9:
        return fail("ticket104 lossy-bound extrema changed")
    if audit104.get("next_theorem_target") != "WeightedMobiusShiftedPrimeDyadicCancellation" or "proves none" not in str(audit104.get("proof_boundary", "")):
        return fail("ticket104 target or proof boundary changed")

    path105 = Path("data/open-problem/ticket105-twin-centered-progression-discrepancy.json")
    if not path105.exists():
        return fail("missing ticket105 centered progression artifact")
    ticket105 = read_json(path105)
    expected_status105 = "progression_centering_exact_full_vector_envelopes_insufficient_open"
    if ticket105.get("schema") != TICKET105_SCHEMA or ticket105.get("status") != expected_status105:
        return fail("ticket105 schema or status changed")
    attempts105 = ticket105.get("attempts", [])
    by_id105 = {str(row.get("problem_id")): row for row in attempts105 if isinstance(row, dict)} if isinstance(attempts105, list) else {}
    if set(by_id105) != EXPECTED_PROBLEMS:
        return fail("ticket105 attempts missing problems")
    paths105 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-105-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-105-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-105-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-105-centered-progression-discrepancy.json"),
    }
    for problem_id, attempt in by_id105.items():
        if not paths105[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket105 artifact or proof boundary missing")
    if by_id105["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_centered_progression_discrepancy":
        return fail("ticket105 shared audit reference changed")
    audit105 = ticket105.get("twin_centered_progression_discrepancy", {})
    machine105 = audit105.get("machine_audit", {})
    if audit105.get("theorem_name") != "CenteredProgressionTypeIIDiscrepancyAudit" or {key: int(machine105.get(key, -1)) for key in ("maximum_horizon", "row_count", "contract_failure_count")} != {"maximum_horizon": 2000000, "row_count": 4, "contract_failure_count": 0}:
        return fail("ticket105 theorem or machine contract changed")
    rows105 = audit105.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows105] != [1000, 125000, 1000000, 2000000] or max(float(row.get("centered_identity_absolute_error", 1)) for row in rows105) > 1e-7:
        return fail("ticket105 centered identity schedule changed")
    row2m_105 = rows105[-1]
    if abs(float(row2m_105.get("negative_centered_mass_required_constant", 0)) - 5.411964367928027) > 1e-9 or abs(float(row2m_105.get("cauchy_centered_required_constant", 0)) - 41.147064309511606) > 1e-9:
        return fail("ticket105 centered envelope extrema changed")
    if audit105.get("next_theorem_target") != "MobiusWeightedPrimeProgressionDiscrepancyBound" or "proves none" not in str(audit105.get("proof_boundary", "")):
        return fail("ticket105 target or proof boundary changed")

    path106 = Path("data/open-problem/ticket106-twin-modulus-grouped-dispersion.json")
    if not path106.exists():
        return fail("missing ticket106 modulus-grouped dispersion artifact")
    ticket106 = read_json(path106)
    expected_status106 = "modulus_grouping_exact_dispersion_theorem_open"
    if ticket106.get("schema") != TICKET106_SCHEMA or ticket106.get("status") != expected_status106:
        return fail("ticket106 schema or status changed")
    attempts106 = ticket106.get("attempts", [])
    by_id106 = {str(row.get("problem_id")): row for row in attempts106 if isinstance(row, dict)} if isinstance(attempts106, list) else {}
    if set(by_id106) != EXPECTED_PROBLEMS:
        return fail("ticket106 attempts missing problems")
    paths106 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-106-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-106-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-106-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-106-modulus-grouped-dispersion.json"),
    }
    for problem_id, attempt in by_id106.items():
        if not paths106[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket106 artifact or proof boundary missing")
    if by_id106["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_modulus_grouped_dispersion":
        return fail("ticket106 shared audit reference changed")
    audit106 = ticket106.get("twin_modulus_grouped_dispersion", {})
    machine106 = audit106.get("machine_audit", {})
    if audit106.get("theorem_name") != "GroupedModulusCenteredDispersionAudit" or {key: int(machine106.get(key, -1)) for key in ("maximum_horizon", "row_count", "contract_failure_count")} != {"maximum_horizon": 2000000, "row_count": 4, "contract_failure_count": 0}:
        return fail("ticket106 theorem or machine contract changed")
    rows106 = audit106.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows106] != [1000, 125000, 1000000, 2000000] or max(float(row.get("centered_identity_absolute_error", 1)) for row in rows106) > 1e-7:
        return fail("ticket106 grouped identity schedule changed")
    row2m_106 = rows106[-1]
    if abs(float(row2m_106.get("grouped_cauchy_required_constant", 0)) - 249.11924209715178) > 1e-9 or abs(float(row2m_106.get("outer_d_cauchy_required_constant", 0)) - 41.147064309511606) > 1e-9:
        return fail("ticket106 grouped envelope extrema changed")
    if int(row2m_106.get("row_unique_support_count", -1)) != 400315 or abs(float(row2m_106.get("row_unique_support_fraction", 0)) - 0.7231345615743258) > 1e-12:
        return fail("ticket106 sparse-cell support changed")
    if abs(float(row2m_106.get("row_unique_signed_contribution", 0)) - 64933.82659062814) > 1e-7 or abs(float(row2m_106.get("grouped_centered_discrepancy", 0)) - 67608.76030549759) > 1e-7:
        return fail("ticket106 sparse-cell contribution changed")
    if audit106.get("next_theorem_target") != "NonSparseModulusTwinDispersionWithSparseTailControl" or "proves none" not in str(audit106.get("proof_boundary", "")):
        return fail("ticket106 target or proof boundary changed")

    path107 = Path("data/open-problem/ticket107-twin-sparse-tail-recombination.json")
    if not path107.exists():
        return fail("missing ticket107 sparse-tail recombination artifact")
    ticket107 = read_json(path107)
    expected_status107 = "sparse_tail_sign_shortcut_refuted_joint_absorption_theorem_open"
    if ticket107.get("schema") != TICKET107_SCHEMA or ticket107.get("status") != expected_status107:
        return fail("ticket107 schema or status changed")
    attempts107 = ticket107.get("attempts", [])
    by_id107 = {str(row.get("problem_id")): row for row in attempts107 if isinstance(row, dict)} if isinstance(attempts107, list) else {}
    if set(by_id107) != EXPECTED_PROBLEMS:
        return fail("ticket107 attempts missing problems")
    paths107 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-107-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-107-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-107-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-107-sparse-tail-recombination.json"),
    }
    for problem_id, attempt in by_id107.items():
        if not paths107[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket107 artifact or proof boundary missing")
    if by_id107["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_sparse_tail_recombination":
        return fail("ticket107 shared audit reference changed")
    audit107 = ticket107.get("twin_sparse_tail_recombination", {})
    machine107 = audit107.get("machine_audit", {})
    if audit107.get("theorem_name") != "SparseTailVaughanRecombinationAudit" or {key: int(machine107.get(key, -1)) for key in ("maximum_horizon", "row_count", "centered_sparse_sign_count", "contract_failure_count")} != {"maximum_horizon": 8000000, "row_count": 6, "centered_sparse_sign_count": 2, "contract_failure_count": 0}:
        return fail("ticket107 theorem or machine contract changed")
    rows107 = audit107.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows107] != [1000, 125000, 1000000, 2000000, 4000000, 8000000]:
        return fail("ticket107 horizon schedule changed")
    if max(float(row.get("sparse_shifted_q_to_n_absolute_error", 1)) for row in rows107) > 1e-7 or max(float(row.get("type_ii_q_to_vaughan_max_error", 1)) for row in rows107) > 1e-9 or max(float(row.get("joint_correlation_absolute_error", 1)) for row in rows107) > 1e-7:
        return fail("ticket107 recombination identity changed")
    row8m_107 = rows107[-1]
    if {key: int(row8m_107.get(key, -1)) for key in ("sparse_q_support_count", "sparse_n_support_count", "sparse_n_collision_count", "maximum_sparse_q_multiplicity_per_n")} != {"sparse_q_support_count": 1589098, "sparse_n_support_count": 1099268, "sparse_n_collision_count": 247461, "maximum_sparse_q_multiplicity_per_n": 2}:
        return fail("ticket107 q-to-n support geometry changed")
    if abs(float(row8m_107.get("n_grouping_l1_retention", 0)) - 0.6953433186036189) > 1e-12:
        return fail("ticket107 q-to-n L1 retention changed")
    if abs(float(row8m_107.get("structured_sparse_required_constant", 0)) - 2.5889102044208583) > 1e-9 or abs(float(row8m_107.get("joint_required_constant", 0)) - 0.36905581676567056) > 1e-9:
        return fail("ticket107 component budget frontier changed")
    if audit107.get("next_theorem_target") != "JointStructuredSparseDenseTwinDispersion" or "proves none" not in str(audit107.get("proof_boundary", "")):
        return fail("ticket107 target or proof boundary changed")

    path108 = Path("data/open-problem/ticket108-twin-joint-equivalence-smoothing.json")
    if not path108.exists():
        return fail("missing ticket108 joint-equivalence smoothing artifact")
    ticket108 = read_json(path108)
    expected_status108 = "joint_target_equivalent_smoothed_excess_bridge_open"
    if ticket108.get("schema") != TICKET108_SCHEMA or ticket108.get("status") != expected_status108:
        return fail("ticket108 schema or status changed")
    attempts108 = ticket108.get("attempts", [])
    by_id108 = {str(row.get("problem_id")): row for row in attempts108 if isinstance(row, dict)} if isinstance(attempts108, list) else {}
    if set(by_id108) != EXPECTED_PROBLEMS:
        return fail("ticket108 attempts missing problems")
    paths108 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-108-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-108-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-108-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-108-joint-equivalence-smoothing.json"),
    }
    for problem_id, attempt in by_id108.items():
        if not paths108[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket108 artifact or proof boundary missing")
    if by_id108["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_joint_equivalence_smoothing":
        return fail("ticket108 shared audit reference changed")
    audit108 = ticket108.get("twin_joint_equivalence_smoothing", {})
    machine108 = audit108.get("machine_audit", {})
    expected_metrics108 = {"maximum_horizon": 8000000, "row_count": 6, "smoothing_improvement_count": 2, "smoothing_worsening_count": 4, "contract_failure_count": 0}
    if audit108.get("theorem_name") != "JointResidualEquivalenceAndSmoothedExcessBridge" or {key: int(machine108.get(key, -1)) for key in expected_metrics108} != expected_metrics108:
        return fail("ticket108 theorem or machine contract changed")
    rows108 = audit108.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows108] != [1000, 125000, 1000000, 2000000, 4000000, 8000000]:
        return fail("ticket108 horizon schedule changed")
    if max(float(row.get("hard_joint_equivalence_absolute_error", 1)) for row in rows108) > 1e-7 or max(float(row.get("smooth_joint_equivalence_absolute_error", 1)) for row in rows108) > 1e-7 or max(float(row.get("type_ii_q_to_vaughan_max_error", 1)) for row in rows108) > 1e-9:
        return fail("ticket108 equivalence identity changed")
    if any(not bool(row.get("smooth_contamination_bound_holds")) for row in rows108):
        return fail("ticket108 contamination contract changed")
    row8m_108 = rows108[-1]
    if abs(float(row8m_108.get("hard_joint_required_constant", 0)) - 0.36905581676567056) > 1e-9 or abs(float(row8m_108.get("smooth_joint_required_constant", 0)) - 0.4226078109966721) > 1e-9:
        return fail("ticket108 hard-smooth frontier changed")
    if audit108.get("next_theorem_target") != "SmoothedShiftTwoTypeIICorrelationExcess" or "does not prove" not in str(audit108.get("proof_boundary", "")):
        return fail("ticket108 target or proof boundary changed")

    path109 = Path("data/open-problem/ticket109-twin-spectral-phase-audit.json")
    if not path109.exists():
        return fail("missing ticket109 spectral-phase artifact")
    ticket109 = read_json(path109)
    expected_status109 = "spectral_identity_exact_low_frequency_route_refuted_rational_arc_theorem_open"
    if ticket109.get("schema") != TICKET109_SCHEMA or ticket109.get("status") != expected_status109:
        return fail("ticket109 schema or status changed")
    attempts109 = ticket109.get("attempts", [])
    by_id109 = {str(row.get("problem_id")): row for row in attempts109 if isinstance(row, dict)} if isinstance(attempts109, list) else {}
    if set(by_id109) != EXPECTED_PROBLEMS:
        return fail("ticket109 attempts missing problems")
    paths109 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-109-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-109-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-109-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-109-spectral-phase-audit.json"),
    }
    for problem_id, attempt in by_id109.items():
        if not paths109[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket109 artifact or proof boundary missing")
    if by_id109["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_spectral_phase_audit":
        return fail("ticket109 shared audit reference changed")
    audit109 = ticket109.get("twin_spectral_phase_audit", {})
    machine109 = audit109.get("machine_audit", {})
    expected_metrics109 = {"maximum_horizon": 1048576, "row_count": 4, "low_frequency_refutation_count": 4, "contract_failure_count": 0}
    if audit109.get("theorem_name") != "SymmetricBumpSpectralPhaseAndLowFrequencyNoGo" or {key: int(machine109.get(key, -1)) for key in expected_metrics109} != expected_metrics109:
        return fail("ticket109 theorem or machine contract changed")
    rows109 = audit109.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows109] != [4096, 32768, 262144, 1048576]:
        return fail("ticket109 horizon schedule changed")
    if max(float(row.get("spectral_identity_absolute_error", 1)) for row in rows109) > 1e-6 or any(not bool(row.get("low_frequency_only_route_refuted")) for row in rows109):
        return fail("ticket109 spectral identity or no-go changed")
    row1m_109 = rows109[-1]
    if abs(float(row1m_109.get("phase_cancellation_ratio", 0)) - 0.14349856934226232) > 1e-12 or abs(float(row1m_109.get("best_low_frequency_lower_bound", 0)) + 3338010.570271939) > 1e-6:
        return fail("ticket109 phase frontier changed")
    if audit109.get("next_theorem_target") != "RamanujanMajorArcPhaseMarginWithMinorArcControl" or "proves none" not in str(audit109.get("proof_boundary", "")):
        return fail("ticket109 target or proof boundary changed")

    path110 = Path("data/open-problem/ticket110-twin-rational-arc-budget.json")
    if not path110.exists():
        return fail("missing ticket110 rational-arc artifact")
    ticket110 = read_json(path110)
    expected_status110 = "rational_arc_partition_exact_trivial_minor_bound_refuted_open"
    if ticket110.get("schema") != TICKET110_SCHEMA or ticket110.get("status") != expected_status110:
        return fail("ticket110 schema or status changed")
    attempts110 = ticket110.get("attempts", [])
    by_id110 = {str(row.get("problem_id")): row for row in attempts110 if isinstance(row, dict)} if isinstance(attempts110, list) else {}
    if set(by_id110) != EXPECTED_PROBLEMS:
        return fail("ticket110 attempts missing problems")
    paths110 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-110-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-110-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-110-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-110-rational-arc-budget.json"),
    }
    for problem_id, attempt in by_id110.items():
        if not paths110[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket110 artifact or proof boundary missing")
    if by_id110["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_rational_arc_budget":
        return fail("ticket110 shared audit reference changed")
    audit110 = ticket110.get("twin_rational_arc_budget", {})
    machine110 = audit110.get("machine_audit", {})
    expected_metrics110 = {"maximum_horizon": 1048576, "row_count": 4, "cutoff_count": 8, "trivial_minor_refutation_count": 4, "contract_failure_count": 0}
    if audit110.get("theorem_name") != "RationalMajorArcPartitionAndTrivialMinorNoGo" or {key: int(machine110.get(key, -1)) for key in expected_metrics110} != expected_metrics110:
        return fail("ticket110 theorem or machine contract changed")
    rows110 = audit110.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows110] != [4096, 32768, 262144, 1048576] or any(not bool(row.get("trivial_minor_bound_route_refuted")) for row in rows110):
        return fail("ticket110 horizon or no-go schedule changed")
    row1m_110 = rows110[-1]
    if int(row1m_110.get("best_denominator_cutoff", -1)) != 32 or abs(float(row1m_110.get("best_major_phase_contribution", 0)) - 461203.6226842761) > 1e-6 or abs(float(row1m_110.get("best_minor_phase_contribution", 0)) + 2063.711506365915) > 1e-6:
        return fail("ticket110 major-minor frontier changed")
    if audit110.get("next_theorem_target") != "FixedBumpMajorArcAsymptoticWithTypeIIMinorPowerSaving" or "proves none" not in str(audit110.get("proof_boundary", "")):
        return fail("ticket110 target or proof boundary changed")

    path111 = Path("data/open-problem/ticket111-twin-typeii-minor-phase-audit.json")
    if not path111.exists():
        return fail("missing ticket111 Type II minor-phase artifact")
    ticket111 = read_json(path111)
    expected_status111 = "typeii_cross_spectrum_exact_phase_blind_partition_refuted_candidate_survives_holdout_open"
    if ticket111.get("schema") != TICKET111_SCHEMA or ticket111.get("status") != expected_status111:
        return fail("ticket111 schema or status changed")
    attempts111 = ticket111.get("attempts", [])
    by_id111 = {str(row.get("problem_id")): row for row in attempts111 if isinstance(row, dict)} if isinstance(attempts111, list) else {}
    if set(by_id111) != EXPECTED_PROBLEMS:
        return fail("ticket111 attempts missing problems")
    paths111 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-111-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-111-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-111-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-111-typeii-minor-phase-audit.json"),
    }
    for problem_id, attempt in by_id111.items():
        if not paths111[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket111 artifact or proof boundary missing")
    if by_id111["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_typeii_minor_phase_audit":
        return fail("ticket111 shared audit reference changed")
    audit111 = ticket111.get("twin_typeii_minor_phase_audit", {})
    machine111 = audit111.get("machine_audit", {})
    expected_metrics111 = {
        "maximum_horizon": 2097152,
        "row_count": 5,
        "calibration_row_count": 4,
        "holdout_row_count": 1,
        "phase_blind_refutation_count": 5,
        "holdout_candidate_failure_count": 0,
        "contract_failure_count": 0,
    }
    if audit111.get("theorem_name") != "ExactVaughanMinorCrossSpectrumAndPhaseBlindPartitionNoGo" or {key: int(machine111.get(key, -1)) for key in expected_metrics111} != expected_metrics111:
        return fail("ticket111 theorem or machine contract changed")
    rows111 = audit111.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows111] != [4096, 32768, 262144, 1048576, 2097152]:
        return fail("ticket111 horizon schedule changed")
    if any(not bool(row.get("phase_blind_route_refuted")) for row in rows111):
        return fail("ticket111 phase-blind no-go changed")
    if max(float(row.get("component_reconstruction_error", 1)) for row in rows111) > 1e-6 or max(float(row.get("minor_component_reconstruction_error", 1)) for row in rows111) > 1e-6:
        return fail("ticket111 component identity changed")
    holdout111 = rows111[-1]
    if holdout111.get("split") != "post_selection_holdout" or not bool(holdout111.get("registered_lower_inequality_passes")) or not bool(holdout111.get("registered_positivity_closes")):
        return fail("ticket111 holdout candidate changed")
    if abs(float(holdout111.get("phase_blind_lower_bound", 0)) + 6667225.373005189) > 1e-6 or abs(float(holdout111.get("registered_power_saving_lower_bound", 0)) - 257818.1696008843) > 1e-6:
        return fail("ticket111 quantitative frontier changed")
    if audit111.get("next_theorem_target") != "PhaseAwareVaughanTypeIIMinorArcPowerSaving" or "proves none" not in str(audit111.get("proof_boundary", "")):
        return fail("ticket111 target or proof boundary changed")

    path112 = Path("data/open-problem/ticket112-twin-farey-endpoint-abel-audit.json")
    if not path112.exists():
        return fail("missing ticket112 Farey endpoint artifact")
    ticket112 = read_json(path112)
    expected_status112 = "farey_abel_exact_endpoint_triangle_refuted_inherited_candidate_survives_open"
    if ticket112.get("schema") != TICKET112_SCHEMA or ticket112.get("status") != expected_status112:
        return fail("ticket112 schema or status changed")
    attempts112 = ticket112.get("attempts", [])
    by_id112 = {str(row.get("problem_id")): row for row in attempts112 if isinstance(row, dict)} if isinstance(attempts112, list) else {}
    if set(by_id112) != EXPECTED_PROBLEMS:
        return fail("ticket112 attempts missing problems")
    paths112 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-112-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-112-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-112-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-112-farey-endpoint-abel-audit.json"),
    }
    for problem_id, attempt in by_id112.items():
        if not paths112[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket112 artifact or proof boundary missing")
    if by_id112["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_farey_endpoint_abel_audit":
        return fail("ticket112 shared audit reference changed")
    audit112 = ticket112.get("twin_farey_endpoint_abel_audit", {})
    machine112 = audit112.get("machine_audit", {})
    expected_metrics112 = {
        "maximum_horizon": 2097152,
        "row_count": 5,
        "minor_cell_count": 162,
        "endpoint_triangle_refutation_count": 5,
        "holdout_candidate_failure_count": 0,
        "contract_failure_count": 0,
    }
    if audit112.get("theorem_name") != "ExactFareyCellAbelDecompositionAndEndpointTriangleNoGo" or {key: int(machine112.get(key, -1)) for key in expected_metrics112} != expected_metrics112:
        return fail("ticket112 theorem or machine contract changed")
    rows112 = audit112.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows112] != [4096, 32768, 262144, 1048576, 2097152]:
        return fail("ticket112 horizon schedule changed")
    if any(not bool(row.get("farey_abel_route_refuted")) for row in rows112):
        return fail("ticket112 endpoint-triangle no-go changed")
    if max(float(row.get("abel_identity_absolute_error", 1)) for row in rows112) > 1e-6 or any(int(row.get("minor_cell_count", -1)) != 162 for row in rows112):
        return fail("ticket112 Abel identity changed")
    holdout112 = rows112[-1]
    if holdout112.get("split") != "post_selection_holdout" or not bool(holdout112.get("inherited_endpoint_inequality_passes")) or not bool(holdout112.get("inherited_positivity_closes")):
        return fail("ticket112 inherited candidate changed")
    if abs(float(holdout112.get("farey_abel_lower_bound", 0)) + 351106.38706108497) > 1e-6 or abs(float(holdout112.get("inherited_lower_bound", 0)) - 770014.5783472147) > 1e-6:
        return fail("ticket112 quantitative frontier changed")
    if audit112.get("next_theorem_target") != "UniformFareyCellEndpointCancellationForVaughanCrossSpectrum" or "proves none" not in str(audit112.get("proof_boundary", "")):
        return fail("ticket112 target or proof boundary changed")

    path113 = Path("data/open-problem/ticket113-twin-farey-denominator-endpoint-audit.json")
    if not path113.exists():
        return fail("missing ticket113 Farey denominator artifact")
    ticket113 = read_json(path113)
    expected_status113 = "right_denominator_grouping_exact_new_holdout_finite_closure_open"
    if ticket113.get("schema") != TICKET113_SCHEMA or ticket113.get("status") != expected_status113:
        return fail("ticket113 schema or status changed")
    attempts113 = ticket113.get("attempts", [])
    by_id113 = {str(row.get("problem_id")): row for row in attempts113 if isinstance(row, dict)} if isinstance(attempts113, list) else {}
    if set(by_id113) != EXPECTED_PROBLEMS:
        return fail("ticket113 attempts missing problems")
    paths113 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-113-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-113-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-113-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-113-farey-denominator-endpoint-audit.json"),
    }
    for problem_id, attempt in by_id113.items():
        if not paths113[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket113 artifact or proof boundary missing")
    if by_id113["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_farey_denominator_endpoint_audit":
        return fail("ticket113 shared audit reference changed")
    audit113 = ticket113.get("twin_farey_denominator_endpoint_audit", {})
    machine113 = audit113.get("machine_audit", {})
    expected_metrics113 = {
        "maximum_horizon": 4194304,
        "row_count": 6,
        "calibration_row_count": 5,
        "holdout_row_count": 1,
        "minor_cell_count": 162,
        "right_denominator_group_count": 31,
        "finite_closure_count": 6,
        "magnitude_label_adversary_refutation_count": 6,
        "holdout_closure_failure_count": 0,
        "contract_failure_count": 0,
    }
    if audit113.get("theorem_name") != "ExactRightFareyDenominatorEndpointGroupingAndMagnitudeLabelNoGo" or {key: int(machine113.get(key, -1)) for key in expected_metrics113} != expected_metrics113:
        return fail("ticket113 theorem or machine contract changed")
    rows113 = audit113.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows113] != [4096, 32768, 262144, 1048576, 2097152, 4194304]:
        return fail("ticket113 horizon schedule changed")
    if any(not bool(row.get("grouped_triangle_closes_finite")) for row in rows113) or any(not bool(row.get("magnitude_label_adversary_refutes_closure")) for row in rows113):
        return fail("ticket113 finite closure or adversary no-go changed")
    if max(float(row.get("abel_identity_absolute_error", 1)) for row in rows113) > 1e-5 or max(float(row.get("denominator_group_identity_absolute_error", 1)) for row in rows113) > 1e-5:
        return fail("ticket113 exact identities changed")
    holdout113 = rows113[-1]
    if holdout113.get("split") != "post_selection_holdout" or int(holdout113.get("right_denominator_group_count", -1)) != 31:
        return fail("ticket113 holdout contract changed")
    if abs(float(holdout113.get("right_denominator_group_envelope", 0)) - 767682.175108969) > 1e-6 or abs(float(holdout113.get("grouped_lower_bound", 0)) - 1017376.1779486465) > 1e-6 or abs(float(holdout113.get("independent_endpoint_lower_bound", 0)) + 376366.25818842696) > 1e-6:
        return fail("ticket113 quantitative frontier changed")
    if audit113.get("next_theorem_target") != "UniformRightFareyDenominatorEndpointBudgetForVaughanCrossSpectrum" or "proves none" not in str(audit113.get("proof_boundary", "")):
        return fail("ticket113 target or proof boundary changed")

    path114 = Path("data/open-problem/ticket114-twin-ramanujan-numerator-dispersion-audit.json")
    if not path114.exists():
        return fail("missing ticket114 Ramanujan numerator-dispersion artifact")
    ticket114 = read_json(path114)
    expected_status114 = "ramanujan_centered_decomposition_exact_sharp_l2_support_audited_open"
    if ticket114.get("schema") != TICKET114_SCHEMA or ticket114.get("status") != expected_status114:
        return fail("ticket114 schema or status changed")
    attempts114 = ticket114.get("attempts", [])
    by_id114 = {str(row.get("problem_id")): row for row in attempts114 if isinstance(row, dict)} if isinstance(attempts114, list) else {}
    if set(by_id114) != EXPECTED_PROBLEMS:
        return fail("ticket114 attempts missing problems")
    paths114 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-114-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-114-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-114-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-114-ramanujan-numerator-dispersion-audit.json"),
    }
    for problem_id, attempt in by_id114.items():
        if not paths114[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket114 artifact or proof boundary missing")
    if by_id114["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_ramanujan_numerator_dispersion_audit":
        return fail("ticket114 shared audit reference changed")
    audit114 = ticket114.get("twin_ramanujan_numerator_dispersion_audit", {})
    machine114 = audit114.get("machine_audit", {})
    expected_metrics114 = {
        "maximum_horizon": 4194304,
        "row_count": 6,
        "minor_cell_count": 162,
        "right_denominator_group_count": 31,
        "signed_mean_finite_closure_count": 4,
        "sign_free_finite_closure_count": 3,
        "sign_free_terminal_run_start_horizon": 1048576,
        "contract_failure_count": 0,
    }
    if audit114.get("theorem_name") != "ExactRamanujanMeanCenteredNumeratorDecompositionAndSharpL2SupportBound" or {key: int(machine114.get(key, -1)) for key in expected_metrics114} != expected_metrics114:
        return fail("ticket114 theorem or machine contract changed")
    rows114 = audit114.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows114] != [4096, 32768, 262144, 1048576, 2097152, 4194304]:
        return fail("ticket114 horizon schedule changed")
    if [bool(row.get("signed_mean_l2_closes_finite")) for row in rows114] != [False, False, True, True, True, True]:
        return fail("ticket114 signed-mean finite frontier changed")
    if [bool(row.get("sign_free_l2_closes_finite")) for row in rows114] != [False, False, False, True, True, True]:
        return fail("ticket114 sign-free finite frontier changed")
    if max(float(row.get("maximum_ramanujan_contract_error", 1)) for row in rows114) > 1e-9 or max(float(row.get("maximum_rational_boundary_decomposition_error", 1)) for row in rows114) > 1e-7 or max(float(row.get("type_ii_abel_identity_absolute_error", 1)) for row in rows114) > 1e-5 or max(float(row.get("endpoint_ramanujan_identity_absolute_error", 1)) for row in rows114) > 1e-5:
        return fail("ticket114 exact identities changed")
    if any([int(item.get("right_denominator", -1)) for item in row.get("denominator_profile", [])] != list(range(2, 33)) for row in rows114):
        return fail("ticket114 right-denominator support changed")
    frontier114 = rows114[-1]
    if abs(float(frontier114.get("signed_mean_l2_lower_bound", 0)) - 621322.8285207893) > 1e-6 or abs(float(frontier114.get("sign_free_l2_lower_bound", 0)) - 327951.01574892923) > 1e-6 or abs(float(frontier114.get("sign_free_budget_to_known_ratio", 0)) - 0.8250221952011711) > 1e-12:
        return fail("ticket114 quantitative frontier changed")
    if audit114.get("next_theorem_target") != "EventuallySubcriticalVaughanCenteredFareyNumeratorDispersionBudget" or "proves none" not in str(audit114.get("proof_boundary", "")):
        return fail("ticket114 target or proof boundary changed")

    path115 = Path("data/open-problem/ticket115-twin-complex-cyclotomic-dispersion-audit.json")
    if not path115.exists():
        return fail("missing ticket115 complex cyclotomic artifact")
    ticket115 = read_json(path115)
    expected_status115 = "complex_cyclotomic_mean_exact_sharp_centered_l2_audited_open"
    if ticket115.get("schema") != TICKET115_SCHEMA or ticket115.get("status") != expected_status115:
        return fail("ticket115 schema or status changed")
    attempts115 = ticket115.get("attempts", [])
    by_id115 = {str(row.get("problem_id")): row for row in attempts115 if isinstance(row, dict)} if isinstance(attempts115, list) else {}
    if set(by_id115) != EXPECTED_PROBLEMS:
        return fail("ticket115 attempts missing problems")
    paths115 = {
        "riemann": Path("data/open-problem/riemann/rh-ticket-115-kernel-positivity-preserved.json"),
        "collatz": Path("data/open-problem/collatz/co-ticket-115-golden-mean-preserved.json"),
        "goldbach": Path("data/open-problem/goldbach/gb-ticket-115-joint-balanced-preserved.json"),
        "twin-prime": Path("data/open-problem/twin-prime/tp-ticket-115-complex-cyclotomic-dispersion-audit.json"),
    }
    for problem_id, attempt in by_id115.items():
        if not paths115[problem_id].exists() or "No " not in str(attempt.get("claim_boundary", "")):
            return fail(f"{problem_id}: ticket115 artifact or proof boundary missing")
    if by_id115["twin-prime"].get("bounded_result", {}).get("audit_ref") != "twin_complex_cyclotomic_dispersion_audit":
        return fail("ticket115 shared audit reference changed")
    audit115 = ticket115.get("twin_complex_cyclotomic_dispersion_audit", {})
    machine115 = audit115.get("machine_audit", {})
    expected_metrics115 = {
        "maximum_horizon": 4194304,
        "row_count": 6,
        "minor_cell_count": 162,
        "right_denominator_group_count": 31,
        "complex_scalar_centering_reduces_budget_count": 6,
        "orientation_free_worsens_budget_count": 6,
        "complex_signed_mean_finite_closure_count": 4,
        "complex_sign_free_finite_closure_count": 3,
        "orientation_free_finite_closure_count": 2,
        "contract_failure_count": 0,
    }
    expected_theorem115 = "ExactHalfFareyCyclotomicComplexMeanDecompositionSharpCenteredL2AndOrientationFreeNoGo"
    if audit115.get("theorem_name") != expected_theorem115 or {key: int(machine115.get(key, -1)) for key in expected_metrics115} != expected_metrics115:
        return fail("ticket115 theorem or machine contract changed")
    rows115 = audit115.get("rows", [])
    if [int(row.get("horizon", -1)) for row in rows115] != [4096, 32768, 262144, 1048576, 2097152, 4194304]:
        return fail("ticket115 horizon schedule changed")
    if [bool(row.get("complex_sign_free_closes_finite")) for row in rows115] != [False, False, False, True, True, True]:
        return fail("ticket115 scalar-mean finite frontier changed")
    if [bool(row.get("orientation_free_closes_finite")) for row in rows115] != [False, False, False, False, True, True]:
        return fail("ticket115 orientation-free no-go frontier changed")
    if any(float(row.get("complex_scalar_centering_budget_reduction", 0)) <= 0 for row in rows115) or any(float(row.get("complex_orientation_free_budget_increase", 0)) <= 0 for row in rows115):
        return fail("ticket115 centering comparison changed")
    if max(float(row.get("maximum_half_ramanujan_real_error", 1)) for row in rows115) > 1e-9 or max(float(row.get("maximum_complex_decomposition_error", 1)) for row in rows115) > 1e-7 or max(float(row.get("aggregate_complex_decomposition_error", 1)) for row in rows115) > 1e-6 or max(float(row.get("maximum_complex_geometry_identity_error", 1)) for row in rows115) > 1e-9:
        return fail("ticket115 exact identities changed")
    if any([int(item.get("right_denominator", -1)) for item in row.get("complex_denominator_profile", [])] != list(range(2, 33)) for row in rows115):
        return fail("ticket115 right-denominator support changed")
    frontier115 = rows115[-1]
    if abs(float(frontier115.get("complex_sign_free_lower_bound", 0)) - 335523.7440742075) > 1e-6 or abs(float(frontier115.get("complex_sign_free_budget_to_known_ratio", 0)) - 0.8209817766171058) > 1e-12 or abs(float(frontier115.get("orientation_free_lower_bound", 0)) - 248127.10487070633) > 1e-6:
        return fail("ticket115 quantitative frontier changed")
    expected_target115 = "EventuallySubcriticalVaughanCyclotomicMeanAndComplexCenteredNumeratorBudget"
    if audit115.get("next_theorem_target") != expected_target115 or "proves none" not in str(audit115.get("proof_boundary", "")):
        return fail("ticket115 target or proof boundary changed")

    print("open problem structure verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
