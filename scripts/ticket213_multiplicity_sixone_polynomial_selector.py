from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket213-multiplicity-sixone-polynomial-selector.v1"
GENERATED_AT = "2026-08-12T23:58:00+09:00"
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
            {"id": f"{prefix}-T212", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T213", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N213",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN213",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T212", f"{prefix}-T213"],
            [f"{prefix}-T213", f"{prefix}-N213"],
            [f"{prefix}-T213", f"{prefix}-OPEN213"],
            [f"{prefix}-OPEN213", prefix],
        ],
    }


def zero_multiplicity_row(
    label: str,
    line_multiplicities: tuple[int, ...],
    off_line_pair_multiplicities: tuple[int, ...],
) -> dict[str, Any]:
    line_count = sum(line_multiplicities)
    off_line_pair_count = sum(off_line_pair_multiplicities)
    total_count = line_count + 2 * off_line_pair_count
    odd_line_count = sum(multiplicity % 2 for multiplicity in line_multiplicities)
    count_defect = total_count - line_count
    sign_defect = total_count - odd_line_count
    all_on_line = off_line_pair_count == 0
    all_on_line_and_simple = all_on_line and all(
        multiplicity == 1 for multiplicity in line_multiplicities
    )
    return {
        "configuration": label,
        "critical_line_multiplicities": list(line_multiplicities),
        "off_line_pair_multiplicities": list(off_line_pair_multiplicities),
        "total_zero_count_N": total_count,
        "critical_line_multiplicity_count_M": line_count,
        "distinct_odd_line_zero_count_O": odd_line_count,
        "multiplicity_aware_defect_N_minus_M": count_defect,
        "sign_change_defect_N_minus_O": sign_defect,
        "multiplicity_subtwo_certificate": count_defect < 2,
        "sign_change_subtwo_certificate": sign_defect < 2,
        "all_zeros_on_critical_line": all_on_line,
        "all_zeros_on_line_and_simple": all_on_line_and_simple,
    }


def riemann_multiplicity_audit() -> dict[str, Any]:
    rows = [
        zero_multiplicity_row("simple_line_zeros", (1, 1, 1, 1), ()),
        zero_multiplicity_row("double_line_zero_is_RH_compatible", (1, 2, 1), ()),
        zero_multiplicity_row("triple_line_zero_is_RH_compatible", (1, 3), ()),
        zero_multiplicity_row("one_simple_off_line_pair", (1, 1), (1,)),
        zero_multiplicity_row("one_double_off_line_pair", (), (2,)),
    ]
    failures = 0
    for row in rows:
        failures += int(
            row["multiplicity_subtwo_certificate"]
            != row["all_zeros_on_critical_line"]
        )
        failures += int(
            row["sign_change_subtwo_certificate"]
            != row["all_zeros_on_line_and_simple"]
        )
        failures += int(row["multiplicity_aware_defect_N_minus_M"] % 2 != 0)

    theorem = (
        "Let R be an upper-half critical-strip rectangle invariant under "
        "rho -> 1-conjugate(rho), with no boundary zeros. Let N count all "
        "zeros in R with multiplicity and M count the total multiplicity of "
        "zeros on Re(s)=1/2. Then N-M is a nonnegative even integer and "
        "N-M<2 if and only if every zero in R lies on the critical line. "
        "If O instead counts distinct odd-multiplicity line zeros, N-O<2 "
        "holds if and only if every zero lies on the line and is simple. "
        "Consequently an all-height N-O<2 target is strictly stronger than "
        "RH unless simplicity is supplied separately; N-M<2 is the exact "
        "multiplicity-aware finite-rectangle RH certificate."
    )
    proof = (
        "Symmetry partitions every off-line zero, including multiplicity, "
        "into a pair {rho,1-conjugate(rho)}. Hence N-M equals twice the total "
        "multiplicity on one side of the line. It is nonnegative and even, "
        "so it is below two exactly when it vanishes. For a line zero of "
        "multiplicity m, a Hardy-function sign count sees m mod 2 rather than "
        "m. Therefore N-O=(N-M)+sum_line(m-(m mod 2)); this vanishes exactly "
        "when there are no off-line zeros and every line multiplicity is one. "
        "A double line zero gives N-M=0 but N-O=2, proving strictness."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "multiplicity_identity": "N-M=2*(off-line multiplicity on one side)",
        "sign_identity": "N-O=(N-M)+sum_line(m-(m mod 2))",
        "configuration_rows": rows,
        "aggregate": {
            "multiplicity_aware_subtwo_equivalent_to_rectangle_RH": True,
            "sign_change_subtwo_equivalent_to_rectangle_RH_plus_simplicity": True,
            "ticket212_sign_change_target_was_stronger_than_RH": True,
            "all_height_multiplicity_count_bound_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "This corrects the target contract but computes no zeta zeros and "
            "does not prove an all-height equality N=M. Multiple line zeros "
            "are logical configurations; their existence for zeta is not asserted."
        ),
        "failure_count": failures,
    }


