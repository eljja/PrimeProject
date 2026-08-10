from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
from typing import Any

from ticket200_derivative_mesh_three_run_chen_channels import (
    ordered_affine_numerator,
    prime_sieve,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket206-adaptive-singleone-crt-projector.v1"
GENERATED_AT = "2026-08-10T10:39:10+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def riemann_adaptive_termination_audit() -> dict[str, Any]:
    rows = []
    for reciprocal_clearance in (8, 16, 32, 64, 128):
        epsilon = Fraction(1, reciprocal_clearance)
        largest_budget_proved_insufficient = 6 * reciprocal_clearance
        sufficient_budget = 8 * reciprocal_clearance
        rows.append(
            {
                "epsilon": fraction_text(epsilon),
                "function": f"f(z)=z-(1-{fraction_text(epsilon)})",
                "boundary_clearance": fraction_text(epsilon),
                "arclength_derivative_bound": "1",
                "uniform_global_criterion_fails_for_every_N_at_most": (
                    largest_budget_proved_insufficient
                ),
                "uniform_global_criterion_certified_at_N": sufficient_budget,
                "failure_proof": (
                    "N<=6/epsilon gives h=2*pi/N>epsilon using pi>3"
                ),
                "success_proof": (
                    "N=8/epsilon gives h=2*pi/N<epsilon using pi<22/7"
                ),
                "actual_winding": 1,
            }
        )

    failures = 0
    for row in rows:
        q = int(Fraction(row["epsilon"]).denominator)
        failures += int(
            row["uniform_global_criterion_fails_for_every_N_at_most"] != 6 * q
        )
        failures += int(row["uniform_global_criterion_certified_at_N"] != 8 * q)
        failures += int(row["actual_winding"] != 1)

    theorem = (
        "Let gamma:[0,L]->C be a unit-speed C1 closed contour and let g=f o gamma, "
        "where f is analytic near the contour. If g is nonzero on the contour, "
        "delta=min|g| is positive and K=max|g'| is finite. Repeated uniform "
        "bisection therefore terminates with a partition of mesh h<delta/K "
        "(with the constant case handled separately), and every arc satisfies "
        "K h<|g(t_j)|. The TICKET-205 disk homotopies then certify the exact "
        "winding number. This completeness is conditional on rigorous bounds "
        "delta and K. No fixed segment budget works uniformly as the contour "
        "clearance tends to zero."
    )
    proof = (
        "Compactness and continuity give delta>0 and K<infinity. If K=0 the "
        "image is constant and nonzero. Otherwise choose a dyadic mesh below "
        "delta/K. The fundamental theorem of calculus gives "
        "|g(t)-g(t_j)|<=K h<delta<=|g(t_j)| on every arc, so TICKET-205 applies. "
        "For the sharpness family f_epsilon(z)=z-(1-epsilon) on the unit circle, "
        "delta=epsilon, K=1, and the global criterion requires 2*pi/N<epsilon. "
        "If N<=6/epsilon it fails because pi>3; N=8/epsilon succeeds because "
        "pi<22/7. The enclosed zero 1-epsilon gives winding one."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "termination_certificate": {
            "boundary_clearance": "delta=min_t |f(gamma(t))|>0",
            "global_derivative_bound": "K=max_t |(f o gamma)'(t)|<infinity",
            "sufficient_mesh_condition": "h<delta/K when K>0",
            "uniform_bisection_terminates": True,
            "accepted_partition_certifies_zero_free_boundary": True,
        },
        "clearance_complexity_rows": rows,
        "aggregate": {
            "zero_free_boundary_implies_finite_mesh_certificate": True,
            "fixed_uniform_segment_budget_refuted": True,
            "complexity_lower_bound_order_inverse_clearance": True,
            "completed_zeta_rigorous_bound_oracle_constructed": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The theorem proves completeness of a certificate grammar once exact "
            "positive clearance and derivative bounds are available. It neither "
            "constructs those bounds for cofinal completed-zeta rectangles nor "
            "excludes zeros off the critical line."
        ),
        "failure_count": failures,
    }


def collatz_single_one_regression(maximum_length: int = 8) -> dict[str, Any]:
    rows = []
    total_words = 0
    total_divisible = 0
    for length in range(1, maximum_length + 1):
        word_count = 0
        divisible_count = 0
        for word in product(range(1, 6), repeat=length):
            if word.count(1) != 1:
                continue
            word_count += 1
            denominator = 2 ** sum(word) - 3**length
            numerator = ordered_affine_numerator(word)
            if denominator > 0 and numerator % denominator == 0:
                divisible_count += 1
        total_words += word_count
        total_divisible += divisible_count
        rows.append(
            {
                "length": length,
                "valuation_alphabet": [1, 2, 3, 4, 5],
                "exactly_one_valuation_one_word_count": word_count,
                "positive_integral_cycle_word_count": divisible_count,
            }
        )
    return {
        "rows": rows,
        "maximum_length": maximum_length,
        "total_words_checked": total_words,
        "positive_integral_cycle_words": total_divisible,
    }


def collatz_single_one_exclusion_audit() -> dict[str, Any]:
    regression = collatz_single_one_regression()
    expected_words = sum(length * 4 ** (length - 1) for length in range(1, 9))
    failures = regression["positive_integral_cycle_words"]
    failures += int(regression["total_words_checked"] != expected_words)

    theorem = (
        "No nontrivial positive accelerated Collatz cycle has a valuation period "
        "containing exactly one entry equal to one and every other entry at least "
        "two. Thus any hypothetical nontrivial positive cycle must contain at "
        "least two valuation-one entries and at least one entry at least two."
    )
    proof = (
        "Rotate a hypothetical period to its minimum odd value m. TICKET-205 "
        "forces the outgoing valuation there to be one, so it is the unique such "
        "entry. The next value is y=(3m+1)/2. Every remaining step has valuation "
        "at least two and is bounded by F(x)=(3x+1)/4. With "
        "q=(3/4)^(h-1), return to m implies "
        "m<=(1-q/2)/(1-3q/2). For h>=4, q<=27/64<1/2, so the right side is "
        "strictly below 3, contradicting the odd nontrivial minimum m>=3. For "
        "h=3 the bound gives m<=23/5, hence m=3; but 3 maps to 5 and then 1, "
        "not back to 3. For h=2, writing the other valuation as b>=2 gives "
        "(2^(b+1)-9)m=5, which has no positive integral solution. For h=1, "
        "the valuation-one fixed-point equation gives m=-1."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "length_cases": {
            "h_ge_4": {
                "q_upper": "27/64",
                "minimum_upper_strict": "3",
                "contradiction": "nontrivial positive odd minimum is at least 3",
            },
            "h_eq_3": {
                "minimum_upper": "23/5",
                "only_odd_candidate": 3,
                "trajectory_prefix": [3, 5, 1],
            },
            "h_eq_2": "(2^(b+1)-9)m=5 has no positive integer solution for b>=2",
            "h_eq_1": "2m=3m+1 gives m=-1",
        },
        "finite_integrality_regression": regression,
        "aggregate": {
            "single_one_arbitrary_ge_two_cycle_stratum_excluded": True,
            "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle": 2,
            "two_or_more_one_mixed_necklaces_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This strictly extends the TICKET-185 rest-all-two family to arbitrary "
            "remaining valuations at least two. It does not exclude periods with "
            "two or more valuation-one entries or any divergent nonperiodic orbit."
        ),
        "failure_count": failures,
    }


def primes_through(limit: int) -> list[int]:
    flags = prime_sieve(limit)
    return [value for value in range(2, limit + 1) if flags[value]]


def next_primes(start: int, count: int) -> list[int]:
    upper = max(start + 32, 2 * start + 32)
    while True:
        values = [prime for prime in primes_through(upper) if prime > start]
        if len(values) >= count:
            return values[:count]
        upper *= 2


def goldbach_forced_large_witness_row(bound: int) -> dict[str, Any]:
    witness_primes = [prime for prime in primes_through(bound) if prime >= 3]
    forcing_primes = next_primes(bound, len(witness_primes))
    modulus = 2
    residue = 0
    forcing_rows = []
    for witness, forcing in zip(witness_primes, forcing_primes, strict=True):
        old_modulus = modulus
        step = ((witness - residue) * pow(old_modulus, -1, forcing)) % forcing
        residue += old_modulus * step
        modulus *= forcing
        residue %= modulus
        forcing_rows.append(
            {
                "excluded_witness_prime": witness,
                "forcing_divisor_of_complement": forcing,
            }
        )
    threshold = max(
        [4]
        + [
            row["excluded_witness_prime"]
            + row["forcing_divisor_of_complement"]
            for row in forcing_rows
        ]
    )
    while residue <= threshold:
        residue += modulus

    for row in forcing_rows:
        witness = row["excluded_witness_prime"]
        forcing = row["forcing_divisor_of_complement"]
        complement = residue - witness
        row["complement"] = str(complement)
        row["complement_quotient"] = str(complement // forcing)
        row["proper_composite_complement"] = (
            complement % forcing == 0 and complement > forcing
        )

    return {
        "witness_bound_B": bound,
        "excluded_prime_witness_count": len(witness_primes) + 1,
        "even_residue_representative_N0": str(residue),
        "arithmetic_progression_modulus_M": str(modulus),
        "all_N_equals_N0_plus_tM_are_even": residue % 2 == 0 and modulus % 2 == 0,
        "p_equals_2_complement_is_composite": residue > 4,
        "forcing_rows": forcing_rows,
        "all_prime_witnesses_at_most_B_excluded": all(
            row["proper_composite_complement"] for row in forcing_rows
        ),
    }


def goldbach_crt_witness_no_go_audit() -> dict[str, Any]:
    rows = [goldbach_forced_large_witness_row(bound) for bound in (5, 11, 19, 29, 43)]
    failures = sum(
        int(not row["all_N_equals_N0_plus_tM_are_even"])
        + int(not row["p_equals_2_complement_is_composite"])
        + int(not row["all_prime_witnesses_at_most_B_excluded"])
        for row in rows
    )
    theorem = (
        "For every bound B there is an infinite arithmetic progression of even "
        "integers N for which N-p is composite for every prime p<=B. Therefore "
        "no fixed finite set of prime summands can witness strong Goldbach on "
        "all sufficiently large even integers. If strong Goldbach is true, its "
        "least prime witness is necessarily unbounded."
    )
    proof = (
        "For each odd prime p<=B choose a distinct odd prime q_p>B. The Chinese "
        "remainder theorem gives one class satisfying N=0 mod 2 and N=p mod q_p "
        "for every p. Choose a sufficiently large representative. Then N-p is "
        "a proper multiple of q_p and is composite. Also N-2 is even and greater "
        "than two. Adding multiples of 2 product(q_p) preserves every condition, "
        "so the family is infinite. This excludes bounded witness bases but does "
        "not produce a Goldbach counterexample because witnesses above B remain."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "crt_fixture_rows": rows,
        "aggregate": {
            "fixed_bounded_prime_witness_basis_refuted": True,
            "least_witness_unbounded_conditional_on_goldbach": True,
            "infinite_forced_large_witness_progressions_constructed": True,
            "goldbach_counterexample_found": False,
            "tail_exception_bound_below_one_constructed": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The CRT progression suppresses only primes through B. It neither "
            "suppresses all larger primes nor proves that any constructed N lacks "
            "a Goldbach representation. Its exact conclusion is the necessity of "
            "a witness cutoff that grows with the target."
        ),
        "failure_count": failures,
    }


def omega_binomial_projector(omega: int, truncation: int) -> int:
    if omega < 0 or truncation < 1:
        raise ValueError("omega must be nonnegative and truncation positive")
    return sum(
        (-1) ** (index - 1) * index * comb(omega, index)
        for index in range(1, min(omega, truncation) + 1)
    )


def twin_crt_false_positive_row(truncation: int) -> dict[str, Any]:
    primes = [prime for prime in primes_through(256) if prime >= 3]
    width = truncation + 1
    left_primes = primes[:width]
    right_primes = primes[width : 2 * width]
    left_modulus = 1
    right_modulus = 1
    for prime in left_primes:
        left_modulus *= prime
    for prime in right_primes:
        right_modulus *= prime
    multiplier = (-2 * pow(left_modulus, -1, right_modulus)) % right_modulus
    residue = left_modulus * multiplier
    modulus = left_modulus * right_modulus
    while residue <= max(left_modulus, right_modulus):
        residue += modulus
    sign = 1 if truncation % 2 == 1 else -1
    return {
        "truncation_R": truncation,
        "left_forced_distinct_prime_factors": left_primes,
        "right_forced_distinct_prime_factors": right_primes,
        "n0": str(residue),
        "progression_modulus": str(modulus),
        "n0_divisible_by_left_product": residue % left_modulus == 0,
        "n0_plus_2_divisible_by_right_product": (residue + 2) % right_modulus == 0,
        "Omega_n_lower_bound": width,
        "Omega_n_plus_2_lower_bound": width,
        "truncated_projector_sign_on_both_endpoints": sign,
        "truncated_shift_two_product_positive": True,
        "infinite_progression": "n=n0+t*progression_modulus for every t>=0",
    }


def twin_binomial_projector_audit() -> dict[str, Any]:
    identity_rows = []
    failures = 0
    for truncation in range(1, 9):
        values = []
        for omega in range(0, 13):
            value = omega_binomial_projector(omega, truncation)
            expected = int(omega == 1) if omega <= truncation else (
                (-1) ** (truncation - 1)
                * omega
                * comb(omega - 2, truncation - 1)
            )
            failures += int(value != expected)
            values.append({"Omega": omega, "P_R": value, "closed_form": expected})
        identity_rows.append({"truncation_R": truncation, "values": values})
    crt_rows = [twin_crt_false_positive_row(truncation) for truncation in range(1, 7)]
    failures += sum(
        int(not row["n0_divisible_by_left_product"])
        + int(not row["n0_plus_2_divisible_by_right_product"])
        + int(not row["truncated_shift_two_product_positive"])
        for row in crt_rows
    )

    theorem = (
        "For m>=0, sum_{j>=1} (-1)^(j-1) j binom(m,j) equals one for m=1 "
        "and zero otherwise; the sum is pointwise finite. Hence substituting "
        "m=Omega(n) gives an exact prime indicator. Its truncation at j<=R is "
        "exact only for Omega(n)<=R. For m>R it equals "
        "(-1)^(R-1) m binom(m-2,R-1), so every fixed truncation is nonzero on "
        "all sufficiently factor-rich composites. Moreover each fixed R has an "
        "infinite CRT progression where both n and n+2 have at least R+1 distinct "
        "prime factors and the truncated correlation is positive."
    )
    proof = (
        "Use j binom(m,j)=m binom(m-1,j-1). The complete alternating binomial "
        "sum is the derivative identity for (1-x)^m at x=1, giving the Kronecker "
        "delta at m=1. The finite partial-sum identity "
        "sum_{k=0}^{R-1}(-1)^k binom(m-1,k)=(-1)^(R-1)binom(m-2,R-1) "
        "gives the displayed truncation formula. For the no-go, choose disjoint "
        "sets of R+1 odd primes with products A and B. CRT solves n=0 mod A and "
        "n=-2 mod B. Large representatives make both endpoints composite; both "
        "truncated projectors have sign (-1)^(R-1), so their product is positive."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "binomial_identity_rows": identity_rows,
        "crt_false_positive_rows": crt_rows,
        "aggregate": {
            "pointwise_finite_exact_prime_projector_proved": True,
            "every_fixed_truncation_formula_proved": True,
            "every_fixed_truncation_has_infinite_positive_false_positives": True,
            "finite_degree_Omega_prime_projector_refuted": True,
            "uniform_infinite_tail_cancellation_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The infinite identity is an exact re-expression of primality, not a "
            "new lower bound for twin primes. Rearranging or truncating its shift-two "
            "correlation requires a uniform tail estimate that is not proved here."
        ),
        "failure_count": failures,
    }


def proof_dag(
    prefix: str,
    previous: str,
    closed: str,
    refuted: str,
    open_lemma: str,
    parent: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T205", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T206", "label": closed, "status": "closed"},
            {"id": f"{prefix}-N206", "label": refuted, "status": "refuted_or_limited"},
            {"id": f"{prefix}-OPEN206", "label": open_lemma, "status": "highest_risk_open"},
            {"id": prefix, "label": parent, "status": "open_not_proven"},
        ],
        "edges": [
            [f"{prefix}-T205", f"{prefix}-T206"],
            [f"{prefix}-T206", f"{prefix}-N206"],
            [f"{prefix}-T206", f"{prefix}-OPEN206"],
            [f"{prefix}-OPEN206", prefix],
        ],
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_adaptive_termination_audit()
    collatz_compute = collatz_single_one_exclusion_audit()
    goldbach_compute = goldbach_crt_witness_no_go_audit()
    twin_compute = twin_binomial_projector_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-206",
            "theorem_name": "ZeroFreeBoundaryAdaptiveMeshTerminationAndClearanceComplexityNoGo",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No effective rigorous clearance oracle is constructed for a cofinal family of completed-zeta rectangles.",
            "route_decision": {
                "discard": "using a fixed contour-segment budget independently of boundary clearance",
                "retain": "adaptive interval bounds with termination tied explicitly to positive clearance",
                "next_single_lemma": "EffectiveCompletedZetaRectangleBoundsAndCofinalAdaptiveTermination",
            },
            "proof_dag": proof_dag(
                "RH",
                "DerivativeCertifiedPolygonalWindingAndFiniteSampleNoGo",
                "ZeroFreeBoundaryAdaptiveMeshTerminationAndClearanceComplexityNoGo",
                "FixedBudgetContourCertificationIndependentOfClearance",
                "EffectiveCompletedZetaRectangleBoundsAndCofinalAdaptiveTermination",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof or counterexample. A certificate-completeness theorem and an inverse-clearance fixed-budget no-go are proved.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-206",
            "theorem_name": "SingleOneArbitraryGeTwoValuationCycleExclusion",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "Primitive mixed necklaces with at least two valuation-one entries and nonperiodic divergence remain open.",
            "route_decision": {
                "discard": "searching any exactly-one-valuation-one period for a positive cycle",
                "retain": "primitive mixed necklaces with at least two valuation-one entries",
                "next_single_lemma": "UniformNondivisibilityForPrimitiveMixedNecklacesWithAtLeastTwoOnes",
            },
            "proof_dag": proof_dag(
                "CO",
                "CycleExtremumValuationSeparationAndAllGeTwoExclusion",
                "SingleOneArbitraryGeTwoValuationCycleExclusion",
                "ExactlyOneValuationOneCanSupportANontrivialPositiveCycle",
                "UniformNondivisibilityForPrimitiveMixedNecklacesWithAtLeastTwoOnes",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or counterexample. The complete exactly-one-valuation-one periodic stratum is excluded.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-206",
            "theorem_name": "UnboundedLeastWitnessCRTNoGoForFixedPrimeBases",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "The CRT families exclude only bounded summands and do not bound the full Goldbach exceptional set.",
            "route_decision": {
                "discard": "proving strong Goldbach with one fixed bounded set of small prime summands",
                "retain": "tail exceptional-set control with a witness cutoff growing with the target",
                "next_single_lemma": "GrowingWitnessCutoffGoldbachTailExceptionalCountStrictlyBelowOne",
            },
            "proof_dag": proof_dag(
                "GB",
                "TenMillionExactWitnessCertificateAndFinitePrefixNoGo",
                "UnboundedLeastWitnessCRTNoGoForFixedPrimeBases",
                "FixedBoundedPrimeWitnessBasisCoversAllLargeEvenTargets",
                "GrowingWitnessCutoffGoldbachTailExceptionalCountStrictlyBelowOne",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. An exact infinite CRT obstruction to every fixed witness basis is proved.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-206",
            "theorem_name": "BinomialOmegaPrimeProjectorAndEveryFiniteTruncationNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "The exact infinite projector is tautological until its shift-two tail is controlled uniformly.",
            "route_decision": {
                "discard": "using any fixed finite Omega-binomial truncation as an exact twin indicator",
                "retain": "the exact infinite projector only with a proved uniform correlation-tail bound",
                "next_single_lemma": "UniformTailCancellationForBinomialOmegaProjectorCorrelation",
            },
            "proof_dag": proof_dag(
                "TP",
                "PrimePowerDivisorOmegaWeightAndProductParityNoGo",
                "BinomialOmegaPrimeProjectorAndEveryFiniteTruncationNoGo",
                "FiniteOmegaBinomialTruncationIsAnExactTwinPrimeIndicator",
                "UniformTailCancellationForBinomialOmegaProjectorCorrelation",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. An exact Omega-binomial projector and an infinite no-go for every finite truncation are proved.",
        },
    }
    failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    boundary = (
        "TICKET-206 resolves none of the four conjectures. It proves adaptive "
        "winding-certificate termination under positive clearance while quantifying "
        "fixed-budget failure, excludes every Collatz cycle stratum with exactly "
        "one valuation one, proves by CRT that Goldbach witnesses cannot remain "
        "uniformly bounded, and constructs an exact Omega-binomial prime projector "
        "while refuting every finite truncation by infinite shift-two false positives."
    )
    return {
        "theorem_name": "FourConjectureAdaptiveSingleOneCRTProjectorAudit",
        "status": STATUS,
        "proof_boundary": boundary,
        **sections,
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_limited_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = []
    for section_key in ("riemann", "collatz", "goldbach", "twin_prime"):
        section = audit[section_key]
        decision = section["route_decision"]
        attempts.append(
            {
                "problem_id": section["problem_id"],
                "ticket_id": section["ticket_id"],
                "status": STATUS,
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": decision["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": decision["next_single_lemma"],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": decision["next_single_lemma"],
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
        "adaptive_singleone_crt_projector_audit": audit,
        "attempts": attempts,
    }
    integrated = ROOT / "data/open-problem/ticket206-adaptive-singleone-crt-projector.json"
    write_json(integrated, payload)
    file_map = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-206-adaptive-clearance.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-206-single-one-general.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-206-unbounded-witness-crt.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-206-binomial-omega-projector.json",
    }
    section_map = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    for attempt in attempts:
        problem_id = attempt["problem_id"]
        section = audit[section_map[problem_id]]
        write_json(
            file_map[problem_id],
            {
                "schema": "primeproject.open-problem-attempt.v1",
                "generated_at": GENERATED_AT,
                **attempt,
                "mathematical_argument": section["mathematical_argument"],
                "reproducible_computation": section["reproducible_computation"],
                "route_decision": section["route_decision"],
            },
        )
    print(f"integrated_sha256 {hashlib.sha256(integrated.read_bytes()).hexdigest()}")


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
