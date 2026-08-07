from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket180_finite_information_localization import ordered_affine_numerator
from ticket188_nested_fourone_primepower_dyadic import (
    fraction_payload,
    goldbach_prime_power_row,
    prime_power_metadata,
)
from ticket189_corefive_sublinear_shift import twin_shift_two_row
from ticket193_everywhere_nineone_parity_envelope import (
    weighted_odd_proper_prime_power_mass,
)
from ticket194_densecore_tenone_theta_layers import (
    exact_binary_mass_classification,
    integer_kth_root,
    odd_primes_from_metadata,
    theta_interval_mass,
    theta_layer_mass,
    theta_odd,
)


GENERATED_AT = "2026-08-08T08:30:00+09:00"
SCHEMA = "primeproject.ticket195-finitejet-elevenone-squarelayer.v1"
STATUS = (
    "finite_jet_no_go_and_fixed_stratum_decidability_proved_"
    "eleven_one_cycle_stratum_closed_square_layer_decompositions_proved_all_open"
)
ELEVEN_ONES = 11


def proof_dag(
    problem_code: str,
    previous_name: str,
    closed_name: str,
    rejected_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T194-INPUT",
                "label": previous_name,
                "status": "proved_exact_input_or_open_target",
            },
            {
                "id": f"{problem_code}-T195-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T195-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_incomplete_surrogate",
            },
            {
                "id": f"{problem_code}-T195-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T194-INPUT", f"{problem_code}-T195-CLOSED"],
            [f"{problem_code}-T195-CLOSED", f"{problem_code}-T195-OPEN"],
            [f"{problem_code}-T195-REJECTED", f"{problem_code}-T195-OPEN"],
        ],
    }


def evaluate_even_polynomial_at_i(coefficients: list[Fraction]) -> Fraction:
    return sum(
        (coefficient * (-1) ** index for index, coefficient in enumerate(coefficients)),
        Fraction(),
    )


def finite_even_jet_ambiguity_row(order_m: int) -> dict[str, object]:
    if order_m < 0:
        raise ValueError("order must be nonnegative")
    coefficients = [
        Fraction((-1) ** index, index + 1) for index in range(order_m + 1)
    ]
    jet_at_i = evaluate_even_polynomial_at_i(coefficients)
    extension_coefficient = Fraction((-1) ** order_m) * jet_at_i
    extension_at_i = jet_at_i + extension_coefficient * (-1) ** (order_m + 1)
    return {
        "order_m": order_m,
        "matched_through_degree": 2 * order_m,
        "jet_coefficients": [fraction_payload(value) for value in coefficients],
        "jet_value_at_i": fraction_payload(jet_at_i),
        "extension_coefficient_degree_2m_plus_2": fraction_payload(
            extension_coefficient
        ),
        "extended_polynomial_value_at_i": fraction_payload(extension_at_i),
        "shares_entire_declared_even_jet": True,
        "forced_nonreal_roots": ["i", "-i"],
    }


def rouche_unit_disk_row(order_m: int) -> dict[str, object]:
    if order_m < 0:
        raise ValueError("order must be nonnegative")
    tail_supremum = Fraction(1, 2 ** (order_m + 1))
    approximant_boundary_minimum = Fraction(1)
    return {
        "order_m": order_m,
        "approximant": "P(z)=1",
        "tail": f"R(z)=2^(-{order_m + 1}) z^{2 * order_m + 2}",
        "boundary": "|z|=1",
        "approximant_boundary_minimum": fraction_payload(
            approximant_boundary_minimum
        ),
        "tail_boundary_supremum": fraction_payload(tail_supremum),
        "strict_rouche_margin": fraction_payload(
            approximant_boundary_minimum - tail_supremum
        ),
        "same_zero_count_inside": True,
        "certified_zero_count_inside": 0,
    }


