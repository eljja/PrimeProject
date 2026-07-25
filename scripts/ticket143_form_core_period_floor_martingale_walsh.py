from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from typing import Sequence

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket142_effective_rank_cycle_direction_haar_liouville import (
    twin_liouville_ledger,
)


GENERATED_AT = "2026-07-25T23:35:00+09:00"
SCHEMA = "primeproject.ticket143-form-core-period-floor-martingale-walsh.v1"


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
    closed_id = f"{problem_code}-T143-CLOSED"
    open_id = f"{problem_code}-T143-OPEN"
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


def riemann_form_core_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for dimension in [1, 2, 4, 8, 16, 32, 64, 128]:
        reciprocal_energy = sum(
            (
                Fraction(1, 2 * index * index)
                for index in range(1, dimension + 1)
            ),
            Fraction(),
        )
        schur_margin = 1 - reciprocal_energy
        checks = {
            "finite_graph_gram_is_strictly_positive": schur_margin > 0,
            "margin_identity": (
                schur_margin + reciprocal_energy == 1
            ),
            "margin_below_one": schur_margin < 1,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "dimension": dimension,
                "reciprocal_energy_sum": fraction_payload(
                    reciprocal_energy
                ),
                "rank_one_schur_margin": fraction_payload(schur_margin),
                "checks": checks,
            }
        )
    return {
        "closed_form": (
            "q(a,y)=2*sum_{n>=1} n^2*|y_n|^2-|a|^2 on "
            "C direct_sum l2"
        ),
        "finite_graph_subspace": (
            "V_N=span{f_n=(1,e_n):1<=n<=N}; "
            "Gram(V_N)=diag(2n^2)-11^T"
        ),
        "strict_positivity_certificate": (
            "sum_{n=1}^N 1/(2n^2)<1; for n>=2 use "
            "1/n^2<1/(n(n-1)), so the infinite sum is also below one"
        ),
        "hilbert_density_certificate": (
            "an orthogonal vector (alpha,z) satisfies "
            "z_n=-alpha for every n; l2 membership forces alpha=0 and z=0"
        ),
        "negative_witness": {
            "vector": "(1,0)",
            "form_value": -1,
        },
        "rows": rows,
        "failure_count": failures,
    }


def collatz_affine_numerator(word: Sequence[int]) -> int:
    if not word or any(value < 1 for value in word):
        raise ValueError("a nonempty positive valuation word is required")
    length = len(word)
    prefix_sum = 0
    numerator = 0
    for index, valuation in enumerate(word):
        numerator += 3 ** (length - 1 - index) * (1 << prefix_sum)
        prefix_sum += valuation
    return numerator


def collatz_period_floor_audit() -> dict[str, object]:
    period = 15_601
    valuation_sum = 24_727
    published_odd_period_floor = 72_000_000_000
    raw_word_count = math.comb(valuation_sum - 2, period - 2)
    sys.set_int_max_str_digits(max(sys.get_int_max_str_digits(), 20_000))
    raw_word_count_text = str(raw_word_count)
    order_rows = []
    for word in [(1, 1, 4), (1, 2, 3), (1, 3, 2), (1, 4, 1)]:
        numerator = collatz_affine_numerator(word)
        denominator = (1 << sum(word)) - 3 ** len(word)
        order_rows.append(
            {
                "word": list(word),
                "length": len(word),
                "valuation_sum": sum(word),
                "affine_numerator": numerator,
                "cycle_denominator": denominator,
                "numerator_mod_denominator": numerator % denominator,
            }
        )
    checks = {
        "ticket142_period_below_published_floor": (
            period < published_odd_period_floor
        ),
        "raw_composition_count_has_expected_digits": (
            len(raw_word_count_text) == 7_069
        ),
        "same_length_and_sum_can_change_numerator": (
            len({row["affine_numerator"] for row in order_rows}) > 1
        ),
        "small_order_rows_share_length_and_sum": (
            len({(row["length"], row["valuation_sum"]) for row in order_rows})
            == 1
        ),
    }
    return {
        "external_published_premise": {
            "statement": (
                "Every nontrivial Collatz cycle has more than "
                "7.2e10 odd members."
            ),
            "source": "https://arxiv.org/abs/2201.00406",
            "source_role": (
                "published theorem imported as a premise; not re-proved by "
                "PrimeProject"
            ),
        },
        "retired_ticket142_branch": {
            "odd_period": period,
            "valuation_sum": valuation_sum,
            "published_odd_period_floor": published_odd_period_floor,
            "closed_under_published_premise": (
                period < published_odd_period_floor
            ),
        },
        "raw_valuation_word_space": {
            "constraints": (
                "a_0=1, a_i>=1, length=15601, sum=24727"
            ),
            "exact_count_formula": "binom(24725,15599)",
            "exact_count": raw_word_count_text,
            "decimal_digits": len(raw_word_count_text),
            "log2_count": math.log2(raw_word_count),
            "interpretation": (
                "raw positive compositions only; not a count of cycles or "
                "minimum-compatible words"
            ),
        },
        "order_sensitivity_rows": order_rows,
        "checks": checks,
        "failure_count": sum(not value for value in checks.values()),
    }


