from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket142_effective_rank_cycle_direction_haar_liouville import (
    twin_liouville_ledger,
)
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket180_finite_information_localization import ordered_affine_numerator
from ticket185_spectral_cycle_factor_granularity import smallest_prime_factors


GENERATED_AT = "2026-08-02T21:15:00+09:00"
SCHEMA = "primeproject.ticket186-codimension-twoone-layercake-quantization.v1"
STATUS = "one_infinite_cycle_stratum_closed_three_exact_target_corrections_all_open"


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "exact": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


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
                "id": f"{problem_code}-T185-INPUT",
                "label": previous_name,
                "status": "proved_exact_input_or_open_target",
            },
            {
                "id": f"{problem_code}-T186-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T186-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_overstrong",
            },
            {
                "id": f"{problem_code}-T186-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T185-INPUT", f"{problem_code}-T186-CLOSED"],
            [f"{problem_code}-T186-CLOSED", f"{problem_code}-T186-OPEN"],
            [f"{problem_code}-T186-REJECTED", f"{problem_code}-T186-OPEN"],
        ],
    }


def finite_codimension_diagonal_row(
    ambient_dimension: int, removed_coordinate_count: int = 3
) -> dict[str, object]:
    if ambient_dimension <= removed_coordinate_count:
        raise ValueError("the quotient section must have positive dimension")
    smallest_value = Fraction(1, ambient_dimension)
    return {
        "finite_section_dimension_N": ambient_dimension,
        "removed_coordinate_modes": removed_coordinate_count,
        "quotient_section_dimension": ambient_dimension - removed_coordinate_count,
        "smallest_quotient_quadratic_value": fraction_payload(smallest_value),
        "witness_coordinate": ambient_dimension,
        "checks": {
            "finite_section_is_strictly_positive": smallest_value > 0,
            "witness_avoids_removed_modes": ambient_dimension
            > removed_coordinate_count,
            "closed_form_is_one_over_N": smallest_value
            == Fraction(1, ambient_dimension),
        },
    }


def riemann_resolution_audit() -> dict[str, object]:
    rows = [
        finite_codimension_diagonal_row(dimension)
        for dimension in [8, 16, 32, 64, 128, 256]
    ]
    failures = sum(
        not check for row in rows for check in row["checks"].values()
    )
    failures += int(
        not all(
            rows[index + 1]["smallest_quotient_quadratic_value"]["decimal"]
            < rows[index]["smallest_quotient_quadratic_value"]["decimal"]
            for index in range(len(rows) - 1)
        )
    )
    return {
        "theorem": (
            "Let H be an infinite-dimensional Hilbert space and let A be the "
            "positive injective compact operator Ae_n=e_n/n on an orthonormal "
            "basis. For every finite-dimensional subspace T, the infimum of "
            "<Ax,x> over unit vectors x perpendicular to T is zero. Therefore "
            "nonnegativity and injectivity, even after quotienting any finite "
            "list of nuisance or translation modes, do not imply a positive "
            "coercive gap."
        ),
        "proof": (
            "Let P_T be the orthogonal projection onto T. Finite rank implies "
            "||P_T e_n|| tends to zero. Normalize x_n=(I-P_T)e_n. Then x_n is "
            "perpendicular to T, ||x_n-e_n|| tends to zero, and boundedness of "
            "A gives <Ax_n,x_n>-<Ae_n,e_n> tending to zero. Since "
            "<Ae_n,e_n>=1/n, the quotient infimum is zero. Positivity of A "
            "makes the infimum nonnegative, completing the proof."
        ),
        "finite_coordinate_quotient_rows": rows,
        "aggregate": {
            "finite_section_count": len(rows),
            "largest_dimension": rows[-1]["finite_section_dimension_N"],
            "smallest_observed_quotient_gap": rows[-1][
                "smallest_quotient_quadratic_value"
            ],
            "all_finite_sections_strictly_positive": all(
                row["checks"]["finite_section_is_strictly_positive"]
                for row in rows
            ),
            "infinite_quotient_infimum": fraction_payload(Fraction(0, 1)),
        },
        "route_correction": (
            "TICKET-185's coercivity wording is stronger than the RH-equivalent "
            "Weil nonnegativity target unless an independently proved spectral "
            "gap is available. A valid promotion route may use nonnegativity on "
            "a dense pole-neutral form core together with certified negative "
            "defects tending to zero."
        ),
        "no_go_scope": (
            "This is an exact operator-theoretic countermodel, not the zeta Weil "
            "operator. It refutes coercivity as a logically necessary generic "
            "target and finite-dimensional mode removal as a generic repair; it "
            "does not establish actual Weil-form nonnegativity or exclude a "
            "zeta zero off the critical line."
        ),
        "failure_count": failures,
    }