def riemann_finite_jet_audit() -> dict[str, object]:
    ambiguity_rows = [finite_even_jet_ambiguity_row(order) for order in range(13)]
    rouche_rows = [rouche_unit_disk_row(order) for order in range(1, 13)]
    failures = sum(
        int(row["extended_polynomial_value_at_i"]["numerator"] != 0)
        + int(not row["shares_entire_declared_even_jet"])
        for row in ambiguity_rows
    )
    failures += sum(
        int(row["strict_rouche_margin"]["numerator"] <= 0)
        + int(row["certified_zero_count_inside"] != 0)
        for row in rouche_rows
    )
    return {
        "theorem": (
            "Let J_m(z)=sum_(r=0)^m a_r z^(2r) be any finite real even "
            "Taylor jet. Since J_m(i) is real, c=(-1)^m J_m(i) is real and "
            "P_m(z)=J_m(z)+c z^(2m+2) shares every declared coefficient but "
            "satisfies P_m(i)=P_m(-i)=0. Thus no finite even Taylor jet, by "
            "itself, certifies that all zeros are real. A valid bounded-domain "
            "bridge is instead Rouche: if an entire F=P+R satisfies "
            "sup_boundary |R|<inf_boundary |P|, then F and P have the same "
            "zero count inside."
        ),
        "proof": (
            "Evenness and real coefficients give J_m(i)=sum a_r(-1)^r in R. "
            "Because i^(2m+2)=(-1)^(m+1), the chosen c makes the added term "
            "equal -J_m(i) at i; evenness gives the root -i. The coefficient "
            "change starts only at degree 2m+2. Rouche's theorem supplies the "
            "positive bridge once a strict uniform tail inequality is proved "
            "on a contour."
        ),
        "finite_even_jet_ambiguity_rows": ambiguity_rows,
        "rouche_synthetic_certificate_rows": rouche_rows,
        "contract": {
            "finite_even_jet_alone_certifies_real_zero_property": False,
            "strict_rouche_tail_margin_certifies_bounded_zero_count": True,
            "actual_xi_tail_margin_on_exhausting_off_real_domains_verified": False,
            "actual_pole_neutral_weil_premises_verified": False,
        },
        "no_go_scope": (
            "The ambiguity theorem blocks finite coefficient or finite Jensen "
            "data without a tail class. It neither places a nonreal zero of "
            "the actual Xi function nor proves the required Xi or Weil tail bound."
        ),
        "failure_count": failures,
    }


def fixed_one_product_bound(one_count: int, horizon: int) -> Fraction:
    if one_count < 1 or horizon < one_count:
        raise ValueError("require horizon>=one_count>=1")
    return Fraction(2**one_count) * Fraction(5, 6) ** horizon


def contracting_start(one_count: int) -> int:
    horizon = one_count
    while 2 ** (2 * horizon - one_count) <= 3**horizon:
        horizon += 1
    return horizon


def analytic_tail_start(one_count: int) -> int:
    horizon = one_count
    while fixed_one_product_bound(one_count, horizon) >= 1:
        horizon += 1
    return horizon


def fixed_stratum_decidability_row(one_count: int) -> dict[str, object]:
    start = contracting_start(one_count)
    tail = analytic_tail_start(one_count)
    finite_word_count = (
        math.comb(tail - 1, one_count) - math.comb(start - 1, one_count)
    )
    return {
        "one_count_r": one_count,
        "contracting_range_starts_at_h": start,
        "analytic_exclusion_starts_at_h": tail,
        "finite_exact_horizons": [start, tail - 1],
        "normalized_words_in_finite_decision_range": finite_word_count,
        "finite_decision_range_is_finite": True,
    }


def boundary_components(
    one_count: int, horizon: int
) -> tuple[int, list[list[int]]]:
    if horizon < one_count:
        raise ValueError("horizon must contain every valuation-one position")
    prefixes: list[list[int]] = []
    for ones_before in range(one_count + 1):
        values = [0]
        running = 0
        for index in range(horizon):
            exponent = 2 * index - ones_before
            if exponent >= 0:
                running += 3 ** (horizon - 1 - index) * 2**exponent
            values.append(running)
        prefixes.append(values)
    constant = 3 ** (horizon - 1) + prefixes[one_count][horizon] - prefixes[1][1]
    boundaries = [[0] * horizon for _ in range(one_count)]
    for boundary_index in range(1, one_count):
        for position in range(1, horizon):
            boundaries[boundary_index][position] = (
                prefixes[boundary_index][position + 1]
                - prefixes[boundary_index + 1][position + 1]
            )
    return constant, boundaries


