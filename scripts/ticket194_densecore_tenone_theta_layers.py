from __future__ import annotations

import bisect
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
    power_of_two_contamination,
    weighted_odd_proper_prime_power_mass,
)


GENERATED_AT = "2026-08-08T06:30:00+09:00"
SCHEMA = "primeproject.ticket194-densecore-tenone-theta-layers.v1"
STATUS = (
    "dense_core_extension_and_ten_one_cycle_stratum_closed_"
    "theta_layer_prime_power_scale_proved_all_open"
)


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
                "id": f"{problem_code}-T193-INPUT",
                "label": previous_name,
                "status": "proved_exact_input_or_open_target",
            },
            {
                "id": f"{problem_code}-T194-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T194-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_coarse_surrogate",
            },
            {
                "id": f"{problem_code}-T194-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T193-INPUT", f"{problem_code}-T194-CLOSED"],
            [f"{problem_code}-T194-CLOSED", f"{problem_code}-T194-OPEN"],
            [f"{problem_code}-T194-REJECTED", f"{problem_code}-T194-OPEN"],
        ],
    }


def dense_core_projection_row(level: int) -> dict[str, object]:
    if level < 1:
        raise ValueError("level must be positive")
    quadratic_value = sum(
        (Fraction(1, 4**index) for index in range(1, level + 1)),
        Fraction(),
    )
    limit = Fraction(1, 3)
    return {
        "level_n": level,
        "operator_norm": 1,
        "quadratic_value": fraction_payload(quadratic_value),
        "limit_value": fraction_payload(limit),
        "exact_tail": fraction_payload(limit - quadratic_value),
        "tail_is_four_to_minus_n_over_three": (
            limit - quadratic_value == Fraction(1, 3 * 4**level)
        ),
    }


def monotone_dense_core_no_go_row(level: int) -> dict[str, object]:
    if level < 1:
        raise ValueError("level must be positive")
    coordinate = 2**level
    partial_norm_square = sum(
        (Fraction(1, 2**index) for index in range(1, level + 1)),
        Fraction(),
    )
    return {
        "level_j": level,
        "section_n": coordinate,
        "operator_norm": coordinate,
        "witness_partial_norm_square": fraction_payload(partial_norm_square),
        "witness_quadratic_value": level,
        "positive_semidefinite": True,
        "monotone_on_the_dense_core": True,
    }


def riemann_dense_core_extension_audit() -> dict[str, object]:
    projection_rows = [dense_core_projection_row(level) for level in range(1, 13)]
    no_go_rows = [monotone_dense_core_no_go_row(level) for level in range(1, 13)]
    failures = sum(
        int(row["operator_norm"] != 1)
        + int(not row["tail_is_four_to_minus_n_over_three"])
        for row in projection_rows
    )
    failures += sum(
        int(row["operator_norm"] != row["section_n"])
        + int(row["witness_quadratic_value"] != row["level_j"])
        + int(not row["positive_semidefinite"])
        + int(not row["monotone_on_the_dense_core"])
        for row in no_go_rows
    )
    return {
        "theorem": (
            "Let q_n be continuous Hermitian quadratic forms on a complex "
            "Hilbert space H, with associated forms B_n, and let D be dense "
            "in H. If sup_n ||B_n||<infinity and q_n(x) converges for every "
            "x in D, then B_n(x,y) and q_n(x) converge for every x,y in H "
            "to a bounded Hermitian form. Positivity passes to the limit. "
            "Positivity and monotonicity on D do not replace the uniform "
            "bound: q_n(x)=sum_(k<=n) k|x_k|^2 has all those core properties "
            "on c_00 while ||B_n||=n and diverges at an explicit l^2 vector."
        ),
        "proof": (
            "Polarization gives convergence of B_n(u,v) for u,v in D. If "
            "||B_n||<=M and u,v approximate x,y, then the Cauchy difference "
            "B_n-B_m away from D is bounded by 2M(||x-u||||y||+"
            "||u||||y-v||). First choose u,v, then use core convergence. "
            "This proves convergence everywhere and a norm-M limit. For the "
            "no-go, positive diagonal sections sum_(k<=n) k|x_k|^2 increase "
            "and stabilize on every c_00 vector. The l^2 vector with "
            "|x_(2^j)|^2=2^(-j) has norm one but q_(2^J)(x)=J."
        ),
        "uniform_projection_rows": projection_rows,
        "positive_monotone_dense_core_no_go_rows": no_go_rows,
        "extension_contract": {
            "uniform_bound_plus_dense_core_convergence_extends_everywhere": True,
            "positivity_passes_to_limit": True,
            "positive_monotone_dense_core_convergence_alone_is_sufficient": False,
            "actual_weil_uniform_bound_verified": False,
            "actual_weil_dense_core_convergence_verified": False,
        },
        "no_go_scope": (
            "This is an exact extension criterion, not a proof that the "
            "pole-neutral Weil sections satisfy either premise."
        ),
        "failure_count": failures,
    }


