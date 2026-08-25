from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket240-route-corrections-wieferich-prime-crt.v1"
GENERATED_AT = "2026-08-25T23:40:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "route_corrections_wieferich_prime_crt_audit"
PRIME_LIMIT = 20_000_000


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fraction_payload(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "float": float(value)}


def prime_flags_up_to(limit: int) -> bytearray:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            flags[prime * prime : limit + 1 : prime] = b"\x00" * (
                (limit - prime * prime) // prime + 1
            )
    return flags


def riemann_cotlar_audit() -> dict[str, Any]:
    mixture_constant = Fraction(1, 2)
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    previous_cotlar_sum = -1.0

    for dimension in (16, 32, 64, 128, 256, 512, 1024):
        absolute_rows: list[Fraction] = []
        cotlar_rows: list[float] = []
        for row in range(dimension):
            absolute_rows.append(
                sum(
                    mixture_constant * Fraction(1, 1 + abs(row - column))
                    for column in range(dimension)
                    if column != row
                )
            )
            cotlar_rows.append(
                sum(
                    math.sqrt(float(mixture_constant) / (1 + abs(row - column)))
                    for column in range(dimension)
                    if column != row
                )
            )

        maximum_absolute_row_sum = max(absolute_rows)
        maximum_cotlar_row_sum = max(cotlar_rows)
        lower_bound = 1 - mixture_constant
        verified = (
            lower_bound == Fraction(1, 2)
            and maximum_cotlar_row_sum > previous_cotlar_sum
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{dimension}:{maximum_absolute_row_sum}:"
                f"{maximum_cotlar_row_sum:.17g}:{lower_bound}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "dimension_J": dimension,
                "mixture_constant_C": fraction_payload(mixture_constant),
                "maximum_absolute_gram_cross_row_sum": fraction_payload(
                    maximum_absolute_row_sum
                ),
                "maximum_cotlar_sqrt_overlap_row_sum": maximum_cotlar_row_sum,
                "uniform_gram_lower_bound": fraction_payload(lower_bound),
                "cotlar_sum_increases": maximum_cotlar_row_sum
                > previous_cotlar_sum,
                "certificate_verified": verified,
            }
        )
        previous_cotlar_sum = maximum_cotlar_row_sum

    theorem = (
        "For 0<C<1 let R_ij=(1+|i-j|)^(-1) and "
        "G=(1-C)I+C R. Every finite section G_J is a Gram matrix with "
        "G_J>=(1-C)I. It can be realized by unit vectors w_j. For their "
        "rank-one projections P_j, ||P_i P_j||^(1/2)="
        "sqrt(C)(1+|i-j|)^(-1/2) when i!=j, so the Cotlar-Stein row sums "
        "diverge. Thus absolute Cotlar norm summability is not necessary "
        "for a uniform Gram lower bound and cannot, by itself, encode signed "
        "cross-shell cancellation."
    )
    proof = (
        "The identity (n+1)^(-1)=integral_0^1 t^n dt writes R as a positive "
        "mixture of the kernels [t^|i-j|]. For 0<=t<1, the quadratic "
        "form of this Toeplitz kernel is the integral of "
        "|sum_j z_j exp(ijtheta)|^2 against the nonnegative Poisson kernel "
        "(1-t^2)/(1-2t cos(theta)+t^2); the endpoint t=1 follows by a "
        "limit. Hence R is positive semidefinite with unit diagonal. "
        "Therefore G_J>=(1-C)I and a Gram realization by unit vectors exists. "
        "For rank-one orthogonal projections, "
        "||P_iP_j||=|<w_i,w_j>|=C/(1+|i-j|). A central row of the "
        "square-root overlap sum dominates two constant multiples of "
        "sum_(d<=J/2)d^(-1/2), which diverges. Projection norms are invariant "
        "under inner-product phase changes, so they do not by themselves "
        "record signed cancellation."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_model_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "uniform_positive_gram_family_proved": True,
            "cotlar_sqrt_overlap_summability_necessity_refuted": True,
            "cotlar_norms_do_not_encode_signed_cancellation": True,
            "arithmetic_weil_signed_operator_lower_bound_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "This does not refute the possibility that the actual arithmetic "
            "Weil shell operators satisfy a useful Cotlar estimate. It refutes "
            "only treating absolute Cotlar summability as a necessary or "
            "sign-sensitive bridge. The model contains no zeta-zero data."
        ),
        "failure_count": failures,
    }


