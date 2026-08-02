from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket180_finite_information_localization import ordered_affine_numerator
from ticket187_positive_ray_threeone_signature_interval import (
    fraction_payload,
    quantized_twin_interval,
)


GENERATED_AT = "2026-08-02T23:58:00+09:00"
SCHEMA = "primeproject.ticket188-nested-fourone-primepower-dyadic.v1"
STATUS = (
    "one_additional_infinite_cycle_stratum_closed_"
    "three_exact_promotion_boundaries_all_open"
)


def proof_dag(
    problem_code: str,
    previous_name: str,
    closed_name: str,
    rejected_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T187-INPUT",
                "label": previous_name,
                "status": "proved_exact_input_or_open_target",
            },
            {
                "id": f"{problem_code}-T188-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T188-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T188-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T187-INPUT", f"{problem_code}-T188-CLOSED"],
            [f"{problem_code}-T188-CLOSED", f"{problem_code}-T188-OPEN"],
            [f"{problem_code}-T188-REJECTED", f"{problem_code}-T188-OPEN"],
        ],
    }


def nested_defect_row(dimension: int) -> dict[str, object]:
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    diagonal = [Fraction(1, index + 1) for index in range(dimension)]
    if dimension >= 3:
        diagonal[2] = Fraction(-1, 7)
    minimum = min(diagonal)
    defect = max(Fraction(0), -minimum)
    return {
        "dimension_N": dimension,
        "minimum_eigenvalue": fraction_payload(minimum),
        "negative_defect": fraction_payload(defect),
        "negative_coordinate_present": dimension >= 3,
    }


def moving_direction_row(dimension: int) -> dict[str, object]:
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    defect = Fraction(1, dimension)
    return {
        "dimension_N": dimension,
        "matrix": "diag(1,...,1,-1/N)",
        "minimum_eigenvalue": fraction_payload(-defect),
        "negative_defect": fraction_payload(defect),
        "indefinite": True,
        "negative_coordinate": dimension,
        "next_overlap_difference_at_old_last_coordinate": fraction_payload(
            Fraction(dimension + 1, dimension)
        ),
        "exactly_nested": False,
    }


def riemann_common_form_audit() -> dict[str, object]:
    dimensions = [2, 3, 4, 8, 16, 32]
    nested_rows = [nested_defect_row(n) for n in dimensions]
    moving_rows = [moving_direction_row(n) for n in dimensions]
    nested_defects = [
        Fraction(row["negative_defect"]["exact"]) for row in nested_rows
    ]
    moving_defects = [
        Fraction(row["negative_defect"]["exact"]) for row in moving_rows
    ]
    failures = 0
    failures += int(
        any(left > right for left, right in zip(nested_defects, nested_defects[1:]))
    )
    failures += int(
        any(left <= right for left, right in zip(moving_defects, moving_defects[1:]))
    )
    failures += sum(not row["indefinite"] for row in moving_rows)
    failures += sum(row["exactly_nested"] for row in moving_rows)
    return {
        "theorem": (
            "Let A_N be exact nested principal restrictions of one Hermitian "
            "quadratic form and put delta_N=max(0,-lambda_min(A_N)). Then "
            "delta_N is nondecreasing. Hence delta_N tending to zero on a "
            "cofinal subsequence forces delta_N=0 for every N and proves "
            "nonnegativity on the algebraic union. More generally, if A_N "
            "approximates one fixed form Q on every fixed finite-support "
            "vector with certified error epsilon_N tending to zero and "
            "lambda_min(A_N)>=-eta_N with eta_N tending to zero, then Q is "
            "nonnegative. Without exact nesting or common-form convergence, "
            "vanishing defect is insufficient: diag(1,...,1,-1/N) is "
            "indefinite for every N although its defect is 1/N."
        ),
        "proof": (
            "The Rayleigh quotient of A_{N+1}, restricted to the first N "
            "coordinates, contains the Rayleigh quotients of A_N. Therefore "
            "lambda_min(A_{N+1})<=lambda_min(A_N), so the negative defect is "
            "nondecreasing. A nonnegative nondecreasing sequence with a "
            "cofinal subsequence converging to zero is identically zero. For "
            "the approximate statement, fix a finite-support vector f and "
            "pass to the limit in Q(f)>=-(epsilon_N+eta_N)||f||^2. The moving "
            "diagonal counterfamily has exact minimum -1/N, but its negative "
            "coordinate changes at every dimension and adjacent restrictions "
            "disagree at the old last coordinate."
        ),
        "exact_nested_interlacing_rows": nested_rows,
        "moving_negative_direction_counterfamily": moving_rows,
        "promotion_contract": {
            "fixed_form_Q_required": True,
            "cofinal_finite_support_coverage_required": True,
            "certified_form_error_epsilon_tends_to_zero_required": True,
            "certified_negative_bound_eta_tends_to_zero_required": True,
            "conclusion": "Q(f)>=0 for every finite-support f",
        },
        "aggregate": {
            "nested_dimension_count": len(nested_rows),
            "nested_defect_is_nondecreasing": True,
            "moving_counterfamily_dimension_count": len(moving_rows),
            "moving_defect_strictly_decreases": True,
            "moving_family_is_indefinite_at_every_dimension": True,
            "common_form_weil_contract_verified": False,
        },
        "no_go_scope": (
            "This is a functional-analytic promotion criterion and an exact "
            "counterexample to defect-only reasoning. PrimeProject has not "
            "proved that the cutoff-dependent Guinand-Weil matrices are exact "
            "nested restrictions or certified approximations to one common "
            "pole-neutral form, and has not proved RH."
        ),
        "failure_count": failures,
    }


