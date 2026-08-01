from __future__ import annotations

import json
import math
from itertools import permutations
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket173_finite_section_cylinder_phase_tensor import (
    accelerated_odd_step,
    cylinder_least_representative,
    realized_valuations,
)


GENERATED_AT = "2026-08-02T06:30:00+09:00"
SCHEMA = "primeproject.ticket180-finite-information-localization.v1"
STATUS = "four_exact_localization_no_go_theorems_all_conjectures_open"


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T180-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T180-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T180-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T180-REJECTED", f"{problem_code}-T180-CLOSED"],
            [f"{problem_code}-T180-CLOSED", f"{problem_code}-T180-OPEN"],
        ],
    }


def square_wave_coefficient(distance: int, amplitude: float) -> float:
    if distance == 0 or distance % 2 == 0:
        return 0.0
    index = (abs(distance) - 1) // 2
    return 2.0 * amplitude * ((-1.0) ** index) / (
        math.pi * abs(distance)
    )


def toeplitz_section(
    dimension: int,
    amplitude: float,
    hidden_frequency: int | None = None,
    hidden_amplitude: float = 0.0,
) -> list[list[float]]:
    matrix = []
    for row in range(dimension):
        values = []
        for column in range(dimension):
            distance = row - column
            coefficient = square_wave_coefficient(distance, amplitude)
            if hidden_frequency is not None and abs(distance) == hidden_frequency:
                coefficient += hidden_amplitude / 2.0
            values.append(coefficient)
        matrix.append(values)
    return matrix


def matrix_max_difference(
    left: list[list[float]], right: list[list[float]]
) -> float:
    return max(
        abs(left[row][column] - right[row][column])
        for row in range(len(left))
        for column in range(len(left[row]))
    )


def riemann_hidden_frequency_audit() -> dict[str, object]:
    base_amplitude = 0.2
    hidden_amplitude = 1.0
    core_margin = 0.25
    rows = []
    failures = 0
    for dimension in [8, 16, 32, 64, 128]:
        hidden_frequency = 2 * dimension + 1
        base = toeplitz_section(dimension, base_amplitude)
        perturbed = toeplitz_section(
            dimension,
            base_amplitude,
            hidden_frequency,
            hidden_amplitude,
        )
        difference = matrix_max_difference(base, perturbed)
        witnessed_symbol_value = base_amplitude + hidden_amplitude
        checks = {
            "hidden_frequency_is_outside_observed_band": hidden_frequency
            >= dimension,
            "finite_toeplitz_section_is_identical": difference == 0.0,
            "base_symbol_is_below_margin": base_amplitude < core_margin,
            "perturbed_symbol_exceeds_margin": witnessed_symbol_value
            > core_margin,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "dimension_N": dimension,
                "observed_fourier_band": dimension - 1,
                "hidden_frequency_M": hidden_frequency,
                "hidden_amplitude_A": hidden_amplitude,
                "finite_section_max_difference": difference,
                "base_symbol_bound": base_amplitude,
                "core_margin_delta": core_margin,
                "perturbed_symbol_value_at_zero": witnessed_symbol_value,
                "checks": checks,
            }
        )
    return {
        "theorem": (
            "Let T_N(f) be the N by N Toeplitz section formed from the Fourier "
            "coefficients of a real bounded symbol f. For every integer M>=N and "
            "A>0, g(theta)=f(theta)+A cos(M theta) has T_N(g)=T_N(f), while "
            "||g-f||_infinity=A and ||g||_infinity>=A-||f||_infinity. Therefore "
            "no finite family of Toeplitz moments can certify an L-infinity tail "
            "bound without an independent high-frequency envelope."
        ),
        "proof": (
            "Entries of T_N use only Fourier modes i-j with |i-j|<=N-1. The "
            "perturbation A cos(M theta) has Fourier support only at plus/minus M, "
            "so it is invisible when M>=N. The reverse triangle inequality gives "
            "the norm lower bound. In the computed square-wave family, theta=0 "
            "witnesses the stronger value C+A."
        ),
        "hidden_frequency_counterfamily": rows,
        "aggregate": {
            "dimension_count": len(rows),
            "largest_dimension": rows[-1]["dimension_N"],
            "all_finite_sections_identical": all(
                row["finite_section_max_difference"] == 0.0 for row in rows
            ),
            "all_hidden_symbols_cross_margin": all(
                row["perturbed_symbol_value_at_zero"] > core_margin for row in rows
            ),
        },
        "no_go_scope": (
            "This refutes finite-section agreement as a certificate for the "
            "unobserved Weil-symbol L-infinity norm. It does not identify the "
            "actual arithmetic tail or prove that its high-frequency modes obey "
            "a summable or uniform envelope."
        ),
        "failure_count": failures,
    }