def weak_compositions(total: int, parts: int) -> Iterable[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


def total_valuation_upper_bound(length: int) -> int:
    exponent = 0
    while 2 ** (exponent + 1) * 3**length <= 10**length:
        exponent += 1
    return exponent


def cycle_numerator(word: tuple[int, ...]) -> int:
    length = len(word)
    prefix_sum = 0
    numerator = 0
    for index, valuation in enumerate(word):
        numerator += 3 ** (length - 1 - index) * 2**prefix_sum
        prefix_sum += valuation
    return numerator


def six_one_words(length: int, maximum_total: int) -> Iterator[tuple[int, ...]]:
    baseline_total = 2 * length - 6
    if baseline_total > maximum_total:
        return
    for other_ones in itertools.combinations(range(1, length - 1), 5):
        one_positions = {0, *other_ones}
        non_one_positions = [
            index for index in range(length) if index not in one_positions
        ]
        for extra_total in range(maximum_total - baseline_total + 1):
            for extras in weak_compositions(extra_total, len(non_one_positions)):
                word = [
                    1 if index in one_positions else 2 for index in range(length)
                ]
                for index, extra in zip(non_one_positions, extras, strict=True):
                    word[index] += extra
                yield tuple(word)


def collatz_six_one_audit() -> dict[str, Any]:
    rows = []
    total_words = 0
    positive_integer_candidates = 0
    divisibility_candidates = 0
    failures = 0
    for length in range(7, 23):
        maximum_total = total_valuation_upper_bound(length)
        baseline_total = 2 * length - 6
        digest = hashlib.sha256()
        local_words = 0
        local_divisible = 0
        local_positive = 0
        for word in six_one_words(length, maximum_total):
            local_words += 1
            numerator = cycle_numerator(word)
            divisor = 2 ** sum(word) - 3**length
            digest.update(
                (
                    f"{','.join(map(str, word))}:{numerator}:{divisor}\n"
                ).encode("ascii")
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
                "minimum_total_valuation_2h_minus_6": baseline_total,
                "maximum_total_valuation_from_minimum_bound": maximum_total,
                "enumerated_word_count": local_words,
                "ordinary_divisibility_candidate_count": local_divisible,
                "positive_odd_integer_fixed_point_count": local_positive,
                "valuation_word_and_divisor_sha256": digest.hexdigest(),
            }
        )

    multiplicity = 6
    exact_length_cap = math.floor(
        multiplicity * math.log(2) / math.log(Fraction(6, 5))
    )
    threshold = exact_length_cap + 1
    threshold_left = 2 ** (2 * threshold - multiplicity) * 3**threshold
    threshold_right = 10**threshold
    long_exclusion = threshold_left > threshold_right
    failures += int(total_words != 376_788)
    failures += int(divisibility_candidates != 0)
    failures += int(positive_integer_candidates != 0)
    failures += int(exact_length_cap != 22)
    failures += int(not long_exclusion)

    theorem = (
        "No nontrivial positive accelerated Collatz cycle has exactly six "
        "valuation entries equal to one and every other valuation at least "
        "two. Rotating a hypothetical cycle to its least odd element forces "
        "the first valuation to be one and the last to be at least two. The "
        "cycle product bound gives h<=floor(6 log(2)/log(6/5))=22. Exact "
        "ordinary-integer divisibility enumeration of all 376,788 admissible "
        "minimum-rotation candidate words of lengths 7 through 22 finds no "
        "positive odd integer fixed point. Combined with TICKET-210, every "
        "hypothetical nontrivial positive cycle therefore has at least seven "
        "valuation-one entries."
    )
    proof = (
        "For a least cycle element m>=3, valuation one is forced on the "
        "outgoing step and valuation at least two on the incoming step. If "
        "exactly k entries equal one, then A>=2h-k. Multiplying "
        "2^A=product_i(3+1/x_i) and using x_i>=3 gives "
        "2^A<=(10/3)^h, hence (6/5)^h<=2^k. At k=6 this leaves only "
        "7<=h<=22 and the same inequality gives a finite upper bound for A. "
        "The position choices and weak compositions enumerate every such "
        "least-rotation candidate. For each word the exact cycle equation is "
        "(2^A-3^h)x=C. None has positive divisor dividing C, as recorded by "
        "the deterministic transcript hashes. Length h>=23 is excluded by "
        "the product inequality."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "general_k_one_length_cap": (
            "h<=floor(k*log(2)/log(6/5)) for a cycle with exactly k ones"
        ),
        "k": multiplicity,
        "exact_length_cap_h": exact_length_cap,
        "exact_enumeration_rows": rows,
        "total_exact_words_enumerated": total_words,
        "ordinary_divisibility_candidate_count": divisibility_candidates,
        "positive_odd_integer_fixed_point_count": positive_integer_candidates,
        "length_at_least_twenty_three_exclusion": {
            "threshold_h": threshold,
            "left_2_pow_40_times_3_pow_23": str(threshold_left),
            "right_10_pow_23": str(threshold_right),
            "left_exceeds_right": long_exclusion,
        },
        "aggregate": {
            "exactly_six_valuation_one_cycle_stratum_excluded": True,
            "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle": 7,
            "seven_or_more_one_necklaces_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This is a finite exhaustive proof for one periodic stratum, not "
            "a proof of Collatz. Cycles with seven or more valuation-one "
            "entries and all nonperiodic divergent trajectories remain open."
        ),
        "failure_count": failures,
    }