def distinct_prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def multiplicative_order_ratio(numerator: int, denominator: int, prime: int) -> int:
    residue = numerator * pow(denominator, -1, prime) % prime
    order = prime - 1
    for factor in distinct_prime_factors(order):
        while order % factor == 0 and pow(residue, order // factor, prime) == 1:
            order //= factor
    return order


def valuation_of_power_difference(
    left: int, right: int, exponent: int, prime: int, cap: int = 8
) -> tuple[int, bool]:
    for depth in range(1, cap + 1):
        modulus = prime**depth
        if (pow(left, exponent, modulus) - pow(right, exponent, modulus)) % modulus:
            return depth - 1, False
    return cap, True


def fermat_quotient_mod_prime(base: int, prime: int) -> int:
    residue = pow(base, prime - 1, prime * prime)
    return ((residue - 1) // prime) % prime


def collatz_wieferich_audit(flags: bytearray) -> dict[str, Any]:
    representative_primes = {5, 7, 23, 29, 59, 109, 487, 1009, 10007}
    representatives: list[dict[str, Any]] = []
    x_depth_two_primes: list[int] = []
    y_depth_two_primes: list[int] = []
    ambiguous_higher_depth_primes: list[int] = []
    first_order_positive_candidates: list[int] = []
    scanned = 0
    transcript = hashlib.sha256()
    failures = 0

    for prime in range(5, PRIME_LIMIT + 1):
        if not flags[prime]:
            continue
        scanned += 1
        f2 = fermat_quotient_mod_prime(2, prime)
        f3 = fermat_quotient_mod_prime(3, prime)
        x_first = (5 * f2 - 3 * f3) % prime
        y_first = (f2 - f3) % prime
        x_depth_at_least_two = x_first == 0
        y_depth_at_least_two = y_first == 0
        if x_depth_at_least_two:
            x_depth_two_primes.append(prime)
        if y_depth_at_least_two:
            y_depth_two_primes.append(prime)
        if x_depth_at_least_two and y_depth_at_least_two:
            ambiguous_higher_depth_primes.append(prime)
        if x_depth_at_least_two and not y_depth_at_least_two:
            first_order_positive_candidates.append(prime)
        transcript.update(
            f"{prime}:{x_first}:{y_first}\n".encode("ascii")
        )

        if prime in representative_primes:
            order_x = multiplicative_order_ratio(32, 27, prime)
            order_y = multiplicative_order_ratio(2, 3, prime)
            local_period = math.lcm(order_x, order_y)
            local_x, censored_local_x = valuation_of_power_difference(
                32, 27, local_period, prime
            )
            local_y, censored_local_y = valuation_of_power_difference(
                2, 3, local_period, prime
            )
            fermat_x, censored_fermat_x = valuation_of_power_difference(
                32, 27, prime - 1, prime
            )
            fermat_y, censored_fermat_y = valuation_of_power_difference(
                2, 3, prime - 1, prime
            )
            verified = (
                not censored_local_x
                and not censored_local_y
                and not censored_fermat_x
                and not censored_fermat_y
                and local_x == fermat_x
                and local_y == fermat_y
                and (fermat_x >= 2) == x_depth_at_least_two
                and (fermat_y >= 2) == y_depth_at_least_two
            )
            failures += int(not verified)
            representatives.append(
                {
                    "prime_q": prime,
                    "local_period_ell_q": local_period,
                    "q_minus_one_multiplier": (prime - 1) // local_period,
                    "local_x_depth_a_q": local_x,
                    "fermat_x_depth_W_q_32_over_27": fermat_x,
                    "local_y_depth_c_q": local_y,
                    "fermat_y_depth_W_q_2_over_3": fermat_y,
                    "fermat_quotient_linear_form_x": x_first,
                    "fermat_quotient_linear_form_y": y_first,
                    "depth_reduction_verified": verified,
                }
            )

    bounded_no_positive = not x_depth_two_primes
    failures += int(not bounded_no_positive)
    theorem = (
        "For every prime q>3, let ell_q=lcm(ord_q(32/27),ord_q(2/3)) and "
        "define a_q and c_q as in TICKET-239. Since ell_q divides q-1 and "
        "q does not divide (q-1)/ell_q, LTE gives the exact reduction "
        "a_q=v_q(32^(q-1)-27^(q-1)) and "
        "c_q=v_q(2^(q-1)-3^(q-1)). Hence the global nonpositive-defect "
        "claim is exactly a rational Wieferich-depth domination problem. "
        "At first depth, writing F_q(b)=(b^(q-1)-1)/q mod q, a_q>=2 iff "
        "5F_q(2)-3F_q(3)=0 mod q, while c_q>=2 iff "
        "F_q(2)-F_q(3)=0 mod q."
    )
    proof = (
        "Put r=(q-1)/ell_q. For (U,V)=(32^ell_q,27^ell_q) and "
        "(2^ell_q,3^ell_q), q is odd, q divides U-V, q does not divide UV, "
        "and q does not divide r because 1<=r<q. LTE gives "
        "v_q(U^r-V^r)=v_q(U-V)+v_q(r)=v_q(U-V), proving both equalities. "
        "Modulo q^2, b^(q-1)=1+qF_q(b). Multiplication and inversion give "
        "the first quotient of (2^5/3^3)^(q-1)-1 as "
        "5F_q(2)-3F_q(3), and that of (2/3)^(q-1)-1 as "
        "F_q(2)-F_q(3)."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "representative_depth_reduction_rows": representatives,
        "bounded_rational_wieferich_scan": {
            "prime_limit": PRIME_LIMIT,
            "odd_primes_scanned": scanned,
            "x_depth_at_least_two_count": len(x_depth_two_primes),
            "x_depth_at_least_two_primes": x_depth_two_primes[:50],
            "y_depth_at_least_two_count": len(y_depth_two_primes),
            "y_depth_at_least_two_primes": y_depth_two_primes[:50],
            "ambiguous_higher_depth_count": len(ambiguous_higher_depth_primes),
            "first_order_positive_defect_candidate_count": len(
                first_order_positive_candidates
            ),
            "first_order_positive_defect_candidates": (
                first_order_positive_candidates[:50]
            ),
            "scope": (
                "The absence of an x-depth-two prime through this finite limit "
                "proves nonpositive defect only in the scanned range. It does "
                "not prove rational Wieferich-depth domination for all primes."
            ),
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "local_defect_fermat_depth_reduction_proved": True,
            "first_order_fermat_quotient_criterion_proved": True,
            "bounded_scan_has_no_positive_defect": bounded_no_positive,
            "all_prime_depth_domination_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The reduction replaces an opaque order scan by a precise rational "
            "Wieferich comparison, but no known argument excludes exceptional "
            "primes above the bound. Even global domination would settle only "
            "the run-block finite-palette route, not general necklaces or "
            "aperiodic Collatz descent."
        ),
        "failure_count": failures,
    }


def goldbach_signed_slack_audit(flags: bytearray) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for cutoff in (1_000, 10_000, 100_000, 1_000_000, 10_000_000):
        base_buffer = cutoff / (math.log(cutoff) ** 2)
        for multiplier in (1, 2, 4):
            buffer_width = max(2, 2 * math.ceil(multiplier * base_buffer / 2))
            modulus = 2 * buffer_width + 1
            offsets = {
                offset
                for offset in range(buffer_width + 1)
                if cutoff - offset >= 2 and flags[cutoff - offset]
            }
            cardinality = len(offsets)
            reflection_count = sum(
                1 for offset in offsets if buffer_width - offset in offsets
            )
            dc_term = Fraction(cardinality * cardinality, modulus)
            signed_remainder = Fraction(reflection_count) - dc_term
            strict_threshold = signed_remainder > -dc_term
            integral_unit_threshold = signed_remainder >= 1 - dc_term
            represented = reflection_count >= 1
            verified = strict_threshold == represented == integral_unit_threshold
            failures += int(not verified)
            transcript.update(
                (
                    f"{cutoff}:{multiplier}:{buffer_width}:{modulus}:"
                    f"{cardinality}:{reflection_count}:{dc_term}:"
                    f"{signed_remainder}\n"
                ).encode("ascii")
            )
            rows.append(
                {
                    "cutoff_X": cutoff,
                    "buffer_scale_multiplier": multiplier,
                    "even_buffer_h": buffer_width,
                    "target_N": 2 * cutoff - buffer_width,
                    "fourier_modulus_M": modulus,
                    "prime_window_cardinality_m": cardinality,
                    "ordered_reflection_count_R_A_h": reflection_count,
                    "dc_term_m_squared_over_M": fraction_payload(dc_term),
                    "signed_nonzero_frequency_remainder": fraction_payload(
                        signed_remainder
                    ),
                    "strict_negative_dc_threshold_passes": strict_threshold,
                    "integral_unit_slack_threshold_passes": integral_unit_threshold,
                    "restricted_prime_window_representation_exists": represented,
                    "equivalence_verified": verified,
                }
            )

    theorem = (
        "For every finite A and target h in the non-wrapping Fourier model "
        "of TICKET-239, write R_A(h)=DC_A+S_A(h), where "
        "DC_A=|A|^2/M and R_A(h) is a nonnegative integer. Then "
        "S_A(h)>-DC_A iff R_A(h)>=1; equivalently, for every fixed "
        "0<eta<=1, S_A(h)>=eta-DC_A iff R_A(h)>=1. Therefore a uniform "
        "signed-remainder slack above negative DC is exactly the pointwise "
        "representation claim, not a weaker intermediate lemma."
    )
    proof = (
        "Substitution gives S_A(h)+DC_A=R_A(h). The strict inequality is "
        "R_A(h)>0, which is equivalent to R_A(h)>=1 by integrality. For "
        "0<eta<=1, R_A(h)>=eta is equivalent to the same integer condition."
    )
    zero_rows = sum(
        not row["restricted_prime_window_representation_exists"] for row in rows
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "prime_window_signed_slack_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "signed_slack_integrality_equivalence_proved": True,
            "negative_dc_uniform_slack_is_not_weaker_than_positivity": True,
            "prime_window_row_count": len(rows),
            "zero_restricted_window_row_count": zero_rows,
            "pointwise_major_minor_error_bound_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The equivalence does not say that the required inequality is "
            "false. It says that naming it as the next lemma makes no logical "
            "progress unless the signed sum is decomposed into an independently "
            "positive arithmetic main term and explicit major/minor-arc errors. "
            "A zero in a restricted prime window is not a Goldbach counterexample."
        ),
        "failure_count": failures,
    }


def deterministic_is_prime(value: int) -> bool:
    if value < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if value % prime == 0:
            return value == prime
    exponent = value - 1
    power_of_two = 0
    while exponent % 2 == 0:
        exponent //= 2
        power_of_two += 1
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % value == 0:
            continue
        witness = pow(base, exponent, value)
        if witness in (1, value - 1):
            continue
        for _ in range(power_of_two - 1):
            witness = witness * witness % value
            if witness == value - 1:
                break
        else:
            return False
    return True


def crt_residue(residues: list[int], moduli: list[int]) -> tuple[int, int]:
    residue = 0
    modulus = 1
    for target, next_modulus in zip(residues, moduli, strict=True):
        step = ((target - residue) * pow(modulus, -1, next_modulus)) % next_modulus
        residue += modulus * step
        modulus *= next_modulus
        residue %= modulus
    return residue, modulus


def first_prime_in_progression(residue: int, modulus: int, lower: int) -> int:
    step = max(0, (lower - residue + modulus - 1) // modulus)
    while True:
        candidate = residue + step * modulus
        if deterministic_is_prime(candidate):
            return candidate
        step += 1


def empirical_prime_weighted_gram(
    flags: bytearray, upper: int, coordinate_primes: list[int]
) -> dict[str, Any]:
    primes = [
        prime
        for prime in range(upper // 2, upper - 1)
        if flags[prime]
    ]
    sample_count = len(primes)
    dimension = len(coordinate_primes)
    sums = [0] * dimension
    cross = [[0] * dimension for _ in range(dimension)]
    for prime in primes:
        values = [int((prime + 2) % q != 0) for q in coordinate_primes]
        for row in range(dimension):
            sums[row] += values[row]
            if values[row]:
                for column in range(row, dimension):
                    cross[row][column] += values[column]

    gram = [[0.0] * dimension for _ in range(dimension)]
    for row in range(dimension):
        mean_row = sums[row] / sample_count
        for column in range(row, dimension):
            mean_column = sums[column] / sample_count
            covariance = cross[row][column] / sample_count - mean_row * mean_column
            denominator = math.sqrt(
                mean_row
                * (1 - mean_row)
                * mean_column
                * (1 - mean_column)
            )
            gram[row][column] = gram[column][row] = covariance / denominator

    maximum_coherence = max(
        abs(gram[row][column])
        for row in range(dimension)
        for column in range(row + 1, dimension)
    )
    trace_square = sum(value * value for row in gram for value in row)
    effective_rank = dimension * dimension / trace_square
    coherence_lower_bound = dimension / (
        1 + (dimension - 1) * maximum_coherence * maximum_coherence
    )
    twin_count = sum(1 for prime in primes if flags[prime + 2])
    checks = {
        "gram_diagonal_is_one": all(
            abs(gram[index][index] - 1.0) < 1e-12
            for index in range(dimension)
        ),
        "effective_rank_obeys_coherence_bound": (
            effective_rank + 1e-12 >= coherence_lower_bound
        ),
        "effective_rank_does_not_exceed_dimension": (
            effective_rank <= dimension + 1e-12
        ),
    }
    return {
        "upper_scale_X": upper,
        "prime_sample_interval": [upper // 2, upper - 2],
        "prime_sample_count": sample_count,
        "coordinate_primes_Q": coordinate_primes,
        "coordinate_count_m": dimension,
        "maximum_absolute_pair_correlation_mu": maximum_coherence,
        "gram_effective_rank": effective_rank,
        "coherence_effective_rank_lower_bound": coherence_lower_bound,
        "finite_twin_pair_count_in_sample": twin_count,
        "checks": checks,
    }


def twin_one_sided_prime_crt_audit(flags: bytearray) -> dict[str, Any]:
    pattern_primes = [5, 7, 11]
    outside_prime = 43
    pattern_rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for bits in itertools.product((0, 1), repeat=len(pattern_primes)):
        residues = [1 if bit else (-2) % prime for bit, prime in zip(bits, pattern_primes)]
        residues.append((-2) % outside_prime)
        moduli = [*pattern_primes, outside_prime]
        residue, modulus = crt_residue(residues, moduli)
        first_prime = first_prime_in_progression(
            residue, modulus, 2 * modulus + outside_prime
        )
        observed_bits = tuple(
            int((first_prime + 2) % prime != 0) for prime in pattern_primes
        )
        successor_cofactor = (first_prime + 2) // outside_prime
        verified = (
            math.gcd(residue, modulus) == 1
            and observed_bits == bits
            and deterministic_is_prime(first_prime)
            and (first_prime + 2) % outside_prime == 0
            and successor_cofactor > 1
        )
        failures += int(not verified)
        transcript.update(
            f"{bits}:{residue}:{modulus}:{first_prime}:{successor_cofactor}\n".encode(
                "ascii"
            )
        )
        pattern_rows.append(
            {
                "local_admissibility_bits": list(bits),
                "crt_residue_r": residue,
                "crt_modulus_M": modulus,
                "gcd_r_M": math.gcd(residue, modulus),
                "first_prime_witness_p": first_prime,
                "forced_composite_successor_p_plus_2": first_prime + 2,
                "outside_prime_factor": outside_prime,
                "successor_cofactor": successor_cofactor,
                "certificate_verified": verified,
            }
        )

    coordinate_primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
    gram_rows = [
        empirical_prime_weighted_gram(flags, upper, coordinate_primes[:dimension])
        for upper, dimension in ((100_000, 4), (1_000_000, 8), (10_000_000, 12))
    ]
    failures += sum(
        not check
        for row in gram_rows
        for check in row["checks"].values()
    )
    theorem = (
        "Let Q be any finite set of primes greater than 3 and prescribe every "
        "binary pattern epsilon_q for the coordinates 1_(q does not divide "
        "p+2). There are infinitely many primes p realizing that complete "
        "pattern while p+2 is composite. Choose residues p=-2 mod q for a "
        "zero coordinate and p=1 mod q for a one coordinate, and also impose "
        "p=-2 mod ell for one new prime ell outside Q. CRT gives a reduced "
        "class modulo ell product(Q); Dirichlet's theorem supplies infinitely "
        "many primes in it, and every sufficiently large successor is divisible "
        "by ell. Thus even full finite-CRT support under one-sided prime "
        "weighting cannot certify twin-prime mass."
    )
    proof = (
        "All prescribed residues are nonzero modulo their primes, so the CRT "
        "class is coprime to the product modulus. Dirichlet's theorem applies. "
        "The selected residues realize the requested local bits exactly. The "
        "extra congruence makes p+2 a proper multiple of ell once p is large. "
        "The empirical Gram identity is independent: after centering and "
        "variance normalization its trace is m, and if every off-diagonal "
        "correlation has magnitude at most mu, then tr(G^2)<=m+m(m-1)mu^2, "
        "so r_eff=(tr G)^2/tr(G^2)>=m/(1+(m-1)mu^2)."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_all_pattern_crt_rows": pattern_rows,
        "actual_one_sided_prime_weighted_gram_rows": gram_rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "all_finite_crt_patterns_have_infinite_prime_composite_successors": True,
            "one_sided_prime_weighted_finite_crt_sufficiency_refuted": True,
            "empirical_gram_coherence_bound_proved": True,
            "largest_empirical_scale": gram_rows[-1]["upper_scale_X"],
            "largest_empirical_effective_rank": gram_rows[-1]["gram_effective_rank"],
            "two_sided_parity_breaking_main_term_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Dirichlet's theorem proves infinite prime/composite successors in "
            "each fixed local pattern, not the absence of twins. The empirical "
            "rows are finite observations and their twin counts cannot establish "
            "an infinite lower bound. A genuinely two-sided prime correlation "
            "with parity-breaking error control remains missing."
        ),
        "failure_count": failures,
    }


def proof_dag(
    problem_code: str,
    input_name: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{problem_code}-T239", "label": input_name, "status": "closed_input"},
            {
                "id": f"{problem_code}-N240",
                "label": rejected_name,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{problem_code}-T240",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-OPEN240",
                "label": open_name,
                "status": "highest_risk_open",
            },
        ],
        "edges": [
            [f"{problem_code}-T239", f"{problem_code}-N240"],
            [f"{problem_code}-T239", f"{problem_code}-T240"],
            [f"{problem_code}-N240", f"{problem_code}-T240"],
            [f"{problem_code}-T240", f"{problem_code}-OPEN240"],
        ],
    }


def section(
    problem_id: str,
    problem_code: str,
    theorem_name: str,
    computation: dict[str, Any],
    discarded: str,
    retained: str,
    next_lemma: str,
    input_name: str,
    rejected_name: str,
    logical_limit: str,
    claim_boundary: str,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{problem_code}-TICKET-240",
        "theorem_name": theorem_name,
        "declared_proposition": computation["theorem"],
        "mathematical_argument": computation["proof"],
        "reproducible_computation": computation,
        "logical_limit": logical_limit,
        "route_decision": {
            "discard": discarded,
            "retain": retained,
            "next_single_lemma": next_lemma,
        },
        "proof_dag": proof_dag(
            problem_code,
            input_name,
            rejected_name,
            theorem_name,
            next_lemma,
        ),
        "claim_boundary": claim_boundary,
    }


def build_audit() -> dict[str, Any]:
    flags = prime_flags_up_to(PRIME_LIMIT)
    riemann = riemann_cotlar_audit()
    collatz = collatz_wieferich_audit(flags)
    goldbach = goldbach_signed_slack_audit(flags)
    twin = twin_one_sided_prime_crt_audit(flags)

    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "CotlarNormSummabilityNoGoForUniformGramLowerBounds",
            riemann,
            "absolute Cotlar-Stein overlap summability as the necessary or uniquely sign-sensitive RH bridge",
            "a signed arithmetic block symbol or direct operator lower bound after common-mode removal",
            "ArithmeticWeilSignedBlockOperatorSymbolHasUniformPositiveLowerBoundAfterCommonModeRemoval",
            "PowerDecaySchurThresholdAndNonsummablePositiveGramNoGo",
            "CotlarNormSummabilityCapturesSignedWeilCancellation",
            "No signed lower bound is proved for the actual Guinand-Weil operator.",
            "No RH proof, disproof, or zeta-zero exclusion; one exact route-correction theorem and seven model rows only.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "RunBlockDefectFermatQuotientReductionAndTwentyMillionAudit",
            collatz,
            "bounded absence of positive lifting defects as an all-prime proof",
            "the exact rational Wieferich-depth comparison, with finite scans labeled only as bounded evidence",
            "RationalWieferichDepthDominationFor32Over27Versus2Over3AtEveryOddPrime",
            "LocalLiftingDefectDichotomyAndPaletteCriterion",
            "FiniteLiftingDefectScanProvesGlobalNonpositivity",
            "The all-prime rational Wieferich-depth domination, general necklace exclusion, and aperiodic descent remain open.",
            "No Collatz proof, divergent orbit, or nontrivial-cycle exclusion; one exact depth reduction and a finite scan through twenty million only.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "SignedFourierSlackIntegralityEquivalenceAndIntermediateTargetNoGo",
            goldbach,
            "negative-DC signed slack as a weaker intermediate target than pointwise Goldbach positivity",
            "a targetwise positive arithmetic main term with separately bounded major- and minor-arc errors",
            "BinaryPrimeMajorArcMainTermMinusAllExplicitErrorsIsAtLeastOneForEverySufficientlyLargeEvenTarget",
            "MesoscopicReflectionFourierIdentityAndL2NoGo",
            "UniformSignedRemainderSlackIsAWeakerGoldbachMilestone",
            "No target-uniform binary-prime major/minor error estimate is proved.",
            "No Goldbach proof or counterexample; one exact integrality equivalence and fifteen restricted-window rows only.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "OneSidedPrimeWeightedCRTFullSupportAndCompositeSuccessorNoGo",
            twin,
            "one-sided prime weighting plus any finite CRT feature hierarchy as sufficient for twin-prime mass",
            "a genuinely two-sided prime correlation with parity-breaking error control on growing CRT support",
            "ParityBreakingTwoSidedLambdaLambdaMainTermDominatesGrowingCRTErrorOnCofinalDyadicBlocks",
            "UniformCRTGramIdentityAndCompositeProgressionNoGo",
            "OneSidedPrimeWeightedCRTOrthogonalityImpliesTwinMass",
            "No two-sided Lambda(n)Lambda(n+2) lower bound is proved on any cofinal family of blocks.",
            "No twin-prime proof or counterexample; one exact Dirichlet-CRT no-go theorem, eight pattern certificates, and three finite empirical Gram rows only.",
        ),
    }

    total_failures = sum(
        track["reproducible_computation"]["failure_count"]
        for track in sections.values()
    )
    machine_audit = {
        "exact_theorem_count": 4,
        "route_correction_count": 4,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "conjecture_resolution_count": 0,
        "bounded_prime_scan_limit": PRIME_LIMIT,
        "total_failure_count": total_failures,
    }
    audit: dict[str, Any] = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureRouteCorrectionWieferichPrimeCRTAudit",
            "summary": (
                "TICKET-240 corrects three overstrong intermediate routes and "
                "reduces the Collatz run-block defect to an exact rational "
                "Wieferich-depth comparison. All four parent conjectures remain open."
            ),
            **sections,
            "research_baselines": {
                "riemann": "https://www.claymath.org/millennium/riemann-hypothesis/",
                "collatz": "https://arxiv.org/abs/1909.03562",
                "fermat_quotient": "https://arxiv.org/abs/1110.3113",
                "goldbach": "https://arxiv.org/abs/1501.05438",
                "twin_prime": "https://arxiv.org/abs/1311.4600",
            },
            "machine_audit": machine_audit,
        },
        "attempts": [],
    }
    for track in sections.values():
        route = track["route_decision"]
        audit["attempts"].append(
            {
                "problem_id": track["problem_id"],
                "ticket_id": track["ticket_id"],
                "declared_proposition": track["declared_proposition"],
                "new_result": track["theorem_name"],
                "status": STATUS,
                "bounded_result": {
                    "audit_ref": f"#/{AUDIT_KEY}/{track['problem_id']}",
                    "failure_count": track["reproducible_computation"][
                        "failure_count"
                    ],
                },
                "discarded_route": route["discard"],
                "remaining_gap": track["logical_limit"],
                "candidate_theorem": route["next_single_lemma"],
            }
        )
    return audit


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(
        ROOT
        / "data/open-problem/ticket240-route-corrections-wieferich-prime-crt.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-240-cotlar-norm-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-240-wieferich-depth.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-240-signed-slack-equivalence.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-240-one-sided-prime-crt.json",
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


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    machine = audit[AUDIT_KEY]["machine_audit"]
    print(json.dumps(machine, indent=2))
    return 0 if machine["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