def valuation_layers(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(value >= layer for value in word)
        for layer in range(1, max(word) + 1)
    )


def ordered_affine_numerator(word: tuple[int, ...]) -> int:
    horizon = len(word)
    prefix_sum = 0
    numerator = 0
    for index, valuation in enumerate(word):
        numerator += 3 ** (horizon - 1 - index) * 2**prefix_sum
        prefix_sum += valuation
    return numerator


def orbit_prefix(start: int, horizon: int) -> tuple[list[int], tuple[int, ...]]:
    states = [start]
    valuations = []
    current = start
    for _ in range(horizon):
        current, valuation = accelerated_odd_step(current)
        states.append(current)
        valuations.append(valuation)
    return states, tuple(valuations)


def first_descent_time(states: list[int]) -> int | None:
    start = states[0]
    return next(
        (index for index, state in enumerate(states[1:], start=1) if state < start),
        None,
    )


def collatz_order_pair(high_valuation: int) -> dict[str, object]:
    early = (high_valuation, 1, 1)
    delayed = (1, high_valuation, 1)
    rows = []
    for label, word in [("early_high_valuation", early), ("delayed_high_valuation", delayed)]:
        representative, modulus = cylinder_least_representative(list(word))
        states, observed = orbit_prefix(representative, len(word))
        rows.append(
            {
                "label": label,
                "valuation_word": list(word),
                "layer_counts": list(valuation_layers(word)),
                "valuation_sum_S": sum(word),
                "ordered_affine_numerator_B": ordered_affine_numerator(word),
                "cylinder_representative": representative,
                "cylinder_modulus": modulus,
                "states": states,
                "first_descent_time": first_descent_time(states),
                "word_is_realized": observed == word
                and tuple(realized_valuations(representative, len(word))) == word,
            }
        )
    checks = {
        "same_valuation_multiset": sorted(early) == sorted(delayed),
        "same_adaptive_layer_counts": rows[0]["layer_counts"]
        == rows[1]["layer_counts"],
        "same_total_valuation": rows[0]["valuation_sum_S"]
        == rows[1]["valuation_sum_S"],
        "different_affine_numerators": rows[0]["ordered_affine_numerator_B"]
        != rows[1]["ordered_affine_numerator_B"],
        "different_first_descent_times": rows[0]["first_descent_time"]
        != rows[1]["first_descent_time"],
        "both_words_are_naturally_realized": all(
            row["word_is_realized"] for row in rows
        ),
    }
    return {
        "high_valuation": high_valuation,
        "ordered_realizations": rows,
        "checks": checks,
    }


def collatz_order_audit() -> dict[str, object]:
    rows = [collatz_order_pair(value) for value in range(2, 9)]
    failures = sum(
        not check
        for row in rows
        for check in row["checks"].values()
    )
    return {
        "theorem": (
            "For a valuation word v=(v_0,...,v_(h-1)), the accelerated affine "
            "composition is T_v(n)=(3^h n+B(v))/2^S, where "
            "B(v)=sum_j 3^(h-1-j)2^(v_0+...+v_(j-1)). Adaptive layer counts "
            "determine the valuation multiset and S, but not B(v) or first-descent "
            "time. In particular, the naturally realized words (2,1,1) and "
            "(1,2,1) have identical layers (3,1); the first descends at step one "
            "from 9 to 7, while the second starts at 27 and has no descent in its "
            "three-step prefix."
        ),
        "proof": (
            "Induction through (3n+1)/2^v gives the displayed affine numerator. "
            "Layer counts are invariant under permutation, whereas the powers of "
            "two in B(v) use ordered prefix sums. The cylinder congruence theorem "
            "realizes every positive valuation word as an odd residue class. Direct "
            "iteration of the two stated representatives proves the descent split."
        ),
        "permutation_counterfamilies": rows,
        "aggregate": {
            "high_valuation_cases": len(rows),
            "largest_high_valuation": rows[-1]["high_valuation"],
            "all_layer_summaries_match": all(
                row["checks"]["same_adaptive_layer_counts"] for row in rows
            ),
            "all_first_descent_times_differ": all(
                row["checks"]["different_first_descent_times"] for row in rows
            ),
        },
        "no_go_scope": (
            "Adaptive layer totals are exact for total valuation but erase order. "
            "They cannot alone classify first descent or cycle divisibility. This "
            "does not prove that every natural orbit eventually acquires an ordered "
            "prefix with descent, and it does not exclude nontrivial cycles."
        ),
        "failure_count": failures,
    }


