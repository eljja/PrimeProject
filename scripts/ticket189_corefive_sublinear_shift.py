from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket180_finite_information_localization import ordered_affine_numerator
from ticket188_nested_fourone_primepower_dyadic import (
    fraction_payload,
    goldbach_prime_power_row,
    integer_nth_root,
    prime_power_metadata,
)


GENERATED_AT = "2026-08-08T23:30:00+09:00"
SCHEMA = "primeproject.ticket189-corefive-sublinear-shift.v1"
STATUS = (
    "one_additional_infinite_cycle_stratum_closed_"
    "three_exact_promotion_bridges_all_open"
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
                "id": f"{problem_code}-T188-INPUT",
                "label": previous_name,
                "status": "proved_exact_input_or_open_target",
            },
            {
                "id": f"{problem_code}-T189-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T189-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T189-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T188-INPUT", f"{problem_code}-T189-CLOSED"],
            [f"{problem_code}-T189-CLOSED", f"{problem_code}-T189-OPEN"],
            [f"{problem_code}-T189-REJECTED", f"{problem_code}-T189-OPEN"],
        ],
    }


def summable_core_row(core_dimension: int, ambient_dimension: int) -> dict[str, object]:
    if core_dimension < 1 or ambient_dimension < core_dimension:
        raise ValueError("ambient dimension must contain a nonempty fixed core")
    limit_diagonal = [Fraction(1, index + 1) for index in range(core_dimension)]
    core_diagonal = [value + Fraction(1, ambient_dimension) for value in limit_diagonal]
    error = Fraction(1, ambient_dimension)
    adjacent_drift = Fraction(1, ambient_dimension * (ambient_dimension + 1))
    minimum_full_eigenvalue = Fraction(2, ambient_dimension)
    return {
        "fixed_core_dimension_m": core_dimension,
        "ambient_dimension_N": ambient_dimension,
        "limit_core_diagonal": [fraction_payload(value) for value in limit_diagonal],
        "finite_core_diagonal": [fraction_payload(value) for value in core_diagonal],
        "operator_error_to_limit": fraction_payload(error),
        "adjacent_core_operator_drift": fraction_payload(adjacent_drift),
        "exact_remaining_drift_sum": fraction_payload(error),
        "minimum_full_matrix_eigenvalue": fraction_payload(minimum_full_eigenvalue),
        "checks": {
            "tail_sum_equals_core_error": error
            == sum(
                Fraction(1, index * (index + 1))
                for index in range(ambient_dimension, 1000 * ambient_dimension)
            )
            + Fraction(1, 1000 * ambient_dimension),
            "finite_matrix_is_positive": minimum_full_eigenvalue > 0,
            "core_error_matches_uniform_diagonal_shift": all(
                finite - limit == error
                for finite, limit in zip(core_diagonal, limit_diagonal)
            ),
        },
    }


def harmonic_drift_row(ambient_dimension: int) -> dict[str, object]:
    if ambient_dimension < 1:
        raise ValueError("ambient dimension must be positive")
    value = sum((Fraction(1, index) for index in range(1, ambient_dimension + 1)), Fraction())
    return {
        "ambient_dimension_N": ambient_dimension,
        "scalar_core_value_H_N": fraction_payload(value),
        "adjacent_drift": fraction_payload(Fraction(1, ambient_dimension + 1)),
    }


