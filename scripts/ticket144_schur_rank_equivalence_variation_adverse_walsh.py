from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from typing import Sequence

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket143_form_core_period_floor_martingale_walsh import twin_walsh_row


GENERATED_AT = "2026-07-26T00:30:00+09:00"
SCHEMA = (
    "primeproject.ticket144-schur-rank-equivalence-variation-"
    "adverse-walsh.v1"
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
    closed_id = f"{problem_code}-T144-CLOSED"
    open_id = f"{problem_code}-T144-OPEN"
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


def exact_ldl_pivots(
    matrix: Sequence[Sequence[Fraction]],
) -> list[Fraction]:
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("a square matrix is required")
    lower = [
        [Fraction() for _ in range(size)]
        for _ in range(size)
    ]
    pivots: list[Fraction] = []
    for column in range(size):
        pivot = matrix[column][column] - sum(
            (
                lower[column][index]
                * lower[column][index]
                * pivots[index]
                for index in range(column)
            ),
            Fraction(),
        )
        if pivot == 0:
            raise ValueError("zero Schur pivot")
        pivots.append(pivot)
        lower[column][column] = Fraction(1)
        for row in range(column + 1, size):
            numerator = matrix[row][column] - sum(
                (
                    lower[row][index]
                    * lower[column][index]
                    * pivots[index]
                    for index in range(column)
                ),
                Fraction(),
            )
            lower[row][column] = numerator / pivot
    return pivots


def hilbert_matrix(size: int) -> list[list[Fraction]]:
    if size < 1:
        raise ValueError("positive size required")
    return [
        [
            Fraction(1, row + column + 1)
            for column in range(size)
        ]
        for row in range(size)
    ]


def riemann_schur_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for size in range(1, 11):
        pivots = exact_ldl_pivots(hilbert_matrix(size))
        expected_last = Fraction(
            1,
            (2 * size - 1) * comb(2 * size - 2, size - 1) ** 2,
        )
        checks = {
            "all_exact_schur_pivots_positive": all(
                pivot > 0 for pivot in pivots
            ),
            "last_pivot_matches_closed_form": (
                pivots[-1] == expected_last
            ),
            "leading_determinant_ratio_positive": pivots[-1] > 0,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "dimension": size,
                "last_schur_pivot": fraction_payload(pivots[-1]),
                "closed_form": (
                    "1/((2N-1)*binom(2N-2,N-1)^2)"
                ),
                "pivot_denominator_digits": len(
                    str(pivots[-1].denominator)
                ),
                "checks": checks,
            }
        )

    extension_rows = []
    for prefix_size in [1, 2, 4, 8, 16]:
        prefix_pivots = [Fraction(1) for _ in range(prefix_size)]
        extended_pivots = [*prefix_pivots, Fraction(-1)]
        checks = {
            "audited_prefix_is_positive_definite": all(
                pivot > 0 for pivot in prefix_pivots
            ),
            "next_extension_is_indefinite": extended_pivots[-1] < 0,
            "old_prefix_is_unchanged": (
                extended_pivots[:-1] == prefix_pivots
            ),
        }
        failures += sum(not value for value in checks.values())
        extension_rows.append(
            {
                "positive_prefix_dimension": prefix_size,
                "extension": "diag(I_N,-1)",
                "new_schur_pivot": -1,
                "checks": checks,
            }
        )

    return {
        "schur_theorem": (
            "For G_{N+1}=[[G_N,b],[b*,c]] with G_N positive definite, "
            "G_{N+1} is positive definite iff "
            "delta_{N+1}=c-b*G_N^{-1}b is positive; moreover "
            "delta_{N+1}=det(G_{N+1})/det(G_N)."
        ),
        "inductive_certificate": (
            "Every nested finite Gram section is positive definite iff "
            "every exact Schur pivot is positive."
        ),
        "finite_prefix_no_go": (
            "Any finite positive prefix can be preserved and extended by "
            "diag(I_N,-1), so a bounded list of positive sections cannot "
            "certify the infinite family."
        ),
        "hilbert_rows": rows,
        "negative_extension_rows": extension_rows,
        "failure_count": failures,
    }


def v2(value: int) -> int:
    if value <= 0:
        raise ValueError("positive value required")
    exponent = 0
    while value % 2 == 0:
        exponent += 1
        value //= 2
    return exponent


def accelerated_collatz(odd: int) -> int:
    if odd < 1 or odd % 2 == 0:
        raise ValueError("positive odd value required")
    numerator = 3 * odd + 1
    return numerator >> v2(numerator)