def interpolation_polynomial_value(order: int, value: int) -> Fraction:
    result = Fraction(1)
    for root in range(1, order + 1):
        result *= Fraction(root - value, root)
    return result


def goldbach_polynomial_no_go_audit() -> dict[str, Any]:
    interpolation_rows = []
    failures = 0
    for order in range(1, 13):
        values = [interpolation_polynomial_value(order, value) for value in range(order + 2)]
        matches = values[0] == 1 and all(value == 0 for value in values[1 : order + 1])
        failures += int(not matches)
        interpolation_rows.append(
            {
                "interpolation_order_M": order,
                "degree": order,
                "values_at_A_0_through_M_plus_1": [str(value) for value in values],
                "matches_zero_indicator_on_0_through_M": matches,
                "first_out_of_range_value_at_M_plus_1": str(values[-1]),
            }
        )

    sample_polynomials = [
        {
            "label": "constant_one",
            "degree": 0,
            "P_0": "1",
            "tail_behavior": "equals 1, violating strict subunit value",
        },
        {
            "label": "positive_leading_coefficient",
            "degree": 2,
            "P_0": "1",
            "tail_behavior": "tends to positive infinity",
        },
        {
            "label": "negative_leading_coefficient",
            "degree": 3,
            "P_0": "1",
            "tail_behavior": "tends to negative infinity",
        },
    ]

    theorem = (
        "Let A(N) be the number of unordered Goldbach witnesses of an even "
        "target N. There is no fixed real polynomial P such that P(0)>=1 "
        "and 0<=P(A(N))<1 for every represented even N. TICKET-212 proves "
        "that the attained positive values A(N) are unbounded. A nonconstant "
        "polynomial tends to positive or negative infinity along that "
        "unbounded sequence, violating respectively P<1 or P>=0; a constant "
        "polynomial cannot satisfy both P(0)>=1 and P(A(N))<1. Moreover, any "
        "polynomial agreeing with the exact zero indicator on A=0,1,...,M "
        "has degree at least M, and the degree-M product "
        "prod_{j=1}^M(1-A/j) attains this bound. Thus polynomial complexity "
        "must grow with the witness range."
    )
    proof = (
        "The unbounded attained sequence A(N_k) tends to infinity after "
        "passing to a subsequence. The sign of a nonconstant polynomial on "
        "the positive tail is the sign of its leading coefficient, and its "
        "absolute value diverges. This contradicts membership in [0,1). A "
        "constant c must have c>=1 at zero and c<1 on represented targets, "
        "also impossible. For finite interpolation, a polynomial with value "
        "zero at each of 1,...,M has M distinct roots; because its value at "
        "zero is one it is nonzero, so its degree is at least M. The displayed "
        "product has exactly those roots and value one at zero."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "pointwise_majorant_contract": (
            "P(0)>=1 and 0<=P(A(N))<1 for every represented target N"
        ),
        "finite_interpolation_rows": interpolation_rows,
        "polynomial_tail_cases": sample_polynomials,
        "aggregate": {
            "fixed_degree_polynomial_majorant_route_refuted": True,
            "degree_at_least_witness_range_for_exact_interpolation_proved": True,
            "scale_growing_or_nonpolynomial_resummation_required": True,
            "uniform_subunit_exception_bound_proved": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem rejects fixed polynomials of the witness count only. "
            "It does not reject scale-dependent, rational, exponential, or "
            "analytic resummations, and proves no Goldbach tail positivity."
        ),
        "failure_count": failures,
    }


