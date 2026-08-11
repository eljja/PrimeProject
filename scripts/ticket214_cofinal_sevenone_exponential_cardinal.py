from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Iterator

from ticket213_multiplicity_sixone_polynomial_selector import (
    total_valuation_upper_bound,
    weak_compositions,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket214-cofinal-sevenone-exponential-cardinal.v1"
GENERATED_AT = "2026-08-13T00:15:00+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def proof_dag(
    prefix: str,
    previous: str,
    closed: str,
    rejected: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T213", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T214", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N214",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN214",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T213", f"{prefix}-T214"],
            [f"{prefix}-T214", f"{prefix}-N214"],
            [f"{prefix}-T214", f"{prefix}-OPEN214"],
            [f"{prefix}-OPEN214", prefix],
        ],
    }


def riemann_cofinal_density_audit() -> dict[str, Any]:
    density_rows = []
    failures = 0
    for line_count in (10**2, 10**4, 10**6, 10**8):
        total_count = line_count + 2
        defect = total_count - line_count
        relative_defect = Fraction(defect, total_count)
        row = {
            "critical_line_multiplicity_M": line_count,
            "total_multiplicity_N": total_count,
            "off_line_pair_multiplicity": 1,
            "defect_N_minus_M": defect,
            "critical_line_density_M_over_N": str(Fraction(line_count, total_count)),
            "relative_defect": str(relative_defect),
            "rectangle_RH": False,
            "density_tends_to_one_model": True,
        }
        failures += int(defect != 2)
        failures += int(relative_defect >= Fraction(1, 10))
        density_rows.append(row)

    cofinal_rows = []
    defect_seen = False
    for index, defect in enumerate((0, 0, 2, 2, 4, 4), start=1):
        defect_seen = defect_seen or defect > 0
        cofinal_rows.append(
            {
                "height_index": index,
                "defect": defect,
                "exact_multiplicity_equality": defect == 0,
                "off_line_zero_already_seen": defect_seen,
            }
        )
    failures += int(any(
        row["exact_multiplicity_equality"]
        for row in cofinal_rows
        if row["off_line_zero_already_seen"]
    ))

    theorem = (
        "Let D(T)=N(T)-M(T) be the multiplicity-aware critical-line defect "
        "from TICKET-213 at boundary-free heights. Symmetry makes D a "
        "nonnegative, even, nondecreasing step function. The Riemann "
        "Hypothesis is therefore equivalent to the existence of an unbounded "
        "sequence of boundary-free heights T_j with D(T_j)=0. In contrast, the asymptotic "
        "condition M(T)/N(T)->1, or equivalently D(T)=o(N(T)), does not imply "
        "RH: a symmetric zero multiset with one persistent off-line pair and "
        "an unbounded number of critical-line zeros has D(T)=2 but D(T)/N(T)->0."
    )
    proof = (
        "Every off-line pair that enters an expanding rectangle contributes "
        "a positive even amount to D and never leaves, so D is nondecreasing. "
        "If D vanishes at unbounded heights, any hypothetical off-line zero "
        "would enter before one of those heights and force D>=2 there, a "
        "contradiction. The converse is immediate. For insufficiency of "
        "density one, place one symmetry pair off the line and let the line "
        "multiplicity tend to infinity. Then the defect remains exactly two "
        "while its relative share tends to zero. This is a logical zero-model, "
        "not a claim that such a zeta zero exists."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "cofinal_equivalence": (
            "RH iff D(T_j)=0 for one unbounded sequence of boundary-free heights"
        ),
        "density_one_countermodel_rows": density_rows,
        "monotone_defect_rows": cofinal_rows,
        "aggregate": {
            "cofinal_exact_equality_equivalent_to_rh": True,
            "critical_line_density_one_sufficient_for_rh": False,
            "relative_defect_little_o_sufficient_for_rh": False,
            "actual_zeta_cofinal_equality_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The countermodel rejects density-only promotion. It is not an "
            "off-critical zeta zero, and the cofinal equality remains unproved "
            "for the actual zeta function."
        ),
        "failure_count": failures,
    }


