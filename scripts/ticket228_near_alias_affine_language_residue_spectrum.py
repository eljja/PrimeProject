from __future__ import annotations

import cmath
import itertools
import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket226_signal_transfer_same_order_obstructions import (
    collatz_intercept,
    cube_root_support,
    is_primitive_word,
)
from ticket227_mellin_block_buchstab_lifts import rough_semiprime_factor_pairs


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket228-near-alias-affine-language-residue-spectrum.v1"
GENERATED_AT = "2026-08-14T05:40:00+09:00"
STATUS = "open_not_proven"
HORIZONS = (10_000, 100_000, 1_000_000)
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
    corrected: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T227", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T228", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N228",
                "label": corrected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN228",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T227", f"{prefix}-T228"],
            [f"{prefix}-T228", f"{prefix}-N228"],
            [f"{prefix}-T228", f"{prefix}-OPEN228"],
            [f"{prefix}-OPEN228", prefix],
        ],
    }


def continued_fraction_near_alias_rows(limit: int = 20_000_000) -> list[dict[str, Any]]:
    with localcontext() as context:
        context.prec = 80
        alpha = Decimal(3).ln() / Decimal(2).ln()
        value = alpha
        p_previous_previous, p_previous = 0, 1
        q_previous_previous, q_previous = 1, 0
        rows = []
        index = 0
        while True:
            coefficient = int(value)
            numerator = coefficient * p_previous + p_previous_previous
            denominator = coefficient * q_previous + q_previous_previous
            if denominator > limit:
                break
            error = abs(Decimal(denominator) * alpha - Decimal(numerator))
            if denominator >= 2:
                phase_gap = float(error)
                normalized_energy = 4.0 * math.sin(math.pi * phase_gap) ** 2
                tau = 2.0 * math.pi * denominator / math.log(2.0)
                rows.append(
                    {
                        "convergent_index": index,
                        "p_over_q": f"{numerator}/{denominator}",
                        "numerator_p": numerator,
                        "denominator_q": denominator,
                        "absolute_q_log3_over_log2_minus_p": str(error),
                        "frequency_tau_2pi_q_over_log2": tau,
                        "q2_phase_factor_abs": 0.0,
                        "q3_phase_factor_abs": 2.0
                        * abs(math.sin(math.pi * phase_gap)),
                        "normalized_dual_energy": normalized_energy,
                    }
                )
            p_previous_previous, p_previous = p_previous, numerator
            q_previous_previous, q_previous = q_previous, denominator
            remainder = value - coefficient
            if not remainder:
                break
            value = 1 / remainder
            index += 1
        return rows


def riemann_finite_dilation_no_go_audit() -> dict[str, Any]:
    rows = continued_fraction_near_alias_rows()
    failures = 0
    decreasing = all(
        current["normalized_dual_energy"]
        < previous["normalized_dual_energy"]
        for previous, current in zip(rows, rows[1:])
    )
    failures += int(not decreasing)
    failures += int(not rows or rows[-1]["normalized_dual_energy"] >= 1e-12)
    for row in rows:
        tau = row["frequency_tau_2pi_q_over_log2"]
        factor_two = 1 - cmath.exp(-1j * tau * math.log(2.0))
        factor_three = 1 - cmath.exp(-1j * tau * math.log(3.0))
        # q=2 is mathematically exact; this only audits floating-point evaluation.
        row["floating_phase_energy"] = abs(factor_two) ** 2 + abs(factor_three) ** 2
        row["floating_vs_reduced_phase_error"] = abs(
            row["floating_phase_energy"] - row["normalized_dual_energy"]
        )

    theorem = (
        "For every finite set Q={q_1,...,q_m} of dilation ratios greater "
        "than one, F_Q(tau)=sum_j |1-q_j^(-i tau)|^2 has arbitrarily "
        "large near-zero frequencies: for every T and epsilon>0 there is "
        "tau>T with F_Q(tau)<epsilon. Thus no finite dilation family has "
        "a positive frequency-uniform lower frame bound on the full "
        "imaginary axis. For Q={2,3}, convergents p/q to log(3)/log(2) "
        "give tau=2 pi q/log(2), where the q=2 factor is exactly zero and "
        "the q=3 factor tends to zero."
    )
    proof = (
        "Fix q_1 and apply simultaneous Dirichlet approximation to the "
        "m-1 ratios log(q_j)/log(q_1). For every N there is an integer n "
        "with 1<=n<=N^(m-1) and every distance from n log(q_j)/log(q_1) "
        "to an integer at most 1/N. At tau=2 pi n/log(q_1), the first "
        "phase is one and every other phase differs from one by at most "
        "2 pi/N. If the selected n are unbounded this gives arbitrarily "
        "large near aliases. If some n repeats for unbounded N, it is an "
        "exact common alias and its multiples give arbitrarily large exact "
        "zeros. Either case forces the tail infimum of F_Q to be zero."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "dual_ratio": [2, 3],
        "near_alias_rows": rows,
        "aggregate": {
            "ticket227_exact_common_alias_elimination_preserved": True,
            "finite_dilation_arbitrarily_large_near_aliases_proved": True,
            "unweighted_uniform_full_line_frame_bound_refuted": True,
            "explicit_bandlimited_diophantine_loss_bound_proved": False,
            "weil_positivity_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "Mode-wise injectivity does not imply stable inversion. Even after "
            "removing Gamma decay, every finite dilation set has unbounded near "
            "aliases. A useful frame theorem must be bandlimited or carry an "
            "explicit frequency-dependent Diophantine loss."
        ),
        "failure_count": failures,
    }


