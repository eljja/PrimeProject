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

from scripts.ticket246_moment_alldepth_parseval_primepower import (
    fixed_base_polynomial,
    prime_power_representation_table,
)
from scripts.ticket247_hilbert_hensel_lipschitz_primepower import (
    legendre_coefficients,
    legendre_rodrigues_coefficients,
    polynomial_integral_moment,
    polynomial_l2_norm_squared,
    primes_up_to,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket248-unweighted-wieferich-jet-active.v1"
GENERATED_AT = "2026-08-26T22:40:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "unweighted_wieferich_jet_active_audit"

RIEMANN_ORDERS = (1, 2, 4, 8, 16, 32, 64, 128)
RIEMANN_PARTIAL_CUTOFF = 256
COLLATZ_PRIME_LIMIT = 1_000_000
GOLDBACH_X_SCALES = (10_000, 100_000, 500_000)
GOLDBACH_Q_LIMIT = 96
GOLDBACH_SELECTED_Q = {3, 4, 5, 7, 8, 12, 16, 24, 32, 48, 64, 96}
TWIN_X_SCALES = (100, 1_000, 10_000, 100_000, 1_000_000, 5_000_000, 10_000_000)


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "display_float": float(value),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def legendre_even_moment_factorial(half_degree: int, moment_index: int) -> Fraction:
    if moment_index < half_degree:
        return Fraction(0)
    n = half_degree
    k = moment_index
    return Fraction(
        2 ** (2 * n + 1)
        * math.factorial(2 * k)
        * math.factorial(k + n),
        math.factorial(k - n) * math.factorial(2 * k + 2 * n + 1),
    )


def legendre_even_moment_product(half_degree: int, moment_index: int) -> Fraction:
    if moment_index < half_degree:
        return Fraction(0)
    n = half_degree
    k = moment_index
    value = Fraction(2, 2 * k + 1)
    for j in range(1, n + 1):
        value *= Fraction(2 * (k - j + 1), 2 * k + 2 * j + 1)
    return value


@lru_cache(maxsize=1)
def riemann_unweighted_moment_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for n in RIEMANN_ORDERS:
        recurrence = legendre_coefficients(2 * n)
        rodrigues = legendre_rodrigues_coefficients(2 * n)
        vanished = [
            polynomial_integral_moment(recurrence, 2 * k) for k in range(n)
        ]
        norm = polynomial_l2_norm_squared(recurrence)
        expected_norm = Fraction(2, 4 * n + 1)
        selected_indices = sorted({n, n + 1, 2 * n, RIEMANN_PARTIAL_CUTOFF})
        selected_moments = []
        formulas_agree = True
        for k in selected_indices:
            factorial_value = legendre_even_moment_factorial(n, k)
            product_value = legendre_even_moment_product(n, k)
            formulas_agree = formulas_agree and factorial_value == product_value
            selected_moments.append(
                {
                    "moment_index_k": k,
                    "unnormalized_moment": fraction_record(factorial_value),
                    "normalized_moment_squared": fraction_record(
                        Fraction(4 * n + 1, 2) * factorial_value * factorial_value
                    ),
                }
            )

        partial_q = Fraction(0)
        for k in range(n, RIEMANN_PARTIAL_CUTOFF + 1):
            moment = legendre_even_moment_factorial(n, k)
            partial_q += Fraction(4 * n + 1, 2) * moment * moment
        elementary_tail_bound = Fraction(4 * n + 1, 2 * RIEMANN_PARTIAL_CUTOFF)
        analytic_bound = Fraction(11, n)
        verified = (
            recurrence == rodrigues
            and all(value == 0 for value in vanished)
            and norm == expected_norm
            and formulas_agree
            and partial_q <= analytic_bound
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{n}:{partial_q.numerator}/{partial_q.denominator}:"
                f"{analytic_bound.numerator}/{analytic_bound.denominator}:"
                f"{int(formulas_agree)}:{int(verified)}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "half_degree_n": n,
                "legendre_degree": 2 * n,
                "partial_cutoff_K": RIEMANN_PARTIAL_CUTOFF,
                "vanished_even_moment_count": len(vanished),
                "exact_L2_norm_squared": fraction_record(norm),
                "selected_exact_moments": selected_moments,
                "partial_unweighted_energy": fraction_record(partial_q),
                "elementary_tail_bound_after_K": fraction_record(
                    elementary_tail_bound
                ),
                "proved_all_tail_energy_bound": fraction_record(analytic_bound),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let H=L2_even([-1,1]) and Q_0(f)=sum_(k>=0) |integral_(-1)^1 "
        "x^(2k)f(x)dx|^2, allowing +infinity. For n>=1 put "
        "f_n=sqrt((4n+1)/2)P_(2n). Then ||f_n||_2=1, its first n even "
        "moments vanish, Q_0(f_n) is finite, and Q_0(f_n)<=11/n. Hence "
        "inf Q_0 over the normalized even L2 sphere is zero. The raw "
        "unweighted infinite-moment family, which is not Hilbert-Schmidt, "
        "still cannot provide positive uniform coercivity on that sphere."
    )
    proof = (
        "For k>=n, Rodrigues integration gives mu_(n,k)=2/(2k+1) times "
        "product_(j=1)^n (k-j+1)/(k+j+1/2), and mu_(n,k)=0 for k<n. "
        "Using 1-u<=exp(-u), the product is at most "
        "exp(-n^2/(k+n+1)). Since k+n+1<=3k, the normalized square is "
        "at most ((4n+1)/2)k^(-2)exp(-2n^2/(3k)). The elementary lemma "
        "sum_(k>=1) x_k <= integral_0^infinity f(x)dx+2 sup f for a "
        "nonnegative unimodal sample f(k)=x_k gives 3/(2n^2)+18/(7n^4): "
        "the integral is 3/(2n^2), the maximum is 9e^(-2)/n^4, and "
        "e^2>7. Multiplication by (4n+1)/2 gives less than 11/n."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_legendre_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "unweighted_non_hilbert_schmidt_no_go_proved": True,
            "analytic_bound_constant": 11,
            "genuine_weil_admissible_closure_reached": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def collatz_wieferich_separation_audit() -> dict[str, Any]:
    primes = [q for q in primes_up_to(COLLATZ_PRIME_LIMIT) if q > 5]
    selected_q = {7, 11, 23, 101, 1009, primes[-1]}
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    zero_32_27: list[int] = []
    zero_2_3: list[int] = []
    separated: list[int] = []
    simultaneous: list[int] = []

    for q in primes:
        modulus = q * q
        pow32 = pow(32, q - 1, modulus)
        pow27 = pow(27, q - 1, modulus)
        pow2 = pow(2, q - 1, modulus)
        pow3 = pow(3, q - 1, modulus)
        w32 = ((pow32 - pow27) % modulus) // q
        w23 = ((pow2 - pow3) % modulus) // q
        u = ((pow2 - 1) % modulus) // q
        v = ((pow3 - 1) % modulus) // q
        polynomial_residue = fixed_base_polynomial(u, v, q) % q
        separated_here = w32 == 0 and w23 != 0
        simultaneous_here = w32 == 0 and w23 == 0
        verified = polynomial_residue == w32 and (u - v) % q == w23
        failures += int(not verified)
        if w32 == 0:
            zero_32_27.append(q)
        if w23 == 0:
            zero_2_3.append(q)
        if separated_here:
            separated.append(q)
        if simultaneous_here:
            simultaneous.append(q)
        transcript.update(
            f"{q}:{w32}:{w23}:{u}:{v}:{int(verified)}\n".encode("ascii")
        )
        if q in selected_q or w32 == 0 or w23 == 0:
            rows.append(
                {
                    "prime_q": q,
                    "W_32_27_mod_q": w32,
                    "W_2_3_mod_q": w23,
                    "fermat_quotient_2_mod_q": u,
                    "fermat_quotient_3_mod_q": v,
                    "P_q_mod_q": polynomial_residue,
                    "generalized_wieferich_32_over_27": w32 == 0,
                    "generalized_wieferich_2_over_3": w23 == 0,
                    "separated_bad_prime": separated_here,
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "For every prime q>5, let U_q=(2^(q-1)-1)/q, "
        "V_q=(3^(q-1)-1)/q, and let P_q be the TICKET-246 polynomial. "
        "Define W_q(a,b)=((a^(q-1)-b^(q-1))/q) mod q. Then exactly "
        "P_q(U_q,V_q)=W_q(32,27) mod q and U_q-V_q=W_q(2,3) mod q. "
        "Consequently the actual quotient pair violates first-level valuation "
        "domination precisely at primes in the set {W_q(32,27)=0} minus "
        "{W_q(2,3)=0}. These are separated generalized-Wieferich primes."
    )
    proof = (
        "The exact identities 32^(q-1)-27^(q-1)=qP_q(U_q,V_q) and "
        "2^(q-1)-3^(q-1)=q(U_q-V_q) were proved in TICKET-246. Divide by "
        "q and reduce modulo q. Thus v_q(P_q)>0 while v_q(U_q-V_q)=0 "
        "if and only if q^2 divides the first base difference but not the "
        "second. This is an exact arithmetic reduction, not an inference from "
        "the finite scan."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "selected_exact_rows": rows,
        "exact_modular_scan": {
            "prime_limit": COLLATZ_PRIME_LIMIT,
            "primes_checked": len(primes),
            "W_32_27_zero_primes": zero_32_27,
            "W_2_3_zero_primes": zero_2_3,
            "separated_bad_primes": separated,
            "simultaneous_zero_primes": simultaneous,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "actual_bad_branch_equivalence_proved": True,
            "finite_scan_proves_global_absence": False,
            "actual_valuation_domination_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def reduced_residues(q: int) -> list[int]:
    return [r for r in range(q) if math.gcd(r, q) == 1]


@lru_cache(maxsize=1)
def goldbach_centered_first_jet_audit() -> dict[str, Any]:
    primes = [p for p in primes_up_to(max(GOLDBACH_X_SCALES)) if p % 2 == 1]
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    denominator_cases = 0

    for x_limit in GOLDBACH_X_SCALES:
        active_primes = [p for p in primes if p <= x_limit]
        for q in range(3, GOLDBACH_Q_LIMIT + 1):
            denominator_cases += 1
            residues = reduced_residues(q)
            index = {r: i for i, r in enumerate(residues)}
            counts = [0] * len(residues)
            first_moments = [0] * len(residues)
            prime_count = 0
            prime_sum = 0
            prime_square_sum = 0
            for prime in active_primes:
                residue = prime % q
                if residue not in index:
                    continue
                slot = index[residue]
                counts[slot] += 1
                first_moments[slot] += prime
                prime_count += 1
                prime_sum += prime
                prime_square_sum += prime * prime

            phi = len(residues)
            d0_numerator = phi * sum(value * value for value in counts) - prime_count**2
            d1_numerator = (
                phi * sum(value * value for value in first_moments)
                - prime_sum**2
            )
            cross_numerator = (
                phi
                * sum(
                    count * moment
                    for count, moment in zip(counts, first_moments, strict=True)
                )
                - prime_count * prime_sum
            )
            d0_direct = sum(
                (Fraction(value) - Fraction(prime_count, phi)) ** 2
                for value in counts
            )
            d1_direct = sum(
                (Fraction(value) - Fraction(prime_sum, phi)) ** 2
                for value in first_moments
            )
            cross_direct = sum(
                (Fraction(count) - Fraction(prime_count, phi))
                * (Fraction(moment) - Fraction(prime_sum, phi))
                for count, moment in zip(counts, first_moments, strict=True)
            )
            verified = (
                d0_direct == Fraction(d0_numerator, phi)
                and d1_direct == Fraction(d1_numerator, phi)
                and cross_direct == Fraction(cross_numerator, phi)
                and d0_numerator >= 0
                and d1_numerator >= 0
                and cross_numerator * cross_numerator
                <= d0_numerator * d1_numerator
            )
            failures += int(not verified)
            transcript.update(
                (
                    f"{x_limit}:{q}:{phi}:{prime_count}:{prime_sum}:"
                    f"{prime_square_sum}:{d0_numerator}:{d1_numerator}:"
                    f"{cross_numerator}:{int(verified)}\n"
                ).encode("ascii")
            )
            if q in GOLDBACH_SELECTED_Q:
                rows.append(
                    {
                        "limit_X": x_limit,
                        "denominator_q": q,
                        "phi_q": phi,
                        "prime_count_P": prime_count,
                        "prime_first_moment_M": prime_sum,
                        "prime_second_moment_M2": prime_square_sum,
                        "phi_times_count_variance": d0_numerator,
                        "phi_times_first_moment_variance": d1_numerator,
                        "phi_times_cross_covariance": cross_numerator,
                        "count_variance_D0": fraction_record(
                            Fraction(d0_numerator, phi)
                        ),
                        "first_moment_variance_D1": fraction_record(
                            Fraction(d1_numerator, phi)
                        ),
                        "beta_squared_remainder_scale_M2_over_X4": fraction_record(
                            Fraction(prime_square_sum, x_limit**4)
                        ),
                        "beta_squared_first_jet_energy_D1_over_X4": fraction_record(
                            Fraction(d1_numerator, phi * x_limit**4)
                        ),
                        "certificate_verified": verified,
                    }
                )

    theorem = (
        "Fix q>=3 and X>=3. Over reduced residues r mod q let n_r count "
        "odd primes p<=X coprime to q, m_r sum those primes, P=sum n_r, "
        "M=sum m_r, delta_r=n_r-P/phi(q), eta_r=m_r-M/phi(q), and define "
        "R_j(a) as the additive Fourier transforms of delta and eta. For "
        "every real t, sum_(a mod q)|R_0(a)+itR_1(a)|^2="
        "q(D_0+t^2D_1), where D_0=sum delta_r^2 and D_1=sum eta_r^2. "
        "Moreover, with t=2pi beta, S*(a/q+beta) differs from "
        "c_q(a)(P+2pi i beta M)/phi(q)+R_0(a)+2pi i beta R_1(a) "
        "by at most 2pi^2 beta^2 M_2, M_2=sum p^2."
    )
    proof = (
        "Taylor's integral remainder gives |exp(iu)-1-iu|<=u^2/2, so "
        "termwise summation proves the second-order arc bound. Additive "
        "orthogonality gives sum_a|R_0|^2=qD_0, sum_a|R_1|^2=qD_1, and "
        "sum_a R_0 conjugate(R_1)=q sum_r delta_r eta_r, which is real. "
        "Therefore the cross term in |R_0+itR_1|^2 sums to zero. The exact "
        "identity gives mean-square and exceptional-numerator control, but "
        "does not turn it into a uniform pointwise saving."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_selected_first_jet_rows": rows,
        "exact_modular_replay": {
            "q_min": 3,
            "q_max": GOLDBACH_Q_LIMIT,
            "X_scales": list(GOLDBACH_X_SCALES),
            "denominator_cases": denominator_cases,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "centered_first_jet_parseval_identity_proved": True,
            "second_order_arc_remainder_proved": True,
            "uniform_all_numerator_saving_proved": False,
            "strong_goldbach_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def twin_active_contamination_audit() -> dict[str, Any]:
    upper = max(TWIN_X_SCALES) + 2
    primes = primes_up_to(upper)
    prime_flags = bytearray(upper + 1)
    for prime in primes:
        prime_flags[prime] = 1
    power_flags, _ = prime_power_representation_table(upper, primes)
    scale_set = set(TWIN_X_SCALES)
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    pair_count = 0
    twin_count = 0
    left_active = 0
    right_active = 0
    both_composite = 0

    for n in range(3, max(TWIN_X_SCALES) + 1, 2):
        if power_flags[n] and power_flags[n + 2]:
            pair_count += 1
            left_composite = not prime_flags[n]
            right_composite = not prime_flags[n + 2]
            if not left_composite and not right_composite:
                twin_count += 1
            if left_composite:
                left_active += 1
            if right_composite:
                right_active += 1
            if left_composite and right_composite:
                both_composite += 1

        if n + 1 in scale_set:
            x_limit = n + 1
            contamination = pair_count - twin_count
            exact_active_identity = left_active + right_active - both_composite
            active_union_bound = left_active + right_active
            verified = (
                contamination == exact_active_identity
                and contamination <= active_union_bound
                and active_union_bound <= 2 * sum(
                    1
                    for value in range(3, x_limit + 3, 2)
                    if power_flags[value] and not prime_flags[value]
                )
            )
            failures += int(not verified)
            transcript.update(
                (
                    f"{x_limit}:{pair_count}:{twin_count}:{contamination}:"
                    f"{left_active}:{right_active}:{both_composite}:"
                    f"{active_union_bound}:{int(verified)}\n"
                ).encode("ascii")
            )
            rows.append(
                {
                    "limit_X": x_limit,
                    "prime_power_pair_count_A2": pair_count,
                    "twin_prime_pair_count_pi2": twin_count,
                    "exact_contamination_A2_minus_pi2": contamination,
                    "left_active_composite_power_pairs_L": left_active,
                    "right_active_composite_power_pairs_R": right_active,
                    "both_composite_power_pairs_B": both_composite,
                    "exact_inclusion_exclusion_L_plus_R_minus_B": exact_active_identity,
                    "active_union_bound_L_plus_R": active_union_bound,
                    "ticket247_sharp_bound": next(
                        row["sharp_contamination_bound"]
                        for row in __import__(
                            "scripts.ticket247_hilbert_hensel_lipschitz_primepower",
                            fromlist=["twin_sharp_prime_power_audit"],
                        )
                        .twin_sharp_prime_power_audit()[
                            "exact_sharp_contamination_rows"
                        ]
                        if row["limit_X"] == x_limit
                    ),
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "Let PP(n) indicate an odd prime power, P(n) an odd prime, and "
        "C(n)=PP(n)-P(n). For X>=3 define A_2(X)=sum_(odd n<=X) "
        "PP(n)PP(n+2), pi_2 analogously with P, L=sum C(n)PP(n+2), "
        "R=sum PP(n)C(n+2), and B=sum C(n)C(n+2). Then exactly "
        "A_2(X)-pi_2(X)=L(X)+R(X)-B(X)<=L(X)+R(X). Thus only composite "
        "prime powers with an actual shift-two prime-power neighbor contribute "
        "to the correction; all inactive powers can be removed."
    )
    proof = (
        "For every pair with PP(n)PP(n+2)=1, failure to be a twin-prime pair "
        "is the union of the events C(n)=1 and C(n+2)=1. Inclusion-exclusion "
        "on this two-event set gives its indicator as C(n)PP(n+2)+"
        "PP(n)C(n+2)-C(n)C(n+2). Summing over odd n<=X proves the exact "
        "identity and the active union bound."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_active_contamination_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "active_contamination_identity_proved": True,
            "inactive_prime_powers_removed_from_correction": True,
            "unbounded_type_II_lower_bound_proved": False,
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
    return {
        "nodes": [
            {"id": f"{code}-T247", "label": prior_name, "status": "proved"},
            {"id": f"{code}-T248", "label": theorem_name, "status": "proved"},
            {
                "id": f"{code}-REJECT248",
                "label": rejected_name,
                "status": "disproved",
            },
            {"id": f"{code}-OPEN248", "label": open_name, "status": "open"},
        ],
        "edges": [
            [f"{code}-T247", f"{code}-T248"],
            [f"{code}-T248", f"{code}-REJECT248"],
            [f"{code}-T248", f"{code}-OPEN248"],
        ],
        "resolution_path": [f"{code}-T247", f"{code}-T248", f"{code}-OPEN248"],
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
        "ticket_id": f"{code}-TICKET-248",
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
    riemann = riemann_unweighted_moment_audit()
    collatz = collatz_wieferich_separation_audit()
    goldbach = goldbach_centered_first_jet_audit()
    twin = twin_active_contamination_audit()
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "UnweightedInfiniteMomentCoercivityNoGo",
            "exact_no_go",
            riemann,
            "uniform positive coercivity from the raw unweighted infinite even-moment family on the full normalized even L2 sphere",
            [],
            "arithmetic off-diagonal Weil features on the genuine normalized admissible closure",
            "ArithmeticOffDiagonalWeilCoercivityOnAdmissibleClosure",
            "HilbertSchmidtInfiniteMomentCoercivityNoGo",
            "UnweightedRawMomentsCoerceTheEvenL2UnitSphere",
            "The non-Hilbert-Schmidt diagonal raw-moment upgrade is now also closed, but the Legendre sequence has not been placed in the genuine Guinand-Weil admissible closure and no arithmetic off-diagonal form is controlled.",
            "No RH proof or disproof; one exact non-Hilbert-Schmidt raw-moment no-go on the full even L2 model.",
            f"{len(RIEMANN_ORDERS)} exact Legendre formula rows through half-degree {max(RIEMANN_ORDERS)} and cutoff {RIEMANN_PARTIAL_CUTOFF} audit the formulas; the all-n 11/n theorem is analytic, not inferred from those rows.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "ActualBadBranchGeneralizedWieferichSeparation",
            "partial_theorem",
            collatz,
            "treating a finite absence of separated generalized-Wieferich primes as an all-prime arithmetic exclusion",
            ["all-prime exclusion of separated generalized-Wieferich primes without a structural theorem"],
            "an exact construction or obstruction for separated generalized-Wieferich primes comparing 32/27 with 2/3",
            "ExistenceOfSeparatedGeneralizedWieferichPrimeFor32Over27Against2Over3",
            "FormalHenselBranchNoGoForValuationDomination",
            "FiniteSeparatedWieferichScanImpliesAllPrimeExclusion",
            "The actual bad-prime set is now exact, but neither its emptiness nor nonemptiness is proved, and even settling that valuation route would not control all Collatz trajectories.",
            "No Collatz proof, divergent orbit, or cycle; one exact reduction of the actual first-level branch obstruction to a separated generalized-Wieferich set.",
            f"Exact modular arithmetic checks all {len([q for q in primes_up_to(COLLATZ_PRIME_LIMIT) if q > 5]):,} primes q<= {COLLATZ_PRIME_LIMIT:,}; zero finite hits do not prove global absence.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "CenteredFirstJetParsevalArcBridge",
            "partial_theorem",
            goldbach,
            "using the zeroth-order 2 pi |beta| M mass bound as the final center-to-arc transfer",
            [],
            "a uniform arithmetic saving for the centered count/first-moment jet on every reduced quarter-torus numerator",
            "UniformReducedNumeratorCenteredFirstJetSavingOnQuarterTorus",
            "RationalCenterArcLipschitzBridgeAndCenterOnlyNoGo",
            "ZerothOrderPrimeMassLipschitzIsTheFinalArcBridge",
            "The exact first-jet energy controls an average and exceptional numerators, but no theorem converts it to the uniform pointwise saving needed for all even Goldbach targets.",
            "No strong Goldbach proof or counterexample; one exact second-order arc expansion and centered first-jet Parseval identity.",
            f"Exact integer/rational invariants cover q=3..{GOLDBACH_Q_LIMIT} at X={','.join(map(str, GOLDBACH_X_SCALES))}; they prove no growing-q uniform saving.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "ExactActivePrimePowerContaminationIdentity",
            "partial_theorem",
            twin,
            "using all odd composite prime powers, including those with no shift-two prime-power neighbor, as the final contamination correction",
            [],
            "a scale-local nonperiodic Type-II lower bound for A_2 exceeding the active shift-two contamination",
            "ScaleLocalTypeIILowerBoundBeyondActivePrimePowerContamination",
            "SharpOddPrimePowerContaminationBound",
            "AllCompositePrimePowersRemainActiveContaminants",
            "The correction is now the exact active inclusion-exclusion term, but no unbounded scale sequence has a Type-II lower bound for A_2 beyond it.",
            "No twin-prime proof or counterexample; one exact active-contamination identity and much sharper finite correction.",
            f"Prime-power supports are enumerated through {max(TWIN_X_SCALES):,}; the identity holds for every X, but finite positive twin counts imply no infinitude.",
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
            "theorem_name": "FourConjectureUnweightedWieferichJetActiveAudit",
            "summary": "TICKET-248 proves one exact no-go theorem and three partial theorems while leaving all four parent conjectures open.",
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
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
                "deep_focus_problem": "goldbach",
                "stagnated_problem_count": 0,
                "riemann_unweighted_certificate_count": len(
                    riemann["exact_legendre_rows"]
                ),
                "collatz_wieferich_prime_count": collatz["exact_modular_scan"][
                    "primes_checked"
                ],
                "goldbach_first_jet_row_count": len(
                    goldbach["exact_selected_first_jet_rows"]
                ),
                "twin_active_scale_count": len(
                    twin["exact_active_contamination_rows"]
                ),
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
        "ticket": 248,
        "parent_ticket": 247,
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
        ROOT / "data/open-problem/ticket248-unweighted-wieferich-jet-active.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-248-unweighted-moment-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-248-generalized-wieferich-separation.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-248-centered-first-jet-parseval.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-248-active-contamination-identity.json",
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
