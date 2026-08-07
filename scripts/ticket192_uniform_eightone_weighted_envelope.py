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
from ticket189_corefive_sublinear_shift import (
    proper_prime_power_budget_row,
    twin_shift_two_row,
)


GENERATED_AT = "2026-08-08T03:00:00+09:00"
SCHEMA = "primeproject.ticket192-uniform-eightone-weighted-envelope.v1"
STATUS = (
    "one_additional_infinite_cycle_stratum_closed_"
    "three_uniformity_or_weighted_targets_sharpened_all_open"
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
                "id": f"{problem_code}-T191-INPUT",
                "label": previous_name,
                "status": "proved_exact_input_or_open_target",
            },
            {
                "id": f"{problem_code}-T192-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T192-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_stronger_than_necessary",
            },
            {
                "id": f"{problem_code}-T192-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T191-INPUT", f"{problem_code}-T192-CLOSED"],
            [f"{problem_code}-T192-CLOSED", f"{problem_code}-T192-OPEN"],
            [f"{problem_code}-T192-REJECTED", f"{problem_code}-T192-OPEN"],
        ],
    }


def unbounded_core_row(dimension: int) -> dict[str, object]:
    if dimension < 1:
        raise ValueError("dimension must be positive")
    return {
        "dimension_N": dimension,
        "diagonal": list(range(1, dimension + 1)),
        "unit_coordinate_witness": dimension,
        "witness_quadratic_value": dimension,
        "operator_norm": dimension,
        "positive_semidefinite": True,
        "pointwise_stable_on_vectors_supported_below_N": True,
    }


def riemann_uniform_extension_audit() -> dict[str, object]:
    rows = [unbounded_core_row(dimension) for dimension in [2, 4, 8, 16, 32, 64]]
    fixed_vectors = [
        {"support": 1, "eventual_value": 1},
        {"support": 2, "eventual_value": 1 + 2},
        {"support": 4, "eventual_value": 1 + 2 + 3 + 4},
        {"support": 8, "eventual_value": sum(range(1, 9))},
    ]
    failures = sum(
        int(not row["positive_semidefinite"])
        + int(row["operator_norm"] != row["dimension_N"])
        for row in rows
    )
    failures += int(
        any(
            later["operator_norm"] <= earlier["operator_norm"]
            for earlier, later in zip(rows, rows[1:])
        )
    )
    return {
        "theorem": (
            "Let D be dense in a complex Hilbert space H and q a Hermitian "
            "quadratic form on D. The form extends uniquely to a bounded "
            "Hermitian form on H if and only if |q(x)|<=C||x||^2 on D for "
            "some finite C. Positivity then passes to H. Pointwise Cauchy "
            "convergence on a countable dense core is not sufficient: the "
            "positive finite sections q_N(x)=sum_{k<=N} k|x_k|^2 stabilize "
            "on c_00 but their limit has q(e_k)=k and no bounded extension "
            "to l^2."
        ),
        "proof": (
            "Necessity follows by restricting a bounded extension to D. For "
            "sufficiency, complex polarization and rescaling give "
            "|B(x,y)|<=2C||x||||y||, so B extends uniquely by density. The "
            "quadratic form of the extension is continuous, and nonnegativity "
            "passes from D to H. In the counterexample every finite-support "
            "vector is eventually unchanged by the truncations, while the "
            "unit coordinate values k are unbounded; a bounded extension "
            "would bound all of them by one common constant."
        ),
        "finite_section_counterexample_rows": rows,
        "fixed_vector_stabilization_rows": fixed_vectors,
        "extension_contract": {
            "uniform_quadratic_bound_is_necessary_and_sufficient": True,
            "positivity_passes_under_continuous_extension": True,
            "pointwise_dense_core_cauchy_is_sufficient": False,
            "actual_pole_neutral_weil_uniform_bound_verified": False,
        },
        "no_go_scope": (
            "This is an abstract extension theorem and an exact no-go for "
            "pointwise-only promotion. It proves no convergence or uniform "
            "admissible-norm bound for the actual Weil quadratic form and does "
            "not prove the Riemann hypothesis."
        ),
        "failure_count": failures,
    }


def eight_one_product_bound(horizon: int) -> Fraction:
    if horizon < 1:
        raise ValueError("horizon must be positive")
    return Fraction(256) * Fraction(5, 6) ** horizon


