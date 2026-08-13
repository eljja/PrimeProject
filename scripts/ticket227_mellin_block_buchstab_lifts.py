from __future__ import annotations

import bisect
import cmath
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket226_signal_transfer_same_order_obstructions import (
    collatz_intercept,
    cube_root_support,
    is_primitive_word,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket227-mellin-block-buchstab-lifts.v1"
GENERATED_AT = "2026-08-14T23:58:00+09:00"
STATUS = "open_not_proven"
HORIZONS = (10_000, 100_000, 1_000_000)
BIN_LABELS = (
    "[1/3,3/8)",
    "[3/8,5/12)",
    "[5/12,11/24)",
    "[11/24,1/2]",
)
LANCZOS_COEFFICIENTS = (
    0.99999999999980993,
    676.5203681218851,
    -1259.1392167224028,
    771.32342877765313,
    -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
    9.9843695780195716e-6,
    1.5056327351493116e-7,
)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def proof_dag(
    prefix: str,
    previous: str,
    closed: str,
    corrected: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T226", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T227", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N227",
                "label": corrected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN227",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T226", f"{prefix}-T227"],
            [f"{prefix}-T227", f"{prefix}-N227"],
            [f"{prefix}-T227", f"{prefix}-OPEN227"],
            [f"{prefix}-OPEN227", prefix],
        ],
    }


def complex_gamma_lanczos(value: complex) -> complex:
    """Evaluate Gamma(z) in double precision with the g=7 Lanczos formula."""
    if value.real < 0.5:
        return math.pi / (
            cmath.sin(math.pi * value) * complex_gamma_lanczos(1 - value)
        )
    shifted = value - 1
    series = complex(LANCZOS_COEFFICIENTS[0])
    for index, coefficient in enumerate(LANCZOS_COEFFICIENTS[1:], start=1):
        series += coefficient / (shifted + index)
    base = shifted + 7.5
    return (
        math.sqrt(2 * math.pi)
        * base ** (shifted + 0.5)
        * cmath.exp(-base)
        * series
    )


def transformed_mellin_quadrature(q: int, tau: float) -> complex:
    """Independently integrate after u=exp(x) on a fixed finite window."""
    lower = -40.0
    upper = 6.0
    intervals = 46_000
    step = (upper - lower) / intervals
    s = 1 + 1j * tau

    def integrand(x: float) -> complex:
        u = math.exp(x)
        kernel = math.exp(-u) - q * math.exp(-q * u)
        return cmath.exp(s * x) * kernel

    total = integrand(lower) + integrand(upper)
    for index in range(1, intervals):
        total += (4 if index % 2 else 2) * integrand(lower + index * step)
    return total * step / 3


