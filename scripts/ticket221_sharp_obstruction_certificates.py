from __future__ import annotations

import hashlib
import itertools
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from ticket220_dyadic_partition_primitive_refinement_crt import (
    cyclic_transition_count,
    goldbach_refinement_audit,
    primitive_root,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket221-sharp-obstruction-certificates.v1"
GENERATED_AT = "2026-08-15T09:30:00+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fraction_string(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def decimal_string(value: Decimal, digits: int = 30) -> str:
    return format(value, f".{digits}E")


def proof_dag(
    prefix: str,
    previous: str,
    closed: str,
    rejected: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T220", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T221", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N221",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN221",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T220", f"{prefix}-T221"],
            [f"{prefix}-T221", f"{prefix}-N221"],
            [f"{prefix}-T221", f"{prefix}-OPEN221"],
            [f"{prefix}-OPEN221", prefix],
        ],
    }


def dyadic_kernel(x: Decimal) -> Decimal:
    return (-x).exp() - (-(Decimal(2) * x)).exp()


def riemann_scale_uniform_envelope_audit() -> dict[str, Any]:
    getcontext().prec = 100
    height = Decimal(11)
    log_two = Decimal(2).ln()
    quarter = Decimal(1) / Decimal(4)
    scale_rows = []
    failures = 0

    for index in range(-12, 13):
        atom = height * (Decimal(2) ** index) * log_two
        x = (Decimal(2) ** (-index)) * atom / height
        value = dyadic_kernel(x)
        derivative = -(-x).exp() + Decimal(2) * (
            -(Decimal(2) * x)
        ).exp()
        maximum_verified = abs(value - quarter) < Decimal("1e-90")
        stationary_verified = abs(derivative) < Decimal("1e-90")
        failures += int(not (maximum_verified and stationary_verified))
        scale_rows.append(
            {
                "dyadic_index_j": index,
                "maximizing_atom_t": decimal_string(atom),
                "normalized_x": decimal_string(x),
                "kernel_value": decimal_string(value),
                "derivative_at_x": decimal_string(derivative),
                "maximum_one_quarter_verified": maximum_verified,
                "stationary_point_verified": stationary_verified,
            }
        )

    partial_sum_rows = []
    for radius in (1, 2, 4, 8, 16, 32):
        lower_bound = Fraction(2 * radius + 1, 4)
        partial_sum_rows.append(
            {
                "radius_R": radius,
                "envelope_coordinates": 2 * radius + 1,
                "universal_envelope_partial_sum_lower_bound": fraction_string(
                    lower_bound
                ),
                "already_exceeds_one": lower_bound > 1,
            }
        )

    theorem = (
        "For K_j(t;H)=exp(-2^(-j)t/H)-exp(-2^(1-j)t/H), H>0, "
        "one has sup_(t>0) K_j(t;H)=1/4 for every integer j. Hence any "
        "coordinatewise envelope U_j that dominates K_j(t;H) for every "
        "possible one-atom positive defect measure must satisfy U_j>=1/4 "
        "for all j, so sum_j U_j diverges. In particular, the TICKET-220 "
        "summable-envelope route cannot be completed by scale-uniform, "
        "arithmetic-free bounds applied independently to each band."
    )
    proof = (
        "Put x=2^(-j)t/H. As t ranges over (0,infinity), so does x, and "
        "K_j=e^(-x)-e^(-2x). Its derivative is -e^(-x)+2e^(-2x), which "
        "vanishes only at x=log 2; the endpoint limits are zero and the "
        "value at log 2 is 1/2-1/4=1/4. A one-atom defect placed at "
        "t=H 2^j log 2 therefore forces U_j>=1/4. Summing over infinitely "
        "many j proves divergence. This does not exclude an envelope tied "
        "to the actual prime-side explicit formula or a coupled estimate "
        "that transfers budget between scales."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "kernel": "exp(-x)-exp(-2x), x=2^(-j)t/H",
        "scale_maximum_rows": scale_rows,
        "universal_envelope_partial_sum_rows": partial_sum_rows,
        "aggregate": {
            "sharp_scale_supremum_one_quarter_proved": True,
            "universal_coordinatewise_envelope_diverges": True,
            "ticket220_scale_uniform_envelope_route_refuted": True,
            "actual_arithmetic_coupled_tail_budget_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "Only envelopes that dominate every possible one-atom defect "
            "independently at every scale are excluded. Arithmetic-dependent "
            "coupled bounds, signed explicit-formula cancellation, and direct "
            "Weil or Li positivity arguments are not excluded."
        ),
        "failure_count": failures,
    }


