from __future__ import annotations

import json
import math
from fractions import Fraction
from math import comb
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
from ticket136_scale_sensitive_obstructions_and_affine_bridge import (
    accelerated_collatz_step,
    euler_phi,
    minimal_moment_for_inflation,
)


GENERATED_AT = "2026-07-26T12:00:00+09:00"
SCHEMA = "primeproject.ticket137-cancellation-entropy-and-information-budget.v1"


def sylvester_hadamard(dimension: int) -> list[list[int]]:
    if dimension < 1 or dimension & (dimension - 1):
        raise ValueError("dimension must be a positive power of two")
    matrix = [[1]]
    while len(matrix) < dimension:
        top = [row + row for row in matrix]
        bottom = [row + [-value for value in row] for row in matrix]
        matrix = top + bottom
    return matrix


def riemann_hadamard_cancellation_no_go() -> dict[str, Any]:
    rows = []
    failures = 0
    for dimension in [4, 8, 16, 32, 64, 128]:
        hadamard = sylvester_hadamard(dimension)
        diagonal_products = {
            sum(hadamard[row][column] ** 2 for column in range(dimension))
            for row in range(dimension)
        }
        off_diagonal_products = {
            sum(
                hadamard[left][column] * hadamard[right][column]
                for column in range(dimension)
            )
            for left in range(dimension)
            for right in range(left)
        }
        absolute_row_sum = Fraction(1)
        absolute_column_sum = Fraction(1)
        operator_norm_squared = Fraction(1, dimension)
        alpha = Fraction(1)
        gamma = Fraction(2, dimension)
        true_margin = alpha * gamma - operator_norm_squared
        schur_margin = alpha * gamma - absolute_row_sum * absolute_column_sum
        checks = {
            "hadamard_diagonal_identity": diagonal_products == {dimension},
            "hadamard_off_diagonal_identity": off_diagonal_products == {0},
            "true_block_margin_positive": true_margin > 0,
            "absolute_schur_margin_negative": schur_margin < 0,
        }
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "dimension": dimension,
                "scaled_entry_absolute_value": fraction_payload(
                    Fraction(1, dimension)
                ),
                "maximum_absolute_row_sum": fraction_payload(absolute_row_sum),
                "maximum_absolute_column_sum": fraction_payload(
                    absolute_column_sum
                ),
                "exact_operator_norm_squared": fraction_payload(
                    operator_norm_squared
                ),
                "tail_gap_gamma": fraction_payload(gamma),
                "true_operator_margin": fraction_payload(true_margin),
                "absolute_schur_margin": fraction_payload(schur_margin),
                "schur_overestimate_factor_squared": dimension,
                "checks": checks,
            }
        )

    return {
        "theorem_name": "HadamardCancellationSchurOverestimateNoGo",
        "title_ko": "Hadamard 상쇄에 의한 절댓값 Schur 과대평가 한계 정리",
        "declared_target": (
            "Test whether the absolute row/column Schur target promoted by "
            "TICKET136 is close enough to the true projected cross-operator norm "
            "to remain the decisive RH route."
        ),
        "proved_statement": (
            "For every N=2^m>=4, let H_N be a Sylvester Hadamard matrix and "
            "B_N=H_N/N. Then every absolute row and column sum of B_N is one, "
            "whereas ||B_N||_2^2=1/N. Consequently the self-adjoint block with "
            "A=I and C=(2/N)I has positive true Schur margin 1/N, while the "
            "absolute-sum certificate reports the negative margin 2/N-1. The "
            "multiplicative overestimate in squared norm is exactly N."
        ),
        "proved_statement_ko": (
            "N=2^m>=4인 모든 차원에서 Sylvester Hadamard 행렬 H_N과 "
            "B_N=H_N/N을 잡으면 B_N의 절댓값 행합과 열합은 모두 1이지만 "
            "실제 연산자 노름의 제곱은 1/N이다. 따라서 A=I, C=(2/N)I인 "
            "블록은 실제로 1/N의 양의 여유를 가지지만 절댓값 Schur "
            "인증서는 2/N-1이라는 음의 여유를 보고한다. 제곱 노름의 "
            "과대평가 배수는 정확히 N이다."
        ),
        "proof": (
            "Sylvester matrices satisfy H_N H_N^T=N I. Hence all singular "
            "values of B_N=H_N/N equal 1/sqrt(N). Every entry has magnitude "
            "1/N, so each absolute row and column sum equals one. The sharp "
            "block criterion from TICKET135 accepts because "
            "alpha*gamma-||B_N||^2=2/N-1/N=1/N>0, but the TICKET136 absolute "
            "Schur substitution gives alpha*gamma-R*S=2/N-1<0."
        ),
        "exact_contract": {
            "orthogonality": "H_N*H_N^T=N*I",
            "scaled_cross_block": "B_N=H_N/N",
            "true_norm": "||B_N||_2^2=1/N",
            "absolute_schur_bound": "R*S=1",
            "positive_block_example": "A=I, C=(2/N)I",
        },
        "hadamard_audit": {
            "rows": rows,
            "dimension_count": len(rows),
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "signed or cancellation-sensitive projected Weil cross-block "
                "operator estimates combined with certified core and tail gaps"
            ),
            "discard": (
                "requiring absolute row/column summability as though it were a "
                "necessary approximation to the true cross-operator norm"
            ),
            "next_theorem": "ProjectedWeilSignedCrossBlockCancellationWithPositiveMargin",
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "RH-TD4b.1",
                    "label": "SchurTestWeilBlockBridgeAndEntrywiseDecayNoGo",
                    "status": "closed",
                },
                {
                    "id": "RH-TD4b.2a",
                    "label": "HadamardCancellationSchurOverestimateNoGo",
                    "status": "closed",
                },
                {
                    "id": "RH-TD4b.2b",
                    "label": "ProjectedWeilSignedCrossBlockCancellationWithPositiveMargin",
                    "status": "highest_risk_open",
                },
                {
                    "id": "RH",
                    "label": "Riemann Hypothesis",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["RH-TD4b.1", "RH-TD4b.2a"],
                ["RH-TD4b.2a", "RH-TD4b.2b"],
                ["RH-TD4b.2b", "RH"],
            ],
        },
        "machine_audit": {
            "hadamard_dimension_count": len(rows),
            "positive_true_margin_count": sum(
                int(row["checks"]["true_block_margin_positive"]) for row in rows
            ),
            "rejected_absolute_schur_count": sum(
                int(row["checks"]["absolute_schur_margin_negative"])
                for row in rows
            ),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The counterfamily is an exact linear-algebra theorem, not a projected "
            "Weil estimate. It proves that the absolute Schur route can be "
            "arbitrarily wasteful; it supplies neither a signed Weil cross-block "
            "bound nor an RH proof or counterexample."
        ),
    }


