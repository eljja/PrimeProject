from __future__ import annotations

from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket82_fixed_mersenne_compensation_window_no_go_lab import reference_symbolic_states


GENERATED_AT = "2026-07-11T20:05:00+09:00"
SCHEMA = "primeproject.ticket83-mersenne-log-window-lower-bound-lab.v1"
MIN_HORIZON = 2
MAX_HORIZON = 256
SAMPLE_HORIZONS = {2, 3, 4, 8, 16, 32, 64, 128, 256}


def explicit_exponent(horizon: int) -> int:
    if horizon < MIN_HORIZON:
        raise ValueError("horizon must be at least 2")
    return 3 + (1 << (2 * horizon + 3))


def audit_quantitative_horizon(horizon: int) -> dict[str, Any]:
    states = reference_symbolic_states(horizon)
    exponent = explicit_exponent(horizon)
    period_log2 = 2 * horizon + 3
    period = 1 << period_log2
    progression_failures = int(exponent % period != 3)
    denominator_failures = 0
    constant_bound_failures = 0
    prefix_shape_failures = 0

    for state in states:
        post_index = int(state["post_index"])
        denominator_power = int(state["denominator_power"])
        constant = int(state["constant"])
        expected_denominator = 1 if post_index == 0 else 4 if post_index == 1 else 2 * post_index + 4
        if denominator_power != expected_denominator:
            denominator_failures += 1
        if abs(constant) >= 1 << denominator_power:
            constant_bound_failures += 1
        incoming = int(state["incoming_valuation"])
        if post_index == 0:
            expected_incoming = 2
        elif post_index == 1:
            expected_incoming = 3
        elif post_index == 2:
            expected_incoming = 4
        else:
            expected_incoming = 2
        if incoming != expected_incoming:
            prefix_shape_failures += 1

    linear_exponent_guard = exponent >= 4 * horizon + 11
    base_ratio_guard = 3**11 > (1 << 5) * (2**11)
    denominator_cap_guard = max(int(row["denominator_power"]) for row in states) == 2 * horizon + 4
    growth_proof_failure_count = sum(
        int(not guard)
        for guard in (linear_exponent_guard, base_ratio_guard, denominator_cap_guard)
    )

    # k_H < 2^(2H+4), so H > 0.5*log2(k_H)-2 without floating point.
    logarithmic_bound_failure_count = int(exponent >= 1 << (2 * horizon + 4))
    total_failures = (
        progression_failures
        + denominator_failures
        + constant_bound_failures
        + prefix_shape_failures
        + growth_proof_failure_count
        + logarithmic_bound_failure_count
    )
    return {
        "horizon": horizon,
        "explicit_exponent": exponent,
        "progression_period_log2": period_log2,
        "post_descent_delay_strict_lower_bound": horizon,
        "logarithmic_lower_bound": "delay > (1/2)*log2(k_H)-2",
        "maximum_denominator_power": max(int(row["denominator_power"]) for row in states),
        "symbolic_state_count": len(states),
        "progression_failure_count": progression_failures,
        "denominator_failure_count": denominator_failures,
        "constant_bound_failure_count": constant_bound_failures,
        "prefix_shape_failure_count": prefix_shape_failures,
        "growth_proof_failure_count": growth_proof_failure_count,
        "logarithmic_bound_failure_count": logarithmic_bound_failure_count,
        "total_failure_count": total_failures,
    }


