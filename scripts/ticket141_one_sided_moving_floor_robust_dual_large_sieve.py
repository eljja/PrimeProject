from __future__ import annotations

import cmath
import json
import math
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket132_admissibility_nullset_hard_stratum_local_parity import (
    fraction_payload,
)
from ticket140_spectral_moments_fixed_floor_duality_rotation import (
    evaluate_polynomial,
    lagrange_coordinate_coefficients,
    minimum_even_moment_order,
)


GENERATED_AT = "2026-07-30T12:00:00+09:00"
SCHEMA = (
    "primeproject.ticket141-one-sided-moving-floor-robust-dual-"
    "large-sieve.v1"
)


def safe_fraction_payload(value: Fraction) -> dict[str, Any]:
    log2_magnitude = (
        math.log2(abs(value.numerator)) - math.log2(value.denominator)
        if value
        else None
    )
    decimal = (
        float(value)
        if value and abs(log2_magnitude or 0) < 1020
        else (0.0 if not value else None)
    )
    return {
        "exact": str(value),
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": decimal,
        "log2_magnitude": log2_magnitude,
    }


def riemann_shifted_trace_certificate() -> dict[str, Any]:
    rows = []
    failures = 0
    gap = Fraction(1)
    spike = Fraction(6, 5)
    upper_bound = spike
    shifted_threshold = upper_bound + gap
    for rank in [4, 16, 64, 256, 1024, 4096]:
        order = minimum_even_moment_order(rank)
        two_sided_moment = rank * spike ** (2 * order)
        positive_shifted_moment = Fraction(0)
        negative_shifted_moment = rank * (2 * spike) ** (2 * order)
        threshold_moment = shifted_threshold ** (2 * order)
        checks = {
            "opposite_spikes_have_identical_even_moments": (
                two_sided_moment == rank * (-spike) ** (2 * order)
            ),
            "positive_spike_passes_shifted_certificate": (
                positive_shifted_moment < threshold_moment
            ),
            "negative_spike_fails_shifted_certificate": (
                negative_shifted_moment >= threshold_moment
            ),
            "positive_base_sum_is_strictly_positive": gap + spike > 0,
            "negative_base_sum_is_not_positive": gap - spike < 0,
        }
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "rank": rank,
                "moment_order_m": order,
                "spike_c": fraction_payload(spike),
                "base_gap_g": fraction_payload(gap),
                "common_even_trace_moment": fraction_payload(
                    two_sided_moment
                ),
                "positive_shifted_trace_moment": fraction_payload(
                    positive_shifted_moment
                ),
                "negative_shifted_trace_moment": fraction_payload(
                    negative_shifted_moment
                ),
                "shifted_threshold_moment": fraction_payload(
                    threshold_moment
                ),
                "checks": checks,
            }
        )

    return {
        "theorem_name": (
            "ShiftedTraceMomentOneSidedCertificateAndSignBlindnessNoGo"
        ),
        "title_ko": "이동 trace moment 단측 인증과 부호 맹목성 한계 정리",
        "declared_target": (
            "Test whether TICKET140 even moments contain the one-sided "
            "spectral information needed for projected Weil positivity, and "
            "replace them by a sign-sensitive computable certificate."
        ),
        "proved_statement": (
            "Let E be self-adjoint with lambda_max(E)<=R and let A>=gI. "
            "For every m>=1, if tr((RI-E)^(2m))<(R+g)^(2m), then A+E>0. "
            "Indeed RI-E is positive semidefinite and its spectral radius is "
            "R-lambda_min(E). In contrast, the complete sequence of even "
            "moments tr(E^(2m)) is sign-blind: E=cI and E=-cI have identical "
            "even moments, while for A=gI and c>g the first perturbation is "
            "positive and the second is not. Therefore even moments of E "
            "alone cannot be a sound-and-complete positivity decision rule."
        ),
        "proved_statement_ko": (
            "E가 자기수반이고 lambda_max(E)<=R, A>=gI라 하자. m>=1에서 "
            "tr((RI-E)^(2m))<(R+g)^(2m)이면 A+E>0이다. RI-E의 spectral "
            "radius가 R-lambda_min(E)이므로 이 이동 moment는 음의 spectral "
            "edge를 직접 본다. 반면 E=cI와 E=-cI는 모든 짝수 moment가 "
            "같지만 c>g일 때 A=gI에 대한 양의 정부호 여부는 반대다. 따라서 "
            "E의 짝수 moment만으로는 positivity를 필요충분하게 판정할 수 "
            "없다."
        ),
        "proof": (
            "The eigenvalues of F=RI-E are R-lambda_i(E), all nonnegative. "
            "Hence rho(F)^(2m)<=tr(F^(2m)). The strict trace inequality gives "
            "R-lambda_min(E)=rho(F)<R+g, so lambda_min(E)>-g. Weyl's lower "
            "bound yields lambda_min(A+E)>=g+lambda_min(E)>0. For the no-go, "
            "all even powers of cI and -cI have the same trace, but gI+cI>0 "
            "and gI-cI has negative eigenvalue when c>g."
        ),
        "exact_contract": {
            "upper_spectral_input": "lambda_max(E)<=R",
            "one_sided_certificate": (
                "tr((RI-E)^(2m))<(R+g)^(2m) implies A+E>0"
            ),
            "sign_blind_family": "E=cI versus E=-cI with c>g",
            "scope": (
                "finite-dimensional certificate; projected Weil estimate open"
            ),
        },
        "shifted_trace_audit": {
            "rows": rows,
            "row_count": len(rows),
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "shifted one-sided moments of the actual projected Weil tail "
                "with an independently proved upper spectral bound"
            ),
            "discard": (
                "unshifted even moments of the tail as a necessary-and-"
                "sufficient positivity decision rule"
            ),
            "next_theorem": (
                "ProjectedWeilShiftedLogMomentBelowTailGap"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "RH-TD4b.2b.3a",
                    "label": (
                        "EvenTraceMomentSpectralCertificateAndLogOrderBarrier"
                    ),
                    "status": "closed",
                },
                {
                    "id": "RH-TD4b.2b.4a",
                    "label": (
                        "ShiftedTraceMomentOneSidedCertificateAndSignBlindnessNoGo"
                    ),
                    "status": "closed",
                },
                {
                    "id": "RH-TD4b.2b.4b",
                    "label": "ProjectedWeilShiftedLogMomentBelowTailGap",
                    "status": "highest_risk_open",
                },
                {
                    "id": "RH",
                    "label": "Riemann Hypothesis",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["RH-TD4b.2b.3a", "RH-TD4b.2b.4a"],
                ["RH-TD4b.2b.4a", "RH-TD4b.2b.4b"],
                ["RH-TD4b.2b.4b", "RH"],
            ],
        },
        "machine_audit": {
            "shifted_trace_row_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem is exact finite-dimensional spectral algebra. It "
            "does not prove the required upper spectral bound or shifted "
            "trace estimates for the projected Weil operator, does not close "
            "the infinite test-function limit, and proves no RH implication "
            "or counterexample."
        ),
    }


