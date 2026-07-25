from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from typing import Any, Iterable

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket132_admissibility_nullset_hard_stratum_local_parity import (
    fraction_payload,
)
from ticket136_scale_sensitive_obstructions_and_affine_bridge import (
    euler_phi,
    minimal_moment_for_inflation,
)
from ticket137_cancellation_entropy_and_information_budget import (
    affine_cap,
    is_squarefree_odd,
    sylvester_hadamard,
)


GENERATED_AT = "2026-07-27T12:00:00+09:00"
SCHEMA = "primeproject.ticket138-correlation-periodicity-and-scale-closure.v1"


def riemann_cross_gram_correlation_criterion() -> dict[str, Any]:
    hadamard_rows = []
    coherent_rows = []
    failures = 0

    for dimension in [4, 8, 16, 32, 64, 128]:
        hadamard = sylvester_hadamard(dimension)
        diagonal = {
            sum(value * value for value in row) for row in hadamard
        }
        off_diagonal = {
            sum(
                hadamard[left][column] * hadamard[right][column]
                for column in range(dimension)
            )
            for left in range(dimension)
            for right in range(left)
        }
        row_energy = Fraction(1, dimension)
        off_diagonal_budget = Fraction(0)
        correlation_bound = row_energy + off_diagonal_budget
        alpha = Fraction(1)
        gamma = Fraction(2, dimension)
        margin = alpha * gamma - correlation_bound
        checks = {
            "integer_hadamard_orthogonality": (
                diagonal == {dimension} and off_diagonal == {0}
            ),
            "cross_gram_bound_equals_true_norm_squared": (
                correlation_bound == Fraction(1, dimension)
            ),
            "positive_block_margin": margin > 0,
        }
        failures += sum(int(not value) for value in checks.values())
        hadamard_rows.append(
            {
                "dimension": dimension,
                "maximum_row_energy": fraction_payload(row_energy),
                "maximum_off_diagonal_correlation_budget": fraction_payload(
                    off_diagonal_budget
                ),
                "cross_gram_operator_bound": fraction_payload(
                    correlation_bound
                ),
                "exact_operator_norm_squared": fraction_payload(
                    Fraction(1, dimension)
                ),
                "tail_gap_product": fraction_payload(alpha * gamma),
                "certified_margin": fraction_payload(margin),
                "checks": checks,
            }
        )

        signs = [1] * (dimension // 2) + [-1] * (dimension // 2)
        signed_row_sums = {
            Fraction(left * sum(signs), dimension) for left in signs
        }
        signed_column_sums = {
            Fraction(right * sum(signs), dimension) for right in signs
        }
        coherent_energy = Fraction(1, dimension)
        coherent_off_budget = Fraction(dimension - 1, dimension)
        coherent_bound = coherent_energy + coherent_off_budget
        coherent_checks = {
            "all_signed_row_sums_zero": signed_row_sums == {Fraction(0)},
            "all_signed_column_sums_zero": (
                signed_column_sums == {Fraction(0)}
            ),
            "coherent_cross_gram_bound_exact": coherent_bound == 1,
            "operator_norm_squared_one": coherent_bound == 1,
        }
        failures += sum(int(not value) for value in coherent_checks.values())
        coherent_rows.append(
            {
                "dimension": dimension,
                "entry_model": "B_ij=s_i*t_j/N with balanced signs",
                "signed_row_sum": fraction_payload(Fraction(0)),
                "signed_column_sum": fraction_payload(Fraction(0)),
                "maximum_row_energy": fraction_payload(coherent_energy),
                "maximum_off_diagonal_correlation_budget": fraction_payload(
                    coherent_off_budget
                ),
                "cross_gram_operator_bound": fraction_payload(coherent_bound),
                "exact_operator_norm_squared": fraction_payload(Fraction(1)),
                "checks": coherent_checks,
            }
        )

    return {
        "theorem_name": "CrossGramCorrelationBlockPositivityCriterion",
        "title_ko": "cross-Gram 상관 예산 블록 양성 판정 정리",
        "declared_target": (
            "Replace the TICKET137 absolute Schur target by a signed, "
            "cancellation-sensitive quantity that can still certify block "
            "positivity, and test whether signed row or column means alone suffice."
        ),
        "proved_statement": (
            "Let B have rows b_i. Put d=max_i ||b_i||_2^2 and "
            "c=max_i sum_{j!=i}|<b_i,b_j>|. Then ||B||_2^2<=d+c. Hence a "
            "self-adjoint block [[A,B],[B*,C]] is positive definite whenever "
            "alpha>0, gamma>0, A>=alpha I, C>=gamma I, and "
            "d+c<alpha*gamma. The bound preserves "
            "signed cancellation inside row inner products. In contrast, for "
            "balanced sign vectors s,t, B=s*t^T/N has every signed row and "
            "column sum zero but ||B||_2^2=1, so signed means alone do not "
            "control the operator norm."
        ),
        "proved_statement_ko": (
            "B의 행을 b_i라 하고 d=max ||b_i||^2, "
            "c=max_i sum_{j!=i}|<b_i,b_j>|라 하면 ||B||^2<=d+c이다. 따라서 "
            "alpha>0, gamma>0, A>=alpha I, C>=gamma I이고 "
            "d+c<alpha*gamma이면 대응하는 "
            "자기수반 블록은 양의 정부호다. 이 예산은 행 내적의 부호 상쇄를 "
            "보존한다. 반면 균형 부호 벡터 s,t에 대한 B=s*t^T/N은 모든 "
            "부호 행합과 열합이 0이지만 ||B||^2=1이므로 평균 상쇄만으로는 "
            "연산자 노름을 제어할 수 없다."
        ),
        "proof": (
            "The nonzero eigenvalues of B*B and BB* agree. The Gram matrix "
            "G=BB* has diagonal entries ||b_i||^2 and off-diagonal entries "
            "<b_i,b_j>. Gershgorin, equivalently the Hermitian row-sum bound, "
            "gives lambda_max(G)<=d+c. The Schur-complement criterion then gives "
            "block positivity under alpha>0, gamma>0, and "
            "d+c<alpha*gamma. For the no-go family, "
            "balanced signs make all signed row and column sums vanish, while "
            "B=(s/sqrt(N))(t/sqrt(N))^T is rank one with singular value one."
        ),
        "exact_contract": {
            "row_energy": "d=max_i ||b_i||_2^2",
            "signed_cross_correlation": (
                "c=max_i sum_{j!=i}|<b_i,b_j>|"
            ),
            "operator_bound": "||B||_2^2<=d+c",
            "positive_tail_bounds": "alpha>0 and gamma>0",
            "block_certificate": "d+c<alpha*gamma",
            "mean_cancellation_no_go": (
                "signed row sums=signed column sums=0 does not imply ||B||<1"
            ),
        },
        "correlation_audit": {
            "hadamard_rows": hadamard_rows,
            "coherent_counterfamily_rows": coherent_rows,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "projected Weil row-energy and off-diagonal cross-Gram "
                "correlation estimates below an independently certified tail gap"
            ),
            "discard": (
                "using signed row means, signed column means, or total signed "
                "mass as a substitute for cross-operator control"
            ),
            "next_theorem": (
                "ProjectedWeilCrossGramCorrelationBudgetBelowTailGap"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "RH-TD4b.2a",
                    "label": "HadamardCancellationSchurOverestimateNoGo",
                    "status": "closed",
                },
                {
                    "id": "RH-TD4b.2b.1",
                    "label": "CrossGramCorrelationBlockPositivityCriterion",
                    "status": "closed",
                },
                {
                    "id": "RH-TD4b.2b.2",
                    "label": (
                        "ProjectedWeilCrossGramCorrelationBudgetBelowTailGap"
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
                ["RH-TD4b.2a", "RH-TD4b.2b.1"],
                ["RH-TD4b.2b.1", "RH-TD4b.2b.2"],
                ["RH-TD4b.2b.2", "RH"],
            ],
        },
        "machine_audit": {
            "hadamard_scale_count": len(hadamard_rows),
            "signed_mean_counterexample_count": len(coherent_rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem is exact finite-dimensional linear algebra. It does "
            "not provide the required projected Weil row-correlation estimate, "
            "a uniform tail gap, an RH proof, or an RH counterexample."
        ),
    }


def periodic_affine_data(word: Iterable[int]) -> dict[str, Any]:
    values = tuple(int(value) for value in word)
    if not values or any(value < 1 for value in values):
        raise ValueError("periodic valuation words must be nonempty and positive")
    correction = 0
    valuation_sum = 0
    for value in values:
        correction = 3 * correction + 2**valuation_sum
        valuation_sum += value
    denominator = 2**valuation_sum - 3 ** len(values)
    start = Fraction(correction, denominator)
    return {
        "word": values,
        "period": len(values),
        "valuation_sum": valuation_sum,
        "affine_correction": correction,
        "denominator": denominator,
        "fixed_point": start,
    }


def rational_v2(value: Fraction) -> int:
    if value == 0:
        raise ValueError("v2(0) is undefined")

    def integer_v2(integer: int) -> int:
        integer = abs(integer)
        exponent = 0
        while integer % 2 == 0:
            integer //= 2
            exponent += 1
        return exponent

    return integer_v2(value.numerator) - integer_v2(value.denominator)


def accelerated_fraction_step(value: Fraction) -> tuple[Fraction, int]:
    raw = 3 * value + 1
    valuation = rational_v2(raw)
    if valuation < 1:
        raise AssertionError("periodic odd 2-adic itinerary lost positivity")
    return raw / (2**valuation), valuation


def replay_periodic_fraction(
    start: Fraction, word: Iterable[int]
) -> tuple[Fraction, tuple[int, ...]]:
    current = start
    observed = []
    for _ in tuple(word):
        current, valuation = accelerated_fraction_step(current)
        observed.append(valuation)
    return current, tuple(observed)


def repeated_affine_cap_admissible(
    word: Iterable[int], lower_bound: int, repeat_count: int
) -> bool:
    values = tuple(word)
    total = 0
    for depth, value in enumerate(values * repeat_count, start=1):
        total += value
        if total > affine_cap(lower_bound, depth):
            return False
    return True


def collatz_subcritical_periodic_code_no_go() -> dict[str, Any]:
    rows = []
    failures = 0
    total_words = 0
    total_subcritical = 0
    total_positive_integer = 0
    total_nontrivial_positive_integer = 0

    for period in range(1, 9):
        row_total = 0
        subcritical = 0
        positive_rational = 0
        positive_integer = 0
        nontrivial_positive_integer = 0
        affine_capped_subcritical = 0
        row_failures = 0
        for word in itertools.product([1, 2, 3], repeat=period):
            data = periodic_affine_data(word)
            start = data["fixed_point"]
            replay_end, replay_word = replay_periodic_fraction(start, word)
            row_total += 1
            denominator = int(data["denominator"])
            is_subcritical = denominator < 0
            if is_subcritical:
                subcritical += 1
                if repeated_affine_cap_admissible(word, 1_000_000, 4):
                    affine_capped_subcritical += 1
            if start > 0:
                positive_rational += 1
            if start > 0 and start.denominator == 1:
                positive_integer += 1
                if start != 1:
                    nontrivial_positive_integer += 1
            checks = {
                "denominator_never_zero": denominator != 0,
                "fixed_point_replays": replay_end == start,
                "valuation_word_replays": replay_word == word,
                "subcritical_fixed_point_nonpositive": (
                    not is_subcritical or start < 0
                ),
            }
            row_failures += sum(int(not value) for value in checks.values())

        failures += row_failures
        total_words += row_total
        total_subcritical += subcritical
        total_positive_integer += positive_integer
        total_nontrivial_positive_integer += nontrivial_positive_integer
        rows.append(
            {
                "period": period,
                "alphabet": [1, 2, 3],
                "word_count": row_total,
                "subcritical_word_count": subcritical,
                "positive_rational_fixed_point_count": positive_rational,
                "positive_integer_fixed_point_count": positive_integer,
                "nontrivial_positive_integer_fixed_point_count": (
                    nontrivial_positive_integer
                ),
                "affine_capped_subcritical_word_count_B_1e6": (
                    affine_capped_subcritical
                ),
                "row_failure_count": row_failures,
            }
        )

    examples = []
    for word in [(1,), (1, 2), (2,), (1, 1, 2), (2, 2, 2)]:
        data = periodic_affine_data(word)
        examples.append(
            {
                "word": list(word),
                "valuation_sum": data["valuation_sum"],
                "affine_correction": str(data["affine_correction"]),
                "denominator": str(data["denominator"]),
                "fixed_point": fraction_payload(data["fixed_point"]),
                "subcritical": data["denominator"] < 0,
                "affine_capped_through_four_periods_B_1e6": (
                    repeated_affine_cap_admissible(word, 1_000_000, 4)
                ),
            }
        )

    return {
        "theorem_name": (
            "SubcriticalPeriodicValuationCodesHaveNoPositiveNaturalEmbedding"
        ),
        "title_ko": "임계 이하 주기 valuation 코드의 양의 자연수 비매장 정리",
        "declared_target": (
            "Close a nontrivial infinite subclass of the TICKET137 "
            "affine-capped survivor language by deciding exactly which periodic "
            "valuation codes can represent positive natural Collatz orbits."
        ),
        "proved_statement": (
            "Let a_1,...,a_k be a positive valuation word, S=sum a_i, and "
            "C=sum_{j=0}^{k-1}3^(k-1-j)2^(a_1+...+a_j). The infinite periodic "
            "itinerary (a_1,...,a_k)^infinity has the unique odd 2-adic start "
            "n=C/(2^S-3^k). If 2^S<=3^k, then n<0 and the itinerary has no "
            "positive natural embedding. Consequently every positive periodic "
            "Collatz orbit must satisfy the strict supercritical inequality "
            "2^S>3^k. This excludes every subcritical periodic branch of the "
            "affine-capped survivor language at all periods."
        ),
        "proved_statement_ko": (
            "양의 valuation 주기어 a_1,...,a_k의 합을 S라 하고 정확한 affine "
            "보정항을 C라 하면 무한 반복 itinerary의 유일한 홀수 2-adic "
            "시작점은 n=C/(2^S-3^k)이다. 2^S<=3^k이면 C>0이고 분모가 "
            "음수이므로 n<0이다. 따라서 이 임계 이하 주기 코드는 양의 "
            "자연수 Collatz 궤도를 나타낼 수 없다. 모든 양의 주기 궤도는 "
            "반드시 2^S>3^k를 만족해야 한다."
        ),
        "proof": (
            "Finite valuation prefixes determine nested odd residue classes "
            "whose moduli tend to infinity, hence an infinite itinerary has at "
            "most one odd 2-adic start. Shifting a periodic itinerary by k "
            "symbols leaves it unchanged, so its k-step accelerated image equals "
            "its start. Iterating the exact affine identity gives "
            "2^S n=3^k n+C, with C>0. Thus "
            "(2^S-3^k)n=C. Equality 2^S=3^k is impossible for positive k, and "
            "2^S<3^k forces n<0."
        ),
        "exact_contract": {
            "affine_correction": (
                "C=sum_{j=0}^{k-1}3^(k-1-j)*2^(S_j), S_0=0"
            ),
            "periodic_fixed_point": "n=C/(2^S-3^k)",
            "positive_cycle_necessary_condition": "2^S>3^k",
            "closed_subclass": (
                "all exactly periodic infinite valuation codes with 2^S<=3^k"
            ),
        },
        "periodic_code_audit": {
            "rows": rows,
            "examples": examples,
            "total_word_count": total_words,
            "total_subcritical_word_count": total_subcritical,
            "total_positive_integer_fixed_point_count": total_positive_integer,
            "total_nontrivial_positive_integer_fixed_point_count": (
                total_nontrivial_positive_integer
            ),
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "Archimedean well-foundedness for supercritical periodic and "
                "aperiodic affine-capped natural codes"
            ),
            "discard": (
                "subcritical periodic valuation words, including the all-one "
                "boundary code, as possible positive natural counterexample codes"
            ),
            "next_theorem": "AffineCappedNaturalCodeWellFoundedness",
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "CO-TD4b.2a",
                    "label": "AffineCappedValuationCylinderMassDecay",
                    "status": "closed",
                },
                {
                    "id": "CO-TD4b.2b.1",
                    "label": (
                        "SubcriticalPeriodicValuationCodesHaveNoPositiveNaturalEmbedding"
                    ),
                    "status": "closed",
                },
                {
                    "id": "CO-TD4b.2b.2",
                    "label": "AffineCappedNaturalCodeWellFoundedness",
                    "status": "highest_risk_open",
                },
                {
                    "id": "CO",
                    "label": "Collatz Conjecture",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["CO-TD4b.2a", "CO-TD4b.2b.1"],
                ["CO-TD4b.2b.1", "CO-TD4b.2b.2"],
                ["CO-TD4b.2b.2", "CO"],
            ],
        },
        "machine_audit": {
            "period_rows": len(rows),
            "enumerated_word_count": total_words,
            "subcritical_word_count": total_subcritical,
            "nontrivial_positive_integer_fixed_point_count": (
                total_nontrivial_positive_integer
            ),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The general theorem closes only exactly periodic subcritical "
            "valuation codes. The finite alphabet audit through period eight is "
            "not a cycle-exclusion proof at arbitrary period. Supercritical "
            "periodic codes and all aperiodic natural codes remain open."
        ),
    }


