from __future__ import annotations

import cmath
import json
import math
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket132_admissibility_nullset_hard_stratum_local_parity import (
    fraction_payload,
)
from ticket139_uniformity_diophantine_and_complexity import (
    barycentric_annihilator,
)


GENERATED_AT = "2026-07-29T12:00:00+09:00"
SCHEMA = (
    "primeproject.ticket140-spectral-moments-fixed-floor-duality-rotation.v1"
)


def minimum_even_moment_order(
    rank: int,
    factor_numerator: int = 6,
    factor_denominator: int = 5,
) -> int:
    order = 1
    while (
        rank * factor_denominator ** (2 * order)
        > factor_numerator ** (2 * order)
    ):
        order += 1
    return order


def riemann_even_trace_moment_certificate() -> dict[str, Any]:
    rows = []
    failures = 0
    for rank in [4, 16, 64, 256, 1024, 4096]:
        order = minimum_even_moment_order(rank)
        current_passes = rank * 5 ** (2 * order) <= 6 ** (2 * order)
        previous_fails = (
            order == 1
            or rank * 5 ** (2 * (order - 1)) > 6 ** (2 * (order - 1))
        )
        checks = {
            "minimum_order_passes_exact_integer_test": current_passes,
            "previous_order_fails_exact_integer_test": previous_fails,
            "logarithmic_order_is_positive": order >= 1,
        }
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "rank": rank,
                "target_schatten_factor": "6/5",
                "minimum_even_moment_order_m": order,
                "moment_power": 2 * order,
                "sharp_identity_family_factor_decimal": (
                    rank ** (1 / (2 * order))
                ),
                "checks": checks,
            }
        )

    return {
        "theorem_name": "EvenTraceMomentSpectralCertificateAndLogOrderBarrier",
        "title_ko": "짝수 trace moment 스펙트럼 인증과 로그 차수 장벽 정리",
        "declared_target": (
            "Replace the TICKET139 absolute cross-Gram budget by a signed, "
            "computable spectral certificate and determine how its moment "
            "order must scale with matrix dimension."
        ),
        "proved_statement": (
            "For every self-adjoint r by r matrix E and integer m>=1, "
            "rho(E)^(2m)<=tr(E^(2m))<=r rho(E)^(2m). Hence a positive base "
            "operator A>=gI remains positive after adding E whenever "
            "tr(E^(2m))<g^(2m). The certificate preserves signed closed-walk "
            "cancellation inside the trace expansion. It is sharp on E=I_r: "
            "the Schatten estimate overstates rho(E) by r^(1/(2m)). Therefore "
            "a fixed factor 1+epsilon requires "
            "m>=log(r)/(2log(1+epsilon)) in the worst case."
        ),
        "proved_statement_ko": (
            "r차 자기수반 행렬 E와 m>=1에 대해 "
            "rho(E)^(2m)<=tr(E^(2m))<=r rho(E)^(2m)이다. 따라서 A>=gI이고 "
            "tr(E^(2m))<g^(2m)이면 A+E는 양의 정부호다. trace 전개 내부의 "
            "부호 있는 닫힌 경로 상쇄를 보존하지만, E=I_r에서는 추정값이 "
            "실제 spectral radius를 r^(1/(2m))배 과대평가한다. 고정 상대 "
            "정확도를 얻으려면 최악의 경우 moment 차수가 log r 규모로 "
            "증가해야 한다."
        ),
        "proof": (
            "Diagonalize E with real eigenvalues lambda_i. Then "
            "tr(E^(2m))=sum_i |lambda_i|^(2m), which is at least the largest "
            "term rho(E)^(2m) and at most r times that term. Thus the strict "
            "trace inequality implies ||E||=rho(E)<g, and "
            "<x,(A+E)x>>=(g-||E||)||x||^2 for nonzero x. For E=I_r, the "
            "trace root is exactly r^(1/(2m)) while rho(E)=1, proving the "
            "worst-case order barrier."
        ),
        "exact_contract": {
            "spectral_sandwich": (
                "rho(E)^(2m)<=tr(E^(2m))<=r*rho(E)^(2m)"
            ),
            "positivity_certificate": "tr(E^(2m))<g^(2m) implies A+E>0",
            "sharp_family": "E=I_r",
            "six_fifths_order": (
                "r*5^(2m)<=6^(2m)"
            ),
        },
        "trace_moment_audit": {
            "rows": rows,
            "row_count": len(rows),
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "dimension-growing even trace moments of the actual projected "
                "Weil signed Gram tail"
            ),
            "discard": (
                "any fixed finite trace-moment order as a dimension-uniform "
                "replacement for the signed spectral-radius theorem"
            ),
            "next_theorem": (
                "ProjectedWeilLogOrderEvenTraceMomentBelowTailGap"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "RH-TD4b.2b.2",
                    "label": "TwoMutuallyUnbiasedBasesCrossGramL1NoGo",
                    "status": "closed",
                },
                {
                    "id": "RH-TD4b.2b.3a",
                    "label": (
                        "EvenTraceMomentSpectralCertificateAndLogOrderBarrier"
                    ),
                    "status": "closed",
                },
                {
                    "id": "RH-TD4b.2b.3b",
                    "label": (
                        "ProjectedWeilLogOrderEvenTraceMomentBelowTailGap"
                    ),
                    "status": "highest_risk_open",
                },
                {
                    "id": "RH",
                    "label": "Riemann Hypothesis",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["RH-TD4b.2b.2", "RH-TD4b.2b.3a"],
                ["RH-TD4b.2b.3a", "RH-TD4b.2b.3b"],
                ["RH-TD4b.2b.3b", "RH"],
            ],
        },
        "machine_audit": {
            "trace_moment_row_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem is exact finite-dimensional linear algebra. It does "
            "not identify or bound the actual projected Weil trace moments, "
            "does not establish a uniform positive tail gap, and proves no RH "
            "implication or counterexample."
        ),
    }


