from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, ROUND_FLOOR, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket214_cofinal_sevenone_exponential_cardinal import (
    goldbach_counts,
    prime_sieve,
)
from ticket217_relative_threshold_convergent_moment_tail import (
    convergents,
    interval_continued_fraction,
    log_rational_interval,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket218-adaptive-radius-spike-residual-surplus.v1"
GENERATED_AT = "2026-08-13T05:30:00+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def proof_dag(
    prefix: str,
    previous: str,
    previous_open: str,
    closed: str,
    rejected: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T217", "label": previous, "status": "closed"},
            {
                "id": f"{prefix}-OPEN217",
                "label": previous_open,
                "status": "refined_by_ticket218",
            },
            {"id": f"{prefix}-T218", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N218",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN218",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T217", f"{prefix}-OPEN217"],
            [f"{prefix}-OPEN217", f"{prefix}-T218"],
            [f"{prefix}-T218", f"{prefix}-N218"],
            [f"{prefix}-T218", f"{prefix}-OPEN218"],
            [f"{prefix}-OPEN218", prefix],
        ],
    }


def decimal_string(value: Decimal, digits: int = 24) -> str:
    return format(value, f".{digits}E")


def riemann_scale_adaptive_audit() -> dict[str, Any]:
    getcontext().prec = 90
    heights = (100, 10_000, 1_000_000, 1_000_000_000)
    taus = (Decimal(1), Decimal(2))
    rows = []
    failures = 0
    for tau in taus:
        expected = (-tau).exp()
        for height in heights:
            radius = (-tau / Decimal(height)).exp()
            signal = (Decimal(height) * radius.ln()).exp()
            error = abs(signal - expected)
            failures += int(error > Decimal("1e-75"))
            rows.append(
                {
                    "H": height,
                    "tau": str(tau),
                    "radius_exp_minus_tau_over_H": decimal_string(radius),
                    "first_atom_signal_r_H_pow_H": decimal_string(signal),
                    "exact_target_exp_minus_tau": decimal_string(expected),
                    "absolute_decimal_error": decimal_string(error),
                }
            )

    phase_rows = []
    for height in heights:
        h = Decimal(height)
        log_h = h.ln()
        schedules = (
            ("bounded_H_beta", Decimal(2), (-Decimal(2)).exp()),
            ("logarithmic_H_beta", log_h, (-log_h).exp()),
            ("square_root_H_beta", log_h.sqrt(), (-log_h.sqrt()).exp()),
        )
        for name, h_beta, signal in schedules:
            phase_rows.append(
                {
                    "H": height,
                    "schedule": name,
                    "H_times_minus_log_radius": decimal_string(h_beta),
                    "first_atom_signal": decimal_string(signal),
                }
            )

    theorem = (
        "Let C be the nonnegative integer-valued off-critical-pair counting "
        "measure of TICKET-217 and L(r)=integral r^t dC(t). For tau>0 set "
        "r_H=exp(-tau/H). Then C(H)<=floor(exp(tau)L(r_H)); consequently "
        "a rigorous actual-zeta upper bound U_H<exp(-tau) certifies C(H)=0. "
        "If such bounds hold on a cofinal sequence of H, then C is identically "
        "zero and RH follows within the established defect-measure equivalence. "
        "More generally the first-atom signal is r_H^H=exp(-H beta_H), where "
        "beta_H=-log r_H. It stays uniformly detectable exactly when H beta_H "
        "is bounded above, and vanishes when H beta_H tends to infinity."
    )
    proof = (
        "TICKET-217 gives C(H)r_H^H<=L(r_H). Substitution of "
        "r_H^H=exp(-tau) and integrality gives the certificate. A cofinal "
        "zero certificate covers every finite height. The phase statement is "
        "the identity r_H^H=exp(-H beta_H): bounded H beta_H gives a positive "
        "uniform lower signal, while H beta_H tending to infinity makes that "
        "signal tend to zero. This schedule theorem does not construct or "
        "bound the actual zeta defect transform."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "scale_adaptive_certificate": (
            "r_H=exp(-tau/H), C(H)<=floor(exp(tau)U_H), "
            "U_H<exp(-tau) => C(H)=0"
        ),
        "scale_adaptive_rows": rows,
        "schedule_phase_rows": phase_rows,
        "aggregate": {
            "scale_adaptive_radius_certificate_proved": True,
            "first_atom_schedule_phase_transition_proved": True,
            "cofinal_certificate_would_imply_RH": True,
            "actual_zeta_scale_adaptive_upper_bound_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "Any radius schedule with H(-log r_H) tending to infinity again "
            "drives the first-atom signal to zero, so a fixed positive absolute "
            "error floor cannot close that schedule. This is an information "
            "boundary for the defect measure, not an off-line zeta zero."
        ),
        "failure_count": failures,
    }


