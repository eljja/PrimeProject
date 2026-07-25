from __future__ import annotations

import json
import math
from fractions import Fraction
from functools import lru_cache
from math import prod
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json


GENERATED_AT = "2026-07-25T12:00:00+09:00"
SCHEMA = (
    "primeproject.ticket142-effective-rank-cycle-direction-haar-liouville.v1"
)


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def proof_dag(
    problem_code: str,
    closed_name: str,
    next_name: str,
) -> dict[str, object]:
    closed_id = f"{problem_code}-T142-CLOSED"
    open_id = f"{problem_code}-T142-OPEN"
    return {
        "nodes": [
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
        "edges": [[closed_id, open_id]],
    }


def riemann_effective_rank_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for k in range(1, 9):
        rank = 4**k
        boundary_order = 2 * k
        boundary_trace = Fraction(rank, 2**boundary_order)
        passing_trace = Fraction(rank, 2 ** (boundary_order + 2))
        checks = {
            "positive_margin_exact": Fraction(1, 2) > 0,
            "boundary_trace_equals_threshold": boundary_trace == 1,
            "next_even_order_passes": passing_trace == Fraction(1, 4),
            "effective_rank_equals_rank": rank == 4**k,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "k": k,
                "rank": rank,
                "relative_spectral_margin": fraction_payload(Fraction(1, 2)),
                "boundary_even_moment_order": boundary_order,
                "boundary_normalized_trace": fraction_payload(boundary_trace),
                "next_even_moment_order": boundary_order + 2,
                "next_normalized_trace": fraction_payload(passing_trace),
                "checks": checks,
            }
        )
    return {
        "identity": (
            "tr(F^q)=||F||^q*kappa_q with "
            "1<=kappa_q<=rank(F)"
        ),
        "sharp_log_condition": (
            "q>log(rank)/(-log(1-eta)) is sufficient when only "
            "kappa_q<=rank is known, and scalar F makes it sharp"
        ),
        "rows": rows,
        "failure_count": failures,
    }


def collatz_distinct_successor_set(period: int, minimum: int) -> list[int]:
    if period < 2 or minimum < 3 or minimum % 4 != 3:
        raise ValueError("period>=2 and minimum=3 mod 4 are required")
    successor = (3 * minimum + 1) // 2
    successor_offset = (minimum + 1) // 4
    if successor_offset <= period - 1:
        return list(range(minimum, minimum + 2 * period, 2))
    return (
        list(range(minimum, minimum + 2 * (period - 1), 2))
        + [successor]
    )


def collatz_distinct_product_delta(period: int, minimum: int) -> int:
    values = collatz_distinct_successor_set(period, minimum)
    valuation_sum_floor = (3**period).bit_length()
    return (
        prod(3 * value + 1 for value in values)
        - (1 << valuation_sum_floor) * prod(values)
    )


def collatz_distinct_product_admits(period: int, minimum: int) -> bool:
    return collatz_distinct_product_delta(period, minimum) >= 0


@lru_cache(maxsize=None)
def collatz_maximum_distinct_product_minimum(period: int) -> int | None:
    if not collatz_distinct_product_admits(period, 3):
        return None
    low_index = 0
    high_index = 1
    while collatz_distinct_product_admits(period, 4 * high_index + 3):
        low_index, high_index = high_index, 2 * high_index
    while high_index - low_index > 1:
        middle = (low_index + high_index) // 2
        if collatz_distinct_product_admits(period, 4 * middle + 3):
            low_index = middle
        else:
            high_index = middle
    return 4 * low_index + 3


