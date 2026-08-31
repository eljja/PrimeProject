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
from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket258_variation_character_convergent import (
    certified_root_continued_fraction,
)
from scripts.ticket260_weighted_equidistribution_primerace_variablemod import (
    goldbach_q3_prime_race_audit,
    least_prime_above,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket261-sharpness-weyl-ties-dualcongruence.v1"
GENERATED_AT = "2026-08-31T23:55:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "sharpness_weyl_ties_dualcongruence_audit"

RIEMANN_REPLAY_COUNT = 128
COLLATZ_COUNTERMODEL_COUNT = 128
COLLATZ_CANONICAL_PREFIXES = tuple(2**power for power in range(3, 15))
GOLDBACH_ABSTRACT_LEVELS = tuple(range(16))
TWIN_CONVERGENT_COUNT = 1024


def reciprocal_tail_energy(index: int, limit: Fraction = Fraction(1), scale: Fraction = Fraction(1)) -> Fraction:
    if index < 1:
        raise ValueError("packet index must be positive")
    if limit <= 0 or scale <= 0:
        raise ValueError("limit and scale must be positive")
    return limit + scale / index


@lru_cache(maxsize=1)
def riemann_summability_sharpness_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    partial_weighted_variation = Fraction(0)
    failures = 0
    for index in range(1, RIEMANN_REPLAY_COUNT + 1):
        energy = reciprocal_tail_energy(index)
        next_energy = reciprocal_tail_energy(index + 1)
        drop = energy - next_energy
        weighted_drop = index * drop
        partial_weighted_variation += weighted_drop
        lag = (index + 1) * next_energy - index * energy
        expected_partial = sum(Fraction(1, n + 1) for n in range(1, index + 1))
        verified = (
            drop == Fraction(1, index * (index + 1))
            and weighted_drop == Fraction(1, index + 1)
            and lag == 1
            and partial_weighted_variation == expected_partial
        )
        failures += int(not verified)
        row = {
            "index_n": index,
            "energy_E_n": fraction_record(energy),
            "downward_drop_d_n": fraction_record(drop),
            "scaled_drop_n_d_n": fraction_record(weighted_drop),
            "lag_S_n": fraction_record(lag),
            "partial_scaled_downward_variation": fraction_record(partial_weighted_variation),
            "row_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"{index}:{energy}:{drop}:{weighted_drop}:{lag}:"
            f"{partial_weighted_variation}:{int(verified)}\n".encode("ascii")
        )
    theorem = (
        "For arbitrary real L,c>0, define E_n=L+c/n for n>=1, "
        "d_n=(E_n-E_(n+1))_+, and S_n=(n+1)E_(n+1)-nE_n. Then "
        "E_n tends to L, every S_n equals L>0, but sum_(n>=1) n d_n "
        "diverges. Therefore the TICKET-260 summable scaled-downward-variation "
        "hypothesis is sufficient but not necessary for eventual lag positivity."
    )
    proof = (
        "Direct subtraction gives d_n=c/[n(n+1)], hence n d_n=c/(n+1). "
        "The harmonic series diverges, so the nonnegative scaled-variation "
        "series diverges. On the other hand nE_n=nL+c and "
        "(n+1)E_(n+1)=(n+1)L+c, so S_n=L for every n. The exact replay "
        "uses L=c=1. This refutes necessity of the abstract sufficient "
        "condition; it computes no actual Guinand-Weil packet coefficient."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_reciprocal_tail_rows": rows,
        "algorithm": "closed-form Fraction replay of E_n=1+1/n",
        "complexity": "O(N) exact rational operations for N replay rows; the counterfamily is proved for every n",
        "random_seed": None,
        "input_range": {"index_n_min": 1, "index_n_max": RIEMANN_REPLAY_COUNT},
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "eventual_lag_positivity_proved": True,
            "scaled_downward_variation_diverges_proved": True,
            "summable_scaled_variation_is_necessary_refuted": True,
            "actual_weil_packet_used": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


def fermat_quotient_mod_prime(base: int, prime: int) -> int:
    residue = pow(base, prime - 1, prime * prime)
    return ((residue - 1) // prime) % prime


def exact_star_discrepancy(points: list[tuple[Fraction, int, int, int, int]]) -> tuple[Fraction, dict[str, Any]]:
    if not points:
        raise ValueError("at least one point is required")
    ordered = sorted(points, key=lambda row: (row[0], row[1]))
    count = len(ordered)
    best = Fraction(-1)
    witness: dict[str, Any] = {}
    for rank, (point, prime, exponent, quotient_two, quotient_three) in enumerate(ordered, 1):
        candidates = (
            ("right", Fraction(rank, count) - point),
            ("left", point - Fraction(rank - 1, count)),
        )
        for side, gap in candidates:
            if gap > best:
                best = gap
                witness = {
                    "rank": rank,
                    "side": side,
                    "point": fraction_record(point),
                    "prime_q": prime,
                    "canonical_exponent_D_q": exponent,
                    "fermat_quotient_F_q_2": quotient_two,
                    "fermat_quotient_F_q_3": quotient_three,
                }
    return best, witness


@lru_cache(maxsize=1)
def collatz_first_harmonic_no_go_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    previous_prime = 13
    deviation_sum = Fraction(0)
    interval_count = 0
    for index in range(1, COLLATZ_COUNTERMODEL_COUNT + 1):
        prime = least_prime_above(max(previous_prime, index**3, 13))
        previous_prime = prime
        if index % 2:
            exponent = prime // 4
            ideal_point = Fraction(1, 4)
            ideal_phase = "i"
        else:
            exponent = (3 * prime) // 4
            ideal_point = Fraction(3, 4)
            ideal_phase = "-i"
        point = Fraction(exponent, prime)
        point_error = abs(point - ideal_point)
        chord_bound = 8 * point_error
        deviation_sum += chord_bound
        if point < Fraction(1, 3):
            interval_count += 1
        witness_discrepancy = Fraction(interval_count, index) - Fraction(1, 3)
        normalized_first_harmonic_bound = (
            Fraction(index % 2, index) + deviation_sum / index
        )
        verified = (
            is_prime(prime)
            and prime > index**3
            and 1 <= exponent < prime
            and point_error <= Fraction(1, prime)
            and chord_bound <= Fraction(8, prime)
            and interval_count == (index + 1) // 2
            and witness_discrepancy > 0
        )
        failures += int(not verified)
        row = {
            "index_j": index,
            "prime_modulus_q_j": prime,
            "phase_exponent_d_j": exponent,
            "normalized_point_d_j_over_q_j": fraction_record(point),
            "ideal_point": fraction_record(ideal_point),
            "ideal_phase": ideal_phase,
            "point_error": fraction_record(point_error),
            "chord_error_upper_bound": fraction_record(chord_bound),
            "normalized_first_harmonic_upper_bound": fraction_record(normalized_first_harmonic_bound),
            "count_in_zero_to_one_third": interval_count,
            "star_discrepancy_interval_witness": fraction_record(witness_discrepancy),
            "row_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"model:{index}:{prime}:{exponent}:{point}:{ideal_point}:"
            f"{point_error}:{chord_bound}:{interval_count}:{witness_discrepancy}:"
            f"{int(verified)}\n".encode("ascii")
        )

    maximum_prefix = max(COLLATZ_CANONICAL_PREFIXES)
    canonical_points: list[tuple[Fraction, int, int, int, int]] = []
    prime = 7
    while len(canonical_points) < maximum_prefix:
        if is_prime(prime):
            quotient_two = fermat_quotient_mod_prime(2, prime)
            quotient_three = fermat_quotient_mod_prime(3, prime)
            exponent = (5 * quotient_two - 3 * quotient_three) % prime
            canonical_points.append(
                (Fraction(exponent, prime), prime, exponent, quotient_two, quotient_three)
            )
        prime += 2
    canonical_rows: list[dict[str, Any]] = []
    previous_discrepancy: Fraction | None = None
    first_increase_prefix: int | None = None
    for prefix in COLLATZ_CANONICAL_PREFIXES:
        discrepancy, witness = exact_star_discrepancy(canonical_points[:prefix])
        increased = previous_discrepancy is not None and discrepancy > previous_discrepancy
        if increased and first_increase_prefix is None:
            first_increase_prefix = prefix
        row = {
            "canonical_prime_prefix_count": prefix,
            "largest_prime_q": canonical_points[prefix - 1][1],
            "exact_star_discrepancy": fraction_record(discrepancy),
            "increased_from_previous_dyadic_prefix": increased,
            "extremal_witness": witness,
        }
        canonical_rows.append(row)
        transcript.update(
            f"canonical:{prefix}:{canonical_points[prefix - 1][1]}:"
            f"{discrepancy}:{int(increased)}:{witness['rank']}:"
            f"{witness['side']}:{witness['prime_q']}:{witness['canonical_exponent_D_q']}\n".encode("ascii")
        )
        previous_discrepancy = discrepancy
    failures += int(first_increase_prefix != 4096)
    theorem = (
        "There exist strictly increasing odd prime moduli q_j and integers "
        "1<=d_j<q_j such that N^(-1)sum_(j<=N) exp(2*pi*i*d_j/q_j) "
        "tends to zero, while the star discrepancy of d_j/q_j has liminf at "
        "least 1/6. Hence cancellation of the first Weyl harmonic alone does "
        "not imply angular equidistribution on growing prime moduli."
    )
    proof = (
        "Take q_j to be the least prime above max(q_(j-1),j^3,13). For odd j "
        "put d_j=floor(q_j/4), and for even j put d_j=floor(3q_j/4). The "
        "points lie within 1/q_j of 1/4 and 3/4. Their ideal first-harmonic "
        "phases i and -i cancel in pairs, while the total chord error is "
        "bounded by 8 sum 1/q_j<8 sum 1/j^3<16; division by N gives zero. "
        "Exactly ceil(N/2) points lie in [0,1/3), so the associated discrepancy "
        "tends to 1/2-1/3=1/6. The separate canonical table uses exact Fermat "
        "quotients and exact rational star discrepancy; it is finite evidence "
        "only and its first dyadic increase occurs at prefix 4096."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_first_harmonic_countermodel_rows": rows,
        "exact_canonical_star_discrepancy_rows": canonical_rows,
        "algorithm": "deterministic prime construction, rational chord envelopes, exact Fermat quotients modulo q, and Fraction star-discrepancy sorting",
        "complexity": "O(N sqrt(q_N)) replay for the countermodel and O(P log P) exact sorting plus modular exponentiation for P canonical primes",
        "random_seed": None,
        "input_range": {
            "countermodel_term_count": COLLATZ_COUNTERMODEL_COUNT,
            "canonical_maximum_prime_prefix_count": maximum_prefix,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "first_harmonic_cancellation_proved": True,
            "star_discrepancy_liminf_lower_bound": fraction_record(Fraction(1, 6)),
            "first_harmonic_implies_angular_discrepancy_refuted": True,
            "canonical_prefix_count": maximum_prefix,
            "canonical_largest_prime": canonical_points[-1][1],
            "canonical_first_dyadic_discrepancy_increase_prefix": first_increase_prefix,
            "canonical_angular_discrepancy_tends_to_zero_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def goldbach_q3_product_parity_audit() -> dict[str, Any]:
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
        product_residue = 1 if minus_count % 2 == 0 else 2
        tie_forced_count = (prefix - 1) // 2
        verified = (
            tie_forced_count == 3 * scale + 1
            and tie_forced_count % 2 == 0
            and product_residue == 2
            and counts == source["independent_segmented_residue_counts"]
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
            "prime_prefix_product_mod_3_excluding_prime_3": product_residue,
            "tie_would_force_each_nonzero_count": tie_forced_count,
            "tie_would_force_product_mod_3": 1,
            "minus_one_product_excludes_tie": product_residue == 2,
            "independent_residue_algorithms_agree": counts == source["independent_segmented_residue_counts"],
            "row_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"actual:{level}:{scale}:{prefix}:{source['exact_nth_prime_endpoint']}:"
            f"{','.join(map(str, counts))}:{minus_count}:{product_residue}:"
            f"{tie_forced_count}:{int(verified)}\n".encode("ascii")
        )
    for level in GOLDBACH_ABSTRACT_LEVELS:
        scale = 3 ** (6 * level + 2)
        prefix = 6 * scale + 3
        nonzero_length = prefix - 1
        plus_count = nonzero_length // 2
        minus_count = nonzero_length // 2
        alternating_sum = 0
        product_residue = 1 if minus_count % 2 == 0 else 2
        verified = (
            nonzero_length % 2 == 0
            and plus_count == minus_count == 3 * scale + 1
            and minus_count % 2 == 0
            and alternating_sum == 0
            and product_residue == 1
        )
        failures += int(not verified)
        row = {
            "level_l": level,
            "special_prefix_length_T_l": str(prefix),
            "abstract_nonzero_symbol_length": str(nonzero_length),
            "alternating_plus_count": str(plus_count),
            "alternating_minus_count": str(minus_count),
            "prefix_difference": alternating_sum,
            "abstract_product_mod_3": product_residue,
            "all_prefix_discrepancies_at_most_one": True,
            "special_tie_verified": verified,
        }
        abstract_rows.append(row)
        transcript.update(
            f"abstract:{level}:{scale}:{prefix}:{nonzero_length}:{plus_count}:"
            f"{minus_count}:{product_residue}:{int(verified)}\n".encode("ascii")
        )
    theorem = (
        "For every l>=0 let T_l=6*3^(6l+2)+3 and let P_l be the product "
        "modulo 3 of the first T_l primes after omitting the prime 3. If the "
        "mod-3 prime race ties at T_l, then P_l=1 modulo 3. Consequently "
        "P_l=-1 modulo 3 is a sufficient exact certificate excluding the "
        "TICKET-260 compatible prefix. Moreover asymptotic density balance "
        "alone cannot exclude these ties."
    )
    proof = (
        "A tie has N_1=N_2=(T_l-1)/2=3*3^(6l+2)+1, an even integer. The "
        "product of all nonzero residue symbols is (-1)^N_2=1 modulo 3. Its "
        "contrapositive proves the product-minus-one certificate. For the "
        "density-only no-go, prepend the unique zero symbol and then alternate "
        "+1,-1 forever. Every ordinary prefix discrepancy is at most one, the "
        "two symbol densities tend to one half, yet every T_l-1 is even and "
        "there is an exact tie at every special prefix. The three actual finite "
        "certificates have product -1, but no all-l product theorem is proved."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_q3_product_parity_certificate_rows": rows,
        "exact_density_only_tie_countermodel_rows": abstract_rows,
        "algorithm": "exact parity arithmetic applied to two independently reproduced mod-3 prime-prefix counts, plus a closed-form alternating countermodel",
        "complexity": "O(1) parity work per level after the TICKET-260 exact residue certificates; the symbolic countermodel is unrestricted",
        "random_seed": None,
        "input_range": {
            "actual_certificate_level_min": rows[0]["level_l"],
            "actual_certificate_level_max": rows[-1]["level_l"],
            "abstract_replay_level_min": GOLDBACH_ABSTRACT_LEVELS[0],
            "abstract_replay_level_max": GOLDBACH_ABSTRACT_LEVELS[-1],
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "tie_forces_product_plus_one_mod_3_proved": True,
            "product_minus_one_excludes_tie_proved": True,
            "actual_product_minus_one_certificate_count": len(rows),
            "density_balance_alone_excludes_special_ties_refuted": True,
            "all_special_prime_prefix_products_minus_one_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def twin_bidirectional_second_order_audit() -> dict[str, Any]:
    _, source_rows, lower, upper = certified_root_continued_fraction(TWIN_CONVERGENT_COUNT)
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    denominator_first_passes: list[dict[str, Any]] = []
    denominator_second_passes: list[dict[str, Any]] = []
    numerator_first_nontrivial_passes: list[dict[str, Any]] = []
    numerator_second_nontrivial_passes: list[dict[str, Any]] = []
    joint_first_passes: list[dict[str, Any]] = []
    joint_second_passes: list[dict[str, Any]] = []
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
            denominator_squared = denominator * denominator
            denominator_first_residue = (
                pow(numerator, 17, denominator) - epsilon
            ) % denominator
            denominator_second_residue = (
                pow(numerator, 17, denominator_squared)
                + 17 * pow(numerator, 16, denominator_squared) * denominator
                - epsilon
            ) % denominator_squared
            denominator_direct_residue = (coefficient - epsilon) % denominator_squared
            denominator_first_pass = denominator_first_residue == 0
            denominator_second_pass = denominator_second_residue == 0

            numerator_modulus = abs(numerator)
            numerator_defined = numerator_modulus > 0
            if numerator_defined:
                numerator_squared = numerator_modulus * numerator_modulus
                numerator_first_residue = (
                    256 * pow(denominator, 17, numerator_modulus) - epsilon
                ) % numerator_modulus
                numerator_second_residue = (
                    256 * pow(denominator, 17, numerator_squared)
                    + 4352
                    * (numerator % numerator_squared)
                    * pow(denominator, 16, numerator_squared)
                    - epsilon
                ) % numerator_squared
                numerator_direct_residue = (coefficient - epsilon) % numerator_squared
                numerator_first_pass = numerator_first_residue == 0
                numerator_second_pass = numerator_second_residue == 0
            else:
                numerator_first_residue = None
                numerator_second_residue = None
                numerator_direct_residue = None
                numerator_first_pass = False
                numerator_second_pass = False
            joint_first_pass = denominator_first_pass and numerator_first_pass
            joint_second_pass = denominator_second_pass and numerator_second_pass
            witness = {
                "term_index": index,
                "epsilon": epsilon,
                "numerator": str(numerator),
                "denominator": str(denominator),
            }
            if denominator >= 2 and denominator_first_pass:
                denominator_first_passes.append(witness)
            if denominator >= 2 and denominator_second_pass:
                denominator_second_passes.append(witness)
            if numerator_modulus >= 2 and numerator_first_pass:
                numerator_first_nontrivial_passes.append(witness)
            if numerator_modulus >= 2 and numerator_second_pass:
                numerator_second_nontrivial_passes.append(witness)
            if denominator >= 2 and numerator_defined and joint_first_pass:
                joint_first_passes.append(witness)
            if denominator >= 2 and numerator_defined and joint_second_pass:
                joint_second_passes.append(witness)
            expansion_verified = expansion_verified and (
                denominator_second_residue == denominator_direct_residue
                and (
                    not numerator_defined
                    or numerator_second_residue == numerator_direct_residue
                )
            )
            sign_rows.append(
                {
                    "epsilon": epsilon,
                    "numerator_modulus_defined": numerator_defined,
                    "denominator_first_residue_mod_v": str(denominator_first_residue),
                    "denominator_second_residue_mod_v_squared": str(denominator_second_residue),
                    "denominator_direct_B1_residue_mod_v_squared": str(denominator_direct_residue),
                    "numerator_first_residue_mod_abs_u": None
                    if numerator_first_residue is None
                    else str(numerator_first_residue),
                    "numerator_second_residue_mod_u_squared": None
                    if numerator_second_residue is None
                    else str(numerator_second_residue),
                    "numerator_direct_B1_residue_mod_u_squared": None
                    if numerator_direct_residue is None
                    else str(numerator_direct_residue),
                    "denominator_first_pass": denominator_first_pass,
                    "denominator_second_pass": denominator_second_pass,
                    "numerator_first_pass": numerator_first_pass,
                    "numerator_second_pass": numerator_second_pass,
                    "joint_first_pass": joint_first_pass,
                    "joint_second_pass": joint_second_pass,
                }
            )
        direct_unit_hit = abs(coefficient) == 1
        verified = monotone and expansion_verified and not direct_unit_hit
        failures += int(not verified)
        coefficient_digest = hashlib.sha256(str(coefficient).encode("ascii")).hexdigest()
        row = {
            "term_index": index,
            "partial_quotient": source["partial_quotient"],
            "convergent_numerator": str(numerator),
            "convergent_denominator": str(denominator),
            "denominator_digit_count": len(str(denominator)),
            "root_side": source["root_side"],
            "B_1_value_sha256": coefficient_digest,
            "sign_tests": sign_rows,
            "both_truncated_expansions_match_direct_B1": expansion_verified,
            "direct_unit_coefficient_hit": direct_unit_hit,
            "row_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"{index}:{source['partial_quotient']}:{numerator}:{denominator}:"
            f"{coefficient_digest}:{sign_rows[0]['denominator_second_residue_mod_v_squared']}:"
            f"{sign_rows[0]['numerator_second_residue_mod_u_squared']}:"
            f"{sign_rows[1]['denominator_second_residue_mod_v_squared']}:"
            f"{sign_rows[1]['numerator_second_residue_mod_u_squared']}:"
            f"{int(expansion_verified)}:{int(direct_unit_hit)}\n".encode("ascii")
        )
    expected_denominator_first = [(2, -1, -1, 13), (3, -1, -1, 14)]
    observed_denominator_first = [
        (
            row["term_index"],
            row["epsilon"],
            int(row["numerator"]),
            int(row["denominator"]),
        )
        for row in denominator_first_passes
    ]
    expected_numerator_first = [(5, -1, -3, 41)]
    observed_numerator_first = [
        (
            row["term_index"],
            row["epsilon"],
            int(row["numerator"]),
            int(row["denominator"]),
        )
        for row in numerator_first_nontrivial_passes
    ]
    failures += int(observed_denominator_first != expected_denominator_first)
    failures += int(observed_numerator_first != expected_numerator_first)
    failures += len(denominator_second_passes)
    failures += len(numerator_second_nontrivial_passes)
    failures += len(joint_second_passes)
    theorem = (
        "Let B_1(u,v) be the TICKET-257 degree-17 homogeneous form. For "
        "integers u,v with uv nonzero and epsilon in {-1,1}, B_1(u,v)=epsilon "
        "forces u^17+17u^16v=epsilon modulo v^2 and "
        "256v^17+4352uv^16=epsilon modulo u^2. Among the first 1024 certified "
        "continued-fraction convergents of the unique root, both signs fail the "
        "joint second-order condition."
    )
    proof = (
        "The terms of B_1 with v-degree zero and one are u^17 and 17u^16v; "
        "all remaining terms are divisible by v^2. At the opposite end, the "
        "u-degree zero and one terms are 256v^17 and 4352uv^16; all remaining "
        "terms are divisible by u^2. Reduction proves both necessary "
        "congruences. Each certified convergent is checked for both signs by "
        "modular exponentiation, and both truncated residues are independently "
        "compared with the full exact B_1 value. The finite prefix reaches a "
        "519-digit denominator and cannot exclude infinitely many later "
        "convergents."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_bidirectional_convergent_rows": rows,
        "denominator_first_order_nontrivial_passes": denominator_first_passes,
        "denominator_second_order_nontrivial_passes": denominator_second_passes,
        "numerator_first_order_nontrivial_passes": numerator_first_nontrivial_passes,
        "numerator_second_order_nontrivial_passes": numerator_second_nontrivial_passes,
        "joint_first_order_passes": joint_first_passes,
        "joint_second_order_passes": joint_second_passes,
        "final_exact_root_bracket": {
            "lower": fraction_record(lower),
            "upper": fraction_record(upper),
        },
        "algorithm": "certified rational continued fractions, modular exponentiation modulo v^2 and u^2, and two independent full-form residue comparisons",
        "complexity": "O(K) certified convergents and O(K log 17) modular multiplications on O(log v_K)-bit integers",
        "random_seed": None,
        "input_range": {
            "certified_convergent_count": TWIN_CONVERGENT_COUNT,
            "epsilon_values": [-1, 1],
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "bidirectional_second_order_congruence_necessary_proved": True,
            "certified_convergent_count": len(rows),
            "maximum_denominator": rows[-1]["convergent_denominator"],
            "maximum_denominator_digit_count": rows[-1]["denominator_digit_count"],
            "denominator_first_order_nontrivial_pass_count": len(denominator_first_passes),
            "denominator_second_order_nontrivial_pass_count": len(denominator_second_passes),
            "numerator_first_order_nontrivial_pass_count": len(numerator_first_nontrivial_passes),
            "numerator_second_order_nontrivial_pass_count": len(numerator_second_nontrivial_passes),
            "joint_second_order_pass_count": len(joint_second_passes),
            "bidirectional_first_order_filter_complete": False,
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
        {"id": f"{code}-T260", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T261", "label": theorem_name, "status": "proved"},
        {
            "id": f"{code}-CERT261",
            "label": f"{theorem_name}ExactReplay",
            "status": "computed_finite",
        },
        {"id": f"{code}-REJECT261", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN261", "label": open_name, "status": "open"},
    ]
    return {
        "nodes": nodes,
        "edges": [
            [f"{code}-T260", f"{code}-T261"],
            [f"{code}-T261", f"{code}-CERT261"],
            [f"{code}-T261", f"{code}-REJECT261"],
            [f"{code}-T261", f"{code}-OPEN261"],
        ],
        "resolution_path": [f"{code}-T260", f"{code}-T261", f"{code}-OPEN261"],
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
        "ticket_id": f"{code}-TICKET-261",
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
    riemann = riemann_summability_sharpness_audit()
    collatz = collatz_first_harmonic_no_go_audit()
    goldbach = goldbach_q3_product_parity_audit()
    twin = twin_bidirectional_second_order_audit()
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "SummableScaledVariationNecessityNoGo",
            "exact_no_go",
            riemann,
            "treating summable scaled downward variation as necessary for eventual packet-lag positivity",
            [
                "direct arithmetic proof of a strict scaled-jump limsup bound for actual Guinand-Weil packet energies"
            ],
            "the TICKET-260 sufficient criterion together with the exact reciprocal-tail sharpness counterfamily",
            "ActualWeilPacketScaledDownwardJumpLimsupBelowLimit",
            "SummableScaledDownwardVariationForcesEventualLagPositivity",
            "EventualLagPositivityImpliesSummableScaledDownwardVariation",
            "Summability is now known to be stronger than necessary, but no weaker scaled-jump estimate is proved for actual Guinand-Weil packets.",
            "No RH proof or disproof; the abstract sufficient hypothesis is sharply classified as non-necessary.",
            f"{len(riemann['exact_reciprocal_tail_rows'])} Fraction rows replay the exact reciprocal-tail family; no actual Weil coefficient is computed.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "FirstHarmonicCancellationAngularDiscrepancyNoGo",
            "exact_no_go",
            collatz,
            "deducing angular discrepancy decay from cancellation of only the first growing-modulus Weyl harmonic",
            [
                "all-nonzero-harmonic Weyl cancellation for the canonical fixed-base Fermat-quotient exponents"
            ],
            "the exact two-cluster growing-prime counterfamily and exact canonical star-discrepancy diagnostics",
            "CanonicalFermatQuotientWeylSumsVanishForEveryNonzeroH",
            "FixedModulusExponentEquidistributionPhaseAlignmentNoGo",
            "FirstHarmonicCancellationImpliesAngularDiscrepancyZeroForGrowingPrimeModuli",
            "The first harmonic is insufficient; no all-harmonic Weyl-sum theorem is proved for the canonical Fermat-quotient exponents.",
            "No Collatz proof or counterexample; a one-harmonic shortcut to the canonical angular-discrepancy target is eliminated.",
            f"{len(collatz['exact_first_harmonic_countermodel_rows'])} abstract phase rows and {len(collatz['exact_canonical_star_discrepancy_rows'])} exact canonical dyadic prefixes are checked.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "Q3PrimePrefixProductParityObstruction",
            "partial_theorem",
            goldbach,
            "using asymptotic or even uniformly bounded residue-density discrepancy alone to exclude exact ties at the special q=3 indices",
            [
                "an all-level arithmetic proof that every special q=3 prime-prefix product is minus one modulo three"
            ],
            "the exact tie-to-product parity implication, three actual product certificates, and the density-only alternating no-go",
            "Q3SpecialPrimePrefixProductIsMinusOneModuloThree",
            "Q3CompatibleFamilyPrimeRaceEquivalence",
            "DensityBalanceAloneExcludesEveryQ3SpecialPrimeRaceTie",
            "Product minus one is a sufficient parity certificate, but no theorem establishes it at every special prime prefix.",
            "No strong Goldbach proof or counterexample; three finite levels pass the new parity certificate and the density-only route is rigorously blocked.",
            f"{len(goldbach['exact_q3_product_parity_certificate_rows'])} actual levels are certified; the parity implication and alternating countermodel hold for all levels.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "BidirectionalSecondOrderCongruenceAnd1024ConvergentCertificate",
            "partial_theorem",
            twin,
            "using the pair of first-order numerator and denominator congruences as a complete unique-root convergent filter",
            [
                "global exclusion of simultaneous second-order numerator and denominator congruences on every later unique-root convergent"
            ],
            "the exact modulo-v-squared and modulo-u-squared necessary pair and the 1024-convergent two-sign certificate",
            "NoUniqueRootConvergentSatisfiesBothSecondOrderCongruences",
            "SecondOrderDenominatorCongruenceAnd256ConvergentCertificate",
            "BidirectionalFirstOrderCongruencesEliminateEveryUniqueRootConvergent",
            "The dual second-order sieve eliminates 1024 certified convergents, but infinitely many later convergents are not controlled.",
            "No twin-prime proof or counterexample; the remaining exponent-17 branch gains a second independent scale-dependent congruence.",
            f"Both signs are tested on the first {TWIN_CONVERGENT_COUNT} certified convergents; no finite prefix excludes every convergent.",
        ),
    }
    total_failures = sum(
        item["reproducible_computation"]["failure_count"] for item in sections.values()
    )
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureSharpnessWeylTiesDualCongruenceAudit",
            "summary": (
                "TICKET-261 proves two exact route no-go theorems and two partial "
                "theorems: scaled-variation summability is not necessary for RH-style "
                "lag positivity, one Weyl harmonic does not force Collatz angular "
                "discrepancy, q=3 Goldbach ties obey a prime-prefix product parity "
                "obstruction, and the Twin degree-17 branch obeys bidirectional "
                "second-order congruences; all parent conjectures remain open."
            ),
            **sections,
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 2,
                "exact_no_go_count": 2,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "twin_prime",
                "stagnated_problem_count": 0,
                "riemann_reciprocal_tail_case_count": len(
                    riemann["exact_reciprocal_tail_rows"]
                ),
                "collatz_countermodel_phase_case_count": len(
                    collatz["exact_first_harmonic_countermodel_rows"]
                ),
                "collatz_canonical_prefix_count": collatz["aggregate"][
                    "canonical_prefix_count"
                ],
                "collatz_canonical_dyadic_row_count": len(
                    collatz["exact_canonical_star_discrepancy_rows"]
                ),
                "goldbach_actual_parity_certificate_count": len(
                    goldbach["exact_q3_product_parity_certificate_rows"]
                ),
                "goldbach_abstract_tie_replay_count": len(
                    goldbach["exact_density_only_tie_countermodel_rows"]
                ),
                "twin_convergent_count": len(
                    twin["exact_bidirectional_convergent_rows"]
                ),
                "twin_denominator_first_order_pass_count": twin["aggregate"][
                    "denominator_first_order_nontrivial_pass_count"
                ],
                "twin_numerator_first_order_nontrivial_pass_count": twin[
                    "aggregate"
                ]["numerator_first_order_nontrivial_pass_count"],
                "twin_joint_second_order_pass_count": twin["aggregate"][
                    "joint_second_order_pass_count"
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
                "candidate_theorem": item["route_decision"]["next_single_lemma"],
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
        "ticket": 261,
        "parent_ticket": 260,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "twin_prime",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(
        ROOT
        / "data/open-problem/ticket261-sharpness-weyl-ties-dualcongruence.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-261-summability-necessity-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-261-first-harmonic-discrepancy-no-go.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-261-q3-product-parity.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-261-bidirectional-second-order.json",
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
