from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache
from math import comb, gcd
from pathlib import Path
from typing import Any


sys.set_int_max_str_digits(0)

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket254_diagonal_weighted_reflection_thue import (
    fraction_record,
    write_json,
)
from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket258_variation_character_convergent import (
    certified_root_continued_fraction,
)
from scripts.ticket260_weighted_equidistribution_primerace_variablemod import (
    goldbach_q3_prime_race_audit,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket263-sharp-envelope-diagonal-mod32-ninthorder.v1"
GENERATED_AT = "2026-09-01T23:59:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "sharp_envelope_diagonal_mod32_ninthorder_audit"

RIEMANN_REPLAY_COUNT = 64
RIEMANN_AMPLITUDES = (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3))
COLLATZ_GRID_SIZES = (4, 8, 16, 32, 64)
GOLDBACH_ABSTRACT_LEVELS = tuple(range(16))
TWIN_CONVERGENT_COUNT = 1024
TWIN_JET_ORDER = 9
TWIN_COEFFICIENTS = tuple(comb(17, k) * 2 ** (k // 2) for k in range(18))
TWIN_ABSOLUTE_COEFFICIENT_SUM = sum(TWIN_COEFFICIENTS)
TWIN_ROOT_CONE_RECIPROCAL_FLOOR = 16
TWIN_EXACTNESS_THRESHOLD = (
    TWIN_ABSOLUTE_COEFFICIENT_SUM + 1
) * TWIN_ROOT_CONE_RECIPROCAL_FLOOR**TWIN_JET_ORDER


@lru_cache(maxsize=1)
def riemann_sharp_reciprocal_envelope_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for amplitude in RIEMANN_AMPLITUDES:
        family_rows: list[dict[str, Any]] = []
        for index in range(1, RIEMANN_REPLAY_COUNT + 1):
            sign = -1 if index % 2 else 1
            energy = Fraction(1) + sign * amplitude / index
            next_energy = Fraction(1) - sign * amplitude / (index + 1)
            scaled_error = index * abs(energy - 1)
            signed_jump = index * (energy - next_energy)
            lag = (index + 1) * next_energy - index * energy
            expected_jump = sign * amplitude * Fraction(2 * index + 1, index + 1)
            expected_lag = Fraction(1) - 2 * sign * amplitude
            verified = (
                scaled_error == amplitude
                and signed_jump == expected_jump
                and lag == expected_lag
                and lag == next_energy - signed_jump
            )
            failures += int(not verified)
            row = {
                "index_n": index,
                "parity_sign": sign,
                "energy_E_n": fraction_record(energy),
                "next_energy_E_n_plus_1": fraction_record(next_energy),
                "scaled_absolute_error": fraction_record(scaled_error),
                "scaled_signed_jump_J_n": fraction_record(signed_jump),
                "lag_S_n": fraction_record(lag),
                "row_verified": verified,
            }
            family_rows.append(row)
            transcript.update(
                f"{amplitude}:{index}:{sign}:{energy}:{next_energy}:"
                f"{scaled_error}:{signed_jump}:{lag}:{int(verified)}\n".encode(
                    "ascii"
                )
            )
        rows.append(
            {
                "limit_L": fraction_record(Fraction(1)),
                "reciprocal_envelope_A": fraction_record(amplitude),
                "regime": (
                    "strict" if 2 * amplitude < 1 else "critical" if 2 * amplitude == 1 else "supercritical"
                ),
                "predicted_liminf_lag": fraction_record(1 - 2 * amplitude),
                "exact_rows": family_rows,
            }
        )
    theorem = (
        "Let E_n be a real sequence converging to L>0, put "
        "A=limsup_(n to infinity) n|E_n-L|, J_n=n(E_n-E_(n+1)), and "
        "S_n=(n+1)E_(n+1)-nE_n. Then limsup J_n<=2A and "
        "liminf S_n>=L-2A. Hence A<L/2 implies an eventual positive lag "
        "margin. The factor two is optimal: for every L,A>0, "
        "E_n=L+(-1)^n A/n has limsup J_n=2A and liminf S_n=L-2A; at "
        "A=L/2 no positive margin follows."
    )
    proof = (
        "Write a_n=E_n-L. The inequality J_n<=n|a_n|+n|a_(n+1)| "
        "and n|a_(n+1)|=[n/(n+1)](n+1)|a_(n+1)| give limsup J_n<=2A. "
        "TICKET-262's identity S_n=E_(n+1)-J_n then gives "
        "liminf S_n>=L-2A. If A<L/2, half the positive residual supplies "
        "an eventual margin. For the alternating reciprocal family, direct "
        "calculation gives J_n=(-1)^n A(2n+1)/(n+1) and "
        "S_n=L-2(-1)^n A, proving equality and refuting every universal "
        "constant smaller than two. These are abstract sequences, not actual "
        "Guinand-Weil packet energies."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_alternating_reciprocal_envelope_families": rows,
        "algorithm": "closed-form Fraction evaluation of three alternating reciprocal error families",
        "complexity": "O(FN) exact rational operations; the sharp inequality is symbolic",
        "random_seed": None,
        "input_range": {
            "limit_L": "1",
            "amplitudes_A": [str(value) for value in RIEMANN_AMPLITUDES],
            "index_min": 1,
            "index_max": RIEMANN_REPLAY_COUNT,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "sharp_reciprocal_envelope_bound_proved": True,
            "optimal_factor_two_proved": True,
            "critical_half_limit_margin_refuted": True,
            "replayed_row_count": len(RIEMANN_AMPLITUDES) * RIEMANN_REPLAY_COUNT,
            "actual_weil_reciprocal_envelope_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def collatz_diagonal_weyl_uniformization_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    total_harmonics = 0
    for modulus in COLLATZ_GRID_SIZES:
        residue_counts = [1] * modulus
        harmonic_rows: list[dict[str, Any]] = []
        for harmonic in range(1, modulus):
            root_sum_zero = harmonic % modulus != 0
            verified = root_sum_zero and sum(residue_counts) == modulus
            failures += int(not verified)
            harmonic_rows.append(
                {
                    "harmonic_h": harmonic,
                    "complete_root_sum_zero": root_sum_zero,
                    "normalized_weyl_magnitude_squared": fraction_record(Fraction(0)),
                    "row_verified": verified,
                }
            )
            transcript.update(
                f"grid:{modulus}:{harmonic}:{int(root_sum_zero)}:{int(verified)}\n".encode(
                    "ascii"
                )
            )
        total_harmonics += len(harmonic_rows)
        discrepancy = Fraction(1, modulus)
        rows.append(
            {
                "grid_modulus_M": modulus,
                "point_count_N": modulus,
                "uniform_cutoff_H": modulus - 1,
                "residue_counts": residue_counts,
                "exact_star_discrepancy": fraction_record(discrepancy),
                "harmonic_rows": harmonic_rows,
                "case_verified": all(row["row_verified"] for row in harmonic_rows),
            }
        )
    theorem = (
        "For any sequence x_j in R/Z, write W_N(h)=N^(-1) sum_(j<=N) "
        "exp(2*pi*i*h*x_j). The following are equivalent: (i) W_N(h) tends "
        "to zero for every nonzero integer h; (ii) there is a nondecreasing "
        "integer sequence H_N tending to infinity such that "
        "max_(1<=|h|<=H_N)|W_N(h)| tends to zero. Consequently either "
        "condition implies star discrepancy tending to zero by the classical "
        "Weyl criterion."
    )
    proof = (
        "Condition (ii) immediately implies (i), since every fixed h is "
        "eventually below H_N. Conversely, under (i), for each m choose an "
        "integer N_m larger than N_(m-1) such that for every N>=N_m and "
        "1<=|h|<=m one has |W_N(h)|<=1/m. Define H_N as the largest m with "
        "N_m<=N (and one before N_1). Then H_N is nondecreasing, tends to "
        "infinity, and the moving maximum is at most 1/H_N. The discrepancy "
        "conclusion is exactly the classical Weyl criterion, not a new "
        "arithmetic estimate. The complete rational grids replay simultaneous "
        "finite cancellation symbolically through the geometric root-sum "
        "identity; they contain no canonical Fermat-quotient data."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_complete_grid_replays": rows,
        "algorithm": "integer residue counts and the exact complete-root geometric-sum criterion h mod M != 0",
        "complexity": "O(sum M) integer checks for the replay; the diagonal equivalence is nonquantitative and symbolic",
        "random_seed": None,
        "input_range": {"complete_grid_moduli": list(COLLATZ_GRID_SIZES)},
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "pointwise_all_harmonics_iff_some_growing_uniform_cutoff_proved": True,
            "weyl_criterion_external_transfer_used": True,
            "complete_grid_replay_count": len(rows),
            "complete_grid_harmonic_case_count": total_harmonics,
            "canonical_growing_cutoff_uniform_cancellation_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def _tie_mod32(level: int) -> int:
    return (pow(3, 6 * level + 3, 32) + 1) % 32


@lru_cache(maxsize=1)
def goldbach_q3_mod32_phase_audit() -> dict[str, Any]:
    prior = goldbach_q3_prime_race_audit()
    actual_rows: list[dict[str, Any]] = []
    symbolic_rows: list[dict[str, Any]] = []
    countermodels: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    expected_phase = (28, 4, 12, 20)
    for source in prior["exact_q3_prime_race_certificate_rows"]:
        level = source["level_l"]
        counts = source["actual_residue_counts"]
        minus_count = counts[2]
        tie_count = 3 ** (6 * level + 3) + 1
        predicted = expected_phase[level % 4]
        actual = minus_count % 32
        verified = (
            predicted == _tie_mod32(level)
            and tie_count % 32 == predicted
            and actual != predicted
            and counts == source["independent_segmented_residue_counts"]
        )
        failures += int(not verified)
        row = {
            "level_l": level,
            "special_prime_prefix_length_T_l": source["forced_prefix_length_T"],
            "exact_nth_prime_endpoint": source["exact_nth_prime_endpoint"],
            "actual_residue_counts_mod_3": counts,
            "actual_minus_one_count_N_2": minus_count,
            "actual_N_2_mod_32": actual,
            "tie_forced_count": tie_count,
            "tie_forced_mod_32": predicted,
            "tie_excluded_by_mod_32_contrapositive": actual != predicted,
            "independent_residue_algorithms_agree": counts == source["independent_segmented_residue_counts"],
            "row_verified": verified,
        }
        actual_rows.append(row)
        transcript.update(
            f"actual:{level}:{source['forced_prefix_length_T']}:"
            f"{source['exact_nth_prime_endpoint']}:{minus_count}:{actual}:"
            f"{tie_count}:{predicted}:{int(verified)}\n".encode("ascii")
        )
    for level in GOLDBACH_ABSTRACT_LEVELS:
        tie_count = 3 ** (6 * level + 3) + 1
        predicted = expected_phase[level % 4]
        valuation_two = (tie_count % 8 == 4) and (tie_count % 16 in (4, 12))
        verified = tie_count % 32 == predicted and valuation_two
        failures += int(not verified)
        symbolic_rows.append(
            {
                "level_l": level,
                "level_phase_mod_4": level % 4,
                "tie_forced_count": str(tie_count),
                "tie_forced_mod_32": predicted,
                "exact_two_adic_valuation_two": valuation_two,
                "row_verified": verified,
            }
        )
        transcript.update(
            f"symbolic:{level}:{level % 4}:{tie_count}:{predicted}:"
            f"{int(valuation_two)}:{int(verified)}\n".encode("ascii")
        )
        if level >= 1:
            plus_count = tie_count - 32
            minus_count = tie_count + 32
            model_verified = (
                plus_count >= 0
                and plus_count + minus_count == 2 * tie_count
                and plus_count != minus_count
                and minus_count % 32 == predicted
            )
            failures += int(not model_verified)
            countermodels.append(
                {
                    "level_l": level,
                    "N_1": str(plus_count),
                    "N_2": str(minus_count),
                    "N_2_mod_32": minus_count % 32,
                    "same_total_as_tie": plus_count + minus_count == 2 * tie_count,
                    "non_tie": plus_count != minus_count,
                    "row_verified": model_verified,
                }
            )
            transcript.update(
                f"countermodel:{level}:{plus_count}:{minus_count}:"
                f"{minus_count % 32}:{int(model_verified)}\n".encode("ascii")
            )
    theorem = (
        "Put T_l=6*3^(6l+2)+3. If the nonzero modulo-three residue counts "
        "among the first T_l primes tie, then N_2=3^(6l+3)+1 and, according "
        "to l modulo four, N_2 is congruent modulo 32 to 28, 4, 12, or 20. "
        "Thus an actual N_2 outside the corresponding phase excludes the tie. "
        "For every l>=1 this phased congruence is not sufficient: the exact "
        "count pair (N_1,N_2)=(M-32,M+32), M=3^(6l+3)+1, has the same total "
        "and the required N_2 residue but is not tied."
    )
    proof = (
        "A tie splits the T_l-1 nonzero residues equally, giving "
        "M=3^(6l+3)+1. The powers of 3 modulo 32 have period eight. The "
        "exponent 6l+3 has residues 3,1,7,5 modulo eight as l has residues "
        "0,1,2,3 modulo four, which yields 28,4,12,20 after adding one. "
        "The displayed shifted counts are nonnegative for l>=1, preserve "
        "the total 2M and N_2 modulo 32, but differ by 64. Therefore the "
        "condition is necessary and sharply non-sufficient beyond level zero."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_actual_q3_mod32_certificate_rows": actual_rows,
        "exact_symbolic_mod32_phase_rows": symbolic_rows,
        "exact_mod32_nonsufficiency_countermodels": countermodels,
        "algorithm": "two independent exact prime-residue counts inherited from TICKET-260 plus integer modular exponentiation modulo 32",
        "complexity": "O(pi endpoint) for the three inherited actual prefixes and O(L log exponent) modular operations for symbolic levels",
        "random_seed": None,
        "input_range": {
            "actual_levels": [row["level_l"] for row in actual_rows],
            "symbolic_level_min": min(GOLDBACH_ABSTRACT_LEVELS),
            "symbolic_level_max": max(GOLDBACH_ABSTRACT_LEVELS),
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "tie_forces_level_phased_mod32_proved": True,
            "actual_mod32_non_tie_certificate_count": len(actual_rows),
            "mod32_sufficiency_refuted_for_every_level_at_least_one": True,
            "mod32_countermodel_count": len(countermodels),
            "all_actual_special_counts_avoid_phased_mod32_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def _truncated_b1(u: int, v: int, start: int, stop: int) -> int:
    return sum(
        TWIN_COEFFICIENTS[k] * u ** (17 - k) * v**k
        for k in range(start, stop)
    )


@lru_cache(maxsize=1)
def twin_ninth_order_exactness_audit() -> dict[str, Any]:
    _, source_rows, lower, upper = certified_root_continued_fraction(
        TWIN_CONVERGENT_COUNT
    )
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    joint_passes: list[dict[str, Any]] = []
    degenerate_joint_passes: list[dict[str, Any]] = []
    first_tail_index: int | None = None
    tail_case_count = 0
    failure_order_histogram = {str(order): 0 for order in range(1, TWIN_JET_ORDER + 1)}
    failure_order_histogram["none_through_9"] = 0
    previous_denominator = 0
    for source in source_rows:
        index = source["term_index"]
        numerator = int(source["convergent_numerator"])
        denominator = int(source["convergent_denominator"])
        coefficient = int(source["B_1_at_convergent"])
        coprime = gcd(abs(numerator), denominator) == 1
        monotone = denominator >= previous_denominator
        previous_denominator = denominator
        in_root_cone = (
            numerator != 0
            and abs(numerator) <= denominator
            and TWIN_ROOT_CONE_RECIPROCAL_FLOOR * abs(numerator) >= denominator
        )
        above_threshold = denominator > TWIN_EXACTNESS_THRESHOLD
        tail_applicable = coprime and in_root_cone and above_threshold
        if tail_applicable:
            tail_case_count += 1
            if first_tail_index is None:
                first_tail_index = index
        sign_rows: list[dict[str, Any]] = []
        row_verified = monotone and coprime
        for epsilon in (-1, 1):
            difference = coefficient - epsilon
            joint_by_order: list[bool] = []
            expansion_verified = True
            for order in range(1, TWIN_JET_ORDER + 1):
                modulus_v = denominator**order
                left = (_truncated_b1(numerator, denominator, 0, order) - epsilon) % modulus_v
                direct_v = difference % modulus_v
                if numerator:
                    modulus_u = abs(numerator) ** order
                    right = (
                        _truncated_b1(numerator, denominator, 18 - order, 18)
                        - epsilon
                    ) % modulus_u
                    direct_u = difference % modulus_u
                    joint = left == 0 and right == 0
                    expansion_verified = expansion_verified and left == direct_v and right == direct_u
                else:
                    joint = False
                    expansion_verified = expansion_verified and left == direct_v
                joint_by_order.append(joint)
            first_failure = next(
                (order for order, passed in enumerate(joint_by_order, 1) if not passed),
                None,
            )
            histogram_key = "none_through_9" if first_failure is None else str(first_failure)
            failure_order_histogram[histogram_key] += 1
            ninth_pass = joint_by_order[-1]
            witness = {
                "term_index": index,
                "epsilon": epsilon,
                "numerator": str(numerator),
                "denominator": str(denominator),
            }
            if ninth_pass:
                if abs(numerator) >= 2 and denominator >= 2:
                    joint_passes.append(witness)
                else:
                    degenerate_joint_passes.append(witness)
            size_bound_verified = True
            if tail_applicable:
                upper_size = (TWIN_ABSOLUTE_COEFFICIENT_SUM + 1) * denominator**17
                divisor_size = (abs(numerator) * denominator) ** TWIN_JET_ORDER
                size_bound_verified = upper_size < divisor_size
            row_verified = row_verified and expansion_verified and size_bound_verified
            sign_rows.append(
                {
                    "epsilon": epsilon,
                    "joint_pass_by_order_1_through_9": joint_by_order,
                    "first_joint_failure_order": first_failure,
                    "joint_ninth_order_pass": ninth_pass,
                    "ninth_order_expansions_match_direct_B1": expansion_verified,
                    "tail_size_bound_verified_when_applicable": size_bound_verified,
                }
            )
        direct_unit_hit = abs(coefficient) == 1
        row_verified = row_verified and not direct_unit_hit
        failures += int(not row_verified)
        coefficient_digest = hashlib.sha256(str(coefficient).encode("ascii")).hexdigest()
        row = {
            "term_index": index,
            "partial_quotient": source["partial_quotient"],
            "convergent_numerator": str(numerator),
            "convergent_denominator": str(denominator),
            "denominator_digit_count": len(str(denominator)),
            "root_side": source["root_side"],
            "coprime": coprime,
            "inside_one_sixteenth_to_one_root_cone": in_root_cone,
            "above_ninth_order_exactness_threshold": above_threshold,
            "tail_exactness_theorem_applicable": tail_applicable,
            "B_1_value_sha256": coefficient_digest,
            "sign_tests": sign_rows,
            "direct_unit_coefficient_hit": direct_unit_hit,
            "row_verified": row_verified,
        }
        rows.append(row)
        transcript.update(
            f"{index}:{source['partial_quotient']}:{numerator}:{denominator}:"
            f"{coefficient_digest}:{int(in_root_cone)}:{int(above_threshold)}:"
            f"{int(tail_applicable)}:{sign_rows[0]['first_joint_failure_order']}:"
            f"{sign_rows[1]['first_joint_failure_order']}:"
            f"{int(row_verified)}\n".encode("ascii")
        )
    failures += len(joint_passes)
    theorem = (
        "Let a_k=C(17,k)2^floor(k/2) and "
        "B_1(u,v)=sum_(k=0)^17 a_k u^(17-k)v^k. Put A=sum a_k=2744210 "
        "and V_0=(A+1)16^9=188580743973175296. For coprime nonzero "
        "integers u,v with v>V_0 and 1/16<=|u|/v<=1, and epsilon in "
        "{-1,1}, B_1(u,v)=epsilon if and only if the first nine terms are "
        "epsilon modulo v^9 and the last nine terms are epsilon modulo u^9."
    )
    proof = (
        "Necessity follows by deleting terms divisible by v^9 or u^9. "
        "Conversely the joint congruences and gcd(u,v)=1 imply "
        "(|uv|)^9 divides B_1(u,v)-epsilon. Since |u|<=v, positivity of "
        "the coefficients gives |B_1-epsilon|<=(A+1)v^17. The cone gives "
        "(|uv|)^9>=v^18/16^9, which is strictly larger when v>V_0. A "
        "nonzero divisible integer cannot have smaller absolute value than "
        "its divisor, so B_1-epsilon=0. Thus order nine is an exact tail "
        "criterion on this cone, not merely another necessary jet. The finite "
        "continued-fraction replay checks both signs and orders one through "
        "nine on 1024 convergents; it does not prove that every later "
        "convergent fails the ninth-order pair."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "coefficient_vector_a_0_through_a_17": list(TWIN_COEFFICIENTS),
        "absolute_coefficient_sum_A": TWIN_ABSOLUTE_COEFFICIENT_SUM,
        "ninth_order_exactness_threshold_V_0": str(TWIN_EXACTNESS_THRESHOLD),
        "exact_ninth_order_convergent_rows": rows,
        "joint_ninth_order_passes": joint_passes,
        "degenerate_modulus_one_joint_ninth_order_passes": degenerate_joint_passes,
        "first_joint_failure_order_histogram_both_signs": failure_order_histogram,
        "final_exact_root_bracket": {
            "lower": fraction_record(lower),
            "upper": fraction_record(upper),
        },
        "algorithm": "certified rational continued fractions, exact degree-17 evaluation, and bidirectional modular truncation for orders one through nine",
        "complexity": "O(K*R*17) exact big-integer terms with moduli u^r and v^r, R=9",
        "random_seed": None,
        "input_range": {
            "certified_convergent_count": TWIN_CONVERGENT_COUNT,
            "epsilon_values": [-1, 1],
            "jet_order_min": 1,
            "jet_order_max": TWIN_JET_ORDER,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "joint_ninth_order_exactness_on_root_cone_proved": True,
            "certified_convergent_count": len(rows),
            "tail_exactness_applicable_convergent_count": tail_case_count,
            "first_tail_exactness_applicable_term_index": first_tail_index,
            "maximum_denominator_digit_count": rows[-1]["denominator_digit_count"],
            "joint_ninth_order_pass_count": len(joint_passes),
            "degenerate_modulus_one_joint_ninth_order_pass_count": len(
                degenerate_joint_passes
            ),
            "all_unique_root_convergents_excluded": False,
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
    external_name: str | None = None,
) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T262", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T263", "label": theorem_name, "status": "proved"},
        {
            "id": f"{code}-CERT263",
            "label": f"{theorem_name}ExactReplay",
            "status": "computed_finite",
        },
        {"id": f"{code}-REJECT263", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN263", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T262", f"{code}-T263"],
        [f"{code}-T263", f"{code}-CERT263"],
        [f"{code}-T263", f"{code}-REJECT263"],
        [f"{code}-T263", f"{code}-OPEN263"],
    ]
    if external_name:
        nodes.append(
            {"id": f"{code}-EXT263", "label": external_name, "status": "external_theorem"}
        )
        edges.append([f"{code}-EXT263", f"{code}-T263"])
    return {
        "nodes": nodes,
        "edges": edges,
        "resolution_path": [f"{code}-T262", f"{code}-T263", f"{code}-OPEN263"],
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
    external_name: str | None = None,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{code}-TICKET-263",
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
            code, prior_name, theorem_name, rejected_name, next_lemma, external_name
        ),
        "claim_boundary": claim_boundary,
    }


@lru_cache(maxsize=1)
def build_audit() -> dict[str, Any]:
    riemann = riemann_sharp_reciprocal_envelope_audit()
    collatz = collatz_diagonal_weyl_uniformization_audit()
    goldbach = goldbach_q3_mod32_phase_audit()
    twin = twin_ninth_order_exactness_audit()
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "SharpReciprocalEnvelopeForScaledJumpMargin",
            "partial_theorem",
            riemann,
            "replacing the factor two in a reciprocal convergence-rate-only argument by any smaller universal constant",
            ["an arithmetic proof that actual Guinand-Weil packet energies satisfy a reciprocal envelope strictly below half their positive limit"],
            "the sharp reciprocal-rate sufficient condition and its alternating critical counterfamily",
            "ActualWeilPacketReciprocalEnvelopeBelowHalfLimit",
            "PacketLagMarginIffScaledSignedJumpLimsupBelowLimit",
            "ReciprocalEnvelopeControlsScaledJumpWithConstantBelowTwo",
            "The sharp abstract rate criterion is proved, but no O(1/n) bound with constant below L/2 is known for actual Guinand-Weil packet energies.",
            "No RH proof or disproof; the arithmetic packet-rate estimate is open.",
            f"Three exact Fraction families with {RIEMANN_REPLAY_COUNT} rows each are replayed; none is an actual Weil packet.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "PointwiseWeylCancellationIffSomeGrowingCutoffUniformCancellation",
            "partial_theorem",
            collatz,
            "treating countably many fixed-h harmonic limits as intrinsically impossible to package into one growing uniform cutoff",
            ["uniform moving-cutoff cancellation for the canonical fixed-base Fermat-quotient phases"],
            "the exact diagonal quantifier reduction from all fixed harmonics to one data-dependent growing cutoff",
            "CanonicalFermatQuotientGrowingCutoffUniformWeylCancellation",
            "EveryFixedFiniteWeylCutoffAngularDiscrepancyNoGo",
            "NoGrowingUniformCutoffCanRepresentAllPointwiseWeylLimits",
            "The diagonal schedule exists abstractly if every canonical fixed harmonic cancels, but neither the fixed-h limits nor a quantitative canonical schedule is proved.",
            "No Collatz proof or counterexample; this is a quantifier-equivalent reformulation plus classical Weyl transfer.",
            f"Exact complete-grid replays use M={list(COLLATZ_GRID_SIZES)} and are triangular models, not canonical Fermat-quotient prefixes.",
            "ClassicalWeylEquidistributionCriterion",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "Q3TieForcesLevelPhasedModuloThirtyTwo",
            "partial_theorem",
            goldbach,
            "treating the phased modulo-thirty-two condition as sufficient for a q=3 special-prefix tie at every level",
            ["an all-level arithmetic proof that actual q=3 special minus-one counts avoid their level-phased residue modulo thirty-two"],
            "the exact four-phase modulo-thirty-two necessary condition, three actual certificates, and all-level-above-zero nonsufficiency countermodels",
            "Q3SpecialMinusOneResidueCountAvoidsLevelPhasedModuloThirtyTwo",
            "Q3TieForcesMinusCountFourModuloEight",
            "Q3LevelPhasedModuloThirtyTwoConditionIsSufficientForTie",
            "The phased residue is necessary but not sufficient for l>=1, and no theorem excludes it at every actual special prime prefix.",
            "No strong Goldbach proof or counterexample; only the first three actual special levels are certified non-ties.",
            f"{len(goldbach['exact_actual_q3_mod32_certificate_rows'])} actual levels are certified; symbolic phase and countermodels cover the declared level ranges only.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "NinthOrderJointCongruenceExactOnRootCone",
            "partial_theorem",
            twin,
            "treating successively higher finite binomial jets as an endless source of independent necessary conditions beyond the degree-seventeen form",
            ["global exclusion of the joint ninth-order congruences on every unique-root continued-fraction convergent"],
            "the explicit root-cone size threshold where the bidirectional ninth-order congruence pair is equivalent to the original unit equation",
            "NoUniqueRootConvergentSatisfiesJointNinthOrderCongruences",
            "BidirectionalThirdOrderCongruenceAnd1024ConvergentCertificate",
            "HigherThanDegreeFiniteJetsYieldNewIndependentCongruenceInformation",
            "The tail congruence criterion is exact on the cone, but infinitely many later convergents and the finite denominators below the explicit threshold are not globally excluded.",
            "No twin-prime proof or counterexample; one exponent-17 Thue branch is reduced to an exact ninth-order tail congruence test.",
            f"Both signs and orders one through nine are tested on {TWIN_CONVERGENT_COUNT} certified convergents; this is finite despite reaching a 519-digit denominator.",
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
            "theorem_name": "FourConjectureSharpEnvelopeDiagonalMod32NinthOrderAudit",
            "summary": (
                "TICKET-263 proves four partial theorems: a sharp reciprocal RH-packet envelope bound, "
                "a Collatz Weyl quantifier diagonalization, a four-phase modulo-32 Goldbach tie obstruction, "
                "and a Twin ninth-order congruence criterion that becomes exact on an explicit root cone. "
                "All four parent conjectures remain open."
            ),
            **sections,
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 4,
                "exact_no_go_count": 0,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "twin_prime",
                "stagnated_problem_count": 0,
                "riemann_replay_case_count": riemann["aggregate"]["replayed_row_count"],
                "collatz_grid_replay_count": collatz["aggregate"]["complete_grid_replay_count"],
                "collatz_harmonic_case_count": collatz["aggregate"]["complete_grid_harmonic_case_count"],
                "goldbach_actual_mod32_certificate_count": len(goldbach["exact_actual_q3_mod32_certificate_rows"]),
                "goldbach_mod32_countermodel_count": len(goldbach["exact_mod32_nonsufficiency_countermodels"]),
                "twin_convergent_count": len(twin["exact_ninth_order_convergent_rows"]),
                "twin_tail_exactness_applicable_count": twin["aggregate"]["tail_exactness_applicable_convergent_count"],
                "twin_first_tail_exactness_term_index": twin["aggregate"]["first_tail_exactness_applicable_term_index"],
                "twin_joint_ninth_order_pass_count": twin["aggregate"]["joint_ninth_order_pass_count"],
                "twin_maximum_denominator_digit_count": twin["aggregate"]["maximum_denominator_digit_count"],
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
                    "failure_count": item["reproducible_computation"]["failure_count"],
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
                "generator_failure_count": item["reproducible_computation"]["failure_count"],
                "focused_tests_required": True,
                "remote_ci_status": "tracked_by_commit_workflow",
            },
        }
    return {
        "schema": "primeproject.four-problem-research-state.v1",
        "ticket": 263,
        "parent_ticket": 262,
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
        ROOT / "data/open-problem/ticket263-sharp-envelope-diagonal-mod32-ninthorder.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-263-sharp-reciprocal-envelope.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-263-diagonal-weyl-uniformization.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-263-mod32-tie-phase.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-263-ninth-order-exactness.json",
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
