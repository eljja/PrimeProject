from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any, Iterable

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket132_admissibility_nullset_hard_stratum_local_parity import (
    crt,
    first_primes_above,
    fraction_payload,
)
from ticket135_conditional_bridges_and_exceptional_set import (
    first_admissible_residues,
    lcm_many,
)


GENERATED_AT = "2026-07-25T12:00:00+09:00"
SCHEMA = "primeproject.ticket136-scale-sensitive-obstructions-and-affine-bridge.v1"


def ceil_log2(value: int) -> int:
    if value <= 1:
        return 0
    return (value - 1).bit_length()


def riemann_schur_test_bridge() -> dict[str, Any]:
    contracts = [
        (Fraction(2), Fraction(3), Fraction(1), Fraction(2)),
        (Fraction(5, 2), Fraction(4), Fraction(3, 2), Fraction(2)),
        (Fraction(1), Fraction(1), Fraction(1), Fraction(1)),
    ]
    rows = []
    failures = 0
    for alpha, gamma, row_sum, column_sum in contracts:
        margin = alpha * gamma - row_sum * column_sum
        rows.append(
            {
                "alpha": fraction_payload(alpha),
                "gamma": fraction_payload(gamma),
                "maximum_absolute_row_sum": fraction_payload(row_sum),
                "maximum_absolute_column_sum": fraction_payload(column_sum),
                "certified_schur_margin": fraction_payload(margin),
                "certificate_accepts": margin >= 0,
            }
        )
        failures += int(margin < 0)

    entrywise_rows = []
    for dimension in [2, 4, 8, 16, 32, 64, 128]:
        entry = Fraction(1, dimension)
        row_sum = dimension * entry
        column_sum = dimension * entry
        all_ones_norm_ratio = row_sum
        entrywise_rows.append(
            {
                "dimension": dimension,
                "maximum_entry": fraction_payload(entry),
                "maximum_absolute_row_sum": fraction_payload(row_sum),
                "maximum_absolute_column_sum": fraction_payload(column_sum),
                "operator_norm_witness_ratio": fraction_payload(all_ones_norm_ratio),
            }
        )
        failures += int(row_sum != 1 or column_sum != 1 or all_ones_norm_ratio != 1)

    return {
        "theorem_name": "SchurTestWeilBlockBridgeAndEntrywiseDecayNoGo",
        "title_ko": "Schur 검사를 이용한 Weil 블록 연결과 원소별 감소의 한계 정리",
        "declared_target": (
            "Refine the TICKET135 block certificate into computable absolute "
            "row/column tail bounds, and determine whether entrywise decay alone "
            "can supply the missing operator-norm premise."
        ),
        "proved_statement": (
            "Let M=[[A,B],[B*,C]] be self-adjoint, with A>=alpha I and "
            "C>=gamma I. If every absolute row sum of B is at most R and every "
            "absolute column sum is at most S, then ||B||_2^2<=R*S. Hence "
            "R*S<=alpha*gamma implies M>=0. Entrywise decay alone is insufficient: "
            "B_n=J_n/n has max_ij |B_ij|=1/n -> 0 but ||B_n||_2=1 for every n."
        ),
        "proved_statement_ko": (
            "자기수반 블록 M의 코어와 꼬리 하한이 각각 alpha, gamma이고 "
            "교차 블록 B의 절댓값 행합과 열합이 R, S 이하이면 "
            "||B||_2^2<=R*S이다. 따라서 R*S<=alpha*gamma이면 전체 블록은 "
            "양의 준정부호다. 그러나 B_n=J_n/n은 각 원소가 0으로 가면서도 "
            "연산자 노름이 항상 1이므로 원소별 감소만으로는 충분하지 않다."
        ),
        "proof": (
            "The Schur test gives ||B||_2<=sqrt(||B||_infinity*||B||_1)"
            "<=sqrt(R*S). Substitution into the sharp TICKET135 block inequality "
            "proves positivity. For B_n=J_n/n, every row and column sum is one, "
            "and the all-ones vector is an eigenvector with eigenvalue one. Thus "
            "the operator norm remains one although the largest entry tends to zero."
        ),
        "exact_certificate_contract": {
            "finite_core_lower_bound": "A>=alpha I",
            "tail_lower_bound": "C>=gamma I",
            "cross_row_bound": "sup_i sum_j |B_ij|<=R",
            "cross_column_bound": "sup_j sum_i |B_ij|<=S",
            "operator_bound": "||B||_2^2<=R*S",
            "acceptance_inequality": "R*S<=alpha*gamma",
        },
        "rational_audit": {
            "accepted_contracts": rows,
            "entrywise_decay_counterfamily": entrywise_rows,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "absolute row/column summability bounds for the projected Weil "
                "core-tail coupling, combined with certified core and tail gaps"
            ),
            "discard": (
                "deducing a vanishing projected Weil cross-operator norm solely "
                "from entrywise matrix-element decay"
            ),
            "next_theorem": "ProjectedWeilAbsoluteRowColumnTailBoundsWithPositiveMargin",
        },
        "proof_dag": {
            "nodes": [
                {"id": "RH-TD4a", "label": "SharpBlockTailPositivityCertificate", "status": "closed"},
                {"id": "RH-TD4b.1", "label": "SchurTestWeilBlockBridgeAndEntrywiseDecayNoGo", "status": "closed"},
                {
                    "id": "RH-TD4b.2",
                    "label": "ProjectedWeilAbsoluteRowColumnTailBoundsWithPositiveMargin",
                    "status": "highest_risk_open",
                },
                {"id": "RH", "label": "Riemann Hypothesis", "status": "open_not_proven"},
            ],
            "edges": [["RH-TD4a", "RH-TD4b.1"], ["RH-TD4b.1", "RH-TD4b.2"], ["RH-TD4b.2", "RH"]],
        },
        "machine_audit": {
            "accepted_contract_count": len(rows),
            "entrywise_counterfamily_size": len(entrywise_rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The Schur-test bridge and counterfamily are exact. No absolute "
            "row/column estimates are proved here for a fixed published projected "
            "Weil operator, and no tail spectral gap is supplied. RH remains open."
        ),
    }