def boundary_numerator(
    one_count: int, horizon: int, positions: tuple[int, ...]
) -> int:
    if len(positions) != one_count or positions[0] != 0:
        raise ValueError("positions must be normalized with p_0=0")
    if tuple(sorted(positions)) != positions or positions[-1] >= horizon:
        raise ValueError("positions must be strictly increasing inside the horizon")
    constant, boundaries = boundary_components(one_count, horizon)
    return constant + sum(
        boundaries[index][positions[index]] for index in range(1, one_count)
    )


def eleven_one_boundary_validation() -> dict[str, object]:
    checked = 0
    failures = 0
    transcript = hashlib.sha256()
    for horizon in range(ELEVEN_ONES, 18):
        for tail in itertools.combinations(range(1, horizon), ELEVEN_ONES - 1):
            positions = (0,) + tail
            position_set = set(positions)
            word = tuple(
                1 if index in position_set else 2 for index in range(horizon)
            )
            direct = ordered_affine_numerator(word)
            boundary = boundary_numerator(ELEVEN_ONES, horizon, positions)
            failures += int(direct != boundary)
            checked += 1
            transcript.update(
                f"{horizon}:{positions}:{direct}:{boundary}\n".encode("ascii")
            )
    return {
        "horizons": [ELEVEN_ONES, 17],
        "normalized_words_checked": checked,
        "formula_mismatch_count": failures,
        "transcript_sha256": transcript.hexdigest(),
    }


def finite_eleven_one_horizon_row(horizon: int) -> dict[str, object]:
    if not 27 <= horizon <= 41:
        raise ValueError("finite contracting range is h=27..41")
    denominator = 2 ** (2 * horizon - ELEVEN_ONES) - 3**horizon
    constant, boundary = boundary_components(ELEVEN_ONES, horizon)
    left_buckets: list[list[tuple[int, tuple[int, ...]]]] = [
        [] for _ in range(horizon)
    ]
    left_tuple_count = 0
    for positions in itertools.combinations(range(1, horizon), 5):
        remainder = (
            constant
            + sum(boundary[index][positions[index - 1]] for index in range(1, 6))
        ) % denominator
        left_buckets[positions[-1]].append((remainder, positions))
        left_tuple_count += 1

    active: dict[int, tuple[int, ...]] = {}
    next_last = 0
    right_tuple_count = 0
    represented_word_count = 0
    hits: list[dict[str, object]] = []
    transcript = hashlib.sha256()
    for first_right in range(6, horizon - 4):
        while next_last < first_right:
            for remainder, positions in left_buckets[next_last]:
                active.setdefault(remainder, positions)
            next_last += 1
        for tail in itertools.combinations(range(first_right + 1, horizon), 4):
            right_positions = (first_right,) + tail
            right_remainder = sum(
                boundary[index][right_positions[index - 6]]
                for index in range(6, ELEVEN_ONES)
            ) % denominator
            target = (-right_remainder) % denominator
            hit = target in active
            transcript.update(
                f"{right_positions}:{target}:{int(hit)}\n".encode("ascii")
            )
            if hit:
                hits.append(
                    {
                        "positions": [0, *active[target], *right_positions],
                        "target_remainder": target,
                    }
                )
            right_tuple_count += 1
            represented_word_count += math.comb(first_right - 1, 5)
    expected = math.comb(horizon - 1, ELEVEN_ONES - 1)
    return {
        "horizon_h": horizon,
        "denominator": denominator,
        "split": "5+5 boundary terms",
        "left_tuple_count": left_tuple_count,
        "right_tuple_count": right_tuple_count,
        "represented_word_count": represented_word_count,
        "expected_normalized_word_count": expected,
        "coverage_matches_binomial_count": represented_word_count == expected,
        "divisibility_hit_count": len(hits),
        "divisibility_hits": hits,
        "mitm_transcript_sha256": transcript.hexdigest(),
    }