def affine_word_exact(word: tuple[int, ...]) -> tuple[int, int, int]:
    a, b, d = 1, 0, 1
    for valuation in word:
        a, b, d = 3 * a, 3 * b + d, d * (2**valuation)
    return a, b, d


def intercept_formula(word: tuple[int, ...]) -> int:
    height = len(word)
    prefix = 0
    total = 0
    for index, valuation in enumerate(word):
        total += (3 ** (height - index - 1)) * (2**prefix)
        prefix += valuation
    return total


def adjacent_swap_predicted_difference(
    word: tuple[int, ...], index: int
) -> int:
    height = len(word)
    prefix = sum(word[:index])
    left = word[index]
    right = word[index + 1]
    return (3 ** (height - index - 2)) * (2**prefix) * (
        (2**left) - (2**right)
    )


def collatz_order_sensitive_intercept_audit() -> dict[str, Any]:
    seed_multisets = (
        (1, 1, 2, 4),
        (1, 2, 2, 4),
        (1, 2, 3, 4),
        (1, 1, 2, 3, 4),
    )
    class_rows = []
    swap_rows = []
    transcript = hashlib.sha256()
    failures = 0

    for seed in seed_multisets:
        words = sorted(set(itertools.permutations(seed)))
        records = []
        for word in words:
            a, b, d = affine_word_exact(word)
            formula_b = intercept_formula(word)
            denominator = d - a
            primitive_multi_run = (
                primitive_root(word) == word
                and cyclic_transition_count(word) >= 4
            )
            failures += int(formula_b != b)
            records.append(
                {
                    "word": list(word),
                    "A": a,
                    "B": b,
                    "D": d,
                    "fixed_point_denominator_D_minus_A": denominator,
                    "fixed_point_n": fraction_string(Fraction(b, denominator)),
                    "fixed_point_above_one": b > denominator,
                    "denominator_divides_intercept": b % denominator == 0,
                    "primitive_multi_run": primitive_multi_run,
                }
            )
            transcript.update(f"{word}:{a}:{b}:{d}\n".encode("ascii"))

            for index in range(len(word) - 1):
                if word[index] == word[index + 1]:
                    continue
                swapped = list(word)
                swapped[index], swapped[index + 1] = (
                    swapped[index + 1],
                    swapped[index],
                )
                swapped_word = tuple(swapped)
                _, swapped_b, _ = affine_word_exact(swapped_word)
                predicted = adjacent_swap_predicted_difference(word, index)
                actual = b - swapped_b
                verified = actual == predicted
                failures += int(not verified)
                swap_rows.append(
                    {
                        "word": list(word),
                        "swap_index_zero_based": index,
                        "swapped_word": list(swapped_word),
                        "actual_B_difference": actual,
                        "predicted_B_difference": predicted,
                        "identity_verified": verified,
                    }
                )

        slopes = {(row["A"], row["D"]) for row in records}
        intercepts = {row["B"] for row in records}
        class_rows.append(
            {
                "valuation_multiset": list(seed),
                "height_h": len(seed),
                "valuation_sum_S": sum(seed),
                "permutation_count": len(records),
                "slope_pair_A_D": list(next(iter(slopes))),
                "single_baker_datum_for_all_permutations": len(slopes) == 1,
                "distinct_intercept_count": len(intercepts),
                "minimum_intercept_B": min(intercepts),
                "maximum_intercept_B": max(intercepts),
                "primitive_multi_run_permutation_count": sum(
                    row["primitive_multi_run"] for row in records
                ),
                "any_integer_fixed_point": any(
                    row["denominator_divides_intercept"] for row in records
                ),
            }
        )
        failures += int(len(slopes) != 1 or len(intercepts) <= 1)

    low_word = (1, 2, 3, 4)
    high_word = (3, 4, 2, 1)
    low_a, low_b, low_d = affine_word_exact(low_word)
    high_a, high_b, high_d = affine_word_exact(high_word)
    denominator = low_d - low_a
    witness_checks = {
        "same_height": len(low_word) == len(high_word),
        "same_valuation_sum": sum(low_word) == sum(high_word),
        "same_slope_A_over_D": (low_a, low_d) == (high_a, high_d),
        "both_primitive_multi_run": all(
            primitive_root(word) == word and cyclic_transition_count(word) >= 4
            for word in (low_word, high_word)
        ),
        "not_cyclic_rotations": high_word not in {
            low_word[index:] + low_word[:index]
            for index in range(len(low_word))
        },
        "low_order_fixed_point_below_one": low_b < denominator,
        "high_order_fixed_point_above_one": high_b > denominator,
        "intercepts_differ": low_b != high_b,
    }
    failures += sum(not value for value in witness_checks.values())

    theorem = (
        "For an accelerated Collatz valuation word a=(a_1,...,a_h), its "
        "one-turn affine map is (3^h n+B(a))/2^S, where S=sum a_i and "
        "B(a)=sum_(i=1)^h 3^(h-i)2^(a_1+...+a_(i-1)). The Baker linear "
        "form S log 2-h log 3 and the slope 3^h/2^S are invariant under "
        "permutation, but B is not: swapping adjacent unequal x,y after "
        "prefix sum s changes B by 3^(h-i-1)2^s(2^x-2^y), with one-based "
        "position i. In particular, the cyclically inequivalent primitive "
        "multi-run words (1,2,3,4) and (3,4,2,1) share h=4,S=10 and "
        "denominator 943, yet their intercepts are 133 and 995, so their "
        "rational fixed points lie on opposite sides of one. Thus scalar "
        "Baker separation in "
        "h,S is not a sufficient statistic for primitive-word closure."
    )
    proof = (
        "Induction through n -> (3n+1)/2^a gives the displayed affine "
        "formula. A permutation leaves h and S unchanged. In the intercept "
        "sum, an adjacent swap changes only the second of the two local "
        "terms before their common total prefix resumes, giving the stated "
        "difference exactly. Direct substitution gives A=81,D=1024 and "
        "D-A=943 for both witness words, while B=133 and B=995. The words "
        "are not cyclic rotations. Therefore "
        "a lower bound for |S log 2-h log 3| alone loses order information "
        "needed even to locate the rational fixed point, let alone prove "
        "divisibility and exact 2-adic valuation admissibility."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "permutation_class_rows": class_rows,
        "adjacent_swap_identity_rows": swap_rows,
        "opposite_side_witness": {
            "low_word": list(low_word),
            "low_intercept_B": low_b,
            "low_fixed_point": fraction_string(Fraction(low_b, denominator)),
            "high_word": list(high_word),
            "high_intercept_B": high_b,
            "high_fixed_point": fraction_string(Fraction(high_b, denominator)),
            "common_A": low_a,
            "common_D": low_d,
            "common_D_minus_A": denominator,
            "checks": witness_checks,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "order_sensitive_intercept_formula_proved": True,
            "adjacent_swap_identity_proved": True,
            "same_baker_data_can_straddle_fixed_point_one": True,
            "baker_separation_alone_sufficient_for_primitive_words": False,
            "order_sensitive_cycle_divisibility_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The result rejects only a criterion that uses h,S or the scalar "
            "two-logarithm separation without order-sensitive data. It does "
            "not reject Baker estimates combined with intercept divisibility, "
            "2-adic admissibility, or a global descent argument."
        ),
        "failure_count": failures,
    }