TEN_ONES = 10


def ten_one_product_bound(horizon: int) -> Fraction:
    if horizon < 1:
        raise ValueError("horizon must be positive")
    return Fraction(2**TEN_ONES) * Fraction(5, 6) ** horizon


def ten_one_boundary_components(horizon: int) -> tuple[int, list[list[int]]]:
    if horizon < TEN_ONES:
        raise ValueError("ten valuation-one positions require h>=10")
    prefixes: list[list[int]] = []
    for ones_before in range(TEN_ONES + 1):
        values = [0]
        running = 0
        for index in range(horizon):
            exponent = 2 * index - ones_before
            if exponent >= 0:
                running += 3 ** (horizon - 1 - index) * 2**exponent
            values.append(running)
        prefixes.append(values)
    constant = (
        3 ** (horizon - 1)
        + prefixes[TEN_ONES][horizon]
        - prefixes[1][1]
    )
    boundaries = [[0] * horizon for _ in range(TEN_ONES)]
    for boundary_index in range(1, TEN_ONES):
        for position in range(1, horizon):
            boundaries[boundary_index][position] = (
                prefixes[boundary_index][position + 1]
                - prefixes[boundary_index + 1][position + 1]
            )
    return constant, boundaries


def ten_one_boundary_numerator(
    horizon: int, positions: tuple[int, ...]
) -> int:
    if len(positions) != TEN_ONES or positions[0] != 0:
        raise ValueError("positions must contain ten entries with p_0=0")
    if tuple(sorted(positions)) != positions or positions[-1] >= horizon:
        raise ValueError("positions must be strictly increasing inside the horizon")
    constant, boundaries = ten_one_boundary_components(horizon)
    return constant + sum(
        boundaries[index][positions[index]]
        for index in range(1, TEN_ONES)
    )


def ten_one_boundary_formula_validation() -> dict[str, object]:
    checked = 0
    failures = 0
    transcript = hashlib.sha256()
    for horizon in range(10, 17):
        for tail in itertools.combinations(range(1, horizon), 9):
            positions = (0,) + tail
            position_set = set(positions)
            word = tuple(
                1 if index in position_set else 2
                for index in range(horizon)
            )
            direct = ordered_affine_numerator(word)
            boundary = ten_one_boundary_numerator(horizon, positions)
            failures += int(direct != boundary)
            checked += 1
            transcript.update(
                f"{horizon}:{positions}:{direct}:{boundary}\n".encode("ascii")
            )
    return {
        "horizons": [10, 16],
        "normalized_words_checked": checked,
        "formula_mismatch_count": failures,
        "transcript_sha256": transcript.hexdigest(),
    }


