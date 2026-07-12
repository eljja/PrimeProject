from __future__ import annotations

import math
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, v2, write_json


GENERATED_AT = "2026-07-11T10:40:00+09:00"
SCHEMA = "primeproject.ticket79-archimedean-two-adic-rank-no-go-lab.v1"
MAX_EXPANSION_DEPTH = 256
EXPANSION_Q_VALUES = (1, 2, 7, 31)
MAX_CONTRACTION_DEPTH = 128
LOG_COEFFICIENTS = (
    Fraction(-4, 1),
    Fraction(-1, 1),
    Fraction(-1, 4),
    Fraction(0, 1),
    Fraction(1, 4),
    Fraction(1, 1),
    Fraction(4, 1),
)
CORRECTION_OSCILLATIONS = (0, 1, 4, 16, 64)
FINITE_STATE_COUNTS = (1, 2, 8, 32, 128)


def accelerated_step(n: int) -> tuple[int, int]:
    numerator = 3 * n + 1
    valuation = v2(numerator)
    return numerator >> valuation, valuation


def expansion_value(m: int, q: int, step: int = 0) -> int:
    return (3**step) * (1 << (m + 1 - step)) * q - 1


def contraction_value(r: int) -> int:
    return (5 * (1 << (2 * r + 1)) - 1) // 3


def audit_exact_families() -> dict[str, Any]:
    expansion_formula_failures = 0
    expansion_valuation_failures = 0
    expansion_growth_failures = 0
    expansion_step_replays = 0
    contraction_formula_failures = 0
    contraction_replay_failures = 0
    expansion_samples: list[dict[str, Any]] = []
    contraction_samples: list[dict[str, Any]] = []

    for m in range(1, MAX_EXPANSION_DEPTH + 1):
        for q in EXPANSION_Q_VALUES:
            start = expansion_value(m, q)
            current = start
            for step in range(m):
                expected = expansion_value(m, q, step)
                if current != expected:
                    expansion_formula_failures += 1
                current, valuation = accelerated_step(current)
                expansion_step_replays += 1
                if valuation != 1:
                    expansion_valuation_failures += 1
            terminal = expansion_value(m, q, m)
            if current != terminal:
                expansion_formula_failures += 1
            # terminal/start > (3/2)^m, checked without floating point.
            if terminal * (1 << m) <= start * (3**m):
                expansion_growth_failures += 1
            if q == 1 and m in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
                expansion_samples.append(
                    {
                        "m": m,
                        "q": q,
                        "start": start,
                        "terminal": terminal,
                        "valuation_word": f"1 repeated {m} times",
                        "exact_formula": "A^j(n)=3^j*2^(m+1-j)*q-1",
                        "growth_exceeds_three_halves_power": True,
                    }
                )

    for r in range(1, MAX_CONTRACTION_DEPTH + 1):
        start = contraction_value(r)
        if 3 * start + 1 != 5 * (1 << (2 * r + 1)) or start % 2 != 1:
            contraction_formula_failures += 1
        terminal, valuation = accelerated_step(start)
        if terminal != 5 or valuation != 2 * r + 1:
            contraction_replay_failures += 1
        if r in {1, 2, 4, 8, 16, 32, 64, 128}:
            contraction_samples.append(
                {
                    "r": r,
                    "start": start,
                    "terminal": terminal,
                    "valuation": valuation,
                    "exact_formula": "n=(5*2^(2r+1)-1)/3 and A(n)=5",
                }
            )

    failure_count = (
        expansion_formula_failures
        + expansion_valuation_failures
        + expansion_growth_failures
        + contraction_formula_failures
        + contraction_replay_failures
    )
    return {
        "max_expansion_depth": MAX_EXPANSION_DEPTH,
        "expansion_q_values": list(EXPANSION_Q_VALUES),
        "expansion_family_case_count": MAX_EXPANSION_DEPTH * len(EXPANSION_Q_VALUES),
        "expansion_step_replay_count": expansion_step_replays,
        "expansion_formula_failure_count": expansion_formula_failures,
        "expansion_valuation_failure_count": expansion_valuation_failures,
        "expansion_growth_failure_count": expansion_growth_failures,
        "max_contraction_depth": MAX_CONTRACTION_DEPTH,
        "contraction_family_case_count": MAX_CONTRACTION_DEPTH,
        "contraction_formula_failure_count": contraction_formula_failures,
        "contraction_replay_failure_count": contraction_replay_failures,
        "exact_family_failure_count": failure_count,
        "expansion_samples": expansion_samples,
        "contraction_samples": contraction_samples,
    }


