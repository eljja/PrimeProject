from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket199-symmetric-sampling-two-run-squarefree-filter.v1"
GENERATED_AT = "2026-08-10T03:00:00+09:00"
STATUS = "open_not_proven"
GOLDBACH_LIMIT = 1 << 20
TWIN_LIMIT = 1 << 23

Gaussian = tuple[Fraction, Fraction]


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


def gaussian_payload(value: Gaussian) -> dict[str, str]:
    return {"real": fraction_text(value[0]), "imag": fraction_text(value[1])}


def g_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def g_mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def g_neg(value: Gaussian) -> Gaussian:
    return -value[0], -value[1]


def g_sub(left: Gaussian, right: Gaussian) -> Gaussian:
    return g_add(left, g_neg(right))


def g_conj(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def g_inv(value: Gaussian) -> Gaussian:
    norm = value[0] * value[0] + value[1] * value[1]
    if norm == 0:
        raise ZeroDivisionError("zero Gaussian rational")
    return value[0] / norm, -value[1] / norm


def g_square(value: Gaussian) -> Gaussian:
    return g_mul(value, value)


def boundary_samples(segments: int) -> list[Gaussian]:
    if segments < 1:
        raise ValueError("segments must be positive")
    samples: set[Gaussian] = set()
    for index in range(segments + 1):
        x = Fraction(-3) + Fraction(6 * index, segments)
        samples.add((x, Fraction(1, 3)))
        samples.add((x, Fraction(3)))
    for index in range(1, segments):
        y = Fraction(1, 3) + Fraction(8 * index, 3 * segments)
        samples.add((Fraction(-3), y))
        samples.add((Fraction(3), y))
    return sorted(samples)


def symmetric_t_roots(samples: list[Gaussian]) -> list[Gaussian]:
    roots: set[Gaussian] = set()
    for sample in samples:
        square = g_square(sample)
        roots.add(square)
        roots.add(g_conj(square))
    return sorted(roots)


def polynomial_product_at(value: Gaussian, roots: list[Gaussian]) -> Gaussian:
    result: Gaussian = (Fraction(1), Fraction(0))
    for root in roots:
        result = g_mul(result, g_sub(value, root))
    return result


def rh_sampling_row(segments: int) -> dict[str, Any]:
    samples = boundary_samples(segments)
    roots = symmetric_t_roots(samples)
    root_set = set(roots)
    a: Gaussian = (Fraction(1), Fraction(1))
    a_squared = g_square(a)
    q_at_a = polynomial_product_at(a_squared, roots)
    target = g_neg(g_inv(q_at_a))
    v = target[1] / a_squared[1]
    u = target[0] - v * a_squared[0]
    affine_at_a: Gaussian = g_add((u, Fraction(0)), g_mul((v, Fraction(0)), a_squared))
    g_at_a = g_add((Fraction(1), Fraction(0)), g_mul(q_at_a, affine_at_a))
    sample_match = all(g_square(sample) in root_set for sample in samples)
    max_bits = max(
        abs(value).bit_length()
        for part in q_at_a
        for value in (part.numerator, part.denominator)
    )
    return {
        "segments_per_edge": segments,
        "sample_count_on_D3_plus_boundary": len(samples),
        "symmetric_t_root_count": len(roots),
        "interior_witness_a": gaussian_payload(a),
        "a_squared": gaussian_payload(a_squared),
        "Q_at_a": gaussian_payload(q_at_a),
        "u": fraction_text(u),
        "v": fraction_text(v),
        "all_boundary_samples_match_F_equals_one": sample_match,
        "constructed_G_at_a": gaussian_payload(g_at_a),
        "constructed_off_real_zero_exact": g_at_a == (0, 0),
        "Q_at_a_nonzero": q_at_a != (0, 0),
        "largest_Q_at_a_rational_bit_length": max_bits,
    }


def riemann_finite_sampling_no_go_audit() -> dict[str, Any]:
    rows = [rh_sampling_row(segments) for segments in (2, 4, 8, 16)]
    failures = sum(
        int(
            not row["all_boundary_samples_match_F_equals_one"]
            or not row["constructed_off_real_zero_exact"]
            or not row["Q_at_a_nonzero"]
        )
        for row in rows
    )
    return {
        "theorem": (
            "Let S be any finite subset of the boundary of D_3^+ and close S "
            "under conjugation and sign. Choose an interior a with Im(a^2) != 0 "
            "outside that finite orbit. There is a real even polynomial G such "
            "that G(s)=1 for every sampled s but G(a)=0. Therefore finitely many "
            "boundary values, without interval or derivative control between "
            "samples, cannot certify a zero-free D_3 rectangle or a strict "
            "Rouche margin, even inside the class of real even entire functions."
        ),
        "proof": (
            "Let Q(z)=product_(rho in R)(z^2-rho), where R contains the squared "
            "sample points and their conjugates. Then Q is real and even and "
            "vanishes at every sample. Put w=-1/Q(a). Since 1 and a^2 span C "
            "over R when Im(a^2) is nonzero, unique real u,v satisfy u+v a^2=w. "
            "The polynomial G(z)=1+Q(z)(u+v z^2) matches the zero-free function "
            "F=1 at every sample and obeys G(a)=0."
        ),
        "exact_rational_rows": rows,
        "aggregate": {
            "finite_sample_families_checked": len(rows),
            "largest_boundary_sample_count": rows[-1][
                "sample_count_on_D3_plus_boundary"
            ],
            "all_countermodels_exact": failures == 0,
            "actual_Xi_zero_exhibited": False,
            "interval_Rouche_certificate_refuted": False,
        },
        "no_go_scope": (
            "The construction changes the function and is not a counterexample "
            "to RH or a statement about Xi. It rejects only point-sampling rules "
            "that lack a certified between-sample modulus or derivative bound."
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


def collatz_two_run_word(scale: int) -> tuple[int, ...]:
    if scale < 2:
        raise ValueError("scale must be at least two")
    return (1,) * scale + (2,) * (2 * scale) + (1, 2, 2)


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


def collatz_two_run_row(scale: int) -> dict[str, Any]:
    word = collatz_two_run_word(scale)
    x = 32**scale
    y = 27**scale
    z = 18**scale
    denominator = 32 * x - 27 * y
    numerator_closed = 50 * x + 27 * y - 54 * z
    numerator_direct = ordered_affine_numerator(word)
    residual = 41 * x - 27 * z
    congruence = numerator_closed % denominator == (2 * residual) % denominator
    in_interval = denominator < residual < 2 * denominator
    finite_base_case = scale in (2, 3, 4)
    rotation_audit = cyclic_rotation_affine_audit(word)
    return {
        "scale_k": scale,
        "word": f"1^{scale} 2^{2 * scale} 1 2^2",
        "horizon_h": len(word),
        "valuation_sum_S": sum(word),
        "denominator_D": str(denominator),
        "affine_numerator_B": str(numerator_closed),
        "residual_R": str(residual),
        "direct_numerator_matches_closed_form": numerator_direct == numerator_closed,
        "B_congruent_to_2R_mod_D": congruence,
        "D_less_than_R_less_than_2D": in_interval,
        "finite_base_case_k_2_to_4": finite_base_case,
        "finite_base_residue_R_mod_D": str(residual % denominator)
        if finite_base_case
        else None,
        "affine_divisibility_hit": numerator_closed % denominator == 0,
        **rotation_audit,
        "both_scalar_gates_pass": 2 ** sum(word) > 3 ** len(word)
        and Fraction(2**sum(value == 1 for value in word), 1)
        * Fraction(5, 6) ** len(word)
        > 1,
    }


def collatz_two_run_obstruction_audit() -> dict[str, Any]:
    rows = [collatz_two_run_row(scale) for scale in range(2, 129)]
    failures = sum(
        int(
            not row["direct_numerator_matches_closed_form"]
            or not row["B_congruent_to_2R_mod_D"]
            or row["affine_divisibility_hit"]
            or row["cyclic_rotation_divisibility_hit_count"] != 0
            or not row["rotation_recurrence_holds_exactly"]
            or not row["rotation_cycle_closes"]
            or not row["both_scalar_gates_pass"]
            or (
                row["scale_k"] >= 5
                and not row["D_less_than_R_less_than_2D"]
            )
        )
        for row in rows
    )
    return {
        "theorem": (
            "For every k>=2, the primitive two-run-pair word "
            "w_k=1^k 2^(2k) 1 2^2 and every cyclic rotation pass both scalar "
            "gates but fail the accelerated-Collatz affine divisibility equation."
        ),
        "proof": (
            "Writing x=32^k, y=27^k, z=18^k gives "
            "D=32x-27y and B=50x+27y-54z. Modulo D, B is congruent to "
            "2R with R=41x-27z; D is odd, so D|B iff D|R. For k>=5, "
            "R-D=9(x+3y-3z)>0 and 2D-R=x[23-54(27/32)^k+27(18/32)^k]>0. "
            "The bracket is positive at k=5 and strictly increasing because "
            "its forward difference has the sign of 5(27/32)^k-7(18/32)^k. "
            "Thus D<R<2D. The exact residues for k=2,3,4 are nonzero. "
            "If rot(w) moves the first valuation v to the end, its numerator "
            "B' satisfies 2^v B'=3B+D. Since gcd(6,D)=1, D|B iff D|B'; "
            "iteration proves cyclic-rotation invariance."
        ),
        "closed_form_rows": rows,
        "base_case_residues": {
            str(row["scale_k"]): row["finite_base_residue_R_mod_D"]
            for row in rows[:3]
        },
        "aggregate": {
            "all_scales_k_ge_2_excluded": failures == 0,
            "finite_regression_scale_count": len(rows),
            "largest_checked_scale": rows[-1]["scale_k"],
            "all_cyclic_rotations_excluded_by_invariance": failures == 0,
            "nontrivial_cycle_found": False,
            "all_fixed_run_counts_resolved": False,
        },
        "no_go_scope": (
            "The theorem closes only the explicit r=2 family introduced in "
            "TICKET-198. Other primitive words with two run pairs, every family "
            "with three or more run pairs, and aperiodic trajectories remain open."
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


def squarefree_sieve(limit: int, primes: bytearray) -> bytearray:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if primes[prime]:
            square = prime * prime
            count = (limit - square) // square + 1
            flags[square : limit + 1 : square] = b"\x00" * count
    return flags


def von_mangoldt_support_sieve(limit: int, primes: bytearray) -> bytearray:
    support = bytearray(limit + 1)
    for prime in range(2, limit + 1):
        if not primes[prime]:
            continue
        power = prime
        while power <= limit:
            support[power] = 1
            if power > limit // prime:
                break
            power *= prime
    return support


def prime_projector_audit(
    limit: int, primes: bytearray, squarefree: bytearray, mangoldt: bytearray
) -> dict[str, Any]:
    mismatch_count = 0
    proper_power_leakage = 0
    filtered_support_count = 0
    for value in range(2, limit + 1):
        filtered = bool(squarefree[value] and mangoldt[value])
        mismatch_count += int(filtered != bool(primes[value]))
        filtered_support_count += int(filtered)
        proper_power_leakage += int(filtered and mangoldt[value] and not primes[value])
    return {
        "checked_limit": limit,
        "filtered_support_count": filtered_support_count,
        "prime_count": int(sum(primes[: limit + 1])),
        "support_mismatch_count": mismatch_count,
        "proper_prime_power_leakage_count": proper_power_leakage,
        "exact_prime_projector_on_checked_range": mismatch_count == 0,
    }


def odd_proper_prime_powers(limit: int, primes: bytearray) -> list[int]:
    values: set[int] = set()
    for prime in range(3, math.isqrt(limit) + 1, 2):
        if not primes[prime]:
            continue
        power = prime * prime
        while power <= limit:
            values.add(power)
            if power > limit // prime:
                break
            power *= prime
    return sorted(values)


def first_goldbach_witness(target: int, prime_values: list[int], primes: bytearray) -> tuple[int, int] | None:
    for prime in prime_values:
        if prime > target // 2:
            break
        if primes[target - prime]:
            return prime, target - prime
    return None


def goldbach_squarefree_filter_audit(
    primes: bytearray,
    squarefree: bytearray,
    mangoldt: bytearray,
) -> dict[str, Any]:
    limit = GOLDBACH_LIMIT
    projector = prime_projector_audit(limit, primes, squarefree, mangoldt)
    prime_values = [value for value in range(2, limit + 1) if primes[value]]
    powers = odd_proper_prime_powers(limit, primes)
    collision_targets: set[int] = set()
    for index, left in enumerate(powers):
        for right in powers[index:]:
            target = left + right
            if target > limit:
                break
            collision_targets.add(target)
    witness_map = {
        target: first_goldbach_witness(target, prime_values, primes)
        for target in sorted(collision_targets)
    }
    rows = []
    for cutoff in [1 << exponent for exponent in range(10, 21)]:
        targets = [target for target in collision_targets if target <= cutoff]
        failures = sum(witness_map[target] is None for target in targets)
        rows.append(
            {
                "cutoff_X": cutoff,
                "collision_supported_target_count": len(targets),
                "squarefree_Lambda_detector_positive_count": len(targets) - failures,
                "finite_goldbach_failure_count": failures,
            }
        )
    finite_failures = sum(witness is None for witness in witness_map.values())
    failures = (
        projector["support_mismatch_count"]
        + projector["proper_prime_power_leakage_count"]
        + finite_failures
    )
    return {
        "theorem": (
            "For every n>=1, P(n)=mu(n)^2 Lambda(n) equals log(p) when n=p "
            "is prime and equals zero otherwise. Hence "
            "G(N)=sum_(a+b=N)P(a)P(b) is positive exactly when N is a sum "
            "of two primes. Proper-prime-power collision support disappears "
            "identically from this detector, including N=2p^2."
        ),
        "proof": (
            "Lambda is supported on prime powers p^k. The squarefree factor "
            "mu^2 is one at p and zero at p^k for k>=2; away from prime powers "
            "Lambda is zero. Multiplying proves the projector identity term by "
            "term, and convolution positivity is then equivalent to a prime pair."
        ),
        "projector_audit": projector,
        "collision_supported_rows": rows,
        "aggregate": {
            "finite_limit": limit,
            "proper_prime_power_count": len(powers),
            "collision_supported_target_count": len(collision_targets),
            "finite_collision_target_failure_count": finite_failures,
            "prime_power_collision_removed_algebraically": True,
            "eventual_positive_lower_bound_proved": False,
        },
        "no_go_scope": (
            "The exact filter removes a bookkeeping artifact, not the binary "
            "correlation difficulty. Estimating the mu^2 Lambda convolution "
            "pointwise is essentially the remaining Goldbach problem; the finite "
            "scan supplies no all-N theorem."
        ),
        "failure_count": failures,
    }


def twin_squarefree_detector_audit(
    primes: bytearray,
    squarefree: bytearray,
    mangoldt: bytearray,
) -> dict[str, Any]:
    projector = prime_projector_audit(TWIN_LIMIT, primes, squarefree, mangoldt)
    rows = []
    failures = projector["support_mismatch_count"] + projector[
        "proper_prime_power_leakage_count"
    ]
    for exponent in range(10, 23):
        lower = 1 << exponent
        upper = 2 * lower
        prime_pair_count = 0
        filtered_pair_count = 0
        for value in range(lower, upper):
            prime_pair_count += int(primes[value] and primes[value + 2])
            filtered_pair_count += int(
                mangoldt[value]
                and squarefree[value]
                and mangoldt[value + 2]
                and squarefree[value + 2]
            )
        matches = prime_pair_count == filtered_pair_count
        failures += int(not matches)
        rows.append(
            {
                "block": [lower, upper],
                "prime_pair_count": prime_pair_count,
                "squarefree_Lambda_detector_count": filtered_pair_count,
                "exact_support_match": matches,
                "detector_positive": filtered_pair_count > 0,
            }
        )
    return {
        "theorem": (
            "With P(n)=mu(n)^2 Lambda(n), the localized shift-two detector "
            "T(X)=sum_(X<=n<2X)P(n)P(n+2) is nonnegative, contains no proper "
            "prime-power contribution, and is positive if and only if [X,2X) "
            "contains a twin-prime start. Thus TICKET-198's requested exact "
            "prime-power-free detector exists."
        ),
        "proof": (
            "The same pointwise projector identity P(p)=log p and P(n)=0 for "
            "nonprimes turns every summand into log(p)log(p+2) for a genuine "
            "twin pair and zero otherwise. Nonnegativity makes block positivity "
            "equivalent to at least one pair."
        ),
        "projector_audit": projector,
        "finite_dyadic_rows": rows,
        "aggregate": {
            "finite_block_count": len(rows),
            "largest_block_upper": rows[-1]["block"][1],
            "all_finite_supports_match": all(row["exact_support_match"] for row in rows),
            "prime_power_free_detector_constructed": True,
            "infinitely_many_positive_blocks_proved": False,
        },
        "no_go_scope": (
            "Constructing an exact detector does not prove its positivity on an "
            "unbounded block sequence. The parity-breaking lower bound for this "
            "fixed shift remains precisely the Twin Prime obstruction."
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
            {"id": f"{prefix}-T198", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T199", "label": theorem, "status": "closed"},
            {"id": f"{prefix}-N199", "label": rejected, "status": "refuted_or_limited"},
            {"id": f"{prefix}-OPEN199", "label": next_theorem, "status": "highest_risk_open"},
            {"id": prefix, "label": prefix, "status": "open_not_proven"},
        ],
        "edges": [
            [f"{prefix}-T198", f"{prefix}-T199"],
            [f"{prefix}-T199", f"{prefix}-N199"],
            [f"{prefix}-T199", f"{prefix}-OPEN199"],
            [f"{prefix}-OPEN199", prefix],
        ],
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_finite_sampling_no_go_audit()
    collatz = collatz_two_run_obstruction_audit()
    primes = prime_sieve(TWIN_LIMIT + 2)
    squarefree = squarefree_sieve(TWIN_LIMIT + 2, primes)
    mangoldt = von_mangoldt_support_sieve(TWIN_LIMIT + 2, primes)
    goldbach = goldbach_squarefree_filter_audit(primes, squarefree, mangoldt)
    twin = twin_squarefree_detector_audit(primes, squarefree, mangoldt)
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-199",
            "theorem_name": "FiniteBoundarySamplingNoGoForRealEvenRoucheCertification",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No statement about Xi is proved; a certified interval or derivative-controlled boundary enclosure is still missing.",
            "route_decision": {
                "discard": "using finitely many boundary point evaluations, however dense, as a standalone zero-free or Rouche certificate",
                "retain": "cover the full D3 boundary by intervals and propagate a rigorous derivative or modulus bound between mesh points",
                "next_single_lemma": "IntervalBoundaryMeshWithDerivativeBoundCertifiesStrictRoucheMarginOnD3",
            },
            "proof_dag": proof_dag(
                "RH",
                "StandaloneIntervalXiTaylorDegreeAndRoucheMarginOnD3WithoutImportingFiniteHeightRH",
                "FiniteBoundarySamplingNoGoForRealEvenRoucheCertification",
                "FinitePointSamplesAloneCertifyD3RoucheMargin",
                "IntervalBoundaryMeshWithDerivativeBoundCertifiesStrictRoucheMarginOnD3",
            ),
            "claim_boundary": "No RH proof or counterexample. The exact countermodel concerns finite sample information, not the Riemann Xi function.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-199",
            "theorem_name": "TwoRunPairPrimitiveFamilyAffineDivisibilityObstruction",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Only the explicit TICKET-198 r=2 family is closed; arbitrary two-run-pair words and all larger run counts remain open.",
            "route_decision": {
                "discard": "treating the TICKET-198 r=2 primitive family as a possible positive-cycle family after its exact residual interval is exposed",
                "retain": "extend the residual interval or modular obstruction to the r=3 family and then to arbitrary fixed run count",
                "next_single_lemma": "ThreeRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales",
            },
            "proof_dag": proof_dag(
                "CO",
                "FixedRunCountLeavesInfinitePrimitiveAdmissibleFamilies",
                "TwoRunPairPrimitiveFamilyAffineDivisibilityObstruction",
                "TheExplicitR2PrimitiveFamilyCanRealizeAPositiveCycle",
                "ThreeRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales",
            ),
            "claim_boundary": "No Collatz proof or nontrivial cycle. One explicit infinite primitive family is excluded for every scale by an exact affine argument.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-199",
            "theorem_name": "MobiusSquarefreeLambdaExactGoldbachPrimeProjector",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "The exact prime projector removes prime-power contamination but supplies no pointwise positive lower bound for the binary convolution.",
            "route_decision": {
                "discard": "treating proper-prime-power collision support as an intrinsic exceptional stratum after an exact prime-supported detector is chosen",
                "retain": "estimate the exact mu-squared-Lambda binary convolution pointwise without reintroducing absolute prime-power envelopes",
                "next_single_lemma": "UniformPositiveLowerBoundForMobiusSquarefreeGoldbachCorrelationAtEverySufficientlyLargeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "CollisionFreeGoldbachMarginLeavesLogSquaredExceptionalSet",
                "MobiusSquarefreeLambdaExactGoldbachPrimeProjector",
                "PrimePowerCollisionSupportIsIntrinsicToAnExactGoldbachDetector",
                "UniformPositiveLowerBoundForMobiusSquarefreeGoldbachCorrelationAtEverySufficientlyLargeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The result is an exact reformulation that removes a project-local contamination split, not a new correlation lower bound.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-199",
            "theorem_name": "MobiusSquarefreeLambdaExactTwinPrimeDetector",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "The requested detector is constructed exactly, but no theorem makes it positive on infinitely many blocks.",
            "route_decision": {
                "discard": "continuing to subtract proper-prime-power contamination inside the final localized detector",
                "retain": "prove a parity-breaking positive lower bound directly for the squarefree-Lambda shift-two correlation",
                "next_single_lemma": "ParityBreakingPositiveLowerBoundForMobiusSquarefreeLambdaShiftTwoCorrelationOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "PrimePowerFreeLocalizedTwinDetectorHasPositiveMassOnInfinitelyManyDyadicBlocks",
                "MobiusSquarefreeLambdaExactTwinPrimeDetector",
                "ASeparatePrimePowerContaminationEnvelopeIsNeededInsideTheFinalDetector",
                "ParityBreakingPositiveLowerBoundForMobiusSquarefreeLambdaShiftTwoCorrelationOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. TICKET-199 constructs the exact detector half of the TICKET-198 target and leaves infinitude as an explicit positivity theorem.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureSymmetricSamplingTwoRunSquarefreeFilterAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-199 resolves none of the four conjectures. It proves a finite-boundary-sampling no-go, closes one infinite Collatz family, and constructs exact prime-supported Goldbach and Twin detectors with their positivity obligations left open."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The shared principle is to preserve exactly the information the final claim needs. Point samples lose between-sample analytic control; the Collatz affine residual preserves order information; mu^2 Lambda removes prime-power support exactly before additive or shift-two correlation."
        ),
        "literature_boundary": {
            "riemann": "The interpolation countermodel is elementary and project-local; it does not improve finite-height zero verification or estimate Xi.",
            "collatz": "Parity-vector affine equations and rotation invariance are classical. The all-scale r=2 residual interval is the new project-local subfamily result.",
            "goldbach": "The mu^2 Lambda identity is elementary and not claimed as a novel number-theory theorem. Its role is to correct the project's collision-stratum formulation.",
            "twin_prime": "The exact detector is elementary and does not bypass the classical parity obstruction or improve known bounded-gap results.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "riemann_exact_sampling_countermodel_family_count": len(
                riemann["exact_rational_rows"]
            ),
            "collatz_all_scale_family_obstruction_count": 1,
            "collatz_finite_regression_scale_count": collatz["aggregate"][
                "finite_regression_scale_count"
            ],
            "goldbach_exact_prime_projector_count": 1,
            "goldbach_collision_row_count": len(
                goldbach["collision_supported_rows"]
            ),
            "twin_exact_prime_projector_count": 1,
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
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": section["route_decision"]["next_single_lemma"],
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
        "symmetric_sampling_two_run_squarefree_filter_audit": audit,
        "attempts": attempts,
    }
    integrated = (
        ROOT
        / "data"
        / "open-problem"
        / "ticket199-symmetric-sampling-two-run-squarefree-filter.json"
    )
    write_json(integrated, payload)
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-199-finite-boundary-sampling-no-go.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-199-two-run-pair-obstruction.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-199-squarefree-lambda-filter.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-199-squarefree-lambda-detector.json",
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
            "TICKET-199 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