def affine_data(word: tuple[int, ...]) -> tuple[int, int, int]:
    return 3 ** len(word), 2 ** sum(word), collatz_intercept(word)


def collatz_branching_language_audit() -> dict[str, Any]:
    blocks = ((1, 3, 3, 1), (2, 3, 1, 2))
    suffix = (1, 4, 1)
    block_data = [affine_data(block) for block in blocks]
    suffix_data = affine_data(suffix)
    common_a = Fraction(block_data[0][0], block_data[0][1])
    block_intercepts = [Fraction(data[2], data[1]) for data in block_data]
    suffix_a = Fraction(suffix_data[0], suffix_data[1])
    suffix_b = Fraction(suffix_data[2], suffix_data[1])

    endpoint_values = []
    for intercept in (min(block_intercepts), max(block_intercepts)):
        for t in (Fraction(0), common_a):
            endpoint_values.append(
                (
                    suffix_a
                    * intercept
                    * (1 - t)
                    / (1 - common_a)
                    + suffix_b
                )
                / (1 - suffix_a * t)
            )
    cone_lower = min(endpoint_values)
    cone_upper = max(endpoint_values)

    failures = 0
    level_rows = []
    total_words = 0
    for level in range(1, 11):
        ratios = []
        level_failures = 0
        for choices in itertools.product(range(2), repeat=level):
            word = tuple(
                exponent
                for choice in choices
                for exponent in blocks[choice]
            ) + suffix
            a_word, c_word, b_word = affine_data(word)
            denominator = c_word - a_word
            ratio = Fraction(b_word, denominator)
            ratios.append(ratio)
            verified = (
                denominator > 0
                and cone_lower <= ratio <= cone_upper
                and 1 < ratio < 2
                and word.count(4) == 1
                and is_primitive_word(word)
                and b_word % denominator != 0
            )
            level_failures += int(not verified)
        failures += level_failures
        total_words += len(ratios)
        level_rows.append(
            {
                "block_count_r": level,
                "distinct_word_count_2_to_r": len(ratios),
                "minimum_B_over_D": str(min(ratios)),
                "maximum_B_over_D": str(max(ratios)),
                "minimum_B_over_D_float": float(min(ratios)),
                "maximum_B_over_D_float": float(max(ratios)),
                "verification_failures": level_failures,
            }
        )
    failures += int(
        not (
            block_data == [(81, 256, 221), (81, 256, 223)]
            and suffix_data == (27, 64, 47)
            and cone_lower == Fraction(887, 700)
            and cone_upper == Fraction(7123, 5600)
            and 1 < cone_lower < cone_upper < 2
        )
    )

    theorem = (
        "Let U_0=(1,3,3,1), U_1=(2,3,1,2), and V=(1,4,1). "
        "The two blocks have the same normalized slope 81/256 and "
        "normalized intercepts 221/256 and 223/256; V has slope 27/64 "
        "and intercept 47/64. For every r>=1 and every binary string "
        "epsilon of length r, the word U_epsilon1...U_epsilonr V has "
        "887/700 <= B/D <= 7123/5600, hence 1<B/D<2. It contains one "
        "symbol 4, so it is primitive. Therefore all 2^r words at level r "
        "are distinct primitive noncycles."
    )
    proof = (
        "Write each normalized block map as x -> a x+b_j with common "
        "a=81/256 and b_j in [221/256,223/256]. After r blocks its "
        "intercept y lies between b_min(1-a^r)/(1-a) and "
        "b_max(1-a^r)/(1-a). Appending V gives fixed-point ratio "
        "R=(c y+d)/(1-c a^r). Each extreme is fractional-linear in "
        "t=a^r and is bounded by its values at t=0 and t=a. The four "
        "exact endpoint values have minimum 887/700 and maximum "
        "7123/5600. Thus R is never integral. A nontrivial power repeats "
        "every symbol count, while these words contain exactly one 4, so "
        "they are primitive."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "blocks": [list(block) for block in blocks],
        "block_affine_data": [list(data) for data in block_data],
        "suffix": list(suffix),
        "suffix_affine_data": list(suffix_data),
        "global_ratio_cone": {
            "lower": str(cone_lower),
            "upper": str(cone_upper),
            "inside_open_unit_interval": [1, 2],
        },
        "level_rows": level_rows,
        "aggregate": {
            "equal_slope_affine_cone_theorem_proved": True,
            "binary_branching_primitive_noncycle_language_proved": True,
            "words_computationally_checked": total_words,
            "universal_prime_power_witness_is_more_than_divisibility_restatement": False,
            "all_primitive_cycle_words_excluded": False,
            "aperiodic_descent_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "TICKET-224 already proved that a prime-power witness exists "
            "exactly when D does not divide B, so demanding a universal "
            "witness merely renames the cycle-exclusion target and does not "
            "address divergent aperiodic orbits. The new affine cone certifies "
            "an exponentially branching language, not every primitive word."
        ),
        "failure_count": failures,
    }