def affine_cap(lower_bound: int, depth: int) -> int:
    if lower_bound < 1 or depth < 1:
        raise ValueError("lower_bound and depth must be positive")
    base = lower_bound**depth
    upper = (3 * lower_bound + 1) ** depth
    quotient = upper // base
    return quotient.bit_length() - 1


def terminal_affine_cap_mass(lower_bound: int, depth: int) -> Fraction:
    cap = affine_cap(lower_bound, depth)
    return sum(
        (Fraction(comb(total - 1, depth - 1), 2**total)
         for total in range(depth, cap + 1)),
        Fraction(0),
    )


def prefix_affine_cap_mass(lower_bound: int, depth: int) -> Fraction:
    states = {0: Fraction(1)}
    for step in range(1, depth + 1):
        cap = affine_cap(lower_bound, step)
        next_states: dict[int, Fraction] = {}
        for total, mass in states.items():
            for valuation in range(1, cap - total + 1):
                new_total = total + valuation
                next_states[new_total] = next_states.get(
                    new_total, Fraction(0)
                ) + mass * Fraction(1, 2**valuation)
        states = next_states
    return sum(states.values(), Fraction(0))


def valuation_prefix(start: int, depth: int) -> tuple[int, ...]:
    current = start
    values = []
    for _ in range(depth):
        current, valuation = accelerated_collatz_step(current)
        values.append(valuation)
    return tuple(values)


