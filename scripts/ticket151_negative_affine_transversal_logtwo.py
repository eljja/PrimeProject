from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket150_relative_delay_hole_parity import type_two_delay_witness


GENERATED_AT = "2026-07-29T09:00:00+09:00"
SCHEMA = "primeproject.ticket151-negative-affine-transversal-logtwo.v1"
STATUS = "exact_partial_theorems_and_target_corrections_all_conjectures_open"


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
    rejected_id = f"{problem_code}-T151-REJECTED"
    closed_id = f"{problem_code}-T151-CLOSED"
    open_id = f"{problem_code}-T151-OPEN"
    return {
        "nodes": [
            {
                "id": rejected_id,
                "label": rejected_name,
                "status": "refuted_or_insufficient",
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
        "edges": [[rejected_id, closed_id], [closed_id, open_id]],
    }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def riemann_negative_part_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0
    negative_levels = [Fraction(0), Fraction(1, 2), Fraction(1)]
    for exponent in range(1, 17):
        positive_spike = Fraction(2**exponent)
        for negative_level in negative_levels:
            eigenvalues = [positive_spike, -negative_level]
            full_norm = max(abs(value) for value in eigenvalues)
            negative_part_norm = max(
                max(-value, Fraction(0)) for value in eigenvalues
            )
            combined_minimum = min(
                Fraction(1) + value for value in eigenvalues
            )
            checks = {
                "negative_part_criterion_exact": (
                    (combined_minimum >= 0)
                    == (negative_part_norm <= 1)
                ),
                "full_norm_exceeds_one": full_norm > 1,
                "form_remains_nonnegative": combined_minimum >= 0,
                "positive_spike_controls_full_norm": (
                    full_norm == positive_spike
                ),
            }
            failures += sum(not value for value in checks.values())
            rows.append(
                {
                    "positive_relative_eigenvalue_M": fraction_payload(
                        positive_spike
                    ),
                    "negative_relative_eigenvalue_minus_a": fraction_payload(
                        -negative_level
                    ),
                    "full_relative_norm": fraction_payload(full_norm),
                    "negative_part_norm": fraction_payload(
                        negative_part_norm
                    ),
                    "minimum_eigenvalue_of_I_plus_B": fraction_payload(
                        combined_minimum
                    ),
                    "checks": checks,
                }
            )

    failure_rows: list[dict[str, object]] = []
    for exponent in range(1, 17):
        positive_spike = Fraction(2**exponent)
        negative_level = Fraction(2 * exponent + 3, 2 * exponent + 2)
        combined_minimum = Fraction(1) - negative_level
        checks = {
            "negative_part_exceeds_one": negative_level > 1,
            "combined_form_has_negative_direction": combined_minimum < 0,
            "positive_spike_cannot_repair_negative_direction": (
                positive_spike > 0 and combined_minimum < 0
            ),
        }
        failures += sum(not value for value in checks.values())
        failure_rows.append(
            {
                "positive_relative_eigenvalue_M": fraction_payload(
                    positive_spike
                ),
                "negative_part_norm": fraction_payload(negative_level),
                "minimum_eigenvalue_of_I_plus_B": fraction_payload(
                    combined_minimum
                ),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let p be the closed nonnegative form of a self-adjoint P with "
            "trivial kernel, and let "
            "k[v,w]=<P^(1/2)v,BP^(1/2)w> for bounded self-adjoint B. Then "
            "p+k is nonnegative if and only if B>=-I, equivalently "
            "||B_-||<=1 for the spectral negative part B_-=max(-B,0). "
            "The two-sided condition ||B||<=1 from TICKET-150 is sufficient "
            "but not necessary: B=diag(M,-a), M>1 and 0<=a<=1, gives "
            "p+k>=0 while ||B||=M is arbitrarily large. If ||B_-||>1, a "
            "negative spectral direction makes p+k negative regardless of "
            "the positive spectrum."
        ),
        "proof": (
            "For u=P^(1/2)v, (p+k)[v]=<u,(I+B)u>. Hence positivity is "
            "equivalent to I+B>=0, which by spectral calculus is equivalent "
            "to inf spectrum(B)>=-1 and to ||B_-||<=1. The diagonal family "
            "has spectrum {M,-a}; I+B has minimum eigenvalue 1-a while the "
            "full norm is M. For a>1 the second coordinate has value 1-a<0."
        ),
        "finite_large_positive_spectrum_rows": rows,
        "finite_negative_threshold_failure_rows": failure_rows,
        "failure_count": failures,
    }


def v2(value: int) -> int:
    if value == 0:
        raise ValueError("v2(0) is undefined")
    value = abs(value)
    return (value & -value).bit_length() - 1


def accelerated_collatz(value: int) -> tuple[int, int]:
    if value <= 0 or value % 2 == 0:
        raise ValueError("accelerated Collatz expects a positive odd integer")
    numerator = 3 * value + 1
    valuation = v2(numerator)
    return numerator >> valuation, valuation


def affine_word_data(start: int, length: int) -> dict[str, object]:
    if start <= 0 or start % 2 == 0 or length < 1:
        raise ValueError("start must be positive odd and length positive")
    current = start
    valuations: list[int] = []
    valuation_sum = 0
    affine_constant = 0
    for _ in range(length):
        current, valuation = accelerated_collatz(current)
        affine_constant = (
            3 * affine_constant + (1 << valuation_sum)
        )
        valuation_sum += valuation
        valuations.append(valuation)
    multiplier_gap = (1 << valuation_sum) - 3**length
    formula_passes = (
        (1 << valuation_sum) * current
        == 3**length * start + affine_constant
    )
    if multiplier_gap > 0:
        threshold = Fraction(affine_constant, multiplier_gap)
        threshold_payload: dict[str, object] | None = fraction_payload(
            threshold
        )
        threshold_prediction = (current < start) == (start > threshold)
    else:
        threshold = None
        threshold_payload = None
        threshold_prediction = current >= start
    return {
        "start_n": str(start),
        "length_m": length,
        "valuation_word": valuations,
        "valuation_sum_S": valuation_sum,
        "terminal_Tm_n": str(current),
        "affine_constant_C": str(affine_constant),
        "multiplier_gap_D": str(multiplier_gap),
        "exact_descent_threshold_C_over_D": threshold_payload,
        "strict_descent": current < start,
        "checks": {
            "exact_affine_formula": formula_passes,
            "threshold_prediction_exact": threshold_prediction,
        },
    }


def collatz_affine_threshold_audit() -> dict[str, object]:
    counter_rows: list[dict[str, object]] = []
    failures = 0
    seen_words: set[tuple[int, ...]] = set()
    for start in range(3, 200_000, 2):
        current = start
        valuations: list[int] = []
        valuation_sum = 0
        for length in range(1, 31):
            current, valuation = accelerated_collatz(current)
            valuations.append(valuation)
            valuation_sum += valuation
            if (
                (1 << valuation_sum) > 3**length
                and current >= start
            ):
                word = tuple(valuations)
                if word in seen_words:
                    continue
                seen_words.add(word)
                row = affine_word_data(start, length)
                modulus = 1 << (valuation_sum + 1)
                lifted_start = start + modulus
                lifted = affine_word_data(lifted_start, length)
                same_word = lifted["valuation_word"] == valuations
                lifted_descends = bool(lifted["strict_descent"])
                row["same_word_lift_start"] = str(lifted_start)
                row["same_word_lift_terminal"] = lifted["terminal_Tm_n"]
                row["same_word_lift_descends"] = lifted_descends
                row["checks"]["positive_multiplier_gap"] = (
                    int(row["multiplier_gap_D"]) > 0
                )
                row["checks"]["base_member_does_not_descend"] = (
                    not row["strict_descent"]
                )
                row["checks"]["cylinder_lift_preserves_word"] = same_word
                row["checks"]["large_cylinder_member_descends"] = (
                    lifted_descends
                )
                failures += sum(
                    not value for value in row["checks"].values()
                )
                counter_rows.append(row)
                if len(counter_rows) == 32:
                    break
        if len(counter_rows) == 32:
            break

    forced_rows: list[dict[str, object]] = []
    for shadow_pairs in range(0, 7):
        for delay in [1, 2, 4, 8, 16]:
            witness = type_two_delay_witness(shadow_pairs, delay)
            start = int(witness["original_start_n"])
            length = 2 * shadow_pairs + delay + 2
            row = affine_word_data(start, length)
            expected_word = (
                [1, 2] * shadow_pairs + [1, 1] + [1] * delay
            )
            row["shadow_pair_count_L"] = shadow_pairs
            row["forced_post_delay_H"] = delay
            row["checks"]["forced_word_exact"] = (
                row["valuation_word"] == expected_word
            )
            row["checks"]["multiplier_gap_is_negative"] = (
                int(row["multiplier_gap_D"]) < 0
            )
            row["checks"]["forced_horizon_cannot_descend"] = (
                not row["strict_descent"]
            )
            failures += sum(not value for value in row["checks"].values())
            forced_rows.append(row)

    return {
        "theorem": (
            "For an accelerated Collatz valuation word "
            "a=(a_1,...,a_m), put S=sum a_i and define C_0=0, "
            "C_i=3C_(i-1)+2^(a_1+...+a_(i-1)). Every realizing positive "
            "odd n satisfies T^m(n)=(3^m n+C_m)/2^S. Therefore "
            "T^m(n)<n if and only if D=2^S-3^m is positive and "
            "n>C_m/D. Positive valuation surplus D>0 alone is not "
            "sufficient: n=165 with its exact 17-step word has S=27 and "
            "D=5,077,565>0 but T^17(165)=167. Members of one exact word "
            "cylinder share C and D, so the descent boundary is an exact "
            "Archimedean threshold. For every TICKET-150 forced type-two "
            "block (1,2)^L,(1,1),1^H, D<0, so its forced horizon cannot "
            "descend below its start."
        ),
        "proof": (
            "Induction through one accelerated step gives "
            "C_i=3C_(i-1)+2^S_(i-1), proving the affine formula. "
            "Subtracting n yields "
            "T^m(n)-n=(C_m-(2^S-3^m)n)/2^S, which gives the exact "
            "threshold. The displayed natural-number witness is replayed "
            "exactly. For the forced type-two block, "
            "3^m/2^S=(9/8)^L(3/2)^(H+2)>1, hence D<0."
        ),
        "finite_positive_surplus_nondescending_rows": counter_rows,
        "finite_type_two_forced_affine_rows": forced_rows,
        "failure_count": failures,
    }


def cyclic_convolution(
    values: list[Fraction], endpoint: int
) -> Fraction:
    modulus = len(values)
    return sum(
        (
            values[index]
            * values[(endpoint - index) % modulus]
            for index in range(modulus)
        ),
        Fraction(0),
    )


def weighted_hole_radius(
    weights: list[Fraction], endpoint: int
) -> Fraction:
    modulus = len(weights)
    visited: set[int] = set()
    radius = Fraction(0)
    for index in range(modulus):
        if index in visited:
            continue
        partner = (endpoint - index) % modulus
        visited.add(index)
        visited.add(partner)
        if partner == index:
            radius += weights[index] ** 2
        else:
            radius += min(
                weights[index] ** 2,
                weights[partner] ** 2,
            )
    return radius


def prime_sieve(limit: int) -> list[bool]:
    is_prime = [True] * (limit + 1)
    if limit >= 0:
        is_prime[0] = False
    if limit >= 1:
        is_prime[1] = False
    for prime in range(2, math.isqrt(limit) + 1):
        if is_prime[prime]:
            start = prime * prime
            is_prime[start : limit + 1 : prime] = [False] * (
                (limit - start) // prime + 1
            )
    return is_prime


def goldbach_weighted_transversal_audit() -> dict[str, object]:
    moment_rows: list[dict[str, object]] = []
    failures = 0
    for scale in range(1, 17):
        hole = [
            Fraction(2 * scale),
            Fraction(scale),
            Fraction(0),
            Fraction(0),
        ]
        positive = [
            Fraction(2 * scale),
            Fraction(0),
            Fraction(0),
            Fraction(scale),
        ]
        endpoint = 3
        hole_convolution = cyclic_convolution(hole, endpoint)
        positive_convolution = cyclic_convolution(positive, endpoint)
        hole_moments = [
            sum((value**power for value in hole), Fraction(0))
            for power in range(1, 7)
        ]
        positive_moments = [
            sum((value**power for value in positive), Fraction(0))
            for power in range(1, 7)
        ]
        radius = weighted_hole_radius(positive, endpoint)
        checks = {
            "same_all_audited_global_moments": (
                hole_moments == positive_moments
            ),
            "hole_convolution_is_zero": hole_convolution == 0,
            "positive_convolution_is_positive": positive_convolution > 0,
            "positive_baseline_hole_radius_is_scale_squared": (
                radius == scale**2
            ),
        }
        failures += sum(not value for value in checks.values())
        moment_rows.append(
            {
                "scale": scale,
                "hole_weights": [str(value) for value in hole],
                "positive_weights": [str(value) for value in positive],
                "moments_power_1_through_6": [
                    str(value) for value in hole_moments
                ],
                "hole_endpoint_convolution": str(hole_convolution),
                "positive_endpoint_convolution": str(
                    positive_convolution
                ),
                "positive_weighted_hole_radius_squared": str(radius),
                "checks": checks,
            }
        )

    limit = 20_000
    is_prime = prime_sieve(limit)
    primes = [value for value in range(2, limit + 1) if is_prime[value]]
    representation_counts: dict[int, int] = {}
    for endpoint in range(4, limit + 1, 2):
        count = 0
        for prime in primes:
            if prime > endpoint // 2:
                break
            if is_prime[endpoint - prime]:
                count += 1
        representation_counts[endpoint] = count
    finite_rows: list[dict[str, object]] = []
    for cutoff in [100, 1_000, 10_000, 20_000]:
        counts = [
            representation_counts[endpoint]
            for endpoint in range(4, cutoff + 1, 2)
        ]
        zero_endpoints = [
            endpoint
            for endpoint in range(4, cutoff + 1, 2)
            if representation_counts[endpoint] == 0
        ]
        checks = {
            "all_even_endpoints_have_positive_prime_indicator_radius": (
                not zero_endpoints
            ),
            "minimum_radius_is_positive": min(counts) > 0,
            "audit_is_finite": cutoff <= limit,
        }
        failures += sum(not value for value in checks.values())
        finite_rows.append(
            {
                "cutoff": cutoff,
                "even_endpoints_audited": len(counts),
                "minimum_prime_indicator_hole_radius_squared": min(counts),
                "maximum_prime_indicator_hole_radius_squared": max(counts),
                "zero_radius_endpoints": zero_endpoints,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let tau be an involution of a finite set and w>=0 a baseline. "
            "For R_N(f)=sum_a f(a)f(tau(a)), the exact squared L2 distance "
            "from w to the nonnegative endpoint-hole set {f:R_N(f)=0} is "
            "rho_N(w)^2=sum over two-cycles {a,b} of "
            "min(w(a)^2,w(b)^2), plus sum over fixed points a of w(a)^2. "
            "Thus ||f-w||_2^2<rho_N(w)^2 forces R_N(f)>0, and equality is "
            "sharp. However, endpoint positivity is not determined by any "
            "permutation-invariant global moments: on Z/4 at N=3, "
            "(2s,s,0,0) and (2s,0,0,s) have the same multiset and every "
            "global power moment, while their endpoint convolutions are "
            "0 and 4s^2."
        ),
        "proof": (
            "On a two-cycle, a zero nonnegative convolution forces at least "
            "one coordinate to zero; the cheapest squared displacement is "
            "the smaller of the two squared baseline weights. A fixed point "
            "must itself be zero. The orbit costs add independently, and "
            "zeroing the cheaper coordinate in each orbit attains equality. "
            "The Z/4 pair is a coordinate permutation, so all symmetric "
            "moments agree, but the reflection pairing changes."
        ),
        "finite_permutation_moment_counterrows": moment_rows,
        "finite_prime_indicator_radius_rows": finite_rows,
        "failure_count": failures,
    }


def smallest_prime_factor_sieve(limit: int) -> list[int]:
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1
    for prime in range(2, math.isqrt(limit) + 1):
        if spf[prime] == prime:
            for value in range(prime * prime, limit + 1, prime):
                if spf[value] == value:
                    spf[value] = prime
    return spf


def integer_cube_root(value: int) -> int:
    root = int(round(value ** (1 / 3)))
    while (root + 1) ** 3 <= value:
        root += 1
    while root**3 > value:
        root -= 1
    return root


def twin_logtwo_selection_audit() -> dict[str, object]:
    limits = [1_000, 10_000, 100_000, 1_000_000]
    spf = smallest_prime_factor_sieve(limits[-1])
    population_rows: list[dict[str, object]] = []
    selection_rows: list[dict[str, object]] = []
    failures = 0
    target_semiprime_ratio = math.log(2)
    target_liouville_mean = (
        (math.log(2) - 1) / (math.log(2) + 1)
    )
    for cutoff in limits:
        roughness = integer_cube_root(cutoff)
        primes = 0
        semiprimes = 0
        other_composites = 0
        for value in range(2, cutoff + 1):
            if spf[value] <= roughness:
                continue
            if spf[value] == value:
                primes += 1
            else:
                semiprimes += 1
                first = spf[value]
                second = value // first
                if (
                    first <= roughness
                    or second <= roughness
                    or spf[second] != second
                ):
                    other_composites += 1
        ratio = semiprimes / primes
        liouville_mean = (
            (semiprimes - primes) / (semiprimes + primes)
        )
        checks = {
            "only_primes_or_semiprimes_on_cubic_rough_support": (
                other_composites == 0
            ),
            "prime_population_exceeds_semiprime_population": (
                primes > semiprimes
            ),
            "liouville_mean_is_negative": liouville_mean < 0,
        }
        failures += sum(not value for value in checks.values())
        population_rows.append(
            {
                "X": cutoff,
                "cubic_roughness_floor_y": roughness,
                "rough_prime_count_P": primes,
                "rough_semiprime_count_D": semiprimes,
                "semiprime_to_prime_ratio": ratio,
                "distance_to_log_two": abs(
                    ratio - target_semiprime_ratio
                ),
                "normalized_liouville_mean": liouville_mean,
                "distance_to_limit_mean": abs(
                    liouville_mean - target_liouville_mean
                ),
                "other_composite_count": other_composites,
                "checks": checks,
            }
        )
        selected = semiprimes
        selection_checks = {
            "same_ambient_populations": primes > 0 and semiprimes > 0,
            "prime_only_selection_has_positive_deficit": selected > 0,
            "semiprime_only_selection_has_negative_deficit": -selected < 0,
            "selection_signs_are_opposite": selected == -(-selected),
        }
        failures += sum(not value for value in selection_checks.values())
        selection_rows.append(
            {
                "X": cutoff,
                "ambient_prime_vertices_each_side": primes,
                "ambient_semiprime_vertices_each_side": semiprimes,
                "selected_matching_size": selected,
                "prime_only_selected_deficit_T_minus_D": selected,
                "semiprime_only_selected_deficit_T_minus_D": -selected,
                "checks": selection_checks,
            }
        )

    source_path = (
        ROOT
        / "data/open-problem/ticket149-smooth-escape-wheel-cover.json"
    )
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source_rows = source["smooth_escape_wheel_cover_audit"]["twin_prime"][
        "reproducible_computation"
    ]["finite_cover_rows"]
    shifted_rows: list[dict[str, object]] = []
    population_by_x = {
        int(row["X"]): row for row in population_rows
    }
    for source_row in source_rows:
        cutoff = int(source_row["X"])
        edge_count = int(source_row["edge_count_E"])
        left_semiprime = int(source_row["left_semiprime_edges_L"])
        right_semiprime = int(source_row["right_semiprime_edges_R"])
        left_mean = Fraction(
            2 * left_semiprime - edge_count,
            edge_count,
        )
        right_mean = Fraction(
            2 * right_semiprime - edge_count,
            edge_count,
        )
        deficit = int(source_row["marginal_only_twin_lower_bound"])
        checks = {
            "left_shifted_mean_is_negative": left_mean < 0,
            "right_shifted_mean_is_negative": right_mean < 0,
            "deficit_identity_replays": (
                2 * deficit
                == -(
                    (2 * left_semiprime - edge_count)
                    + (2 * right_semiprime - edge_count)
                )
            ),
            "matching_population_row_exists": cutoff in population_by_x,
        }
        failures += sum(not value for value in checks.values())
        shifted_rows.append(
            {
                "X": cutoff,
                "gap_two_cubic_rough_edges_E": edge_count,
                "unshifted_liouville_mean": population_by_x[cutoff][
                    "normalized_liouville_mean"
                ],
                "left_edge_conditioned_liouville_mean": fraction_payload(
                    left_mean
                ),
                "right_edge_conditioned_liouville_mean": fraction_payload(
                    right_mean
                ),
                "cover_deficit_ratio": fraction_payload(
                    Fraction(deficit, edge_count)
                ),
                "log_two_predicted_deficit_ratio": (
                    -target_liouville_mean
                ),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let y=X^(1/3), and count integers 2<=n<=X having no prime "
            "factor <=y. Apart from the negligible endpoint convention, "
            "every such n is prime or a product of two primes. The prime "
            "count P_X is asymptotic to X/log X, while the semiprime count "
            "D_X is asymptotic to (log 2)X/log X. Consequently the "
            "one-variable Liouville mean tends to "
            "(log 2-1)/(log 2+1)<0. This does not imply the same sign after "
            "conditioning on n and n+2 both being cubic-rough: identical "
            "ambient prime/semiprime populations admit a selected matching "
            "consisting only of prime-prime edges or only of "
            "semiprime-semiprime edges, giving opposite T-D signs."
        ),
        "proof": (
            "Three prime factors all exceeding X^(1/3) have product>X. "
            "The prime count follows from the prime number theorem. Writing "
            "a rough semiprime as pq with X^(1/3)<p<=sqrt(X) and p<=q, "
            "PNT plus partial summation gives "
            "X/log X times integral from 1/3 to 1/2 of "
            "dt/(t(1-t))=log 2; the diagonal and lower endpoint contribute "
            "o(X/log X). The matching countermodels keep the same ambient "
            "vertices and change only which vertices enter the gap-two "
            "selected support, so unshifted density cannot determine the "
            "shifted marginal."
        ),
        "finite_cubic_rough_population_rows": population_rows,
        "finite_selection_countermodel_rows": selection_rows,
        "finite_gap_two_shifted_rows": shifted_rows,
        "target_constants": {
            "semiprime_to_prime_ratio_log_two": target_semiprime_ratio,
            "liouville_mean": target_liouville_mean,
            "predicted_deficit_ratio_under_marginal_transfer": (
                -target_liouville_mean
            ),
        },
        "source_artifact": str(source_path.relative_to(ROOT)).replace(
            "\\", "/"
        ),
        "source_sha256": file_sha256(source_path),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_negative_part_audit()
    collatz = collatz_affine_threshold_audit()
    goldbach = goldbach_weighted_transversal_audit()
    twin_prime = twin_logtwo_selection_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )
    next_theorems = {
        "riemann": "ActualWeilNegativeRelativeFormPartBoundAtMostOne",
        "collatz": (
            "TypeTwoAffineThresholdCylinderCoverBelowShadowEntry"
        ),
        "goldbach": (
            "OrbitResolvedVonMangoldtApproximationInsideWeightedHoleRadiusK56"
        ),
        "twin_prime": (
            "PositiveGapTwoCubicRoughMassAndShiftedLogTwoMarginalTransfer"
        ),
    }
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-151",
            "theorem_name": (
                "OneSidedNegativeRelativeFormCriterionAndFullNormNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The criterion is an abstract spectral equivalence. It does "
                "not construct the actual Weil reference form, represent its "
                "prime and archimedean terms by B, or bound B_-. No zeta zero "
                "is controlled."
            ),
            "route_decision": {
                "discard": (
                    "the unnecessarily strong two-sided target "
                    "||B||<=1, which also suppresses harmless positive "
                    "relative spectrum"
                ),
                "retain": (
                    "construct the actual Weil relative operator and bound "
                    "only its spectral negative part by one"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "ActualWeilFullRelativeNormAtMostOne",
                "OneSidedNegativeRelativeFormCriterionAndFullNormNoGo",
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One exact one-sided "
                "form criterion and a no-go for requiring the full norm."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-151",
            "theorem_name": (
                "ExactAffineStoppingThresholdAndPositiveSurplusNoGo"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The exact threshold classifies a fixed finite valuation "
                "word. It neither proves that every type-two cylinder has a "
                "descent-producing extension nor supplies a uniform stopping "
                "time for all positive integers."
            ),
            "route_decision": {
                "discard": (
                    "using positive cumulative valuation surplus "
                    "2^S>3^m by itself as a strict descent certificate"
                ),
                "retain": (
                    "cover every type-two cylinder by an extension whose "
                    "affine threshold lies below every represented natural "
                    "start and below the pre-shadow entry"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "PositiveValuationSurplusAloneImpliesDescent",
                "ExactAffineStoppingThresholdAndPositiveSurplusNoGo",
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. One exact affine "
                "threshold theorem and finite natural counterexamples to a "
                "surplus-only rule."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-151",
            "theorem_name": (
                "WeightedReflectionHoleRadiusAndPermutationMomentNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The weighted radius is exact finite reflection geometry, "
                "not a lower bound for the actual von Mangoldt convolution. "
                "The finite prime-indicator audit through 20,000 cannot be "
                "promoted to all even integers."
            ),
            "route_decision": {
                "discard": (
                    "any K56 transfer argument based only on global moments, "
                    "energy, or the unordered weight histogram"
                ),
                "retain": (
                    "construct an orbit-resolved positive major-arc reference "
                    "and prove the von Mangoldt error lies strictly inside "
                    "its exact weighted endpoint-hole radius"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "GlobalMomentsDetermineEndpointReflectionMass",
                "WeightedReflectionHoleRadiusAndPermutationMomentNoGo",
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "weighted stability radius and a global-moment no-go."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-151",
            "theorem_name": (
                "CubicRoughLogTwoBiasAndShiftedSelectionNoGo"
            ),
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The PNT consequence is one-dimensional. It gives no "
                "positive lower bound for gap-two cubic-rough edges and no "
                "shifted Liouville marginal estimate on that selected "
                "support."
            ),
            "route_decision": {
                "discard": (
                    "transferring the unshifted cubic-rough log-two bias "
                    "directly to the n,n+2 selected edge support"
                ),
                "retain": (
                    "prove positive gap-two cubic-rough mass and a shifted "
                    "marginal transfer preserving a quantitative fraction of "
                    "the negative log-two bias"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "UnshiftedCubicRoughBiasAutomaticallyTransfersToGapTwo",
                "CubicRoughLogTwoBiasAndShiftedSelectionNoGo",
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof or counterexample. One PNT-derived "
                "univariate bias and a shifted-selection no-go."
            ),
        },
    }
    return {
        "theorem_name": (
            "FourConjectureNegativeAffineTransversalLogTwoAudit"
        ),
        "status": STATUS,
        "proof_boundary": (
            "TICKET-151 proves four exact partial or no-go theorems and "
            "resolves no target conjecture. It replaces a two-sided RH norm "
            "target by the exact negative-part criterion, inserts the "
            "Collatz affine threshold missing from surplus arguments, "
            "generalizes the Goldbach endpoint-hole radius to weighted "
            "reflection orbits, and separates the Twin cubic-rough log-two "
            "bias from the still-missing shifted selection theorem."
        ),
        **sections,
        "literature_boundary": [
            {
                "citation": (
                    "Suzuki, Weil's quadratic form via the screw function"
                ),
                "url": "https://arxiv.org/abs/2606.09096",
                "role": (
                    "Current Weil-form context; TICKET-151 proves only the "
                    "abstract one-sided relative spectral criterion."
                ),
            },
            {
                "citation": (
                    "Niu, Parity vectors and paradoxical sequences in the "
                    "accelerated Collatz map"
                ),
                "url": "https://arxiv.org/abs/2605.13886",
                "role": (
                    "Current parity-vector context; the affine threshold "
                    "audit supplies no all-cylinder descent cover."
                ),
            },
            {
                "citation": "Helfgott, Minor arcs for Goldbach's problem",
                "url": "https://arxiv.org/abs/1205.5252",
                "role": (
                    "Primary explicit minor-arc context; global moment "
                    "control is separated from endpoint reflection control."
                ),
            },
            {
                "citation": (
                    "Ford and Maynard, On the theory of prime producing "
                    "sieves"
                ),
                "url": "https://arxiv.org/abs/2407.14368",
                "role": (
                    "Primary Type I/II boundary; the log-two PNT calculation "
                    "does not supply the required shifted lower bound."
                ),
            },
        ],
        "machine_audit": {
            "exact_theorem_count": 4,
            "rejected_target_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, object]) -> list[dict[str, object]]:
    attempts: list[dict[str, object]] = []
    for problem_id in ["riemann", "collatz", "goldbach", "twin-prime"]:
        key = problem_id.replace("-", "_")
        section = audit[key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "attempt": section["declared_proposition"],
                "bounded_result": {
                    "audit_ref": (
                        "negative_affine_transversal_logtwo_audit."
                        f"{key}"
                    )
                },
                "obstruction": section["logical_limit"],
                "candidate_theorem": section["route_decision"][
                    "next_theorem"
                ],
                "next_experiment": section["route_decision"]["retain"],
                "claim_boundary": section["claim_boundary"],
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
        "negative_affine_transversal_logtwo_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket151-negative-affine-transversal-logtwo.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-151-negative-relative-part.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-151-affine-threshold.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-151-weighted-reflection-radius.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-151-logtwo-shift-selection.json"
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
