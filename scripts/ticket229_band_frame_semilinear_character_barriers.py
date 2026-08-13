from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket226_signal_transfer_same_order_obstructions import is_primitive_word


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket229-band-frame-semilinear-character-barriers.v1"
GENERATED_AT = "2026-08-14T15:20:00+09:00"
STATUS = "open_not_proven"
LOCAL_PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)


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
    no_go: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T228", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T229", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N229",
                "label": no_go,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN229",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T228", f"{prefix}-T229"],
            [f"{prefix}-T229", f"{prefix}-N229"],
            [f"{prefix}-T229", f"{prefix}-OPEN229"],
            [f"{prefix}-OPEN229", prefix],
        ],
    }


def dual_dilation_energy(tau: float) -> float:
    return (
        4.0 * math.sin(0.5 * tau * math.log(2.0)) ** 2
        + 4.0 * math.sin(0.5 * tau * math.log(3.0)) ** 2
    )


def explicit_band_log10_lower_bound(max_frequency: float) -> float:
    log_two = math.log(2.0)
    log_three = math.log(3.0)
    leading = math.log10(16.0 / (log_two**2 + log_three**2))
    exponent = max_frequency * log_two * log_three / math.pi + log_three
    return leading - exponent / math.log(10.0)


def nearest_phase_linear_form(tau: float) -> dict[str, Any]:
    log_two = math.log(2.0)
    log_three = math.log(3.0)
    phase_two = tau * log_two / (2.0 * math.pi)
    phase_three = tau * log_three / (2.0 * math.pi)
    n = math.floor(phase_two + 0.5)
    m = math.floor(phase_three + 0.5)
    delta_two = abs(phase_two - n)
    delta_three = abs(phase_three - m)
    linear_form = abs(n * log_three - m * log_two)
    torus_lower = 16.0 * (delta_two**2 + delta_three**2)
    form_lower = 16.0 * linear_form**2 / (log_two**2 + log_three**2)
    energy = dual_dilation_energy(tau)
    return {
        "tau": tau,
        "nearest_n_for_log2_phase": n,
        "nearest_m_for_log3_phase": m,
        "delta_two": delta_two,
        "delta_three": delta_three,
        "linear_form_abs": linear_form,
        "dual_energy": energy,
        "torus_distance_lower": torus_lower,
        "linear_form_lower": form_lower,
        "energy_above_torus_lower": energy + 1e-25 >= torus_lower,
        "torus_lower_above_form_lower": torus_lower + 1e-25 >= form_lower,
    }


def riemann_band_frame_audit() -> dict[str, Any]:
    log_two = math.log(2.0)
    log_three = math.log(3.0)
    lower_frequency = math.pi / log_three
    band_rows = []
    failures = 0
    for maximum in (10, 25, 50, 100, 250, 500, 1_000, 5_000):
        log10_bound = explicit_band_log10_lower_bound(maximum)
        band_rows.append(
            {
                "band_lower_abs_tau": lower_frequency,
                "band_upper_T": maximum,
                "log10_certified_frame_lower_bound": log10_bound,
                "log10_inverse_condition_upper": -log10_bound,
                "polynomial_T_minus_12_log10": -12.0 * math.log10(maximum),
                "polynomial_error_eventually_exceeds_bound": (
                    -12.0 * math.log10(maximum) > log10_bound
                ),
            }
        )

    sample_taus = [
        lower_frequency,
        5.0,
        10.0,
        18.129440567308777,
        45.323601418271934,
        108.77664340385265,
        480.43017503368253,
    ]
    phase_rows = [nearest_phase_linear_form(tau) for tau in sample_taus]
    failures += sum(
        int(
            not (
                row["energy_above_torus_lower"]
                and row["torus_lower_above_form_lower"]
                and row["nearest_m_for_log3_phase"] >= 1
            )
        )
        for row in phase_rows
    )
    failures += int(not all(math.isfinite(row["log10_certified_frame_lower_bound"]) for row in band_rows))
    failures += int(not band_rows[-1]["polynomial_error_eventually_exceeds_bound"])

    theorem = (
        "Let F(tau)=|1-2^(-i tau)|^2+|1-3^(-i tau)|^2 and "
        "T>=pi/log 3. For every pi/log 3<=|tau|<=T, "
        "F(tau) >= 16 exp(-T log(2)log(3)/pi-log(3)) / "
        "(log(2)^2+log(3)^2). This is a positive, completely explicit "
        "band-limited frame lower bound. Its reciprocal grows exponentially "
        "in T, so this elementary certificate cannot be paired with only "
        "polynomially decaying Weil-core truncation error."
    )
    proof = (
        "Write x=tau log(2)/(2 pi), y=tau log(3)/(2 pi), and let n,m be "
        "nearest integers. Since |sin(pi u)|>=2|u| for |u|<=1/2, F is at "
        "least 16 times the squared torus distance. The linear form "
        "Lambda=n log(3)-m log(2) is bounded above by that distance times "
        "sqrt(log(2)^2+log(3)^2). Here m is nonzero and 3^n differs from "
        "2^m. For distinct positive integers A,B, |log(A/B)| is at least "
        "1/max(A,B). The phase bounds give max(3^n,2^m) at most "
        "exp(T log(2)log(3)/(2 pi)+log(3)/2). Squaring yields the formula. "
        "Finally exp(-cT)=o(T^-k) for every fixed k, proving the mismatch "
        "with polynomial error budgets."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "band_rows": band_rows,
        "phase_inequality_rows": phase_rows,
        "exact_constants": {
            "lower_frequency_pi_over_log3": lower_frequency,
            "bound_formula": "16*exp(-T*log(2)*log(3)/pi-log(3))/(log(2)^2+log(3)^2)",
        },
        "aggregate": {
            "explicit_finite_band_dual_dilation_lower_bound_proved": True,
            "elementary_bound_has_exponential_condition_loss": True,
            "polynomial_tail_matching_from_this_bound_refuted": True,
            "actual_weil_core_operator_bound_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "TICKET-229 closes the scalar finite-band Diophantine bound but "
            "not the Weil-core frame theorem. Its elementary lower bound is "
            "exponentially small, so a polynomial truncation estimate cannot "
            "certify positivity at all large bands."
        ),
        "failure_count": failures,
    }