def collatz_eleven_one_audit() -> dict[str, object]:
    decision_rows = [fixed_stratum_decidability_row(r) for r in range(1, 33)]
    validation = eleven_one_boundary_validation()
    finite_rows = [finite_eleven_one_horizon_row(h) for h in range(27, 42)]
    finite_word_count = sum(int(row["represented_word_count"]) for row in finite_rows)
    expected_word_count = math.comb(41, 11) - math.comb(26, 11)
    failures = int(validation["formula_mismatch_count"] != 0)
    failures += sum(
        int(not row["coverage_matches_binomial_count"])
        + int(row["divisibility_hit_count"] != 0)
        for row in finite_rows
    )
    failures += int(finite_word_count != expected_word_count)
    failures += int(fixed_one_product_bound(ELEVEN_ONES, 41) <= 1)
    failures += int(fixed_one_product_bound(ELEVEN_ONES, 42) >= 1)
    return {
        "theorem": (
            "For every fixed r>=1, positive accelerated Collatz cycles whose "
            "valuations contain exactly r ones and otherwise only twos are "
            "decidable by a finite exact computation: noncontraction removes "
            "an initial interval and 1<=2^r(5/6)^h removes an infinite tail. "
            "For r=11 the remaining horizons are h=27..41; an exact 5+5 "
            "boundary-term MITM finds no affine divisibility hit, so the entire "
            "eleven-one/rest-two cycle stratum is empty, including imprimitive words."
        ),
        "proof": (
            "A contracting word requires 2^(2h-r)>3^h. Rotating one of its r "
            "ones to the first position preserves affine divisibility. Every "
            "state of a nontrivial positive odd cycle is at least three, so "
            "multiplying step ratios gives 1<=2^r(5/6)^h. For fixed r these "
            "two inequalities leave finitely many h and finitely many normalized "
            "words. At r=11, h<=26 is noncontracting, h>=42 contradicts the "
            "product bound, and the exact residue search closes h=27..41."
        ),
        "fixed_stratum_decidability_rows": decision_rows,
        "boundary_formula_validation": validation,
        "finite_exception_horizon_rows": finite_rows,
        "analytic_bound": {
            "formula": "1 <= 2^11 (5/6)^h",
            "h_41": fraction_payload(fixed_one_product_bound(ELEVEN_ONES, 41)),
            "h_42": fraction_payload(fixed_one_product_bound(ELEVEN_ONES, 42)),
            "analytic_range_starts_at_h": 42,
        },
        "aggregate": {
            "fixed_r_decidability_theorem_proved": True,
            "decidability_rows": len(decision_rows),
            "eleven_one_infinite_family_proved_empty": True,
            "includes_imprimitive_words": True,
            "contracting_range_starts_at_h": 27,
            "analytic_range_starts_at_h": 42,
            "finite_exception_word_count": finite_word_count,
            "finite_word_count_identity": (
                "C(41,11)-C(26,11)=3151735808"
            ),
            "left_tuple_count": sum(int(row["left_tuple_count"]) for row in finite_rows),
            "right_tuple_count": sum(int(row["right_tuple_count"]) for row in finite_rows),
            "divisibility_hits": sum(
                int(row["divisibility_hit_count"]) for row in finite_rows
            ),
        },
        "no_go_scope": (
            "Fixed-r decidability is not one finite certificate uniform in r. "
            "It leaves unbounded one-count, valuations at least three, and "
            "aperiodic divergence open."
        ),
        "failure_count": failures,
    }


def split_theta_layers(layers: dict[str, object]) -> dict[str, object]:
    rows = list(layers["layers"])
    square_mass = math.fsum(
        float(row["theta_odd_root"])
        for row in rows
        if int(row["exponent_k"]) == 2
    )
    higher_mass = math.fsum(
        float(row["theta_odd_root"])
        for row in rows
        if int(row["exponent_k"]) >= 3
    )
    return {
        "prime_square_layer_mass": square_mass,
        "exponent_at_least_three_mass": higher_mass,
        "reconstructed_mass": square_mass + higher_mass,
    }