def v2(value: int) -> int:
    exponent = 0
    while value % 2 == 0:
        value //= 2
        exponent += 1
    return exponent


def accelerated_collatz_step(odd_value: int) -> tuple[int, int]:
    numerator = 3 * odd_value + 1
    valuation = v2(numerator)
    return numerator >> valuation, valuation


def collatz_affine_audit(maximum_start: int = 9999, maximum_depth: int = 64) -> dict[str, Any]:
    failures = 0
    exact_identity_checks = 0
    necessary_cap_checks = 0
    sufficient_threshold_checks = 0
    descended_starts = 0
    selected = {1, 3, 7, 27, 31, 63, 703}
    examples = []

    for start in range(1, maximum_start + 1, 2):
        current = start
        valuation_sum = 0
        correction_product = Fraction(1)
        no_descent_before_step = True
        selected_rows = []
        descended = False
        for depth in range(1, maximum_depth + 1):
            previous = current
            current, valuation = accelerated_collatz_step(previous)
            valuation_sum += valuation
            correction_product *= Fraction(3 * previous + 1, 3 * previous)

            exact_ratio = Fraction(3**depth, 2**valuation_sum) * correction_product
            failures += int(exact_ratio != Fraction(current, start))
            exact_identity_checks += 1

            no_descent_through_step = no_descent_before_step and current >= start
            cap_left = (2**valuation_sum) * (start**depth)
            cap_right = (3 * start + 1) ** depth
            if no_descent_through_step:
                failures += int(cap_left > cap_right)
                necessary_cap_checks += 1

            threshold_crossed = no_descent_before_step and cap_left > cap_right
            if threshold_crossed:
                failures += int(current >= start)
                sufficient_threshold_checks += 1

            if start in selected and (
                depth in {1, 2, 4, 8, 16, 32, 64} or threshold_crossed
            ):
                selected_rows.append(
                    {
                        "depth": depth,
                        "iterate": str(current),
                        "valuation_sum": valuation_sum,
                        "slope_contracts": 2**valuation_sum > 3**depth,
                        "affine_threshold_crossed": threshold_crossed,
                        "strict_descent": current < start,
                    }
                )

            if current < start:
                descended = True
                break
            no_descent_before_step = no_descent_through_step

        descended_starts += int(descended)
        if start in selected:
            examples.append(
                {
                    "start": start,
                    "first_descent_found": descended,
                    "audited_rows": selected_rows,
                }
            )

    fixed_point_rows = []
    for depth in [1, 2, 4, 8, 16, 32]:
        valuation_sum = 2 * depth
        fixed_point_rows.append(
            {
                "depth": depth,
                "valuation_sum": valuation_sum,
                "slope_left_2_pow_S": str(2**valuation_sum),
                "slope_right_3_pow_k": str(3**depth),
                "slope_contracts": 2**valuation_sum > 3**depth,
                "affine_threshold_left": str(2**valuation_sum),
                "affine_threshold_right": str(4**depth),
                "strict_descent": False,
            }
        )
        failures += int(2**valuation_sum <= 3**depth)
        failures += int(2**valuation_sum != 4**depth)

    return {
        "maximum_odd_start": maximum_start,
        "maximum_depth": maximum_depth,
        "odd_start_count": (maximum_start + 1) // 2,
        "descended_start_count": descended_starts,
        "exact_identity_check_count": exact_identity_checks,
        "necessary_cap_check_count": necessary_cap_checks,
        "sufficient_threshold_check_count": sufficient_threshold_checks,
        "selected_examples": examples,
        "slope_only_counterexample_n_equals_1": fixed_point_rows,
        "failure_count": failures,
    }