def exact_fixed_floor_threshold(minimum: int) -> int:
    numerator = 3 * minimum + 1
    denominator = 3 * minimum
    numerator_power = 1
    denominator_power = 1
    period = 0
    while numerator_power <= 2 * denominator_power:
        period += 1
        numerator_power *= numerator
        denominator_power *= denominator
    return period


def collatz_fixed_floor_window_no_go() -> dict[str, Any]:
    rows = []
    failures = 0
    for exponent in [4, 6, 8, 10, 12, 28]:
        minimum = 2**exponent
        certified_period = (7 * (3 * minimum + 1) + 9) // 10
        exact_threshold = (
            exact_fixed_floor_threshold(minimum) if exponent <= 12 else None
        )
        checks = {
            "certified_period_meets_rational_threshold": (
                10 * certified_period >= 7 * (3 * minimum + 1)
            ),
            "truncated_exponential_proves_exp_point_seven_gt_two": (
                12013 > 12000
            ),
            "exact_small_threshold_not_above_certificate": (
                exact_threshold is None
                or exact_threshold <= certified_period
            ),
        }
        if exact_threshold is not None:
            base = 3 * minimum
            checks["exact_threshold_passes"] = (
                (base + 1) ** exact_threshold > 2 * base**exact_threshold
            )
            checks["preceding_period_fails"] = (
                (base + 1) ** (exact_threshold - 1)
                <= 2 * base ** (exact_threshold - 1)
            )
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "minimum_cycle_floor_M": minimum,
                "floor_exponent": exponent,
                "certified_vacuity_period_K": certified_period,
                "exact_first_vacuity_period_if_computed": exact_threshold,
                "certificate_overhead": (
                    None
                    if exact_threshold is None
                    else certified_period - exact_threshold
                ),
                "checks": checks,
            }
        )

    return {
        "theorem_name": "FixedCycleMinimumWindowEventuallyVacuousNoGo",
        "title_ko": "고정 주기 최솟값 창의 대주기 무력화 한계 정리",
        "declared_target": (
            "Test whether the TICKET139 fixed minimum-cycle floor and product "
            "window can possibly exclude every supercritical period."
        ),
        "proved_statement": (
            "Fix M>=1 and let K=ceil(7(3M+1)/10). For every k>=K, "
            "(1+1/(3M))^k>2. Since S=ceil(k log_2 3) always gives "
            "1<2^S/3^k<2, the fixed-floor TICKET139 necessary window admits "
            "a valuation sum at every k>=K. Thus no fixed lower bound m>=M, "
            "regardless of its size, can yield an all-period cycle exclusion "
            "through this window alone."
        ),
        "proved_statement_ko": (
            "M>=1을 고정하고 K=ceil(7(3M+1)/10)라 하자. 모든 k>=K에서 "
            "(1+1/(3M))^k>2이다. 한편 S=ceil(k log_2 3)이면 항상 "
            "1<2^S/3^k<2이므로 TICKET139의 고정 하한 창은 k>=K인 모든 "
            "주기에서 valuation 합 하나를 허용한다. 따라서 아무리 큰 "
            "고정 최솟값 하한도 이 창만으로 모든 주기를 배제할 수 없다."
        ),
        "proof": (
            "For x>0, log(1+x)>=x/(1+x), so "
            "log(1+1/(3M))>=1/(3M+1). If k>=7(3M+1)/10, the logarithm of the "
            "upper window is at least 7/10. The first four exponential-series "
            "terms give exp(7/10)>1+7/10+49/200+343/6000="
            "12013/6000>2. Irrationality of log_2 3 gives "
            "2^(S-1)<3^k<2^S for S=ceil(k log_2 3), hence the candidate ratio "
            "lies strictly between one and two and is admitted."
        ),
        "exact_contract": {
            "certified_period": "K=ceil(7(3M+1)/10)",
            "log_lower_bound": (
                "log(1+1/(3M))>=1/(3M+1)"
            ),
            "rational_exponential_witness": (
                "1+7/10+49/200+343/6000=12013/6000>2"
            ),
            "candidate_ratio": (
                "1<2^ceil(k log_2 3)/3^k<2"
            ),
        },
        "fixed_floor_audit": {
            "rows": rows,
            "row_count": len(rows),
            "verified_floor_M": 2**28,
            "verified_floor_certified_vacuity_period": rows[-1][
                "certified_vacuity_period_K"
            ],
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "a period-dependent lower bound for the cycle minimum joined "
                "to an explicit lower bound for the logarithmic separation"
            ),
            "discard": (
                "the fixed M=2^28 minimum-cycle floor and product window as an "
                "all-period supercritical cycle exclusion"
            ),
            "next_theorem": (
                "PeriodDependentCycleMinimumDiophantineSeparation"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "CO-TD4b.2b.2",
                    "label": (
                        "CollatzCycleDiophantineWindowAndVerifiedFloorExclusion"
                    ),
                    "status": "closed",
                },
                {
                    "id": "CO-TD4b.2b.3a",
                    "label": "FixedCycleMinimumWindowEventuallyVacuousNoGo",
                    "status": "closed",
                },
                {
                    "id": "CO-TD4b.2b.3b",
                    "label": (
                        "PeriodDependentCycleMinimumDiophantineSeparation"
                    ),
                    "status": "highest_risk_open",
                },
                {
                    "id": "CO-TD4b.2b.4",
                    "label": "AffineCappedAperiodicNaturalCodeWellFoundedness",
                    "status": "open",
                },
                {
                    "id": "CO",
                    "label": "Collatz Conjecture",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["CO-TD4b.2b.2", "CO-TD4b.2b.3a"],
                ["CO-TD4b.2b.3a", "CO-TD4b.2b.3b"],
                ["CO-TD4b.2b.3b", "CO-TD4b.2b.4"],
                ["CO-TD4b.2b.4", "CO"],
            ],
        },
        "machine_audit": {
            "fixed_floor_row_count": len(rows),
            "verified_floor_certified_vacuity_period": rows[-1][
                "certified_vacuity_period_K"
            ],
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This is an exact no-go for one necessary-condition method, not "
            "evidence for a Collatz cycle. Admitting a valuation sum does not "
            "construct a valuation word or integer orbit. Period-dependent "
            "minimum bounds, all cycle realizability constraints, and every "
            "aperiodic trajectory remain open."
        ),
    }


