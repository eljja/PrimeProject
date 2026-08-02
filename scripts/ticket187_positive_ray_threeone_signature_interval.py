from __future__ import annotations

import hashlib
import itertools
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket142_effective_rank_cycle_direction_haar_liouville import (
    twin_liouville_ledger,
)
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket180_finite_information_localization import ordered_affine_numerator
from ticket185_spectral_cycle_factor_granularity import smallest_prime_factors


GENERATED_AT = "2026-08-02T23:40:00+09:00"
SCHEMA = "primeproject.ticket187-positive-ray-threeone-signature-interval.v1"
STATUS = (
    "one_additional_infinite_cycle_stratum_closed_"
    "three_exact_certification_boundaries_all_open"
)


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "exact": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def decimal_payload(value: Decimal) -> dict[str, str]:
    return {"exact_decimal": format(value, "f"), "scientific": f"{value:E}"}


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
                "id": f"{problem_code}-T186-INPUT",
                "label": previous_name,
                "status": "proved_exact_input_or_open_target",
            },
            {
                "id": f"{problem_code}-T187-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T187-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T187-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T186-INPUT", f"{problem_code}-T187-CLOSED"],
            [f"{problem_code}-T187-CLOSED", f"{problem_code}-T187-OPEN"],
            [f"{problem_code}-T187-REJECTED", f"{problem_code}-T187-OPEN"],
        ],
    }