def residue_matrix(prime: int, target: int) -> list[list[int]]:
    units = range(1, prime)
    return [
        [int((left * right - target) % prime != 0) for right in units]
        for left in units
    ]


def transpose_product(
    left: list[list[int]], right: list[list[int]]
) -> list[list[int]]:
    size = len(left)
    return [
        [
            sum(left[row][column_left] * right[row][column_right] for row in range(size))
            for column_right in range(size)
        ]
        for column_left in range(size)
    ]


def single_residue_operator_check(prime: int, target: int) -> dict[str, Any]:
    size = prime - 1
    matrix = residue_matrix(prime, target)
    gram = transpose_product(matrix, matrix)
    if target % prime == 0:
        expected = [[size for _ in range(size)] for _ in range(size)]
        principal = size
        nonconstant = 0
        survival = Fraction(1, 1)
    else:
        expected = [
            [size - 1 if row == column else size - 2 for column in range(size)]
            for row in range(size)
        ]
        principal = size - 1
        nonconstant = 1
        survival = Fraction(size - 1, size)
    row_sums = {sum(row) for row in matrix}
    return {
        "prime_l": prime,
        "target_residue_a": target % prime,
        "row_sum": next(iter(row_sums)) if len(row_sums) == 1 else None,
        "principal_singular_value": principal,
        "nonconstant_singular_value": nonconstant,
        "nonconstant_multiplicity": size - 1,
        "local_survival_fraction": str(survival),
        "gram_identity_verified": gram == expected,
        "constant_row_sum_verified": len(row_sums) == 1,
    }


def exhaustive_single_operator_audit() -> tuple[list[dict[str, Any]], int, int]:
    rows = []
    failures = 0
    residue_cases = 0
    for prime in LOCAL_PRIMES:
        local_failures = 0
        for target in range(prime):
            result = single_residue_operator_check(prime, target)
            residue_cases += 1
            local_failures += int(
                not (
                    result["gram_identity_verified"]
                    and result["constant_row_sum_verified"]
                )
            )
        failures += local_failures
        rows.append(
            {
                "prime_l": prime,
                "residues_checked": prime,
                "zero_target": single_residue_operator_check(prime, 0),
                "nonzero_target": single_residue_operator_check(prime, 1),
                "verification_failures": local_failures,
            }
        )
    return rows, residue_cases, failures