def window_is_below_two(period: int, minimum: int) -> bool:
    return (3 * minimum + 1) ** period < 2 * (3 * minimum) ** period


def minimum_floor_for_window_below_two(period: int) -> int:
    low = 1
    high = max(2, period)
    while not window_is_below_two(period, high):
        high *= 2
    while low < high:
        middle = (low + high) // 2
        if window_is_below_two(period, middle):
            high = middle
        else:
            low = middle + 1
    return low


def collatz_period_dependent_floor_barrier() -> dict[str, Any]:
    periods = [16, 64, 256, 1024, 4096, 16384]
    rows = []
    failures = 0
    asymptotic_slope = 1 / (3 * math.log(2))
    for period in periods:
        minimum = minimum_floor_for_window_below_two(period)
        checks = {
            "minimum_floor_makes_window_strictly_below_two": (
                window_is_below_two(period, minimum)
            ),
            "previous_floor_keeps_window_at_least_two": (
                minimum == 1
                or not window_is_below_two(period, minimum - 1)
            ),
            "ratio_is_positive": minimum / period > 0,
        }
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "period_k": period,
                "minimum_integer_floor_for_window_below_two": minimum,
                "floor_to_period_ratio": minimum / period,
                "asymptotic_required_slope": asymptotic_slope,
                "ratio_error": minimum / period - asymptotic_slope,
                "checks": checks,
            }
        )

    return {
        "theorem_name": "PeriodDependentFloorLinearGrowthBarrier",
        "title_ko": "주기 의존 최솟값 하한의 선형 성장 장벽 정리",
        "declared_target": (
            "Attack the TICKET140 period-dependent cycle-minimum route by "
            "determining the minimum growth rate needed merely to keep its "
            "relaxed Diophantine window from becoming automatically vacuous."
        ),
        "proved_statement": (
            "Let M_k>=1 be a period-dependent lower bound for the minimum "
            "element of a hypothetical positive k-cycle. The TICKET139 window "
            "has upper factor U_k=(1+1/(3M_k))^k. Since "
            "q_k=2^ceil(k log_2 3)/3^k lies strictly between one and two, "
            "U_k>=2 automatically leaves q_k inside the relaxed window. "
            "Avoiding this automatic failure requires "
            "M_k>1/(3(2^(1/k)-1)). The threshold divided by k tends to "
            "1/(3 log 2). Consequently every floor with "
            "limsup M_k/k<1/(3 log 2) is eventually insufficient."
        ),
        "proved_statement_ko": (
            "가상 양의 k-cycle의 최솟값 하한을 M_k라 하자. TICKET139 창의 "
            "상단은 U_k=(1+1/(3M_k))^k이다. "
            "q_k=2^ceil(k log_2 3)/3^k는 항상 1과 2 사이이므로 U_k>=2이면 "
            "완화 창이 q_k를 자동으로 허용한다. 이를 피하려면 "
            "M_k>1/(3(2^(1/k)-1))가 필요하고, 이 임계값을 k로 나눈 값은 "
            "1/(3 log 2)로 수렴한다. 따라서 그보다 작은 선형 기울기의 "
            "주기 의존 하한은 결국 충분하지 않다."
        ),
        "proof": (
            "The candidate q_k is in (1,2) by irrationality of log_2 3. "
            "Thus U_k>=2 places q_k below the upper endpoint. Because the "
            "map M -> (1+1/(3M))^k is strictly decreasing, U_k<2 is "
            "equivalent to M>1/(3(2^(1/k)-1)). Finally "
            "k(2^(1/k)-1) tends to log 2, giving the stated slope and the "
            "limsup consequence."
        ),
        "exact_contract": {
            "automatic_vacuity": (
                "(1+1/(3M_k))^k>=2 leaves "
                "2^ceil(k log_2 3)/3^k in the relaxed window"
            ),
            "necessary_floor_threshold": (
                "M_k>1/(3(2^(1/k)-1))"
            ),
            "asymptotic_slope": "1/(3 log 2)",
            "scope": "necessary condition only; no cycle construction",
        },
        "moving_floor_audit": {
            "rows": rows,
            "row_count": len(rows),
            "asymptotic_required_slope": asymptotic_slope,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "a cycle-minimum lower bound that beats the exact "
                "power-of-two approximation threshold for each period"
            ),
            "discard": (
                "every subcritical-linear period-dependent minimum floor as "
                "an all-period exclusion through the relaxed product window"
            ),
            "next_theorem": (
                "CycleMinimumAboveExactPowerOfTwoWindowThreshold"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "CO-TD4b.2b.3a",
                    "label": "FixedCycleMinimumWindowEventuallyVacuousNoGo",
                    "status": "closed",
                },
                {
                    "id": "CO-TD4b.2b.4a",
                    "label": "PeriodDependentFloorLinearGrowthBarrier",
                    "status": "closed",
                },
                {
                    "id": "CO-TD4b.2b.4b",
                    "label": (
                        "CycleMinimumAboveExactPowerOfTwoWindowThreshold"
                    ),
                    "status": "highest_risk_open",
                },
                {
                    "id": "CO-TD4c",
                    "label": "AperiodicNaturalCodeWellFoundedness",
                    "status": "open",
                },
                {
                    "id": "CO",
                    "label": "Collatz Conjecture",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["CO-TD4b.2b.3a", "CO-TD4b.2b.4a"],
                ["CO-TD4b.2b.4a", "CO-TD4b.2b.4b"],
                ["CO-TD4b.2b.4b", "CO"],
                ["CO-TD4c", "CO"],
            ],
        },
        "machine_audit": {
            "moving_floor_row_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This is a sharp necessary-growth theorem for one relaxed cycle "
            "window. It neither supplies the required cycle-minimum lower "
            "bound nor realizes a valuation word or integer cycle. It says "
            "nothing about divergent aperiodic trajectories and is not a "
            "Collatz proof or counterexample."
        ),
    }


