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
from ticket192_uniform_eightone_weighted_envelope import (
    weighted_proper_prime_power_mass,
)


GENERATED_AT = "2026-08-08T05:00:00+09:00"
SCHEMA = "primeproject.ticket193-everywhere-nineone-parity-envelope.v1"
STATUS = (
    "one_additional_infinite_cycle_stratum_closed_"
    "everywhere_extension_and_two_parity_envelopes_proved_all_open"
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
                "id": f"{problem_code}-T192-INPUT",
                "label": previous_name,
                "status": "proved_exact_input_or_open_target",
            },
            {
                "id": f"{problem_code}-T193-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T193-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_stronger_than_necessary",
            },
            {
                "id": f"{problem_code}-T193-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T192-INPUT", f"{problem_code}-T193-CLOSED"],
            [f"{problem_code}-T193-CLOSED", f"{problem_code}-T193-OPEN"],
            [f"{problem_code}-T193-REJECTED", f"{problem_code}-T193-OPEN"],
        ],
    }


def dense_core_spike_row(index: int) -> dict[str, object]:
    if index < 1:
        raise ValueError("index must be positive")
    return {
        "spike_index_n": index,
        "operator_norm": index,
        "quadratic_form": f"q_{index}(x)={index}|x_{index}|^2",
        "positive_semidefinite": True,
        "vanishes_on_every_vector_supported_below_n": True,
    }


def all_space_witness_row(level: int) -> dict[str, object]:
    if level < 1:
        raise ValueError("level must be positive")
    coordinate = 2**level
    coordinate_square = Fraction(level, coordinate)
    partial_norm_square = sum(
        (Fraction(j, 2**j) for j in range(1, level + 1)), Fraction()
    )
    return {
        "level_j": level,
        "coordinate_n": coordinate,
        "coordinate_square": fraction_payload(coordinate_square),
        "quadratic_value_q_n_x": level,
        "partial_norm_square": fraction_payload(partial_norm_square),
        "partial_norm_square_below_two": partial_norm_square < 2,
    }


def riemann_everywhere_extension_audit() -> dict[str, object]:
    spike_rows = [dense_core_spike_row(index) for index in [2, 4, 8, 16, 32, 64]]
    witness_rows = [all_space_witness_row(level) for level in range(1, 13)]
    failures = sum(
        int(not row["positive_semidefinite"])
        + int(row["operator_norm"] != row["spike_index_n"])
        for row in spike_rows
    )
    failures += sum(
        int(row["quadratic_value_q_n_x"] != row["level_j"])
        + int(not row["partial_norm_square_below_two"])
        for row in witness_rows
    )
    failures += int(
        any(
            later["operator_norm"] <= earlier["operator_norm"]
            for earlier, later in zip(spike_rows, spike_rows[1:])
        )
    )
    return {
        "theorem": (
            "Let q_n be continuous Hermitian quadratic forms on a complex "
            "Hilbert space H, with associated bounded Hermitian forms B_n. "
            "If q_n(x) converges for every x in H, then "
            "sup_n ||B_n|| is finite, B_n(x,y) converges for every x,y, and "
            "the limit is a bounded Hermitian form whose quadratic form is "
            "lim_n q_n. Positivity passes to the limit. Convergence merely "
            "on a dense core is insufficient: q_n(x)=n|x_n|^2 converges to "
            "zero on c_00 while ||B_n||=n."
        ),
        "proof": (
            "Complex polarization turns diagonal convergence into scalar "
            "convergence of B_n(x,y) for every x,y. For fixed x, the bounded "
            "linear functionals y -> B_n(x,y) are pointwise bounded, so the "
            "uniform boundedness principle gives sup_n ||B_n(x,.)||<infinity. "
            "Applying the principle again to the representing operators T_n "
            "gives sup_n ||T_n||<infinity. The pointwise form limit is then "
            "bounded and Hermitian. For the dense-core no-go, every fixed "
            "finite-support vector is annihilated eventually, but the norms "
            "diverge. The vector x_(2^j)=sqrt(j/2^j), zero elsewhere, belongs "
            "to l^2 because sum j/2^j=2 and has q_(2^j)(x)=j, so convergence "
            "indeed fails somewhere in the complete space."
        ),
        "dense_core_spike_rows": spike_rows,
        "all_space_failure_witness_rows": witness_rows,
        "extension_contract": {
            "everywhere_pointwise_convergence_forces_uniform_bound": True,
            "associated_forms_converge_pointwise": True,
            "positivity_passes_to_limit": True,
            "dense_core_pointwise_convergence_is_sufficient": False,
            "actual_weil_everywhere_convergence_verified": False,
        },
        "no_go_scope": (
            "The theorem is an exact functional-analytic promotion rule. It "
            "does not prove everywhere convergence of the actual pole-neutral "
            "Weil finite sections and therefore does not prove RH."
        ),
        "failure_count": failures,
    }