def lp_residual_power(
    vector: Iterable[Fraction], model: Iterable[Fraction], order: int
) -> Fraction:
    return sum(
        abs(value - target) ** order
        for value, target in zip(vector, model, strict=True)
    )


def goldbach_sharp_positivity_radius_audit() -> dict[str, Any]:
    models = (
        tuple(Fraction(value) for value in (3, 5, 7, 11, 13)),
        tuple(Fraction(value, 3) for value in (5, 8, 11, 17, 20, 26)),
        tuple(Fraction(value, 5) for value in (7, 9, 14, 18, 23, 31, 36)),
    )
    radius_rows = []
    failures = 0
    for model_index, model in enumerate(models):
        minimum = min(model)
        zero_index = model.index(minimum)
        witness = list(model)
        witness[zero_index] = Fraction(0)
        for order in (1, 2, 4, 8):
            power = lp_residual_power(witness, model, order)
            expected = minimum**order
            verified = power == expected
            failures += int(not verified)
            radius_rows.append(
                {
                    "model_index": model_index,
                    "dimension": len(model),
                    "p": order,
                    "minimum_model_coordinate": fraction_string(minimum),
                    "zero_witness_index": zero_index,
                    "residual_pth_power": fraction_string(power),
                    "expected_radius_pth_power": fraction_string(expected),
                    "sharp_boundary_verified": verified,
                }
            )

    extension_rows = []
    for prefix_length in (4, 8, 16, 32, 64):
        old_model = tuple(Fraction(index + 2) for index in range(prefix_length))
        old_counts = old_model
        new_model_coordinate = Fraction(prefix_length + 2)
        extended_model = old_model + (new_model_coordinate,)
        extended_counts = old_counts + (Fraction(0),)
        old_residual = lp_residual_power(old_counts, old_model, 8)
        extended_residual = lp_residual_power(
            extended_counts, extended_model, 8
        )
        checks = {
            "old_prefix_unchanged": extended_counts[:-1] == old_counts,
            "old_prefix_certificate_exact": old_residual == 0,
            "new_coordinate_is_zero": extended_counts[-1] == 0,
            "extended_residual_hits_new_zero_barrier": (
                extended_residual == new_model_coordinate**8
            ),
        }
        failures += sum(not value for value in checks.values())
        extension_rows.append(
            {
                "certified_prefix_length": prefix_length,
                "old_eighth_residual_power": fraction_string(old_residual),
                "new_model_coordinate": fraction_string(new_model_coordinate),
                "extended_eighth_residual_power": fraction_string(
                    extended_residual
                ),
                "checks": checks,
            }
        )

    previous = goldbach_refinement_audit()
    bridge_rows = previous["refinement_bridge_rows"]
    worst_ratio = max(
        Decimal(row["minkowski_to_barrier_ratio"]) for row in bridge_rows
    )

    theorem = (
        "Let m be a vector with strictly positive coordinates and let Z be "
        "the set of nonnegative vectors having at least one zero coordinate. "
        "For every 1<=p<infinity, dist_p(m,Z)=min_i m_i; the same holds for "
        "p=infinity. Hence ||r-m||_p<min_i m_i guarantees r_i>0 for every "
        "i, and the strict constant is optimal. Appending one unchecked zero "
        "coordinate leaves every finite-prefix certificate unchanged while "
        "hitting the new zero barrier exactly. Therefore TICKET-220's finite "
        "cross-fit margins cannot become a cofinal Goldbach theorem without "
        "an independent uniform all-block margin estimate."
    )
    proof = (
        "If z_k=0, then ||z-m||_p>=|z_k-m_k|=m_k>=min_i m_i. Equality is "
        "attained by changing only a coordinate where m is minimal to zero; "
        "the sup norm is identical. The positivity implication follows by "
        "contraposition. For any certified finite prefix, append a positive "
        "model coordinate and an observed value zero. No old coordinate or "
        "old statistic changes, but the extended vector is on Z. This proves "
        "sharpness and the finite-prefix no-go, not an asymptotic estimate "
        "for actual Goldbach representation counts."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_lp_radius_rows": radius_rows,
        "finite_prefix_extension_rows": extension_rows,
        "ticket220_finite_margin_summary": {
            "direct_eighth_moment_folds_certified": previous["aggregate"][
                "direct_eighth_moment_folds_certified"
            ],
            "direct_eighth_moment_fold_total": previous["aggregate"][
                "direct_eighth_moment_fold_total"
            ],
            "refinement_bridges_certified": previous["aggregate"][
                "refinement_bridges_certified"
            ],
            "refinement_bridge_total": previous["aggregate"][
                "refinement_bridge_total"
            ],
            "worst_minkowski_to_zero_barrier_ratio": decimal_string(
                worst_ratio, 18
            ),
        },
        "aggregate": {
            "exact_lp_distance_to_zero_set_proved": True,
            "strict_zero_barrier_constant_proved_sharp": True,
            "finite_prefix_to_cofinal_positivity_route_refuted": True,
            "uniform_cofinal_margin_from_prime_distribution_proved": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem is the exact geometry of residual certificates. It "
            "does not rule out a circle-method or transference estimate that "
            "proves a uniform residual ratio below one for every sufficiently "
            "large dyadic block."
        ),
        "failure_count": failures + previous["failure_count"],
    }


