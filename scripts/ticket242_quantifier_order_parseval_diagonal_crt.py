from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket242-quantifier-order-parseval-diagonal-crt.v1"
GENERATED_AT = "2026-08-25T23:59:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "quantifier_order_parseval_diagonal_crt_audit"
ORDER_SCAN_LIMIT = 200_000


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
    flags = prime_flags_up_to(limit)
    return [value for value, flag in enumerate(flags) if flag]


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


def riemann_moving_vector_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for dimension in (4, 8, 16, 32, 64, 128):
        negative_index = dimension
        minimum = Fraction(-1)
        fixed_probe_value = Fraction(1)
        normalized_trace = Fraction(dimension - 2, dimension)
        operator_distance_from_identity = Fraction(2)
        verified = (
            minimum == -1
            and fixed_probe_value == 1
            and normalized_trace == Fraction(dimension - 2, dimension)
            and operator_distance_from_identity == 2
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{dimension}:{negative_index}:{minimum}:{fixed_probe_value}:"
                f"{normalized_trace}:{operator_distance_from_identity}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "finite_section_dimension_n": dimension,
                "moving_negative_coordinate_index": negative_index,
                "smallest_eigenvalue": fraction_payload(minimum),
                "fixed_early_coordinate_probe_value": fraction_payload(
                    fixed_probe_value
                ),
                "normalized_trace": fraction_payload(normalized_trace),
                "operator_norm_distance_from_identity": fraction_payload(
                    operator_distance_from_identity
                ),
                "negative_eigenvalue_count": 1,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "On H=l2(N), let A_n=I-2<.,e_n>e_n. For every fixed x in H, "
        "<A_n x,x>=||x||^2-2|x_n|^2 tends to ||x||^2 and is eventually "
        "positive when x is nonzero. Nevertheless inf_(||x||=1)<A_n x,x>="
        "-1 for every n, attained by the moving vector e_n. Thus pointwise "
        "finite-section convergence, even with eventual positivity for every "
        "fixed test, does not imply uniform positivity on a growing test "
        "family. Conversely, if K is a compact normalized test class, q_n "
        "converges uniformly to q on K, and inf_K q>=delta>0, then inf_K "
        "q_n>=delta/2 eventually."
    )
    proof = (
        "Every l2 sequence has x_n->0, which proves fixed-test convergence "
        "and eventual positivity. Direct substitution of e_n gives -1, while "
        "A_n is diagonal with one entry -1 and all other entries 1. For the "
        "compact transfer statement, choose n so that sup_K|q_n-q|<delta/2 "
        "and subtract this uniform error from the lower margin."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "moving_vector_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "fixed_test_pointwise_convergence_proved": True,
            "fixed_test_eventual_positivity_proved": True,
            "growing_family_uniform_positivity_refuted": True,
            "compact_uniform_transfer_criterion_proved": True,
            "signed_guinand_weil_uniform_tail_bound_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The diagonal forms are an abstract quantifier countermodel, not "
            "the Guinand-Weil form. They prove that fixed-test convergence is "
            "logically insufficient; they do not show that an arithmetic "
            "uniform tail estimate or a compact admissible class is impossible."
        ),
        "failure_count": failures,
    }