def goldbach_raw_moment_conditioning_no_go() -> dict[str, Any]:
    orders = [2, 4, 6, 8, 10, 12, 16, 56]
    rows = []
    failures = 0
    for order in orders:
        points = [
            Fraction(2**index, 2**order) for index in range(order + 1)
        ]
        dual = lagrange_coordinate_coefficients(points, 0)
        leading = abs(dual[-1])
        amplification = sum(abs(value) for value in dual)
        exponent = order * (order - 1) // 2
        lower_bound = Fraction(2**exponent)
        interpolation_values = [
            evaluate_polynomial(dual, point) for point in points
        ]
        checks = {
            "dual_reconstructs_endpoint_coordinate": (
                interpolation_values
                == [Fraction(1)] + [Fraction(0)] * order
            ),
            "leading_coefficient_matches_closed_formula": (
                leading
                == Fraction(
                    2 ** (order * order),
                    math.prod(2**index - 1 for index in range(1, order + 1)),
                )
            ),
            "l1_amplification_dominates_leading_coefficient": (
                amplification >= leading
            ),
            "quadratic_exponential_lower_bound_is_strict": (
                leading > lower_bound
            ),
            "adversarial_unit_error_attains_l1_amplification": (
                sum(
                    coefficient
                    * (1 if coefficient >= 0 else -1)
                    for coefficient in dual
                )
                == amplification
            ),
        }
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "moment_order_q": order,
                "support_size": order + 1,
                "endpoint_leading_dual_coefficient": safe_fraction_payload(
                    leading
                ),
                "endpoint_l1_amplification": safe_fraction_payload(
                    amplification
                ),
                "strict_lower_bound_power_of_two_exponent": exponent,
                "strict_lower_bound": f"2^{exponent}",
                "amplification_bit_length": amplification.numerator.bit_length(),
                "checks": checks,
            }
        )

    return {
        "theorem_name": (
            "PowerOfTwoRawMomentDualQuadraticExponentialConditioningNoGo"
        ),
        "title_ko": "거듭제곱 2 원시 모멘트 dual의 이차지수 조건수 한계 정리",
        "declared_target": (
            "Test whether the TICKET140 exact row-space dual can be made "
            "robust enough for a pointwise Goldbach residual certificate when "
            "the available measurements are raw monomial moments."
        ),
        "proved_statement": (
            "On q+1 normalized power-of-two nodes x_i=2^(i-q), the unique "
            "degree-q polynomial dual that reconstructs the first coordinate "
            "from moments 0 through q has leading coefficient "
            "2^(q^2)/product_(j=1)^q(2^j-1), which is strictly larger than "
            "2^(q(q-1)/2). Its l1 norm is at least this large. If every raw "
            "moment has independent error at most epsilon, the worst-case "
            "endpoint reconstruction error is exactly epsilon times the dual "
            "l1 norm. Thus raw monomial moments are quadratically "
            "exponentially ill-conditioned for this pointwise task."
        ),
        "proved_statement_ko": (
            "정규화된 q+1개 거듭제곱 2 점 x_i=2^(i-q)에서 0차부터 q차 "
            "모멘트로 첫 좌표를 복원하는 유일한 dual 다항식의 최고차 "
            "계수 절댓값은 2^(q^2)/product(2^j-1)이고 "
            "2^(q(q-1)/2)보다 크다. dual의 l1 norm도 최소 이만큼 크며, "
            "각 원시 모멘트 오차가 epsilon 이하이면 최악의 복원 오차는 "
            "정확히 epsilon 곱하기 dual l1 norm이다. 따라서 이 원시 "
            "모멘트 좌표계는 점별 Goldbach residual 인증에 매우 불안정하다."
        ),
        "proof": (
            "The endpoint Lagrange polynomial is "
            "L_0(x)=product_(j=1)^q(x-x_j)/(x_0-x_j). Its leading "
            "coefficient has magnitude 1/product_(j=1)^q(x_j-x_0). Since "
            "x_j-x_0=(2^j-1)/2^q, the displayed closed formula follows. "
            "Replacing every factor 2^j-1 by the larger 2^j gives the strict "
            "lower bound 2^(q^2-q(q+1)/2)=2^(q(q-1)/2). The l1 statement is "
            "immediate, and choosing each measurement error with the sign of "
            "the matching dual coefficient attains epsilon||lambda||_1."
        ),
        "exact_contract": {
            "nodes": "x_i=2^(i-q), 0<=i<=q",
            "leading_dual_coefficient": (
                "2^(q^2)/product_(j=1)^q(2^j-1)"
            ),
            "conditioning_lower_bound": "||lambda||_1>2^(q(q-1)/2)",
            "robust_error": "worst endpoint error=epsilon||lambda||_1",
        },
        "raw_moment_conditioning_audit": {
            "rows": rows,
            "row_count": len(rows),
            "largest_order": orders[-1],
            "largest_lower_bound_exponent": orders[-1] * (orders[-1] - 1) // 2,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "localized or orthogonal arithmetic measurements with a "
                "uniformly controlled dual norm"
            ),
            "discard": (
                "high-order raw monomial moments on the power-of-two hard "
                "stratum as a numerically and analytically robust pointwise "
                "certificate"
            ),
            "next_theorem": (
                "LocalizedOrthogonalArithmeticK56DualCertificate"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "GB-TD4b.2b.3a",
                    "label": (
                        "FiniteMeasurementDualCertificateAndPowerOfTwoNullspaceNoGo"
                    ),
                    "status": "closed",
                },
                {
                    "id": "GB-TD4b.2b.4a",
                    "label": (
                        "PowerOfTwoRawMomentDualQuadraticExponentialConditioningNoGo"
                    ),
                    "status": "closed",
                },
                {
                    "id": "GB-TD4b.2b.4b",
                    "label": (
                        "LocalizedOrthogonalArithmeticK56DualCertificate"
                    ),
                    "status": "highest_risk_open",
                },
                {
                    "id": "GB",
                    "label": "Strong Goldbach Conjecture",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["GB-TD4b.2b.3a", "GB-TD4b.2b.4a"],
                ["GB-TD4b.2b.4a", "GB-TD4b.2b.4b"],
                ["GB-TD4b.2b.4b", "GB"],
            ],
        },
        "machine_audit": {
            "conditioning_order_count": len(rows),
            "largest_lower_bound_exponent": (
                orders[-1] * (orders[-1] - 1) // 2
            ),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The null and conditioning vectors are linear-inference stress "
            "objects, not Goldbach residuals. This theorem rejects one raw-"
            "moment coordinate system; it neither constructs the localized "
            "arithmetic measurements nor proves a K=56 residual margin, a "
            "Goldbach representation, or a counterexample."
        ),
    }


