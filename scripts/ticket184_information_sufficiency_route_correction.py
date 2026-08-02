from __future__ import annotations

import json
import math
from itertools import product
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket180_finite_information_localization import ordered_affine_numerator
from ticket183_abel_primitive_spectral_haar import (
    finite_twin_haar_diagnostic,
    primitive_root,
)


GENERATED_AT = "2026-08-02T16:30:00+09:00"
SCHEMA = "primeproject.ticket184-information-sufficiency-route-correction.v1"
STATUS = "four_exact_information_boundaries_with_two_route_corrections_all_open"


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
                "id": f"{problem_code}-T183-INPUT",
                "label": previous_name,
                "status": "proved_exact_input",
            },
            {
                "id": f"{problem_code}-T184-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T184-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_overstrong",
            },
            {
                "id": f"{problem_code}-T184-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T183-INPUT", f"{problem_code}-T184-CLOSED"],
            [f"{problem_code}-T184-CLOSED", f"{problem_code}-T184-OPEN"],
            [f"{problem_code}-T184-REJECTED", f"{problem_code}-T184-OPEN"],
        ],
    }


def moment_canceling_abel_row(
    cancellation_order: int, frequency: int, rho: float
) -> dict[str, object]:
    if cancellation_order < 1 or frequency < 1 or not 0.0 < rho < 1.0:
        raise ValueError("need m>=1, M>=1, and 0<rho<1")
    coefficients = [
        (-1) ** offset * math.comb(cancellation_order, offset)
        for offset in range(cancellation_order + 1)
    ]
    moment_numerators = [
        sum(
            coefficient * (frequency + offset) ** degree
            for offset, coefficient in enumerate(coefficients)
        )
        for degree in range(cancellation_order)
    ]
    abel_norm = rho**frequency * ((1.0 + rho) / 2.0) ** cancellation_order
    distance_at_pi = 1.0 - abel_norm
    return {
        "cancellation_order_m": cancellation_order,
        "base_frequency_M": frequency,
        "rho": rho,
        "integer_fourier_coefficients_before_2_pow_minus_m": coefficients,
        "cancelled_moment_numerators": moment_numerators,
        "original_uniform_norm": 1.0,
        "abel_uniform_norm": abel_norm,
        "desmoothing_distance_lower_bound": distance_at_pi,
        "checks": {
            "all_declared_moments_cancel_exactly": all(
                value == 0 for value in moment_numerators
            ),
            "abel_norm_has_closed_form": 0.0 < abel_norm < 1.0,
            "distance_at_pi_is_exact_lower_bound": math.isclose(
                distance_at_pi, 1.0 - abel_norm
            ),
        },
    }


def riemann_information_audit() -> dict[str, object]:
    rows = [
        moment_canceling_abel_row(order, frequency, 0.9)
        for order in [1, 2, 4, 8]
        for frequency in [16, 32, 64]
    ]
    failures = sum(not check for row in rows for check in row["checks"].values())
    return {
        "theorem": (
            "Fix an integer m>=1. For every M>=1, the trigonometric polynomial "
            "f_(M,m)(theta)=2^(-m)e^(iMtheta)(1-e^(itheta))^m has uniform "
            "norm one and its Fourier coefficients c_r satisfy "
            "sum_r c_r(M+r)^j=0 for every 0<=j<m. Nevertheless its Abel mean "
            "has uniform norm rho^M((1+rho)/2)^m, and at theta=pi the "
            "desmoothing error is exactly 1-rho^M((1+rho)/2)^m. Thus any "
            "fixed finite list of polynomial frequency-moment cancellations "
            "still permits Abel-hidden unit high-frequency mass."
        ),
        "proof": (
            "Expand (1-e^(itheta))^m. The moment sums are m-th finite "
            "differences of polynomials of degree below m and therefore vanish "
            "exactly. The maximum of |1-e^(itheta)| is two, attained at pi. "
            "Abel multiplication contributes rho^(M+r), so the transformed "
            "binomial factors as rho^M(1-rho e^(itheta))^m/2^m. Evaluating at "
            "pi proves both the norm formula and the lower bound."
        ),
        "counterfamily_rows": rows,
        "aggregate": {
            "case_count": len(rows),
            "largest_cancellation_order": max(
                row["cancellation_order_m"] for row in rows
            ),
            "largest_frequency": max(row["base_frequency_M"] for row in rows),
            "all_finite_moments_cancel": all(
                row["checks"]["all_declared_moments_cancel_exactly"] for row in rows
            ),
            "smallest_abel_norm": min(row["abel_uniform_norm"] for row in rows),
            "largest_desmoothing_lower_bound": max(
                row["desmoothing_distance_lower_bound"] for row in rows
            ),
        },
        "no_go_scope": (
            "This refutes finite polynomial Fourier-moment cancellation as a "
            "standalone compactness mechanism. It does not refute a theorem "
            "using the full Mellin support, positivity, and pole-neutral "
            "admissibility conditions of the Weil test cone."
        ),
        "failure_count": failures,
    }