def collatz_affine_correction_bridge() -> dict[str, Any]:
    audit = collatz_affine_audit()
    return {
        "theorem_name": "LeastCounterexampleAffineCorrectionInequality",
        "title_ko": "최소 반례의 affine 보정 부등식",
        "declared_target": (
            "Replace slope-only contraction by an exact, integer-checkable "
            "criterion that includes the positive affine correction and applies "
            "to a hypothetical least Collatz counterexample."
        ),
        "proved_statement": (
            "For the accelerated odd Collatz orbit n_{j+1}=(3n_j+1)/2^{a_j}, "
            "S_k=sum_{j<k} a_j, one has the exact identity "
            "n_k/n_0=(3^k/2^S_k) product_{j<k}(1+1/(3n_j)). If "
            "n_j>=n_0 for 0<=j<=k, then 2^S_k*n_0^k<=(3n_0+1)^k. "
            "Consequently the strict reverse inequality certifies a descent by "
            "time k. A hypothetical least counterexample must satisfy the "
            "non-strict inequality for every k."
        ),
        "proved_statement_ko": (
            "가속 홀수 콜라츠 궤도는 기울기 항뿐 아니라 "
            "product(1+1/(3n_j))라는 양의 affine 보정항을 정확히 가진다. "
            "k단계 동안 시작값 아래로 내려가지 않았다면 "
            "2^S_k*n_0^k<=(3n_0+1)^k가 반드시 성립한다. 따라서 반대의 "
            "엄격한 부등식은 k단계 이내 하강의 정확한 충분조건이며, 가상의 "
            "최소 반례는 이 부등식을 모든 k에서 위반하지 못한다."
        ),
        "proof": (
            "Multiplying n_{j+1}/n_j=(3/2^{a_j})(1+1/(3n_j)) gives the "
            "identity. Under n_j>=n_0, every correction factor is at most "
            "1+1/(3n_0), so n_k/n_0 is at most "
            "((3n_0+1)/n_0)^k/2^S_k. Non-descent forces this upper bound "
            "to be at least one, which is the displayed integer inequality. "
            "If n_0 were the least counterexample, reaching a smaller positive "
            "integer would join an orbit known by minimality to reach one; hence "
            "its orbit can never descend and the inequality is necessary for all k."
        ),
        "exact_bridge_contract": {
            "iterate_identity": (
                "n_k/n_0=(3^k/2^S_k)*product_{j<k}(1+1/(3n_j))"
            ),
            "no_descent_necessary_condition": "2^S_k*n_0^k<=(3n_0+1)^k",
            "descent_sufficient_condition": "2^S_k*n_0^k>(3n_0+1)^k",
            "log_form": (
                "S_k-k*log_2(3)<=k*log_2(1+1/(3n_0)) under no descent"
            ),
        },
        "finite_orbit_audit": audit,
        "route_decision": {
            "retain": (
                "least-counterexample valuation surplus estimates that dominate "
                "the explicit n-dependent affine correction"
            ),
            "discard": (
                "using 2^S_k>3^k alone as a certificate of strict integer descent"
            ),
            "next_theorem": "UniformValuationSurplusBeyondAffineCorrectionForLeastCounterexampleCodes",
        },
        "proof_dag": {
            "nodes": [
                {"id": "CO-TD4a", "label": "MinimalNegativeSlopePrefixesFormFullMeasurePrefixFreeCover", "status": "closed"},
                {"id": "CO-TD4b.1", "label": "LeastCounterexampleAffineCorrectionInequality", "status": "closed"},
                {
                    "id": "CO-TD4b.2",
                    "label": "UniformValuationSurplusBeyondAffineCorrectionForLeastCounterexampleCodes",
                    "status": "highest_risk_open",
                },
                {"id": "CO", "label": "Collatz Conjecture", "status": "open_not_proven"},
            ],
            "edges": [["CO-TD4a", "CO-TD4b.1"], ["CO-TD4b.1", "CO-TD4b.2"], ["CO-TD4b.2", "CO"]],
        },
        "machine_audit": {
            "exact_identity_check_count": audit["exact_identity_check_count"],
            "necessary_cap_check_count": audit["necessary_cap_check_count"],
            "slope_only_counterexample_verified": True,
            "conjecture_resolution_count": 0,
            "total_failure_count": audit["failure_count"],
        },
        "proof_boundary": (
            "The identity and least-counterexample necessity are universal, but "
            "PrimeProject has not proved that every possible least-counterexample "
            "valuation code eventually exceeds the affine correction. The finite "
            "orbit audit is a replay, not a proof of Collatz."
        ),
    }