def factor_pair_residue_rows(mode: str) -> list[dict[str, Any]]:
    rows = []
    for horizon in HORIZONS:
        cutoff, _, _, _, primes = cube_root_support(horizon)
        pairs = rough_semiprime_factor_pairs(horizon, cutoff, primes)
        for prime in LOCAL_PRIMES:
            if prime > cutoff:
                continue
            products = list(pairs)
            if mode == "goldbach":
                target = horizon % prime
                excluded = sum(product % prime == target for product in products)
                rows.append(
                    {
                        "horizon_or_target": horizon,
                        "cutoff_z": cutoff,
                        "prime_l": prime,
                        "target_residue": target,
                        "rough_semiprime_pairs": len(products),
                        "empirical_excluded_pairs": excluded,
                        "empirical_surviving_pairs": len(products) - excluded,
                        "divisor_case_has_zero_exclusions": target != 0 or excluded == 0,
                    }
                )
            else:
                minus_excluded = sum(product % prime == 2 % prime for product in products)
                plus_excluded = sum(product % prime == (-2) % prime for product in products)
                joint_survivors = sum(
                    product % prime not in {2 % prime, (-2) % prime}
                    for product in products
                )
                rows.append(
                    {
                        "horizon_or_target": horizon,
                        "cutoff_z": cutoff,
                        "prime_l": prime,
                        "rough_semiprime_pairs": len(products),
                        "qr_minus_2_excluded": minus_excluded,
                        "qr_plus_2_excluded": plus_excluded,
                        "joint_local_survivors": joint_survivors,
                        "mod3_joint_zero_verified": prime != 3 or joint_survivors == 0,
                    }
                )
    return rows


def goldbach_residue_spectrum_audit() -> dict[str, Any]:
    operator_rows, residue_cases, failures = exhaustive_single_operator_audit()
    empirical_rows = factor_pair_residue_rows("goldbach")
    failures += sum(
        int(not row["divisor_case_has_zero_exclusions"])
        for row in empirical_rows
    )
    theorem = (
        "Let l be an odd prime, G=(Z/lZ)^*, n=l-1, and define the unit "
        "residue operator M_a(u,v)=1_{uv != a}. If a=0 then M_a=J has "
        "singular values n,0,...,0. If a is nonzero then M_a=J-P_a, "
        "where P_a(u,v)=1_{uv=a} is a symmetric permutation matrix, and "
        "M_a^T M_a=I+(n-2)J. Hence its singular values are l-2 on the "
        "constant mode and 1 with multiplicity l-2 on the nonconstant "
        "modes. Applied with a=N mod l, the local survival fraction is 1 "
        "when l divides N and (l-2)/(l-1) otherwise."
    )
    proof = (
        "Products of units never equal zero, giving M_0=J. For nonzero a, "
        "each row and column has one excluded entry, so P_a is the "
        "permutation u -> a/u. This map is an involution, P_a is symmetric, "
        "P_a^2=I, and JP_a=P_aJ=J. Expanding (J-P_a)^2 with J^2=nJ gives "
        "I+(n-2)J. The constant vector and its orthogonal complement give "
        "the stated singular values and exact local fractions."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "operator_rows": operator_rows,
        "exhaustive_residue_cases_checked": residue_cases,
        "factor_cell_residue_rows": empirical_rows,
        "aggregate": {
            "moving_residue_operator_spectrum_proved": True,
            "target_dependent_local_factor_proved": True,
            "nonconstant_character_modes_survive_locally": True,
            "scalar_local_density_suffices_for_pointwise_goldbach": False,
            "uniform_moving_target_character_cancellation_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Extracting the scalar local survival factor does not estimate the "
            "actual prime-weighted factor cells: every nonzero target leaves "
            "l-2 nonconstant unit modes with singular value one. Uniform "
            "moving-target character cancellation across unbounded cells is open."
        ),
        "failure_count": failures,
    }


