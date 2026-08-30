from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket254_diagonal_weighted_reflection_thue import (
    fraction_record,
    is_prime,
    write_json,
)
from scripts.ticket256_cesaro_kernel_qdiv_gl2 import cyclic_binomial_coefficients
from scripts.ticket258_variation_character_convergent import (
    certified_root_continued_fraction,
)
from scripts.ticket259_critical_alignment_compatibility_local import (
    LehmerPrimeCounter,
    combinatorial_residue_prime_counts,
    direct_segmented_residue_prime_counts,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket260-weighted-equidistribution-primerace-variablemod.v1"
GENERATED_AT = "2026-08-31T23:30:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "weighted_equidistribution_primerace_variablemod_audit"

RIEMANN_LEVELS = tuple(range(1, 17))
COLLATZ_TERM_COUNT = 64
COLLATZ_FIXED_MODULI = tuple(range(2, 17))
GOLDBACH_LEVELS = (0, 1, 2)
GOLDBACH_SEGMENT_ODD_COUNT = 5_000_000
TWIN_CONVERGENT_COUNT = 256


def is_positive_power_of_two(value: int) -> bool:
    return value >= 2 and value & (value - 1) == 0


def summable_demo_energy(dimension: int) -> Fraction:
    if dimension < 1:
        raise ValueError("packet dimension must be positive")
    transition = dimension - 1
    if is_positive_power_of_two(transition):
        return Fraction(transition**3 - 1, transition**3)
    return Fraction(1)


def summable_demo_lag(index: int) -> Fraction:
    if index < 0:
        raise ValueError("lag index must be nonnegative")
    return (index + 1) * summable_demo_energy(index + 1) - index * summable_demo_energy(index)


@lru_cache(maxsize=1)
def riemann_weighted_variation_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    partial_weighted_variation = Fraction(0)
    for level in RIEMANN_LEVELS:
        transition = 2**level
        drop = Fraction(1, transition**3)
        weighted_drop = transition * drop
        partial_weighted_variation += weighted_drop
        lag = summable_demo_lag(transition)
        predicted_partial_sum = Fraction(1, 3) * (
            1 - Fraction(1, 4**level)
        )
        verified = (
            summable_demo_energy(transition) == 1
            and summable_demo_energy(transition + 1) == 1 - drop
            and summable_demo_energy(transition + 2) == 1
            and weighted_drop == Fraction(1, transition**2)
            and lag == 1 - Fraction(transition + 1, transition**3)
            and lag > 0
            and partial_weighted_variation == predicted_partial_sum
        )
        failures += int(not verified)
        row = {
            "level_k": level,
            "downward_transition_n": transition,
            "drop": fraction_record(drop),
            "weighted_drop_n_times_drop": fraction_record(weighted_drop),
            "lag_partial_sum_S_n": fraction_record(lag),
            "partial_weighted_downward_variation": fraction_record(
                partial_weighted_variation
            ),
            "identity_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"{level}:{transition}:{drop}:{weighted_drop}:{lag}:"
            f"{partial_weighted_variation}:{int(verified)}\n".encode("ascii")
        )
    theorem = (
        "Let (E_n) be a positive real sequence with E_n tending to L>0, put "
        "d_n=(E_n-E_(n+1))_+, and S_n=(n+1)E_(n+1)-nE_n. If the nonnegative "
        "series sum_(n>=1) n d_n converges, then S_n>0 for all sufficiently "
        "large n; more precisely liminf S_n>=L. Thus summable scaled downward "
        "variation is a sufficient abstract packet criterion."
    )
    proof = (
        "The identity S_n=E_(n+1)-n(E_n-E_(n+1)) gives "
        "S_n>=E_(n+1)-n d_n. Convergence of the nonnegative series implies "
        "n d_n tends to zero, while E_(n+1) tends to L. Taking lower limits "
        "gives liminf S_n>=L, hence eventual positivity. The exact replay uses "
        "E_(2^k+1)=1-2^(-3k) and E_n=1 otherwise: its weighted downward "
        "variation is sum 4^(-k)=1/3 and every displayed downward lag is "
        "1-(2^k+1)/2^(3k)>0. This theorem does not prove the required summability "
        "for actual Guinand-Weil packet energies."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_summable_variation_rows": rows,
        "weighted_downward_variation_exact": fraction_record(Fraction(1, 3)),
        "algorithm": "closed-form Fraction replay of a summable scaled-downward-variation packet sequence",
        "complexity": "O(K) exact rational operations for K replay rows; the sufficient theorem is unrestricted",
        "random_seed": None,
        "input_range": {"level_k_min": RIEMANN_LEVELS[0], "level_k_max": RIEMANN_LEVELS[-1]},
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "summable_scaled_downward_variation_implies_eventual_lag_positivity_proved": True,
            "demo_weighted_downward_variation": fraction_record(Fraction(1, 3)),
            "actual_weil_scaled_downward_variation_summable": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


def least_prime_above(value: int) -> int:
    candidate = value + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate


@lru_cache(maxsize=1)
def collatz_fixed_modulus_equidistribution_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    previous_prime = 3
    deviation_sum = Fraction(0)
    exponents: list[int] = []
    for index in range(1, COLLATZ_TERM_COUNT + 1):
        prime = least_prime_above(max(previous_prime, index**3))
        exponent = index
        previous_prime = prime
        exponents.append(exponent)
        deviation_bound = Fraction(8 * exponent, prime)
        comparison_bound = Fraction(8, index**2)
        deviation_sum += deviation_bound
        normalized_bound = deviation_sum / index
        verified = (
            prime > index**3
            and prime > exponent
            and deviation_bound < comparison_bound
            and is_prime(prime)
        )
        failures += int(not verified)
        row = {
            "index_j": index,
            "prime_order_q_j": prime,
            "phase_exponent_d_j": exponent,
            "exponent_over_prime": fraction_record(Fraction(exponent, prime)),
            "chord_deviation_upper_bound": fraction_record(deviation_bound),
            "eight_over_j_squared_bound": fraction_record(comparison_bound),
            "normalized_prefix_deviation_upper_bound": fraction_record(
                normalized_bound
            ),
            "row_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"phase:{index}:{prime}:{exponent}:{deviation_bound}:"
            f"{normalized_bound}:{int(verified)}\n".encode("ascii")
        )
    modulus_rows: list[dict[str, Any]] = []
    for modulus in COLLATZ_FIXED_MODULI:
        counts = [sum(value % modulus == residue for value in exponents) for residue in range(modulus)]
        discrepancy = max(counts) - min(counts)
        verified = discrepancy <= 1
        failures += int(not verified)
        row = {
            "fixed_modulus_M": modulus,
            "prefix_length_N": COLLATZ_TERM_COUNT,
            "residue_counts": counts,
            "maximum_count_difference": discrepancy,
            "balanced_verified": verified,
        }
        modulus_rows.append(row)
        transcript.update(
            f"mod:{modulus}:{','.join(map(str, counts))}:{discrepancy}:"
            f"{int(verified)}\n".encode("ascii")
        )
    theorem = (
        "There are distinct prime moduli q_j and nonzero exponents "
        "1<=d_j<q_j such that d_j is uniformly distributed modulo every fixed "
        "integer M in the strongest prefix sense (the residue counts of d_1,...,d_N "
        "differ by at most one), while N^(-1) sum_(j<=N) exp(2*pi*i*d_j/q_j) "
        "tends to one. Hence equidistribution of the exponents in every fixed "
        "modulus does not imply cancellation on their growing prime moduli."
    )
    proof = (
        "Choose q_j recursively as the least prime exceeding both q_(j-1) and "
        "j^3, and put d_j=j. For every fixed M, consecutive integers have "
        "residue counts differing by at most one. The chord bound and pi<4 give "
        "|exp(2*pi*i*j/q_j)-1|<8j/q_j<8/j^2. Since sum_(j>=1)1/j^2<=2 by "
        "comparison with 1+sum_(j>=2)1/(j(j-1)), the normalized prefix deviation "
        "is at most 16/N and tends to zero. This counterfamily is not the "
        "canonical Fermat-quotient sequence; it proves that fixed-modulus exponent "
        "statistics are the wrong scale for that remaining problem."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_phase_envelope_rows": rows,
        "exact_fixed_modulus_balance_rows": modulus_rows,
        "algorithm": "deterministic prime search plus exact Fraction chord envelopes and integer residue counts",
        "complexity": "O(N sqrt(q_N)) trial-division work in the replay and O(NM_max) balance checks; the construction is infinite",
        "random_seed": None,
        "input_range": {"term_count": COLLATZ_TERM_COUNT, "fixed_modulus_min": 2, "fixed_modulus_max": 16},
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "fixed_modulus_exponent_equidistribution_proved": True,
            "normalized_phase_sum_tends_to_one_proved": True,
            "fixed_modulus_equidistribution_implies_cancellation_refuted": True,
            "canonical_fermat_quotient_exponents_used": False,
            "canonical_angular_discrepancy_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def q3_goldbach_level(level: int, counter: LehmerPrimeCounter) -> dict[str, Any]:
    exponent_m = 12 * level + 6
    scale_A = 3 ** (6 * level + 2)
    cyclic = cyclic_binomial_coefficients(3, exponent_m)
    predicted_cyclic = [-2 * scale_A, scale_A, scale_A]
    shift = 1 + 2 * scale_A
    prefix_length = 3 * shift
    target = [1, 1 + 3 * scale_A, 1 + 3 * scale_A]
    endpoint = counter.nth_prime(prefix_length, max(1_000, 25 * prefix_length))
    combinatorial, combinatorial_metrics = combinatorial_residue_prime_counts(endpoint, 3)
    segmented, segmented_metrics = direct_segmented_residue_prime_counts(
        endpoint, 3, GOLDBACH_SEGMENT_ODD_COUNT
    )
    prime_race_difference = combinatorial[1] - combinatorial[2]
    verified = (
        cyclic == predicted_cyclic
        and sum(target) == prefix_length
        and counter.prime_pi(endpoint) == prefix_length
        and counter.prime_pi(endpoint - 1) == prefix_length - 1
        and combinatorial == segmented
        and combinatorial[0] == 1
        and prime_race_difference != 0
        and combinatorial != target
    )
    return {
        "level_l": level,
        "prime_modulus_q": 3,
        "exponent_m": exponent_m,
        "scale_A_equals_3_power_6l_plus_2": str(scale_A),
        "cyclic_coefficients": cyclic,
        "predicted_cyclic_coefficients": predicted_cyclic,
        "forced_shift_t": str(shift),
        "forced_prefix_length_T": prefix_length,
        "forced_residue_counts": target,
        "exact_nth_prime_endpoint": endpoint,
        "actual_residue_counts": combinatorial,
        "independent_segmented_residue_counts": segmented,
        "mod_3_prime_race_difference_N1_minus_N2": prime_race_difference,
        "prime_race_tie": prime_race_difference == 0,
        "compatible_prefix_excluded": combinatorial != target,
        "combinatorial_algorithm_metrics": combinatorial_metrics,
        "segmented_algorithm_metrics": segmented_metrics,
        "certificate_verified": verified,
    }


@lru_cache(maxsize=1)
def goldbach_q3_prime_race_audit() -> dict[str, Any]:
    counter = LehmerPrimeCounter()
    rows = [q3_goldbach_level(level, counter) for level in GOLDBACH_LEVELS]
    transcript = hashlib.sha256()
    failures = 0
    for row in rows:
        failures += int(not row["certificate_verified"])
        transcript.update(
            f"{row['level_l']}:{row['exponent_m']}:"
            f"{row['scale_A_equals_3_power_6l_plus_2']}:"
            f"{row['forced_prefix_length_T']}:{row['exact_nth_prime_endpoint']}:"
            f"{','.join(map(str, row['actual_residue_counts']))}:"
            f"{row['mod_3_prime_race_difference_N1_minus_N2']}:"
            f"{int(row['certificate_verified'])}\n".encode("ascii")
        )
    theorem = (
        "For every integer l>=0, put q=3, m=12l+6, and A=3^(6l+2). "
        "The cyclic coefficients of (1-X)^m modulo X^3-1 are (-2A,A,A), "
        "so the unique compatible forced prime-prefix vector is "
        "(1,1+3A,1+3A) with length T_l=6A+3. It equals the actual residue "
        "vector of the first T_l primes if and only if the mod-3 prime-race "
        "difference N_1(T_l)-N_2(T_l) is zero."
    )
    proof = (
        "A root-of-unity filter has a zero contribution at 1. For a primitive "
        "cube root zeta, (1-zeta)^m and its conjugate both equal -3^(m/2) "
        "because m=12l+6. Fourier inversion gives c_0=-2*3^(m/2-1)=-2A "
        "and c_1=c_2=A. The forced shift is 1-c_0=1+2A, yielding the stated "
        "vector and T_l. In any actual prefix beyond 3, residue zero contains "
        "only the prime 3; the other T_l-1 entries match the equal target "
        "counts exactly iff N_1=N_2. Two independent exact residue sieves "
        "exclude l=0,1,2, but no finite computation proves nonvanishing for "
        "all l."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_q3_prime_race_certificate_rows": rows,
        "algorithm": "closed-form integer root-of-unity coefficients, exact Lehmer nth-prime counting, vector combinatorial sieve, and independent segmented sieve",
        "complexity": "O(1) symbolic arithmetic per l; finite residue certificates use O(sqrt(x)) quotient states and an independent O(x log log x) segmented sieve",
        "random_seed": None,
        "input_range": {"level_l_min": GOLDBACH_LEVELS[0], "level_l_max": GOLDBACH_LEVELS[-1]},
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "q3_compatible_family_prime_race_equivalence_proved": True,
            "finite_level_count": len(rows),
            "maximum_prefix_length": max(row["forced_prefix_length_T"] for row in rows),
            "maximum_endpoint": max(row["exact_nth_prime_endpoint"] for row in rows),
            "independent_exact_algorithm_count": 2,
            "finite_levels_excluded": sum(row["compatible_prefix_excluded"] for row in rows),
            "all_q3_levels_excluded": False,
            "all_compatible_even_q_divisible_prefixes_excluded": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def twin_variable_denominator_audit() -> dict[str, Any]:
    _, source_rows, lower, upper = certified_root_continued_fraction(
        TWIN_CONVERGENT_COUNT
    )
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    first_order_passes: list[dict[str, Any]] = []
    second_order_passes: list[dict[str, Any]] = []
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
            if denominator == 1:
                first_residue = 0
                second_residue = 0
                first_pass = True
                second_pass = coefficient == epsilon
                direct_residue = 0
            else:
                modulus_squared = denominator * denominator
                first_residue = (pow(numerator, 17, denominator) - epsilon) % denominator
                truncated = (
                    pow(numerator, 17, modulus_squared)
                    + 17 * pow(numerator, 16, modulus_squared) * denominator
                    - epsilon
                ) % modulus_squared
                direct_residue = (coefficient - epsilon) % modulus_squared
                second_residue = truncated
                first_pass = first_residue == 0
                second_pass = second_residue == 0
                expansion_verified = expansion_verified and truncated == direct_residue
                if first_pass:
                    first_order_passes.append(
                        {
                            "term_index": index,
                            "epsilon": epsilon,
                            "numerator": str(numerator),
                            "denominator": str(denominator),
                            "B_1_at_convergent": str(coefficient),
                        }
                    )
                if second_pass:
                    second_order_passes.append(
                        {
                            "term_index": index,
                            "epsilon": epsilon,
                            "numerator": str(numerator),
                            "denominator": str(denominator),
                            "B_1_at_convergent": str(coefficient),
                        }
                    )
            sign_rows.append(
                {
                    "epsilon": epsilon,
                    "first_order_residue_mod_v": str(first_residue),
                    "second_order_residue_mod_v_squared": str(second_residue),
                    "direct_B1_residue_mod_v_squared": str(direct_residue),
                    "first_order_pass": first_pass,
                    "second_order_pass": second_pass,
                }
            )
        direct_unit_hit = abs(coefficient) == 1
        verified = monotone and expansion_verified and not direct_unit_hit
        failures += int(not verified)
        row = {
            "term_index": index,
            "partial_quotient": source["partial_quotient"],
            "convergent_numerator": str(numerator),
            "convergent_denominator": str(denominator),
            "denominator_digit_count": len(str(denominator)),
            "root_side": source["root_side"],
            "sign_tests": sign_rows,
            "truncated_expansion_matches_direct_B1_mod_v_squared": expansion_verified,
            "direct_unit_coefficient_hit": direct_unit_hit,
            "row_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"{index}:{source['partial_quotient']}:{numerator}:{denominator}:"
            f"{coefficient}:{sign_rows[0]['first_order_residue_mod_v']}:"
            f"{sign_rows[0]['second_order_residue_mod_v_squared']}:"
            f"{sign_rows[1]['first_order_residue_mod_v']}:"
            f"{sign_rows[1]['second_order_residue_mod_v_squared']}:"
            f"{int(expansion_verified)}:{int(direct_unit_hit)}\n".encode("ascii")
        )
    nontrivial_second_passes = [
        row for row in second_order_passes if int(row["denominator"]) >= 2
    ]
    failures += len(nontrivial_second_passes)
    expected_first = [(2, -1, 13), (3, -1, 14)]
    observed_first = [
        (row["term_index"], row["epsilon"], int(row["denominator"]))
        for row in first_order_passes
        if int(row["denominator"]) >= 2
    ]
    failures += int(observed_first != expected_first)
    theorem = (
        "For integers u,v with v>=2 and epsilon in {-1,1}, the equality "
        "B_1(u,v)=epsilon forces both u^17=epsilon modulo v and "
        "u^17+17u^16v=epsilon modulo v^2. Among the first 256 certified "
        "continued-fraction convergents of the unique TICKET-258 root, both "
        "signs fail the second-order condition. Only (u,v,epsilon)=(-1,13,-1) "
        "and (-1,14,-1) pass the weaker first-order condition, so first-order "
        "variable-modulus filtering alone is exactly insufficient on this list."
    )
    proof = (
        "The degree-17 form begins B_1(u,v)=u^17+17u^16v plus terms each "
        "divisible by v^2. Reduction modulo v and v^2 proves the two necessary "
        "conditions without approximation. TICKET-258 proves every nonzero "
        "unit-coefficient solution must be a convergent of the isolated root. "
        "For each of the first 256 certified convergents, the replay checks both "
        "epsilon signs with modular exponentiation and independently compares "
        "the truncated residue with the full integer B_1 value modulo v^2. "
        "The two denominator-one convergents are checked directly. Infinitely "
        "many later convergents remain, so this is a finite certificate plus an "
        "unrestricted necessary lemma, not a solution of the Thue equation."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_variable_denominator_convergent_rows": rows,
        "first_order_nontrivial_passes": first_order_passes,
        "second_order_nontrivial_passes": nontrivial_second_passes,
        "final_exact_root_bracket": {
            "lower": fraction_record(lower),
            "upper": fraction_record(upper),
        },
        "algorithm": "certified rational continued fractions, modular exponentiation modulo v and v^2, and independent full-form residue comparison",
        "complexity": "O(K) certified convergents and O(K log 17) modular multiplications on O(log v_K)-bit integers",
        "random_seed": None,
        "input_range": {"certified_convergent_count": TWIN_CONVERGENT_COUNT, "epsilon_values": [-1, 1]},
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "second_order_denominator_congruence_necessary_proved": True,
            "certified_convergent_count": len(rows),
            "maximum_denominator": rows[-1]["convergent_denominator"],
            "maximum_denominator_digit_count": rows[-1]["denominator_digit_count"],
            "first_order_nontrivial_pass_count": len(observed_first),
            "second_order_nontrivial_pass_count": len(nontrivial_second_passes),
            "first_order_only_filter_complete": False,
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
        {"id": f"{code}-T259", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T260", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-CERT260", "label": f"{theorem_name}ExactReplay", "status": "computed_finite"},
        {"id": f"{code}-REJECT260", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN260", "label": open_name, "status": "open"},
    ]
    return {
        "nodes": nodes,
        "edges": [
            [f"{code}-T259", f"{code}-T260"],
            [f"{code}-T260", f"{code}-CERT260"],
            [f"{code}-T260", f"{code}-REJECT260"],
            [f"{code}-T260", f"{code}-OPEN260"],
        ],
        "resolution_path": [f"{code}-T259", f"{code}-T260", f"{code}-OPEN260"],
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
        "ticket_id": f"{code}-TICKET-260",
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
    riemann = riemann_weighted_variation_audit()
    collatz = collatz_fixed_modulus_equidistribution_audit()
    goldbach = goldbach_q3_prime_race_audit()
    twin = twin_variable_denominator_audit()
    sections = {
        "riemann": section(
            "riemann", "RH", "SummableScaledDownwardVariationForcesEventualLagPositivity", "partial_theorem", riemann,
            "treating ordinary bounded total variation as sufficient without the summable n-weighted one-sided condition",
            ["direct arithmetic proof of summable scaled downward variation for actual Guinand-Weil packet energies"],
            "the exact weighted one-sided sufficient criterion and TICKET-259 sharp critical obstruction",
            "ActualWeilPacketScaledDownwardVariationIsSummable",
            "CriticalScaledDownwardJumpEqualityNoGo",
            "BoundedTotalVariationAloneForcesEventualLagPositivity",
            "The sufficient abstract criterion is proved, but no estimate establishes its hypothesis for actual Guinand-Weil packet energies.",
            "No RH proof or disproof; the actual-Weil gap is reduced to one explicit weighted one-sided summability statement.",
            f"{len(riemann['exact_summable_variation_rows'])} Fraction rows replay one infinite model; no actual Weil coefficient is computed.",
        ),
        "collatz": section(
            "collatz", "CO", "FixedModulusExponentEquidistributionPhaseAlignmentNoGo", "exact_no_go", collatz,
            "deducing growing-prime-modulus phase cancellation from equidistribution of exponents modulo every fixed integer",
            ["angular discrepancy of the canonical fixed-base Fermat-quotient exponents on their varying prime moduli"],
            "the exact fixed-modulus-equidistributed aligned counterfamily and the need for moving-modulus angular information",
            "CanonicalFermatQuotientAngularDiscrepancyTendsToZero",
            "DistinctPrimePhaseAlignmentLinearGrowthNoGo",
            "FixedModulusExponentEquidistributionImpliesGrowingModulusPhaseCancellation",
            "Even all fixed-modulus exponent statistics are insufficient; no angular discrepancy theorem is proved for the canonical Fermat-quotient exponents.",
            "No Collatz proof or counterexample; a stronger structural shortcut to the canonical phase cancellation is eliminated.",
            f"{len(collatz['exact_phase_envelope_rows'])} phase rows and {len(collatz['exact_fixed_modulus_balance_rows'])} fixed-modulus balance rows replay the construction; canonical D_q values are not used.",
        ),
        "goldbach": section(
            "goldbach", "GB", "Q3CompatibleFamilyPrimeRaceEquivalence", "partial_theorem", goldbach,
            "treating the q=3 compatible q-divisible family as requiring the full higher-dimensional odd-character detector",
            ["nonvanishing of the mod-3 prime race at the special indices 6*3^(6l+2)+3"],
            "the exact q=3 closed form, prime-race equivalence, and three independently reproduced prefix exclusions",
            "Q3SpecialPrimeRaceNeverTiesAtSixTimesPowerOfThreePlusThree",
            "QDivisibleCompatibilityIffTwoModuloFourAndQ13Certificate",
            "Q3CompatibleFamilyRequiresHigherDimensionalCharacterAnalysis",
            "The q=3 family is reduced to one scalar prime-race nonvanishing statement, but no theorem excludes a tie at every special exponential index.",
            "No strong Goldbach proof or counterexample; an infinite compatible subfamily is exactly reduced and only three levels are computationally excluded.",
            f"The equivalence holds for all l>=0; exact prime-prefix calculations cover only l={GOLDBACH_LEVELS[0]} through {GOLDBACH_LEVELS[-1]}.",
        ),
        "twin_prime": section(
            "twin-prime", "TP", "SecondOrderDenominatorCongruenceAnd256ConvergentCertificate", "partial_theorem", twin,
            "using only the first-order variable condition u^17 congruent to plus or minus one modulo v as a complete convergent filter",
            ["global exclusion of the second-order modulo-v-squared condition on every later unique-root convergent"],
            "the exact modulo-v-squared necessary condition and the 256-convergent two-sign certificate",
            "NoUniqueRootConvergentSatisfiesSecondOrderDenominatorCongruence",
            "FiniteCongruenceFixedRootWindowNoGo",
            "FirstOrderDenominatorCongruenceEliminatesEveryUniqueRootConvergent",
            "The scale-dependent second-order sieve eliminates 256 certified convergents, but infinitely many later convergents are not controlled.",
            "No twin-prime proof or counterexample; the last exponent-17 branch now has a genuinely scale-dependent necessary congruence modulo v^2.",
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
            "theorem_name": "FourConjectureWeightedEquidistributionPrimeRaceVariableModAudit",
            "summary": "TICKET-260 proves three partial theorems and one exact route no-go: weighted one-sided variation suffices for eventual RH-packet lag positivity, fixed-modulus exponent equidistribution still permits aligned Collatz phases, the q=3 Goldbach compatible family is exactly a special prime-race nonvanishing problem, and the Twin degree-17 branch obeys a new scale-dependent modulo-v-squared condition; all parent conjectures remain open.",
            **sections,
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 3,
                "exact_no_go_count": 1,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "twin_prime",
                "stagnated_problem_count": 0,
                "riemann_weighted_variation_case_count": len(riemann["exact_summable_variation_rows"]),
                "collatz_phase_case_count": len(collatz["exact_phase_envelope_rows"]),
                "collatz_fixed_modulus_case_count": len(collatz["exact_fixed_modulus_balance_rows"]),
                "goldbach_q3_level_count": len(goldbach["exact_q3_prime_race_certificate_rows"]),
                "goldbach_maximum_prefix_length": goldbach["aggregate"]["maximum_prefix_length"],
                "goldbach_maximum_endpoint": goldbach["aggregate"]["maximum_endpoint"],
                "goldbach_independent_algorithm_count": 2,
                "twin_convergent_count": len(twin["exact_variable_denominator_convergent_rows"]),
                "twin_first_order_nontrivial_pass_count": twin["aggregate"]["first_order_nontrivial_pass_count"],
                "twin_second_order_nontrivial_pass_count": twin["aggregate"]["second_order_nontrivial_pass_count"],
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
    previous = json.loads(
        (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
            encoding="utf-8"
        )
    )
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
        "ticket": 260,
        "parent_ticket": 259,
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
        ROOT / "data/open-problem/ticket260-weighted-equidistribution-primerace-variablemod.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-260-summable-scaled-variation.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-260-fixed-modulus-equidistribution-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-260-q3-prime-race-reduction.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-260-variable-denominator-congruence.json",
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