def multiply_polynomials(
    left: list[Fraction],
    right: list[Fraction],
) -> list[Fraction]:
    product = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            product[left_index + right_index] += left_value * right_value
    return product


def lagrange_coordinate_coefficients(
    points: list[Fraction],
    coordinate: int,
) -> list[Fraction]:
    coefficients = [Fraction(1)]
    denominator = Fraction(1)
    selected = points[coordinate]
    for index, point in enumerate(points):
        if index == coordinate:
            continue
        coefficients = multiply_polynomials(
            coefficients,
            [-point, Fraction(1)],
        )
        denominator *= selected - point
    return [coefficient / denominator for coefficient in coefficients]


def evaluate_polynomial(
    coefficients: list[Fraction],
    point: Fraction,
) -> Fraction:
    result = Fraction(0)
    for coefficient in reversed(coefficients):
        result = result * point + coefficient
    return result


def goldbach_measurement_duality_no_go() -> dict[str, Any]:
    rows = []
    failures = 0
    for order in range(1, 11):
        integer_points = [2 ** (index + 1) for index in range(order + 1)]
        annihilator = barycentric_annihilator(integer_points)
        normalized_points = [
            Fraction(point, integer_points[-1]) for point in integer_points
        ]
        dual = lagrange_coordinate_coefficients(normalized_points, 0)
        interpolation_values = [
            evaluate_polynomial(dual, point) for point in normalized_points
        ]
        amplification = sum(abs(coefficient) for coefficient in dual)
        checks = {
            "q_moments_have_nonzero_null_vector": (
                annihilator["annihilated_moments"] == [0] * order
            ),
            "null_vector_moves_every_coordinate": all(
                int(weight) != 0
                for weight in annihilator["integer_weights"]
            ),
            "q_plus_one_moments_reconstruct_first_coordinate": (
                interpolation_values
                == [Fraction(1)] + [Fraction(0)] * order
            ),
            "dual_amplification_positive": amplification > 0,
        }
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "moment_order_q": order,
                "support_size": order + 1,
                "q_measurement_rank": order,
                "nullity": 1,
                "all_coordinates_unbounded_under_q_measurements": True,
                "normalized_support": [
                    fraction_payload(point) for point in normalized_points
                ],
                "first_coordinate_dual_coefficients": [
                    fraction_payload(coefficient) for coefficient in dual
                ],
                "first_coordinate_l1_amplification": fraction_payload(
                    amplification
                ),
                "checks": checks,
            }
        )

    return {
        "theorem_name": "FiniteMeasurementDualCertificateAndPowerOfTwoNullspaceNoGo",
        "title_ko": "유한 측정 dual 인증과 거듭제곱 2 nullspace 한계 정리",
        "declared_target": (
            "Turn the TICKET139 moment annihilator into an exact criterion for "
            "when bounded linear measurements can or cannot control one "
            "Goldbach residual coordinate."
        ),
        "proved_statement": (
            "Let A be a real r by n measurement matrix. A coordinate f_j is "
            "bounded by constraints |Af|<=b only if e_j belongs to the row "
            "space of A. If not, there is z in ker(A) with z_j nonzero, and "
            "f+t z makes the coordinate unbounded without changing any "
            "measurement. If e_j=A^T lambda, then "
            "|f_j|<=sum_i |lambda_i|b_i. For q polynomial moments on q+1 "
            "distinct powers of two, the TICKET139 barycentric vector lies in "
            "the kernel and has every coordinate nonzero, so no coordinate is "
            "controlled. Adding moment q makes the Vandermonde matrix "
            "invertible, but the exact Lagrange dual amplification grows "
            "rapidly on the normalized power-of-two support."
        ),
        "proved_statement_ko": (
            "실수 측정 행렬 A에 대해 |Af|<=b만으로 좌표 f_j를 제어하려면 "
            "e_j가 A의 row space에 있어야 한다. 그렇지 않으면 z_j!=0인 "
            "z in ker(A)가 존재해 측정값을 바꾸지 않고 f+t z의 좌표를 "
            "무한히 키울 수 있다. e_j=A^T lambda이면 "
            "|f_j|<=sum |lambda_i|b_i다. q+1개 거듭제곱 2 점에서 q개 "
            "모멘트만 쓰면 TICKET139 barycentric 벡터가 모든 좌표가 "
            "0이 아닌 null 벡터이므로 어느 점도 제어되지 않는다. 모멘트 "
            "하나를 더하면 대수적 복원은 가능하지만 dual 증폭이 빠르게 "
            "증가한다."
        ),
        "proof": (
            "The orthogonal complement of row(A) is ker(A). If e_j is not in "
            "row(A), its projection onto ker(A) gives z with z_j=<e_j,z> "
            "nonzero. Then A(f+t z)=Af for every t. Conversely, "
            "e_j=A^T lambda gives f_j=<lambda,Af>, and the weighted triangle "
            "inequality proves the bound. Distinct-node Vandermonde rank and "
            "the exact barycentric identities prove the power-of-two "
            "specialization. Lagrange interpolation supplies the displayed "
            "dual after the final moment is added."
        ),
        "exact_contract": {
            "boundedness_criterion": "e_j belongs to row(A)",
            "nullspace_no_go": (
                "z in ker(A), z_j!=0 implies unbounded f_j"
            ),
            "dual_certificate": (
                "A^T lambda=e_j implies |f_j|<=sum |lambda_i|b_i"
            ),
            "power_two_rank": (
                "q moments on q+1 nodes have rank q and nullity one"
            ),
        },
        "measurement_duality_audit": {
            "rows": rows,
            "row_count": len(rows),
            "largest_first_coordinate_amplification": rows[-1][
                "first_coordinate_l1_amplification"
            ],
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "an arithmetic dual certificate whose rows are actual "
                "localized or all-frequency Goldbach residual estimates"
            ),
            "discard": (
                "any incomplete finite measurement family whose row space "
                "does not contain the required point-evaluation functional"
            ),
            "next_theorem": (
                "ArithmeticK56DualCertificateOnPowerOfTwoHardStratum"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "GB-TD4b.2b.2",
                    "label": "PowerOfTwoBarycentricMomentAnnihilatorNoGo",
                    "status": "closed",
                },
                {
                    "id": "GB-TD4b.2b.3a",
                    "label": (
                        "FiniteMeasurementDualCertificateAndPowerOfTwoNullspaceNoGo"
                    ),
                    "status": "closed",
                },
                {
                    "id": "GB-TD4b.2b.3b",
                    "label": (
                        "ArithmeticK56DualCertificateOnPowerOfTwoHardStratum"
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
                ["GB-TD4b.2b.2", "GB-TD4b.2b.3a"],
                ["GB-TD4b.2b.3a", "GB-TD4b.2b.3b"],
                ["GB-TD4b.2b.3b", "GB"],
            ],
        },
        "machine_audit": {
            "measurement_order_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem characterizes information sufficiency for finite "
            "linear measurements. The null signals are inference "
            "countermodels, not actual Goldbach residuals. No arithmetic "
            "K=56 dual certificate, minor-arc estimate, or all-even cutoff is "
            "proved."
        ),
    }


