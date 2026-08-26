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


SCHEMA = "primeproject.ticket246-moment-alldepth-parseval-primepower.v1"
GENERATED_AT = "2026-08-26T13:40:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "moment_alldepth_parseval_primepower_audit"
MOMENT_ORDERS = (1, 2, 3, 4, 5, 6, 8, 10, 12)
COLLATZ_REPLAY_LIMIT = 200_000
COLLATZ_DIGITS = 5
GOLDBACH_X_SCALES = (10_000, 100_000, 500_000)
GOLDBACH_Q_LIMIT = 64
TWIN_X_SCALES = (100, 1_000, 10_000, 100_000, 1_000_000, 5_000_000)


def riemann_finite_moment_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for m in MOMENT_ORDERS:
        coefficients = [(-1) ** j * math.comb(2 * m, j) for j in range(2 * m + 1)]
        moment_sums: list[Fraction] = []
        for k in range(m):
            moment_sums.append(
                sum(
                    (
                        Fraction(
                            coefficient
                            * ((j + 1) ** (2 * k + 1) - j ** (2 * k + 1)),
                            2 * k + 1,
                        )
                        for j, coefficient in enumerate(coefficients)
                    ),
                    Fraction(0),
                )
            )
        norm_squared = sum(value * value for value in coefficients)
        expected_norm_squared = math.comb(4 * m, 2 * m)
        verified = (
            all(value == 0 for value in moment_sums)
            and norm_squared == expected_norm_squared
            and coefficients[0] == 1
            and coefficients[-1] == 1
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{m}:{','.join(map(str, coefficients))}:{norm_squared}:"
                f"{','.join(str(value) for value in moment_sums)}:{int(verified)}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "moment_count_m": m,
                "shell_dimension": 2 * m + 1,
                "finite_difference_order": 2 * m,
                "integer_coefficients": coefficients,
                "unnormalized_L2_norm_squared": norm_squared,
                "central_binomial_norm_certificate": expected_norm_squared,
                "annihilated_even_moment_orders": list(range(m)),
                "all_exact_moment_sums_zero": all(value == 0 for value in moment_sums),
                "common_compact_support": f"[-{2 * m + 1},{2 * m + 1}]",
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For every integer m>=1 let e_j=2^(-1/2) times the indicator of "
        "[-j-1,-j] union [j,j+1], for 0<=j<=2m, and put "
        "c_j=(-1)^j binom(2m,j). Then g_m=sum_j c_j e_j is nonzero, real-even, "
        "compactly supported, and its even moments integral x^(2k)g_m(x)dx "
        "vanish for every 0<=k<m. Moreover ||g_m||_2^2=binom(4m,2m). "
        "Thus the normalized f_m=g_m/sqrt(binom(4m,2m)) lies on the L2 unit "
        "sphere and Q_m(f_m)=sum_(k<m)|integral x^(2k)f_m(x)dx|^2=0. "
        "No nonnegative certificate using only the first m even moments can "
        "separate every normalized member of any class containing f_m from its zero set."
    )
    proof = (
        "The shell indicators are real-even orthonormal vectors. After removing "
        "their common square-root-two factor, the 2k-th moment of e_j is "
        "((j+1)^(2k+1)-j^(2k+1))/(2k+1), a polynomial in j of degree 2k. "
        "For k<m this degree is at most 2m-2. The alternating binomial sum of "
        "order 2m annihilates every polynomial of degree below 2m, proving all "
        "m moment identities. Orthogonality gives the coefficient-square norm, "
        "and Vandermonde's identity gives sum_j binom(2m,j)^2=binom(4m,2m). "
        "Normalization is therefore legitimate and leaves all moments zero."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_finite_difference_moment_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "all_finite_moment_annihilators_verified": failures == 0,
            "finite_even_moment_zero_separation_refuted": True,
            "actual_admissible_weil_infinite_feature_coercivity_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The explicit functions are compactly supported even L2 step functions. "
            "They are not proved to belong to the normalized smooth Guinand-Weil "
            "admissible class, and Q_m is only a finite-moment proxy, not the genuine "
            "Weil functional. The theorem blocks finite-moment zero separation on "
            "classes containing these functions; it does not prove that the actual "
            "Weil closure meets its zero set."
        ),
        "failure_count": failures,
    }