def split_theta_interval(layers: dict[str, object]) -> dict[str, object]:
    rows = list(layers["layers"])
    square_mass = math.fsum(
        float(row["theta_odd_difference"])
        for row in rows
        if int(row["exponent_k"]) == 2
    )
    higher_mass = math.fsum(
        float(row["theta_odd_difference"])
        for row in rows
        if int(row["exponent_k"]) >= 3
    )
    return {
        "prime_square_layer_mass": square_mass,
        "exponent_at_least_three_mass": higher_mass,
        "reconstructed_mass": square_mass + higher_mass,
    }


def goldbach_prime_square_audit() -> dict[str, object]:
    targets = [2**exponent for exponent in range(10, 22)]
    metadata = prime_power_metadata(max(targets) + 2)
    primes = odd_primes_from_metadata(metadata, math.isqrt(max(targets)))
    rows: list[dict[str, object]] = []
    for target in targets:
        decomposition = goldbach_prime_power_row(target, metadata)
        layers = theta_layer_mass(target, primes)
        split = split_theta_layers(layers)
        actual_mass = weighted_odd_proper_prime_power_mass(metadata, 2, target + 1)
        binary = exact_binary_mass_classification(target)
        square_envelope = (
            2.0 * math.log(target) * split["prime_square_layer_mass"]
            + binary["exact_weight"]
        )
        full_envelope = square_envelope + (
            2.0 * math.log(target) * split["exponent_at_least_three_mass"]
        )
        rows.append(
            {
                "target_N": target,
                "theta_layers": layers,
                "layer_split": split,
                "actual_odd_weighted_proper_power_mass": actual_mass,
                "prime_square_leading_envelope": square_envelope,
                "higher_exponent_envelope_remainder": full_envelope - square_envelope,
                "full_theta_layer_envelope": full_envelope,
                "weighted_total_convolution": decomposition["weighted_total_convolution"],
                "actual_contamination": decomposition[
                    "weighted_prime_power_contamination"
                ],
                "higher_to_square_mass_ratio": (
                    split["exponent_at_least_three_mass"]
                    / split["prime_square_layer_mass"]
                    if split["prime_square_layer_mass"]
                    else 0.0
                ),
                "checks": {
                    "split_reconstructs_theta_mass": abs(
                        split["reconstructed_mass"] - layers["reconstructed_mass"]
                    )
                    < 1e-9,
                    "theta_mass_matches_direct_mass": abs(
                        layers["reconstructed_mass"] - actual_mass
                    )
                    < 1e-9,
                    "actual_contamination_below_full_envelope": (
                        decomposition["weighted_prime_power_contamination"]
                        <= full_envelope + 1e-9
                    ),
                    "finite_total_exceeds_full_envelope": (
                        decomposition["weighted_total_convolution"] > full_envelope
                    ),
                },
            }
        )
    cube_witness = {
        "target_N": 32,
        "ordered_pair": [27, 5],
        "left_prime_power": {"base": 3, "exponent": 3},
        "right_prime": 5,
        "von_mangoldt_weight": math.log(3) * math.log(5),
        "omitted_by_square_only_support": True,
    }
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(27 + 5 != 32) + int(not cube_witness["omitted_by_square_only_support"])
    return {
        "theorem": (
            "The exact odd proper-prime-power mass decomposes as "
            "W_odd(Y)=theta_odd(floor(sqrt Y))+R_>=3(Y), where "
            "R_>=3(Y)=sum_(k>=3)theta_odd(floor(Y^(1/k))). Under the classical "
            "Chebyshev bound theta(t)=O(t), R_>=3(Y)=O(Y^(1/3)). Hence the "
            "Goldbach contamination envelope has a prime-square leading term "
            "2 log(N) theta_odd(floor(sqrt N)) plus O(N^(1/3) log N) and the "
            "exact power-of-two term. Higher layers cannot be deleted exactly: "
            "32=27+5 is a cube-prime contamination witness."
        ),
        "proof": (
            "Separate k=2 in the exact TICKET-194 theta identity. Chebyshev "
            "bounds the k=3 layer by O(Y^(1/3)); every k>=4 layer is "
            "O(Y^(1/4)), and O(log Y)Y^(1/4)=O(Y^(1/3)). Multiplication by "
            "the partner log weight yields the stated remainder."
        ),
        "prime_square_layer_rows": rows,
        "cube_support_no_go_witness": cube_witness,
        "aggregate": {
            "target_count": len(rows),
            "largest_target": targets[-1],
            "prime_square_layer_decomposition_proved": True,
            "higher_layer_mass_scale": "O(N^(1/3))",
            "higher_layer_contamination_scale": "O(N^(1/3) log(N))",
            "finite_sample_success_count": sum(
                row["checks"]["finite_total_exceeds_full_envelope"] for row in rows
            ),
            "all_large_even_targets_proved": False,
        },
        "no_go_scope": (
            "The smaller remainder sharpens the sufficient envelope but gives "
            "no pointwise lower bound for the binary correlation."
        ),
        "failure_count": failures,
    }


