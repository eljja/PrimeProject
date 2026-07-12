from __future__ import annotations

from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, v2, write_json


GENERATED_AT = "2026-07-11T18:20:00+09:00"
SCHEMA = "primeproject.ticket82-fixed-mersenne-compensation-window-no-go-lab.v1"
MAX_HORIZON = 128
REFERENCE_EXPONENT = 3
SAMPLE_HORIZONS = {0, 1, 2, 4, 8, 16, 32, 64, 128}


def accelerated_step(n: int) -> tuple[int, int]:
    numerator = 3 * n + 1
    valuation = v2(numerator)
    return numerator >> valuation, valuation


def reference_symbolic_states(horizon: int) -> list[dict[str, int]]:
    if horizon < 0:
        raise ValueError("horizon must be nonnegative")

    # x_t(k)=(3^(k+t)+c_t)/2^d_t models A^(k+t)(2^k-1) for odd k.
    current = (3**REFERENCE_EXPONENT - 1) // 2
    constant = -1
    denominator_power = 1
    states = [
        {
            "post_index": 0,
            "reference_value": current,
            "constant": constant,
            "denominator_power": denominator_power,
            "incoming_valuation": 2,
        }
    ]

    for post_index in range(1, horizon + 1):
        next_value, valuation = accelerated_step(current)
        next_constant = 3 * constant + (1 << denominator_power)
        next_denominator_power = denominator_power + valuation
        numerator = 3 ** (REFERENCE_EXPONENT + post_index) + next_constant
        if v2(numerator) != next_denominator_power:
            raise AssertionError("reference symbolic valuation identity failed")
        if numerator >> next_denominator_power != next_value:
            raise AssertionError("reference symbolic iterate identity failed")
        current = next_value
        constant = next_constant
        denominator_power = next_denominator_power
        states.append(
            {
                "post_index": post_index,
                "reference_value": current,
                "constant": constant,
                "denominator_power": denominator_power,
                "incoming_valuation": valuation,
            }
        )
    return states


def progression_precision(horizon: int, states: list[dict[str, int]]) -> tuple[int, int]:
    precision = max(3, max(state["denominator_power"] + 1 for state in states))
    period_log2 = precision - 2
    if horizon == 0 and period_log2 != 1:
        raise AssertionError("odd-exponent base progression changed")
    if horizon == 1 and period_log2 != 3:
        raise AssertionError("one-step progression changed")
    if horizon >= 2 and period_log2 != 2 * horizon + 3:
        raise AssertionError("closed progression precision changed")
    return precision, period_log2


def dominance_threshold(states: list[dict[str, int]]) -> int:
    exponent = 3
    while True:
        sufficient = True
        for state in states:
            post_index = state["post_index"]
            denominator_power = state["denominator_power"]
            constant = abs(state["constant"])
            if 3 ** (exponent + post_index) <= (1 << (exponent + denominator_power)) + constant:
                sufficient = False
                break
        if sufficient:
            return exponent
        exponent += 1