def analyze_log_window_lower_bound() -> dict[str, Any]:
    rows = [audit_quantitative_horizon(horizon) for horizon in range(MIN_HORIZON, MAX_HORIZON + 1)]
    failures = sum(int(row["total_failure_count"]) for row in rows)
    state_count = sum(int(row["symbolic_state_count"]) for row in rows)
    samples = [row for row in rows if int(row["horizon"]) in SAMPLE_HORIZONS]
    status = (
        "mersenne_sub_half_log_window_refuted_exactly_no_collatz_resolution"
        if failures == 0
        else "mersenne_log_window_audit_inconclusive_no_collatz_resolution"
    )
    return {
        "theorem_name": "MersenneHalfLogDelayLowerBound",
        "source_ticket": "CO-TICKET-82",
        "delay_definition": (
            "D(k)=min{t>=0: A^(k+t)(2^k-1)<2^k-1}, with D(k)=infinity if the set is empty."
        ),
        "explicit_sequence": "k_H=3+2^(2H+3), H>=2",
        "statement": (
            "For every H>=2, D(k_H)>H>(1/2)*log2(k_H)-2. Consequently every o(log k) "
            "post-expansion descent window, and every c*log2(k) window with c<1/2, fails on infinitely many Mersenne exponents."
        ),
        "proof_chain": [
            "TICKET82 preserves the exact post-compensation valuation word 3,4,2,...,2 through H whenever k=3 mod 2^(2H+3).",
            "The explicit exponent k_H=3+2^(2H+3) lies in that progression.",
            "The symbolic iterates are x_t(k)=(3^(k+t)+c_t)/2^d_t with d_0=1, d_1=4, and d_t=2t+4 for t>=2.",
            "Direct bases and induction give |c_t|<2^d_t: after t>=2, c_(t+1)=3c_t+2^d_t<2^(d_t+2)=2^d_(t+1).",
            "For H>=2, k_H>=4H+11. Since (3/2)^4>2^2 and (3/2)^11>2^5, (3/2)^k_H>2^(2H+5)>=2^(d_t+1).",
            "Thus 3^(k_H+t)>2^(k_H+d_t)+|c_t| and x_t(k_H)>2^k_H-1 for every 0<=t<=H, proving D(k_H)>H.",
            "Because k_H<2^(2H+4), one has H>(1/2)*log2(k_H)-2.",
            "Any o(log k) window or c*log2(k) window with c<1/2 is eventually shorter than H on this explicit sequence and therefore cannot be a universal Mersenne descent window.",
        ],
        "machine_audit": {
            "min_horizon": MIN_HORIZON,
            "max_horizon": MAX_HORIZON,
            "horizon_case_count": len(rows),
            "symbolic_state_count": state_count,
            "total_failure_count": failures,
            "samples": samples,
        },
        "computational_failure_count": failures,
        "theorem_status": status,
        "rejected_candidate_families": [
            {
                "family": "sub_half_logarithmic_mersenne_window",
                "status": "refuted_by_explicit_k_H_sequence",
                "counteredge": "D(k_H)>H>(1/2)log2(k_H)-2 on the infinite sequence k_H=3+2^(2H+3).",
            },
            {
                "family": "little_o_log_mersenne_window",
                "status": "refuted_asymptotically",
                "counteredge": "Every o(log k) window is eventually below the certified H delay along k_H.",
            },
            {
                "family": "log_window_coefficient_below_one_half",
                "status": "refuted_asymptotically",
                "counteredge": "Every c log2(k) window with fixed c<1/2 is eventually shorter than H along k_H.",
            },
        ],
        "discarded_route": (
            "Attempt a universal Mersenne descent theorem with a post-expansion window growing slower than "
            "one half of log2(k), up to an additive constant."
        ),
        "retained_route": (
            "Search at logarithmic scale or above, improve the lower-bound coefficient by optimizing reference "
            "valuation words, and separately seek a proved upper bound for Mersenne descent."
        ),
        "candidate_theorem": (
            "MersenneLogWindowDichotomy: determine the optimal lower-bound coefficient alpha for explicit delayed "
            "Mersenne subsequences and prove or refute a finite logarithmic upper coefficient beta for all exponents."
        ),
        "next_theorem_target": "MersenneLogWindowDichotomy",
        "equivalence_warning": (
            "A lower bound on finite descent delay does not imply divergence. An upper bound only for Mersenne starts "
            "would remain a restricted family theorem, not the full Collatz conjecture."
        ),
        "literature_context": [
            {
                "citation": "Terras, A stopping time problem on the positive integers, Acta Arithmetica 30 (1976)",
                "url": "https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers",
                "role": "Established stopping-time and finite parity-prefix framework.",
            },
            {
                "citation": "Inselmann, An approximation of the Collatz map and a lower bound for the average total stopping time (2024)",
                "url": "https://arxiv.org/abs/2402.03276",
                "role": "Modern logarithmic-scale stopping-time context; it does not supply this Mersenne subsequence theorem.",
            },
            {
                "citation": "Bernstein and Lagarias, The 3x+1 Conjugacy Map, Canadian Journal of Mathematics 48 (1996)",
                "url": "https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13",
                "role": "Established 2-adic finite-prefix context used by TICKET82.",
            },
        ],
        "novelty_boundary": (
            "The underlying finite-prefix periodicity is established. PrimeProject claims only the explicit k_H "
            "quantitative corollary, half-log window no-go, and reproducible audit. Literature completeness and novelty "
            "require independent systematic review."
        ),
        "proof_boundary": (
            "TICKET83 proves a restricted lower bound for finite post-expansion descent delay. It proves neither a "
            "divergent Collatz orbit nor any of the four open problems."
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
        "proof_or_counterexample_mode": "quantitative growing-window lower-bound transfer discipline",
        "attempt": "Transfer only the need to quantify the minimum scale of any proposed local-to-global bridge.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket83_transfer": route, "candidate_theorem": target},
        "obstruction": "No problem-specific quantitative lower-bound sequence was proved for this problem.",
        "candidate_theorem": target,
        "next_experiment": "Derive a target-specific scale lower bound before proposing an all-scale theorem.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket82 = read_json(ROOT / "data/open-problem/ticket82-fixed-mersenne-compensation-window-no-go-lab.json")
    collatz_audit = analyze_log_window_lower_bound()
    attempts = [
        transfer_attempt(ticket82, "riemann", "RH-TICKET-83", "AllHeightScaleLowerBoundGuard", "Quantify the minimum height range required by any zero detector."),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-83",
            "route": "MersenneHalfLogDelayLowerBound",
            "status": collatz_audit["theorem_status"],
            "proof_or_counterexample_mode": "explicit exponent sequence plus exact logarithmic delay inequality",
            "attempt": "Quantify the minimum growth scale of a universal post-expansion Mersenne descent window.",
            "bounded_result": {"source_ticket": "CO-TICKET-82", "mersenne_log_window_lower_bound_audit": collatz_audit},
            "obstruction": collatz_audit["discarded_route"],
            "candidate_theorem": collatz_audit["candidate_theorem"],
            "next_experiment": "Build TICKET84 to optimize the lower coefficient and search for a rigorous logarithmic upper coefficient.",
            "claim_boundary": "No Collatz proof and no certified divergent Collatz counterexample.",
        },
        transfer_attempt(ticket82, "goldbach", "GB-TICKET-83", "ExceptionalScaleLowerBoundGuard", "Quantify the minimum unbounded modulus and cutoff scale of any positivity bridge."),
        transfer_attempt(ticket82, "twin-prime", "TP-TICKET-83", "ParityBreakingScaleLowerBoundGuard", "Quantify the minimum sieve-depth growth required before exact gap-2 claims."),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "mersenne_log_window_lower_bound_open_no_collatz_resolution",
        "claim_boundary": "Ticket 83 proves one restricted Collatz Mersenne-family delay lower bound but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket83-mersenne-log-window-lower-bound-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-83-mersenne-log-window-lower-bound.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-83-mersenne-log-window-lower-bound.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-83-mersenne-log-window-lower-bound.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-83-mersenne-log-window-lower-bound.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