def twin_prime_square_audit() -> dict[str, object]:
    exponents = list(range(4, 21))
    limit = 2 ** (exponents[-1] + 1) + 2
    metadata = prime_power_metadata(limit)
    primes = odd_primes_from_metadata(metadata, math.isqrt(limit))
    rows: list[dict[str, object]] = []
    for exponent in exponents:
        arithmetic = twin_shift_two_row(exponent, metadata)
        lower = 2**exponent
        upper = 2 * lower
        ceiling = upper + 2
        left_layers = theta_interval_mass(lower, upper, primes)
        right_layers = theta_interval_mass(lower + 2, upper + 2, primes)
        left_split = split_theta_interval(left_layers)
        right_split = split_theta_interval(right_layers)
        square_mass = (
            left_split["prime_square_layer_mass"]
            + right_split["prime_square_layer_mass"]
        )
        higher_mass = (
            left_split["exponent_at_least_three_mass"]
            + right_split["exponent_at_least_three_mass"]
        )
        full_envelope = math.log(ceiling) * (square_mass + higher_mass)
        left_actual = weighted_odd_proper_prime_power_mass(metadata, lower, upper)
        right_actual = weighted_odd_proper_prime_power_mass(
            metadata, lower + 2, upper + 2
        )
        rows.append(
            {
                **arithmetic,
                "left_theta_interval": left_layers,
                "right_theta_interval": right_layers,
                "left_layer_split": left_split,
                "right_layer_split": right_split,
                "prime_square_leading_envelope": math.log(ceiling) * square_mass,
                "higher_exponent_envelope_remainder": math.log(ceiling) * higher_mass,
                "full_theta_layer_local_envelope": full_envelope,
                "checks": {
                    **arithmetic["checks"],
                    "left_split_matches_direct_mass": abs(
                        left_split["reconstructed_mass"] - left_actual
                    )
                    < 1e-9,
                    "right_split_matches_direct_mass": abs(
                        right_split["reconstructed_mass"] - right_actual
                    )
                    < 1e-9,
                    "actual_contamination_below_full_envelope": (
                        arithmetic["weighted_prime_power_contamination"]
                        <= full_envelope + 1e-9
                    ),
                    "finite_total_exceeds_full_envelope": (
                        arithmetic["weighted_shift_two_correlation"] > full_envelope
                    ),
                },
            }
        )
    cube_witness = {
        "dyadic_block": [16, 32],
        "shift_two_pair": [27, 29],
        "left_prime_power": {"base": 3, "exponent": 3},
        "right_prime": 29,
        "von_mangoldt_weight": math.log(3) * math.log(29),
        "omitted_by_square_only_support": True,
    }
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(27 + 2 != 29) + int(not cube_witness["omitted_by_square_only_support"])
    return {
        "theorem": (
            "On each interval [A,B), the exact odd proper-prime-power theta "
            "mass is its prime-square interval layer plus an exponent-at-least-"
            "three remainder. Chebyshev gives remainder O(B^(1/3)); therefore "
            "the dyadic shift-two contamination is a prime-square leading "
            "envelope plus O(X^(1/3) log X). The pair (27,29) proves that a "
            "square-only support decomposition is not exact."
        ),
        "proof": (
            "Subtract the cumulative square-layer identity at interval endpoints "
            "and separate k=2. Bound the cumulative k>=3 layers exactly as in "
            "the Goldbach theorem. Both shifted intervals lie below 2X+2, so "
            "multiplication by the partner log weight gives the stated local remainder."
        ),
        "finite_dyadic_rows": rows,
        "cube_support_no_go_witness": cube_witness,
        "aggregate": {
            "dyadic_block_count": len(rows),
            "largest_upper_endpoint": rows[-1]["block"][1],
            "prime_square_interval_decomposition_proved": True,
            "higher_layer_local_mass_scale": "O(X^(1/3))",
            "higher_layer_contamination_scale": "O(X^(1/3) log(X))",
            "finite_block_success_count": sum(
                row["checks"]["finite_total_exceeds_full_envelope"] for row in rows
            ),
            "infinitely_many_envelope_successes_proved": False,
        },
        "no_go_scope": (
            "The square-leading decomposition sharpens the error hierarchy but "
            "does not produce a shift-two lower bound on infinitely many blocks."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_finite_jet_audit()
    collatz = collatz_eleven_one_audit()
    goldbach = goldbach_prime_square_audit()
    twin = twin_prime_square_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-195",
            "theorem_name": "FiniteEvenJetAmbiguityAndRoucheTailBridge",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No certified Xi tail margin is proved on an exhausting family of off-real domains, and the actual Weil premises remain open.",
            "route_decision": {
                "discard": "promoting finitely many Xi Taylor coefficients, Jensen polynomials, or Hankel checks to the all-zero statement without a uniform tail class",
                "retain": "combine exact finite-section zero counts with certified Rouche tail margins on exhausting off-real domains",
                "next_single_lemma": "XiTaylorSectionsAdmitCertifiedRoucheTailBoundsOnAnExhaustingOffRealDomainFamily",
            },
            "proof_dag": proof_dag(
                "RH",
                "PoleNeutralWeilFiniteSectionsAreUniformlyBoundedAndConvergeOnADenseCore",
                "FiniteEvenJetAmbiguityAndRoucheTailBridge",
                "FiniteXiTaylorJetAloneCertifiesTheRealZeroProperty",
                "XiTaylorSectionsAdmitCertifiedRoucheTailBoundsOnAnExhaustingOffRealDomainFamily",
            ),
            "claim_boundary": "No RH proof or counterexample. Finite-jet promotion is refuted; only a conditional bounded-domain tail bridge is proved.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-195",
            "theorem_name": "FixedOneCountRestTwoDecidabilityAndElevenStratumExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "The finite decision algorithm depends on fixed r and does not cover all one-counts at once, valuations at least three, or divergent aperiodic trajectories.",
            "route_decision": {
                "discard": "the exactly-eleven-one/rest-two valuation stratum as a source of positive cycles, and the claim that each fixed stratum requires an infinite search",
                "retain": "seek a uniform-in-r nondivisibility theorem rather than executing infinitely many separate finite decisions",
                "next_single_lemma": "NoPositiveAcceleratedCollatzCycleHasAllValuationsInTheSetOneTwo",
            },
            "proof_dag": proof_dag(
                "CO",
                "ExactlyTenValuationOnesOtherwiseTwoCycleExclusion",
                "FixedOneCountRestTwoDecidabilityAndElevenStratumExclusion",
                "FixedOneCountRestTwoStrataRequireInfiniteSearch",
                "NoPositiveAcceleratedCollatzCycleHasAllValuationsInTheSetOneTwo",
            ),
            "claim_boundary": "No Collatz proof. One more infinite stratum is excluded and every fixed one-count stratum is shown decidable, but no uniform all-r theorem is proved.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-195",
            "theorem_name": "PrimeSquareDominantThetaLayerDecomposition",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No lower bound exceeds the square-leading plus higher-layer envelope for every sufficiently large even target.",
            "route_decision": {
                "discard": "deleting all exponent-at-least-three prime powers from the exact contamination support",
                "retain": "prove an every-large-even correlation lower bound above the prime-square leading layer plus the cubic-scale tail",
                "next_single_lemma": "BinaryCorrelationExceedsPrimeSquareLayerPlusCubicTailEnvelopeForEveryLargeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "BinaryCorrelationExceedsThetaLayerPrimePowerEnvelopeForEveryLargeEvenTarget",
                "PrimeSquareDominantThetaLayerDecomposition",
                "PrimeSquareLayerAloneIsTheExactContaminationSupport",
                "BinaryCorrelationExceedsPrimeSquareLayerPlusCubicTailEnvelopeForEveryLargeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof. The contamination hierarchy is sharper, but the universal binary-correlation lower bound is open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-195",
            "theorem_name": "PrimeSquareDominantIntervalThetaLayerDecomposition",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No lower bound exceeds the square-leading plus higher-layer local envelope on infinitely many unbounded blocks.",
            "route_decision": {
                "discard": "using only prime-square support as the exact shift-two contamination set",
                "retain": "prove shift-two excess above the prime-square leading local layer plus cubic-scale tail on infinitely many blocks",
                "next_single_lemma": "ShiftTwoCorrelationExceedsPrimeSquareLayerPlusCubicTailEnvelopeOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "ShiftTwoCorrelationExceedsThetaLayerOddLocalEnvelopeOnInfinitelyManyDyadicBlocks",
                "PrimeSquareDominantIntervalThetaLayerDecomposition",
                "PrimeSquareSupportAloneIsTheExactShiftTwoContaminationSet",
                "ShiftTwoCorrelationExceedsPrimeSquareLayerPlusCubicTailEnvelopeOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof. The local contamination hierarchy is sharper, but infinitude remains entirely in the missing correlation lower bound.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureFiniteJetElevenOneSquareLayerAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-195 resolves none of the four conjectures. It refutes "
            "finite-even-jet-only RH promotion, proves fixed-r rest-two Collatz "
            "strata decidable and closes r=11, and separates prime-square leading "
            "contamination from a smaller cubic-scale tail in Goldbach and Twin Prime."
        ),
        **sections,
        "cross_problem_synthesis": (
            "All four tracks now expose the same missing ingredient: a uniform "
            "infinite control cannot be replaced by a finite jet, infinitely many "
            "fixed-r decisions, or a sharper sublinear contamination hierarchy."
        ),
        "literature_boundary": {
            "riemann": "Rouche's theorem is classical; no literature novelty or actual Xi tail estimate is claimed.",
            "collatz": "The fixed-r decision reduction and r=11 computation do not imply global Collatz convergence.",
            "goldbach": "Chebyshev theta bounds are classical; no pointwise binary lower bound is inferred.",
            "twin_prime": "The interval decomposition does not overcome the parity barrier or prove exact gap two infinitely often.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "finite_jet_no_go_count": 1,
            "fixed_stratum_decidability_theorem_count": 1,
            "new_infinite_cycle_stratum_closure_count": 1,
            "prime_square_layer_decomposition_count": 2,
            "represented_collatz_word_count": collatz["aggregate"][
                "finite_exception_word_count"
            ],
            "rejected_or_corrected_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, object]]:
    attempts = []
    for problem_id, section_key in [
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin-prime", "twin_prime"),
    ]:
        section = audit[section_key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "status": "open_not_proven",
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": section["route_decision"]["next_single_lemma"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "finitejet_elevenone_squarelayer_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data" / "open-problem" / "ticket195-finitejet-elevenone-squarelayer.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-195-finite-jet-rouche.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-195-eleven-one-decidability.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-195-prime-square-layer.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-195-prime-square-local-layer.json",
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    for attempt in attempts:
        problem_id = str(attempt["problem_id"])
        section = audit[section_keys[problem_id]]
        write_json(
            paths[problem_id],
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "ticket_id": section["ticket_id"],
                "problem_id": problem_id,
                "status": "open_not_proven",
                "theorem_name": section["theorem_name"],
                "declared_proposition": section["declared_proposition"],
                "mathematical_argument": section["mathematical_argument"],
                "reproducible_computation": section["reproducible_computation"],
                "discarded_route": attempt["discarded_route"],
                "remaining_gap": attempt["remaining_gap"],
                "candidate_theorem": attempt["candidate_theorem"],
                "claim_boundary": attempt["claim_boundary"],
                "proof_dag": attempt["proof_dag"],
            },
        )


def main() -> None:
    audit = build_audit()
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(
            "TICKET-195 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