def mean(values: Sequence[Fraction]) -> Fraction:
    return sum(values, Fraction()) / len(values)


def dyadic_point_ledger(
    values: Sequence[Fraction],
    point: int,
) -> dict[str, object]:
    size = len(values)
    if size < 1 or size & (size - 1):
        raise ValueError("dyadic vector length is required")
    if not 0 <= point < size:
        raise IndexError(point)
    root_mean = mean(values)
    reconstruction = root_mean
    path_variation = abs(root_mean)
    start = 0
    width = size
    path = []
    while width > 1:
        half = width // 2
        midpoint = start + half
        left_mean = mean(values[start:midpoint])
        right_mean = mean(values[midpoint : start + width])
        difference = (left_mean - right_mean) / 2
        sign = 1 if point < midpoint else -1
        reconstruction += sign * difference
        path_variation += abs(difference)
        path.append(
            {
                "interval_start": start,
                "interval_size": width,
                "martingale_difference": fraction_payload(difference),
                "point_sign": sign,
            }
        )
        if point >= midpoint:
            start = midpoint
        width = half
    return {
        "point": point,
        "root_mean": fraction_payload(root_mean),
        "reconstruction": fraction_payload(reconstruction),
        "target": fraction_payload(values[point]),
        "path_variation_envelope": fraction_payload(path_variation),
        "path": path,
        "checks": {
            "exact_reconstruction": reconstruction == values[point],
            "point_below_path_envelope": (
                abs(values[point]) <= path_variation
            ),
        },
    }


def goldbach_martingale_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for depth in range(2, 7):
        size = 1 << depth
        values = [
            Fraction(((index * index + 3 * index + 1) % 17) - 8)
            for index in range(size)
        ]
        point_rows = [
            dyadic_point_ledger(values, point)
            for point in range(size)
        ]
        checks = {
            "all_points_reconstruct_exactly": all(
                row["checks"]["exact_reconstruction"]
                for row in point_rows
            ),
            "all_points_obey_path_envelope": all(
                row["checks"]["point_below_path_envelope"]
                for row in point_rows
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "depth": depth,
                "size": size,
                "root_mean": fraction_payload(mean(values)),
                "maximum_absolute_point": int(
                    max(abs(value) for value in values)
                ),
                "maximum_path_variation_envelope": fraction_payload(
                    max(
                        Fraction(
                            row["path_variation_envelope"]["exact"]
                        )
                        for row in point_rows
                    )
                ),
                "checks": checks,
            }
        )
    root_mode_rows = []
    for depth in [4, 6, 8, 9, 10, 12]:
        size = 1 << depth
        root_mode_rows.append(
            {
                "depth": depth,
                "size": size,
                "constant_point_value": 1,
                "pointwise_below_K56": True,
                "orthonormal_root_coefficient_squared": size,
                "root_coefficient_exceeds_23": size > 23**2,
                "all_wavelet_coefficients_zero": True,
            }
        )
    exact_checks = {
        "first_dyadic_constant_root_failure_is_depth_10": (
            min(
                row["depth"]
                for row in root_mode_rows
                if row["root_coefficient_exceeds_23"]
            )
            == 10
        ),
        "constant_vector_remains_pointwise_below_56": all(
            row["pointwise_below_K56"] for row in root_mode_rows
        ),
    }
    failures += sum(not value for value in exact_checks.values())
    return {
        "pointwise_identity": (
            "rho_j=mean(rho)+sum_{dyadic I containing j} "
            "sign(I,j)*(mean(left I)-mean(right I))/2"
        ),
        "orthonormal_conversion": (
            "c_root=sqrt(n)*mean(rho), "
            "c_I=sqrt(|I|)*(mean(left I)-mean(right I))/2"
        ),
        "rows": rows,
        "root_mode_no_go_rows": root_mode_rows,
        "exact_checks": exact_checks,
        "failure_count": failures,
    }


