from __future__ import annotations

from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json


GENERATED_AT = "2026-07-11T21:40:00+09:00"
SCHEMA = "primeproject.ticket84-two-adic-cycle-log-delay-lab.v1"
MIN_HORIZON = 2
MAX_HORIZON = 256
TARGET_POWER = -13
SAMPLE_HORIZONS = {2, 3, 4, 8, 16, 32, 64, 128, 256}


def expected_denominator_power(post_index: int) -> int:
    if post_index < 0:
        raise ValueError("post index must be nonnegative")
    if post_index % 2 == 0:
        return 1 + 3 * (post_index // 2)
    return 3 + 3 * ((post_index - 1) // 2)


def cycle_symbolic_states(horizon: int) -> list[dict[str, int]]:
    if horizon < 0:
        raise ValueError("horizon must be nonnegative")
    constant = -1
    denominator_power = 1
    states = [{
        "post_index": 0,
        "constant": constant,
        "denominator_power": denominator_power,
        "ghost_value": -7,
        "incoming_valuation": 2,
    }]
    for post_index in range(1, horizon + 1):
        valuation = 2 if post_index % 2 == 1 else 1
        constant = 3 * constant + (1 << denominator_power)
        denominator_power += valuation
        ghost_value = -5 if post_index % 2 == 1 else -7
        ghost_numerator = (TARGET_POWER * (3**post_index)) + constant
        if ghost_numerator != (1 << denominator_power) * ghost_value:
            raise AssertionError("two-adic cycle symbolic identity failed")
        states.append({
            "post_index": post_index,
            "constant": constant,
            "denominator_power": denominator_power,
            "ghost_value": ghost_value,
            "incoming_valuation": valuation,
        })
    return states


def lift_discrete_log_residues(max_precision: int) -> dict[int, int]:
    if max_precision < 3:
        raise ValueError("precision must be at least 3")
    residues = {3: 1}
    residue = 1
    for precision in range(3, max_precision):
        next_modulus = 1 << (precision + 1)
        lift_step = 1 << (precision - 2)
        candidates = (residue, residue + lift_step)
        valid = [candidate for candidate in candidates if pow(3, candidate, next_modulus) == TARGET_POWER % next_modulus]
        if len(valid) != 1:
            raise AssertionError("discrete logarithm Hensel lift lost uniqueness")
        residue = valid[0]
        residues[precision + 1] = residue
    return residues


def explicit_cycle_exponent(horizon: int, residues: dict[int, int] | None = None) -> dict[str, int]:
    states = cycle_symbolic_states(horizon)
    denominator_power = states[-1]["denominator_power"]
    precision = denominator_power + 1
    table = residues or lift_discrete_log_residues(precision)
    residue = table[precision]
    period_log2 = precision - 2
    period = 1 << period_log2
    exponent = residue + period
    return {
        "horizon": horizon,
        "denominator_power": denominator_power,
        "precision": precision,
        "period_log2": period_log2,
        "period": period,
        "residue": residue,
        "exponent": exponent,
    }


def audit_horizon(horizon: int, residues: dict[int, int]) -> dict[str, Any]:
    states = cycle_symbolic_states(horizon)
    exponent_data = explicit_cycle_exponent(horizon, residues)
    exponent = exponent_data["exponent"]
    denominator_power = exponent_data["denominator_power"]
    period = exponent_data["period"]
    residue = exponent_data["residue"]
    lift_failure_count = int(pow(3, residue, 1 << exponent_data["precision"]) != TARGET_POWER % (1 << exponent_data["precision"]))
    range_failure_count = int(not (0 < residue < period and period < exponent < 2 * period))
    valuation_failure_count = 0
    denominator_failure_count = 0
    constant_failure_count = 0
    for state in states:
        post_index = state["post_index"]
        d_t = state["denominator_power"]
        constant = state["constant"]
        modulus = 1 << (d_t + 1)
        numerator_residue = (pow(3, exponent + post_index, modulus) + constant) % modulus
        if numerator_residue != 1 << d_t:
            valuation_failure_count += 1
        if d_t != expected_denominator_power(post_index):
            denominator_failure_count += 1
        if abs(constant) >= 1 << (2 * post_index + 1):
            constant_failure_count += 1

    # For d>=4, (3/2)^(2^(d-1)+1)>2^(d+1); d=4 is direct and the claim propagates by squaring.
    base_growth_guard = 3**9 > 1 << 14
    period_growth_guard = denominator_power >= 4 and exponent >= (1 << (denominator_power - 1)) + 1
    affine_margin_guard = exponent + 1 > 2 * horizon + 1
    growth_failure_count = sum(int(not value) for value in (base_growth_guard, period_growth_guard, affine_margin_guard))

    # exponent < 2^d and d<=3H/2+3/2 imply H>(2/3)log2(exponent)-1.
    denominator_cap_twice = 3 * horizon + (2 if horizon % 2 == 0 else 3)
    log_bound_failure_count = int(2 * denominator_power > denominator_cap_twice)
    exponent_cap_failure_count = int(exponent >= 1 << denominator_power)
    total_failures = (
        lift_failure_count
        + range_failure_count
        + valuation_failure_count
        + denominator_failure_count
        + constant_failure_count
        + growth_failure_count
        + log_bound_failure_count
        + exponent_cap_failure_count
    )
    return {
        **exponent_data,
        "post_descent_delay_strict_lower_bound": horizon,
        "logarithmic_lower_bound": "delay > (2/3)*log2(k_H)-1",
        "symbolic_state_count": len(states),
        "lift_failure_count": lift_failure_count,
        "range_failure_count": range_failure_count,
        "valuation_failure_count": valuation_failure_count,
        "denominator_failure_count": denominator_failure_count,
        "constant_failure_count": constant_failure_count,
        "growth_failure_count": growth_failure_count,
        "log_bound_failure_count": log_bound_failure_count,
        "exponent_cap_failure_count": exponent_cap_failure_count,
        "total_failure_count": total_failures,
    }


def analyze_two_adic_cycle_bound() -> dict[str, Any]:
    max_d = expected_denominator_power(MAX_HORIZON)
    residues = lift_discrete_log_residues(max_d + 1)
    rows = [audit_horizon(horizon, residues) for horizon in range(MIN_HORIZON, MAX_HORIZON + 1)]
    failures = sum(int(row["total_failure_count"]) for row in rows)
    state_count = sum(int(row["symbolic_state_count"]) for row in rows)
    samples = [row for row in rows if int(row["horizon"]) in SAMPLE_HORIZONS]
    status = (
        "mersenne_two_thirds_log_window_refuted_exactly_no_collatz_resolution"
        if failures == 0
        else "two_adic_cycle_log_delay_audit_inconclusive_no_collatz_resolution"
    )
    return {
        "theorem_name": "MersenneTwoThirdsLogDelayLowerBound",
        "source_ticket": "CO-TICKET-83",
        "delay_definition": "D(k)=min{t>=0: A^(k+t)(2^k-1)<2^k-1}, with infinity if no such t exists.",
        "two_adic_cycle": {
            "exponent_equation": "3^kappa=-13 in the odd 2-adic exponent branch",
            "post_value": "x_0(kappa)=(3^kappa-1)/2=-7",
            "cycle": "-7 --v2=2--> -5 --v2=1--> -7",
            "valuation_word": "2,1,2,1,...",
            "average_valuation": "3/2",
            "natural_number_guard": "kappa and the negative cycle are 2-adic proof devices only; every k_H is a positive ordinary exponent.",
        },
        "explicit_sequence": (
            "For each H, let d_H=1+sum of the first H symbols of 2,1,2,1,..., let r_H be the unique odd residue "
            "modulo 2^(d_H-1) with 3^r_H=-13 mod 2^(d_H+1), and set k_H=r_H+2^(d_H-1)."
        ),
        "statement": (
            "For every H>=2, D(k_H)>H>(2/3)*log2(k_H)-1. Consequently every c*log2(k) "
            "post-expansion Mersenne descent window with fixed c<2/3 fails on infinitely many exponents."
        ),
        "proof_chain": [
            "Odd powers of 3 modulo 2^Q are exactly the residues congruent to 3 modulo 8; since -13=3 mod 8, a unique odd exponent residue r_Q exists modulo 2^(Q-2).",
            "The residue is constructed one bit at a time: exactly one of r and r+2^(Q-2) lifts 3^r=-13 from modulus 2^Q to 2^(Q+1).",
            "The 2-adic post value -7 follows the exact accelerated valuation cycle 2,1 and alternates with -5.",
            "Preserving 3^k=-13 modulo 2^(d_H+1) preserves the exact finite valuation prefix for the positive exponent k_H=r_H+2^(d_H-1).",
            "The symbolic iterates satisfy x_t(k)=(3^(k+t)+c_t)/2^d_t, d_t follows the 2,1 word, and |c_t|<2^(2t+1).",
            "For d_H>=4, k_H>=2^(d_H-1)+1 and the base inequality (3/2)^9>2^5 propagates to give (3/2)^k_H>2^(d_H+1).",
            "This multiplicative margin and the affine bound force x_t(k_H)>2^k_H-1 for every 0<=t<=H, hence D(k_H)>H.",
            "Because k_H<2^d_H and d_H<=3H/2+3/2, one obtains H>(2/3)log2(k_H)-1.",
        ],
        "machine_audit": {
            "min_horizon": MIN_HORIZON,
            "max_horizon": MAX_HORIZON,
            "horizon_case_count": len(rows),
            "hensel_precision_count": len(residues),
            "maximum_precision": max(residues),
            "symbolic_state_count": state_count,
            "total_failure_count": failures,
            "samples": samples,
        },
        "computational_failure_count": failures,
        "theorem_status": status,
        "rejected_candidate_families": [
            {
                "family": "sub_two_thirds_logarithmic_mersenne_window",
                "status": "refuted_by_two_adic_cycle_lifts",
                "counteredge": "D(k_H)>H>(2/3)log2(k_H)-1 on an explicit Hensel-lifted positive exponent sequence.",
            },
            {
                "family": "positive_reference_orbit_is_coefficient_optimal",
                "status": "refuted_by_accessible_two_adic_cycle",
                "counteredge": "The positive reference tail has mean valuation 2, while the accessible -7/-5 2-adic cycle has mean 3/2 and improves the coefficient from 1/2 to 2/3.",
            },
            {
                "family": "two_adic_ghost_is_a_natural_counterexample",
                "status": "forbidden_category_error",
                "counteredge": "Only finite exponent residues are lifted to positive integers; the negative 2-adic cycle itself is never classified as a natural orbit.",
            },
        ],
        "discarded_route": "Treat the TICKET83 positive reference orbit and its coefficient 1/2 as optimal, or promote the negative 2-adic cycle itself to a natural counterexample.",
        "retained_route": "Classify accessible periodic 2-adic exponent cycles by mean valuation, lift only finite prefixes to positive exponents, and optimize the rigorous logarithmic delay coefficient.",
        "candidate_theorem": (
            "AccessibleCycleCoefficientSupremum: classify all periodic accelerated valuation words whose 2-adic cycle lies in the exponent image x=(3^kappa-1)/2, "
            "and determine the supremum of reciprocal mean valuation subject to exact positive-exponent lifts."
        ),
        "next_theorem_target": "AccessibleCycleCoefficientSupremum",
        "equivalence_warning": "A stronger finite-delay lower bound still does not imply divergence. The 2-adic cycle is a prefix generator, not a positive Collatz orbit.",
        "literature_context": [
            {
                "citation": "Bernstein and Lagarias, The 3x+1 Conjugacy Map, Canadian Journal of Mathematics 48 (1996)",
                "url": "https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13",
                "role": "Established 2-adic conjugacy and finite-prefix context.",
            },
            {
                "citation": "Terras, A stopping time problem on the positive integers, Acta Arithmetica 30 (1976)",
                "url": "https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers",
                "role": "Established stopping-time and parity-vector context.",
            },
        ],
        "novelty_boundary": (
            "2-adic cycles and prefix lifting are established ideas. PrimeProject claims only this accessible exponent-cycle construction, "
            "the explicit two-thirds logarithmic corollary, and its reproducible audit; novelty requires independent literature review."
        ),
        "proof_boundary": "TICKET84 proves a restricted finite-delay lower bound. It proves neither divergence nor the Collatz conjecture nor any of the other three open problems.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "completion-cycle finite-prefix lift transfer discipline",
        "attempt": "Transfer only the discipline of using completion-space objects to generate finite target-domain obstructions without identifying the completion object with a target-domain counterexample.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket84_transfer": route, "candidate_theorem": target},
        "obstruction": "No problem-specific accessible completion cycle was proved for this problem.",
        "candidate_theorem": target,
        "next_experiment": "Classify target-specific completion objects and prove finite-prefix lift admissibility.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket83 = read_json(ROOT / "data/open-problem/ticket83-mersenne-log-window-lower-bound-lab.json")
    collatz_audit = analyze_two_adic_cycle_bound()
    attempts = [
        transfer_attempt(ticket83, "riemann", "RH-TICKET-84", "CompletionKernelCycleGuard", "Classify completion-space kernel obstructions without calling them zeta zeros."),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-84",
            "route": "MersenneTwoThirdsLogDelayLowerBound",
            "status": collatz_audit["theorem_status"],
            "proof_or_counterexample_mode": "accessible two-adic exponent cycle plus positive finite-prefix Hensel lifts",
            "attempt": "Improve the certified logarithmic Mersenne delay coefficient beyond the positive-reference limit 1/2.",
            "bounded_result": {"source_ticket": "CO-TICKET-83", "two_adic_cycle_log_delay_audit": collatz_audit},
            "obstruction": collatz_audit["discarded_route"],
            "candidate_theorem": collatz_audit["candidate_theorem"],
            "next_experiment": "Build TICKET85 to enumerate accessible periodic valuation words and optimize reciprocal mean valuation.",
            "claim_boundary": "No Collatz proof and no certified divergent Collatz counterexample.",
        },
        transfer_attempt(ticket83, "goldbach", "GB-TICKET-84", "CompletionCharacterCycleGuard", "Use completion characters only after proving finite even-integer lift consequences."),
        transfer_attempt(ticket83, "twin-prime", "TP-TICKET-84", "CompletionParityCycleGuard", "Use parity-completion cycles only through exact positive-integer gap-2 lift lemmas."),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "two_adic_cycle_log_delay_open_no_collatz_resolution",
        "claim_boundary": "Ticket 84 proves one restricted Mersenne delay lower bound but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket84-two-adic-cycle-log-delay-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-84-two-adic-cycle-log-delay.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-84-two-adic-cycle-log-delay.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-84-two-adic-cycle-log-delay.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-84-two-adic-cycle-log-delay.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
