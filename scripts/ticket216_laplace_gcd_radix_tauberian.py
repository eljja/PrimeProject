from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, ROUND_CEILING, getcontext
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Any

from ticket214_cofinal_sevenone_exponential_cardinal import goldbach_counts, prime_sieve
from ticket215_lattice_nearcollision_exception_abel import (
    first_positive_single_mountain_m,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket216-laplace-gcd-radix-tauberian.v1"
GENERATED_AT = "2026-08-13T02:00:00+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def proof_dag(
    prefix: str,
    previous: str,
    closed: str,
    rejected: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T215", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T216", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N216",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN216",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T215", f"{prefix}-T216"],
            [f"{prefix}-T216", f"{prefix}-N216"],
            [f"{prefix}-T216", f"{prefix}-OPEN216"],
            [f"{prefix}-OPEN216", prefix],
        ],
    }


def defect_transform(atoms: list[tuple[int, int]], radius: Fraction) -> Fraction:
    return sum(
        (multiplicity * radius**height for height, multiplicity in atoms),
        start=Fraction(0),
    )


def riemann_defect_laplace_audit() -> dict[str, Any]:
    atoms = [(12, 1), (47, 2)]
    radius = Fraction(1, 2)
    transform = defect_transform(atoms, radius)
    rows = []
    failures = 0
    for height in (8, 10, 11, 12, 46, 47):
        threshold = radius**height
        actual_pair_count = sum(
            multiplicity
            for atom_height, multiplicity in atoms
            if atom_height <= height
        )
        certifies_zero = transform < threshold
        rows.append(
            {
                "H": height,
                "transform": str(transform),
                "first_atom_threshold_r_pow_H": str(threshold),
                "certifies_no_offline_pair_through_H": certifies_zero,
                "actual_synthetic_pair_count_through_H": actual_pair_count,
            }
        )
        failures += int(certifies_zero and actual_pair_count != 0)

    epsilon_rows = []
    for denominator_power in (3, 6, 12, 24):
        epsilon = Fraction(1, 10**denominator_power)
        delayed_height = 1
        while radius**delayed_height >= epsilon:
            delayed_height += 1
        atom_value = radius**delayed_height
        epsilon_rows.append(
            {
                "epsilon": str(epsilon),
                "delayed_offline_pair_height": delayed_height,
                "transform_of_one_delayed_pair": str(atom_value),
                "below_epsilon": atom_value < epsilon,
            }
        )
        failures += int(atom_value >= epsilon)

    theorem = (
        "At every boundary-free height let D(T)=N(T)-M(T), and let "
        "C(T)=D(T)/2 count off-critical symmetry pairs with multiplicity. "
        "The Stieltjes measure dC is nonnegative and atomic. For 0<r<1 put "
        "L(r)=integral r^t dC(t). Then C(H) r^H<=L(r). Hence any rigorous "
        "upper bound U(r)<r^H certifies that no off-critical zero has "
        "ordinate at most H. Cofinal certificates with H tending to infinity "
        "imply RH. The threshold is sharp for this information: one pair at "
        "height H contributes exactly r^H."
    )
    proof = (
        "Critical-line zeros increase N and M equally, while each off-line "
        "pair increases N-M by two; therefore C is an integer-valued "
        "nondecreasing step function. Every atom below H has weight at least "
        "r^H, so L(r)>=C(H)r^H. If U(r)<r^H, the integer C(H) is zero. "
        "Applying the certificate at unbounded H excludes every finite "
        "ordinate. Equality for one atom at H proves sharpness. Finally, any "
        "fixed positive tolerance is insufficient globally because a single "
        "atom can be delayed until its weight is below that tolerance."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "defect_pair_measure": "dC=d(N-M)/2",
        "transform": "L(r)=integral r^t dC(t)",
        "synthetic_atoms": [
            {"height": height, "pair_multiplicity": multiplicity}
            for height, multiplicity in atoms
        ],
        "threshold_rows": rows,
        "fixed_tolerance_no_go_rows": epsilon_rows,
        "aggregate": {
            "first_atom_threshold_certificate_proved": True,
            "cofinal_certificates_imply_RH": True,
            "fixed_positive_tolerance_sufficient_for_RH": False,
            "actual_zeta_transform_upper_bounds_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The delayed atoms are logical defect measures, not zeros of the "
            "actual zeta function. They refute fixed-tolerance promotion only."
        ),
        "failure_count": failures,
    }