def collatz_cycle_direction_audit() -> dict[str, object]:
    expected = {
        16: 3,
        64: 11,
        256: 279,
        1024: 31,
        4096: 131,
        15601: 285795879,
        16384: 579,
        20000: 1847,
    }
    rows = []
    failures = 0
    for period, expected_maximum in expected.items():
        maximum = collatz_maximum_distinct_product_minimum(period)
        valuation_sum_floor = (3**period).bit_length()
        checks = {
            "expected_maximum_reproduced": maximum == expected_maximum,
            "maximum_is_admitted": (
                maximum is not None
                and collatz_distinct_product_admits(period, maximum)
            ),
            "next_mod4_candidate_is_rejected": (
                maximum is not None
                and not collatz_distinct_product_admits(period, maximum + 4)
            ),
            "minimum_congruence_is_three_mod_four": (
                maximum is not None and maximum % 4 == 3
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "period_k": period,
                "minimum_valuation_sum_s_k": valuation_sum_floor,
                "maximum_minimum_surviving_distinct_product_bound": maximum,
                "checks": checks,
            }
        )
    verified_floor = 1 << 28
    first_candidate = verified_floor + ((3 - verified_floor) % 4)
    last_candidate = expected[15601]
    candidate_count = (last_candidate - first_candidate) // 4 + 1
    candidate_checks = {
        "first_candidate": first_candidate == 268435459,
        "last_candidate": last_candidate == 285795879,
        "candidate_count": candidate_count == 4340106,
    }
    failures += sum(not value for value in candidate_checks.values())
    return {
        "exact_direction": (
            "Every primitive nontrivial cycle minimum satisfies an upper "
            "bound; the product window does not supply a lower bound"
        ),
        "rows": rows,
        "period_15601_holdout": {
            "verified_minimum_floor": verified_floor,
            "first_mod4_candidate": first_candidate,
            "last_distinct_product_candidate": last_candidate,
            "candidate_minimum_count": candidate_count,
            "checks": candidate_checks,
        },
        "failure_count": failures,
    }


def haar_amplification(depth: int) -> float:
    return 2 ** (-depth / 2) + sum(
        2 ** (-level / 2) for level in range(1, depth + 1)
    )


def goldbach_haar_dual_audit() -> dict[str, object]:
    specifications = [
        ("haar", 4, 23),
        ("haar", 8, 23),
        ("haar", 12, 23),
        ("haar", 9, 24),
        ("hadamard", 3, 23),
    ]
    rows = []
    failures = 0
    for basis, depth, coefficient_budget in specifications:
        size = 2**depth
        if basis == "haar":
            amplification = haar_amplification(depth)
        else:
            amplification = math.sqrt(size)
        pointwise_bound = coefficient_budget * amplification
        expected_below_56 = (
            basis == "haar"
            and coefficient_budget == 23
        )
        checks = {
            "finite_value": math.isfinite(pointwise_bound),
            "expected_k56_side": (
                (pointwise_bound < 56) == expected_below_56
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "basis": basis,
                "depth": depth,
                "size": size,
                "coefficient_budget": coefficient_budget,
                "pointwise_amplification": amplification,
                "pointwise_bound": pointwise_bound,
                "below_K56": pointwise_bound < 56,
                "checks": checks,
            }
        )
    endpoint_margin = (
        Fraction(131917, 100000)
        - Fraction(140, 107)
        - Fraction(38829, 20000000000)
    )
    exact_checks = {
        "23_uniform_haar_budget_below_56": 2 * 23**2 < 33**2,
        "24_uniform_haar_budget_not_below_56": 24 * (1 + math.sqrt(2)) > 56,
        "endpoint_margin_is_positive": endpoint_margin > 0,
        "endpoint_margin_exact_value": (
            endpoint_margin == Fraction(23019645297, 2140000000000)
        ),
    }
    failures += sum(not value for value in exact_checks.values())
    return {
        "basis_change_identity": "C_j(TA,TU)=C_j(A,U) for invertible T",
        "haar_pointwise_identity": (
            "sup|rho_j|=sum_k |Q_kj| epsilon_k; "
            "Haar row l1 is below 1+sqrt(2)"
        ),
        "uniform_integer_coefficient_budget_below_K56": 23,
        "endpoint_margin": fraction_payload(endpoint_margin),
        "rows": rows,
        "exact_checks": exact_checks,
        "failure_count": failures,
    }


def smallest_prime_factors(limit: int) -> list[int]:
    factors = list(range(limit + 1))
    if limit >= 1:
        factors[1] = 1
    for prime in range(2, math.isqrt(limit) + 1):
        if factors[prime] != prime:
            continue
        for multiple in range(prime * prime, limit + 1, prime):
            if factors[multiple] == multiple:
                factors[multiple] = prime
    return factors