def cylinder_residue(word: Iterable[int]) -> tuple[int, int]:
    values = tuple(word)
    modulus = 2 ** (sum(values) + 1)
    matches = [
        residue
        for residue in range(1, modulus, 2)
        if valuation_prefix(residue, len(values)) == values
    ]
    if len(matches) != 1:
        raise AssertionError("valuation word must define one odd residue class")
    return matches[0], modulus


def collatz_affine_capped_mass_decay() -> dict[str, Any]:
    rows = []
    failures = 0
    for lower_bound in [2, 10, 1000, 1_000_000]:
        previous_prefix_mass = Fraction(1)
        for depth in [8, 16, 32, 64]:
            cap = affine_cap(lower_bound, depth)
            terminal_mass = terminal_affine_cap_mass(lower_bound, depth)
            prefix_mass = prefix_affine_cap_mass(lower_bound, depth)
            lambda_value = math.log2(3 + 1 / lower_bound)
            chernoff_base = (
                (lambda_value / 2)
                * (lambda_value / (2 * (lambda_value - 1)))
                ** (lambda_value - 1)
            )
            checks = {
                "integer_cap_exact": (
                    (2**cap) * (lower_bound**depth)
                    <= (3 * lower_bound + 1) ** depth
                    < (2 ** (cap + 1)) * (lower_bound**depth)
                ),
                "prefix_mass_bounded_by_terminal_mass": (
                    prefix_mass <= terminal_mass
                ),
                "prefix_survivor_mass_nonincreasing": (
                    prefix_mass <= previous_prefix_mass
                ),
                "chernoff_base_strictly_below_one": chernoff_base < 1,
                "terminal_mass_within_chernoff_bound": (
                    float(terminal_mass) <= chernoff_base**depth + 1e-15
                ),
            }
            failures += sum(int(not value) for value in checks.values())
            rows.append(
                {
                    "least_counterexample_lower_bound": lower_bound,
                    "depth": depth,
                    "exact_terminal_valuation_cap": cap,
                    "terminal_cap_mass": fraction_payload(terminal_mass),
                    "all_prefix_cap_mass": fraction_payload(prefix_mass),
                    "chernoff_exponential_base": chernoff_base,
                    "checks": checks,
                }
            )
            previous_prefix_mass = prefix_mass

    cylinder_rows = []
    for word in [(1, 2, 1), (2, 1, 3), (3, 2, 2), (1, 1, 1, 1, 2)]:
        residue, modulus = cylinder_residue(word)
        replay_starts = [residue + multiplier * modulus for multiplier in [1, 7, 31]]
        checks = {
            "unique_class_measure": Fraction(2, modulus)
            == Fraction(1, 2 ** sum(word)),
            "arbitrarily_large_representatives_replay": all(
                valuation_prefix(start, len(word)) == word
                for start in replay_starts
            ),
        }
        failures += sum(int(not value) for value in checks.values())
        cylinder_rows.append(
            {
                "valuation_word": list(word),
                "valuation_sum": sum(word),
                "odd_residue": residue,
                "modulus": modulus,
                "relative_haar_mass": fraction_payload(
                    Fraction(1, 2 ** sum(word))
                ),
                "positive_representatives": replay_starts,
                "checks": checks,
            }
        )

    return {
        "theorem_name": "AffineCappedValuationCylinderMassDecay",
        "title_ko": "Affine cap을 만족하는 valuation cylinder 질량 감소 정리",
        "declared_target": (
            "Quantify how exceptional the TICKET136 least-counterexample "
            "valuation constraint is, while testing whether small 2-adic measure "
            "can exclude a natural Collatz counterexample."
        ),
        "proved_statement": (
            "Let B>=2 and let m_B(k) be the largest integer s with "
            "2^s B^k<=(3B+1)^k. A least Collatz counterexample n_0>=B must have "
            "S_j<=m_B(j) for every j. Under normalized Haar measure on odd "
            "2-adic integers, a valuation word of sum s has mass 2^-s, so the "
            "terminal-cap mass is exactly sum_{s=k}^{m_B(k)} "
            "C(s-1,k-1)2^-s. The all-prefix survivor mass is no larger and "
            "decays exponentially in k. Nevertheless every finite valuation "
            "cylinder is one odd residue class modulo 2^(s+1) and contains "
            "arbitrarily large positive integers."
        ),
        "proved_statement_ko": (
            "B>=2에 대해 2^s B^k<=(3B+1)^k를 만족하는 최대 정수를 "
            "m_B(k)라 하자. B 이상인 최소 콜라츠 반례가 있다면 모든 j에서 "
            "S_j<=m_B(j)를 만족해야 한다. 홀수 2-adic 정수의 정규화 Haar "
            "측도에서 valuation 합이 s인 word의 질량은 2^-s이므로 종단 cap "
            "질량은 정확히 sum C(s-1,k-1)2^-s이며, 모든 prefix cap을 "
            "만족하는 질량은 이보다 작고 k에 대해 지수적으로 감소한다. "
            "그러나 모든 유한 valuation cylinder는 modulo 2^(s+1)의 한 "
            "홀수 나머지류이므로 임의로 큰 양의 정수를 포함한다."
        ),
        "proof": (
            "TICKET136 gives the cap for every non-descending prefix. A positive "
            "valuation composition a_1+...+a_k=s defines one odd cylinder of "
            "relative measure 2^-s, and there are C(s-1,k-1) such compositions. "
            "Summing gives the exact terminal mass; imposing every prefix cap "
            "only removes cylinders. For lambda=log_2(3+1/B) in (1,2), Chernoff "
            "applied to iid geometric masses P(a=r)=2^-r gives an exponential "
            "upper bound q(lambda)^k with "
            "q=(lambda/2)(lambda/(2(lambda-1)))^(lambda-1)<1. The residue-class "
            "description proves the finite-cylinder natural representatives."
        ),
        "exact_contract": {
            "integer_cap": "m_B(k)=max{s:2^s*B^k<=(3B+1)^k}",
            "word_mass": "mu(a_1,...,a_k)=2^-(a_1+...+a_k)",
            "terminal_mass": (
                "sum_{s=k}^{m_B(k)} binom(s-1,k-1)*2^-s"
            ),
            "least_counterexample_condition": "S_j<=m_B(j) for every j",
        },
        "mass_audit": {
            "rows": rows,
            "cylinder_rows": cylinder_rows,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "deterministic arithmetic exclusion of natural integer codes "
                "from the infinite affine-capped survivor set"
            ),
            "discard": (
                "promoting exponentially small or zero 2-adic measure to "
                "emptiness of the embedded natural Collatz codes"
            ),
            "next_theorem": "ArithmeticEmptinessOfInfiniteAffineCappedNaturalCodeSet",
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "CO-TD4b.1",
                    "label": "LeastCounterexampleAffineCorrectionInequality",
                    "status": "closed",
                },
                {
                    "id": "CO-TD4b.2a",
                    "label": "AffineCappedValuationCylinderMassDecay",
                    "status": "closed",
                },
                {
                    "id": "CO-TD4b.2b",
                    "label": "ArithmeticEmptinessOfInfiniteAffineCappedNaturalCodeSet",
                    "status": "highest_risk_open",
                },
                {
                    "id": "CO",
                    "label": "Collatz Conjecture",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["CO-TD4b.1", "CO-TD4b.2a"],
                ["CO-TD4b.2a", "CO-TD4b.2b"],
                ["CO-TD4b.2b", "CO"],
            ],
        },
        "machine_audit": {
            "mass_row_count": len(rows),
            "finite_cylinder_count": len(cylinder_rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The exact measure formula and exponential upper bound concern "
            "2-adic Haar mass. A measure-zero survivor set can still contain "
            "embedded natural integers, and every finite cylinder does. No "
            "arithmetic emptiness theorem, Collatz proof, or counterexample is supplied."
        ),
    }


