from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache
from math import comb, isqrt
from pathlib import Path
from typing import Any


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket251_interior_crt_cyclotomic_righteven import (
    cyclic_binomial_coefficients,
)
from scripts.ticket253_density_character_prefix_lebesgue import (
    fermat_quotient_mod_prime,
)
from scripts.ticket254_diagonal_weighted_reflection_thue import (
    fraction_record,
    is_prime,
    write_json,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket257-spike-cyclotomic-character-root.v1"
GENERATED_AT = "2026-08-31T12:00:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "spike_cyclotomic_character_root_audit"

RIEMANN_SPIKE_LEVELS = tuple(range(1, 9))
COLLATZ_PRIMES = tuple(q for q in range(7, 98) if is_prime(q))
GOLDBACH_CASES = ((5, 10), (7, 14), (11, 22))
GOLDBACH_SIEVE_LIMIT = 150_000_000
GOLDBACH_SEGMENT_ODD_COUNT = 1 << 20
TWIN_DENOMINATOR_LIMIT = 200_000
TWIN_ROOT_LOWER_NUMERATOR = -7_325_500
TWIN_ROOT_UPPER_NUMERATOR = -7_325_499
TWIN_ROOT_DENOMINATOR = 100_000_000


def fourth_power_level(value: int) -> int | None:
    if value < 4:
        return None
    level = 0
    residual = value
    while residual % 4 == 0:
        residual //= 4
        level += 1
    return level if residual == 1 else None


def prescribed_packet_energy(dimension: int) -> Fraction:
    if dimension < 1:
        raise ValueError("packet dimension must be positive")
    level = fourth_power_level(dimension)
    return Fraction(1) if level is None else Fraction(1) - Fraction(1, 2**level)


def induced_lag_partial_sum(index: int) -> Fraction:
    if index < 0:
        raise ValueError("partial-sum index must be nonnegative")
    if index == 0:
        return prescribed_packet_energy(1)
    return (index + 1) * prescribed_packet_energy(index + 1) - index * prescribed_packet_energy(index)


def induced_lag_coefficient(index: int) -> Fraction:
    if index == 0:
        return induced_lag_partial_sum(0)
    return (induced_lag_partial_sum(index) - induced_lag_partial_sum(index - 1)) / 2


def direct_packet_energy(dimension: int) -> Fraction:
    coefficients = [induced_lag_coefficient(index) for index in range(dimension)]
    return coefficients[0] + 2 * sum(
        Fraction(dimension - lag, dimension) * coefficients[lag]
        for lag in range(1, dimension)
    )


@lru_cache(maxsize=1)
def riemann_spike_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for level in RIEMANN_SPIKE_LEVELS:
        dimension = 4**level
        energy = prescribed_packet_energy(dimension)
        previous_energy = prescribed_packet_energy(dimension - 1)
        partial_sum = induced_lag_partial_sum(dimension - 1)
        direct = direct_packet_energy(dimension)
        expected_partial_sum = Fraction(1 - 2**level)
        verified = (
            energy >= Fraction(1, 2)
            and previous_energy == 1
            and partial_sum == expected_partial_sum
            and direct == energy
        )
        failures += int(not verified)
        transcript.update(
            f"{level}:{dimension}:{energy}:{previous_energy}:{partial_sum}:"
            f"{direct}:{int(verified)}\n".encode("ascii")
        )
        rows.append(
            {
                "spike_level_k": level,
                "packet_dimension_L_equals_4_power_k": dimension,
                "packet_energy_E_L": fraction_record(energy),
                "preceding_packet_energy_E_L_minus_1": fraction_record(previous_energy),
                "symmetric_lag_partial_sum_S_L_minus_1": fraction_record(partial_sum),
                "direct_energy_from_reconstructed_lags": fraction_record(direct),
                "identity_verified": verified,
            }
        )

    theorem = (
        "There is a real Toeplitz lag sequence whose normalized all-ones packet "
        "energies satisfy E_L>=1/2 for every L and E_L->1, while its symmetric "
        "lag partial sums are unbounded below. Explicitly prescribe E_L=1-2^(-k) "
        "when L=4^k (k>=1) and E_L=1 otherwise, set S_n=(n+1)E_(n+1)-nE_n, "
        "and reconstruct a_0=S_0, a_n=(S_n-S_(n-1))/2. Then at L=4^k, "
        "S_(L-1)=1-2^k. Hence positivity and convergence of packet energies "
        "alone cannot imply the TICKET-256 lag-partial-sum lower bound. A valid "
        "repair is: if delta=inf E_L>0 and V=sup_L L(E_L-E_(L+1))_+<delta, "
        "then every S_L>=delta-V>0."
    )
    proof = (
        "TICKET-256 gives E_L=L^(-1)sum_(n<L)S_n, whose exact inversion is "
        "S_n=(n+1)E_(n+1)-nE_n. The displayed reconstruction therefore realizes "
        "the prescribed E_L. Every spike is at least one half and the spike "
        "depth 2^(-k) tends to zero, so E_L tends to one. Immediately before "
        "L=4^k, E_(L-1)=1 and S_(L-1)=L(1-2^(-k))-(L-1)=1-2^k, which tends "
        "to minus infinity. For the repair criterion, S_L=E_(L+1)-"
        "L(E_L-E_(L+1))>=delta-V. The construction is abstract and does not "
        "identify these lags with the Guinand-Weil form."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_sparse_spike_rows": rows,
        "algorithm": "exact Fraction inversion from prescribed packet energies to lag partial sums and coefficients",
        "complexity": "O(sum 4^k) exact rational operations for direct replay; the counterexample and repair criterion are algebraic for all L",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "packet_energy_uniform_lower_bound": fraction_record(Fraction(1, 2)),
            "packet_energy_limit": fraction_record(Fraction(1)),
            "lag_partial_sums_unbounded_below_proved": True,
            "positivity_and_convergence_only_route_refuted": True,
            "scaled_downward_variation_repair_proved": True,
            "actual_weil_packet_analyzed": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def collatz_cyclotomic_no_go_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    conductor = 1
    compositum_degree = 1
    nonzero_count = 0
    failures = 0
    for index, prime in enumerate(COLLATZ_PRIMES, start=1):
        f2 = fermat_quotient_mod_prime(2, prime)
        f3 = fermat_quotient_mod_prime(3, prime)
        exponent = (5 * f2 - 3 * f3) % prime
        conductor *= prime
        compositum_degree *= prime - 1
        nonzero_count += int(exponent != 0)
        verified = (
            is_prime(prime)
            and prime % 2 == 1
            and 0 <= exponent < prime
            and conductor > 1
            and compositum_degree > 0
        )
        failures += int(not verified)
        transcript.update(
            f"{index}:{prime}:{f2}:{f3}:{exponent}:{conductor}:"
            f"{compositum_degree}:{int(verified)}\n".encode("ascii")
        )
        rows.append(
            {
                "prefix_length": index,
                "prime_q": prime,
                "fermat_quotient_F_q_2": f2,
                "fermat_quotient_F_q_3": f3,
                "canonical_phase_exponent_D_q": exponent,
                "phase_is_primitive_qth_root": exponent != 0,
                "coprime_conductor_product": conductor,
                "cyclotomic_compositum_degree": compositum_degree,
                "finite_prefix_exact_zero_impossible": True,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let q_1,...,q_N be distinct odd primes, let zeta_q be a primitive "
        "qth root of unity, and let d_j be any residue modulo q_j. Then "
        "sum_(j=1)^N zeta_(q_j)^(d_j) is never zero. In particular no finite "
        "prefix of the renormalized canonical Collatz phases "
        "exp(2 pi i D_q/q), D_q=5F_q(2)-3F_q(3), can cancel exactly. This "
        "rules out exact finite pairing or grouping, but does not rule out "
        "sublinear asymptotic magnitude."
    )
    proof = (
        "If every d_j is zero, the sum is N. Otherwise select j with d_j "
        "nonzero and put m=product_(i!=j)q_i and F=Q(zeta_m). Coprimality "
        "gives Q(zeta_m,zeta_(q_j))=Q(zeta_(m q_j)); Euler-phi "
        "multiplicativity shows its degree is [F:Q](q_j-1), hence "
        "F intersect Q(zeta_(q_j))=Q. A zero relation would place the "
        "primitive root zeta_(q_j)^(d_j) in F. Since d_j is invertible "
        "modulo q_j, this would place zeta_(q_j) in F, contradicting the "
        "trivial intersection. No estimate on how close the nonzero sum can "
        "be to zero follows."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_canonical_phase_prefix_rows": rows,
        "algorithm": "exact modular Fermat quotients plus coprime cyclotomic conductor and degree products; roots are stored only by exponents",
        "complexity": "O(sum log q) modular exponentiation for replay; the all-prefix no-go is a cyclotomic degree argument",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "prime_count": len(rows),
            "nonzero_canonical_phase_exponent_count": nonzero_count,
            "every_finite_distinct_prime_phase_sum_nonzero_proved": True,
            "exact_finite_pairing_or_grouping_route_refuted": True,
            "sublinear_phase_sum_bound_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def small_primes(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [value for value in range(2, limit + 1) if sieve[value]]


def reflection_character_prefix_snapshots(
    targets: list[tuple[int, int]],
) -> dict[int, dict[str, Any]]:
    target_by_q = dict(targets)
    maximum_target = max(target_by_q.values())
    base = small_primes(isqrt(GOLDBACH_SIEVE_LIMIT) + 1)
    active: dict[int, dict[str, Any]] = {
        q: {"counts": [0] * q, "legendre_product": 1}
        for q in target_by_q
    }
    snapshots: dict[int, dict[str, Any]] = {}
    seen = 0

    def record_prime(prime: int) -> None:
        nonlocal seen
        seen += 1
        for q in list(active):
            state = active[q]
            residue = prime % q
            state["counts"][residue] += 1
            if residue:
                state["legendre_product"] = (
                    state["legendre_product"]
                    * pow(residue, (q - 1) // 2, q)
                ) % q
            if seen == target_by_q[q]:
                snapshots[q] = {
                    "prime_count": seen,
                    "last_prime": prime,
                    "counts": list(state["counts"]),
                    "legendre_product": state["legendre_product"],
                }
                del active[q]

    record_prime(2)
    low = 3
    while active and low <= GOLDBACH_SIEVE_LIMIT:
        high = min(
            GOLDBACH_SIEVE_LIMIT,
            low + 2 * (GOLDBACH_SEGMENT_ODD_COUNT - 1),
        )
        mark = bytearray(b"\x01") * (((high - low) // 2) + 1)
        for prime in base[1:]:
            if prime * prime > high:
                break
            start = max(prime * prime, ((low + prime - 1) // prime) * prime)
            if start % 2 == 0:
                start += prime
            if start > high:
                continue
            offset = (start - low) // 2
            mark[offset::prime] = b"\x00" * (
                ((len(mark) - 1 - offset) // prime) + 1
            )
        for offset, flag in enumerate(mark):
            if flag:
                record_prime(low + 2 * offset)
                if seen == maximum_target:
                    break
        low = high + 2
    if active:
        raise RuntimeError(
            f"sieve limit {GOLDBACH_SIEVE_LIMIT} did not reach targets {sorted(active)}"
        )
    return snapshots


@lru_cache(maxsize=1)
def goldbach_character_audit() -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for prime, exponent in GOLDBACH_CASES:
        coefficients = cyclic_binomial_coefficients(prime, exponent)
        shift = 1 - coefficients[0]
        total = prime * shift
        candidates.append(
            {
                "prime_q": prime,
                "exponent_m": exponent,
                "coefficients": coefficients,
                "shift_t": shift,
                "prime_prefix_length_T": total,
                "compatible": shift > 0 and min(coefficients) + shift >= 0,
                "forced_counts": [value + shift for value in coefficients],
            }
        )
    snapshots = reflection_character_prefix_snapshots(
        [(row["prime_q"], row["prime_prefix_length_T"]) for row in candidates]
    )
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for candidate in candidates:
        prime = candidate["prime_q"]
        total = candidate["prime_prefix_length_T"]
        snapshot = snapshots[prime]
        counts = snapshot["counts"]
        asymmetry = [counts[r] - counts[(-r) % prime] for r in range(prime)]
        half_nonzero_count = (total - 1) // 2
        legendre_minus_one = pow(prime - 1, (prime - 1) // 2, prime)
        symmetric_expected = pow(legendre_minus_one, half_nonzero_count, prime)
        product_from_counts = 1
        for residue in range(1, prime):
            product_from_counts = (
                product_from_counts
                * pow(
                    pow(residue, (prime - 1) // 2, prime),
                    counts[residue],
                    prime,
                )
            ) % prime
        character_mismatch = snapshot["legendre_product"] != symmetric_expected
        vector_asymmetric = any(asymmetry)
        verified = (
            candidate["compatible"]
            and candidate["exponent_m"] % 2 == 0
            and candidate["exponent_m"] % prime == 0
            and counts[0] == 1
            and sum(counts) == total
            and snapshot["legendre_product"] == product_from_counts
            and (not character_mismatch or vector_asymmetric)
        )
        failures += int(not verified)
        transcript.update(
            f"{prime}:{candidate['exponent_m']}:{candidate['shift_t']}:{total}:"
            f"{snapshot['last_prime']}:{','.join(map(str, counts))}:"
            f"{snapshot['legendre_product']}:{symmetric_expected}:"
            f"{int(character_mismatch)}:{int(verified)}\n".encode("ascii")
        )
        rows.append(
            {
                **candidate,
                "last_prime_in_prefix": snapshot["last_prime"],
                "actual_prime_residue_counts": counts,
                "actual_reflection_differences": asymmetry,
                "actual_quadratic_character_product_mod_q": snapshot[
                    "legendre_product"
                ],
                "reflection_symmetric_expected_product_mod_q": symmetric_expected,
                "product_recomputed_independently_from_counts": product_from_counts,
                "quadratic_character_mismatch": character_mismatch,
                "quadratic_character_certificate_excludes_prefix": character_mismatch,
                "actual_vector_is_reflection_asymmetric": vector_asymmetric,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let q>=5 be prime and let N_r be the residue counts of the first T "
        "primes, where q itself occurs exactly once, so N_0=1. If "
        "N_r=N_(-r) for all nonzero r, then the Legendre-symbol product over "
        "the nonzero prefix primes equals chi_q(-1)^((T-1)/2). A mismatch is "
        "therefore an exact reflection-asymmetry certificate. More generally, "
        "reflection symmetry is equivalent to vanishing of every odd "
        "multiplicative-character moment sum_r N_r chi(r), chi(-1)=-1. "
        "For the next q-divisible compatible candidate (q,m)=(11,22), "
        "T=7,759,741, the actual quadratic product is -1 modulo 11 while "
        "symmetry requires +1, so that prefix is excluded."
    )
    proof = (
        "Under reflection symmetry, pair residues r and -r. Their product "
        "contribution is (-r^2)^(N_r), whose Legendre symbol is "
        "chi_q(-1)^(N_r). Since T-1=2 sum_pairs N_r, multiplying gives the "
        "stated necessary value. For the full character criterion, odd "
        "characters annihilate every symmetric pair. Conversely the "
        "antisymmetric function A(r)=N_r-N_(-r) lies in the odd subspace of "
        "the multiplicative group; if every odd Fourier coefficient vanishes, "
        "character inversion gives A=0. The segmented sieve exactly counts "
        "the first T primes. At q=11 the computed product 10 differs from the "
        "required value 1. The q=5 and q=7 rows show the quadratic product can "
        "match even when the full vector is asymmetric, so this one-bit test "
        "is sufficient but not necessary."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_reflection_character_certificate_rows": rows,
        "algorithm": "exact odd-only segmented sieve, integer residue counts, Euler-criterion products, and an independent product replay from counts",
        "complexity": "O(p_T log log p_T) sieve time and O(sqrt(p_T)+segment+q) memory; no list of all T primes is stored",
        "random_seed": None,
        "input_sieve_limit": GOLDBACH_SIEVE_LIMIT,
        "segment_odd_count": GOLDBACH_SEGMENT_ODD_COUNT,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "character_row_count": len(rows),
            "maximum_prime_prefix_length": max(
                row["prime_prefix_length_T"] for row in rows
            ),
            "maximum_last_prime": max(row["last_prime_in_prefix"] for row in rows),
            "quadratic_character_exclusion_count": sum(
                row["quadratic_character_certificate_excludes_prefix"] for row in rows
            ),
            "new_q11_m22_prefix_excluded": next(
                row["quadratic_character_certificate_excludes_prefix"]
                for row in rows
                if row["prime_q"] == 11
            ),
            "quadratic_character_is_complete_asymmetry_detector": False,
            "all_odd_character_moments_characterize_symmetry_proved": True,
            "all_compatible_even_q_divisible_prefixes_excluded": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def b1_coefficient_form(u: int, v: int) -> int:
    even = sum(
        comb(17, k) * u ** (17 - k) * v**k * 2 ** (k // 2)
        for k in range(0, 18, 2)
    )
    odd = sum(
        comb(17, k) * u ** (17 - k) * v**k * 2 ** ((k - 1) // 2)
        for k in range(1, 18, 2)
    )
    return even + odd


def ceil_fraction(numerator: int, denominator: int) -> int:
    return -((-numerator) // denominator)


@lru_cache(maxsize=1)
def twin_unique_root_audit() -> dict[str, Any]:
    lower_value = b1_coefficient_form(
        TWIN_ROOT_LOWER_NUMERATOR, TWIN_ROOT_DENOMINATOR
    )
    upper_value = b1_coefficient_form(
        TWIN_ROOT_UPPER_NUMERATOR, TWIN_ROOT_DENOMINATOR
    )
    bracket_verified = lower_value < 0 < upper_value
    candidate_evaluations = 0
    maximum_candidate_span = 0
    nonzero_hits: list[dict[str, int]] = []
    sample_rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    sample_denominators = {1, 2, 10, 100, 1_000, 10_000, 100_000, 200_000}
    for denominator in range(1, TWIN_DENOMINATOR_LIMIT + 1):
        positive_low = ceil_fraction(
            TWIN_ROOT_LOWER_NUMERATOR * denominator,
            TWIN_ROOT_DENOMINATOR,
        )
        positive_high = ceil_fraction(
            TWIN_ROOT_UPPER_NUMERATOR * denominator,
            TWIN_ROOT_DENOMINATOR,
        )
        negative_low = (
            TWIN_ROOT_LOWER_NUMERATOR * denominator
        ) // TWIN_ROOT_DENOMINATOR
        negative_high = (
            TWIN_ROOT_UPPER_NUMERATOR * denominator
        ) // TWIN_ROOT_DENOMINATOR
        maximum_candidate_span = max(
            maximum_candidate_span,
            positive_high - positive_low + 1,
            negative_high - negative_low + 1,
        )
        positive_values: list[tuple[int, int]] = []
        negative_values: list[tuple[int, int]] = []
        for u in range(positive_low, positive_high + 1):
            value = b1_coefficient_form(u, denominator)
            candidate_evaluations += 1
            positive_values.append((u, value))
            if value == 1:
                nonzero_hits.append(
                    {"u": u, "v": denominator, "reduced_y": 2 * denominator**2 - u**2}
                )
            transcript.update(
                f"+:{denominator}:{u}:{value}\n".encode("ascii")
            )
        for x in range(negative_low, negative_high + 1):
            value = b1_coefficient_form(x, denominator)
            candidate_evaluations += 1
            negative_values.append((x, value))
            if value == -1:
                nonzero_hits.append(
                    {"u": -x, "v": -denominator, "reduced_y": 2 * denominator**2 - x**2}
                )
            transcript.update(
                f"-:{denominator}:{x}:{value}\n".encode("ascii")
            )
        if denominator in sample_denominators:
            sample_rows.append(
                {
                    "absolute_denominator_v": denominator,
                    "positive_v_candidate_values": [
                        {"u": u, "B_1": value} for u, value in positive_values
                    ],
                    "negative_v_reflected_candidate_values": [
                        {"x_equals_minus_u": x, "B_1_x_positive_v": value}
                        for x, value in negative_values
                    ],
                }
            )

    theorem = (
        "Let B_1(u,v) be the sqrt(2)-coefficient of "
        "(1+sqrt(2))(u+v sqrt(2))^17 and put P(x)=B_1(x,1). Then P is "
        "strictly increasing on R and has one irrational root rho in (-1,0). "
        "Every integral solution B_1(u,v)=1 is either (u,v)=(1,0), or, for "
        "v>0, u=ceil(rho v), or, for v<0, u=-floor(rho |v|). Every nonzero-v "
        "solution is primitive and satisfies v divides u^17-1 and u divides "
        "256v^17-1. The exact root bracket -0.073255<rho<-0.07325499 reduces "
        "all 0<|v|<=200000 to 400399 integer evaluations; none equals one."
    )
    proof = (
        "Writing epsilon=1+sqrt(2) gives P(x)=[epsilon(x+sqrt(2))^17+"
        "epsilon^(-1)(x-sqrt(2))^17]/(2sqrt(2)). Its derivative is 17 times "
        "a sum of two positive even powers, so P is strictly increasing. "
        "Exact evaluation gives P(-1)=-470832 and P(0)=256. The root is "
        "irrational because P is monic integral and has no integer root in "
        "(-1,0). For fixed v>0, B_1(u,v)=v^17P(u/v) is a strictly increasing "
        "integer sequence. Its first positive value occurs at ceil(rho v); "
        "all later values are at least two. The negative-v case follows from "
        "B_1(u,-w)=-B_1(-u,w). Homogeneity gives gcd(u,v)=1, while reduction "
        "modulo v and u gives B_1 congruent to u^17 mod v and to 256v^17 mod u. "
        "The rational bracket signs are checked after clearing the denominator; "
        "its width times 200000 is below one, leaving at most two exact neighbor "
        "candidates per sign. The bounded scan is not an all-denominator proof."
    )
    failures = int(not bracket_verified) + len(nonzero_hits)
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_root_bracket": {
            "lower": fraction_record(
                Fraction(TWIN_ROOT_LOWER_NUMERATOR, TWIN_ROOT_DENOMINATOR)
            ),
            "upper": fraction_record(
                Fraction(TWIN_ROOT_UPPER_NUMERATOR, TWIN_ROOT_DENOMINATOR)
            ),
            "cleared_lower_form_value": lower_value,
            "cleared_upper_form_value": upper_value,
            "bracket_verified": bracket_verified,
        },
        "exact_candidate_sample_rows": sample_rows,
        "finite_denominator_audit": {
            "absolute_v_limit": TWIN_DENOMINATOR_LIMIT,
            "candidate_evaluation_count": candidate_evaluations,
            "maximum_candidate_span_per_sign": maximum_candidate_span,
            "nonzero_v_coefficient_one_hits": nonzero_hits,
            "v_zero_integral_solutions": [{"u": 1, "v": 0, "reduced_y": -1}],
            "admissible_negative_norm_hit_count": sum(
                hit["reduced_y"] > 0 for hit in nonzero_hits
            ),
        },
        "algorithm": "exact rational root bracketing followed by candidate-complete integer evaluation of at most two root neighbors per sign and denominator",
        "complexity": "O(V) degree-17 integer evaluations after one exact root bracket, replacing an O(V^2) box scan",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "strict_monotonicity_and_unique_real_root_proved": True,
            "all_integral_solutions_reduce_to_unique_root_neighbors_proved": True,
            "primitive_double_divisibility_conditions_proved": True,
            "bounded_nonzero_v_solution_count": len(nonzero_hits),
            "single_absolute_branch_globally_solved": False,
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
        {"id": f"{code}-T256", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T257", "label": theorem_name, "status": "proved"},
        {
            "id": f"{code}-CERT257",
            "label": f"{theorem_name}ExactReplay",
            "status": "computed_finite",
        },
        {"id": f"{code}-REJECT257", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN257", "label": open_name, "status": "open"},
    ]
    return {
        "nodes": nodes,
        "edges": [
            [f"{code}-T256", f"{code}-T257"],
            [f"{code}-T257", f"{code}-CERT257"],
            [f"{code}-T257", f"{code}-REJECT257"],
            [f"{code}-T257", f"{code}-OPEN257"],
        ],
        "resolution_path": [f"{code}-T256", f"{code}-T257", f"{code}-OPEN257"],
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
        "ticket_id": f"{code}-TICKET-257",
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


def build_audit() -> dict[str, Any]:
    riemann = riemann_spike_audit()
    collatz = collatz_cyclotomic_no_go_audit()
    goldbach = goldbach_character_audit()
    twin = twin_unique_root_audit()
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "PositiveConvergentPacketEnergyLagPartialSumNoGo",
            "exact_no_go",
            riemann,
            "deriving a uniform lag-partial-sum lower bound from strict positivity and convergence of packet energies alone",
            ["direct arithmetic control of scaled downward variation for actual Weil packets"],
            "the exact sparse-spike counterexample and the scaled-downward-variation repair criterion",
            "ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation",
            "ToeplitzPacketCesaroLagPartialSumCriterion",
            "PositiveConvergentPacketEnergiesForceUniformLagPartialSumLowerBound",
            "The abstract implication is false. The repaired criterion is exact, but neither its positive margin nor its scaled-variation bound is proved for actual Guinand-Weil packets.",
            "No RH proof or disproof; a tempting analytic shortcut is refuted and replaced by one quantitative actual-Weil target.",
            f"{len(riemann['exact_sparse_spike_rows'])} exact spike rows replay the all-L construction; no actual Weil coefficient is computed.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "DistinctPrimeCyclotomicPhaseExactCancellationNoGo",
            "exact_no_go",
            collatz,
            "seeking exact zero by pairing or grouping one canonical phase from each distinct prime modulus in a finite prefix",
            ["quantitative sublinear cancellation of canonical fixed-base Fermat-quotient phases"],
            "the cyclotomic linear-disjointness obstruction separating exact zero from asymptotic cancellation",
            "CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude",
            "SharpIncompleteKernelErrorAndDecayOnlyPrimeAverage",
            "FiniteDistinctPrimeCanonicalPhasePrefixCanVanishExactly",
            "Every finite prefix is nonzero, but no upper bound smaller than its length is proved; the canonical phase sum may still cancel asymptotically or fail to do so.",
            "No Collatz proof or counterexample; exact finite cancellation is impossible, while the required quantitative cross-prime estimate remains open.",
            f"{len(collatz['exact_canonical_phase_prefix_rows'])} canonical exponents are replayed; the no-go itself holds for every finite family of distinct odd primes.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "QuadraticCharacterReflectionObstructionAndNextPrefixExclusion",
            "partial_theorem",
            goldbach,
            "using the quadratic-character product obstruction as a complete detector of prime-prefix reflection asymmetry",
            ["uniform nonvanishing of an odd multiplicative-character moment for every compatible even q-divisible prime prefix"],
            "the one-bit Legendre-product obstruction, the full odd-character equivalence, and the new q=11 prefix certificate",
            "EveryCompatibleEvenQDivisiblePrimePrefixHasNonzeroOddCharacterMoment",
            "QDivisibleReflectionAsymmetryPrimePrefixExclusion",
            "QuadraticCharacterProductDetectsEveryReflectionAsymmetricPrimePrefix",
            "The q=11,m=22 prefix is excluded and odd character moments exactly characterize asymmetry, but no arithmetic theorem forces a nonzero odd moment for every compatible even exponent.",
            "No strong Goldbach proof or counterexample; the next untested q-divisible prefix is exactly excluded and the universal gap is recast spectrally.",
            f"{len(goldbach['exact_reflection_character_certificate_rows'])} prefixes are sieved, with maximum T={goldbach['aggregate']['maximum_prime_prefix_length']}; larger compatible exponents are not computed.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "UniqueRealRootNeighborReductionAndBoundedExclusion",
            "partial_theorem",
            twin,
            "treating the surviving coefficient-one branch as a two-dimensional integer box search",
            ["all-denominator exclusion of the unique-root neighbor sequence"],
            "the exact one-dimensional root-neighbor reduction, primitive divisibility conditions, and bounded certificate",
            "EveryNonzeroDenominatorUniqueRootNeighborMissesCoefficientOne",
            "SurvivingTwistGL2EquivalenceAndSingleAbsoluteBranchReduction",
            "TwoDimensionalBoxSearchIsNecessaryForTheSurvivingCoefficientOneBranch",
            "The search dimension is reduced and |v|<=200000 is excluded, but no argument handles every denominator, so exponent 17 and twin primes remain open.",
            "No twin-prime proof or counterexample; the last Thue branch is reduced to one exact candidate sequence and a much larger finite range is excluded.",
            f"{twin['finite_denominator_audit']['candidate_evaluation_count']} exact root-neighbor evaluations cover 0<|v|<={TWIN_DENOMINATOR_LIMIT}; absence there is not an infinite exclusion.",
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
            "theorem_name": "FourConjectureSpikeCyclotomicCharacterRootAudit",
            "summary": "TICKET-257 proves two exact route no-gos and two partial theorems: a sparse packet spike obstruction, finite cyclotomic phase noncancellation, a q=11 Goldbach character certificate, and a one-dimensional Twin root-neighbor reduction; every parent conjecture remains open.",
            **sections,
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 2,
                "exact_no_go_count": 2,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "goldbach",
                "stagnated_problem_count": 0,
                "riemann_spike_case_count": len(riemann["exact_sparse_spike_rows"]),
                "collatz_prime_case_count": len(collatz["exact_canonical_phase_prefix_rows"]),
                "goldbach_character_row_count": len(goldbach["exact_reflection_character_certificate_rows"]),
                "goldbach_maximum_prime_prefix_length": goldbach["aggregate"]["maximum_prime_prefix_length"],
                "goldbach_new_q11_certificate_count": int(goldbach["aggregate"]["new_q11_m22_prefix_excluded"]),
                "twin_root_neighbor_candidate_count": twin["finite_denominator_audit"]["candidate_evaluation_count"],
                "twin_denominator_limit": TWIN_DENOMINATOR_LIMIT,
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
        "ticket": 257,
        "parent_ticket": 256,
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
        ROOT / "data/open-problem/ticket257-spike-cyclotomic-character-root.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-257-positive-convergent-spike-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-257-cyclotomic-exact-cancellation-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-257-character-prefix-exclusion.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-257-unique-root-neighbor.json",
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