def collatz_spike_barrier_audit() -> dict[str, Any]:
    log_three_halves = log_rational_interval(3, 2, 800)
    log_four_thirds = log_rational_interval(4, 3, 800)
    alpha_lower = log_three_halves[0] / log_four_thirds[1]
    alpha_upper = log_three_halves[1] / log_four_thirds[0]
    coefficients = interval_continued_fraction(alpha_lower, alpha_upper, 100)
    all_convergents = convergents(coefficients)
    failures = int(len(coefficients) != 100)
    transcript = hashlib.sha256()
    rows = []

    # Odd-index convergents are above alpha. Index 99 needs q_100 and is left open.
    for index in range(1, 99, 2):
        numerator_p, denominator_q = all_convergents[index]
        next_denominator = all_convergents[index + 1][1]
        neighbor_threshold = 4 * (denominator_q + next_denominator)
        if numerator_p <= 10_000:
            neighbor_barrier = neighbor_threshold < 3**numerator_p
            neighbor_method = "direct_integer_power"
        else:
            neighbor_barrier = neighbor_threshold.bit_length() <= numerator_p
            neighbor_method = "binary_dominance_2_pow_p_below_3_pow_p"

        direct_base_barrier = False
        if not neighbor_barrier and numerator_p <= 10_000:
            delta = (
                1 << (denominator_q + 2 * numerator_p)
            ) - 3 ** (denominator_q + numerator_p)
            direct_base_barrier = delta >= 3**denominator_q
        excluded = neighbor_barrier or direct_base_barrier
        failures += int(not excluded)
        transcript_row = (
            f"{index}:{numerator_p}:{denominator_q}:{next_denominator}:"
            f"{neighbor_method}:{int(neighbor_barrier)}:"
            f"{int(direct_base_barrier)}:{int(excluded)}\n"
        )
        transcript.update(transcript_row.encode("ascii"))
        rows.append(
            {
                "convergent_index": index,
                "reduced_upper_numerator_p": numerator_p,
                "reduced_upper_denominator_q": denominator_q,
                "next_convergent_denominator_q_next": next_denominator,
                "reduced_upper_numerator_p_decimal": str(numerator_p),
                "reduced_upper_denominator_q_decimal": str(denominator_q),
                "next_convergent_denominator_q_next_decimal": str(next_denominator),
                "neighbor_spike_threshold_bit_length": neighbor_threshold.bit_length(),
                "neighbor_barrier_method": neighbor_method,
                "four_q_plus_qnext_below_three_pow_p": neighbor_barrier,
                "fallback_exact_base_difference_barrier": direct_base_barrier,
                "all_positive_multiples_excluded": excluded,
            }
        )

    next_upper = all_convergents[99]
    theorem = (
        "Let p_n/q_n be an upper continued-fraction convergent of "
        "alpha=log(3/2)/log(4/3), and let q_(n+1) be the next convergent "
        "denominator. If 4(q_n+q_(n+1))<3^p_n, then the TICKET-217 scaling "
        "barrier holds and no positive multiple of p_n/q_n can be a "
        "single-mountain Collatz cycle. Therefore any upper convergent that "
        "escapes this sufficient certificate must satisfy the exponential "
        "spike condition 4(q_n+q_(n+1))>=3^p_n. A rational-interval audit "
        "certifies 100 continued-fraction coefficients and excludes the first "
        "49 upper convergents (the first by the earlier exact base-difference "
        "test and the other 48 by the neighbor barrier). The next unaudited "
        "upper denominator is 11828991589305104738667316989568711874512497900863, "
        "so no single-mountain cycle has smaller k."
    )
    proof = (
        "The standard convergent inequality gives "
        "p_n/q_n-alpha>1/(q_n(q_n+q_(n+1))). Multiplication by "
        "q_n log(4/3) yields lambda_n>log(4/3)/(q_n+q_(n+1)). Since "
        "log(1+x)>x/(1+x), log(4/3)>1/4. Under the displayed integer "
        "condition, lambda_n>3^(-p_n), hence exp(lambda_n)-1>3^(-p_n). "
        "TICKET-217 then excludes every positive scaling. Negating the "
        "sufficient condition gives the spike necessity for any candidate "
        "not excluded by this argument. Exact atanh-series intervals certify "
        "the continued fraction; large comparisons use the exact implication "
        "4(q+q_next)<2^p<3^p instead of materializing 3^p."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "alpha_definition": "log(3/2)/log(4/3)",
        "certified_continued_fraction_coefficient_count": len(coefficients),
        "certified_continued_fraction_coefficients": coefficients,
        "audited_upper_convergent_rows": rows,
        "next_unaudited_upper_convergent": {
            "p": next_upper[0],
            "q": next_upper[1],
            "p_decimal": str(next_upper[0]),
            "q_decimal": str(next_upper[1]),
        },
        "single_mountain_k_exclusive_upper_bound": next_upper[1],
        "single_mountain_k_exclusive_upper_bound_decimal": str(next_upper[1]),
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "exponential_next_denominator_spike_necessity_proved": True,
            "audited_upper_convergent_count": len(rows),
            "all_audited_upper_convergents_excluded": all(
                row["all_positive_multiples_excluded"] for row in rows
            ),
            "single_mountain_cycles_below_reported_k_excluded": True,
            "all_single_mountain_cycles_excluded": False,
            "multi_run_cycle_words_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This replaces brute-force cross-power construction by a sharp "
            "continued-fraction neighbor test, but it does not bound every "
            "future partial quotient. Even a complete single-mountain "
            "exclusion would not cover multi-run words or divergence."
        ),
        "failure_count": failures,
    }


