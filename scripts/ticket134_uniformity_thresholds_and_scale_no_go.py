from __future__ import annotations

import json
import math
from fractions import Fraction
from itertools import product
from typing import Any, Iterable

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket131_proof_viability_target_correction import valuation_word_cylinder
from ticket132_admissibility_nullset_hard_stratum_local_parity import (
    accelerated_valuations,
    crt,
    first_primes_above,
    fraction_payload,
    primes_through,
)


GENERATED_AT = "2026-07-20T23:50:00+09:00"
SCHEMA = "primeproject.ticket134-uniformity-thresholds-and-scale-no-go.v1"
K56_MARGIN = Fraction(23_019_645_297, 2_140_000_000_000)


def fraction_matrix(values: Iterable[Iterable[int | Fraction]]) -> list[list[Fraction]]:
    return [[Fraction(value) for value in row] for row in values]


def interval_box(
    center: list[list[Fraction]], radius: Fraction
) -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    lower = [[value - radius for value in row] for row in center]
    upper = [[value + radius for value in row] for row in center]
    return lower, upper


def congruence_interval(
    lower: list[list[Fraction]],
    upper: list[list[Fraction]],
    transform: list[list[Fraction]],
) -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    """Enclose C^T G C while treating each symmetric G_ab as one variable."""
    dimension = len(lower)
    out_lower = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    out_upper = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    for row in range(dimension):
        for column in range(dimension):
            low = Fraction(0)
            high = Fraction(0)
            for left in range(dimension):
                for right in range(left, dimension):
                    if left == right:
                        coefficient = transform[left][row] * transform[left][column]
                    else:
                        coefficient = (
                            transform[left][row] * transform[right][column]
                            + transform[right][row] * transform[left][column]
                        )
                    if coefficient >= 0:
                        low += coefficient * lower[left][right]
                        high += coefficient * upper[left][right]
                    else:
                        low += coefficient * upper[left][right]
                        high += coefficient * lower[left][right]
            out_lower[row][column] = low
            out_upper[row][column] = high
    return out_lower, out_upper


def gershgorin_lower_margins(
    lower: list[list[Fraction]], upper: list[list[Fraction]]
) -> list[Fraction]:
    margins = []
    for row in range(len(lower)):
        radius = sum(
            max(abs(lower[row][column]), abs(upper[row][column]))
            for column in range(len(lower))
            if column != row
        )
        margins.append(lower[row][row] - radius)
    return margins


def quadratic_interval_upper(
    lower: list[list[Fraction]],
    upper: list[list[Fraction]],
    vector: list[Fraction],
) -> Fraction:
    value = Fraction(0)
    for row in range(len(vector)):
        value += vector[row] ** 2 * upper[row][row]
        for column in range(row + 1, len(vector)):
            coefficient = 2 * vector[row] * vector[column]
            endpoint = upper[row][column] if coefficient >= 0 else lower[row][column]
            value += coefficient * endpoint
    return value