def first_positive_threshold(alpha: Fraction, oscillation: int) -> int:
    if alpha <= 0:
        raise ValueError("alpha must be positive")
    m = 1
    while float(alpha) * m * math.log(1.5) <= oscillation:
        m += 1
    return m


def first_negative_threshold(alpha: Fraction, oscillation: int) -> int:
    if alpha >= 0:
        raise ValueError("alpha must be negative")
    r = 1
    while -float(alpha) * math.log(contraction_value(r) / 5) <= oscillation:
        r += 1
    return r


def audit_rank_thresholds() -> dict[str, Any]:
    positive_rows: list[dict[str, Any]] = []
    negative_rows: list[dict[str, Any]] = []
    zero_rows: list[dict[str, Any]] = []
    threshold_failures = 0

    for alpha in (value for value in LOG_COEFFICIENTS if value > 0):
        for oscillation in CORRECTION_OSCILLATIONS:
            m = first_positive_threshold(alpha, oscillation)
            margin = float(alpha) * m * math.log(1.5) - oscillation
            if margin <= 0:
                threshold_failures += 1
            positive_rows.append(
                {
                    "alpha": str(alpha),
                    "bounded_correction_oscillation": oscillation,
                    "witness_depth_m": m,
                    "witness_start": expansion_value(m, 1),
                    "lower_bound_on_total_rank_change": round(margin, 12),
                    "status": "strict_one_step_descent_contradicted_by_expansion_block",
                }
            )

    for alpha in (value for value in LOG_COEFFICIENTS if value < 0):
        for oscillation in CORRECTION_OSCILLATIONS:
            r = first_negative_threshold(alpha, oscillation)
            start = contraction_value(r)
            margin = -float(alpha) * math.log(start / 5) - oscillation
            if margin <= 0:
                threshold_failures += 1
            negative_rows.append(
                {
                    "alpha": str(alpha),
                    "bounded_correction_oscillation": oscillation,
                    "witness_r": r,
                    "witness_start": start,
                    "terminal": 5,
                    "lower_bound_on_one_step_rank_change": round(margin, 12),
                    "status": "strict_one_step_descent_contradicted_by_exact_contraction",
                }
            )

    for state_count in FINITE_STATE_COUNTS:
        m = state_count
        zero_rows.append(
            {
                "finite_state_count": state_count,
                "witness_depth_m": m,
                "path_vertex_count": m + 1,
                "witness_start": expansion_value(m, 1),
                "status": "strict_descent_contradicted_by_pigeonhole_repeated_state",
                "reason": "m+1 path vertices mapped to at most m states force a repeated state.",
            }
        )

    return {
        "log_coefficient_grid": [str(value) for value in LOG_COEFFICIENTS],
        "correction_oscillation_grid": list(CORRECTION_OSCILLATIONS),
        "finite_state_count_grid": list(FINITE_STATE_COUNTS),
        "positive_alpha_certificate_count": len(positive_rows),
        "negative_alpha_certificate_count": len(negative_rows),
        "zero_alpha_certificate_count": len(zero_rows),
        "threshold_failure_count": threshold_failures,
        "positive_alpha_rows": positive_rows,
        "negative_alpha_rows": negative_rows,
        "zero_alpha_rows": zero_rows,
        "scope": "Threshold rows illustrate the exact theorem; the proof itself is symbolic and not limited to this grid.",
    }


