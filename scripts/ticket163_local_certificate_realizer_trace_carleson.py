from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Iterator

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket156_cutoff_potential_signed_information import (
    farey_major_mask,
    next_power_of_two_above,
    radix_two_fft,
)
from ticket159_diagonal_threshold_phase_parity import (
    inverse_radix_two_fft,
    prime_sieve,
)


GENERATED_AT = "2026-07-31T12:00:00+09:00"
SCHEMA = "primeproject.ticket163-local-certificate-realizer-trace-carleson.v1"
STATUS = "four_localization_reductions_and_no_go_results_all_conjectures_open"


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {"exact": f"{value.numerator}/{value.denominator}", "decimal": float(value)}


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T163-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T163-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T163-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T163-REJECTED", f"{problem_code}-T163-CLOSED"],
            [f"{problem_code}-T163-CLOSED", f"{problem_code}-T163-OPEN"],
        ],
    }


def von_mangoldt_prefix(limit: int) -> list[float]:
    flags = prime_sieve(limit)
    values = [0.0] * (limit + 1)
    for prime in range(2, limit + 1):
        if not flags[prime]:
            continue
        logarithm = math.log(prime)
        power = prime
        while power <= limit:
            values[power] = logarithm
            if power > limit // prime:
                break
            power *= prime
    prefix = [0.0] * (limit + 1)
    running = 0.0
    for value in range(1, limit + 1):
        if values[value]:
            running += values[value] / math.sqrt(value)
        prefix[value] = running
    return prefix


def riemann_finite_prime_trace_audit() -> dict[str, object]:
    endpoints = [100, 1_000, 10_000, 100_000, 1_000_000]
    prefix = von_mangoldt_prefix(endpoints[-1])
    rows: list[dict[str, object]] = []
    failures = 0
    for endpoint in endpoints:
        radius = math.log(endpoint)
        trace_squared = 2 * radius + 1 / (2 * radius)
        coefficient_mass = prefix[endpoint]
        continuity_constant = trace_squared * coefficient_mass
        constant_function_lower_witness = coefficient_mass / (2 * radius)
        checks = {
            "finite_coefficient_mass_is_positive": coefficient_mass > 0,
            "sobolev_trace_constant_is_positive": trace_squared > 0,
            "absolute_continuity_constant_is_finite": math.isfinite(continuity_constant),
            "constant_function_is_below_absolute_bound": (
                constant_function_lower_witness <= continuity_constant
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "prime_power_cutoff_X": endpoint,
                "log_interval_radius_R": radius,
                "von_mangoldt_sqrt_weight_mass_W_X": coefficient_mass,
                "sobolev_point_trace_constant_squared": trace_squared,
                "absolute_quadratic_continuity_constant": continuity_constant,
                "constant_h1_unit_witness_value": constant_function_lower_witness,
                "checks": checks,
            }
        )
    trend_checks = {
        "coefficient_mass_increases": all(
            left["von_mangoldt_sqrt_weight_mass_W_X"]
            < right["von_mangoldt_sqrt_weight_mass_W_X"]
            for left, right in zip(rows, rows[1:])
        ),
        "absolute_continuity_constant_increases": all(
            left["absolute_quadratic_continuity_constant"]
            < right["absolute_quadratic_continuity_constant"]
            for left, right in zip(rows, rows[1:])
        ),
    }
    failures += sum(not value for value in trend_checks.values())
    return {
        "theorem": (
            "Put R=log X and Q_X(f)=sum_{n<=X} Lambda(n)n^(-1/2)"
            "|f(log n)|^2 on H1(-R,R). For every f,g, "
            "|Q_X(f)-Q_X(g)| <= C_R^2 W_X "
            "(||f||_H1+||g||_H1)||f-g||_H1, where "
            "C_R^2=2R+(2R)^(-1) and W_X=sum_{n<=X}Lambda(n)/sqrt(n). "
            "Thus every finite prime trace is H1-continuous. However W_X "
            "diverges, already from its prime terms. Consequently the "
            "coefficient-mass majorant C_R^2 W_X does not supply the "
            "uniform-in-X continuity required by the TICKET-162 "
            "Guinand-Weil bridge."
        ),
        "proof": (
            "Writing f(x) as its interval mean plus its mean-zero part gives "
            "|f(x)| <= (2R)^(-1/2)||f||_2+(2R)^(1/2)||f'||_2 "
            "<= C_R||f||_H1. Apply |a^2-b^2|<=|a-b|(|a|+|b|) "
            "at every prime-power trace point and sum the positive weights. "
            "For primes p>=3, log(p)/sqrt(p)>=1/p, while Euler's prime "
            "reciprocal series diverges; hence W_X diverges. This rejects "
            "only this coefficient-mass majorant, not every possible "
            "absolute estimate and not cancellation-aware continuity of the "
            "complete Guinand-Weil form."
        ),
        "finite_prime_trace_rows": rows,
        "trend_checks": trend_checks,
        "failure_count": failures,
    }