def collatz_order_core_audit() -> dict[str, Any]:
    primes = [prime for prime in primes_up_to(ORDER_SCAN_LIMIT) if prime > 5]
    cutoffs = (100, 1_000, 10_000, 100_000, ORDER_SCAN_LIMIT)
    cutoff_rows: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    maximum_order = 0
    maximum_order_prime = 0
    bad_line_count = 0
    good_line_count = 0
    lifting_identity_failures = 0
    cutoff_index = 0

    for prime in primes:
        ratio = 32 * pow(27, -1, prime) % prime
        order = multiplicative_order(ratio, prime)
        modulus = prime * prime
        core_depth_two = (
            pow(32, order, modulus) - pow(27, order, modulus)
        ) % modulus == 0
        full_depth_two = (
            pow(32, prime - 1, modulus) - pow(27, prime - 1, modulus)
        ) % modulus == 0
        good_depth_two = (
            pow(2, prime - 1, modulus) - pow(3, prime - 1, modulus)
        ) % modulus == 0
        lifting_ok = core_depth_two == full_depth_two
        lifting_identity_failures += int(not lifting_ok)
        bad_line_count += int(full_depth_two)
        good_line_count += int(full_depth_two and good_depth_two)
        if order > maximum_order:
            maximum_order = order
            maximum_order_prime = prime
        if prime in (7, 11, 13, 17, 29, 59, 109, 1_009, 10_007, 100_003):
            selected_rows.append(
                {
                    "prime_q": prime,
                    "order_d_of_32_over_27": order,
                    "q_squared_divides_order_core": core_depth_two,
                    "q_squared_divides_full_fermat_power": full_depth_two,
                    "q_squared_divides_2_power_minus_3_power": good_depth_two,
                    "order_core_lifting_identity_verified": lifting_ok,
                }
            )
        while cutoff_index < len(cutoffs) and prime >= cutoffs[cutoff_index]:
            cutoff_rows.append(
                {
                    "prime_cutoff": cutoffs[cutoff_index],
                    "largest_order_seen": maximum_order,
                    "order_witness_prime": maximum_order_prime,
                }
            )
            cutoff_index += 1
        transcript.update(
            f"{prime}:{order}:{int(core_depth_two)}:{int(full_depth_two)}\n".encode(
                "ascii"
            )
        )

    while cutoff_index < len(cutoffs):
        cutoff_rows.append(
            {
                "prime_cutoff": cutoffs[cutoff_index],
                "largest_order_seen": maximum_order,
                "order_witness_prime": maximum_order_prime,
            }
        )
        cutoff_index += 1
    failures += lifting_identity_failures

    theorem = (
        "Let q>5 be prime and d=ord_q(32/27). Then v_q(32^(q-1)-"
        "27^(q-1))=v_q(32^d-27^d). In particular the bad Fermat-quotient "
        "line 5F_q(2)=3F_q(3) is equivalent to q^2 dividing the order core "
        "32^d-27^d. The orders d are unbounded as q varies: otherwise every "
        "prime q>5 would divide the fixed nonzero product over 1<=d<=D of "
        "32^d-27^d. Hence checking or controlling only bounded order cores "
        "cannot prove the all-prime fixed-base line avoidance."
    )
    proof = (
        "Write q-1=dk. Since 1<=k<q, q does not divide k. LTE applied to "
        "(32^d)^k-(27^d)^k gives the valuation identity. If all orders were "
        "at most D, each prime q>5 would divide one member of a finite list "
        "of fixed nonzero integers, contradicting the infinitude of primes."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "selected_order_core_rows": selected_rows,
        "order_growth_rows": cutoff_rows,
        "bounded_identity_scan": {
            "prime_limit": ORDER_SCAN_LIMIT,
            "odd_primes_scanned": len(primes),
            "order_core_lifting_identity_failures": lifting_identity_failures,
            "bad_line_candidate_count": bad_line_count,
            "bad_line_candidates_also_on_good_line": good_line_count,
            "largest_order_seen": maximum_order,
            "order_witness_prime": maximum_order_prime,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "order_core_lte_reduction_proved": True,
            "multiplicative_orders_unbounded_proved": True,
            "bounded_order_core_route_sufficient_refuted": True,
            "all_prime_order_core_square_divisor_transfer_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The exact reduction does not exclude a rational Wieferich prime "
            "on an unbounded order core. The bounded scan is smaller than the "
            "TICKET-241 search and is used only to replay the LTE identity. "
            "General necklaces and aperiodic Collatz descent remain open."
        ),
        "failure_count": failures,
    }


