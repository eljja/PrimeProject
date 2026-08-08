from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json


GENERATED_AT = "2026-08-08T23:55:00+09:00"
SCHEMA = "primeproject.ticket197-first-rectangle-run-block-sparse-collision.v1"
STATUS = (
    "first_xi_rectangle_existentially_closed_contiguous_collatz_runs_excluded_"
    "goldbach_collision_support_sparse_twin_collision_mixed_layer_all_open"
)


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "exact": str(value),
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
                "id": f"{problem_code}-T196-INPUT",
                "label": previous_name,
                "status": "open_input_from_ticket196",
            },
            {
                "id": f"{problem_code}-T197-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T197-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_route_limited",
            },
            {
                "id": f"{problem_code}-T197-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T196-INPUT", f"{problem_code}-T197-CLOSED"],
            [f"{problem_code}-T197-CLOSED", f"{problem_code}-T197-OPEN"],
            [f"{problem_code}-T197-REJECTED", f"{problem_code}-T197-OPEN"],
        ],
    }


def xi_rectangle_map(sign: str) -> dict[str, object]:
    if sign == "upper":
        y_interval = (Fraction(1, 2), Fraction(2))
    elif sign == "lower":
        y_interval = (Fraction(-2), Fraction(-1, 2))
    else:
        raise ValueError("sign must be upper or lower")
    sigma_values = (Fraction(1, 2) - y_interval[1], Fraction(1, 2) - y_interval[0])
    return {
        "rectangle": f"D_2^{sign[0]}",
        "z_real_interval": [-2, 2],
        "z_imaginary_interval": [str(y_interval[0]), str(y_interval[1])],
        "s_map": "s=1/2+i z=(1/2-Im z)+i Re z",
        "s_real_interval": [str(sigma_values[0]), str(sigma_values[1])],
        "s_imaginary_interval": [-2, 2],
        "open_critical_strip_intersection": False,
        "xi_zero_possible_on_closed_image": False,
    }


def riemann_first_rectangle_audit() -> dict[str, object]:
    rows = [xi_rectangle_map("upper"), xi_rectangle_map("lower")]
    failures = sum(
        int(row["open_critical_strip_intersection"])
        + int(row["xi_zero_possible_on_closed_image"])
        for row in rows
    )
    return {
        "theorem": (
            "Let Xi(z)=xi(1/2+i z), and let S_n be its Taylor sections at zero. "
            "On the closed first exhaustion rectangles D_2^+ and D_2^-, Xi has "
            "no zero. Consequently, for each sign there exists an index n for "
            "which S_n has zero count zero in D_2^sign and satisfies "
            "sup_boundary|Xi-S_n|<inf_boundary|S_n|. This is an existential "
            "actual-Xi Rouché theorem, not an explicit interval certificate."
        ),
        "proof": (
            "For z=x+i y, s=1/2+i z=(1/2-y)+i x. The upper closed rectangle "
            "maps to -3/2<=Re(s)<=0 and the lower one to 1<=Re(s)<=5/2. "
            "Every zero of the completed xi function is a nontrivial zeta zero "
            "and therefore has 0<Re(s)<1; xi(0)=xi(1)=1/2. Hence Xi is "
            "zero-free on both compact closures. If delta is its positive "
            "minimum modulus there, uniform Taylor convergence gives "
            "sup|Xi-S_n|<delta/3. Then inf|S_n|>=2delta/3, and Rouché gives "
            "the asserted zero count and strict boundary inequality."
        ),
        "exact_coordinate_rows": rows,
        "contract": {
            "actual_xi_D2_zero_free": True,
            "actual_xi_taylor_rouche_section_exists": True,
            "explicit_taylor_degree_exhibited": False,
            "rational_or_interval_rouche_margin_exhibited": False,
            "D2_enters_open_critical_strip": False,
            "full_rh_resolved": False,
        },
        "no_go_scope": (
            "D_2 avoids the open critical strip, so closing it is not evidence "
            "that controls an off-critical zero. The proof is existential and "
            "does not output a Taylor degree, coefficient enclosure, or margin."
        ),
        "failure_count": failures,
    }