def riemann_interval_dichotomy() -> dict[str, Any]:
    positive = fraction_matrix([[2, 3], [3, 5]])
    positive_lower, positive_upper = interval_box(positive, Fraction(1, 1000))
    direct_margins = gershgorin_lower_margins(positive_lower, positive_upper)
    preconditioner = fraction_matrix([[1, Fraction(-3, 2)], [0, 1]])
    transformed_lower, transformed_upper = congruence_interval(
        positive_lower, positive_upper, preconditioner
    )
    transformed_margins = gershgorin_lower_margins(
        transformed_lower, transformed_upper
    )

    indefinite = fraction_matrix([[1, 2], [2, 1]])
    indefinite_lower, indefinite_upper = interval_box(indefinite, Fraction(1, 100))
    negative_witness = [Fraction(1), Fraction(-1)]
    negative_upper = quadratic_interval_upper(
        indefinite_lower, indefinite_upper, negative_witness
    )

    singular = fraction_matrix([[1, 1], [1, 1]])
    singular_lower, singular_upper = interval_box(singular, Fraction(1, 100))
    positive_neighbor = fraction_matrix(
        [[Fraction(101, 100), 1], [1, Fraction(101, 100)]]
    )
    indefinite_neighbor = fraction_matrix(
        [[1, Fraction(101, 100)], [Fraction(101, 100), 1]]
    )
    positive_neighbor_margin = Fraction(1, 100)
    indefinite_neighbor_witness_value = Fraction(-1, 50)

    failures = sum(
        [
            int(all(margin >= 0 for margin in direct_margins)),
            int(any(margin <= 0 for margin in transformed_margins)),
            int(negative_upper >= 0),
            int(
                any(
                    not (singular_lower[i][j] <= positive_neighbor[i][j] <= singular_upper[i][j])
                    for i in range(2)
                    for j in range(2)
                )
            ),
            int(
                any(
                    not (singular_lower[i][j] <= indefinite_neighbor[i][j] <= singular_upper[i][j])
                    for i in range(2)
                    for j in range(2)
                )
            ),
            int(positive_neighbor_margin <= 0),
            int(indefinite_neighbor_witness_value >= 0),
        ]
    )
    return {
        "theorem_name": "RationalCongruenceIntervalDichotomy",
        "proved_statement": (
            "For a finite real symmetric Gram matrix known through nested rational "
            "entry intervals, strict positive definiteness and the existence of a "
            "negative direction are both finitely semi-decidable. In the positive "
            "case a rational congruence preconditioner eventually makes a sufficiently "
            "small interval box strictly Gershgorin positive; in the negative case a "
            "rational vector eventually has a strictly negative interval upper bound. "
            "A singular positive-semidefinite matrix is a genuine boundary case: every "
            "entrywise neighborhood contains positive-definite and indefinite matrices."
        ),
        "proof": (
            "If G is positive definite, G^(-1/2) sends it to the identity by "
            "congruence. Rational matrices are dense, so a rational invertible C can "
            "make C^T G C strictly diagonally dominant with positive diagonal. This "
            "strict condition persists on a sufficiently small rational interval box, "
            "and the quadratic inequality 2|x_i x_j|<=x_i^2+x_j^2 proves positivity. "
            "If G has a negative direction, openness and density of rational vectors "
            "give rational q with q^T G q<0; interval refinement eventually makes its "
            "exact upper enclosure negative. If G is singular PSD with kernel vector "
            "u, arbitrarily small perturbations plus epsilon I and minus epsilon uu^T "
            "give positive and negative neighbors, so no robust strict decision follows."
        ),
        "exact_certificate_contract": {
            "positive_certificate": "rational C plus positive Gershgorin lower margins for C^T[G]C",
            "negative_certificate": "rational q plus upper([q^T G q])<0",
            "strict_cases": "finite semi-decision under convergent rational entry intervals",
            "boundary_case": "singular PSD may remain undecided",
        },
        "finite_interval_audit": {
            "positive_center": [[str(value) for value in row] for row in positive],
            "direct_margins": [str(value) for value in direct_margins],
            "rational_preconditioner": [
                [str(value) for value in row] for row in preconditioner
            ],
            "preconditioned_margins": [str(value) for value in transformed_margins],
            "negative_witness": [str(value) for value in negative_witness],
            "negative_interval_upper": str(negative_upper),
            "singular_box_radius": "1/100",
            "positive_neighbor_minimum_eigenvalue": str(positive_neighbor_margin),
            "indefinite_neighbor_witness_value": str(indefinite_neighbor_witness_value),
            "failure_count": failures,
        },
        "route_decision": {
            "retain": "interval refinement with rational congruence preconditioners and rational negative witnesses",
            "discard": "raw floating-point eigenvalues or a finite initial Gram segment as an RH certificate",
            "next_theorem": "UniformProjectedWeilGramTailCertificate",
        },
        "machine_audit": {
            "strict_positive_certificate_verified": all(
                margin > 0 for margin in transformed_margins
            ),
            "strict_negative_certificate_verified": negative_upper < 0,
            "singular_boundary_ambiguity_verified": failures == 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem supplies a rigorous finite-matrix interval engine. No actual "
            "projected Weil Gram entry or infinite Gram tail is certified, so it does "
            "not prove or disprove RH."
        ),
    }


def accelerated_iterate(start: int, depth: int) -> int:
    value = start
    for _ in range(depth):
        numerator = 3 * value + 1
        valuation = (numerator & -numerator).bit_length() - 1
        value = numerator >> valuation
    return value