def analyze_rank_no_go() -> dict[str, Any]:
    family_audit = audit_exact_families()
    threshold_audit = audit_rank_thresholds()
    computational_failures = int(family_audit["exact_family_failure_count"]) + int(
        threshold_audit["threshold_failure_count"]
    )
    status = (
        "bounded_archimedean_two_adic_one_step_rank_refuted_exactly_no_collatz_resolution"
        if computational_failures == 0
        else "archimedean_two_adic_rank_audit_inconclusive_no_collatz_resolution"
    )
    return {
        "theorem_name": "BoundedTwoAdicCorrectionOneStepRankNoGo",
        "source_ticket": "CO-TICKET-78",
        "rank_family": "R(n)=alpha*log(n)+b(s(n)), with finite state set S and b:S->R",
        "stronger_nonzero_scope": (
            "For alpha!=0 the same contradiction holds whenever the correction term is merely bounded, even if it uses "
            "growing 2-adic precision or infinitely many states."
        ),
        "exact_witness_families": {
            "expansion": {
                "start": "E_(m,q)=2^(m+1)*q-1",
                "iterate": "A^j(E_(m,q))=3^j*2^(m+1-j)*q-1 for 0<=j<=m",
                "valuation_word": "v2(3*A^j(E_(m,q))+1)=1 for 0<=j<m",
                "growth": "A^m(E_(m,q))/E_(m,q)>(3/2)^m",
            },
            "contraction": {
                "start": "D_r=(5*2^(2r+1)-1)/3",
                "valuation": "v2(3*D_r+1)=2r+1",
                "terminal": "A(D_r)=5",
            },
        },
        "proof_chain": [
            "For every m,q>=1, direct induction gives the expansion formula and an exact valuation-1 word of length m.",
            "If alpha>0 and osc(b)=W, the total rank change along that block exceeds alpha*m*log(3/2)-W, which is positive for sufficiently large m.",
            "If alpha<0, the exact nonterminal contraction D_r->5 changes the log term by -alpha*log(D_r/5); this exceeds W for sufficiently large r.",
            "If alpha=0 and b factors through K states, the K+1 vertices of an expansion block of length K contain a repeated state, contradicting strict decrease on every intervening edge.",
            "Therefore no member of the stated rank family strictly decreases on every accelerated Collatz edge outside the known basin.",
            "The argument does not exclude adaptive multi-step descent, an unbounded history correction, or an ordinal/well-founded rank with a separately proved lower bound.",
        ],
        "machine_audit": {
            "exact_families": family_audit,
            "rank_thresholds": threshold_audit,
        },
        "computational_failure_count": computational_failures,
        "theorem_status": status,
        "rejected_candidate_families": [
            {
                "family": "positive_log_height_plus_bounded_two_adic_correction",
                "status": "refuted_by_arbitrarily_long_exact_expansion_blocks",
                "counteredge": "E_(m,q) realizes m valuation-1 steps and grows by more than (3/2)^m.",
            },
            {
                "family": "negative_log_height_plus_bounded_two_adic_correction",
                "status": "refuted_by_unbounded_exact_one_step_contractions",
                "counteredge": "D_r grows without bound but maps to the nonterminal value 5 in one accelerated step.",
            },
            {
                "family": "zero_log_finite_state_correction",
                "status": "refuted_by_pigeonhole_on_arbitrarily_long_natural_paths",
                "counteredge": "A valuation-1 block with K edges has K+1 natural vertices but only K states.",
            },
        ],
        "discarded_route": (
            "Seek a universal one-step strict Lyapunov function by adding any bounded 2-adic or finite-state correction "
            "to a fixed multiple of log(n). Exact natural expansion and contraction families defeat every coefficient."
        ),
        "retained_route": (
            "Use an adaptive stopping time or an unbounded, demonstrably well-founded correction. Any proposal must prove "
            "both descent and a global lower bound; fitting a bounded residue table is no longer admissible."
        ),
        "candidate_theorem": (
            "MinimalCounterexampleValuationSurplusContradiction: assuming a least Collatz counterexample N, its exact "
            "valuation words satisfy the non-descent inequalities 2^S*N<=3^m*N+C_m for every prefix; combine these "
            "inequalities with cylinder congruences to force an impossible prefix."
        ),
        "next_theorem_target": "MinimalCounterexampleValuationSurplusContradiction",
        "equivalence_warning": (
            "Proving that every n>1 has an accelerated iterate below n is already equivalent to Collatz by strong induction. "
            "It must not be presented as a weaker solved bridge."
        ),
        "literature_context": [
            {
                "citation": "Bernstein and Lagarias, The 3x+1 Conjugacy Map, Canadian Journal of Mathematics 48 (1996), 1154-1169",
                "url": "https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13",
                "role": "Primary source for 2-adic shift conjugacy and finite parity-prefix realizability context.",
            },
            {
                "citation": "Tao, Almost all orbits of the Collatz map attain almost bounded values, Forum of Mathematics, Pi 10 (2022)",
                "url": "https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/almost-all-orbits-of-the-collatz-map-attain-almost-bounded-values/1008CC2DF91AF87F66D190C5E01C907F",
                "role": "Primary context separating almost-all logarithmic-density descent from an all-integer proof.",
            },
        ],
        "novelty_boundary": (
            "Arbitrarily prescribed finite parity behavior and 2-adic conjugacy are established mathematics. PrimeProject "
            "claims only the explicit two-family no-go formulation for this bounded Archimedean-plus-2-adic rank class, "
            "its machine audit, and its integration into the existing proof-search ledger."
        ),
        "proof_boundary": (
            "TICKET79 proves a restricted no-go theorem for universal one-step ranks of the displayed form. It neither proves "
            "nor disproves Collatz and says nothing by itself about adaptive block descent or unbounded well-founded ranks."
        ),
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    candidate_theorem: str,
) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "bounded-correction no-go transfer discipline",
        "attempt": (
            "Transfer only the methodological guard from TICKET79: a bounded local correction cannot be assumed to repair "
            "an unbounded global obstruction. No Collatz witness family or theorem is transferred to this problem."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "ticket79_transfer": route,
            "candidate_theorem": candidate_theorem,
        },
        "obstruction": "No problem-specific unbounded witness family or bounded-correction no-go theorem was proved here.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Derive a problem-specific exact unbounded witness family before applying this guard.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket78 = read_json(ROOT / "data/open-problem/ticket78-finite-cylinder-admissibility-no-go-lab.json")
    collatz_audit = analyze_rank_no_go()
    attempts = [
        transfer_attempt(
            ticket78,
            "riemann",
            "RH-TICKET-79",
            "UnboundedHeightKernelCorrectionGuard",
            "Any positivity certificate must control the all-height analytic tail with an unbounded quantitative margin, not a bounded finite-kernel correction.",
        ),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-79",
            "route": "ArchimedeanTwoAdicOneStepRankNoGo",
            "status": collatz_audit["theorem_status"],
            "proof_or_counterexample_mode": "exact infinite witness families plus symbolic coefficient trichotomy",
            "attempt": (
                "Test the TICKET78 continuation target by coupling log-height to bounded 2-adic state, then attack every "
                "coefficient sign with exact positive-integer Collatz families."
            ),
            "bounded_result": {"source_ticket": "CO-TICKET-78", "archimedean_two_adic_rank_no_go_audit": collatz_audit},
            "obstruction": collatz_audit["discarded_route"],
            "candidate_theorem": collatz_audit["candidate_theorem"],
            "next_experiment": "Build TICKET80 around the least-counterexample non-descent inequalities and exact cylinder congruences.",
            "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
        },
        transfer_attempt(
            ticket78,
            "goldbach",
            "GB-TICKET-79",
            "UnboundedExceptionalTailCorrectionGuard",
            "A Goldbach positivity proof must dominate the unbounded exceptional analytic tail rather than append a bounded residue correction.",
        ),
        transfer_attempt(
            ticket78,
            "twin-prime",
            "TP-TICKET-79",
            "UnboundedParityBarrierCorrectionGuard",
            "An exact gap-2 lower bound must break the parity barrier with an unbounded quantitative estimate rather than a bounded finite sieve-state correction.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "archimedean_two_adic_rank_no_go_open_no_collatz_resolution",
        "claim_boundary": "Ticket 79 proves one restricted Collatz rank no-go theorem but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket79-archimedean-two-adic-rank-no-go-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-79-archimedean-two-adic-rank-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-79-archimedean-two-adic-rank-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-79-archimedean-two-adic-rank-no-go.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-79-archimedean-two-adic-rank-no-go.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