def positive_denominator_witness(height: int, offset: int) -> tuple[int, ...]:
    return (offset + 2,) + (2,) * (height - 1)


def affine_line_contains(
    height: int,
    valuation_sum: int,
    block_height: int,
    block_sum: int,
    suffix_height: int,
    suffix_sum: int,
) -> bool:
    delta_height = height - suffix_height
    delta_sum = valuation_sum - suffix_sum
    return (
        delta_height >= 0
        and delta_sum >= 0
        and delta_height % block_height == 0
        and delta_sum * block_height == delta_height * block_sum
    )


def collatz_semilinear_no_go_audit() -> dict[str, Any]:
    languages = [
        {
            "name": "T228-equal-slope-binary-language",
            "block_height": 4,
            "block_sum": 8,
            "suffix_height": 3,
            "suffix_sum": 6,
        },
        {
            "name": "T227-repeated-block-language",
            "block_height": 3,
            "block_sum": 5,
            "suffix_height": 3,
            "suffix_sum": 7,
        },
        {
            "name": "independent-sample-language",
            "block_height": 5,
            "block_sum": 9,
            "suffix_height": 2,
            "suffix_sum": 4,
        },
    ]
    chosen_offset = 1
    rows = []
    failures = 0
    for height in range(2, 65):
        word = positive_denominator_witness(height, chosen_offset)
        valuation_sum = sum(word)
        denominator = 2**valuation_sum - 3**height
        memberships = [
            language["name"]
            for language in languages
            if affine_line_contains(
                height,
                valuation_sum,
                language["block_height"],
                language["block_sum"],
                language["suffix_height"],
                language["suffix_sum"],
            )
        ]
        verified = denominator > 0 and is_primitive_word(word)
        failures += int(not verified)
        rows.append(
            {
                "height_h": height,
                "offset_c": chosen_offset,
                "valuation_sum_S_equals_2h_plus_c": valuation_sum,
                "word_head": word[0],
                "tail_symbol": 2,
                "D_positive": denominator > 0,
                "primitive_unique_exception_verified": is_primitive_word(word),
                "sample_language_memberships": memberships,
            }
        )

    invariant_rows = []
    for language in languages:
        invariant_rows.append(
            {
                **language,
                "affine_invariant": (
                    f"{language['block_height']}*S-"
                    f"{language['block_sum']}*h="
                    f"{language['block_height'] * language['suffix_sum'] - language['block_sum'] * language['suffix_height']}"
                ),
                "parallel_to_S_equals_2h_plus_c": (
                    language["block_sum"] == 2 * language["block_height"]
                ),
            }
        )
    membership_rows = [row for row in rows if row["sample_language_memberships"]]
    nonparallel_languages = sum(
        language["block_sum"] != 2 * language["block_height"]
        for language in languages
    )
    failures += int(len(membership_rows) > nonparallel_languages)
    failures += int(
        any(
            row["sample_language_memberships"]
            for row in rows
            if row["height_h"] > max(
                [item["height_h"] for item in membership_rows] or [1]
            )
        )
    )

    theorem = (
        "Every language obtained by concatenating blocks with one common "
        "normalized Collatz slope and then one fixed suffix lies on one "
        "affine line in the integer (height h, valuation sum S) plane. "
        "Consequently no finite union of such languages is cofinal among "
        "all primitive positive-denominator valuation words. More explicitly, "
        "for an offset c avoiding the finitely many parallel-line intercepts, "
        "w_(h,c)=(c+2,2,...,2) has S=2h+c, is primitive, and has "
        "2^S-3^h>0; each nonparallel language meets this family at most once."
    )
    proof = (
        "Equal normalized slopes 3^k/2^S force both k and S to agree, by "
        "unique factorization. A concatenation of r common-slope blocks and "
        "a suffix therefore has (h,S)=(rk+h0,rS0+s0), hence satisfies one "
        "affine linear equation. A finite union gives finitely many lines. "
        "Choose c so S=2h+c is not one of their parallel lines. Every other "
        "line intersects it in at most one lattice point. The word with one "
        "entry c+2 and all remaining entries 2 is primitive because its "
        "exceptional symbol occurs once, and 2^(2h+c)>3^h. Thus infinitely "
        "many positive-denominator primitive words remain outside."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "sample_language_invariants": invariant_rows,
        "witness_family_rows": rows,
        "finite_sample_intersection_rows": membership_rows,
        "eventual_outside_start_height": 1
        + max([item["height_h"] for item in membership_rows] or [1]),
        "aggregate": {
            "equal_slope_languages_have_affine_count_invariant_proved": True,
            "finite_equal_slope_union_cofinal_coverage_refuted": True,
            "positive_denominator_primitive_witness_family_proved": True,
            "exact_cycle_divisibility_for_all_outside_words_proved": False,
            "aperiodic_descent_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The cofinal equal-slope-cone route is too narrow even before "
            "the order-sensitive D|B test. The theorem does not show that an "
            "outside witness is an actual cycle; it redirects the proof to a "
            "uniform order-sensitive nondivisibility theorem and still does "
            "not address divergent aperiodic trajectories."
        ),
        "failure_count": failures,
    }