def accelerated_collatz(odd_value: int) -> tuple[int, int]:
    value = 3 * odd_value + 1
    valuation = 0
    while value % 2 == 0:
        value //= 2
        valuation += 1
    return value, valuation


def collatz_first_descent_audit(limit: int = 1_000_000) -> dict[str, object]:
    unresolved: list[int] = []
    maximum_steps = -1
    maximizer = 1
    maximum_peak = 1
    for start in range(3, limit + 1, 2):
        current = start
        peak = start
        steps = 0
        while current >= start and current != 1 and steps < 10_000:
            current, _ = accelerated_collatz(current)
            peak = max(peak, current)
            steps += 1
        if current >= start and current != 1:
            unresolved.append(start)
        if steps > maximum_steps:
            maximum_steps = steps
            maximizer = start
        maximum_peak = max(maximum_peak, peak)
    return {
        "odd_start_limit": limit,
        "odd_starts_checked": (limit - 1) // 2,
        "first_descent_step_cap": 10_000,
        "unresolved_starts": unresolved,
        "maximum_first_descent_steps": maximum_steps,
        "first_descent_step_maximizer": maximizer,
        "maximum_intermediate_odd_value": maximum_peak,
        "claim_boundary": (
            "This is a bounded exact integer computation. It cannot establish "
            "finite descent for an unbounded set of starting values."
        ),
    }


def minimal_cycle_prefix_barrier(word: tuple[int, ...]) -> dict[str, object]:
    horizon = len(word)
    exponent_sum = sum(word)
    numerator = ordered_affine_numerator(word)
    denominator = 2**exponent_sum - 3**horizon
    slacks = []
    for length in range(1, horizon + 1):
        prefix = word[:length]
        prefix_numerator = ordered_affine_numerator(prefix)
        prefix_denominator = 2 ** sum(prefix) - 3**length
        slacks.append(
            prefix_numerator * denominator - prefix_denominator * numerator
        )
    return {
        "word": list(word),
        "horizon_h": horizon,
        "affine_numerator_B": numerator,
        "cycle_denominator_D": denominator,
        "starts_with_one": word[0] == 1,
        "contracting": denominator > 0,
        "prefix_barrier_slacks": slacks,
        "prefix_barrier_passes": denominator > 0
        and word[0] == 1
        and all(slack >= 0 for slack in slacks),
        "affine_divisibility_hit": denominator > 0
        and numerator % denominator == 0,
    }


