from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from typing import Sequence

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket144_schur_rank_equivalence_variation_adverse_walsh import (
    exact_ldl_pivots,
    hilbert_matrix,
    twin_adverse_row,
    walsh_coefficients_from_counts,
)


GENERATED_AT = "2026-07-26T03:00:00+09:00"
SCHEMA = (
    "primeproject.ticket145-normalization-affine-endpoint-separable-no-go.v1"
)
STATUS = "exact_structural_no_go_theorems_all_conjectures_open"


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    next_name: str,
) -> dict[str, object]:
    rejected_id = f"{problem_code}-T145-REJECTED"
    closed_id = f"{problem_code}-T145-CLOSED"
    open_id = f"{problem_code}-T145-OPEN"
    return {
        "nodes": [
            {
                "id": rejected_id,
                "label": rejected_name,
                "status": "refuted_or_circular",
            },
            {
                "id": closed_id,
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": open_id,
                "label": next_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [rejected_id, closed_id],
            [closed_id, open_id],
        ],
    }


def diagonal_scale(
    matrix: Sequence[Sequence[Fraction]],
    scales: Sequence[Fraction],
) -> list[list[Fraction]]:
    size = len(matrix)
    if len(scales) != size or any(len(row) != size for row in matrix):
        raise ValueError("square matrix and one scale per basis vector required")
    if any(scale == 0 for scale in scales):
        raise ValueError("basis scales must be nonzero")
    return [
        [
            scales[row] * matrix[row][column] * scales[column]
            for column in range(size)
        ]
        for row in range(size)
    ]


def riemann_normalized_schur_audit() -> dict[str, object]:
    hilbert_rows = []
    failures = 0
    for size in range(1, 13):
        matrix = hilbert_matrix(size)
        pivot = exact_ldl_pivots(matrix)[-1]
        diagonal = matrix[-1][-1]
        normalized = pivot / diagonal
        expected = Fraction(1, comb(2 * size - 2, size - 1) ** 2)
        checks = {
            "pivot_positive": pivot > 0,
            "normalized_pivot_positive": normalized > 0,
            "normalized_closed_form": normalized == expected,
            "normalized_at_most_one": 0 < normalized <= 1,
        }
        failures += sum(not value for value in checks.values())
        hilbert_rows.append(
            {
                "dimension": size,
                "last_pivot": fraction_payload(pivot),
                "last_diagonal": fraction_payload(diagonal),
                "normalized_pivot": fraction_payload(normalized),
                "normalized_closed_form": (
                    "1/binom(2N-2,N-1)^2"
                ),
                "checks": checks,
            }
        )

    size = 8
    matrix = hilbert_matrix(size)
    scales = [Fraction(index + 1) for index in range(size)]
    original_pivots = exact_ldl_pivots(matrix)
    scaled_matrix = diagonal_scale(matrix, scales)
    scaled_pivots = exact_ldl_pivots(scaled_matrix)
    scaling_rows = []
    for index, (original, scaled, scale) in enumerate(
        zip(original_pivots, scaled_pivots, scales),
        start=1,
    ):
        original_eta = original / matrix[index - 1][index - 1]
        scaled_eta = (
            scaled / scaled_matrix[index - 1][index - 1]
        )
        checks = {
            "pivot_scales_quadratically": scaled == scale**2 * original,
            "normalized_pivot_is_invariant": scaled_eta == original_eta,
        }
        failures += sum(not value for value in checks.values())
        scaling_rows.append(
            {
                "index": index,
                "basis_scale": fraction_payload(scale),
                "original_pivot": fraction_payload(original),
                "scaled_pivot": fraction_payload(scaled),
                "original_normalized_pivot": fraction_payload(original_eta),
                "scaled_normalized_pivot": fraction_payload(scaled_eta),
                "checks": checks,
            }
        )

    return {
        "scaling_theorem": (
            "For a nested Gram family G and diagonal basis rescaling "
            "D=diag(d_1,...), the nth Schur pivot obeys "
            "delta'_n=|d_n|^2*delta_n."
        ),
        "normalized_invariant": (
            "eta_n=delta_n/G_nn is invariant under every nonzero diagonal "
            "basis rescaling and equals the squared relative distance of "
            "the nth vector from the span of its predecessors."
        ),
        "arbitrary_margin_no_go": (
            "If every delta_n is positive, any prescribed positive pivot "
            "sequence t_n can be obtained by choosing "
            "|d_n|^2=t_n/delta_n. Absolute pivot margins therefore have no "
            "basis-independent meaning."
        ),
        "uniform_normalized_margin_no_go": (
            "Every finite Hilbert section is positive definite, but "
            "eta_N=1/binom(2N-2,N-1)^2 tends to zero. Thus even a uniform "
            "positive normalized margin is not necessary for all-section "
            "positivity."
        ),
        "hilbert_rows": hilbert_rows,
        "scaling_rows": scaling_rows,
        "failure_count": failures,
    }


def v2(value: int) -> int:
    if value <= 0:
        raise ValueError("v2 requires a positive integer")
    return (value & -value).bit_length() - 1


def accelerated_collatz(odd: int) -> int:
    if odd <= 0 or odd % 2 == 0:
        raise ValueError("positive odd input required")
    numerator = 3 * odd + 1
    return numerator >> v2(numerator)


def collatz_piecewise_affine_rank_audit() -> dict[str, object]:
    rows = []
    failures = 0
    moduli = [1, 2, 3, 5, 7, 16, 31, 64]
    multipliers = [1, 2, 4, 8, 16, 32]
    for modulus in moduli:
        for multiplier in multipliers:
            start = 4 * modulus * multiplier - 1
            successor = accelerated_collatz(start)
            expected = 6 * modulus * multiplier - 1
            checks = {
                "valuation_is_one": v2(3 * start + 1) == 1,
                "successor_formula": successor == expected,
                "same_residue_state": (
                    start % modulus == successor % modulus
                ),
                "strict_archimedean_expansion": successor > start,
                "exact_growth_difference": (
                    successor - start == 2 * modulus * multiplier
                ),
            }
            failures += sum(not value for value in checks.values())
            rows.append(
                {
                    "modulus": modulus,
                    "multiplier": multiplier,
                    "start": start,
                    "successor": successor,
                    "shared_residue": start % modulus,
                    "growth_difference": successor - start,
                    "checks": checks,
                }
            )
    return {
        "rank_class": (
            "R(n)=a_r*n+b_r for odd n congruent to r (mod M), with finitely "
            "many coefficients and R bounded below on positive odd integers."
        ),
        "exact_witness_family": (
            "For every M,k>=1, n_(M,k)=4Mk-1 has v2(3n+1)=1 and "
            "T(n)=6Mk-1. Both values are -1 mod M and T(n)-n=2Mk>0."
        ),
        "no_go_proof": (
            "On the residue r=-1 mod M, lower boundedness along arbitrarily "
            "large n forces a_r>=0. If a_r=0, R(T(n))=R(n); if a_r>0, "
            "R(T(n))-R(n)=2Mk*a_r>0. Strict one-step descent is impossible."
        ),
        "scope": (
            "The theorem excludes finite-modulus piecewise-affine, "
            "lower-bounded one-step ranks. It does not exclude nonlinear "
            "unbounded-state ranks, adaptive block descent, or a direct "
            "termination argument."
        ),
        "moduli": moduli,
        "multipliers": multipliers,
        "rows": rows,
        "failure_count": failures,
    }


def is_power_of_two(value: int) -> bool:
    return value > 0 and value & (value - 1) == 0


def conditional_path(
    values: Sequence[Fraction],
    leaf: int,
) -> list[Fraction]:
    size = len(values)
    if not is_power_of_two(size) or not 0 <= leaf < size:
        raise ValueError("a dyadic vector and valid leaf are required")
    depth = size.bit_length() - 1
    means = []
    for level in range(depth + 1):
        width = size >> level
        start = (leaf // width) * width
        means.append(
            sum(values[start : start + width], Fraction()) / width
        )
    return means


def dyadic_level_increment_sums(
    values: Sequence[Fraction],
) -> list[Fraction]:
    size = len(values)
    depth = size.bit_length() - 1
    totals = []
    for level in range(1, depth + 1):
        total = Fraction()
        for leaf in range(size):
            path = conditional_path(values, leaf)
            total += path[level] - path[level - 1]
        totals.append(total)
    return totals


def goldbach_signed_endpoint_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for depth in range(2, 11):
        size = 1 << depth
        background = Fraction(-57, size - 1)
        values = [Fraction(57), *([background] * (size - 1))]
        root_mean = sum(values, Fraction()) / size
        increment_sums = dyadic_level_increment_sums(values)
        endpoint_failures = 0
        for leaf, value in enumerate(values):
            path = conditional_path(values, leaf)
            endpoint = path[0] + sum(
                (
                    path[level] - path[level - 1]
                    for level in range(1, len(path))
                ),
                Fraction(),
            )
            endpoint_failures += int(endpoint != value)
        checks = {
            "root_mean_is_zero": root_mean == 0,
            "every_level_global_increment_sum_is_zero": all(
                value == 0 for value in increment_sums
            ),
            "all_leaf_endpoints_telescope": endpoint_failures == 0,
            "pointwise_K56_fails": max(abs(value) for value in values) > 56,
            "bad_leaf_value_is_57": values[0] == 57,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "depth": depth,
                "size": size,
                "root_mean": fraction_payload(root_mean),
                "bad_leaf_value": fraction_payload(values[0]),
                "other_leaf_value": fraction_payload(background),
                "level_signed_increment_sums": [
                    fraction_payload(value) for value in increment_sums
                ],
                "endpoint_failure_count": endpoint_failures,
                "maximum_absolute_endpoint": 57,
                "checks": checks,
            }
        )
    return {
        "endpoint_equivalence": (
            "For every dyadic vector rho and leaf j, conditional means "
            "telescope exactly: rho_j=mu_root+sum_l Delta_l(j). Hence "
            "max_j|mu_root+sum_l Delta_l(j)|<=56 is exactly the original "
            "pointwise K56 condition, not a weaker bridge."
        ),
        "aggregate_cancellation_identity": (
            "At every level, the sum over all leaves of the signed martingale "
            "increment is zero. This is an automatic conditional-expectation "
            "identity and supplies no pointwise bound."
        ),
        "spike_counterfamily": (
            "On 2^d leaves take rho_0=57 and rho_j=-57/(2^d-1) for j>0. "
            "The root mean and every level aggregate signed increment vanish, "
            "but the first point violates K56."
        ),
        "actual_residual_boundary": (
            "The spike family is not the actual binary Goldbach residual. It "
            "refutes only endpoint renaming and aggregate-cancellation "
            "promotion; a pointwise arithmetic K56 estimate remains open."
        ),
        "rows": rows,
        "failure_count": failures,
    }


def adverse_part(a10: int, a01: int, a11: int) -> int:
    return max(a10, 0) + max(a01, 0) + max(-a11, 0)


def favorable_slack(a10: int, a01: int, a11: int) -> int:
    return max(-a10, 0) + max(-a01, 0) + max(a11, 0)


def twin_separable_majorant_audit() -> dict[str, object]:
    grid_failures = 0
    grid_size = 0
    for a10 in range(-8, 9):
        for a01 in range(-8, 9):
            for a11 in range(-8, 9):
                grid_size += 1
                deficit = a10 + a01 - a11
                majorant = adverse_part(a10, a01, a11)
                slack = favorable_slack(a10, a01, a11)
                grid_failures += int(majorant < deficit)
                grid_failures += int(majorant - deficit != slack)

    actual_rows = []
    failures = grid_failures
    for scale in [1_000, 10_000, 100_000, 1_000_000]:
        source = twin_adverse_row(scale)
        a00 = int(source["A00"])
        a10 = int(source["A10"])
        a01 = int(source["A01"])
        a11 = int(source["A11"])
        deficit = a10 + a01 - a11
        majorant = adverse_part(a10, a01, a11)
        slack = favorable_slack(a10, a01, a11)
        twin_count = int(source["direct_twin_count"])
        checks = {
            "walsh_inversion": 4 * twin_count == a00 - deficit,
            "slack_identity": majorant - deficit == slack,
            "adverse_majorizes_joint_deficit": majorant >= deficit,
        }
        failures += sum(not value for value in checks.values())
        actual_rows.append(
            {
                "X": scale,
                "A00": a00,
                "A10": a10,
                "A01": a01,
                "A11": a11,
                "joint_deficit_C": deficit,
                "adverse_part_B": majorant,
                "favorable_slack_F": slack,
                "direct_twin_count": twin_count,
                "checks": checks,
            }
        )

    counts = [90, 5, 4, 1]
    a00, a10, a01, a11 = walsh_coefficients_from_counts(counts)
    deficit = a10 + a01 - a11
    majorant = adverse_part(a10, a01, a11)
    slack = favorable_slack(a10, a01, a11)
    witness_checks = {
        "twin_class_positive": counts[3] > 0,
        "exact_walsh_inversion": 4 * counts[3] == a00 - deficit,
        "adverse_contraction_fails": majorant > a00,
        "slack_identity": majorant - deficit == slack,
    }
    failures += sum(not value for value in witness_checks.values())
    witness = {
        "category_counts": counts,
        "A00": a00,
        "A10": a10,
        "A01": a01,
        "A11": a11,
        "joint_deficit_C": deficit,
        "adverse_part_B": majorant,
        "favorable_slack_F": slack,
        "direct_twin_count": counts[3],
        "checks": witness_checks,
    }
    return {
        "slack_identity": (
            "For C=A10+A01-A11 and "
            "B=(A10)_+ +(A01)_+ +(-A11)_+, "
            "B-C=(-A10)_+ +(-A01)_+ +(A11)_+=F>=0."
        ),
        "minimal_separable_majorant_theorem": (
            "Let f,g,h:R->[0,infinity) vanish at zero and suppose "
            "f(x)+g(y)+h(z)>=x+y-z for all x,y,z. Setting two variables "
            "to zero forces f(x)>=x_+, g(y)>=y_+, and h(z)>=(-z)_+. "
            "Therefore B is the pointwise-smallest nonnegative separable "
            "majorant of the joint Walsh deficit C."
        ),
        "nonnecessity_no_go": (
            "Counts (90,5,4,1) give (A00,A10,A01,A11)=(100,90,88,82), "
            "C=96 and N--=1, but B=178>A00. Thus adverse-part contraction "
            "is sufficient but not necessary even for positive twin mass. "
            "No separable nonnegative componentwise majorant can be sharper "
            "than B; future work must preserve joint signed cancellation."
        ),
        "grid_audit": {
            "coordinate_range": [-8, 8],
            "triple_count": grid_size,
            "failure_count": grid_failures,
        },
        "actual_rows": actual_rows,
        "synthetic_nonnecessity_witness": witness,
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann_audit = riemann_normalized_schur_audit()
    collatz_audit = collatz_piecewise_affine_rank_audit()
    goldbach_audit = goldbach_signed_endpoint_audit()
    twin_audit = twin_separable_majorant_audit()

    riemann_next = "ExplicitWeilFormCoreNormalizedSchurSignRecurrence"
    collatz_next = "NonlinearLiftClosedCollatzRankBeyondFiniteResidueAffine"
    goldbach_next = "ArithmeticBinaryGoldbachScaleEnvelopeSummableK56"
    twin_next = "IndependentCubicRoughJointWalshTypeIIBound"

    riemann_name = (
        "SchurPivotBasisScalingNoGoAndNormalizedAngleReduction"
    )
    collatz_name = "FiniteModulusPiecewiseAffineCollatzRankNoGo"
    goldbach_name = (
        "SignedMartingaleEndpointEquivalenceAndAggregateCancellationNoGo"
    )
    twin_name = (
        "AdverseWalshSlackIdentityAndMinimalSeparableMajorantNoGo"
    )

    riemann = {
        "theorem_name": riemann_name,
        "declared_target": (
            "Determine which Schur-pivot lower bounds are basis invariant "
            "and whether a uniform normalized pivot margin is necessary."
        ),
        "declared_target_ko": (
            "어떤 Schur pivot 하한이 기저 불변인지, 균일 정규화 pivot "
            "여유가 모든 절단 양성에 필요한지 판정한다."
        ),
        "proved_statement": (
            "Absolute Schur pivots scale quadratically with individual basis "
            "vectors, while eta_n=delta_n/G_nn is invariant. Positive Hilbert "
            "sections have eta_n tending to zero, so neither absolute nor "
            "uniform normalized margins are valid necessary targets."
        ),
        "proved_statement_ko": (
            "절대 Schur pivot은 개별 기저 벡터 배율의 제곱에 따라 "
            "변하지만 eta_n=delta_n/G_nn은 불변이다. Hilbert 양성 "
            "절단에서는 eta_n이 0으로 가므로 절대 하한과 균일 정규화 "
            "하한 모두 필요한 조건이 아니다."
        ),
        "proof": (
            "Diagonal congruence cancels every predecessor scale in the "
            "Schur complement and leaves |d_n|^2. Dividing by the nth "
            "diagonal removes that factor. The exact Hilbert pivot formula "
            "gives eta_n=binom(2n-2,n-1)^(-2), which tends to zero."
        ),
        "normalized_schur_audit": riemann_audit,
        "logical_limit": (
            "No actual Weil form-core Gram entry or all-section sign "
            "recurrence is derived. Hilbert matrices are controls only."
        ),
        "route_decision": {
            "discard": (
                "an unnormalized absolute Schur-pivot lower bound, or a "
                "uniform normalized margin, as a necessary RH certificate"
            ),
            "retain": (
                "derive actual normalized Weil Gram entries and an exact "
                "Schur-sign recurrence without assuming positivity"
            ),
            "next_theorem": riemann_next,
        },
        "proof_boundary": (
            "No RH proof or counterexample. This theorem corrects the "
            "normalization and excludes two overstrong pivot targets."
        ),
        "machine_audit": {
            "row_count": (
                len(riemann_audit["hilbert_rows"])
                + len(riemann_audit["scaling_rows"])
            ),
            "failure_count": riemann_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "RH",
            "UniformAbsoluteOrNormalizedSchurPivotMargin",
            riemann_name,
            riemann_next,
        ),
    }

    collatz = {
        "theorem_name": collatz_name,
        "declared_target": (
            "Test every lower-bounded finite-modulus piecewise-affine "
            "one-step rank using an exact same-state expanding family."
        ),
        "declared_target_ko": (
            "정확한 동일 상태 확장족으로 하방 유계인 모든 유한 modulus별 "
            "affine 1-step rank를 판정한다."
        ),
        "proved_statement": (
            "For every modulus M, no lower-bounded rank "
            "R(n)=a_(n mod M)n+b_(n mod M) strictly decreases on every "
            "accelerated odd Collatz edge."
        ),
        "proved_statement_ko": (
            "모든 modulus M에 대해 R(n)=a_(n mod M)n+b_(n mod M) "
            "형태의 하방 유계 rank는 모든 가속 홀수 Collatz 간선에서 "
            "엄격히 감소할 수 없다."
        ),
        "proof": collatz_audit["no_go_proof"],
        "piecewise_affine_rank_audit": collatz_audit,
        "logical_limit": (
            "The result excludes this finite residue-affine one-step class "
            "only. It neither proves termination nor excludes nonlinear, "
            "history-dependent, or adaptive block ranks."
        ),
        "route_decision": {
            "discard": (
                "all finite-modulus piecewise-affine lower-bounded one-step "
                "ranks, including the TICKET144 finite-description affine "
                "candidate"
            ),
            "retain": (
                "a nonlinear lift-closed rank or adaptive block descent that "
                "handles same-residue expanding self-loops"
            ),
            "next_theorem": collatz_next,
        },
        "proof_boundary": (
            "No Collatz proof or counterexample. One broad finite-state "
            "piecewise-affine rank class is refuted exactly."
        ),
        "machine_audit": {
            "row_count": len(collatz_audit["rows"]),
            "failure_count": collatz_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "CO",
            "ExplicitLiftClosedFiniteDescriptionCollatzAffineRank",
            collatz_name,
            collatz_next,
        ),
    }

    goldbach = {
        "theorem_name": goldbach_name,
        "declared_target": (
            "Determine whether signed martingale endpoint cancellation or "
            "levelwise aggregate cancellation is a genuine route to K56."
        ),
        "declared_target_ko": (
            "부호 있는 martingale endpoint 상쇄나 level별 전체 상쇄가 "
            "K56으로 가는 실제 중간정리인지 판정한다."
        ),
        "proved_statement": (
            "The signed endpoint expression is exactly the original "
            "pointwise residual. Levelwise aggregate signed cancellation is "
            "automatic and can coexist with a point of size 57."
        ),
        "proved_statement_ko": (
            "부호 있는 endpoint 식은 원래 점별 잔차와 정확히 같다. "
            "level별 전체 부호 상쇄는 자동 항등식이며 크기 57인 점과도 "
            "동시에 성립할 수 있다."
        ),
        "proof": (
            "Conditional means telescope on each leaf. Summing each level "
            "difference over all leaves gives zero because each child mean "
            "averages to its parent. The exact zero-mean spike family "
            "separates aggregate cancellation from pointwise K56."
        ),
        "signed_endpoint_audit": goldbach_audit,
        "logical_limit": goldbach_audit["actual_residual_boundary"],
        "route_decision": {
            "discard": (
                "renaming the pointwise residual as signed endpoint "
                "cancellation, or using aggregate signed cancellation alone"
            ),
            "retain": (
                "independently prove summable arithmetic envelopes for every "
                "dyadic scale increment of the actual binary residual"
            ),
            "next_theorem": goldbach_next,
        },
        "proof_boundary": (
            "No strong Goldbach proof or counterexample. The theorem exposes "
            "a circular target and an exact aggregate-cancellation no-go."
        ),
        "machine_audit": {
            "row_count": len(goldbach_audit["rows"]),
            "failure_count": goldbach_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "GB",
            "ArithmeticBinaryGoldbachSignedMartingaleCancellationK56",
            goldbach_name,
            goldbach_next,
        ),
    }

    twin_prime = {
        "theorem_name": twin_name,
        "declared_target": (
            "Determine whether adverse Walsh contraction is close to "
            "necessary and whether any sharper separable majorant exists."
        ),
        "declared_target_ko": (
            "adverse Walsh 수축이 필요조건에 가까운지, 더 날카로운 "
            "separable majorant가 존재하는지 판정한다."
        ),
        "proved_statement": (
            "The adverse part B is the pointwise-smallest nonnegative "
            "separable majorant of the joint deficit C, yet B<A00 is not "
            "necessary for positive twin mass."
        ),
        "proved_statement_ko": (
            "adverse part B는 joint deficit C의 점별 최소 비음수 separable "
            "majorant이지만 B<A00은 twin 질량 양성의 필요조건이 아니다."
        ),
        "proof": (
            "The exact slack identity proves B>=C. Testing one coordinate at "
            "a time forces every nonnegative separable majorant to dominate "
            "the three positive parts defining B. Counts (90,5,4,1) then "
            "give positive twin mass while B>A00."
        ),
        "separable_majorant_audit": twin_audit,
        "logical_limit": (
            "The exact joint deficit C<A00 is itself equivalent to positive "
            "twin mass. Progress now requires an independent arithmetic "
            "Type I/II estimate that preserves joint cancellation."
        ),
        "route_decision": {
            "discard": (
                "uniform adverse-part contraction and every nonnegative "
                "separable componentwise Walsh majorant as the primary target"
            ),
            "retain": (
                "a joint signed cubic-rough Type I/II estimate derived "
                "without using the twin count it must lower-bound"
            ),
            "next_theorem": twin_next,
        },
        "proof_boundary": (
            "No Twin Prime proof or counterexample. The theorem proves a "
            "minimal-majorant no-go and requires joint arithmetic "
            "cancellation beyond the sieve parity barrier."
        ),
        "machine_audit": {
            "row_count": len(twin_audit["actual_rows"]) + 1,
            "failure_count": twin_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "TP",
            "UniformCubicRoughAdverseWalshPartContraction",
            twin_name,
            twin_next,
        ),
    }

    sections = [riemann, collatz, goldbach, twin_prime]
    total_failures = sum(
        int(section["machine_audit"]["failure_count"])
        for section in sections
    )
    return {
        "theorem_name": (
            "FourConjectureNormalizationAffineEndpointSeparableNoGoAudit"
        ),
        "status": STATUS,
        "proof_boundary": (
            "No conjecture proof or counterexample. TICKET145 proves four "
            "exact structural no-go theorems, rejects four overstrong or "
            "circular TICKET144 targets, and leaves all conjectures open."
        ),
        "riemann": riemann,
        "collatz": collatz,
        "goldbach": goldbach,
        "twin_prime": twin_prime,
        "machine_audit": {
            "exact_theorem_count": 4,
            "rejected_target_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, object]) -> list[dict[str, object]]:
    specifications = [
        (
            "riemann",
            "RH-TICKET-145",
            "basis-invariant normalized Schur audit",
        ),
        (
            "collatz",
            "CO-TICKET-145",
            "finite-modulus piecewise-affine rank no-go",
        ),
        (
            "goldbach",
            "GB-TICKET-145",
            "signed endpoint and aggregate cancellation no-go",
        ),
        (
            "twin-prime",
            "TP-TICKET-145",
            "minimal separable Walsh majorant no-go",
        ),
    ]
    attempts = []
    for problem_id, ticket_id, route in specifications:
        key = problem_id.replace("-", "_")
        section = audit[key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": ticket_id,
                "status": "exact_no_go_theorem_conjecture_open",
                "route": route,
                "bounded_result": {"audit_ref": key},
                "obstruction": section["logical_limit"],
                "candidate_theorem": section["route_decision"][
                    "next_theorem"
                ],
                "next_experiment": section["route_decision"]["retain"],
                "claim_boundary": section["proof_boundary"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, object]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "normalization_affine_endpoint_separable_no_go_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / (
            "data/open-problem/"
            "ticket145-normalization-affine-endpoint-separable-no-go.json"
        ),
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-145-normalized-schur-no-go.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-145-piecewise-affine-rank-no-go.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-145-signed-endpoint-no-go.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-145-separable-majorant-no-go.json"
        ),
    }
    for attempt in attempts:
        problem_id = str(attempt["problem_id"])
        key = problem_id.replace("-", "_")
        write_json(
            paths[problem_id],
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                **attempt,
                "result": audit[key],
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