def weighted_selector_row(label: str, weights: tuple[Fraction, ...]) -> dict[str, Any]:
    gaps = tuple(range(2, 2 * len(weights) + 1, 2))
    basis_values = []
    for index, gap in enumerate(gaps):
        vector = [Fraction(0)] * len(gaps)
        vector[index] = Fraction(1)
        functional = sum(weight * value for weight, value in zip(weights, vector, strict=True))
        basis_values.append(
            {
                "positive_gap_channel": gap,
                "gap_two_positive": gap == 2,
                "functional_value": str(functional),
            }
        )
    exact_selector = weights[0] > 0 and all(weight == 0 for weight in weights[1:])
    observed_equivalence = all(
        (Fraction(row["functional_value"]) > 0) == row["gap_two_positive"]
        for row in basis_values
    )
    return {
        "label": label,
        "gaps": list(gaps),
        "nonnegative_weights": [str(weight) for weight in weights],
        "basis_extreme_ray_rows": basis_values,
        "support_only_at_gap_two_with_positive_weight": exact_selector,
        "basis_equivalence_observed": observed_equivalence,
    }


def twin_nonnegative_selector_audit() -> dict[str, Any]:
    rows = [
        weighted_selector_row(
            "pure_gap_two_selector",
            (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        ),
        weighted_selector_row(
            "uniform_bounded_gap_aggregate",
            (Fraction(1), Fraction(1), Fraction(1), Fraction(1)),
        ),
        weighted_selector_row(
            "small_gap_suppressed_but_contaminated",
            (Fraction(1, 100), Fraction(0), Fraction(7, 3), Fraction(0)),
        ),
        weighted_selector_row(
            "gap_two_missing",
            (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
        ),
    ]
    failures = sum(
        int(row["support_only_at_gap_two_with_positive_weight"] != row["basis_equivalence_observed"])
        for row in rows
    )
    theorem = (
        "Let H be a finite gap set containing 2, let w_h>=0, and define "
        "L_w(t)=sum_{h in H}w_h t_h on the nonnegative gap-channel cone. "
        "Then L_w(t)>0 if and only if t_2>0 for every t>=0 exactly when "
        "w_2>0 and w_h=0 for all h!=2. Thus no nonnegative weighted "
        "bounded-gap statistic contaminated by another gap can isolate twin "
        "primes, regardless of how small the contaminating weight is."
    )
    proof = (
        "If only w_2 is positive, L_w(t)=w_2 t_2 and the equivalence is "
        "immediate. Conversely, testing the extreme ray e_2 forces w_2>0. "
        "Testing e_g for each g!=2 forces w_g=0, because t_2=0 there while "
        "L_w(e_g)=w_g. These extreme rays exhaust the required coefficient "
        "conditions on the nonnegative orthant."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "selector_equivalence": (
            "forall t>=0, L_w(t)>0 iff t_2>0  <=>  w_2>0 and support(w)={2}"
        ),
        "weight_audit_rows": rows,
        "aggregate": {
            "nonnegative_selector_characterization_proved": True,
            "all_contaminated_nonnegative_aggregates_refuted": True,
            "signed_or_arithmetic_remainder_selector_constructed": False,
            "gap_two_positive_on_infinitely_many_blocks_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This is an exact cone-duality theorem for abstract nonnegative "
            "channels. It does not rule out signed arithmetic functionals with "
            "controlled remainders and gives no lower bound for actual gap two."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_multiplicity_audit()
    collatz_compute = collatz_six_one_audit()
    goldbach_compute = goldbach_polynomial_no_go_audit()
    twin_compute = twin_nonnegative_selector_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-213",
            "theorem_name": "MultiplicityAwareCriticalLineCountEquivalenceAndSignChangeNoGo",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No all-height equality between total zero multiplicity and critical-line multiplicity is proved for zeta.",
            "route_decision": {
                "discard": "using odd-multiplicity sign changes as an RH-equivalent count without a separate simplicity theorem",
                "retain": "total critical-line multiplicity M and the exact symmetry-quantized defect N-M",
                "next_single_lemma": "UniformMultiplicityAwareCriticalLineDefectStrictlyBelowTwo",
            },
            "proof_dag": proof_dag(
                "RH",
                "EvenCriticalLineDefectSubTwoSaturationCertificate",
                "MultiplicityAwareCriticalLineCountEquivalenceAndSignChangeNoGo",
                "SignChangeSubTwoIsExactlyRHEquivalent",
                "UniformMultiplicityAwareCriticalLineDefectStrictlyBelowTwo",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof and no off-line zeta zero. The finite-rectangle target is corrected so multiple critical-line zeros no longer create a false RH defect.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-213",
            "theorem_name": "CompleteSixValuationOneCycleStratumExclusion",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "Cycles with at least seven valuation-one entries and nonperiodic divergence remain open.",
            "route_decision": {
                "discard": "every accelerated positive cycle word with exactly six valuation-one entries",
                "retain": "ordinary divisor tests on the unbounded primitive strata with seven or more valuation-one entries",
                "next_single_lemma": "UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastSeven",
            },
            "proof_dag": proof_dag(
                "CO",
                "TwoAdicGhostUniversalityAndOddDivisibilityCorrection",
                "CompleteSixValuationOneCycleStratumExclusion",
                "SixValuationOnePositiveCycleStratum",
                "UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastSeven",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or positive integer counterexample. One previously open periodic stratum is exhaustively eliminated with exact integer arithmetic.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-213",
            "theorem_name": "FixedDegreePolynomialWitnessMajorantNoGo",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "No scale-growing or nonpolynomial resummation has a proved uniformly subunit exceptional tail.",
            "route_decision": {
                "discard": "every fixed-degree polynomial in the Goldbach witness count as a pointwise subunit exception majorant",
                "retain": "scale-growing or nonpolynomial full-witness resummation with a uniform dyadic tail bound",
                "next_single_lemma": "ScaleGrowingWitnessResummationWithUniformDyadicTailBelowOne",
            },
            "proof_dag": proof_dag(
                "GB",
                "FullWitnessProductIdentityAndFixedBonferroniNoGo",
                "FixedDegreePolynomialWitnessMajorantNoGo",
                "FixedPolynomialCanMajorizeAllGoldbachExceptionsBelowOne",
                "ScaleGrowingWitnessResummationWithUniformDyadicTailBelowOne",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The fixed-Bonferroni obstruction is extended to every fixed polynomial of representation multiplicity.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-213",
            "theorem_name": "NonnegativeGapFunctionalIsolationIffSupportAtTwo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No signed arithmetic selector with a uniformly controlled remainder, or direct infinite gap-two lower bound, is proved.",
            "route_decision": {
                "discard": "every nonnegative bounded-gap weighted aggregate with positive support away from gap two",
                "retain": "a gap-two-selective signed arithmetic functional with a uniform remainder estimate",
                "next_single_lemma": "GapTwoSelectiveSignedFunctionalWithUniformArithmeticRemainder",
            },
            "proof_dag": proof_dag(
                "TP",
                "DyadicGapTwoEquivalenceAndFiniteGapAggregateNoGo",
                "NonnegativeGapFunctionalIsolationIffSupportAtTwo",
                "ContaminatedNonnegativeWeightsCanSelectGapTwo",
                "GapTwoSelectiveSignedFunctionalWithUniformArithmeticRemainder",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. The aggregate no-go now covers every nonnegative weighting and identifies the only exact nonnegative selector.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "MultiplicitySixOnePolynomialSelectorAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-213 proves four exact partial or no-go theorems and resolves "
            "none of the parent conjectures. It corrects the RH counting target, "
            "eliminates the full six-one Collatz cycle stratum, rejects all fixed "
            "polynomial Goldbach witness majorants, and characterizes every exact "
            "nonnegative gap-two selector."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common requirement is target-selective information. Multiplicity "
            "must be counted rather than inferred from signs; Collatz integrality "
            "needs its ordinary odd divisor; Goldbach needs complexity growing with "
            "the witness range; and Twin Prime needs a functional that annihilates "
            "every non-two gap or controls signed cancellation arithmetically."
        ),
        "literature_boundary": {
            "riemann": "Published finite-height verification does not provide the all-height multiplicity equality required here; no novelty claim is made for symmetry counting.",
            "collatz": "The finite stratum proof uses the standard accelerated-cycle equation and PrimeProject's earlier product bound and primitive-word reductions.",
            "goldbach": "Unbounded representation multiplicity imports the prime number theorem through TICKET-212; no new analytic Goldbach range is claimed.",
            "twin_prime": "Maynard-style bounded-gap theorems control an aggregate existence statement, not the exact gap-two channel characterized here.",
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
                    "audit_ref": "#/multiplicity_sixone_polynomial_selector_audit"
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
    integrated = ROOT / "data/open-problem/ticket213-multiplicity-sixone-polynomial-selector.json"
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "multiplicity_sixone_polynomial_selector_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-213-multiplicity-aware-count.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-213-six-one-exclusion.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-213-polynomial-majorant-no-go.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-213-nonnegative-selector.json",
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