def nine_one_product_bound(horizon: int) -> Fraction:
    if horizon < 1:
        raise ValueError("horizon must be positive")
    return Fraction(512) * Fraction(5, 6) ** horizon


def nine_one_boundary_components(horizon: int) -> tuple[int, list[list[int]]]:
    if horizon < 9:
        raise ValueError("nine valuation-one positions require h>=9")
    prefixes: list[list[int]] = []
    for ones_before in range(10):
        values = [0]
        running = 0
        for index in range(horizon):
            exponent = 2 * index - ones_before
            if exponent >= 0:
                running += 3 ** (horizon - 1 - index) * 2**exponent
            values.append(running)
        prefixes.append(values)
    constant = 3 ** (horizon - 1) + prefixes[9][horizon] - prefixes[1][1]
    boundaries = [[0] * horizon for _ in range(9)]
    for boundary_index in range(1, 9):
        for position in range(1, horizon):
            boundaries[boundary_index][position] = (
                prefixes[boundary_index][position + 1]
                - prefixes[boundary_index + 1][position + 1]
            )
    return constant, boundaries


def nine_one_boundary_numerator(
    horizon: int, positions: tuple[int, ...]
) -> int:
    if len(positions) != 9 or positions[0] != 0:
        raise ValueError("positions must contain nine entries with p_0=0")
    if tuple(sorted(positions)) != positions or positions[-1] >= horizon:
        raise ValueError("positions must be strictly increasing inside the horizon")
    constant, boundaries = nine_one_boundary_components(horizon)
    return constant + sum(
        boundaries[index][positions[index]] for index in range(1, 9)
    )