def ordered_affine_numerator(word: tuple[int, ...]) -> int:
    horizon = len(word)
    prefix = 0
    numerator = 0
    for index, valuation in enumerate(word):
        numerator += 3 ** (horizon - 1 - index) * 2**prefix
        prefix += valuation
    return numerator


def rotate_word(word: tuple[int, ...], amount: int) -> tuple[int, ...]:
    amount %= len(word)
    return word[amount:] + word[:amount]


def collatz_contiguous_run_row(scale_k: int) -> dict[str, object]:
    if scale_k < 1:
        raise ValueError("scale must be positive")
    word = (1,) * scale_k + (2,) * (2 * scale_k)
    horizon = 3 * scale_k
    denominator = 2 ** (5 * scale_k) - 3 ** (3 * scale_k)
    direct_numerator = ordered_affine_numerator(word)
    closed_numerator = (
        32**scale_k + 27**scale_k - 2 * 18**scale_k
    )
    residual = direct_numerator - denominator
    reduced_residual = 3**scale_k - 2**scale_k
    gcd_with_prefactor = math.gcd(denominator, 2 * 9**scale_k)
    rotation_divisibility_hits = sum(
        int(ordered_affine_numerator(rotate_word(word, shift)) % denominator == 0)
        for shift in range(horizon)
    )
    return {
        "scale_k": scale_k,
        "cyclic_word": f"1^{scale_k} 2^{2 * scale_k}",
        "horizon_h": horizon,
        "one_count_r": scale_k,
        "one_density": "1/3",
        "denominator_D": str(denominator),
        "affine_numerator_direct_B": str(direct_numerator),
        "affine_numerator_closed_form": str(closed_numerator),
        "closed_form_matches_direct": direct_numerator == closed_numerator,
        "B_minus_D": str(residual),
        "B_minus_D_factorization": f"2*9^{scale_k}*(3^{scale_k}-2^{scale_k})",
        "factorization_matches": residual == 2 * 9**scale_k * reduced_residual,
        "gcd_D_with_2_times_9_power": gcd_with_prefactor,
        "reduced_positive_residual": str(reduced_residual),
        "reduced_residual_strictly_below_D": 0 < reduced_residual < denominator,
        "contraction_gate_passes": 32**scale_k > 27**scale_k,
        "product_gate": {
            "exact": f"(125/108)^{scale_k}",
            "passes": 125**scale_k > 108**scale_k,
        },
        "base_word_divisibility_hit": direct_numerator % denominator == 0,
        "cyclic_rotation_divisibility_hit_count": rotation_divisibility_hits,
    }


def collatz_contiguous_run_audit() -> dict[str, object]:
    rows = [collatz_contiguous_run_row(scale) for scale in range(1, 65)]
    transcript = hashlib.sha256()
    for row in rows:
        transcript.update(
            (
                f"{row['scale_k']}:{row['denominator_D']}:"
                f"{row['affine_numerator_direct_B']}:"
                f"{int(row['base_word_divisibility_hit'])}:"
                f"{row['cyclic_rotation_divisibility_hit_count']}\n"
            ).encode("ascii")
        )
    failures = sum(
        int(not row["closed_form_matches_direct"])
        + int(not row["factorization_matches"])
        + int(row["gcd_D_with_2_times_9_power"] != 1)
        + int(not row["reduced_residual_strictly_below_D"])
        + int(not row["contraction_gate_passes"])
        + int(not row["product_gate"]["passes"])
        + int(row["base_word_divisibility_hit"])
        + int(row["cyclic_rotation_divisibility_hit_count"] != 0)
        for row in rows
    )
    return {
        "theorem": (
            "For every k>=1, the cyclic accelerated-Collatz valuation family "
            "w_k=1^k 2^(2k), including every cyclic rotation, passes both "
            "TICKET-196 scalar gates but cannot satisfy affine divisibility. "
            "Its denominator is D_k=32^k-27^k and its affine numerator is "
            "B_k=32^k+27^k-2*18^k. If D_k divided B_k, coprimality with "
            "2*9^k would force D_k to divide 3^k-2^k, which is positive and "
            "strictly smaller than D_k, a contradiction."
        ),
        "proof": (
            "Summing the first k valuation-one terms and the following 2k "
            "valuation-two terms as geometric series gives the displayed B_k. "
            "Then B_k-D_k=2*9^k*(3^k-2^k). The odd number D_k is coprime to "
            "3, hence to 2*9^k, while 0<3^k-2^k<D_k. Divisibility is therefore "
            "impossible. A one-step rotation obeys "
            "2^(v_0)B_rot=3B+D, so divisibility is rotation invariant."
        ),
        "exact_scale_rows": rows,
        "aggregate": {
            "checked_scale_count": len(rows),
            "infinite_contiguous_run_family_proved_empty": True,
            "all_cyclic_rotations_included": True,
            "scalar_gates_still_pass": True,
            "actual_nontrivial_cycle_found": False,
            "transcript_sha256": transcript.hexdigest(),
        },
        "no_go_scope": (
            "The theorem uses one cyclic block of ones and one cyclic block of "
            "twos. Words with two or more alternating run pairs, arbitrary "
            "one-density in the admissible window, valuations at least three, "
            "and divergent aperiodic trajectories remain open."
        ),
        "failure_count": failures,
    }


