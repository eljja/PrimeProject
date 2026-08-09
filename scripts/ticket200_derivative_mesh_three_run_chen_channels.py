from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket200-derivative-mesh-three-run-chen-channels.v1"
GENERATED_AT = "2026-08-10T12:00:00+09:00"
STATUS = "open_not_proven"
GOLDBACH_LIMIT = 1 << 20
TWIN_LIMIT = 1 << 23


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


def boundary_samples(segments: int) -> list[tuple[Fraction, Fraction]]:
    if segments < 1:
        raise ValueError("segments must be positive")
    samples: set[tuple[Fraction, Fraction]] = set()
    for index in range(segments + 1):
        x = Fraction(-3) + Fraction(6 * index, segments)
        samples.add((x, Fraction(1, 3)))
        samples.add((x, Fraction(3)))
    for index in range(1, segments):
        y = Fraction(1, 3) + Fraction(8 * index, 3 * segments)
        samples.add((Fraction(-3), y))
        samples.add((Fraction(3), y))
    return sorted(samples)


def rh_derivative_mesh_row(segments: int) -> dict[str, Any]:
    samples = boundary_samples(segments)
    # Synthetic exact instance on the same D_3^+ boundary used by TICKET-199:
    # P(z)=20+z^2 and R(z)=1/4.  Re(P)=20+x^2-y^2 is positive there.
    node_margins = [
        20 + x * x - y * y - Fraction(1, 4) for x, y in samples
    ]
    minimum_node_margin = min(node_margins)
    maximum_segment_length = max(
        Fraction(6, segments), Fraction(8, 3 * segments)
    )
    nearest_node_radius = maximum_segment_length / 2
    derivative_budget = Fraction(12)
    propagated_clearance = (
        minimum_node_margin - derivative_budget * nearest_node_radius
    )
    return {
        "segments_per_edge": segments,
        "boundary_node_count": len(samples),
        "minimum_certified_node_margin_eta": fraction_text(minimum_node_margin),
        "maximum_segment_length_h": fraction_text(maximum_segment_length),
        "nearest_node_radius_h_over_2": fraction_text(nearest_node_radius),
        "certified_derivative_budget_L": fraction_text(derivative_budget),
        "propagated_strict_clearance_eta_minus_Lh_over_2": fraction_text(
            propagated_clearance
        ),
        "strict_rouche_margin_certified": propagated_clearance > 0,
    }


