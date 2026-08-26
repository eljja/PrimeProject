from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket244_joint_tightness_harmonic_parity_fold_polylog_mimicry import (
    ROOT,
    fraction_payload,
    primes_up_to,
    write_json,
)
from scripts.ticket246_moment_alldepth_parseval_primepower import (
    euler_phi,
    fixed_base_polynomial,
    prime_power_representation_table,
)


SCHEMA = "primeproject.ticket247-hilbert-hensel-lipschitz-primepower.v1"
GENERATED_AT = "2026-08-26T18:10:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "hilbert_hensel_lipschitz_primepower_audit"
LEGENDRE_ORDERS = (1, 2, 3, 4, 5, 6, 8, 10, 12, 16)
COLLATZ_PRIME_LIMIT = 10_000
COLLATZ_LIFT_DEPTH = 8
GOLDBACH_X_SCALES = (10_000, 100_000, 500_000)
GOLDBACH_Q_LIMIT = 64
TWIN_X_SCALES = (100, 1_000, 10_000, 100_000, 1_000_000, 5_000_000, 10_000_000)


def polynomial_subtract(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    size = max(len(left), len(right))
    result = [Fraction(0) for _ in range(size)]
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] -= value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def legendre_coefficients(degree: int) -> list[Fraction]:
    if degree == 0:
        return [Fraction(1)]
    previous = [Fraction(1)]
    current = [Fraction(0), Fraction(1)]
    for n in range(1, degree):
        shifted = [Fraction(0)] + [Fraction(2 * n + 1) * value for value in current]
        padded_previous = [Fraction(n) * value for value in previous]
        numerator = polynomial_subtract(shifted, padded_previous)
        following = [value / Fraction(n + 1) for value in numerator]
        previous, current = current, following
    return current


def legendre_rodrigues_coefficients(degree: int) -> list[Fraction]:
    coefficients = [Fraction(0) for _ in range(degree + 1)]
    for j in range(degree // 2 + 1):
        exponent = degree - 2 * j
        coefficients[exponent] = Fraction(
            (-1) ** j * math.factorial(2 * degree - 2 * j),
            2**degree
            * math.factorial(j)
            * math.factorial(degree - j)
            * math.factorial(degree - 2 * j),
        )
    return coefficients


def polynomial_integral_moment(coefficients: list[Fraction], power: int) -> Fraction:
    total = Fraction(0)
    for exponent, coefficient in enumerate(coefficients):
        combined = exponent + power
        if combined % 2 == 0:
            total += coefficient * Fraction(2, combined + 1)
    return total


def polynomial_l2_norm_squared(coefficients: list[Fraction]) -> Fraction:
    product = [Fraction(0) for _ in range(2 * len(coefficients) - 1)]
    for left_index, left in enumerate(coefficients):
        for right_index, right in enumerate(coefficients):
            product[left_index + right_index] += left * right
    return polynomial_integral_moment(product, 0)


@lru_cache(maxsize=1)
def riemann_hilbert_schmidt_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for n in LEGENDRE_ORDERS:
        degree = 2 * n
        coefficients = legendre_coefficients(degree)
        independent_coefficients = legendre_rodrigues_coefficients(degree)
        moments = [
            polynomial_integral_moment(coefficients, 2 * k) for k in range(n)
        ]
        norm_squared = polynomial_l2_norm_squared(coefficients)
        expected_norm_squared = Fraction(2, 4 * n + 1)
        dyadic_tail_upper_bound = Fraction(2 ** max(0, 2 - n), 4 * n + 1)
        if n > 2:
            dyadic_tail_upper_bound = Fraction(1, 2 ** (n - 2) * (4 * n + 1))
        verified = (
            coefficients == independent_coefficients
            and all(moment == 0 for moment in moments)
            and norm_squared == expected_norm_squared
            and coefficients[degree] != 0
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{n}:{','.join(map(str, coefficients))}:{norm_squared}:"
                f"{','.join(map(str, moments))}:{dyadic_tail_upper_bound}:{int(verified)}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "legendre_half_degree_n": n,
                "polynomial_degree": degree,
                "coefficients_low_to_high": [str(value) for value in coefficients],
                "annihilated_even_moment_orders": list(range(n)),
                "all_exact_moments_zero": all(moment == 0 for moment in moments),
                "unnormalized_L2_norm_squared": fraction_payload(norm_squared),
                "dyadic_weight_feature_tail_upper_bound": fraction_payload(
                    dyadic_tail_upper_bound
                ),
                "recurrence_matches_rodrigues": coefficients == independent_coefficients,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let H=L2_even([-1,1]) and let w_k>=0 satisfy "
        "sum_(k>=0) 2w_k/(4k+1)<infinity. Define "
        "Q_w(f)=sum_(k>=0) w_k |integral_(-1)^1 x^(2k)f(x)dx|^2. "
        "For every n>=1, the normalized even Legendre polynomial "
        "f_n=sqrt((4n+1)/2) P_(2n) has norm one, its moments of orders "
        "0,2,...,2n-2 vanish, and Q_w(f_n)<=sum_(k>=n)2w_k/(4k+1). "
        "Consequently inf_{||f||_2=1,f in H} Q_w(f)=0. Equivalently, the "
        "weighted moment feature operator is Hilbert-Schmidt and cannot be "
        "bounded below on the infinite-dimensional unit sphere."
    )
    proof = (
        "Legendre orthogonality makes P_(2n) orthogonal to every polynomial "
        "of degree below 2n, hence to x^(2k) for k<n, and its exact squared "
        "norm is 2/(4n+1). For k>=n, Cauchy-Schwarz gives the normalized "
        "bound |integral x^(2k)f_n|^2<=integral x^(4k)dx=2/(4k+1). "
        "Summing with w_k proves the tail bound, whose right side tends to "
        "zero by convergence. The same summability is exactly the sum of "
        "the squared norms of the weighted coordinate functionals, so the "
        "feature map is Hilbert-Schmidt and compact. A positive uniform lower "
        "bound would contradict the displayed unit sequence."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_legendre_certificates": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "hilbert_schmidt_weighted_moment_coercivity_refuted": True,
            "explicit_normalized_weak_sequence_proved": True,
            "dyadic_weight_tail_tends_to_zero_proved": True,
            "non_hilbert_schmidt_arithmetic_weil_coercivity_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "This is an all-Hilbert-space no-go for weighted monomial feature maps "
            "whose coordinate norm squares are summable. It does not show that the "
            "Legendre sequence belongs to the genuine normalized Guinand-Weil "
            "admissible closure, and it does not cover a non-Hilbert-Schmidt or "
            "arithmetic feature operator. It therefore proves no RH implication."
        ),
        "failure_count": failures,
    }


