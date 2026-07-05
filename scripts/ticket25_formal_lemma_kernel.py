from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket25-formal-lemma-kernel.v1"
TICKET24_PATH = ROOT / "data/open-problem/ticket24-bridge-weight-lab.json"


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ticket24_attempt(problem_id: str) -> dict[str, object]:
    payload = read_json(TICKET24_PATH)
    for attempt in payload.get("attempts", []):
        if isinstance(attempt, dict) and attempt.get("problem_id") == problem_id:
            return attempt
    raise ValueError(f"missing Ticket 24 attempt for {problem_id}")


def riemann_finite_prefix_kernel() -> dict[str, object]:
    source = ticket24_attempt("riemann")
    bounded = source["bounded_result"]
    missed = bounded.get("missed_threshold_cases", [])
    fit = bounded.get("quadratic_budget_fit", [])
    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-25",
        "status": "proof_pressure_open",
        "route": "FinitePrefixKernel",
        "proof_or_counterexample_mode": "surrogate_fixed_prefix_refutation",
        "attempt": (
            "Extract a formal kernel from the detector-budget experiment: a proof route that verifies only a fixed "
            "finite Li-prefix is refuted by a surrogate off-critical zero whose threshold witness lies beyond the "
            "prefix."
        ),
        "bounded_result": {
            "source_ticket": "RH-TICKET-24",
            "search_cap": bounded.get("search_cap"),
            "threshold": bounded.get("threshold"),
            "missed_case_count": len(missed),
            "fixed_prefix_kernel_status": "fixed_prefix_refuted_for_surrogate_family" if missed else "no_missed_case",
            "kernel_rows": [
                {
                    "offcritical_beta": row.get("offcritical_beta"),
                    "height": row.get("height"),
                    "search_cap": row.get("search_limit"),
                    "threshold_seen": row.get("threshold_seen"),
                    "minimum_value_seen": row.get("minimum_value_seen"),
                    "minimum_index_seen": row.get("minimum_index_seen"),
                }
                for row in missed
            ],
            "quadratic_budget_fit": fit,
        },
        "formal_kernel_statement": (
            "In the surrogate detector family, finite prefix P is not a uniform RH proof certificate when there exists "
            "an off-critical surrogate row with threshold_seen=false up to P."
        ),
        "obstruction": (
            "This is a kernel against a proof strategy, not an RH counterexample. The real target still requires a "
            "zeta-zero theorem with a uniform all-height explicit-formula bound."
        ),
        "candidate_theorem": (
            "A valid contrapositive RH proof must provide an explicit N(delta,T) and a zero-interference bound for "
            "all off-critical zeros, not a finite prefix check."
        ),
        "next_experiment": "Formalize the surrogate prefix-refutation lemma and then replace the surrogate with zeta-zero bounds.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def collatz_affine_lift_lemma() -> dict[str, object]:
    source = ticket24_attempt("collatz")
    bounded = source["bounded_result"]
    eliminated = bounded.get("false_quotient_cycles_eliminated_by_affine_lift", [])
    positive = bounded.get("positive_cycle_candidates_seen", [])
    nontrivial_positive = bounded.get("nontrivial_positive_cycle_candidates_seen", [])
    kernel_rows = [
        {
            "modulus_bits": row.get("modulus_bits"),
            "cycle_length": row.get("cycle_length"),
            "total_shift": row.get("total_shift"),
            "expansion_multiplier": row.get("expansion_multiplier"),
            "affine_cycle_status": row.get("affine_cycle_status"),
            "candidate_value": row.get("candidate_value"),
        }
        for row in eliminated
    ]
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-25",
        "status": "proof_pressure_open",
        "route": "FormalAffineLiftLemma",
        "proof_or_counterexample_mode": "quotient_cycle_elimination_lemma",
        "attempt": (
            "Promote the Ticket 24 Collatz lift audit into a theorem-kernel candidate. A quotient cycle is not a "
            "positive integer cycle unless its valuation word has a positive integral affine fixed point that validates "
            "exactly."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-24",
            "tested_modulus_bits": bounded.get("modulus_bits_tested"),
            "first_tested_clean_suffix_modulus_bits": bounded.get("first_tested_clean_suffix_modulus_bits"),
            "affine_lift_eliminated_cycle_count": len(eliminated),
            "positive_cycle_candidate_count": len(positive),
            "nontrivial_positive_cycle_candidate_count": len(nontrivial_positive),
            "kernel_rows": kernel_rows,
            "known_positive_cycle_values": sorted(
                {
                    row.get("candidate_value")
                    for row in positive
                    if isinstance(row, dict) and row.get("candidate_value") is not None
                }
            ),
        },
        "formal_kernel_statement": (
            "For an accelerated Collatz valuation word w of length k, total shift s, and affine constant c>0, a "
            "positive integer cycle with exact word w can exist only if 2^s-3^k>0, c is divisible by 2^s-3^k, and "
            "the resulting odd integer validates the exact valuations. Every listed false quotient cycle fails this "
            "kernel."
        ),
        "obstruction": (
            "The lemma eliminates the tested false quotient cycles. It does not prove that all larger quotients have "
            "no nontrivial liftable SCC, and it does not prove descent for non-cyclic branches."
        ),
        "candidate_theorem": (
            "Every finite quotient SCC of the accelerated Collatz map either fails the affine lift kernel or is the "
            "known 1-cycle; all remaining branches descend under a well-founded exact-cylinder rank."
        ),
        "next_experiment": "Move this affine lift kernel into a minimal formal proof file, then attack the non-cyclic branch rank.",
        "claim_boundary": "No Collatz proof and no Collatz counterexample found.",
    }