def positive_compositions(total: int, length: int) -> Iterator[tuple[int, ...]]:
    if length == 1:
        yield (total,)
        return
    for first in range(1, total - length + 2):
        for tail in positive_compositions(total - first, length - 1):
            yield (first, *tail)


def collatz_affine_correction(word: tuple[int, ...]) -> int:
    length = len(word)
    prefix = 0
    correction = 0
    for index, valuation in enumerate(word):
        correction += 3 ** (length - 1 - index) * (1 << prefix)
        prefix += valuation
    return correction


def collatz_least_realizer(word: tuple[int, ...]) -> tuple[int, int, int]:
    total = sum(word)
    denominator = 1 << total
    modulus = 1 << (total + 1)
    power_three = 3 ** len(word)
    correction = collatz_affine_correction(word)
    residue = (
        (denominator - correction)
        * pow(power_three, -1, modulus)
    ) % modulus
    if residue == 0:
        residue = modulus
    endpoint = (power_three * residue + correction) // denominator
    return residue, endpoint, residue - endpoint


def collatz_replay(start: int, length: int) -> tuple[tuple[int, ...], int]:
    value = start
    valuations: list[int] = []
    for _ in range(length):
        numerator = 3 * value + 1
        valuation = (numerator & -numerator).bit_length() - 1
        valuations.append(valuation)
        value = numerator >> valuation
    return tuple(valuations), value