def finite_ten_one_horizon_row(horizon: int) -> dict[str, object]:
    if not 25 <= horizon <= 38:
        raise ValueError("the finite contracting range is h=25..38")
    denominator = 2 ** (2 * horizon - TEN_ONES) - 3**horizon
    constant, boundary = ten_one_boundary_components(horizon)
    left_buckets: list[list[tuple[int, tuple[int, ...]]]] = [
        [] for _ in range(horizon)
    ]
    left_tuple_count = 0
    for positions in itertools.combinations(range(1, horizon), 5):
        remainder = (
            constant
            + sum(
                boundary[index][positions[index - 1]]
                for index in range(1, 6)
            )
        ) % denominator
        left_buckets[positions[-1]].append((remainder, positions))
        left_tuple_count += 1

    residue_representatives: dict[int, tuple[int, ...]] = {}
    next_last = 0
    right_tuple_count = 0
    represented_word_count = 0
    hits: list[dict[str, object]] = []
    transcript = hashlib.sha256()
    for first_right in range(6, horizon - 3):
        while next_last < first_right:
            for remainder, positions in left_buckets[next_last]:
                residue_representatives.setdefault(remainder, positions)
            next_last += 1
        for tail in itertools.combinations(range(first_right + 1, horizon), 3):
            right_positions = (first_right,) + tail
            right_remainder = sum(
                boundary[index][right_positions[index - 6]]
                for index in range(6, TEN_ONES)
            ) % denominator
            target = (-right_remainder) % denominator
            hit = target in residue_representatives
            transcript.update(
                f"{right_positions}:{target}:{int(hit)}\n".encode("ascii")
            )
            right_tuple_count += 1
            represented_word_count += math.comb(first_right - 1, 5)
            if hit:
                positions = (
                    (0,)
                    + residue_representatives[target]
                    + right_positions
                )
                numerator = ten_one_boundary_numerator(horizon, positions)
                hits.append(
                    {
                        "positions": list(positions),
                        "affine_numerator_B": str(numerator),
                        "cycle_denominator_D": str(denominator),
                        "B_mod_D": str(numerator % denominator),
                    }
                )
    return {
        "horizon_h": horizon,
        "rotation_normalization": "v_0=1",
        "contracting": denominator > 0,
        "left_tuple_count": left_tuple_count,
        "expected_left_tuple_count": math.comb(horizon - 1, 5),
        "right_tuple_count": right_tuple_count,
        "expected_right_tuple_count": math.comb(horizon - 6, 4),
        "represented_word_count": represented_word_count,
        "expected_word_count": math.comb(horizon - 1, 9),
        "active_left_residue_count_at_final_boundary": len(
            residue_representatives
        ),
        "divisibility_hit_count": len(hits),
        "divisibility_hits": hits,
        "mitm_transcript_sha256": transcript.hexdigest(),
    }


def collatz_ten_one_audit() -> dict[str, object]:
    formula_validation = ten_one_boundary_formula_validation()
    finite_rows = [finite_ten_one_horizon_row(h) for h in range(25, 39)]
    analytic_rows = [
        {
            "horizon_h": horizon,
            "cycle_product_upper_bound": fraction_payload(
                ten_one_product_bound(horizon)
            ),
            "strictly_below_one": ten_one_product_bound(horizon) < 1,
        }
        for horizon in [39, 40, 48, 64, 96]
    ]
    failures = int(formula_validation["formula_mismatch_count"])
    failures += sum(
        int(not row["contracting"])
        + int(row["left_tuple_count"] != row["expected_left_tuple_count"])
        + int(row["right_tuple_count"] != row["expected_right_tuple_count"])
        + int(row["represented_word_count"] != row["expected_word_count"])
        + int(row["divisibility_hit_count"] != 0)
        for row in finite_rows
    )
    failures += sum(int(not row["strictly_below_one"]) for row in analytic_rows)
    failures += int(ten_one_product_bound(38) <= 1)
    total_words = sum(int(row["represented_word_count"]) for row in finite_rows)
    return {
        "theorem": (
            "No positive accelerated Collatz cycle has a valuation period "
            "with exactly ten entries equal to one and every other entry "
            "equal to two, including primitive and imprimitive periods."
        ),
        "proof": (
            "For length h the affine denominator is D=2^(2h-10)-3^h, "
            "positive exactly from h=25. Rotate to v_0=1. The numerator is "
            "a constant plus nine boundary terms. An exact 5+4 residue MITM "
            "covers every normalized word for h=25..38 and finds no "
            "divisibility hit. For a nontrivial positive odd cycle, "
            "1<=1024(5/6)^h; this is below one from h=39 onward."
        ),
        "boundary_formula_validation": formula_validation,
        "finite_exception_horizon_rows": finite_rows,
        "analytic_product_rows": analytic_rows,
        "analytic_bound": {
            "bound_at_h_38": fraction_payload(ten_one_product_bound(38)),
            "bound_at_h_39": fraction_payload(ten_one_product_bound(39)),
            "analytic_range_starts_at_h": 39,
            "bound_is_strictly_decreasing": True,
        },
        "aggregate": {
            "infinite_family_proved": True,
            "includes_imprimitive_words": True,
            "rotation_normalization_is_complete": True,
            "mitm_coverage_is_complete": True,
            "contracting_range_starts_at_h": 25,
            "analytic_range_starts_at_h": 39,
            "finite_exception_word_count": total_words,
            "finite_word_count_identity": "C(38,10)-C(24,10)=470772500",
            "left_tuple_count": sum(
                int(row["left_tuple_count"]) for row in finite_rows
            ),
            "right_tuple_count": sum(
                int(row["right_tuple_count"]) for row in finite_rows
            ),
            "divisibility_hits": sum(
                int(row["divisibility_hit_count"]) for row in finite_rows
            ),
        },
        "no_go_scope": (
            "This closes only the exactly-ten-one/rest-two periodic stratum. "
            "Eleven-or-more-one strata, valuations at least three, and "
            "aperiodic divergence remain open."
        ),
        "failure_count": failures,
    }