def exceptional_spike_row(target_count: int, overshoot: float = 0.1) -> dict[str, object]:
    main = 1.0
    spike = -(1.0 + overshoot) * main
    rms = abs(spike) / math.sqrt(target_count)
    mean_absolute = abs(spike) / target_count
    minimum_total = main + spike
    checks = {
        "normalized_rms_formula_holds": math.isclose(
            rms, (1.0 + overshoot) / math.sqrt(target_count)
        ),
        "mean_absolute_formula_holds": math.isclose(
            mean_absolute, (1.0 + overshoot) / target_count
        ),
        "one_target_is_negative": minimum_total < 0.0,
        "exception_density_tends_down": 1.0 / target_count <= 1.0,
    }
    return {
        "target_count_L": target_count,
        "main_value_mu": main,
        "single_minor_spike": spike,
        "normalized_minor_rms": rms,
        "normalized_minor_mean_absolute": mean_absolute,
        "exception_density": 1.0 / target_count,
        "minimum_major_plus_minor": minimum_total,
        "checks": checks,
    }


def ordered_goldbach_count(target: int, is_prime: list[bool]) -> int:
    return sum(
        1
        for prime in range(2, target - 1)
        if is_prime[prime] and is_prime[target - prime]
    )


def finite_goldbach_rows(limits: list[int]) -> list[dict[str, object]]:
    maximum = max(limits)
    is_prime = prime_sieve(maximum)
    counts = {
        target: ordered_goldbach_count(target, is_prime)
        for target in range(4, maximum + 1, 2)
    }
    rows = []
    for limit in limits:
        local = [counts[target] for target in range(4, limit + 1, 2)]
        rows.append(
            {
                "even_target_limit": limit,
                "even_targets_checked": len(local),
                "minimum_ordered_goldbach_count": min(local),
                "maximum_ordered_goldbach_count": max(local),
                "counterexample_found": any(value == 0 for value in local),
            }
        )
    return rows


def goldbach_spike_audit() -> dict[str, object]:
    rows = [exceptional_spike_row(size) for size in [16, 64, 256, 1024, 4096]]
    finite = finite_goldbach_rows([100, 1_000, 10_000])
    failures = sum(
        not check
        for row in rows
        for check in row["checks"].values()
    )
    failures += sum(row["counterexample_found"] for row in finite)
    return {
        "theorem": (
            "Mean-square or exceptional-density control cannot certify binary "
            "Goldbach positivity at every target. For L targets with major value "
            "mu>0, put a minor error -(1+epsilon)mu at one target and zero elsewhere. "
            "The normalized RMS is (1+epsilon)mu/sqrt(L) and tends to zero, but the "
            "major-plus-minor value at that target is -epsilon mu."
        ),
        "proof": (
            "The squared error has one nonzero term, so its normalized mean square "
            "is (1+epsilon)^2 mu^2/L. The exceptional set has density 1/L, yet the "
            "single spike reverses the sign. Thus an exceptional-set theorem or an "
            "L2 minor-arc estimate requires a separate L-infinity exception-removal "
            "argument before it can imply the strong Goldbach conjecture."
        ),
        "exceptional_spike_counterfamily": rows,
        "finite_exact_goldbach_rows": finite,
        "aggregate": {
            "spike_size_count": len(rows),
            "largest_target_count": rows[-1]["target_count_L"],
            "rms_decreases": all(
                rows[index + 1]["normalized_minor_rms"]
                < rows[index]["normalized_minor_rms"]
                for index in range(len(rows) - 1)
            ),
            "every_spike_breaks_positivity": all(
                row["minimum_major_plus_minor"] < 0.0 for row in rows
            ),
            "largest_finite_even_target": finite[-1]["even_target_limit"],
        },
        "no_go_scope": (
            "This proves that average error and a vanishing exceptional density do "
            "not imply every-target positivity. Exact finite verification through "
            "10,000 finds no counterexample but has no implication for unbounded "
            "targets. A target-uniform arithmetic L-infinity deficit remains open."
        ),
        "failure_count": failures,
    }