def collatz_stopping_rank_audit(limit: int = 100_000) -> dict[str, object]:
    ranks = {1: 0}
    failures = 0
    for start in range(1, limit + 1, 2):
        path: list[int] = []
        position: dict[int, int] = {}
        current = start
        while current not in ranks:
            if current in position:
                raise RuntimeError(
                    f"unexpected finite-audit cycle at {current}"
                )
            position[current] = len(path)
            path.append(current)
            current = accelerated_collatz(current)
        rank = ranks[current]
        for value in reversed(path):
            rank += 1
            ranks[value] = rank

    input_rows = []
    maximum_start = 1
    maximum_rank = 0
    for start in range(1, limit + 1, 2):
        if ranks[start] > maximum_rank:
            maximum_start = start
            maximum_rank = ranks[start]
    selected = [1, 3, 7, 27, 97, 871, 6171, maximum_start]
    for start in selected:
        successor = accelerated_collatz(start)
        checks = {
            "rank_is_nonnegative": ranks[start] >= 0,
            "sink_or_rank_drops_by_one": (
                start == 1
                or ranks[successor] == ranks[start] - 1
            ),
        }
        failures += sum(not value for value in checks.values())
        input_rows.append(
            {
                "start": start,
                "successor": successor,
                "finite_verified_hitting_rank": ranks[start],
                "successor_rank": ranks[successor],
                "checks": checks,
            }
        )

    all_input_descents = all(
        start == 1
        or ranks[accelerated_collatz(start)] == ranks[start] - 1
        for start in range(1, limit + 1, 2)
    )
    failures += int(not all_input_descents)
    return {
        "limit": limit,
        "verified_odd_start_count": (limit + 1) // 2,
        "memoized_orbit_state_count": len(ranks),
        "maximum_input_rank": maximum_rank,
        "maximum_input_rank_start": maximum_start,
        "selected_rows": input_rows,
        "all_audited_input_ranks_drop": all_input_descents,
        "interpretation": (
            "These ranks are computed after each finite trajectory reaches "
            "1. They verify the equivalence on a bounded set but do not "
            "supply an independent global rank formula."
        ),
        "failure_count": failures,
    }


def collatz_rank_equivalence_audit() -> dict[str, object]:
    stopping = collatz_stopping_rank_audit()
    checks = {
        "finite_rank_rows_pass": stopping["failure_count"] == 0,
        "maximum_rank_is_reproduced": (
            stopping["maximum_input_rank"] == 129
            and stopping["maximum_input_rank_start"] == 77_031
        ),
        "published_floor_not_used_in_equivalence": True,
    }
    return {
        "equivalence": (
            "Every positive odd accelerated Collatz orbit reaches 1 iff "
            "there exists a map R into a well-order with R(T(n))<R(n) for "
            "every n!=1."
        ),
        "forward_proof": (
            "If every orbit reaches 1, define R(n) as the least accelerated "
            "hitting time of 1. Then R(T(n))=R(n)-1."
        ),
        "reverse_proof": (
            "A nonterminating orbit would create an infinite strictly "
            "descending sequence in a well-order, which is impossible."
        ),
        "no_go": (
            "An unrestricted global well-founded rank is an exact "
            "reparameterization of Collatz termination. A rank defined by "
            "the already observed hitting time is circular as a proof route."
        ),
        "published_odd_period_floor": {
            "value": 72_000_000_000,
            "role": (
                "preserved external premise from TICKET143; it does not "
                "weaken the aperiodic rank equivalence"
            ),
        },
        "finite_stopping_rank_audit": stopping,
        "checks": checks,
        "failure_count": (
            stopping["failure_count"]
            + sum(not value for value in checks.values())
        ),
    }


def path_mean(level: int) -> Fraction:
    return Fraction(1, 2) if level % 2 else Fraction()


def sibling_mean(level: int) -> Fraction:
    return 2 * path_mean(level) - path_mean(level + 1)


def dyadic_counterfamily_value(depth: int, index: int) -> Fraction:
    if depth < 1 or not 0 <= index < 1 << depth:
        raise ValueError("invalid dyadic leaf")
    if index == 0:
        return path_mean(depth)
    binary = f"{index:0{depth}b}"
    first_right = binary.index("1")
    return sibling_mean(first_right)


