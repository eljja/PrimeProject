from __future__ import annotations

from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, v2, write_json


GENERATED_AT = "2026-07-11T16:10:00+09:00"
SCHEMA = "primeproject.ticket81-mersenne-post-compensation-no-go-lab.v1"
MAX_K = 1024
EXACT_DESCENT_EXCEPTIONS = {2, 4, 8}
SAMPLE_K = {2, 3, 4, 5, 6, 8, 9, 10, 16, 32, 64, 128, 256, 512, 1024}


def accelerated_step(n: int) -> tuple[int, int]:
    numerator = 3 * n + 1
    valuation = v2(numerator)
    return numerator >> valuation, valuation


def mersenne_start(k: int) -> int:
    if k < 2:
        raise ValueError("k must be at least 2")
    return (1 << k) - 1


def initial_block_iterate(k: int, step: int) -> int:
    if not 0 <= step <= k - 1:
        raise ValueError("step must lie in the initial valuation-one block")
    return (3**step) * (1 << (k - step)) - 1


def expected_post_block_valuation(k: int) -> int:
    return 2 if k % 2 == 1 else 3 + v2(k)


def post_block_iterate(k: int) -> int:
    value = 3**k - 1
    return value >> v2(value)


def audit_mersenne_post_compensation() -> dict[str, Any]:
    case_count = 0
    initial_step_replay_count = 0
    initial_formula_failures = 0
    initial_valuation_failures = 0
    stabilization_failures = 0
    post_formula_failures = 0
    post_valuation_failures = 0
    exception_classification_failures = 0
    symbolic_partition_failures = 0
    non_descent_count = 0
    descent_count = 0
    odd_k_count = 0
    even_k_count = 0
    samples: list[dict[str, Any]] = []

    for k in range(2, MAX_K + 1):
        case_count += 1
        odd_k_count += int(k % 2 == 1)
        even_k_count += int(k % 2 == 0)
        start = mersenne_start(k)
        current = start
        for step in range(1, k):
            current, valuation = accelerated_step(current)
            initial_step_replay_count += 1
            if valuation != 1:
                initial_valuation_failures += 1
            if current != initial_block_iterate(k, step):
                initial_formula_failures += 1
            if current <= start:
                initial_formula_failures += 1

        modulus = 1 << k
        if start >= modulus or start % modulus != start:
            stabilization_failures += 1
        post, valuation = accelerated_step(current)
        expected_post = post_block_iterate(k)
        expected_valuation = expected_post_block_valuation(k)
        if post != expected_post:
            post_formula_failures += 1
        if valuation != expected_valuation:
            post_valuation_failures += 1

        descends = post < start
        expected_descends = k in EXACT_DESCENT_EXCEPTIONS
        if descends != expected_descends:
            exception_classification_failures += 1
        descent_count += int(descends)
        non_descent_count += int(not descends)

        symbolic_pass = (
            (k % 2 == 1 and k >= 3)
            or k == 6
            or (k % 2 == 0 and k >= 10)
        )
        if symbolic_pass != (not descends):
            symbolic_partition_failures += 1

        if k in SAMPLE_K:
            samples.append(
                {
                    "k": k,
                    "start": start,
                    "initial_valuation_one_steps": k - 1,
                    "residue_stabilized_by_initial_block": True,
                    "first_post_block_valuation": valuation,
                    "post_block_iterate": post,
                    "post_block_above_start": post > start,
                    "classification": "descent_exception" if descends else "post_compensation_non_descent",
                }
            )

    failure_count = (
        initial_formula_failures
        + initial_valuation_failures
        + stabilization_failures
        + post_formula_failures
        + post_valuation_failures
        + exception_classification_failures
        + symbolic_partition_failures
    )
    return {
        "min_k": 2,
        "max_k": MAX_K,
        "mersenne_case_count": case_count,
        "initial_step_replay_count": initial_step_replay_count,
        "odd_k_count": odd_k_count,
        "even_k_count": even_k_count,
        "post_compensation_non_descent_count": non_descent_count,
        "descent_exception_count": descent_count,
        "descent_exception_k": sorted(EXACT_DESCENT_EXCEPTIONS),
        "initial_formula_failure_count": initial_formula_failures,
        "initial_valuation_failure_count": initial_valuation_failures,
        "stabilization_failure_count": stabilization_failures,
        "post_formula_failure_count": post_formula_failures,
        "post_valuation_failure_count": post_valuation_failures,
        "exception_classification_failure_count": exception_classification_failures,
        "symbolic_partition_failure_count": symbolic_partition_failures,
        "total_failure_count": failure_count,
        "samples": samples,
    }