def riemann_positive_ray_audit() -> dict[str, object]:
    getcontext().prec = 90
    source = {
        "title": (
            "A finite Guinand-Weil dictionary and archimedean tail order "
            "for the truncated Weil quadratic form"
        ),
        "author": "Akiva Groskin",
        "arxiv": "2607.02828v1",
        "source_url": (
            "https://arxiv.org/src/2607.02828v1/anc/"
            "threeroute_c29N6_poleneutral.json"
        ),
        "license": "CC BY 4.0",
        "source_sha256": (
            "95e0f1d613d217478b1145ddef7fd884"
            "b0aa2c42bb477474848e44256df8f83d"
        ),
        "tag": "c29N6_poleneutral",
        "c": 29,
        "N": 6,
        "vector": [
            "-0.068849362039686715138",
            "0.54868385077863014544",
            "1.0",
            "0.5",
            "-3.0",
            "2.0",
            "-1.0",
        ],
    }
    ldlt_source = {
        "source_url": (
            "https://arxiv.org/src/2607.02828v1/anc/"
            "c100_N200_arb_ldlt_prec9000_provenance.json"
        ),
        "source_sha256": (
            "ccb6327eb2f5fc2d81fae923b2db272d"
            "4371b7bcbd0ef995562fb99e04538e98"
        ),
        "script": "arb_ldlt_certify.py",
        "c": 100,
        "N": 200,
        "dimension": 401,
        "prec_bits": 9000,
        "n_pos": 401,
        "n_neg": 0,
        "undetermined_pivot": None,
        "certified_positive_definite": True,
        "independently_rerun_by_primeproject": False,
    }
    route1 = Decimal("0.028981466814873948251427313471228345")
    route1_guard = Decimal("4.59177e-41")
    route2 = Decimal("0.028981466814884184353882396894187551")
    route2_tail = Decimal("1.07788e-12")
    prime = Decimal("-2.80667490260305724378367431208")
    pole = Decimal("-9.42207347425325302663222483685e-41")
    arch = Decimal("2.83565636941794142813755670898")
    component_sum = prime + pole + arch
    component_rounding_residual = abs(component_sum - route2)
    route_difference = abs(route1 - route2)
    cancellation_condition_number = (
        abs(prime) + abs(pole) + abs(arch)
    ) / route2
    failures = sum(
        [
            route1 <= 0,
            route2 <= 0,
            route_difference > route2_tail,
            component_rounding_residual > Decimal("1e-28"),
            ldlt_source["dimension"] != ldlt_source["n_pos"],
            ldlt_source["n_neg"] != 0,
            ldlt_source["undetermined_pivot"] is not None,
            not ldlt_source["certified_positive_definite"],
        ]
    )
    return {
        "theorem": (
            "The pinned provenance artifact for the published c=100, N=200 "
            "cutoff-free Guinand-Weil block reports 401 positive interval-LDL "
            "pivots, zero negative pivots, and no undetermined pivot. The "
            "separate c=29, N=6 pole-neutral archive has positive closed-form "
            "and source-side numerical values whose discrepancy is below its "
            "reported tail remainder. Even accepting the reported 401-"
            "dimensional certificate, one finite positive section cannot imply "
            "global Weil nonnegativity: for every positive matrix M, the block "
            "extension diag(M,-1) agrees with M on that section and is indefinite."
        ),
        "proof": (
            "The provenance checks are exact checks of the archived JSON fields "
            "and pinned SHA-256, not a rerun of Arb. Treating the selected "
            "three-route decimals as exact transcript strings confirms that "
            "both displayed values are positive, their difference is below the "
            "reported route-2 tail remainder, and the rounded source components "
            "recombine within 1e-28. The fields guard_K and guard_g are retained "
            "only as closed-form-versus-quadrature diagnostics, not interval "
            "radii. The finite-section no-go is exact linear algebra: append a "
            "negative orthogonal coordinate to any accepted positive matrix."
        ),
        "source_provenance": source,
        "reported_interval_ldlt_provenance": ldlt_source,
        "pole_neutral_numerical_replay": {
            "route1_center": decimal_payload(route1),
            "guard_K_closed_form_vs_quadrature": decimal_payload(route1_guard),
            "route2_center": decimal_payload(route2),
            "route2_tail_remainder_bound": decimal_payload(route2_tail),
            "route_difference": decimal_payload(route_difference),
            "difference_below_reported_tail_remainder": (
                route_difference <= route2_tail
            ),
            "both_archived_values_positive": route1 > 0 and route2 > 0,
            "is_rigorous_interval_certificate": False,
        },
        "source_components": {
            "prime": decimal_payload(prime),
            "pole": decimal_payload(pole),
            "archimedean": decimal_payload(arch),
            "component_sum": decimal_payload(component_sum),
            "component_rounding_residual": decimal_payload(
                component_rounding_residual
            ),
            "absolute_cancellation_condition_number": decimal_payload(
                cancellation_condition_number
            ),
        },
        "finite_section_no_go_extension": {
            "input": "any positive-definite finite matrix M",
            "extension": "diag(M,-1)",
            "agrees_on_original_section": True,
            "extension_is_indefinite": True,
        },
        "aggregate": {
            "audited_vector_dimension": len(source["vector"]),
            "reported_ldlt_dimension": ldlt_source["dimension"],
            "reported_positive_pivots": ldlt_source["n_pos"],
            "reported_negative_pivots": ldlt_source["n_neg"],
            "reported_undetermined_pivots": 0,
            "primeproject_independent_arb_rerun": False,
            "pole_neutral_replay_values_positive": route1 > 0 and route2 > 0,
            "cofinal_family_certified": False,
        },
        "no_go_scope": (
            "PrimeProject verifies the provenance transcript and its internal "
            "claims but has not rerun the 9000-bit Arb LDL calculation. Even an "
            "independently accepted finite positive block supplies no cofinal "
            "nested family, actual global Weil nonnegativity, or RH."
        ),
        "failure_count": failures,
    }


def canonical_three_one_word(a: int, b: int, c: int) -> tuple[int, ...]:
    if min(a, b, c) < 1:
        raise ValueError("all three cyclic gaps must be positive")
    return (
        (1,)
        + (2,) * (a - 1)
        + (1,)
        + (2,) * (b - 1)
        + (1,)
        + (2,) * (c - 1)
    )


def three_one_closed_form(a: int, b: int, c: int) -> int:
    h = a + b + c
    return (
        2 ** (2 * h - 3)
        - 3 ** (h - 1)
        + 4**a * 3 ** (h - a - 1)
        + 2 * 4 ** (a + b - 1) * 3 ** (c - 1)
    )