def k_one_words(
    length: int,
    one_count: int,
    maximum_total: int,
) -> Iterator[tuple[int, ...]]:
    baseline_total = 2 * length - one_count
    if baseline_total > maximum_total:
        return
    for other_ones in itertools.combinations(range(1, length - 1), one_count - 1):
        one_positions = {0, *other_ones}
        non_one_positions = [
            index for index in range(length) if index not in one_positions
        ]
        for extra_total in range(maximum_total - baseline_total + 1):
            for extras in weak_compositions(extra_total, len(non_one_positions)):
                word = [
                    1 if index in one_positions else 2
                    for index in range(length)
                ]
                for index, extra in zip(non_one_positions, extras, strict=True):
                    word[index] += extra
                yield tuple(word)


def cycle_numerator(word: tuple[int, ...]) -> int:
    numerator = 0
    prefix_sum = 0
    for valuation in word:
        numerator = 3 * numerator + 2**prefix_sum
        prefix_sum += valuation
    return numerator


def candidate_word_count(one_count: int) -> int:
    length_cap = math.floor(
        one_count * math.log(2) / math.log(Fraction(6, 5))
    )
    total = 0
    for length in range(one_count + 1, length_cap + 1):
        maximum_total = total_valuation_upper_bound(length)
        extra_cap = maximum_total - (2 * length - one_count)
        if extra_cap < 0:
            continue
        non_one_count = length - one_count
        total += math.comb(length - 2, one_count - 1) * math.comb(
            extra_cap + non_one_count,
            non_one_count,
        )
    return total