def riemann_summable_core_audit() -> dict[str, object]:
    core_dimension = 4
    rows = [summable_core_row(core_dimension, n) for n in [4, 8, 16, 32, 64]]
    harmonic_rows = [harmonic_drift_row(n) for n in [4, 8, 16, 32, 64, 128]]
    errors = [Fraction(row["operator_error_to_limit"]["exact"]) for row in rows]
    harmonic_values = [Fraction(row["scalar_core_value_H_N"]["exact"]) for row in harmonic_rows]
    harmonic_drifts = [Fraction(row["adjacent_drift"]["exact"]) for row in harmonic_rows]
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(any(left <= right for left, right in zip(errors, errors[1:])))
    failures += int(any(left >= right for left, right in zip(harmonic_values, harmonic_values[1:])))
    failures += int(any(left <= right for left, right in zip(harmonic_drifts, harmonic_drifts[1:])))
    return {
        "theorem": (
            "Let A_N be finite Hermitian matrices. For each fixed m, suppose the "
            "leading m by m cores satisfy ||A_(N+1)^[m]-A_N^[m]||<=d_(N,m) "
            "and sum from N=m to infinity of d_(N,m) is finite. Then every "
            "fixed core converges in operator norm to a Hermitian Q_m, with "
            "the tail bounded by the remaining drift sum, and the Q_m are "
            "compatible principal sections of one form Q on c_00. If also "
            "lambda_min(A_N)>=-eta_N with eta_N tending to zero, then Q is "
            "positive semidefinite. Merely requiring adjacent fixed-core drift "
            "to tend to zero is insufficient for convergence."
        ),
        "proof": (
            "The summable drift bound makes every fixed core Cauchy in the "
            "finite-dimensional operator norm, and summing the tail gives the "
            "quantitative error estimate. Leading-core restriction commutes "
            "with the limit, so Q_(m+1) restricts to Q_m. Interlacing gives "
            "lambda_min(A_N^[m])>=lambda_min(A_N)>=-eta_N; norm convergence and "
            "eta_N->0 therefore make Q_m positive semidefinite. Every vector "
            "in c_00 lies in one such core. For the no-go statement take the "
            "one-dimensional core A_N=H_N. Its adjacent drift 1/(N+1) tends "
            "to zero, but the harmonic sequence diverges."
        ),
        "summable_positive_family": {
            "definition": "A_N=diag(1+1/N,1/2+1/N,...,1/N+1/N)",
            "fixed_core_rows": rows,
        },
        "vanishing_but_nonsummable_drift_counterfamily": {
            "definition": "the scalar fixed core A_N=H_N",
            "rows": harmonic_rows,
            "adjacent_drift_tends_to_zero": True,
            "core_sequence_converges": False,
        },
        "promotion_contract": {
            "fixed_core_drift_has_summable_certified_majorant": True,
            "compatible_limit_form_on_c00_constructed": True,
            "vanishing_negative_floor_promotes_to_positivity": True,
            "actual_pole_neutral_weil_family_verified": False,
        },
        "no_go_scope": (
            "This is an abstract promotion theorem, not a proof about the actual "
            "Guinand-Weil finite sections. PrimeProject has not established a "
            "summable fixed-core majorant or a vanishing negative floor for that "
            "arithmetic family and has not proved the Riemann hypothesis."
        ),
        "failure_count": failures,
    }


def canonical_five_one_word(
    a: int, b: int, c: int, d: int, e: int
) -> tuple[int, ...]:
    if min(a, b, c, d, e) < 1:
        raise ValueError("all five cyclic gaps must be positive")
    return (
        (1,)
        + (2,) * (a - 1)
        + (1,)
        + (2,) * (b - 1)
        + (1,)
        + (2,) * (c - 1)
        + (1,)
        + (2,) * (d - 1)
        + (1,)
        + (2,) * (e - 1)
    )


def five_one_closed_form(a: int, b: int, c: int, d: int, e: int) -> int:
    h = a + b + c + d + e
    return (
        2 ** (2 * h - 5)
        - 3 ** (h - 1)
        + 4**a * 3 ** (h - a - 1)
        + 2 * 4 ** (a + b - 1) * 3 ** (c + d + e - 1)
        + 4 ** (a + b + c - 1) * 3 ** (d + e - 1)
        + 2 * 4 ** (a + b + c + d - 2) * 3 ** (e - 1)
    )


