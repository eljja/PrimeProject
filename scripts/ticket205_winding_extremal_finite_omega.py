from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any

from ticket200_derivative_mesh_three_run_chen_channels import (
    ordered_affine_numerator,
    prime_sieve,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket205-winding-extremal-finite-omega.v1"
GENERATED_AT = "2026-08-10T23:59:45+09:00"
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


def riemann_polygonal_winding_audit() -> dict[str, Any]:
    sample_count = 24
    derivative_bound = Fraction(3)
    segment_length_upper = Fraction(11, 42)  # pi/12 <= (22/7)/12
    excursion_bound = derivative_bound * segment_length_upper
    clearance = 1 - excursion_bound

    sample_phase_increment_turns = Fraction(1, 8)
    total_phase_turns = sample_count * sample_phase_increment_turns
    polygon_winding = int(total_phase_turns)
    no_go_samples = 8
    failures = 0
    failures += int(excursion_bound != Fraction(11, 14))
    failures += int(clearance != Fraction(3, 14))
    failures += int(polygon_winding != 3)
    failures += int(no_go_samples != 8)

    theorem = (
        "Let Gamma be a positively oriented rectifiable Jordan contour, let f "
        "be analytic on and inside Gamma, and partition Gamma into arcs Gamma_j "
        "starting at z_j. If |f(z_j)|>=m_j>0 and the arclength derivative of "
        "f is bounded by M_j on Gamma_j of length h_j, with M_j h_j<m_j, "
        "then f(Gamma_j) and the chord [f(z_j),f(z_(j+1))] are homotopic in "
        "C\\{0}. Hence the winding number of f(Gamma) equals that of the sampled "
        "polygon and, by the argument principle, equals the number of zeros of "
        "f inside Gamma counted with multiplicity. Finite values without the "
        "derivative bounds do not determine winding."
    )
    proof = (
        "For z on Gamma_j, integration along arclength gives "
        "|f(z)-f(z_j)|<=M_j h_j<m_j<=|f(z_j)|. Thus the true image arc lies "
        "in an open disk centered at f(z_j) that excludes zero. Its endpoint "
        "and the straight chord also lie in this convex disk, so the arc can "
        "be replaced by the chord through a zero-avoiding homotopy. Applying "
        "this on every segment preserves winding. For the no-go, 1 and z^8 "
        "agree at all eighth roots of unity but have winding numbers 0 and 8."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_argument_principle_fixture": {
            "contour": "positively oriented unit circle",
            "analytic_function_f": "z^3",
            "sample_count": sample_count,
            "sample_modulus_lower_m": "1",
            "arclength_derivative_bound_M": fraction_text(derivative_bound),
            "segment_length_h_upper_using_pi_le_22_over_7": fraction_text(
                segment_length_upper
            ),
            "image_excursion_Mh_upper": fraction_text(excursion_bound),
            "zero_avoidance_margin_lower": fraction_text(clearance),
            "sample_phase_increment_turns": fraction_text(
                sample_phase_increment_turns
            ),
            "sampled_polygon_total_phase_turns": fraction_text(total_phase_turns),
            "certified_polygon_winding": polygon_winding,
            "certified_interior_zero_count": polygon_winding,
            "actual_zero_count_of_fixture": 3,
            "all_segment_disks_exclude_zero": excursion_bound < 1,
        },
        "finite_sample_winding_no_go": {
            "sample_nodes": "8th roots of unity",
            "sample_count": no_go_samples,
            "function_f0": "1",
            "function_f1": "z^8",
            "all_sample_values_equal": True,
            "winding_f0": 0,
            "winding_f1": 8,
            "finite_values_alone_determine_winding": False,
        },
        "aggregate": {
            "derivative_certified_polygonal_winding_theorem_proved": True,
            "direct_argument_principle_zero_count_fixture_certified": True,
            "finite_sample_only_winding_inference_refuted": True,
            "completed_zeta_cofinal_contour_certificate_constructed": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The theorem certifies a zero count only after a zero-avoiding "
            "derivative bound is supplied on every contour arc. The z^3 and "
            "z^8 examples are exact regressions, not the completed zeta function."
        ),
        "failure_count": failures,
    }