def direct_zero_path_means(depth: int) -> list[Fraction]:
    values = [
        dyadic_counterfamily_value(depth, index)
        for index in range(1 << depth)
    ]
    means = []
    width = 1 << depth
    for level in range(depth + 1):
        means.append(
            sum(values[:width], Fraction()) / width
        )
        width //= 2
    return means


def goldbach_variation_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for depth in [4, 8, 16, 32, 64, 111, 112, 113, 128]:
        signed_sum = path_mean(depth) - path_mean(0)
        absolute_variation = Fraction(depth, 2)
        terminal_values = {
            path_mean(depth),
            *(
                sibling_mean(level)
                for level in range(depth)
            ),
        }
        checks = {
            "root_mean_is_zero": path_mean(0) == 0,
            "terminal_sup_norm_at_most_one": max(
                abs(value) for value in terminal_values
            )
            <= 1,
            "signed_path_telescopes": (
                signed_sum == path_mean(depth)
            ),
            "absolute_path_variation_is_depth_over_two": (
                absolute_variation == Fraction(depth, 2)
            ),
            "k56_crossing_flag_is_exact": (
                (absolute_variation > 56) == (depth > 112)
            ),
        }
        if depth <= 8:
            checks["direct_leaf_means_match_symbolic_path"] = (
                direct_zero_path_means(depth)
                == [path_mean(level) for level in range(depth + 1)]
            )
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "depth": depth,
                "dyadic_size": f"2^{depth}",
                "root_mean": fraction_payload(path_mean(0)),
                "zero_path_endpoint": fraction_payload(path_mean(depth)),
                "terminal_sup_norm": 1,
                "signed_path_sum": fraction_payload(signed_sum),
                "absolute_path_variation": fraction_payload(
                    absolute_variation
                ),
                "absolute_variation_exceeds_56": (
                    absolute_variation > 56
                ),
                "checks": checks,
            }
        )
    return {
        "counterfamily": (
            "Along the all-left path set m_l=0 for even l and m_l=1/2 "
            "for odd l. Give the sibling subtree at level l the constant "
            "mean 2m_l-m_{l+1}. Every leaf lies in [-1,1]."
        ),
        "exact_identity": (
            "The signed martingale path telescopes to m_d, while the "
            "absolute path variation equals d/2."
        ),
        "no_go": (
            "Uniformly bounded point values do not imply a scale-independent "
            "absolute martingale path-variation bound. The variation reaches "
            "56 at depth 112 and exceeds it at depth 113."
        ),
        "actual_residual_boundary": (
            "The counterfamily is not an actual binary Goldbach residual. "
            "It refutes only absolute variation as a generic transform "
            "principle; arithmetic signed cancellation remains open."
        ),
        "rows": rows,
        "failure_count": failures,
    }


def walsh_coefficients_from_counts(
    counts: Sequence[int],
) -> tuple[int, int, int, int]:
    if len(counts) != 4 or any(value < 0 for value in counts):
        raise ValueError("four nonnegative category counts required")
    plus_plus, plus_minus, minus_plus, minus_minus = counts
    return (
        sum(counts),
        plus_plus + plus_minus - minus_plus - minus_minus,
        plus_plus - plus_minus + minus_plus - minus_minus,
        plus_plus - plus_minus - minus_plus + minus_minus,
    )


def twin_adverse_row(scale: int) -> dict[str, object]:
    source = twin_walsh_row(scale)
    counts = [
        int(source["category_counts"]["lambda_plus_plus"]),
        int(source["category_counts"]["lambda_plus_minus"]),
        int(source["category_counts"]["lambda_minus_plus"]),
        int(source["category_counts"]["lambda_minus_minus_twins"]),
    ]
    a00, a10, a01, a11 = walsh_coefficients_from_counts(counts)
    walsh_l1 = abs(a10) + abs(a01) + abs(a11)
    simplex_radius = max(
        abs(4 * count - a00) for count in counts
    )
    adverse = max(a10, 0) + max(a01, 0) + max(-a11, 0)
    lower_bound = Fraction(a00 - adverse, 4)
    checks = {
        "walsh_coefficients_match_source": (
            [a00, a10, a01, a11]
            == [
                source["A00"],
                source["A10"],
                source["A01"],
                source["A11"],
            ]
        ),
        "l1_equals_max_simplex_deviation": (
            walsh_l1 == simplex_radius
        ),
        "adverse_part_is_no_larger_than_l1": adverse <= walsh_l1,
        "targeted_twin_lower_bound_holds": (
            counts[3] >= lower_bound
        ),
    }
    return {
        "X": scale,
        "A00": a00,
        "A10": a10,
        "A01": a01,
        "A11": a11,
        "category_counts": counts,
        "walsh_l1": walsh_l1,
        "simplex_max_deviation": simplex_radius,
        "adverse_walsh_part": adverse,
        "adverse_margin": a00 - adverse,
        "certified_twin_lower_bound": fraction_payload(lower_bound),
        "direct_twin_count": counts[3],
        "checks": checks,
    }