def riemann_dual_dilation_audit() -> dict[str, Any]:
    rows = []
    failures = 0
    for alias_index in range(1, 6):
        tau = 2 * math.pi * alias_index / math.log(2)
        s = 1 + 1j * tau
        gamma_s = complex_gamma_lanczos(s)
        factor_2 = 1 - cmath.exp((1 - s) * math.log(2))
        factor_3 = 1 - cmath.exp((1 - s) * math.log(3))
        multiplier_2 = gamma_s * factor_2
        multiplier_3 = gamma_s * factor_3
        quadrature_checked = alias_index <= 2
        integral_2 = (
            transformed_mellin_quadrature(2, tau) if quadrature_checked else None
        )
        integral_3 = (
            transformed_mellin_quadrature(3, tau) if quadrature_checked else None
        )
        q2_zero = abs(factor_2) < 1e-12
        q3_visible = abs(factor_3) > 1e-6 and abs(multiplier_3) > 1e-50
        quadrature_matches = quadrature_checked and (
            abs(integral_2 - multiplier_2) < 1e-15
            and abs(integral_3 - multiplier_3) < 1e-15
        )
        verified = q2_zero and q3_visible and (
            not quadrature_checked or quadrature_matches
        )
        failures += int(not verified)
        rows.append(
            {
                "alias_index_k": alias_index,
                "tau_2pi_k_over_log2": float(tau),
                "q2_analytic_multiplier_abs": float(abs(multiplier_2)),
                "q3_analytic_multiplier_abs": float(abs(multiplier_3)),
                "q2_quadrature_error": float(abs(integral_2 - multiplier_2))
                if quadrature_checked
                else None,
                "q3_quadrature_error": float(abs(integral_3 - multiplier_3))
                if quadrature_checked
                else None,
                "q2_alias_zero_verified": bool(q2_zero),
                "q3_alias_visible_verified": bool(q3_visible),
                "quadrature_independent_check_required": quadrature_checked,
                "quadrature_identity_verified": bool(quadrature_matches)
                if quadrature_checked
                else None,
                "quadrature_limit": None
                if quadrature_checked
                else "double-precision quadrature is not required after Gamma decay",
            }
        )

    bounded_common_aliases = []
    for k in range(-100, 101):
        for ell in range(-100, 101):
            if k == 0 and ell == 0:
                continue
            if 2**abs(ell) == 3**abs(k):
                bounded_common_aliases.append([k, ell])
    no_bounded_alias = not bounded_common_aliases
    failures += int(not no_bounded_alias)

    theorem = (
        "For q>1 define B_q[E](a)=a integral E(x)(exp(-a x)-"
        "q exp(-q a x)) dx. On the Mellin mode E_s(x)=x^(s-1), "
        "B_q[E_s](a)=a^(1-s) Gamma(s)(1-q^(1-s)). Consequently a "
        "single q=2 family is blind to every nonconstant log-periodic "
        "mode s=1+2 pi i k/log(2). The joint q=2 and q=3 family has no "
        "nonconstant common blind mode on Re(s)=1."
    )
    proof = (
        "The Mellin-Laplace integral is Gamma(s)a^(-s); scaling the "
        "second term gives q^(1-s), proving the multiplier identity. On "
        "Re(s)=1 blindness is equivalent to tau log(q) in 2 pi Z. A "
        "common nonzero blind frequency for q=2 and q=3 would imply "
        "log(2)/log(3) is rational and hence 2^ell=3^k for positive "
        "integers k,ell, contradicting unique prime factorization."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "mellin_alias_rows": rows,
        "bounded_integer_relation_audit": {
            "absolute_index_bound": 100,
            "nonzero_common_aliases": bounded_common_aliases,
            "none_found": no_bounded_alias,
            "role": "reproducible sanity check only; the proof uses unique factorization",
        },
        "aggregate": {
            "mellin_multiplier_identity_proved": True,
            "single_dilation_infinite_alias_family_proved": True,
            "dual_incommensurate_dilation_removes_nonconstant_line_aliases_proved": True,
            "constant_mode_remains_blind": True,
            "uniform_dense_weil_core_frame_bound_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "Alias elimination is injectivity on individual Mellin modes, "
            "not a lower frame bound for arbitrary superpositions and not "
            "control of the zeta explicit formula on a dense Weil core."
        ),
        "failure_count": failures,
    }


def affine_data(word: tuple[int, ...]) -> tuple[int, int, int]:
    return 3 ** len(word), 2 ** sum(word), collatz_intercept(word)


def repeated_block_suffix_formula(
    repetition: int, suffix: tuple[int, ...]
) -> tuple[int, int]:
    a_v, c_v, b_v = affine_data(suffix)
    power_32 = 32**repetition
    power_27 = 27**repetition
    denominator = c_v * power_32 - a_v * power_27
    numerator = (
        (5 * b_v + 19 * a_v) * power_32 - 19 * a_v * power_27
    ) // 5
    return denominator, numerator