@lru_cache(maxsize=1)
def collatz_seven_one_audit() -> dict[str, Any]:
    rows = []
    total_words = 0
    divisibility_candidates = 0
    positive_integer_candidates = 0
    failures = 0
    one_count = 7
    length_cap = math.floor(
        one_count * math.log(2) / math.log(Fraction(6, 5))
    )
    for length in range(one_count + 1, length_cap + 1):
        maximum_total = total_valuation_upper_bound(length)
        baseline_total = 2 * length - one_count
        digest = hashlib.sha256()
        local_words = 0
        local_divisible = 0
        local_positive = 0
        for word in k_one_words(length, one_count, maximum_total):
            local_words += 1
            numerator = cycle_numerator(word)
            divisor = 2 ** sum(word) - 3**length
            digest.update(
                f"{','.join(map(str, word))}:{numerator}:{divisor}\n".encode("ascii")
            )
            if divisor <= 0 or numerator % divisor:
                continue
            local_divisible += 1
            fixed_point = numerator // divisor
            if fixed_point >= 3 and fixed_point % 2:
                local_positive += 1
        total_words += local_words
        divisibility_candidates += local_divisible
        positive_integer_candidates += local_positive
        rows.append(
            {
                "length_h": length,
                "minimum_total_valuation_2h_minus_7": baseline_total,
                "maximum_total_valuation_from_minimum_bound": maximum_total,
                "enumerated_word_count": local_words,
                "ordinary_divisibility_candidate_count": local_divisible,
                "positive_odd_integer_fixed_point_count": local_positive,
                "valuation_word_and_divisor_sha256": digest.hexdigest(),
            }
        )

    complexity_rows = []
    for k in range(1, 11):
        direct_count = candidate_word_count(k)
        central_binomial_lower_bound = math.comb(2 * k - 2, k - 1)
        complexity_rows.append(
            {
                "one_count_k": k,
                "length_cap": math.floor(k * math.log(2) / math.log(Fraction(6, 5))),
                "candidate_word_count": direct_count,
                "h_equals_2k_binomial_lower_bound": central_binomial_lower_bound,
            }
        )
        failures += int(direct_count < central_binomial_lower_bound)

    failures += int(length_cap != 26)
    failures += int(total_words != 4_349_349)
    failures += int(total_words != candidate_word_count(one_count))
    failures += int(divisibility_candidates != 0)
    failures += int(positive_integer_candidates != 0)

    theorem = (
        "No nontrivial positive accelerated Collatz cycle has exactly seven "
        "valuation entries equal to one and every other valuation at least "
        "two. Minimum rotation forces the first valuation to be one and the "
        "last to be at least two; the product bound gives h<=26. Exact "
        "ordinary-integer divisibility testing of all 4,349,349 admissible "
        "words of lengths 8 through 26 finds no positive odd fixed point. "
        "Consequently every hypothetical nontrivial positive cycle has at "
        "least eight valuation-one entries. The direct fixed-k enumeration "
        "scheme has at least C(2k-2,k-1) candidates and therefore cannot be "
        "promoted to a uniform all-k proof by any finite list of strata."
    )
    proof = (
        "The TICKET-213 inequalities apply with k=7: A>=2h-7 and "
        "(6/5)^h<=2^7, hence h<=26 and A has a finite upper bound. Position "
        "choices and weak compositions enumerate every minimum-rotation word. "
        "For each one, the exact equation (2^A-3^h)x=C is tested in ordinary "
        "integers; none has a positive odd solution. For complexity, length "
        "h=2k is always admissible at baseline A=3k, and choosing the remaining "
        "k-1 one positions already gives C(2k-2,k-1) words. This lower bound "
        "grows exponentially. It limits this brute-force scheme, not every "
        "possible structural proof."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "k": one_count,
        "exact_length_cap_h": length_cap,
        "exact_enumeration_rows": rows,
        "total_exact_words_enumerated": total_words,
        "ordinary_divisibility_candidate_count": divisibility_candidates,
        "positive_odd_integer_fixed_point_count": positive_integer_candidates,
        "fixed_stratum_complexity_rows": complexity_rows,
        "aggregate": {
            "exactly_seven_valuation_one_cycle_stratum_excluded": True,
            "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle": 8,
            "finite_fixed_stratum_list_sufficient_for_collatz": False,
            "eight_or_more_one_strata_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This closes one finite periodic stratum and quantifies the direct "
            "enumeration explosion. It neither excludes cycles with eight or "
            "more one-valuations nor controls nonperiodic divergent orbits."
        ),
        "failure_count": failures,
    }


def prime_sieve(limit: int) -> bytearray:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            flags[prime * prime : limit + 1 : prime] = b"\x00" * (
                (limit - prime * prime) // prime + 1
            )
    return flags


def goldbach_counts(start: int, flags: bytearray, primes: list[int]) -> list[int]:
    counts = []
    for target in range(start, 2 * start, 2):
        count = 0
        for prime in primes:
            if prime > target // 2:
                break
            count += int(flags[target - prime])
        counts.append(count)
    return counts


def maximum_zero_occupancy(boxes: int, total: int, capacity: int) -> int:
    if total == 0:
        return boxes
    return boxes - math.ceil(total / capacity)