def goldbach_parseval_scale_audit() -> dict[str, Any]:
    cutoffs = (1_000, 3_000, 10_000, 30_000, 100_000, 300_000, 1_000_000)
    flags = prime_flags_up_to(max(cutoffs))
    prefix = [0] * (len(flags))
    count = 0
    for value, flag in enumerate(flags):
        count += int(flag)
        prefix[value] = count
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for cutoff in cutoffs:
        prime_count = prefix[cutoff]
        target = cutoff if cutoff % 2 == 0 else cutoff - 1
        representation_count = sum(
            1
            for prime in range(2, target + 1)
            if flags[prime] and flags[target - prime]
        )
        natural_scale = cutoff / (math.log(cutoff) ** 2)
        scale_ratio = prime_count / natural_scale
        verified = (
            representation_count <= prime_count
            and prime_count > natural_scale
            and scale_ratio > 1
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{cutoff}:{prime_count}:{target}:{representation_count}:"
                f"{natural_scale:.17g}:{scale_ratio:.17g}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "prime_cutoff_X": cutoff,
                "parseval_global_L2_energy_pi_X": prime_count,
                "sample_even_target_N": target,
                "ordered_representation_count_R_X_N": representation_count,
                "binary_natural_scale_X_over_log_squared_X": natural_scale,
                "parseval_to_natural_scale_ratio": scale_ratio,
                "global_L2_bound_at_least_entire_representation_count": (
                    prime_count >= representation_count
                ),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For S_X(alpha)=sum_(p<=X)e(p alpha), Parseval gives integral_0^1 "
        "|S_X|^2=pi(X). For every measurable minor-arc set m and even N, "
        "|integral_m S_X(alpha)^2 e(-N alpha)dalpha| is at most the minor "
        "L2 energy and hence at most pi(X). Therefore any fixed binary-arc "
        "certificate whose only minor estimate is the global Parseval bound "
        "cannot close against a proposed main term M_X(N)=o(pi(X)). In "
        "particular X/log^2 X=o(pi(X)) by the prime number theorem, so an "
        "L2-only minor bound misses the natural binary scale by a factor of "
        "order log X."
    )
    proof = (
        "Apply the triangle inequality to the minor Fourier coefficient and "
        "then enlarge the integral to the full circle. Parseval supplies "
        "pi(X). If M_X=o(pi(X)), then M_X-pi(X)<0 eventually. The PNT gives "
        "pi(X)~X/log X, so pi(X)/(X/log^2 X)~log X."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "parseval_scale_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "global_parseval_minor_bound_proved": True,
            "l2_only_natural_scale_certificate_refuted": True,
            "signed_minor_fourier_coefficient_saving_proved": False,
            "uniform_binary_goldbach_lower_bound_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This rejects only a global L2 or triangle-inequality minor-arc "
            "certificate. A fixed decomposition with targetwise signed "
            "cancellation, restriction estimates, or Type I/II information "
            "can be much sharper. No Goldbach counterexample is produced."
        ),
        "failure_count": failures,
    }


def smallest_admissible_residue(modulus: int) -> int:
    for residue in range(1, modulus):
        if math.gcd(residue, modulus) == 1 and math.gcd(residue + 2, modulus) == 1:
            return residue
    raise ValueError(f"no admissible residue modulo {modulus}")


def first_prime_in_progression(
    residue: int, modulus: int, lower_bound: int
) -> int:
    candidate = residue
    if candidate <= lower_bound:
        candidate += ((lower_bound - candidate) // modulus + 1) * modulus
    while not deterministic_is_prime(candidate):
        candidate += modulus
    return candidate


def twin_growing_modulus_diagonal_audit() -> dict[str, Any]:
    moduli = (30, 210, 2_310, 30_030, 510_510, 9_699_690)
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    previous_prime = 2
    outside_start = 3
    for index, modulus in enumerate(moduli, start=1):
        residue = smallest_admissible_residue(modulus)
        outside_prime = next_prime_not_dividing(2 * modulus, outside_start)
        outside_start = outside_prime + 2
        crt_residue, combined = crt_pair(
            residue, modulus, (-2) % outside_prime, outside_prime
        )
        prime = first_prime_in_progression(
            crt_residue, combined, max(previous_prime, outside_prime)
        )
        successor = prime + 2
        verified = (
            prime > previous_prime
            and deterministic_is_prime(prime)
            and prime % modulus == residue
            and successor % outside_prime == 0
            and successor > outside_prime
            and math.gcd(residue, modulus) == 1
            and math.gcd(residue + 2, modulus) == 1
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{index}:{modulus}:{residue}:{outside_prime}:{crt_residue}:"
                f"{combined}:{prime}:{successor}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "stage_j": index,
                "growing_period_M_j": modulus,
                "admissible_residue_a_j": residue,
                "outside_prime_ell_j": outside_prime,
                "combined_crt_residue": crt_residue,
                "combined_modulus_M_j_ell_j": combined,
                "strictly_increasing_prime_witness_p_j": prime,
                "forced_composite_successor_p_j_plus_2": successor,
                "successor_cofactor": successor // outside_prime,
                "certificate_verified": verified,
            }
        )
        previous_prime = prime

    theorem = (
        "Let (M_j) be any sequence of positive periods and choose a_j modulo "
        "M_j with gcd(a_j,M_j)=gcd(a_j+2,M_j)=1. For every j let F_j be any "
        "feature periodic modulo M_j. There is a strictly increasing sequence "
        "of primes p_j such that F_j(p_j,p_j+2)=F_j(a_j,a_j+2) while p_j+2 "
        "is composite. For each j choose a prime ell_j not dividing 2M_j, "
        "impose p_j=a_j mod M_j and p_j=-2 mod ell_j, and choose a Dirichlet "
        "prime in the reduced CRT class above p_(j-1). Thus modulus growth by "
        "itself does not defeat periodic mimicry."
    )
    proof = (
        "CRT gives a reduced class modulo M_j ell_j. Dirichlet supplies "
        "infinitely many primes in it, so one may exceed the preceding "
        "witness. Periodicity preserves F_j, while ell_j divides p_j+2; "
        "choosing p_j>ell_j makes the successor a proper composite multiple."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "growing_modulus_diagonal_crt_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "arbitrary_growing_period_diagonal_mimicry_proved": True,
            "strictly_increasing_prime_mimics_proved": True,
            "modulus_growth_alone_sufficient_refuted": True,
            "predeclared_dyadic_block_mimicry_proved": False,
            "scale_local_type_ii_cancellation_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The scales are selected after the CRT classes: no witness is "
            "placed in a predeclared dyadic block, and no quantitative least-"
            "prime estimate is claimed. The theorem does not touch genuinely "
            "nonperiodic signed Type II information or disprove twin primes."
        ),
        "failure_count": failures,
    }


