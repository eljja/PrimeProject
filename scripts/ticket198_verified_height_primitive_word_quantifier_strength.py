from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json


GENERATED_AT = "2026-08-09T00:30:00+09:00"
SCHEMA = "primeproject.ticket198-verified-height-primitive-word-quantifier-strength.v1"
STATUS = (
    "verified_height_transferred_to_rouche_prefix_collatz_fixed_run_families_"
    "goldbach_stratum_gap_exposed_twin_mass_target_strengthened_all_open"
)
VERIFIED_RH_HEIGHT = 3_000_000_000_000


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
                "id": f"{problem_code}-T197-INPUT",
                "label": previous_name,
                "status": "open_input_from_ticket197",
            },
            {
                "id": f"{problem_code}-T198-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T198-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_route_limited",
            },
            {
                "id": f"{problem_code}-T198-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T197-INPUT", f"{problem_code}-T198-CLOSED"],
            [f"{problem_code}-T198-CLOSED", f"{problem_code}-T198-OPEN"],
            [f"{problem_code}-T198-REJECTED", f"{problem_code}-T198-OPEN"],
        ],
    }


def rh_rectangle_row(m: int) -> dict[str, object]:
    if m < 2:
        raise ValueError("m must be at least two")
    reciprocal = Fraction(1, m)
    half = Fraction(1, 2)
    return {
        "m": m,
        "upper_s_real_interval": [str(half - m), str(half - reciprocal)],
        "lower_s_real_interval": [str(half + reciprocal), str(half + m)],
        "s_imaginary_interval": [-m, m],
        "minimum_distance_from_critical_line": str(reciprocal),
        "enters_open_critical_strip": m >= 3,
        "covered_by_imported_verified_height": m <= VERIFIED_RH_HEIGHT,
        "zero_free_off_critical_line_from_imported_theorem": (
            m <= VERIFIED_RH_HEIGHT
        ),
    }


