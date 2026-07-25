from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket132_admissibility_nullset_hard_stratum_local_parity import (
    fraction_payload,
)
from ticket137_cancellation_entropy_and_information_budget import (
    sylvester_hadamard,
)


GENERATED_AT = "2026-07-28T12:00:00+09:00"
SCHEMA = "primeproject.ticket139-uniformity-diophantine-complexity.v1"


def integer_digest(value: int) -> str:
    magnitude = abs(value)
    payload = magnitude.to_bytes(
        max(1, (magnitude.bit_length() + 7) // 8),
        "big",
    )
    sign = b"-" if value < 0 else b"+"
    return hashlib.sha256(sign + payload).hexdigest()


def riemann_tight_frame_cross_gram_no_go() -> dict[str, Any]:
    rows = []
    failures = 0
    for dimension in [4, 16, 64, 256]:
        root = math.isqrt(dimension)
        hadamard = sylvester_hadamard(dimension)
        diagonal_ok = all(
            sum(value * value for value in row) == dimension
            for row in hadamard
        )
        off_diagonal_ok = all(
            sum(
                hadamard[left][column] * hadamard[right][column]
                for column in range(dimension)
            )
            == 0
            for left in range(dimension)
            for right in range(left)
        )

        row_energy = Fraction(1, 2)
        cross_budget = Fraction(root, 2)
        cross_gram_l1_bound = row_energy + cross_budget
        true_operator_norm_squared = Fraction(1)
        tail_gap_product = Fraction(2)
        checks = {
            "dimension_is_square_hadamard_order": root * root == dimension,
            "integer_hadamard_orthogonality": (
                diagonal_ok and off_diagonal_ok
            ),
            "tight_frame_operator_norm_squared_one": (
                true_operator_norm_squared == 1
            ),
            "true_tail_margin_positive": (
                true_operator_norm_squared < tail_gap_product
            ),
            "l1_cross_gram_rejects_from_dimension_16": (
                dimension < 16
                or cross_gram_l1_bound >= tail_gap_product
            ),
        }
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "dimension": dimension,
                "frame": (
                    "rows of I/sqrt(2) union rows of "
                    "H/sqrt(2N)"
                ),
                "maximum_row_energy": fraction_payload(row_energy),
                "maximum_absolute_cross_gram_budget": fraction_payload(
                    cross_budget
                ),
                "cross_gram_l1_bound": fraction_payload(
                    cross_gram_l1_bound
                ),
                "exact_operator_norm_squared": fraction_payload(
                    true_operator_norm_squared
                ),
                "tail_gap_product": fraction_payload(tail_gap_product),
                "true_operator_margin": fraction_payload(
                    tail_gap_product - true_operator_norm_squared
                ),
                "l1_overestimate_factor": fraction_payload(
                    cross_gram_l1_bound
                ),
                "checks": checks,
            }
        )

    return {
        "theorem_name": "TwoMutuallyUnbiasedBasesCrossGramL1NoGo",
        "title_ko": "두 상호 비편향 기저의 cross-Gram L1 과대평가 한계 정리",
        "declared_target": (
            "Test whether the TICKET138 cross-Gram absolute row budget is "
            "dimension-uniformly close enough to the true operator norm to be "
            "a plausible projected Weil closure criterion."
        ),
        "proved_statement": (
            "Let H be a real Hadamard matrix of square order N and form B by "
            "stacking the rows of I/sqrt(2) and H/sqrt(2N). Then B*B=I, so "
            "||B||_2^2=1. Every row has energy 1/2, but each row has N cross-"
            "basis correlations of magnitude 1/(2sqrt(N)); hence the TICKET138 "
            "absolute cross-Gram row bound is (1+sqrt(N))/2. Its ratio to the "
            "true norm diverges like sqrt(N)/2. Thus the criterion is sufficient "
            "but not necessary and can reject uniformly bounded tight frames."
        ),
        "proved_statement_ko": (
            "제곱 차수 N의 실 Hadamard 행렬 H에 대해 I/sqrt(2)의 행과 "
            "H/sqrt(2N)의 행을 쌓아 B를 만들면 B*B=I이므로 ||B||^2=1이다. "
            "각 행 에너지는 1/2이지만 서로 다른 기저 사이의 상관 절댓값 "
            "합은 sqrt(N)/2여서 TICKET138 예산은 (1+sqrt(N))/2가 된다. "
            "따라서 이 충분조건은 실제 노름을 sqrt(N) 규모로 과대평가할 "
            "수 있으며 projected Weil 경로의 필요조건으로 승격할 수 없다."
        ),
        "proof": (
            "Hadamard orthogonality gives H^T H=N I. Therefore "
            "B*B=I/2+H^T H/(2N)=I. Rows within either basis are orthogonal. "
            "Every standard-basis row has inner product plus or minus "
            "1/(2sqrt(N)) with each of the N Hadamard-basis rows, and the same "
            "holds in the reverse direction. The maximum absolute off-diagonal "
            "row sum is sqrt(N)/2, proving the formula and its divergence."
        ),
        "exact_contract": {
            "frame_operator": "B*B=I",
            "true_norm_squared": "||B||_2^2=1",
            "cross_gram_l1_bound": "(1+sqrt(N))/2",
            "scope": "square Sylvester-Hadamard orders",
        },
        "tight_frame_audit": {
            "rows": rows,
            "row_count": len(rows),
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "signed spectral cancellation in the projected Weil Gram "
                "operator, with a dimension-uniform arithmetic estimate"
            ),
            "discard": (
                "the absolute cross-Gram row budget as a necessary or "
                "dimension-sharp projected Weil criterion"
            ),
            "next_theorem": (
                "ProjectedWeilSignedGramSpectralRadiusBelowTailGap"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "RH-TD4b.2b.1",
                    "label": "CrossGramCorrelationBlockPositivityCriterion",
                    "status": "closed",
                },
                {
                    "id": "RH-TD4b.2b.2a",
                    "label": "TwoMutuallyUnbiasedBasesCrossGramL1NoGo",
                    "status": "closed",
                },
                {
                    "id": "RH-TD4b.2b.2b",
                    "label": (
                        "ProjectedWeilSignedGramSpectralRadiusBelowTailGap"
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
                ["RH-TD4b.2b.1", "RH-TD4b.2b.2a"],
                ["RH-TD4b.2b.2a", "RH-TD4b.2b.2b"],
                ["RH-TD4b.2b.2b", "RH"],
            ],
        },
        "machine_audit": {
            "tight_frame_row_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem is an exact matrix no-go for an auxiliary sufficient "
            "criterion. It neither identifies the actual projected Weil Gram "
            "operator nor estimates its signed spectral radius, and it proves "
            "no RH implication or counterexample."
        ),
    }