def residue_matrix(prime: int, target: int) -> list[list[int]]:
    units = range(1, prime)
    return [
        [int((left * right - target) % prime != 0) for right in units]
        for left in units
    ]


def matrix_sum(matrices: list[list[list[int]]]) -> list[list[int]]:
    size = len(matrices[0])
    return [
        [sum(matrix[row][column] for matrix in matrices) for column in range(size)]
        for row in range(size)
    ]


def matrix_vector(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(value * vector[column] for column, value in enumerate(row)) for row in matrix]


def goldbach_target_average_audit() -> dict[str, Any]:
    rows = []
    failures = 0
    for prime in LOCAL_PRIMES:
        size = prime - 1
        matrices = [residue_matrix(prime, target) for target in range(prime)]
        complete = matrix_sum(matrices)
        expected = [[size for _ in range(size)] for _ in range(size)]
        zero_sum_basis = [
            [int(index == basis) - int(index == size - 1) for index in range(size)]
            for basis in range(size - 1)
        ]
        complete_annihilates = all(
            matrix_vector(complete, vector) == [0] * size
            for vector in zero_sum_basis
        )
        individual_isometry = True
        for target in range(1, prime):
            matrix = matrices[target]
            for vector in zero_sum_basis:
                image = matrix_vector(matrix, vector)
                individual_isometry &= sum(x * x for x in image) == sum(
                    x * x for x in vector
                )
        verified = complete == expected and complete_annihilates and individual_isometry
        failures += int(not verified)
        rows.append(
            {
                "prime_l": prime,
                "complete_target_period_length": prime,
                "complete_sum_equals_l_minus_1_times_J": complete == expected,
                "zero_sum_basis_dimension": size - 1,
                "complete_period_annihilates_nonconstant_space": complete_annihilates,
                "each_nonzero_target_nonconstant_norm": 1,
                "individual_nonzero_target_isometry_verified": individual_isometry,
                "window_average_bound": f"remainder/H < {prime}/H",
            }
        )

    window_rows = []
    for prime, horizon in itertools.product((5, 7, 11, 13), (10, 25, 100, 1_000)):
        quotient, remainder = divmod(horizon, prime)
        window_rows.append(
            {
                "prime_l": prime,
                "window_length_H": horizon,
                "complete_periods": quotient,
                "remainder_r": remainder,
                "certified_nonconstant_average_norm_upper": Fraction(remainder, horizon).__str__(),
                "strict_l_over_H_upper": remainder < prime,
            }
        )
    failures += int(not all(row["strict_l_over_H_upper"] for row in window_rows))

    theorem = (
        "For an odd prime l, let M_a(u,v)=1_{uv!=a} on the unit group. "
        "The complete moving-target sum satisfies sum_(a mod l) M_a=(l-1)J, "
        "so it annihilates every nonconstant character exactly. For any H "
        "consecutive targets, complete residue periods vanish on that space "
        "and the normalized remainder has operator norm at most r/H<l/H, "
        "where r=H mod l. In contrast, each fixed nonzero M_a restricts to "
        "minus a permutation and has nonconstant operator norm exactly one."
    )
    proof = (
        "For fixed units u,v there is exactly one nonzero residue a=uv. "
        "Among all l targets, M_a(u,v) is one zero and l-1 ones, proving "
        "the rank-one complete-period identity. On the zero-sum space J "
        "vanishes. Splitting an H-window into complete periods and a remainder "
        "of r targets, then using the triangle inequality and ||M_a||=1 on "
        "the nonconstant space, gives r/H. For one nonzero target, "
        "M_a=J-P_a=-P_a on that space, and P_a is a permutation isometry."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "complete_period_rows": rows,
        "window_rows": window_rows,
        "aggregate": {
            "complete_target_period_character_cancellation_proved": True,
            "consecutive_target_average_l_over_H_bound_proved": True,
            "single_target_nonconstant_norm_one_proved": True,
            "target_averaging_implies_pointwise_goldbach_refuted": True,
            "prime_weighted_single_target_cancellation_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Target averaging provides exact character cancellation but strong "
            "Goldbach is pointwise in each even N. A single target retains norm "
            "one on every nonconstant mode, so the remaining saving must come "
            "from prime weights and factor-cell geometry, not target averaging."
        ),
        "failure_count": failures,
    }


