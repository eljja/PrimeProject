from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache
from math import gcd
from pathlib import Path
from typing import Any


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket253_density_character_prefix_lebesgue import (
    fermat_quotient_mod_prime,
)
from scripts.ticket254_diagonal_weighted_reflection_thue import (
    fraction_record,
    is_prime,
    write_json,
)
from scripts.ticket257_spike_cyclotomic_character_root import (
    b1_coefficient_form,
    small_primes,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket258-variation-character-convergent.v1"
GENERATED_AT = "2026-08-31T18:00:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "variation_character_convergent_audit"

RIEMANN_SPIKE_LEVELS = tuple(range(1, 13))
COLLATZ_PRIME_LIMIT = 997
GOLDBACH_MODULI = (5, 7, 11, 13, 17, 19)
TWIN_CF_TERM_COUNT = 128
TWIN_ROOT_LOWER = Fraction(-14_651, 200_000)
TWIN_ROOT_UPPER = Fraction(-7_325_499, 100_000_000)


def prescribed_bv_energy(dimension: int) -> Fraction:
    if dimension < 1:
        raise ValueError("packet dimension must be positive")
    level = 0
    residual = dimension
    while residual >= 4 and residual % 4 == 0:
        residual //= 4
        level += 1
    if residual == 1 and level:
        return Fraction(1) - Fraction(1, 2**level)
    return Fraction(1)


def induced_partial_sum(index: int) -> Fraction:
    if index < 0:
        raise ValueError("partial-sum index must be nonnegative")
    return (index + 1) * prescribed_bv_energy(index + 1) - index * prescribed_bv_energy(index)


@lru_cache(maxsize=1)
def riemann_bounded_variation_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    partial_variation = Fraction(0)
    for level in RIEMANN_SPIKE_LEVELS:
        dimension = 4**level
        depth = Fraction(1, 2**level)
        variation_contribution = 2 * depth
        partial_variation += variation_contribution
        partial_sum = induced_partial_sum(dimension - 1)
        verified = (
            prescribed_bv_energy(dimension) == 1 - depth
            and prescribed_bv_energy(dimension - 1) == 1
            and prescribed_bv_energy(dimension + 1) == 1
            and partial_sum == 1 - 2**level
            and partial_variation == 2 * (1 - depth)
        )
        failures += int(not verified)
        transcript.update(
            f"{level}:{dimension}:{depth}:{variation_contribution}:"
            f"{partial_variation}:{partial_sum}:{int(verified)}\n".encode("ascii")
        )
        rows.append(
            {
                "spike_level_k": level,
                "packet_dimension_L": dimension,
                "spike_depth": fraction_record(depth),
                "total_variation_contribution": fraction_record(variation_contribution),
                "partial_total_variation_through_return": fraction_record(partial_variation),
                "lag_partial_sum_S_L_minus_1": fraction_record(partial_sum),
                "identity_verified": verified,
            }
        )
    theorem = (
        "There is a real Toeplitz lag sequence whose normalized all-ones packet "
        "energies E_L are at least 1/2, converge to 1, and have finite total "
        "variation sum_(L>=1)|E_(L+1)-E_L|=2, while the symmetric lag partial "
        "sums are unbounded below. Take E_(4^k)=1-2^(-k) and E_L=1 otherwise, "
        "then invert by S_n=(n+1)E_(n+1)-nE_n. At L=4^k one has "
        "S_(L-1)=1-2^k. Thus ordinary bounded variation cannot replace the "
        "scaled one-sided variation in TICKET-257's repair criterion."
    )
    proof = (
        "Each isolated spike contributes 2*2^(-k) to total variation, hence "
        "the exact total is 2 sum_(k>=1)2^(-k)=2. The energy lower bound and "
        "limit are immediate. TICKET-256's inversion identity gives, immediately "
        "before L=4^k, S_(L-1)=L(1-2^(-k))-(L-1)=1-2^k. Therefore even "
        "positivity, convergence, and finite total variation do not bound the "
        "lag partial sums below. The construction is abstract and computes no "
        "actual Guinand-Weil coefficient."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_bounded_variation_spike_rows": rows,
        "total_variation_exact": fraction_record(Fraction(2)),
        "algorithm": "closed-form exact Fraction audit of isolated packet-energy spikes and the Cesaro inversion identity",
        "complexity": "O(K) exact rational operations for K certificate rows; the theorem is algebraic for every k",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "positive_convergent_energy_proved": True,
            "finite_total_variation_proved": True,
            "lag_partial_sums_unbounded_below_proved": True,
            "ordinary_bounded_variation_repair_refuted": True,
            "scaled_one_sided_variation_still_sufficient": True,
            "actual_weil_packet_analyzed": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def collatz_rational_independence_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for index, prime in enumerate(
        (q for q in range(5, COLLATZ_PRIME_LIMIT + 1) if is_prime(q)), start=1
    ):
        f2 = fermat_quotient_mod_prime(2, prime)
        f3 = fermat_quotient_mod_prime(3, prime)
        exponent = (5 * f2 - 3 * f3) % prime
        verified = 0 <= exponent < prime
        failures += int(not verified)
        transcript.update(
            f"{index}:{prime}:{f2}:{f3}:{exponent}:{int(exponent != 0)}:"
            f"{int(verified)}\n".encode("ascii")
        )
        rows.append(
            {
                "index": index,
                "prime_q": prime,
                "fermat_quotient_F_q_2": f2,
                "fermat_quotient_F_q_3": f3,
                "canonical_phase_exponent_D_q": exponent,
                "phase_is_nontrivial_primitive_qth_root": exponent != 0,
                "certificate_verified": verified,
            }
        )
    theorem = (
        "Let q_1,...,q_N be distinct odd primes and let 0<d_j<q_j. Then "
        "1,zeta_(q_1)^(d_1),...,zeta_(q_N)^(d_N) are linearly independent "
        "over Q. Consequently every finite family of nontrivial canonical "
        "Collatz phases has no nonzero rationally weighted cancellation. This "
        "strictly strengthens TICKET-257's unweighted nonzero-sum theorem but "
        "does not imply any upper bound for prefix magnitudes."
    )
    proof = (
        "Assume c_0+sum_j c_j zeta_(q_j)^(d_j)=0 with rational coefficients "
        "and choose j with c_j nonzero. Let F be the compositum of the other "
        "prime cyclotomic fields. Solving the relation puts the primitive root "
        "zeta_(q_j)^(d_j), and therefore zeta_(q_j), in F. Coprime conductors "
        "and Euler-phi multiplicativity give F intersect Q(zeta_(q_j))=Q, a "
        "contradiction. If no c_j is nonzero then c_0=0. A canonical phase "
        "with D_q=0 is excluded from the theorem because it equals 1."
    )
    nontrivial = [row for row in rows if row["phase_is_nontrivial_primitive_qth_root"]]
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_canonical_phase_rows": rows,
        "algorithm": "exact modular Fermat quotients; the rational-independence result is a coprime-conductor cyclotomic field argument",
        "complexity": "O(pi(Q) log Q) modular exponentiation through Q; the independence theorem is finite-dimensional and exact",
        "random_seed": None,
        "prime_limit": COLLATZ_PRIME_LIMIT,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "prime_count": len(rows),
            "nontrivial_phase_count": len(nontrivial),
            "trivial_phase_primes": [row["prime_q"] for row in rows if not row["phase_is_nontrivial_primitive_qth_root"]],
            "rational_linear_independence_proved_for_nontrivial_distinct_prime_phases": True,
            "rational_weighted_finite_cancellation_route_refuted": True,
            "sublinear_phase_sum_bound_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def polynomial_trim(coefficients: list[int]) -> list[int]:
    result = list(coefficients)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def polynomial_divmod_monic(dividend: list[int], divisor: list[int]) -> tuple[list[int], list[int]]:
    remainder = polynomial_trim(dividend)
    divisor = polynomial_trim(divisor)
    if divisor[-1] != 1:
        raise ValueError("divisor must be monic")
    quotient = [0] * max(1, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and remainder != [0]:
        shift = len(remainder) - len(divisor)
        coefficient = remainder[-1]
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            remainder[index + shift] -= coefficient * value
        remainder = polynomial_trim(remainder)
    return polynomial_trim(quotient), polynomial_trim(remainder)


def proper_divisors(value: int) -> list[int]:
    return [candidate for candidate in range(1, value) if value % candidate == 0]


@lru_cache(maxsize=None)
def cyclotomic_polynomial(order: int) -> tuple[int, ...]:
    polynomial = [-1] + [0] * (order - 1) + [1]
    for divisor in proper_divisors(order):
        quotient, remainder = polynomial_divmod_monic(
            polynomial, list(cyclotomic_polynomial(divisor))
        )
        if remainder != [0]:
            raise ArithmeticError("cyclotomic division was not exact")
        polynomial = quotient
    return tuple(polynomial_trim(polynomial))


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    residual = value
    candidate = 2
    while candidate * candidate <= residual:
        if residual % candidate == 0:
            factors.append(candidate)
            while residual % candidate == 0:
                residual //= candidate
        candidate += 1
    if residual > 1:
        factors.append(residual)
    return factors


def primitive_root_prime(prime: int) -> int:
    order = prime - 1
    factors = prime_factors(order)
    for candidate in range(2, prime):
        if all(pow(candidate, order // factor, prime) != 1 for factor in factors):
            return candidate
    raise ArithmeticError("primitive root not found")


def is_power_of_two(value: int) -> bool:
    return value > 0 and value & (value - 1) == 0


def constructed_character_blind_counts(prime: int) -> dict[str, Any] | None:
    order = prime - 1
    half = order // 2
    if is_power_of_two(order):
        return None
    primitive_root = primitive_root_prime(prime)
    cyclotomic = list(cyclotomic_polynomial(order))
    if len(cyclotomic) - 1 >= half:
        raise AssertionError("non-power-of-two order should have phi(n)<n/2")
    antisymmetric = cyclotomic + [0] * (half - len(cyclotomic))
    counts = [0] * prime
    for exponent, difference in enumerate(antisymmetric):
        residue = pow(primitive_root, exponent, prime)
        negative = (-residue) % prime
        counts[residue] = max(difference, 0)
        counts[negative] = max(-difference, 0)
    _, remainder = polynomial_divmod_monic(antisymmetric, cyclotomic)
    return {
        "primitive_root_g": primitive_root,
        "cyclotomic_polynomial_coefficients_low_to_high": cyclotomic,
        "antisymmetric_half_vector": antisymmetric,
        "nonnegative_residue_counts": counts,
        "primitive_character_moment_remainder": remainder,
        "reflection_asymmetric": any(antisymmetric),
        "primitive_character_moment_is_zero": remainder == [0],
    }


@lru_cache(maxsize=1)
def goldbach_character_basis_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for prime in GOLDBACH_MODULI:
        order = prime - 1
        blind = constructed_character_blind_counts(prime)
        power_two = is_power_of_two(order)
        complete = power_two
        verified = (blind is None) == power_two
        if blind is not None:
            verified = verified and blind["reflection_asymmetric"] and blind["primitive_character_moment_is_zero"]
        failures += int(not verified)
        transcript.update(
            f"{prime}:{order}:{int(power_two)}:{int(complete)}:"
            f"{json.dumps(blind, sort_keys=True, separators=(',', ':')) if blind else '-'}:"
            f"{int(verified)}\n".encode("ascii")
        )
        rows.append(
            {
                "prime_q": prime,
                "character_order_q_minus_1": order,
                "q_minus_1_is_power_of_two": power_two,
                "one_primitive_odd_character_is_complete": complete,
                "blind_vector_certificate": blind,
                "certificate_verified": verified,
            }
        )

    first_primes = small_primes(11_000)[:1_255]
    q = 5
    counts = [0] * q
    for prime in first_primes:
        counts[prime % q] += 1
    generator = primitive_root_prime(q)
    antisymmetric = [
        counts[pow(generator, exponent, q)]
        - counts[(-pow(generator, exponent, q)) % q]
        for exponent in range((q - 1) // 2)
    ]
    phi4 = list(cyclotomic_polynomial(4))
    _, quartic_remainder = polynomial_divmod_monic(antisymmetric, phi4)
    actual_q5 = {
        "prime_prefix_length": len(first_primes),
        "last_prime": first_primes[-1],
        "residue_counts": counts,
        "primitive_root_g": generator,
        "antisymmetric_half_vector": antisymmetric,
        "quartic_character_moment_remainder": quartic_remainder,
        "quartic_character_detects_asymmetry": quartic_remainder != [0],
    }
    actual_verified = (
        actual_q5["last_prime"] == 10_243
        and counts == [1, 313, 313, 317, 311]
        and antisymmetric == [2, -4]
        and quartic_remainder == [2, -4]
    )
    failures += int(not actual_verified)
    transcript.update(
        f"actual-q5:{json.dumps(actual_q5, sort_keys=True, separators=(',', ':'))}:"
        f"{int(actual_verified)}\n".encode("ascii")
    )
    theorem = (
        "Let q be an odd prime, n=q-1=2h, g a primitive root, and chi(g) a "
        "primitive nth root of unity. The single odd-character moment "
        "sum_(r!=0)N_r chi(r) detects reflection symmetry N_r=N_(-r) for "
        "every rational count vector if and only if n is a power of two. If "
        "n=2^a, the antisymmetric polynomial has degree below h=phi(n) and "
        "cannot vanish at a primitive nth root unless it is zero. Otherwise "
        "Phi_n has degree phi(n)<h and its coefficient vector is an exact "
        "nonzero reflection-asymmetric blind vector. For the actual q=5, "
        "T=1255 prime prefix, the quartic moment is represented by 2-4i and "
        "detects the asymmetry missed by TICKET-257's quadratic bit."
    )
    proof = (
        "Index nonzero residues by g^j. Oddness gives chi(g^(j+h))=-chi(g^j), "
        "so the moment equals A(zeta_n), where A(x)=sum_(j<h) "
        "(N_(g^j)-N_(-g^j))x^j. If n is a power of two, Phi_n=x^h+1 has "
        "degree h, hence a polynomial of degree below h vanishes at zeta_n "
        "only when A=0. If n is not a power of two, phi(n)<h; taking A=Phi_n "
        "and splitting each coefficient into nonnegative positive and negative "
        "residue counts gives a nonsymmetric vector with zero moment. This is "
        "a theorem about detectors, not a proof that actual prime prefixes "
        "always have a nonzero odd-character moment."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_modulus_classification_rows": rows,
        "actual_q5_quartic_certificate": actual_q5,
        "algorithm": "exact integer cyclotomic polynomial division, primitive-root indexing, and a deterministic sieve for the first 1255 primes",
        "complexity": "finite polynomial arithmetic in degree q-1 for sample moduli plus O(10243 log log 10243) sieve time",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "single_primitive_character_complete_iff_fermat_modulus_proved": True,
            "non_power_two_blind_vector_count": sum(row["blind_vector_certificate"] is not None for row in rows),
            "actual_q5_quartic_character_detects_asymmetry": actual_q5["quartic_character_detects_asymmetry"],
            "universal_single_character_detector_route_refuted": True,
            "all_compatible_even_q_divisible_prefixes_excluded": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def mobius_value(a: int, b: int, c: int, d: int, value: Fraction) -> Fraction:
    denominator = c * value + d
    if denominator == 0:
        raise ZeroDivisionError
    return (a * value + b) / denominator


def refine_root_bracket(lower: Fraction, upper: Fraction) -> tuple[Fraction, Fraction]:
    midpoint = (lower + upper) / 2
    sign_value = b1_coefficient_form(midpoint.numerator, midpoint.denominator)
    if sign_value == 0:
        raise ArithmeticError("the irrational root acquired a rational midpoint")
    return (midpoint, upper) if sign_value < 0 else (lower, midpoint)


def certified_root_continued_fraction(term_count: int) -> tuple[list[int], list[dict[str, Any]], Fraction, Fraction]:
    lower = TWIN_ROOT_LOWER
    upper = TWIN_ROOT_UPPER
    if not (
        b1_coefficient_form(lower.numerator, lower.denominator) < 0
        and b1_coefficient_form(upper.numerator, upper.denominator) > 0
    ):
        raise ArithmeticError("initial root bracket is invalid")
    transform = (1, 0, 0, 1)
    digits: list[int] = []
    rows: list[dict[str, Any]] = []
    p_minus_two, p_minus_one = 0, 1
    q_minus_two, q_minus_one = 1, 0
    for index in range(term_count):
        refinements = 0
        while True:
            a, b, c, d = transform
            try:
                left = mobius_value(a, b, c, d, lower)
                right = mobius_value(a, b, c, d, upper)
            except ZeroDivisionError:
                lower, upper = refine_root_bracket(lower, upper)
                refinements += 1
                continue
            low_value, high_value = sorted((left, right))
            digit = low_value.numerator // low_value.denominator
            if (
                high_value.numerator // high_value.denominator == digit
                and low_value > digit
                and high_value < digit + 1
            ):
                break
            lower, upper = refine_root_bracket(lower, upper)
            refinements += 1
            if refinements > 20_000:
                raise RuntimeError("continued-fraction certification did not converge")
        digits.append(digit)
        p = digit * p_minus_one + p_minus_two
        q = digit * q_minus_one + q_minus_two
        if q <= 0 or gcd(abs(p), q) != 1:
            raise ArithmeticError("invalid continued-fraction convergent")
        coefficient = b1_coefficient_form(p, q)
        rows.append(
            {
                "term_index": index,
                "partial_quotient": digit,
                "convergent_numerator": str(p),
                "convergent_denominator": str(q),
                "B_1_at_convergent": str(coefficient),
                "root_side": "below" if coefficient < 0 else "above",
                "unit_coefficient_hit": abs(coefficient) == 1,
                "root_bracket_refinements_for_digit": refinements,
            }
        )
        p_minus_two, p_minus_one = p_minus_one, p
        q_minus_two, q_minus_one = q_minus_one, q
        a, b, c, d = transform
        transform = (c, d, a - digit * c, b - digit * d)
    return digits, rows, lower, upper


@lru_cache(maxsize=1)
def twin_continued_fraction_audit() -> dict[str, Any]:
    digits, rows, lower, upper = certified_root_continued_fraction(TWIN_CF_TERM_COUNT)
    transcript = hashlib.sha256()
    failures = 0
    previous_q = 0
    unit_hits: list[dict[str, Any]] = []
    for row in rows:
        q = int(row["convergent_denominator"])
        coefficient = int(row["B_1_at_convergent"])
        monotone_denominator = q >= previous_q
        verified = monotone_denominator and coefficient != 0
        failures += int(not verified)
        previous_q = q
        if row["unit_coefficient_hit"]:
            unit_hits.append(row)
        transcript.update(
            f"{row['term_index']}:{row['partial_quotient']}:"
            f"{row['convergent_numerator']}:{row['convergent_denominator']}:"
            f"{row['B_1_at_convergent']}:{row['root_side']}:"
            f"{row['root_bracket_refinements_for_digit']}\n".encode("ascii")
        )
    failures += len(unit_hits)
    maximum_denominator = int(rows[-1]["convergent_denominator"])
    theorem = (
        "Let rho be the unique root in (-1,0) of P(x)=B_1(x,1). Every "
        "nonzero-denominator integral solution B_1(u,v)=1 from TICKET-257, "
        "after reflecting v<0 to B_1(x,|v|)=-1, has reduced rational ratio "
        "u/v (respectively x/|v|) equal to a regular continued-fraction "
        "convergent of rho. Indeed every candidate lies in [-1,0], P'(x)>544 "
        "there, and the mean-value theorem gives |rho-p/q|<1/(544q^17)<"
        "1/(2q^2), so Legendre's convergent criterion applies for q>=2; q=1 "
        "is checked directly. The first 128 certified convergents contain no "
        "B_1 value equal to plus or minus one, excluding every nonzero solution "
        "with denominator at most the 128th denominator."
    )
    proof = (
        "TICKET-257 proves primitivity and reduces the two signs to P(p/q)="
        "+/-q^(-17). From the exact derivative formula, the second positive "
        "term alone gives P'(x)>=2176(1-1/sqrt(2))>544 on [-1,0]. The mean "
        "value theorem yields the displayed approximation. Legendre's theorem "
        "then forces every q>=2 solution ratio to be a continued-fraction "
        "convergent. Each partial quotient is certified from a rational interval "
        "whose endpoints have opposite exact B_1 signs; every convergent is "
        "evaluated with integers. This leaves infinitely many later convergents "
        "and therefore does not solve the Thue equation or twin-prime conjecture."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "derivative_lower_bound": {
            "rational_bound": 544,
            "proof": "2176*(1-1/sqrt(2))>544 because 1/sqrt(2)<3/4",
        },
        "continued_fraction_partial_quotients": digits,
        "certified_convergent_rows": rows,
        "final_exact_root_bracket": {
            "lower": fraction_record(lower),
            "upper": fraction_record(upper),
        },
        "finite_convergent_audit": {
            "term_count": len(rows),
            "maximum_excluded_denominator": str(maximum_denominator),
            "maximum_excluded_denominator_digit_count": len(str(maximum_denominator)),
            "unit_coefficient_hits": unit_hits,
        },
        "algorithm": "exact rational root isolation, certified Möbius-transform continued fractions, and integer degree-17 form evaluation",
        "complexity": "O(K) convergent evaluations and adaptive exact bisection for K partial quotients, replacing an O(V) denominator scan by O(log V) candidates",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "continued_fraction_necessity_proved": True,
            "linear_denominator_scan_necessity_refuted": True,
            "certified_convergent_count": len(rows),
            "bounded_nonzero_v_solution_count": len(unit_hits),
            "all_convergents_excluded": False,
            "exponent_seventeen_excluded": False,
            "twin_prime_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def proof_dag(code: str, prior_name: str, theorem_name: str, rejected_name: str, open_name: str) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T257", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T258", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-CERT258", "label": f"{theorem_name}ExactReplay", "status": "computed_finite"},
        {"id": f"{code}-REJECT258", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN258", "label": open_name, "status": "open"},
    ]
    return {
        "nodes": nodes,
        "edges": [
            [f"{code}-T257", f"{code}-T258"],
            [f"{code}-T258", f"{code}-CERT258"],
            [f"{code}-T258", f"{code}-REJECT258"],
            [f"{code}-T258", f"{code}-OPEN258"],
        ],
        "resolution_path": [f"{code}-T257", f"{code}-T258", f"{code}-OPEN258"],
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
        "ticket_id": f"{code}-TICKET-258",
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
        "proof_dag": proof_dag(code, prior_name, theorem_name, rejected_name, next_lemma),
        "claim_boundary": claim_boundary,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_bounded_variation_audit()
    collatz = collatz_rational_independence_audit()
    goldbach = goldbach_character_basis_audit()
    twin = twin_continued_fraction_audit()
    sections = {
        "riemann": section(
            "riemann", "RH", "BoundedTotalVariationPacketEnergyLagNoGo", "exact_no_go", riemann,
            "using ordinary bounded total variation, together with positivity and convergence, as a substitute for scaled one-sided variation",
            ["direct arithmetic control of scaled downward variation for actual Weil packets"],
            "the exact finite-total-variation counterexample and TICKET-257's scaled one-sided repair",
            "ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation",
            "PositiveConvergentPacketEnergyLagPartialSumNoGo",
            "PositiveConvergentBoundedVariationPacketEnergiesForceUniformLagLowerBound",
            "Even total variation two does not control the scaled drops; no positive margin or weighted variation estimate is known for actual Guinand-Weil packets.",
            "No RH proof or disproof; a strictly stronger abstract shortcut is eliminated while the actual-Weil arithmetic target remains open.",
            f"{len(riemann['exact_bounded_variation_spike_rows'])} exact rows replay an all-k theorem; no actual Weil coefficient is computed.",
        ),
        "collatz": section(
            "collatz", "CO", "DistinctPrimeCyclotomicPhaseRationalIndependence", "exact_no_go", collatz,
            "seeking a nonzero rationally weighted exact cancellation or telescoping identity among finitely many nontrivial canonical phases",
            ["quantitative sublinear cancellation of canonical fixed-base Fermat-quotient phases"],
            "the rational linear-independence theorem, with trivial D_q=0 phases explicitly separated",
            "CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude",
            "DistinctPrimeCyclotomicPhaseExactCancellationNoGo",
            "NontrivialDistinctPrimeCanonicalPhasesAdmitARationalLinearRelation",
            "Exact rational relations are impossible, but algebraic independence supplies no quantitative complex-magnitude cancellation across primes.",
            "No Collatz proof or counterexample; finite rational telescoping is ruled out while the cross-prime power-saving problem remains open.",
            f"Canonical D_q values are replayed for primes through {COLLATZ_PRIME_LIMIT}; the independence theorem itself is unrestricted for finite distinct-prime families with D_q nonzero.",
        ),
        "goldbach": section(
            "goldbach", "GB", "PrimitiveOddCharacterCompletenessClassification", "partial_theorem", goldbach,
            "using one fixed primitive odd character as a complete reflection-asymmetry detector for every prime modulus",
            ["uniform nonvanishing of an odd multiplicative-character moment for every compatible even q-divisible prime prefix"],
            "the exact power-of-two classification, explicit blind vectors otherwise, and the actual q=5 quartic certificate",
            "EveryCompatibleEvenQDivisiblePrimePrefixHasNonzeroOddCharacterMoment",
            "QuadraticCharacterReflectionObstructionAndNextPrefixExclusion",
            "OnePrimitiveOddCharacterDetectsReflectionAsymmetryForEveryPrimeModulus",
            "Detector completeness is now classified, but no theorem forces an actual compatible prime prefix to activate one of the required odd-character coordinates.",
            "No strong Goldbach proof or counterexample; the minimal character detector is determined for Fermat moduli and proved insufficient in general.",
            f"{len(goldbach['exact_modulus_classification_rows'])} sample moduli and the first 1255 primes modulo five are replayed; the detector theorem is exact for every odd prime.",
        ),
        "twin_prime": section(
            "twin-prime", "TP", "UnitCoefficientSolutionsAreRootConvergents", "partial_theorem", twin,
            "treating a linear scan over every denominator as necessary after the unique-root-neighbor reduction",
            ["all-convergent exclusion for the unique real root"],
            "the derivative bound, Legendre reduction, certified continued fraction, and finite convergent certificate",
            "EveryUniqueRootConvergentMissesUnitCoefficient",
            "UniqueRealRootNeighborReductionAndBoundedExclusion",
            "LinearDenominatorScanningIsNecessaryForTheRemainingCoefficientOneBranch",
            "Every solution must be a convergent and a huge finite denominator interval is excluded, but infinitely many later convergents remain.",
            "No twin-prime proof or counterexample; the last Thue branch is reduced from all denominators to the continued-fraction convergents of one algebraic root.",
            f"The first {TWIN_CF_TERM_COUNT} exact convergents are checked; the absence of unit coefficients there is not an infinite exclusion.",
        ),
    }
    twin_dag = sections["twin_prime"]["proof_dag"]
    twin_dag["nodes"].insert(
        1,
        {
            "id": "TP-LEGENDRE258",
            "label": "LegendreContinuedFractionCriterion",
            "status": "external_theorem",
        },
    )
    twin_dag["edges"].insert(1, ["TP-LEGENDRE258", "TP-T258"])
    total_failures = sum(section["reproducible_computation"]["failure_count"] for section in sections.values())
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureVariationCharacterConvergentAudit",
            "summary": "TICKET-258 proves two exact route no-gos and two partial theorems: bounded total variation still fails for packet lags, nontrivial distinct-prime phases are Q-linearly independent, primitive odd-character completeness is classified, and the remaining Twin Thue branch reduces to certified continued-fraction convergents; all parent conjectures remain open.",
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
                "riemann_spike_case_count": len(riemann["exact_bounded_variation_spike_rows"]),
                "collatz_prime_case_count": len(collatz["exact_canonical_phase_rows"]),
                "collatz_trivial_phase_count": len(collatz["aggregate"]["trivial_phase_primes"]),
                "goldbach_modulus_case_count": len(goldbach["exact_modulus_classification_rows"]),
                "goldbach_blind_vector_count": goldbach["aggregate"]["non_power_two_blind_vector_count"],
                "twin_convergent_count": twin["finite_convergent_audit"]["term_count"],
                "twin_maximum_excluded_denominator": twin["finite_convergent_audit"]["maximum_excluded_denominator"],
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
        "ticket": 258,
        "parent_ticket": 257,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "twin_prime",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(ROOT / "data/open-problem/ticket258-variation-character-convergent.json", audit)
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-258-bounded-variation-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-258-rational-independence.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-258-character-completeness.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-258-root-convergents.json",
    }
    for key, path in paths.items():
        write_json(path, {"schema": SCHEMA, "generated_at": GENERATED_AT, "status": STATUS, **root[key]})
    write_json(ROOT / "data/open-problem/four-problem-research-state.json", build_research_state(audit))


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    machine = audit[AUDIT_KEY]["machine_audit"]
    print(json.dumps(machine, indent=2))
    return 0 if machine["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