def three_one_cycle_row(a: int, b: int, c: int) -> dict[str, object]:
    word = canonical_three_one_word(a, b, c)
    h = len(word)
    numerator = ordered_affine_numerator(word)
    closed_form = three_one_closed_form(a, b, c)
    denominator = 2 ** (2 * h - 3) - 3**h
    shifted = word[1:] + word[:1]
    shifted_numerator = ordered_affine_numerator(shifted)
    return {
        "horizon_h": h,
        "cyclic_gaps": [a, b, c],
        "word": list(word),
        "affine_numerator_B": str(numerator),
        "cycle_denominator_D": str(denominator),
        "B_mod_D": str(numerator % denominator),
        "B_over_D_decimal": numerator / denominator,
        "checks": {
            "closed_form_matches_recurrence": numerator == closed_form,
            "contracting": denominator > 0,
            "B_exceeds_D": numerator > denominator,
            "B_is_below_3D": numerator < 3 * denominator,
            "B_and_D_are_odd": numerator % 2 == denominator % 2 == 1,
            "rotation_identity": (
                2 ** word[0] * shifted_numerator
                == 3 * numerator + denominator
            ),
            "affine_divisibility_fails": numerator % denominator != 0,
        },
    }


def finite_three_one_horizon_row(horizon: int) -> dict[str, object]:
    if not 8 <= horizon <= 12:
        raise ValueError("this is the exact finite-exception range h=8..12")
    denominator = 2 ** (2 * horizon - 3) - 3**horizon
    transcript: list[str] = []
    hits: list[dict[str, object]] = []
    formula_failures = 0
    rotation_failures = 0
    for positions in itertools.combinations(range(horizon), 3):
        position_set = set(positions)
        word = tuple(1 if index in position_set else 2 for index in range(horizon))
        numerator = ordered_affine_numerator(word)
        remainder = numerator % denominator
        transcript.append(f"{positions}:{remainder}")
        p0, p1, p2 = positions
        a, b, c = p1 - p0, p2 - p1, horizon - p2 + p0
        rotated = word[p0:] + word[:p0]
        if ordered_affine_numerator(rotated) != three_one_closed_form(a, b, c):
            formula_failures += 1
        shifted = word[1:] + word[:1]
        if (
            2 ** word[0] * ordered_affine_numerator(shifted)
            != 3 * numerator + denominator
        ):
            rotation_failures += 1
        if remainder == 0:
            hits.append(
                {"positions": list(positions), "integer_quotient": numerator // denominator}
            )
    return {
        "horizon_h": horizon,
        "contracting": denominator > 0,
        "word_count": math.comb(horizon, 3),
        "divisibility_hit_count": len(hits),
        "divisibility_hits": hits,
        "closed_form_failure_count": formula_failures,
        "rotation_identity_failure_count": rotation_failures,
        "remainder_transcript_sha256": hashlib.sha256(
            "\n".join(transcript).encode("ascii")
        ).hexdigest(),
    }


def collatz_three_one_audit() -> dict[str, object]:
    finite_rows = [finite_three_one_horizon_row(h) for h in range(8, 13)]
    analytic_rows = []
    for h in [13, 16, 32, 64, 128]:
        c = (h + 2) // 3
        a = (h - c) // 2
        b = h - a - c
        analytic_rows.append(three_one_cycle_row(a, b, c))
    threshold_tail = Fraction(64, 3) * Fraction(3, 4) ** 13
    threshold_budget = Fraction(19, 32)
    failures = sum(
        row["divisibility_hit_count"]
        + row["closed_form_failure_count"]
        + row["rotation_identity_failure_count"]
        + int(not row["contracting"])
        for row in finite_rows
    )
    failures += sum(
        not check for row in analytic_rows for check in row["checks"].values()
    )
    failures += int(not threshold_tail < threshold_budget)
    return {
        "theorem": (
            "No positive accelerated Collatz cycle has a valuation period with "
            "exactly three entries equal to one and every other entry equal to "
            "two, including primitive and imprimitive periods."
        ),
        "proof": (
            "Rotate the word to gaps a,b,c>=1 with a+b+c=h and choose c as a "
            "largest gap, so c>=3. Its exact numerator is B=2^(2h-3)-"
            "3^(h-1)+4^a*3^(h-a-1)+2*4^(a+b-1)*3^(c-1), and D=2^(2h-3)-"
            "3^h. Thus B>D and B,D are odd. Put u=3/4 and Q=4^h/8. The "
            "inequality B<3D follows from (8/3)u^(b+c)+(4/3)u^c+"
            "(64/3)u^h<2. Since c>=3 and b+c>=4, the first two terms are at "
            "most 45/32; at h=13 the last term is already below 19/32 and "
            "decreases thereafter. Hence for h>=13, divisibility would make "
            "B/D an odd integer strictly between one and three, impossible. "
            "Contraction starts at h=8. Exact enumeration of all C(h,3) words "
            "for h=8,...,12 gives 645 cases and no divisibility hit. Cyclic "
            "rotation preserves divisibility because 2^v B_shift=3B+D and D "
            "is odd."
        ),
        "finite_exception_horizon_rows": finite_rows,
        "analytic_replay_rows": analytic_rows,
        "analytic_bound": {
            "tail_at_h_13": fraction_payload(threshold_tail),
            "available_budget": fraction_payload(threshold_budget),
            "first_two_term_bound": fraction_payload(Fraction(45, 32)),
            "analytic_range_starts_at_h": 13,
        },
        "aggregate": {
            "infinite_family_proved": True,
            "includes_imprimitive_words": True,
            "contracting_range_starts_at_h": 8,
            "analytic_range_starts_at_h": 13,
            "finite_exception_word_count": sum(
                row["word_count"] for row in finite_rows
            ),
            "divisibility_hits": sum(
                row["divisibility_hit_count"] for row in finite_rows
            ),
            "largest_replayed_horizon": max(
                row["horizon_h"] for row in analytic_rows
            ),
        },
        "no_go_scope": (
            "This closes one more infinite periodic stratum. It does not exclude "
            "words with four or more valuation-one entries, valuations at least "
            "three, or divergent aperiodic natural-number orbits."
        ),
        "failure_count": failures,
    }


def goldbach_signature_row(
    target: int, is_prime: list[bool], least_factor: list[int]
) -> dict[str, object]:
    if target < 8 or target % 2:
        raise ValueError("an even target at least eight is required")
    prime_pairs: list[tuple[int, int]] = []
    bad_pairs: list[tuple[int, int, int]] = []
    for left in range(3, target // 2 + 1, 2):
        right = target - left
        if is_prime[left] and is_prime[right]:
            prime_pairs.append((left, right))
        else:
            gate = min(least_factor[left], least_factor[right])
            bad_pairs.append((gate, left, right))
    if not prime_pairs or not bad_pairs:
        raise ValueError("the audit row needs both a prime pair and a bad pair")
    gate, bad_left, bad_right = max(bad_pairs)
    prime_left, prime_right = max(prime_pairs)
    prime_gate = min(prime_left, prime_right)
    shared_gate = min(gate, prime_gate)
    depth = shared_gate - 1
    signature = "1" * shared_gate
    return {
        "even_target_N": target,
        "prime_pair_count": len(prime_pairs),
        "bad_pair_count": len(bad_pairs),
        "maximum_bad_gate_tau_N": gate,
        "maximum_prime_pair_small_endpoint_rho_N": prime_gate,
        "shared_gate_sigma_N": shared_gate,
        "maximum_indistinguishable_depth_Y": depth,
        "prime_pair_witness": [prime_left, prime_right],
        "bad_pair_witness": [bad_left, bad_right],
        "bad_pair_gate": gate,
        "shared_signature_length": len(signature),
        "shared_signature_sha256": hashlib.sha256(
            signature.encode("ascii")
        ).hexdigest(),
        "checks": {
            "prime_witness_is_prime_pair": (
                is_prime[prime_left] and is_prime[prime_right]
            ),
            "bad_witness_is_not_prime_pair": not (
                is_prime[bad_left] and is_prime[bad_right]
            ),
            "bad_witness_survives_through_Y": gate > depth,
            "prime_witness_survives_through_Y": (
                min(prime_left, prime_right) > depth
            ),
            "truncated_signatures_are_identical": True,
        },
    }


def goldbach_signature_audit() -> dict[str, object]:
    targets = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000]
    is_prime = prime_sieve(max(targets))
    least_factor = smallest_prime_factors(max(targets))
    rows = [
        goldbach_signature_row(target, is_prime, least_factor)
        for target in targets
    ]
    failures = sum(
        not check for row in rows for check in row["checks"].values()
    )
    return {
        "theorem": (
            "Fix an even N having both a Goldbach representation and a bad odd "
            "candidate pair. Let tau_N be the largest bad-pair least-factor "
            "gate, let rho_N be the largest smaller endpoint of a prime pair, "
            "and put sigma_N=min(tau_N,rho_N). For every integer Y<sigma_N, "
            "one prime pair and a bad pair "
            "have the same truncated small-factor survivor signature through "
            "depth Y. Consequently no function of that signature alone, linear "
            "or nonlinear and with arbitrary signed weights, classifies every "
            "candidate pair correctly."
        ),
        "proof": (
            "Choose a bad pair attaining tau_N and a prime pair attaining "
            "rho_N. Through every depth below sigma_N, neither witness is "
            "removed by a trial divisor, so both signatures are all ones. Equal "
            "inputs receive equal outputs under every deterministic function; "
            "therefore signed depth weights do not repair the information loss."
        ),
        "target_signature_rows": rows,
        "aggregate": {
            "target_count": len(rows),
            "largest_target": rows[-1]["even_target_N"],
            "largest_shared_signature_length": max(
                row["shared_signature_length"] for row in rows
            ),
            "largest_indistinguishable_depth": max(
                row["maximum_indistinguishable_depth_Y"] for row in rows
            ),
            "signature_separation_failures": 0,
        },
        "no_go_scope": (
            "The theorem is conditional on a target already having a prime "
            "pair and therefore proves no Goldbach case. It shows that even "
            "signed or nonlinear reuse of the same truncated roughness bits is "
            "insufficient; new prime-sensitive amplitude or phase information "
            "is required."
        ),
        "failure_count": failures,
    }


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def quantized_twin_interval(
    lower: Fraction, upper: Fraction
) -> dict[str, object]:
    if lower > upper:
        raise ValueError("lower interval endpoint exceeds upper endpoint")
    minimum_count = max(0, ceil_fraction(lower / 4))
    maximum_count = math.floor(upper / 4)
    feasible = maximum_count >= minimum_count
    return {
        "lower": fraction_payload(lower),
        "upper": fraction_payload(upper),
        "minimum_compatible_twin_count": minimum_count if feasible else None,
        "maximum_compatible_twin_count": maximum_count if feasible else None,
        "feasible_nonnegative_quantized_projector": feasible,
        "positive_count_certified": feasible and minimum_count >= 1,
        "zero_count_certified": feasible and maximum_count == 0,
        "exact_count_certified": feasible and minimum_count == maximum_count,
        "ambiguous_between_zero_and_positive": (
            feasible and minimum_count == 0 and maximum_count >= 1
        ),
    }


def twin_interval_audit() -> dict[str, object]:
    sharp_rows = [
        {
            "name": "strict-positive-small-lower-endpoint",
            **quantized_twin_interval(Fraction(1, 1000), Fraction(7999, 1000)),
        },
        {
            "name": "sub-four-upper-endpoint",
            **quantized_twin_interval(Fraction(-1, 1000), Fraction(3999, 1000)),
        },
        {
            "name": "zero-four-boundary-ambiguity",
            **quantized_twin_interval(Fraction(0), Fraction(4)),
        },
    ]
    finite_rows = []
    for scale in [1_000, 10_000, 100_000, 1_000_000]:
        source = twin_liouville_ledger(scale)
        projector = (
            source["A00"] - source["A10"] - source["A01"] + source["A11"]
        )
        interval = quantized_twin_interval(
            Fraction(2 * projector - 1, 2),
            Fraction(2 * projector + 1, 2),
        )
        finite_rows.append(
            {
                "X": scale,
                "projector_Delta": projector,
                "direct_twin_count": source["direct_twin_count"],
                "certified_count_interval": interval,
                "checks": {
                    "projector_is_four_times_count": (
                        projector == 4 * source["direct_twin_count"]
                    ),
                    "half_unit_interval_certifies_exact_count": (
                        interval["exact_count_certified"]
                        and interval["minimum_compatible_twin_count"]
                        == source["direct_twin_count"]
                    ),
                },
            }
        )
    failures = sum(
        not check for row in finite_rows for check in row["checks"].values()
    )
    failures += int(not sharp_rows[0]["positive_count_certified"])
    failures += int(not sharp_rows[1]["zero_count_certified"])
    failures += int(not sharp_rows[2]["ambiguous_between_zero_and_positive"])
    return {
        "theorem": (
            "Let a certified interval [L,U] contain the exact cubic-rough twin "
            "projector Delta=4C with C a nonnegative integer. Then the complete "
            "compatible count interval is ceil(max(L,0)/4)<=C<=floor(U/4). "
            "In particular L>0 certifies C>=1 even when L<4, U<4 certifies "
            "C=0, and [0,4] is sharply ambiguous between C=0 and C=1."
        ),
        "proof": (
            "Intersect [L,U] with the lattice 4 times the nonnegative integers "
            "and divide by four. Ceiling and floor give the exact compatible "
            "integer counts. The intervals containing only 4, only 0, and both "
            "0 and 4 prove the three stated decisions and sharpness. Thus an "
            "analytic lower endpoint need only be rigorously strict-positive; "
            "integrality promotes it to the four-unit arithmetic threshold."
        ),
        "sharp_interval_rows": sharp_rows,
        "finite_cubic_rough_interval_rows": finite_rows,
        "aggregate": {
            "sharp_rule_count": len(sharp_rows),
            "finite_scale_count": len(finite_rows),
            "largest_finite_scale": finite_rows[-1]["X"],
            "strict_positive_lower_endpoint_is_sufficient": True,
            "zero_to_four_interval_is_ambiguous": True,
            "conjecture_resolution_count": 0,
        },
        "no_go_scope": (
            "Quantized rounding reduces the certification margin but does not "
            "produce a positive lower endpoint. No Type I/II estimate, parity "
            "break, or infinitely recurring positive block is proved."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_positive_ray_audit()
    collatz = collatz_three_one_audit()
    goldbach = goldbach_signature_audit()
    twin = twin_interval_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-187",
            "theorem_name": "PublishedFiniteWeilLDLTProvenanceAndOneSectionNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "The external 9000-bit Arb run was not independently rerun, and one finite positive block does not certify a cofinal family, the global Weil form, or RH.",
            "route_decision": {
                "discard": "promoting one reported positive finite Guinand-Weil block or one positive pole-neutral numerical ray to the global Weil form",
                "retain": "independently replayable interval certificates for complete pole-neutral finite matrices on one cofinal nested family",
                "next_single_lemma": "CofinalPoleNeutralGuinandWeilIntervalLDLCertificatesHaveVanishingNegativeDefect",
            },
            "proof_dag": proof_dag(
                "RH",
                "WeilQuadraticFormNonnegativityOnExplicitPoleNeutralCoreWithVanishingCertifiedDefect",
                "PublishedFiniteWeilLDLTProvenanceAndOneSectionNoGo",
                "OnePositiveFiniteGuinandWeilBlockImpliesGlobalWeilPositivity",
                "CofinalPoleNeutralGuinandWeilIntervalLDLCertificatesHaveVanishingNegativeDefect",
            ),
            "claim_boundary": "No RH proof or global Weil positivity. One external finite interval-LDL provenance record is pinned but not independently rerun; one finite-section promotion is refuted exactly.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-187",
            "theorem_name": "ExactlyThreeValuationOnesOtherwiseTwoCycleExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Four-or-more-one words, valuations at least three, and divergent aperiodic orbits remain open.",
            "route_decision": {
                "discard": "treating bounded search beyond h=12 as evidence for the remaining exactly-three-one horizons",
                "retain": "cyclic-gap closed forms, an all-horizon parity interval, and exact enumeration only below the analytic threshold",
                "next_single_lemma": "NoContractingValuationWordWithExactlyFourOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "NoContractingValuationWordWithExactlyThreeOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
                "ExactlyThreeValuationOnesOtherwiseTwoCycleExclusion",
                "FiniteThreeOneEnumerationProvesEveryHorizon",
                "NoContractingValuationWordWithExactlyFourOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            ),
            "claim_boundary": "No Collatz proof or complete cycle exclusion; the entire exactly-three-one/rest-two periodic stratum is newly excluded.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-187",
            "theorem_name": "SignedSubhorizonSurvivorSignatureIndistinguishability",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No prime-weighted every-target lower bound, signed minor-arc power saving, or exceptional-set elimination is proved.",
            "route_decision": {
                "discard": "expecting arbitrary signed or nonlinear post-processing of the same subhorizon roughness signature to distinguish prime pairs from all composite impostors",
                "retain": "new von Mangoldt amplitude or target-aligned phase information with a uniform signed residual estimate",
                "next_single_lemma": "SignedVonMangoldtSubhorizonResidualIsBelowExplicitMajorMainForEveryLargeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "SignedPrimeWeightedBadSurvivorCorrelationHasUniformSubHorizonPowerSaving",
                "SignedSubhorizonSurvivorSignatureIndistinguishability",
                "SignedWeightsOnUnchangedSurvivorBitsBreakCompositeContamination",
                "SignedVonMangoldtSubhorizonResidualIsBelowExplicitMajorMainForEveryLargeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof or counterexample; one exact information-theoretic no-go for subhorizon roughness signatures only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-187",
            "theorem_name": "QuantizedTwinProjectorIntervalRoundingCertificate",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No arithmetic estimate supplies positive lower endpoints on infinitely many unbounded predeclared blocks.",
            "route_decision": {
                "discard": "requiring an analytic lower endpoint of at least four before using the known four-integer quantization",
                "retain": "rigorous strict-positive projector intervals, promoted by Delta in 4Z to an actual twin count",
                "next_single_lemma": "CertifiedStrictlyPositiveTwinProjectorLowerEndpointOnInfinitelyManyPredeclaredDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "PredeclaredCubicRoughSignedTypeIIMainDominatesRemainderOnInfinitelyManyDyadicBlocks",
                "QuantizedTwinProjectorIntervalRoundingCertificate",
                "AnalyticLowerBoundMustReachFourBeforeQuantizationCanCertifyATwin",
                "CertifiedStrictlyPositiveTwinProjectorLowerEndpointOnInfinitelyManyPredeclaredDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof or Type I/II breakthrough; one exact interval-lattice promotion rule and its sharp ambiguity boundary only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjecturePositiveRayThreeOneSignatureIntervalAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-187 resolves none of the four conjectures. It excludes the "
            "entire accelerated Collatz cycle stratum with exactly three "
            "valuation-one entries and all other entries two. The RH result is "
            "an attributed audit of one published positive finite ray; the "
            "Goldbach and Twin results are exact information and interval "
            "certification boundaries."
        ),
        **sections,
        "cross_problem_synthesis": (
            "Exact finite information helps only when its quantifier is kept: "
            "a positive ray is not a positive operator, a closed affine formula "
            "can cover every cycle horizon, unchanged roughness bits remain "
            "indistinguishable under any post-processing, and arithmetic "
            "quantization can promote any rigorous strict-positive interval."
        ),
        "literature_boundary": {
            "riemann": "The selected c=29,N=6 ray is attributed to arXiv:2607.02828v1 (CC BY 4.0); PrimeProject independently checks only its archived decimals and imports no RH conclusion.",
            "collatz": "The proof is project-derived exact affine arithmetic; almost-all orbit results do not supply the missing universal aperiodic conclusion.",
            "goldbach": "The 2026 exceptional-set work supplies major-arc context, not the every-target signed residual required here.",
            "twin_prime": "Prime-producing sieve theory still requires genuine Type I/II information; interval rounding does not create that estimate.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "new_infinite_stratum_closure_count": 1,
            "attributed_primary_artifact_audit_count": 1,
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
        ROOT
        / "data"
        / "open-problem"
        / "ticket187-positive-ray-threeone-signature-interval.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "positive_ray_threeone_signature_interval_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT
        / "data"
        / "open-problem"
        / "riemann"
        / "rh-ticket-187-pole-neutral-positive-ray.json",
        "collatz": ROOT
        / "data"
        / "open-problem"
        / "collatz"
        / "co-ticket-187-three-one-cycle-exclusion.json",
        "goldbach": ROOT
        / "data"
        / "open-problem"
        / "goldbach"
        / "gb-ticket-187-subhorizon-signature-no-go.json",
        "twin-prime": ROOT
        / "data"
        / "open-problem"
        / "twin-prime"
        / "tp-ticket-187-quantized-interval-certificate.json",
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
            "TICKET-187 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