def finite_eight_one_horizon_row(horizon: int) -> dict[str, object]:
    if not 20 <= horizon <= 30:
        raise ValueError("the rotation-normalized finite range is h=20..30")
    denominator = 2 ** (2 * horizon - 8) - 3**horizon
    digest = hashlib.sha256()
    hits: list[dict[str, object]] = []
    word_count = 0
    for remaining_positions in itertools.combinations(range(1, horizon), 7):
        positions = (0,) + remaining_positions
        word = [2] * horizon
        for position in positions:
            word[position] = 1
        word_tuple = tuple(word)
        numerator = ordered_affine_numerator(word_tuple)
        remainder = numerator % denominator
        digest.update(f"{positions}:{remainder}\n".encode("ascii"))
        word_count += 1
        if remainder == 0:
            hits.append(
                {
                    "positions": list(positions),
                    "integer_quotient": numerator // denominator,
                }
            )
    return {
        "horizon_h": horizon,
        "rotation_normalization": "v_0=1",
        "contracting": denominator > 0,
        "word_count": word_count,
        "expected_word_count": math.comb(horizon - 1, 7),
        "divisibility_hit_count": len(hits),
        "divisibility_hits": hits,
        "remainder_transcript_sha256": digest.hexdigest(),
    }


def collatz_eight_one_audit() -> dict[str, object]:
    finite_rows = [finite_eight_one_horizon_row(h) for h in range(20, 31)]
    analytic_rows = [
        {
            "horizon_h": horizon,
            "cycle_product_upper_bound": fraction_payload(
                eight_one_product_bound(horizon)
            ),
            "strictly_below_one": eight_one_product_bound(horizon) < 1,
        }
        for horizon in [31, 32, 40, 64, 96]
    ]
    failures = sum(
        int(not row["contracting"])
        + int(row["word_count"] != row["expected_word_count"])
        + int(row["divisibility_hit_count"])
        for row in finite_rows
    )
    failures += sum(not row["strictly_below_one"] for row in analytic_rows)
    failures += int(eight_one_product_bound(30) <= 1)
    failures += int(
        any(
            eight_one_product_bound(h + 1) >= eight_one_product_bound(h)
            for h in range(31, 256)
        )
    )
    total_words = sum(row["word_count"] for row in finite_rows)
    return {
        "theorem": (
            "No positive accelerated Collatz cycle has a valuation period "
            "with exactly eight entries equal to one and every other entry "
            "equal to two, including primitive and imprimitive periods."
        ),
        "proof": (
            "For period length h the affine denominator is "
            "D=2^(2h-8)-3^h, positive from h=20. Rotate any word so one of "
            "its eight ones is first. Divisibility is rotation invariant via "
            "2^v B_shift=3B+D, and D is odd. Exact enumeration of all "
            "sum_{h=20}^{30} C(h-1,7)=5,777,343 normalized words finds no "
            "D|B hit. A nontrivial positive odd cycle has every value at least "
            "three, so multiplication gives 1<=256(5/6)^h. The right side is "
            "strictly below one at h=31 and decreases thereafter."
        ),
        "finite_exception_horizon_rows": finite_rows,
        "analytic_product_rows": analytic_rows,
        "analytic_bound": {
            "bound_at_h_31": fraction_payload(eight_one_product_bound(31)),
            "required_upper_threshold": fraction_payload(Fraction(1)),
            "analytic_range_starts_at_h": 31,
            "bound_is_strictly_decreasing": True,
        },
        "aggregate": {
            "infinite_family_proved": True,
            "includes_imprimitive_words": True,
            "rotation_normalization_is_complete": True,
            "contracting_range_starts_at_h": 20,
            "analytic_range_starts_at_h": 31,
            "finite_exception_word_count": total_words,
            "finite_word_count_identity": "C(30,8)-C(19,8)=5777343",
            "divisibility_hits": sum(
                row["divisibility_hit_count"] for row in finite_rows
            ),
        },
        "no_go_scope": (
            "This closes only the exactly-eight-one/rest-two periodic "
            "valuation stratum. Nine-or-more-one strata, valuations at least "
            "three, and aperiodic divergence remain open."
        ),
        "failure_count": failures,
    }


def weighted_proper_prime_power_mass(
    metadata: list[tuple[int, int] | None], start: int, stop: int
) -> float:
    lower = max(2, start)
    upper = min(stop, len(metadata))
    return math.fsum(
        math.log(meta[0])
        for meta in metadata[lower:upper]
        if meta is not None and meta[1] >= 2
    )