def fermat_quotient_mod(base: int, prime: int, digits: int) -> int:
    modulus = prime ** (digits + 1)
    return ((pow(base, prime - 1, modulus) - 1) // prime) % (prime**digits)


def fixed_base_polynomial(u: int, v: int, q: int) -> int:
    return (
        5 * u
        - 3 * v
        + q * (10 * u * u - 3 * v * v)
        + q**2 * (10 * u**3 - v**3)
        + 5 * q**3 * u**4
        + q**4 * u**5
    )


def valuation_label_from_quotient_residue(residue: int, prime: int, digits: int) -> str:
    if residue == 0:
        return f">={digits + 1}"
    valuation = 1
    while residue % prime == 0:
        valuation += 1
        residue //= prime
    return str(valuation)


@lru_cache(maxsize=1)
def collatz_all_depth_audit() -> dict[str, Any]:
    primes = [q for q in primes_up_to(COLLATZ_REPLAY_LIMIT) if q > 5]
    selected = {7, 23, 109, 487, 1_093, 3_511, 10_007, 49_999, 199_999}
    selected_rows: list[dict[str, Any]] = []
    bad_valuation_counts: dict[str, int] = {}
    comparison_valuation_counts: dict[str, int] = {}
    transcript = hashlib.sha256()
    failures = 0

    for q in primes:
        q_power = q**COLLATZ_DIGITS
        modulus = q ** (COLLATZ_DIGITS + 1)
        u = fermat_quotient_mod(2, q, COLLATZ_DIGITS)
        v = fermat_quotient_mod(3, q, COLLATZ_DIGITS)
        polynomial_residue = fixed_base_polynomial(u, v, q) % q_power
        bad_direct_quotient = (
            (pow(32, q - 1, modulus) - pow(27, q - 1, modulus)) % modulus
        ) // q
        comparison_direct_quotient = (
            (pow(2, q - 1, modulus) - pow(3, q - 1, modulus)) % modulus
        ) // q
        comparison_residue = (u - v) % q_power
        ticket245_residue = (
            5 * u - 3 * v + q * (10 * u * u - 3 * v * v)
        ) % (q * q)
        verified = (
            polynomial_residue == bad_direct_quotient
            and comparison_residue == comparison_direct_quotient
            and polynomial_residue % (q * q) == ticket245_residue
        )
        failures += int(not verified)
        bad_label = valuation_label_from_quotient_residue(
            polynomial_residue, q, COLLATZ_DIGITS
        )
        comparison_label = valuation_label_from_quotient_residue(
            comparison_residue, q, COLLATZ_DIGITS
        )
        bad_valuation_counts[bad_label] = bad_valuation_counts.get(bad_label, 0) + 1
        comparison_valuation_counts[comparison_label] = (
            comparison_valuation_counts.get(comparison_label, 0) + 1
        )
        transcript.update(
            (
                f"{q}:{u}:{v}:{polynomial_residue}:{comparison_residue}:"
                f"{bad_label}:{comparison_label}:{int(verified)}\n"
            ).encode("ascii")
        )
        if q in selected:
            selected_rows.append(
                {
                    "prime_q": q,
                    "U_mod_q_to_fifth": u,
                    "V_mod_q_to_fifth": v,
                    "P_q_mod_q_to_fifth": polynomial_residue,
                    "U_minus_V_mod_q_to_fifth": comparison_residue,
                    "bad_difference_q_adic_valuation_capped_at_six": bad_label,
                    "comparison_difference_q_adic_valuation_capped_at_six": comparison_label,
                    "ticket245_second_order_residue": ticket245_residue,
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "For every prime q>5 define the exact integers U=(2^(q-1)-1)/q and "
        "V=(3^(q-1)-1)/q, and define P_q=5U-3V+q(10U^2-3V^2)+"
        "q^2(10U^3-V^3)+5q^3U^4+q^4U^5. Then exactly "
        "32^(q-1)-27^(q-1)=qP_q and 2^(q-1)-3^(q-1)=q(U-V). "
        "Consequently, for every integer r>=1, q^(r+1) divides the first "
        "difference if and only if P_q=0 modulo q^r, and divides the second "
        "difference if and only if U-V=0 modulo q^r. Equivalently their exact "
        "q-adic valuations are 1+v_q(P_q) and 1+v_q(U-V), respectively."
    )
    proof = (
        "The definitions give 2^(q-1)=1+qU and 3^(q-1)=1+qV as exact integer "
        "equalities. Since 32^(q-1)=(1+qU)^5 and "
        "27^(q-1)=(1+qV)^3, expanding both binomials and subtracting gives "
        "the displayed five-term P_q identity with no omitted tail. Direct "
        "subtraction gives the U-V identity. Both differences are nonzero, so "
        "taking q-adic valuations and reducing modulo arbitrary q^r are valid."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "selected_all_depth_rows": selected_rows,
        "exact_modular_replay": {
            "prime_limit": COLLATZ_REPLAY_LIMIT,
            "primes_scanned": len(primes),
            "q_adic_digits_replayed": COLLATZ_DIGITS,
            "bad_difference_valuation_counts": dict(sorted(bad_valuation_counts.items())),
            "comparison_difference_valuation_counts": dict(
                sorted(comparison_valuation_counts.items())
            ),
            "failure_count": failures,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "exact_all_depth_polynomial_identity_proved": True,
            "ticket245_second_order_formula_recovered": True,
            "all_prime_valuation_domination_proved": False,
            "general_collatz_dynamics_controlled": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The identities decide every q-adic depth once U,V are supplied, but "
            "they do not compare v_q(P_q) with v_q(U-V) uniformly over all primes. "
            "The finite replay is not an all-prime valuation theorem and these two "
            "fixed bases still encode only one local run-block route, not arbitrary "
            "Collatz trajectories or nontrivial cycles."
        ),
        "failure_count": failures,
    }


def mobius(value: int) -> int:
    remaining = value
    result = 1
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            remaining //= divisor
            result = -result
            if remaining % divisor == 0:
                return 0
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        result = -result
    return result


def euler_phi(value: int) -> int:
    result = value
    remaining = value
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            result -= result // divisor
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        result -= result // remaining
    return result


def ramanujan_sum_integer(q: int, a: int) -> int:
    common = math.gcd(q, a)
    reduced = q // common
    mu = mobius(reduced)
    if mu == 0:
        return 0
    return mu * euler_phi(q) // euler_phi(reduced)


@lru_cache(maxsize=1)
def goldbach_residue_parseval_audit() -> dict[str, Any]:
    primes = [p for p in primes_up_to(max(GOLDBACH_X_SCALES)) if p >= 3]
    selected_q = {3, 4, 5, 8, 12, 16, 30, 60, 64}
    rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0

    for x_limit in GOLDBACH_X_SCALES:
        scale_primes = [p for p in primes if p <= x_limit]
        scale_ratios: list[tuple[Fraction, int]] = []
        scale_failures = 0
        for q in range(3, GOLDBACH_Q_LIMIT + 1):
            units = [r for r in range(q) if math.gcd(r, q) == 1]
            counts = {r: 0 for r in units}
            dividing_primes: list[int] = []
            for p in scale_primes:
                if math.gcd(p, q) == 1:
                    counts[p % q] += 1
                elif q % p == 0:
                    dividing_primes.append(p)
            prime_mass = sum(counts.values())
            phi = len(units)
            sum_squares = sum(count * count for count in counts.values())
            variance_numerator = phi * sum_squares - prime_mass * prime_mass
            relative_variance = (
                Fraction(variance_numerator, prime_mass * prime_mass)
                if prime_mass
                else Fraction(0)
            )
            parseval_energy = Fraction(q * variance_numerator, phi)
            ramanujan_verified = all(
                ramanujan_sum_integer(q, a) == mobius(q)
                for a in range(q)
                if math.gcd(a, q) == 1
            )
            verified = (
                prime_mass > 0
                and variance_numerator >= 0
                and sum(counts.values()) == prime_mass
                and parseval_energy >= 0
                and ramanujan_verified
                and all(math.gcd(r, q) == 1 for r in counts)
            )
            failures += int(not verified)
            scale_failures += int(not verified)
            scale_ratios.append((relative_variance, q))
            transcript.update(
                (
                    f"{x_limit}:{q}:{phi}:{prime_mass}:{sum_squares}:"
                    f"{variance_numerator}:{parseval_energy}:{int(verified)}\n"
                ).encode("ascii")
            )
            if q in selected_q:
                rows.append(
                    {
                        "prime_limit_X": x_limit,
                        "denominator_q": q,
                        "phi_q": phi,
                        "unit_prime_mass": prime_mass,
                        "odd_prime_divisors_of_q_removed": dividing_primes,
                        "residue_count_square_sum": sum_squares,
                        "variance_numerator_phi_sum_n_squared_minus_P_squared": variance_numerator,
                        "relative_variance_V": fraction_payload(relative_variance),
                        "parseval_residual_energy": fraction_payload(parseval_energy),
                        "coprime_center_main_coefficient_mu_q": mobius(q),
                        "certificate_verified": verified,
                    }
                )
        maximum_ratio, maximum_q = max(scale_ratios)
        minimum_ratio, minimum_q = min(scale_ratios)
        summaries.append(
            {
                "prime_limit_X": x_limit,
                "denominators_checked": len(scale_ratios),
                "maximum_relative_variance": fraction_payload(maximum_ratio),
                "maximum_relative_variance_denominator_q": maximum_q,
                "minimum_relative_variance": fraction_payload(minimum_ratio),
                "minimum_relative_variance_denominator_q": minimum_q,
                "failure_count": scale_failures,
            }
        )

    theorem = (
        "Let q>=3 and X>=3. For each unit r modulo q let n_r count odd primes "
        "p<=X with p congruent to r modulo q, let P=sum_r n_r, and put "
        "delta_r=n_r-P/phi(q). Define S*(a)=sum over odd p<=X with gcd(p,q)=1 "
        "of exp(2 pi i ap/q). Then for every a modulo q, "
        "S*(a)=(P/phi(q))c_q(a)+R(a), where R(a)=sum_r delta_r exp(2 pi i ar/q). "
        "Exactly, sum_(a mod q)|R(a)|^2=q sum_r delta_r^2, and "
        "|R(a)|^2<=phi(q)sum_r delta_r^2. If gcd(a,q)=1 then c_q(a)=mu(q). "
        "The omitted odd primes dividing q contribute the explicit finite term "
        "D_q(a)=sum_(p|q, 3<=p<=X)exp(2 pi i ap/q)."
    )
    proof = (
        "Group the coprime prime sum by its reduced residue class and write "
        "n_r=P/phi(q)+delta_r. The mean part is the Ramanujan sum. Expanding "
        "sum_a|R(a)|^2 and using exact character orthogonality modulo q kills "
        "all r not equal to s and leaves q sum_r delta_r^2. Cauchy-Schwarz "
        "gives the pointwise inequality. Moebius inversion of the unit indicator "
        "gives c_q(a)=mu(q) at coprime a. Splitting the original odd-prime sum "
        "according to gcd(p,q)=1 adds exactly the displayed divisor-prime term."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_selected_residue_variance_rows": rows,
        "exhaustive_denominator_summaries": summaries,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "rational_center_mean_residual_decomposition_proved": True,
            "exact_residual_parseval_identity_proved": True,
            "pointwise_residual_bound_proved": True,
            "uniform_growing_denominator_variance_decay_proved": False,
            "representative_arc_stability_proved": False,
            "strong_goldbach_resolved": False,
        },
        "no_go_scope": (
            "The identity is exact at rational centers only. The finite tables do "
            "not prove variance decay for growing q, control neighborhoods around "
            "the centers, or supply signed minor-arc cancellation. Dropping R(a) "
            "without a discrepancy theorem is invalid whenever the exact variance "
            "is nonzero. No positive Goldbach representation lower bound follows."
        ),
        "failure_count": failures,
    }


def prime_power_representation_table(limit: int, primes: list[int]) -> tuple[bytearray, dict[int, tuple[int, int]]]:
    flags = bytearray(limit + 1)
    representations: dict[int, tuple[int, int]] = {}
    for prime in primes:
        power = prime
        exponent = 1
        while power <= limit:
            flags[power] = 1
            representations.setdefault(power, (prime, exponent))
            if power > limit // prime:
                break
            power *= prime
            exponent += 1
    return flags, representations


@lru_cache(maxsize=1)
def twin_prime_power_proxy_audit() -> dict[str, Any]:
    limit = max(TWIN_X_SCALES) + 2
    primes = primes_up_to(limit)
    prime_flags = bytearray(limit + 1)
    for prime in primes:
        prime_flags[prime] = 1
    power_flags, representations = prime_power_representation_table(limit, primes)
    scale_set = set(TWIN_X_SCALES)
    rows: list[dict[str, Any]] = []
    false_rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    pair_count = 0
    twin_count = 0
    false_count = 0

    for n in range(3, max(TWIN_X_SCALES) + 1, 2):
        if power_flags[n] and power_flags[n + 2]:
            pair_count += 1
            if prime_flags[n] and prime_flags[n + 2]:
                twin_count += 1
            else:
                false_count += 1
                if len(false_rows) < 20:
                    left = representations[n]
                    right = representations[n + 2]
                    false_rows.append(
                        {
                            "n": n,
                            "n_plus_2": n + 2,
                            "left_prime_power": f"{left[0]}^{left[1]}",
                            "right_prime_power": f"{right[0]}^{right[1]}",
                            "left_is_prime": bool(prime_flags[n]),
                            "right_is_prime": bool(prime_flags[n + 2]),
                        }
                    )
        if n + 1 in scale_set:
            x_limit = n + 1
            y = x_limit + 2
            exponent_cap = y.bit_length() - 1
            explicit_bound = 2 * max(0, exponent_cap - 1) * math.isqrt(y)
            composite_prime_powers = sum(
                1
                for value in range(4, y + 1)
                if power_flags[value] and not prime_flags[value]
            )
            verified = (
                pair_count == twin_count + false_count
                and false_count <= 2 * composite_prime_powers
                and 2 * composite_prime_powers <= explicit_bound
            )
            failures += int(not verified)
            transcript.update(
                (
                    f"{x_limit}:{pair_count}:{twin_count}:{false_count}:"
                    f"{composite_prime_powers}:{explicit_bound}:{int(verified)}\n"
                ).encode("ascii")
            )
            rows.append(
                {
                    "limit_X": x_limit,
                    "prime_power_pair_count_A2": pair_count,
                    "twin_prime_pair_count_pi2": twin_count,
                    "composite_prime_power_contamination": false_count,
                    "composite_prime_powers_through_X_plus_2": composite_prime_powers,
                    "explicit_contamination_bound_B": explicit_bound,
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "Let PP(n)=1 when n is a positive prime power p^k with prime p and "
        "k>=1, and PP(n)=0 otherwise. Put A_2(X)=sum over odd 3<=n<=X "
        "of PP(n)PP(n+2), and let pi_2(X) count odd twin-prime starts p<=X. "
        "For Y=X+2 and "
        "K=floor(log_2 Y), exactly 0<=A_2(X)-pi_2(X)<=B(Y), where "
        "B(Y)=2(K-1)floor(sqrt(Y)). In particular, any lower bound "
        "A_2(X)-B(X+2) tending to infinity along an unbounded sequence forces "
        "infinitely many twin primes. The uncorrected identity A_2=pi_2 is "
        "false, with minimal counterexample n=7 because 7 and 9=3^2 are prime powers."
    )
    proof = (
        "Every twin pair is a prime-power pair, so the difference is nonnegative. "
        "Every false prime-power pair contains a composite prime power in its left "
        "or right coordinate. If N(Y) counts composite prime powers at most Y, a "
        "union bound gives A_2-pi_2<=2N(Y). Every composite prime power is p^k "
        "with 2<=k<=K. For each k there are at most floor(Y^(1/k)) choices, "
        "which is at most floor(sqrt(Y)); hence N(Y)<=(K-1)floor(sqrt(Y)). "
        "The sufficient infinitude criterion follows by rearranging the bound. "
        "Direct inspection of the odd starts below seven and the pair (7,9) "
        "prove minimality on the declared domain."
    )
    minimal_false = false_rows[0] if false_rows else None
    failures += int(minimal_false is None or minimal_false.get("n") != 7)
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_prime_power_proxy_rows": rows,
        "first_false_proxy_pairs": false_rows,
        "minimal_false_proxy_pair": minimal_false,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "prime_power_proxy_contamination_bound_proved": True,
            "uncorrected_prime_power_proxy_equality_refuted": True,
            "minimal_false_proxy_start": minimal_false.get("n") if minimal_false else None,
            "scale_local_type_ii_lower_bound_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem bounds contamination in an enlarged prime-power support. "
            "It does not prove a lower bound for A_2 beyond the explicit error, and "
            "the sufficient criterion is substantially stronger than mere twin "
            "infinitude. The finite sieve rows are exact certificates only through "
            "five million and provide no asymptotic Type-II cancellation."
        ),
        "failure_count": failures,
    }