def canonical_four_one_word(
    a: int, b: int, c: int, d: int
) -> tuple[int, ...]:
    if min(a, b, c, d) < 1:
        raise ValueError("all four cyclic gaps must be positive")
    return (
        (1,)
        + (2,) * (a - 1)
        + (1,)
        + (2,) * (b - 1)
        + (1,)
        + (2,) * (c - 1)
        + (1,)
        + (2,) * (d - 1)
    )


def four_one_closed_form(a: int, b: int, c: int, d: int) -> int:
    h = a + b + c + d
    return (
        2 ** (2 * h - 4)
        - 3 ** (h - 1)
        + 4**a * 3 ** (h - a - 1)
        + 2 * 4 ** (a + b - 1) * 3 ** (c + d - 1)
        + 4 ** (a + b + c - 1) * 3 ** (d - 1)
    )


def four_one_cycle_row(a: int, b: int, c: int, d: int) -> dict[str, object]:
    word = canonical_four_one_word(a, b, c, d)
    h = len(word)
    numerator = ordered_affine_numerator(word)
    denominator = 2 ** (2 * h - 4) - 3**h
    shifted = word[1:] + word[:1]
    return {
        "horizon_h": h,
        "cyclic_gaps": [a, b, c, d],
        "largest_gap_is_d": d == max(a, b, c, d),
        "affine_numerator_B": str(numerator),
        "cycle_denominator_D": str(denominator),
        "B_mod_D": str(numerator % denominator),
        "checks": {
            "closed_form_matches_recurrence": numerator
            == four_one_closed_form(a, b, c, d),
            "contracting": denominator > 0,
            "B_exceeds_D": numerator > denominator,
            "B_is_below_3D": numerator < 3 * denominator,
            "B_and_D_are_odd": numerator % 2 == denominator % 2 == 1,
            "rotation_identity": (
                2 ** word[0] * ordered_affine_numerator(shifted)
                == 3 * numerator + denominator
            ),
            "affine_divisibility_fails": numerator % denominator != 0,
        },
    }