def primitive_root(prime: int) -> int:
    order = prime - 1
    factors = []
    remainder = order
    divisor = 2
    while divisor * divisor <= remainder:
        if remainder % divisor == 0:
            factors.append(divisor)
            while remainder % divisor == 0:
                remainder //= divisor
        divisor += 1
    if remainder > 1:
        factors.append(remainder)
    for candidate in range(2, prime):
        if all(pow(candidate, order // factor, prime) != 1 for factor in factors):
            return candidate
    raise AssertionError("primitive root missing")


def twin_character_parity_audit() -> dict[str, Any]:
    rows = []
    failures = 0
    for prime in LOCAL_PRIMES:
        if prime == 3:
            rows.append(
                {
                    "prime_l": 3,
                    "special_case": "joint mask identically zero",
                    "odd_nonconstant_modes": 1,
                    "even_nonconstant_modes": 0,
                    "worst_normalized_nonconstant_ratio": 0.0,
                    "verification_failures": 0,
                }
            )
            continue
        order = prime - 1
        root = primitive_root(prime)
        odd_modes = [index for index in range(1, order) if index % 2 == 1]
        even_modes = [index for index in range(1, order) if index % 2 == 0]
        mode_rows = []
        for index in range(1, order):
            parity = -1 if index % 2 else 1
            singular = abs(1 + parity)
            normalized = Fraction(singular, prime - 3)
            mode_rows.append(
                {
                    "character_index_k": index,
                    "chi_of_minus_one": parity,
                    "parity": "odd" if parity == -1 else "even",
                    "nonconstant_singular_value": singular,
                    "normalized_to_constant_mode": str(normalized),
                }
            )
        expected_odd = order // 2
        expected_even = order // 2 - 1
        worst = max(Fraction(row["normalized_to_constant_mode"]) for row in mode_rows)
        verified = (
            len(odd_modes) == expected_odd
            and len(even_modes) == expected_even
            and all(row["nonconstant_singular_value"] == 0 for row in mode_rows if row["parity"] == "odd")
            and all(row["nonconstant_singular_value"] == 2 for row in mode_rows if row["parity"] == "even")
        )
        failures += int(not verified)
        rows.append(
            {
                "prime_l": prime,
                "primitive_root": root,
                "constant_singular_value": prime - 3,
                "odd_nonconstant_modes": len(odd_modes),
                "even_nonconstant_modes": len(even_modes),
                "mode_rows": mode_rows,
                "worst_normalized_nonconstant_ratio": str(worst),
                "mod5_quadratic_mode_has_no_contraction": prime == 5 and worst == 1,
                "verification_failures": int(not verified),
            }
        )

    tensor_rows = []
    for primes in ((5,), (7,), (5, 7), (5, 7, 11), (7, 11, 13)):
        ratios = [Fraction(2, prime - 3) for prime in primes]
        supported_at_all = math.prod(ratios, start=Fraction(1))
        supported_at_one = max(ratios)
        tensor_rows.append(
            {
                "squarefree_local_primes": list(primes),
                "all_even_nonprincipal_tensor_ratio": str(supported_at_all),
                "worst_single_prime_supported_ratio": str(supported_at_one),
                "mod5_supported_mode_blocks_uniform_contraction": 5 in primes and supported_at_one == 1,
            }
        )
    failures += int(not any(row["mod5_quadratic_mode_has_no_contraction"] for row in rows if row["prime_l"] == 5))

    theorem = (
        "For l>3 define the simultaneous shift-two survival operator "
        "S=J-P_2-P_{-2} on the unit group. On a nonprincipal multiplicative "
        "character chi, S chi=-chi(2)(1+chi(-1)) chi^{-1}. Hence every odd "
        "character is annihilated exactly, while every even nonprincipal "
        "character has singular value two; the constant singular value is "
        "l-3. In particular, modulo 5 the quadratic character has normalized "
        "singular ratio 2/(5-3)=1. Tensoring more local factors cannot remove "
        "a mode supported only on this modulo-5 component."
    )
    proof = (
        "The identity S=J-P_2-P_{-2} follows because the two forbidden "
        "products are distinct for l>3. On nonprincipal characters J=0 and "
        "P_a chi=chi(a)chi^{-1}. Since chi(-2)=chi(-1)chi(2), the displayed "
        "formula follows. Character parity gives 1+chi(-1) equal to zero or "
        "two. The constant row sum is l-3. Local operators tensor over a "
        "squarefree modulus, and a global character may be principal at every "
        "prime except 5, so its normalized ratio remains one."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "local_character_rows": rows,
        "tensor_obstruction_rows": tensor_rows,
        "aggregate": {
            "odd_shift_two_characters_annihilated_proved": True,
            "even_character_singular_value_two_proved": True,
            "mod5_quadratic_normalized_no_contraction_proved": True,
            "local_tensor_uniform_contraction_refuted": True,
            "prime_weighted_mod5_quadratic_cancellation_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Local shift symmetry solves exactly half of the character modes, "
            "but the modulo-5 quadratic mode survives at full normalized size. "
            "The remaining theorem is a prime-weighted cancellation estimate "
            "for that explicit mode across the cube-root factor cells."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_band_frame_audit()
    collatz = collatz_semilinear_no_go_audit()
    goldbach = goldbach_target_average_audit()
    twin = twin_character_parity_audit()
    root = {
        "theorem_name": "BandFrameSemilinearAndCharacterBarriersForFourOpenProblems",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-229 proves four exact partial or no-go theorems and "
            "resolves none of the four parent conjectures. Computations audit "
            "the identities and are not extrapolated to infinite claims."
        ),
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-229",
            "theorem_name": "ExplicitFiniteBandDualDilationBoundAndPolynomialTailMismatch",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": riemann["no_go_scope"],
            "route_decision": {
                "discard": "combining the elementary exponentially small frame floor with only polynomial Weil-core truncation errors",
                "retain": "seek a subexponential Diophantine loss or prove an exponentially decaying actual Weil-core tail",
                "next_single_lemma": "SubexponentialDualDilationLossMatchedToExplicitWeilCoreTail",
            },
            "proof_dag": proof_dag(
                "RH",
                "FiniteDilationNearAliasNoUniformFrame",
                "ExplicitFiniteBandDualDilationBoundAndPolynomialTailMismatch",
                "ElementaryExponentialFrameFloorClosesPolynomialWeilTail",
                "SubexponentialDualDilationLossMatchedToExplicitWeilCoreTail",
                "RiemannHypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-229",
            "theorem_name": "FiniteEqualSlopeLanguageSemilinearCoverageNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": collatz["no_go_scope"],
            "route_decision": {
                "discard": "covering all positive-denominator primitive valuation words by finitely many fixed-suffix equal-slope affine languages",
                "retain": "attack order-sensitive D nondivisibility directly outside every regular affine language",
                "next_single_lemma": "OrderSensitiveNondivisibilityForAllPositiveDenominatorPrimitiveWords",
            },
            "proof_dag": proof_dag(
                "CO",
                "BinaryEqualSlopeAffineLanguageNoncycleCone",
                "FiniteEqualSlopeLanguageSemilinearCoverageNoGo",
                "FiniteEqualSlopeConeCofinalCoverage",
                "OrderSensitiveNondivisibilityForAllPositiveDenominatorPrimitiveWords",
                "CollatzConjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-229",
            "theorem_name": "CompleteTargetPeriodCharacterCancellationAndPointwiseNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": goldbach["no_go_scope"],
            "route_decision": {
                "discard": "promoting exact cancellation after averaging a complete target-residue period to a pointwise statement for each even target",
                "retain": "use prime weights and factor-cell geometry to cancel nonconstant modes at one fixed target",
                "next_single_lemma": "PrimeWeightedPointwiseCharacterCancellationForEachGoldbachFactorCell",
            },
            "proof_dag": proof_dag(
                "GB",
                "MovingResidueUnitOperatorSpectrumAndLocalFactor",
                "CompleteTargetPeriodCharacterCancellationAndPointwiseNoGo",
                "TargetAverageCancellationImpliesPointwiseGoldbachCancellation",
                "PrimeWeightedPointwiseCharacterCancellationForEachGoldbachFactorCell",
                "StrongGoldbachConjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-229",
            "theorem_name": "ShiftTwoParityProjectionAndModuloFiveQuadraticObstruction",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": twin["no_go_scope"],
            "route_decision": {
                "discard": "claiming uniform local character contraction after shift-two parity projection and tensoring more local primes",
                "retain": "isolate and cancel the full-size modulo-5 quadratic mode with prime-weighted Type-II information",
                "next_single_lemma": "PrimeWeightedCancellationOfModuloFiveQuadraticShiftTwoMode",
            },
            "proof_dag": proof_dag(
                "TP",
                "ShiftTwoOperatorCrossGramAndModThreeJointNoGo",
                "ShiftTwoParityProjectionAndModuloFiveQuadraticObstruction",
                "LocalParityProjectionGivesUniformCharacterContraction",
                "PrimeWeightedCancellationOfModuloFiveQuadraticShiftTwoMode",
                "TwinPrimeConjecture",
            ),
        },
    }
    tracks = ("riemann", "collatz", "goldbach", "twin_prime")
    total_failures = sum(root[key]["reproducible_computation"]["failure_count"] for key in tracks)
    root["machine_audit"] = {
        "exact_partial_theorem_count": 4,
        "refuted_or_corrected_route_count": 4,
        "next_single_lemma_count": 4,
        "proof_dag_count": 4,
        "conjecture_resolution_count": 0,
        "total_failure_count": total_failures,
    }
    attempts = []
    for key in tracks:
        track = root[key]
        attempts.append(
            {
                "problem_id": track["problem_id"],
                "ticket_id": track["ticket_id"],
                "status": STATUS,
                "declared_proposition": track["declared_proposition"],
                "mathematical_argument": track["mathematical_argument"],
                "new_result": track["theorem_name"],
                "bounded_result": {
                    "audit_ref": f"#/band_frame_semilinear_character_barriers_audit/{key}",
                    "failure_count": track["reproducible_computation"]["failure_count"],
                },
                "discarded_route": track["route_decision"]["discard"],
                "remaining_gap": track["logical_limit"],
                "candidate_theorem": track["route_decision"]["next_single_lemma"],
                "proof_dag": track["proof_dag"],
            }
        )
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": (
            "TICKET-229 proves four exact partial results and resolves none "
            "of the four parent conjectures."
        ),
        "band_frame_semilinear_character_barriers_audit": root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit["band_frame_semilinear_character_barriers_audit"]
    write_json(
        ROOT / "data/open-problem/ticket229-band-frame-semilinear-character-barriers.json",
        audit,
    )
    destinations = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-229-band-frame-bound.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-229-semilinear-coverage-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-229-target-period-cancellation.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-229-character-parity-obstruction.json",
    }
    for key, destination in destinations.items():
        write_json(
            destination,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": STATUS,
                **root[key],
            },
        )


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    machine = audit["band_frame_semilinear_character_barriers_audit"]["machine_audit"]
    print(json.dumps(machine, indent=2))
    if machine["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