def balanced_five_gaps(horizon: int) -> tuple[int, int, int, int, int]:
    if horizon < 5:
        raise ValueError("horizon must accommodate five positive gaps")
    gaps = [horizon // 5] * 5
    for offset in range(horizon % 5):
        gaps[4 - offset] += 1
    return tuple(gaps)  # type: ignore[return-value]


def five_one_cycle_row(
    a: int, b: int, c: int, d: int, e: int
) -> dict[str, object]:
    word = canonical_five_one_word(a, b, c, d, e)
    h = len(word)
    numerator = ordered_affine_numerator(word)
    denominator = 2 ** (2 * h - 5) - 3**h
    shifted = word[1:] + word[:1]
    return {
        "horizon_h": h,
        "cyclic_gaps": [a, b, c, d, e],
        "largest_gap_is_e": e == max(a, b, c, d, e),
        "affine_numerator_B": str(numerator),
        "cycle_denominator_D": str(denominator),
        "B_mod_D": str(numerator % denominator),
        "checks": {
            "closed_form_matches_recurrence": numerator
            == five_one_closed_form(a, b, c, d, e),
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


def finite_five_one_horizon_row(horizon: int) -> dict[str, object]:
    if not 13 <= horizon <= 21:
        raise ValueError("the exact finite-exception range is h=13..21")
    denominator = 2 ** (2 * horizon - 5) - 3**horizon
    transcript: list[str] = []
    hits: list[dict[str, object]] = []
    formula_failures = 0
    rotation_failures = 0
    for positions in itertools.combinations(range(horizon), 5):
        position_set = set(positions)
        word = tuple(1 if index in position_set else 2 for index in range(horizon))
        numerator = ordered_affine_numerator(word)
        remainder = numerator % denominator
        transcript.append(f"{positions}:{remainder}")
        p0, p1, p2, p3, p4 = positions
        gaps = (
            p1 - p0,
            p2 - p1,
            p3 - p2,
            p4 - p3,
            horizon - p4 + p0,
        )
        rotated = word[p0:] + word[:p0]
        if ordered_affine_numerator(rotated) != five_one_closed_form(*gaps):
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
        "word_count": math.comb(horizon, 5),
        "divisibility_hit_count": len(hits),
        "divisibility_hits": hits,
        "closed_form_failure_count": formula_failures,
        "rotation_identity_failure_count": rotation_failures,
        "remainder_transcript_sha256": hashlib.sha256(
            "\n".join(transcript).encode("ascii")
        ).hexdigest(),
    }


def five_one_global_bound(horizon: int) -> Fraction:
    u = Fraction(3, 4)
    fifth = math.ceil(horizon / 5)
    return (
        Fraction(32, 3) * u ** math.ceil((horizon + 3) / 2)
        + Fraction(16, 3) * u ** (fifth + 2)
        + Fraction(8, 3) * u ** (fifth + 1)
        + Fraction(4, 3) * u**fifth
        + Fraction(256, 3) * u**horizon
    )


def collatz_five_one_audit() -> dict[str, object]:
    finite_rows = [finite_five_one_horizon_row(h) for h in range(13, 22)]
    analytic_rows = [
        five_one_cycle_row(*balanced_five_gaps(h))
        for h in [22, 25, 40, 80, 160]
    ]
    threshold_bound = five_one_global_bound(22)
    failures = sum(
        row["divisibility_hit_count"]
        + row["closed_form_failure_count"]
        + row["rotation_identity_failure_count"]
        + int(not row["contracting"])
        for row in finite_rows
    )
    failures += sum(not check for row in analytic_rows for check in row["checks"].values())
    failures += int(not threshold_bound < 2)
    failures += int(
        any(
            five_one_global_bound(h + 1) > five_one_global_bound(h)
            for h in range(22, 512)
        )
    )
    return {
        "theorem": (
            "No positive accelerated Collatz cycle has a valuation period with "
            "exactly five entries equal to one and every other entry equal to "
            "two, including primitive and imprimitive periods."
        ),
        "proof": (
            "Rotate the five ones into cyclic gaps a,b,c,d,e>=1 with e largest. "
            "Then e>=ceil(h/5), d+e>=ceil(h/5)+1, c+d+e>=ceil(h/5)+2, "
            "and h-a>=ceil((h+3)/2). The exact numerator is "
            "B=4^h/32-3^(h-1)+4^a3^(h-a-1)+2*4^(a+b-1)3^(c+d+e-1)"
            "+4^(a+b+c-1)3^(d+e-1)+2*4^(a+b+c+d-2)3^(e-1), "
            "and D=4^h/32-3^h. Both are odd and B>D. With u=3/4, "
            "the gap inequalities give an all-word sufficient upper majorant "
            "for B<3D equal to (32/3)u^ceil((h+3)/2)+(16/3)"
            "u^(ceil(h/5)+2)+(8/3)u^(ceil(h/5)+1)+(4/3)u^ceil(h/5)"
            "+(256/3)u^h. It is nonincreasing and is already below two at "
            "h=22. Hence 1<B/D<3 for h>=22, so divisibility would force an "
            "impossible odd integer in that interval. Contraction starts at "
            "h=13. Exact enumeration of all sum C(h,5)=72897 words for "
            "13<=h<=21 finds no divisibility hit. Cyclic rotation preserves "
            "divisibility through 2^v B_shift=3B+D."
        ),
        "finite_exception_horizon_rows": finite_rows,
        "analytic_replay_rows": analytic_rows,
        "analytic_bound": {
            "bound_at_h_22": fraction_payload(threshold_bound),
            "required_upper_threshold": fraction_payload(Fraction(2)),
            "analytic_range_starts_at_h": 22,
            "bound_is_nonincreasing_after_threshold": True,
        },
        "aggregate": {
            "infinite_family_proved": True,
            "includes_imprimitive_words": True,
            "contracting_range_starts_at_h": 13,
            "analytic_range_starts_at_h": 22,
            "finite_exception_word_count": sum(row["word_count"] for row in finite_rows),
            "divisibility_hits": sum(row["divisibility_hit_count"] for row in finite_rows),
            "largest_replayed_horizon": analytic_rows[-1]["horizon_h"],
        },
        "no_go_scope": (
            "This closes one additional periodic valuation stratum only. Words "
            "with six or more ones, any valuation at least three, and divergent "
            "aperiodic natural-number orbits remain untreated."
        ),
        "failure_count": failures,
    }


def proper_prime_power_budget_row(
    target: int, metadata: list[tuple[int, int] | None]
) -> dict[str, object]:
    if target < 4:
        raise ValueError("target must be at least four")
    actual_count = sum(
        meta is not None and meta[1] >= 2 for meta in metadata[: target + 1]
    )
    maximum_exponent = target.bit_length() - 1
    exponent_sum_bound = sum(
        integer_nth_root(target, exponent)
        for exponent in range(2, maximum_exponent + 1)
    )
    simplified_bound = math.isqrt(target) + max(maximum_exponent - 2, 0) * integer_nth_root(target, 3)
    contamination_bound = 2.0 * simplified_bound * math.log(target) ** 2
    return {
        "target_N": target,
        "floor_log2_N": maximum_exponent,
        "actual_proper_prime_power_count_A_N": actual_count,
        "exponent_sum_upper_bound": exponent_sum_bound,
        "simplified_upper_bound": simplified_bound,
        "simplified_contamination_mass_bound": contamination_bound,
        "bound_over_N": contamination_bound / target,
        "checks": {
            "actual_count_below_exponent_sum": actual_count <= exponent_sum_bound,
            "exponent_sum_below_simplified_bound": exponent_sum_bound <= simplified_bound,
        },
    }


def goldbach_sublinear_audit() -> dict[str, object]:
    targets = [18, 100, 1_000, 10_000, 100_000, 1_000_000]
    metadata = prime_power_metadata(max(targets))
    budget_rows = [proper_prime_power_budget_row(target, metadata) for target in targets]
    decomposition_rows = [goldbach_prime_power_row(target, metadata) for target in targets]
    failures = sum(not check for row in budget_rows for check in row["checks"].values())
    failures += sum(not check for row in decomposition_rows for check in row["checks"].values())
    failures += sum(
        row["weighted_prime_power_contamination"]
        > budget["simplified_contamination_mass_bound"] + 1e-9
        for row, budget in zip(decomposition_rows, budget_rows)
    )
    return {
        "theorem": (
            "If A(N) is the number of distinct proper prime powers at most N "
            "and L=floor(log_2 N), then A(N)<=sum_(k=2)^L floor(N^(1/k))"
            "<=floor(sqrt(N))+max(L-2,0)floor(N^(1/3)). Consequently the "
            "proper-prime-power part E_pp(N) of the binary von Mangoldt "
            "convolution is at most twice this bound times (log N)^2, which is "
            "o(N). Therefore any certified lower bound R_Lambda(N)>=cN for "
            "all sufficiently large even N, with fixed c>0, eventually forces "
            "positive prime-prime mass and reduces strong Goldbach to a finite "
            "range plus that analytic lower bound."
        ),
        "proof": (
            "Every proper prime power p^k<=N is counted in the k-th root sum. "
            "The k=2 term is at most floor(sqrt N), while every term for k>=3 "
            "is at most floor(N^(1/3)), and there are L-2 such exponents. "
            "TICKET-188 bounds contamination by 2A(N)(log N)^2. Dividing the "
            "displayed estimate by N leaves O(log^2(N)/sqrt(N)+"
            "log^3(N)/N^(2/3)), which tends to zero. Subtracting this budget "
            "from a positive linear all-target lower bound eventually leaves "
            "positive prime-prime mass."
        ),
        "prime_power_budget_rows": budget_rows,
        "finite_decomposition_rows": decomposition_rows,
        "aggregate": {
            "target_count": len(targets),
            "largest_target": targets[-1],
            "sublinear_contamination_budget_proved": True,
            "positive_linear_every_target_lower_bound_proved": False,
        },
        "no_go_scope": (
            "Sublinear contamination does not itself lower-bound the full "
            "von Mangoldt convolution. Finite decline or small observed ratios "
            "cannot replace a rigorous positive linear lower bound for every "
            "sufficiently large even target. Strong Goldbach remains open."
        ),
        "failure_count": failures,
    }


def twin_shift_two_row(
    exponent: int, metadata: list[tuple[int, int] | None]
) -> dict[str, object]:
    lower = 2**exponent
    upper = 2 ** (exponent + 1)
    total_mass = 0.0
    prime_mass = 0.0
    contamination_mass = 0.0
    total_support = 0
    prime_support = 0
    contamination_support = 0
    examples: list[list[int]] = []
    for left in range(lower, upper):
        right = left + 2
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
            if len(examples) < 4:
                examples.append([left, right, left_meta[1], right_meta[1]])
    limit = upper + 2
    proper_count = sum(
        meta is not None and meta[1] >= 2 for meta in metadata[: limit + 1]
    )
    contamination_bound = 2.0 * proper_count * math.log(limit) ** 2
    return {
        "dyadic_exponent_j": exponent,
        "block": [lower, upper],
        "shift_two_von_mangoldt_support_count": total_support,
        "twin_prime_support_count": prime_support,
        "proper_prime_power_contamination_support_count": contamination_support,
        "weighted_shift_two_correlation": total_mass,
        "weighted_twin_prime_mass": prime_mass,
        "weighted_prime_power_contamination": contamination_mass,
        "proper_prime_power_count_A_2X_plus_2": proper_count,
        "contamination_mass_upper_bound": contamination_bound,
        "contamination_examples_left_right_exponents": examples,
        "checks": {
            "support_decomposition_exact": total_support
            == prime_support + contamination_support,
            "weighted_decomposition_replays": abs(
                total_mass - prime_mass - contamination_mass
            )
            < 1e-9,
            "contamination_support_below_two_A": contamination_support
            <= 2 * proper_count,
            "contamination_mass_below_explicit_bound": contamination_mass
            <= contamination_bound,
        },
    }


def twin_shift_two_audit() -> dict[str, object]:
    exponents = list(range(4, 20))
    limit = 2 ** (exponents[-1] + 1) + 2
    metadata = prime_power_metadata(limit)
    rows = [twin_shift_two_row(exponent, metadata) for exponent in exponents]
    no_go_weight = math.log(5) * math.log(3)
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int([25, 27, 2, 3] not in rows[0]["contamination_examples_left_right_exponents"])
    return {
        "theorem": (
            "On every dyadic block [X,2X), the shift-two von Mangoldt "
            "correlation S_Lambda(X) decomposes exactly into twin-prime mass "
            "P_2(X) plus nonnegative proper-prime-power contamination E_2pp(X), "
            "with E_2pp(X)<=2A(2X+2)(log(2X+2))^2=o(X). Hence a sound lower "
            "bound for S_Lambda(X) above this budget proves a twin in that "
            "block. In particular, if S_Lambda(2^j)>=c2^j for one fixed c>0 "
            "on infinitely many unbounded j, then the Twin Prime conjecture "
            "follows. Positivity of S_Lambda alone is insufficient."
        ),
        "proof": (
            "Partition nonzero terms Lambda(n)Lambda(n+2) according to whether "
            "both exponents are one. A contaminated term has a proper prime "
            "power at n or n+2, giving at most 2A(2X+2) possible starts and "
            "weight at most log^2(2X+2). The proper-power count estimate from "
            "the Goldbach track makes this o(X). A fixed positive linear lower "
            "bound therefore eventually exceeds contamination. The term n=25 "
            "is an exact no-go witness: (25,27)=(5^2,3^3) contributes the "
            "positive weight log(5)log(3) although neither endpoint is prime."
        ),
        "finite_dyadic_decomposition_rows": rows,
        "positive_correlation_no_go_witness": {
            "n": 25,
            "n_plus_2": 27,
            "factorization": ["5^2", "3^3"],
            "positive_von_mangoldt_weight": no_go_weight,
            "both_endpoints_prime": False,
        },
        "aggregate": {
            "dyadic_block_count": len(rows),
            "largest_upper_endpoint": rows[-1]["block"][1],
            "prime_power_contamination_bridge_proved": True,
            "positive_linear_infinitely_many_block_lower_bound_proved": False,
            "conjecture_resolution_count": 0,
        },
        "no_go_scope": (
            "The finite rows directly inspect prime powers and primes; they do "
            "not supply independent Type I/II estimates. No positive linear "
            "lower bound is proved on infinitely many unbounded blocks, so the "
            "Twin Prime conjecture remains open."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_summable_core_audit()
    collatz = collatz_five_one_audit()
    goldbach = goldbach_sublinear_audit()
    twin = twin_shift_two_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-189",
            "theorem_name": "SummableFiniteCoreDriftConstructsCompatiblePositiveForm",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No certified summable fixed-core drift majorant or vanishing negative floor is proved for the actual pole-neutral Guinand-Weil matrices.",
            "route_decision": {
                "discard": "using adjacent fixed-core drift tending to zero as if it implied a Cauchy limit",
                "retain": "a summable fixed-core operator majorant, compatible core limits, and a certified vanishing negative floor",
                "next_single_lemma": "PoleNeutralGuinandWeilFixedCoreDriftHasCertifiedSummableOperatorMajorantAndVanishingNegativeFloor",
            },
            "proof_dag": proof_dag(
                "RH",
                "CommonFormDefectPromotionAndMovingDirectionNoGo",
                "SummableFiniteCoreDriftConstructsCompatiblePositiveForm",
                "VanishingAdjacentCoreDriftImpliesCommonFormConvergence",
                "PoleNeutralGuinandWeilFixedCoreDriftHasCertifiedSummableOperatorMajorantAndVanishingNegativeFloor",
            ),
            "claim_boundary": "No RH proof. A precise finite-core promotion theorem and a harmonic-drift no-go example are proved; the arithmetic hypotheses remain open.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-189",
            "theorem_name": "ExactlyFiveValuationOnesOtherwiseTwoCycleExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Six-or-more-one valuation words, valuations at least three, and aperiodic divergence remain open.",
            "route_decision": {
                "discard": "extrapolating finite five-one enumeration to unbounded horizons without an all-word majorant",
                "retain": "the exact five-gap numerator, odd-quotient exclusion from h=22, and exhaustive exact closure of h=13..21",
                "next_single_lemma": "NoContractingValuationWordWithExactlySixOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "ExactlyFourValuationOnesOtherwiseTwoCycleExclusion",
                "ExactlyFiveValuationOnesOtherwiseTwoCycleExclusion",
                "FiniteFiveOneEnumerationProvesEveryHorizon",
                "NoContractingValuationWordWithExactlySixOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            ),
            "claim_boundary": "No Collatz proof. The entire exactly-five-one/rest-two periodic valuation stratum is excluded, including imprimitive periods.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-189",
            "theorem_name": "ProperPrimePowerContaminationHasExplicitSublinearBudget",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No positive linear lower bound is proved for the binary von Mangoldt convolution on every sufficiently large even target.",
            "route_decision": {
                "discard": "claiming that a sublinear contamination upper bound alone proves positive prime-prime mass",
                "retain": "an explicit all-target main-term lower bound that exceeds the sublinear prime-power budget, followed by finite verification",
                "next_single_lemma": "ExplicitMajorArcMainMinusMinorArcErrorExceedsSublinearPrimePowerBudgetForEveryLargeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "VonMangoldtPrimePowerContaminationBridge",
                "ProperPrimePowerContaminationHasExplicitSublinearBudget",
                "SublinearContaminationAloneImpliesStrongGoldbach",
                "ExplicitMajorArcMainMinusMinorArcErrorExceedsSublinearPrimePowerBudgetForEveryLargeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof. The prime-power correction is now explicitly o(N), but the required every-target positive linear lower bound remains open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-189",
            "theorem_name": "ShiftTwoVonMangoldtPrimePowerContaminationBridge",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No positive linear shift-two von Mangoldt lower bound is proved on infinitely many unbounded dyadic blocks.",
            "route_decision": {
                "discard": "using positivity of the shift-two von Mangoldt correlation as if every positive term were a twin-prime pair",
                "retain": "a sound correlation lower bound above an explicit proper-prime-power budget on infinitely many unbounded dyadic blocks",
                "next_single_lemma": "ShiftTwoVonMangoldtCorrelationHasPositiveLinearLowerBoundOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "SubFourTwinIntervalExactCountOracleAndDyadicEquivalence",
                "ShiftTwoVonMangoldtPrimePowerContaminationBridge",
                "PositiveShiftTwoVonMangoldtCorrelationImpliesATwinWithoutSubtraction",
                "ShiftTwoVonMangoldtCorrelationHasPositiveLinearLowerBoundOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof. An exact sublinear contamination bridge and a concrete positivity counterexample are proved; the correlation lower bound is open.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureCoreFiveSublinearShiftAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-189 resolves none of the four conjectures. It excludes the "
            "entire accelerated Collatz cycle stratum with exactly five "
            "valuation-one entries and all other entries two. The RH result is "
            "a compatible-form promotion theorem; Goldbach and Twin share an "
            "explicit sublinear proper-prime-power contamination budget."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common mechanism is quantitative promotion across an infinite "
            "boundary: summable fixed-core drift for RH, an all-horizon gap "
            "majorant for Collatz, and a shared o(N) prime-power subtraction "
            "for Goldbach and shift-two twin correlation."
        ),
        "literature_boundary": {
            "riemann": "Suzuki's 2026 screw-function formulation and numerical finite-section realizations do not prove RH; TICKET-189 states a sufficient summable-drift promotion contract rather than identifying it with those matrices.",
            "collatz": "Recent parity-vector and 2-adic ghost-cycle work does not settle integer cycles; this ticket proves one exact divisibility stratum only.",
            "goldbach": "Recent exceptional-set and explicit major-arc work does not give an every-even-target lower bound; the ticket isolates the remaining uniform inequality after proper-prime-power subtraction.",
            "twin_prime": "Prime-producing sieve results still require strong Type I/II information; this ticket only identifies the precise weighted-correlation subtraction and does not supply that distributional input.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "new_infinite_cycle_stratum_closure_count": 1,
            "cross_problem_primepower_bridge_count": 1,
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
        ROOT / "data" / "open-problem" / "ticket189-corefive-sublinear-shift.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "corefive_sublinear_shift_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-189-summable-core-drift.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-189-five-one-cycle-exclusion.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-189-sublinear-primepower-budget.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-189-shift-two-contamination.json",
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
            "TICKET-189 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