def twin_walsh_row(scale: int) -> dict[str, object]:
    source = twin_liouville_ledger(scale)
    a00 = int(source["A00"])
    a10 = int(source["A10"])
    a01 = int(source["A01"])
    a11 = int(source["A11"])
    category_counts = {
        "lambda_plus_plus": (a00 + a10 + a01 + a11) // 4,
        "lambda_plus_minus": (a00 + a10 - a01 - a11) // 4,
        "lambda_minus_plus": (a00 - a10 + a01 - a11) // 4,
        "lambda_minus_minus_twins": (a00 - a10 - a01 + a11) // 4,
    }
    one_sided_gap = a00 - a10 - a01 + a11
    walsh_l1 = abs(a10) + abs(a01) + abs(a11)
    l1_margin = a00 - walsh_l1
    checks = {
        "category_counts_sum_to_rough_mass": (
            sum(category_counts.values()) == a00
        ),
        "minus_minus_is_direct_twin_count": (
            category_counts["lambda_minus_minus_twins"]
            == source["direct_twin_count"]
        ),
        "one_sided_gap_is_exactly_four_twins": (
            one_sided_gap == 4 * source["direct_twin_count"]
        ),
        "finite_row_walsh_l1_contraction": l1_margin > 0,
        "all_four_categories_positive": all(
            value > 0 for value in category_counts.values()
        ),
    }
    return {
        **source,
        "category_counts": category_counts,
        "one_sided_gap": one_sided_gap,
        "walsh_l1": walsh_l1,
        "walsh_l1_margin": l1_margin,
        "walsh_l1_contraction_delta": fraction_payload(
            Fraction(l1_margin, a00)
        ),
        "checks": checks,
    }