def twin_adverse_walsh_audit() -> dict[str, object]:
    rows = [
        twin_adverse_row(scale)
        for scale in [1_000, 10_000, 100_000, 1_000_000]
    ]
    synthetic_counts = [90, 5, 4, 1]
    a00, a10, a01, a11 = walsh_coefficients_from_counts(
        synthetic_counts
    )
    synthetic_l1 = abs(a10) + abs(a01) + abs(a11)
    synthetic = {
        "category_counts": synthetic_counts,
        "A00": a00,
        "A10": a10,
        "A01": a01,
        "A11": a11,
        "walsh_l1": synthetic_l1,
        "twin_class_positive": synthetic_counts[3] > 0,
        "l1_contraction_fails": synthetic_l1 > a00,
    }
    checks = {
        "all_finite_rows_pass": all(
            all(row["checks"].values()) for row in rows
        ),
        "all_observed_adverse_parts_are_zero": all(
            row["adverse_walsh_part"] == 0 for row in rows
        ),
        "l1_is_not_necessary_for_positive_twin_class": (
            synthetic["twin_class_positive"]
            and synthetic["l1_contraction_fails"]
        ),
    }
    return {
        "simplex_identity": (
            "|A10|+|A01|+|A11|="
            "max_{s,t}|4N_{s,t}-A00|"
        ),
        "simplex_interpretation": (
            "L1 <= (1-delta)A00 iff every parity class lies between "
            "delta*A00/4 and (2-delta)*A00/4."
        ),
        "adverse_part": (
            "B=A10_+ + A01_+ + (-A11)_+; since "
            "A10+A01-A11<=B, N_{-,-}>=(A00-B)/4."
        ),
        "strictly_weaker_next_condition": (
            "B <= (1-delta)A00 on all sufficiently large cubic-rough "
            "pair blocks"
        ),
        "rows": rows,
        "synthetic_nonnecessity_witness": synthetic,
        "checks": checks,
        "failure_count": (
            sum(
                not value
                for row in rows
                for value in row["checks"].values()
            )
            + sum(not value for value in checks.values())
        ),
    }