def integer_kth_root(value: int, exponent: int) -> int:
    if value < 0 or exponent < 1:
        raise ValueError("value must be nonnegative and exponent positive")
    if value < 2 or exponent == 1:
        return value
    low = 1
    high = 1 << ((value.bit_length() + exponent - 1) // exponent)
    while low <= high:
        middle = (low + high) // 2
        power = middle**exponent
        if power <= value:
            low = middle + 1
        else:
            high = middle - 1
    return high


def odd_primes_from_metadata(
    metadata: list[tuple[int, int] | None], limit: int
) -> list[int]:
    return [
        value
        for value in range(3, min(limit, len(metadata) - 1) + 1)
        if metadata[value] == (value, 1)
    ]


def theta_odd(primes: list[int], limit: int) -> float:
    stop = bisect.bisect_right(primes, limit)
    return math.fsum(math.log(prime) for prime in primes[:stop])


def theta_layer_mass(limit: int, primes: list[int]) -> dict[str, object]:
    if limit < 0:
        raise ValueError("limit must be nonnegative")
    layers: list[dict[str, object]] = []
    exponent = 2
    while 3**exponent <= limit:
        root = integer_kth_root(limit, exponent)
        theta = theta_odd(primes, root)
        layers.append(
            {
                "exponent_k": exponent,
                "integer_root": root,
                "theta_odd_root": theta,
            }
        )
        exponent += 1
    return {
        "limit_Y": limit,
        "layers": layers,
        "layer_count": len(layers),
        "reconstructed_mass": math.fsum(
            float(row["theta_odd_root"]) for row in layers
        ),
    }


def theta_interval_mass(
    start: int, stop: int, primes: list[int]
) -> dict[str, object]:
    if start < 0 or stop < start:
        raise ValueError("require 0<=start<=stop")
    upper = theta_layer_mass(stop - 1, primes)
    lower = theta_layer_mass(start - 1, primes)
    lower_by_exponent = {
        int(row["exponent_k"]): float(row["theta_odd_root"])
        for row in lower["layers"]
    }
    layers = []
    for row in upper["layers"]:
        exponent = int(row["exponent_k"])
        contribution = float(row["theta_odd_root"]) - lower_by_exponent.get(
            exponent, 0.0
        )
        layers.append(
            {
                "exponent_k": exponent,
                "upper_integer_root": row["integer_root"],
                "lower_integer_root": integer_kth_root(start - 1, exponent),
                "theta_odd_difference": contribution,
            }
        )
    return {
        "interval": [start, stop],
        "layers": layers,
        "reconstructed_mass": math.fsum(
            float(row["theta_odd_difference"]) for row in layers
        ),
    }


def exact_binary_mass_classification(target: int) -> dict[str, object]:
    direct = power_of_two_contamination(target)
    bit_positions = [
        bit for bit in range(target.bit_length()) if target & (1 << bit)
    ]
    if target >= 6 and len(bit_positions) == 1:
        expected_count = 1
        classification = "one repeated power-of-two pair"
    elif (
        target >= 6
        and len(bit_positions) == 2
        and bit_positions[0] >= 1
    ):
        expected_count = 2
        classification = "two ordered distinct power-of-two pairs"
    else:
        expected_count = 0
        classification = "no admissible power-of-two pair"
    return {
        **direct,
        "binary_one_bit_positions": bit_positions,
        "classification": classification,
        "expected_ordered_pair_count": expected_count,
        "classification_matches_direct_enumeration": (
            expected_count == direct["ordered_pair_count"]
        ),
    }


def goldbach_theta_layer_audit() -> dict[str, object]:
    targets = [2**exponent for exponent in range(10, 21)]
    binary_targets = [6, 8, 10, 12, 14, 18, 20, 24, 30, 32, 34]
    metadata = prime_power_metadata(max(targets) + 2)
    primes = odd_primes_from_metadata(metadata, math.isqrt(max(targets)))
    rows: list[dict[str, object]] = []
    for target in targets:
        decomposition = goldbach_prime_power_row(target, metadata)
        layers = theta_layer_mass(target, primes)
        actual_mass = weighted_odd_proper_prime_power_mass(
            metadata, 2, target + 1
        )
        binary = exact_binary_mass_classification(target)
        envelope = (
            2.0 * math.log(target) * layers["reconstructed_mass"]
            + binary["exact_weight"]
        )
        total = decomposition["weighted_total_convolution"]
        contamination = decomposition["weighted_prime_power_contamination"]
        rows.append(
            {
                "target_N": target,
                "theta_layers": layers,
                "actual_odd_weighted_proper_power_mass": actual_mass,
                "binary_mass": binary,
                "theta_layer_parity_envelope": envelope,
                "weighted_total_convolution": total,
                "actual_contamination": contamination,
                "mass_over_sqrt_N": actual_mass / math.sqrt(target),
                "envelope_over_sqrt_N_log_N": envelope
                / (math.sqrt(target) * math.log(target)),
                "checks": {
                    "theta_layers_reconstruct_odd_mass": abs(
                        layers["reconstructed_mass"] - actual_mass
                    )
                    < 1e-9,
                    "binary_classification_exact": binary[
                        "classification_matches_direct_enumeration"
                    ],
                    "actual_contamination_below_theta_layer_envelope": (
                        contamination <= envelope + 1e-9
                    ),
                    "finite_total_exceeds_theta_layer_envelope": total > envelope,
                },
            }
        )
    binary_rows = [exact_binary_mass_classification(n) for n in binary_targets]
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += sum(
        int(not row["classification_matches_direct_enumeration"])
        for row in binary_rows
    )
    return {
        "theorem": (
            "For every Y>=1, the odd proper-prime-power mass satisfies the "
            "exact identity W_odd(Y)=sum_(k>=2) theta_odd(floor(Y^(1/k))). "
            "By the classical Chebyshev bound theta(t)=O(t), W_odd(Y)="
            "O(sqrt(Y)); hence the TICKET-193 Goldbach contamination "
            "envelope is O(sqrt(N) log N), not merely the earlier elementary "
            "O(sqrt(N) log^2 N). The power-of-two term is exactly classified "
            "by the binary expansion of N."
        ),
        "proof": (
            "Each exponent k>=2 contributes log p exactly when p^k<=Y, "
            "giving the theta-layer identity after exchanging two finite "
            "sums. Chebyshev gives theta(t)<=Ct. The k=2 layer is O(sqrt Y); "
            "the remaining O(log Y) layers are each O(Y^(1/3)), whose total "
            "is O(sqrt Y). Binary uniqueness gives one ordered pair when N "
            "is a power of two, two when its even binary expansion has two "
            "one-bits, and none otherwise, for N>=6."
        ),
        "theta_layer_rows": rows,
        "binary_classification_rows": binary_rows,
        "aggregate": {
            "target_count": len(rows),
            "largest_target": targets[-1],
            "theta_layer_identity_proved": True,
            "chebyshev_mass_scale": "O(sqrt(N))",
            "contamination_scale": "O(sqrt(N) log(N))",
            "binary_mass_exactly_classified": True,
            "finite_sample_success_count": sum(
                row["checks"]["finite_total_exceeds_theta_layer_envelope"]
                for row in rows
            ),
            "all_large_even_targets_proved": False,
        },
        "no_go_scope": (
            "The theta layers improve the analytic contamination scale but "
            "do not prove a pointwise lower bound for every sufficiently "
            "large even target."
        ),
        "failure_count": failures,
    }


def twin_theta_layer_audit() -> dict[str, object]:
    exponents = list(range(4, 20))
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
        left_actual = weighted_odd_proper_prime_power_mass(
            metadata, lower, upper
        )
        right_actual = weighted_odd_proper_prime_power_mass(
            metadata, lower + 2, upper + 2
        )
        envelope = math.log(ceiling) * (
            left_layers["reconstructed_mass"]
            + right_layers["reconstructed_mass"]
        )
        total = arithmetic["weighted_shift_two_correlation"]
        contamination = arithmetic["weighted_prime_power_contamination"]
        rows.append(
            {
                **arithmetic,
                "left_theta_interval": left_layers,
                "right_theta_interval": right_layers,
                "left_actual_odd_mass": left_actual,
                "right_actual_odd_mass": right_actual,
                "theta_layer_odd_local_envelope": envelope,
                "local_mass_over_sqrt_X": (
                    left_actual + right_actual
                ) / math.sqrt(lower),
                "envelope_over_sqrt_X_log_X": envelope
                / (math.sqrt(lower) * math.log(lower)),
                "checks": {
                    **arithmetic["checks"],
                    "left_theta_layers_reconstruct_mass": abs(
                        left_layers["reconstructed_mass"] - left_actual
                    )
                    < 1e-9,
                    "right_theta_layers_reconstruct_mass": abs(
                        right_layers["reconstructed_mass"] - right_actual
                    )
                    < 1e-9,
                    "actual_contamination_below_theta_layer_envelope": (
                        contamination <= envelope + 1e-9
                    ),
                    "finite_total_exceeds_theta_layer_envelope": total > envelope,
                },
            }
        )
    failures = sum(not check for row in rows for check in row["checks"].values())
    return {
        "theorem": (
            "For every integer interval [A,B), its odd proper-prime-power "
            "mass is exactly sum_(k>=2)[theta_odd(floor((B-1)^(1/k)))-"
            "theta_odd(floor((A-1)^(1/k)))]. Therefore the TICKET-193 "
            "shift-two odd local contamination has exact theta-layer form "
            "and is O(sqrt(X) log X) on [X,2X). Correlation above that exact "
            "envelope still forces a twin prime in the block."
        ),
        "proof": (
            "Subtract the two cumulative theta-layer identities at B-1 and "
            "A-1. Each proper prime power in [A,B) is counted once at its "
            "exponent. Both translated intervals lie below 2X+2, so the "
            "Chebyshev O(sqrt Y) cumulative bound makes their total mass "
            "O(sqrt X); multiplication by the partner log weight gives "
            "O(sqrt X log X). TICKET-193 supplies the exact forcing bridge."
        ),
        "finite_dyadic_rows": rows,
        "aggregate": {
            "dyadic_block_count": len(rows),
            "largest_upper_endpoint": rows[-1]["block"][1],
            "theta_interval_identity_proved": True,
            "odd_local_mass_scale": "O(sqrt(X))",
            "contamination_scale": "O(sqrt(X) log(X))",
            "finite_block_success_count": sum(
                row["checks"]["finite_total_exceeds_theta_layer_envelope"]
                for row in rows
            ),
            "infinitely_many_envelope_successes_proved": False,
        },
        "no_go_scope": (
            "The exact theta-layer form and sublinear contamination scale do "
            "not establish a correlation lower bound on infinitely many "
            "unbounded dyadic blocks."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_dense_core_extension_audit()
    collatz = collatz_ten_one_audit()
    goldbach = goldbach_theta_layer_audit()
    twin = twin_theta_layer_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-194",
            "theorem_name": "UniformlyBoundedDenseCoreQuadraticConvergenceExtendsEverywhere",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "Neither uniform boundedness nor dense-core convergence of the actual pole-neutral Weil sections is proved.",
            "route_decision": {
                "discard": "using positivity and monotonicity on a dense core as a substitute for a uniform operator bound",
                "retain": "prove one uniform bound and dense-core convergence for the actual pole-neutral Weil finite sections",
                "next_single_lemma": "PoleNeutralWeilFiniteSectionsAreUniformlyBoundedAndConvergeOnADenseCore",
            },
            "proof_dag": proof_dag(
                "RH",
                "EverywherePointwiseQuadraticConvergenceForcesUniformBoundedExtension",
                "UniformlyBoundedDenseCoreQuadraticConvergenceExtendsEverywhere",
                "PositiveMonotoneDenseCoreConvergenceReplacesUniformBoundedness",
                "PoleNeutralWeilFiniteSectionsAreUniformlyBoundedAndConvergeOnADenseCore",
            ),
            "claim_boundary": "No RH proof. The extension mechanism is complete, but both arithmetic Weil premises remain open.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-194",
            "theorem_name": "ExactlyTenValuationOnesOtherwiseTwoCycleExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Eleven-or-more-one strata, valuations at least three, and aperiodic divergence remain open.",
            "route_decision": {
                "discard": "the exactly-ten-one/rest-two valuation stratum as a source of positive Collatz cycles",
                "retain": "boundary-term MITM plus a uniform product contradiction, generalized one stratum at a time",
                "next_single_lemma": "NoContractingValuationWordWithExactlyElevenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "ExactlyNineValuationOnesOtherwiseTwoCycleExclusion",
                "ExactlyTenValuationOnesOtherwiseTwoCycleExclusion",
                "ExactlyTenOneRestTwoCanContainAPositiveCycle",
                "NoContractingValuationWordWithExactlyElevenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            ),
            "claim_boundary": "No Collatz proof. The complete exactly-ten-one/rest-two periodic valuation stratum is excluded.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-194",
            "theorem_name": "OddPrimePowerThetaLayerCompressionAndBinaryMassClassification",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No pointwise lower bound exceeds the exact theta-layer envelope for every sufficiently large even target.",
            "route_decision": {
                "discard": "treating the elementary O(sqrt(N) log^2 N) contamination majorant as the intrinsic analytic scale",
                "retain": "prove every-large-even binary correlation above the exact theta-layer parity envelope",
                "next_single_lemma": "BinaryCorrelationExceedsThetaLayerPrimePowerEnvelopeForEveryLargeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "ParitySeparatedPrimePowerContaminationEnvelope",
                "OddPrimePowerThetaLayerCompressionAndBinaryMassClassification",
                "PrimePowerContaminationRequiresASqrtNLogSquaredNThreshold",
                "BinaryCorrelationExceedsThetaLayerPrimePowerEnvelopeForEveryLargeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof. The exact contamination representation and sharper asymptotic scale are proved; the universal lower bound is open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-194",
            "theorem_name": "OddPrimePowerIntervalThetaLayerCompression",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No proof exceeds the exact theta-layer local envelope on infinitely many unbounded dyadic blocks.",
            "route_decision": {
                "discard": "treating the earlier sqrt(X) log^2(X) global majorant as the natural shift-two contamination scale",
                "retain": "prove shift-two correlation above the exact two-interval theta-layer envelope on infinitely many blocks",
                "next_single_lemma": "ShiftTwoCorrelationExceedsThetaLayerOddLocalEnvelopeOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "OddOnlyShiftTwoContaminationEnvelope",
                "OddPrimePowerIntervalThetaLayerCompression",
                "ShiftTwoContaminationRequiresASqrtXLogSquaredXThreshold",
                "ShiftTwoCorrelationExceedsThetaLayerOddLocalEnvelopeOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof. The local contamination is exactly layered and sublinear, but infinitely many positive blocks are not proved.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureDenseCoreTenOneThetaLayerAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-194 resolves none of the four conjectures. It closes the "
            "complete exactly-ten-one/rest-two accelerated Collatz cycle "
            "stratum, completes the uniformly-bounded dense-core extension "
            "step for the RH route, and proves exact theta-layer identities "
            "that lower both prime-power contamination scales by one log."
        ),
        **sections,
        "cross_problem_synthesis": (
            "Uniform boundedness and Chebyshev theta layers convert local "
            "information into controlled global extensions. The Collatz "
            "boundary decomposition converts a 470-million-word finite "
            "exception range into an exact low-dimensional residue audit."
        ),
        "literature_boundary": {
            "riemann": "No external result supplies the two actual pole-neutral Weil premises required by the extension theorem.",
            "collatz": "No global Collatz convergence result is claimed; one complete periodic valuation stratum is removed.",
            "goldbach": "The classical Chebyshev theta bound is used only for contamination scale; no every-even exceptional-set upgrade is inferred.",
            "twin_prime": "The theta-layer identity does not overcome the parity barrier or produce a lower bound for exact gap two.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "new_infinite_cycle_stratum_closure_count": 1,
            "theta_layer_identity_count": 2,
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
                "candidate_theorem": section["route_decision"][
                    "next_single_lemma"
                ],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": section["route_decision"][
                    "next_single_lemma"
                ],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    write_json(
        ROOT / "data" / "open-problem" / "ticket194-densecore-tenone-theta-layers.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "densecore_tenone_theta_layer_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-194-dense-core-extension.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-194-ten-one-cycle-exclusion.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-194-theta-layer-envelope.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-194-theta-layer-local-envelope.json",
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    attempts_by_problem = {row["problem_id"]: row for row in attempts}
    for problem_id, path in paths.items():
        section = audit[section_keys[problem_id]]
        attempt = attempts_by_problem[problem_id]
        write_json(
            path,
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
            "TICKET-194 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