def is_squarefree_odd(value: int) -> bool:
    if value < 1 or value % 2 == 0:
        return False
    remaining = value
    divisor = 2
    while divisor * divisor <= remaining:
        exponent = 0
        while remaining % divisor == 0:
            remaining //= divisor
            exponent += 1
        if exponent > 1:
            return False
        divisor += 1
    return True


def goldbach_subpower_wheel_barrier() -> dict[str, Any]:
    wheels = [3, 15, 105, 1155, 15015]
    rows = []
    failures = 0
    for wheel in wheels:
        block_count = wheel
        scale = 2 * wheel * block_count
        hard_residue_count = sum(
            int(math.gcd(2 * index, wheel) == 1)
            for index in range(1, wheel + 1)
        )
        hard_count = block_count * hard_residue_count
        minimum_moment = minimal_moment_for_inflation(hard_count)
        checks = {
            "wheel_odd_squarefree": is_squarefree_odd(wheel),
            "complete_residue_block_count": (
                hard_residue_count == euler_phi(wheel)
            ),
            "exact_hard_count": hard_count == block_count * euler_phi(wheel),
            "phi_square_lower_bound": euler_phi(wheel) ** 2 >= wheel,
            "hard_count_scale_lower_bound": (
                4 * wheel * hard_count**2 >= scale**2
            ),
            "half_power_wheel_condition": wheel**2 <= scale,
            "exact_moment_threshold": (
                5**minimum_moment * hard_count <= 6**minimum_moment
                and (
                    minimum_moment == 1
                    or 5 ** (minimum_moment - 1) * hard_count
                    > 6 ** (minimum_moment - 1)
                )
            ),
        }
        failures += sum(int(not value) for value in checks.values())
        rows.append(
            {
                "wheel": wheel,
                "scale_X": scale,
                "complete_period_blocks": block_count,
                "hard_residues_per_period": hard_residue_count,
                "hard_stratum_size": hard_count,
                "minimum_p_for_factor_at_most_6_over_5": minimum_moment,
                "log_X": math.log(scale),
                "moment_over_log_X": minimum_moment / math.log(scale),
                "checks": checks,
            }
        )

    return {
        "theorem_name": "SubpowerGrowingWheelLogMomentBarrier",
        "title_ko": "부분 거듭제곱 성장 wheel의 로그 모멘트 장벽 정리",
        "declared_target": (
            "Determine whether merely replacing the fixed Goldbach wheel in "
            "TICKET136 by a growing wheel can reduce the moment order below log X."
        ),
        "proved_statement": (
            "Let W be odd and squarefree, X=2WM, and H_W(X) the even integers "
            "through X coprime to W. Then |H_W(X)|=M phi(W) and "
            "phi(W)^2>=W. If W<=X^(1-epsilon), then "
            "|H_W(X)|>=X^((1+epsilon)/2)/2. Therefore any normalized "
            "L^p-to-maximum promotion with inflation factor at most 6/5 still "
            "requires p>=(((1+epsilon)/2)log X-log 2)/log(6/5), "
            "which is Omega(log X)."
        ),
        "proved_statement_ko": (
            "W가 홀수 squarefree이고 X=2WM일 때 W와 서로소인 X 이하 짝수의 "
            "수는 M phi(W)이며 phi(W)^2>=W이다. W<=X^(1-epsilon)이면 "
            "hard stratum의 크기는 X^((1+epsilon)/2)/2 이상이다. "
            "따라서 정규화 L^p 값을 최대값으로 올릴 때 팽창계수를 6/5 이하로 "
            "만들려면 여전히 p=Omega(log X)가 필요하다."
        ),
        "proof": (
            "Writing each even N as 2m, oddness of W gives "
            "gcd(N,W)=gcd(m,W). Each complete block of W consecutive m therefore "
            "contributes phi(W) hard residues. For squarefree odd W, "
            "phi(W)^2/W=product_{p|W}(p-1)^2/p>=1. Substituting M=X/(2W) "
            "yields h=M phi(W)>=X/(2 sqrt(W)); the assumed wheel scale gives the "
            "displayed power lower bound. Since ||x||_infinity<=h^(1/p)||x||_p "
            "is sharp on one-point spikes, h^(1/p)<=6/5 forces "
            "p>=log(h)/log(6/5)."
        ),
        "exact_contract": {
            "hard_count": "|H_W(2WM)|=M*phi(W)",
            "totient_bound": "phi(W)^2>=W for odd squarefree W",
            "subpower_assumption": "0<epsilon<=1 and W<=X^(1-epsilon)",
            "moment_threshold": "p>=log(|H_W(X)|)/log(6/5)",
        },
        "wheel_audit": {
            "rows": rows,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "near-full-scale wheel localization or a direct pointwise signed "
                "binary Goldbach residual bound with K<=56"
            ),
            "discard": (
                "expecting any W(X)<=X^(1-epsilon) growing wheel by itself to "
                "turn a sublogarithmic moment estimate into pointwise positivity"
            ),
            "next_theorem": "NearFullScaleWheelOrPointwiseBinaryGoldbachResidualK56",
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "GB-TD4b.1",
                    "label": "FixedWheelRoughStratumHasLinearMassAndLogMomentBarrier",
                    "status": "closed",
                },
                {
                    "id": "GB-TD4b.2a",
                    "label": "SubpowerGrowingWheelLogMomentBarrier",
                    "status": "closed",
                },
                {
                    "id": "GB-TD4b.2b",
                    "label": "NearFullScaleWheelOrPointwiseBinaryGoldbachResidualK56",
                    "status": "highest_risk_open",
                },
                {
                    "id": "GB",
                    "label": "Strong Goldbach Conjecture",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["GB-TD4b.1", "GB-TD4b.2a"],
                ["GB-TD4b.2a", "GB-TD4b.2b"],
                ["GB-TD4b.2b", "GB"],
            ],
        },
        "machine_audit": {
            "wheel_scale_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This theorem is an inference barrier for subpower squarefree wheels. "
            "It proves no binary Goldbach residual estimate and does not cover "
            "near-full-scale localization or a direct pointwise argument."
        ),
    }