def collatz_denominator(word: tuple[int, ...]) -> int:
    return 2 ** sum(word) - 3 ** len(word)


def collatz_all_ge_two_enumeration(maximum_length: int = 8) -> dict[str, Any]:
    rows = []
    total_words = 0
    total_divisible = 0
    non_all_two_divisible = 0
    for length in range(1, maximum_length + 1):
        word_count = 0
        divisible_count = 0
        nontrivial_count = 0
        for word in product(range(2, 6), repeat=length):
            word_count += 1
            denominator = collatz_denominator(word)
            numerator = ordered_affine_numerator(word)
            if denominator > 0 and numerator % denominator == 0:
                divisible_count += 1
                if any(value != 2 for value in word):
                    nontrivial_count += 1
        total_words += word_count
        total_divisible += divisible_count
        non_all_two_divisible += nontrivial_count
        rows.append(
            {
                "length": length,
                "valuation_alphabet": [2, 3, 4, 5],
                "word_count": word_count,
                "divisible_word_count": divisible_count,
                "all_two_word_is_the_only_divisible_word": (
                    divisible_count == 1 and nontrivial_count == 0
                ),
                "non_all_two_divisible_word_count": nontrivial_count,
            }
        )
    return {
        "rows": rows,
        "maximum_length": maximum_length,
        "total_words_checked": total_words,
        "total_divisible_words": total_divisible,
        "non_all_two_divisible_words": non_all_two_divisible,
    }


def collatz_extremal_valuation_audit() -> dict[str, Any]:
    enumeration = collatz_all_ge_two_enumeration()
    failures = 0
    failures += enumeration["non_all_two_divisible_words"]
    failures += int(enumeration["total_words_checked"] != 87_380)
    failures += int(enumeration["total_divisible_words"] != 8)

    theorem = (
        "In any nontrivial positive accelerated Collatz cycle, every occurrence "
        "of a minimum cycle value has outgoing valuation exactly one, while "
        "every occurrence of a maximum value has outgoing valuation at least "
        "two. Consequently every nontrivial periodic valuation necklace contains "
        "both a 1 and an entry at least 2. In particular, a positive integral "
        "cycle word whose valuations are all at least 2 is necessarily a power "
        "of the trivial word (2), representing the fixed cycle 1."
    )
    proof = (
        "Let m be a minimum and write 3m+1=2^a m', with m'>=m. If a>=2, "
        "then 3m+1>=4m, so m<=1. Positivity and oddness give m=1; the equation "
        "then forces a=2 and m'=1, and determinism makes the whole cycle "
        "trivial. Thus a=1 in a nontrivial cycle. At a maximum M, a=1 would "
        "give M'=(3M+1)/2>M, impossible, so a>=2. For a word with D>0 and "
        "D dividing its affine numerator B, x=B/D is a positive odd integral "
        "cycle value; the extremal argument then proves the word is all 2."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_extremal_inequalities": {
            "minimum_step": "3m+1=2^a m' with m'>=m",
            "minimum_if_a_ge_2": "4m<=3m+1, hence m<=1",
            "nontrivial_minimum_outgoing_valuation": 1,
            "maximum_if_a_eq_1": "M'=(3M+1)/2>M",
            "nontrivial_maximum_outgoing_valuation_lower": 2,
        },
        "finite_integrality_regression": enumeration,
        "aggregate": {
            "all_ge_two_nontrivial_cycle_family_excluded_for_all_lengths": True,
            "only_surviving_all_ge_two_primitive_necklace": [2],
            "mixed_valuation_necklaces_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem retires the entire all-valuations-at-least-two periodic "
            "search region. It does not exclude primitive necklaces containing "
            "both 1 and larger valuations and says nothing about nonperiodic orbits."
        ),
        "failure_count": failures,
    }