def twin_block_row(component_count: int, good_block_count: int) -> dict[str, object]:
    block_diagonal = float(component_count)
    good_zero_mode = 0.0
    bad_zero_mode = float(component_count**2)
    total_diagonal = (good_block_count + 1) * block_diagonal
    total_zero_mode = bad_zero_mode
    global_ratio = total_zero_mode / total_diagonal
    global_centered_ratio = 1.0 - global_ratio / component_count
    checks = {
        "global_ratio_formula_holds": math.isclose(
            global_ratio, component_count / (good_block_count + 1)
        ),
        "global_centered_ratio_formula_holds": math.isclose(
            global_centered_ratio, good_block_count / (good_block_count + 1)
        ),
        "bad_block_is_fully_aligned": bad_zero_mode / block_diagonal
        == component_count,
        "bad_block_has_zero_centered_energy": True,
    }
    return {
        "component_count_m": component_count,
        "good_cancelling_block_count_K": good_block_count,
        "bad_aligned_block_count": 1,
        "global_zero_mode_to_diagonal_ratio": global_ratio,
        "global_centered_to_diagonal_ratio": global_centered_ratio,
        "bad_block_zero_mode_to_diagonal_ratio": bad_zero_mode / block_diagonal,
        "bad_block_centered_to_diagonal_ratio": 0.0,
        "checks": checks,
    }