def twin_cross_operator_rows() -> tuple[list[dict[str, Any]], int]:
    rows = []
    failures = 0
    for prime in LOCAL_PRIMES:
        size = prime - 1
        minus_matrix = residue_matrix(prime, 2)
        plus_matrix = residue_matrix(prime, -2)
        cross_gram = transpose_product(minus_matrix, plus_matrix)
        cross_shape_verified = all(
            sorted(row) == [size - 2] * (size - 1) + [size - 1]
            for row in cross_gram
        )
        joint_allowed = sum(
            minus_matrix[row][column] * plus_matrix[row][column]
            for row in range(size)
            for column in range(size)
        )
        expected_joint = size * (size - 2)
        minus_check = single_residue_operator_check(prime, 2)
        plus_check = single_residue_operator_check(prime, -2)
        verified = (
            cross_shape_verified
            and joint_allowed == expected_joint
            and minus_check["gram_identity_verified"]
            and plus_check["gram_identity_verified"]
        )
        failures += int(not verified)
        rows.append(
            {
                "prime_l": prime,
                "individual_principal_singular_value": prime - 2,
                "individual_nonconstant_singular_value": 1,
                "cross_gram_zero_sum_action": "multiplication-by-minus-one permutation",
                "cross_gram_shape_verified": cross_shape_verified,
                "joint_allowed_unit_pairs": joint_allowed,
                "expected_joint_allowed_unit_pairs": expected_joint,
                "joint_survival_fraction": str(Fraction(prime - 3, prime - 1)),
                "mod3_joint_mask_is_zero": prime == 3 and joint_allowed == 0,
            }
        )
    return rows, failures