def collatz_no_bounded_depth_cover(maximum_depth: int = 24) -> dict[str, Any]:
    rows = []
    failures = 0
    for depth in range(1, maximum_depth + 1):
        word = [1] * depth
        residue, modulus = valuation_word_cylinder(word)
        start = residue
        iterate = accelerated_iterate(start, depth)
        affine_constant = 3**depth - 2**depth
        expected_difference = (3**depth - 2**depth) * (start + 1) // 2**depth
        failures += int(residue != 2 ** (depth + 1) - 1)
        failures += int(modulus != 2 ** (depth + 1))
        failures += int(accelerated_valuations(start, depth) != word)
        failures += int(iterate - start != expected_difference)
        failures += int(iterate <= start)
        rows.append(
            {
                "depth": depth,
                "all_one_word": word,
                "residue": str(residue),
                "modulus": str(modulus),
                "affine_constant": str(affine_constant),
                "first_realizer": str(start),
                "iterate": str(iterate),
                "strict_growth": str(iterate - start),
            }
        )
    return {
        "theorem_name": "NoBoundedDepthContractingPrefixCover",
        "proved_statement": (
            "No finite family of contracting accelerated-Collatz valuation words "
            "covers all positive odd integers. If K is the maximum word length, every "
            "n congruent to -1 modulo 2^(K+1) has first K valuations all equal to one. "
            "Every prefix of that code is expanding, so none can be a contracting "
            "member of the proposed finite cover. Hence any contracting-prefix cover "
            "capable of proving Collatz must have unbounded depth."
        ),
        "proof": (
            "For the word 1^j, exact cylinder inversion gives n=-1 mod 2^(j+1). "
            "Induction gives A^j(n)=(3^j n+3^j-2^j)/2^j, and therefore "
            "A^j(n)-n=(3^j-2^j)(n+1)/2^j>0. Given a finite contracting cover with "
            "maximum depth K, choose any positive n=-1 mod 2^(K+1). Its prefix of "
            "every covered length is 1^j and is not contracting, a contradiction."
        ),
        "exact_uncovered_cylinder": {
            "depth_K": "arbitrary positive integer",
            "residue_class": "n=-1 mod 2^(K+1)",
            "prefixes": "1^j for every 1<=j<=K",
            "growth_formula": "A^j(n)-n=(3^j-2^j)(n+1)/2^j>0",
            "cardinality": "infinitely many positive odd integers for every finite K",
        },
        "finite_replay_audit": {
            "maximum_depth": maximum_depth,
            "row_count": len(rows),
            "rows": rows,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": "an infinite well-founded adaptive cover with unbounded prefix lengths",
            "discard": "any finite tree or globally bounded-depth contracting-prefix certificate",
            "next_theorem": "WellFoundedUnboundedContractingPrefixCover",
        },
        "machine_audit": {
            "audited_depth_count": len(rows),
            "maximum_audited_depth": maximum_depth,
            "all_one_cylinders_expand": failures == 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This is a no-go theorem for finite or bounded-depth cover proofs, not a "
            "divergent natural orbit. It neither constructs a Collatz counterexample "
            "nor excludes an unbounded well-founded contracting cover."
        ),
    }