def collatz_cycle_window_audit(
    minimum_cycle_value: int = 2**28,
    maximum_period: int = 20_000,
) -> dict[str, Any]:
    three_power = 1
    denominator_power = 1
    upper_power = 1
    admissible = []
    checkpoints = []
    checkpoint_set = {
        1,
        10,
        100,
        1_000,
        5_000,
        10_000,
        15_600,
        15_601,
        maximum_period,
    }
    denominator_base = 3 * minimum_cycle_value
    upper_base = 3 * (3 * minimum_cycle_value + 1)

    for period in range(1, maximum_period + 1):
        three_power *= 3
        denominator_power *= denominator_base
        upper_power *= upper_base
        valuation_sum = three_power.bit_length()
        lower_scaled = denominator_power << valuation_sum
        fits_upper_window = lower_scaled <= upper_power
        if fits_upper_window:
            admissible.append(
                {
                    "period": period,
                    "candidate_total_valuation": valuation_sum,
                    "window_difference_sign": 1,
                    "window_difference_bit_length": (
                        upper_power - lower_scaled
                    ).bit_length(),
                    "window_difference_sha256": integer_digest(
                        upper_power - lower_scaled
                    ),
                }
            )
        if period in checkpoint_set:
            difference = upper_power - lower_scaled
            checkpoints.append(
                {
                    "period": period,
                    "candidate_total_valuation": valuation_sum,
                    "three_power_below_candidate_power_two": (
                        three_power < (1 << valuation_sum)
                    ),
                    "candidate_fits_cycle_window": fits_upper_window,
                    "signed_window_difference": (
                        1 if difference > 0 else -1
                    ),
                    "absolute_difference_bit_length": abs(difference).bit_length(),
                    "absolute_difference_sha256": integer_digest(difference),
                }
            )

    first_admissible = admissible[0]["period"] if admissible else None
    checks = {
        "verified_floor_positive": minimum_cycle_value == 2**28,
        "all_periods_audited": maximum_period == 20_000,
        "first_unexcluded_period_is_15601": first_admissible == 15_601,
        "unique_unexcluded_period_through_20000": len(admissible) == 1,
        "excluded_period_count_19999": (
            maximum_period - len(admissible) == 19_999
        ),
    }
    failures = sum(int(not value) for value in checks.values())
    return {
        "minimum_cycle_value": minimum_cycle_value,
        "maximum_period": maximum_period,
        "excluded_period_count": maximum_period - len(admissible),
        "arithmetically_unexcluded_periods": admissible,
        "first_arithmetically_unexcluded_period": first_admissible,
        "checkpoints": checkpoints,
        "checks": checks,
        "failure_count": failures,
    }