def analyze_post_compensation_no_go() -> dict[str, Any]:
    audit = audit_mersenne_post_compensation()
    failures = int(audit["total_failure_count"])
    status = (
        "mersenne_first_post_compensation_descent_refuted_exactly_no_collatz_resolution"
        if failures == 0
        else "mersenne_post_compensation_audit_inconclusive_no_collatz_resolution"
    )
    return {
        "theorem_name": "MersenneFirstPostCompensationDescentNoGo",
        "source_ticket": "CO-TICKET-80",
        "family": "N_k=2^k-1, k>=2",
        "exact_formula": {
            "initial_block": "A^j(N_k)=3^j*2^(k-j)-1 for 0<=j<=k-1",
            "initial_valuations": "a_1=...=a_(k-1)=1",
            "stabilization": "the depth-(k-1) cylinder modulus is 2^k=N_k+1, so its least residue is already N_k",
            "post_block": "A^k(N_k)=oddpart(3^k-1)",
            "post_valuation": "a_k=2 for odd k; a_k=3+v2(k) for even k",
        },
        "classification": {
            "descent_exceptions": "k in {2,4,8}",
            "non_descent_infinite_families": [
                "every odd k>=3",
                "k=6",
                "every even k>=10",
            ],
        },
        "proof_chain": [
            "Direct induction gives the initial k-1 valuation-one block and keeps every one of those iterates above N_k.",
            "At depth k-1 the exact cylinder modulus equals N_k+1, so the least residue has already stabilized to the positive integer N_k.",
            "The next numerator is 2*(3^k-1). LTE gives v2(3^k-1)=1 for odd k and 2+v2(k) for even k.",
            "Hence the first post-block iterate is oddpart(3^k-1).",
            "For odd k>=3, (3^k-1)/2>2^k-1, so every odd exponent is non-descending.",
            "For even k>=10, 2^(2+v2(k))<=4k and (3^k-1)/(4k)>2^k-1; the latter follows from (8/9)*(3/2)^k>4k at k=10 and monotonicity of (3/2)^k/k.",
            "Only k=2,4,6,8 remain. Direct evaluation gives descent for k=2,4,8 and non-descent for k=6.",
            "Therefore the first non-1 compensation valuation after the stabilized Mersenne expansion block does not force descent for an infinite family.",
        ],
        "machine_audit": audit,
        "computational_failure_count": failures,
        "theorem_status": status,
        "rejected_candidate_families": [
            {
                "family": "first_post_expansion_valuation_forces_descent",
                "status": "refuted_by_infinite_mersenne_families",
                "counteredge": "All odd k>=3 and all even k>=10 remain above N_k after the first compensation step.",
            },
            {
                "family": "positive_residue_stabilization_implies_near_term_descent",
                "status": "refuted_by_stabilized_mersenne_cylinders",
                "counteredge": "The least residue is N_k by depth k-1, yet the next step is non-descending for infinitely many k.",
            },
            {
                "family": "single_lte_burst_repays_linear_valuation_debt",
                "status": "refuted_by_logarithmic_post_valuation",
                "counteredge": "The compensating valuation is 2 or 3+v2(k), while the expansion block length is k-1.",
            },
        ],
        "discarded_route": (
            "After a long valuation-one block, use only the first larger valuation to force descent, even when the "
            "positive-integer cylinder residue has already stabilized."
        ),
        "retained_route": (
            "Analyze an adaptive multi-step compensation window and prove cumulative valuation surplus, not one LTE burst, "
            "overcomes the preceding expansion while preserving a horizon-independent argument."
        ),
        "candidate_theorem": (
            "MersenneAdaptiveCompensationWindow: find an explicit window L(k) and prove that the cumulative valuations "
            "after the initial k-1 expansion steps force an iterate below 2^k-1, without importing empirical stopping time."
        ),
        "next_theorem_target": "MersenneAdaptiveCompensationWindow",
        "equivalence_warning": (
            "Proving such a compensation window only for Mersenne starts would be a genuine family theorem but not Collatz. "
            "Claiming the same window for every stabilized positive cylinder without proof would reintroduce the full conjecture."
        ),
        "literature_context": [
            {
                "citation": "Bernstein and Lagarias, The 3x+1 Conjugacy Map, Canadian Journal of Mathematics 48 (1996)",
                "url": "https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13",
                "role": "Established parity-cylinder and 2-adic context.",
            },
            {
                "citation": "Tao, Almost all orbits of the Collatz map attain almost bounded values, Forum of Mathematics, Pi 10 (2022)",
                "url": "https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/almost-all-orbits-of-the-collatz-map-attain-almost-bounded-values/1008CC2DF91AF87F66D190C5E01C907F",
                "role": "Primary context separating explicit family behavior from an all-integer theorem.",
            },
        ],
        "novelty_boundary": (
            "The initial Mersenne trajectory formula and LTE are elementary established tools. PrimeProject claims only "
            "the explicit stabilized-cylinder post-compensation classification, no-go framing, audit, and integration with TICKET80."
        ),
        "proof_boundary": (
            "TICKET81 proves a restricted no-go theorem for one proposed compensation rule. It does not establish the full "
            "stopping time of Mersenne numbers and neither proves nor disproves Collatz."
        ),
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "single-compensation-step no-go transfer discipline",
        "attempt": (
            "Transfer only the requirement that one local compensation event cannot be assumed to repair an unbounded "
            "global deficit. No Mersenne or Collatz formula is transferred."
        ),
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket81_transfer": route, "candidate_theorem": target},
        "obstruction": "No problem-specific exact compensation family was proved for this problem.",
        "candidate_theorem": target,
        "next_experiment": "Derive a target-specific cumulative rather than one-step margin theorem.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket80 = read_json(ROOT / "data/open-problem/ticket80-least-counterexample-compactness-no-go-lab.json")
    collatz_audit = analyze_post_compensation_no_go()
    attempts = [
        transfer_attempt(ticket80, "riemann", "RH-TICKET-81", "SingleHeightCorrectionNoGoGuard", "Control a cumulative all-height positivity margin rather than one local kernel correction."),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-81",
            "route": "MersenneFirstPostCompensationDescentNoGo",
            "status": collatz_audit["theorem_status"],
            "proof_or_counterexample_mode": "exact stabilized Mersenne cylinders plus LTE compensation classification",
            "attempt": "Test whether the first non-1 valuation after a stabilized all-ones Mersenne expansion block forces descent.",
            "bounded_result": {"source_ticket": "CO-TICKET-80", "mersenne_post_compensation_no_go_audit": collatz_audit},
            "obstruction": collatz_audit["discarded_route"],
            "candidate_theorem": collatz_audit["candidate_theorem"],
            "next_experiment": "Build TICKET82 for cumulative multi-step compensation after the Mersenne expansion block.",
            "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
        },
        transfer_attempt(ticket80, "goldbach", "GB-TICKET-81", "SingleExceptionalCorrectionNoGoGuard", "Prove cumulative main-term dominance across the full exceptional range, not one corrected modulus."),
        transfer_attempt(ticket80, "twin-prime", "TP-TICKET-81", "SingleParityCorrectionNoGoGuard", "Prove cumulative exact-gap mass survives every parity leakage stage, not one selector correction."),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "mersenne_post_compensation_no_go_open_no_collatz_resolution",
        "claim_boundary": "Ticket 81 proves one restricted Collatz family no-go theorem but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket81-mersenne-post-compensation-no-go-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-81-mersenne-post-compensation-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-81-mersenne-post-compensation-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-81-mersenne-post-compensation-no-go.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-81-mersenne-post-compensation-no-go.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