def euler_phi(value: int) -> int:
    result = value
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            while remaining % divisor == 0:
                remaining //= divisor
            result -= result // divisor
        divisor += 1
    if remaining > 1:
        result -= result // remaining
    return result


def minimal_moment_for_inflation(size: int, numerator: int = 6, denominator: int = 5) -> int:
    moment = 1
    while numerator**moment < size * denominator**moment:
        moment += 1
    return moment


def count_fixed_wheel_rough_evens(wheel: int, blocks: int) -> int:
    horizon = 2 * wheel * blocks
    return sum(
        1
        for even_value in range(2, horizon + 1, 2)
        if math.gcd(even_value, wheel) == 1
    )


def goldbach_fixed_wheel_barrier() -> dict[str, Any]:
    wheels = [15, 105, 1155, 15015]
    block_counts = [1, 8, 64, 512, 4096]
    rows = []
    failures = 0
    for wheel in wheels:
        phi = euler_phi(wheel)
        direct_count = count_fixed_wheel_rough_evens(wheel, 3)
        failures += int(direct_count != 3 * phi)
        for blocks in block_counts:
            horizon = 2 * wheel * blocks
            hard_size = blocks * phi
            required_moment = minimal_moment_for_inflation(hard_size)
            sparse_guess = 4 * ceil_log2(max(2, ceil_log2(horizon)))
            rows.append(
                {
                    "wheel": wheel,
                    "phi_wheel": phi,
                    "complete_period_blocks": blocks,
                    "horizon": horizon,
                    "rough_even_stratum_size": hard_size,
                    "exact_density_among_evens": fraction_payload(Fraction(phi, wheel)),
                    "minimum_p_for_inflation_at_most_6_over_5": required_moment,
                    "power_only_loglog_moment": sparse_guess,
                    "power_only_moment_is_insufficient": sparse_guess < required_moment,
                }
            )
            failures += int(hard_size != blocks * phi)

    return {
        "theorem_name": "FixedWheelRoughStratumHasLinearMassAndLogMomentBarrier",
        "title_ko": "고정 wheel 거친 층의 선형 크기와 로그 모멘트 장벽",
        "declared_target": (
            "Test whether the O(log log X) moment order obtained for the powers-of-"
            "two stratum in TICKET135 can control the full finite-wheel rough "
            "Goldbach hard stratum."
        ),
        "proved_statement": (
            "Let W be odd and squarefree, and H_W(X)={2<=N<=X: N even, "
            "gcd(N,W)=1}. At X=2WM, |H_W(X)|=M*phi(W), so every fixed-wheel "
            "rough stratum has positive linear density. The sharp normalized "
            "Lp-to-sup factor is h^(1/p); keeping it at most 6/5 requires "
            "p>=log(h)/log(6/5)=Theta(log X). In particular p=O(log log X) "
            "cannot promote arbitrary residual control on H_W(X) to a pointwise "
            "bound. A one-point spike proves the obstruction."
        ),
        "proved_statement_ko": (
            "홀수 squarefree wheel W를 고정하면 W의 작은 소인수를 피하는 짝수 "
            "hard stratum은 X=2WM에서 정확히 M*phi(W)개다. 즉 이 층은 "
            "powers of two처럼 희소하지 않고 X에 선형이다. 정규화 Lp 노름을 "
            "점별 노름으로 올릴 때 필요한 차수는 Theta(log X)이며, "
            "O(log log X)는 한 점 spike조차 검출하지 못한다."
        ),
        "proof": (
            "Write N=2m. In each complete interval of W consecutive m-values, "
            "exactly phi(W) are coprime to W, proving the count. The finite-set "
            "norm inequality from TICKET135 is sharp on a one-point spike and "
            "has inflation h^(1/p). Solving h^(1/p)<=6/5 gives the logarithmic "
            "lower bound on p. Since h is proportional to X for fixed W, every "
            "p=o(log X), including O(log log X), leaves unbounded inflation."
        ),
        "exact_barrier_contract": {
            "hard_stratum": "H_W(X)={N<=X: 2|N and gcd(N,W)=1}",
            "complete_period_count": "|H_W(2WM)|=M*phi(W)",
            "sharp_inflation": "h^(1/p)",
            "minimum_moment": "p>=log(h)/log(6/5)",
            "countermodel": "one residual spike of fixed amplitude on H_W(X)",
        },
        "finite_wheel_audit": {
            "rows": rows,
            "direct_three_period_checks": len(wheels),
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "a growing-wheel stratification with a residual estimate uniform "
                "in both the analytic scale and the wheel level"
            ),
            "discard": (
                "extending the powers-of-two O(log log X) moment order to a "
                "fixed-wheel rough hard stratum"
            ),
            "next_theorem": "BinaryGoldbachGrowingWheelResidualBoundK56",
        },
        "proof_dag": {
            "nodes": [
                {"id": "GB-TD4a", "label": "SparseHardStratumMomentToMaximumBridge", "status": "closed"},
                {"id": "GB-TD4b.1", "label": "FixedWheelRoughStratumHasLinearMassAndLogMomentBarrier", "status": "closed"},
                {
                    "id": "GB-TD4b.2",
                    "label": "BinaryGoldbachGrowingWheelResidualBoundK56",
                    "status": "highest_risk_open",
                },
                {"id": "GB", "label": "Strong Goldbach Conjecture", "status": "open_not_proven"},
            ],
            "edges": [["GB-TD4a", "GB-TD4b.1"], ["GB-TD4b.1", "GB-TD4b.2"], ["GB-TD4b.2", "GB"]],
        },
        "machine_audit": {
            "wheel_count": len(wheels),
            "scale_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The counting theorem and norm barrier are exact, but the spike is an "
            "inference countermodel, not the actual Goldbach residual. No K=56 "
            "minor-arc estimate or representation lower bound is proved."
        ),
    }