def finite_four_one_horizon_row(horizon: int) -> dict[str, object]:
    if not 10 <= horizon <= 15:
        raise ValueError("the exact finite-exception range is h=10..15")
    denominator = 2 ** (2 * horizon - 4) - 3**horizon
    transcript: list[str] = []
    hits: list[dict[str, object]] = []
    formula_failures = 0
    rotation_failures = 0
    for positions in itertools.combinations(range(horizon), 4):
        position_set = set(positions)
        word = tuple(1 if index in position_set else 2 for index in range(horizon))
        numerator = ordered_affine_numerator(word)
        remainder = numerator % denominator
        transcript.append(f"{positions}:{remainder}")
        p0, p1, p2, p3 = positions
        gaps = (p1 - p0, p2 - p1, p3 - p2, horizon - p3 + p0)
        rotated = word[p0:] + word[:p0]
        if ordered_affine_numerator(rotated) != four_one_closed_form(*gaps):
            formula_failures += 1
        shifted = word[1:] + word[:1]
        if (
            2 ** word[0] * ordered_affine_numerator(shifted)
            != 3 * numerator + denominator
        ):
            rotation_failures += 1
        if remainder == 0:
            hits.append(
                {"positions": list(positions), "integer_quotient": numerator // denominator}
            )
    return {
        "horizon_h": horizon,
        "contracting": denominator > 0,
        "word_count": math.comb(horizon, 4),
        "divisibility_hit_count": len(hits),
        "divisibility_hits": hits,
        "closed_form_failure_count": formula_failures,
        "rotation_identity_failure_count": rotation_failures,
        "remainder_transcript_sha256": hashlib.sha256(
            "\n".join(transcript).encode("ascii")
        ).hexdigest(),
    }


def balanced_four_gaps(horizon: int) -> tuple[int, int, int, int]:
    gaps = [horizon // 4] * 4
    for offset in range(horizon % 4):
        gaps[3 - offset] += 1
    return tuple(gaps)  # type: ignore[return-value]


def four_one_global_bound(horizon: int) -> Fraction:
    u = Fraction(3, 4)
    return (
        Fraction(16, 3) * u ** math.ceil((horizon + 2) / 2)
        + Fraction(8, 3) * u ** (math.ceil(horizon / 4) + 1)
        + Fraction(4, 3) * u ** math.ceil(horizon / 4)
        + Fraction(128, 3) * u**horizon
    )


def collatz_four_one_audit() -> dict[str, object]:
    finite_rows = [finite_four_one_horizon_row(h) for h in range(10, 16)]
    analytic_rows = [
        four_one_cycle_row(*balanced_four_gaps(h))
        for h in [16, 20, 32, 64, 128]
    ]
    threshold_bound = four_one_global_bound(16)
    failures = sum(
        row["divisibility_hit_count"]
        + row["closed_form_failure_count"]
        + row["rotation_identity_failure_count"]
        + int(not row["contracting"])
        for row in finite_rows
    )
    failures += sum(
        not check for row in analytic_rows for check in row["checks"].values()
    )
    failures += int(not threshold_bound < 2)
    return {
        "theorem": (
            "No positive accelerated Collatz cycle has a valuation period with "
            "exactly four entries equal to one and every other entry equal to "
            "two, including primitive and imprimitive periods."
        ),
        "proof": (
            "Rotate the four ones into cyclic gaps a,b,c,d>=1 with d largest. "
            "Then h=a+b+c+d, d>=ceil(h/4), c+d>=ceil(h/4)+1, and "
            "h-a>=ceil((h+2)/2). The exact cycle numerator is "
            "B=4^h/16-3^(h-1)+4^a3^(h-a-1)+2*4^(a+b-1)"
            "3^(c+d-1)+4^(a+b+c-1)3^(d-1), while D=4^h/16-3^h. "
            "Thus B>D and both are odd. With u=3/4, B<3D follows if "
            "(16/3)u^(h-a)+(8/3)u^(c+d)+(4/3)u^d+(128/3)u^h<2. "
            "The displayed gap bounds give a decreasing all-word majorant "
            "equal to 63175275/33554432<2 at h=16. Hence B/D is strictly "
            "between one and three for every h>=16; if integral it would have "
            "to be odd, which is impossible. Contraction starts at h=10, and "
            "exact enumeration of all sum_{h=10}^{15} C(h,4)=4116 remaining "
            "words finds no divisibility hit. Cyclic rotation preserves "
            "divisibility through 2^v B_shift=3B+D."
        ),
        "finite_exception_horizon_rows": finite_rows,
        "analytic_replay_rows": analytic_rows,
        "analytic_bound": {
            "bound_at_h_16": fraction_payload(threshold_bound),
            "required_upper_threshold": fraction_payload(Fraction(2)),
            "analytic_range_starts_at_h": 16,
            "bound_is_nonincreasing_after_threshold": True,
        },
        "aggregate": {
            "infinite_family_proved": True,
            "includes_imprimitive_words": True,
            "contracting_range_starts_at_h": 10,
            "analytic_range_starts_at_h": 16,
            "finite_exception_word_count": sum(
                row["word_count"] for row in finite_rows
            ),
            "divisibility_hits": sum(
                row["divisibility_hit_count"] for row in finite_rows
            ),
            "largest_replayed_horizon": analytic_rows[-1]["horizon_h"],
        },
        "no_go_scope": (
            "This closes one additional infinite periodic stratum. Words with "
            "five or more valuation-one entries, any valuation at least three, "
            "and divergent aperiodic natural-number orbits remain untreated."
        ),
        "failure_count": failures,
    }


def prime_power_metadata(limit: int) -> list[tuple[int, int] | None]:
    is_prime = prime_sieve(limit)
    metadata: list[tuple[int, int] | None] = [None] * (limit + 1)
    for prime in range(2, limit + 1):
        if not is_prime[prime]:
            continue
        value = prime
        exponent = 1
        while value <= limit:
            metadata[value] = (prime, exponent)
            if value > limit // prime:
                break
            value *= prime
            exponent += 1
    return metadata


def integer_nth_root(value: int, exponent: int) -> int:
    if value < 0 or exponent < 1:
        raise ValueError("nonnegative value and positive exponent required")
    low, high = 0, 1
    while high**exponent <= value:
        high *= 2
    while low + 1 < high:
        middle = (low + high) // 2
        if middle**exponent <= value:
            low = middle
        else:
            high = middle
    return low


def goldbach_prime_power_row(
    target: int, metadata: list[tuple[int, int] | None]
) -> dict[str, object]:
    if target < 6 or target % 2:
        raise ValueError("an even target at least six is required")
    total_mass = 0.0
    prime_mass = 0.0
    contamination_mass = 0.0
    total_support = 0
    prime_support = 0
    contamination_support = 0
    contamination_examples: list[list[int]] = []
    for left in range(2, target - 1):
        right = target - left
        left_meta = metadata[left]
        right_meta = metadata[right]
        if left_meta is None or right_meta is None:
            continue
        weight = math.log(left_meta[0]) * math.log(right_meta[0])
        total_mass += weight
        total_support += 1
        if left_meta[1] == right_meta[1] == 1:
            prime_mass += weight
            prime_support += 1
        else:
            contamination_mass += weight
            contamination_support += 1
            if len(contamination_examples) < 4:
                contamination_examples.append(
                    [left, right, left_meta[1], right_meta[1]]
                )
    proper_count = sum(
        meta is not None and meta[1] >= 2 for meta in metadata[: target + 1]
    )
    maximum_exponent = target.bit_length() - 1
    coarse_count_bound = sum(
        integer_nth_root(target, exponent)
        for exponent in range(2, maximum_exponent + 1)
    )
    contamination_bound = 2 * proper_count * math.log(target) ** 2
    return {
        "even_target_N": target,
        "ordered_von_mangoldt_support_count": total_support,
        "ordered_prime_pair_support_count": prime_support,
        "ordered_prime_power_contamination_count": contamination_support,
        "weighted_total_convolution": total_mass,
        "weighted_prime_pair_mass": prime_mass,
        "weighted_prime_power_contamination": contamination_mass,
        "decomposition_rounding_residual": abs(
            total_mass - prime_mass - contamination_mass
        ),
        "proper_prime_power_count_A_N": proper_count,
        "coarse_prime_power_count_upper_bound": coarse_count_bound,
        "contamination_mass_upper_bound": contamination_bound,
        "contamination_examples_left_right_exponents": contamination_examples,
        "checks": {
            "support_decomposition_exact": total_support
            == prime_support + contamination_support,
            "weighted_decomposition_replays": abs(
                total_mass - prime_mass - contamination_mass
            )
            < 1e-9,
            "contamination_count_below_two_A": contamination_support
            <= 2 * proper_count,
            "contamination_mass_below_explicit_bound": contamination_mass
            <= contamination_bound,
            "proper_power_count_below_coarse_bound": proper_count
            <= coarse_count_bound,
        },
    }


def goldbach_prime_power_audit() -> dict[str, object]:
    targets = [18, 100, 1_000, 10_000, 100_000]
    metadata = prime_power_metadata(max(targets))
    rows = [goldbach_prime_power_row(target, metadata) for target in targets]
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(rows[0]["ordered_prime_power_contamination_count"] == 0)
    return {
        "theorem": (
            "For every even N, the binary von Mangoldt convolution R_Lambda(N) "
            "decomposes exactly as P_Lambda(N)+E_pp(N), where P_Lambda is the "
            "ordered prime-prime mass and E_pp is the nonnegative mass from "
            "terms with at least one proper prime power. If A(N) counts proper "
            "prime powers at most N, then E_pp(N)<=2 A(N)(log N)^2. Therefore "
            "a certified lower bound L(N)>2 A(N)(log N)^2 implies P_Lambda(N)>0 "
            "and hence a Goldbach representation. Positivity of R_Lambda alone, "
            "or identifying R_Lambda with P_Lambda, does not perform this "
            "subtraction; N=18 already has the contaminating term 9+9."
        ),
        "proof": (
            "Partition every nonzero summand Lambda(m)Lambda(N-m) according "
            "to whether both exponents are one. This gives the exact "
            "decomposition and E_pp>=0. A contaminated ordered pair has a "
            "proper prime power in at least one endpoint. There are at most "
            "A(N) choices for each endpoint position and every Lambda weight "
            "is at most log N, proving the upper bound. Subtracting this bound "
            "from any rigorous lower bound for R_Lambda leaves positive "
            "prime-prime mass."
        ),
        "finite_decomposition_rows": rows,
        "aggregate": {
            "target_count": len(rows),
            "largest_target": rows[-1]["even_target_N"],
            "n18_contamination_present": (
                rows[0]["ordered_prime_power_contamination_count"] > 0
            ),
            "all_finite_prime_pair_masses_positive": all(
                row["weighted_prime_pair_mass"] > 0 for row in rows
            ),
            "every_target_weighted_lower_bound_proved": False,
        },
        "no_go_scope": (
            "The decomposition does not provide the required lower bound for "
            "R_Lambda on every even target. The finite rows use already known "
            "representations and are diagnostics only. Exceptional-set and "
            "major-arc formulae do not by themselves remove every target."
        ),
        "failure_count": failures,
    }


def dyadic_twin_row(
    exponent: int, is_prime: list[bool]
) -> dict[str, object]:
    lower_x = 2**exponent
    upper_x = 2 ** (exponent + 1)
    count = sum(
        is_prime[prime] and is_prime[prime + 2]
        for prime in range(lower_x, upper_x)
    )
    projector = 4 * count
    interval = quantized_twin_interval(
        Fraction(4 * projector - 7, 4),
        Fraction(4 * projector + 7, 4),
    )
    return {
        "dyadic_exponent_j": exponent,
        "block": [lower_x, upper_x],
        "direct_twin_count_C_j": count,
        "projector_Delta_j": projector,
        "sound_subfour_interval": interval,
        "checks": {
            "interval_width_is_seven_halves": (
                Fraction(interval["upper"]["exact"])
                - Fraction(interval["lower"]["exact"])
                == Fraction(7, 2)
            ),
            "interval_certifies_exact_count": (
                interval["exact_count_certified"]
                and interval["minimum_compatible_twin_count"] == count
            ),
            "positive_lower_endpoint_iff_block_occupied": (
                (Fraction(interval["lower"]["exact"]) > 0) == (count > 0)
            ),
        },
    }


def twin_dyadic_audit() -> dict[str, object]:
    exponents = list(range(4, 20))
    is_prime = prime_sieve(2 ** (exponents[-1] + 1) + 2)
    rows = [dyadic_twin_row(exponent, is_prime) for exponent in exponents]
    sharp_ambiguous = quantized_twin_interval(Fraction(0), Fraction(4))
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(not sharp_ambiguous["ambiguous_between_zero_and_positive"])
    return {
        "theorem": (
            "Let C_j count twin-prime starts in the dyadic block "
            "[2^j,2^(j+1)) and Delta_j=4C_j. Every sound interval [L_j,U_j] "
            "of width strictly below four that contains Delta_j contains "
            "exactly one point of 4 times the nonnegative integers. It therefore "
            "recovers C_j exactly, and L_j>0 if and only if C_j>0. Width four "
            "is sharp because [0,4] is compatible with both zero and one. "
            "Consequently the Twin Prime conjecture is equivalent to positive "
            "lower endpoints on infinitely many dyadic blocks, but demanding "
            "sub-four intervals on every block is an exact-count oracle and is "
            "strictly more information than a one-sided infinitude proof needs."
        ),
        "proof": (
            "Distinct points of 4 times the nonnegative integers are separated "
            "by four, so an interval of smaller width contains at most one. "
            "Soundness supplies Delta_j, hence the count is exact. If C_j=0, "
            "soundness gives L_j<=0. If C_j>=1, then U_j>=4 and U_j-L_j<4, "
            "so L_j>0. Every twin belongs to one dyadic block and every bounded "
            "collection of blocks is finite, proving the infinitude equivalence."
        ),
        "finite_dyadic_rows": rows,
        "sharp_width_four_counterinterval": sharp_ambiguous,
        "aggregate": {
            "dyadic_block_count": len(rows),
            "largest_upper_endpoint": rows[-1]["block"][1],
            "occupied_block_count": sum(
                row["direct_twin_count_C_j"] > 0 for row in rows
            ),
            "subfour_intervals_recover_exact_count": True,
            "width_four_is_ambiguous": True,
            "independent_analytic_interval_construction": False,
            "conjecture_resolution_count": 0,
        },
        "no_go_scope": (
            "The displayed intervals are centered on directly counted twins "
            "and are only exact replay witnesses. No independent Type I/II "
            "estimate constructs a positive lower endpoint on infinitely many "
            "unbounded blocks."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_common_form_audit()
    collatz = collatz_four_one_audit()
    goldbach = goldbach_prime_power_audit()
    twin = twin_dyadic_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-188",
            "theorem_name": "CommonFormDefectPromotionAndMovingDirectionNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No common-form convergence estimate or cofinal zero-defect interval LDL certificate is proved for the actual Guinand-Weil family.",
            "route_decision": {
                "discard": "using vanishing minimum-eigenvalue defect without exact nesting or certified convergence to one common Weil form",
                "retain": "a common pole-neutral form, cofinal support coverage, and certified approximation plus negative-defect errors tending to zero",
                "next_single_lemma": "PoleNeutralGuinandWeilMatricesConvergeToOneCommonFormWithCertifiedVanishingOperatorError",
            },
            "proof_dag": proof_dag(
                "RH",
                "CofinalPoleNeutralGuinandWeilIntervalLDLCertificatesHaveVanishingNegativeDefect",
                "CommonFormDefectPromotionAndMovingDirectionNoGo",
                "VanishingFiniteSectionDefectWithoutCommonFormConvergenceImpliesWeilPositivity",
                "PoleNeutralGuinandWeilMatricesConvergeToOneCommonFormWithCertifiedVanishingOperatorError",
            ),
            "claim_boundary": "No RH proof. Vanishing defect is promoted only under exact nesting or certified convergence to one fixed form; that arithmetic contract remains open.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-188",
            "theorem_name": "ExactlyFourValuationOnesOtherwiseTwoCycleExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Five-or-more-one words, valuations at least three, and all aperiodic divergence questions remain open.",
            "route_decision": {
                "discard": "treating bounded four-one enumeration as evidence for all horizons",
                "retain": "a cyclic four-gap closed form, an all-horizon odd-quotient exclusion, and exact enumeration only below h=16",
                "next_single_lemma": "NoContractingValuationWordWithExactlyFiveOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "NoContractingValuationWordWithExactlyFourOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
                "ExactlyFourValuationOnesOtherwiseTwoCycleExclusion",
                "FiniteFourOneEnumerationProvesEveryHorizon",
                "NoContractingValuationWordWithExactlyFiveOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            ),
            "claim_boundary": "No Collatz proof or complete cycle exclusion; the entire exactly-four-one/rest-two periodic stratum is newly excluded.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-188",
            "theorem_name": "VonMangoldtPrimePowerContaminationBridge",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No every-target lower bound for the weighted binary convolution is proved, so the contamination bound cannot yet force prime-prime mass.",
            "route_decision": {
                "discard": "identifying the full von Mangoldt convolution with prime-prime mass or using its positivity without a prime-power contamination subtraction",
                "retain": "an explicit every-target lower bound for the total convolution that exceeds the exact prime-power contamination budget",
                "next_single_lemma": "ExplicitBinaryGoldbachVonMangoldtLowerBoundDominatesPrimePowerContaminationForEveryLargeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "SignedVonMangoldtSubhorizonResidualIsBelowExplicitMajorMainForEveryLargeEvenTarget",
                "VonMangoldtPrimePowerContaminationBridge",
                "PositiveVonMangoldtConvolutionEqualsPositivePrimePairMassWithoutSubtraction",
                "ExplicitBinaryGoldbachVonMangoldtLowerBoundDominatesPrimePowerContaminationForEveryLargeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The exact prime-power correction and a sufficient domination inequality are proved; the uniform lower bound is open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-188",
            "theorem_name": "SubFourTwinIntervalExactCountOracleAndDyadicEquivalence",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No independent arithmetic estimate yields positive certified lower endpoints on infinitely many unbounded dyadic blocks.",
            "route_decision": {
                "discard": "treating uniform sub-four interval width as a modest relaxation; it recovers every dyadic twin count exactly",
                "retain": "one-sided sound lower endpoints that are strictly positive on an infinite predeclared dyadic subsequence",
                "next_single_lemma": "IndependentTypeIITwinProjectorLowerEndpointIsPositiveOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "CertifiedStrictlyPositiveTwinProjectorLowerEndpointOnInfinitelyManyPredeclaredDyadicBlocks",
                "SubFourTwinIntervalExactCountOracleAndDyadicEquivalence",
                "UniformSubFourTwinIntervalsAreOnlyAWeakApproximationRequirement",
                "IndependentTypeIITwinProjectorLowerEndpointIsPositiveOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof. The exact dyadic equivalence and width-four information threshold are proved; no infinite positive lower-bound sequence is constructed.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureNestedFourOnePrimePowerDyadicAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-188 resolves none of the four conjectures. It excludes the "
            "entire accelerated Collatz cycle stratum with exactly four "
            "valuation-one entries and all other entries two. The RH, Goldbach, "
            "and Twin results are exact promotion, contamination, and "
            "information-threshold theorems that sharpen the remaining gaps."
        ),
        **sections,
        "cross_problem_synthesis": (
            "A finite certificate promotes only through an explicit invariant "
            "contract: common-form convergence for Weil matrices, an all-horizon "
            "gap bound for Collatz words, prime-power subtraction for weighted "
            "Goldbach mass, and a sound one-sided interval for Twin occupancy."
        ),
        "literature_boundary": {
            "riemann": "Suzuki's 2026 screw-function/operator program and subsequent finite numerical realizations explicitly stop short of RH; TICKET-188 isolates the common-form convergence contract required for promotion.",
            "collatz": "Recent 2-adic cycle work emphasizes that local cycle equations admit ghost solutions; the project result is instead an exact integer-divisibility exclusion for one valuation stratum.",
            "goldbach": "The 2026 exceptional-set work supplies an explicit major-arc formula but not an every-even-target lower bound; prime-power subtraction remains mandatory when using Lambda weights.",
            "twin_prime": "Ford-Maynard prime-producing sieve theory requires substantial Type I/II information; the exact interval oracle theorem supplies no such arithmetic estimate.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "new_infinite_stratum_closure_count": 1,
            "rejected_or_corrected_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, object]]:
    attempts = []
    for problem_id, section_key in [
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin-prime", "twin_prime"),
    ]:
        section = audit[section_key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "status": "open_not_proven",
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": section["route_decision"]["next_single_lemma"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    write_json(
        ROOT / "data" / "open-problem" / "ticket188-nested-fourone-primepower-dyadic.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "nested_fourone_primepower_dyadic_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-188-common-form-defect.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-188-four-one-cycle-exclusion.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-188-prime-power-contamination.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-188-dyadic-interval-oracle.json",
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    by_problem = {attempt["problem_id"]: attempt for attempt in attempts}
    for problem_id, path in paths.items():
        section = audit[section_keys[problem_id]]
        attempt = by_problem[problem_id]
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "ticket_id": section["ticket_id"],
                "problem_id": problem_id,
                "status": "open_not_proven",
                "theorem_name": section["theorem_name"],
                "declared_proposition": section["declared_proposition"],
                "mathematical_argument": section["mathematical_argument"],
                "reproducible_computation": section["reproducible_computation"],
                "discarded_route": attempt["discarded_route"],
                "remaining_gap": attempt["remaining_gap"],
                "candidate_theorem": attempt["candidate_theorem"],
                "claim_boundary": attempt["claim_boundary"],
                "proof_dag": attempt["proof_dag"],
            },
        )


def main() -> None:
    audit = build_audit()
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(
            "TICKET-188 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