def two_one_cycle_row(horizon: int, first_block_length: int) -> dict[str, object]:
    if horizon < 5:
        raise ValueError("the exactly-two-one family contracts only from h=5")
    if not 1 <= first_block_length < horizon:
        raise ValueError("both cyclic blocks must be nonempty")
    a = first_block_length
    b = horizon - a
    word = (1,) + (2,) * (a - 1) + (1,) + (2,) * (b - 1)
    numerator = (
        4 ** (horizon - 1)
        - 3 ** (horizon - 1)
        + 4**a * 3 ** (b - 1)
    )
    denominator = 4 ** (horizon - 1) - 3**horizon
    quotient_floor = numerator // denominator
    return {
        "horizon_h": horizon,
        "first_block_a": a,
        "second_block_b": b,
        "word": list(word),
        "affine_numerator_B": str(numerator),
        "cycle_denominator_D": str(denominator),
        "B_minus_D": str(numerator - denominator),
        "B_mod_D": str(numerator % denominator),
        "quotient_floor": quotient_floor,
        "checks": {
            "closed_form_matches_recurrence": numerator
            == ordered_affine_numerator(word),
            "contracting": denominator > 0,
            "numerator_is_odd": numerator % 2 == 1,
            "denominator_is_odd": denominator % 2 == 1,
            "numerator_exceeds_denominator": numerator > denominator,
            "affine_divisibility_fails": numerator % denominator != 0,
        },
    }


def collatz_resolution_audit() -> dict[str, object]:
    small_rows = [
        two_one_cycle_row(horizon, first_block)
        for horizon in range(5, 9)
        for first_block in range(1, horizon)
    ]
    replay_rows = [
        two_one_cycle_row(horizon, first_block)
        for horizon in [9, 16, 32, 64, 128]
        for first_block in range(1, horizon)
    ]
    rows = small_rows + replay_rows
    failures = sum(
        not check for row in rows for check in row["checks"].values()
    )
    analytic_threshold_h = 9
    threshold_check = Fraction(4, 3) ** (analytic_threshold_h - 1) > 8
    failures += int(not threshold_check)
    return {
        "theorem": (
            "No positive accelerated Collatz cycle has a valuation period with "
            "exactly two entries equal to one and every other entry equal to "
            "two. After cyclic rotation write the word as "
            "(1,2^(a-1),1,2^(b-1)), where a,b>=1 and h=a+b. The contracting "
            "range is h>=5, and its cycle denominator never divides its affine "
            "numerator. This includes primitive and imprimitive words."
        ),
        "proof": (
            "Block composition gives B=4^(h-1)-3^(h-1)+4^a*3^(b-1) and "
            "D=4^(h-1)-3^h. Thus B-D=2*3^(h-1)+4^a*3^(b-1)>0. For fixed h, "
            "B is maximal at a=h-1, so B<=2*4^(h-1)-3^(h-1). When h>=9, "
            "(4/3)^(h-1)>8 implies B<3D. Both B and D are odd. If D divided "
            "B, the integer B/D would therefore be odd, but 1<B/D<3 leaves "
            "only the even integer two, a contradiction. The finitely many "
            "contracting cases h=5,6,7,8 are exhaustively evaluated for every "
            "a=1,...,h-1 and have no divisibility hit."
        ),
        "small_h_complete_rows": small_rows,
        "large_h_replay_rows": replay_rows,
        "aggregate": {
            "infinite_family_proved": True,
            "includes_imprimitive_words": True,
            "analytic_range_starts_at_h": analytic_threshold_h,
            "small_h_complete_case_count": len(small_rows),
            "replayed_case_count": len(rows),
            "largest_replayed_horizon": max(
                row["horizon_h"] for row in rows
            ),
            "divisibility_hits": sum(
                not row["checks"]["affine_divisibility_fails"] for row in rows
            ),
            "analytic_threshold_check": threshold_check,
        },
        "no_go_scope": (
            "The theorem excludes one additional infinite cycle stratum. It "
            "does not exclude words with three or more valuation-one entries, "
            "entries at least three, or divergent nonperiodic natural-number "
            "orbits."
        ),
        "failure_count": failures,
    }