def first_progression_exponent(period: int, threshold: int) -> int:
    multiplier = max(0, (threshold - REFERENCE_EXPONENT + period - 1) // period)
    return REFERENCE_EXPONENT + multiplier * period


def audit_horizon(horizon: int) -> dict[str, Any]:
    states = reference_symbolic_states(horizon)
    precision, period_log2 = progression_precision(horizon, states)
    period = 1 << period_log2
    threshold = dominance_threshold(states)
    witness_exponent = first_progression_exponent(period, threshold)
    congruence_failures = 0
    symbolic_formula_failures = 0
    growth_guard_failures = 0

    for state in states:
        post_index = state["post_index"]
        denominator_power = state["denominator_power"]
        constant = state["constant"]
        modulus = 1 << (denominator_power + 1)
        residue = (pow(3, witness_exponent + post_index, modulus) + constant) % modulus
        if residue != 1 << denominator_power:
            congruence_failures += 1

        reference_numerator = 3 ** (REFERENCE_EXPONENT + post_index) + constant
        if reference_numerator >> denominator_power != state["reference_value"]:
            symbolic_formula_failures += 1

        if 3 ** (threshold + post_index) <= (1 << (threshold + denominator_power)) + abs(constant):
            growth_guard_failures += 1

    expected_word = [3, 4] + [2] * max(0, horizon - 2)
    observed_word = [state["incoming_valuation"] for state in states[1:]]
    word_failure_count = int(observed_word != expected_word[:horizon])
    progression_failure_count = int(witness_exponent % period != REFERENCE_EXPONENT % period)
    threshold_failure_count = int(witness_exponent < threshold)
    total_failures = (
        congruence_failures
        + symbolic_formula_failures
        + growth_guard_failures
        + word_failure_count
        + progression_failure_count
        + threshold_failure_count
    )
    return {
        "horizon": horizon,
        "state_count": len(states),
        "post_reference_word": observed_word,
        "required_precision_bits": precision,
        "progression_period_log2": period_log2,
        "progression_period": period,
        "dominance_threshold": threshold,
        "first_certified_progression_exponent": witness_exponent,
        "symbolic_state_count": len(states),
        "congruence_failure_count": congruence_failures,
        "symbolic_formula_failure_count": symbolic_formula_failures,
        "growth_guard_failure_count": growth_guard_failures,
        "word_failure_count": word_failure_count,
        "progression_failure_count": progression_failure_count,
        "threshold_failure_count": threshold_failure_count,
        "total_failure_count": total_failures,
        "states": states,
    }


def analyze_fixed_window_no_go() -> dict[str, Any]:
    horizon_audits = [audit_horizon(horizon) for horizon in range(MAX_HORIZON + 1)]
    failures = sum(int(row["total_failure_count"]) for row in horizon_audits)
    symbolic_state_count = sum(int(row["symbolic_state_count"]) for row in horizon_audits)
    transition_condition_count = sum(int(row["horizon"]) for row in horizon_audits)
    samples = []
    for row in horizon_audits:
        if int(row["horizon"]) not in SAMPLE_HORIZONS:
            continue
        word = list(row["post_reference_word"])
        samples.append(
            {
                "horizon": row["horizon"],
                "post_reference_word_prefix": word[:12],
                "post_reference_word_length": len(word),
                "required_precision_bits": row["required_precision_bits"],
                "progression_period_log2": row["progression_period_log2"],
                "dominance_threshold": row["dominance_threshold"],
                "first_certified_progression_exponent": row["first_certified_progression_exponent"],
                "total_failure_count": row["total_failure_count"],
            }
        )

    status = (
        "fixed_mersenne_compensation_window_refuted_exactly_no_collatz_resolution"
        if failures == 0
        else "fixed_mersenne_window_audit_inconclusive_no_collatz_resolution"
    )
    return {
        "theorem_name": "FixedMersenneCompensationWindowNoGo",
        "source_ticket": "CO-TICKET-81",
        "family": "N_k=2^k-1 with odd exponents k in explicit arithmetic progressions",
        "statement": (
            "For every fixed H>=0, infinitely many odd exponents k satisfy "
            "A^(k+t)(2^k-1)>2^k-1 for every 0<=t<=H."
        ),
        "exact_symbolic_family": {
            "iterate": "x_t(k)=A^(k+t)(N_k)=(3^(k+t)+c_t)/2^d_t",
            "initial": "c_0=-1, d_0=1, x_0(k)=(3^k-1)/2 for odd k",
            "recurrence": "c_(t+1)=3*c_t+2^d_t; d_(t+1)=d_t+b_(t+1)",
            "reference_exponent": REFERENCE_EXPONENT,
            "reference_post_word": "b_1=3, b_2=4, and b_t=2 for every t>=3",
        },
        "explicit_progressions": {
            "horizon_0": "k congruent to 3 modulo 2",
            "horizon_1": "k congruent to 3 modulo 8",
            "horizon_at_least_2": "k congruent to 3 modulo 2^(2H+3)",
            "reason": "3 has multiplicative order 2^(Q-2) modulo 2^Q, and Q=2H+5 preserves every exact numerator valuation through post-index H.",
        },
        "proof_chain": [
            "TICKET81 gives x_0(k)=A^k(N_k)=(3^k-1)/2 for every odd exponent k.",
            "Along the reference exponent k=3, x_0=13 maps to 5, then 1, then remains 1; the additional valuation word is 3,4,2,2,... .",
            "Induction gives x_t(k)=(3^(k+t)+c_t)/2^d_t with c_(t+1)=3c_t+2^d_t and d_(t+1)=d_t+b_(t+1).",
            "For a fixed H, congruence k=3 mod 2^(Q-2) preserves 3^(k+t) modulo 2^Q and therefore preserves all exact valuations through H.",
            "For H>=2 the largest denominator exponent is d_H=2H+4, so Q=2H+5 and the explicit exponent progression is k=3 mod 2^(2H+3).",
            "For each fixed t and d_t,c_t, exponential dominance of 3^k over 2^k gives x_t(k)>N_k for all sufficiently large k in that progression.",
            "Hence no compensation-window length independent of k can force every Mersenne start below itself.",
        ],
        "machine_audit": {
            "max_horizon": MAX_HORIZON,
            "horizon_case_count": len(horizon_audits),
            "symbolic_state_count": symbolic_state_count,
            "transition_condition_count": transition_condition_count,
            "total_failure_count": failures,
            "samples": samples,
        },
        "computational_failure_count": failures,
        "theorem_status": status,
        "rejected_candidate_families": [
            {
                "family": "constant_post_expansion_compensation_window",
                "status": "refuted_by_explicit_infinite_exponent_progressions",
                "counteredge": "For every fixed H, an infinite progression of exponents preserves H post-block valuations and remains above the start throughout the window.",
            },
            {
                "family": "finite_parity_prefix_implies_uniform_mersenne_descent",
                "status": "refuted_by_two_adic_prefix_replication",
                "counteredge": "Every fixed reference prefix repeats on an exponent progression while Archimedean size grows without bound.",
            },
            {
                "family": "bounded_lookahead_least_counterexample_contradiction",
                "status": "refuted_on_the_mersenne_subfamily",
                "counteredge": "No bounded post-expansion lookahead supplies a uniform descent contradiction even on Mersenne starts.",
            },
        ],
        "discarded_route": (
            "Choose any constant number of post-expansion accelerated steps and claim that this bounded lookahead "
            "must repay the Mersenne expansion for every exponent."
        ),
        "retained_route": (
            "Any valid Mersenne compensation theorem must use an unbounded exponent-dependent window L(k), or a "
            "different global invariant that is not determined by a fixed finite valuation prefix."
        ),
        "candidate_theorem": (
            "MersenneGrowingWindowDescent: find an explicit unbounded L(k), preferably with a proved asymptotic "
            "upper bound, such that some A^(k+t)(2^k-1)<2^k-1 for 0<=t<=L(k)."
        ),
        "next_theorem_target": "MersenneGrowingWindowDescent",
        "equivalence_warning": (
            "The theorem proves unbounded post-expansion stopping delay on a Mersenne subfamily, not divergence. "
            "An exponent-dependent descent theorem for Mersenne starts would still not prove Collatz for all integers."
        ),
        "literature_context": [
            {
                "citation": "Terras, A stopping time problem on the positive integers, Acta Arithmetica 30 (1976)",
                "url": "https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers",
                "role": "Established stopping-time and finite parity-prefix context.",
            },
            {
                "citation": "Bernstein and Lagarias, The 3x+1 Conjugacy Map, Canadian Journal of Mathematics 48 (1996)",
                "url": "https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13",
                "role": "Established 2-adic finite-prefix and conjugacy context.",
            },
            {
                "citation": "Lagarias, The 3x+1 Problem: An Overview (2021)",
                "url": "https://arxiv.org/abs/2111.02635",
                "role": "Survey context for claim boundaries and the unresolved global problem.",
            },
        ],
        "novelty_boundary": (
            "Finite parity-prefix periodicity and 2-adic continuity are established. PrimeProject claims only the "
            "explicit Mersenne-exponent progression corollary, fixed-window no-go formulation, and reproducible symbolic audit; "
            "a stronger novelty claim requires dedicated literature and peer review."
        ),
        "proof_boundary": (
            "TICKET82 proves a restricted unbounded-delay theorem. It neither constructs a divergent orbit nor proves "
            "or disproves the Collatz conjecture."
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
        "proof_or_counterexample_mode": "fixed-local-window no-go transfer discipline",
        "attempt": (
            "Transfer only the requirement that a bounded local observation window cannot be promoted to a uniform "
            "global theorem without a target-specific compactness or growth bridge."
        ),
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket82_transfer": route, "candidate_theorem": target},
        "obstruction": "No problem-specific infinite arithmetic progression theorem was proved for this problem.",
        "candidate_theorem": target,
        "next_experiment": "Derive a target-specific growing-window or all-scale theorem.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket81 = read_json(ROOT / "data/open-problem/ticket81-mersenne-post-compensation-no-go-lab.json")
    collatz_audit = analyze_fixed_window_no_go()
    attempts = [
        transfer_attempt(ticket81, "riemann", "RH-TICKET-82", "FixedHeightWindowNoGoGuard", "Prove a genuinely all-height positivity or zero-detection bridge."),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-82",
            "route": "FixedMersenneCompensationWindowNoGo",
            "status": collatz_audit["theorem_status"],
            "proof_or_counterexample_mode": "explicit exponent progressions plus symbolic valuation-prefix preservation",
            "attempt": "Test whether any exponent-independent post-expansion compensation window forces descent for every Mersenne start.",
            "bounded_result": {"source_ticket": "CO-TICKET-81", "fixed_mersenne_compensation_window_no_go_audit": collatz_audit},
            "obstruction": collatz_audit["discarded_route"],
            "candidate_theorem": collatz_audit["candidate_theorem"],
            "next_experiment": "Build TICKET83 around growing exponent-dependent windows and lower/upper bounds for their necessary scale.",
            "claim_boundary": "No Collatz proof and no certified divergent Collatz counterexample.",
        },
        transfer_attempt(ticket81, "goldbach", "GB-TICKET-82", "FixedCutoffWindowNoGoGuard", "Prove positivity uniformly across an unbounded major/minor-arc scale."),
        transfer_attempt(ticket81, "twin-prime", "TP-TICKET-82", "FixedSieveDepthNoGoGuard", "Prove exact gap-2 mass through an unbounded parity-breaking hierarchy."),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "fixed_mersenne_window_no_go_open_no_collatz_resolution",
        "claim_boundary": "Ticket 82 proves one restricted Collatz Mersenne-family theorem but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket82-fixed-mersenne-compensation-window-no-go-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-82-fixed-mersenne-compensation-window-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-82-fixed-mersenne-compensation-window-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-82-fixed-mersenne-compensation-window-no-go.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-82-fixed-mersenne-compensation-window-no-go.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
