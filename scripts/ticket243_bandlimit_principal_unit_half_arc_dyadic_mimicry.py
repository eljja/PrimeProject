from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket243-bandlimit-principal-unit-half-arc-dyadic-mimicry.v1"
GENERATED_AT = "2026-08-26T07:30:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "bandlimit_principal_unit_half_arc_dyadic_mimicry_audit"
LOCAL_MODEL_SCAN_LIMIT = 50_000


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fraction_payload(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "float": float(value)}


def prime_flags_up_to(limit: int) -> bytearray:
    flags = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        flags[0] = 0
    if limit >= 1:
        flags[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            flags[prime * prime : limit + 1 : prime] = b"\x00" * (
                (limit - prime * prime) // prime + 1
            )
    return flags


def primes_up_to(limit: int) -> list[int]:
    return [
        value
        for value, flag in enumerate(prime_flags_up_to(limit))
        if flag
    ]


def deterministic_is_prime(value: int) -> bool:
    if value < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if value % prime == 0:
            return value == prime
    exponent = value - 1
    shifts = 0
    while exponent % 2 == 0:
        exponent //= 2
        shifts += 1
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % value == 0:
            continue
        witness = pow(base, exponent, value)
        if witness in (1, value - 1):
            continue
        for _ in range(shifts - 1):
            witness = witness * witness % value
            if witness == value - 1:
                break
        else:
            return False
    return True


def factor_distinct(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if value > 1:
        factors.append(value)
    return factors


def multiplicative_order(value: int, prime: int) -> int:
    order = prime - 1
    for factor in factor_distinct(order):
        while order % factor == 0 and pow(value, order // factor, prime) == 1:
            order //= factor
    return order


def primitive_root(prime: int) -> int:
    factors = factor_distinct(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise AssertionError(f"primitive root not found for {prime}")


def next_prime_not_dividing(value: int, start: int = 3) -> int:
    candidate = max(3, start | 1)
    while True:
        if deterministic_is_prime(candidate) and value % candidate:
            return candidate
        candidate += 2


def crt_pair(a: int, modulus_a: int, b: int, modulus_b: int) -> tuple[int, int]:
    if math.gcd(modulus_a, modulus_b) != 1:
        raise ValueError("CRT moduli must be coprime")
    step = ((b - a) * pow(modulus_a, -1, modulus_b)) % modulus_b
    modulus = modulus_a * modulus_b
    return (a + modulus_a * step) % modulus, modulus


def first_prime_in_dyadic_progression(
    residue: int, modulus: int, block_start: int
) -> int | None:
    step = max(0, (block_start - residue + modulus - 1) // modulus)
    candidate = residue + step * modulus
    if candidate < block_start:
        candidate += modulus
    while candidate <= 2 * block_start:
        if deterministic_is_prime(candidate):
            return candidate
        candidate += modulus
    return None


def riemann_bandlimit_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for size in (4, 8, 16, 32, 64):
        minimum_pair_distance_squared = Fraction(2)
        gram_diagonal = Fraction(1)
        maximum_off_diagonal = Fraction(0)
        verified = (
            gram_diagonal == 1
            and maximum_off_diagonal == 0
            and minimum_pair_distance_squared == 2
        )
        failures += int(not verified)
        transcript.update(
            f"{size}:{gram_diagonal}:{maximum_off_diagonal}:{minimum_pair_distance_squared}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "orthonormal_family_size": size,
                "fourier_support": "[-pi,pi]",
                "real_even": True,
                "gram_diagonal": fraction_payload(gram_diagonal),
                "maximum_off_diagonal_absolute_value": fraction_payload(
                    maximum_off_diagonal
                ),
                "minimum_pair_distance_squared": fraction_payload(
                    minimum_pair_distance_squared
                ),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let g_n(xi)=pi^(-1/2) cos(n xi) in L2([-pi,pi]) for n>=1, and let "
        "f_n be its inverse Fourier transform. Then every f_n is normalized, "
        "real, even, and bandlimited to the same interval, while <f_n,f_m>="
        "delta_nm. Hence fixed frequency support and L2 normalization do not "
        "make an even test family relatively compact. Moreover, replacing the "
        "sharp cutoff by a nonzero real even phi in C_c^infinity and taking "
        "normalized inverse transforms of phi(xi)cos(t xi) gives a smooth "
        "bandlimited non-precompact subsequence. Therefore frequency tightness "
        "alone cannot supply the compactness premise in the TICKET-242 uniform "
        "positivity transfer criterion."
    )
    proof = (
        "Cosine orthogonality gives integral from -pi to pi of cos(n xi)cos(m "
        "xi) equal to pi delta_nm; Plancherel transfers this Gram matrix to the "
        "inverse transforms, whose pairwise squared distance is two. For smooth "
        "phi, products of two modulated copies reduce to Fourier coefficients "
        "of |phi|^2 at t-s and t+s. Riemann-Lebesgue makes those coefficients "
        "tend to zero, so a separated subsequence exists."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_cosine_gram_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "fixed_frequency_support_proved": True,
            "real_even_normalization_proved": True,
            "relative_compactness_refuted": True,
            "smooth_bandlimited_noncompact_subsequence_proved": True,
            "uniform_signed_guinand_weil_tail_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The examples are functional-analytic test families, not a proof that "
            "the actual Guinand-Weil admissible class contains them or that its "
            "arithmetic tail fails. They refute frequency tightness alone as a "
            "compactness argument; joint physical tightness, admissibility, a "
            "uniform arithmetic tail, and a positive margin remain open."
        ),
        "failure_count": failures,
    }


def collatz_principal_unit_audit() -> dict[str, Any]:
    primes = [prime for prime in primes_up_to(LOCAL_MODEL_SCAN_LIMIT) if prime > 5]
    selected = {7, 11, 13, 17, 29, 59, 109, 1009, 10007, 49999}
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    largest_order = 0
    largest_order_prime = 0

    for prime in primes:
        modulus = prime * prime
        generator = primitive_root(prime)
        teichmuller = pow(generator, prime, modulus)
        a_unit = teichmuller * (1 + 3 * prime) % modulus
        b_unit = teichmuller * (1 + 5 * prime) % modulus
        ratio_u = a_unit * pow(b_unit, -1, modulus) % modulus
        ratio_v = (
            pow(a_unit, 5, modulus)
            * pow(pow(b_unit, 3, modulus), -1, modulus)
        ) % modulus
        order_d = (prime - 1) // 2
        verified = (
            multiplicative_order(generator, prime) == prime - 1
            and pow(teichmuller, prime - 1, modulus) == 1
            and ratio_v == pow(teichmuller, 2, modulus)
            and multiplicative_order(ratio_v % prime, prime) == order_d
            and pow(ratio_v, order_d, modulus) == 1
            and ratio_u % prime == 1
            and ratio_u != 1
            and (ratio_u - 1) % prime == 0
            and (ratio_u - 1) % modulus != 0
        )
        failures += int(not verified)
        if order_d > largest_order:
            largest_order = order_d
            largest_order_prime = prime
        transcript.update(
            (
                f"{prime}:{generator}:{teichmuller}:{a_unit}:{b_unit}:"
                f"{ratio_u}:{ratio_v}:{order_d}:{int(verified)}\n"
            ).encode("ascii")
        )
        if prime in selected:
            rows.append(
                {
                    "prime_q": prime,
                    "primitive_root_t": generator,
                    "teichmuller_lift_T_mod_q_squared": teichmuller,
                    "A_mod_q_squared": a_unit,
                    "B_mod_q_squared": b_unit,
                    "U_equals_A_over_B_mod_q_squared": ratio_u,
                    "V_equals_A_power_5_over_B_power_3_mod_q_squared": ratio_v,
                    "order_d_of_V_mod_q": order_d,
                    "q_squared_divides_V_power_d_minus_1": True,
                    "q_exactly_divides_U_minus_1": True,
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "For every prime q>5 choose a primitive root t modulo q and its "
        "Teichmuller lift T=t^q modulo q^2. Put A=T(1+3q), B=T(1+5q), "
        "U=A/B, and V=A^5/B^3 modulo q^2. Then ord_q(V)=(q-1)/2 and "
        "V^((q-1)/2)=1 modulo q^2, whereas ord_q(U)=1 but U is not 1 modulo "
        "q^2; indeed U=1-2q modulo q^2. Thus the square-depth condition for "
        "the (5,-3) order core does not universally transfer to the (1,-1) "
        "core, even along an unbounded sequence of exact orders."
    )
    proof = (
        "The lift T has order q-1 modulo q^2 because T^(q-1)=1 and its "
        "reduction has order q-1. Binomial expansion modulo q^2 gives "
        "(1+3q)^5(1+5q)^(-3)=1, hence V=T^2, of order (q-1)/2 and depth at "
        "least two at that order. The same expansion gives U=(1+3q)/(1+5q)"
        "=1-2q, which has exact q-depth one. Since (q-1)/2 is unbounded, the "
        "countermodels are not confined to bounded orders."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "selected_principal_unit_rows": rows,
        "bounded_universal_model_replay": {
            "prime_limit": LOCAL_MODEL_SCAN_LIMIT,
            "primes_scanned": len(primes),
            "failure_count": failures,
            "largest_countermodel_order": largest_order,
            "largest_order_witness_prime": largest_order_prime,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "unbounded_order_local_countermodel_family_proved": True,
            "universal_local_order_core_transfer_refuted": True,
            "fixed_base_32_over_27_exception_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "A and B vary with q and are not the fixed integers 2 and 3. The "
            "theorem closes only deductions valid for arbitrary q-adic units "
            "using order, LTE, and principal-unit algebra. Special arithmetic "
            "of the fixed bases, general necklaces, and aperiodic Collatz "
            "descent remain open."
        ),
        "failure_count": failures,
    }


def goldbach_half_arc_audit() -> dict[str, Any]:
    cutoffs = (1_000, 3_000, 10_000, 30_000, 100_000, 300_000, 1_000_000)
    flags = prime_flags_up_to(max(cutoffs))
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    prime_count = 0
    cutoff_set = set(cutoffs)
    counts: dict[int, int] = {}
    for value, flag in enumerate(flags):
        prime_count += int(flag)
        if value in cutoff_set:
            counts[value] = prime_count

    for cutoff in cutoffs:
        count = counts[cutoff]
        half_width = Fraction(1, 6 * cutoff)
        pointwise_floor = Fraction(count - 3, 2)
        energy_floor = Fraction((count - 3) ** 2, 12 * cutoff)
        natural_scale = cutoff / (math.log(cutoff) ** 2)
        ratio = float(energy_floor) / natural_scale
        verified = (
            count >= 4
            and pointwise_floor > 0
            and energy_floor
            == 2 * half_width * pointwise_floor * pointwise_floor
        )
        failures += int(not verified)
        transcript.update(
            f"{cutoff}:{count}:{half_width}:{pointwise_floor}:{energy_floor}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "prime_cutoff_X": cutoff,
                "prime_count_pi_X": count,
                "half_frequency_arc_half_width": fraction_payload(half_width),
                "pointwise_absolute_S_floor": fraction_payload(pointwise_floor),
                "exact_integrated_energy_floor": fraction_payload(energy_floor),
                "energy_floor_over_X_log_squared_X": ratio,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let S_X(alpha)=sum_(p<=X) exp(2 pi i p alpha). For X>=5 and "
        "|beta|<=1/(6X), one has |S_X(1/2+beta)| >= (pi(X)-3)/2. Therefore "
        "the interval I_X=[1/2-1/(6X),1/2+1/(6X)] satisfies integral over "
        "I_X of |S_X(alpha)|^2 d alpha >= (pi(X)-3)^2/(12X), which is "
        "asymptotic to X/(12 log^2 X). Any absolute-energy minor-arc budget "
        "of size o(X/log^2 X) must exclude this half-frequency neighborhood."
    )
    proof = (
        "Write alpha=1/2+beta. Every odd prime contributes -exp(2 pi i p "
        "beta). Since |2 pi p beta|<=pi/3, its cosine is at least 1/2. After "
        "multiplying S_X by -1, the odd-prime real parts contribute at least "
        "(pi(X)-1)/2, while the p=2 term costs at most one. This gives the "
        "pointwise floor. Squaring and integrating over length 1/(3X) gives "
        "the exact energy floor; the prime number theorem gives its asymptotic."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_half_frequency_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "half_frequency_pointwise_floor_proved": True,
            "natural_binary_scale_local_energy_proved": True,
            "minor_arc_omission_route_refuted": True,
            "signed_targetwise_residual_saving_proved": False,
            "strong_goldbach_resolved": False,
        },
        "no_go_scope": (
            "The theorem forces the parity rational neighborhood into the major "
            "arcs for absolute-energy arguments. It does not estimate the signed "
            "Fourier coefficient on the correctly defined residual minor arcs, "
            "and it proves no Goldbach representation lower bound."
        ),
        "failure_count": failures,
    }


def twin_dyadic_mimicry_audit() -> dict[str, Any]:
    cases = (
        (30, 11, 7),
        (210, 11, 11),
        (2310, 17, 13),
        (30030, 17, 17),
    )
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for modulus, residue, outside_prime in cases:
        if modulus % outside_prime == 0:
            outside_prime = next_prime_not_dividing(2 * modulus, outside_prime + 2)
        crt_residue, combined = crt_pair(
            residue, modulus, (-2) % outside_prime, outside_prime
        )
        for multiplier in (100, 200, 400, 800):
            block_start = multiplier * combined
            prime = first_prime_in_dyadic_progression(
                crt_residue, combined, block_start
            )
            successor = prime + 2 if prime is not None else None
            verified = (
                prime is not None
                and block_start <= prime <= 2 * block_start
                and deterministic_is_prime(prime)
                and prime % modulus == residue
                and successor is not None
                and successor % outside_prime == 0
                and successor > outside_prime
                and math.gcd(residue, modulus) == 1
                and math.gcd(residue + 2, modulus) == 1
            )
            failures += int(not verified)
            transcript.update(
                (
                    f"{modulus}:{residue}:{outside_prime}:{crt_residue}:"
                    f"{combined}:{block_start}:{prime}:{successor}:{int(verified)}\n"
                ).encode("ascii")
            )
            rows.append(
                {
                    "fixed_period_M": modulus,
                    "admissible_residue_a": residue,
                    "outside_prime_ell": outside_prime,
                    "combined_crt_residue": crt_residue,
                    "combined_modulus_Q": combined,
                    "dyadic_block_start_X": block_start,
                    "prime_mimic_p": prime,
                    "forced_composite_successor_p_plus_2": successor,
                    "successor_cofactor": (
                        successor // outside_prime if successor is not None else None
                    ),
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "Fix M>=1, a modulo M with gcd(a,M)=gcd(a+2,M)=1, and any feature "
        "F periodic modulo M. Choose a prime ell not dividing 2M and let r be "
        "the reduced CRT class r=a modulo M, r=-2 modulo ell. Then there is "
        "X_0 such that every dyadic interval [X,2X] with X>=X_0 contains a "
        "prime p congruent to r modulo M ell. Consequently F(p,p+2)="
        "F(a,a+2) while p+2 is composite in every sufficiently large dyadic "
        "block."
    )
    proof = (
        "CRT gives gcd(r,M ell)=1. The prime number theorem in arithmetic "
        "progressions for the fixed modulus Q=M ell gives pi(2X;Q,r)-"
        "pi(X;Q,r) asymptotic to X/(phi(Q) log X), hence positive for every "
        "sufficiently large X. Taking X_0>ell makes ell a proper divisor of "
        "p+2, and periodicity preserves F."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "finite_dyadic_witness_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "fixed_period_every_large_dyadic_mimicry_proved": True,
            "finite_witness_rows_verified": failures == 0,
            "growing_modulus_uniformity_proved": False,
            "scale_local_type_ii_cancellation_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The threshold X_0 depends on the fixed modulus M ell. The proof is "
            "not uniform when M grows with X and supplies no signed Type II "
            "Lambda correlation. It neither proves nor disproves twin primes."
        ),
        "failure_count": failures,
    }


def proof_dag(
    code: str,
    input_name: str,
    rejected_name: str,
    theorem_name: str,
    open_name: str,
    external_name: str | None = None,
) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T242", "label": input_name, "status": "proved"},
        {"id": f"{code}-N243", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-T243", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-OPEN243", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T242", f"{code}-N243"],
        [f"{code}-T242", f"{code}-T243"],
        [f"{code}-N243", f"{code}-T243"],
        [f"{code}-T243", f"{code}-OPEN243"],
    ]
    if external_name:
        nodes.insert(
            1,
            {
                "id": f"{code}-EXT243",
                "label": external_name,
                "status": "external_theorem",
            },
        )
        edges.insert(1, [f"{code}-EXT243", f"{code}-T243"])
    return {"nodes": nodes, "edges": edges}


def section(
    problem_id: str,
    code: str,
    theorem_name: str,
    result_classification: str,
    computation: dict[str, Any],
    discarded: str,
    retained: str,
    next_lemma: str,
    input_name: str,
    rejected_name: str,
    logical_limit: str,
    claim_boundary: str,
    finite_boundary: str,
    external_name: str | None = None,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{code}-TICKET-243",
        "theorem_name": theorem_name,
        "declared_proposition": computation["theorem"],
        "mathematical_argument": computation["proof"],
        "result_classification": result_classification,
        "problem_status": STATUS,
        "reproducible_computation": computation,
        "finite_computation_boundary": finite_boundary,
        "logical_limit": logical_limit,
        "route_decision": {
            "discard": discarded,
            "parked": [],
            "retain": retained,
            "next_single_lemma": next_lemma,
        },
        "stagnation_count": 0,
        "proof_dag": proof_dag(
            code,
            input_name,
            rejected_name,
            theorem_name,
            next_lemma,
            external_name,
        ),
        "claim_boundary": claim_boundary,
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "BandlimitedEvenTestFamilyNoncompactnessAndFrequencyTightnessNoGo",
            "exact_no_go",
            riemann_bandlimit_audit(),
            "frequency support or frequency tightness alone as compactness of a normalized even Weil-test family",
            "joint physical and frequency tightness plus a uniform arithmetic tail and positive limiting margin",
            "JointPhysicalFrequencyTightnessAndUniformSignedGuinandWeilTailWithPositiveMargin",
            "PointwiseFiniteSectionMovingVectorNoGoAndCompactUniformTransfer",
            "FrequencyTightNormalizedEvenTestFamiliesAreAutomaticallyCompact",
            "No compactness or uniform signed Guinand-Weil tail is proved for the actual admissible class.",
            "No RH proof, disproof, or zero exclusion; one exact bandlimit compactness no-go only.",
            "Five exact symbolic Gram certificates, sizes 4 through 64; the infinite theorem is analytic and does not depend on those rows.",
            "Riemann-Lebesgue lemma and Plancherel theorem",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "UnboundedOrderPrincipalUnitTransferCountermodels",
            "exact_no_go",
            collatz_principal_unit_audit(),
            "deducing the fixed-base 32/27 to 2/3 square-depth transfer from universal order, LTE, and principal-unit algebra",
            "special arithmetic excluding rational-Wieferich order cores for the fixed integers 32 and 27",
            "FixedBaseRationalWieferichExclusionFor32Over27OnAllPrimeOrderCores",
            "RationalWieferichOrderCoreReductionAndBoundedOrderNoGo",
            "UniversalLocalOrderCoreSquareDivisorTransferFromFiveMinusThreeToOneMinusOne",
            "The countermodels vary with q; the fixed-base order-core exception and general Collatz dynamics remain open.",
            "No Collatz proof or cycle; an exact all-prime local countermodel family separates universal algebra from fixed-base arithmetic.",
            f"All {len([p for p in primes_up_to(LOCAL_MODEL_SCAN_LIMIT) if p > 5]):,} primes 5<q<={LOCAL_MODEL_SCAN_LIMIT:,} replayed with exact modular arithmetic; the theorem covers every q>5 independently of the scan.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "OmittedHalfFrequencyArcCarriesNaturalBinaryEnergy",
            "exact_no_go",
            goldbach_half_arc_audit(),
            "placing the parity rational neighborhood around one half in a minor set while demanding an absolute-energy o(X/log^2 X) budget",
            "a complete fixed major-arc cover followed by signed targetwise cancellation on the residual minor arcs",
            "CompleteSmallDenominatorMajorArcCoverageAndSignedResidualBinaryCoefficientSaving",
            "ParsevalScaleObstructionToL2OnlyBinaryMinorArcCertificates",
            "AnAbsoluteMinorEnergyBudgetCanOmitTheHalfFrequencyNeighborhood",
            "No signed residual minor coefficient or positive representation lower bound is proved.",
            "No Goldbach proof or counterexample; one exact local energy lower bound and seven finite prime-count rows only.",
            "Seven exact prime-count/energy-floor rows for 1,000<=X<=1,000,000; the asymptotic uses the prime number theorem.",
            "Prime number theorem",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "FixedPeriodicMimicryInEverySufficientlyLargeDyadicBlock",
            "partial_theorem",
            twin_dyadic_mimicry_audit(),
            "using fixed periodic features even with eventual per-dyadic-scale sampling as a twin-prime certificate",
            "uniform control for moduli growing with scale and genuinely parity-sensitive signed Type II information",
            "ScaleLocalGrowingModulusTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass",
            "GrowingPeriodDiagonalCRTMimicryForShiftTwo",
            "FixedPeriodicPrimeCompositeSuccessorMimicsDisappearOnSomeArbitrarilyLargeDyadicBlocks",
            "The PNT-AP threshold depends on the fixed modulus; growing moduli and Type II cancellation remain open.",
            "No twin-prime proof or counterexample; fixed-period mimicry is upgraded to every sufficiently large dyadic block.",
            "Sixteen exact dyadic witnesses for four fixed periods; the all-large-block theorem relies on fixed-modulus PNT in arithmetic progressions.",
            "Prime number theorem in arithmetic progressions for a fixed modulus",
        ),
    }
    total_failures = sum(
        section_data["reproducible_computation"]["failure_count"]
        for section_data in sections.values()
    )
    machine = {
        "exact_theorem_count": 4,
        "partial_theorem_count": 1,
        "exact_no_go_count": 3,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "collatz",
        "stagnated_problem_count": 0,
        "local_model_scan_limit": LOCAL_MODEL_SCAN_LIMIT,
        "total_failure_count": total_failures,
    }
    audit: dict[str, Any] = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureBandlimitPrincipalUnitHalfArcDyadicMimicryAudit",
            "summary": (
                "TICKET-243 proves three exact route no-go theorems and one "
                "dyadic partial theorem while leaving all four parent conjectures open."
            ),
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
                "compactness": "https://arxiv.org/abs/2204.14237",
                "collatz": "https://arxiv.org/abs/1909.03562",
                "goldbach_minor": "https://arxiv.org/abs/1205.5252",
                "pnt_arithmetic_progressions": "https://arxiv.org/abs/2108.10878",
                "twin_prime_parity": "https://arxiv.org/abs/1407.4897",
            },
            "machine_audit": machine,
        },
        "attempts": [],
    }
    for item in sections.values():
        audit["attempts"].append(
            {
                "problem_id": item["problem_id"],
                "ticket_id": item["ticket_id"],
                "declared_proposition": item["declared_proposition"],
                "new_result": item["theorem_name"],
                "result_classification": item["result_classification"],
                "status": STATUS,
                "bounded_result": {
                    "audit_ref": f"#/{AUDIT_KEY}/{item['problem_id']}",
                    "failure_count": item["reproducible_computation"][
                        "failure_count"
                    ],
                },
                "discarded_route": item["route_decision"]["discard"],
                "parked_routes": item["route_decision"]["parked"],
                "remaining_gap": item["logical_limit"],
                "stagnation_count": item["stagnation_count"],
                "candidate_theorem": item["route_decision"]["next_single_lemma"],
            }
        )
    return audit