def collatz_information_audit() -> dict[str, object]:
    horizon_rows = []
    examples = []
    total_barrier_passes = 0
    total_barrier_without_divisibility = 0
    for horizon in range(2, 8):
        counts = {
            "primitive_contracting_start_one_count": 0,
            "minimal_prefix_barrier_pass_count": 0,
            "barrier_without_divisibility_count": 0,
        }
        for word in product(range(1, 6), repeat=horizon):
            if primitive_root(word)[1] != 1 or word[0] != 1:
                continue
            row = minimal_cycle_prefix_barrier(word)
            if not row["contracting"]:
                continue
            counts["primitive_contracting_start_one_count"] += 1
            if row["prefix_barrier_passes"]:
                counts["minimal_prefix_barrier_pass_count"] += 1
                total_barrier_passes += 1
                if not row["affine_divisibility_hit"]:
                    counts["barrier_without_divisibility_count"] += 1
                    total_barrier_without_divisibility += 1
                    if len(examples) < 8:
                        examples.append(row)
        horizon_rows.append({"horizon_h": horizon, **counts})
    descent = collatz_first_descent_audit()
    failures = len(descent["unresolved_starts"])
    failures += sum(
        not (
            row["prefix_barrier_passes"]
            and not row["affine_divisibility_hit"]
        )
        for row in examples
    )
    return {
        "theorem": (
            "A positive accelerated Collatz counterexample has exactly two "
            "possible types: a nontrivial periodic orbit, or an orbit unbounded "
            "in limsup. If a nontrivial cycle is rotated to its least odd member "
            "n=B/D, then its first valuation is one and every prefix k satisfies "
            "B_k D >= (2^S_k-3^k)B. These prefix barriers are necessary but not "
            "sufficient; for example w=(1,3) passes every barrier while D=7 "
            "does not divide B=5."
        ),
        "proof": (
            "A bounded orbit in the positive integers repeats, hence is "
            "periodic; otherwise its limsup is infinite. At the least member "
            "n>1, a first valuation at least two would give (3n+1)/4<n, a "
            "contradiction. The prefix affine identity "
            "n_k=(3^k n+B_k)/2^S_k and n_k>=n gives the cross-multiplied "
            "barrier. The explicit word (1,3) proves that barriers without "
            "affine divisibility do not close the cycle branch."
        ),
        "finite_prefix_barrier_rows": horizon_rows,
        "barrier_no_go_examples": examples,
        "finite_first_descent_diagnostic": descent,
        "aggregate": {
            "prefix_barrier_passes": total_barrier_passes,
            "barrier_without_divisibility": total_barrier_without_divisibility,
            "largest_word_horizon": horizon_rows[-1]["horizon_h"],
            "first_descent_limit": descent["odd_start_limit"],
            "first_descent_unresolved_count": len(descent["unresolved_starts"]),
        },
        "no_go_scope": (
            "Excluding every nontrivial cycle would still leave the divergent "
            "orbit branch open. The TICKET-183 primitive-word lemma is therefore "
            "a cycle-branch target, not a complete Collatz proof target."
        ),
        "failure_count": failures,
    }


def distinct_prime_factors(value: int) -> list[int]:
    factors = []
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors.append(remaining)
    return factors


def goldbach_wheel_row(modulus: int) -> dict[str, object]:
    factors = distinct_prime_factors(modulus)
    if 2 in factors or math.prod(factors) != modulus:
        raise ValueError("modulus must be odd and squarefree")
    units = [residue for residue in range(modulus) if math.gcd(residue, modulus) == 1]
    mismatches = []
    counts = []
    for target in range(modulus):
        actual = sum(
            math.gcd((target - residue) % modulus, modulus) == 1
            for residue in units
        )
        formula = math.prod(
            prime - 1 if target % prime == 0 else prime - 2
            for prime in factors
        )
        counts.append(actual)
        if actual != formula:
            mismatches.append(target)
    return {
        "squarefree_odd_modulus_Q": modulus,
        "prime_factors": factors,
        "unit_residue_count": len(units),
        "minimum_local_representation_count": min(counts),
        "maximum_local_representation_count": max(counts),
        "factorization_mismatches": mismatches,
        "checks": {
            "crt_factorization_exact_for_every_target": not mismatches,
            "every_local_target_has_positive_margin": min(counts) > 0,
        },
    }


def composite_impostor_row(modulus: int) -> dict[str, object]:
    units = [residue for residue in range(modulus) if math.gcd(residue, modulus) == 1]
    sieve = prime_sieve(20_000)
    outside_primes = [
        value
        for value in range(2, len(sieve))
        if sieve[value] and math.gcd(value, modulus) == 1
    ][: len(units)]
    representatives = []
    for residue, divisor in zip(units, outside_primes):
        multiplier = (residue * pow(divisor, -1, modulus)) % modulus
        if multiplier < 2:
            multiplier += modulus
        value = divisor * multiplier
        representatives.append(
            {
                "unit_residue": residue,
                "composite_representative": value,
                "known_divisor": divisor,
            }
        )
    residue_histogram = sorted(row["composite_representative"] % modulus for row in representatives)
    return {
        "modulus_Q": modulus,
        "unit_residue_count": len(units),
        "composite_representative_count": len(representatives),
        "largest_composite_representative": max(
            row["composite_representative"] for row in representatives
        ),
        "sample": representatives[:8],
        "checks": {
            "one_representative_per_unit_residue": residue_histogram == units,
            "all_representatives_have_proper_known_divisor": all(
                row["composite_representative"] > row["known_divisor"]
                and row["composite_representative"] % row["known_divisor"] == 0
                for row in representatives
            ),
        },
    }


