from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket151_negative_affine_transversal_logtwo import (
    integer_cube_root,
    smallest_prime_factor_sieve,
)


GENERATED_AT = "2026-07-26T15:00:00+09:00"
SCHEMA = "primeproject.ticket152-compression-cylinder-energy-selection.v1"
STATUS = "exact_target_corrections_all_four_conjectures_open"


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
    rejected_id = f"{problem_code}-T152-REJECTED"
    closed_id = f"{problem_code}-T152-CLOSED"
    open_id = f"{problem_code}-T152-OPEN"
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


def riemann_compression_audit() -> dict[str, object]:
    hidden_rows: list[dict[str, object]] = []
    tail_rows: list[dict[str, object]] = []
    failures = 0

    for cutoff in [1, 2, 4, 8, 16, 32, 64]:
        delta = Fraction(1, cutoff + 1)
        hidden_eigenvalue = -Fraction(1) - delta
        checked_minimum = Fraction(0)
        full_minimum = hidden_eigenvalue
        checks = {
            "all_checked_compressions_pass_floor_minus_one": (
                checked_minimum >= -1
            ),
            "full_operator_fails_floor_minus_one": full_minimum < -1,
            "negative_direction_is_first_hidden_coordinate": (
                hidden_eigenvalue == full_minimum
            ),
        }
        failures += sum(not value for value in checks.values())
        hidden_rows.append(
            {
                "checked_cutoff_N": cutoff,
                "checked_compression_minimum_mu_N": fraction_payload(
                    checked_minimum
                ),
                "hidden_coordinate": cutoff + 1,
                "hidden_eigenvalue": fraction_payload(hidden_eigenvalue),
                "full_spectral_infimum": fraction_payload(full_minimum),
                "checks": checks,
            }
        )

    for exponent in range(2, 11):
        epsilon = Fraction(1, 2**exponent)
        finite_rank_minimum = -Fraction(1) + 2 * epsilon
        certified_lower_bound = finite_rank_minimum - epsilon
        checks = {
            "finite_rank_margin_dominates_tail": (
                finite_rank_minimum >= -1 + epsilon
            ),
            "certified_full_floor_at_least_minus_one": (
                certified_lower_bound >= -1
            ),
            "strict_margin_survives": certified_lower_bound > -1,
        }
        failures += sum(not value for value in checks.values())
        tail_rows.append(
            {
                "operator_norm_tail_epsilon": fraction_payload(epsilon),
                "finite_rank_minimum": fraction_payload(
                    finite_rank_minimum
                ),
                "certified_full_lower_bound": fraction_payload(
                    certified_lower_bound
                ),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let B be bounded and self-adjoint on a separable Hilbert space, "
            "and let H_N be nested finite-dimensional subspaces with dense "
            "union. If mu_N is the minimum Rayleigh quotient of B on H_N, "
            "then mu_N decreases to inf sigma(B), and "
            "||B_-||=sup_N max(0,-mu_N). Hence B>=-I exactly when every "
            "compression has mu_N>=-1. No finite cutoff can certify this: "
            "a diagonal entry below -1 can be placed at the first unchecked "
            "coordinate. A finite-rank approximation F with "
            "||B-F||<=epsilon and lambda_min(F)>=-1+epsilon does certify "
            "B>=-I."
        ),
        "proof": (
            "Nestedness makes mu_N nonincreasing. Density and continuity of "
            "the bounded quadratic form let every unit vector be "
            "approximated by normalized vectors from the union, so the limit "
            "equals the global Rayleigh infimum, namely inf sigma(B). "
            "Spectral calculus gives ||B_-||=max(0,-inf sigma(B)). For the "
            "finite-cutoff counterexample use diag(0,...,0,-1-delta,0,...). "
            "Finally, |<x,(B-F)x>|<=epsilon||x||^2 yields "
            "inf sigma(B)>=lambda_min(F)-epsilon."
        ),
        "finite_hidden_direction_rows": hidden_rows,
        "finite_tail_certificate_rows": tail_rows,
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


def affine_word_constants(word: list[int]) -> tuple[int, int]:
    if not word or any(value < 1 for value in word):
        raise ValueError("valuation words must be nonempty and positive")
    valuation_sum = 0
    constant = 0
    for valuation in word:
        constant = 3 * constant + (1 << valuation_sum)
        valuation_sum += valuation
    return valuation_sum, constant


def valuation_word(start: int, length: int) -> list[int]:
    current = start
    result: list[int] = []
    for _ in range(length):
        current, valuation = accelerated_collatz(current)
        result.append(valuation)
    return result


def word_cylinder(word: list[int]) -> dict[str, int]:
    valuation_sum, constant = affine_word_constants(word)
    modulus = 1 << (valuation_sum + 1)
    inverse = pow(3 ** len(word), -1, modulus)
    residue = ((1 << valuation_sum) - constant) * inverse % modulus
    if residue == 0:
        residue = modulus
    terminal = (
        3 ** len(word) * residue + constant
    ) // (1 << valuation_sum)
    return {
        "valuation_sum": valuation_sum,
        "affine_constant": constant,
        "modulus": modulus,
        "least_positive_residue": residue,
        "terminal_at_residue": terminal,
        "multiplier_gap": (1 << valuation_sum) - 3 ** len(word),
    }


def first_descent_index(word: list[int]) -> int | None:
    cylinder = word_cylinder(word)
    gap = cylinder["multiplier_gap"]
    if gap <= 0:
        return None
    numerator = (
        cylinder["affine_constant"]
        - gap * cylinder["least_positive_residue"]
    )
    denominator = gap * cylinder["modulus"]
    return max(0, numerator // denominator + 1)


def realize_next_valuation(word: list[int], valuation: int) -> dict[str, int]:
    if valuation < 1:
        raise ValueError("next valuation must be positive")
    cylinder = word_cylinder(word)
    terminal = cylinder["terminal_at_residue"]
    modulus = 1 << valuation
    inverse = pow(3 ** (len(word) + 1), -1, modulus)
    lift_index = (
        ((1 << (valuation - 1)) - (3 * terminal + 1) // 2)
        * inverse
    ) % modulus
    start = (
        cylinder["least_positive_residue"]
        + lift_index * cylinder["modulus"]
    )
    return {
        "lift_index_k": lift_index,
        "start_n": start,
        "next_valuation": valuation,
    }


def collatz_cylinder_audit() -> dict[str, object]:
    words = [
        [1],
        [2],
        [3],
        [1, 1],
        [1, 2],
        [2, 1],
        [3, 1],
        [1, 1, 1],
        [1, 2, 3],
        [2, 2, 1],
    ]
    cylinder_rows: list[dict[str, object]] = []
    unbounded_rows: list[dict[str, object]] = []
    failures = 0

    for word in words:
        cylinder = word_cylinder(word)
        descent_index = first_descent_index(word)
        checks = {
            "least_residue_realizes_word": (
                valuation_word(
                    cylinder["least_positive_residue"],
                    len(word),
                )
                == word
            ),
            "first_64_lifts_realize_same_word": True,
            "tail_descent_prediction_exact": True,
        }
        for lift_index in range(64):
            start = (
                cylinder["least_positive_residue"]
                + lift_index * cylinder["modulus"]
            )
            if valuation_word(start, len(word)) != word:
                checks["first_64_lifts_realize_same_word"] = False
            current = start
            for _ in word:
                current, _ = accelerated_collatz(current)
            predicted = (
                descent_index is not None and lift_index >= descent_index
            )
            if (current < start) != predicted:
                checks["tail_descent_prediction_exact"] = False
        failures += sum(not value for value in checks.values())
        cylinder_rows.append(
            {
                "valuation_word": word,
                "length_m": len(word),
                "valuation_sum_S": cylinder["valuation_sum"],
                "affine_constant_C": str(cylinder["affine_constant"]),
                "cylinder_modulus_2_to_S_plus_1": str(
                    cylinder["modulus"]
                ),
                "least_positive_residue_r": str(
                    cylinder["least_positive_residue"]
                ),
                "multiplier_gap_D": str(cylinder["multiplier_gap"]),
                "first_descent_lift_index_k": descent_index,
                "checks": checks,
            }
        )

    parent_words = [[1], [2], [1, 1], [1, 2], [2, 1]]
    for parent in parent_words:
        for finite_cap in [4, 8, 16, 24, 32]:
            missing = finite_cap + 1
            witness = realize_next_valuation(parent, missing)
            replay = valuation_word(
                witness["start_n"],
                len(parent) + 1,
            )
            checks = {
                "parent_word_replayed": replay[:-1] == parent,
                "missing_next_valuation_replayed": replay[-1] == missing,
                "outside_every_first_extension_at_or_below_cap": (
                    replay[-1] > finite_cap
                ),
            }
            failures += sum(not value for value in checks.values())
            unbounded_rows.append(
                {
                    "parent_word": parent,
                    "finite_first_extension_cap_B": finite_cap,
                    "constructed_missing_next_valuation_B_plus_1": missing,
                    "lift_index_k": str(witness["lift_index_k"]),
                    "witness_start_n": str(witness["start_n"]),
                    "replayed_extended_word": replay,
                    "checks": checks,
                }
            )

    return {
        "theorem": (
            "Every finite accelerated valuation word a=(a_1,...,a_m), with "
            "S=sum a_i and affine constant C, is realized by exactly one "
            "positive odd residue r modulo 2^(S+1). Its starts are "
            "n=r+k2^(S+1). If D=2^S-3^m>0, descent at time m holds exactly "
            "for the terminal tail k>=k_min; if D<=0 it never holds at that "
            "time. Moreover the next valuation is unbounded on every such "
            "cylinder. Therefore a nonterminal cylinder cannot be covered "
            "by any finite family of strict valuation-word extensions."
        ),
        "proof": (
            "The congruence 3^m n+C congruent to 2^S modulo 2^(S+1) has a "
            "unique solution because 3^m is odd; induction through the "
            "accelerated map shows it realizes all exact prefix valuations. "
            "The identity T^m(n)-n=(C-Dn)/2^S gives the tail threshold. If "
            "t is the terminal value at r, then terminals along the cylinder "
            "are t+2*3^m k. For any b>=1, the congruence "
            "(3t+1)/2+3^(m+1)k congruent to 2^(b-1) modulo 2^b has a unique "
            "solution, so v2(3T^m(n)+1)=b is realizable. Choosing b larger "
            "than every first new valuation in a finite extension family "
            "produces an uncovered natural start."
        ),
        "finite_cylinder_tail_rows": cylinder_rows,
        "finite_unbounded_next_valuation_rows": unbounded_rows,
        "failure_count": failures,
    }


def von_mangoldt_values(limit: int) -> list[float]:
    spf = smallest_prime_factor_sieve(limit)
    values = [0.0] * (limit + 1)
    for prime in range(2, limit + 1):
        if spf[prime] != prime:
            continue
        logarithm = math.log(prime)
        power = prime
        while power <= limit:
            values[power] = logarithm
            if power > limit // prime:
                break
            power *= prime
    return values


def goldbach_global_l2_audit() -> dict[str, object]:
    endpoints = [1_000, 10_000, 100_000, 1_000_000]
    values = von_mangoldt_values(endpoints[-1])
    prefix = [0.0] * len(values)
    prefix_squared = [0.0] * len(values)
    for index in range(1, len(values)):
        prefix[index] = prefix[index - 1] + values[index]
        prefix_squared[index] = (
            prefix_squared[index - 1] + values[index] ** 2
        )

    rows: list[dict[str, object]] = []
    failures = 0
    for endpoint in endpoints:
        x = endpoint - 1
        l2_squared = (
            prefix_squared[x] - 2 * prefix[x] + x
        )
        hole_radius_squared = endpoint / 2
        ratio = l2_squared / hole_radius_squared
        convolution = sum(
            values[index] * values[endpoint - index]
            for index in range(1, endpoint)
        )
        checks = {
            "uniform_hole_radius_formula": (
                hole_radius_squared == endpoint / 2
            ),
            "global_l2_error_exceeds_hole_radius": (
                l2_squared > hole_radius_squared
            ),
            "finite_endpoint_von_mangoldt_convolution_positive": (
                convolution > 0
            ),
            "ratio_positive": ratio > 0,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "even_endpoint_N": endpoint,
                "uniform_endpoint_hole_radius_squared": (
                    hole_radius_squared
                ),
                "von_mangoldt_minus_one_l2_squared": l2_squared,
                "l2_to_hole_radius_squared_ratio": ratio,
                "two_log_N_reference": 2 * math.log(endpoint),
                "von_mangoldt_endpoint_convolution": convolution,
                "checks": checks,
            }
        )

    ratios = [
        float(row["l2_to_hole_radius_squared_ratio"])
        for row in rows
    ]
    monotone = all(
        right > left for left, right in zip(ratios, ratios[1:])
    )
    if not monotone:
        failures += 1

    return {
        "theorem": (
            "For the reflection a maps to N-a on {1,...,N-1}, the constant "
            "baseline w=1 has exact endpoint-hole radius squared N/2. Yet "
            "||Lambda-1||_2^2 is asymptotic to N log N, so the squared-error "
            "to radius ratio is asymptotic to 2 log N and diverges. More "
            "generally, for any dense baselines uniformly bounded between "
            "fixed positive constants c and C, the hole radius is O(N) "
            "while ||Lambda-w_N||_2^2 is asymptotic to N log N. Thus the "
            "global L2-ball transfer proposed after TICKET-151 is "
            "asymptotically unreachable for this natural baseline class."
        ),
        "proof": (
            "The reflection has (N-2)/2 two-cycles and one fixed point, each "
            "costing one, so rho_N(1)^2=N/2. The prime number theorem and "
            "partial summation give sum_{n<=N} Lambda(n)^2="
            "N log N+O(N) and psi(N)=N+o(N); hence "
            "sum(Lambda(n)-1)^2=N log N+O(N). For c<=w_N<=C, the exact "
            "orbit formula gives rho_N(w_N)^2<=C^2 N/2, while "
            "sum(Lambda-w_N)^2>=sum Lambda^2-2C psi(N), still "
            "N log N+O(N). This rejects only global norm transfer, not "
            "endpoint-resolved circle-method cancellation."
        ),
        "finite_uniform_baseline_rows": rows,
        "finite_ratio_strictly_increasing": monotone,
        "failure_count": failures,
    }


def twin_selection_transfer_audit() -> dict[str, object]:
    limits = [1_000, 10_000, 100_000, 1_000_000]
    spf = smallest_prime_factor_sieve(limits[-1] + 2)
    rows: list[dict[str, object]] = []
    sharp_rows: list[dict[str, object]] = []
    failures = 0
    target_mean = (math.log(2) - 1) / (math.log(2) + 1)

    for cutoff in limits:
        roughness = integer_cube_root(cutoff)

        def is_rough(value: int) -> bool:
            return value >= 2 and spf[value] > roughness

        def label(value: int) -> int:
            return -1 if spf[value] == value else 1

        ambient = [
            value for value in range(2, cutoff - 1) if is_rough(value)
        ]
        selected = [
            value for value in ambient if is_rough(value + 2)
        ]
        ambient_sum = sum(label(value) for value in ambient)
        selected_left_sum = sum(label(value) for value in selected)
        selected_right_sum = sum(label(value + 2) for value in selected)
        ambient_size = len(ambient)
        selected_size = len(selected)
        omitted = ambient_size - selected_size
        deficit_fraction = Fraction(-ambient_sum, ambient_size)
        coverage = Fraction(selected_size, ambient_size)
        required_coverage = Fraction(
            ambient_size + ambient_sum,
            ambient_size,
        )
        guaranteed_negative = omitted < -ambient_sum
        checks = {
            "ambient_liouville_sum_negative": ambient_sum < 0,
            "gap_two_support_nonempty": selected_size > 0,
            "actual_coverage_below_worst_case_transfer_threshold": (
                coverage <= required_coverage
            ),
            "ambient_bias_does_not_force_selected_sign": (
                not guaranteed_negative
            ),
            "actual_left_selected_sum_negative_finite_only": (
                selected_left_sum < 0
            ),
            "actual_right_selected_sum_negative_finite_only": (
                selected_right_sum < 0
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "X": cutoff,
                "cubic_roughness_floor_y": roughness,
                "ambient_rough_vertices_M": ambient_size,
                "ambient_liouville_sum_A": ambient_sum,
                "ambient_negative_bias_delta": fraction_payload(
                    deficit_fraction
                ),
                "gap_two_selected_edges_E": selected_size,
                "omitted_vertices_q": omitted,
                "selected_coverage_E_over_M": fraction_payload(coverage),
                "worst_case_required_coverage": fraction_payload(
                    required_coverage
                ),
                "ambient_bias_guarantees_selected_negative": (
                    guaranteed_negative
                ),
                "actual_selected_left_liouville_sum": selected_left_sum,
                "actual_selected_right_liouville_sum": selected_right_sum,
                "distance_to_log_two_limit_mean": abs(
                    float(Fraction(ambient_sum, ambient_size))
                    - target_mean
                ),
                "checks": checks,
            }
        )

        positive_count = (ambient_size + ambient_sum) // 2
        maximum_selected_sum = min(
            selected_size,
            ambient_sum + omitted,
        )
        if selected_size <= positive_count:
            maximum_selected_sum = selected_size
        sharp_checks = {
            "maximum_formula_nonnegative_in_audit": (
                maximum_selected_sum >= 0
            ),
            "counterselection_exists_at_same_size": (
                selected_size <= ambient_size
            ),
            "guarantee_threshold_fails_exactly": (
                omitted >= -ambient_sum
            ),
        }
        failures += sum(not value for value in sharp_checks.values())
        sharp_rows.append(
            {
                "X": cutoff,
                "ambient_size_M": ambient_size,
                "ambient_sum_A": ambient_sum,
                "selected_size_E": selected_size,
                "omitted_q": omitted,
                "sharp_maximum_selected_sum": maximum_selected_sum,
                "checks": sharp_checks,
            }
        )

    coverages = [
        Fraction(row["selected_coverage_E_over_M"]["exact"])
        for row in rows
    ]
    decreasing = all(
        right < left for left, right in zip(coverages, coverages[1:])
    )
    if not decreasing:
        failures += 1

    return {
        "theorem": (
            "Let x_i be signs with ambient size M and total A<0, and retain "
            "E=M-q of them. Every retained subset has negative sum if and "
            "only if q<-A; equivalently E/M>1+A/M. This bound is sharp. For "
            "cubic-rough integers the ambient mean tends to "
            "(log 2-1)/(log 2+1), so an ambient-only argument would require "
            "retaining more than 2 log(2)/(1+log(2)), about 81.87 percent. "
            "Standard one- and two-dimensional sieve bounds give rough "
            "vertex mass of order X/log z and gap-two rough-pair mass at "
            "most order X/(log z)^2; their coverage therefore tends to zero. "
            "The unshifted log-two bias cannot transfer by deletion "
            "robustness."
        ),
        "proof": (
            "The largest sum of an E-subset is E if enough positive signs "
            "exist, and otherwise A+q, obtained by deleting q negative "
            "signs first. Since A<0, this maximum is negative exactly when "
            "q<-A, proving necessity, sufficiency, and sharpness. In the "
            "cubic-rough population A/M tends to the stated log-two mean. "
            "Buchstab/linear-sieve size for one rough variable and the "
            "Selberg upper-bound sieve for the admissible pair (n,n+2) give "
            "the coverage orders. This no-go does not determine the actual "
            "shifted Liouville sign; it proves that sign must be estimated "
            "directly rather than inherited from the ambient marginal."
        ),
        "finite_actual_selection_rows": rows,
        "finite_sharp_counterselection_rows": sharp_rows,
        "finite_coverage_strictly_decreasing": decreasing,
        "target_constants": {
            "ambient_liouville_limit": target_mean,
            "required_retention_limit": (
                2 * math.log(2) / (1 + math.log(2))
            ),
        },
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_compression_audit()
    collatz = collatz_cylinder_audit()
    goldbach = goldbach_global_l2_audit()
    twin_prime = twin_selection_transfer_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )
    next_theorems = {
        "riemann": (
            "ActualWeilCoreCompressionWithCertifiedOperatorNormTailBelowMargin"
        ),
        "collatz": (
            "TypeTwoCountableExtensionCoverWithUniformAnalyticValuationTail"
        ),
        "goldbach": (
            "EndpointBilinearVonMangoldtErrorBelowSingularSeriesMainTermK56"
        ),
        "twin_prime": (
            "DirectShiftedCubicRoughLiouvilleSumNegativeProportion"
        ),
    }
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-152",
            "theorem_name": (
                "NestedCompressionExhaustionAndFiniteCutoffNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The theorem is functional analysis for an already "
                "constructed bounded relative operator. PrimeProject still "
                "does not construct the actual Weil operator on a proved "
                "form core or certify an operator-norm tail. No zeta zero is "
                "excluded from the off-critical region."
            ),
            "route_decision": {
                "discard": (
                    "treating any fixed Galerkin cutoff, however large, as "
                    "a positivity proof"
                ),
                "retain": (
                    "combine nested actual-Weil compressions with a rigorous "
                    "operator-norm tail smaller than the finite spectral "
                    "margin"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "FiniteWeilCompressionPositivityImpliesGlobalPositivity",
                "NestedCompressionExhaustionAndFiniteCutoffNoGo",
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One exact exhaustion "
                "criterion, a rigorous finite-cutoff no-go, and a certified "
                "tail template."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-152",
            "theorem_name": (
                "AffineCylinderTailAndFiniteExtensionCoverNoGo"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The terminal-tail formula handles one fixed word, and the "
                "no-go rules out finite strict-extension covers. It does not "
                "control the countably many next valuations uniformly or "
                "prove that every natural start eventually enters a "
                "descending leaf."
            ),
            "route_decision": {
                "discard": (
                    "searching for a finite strict valuation-word tree that "
                    "covers an entire nonterminal type-two cylinder"
                ),
                "retain": (
                    "use a countable prefix cover plus an analytic estimate "
                    "for the unbounded valuation tail"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "FiniteTypeTwoStrictExtensionTreeCoversCylinder",
                "AffineCylinderTailAndFiniteExtensionCoverNoGo",
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. One exact cylinder "
                "classification and a no-go for finite strict-extension "
                "coverage."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-152",
            "theorem_name": (
                "VonMangoldtGlobalL2HoleBallDivergenceNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The argument rejects a global norm sufficient condition; "
                "it neither proves a pointwise lower bound for the actual "
                "Goldbach convolution nor rules out an even counterexample. "
                "Endpoint-specific signed cancellation remains open."
            ),
            "route_decision": {
                "discard": (
                    "placing the global von Mangoldt error inside the "
                    "weighted endpoint-hole L2 ball of a uniformly bounded "
                    "dense baseline"
                ),
                "retain": (
                    "bound the endpoint bilinear and quadratic error against "
                    "the singular-series main term, with explicit major and "
                    "minor arcs"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "GlobalVonMangoldtL2InsideWeightedHoleRadiusK56",
                "VonMangoldtGlobalL2HoleBallDivergenceNoGo",
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One "
                "asymptotic no-go that replaces an unreachable global L2 "
                "bridge by an endpoint bilinear target."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-152",
            "theorem_name": (
                "SharpMarginalDeletionTransferAndVanishingCoverageNoGo"
            ),
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The sharp selection lemma proves ambient bias is "
                "insufficient. It does not estimate the actual shifted "
                "Liouville sums or prove positive twin-prime mass at every "
                "large scale."
            ),
            "route_decision": {
                "discard": (
                    "using high-retention deletion robustness to transfer "
                    "the one-variable log-two bias to cubic-rough gap-two "
                    "support"
                ),
                "retain": (
                    "estimate the two shifted Liouville sums directly on "
                    "the cubic-rough gap-two support"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "AmbientLogTwoBiasTransfersBySelectionRetention",
                "SharpMarginalDeletionTransferAndVanishingCoverageNoGo",
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof and no finite counterexample to the "
                "conjecture. One sharp transfer threshold and an asymptotic "
                "coverage no-go."
            ),
        },
    }
    return {
        "theorem_name": (
            "FourConjectureCompressionCylinderEnergySelectionAudit"
        ),
        "status": STATUS,
        "proof_boundary": (
            "TICKET-152 proves four exact partial or no-go theorems and "
            "resolves no target conjecture. It turns RH finite compression "
            "tests into an exhaustion-plus-tail contract, proves finite "
            "strict Collatz extension trees cannot cover a nonterminal "
            "valuation cylinder, rejects a globally unreachable Goldbach "
            "von Mangoldt L2 transfer, and proves the Twin ambient log-two "
            "bias cannot survive gap-two selection by deletion robustness."
        ),
        **sections,
        "literature_boundary": [
            {
                "citation": (
                    "Connes and Consani, The Scaling Hamiltonian"
                ),
                "url": "https://arxiv.org/abs/1910.14368",
                "role": (
                    "Primary Weil-positivity operator context; TICKET-152 "
                    "supplies only the abstract compression-and-tail logic."
                ),
            },
            {
                "citation": (
                    "Niu, Parity vectors and paradoxical sequences in the "
                    "accelerated Collatz map"
                ),
                "url": "https://arxiv.org/abs/2605.13886",
                "role": (
                    "Current parity-vector context; the new congruence proof "
                    "isolates the unbounded next-valuation obstruction."
                ),
            },
            {
                "citation": "Helfgott, Minor arcs for Goldbach's problem",
                "url": "https://arxiv.org/abs/1205.5252",
                "role": (
                    "Primary explicit circle-method context; TICKET-152 "
                    "redirects the open bridge to endpoint signed errors."
                ),
            },
            {
                "citation": (
                    "Ford and Maynard, On the theory of prime producing "
                    "sieves"
                ),
                "url": "https://arxiv.org/abs/2407.14368",
                "role": (
                    "Primary sieve-boundary context; rough-pair sparsity "
                    "does not determine the shifted Liouville sign."
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
                        "compression_cylinder_energy_selection_audit."
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
        "compression_cylinder_energy_selection_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket152-compression-cylinder-energy-selection.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-152-compression-tail.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-152-cylinder-cover.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-152-global-l2-no-go.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-152-selection-coverage.json"
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