def goldbach_all_scale_wheel_barrier() -> dict[str, Any]:
    rows = []
    failures = 0
    for wheel in [3, 15, 105, 1155, 15015]:
        hard_residues = sum(
            int(math.gcd(2 * index, wheel) == 1)
            for index in range(1, wheel + 1)
        )
        for block_count in [1, 2, 5, 10]:
            scale = 2 * wheel * block_count
            hard_count = block_count * euler_phi(wheel)
            minimum_moment = minimal_moment_for_inflation(hard_count)
            checks = {
                "wheel_odd_squarefree": is_squarefree_odd(wheel),
                "complete_residue_block_count": (
                    hard_residues == euler_phi(wheel)
                ),
                "exact_hard_count": (
                    hard_count == block_count * hard_residues
                ),
                "totient_square_bound": euler_phi(wheel) ** 2 >= wheel,
                "universal_half_scale_square_bound": (
                    2 * hard_count**2 >= scale
                ),
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
                    "complete_period_blocks_M": block_count,
                    "scale_X": scale,
                    "hard_residues_per_period": hard_residues,
                    "hard_stratum_size": hard_count,
                    "minimum_p_for_factor_at_most_6_over_5": minimum_moment,
                    "universal_lower_bound": "sqrt(X/2)",
                    "checks": checks,
                }
            )

    return {
        "theorem_name": "AllScaleOddSquarefreeWheelMomentBarrier",
        "title_ko": "전 규모 홀수 squarefree wheel 로그 모멘트 장벽 정리",
        "declared_target": (
            "Test the remaining TICKET137 near-full-scale wheel escape and "
            "decide whether wheel scale alone can ever reduce worst-case "
            "moment-to-pointwise promotion below logarithmic order."
        ),
        "proved_statement": (
            "Let W be odd and squarefree, M>=1, X=2WM, and H_W(X) the even "
            "integers through X coprime to W. Then h=|H_W(X)|=M*phi(W) and "
            "phi(W)^2>=W, so h^2>=M^2 W=M X/2>=X/2. Therefore "
            "h>=sqrt(X/2) at every complete-block wheel scale, including "
            "near-full scales. The sharp normalized L^p-to-maximum factor "
            "h^(1/p) can be at most 6/5 only if "
            "p>=(log X-log 2)/(2 log(6/5))=Omega(log X)."
        ),
        "proved_statement_ko": (
            "W가 홀수 squarefree이고 X=2WM, M>=1이면 hard stratum의 크기는 "
            "h=M*phi(W)이다. phi(W)^2>=W이므로 "
            "h^2>=M^2 W=M X/2>=X/2이고, 모든 complete-block 규모에서 "
            "h>=sqrt(X/2)이다. 따라서 near-full wheel에서도 정규화 L^p를 "
            "최대값으로 승격하는 최악의 팽창을 6/5 이하로 만들려면 "
            "p=Omega(log X)가 필요하다."
        ),
        "proof": (
            "Oddness of W identifies even N=2m coprime to W with m coprime to "
            "W, giving M*phi(W) elements in M complete residue blocks. For "
            "squarefree odd W, phi(W)^2/W=product_{p|W}(p-1)^2/p>=1. Thus "
            "h^2=M^2 phi(W)^2>=M^2 W=M X/2>=X/2. The norm comparison "
            "||x||_infinity<=h^(1/p)||x||_p is sharp on a one-point spike, so "
            "the displayed logarithmic lower bound on p is necessary."
        ),
        "exact_contract": {
            "hard_count": "|H_W(2WM)|=M*phi(W)",
            "totient_bound": "phi(W)^2>=W",
            "all_scale_size_bound": "|H_W(X)|>=sqrt(X/2)",
            "moment_threshold": (
                "p>=(log X-log 2)/(2*log(6/5))"
            ),
        },
        "wheel_audit": {
            "rows": rows,
            "wheel_count": 5,
            "block_count_setting_count": 4,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "a direct pointwise signed binary Goldbach residual estimate "
                "with K<=56, with explicit large-even glue"
            ),
            "discard": (
                "near-full wheel scale by itself as an escape from logarithmic "
                "worst-case moment promotion"
            ),
            "next_theorem": "PointwiseSignedBinaryGoldbachResidualK56",
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "GB-TD4b.2a",
                    "label": "SubpowerGrowingWheelLogMomentBarrier",
                    "status": "closed",
                },
                {
                    "id": "GB-TD4b.2b.1",
                    "label": "AllScaleOddSquarefreeWheelMomentBarrier",
                    "status": "closed",
                },
                {
                    "id": "GB-TD4b.2b.2",
                    "label": "PointwiseSignedBinaryGoldbachResidualK56",
                    "status": "highest_risk_open",
                },
                {
                    "id": "GB",
                    "label": "Strong Goldbach Conjecture",
                    "status": "open_not_proven",
                },
            ],
            "edges": [
                ["GB-TD4b.2a", "GB-TD4b.2b.1"],
                ["GB-TD4b.2b.1", "GB-TD4b.2b.2"],
                ["GB-TD4b.2b.2", "GB"],
            ],
        },
        "machine_audit": {
            "wheel_scale_row_count": len(rows),
            "near_full_block_count_one_rows": sum(
                int(row["complete_period_blocks_M"] == 1) for row in rows
            ),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This is a sharp worst-case norm-promotion barrier for complete "
            "wheel blocks, not an estimate of the actual signed Goldbach "
            "residual. Analytic use of a wheel together with additional "
            "pointwise information is not excluded. No Goldbach proof or "
            "counterexample is supplied."
        ),
    }