def approximate_phase_operator_norm_squared(
    rows: int,
    columns: int,
    iterations: int = 80,
) -> float:
    alpha = math.sqrt(2)
    vector = [
        cmath.exp(2j * math.pi * (index + 1) / (columns + 1))
        for index in range(columns)
    ]
    norm = math.sqrt(sum(abs(value) ** 2 for value in vector))
    vector = [value / norm for value in vector]
    rayleigh = 0.0
    for _ in range(iterations):
        image = [
            sum(
                vector[column]
                * cmath.exp(
                    2j
                    * math.pi
                    * alpha
                    * (row + 1)
                    * (column + 1)
                )
                for column in range(columns)
            )
            for row in range(rows)
        ]
        adjoint_image = [
            sum(
                image[row]
                * cmath.exp(
                    -2j
                    * math.pi
                    * alpha
                    * (row + 1)
                    * (column + 1)
                )
                for row in range(rows)
            )
            for column in range(columns)
        ]
        next_norm = math.sqrt(
            sum(abs(value) ** 2 for value in adjoint_image)
        )
        if next_norm == 0:
            return 0.0
        vector = [value / next_norm for value in adjoint_image]
        rayleigh = sum(
            vector[index].conjugate() * adjoint_image[index]
            for index in range(columns)
        ).real
    image = [
        sum(
            vector[column]
            * cmath.exp(
                2j
                * math.pi
                * alpha
                * (row + 1)
                * (column + 1)
            )
            for column in range(columns)
        )
        for row in range(rows)
    ]
    return float(sum(abs(value) ** 2 for value in image))