def twin_residue_spectrum_audit() -> dict[str, Any]:
    operator_rows, failures = twin_cross_operator_rows()
    empirical_rows = factor_pair_residue_rows("twin")
    failures += sum(
        int(not row["mod3_joint_zero_verified"])
        for row in empirical_rows
    )
    theorem = (
        "For every odd prime l, the qr-2 and qr+2 local masks are "
        "M_2=J-P_2 and M_{-2}=J-P_{-2}. Each has constant singular value "
        "l-2 and nonconstant singular value 1. Their cross Gram matrix is "
        "M_2^T M_{-2}=(l-3)J+P_2P_{-2}; on the zero-sum subspace it is "
        "the permutation induced by multiplication by -1, so the two side "
        "channels retain coherent nonconstant modes. At l=3, the forbidden "
        "product residues 2 and -2 exhaust all units, so no rough product "
        "qr can make both qr-2 and qr+2 locally prime-eligible."
    )
    proof = (
        "Apply the Goldbach unit-operator identity to a=2 and a=-2. "
        "Expanding the cross product gives (n-2)J+P_2P_{-2}; composition "
        "of u -> 2/u and u -> -2/u is multiplication by -1. For l>3, "
        "the two forbidden residues are distinct and each row retains "
        "l-3 of l-1 columns. For l=3 they are the two units themselves, "
        "so the joint mask is identically zero."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "cross_operator_rows": operator_rows,
        "factor_cell_residue_rows": empirical_rows,
        "aggregate": {
            "shift_two_individual_operator_spectrum_proved": True,
            "shift_two_cross_gram_permutation_proved": True,
            "mod3_simultaneous_side_channel_route_refuted": True,
            "nonconstant_shifted_character_modes_cancelled": False,
            "uniform_shifted_bilinear_power_saving_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The exact local spectra do not yield cancellation in the actual "
            "prime-weighted qr+/-2 sums. Coupling the two side channels through "
            "simultaneous local survival is impossible already modulo three; "
            "they must be estimated separately with character-mode cancellation."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_finite_dilation_no_go_audit()
    collatz = collatz_branching_language_audit()
    goldbach = goldbach_residue_spectrum_audit()
    twin = twin_residue_spectrum_audit()
    root = {
        "theorem_name": "NearAliasAffineLanguageAndResidueSpectrumForFourOpenProblems",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-228 proves four exact operator or affine-language results "
            "and resolves none of the four parent conjectures. Finite tables "
            "audit exact identities and are not extrapolated."
        ),
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-228",
            "theorem_name": "FiniteDilationNearAliasNoUniformFrame",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": riemann["no_go_scope"],
            "route_decision": {
                "discard": "seeking a positive frequency-uniform frame lower bound from any finite set of dilation ratios",
                "retain": "use bandlimited Weil cores with an explicit frequency-dependent Diophantine loss",
                "next_single_lemma": "ExplicitDiophantineLossDualDilationFrameBoundOnBandlimitedWeilCores",
            },
            "proof_dag": proof_dag(
                "RH",
                "DualDilationMellinAliasEliminationAndSingleRatioNoGo",
                "FiniteDilationNearAliasNoUniformFrame",
                "FiniteDilationUniformFullLineFrameBound",
                "ExplicitDiophantineLossDualDilationFrameBoundOnBandlimitedWeilCores",
                "RiemannHypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-228",
            "theorem_name": "BinaryEqualSlopeAffineLanguageNoncycleCone",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": collatz["no_go_scope"],
            "route_decision": {
                "discard": "treating universal prime-power witnesses as a bridge stronger than the exact D-divisibility condition already proved in TICKET-224",
                "retain": "build cofinal affine-cone languages whose exact fixed-point intervals avoid every integer",
                "next_single_lemma": "CofinalEqualSlopeAffineConeCoverForAllPrimitiveCycleCandidateWords",
            },
            "proof_dag": proof_dag(
                "CO",
                "RepeatedBlockSuffixUnitIntervalCertificate",
                "BinaryEqualSlopeAffineLanguageNoncycleCone",
                "UniversalPrimePowerWitnessIsANewStrictlyWeakerBridge",
                "CofinalEqualSlopeAffineConeCoverForAllPrimitiveCycleCandidateWords",
                "CollatzConjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-228",
            "theorem_name": "MovingResidueUnitOperatorSpectrumAndLocalFactor",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": goldbach["no_go_scope"],
            "route_decision": {
                "discard": "using only scalar local survival densities after the factor-cell lift",
                "retain": "extract the target-dependent local factor and bound every surviving nonconstant unit-character mode",
                "next_single_lemma": "UniformMovingTargetCharacterCancellationAfterLocalSpectrumExtraction",
            },
            "proof_dag": proof_dag(
                "GB",
                "CubeRootBuchstabFactorLiftAndDivisorExceptionSplit",
                "MovingResidueUnitOperatorSpectrumAndLocalFactor",
                "ScalarLocalDensityControlsEveryMovingFactorCell",
                "UniformMovingTargetCharacterCancellationAfterLocalSpectrumExtraction",
                "StrongGoldbachConjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-228",
            "theorem_name": "ShiftTwoOperatorCrossGramAndModThreeJointNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": twin["no_go_scope"],
            "route_decision": {
                "discard": "forcing cancellation by requiring simultaneous local survival of the qr-2 and qr+2 side channels",
                "retain": "diagonalize each shifted residue operator and prove separate character-mode cancellation across cube-root cells",
                "next_single_lemma": "UniformShiftTwoCharacterModeCancellationAcrossCubeRootFactorCells",
            },
            "proof_dag": proof_dag(
                "TP",
                "ShiftTwoBuchstabFactorLiftAndDisjointFactorGraph",
                "ShiftTwoOperatorCrossGramAndModThreeJointNoGo",
                "SimultaneousPlusMinusTwoLocalSurvivalCreatesCancellation",
                "UniformShiftTwoCharacterModeCancellationAcrossCubeRootFactorCells",
                "TwinPrimeConjecture",
            ),
        },
    }
    tracks = ("riemann", "collatz", "goldbach", "twin_prime")
    total_failures = sum(
        root[key]["reproducible_computation"]["failure_count"] for key in tracks
    )
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
                    "audit_ref": f"#/near_alias_affine_language_residue_spectrum_audit/{key}",
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
            "TICKET-228 proves four exact partial results and resolves none "
            "of the four parent conjectures."
        ),
        "near_alias_affine_language_residue_spectrum_audit": root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit["near_alias_affine_language_residue_spectrum_audit"]
    write_json(
        ROOT
        / "data/open-problem/ticket228-near-alias-affine-language-residue-spectrum.json",
        audit,
    )
    destinations = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-228-finite-dilation-near-alias.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-228-branching-affine-language.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-228-moving-residue-spectrum.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-228-shift-two-residue-spectrum.json",
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
    machine = audit["near_alias_affine_language_residue_spectrum_audit"][
        "machine_audit"
    ]
    print(json.dumps(machine, indent=2))
    if machine["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