def finite_nine_one_horizon_row(horizon: int) -> dict[str, object]:
    if not 22 <= horizon <= 34:
        raise ValueError("the finite contracting range is h=22..34")
    denominator = 2 ** (2 * horizon - 9) - 3**horizon
    constant, boundary = nine_one_boundary_components(horizon)
    left_buckets: list[list[tuple[int, tuple[int, ...]]]] = [
        [] for _ in range(horizon)
    ]
    left_tuple_count = 0
    for positions in itertools.combinations(range(1, horizon), 4):
        remainder = (
            constant
            + boundary[1][positions[0]]
            + boundary[2][positions[1]]
            + boundary[3][positions[2]]
            + boundary[4][positions[3]]
        ) % denominator
        left_buckets[positions[3]].append((remainder, positions))
        left_tuple_count += 1

    residue_representatives: dict[int, tuple[int, ...]] = {}
    next_last = 0
    right_tuple_count = 0
    represented_word_count = 0
    hits: list[dict[str, object]] = []
    transcript = hashlib.sha256()
    for first_right in range(5, horizon - 3):
        while next_last < first_right:
            for remainder, positions in left_buckets[next_last]:
                residue_representatives.setdefault(remainder, positions)
            next_last += 1
        for tail in itertools.combinations(range(first_right + 1, horizon), 3):
            right_positions = (first_right,) + tail
            right_remainder = (
                boundary[5][right_positions[0]]
                + boundary[6][right_positions[1]]
                + boundary[7][right_positions[2]]
                + boundary[8][right_positions[3]]
            ) % denominator
            target = (-right_remainder) % denominator
            hit = target in residue_representatives
            transcript.update(
                f"{right_positions}:{target}:{int(hit)}\n".encode("ascii")
            )
            right_tuple_count += 1
            represented_word_count += math.comb(first_right - 1, 4)
            if hit:
                full_positions = (
                    (0,)
                    + residue_representatives[target]
                    + right_positions
                )
                numerator = nine_one_boundary_numerator(horizon, full_positions)
                hits.append(
                    {
                        "positions": list(full_positions),
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
        "expected_left_tuple_count": math.comb(horizon - 1, 4),
        "right_tuple_count": right_tuple_count,
        "expected_right_tuple_count": math.comb(horizon - 5, 4),
        "represented_word_count": represented_word_count,
        "expected_word_count": math.comb(horizon - 1, 8),
        "active_left_residue_count_at_final_boundary": len(
            residue_representatives
        ),
        "divisibility_hit_count": len(hits),
        "divisibility_hits": hits,
        "mitm_transcript_sha256": transcript.hexdigest(),
    }


def boundary_formula_validation() -> dict[str, object]:
    checked = 0
    failures = 0
    digest = hashlib.sha256()
    for horizon in range(9, 16):
        for tail in itertools.combinations(range(1, horizon), 8):
            positions = (0,) + tail
            position_set = set(positions)
            word = tuple(
                1 if index in position_set else 2 for index in range(horizon)
            )
            direct = ordered_affine_numerator(word)
            boundary = nine_one_boundary_numerator(horizon, positions)
            failures += int(direct != boundary)
            checked += 1
            digest.update(f"{horizon}:{positions}:{direct}:{boundary}\n".encode("ascii"))
    return {
        "horizons": [9, 15],
        "normalized_words_checked": checked,
        "formula_mismatch_count": failures,
        "transcript_sha256": digest.hexdigest(),
    }


def collatz_nine_one_audit() -> dict[str, object]:
    formula_validation = boundary_formula_validation()
    finite_rows = [finite_nine_one_horizon_row(h) for h in range(22, 35)]
    analytic_rows = [
        {
            "horizon_h": horizon,
            "cycle_product_upper_bound": fraction_payload(
                nine_one_product_bound(horizon)
            ),
            "strictly_below_one": nine_one_product_bound(horizon) < 1,
        }
        for horizon in [35, 36, 48, 64, 96]
    ]
    failures = formula_validation["formula_mismatch_count"]
    failures += sum(
        int(not row["contracting"])
        + int(row["left_tuple_count"] != row["expected_left_tuple_count"])
        + int(row["right_tuple_count"] != row["expected_right_tuple_count"])
        + int(row["represented_word_count"] != row["expected_word_count"])
        + int(row["divisibility_hit_count"] != 0)
        for row in finite_rows
    )
    failures += sum(not row["strictly_below_one"] for row in analytic_rows)
    failures += int(nine_one_product_bound(34) <= 1)
    total_words = sum(row["represented_word_count"] for row in finite_rows)
    return {
        "theorem": (
            "No positive accelerated Collatz cycle has a valuation period "
            "with exactly nine entries equal to one and every other entry "
            "equal to two, including primitive and imprimitive periods."
        ),
        "proof": (
            "For length h the affine denominator is D=2^(2h-9)-3^h, "
            "positive exactly from h=22. Rotate a word so one of its nine "
            "ones is first; divisibility is rotation invariant. The affine "
            "numerator separates into a constant plus eight boundary terms. "
            "A 4+4 meet-in-the-middle residue audit represents all "
            "sum_(h=22)^34 C(h-1,8)=52,157,326 normalized words and finds no "
            "D-divisibility hit. For a nontrivial positive odd cycle every "
            "state is at least three, so 1<=512(5/6)^h. The right side is "
            "strictly below one at h=35 and decreases thereafter."
        ),
        "boundary_formula_validation": formula_validation,
        "finite_exception_horizon_rows": finite_rows,
        "analytic_product_rows": analytic_rows,
        "analytic_bound": {
            "bound_at_h_35": fraction_payload(nine_one_product_bound(35)),
            "bound_at_h_34": fraction_payload(nine_one_product_bound(34)),
            "analytic_range_starts_at_h": 35,
            "bound_is_strictly_decreasing": True,
        },
        "aggregate": {
            "infinite_family_proved": True,
            "includes_imprimitive_words": True,
            "rotation_normalization_is_complete": True,
            "mitm_coverage_is_complete": True,
            "contracting_range_starts_at_h": 22,
            "analytic_range_starts_at_h": 35,
            "finite_exception_word_count": total_words,
            "finite_word_count_identity": "C(34,9)-C(21,9)=52157326",
            "right_tuple_count": sum(row["right_tuple_count"] for row in finite_rows),
            "divisibility_hits": sum(
                row["divisibility_hit_count"] for row in finite_rows
            ),
        },
        "no_go_scope": (
            "This closes only the exactly-nine-one/rest-two periodic stratum. "
            "Ten-or-more-one strata, valuations at least three, and aperiodic "
            "divergence remain open."
        ),
        "failure_count": failures,
    }


def weighted_odd_proper_prime_power_mass(
    metadata: list[tuple[int, int] | None], start: int, stop: int
) -> float:
    lower = max(2, start)
    upper = min(stop, len(metadata))
    return math.fsum(
        math.log(meta[0])
        for meta in metadata[lower:upper]
        if meta is not None and meta[1] >= 2 and meta[0] != 2
    )


def prime_base_compression_row(
    limit: int, metadata: list[tuple[int, int] | None]
) -> dict[str, object]:
    if limit < 4:
        raise ValueError("limit must be at least four")
    root = math.isqrt(limit)
    odd_primes = [
        value
        for value in range(3, root + 1)
        if metadata[value] == (value, 1)
    ]
    theta_odd = math.fsum(math.log(prime) for prime in odd_primes)
    actual_mass = weighted_odd_proper_prime_power_mass(
        metadata, 2, limit + 1
    )
    reconstructed_mass = 0.0
    for prime in odd_primes:
        value = prime * prime
        while value <= limit:
            reconstructed_mass += math.log(prime)
            if value > limit // prime:
                break
            value *= prime
    compressed_upper = len(odd_primes) * math.log(limit) - theta_odd
    elementary_upper = math.sqrt(limit) * math.log(limit)
    return {
        "limit_X": limit,
        "sqrt_floor": root,
        "odd_prime_base_count": len(odd_primes),
        "theta_odd_sqrt_X": theta_odd,
        "actual_odd_weighted_proper_power_mass": actual_mass,
        "reconstructed_odd_mass": reconstructed_mass,
        "prime_base_compressed_upper": compressed_upper,
        "elementary_sqrt_log_upper": elementary_upper,
        "checks": {
            "base_reconstruction_matches": abs(actual_mass - reconstructed_mass)
            < 1e-9,
            "actual_mass_below_compressed_upper": actual_mass
            <= compressed_upper + 1e-9,
            "compressed_upper_below_sqrt_log": compressed_upper
            <= elementary_upper + 1e-9,
        },
    }


def power_of_two_contamination(target: int) -> dict[str, object]:
    ordered_pairs: list[list[int]] = []
    for left_exponent in range(1, target.bit_length()):
        left = 2**left_exponent
        right = target - left
        if right < 2 or right & (right - 1):
            continue
        right_exponent = right.bit_length() - 1
        if max(left_exponent, right_exponent) >= 2:
            ordered_pairs.append([left_exponent, right_exponent])
    return {
        "ordered_exponent_pairs": ordered_pairs,
        "ordered_pair_count": len(ordered_pairs),
        "exact_weight": len(ordered_pairs) * math.log(2) ** 2,
        "at_most_two_ordered_pairs": len(ordered_pairs) <= 2,
    }


def goldbach_parity_envelope_audit() -> dict[str, object]:
    targets = [2**exponent for exponent in range(10, 21)]
    metadata = prime_power_metadata(max(targets) + 2)
    rows: list[dict[str, object]] = []
    for target in targets:
        decomposition = goldbach_prime_power_row(target, metadata)
        base = prime_base_compression_row(target, metadata)
        odd_mass = base["actual_odd_weighted_proper_power_mass"]
        powers_two = power_of_two_contamination(target)
        parity_envelope = (
            2.0 * math.log(target) * odd_mass + powers_two["exact_weight"]
        )
        compressed_envelope = (
            2.0
            * math.log(target)
            * base["prime_base_compressed_upper"]
            + powers_two["exact_weight"]
        )
        elementary_envelope = (
            2.0 * math.sqrt(target) * math.log(target) ** 2
            + 2.0 * math.log(2) ** 2
        )
        old_weighted_envelope = (
            2.0
            * math.log(target)
            * weighted_proper_prime_power_mass(metadata, 2, target + 1)
        )
        total = decomposition["weighted_total_convolution"]
        contamination = decomposition["weighted_prime_power_contamination"]
        rows.append(
            {
                "target_N": target,
                "actual_contamination": contamination,
                "odd_weighted_proper_power_mass": odd_mass,
                "power_of_two_contamination": powers_two,
                "parity_separated_envelope": parity_envelope,
                "prime_base_compressed_envelope": compressed_envelope,
                "elementary_envelope": elementary_envelope,
                "ticket192_weighted_envelope": old_weighted_envelope,
                "weighted_total_convolution": total,
                "base_compression": base,
                "checks": {
                    "actual_contamination_below_parity_envelope": contamination
                    <= parity_envelope + 1e-9,
                    "parity_envelope_below_ticket192_envelope": parity_envelope
                    <= old_weighted_envelope + 1e-9,
                    "parity_envelope_below_compressed_envelope": parity_envelope
                    <= compressed_envelope + 1e-9,
                    "compressed_envelope_below_elementary_envelope": compressed_envelope
                    <= elementary_envelope + 1e-9,
                    "finite_total_exceeds_parity_envelope": total
                    > parity_envelope,
                    "power_two_pair_classification_exact": powers_two[
                        "at_most_two_ordered_pairs"
                    ],
                },
            }
        )
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += sum(
        not check
        for row in rows
        for check in row["base_compression"]["checks"].values()
    )
    return {
        "theorem": (
            "For every even N>=6, let W_odd(N) sum log p over odd proper "
            "prime powers p^k<=N. Let C_2(N) be the exact von Mangoldt mass "
            "of ordered power-of-two pairs summing to N. Then the proper-"
            "prime-power contamination satisfies "
            "E_pp(N)<=2 log(N) W_odd(N)+C_2(N), where "
            "C_2(N)<=2(log 2)^2. Moreover, with y=floor(sqrt N), "
            "W_odd(N)<=(pi(y)-1)log N-(theta(y)-log 2)<=sqrt(N)log N."
        ),
        "proof": (
            "A supported pair summing to even N has equal parity. An even "
            "von Mangoldt-supported integer is a power of two, so all even "
            "contamination is exactly C_2(N); binary uniqueness gives at most "
            "two ordered exponent pairs. Every remaining contaminated pair "
            "has an odd proper prime power in one coordinate and is charged "
            "there with partner weight at most log N. For each odd prime "
            "p<=sqrt N, its exponents k=2,...,K contribute (K-1)log p, at "
            "most log N-log p. Summing by prime base gives the compressed "
            "Chebyshev-function bound."
        ),
        "parity_envelope_rows": rows,
        "aggregate": {
            "target_count": len(rows),
            "largest_target": targets[-1],
            "parity_separated_envelope_theorem_proved": True,
            "power_of_two_contamination_exactly_classified": True,
            "prime_base_compression_proved": True,
            "finite_sample_envelope_success_count": sum(
                row["checks"]["finite_total_exceeds_parity_envelope"]
                for row in rows
            ),
            "all_large_even_targets_proved": False,
        },
        "no_go_scope": (
            "Parity strictly lowers the sufficient contamination threshold, "
            "but the displayed finite successes do not prove correlation "
            "above it for every sufficiently large even N."
        ),
        "failure_count": failures,
    }


def twin_parity_envelope_audit() -> dict[str, object]:
    exponents = list(range(4, 20))
    limit = 2 ** (exponents[-1] + 1) + 2
    metadata = prime_power_metadata(limit)
    rows: list[dict[str, object]] = []
    for exponent in exponents:
        arithmetic = twin_shift_two_row(exponent, metadata)
        lower = 2**exponent
        upper = 2 * lower
        ceiling = upper + 2
        left_odd_mass = weighted_odd_proper_prime_power_mass(
            metadata, lower, upper
        )
        right_odd_mass = weighted_odd_proper_prime_power_mass(
            metadata, lower + 2, upper + 2
        )
        odd_local_envelope = math.log(ceiling) * (
            left_odd_mass + right_odd_mass
        )
        old_local_envelope = math.log(ceiling) * (
            weighted_proper_prime_power_mass(metadata, lower, upper)
            + weighted_proper_prime_power_mass(
                metadata, lower + 2, upper + 2
            )
        )
        base = prime_base_compression_row(ceiling, metadata)
        compressed_global_envelope = (
            2.0
            * math.log(ceiling)
            * base["prime_base_compressed_upper"]
        )
        elementary_envelope = (
            2.0 * math.sqrt(ceiling) * math.log(ceiling) ** 2
        )
        total = arithmetic["weighted_shift_two_correlation"]
        contamination = arithmetic["weighted_prime_power_contamination"]
        rows.append(
            {
                **arithmetic,
                "even_supported_shift_two_pair_count": 0,
                "left_odd_weighted_proper_power_mass": left_odd_mass,
                "right_odd_weighted_proper_power_mass": right_odd_mass,
                "odd_local_contamination_envelope": odd_local_envelope,
                "ticket192_local_weighted_envelope": old_local_envelope,
                "prime_base_compressed_global_envelope": compressed_global_envelope,
                "elementary_global_envelope": elementary_envelope,
                "base_compression": base,
                "checks": {
                    **arithmetic["checks"],
                    "no_even_supported_shift_pair_for_X_ge_4": lower >= 4,
                    "actual_contamination_below_odd_local_envelope": contamination
                    <= odd_local_envelope + 1e-9,
                    "odd_local_below_ticket192_envelope": odd_local_envelope
                    <= old_local_envelope + 1e-9,
                    "odd_local_below_compressed_global_envelope": odd_local_envelope
                    <= compressed_global_envelope + 1e-9,
                    "compressed_below_elementary_envelope": compressed_global_envelope
                    <= elementary_envelope + 1e-9,
                    "finite_total_exceeds_odd_local_envelope": total
                    > odd_local_envelope,
                },
            }
        )
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += sum(
        not check
        for row in rows
        for check in row["base_compression"]["checks"].values()
    )
    return {
        "theorem": (
            "For every X>=4, a von Mangoldt-supported pair n,n+2 with "
            "X<=n<2X is necessarily odd. Hence shift-two proper-prime-power "
            "contamination is at most log(2X+2) times the odd proper-power "
            "masses in [X,2X) and [X+2,2X+2). Correlation above this odd-only "
            "local envelope forces a twin prime in the block."
        ),
        "proof": (
            "If an even supported n occurs then n=2^a. Requiring n+2 to be "
            "even and von Mangoldt-supported gives 2^b-2^a=2. Factoring "
            "2^a(2^(b-a)-1)=2 shows a=1 and {n,n+2}={2,4}, impossible for "
            "X>=4. Thus every supported block pair is odd-odd, and charging "
            "contamination to the odd proper-power coordinate proves the "
            "local bound. Prime-base compression supplies an explicit global "
            "sqrt-scale majorant."
        ),
        "finite_dyadic_rows": rows,
        "aggregate": {
            "dyadic_block_count": len(rows),
            "largest_upper_endpoint": rows[-1]["block"][1],
            "odd_only_local_envelope_theorem_proved": True,
            "even_supported_pairs_excluded_for_all_X_ge_4": True,
            "prime_base_compression_proved": True,
            "finite_block_envelope_success_count": sum(
                row["checks"]["finite_total_exceeds_odd_local_envelope"]
                for row in rows
            ),
            "infinitely_many_envelope_successes_proved": False,
        },
        "no_go_scope": (
            "All displayed finite blocks pass the sharper odd-only envelope. "
            "No theorem proves this on infinitely many unbounded blocks, so "
            "the Twin Prime conjecture remains open."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_everywhere_extension_audit()
    collatz = collatz_nine_one_audit()
    goldbach = goldbach_parity_envelope_audit()
    twin = twin_parity_envelope_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-193",
            "theorem_name": "EverywherePointwiseQuadraticConvergenceForcesUniformBoundedExtension",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "Everywhere convergence of the actual pole-neutral Weil finite sections is not proved.",
            "route_decision": {
                "discard": "treating convergence on a merely dense countable core as enough for Banach-Steinhaus promotion",
                "retain": "prove pointwise convergence on every vector of one complete admissible Hilbert completion",
                "next_single_lemma": "PoleNeutralWeilFiniteSectionsConvergeOnEveryVectorOfACompleteAdmissibleHilbertCompletion",
            },
            "proof_dag": proof_dag(
                "RH",
                "UniformBoundedCoreExtensionAndPointwiseCauchyNoGo",
                "EverywherePointwiseQuadraticConvergenceForcesUniformBoundedExtension",
                "DenseCorePointwiseConvergenceInvokesUniformBoundedness",
                "PoleNeutralWeilFiniteSectionsConvergeOnEveryVectorOfACompleteAdmissibleHilbertCompletion",
            ),
            "claim_boundary": "No RH proof. The everywhere-convergence promotion theorem is exact, but its actual Weil premise remains open.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-193",
            "theorem_name": "ExactlyNineValuationOnesOtherwiseTwoCycleExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Ten-or-more-one strata, valuations at least three, and aperiodic divergence remain open.",
            "route_decision": {
                "discard": "pairwise enumeration of all 52,157,326 words after the affine numerator separates into eight boundary terms",
                "retain": "exact 4+4 residue coverage for h=22..34 and the product contradiction for h>=35",
                "next_single_lemma": "NoContractingValuationWordWithExactlyTenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "NoContractingValuationWordWithExactlyNineOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
                "ExactlyNineValuationOnesOtherwiseTwoCycleExclusion",
                "AllNineOneWordsMustBeTestedPairwise",
                "NoContractingValuationWordWithExactlyTenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            ),
            "claim_boundary": "No Collatz proof. The complete exactly-nine-one/rest-two periodic valuation stratum is excluded.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-193",
            "theorem_name": "ParitySeparatedPrimePowerContaminationEnvelope",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No every-large-even lower bound above the parity-separated envelope is proved.",
            "route_decision": {
                "discard": "charging every power of two by log(N) after even-even von Mangoldt support can be classified exactly",
                "retain": "binary correlation above 2 log(N) W_odd(N)+C_2(N) for every sufficiently large even N",
                "next_single_lemma": "BinaryCorrelationExceedsParitySeparatedPrimePowerEnvelopeForEveryLargeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "WeightedPrimePowerEnvelopeAndFactorTwoBudgetReduction",
                "ParitySeparatedPrimePowerContaminationEnvelope",
                "EvenPrimePowersRequireTheSameUnionBoundAsOddPrimePowers",
                "BinaryCorrelationExceedsParitySeparatedPrimePowerEnvelopeForEveryLargeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof. Parity strictly sharpens the sufficient contamination envelope, but the universal correlation lower bound is open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-193",
            "theorem_name": "OddOnlyShiftTwoContaminationEnvelope",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No proof gives correlation above the odd-only local envelope on infinitely many unbounded dyadic blocks.",
            "route_decision": {
                "discard": "including powers of two in shift-two contamination for blocks X>=4",
                "retain": "shift-two correlation above the two translated odd proper-power masses on infinitely many blocks",
                "next_single_lemma": "ShiftTwoCorrelationExceedsOddLocalWeightedEnvelopeOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "LocalTwoSidedWeightedEnvelopeBridge",
                "OddOnlyShiftTwoContaminationEnvelope",
                "EvenVonMangoldtSupportCanContaminateShiftTwoBlocksAboveFour",
                "ShiftTwoCorrelationExceedsOddLocalWeightedEnvelopeOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof. Even support is removed exactly and the odd-only local envelope passes finite replay, but infinitude is open.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureEverywhereNineOneParityEnvelopeAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-193 resolves none of the four conjectures. It closes the "
            "complete exactly-nine-one/rest-two accelerated Collatz cycle "
            "stratum, proves that everywhere pointwise convergence supplies "
            "the uniform form bound missing from the RH route, and removes "
            "even prime-power overcharging from the Goldbach and Twin Prime "
            "contamination envelopes."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The RH and prime-correlation tracks both replace an unnecessarily "
            "coarse premise by the correct global structure: completeness for "
            "uniform boundedness and parity for contamination. The Collatz "
            "track uses an exact low-rank boundary decomposition to replace "
            "pairwise search without weakening coverage."
        ),
        "literature_boundary": {
            "riemann": "The recent screw-function operator route still leaves the decisive limiting operator conjectural; no actual Weil everywhere-convergence theorem is imported here.",
            "collatz": "Recent accelerated-map work does not prove global convergence; this ticket excludes one periodic valuation stratum only.",
            "goldbach": "Exceptional-set results do not provide every-even-target binary correlation control above the new pointwise envelope.",
            "twin_prime": "Bounded-gap theorems do not force exact gap two; parity sharpening of contamination does not supply infinitely many positive blocks.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "new_infinite_cycle_stratum_closure_count": 1,
            "parity_sharpened_envelope_count": 2,
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
        ROOT / "data" / "open-problem" / "ticket193-everywhere-nineone-parity-envelope.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "everywhere_nineone_parity_envelope_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-193-everywhere-extension.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-193-nine-one-cycle-exclusion.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-193-parity-envelope.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-193-odd-local-envelope.json",
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    by_problem = {attempt["problem_id"]: attempt for attempt in attempts}
    for problem_id, path in paths.items():
        section = audit[section_keys[problem_id]]
        attempt = by_problem[problem_id]
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
            "TICKET-193 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