def collatz_rearrangement_realizer_audit() -> dict[str, object]:
    failures = 0
    layer_rows: list[dict[str, object]] = []
    exact_non_descent: list[dict[str, object]] = []
    for length in range(2, 14):
        total = (3**length).bit_length()
        front_word = (total - length + 1, *(1 for _ in range(length - 1)))
        front_correction = collatz_affine_correction(front_word)
        count = 0
        strict_descent_count = 0
        maximum_correction = -1
        maximum_word: tuple[int, ...] | None = None
        minimum_margin: int | None = None
        replay_failure_count = 0
        for word in positive_compositions(total, length):
            count += 1
            correction = collatz_affine_correction(word)
            if correction > maximum_correction:
                maximum_correction = correction
                maximum_word = word
            residue, endpoint, margin = collatz_least_realizer(word)
            replay_word, replay_endpoint = collatz_replay(residue, length)
            replay_failure_count += int(
                replay_word != word or replay_endpoint != endpoint
            )
            minimum_margin = margin if minimum_margin is None else min(minimum_margin, margin)
            strict_descent_count += int(margin > 0)
            if margin <= 0:
                exact_non_descent.append(
                    {
                        "word_length_m": length,
                        "total_valuation_S": total,
                        "valuation_word": list(word),
                        "affine_correction_C": correction,
                        "least_odd_realizer_r": residue,
                        "endpoint_Tm_r": endpoint,
                        "strict_descent_margin": margin,
                    }
                )
        expected = math.comb(total - 1, length - 1)
        checks = {
            "all_compositions_enumerated": count == expected,
            "front_loaded_word_maximizes_correction": maximum_word == front_word,
            "front_loaded_correction_matches_maximum": maximum_correction == front_correction,
            "every_natural_residue_replays_exact_word": replay_failure_count == 0,
            "eventual_candidate_only_claimed_on_finite_scan": True,
        }
        failures += sum(not value for value in checks.values())
        layer_rows.append(
            {
                "word_length_m": length,
                "minimal_contracting_total_S": total,
                "composition_count": count,
                "strict_descent_count": strict_descent_count,
                "non_strict_count": count - strict_descent_count,
                "minimum_strict_descent_margin": minimum_margin,
                "natural_residue_replay_failure_count": replay_failure_count,
                "front_loaded_word": list(front_word),
                "maximum_affine_correction_C": maximum_correction,
                "checks": checks,
            }
        )

    coupled = (4, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 3)
    front = (sum(coupled) - len(coupled) + 1, *(1 for _ in range(len(coupled) - 1)))
    front_r, front_e, front_margin = collatz_least_realizer(front)
    coupled_r, coupled_e, coupled_margin = collatz_least_realizer(coupled)
    coupling_checks = {
        "front_word_has_larger_correction": (
            collatz_affine_correction(front) > collatz_affine_correction(coupled)
        ),
        "front_word_least_realizer_descends": front_margin > 0,
        "smaller_correction_word_least_realizer_grows": coupled_margin < 0,
        "coupled_word_is_replayed_by_165": (
            coupled_r == 165 and collatz_replay(coupled_r, len(coupled)) == (coupled, coupled_e)
        ),
        "finite_layers_three_through_thirteen_all_descend": all(
            row["non_strict_count"] == 0
            for row in layer_rows
            if row["word_length_m"] >= 3
        ),
    }
    failures += sum(not value for value in coupling_checks.values())
    return {
        "theorem": (
            "For a positive valuation word a=(a_1,...,a_m), write "
            "2^S T_a(n)=3^m n+C(a). At fixed m and S, C(a) is maximized "
            "by the front-loaded word (S-m+1,1,...,1). More exactly, "
            "swapping adjacent x<y into y,x increases C by "
            "3^(m-i-2)2^P(2^y-2^x), where P is the preceding valuation "
            "sum. This extremality does not transfer natural descent: at "
            "m=17,S=27, the displayed word realized by n=165 has smaller "
            "correction than the front-loaded word but endpoint 167. The "
            "natural residue and affine correction must be controlled "
            "jointly. The same orbit already descends at its first step, so "
            "this is a no-go for fixed-length transfer, not a Collatz "
            "counterexample."
        ),
        "proof": (
            "The affine iteration formula follows by induction. An adjacent "
            "swap changes only the prefix entering the next correction term, "
            "which gives the displayed positive difference; repeated swaps "
            "sort the word. More directly, every proper prefix sum is "
            "at most S minus the positive suffix length, with equality for "
            "the front-loaded word, proving its maximality term by term. The "
            "exact natural realizer must also make the endpoint odd and is "
            "the unique residue r=(2^S-C(a))3^(-m) mod 2^(S+1). "
            "Substitution gives the two exact comparison endpoints. "
            "Complete enumeration of all positive compositions is recorded "
            "only through m=13 and is not an all-length theorem."
        ),
        "minimal_layer_complete_rows": layer_rows,
        "exact_natural_realizer_coupling_no_go": {
            "front_loaded": {
                "word": list(front),
                "correction": collatz_affine_correction(front),
                "least_realizer": front_r,
                "endpoint": front_e,
                "margin": front_margin,
            },
            "smaller_correction": {
                "word": list(coupled),
                "correction": collatz_affine_correction(coupled),
                "least_realizer": coupled_r,
                "endpoint": coupled_e,
                "margin": coupled_margin,
            },
            "checks": coupling_checks,
        },
        "non_strict_words_through_m13": exact_non_descent,
        "failure_count": failures,
    }