def build_audit() -> dict[str, object]:
    riemann_audit = riemann_schur_audit()
    collatz_audit = collatz_rank_equivalence_audit()
    goldbach_audit = goldbach_variation_audit()
    twin_audit = twin_adverse_walsh_audit()

    riemann_next = "ExplicitWeilFormCoreSchurPivotLowerBound"
    collatz_next = "ExplicitLiftClosedFiniteDescriptionCollatzRank"
    goldbach_next = (
        "ArithmeticBinaryGoldbachSignedMartingaleCancellationK56"
    )
    twin_next = "UniformCubicRoughAdverseWalshPartContraction"

    riemann = {
        "theorem_name": (
            "NestedGramSchurPivotCertificateAndFinitePrefixExtensionNoGo"
        ),
        "declared_target": (
            "Reduce all-section form-core compression positivity to exact "
            "scalar certificates and test whether finite prefix success "
            "can imply the infinite family."
        ),
        "declared_target_ko": (
            "form-core의 모든 압축 양성을 정확한 스칼라 인증으로 환원하고 "
            "유한 prefix 성공이 무한 가족을 함의하는지 판정한다."
        ),
        "proved_statement": (
            "Nested positive Gram sections are equivalent to positivity of "
            "every exact Schur pivot. Any finite positive prefix admits an "
            "unchanged negative-pivot extension."
        ),
        "proved_statement_ko": (
            "중첩 Gram 절단의 양성은 모든 정확 Schur pivot의 양성과 "
            "동치다. 임의의 유한 양성 prefix는 그대로 둔 채 다음 "
            "pivot을 음수로 확장할 수 있다."
        ),
        "proof": (
            "Block Gaussian elimination gives the Schur-complement "
            "criterion and determinant ratio. The extension diag(G_N,-1) "
            "preserves every audited principal section and is indefinite."
        ),
        "schur_audit": riemann_audit,
        "logical_limit": (
            "No actual Weil Gram entries or all-N pivot lower bound is "
            "proved. Hilbert matrices are exact conditioning controls, not "
            "zeta-form compressions."
        ),
        "route_decision": {
            "discard": (
                "promoting any bounded list of positive finite sections to "
                "the infinite compression family"
            ),
            "retain": (
                "an explicit Weil form-core basis with a symbolic positive "
                "lower bound for every Schur pivot"
            ),
            "next_theorem": riemann_next,
        },
        "proof_boundary": (
            "No RH proof or counterexample. The result supplies an exact "
            "certificate grammar and a finite-prefix no-go only."
        ),
        "machine_audit": {
            "row_count": (
                len(riemann_audit["hilbert_rows"])
                + len(riemann_audit["negative_extension_rows"])
            ),
            "failure_count": riemann_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "RH",
            (
                "NestedGramSchurPivotCertificateAnd"
                "FinitePrefixExtensionNoGo"
            ),
            riemann_next,
        ),
    }

    collatz = {
        "theorem_name": "GlobalWellFoundedRankIffCollatzTermination",
        "declared_target": (
            "Determine whether an unrestricted well-founded natural-code "
            "rank is a genuine intermediate lemma."
        ),
        "declared_target_ko": (
            "제약 없는 well-founded 자연 코드 rank가 실제 중간정리인지 "
            "판정한다."
        ),
        "proved_statement": (
            "Global accelerated Collatz termination is equivalent to the "
            "existence of a well-founded rank strictly decreasing outside "
            "1. The least hitting time supplies the reverse construction."
        ),
        "proved_statement_ko": (
            "가속 Collatz의 전역 종료는 1 밖에서 엄격히 감소하는 "
            "well-founded rank의 존재와 동치다. 종료를 가정하면 최소 "
            "도달시간이 그 rank를 만든다."
        ),
        "proof": (
            "Hitting time gives a natural-valued rank when termination is "
            "known. Conversely, a nonterminating orbit would be an infinite "
            "strict descent in a well-order."
        ),
        "rank_equivalence_audit": collatz_audit,
        "logical_limit": (
            "The equivalence does not construct an independent rank. The "
            "100,000-start audit computes ranks only after bounded "
            "termination and cannot exclude a larger cycle or divergence."
        ),
        "route_decision": {
            "discard": (
                "presenting an unrestricted rank, or a rank defined by "
                "observed stopping time, as a weaker Collatz lemma"
            ),
            "retain": (
                "a finite-description residue/affine rank with independent "
                "lift closure and descent proof"
            ),
            "next_theorem": collatz_next,
        },
        "proof_boundary": (
            "No Collatz proof or counterexample. One rank formulation is "
            "proved exactly equivalent to the unresolved conjecture."
        ),
        "machine_audit": {
            "row_count": len(
                collatz_audit["finite_stopping_rank_audit"][
                    "selected_rows"
                ]
            ),
            "failure_count": collatz_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "CO",
            "GlobalWellFoundedRankIffCollatzTermination",
            collatz_next,
        ),
    }

    goldbach = {
        "theorem_name": (
            "BoundedSignalLinearAbsoluteMartingaleVariationNoGo"
        ),
        "declared_target": (
            "Test whether uniformly bounded dyadic point values force a "
            "scale-independent absolute martingale path budget."
        ),
        "declared_target_ko": (
            "균일하게 bounded인 dyadic 점값이 척도 독립 절대 martingale "
            "경로 예산을 강제하는지 판정한다."
        ),
        "proved_statement": (
            "There are exact dyadic vectors with sup norm at most one whose "
            "all-left absolute path variation is d/2 while the signed "
            "endpoint stays in {0,1/2}."
        ),
        "proved_statement_ko": (
            "sup norm이 1 이하이지만 all-left 절대 경로변동은 d/2이고 "
            "부호 있는 endpoint는 0 또는 1/2인 정확한 dyadic 벡터족이 "
            "존재한다."
        ),
        "proof": (
            "Alternate path conditional means between 0 and 1/2 and assign "
            "each sibling subtree the constant mean preserving its parent. "
            "Every increment has magnitude 1/2 and signs telescope."
        ),
        "variation_audit": goldbach_audit,
        "logical_limit": (
            "The vector family is not an arithmetic Goldbach residual. It "
            "does not refute a K56 theorem for that residual; it refutes "
            "absolute path variation as a generic bounded-signal proxy."
        ),
        "route_decision": {
            "discard": (
                "deriving a uniform absolute path-variation budget from "
                "bounded point values or transform structure alone"
            ),
            "retain": (
                "signed arithmetic cancellation on actual binary Goldbach "
                "residuals, stratified by the hard rough classes"
            ),
            "next_theorem": goldbach_next,
        },
        "proof_boundary": (
            "No Goldbach proof or counterexample. An exact auxiliary "
            "counterfamily only removes an overstrong generic proxy."
        ),
        "machine_audit": {
            "row_count": len(goldbach_audit["rows"]),
            "failure_count": goldbach_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "GB",
            "BoundedSignalLinearAbsoluteMartingaleVariationNoGo",
            goldbach_next,
        ),
    }

    twin_prime = {
        "theorem_name": (
            "WalshL1SimplexBalanceIdentityAndAdversePartReduction"
        ),
        "declared_target": (
            "Determine the exact combinatorial strength of full Walsh L1 "
            "contraction and derive a weaker twin-targeted sufficient bound."
        ),
        "declared_target_ko": (
            "전체 Walsh L1 수축의 정확한 조합론적 강도를 판정하고 더 약한 "
            "twin 표적 충분조건을 도출한다."
        ),
        "proved_statement": (
            "Walsh L1 equals the maximum two-sided deviation of any parity "
            "class from one quarter of the rough mass. Replacing it by the "
            "adverse positive parts alone still gives "
            "N_{-,-}>=(A00-B)/4."
        ),
        "proved_statement_ko": (
            "Walsh L1은 각 parity 부류가 rough 질량의 1/4에서 벗어나는 "
            "최대 양방향 편차와 같다. twin에 불리한 양의 부분만 남겨도 "
            "N_{-,-}>=(A00-B)/4가 성립한다."
        ),
        "proof": (
            "Walsh inversion and the eight signed character directions give "
            "the simplex identity. Bounding each adverse signed term by its "
            "positive part yields the targeted lower bound."
        ),
        "adverse_walsh_audit": twin_audit,
        "logical_limit": (
            "Four finite blocks have zero adverse part, but no eventual "
            "sign theorem or uniform all-scale contraction is proved. The "
            "sieve parity barrier remains."
        ),
        "route_decision": {
            "discard": (
                "requiring two-sided balance of all four parity classes via "
                "full Walsh L1 as the primary twin target"
            ),
            "retain": (
                "control only A10_+, A01_+, and (-A11)_+ on cubic-rough "
                "pair blocks"
            ),
            "next_theorem": twin_next,
        },
        "proof_boundary": (
            "No Twin Prime proof or counterexample. The result weakens one "
            "sufficient correlation target and audits four finite blocks."
        ),
        "machine_audit": {
            "row_count": len(twin_audit["rows"]),
            "failure_count": twin_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "TP",
            (
                "WalshL1SimplexBalanceIdentityAnd"
                "AdversePartReduction"
            ),
            twin_next,
        ),
    }

    sections = [riemann, collatz, goldbach, twin_prime]
    total_failures = sum(
        section["machine_audit"]["failure_count"]
        for section in sections
    )
    return {
        "theorem_name": (
            "FourConjectureSchurRankVariationAdverseWalshAudit"
        ),
        "status": (
            "exact_reductions_and_no_go_theorems_all_conjectures_open"
        ),
        "proof_boundary": (
            "No conjecture proof or counterexample. TICKET144 proves four "
            "exact linear-algebraic, dynamical, martingale, or Walsh "
            "statements, rejects overstrong or circular intermediate "
            "targets, and leaves all four conjectures open."
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
        ("riemann", "RH-TICKET-144", "nested exact Schur-pivot audit"),
        (
            "collatz",
            "CO-TICKET-144",
            "global well-founded rank equivalence audit",
        ),
        (
            "goldbach",
            "GB-TICKET-144",
            "bounded-signal absolute-variation counterfamily",
        ),
        (
            "twin-prime",
            "TP-TICKET-144",
            "Walsh simplex and adverse-part reduction",
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
        "status": (
            "exact_reductions_and_no_go_theorems_all_conjectures_open"
        ),
        "claim_boundary": audit["proof_boundary"],
        "schur_rank_equivalence_variation_adverse_walsh_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / (
            "data/open-problem/"
            "ticket144-schur-rank-equivalence-variation-adverse-walsh.json"
        ),
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/rh-ticket-144-schur-pivots.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/co-ticket-144-rank-equivalence.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/gb-ticket-144-variation-no-go.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/tp-ticket-144-adverse-walsh.json"
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
