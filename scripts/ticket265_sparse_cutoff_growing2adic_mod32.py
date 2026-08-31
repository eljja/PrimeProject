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

from scripts.ticket254_diagonal_weighted_reflection_thue import fraction_record, write_json
from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket258_variation_character_convergent import certified_root_continued_fraction


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket265-sparse-cutoff-growing2adic-mod32.v1"
GENERATED_AT = "2026-09-02T23:59:30+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "sparse_cutoff_growing2adic_mod32_audit"

RIEMANN_SPIKE_EXPONENTS = tuple(range(2, 18))
RIEMANN_LIMIT = Fraction(1)
RIEMANN_POSITIVE_SPIKE = Fraction(3, 4)
RIEMANN_NEGATIVE_SPIKE = Fraction(1, 2)
COLLATZ_DYADIC_MODULI = tuple(2**power for power in range(3, 12))
GOLDBACH_LEVELS = tuple(range(32))
TWIN_CONVERGENT_COUNT = 1024
TWIN_COUNTERMODEL_PARAMETERS = tuple(range(1, 33))
TWIN_COEFFICIENTS = tuple(comb(17, k) * 2 ** (k // 2) for k in range(18))


@lru_cache(maxsize=1)
def riemann_sparse_spike_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for exponent in RIEMANN_SPIKE_EXPONENTS:
        index = 2**exponent
        error = RIEMANN_POSITIVE_SPIKE / index
        next_error = -RIEMANN_NEGATIVE_SPIKE / (index + 1)
        energy = RIEMANN_LIMIT + error
        next_energy = RIEMANN_LIMIT + next_error
        jump = index * (energy - next_energy)
        lag = (index + 1) * next_energy - index * energy
        support_count = 2 * (exponent - 1)
        support_window_end = 2 ** (exponent + 1) - 1
        support_density = Fraction(support_count, support_window_end)
        verified = (
            energy > 0
            and next_energy > 0
            and index * error == RIEMANN_POSITIVE_SPIKE
            and (index + 1) * (-next_error) == RIEMANN_NEGATIVE_SPIKE
            and lag
            == RIEMANN_LIMIT
            - RIEMANN_POSITIVE_SPIKE
            - RIEMANN_NEGATIVE_SPIKE
            == Fraction(-1, 4)
            and support_count < support_window_end
        )
        failures += int(not verified)
        row = {
            "spike_exponent_k": exponent,
            "positive_spike_index_n": index,
            "energy_E_n": fraction_record(energy),
            "energy_E_n_plus_1": fraction_record(next_energy),
            "scaled_positive_error": fraction_record(index * error),
            "scaled_negative_error": fraction_record((index + 1) * (-next_error)),
            "scaled_signed_jump_J_n": fraction_record(jump),
            "lag_S_n": fraction_record(lag),
            "nonzero_support_count_through_2n_minus_1": support_count,
            "support_window_end": support_window_end,
            "support_density": fraction_record(support_density),
            "zero_error_gap_before_next_pair": index - 2,
            "row_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"{exponent}:{index}:{energy}:{next_energy}:{jump}:{lag}:"
            f"{support_count}:{support_window_end}:{support_density}:{int(verified)}\n".encode(
                "ascii"
            )
        )
    theorem = (
        "Let L>0 and P,M>=0 satisfy P+M>L. Choose k_0 so that "
        "2^k+1>M/L for k>=k_0. Define a_(2^k)=P/2^k, "
        "a_(2^k+1)=-M/(2^k+1) for k>=k_0, and a_n=0 otherwise; put "
        "E_n=L+a_n. Then E_n>0 and E_n tends to L, the exceptional set "
        "{n:a_n!=0} has natural density zero and arbitrarily long zero-error "
        "gaps, while A_+=limsup n a_n^+=P, A_-=limsup n a_n^-=M and "
        "S_(2^k)=(2^k+1)E_(2^k+1)-2^k E_(2^k)=L-P-M<0 for every k>=k_0. "
        "Hence reciprocal control on a density-one set, even with exact zero "
        "error there, cannot replace the all-index limsup envelope in TICKET-264."
    )
    proof = (
        "Positivity follows from the choice of k_0, and the two nonzero "
        "errors are O(1/n), so E_n tends to L. Up to X there are at most "
        "2(log_2 X+1) exceptional indices, hence their natural density is "
        "zero; the gaps between consecutive spike pairs grow like 2^k. "
        "On the positive and negative spike subsequences the scaled errors "
        "are exactly P and M, and they vanish elsewhere, proving the two "
        "limsups. Direct substitution cancels the nL terms and gives "
        "S_(2^k)=L-P-M. Thus the displayed family is an exact counterexample "
        "to every density-one or sparse-sampling replacement of the uniform "
        "one-sided envelope condition. It is not an actual Weil packet."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_sparse_reciprocal_spike_rows": rows,
        "algorithm": "closed-form Fraction evaluation at dyadic adjacent spike pairs",
        "complexity": "O(K) exact rational operations for the replay; the density-zero no-go is symbolic",
        "random_seed": None,
        "input_range": {
            "limit_L": str(RIEMANN_LIMIT),
            "positive_spike_P": str(RIEMANN_POSITIVE_SPIKE),
            "negative_spike_M": str(RIEMANN_NEGATIVE_SPIKE),
            "spike_exponents": list(RIEMANN_SPIKE_EXPONENTS),
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "density_one_reciprocal_control_sufficiency_refuted": True,
            "exceptional_support_density_zero_proved": True,
            "negative_lag_infinitely_often_proved": True,
            "replayed_spike_pair_count": len(rows),
            "actual_weil_one_sided_envelope_sum_below_limit_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def collatz_unbounded_cutoff_no_go_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    lower_bound = Fraction(7, 33)
    threshold = Fraction(1, 6)
    for modulus in COLLATZ_DYADIC_MODULI:
        positive_arc_odds = list(range(-modulus // 4 + 1, modulus // 4, 2))
        good_prefix = modulus
        bad_prefix = 3 * modulus // 4
        verified = (
            modulus >= 8
            and modulus & (modulus - 1) == 0
            and len(positive_arc_odds) == modulus // 4
            and all(residue % 2 for residue in positive_arc_odds)
            and positive_arc_odds == [-value for value in reversed(positive_arc_odds)]
            and lower_bound > threshold
            and bad_prefix >= 6
        )
        failures += int(not verified)
        row = {
            "dyadic_grid_modulus_q": modulus,
            "complete_grid_good_prefix_N": good_prefix,
            "exact_good_cutoff_K_N": modulus - 1,
            "positive_arc_bad_prefix_N": bad_prefix,
            "positive_arc_new_odd_root_count": len(positive_arc_odds),
            "first_positive_arc_odd_residue": positive_arc_odds[0],
            "last_positive_arc_odd_residue": positive_arc_odds[-1],
            "root_sum_magnitude_identity": "csc(2*pi/q)",
            "exact_rational_lower_bound_for_abs_W_N_1": fraction_record(lower_bound),
            "harmonic_six_threshold": fraction_record(threshold),
            "harmonic_six_fails": lower_bound > threshold,
            "bad_prefix_cutoff_upper_bound": 5,
            "row_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"{modulus}:{good_prefix}:{modulus - 1}:{bad_prefix}:"
            f"{positive_arc_odds[0]}:{positive_arc_odds[-1]}:"
            f"{len(positive_arc_odds)}:{lower_bound}:{threshold}:{int(verified)}\n".encode(
                "ascii"
            )
        )
    theorem = (
        "There is an explicit sequence x_j in R/Z whose TICKET-264 cutoff "
        "K_N is unbounded but does not tend to infinity. Start with a complete "
        "four-point grid. For each dyadic q=2^r, r>=3, regard the preceding "
        "q/2-grid as the even q-th roots, append first the q/4 odd q-th roots "
        "with arguments in (-pi/2,pi/2), and then append the remaining odd "
        "roots. At N=q the prefix is the complete q-grid and K_q=q-1. At "
        "N=3q/4, |W_N(1)|=1/[N sin(2*pi/q)]>7/33>1/6, so H=6 is not "
        "admissible and K_N<=5. Consequently limsup K_N=infinity while "
        "liminf K_N<=5. Arbitrarily large finite cutoff certificates therefore "
        "do not imply divergence or pointwise Weyl cancellation."
    )
    proof = (
        "The recursive enumeration is consistent because a complete q/2-grid "
        "is exactly the even part of the q-grid. Thus each power-of-two endpoint "
        "is a complete grid, and the root-sum dichotomy gives K_q=q-1. For the "
        "intermediate prefix the previous grid has first-harmonic sum zero. "
        "The appended odd residues form a symmetric geometric progression of "
        "q/4 terms whose sum has magnitude csc(2*pi/q). Since sin x<x and "
        "pi<22/7, this magnitude is greater than 7q/44; division by N=3q/4 "
        "gives |W_N(1)|>7/33>1/6. Hence E_N(6)>1/6 and, because admissible "
        "cutoffs form an initial segment, K_N<=5. This exact construction "
        "refutes only the weakening 'K_N is unbounded'; it is not a canonical "
        "Fermat-quotient sequence."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_dyadic_good_bad_prefix_rows": rows,
        "algorithm": "exact dyadic residue enumeration plus rational bounds sin(x)<x and pi<22/7",
        "complexity": "O(sum q) integer checks in the replay; the infinite construction and geometric-sum identity are symbolic",
        "random_seed": None,
        "input_range": {"dyadic_grid_moduli": list(COLLATZ_DYADIC_MODULI)},
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "unbounded_cutoff_sufficiency_refuted": True,
            "cutoff_limsup_infinite_proved": True,
            "cutoff_liminf_at_most_five_proved": True,
            "dyadic_good_bad_prefix_replay_count": len(rows),
            "canonical_fermat_quotient_threshold_cutoff_diverges_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def _tie_count(level: int) -> int:
    return 3 ** (6 * level + 3) + 1


@lru_cache(maxsize=1)
def goldbach_growing_two_adic_audit() -> dict[str, Any]:
    threshold_rows: list[dict[str, Any]] = []
    countermodels: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for level in GOLDBACH_LEVELS:
        middle = _tie_count(level)
        exponent = middle.bit_length()
        modulus = 1 << exponent
        lower_modulus = 1 << (exponent - 1)
        n1 = middle - lower_modulus
        n2 = middle + lower_modulus
        verified = (
            lower_modulus <= middle < modulus
            and n1 >= 0
            and n1 + n2 == 2 * middle
            and n1 != n2
            and n2 % lower_modulus == middle % lower_modulus
        )
        failures += int(not verified)
        threshold_rows.append(
            {
                "level_l": level,
                "tie_count_M_l": str(middle),
                "least_decisive_exponent_m_l": exponent,
                "least_decisive_modulus_two_to_m_l": str(modulus),
                "largest_insufficient_modulus_two_to_m_l_minus_1": str(lower_modulus),
                "threshold_inequality_verified": lower_modulus <= middle < modulus,
                "row_verified": verified,
            }
        )
        countermodels.append(
            {
                "level_l": level,
                "insufficient_exponent_m_l_minus_1": exponent - 1,
                "tie_count_M_l": str(middle),
                "abstract_N_1": str(n1),
                "abstract_N_2": str(n2),
                "common_residue_mod_two_to_m_l_minus_1": middle % lower_modulus,
                "same_total_as_tie": n1 + n2 == 2 * middle,
                "non_tie": n1 != n2,
                "row_verified": verified,
            }
        )
        transcript.update(
            f"{level}:{middle}:{exponent}:{modulus}:{lower_modulus}:"
            f"{n1}:{n2}:{int(verified)}\n".encode("ascii")
        )

    source_path = ROOT / "data/open-problem/goldbach/gb-ticket-260-q3-prime-race-reduction.json"
    source_bytes = source_path.read_bytes()
    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
    source_payload = json.loads(source_bytes)
    source_rows = source_payload["reproducible_computation"]["exact_q3_prime_race_certificate_rows"]
    actual_rows: list[dict[str, Any]] = []
    for source in source_rows:
        level = int(source["level_l"])
        if level > 2:
            continue
        counts = [int(value) for value in source["actual_residue_counts"]]
        middle = _tie_count(level)
        exponent = middle.bit_length()
        modulus = 1 << exponent
        actual_n1, actual_n2 = counts[1], counts[2]
        mismatch = actual_n2 % modulus != middle % modulus
        verified = (
            source["certificate_verified"]
            and actual_n1 + actual_n2 == 2 * middle
            and actual_n1 - actual_n2 == int(source["mod_3_prime_race_difference_N1_minus_N2"])
            and actual_n1 != actual_n2
            and mismatch
        )
        failures += int(not verified)
        actual_rows.append(
            {
                "level_l": level,
                "least_decisive_exponent_m_l": exponent,
                "least_decisive_modulus_two_to_m_l": str(modulus),
                "actual_N_1": actual_n1,
                "actual_N_2": actual_n2,
                "actual_minus_tie": actual_n2 - middle,
                "actual_N_2_residue": actual_n2 % modulus,
                "tie_residue": middle % modulus,
                "decisive_residue_mismatch": mismatch,
                "row_verified": verified,
            }
        )
        transcript.update(
            f"actual:{level}:{actual_n1}:{actual_n2}:{middle}:{exponent}:"
            f"{modulus}:{int(mismatch)}:{int(verified)}\n".encode("ascii")
        )
    theorem = (
        "Let M>=1 and let N_1,N_2 be nonnegative integers with N_1+N_2=2M. "
        "For a fixed m>=1, the congruence N_2 congruent to M modulo 2^m "
        "forces N_1=N_2=M for every such pair if and only if 2^m>M. "
        "Consequently, for M_l=3^(6l+3)+1 the least decisive exponent is "
        "m_l=bit_length(M_l): the total-count constraint together with "
        "N_2 congruent to M_l modulo 2^m_l is exactly equivalent to the tie, "
        "whereas exponent m_l-1 always admits the explicit non-tie pair "
        "(M_l-2^(m_l-1),M_l+2^(m_l-1)). This growing two-adic signature is "
        "sharp; it does not prove that the actual prime counts avoid the tie."
    )
    proof = (
        "The sum condition gives N_1=M-d and N_2=M+d for the integer "
        "d=N_2-M, and nonnegativity gives |d|<=M. The congruence says 2^m "
        "divides d. If 2^m>M, the only multiple in [-M,M] is d=0, proving "
        "the tie. If 2^m<=M, taking d=2^m gives a nonnegative non-tie pair "
        "with the same total and residue, proving necessity and sharpness. "
        "By definition 2^(m_l-1)<=M_l<2^m_l, so the specialization follows. "
        "The finite replay imports only three already certified actual q=3 "
        "levels from TICKET-260 and checks their decisive residues; no finite "
        "set of levels establishes the required all-level avoidance."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_growing_modulus_threshold_rows": threshold_rows,
        "sharp_lower_exponent_nontie_countermodels": countermodels,
        "inherited_actual_decisive_residue_rows": actual_rows,
        "inherited_source": {
            "path": source_path.relative_to(ROOT).as_posix(),
            "sha256": source_sha256,
            "ticket": 260,
        },
        "algorithm": "exact bit-length threshold construction plus hash-pinned replay of three TICKET-260 prime-count certificates",
        "complexity": "O(L) exact integer operations for L declared symbolic levels; no new prime sieve",
        "random_seed": None,
        "input_range": {
            "symbolic_level_min": min(GOLDBACH_LEVELS),
            "symbolic_level_max": max(GOLDBACH_LEVELS),
            "inherited_actual_levels": [row["level_l"] for row in actual_rows],
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "sharp_growing_modulus_threshold_proved": True,
            "least_decisive_exponent_proved": True,
            "symbolic_threshold_replay_count": len(threshold_rows),
            "lower_exponent_countermodel_count": len(countermodels),
            "inherited_actual_decisive_certificate_count": len(actual_rows),
            "actual_q3_special_prime_race_nonvanishing_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def twin_subthreshold_head_audit() -> dict[str, Any]:
    _, source_rows, lower, upper = certified_root_continued_fraction(
        TWIN_HEAD_CERTIFICATE_COUNT
    )
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    previous_denominator = 0
    subthreshold_count = 0
    first_above_index: int | None = None
    for source in source_rows:
        index = source["term_index"]
        numerator = int(source["convergent_numerator"])
        denominator = int(source["convergent_denominator"])
        coefficient = b1_coefficient_form(numerator, denominator)
        nondecreasing = denominator >= previous_denominator
        strict_after_first = index <= 1 or denominator > previous_denominator
        previous_denominator = denominator
        at_or_below = denominator <= TWIN_EXACTNESS_THRESHOLD
        if at_or_below:
            subthreshold_count += 1
        elif first_above_index is None:
            first_above_index = index
        direct_unit_free = abs(coefficient) != 1
        verified = nondecreasing and strict_after_first and (direct_unit_free if at_or_below else True)
        failures += int(not verified)
        digest = hashlib.sha256(str(coefficient).encode("ascii")).hexdigest()
        rows.append(
            {
                "term_index": index,
                "partial_quotient": source["partial_quotient"],
                "convergent_numerator": str(numerator),
                "convergent_denominator": str(denominator),
                "at_or_below_exactness_threshold": at_or_below,
                "B_1_value": str(coefficient),
                "B_1_value_sha256": digest,
                "direct_unit_free": direct_unit_free,
                "denominator_nondecreasing": nondecreasing,
                "row_verified": verified,
            }
        )
        transcript.update(
            f"{index}:{source['partial_quotient']}:{numerator}:{denominator}:"
            f"{coefficient}:{int(at_or_below)}:{int(direct_unit_free)}:{int(verified)}\n".encode("ascii")
        )
    crossing_verified = (
        subthreshold_count == 38
        and first_above_index == 38
        and int(rows[37]["convergent_denominator"]) == 110221790993960069
        and int(rows[38]["convergent_denominator"]) == 309742427372962732
        and all(row["direct_unit_free"] for row in rows[:38])
    )
    failures += int(not crossing_verified)
    theorem = (
        "Let p_n/q_n be the certified continued-fraction convergents to the "
        "unique real root used by the degree-17 Twin branch, and put "
        "V_0=188580743973175296. Every convergent with q_n<=V_0 is among "
        "n=0,...,37, and none satisfies B_1(p_n,q_n)=+1 or -1. The next "
        "denominator is q_38=309742427372962732>V_0. Thus the entire finite "
        "subthreshold head is closed; only the infinite n>=38 tail remains."
    )
    proof = (
        "The certified rational root bracket fixes the first 39 continued-"
        "fraction terms. Exact recurrence gives nondecreasing denominators "
        "and strict increase after the initial modulus-one duplication. "
        "Direct integer evaluation of B_1 on indices 0 through 37 gives no "
        "unit value. Since q_37=110221790993960069<=V_0<q_38 and all later "
        "continued-fraction denominators strictly increase, there can be no "
        "additional subthreshold convergent. TICKET-263's ninth-order "
        "equivalence applies in the later root-cone tail, but this theorem "
        "does not exclude infinitely many later congruence passes."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "coefficient_vector_a_0_through_a_17": list(TWIN_COEFFICIENTS),
        "ninth_order_exactness_threshold_V_0": str(TWIN_EXACTNESS_THRESHOLD),
        "exact_head_and_crossing_rows": rows,
        "final_exact_root_bracket": {
            "lower": fraction_record(lower),
            "upper": fraction_record(upper),
        },
        "algorithm": "certified rational continued fraction plus exact degree-17 integer evaluation through the first threshold crossing",
        "complexity": "O(K*17) exact big-integer terms for K=39",
        "random_seed": None,
        "input_range": {"certified_convergent_count": TWIN_HEAD_CERTIFICATE_COUNT},
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "all_subthreshold_unique_root_convergents_unit_free_proved": True,
            "subthreshold_convergent_count": subthreshold_count,
            "first_above_threshold_term_index": first_above_index,
            "last_subthreshold_denominator": rows[37]["convergent_denominator"],
            "first_above_threshold_denominator": rows[38]["convergent_denominator"],
            "crossing_verified": crossing_verified,
            "all_unique_root_convergents_excluded": False,
            "twin_prime_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def twin_mod32_diagonal_filter_audit() -> dict[str, Any]:
    _, source_rows, lower, upper = certified_root_continued_fraction(TWIN_CONVERGENT_COUNT)
    rows: list[dict[str, Any]] = []
    valuation_rows: list[dict[str, Any]] = []
    countermodels: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0

    for k in range(2, 18):
        binomial = comb(17, k)
        coefficient_valuation = (k // 2) + ((binomial & -binomial).bit_length() - 1)
        total_valuation = coefficient_valuation + k
        verified = total_valuation >= 5
        failures += int(not verified)
        valuation_rows.append(
            {
                "term_index_k": k,
                "coefficient_a_k": TWIN_COEFFICIENTS[k],
                "two_adic_valuation_of_a_k": coefficient_valuation,
                "minimum_two_adic_valuation_when_v_even": total_valuation,
                "vanishes_mod_32": verified,
            }
        )
        transcript.update(
            f"valuation:{k}:{TWIN_COEFFICIENTS[k]}:{coefficient_valuation}:"
            f"{total_valuation}:{int(verified)}\n".encode("ascii")
        )

    for parameter in TWIN_COUNTERMODEL_PARAMETERS:
        plus_u, plus_v = 1, 32 * parameter
        minus_u, minus_v = -1, -32 * parameter
        plus_value = b1_coefficient_form(plus_u, plus_v)
        minus_value = b1_coefficient_form(minus_u, minus_v)
        verified = (
            gcd(plus_u, plus_v) == 1
            and (plus_u + plus_v) % 32 == 1
            and (minus_u + minus_v) % 32 == 31
            and plus_value > 1
            and minus_value == -plus_value < -1
        )
        failures += int(not verified)
        countermodels.append(
            {
                "parameter_t": parameter,
                "plus_pair_u_v": [plus_u, plus_v],
                "plus_diagonal_residue_mod_32": (plus_u + plus_v) % 32,
                "plus_B_1_value": str(plus_value),
                "minus_pair_u_v": [minus_u, minus_v],
                "minus_diagonal_residue_mod_32": (minus_u + minus_v) % 32,
                "minus_B_1_value": str(minus_value),
                "both_primitive": gcd(plus_u, plus_v) == gcd(minus_u, minus_v) == 1,
                "necessary_filter_passes_but_unit_fails": verified,
                "row_verified": verified,
            }
        )
        transcript.update(
            f"countermodel:{parameter}:{plus_value}:{minus_value}:{int(verified)}\n".encode("ascii")
        )

    even_denominator_count = 0
    plus_filter_count = 0
    minus_filter_count = 0
    either_filter_count = 0
    later_either_filter_count = 0
    for source in source_rows:
        index = source["term_index"]
        numerator = int(source["convergent_numerator"])
        denominator = int(source["convergent_denominator"])
        coefficient = b1_coefficient_form(numerator, denominator)
        primitive = gcd(numerator, denominator) == 1
        denominator_even = denominator % 2 == 0
        plus_filter = denominator_even and (numerator + denominator) % 32 == 1
        minus_filter = denominator_even and (numerator + denominator) % 32 == 31
        either_filter = plus_filter or minus_filter
        even_denominator_count += int(denominator_even)
        plus_filter_count += int(plus_filter)
        minus_filter_count += int(minus_filter)
        either_filter_count += int(either_filter)
        later_either_filter_count += int(either_filter and index >= 38)
        unit_implies_filter = abs(coefficient) != 1 or (
            denominator_even and (numerator + denominator) % 32 == coefficient % 32
        )
        verified = primitive and unit_implies_filter
        failures += int(not verified)
        coefficient_digest = hashlib.sha256(str(coefficient).encode("ascii")).hexdigest()
        rows.append(
            {
                "term_index": index,
                "u_mod_32": numerator % 32,
                "v_mod_32": denominator % 32,
                "denominator_even": denominator_even,
                "plus_diagonal_filter": plus_filter,
                "minus_diagonal_filter": minus_filter,
                "either_sign_filter": either_filter,
                "later_than_subthreshold_head": index >= 38,
                "B_1_value_sha256": coefficient_digest,
                "actual_unit_value": coefficient if abs(coefficient) == 1 else None,
                "unit_implies_mod32_filter": unit_implies_filter,
                "row_verified": verified,
            }
        )
        transcript.update(
            f"convergent:{index}:{numerator % 32}:{denominator % 32}:"
            f"{int(denominator_even)}:{int(plus_filter)}:{int(minus_filter)}:"
            f"{coefficient_digest}:{int(verified)}\n".encode("ascii")
        )

    theorem = (
        "Let B_1(u,v)=sum_(k=0)^17 C(17,k)2^floor(k/2)u^(17-k)v^k. "
        "If gcd(u,v)=1 and B_1(u,v)=epsilon in {+1,-1}, then u is odd, v is "
        "even, and u+v is congruent to epsilon modulo 32. This necessary "
        "diagonal filter is not sufficient: for every t>=1, (1,32t) passes "
        "the +1 filter but B_1(1,32t)>1, while (-1,-32t) passes the -1 "
        "filter but B_1(-1,-32t)<-1. On the first 1024 certified unique-root "
        "convergents the filter leaves only 35 candidates, 33 of them in the "
        "still-open n>=38 tail."
    )
    proof = (
        "Modulo 2, an even u and odd v make every term even, while odd u and "
        "odd v leave only k=0,1 and give u+v=0; a unit therefore requires u "
        "odd and v even. For odd u, u^16=1 modulo 32. The k=0 term is u, "
        "the k=1 term is 17u^16v congruent to v because 16v is divisible by "
        "32, and every k>=2 term has two-adic valuation at least five. Hence "
        "B_1(u,v) is congruent to u+v modulo 32. Positivity of all coefficients "
        "gives B_1(1,32t)>1, and degree-17 homogeneity gives the negative "
        "countermodels. The convergent counts are a finite exact replay, not "
        "an exclusion of the infinite continued-fraction tail."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "coefficient_vector_a_0_through_a_17": list(TWIN_COEFFICIENTS),
        "exact_two_adic_valuation_rows": valuation_rows,
        "explicit_filter_insufficiency_countermodels": countermodels,
        "certified_convergent_mod32_filter_rows": rows,
        "final_exact_root_bracket": {
            "lower": fraction_record(lower),
            "upper": fraction_record(upper),
        },
        "algorithm": "symbolic parity/mod-32 reduction plus exact modular scan and hashed B_1 evaluation of certified convergents",
        "complexity": "O(K*17) exact big-integer operations for K=1024",
        "random_seed": None,
        "input_range": {
            "certified_convergent_count": TWIN_CONVERGENT_COUNT,
            "countermodel_parameter_min": min(TWIN_COUNTERMODEL_PARAMETERS),
            "countermodel_parameter_max": max(TWIN_COUNTERMODEL_PARAMETERS),
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "primitive_unit_implies_mod32_diagonal_filter_proved": True,
            "mod32_diagonal_filter_sufficiency_refuted": True,
            "valuation_row_count": len(valuation_rows),
            "countermodel_pair_count": len(countermodels),
            "even_denominator_count": even_denominator_count,
            "plus_filter_count": plus_filter_count,
            "minus_filter_count": minus_filter_count,
            "either_sign_filter_count": either_filter_count,
            "later_either_sign_filter_count": later_either_filter_count,
            "all_unique_root_convergents_excluded": False,
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
    *,
    external_name: str | None = None,
) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T264", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T265", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-CERT265", "label": f"{theorem_name}ExactReplay", "status": "computed_finite"},
        {"id": f"{code}-REJECT265", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN265", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T264", f"{code}-T265"],
        [f"{code}-T265", f"{code}-CERT265"],
        [f"{code}-T265", f"{code}-REJECT265"],
        [f"{code}-T265", f"{code}-OPEN265"],
    ]
    if external_name:
        nodes.append({"id": f"{code}-EXT265", "label": external_name, "status": "external_theorem"})
        edges.append([f"{code}-EXT265", f"{code}-T265"])
    return {
        "nodes": nodes,
        "edges": edges,
        "resolution_path": [f"{code}-T264", f"{code}-T265", f"{code}-OPEN265"],
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
        "ticket_id": f"{code}-TICKET-265",
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
            code, prior_name, theorem_name, rejected_name, next_lemma,
            external_name=external_name,
        ),
        "claim_boundary": claim_boundary,
    }


@lru_cache(maxsize=1)
def build_audit_legacy_ticket264_template() -> dict[str, Any]:
    riemann = riemann_asymmetric_envelope_audit()
    collatz = collatz_threshold_cutoff_audit()
    goldbach = goldbach_fixed_two_adic_no_go_audit()
    twin = twin_subthreshold_head_audit()
    sections = {
        "riemann": section(
            "riemann", "RH", "AsymmetricReciprocalEnvelopeForScaledJumpMargin", "partial_theorem", riemann,
            "treating the symmetric max-envelope threshold A<L/2 as the sharpest rate-only formulation",
            ["an arithmetic proof that actual Guinand-Weil packet energies satisfy A_++A_-<L"],
            "the strictly weaker sharp one-sided envelope-sum criterion and its asymmetric critical family",
            "ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit",
            "SharpReciprocalEnvelopeForScaledJumpMargin",
            "NoAsymmetricImprovementOverTheSymmetricFactorTwoBound",
            "The abstract criterion is now sharper, but neither one-sided reciprocal envelope is bounded for actual Guinand-Weil packets.",
            "No RH proof or disproof; the missing step is an arithmetic packet estimate, not another sequence inequality.",
            f"Three abstract Fraction families and {riemann['aggregate']['replayed_row_count']} rows are checked; none is an actual Weil packet.",
        ),
        "collatz": section(
            "collatz", "CO", "PointwiseWeylCancellationIffExplicitThresholdCutoffDiverges", "partial_theorem", collatz,
            "claiming that the TICKET-263 diagonal cutoff can only be existential and cannot be selected from the finite prefix data",
            ["a proof that the explicit threshold cutoff diverges for canonical fixed-base Fermat-quotient phases"],
            "the exact maximal threshold functional K_N, equivalent to all fixed-h cancellation",
            "CanonicalFermatQuotientThresholdCutoffDiverges",
            "PointwiseWeylCancellationIffSomeGrowingCutoffUniformCancellation",
            "EveryDataDefinedGrowingCutoffFailsToEncodePointwiseWeylCancellation",
            "K_N is explicit and finite-data-defined, but its divergence is not proved for the canonical Fermat-quotient sequence.",
            "No Collatz proof or counterexample; this is a computable quantifier reformulation without a canonical arithmetic estimate.",
            f"Exact complete grids M={list(COLLATZ_GRID_SIZES)} give {collatz['aggregate']['harmonic_threshold_case_count']} threshold checks; they are not canonical prefixes.",
        ),
        "goldbach": section(
            "goldbach", "GB", "EveryFixedTwoAdicTieSignatureHasNonTieCountModels", "exact_no_go", goldbach,
            "climbing to any one fixed power-of-two congruence and treating the tie residue plus total as sufficient",
            ["noncongruential control of the q=3 special prime-race integer gap"],
            "the exact all-m phase periods and universal shifted-count countermodels",
            "Q3SpecialPrimeRaceAbsoluteGapAtLeastTwo",
            "Q3TieForcesLevelPhasedModuloThirtyTwo",
            "SomeFixedTwoAdicTieSignatureAndTotalSufficeToDecideEverySpecialTie",
            "Every fixed two-adic congruence loses the integer displacement by a multiple of its modulus; an all-level nonzero prime-race estimate is still absent.",
            "No strong Goldbach proof or counterexample; the no-go concerns only a fixed-modulus information route and uses abstract count models.",
            f"Periods are replayed for m=1..16 and {goldbach['aggregate']['countermodel_count']} valid (m,l) countermodels with l=0..15; the theorem itself is symbolic for all m,l.",
        ),
        "twin_prime": section(
            "twin-prime", "TP", "AllSubthresholdUniqueRootConvergentsAreUnitFree", "partial_theorem", twin,
            "leaving the finitely many unique-root convergents below the TICKET-263 exactness threshold as an unresolved global subcase",
            ["global exclusion of joint ninth-order congruences on every later unique-root convergent"],
            "the certified first threshold crossing and exact unit-free evaluation of the complete finite head",
            "NoLaterUniqueRootConvergentSatisfiesJointNinthOrderCongruences",
            "NinthOrderJointCongruenceExactOnRootCone",
            "SomeAdditionalSubthresholdUniqueRootConvergentMayRemainBeyondTheCertifiedHead",
            "The finite q<=V_0 head is closed, but infinitely many q>V_0 convergents remain and no recurrence excludes all ninth-order passes.",
            "No twin-prime proof or counterexample; only one degree-17 branch's finite continued-fraction head is completely closed.",
            "The first 39 certified convergents locate q_37<=V_0<q_38 and evaluate all 38 subthreshold B_1 values exactly.",
        ),
    }
    total_failures = sum(item["reproducible_computation"]["failure_count"] for item in sections.values())
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureAsymmetricThresholdFixedTwoAdicHeadAudit",
            "summary": (
                "TICKET-264 proves three partial theorems and one exact route no-go: a sharp asymmetric RH-packet envelope, "
                "an explicit Collatz Weyl threshold-cutoff equivalence, failure of every fixed two-adic Goldbach tie signature, "
                "and complete closure of the Twin degree-17 subthreshold convergent head. All parent conjectures remain open."
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
                "deep_focus_problem": "riemann",
                "stagnated_problem_count": 0,
                "riemann_replay_case_count": riemann["aggregate"]["replayed_row_count"],
                "collatz_grid_replay_count": collatz["aggregate"]["complete_grid_replay_count"],
                "collatz_harmonic_threshold_case_count": collatz["aggregate"]["harmonic_threshold_case_count"],
                "goldbach_phase_period_replay_count": goldbach["aggregate"]["phase_period_replay_count"],
                "goldbach_fixed_modulus_countermodel_count": goldbach["aggregate"]["countermodel_count"],
                "twin_head_certificate_row_count": len(twin["exact_head_and_crossing_rows"]),
                "twin_subthreshold_convergent_count": twin["aggregate"]["subthreshold_convergent_count"],
                "twin_first_above_threshold_term_index": twin["aggregate"]["first_above_threshold_term_index"],
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
                "bounded_result": {"audit_ref": f"#/{AUDIT_KEY}/{key}", "failure_count": item["reproducible_computation"]["failure_count"]},
                "discarded_route": item["route_decision"]["discard"],
                "parked_routes": item["route_decision"]["parked"],
                "remaining_gap": item["logical_limit"],
                "stagnation_count": item["stagnation_count"],
                "candidate_theorem": item["route_decision"]["next_single_lemma"],
            }
            for key, item in sections.items()
        ],
    }


@lru_cache(maxsize=1)
def build_audit() -> dict[str, Any]:
    riemann = riemann_sparse_spike_audit()
    collatz = collatz_unbounded_cutoff_no_go_audit()
    goldbach = goldbach_growing_two_adic_audit()
    twin = twin_mod32_diagonal_filter_audit()
    sections = {
        "riemann": section(
            "riemann", "RH", "DensityOneReciprocalControlCannotReplaceLimsupEnvelope", "exact_no_go", riemann,
            "using density-one or sparse packet-index reciprocal control as a sufficient substitute for the all-index envelope",
            ["an arithmetic proof that actual Guinand-Weil packet energies satisfy A_++A_-<L"],
            "TICKET-264's all-index one-sided reciprocal limsup envelope sum",
            "ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit",
            "AsymmetricReciprocalEnvelopeForScaledJumpMargin",
            "DensityOneReciprocalControlSufficesForPositiveScaledLag",
            "The sparse sequence is an exact abstract counterexample, but no theorem transfers its spikes to actual Guinand-Weil packet energies.",
            "No RH proof or disproof: the no-go eliminates a weakening, while the actual all-index arithmetic envelope remains unproved.",
            f"The Fraction replay checks {len(riemann['exact_sparse_reciprocal_spike_rows'])} dyadic spike pairs k=2..17; the symbolic construction is infinite but is not an actual Weil packet.",
        ),
        "collatz": section(
            "collatz", "CO", "UnboundedExplicitThresholdCutoffDoesNotImplyDivergence", "exact_no_go", collatz,
            "replacing K_N to infinity by the weaker assertion that K_N is merely unbounded or large on a sparse subsequence",
            ["a canonical fixed-base Fermat-quotient estimate ruling out every bounded subsequence of K_N"],
            "TICKET-264's exact equivalence requiring full-sequence divergence K_N to infinity",
            "CanonicalFermatQuotientThresholdCutoffHasNoBoundedSubsequence",
            "PointwiseWeylCancellationIffExplicitThresholdCutoffDiverges",
            "UnboundedExplicitThresholdCutoffImpliesPointwiseWeylCancellation",
            "The recursive dyadic-root sequence is exact but is not the canonical Fermat-quotient sequence arising from the Collatz reduction.",
            "No Collatz proof or counterexample: limsup K_N=infinity is separated sharply from K_N to infinity, and the canonical no-bounded-subsequence estimate is open.",
            f"The replay checks {len(collatz['exact_dyadic_good_bad_prefix_rows'])} powers q=8..2048 using exact integer structure and rational bounds; it certifies the construction, not canonical phases.",
        ),
        "goldbach": section(
            "goldbach", "GB", "GrowingTwoAdicTieSignatureIsSharpAndDecisive", "partial_theorem", goldbach,
            "interpreting TICKET-264's fixed-modulus no-go as excluding every level-dependent growing two-adic tie signature",
            ["an all-level proof that the actual q=3 residue count N_2(l) avoids M_l modulo 2^m_l"],
            "the least level-dependent modulus 2^m_l>M_l, which decides the abstract tie exactly",
            "Q3ActualMinusCountAvoidsLeastDecisiveTwoAdicTieResidue",
            "EveryFixedTwoAdicTieSignatureHasNonTieCountModels",
            "NoGrowingTwoAdicSignatureCanDecideTheTieFromTheTotal",
            "The criterion decides equality for abstract nonnegative count pairs, but it supplies no analytic control of the actual prime-residue displacement.",
            "No strong Goldbach proof or counterexample: exact decisiveness is established, while actual avoidance of the decisive residue remains an all-level prime-race problem.",
            f"Levels l=0..31 receive exact threshold/countermodel checks; only {goldbach['aggregate']['inherited_actual_decisive_certificate_count']} actual levels are hash-pinned from TICKET-260.",
        ),
        "twin_prime": section(
            "twin-prime", "TP", "PrimitiveTwinUnitSolutionsObeyMod32DiagonalFilter", "partial_theorem", twin,
            "treating the primitive parity and mod-32 diagonal filter as sufficient for B_1(u,v)=+/-1",
            ["joint ninth-order exclusion for every later unique-root convergent that survives the mod-32 filter"],
            "the cheap mod-32 necessary filter as a front end to TICKET-263's exact ninth-order test",
            "EveryLaterMod32FilterPassFailsJointNinthOrderCongruences",
            "AllSubthresholdUniqueRootConvergentsAreUnitFree",
            "PrimitiveMod32DiagonalFilterIsSufficientForTwinUnitValues",
            "The congruence is only necessary; explicit infinite primitive countermodels pass it, and the later continued-fraction tail remains infinite.",
            "No twin-prime proof or counterexample: the new local filter narrows certified candidates but does not globally exclude the degree-17 unit equation.",
            f"Exactly {len(twin['certified_convergent_mod32_filter_rows'])} certified convergents and {len(twin['explicit_filter_insufficiency_countermodels'])} paired countermodels are replayed; later filter survivors are not thereby excluded.",
        ),
    }
    total_failures = sum(item["reproducible_computation"]["failure_count"] for item in sections.values())
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureSparseCutoffGrowingTwoAdicMod32Audit",
            "summary": (
                "TICKET-265 proves two exact route no-go theorems and two partial theorems: density-one reciprocal control cannot replace the RH all-index envelope; unbounded Collatz threshold cutoffs cannot replace divergence; a sharp growing two-adic modulus decides abstract Goldbach ties; and primitive Twin unit solutions obey a necessary but insufficient mod-32 diagonal filter. All four parent conjectures remain open."
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
                "deep_focus_problem": "collatz",
                "stagnated_problem_count": 0,
                "riemann_sparse_spike_replay_count": len(riemann["exact_sparse_reciprocal_spike_rows"]),
                "collatz_dyadic_good_bad_replay_count": len(collatz["exact_dyadic_good_bad_prefix_rows"]),
                "goldbach_symbolic_threshold_replay_count": goldbach["aggregate"]["symbolic_threshold_replay_count"],
                "goldbach_lower_exponent_countermodel_count": goldbach["aggregate"]["lower_exponent_countermodel_count"],
                "goldbach_inherited_actual_certificate_count": goldbach["aggregate"]["inherited_actual_decisive_certificate_count"],
                "twin_certified_convergent_count": len(twin["certified_convergent_mod32_filter_rows"]),
                "twin_either_sign_filter_count": twin["aggregate"]["either_sign_filter_count"],
                "twin_later_either_sign_filter_count": twin["aggregate"]["later_either_sign_filter_count"],
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
                "bounded_result": {"audit_ref": f"#/{AUDIT_KEY}/{key}", "failure_count": item["reproducible_computation"]["failure_count"]},
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
    previous = json.loads((ROOT / "data/open-problem/four-problem-research-state.json").read_text(encoding="utf-8"))
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
            "unresolved_dependencies": [node["label"] for node in item["proof_dag"]["nodes"] if node["status"] in {"assumption", "heuristic", "open"}],
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
        "ticket": 265,
        "parent_ticket": 264,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "collatz",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(ROOT / "data/open-problem/ticket265-sparse-cutoff-growing2adic-mod32.json", audit)
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-265-density-one-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-265-unbounded-cutoff-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-265-growing-two-adic-threshold.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-265-mod32-diagonal-filter.json",
    }
    for key, path in paths.items():
        write_json(path, {"schema": SCHEMA, "generated_at": GENERATED_AT, "status": STATUS, **root[key]})
    write_json(ROOT / "data/open-problem/four-problem-research-state.json", build_research_state(audit))


if __name__ == "__main__":
    payload = build_audit()
    write_outputs(payload)
    machine = payload[AUDIT_KEY]["machine_audit"]
    print(json.dumps(machine, ensure_ascii=False, indent=2))