def rational_phase_transcript(
    value: int, characters: Iterable[tuple[int, int]]
) -> list[list[int]]:
    return [
        [numerator * value % denominator, numerator * (value + 2) % denominator]
        for numerator, denominator in characters
    ]


def twin_rational_fourier_no_go() -> dict[str, Any]:
    feature_families = [
        [(1, 3), (2, 5), (1, 8)],
        [(1, 4), (3, 9), (2, 25)],
        [(5, 7), (7, 11), (11, 13)],
        [(1, 16), (5, 27), (7, 49)],
    ]
    rows = []
    failures = 0
    total_witnesses = 0
    for characters in feature_families:
        denominators = [denominator for _, denominator in characters]
        transcript_modulus = lcm_many(denominators)
        residues = first_admissible_residues(transcript_modulus, 24)
        left_factor, right_factor = first_primes_above(max(denominators))
        period = transcript_modulus * left_factor * right_factor
        examples = []
        row_failures = 0
        for residue in residues:
            witness, crt_modulus = crt(
                [
                    (residue, transcript_modulus),
                    (0, left_factor),
                    ((-2) % right_factor, right_factor),
                ]
            )
            if witness <= left_factor or witness + 2 <= right_factor:
                witness += crt_modulus
            source_phase = rational_phase_transcript(residue, characters)
            witness_phase = rational_phase_transcript(witness, characters)
            checks = {
                "same_rational_fourier_phases": source_phase == witness_phase,
                "left_proper_composite": witness % left_factor == 0 and witness > left_factor,
                "right_proper_composite": (
                    (witness + 2) % right_factor == 0 and witness + 2 > right_factor
                ),
                "below_twice_period": witness < 2 * period,
            }
            row_failures += sum(int(not check) for check in checks.values())
            if len(examples) < 3:
                examples.append(
                    {
                        "admissible_residue": residue,
                        "phase_exponents": source_phase,
                        "composite_pair_start": str(witness),
                        "checks": checks,
                    }
                )
        total_witnesses += len(residues)
        failures += row_failures
        rows.append(
            {
                "rational_characters": [
                    {"numerator": numerator, "denominator": denominator}
                    for numerator, denominator in characters
                ],
                "factored_transcript_modulus": transcript_modulus,
                "forced_composite_factors": [left_factor, right_factor],
                "audited_admissible_residue_count": len(residues),
                "examples": examples,
                "row_failure_count": row_failures,
            }
        )

    return {
        "theorem_name": "FiniteRationalFourierAlgebraCompositeLift",
        "title_ko": "유한 유리 Fourier 대수의 합성수 쌍 lift 정리",
        "declared_target": (
            "Test whether a finite family of rational Fourier phases is a genuine "
            "non-congruence Type II separator capable of escaping TICKET135."
        ),
        "proved_statement": (
            "For finitely many rational additive characters "
            "exp(2*pi*i*a_j*n/q_j), the joint values at n and n+2 factor through "
            "n mod L, L=lcm(q_j). Every locally admissible phase transcript has "
            "a proper composite-pair realizer below 2Lrs by CRT. Thus any finite "
            "algebra generated by rational Fourier phases is still finite "
            "congruence information and cannot by itself certify twin primality."
        ),
        "proved_statement_ko": (
            "유한 개의 유리 주파수 exp(2*pi*i*a_j*n/q_j)를 사용해도 n과 n+2의 "
            "모든 위상값은 L=lcm(q_j)에 대한 n의 나머지로 결정된다. 따라서 "
            "TICKET135의 CRT lift가 그대로 적용되어 같은 Fourier 특성을 갖는 "
            "합성수 쌍이 존재한다. 유리 Fourier 특성이라는 표현만으로는 "
            "진정한 비합동 Type II 정보가 되지 않는다."
        ),
        "proof": (
            "Each character depends only on n modulo its denominator, so their "
            "joint algebra factors through n modulo L. For an admissible class, "
            "choose primes r,s not dividing L and solve n=a mod L, n=0 mod r, "
            "n=-2 mod s. The proper-factor and range argument is the quantitative "
            "CRT lift from TICKET135. Equality of every phase follows exactly "
            "from equality modulo each q_j."
        ),
        "exact_feature_contract": {
            "features": "exp(2*pi*i*a_j*n/q_j) and exp(2*pi*i*a_j*(n+2)/q_j)",
            "factor_modulus": "L=lcm(q_j)",
            "composite_lift": "n=a mod L, n=0 mod r, n=-2 mod s",
            "range_bound": "n<2Lrs",
        },
        "finite_fourier_audit": {
            "rows": rows,
            "total_witnesses": total_witnesses,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "aperiodic or scale-growing bilinear information with a uniform "
                "factor-sensitive separation margin"
            ),
            "discard": (
                "finite rational Fourier feature algebras as non-congruence "
                "certificates of twin primality"
            ),
            "next_theorem": "AperiodicScaleGrowingTypeIITwinSeparation",
        },
        "proof_dag": {
            "nodes": [
                {"id": "TP-TD3a", "label": "FiniteCongruenceTranscriptCompositeLift", "status": "closed"},
                {"id": "TP-TD3b.1", "label": "FiniteRationalFourierAlgebraCompositeLift", "status": "closed"},
                {
                    "id": "TP-TD3b.2",
                    "label": "AperiodicScaleGrowingTypeIITwinSeparation",
                    "status": "highest_risk_open",
                },
                {"id": "TP", "label": "Twin Prime Conjecture", "status": "open_not_proven"},
            ],
            "edges": [["TP-TD3a", "TP-TD3b.1"], ["TP-TD3b.1", "TP-TD3b.2"], ["TP-TD3b.2", "TP"]],
        },
        "machine_audit": {
            "feature_family_count": len(rows),
            "audited_witness_count": total_witnesses,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The factorization theorem covers only finitely many rational "
            "frequencies. Irrational, aperiodic, or scale-growing Type II data are "
            "not excluded. No positive exact-gap-two lower bound is obtained."
        ),
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": riemann_schur_test_bridge(),
        "collatz": collatz_affine_correction_bridge(),
        "goldbach": goldbach_fixed_wheel_barrier(),
        "twin_prime": twin_rational_fourier_no_go(),
    }
    failures = sum(
        section["machine_audit"]["total_failure_count"] for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureScaleSensitiveObstructionAndAffineBridgeAudit",
        **sections,
        "machine_audit": {
            "exact_theorem_count": 4,
            "route_correction_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "TICKET136 proves four exact intermediate theorems and four route "
            "corrections. It does not prove or refute any of the four conjectures. "
            "No conjecture proof and no conjecture counterexample is claimed. "
            "Every finite audit is subordinate to a displayed universal argument, "
            "and all conjecture resolution counters remain zero."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-136",
            "SchurTestWeilBlockBridgeAndEntrywiseDecayNoGo",
            "ProjectedWeilAbsoluteRowColumnTailBoundsWithPositiveMargin",
            "Fix one published projected Weil normalization and derive outward-rounded absolute row/column sums plus a positive tail gap.",
        ),
        (
            "collatz",
            "CO-TICKET-136",
            "LeastCounterexampleAffineCorrectionInequality",
            "UniformValuationSurplusBeyondAffineCorrectionForLeastCounterexampleCodes",
            "Prove that every hypothetical least-counterexample code has one prefix whose valuation surplus exceeds k*log2(1+1/(3n)).",
        ),
        (
            "goldbach",
            "GB-TICKET-136",
            "FixedWheelRoughStratumHasLinearMassAndLogMomentBarrier",
            "BinaryGoldbachGrowingWheelResidualBoundK56",
            "Choose a growing wheel W(X) and prove a K=56 residual budget uniformly over its rough residue classes and the complementary strata.",
        ),
        (
            "twin-prime",
            "TP-TICKET-136",
            "FiniteRationalFourierAlgebraCompositeLift",
            "AperiodicScaleGrowingTypeIITwinSeparation",
            "Construct a scale-growing bilinear statistic that does not factor through any fixed rational period and prove a uniform signed separation from CRT composite lifts.",
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
                "claim_boundary": "No conjecture proof and no certified conjecture counterexample.",
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
        "scale_sensitive_obstruction_and_affine_bridge_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data/open-problem/ticket136-scale-sensitive-obstructions-and-affine-bridge.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-136-schur-test-tail-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-136-affine-correction-inequality.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-136-fixed-wheel-moment-barrier.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-136-rational-fourier-lift.json",
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
    print(json.dumps({"schema": SCHEMA, "machine_audit": audit["machine_audit"]}, indent=2))
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