def fixed_base_polynomial_derivative_v(v: int, q: int) -> int:
    return -3 - 6 * q * v - 3 * q * q * v * v


def hensel_countermodel(prime: int, depth: int) -> tuple[int, list[int], bool]:
    u = 3
    v = 5
    digits = [v % prime]
    verified = fixed_base_polynomial(u, v, prime) % prime == 0
    for current_depth in range(1, depth):
        modulus = prime**current_depth
        value = fixed_base_polynomial(u, v, prime)
        derivative = fixed_base_polynomial_derivative_v(v, prime)
        verified = verified and value % modulus == 0 and math.gcd(derivative, prime) == 1
        quotient_digit = (value // modulus) % prime
        lift_digit = (-quotient_digit * pow(derivative, -1, prime)) % prime
        candidate = v + lift_digit * modulus
        verified = verified and (
            fixed_base_polynomial(u, candidate, prime) % (modulus * prime) == 0
        )
        v = candidate
        digits.append(lift_digit)
    verified = verified and (
        fixed_base_polynomial(u, v, prime) % prime**depth == 0
        and (u - v) % prime != 0
        and v % prime == 5
    )
    return v, digits, verified


@lru_cache(maxsize=1)
def collatz_hensel_no_go_audit() -> dict[str, Any]:
    primes = [q for q in primes_up_to(COLLATZ_PRIME_LIMIT) if q > 5]
    selected = {7, 11, 23, 101, 1009, primes[-1]}
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for q in primes:
        v, digits, verified = hensel_countermodel(q, COLLATZ_LIFT_DEPTH)
        polynomial = fixed_base_polynomial(3, v, q)
        failures += int(not verified)
        transcript.update(
            (
                f"{q}:{v}:{','.join(map(str, digits))}:{polynomial % q**COLLATZ_LIFT_DEPTH}:"
                f"{(3-v)%q}:{int(verified)}\n"
            ).encode("ascii")
        )
        if q in selected:
            rows.append(
                {
                    "prime_q": q,
                    "fixed_U": 3,
                    "lifted_V_mod_q_to_depth": v,
                    "base_q_digits_low_to_high": digits,
                    "lift_depth": COLLATZ_LIFT_DEPTH,
                    "P_q_mod_q_to_depth": polynomial % q**COLLATZ_LIFT_DEPTH,
                    "U_minus_V_mod_q": (3 - v) % q,
                    "P_q_valuation_lower_bound": COLLATZ_LIFT_DEPTH,
                    "U_minus_V_valuation": 0,
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "For every prime q>5 and every integer r>=1 there is an integer V_r, "
        "unique modulo q^r subject to V_r=5 modulo q, such that with U=3, "
        "P_q(U,V_r)=0 modulo q^r while U-V_r is nonzero modulo q. Therefore "
        "v_q(P_q(U,V_r))>=r>0=v_q(U-V_r). The unrestricted formal assertion "
        "v_q(P_q(U,V))<=v_q(U-V) for all q-adic quotient pairs is false at "
        "every prime q>5 and arbitrary depth."
    )
    proof = (
        "Modulo q the polynomial is P_q(3,V)=15-3V, so V=5 is a root. "
        "Its V-derivative is -3-6qV-3q^2V^2=-3(1+qV)^2, a unit modulo every "
        "prime q>5. Hensel lifting gives one and only one compatible root "
        "modulo q^r for every r. Along that branch 3-V=-2 modulo q, hence it "
        "is a unit. The valuation inequality is therefore violated by exact "
        "integer representatives at each requested finite depth."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "selected_hensel_countermodels": rows,
        "exact_modular_replay": {
            "prime_limit": COLLATZ_PRIME_LIMIT,
            "primes_checked": len(primes),
            "lift_depth": COLLATZ_LIFT_DEPTH,
            "all_lifts_verified": failures == 0,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "formal_unrestricted_valuation_domination_refuted": True,
            "all_prime_all_depth_hensel_branch_proved": True,
            "actual_fermat_quotients_excluded_from_hensel_branch": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The countermodels are unrestricted q-adic pairs with U fixed to 3. "
            "They are not the actual Fermat quotients U=(2^(q-1)-1)/q and "
            "V=(3^(q-1)-1)/q. Thus the theorem blocks a deduction from the "
            "polynomial identity alone, but it neither refutes an arithmetic "
            "inequality on actual quotient pairs nor decides any Collatz orbit."
        ),
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def goldbach_arc_lipschitz_audit() -> dict[str, Any]:
    primes = [p for p in primes_up_to(max(GOLDBACH_X_SCALES)) if p >= 3]
    selected_q = {3, 4, 5, 8, 12, 16, 30, 60, 64}
    rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for x_limit in GOLDBACH_X_SCALES:
        scale_primes = [p for p in primes if p <= x_limit]
        scale_failures = 0
        maximum_budget = (Fraction(0), 0)
        for q in range(3, GOLDBACH_Q_LIMIT + 1):
            units = [r for r in range(q) if math.gcd(r, q) == 1]
            counts = {r: 0 for r in units}
            first_moment = 0
            for p in scale_primes:
                if math.gcd(p, q) == 1:
                    counts[p % q] += 1
                    first_moment += p
            prime_mass = sum(counts.values())
            phi = euler_phi(q)
            sum_squares = sum(count * count for count in counts.values())
            variance_numerator = phi * sum_squares - prime_mass * prime_mass
            arc_width = Fraction(1, x_limit * x_limit)
            lipschitz_budget_without_2pi = arc_width * first_moment
            verified = (
                phi == len(units)
                and prime_mass > 0
                and variance_numerator >= 0
                and first_moment <= x_limit * prime_mass
                and sum(counts.values()) == prime_mass
            )
            failures += int(not verified)
            scale_failures += int(not verified)
            if lipschitz_budget_without_2pi > maximum_budget[0]:
                maximum_budget = (lipschitz_budget_without_2pi, q)
            transcript.update(
                (
                    f"{x_limit}:{q}:{phi}:{prime_mass}:{first_moment}:"
                    f"{variance_numerator}:{arc_width}:{lipschitz_budget_without_2pi}:"
                    f"{int(verified)}\n"
                ).encode("ascii")
            )
            if q in selected_q:
                rows.append(
                    {
                        "prime_limit_X": x_limit,
                        "denominator_q": q,
                        "phi_q": phi,
                        "unit_prime_mass": prime_mass,
                        "unit_prime_first_moment_M": first_moment,
                        "residual_pointwise_squared_bound_phi_D": variance_numerator,
                        "arc_width_abs_beta": fraction_payload(arc_width),
                        "lipschitz_budget_M_abs_beta_without_2pi": fraction_payload(
                            lipschitz_budget_without_2pi
                        ),
                        "certificate_verified": verified,
                    }
                )
        summaries.append(
            {
                "prime_limit_X": x_limit,
                "denominators_checked": GOLDBACH_Q_LIMIT - 2,
                "maximum_M_abs_beta_without_2pi": fraction_payload(maximum_budget[0]),
                "maximum_budget_denominator_q": maximum_budget[1],
                "failure_count": scale_failures,
            }
        )

    center_only_counterfamily = []
    for frequency in (10, 100, 1_000, 10_000):
        beta = Fraction(1, 2 * frequency)
        row = {
            "frequency_N": frequency,
            "center_value_abs_F_N_0": 0,
            "test_beta": fraction_payload(beta),
            "exact_abs_F_N_beta": 2,
            "certificate_verified": 2 * frequency * beta == 1,
        }
        transcript.update(
            f"counter:{frequency}:{beta}:0:2:{int(row['certificate_verified'])}\n".encode(
                "ascii"
            )
        )
        failures += int(not row["certificate_verified"])
        center_only_counterfamily.append(row)

    theorem = (
        "Let q>=3, X>=3, and let S*(alpha) sum exp(2 pi i alpha p) over "
        "odd primes p<=X coprime to q. For reduced residues r let n_r be the "
        "counts, P=sum n_r, delta_r=n_r-P/phi(q), D=sum delta_r^2, and "
        "M=sum p over the same primes. For every integer a and real beta, "
        "|S*(a/q+beta)-(P/phi(q))c_q(a)| <= sqrt(phi(q)D)+2 pi |beta|M, "
        "where phi(q)D=phi(q)sum n_r^2-P^2 is an exact nonnegative integer. "
        "No modulus of continuity uniform in the maximum frequency can follow "
        "from center values alone: F_N(beta)=exp(2 pi i N beta)-1 has F_N(0)=0 "
        "but |F_N(1/(2N))|=2 as 1/(2N) tends to zero."
    )
    proof = (
        "TICKET-246 gives the center decomposition and Cauchy-Schwarz bound "
        "|R(a)|<=sqrt(phi D). Subtract the center sum term by term and use "
        "|exp(it)-1|<=|t| to obtain at most 2 pi |beta| sum p. The variance "
        "identity follows by expanding delta_r. For the no-go family, the "
        "center is exactly zero while exp(2 pi i N/(2N))=-1, so the displaced "
        "value is exactly -2."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_selected_arc_rows": rows,
        "exhaustive_denominator_summaries": summaries,
        "center_only_uniformity_counterfamily": center_only_counterfamily,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "rational_center_arc_lipschitz_bridge_proved": True,
            "center_only_uniform_modulus_refuted": True,
            "uniform_signed_first_moment_saving_proved": False,
            "uniform_growing_denominator_variance_decay_proved": False,
            "strong_goldbach_resolved": False,
        },
        "no_go_scope": (
            "The Lipschitz term is deterministic but may be as large as the "
            "trivial prime first moment; it is not signed cancellation. The "
            "counterfamily blocks center-only promotion for unrestricted "
            "trigonometric polynomials, not a sharper theorem using prime "
            "arithmetic. The finite residue tables prove no asymptotic in X or q "
            "and no positive Goldbach representation bound."
        ),
        "failure_count": failures,
    }


def integer_nth_root(value: int, degree: int) -> int:
    low = 0
    high = 1
    while high**degree <= value:
        high *= 2
    while low + 1 < high:
        middle = (low + high) // 2
        if middle**degree <= value:
            low = middle
        else:
            high = middle
    return low


def odd_composite_prime_power_count_by_base(limit: int, primes: list[int]) -> int:
    count = 0
    for prime in primes:
        if prime == 2:
            continue
        if prime * prime > limit:
            break
        power = prime * prime
        while power <= limit:
            count += 1
            if power > limit // prime:
                break
            power *= prime
    return count


@lru_cache(maxsize=1)
def twin_sharp_prime_power_audit() -> dict[str, Any]:
    upper = max(TWIN_X_SCALES) + 2
    primes = primes_up_to(upper)
    prime_flags = bytearray(upper + 1)
    for prime in primes:
        prime_flags[prime] = 1
    power_flags, _ = prime_power_representation_table(upper, primes)
    scale_set = set(TWIN_X_SCALES)
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    pair_count = 0
    twin_count = 0
    failures = 0

    for n in range(3, max(TWIN_X_SCALES) + 1, 2):
        if power_flags[n] and power_flags[n + 2]:
            pair_count += 1
            if prime_flags[n] and prime_flags[n + 2]:
                twin_count += 1
        if n + 1 in scale_set:
            x_limit = n + 1
            y = x_limit + 2
            exponent_cap = y.bit_length() - 1
            exact_odd_composite_powers = odd_composite_prime_power_count_by_base(
                y, primes
            )
            enumerated_odd_composite_powers = sum(
                1
                for value in range(3, y + 1, 2)
                if power_flags[value] and not prime_flags[value]
            )
            square_root = math.isqrt(y)
            cube_root = integer_nth_root(y, 3)
            odd_prime_square_bases = sum(
                1 for prime in primes if prime != 2 and prime <= square_root
            )
            odd_prime_cube_bases = sum(
                1 for prime in primes if prime != 2 and prime <= cube_root
            )
            sharp_power_count_bound = odd_prime_square_bases + max(
                0, exponent_cap - 2
            ) * odd_prime_cube_bases
            sharp_pair_bound = 2 * sharp_power_count_bound
            prior_pair_bound = 2 * max(0, exponent_cap - 1) * square_root
            contamination = pair_count - twin_count
            verified = (
                contamination >= 0
                and exact_odd_composite_powers == enumerated_odd_composite_powers
                and contamination <= 2 * exact_odd_composite_powers
                and exact_odd_composite_powers <= sharp_power_count_bound
                and sharp_pair_bound <= prior_pair_bound
            )
            failures += int(not verified)
            transcript.update(
                (
                    f"{x_limit}:{pair_count}:{twin_count}:{contamination}:"
                    f"{exact_odd_composite_powers}:{odd_prime_square_bases}:"
                    f"{odd_prime_cube_bases}:{exponent_cap}:{sharp_pair_bound}:"
                    f"{prior_pair_bound}:{int(verified)}\n"
                ).encode("ascii")
            )
            rows.append(
                {
                    "limit_X": x_limit,
                    "prime_power_pair_count_A2": pair_count,
                    "twin_prime_pair_count_pi2": twin_count,
                    "composite_prime_power_contamination": contamination,
                    "exact_odd_composite_prime_powers_N": exact_odd_composite_powers,
                    "odd_prime_bases_through_sqrt_Y": odd_prime_square_bases,
                    "odd_prime_bases_through_cuberoot_Y": odd_prime_cube_bases,
                    "exponent_cap_K": exponent_cap,
                    "sharp_contamination_bound": sharp_pair_bound,
                    "ticket246_exponent_blind_bound": prior_pair_bound,
                    "strictly_improves_ticket246_bound": sharp_pair_bound
                    < prior_pair_bound,
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "Let A_2(X) and pi_2(X) be the odd prime-power-pair and twin-prime "
        "counts of TICKET-246, put Y=X+2, K=floor(log_2 Y), and let pi_odd(t) "
        "count odd primes at most t. If N_odd(Y) counts odd composite prime "
        "powers at most Y, then exactly N_odd(Y)=sum_(k=2)^K "
        "pi_odd(floor(Y^(1/k))). Consequently 0<=A_2(X)-pi_2(X)<=2N_odd(Y) "
        "<=2pi_odd(floor(sqrt(Y)))+2(K-2)pi_odd(floor(cuberoot(Y))). This "
        "strictly sharpens the exponent-blind TICKET-246 correction at every "
        "audited scale."
    )
    proof = (
        "Every odd composite prime power has a unique representation p^k with "
        "odd prime p and k>=2, so counting by exponent gives the exact sum. "
        "As before, every false pair contains such a power in one of two "
        "coordinates, giving the factor-two union bound. The k=2 contribution "
        "is exactly pi_odd(floor sqrt(Y)); every one of the K-2 remaining "
        "contributions is at most the k=3 count, proving the sharper bound."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_sharp_contamination_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "exact_odd_composite_prime_power_formula_proved": True,
            "sharp_contamination_bound_proved": True,
            "strict_improvement_on_all_audited_scales": all(
                row["strictly_improves_ticket246_bound"] for row in rows
            ),
            "scale_local_type_ii_lower_bound_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The exact correction is smaller than the previous crude correction, "
            "but there is still no lower bound for A_2 exceeding it on unbounded "
            "scales. The finite sieve through ten million supplies no Type-II "
            "cancellation and no infinitude conclusion."
        ),
        "failure_count": failures,
    }


def proof_dag(
    code: str,
    prior_name: str,
    theorem_name: str,
    rejected_name: str,
    open_name: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{code}-T246", "label": prior_name, "status": "proved"},
            {"id": f"{code}-T247", "label": theorem_name, "status": "proved"},
            {"id": f"{code}-REJECT247", "label": rejected_name, "status": "disproved"},
            {"id": f"{code}-OPEN247", "label": open_name, "status": "open"},
        ],
        "edges": [
            [f"{code}-T246", f"{code}-T247"],
            [f"{code}-T247", f"{code}-REJECT247"],
            [f"{code}-T247", f"{code}-OPEN247"],
        ],
        "resolution_path": [f"{code}-T246", f"{code}-T247", f"{code}-OPEN247"],
        "acyclic": True,
    }


def section(
    problem_id: str,
    code: str,
    theorem_name: str,
    result_classification: str,
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
        "ticket_id": f"{code}-TICKET-247",
        "theorem_name": theorem_name,
        "declared_proposition": computation["theorem"],
        "mathematical_argument": computation["proof"],
        "result_classification": result_classification,
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
    riemann = riemann_hilbert_schmidt_audit()
    collatz = collatz_hensel_no_go_audit()
    goldbach = goldbach_arc_lipschitz_audit()
    twin = twin_sharp_prime_power_audit()
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "HilbertSchmidtInfiniteMomentCoercivityNoGo",
            "exact_no_go",
            riemann,
            "uniform positive coercivity from any Hilbert-Schmidt weighted even-moment feature map on the full normalized even L2 sphere",
            [],
            "non-Hilbert-Schmidt arithmetic Weil features on the genuine normalized admissible closure",
            "NonHilbertSchmidtArithmeticWeilCoercivityOnAdmissibleClosure",
            "FiniteEvenMomentAnnihilatorNoGo",
            "HilbertSchmidtInfiniteMomentsCoerceTheEvenL2UnitSphere",
            "The theorem closes the summable weighted-moment upgrade, but no bridge identifies the genuine admissible Weil closure with the full even L2 sphere or proves coercivity for a noncompact arithmetic feature operator.",
            "No RH proof or disproof; one exact infinite-feature no-go under the Hilbert-Schmidt summability condition.",
            f"{len(LEGENDRE_ORDERS)} exact Legendre rows through half-degree {max(LEGENDRE_ORDERS)} verify the construction; the all-n and all-summable-weight theorem is proved analytically, not inferred from those rows.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "FormalHenselBranchNoGoForValuationDomination",
            "exact_no_go",
            collatz,
            "deducing v_q(P_q)<=v_q(U_q-V_q) for actual Fermat quotients from the unrestricted q-adic polynomial identity alone",
            [],
            "an arithmetic exclusion showing that actual fixed-base Fermat quotients cannot approach the bad Hensel branch",
            "ArithmeticFermatQuotientExclusionOfPqHenselBranch",
            "AllDepthFixedBaseFermatPolynomialIdentity",
            "UnrestrictedQAdicPolynomialValuationDomination",
            "Hensel countermodels destroy the formal-algebra route, but they do not occur at the actual quotient pair unless an additional arithmetic theorem places it there; no global trajectory implication is known.",
            "No Collatz proof, divergent orbit, or nontrivial cycle; one exact no-go for the unrestricted q-adic valuation-transfer route.",
            f"Depth {COLLATZ_LIFT_DEPTH} is replayed for all primes q>5 through {COLLATZ_PRIME_LIMIT:,}; Hensel's derivative-unit proof supplies every prime and arbitrary depth, while the finite table says nothing about actual Fermat quotient pairs.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "RationalCenterArcLipschitzBridgeAndCenterOnlyNoGo",
            "partial_theorem",
            goldbach,
            "promoting rational-center control to a uniform arc-neighborhood bound without a frequency-scale or signed first-moment term",
            [],
            "the exact center Parseval bound plus uniform signed residue and prime-first-moment savings on quarter-torus arcs",
            "UniformSignedResidueVarianceAndFirstMomentSavingOnQuarterTorus",
            "RationalCenterResidueParsevalBridge",
            "CenterValuesAloneGiveUniformArcModulus",
            "The deterministic 2 pi |beta|M term can be trivial-sized, and no growing-denominator residue-variance decay or signed first-moment cancellation has been proved.",
            "No strong Goldbach proof or counterexample; one exact center-to-arc inequality and one exact center-only uniformity obstruction.",
            f"Exact integer/rational rows cover q=3..{GOLDBACH_Q_LIMIT} at X={','.join(map(str, GOLDBACH_X_SCALES))}; beta=1/X^2 is illustrative only and proves no asymptotic major/minor-arc saving.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "SharpOddPrimePowerContaminationBound",
            "partial_theorem",
            twin,
            "using the exponent-blind TICKET-246 O(sqrt(X) log(X)) correction as the final prime-power contamination scale",
            [],
            "a scale-local nonperiodic Type-II lower bound for A_2 exceeding the exact odd composite-prime-power correction",
            "ScaleLocalTypeIILowerBoundBeyondSharpPrimePowerContamination",
            "PrimePowerPairProxyContaminationBound",
            "ExponentBlindPrimePowerCorrectionIsSharp",
            "The correction is now counted exactly and bounded more sharply, but no unbounded scale sequence has A_2 beyond that correction and no parity-breaking Type-II estimate is proved.",
            "No twin-prime proof or counterexample; one exact contamination count formula and sharper sufficient target.",
            f"Prime-power and twin supports are enumerated through {max(TWIN_X_SCALES):,}; the exact all-X count identity is combinatorial, but the finite rows imply no twin-prime infinitude.",
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
            "theorem_name": "FourConjectureHilbertHenselLipschitzPrimePowerAudit",
            "summary": "TICKET-247 proves two exact route no-go theorems and two partial theorems while leaving all four parent conjectures open.",
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
                "collatz": "https://arxiv.org/abs/1909.03562",
                "goldbach_major_arcs": "https://arxiv.org/abs/1205.5252",
                "twin_prime_parity": "https://arxiv.org/abs/1407.4897",
            },
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 2,
                "exact_no_go_count": 2,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "riemann",
                "stagnated_problem_count": 0,
                "riemann_legendre_certificate_count": len(
                    riemann["exact_legendre_certificates"]
                ),
                "collatz_hensel_prime_count": collatz["exact_modular_replay"][
                    "primes_checked"
                ],
                "goldbach_arc_row_count": len(goldbach["exact_selected_arc_rows"]),
                "twin_scale_count": len(twin["exact_sharp_contamination_rows"]),
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
    previous = (
        json.loads(state_path.read_text(encoding="utf-8"))
        if state_path.exists()
        else {"problems": {}}
    )
    root = audit[AUDIT_KEY]
    problems: dict[str, Any] = {}
    for key in ("riemann", "collatz", "goldbach", "twin_prime"):
        item = root[key]
        old = previous.get("problems", {}).get(key, {})
        established = list(old.get("established_results", []))
        if item["theorem_name"] not in established:
            established.append(item["theorem_name"])
        retired = list(old.get("retired_routes", []))
        discarded = item["route_decision"]["discard"]
        if discarded and discarded not in retired:
            retired.append(discarded)
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
        "ticket": 247,
        "parent_ticket": 246,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "riemann",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(
        ROOT / "data/open-problem/ticket247-hilbert-hensel-lipschitz-primepower.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-247-hilbert-schmidt-moment-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-247-hensel-polynomial-countermodels.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-247-rational-arc-lipschitz.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-247-sharp-prime-power-contamination.json",
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