def parity_value(point: tuple[int, ...]) -> int:
    product = 1
    for value in point:
        product *= value
    return product


def monomial_value(point: tuple[int, ...], subset: tuple[int, ...]) -> int:
    product = 1
    for index in subset:
        product *= point[index]
    return product


def twin_boolean_parity_audit() -> dict[str, Any]:
    rows = []
    transcript = hashlib.sha256()
    failures = 0
    for dimension in range(2, 13):
        points = list(itertools.product((-1, 1), repeat=dimension))
        maximum_low_degree_correlation_sum = 0
        checked_monomials = 0
        degree_counts = {}
        for degree in range(dimension):
            degree_maximum = 0
            for subset in itertools.combinations(range(dimension), degree):
                correlation_sum = sum(
                    parity_value(point) * monomial_value(point, subset)
                    for point in points
                )
                degree_maximum = max(degree_maximum, abs(correlation_sum))
                checked_monomials += 1
                transcript.update(
                    f"{dimension}:{subset}:{correlation_sum}\n".encode("ascii")
                )
            degree_counts[str(degree)] = {
                "monomial_count": len(
                    list(itertools.combinations(range(dimension), degree))
                ),
                "maximum_absolute_correlation_sum": degree_maximum,
            }
            maximum_low_degree_correlation_sum = max(
                maximum_low_degree_correlation_sum, degree_maximum
            )

        full_subset = tuple(range(dimension))
        full_correlation_sum = sum(
            parity_value(point) * monomial_value(point, full_subset)
            for point in points
        )
        checks = {
            "all_degrees_below_m_orthogonal": (
                maximum_low_degree_correlation_sum == 0
            ),
            "full_degree_recovers_parity": full_correlation_sum == 2**dimension,
            "all_proper_walsh_monomials_checked": (
                checked_monomials == (2**dimension) - 1
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "boolean_dimension_m": dimension,
                "cube_point_count": len(points),
                "proper_monomials_checked": checked_monomials,
                "maximum_low_degree_absolute_correlation_sum": (
                    maximum_low_degree_correlation_sum
                ),
                "full_degree_correlation_sum": full_correlation_sum,
                "degree_audit": degree_counts,
                "checks": checks,
            }
        )

    theorem = (
        "On the uniform Boolean cube {-1,1}^m, the parity character "
        "P(x)=product_(i=1)^m x_i is orthogonal to every polynomial of "
        "Walsh degree below m. Indeed, for every proper subset S, the mean "
        "of P(x) product_(i in S)x_i is zero, while the full-degree "
        "correlation is one. Consequently any abstract sieve statistic "
        "whose selected-prime interaction expansion has degree <m has zero "
        "correlation with factor parity in this balanced model. A claimed "
        "Twin lower bound from such low-degree local data alone therefore "
        "fails this exact parity stress test."
    )
    proof = (
        "For a proper S choose k outside S. Pair each cube point x with the "
        "point obtained by flipping x_k. The monomial on S is unchanged and "
        "P changes sign, so all terms cancel. For S equal to every coordinate, "
        "P(x)^2=1 at all 2^m points. By linearity every polynomial supported "
        "on proper Walsh subsets is orthogonal to parity. This is an exact "
        "finite model of the information loss behind the sieve parity "
        "barrier; it is not a theorem that every analytic bilinear form has "
        "low Walsh degree, nor a lower bound for Lambda(n)Lambda(n+2)."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "boolean_parity_orthogonality_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "proper_walsh_degree_parity_orthogonality_proved": True,
            "full_degree_parity_correlation_recovered": True,
            "low_degree_local_parity_certificate_refuted": True,
            "arithmetic_parity_breaking_type_ii_lower_bound_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The no-go applies to the balanced Boolean model and observables "
            "with no full selected-prime interaction. It does not classify "
            "Maynard weights, Type II information, shifted convolution sums, "
            "or every possible parity-breaking analytic method."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_scale_uniform_envelope_audit()
    collatz_compute = collatz_order_sensitive_intercept_audit()
    goldbach_compute = goldbach_sharp_positivity_radius_audit()
    twin_compute = twin_boolean_parity_audit()

    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-221",
            "theorem_name": "ScaleUniformDyadicEnvelopeDivergenceNoGo",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No arithmetic-coupled prime-side tail budget with total mass below one is proved.",
            "route_decision": {
                "discard": "independently dominating every dyadic band by a scale-uniform arithmetic-free envelope",
                "retain": "coupled explicit-formula estimates whose total tail budget uses actual prime arithmetic across scales",
                "next_single_lemma": "ArithmeticCoupledDyadicTailBudgetBelowOne",
            },
            "proof_dag": proof_dag(
                "RH",
                "DyadicLaplacePartitionAndFiniteWindowNoGo",
                "ScaleUniformDyadicEnvelopeDivergenceNoGo",
                "ScaleUniformCoordinatewiseEnvelopeCanBeSummable",
                "ArithmeticCoupledDyadicTailBudgetBelowOne",
                "Riemann Hypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-221",
            "theorem_name": "OrderBlindLogarithmicSeparationNoGoForPrimitiveWords",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "No order-sensitive divisibility or global descent theorem for arbitrary primitive valuation words is proved.",
            "route_decision": {
                "discard": "treating a lower bound for |S log 2-h log 3| alone as a complete primitive-word cycle criterion",
                "retain": "combine logarithmic separation with the ordered affine intercept, divisibility, and exact valuation admissibility",
                "next_single_lemma": "OrderSensitiveDivisibilityOrDescentForPrimitiveValuationWords",
            },
            "proof_dag": proof_dag(
                "CO",
                "PrimitiveRootExtensionOfSingleMountainExclusion",
                "OrderBlindLogarithmicSeparationNoGoForPrimitiveWords",
                "BakerDatumHSDeterminesPrimitiveWordClosure",
                "OrderSensitiveDivisibilityOrDescentForPrimitiveValuationWords",
                "Collatz Conjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-221",
            "theorem_name": "SharpLpDistanceToGoldbachZeroSet",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "No representation-free prime-distribution estimate proves a strict residual ratio below one on every sufficiently large block.",
            "route_decision": {
                "discard": "promoting finite cross-fit success or higher moment order to cofinal positivity without a uniform margin theorem",
                "retain": "derive an all-large-block residual bound strictly inside the exact positive-orthant radius",
                "next_single_lemma": "UniformCofinalLpMarginBelowOneFromPrimeDistribution",
            },
            "proof_dag": proof_dag(
                "GB",
                "CrossFitPartitionRefinementStabilityCertificate",
                "SharpLpDistanceToGoldbachZeroSet",
                "FiniteCrossFitMarginsImplyCofinalPositivity",
                "UniformCofinalLpMarginBelowOneFromPrimeDistribution",
                "Strong Goldbach Conjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-221",
            "theorem_name": "LowDegreeBooleanParityOrthogonalityNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No arithmetic Type II or shifted-von-Mangoldt lower bound breaking parity at gap two is proved.",
            "route_decision": {
                "discard": "claiming parity sensitivity from an observable with only proper low-degree selected-prime interactions",
                "retain": "construct genuinely parity-breaking arithmetic correlation beyond the balanced Boolean model",
                "next_single_lemma": "VonMangoldtPairLowerBoundWithParityBreakingTypeIIInput",
            },
            "proof_dag": proof_dag(
                "TP",
                "FiniteWheelTwinCertificationCRTNoGo",
                "LowDegreeBooleanParityOrthogonalityNoGo",
                "LowDegreeLocalSieveStatisticDetectsFactorParity",
                "VonMangoldtPairLowerBoundWithParityBreakingTypeIIInput",
                "Twin Prime Conjecture",
            ),
        },
    }

    machine_audit = {
        "exact_partial_theorem_count": 4,
        "refuted_or_limited_route_count": 4,
        "corrected_next_lemma_count": 4,
        "proof_dag_count": 4,
        "conjecture_resolution_count": 0,
        "total_failure_count": sum(
            section["reproducible_computation"]["failure_count"]
            for section in sections.values()
        ),
    }
    audit = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": (
            "TICKET-221 proves four exact obstruction or sharpness theorems "
            "and resolves none of the four parent conjectures."
        ),
        "sharp_obstruction_certificate_audit": {
            "theorem_name": "SharpObstructionCertificatesForFourOpenProblems",
            "status": STATUS,
            "proof_boundary": (
                "The results correct four insufficient next-lemma formulations. "
                "They resolve none of RH, Collatz, Goldbach, or Twin Prime."
            ),
            **sections,
            "cross_problem_synthesis": (
                "All four failures are information-boundary failures: independent "
                "scale envelopes lose arithmetic coupling, scalar Collatz slope "
                "data lose word order, finite Goldbach norms lose unchecked "
                "coordinates, and low-degree sieve observables lose parity."
            ),
            "literature_boundary": {
                "riemann": "Li positivity and Weil-type criteria motivate global coupled positivity; the dyadic supremum theorem here is an elementary project obstruction and carries no literature-priority claim.",
                "collatz": "Baker-type logarithmic bounds and cycle work by Simons motivate the scalar separation input; the adjacent-swap identity is used only to expose missing order information.",
                "goldbach": "Circle-method exceptional-set research targets uniform arithmetic estimates; the Lp radius theorem here is finite-dimensional geometry, not a new Goldbach asymptotic.",
                "twin_prime": "The classical sieve parity problem and Maynard's bounded-gap method define the boundary; the Boolean-cube theorem is an exact stress model, not a classification of all sieve methods.",
            },
            "machine_audit": machine_audit,
        },
        "attempts": [],
    }

    for key, section in sections.items():
        route = section["route_decision"]
        audit["attempts"].append(
            {
                "problem_id": section["problem_id"],
                "ticket_id": section["ticket_id"],
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "status": STATUS,
                "bounded_result": {
                    "audit_ref": "#/sharp_obstruction_certificate_audit",
                    "failure_count": section["reproducible_computation"][
                        "failure_count"
                    ],
                },
                "discarded_route": route["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": route["next_single_lemma"],
            }
        )
    return audit


def write_outputs(audit: dict[str, Any]) -> None:
    integrated_path = (
        ROOT / "data/open-problem/ticket221-sharp-obstruction-certificates.json"
    )
    write_json(integrated_path, audit)
    section_root = audit["sharp_obstruction_certificate_audit"]
    track_paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-221-scale-uniform-envelope.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-221-order-sensitive-intercept.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-221-sharp-lp-positivity-barrier.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-221-boolean-parity-orthogonality.json",
    }
    for key, path in track_paths.items():
        section = section_root[key]
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": STATUS,
                **section,
            },
        )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    machine = audit["sharp_obstruction_certificate_audit"]["machine_audit"]
    print(json.dumps(machine, indent=2))
    return 0 if machine["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