def proper_prime_power_count(
    metadata: list[tuple[int, int] | None], start: int, stop: int
) -> int:
    lower = max(2, start)
    upper = min(stop, len(metadata))
    return sum(
        meta is not None and meta[1] >= 2 for meta in metadata[lower:upper]
    )


def goldbach_weighted_envelope_audit() -> dict[str, object]:
    targets = [64, 256, 1_024, 4_096, 16_384, 65_536, 262_144, 1_048_576]
    metadata = prime_power_metadata(max(targets) + 2)
    rows: list[dict[str, object]] = []
    for target in targets:
        decomposition = goldbach_prime_power_row(target, metadata)
        old_budget = proper_prime_power_budget_row(target, metadata)
        weighted_mass = weighted_proper_prime_power_mass(metadata, 2, target + 1)
        actual_count = proper_prime_power_count(metadata, 2, target + 1)
        weighted_envelope = 2.0 * math.log(target) * weighted_mass
        count_envelope = actual_count * math.log(target) ** 2
        total = decomposition["weighted_total_convolution"]
        contamination = decomposition["weighted_prime_power_contamination"]
        rows.append(
            {
                "target_N": target,
                "weighted_proper_prime_power_mass": weighted_mass,
                "actual_proper_prime_power_count": actual_count,
                "actual_contamination": contamination,
                "weighted_contamination_envelope": weighted_envelope,
                "count_envelope": count_envelope,
                "ticket191_simplified_budget": old_budget[
                    "simplified_contamination_mass_bound"
                ],
                "weighted_total_convolution": total,
                "checks": {
                    "actual_contamination_below_weighted_envelope": contamination
                    <= weighted_envelope + 1e-9,
                    "weighted_envelope_below_count_envelope": weighted_envelope
                    <= count_envelope + 1e-9,
                    "count_envelope_below_half_ticket191_budget": count_envelope
                    <= old_budget["simplified_contamination_mass_bound"] / 2.0
                    + 1e-9,
                    "finite_total_exceeds_weighted_envelope": total
                    > weighted_envelope,
                },
            }
        )
    failures = sum(not check for row in rows for check in row["checks"].values())
    return {
        "theorem": (
            "Let W_pp(X)=sum_{p^k<=X,k>=2} log p. The proper-prime-power "
            "part E_pp(N) of the binary von Mangoldt correlation satisfies "
            "E_pp(N)<=2 log(N) W_pp(N). If A(N) counts proper prime powers, "
            "then W_pp(N)<=A(N)log(N)/2 and hence "
            "E_pp(N)<=A(N)(log N)^2, halving the corresponding count-based "
            "factor in the TICKET-191 sufficient budget."
        ),
        "proof": (
            "Charge each contaminated ordered pair to a proper prime power in "
            "its left or right coordinate. The other von Mangoldt factor is "
            "at most log N, giving the first union bound. For q=p^k with "
            "k>=2 and q<=N, log p=log q/k<=log N/2. Summing over the A(N) "
            "proper powers gives the second bound. Strict total correlation "
            "above this envelope leaves positive prime-prime mass."
        ),
        "weighted_budget_rows": rows,
        "aggregate": {
            "target_count": len(rows),
            "largest_target": targets[-1],
            "weighted_envelope_theorem_proved": True,
            "count_budget_factor_two_removed": True,
            "finite_sample_budget_excess_count": sum(
                row["checks"]["finite_total_exceeds_weighted_envelope"]
                for row in rows
            ),
            "all_large_even_targets_proved": False,
        },
        "no_go_scope": (
            "The finite rows verify the sharper sufficient inequality only at "
            "listed targets. They do not establish it for every sufficiently "
            "large even integer, so strong Goldbach remains open."
        ),
        "failure_count": failures,
    }