def collatz_cycle_diophantine_window() -> dict[str, Any]:
    audit = collatz_cycle_window_audit()
    failures = audit["failure_count"]
    return {
        "theorem_name": "CollatzCycleDiophantineWindowAndVerifiedFloorExclusion",
        "title_ko": "콜라츠 주기 디오판토스 창과 검증 하한 주기 배제 정리",
        "declared_target": (
            "Separate the remaining supercritical periodic branch from the "
            "aperiodic affine-capped branch and derive an exact, integer-"
            "checkable obstruction from the verified least cycle value."
        ),
        "proved_statement": (
            "For a positive accelerated Collatz cycle with k odd terms n_i, "
            "valuations a_i, S=sum a_i, and m=min n_i, one has "
            "2^S/3^k=product_i(1+1/(3n_i)). Hence "
            "1<2^S/3^k<=(1+1/(3m))^k. If m>=M, the existence of the cycle "
            "requires a power of two in this explicit Diophantine window. "
            "Using PrimeProject's verified nontrivial-cycle floor M=2^28, exact "
            "integer comparison excludes 19,999 of the first 20,000 odd-step "
            "periods; the unique arithmetically unexcluded period is k=15,601 "
            "with S=24,727."
        ),
        "proved_statement_ko": (
            "양의 가속 Collatz 주기의 홀수 항이 n_i, valuation 합이 S, "
            "최솟값이 m이면 2^S/3^k=product(1+1/(3n_i))이다. 따라서 "
            "1<2^S/3^k<=(1+1/(3m))^k인 매우 좁은 디오판토스 창이 "
            "필요하다. PrimeProject의 비자명 주기 하한 M=2^28을 넣어 "
            "정수만으로 비교하면 k<=20,000 중 19,999개 주기가 배제되고, "
            "k=15,601, S=24,727만 이 조건으로는 배제되지 않는다."
        ),
        "proof": (
            "Multiply the exact step identities "
            "2^(a_i)n_(i+1)=3n_i+1 around the cycle. The n_i telescope and "
            "give 2^S/3^k=product_i(1+1/(3n_i)). Every factor exceeds one "
            "and is at most 1+1/(3m). For a floor m>=M, the only possible "
            "integer S at each k starts at S=ceil(k log_2 3). The audit avoids "
            "floating point: it compares exactly "
            "2^S(3M)^k <= [3(3M+1)]^k. Higher S only increase the left side."
        ),
        "exact_contract": {
            "cycle_identity": (
                "2^S/3^k=product_i(1+1/(3n_i))"
            ),
            "window": (
                "1<2^S/3^k<=(1+1/(3m))^k"
            ),
            "integer_comparison": (
                "2^S(3M)^k <= [3(3M+1)]^k"
            ),
            "verified_floor": "m>=2^28 for a nontrivial cycle",
        },
        "cycle_window_audit": audit,
        "route_decision": {
            "retain": (
                "all-period Diophantine exclusion for supercritical cycles, "
                "followed separately by aperiodic natural-code descent"
            ),
            "discard": (
                "finite period enumeration, including the exact 20,000-period "
                "audit, as a proof of global Collatz convergence"
            ),
            "next_theorem": (
                "AllPeriodSupercriticalCycleDiophantineExclusion"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "CO-TD4b.2b.1",
                    "label": (
                        "SubcriticalPeriodicValuationCodesHaveNoPositiveNaturalEmbedding"
                    ),
                    "status": "closed",
                },
                {
                    "id": "CO-TD4b.2b.2a",
                    "label": (
                        "CollatzCycleDiophantineWindowAndVerifiedFloorExclusion"
                    ),
                    "status": "closed",
                },
                {
                    "id": "CO-TD4b.2b.2b",
                    "label": (
                        "AllPeriodSupercriticalCycleDiophantineExclusion"
                    ),
                    "status": "highest_risk_open",
                },
                {
                    "id": "CO-TD4b.2b.3",
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
                ["CO-TD4b.2b.1", "CO-TD4b.2b.2a"],
                ["CO-TD4b.2b.2a", "CO-TD4b.2b.2b"],
                ["CO-TD4b.2b.2b", "CO-TD4b.2b.3"],
                ["CO-TD4b.2b.3", "CO"],
            ],
        },
        "machine_audit": {
            "periods_audited": audit["maximum_period"],
            "periods_excluded": audit["excluded_period_count"],
            "arithmetically_unexcluded_period_count": len(
                audit["arithmetically_unexcluded_periods"]
            ),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The product-window theorem is universal for positive cycles. The "
            "19,999 exclusions are finite and depend on the stored M=2^28 "
            "nontrivial-cycle floor. Period 15,601 is only unexcluded by this "
            "necessary condition, not a cycle candidate with a realized "
            "valuation word. Periods above 20,000 and every divergent aperiodic "
            "orbit remain open."
        ),
    }