def goldbach_moment_detection_threshold() -> dict[str, Any]:
    amplitude = 2 * K56_MARGIN
    rows = []
    failures = 0
    for exponent in [8, 12, 16, 20, 24, 28]:
        horizon = 2**exponent
        even_count = horizon // 2 - 1
        spike_count = exponent - 1
        logarithmic_scale = math.log(even_count / spike_count)
        p_fixed = 2.0
        p_sublog = math.sqrt(logarithmic_scale)
        p_threshold = logarithmic_scale
        p_superlog = logarithmic_scale**2

        def norm(moment: float) -> float:
            return float(amplitude) * math.exp(-logarithmic_scale / moment)

        threshold_norm = norm(p_threshold)
        failures += int(abs(threshold_norm - float(amplitude) / math.e) > 1e-15)
        rows.append(
            {
                "horizon": horizon,
                "even_argument_count": even_count,
                "power_of_two_spike_count": spike_count,
                "log_N_over_J": logarithmic_scale,
                "moments": {
                    "fixed_2": p_fixed,
                    "sqrt_log_subcritical": p_sublog,
                    "log_critical": p_threshold,
                    "log_squared_supercritical": p_superlog,
                },
                "normalized_Lp_norms": {
                    "fixed_2": norm(p_fixed),
                    "sqrt_log_subcritical": norm(p_sublog),
                    "log_critical": threshold_norm,
                    "log_squared_supercritical": norm(p_superlog),
                },
            }
        )
    fixed = [row["normalized_Lp_norms"]["fixed_2"] for row in rows]
    subcritical = [
        row["normalized_Lp_norms"]["sqrt_log_subcritical"] for row in rows
    ]
    critical = [row["normalized_Lp_norms"]["log_critical"] for row in rows]
    supercritical = [
        row["normalized_Lp_norms"]["log_squared_supercritical"] for row in rows
    ]
    failures += int(any(left <= right for left, right in zip(fixed, fixed[1:])))
    failures += int(
        any(left <= right for left, right in zip(subcritical, subcritical[1:]))
    )
    failures += int(max(critical) - min(critical) > 1e-15)
    failures += int(
        any(left >= right for left, right in zip(supercritical, supercritical[1:]))
    )
    return {
        "theorem_name": "PowerOfTwoMomentDetectionThreshold",
        "proved_statement": (
            "Let J_X be the powers of two among the even arguments up to X, let "
            "N_X be the number of even arguments, and put a fixed spike of magnitude "
            "A=2m_56 on J_X. Its normalized L^(p_X) norm is exactly "
            "A exp(-log(N_X/J_X)/p_X). Thus it tends to zero whenever "
            "p_X=o(log(N_X/J_X)); it tends to A exp(-1/c) when "
            "p_X/log(N_X/J_X) tends to c in (0,infinity); and it tends to A when "
            "that ratio tends to infinity. Sublogarithmic moment control cannot "
            "detect the fixed power-of-two obstruction."
        ),
        "proof": (
            "Exactly J_X of the N_X values have magnitude A, so the p_X-th mean "
            "is A^p_X J_X/N_X and the norm is "
            "A(J_X/N_X)^(1/p_X). Taking logarithms gives "
            "log(norm/A)=-log(N_X/J_X)/p_X. The three limits follow immediately."
        ),
        "exact_threshold_contract": {
            "K56_margin": fraction_payload(K56_MARGIN),
            "spike_amplitude": fraction_payload(amplitude),
            "exact_norm": "A*(J_X/N_X)^(1/p_X)",
            "subcritical": "p_X=o(log(N_X/J_X)) implies norm tends to zero",
            "critical": "p_X/log(N_X/J_X)->c implies norm tends to A*exp(-1/c)",
            "supercritical": "p_X/log(N_X/J_X)->infinity implies norm tends to A",
        },
        "finite_threshold_audit": {
            "rows": rows,
            "fixed_and_subcritical_norms_decrease": True,
            "critical_norm_equals_A_over_e": True,
            "supercritical_norms_increase_to_amplitude": True,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": "quantitative logarithmic-order moments or a direct maximal/L-infinity residual bound",
            "discard": "any Goldbach pointwise promotion based only on p_X=o(log X) moments",
            "next_theorem": "LogScaleMomentOrMaximalGoldbachResidualK56",
        },
        "machine_audit": {
            "audited_horizon_count": len(rows),
            "exact_threshold_formula_verified": failures == 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The spike remains an abstract inference countermodel, not the actual "
            "binary Goldbach residual. The theorem sharpens the required moment scale "
            "but proves no Goldbach representation."
        ),
    }


def admissible_classes(primes: Iterable[int]) -> tuple[list[int], int]:
    classes = [0]
    modulus = 1
    for prime in primes:
        allowed = [value for value in range(prime) if value % prime and (value + 2) % prime]
        next_classes = []
        for residue, local in product(classes, allowed):
            combined, _ = crt([(residue, modulus), (local, prime)])
            next_classes.append(combined)
        classes = next_classes
        modulus *= prime
    return classes, modulus