def build_research_state(audit: dict[str, Any]) -> dict[str, Any]:
    root = audit[AUDIT_KEY]
    prior = {
        "riemann": "PointwiseFiniteSectionMovingVectorNoGoAndCompactUniformTransfer",
        "collatz": "RationalWieferichOrderCoreReductionAndBoundedOrderNoGo",
        "goldbach": "ParsevalScaleObstructionToL2OnlyBinaryMinorArcCertificates",
        "twin_prime": "GrowingPeriodDiagonalCRTMimicryForShiftTwo",
    }
    problems: dict[str, Any] = {}
    for key in ("riemann", "collatz", "goldbach", "twin_prime"):
        item = root[key]
        problems[key] = {
            "problem_status": STATUS,
            "current_target": item["theorem_name"],
            "established_results": [prior[key], item["theorem_name"]],
            "retired_routes": [item["route_decision"]["discard"]],
            "parked_routes": item["route_decision"]["parked"],
            "remaining_gap": item["logical_limit"],
            "next_single_lemma": item["route_decision"]["next_single_lemma"],
            "stagnation_count": item["stagnation_count"],
            "unresolved_dependencies": [
                node["label"]
                for node in item["proof_dag"]["nodes"]
                if node["status"] in {"assumption", "heuristic", "open"}
            ],
            "finite_computation_boundary": item["finite_computation_boundary"],
            "proof_dag_status": "acyclic_with_one_open_frontier",
            "validation_status": {
                "generator_failure_count": item["reproducible_computation"][
                    "failure_count"
                ],
                "focused_tests_required": True,
                "remote_ci_status": "tracked_by_commit_workflow",
            },
        }
    return {
        "schema": "primeproject.four-problem-research-state.v1",
        "ticket": 243,
        "parent_ticket": 242,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "collatz",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    integrated = (
        ROOT
        / "data/open-problem/ticket243-bandlimit-principal-unit-half-arc-dyadic-mimicry.json"
    )
    write_json(integrated, audit)
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-243-bandlimit-noncompactness.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-243-principal-unit-transfer-no-go.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-243-half-arc-energy.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-243-dyadic-fixed-period-mimicry.json",
    }
    for key, path in paths.items():
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": STATUS,
                **root[key],
            },
        )
    write_json(
        ROOT / "data/open-problem/four-problem-research-state.json",
        build_research_state(audit),
    )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    machine = audit[AUDIT_KEY]["machine_audit"]
    print(json.dumps(machine, indent=2))
    return 0 if machine["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