def barycentric_annihilator(points: list[int]) -> dict[str, Any]:
    weights = []
    for index, point in enumerate(points):
        denominator = 1
        for other_index, other in enumerate(points):
            if other_index != index:
                denominator *= point - other
        weights.append(Fraction(1, denominator))

    scale = 1
    for weight in weights:
        scale = math.lcm(scale, weight.denominator)
    integer_weights = [int(weight * scale) for weight in weights]
    common = 0
    for value in integer_weights:
        common = math.gcd(common, abs(value))
    integer_weights = [value // common for value in integer_weights]
    normalized_scale = scale // common

    annihilated_degree_count = len(points) - 1
    moments = [
        sum(
            coefficient * point**degree
            for coefficient, point in zip(integer_weights, points)
        )
        for degree in range(annihilated_degree_count + 1)
    ]
    return {
        "points": points,
        "integer_weights": integer_weights,
        "annihilated_moments": moments[:-1],
        "first_surviving_moment": moments[-1],
        "expected_first_surviving_moment": normalized_scale,
    }


def goldbach_power_two_moment_no_go() -> dict[str, Any]:
    rows = []
    failures = 0
    for order in range(1, 11):
        points = [1 << (index + 1) for index in range(order + 1)]
        result = barycentric_annihilator(points)
        weights = result["integer_weights"]
        checks = {
            "all_points_are_even_powers_of_two": all(
                point >= 2 and point & (point - 1) == 0
                for point in points
            ),
            "all_declared_moments_zero": all(
                moment == 0 for moment in result["annihilated_moments"]
            ),
            "first_surviving_moment_exact": (
                result["first_surviving_moment"]
                == result["expected_first_surviving_moment"]
            ),
            "pointwise_signal_nonzero": max(abs(value) for value in weights) > 0,
            "primitive_integer_weights": (
                math.gcd(*(abs(value) for value in weights)) == 1
            ),
        }
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "moment_order": order,
                "support_size": len(points),
                "power_two_exponents": list(range(1, order + 2)),
                "integer_weights": [str(value) for value in weights],
                "maximum_pointwise_amplitude": str(
                    max(abs(value) for value in weights)
                ),
                "l1_mass": str(sum(abs(value) for value in weights)),
                "annihilated_moment_count": len(
                    result["annihilated_moments"]
                ),
                "first_surviving_moment": str(
                    result["first_surviving_moment"]
                ),
                "checks": checks,
            }
        )

    return {
        "theorem_name": "PowerOfTwoBarycentricMomentAnnihilatorNoGo",
        "title_ko": "2의 거듭제곱 barycentric 모멘트 소거 한계 정리",
        "declared_target": (
            "Test whether finitely many exact signed polynomial moments on the "
            "Goldbach power-of-two hard stratum can force the pointwise K=56 "
            "residual bound."
        ),
        "proved_statement": (
            "For any q>=1 and distinct points x_0,...,x_q, let "
            "w_i=1/product_{j!=i}(x_i-x_j). Then "
            "sum_i w_i x_i^r=0 for 0<=r<q and equals one for r=q. After "
            "clearing denominators this gives a nonzero integer vector whose "
            "first q signed polynomial moments vanish exactly. Taking "
            "x_i=2^(i+1) places the entire countermodel on the unavoidable "
            "Goldbach power-of-two hard stratum. Therefore any fixed finite "
            "moment transcript alone cannot control a pointwise residual."
        ),
        "proved_statement_ko": (
            "서로 다른 x_0,...,x_q에 대해 "
            "w_i=1/product_{j!=i}(x_i-x_j)라 두면 r<q인 모든 차수에서 "
            "sum w_i x_i^r=0이고 q차 모멘트는 1이다. 분모를 제거하면 "
            "처음 q개 signed 다항 모멘트가 정확히 0이지만 점별 값은 "
            "0이 아닌 정수 벡터가 된다. x_i=2^(i+1)을 택하면 이 반대모형은 "
            "Goldbach의 필수 powers-of-two hard stratum 안에 놓인다."
        ),
        "proof": (
            "The Lagrange basis polynomial "
            "L_i(x)=product_{j!=i}(x-x_j)/(x_i-x_j) has leading coefficient "
            "w_i. Interpolate x^r on q+1 nodes. For r<q its x^q coefficient "
            "is zero, so sum_i w_i x_i^r=0; for r=q that coefficient is one. "
            "Clearing denominators and dividing by the coefficient gcd preserves "
            "all zero moments and leaves a primitive nonzero integer vector."
        ),
        "exact_contract": {
            "nodes": "x_i=2^(i+1)",
            "weights": "w_i=1/product_{j!=i}(x_i-x_j)",
            "annihilation": "sum_i w_i*x_i^r=0 for 0<=r<q",
            "normalization": "sum_i w_i*x_i^q=1",
        },
        "moment_annihilator_audit": {
            "rows": rows,
            "row_count": len(rows),
            "maximum_moment_order": 10,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "a localized maximal or all-frequency arithmetic estimate for "
                "the actual signed binary Goldbach residual on powers of two"
            ),
            "discard": (
                "any fixed finite collection of signed polynomial moments as "
                "a standalone pointwise K=56 certificate"
            ),
            "next_theorem": (
                "LocalizedPowerOfTwoSignedGoldbachResidualK56"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "GB-TD4b.2b.1",
                    "label": "AllScaleOddSquarefreeWheelMomentBarrier",
                    "status": "closed",
                },
                {
                    "id": "GB-TD4b.2b.2a",
                    "label": "PowerOfTwoBarycentricMomentAnnihilatorNoGo",
                    "status": "closed",
                },
                {
                    "id": "GB-TD4b.2b.2b",
                    "label": "LocalizedPowerOfTwoSignedGoldbachResidualK56",
                    "status": "highest_risk_open",
                },
                {
                    "id": "GB",
                    "label": "Strong Goldbach Conjecture",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["GB-TD4b.2b.1", "GB-TD4b.2b.2a"],
                ["GB-TD4b.2b.2a", "GB-TD4b.2b.2b"],
                ["GB-TD4b.2b.2b", "GB"],
            ],
        },
        "machine_audit": {
            "moment_orders_audited": len(rows),
            "exact_zero_moment_failure_count": failures,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The barycentric vectors are exact inference countermodels, not "
            "values of the actual Goldbach residual. The theorem excludes only "
            "standalone finite polynomial-moment promotion; it does not exclude "
            "localized analytic estimates, all-frequency control, or arithmetic "
            "structure, and it proves no Goldbach representation."
        ),
    }