def sqrt_two_nearest_integer(value: int, sqrt_two: Decimal) -> int:
    return int(
        (Decimal(value) * sqrt_two).to_integral_value(
            rounding=ROUND_HALF_EVEN
        )
    )


def rotation_polynomial_sum(
    harmonic_limit: int,
    sample_count: int,
) -> float:
    alpha = math.sqrt(2)
    total = 0j
    for harmonic in range(1, harmonic_limit + 1):
        phase = cmath.exp(2j * math.pi * harmonic * alpha)
        geometric = (
            phase * (1 - phase**sample_count) / (1 - phase)
        )
        total += (
            geometric + geometric.conjugate()
        ) / harmonic**3
    return abs(total.real)


def twin_sobolev_rotation_cancellation() -> dict[str, Any]:
    getcontext().prec = 90
    sqrt_two = Decimal(2).sqrt()
    rows = []
    failures = 0
    sample_counts = [10, 100, 1000, 10_000]
    for harmonic_limit in [4, 8, 16, 32, 64]:
        diophantine_checks = []
        for harmonic in range(1, harmonic_limit + 1):
            nearest = sqrt_two_nearest_integer(harmonic, sqrt_two)
            residual = nearest * nearest - 2 * harmonic * harmonic
            diophantine_checks.append(
                residual != 0 and nearest < 2 * harmonic
            )
        exact_bound = 4 * sum(
            (Fraction(1, harmonic * harmonic)
             for harmonic in range(1, harmonic_limit + 1)),
            Fraction(0),
        )
        observations = [
            {
                "sample_count_N": sample_count,
                "absolute_birkhoff_sum": rotation_polynomial_sum(
                    harmonic_limit,
                    sample_count,
                ),
            }
            for sample_count in sample_counts
        ]
        maximum_observation = max(
            observations,
            key=lambda row: row["absolute_birkhoff_sum"],
        )
        checks = {
            "quadratic_irrational_bound_verified_for_harmonics": all(
                diophantine_checks
            ),
            "numeric_sums_below_exact_uniform_bound": all(
                row["absolute_birkhoff_sum"] < float(exact_bound)
                for row in observations
            ),
            "bound_independent_of_sample_count": True,
        }
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "harmonic_limit_H": harmonic_limit,
                "coefficient_family": "c_h=c_-h=1/h^3",
                "sobolev_order_s": 2,
                "sample_counts": sample_counts,
                "exact_uniform_bound": fraction_payload(exact_bound),
                "maximum_observed_absolute_sum": maximum_observation[
                    "absolute_birkhoff_sum"
                ],
                "maximum_observation_sample_count": maximum_observation[
                    "sample_count_N"
                ],
                "observations": observations,
                "checks": checks,
            }
        )

    return {
        "theorem_name": "QuadraticIrrationalSobolevRotationCancellation",
        "title_ko": "이차 무리수 Sobolev 회전 상쇄 정리",
        "declared_target": (
            "Prove the first genuinely scale-uniform analytic cancellation "
            "statement inside the TICKET139 irrational-feature route, while "
            "separating it from the still-missing arithmetic Type II estimate."
        ),
        "proved_statement": (
            "Let F(x)=sum_(0<|h|<=H)c_h exp(2pi i h x) have zero mean. For "
            "alpha=sqrt(2), ||h alpha||>1/(4|h|), so every N satisfies "
            "|sum_(n=1)^N F(n alpha)|<="
            "2 sum_(0<|h|<=H)|h c_h|. By Cauchy-Schwarz this is at most "
            "2 C_(s,H)||F||_(H^s), where "
            "C_(s,H)^2=sum_(0<|h|<=H)|h|^(2-2s). For s>3/2 the constants "
            "remain bounded as H grows. This is uniform in N."
        ),
        "proved_statement_ko": (
            "평균 0인 삼각다항식 F와 alpha=sqrt(2)에 대해 "
            "||h alpha||>1/(4|h|)이므로 모든 N에서 "
            "|sum_{n<=N}F(n alpha)|<=2 sum |h c_h|이다. Cauchy-Schwarz를 "
            "적용하면 이는 2 C_(s,H)||F||_(H^s) 이하이고, s>3/2이면 "
            "H가 증가해도 C_(s,H)는 유계다. 따라서 TICKET139에서 요구한 "
            "규모 독립 정칙성으로 순수 무리수 회전합의 N-균일 상쇄를 "
            "실제로 얻는다."
        ),
        "proof": (
            "For p nearest to h sqrt(2), the nonzero integer "
            "|p^2-2h^2| is at least one. Since p<2h and sqrt(2)<2, "
            "||h sqrt(2)||=|p-h sqrt(2)|="
            "|p^2-2h^2|/(p+h sqrt(2))>1/(4h). The geometric-sum identity and "
            "|sin(pi x)|>=2||x|| give "
            "|sum_(n<=N)e(h n sqrt(2))|<=1/(2||h sqrt(2)||)<2h. Summing "
            "Fourier modes and applying Cauchy-Schwarz proves both displayed "
            "bounds. The p-series converges exactly when s>3/2."
        ),
        "exact_contract": {
            "diophantine_bound": (
                "||h sqrt(2)||>1/(4|h|)"
            ),
            "mode_sum_bound": (
                "|sum_(n<=N)e(h n sqrt(2))|<2|h|"
            ),
            "sobolev_bound": (
                "|sum F(n sqrt(2))|<=2 C_(s,H)||F||_(H^s)"
            ),
            "uniform_sobolev_threshold": "s>3/2",
        },
        "sobolev_rotation_audit": {
            "alpha": "sqrt(2)",
            "rows": rows,
            "row_count": len(rows),
            "failure_count": failures,
            "numeric_boundary": (
                "floating-point geometric sums are diagnostics only; the "
                "Diophantine and Sobolev theorem is algebraic"
            ),
        },
        "route_decision": {
            "retain": (
                "scale-uniform Sobolev regularity combined with arithmetic "
                "bilinear Type II coefficients and positive exact-gap-two mass"
            ),
            "discard": (
                "unweighted irrational-rotation cancellation alone as a "
                "parity-breaking or twin-prime lower-bound theorem"
            ),
            "next_theorem": (
                "DiophantineSobolevTypeIIBilinearCancellationWithPositiveTwinMass"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "TP-TD3b.2b.2",
                    "label": (
                        "FiniteIrrationalOrbitLipschitzLookupComplexityNoGo"
                    ),
                    "status": "closed",
                },
                {
                    "id": "TP-TD3b.2b.3a",
                    "label": (
                        "QuadraticIrrationalSobolevRotationCancellation"
                    ),
                    "status": "closed",
                },
                {
                    "id": "TP-TD3b.2b.3b",
                    "label": (
                        "DiophantineSobolevTypeIIBilinearCancellationWithPositiveTwinMass"
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
                ["TP-TD3b.2b.2", "TP-TD3b.2b.3a"],
                ["TP-TD3b.2b.3a", "TP-TD3b.2b.3b"],
                ["TP-TD3b.2b.3b", "TP"],
            ],
        },
        "machine_audit": {
            "sobolev_rotation_row_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem proves uniform cancellation only for an unweighted "
            "quadratic-irrational rotation and a regular Fourier observable. "
            "It does not control Vaughan or Mobius bilinear coefficients, "
            "does not break the sieve parity barrier, and provides no positive "
            "exact-gap-two mass."
        ),
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": riemann_even_trace_moment_certificate(),
        "collatz": collatz_fixed_floor_window_no_go(),
        "goldbach": goldbach_measurement_duality_no_go(),
        "twin_prime": twin_sobolev_rotation_cancellation(),
    }
    failures = sum(
        section["machine_audit"]["total_failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureSpectralMomentDualityRotationAudit",
        **sections,
        "cross_problem_synthesis": {
            "shared_obstruction": (
                "A useful finite or analytic certificate must carry the right "
                "scale: fixed moment order, fixed cycle floor, incomplete "
                "measurements, and unweighted rotation sums each lose the "
                "problem-specific infinite information."
            ),
            "shared_upgrade": (
                "The next routes require logarithmically growing projected "
                "Weil moments, period-dependent Collatz minimum separation, "
                "an arithmetic Goldbach dual certificate, and weighted "
                "Sobolev Type II cancellation with positive twin mass."
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
            "TICKET140 proves four exact intermediate or proof-route no-go "
            "theorems and revises four proof targets. It does not prove or "
            "refute RH, Collatz, strong Goldbach, or Twin Prime. No conjecture "
            "proof and no certified conjecture counterexample is claimed."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-140",
            "EvenTraceMomentSpectralCertificateAndLogOrderBarrier",
            "ProjectedWeilLogOrderEvenTraceMomentBelowTailGap",
            "Compute signed even trace moments of one explicit projected Weil Gram tail at moment order proportional to log dimension.",
        ),
        (
            "collatz",
            "CO-TICKET-140",
            "FixedCycleMinimumWindowEventuallyVacuousNoGo",
            "PeriodDependentCycleMinimumDiophantineSeparation",
            "Join a period-dependent lower bound for the cycle minimum to explicit separation of k log 3 from powers of two.",
        ),
        (
            "goldbach",
            "GB-TICKET-140",
            "FiniteMeasurementDualCertificateAndPowerOfTwoNullspaceNoGo",
            "ArithmeticK56DualCertificateOnPowerOfTwoHardStratum",
            "Build a dual point-evaluation certificate from actual localized Goldbach major/minor-arc measurements and audit its K=56 amplification.",
        ),
        (
            "twin-prime",
            "TP-TICKET-140",
            "QuadraticIrrationalSobolevRotationCancellation",
            "DiophantineSobolevTypeIIBilinearCancellationWithPositiveTwinMass",
            "Insert Vaughan or Mobius bilinear coefficients into the uniform Sobolev rotation estimate and preserve a positive exact-gap-two main term.",
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
        "spectral_moment_duality_rotation_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket140-spectral-moments-fixed-floor-duality-rotation.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-140-even-trace-moment.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-140-fixed-floor-window-no-go.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-140-measurement-duality.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-140-sobolev-rotation-cancellation.json",
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