def rational_phase_pair_transcript(
    value: int, characters: Iterable[tuple[int, int]]
) -> tuple[tuple[int, int], ...]:
    result = []
    for numerator, denominator in characters:
        result.append(
            (
                (numerator * value) % denominator,
                (numerator * (value + 2)) % denominator,
            )
        )
    return tuple(result)


def twin_rational_fourier_information_budget() -> dict[str, Any]:
    character_sets = [
        [(1, 3), (2, 5), (1, 8)],
        [(1, 7), (3, 9), (2, 11)],
        [(1, 16), (5, 21), (7, 25)],
        [(1, 27), (4, 32), (9, 35)],
    ]
    rows = []
    failures = 0
    total_collisions = 0
    for characters in character_sets:
        denominators = [denominator for _, denominator in characters]
        period = lcm_many(denominators)
        left_prime, right_prime = first_primes_above(max(denominators))
        witness_period = period * left_prime * right_prime
        scale = 2 * witness_period
        residues = first_admissible_residues(period, 32)
        examples = []
        row_failures = 0
        for residue in residues:
            base, crt_modulus = crt(
                [
                    (residue, period),
                    (0, left_prime),
                    ((-2) % right_prime, right_prime),
                ]
            )
            if crt_modulus != witness_period:
                raise AssertionError("unexpected CRT witness modulus")
            witness = base
            if witness <= left_prime or witness + 2 <= right_prime:
                witness += witness_period
            checks = {
                "below_information_budget_scale": witness < scale,
                "same_rational_fourier_pair_transcript": (
                    rational_phase_pair_transcript(witness, characters)
                    == rational_phase_pair_transcript(residue, characters)
                ),
                "left_proper_composite": (
                    witness % left_prime == 0 and witness > left_prime
                ),
                "right_proper_composite": (
                    (witness + 2) % right_prime == 0
                    and witness + 2 > right_prime
                ),
            }
            row_failures += sum(int(not value) for value in checks.values())
            total_collisions += 1
            if len(examples) < 3:
                examples.append(
                    {
                        "admissible_residue": residue,
                        "composite_pair_start": str(witness),
                        "checks": checks,
                    }
                )
        failures += row_failures
        rows.append(
            {
                "characters": [
                    {"numerator": numerator, "denominator": denominator}
                    for numerator, denominator in characters
                ],
                "denominator_lcm_L": period,
                "outside_primes": [left_prime, right_prime],
                "audit_scale_X": scale,
                "exact_budget_ratio_X_over_2qr": period,
                "denominator_information_bits": period.bit_length(),
                "admissible_class_count": len(residues),
                "collision_count": len(residues),
                "examples": examples,
                "row_failure_count": row_failures,
            }
        )

    return {
        "theorem_name": "RationalFourierInformationBudgetLowerBound",
        "title_ko": "유리 Fourier 분리기의 정보 예산 하한 정리",
        "declared_target": (
            "Quantify how fast the rational Fourier denominator budget must grow "
            "before the finite-period obstruction of TICKET136 can even cease to "
            "produce an in-range composite-pair collision."
        ),
        "proved_statement": (
            "At scale X, let a finite rational Fourier pair-feature map use "
            "frequencies a_j/q_j and put L=lcm(q_j). For every locally admissible "
            "class modulo L and distinct primes r,s not dividing 2L, there is a "
            "proper composite pair n,n+2 with the same transcript as every "
            "integer in that class and n<2Lrs. Hence if 2Lrs<=X, no locally "
            "admissible transcript is by itself a sound sufficient certificate "
            "of twin primality on [1,X]. Any zero-false-positive separator that "
            "depends only on these transcripts must violate this budget, requiring "
            "L>X/(2rs) for the selected outside-prime pair."
        ),
        "proved_statement_ko": (
            "규모 X에서 유한 rational Fourier pair-feature가 a_j/q_j를 사용하고 "
            "L=lcm(q_j)라 하자. modulo L의 모든 국소 허용류와 2L을 나누지 "
            "않는 서로 다른 소수 r,s에 대해 같은 feature transcript를 가지는 "
            "그 나머지류의 모든 정수와 같은 transcript를 가진 합성수 쌍 "
            "n,n+2가 n<2Lrs에 존재한다. 따라서 2Lrs<=X이면 국소 허용 "
            "transcript만으로는 X 이하 쌍둥이 소수성의 건전한 충분 인증서가 "
            "될 수 없다. 오탐이 없는 transcript 전용 유리 분리기는 최소한 "
            "L>X/(2rs)의 정보 예산을 가져야 한다."
        ),
        "proof": (
            "Every character exp(2 pi i a_j n/q_j), evaluated at n and n+2, "
            "factors through n modulo L. CRT imposes n=a mod L, r|n, and "
            "s|n+2. Adding Lrs once when needed makes both factors proper while "
            "keeping n<2Lrs. The contrapositive gives the denominator-lcm lower "
            "bound for any in-range collision-free rational separator."
        ),
        "exact_contract": {
            "feature_period": "L=lcm(q_1,...,q_m)",
            "collision_bound": "n<2*L*r*s",
            "subcritical_budget": "2*L*r*s<=X",
            "certificate_scope": (
                "feature-transcript-only sufficient certificates with zero "
                "composite-pair false positives on [1,X]"
            ),
            "necessary_escape": "L>X/(2*r*s) or non-rational/aperiodic information",
        },
        "information_budget_audit": {
            "rows": rows,
            "total_collision_count": total_collisions,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "irrational, aperiodic, factor-sensitive Type II information or "
                "a supercritical rational denominator budget with signed transport"
            ),
            "discard": (
                "subcritical rational Fourier feature families satisfying "
                "2*lcm(q_j)*r*s<=X as exact twin-primality separators"
            ),
            "next_theorem": "IrrationalOrSupercriticalAperiodicTypeIITwinSeparation",
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "TP-TD3b.1",
                    "label": "FiniteRationalFourierAlgebraCompositeLift",
                    "status": "closed",
                },
                {
                    "id": "TP-TD3b.2a",
                    "label": "RationalFourierInformationBudgetLowerBound",
                    "status": "closed",
                },
                {
                    "id": "TP-TD3b.2b",
                    "label": "IrrationalOrSupercriticalAperiodicTypeIITwinSeparation",
                    "status": "highest_risk_open",
                },
                {
                    "id": "TP",
                    "label": "Twin Prime Conjecture",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["TP-TD3b.1", "TP-TD3b.2a"],
                ["TP-TD3b.2a", "TP-TD3b.2b"],
                ["TP-TD3b.2b", "TP"],
            ],
        },
        "machine_audit": {
            "feature_family_count": len(rows),
            "composite_collision_count": total_collisions,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The budget theorem excludes only transcript-only sufficient "
            "certificates built from exact finite rational Fourier features below "
            "the displayed scale. It does not exclude certificates using external "
            "arithmetic data, irrational phases, supercritical denominator growth, "
            "or analytic Type II cancellation, and it gives no positive "
            "exact-gap-two lower bound."
        ),
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": riemann_hadamard_cancellation_no_go(),
        "collatz": collatz_affine_capped_mass_decay(),
        "goldbach": goldbach_subpower_wheel_barrier(),
        "twin_prime": twin_rational_fourier_information_budget(),
    }
    failures = sum(
        section["machine_audit"]["total_failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureCancellationEntropyAndInformationBudgetAudit",
        **sections,
        "cross_problem_synthesis": {
            "shared_obstruction": (
                "Magnitude-only, measure-only, and finite-period summaries can "
                "be quantitatively strong while still losing the signed or "
                "pointwise arithmetic information needed by the conjecture."
            ),
            "shared_upgrade": (
                "The next routes must preserve cancellation, arithmetic emptiness, "
                "near-pointwise control, or aperiodic factor-sensitive information."
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
            "TICKET137 proves four exact intermediate or no-go theorems and "
            "revises four proof targets. It does not prove or refute RH, Collatz, "
            "strong Goldbach, or Twin Prime. No conjecture proof and no certified "
            "conjecture counterexample is claimed; all resolution counters remain zero."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-137",
            "HadamardCancellationSchurOverestimateNoGo",
            "ProjectedWeilSignedCrossBlockCancellationWithPositiveMargin",
            "Fix one projected Weil normalization and derive a signed operator or orthogonality-based spectral estimate together with an independently certified tail gap.",
        ),
        (
            "collatz",
            "CO-TICKET-137",
            "AffineCappedValuationCylinderMassDecay",
            "ArithmeticEmptinessOfInfiniteAffineCappedNaturalCodeSet",
            "Characterize the infinite affine-capped survivor set and prove that no embedded positive-integer valuation code can remain in it at every depth.",
        ),
        (
            "goldbach",
            "GB-TICKET-137",
            "SubpowerGrowingWheelLogMomentBarrier",
            "NearFullScaleWheelOrPointwiseBinaryGoldbachResidualK56",
            "Either localize at near-full wheel scale with all complementary strata controlled or prove the signed residual bound pointwise with K<=56.",
        ),
        (
            "twin-prime",
            "TP-TICKET-137",
            "RationalFourierInformationBudgetLowerBound",
            "IrrationalOrSupercriticalAperiodicTypeIITwinSeparation",
            "Construct a factor-sensitive Type II statistic outside the subcritical rational-period budget and prove signed transport to positive exact-gap-two mass.",
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
        "cancellation_entropy_and_information_budget_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket137-cancellation-entropy-and-information-budget.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-137-hadamard-schur-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-137-affine-cap-mass-decay.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-137-subpower-wheel-barrier.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-137-fourier-information-budget.json",
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