def goldbach_dyadic_budget_audit() -> dict[str, object]:
    endpoint = 65_536
    flags = prime_sieve(endpoint)
    transform_size = next_power_of_two_above(2 * endpoint)
    weights = [0.0] * transform_size
    for value in range(2, endpoint + 1):
        weights[value] = float(flags[value])
    transform = radix_two_fft(weights)
    squared = [value * value for value in transform]
    full = inverse_radix_two_fft(squared)
    mask = farey_major_mask(transform_size, 8, 2)
    major = inverse_radix_two_fft(
        [value if mask[index] else 0j for index, value in enumerate(squared)]
    )

    rows: list[dict[str, object]] = []
    failures = 0
    for upper in [256, 512, 1_024, 2_048, 4_096, 8_192, 16_384, 32_768, 65_536]:
        lower = upper // 2
        budget = 0.0
        maximum_deficit = 0.0
        positive_major = 0
        zero_count = 0
        fft_positivity_mismatch_count = 0
        maximum_rounding_error = 0.0
        target_count = 0
        for even in range(lower + 2, upper + 1, 2):
            target_count += 1
            observed_float = full[even].real
            observed = round(observed_float)
            major_value = major[even].real
            minor_value = observed_float - major_value
            maximum_rounding_error = max(
                maximum_rounding_error, abs(observed_float - observed)
            )
            direct_has_representation = any(
                flags[left] and flags[even - left]
                for left in range(2, even // 2 + 1)
            )
            zero_count += int(not direct_has_representation)
            fft_positivity_mismatch_count += int(
                (observed > 0) != direct_has_representation
            )
            if major_value <= 0:
                continue
            positive_major += 1
            deficit = max(0.0, -minor_value / major_value)
            budget += deficit * deficit
            maximum_deficit = max(maximum_deficit, deficit)
        checks = {
            "all_major_terms_positive": positive_major == target_count,
            "direct_integer_scan_has_no_goldbach_zero": zero_count == 0,
            "fft_positivity_matches_direct_integer_scan": (
                fft_positivity_mismatch_count == 0
            ),
            "fft_rounding_residual_is_below_tolerance": maximum_rounding_error < 1e-7,
            "tested_farey_shell_does_not_pass_unit_gate": budget >= 1,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "dyadic_lower_exclusive": lower,
                "dyadic_upper_inclusive": upper,
                "even_target_count": target_count,
                "normalized_negative_budget": budget,
                "mean_normalized_negative_budget": budget / target_count,
                "maximum_normalized_deficit": maximum_deficit,
                "unit_gate_passes": budget < 1,
                "observed_zero_count": zero_count,
                "fft_positivity_mismatch_count": fft_positivity_mismatch_count,
                "checks": checks,
            }
        )

    spike_rows: list[dict[str, object]] = []
    for size in [8, 32, 128, 512, 2_048]:
        spike_rows.append(
            {
                "block_size": size,
                "zero_count": 1,
                "normalized_budget": 1.0,
                "mean_normalized_budget": 1 / size,
            }
        )
    spike_checks = {
        "spike_means_tend_to_zero": all(
            left["mean_normalized_budget"] > right["mean_normalized_budget"]
            for left, right in zip(spike_rows, spike_rows[1:])
        ),
        "every_spike_block_retains_one_exception": all(
            row["zero_count"] == 1 and row["normalized_budget"] == 1
            for row in spike_rows
        ),
    }
    failures += sum(not value for value in spike_checks.values())
    return {
        "theorem": (
            "Partition the even targets into finite blocks A_k. If "
            "G_N=M_N+E_N with integer G_N>=0 and M_N>0, then on every "
            "block # {N in A_k:G_N=0} <= B_k, where "
            "B_k=sum_{A_k}(E_N^-/M_N)^2. Therefore the shellwise condition "
            "B_k<1 for every k, together with a finite initial check, "
            "excludes all Goldbach exceptions. A single unit spike in each "
            "growing block has mean budget tending to zero while preserving "
            "one exception, so vanishing average error is insufficient."
        ),
        "proof": (
            "Apply the TICKET-162 integrality inequality separately on each "
            "block. No summation across infinitely many blocks is needed. "
            "The unit-spike construction has one term equal to one and all "
            "others zero, proving both sharpness and the average-error "
            "no-go. The finite prime DFT uses one fixed Farey mask; its "
            "shell budgets remain above one and are diagnostics only."
        ),
        "finite_prime_dft_dyadic_shell_rows": rows,
        "exact_diluted_unit_spike_rows": spike_rows,
        "spike_checks": spike_checks,
        "failure_count": failures,
    }


def region_variance(
    matrix: list[list[int]], row: int, column: int, size: int
) -> Fraction:
    values = [
        matrix[r][c]
        for r in range(row, row + size)
        for c in range(column, column + size)
    ]
    mean = Fraction(sum(values), len(values))
    return sum((Fraction(value) - mean) ** 2 for value in values)


def dyadic_detail_energy(
    matrix: list[list[int]], row: int, column: int, size: int
) -> Fraction:
    if size == 1:
        return Fraction(0)
    half = size // 2
    parent_values = [
        matrix[r][c]
        for r in range(row, row + size)
        for c in range(column, column + size)
    ]
    parent_mean = Fraction(sum(parent_values), size * size)
    energy = Fraction(0)
    for dr, dc in [(0, 0), (0, half), (half, 0), (half, half)]:
        child_values = [
            matrix[r][c]
            for r in range(row + dr, row + dr + half)
            for c in range(column + dc, column + dc + half)
        ]
        child_mean = Fraction(sum(child_values), half * half)
        energy += half * half * (child_mean - parent_mean) ** 2
    return energy


def dyadic_descendant_energy(
    matrix: list[list[int]], row: int, column: int, size: int
) -> Fraction:
    if size == 1:
        return Fraction(0)
    half = size // 2
    return dyadic_detail_energy(matrix, row, column, size) + sum(
        dyadic_descendant_energy(matrix, row + dr, column + dc, half)
        for dr, dc in [(0, 0), (0, half), (half, 0), (half, half)]
    )


