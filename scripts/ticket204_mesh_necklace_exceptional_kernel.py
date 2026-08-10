from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any

from ticket200_derivative_mesh_three_run_chen_channels import (
    ordered_affine_numerator,
    prime_sieve,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket204-mesh-necklace-exceptional-kernel.v1"
GENERATED_AT = "2026-08-10T23:59:30+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def riemann_mesh_certificate_audit() -> dict[str, Any]:
    sample_count = 16
    sample_bound = Fraction(1, 10)
    derivative_bound = Fraction(1, 5)
    covering_radius_upper = Fraction(11, 56)  # pi/16 <= (22/7)/16
    certified_supremum = sample_bound + derivative_bound * covering_radius_upper
    certified_margin = 1 - certified_supremum

    no_go_sample_count = 8
    sample_only_ratio = 0
    missed_midpoint_ratio = 2
    failures = 0
    failures += int(certified_supremum != Fraction(39, 280))
    failures += int(certified_margin != Fraction(241, 280))
    failures += int(certified_supremum >= 1)
    failures += int(sample_only_ratio != 0)
    failures += int(missed_midpoint_ratio <= 1)

    theorem = (
        "Let Gamma be parameterized by arclength and let r=(X-P)/P, with P "
        "nonzero on Gamma. If a finite sample set has covering radius delta, "
        "|r|<=q at every sample, and |dr/ds|<=M everywhere on Gamma, then "
        "sup_Gamma |r|<=q+M delta. Hence q+M delta<1 certifies the strict "
        "Rouche inequality. No finite sample set alone can certify this: on "
        "the unit circle, P=1 and X=z^m agree at all m-th roots of unity, "
        "while |X-P|=2 at every intervening half-step."
    )
    proof = (
        "Choose a nearest sample s_j for any boundary point s. The fundamental "
        "theorem of calculus and the derivative bound give "
        "|r(s)|<=|r(s_j)|+integral |r'|<=q+M delta. Rouche follows when this "
        "quantity is below one. For the no-go family r(z)=z^m-1: r vanishes "
        "at every sampled m-th root, but at z=exp(pi i/m) one has z^m=-1 and "
        "|r|=2. Thus regularity information is logically indispensable."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_certified_regression": {
            "contour": "unit circle",
            "comparison_P": "1",
            "analytic_X": "1+z^2/10",
            "relative_error_r": "z^2/10",
            "sample_count": sample_count,
            "sample_ratio_bound_q": fraction_text(sample_bound),
            "arclength_derivative_bound_M": fraction_text(derivative_bound),
            "covering_radius_delta_upper_using_pi_le_22_over_7": fraction_text(
                covering_radius_upper
            ),
            "certified_contour_supremum_upper": fraction_text(certified_supremum),
            "strict_rouche_margin_lower": fraction_text(certified_margin),
            "rouche_hypothesis_certified": certified_supremum < 1,
        },
        "finite_sampling_no_go": {
            "contour": "unit circle",
            "sample_count": no_go_sample_count,
            "sample_nodes": "8th roots of unity",
            "comparison_P": "1",
            "analytic_X": "z^8",
            "relative_error_r": "z^8-1",
            "maximum_sample_ratio": sample_only_ratio,
            "missed_midpoint": "exp(pi i/8)",
            "missed_midpoint_ratio": missed_midpoint_ratio,
            "comparison_zero_count_inside": 0,
            "analytic_zero_count_inside": 8,
            "sample_only_certificate_refuted": True,
        },
        "aggregate": {
            "derivative_certified_mesh_theorem_proved": True,
            "finite_sampling_without_regularizer_refuted": True,
            "actual_xi_relative_derivative_bound_constructed": False,
            "actual_cofinal_xi_certificate_constructed": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The theorem closes the finite-mesh-to-continuous-boundary transfer, "
            "not the Xi-specific derivative estimate. The polynomial examples "
            "are exact regression fixtures and are not the completed zeta function."
        ),
        "failure_count": failures,
    }