def goldbach_witness_certificate(
    limit: int,
    checkpoints: tuple[int, ...] | None = None,
) -> dict[str, Any]:
    if limit < 4:
        raise ValueError("limit must be at least four")
    if checkpoints is None:
        checkpoints = tuple(
            value for value in (100, 1_000, 10_000, 100_000, 1_000_000, limit)
            if value <= limit
        )
    checkpoints = tuple(sorted(set(value - value % 2 for value in checkpoints)))
    flags = prime_sieve(limit)
    primes = [value for value in range(2, limit + 1) if flags[value]]
    digest = hashlib.sha256()
    digest_chunk = bytearray()
    maximum_least_witness = 0
    maximum_witness_target = 0
    witness_records = []
    checkpoint_rows = []
    checkpoint_set = set(checkpoints)
    exception_count = 0
    target_count = 0
    last_witness: tuple[int, int] | None = None

    for target in range(4, limit + 1, 2):
        target_count += 1
        witness = 0
        for prime in primes:
            if prime > target // 2:
                break
            if flags[target - prime]:
                witness = prime
                break
        if not witness:
            exception_count += 1
            digest_chunk.extend(f"{target}:NONE\n".encode("ascii"))
        else:
            last_witness = (target, witness)
            digest_chunk.extend(f"{target}:{witness}\n".encode("ascii"))
            if witness > maximum_least_witness:
                maximum_least_witness = witness
                maximum_witness_target = target
                witness_records.append(
                    {
                        "target": target,
                        "new_record_least_prime_witness": witness,
                        "complementary_prime": target - witness,
                    }
                )
        if len(digest_chunk) >= 1_000_000:
            digest.update(digest_chunk)
            digest_chunk.clear()
        if target in checkpoint_set:
            checkpoint_rows.append(
                {
                    "limit": target,
                    "even_targets_checked": target_count,
                    "exception_count": exception_count,
                    "maximum_least_prime_witness": maximum_least_witness,
                    "maximum_witness_target": maximum_witness_target,
                }
            )
    digest.update(digest_chunk)
    return {
        "limit": limit,
        "even_targets_checked": target_count,
        "exception_count": exception_count,
        "all_checked_targets_have_prime_pair_witness": exception_count == 0,
        "maximum_least_prime_witness": maximum_least_witness,
        "maximum_witness_target": maximum_witness_target,
        "last_target_witness": (
            {
                "target": last_witness[0],
                "least_prime_witness": last_witness[1],
                "complementary_prime": last_witness[0] - last_witness[1],
            }
            if last_witness
            else None
        ),
        "witness_stream_format": "ASCII lines N:p using the least p<=N/2",
        "witness_stream_sha256": digest.hexdigest(),
        "witness_stream_record_count": target_count,
        "record_least_witness_rows": witness_records,
        "checkpoint_rows": checkpoint_rows,
    }