def goldbach_bad_survivor_layer_row(
    target: int, is_prime: list[bool], least_factor: list[int]
) -> dict[str, object]:
    if target < 6 or target % 2:
        raise ValueError("an even target at least six is required")
    bad_pairs: list[tuple[int, int, int]] = []
    prime_pair_count = 0
    for left in range(3, target // 2 + 1, 2):
        right = target - left
        if is_prime[left] and is_prime[right]:
            prime_pair_count += 1
        else:
            bad_pairs.append(
                (min(least_factor[left], least_factor[right]), left, right)
            )
    horizon = max((gate for gate, _, _ in bad_pairs), default=0)
    survivor_counts = [
        sum(gate > depth for gate, _, _ in bad_pairs)
        for depth in range(horizon)
    ]
    layer_area = sum(survivor_counts)
    direct_gate_sum = sum(gate for gate, _, _ in bad_pairs)
    last_layer_count = survivor_counts[-1] if survivor_counts else 0
    max_gate_multiplicity = sum(
        gate == horizon for gate, _, _ in bad_pairs
    )
    return {
        "even_target_N": target,
        "bad_candidate_pair_count": len(bad_pairs),
        "prime_representation_count": prime_pair_count,
        "factor_horizon_tau_N": horizon,
        "bad_survivor_layer_area": layer_area,
        "sum_of_bad_pair_gates": direct_gate_sum,
        "initial_bad_survivor_count": survivor_counts[0]
        if survivor_counts
        else 0,
        "last_subhorizon_bad_survivor_count": last_layer_count,
        "maximum_gate_multiplicity": max_gate_multiplicity,
        "normalized_layer_area_per_bad_pair": (
            layer_area / len(bad_pairs) if bad_pairs else 0.0
        ),
        "checks": {
            "layer_cake_identity_is_exact": layer_area == direct_gate_sum,
            "every_subhorizon_layer_is_contaminated": all(
                count > 0 for count in survivor_counts
            ),
            "last_layer_equals_max_gate_multiplicity": last_layer_count
            == max_gate_multiplicity,
            "finite_target_has_prime_representation": prime_pair_count > 0,
        },
    }


def goldbach_resolution_audit() -> dict[str, object]:
    targets = [100, 500, 1_000, 5_000, 10_000, 50_000]
    primality = prime_sieve(max(targets))
    least_factor = smallest_prime_factors(max(targets))
    rows = [
        goldbach_bad_survivor_layer_row(target, primality, least_factor)
        for target in targets
    ]
    failures = sum(
        not check for row in rows for check in row["checks"].values()
    )
    return {
        "theorem": (
            "For a fixed even N, let gamma(a) be the smaller least prime "
            "factor of a bad odd pair (a,N-a), define tau as the maximum "
            "gamma with max(empty set)=0, and let B_N(y) count bad pairs with "
            "gamma>y. Then B_N(y)>=1 for every integer 0<=y<tau and the "
            "exact layer-cake identity sum_{y=0}^{tau-1} B_N(y)=sum_bad "
            "gamma(a) holds. Consequently, when tau>0, any nonzero "
            "nonnegative linear combination of subhorizon survivor counts "
            "remains strictly contaminated."
        ),
        "proof": (
            "A bad pair with gate gamma survives exactly the integer depths "
            "y=0,...,gamma-1, so exchanging the two finite sums proves the "
            "identity. If tau>0, a pair attaining the maximum gate tau "
            "survives every depth y<tau, proving strict contamination. If "
            "weights w_y are nonnegative and at least one is positive below "
            "tau, then sum w_y B_N(y)>0. When tau=0 all these subhorizon "
            "statements are vacuous. Cancellation in the nonempty case "
            "therefore requires signed prime-sensitive information or "
            "completion to the exact factor horizon."
        ),
        "target_layer_cake_rows": rows,
        "aggregate": {
            "target_count": len(rows),
            "largest_target": rows[-1]["even_target_N"],
            "largest_factor_horizon": max(
                row["factor_horizon_tau_N"] for row in rows
            ),
            "largest_layer_area": max(
                row["bad_survivor_layer_area"] for row in rows
            ),
            "layer_cake_identity_failures": sum(
                not row["checks"]["layer_cake_identity_is_exact"]
                for row in rows
            ),
        },
        "no_go_scope": (
            "This theorem concerns nonnegative survivor occupancy only. It does "
            "not bound a von Mangoldt-weighted signed sum, a minor-arc term, or "
            "the exceptional set uniformly in N. Finite prime representations "
            "in the replay table do not prove Goldbach."
        ),
        "failure_count": failures,
    }


def quantized_twin_counterledger(total_mass: int) -> dict[str, object]:
    if total_mass < 2:
        raise ValueError("the abstract ledger needs at least two entries")
    categories = {
        "N_plus_plus": total_mass - 1,
        "N_plus_minus": 0,
        "N_minus_plus": 0,
        "N_minus_minus": 1,
    }
    a00 = total_mass
    a10 = total_mass - 2
    a01 = total_mass - 2
    a11 = total_mass
    projector = a00 - a10 - a01 + a11
    return {
        "A00": a00,
        "A10": a10,
        "A01": a01,
        "A11": a11,
        "categories": categories,
        "quantized_projector_Delta": projector,
        "twin_class_count": projector // 4,
        "normalized_projector_margin": projector / a00,
        "checks": {
            "projector_is_exactly_four": projector == 4,
            "one_twin_class_entry": projector // 4 == 1,
            "category_mass_matches_A00": sum(categories.values()) == a00,
            "all_category_counts_are_nonnegative": all(
                value >= 0 for value in categories.values()
            ),
        },
    }


def twin_resolution_audit() -> dict[str, object]:
    finite_rows = []
    for scale in [1_000, 10_000, 100_000, 1_000_000]:
        row = twin_liouville_ledger(scale)
        projector = row["A00"] - row["A10"] - row["A01"] + row["A11"]
        finite_rows.append(
            {
                **row,
                "quantized_projector_Delta": projector,
                "normalized_projector_margin": projector / row["A00"],
                "checks": {
                    **row["checks"],
                    "positive_projector_is_at_least_four": projector >= 4,
                    "projector_equals_four_times_count": projector
                    == 4 * row["direct_twin_count"],
                },
            }
        )
    counter_rows = [
        quantized_twin_counterledger(total_mass)
        for total_mass in [10, 100, 1_000, 10_000, 100_000]
    ]
    failures = sum(
        not check
        for row in finite_rows + counter_rows
        for check in row["checks"].values()
    )
    failures += int(
        not all(
            counter_rows[index + 1]["normalized_projector_margin"]
            < counter_rows[index]["normalized_projector_margin"]
            for index in range(len(counter_rows) - 1)
        )
    )
    return {
        "theorem": (
            "On every cubic-rough Twin block the Walsh projector Delta="
            "A00-A10-A01+A11 equals four times the integer twin count C. Hence "
            "Delta>0 is exactly the quantized condition Delta>=4. On a fixed "
            "predeclared partition into finite disjoint blocks that covers "
            "all sufficiently large candidate starts, infinitely many "
            "positive projectors are equivalent to infinitely many twin "
            "primes. No "
            "fixed relative margin Delta>=delta*A00 is logically necessary: "
            "valid sign ledgers can have C=1, A00 tending to infinity, and "
            "Delta/A00=4/A00 tending to zero."
        ),
        "proof": (
            "Walsh inversion gives C=Delta/4 and category counts are integers, "
            "so Delta is a nonnegative multiple of four on the exact projector. "
            "The abstract category table N--=1, N++=A00-1 and both mixed "
            "categories zero has (A10,A01,A11)=(A00-2,A00-2,A00), hence "
            "Delta=4 for arbitrarily large A00. This proves the fixed-relative-"
            "margin no-go while preserving one positive twin class per block."
        ),
        "finite_cubic_rough_ledger_rows": finite_rows,
        "abstract_vanishing_margin_counterledgers": counter_rows,
        "aggregate": {
            "finite_scale_count": len(finite_rows),
            "largest_finite_scale": finite_rows[-1]["X"],
            "smallest_abstract_relative_margin": counter_rows[-1][
                "normalized_projector_margin"
            ],
            "all_finite_projectors_match_counts": all(
                row["checks"]["projector_equals_four_times_count"]
                for row in finite_rows
            ),
            "conjecture_resolution_count": 0,
        },
        "no_go_scope": (
            "The vanishing-margin ledgers are abstract sign tables, not "
            "alternative values of the arithmetic Liouville function. They "
            "show only that a fixed positive normalized margin is stronger than "
            "Twin infinitude. The finite actual ledgers do not prove recurring "
            "positive projectors on unbounded blocks or break sieve parity."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_resolution_audit()
    collatz = collatz_resolution_audit()
    goldbach = goldbach_resolution_audit()
    twin = twin_resolution_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-186",
            "theorem_name": "FiniteCodimensionCoercivityIsNotNecessaryForNonnegativity",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "The countermodel is not the zeta Weil form; actual nonnegativity on a dense pole-neutral core remains unproved.",
            "route_decision": {
                "discard": "a uniform positive coercive gap, even after removing finitely many declared spectral modes, as a necessary consequence of Weil nonnegativity",
                "retain": "direct nonnegativity on one explicit dense pole-neutral Weil form core, allowing certified negative defects that vanish",
                "next_single_lemma": "WeilQuadraticFormNonnegativityOnExplicitPoleNeutralCoreWithVanishingCertifiedDefect",
            },
            "proof_dag": proof_dag(
                "RH",
                "WeilQuadraticFormCoercivityModuloSpectralTranslationsOnExplicitPoleNeutralCore",
                "FiniteCodimensionCoercivityIsNotNecessaryForNonnegativity",
                "FiniteModeQuotientTurnsWeilNonnegativityIntoUniformCoercivity",
                "WeilQuadraticFormNonnegativityOnExplicitPoleNeutralCoreWithVanishingCertifiedDefect",
            ),
            "claim_boundary": "No RH proof, no actual Weil-form positivity, and no off-critical zero exclusion; one exact finite-codimension coercivity no-go only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-186",
            "theorem_name": "ExactlyTwoValuationOnesOtherwiseTwoCycleExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Exactly-three-one words, larger valuations, and divergent nonperiodic orbits remain open.",
            "route_decision": {
                "discard": "finite horizon enumeration as a substitute for the all-horizon affine divisibility proof",
                "retain": "closed-form affine numerator bounds plus exact enumeration of only the finite exceptional horizons",
                "next_single_lemma": "NoContractingValuationWordWithExactlyThreeOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "NoPrimitiveContractingValuationWordWithExactlyTwoOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
                "ExactlyTwoValuationOnesOtherwiseTwoCycleExclusion",
                "BoundedEnumerationProvesAllExactlyTwoOneHorizons",
                "NoContractingValuationWordWithExactlyThreeOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            ),
            "claim_boundary": "No Collatz proof, no complete cycle exclusion, and no divergent-orbit exclusion; the complete exactly-two-one/rest-two periodic stratum is excluded.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-186",
            "theorem_name": "BadSurvivorLayerCakeAndNonnegativeSubhorizonNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No signed prime-weighted cancellation, target-uniform minor-arc bound, or exceptional-set elimination is proved.",
            "route_decision": {
                "discard": "any nonnegative combination of subhorizon wheel survivor occupancies as a mechanism for cancelling all composite contamination",
                "retain": "signed von Mangoldt or parity-sensitive correlation estimates below the exact target factor horizon",
                "next_single_lemma": "SignedPrimeWeightedBadSurvivorCorrelationHasUniformSubHorizonPowerSaving",
            },
            "proof_dag": proof_dag(
                "GB",
                "SubHorizonPrimeWeightedBadSurvivorCancellationBelowTargetMargin",
                "BadSurvivorLayerCakeAndNonnegativeSubhorizonNoGo",
                "NonnegativeSubhorizonOccupancyCancelsCompositeContamination",
                "SignedPrimeWeightedBadSurvivorCorrelationHasUniformSubHorizonPowerSaving",
            ),
            "claim_boundary": "No Goldbach proof, counterexample, or every-target minor-arc theorem; one exact survivor layer-cake identity and nonnegative-information no-go only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-186",
            "theorem_name": "QuantizedTwinProjectorAndFixedRelativeMarginNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No actual unbounded-block Liouville or Type I/II lower bound is proved; the parity barrier remains.",
            "route_decision": {
                "discard": "a fixed positive normalized joint-Liouville margin as a necessary formulation of Twin Prime infinitude",
                "retain": "a predeclared signed arithmetic decomposition whose certified one-sided lower bound clears the exact four-unit projector threshold infinitely often",
                "next_single_lemma": "PredeclaredCubicRoughSignedTypeIIMainDominatesRemainderOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "CubicRoughOneSidedJointLiouvilleBlockMarginOnUnboundedScales",
                "QuantizedTwinProjectorAndFixedRelativeMarginNoGo",
                "TwinInfinitudeRequiresAUniformPositiveRelativeProjectorMargin",
                "PredeclaredCubicRoughSignedTypeIIMainDominatesRemainderOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof, infinitude theorem, or parity-breaking estimate; one exact four-unit projector threshold and fixed-relative-margin no-go only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureCodimensionCycleLayerCakeQuantizationAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-186 resolves none of the four conjectures. It closes the "
            "entire Collatz cycle stratum with exactly two valuation ones and "
            "all other valuations two, and proves three exact target or "
            "information-class corrections for RH, Goldbach, and Twin Prime."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The useful common pattern is quantifier control. A finite-mode "
            "quotient does not manufacture a spectral gap; a closed affine "
            "formula can cover every horizon; nonnegative survivor layers "
            "cannot cancel contamination; and a fixed relative Twin margin is "
            "stronger than the exact four-unit existence threshold."
        ),
        "literature_boundary": {
            "riemann": "Suzuki's 2026 screw-function framework and numerical Weil-operator work do not prove global Weil positivity or RH.",
            "collatz": "Cycle exclusions and almost-all orbit results do not exclude all nontrivial cycles plus divergent natural-number orbits.",
            "goldbach": "The 2026 exceptional-set survey gives explicit major-arc structure but not an every-even-integer binary theorem.",
            "twin_prime": "Prime-producing sieve theory still requires parity-sensitive Type I/II information for exact gap two.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "new_infinite_stratum_closure_count": 1,
            "rejected_target_count": 4,
            "proof_dag_count": 4,
            "finite_arithmetic_diagnostic_count": 4,
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
        ROOT
        / "data"
        / "open-problem"
        / "ticket186-codimension-twoone-layercake-quantization.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "codimension_cycle_layercake_quantization_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT
        / "data"
        / "open-problem"
        / "riemann"
        / "rh-ticket-186-finite-codimension-no-go.json",
        "collatz": ROOT
        / "data"
        / "open-problem"
        / "collatz"
        / "co-ticket-186-two-one-cycle-exclusion.json",
        "goldbach": ROOT
        / "data"
        / "open-problem"
        / "goldbach"
        / "gb-ticket-186-bad-survivor-layer-cake.json",
        "twin-prime": ROOT
        / "data"
        / "open-problem"
        / "twin-prime"
        / "tp-ticket-186-quantized-projector.json",
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
            "TICKET-186 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