def rotations(word: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [word[index:] + word[:index] for index in range(len(word))]


def canonical_rotation(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(rotations(word))


def primitive_root(word: tuple[int, ...]) -> tuple[int, ...]:
    length = len(word)
    for root_length in range(1, length + 1):
        if length % root_length:
            continue
        root = word[:root_length]
        if root * (length // root_length) == word:
            return root
    raise AssertionError("every finite word has itself as a primitive root")


def collatz_denominator(word: tuple[int, ...]) -> int:
    return 2 ** sum(word) - 3 ** len(word)


def rotation_identity_row(word: tuple[int, ...]) -> dict[str, Any]:
    rotated = word[1:] + word[:1]
    denominator = collatz_denominator(word)
    numerator = ordered_affine_numerator(word)
    rotated_numerator = ordered_affine_numerator(rotated)
    left = 2 ** word[0] * rotated_numerator
    right = 3 * numerator + denominator
    source_divisible = denominator != 0 and numerator % denominator == 0
    target_divisible = denominator != 0 and rotated_numerator % denominator == 0
    return {
        "word": list(word),
        "rotated_word": list(rotated),
        "denominator_D": denominator,
        "numerator_B": numerator,
        "rotated_numerator_B": rotated_numerator,
        "identity_2a0_Brot_equals_3B_plus_D": left == right,
        "divisibility_invariant": source_divisible == target_divisible,
    }


def repetition_identity_row(
    root: tuple[int, ...], repetition_count: int
) -> dict[str, Any]:
    repeated = root * repetition_count
    root_length = len(root)
    root_sum = sum(root)
    geometric_factor = sum(
        3 ** (root_length * (repetition_count - 1 - index))
        * 2 ** (root_sum * index)
        for index in range(repetition_count)
    )
    root_numerator = ordered_affine_numerator(root)
    repeated_numerator = ordered_affine_numerator(repeated)
    root_denominator = collatz_denominator(root)
    repeated_denominator = collatz_denominator(repeated)
    return {
        "primitive_root": list(root),
        "repetition_count": repetition_count,
        "repeated_length": len(repeated),
        "geometric_factor_G": geometric_factor,
        "root_numerator_B": root_numerator,
        "repeated_numerator_B": repeated_numerator,
        "root_denominator_D": root_denominator,
        "repeated_denominator_D": repeated_denominator,
        "numerator_factorization_holds": (
            repeated_numerator == root_numerator * geometric_factor
        ),
        "denominator_factorization_holds": (
            repeated_denominator == root_denominator * geometric_factor
        ),
        "rational_cycle_value_preserved": (
            repeated_numerator * root_denominator
            == root_numerator * repeated_denominator
        ),
        "divisibility_equivalent": (
            (root_numerator % root_denominator == 0)
            == (repeated_numerator % repeated_denominator == 0)
        )
        if root_denominator and repeated_denominator
        else False,
    }


def collatz_necklace_summary(horizon: int) -> dict[str, Any]:
    alphabet = range(1, 5)
    positive_words = 0
    necklaces: set[tuple[int, ...]] = set()
    primitive_necklaces: set[tuple[int, ...]] = set()
    divisible_words = 0
    divisible_necklaces: set[tuple[int, ...]] = set()
    divisible_primitive_necklaces: set[tuple[int, ...]] = set()
    non_all_two_divisible_words = 0
    rotation_identity_failures = 0
    divisibility_invariance_failures = 0
    primitive_factorization_failures = 0

    for word in product(alphabet, repeat=horizon):
        denominator = collatz_denominator(word)
        if denominator <= 0:
            continue
        positive_words += 1
        rotation_row = rotation_identity_row(word)
        rotation_identity_failures += int(
            not rotation_row["identity_2a0_Brot_equals_3B_plus_D"]
        )
        divisibility_invariance_failures += int(
            not rotation_row["divisibility_invariant"]
        )
        necklace = canonical_rotation(word)
        root = primitive_root(word)
        primitive_necklace = canonical_rotation(root)
        necklaces.add(necklace)
        primitive_necklaces.add(primitive_necklace)

        repetition_row = repetition_identity_row(root, horizon // len(root))
        primitive_factorization_failures += int(
            not repetition_row["numerator_factorization_holds"]
            or not repetition_row["denominator_factorization_holds"]
            or not repetition_row["divisibility_equivalent"]
        )

        numerator = ordered_affine_numerator(word)
        if numerator % denominator == 0:
            divisible_words += 1
            divisible_necklaces.add(necklace)
            divisible_primitive_necklaces.add(primitive_necklace)
            if any(value != 2 for value in word):
                non_all_two_divisible_words += 1

    return {
        "length": horizon,
        "valuation_alphabet": [1, 2, 3, 4],
        "positive_denominator_word_count": positive_words,
        "cyclic_necklace_count": len(necklaces),
        "primitive_necklace_count": len(primitive_necklaces),
        "divisible_raw_word_count": divisible_words,
        "divisible_necklace_count": len(divisible_necklaces),
        "divisible_primitive_necklace_count": len(divisible_primitive_necklaces),
        "non_all_two_divisible_raw_word_count": non_all_two_divisible_words,
        "rotation_identity_failure_count": rotation_identity_failures,
        "rotation_divisibility_failure_count": divisibility_invariance_failures,
        "primitive_factorization_failure_count": primitive_factorization_failures,
    }


def collatz_cross_length_necklace_counts(maximum_length: int) -> dict[str, int]:
    necklaces: set[tuple[int, ...]] = set()
    primitive_necklaces: set[tuple[int, ...]] = set()
    for horizon in range(2, maximum_length + 1):
        for word in product(range(1, 5), repeat=horizon):
            if collatz_denominator(word) <= 0:
                continue
            necklaces.add(canonical_rotation(word))
            primitive_necklaces.add(canonical_rotation(primitive_root(word)))
    return {
        "cross_length_cyclic_necklace_count": len(necklaces),
        "cross_length_unique_primitive_necklace_count": len(primitive_necklaces),
        "repeated_necklaces_removed": len(necklaces) - len(primitive_necklaces),
    }


def collatz_primitive_necklace_audit() -> dict[str, Any]:
    summaries = [collatz_necklace_summary(length) for length in range(2, 9)]
    cross_length = collatz_cross_length_necklace_counts(8)
    repetition_rows = [
        repetition_identity_row((2,), count) for count in range(2, 9)
    ] + [
        repetition_identity_row((3, 1), count) for count in range(2, 6)
    ] + [
        repetition_identity_row((4, 1), count) for count in range(2, 6)
    ]
    failures = sum(
        row["rotation_identity_failure_count"]
        + row["rotation_divisibility_failure_count"]
        + row["primitive_factorization_failure_count"]
        for row in summaries
    )
    failures += sum(
        int(
            not row["numerator_factorization_holds"]
            or not row["denominator_factorization_holds"]
            or not row["rational_cycle_value_preserved"]
            or not row["divisibility_equivalent"]
        )
        for row in repetition_rows
    )
    theorem = (
        "For a positive valuation word a=(a0,...,a_(h-1)), let B(a) be its "
        "affine numerator and D=2^sum(a)-3^h. If rho(a) is the left cyclic "
        "rotation, then 2^a0 B(rho(a))=3B(a)+D; consequently D divides B(a) "
        "if and only if D divides B(rho(a)). If a=u^k, then B(a)=B(u)G and "
        "D(a)=D(u)G for the same positive geometric factor G. Every periodic "
        "integrality test therefore reduces exactly to a primitive cyclic "
        "valuation necklace."
    )
    proof = (
        "One accelerated step sends x=B(a)/D to (3x+1)/2^a0, which is the "
        "cycle value associated with rho(a); clearing D gives the rotation "
        "identity. Since D is coprime to 2 and 3, divisibility is equivalent "
        "under rotation. Iterating the affine map for u, "
        "F_u(x)=(3^r x+B(u))/2^s, k times gives the common geometric factor "
        "G=sum_j 3^(r(k-1-j))2^(sj) in both numerator and denominator."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_rotation_examples": [
            rotation_identity_row((3, 1)),
            rotation_identity_row((4, 1, 2)),
            rotation_identity_row((2, 3, 1, 4)),
        ],
        "exact_repetition_examples": repetition_rows,
        "finite_primitive_necklace_audit": summaries,
        "aggregate": {
            "maximum_tested_length": 8,
            "total_positive_denominator_words": sum(
                row["positive_denominator_word_count"] for row in summaries
            ),
            "total_rotation_identity_failures": sum(
                row["rotation_identity_failure_count"] for row in summaries
            ),
            "total_primitive_factorization_failures": sum(
                row["primitive_factorization_failure_count"] for row in summaries
            ),
            "non_all_two_divisible_word_count_in_tested_box": sum(
                row["non_all_two_divisible_raw_word_count"] for row in summaries
            ),
            **cross_length,
            "raw_rotation_or_repetition_counts_are_independent_evidence": False,
            "nontrivial_cycles_excluded_for_all_lengths": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The reduction proves that rotations and powers of a word are not "
            "independent cycle candidates. It does not prove nondivisibility for "
            "the unbounded family of non-all-two primitive necklaces and says "
            "nothing about divergent nonperiodic trajectories."
        ),
        "failure_count": failures,
    }


def ordered_goldbach_count(limit: int) -> list[int]:
    is_prime = prime_sieve(limit)
    primes = [value for value in range(2, limit + 1) if is_prime[value]]
    counts = [0] * (limit + 1)
    for even in range(4, limit + 1, 2):
        counts[even] = sum(
            1 for prime in primes if prime <= even and is_prime[even - prime]
        )
    return counts


def goldbach_finite_row(limit: int, counts: list[int]) -> dict[str, Any]:
    targets = list(range(4, limit + 1, 2))
    exceptions = [target for target in targets if counts[target] == 0]
    return {
        "limit": limit,
        "even_target_count": len(targets),
        "exception_count": len(exceptions),
        "minimum_ordered_representation_count": min(counts[target] for target in targets),
        "maximum_ordered_representation_count": max(counts[target] for target in targets),
    }


def one_exception_model_row(limit: int, exception: int = 10) -> dict[str, Any]:
    target_count = max(0, (limit - 2) // 2)
    exception_count = int(limit >= exception)
    return {
        "limit": limit,
        "model_exception": exception,
        "even_target_count": target_count,
        "exception_count": exception_count,
        "exception_density": fraction_text(
            Fraction(exception_count, target_count) if target_count else Fraction(0)
        ),
        "subunit_threshold_met": exception_count < 1,
    }


def sparse_exception_model_row(limit: int) -> dict[str, Any]:
    exceptions = []
    value = 8
    while value <= limit:
        exceptions.append(value)
        value *= 2
    target_count = max(0, (limit - 2) // 2)
    return {
        "limit": limit,
        "exception_count": len(exceptions),
        "largest_exception": exceptions[-1] if exceptions else None,
        "exception_density": fraction_text(
            Fraction(len(exceptions), target_count) if target_count else Fraction(0)
        ),
        "density_below_one_tenth": (
            Fraction(len(exceptions), target_count) < Fraction(1, 10)
            if target_count
            else False
        ),
        "still_has_counterexamples": bool(exceptions),
    }


def goldbach_subunit_exceptional_audit() -> dict[str, Any]:
    counts = ordered_goldbach_count(10_000)
    finite_rows = [goldbach_finite_row(limit, counts) for limit in (100, 1_000, 10_000)]
    one_exception_rows = [
        one_exception_model_row(limit) for limit in (16, 64, 256, 1_024, 4_096)
    ]
    sparse_rows = [
        sparse_exception_model_row(limit)
        for limit in (64, 256, 1_024, 4_096, 65_536)
    ]
    failures = 0
    failures += sum(row["exception_count"] for row in finite_rows)
    failures += int(any(row["subunit_threshold_met"] for row in one_exception_rows))
    failures += int(not all(row["still_has_counterexamples"] for row in sparse_rows))
    failures += int(not sparse_rows[-1]["density_below_one_tenth"])
    theorem = (
        "Let E(X) be the number of even Goldbach exceptions up to X. After an "
        "exact verification through X0, any rigorous tail bound "
        "0<=E(X)-E(X0)<1 for every X>=X0 forces E(X)=E(X0) and therefore "
        "closes strong Goldbach. The strict subunit threshold is essential: "
        "bounds E(X)=O(1), E(X)=o(X), or even density zero do not exclude one "
        "or infinitely many sparse counterexamples."
    )
    proof = (
        "The tail exceptional count is a nonnegative integer. If it is strictly "
        "below one, it is zero. Conversely, a model with exactly one exceptional "
        "even integer has E(X)<=1 and E(X)/X tending to zero but is not an "
        "all-target theorem. A model exceptional at powers of two has infinitely "
        "many failures while its exceptional density also tends to zero."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_finite_prime_arithmetic_rows": finite_rows,
        "one_exception_no_go_rows": one_exception_rows,
        "sparse_infinite_exception_no_go_rows": sparse_rows,
        "aggregate": {
            "finite_verification_limit": 10_000,
            "finite_exception_count": finite_rows[-1]["exception_count"],
            "integer_subunit_tail_closure_proved": True,
            "density_zero_to_all_targets_inference_refuted": True,
            "bounded_exception_count_to_zero_inference_refuted": True,
            "actual_tail_exception_bound_below_one_constructed": False,
            "actual_goldbach_counterexample_found": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The countermodels concern logical promotion from exceptional-set "
            "bounds and are not prime arithmetic. The finite verification through "
            "10,000 is reproducible evidence only and cannot control the tail."
        ),
        "failure_count": failures,
    }


def rational_matrix_rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def twin_indefinite_kernel_audit() -> dict[str, Any]:
    primes = [2, 3, 5, 7, 11]
    labels = [1] + primes
    scores = {1: Fraction(1)} | {prime: Fraction(-1, 2) for prime in primes}
    matrix = [
        [scores[left] + scores[right] for right in labels] for left in labels
    ]
    rank = rational_matrix_rank(matrix)
    prime_channel = [scores[1] + scores[prime] for prime in primes]
    semiprime_channel = [
        scores[left] + scores[right] for left in primes for right in primes
    ]
    principal_minor = matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2
    failures = 0
    failures += int(rank > 2)
    failures += int(any(value <= 0 for value in prime_channel))
    failures += int(any(value >= 0 for value in semiprime_channel))
    failures += int(principal_minor != Fraction(-9, 4))
    theorem = (
        "No positive-semidefinite symmetric bilinear kernel can be strictly "
        "negative on every prime-semiprime factor channel: a square semiprime "
        "p^2 would require K(p,p)<0, contradicting positive semidefiniteness. "
        "Indefiniteness removes this algebraic obstruction. On formal factor "
        "pairs, K(a,b)=s(a)+s(b), with s(1)=1 and s(p)=-1/2 for primes p, "
        "has rank at most two, gives K(1,p)=1/2>0, and gives K(p,q)=-1<0."
    )
    proof = (
        "A PSD kernel is a Gram kernel, so every diagonal value K(p,p) is a "
        "squared norm and is nonnegative. This rules out strict negative weight "
        "on p^2. For the explicit escape, K=s 1^T+1 s^T, hence rank(K)<=2. "
        "Direct substitution gives the two channel signs. The 2x2 principal "
        "minor on {1,p} is 2(-1)-(1/2)^2=-9/4, certifying that the escape "
        "kernel is indefinite rather than a hidden nonnegative sieve square."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "psd_square_semiprime_no_go": {
            "required_negative_diagonal": "K(p,p)<0 for every prime p",
            "psd_diagonal_constraint": "K(p,p)>=0",
            "strict_psd_parity_separator_exists": False,
        },
        "exact_indefinite_rank_two_escape": {
            "factor_labels": labels,
            "score_s": {str(label): fraction_text(scores[label]) for label in labels},
            "kernel_formula": "K(a,b)=s(a)+s(b)",
            "matrix": [
                [fraction_text(value) for value in row] for row in matrix
            ],
            "exact_rank": rank,
            "prime_channel_values_K_1_p": [
                fraction_text(value) for value in prime_channel
            ],
            "semiprime_channel_distinct_values_K_p_q": sorted(
                {fraction_text(value) for value in semiprime_channel}
            ),
            "principal_minor_on_1_and_first_prime": fraction_text(principal_minor),
            "kernel_is_indefinite": principal_minor < 0,
            "formal_factor_channel_separation_holds": (
                all(value > 0 for value in prime_channel)
                and all(value < 0 for value in semiprime_channel)
            ),
        },
        "aggregate": {
            "psd_or_square_weight_signed_separation_refuted": True,
            "formal_indefinite_rank_two_separator_constructed": True,
            "factorization_free_arithmetic_realization_constructed": False,
            "uniform_distribution_remainder_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The rank-two kernel separates formal factor channels only because "
            "the factor pair is exposed. It is not a computable weight of n alone, "
            "does not supply a switching decomposition with controlled remainder, "
            "and proves no twin prime lower bound."
        ),
        "failure_count": failures,
    }


def proof_dag(
    prefix: str,
    previous: str,
    closed: str,
    refuted: str,
    open_lemma: str,
    parent: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T203", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T204", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N204",
                "label": refuted,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN204",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": parent, "status": "open_not_proven"},
        ],
        "edges": [
            [f"{prefix}-T203", f"{prefix}-T204"],
            [f"{prefix}-T204", f"{prefix}-N204"],
            [f"{prefix}-T204", f"{prefix}-OPEN204"],
            [f"{prefix}-OPEN204", prefix],
        ],
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_mesh_certificate_audit()
    collatz_compute = collatz_primitive_necklace_audit()
    goldbach_compute = goldbach_subunit_exceptional_audit()
    twin_compute = twin_indefinite_kernel_audit()

    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-204",
            "theorem_name": "DerivativeCertifiedRoucheMeshAndFiniteSamplingNoGo",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": (
                "The mesh transfer is exact, but no Xi-specific cofinal relative "
                "derivative bound or comparison function is constructed."
            ),
            "route_decision": {
                "discard": "finite contour sampling without a certified regularity bound",
                "retain": "adaptive contour sampling plus a certified relative derivative bound",
                "next_single_lemma": "CompletedZetaCofinalAdaptiveRelativeDerivativeBound",
            },
            "proof_dag": proof_dag(
                "RH",
                "CertifiedIncludedZerosPlusRoucheCountExactExhaustion",
                "DerivativeCertifiedRoucheMeshAndFiniteSamplingNoGo",
                "FiniteContourSamplesAloneCertifyRoucheMargin",
                "CompletedZetaCofinalAdaptiveRelativeDerivativeBound",
                "Riemann Hypothesis",
            ),
            "claim_boundary": (
                "No RH proof or counterexample. The finite-mesh transfer and a "
                "sampling-only no-go are exact; the Xi-specific derivative premise is open."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-204",
            "theorem_name": "RotationAndPowerReductionToPrimitiveValuationNecklaces",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": (
                "Periodic candidates reduce to primitive necklaces, but the "
                "unbounded non-all-two primitive family and nonperiodic trajectories remain open."
            ),
            "route_decision": {
                "discard": "counting cyclic rotations and repeated words as independent cycle evidence",
                "retain": "one canonical primitive necklace per periodic valuation class",
                "next_single_lemma": "UniformNondivisibilityForAllNonAllTwoPrimitiveValuationNecklaces",
            },
            "proof_dag": proof_dag(
                "CO",
                "ExactSignedTwoSiteTransferIdentityAndUniversalObstructionNoGo",
                "RotationAndPowerReductionToPrimitiveValuationNecklaces",
                "RotationsAndWordPowersProvideIndependentCycleEvidence",
                "UniformNondivisibilityForAllNonAllTwoPrimitiveValuationNecklaces",
                "Collatz Conjecture",
            ),
            "claim_boundary": (
                "No Collatz proof, divergent orbit exclusion, or nontrivial cycle. "
                "An exact symmetry and power reduction for periodic words is proved."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-204",
            "theorem_name": "ExceptionalSetSubunitClosureAndDensityZeroNoGo",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": (
                "The integer promotion threshold is exact, but no analytic "
                "Goldbach tail bound strictly below one is obtained."
            ),
            "route_decision": {
                "discard": "promoting density-zero or bounded exceptional sets directly to zero exceptions",
                "retain": "finite verification plus a rigorous tail exceptional count below one",
                "next_single_lemma": "ExplicitBinaryGoldbachTailExceptionalCountStrictlyBelowOne",
            },
            "proof_dag": proof_dag(
                "GB",
                "PointwiseLogLogDefectStrictStrengthCalibration",
                "ExceptionalSetSubunitClosureAndDensityZeroNoGo",
                "DensityZeroExceptionalSetImpliesNoGoldbachExceptions",
                "ExplicitBinaryGoldbachTailExceptionalCountStrictlyBelowOne",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": (
                "No Goldbach proof or counterexample. The exact integer threshold "
                "for exceptional-set promotion and two logical no-go models are established."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-204",
            "theorem_name": "PsdParitySeparationNoGoAndIndefiniteRankTwoFactorEscape",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": (
                "The indefinite kernel separates formal exposed-factor channels "
                "only; no factorization-free switching weight or uniform remainder is proved."
            ),
            "route_decision": {
                "discard": "PSD or square-form bilinear weights as strict prime-versus-P2 sign separators",
                "retain": "indefinite factor-visible switching with independently controlled arithmetic remainder",
                "next_single_lemma": "ArithmeticRealizationOfIndefiniteRankTwoSwitchingKernelWithUniformRemainder",
            },
            "proof_dag": proof_dag(
                "TP",
                "FixedPrimorialSingleCoordinatePrimeSemiprimeSeparationNoGo",
                "PsdParitySeparationNoGoAndIndefiniteRankTwoFactorEscape",
                "PositiveSemidefiniteKernelStrictlySeparatesPrimeFromEveryP2",
                "ArithmeticRealizationOfIndefiniteRankTwoSwitchingKernelWithUniformRemainder",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": (
                "No Twin Prime proof or counterexample. A PSD parity no-go and "
                "a purely algebraic indefinite factor-channel escape are proved."
            ),
        },
    }
    failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    boundary = (
        "TICKET-204 resolves none of the four conjectures. It proves a derivative-"
        "certified Rouche mesh theorem and finite-sampling no-go, reduces periodic "
        "Collatz words to primitive necklaces, identifies the strict subunit "
        "exceptional-set threshold for Goldbach, and separates the PSD sieve parity "
        "barrier from an indefinite rank-two formal factor-channel escape."
    )
    return {
        "theorem_name": "FourConjectureContinuousAndInfinitePromotionAudit",
        "status": STATUS,
        "proof_boundary": boundary,
        **sections,
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_limited_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = []
    for section_key in ("riemann", "collatz", "goldbach", "twin_prime"):
        section = audit[section_key]
        decision = section["route_decision"]
        attempts.append(
            {
                "problem_id": section["problem_id"],
                "ticket_id": section["ticket_id"],
                "status": STATUS,
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": decision["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": decision["next_single_lemma"],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": decision["next_single_lemma"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    boundary = audit["proof_boundary"]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": boundary,
        "continuous_and_infinite_promotion_audit": audit,
        "attempts": attempts,
    }
    integrated = (
        ROOT
        / "data"
        / "open-problem"
        / "ticket204-mesh-necklace-exceptional-kernel.json"
    )
    write_json(integrated, payload)

    file_map = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-204-mesh-certificate.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-204-primitive-necklace.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-204-subunit-exceptional.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-204-indefinite-kernel.json",
    }
    section_map = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    for attempt in attempts:
        problem_id = attempt["problem_id"]
        section = audit[section_map[problem_id]]
        write_json(
            file_map[problem_id],
            {
                "schema": "primeproject.open-problem-attempt.v1",
                "generated_at": GENERATED_AT,
                **attempt,
                "mathematical_argument": section["mathematical_argument"],
                "reproducible_computation": section["reproducible_computation"],
                "route_decision": section["route_decision"],
            },
        )

    digest = hashlib.sha256(integrated.read_bytes()).hexdigest()
    print(f"integrated_sha256 {digest}")


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            audit["machine_audit"],
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