def exact_singular_factor(value: int, primes: list[int]) -> Fraction:
    remaining = value
    factor = Fraction(1)
    for prime in primes:
        if prime * prime > remaining:
            break
        if remaining % prime == 0:
            if prime > 2:
                factor *= Fraction(prime - 1, prime - 2)
            while remaining % prime == 0:
                remaining //= prime
    if remaining > 2:
        factor *= Fraction(remaining - 1, remaining - 2)
    return factor


def rounded_model_weight(value: int, primes: list[int], scale: int) -> int:
    factor = exact_singular_factor(value, primes)
    numerator = scale * value * factor.numerator
    denominator = factor.denominator
    return (2 * numerator + denominator) // (2 * denominator)


def goldbach_residual_moment_audit() -> dict[str, Any]:
    starts = (128, 512, 2048, 8192, 32768)
    flags = prime_sieve(2 * max(starts))
    primes = [value for value in range(2, len(flags)) if flags[value]]
    shape_scale = 1_000_000
    orders = (2, 4, 6, 8)
    rows = []
    failures = 0
    transcript = hashlib.sha256()

    for start in starts:
        counts = goldbach_counts(start, flags, primes)
        targets = list(range(start, 2 * start, 2))
        weights = [
            rounded_model_weight(target, primes, shape_scale)
            for target in targets
        ]
        fit_numerator = sum(
            count * weight for count, weight in zip(counts, weights)
        )
        fit_denominator = sum(weight * weight for weight in weights)
        minimum_weight = min(weights)
        moment_rows = []
        for order in orders:
            residual_integer_sum = sum(
                abs(count * fit_denominator - fit_numerator * weight) ** order
                for count, weight in zip(counts, weights)
            )
            zero_coordinate_threshold = (
                fit_numerator * minimum_weight
            ) ** order
            passed = residual_integer_sum < zero_coordinate_threshold
            ratio = Decimal(residual_integer_sum) / Decimal(
                zero_coordinate_threshold
            )
            moment_rows.append(
                {
                    "order_p": order,
                    "exact_residual_integer_sum": str(residual_integer_sum),
                    "exact_zero_coordinate_threshold": str(
                        zero_coordinate_threshold
                    ),
                    "residual_to_threshold_ratio": decimal_string(ratio, 18),
                    "full_support_certificate_passed": passed,
                }
            )
        eighth_passed = moment_rows[-1]["full_support_certificate_passed"]
        failures += int(not eighth_passed)
        transcript.update(
            (
                f"{start}:{len(counts)}:{fit_numerator}:{fit_denominator}:"
                + ":".join(
                    f"{row['order_p']}={int(row['full_support_certificate_passed'])}"
                    for row in moment_rows
                )
                + "\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "dyadic_start_X": start,
                "target_count_B": len(counts),
                "minimum_exact_representation_count": min(counts),
                "integer_model_shape": (
                    "round(10^6*n*product_{odd p|n}(p-1)/(p-2))"
                ),
                "least_squares_scale_numerator_P": str(fit_numerator),
                "least_squares_scale_denominator_Q": str(fit_denominator),
                "moment_rows": moment_rows,
                "eighth_residual_moment_full_support_certified": eighth_passed,
            }
        )

    theorem = (
        "Let A_i>=0 and let M_i>0 be any positive model on a finite block. "
        "For every p>0, if E_p=sum_i |A_i-M_i|^p is strictly smaller than "
        "m^p, where m=min_i M_i, then every A_i is positive. The threshold "
        "is sharp over nonnegative vectors: setting one minimum-model "
        "coordinate to zero and every other coordinate equal to its model "
        "gives equality. With an exact integer Hardy-Littlewood-shaped weight "
        "w_i and rational least-squares scale M_i=(P/Q)w_i, the condition is "
        "equivalent to sum_i |A_i Q-Pw_i|^p<(P min_i w_i)^p. Exact arithmetic "
        "shows that p=8 certifies full support on all five audited Goldbach "
        "dyadic blocks, while p=4 fails on all five."
    )
    proof = (
        "If A_j=0, then the j-th residual alone equals M_j^p>=m^p, "
        "contradicting E_p<m^p. Equality in the one-zero construction proves "
        "sharpness. Multiplication by Q^p gives the integer certificate. The "
        "finite audit computes every representation count and every rounded "
        "singular-series weight exactly. It does not provide a cofinal "
        "circle-method bound for the eighth residual moment."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "residual_certificate": (
            "sum_i |A_i Q-Pw_i|^p < (P min_i w_i)^p => all A_i>0"
        ),
        "model_weight_scale": shape_scale,
        "dyadic_goldbach_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "sharp_residual_moment_support_certificate_proved": True,
            "exact_eighth_moment_blocks_certified": sum(
                int(row["eighth_residual_moment_full_support_certified"])
                for row in rows
            ),
            "exact_fourth_moment_blocks_certified": sum(
                int(row["moment_rows"][1]["full_support_certificate_passed"])
                for row in rows
            ),
            "cofinal_eighth_moment_arithmetic_bound_proved": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The strict threshold cannot be weakened to a non-strict one. "
            "The p=4 version of this chosen exact model also fails on every "
            "audited block. Passing p=8 is a finite certificate computed from "
            "the full block, not an independent proof for all even integers."
        ),
        "failure_count": failures,
    }