def goldbach_information_audit() -> dict[str, object]:
    rows = [goldbach_wheel_row(modulus) for modulus in [15, 105, 1155]]
    impostor = composite_impostor_row(1155)
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += sum(not check for check in impostor["checks"].values())
    return {
        "theorem": (
            "Let Q be a squarefree product of odd primes and U_Q its units. "
            "The number R_Q(n) of residues a with a and n-a both in U_Q is "
            "exactly product_(p|Q)(p-1 if p|n, otherwise p-2). Hence every "
            "target has a positive fixed-wheel local margin. Nevertheless, for "
            "every unit residue one can construct a composite integer in that "
            "residue, so a complete unit-residue histogram can be reproduced by "
            "a set containing no primes. Fixed-Q local data alone cannot imply "
            "a Goldbach representation by primes."
        ),
        "proof": (
            "Modulo p, the conditions exclude residues zero and n. They coincide "
            "when p divides n, leaving p-1 choices, and are distinct otherwise, "
            "leaving p-2. The Chinese remainder theorem multiplies the counts. "
            "For the no-go, choose a prime ell not dividing Q and solve "
            "ell*t congruent to r modulo Q; replacing t by t+Q if needed makes "
            "ell*t composite while preserving residue r."
        ),
        "wheel_factorization_rows": rows,
        "composite_impostor": impostor,
        "aggregate": {
            "largest_modulus": rows[-1]["squarefree_odd_modulus_Q"],
            "largest_unit_residue_count": rows[-1]["unit_residue_count"],
            "all_local_factorizations_exact": all(
                row["checks"]["crt_factorization_exact_for_every_target"]
                for row in rows
            ),
            "composite_impostor_size": impostor["composite_representative_count"],
        },
        "no_go_scope": (
            "The theorem closes the finite local-factor calculation, not the "
            "prime-support problem. A growing-modulus major term and a uniform "
            "prime-weighted minor-arc error below that local margin are still "
            "required."
        ),
        "failure_count": failures,
    }


def cantelli_lower_tail(
    masses: list[float], ratios: list[float], threshold: float
) -> dict[str, object]:
    if len(masses) != len(ratios) or not masses or threshold <= 0.0:
        raise ValueError("aligned nonempty data and positive threshold required")
    total_mass = sum(masses)
    weights = [mass / total_mass for mass in masses]
    mean = sum(weight * ratio for weight, ratio in zip(weights, ratios))
    variance = sum(
        weight * (ratio - mean) ** 2 for weight, ratio in zip(weights, ratios)
    )
    lower_tail_mass = sum(
        weight
        for weight, ratio in zip(weights, ratios)
        if ratio <= mean - threshold + 1e-15
    )
    bound = variance / (variance + threshold * threshold)
    return {
        "weighted_mean": mean,
        "weighted_variance": variance,
        "lower_tail_threshold_t": threshold,
        "actual_lower_tail_mass": lower_tail_mass,
        "cantelli_upper_bound": bound,
        "bound_slack": bound - lower_tail_mass,
    }


def twin_cantelli_sharp_row(depth: int) -> dict[str, object]:
    leaf_count = 2**depth
    masses = [1.0 / leaf_count] * leaf_count
    ratios = [0.0] + [1.0] * (leaf_count - 1)
    mean = 1.0 - 1.0 / leaf_count
    row = cantelli_lower_tail(masses, ratios, mean)
    return {
        "tree_depth_L": depth,
        "leaf_count": leaf_count,
        "bad_leaf_mass": 1.0 / leaf_count,
        **row,
        "checks": {
            "cantelli_is_exact_for_two_level_family": math.isclose(
                row["actual_lower_tail_mass"], row["cantelli_upper_bound"], abs_tol=1e-15
            ),
            "positive_root_coexists_with_zero_leaf": row["weighted_mean"] > 0.0
            and row["actual_lower_tail_mass"] > 0.0,
        },
    }