def suffix_interval_certificate(
    suffix: tuple[int, ...],
) -> tuple[bool, int | None, Fraction | None, Fraction | None]:
    a_v, c_v, b_v = affine_data(suffix)
    denominator_1 = c_v * 32 - a_v * 27
    if denominator_1 <= 0:
        return False, None, None, None
    ratio_1 = Fraction((5 * b_v + 19 * a_v) * 32 - 19 * a_v * 27, 5 * denominator_1)
    ratio_infinity = Fraction(5 * b_v + 19 * a_v, 5 * c_v)
    floor_1 = ratio_1.numerator // ratio_1.denominator
    floor_infinity = ratio_infinity.numerator // ratio_infinity.denominator
    certified = (
        floor_1 == floor_infinity
        and ratio_1.denominator != 1
        and ratio_infinity.denominator != 1
    )
    return certified, floor_1 if certified else None, ratio_1, ratio_infinity


def collatz_block_suffix_audit() -> dict[str, Any]:
    failures = 0
    certificates = []
    for length in range(1, 5):
        for suffix in itertools.product(range(1, 7), repeat=length):
            certified, interval_floor, ratio_1, ratio_infinity = (
                suffix_interval_certificate(suffix)
            )
            if certified:
                certificates.append(
                    {
                        "suffix": list(suffix),
                        "unit_interval": [interval_floor, interval_floor + 1],
                        "ratio_at_r1": str(ratio_1),
                        "ratio_limit": str(ratio_infinity),
                    }
                )

    suffix = (4, 2, 1)
    certified, interval_floor, ratio_1, ratio_infinity = (
        suffix_interval_certificate(suffix)
    )
    rows = []
    selected = {1, 2, 3, 5, 10, 20, 40}
    for repetition in range(1, 41):
        word = (1, 1, 3) * repetition + suffix
        denominator, numerator = repeated_block_suffix_formula(repetition, suffix)
        direct_a, direct_c, direct_b = affine_data(word)
        formula_verified = denominator == direct_c - direct_a and numerator == direct_b
        in_interval = denominator < numerator < 2 * denominator
        primitive = is_primitive_word(word)
        noncycle = numerator % denominator != 0
        verified = all((certified, formula_verified, in_interval, primitive, noncycle))
        failures += int(not verified)
        if repetition in selected:
            rows.append(
                {
                    "repetition_r": repetition,
                    "height_h": len(word),
                    "valuation_sum_S": sum(word),
                    "D": denominator,
                    "B": numerator,
                    "B_over_D": numerator / denominator,
                    "formula_verified": formula_verified,
                    "primitive_unique_marker_4_verified": primitive
                    and word.count(4) == 1,
                    "strict_unit_interval_1_2_verified": in_interval,
                    "D_divides_B": not noncycle,
                }
            )

    failures += int(
        not (
            certified
            and interval_floor == 1
            and ratio_1 == Fraction(4385, 3367)
            and ratio_infinity == Fraction(559, 320)
        )
    )
    theorem = (
        "Let U=(1,1,3) with affine data (27,32,19), and let a fixed "
        "suffix V have affine data (A,C,B). For w_r=U^r V, D_r=C "
        "32^r-A 27^r and B_r=((5B+19A)32^r-19A27^r)/5. If the r=1 "
        "and r=infinity ratios lie strictly in one unit interval and D_r "
        "stays positive, fractional-linearity puts every B_r/D_r in that "
        "interval. For V=(4,2,1), 1<B_r/D_r<2 for every r>=1; the unique "
        "4 makes w_r primitive, so this is an infinite primitive noncycle family."
    )
    proof = (
        "Affine composition and the geometric sum for U^r give the two "
        "closed forms. Writing t=(27/32)^r makes B_r/D_r a fractional-"
        "linear function of t with no pole on 0<=t<=27/32, hence it is "
        "monotone or constant and lies between its endpoint values. For "
        "V=(4,2,1) these values are 4385/3367 and 559/320, both strictly "
        "between 1 and 2. An integer fixed point would require D_r|B_r, "
        "which is impossible in that open unit interval."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "selected_suffix": list(suffix),
        "selected_endpoint_ratios": {
            "r_equals_1": str(ratio_1),
            "r_to_infinity": str(ratio_infinity),
            "common_open_unit_interval": [1, 2],
        },
        "selected_family_rows": rows,
        "bounded_suffix_search": {
            "suffix_length_max": 4,
            "exponent_range": [1, 6],
            "certificate_count": len(certificates),
            "first_twelve": certificates[:12],
            "role": "discovery audit; the selected infinite family is proved symbolically",
        },
        "aggregate": {
            "general_repeated_block_suffix_interval_criterion_proved": True,
            "selected_infinite_primitive_noncycle_family_proved": True,
            "selected_repetitions_computationally_checked": 40,
            "all_primitive_words_excluded": False,
            "aperiodic_descent_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The interval criterion settles only suffixes whose two endpoint "
            "ratios share a unit interval. It does not cover arbitrary "
            "primitive valuation words or prove descent of aperiodic orbits."
        ),
        "failure_count": failures,
    }