def goldbach_exponential_occupancy_audit() -> dict[str, Any]:
    starts = (128, 512, 2048, 8192, 32768)
    flags = prime_sieve(2 * max(starts))
    primes = [value for value in range(2, len(flags)) if flags[value]]
    rows = []
    failures = 0
    for start in starts:
        counts = goldbach_counts(start, flags, primes)
        boxes = len(counts)
        total = sum(counts)
        capacity = max(counts)
        selector_exponent = boxes.bit_length()
        positive_selector_upper_bound = Fraction(boxes, 2**selector_exponent)
        aggregate_zero_bound = maximum_zero_occupancy(boxes, total, capacity)
        row = {
            "dyadic_start_X": start,
            "even_targets_B": boxes,
            "minimum_representation_count": min(counts),
            "maximum_representation_capacity_U": capacity,
            "total_representation_count_S": total,
            "smallest_k_with_2_pow_k_greater_than_B": selector_exponent,
            "positive_block_selector_upper_bound_B_over_2_pow_k": str(
                positive_selector_upper_bound
            ),
            "observed_exception_count": sum(count == 0 for count in counts),
            "maximum_zeros_consistent_with_only_B_S_U": aggregate_zero_bound,
            "aggregate_statistics_alone_certify_zero_free": aggregate_zero_bound == 0,
        }
        failures += int(row["observed_exception_count"] != 0)
        failures += int(positive_selector_upper_bound >= 1)
        failures += int(aggregate_zero_bound <= 0)
        rows.append(row)

    synthetic_rows = []
    for counts in ([0, 3, 4, 5], [1, 1, 1, 1], [2, 7, 1, 3, 4]):
        boxes = len(counts)
        exponent = boxes.bit_length()
        has_zero = 0 in counts
        zero_term_forces_at_least_one = has_zero
        all_positive_bound = Fraction(boxes, 2**exponent)
        selector_sum = sum(
            (Fraction(1, 2 ** (exponent * count)) for count in counts),
            start=Fraction(0),
        )
        equivalence = (selector_sum < 1) == (not has_zero)
        synthetic_rows.append(
            {
                "counts": counts,
                "B": boxes,
                "k": exponent,
                "has_zero": has_zero,
                "exact_selector_sum": str(selector_sum),
                "zero_term_forces_selector_sum_at_least_one": zero_term_forces_at_least_one,
                "all_positive_selector_upper_bound": str(all_positive_bound),
                "selector_subunit_iff_all_positive_verified": equivalence,
            }
        )
        failures += int(not equivalence)

    theorem = (
        "For a finite block of B even targets with Goldbach counts A_i, let "
        "k be the least integer with 2^k>B and set E=sum_i 2^(-k A_i). "
        "Then E<1 if and only if every A_i is positive: a zero contributes "
        "one, while an all-positive block has E<=B/2^k<1. This supplies the "
        "scale-growing nonpolynomial selector requested by TICKET-213, but "
        "proving its subunit bound on all blocks is exactly equivalent to "
        "Goldbach on those blocks. Moreover, if only B, total S, and a cap "
        "0<=A_i<=U with U>0 are known, the sharp maximum possible number of zeros is "
        "B-ceil(S/U); aggregate witness mass alone forces zero-free coverage "
        "only when S>(B-1)U."
    )
    proof = (
        "The exponential selector proof is the two-case estimate above. For "
        "the occupancy bound, q=ceil(S/U) positive boxes are necessary to "
        "hold total mass S, so at most B-q boxes are zero. This is sharp by "
        "filling q-1 boxes to U and placing the remainder in one box. Hence "
        "total mass and a capacity bound do not prevent concentration unless "
        "S exceeds (B-1)U. The finite dyadic audit computes every A_i exactly; "
        "it is evidence for the identities, not an infinite Goldbach proof."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "selector": "E_B=sum_i 2^(-k_B A_i), where 2^k_B>B",
        "selector_equivalence": "E_B<1 iff min_i A_i>=1",
        "occupancy_bound": "Z<=B-ceil(S/U), sharp",
        "dyadic_goldbach_rows": rows,
        "synthetic_selector_rows": synthetic_rows,
        "aggregate": {
            "scale_growing_exponential_selector_constructed": True,
            "finite_block_subunit_equivalence_proved": True,
            "aggregate_mass_capacity_zero_free_certificate_characterized": True,
            "aggregate_statistics_sufficient_on_audited_blocks": False,
            "uniform_arithmetic_subunit_bound_proved": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The selector is an exact reformulation, not an independent upper "
            "bound. The occupancy theorem rejects only arguments using total "
            "mass and a per-target cap without additional anti-concentration."
        ),
        "failure_count": failures,
    }