def first_odd_after(value: int) -> int:
    return value + 1 if value % 2 == 0 else value + 2


def twin_abel_surplus_audit() -> dict[str, Any]:
    scales = (1_000, 10_000, 100_000, 1_000_000)
    horizons = [
        math.floor(2 * math.log(math.log(scale)) * scale)
        for scale in scales
    ]
    flags = prime_sieve(max(horizons) + 3)
    twin_starts = [
        value
        for value in range(3, len(flags) - 2, 2)
        if flags[value] and flags[value + 2]
    ]
    rows = []
    failures = 0
    for scale, horizon in zip(scales, horizons):
        radius = 1.0 - 1.0 / scale
        twin_scale = scale / math.log(scale) ** 2
        bounded_twins = [value for value in twin_starts if value <= horizon]
        partial_abel = math.fsum(radius**value for value in bounded_twins)
        first_odd = first_odd_after(horizon)
        geometric_tail = radius**first_odd / (1.0 - radius * radius)
        surplus = partial_abel - geometric_tail
        transfer_lower = max(0.0, surplus)
        inequality_holds = partial_abel <= len(bounded_twins) + geometric_tail
        failures += int(not inequality_holds or surplus <= 0)
        rows.append(
            {
                "X": scale,
                "offset_a": 0,
                "Y_floor_2_loglogX_X": horizon,
                "exact_twin_count_through_Y": len(bounded_twins),
                "partial_actual_twin_Abel_over_X_log2X": partial_abel
                / twin_scale,
                "coefficient_one_tail_over_X_log2X": geometric_tail
                / twin_scale,
                "finite_partial_surplus_over_X_log2X": surplus / twin_scale,
                "transfer_lower_bound_from_partial_data": transfer_lower,
                "finite_transfer_inequality_checked": inequality_holds,
                "numeric_powers_are_not_interval_certificates": True,
            }
        )

    theorem = (
        "For any sequence 0<=a_n<=1 supported on odd n, define "
        "F(r)=sum_n a_n r^n and T(Y)=sum_{n<=Y}a_n. Then "
        "T(Y)>=F(r)-R(r,Y), where R is the coefficient-one odd geometric "
        "tail. Put r_X=1-1/X and Y_X=floor((2 log log X+a)X), with fixed a. "
        "If liminf F(r_X)/(X/log^2 X)>=A and A>exp(-a)/2, then "
        "liminf T(Y_X)/(X/log^2 X)>=A-exp(-a)/2>0. Applied to the twin-prime "
        "indicator, this would prove infinitely many twins. The strict "
        "constant is sharp for this transfer: at any fixed horizon the "
        "logical sequence that is zero through Y and one on every later odd "
        "index has T(Y)=0 and F(r)=R(r,Y)."
    )
    proof = (
        "Split F at Y. The initial part is at most T(Y), because r^n<=1, "
        "and the tail is at most R because a_n<=1. Rearrangement gives the "
        "finite inequality. Divide by X/log^2 X and use the TICKET-217 limit "
        "R/(X/log^2 X)->exp(-a)/2. A positive liminf then forces T(Y_X) to "
        "grow without bound. The horizon-local saturating sequence proves "
        "that equality at the critical constant cannot yield a positive "
        "count from this information alone."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "surplus_transfer": (
            "T(Y)>=F(r)-R(r,Y); liminf F/scale>A_critical => "
            "liminf T/scale>=A-A_critical"
        ),
        "critical_constant_at_offset_zero": 0.5,
        "finite_actual_twin_diagnostic_rows": rows,
        "aggregate": {
            "strict_abel_surplus_to_count_transfer_proved": True,
            "critical_constant_sharp_for_transfer_proved": True,
            "finite_partial_surplus_positive_at_all_scales": all(
                row["finite_partial_surplus_over_X_log2X"] > 0 for row in rows
            ),
            "actual_twin_abel_liminf_above_one_half_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The sharpness sequence is an admissible logical 0-1 sequence, "
            "not a prime sequence. The finite twin rows use deterministic "
            "double-precision powers and are diagnostics, not a cofinal "
            "interval proof of the required Abel liminf."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_scale_adaptive_audit()
    collatz_compute = collatz_spike_barrier_audit()
    goldbach_compute = goldbach_residual_moment_audit()
    twin_compute = twin_abel_surplus_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-218",
            "theorem_name": "ScaleAdaptiveRadiusCertificateAndSignalPhaseTransition",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No rigorous actual-zeta defect-transform upper bound below exp(-tau) is proved on a cofinal scale-adaptive radius sequence.",
            "route_decision": {
                "discard": "radius schedules whose first-atom signal vanishes while numerical absolute error has a fixed positive floor",
                "retain": "the explicit cofinal schedule r_H=exp(-tau/H) together with an actual-zeta upper enclosure below exp(-tau)",
                "next_single_lemma": "ActualZetaScaleAdaptiveDefectEnvelopeBelowExpMinusTau",
            },
            "proof_dag": proof_dag(
                "RH",
                "MultiRadiusNormalizedDefectCertificateAndFinitePrecisionInvisibility",
                "CofinalRelativePrecisionExplicitFormulaEnvelopeBelowOne",
                "ScaleAdaptiveRadiusCertificateAndSignalPhaseTransition",
                "VanishingSignalScheduleWithFixedAbsolutePrecisionImpliesRH",
                "ActualZetaScaleAdaptiveDefectEnvelopeBelowExpMinusTau",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof and no off-line zeta zero. TICKET-218 specifies the nonvanishing-signal radius schedule; the actual-zeta bound on that schedule is open.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-218",
            "theorem_name": "ExponentialNextDenominatorSpikeBarrierAnd49ConvergentExclusion",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "Future exponential continued-fraction spikes, all multi-run valuation words, and nonperiodic divergence remain uncontrolled.",
            "route_decision": {
                "discard": "materializing enormous cross-power differences for every convergent when the next-denominator inequality already certifies exclusion",
                "retain": "an effective upper bound excluding exponential partial-quotient spikes, followed by a separate multi-run and divergence theory",
                "next_single_lemma": "EffectiveExponentialPartialQuotientBoundForCollatzLogRatio",
            },
            "proof_dag": proof_dag(
                "CO",
                "SingleMountainContinuedFractionCompressionAnd71356888Barrier",
                "EffectiveAllUpperConvergentScalingBarrierForSingleMountainWords",
                "ExponentialNextDenominatorSpikeBarrierAnd49ConvergentExclusion",
                "PolynomialSizeNextDenominatorsCanSupportSingleMountainCycles",
                "EffectiveExponentialPartialQuotientBoundForCollatzLogRatio",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or divergent orbit. The reported k bound applies only to single-mountain words and does not control future exponential partial-quotient spikes.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-218",
            "theorem_name": "SharpResidualMomentSupportCertificateAndExactEighthMomentAudit",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "No cofinal arithmetic eighth-residual-moment estimate is proved independently of full block enumeration.",
            "route_decision": {
                "discard": "the uncentered two-moment test and the non-strict residual threshold as routes to empty exceptional sets",
                "retain": "a cofinal exact eighth-residual-moment estimate around a positive singular-series model, plus finite verification below its cutoff",
                "next_single_lemma": "CofinalGoldbachEighthResidualMomentBelowZeroCoordinateBarrier",
            },
            "proof_dag": proof_dag(
                "GB",
                "WeightedSecondMomentFullSupportCertificateAndSharpThresholdNoGo",
                "PointwiseGoldbachLowerTailBoundBeyondSecondMomentSupportBarrier",
                "SharpResidualMomentSupportCertificateAndExactEighthMomentAudit",
                "NonStrictResidualMomentThresholdForcesFullSupport",
                "CofinalGoldbachEighthResidualMomentBelowZeroCoordinateBarrier",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The p=8 certificate closes five finite blocks exactly; its required cofinal arithmetic estimate is open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-218",
            "theorem_name": "SharpAbelSurplusToTwinCountTransferAtCriticalConstant",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No parity-sensitive proof establishes that the actual twin-prime Abel liminf coefficient is strictly greater than one half at offset zero.",
            "route_decision": {
                "discard": "a non-strict Abel lower coefficient equal to the geometric-tail constant as sufficient for twin infinitude",
                "retain": "a strict actual-twin Abel liminf surplus above one half, which transfers quantitatively to the counting function",
                "next_single_lemma": "ActualTwinAbelLiminfCoefficientGreaterThanOneHalf",
            },
            "proof_dag": proof_dag(
                "TP",
                "SharpAdaptiveAbelTailPhaseTransitionAtTwoLogLog",
                "TwinAbelLowerBoundWithExplicitSurplusAboveCriticalTailConstant",
                "SharpAbelSurplusToTwinCountTransferAtCriticalConstant",
                "CriticalEqualityAbelCoefficientImpliesTwinInfinitude",
                "ActualTwinAbelLiminfCoefficientGreaterThanOneHalf",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or last-twin counterexample. The surplus transfer and its constant are exact; the actual parity-breaking Abel lower bound is open.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "AdaptiveRadiusSpikeResidualSurplusAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-218 proves four exact partial, reduction, or no-go "
            "theorems and resolves none of the parent conjectures. It fixes "
            "a nonvanishing-signal RH radius schedule, reduces surviving "
            "single-mountain Collatz candidates to exponential partial-"
            "quotient spikes and excludes 49 upper convergents, replaces the "
            "failed Goldbach second-moment test by an exact finite eighth-"
            "residual-moment certificate, and proves the sharp Twin Abel "
            "surplus-to-count transfer at its critical constant."
        ),
        **sections,
        "cross_problem_synthesis": (
            "All four tracks now expose an explicit strict margin that an "
            "infinite proof must supply: exp(-tau) for RH, exclusion of "
            "exponential continued-fraction spikes for Collatz, an eighth-"
            "moment residual below one missing-coordinate energy for "
            "Goldbach, and an actual Abel coefficient above one half for "
            "Twin Prime. Finite positive diagnostics are kept separate from "
            "those open arithmetic margins."
        ),
        "literature_boundary": {
            "riemann": "The schedule identity is a reduction inside the project defect-measure formalism, not a new zero-free region or verified height.",
            "collatz": "The continued-fraction neighbor inequality is classical; the computation is a narrow single-mountain exclusion and carries no priority claim.",
            "goldbach": "The residual-moment support lemma is elementary; the project does not prove the required circle-method moment estimate.",
            "twin_prime": "The Abel transfer does not overcome the sieve parity barrier; it isolates the exact lower coefficient that would be sufficient.",
        },
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_limited_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = []
    for section_key, problem_id in (
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin_prime", "twin-prime"),
    ):
        section = audit[section_key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "status": STATUS,
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "bounded_result": {
                    "audit_ref": "#/adaptive_radius_spike_residual_surplus_audit"
                },
            }
        )
    return attempts


def standalone_payload(section: dict[str, Any], problem_id: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "ticket_id": section["ticket_id"],
        "problem_id": problem_id,
        "status": STATUS,
        "theorem_name": section["theorem_name"],
        "declared_proposition": section["declared_proposition"],
        "mathematical_argument": section["mathematical_argument"],
        "reproducible_computation": section["reproducible_computation"],
        "discarded_route": section["route_decision"]["discard"],
        "remaining_gap": section["logical_limit"],
        "candidate_theorem": section["route_decision"]["next_single_lemma"],
        "claim_boundary": section["claim_boundary"],
        "proof_dag": section["proof_dag"],
    }


def write_outputs(audit: dict[str, Any]) -> None:
    integrated = (
        ROOT
        / "data/open-problem/ticket218-adaptive-radius-spike-residual-surplus.json"
    )
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "adaptive_radius_spike_residual_surplus_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-218-scale-adaptive-radius.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-218-exponential-spike-barrier.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-218-eighth-residual-moment.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-218-abel-surplus-transfer.json",
    }
    problem_ids = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin_prime": "twin-prime",
    }
    for section_key, path in targets.items():
        write_json(path, standalone_payload(audit[section_key], problem_ids[section_key]))


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {
                "schema": SCHEMA,
                "status": STATUS,
                "machine_audit": audit["machine_audit"],
            },
            indent=2,
        )
    )
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