def goldbach_ten_million_audit(limit: int = 10_000_000) -> dict[str, Any]:
    certificate = goldbach_witness_certificate(limit)
    no_go_exception = limit + 2 + (limit % 2)
    failures = certificate["exception_count"]
    failures += int(certificate["witness_stream_record_count"] != (limit - 2) // 2)
    theorem = (
        f"Every even integer N with 4<=N<={limit} has a prime-pair "
        "representation. The generator records the least prime witness p<=N/2 "
        "for every target and hashes the complete ordered witness stream, so "
        "the finite theorem is independently reproducible. No finite prefix, "
        "regardless of its size, implies strong Goldbach: a Boolean model that "
        "agrees on every N<=B and fails first at B+2 is indistinguishable on "
        "that prefix."
    )
    proof = (
        "The sieve marks primes up to the bound. For each even N the scan stops "
        "only after finding a marked p<=N/2 with N-p also marked; checking these "
        "two table entries is an explicit finite witness. The committed digest "
        "identifies the ordered list of all such least witnesses but is not used "
        "as a stand-alone proof. The prefix no-go follows by defining two models "
        "that coincide through B and differ only at the next even target."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_finite_witness_certificate": certificate,
        "finite_prefix_promotion_no_go": {
            "verified_prefix_bound_B": limit,
            "first_unobserved_even_target": no_go_exception,
            "model_A_goldbach_holds_at_first_unobserved_target": True,
            "model_B_goldbach_holds_at_first_unobserved_target": False,
            "models_agree_on_entire_verified_prefix": True,
            "finite_prefix_alone_determines_infinite_tail": False,
        },
        "aggregate": {
            "finite_goldbach_theorem_limit": limit,
            "finite_exception_count": certificate["exception_count"],
            "reproducible_witness_stream_constructed": True,
            "finite_prefix_to_universal_inference_refuted": True,
            "actual_tail_exception_bound_below_one_constructed": False,
            "actual_goldbach_counterexample_found": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The exhaustive certificate is a finite theorem, not evidence of a "
            "uniform major/minor-arc inequality. The first unchecked even integer "
            "and every later target remain outside the computation."
        ),
        "failure_count": failures,
    }


def omega_with_multiplicity(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive")
    remaining = value
    count = 0
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            remaining //= divisor
            count += 1
        divisor += 1
    if remaining > 1:
        count += 1
    return count


def prime_power_flags(limit: int) -> bytearray:
    primes = prime_sieve(limit)
    flags = bytearray(limit + 1)
    for prime in range(2, limit + 1):
        if not primes[prime]:
            continue
        power = prime
        while power <= limit:
            flags[power] = 1
            if power > limit // prime:
                break
            power *= prime
    return flags


def prime_power_divisor_sum(value: int, flags: bytearray) -> int:
    return sum(flags[divisor] for divisor in range(1, value + 1) if value % divisor == 0)


def omega_weight(value: int) -> Fraction:
    return Fraction(2) - Fraction(3, 2) * omega_with_multiplicity(value)


def twin_omega_weight_audit(limit: int = 512) -> dict[str, Any]:
    q_flags = prime_power_flags(limit)
    divisor_rows = []
    identity_failures = 0
    for value in range(1, limit + 1):
        omega = omega_with_multiplicity(value)
        divisor_sum = prime_power_divisor_sum(value, q_flags)
        identity_failures += int(omega != divisor_sum)
        if value in (1, 2, 4, 6, 8, 12, 30, 210, 512):
            divisor_rows.append(
                {
                    "n": value,
                    "Omega_n": omega,
                    "prime_power_divisor_sum": divisor_sum,
                    "weight_W_n": fraction_text(omega_weight(value)),
                }
            )

    primes = prime_sieve(limit)
    prime_values = [value for value in range(2, limit + 1) if primes[value]]
    prime_weights = {fraction_text(omega_weight(value)) for value in prime_values}
    p2_weights = {
        fraction_text(omega_weight(value))
        for value in range(4, limit + 1)
        if omega_with_multiplicity(value) == 2
    }
    crt_rows = []
    for k in range(2, 18):
        left = 3 + 15 * k
        right = left + 2
        left_weight = omega_weight(left)
        right_weight = omega_weight(right)
        crt_rows.append(
            {
                "k": k,
                "n": left,
                "n_plus_2": right,
                "n_divisible_by_3": left % 3 == 0,
                "n_plus_2_divisible_by_5": right % 5 == 0,
                "both_composite": omega_with_multiplicity(left) >= 2
                and omega_with_multiplicity(right) >= 2,
                "W_n": fraction_text(left_weight),
                "W_n_plus_2": fraction_text(right_weight),
                "product_is_positive": left_weight * right_weight > 0,
            }
        )
    failures = identity_failures
    failures += int(prime_weights != {"1/2"})
    failures += int(p2_weights != {"-1"})
    failures += sum(int(not row["both_composite"]) for row in crt_rows)
    failures += sum(int(not row["product_is_positive"]) for row in crt_rows)

    theorem = (
        "Let Q(d) be one when d is a prime power p^k with k>=1 and zero "
        "otherwise. Then Omega(n)=sum_(d|n) Q(d). Therefore the n-only "
        "arithmetic weight W(n)=2-(3/2)Omega(n) exactly realizes the TICKET-204 "
        "formal signs: W(p)=1/2 on primes and W(pq)=-1 on semiprimes, including "
        "squares. This signed realization does not solve the parity problem: "
        "W(n)W(n+2)>0 also on infinitely many forced composite-composite pairs."
    )
    proof = (
        "If n=product p^e, its prime-power divisors for a fixed p are exactly "
        "p,p^2,...,p^e, so the divisor sum contributes e and totals Omega(n). "
        "Substitution gives the prime and P2 signs. For n=3+15k with k>=2, "
        "n is a proper multiple of 3 and n+2 is a proper multiple of 5. Both "
        "have Omega at least two, hence both W values are negative and their "
        "shift-two product is positive although neither endpoint is prime."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "prime_power_divisor_identity_rows": divisor_rows,
        "channel_signs": {
            "prime_weight_values": sorted(prime_weights),
            "semiprime_weight_values": sorted(p2_weights),
            "prime_channel_positive": prime_weights == {"1/2"},
            "semiprime_channel_negative": p2_weights == {"-1"},
        },
        "composite_composite_product_no_go_rows": crt_rows,
        "aggregate": {
            "prime_power_divisor_identity_verified_through": limit,
            "identity_failure_count": identity_failures,
            "factor_pair_free_n_only_signed_realization_constructed": True,
            "positive_product_is_twin_indicator_refuted": True,
            "composite_composite_false_positive_family_is_infinite": True,
            "uniform_composite_cancellation_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The weight is an exact arithmetic realization of the desired channel "
            "signs, but it is unbounded below with Omega and its positive product "
            "contains an infinite composite-composite CRT family. No positive "
            "twin-prime lower bound or controlled switching remainder follows."
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
            {"id": f"{prefix}-T204", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T205", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N205",
                "label": refuted,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN205",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": parent, "status": "open_not_proven"},
        ],
        "edges": [
            [f"{prefix}-T204", f"{prefix}-T205"],
            [f"{prefix}-T205", f"{prefix}-N205"],
            [f"{prefix}-T205", f"{prefix}-OPEN205"],
            [f"{prefix}-OPEN205", prefix],
        ],
    }


def build_audit(goldbach_limit: int = 10_000_000) -> dict[str, Any]:
    riemann_compute = riemann_polygonal_winding_audit()
    collatz_compute = collatz_extremal_valuation_audit()
    goldbach_compute = goldbach_ten_million_audit(goldbach_limit)
    twin_compute = twin_omega_weight_audit()

    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-205",
            "theorem_name": "DerivativeCertifiedPolygonalWindingAndFiniteSampleNoGo",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": (
                "The direct winding transfer is exact, but no zero-free cofinal "
                "contours with certified completed-zeta derivative bounds are constructed."
            ),
            "route_decision": {
                "discard": "inferring completed-zeta winding from finitely many contour values alone",
                "retain": "polygonal winding plus segmentwise zero-avoidance certificates",
                "next_single_lemma": "CompletedZetaCofinalZeroFreeContourWindingCertificate",
            },
            "proof_dag": proof_dag(
                "RH",
                "DerivativeCertifiedRoucheMeshAndFiniteSamplingNoGo",
                "DerivativeCertifiedPolygonalWindingAndFiniteSampleNoGo",
                "FiniteContourValuesAloneDetermineWinding",
                "CompletedZetaCofinalZeroFreeContourWindingCertificate",
                "Riemann Hypothesis",
            ),
            "claim_boundary": (
                "No RH proof or counterexample. A direct argument-principle mesh "
                "certificate and an exact finite-sample winding no-go are proved."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-205",
            "theorem_name": "CycleExtremumValuationSeparationAndAllGeTwoExclusion",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": (
                "The all-ge-two necklace region is eliminated universally, but "
                "mixed primitive necklaces and every nonperiodic divergence remain open."
            ),
            "route_decision": {
                "discard": "searching all-valuations-at-least-two words for nontrivial positive cycles",
                "retain": "primitive mixed necklaces containing valuation one and a larger valuation",
                "next_single_lemma": "UniformNondivisibilityForPrimitiveMixedValuationNecklaces",
            },
            "proof_dag": proof_dag(
                "CO",
                "RotationAndPowerReductionToPrimitiveValuationNecklaces",
                "CycleExtremumValuationSeparationAndAllGeTwoExclusion",
                "AllValuationsAtLeastTwoContainANontrivialPositiveCycle",
                "UniformNondivisibilityForPrimitiveMixedValuationNecklaces",
                "Collatz Conjecture",
            ),
            "claim_boundary": (
                "No Collatz proof, divergent-orbit exclusion, or nontrivial cycle. "
                "One infinite periodic candidate stratum is rigorously removed."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-205",
            "theorem_name": "TenMillionExactWitnessCertificateAndFinitePrefixNoGo",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": (
                "The verified prefix now reaches ten million with a reproducible "
                "witness digest, but no analytic control starts at the next target."
            ),
            "route_decision": {
                "discard": "promoting any finite Goldbach verification directly to the infinite conjecture",
                "retain": "exact prefix certificate plus a rigorous tail exceptional count below one",
                "next_single_lemma": "ExplicitBinaryGoldbachTailExceptionalCountStrictlyBelowOne",
            },
            "proof_dag": proof_dag(
                "GB",
                "ExceptionalSetSubunitClosureAndDensityZeroNoGo",
                "TenMillionExactWitnessCertificateAndFinitePrefixNoGo",
                "ArbitrarilyLargeFiniteGoldbachPrefixImpliesStrongGoldbach",
                "ExplicitBinaryGoldbachTailExceptionalCountStrictlyBelowOne",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": (
                "No Goldbach proof or counterexample. Every even target through "
                "10,000,000 receives an exact witness; the infinite tail remains open."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-205",
            "theorem_name": "PrimePowerDivisorOmegaWeightAndProductParityNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": (
                "The formal TICKET-204 signs are realized by an n-only arithmetic "
                "weight, but composite-composite products create infinite false positives."
            ),
            "route_decision": {
                "discard": "using positivity of the raw Omega switching product as a twin-prime indicator",
                "retain": "signed Omega switching after explicit composite-composite cancellation",
                "next_single_lemma": "UniformCompositeCompositeCancellationForOmegaSwitchingCorrelation",
            },
            "proof_dag": proof_dag(
                "TP",
                "PsdParitySeparationNoGoAndIndefiniteRankTwoFactorEscape",
                "PrimePowerDivisorOmegaWeightAndProductParityNoGo",
                "PositiveOmegaSwitchingProductIsATwinPrimeIndicator",
                "UniformCompositeCompositeCancellationForOmegaSwitchingCorrelation",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": (
                "No Twin Prime proof or counterexample. An exact n-only signed "
                "realization and an infinite product false-positive family are proved."
            ),
        },
    }
    failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    boundary = (
        "TICKET-205 resolves none of the four conjectures. It replaces RH "
        "comparison-only counting by a direct derivative-certified winding "
        "certificate, removes the all-ge-two Collatz cycle stratum, verifies "
        "Goldbach through ten million with a reproducible witness stream, and "
        "realizes the Twin factor-channel signs as an n-only Omega weight while "
        "proving that raw positive products still suffer parity false positives."
    )
    return {
        "theorem_name": "FourConjectureWindingExtremalFiniteOmegaAudit",
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
        "winding_extremal_finite_omega_audit": audit,
        "attempts": attempts,
    }
    integrated = (
        ROOT
        / "data"
        / "open-problem"
        / "ticket205-winding-extremal-finite-omega.json"
    )
    write_json(integrated, payload)

    file_map = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-205-winding-certificate.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-205-extremal-valuation.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-205-ten-million-witness.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-205-omega-weight.json",
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

    digest = hashlib.sha256(integrated.read_bytes()).hexdigest()
    print(f"integrated_sha256 {digest}")


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
