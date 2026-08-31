from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any


sys.set_int_max_str_digits(0)

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket254_diagonal_weighted_reflection_thue import (
    fraction_record,
    is_prime,
    write_json,
)
from scripts.ticket258_variation_character_convergent import (
    certified_root_continued_fraction,
)
from scripts.ticket260_weighted_equidistribution_primerace_variablemod import (
    goldbach_q3_prime_race_audit,
    least_prime_above,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket262-limsup-finiteharmonic-mod8-thirdorder.v1"
GENERATED_AT = "2026-08-31T23:59:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "limsup_finiteharmonic_mod8_thirdorder_audit"

RIEMANN_REPLAY_COUNT = 64
RIEMANN_CRITICAL_COUNT = 12
COLLATZ_HARMONIC_CUTOFFS = (1, 2, 4, 8, 16)
COLLATZ_BLOCK_COUNT = 32
GOLDBACH_ABSTRACT_LEVELS = tuple(range(16))
TWIN_CONVERGENT_COUNT = 1024


@lru_cache(maxsize=1)
def riemann_exact_limsup_criterion_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    critical_rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for index in range(1, RIEMANN_REPLAY_COUNT + 1):
        energy = Fraction(index + 1, index)
        next_energy = Fraction(index + 2, index + 1)
        signed_jump = index * (energy - next_energy)
        lag = (index + 1) * next_energy - index * energy
        identity_rhs = next_energy - signed_jump
        verified = signed_jump == Fraction(1, index + 1) and lag == 1 and lag == identity_rhs
        failures += int(not verified)
        row = {
            "index_n": index,
            "energy_E_n": fraction_record(energy),
            "next_energy_E_n_plus_1": fraction_record(next_energy),
            "scaled_signed_jump_J_n": fraction_record(signed_jump),
            "lag_S_n": fraction_record(lag),
            "identity_rhs_E_n_plus_1_minus_J_n": fraction_record(identity_rhs),
            "row_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"tail:{index}:{energy}:{next_energy}:{signed_jump}:{lag}:{int(verified)}\n".encode("ascii")
        )
    for power in range(1, RIEMANN_CRITICAL_COUNT + 1):
        index = 4**power
        energy = Fraction(1)
        next_energy = Fraction(index - 1, index)
        signed_jump = index * (energy - next_energy)
        lag = (index + 1) * next_energy - index * energy
        verified = signed_jump == 1 and lag == -Fraction(1, index)
        failures += int(not verified)
        row = {
            "power_k": power,
            "index_n": index,
            "scaled_signed_jump_J_n": fraction_record(signed_jump),
            "lag_S_n": fraction_record(lag),
            "critical_equality_verified": verified,
        }
        critical_rows.append(row)
        transcript.update(
            f"critical:{power}:{index}:{signed_jump}:{lag}:{int(verified)}\n".encode("ascii")
        )
    theorem = (
        "Let (E_n) be a real sequence converging to L>0, define "
        "J_n=n(E_n-E_(n+1)) and S_n=(n+1)E_(n+1)-nE_n. Then, in the "
        "extended-real sense, liminf S_n=L-limsup J_n. Consequently there "
        "exist delta>0 and N such that S_n>=delta for every n>=N if and only "
        "if limsup J_n<L."
    )
    proof = (
        "The exact identity S_n=E_(n+1)-J_n holds for every n. Since "
        "E_(n+1) tends to L, subtracting a convergent sequence from J_n gives "
        "liminf S_n=L-limsup J_n. An eventual positive margin implies a "
        "positive lower limit and hence limsup J_n<L. Conversely, if the "
        "limsup is below L, choose half of the positive gap as delta and use "
        "the definitions of convergence and limsup. The reciprocal-tail rows "
        "replay the strict case; the sparse critical rows replay equality and "
        "negative lag. Neither family contains actual Guinand-Weil energies."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_reciprocal_tail_identity_rows": rows,
        "exact_critical_boundary_rows": critical_rows,
        "algorithm": "closed-form Fraction evaluation of the signed-jump identity and its strict/critical boundary families",
        "complexity": "O(N+K) exact rational operations; the iff theorem is symbolic and independent of replay length",
        "random_seed": None,
        "input_range": {
            "reciprocal_tail_index_min": 1,
            "reciprocal_tail_index_max": RIEMANN_REPLAY_COUNT,
            "critical_power_min": 1,
            "critical_power_max": RIEMANN_CRITICAL_COUNT,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "lag_margin_iff_scaled_signed_jump_limsup_below_limit_proved": True,
            "strict_boundary_replay_count": len(rows),
            "critical_boundary_replay_count": len(critical_rows),
            "actual_weil_packet_limsup_bound_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def collatz_finite_harmonic_cutoff_no_go_audit() -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    total_phase_rows = 0
    for cutoff in COLLATZ_HARMONIC_CUTOFFS:
        modulus = cutoff + 1
        phase_count = COLLATZ_BLOCK_COUNT * modulus
        previous_prime = 8 * modulus
        reciprocal_prime_sum = Fraction(0)
        cluster_zero_count = 0
        residue_counts = [0] * modulus
        samples: list[dict[str, Any]] = []
        for index in range(1, phase_count + 1):
            prime = least_prime_above(max(previous_prime, index**3, 8 * modulus))
            previous_prime = prime
            residue = (index - 1) % modulus
            ideal_point = Fraction(2 * residue + 1, 2 * modulus)
            exponent = (prime * (2 * residue + 1)) // (2 * modulus)
            point = Fraction(exponent, prime)
            error = ideal_point - point
            reciprocal_prime_sum += Fraction(1, prime)
            residue_counts[residue] += 1
            if point < Fraction(3, 4 * modulus):
                cluster_zero_count += 1
            verified = (
                is_prime(prime)
                and prime > index**3
                and prime > 8 * modulus
                and 1 <= exponent < prime
                and 0 <= error < Fraction(1, prime)
                and (point < Fraction(3, 4 * modulus)) == (residue == 0)
            )
            failures += int(not verified)
            if index <= 4 or index > phase_count - 4:
                samples.append(
                    {
                        "index_j": index,
                        "prime_modulus_q_j": prime,
                        "cluster_residue_r_j": residue,
                        "phase_exponent_d_j": exponent,
                        "normalized_point": fraction_record(point),
                        "ideal_midpoint": fraction_record(ideal_point),
                        "point_error": fraction_record(error),
                        "row_verified": verified,
                    }
                )
            transcript.update(
                f"{cutoff}:{index}:{prime}:{residue}:{exponent}:{point}:{ideal_point}:{error}:{int(verified)}\n".encode("ascii")
            )
        harmonic_rows: list[dict[str, Any]] = []
        for harmonic in range(1, cutoff + 1):
            complete_block_sum_zero = harmonic % modulus != 0 and all(
                count == COLLATZ_BLOCK_COUNT for count in residue_counts
            )
            normalized_chord_bound = (
                8 * harmonic * reciprocal_prime_sum / phase_count
            )
            verified = complete_block_sum_zero and normalized_chord_bound > 0
            failures += int(not verified)
            harmonic_rows.append(
                {
                    "harmonic_h": harmonic,
                    "ideal_complete_block_sum_zero": complete_block_sum_zero,
                    "normalized_chord_error_upper_bound": fraction_record(normalized_chord_bound),
                    "row_verified": verified,
                }
            )
        witness = Fraction(cluster_zero_count, phase_count) - Fraction(
            3, 4 * modulus
        )
        expected_witness = Fraction(1, 4 * modulus)
        case_verified = (
            cluster_zero_count == COLLATZ_BLOCK_COUNT
            and witness == expected_witness
            and all(count == COLLATZ_BLOCK_COUNT for count in residue_counts)
        )
        failures += int(not case_verified)
        total_phase_rows += phase_count
        cases.append(
            {
                "harmonic_cutoff_H": cutoff,
                "cluster_modulus_M": modulus,
                "phase_case_count": phase_count,
                "complete_block_count": COLLATZ_BLOCK_COUNT,
                "cluster_counts": residue_counts,
                "star_discrepancy_interval_endpoint": fraction_record(Fraction(3, 4 * modulus)),
                "star_discrepancy_lower_bound": fraction_record(witness),
                "reciprocal_prime_sum": fraction_record(reciprocal_prime_sum),
                "harmonic_rows": harmonic_rows,
                "sample_phase_rows": samples,
                "case_verified": case_verified,
            }
        )
    theorem = (
        "For every integer H>=1 there are strictly increasing odd primes q_j "
        "and integers 1<=d_j<q_j such that, for every nonzero integer h with "
        "|h|<=H, N^(-1) sum_(j<=N) exp(2*pi*i*h*d_j/q_j) tends to zero, while "
        "the star discrepancy of d_j/q_j has liminf at least 1/[4(H+1)]. "
        "Thus no fixed finite Weyl-harmonic cutoff implies angular "
        "equidistribution for growing prime moduli."
    )
    proof = (
        "Put M=H+1 and cycle the ideal midpoints y_j=(2r_j+1)/(2M), "
        "r_j=(j-1) mod M. Choose q_j as the least prime above "
        "max(q_(j-1),j^3,8M), and d_j=floor(q_j*y_j). For 1<=|h|<=H each "
        "complete ideal M-block is a shifted geometric sum and equals zero. "
        "The chord error is below 8|h|/q_j and sum 1/q_j converges, so every "
        "listed normalized harmonic tends to zero. The interval "
        "[0,3/(4M)) contains exactly the r_j=0 cluster; its empirical mass "
        "tends to 1/M, giving discrepancy at least 1/(4M). The construction "
        "is noncanonical and does not decide Fermat-quotient angles."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_finite_harmonic_cutoff_cases": cases,
        "algorithm": "deterministic growing-prime midpoint clusters with symbolic root-of-unity block cancellation and exact Fraction error envelopes",
        "complexity": "O(sum_H H^2) deterministic prime searches and exact rational checks for the replay; the construction is proved for every fixed H",
        "random_seed": None,
        "input_range": {
            "harmonic_cutoffs": list(COLLATZ_HARMONIC_CUTOFFS),
            "complete_blocks_per_cutoff": COLLATZ_BLOCK_COUNT,
            "total_phase_case_count": total_phase_rows,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "arbitrary_fixed_finite_harmonic_cutoff_insufficient_proved": True,
            "largest_replayed_harmonic_cutoff": max(COLLATZ_HARMONIC_CUTOFFS),
            "total_replayed_phase_case_count": total_phase_rows,
            "canonical_all_nonzero_harmonic_cancellation_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def goldbach_q3_mod8_tie_obstruction_audit() -> dict[str, Any]:
    prior = goldbach_q3_prime_race_audit()
    rows: list[dict[str, Any]] = []
    abstract_rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for source in prior["exact_q3_prime_race_certificate_rows"]:
        level = source["level_l"]
        scale = int(source["scale_A_equals_3_power_6l_plus_2"])
        prefix = source["forced_prefix_length_T"]
        counts = source["actual_residue_counts"]
        minus_count = counts[2]
        tie_forced_count = (prefix - 1) // 2
        closed_form_tie_count = 3 ** (6 * level + 3) + 1
        verified = (
            tie_forced_count == 3 * scale + 1 == closed_form_tie_count
            and tie_forced_count % 8 == 4
            and counts == source["independent_segmented_residue_counts"]
            and minus_count % 8 != 4
            and source["mod_3_prime_race_difference_N1_minus_N2"] != 0
        )
        failures += int(not verified)
        row = {
            "level_l": level,
            "scale_A": str(scale),
            "special_prime_prefix_length_T_l": prefix,
            "exact_nth_prime_endpoint": source["exact_nth_prime_endpoint"],
            "actual_residue_counts_mod_3": counts,
            "minus_one_residue_count_N_2": minus_count,
            "minus_one_residue_count_mod_8": minus_count % 8,
            "tie_would_force_each_nonzero_count": tie_forced_count,
            "tie_forced_count_closed_form": str(closed_form_tie_count),
            "tie_forced_count_mod_8": tie_forced_count % 8,
            "tie_excluded_by_mod_8_contrapositive": minus_count % 8 != 4,
            "independent_residue_algorithms_agree": counts
            == source["independent_segmented_residue_counts"],
            "row_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"actual:{level}:{scale}:{prefix}:{source['exact_nth_prime_endpoint']}:"
            f"{','.join(map(str, counts))}:{minus_count}:{minus_count % 8}:"
            f"{tie_forced_count}:{int(verified)}\n".encode("ascii")
        )

    for level in GOLDBACH_ABSTRACT_LEVELS:
        scale = 3 ** (6 * level + 2)
        prefix = 6 * scale + 3
        tie_count = (prefix - 1) // 2
        product_plus_non_tie_minus = tie_count + 2
        product_plus_non_tie_plus = tie_count - 2
        mod8_not_sufficient_minus = tie_count + 8
        mod8_not_sufficient_plus = tie_count - 8
        product_plus_non_tie_verified = (
            product_plus_non_tie_minus % 2 == 0
            and product_plus_non_tie_minus % 8 == 6
            and product_plus_non_tie_minus != product_plus_non_tie_plus
            and product_plus_non_tie_minus + product_plus_non_tie_plus
            == prefix - 1
        )
        mod8_not_sufficient_verified = (
            mod8_not_sufficient_minus % 8 == 4
            and mod8_not_sufficient_minus != mod8_not_sufficient_plus
            and mod8_not_sufficient_minus + mod8_not_sufficient_plus
            == prefix - 1
            and mod8_not_sufficient_plus >= 0
        )
        verified = (
            tie_count == 3 ** (6 * level + 3) + 1
            and tie_count % 8 == 4
            and product_plus_non_tie_verified
            and mod8_not_sufficient_verified
        )
        failures += int(not verified)
        row = {
            "level_l": level,
            "special_prefix_length_T_l": str(prefix),
            "tie_count": str(tie_count),
            "tie_count_mod_8": tie_count % 8,
            "product_plus_one_but_non_tie_counts": {
                "N_1": str(product_plus_non_tie_plus),
                "N_2": str(product_plus_non_tie_minus),
                "N_2_mod_8": product_plus_non_tie_minus % 8,
                "product_mod_3": 1,
                "verified": product_plus_non_tie_verified,
            },
            "N_2_congruent_four_but_non_tie_counts": {
                "N_1": str(mod8_not_sufficient_plus),
                "N_2": str(mod8_not_sufficient_minus),
                "N_2_mod_8": mod8_not_sufficient_minus % 8,
                "verified": mod8_not_sufficient_verified,
            },
            "row_verified": verified,
        }
        abstract_rows.append(row)
        transcript.update(
            f"abstract:{level}:{prefix}:{tie_count}:"
            f"{product_plus_non_tie_plus}:{product_plus_non_tie_minus}:"
            f"{mod8_not_sufficient_plus}:{mod8_not_sufficient_minus}:"
            f"{int(verified)}\n".encode("ascii")
        )
    theorem = (
        "For every l>=0 put T_l=6*3^(6l+2)+3. If the mod-3 prime race "
        "among the first T_l primes ties after omitting the prime 3, then "
        "the number N_2 of primes congruent to -1 modulo 3 satisfies "
        "N_2=3^(6l+3)+1, hence N_2 is congruent to 4 modulo 8 and has "
        "2-adic valuation exactly two. Therefore N_2 not congruent to 4 "
        "modulo 8 is an exact certificate excluding the tie. The congruence "
        "is necessary, not sufficient."
    )
    proof = (
        "A tie forces N_1=N_2=(T_l-1)/2=3^(6l+3)+1. Since 6l+3 is odd, "
        "3^(6l+3) is congruent to 3 modulo 8, proving N_2 congruent to 4 "
        "modulo 8; the same congruence gives exact 2-adic valuation two. "
        "The contrapositive excludes a tie whenever the actual N_2 has a "
        "different residue. To audit sharpness, replace the two tied counts "
        "m,m by m-2,m+2: the product sign remains +1 but the race is not a "
        "tie, so the earlier product-minus-one certificate was not necessary. "
        "Replacing them by m-8,m+8 preserves N_2 congruent to 4 modulo 8 "
        "but is still not a tie, so the new congruence is not sufficient."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_q3_mod8_certificate_rows": rows,
        "exact_sharpness_countermodel_rows": abstract_rows,
        "algorithm": "exact integer congruence arithmetic over independently reproduced mod-3 prime-prefix counts, plus closed-form count-vector countermodels",
        "complexity": "O(1) congruence work per level after the TICKET-260 exact residue certificates; the symbolic implications hold for every l",
        "random_seed": None,
        "input_range": {
            "actual_certificate_level_min": rows[0]["level_l"],
            "actual_certificate_level_max": rows[-1]["level_l"],
            "abstract_replay_level_min": GOLDBACH_ABSTRACT_LEVELS[0],
            "abstract_replay_level_max": GOLDBACH_ABSTRACT_LEVELS[-1],
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "tie_forces_minus_count_four_mod_8_proved": True,
            "tie_forces_exact_two_adic_valuation_two_proved": True,
            "actual_mod8_non_tie_certificate_count": len(rows),
            "product_minus_one_is_necessary_for_non_tie_refuted": True,
            "minus_count_four_mod_8_is_sufficient_for_tie_refuted": True,
            "all_special_minus_counts_not_four_mod_8_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def twin_bidirectional_third_order_audit() -> dict[str, Any]:
    _, source_rows, lower, upper = certified_root_continued_fraction(
        TWIN_CONVERGENT_COUNT
    )
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    denominator_third_passes: list[dict[str, Any]] = []
    numerator_third_nontrivial_passes: list[dict[str, Any]] = []
    joint_third_passes: list[dict[str, Any]] = []
    previous_denominator = 0
    for source in source_rows:
        index = source["term_index"]
        numerator = int(source["convergent_numerator"])
        denominator = int(source["convergent_denominator"])
        coefficient = int(source["B_1_at_convergent"])
        monotone = denominator >= previous_denominator
        previous_denominator = denominator
        sign_rows: list[dict[str, Any]] = []
        expansion_verified = True
        for epsilon in (-1, 1):
            denominator_cubed = denominator**3
            denominator_third_residue = (
                pow(numerator, 17, denominator_cubed)
                + 17
                * pow(numerator, 16, denominator_cubed)
                * denominator
                + 272
                * pow(numerator, 15, denominator_cubed)
                * denominator**2
                - epsilon
            ) % denominator_cubed
            denominator_direct_residue = (
                coefficient - epsilon
            ) % denominator_cubed
            denominator_third_pass = denominator_third_residue == 0

            numerator_modulus = abs(numerator)
            numerator_defined = numerator_modulus > 0
            if numerator_defined:
                numerator_cubed = numerator_modulus**3
                numerator_third_residue = (
                    256 * pow(denominator, 17, numerator_cubed)
                    + 4352
                    * (numerator % numerator_cubed)
                    * pow(denominator, 16, numerator_cubed)
                    + 17408
                    * pow(numerator, 2, numerator_cubed)
                    * pow(denominator, 15, numerator_cubed)
                    - epsilon
                ) % numerator_cubed
                numerator_direct_residue = (
                    coefficient - epsilon
                ) % numerator_cubed
                numerator_third_pass = numerator_third_residue == 0
            else:
                numerator_third_residue = None
                numerator_direct_residue = None
                numerator_third_pass = False
            joint_third_pass = denominator_third_pass and numerator_third_pass
            witness = {
                "term_index": index,
                "epsilon": epsilon,
                "numerator": str(numerator),
                "denominator": str(denominator),
            }
            if denominator >= 2 and denominator_third_pass:
                denominator_third_passes.append(witness)
            if numerator_modulus >= 2 and numerator_third_pass:
                numerator_third_nontrivial_passes.append(witness)
            if denominator >= 2 and numerator_defined and joint_third_pass:
                joint_third_passes.append(witness)
            expansion_verified = expansion_verified and (
                denominator_third_residue == denominator_direct_residue
                and (
                    not numerator_defined
                    or numerator_third_residue == numerator_direct_residue
                )
            )
            sign_rows.append(
                {
                    "epsilon": epsilon,
                    "numerator_modulus_defined": numerator_defined,
                    "denominator_third_residue_mod_v_cubed": str(
                        denominator_third_residue
                    ),
                    "denominator_direct_B1_residue_mod_v_cubed": str(
                        denominator_direct_residue
                    ),
                    "numerator_third_residue_mod_u_cubed": None
                    if numerator_third_residue is None
                    else str(numerator_third_residue),
                    "numerator_direct_B1_residue_mod_u_cubed": None
                    if numerator_direct_residue is None
                    else str(numerator_direct_residue),
                    "denominator_third_pass": denominator_third_pass,
                    "numerator_third_pass": numerator_third_pass,
                    "joint_third_pass": joint_third_pass,
                }
            )
        direct_unit_hit = abs(coefficient) == 1
        verified = monotone and expansion_verified and not direct_unit_hit
        failures += int(not verified)
        coefficient_digest = hashlib.sha256(
            str(coefficient).encode("ascii")
        ).hexdigest()
        row = {
            "term_index": index,
            "partial_quotient": source["partial_quotient"],
            "convergent_numerator": str(numerator),
            "convergent_denominator": str(denominator),
            "denominator_digit_count": len(str(denominator)),
            "root_side": source["root_side"],
            "B_1_value_sha256": coefficient_digest,
            "sign_tests": sign_rows,
            "both_third_order_expansions_match_direct_B1": expansion_verified,
            "direct_unit_coefficient_hit": direct_unit_hit,
            "row_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"{index}:{source['partial_quotient']}:{numerator}:{denominator}:"
            f"{coefficient_digest}:"
            f"{sign_rows[0]['denominator_third_residue_mod_v_cubed']}:"
            f"{sign_rows[0]['numerator_third_residue_mod_u_cubed']}:"
            f"{sign_rows[1]['denominator_third_residue_mod_v_cubed']}:"
            f"{sign_rows[1]['numerator_third_residue_mod_u_cubed']}:"
            f"{int(expansion_verified)}:{int(direct_unit_hit)}\n".encode("ascii")
        )
    failures += len(denominator_third_passes)
    failures += len(numerator_third_nontrivial_passes)
    failures += len(joint_third_passes)
    theorem = (
        "Let B_1(u,v) be the degree-17 coefficient form from TICKET-257. "
        "For integers u,v with uv nonzero and epsilon in {-1,1}, "
        "B_1(u,v)=epsilon forces u^17+17u^16v+272u^15v^2=epsilon "
        "modulo v^3 and 256v^17+4352uv^16+17408u^2v^15=epsilon "
        "modulo u^3. Among the first 1024 certified continued-fraction "
        "convergents of the unique root, both signs fail the joint "
        "third-order condition."
    )
    proof = (
        "In the binomial expansion of B_1, the terms of v-degree zero, one, "
        "and two have coefficients 1, 17, and C(17,2)*2=272; every later "
        "term is divisible by v^3. At the other end, the terms of u-degree "
        "zero, one, and two have coefficients 256, 4352, and "
        "C(17,15)*2^7=17408; every earlier term is divisible by u^3. "
        "Reduction proves the two necessary congruences. Both truncated "
        "residues are compared independently with the full exact B_1 value "
        "for both signs on each certified convergent. The finite prefix "
        "reaches a 519-digit denominator but cannot exclude later convergents."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_bidirectional_third_order_convergent_rows": rows,
        "denominator_third_order_nontrivial_passes": denominator_third_passes,
        "numerator_third_order_nontrivial_passes": numerator_third_nontrivial_passes,
        "joint_third_order_passes": joint_third_passes,
        "final_exact_root_bracket": {
            "lower": fraction_record(lower),
            "upper": fraction_record(upper),
        },
        "algorithm": "certified rational continued fractions, modular exponentiation modulo v^3 and u^3, and independent full-form residue comparisons",
        "complexity": "O(K) certified convergents and O(K log 17) modular multiplications on O(log v_K)-bit integers",
        "random_seed": None,
        "input_range": {
            "certified_convergent_count": TWIN_CONVERGENT_COUNT,
            "epsilon_values": [-1, 1],
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "bidirectional_third_order_congruence_necessary_proved": True,
            "certified_convergent_count": len(rows),
            "maximum_denominator": rows[-1]["convergent_denominator"],
            "maximum_denominator_digit_count": rows[-1]["denominator_digit_count"],
            "denominator_third_order_nontrivial_pass_count": len(
                denominator_third_passes
            ),
            "numerator_third_order_nontrivial_pass_count": len(
                numerator_third_nontrivial_passes
            ),
            "joint_third_order_pass_count": len(joint_third_passes),
            "all_convergents_excluded": False,
            "exponent_seventeen_excluded": False,
            "twin_prime_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def proof_dag(
    code: str,
    prior_name: str,
    theorem_name: str,
    rejected_name: str,
    open_name: str,
) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T261", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T262", "label": theorem_name, "status": "proved"},
        {
            "id": f"{code}-CERT262",
            "label": f"{theorem_name}ExactReplay",
            "status": "computed_finite",
        },
        {"id": f"{code}-REJECT262", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN262", "label": open_name, "status": "open"},
    ]
    return {
        "nodes": nodes,
        "edges": [
            [f"{code}-T261", f"{code}-T262"],
            [f"{code}-T262", f"{code}-CERT262"],
            [f"{code}-T262", f"{code}-REJECT262"],
            [f"{code}-T262", f"{code}-OPEN262"],
        ],
        "resolution_path": [f"{code}-T261", f"{code}-T262", f"{code}-OPEN262"],
        "acyclic": True,
    }


def section(
    problem_id: str,
    code: str,
    theorem_name: str,
    classification: str,
    computation: dict[str, Any],
    discarded: str,
    parked: list[str],
    retained: str,
    next_lemma: str,
    prior_name: str,
    rejected_name: str,
    logical_limit: str,
    claim_boundary: str,
    finite_boundary: str,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{code}-TICKET-262",
        "theorem_name": theorem_name,
        "declared_proposition": computation["theorem"],
        "mathematical_argument": computation["proof"],
        "result_classification": classification,
        "problem_status": STATUS,
        "reproducible_computation": computation,
        "finite_computation_boundary": finite_boundary,
        "logical_limit": logical_limit,
        "route_decision": {
            "discard": discarded,
            "parked": parked,
            "retain": retained,
            "next_single_lemma": next_lemma,
        },
        "stagnation_count": 0,
        "proof_dag": proof_dag(
            code, prior_name, theorem_name, rejected_name, next_lemma
        ),
        "claim_boundary": claim_boundary,
    }


@lru_cache(maxsize=1)
def build_audit() -> dict[str, Any]:
    riemann = riemann_exact_limsup_criterion_audit()
    collatz = collatz_finite_harmonic_cutoff_no_go_audit()
    goldbach = goldbach_q3_mod8_tie_obstruction_audit()
    twin = twin_bidirectional_third_order_audit()
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "PacketLagMarginIffScaledSignedJumpLimsupBelowLimit",
            "partial_theorem",
            riemann,
            "treating any stronger summability hypothesis as the minimal abstract target for eventual packet-lag positivity",
            [
                "an arithmetic proof of the strict scaled signed-jump limsup bound for actual Guinand-Weil packet energies"
            ],
            "the exact lag identity and its necessary-and-sufficient abstract limsup threshold",
            "ActualWeilPacketScaledDownwardJumpLimsupBelowLimit",
            "SummableScaledVariationNecessityNoGo",
            "SummableScaledVariationIsTheMinimalAbstractLagCriterion",
            "The abstract threshold is exact, but no strict limsup estimate is proved for the actual Guinand-Weil packet energies.",
            "No RH proof or disproof; this is an exact abstract equivalence that isolates the missing arithmetic inequality.",
            f"{len(riemann['exact_reciprocal_tail_identity_rows'])} strict-boundary and {len(riemann['exact_critical_boundary_rows'])} critical-boundary Fraction rows are replayed; none is an actual Weil packet.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "EveryFixedFiniteWeylCutoffAngularDiscrepancyNoGo",
            "exact_no_go",
            collatz,
            "deducing angular discrepancy decay from cancellation of any one fixed finite set of growing-modulus Weyl harmonics",
            [
                "all-nonzero-harmonic Weyl cancellation for the canonical fixed-base Fermat-quotient exponents"
            ],
            "the all-H finite-cutoff counterfamily and the canonical all-harmonic target",
            "CanonicalFermatQuotientWeylSumsVanishForEveryNonzeroH",
            "FirstHarmonicCancellationAngularDiscrepancyNoGo",
            "SomeFixedFiniteWeylCutoffImpliesAngularDiscrepancyZero",
            "Every fixed finite cutoff is insufficient, but no all-harmonic Weyl-sum theorem is proved for the canonical Fermat-quotient exponents.",
            "No Collatz proof or counterexample; every finite-harmonic shortcut to the canonical angular-discrepancy target is eliminated.",
            f"The theorem holds for every fixed H; exact rational replays use H={list(COLLATZ_HARMONIC_CUTOFFS)} and {collatz['aggregate']['total_replayed_phase_case_count']} phase cases only.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "Q3TieForcesMinusCountFourModuloEight",
            "partial_theorem",
            goldbach,
            "treating the TICKET-261 product-minus-one certificate as a necessary characterization of q=3 special-prefix non-ties",
            [
                "an all-level arithmetic proof that the actual special q=3 minus-one count never equals four modulo eight"
            ],
            "the weaker exact modulo-eight necessary condition, actual finite certificates, and two sharpness count models",
            "Q3SpecialMinusOneResidueCountNeverFourModuloEight",
            "Q3PrimePrefixProductParityObstruction",
            "ProductMinusOneIsNecessaryForQ3SpecialNonTie",
            "The tie obstruction is necessary but not sufficient, and no theorem excludes residue four modulo eight at every actual special prime prefix.",
            "No strong Goldbach proof or counterexample; three actual finite levels are excluded by the weaker exact congruence.",
            f"{len(goldbach['exact_q3_mod8_certificate_rows'])} actual levels are certified; the implication and countermodels are symbolic for all levels.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "BidirectionalThirdOrderCongruenceAnd1024ConvergentCertificate",
            "partial_theorem",
            twin,
            "treating the bidirectional second-order congruence pair as the sharpest available finite-jet necessary condition",
            [
                "global exclusion of simultaneous third-order numerator and denominator congruences on every later unique-root convergent"
            ],
            "the exact modulo-v-cubed and modulo-u-cubed necessary pair and the 1024-convergent two-sign certificate",
            "NoUniqueRootConvergentSatisfiesBothThirdOrderCongruences",
            "BidirectionalSecondOrderCongruenceAnd1024ConvergentCertificate",
            "SecondOrderCongruencePairIsTheSharpestAvailableFiniteJetCondition",
            "The third-order sieve eliminates 1024 certified convergents, but infinitely many later convergents are not controlled.",
            "No twin-prime proof or counterexample; the remaining exponent-17 branch gains the next exact bidirectional jet condition.",
            f"Both signs are tested on the first {TWIN_CONVERGENT_COUNT} certified convergents; no finite prefix excludes every convergent.",
        ),
    }
    total_failures = sum(
        item["reproducible_computation"]["failure_count"]
        for item in sections.values()
    )
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureLimsupFiniteHarmonicMod8ThirdOrderAudit",
            "summary": (
                "TICKET-262 proves three partial theorems and one exact no-go: "
                "RH-style lag positivity has an exact abstract limsup threshold, "
                "no fixed finite Weyl cutoff forces Collatz angular discrepancy, "
                "q=3 Goldbach ties force a modulo-eight count condition, and the "
                "Twin degree-17 branch obeys bidirectional third-order congruences; "
                "all four parent conjectures remain open."
            ),
            **sections,
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 3,
                "exact_no_go_count": 1,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "collatz",
                "stagnated_problem_count": 0,
                "riemann_strict_boundary_case_count": len(
                    riemann["exact_reciprocal_tail_identity_rows"]
                ),
                "riemann_critical_boundary_case_count": len(
                    riemann["exact_critical_boundary_rows"]
                ),
                "collatz_harmonic_cutoff_replay_count": len(
                    collatz["exact_finite_harmonic_cutoff_cases"]
                ),
                "collatz_total_phase_case_count": collatz["aggregate"][
                    "total_replayed_phase_case_count"
                ],
                "goldbach_actual_mod8_certificate_count": len(
                    goldbach["exact_q3_mod8_certificate_rows"]
                ),
                "goldbach_sharpness_countermodel_count": len(
                    goldbach["exact_sharpness_countermodel_rows"]
                ),
                "twin_convergent_count": len(
                    twin["exact_bidirectional_third_order_convergent_rows"]
                ),
                "twin_joint_third_order_pass_count": twin["aggregate"][
                    "joint_third_order_pass_count"
                ],
                "twin_maximum_denominator_digit_count": twin["aggregate"][
                    "maximum_denominator_digit_count"
                ],
                "total_failure_count": total_failures,
            },
        },
        "attempts": [
            {
                "problem_id": item["problem_id"],
                "ticket_id": item["ticket_id"],
                "declared_proposition": item["declared_proposition"],
                "new_result": item["theorem_name"],
                "result_classification": item["result_classification"],
                "status": STATUS,
                "bounded_result": {
                    "audit_ref": f"#/{AUDIT_KEY}/{key}",
                    "failure_count": item["reproducible_computation"][
                        "failure_count"
                    ],
                },
                "discarded_route": item["route_decision"]["discard"],
                "parked_routes": item["route_decision"]["parked"],
                "remaining_gap": item["logical_limit"],
                "stagnation_count": item["stagnation_count"],
                "candidate_theorem": item["route_decision"][
                    "next_single_lemma"
                ],
            }
            for key, item in sections.items()
        ],
    }


def build_research_state(audit: dict[str, Any]) -> dict[str, Any]:
    state_path = ROOT / "data/open-problem/four-problem-research-state.json"
    previous = json.loads(state_path.read_text(encoding="utf-8"))
    root = audit[AUDIT_KEY]
    problems: dict[str, Any] = {}
    for key in ("riemann", "collatz", "goldbach", "twin_prime"):
        item = root[key]
        old = previous["problems"][key]
        established = list(old.get("established_results", []))
        if item["theorem_name"] not in established:
            established.append(item["theorem_name"])
        retired = list(old.get("retired_routes", []))
        if item["route_decision"]["discard"] not in retired:
            retired.append(item["route_decision"]["discard"])
        parked = list(old.get("parked_routes", []))
        for route in item["route_decision"]["parked"]:
            if route not in parked:
                parked.append(route)
        problems[key] = {
            "problem_status": STATUS,
            "current_target": item["theorem_name"],
            "established_results": established,
            "retired_routes": retired,
            "parked_routes": parked,
            "remaining_gap": item["logical_limit"],
            "next_single_lemma": item["route_decision"]["next_single_lemma"],
            "stagnation_count": item["stagnation_count"],
            "unresolved_dependencies": [
                node["label"]
                for node in item["proof_dag"]["nodes"]
                if node["status"] in {"assumption", "heuristic", "open"}
            ],
            "finite_computation_boundary": item["finite_computation_boundary"],
            "proof_dag_status": "acyclic_with_one_open_frontier",
            "validation_status": {
                "generator_failure_count": item["reproducible_computation"][
                    "failure_count"
                ],
                "focused_tests_required": True,
                "remote_ci_status": "tracked_by_commit_workflow",
            },
        }
    return {
        "schema": "primeproject.four-problem-research-state.v1",
        "ticket": 262,
        "parent_ticket": 261,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "collatz",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(
        ROOT
        / "data/open-problem/ticket262-limsup-finiteharmonic-mod8-thirdorder.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-262-limsup-criterion.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-262-finite-harmonic-cutoff-no-go.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-262-mod8-tie-obstruction.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-262-bidirectional-third-order.json",
    }
    for key, path in paths.items():
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": STATUS,
                **root[key],
            },
        )
    write_json(
        ROOT / "data/open-problem/four-problem-research-state.json",
        build_research_state(audit),
    )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    machine = audit[AUDIT_KEY]["machine_audit"]
    print(json.dumps(machine, indent=2))
    return 0 if machine["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