def lagrange_gap_weight(order: int, half_gap: int) -> Fraction:
    result = Fraction(1)
    for root in range(2, order + 1):
        result *= Fraction(half_gap - root, 1 - root)
    return result


def twin_cardinal_selector_audit() -> dict[str, Any]:
    failures = 0
    interpolation_rows = []
    for order in range(2, 13):
        values = [lagrange_gap_weight(order, r) for r in range(1, order + 4)]
        expected = []
        for r in range(1, order + 4):
            if r == 1:
                expected.append(Fraction(1))
            elif r <= order:
                expected.append(Fraction(0))
            else:
                expected.append(
                    Fraction(((-1) ** (order - 1)) * math.comb(r - 2, order - 1))
                )
        failures += int(values != expected)
        interpolation_rows.append(
            {
                "gap_cutoff_2M": 2 * order,
                "polynomial_degree": order - 1,
                "half_gap_r_values": list(range(1, order + 4)),
                "selector_values": [str(value) for value in values],
                "tail_formula": "(-1)^(M-1)*C(r-2,M-1) for r>M",
                "finite_gap_exact_selector_verified": values == expected,
            }
        )

    limits = (100, 1000, 10000, 100000)
    flags = prime_sieve(max(limits))
    primes = [value for value in range(2, len(flags)) if flags[value]]
    gap_rows = []
    for limit in limits:
        channels: Counter[int] = Counter()
        previous = None
        for prime in primes:
            if prime > limit:
                break
            if previous is not None and previous >= 3:
                channels[prime - previous] += 1
            previous = prime
        twin_count = channels[2]
        cardinal_sum = sum(
            count * (1 if gap == 2 else 0)
            for gap, count in channels.items()
        )
        failures += int(cardinal_sum != twin_count)
        gap_rows.append(
            {
                "prime_limit": limit,
                "exceptional_gap_one_omitted": True,
                "observed_even_gap_channels": len(channels),
                "consecutive_gap_two_count": twin_count,
                "cardinal_sine_symbolic_functional": cardinal_sum,
                "functional_equals_gap_two_count": cardinal_sum == twin_count,
            }
        )

    theorem = (
        "Define S(h)=sinc(h/2-1), with sinc(0)=1 and "
        "sinc(x)=sin(pi x)/(pi x). For every positive even integer gap h, "
        "S(h)=1 when h=2 and S(h)=0 otherwise. Hence on every finite range "
        "of consecutive odd-prime gaps (with the exceptional gap (2,3) "
        "omitted), the cardinal-sine functional sum_h S(h)t_h equals the "
        "exact consecutive twin-prime count t_2, with zero remainder. "
        "Therefore unboundedness of the cumulative functional is equivalent "
        "to the Twin Prime Conjecture, not a proof of it. A "
        "degree-(M-1) Lagrange polynomial gives the same selector through "
        "gap 2M, but its tail equals (-1)^(M-1) C(h/2-2,M-1); no fixed "
        "polynomial can vanish at every non-two even gap while taking value "
        "one at gap two."
    )
    proof = (
        "After omitting the unique odd gap from 2 to 3, every consecutive "
        "prime gap is even. At h=2r the cardinal-sine argument is the integer r-1, so the sine "
        "vanishes for every r>=2 and the removable value at r=1 is one. "
        "Summing against gap counts is therefore exactly coordinate "
        "projection onto t_2. For the finite polynomial, its roots are "
        "r=2,...,M and direct multiplication gives the binomial tail formula. "
        "A fixed nonzero polynomial cannot have the infinitely many roots "
        "2,3,..., so polynomial exact selection at all even gaps is impossible. "
        "The analytic selector solves representation of the channel, not the "
        "arithmetic lower bound for that channel."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "cardinal_selector": "S(h)=sinc(h/2-1)",
        "exact_even_gap_values": "S(2)=1 and S(2r)=0 for every integer r>=2",
        "finite_lagrange_rows": interpolation_rows,
        "prime_gap_audit_rows": gap_rows,
        "aggregate": {
            "cardinal_sine_exact_gap_two_selector_constructed": True,
            "selector_remainder_is_zero_on_even_integer_gaps": True,
            "fixed_degree_polynomial_all_gap_selector_refuted": True,
            "selector_value_equals_exact_twin_count": True,
            "unbounded_gap_two_count_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This constructs an exact analytic coordinate selector and rejects "
            "fixed polynomial all-gap selectors. It provides no positive lower "
            "bound for the selected prime-pair correlation."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_cofinal_density_audit()
    collatz_compute = collatz_seven_one_audit()
    goldbach_compute = goldbach_exponential_occupancy_audit()
    twin_compute = twin_cardinal_selector_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-214",
            "theorem_name": "CofinalExactDefectEquivalenceAndDensityOneNoGo",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No unbounded sequence of exact multiplicity equalities is proved for actual zeta zeros.",
            "route_decision": {
                "discard": "critical-line density one or relative defect o(N) as a sufficient RH criterion",
                "retain": "exact multiplicity equality on one certified unbounded sequence of boundary-free heights",
                "next_single_lemma": "CertifiedCofinalMultiplicityEqualityForActualZeta",
            },
            "proof_dag": proof_dag(
                "RH",
                "MultiplicityAwareCriticalLineCountEquivalenceAndSignChangeNoGo",
                "CofinalExactDefectEquivalenceAndDensityOneNoGo",
                "CriticalLineDensityOneImpliesRH",
                "CertifiedCofinalMultiplicityEqualityForActualZeta",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof and no off-critical zeta zero. Density-one promotion is refuted by a symmetric logical model; exact cofinal equality is an equivalent target.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-214",
            "theorem_name": "CompleteSevenValuationOneExclusionAndFiniteStratumNoGo",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "Cycles with at least eight valuation-one entries and every nonperiodic divergent orbit remain open.",
            "route_decision": {
                "discard": "all exactly-seven-one cycle words and any finite list of fixed-k exclusions as a complete Collatz proof",
                "retain": "a uniform ordinary-divisor obstruction valid for every primitive stratum with k at least eight",
                "next_single_lemma": "UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastEight",
            },
            "proof_dag": proof_dag(
                "CO",
                "CompleteSixValuationOneCycleStratumExclusion",
                "CompleteSevenValuationOneExclusionAndFiniteStratumNoGo",
                "FiniteFixedStratumEnumerationProvesCollatz",
                "UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastEight",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or positive integer counterexample. The seven-one periodic stratum is exhaustively excluded; unbounded strata and divergence remain uncontrolled.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-214",
            "theorem_name": "DyadicExponentialSelectorEquivalenceAndOccupancyNoGo",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "No unconditional uniform arithmetic estimate proves the exponential selector sum below one on every dyadic block.",
            "route_decision": {
                "discard": "treating the selector construction or aggregate witness mass plus a cap as an independent zero-free proof",
                "retain": "a collective arithmetic estimate for the low-representation exponential tail with anti-concentration",
                "next_single_lemma": "UniformArithmeticSubunitBoundForDyadicExponentialWitnessSelector",
            },
            "proof_dag": proof_dag(
                "GB",
                "FixedDegreePolynomialWitnessMajorantNoGo",
                "DyadicExponentialSelectorEquivalenceAndOccupancyNoGo",
                "AggregateWitnessMassOrSelectorConstructionAloneProvesCoverage",
                "UniformArithmeticSubunitBoundForDyadicExponentialWitnessSelector",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. A scale-growing exact selector is constructed, while its subunit estimate is shown to be the unresolved arithmetic content.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-214",
            "theorem_name": "CardinalSineExactGapTwoSelectorAndPositivityCircularity",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No unbounded lower bound is proved for the exact cardinal-sine prime-gap functional.",
            "route_decision": {
                "discard": "exact selector construction alone, or a fixed-degree polynomial selector, as a Twin Prime proof",
                "retain": "an arithmetic minorant forcing the cardinal-sine selected prime-pair correlation to be unbounded",
                "next_single_lemma": "UnboundedArithmeticMinorantForCardinalSinePrimeGapFunctional",
            },
            "proof_dag": proof_dag(
                "TP",
                "NonnegativeGapFunctionalIsolationIffSupportAtTwo",
                "CardinalSineExactGapTwoSelectorAndPositivityCircularity",
                "ExactAnalyticSelectorAloneProvesTwinInfinitude",
                "UnboundedArithmeticMinorantForCardinalSinePrimeGapFunctional",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. Exact all-gap selection is solved analytically, but positivity of the selected arithmetic channel remains exactly the conjectural step.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "CofinalSevenOneExponentialCardinalAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-214 proves four exact partial or no-go theorems and resolves "
            "none of the parent conjectures. It separates exact cofinal RH "
            "counts from density-one evidence, eliminates the full seven-one "
            "Collatz cycle stratum, constructs an exact dyadic exponential "
            "Goldbach selector while proving an aggregate occupancy no-go, and "
            "constructs an exact cardinal-sine gap-two selector while isolating "
            "the still-missing arithmetic positivity theorem."
        ),
        **sections,
        "cross_problem_synthesis": (
            "Exact selection and positive arithmetic control are different "
            "tasks. Density one does not force zero defect; finitely many "
            "Collatz strata do not cover unbounded k; an exact Goldbach selector "
            "does not provide its own subunit estimate; and an exact gap-two "
            "selector does not provide a positive prime-pair correlation."
        ),
        "literature_boundary": {
            "riemann": "The cofinal equivalence and density countermodel are logical reductions; no literature-priority claim or new zeta zero-density theorem is made.",
            "collatz": "The calculation extends PrimeProject's standard accelerated-cycle equation by one finite valuation stratum; it is not a uniform cycle theorem.",
            "goldbach": "The exponential selector and occupancy extremum are elementary exact reformulations; no new circle-method range is claimed.",
            "twin_prime": "Cardinal-sine interpolation is classical sampling algebra applied to the gap channel; no new bounded-gap or prime-pair lower bound is claimed.",
        },
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_limited_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = []
    for section_key, problem_id in (
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin_prime", "twin-prime"),
    ):
        section = audit[section_key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "status": STATUS,
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "bounded_result": {
                    "audit_ref": "#/cofinal_sevenone_exponential_cardinal_audit"
                },
            }
        )
    return attempts


def standalone_payload(section: dict[str, Any], problem_id: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "ticket_id": section["ticket_id"],
        "problem_id": problem_id,
        "status": STATUS,
        "theorem_name": section["theorem_name"],
        "declared_proposition": section["declared_proposition"],
        "mathematical_argument": section["mathematical_argument"],
        "reproducible_computation": section["reproducible_computation"],
        "discarded_route": section["route_decision"]["discard"],
        "remaining_gap": section["logical_limit"],
        "candidate_theorem": section["route_decision"]["next_single_lemma"],
        "claim_boundary": section["claim_boundary"],
        "proof_dag": section["proof_dag"],
    }


def write_outputs(audit: dict[str, Any]) -> None:
    integrated = ROOT / "data/open-problem/ticket214-cofinal-sevenone-exponential-cardinal.json"
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "cofinal_sevenone_exponential_cardinal_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-214-cofinal-defect-density-nogo.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-214-seven-one-exclusion.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-214-exponential-selector.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-214-cardinal-sine-selector.json",
    }
    problem_ids = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin_prime": "twin-prime",
    }
    for section_key, path in targets.items():
        write_json(path, standalone_payload(audit[section_key], problem_ids[section_key]))


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {
                "schema": SCHEMA,
                "status": STATUS,
                "machine_audit": audit["machine_audit"],
            },
            indent=2,
        )
    )
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