def twin_weighted_envelope_audit() -> dict[str, object]:
    exponents = list(range(4, 20))
    limit = 2 ** (exponents[-1] + 1) + 2
    metadata = prime_power_metadata(limit)
    rows: list[dict[str, object]] = []
    for exponent in exponents:
        arithmetic = twin_shift_two_row(exponent, metadata)
        lower = 2**exponent
        upper = 2 * lower
        log_upper = math.log(upper + 2)
        left_mass = weighted_proper_prime_power_mass(
            metadata, lower, upper
        )
        right_mass = weighted_proper_prime_power_mass(
            metadata, lower + 2, upper + 2
        )
        local_envelope = log_upper * (left_mass + right_mass)
        global_count = proper_prime_power_count(metadata, 2, upper + 3)
        half_global_count_envelope = global_count * log_upper**2
        total = arithmetic["weighted_shift_two_correlation"]
        contamination = arithmetic["weighted_prime_power_contamination"]
        rows.append(
            {
                **arithmetic,
                "left_local_weighted_proper_power_mass": left_mass,
                "right_local_weighted_proper_power_mass": right_mass,
                "local_weighted_contamination_envelope": local_envelope,
                "half_global_count_envelope": half_global_count_envelope,
                "checks": {
                    **arithmetic["checks"],
                    "actual_contamination_below_local_envelope": contamination
                    <= local_envelope + 1e-9,
                    "local_envelope_below_half_global_count_envelope": local_envelope
                    <= half_global_count_envelope + 1e-9,
                    "finite_total_exceeds_local_envelope": total > local_envelope,
                },
            }
        )
    failures = sum(not check for row in rows for check in row["checks"].values())
    return {
        "theorem": (
            "For the dyadic block [X,2X), let W_pp(I) be the sum of log p "
            "over proper prime powers p^k in I. The shift-two prime-power "
            "contamination is at most log(2X+2) times "
            "[W_pp([X,2X))+W_pp([X+2,2X+2))]. Correlation above this local "
            "weighted envelope forces a twin prime in the block. Each weighted "
            "mass is at most one half log(2X+2) per proper power, so this also "
            "removes the factor two from the earlier global count envelope."
        ),
        "proof": (
            "A contaminated term has n or n+2 equal to a proper prime power. "
            "Charge it to the appropriate local interval; its partner has von "
            "Mangoldt weight at most log(2X+2). The union bound gives the local "
            "envelope. Subtracting it from the full correlation leaves a "
            "strictly positive prime-prime contribution. The exponent k>=2 "
            "again gives log p<=log(2X+2)/2."
        ),
        "finite_dyadic_rows": rows,
        "aggregate": {
            "dyadic_block_count": len(rows),
            "largest_upper_endpoint": rows[-1]["block"][1],
            "local_weighted_envelope_theorem_proved": True,
            "count_budget_factor_two_removed": True,
            "finite_block_envelope_success_count": sum(
                row["checks"]["finite_total_exceeds_local_envelope"]
                for row in rows
            ),
            "infinitely_many_envelope_successes_proved": False,
        },
        "no_go_scope": (
            "All displayed finite blocks pass the sufficient envelope, but a "
            "finite prefix cannot establish infinitely many successful blocks. "
            "No unbounded dyadic sequence estimate is proved, so the Twin Prime "
            "conjecture remains open."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_uniform_extension_audit()
    collatz = collatz_eight_one_audit()
    goldbach = goldbach_weighted_envelope_audit()
    twin = twin_weighted_envelope_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-192",
            "theorem_name": "UniformBoundedCoreExtensionAndPointwiseCauchyNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No uniform admissible-norm bound is proved for the actual pole-neutral Weil quadratic values.",
            "route_decision": {
                "discard": "promoting pointwise Cauchy convergence on a dense countable core without one uniform continuity bound",
                "retain": "Gaussian-rational probe convergence together with a uniform admissible-norm quadratic bound",
                "next_single_lemma": "PoleNeutralWeilQuadraticValuesConvergeOnGaussianRationalCoreWithUniformAdmissibleNormBound",
            },
            "proof_dag": proof_dag(
                "RH",
                "PoleNeutralWeilQuadraticValuesConvergeOnGaussianRationalCoreAndExtendContinuouslyToAdmissibleTestFunctions",
                "UniformBoundedCoreExtensionAndPointwiseCauchyNoGo",
                "PointwiseDenseCoreCauchyConvergenceAloneImpliesContinuousExtension",
                "PoleNeutralWeilQuadraticValuesConvergeOnGaussianRationalCoreWithUniformAdmissibleNormBound",
            ),
            "claim_boundary": "No RH proof. The exact continuity criterion is proved abstractly; its actual Weil-form premise remains open.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-192",
            "theorem_name": "ExactlyEightValuationOnesOtherwiseTwoCycleExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Nine-or-more-one strata, valuations at least three, and aperiodic divergence remain open.",
            "route_decision": {
                "discard": "enumerating every cyclic rotation separately and continuing enumeration beyond the exact product cutoff",
                "retain": "rotation-normalized affine divisibility for h=20..30 and the product contradiction for h>=31",
                "next_single_lemma": "NoContractingValuationWordWithExactlyNineOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "NoContractingValuationWordWithExactlyEightOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
                "ExactlyEightValuationOnesOtherwiseTwoCycleExclusion",
                "AllCyclicRotationsMustBeEnumeratedIndependently",
                "NoContractingValuationWordWithExactlyNineOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            ),
            "claim_boundary": "No Collatz proof. The complete exactly-eight-one/rest-two periodic valuation stratum is excluded.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-192",
            "theorem_name": "WeightedPrimePowerEnvelopeAndFactorTwoBudgetReduction",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No every-large-even lower bound above the weighted envelope is proved.",
            "route_decision": {
                "discard": "using the unweighted count budget as the primary sufficient target after exponent weights are available",
                "retain": "pointwise binary von Mangoldt correlation above 2 log(N) W_pp(N)",
                "next_single_lemma": "BinaryVonMangoldtCorrelationExceedsWeightedPrimePowerEnvelopeForEveryLargeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "BinaryVonMangoldtCorrelationExceedsExplicitPrimePowerBudgetForEveryLargeEvenTarget",
                "WeightedPrimePowerEnvelopeAndFactorTwoBudgetReduction",
                "UnweightedCountEnvelopeIsTheSharpestPracticalSufficientTarget",
                "BinaryVonMangoldtCorrelationExceedsWeightedPrimePowerEnvelopeForEveryLargeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof. The sufficient contamination envelope is reduced by a factor of at least two, but the universal correlation lower bound is open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-192",
            "theorem_name": "LocalTwoSidedWeightedEnvelopeBridge",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No proof gives correlation above the local weighted envelope on infinitely many unbounded dyadic blocks.",
            "route_decision": {
                "discard": "using a global unweighted proper-power count when only two translated local intervals can contaminate a block",
                "retain": "shift-two correlation above the local two-sided weighted envelope on infinitely many blocks",
                "next_single_lemma": "ShiftTwoCorrelationExceedsLocalWeightedPrimePowerEnvelopeOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "ShiftTwoCorrelationExceedsExactPrimePowerContaminationOnInfinitelyManyDyadicBlocks",
                "LocalTwoSidedWeightedEnvelopeBridge",
                "GlobalUnweightedCountIsTheSharpestDyadicContaminationTarget",
                "ShiftTwoCorrelationExceedsLocalWeightedPrimePowerEnvelopeOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof. A local weighted sufficient envelope is proved and passes finite replay, but infinitude is open.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureUniformEightOneWeightedEnvelopeAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-192 resolves none of the four conjectures. It closes the "
            "complete exactly-eight-one/rest-two accelerated Collatz cycle "
            "stratum, proves the uniform boundedness criterion missing from the "
            "RH core-promotion route, and replaces count-only prime-power "
            "budgets by sharper weighted envelopes for Goldbach and Twin Prime."
        ),
        **sections,
        "cross_problem_synthesis": (
            "All four tracks isolate the uniform estimate that finite evidence "
            "cannot supply by itself: a uniform form bound, a finite-plus-global "
            "cycle cutoff, every-target additive excess, or infinitely-many-"
            "block shift excess. The same weighted proper-prime-power mass "
            "controls both additive and shift-two contamination."
        ),
        "literature_boundary": {
            "riemann": "The 2026 screw-function operator program still states the decisive limiting operator as conjectural; this ticket supplies only an abstract extension criterion.",
            "collatz": "Recent accelerated-map parity-vector work explicitly makes no claim toward Collatz; this ticket excludes one periodic valuation stratum only.",
            "goldbach": "Exceptional-set advances do not provide every-even-target binary correlation control.",
            "twin_prime": "Bounded-gap theorems do not force exact gap two; finite successful blocks do not imply infinitely many.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "new_infinite_cycle_stratum_closure_count": 1,
            "weighted_envelope_bridge_count": 2,
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
    write_json(
        ROOT / "data" / "open-problem" / "ticket192-uniform-eightone-weighted-envelope.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "uniform_eightone_weighted_envelope_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-192-uniform-extension.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-192-eight-one-cycle-exclusion.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-192-weighted-envelope.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-192-local-weighted-envelope.json",
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
            "TICKET-192 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