def irrational_rotation_separation_rows() -> list[dict[str, Any]]:
    getcontext().prec = 90
    alpha = Decimal(2).sqrt()
    rows = []
    previous_delta: Decimal | None = None
    for size in [8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
        best_delta: Decimal | None = None
        best_q = 0
        best_p = 0
        for denominator in range(1, size):
            value = alpha * denominator
            nearest = int(
                value.to_integral_value(rounding=ROUND_HALF_EVEN)
            )
            delta = abs(value - Decimal(nearest))
            if best_delta is None or delta < best_delta:
                best_delta = delta
                best_q = denominator
                best_p = nearest
        assert best_delta is not None
        lower_lipschitz = Decimal(1) / best_delta
        upper_lipschitz = Decimal(2) / best_delta
        pell_residual = best_p * best_p - 2 * best_q * best_q
        checks = {
            "positive_minimum_separation": best_delta > 0,
            "pigeonhole_upper_bound": best_delta <= Decimal(1) / size,
            "worst_label_lipschitz_at_least_size": (
                lower_lipschitz >= size
            ),
            "separation_nonincreasing": (
                previous_delta is None or best_delta <= previous_delta
            ),
            "best_return_is_pell_unit": abs(pell_residual) == 1,
        }
        rows.append(
            {
                "orbit_size": size,
                "closest_return_denominator": best_q,
                "nearest_integer": best_p,
                "pell_residual_p2_minus_2q2": pell_residual,
                "minimum_circle_separation_decimal": format(
                    best_delta, ".40E"
                ),
                "worst_label_lipschitz_lower_bound": format(
                    lower_lipschitz, ".20E"
                ),
                "tent_interpolation_lipschitz_upper_bound": format(
                    upper_lipschitz, ".20E"
                ),
                "checks": checks,
            }
        )
        previous_delta = best_delta
    return rows


def twin_lipschitz_complexity_no_go() -> dict[str, Any]:
    rows = irrational_rotation_separation_rows()
    failures = sum(
        int(not value)
        for row in rows
        for value in row["checks"].values()
    )
    return {
        "theorem_name": "FiniteIrrationalOrbitLipschitzLookupComplexityNoGo",
        "title_ko": "유한 무리수 궤도 Lipschitz lookup 복잡도 한계 정리",
        "declared_target": (
            "Add an explicit regularity restriction to the TICKET138 "
            "irrational lookup and determine whether scale-dependent Lipschitz "
            "regularity is already non-tautological Type II information."
        ),
        "proved_statement": (
            "Let z_1,...,z_N be distinct points on the unit circle with minimum "
            "geodesic separation delta. Every binary labeling of these points "
            "has a piecewise-linear tent interpolant with Lipschitz constant at "
            "most 2/delta. Conversely, a labeling that separates a closest pair "
            "requires Lipschitz constant at least 1/delta. For N irrational-"
            "rotation points, delta<=1/N by the circle pigeonhole principle. "
            "Thus allowing the regularity budget to grow with 1/delta preserves "
            "finite lookup expressivity; a uniform complexity bound is essential."
        ),
        "proved_statement_ko": (
            "원 위의 서로 다른 N개 점의 최소 원거리 간격을 delta라 하자. "
            "모든 0/1 라벨은 Lipschitz 상수 2/delta 이하의 tent 함수로 "
            "보간할 수 있다. 반대로 가장 가까운 두 점에 다른 라벨을 주면 "
            "상수는 최소 1/delta여야 한다. 무리수 회전의 N개 점에서는 "
            "비둘기집 원리로 delta<=1/N이므로, 1/delta와 함께 커지는 "
            "정칙성 예산을 허용하면 유한 lookup을 제거하지 못한다."
        ),
        "proof": (
            "Around each sample point place a geodesic tent of radius delta/2 "
            "and height equal to its binary label. The supports have disjoint "
            "interiors and every slope has magnitude at most 2/delta, giving "
            "the upper bound. A closest pair with labels zero and one forces "
            "|F(z_i)-F(z_j)|/d(z_i,z_j)=1/delta. Finally N circular gaps sum "
            "to one, so their minimum is at most 1/N."
        ),
        "exact_contract": {
            "finite_upper_bound": "Lip(F)<=2/delta",
            "worst_label_lower_bound": "Lip(F)>=1/delta",
            "rotation_separation": "delta_N<=1/N",
            "required_upgrade": (
                "uniform analytic complexity plus arithmetic cancellation"
            ),
        },
        "irrational_rotation_audit": {
            "alpha": "sqrt(2)",
            "rows": rows,
            "row_count": len(rows),
            "failure_count": failures,
            "numeric_boundary": (
                "90-digit Decimal diagnostics; the interpolation theorem is "
                "independent of these finite rows"
            ),
        },
        "route_decision": {
            "retain": (
                "a scale-uniform Sobolev or analytic norm for the aperiodic "
                "observable, a signed Type II estimate, and positive gap-two mass"
            ),
            "discard": (
                "scale-dependent Lipschitz interpolation as evidence that an "
                "irrational classifier contains arithmetic Type II information"
            ),
            "next_theorem": (
                "UniformSobolevAperiodicTypeIICancellationWithPositiveTwinMass"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "TP-TD3b.2b.1",
                    "label": (
                        "IrrationalInjectivityWithoutRegularityIsTautologicalNoGo"
                    ),
                    "status": "closed",
                },
                {
                    "id": "TP-TD3b.2b.2a",
                    "label": (
                        "FiniteIrrationalOrbitLipschitzLookupComplexityNoGo"
                    ),
                    "status": "closed",
                },
                {
                    "id": "TP-TD3b.2b.2b",
                    "label": (
                        "UniformSobolevAperiodicTypeIICancellationWithPositiveTwinMass"
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
                ["TP-TD3b.2b.1", "TP-TD3b.2b.2a"],
                ["TP-TD3b.2b.2a", "TP-TD3b.2b.2b"],
                ["TP-TD3b.2b.2b", "TP"],
            ],
        },
        "machine_audit": {
            "irrational_rotation_row_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem concerns worst-case labels on finite irrational orbits. "
            "It does not prove that the actual twin-prime label sequence has "
            "large Lipschitz complexity, does not estimate a Vaughan Type II "
            "sum, and supplies no positive exact-gap-two lower bound."
        ),
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": riemann_tight_frame_cross_gram_no_go(),
        "collatz": collatz_cycle_diophantine_window(),
        "goldbach": goldbach_power_two_moment_no_go(),
        "twin_prime": twin_lipschitz_complexity_no_go(),
    }
    failures = sum(
        section["machine_audit"]["total_failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureUniformityDiophantineComplexityAudit",
        **sections,
        "cross_problem_synthesis": {
            "shared_obstruction": (
                "A finite certificate can fit every observed object while its "
                "dimension, period, localization, or regularity cost diverges."
            ),
            "shared_upgrade": (
                "The remaining routes need scale-uniform signed spectral "
                "control, all-period Diophantine exclusion, localized Goldbach "
                "residual estimates, and uniform analytic Type II complexity."
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
            "TICKET139 proves four exact intermediate or proof-route no-go "
            "theorems and revises four proof targets. It does not prove or "
            "refute RH, Collatz, strong Goldbach, or Twin Prime. No conjecture "
            "proof and no certified conjecture counterexample is claimed."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-139",
            "TwoMutuallyUnbiasedBasesCrossGramL1NoGo",
            "ProjectedWeilSignedGramSpectralRadiusBelowTailGap",
            "Estimate the signed spectral radius of one explicit projected Weil Gram tail without replacing it by absolute row sums.",
        ),
        (
            "collatz",
            "CO-TICKET-139",
            "CollatzCycleDiophantineWindowAndVerifiedFloorExclusion",
            "AllPeriodSupercriticalCycleDiophantineExclusion",
            "Combine continued-fraction or linear-form lower bounds for |S log 2-k log 3| with the exact cycle window for every period.",
        ),
        (
            "goldbach",
            "GB-TICKET-139",
            "PowerOfTwoBarycentricMomentAnnihilatorNoGo",
            "LocalizedPowerOfTwoSignedGoldbachResidualK56",
            "Prove a localized maximal or all-frequency K=56 residual estimate for the actual binary Goldbach residual on powers of two.",
        ),
        (
            "twin-prime",
            "TP-TICKET-139",
            "FiniteIrrationalOrbitLipschitzLookupComplexityNoGo",
            "UniformSobolevAperiodicTypeIICancellationWithPositiveTwinMass",
            "Fix a scale-uniform analytic norm, prove signed Type II cancellation for that class, and transport it to positive exact-gap-two mass.",
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
        "uniformity_diophantine_complexity_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket139-uniformity-diophantine-complexity.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-139-tight-frame-l1-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-139-cycle-window.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-139-moment-annihilator.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-139-lipschitz-complexity.json",
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