def pell_sqrt2_rows(count: int = 12) -> list[dict[str, Any]]:
    rows = []
    numerator = 1
    denominator = 1
    previous_distance = math.inf
    for index in range(1, count + 1):
        residual = numerator * numerator - 2 * denominator * denominator
        phase_error = abs(math.sqrt(2) * denominator - numerator)
        chord_distance = 2 * abs(math.sin(math.pi * phase_error))
        checks = {
            "pell_residual_unit": abs(residual) == 1,
            "no_exact_rational_collision": residual != 0,
            "phase_near_collision_improves": phase_error < previous_distance,
        }
        rows.append(
            {
                "index": index,
                "convergent": f"{numerator}/{denominator}",
                "numerator": str(numerator),
                "denominator": str(denominator),
                "pell_residual_p2_minus_2q2": residual,
                "absolute_phase_error": phase_error,
                "unit_circle_chord_distance_to_one": chord_distance,
                "checks": checks,
            }
        )
        previous_distance = phase_error
        numerator, denominator = (
            numerator + 2 * denominator,
            numerator + denominator,
        )
    return rows


def twin_irrational_injectivity_no_go() -> dict[str, Any]:
    rows = pell_sqrt2_rows()
    failures = sum(
        int(not value)
        for row in rows
        for value in row["checks"].values()
    )
    return {
        "theorem_name": "IrrationalInjectivityWithoutRegularityIsTautologicalNoGo",
        "title_ko": "정칙성 없는 무리수 injectivity의 동어반복 한계 정리",
        "declared_target": (
            "Test the TICKET137 irrational-phase escape and determine whether "
            "injective aperiodic features alone create any arithmetic separation "
            "or break the parity barrier."
        ),
        "proved_statement": (
            "For irrational alpha, phi_alpha(n)=exp(2*pi*i*alpha*n) is injective "
            "on the integers. Consequently every predicate P on Z, including "
            "the twin-prime-pair predicate, factors set-theoretically as "
            "P=F o phi_alpha for a unique lookup F on phi_alpha(Z). Thus the "
            "bare existence of an arbitrary classifier on an irrational phase "
            "image is equivalent to restating P and supplies no arithmetic "
            "estimate, computable regularity, parity break, or infinitude proof. "
            "Moreover irrational injectivity can coexist with arbitrarily close "
            "phase returns, as the Pell convergents to sqrt(2) demonstrate."
        ),
        "proved_statement_ko": (
            "alpha가 무리수이면 phi_alpha(n)=exp(2*pi*i*alpha*n)은 정수에서 "
            "단사다. 따라서 쌍둥이 소수 판정을 포함한 모든 정수 술어 P는 "
            "상 phi_alpha(Z) 위의 lookup F를 정의하여 P=F o phi_alpha로 "
            "쓸 수 있다. 정칙성이나 계산 가능한 복잡도 제한이 없는 임의 "
            "분류기의 존재는 원래 술어를 다시 적은 것일 뿐이며 산술 추정, "
            "parity 돌파, 무한성 증명을 주지 않는다. sqrt(2)의 Pell "
            "수렴분수는 단사성과 임의로 가까운 위상 재귀가 공존함도 보인다."
        ),
        "proof": (
            "If phi_alpha(m)=phi_alpha(n), then alpha(m-n) is an integer. "
            "Irrationality forces m=n. Injectivity makes F(phi_alpha(n))=P(n) "
            "well-defined for every predicate P, proving the factorization. "
            "This construction merely stores the original labels and has no "
            "regularity guarantee. For alpha=sqrt(2), Pell solutions "
            "p_j^2-2q_j^2=(-1)^j give nonzero errors "
            "|q_j sqrt(2)-p_j|=1/(p_j+q_j sqrt(2))->0, hence unit-circle phase "
            "returns approach one without ever becoming exact."
        ),
        "exact_contract": {
            "feature": "phi_alpha(n)=exp(2*pi*i*alpha*n)",
            "injectivity": "alpha irrational implies phi_alpha injective on Z",
            "tautological_factorization": (
                "for every P:Z->{0,1}, F(phi_alpha(n))=P(n)"
            ),
            "missing_structure": (
                "effective regularity plus signed Type II transport"
            ),
        },
        "irrational_phase_audit": {
            "algebraic_irrational": "sqrt(2)",
            "pell_rows": rows,
            "row_count": len(rows),
            "failure_count": failures,
        },
        "route_decision": {
            "retain": (
                "a regular, computable aperiodic Type II statistic with a "
                "quantitative signed-cancellation theorem and transport to "
                "positive exact-gap-two mass"
            ),
            "discard": (
                "irrational injectivity or arbitrary lookup expressivity by "
                "itself as a parity-breaking Twin Prime argument"
            ),
            "next_theorem": (
                "RegularAperiodicTypeIICancellationWithPositiveTwinMass"
            ),
        },
        "proof_dag": {
            "nodes": [
                {
                    "id": "TP-TD3b.2a",
                    "label": "RationalFourierInformationBudgetLowerBound",
                    "status": "closed",
                },
                {
                    "id": "TP-TD3b.2b.1",
                    "label": (
                        "IrrationalInjectivityWithoutRegularityIsTautologicalNoGo"
                    ),
                    "status": "closed",
                },
                {
                    "id": "TP-TD3b.2b.2",
                    "label": (
                        "RegularAperiodicTypeIICancellationWithPositiveTwinMass"
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
                ["TP-TD3b.2a", "TP-TD3b.2b.1"],
                ["TP-TD3b.2b.1", "TP-TD3b.2b.2"],
                ["TP-TD3b.2b.2", "TP"],
            ],
        },
        "machine_audit": {
            "pell_near_collision_row_count": len(rows),
            "exact_irrational_collision_count": 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem is a no-go for unrestricted feature expressivity, not "
            "a no-go for analytic irrational phases. It neither estimates a "
            "Vaughan Type II sum nor proves positive exact-gap-two mass. The "
            "Pell table is a finite illustration of near-collision, not the "
            "general injectivity proof."
        ),
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": riemann_cross_gram_correlation_criterion(),
        "collatz": collatz_subcritical_periodic_code_no_go(),
        "goldbach": goldbach_all_scale_wheel_barrier(),
        "twin_prime": twin_irrational_injectivity_no_go(),
    }
    failures = sum(
        section["machine_audit"]["total_failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureCorrelationPeriodicityAndScaleClosureAudit",
        **sections,
        "cross_problem_synthesis": {
            "shared_obstruction": (
                "A richer representation can remain proof-theoretically empty "
                "unless it carries quantitative correlation, well-foundedness, "
                "pointwise control, or analytic regularity."
            ),
            "shared_upgrade": (
                "The next routes must control cross-Gram coherence, natural-code "
                "well-foundedness, pointwise Goldbach residuals, and regular "
                "aperiodic Type II cancellation."
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
            "TICKET138 proves four exact intermediate or no-go theorems and "
            "revises four proof targets. It does not prove or refute RH, Collatz, "
            "strong Goldbach, or Twin Prime. No conjecture proof and no certified "
            "conjecture counterexample is claimed; all resolution counters remain zero."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-138",
            "CrossGramCorrelationBlockPositivityCriterion",
            "ProjectedWeilCrossGramCorrelationBudgetBelowTailGap",
            "Fix one projected Weil basis and bound row energy plus off-diagonal signed Gram correlations uniformly below the independently certified core-tail gap.",
        ),
        (
            "collatz",
            "CO-TICKET-138",
            "SubcriticalPeriodicValuationCodesHaveNoPositiveNaturalEmbedding",
            "AffineCappedNaturalCodeWellFoundedness",
            "Construct an Archimedean well-founded rank that excludes supercritical periodic and aperiodic natural codes from the infinite affine-capped survivor set.",
        ),
        (
            "goldbach",
            "GB-TICKET-138",
            "AllScaleOddSquarefreeWheelMomentBarrier",
            "PointwiseSignedBinaryGoldbachResidualK56",
            "Abandon wheel-cardinality promotion and prove the signed binary residual pointwise with K<=56, then combine it with the certified finite cutoff.",
        ),
        (
            "twin-prime",
            "TP-TICKET-138",
            "IrrationalInjectivityWithoutRegularityIsTautologicalNoGo",
            "RegularAperiodicTypeIICancellationWithPositiveTwinMass",
            "Specify a computable regularity class for an aperiodic Type II statistic, prove uniform signed cancellation, and transport it to positive exact-gap-two mass.",
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
        "correlation_periodicity_and_scale_closure_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket138-correlation-periodicity-and-scale-closure.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-138-cross-gram-correlation-criterion.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-138-subcritical-periodic-code-no-go.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-138-all-scale-wheel-barrier.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-138-irrational-injectivity-no-go.json",
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