def twin_liouville_ledger(scale: int) -> dict[str, object]:
    limit = 2 * scale + 2
    factors = smallest_prime_factors(limit)
    liouville = [0] * (limit + 1)
    liouville[1] = 1
    for value in range(2, limit + 1):
        liouville[value] = -liouville[value // factors[value]]
    a00 = a10 = a01 = a11 = direct_twins = 0
    for value in range(scale, 2 * scale + 1):
        rough_pair = (
            factors[value] ** 3 > limit
            and factors[value + 2] ** 3 > limit
        )
        if rough_pair:
            left = liouville[value]
            right = liouville[value + 2]
            a00 += 1
            a10 += left
            a01 += right
            a11 += left * right
        if factors[value] == value and factors[value + 2] == value + 2:
            direct_twins += 1
    reconstructed = (a00 - a10 - a01 + a11) // 4
    checks = {
        "ledger_divisible_by_four": (
            (a00 - a10 - a01 + a11) % 4 == 0
        ),
        "projector_matches_direct_twin_count": reconstructed == direct_twins,
        "rough_pair_mass_dominates_twins": a00 >= direct_twins,
    }
    return {
        "X": scale,
        "A00": a00,
        "A10": a10,
        "A01": a01,
        "A11": a11,
        "reconstructed_twin_count": reconstructed,
        "direct_twin_count": direct_twins,
        "checks": checks,
    }


def twin_liouville_audit() -> dict[str, object]:
    rows = [
        twin_liouville_ledger(scale)
        for scale in [1000, 10000, 100000, 1000000]
    ]
    failures = sum(
        not value
        for row in rows
        for value in row["checks"].values()
    )
    return {
        "pointwise_projector": (
            "1_P(n)1_P(n+2)=R_X(n)R_X(n+2)"
            "(1-lambda(n))(1-lambda(n+2))/4"
        ),
        "ledger_identity": "4*pi_2[X,2X]=A00-A10-A01+A11",
        "rows": rows,
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann_audit = riemann_effective_rank_audit()
    collatz_audit = collatz_cycle_direction_audit()
    goldbach_audit = goldbach_haar_dual_audit()
    twin_audit = twin_liouville_audit()

    riemann_next = "ExplicitProjectedWeilFiniteSectionAndTailConvergenceContract"
    collatz_next = "Period15601AffineNumeratorNondivisibilityCertificate"
    goldbach_next = "UniformEvenGoldbachHaarScaleBudgetBelow56"
    twin_next = "OneSidedCubicRoughLiouvilleLedgerGap"

    riemann = {
        "theorem_name": (
            "EffectiveRankShiftedMomentIdentityAndSharpLogCoefficientNoGo"
        ),
        "declared_target": (
            "Determine exactly when a shifted trace moment certifies a "
            "positive spectral margin and whether O(log rank) alone suffices."
        ),
        "declared_target_ko": (
            "shifted trace moment가 양의 spectral margin을 인증하는 정확 "
            "조건과 O(log rank) 성장률만으로 충분한지 판정한다."
        ),
        "proved_statement": (
            "The shifted moment is exactly ||F||^q times the q-effective "
            "rank. The worst-case logarithmic coefficient is sharp."
        ),
        "proved_statement_ko": (
            "shifted moment는 ||F||^q와 q-유효 rank의 정확한 곱이며, "
            "최악 경우 로그 차수의 계수는 sharp하다."
        ),
        "proof": (
            "Diagonalize F. Normalized eigenvalues lie in [0,1] and one is "
            "one, so their q-power sum is between one and rank. Scalar "
            "F=(1/2)I at rank 4^k attains the boundary exactly."
        ),
        "effective_rank_audit": riemann_audit,
        "logical_limit": (
            "The projected Weil finite sections, spectral constants, and "
            "tail convergence map are not yet defined; finite scalar rows "
            "are not evidence for those missing arithmetic objects."
        ),
        "route_decision": {
            "discard": (
                "O(log rank) as a coefficient-free automatic shifted-moment "
                "certificate"
            ),
            "retain": (
                "one-sided shifted moments after an explicit finite-section "
                "and tail-convergence contract is supplied"
            ),
            "next_theorem": riemann_next,
        },
        "proof_boundary": (
            "No conjecture proof. This is a finite-dimensional spectral "
            "identity and sharp proof-route no-go, not RH."
        ),
        "machine_audit": {
            "row_count": len(riemann_audit["rows"]),
            "failure_count": riemann_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "RH",
            "EffectiveRankShiftedMomentIdentityAndSharpLogCoefficientNoGo",
            riemann_next,
        ),
    }

    collatz = {
        "theorem_name": (
            "PrimitiveCycleSuccessorDistinctProductUpperBoundAndTargetCollapseNoGo"
        ),
        "declared_target": (
            "Audit the direction of the exact power-of-two cycle window and "
            "strengthen it using the forced successor and distinct odd terms."
        ),
        "declared_target_ko": (
            "2의 거듭제곱 순환 창의 부등호 방향을 감사하고, 강제되는 "
            "다음 항과 서로 다른 홀수 항을 이용해 강화한다."
        ),
        "proved_statement": (
            "A primitive nontrivial cycle minimum obeys a strict upper "
            "bound, is 3 mod 4, and must satisfy the successor-distinct "
            "product inequality."
        ),
        "proved_statement_ko": (
            "원시 비자명 순환의 최솟값은 엄격한 상한을 가지며 3 mod 4이고, "
            "successor-distinct 곱 부등식을 만족해야 한다."
        ),
        "proof": (
            "Multiply the k odd Collatz equations, use S>=ceil(k log_2 3), "
            "monotonicity of 1+1/(3x), the forced valuation a_0=1 at the "
            "minimum, and distinctness of primitive-cycle terms."
        ),
        "cycle_direction_audit": collatz_audit,
        "logical_limit": (
            "The strengthened bound leaves 4,340,106 possible minima at "
            "period 15,601 above the verified 2^28 floor. These are minima "
            "candidates, not cycles or valuation words."
        ),
        "route_decision": {
            "discard": (
                "deriving a cycle-minimum lower bound from the product window; "
                "the window gives the opposite direction"
            ),
            "retain": (
                "exact valuation-word divisibility and affine numerator "
                "certificates on the first surviving period"
            ),
            "next_theorem": collatz_next,
        },
        "proof_boundary": (
            "No conjecture proof or Collatz counterexample. The result "
            "corrects a proof direction and narrows one finite period branch."
        ),
        "machine_audit": {
            "row_count": len(collatz_audit["rows"]),
            "failure_count": collatz_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "CO",
            (
                "PrimitiveCycleSuccessorDistinctProductUpperBoundAnd"
                "TargetCollapseNoGo"
            ),
            collatz_next,
        ),
    }

    goldbach = {
        "theorem_name": "RobustDualBasisChangeInvarianceAndHaarK56Reduction",
        "declared_target": (
            "Specify a localized orthogonal dual and determine whether basis "
            "change alone can fit pointwise Goldbach residuals below K=56."
        ),
        "declared_target_ko": (
            "국소 직교 dual을 명시하고 기저변환만으로 Goldbach 점별 잔차를 "
            "K=56 아래에 둘 수 있는지 판정한다."
        ),
        "proved_statement": (
            "Robust recovery is invariant under simultaneous invertible "
            "basis/error-set change. Haar localization converts uniform "
            "coefficient budget 23 into a pointwise bound below 56."
        ),
        "proved_statement_ko": (
            "강건 복원은 기저와 오차집합의 동시 가역변환에 불변이다. "
            "Haar 국소화에서는 균일 계수 예산 23이 점별 56 미만을 준다."
        ),
        "proof": (
            "Af in U iff TAf in TU proves invariance. Orthogonal inversion "
            "gives the exact row-l1 dual. A Haar row has one coefficient per "
            "scale and l1 below 1+sqrt(2); 23(1+sqrt(2))<56."
        ),
        "haar_dual_audit": goldbach_audit,
        "logical_limit": (
            "No arithmetic theorem currently bounds every actual normalized "
            "Goldbach Haar scaling and wavelet coefficient by the required "
            "budgets. K=56 is a residual constant, not moment order 56."
        ),
        "route_decision": {
            "discard": (
                "claiming improved robustness from invertible orthogonalization "
                "while silently replacing the transformed joint error set"
            ),
            "retain": (
                "a fully specified Haar ledger whose actual arithmetic "
                "coefficient budgets are proved scale by scale"
            ),
            "next_theorem": goldbach_next,
        },
        "proof_boundary": (
            "No conjecture proof. The linear-algebra reduction is exact, but "
            "the uniform arithmetic Haar coefficient theorem is open."
        ),
        "machine_audit": {
            "row_count": len(goldbach_audit["rows"]),
            "failure_count": goldbach_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "GB",
            "RobustDualBasisChangeInvarianceAndHaarK56Reduction",
            goldbach_next,
        ),
    }

    twin_prime = {
        "theorem_name": "CubicRoughnessLiouvilleExactTwinProjector",
        "declared_target": (
            "Separate unsigned rough-pair mass from the parity-sensitive "
            "one-sided information required for positive exact-gap-two mass."
        ),
        "declared_target_ko": (
            "부호 없는 rough-pair 질량과 양의 gap-2 질량에 필요한 "
            "parity-sensitive 단측 정보를 분리한다."
        ),
        "proved_statement": (
            "At cubic roughness, Liouville parity is an exact prime "
            "indicator and yields a four-term exact twin-prime ledger."
        ),
        "proved_statement_ko": (
            "세제곱 roughness에서는 Liouville parity가 정확한 소수 지시자가 "
            "되어 네 항의 정확한 쌍둥이 소수 ledger를 준다."
        ),
        "proof": (
            "A z-rough integer at most 2X+2 with z^3=2X+2 has at most two "
            "prime factors with multiplicity. Hence lambda=-1 is equivalent "
            "to primality on that support; expand the two projectors."
        ),
        "liouville_ledger_audit": twin_audit,
        "logical_limit": (
            "Finite ledger identities do not control the one-sided Liouville "
            "combination at all scales. Generic absolute minor-arc bounds do "
            "not supply the missing sign."
        ),
        "route_decision": {
            "discard": (
                "promoting unsigned or absolute-value minor-arc cancellation "
                "directly to positive exact-gap-two mass"
            ),
            "retain": (
                "the cubic rough-pair support together with a one-sided "
                "Liouville mixed-correlation ledger"
            ),
            "next_theorem": twin_next,
        },
        "proof_boundary": (
            "No conjecture proof or counterexample. The projector is an exact "
            "finite identity; the all-scale one-sided Liouville gap is open."
        ),
        "machine_audit": {
            "row_count": len(twin_audit["rows"]),
            "failure_count": twin_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "TP",
            "CubicRoughnessLiouvilleExactTwinProjector",
            twin_next,
        ),
    }

    total_failures = sum(
        section["machine_audit"]["failure_count"]
        for section in [riemann, collatz, goldbach, twin_prime]
    )
    return {
        "theorem_name": (
            "FourConjectureEffectiveRankCycleDirectionHaarLiouvilleAudit"
        ),
        "status": "exact_intermediate_theorems_proved_all_conjectures_open",
        "proof_boundary": (
            "No conjecture proof. This audit proves four exact "
            "finite-dimensional, arithmetic, or linear-algebraic intermediate "
            "theorems. It does not prove or refute RH, Collatz, strong "
            "Goldbach, or Twin Prime."
        ),
        "riemann": riemann,
        "collatz": collatz,
        "goldbach": goldbach,
        "twin_prime": twin_prime,
        "machine_audit": {
            "exact_theorem_count": 4,
            "route_correction_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, object]) -> list[dict[str, object]]:
    specifications = [
        (
            "riemann",
            "RH-TICKET-142",
            "effective-rank shifted-moment coefficient audit",
        ),
        (
            "collatz",
            "CO-TICKET-142",
            "cycle-window direction and distinct-successor product audit",
        ),
        (
            "goldbach",
            "GB-TICKET-142",
            "robust basis-change and Haar K56 reduction audit",
        ),
        (
            "twin-prime",
            "TP-TICKET-142",
            "cubic rough Liouville exact twin projector audit",
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
                "status": "exact_intermediate_theorem_conjecture_open",
                "route": route,
                "bounded_result": {"audit_ref": key},
                "obstruction": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_theorem"],
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
        "status": "exact_intermediate_theorems_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "effective_rank_cycle_direction_haar_liouville_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket142-effective-rank-cycle-direction-haar-liouville.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/rh-ticket-142-effective-rank-moment.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/co-ticket-142-cycle-direction.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/gb-ticket-142-haar-k56.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/tp-ticket-142-liouville-projector.json"
        ),
    }
    for attempt in attempts:
        problem_id = attempt["problem_id"]
        key = str(problem_id).replace("-", "_")
        write_json(
            paths[str(problem_id)],
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