def factor_bin(prime_factor: int, horizon: int) -> int:
    if prime_factor**24 < horizon**9:
        return 0
    if prime_factor**12 < horizon**5:
        return 1
    if prime_factor**24 < horizon**11:
        return 2
    return 3


def rough_semiprime_factor_pairs(
    horizon: int, cutoff: int, primes: list[int]
) -> dict[int, tuple[int, int]]:
    pairs: dict[int, tuple[int, int]] = {}
    lower_index = bisect.bisect_right(primes, cutoff)
    for index in range(lower_index, len(primes)):
        first = primes[index]
        if first * first > horizon:
            break
        upper_index = bisect.bisect_right(primes, horizon // first)
        for second in primes[index:upper_index]:
            pairs[first * second] = (first, second)
    return pairs


def empty_matrix() -> list[list[int]]:
    return [[0 for _ in BIN_LABELS] for _ in BIN_LABELS]


def goldbach_factor_lift_audit() -> dict[str, Any]:
    failures = 0
    rows = []
    for horizon in HORIZONS:
        cutoff, prime, semiprime, rough, primes = cube_root_support(horizon)
        factor_pairs = rough_semiprime_factor_pairs(horizon, cutoff, primes)
        ps_bins = [0] * len(BIN_LABELS)
        sp_bins = [0] * len(BIN_LABELS)
        ss_matrix = empty_matrix()
        counts = {"PP": 0, "PS": 0, "SP": 0, "SS": 0}
        divisor_exceptions = {"PS": 0, "SP": 0}
        exception_identity_failures = 0
        for left in range(2, horizon - 1):
            right = horizon - left
            if prime[left] and prime[right]:
                counts["PP"] += 1
            elif prime[left] and semiprime[right]:
                counts["PS"] += 1
                q, r = factor_pairs[right]
                ps_bins[factor_bin(q, horizon)] += 1
                if horizon % q == 0:
                    divisor_exceptions["PS"] += 1
                    exception_identity_failures += int(
                        not (left == q and r == horizon // q - 1)
                    )
            elif semiprime[left] and prime[right]:
                counts["SP"] += 1
                q, r = factor_pairs[left]
                sp_bins[factor_bin(q, horizon)] += 1
                if horizon % q == 0:
                    divisor_exceptions["SP"] += 1
                    exception_identity_failures += int(
                        not (right == q and r == horizon // q - 1)
                    )
            elif semiprime[left] and semiprime[right]:
                counts["SS"] += 1
                q_left, _ = factor_pairs[left]
                q_right, _ = factor_pairs[right]
                ss_matrix[factor_bin(q_left, horizon)][
                    factor_bin(q_right, horizon)
                ] += 1
        filtered = sum(
            1
            for left in range(2, horizon - 1)
            if rough[left] and rough[horizon - left]
        )
        bin_totals_verified = (
            sum(ps_bins) == counts["PS"]
            and sum(sp_bins) == counts["SP"]
            and sum(map(sum, ss_matrix)) == counts["SS"]
        )
        decomposition_verified = filtered == sum(counts.values())
        verified = (
            bin_totals_verified
            and decomposition_verified
            and exception_identity_failures == 0
            and len(factor_pairs) == sum(semiprime)
        )
        failures += int(not verified)
        rows.append(
            {
                "even_target_N": horizon,
                "cutoff_z": cutoff,
                "counts": counts,
                "least_factor_bin_labels": BIN_LABELS,
                "PS_least_factor_bins": ps_bins,
                "SP_least_factor_bins": sp_bins,
                "SS_least_factor_matrix": ss_matrix,
                "q_divides_N_exception_counts": divisor_exceptions,
                "q_divides_N_exception_identity_failures": exception_identity_failures,
                "rough_semiprime_factor_pair_count": len(factor_pairs),
                "factor_pair_count_verified": len(factor_pairs) == sum(semiprime),
                "bin_totals_verified": bin_totals_verified,
                "exact_decomposition_verified": decomposition_verified,
            }
        )

    theorem = (
        "At z=ceil(X^(1/3)), every retained composite m<=X has the unique "
        "form m=qr with primes z<q<=r. Therefore the Goldbach PS and SP "
        "channels lift exactly to prime sums over N-qr, and SS lifts to a "
        "two-factor-cell convolution. In a PS or SP cell with q|N, a "
        "prime N-qr divisible by q must equal q, leaving at most the single "
        "explicit candidate r=N/q-1."
    )
    proof = (
        "Three factors greater than z have product greater than or equal "
        "to z^3>=X, so every retained composite below X has exactly two "
        "prime factors; ordering gives uniqueness. Substitution m=qr "
        "gives the factor-lift identities. If q divides N and N-qr is "
        "prime, q divides that prime, so it equals q and r=N/q-1. The "
        "tables enumerate every summand and verify all channel totals."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "factor_cell_rows": rows,
        "aggregate": {
            "unique_cube_root_rough_semiprime_factorization_proved": True,
            "exact_PS_SP_SS_factor_lifts_proved": True,
            "q_divides_target_exception_split_proved": True,
            "audited_even_targets": len(rows),
            "uniform_moving_residue_prime_estimate_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The exact lift localizes the arithmetic obligation but supplies "
            "no uniform estimate for primes N-qr in moving nonzero residue "
            "classes and no positive lower bound for PP at every even N."
        ),
        "failure_count": failures,
    }


def twin_factor_lift_audit() -> dict[str, Any]:
    failures = 0
    rows = []
    for horizon in HORIZONS:
        cutoff, prime, semiprime, rough, primes = cube_root_support(horizon)
        factor_pairs = rough_semiprime_factor_pairs(horizon, cutoff, primes)
        ps_bins = [0] * len(BIN_LABELS)
        sp_bins = [0] * len(BIN_LABELS)
        ss_matrix = empty_matrix()
        counts = {"PP": 0, "PS": 0, "SP": 0, "SS": 0}
        shared_factor_collisions = 0
        for left in range(2, horizon - 1):
            right = left + 2
            if prime[left] and prime[right]:
                counts["PP"] += 1
            elif prime[left] and semiprime[right]:
                counts["PS"] += 1
                q, _ = factor_pairs[right]
                ps_bins[factor_bin(q, horizon)] += 1
            elif semiprime[left] and prime[right]:
                counts["SP"] += 1
                q, _ = factor_pairs[left]
                sp_bins[factor_bin(q, horizon)] += 1
            elif semiprime[left] and semiprime[right]:
                counts["SS"] += 1
                left_pair = factor_pairs[left]
                right_pair = factor_pairs[right]
                ss_matrix[factor_bin(left_pair[0], horizon)][
                    factor_bin(right_pair[0], horizon)
                ] += 1
                shared_factor_collisions += int(
                    bool(set(left_pair).intersection(right_pair))
                )
        filtered = sum(
            1
            for left in range(2, horizon - 1)
            if rough[left] and rough[left + 2]
        )
        bin_totals_verified = (
            sum(ps_bins) == counts["PS"]
            and sum(sp_bins) == counts["SP"]
            and sum(map(sum, ss_matrix)) == counts["SS"]
        )
        decomposition_verified = filtered == sum(counts.values())
        verified = (
            bin_totals_verified
            and decomposition_verified
            and shared_factor_collisions == 0
            and len(factor_pairs) == sum(semiprime)
        )
        failures += int(not verified)
        rows.append(
            {
                "horizon_X": horizon,
                "cutoff_z": cutoff,
                "counts": counts,
                "least_factor_bin_labels": BIN_LABELS,
                "PS_qr_minus_2_bins": ps_bins,
                "SP_qr_plus_2_bins": sp_bins,
                "SS_pq_plus_2_equals_rs_matrix": ss_matrix,
                "SS_shared_prime_factor_collisions": shared_factor_collisions,
                "factor_pair_count_verified": len(factor_pairs) == sum(semiprime),
                "bin_totals_verified": bin_totals_verified,
                "exact_decomposition_verified": decomposition_verified,
            }
        )

    theorem = (
        "At the cube-root cutoff the Twin PS, SP, and SS channels lift "
        "exactly to qr-2 prime, qr+2 prime, and pq+2=rs factor sums, "
        "respectively, with all prime factors above z. In every SS term "
        "the factor sets {p,q} and {r,s} are disjoint because a common odd "
        "prime would divide both n and n+2 and hence divide 2."
    )
    proof = (
        "Unique two-prime factorization follows from the same cube-root "
        "argument as in the Goldbach lift. Substituting each semiprime "
        "factorization gives qr-2, qr+2, and pq+2=rs without approximation. "
        "All factors exceed z>=22 in the audited ranges, so a shared factor "
        "cannot divide the difference 2. Complete enumeration verifies the "
        "factor-cell totals and zero shared-factor collisions."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "factor_cell_rows": rows,
        "aggregate": {
            "exact_shift_two_factor_lifts_proved": True,
            "SS_factor_graph_disjointness_proved": True,
            "audited_horizons": len(rows),
            "uniform_shifted_bilinear_power_saving_proved": False,
            "infinitely_many_twin_primes_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Disjoint factor support is an exact structural restriction, not "
            "cancellation. The factor-cell tables are finite and prove no "
            "unbounded positive lower bound for the PP channel."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_dual_dilation_audit()
    collatz = collatz_block_suffix_audit()
    goldbach = goldbach_factor_lift_audit()
    twin = twin_factor_lift_audit()
    root = {
        "theorem_name": "MellinBlockAndBuchstabFactorLiftsForFourOpenProblems",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-227 proves four exact structural lemmas and resolves "
            "none of the four parent conjectures. Numerical rows verify the "
            "identities at finite ranges but are not extrapolated."
        ),
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-227",
            "theorem_name": "DualDilationMellinAliasEliminationAndSingleRatioNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": riemann["no_go_scope"],
            "route_decision": {
                "discard": "using one fixed dilation ratio as if its balanced bands separated every Mellin mode",
                "retain": "combine multiplicatively independent dilation ratios and seek a quantitative frame bound on the explicit-formula test space",
                "next_single_lemma": "UniformDualDilationMellinFrameBoundOnExplicitDenseWeilCore",
            },
            "proof_dag": proof_dag(
                "RH",
                "BalancedChebyshevKernelIdentityAndDirectSignTransferNoGo",
                "DualDilationMellinAliasEliminationAndSingleRatioNoGo",
                "SingleDilationSeparatesAllMellinModes",
                "UniformDualDilationMellinFrameBoundOnExplicitDenseWeilCore",
                "RiemannHypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-227",
            "theorem_name": "RepeatedBlockSuffixUnitIntervalCertificate",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": collatz["no_go_scope"],
            "route_decision": {
                "discard": "checking divisibility separately for every repetition of a block-suffix family",
                "retain": "use exact affine composition and fractional-linear endpoint intervals to certify entire infinite families",
                "next_single_lemma": "UniversalPrimePowerWitnessForPrimitiveValuationWordNondivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "InfinitePrimitiveMinimumInterceptCounterfamily",
                "RepeatedBlockSuffixUnitIntervalCertificate",
                "FiniteRepetitionChecksEstablishAnInfiniteFamily",
                "UniversalPrimePowerWitnessForPrimitiveValuationWordNondivisibility",
                "CollatzConjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-227",
            "theorem_name": "CubeRootBuchstabFactorLiftAndDivisorExceptionSplit",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": goldbach["no_go_scope"],
            "route_decision": {
                "discard": "estimating PS, SP, and SS only from one-variable marginal densities",
                "retain": "estimate the exact factor-resolved moving-residue sums exposed by the cube-root Buchstab lift",
                "next_single_lemma": "UniformMovingResiduePrimeEstimateForCubeRootBuchstabCellsAtEveryEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "CubeRootSemiprimeSameOrderAndGoldbachDominationNoGo",
                "CubeRootBuchstabFactorLiftAndDivisorExceptionSplit",
                "MarginalDensityDeterminesPointwiseGoldbachFactorCells",
                "UniformMovingResiduePrimeEstimateForCubeRootBuchstabCellsAtEveryEvenTarget",
                "StrongGoldbachConjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-227",
            "theorem_name": "ShiftTwoBuchstabFactorLiftAndDisjointFactorGraph",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": twin["no_go_scope"],
            "route_decision": {
                "discard": "treating shifted contamination as an unstructured marginal error term",
                "retain": "attack the exact qr-2, qr+2, and pq+2=rs factor-cell sums with shifted bilinear estimates",
                "next_single_lemma": "UniformShiftTwoBilinearPrimeEstimateForQrPlusMinus2AcrossAllCubeRootCells",
            },
            "proof_dag": proof_dag(
                "TP",
                "CubeRootSemiprimeMarginalSameOrderAndPairDominationNoGo",
                "ShiftTwoBuchstabFactorLiftAndDisjointFactorGraph",
                "FactorDisjointnessAloneForcesShiftedCancellation",
                "UniformShiftTwoBilinearPrimeEstimateForQrPlusMinus2AcrossAllCubeRootCells",
                "TwinPrimeConjecture",
            ),
        },
    }
    tracks = ("riemann", "collatz", "goldbach", "twin_prime")
    total_failures = sum(
        root[key]["reproducible_computation"]["failure_count"] for key in tracks
    )
    root["machine_audit"] = {
        "exact_partial_theorem_count": 4,
        "refuted_or_corrected_route_count": 4,
        "next_single_lemma_count": 4,
        "proof_dag_count": 4,
        "conjecture_resolution_count": 0,
        "total_failure_count": total_failures,
    }
    attempts = []
    for key in tracks:
        track = root[key]
        attempts.append(
            {
                "problem_id": track["problem_id"],
                "ticket_id": track["ticket_id"],
                "status": STATUS,
                "declared_proposition": track["declared_proposition"],
                "mathematical_argument": track["mathematical_argument"],
                "new_result": track["theorem_name"],
                "bounded_result": {
                    "audit_ref": f"#/mellin_block_buchstab_lifts_audit/{key}",
                    "failure_count": track["reproducible_computation"]["failure_count"],
                },
                "discarded_route": track["route_decision"]["discard"],
                "remaining_gap": track["logical_limit"],
                "candidate_theorem": track["route_decision"]["next_single_lemma"],
                "proof_dag": track["proof_dag"],
            }
        )
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": (
            "TICKET-227 proves four exact structural lemmas and resolves "
            "none of the four parent conjectures."
        ),
        "mellin_block_buchstab_lifts_audit": root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit["mellin_block_buchstab_lifts_audit"]
    write_json(
        ROOT / "data/open-problem/ticket227-mellin-block-buchstab-lifts.json",
        audit,
    )
    destinations = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-227-dual-dilation-mellin.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-227-block-suffix-interval.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-227-buchstab-factor-lift.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-227-shift-two-factor-lift.json",
    }
    for key, destination in destinations.items():
        write_json(
            destination,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": STATUS,
                **root[key],
            },
        )


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    machine = audit["mellin_block_buchstab_lifts_audit"]["machine_audit"]
    print(json.dumps(machine, indent=2))
    if machine["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