def goldbach_finite_exception_kernel() -> dict[str, object]:
    source = ticket24_attempt("goldbach")
    bounded = source["bounded_result"]
    hardest = bounded.get("hardest_first_witness", {})
    weakest = bounded.get("weakest_sampled_count_to_scale_ratio", {})
    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-25",
        "status": "proof_pressure_open",
        "route": "FiniteExceptionKernel",
        "proof_or_counterexample_mode": "bounded_exception_elimination",
        "attempt": (
            "Extract the finite theorem-kernel from the Goldbach search: the checked range has no counterexample, and "
            "the weakest sampled windows identify where an eventual explicit lower-bound theorem must be stress-tested."
        ),
        "bounded_result": {
            "source_ticket": "GB-TICKET-24",
            "finite_even_bound": bounded.get("search_limit"),
            "counterexample_count": len(bounded.get("counterexamples_found", [])),
            "finite_exception_kernel_status": bounded.get("exceptional_set_status"),
            "hardest_first_witness": hardest,
            "weakest_sampled_count_to_scale_ratio": weakest,
            "kernel_rows": [
                {
                    "kernel": "finite_counterexample_search",
                    "bound": bounded.get("search_limit"),
                    "counterexamples": len(bounded.get("counterexamples_found", [])),
                },
                {
                    "kernel": "hardest_first_witness",
                    "even": hardest.get("even"),
                    "smallest_prime": hardest.get("smallest_prime"),
                    "partner": hardest.get("partner"),
                },
                {
                    "kernel": "weakest_sampled_ratio",
                    "even": weakest.get("even"),
                    "representation_count": weakest.get("representation_count"),
                    "count_to_scale_ratio": weakest.get("count_to_scale_ratio"),
                },
            ],
        },
        "formal_kernel_statement": (
            "A finite Goldbach verification kernel can close only N <= B. To prove the conjecture, it must be paired "
            "with an independent theorem proving r_2(N)>0 for every even N>B."
        ),
        "obstruction": (
            "The finite kernel is useful but bounded. The missing proof remains an explicit positive lower bound beyond "
            "the verified range."
        ),
        "candidate_theorem": (
            "There is an explicit B such that every even N>B has positive Goldbach representation count, and every even "
            "N<=B is certified by a reproducible finite verifier."
        ),
        "next_experiment": "Turn sampled weak windows into explicit error-budget constraints for a large-N theorem.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found.",
    }


def twin_bounded_gap_counterkernel() -> dict[str, object]:
    source = ticket24_attempt("twin-prime")
    bounded = source["bounded_result"]
    rows = bounded.get("weight_rows", [])
    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-25",
        "status": "proof_pressure_open",
        "route": "BoundedGapCounterKernel",
        "proof_or_counterexample_mode": "bounded_gap_only_shortcut_refutation",
        "attempt": (
            "Extract the counterkernel against bounded-gap-only proof shortcuts: deleting the right member of every "
            "twin pair destroys exact gap 2 while preserving almost all bounded-gap mass excluding gap 2."
        ),
        "bounded_result": {
            "source_ticket": "TP-TICKET-24",
            "bounded_gap_counterkernel_status": "bounded_gap_only_statistic_refuted",
            "max_gap": bounded.get("max_gap"),
            "kernel_rows": [
                {
                    "limit": row.get("limit"),
                    "exact_gap_weight_margin": row.get("exact_gap_weight_margin"),
                    "bounded_gap_retention_ratio": row.get("bounded_gap_retention_ratio"),
                    "bounded_without_gap_2_retention_ratio": row.get("bounded_without_gap_2_retention_ratio"),
                    "deletion_model_exact_gap_2": row.get("deletion_model_exact_gap_2"),
                }
                for row in rows
            ],
            "last_row": bounded.get("last_row"),
        },
        "formal_kernel_statement": (
            "Any argument whose decisive statistic is invariant under removing exact gap-2 pairs while retaining "
            "bounded gaps cannot prove twin-prime infinitude. It must use an exact-gap-2 lower-bound functional."
        ),
        "obstruction": (
            "The counterkernel refutes a proof shortcut, not the twin-prime negation. A proof still needs an "
            "unconditional exact gap-2 lower bound at arbitrarily large scales."
        ),
        "candidate_theorem": (
            "An exact-gap-2 sieve weight has a positive lower bound for infinitely many scales and cannot be replaced "
            "by a bounded-gap-only statistic."
        ),
        "next_experiment": "Search for an exact-gap weight with explicit parity-error control.",
        "claim_boundary": "No Twin Prime proof. The bounded-gap counterkernel only rejects weaker proof routes.",
    }


def build_payload() -> dict[str, object]:
    return {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "formal_kernel_open_no_resolution",
        "claim_boundary": (
            "Ticket 25 extracts theorem-kernel candidates and shortcut counterkernels from Ticket 24. It does not "
            "prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": [
            riemann_finite_prefix_kernel(),
            collatz_affine_lift_lemma(),
            goldbach_finite_exception_kernel(),
            twin_bounded_gap_counterkernel(),
        ],
    }


def write_attempt_artifacts(payload: dict[str, object]) -> None:
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-25-finite-prefix-kernel.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-25-affine-lift-lemma.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-25-finite-exception-kernel.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-25-bounded-gap-counterkernel.json",
    }
    for attempt in payload["attempts"]:
        write_json(paths[attempt["problem_id"]], attempt)


def main() -> int:
    payload = build_payload()
    write_json(ROOT / "data/open-problem/ticket25-formal-lemma-kernel.json", payload)
    write_attempt_artifacts(payload)
    print("ticket25 formal lemma kernel written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