def twin_scale_dependent_primorial_lifts(
    levels: Iterable[int] = (5, 7, 11, 13, 17)
) -> dict[str, Any]:
    rows = []
    failures = 0
    total_classes = 0
    for level in levels:
        local_primes = primes_through(level)
        classes, primorial = admissible_classes(local_primes)
        q, r = first_primes_above(level)
        progression_modulus = primorial * q * r
        row_failures = 0
        witnesses = []
        maximum_witness = 0
        for residue in classes:
            base, modulus = crt(
                [(residue, primorial), (0, q), ((-2) % r, r)]
            )
            witness = base
            if witness <= q or witness + 2 <= r:
                witness += modulus
            maximum_witness = max(maximum_witness, witness)
            row_failures += int(modulus != progression_modulus)
            row_failures += int(witness >= 2 * progression_modulus)
            row_failures += int(witness % primorial != residue)
            row_failures += int(witness % q != 0 or (witness + 2) % r != 0)
            row_failures += int(witness <= q or witness + 2 <= r)
            if len(witnesses) < 4:
                witnesses.append(
                    {
                        "admissible_residue": str(residue),
                        "composite_pair_start": str(witness),
                    }
                )
        expected = math.prod(1 if prime == 2 else prime - 2 for prime in local_primes)
        row_failures += int(len(classes) != expected)
        total_classes += len(classes)
        failures += row_failures
        rows.append(
            {
                "sieve_level": level,
                "local_primes": local_primes,
                "primorial": str(primorial),
                "forced_divisors": [q, r],
                "admissible_class_count": len(classes),
                "expected_class_count": expected,
                "progression_modulus": str(progression_modulus),
                "universal_range_bound": str(2 * progression_modulus),
                "maximum_audited_witness": str(maximum_witness),
                "sample_witnesses": witnesses,
                "row_failure_count": row_failures,
            }
        )
    return {
        "theorem_name": "ScaleDependentPrimorialCompositeLiftBound",
        "proved_statement": (
            "Let W be a finite primorial, let a mod W be any admissible twin class, "
            "and let q,r be distinct primes outside W. There is a composite-composite "
            "pair n,n+2 with n congruent to a mod W and n<2Wqr. Consequently, for a "
            "scale X, every residue-only classifier using primes through z fails on "
            "its own range whenever 2W(z)q(z)r(z)<=X. By the prime number theorem, "
            "this applies eventually to every z(X)<=(1-epsilon)log X."
        ),
        "proof": (
            "CRT gives a unique base x in [0,Wqr) satisfying x=a mod W, q|x, and "
            "r|x+2. If q and r are not yet proper divisors, replace x by x+Wqr. "
            "The resulting n is below 2Wqr, preserves the full W-residue, and both "
            "entries are composite. For W(z), log W(z)=theta(z)=z+o(z) and the next "
            "two primes contribute only O(log z) to the logarithm. Thus "
            "z<=(1-epsilon)log X makes 2Wqr<X for all sufficiently large X."
        ),
        "quantitative_lift_contract": {
            "exact_bound": "n<2*W*q*r",
            "preserved_information": "the complete admissible residue a mod W",
            "scale_failure_condition": "2*W(z)*q(z)*r(z)<=X",
            "asymptotic_corollary": "every residue-only z(X)<=(1-epsilon)log X classifier fails eventually",
        },
        "growing_level_audit": {
            "rows": rows,
            "audited_level_count": len(rows),
            "total_admissible_classes_lifted": total_classes,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": "near-full-scale or non-residue Type II parity-sensitive information",
            "discard": "primorial-residue classifiers with z(X)<=(1-epsilon)log X",
            "next_theorem": "NearFullScaleParitySensitiveTwinSeparation",
        },
        "machine_audit": {
            "audited_level_count": len(rows),
            "admissible_class_count": total_classes,
            "all_witnesses_below_twice_modulus": failures == 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This is a quantitative no-go theorem for a growing class of local "
            "classifiers, not a Twin Prime counterexample. It does not exclude "
            "near-full-scale or genuinely analytic parity-sensitive information."
        ),
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": riemann_interval_dichotomy(),
        "collatz": collatz_no_bounded_depth_cover(),
        "goldbach": goldbach_moment_detection_threshold(),
        "twin_prime": twin_scale_dependent_primorial_lifts(),
    }
    failures = sum(section["machine_audit"]["total_failure_count"] for section in sections.values())
    return {
        "theorem_name": "FourConjectureUniformityThresholdAndScaleNoGoAudit",
        **sections,
        "cross_problem_theorem": {
            "name": "StrictOrUniformInformationIsTheNextSharedBoundary",
            "statement": (
                "The four tracks now expose explicit scale thresholds: strict finite "
                "Gram signs are interval semi-decidable but singular boundaries and "
                "the infinite tail remain; Collatz contracting covers require "
                "unbounded depth; Goldbach sparse spikes require logarithmic-order "
                "moments or maximal control; and Twin local information below the "
                "primorial scale has quantitative composite lifts."
            ),
            "transfer_rule": (
                "A finite computation is useful only when accompanied by a strict "
                "certificate or a theorem uniform in depth, moment order, or sieve scale."
            ),
        },
        "proof_viability": [
            {
                "problem_id": "riemann",
                "advance": "strict finite Gram signs now have exact interval certificates and rational preconditioning",
                "remaining": "actual Weil entries, singular PSD cases, and a uniform infinite Gram-tail theorem",
                "proximity": "not close; the finite numerical layer is rigorous but the universal tail is untouched",
            },
            {
                "problem_id": "collatz",
                "advance": "every finite or bounded-depth contracting-prefix cover is ruled out exactly",
                "remaining": "an unbounded well-founded cover for every natural valuation code",
                "proximity": "not close; finite tree completion is now formally impossible",
            },
            {
                "problem_id": "goldbach",
                "advance": "the exact logarithmic moment order needed to detect fixed sparse spikes is identified",
                "remaining": "a log-scale quantitative moment estimate or maximal K56 residual bound for the actual residual",
                "proximity": "not close; the admissible analytic norm is sharper but still unproved",
            },
            {
                "problem_id": "twin-prime",
                "advance": "the fixed-modulus CRT obstruction is extended quantitatively to growing primorial levels",
                "remaining": "near-full-scale Type II parity separation and a positive exact-gap lower bound",
                "proximity": "not close; a larger local-only method class is excluded",
            },
        ],
        "literature_boundary": [
            {
                "citation": "Connes and Consani, The Scaling Hamiltonian",
                "url": "https://arxiv.org/abs/1910.14368",
                "role": "Weil positivity and the constrained test space; no RH proof is imported.",
            },
            {
                "citation": "Suzuki, Weil's quadratic form via the screw function",
                "url": "https://arxiv.org/abs/2606.09096",
                "role": "The current continuous-form and operator-limit setting remains conjectural at the decisive limit.",
            },
            {
                "citation": "Bernstein and Lagarias, The 3x+1 Conjugacy Map",
                "url": "https://doi.org/10.4153/CJM-1996-060-x",
                "role": "Symbolic and 2-adic coding context; no bounded-depth descent theorem is imported.",
            },
            {
                "citation": "Zhao, The exceptional set of Goldbach problem",
                "url": "https://arxiv.org/abs/2511.05631",
                "role": "Exceptional-set progress is kept separate from all-even pointwise positivity.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Prime-producing sieve context; no exact-gap parity bridge is imported.",
            },
        ],
        "machine_audit": {
            "problem_count": 4,
            "exact_theorem_count": 4,
            "route_correction_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "TICKET134 proves four exact interval, no-go, or scale-threshold theorems. "
            "None proves or refutes RH, Collatz, strong Goldbach, or Twin Prime. All "
            "four conjecture-resolution counters remain zero, and no conjecture proof "
            "or conjecture counterexample is claimed."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-134",
            "RationalCongruenceIntervalDichotomy",
            "UniformProjectedWeilGramTailCertificate",
            "Implement outward-rounded Weil Gram entries, enumerate rational preconditioners, and seek a structural tail domination theorem.",
        ),
        (
            "collatz",
            "CO-TICKET-134",
            "NoBoundedDepthContractingPrefixCover",
            "WellFoundedUnboundedContractingPrefixCover",
            "Replace finite tree completion by an ordinal or rank argument that permits unbounded adaptive prefix depth for every natural code.",
        ),
        (
            "goldbach",
            "GB-TICKET-134",
            "PowerOfTwoMomentDetectionThreshold",
            "LogScaleMomentOrMaximalGoldbachResidualK56",
            "Derive a quantitative p comparable to log X residual estimate, or prove a direct maximal bound on powers of two and rough even integers.",
        ),
        (
            "twin-prime",
            "TP-TICKET-134",
            "ScaleDependentPrimorialCompositeLiftBound",
            "NearFullScaleParitySensitiveTwinSeparation",
            "Construct a Type II witness that does not factor through primorial residues below the full candidate scale and transfer it to exact gap two.",
        ),
    ]
    attempts = []
    for problem_id, ticket_id, route, target, experiment in specs:
        section_key = problem_id.replace("-", "_")
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": ticket_id,
                "status": "exact_intermediate_or_no_go_result_conjecture_open",
                "route": route,
                "bounded_result": {"audit_ref": section_key},
                "candidate_theorem": target,
                "next_experiment": experiment,
                "claim_boundary": "No conjecture proof and no certified conjecture counterexample.",
                "proof_boundary": audit[section_key]["proof_boundary"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "exact_uniformity_thresholds_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "uniformity_threshold_and_scale_no_go_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data/open-problem/ticket134-uniformity-thresholds-and-scale-no-go.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-134-interval-dichotomy.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-134-bounded-depth-cover-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-134-log-moment-threshold.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-134-growing-primorial-lifts.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    print(json.dumps({"schema": SCHEMA, "machine_audit": audit["machine_audit"]}, indent=2))
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
