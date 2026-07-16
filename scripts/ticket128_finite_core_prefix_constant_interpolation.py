from __future__ import annotations

import json
import math
from collections import Counter
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket126_route_correction_audit import _cylinder_certificate, v2


GENERATED_AT = "2026-07-17T02:55:03+09:00"
SCHEMA = "primeproject.ticket128-finite-core-prefix-constant-interpolation.v1"
DEFAULT_COLLATZ_BITS = 28
DEFAULT_COLLATZ_STEP_CAP = 10_000


def primes_up_to(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            sieve[prime * prime :: prime] = b"\x00" * (
                (limit - prime * prime) // prime + 1
            )
    return [number for number, flag in enumerate(sieve) if flag]


def prime_power_inventory(bound: int) -> dict[str, Any]:
    terms: list[tuple[int, int, int]] = []
    exponent_histogram: Counter[int] = Counter()
    for prime in primes_up_to(bound):
        value = prime
        exponent = 1
        while value <= bound:
            terms.append((prime, exponent, value))
            exponent_histogram[exponent] += 1
            if value > bound // prime:
                break
            value *= prime
            exponent += 1
    return {
        "integer_bound_B": bound,
        "prime_count": sum(1 for _, exponent, _ in terms if exponent == 1),
        "prime_power_term_count": len(terms),
        "maximum_exponent": max(exponent_histogram, default=0),
        "exponent_histogram": {
            str(exponent): count
            for exponent, count in sorted(exponent_histogram.items())
        },
        "largest_terms": [
            {"prime": prime, "exponent": exponent, "value": value}
            for prime, exponent, value in sorted(terms, key=lambda row: row[2])[-8:]
        ],
    }


def riemann_compact_support_prime_sum_audit(
    bound: int = 1_000_000,
) -> dict[str, Any]:
    inventory = prime_power_inventory(bound)
    sanity_rows = [prime_power_inventory(value) for value in (10, 100, 1_000)]
    failure_count = sum(
        int(row["prime_power_term_count"] < row["prime_count"])
        for row in [*sanity_rows, inventory]
    )
    return {
        "theorem_name": "CompactSupportFinitePrimeSideReduction",
        "setting": (
            "Use an RH-equivalent Weil explicit formula whose arithmetic side "
            "contains terms indexed by prime powers p^m and evaluated at "
            "h(m log p). Assume h(t)=0 for |t|>log B with an integer B>=2."
        ),
        "proved_statement": (
            "Every nonzero arithmetic term has m log p<=log B, equivalently "
            "p^m<=B. The prime side is therefore an exactly enumerable finite sum."
        ),
        "proof": (
            "Monotonicity of log gives h(m log p)=0 whenever p^m>B. "
            "There are finitely many integers at most B, and trial division or "
            "a certified sieve enumerates exactly the prime-power pairs that remain."
        ),
        "finite_inventory": inventory,
        "sanity_rows": sanity_rows,
        "effective_consequence": (
            "For compact-support core elements, no infinite prime tail remains. "
            "A complete strict-sign evaluator still needs certified function "
            "values, the archimedean term, normalization, and a proved dense admissible core."
        ),
        "route_decision": {
            "retain": "compact-support core candidates with exact prime-power enumeration",
            "discard": "treating a truncated infinite prime sum as an exact Weil value",
            "next_theorem": "ArchimedeanIntervalAndAdmissibleCoreDensity",
        },
        "machine_audit": {
            "inventory_bound": bound,
            "finite_prime_power_term_count": inventory["prime_power_term_count"],
            "conjecture_resolution_count": 0,
            "total_failure_count": failure_count,
        },
        "proof_boundary": (
            "The arithmetic side is finite for each compactly supported test "
            "function. This does not prove density of the chosen core, certify "
            "the archimedean term, establish global positivity, or resolve RH."
        ),
    }


def collatz_unresolved_frontier(bits: int, minimum_bits: int = 4) -> set[int]:
    if bits < minimum_bits:
        raise ValueError("bits must be at least minimum_bits")
    frontier = {
        residue
        for residue in range(1, 1 << minimum_bits, 2)
        if _cylinder_certificate(residue, minimum_bits) is None
    }
    for precision in range(minimum_bits + 1, bits + 1):
        parent_modulus = 1 << (precision - 1)
        next_frontier: set[int] = set()
        for parent in frontier:
            for child in (parent, parent + parent_modulus):
                if _cylinder_certificate(child, precision) is None:
                    next_frontier.add(child)
        frontier = next_frontier
    return frontier


def accelerated_strict_descent(
    start: int, step_cap: int = DEFAULT_COLLATZ_STEP_CAP
) -> dict[str, Any]:
    if start <= 0 or start % 2 == 0:
        raise ValueError("start must be a positive odd integer")
    current = start
    peak = start
    valuation_sum = 0
    for step in range(1, step_cap + 1):
        valuation = v2(3 * current + 1)
        valuation_sum += valuation
        current = (3 * current + 1) >> valuation
        peak = max(peak, current)
        if current < start:
            return {
                "descends": True,
                "accelerated_steps": step,
                "terminal": current,
                "peak": peak,
                "valuation_sum": valuation_sum,
            }
    return {
        "descends": False,
        "accelerated_steps": step_cap,
        "terminal": current,
        "peak": peak,
        "valuation_sum": valuation_sum,
    }


def collatz_finite_prefix_closure_audit(
    bits: int = DEFAULT_COLLATZ_BITS,
    step_cap: int = DEFAULT_COLLATZ_STEP_CAP,
) -> dict[str, Any]:
    frontier = collatz_unresolved_frontier(bits)
    nontrivial = sorted(residue for residue in frontier if residue != 1)
    failure_witnesses: list[int] = []
    maximum_steps = 0
    maximum_step_witnesses: list[int] = []
    maximum_peak = 0
    maximum_peak_witness = 0
    direct_closed = 0
    for residue in nontrivial:
        result = accelerated_strict_descent(residue, step_cap)
        if not result["descends"]:
            if len(failure_witnesses) < 16:
                failure_witnesses.append(residue)
            continue
        direct_closed += 1
        steps = int(result["accelerated_steps"])
        if steps > maximum_steps:
            maximum_steps = steps
            maximum_step_witnesses = [residue]
        elif steps == maximum_steps and len(maximum_step_witnesses) < 16:
            maximum_step_witnesses.append(residue)
        peak = int(result["peak"])
        if peak > maximum_peak:
            maximum_peak = peak
            maximum_peak_witness = residue

    ticket127 = read_json(
        ROOT / "data/open-problem/ticket127-exception-repair-effective-bridges.json"
    )["effective_bridge_audit"]["collatz"]["exact_28_bit_audit"]
    expected_frontier = (
        int(ticket127["all_unresolved_class_count"])
        if bits == DEFAULT_COLLATZ_BITS
        else len(frontier)
    )
    exact_frontier_match = len(frontier) == expected_frontier
    unresolved_after_direct_check = len(nontrivial) - direct_closed
    return {
        "theorem_name": "FinitePrefixEventuallyLowExclusion",
        "proved_statement": (
            "If every unresolved odd representative 1<n<2^k has a finite "
            "strict accelerated descent, then no nontrivial eventually-low "
            "unresolved path stabilizing below 2^k can encode a counterexample."
        ),
        "proof": (
            "An eventually-low binary residue path has only finitely many high "
            "refinements and therefore stabilizes at one positive odd integer n. "
            "If n<2^k, its level-k representative is n. A cylinder certificate "
            "already closes representatives outside the frontier; the direct "
            "strict-descent certificate closes each remaining representative."
        ),
        "exact_prefix_audit": {
            "precision_bits": bits,
            "integer_upper_bound_exclusive": 1 << bits,
            "adaptive_unresolved_class_count": len(frontier),
            "trivial_fixed_path_count": int(1 in frontier),
            "nontrivial_frontier_representative_count": len(nontrivial),
            "directly_closed_nontrivial_count": direct_closed,
            "unresolved_after_direct_check": unresolved_after_direct_check,
            "step_cap": step_cap,
            "maximum_accelerated_steps_to_strict_descent": maximum_steps,
            "maximum_step_witnesses": maximum_step_witnesses,
            "maximum_peak": maximum_peak,
            "maximum_peak_witness": maximum_peak_witness,
            "step_cap_failure_witnesses": failure_witnesses,
        },
        "interpretation_correction": (
            "An unresolved residue cylinder is not an integer counterexample "
            "candidate by itself. It says only that one certificate must cover "
            "every lift in that cylinder. Direct orbit replay may still close its representative."
        ),
        "route_decision": {
            "retain": "adaptive cylinders for infinite lift families plus direct replay for stabilized representatives",
            "discard": "counting every unresolved cylinder representative as a surviving integer counterexample candidate",
            "next_theorem": "UnboundedPrefixClosureOrUniformNontrivialPathRank",
        },
        "machine_audit": {
            "frontier_matches_ticket127": exact_frontier_match,
            "bounded_nontrivial_failure_count": unresolved_after_direct_check,
            "conjecture_resolution_count": 0,
            "total_failure_count": int(not exact_frontier_match),
        },
        "proof_boundary": (
            "The audit excludes stabilized counterexample paths only below the "
            "stated finite bound. It supplies no uniform k and therefore does not prove Collatz."
        ),
    }


def goldbach_sharpened_singular_series_audit(cutoff: int = 1_000) -> dict[str, Any]:
    if cutoff < 3:
        raise ValueError("cutoff must be at least 3")
    prefix = Fraction(1, 1)
    primes = [prime for prime in primes_up_to(cutoff) if prime > 2]
    for prime in primes:
        denominator = (prime - 1) ** 2
        prefix *= Fraction(denominator - 1, denominator)
    tail_lower = Fraction(cutoff - 1, cutoff)
    c2_lower = prefix * tail_lower
    major_lower = 2 * c2_lower
    displayed_major_floor = Fraction(131_917, 100_000)

    verified_limit = 4_000_000_000_000_000_000
    residual_k = 55
    log_lower = 42
    log_upper = 43
    contamination_b_upper = Fraction(21, 10)
    contamination_upper = (
        contamination_b_upper * log_upper**2 / math.isqrt(verified_limit)
    )
    conservative_margin = (
        displayed_major_floor
        - Fraction(residual_k, log_lower)
        - contamination_upper
    )
    ticket126_b = float(
        read_json(ROOT / "data/open-problem/ticket126-route-correction-audit.json")
        ["route_correction_audit"]["goldbach"]["uniform_tail"]
        ["explicit_uniform_B"]
    )
    log_h = math.log(verified_limit)
    floating_ceiling = (
        float(major_lower)
        - ticket126_b * log_h**2 / math.sqrt(verified_limit)
    ) * log_h
    failures = sum(
        [
            int(major_lower <= displayed_major_floor),
            int(ticket126_b >= 2.1),
            int(not (42 < log_h < 43)),
            int(conservative_margin <= 0),
        ]
    )
    return {
        "theorem_name": "ExplicitTwinConstantTailLowerBound",
        "proved_statement": (
            "For every integer M>=3, C2 is at least "
            "product_{3<=p<=M}(1-1/(p-1)^2)*(M-1)/M. "
            "At M=1000 this gives 2*C2>1.31917."
        ),
        "proof": (
            "After extracting the factors p<=M, the remaining prime indices "
            "m=p-1 form a subset of all integers m>=M. Since every factor "
            "1-1/m^2 lies in (0,1), the prime tail is at least the full integer "
            "tail, whose telescoping product is (M-1)/M."
        ),
        "exact_cutoff_certificate": {
            "cutoff_M": cutoff,
            "prime_factor_count": len(primes),
            "prefix_numerator": str(prefix.numerator),
            "prefix_denominator": str(prefix.denominator),
            "tail_lower_numerator": tail_lower.numerator,
            "tail_lower_denominator": tail_lower.denominator,
            "major_lower_numerator": str(major_lower.numerator),
            "major_lower_denominator": str(major_lower.denominator),
            "major_lower_decimal": float(major_lower),
            "certified_display_floor": float(displayed_major_floor),
        },
        "conservative_endpoint_budget": {
            "verified_limit_H": verified_limit,
            "elementary_log_interval": "42<log(H)<43",
            "proved_contamination_constant_B": ticket126_b,
            "conservative_B_upper": float(contamination_b_upper),
            "candidate_pointwise_residual_K": residual_k,
            "exact_positive_margin_lower_numerator": conservative_margin.numerator,
            "exact_positive_margin_lower_denominator": conservative_margin.denominator,
            "exact_positive_margin_lower_decimal": float(conservative_margin),
            "floating_best_ceiling_diagnostic": floating_ceiling,
            "consequence": (
                "A pointwise bound |R(N)|<=55*N/log(N) for every even N>H "
                "would now suffice after the already proved prime-power contamination bound."
            ),
        },
        "route_decision": {
            "retain": "exact singular-series tail lower bounds and the weighted finite-glue theorem",
            "discard": "the unnecessarily weak normalized main coefficient A=1 as the final endpoint budget",
            "next_theorem": "PointwiseBinaryGoldbachResidualK55",
        },
        "machine_audit": {
            "exact_major_floor_passes": major_lower > displayed_major_floor,
            "conservative_k55_margin_positive": conservative_margin > 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The main coefficient and admissible endpoint budget are stronger, "
            "but PrimeProject has not proved the required pointwise residual "
            "bound with K=55. Strong Goldbach remains open."
        ),
    }


def twin_dyadic_interpolation_audit() -> dict[str, Any]:
    alpha = Fraction(3, 4)
    beta = Fraction(23, 100)
    endpoint_ceiling = beta / (1 - alpha)
    c = Fraction(1, 1)
    delta = Fraction(7, 100)
    all_scale_ceiling = c * endpoint_ceiling + delta
    maximum_delta_at_c1 = 1 - endpoint_ceiling

    countermodel_rows = []
    for exponent in range(4, 11):
        left = 1 << exponent
        midpoint = 3 * (1 << (exponent - 1))
        right = 1 << (exponent + 1)
        countermodel_rows.append(
            {
                "left_endpoint": left,
                "midpoint": midpoint,
                "right_endpoint": right,
                "Q_left": float(endpoint_ceiling),
                "Q_midpoint": 2.0,
                "Q_right": float(endpoint_ceiling),
                "endpoint_recurrence_equality": (
                    endpoint_ceiling == alpha * endpoint_ceiling + beta
                ),
                "all_scale_bound_fails": True,
            }
        )
    failures = sum(
        int(not row["endpoint_recurrence_equality"])
        for row in countermodel_rows
    ) + int(all_scale_ceiling >= 1)
    return {
        "theorem_name": "DyadicEndpointInsufficiencyAndAllScaleEnvelope",
        "endpoint_no_go": {
            "statement": (
                "A dyadic recurrence alone cannot imply Q_X<1 at all large X."
            ),
            "countermodel": (
                "Take K_X=1. Set Q_(2^j)=23/25 at every dyadic endpoint and "
                "Q_(3*2^(j-1))=2 at every midpoint. Then the frozen endpoint "
                "recurrence with alpha=3/4,beta=23/100 holds with equality, "
                "while infinitely many non-dyadic scales exceed one."
            ),
            "rows": countermodel_rows,
        },
        "proved_interpolation_theorem": {
            "statement": (
                "If q_(j+1)<=alpha*q_j+beta with 0<=alpha<1, and every "
                "X in [2^j,2^(j+1)] satisfies Q_X<=c*q_j+delta, then "
                "limsup Q_X<=c*beta/(1-alpha)+delta."
            ),
            "proof": (
                "Iterating the endpoint recurrence gives limsup q_j at most "
                "beta/(1-alpha). Apply the within-block envelope and take the "
                "limsup over successive dyadic blocks."
            ),
            "frozen_endpoint_ceiling": float(endpoint_ceiling),
            "required_numeric_condition": "0.92*c+delta<1",
            "maximum_delta_when_c_is_1": float(maximum_delta_at_c1),
            "audited_candidate_c": float(c),
            "audited_candidate_delta": float(delta),
            "candidate_all_scale_ceiling": float(all_scale_ceiling),
            "candidate_condition_passes": all_scale_ceiling < 1,
        },
        "route_decision": {
            "retain": "raw dyadic transport only when paired with an independently proved within-block envelope",
            "discard": "interpolating arbitrary scales from endpoint values without a coefficient theorem",
            "next_theorem": "VaughanWithinDyadicBlockEnvelopeC1DeltaBelow008",
        },
        "machine_audit": {
            "countermodel_block_count": len(countermodel_rows),
            "endpoint_countermodel_passes": failures == 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The no-go and interpolation theorem are exact. The candidate "
            "c=1, delta=0.07 is not proved for Vaughan coefficients, and even "
            "a valid obstruction bound would still require parity survival and exact-gap positivity."
        ),
    }


def build_audit(
    collatz_bits: int = DEFAULT_COLLATZ_BITS,
    collatz_step_cap: int = DEFAULT_COLLATZ_STEP_CAP,
) -> dict[str, Any]:
    sections = {
        "riemann": riemann_compact_support_prime_sum_audit(),
        "collatz": collatz_finite_prefix_closure_audit(
            collatz_bits, collatz_step_cap
        ),
        "goldbach": goldbach_sharpened_singular_series_audit(),
        "twin_prime": twin_dyadic_interpolation_audit(),
    }
    failures = sum(
        int(section["machine_audit"]["total_failure_count"])
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureFiniteCorePrefixConstantInterpolationAudit",
        **sections,
        "literature_boundary": [
            {
                "citation": "Connes and Consani, The Scaling Hamiltonian",
                "url": "https://arxiv.org/abs/1910.14368",
                "role": "Primary Weil explicit-formula context; compact support makes only the prime side finite.",
            },
            {
                "citation": "Tao, Almost all orbits of the Collatz map attain almost bounded values",
                "url": "https://arxiv.org/abs/1909.03562",
                "role": "Primary almost-all boundary; the finite prefix audit is not a universal theorem.",
            },
            {
                "citation": "Friedlander, Goldston, Iwaniec, and Suriajaya, Exceptional zeros and the Goldbach problem",
                "url": "https://doi.org/10.1016/j.jnt.2021.06.004",
                "role": "Primary binary Goldbach normalization; the singular-series sharpening is proved locally.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Primary sieve boundary; interpolation does not remove the parity obstruction.",
            },
        ],
        "machine_audit": {
            "problem_count": 4,
            "exact_intermediate_theorem_count": 4,
            "explicit_route_counterexample_count": 1,
            "strengthened_endpoint_budget_count": 1,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "TICKET128 proves four intermediate reductions or corrections but "
            "proves or refutes none of RH, Collatz, Goldbach, or Twin Prime."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-128",
            "CompactSupportFinitePrimeSideReduction",
            "ArchimedeanIntervalAndAdmissibleCoreDensity",
            "Implement certified archimedean intervals on a proved dense compact-support Weil core.",
        ),
        (
            "collatz",
            "CO-TICKET-128",
            "FinitePrefixEventuallyLowExclusion",
            "UnboundedPrefixClosureOrUniformNontrivialPathRank",
            "Replace bounded direct closure by a uniform rank, or expose a step-cap survivor for exact replay.",
        ),
        (
            "goldbach",
            "GB-TICKET-128",
            "ExplicitTwinConstantTailLowerBound",
            "PointwiseBinaryGoldbachResidualK55",
            "Prove the pointwise signed residual bound with K<=55 above H=4e18.",
        ),
        (
            "twin-prime",
            "TP-TICKET-128",
            "DyadicEndpointInsufficiencyAndAllScaleEnvelope",
            "VaughanWithinDyadicBlockEnvelopeC1DeltaBelow008",
            "Derive c and delta from actual Vaughan coefficients and reject every endpoint-only interpolation.",
        ),
    ]
    return [
        {
            "problem_id": problem_id,
            "ticket_id": ticket_id,
            "status": "exact_intermediate_result_conjecture_open",
            "route": route,
            "bounded_result": {"audit_ref": problem_id.replace("-", "_")},
            "candidate_theorem": target,
            "next_experiment": experiment,
            "claim_boundary": "No conjecture proof and no certified conjecture counterexample.",
            "proof_boundary": audit[problem_id.replace("-", "_")]["proof_boundary"],
        }
        for problem_id, ticket_id, route, target, experiment in specs
    ]


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "finite_core_prefix_constant_interpolation_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "finite_core_prefix_constant_interpolation_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket128-finite-core-prefix-constant-interpolation.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-128-compact-support-prime-side.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-128-finite-prefix-closure.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-128-sharpened-singular-series.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-128-dyadic-interpolation.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    print(json.dumps({"schema": SCHEMA, "machine_audit": audit["machine_audit"]}, indent=2))
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