def riemann_verified_height_transfer_audit() -> dict[str, object]:
    sample_m = [2, 3, 10, 1_000, 1_000_000, VERIFIED_RH_HEIGHT]
    rows = [rh_rectangle_row(m) for m in sample_m]
    failures = sum(
        int(not row["covered_by_imported_verified_height"])
        + int(not row["zero_free_off_critical_line_from_imported_theorem"])
        for row in rows
    )
    failures += int(rows[0]["enters_open_critical_strip"])
    failures += int(not rows[1]["enters_open_critical_strip"])
    return {
        "theorem": (
            "Let Xi(z)=xi(1/2+i z), let D_m^+={|Re z|<=m, 1/m<=Im z<=m}, "
            "and let D_m^- be its conjugate. Assume the rigorous finite-height "
            "theorem that every nontrivial zeta zero beta+i gamma with "
            "0<|gamma|<=H lies on beta=1/2. Then, for every integer "
            "2<=m<=H, Xi is zero-free on both closed D_m rectangles. Hence, "
            "for each such rectangle, some Taylor section of Xi at zero "
            "satisfies the strict Rouche inequality and has zero count zero. "
            "With the Platt-Trudgian value H=3*10^12, this transfers a finite "
            "prefix of 2,999,999,999,999 rectangle levels, but supplies no "
            "effective Taylor degree or margin."
        ),
        "proof": (
            "Writing z=x+i y gives s=1/2-y+i x. A zero in either D_m would "
            "have |Im s|=|x|<=m<=H and Re(s) different from 1/2 by at least "
            "1/m. The imported finite-height theorem excludes every such "
            "nonreal-ordinate zero; the real interval 0<Re(s)<1 is zero-free "
            "because eta(s)>0 there and zeta(s)=eta(s)/(1-2^(1-s)) is nonzero. "
            "All xi zeros are nontrivial zeta zeros, so the compact rectangles "
            "are zero-free. Their positive minimum modulus and compact-uniform "
            "Taylor convergence give the existential Rouche sections exactly "
            "as in TICKET-197."
        ),
        "imported_theorem": {
            "authors": ["Dave Platt", "Tim Trudgian"],
            "title": "The Riemann hypothesis is true up to 3*10^12",
            "verified_height_H": VERIFIED_RH_HEIGHT,
            "method": "rigorous interval arithmetic",
            "doi": "10.1112/blms.12460",
            "url": "https://arxiv.org/abs/2004.09765",
            "project_claim": "imported_peer_reviewed_computer_assisted_theorem",
        },
        "sample_rectangle_rows": rows,
        "contract": {
            "integer_rectangle_levels_transferred": VERIFIED_RH_HEIGHT - 1,
            "D3_enters_open_critical_strip": True,
            "all_integer_m_through_verified_height_zero_free": True,
            "existential_taylor_rouche_sections_through_height": True,
            "explicit_taylor_degree_exhibited": False,
            "explicit_interval_margin_exhibited": False,
            "any_rectangle_above_verified_height_closed": False,
            "full_rh_resolved": False,
        },
        "no_go_scope": (
            "This is a transfer of an existing rigorous finite-height theorem, "
            "not a new verification of zeta zeros. A finite prefix, however "
            "large, leaves every ordinate above H uncontrolled. Compactness "
            "proves existence of Taylor degrees but gives no machine-checkable "
            "degree or numerical margin."
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


def repeat_word(word: tuple[int, ...], repetition: int) -> tuple[int, ...]:
    if not word or repetition < 1:
        raise ValueError("word must be nonempty and repetition positive")
    return word * repetition


def affine_denominator(word: tuple[int, ...]) -> int:
    return 2 ** sum(word) - 3 ** len(word)


def repetition_factor(word: tuple[int, ...], repetition: int) -> int:
    power_two = 2 ** sum(word)
    power_three = 3 ** len(word)
    return sum(
        power_two ** (repetition - 1 - index) * power_three**index
        for index in range(repetition)
    )


def collatz_repetition_row(
    word: tuple[int, ...], repetition: int
) -> dict[str, object]:
    repeated = repeat_word(word, repetition)
    base_numerator = ordered_affine_numerator(word)
    base_denominator = affine_denominator(word)
    factor = repetition_factor(word, repetition)
    repeated_numerator = ordered_affine_numerator(repeated)
    repeated_denominator = affine_denominator(repeated)
    base_integral = base_numerator % abs(base_denominator) == 0
    repeated_integral = repeated_numerator % abs(repeated_denominator) == 0
    return {
        "word": list(word),
        "repetition": repetition,
        "base_horizon": len(word),
        "base_valuation_sum": sum(word),
        "base_numerator": str(base_numerator),
        "base_denominator": str(base_denominator),
        "geometric_factor": str(factor),
        "repeated_numerator": str(repeated_numerator),
        "repeated_denominator": str(repeated_denominator),
        "numerator_factorization_holds": repeated_numerator == base_numerator * factor,
        "denominator_factorization_holds": repeated_denominator == base_denominator * factor,
        "fixed_point_fraction_preserved": (
            Fraction(repeated_numerator, repeated_denominator)
            == Fraction(base_numerator, base_denominator)
        ),
        "affine_integrality_preserved": base_integral == repeated_integral,
        "base_integral": base_integral,
        "repeated_integral": repeated_integral,
    }


def words_of_length(length: int, alphabet: tuple[int, ...]) -> list[tuple[int, ...]]:
    words = [()]
    for _ in range(length):
        words = [prefix + (value,) for prefix in words for value in alphabet]
    return words


def cyclic_run_count(word: tuple[int, ...]) -> int:
    if not word:
        return 0
    return sum(word[index] != word[(index + 1) % len(word)] for index in range(len(word)))


def is_primitive_word(word: tuple[int, ...]) -> bool:
    if not word:
        return False
    for period in range(1, len(word)):
        if len(word) % period == 0 and word == word[:period] * (len(word) // period):
            return False
    return True


def fixed_run_primitive_word(one_run_count: int, scale: int) -> tuple[int, ...]:
    if one_run_count < 2 or scale < 2:
        raise ValueError("one_run_count and scale must both be at least two")
    return (
        (1,) * scale
        + (2,) * (2 * scale)
        + ((1,) + (2, 2)) * (one_run_count - 1)
    )


def collatz_fixed_run_row(one_run_count: int, scale: int) -> dict[str, object]:
    word = fixed_run_primitive_word(one_run_count, scale)
    one_count = sum(value == 1 for value in word)
    two_count = len(word) - one_count
    valuation_sum = sum(word)
    denominator = affine_denominator(word)
    numerator = ordered_affine_numerator(word)
    return {
        "one_run_count": one_run_count,
        "cyclic_run_count": cyclic_run_count(word),
        "scale_k": scale,
        "run_lengths": [scale, 2 * scale] + [1, 2] * (one_run_count - 1),
        "horizon_h": len(word),
        "one_count": one_count,
        "two_count": two_count,
        "one_density": "1/3",
        "valuation_sum": valuation_sum,
        "primitive": is_primitive_word(word),
        "contraction_gate_passes": 2**valuation_sum > 3 ** len(word),
        "product_gate_passes": 125**one_count > 108**one_count,
        "affine_divisibility_hit": denominator > 0 and numerator % denominator == 0,
    }


def collatz_fixed_run_primitive_family_audit() -> dict[str, object]:
    transcript = hashlib.sha256()
    summaries = []
    representatives = []
    failure_count = 0
    checked_words = 0
    total_divisibility_hits = 0
    for one_run_count in range(2, 9):
        family_rows = []
        for scale in range(2, 65):
            row = collatz_fixed_run_row(one_run_count, scale)
            family_rows.append(row)
            checked_words += 1
            total_divisibility_hits += int(row["affine_divisibility_hit"])
            failure_count += int(not row["primitive"])
            failure_count += int(row["cyclic_run_count"] != 2 * one_run_count)
            failure_count += int(not row["contraction_gate_passes"])
            failure_count += int(not row["product_gate_passes"])
            transcript.update(
                (
                    f"{one_run_count}:{scale}:{row['horizon_h']}:"
                    f"{row['cyclic_run_count']}:{int(row['affine_divisibility_hit'])}\n"
                ).encode("ascii")
            )
            if scale in {2, 3, 8, 64}:
                representatives.append(row)
        summaries.append(
            {
                "one_run_count": one_run_count,
                "cyclic_run_count": 2 * one_run_count,
                "checked_scale_range": [2, 64],
                "checked_word_count": len(family_rows),
                "all_checked_words_primitive": all(row["primitive"] for row in family_rows),
                "all_checked_words_pass_both_scalar_gates": all(
                    row["contraction_gate_passes"] and row["product_gate_passes"]
                    for row in family_rows
                ),
                "finite_affine_divisibility_hit_count": sum(
                    int(row["affine_divisibility_hit"]) for row in family_rows
                ),
            }
        )
    return {
        "theorem": (
            "For every fixed one-run count r>=2 and every k>=2, the binary "
            "valuation word w_(r,k)=1^k 2^(2k) (1 2^2)^(r-1) is primitive, "
            "has exactly r cyclic one-runs and r cyclic two-runs, has one-density "
            "1/3, and passes both exact scalar cycle gates. Thus primitive-root "
            "normalization plus any fixed run count still leaves an infinite "
            "family of scalar-admissible Collatz cycle candidates."
        ),
        "proof": (
            "Put q=k+r-1. The word has q ones, 2q twos, horizon 3q, and "
            "valuation sum 5q. Hence 2^(5q)=32^q>27^q=3^(3q), while "
            "2^q(5/6)^(3q)=(125/108)^q>1. Its cyclic run lengths are "
            "(k,2k,1,2,...,1,2), so there are exactly 2r runs. For k>=2 "
            "the unique one-run of length k and unique two-run of length 2k "
            "would have to repeat in any nontrivial word power; therefore the "
            "word is primitive. Letting k grow proves infinitude for each fixed r."
        ),
        "prior_exact_input": {
            "ticket": "TICKET-183",
            "theorem": "PrimitiveWordReductionAndMonotoneValuationExclusion",
            "role": "reused_input_not_new_ticket198_result",
        },
        "family_definition": "w_(r,k)=1^k 2^(2k) (1 2^2)^(r-1), r>=2, k>=2",
        "finite_run_count_summaries": summaries,
        "representative_rows": representatives,
        "aggregate": {
            "checked_fixed_run_word_count": checked_words,
            "checked_one_run_count_range": [2, 8],
            "checked_scale_range": [2, 64],
            "infinite_primitive_family_for_every_fixed_run_count_r_ge_2": True,
            "fixed_run_count_plus_scalar_gates_is_finite_search": False,
            "finite_affine_divisibility_hit_count": total_divisibility_hits,
            "nontrivial_collatz_cycle_found": False,
            "transcript_sha256": transcript.hexdigest(),
        },
        "no_go_scope": (
            "The theorem proves that a fixed run count does not make the "
            "primitive scalar-admissible search finite. It neither proves nor "
            "refutes affine divisibility for the infinite families, and it does "
            "not control valuations above two or divergent aperiodic trajectories."
        ),
        "failure_count": failure_count,
    }


def prime_sieve(limit: int) -> tuple[list[int], bytearray]:
    flags = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        flags[0] = 0
    if limit >= 1:
        flags[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            start = prime * prime
            flags[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [value for value, flag in enumerate(flags) if flag], flags


def odd_proper_prime_powers(limit: int, primes: list[int]) -> list[int]:
    values = set()
    for prime in primes:
        if prime == 2 or prime * prime > limit:
            continue
        value = prime * prime
        while value <= limit:
            values.add(value)
            value *= prime
    return sorted(values)


def goldbach_collision_set(limit: int, powers: list[int]) -> set[int]:
    targets: set[int] = set()
    for left_index, left in enumerate(powers):
        for right in powers[left_index:]:
            target = left + right
            if target > limit:
                break
            targets.add(target)
    return targets


def goldbach_represented(even: int, primes: list[int], flags: bytearray) -> bool:
    for prime in primes:
        if prime > even // 2:
            return False
        if flags[even - prime]:
            return True
    return False


def goldbach_collision_stratum_audit() -> dict[str, object]:
    limit = 2**20
    primes, flags = prime_sieve(limit)
    powers = odd_proper_prime_powers(limit, primes)
    collision_targets = goldbach_collision_set(limit, powers)
    represented = bytearray(limit + 1)
    for even in range(4, limit + 1, 2):
        represented[even] = int(goldbach_represented(even, primes, flags))
    rows = []
    failures = 0
    for exponent in range(8, 21):
        cutoff = 2**exponent
        collision = [value for value in collision_targets if value <= cutoff]
        collision_free_failures = sum(
            int(not represented[even])
            for even in range(4, cutoff + 1, 2)
            if even not in collision_targets
        )
        collision_failures = sum(
            int(not represented[even]) for even in collision
        )
        diagonal = [
            2 * prime * prime
            for prime in primes
            if prime > 2 and 2 * prime * prime <= cutoff
        ]
        diagonal_missing_from_collision = sum(
            int(value not in collision_targets) for value in diagonal
        )
        failures += diagonal_missing_from_collision
        rows.append(
            {
                "cutoff_X": cutoff,
                "collision_supported_target_count": len(collision),
                "collision_free_target_count": cutoff // 2 - 1 - len(collision),
                "actual_goldbach_failure_count": collision_free_failures
                + collision_failures,
                "actual_collision_free_failure_count": collision_free_failures,
                "actual_collision_supported_failure_count": collision_failures,
                "diagonal_2p2_target_count": len(diagonal),
                "diagonal_missing_from_collision_count": diagonal_missing_from_collision,
            }
        )
    return {
        "theorem": (
            "Let C be the even targets supported by Q*Q and let E be the "
            "strong-Goldbach exceptional set. If every sufficiently large "
            "even N outside C has a prime-prime representation, then E is "
            "eventually contained in C. TICKET-197 therefore yields only "
            "|E intersect [1,X]|=O(X/log(X)^2), not E=empty. This inference "
            "cannot be strengthened from those premises alone: C contains the "
            "infinite diagonal S={2p^2:p odd prime}, and the abstract indicator "
            "that vanishes exactly on S while being positive off C satisfies "
            "the collision-free premise but has infinitely many failures."
        ),
        "proof": (
            "The assumed margin gives E\\C finite, hence E is contained in C "
            "up to finitely many targets. Apply the TICKET-197 bound for C. "
            "For every odd prime p, 2p^2=p^2+p^2 is in the Q*Q support, so S "
            "is an explicit infinite subset of C. Defining a surrogate "
            "nonnegative representation indicator to be zero on S and one "
            "elsewhere supplies a countermodel to the set-theoretic inference. "
            "It is not a counterexample to Goldbach and makes no assertion "
            "about the actual representation count on S."
        ),
        "finite_limit": limit,
        "finite_stratum_rows": rows,
        "surrogate_countermodel": {
            "failure_set": "S={2p^2:p odd prime}",
            "failure_set_is_infinite": True,
            "failure_set_subset_of_collision_support": True,
            "positive_on_every_collision_free_target": True,
            "is_actual_goldbach_representation_function": False,
        },
        "aggregate": {
            "finite_row_count": len(rows),
            "largest_cutoff": limit,
            "finite_actual_goldbach_failure_count": rows[-1][
                "actual_goldbach_failure_count"
            ],
            "collision_free_margin_sufficient_for_full_goldbach": False,
            "collision_free_margin_implies_log_squared_exception_bound": True,
            "infinite_collision_diagonal_exhibited": True,
        },
        "no_go_scope": (
            "The countermodel refutes only an inference from collision-free "
            "control to all-even control. It does not exhibit an actual "
            "Goldbach exception. The finite scan through 2^20 is regression "
            "evidence and cannot close the infinite collision-supported stratum."
        ),
        "failure_count": failures,
    }


def twin_block_row(
    lower: int, primes: list[int], flags: bytearray
) -> dict[str, object]:
    upper = 2 * lower
    count = 0
    weighted_mass = 0.0
    for prime in primes:
        if prime < lower:
            continue
        if prime >= upper:
            break
        if prime + 2 < len(flags) and flags[prime + 2]:
            count += 1
            weighted_mass += math.log(prime) * math.log(prime + 2)
    weight_cap = math.log(upper + 2) ** 2
    unit_contamination_scale = math.sqrt(lower) * math.log(lower)
    forced_count = math.ceil(unit_contamination_scale / weight_cap)
    return {
        "block": [lower, upper],
        "actual_twin_pair_count": count,
        "actual_weighted_twin_mass": weighted_mass,
        "per_pair_weight_cap": weight_cap,
        "unit_contamination_scale_sqrtXlogX": unit_contamination_scale,
        "count_forced_by_unit_mass_dominance": forced_count,
        "actual_count_over_forced_count": count / forced_count,
        "weighted_mass_below_count_times_cap": weighted_mass <= count * weight_cap,
    }


def twin_mass_strength_audit() -> dict[str, object]:
    largest_lower = 2**22
    primes, flags = prime_sieve(2 * largest_lower + 2)
    rows = [twin_block_row(2**exponent, primes, flags) for exponent in range(10, 23)]
    sparse_rows = []
    for index in range(3, 9):
        log_x = (2**index) * math.log(2)
        log_upper_weight = 2 * math.log(log_x + 2 * math.log(2))
        log_scale = 0.5 * log_x + math.log(log_x)
        sparse_rows.append(
            {
                "index_j": index,
                "synthetic_block": f"X_j=2^(2^{index})",
                "pair_count": 1,
                "log_upper_bound_ratio_to_sqrtXlogX": log_upper_weight - log_scale,
                "upper_bound_ratio_to_sqrtXlogX": math.exp(
                    log_upper_weight - log_scale
                ),
            }
        )
    failures = sum(
        int(not row["weighted_mass_below_count_times_cap"]) for row in rows
    )
    failures += int(
        any(
            left["upper_bound_ratio_to_sqrtXlogX"]
            <= right["upper_bound_ratio_to_sqrtXlogX"]
            for left, right in zip(sparse_rows, sparse_rows[1:])
        )
    )
    return {
        "theorem": (
            "For X>=2, let T(X) count twin-prime starts p in [X,2X) and "
            "M(X)=sum log(p)log(p+2) over those pairs. Then "
            "M(X)<=T(X)log(2X+2)^2. Consequently any lower bound "
            "M(X)>=K sqrt(X)log(X) forces "
            "T(X)>=K sqrt(X)log(X)/log(2X+2)^2, a quantity tending to "
            "infinity. The TICKET-197 contamination-dominance target is thus "
            "a square-root-scale quantitative twin-count target, not merely a "
            "positivity or infinitude target. Infinitude alone supplies no such "
            "block-mass estimate."
        ),
        "proof": (
            "Every pair in [X,2X) has log(p)log(p+2)<=log(2X+2)^2; summing "
            "gives the upper bound and rearrangement gives the forced count. "
            "To audit the inference from bare infinitude, place one abstract "
            "positive atom in each block X_j=2^(2^j). Its possible logarithmic "
            "weight divided by sqrt(X_j)log(X_j) tends to zero. This synthetic "
            "counting model is not a model of the primes; it proves only that "
            "cardinality infinitude by itself does not contain the required "
            "quantitative block estimate."
        ),
        "finite_dyadic_rows": rows,
        "sparse_inference_countermodel_rows": sparse_rows,
        "aggregate": {
            "finite_block_count": len(rows),
            "largest_block_upper": 2 * largest_lower,
            "mass_dominance_forces_unbounded_pair_count": True,
            "bare_positivity_forces_only_one_pair": True,
            "synthetic_sparse_ratio_tends_to_zero": True,
            "parity_breaking_lower_bound_proved": False,
        },
        "no_go_scope": (
            "The inequality does not prove that actual twin primes are sparse "
            "and is not a formal independence theorem. It proves that the "
            "current global mass route demands far more quantitative output "
            "than the one-positive-atom conclusion needed for infinitude."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_verified_height_transfer_audit()
    collatz = collatz_fixed_run_primitive_family_audit()
    goldbach = goldbach_collision_stratum_audit()
    twin = twin_mass_strength_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-198",
            "theorem_name": "FiniteHeightRHTransfersToFiniteXiRouchePrefix",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "The result imports a finite-height verification, provides no explicit Taylor degree or margin, and controls no ordinate above 3*10^12.",
            "route_decision": {
                "discard": "treating a standalone D3 existence certificate as the decisive RH bridge when a vastly larger finite-height prefix is already rigorously known",
                "retain": "turn the imported zero-free fact into a standalone interval-checkable Taylor degree and Rouche margin rather than another existential compactness statement",
                "next_single_lemma": "StandaloneIntervalXiTaylorDegreeAndRoucheMarginOnD3WithoutImportingFiniteHeightRH",
            },
            "proof_dag": proof_dag(
                "RH",
                "ExplicitXiTaylorDegreeAndRoucheMarginOnFirstCriticalStripEnteringRectangleD3",
                "FiniteHeightRHTransfersToFiniteXiRouchePrefix",
                "SingleD3ExistenceCertificateIsTheDecisiveRHBridge",
                "StandaloneIntervalXiTaylorDegreeAndRoucheMarginOnD3WithoutImportingFiniteHeightRH",
            ),
            "claim_boundary": "No RH proof or counterexample. A peer-reviewed finite-height theorem is transferred to the project Rouche language; the infinite tail remains open.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-198",
            "theorem_name": "FixedRunCountLeavesInfinitePrimitiveAdmissibleFamilies",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Fixed run count and primitive normalization still leave infinite scalar-admissible families; their affine divisibility and aperiodic trajectories remain open.",
            "route_decision": {
                "discard": "treating primitive normalization plus a fixed run count as a finite Collatz search space",
                "retain": "derive an all-length affine divisibility obstruction separately for each fixed run count inside the admissible density window",
                "next_single_lemma": "UniformAffineDivisibilityObstructionForPrimitiveFixedRunCountOneTwoWordsInTheAdmissibleDensityWindow",
            },
            "proof_dag": proof_dag(
                "CO",
                "UniformAffineDivisibilityObstructionForFixedRunCountOneTwoWordsInTheAdmissibleDensityWindow",
                "FixedRunCountLeavesInfinitePrimitiveAdmissibleFamilies",
                "PrimitiveFixedRunCountMakesTheScalarAdmissibleSearchFinite",
                "UniformAffineDivisibilityObstructionForPrimitiveFixedRunCountOneTwoWordsInTheAdmissibleDensityWindow",
            ),
            "claim_boundary": "No Collatz proof or nontrivial cycle. TICKET-183 primitive reduction is reused as an input; the new result proves that every fixed run count still contains an infinite primitive scalar-admissible family.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-198",
            "theorem_name": "CollisionFreeGoldbachMarginLeavesLogSquaredExceptionalSet",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "The actual collision-supported stratum, including the infinite diagonal 2p^2, still lacks a pointwise representation theorem.",
            "route_decision": {
                "discard": "treating a density-one collision-free correlation margin as sufficient for strong Goldbach",
                "retain": "use the collision-free result only as one side of an exact two-stratum proof and attack the sparse collision support separately",
                "next_single_lemma": "ExplicitGoldbachCorrelationMarginOnEveryLargeCollisionSupportedEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "ExplicitGoldbachCorrelationMarginOnEveryLargeCollisionFreeEvenTarget",
                "CollisionFreeGoldbachMarginLeavesLogSquaredExceptionalSet",
                "CollisionFreeMarginAloneProvesStrongGoldbach",
                "ExplicitGoldbachCorrelationMarginOnEveryLargeCollisionSupportedEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The previous next lemma is proved logically insufficient by itself and now forms only half of a two-stratum target.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-198",
            "theorem_name": "TwinBlockMassDominanceForcesSquareRootScalePairCount",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No lower bound for the actual prime-supported shift-two correlation is proved on an unbounded block sequence.",
            "route_decision": {
                "discard": "using global domination of the full prime-power contamination budget as the minimal formulation of twin-prime infinitude",
                "retain": "build a localized nonnegative detector whose positivity witnesses at least one genuine gap-two prime pair without requiring square-root-scale block mass",
                "next_single_lemma": "PrimePowerFreeLocalizedTwinDetectorHasPositiveMassOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "ParityBreakingShiftTwoLowerBoundDominatesPrimeSquareLayerAndMixedExponentTailOnInfinitelyManyDyadicBlocks",
                "TwinBlockMassDominanceForcesSquareRootScalePairCount",
                "GlobalContaminationDominanceIsAMinimalTwinInfinitudeTarget",
                "PrimePowerFreeLocalizedTwinDetectorHasPositiveMassOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. The previous global mass target is certified as quantitatively overstrong relative to mere positivity.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureVerifiedHeightPrimitiveWordQuantifierStrengthAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-198 resolves none of the four conjectures. It transfers an "
            "existing rigorous finite-height RH theorem into the Rouche DAG, "
            "proves fixed-run primitive Collatz search remains infinite, proves the "
            "collision-free Goldbach target insufficient by itself, and shows "
            "that Twin global mass domination demands square-root-scale counts."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The shared result is a quantifier-strength correction. Huge finite "
            "height is still finite, fixed-run primitive normalization still "
            "leaves infinite scalar-admissible words, density-one control leaves an infinite "
            "sparse stratum, and global weighted domination asks for much more "
            "than one positive atom. The next ticket should produce effective "
            "local certificates on the exact remaining strata."
        ),
        "literature_boundary": {
            "riemann": "The finite-height input is explicitly attributed to Platt and Trudgian; PrimeProject proves only the transfer to its Rouche rectangles.",
            "collatz": "TICKET-183's primitive-root theorem is cited as an input, not re-claimed. TICKET-198 adds an all-r fixed-run infinite-family no-go and does not settle affine divisibility or divergent orbits.",
            "goldbach": "The theorem is a set-theoretic inference audit using the TICKET-197 support bound, not a new exceptional-set estimate for actual primes.",
            "twin_prime": "The mass-count inequality is elementary and exposes target strength; it does not improve known sieve lower bounds or bypass parity.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "riemann_verified_height_transfer_count": 1,
            "collatz_fixed_run_infinite_family_count": 1,
            "goldbach_inference_no_go_count": 1,
            "twin_quantitative_strength_no_go_count": 1,
            "riemann_sample_rectangle_row_count": len(
                riemann["sample_rectangle_rows"]
            ),
            "collatz_checked_fixed_run_word_count": collatz["aggregate"][
                "checked_fixed_run_word_count"
            ],
            "goldbach_finite_stratum_row_count": len(
                goldbach["finite_stratum_rows"]
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
        "verified_height_primitive_word_quantifier_strength_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data"
        / "open-problem"
        / "ticket198-verified-height-primitive-word-quantifier-strength.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-198-verified-height-rouche-prefix.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-198-fixed-run-primitive-family.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-198-collision-stratum-gap.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-198-block-mass-strength.json",
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
            "TICKET-198 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