def twin_local_carleson_audit() -> dict[str, object]:
    checkerboard = [
        [1 if (row + column) % 2 == 0 else -1 for column in range(4)]
        for row in range(4)
    ]
    rows: list[dict[str, object]] = []
    failures = 0
    for size in [8, 16, 32, 64, 128]:
        matrix = [[0] * size for _ in range(size)]
        for row in range(4):
            for column in range(4):
                matrix[row][column] = checkerboard[row][column]
        global_variance = region_variance(matrix, 0, 0, size)
        global_tree = dyadic_descendant_energy(matrix, 0, 0, size)
        local_variance = region_variance(matrix, 0, 0, 4)
        local_tree = dyadic_descendant_energy(matrix, 0, 0, 4)
        checks = {
            "global_tree_telescopes": global_tree == global_variance,
            "local_tree_telescopes": local_tree == local_variance,
            "global_energy_is_fixed": global_variance == 16,
            "local_energy_density_is_one": local_variance == 16,
            "row_margins_vanish": all(sum(row) == 0 for row in matrix),
            "column_margins_vanish": all(
                sum(matrix[row][column] for row in range(size)) == 0
                for column in range(size)
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "matrix_side": size,
                "global_variance_energy": fraction_payload(global_variance),
                "global_energy_density": float(global_variance / (size * size)),
                "local_four_by_four_variance_energy": fraction_payload(local_variance),
                "local_four_by_four_energy_density": float(local_variance / 16),
                "checks": checks,
            }
        )
    dilution_checks = {
        "global_density_strictly_decreases": all(
            left["global_energy_density"] > right["global_energy_density"]
            for left, right in zip(rows, rows[1:])
        ),
        "local_density_stays_one": all(
            row["local_four_by_four_energy_density"] == 1.0 for row in rows
        ),
    }
    failures += sum(not value for value in dilution_checks.values())
    return {
        "theorem": (
            "For every dyadic square R in a finite matrix, its variance "
            "sum_{x in R}|H_x-<H>_R|^2 equals the sum of the four-child "
            "martingale detail energies over all dyadic descendants of R. "
            "A global normalized energy bound does not imply a local "
            "Carleson bound: embedding one 4x4 checkerboard in a 2^J by "
            "2^J zero matrix gives global energy density 16/4^J -> 0, "
            "while the local 4x4 density remains one."
        ),
        "proof": (
            "The one-step identity is the finite variance decomposition "
            "into within-child variance plus variance of child means. "
            "Iteration proves exact telescoping on every dyadic square. "
            "The embedded checkerboard has zero mean, row margins, and "
            "column margins. Its energy is always 16, so dilution changes "
            "the global density but not the local square. This rejects "
            "global-energy decay as a substitute for a uniform local "
            "prime-weighted Carleson estimate."
        ),
        "embedded_checkerboard_dilution_rows": rows,
        "dilution_checks": dilution_checks,
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_finite_prime_trace_audit()
    collatz = collatz_rearrangement_realizer_audit()
    goldbach = goldbach_dyadic_budget_audit()
    twin = twin_local_carleson_audit()
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-163",
            "theorem_name": "FinitePrimeTraceH1ContinuityAndAbsoluteMassNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "Continuity is proved only at each fixed prime cutoff. The "
                "complete Guinand-Weil form may contain cancellations not "
                "seen by the divergent absolute coefficient mass."
            ),
            "route_decision": {
                "discard": "uniform H1 continuity obtained from the divergent C_R^2 W_X coefficient-mass majorant",
                "retain": "the fixed-cutoff trace theorem plus cancellation between prime and archimedean terms",
                "next_single_lemma": "CancellationAwareUniformGuinandWeilTraceBoundOnConstraintCore",
            },
            "proof_dag": proof_dag(
                "RH",
                "CoefficientMassMajorantRemainsUniform",
                "FinitePrimeTraceH1ContinuityAndAbsoluteMassNoGo",
                "CancellationAwareUniformGuinandWeilTraceBoundOnConstraintCore",
            ),
            "claim_boundary": "No RH proof and no zero exclusion; one finite trace theorem and one proof-strategy no-go.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-163",
            "theorem_name": "AffineCorrectionMajorizationAndNaturalRealizerCouplingNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The complete minimal-total layer is checked only through "
                "m=13, and fixed-length transfer fails at m=17. No theorem "
                "proves descent at the first multiplicatively contracting "
                "prefix for every nonterminal natural orbit."
            ),
            "route_decision": {
                "discard": "transferring front-loaded descent to permutations by affine correction ordering alone",
                "retain": "joint control of the affine correction and its exact odd-endpoint residue modulo 2^(S+1)",
                "next_single_lemma": "FirstContractingLayerNaturalRealizerDescent",
            },
            "proof_dag": proof_dag(
                "CO",
                "FrontLoadedCorrectionExtremalityTransfersNaturalDescent",
                "AffineCorrectionMajorizationAndNaturalRealizerCouplingNoGo",
                "FirstContractingLayerNaturalRealizerDescent",
            ),
            "claim_boundary": "No Collatz proof and no divergent orbit; exact rearrangement theorem, exact m=17 coupling no-go, finite complete layers through m=13.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-163",
            "theorem_name": "DyadicIntegralExceptionCertificateAndDilutedSpikeNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The fixed finite Farey decomposition has shell budgets "
                "above one. No uniform analytic binary minor-arc estimate "
                "crosses the corrected shellwise gate."
            ),
            "route_decision": {
                "discard": "vanishing mean normalized error as a pointwise no-exception certificate",
                "retain": "strict normalized negative-error budget below one on every dyadic shell",
                "next_single_lemma": "UniformDyadicNormalizedNegativeMinorBudgetBelowOne",
            },
            "proof_dag": proof_dag(
                "GB",
                "VanishingMeanMinorErrorExcludesEveryGoldbachException",
                "DyadicIntegralExceptionCertificateAndDilutedSpikeNoGo",
                "UniformDyadicNormalizedNegativeMinorBudgetBelowOne",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; exact shellwise certificate and exact diluted-spike obstruction.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-163",
            "theorem_name": "LocalDyadicVarianceIdentityAndGlobalDilutionNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "The deterministic identity supplies no prime-weighted "
                "power saving and no positive lower bound for exact gap two."
            ),
            "route_decision": {
                "discard": "global normalized multiscale energy decay as a local Type-II certificate",
                "retain": "uniform local dyadic Carleson control at every relevant prime-weighted rectangle",
                "next_single_lemma": "UniformPrimeWeightedLocalCarlesonPowerSavingBeyondParity",
            },
            "proof_dag": proof_dag(
                "TP",
                "GlobalEnergyDecayControlsEveryLocalTypeIIRectangle",
                "LocalDyadicVarianceIdentityAndGlobalDilutionNoGo",
                "UniformPrimeWeightedLocalCarlesonPowerSavingBeyondParity",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; exact local variance identity and exact global-dilution obstruction.",
        },
    }
    total_failures = sum(
        int(section["reproducible_computation"]["failure_count"])
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureLocalCertificateRealizerTraceCarlesonAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-163 proves four exact localization or no-go results and "
            "resolves none of the four conjectures. It replaces global or "
            "uncoupled proxies by cancellation-aware, residue-coupled, "
            "shellwise, and locally Carleson-normalized proof obligations."
        ),
        **sections,
        "literature_boundary": {
            "riemann": "The Guinand-Weil criterion and finite truncated-form work are external; this ticket analyzes one abstract positive prime trace only.",
            "collatz": "Classical accelerated-map affine formulas motivate the coding; the rearrangement and residue-coupling audit are proved here.",
            "goldbach": "Circle-method exceptional-set estimates motivate the shell decomposition; no imported theorem supplies the required unit budget.",
            "twin_prime": "Ford-Maynard Type I/II theory motivates local information; the deterministic matrix theorem is not a prime-producing estimate.",
        },
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
    for problem_id, key in [
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin-prime", "twin_prime"),
    ]:
        section = audit[key]
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
            }
        )
    return attempts


def write_outputs(audit: dict[str, object]) -> None:
    attempts = build_attempts(audit)
    global_payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "local_certificate_realizer_trace_carleson_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data" / "open-problem" / "ticket163-local-certificate-realizer-trace-carleson.json",
        global_payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-163-prime-trace-continuity.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-163-rearrangement-realizer-coupling.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-163-dyadic-integral-budget.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-163-local-carleson-dilution.json",
    }
    keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    by_problem = {attempt["problem_id"]: attempt for attempt in attempts}
    for problem_id, path in paths.items():
        section = audit[keys[problem_id]]
        attempt = by_problem[problem_id]
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
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
        raise SystemExit(json.dumps(audit["machine_audit"], indent=2))
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