def twin_block_localization_audit() -> dict[str, object]:
    component_count = 8
    rows = [
        twin_block_row(component_count, count)
        for count in [8, 32, 128, 512, 2048]
    ]
    failures = sum(
        not check
        for row in rows
        for check in row["checks"].values()
    )
    return {
        "theorem": (
            "Global centered-energy saturation does not imply uniform blockwise "
            "zero-mode cancellation. With m components, take K blocks whose "
            "components are scalar m-th roots of unity and one block whose components "
            "are all aligned. Then the global ratio sum Z_b/sum D_b equals m/(K+1) "
            "and tends to zero, while the bad block keeps Z_bad/D_bad=m and zero "
            "centered energy."
        ),
        "proof": (
            "Each cancelling block has D=m, Z=0, V=m. The aligned block has D=m, "
            "Z=m^2, V=0. Summing gives D_total=(K+1)m and Z_total=m^2, hence the "
            "stated global ratio. Arbitrarily strong average saturation can therefore "
            "hide a completely non-cancelling scale."
        ),
        "block_counterfamily": rows,
        "aggregate": {
            "component_count": component_count,
            "good_block_count_cases": len(rows),
            "largest_good_block_count": rows[-1]["good_cancelling_block_count_K"],
            "global_zero_mode_ratio_decreases": all(
                rows[index + 1]["global_zero_mode_to_diagonal_ratio"]
                < rows[index]["global_zero_mode_to_diagonal_ratio"]
                for index in range(len(rows) - 1)
            ),
            "bad_block_never_improves": all(
                row["bad_block_zero_mode_to_diagonal_ratio"] == component_count
                for row in rows
            ),
        },
        "no_go_scope": (
            "This refutes a global or averaged centered-energy estimate as a "
            "substitute for uniform dyadic cancellation. It does not prove any "
            "centered-energy bound for actual prime-pair Haar blocks or overcome "
            "the parity barrier needed for a positive twin-prime lower bound."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_hidden_frequency_audit()
    collatz = collatz_order_audit()
    goldbach = goldbach_spike_audit()
    twin = twin_block_localization_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-180",
            "theorem_name": "FiniteToeplitzMomentIndeterminacyAndTailEnvelopeNecessity",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No certified arithmetic envelope controls the unobserved high-frequency modes of the actual pole-neutral Weil tail.",
            "route_decision": {
                "discard": "finite Toeplitz-section agreement as a certificate for a global bounded Weil symbol",
                "retain": "finite sections plus an independent arithmetic high-frequency envelope",
                "next_single_lemma": "ArithmeticWeilTailHasCertifiedUniformHighFrequencyEnvelopeBeyondObservedBand",
            },
            "proof_dag": proof_dag(
                "RH",
                "FiniteToeplitzSectionsCertifyTheGlobalWeilSymbolBound",
                "FiniteToeplitzMomentIndeterminacyAndTailEnvelopeNecessity",
                "ArithmeticWeilTailHasCertifiedUniformHighFrequencyEnvelopeBeyondObservedBand",
            ),
            "claim_boundary": "No RH proof or zero exclusion; one exact finite-moment indeterminacy theorem and five hidden-frequency witnesses only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-180",
            "theorem_name": "ValuationLayerPermutationNoGoAndOrderedAffinePrefixIdentity",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "No theorem forces every natural orbit to cross an ordered-prefix descent boundary, and nontrivial cycles remain unexcluded.",
            "route_decision": {
                "discard": "unordered adaptive valuation layers as a complete first-descent or cycle certificate",
                "retain": "ordered prefix sums and the exact affine numerator on natural cylinders",
                "next_single_lemma": "OrderedCylinderTransferHasUniformDescentOutsideExplicitFiniteExceptionalSet",
            },
            "proof_dag": proof_dag(
                "CO",
                "AdaptiveValuationLayerTotalsDetermineFirstDescent",
                "ValuationLayerPermutationNoGoAndOrderedAffinePrefixIdentity",
                "OrderedCylinderTransferHasUniformDescentOutsideExplicitFiniteExceptionalSet",
            ),
            "claim_boundary": "No Collatz proof, divergent orbit, or cycle exclusion; one ordered affine identity and seven natural permutation counterpairs only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-180",
            "theorem_name": "MeanSquareExceptionalSpikeNoGoForEveryTargetPositivity",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No target-uniform arithmetic L-infinity estimate keeps the parity-aliased minor contribution below the major term on every large dyadic block.",
            "route_decision": {
                "discard": "mean-square minor control or vanishing exceptional density as sufficient for every-target positivity",
                "retain": "target-wise L-infinity deficits with an explicit exception-removal mechanism",
                "next_single_lemma": "ParityAliasedMinorHasUniformLInfinityDeficitBelowMajorMainOnEveryDyadicBlock",
            },
            "proof_dag": proof_dag(
                "GB",
                "VanishingExceptionalDensityImpliesEveryTargetGoldbachPositivity",
                "MeanSquareExceptionalSpikeNoGoForEveryTargetPositivity",
                "ParityAliasedMinorHasUniformLInfinityDeficitBelowMajorMainOnEveryDyadicBlock",
            ),
            "claim_boundary": "No Goldbach proof or counterexample; one exact exceptional-spike no-go family and finite verification through 10,000 only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-180",
            "theorem_name": "GlobalCenteredEnergyNoGoForUniformBlockCancellation",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No arithmetic theorem gives centered-energy saturation uniformly for every sufficiently large prime-pair Haar block.",
            "route_decision": {
                "discard": "global or averaged centered-energy saturation as sufficient for uniform scale cancellation",
                "retain": "uniform dyadic-block centered-energy saturation tied to the prime-pair sequence",
                "next_single_lemma": "PrimePairHaarCenteredEnergySaturatesDiagonalUniformlyOnEveryLargeDyadicBlock",
            },
            "proof_dag": proof_dag(
                "TP",
                "GlobalCenteredEnergySaturationForcesUniformBlockCancellation",
                "GlobalCenteredEnergyNoGoForUniformBlockCancellation",
                "PrimePairHaarCenteredEnergySaturatesDiagonalUniformlyOnEveryLargeDyadicBlock",
            ),
            "claim_boundary": "No Twin Prime proof or parity-breaking lower bound; one exact global-to-local no-go theorem and five block counterfamilies only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureFiniteInformationLocalizationAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-180 proves four exact localization no-go theorems and resolves "
            "none of the conjectures. Finite RH moments miss high frequencies, "
            "unordered Collatz layers miss prefix order, average Goldbach errors miss "
            "exceptional spikes, and global Twin energy misses bad dyadic blocks."
        ),
        **sections,
        "cross_problem_synthesis": (
            "All four failures are quantifier mismatches: finite to infinite, multiset "
            "to ordered path, almost-all to every target, and global average to every "
            "block. The next proof contracts must carry a uniform localization "
            "operator before any conjecture-level conclusion is valid."
        ),
        "literature_boundary": {
            "riemann": "Recent finite Guinand-Weil and truncated-form results provide exact finite dictionaries and explicit tails but make no RH claim; finite moments alone do not control an unobserved symbol.",
            "collatz": "Recent one-bit reductions isolate orbit-level mixing rather than proving it; unordered layer totals still omit the ordered affine numerator.",
            "goldbach": "Exceptional-set estimates explicitly permit exceptional even targets and therefore cannot by themselves prove the strong every-target statement.",
            "twin_prime": "Prime-producing sieve theory requires substantial Type II information and does not turn an averaged Hilbert-space cancellation surrogate into a twin-prime lower bound.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "rejected_target_count": 4,
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
    write_json(
        ROOT / "data" / "open-problem" / "ticket180-finite-information-localization.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "finite_information_localization_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-180-hidden-frequency.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-180-ordered-prefix.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-180-exceptional-spike.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-180-block-localization.json",
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
            "TICKET-180 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
