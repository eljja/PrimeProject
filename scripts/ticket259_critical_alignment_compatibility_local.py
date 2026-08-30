from __future__ import annotations

import hashlib
import json
import sys
from array import array
from fractions import Fraction
from functools import lru_cache
from math import gcd, isqrt
from pathlib import Path
from typing import Any

import numpy as np


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket254_diagonal_weighted_reflection_thue import (
    fraction_record,
    is_prime,
    write_json,
)
from scripts.ticket256_cesaro_kernel_qdiv_gl2 import cyclic_binomial_coefficients
from scripts.ticket257_spike_cyclotomic_character_root import b1_coefficient_form
from scripts.ticket258_variation_character_convergent import (
    TWIN_ROOT_LOWER,
    TWIN_ROOT_UPPER,
    cyclotomic_polynomial,
    polynomial_divmod_monic,
    primitive_root_prime,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket259-critical-alignment-compatibility-local.v1"
GENERATED_AT = "2026-08-31T22:00:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "critical_alignment_compatibility_local_audit"

RIEMANN_LEVELS = tuple(range(1, 13))
COLLATZ_PRIME_LIMIT = 997
GOLDBACH_COMPATIBILITY_PRIMES = tuple(q for q in range(3, 44) if is_prime(q))
GOLDBACH_RATIO_LIMIT = 16
GOLDBACH_Q = 13
GOLDBACH_M = 26
GOLDBACH_PREFIX_T = 135_207_787
GOLDBACH_SEARCH_UPPER = 3_000_000_000
GOLDBACH_SEGMENT_ODD_COUNT = 5_000_000
TWIN_MODULI = tuple(range(2, 32))


def is_positive_power_of_four(value: int) -> bool:
    if value < 4:
        return False
    while value % 4 == 0:
        value //= 4
    return value == 1


def critical_energy(dimension: int) -> Fraction:
    if dimension < 1:
        raise ValueError("packet dimension must be positive")
    transition = dimension - 1
    if is_positive_power_of_four(transition):
        return Fraction(transition - 1, transition)
    return Fraction(1)


def critical_lag_partial_sum(index: int) -> Fraction:
    if index < 0:
        raise ValueError("partial-sum index must be nonnegative")
    return (index + 1) * critical_energy(index + 1) - index * critical_energy(index)


@lru_cache(maxsize=1)
def riemann_critical_threshold_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    partial_variation = Fraction(0)
    for level in RIEMANN_LEVELS:
        transition = 4**level
        drop = Fraction(1, transition)
        partial_variation += 2 * drop
        scaled_drop = transition * (
            critical_energy(transition) - critical_energy(transition + 1)
        )
        partial_sum = critical_lag_partial_sum(transition)
        verified = (
            critical_energy(transition) == 1
            and critical_energy(transition + 1) == 1 - drop
            and critical_energy(transition + 2) == 1
            and scaled_drop == 1
            and partial_sum == -drop
            and partial_variation == Fraction(2, 3) * (1 - Fraction(1, 4**level))
        )
        failures += int(not verified)
        row = {
            "level_k": level,
            "downward_transition_n": transition,
            "critical_drop": fraction_record(drop),
            "scaled_downward_jump_n_times_drop": fraction_record(scaled_drop),
            "lag_partial_sum_S_n": fraction_record(partial_sum),
            "partial_total_variation_through_rebound": fraction_record(partial_variation),
            "identity_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"{level}:{transition}:{drop}:{scaled_drop}:{partial_sum}:"
            f"{partial_variation}:{int(verified)}\n".encode("ascii")
        )
    theorem = (
        "There is a positive packet-energy sequence E_L converging to one, "
        "with total variation 2/3 and sup_(n>=1) n(E_n-E_(n+1))_+=1, whose "
        "lag partial sums S_n=(n+1)E_(n+1)-nE_n are negative infinitely "
        "often. Set E_(4^k+1)=1-4^(-k) and E_L=1 otherwise. Then at n=4^k "
        "the scaled drop is exactly one and S_n=-4^(-k). Hence equality at "
        "the limiting packet margin cannot replace the strict scaled-drop "
        "inequality in the repaired RH packet criterion."
    )
    proof = (
        "The isolated down-and-up spikes contribute 2*4^(-k), so their total "
        "variation is 2 sum_(k>=1)4^(-k)=2/3. The energies are at least 3/4 "
        "and converge to one. At n=4^k, n(E_n-E_(n+1))=1, while direct "
        "Cesaro inversion gives S_n=(n+1)(1-1/n)-n=-1/n. Thus the strict "
        "constant is sharp at the abstract sequence level. No actual "
        "Guinand-Weil coefficient or RH zero is analyzed."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_critical_threshold_rows": rows,
        "total_variation_exact": fraction_record(Fraction(2, 3)),
        "algorithm": "closed-form Fraction replay of isolated critical scaled drops and Cesaro inversion",
        "complexity": "O(K) exact rational operations for K rows; the construction and identities hold for every k",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "positive_convergent_energy_proved": True,
            "critical_scaled_drop_supremum_exactly_one_proved": True,
            "negative_lag_partial_sums_infinitely_often_proved": True,
            "nonstrict_critical_threshold_route_refuted": True,
            "actual_weil_packet_analyzed": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


def primes_from_five(limit: int) -> list[int]:
    return [q for q in range(5, limit + 1) if is_prime(q)]


@lru_cache(maxsize=1)
def collatz_aligned_phase_audit() -> dict[str, Any]:
    primes = primes_from_five(COLLATZ_PRIME_LIMIT)
    reciprocal_sum = Fraction(0)
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for index, prime in enumerate(primes, start=1):
        reciprocal_sum += Fraction(1, prime)
        deviation_envelope = Fraction(8, index) * reciprocal_sum
        normalized_magnitude_lower = max(Fraction(0), 1 - deviation_envelope)
        verified = prime >= index + 4 and deviation_envelope <= Fraction(8, index) * sum(
            (Fraction(1, j) for j in range(1, index + 1)), Fraction(0)
        )
        failures += int(not verified)
        row = {
            "prefix_length_N": index,
            "prime_order_q_N": prime,
            "reciprocal_prime_sum": fraction_record(reciprocal_sum),
            "rigorous_normalized_deviation_upper_bound": fraction_record(deviation_envelope),
            "rigorous_normalized_magnitude_lower_bound": fraction_record(normalized_magnitude_lower),
            "envelope_verified": verified,
        }
        rows.append(row)
        transcript.update(
            f"{index}:{prime}:{reciprocal_sum}:{deviation_envelope}:"
            f"{normalized_magnitude_lower}:{int(verified)}\n".encode("ascii")
        )
    theorem = (
        "Let q_j be the jth prime at least five and let z_j=exp(2*pi*i/q_j). "
        "The phases z_j are nontrivial roots of distinct odd-prime orders "
        "and are rationally independent together with one by TICKET-258, yet "
        "N^(-1) sum_(j<=N) z_j tends to one. In particular the prefix "
        "magnitude is asymptotic to N, not o(N). Therefore distinct prime "
        "orders, nontriviality, and rational independence alone cannot imply "
        "the canonical Collatz sublinear phase bound."
    )
    proof = (
        "The chord estimate |exp(i theta)-1|<=|theta| and pi<4 give "
        "|z_j-1|<8/q_j. Hence |N^(-1)sum z_j-1| is at most "
        "8N^(-1)sum 1/q_j. Since q_j>=j+4, this is bounded by 8H_N/N, "
        "which tends to zero. The reverse triangle inequality then gives "
        "|sum z_j|/N tending to one. The construction deliberately does not "
        "use the canonical Fermat-quotient exponents D_q; their arithmetic "
        "distribution remains the essential open input."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_alignment_envelope_rows": rows,
        "algorithm": "exact rational reciprocal-prime envelopes; no floating-point root of unity is used",
        "complexity": "O(pi(Q)^2) Fraction operations in the deliberately independent harmonic-envelope replay; the proof has an O(N) bound",
        "random_seed": None,
        "prime_limit": COLLATZ_PRIME_LIMIT,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "prime_count": len(primes),
            "distinct_nontrivial_prime_order_phases": True,
            "normalized_phase_sum_tends_to_one_proved": True,
            "sublinear_from_order_data_alone_refuted": True,
            "canonical_fermat_quotient_exponents_used": False,
            "canonical_sublinear_phase_sum_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def compatibility_record(prime: int, ratio: int) -> dict[str, Any]:
    exponent = prime * ratio
    coefficients = cyclic_binomial_coefficients(prime, exponent)
    shift = 1 - coefficients[0]
    compatible = shift > 0 and min(coefficients) + shift >= 0
    predicted = ratio % 4 == 2
    return {
        "prime_q": prime,
        "ratio_s_equals_m_over_q": ratio,
        "exponent_m": exponent,
        "zero_coefficient_c0": str(coefficients[0]),
        "minimum_cyclic_coefficient": str(min(coefficients)),
        "forced_shift_t": str(shift),
        "compatible": compatible,
        "predicted_by_s_mod_4_equals_2": predicted,
        "classification_verified": compatible == predicted,
    }


class LehmerPrimeCounter:
    def __init__(self, limit: int = 1_000_000) -> None:
        sieve = bytearray(b"\x01") * (limit + 1)
        sieve[:2] = b"\x00\x00"
        for prime in range(2, isqrt(limit) + 1):
            if sieve[prime]:
                sieve[prime * prime :: prime] = b"\x00" * (
                    ((limit - prime * prime) // prime) + 1
                )
        self.limit = limit
        self.primes = [value for value, flag in enumerate(sieve) if flag]
        self.pi = array("I", [0]) * (limit + 1)
        count = 0
        for value, flag in enumerate(sieve):
            count += int(flag)
            self.pi[value] = count
        self._phi_cache: dict[tuple[int, int], int] = {}
        self._lehmer_cache: dict[int, int] = {}

    @staticmethod
    def integer_cube_root(value: int) -> int:
        low, high = 0, 1
        while high**3 <= value:
            high *= 2
        while low + 1 < high:
            middle = (low + high) // 2
            if middle**3 <= value:
                low = middle
            else:
                high = middle
        return low

    def phi(self, value: int, count: int) -> int:
        if count == 0:
            return value
        if count == 1:
            return value - value // 2
        key = (value, count)
        cached = self._phi_cache.get(key)
        if cached is not None:
            return cached
        result = self.phi(value, count - 1) - self.phi(
            value // self.primes[count - 1], count - 1
        )
        if value < 10_000_000 and count < 100:
            self._phi_cache[key] = result
        return result

    def prime_pi(self, value: int) -> int:
        if value < self.limit:
            return int(self.pi[value])
        cached = self._lehmer_cache.get(value)
        if cached is not None:
            return cached
        a = self.prime_pi(isqrt(isqrt(value)))
        b = self.prime_pi(isqrt(value))
        c = self.prime_pi(self.integer_cube_root(value))
        total = self.phi(value, a) + ((b + a - 2) * (b - a + 1)) // 2
        for index in range(a, b):
            reduced = value // self.primes[index]
            total -= self.prime_pi(reduced)
            if index < c:
                limit = self.prime_pi(isqrt(reduced))
                for second in range(index, limit):
                    total -= self.prime_pi(reduced // self.primes[second]) - second
        self._lehmer_cache[value] = total
        return total

    def nth_prime(self, target: int, upper: int) -> int:
        low, high = 2, upper
        if self.prime_pi(high) < target:
            raise ValueError("nth-prime upper bound is too small")
        while low < high:
            middle = (low + high) // 2
            if self.prime_pi(middle) >= target:
                high = middle
            else:
                low = middle + 1
        return low


def initial_residue_counts(value: int, modulus: int) -> list[int]:
    blocks, remainder = divmod(value, modulus)
    counts = [
        blocks if residue == 0 else blocks + int(residue <= remainder)
        for residue in range(modulus)
    ]
    if value >= 1:
        counts[1] -= 1
    return counts


def combinatorial_residue_prime_counts(value: int, modulus: int) -> tuple[list[int], dict[str, int]]:
    root = isqrt(value)
    quotient_states = sorted(
        set(range(1, root + 1)) | {value // index for index in range(1, root + 1)},
        reverse=True,
    )
    counts = {
        state: initial_residue_counts(state, modulus) for state in quotient_states
    }
    prime_steps = 0
    update_count = 0
    for prime in range(2, root + 1):
        if sum(counts[prime]) == sum(counts[prime - 1]):
            continue
        prime_steps += 1
        square = prime * prime
        if prime % modulus:
            inverse = pow(prime, -1, modulus)
            mapping = [residue * inverse % modulus for residue in range(modulus)]
            base = counts[prime - 1]
            for state in quotient_states:
                if state < square:
                    break
                source = counts[state // prime]
                row = counts[state]
                for residue, mapped in enumerate(mapping):
                    row[residue] -= source[mapped] - base[mapped]
                update_count += 1
        else:
            base_total = sum(counts[prime - 1])
            for state in quotient_states:
                if state < square:
                    break
                counts[state][0] -= sum(counts[state // prime]) - base_total
                update_count += 1
    return counts[value], {
        "quotient_state_count": len(quotient_states),
        "sieving_prime_count": prime_steps,
        "vector_update_count": update_count,
    }


def direct_segmented_residue_prime_counts(
    value: int, modulus: int, odd_count: int
) -> tuple[list[int], dict[str, int]]:
    root = isqrt(value)
    base = np.ones(root + 1, dtype=np.bool_)
    base[:2] = False
    for prime in range(2, isqrt(root) + 1):
        if base[prime]:
            base[prime * prime :: prime] = False
    base_primes = np.flatnonzero(base)
    counts = np.zeros(modulus, dtype=np.int64)
    counts[2 % modulus] = 1
    seen = 1
    last_prime = 2
    segment_count = 0
    low = 3
    while low <= value:
        high = min(value, low + 2 * (odd_count - 1))
        if high % 2 == 0:
            high -= 1
        size = (high - low) // 2 + 1
        mark = np.ones(size, dtype=np.bool_)
        for raw_prime in base_primes[1:]:
            prime = int(raw_prime)
            if prime * prime > high:
                break
            start = max(prime * prime, ((low + prime - 1) // prime) * prime)
            if start % 2 == 0:
                start += prime
            if start <= high:
                mark[(start - low) // 2 :: prime] = False
        indices = np.flatnonzero(mark)
        primes = low + 2 * indices
        counts += np.bincount(primes % modulus, minlength=modulus)
        if len(primes):
            last_prime = int(primes[-1])
        seen += len(primes)
        segment_count += 1
        low = high + 2
    return [int(entry) for entry in counts], {
        "segment_count": segment_count,
        "enumerated_prime_count": int(seen),
        "last_prime": last_prime,
        "base_prime_count": len(base_primes),
    }


@lru_cache(maxsize=1)
def goldbach_compatibility_and_q13_audit() -> dict[str, Any]:
    classification_rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for prime in GOLDBACH_COMPATIBILITY_PRIMES:
        for ratio in range(1, GOLDBACH_RATIO_LIMIT + 1):
            row = compatibility_record(prime, ratio)
            classification_rows.append(row)
            failures += int(not row["classification_verified"])
            transcript.update(
                f"class:{prime}:{ratio}:{row['zero_coefficient_c0']}:"
                f"{row['minimum_cyclic_coefficient']}:{row['forced_shift_t']}:"
                f"{int(row['compatible'])}:{int(row['classification_verified'])}\n".encode(
                    "ascii"
                )
            )

    coefficients = cyclic_binomial_coefficients(GOLDBACH_Q, GOLDBACH_M)
    shift = 1 - coefficients[0]
    target = [coefficient + shift for coefficient in coefficients]
    forced_total = GOLDBACH_Q * shift
    counter = LehmerPrimeCounter()
    endpoint = counter.nth_prime(GOLDBACH_PREFIX_T, GOLDBACH_SEARCH_UPPER)
    endpoint_pi = counter.prime_pi(endpoint)
    preceding_pi = counter.prime_pi(endpoint - 1)
    combinatorial_counts, combinatorial_metrics = combinatorial_residue_prime_counts(
        endpoint, GOLDBACH_Q
    )
    direct_counts, direct_metrics = direct_segmented_residue_prime_counts(
        endpoint, GOLDBACH_Q, GOLDBACH_SEGMENT_ODD_COUNT
    )
    asymmetry = [
        combinatorial_counts[residue]
        - combinatorial_counts[(-residue) % GOLDBACH_Q]
        for residue in range(GOLDBACH_Q)
    ]
    primitive_root = primitive_root_prime(GOLDBACH_Q)
    antisymmetric_half = [
        combinatorial_counts[pow(primitive_root, exponent, GOLDBACH_Q)]
        - combinatorial_counts[
            (-pow(primitive_root, exponent, GOLDBACH_Q)) % GOLDBACH_Q
        ]
        for exponent in range((GOLDBACH_Q - 1) // 2)
    ]
    cyclotomic = list(cyclotomic_polynomial(GOLDBACH_Q - 1))
    _, primitive_remainder = polynomial_divmod_monic(
        antisymmetric_half, cyclotomic
    )
    q13_verified = (
        forced_total == GOLDBACH_PREFIX_T
        and endpoint_pi == GOLDBACH_PREFIX_T
        and preceding_pi == GOLDBACH_PREFIX_T - 1
        and combinatorial_counts == direct_counts
        and sum(combinatorial_counts) == GOLDBACH_PREFIX_T
        and combinatorial_counts[0] == 1
        and any(asymmetry)
        and primitive_remainder != [0]
        and target != combinatorial_counts
        and all(target[residue] == target[-residue % GOLDBACH_Q] for residue in range(GOLDBACH_Q))
    )
    failures += int(not q13_verified)
    q13 = {
        "prime_modulus_q": GOLDBACH_Q,
        "q_divisible_even_exponent_m": GOLDBACH_M,
        "ratio_s_equals_m_over_q": GOLDBACH_M // GOLDBACH_Q,
        "cyclic_coefficients": coefficients,
        "forced_uniform_shift_t": shift,
        "forced_total_prime_count_T": forced_total,
        "forced_symmetric_residue_counts": target,
        "exact_nth_prime_endpoint": endpoint,
        "prime_pi_at_endpoint": endpoint_pi,
        "prime_pi_before_endpoint": preceding_pi,
        "actual_first_T_prime_residue_counts": combinatorial_counts,
        "independent_direct_segmented_counts": direct_counts,
        "actual_reflection_differences": asymmetry,
        "primitive_root_g": primitive_root,
        "antisymmetric_half_vector": antisymmetric_half,
        "cyclotomic_polynomial_phi_12": cyclotomic,
        "primitive_odd_character_moment_remainder": primitive_remainder,
        "primitive_odd_character_moment_nonzero": primitive_remainder != [0],
        "unique_prime_prefix_excluded": target != combinatorial_counts,
        "combinatorial_algorithm_metrics": combinatorial_metrics,
        "direct_segmented_algorithm_metrics": direct_metrics,
        "certificate_verified": q13_verified,
    }
    transcript.update(
        f"q13:{GOLDBACH_M}:{shift}:{forced_total}:{endpoint}:"
        f"{','.join(map(str, target))}:{','.join(map(str, combinatorial_counts))}:"
        f"{','.join(map(str, direct_counts))}:{','.join(map(str, asymmetry))}:"
        f"{','.join(map(str, antisymmetric_half))}:"
        f"{','.join(map(str, primitive_remainder))}:{int(q13_verified)}\n".encode(
            "ascii"
        )
    )
    theorem = (
        "Let q be an odd prime, let m=qs>0, and let c_r be the coefficients "
        "of (1-X)^m modulo X^q-1. With t=1-c_0, the shifted vector c_r+t "
        "is nonnegative with t>0 if and only if s is congruent to two modulo "
        "four. Thus every q-divisible compatible exponent is exactly "
        "m=q(4ell+2). For the first new case (q,m)=(13,26), the forced "
        "length is T=135207787 and the forced vector is reflection-symmetric. "
        "The exact Tth prime is 2798637773; two independent exact algorithms "
        "give the same actual residue vector, whose reflection differences "
        "are nonzero. Its primitive odd-character remainder modulo Phi_12 is "
        "[-958,1746,-64,-121], so this compatible tail is excluded."
    )
    proof = (
        "Compatibility forces m even by TICKET-256, hence s=2k. The root-of-"
        "unity filter gives (1-zeta_q^a)^m=(-1)^k|1-zeta_q^a|^m for every "
        "a not zero because q divides m. If k is even, c_0 is a positive "
        "integer and t<=0. If k is odd, c_0<0 and c_r-c_0 is q^(-1) times "
        "a sum of positive weights times 1-cos(2*pi*a*r/q), hence c_r>=c_0; "
        "therefore t>0 and c_r+t>=1. This proves the iff classification. For "
        "q=13, Lehmer counting plus a residue-vector combinatorial sieve and "
        "an independent direct segmented sieve agree exactly. The nonzero "
        "integer cyclotomic remainder certifies a nonzero primitive odd "
        "character moment. This is one finite prefix certificate, not the "
        "universal prime-discrepancy theorem."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_compatibility_classification_rows": classification_rows,
        "q13_m26_exact_prime_prefix_certificate": q13,
        "algorithm": "integer cyclic folding; exact Lehmer nth-prime counting; vector combinatorial sieve; independent NumPy segmented sieve; integer cyclotomic reduction",
        "complexity": "classification O(sum m); nth-prime Lehmer sublinear; vector combinatorial sieve uses O(sqrt(x)) states; independent direct replay uses O(x log log x) bit operations in fixed-size segments",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "classification_row_count": len(classification_rows),
            "q_divisible_compatibility_iff_ratio_two_mod_four_proved": True,
            "q13_m26_prefix_length": GOLDBACH_PREFIX_T,
            "q13_m26_last_prime": endpoint,
            "independent_exact_residue_algorithms_agree": combinatorial_counts == direct_counts,
            "q13_m26_primitive_odd_character_nonzero": primitive_remainder != [0],
            "q13_m26_compatible_tail_excluded": q13_verified,
            "all_compatible_even_q_divisible_prefixes_excluded": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def fixed_window_local_witness(modulus: int) -> dict[str, Any]:
    if modulus < 2:
        raise ValueError("modulus must be at least two")
    exponent = 1
    while True:
        denominator = modulus**exponent
        quotient = (TWIN_ROOT_LOWER * denominator - 1) // modulus + 1
        numerator = 1 + modulus * quotient
        ratio = Fraction(numerator, denominator)
        if TWIN_ROOT_LOWER < ratio < TWIN_ROOT_UPPER:
            break
        exponent += 1
    coefficient_modulus = b1_coefficient_form(numerator, denominator) % modulus
    verified = (
        denominator > 0
        and gcd(abs(numerator), denominator) == 1
        and TWIN_ROOT_LOWER < ratio < TWIN_ROOT_UPPER
        and numerator * numerator - 2 * denominator * denominator < 0
        and coefficient_modulus == 1 % modulus
    )
    return {
        "modulus_M": modulus,
        "power_exponent_N": exponent,
        "primitive_numerator_u": str(numerator),
        "denominator_v_equals_M_power_N": str(denominator),
        "ratio_u_over_v": fraction_record(ratio),
        "norm_u_squared_minus_2v_squared_is_negative": numerator * numerator - 2 * denominator * denominator < 0,
        "B1_mod_M": coefficient_modulus,
        "witness_verified": verified,
    }


@lru_cache(maxsize=1)
def twin_local_congruence_audit() -> dict[str, Any]:
    rows = [fixed_window_local_witness(modulus) for modulus in TWIN_MODULI]
    failures = sum(not row["witness_verified"] for row in rows)
    transcript = hashlib.sha256()
    for row in rows:
        transcript.update(
            f"{row['modulus_M']}:{row['power_exponent_N']}:"
            f"{row['primitive_numerator_u']}:"
            f"{row['denominator_v_equals_M_power_N']}:"
            f"{row['ratio_u_over_v']['exact']}:{row['B1_mod_M']}:"
            f"{int(row['witness_verified'])}\n".encode("ascii")
        )
    theorem = (
        "Let B_1(u,v) be the TICKET-258 degree-17 coefficient form. For every "
        "integer modulus M>=2 and every nonempty rational interval I contained "
        "in (-1,0), there are infinitely many primitive pairs (u,v) with "
        "v>0, u/v in I, u^2-2v^2<0, and B_1(u,v)=1 modulo M. Consequently no "
        "finite collection of coefficient congruences, even supplemented by "
        "primitivity, the admissible norm sign, and any fixed root window, can "
        "exclude the remaining unit-coefficient branch."
    )
    proof = (
        "Replace finitely many moduli by their least common multiple M. For "
        "arbitrarily large N set v=M^N. The interval vI eventually has length "
        "greater than M, so it contains u congruent to one modulo M. Every "
        "prime divisor of v divides M, while u is one modulo M, hence gcd(u,v)="
        "1. Since I is contained in (-1,0), the norm u^2-2v^2 is negative. "
        "All terms of B_1(u,v) except u^17 contain v, so B_1(u,v) is congruent "
        "to u^17, hence to one modulo M. The witnesses are only local: exact "
        "equality forces the scale-dependent q^(-17) approximation from "
        "TICKET-258, which a fixed interval does not encode."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "fixed_ticket258_root_window": {
            "lower": fraction_record(TWIN_ROOT_LOWER),
            "upper": fraction_record(TWIN_ROOT_UPPER),
        },
        "exact_local_witness_rows": rows,
        "algorithm": "exact integer arithmetic and Fraction interval membership for the least power-of-M witness in the fixed TICKET-258 root bracket",
        "complexity": "O(log_M(M/|I|)) exponent search per replayed modulus; the theorem constructs infinitely many witnesses",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "modulus_case_count": len(rows),
            "primitive_admissible_fixed_window_local_witnesses_proved": True,
            "finite_coefficient_congruence_plus_fixed_window_route_refuted": True,
            "scale_dependent_convergent_exclusion_proved": False,
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
        {"id": f"{code}-T258", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T259", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-CERT259", "label": f"{theorem_name}ExactReplay", "status": "computed_finite"},
        {"id": f"{code}-REJECT259", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN259", "label": open_name, "status": "open"},
    ]
    return {
        "nodes": nodes,
        "edges": [
            [f"{code}-T258", f"{code}-T259"],
            [f"{code}-T259", f"{code}-CERT259"],
            [f"{code}-T259", f"{code}-REJECT259"],
            [f"{code}-T259", f"{code}-OPEN259"],
        ],
        "resolution_path": [f"{code}-T258", f"{code}-T259", f"{code}-OPEN259"],
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
        "ticket_id": f"{code}-TICKET-259",
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
    riemann = riemann_critical_threshold_audit()
    collatz = collatz_aligned_phase_audit()
    goldbach = goldbach_compatibility_and_q13_audit()
    twin = twin_local_congruence_audit()
    sections = {
        "riemann": section(
            "riemann", "RH", "CriticalScaledDownwardJumpEqualityNoGo", "exact_no_go", riemann,
            "relaxing the strict actual-Weil packet margin versus scaled downward jumps to a non-strict critical inequality",
            ["direct arithmetic control of the strict scaled-drop margin for actual Weil packets"],
            "the sharp abstract threshold and the still-open strict actual-Weil inequality",
            "ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation",
            "BoundedTotalVariationPacketEnergyLagNoGo",
            "CriticalScaledDownwardJumpBoundImpliesNonnegativeLagPartialSums",
            "The equality threshold is now proved insufficient, but neither side of the strict inequality is bounded for actual Guinand-Weil packets.",
            "No RH proof or disproof; only the exact strictness requirement of one abstract packet criterion is sharpened.",
            f"{len(riemann['exact_critical_threshold_rows'])} exact rows replay an all-k construction; no actual Weil coefficient is computed.",
        ),
        "collatz": section(
            "collatz", "CO", "DistinctPrimePhaseAlignmentLinearGrowthNoGo", "exact_no_go", collatz,
            "deducing sublinear complex cancellation from distinct prime orders, phase nontriviality, and rational independence alone",
            ["quantitative cancellation of the canonical fixed-base Fermat-quotient phases"],
            "the exact aligned-phase counterfamily and the arithmetic specificity of the canonical exponents D_q",
            "CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude",
            "DistinctPrimeCyclotomicPhaseRationalIndependence",
            "DistinctNontrivialPrimeOrderPhasesAlwaysHaveSublinearPrefixMagnitude",
            "The structural field data are insufficient; no distribution theorem is proved for the canonical Fermat-quotient exponents.",
            "No Collatz proof or counterexample; a broader phase-cancellation shortcut is eliminated while the canonical sum remains open.",
            f"Exact rational envelopes are replayed for {len(collatz['exact_alignment_envelope_rows'])} primes through {COLLATZ_PRIME_LIMIT}; the aligned asymptotic theorem is unrestricted.",
        ),
        "goldbach": section(
            "goldbach", "GB", "QDivisibleCompatibilityIffTwoModuloFourAndQ13Certificate", "partial_theorem", goldbach,
            "treating q-divisible cyclotomic compatibility as a finite-scan property with no exact exponent classification",
            ["uniform odd-character nonvanishing for every classified q-divisible compatible prime prefix"],
            "the exact m/q congruence classification and the independently reproduced q=13,m=26 prefix exclusion",
            "EveryTwoModuloFourQDivisiblePrimePrefixHasNonzeroOddCharacterMoment",
            "PrimitiveOddCharacterCompletenessClassification",
            "QDivisibleCompatibilityRequiresUnboundedFiniteScanning",
            "Compatible exponents are now classified exactly and one much larger prefix is excluded, but no theorem controls actual prime reflection discrepancy for all q and all ratio 2 mod 4.",
            "No strong Goldbach proof or counterexample; one infinite compatibility classification and one finite 135-million-prime certificate are established.",
            "The compatibility iff theorem is infinite; the actual-prime calculation covers only (q,m)=(13,26), ending at prime 2798637773.",
        ),
        "twin_prime": section(
            "twin-prime", "TP", "FiniteCongruenceFixedRootWindowNoGo", "exact_no_go", twin,
            "using any fixed finite coefficient-congruence sieve, even with primitivity, negative norm, and a fixed root window, to eliminate the remaining branch",
            ["scale-dependent q^(-17) root approximation or an effective global Thue/Lebesgue-Nagell argument"],
            "the infinite primitive admissible local-witness theorem and TICKET-258's scale-dependent convergent necessity",
            "EveryUniqueRootConvergentMissesUnitCoefficient",
            "UnitCoefficientSolutionsAreRootConvergents",
            "FiniteCoefficientCongruencesAndFixedRootWindowExcludeAllNonzeroDenominators",
            "Every fixed local-plus-window test has witnesses; exact equality still requires excluding the scale-dependent convergents globally.",
            "No twin-prime proof or counterexample; the remaining exponent-17 branch is shown to require genuinely scale-dependent or global information.",
            f"Witnesses are replayed for moduli {TWIN_MODULI[0]} through {TWIN_MODULI[-1]}; the no-go theorem covers every finite modulus family but not variable-modulus constraints.",
        ),
    }
    sections["goldbach"]["proof_dag"]["nodes"].append(
        {
            "id": "GB-T256",
            "label": "QDivisibleOddExponentIncompatibility",
            "status": "proved",
        }
    )
    sections["goldbach"]["proof_dag"]["edges"].append(["GB-T256", "GB-T259"])
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
            "theorem_name": "FourConjectureCriticalAlignmentCompatibilityLocalAudit",
            "summary": "TICKET-259 proves three exact route no-gos and one partial theorem: critical scaled-drop equality fails for RH packets, distinct prime-order phases can align linearly, q-divisible Goldbach compatibility is classified with a new q=13 exact certificate, and finite congruences plus a fixed root window cannot close the Twin branch; all parent conjectures remain open.",
            **sections,
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 1,
                "exact_no_go_count": 3,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "goldbach",
                "stagnated_problem_count": 0,
                "riemann_critical_case_count": len(riemann["exact_critical_threshold_rows"]),
                "collatz_alignment_case_count": len(collatz["exact_alignment_envelope_rows"]),
                "goldbach_compatibility_case_count": len(goldbach["exact_compatibility_classification_rows"]),
                "goldbach_q13_prefix_length": GOLDBACH_PREFIX_T,
                "goldbach_q13_last_prime": goldbach["aggregate"]["q13_m26_last_prime"],
                "goldbach_independent_algorithm_count": 2,
                "twin_local_modulus_case_count": len(twin["exact_local_witness_rows"]),
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
        "ticket": 259,
        "parent_ticket": 258,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "goldbach",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(
        ROOT / "data/open-problem/ticket259-critical-alignment-compatibility-local.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-259-critical-scaled-drop-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-259-aligned-phase-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-259-compatibility-q13-certificate.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-259-fixed-local-window-no-go.json",
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