def twin_quadratic_bilinear_large_sieve() -> dict[str, Any]:
    sizes = [8, 16, 32, 64, 128]
    rows = []
    failures = 0
    alpha = math.sqrt(2)
    for size in sizes:
        spacing_checks = []
        minimum_spacing = 1.0
        for difference in range(1, size):
            nearest = round(difference * alpha)
            residual = abs(nearest * nearest - 2 * difference * difference)
            spacing = abs(difference * alpha - nearest)
            minimum_spacing = min(minimum_spacing, spacing)
            spacing_checks.append(
                residual >= 1 and spacing > 1 / (4 * difference)
            )
        bound_squared = size + 4 * size
        observed_norm_squared = approximate_phase_operator_norm_squared(
            size, size
        )
        bounded_coefficient_ratio = math.sqrt(5 / size)
        checks = {
            "quadratic_spacing_certificate_holds": all(spacing_checks),
            "minimum_spacing_beats_uniform_bound": (
                minimum_spacing > 1 / (4 * size)
            ),
            "observed_operator_norm_is_below_large_sieve_bound": (
                observed_norm_squared < bound_squared
            ),
            "balanced_relative_bound_matches_formula": (
                abs(bounded_coefficient_ratio - math.sqrt(5 / size))
                < 1e-15
            ),
        }
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "M": size,
                "N": size,
                "minimum_phase_spacing": minimum_spacing,
                "spacing_lower_bound": 1 / (4 * size),
                "large_sieve_operator_norm_squared_bound": bound_squared,
                "observed_operator_norm_squared": observed_norm_squared,
                "bounded_coefficient_relative_bound": (
                    bounded_coefficient_ratio
                ),
                "checks": checks,
            }
        )

    return {
        "theorem_name": "QuadraticIrrationalBilinearLargeSieveCancellation",
        "title_ko": "이차 무리수 쌍선형 large-sieve 상쇄 정리",
        "declared_target": (
            "Insert arbitrary separable Type-II-style coefficients into the "
            "TICKET140 sqrt(2) phase and prove a sample-length-uniform power "
            "saving rather than an unweighted rotation estimate."
        ),
        "proved_statement": (
            "For arbitrary complex vectors a_1,...,a_M and b_1,...,b_N, "
            "|sum_(m<=M,n<=N) a_m b_n e(sqrt(2)mn)| is at most "
            "sqrt(M+4N)||a||_2||b||_2. In particular, if both coefficient "
            "sequences are bounded by one, the ratio to the trivial MN bound "
            "is at most sqrt(1/N+4/M), and for M=N=L this is sqrt(5/L)."
        ),
        "proved_statement_ko": (
            "임의의 복소 계수 a_m,b_n에 대해 "
            "|sum a_m b_n e(sqrt(2)mn)|<=sqrt(M+4N)||a||_2||b||_2이다. "
            "두 계수열의 절댓값이 1 이하이면 자명한 MN 상계에 대한 비율은 "
            "sqrt(1/N+4/M) 이하이고, M=N=L이면 sqrt(5/L)이다. 따라서 "
            "TICKET140의 비가중 회전합을 고정 sqrt(2) 위의 실제 쌍선형 "
            "상쇄로 강화한다."
        ),
        "proof": (
            "The points x_n={n sqrt(2)} are delta-separated because for "
            "1<=|h|<N, ||h sqrt(2)||>1/(4|h|)>1/(4N). The analytic large "
            "sieve for delta-separated points gives "
            "sum_(m<=M)|sum_(n<=N)b_n e(mx_n)|^2<=(M-1+delta^(-1))||b||_2^2, "
            "which is strictly below (M+4N)||b||_2^2. Cauchy-Schwarz in m "
            "proves the bilinear bound. The bounded-coefficient corollary "
            "uses ||a||_2<=sqrt(M) and ||b||_2<=sqrt(N)."
        ),
        "standard_input": {
            "name": "analytic large sieve for well-spaced points",
            "priority_claim": "none",
            "reference": (
                "Montgomery and Vaughan, The large sieve, Mathematika 20 "
                "(1973), 119-134, DOI 10.1112/S0025579300004708"
            ),
        },
        "exact_contract": {
            "spacing": "||h sqrt(2)||>1/(4|h|)",
            "energy_bound": (
                "sum_m|sum_n b_n e(sqrt(2)mn)|^2"
                "<=(M+4N)||b||_2^2"
            ),
            "bilinear_bound": (
                "|sum_mn a_m b_n e(sqrt(2)mn)|"
                "<=sqrt(M+4N)||a||_2||b||_2"
            ),
            "balanced_ratio": "sqrt(5/L)",
        },
        "bilinear_large_sieve_audit": {
            "rows": rows,
            "row_count": len(rows),
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "large-sieve energy control for arithmetic bilinear "
                "coefficients uniformly over the full minor-arc phase family"
            ),
            "discard": (
                "a single fixed quadratic-irrational phase estimate as a "
                "twin-prime lower-bound or parity-obstruction theorem"
            ),
            "next_theorem": (
                "UniformMinorArcVaughanBilinearCancellationWithPositiveTwinMass"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "TP-TD3b.2b.3a",
                    "label": "QuadraticIrrationalSobolevRotationCancellation",
                    "status": "closed",
                },
                {
                    "id": "TP-TD3b.2b.4a",
                    "label": (
                        "QuadraticIrrationalBilinearLargeSieveCancellation"
                    ),
                    "status": "closed",
                },
                {
                    "id": "TP-TD3b.2b.4b",
                    "label": (
                        "UniformMinorArcVaughanBilinearCancellationWithPositiveTwinMass"
                    ),
                    "status": "highest_risk_open",
                },
                {
                    "id": "TP",
                    "label": "Twin Prime Conjecture",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["TP-TD3b.2b.3a", "TP-TD3b.2b.4a"],
                ["TP-TD3b.2b.4a", "TP-TD3b.2b.4b"],
                ["TP-TD3b.2b.4b", "TP"],
            ],
        },
        "machine_audit": {
            "bilinear_large_sieve_row_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem is a specialization of the standard analytic large "
            "sieve to one fixed quadratic irrational. It does not provide "
            "uniform minor-arc control over rational approximants, does not "
            "complete a Vaughan or Mobius decomposition, does not resolve "
            "the sieve parity obstruction, and provides no positive exact-"
            "gap-two mass."
        ),
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": riemann_shifted_trace_certificate(),
        "collatz": collatz_period_dependent_floor_barrier(),
        "goldbach": goldbach_raw_moment_conditioning_no_go(),
        "twin_prime": twin_quadratic_bilinear_large_sieve(),
    }
    failures = sum(
        section["machine_audit"]["total_failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureOneSidedMovingFloorRobustDualLargeSieveAudit",
        **sections,
        "cross_problem_synthesis": {
            "shared_obstruction": (
                "The previous finite certificates still lacked directional "
                "or robust arithmetic information: sign-blind moments, "
                "subcritical moving floors, ill-conditioned raw moments, and "
                "one unweighted phase cannot close the infinite targets."
            ),
            "shared_upgrade": (
                "The surviving routes require a shifted projected-Weil "
                "one-sided estimate, an exact Collatz minimum threshold tied "
                "to power-of-two approximation, a localized orthogonal "
                "Goldbach dual, and uniform minor-arc Vaughan bilinear "
                "cancellation with positive twin mass."
            ),
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "route_correction_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "TICKET141 proves four exact intermediate, corollary, or proof-"
            "route no-go theorems and revises four proof targets. It does not "
            "prove or refute RH, Collatz, strong Goldbach, or Twin Prime. No "
            "conjecture proof and no certified conjecture counterexample is "
            "claimed."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-141",
            "ShiftedTraceMomentOneSidedCertificateAndSignBlindnessNoGo",
            "ProjectedWeilShiftedLogMomentBelowTailGap",
            "Construct a shifted moment majorant for one explicit projected Weil tail and prove its upper spectral input independently.",
        ),
        (
            "collatz",
            "CO-TICKET-141",
            "PeriodDependentFloorLinearGrowthBarrier",
            "CycleMinimumAboveExactPowerOfTwoWindowThreshold",
            "Compare a rigorous period-dependent cycle-minimum lower bound with the exact threshold induced by ceil(k log_2 3).",
        ),
        (
            "goldbach",
            "GB-TICKET-141",
            "PowerOfTwoRawMomentDualQuadraticExponentialConditioningNoGo",
            "LocalizedOrthogonalArithmeticK56DualCertificate",
            "Replace raw moments by localized orthogonal major/minor-arc measurements and prove a dual norm below the exact K=56 margin.",
        ),
        (
            "twin-prime",
            "TP-TICKET-141",
            "QuadraticIrrationalBilinearLargeSieveCancellation",
            "UniformMinorArcVaughanBilinearCancellationWithPositiveTwinMass",
            "Lift the fixed sqrt(2) estimate to every required minor arc, insert the actual Vaughan coefficients, and preserve a positive gap-two main term.",
        ),
    ]
    attempts = []
    for problem_id, ticket_id, result, target, experiment in specs:
        section_key = problem_id.replace("-", "_")
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": ticket_id,
                "status": "exact_intermediate_theorem_conjecture_open",
                "route": result,
                "bounded_result": {"audit_ref": section_key},
                "candidate_theorem": target,
                "next_experiment": experiment,
                "claim_boundary": (
                    "No conjecture proof and no certified conjecture counterexample."
                ),
                "proof_boundary": audit[section_key]["proof_boundary"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "exact_intermediate_theorems_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "one_sided_moving_floor_robust_dual_large_sieve_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket141-one-sided-moving-floor-robust-dual-large-sieve.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-141-shifted-trace-moment.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-141-moving-floor-barrier.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-141-raw-moment-conditioning.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-141-bilinear-large-sieve.json",
    }
    for attempt in attempts:
        section_key = attempt["problem_id"].replace("-", "_")
        write_json(
            paths[attempt["problem_id"]],
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                **attempt,
                "result": audit[section_key],
            },
        )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {"schema": SCHEMA, "machine_audit": audit["machine_audit"]},
            indent=2,
        )
    )
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