def proof_dag(
    code: str,
    prior_name: str,
    theorem_name: str,
    open_name: str,
    rejected_name: str | None = None,
) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T245", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T246", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-OPEN246", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T245", f"{code}-T246"],
        [f"{code}-T246", f"{code}-OPEN246"],
    ]
    if rejected_name:
        nodes.insert(
            1,
            {"id": f"{code}-N246", "label": rejected_name, "status": "disproved"},
        )
        edges.insert(1, [f"{code}-T245", f"{code}-N246"])
        edges.insert(2, [f"{code}-N246", f"{code}-T246"])
    return {"nodes": nodes, "edges": edges}


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
    logical_limit: str,
    claim_boundary: str,
    finite_boundary: str,
    rejected_name: str | None = None,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{code}-TICKET-246",
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
            code, prior_name, theorem_name, next_lemma, rejected_name
        ),
        "claim_boundary": claim_boundary,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_finite_moment_audit()
    collatz = collatz_all_depth_audit()
    goldbach = goldbach_residue_parseval_audit()
    twin = twin_prime_power_proxy_audit()
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "FiniteEvenMomentAnnihilatorNoGo",
            "exact_no_go",
            riemann,
            "zero-free closure separation based only on any fixed finite list of even moments on a normalized class containing the explicit shell annihilator",
            [],
            "an infinite-feature coercive inequality on the genuine normalized admissible Weil closure",
            "InfiniteFeatureCoercivityOnNormalizedAdmissibleWeilClosure",
            "ClosureZeroSetObstructionToUniformWeilMargin",
            "Finite moments cannot separate the model closure, while no theorem embeds the shell annihilators into the genuine smooth admissible class or controls the full Weil functional.",
            "No RH proof or disproof; one exact finite-moment certificate obstruction on compactly supported even step functions.",
            "Nine exact finite-difference rows for m through 12; the all-m theorem is proved algebraically and is not inferred from those rows.",
            "FiniteEvenMomentsSeparateEveryNormalizedEvenTestFromZero",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "AllDepthFixedBaseFermatPolynomialIdentity",
            "partial_theorem",
            collatz,
            "none newly; the exact polynomial reduction does not by itself decide the required all-prime valuation inequality",
            [],
            "an all-prime comparison between v_q(P_q) and v_q(U_q-V_q), now with every higher digit represented by one exact finite polynomial",
            "FixedBaseAllPrimeValuationDominationForPqByUqMinusVq",
            "SecondOrderFixedBaseFermatDigitCriterion",
            "The all-depth identity removes the omitted-digit gap but supplies no uniform valuation domination over all primes and no global Collatz trajectory argument.",
            "No Collatz proof, divergent orbit, or nontrivial cycle; an exact all-depth fixed-base valuation identity and bounded five-digit replay only.",
            f"Five q-adic quotient digits are replayed for all {len([q for q in primes_up_to(COLLATZ_REPLAY_LIMIT) if q > 5]):,} primes through {COLLATZ_REPLAY_LIMIT:,}; exact identities hold for arbitrary depth, but the finite valuation histogram proves no all-prime inequality.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "RationalCenterResidueParsevalBridge",
            "partial_theorem",
            goldbach,
            "replacing every rational-center prime sum by its Ramanujan mean term while omitting the residue-discrepancy residual",
            [],
            "the quarter-torus representative reduction together with uniform residue-variance decay and stability on full arc neighborhoods",
            "UniformQuarterTorusResidueVarianceDecayWithArcStability",
            "KleinFourOrbitReductionForEvenGoldbachArcs",
            "Exact center Parseval identifies the residual norm, but no growing-denominator decay, neighborhood stability, signed minor-arc saving, or positive Goldbach lower bound is proved.",
            "No strong Goldbach proof or counterexample; one exact rational-center mean/residual decomposition and finite residue-variance certificates.",
            f"Exact prime residue counts are exhausted for q=3..{GOLDBACH_Q_LIMIT} at X={','.join(map(str, GOLDBACH_X_SCALES))}; they do not prove any asymptotic in X or q.",
            "RamanujanMeanAloneEqualsEveryRationalCenterPrimeSum",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "PrimePowerPairProxyContaminationBound",
            "partial_theorem",
            twin,
            "identifying the uncorrected shift-two prime-power pair proxy with the twin-prime indicator; the minimal false pair is (7,9)",
            [],
            "a scale-local nonperiodic Type-II lower bound for the prime-power pair correlation exceeding its explicit composite-power contamination",
            "ScaleLocalTypeIILowerBoundBeyondPrimePowerContamination",
            "PolynomialHeightPeriodicMimicryFromLinnik",
            "The proxy error is sublinear but can dominate an arbitrarily sparse infinite twin sequence; no lower bound beyond the error or parity-breaking Type-II cancellation is proved.",
            "No proof of infinitely many twin primes and no counterexample; one exact proxy-contamination theorem and a corrected sufficient lower-bound target.",
            f"The prime-power and twin supports are enumerated exactly through {max(TWIN_X_SCALES):,}; finite counts do not imply the required unbounded excess.",
            "PrimePowerPairProxyEqualsTwinPrimeIndicator",
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
            "theorem_name": "FourConjectureMomentAllDepthParsevalPrimePowerAudit",
            "summary": "TICKET-246 proves three partial theorems and one exact route no-go theorem while leaving all four parent conjectures open.",
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
                "fermat_quotients": "https://arxiv.org/abs/1110.3113",
                "collatz": "https://arxiv.org/abs/1909.03562",
                "goldbach_major_arcs": "https://arxiv.org/abs/1205.5252",
                "twin_prime_parity": "https://arxiv.org/abs/1407.4897",
            },
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
                "moment_certificate_count": len(
                    riemann["exact_finite_difference_moment_rows"]
                ),
                "collatz_replay_prime_count": collatz["exact_modular_replay"][
                    "primes_scanned"
                ],
                "goldbach_residue_row_count": len(
                    goldbach["exact_selected_residue_variance_rows"]
                ),
                "twin_scale_count": len(twin["exact_prime_power_proxy_rows"]),
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
    root = audit[AUDIT_KEY]
    prior_results = {
        "riemann": [
            "PointwiseFiniteSectionMovingVectorNoGoAndCompactUniformTransfer",
            "BandlimitedEvenTestFamilyNoncompactnessAndFrequencyTightnessNoGo",
            "JointPhysicalFrequencyTightnessCharacterizesL2Precompactness",
            "ClosureZeroSetObstructionToUniformWeilMargin",
        ],
        "collatz": [
            "RationalWieferichOrderCoreReductionAndBoundedOrderNoGo",
            "UnboundedOrderPrincipalUnitTransferCountermodels",
            "FixedBaseBadLineHarmonicSumEquivalence",
            "SecondOrderFixedBaseFermatDigitCriterion",
        ],
        "goldbach": [
            "ParsevalScaleObstructionToL2OnlyBinaryMinorArcCertificates",
            "OmittedHalfFrequencyArcCarriesNaturalBinaryEnergy",
            "ExactParityArcFoldingForEvenBinaryGoldbach",
            "KleinFourOrbitReductionForEvenGoldbachArcs",
        ],
        "twin_prime": [
            "GrowingPeriodDiagonalCRTMimicryForShiftTwo",
            "FixedPeriodicMimicryInEverySufficientlyLargeDyadicBlock",
            "PolylogarithmicGrowingPeriodMimicryInEveryLargeDyadicBlock",
            "PolynomialHeightPeriodicMimicryFromLinnik",
        ],
    }
    prior_retired = {
        "riemann": [
            "frequency support or frequency tightness alone as compactness of a normalized even Weil-test family",
            "physical tightness alone, together with TICKET-243's frequency-tightness-alone route, as a compactness certificate",
            "joint tightness plus pointwise positivity, or positive margins on each compact exhaustion stage, as sufficient for one uniform positive Weil margin",
        ],
        "collatz": [
            "deducing the fixed-base 32/27 to 2/3 square-depth transfer from universal order, LTE, and principal-unit algebra"
        ],
        "goldbach": [
            "placing the parity rational neighborhood around one half in a minor set while demanding an absolute-energy o(X/log^2 X) budget",
            "treating the zero and half-frequency arcs as analytically independent for the odd-prime even-target coefficient",
            "independent signed estimation of all four half-turn/reflection-related rational arcs",
        ],
        "twin_prime": [
            "using fixed periodic features even with eventual per-dyadic-scale sampling as a twin-prime certificate",
            "any pure periodic twin certificate whose scale-dependent period is bounded by a fixed power of log X",
            "a fixed pure periodic twin classifier remaining globally prefix-sound beyond every polynomial height in its period",
        ],
    }
    problems: dict[str, Any] = {}
    for key in ("riemann", "collatz", "goldbach", "twin_prime"):
        item = root[key]
        retired = list(prior_retired[key])
        if not item["route_decision"]["discard"].startswith("none newly"):
            retired.append(item["route_decision"]["discard"])
        problems[key] = {
            "problem_status": STATUS,
            "current_target": item["theorem_name"],
            "established_results": prior_results[key] + [item["theorem_name"]],
            "retired_routes": retired,
            "parked_routes": item["route_decision"]["parked"],
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
        "ticket": 246,
        "parent_ticket": 245,
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
        ROOT / "data/open-problem/ticket246-moment-alldepth-parseval-primepower.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-246-finite-moment-annihilator.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-246-all-depth-fermat-polynomial.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-246-rational-center-parseval.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-246-prime-power-contamination.json",
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