def riemann_derivative_mesh_audit() -> dict[str, Any]:
    rows = [rh_derivative_mesh_row(segments) for segments in (2, 4, 8, 16)]
    expected = [False, True, True, True]
    failures = sum(
        int(row["strict_rouche_margin_certified"] != wanted)
        for row, wanted in zip(rows, expected, strict=True)
    )
    return {
        "theorem": (
            "Let the polygonal boundary of D_3^+ be partitioned into segments "
            "of length at most h, with both endpoints sampled. If analytic P "
            "and R satisfy |P(s)|-|R(s)|>=eta at every sampled endpoint and "
            "sup_boundary(|P'|+|R'|)<=L, then eta-Lh/2>0 implies |R|<|P| "
            "on the full boundary. Therefore P and P+R have the same number "
            "of zeros in D_3^+, counted with multiplicity."
        ),
        "proof": (
            "Every point z of a boundary segment is within h/2 of one sampled "
            "endpoint s. Integration along that segment gives "
            "|P(z)-P(s)|+|R(z)-R(s)|<=L|z-s|. The reverse triangle "
            "inequality then gives |P(z)|-|R(z)|>=eta-Lh/2>0. Rouche's "
            "theorem supplies the zero-count conclusion."
        ),
        "exact_synthetic_rows": rows,
        "synthetic_instance": {
            "domain": "D_3^+={x+iy:-3<=x<=3, 1/3<=y<=3}",
            "P": "20+z^2",
            "R": "1/4",
            "global_derivative_budget": "12",
            "first_certifying_segments_per_edge": 4,
            "instance_is_Xi": False,
        },
        "aggregate": {
            "mesh_family_count": len(rows),
            "certifying_mesh_count": sum(
                row["strict_rouche_margin_certified"] for row in rows
            ),
            "abstract_derivative_mesh_bridge_proved": failures == 0,
            "actual_Xi_interval_certificate_constructed": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "TICKET-199 already proves that point values alone are insufficient. "
            "TICKET-200 closes the missing propagation implication, but the "
            "displayed exact certificate is synthetic. Floating Xi samples or "
            "non-outward-rounded derivative estimates are not rigorous inputs."
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


def collatz_three_run_word(scale: int) -> tuple[int, ...]:
    if scale < 2:
        raise ValueError("scale must be at least two")
    return (1,) * scale + (2,) * (2 * scale) + (1, 2, 2, 1, 2, 2)


def is_primitive_word(word: tuple[int, ...]) -> bool:
    length = len(word)
    return all(
        word != word[:period] * (length // period)
        for period in range(1, length)
        if length % period == 0
    )


def cyclic_rotation_affine_audit(word: tuple[int, ...]) -> dict[str, Any]:
    denominator = 2 ** sum(word) - 3 ** len(word)
    first_numerator = ordered_affine_numerator(word)
    numerator = first_numerator
    hit_count = 0
    recurrence_holds = True
    for valuation in word:
        hit_count += int(numerator % denominator == 0)
        scaled_next = 3 * numerator + denominator
        power = 2**valuation
        recurrence_holds = recurrence_holds and scaled_next % power == 0
        next_numerator = scaled_next // power
        recurrence_holds = recurrence_holds and (
            power * next_numerator == 3 * numerator + denominator
        )
        numerator = next_numerator
    return {
        "cyclic_rotation_count": len(word),
        "cyclic_rotation_divisibility_hit_count": hit_count,
        "rotation_recurrence_holds_exactly": recurrence_holds,
        "rotation_cycle_closes": numerator == first_numerator,
    }


def collatz_three_run_row(scale: int) -> dict[str, Any]:
    word = collatz_three_run_word(scale)
    x = 32**scale
    y = 27**scale
    z = 18**scale
    denominator = 1024 * x - 729 * y
    numerator_closed = 2086 * x + 729 * y - 1458 * z
    numerator_direct = ordered_affine_numerator(word)
    residual = numerator_closed - 2 * denominator
    base_case = scale < 7
    rotation = cyclic_rotation_affine_audit(word)
    one_count = sum(value == 1 for value in word)
    product_gate = (
        Fraction(2**one_count, 1) * Fraction(5, 6) ** len(word) > 1
    )
    return {
        "scale_k": scale,
        "word": f"1^{scale} 2^{2 * scale} (1 2^2)^2",
        "horizon_h": len(word),
        "valuation_sum_S": sum(word),
        "denominator_D": str(denominator),
        "affine_numerator_B": str(numerator_closed),
        "residual_B_minus_2D": str(residual),
        "direct_numerator_matches_closed_form": numerator_direct
        == numerator_closed,
        "primitive_word": is_primitive_word(word),
        "zero_less_than_B_minus_2D_less_than_D": 0 < residual < denominator,
        "finite_base_case_k_2_to_6": base_case,
        "finite_base_residue_B_mod_D": str(numerator_closed % denominator)
        if base_case
        else None,
        "affine_divisibility_hit": numerator_closed % denominator == 0,
        "contraction_gate_passes": 2 ** sum(word) > 3 ** len(word),
        "product_gate_passes": product_gate,
        **rotation,
    }


def collatz_three_run_obstruction_audit() -> dict[str, Any]:
    rows = [collatz_three_run_row(scale) for scale in range(2, 129)]
    failures = sum(
        int(
            not row["direct_numerator_matches_closed_form"]
            or not row["primitive_word"]
            or row["affine_divisibility_hit"]
            or row["cyclic_rotation_divisibility_hit_count"] != 0
            or not row["rotation_recurrence_holds_exactly"]
            or not row["rotation_cycle_closes"]
            or not row["contraction_gate_passes"]
            or not row["product_gate_passes"]
            or (
                row["scale_k"] >= 7
                and not row["zero_less_than_B_minus_2D_less_than_D"]
            )
            or (
                row["scale_k"] < 7
                and row["finite_base_residue_B_mod_D"] == "0"
            )
        )
        for row in rows
    )
    return {
        "theorem": (
            "For every k>=2, the primitive three-run-pair word "
            "w_k=1^k 2^(2k)(1 2^2)^2 and every cyclic rotation pass both "
            "scalar gates but fail the accelerated-Collatz affine divisibility "
            "equation. Hence this entire explicit infinite family contains no "
            "positive cycle code."
        ),
        "proof": (
            "Put x=32^k, y=27^k, z=18^k. Concatenation with (122)^2, whose "
            "ordered numerator is 1357, gives D=1024x-729y and "
            "B=2086x+729y-1458z. For k>=7, R=B-2D="
            "38x+2187y-1458z is positive, while D-R="
            "986x-2916y+1458z is positive at k=7 and increases after division "
            "by x because its forward difference has the sign of "
            "10(27/32)^k-14(18/32)^k>0. Thus 2D<B<3D. The exact residues "
            "for k=2,...,6 are nonzero. The unique run 2^(2k), of length at "
            "least four, proves primitivity. Finally 2^v B'=3B+D under one "
            "cyclic rotation and gcd(6,D)=1, so divisibility is rotation invariant."
        ),
        "tail_block_ordered_numerator": 1357,
        "closed_form_rows": rows,
        "base_case_residues": {
            str(row["scale_k"]): row["finite_base_residue_B_mod_D"]
            for row in rows[:5]
        },
        "aggregate": {
            "all_scales_k_ge_2_excluded": failures == 0,
            "finite_regression_scale_count": len(rows),
            "largest_checked_scale": rows[-1]["scale_k"],
            "all_cyclic_rotations_excluded": failures == 0,
            "explicit_run_pair_count_closed": 3,
            "all_fixed_run_counts_resolved": False,
            "nontrivial_cycle_found": False,
        },
        "no_go_scope": (
            "The theorem closes the r=3 member of one structured family, not "
            "all three-run-pair words, arbitrary fixed run count, nonperiodic "
            "divergence, or the Collatz conjecture."
        ),
        "failure_count": failures,
    }


def prime_sieve(limit: int) -> bytearray:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            start = prime * prime
            count = (limit - start) // prime + 1
            flags[start : limit + 1 : prime] = b"\x00" * count
    return flags


def semiprime_sieve(limit: int, prime_values: list[int]) -> bytearray:
    flags = bytearray(limit + 1)
    for index, left in enumerate(prime_values):
        if left * left > limit:
            break
        for right in prime_values[index:]:
            value = left * right
            if value > limit:
                break
            flags[value] = 1
    return flags


def first_prime_channel_witness(
    target: int,
    prime_values: list[int],
    right_support: bytearray,
) -> tuple[int, int] | None:
    for prime in prime_values:
        if prime >= target:
            break
        right = target - prime
        if right < len(right_support) and right_support[right]:
            return prime, right
    return None


def goldbach_chen_channel_audit(
    primes: bytearray,
    prime_values: list[int],
    semiprimes: bytearray,
) -> dict[str, Any]:
    cutoffs = {1 << exponent for exponent in range(10, 21)}
    rows = []
    counts = {
        "even_targets": 0,
        "goldbach_positive": 0,
        "composite_semiprime_channel_positive": 0,
        "chen_positive": 0,
        "semiprime_only": 0,
        "chen_failure": 0,
    }
    selected_witnesses: dict[str, dict[str, list[int] | None]] = {}
    for target in range(4, GOLDBACH_LIMIT + 1, 2):
        prime_witness = first_prime_channel_witness(target, prime_values, primes)
        semiprime_witness = first_prime_channel_witness(
            target, prime_values, semiprimes
        )
        prime_hit = prime_witness is not None
        semiprime_hit = semiprime_witness is not None
        chen_hit = prime_hit or semiprime_hit
        counts["even_targets"] += 1
        counts["goldbach_positive"] += int(prime_hit)
        counts["composite_semiprime_channel_positive"] += int(semiprime_hit)
        counts["chen_positive"] += int(chen_hit)
        counts["semiprime_only"] += int(semiprime_hit and not prime_hit)
        counts["chen_failure"] += int(not chen_hit)
        if target in (4, 28, 100, 1024, GOLDBACH_LIMIT):
            selected_witnesses[str(target)] = {
                "prime_prime": list(prime_witness) if prime_witness else None,
                "prime_composite_semiprime": list(semiprime_witness)
                if semiprime_witness
                else None,
            }
        if target in cutoffs:
            rows.append({"cutoff_X": target, **counts})
    failures = counts["chen_failure"] + counts["semiprime_only"]
    return {
        "theorem": (
            "Let I_P be the prime indicator and I_2 the indicator of composite "
            "integers with exactly two prime factors counted with multiplicity. "
            "For even N define R(N)=sum I_P(a)I_P(N-a), "
            "S(N)=sum I_P(a)I_2(N-a), and C(N)=R(N)+S(N). This is a "
            "disjoint exact channel decomposition. Bordignon's explicit Chen "
            "theorem gives C(N)>0 for every even N>exp(36). Consequently every "
            "Goldbach counterexample above exp(36), if one exists, must satisfy "
            "R(N)=0<S(N): it is a semiprime-only Chen target."
        ),
        "proof": (
            "A number that is a product of at most two primes is either prime "
            "or a composite semiprime, and the two supports are disjoint. "
            "Splitting Chen's representation count by this dichotomy proves "
            "C=R+S. The imported explicit theorem supplies C(N)>0; if R(N)=0, "
            "then necessarily S(N)>0. No estimate here proves R(N)>0."
        ),
        "imported_theorem": {
            "author": "Matteo Bordignon",
            "title": "An explicit version of Chen's theorem",
            "published": 2022,
            "doi": "10.1017/S0004972721001301",
            "url": "https://doi.org/10.1017/S0004972721001301",
            "statement_used": "Every even N>exp(36) is a prime plus a product of at most two primes.",
            "proved_inside_primeproject": False,
        },
        "finite_channel_rows": rows,
        "selected_witnesses": selected_witnesses,
        "logical_countermodel": {
            "R": 0,
            "S": 1,
            "C": 1,
            "meaning": "C>0 and C=R+S do not logically imply R>0.",
            "is_an_arithmetic_goldbach_counterexample": False,
        },
        "aggregate": {
            "finite_limit": GOLDBACH_LIMIT,
            "finite_even_target_count": counts["even_targets"],
            "finite_goldbach_failure_count": counts["even_targets"]
            - counts["goldbach_positive"],
            "finite_semiprime_only_target_count": counts["semiprime_only"],
            "chen_channel_decomposition_exact": True,
            "explicit_chen_threshold": "exp(36)",
            "semiprime_only_channel_eliminated_above_threshold": False,
            "goldbach_resolved": False,
        },
        "no_go_scope": (
            "Chen positivity alone cannot imply Goldbach positivity because the "
            "composite-semiprime channel can carry all of C in the exact "
            "decomposition. The finite zero count for semiprime-only targets is "
            "a regression result, not a proof that this channel is globally empty."
        ),
        "failure_count": failures,
    }


def twin_chen_channel_audit(
    primes: bytearray,
    semiprimes: bytearray,
) -> dict[str, Any]:
    rows = []
    failures = 0
    for exponent in range(10, 23):
        lower = 1 << exponent
        upper = 2 * lower
        twin_count = 0
        semiprime_count = 0
        for value in range(lower, upper):
            if not primes[value]:
                continue
            twin_count += int(primes[value + 2])
            semiprime_count += int(semiprimes[value + 2])
        chen_count = twin_count + semiprime_count
        decomposition_exact = all(
            not (primes[value + 2] and semiprimes[value + 2])
            for value in range(lower, upper)
            if primes[value]
        )
        failures += int(not decomposition_exact)
        rows.append(
            {
                "block": [lower, upper],
                "twin_prime_channel_count": twin_count,
                "prime_composite_semiprime_channel_count": semiprime_count,
                "chen_channel_count": chen_count,
                "channel_decomposition_exact": decomposition_exact,
                "chen_channel_positive": chen_count > 0,
                "twin_channel_positive": twin_count > 0,
            }
        )
    return {
        "theorem": (
            "For a dyadic block [X,2X), let T_0(X) count primes p for which "
            "p+2 is prime, let S_2(X) count primes p for which p+2 is a "
            "composite semiprime, and let C_2(X)=T_0(X)+S_2(X). The supports "
            "are disjoint. Chen's theorem implies C_2(X)>0 for infinitely many "
            "dyadic X. The TICKET-199 weighted detector is positive exactly "
            "when T_0(X)>0, so the unresolved step is to keep the semiprime "
            "channel from exhausting Chen's infinitely many positive blocks."
        ),
        "proof": (
            "Every Chen prime p has p+2 either prime or composite semiprime, "
            "giving the disjoint identity C_2=T_0+S_2. Infinitely many Chen "
            "primes are unbounded and therefore occupy infinitely many dyadic "
            "blocks. The squarefree-Lambda detector of TICKET-199 has exactly "
            "the twin-prime support, hence its positivity is equivalent to "
            "T_0>0, not merely C_2>0."
        ),
        "imported_theorem": {
            "author": "Jing-Run Chen",
            "title": "On the representation of a large even integer as the sum of a prime and the product of at most two primes",
            "published": 1973,
            "doi": "10.1360/YA1973-16-2-157",
            "url": "https://doi.org/10.1360/YA1973-16-2-157",
            "statement_used": "There are infinitely many primes p for which p+2 has at most two prime factors.",
            "proved_inside_primeproject": False,
        },
        "finite_dyadic_rows": rows,
        "logical_countermodel": {
            "T_0": 0,
            "S_2": 1,
            "C_2": 1,
            "meaning": "C_2>0 and C_2=T_0+S_2 do not logically imply T_0>0.",
            "is_a_twin_prime_counterexample": False,
        },
        "aggregate": {
            "finite_block_count": len(rows),
            "largest_block_upper": rows[-1]["block"][1],
            "all_finite_channel_decompositions_exact": failures == 0,
            "imported_infinitely_many_chen_positive_blocks": True,
            "infinitely_many_twin_positive_blocks_proved": False,
            "twin_prime_resolved": False,
        },
        "no_go_scope": (
            "The imported theorem reaches prime plus P2, not prime plus prime. "
            "The exact decomposition isolates rather than crosses the sieve "
            "parity barrier; finite positive twin blocks prove no infinitude."
        ),
        "failure_count": failures,
    }


def proof_dag(
    prefix: str,
    previous: str,
    theorem: str,
    rejected: str,
    next_theorem: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T199", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T200", "label": theorem, "status": "closed"},
            {
                "id": f"{prefix}-N200",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN200",
                "label": next_theorem,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": prefix, "status": "open_not_proven"},
        ],
        "edges": [
            [f"{prefix}-T199", f"{prefix}-T200"],
            [f"{prefix}-T200", f"{prefix}-N200"],
            [f"{prefix}-T200", f"{prefix}-OPEN200"],
            [f"{prefix}-OPEN200", prefix],
        ],
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_derivative_mesh_audit()
    collatz = collatz_three_run_obstruction_audit()
    primes = prime_sieve(TWIN_LIMIT + 2)
    prime_values = [value for value in range(2, TWIN_LIMIT + 3) if primes[value]]
    semiprimes = semiprime_sieve(TWIN_LIMIT + 2, prime_values)
    goldbach = goldbach_chen_channel_audit(primes, prime_values, semiprimes)
    twin = twin_chen_channel_audit(primes, semiprimes)
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-200",
            "theorem_name": "DerivativeControlledBoundaryMeshRoucheCertificate",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "The mesh propagation theorem is exact, but no outward-rounded Xi Taylor remainder and derivative enclosure on D3 has been supplied.",
            "route_decision": {
                "discard": "treating high-precision Xi point samples or non-rigorous numerical derivatives as a Rouché certificate",
                "retain": "instantiate the proved mesh implication with outward-rounded interval bounds for Xi, a Taylor polynomial, its remainder, and their derivatives",
                "next_single_lemma": "OutwardRoundedXiTaylorRemainderAndDerivativeBoundsInstantiateD3MeshCertificate",
            },
            "proof_dag": proof_dag(
                "RH",
                "FiniteBoundarySamplingNoGoForRealEvenRoucheCertification",
                "DerivativeControlledBoundaryMeshRoucheCertificate",
                "FloatingPointXiMarginsWithoutOutwardRoundedDerivativeAndTailBoundsAreProofCertificates",
                "OutwardRoundedXiTaylorRemainderAndDerivativeBoundsInstantiateD3MeshCertificate",
            ),
            "claim_boundary": "No RH proof or counterexample. The exact theorem closes only the finite-mesh propagation logic; its Xi-specific interval hypotheses remain unproved.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-200",
            "theorem_name": "ThreeRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "One structured r=3 family is excluded; arbitrary three-run words, all run counts, and divergent trajectories remain open.",
            "route_decision": {
                "discard": "retaining the explicit TICKET-198 r=3 family as a positive-cycle candidate after its exact residual interval is proved",
                "retain": "derive the corresponding closed form for r=4 and seek a residual argument uniform in the run-pair count r",
                "next_single_lemma": "FourRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales",
            },
            "proof_dag": proof_dag(
                "CO",
                "TwoRunPairPrimitiveFamilyAffineDivisibilityObstruction",
                "ThreeRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales",
                "TheExplicitR3PrimitiveFamilyCanRealizeAPositiveCycle",
                "FourRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales",
            ),
            "claim_boundary": "No Collatz proof or nontrivial cycle. TICKET-200 excludes every scale and cyclic rotation of one explicit primitive three-run-pair family.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-200",
            "theorem_name": "ChenGoldbachPrimeSemiprimeChannelReduction",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "Chen guarantees prime-plus-P2 representations above exp(36), but no theorem eliminates semiprime-only targets pointwise.",
            "route_decision": {
                "discard": "claiming that Chen positivity or finite zero exceptions automatically imply prime-prime positivity",
                "retain": "bound the composite-semiprime channel sharply enough to prove that it cannot be the sole Chen channel at any sufficiently large even target",
                "next_single_lemma": "SemiprimeOnlyChenGoldbachChannelIsEmptyForEveryEvenNAboveExp36",
            },
            "proof_dag": proof_dag(
                "GB",
                "MobiusSquarefreeLambdaExactGoldbachPrimeProjector",
                "ChenGoldbachPrimeSemiprimeChannelReduction",
                "ChenPrimePlusP2PositivityImpliesGoldbachPrimePlusPrimePositivity",
                "SemiprimeOnlyChenGoldbachChannelIsEmptyForEveryEvenNAboveExp36",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The result imports Chen's theorem and exactly identifies the remaining semiprime-only channel; it does not eliminate that channel.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-200",
            "theorem_name": "ChenTwinPrimeSemiprimeChannelReduction",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "Chen supplies infinitely many prime-plus-P2 starts, but all could lie in the composite-semiprime channel without a parity-breaking theorem.",
            "route_decision": {
                "discard": "identifying infinitely many Chen primes with infinitely many twin primes",
                "retain": "prove that the twin channel, rather than only the composite-semiprime channel, is positive on infinitely many Chen-positive dyadic blocks",
                "next_single_lemma": "TwinChannelPositiveOnInfinitelyManyChenPositiveDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "MobiusSquarefreeLambdaExactTwinPrimeDetector",
                "ChenTwinPrimeSemiprimeChannelReduction",
                "InfinitelyManyChenPrimesImplyInfinitelyManyTwinPrimes",
                "TwinChannelPositiveOnInfinitelyManyChenPositiveDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. The exact Chen-channel split exposes the parity gap but does not cross it.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureDerivativeMeshThreeRunChenChannelAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-200 resolves none of the four conjectures. It proves the "
            "derivative-controlled boundary-mesh implication, closes the explicit "
            "r=3 Collatz family, and reduces the Goldbach and Twin Prime gaps to "
            "precise composite-semiprime channels using Chen's theorems."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common operation is proof-obligation separation: analytic sample "
            "data are separated from between-sample control, Collatz scalar gates "
            "from affine integrality, and prime-plus-P2 positivity from the exact "
            "prime and composite-semiprime channels hidden inside it."
        ),
        "literature_boundary": {
            "riemann": "The propagation lemma is standard analysis specialized to the project domain; no novelty priority or Xi interval computation is claimed. Platt-Trudgian remains the rigorous finite-height reference.",
            "collatz": "Parity-vector affine equations are classical, and 2026 work on Christoffel extremizers is adjacent context. The r=3 residual calculation is a project-local subfamily theorem only.",
            "goldbach": "Bordignon's explicit Chen theorem is imported, not reproved. The channel split is elementary and not claimed as an original Chen-strength result.",
            "twin_prime": "Chen's prime-plus-P2 infinitude is imported. The channel decomposition restates the exact parity gap and proves no new prime-pair lower bound.",
        },
        "sources": [
            {
                "title": "The Riemann hypothesis is true up to 3*10^12",
                "authors": "Dave Platt and Tim Trudgian",
                "url": "https://arxiv.org/abs/2004.09765",
            },
            {
                "title": "Christoffel words as extremal structures in Collatz dynamics",
                "authors": "Carlos Fernandez and Santiago Ibanez",
                "url": "https://arxiv.org/abs/2607.24844",
                "status": "2026 preprint; contextual only",
            },
            {
                "title": "An explicit version of Chen's theorem",
                "authors": "Matteo Bordignon",
                "url": "https://doi.org/10.1017/S0004972721001301",
            },
            {
                "title": "On the representation of a large even integer as the sum of a prime and the product of at most two primes",
                "authors": "Jing-Run Chen",
                "url": "https://doi.org/10.1360/YA1973-16-2-157",
            },
        ],
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "riemann_mesh_family_count": len(riemann["exact_synthetic_rows"]),
            "collatz_all_scale_family_obstruction_count": 1,
            "collatz_finite_regression_scale_count": collatz["aggregate"][
                "finite_regression_scale_count"
            ],
            "goldbach_channel_decomposition_count": 1,
            "goldbach_finite_channel_row_count": len(
                goldbach["finite_channel_rows"]
            ),
            "twin_channel_decomposition_count": 1,
            "twin_finite_dyadic_row_count": len(twin["finite_dyadic_rows"]),
            "rejected_or_limited_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
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
                "status": STATUS,
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
        "derivative_mesh_three_run_chen_channel_audit": audit,
        "attempts": attempts,
    }
    integrated = (
        ROOT
        / "data"
        / "open-problem"
        / "ticket200-derivative-mesh-three-run-chen-channels.json"
    )
    write_json(integrated, payload)
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-200-derivative-mesh-certificate.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-200-three-run-pair-obstruction.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-200-chen-channel-reduction.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-200-chen-channel-reduction.json",
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    for attempt in attempts:
        problem_id = attempt["problem_id"]
        section = audit[section_keys[problem_id]]
        write_json(
            paths[problem_id],
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "ticket_id": section["ticket_id"],
                "problem_id": problem_id,
                "status": STATUS,
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
    digest = hashlib.sha256(integrated.read_bytes()).hexdigest()
    print(f"integrated_sha256 {digest}")


def main() -> None:
    audit = build_audit()
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(
            "TICKET-200 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