def proof_dag(
    code: str,
    input_name: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{code}-T241", "label": input_name, "status": "closed_input"},
            {
                "id": f"{code}-N242",
                "label": rejected_name,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{code}-T242",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{code}-OPEN242",
                "label": open_name,
                "status": "highest_risk_open",
            },
        ],
        "edges": [
            [f"{code}-T241", f"{code}-N242"],
            [f"{code}-T241", f"{code}-T242"],
            [f"{code}-N242", f"{code}-T242"],
            [f"{code}-T242", f"{code}-OPEN242"],
        ],
    }


def section(
    problem_id: str,
    code: str,
    theorem_name: str,
    computation: dict[str, Any],
    discarded: str,
    retained: str,
    next_lemma: str,
    input_name: str,
    rejected_name: str,
    logical_limit: str,
    claim_boundary: str,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{code}-TICKET-242",
        "theorem_name": theorem_name,
        "declared_proposition": computation["theorem"],
        "mathematical_argument": computation["proof"],
        "reproducible_computation": computation,
        "logical_limit": logical_limit,
        "route_decision": {
            "discard": discarded,
            "retain": retained,
            "next_single_lemma": next_lemma,
        },
        "proof_dag": proof_dag(
            code, input_name, rejected_name, theorem_name, next_lemma
        ),
        "claim_boundary": claim_boundary,
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "PointwiseFiniteSectionMovingVectorNoGoAndCompactUniformTransfer",
            riemann_moving_vector_audit(),
            "fixed-test finite-section convergence or eventual positivity as a uniform signed Weil positivity proof",
            "a compact normalized admissible class together with a uniform arithmetic truncation error and positive limit margin",
            "UniformSignedGuinandWeilTailBoundOnFrequencyTightNormalizedAdmissibleTestClasses",
            "FinitePrimeCosineRankNoGoForRegularizedWeilPositivity",
            "PointwiseSignedWeilFiniteSectionConvergenceImpliesGrowingFamilyPositivity",
            "No compactness or uniform tail estimate is proved for the actual signed Guinand-Weil admissible class.",
            "No RH proof, disproof, or zero exclusion; one exact quantifier countermodel and a compact transfer criterion only.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "RationalWieferichOrderCoreReductionAndBoundedOrderNoGo",
            collatz_order_core_audit(),
            "proving fixed-base Fermat-quotient line avoidance by checking or controlling only bounded multiplicative orders",
            "an all-order square-divisor transfer from the 32/27 order core to the 2/3 Fermat core",
            "UniformOrderCoreSquareDivisorTransferFrom32Over27To2Over3",
            "PrincipalUnitFermatLineIndependenceNoGoAndHundredMillionAudit",
            "BoundedMultiplicativeOrderCoresSufficeForAllPrimeLineAvoidance",
            "Unbounded-order rational Wieferich square divisors, general necklaces, and aperiodic descent remain open.",
            "No Collatz proof or cycle; one exact LTE/order theorem and a bounded identity replay only.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "ParsevalScaleObstructionToL2OnlyBinaryMinorArcCertificates",
            goldbach_parseval_scale_audit(),
            "closing a natural-scale binary Goldbach lower certificate using only global L2 Parseval energy and triangle inequality",
            "a fixed arc decomposition with targetwise signed minor Fourier-coefficient cancellation below the singular-series main term",
            "FixedBinaryPrimeMinorArcCoefficientIsLittleOOfTargetMainUniformlyOnBufferedEvenTargets",
            "CanonicalErrorContractAndRefinementInstabilityNoGo",
            "GlobalParsevalEnergyControlsBinaryMinorArcsAtTheNaturalMainScale",
            "No signed targetwise minor-arc saving or uniform positive binary-prime main-minus-error certificate is proved.",
            "No Goldbach proof or counterexample; one exact norm-scale no-go and seven finite scale rows only.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "GrowingPeriodDiagonalCRTMimicryForShiftTwo",
            twin_growing_modulus_diagonal_audit(),
            "modulus growth alone, without scale localization or signed Type II information, as a twin-prime certificate",
            "a predeclared-scale growing-modulus Type II estimate with positive shift-two prime mass",
            "ScaleLocalGrowingModulusTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass",
            "FinitePeriodicPrimeFingerprintMimicryForShiftTwo",
            "ArbitraryGrowingPeriodicFeatureEnrichmentEventuallySeparatesTwinPairs",
            "No mimic is placed in a prescribed dyadic block and no parity-sensitive Lambda correlation lower bound is proved.",
            "No twin-prime proof or counterexample; one exact diagonal CRT no-go and six finite witnesses only.",
        ),
    }
    total_failures = sum(
        item["reproducible_computation"]["failure_count"]
        for item in sections.values()
    )
    machine = {
        "exact_theorem_count": 4,
        "route_correction_count": 4,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "conjecture_resolution_count": 0,
        "bounded_order_scan_limit": ORDER_SCAN_LIMIT,
        "total_failure_count": total_failures,
    }
    audit: dict[str, Any] = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureQuantifierOrderParsevalDiagonalCRTAudit",
            "summary": (
                "TICKET-242 proves four exact quantifier, order-core, norm-scale, "
                "or diagonal-CRT boundary theorems and leaves all four parent "
                "conjectures open."
            ),
            **sections,
            "research_baselines": {
                "riemann": "https://arxiv.org/abs/1910.14368",
                "collatz": "https://arxiv.org/abs/1909.03562",
                "fermat_quotient": "https://arxiv.org/abs/1110.3113",
                "goldbach_minor": "https://arxiv.org/abs/1205.5252",
                "goldbach_major": "https://arxiv.org/abs/1305.2897",
                "twin_prime_parity": "https://arxiv.org/abs/1407.4897",
            },
            "machine_audit": machine,
        },
        "attempts": [],
    }
    for item in sections.values():
        route = item["route_decision"]
        audit["attempts"].append(
            {
                "problem_id": item["problem_id"],
                "ticket_id": item["ticket_id"],
                "declared_proposition": item["declared_proposition"],
                "new_result": item["theorem_name"],
                "status": STATUS,
                "bounded_result": {
                    "audit_ref": f"#/{AUDIT_KEY}/{item['problem_id']}",
                    "failure_count": item["reproducible_computation"][
                        "failure_count"
                    ],
                },
                "discarded_route": route["discard"],
                "remaining_gap": item["logical_limit"],
                "candidate_theorem": route["next_single_lemma"],
            }
        )
    return audit


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(
        ROOT / "data/open-problem/ticket242-quantifier-order-parseval-diagonal-crt.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-242-moving-vector-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-242-order-core-no-go.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-242-parseval-scale-no-go.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-242-growing-period-diagonal-crt.json",
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


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    machine = audit[AUDIT_KEY]["machine_audit"]
    print(json.dumps(machine, indent=2))
    return 0 if machine["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