def collatz_cross_power_gcd_audit(limit_k: int = 4096) -> dict[str, Any]:
    checkpoints = {1, 2, 3, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096}
    rows = []
    failures = 0
    equality_count = 0
    transcript = hashlib.sha256()
    m = 1
    for k in range(1, limit_k + 1):
        m = first_positive_single_mountain_m(k, m)
        delta = 2 ** (k + 2 * m) - 3 ** (k + m)
        left_difference = 3**k - 2**k
        right_difference = 4**m - 3**m
        common_divisor = gcd(left_difference, right_difference)
        gcd_equality = common_divisor == delta
        equality_count += int(gcd_equality)
        failures += int(delta <= 0)
        transcript.update(
            f"{k}:{m}:{delta.bit_length()}:{common_divisor.bit_length()}:"
            f"{int(gcd_equality)}\n".encode("ascii")
        )
        if k in checkpoints:
            rows.append(
                {
                    "valuation_one_count_k": k,
                    "valuation_two_count_m": m,
                    "delta_bit_length": delta.bit_length(),
                    "gcd_bit_length": common_divisor.bit_length(),
                    "delta_equals_cross_power_gcd": gcd_equality,
                    "delta_exceeds_ticket215_ceiling": delta > left_difference,
                }
            )

    failures += int(equality_count != 0)
    theorem = (
        "For a positive accelerated Collatz cycle with cyclic valuation word "
        "1^k 2^m, put Delta=2^(k+2m)-3^(k+m)>0. In addition to the TICKET-215 "
        "near-collision bound, integer closure forces the exact necessary "
        "identity Delta=gcd(3^k-2^k,4^m-3^m). At the unique first-positive "
        "candidate m for each 1<=k<=4096, exact integer arithmetic finds no "
        "gcd equality."
    )
    proof = (
        "TICKET-215 proves that a cycle forces Delta to divide C=3^k-2^k. "
        "Write E=4^m-3^m. The exact identity Delta=2^k E-3^m C shows that "
        "gcd(C,E) divides Delta. Conversely Delta divides C, and the same "
        "identity gives Delta|2^k E. Since Delta is odd, Delta|E. Thus Delta "
        "divides gcd(C,E), proving equality. The audit recomputes the first "
        "positive crossing and the gcd with arbitrary-precision integers."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "necessary_identity": "Delta=gcd(3^k-2^k,4^m-3^m)",
        "audited_k_min": 1,
        "audited_k_max": limit_k,
        "gcd_equality_candidate_count": equality_count,
        "checkpoint_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "cross_power_gcd_identity_proved_as_cycle_necessity": True,
            "gcd_equalities_through_k_4096": equality_count,
            "all_k_gcd_gap_proved": False,
            "multi_run_cycle_words_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The gcd equality is necessary, not sufficient, and the audit is "
            "finite. It covers only one 1-run and one 2-run."
        ),
        "failure_count": failures,
    }


def count_histogram(counts: list[int]) -> list[int]:
    histogram = [0] * (max(counts) + 1)
    for count in counts:
        histogram[count] += 1
    return histogram


def pack_histogram(histogram: list[int], base: int) -> int:
    maximum = len(histogram) - 1
    return sum(
        digit * base ** (maximum - count)
        for count, digit in enumerate(histogram)
    )


def unpack_histogram(packed: int, base: int, maximum: int) -> list[int]:
    reversed_digits = []
    value = packed
    for _ in range(maximum + 1):
        value, digit = divmod(value, base)
        reversed_digits.append(digit)
    if value:
        raise ValueError("packed histogram exceeds declared maximum")
    return list(reversed(reversed_digits))