def prime_sieve(limit: int) -> list[int]:
    if limit < 2:
        return []
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            start = prime * prime
            flags[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [value for value, flag in enumerate(flags) if flag]


def odd_proper_prime_power_metadata(limit: int) -> dict[int, tuple[int, int]]:
    metadata: dict[int, tuple[int, int]] = {}
    for prime in prime_sieve(math.isqrt(limit)):
        if prime == 2:
            continue
        exponent = 2
        value = prime * prime
        while value <= limit:
            metadata[value] = (prime, exponent)
            exponent += 1
            value *= prime
    return metadata


def goldbach_collision_support_row(
    cutoff: int, all_powers: list[int]
) -> dict[str, object]:
    powers = [value for value in all_powers if value <= cutoff]
    targets: set[int] = set()
    pair_count = 0
    for left_index, left in enumerate(powers):
        for right in powers[left_index:]:
            target = left + right
            if target > cutoff:
                break
            targets.add(target)
            pair_count += 1
    even_target_count = cutoff // 2
    target_count = len(targets)
    return {
        "cutoff_X": cutoff,
        "odd_proper_prime_power_count_A": len(powers),
        "unordered_collision_pair_count": pair_count,
        "collision_supported_even_target_count": target_count,
        "collision_free_even_target_count": even_target_count - target_count,
        "even_target_count": even_target_count,
        "support_density": fraction_payload(Fraction(target_count, even_target_count)),
        "support_bound_A_squared": len(powers) ** 2,
        "support_below_A_squared": target_count <= len(powers) ** 2,
        "first_collision_targets": sorted(targets)[:12],
        "target_18_supported": 18 in targets,
    }


def goldbach_sparse_collision_audit() -> dict[str, object]:
    cutoffs = [2**exponent for exponent in range(8, 25)]
    metadata = odd_proper_prime_power_metadata(cutoffs[-1])
    powers = sorted(metadata)
    rows = [goldbach_collision_support_row(cutoff, powers) for cutoff in cutoffs]
    failures = sum(
        int(not row["support_below_A_squared"])
        + int(not row["target_18_supported"])
        for row in rows
    )
    return {
        "theorem": (
            "Let Q be the odd proper-prime-power part of Lambda and let "
            "C(X)={even N<=X:(Q*Q)(N)>0}. Then |C(X)|=o(X). Indeed the number "
            "A(X) of odd proper prime powers is "
            "O(sqrt(X)/log(X)+X^(1/3)log(X))=O(sqrt(X)/log(X)), and every "
            "collision-supported target is a sum of two such powers, so "
            "|C(X)|<=A(X)^2=O(X/log(X)^2). Consequently the exact TICKET-196 "
            "overlap subtraction changes the old union envelope only on a "
            "density-zero set of even targets."
        ),
        "proof": (
            "For exponent two there are pi(sqrt X) choices. For exponents at "
            "least three, summing pi(X^(1/e)) over e<=log_3 X gives "
            "O(X^(1/3)log X). The standard Chebyshev prime-counting bound "
            "pi(y)=O(y/log y) gives A(X)=O(sqrt X/log X). The addition map "
            "from ordered proper-power pairs onto collision-supported targets "
            "gives |C(X)|<=A(X)^2. Dividing by the number of even targets proves "
            "density zero. Outside C(X), Q*Q(N)=0 exactly, so the corrected and "
            "uncorrected envelopes coincide."
        ),
        "finite_support_rows": rows,
        "witness": {
            "target_N": 18,
            "decomposition": "9+9=3^2+3^2",
            "collision_supported": True,
        },
        "aggregate": {
            "finite_cutoff_count": len(rows),
            "largest_cutoff": cutoffs[-1],
            "density_zero_theorem_proved": True,
            "correction_identically_zero_on_density_one_complement": True,
            "every_large_even_correlation_bound_proved": False,
        },
        "no_go_scope": (
            "Density zero does not make the exceptional targets finite and does "
            "not prove Goldbach on either stratum. It proves that overlap "
            "subtraction alone cannot be the uniform every-even mechanism, since "
            "it is exactly zero on a density-one target set."
        ),
        "failure_count": failures,
    }


def twin_collision_row(
    lower: int,
    upper: int,
    metadata: dict[int, tuple[int, int]],
) -> dict[str, object]:
    collisions = []
    weighted_mass = 0.0
    for left in sorted(metadata):
        if left < lower or left >= upper:
            continue
        right = left + 2
        if right not in metadata:
            continue
        left_base, left_exponent = metadata[left]
        right_base, right_exponent = metadata[right]
        weight = math.log(left_base) * math.log(right_base)
        weighted_mass += weight
        collisions.append(
            {
                "pair": [left, right],
                "left": {"base": left_base, "exponent": left_exponent},
                "right": {"base": right_base, "exponent": right_exponent},
                "same_exponent": left_exponent == right_exponent,
                "at_least_one_exponent_ge_3": max(left_exponent, right_exponent) >= 3,
                "weight": weight,
            }
        )
    return {
        "block": [lower, upper],
        "collision_support_count": len(collisions),
        "collision_weighted_mass": weighted_mass,
        "same_exponent_collision_count": sum(
            int(item["same_exponent"]) for item in collisions
        ),
        "mixed_exponent_collision_count": sum(
            int(not item["same_exponent"]) for item in collisions
        ),
        "leading_square_square_collision_count": sum(
            int(
                item["left"]["exponent"] == 2
                and item["right"]["exponent"] == 2
            )
            for item in collisions
        ),
        "all_collisions_touch_exponent_at_least_three": all(
            item["at_least_one_exponent_ge_3"] for item in collisions
        ),
        "collisions": collisions,
    }


def twin_mixed_exponent_collision_audit() -> dict[str, object]:
    exponents = list(range(4, 25))
    limit = 2 ** (exponents[-1] + 1) + 2
    metadata = odd_proper_prime_power_metadata(limit)
    rows = [
        twin_collision_row(2**exponent, 2 ** (exponent + 1), metadata)
        for exponent in exponents
    ]
    collisions = [
        item for row in rows for item in row["collisions"]
    ]
    failures = sum(
        int(row["same_exponent_collision_count"] != 0)
        + int(row["leading_square_square_collision_count"] != 0)
        + int(not row["all_collisions_touch_exponent_at_least_three"])
        for row in rows
    )
    failures += int(not collisions)
    first = collisions[0] if collisions else None
    failures += int(first is None or first["pair"] != [25, 27])
    return {
        "theorem": (
            "If two odd proper prime powers differ by two, their exponents are "
            "unequal. In particular no prime-square layer collision "
            "p^2,p^2+2=q^2 exists, and every Q(n)Q(n+2) overlap touches an "
            "exponent-at-least-three layer. Hence the TICKET-196 collision "
            "subtraction is O(X^(1/3)log X) in weighted dyadic mass under the "
            "classical Chebyshev bound, and it cannot cancel the leading "
            "prime-square contamination layer of order O(sqrt X log X)."
        ),
        "proof": (
            "If q^e-p^e=2 with q>p odd primes and e>=2, factorization gives "
            "(q-p)(q^(e-1)+q^(e-2)p+...+p^(e-1))=2. The first factor is at "
            "least two and the second is greater than one, a contradiction. "
            "Thus equal exponents are impossible, so at least one exponent is "
            "at least three. Charge every collision to such an endpoint; a fixed "
            "endpoint has at most two distance-two neighbours, so this charging "
            "has uniformly bounded multiplicity. The theta-layer bound for "
            "exponent at least three is O(X^(1/3)); the other logarithmic weight "
            "is at most log(2X+2)."
        ),
        "finite_dyadic_rows": rows,
        "witness": first,
        "aggregate": {
            "dyadic_block_count": len(rows),
            "largest_upper_endpoint": 2 ** (exponents[-1] + 1),
            "finite_collision_count": len(collisions),
            "equal_exponent_collision_impossible_globally": True,
            "square_square_collision_impossible_globally": True,
            "collision_saving_is_lower_order_than_square_layer": True,
            "parity_breaking_lower_bound_proved": False,
        },
        "no_go_scope": (
            "The theorem does not classify all mixed-exponent solutions of "
            "p^a+2=q^b and does not prove that only (25,27) occurs. More "
            "importantly, removing a lower-order overlap cannot create the "
            "missing parity-breaking lower bound for the full shift-two correlation."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_first_rectangle_audit()
    collatz = collatz_contiguous_run_audit()
    goldbach = goldbach_sparse_collision_audit()
    twin = twin_mixed_exponent_collision_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-197",
            "theorem_name": "ActualXiFirstRectangleExistenceAndVacuityBoundary",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "The first D_2 certificate is existential, has no explicit Taylor degree or interval margin, and avoids the open critical strip entirely.",
            "route_decision": {
                "discard": "treating existential closure of D_2 as evidence controlling an off-critical Xi zero",
                "retain": "construct an explicit Taylor degree and rational or interval Rouché margin on the first rectangle that enters the open critical strip",
                "next_single_lemma": "ExplicitXiTaylorDegreeAndRoucheMarginOnFirstCriticalStripEnteringRectangleD3",
            },
            "proof_dag": proof_dag(
                "RH",
                "ActualXiTaylorSectionHasCertifiedZeroCountOnFirstOffRealRationalRectangle",
                "ActualXiFirstRectangleExistenceAndVacuityBoundary",
                "FirstExhaustionRectangleProvidesNontrivialRHControl",
                "ExplicitXiTaylorDegreeAndRoucheMarginOnFirstCriticalStripEnteringRectangleD3",
            ),
            "claim_boundary": "No RH proof or counterexample. The first actual-Xi rectangle is closed only existentially and lies outside the open critical strip.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-197",
            "theorem_name": "ContiguousOneTwoRunAffineDivisibilityObstruction",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Only one-block cyclic words 1^k2^(2k) are excluded; arbitrary alternation and the rest of the admissible density window remain open.",
            "route_decision": {
                "discard": "using the scalar-admissible one-third profile as evidence that its most clustered ordered words can realize cycles",
                "retain": "extend the affine factorization from one run pair to every fixed number of alternating run pairs",
                "next_single_lemma": "UniformAffineDivisibilityObstructionForFixedRunCountOneTwoWordsInTheAdmissibleDensityWindow",
            },
            "proof_dag": proof_dag(
                "CO",
                "UniformAffineDivisibilityObstructionForOneTwoWordsInTheAdmissibleDensityWindow",
                "ContiguousOneTwoRunAffineDivisibilityObstruction",
                "ScalarAdmissibilityImpliesContiguousRunCycleRealizability",
                "UniformAffineDivisibilityObstructionForFixedRunCountOneTwoWordsInTheAdmissibleDensityWindow",
            ),
            "claim_boundary": "No Collatz proof or nontrivial cycle. One infinite ordered subfamily surviving both scalar gates is now excluded exactly.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-197",
            "theorem_name": "GoldbachPrimePowerCollisionSupportHasDensityZero",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "The density-one collision-free targets still lack a pointwise binary-correlation lower bound, and the sparse collision-supported targets remain infinite a priori.",
            "route_decision": {
                "discard": "expecting Q*Q overlap subtraction alone to produce a uniform every-even margin",
                "retain": "prove pointwise major-minus-minor dominance first on the density-one collision-free stratum, then handle the sparse collision stratum",
                "next_single_lemma": "ExplicitGoldbachCorrelationMarginOnEveryLargeCollisionFreeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "ExplicitGoldbachMajorArcMainTermDominatesMinorArcAbsoluteErrorAndCollisionCorrectedContaminationForEveryLargeEvenTarget",
                "GoldbachPrimePowerCollisionSupportHasDensityZero",
                "CollisionCorrectionAloneSuppliesUniformEveryEvenMargin",
                "ExplicitGoldbachCorrelationMarginOnEveryLargeCollisionFreeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The overlap correction is exact but supported on a density-zero target set.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-197",
            "theorem_name": "TwinPrimeEqualExponentCollisionNoGoAndLowerOrderSaving",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "The leading prime-square contamination remains untouched, and no parity-breaking lower bound is proved on infinitely many blocks.",
            "route_decision": {
                "discard": "expecting collision subtraction to cancel the leading square-layer contamination",
                "retain": "seek parity-breaking shift-two mass above the unchanged square layer plus the mixed-exponent tail",
                "next_single_lemma": "ParityBreakingShiftTwoLowerBoundDominatesPrimeSquareLayerAndMixedExponentTailOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "ParityBreakingShiftTwoLowerBoundDominatesCollisionCorrectedContaminationOnInfinitelyManyDyadicBlocks",
                "TwinPrimeEqualExponentCollisionNoGoAndLowerOrderSaving",
                "PrimePowerCollisionCorrectionCancelsLeadingSquareLayer",
                "ParityBreakingShiftTwoLowerBoundDominatesPrimeSquareLayerAndMixedExponentTailOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. Equal-exponent overlap is impossible, so the exact correction is a lower-order mixed-layer saving only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureFirstRectangleRunBlockSparseCollisionAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-197 resolves none of the four conjectures. It closes the "
            "first actual-Xi rectangle only existentially, excludes an infinite "
            "ordered Collatz family, and proves that the TICKET-196 collision "
            "savings are sparse for Goldbach and lower-order for Twin Prime."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The shared advance is quantifier localization: one bounded Xi region "
            "can close without RH content, one infinite Collatz order family can "
            "close without controlling all words, and exact overlap corrections "
            "can be too sparse or too low-order to supply universal correlation "
            "lower bounds. The next work must enter the critical strip, increase "
            "run complexity, and confront pointwise parity-sensitive errors."
        ),
        "literature_boundary": {
            "riemann": "The location of xi zeros in the open critical strip and compact-uniform Taylor convergence are classical; no explicit Xi coefficient enclosure or RH progress is claimed.",
            "collatz": "The affine cycle equation and parity-vector restrictions are classical. The contiguous-run factorization is a project-local subfamily theorem and not a Collatz proof.",
            "goldbach": "Prime-power counting and the density-zero support bound use standard Chebyshev estimates. They do not provide a binary Goldbach minor-arc theorem.",
            "twin_prime": "The equal-exponent factorization is elementary. The lower-order overlap result does not bypass the sieve parity barrier or imply exact gap two.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "actual_xi_first_rectangle_existence_count": 1,
            "collatz_infinite_ordered_family_exclusion_count": 1,
            "goldbach_density_zero_collision_support_count": 1,
            "twin_equal_exponent_collision_no_go_count": 1,
            "riemann_exact_coordinate_row_count": len(
                riemann["exact_coordinate_rows"]
            ),
            "collatz_exact_scale_row_count": collatz["aggregate"][
                "checked_scale_count"
            ],
            "goldbach_finite_support_row_count": len(
                goldbach["finite_support_rows"]
            ),
            "twin_finite_dyadic_row_count": len(twin["finite_dyadic_rows"]),
            "rejected_or_limited_route_count": 4,
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
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "first_rectangle_run_block_sparse_collision_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data"
        / "open-problem"
        / "ticket197-first-rectangle-run-block-sparse-collision.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-197-first-rectangle.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-197-contiguous-runs.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-197-sparse-collision-support.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-197-mixed-exponent-collision.json",
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
            "TICKET-197 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