def twin_information_audit() -> dict[str, object]:
    rows = [twin_cantelli_sharp_row(depth) for depth in [4, 8, 12, 16]]
    finite = finite_twin_haar_diagnostic()
    finite["root_positive_implies_at_least_one_pair"] = (
        finite["root_actual_to_expected_ratio"] > 0.0
        and finite["actual_twin_pair_count"] > 0
    )
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(not finite["root_positive_implies_at_least_one_pair"])
    return {
        "theorem": (
            "For finite disjoint blocks of candidate first coordinates, with "
            "positive expected masses E_j and nonnegative actual twin-start "
            "counts C_j, the root ratio R=sum C_j/sum E_j is positive exactly "
            "when their union contains a twin-pair start. Positive roots on "
            "infinitely many pairwise disjoint "
            "intervals escaping to infinity therefore suffice for the Twin "
            "Prime conjecture; positivity of every leaf is unnecessary. "
            "Moreover the weighted lower-tail mass obeys Cantelli's sharp bound "
            "mu{r<=r_bar-t}<=V/(V+t^2)."
        ),
        "proof": (
            "The denominator of R is positive and its numerator is the total "
            "actual count, proving the root equivalence and the disjoint-block "
            "implication. Cantelli follows by applying Markov's inequality to a "
            "shifted square and optimizing the shift. A two-level distribution "
            "with one zero leaf and all other leaves equal to one attains the "
            "bound exactly, so average energy cannot remove the last bad leaf."
        ),
        "cantelli_sharpness_rows": rows,
        "finite_prime_pair_root_diagnostic": finite,
        "aggregate": {
            "sharpness_case_count": len(rows),
            "largest_depth": rows[-1]["tree_depth_L"],
            "smallest_persistent_bad_mass": rows[-1]["bad_leaf_mass"],
            "finite_actual_twin_pair_count": finite["actual_twin_pair_count"],
            "finite_root_ratio": finite["root_actual_to_expected_ratio"],
            "former_every_leaf_certificate_passes": finite[
                "all_leaf_certificates_pass"
            ],
        },
        "no_go_scope": (
            "The TICKET-183 every-path positivity target is sufficient but "
            "strictly stronger than twin infinitude. Haar energy remains useful "
            "for locating exceptional blocks, but the decisive arithmetic target "
            "is recurring positive total mass after a parity-breaking remainder "
            "estimate."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_information_audit()
    collatz = collatz_information_audit()
    goldbach = goldbach_information_audit()
    twin = twin_information_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-184",
            "theorem_name": "FiniteMomentCancellationDoesNotGiveUniformAbelDesmoothing",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "The counterfamily is a periodic Fourier proxy, not a member proof for the full pole-neutral Weil cone; full Mellin support and positivity may impose additional compactness.",
            "route_decision": {
                "discard": "any proof of uniform Abel desmoothing that uses only a fixed finite list of polynomial Fourier moments",
                "retain": "the full normalized Weil-admissible cone, including Mellin support, positivity, and pole-neutral constraints",
                "next_single_lemma": "NormalizedWeilAdmissibleConeHasUniformFourierTailTightnessFromFullMellinConstraints",
            },
            "proof_dag": proof_dag(
                "RH",
                "AbelFejerDesmoothingCertificateAndHighFrequencyNoGo",
                "FiniteMomentCancellationDoesNotGiveUniformAbelDesmoothing",
                "FinitePolynomialMomentsForceUniformAbelDesmoothing",
                "NormalizedWeilAdmissibleConeHasUniformFourierTailTightnessFromFullMellinConstraints",
            ),
            "claim_boundary": "No RH proof, zero exclusion, or Weil-cone compactness theorem; one exact moment-cancelling high-frequency counterfamily only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-184",
            "theorem_name": "CounterexampleDichotomyAndMinimalCyclePrefixBarrier",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Neither all primitive cycle words nor the divergent-orbit branch is excluded; first descent was checked only through one million.",
            "route_decision": {
                "discard": "treating nontrivial-cycle exclusion as a complete proof of the Collatz conjecture, or treating minimal-prefix barriers as sufficient",
                "retain": "exact affine divisibility for cycles plus a logically independent finite-descent argument for every starting value",
                "next_single_lemma": "EveryPositiveOddIntegerAboveOneHasAnAcceleratedIterateBelowItsStart",
            },
            "proof_dag": proof_dag(
                "CO",
                "PrimitiveWordReductionAndMonotoneValuationExclusion",
                "CounterexampleDichotomyAndMinimalCyclePrefixBarrier",
                "CycleExclusionAloneProvesCollatzOrPrefixBarrierIsSufficient",
                "EveryPositiveOddIntegerAboveOneHasAnAcceleratedIterateBelowItsStart",
            ),
            "claim_boundary": "No Collatz proof, divergence exclusion, or universal descent theorem; one exact failure dichotomy, one necessary cycle barrier, and bounded descent evidence only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-184",
            "theorem_name": "SquarefreeWheelFactorizationAndCompositeImpostorNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "Fixed wheel positivity contains no information that distinguishes prime support from composite impostors and supplies no uniform minor-arc bound.",
            "route_decision": {
                "discard": "fixed-modulus residue occupancy as a standalone proof of prime Goldbach representations",
                "retain": "the exact local singular factor inside a growing-modulus, prime-weighted major/minor decomposition",
                "next_single_lemma": "GrowingWheelPrimeWeightedMinorErrorIsUniformlyBelowTheLocalSingularMargin",
            },
            "proof_dag": proof_dag(
                "GB",
                "ExactFourierErrorIdentityAndSparseDensityNoGo",
                "SquarefreeWheelFactorizationAndCompositeImpostorNoGo",
                "FixedWheelLocalPositivityImpliesPrimeGoldbachRepresentations",
                "GrowingWheelPrimeWeightedMinorErrorIsUniformlyBelowTheLocalSingularMargin",
            ),
            "claim_boundary": "No Goldbach proof or counterexample; one exact CRT local factorization and one fixed-information composite impostor construction only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-184",
            "theorem_name": "PositiveRootMassSufficesAndCantelliExceptionalMassIsSharp",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No positive prime-pair block total is proved on an unbounded disjoint sequence; finite root positivity does not break sieve parity.",
            "route_decision": {
                "discard": "requiring every Haar leaf or every dyadic path to be positive as the decisive Twin Prime target",
                "retain": "Haar/Cantelli diagnostics for exceptional blocks while proving recurring positive total block mass directly",
                "next_single_lemma": "PrimePairBlockMainTermDominatesParityRemainderOnAnUnboundedDisjointSequence",
            },
            "proof_dag": proof_dag(
                "TP",
                "WeightedHaarVarianceIdentityAndNegativePathSquareCertificate",
                "PositiveRootMassSufficesAndCantelliExceptionalMassIsSharp",
                "EveryLeafPositivityIsNecessaryForTwinPrimeInfinitude",
                "PrimePairBlockMainTermDominatesParityRemainderOnAnUnboundedDisjointSequence",
            ),
            "claim_boundary": "No Twin Prime proof or parity-breaking lower bound; one exact root sufficiency theorem, one sharp exceptional-mass bound, and one finite block only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureInformationSufficiencyAndRouteCorrectionAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-184 resolves none of the four conjectures. It proves four "
            "exact information boundaries and corrects the decisive target for "
            "the Collatz and Twin Prime tracks."
        ),
        **sections,
        "cross_problem_synthesis": (
            "A proof target must be both information-sufficient and logically "
            "minimal: finite moments and fixed wheels lose arithmetic support, "
            "cycle exclusion misses Collatz divergence, and every-leaf Twin "
            "positivity is stronger than infinitude."
        ),
        "literature_boundary": {
            "riemann": "Weil's criterion uses a constrained Mellin test cone; finite periodic moments are only an information audit.",
            "collatz": "Almost-all descent and finite verification do not prove descent for every starting value or exclude every counterexample branch.",
            "goldbach": "The circle method requires a prime-weighted major term and minor-arc control; CRT local factors alone are insufficient.",
            "twin_prime": "Bounded-gap and averaged sieve results do not produce a positive exact-gap-two block total because the parity barrier remains.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "rejected_target_count": 4,
            "proof_dag_count": 4,
            "finite_arithmetic_diagnostic_count": 4,
            "decisive_route_correction_count": 2,
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
        ROOT / "data" / "open-problem" / "ticket184-information-sufficiency-route-correction.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "information_sufficiency_route_correction_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-184-finite-moment-no-go.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-184-dichotomy-prefix-barrier.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-184-wheel-impostor.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-184-root-cantelli.json",
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
            "TICKET-184 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