def packed_digest(packed: int, base: int, maximum: int) -> str:
    length = max(1, (packed.bit_length() + 7) // 8)
    digest = hashlib.sha256()
    digest.update(f"{base}:{maximum}:{length}:".encode("ascii"))
    digest.update(packed.to_bytes(length, "big"))
    return digest.hexdigest()


def goldbach_radix_histogram_audit() -> dict[str, Any]:
    failures = 0
    synthetic_rows = []
    for counts in ([0, 3, 0, 2], [1, 1, 1, 1], [2, 7, 1, 3, 4]):
        values = list(counts)
        base = len(values) + 1
        histogram = count_histogram(values)
        maximum = len(histogram) - 1
        packed = pack_histogram(histogram, base)
        recovered = unpack_histogram(packed, base, maximum)
        selector = sum(
            (Fraction(1, base) ** count for count in values),
            start=Fraction(0),
        )
        failures += int(recovered != histogram)
        failures += int(selector * base**maximum != packed)
        synthetic_rows.append(
            {
                "counts": values,
                "base_b": base,
                "histogram_h_a": histogram,
                "selector": str(selector),
                "packed_integer": packed,
                "decoded_histogram": recovered,
                "exception_digit_h_0": recovered[0],
            }
        )

    starts = (128, 512, 2048, 8192, 32768)
    flags = prime_sieve(2 * max(starts))
    primes = [value for value in range(2, len(flags)) if flags[value]]
    block_rows = []
    for start in starts:
        counts = goldbach_counts(start, flags, primes)
        base = len(counts) + 1
        histogram = count_histogram(counts)
        maximum = len(histogram) - 1
        packed = pack_histogram(histogram, base)
        recovered = unpack_histogram(packed, base, maximum)
        failures += int(recovered != histogram)
        failures += int(recovered[0] != counts.count(0))
        block_rows.append(
            {
                "dyadic_start_X": start,
                "even_targets_B": len(counts),
                "radix_base_b": base,
                "maximum_representation_count_U": maximum,
                "nonzero_histogram_bins": sum(value > 0 for value in histogram),
                "exception_digit_h_0": recovered[0],
                "minimum_positive_representation_count": min(counts),
                "packed_bit_length": packed.bit_length(),
                "packed_sha256": packed_digest(packed, base, maximum),
                "full_histogram_recovered": recovered == histogram,
            }
        )

    precision_rows = []
    base = 3
    for maximum in (8, 16, 32, 64):
        left = [1, maximum]
        right = [1, maximum + 1]
        left_selector = sum(
            (Fraction(1, base) ** count for count in left), start=Fraction(0)
        )
        right_selector = sum(
            (Fraction(1, base) ** count for count in right), start=Fraction(0)
        )
        difference = abs(left_selector - right_selector)
        expected = Fraction(base - 1, base ** (maximum + 1))
        failures += int(difference != expected)
        precision_rows.append(
            {
                "B": 2,
                "base_b": base,
                "left_counts": left,
                "right_counts": right,
                "exact_selector_difference": str(difference),
                "histograms_differ": True,
            }
        )

    theorem = (
        "For a block of B Goldbach counts A_i, set b=B+1 and let h_a be the "
        "number of targets with A_i=a. If U=max A_i, then the TICKET-215 "
        "selector E=sum b^(-A_i) satisfies b^U E=sum_(a=0)^U h_a b^(U-a). "
        "Because 0<=h_a<b, the base-b digits of this integer recover the "
        "entire representation-count histogram exactly, including the "
        "exception count h_0. This is exact encoding, not an arithmetic "
        "estimate of unseen counts."
    )
    proof = (
        "Grouping equal exponents gives E=sum h_a b^(-a). Multiplication by "
        "b^U produces an integer whose base-b digit at place U-a is h_a. "
        "No carry occurs because h_a<=B=b-1, and uniqueness of finite radix "
        "expansions proves exact recovery. The pairs [1,M] and [1,M+1] have "
        "different histograms but selector distance (b-1)/b^(M+1), so "
        "uniform fixed absolute precision cannot recover arbitrarily deep "
        "histogram digits."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "radix_identity": "b^U E=sum_a h_a b^(U-a), b=B+1",
        "synthetic_rows": synthetic_rows,
        "dyadic_goldbach_rows": block_rows,
        "finite_precision_no_go_rows": precision_rows,
        "aggregate": {
            "full_histogram_radix_reconstruction_proved": True,
            "audited_histogram_decode_failures": 0,
            "fixed_precision_sufficient_for_unbounded_histogram_depth": False,
            "uniform_arithmetic_selector_bound_proved": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The selector is a lossless encoding only after the exact counts "
            "and their maximum are already available. It supplies no new "
            "circle-method or parity estimate."
        ),
        "failure_count": failures,
    }


def first_odd_after(value: int) -> int:
    return value + 1 if value % 2 == 0 else value + 2


def geometric_odd_tail(radius: Decimal, after: int) -> Decimal:
    return radius ** first_odd_after(after) / (Decimal(1) - radius * radius)


def twin_tauberian_audit() -> dict[str, Any]:
    getcontext().prec = 80
    maximum_limit = 1_000_000
    flags = prime_sieve(maximum_limit + 2)
    twin_lower = [
        value
        for value in range(3, maximum_limit + 1, 2)
        if flags[value] and flags[value + 2]
    ]
    rows = []
    failures = 0
    for scale in (100, 1000, 10_000, 100_000):
        horizon = min(10 * scale, maximum_limit)
        radius = Decimal(scale - 1) / Decimal(scale)
        known = [value for value in twin_lower if value <= horizon]
        weighted_lower = sum(
            (radius**value for value in known), start=Decimal(0)
        )
        tail = geometric_odd_tail(radius, horizon)
        transferred = max(
            0,
            int((weighted_lower - tail).to_integral_value(rounding=ROUND_CEILING)),
        )
        actual_count = len(known)
        local_count = sum(value <= scale for value in twin_lower)
        lower_factor = radius**scale
        lower_factor_check = lower_factor * Decimal(local_count) <= weighted_lower
        failures += int(not lower_factor_check)
        failures += int(transferred > actual_count)
        rows.append(
            {
                "X": scale,
                "radius_r_X": f"{scale - 1}/{scale}",
                "Y": horizon,
                "known_Abel_lower_decimal": str(weighted_lower),
                "geometric_unknown_tail_upper_decimal": str(tail),
                "transferred_integer_lower_bound_for_T_Y": transferred,
                "actual_bounded_twin_count_T_Y": actual_count,
                "local_count_T_X": local_count,
                "r_X_pow_X_decimal": str(lower_factor),
                "lower_factor_inequality_holds": lower_factor_check,
            }
        )

    scale_rows = []
    for scale in (1000, 10_000, 100_000, 1_000_000):
        radius = Decimal(scale - 1) / Decimal(scale)
        expected_scale = Decimal(scale) / (Decimal(str(math.log(scale))) ** 2)
        fixed_multiplier = 4
        adaptive_multiplier = math.ceil(2 * math.log(math.log(scale)) + 3)
        fixed_tail = geometric_odd_tail(radius, fixed_multiplier * scale)
        adaptive_tail = geometric_odd_tail(radius, adaptive_multiplier * scale)
        scale_rows.append(
            {
                "X": scale,
                "fixed_multiplier": fixed_multiplier,
                "fixed_tail_over_X_log2X_scale": str(fixed_tail / expected_scale),
                "adaptive_multiplier": adaptive_multiplier,
                "adaptive_tail_over_X_log2X_scale": str(
                    adaptive_tail / expected_scale
                ),
            }
        )
        failures += int(adaptive_tail >= expected_scale)

    theorem = (
        "For any odd-supported sequence 0<=a_n<=1, let T(Y)=sum_(n<=Y)a_n "
        "and F(r)=sum a_n r^n. For 0<r<1 and Y>=X, "
        "r^X T(X)<=F(r)<=T(Y)+r^n0/(1-r^2), where n0 is the first odd "
        "integer above Y. Thus a certified lower bound L<=F(r) gives "
        "T(Y)>=ceil(L-r^n0/(1-r^2)). At r_X=1-1/X, a fixed dilation Y=cX "
        "leaves a tail of order X and cannot by this bracket alone transfer a "
        "Hardy-Littlewood-scale X/log^2 X lower bound. A growing dilation of "
        "about (2 log log X)X removes that geometric obstruction."
    )
    proof = (
        "For n<=X, r^n>=r^X, giving the lower inequality. Terms through Y "
        "are at most T(Y), while replacing every later odd coefficient by "
        "one gives the geometric upper tail r^n0/(1-r^2). Rearrangement and "
        "integrality of T give the transferred lower bound. For r=1-1/X "
        "and Y=cX the tail is asymptotic to (X/2)e^(-c); for fixed c this "
        "dominates X/log^2 X. Taking c=2 log log X+omega(1) makes the tail "
        "little-o of that scale."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "count_transform_bracket": (
            "r^X T(X)<=F(r)<=T(Y)+r^n0/(1-r^2)"
        ),
        "finite_prime_rows": rows,
        "tail_scale_rows": scale_rows,
        "aggregate": {
            "quantitative_Abel_to_count_bracket_proved": True,
            "fixed_dilation_sufficient_at_Hardy_Littlewood_scale": False,
            "adaptive_geometric_tail_schedule_identified": True,
            "parity_breaking_Abel_lower_bound_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The fixed-dilation result is a limitation of this coefficient-one "
            "geometric tail envelope, not a theorem that every Tauberian or "
            "sieve transfer must fail."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_defect_laplace_audit()
    collatz_compute = collatz_cross_power_gcd_audit()
    goldbach_compute = goldbach_radix_histogram_audit()
    twin_compute = twin_tauberian_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-216",
            "theorem_name": "OffLineDefectLaplaceFirstAtomCertificateAndFixedToleranceNoGo",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No rigorous actual-zeta upper bound for the full off-line defect transform is proved on a cofinal height schedule.",
            "route_decision": {
                "discard": "any fixed positive transform tolerance, since one off-line pair can be delayed below it",
                "retain": "cofinal actual-zeta transform upper bounds below the first-atom threshold r^H, with an explicit tail budget",
                "next_single_lemma": "CofinalActualZetaOffLineLaplaceUpperBoundsBelowFirstAtomThreshold",
            },
            "proof_dag": proof_dag(
                "RH",
                "EvenLatticeOneSidedCofinalCertificationAndSharpTwoBarrier",
                "OffLineDefectLaplaceFirstAtomCertificateAndFixedToleranceNoGo",
                "FixedPositiveLaplaceToleranceImpliesRH",
                "CofinalActualZetaOffLineLaplaceUpperBoundsBelowFirstAtomThreshold",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof and no off-line zeta zero. A nonnegative transform certificate is proved only as an interface; the actual-zeta bound is open.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-216",
            "theorem_name": "SingleMountainCrossPowerGCDNecessityAndFiniteDiagonalAudit",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "The strict gcd gap is unproved for every k, and the single-mountain family does not cover multi-run words or divergence.",
            "route_decision": {
                "discard": "treating the finite gcd audit or a necessary gcd equality as a complete Collatz proof",
                "retain": "an all-k strict gap between the first-positive Delta and the cross-power gcd, then a multi-run resultant extension",
                "next_single_lemma": "UniformStrictCrossPowerGCDGapAtEverySingleMountainCrossing",
            },
            "proof_dag": proof_dag(
                "CO",
                "SingleMountainCycleNearCollisionReductionAndFiniteDiagonalAudit",
                "SingleMountainCrossPowerGCDNecessityAndFiniteDiagonalAudit",
                "FiniteCrossPowerGCDAuditProvesCollatz",
                "UniformStrictCrossPowerGCDGapAtEverySingleMountainCrossing",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or divergent orbit. The new gcd identity is a necessary condition for one valuation-word family only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-216",
            "theorem_name": "RadixSelectorFullRepresentationHistogramAndPrecisionDepthNoGo",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "The lossless radix representation begins from exact Goldbach counts and supplies no uniform arithmetic estimate for unseen blocks.",
            "route_decision": {
                "discard": "claiming that lossless histogram encoding or fixed-precision selector values independently prove Goldbach coverage",
                "retain": "an independently certified interval for the radix selector whose leading digit is zero on every dyadic block",
                "next_single_lemma": "ArithmeticRadixSelectorIntervalSeparatesTheZeroDigitOnEveryDyadicBlock",
            },
            "proof_dag": proof_dag(
                "GB",
                "ExponentialSelectorExactExceptionCountAndSharpTemperature",
                "RadixSelectorFullRepresentationHistogramAndPrecisionDepthNoGo",
                "LosslessRadixEncodingAloneProvesCoverage",
                "ArithmeticRadixSelectorIntervalSeparatesTheZeroDigitOnEveryDyadicBlock",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The full finite histogram is encoded exactly, but the required all-block arithmetic interval remains open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-216",
            "theorem_name": "QuantitativeAbelCountBracketAndFixedDilationTailNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No parity-breaking lower bound for the actual twin Abel transform dominates the adaptive geometric tail on an unbounded schedule.",
            "route_decision": {
                "discard": "a fixed-dilation coefficient-one tail bound as a transfer of Hardy-Littlewood-scale Abel mass",
                "retain": "a parity-sensitive Abel lower bound above the tail at a growing roughly 2 log log X dilation",
                "next_single_lemma": "ParityBreakingAbelLowerBoundDominatesAdaptiveGeometricTail",
            },
            "proof_dag": proof_dag(
                "TP",
                "CardinalSelectedAbelBoundaryEquivalenceAndFiniteRadiusNoGo",
                "QuantitativeAbelCountBracketAndFixedDilationTailNoGo",
                "FixedDilationAbelTailTransfersTwinScaleMass",
                "ParityBreakingAbelLowerBoundDominatesAdaptiveGeometricTail",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or last-twin counterexample. The Abel-to-count transfer is quantitative, but its parity-breaking lower input is unproved.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "LaplaceGCDRadixTauberianAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-216 proves four exact partial, reduction, or no-go "
            "theorems and resolves none of the parent conjectures. It adds "
            "an RH first-atom transform certificate, an exact Collatz "
            "cross-power gcd necessity, a lossless Goldbach histogram radix, "
            "and a quantitative Twin Abel-to-count bracket with the correct "
            "growing tail horizon."
        ),
        **sections,
        "cross_problem_synthesis": (
            "All four routes now expose a discrete object hidden behind a "
            "transform: off-line zero pairs, a cross-power gcd collision, "
            "Goldbach count digits, and exact-gap-two support counts. The "
            "remaining work is not decoding; it is an independent arithmetic "
            "bound that crosses the first discrete threshold."
        ),
        "literature_boundary": {
            "riemann": "Platt-Trudgian rigorously verify RH through height 3e12 by interval arithmetic; TICKET-216 neither reproduces nor extends that height.",
            "collatz": "Simons-de Weger use transcendence and Diophantine approximation for m-cycle bounds; the gcd identity here is narrower and carries no priority claim.",
            "goldbach": "Montgomery-Vaughan type exceptional-set theorems do not prove the exceptional set empty; radix decoding is not a circle-method improvement.",
            "twin_prime": "Polymath8 identifies a parity limitation for purely sieve-theoretic bounded-gap methods; the Tauberian bracket supplies no parity-breaking estimate.",
        },
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_limited_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = []
    for section_key, problem_id in (
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin_prime", "twin-prime"),
    ):
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
                "bounded_result": {"audit_ref": "#/laplace_gcd_radix_tauberian_audit"},
            }
        )
    return attempts


def standalone_payload(section: dict[str, Any], problem_id: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "ticket_id": section["ticket_id"],
        "problem_id": problem_id,
        "status": STATUS,
        "theorem_name": section["theorem_name"],
        "declared_proposition": section["declared_proposition"],
        "mathematical_argument": section["mathematical_argument"],
        "reproducible_computation": section["reproducible_computation"],
        "discarded_route": section["route_decision"]["discard"],
        "remaining_gap": section["logical_limit"],
        "candidate_theorem": section["route_decision"]["next_single_lemma"],
        "claim_boundary": section["claim_boundary"],
        "proof_dag": section["proof_dag"],
    }


def write_outputs(audit: dict[str, Any]) -> None:
    integrated = ROOT / "data/open-problem/ticket216-laplace-gcd-radix-tauberian.json"
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "laplace_gcd_radix_tauberian_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-216-defect-laplace.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-216-cross-power-gcd.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-216-radix-histogram.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-216-tauberian-bracket.json",
    }
    problem_ids = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin_prime": "twin-prime",
    }
    for section_key, path in targets.items():
        write_json(path, standalone_payload(audit[section_key], problem_ids[section_key]))


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {
                "schema": SCHEMA,
                "status": STATUS,
                "machine_audit": audit["machine_audit"],
            },
            indent=2,
        )
    )
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