def twin_walsh_audit() -> dict[str, object]:
    rows = [
        twin_walsh_row(scale)
        for scale in [1_000, 10_000, 100_000, 1_000_000]
    ]
    failures = sum(
        not value
        for row in rows
        for value in row["checks"].values()
    )
    return {
        "walsh_inversion": (
            "N_{s,t}=(A00+s*A10+t*A01+s*t*A11)/4 "
            "for s,t in {+1,-1}"
        ),
        "circularity_identity": (
            "A00-A10-A01+A11=4*N_{-,-}=4*pi_2[X,2X]"
        ),
        "strictly_stronger_sufficient_condition": (
            "|A10|+|A01|+|A11| <= (1-delta)*A00 for fixed delta>0"
        ),
        "rows": rows,
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann_audit = riemann_form_core_audit()
    collatz_audit = collatz_period_floor_audit()
    goldbach_audit = goldbach_martingale_audit()
    twin_audit = twin_walsh_audit()

    riemann_next = "ExplicitWeilFormCoreCompressionCertificateFamily"
    collatz_next = (
        "PublishedFloorAwareAffineCappedNaturalCodeWellFoundedness"
    )
    goldbach_next = (
        "UniformBinaryGoldbachRootMeanPlusDyadicPathVariationBelow56"
    )
    twin_next = "UniformCubicRoughWalshL1ContractionBelowOne"

    riemann = {
        "theorem_name": (
            "ClosedFormCoreFiniteSectionBridgeAndHilbertDenseNoGo"
        ),
        "declared_target": (
            "Determine the exact topology needed to promote nonnegative "
            "finite compressions of a closed semibounded form."
        ),
        "declared_target_ko": (
            "닫힌 아래유계 형식의 유한 압축 양성을 전체 양성으로 올리는 "
            "데 필요한 정확한 위상을 판정한다."
        ),
        "proved_statement": (
            "Nonnegativity on nested finite subspaces promotes to the full "
            "closed form when their union is a form core. Hilbert-space "
            "density alone is insufficient."
        ),
        "proved_statement_ko": (
            "중첩 유한부분공간의 합집합이 form core이면 양성이 전체 닫힌 "
            "형식으로 승격된다. Hilbert 공간 조밀성만으로는 부족하다."
        ),
        "proof": (
            "Form-norm approximation and continuity prove the positive "
            "bridge. The explicit graph subspaces have positive rank-one "
            "Schur margins and Hilbert-dense union, while q(1,0)=-1."
        ),
        "form_core_audit": riemann_audit,
        "logical_limit": (
            "PrimeProject still has no explicit Weil form, form-core basis, "
            "interval-certified Gram entries, or all-section positivity "
            "theorem. The counterexample is functional-analytic, not an RH "
            "counterexample."
        ),
        "route_decision": {
            "discard": (
                "Hilbert-dense finite-section positivity without a form-core "
                "contract"
            ),
            "retain": (
                "closed-form compression on an explicit Weil form core with "
                "certified entries for every section"
            ),
            "next_theorem": riemann_next,
        },
        "proof_boundary": (
            "No conjecture proof or RH counterexample. The exact abstract "
            "promotion theorem and topology no-go only repair the proof route."
        ),
        "machine_audit": {
            "row_count": len(riemann_audit["rows"]),
            "failure_count": riemann_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "RH",
            "ClosedFormCoreFiniteSectionBridgeAndHilbertDenseNoGo",
            riemann_next,
        ),
    }

    collatz = {
        "theorem_name": (
            "PublishedOddPeriodFloorRetiresPeriod15601And"
            "CompositionExplosionNoGo"
        ),
        "declared_target": (
            "Audit whether period 15,601 is still a live academic branch and "
            "quantify the exact raw valuation-word search space."
        ),
        "declared_target_ko": (
            "15,601주기 분기가 현재 학술적으로 유효한지 감사하고 원시 "
            "valuation-word 탐색공간을 정확히 계량한다."
        ),
        "proved_statement": (
            "Under the published odd-period floor K>7.2e10, period 15,601 "
            "cannot be a nontrivial cycle. Its raw a0=1 composition space "
            "has 7,069 decimal digits and the affine numerator depends on "
            "word order."
        ),
        "proved_statement_ko": (
            "공개된 홀수 주기 하한 K>7.2×10^10을 전제로 하면 15,601주기는 "
            "비자명 순환일 수 없다. a0=1 원시 조합 수는 7,069자리이고 "
            "affine numerator는 valuation 순서에 의존한다."
        ),
        "proof": (
            "The period comparison imports the cited published theorem. "
            "Stars-and-bars gives binom(24725,15599); direct affine expansion "
            "shows equal length and sum do not determine the numerator."
        ),
        "period_floor_audit": collatz_audit,
        "logical_limit": (
            "The published premise concerns nontrivial cycles, not divergent "
            "aperiodic orbits. PrimeProject does not re-prove the 7.2e10 "
            "floor, and raw composition size is not a complexity lower bound "
            "against every symbolic algorithm."
        ),
        "route_decision": {
            "discard": (
                "enumerating period-15601 affine numerators as the current "
                "decisive Collatz branch"
            ),
            "retain": (
                "unbounded-depth natural-code descent together with cycle "
                "handling beyond the published odd-period floor"
            ),
            "next_theorem": collatz_next,
        },
        "proof_boundary": (
            "No Collatz proof or counterexample. One obsolete finite-cycle "
            "branch is retired under a published external theorem; aperiodic "
            "divergence and longer cycles remain open."
        ),
        "machine_audit": {
            "row_count": len(
                collatz_audit["order_sensitivity_rows"]
            ),
            "failure_count": collatz_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "CO",
            (
                "PublishedOddPeriodFloorRetiresPeriod15601And"
                "CompositionExplosionNoGo"
            ),
            collatz_next,
        ),
    }

    goldbach = {
        "theorem_name": (
            "DyadicMartingaleResidualIdentityAndRootModeScalingNoGo"
        ),
        "declared_target": (
            "Replace ambiguous orthonormal Haar caps by a scale-normalized "
            "pointwise residual ledger."
        ),
        "declared_target_ko": (
            "모호한 정규직교 Haar 계수 상한을 척도 정규화된 점별 잔차 "
            "ledger로 교체한다."
        ),
        "proved_statement": (
            "Every dyadic residual is reconstructed exactly from its root "
            "mean and signed martingale differences. A constant pointwise "
            "signal has zero wavelets but root coefficient sqrt(n), so a "
            "uniform orthonormal coefficient cap is unnecessarily strong."
        ),
        "proved_statement_ko": (
            "모든 dyadic 잔차는 root 평균과 부호 있는 martingale 차이로 "
            "정확히 복원된다. 상수 점별 신호는 wavelet이 모두 0이지만 "
            "root 계수는 √n이므로 균일 정규직교 계수 상한은 과도하다."
        ),
        "proof": (
            "Conditional means telescope along the unique dyadic path to a "
            "point. Haar normalization multiplies each martingale difference "
            "by sqrt(interval size); the constant-vector no-go follows."
        ),
        "martingale_audit": goldbach_audit,
        "logical_limit": (
            "The exact transform is not an arithmetic estimate for the "
            "actual binary Goldbach residual. Neither its root mean nor every "
            "dyadic path variation is bounded below K=56 here."
        ),
        "route_decision": {
            "discard": (
                "a scale-independent cap on every orthonormal Haar "
                "coefficient as the primary arithmetic target"
            ),
            "retain": (
                "separate arithmetic control of the normalized residual root "
                "mean and the total dyadic path variation"
            ),
            "next_theorem": goldbach_next,
        },
        "proof_boundary": (
            "No Goldbach proof or counterexample. The martingale identity and "
            "root-mode countermodel correct the target normalization only."
        ),
        "machine_audit": {
            "row_count": len(goldbach_audit["rows"]),
            "failure_count": goldbach_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "GB",
            "DyadicMartingaleResidualIdentityAndRootModeScalingNoGo",
            goldbach_next,
        ),
    }

    twin_prime = {
        "theorem_name": (
            "WalshHadamardRoughPairInversionAndCircularGapNoGo"
        ),
        "declared_target": (
            "Determine whether the one-sided cubic-rough Liouville ledger gap "
            "is a genuine intermediate theorem or a restatement."
        ),
        "declared_target_ko": (
            "세제곱 rough Liouville 단측 ledger gap이 실제 중간정리인지 "
            "원문제의 재진술인지 판정한다."
        ),
        "proved_statement": (
            "Walsh-Hadamard inversion recovers all four Liouville parity "
            "classes. The proposed one-sided gap equals four times the twin "
            "count, so its strict positivity is exactly blockwise twin "
            "existence. An absolute Walsh L1 contraction is a stronger, "
            "non-circular sufficient target."
        ),
        "proved_statement_ko": (
            "Walsh-Hadamard 역변환은 네 Liouville parity 부류를 모두 "
            "복원한다. 기존 단측 gap은 쌍둥이 수의 정확히 4배이므로 그 "
            "양성은 블록별 쌍둥이 존재와 동치다. 절대 Walsh L1 수축은 "
            "더 강하지만 순환적이지 않은 충분조건이다."
        ),
        "proof": (
            "Fourier inversion on {+1,-1}^2 gives the category formulas. "
            "Substituting (-1,-1) yields the exact twin projector. Triangle "
            "inequality gives every category at least "
            "(A00-|A10|-|A01|-|A11|)/4."
        ),
        "walsh_audit": twin_audit,
        "logical_limit": (
            "Finite positive L1 margins through X=1e6 do not prove a uniform "
            "all-scale contraction. Establishing it for the actual Liouville "
            "correlations still crosses the sieve parity barrier."
        ),
        "route_decision": {
            "discard": (
                "OneSidedCubicRoughLiouvilleLedgerGap as a distinct bridge; "
                "it is algebraically equivalent to positive twin mass"
            ),
            "retain": (
                "a uniform absolute Walsh-correlation contraction on the "
                "cubic-rough pair support"
            ),
            "next_theorem": twin_next,
        },
        "proof_boundary": (
            "No Twin Prime proof or counterexample. The circular target is "
            "retired and replaced by a stronger sufficient correlation "
            "inequality that remains unproved."
        ),
        "machine_audit": {
            "row_count": len(twin_audit["rows"]),
            "failure_count": twin_audit["failure_count"],
            "conjecture_resolution_count": 0,
        },
        "proof_dag": proof_dag(
            "TP",
            "WalshHadamardRoughPairInversionAndCircularGapNoGo",
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
            "FourConjectureFormCorePeriodFloorMartingaleWalshAudit"
        ),
        "status": (
            "exact_route_corrections_proved_all_conjectures_open"
        ),
        "proof_boundary": (
            "No conjecture proof or counterexample. This audit proves four "
            "exact promotion, counting, transform, or inversion results and "
            "uses one clearly labelled published Collatz premise. It does not "
            "prove or refute RH, Collatz, strong Goldbach, or Twin Prime."
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
        ("riemann", "RH-TICKET-143", "closed-form core promotion audit"),
        (
            "collatz",
            "CO-TICKET-143",
            "published odd-period floor and composition-space audit",
        ),
        (
            "goldbach",
            "GB-TICKET-143",
            "dyadic martingale residual normalization audit",
        ),
        (
            "twin-prime",
            "TP-TICKET-143",
            "cubic-rough Walsh inversion and circularity audit",
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
        "status": "exact_route_corrections_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "form_core_period_floor_martingale_walsh_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket143-form-core-period-floor-martingale-walsh.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/rh-ticket-143-form-core.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/co-ticket-143-period-floor.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/gb-ticket-143-martingale.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/tp-ticket-143-walsh.json"
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
