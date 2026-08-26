from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket244_joint_tightness_harmonic_parity_fold_polylog_mimicry import (
    ROOT,
    crt_pair,
    deterministic_is_prime,
    fraction_payload,
    next_prime_after,
    primes_up_to,
    write_json,
)


SCHEMA = "primeproject.ticket245-closure-second-order-klein-linnik.v1"
GENERATED_AT = "2026-08-26T11:30:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "closure_second_order_klein_linnik_audit"
FIRST_LAYER_SCAN_LIMIT = 20_000_000
SECOND_ORDER_SCAN_LIMIT = 50_000
FAREY_DENOMINATOR_LIMITS = (8, 16, 32, 64, 128)


def riemann_closure_margin_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    previous_margin: Fraction | None = None
    for m in (2, 4, 8, 16, 32, 64):
        margin = Fraction(1, m * m + 1)
        verified = margin > 0 and (
            previous_margin is None or margin < previous_margin
        )
        failures += int(not verified)
        transcript.update(f"{m}:{margin.numerator}:{margin.denominator}\n".encode("ascii"))
        rows.append(
            {
                "compact_class_K_m_lower_t": fraction_payload(Fraction(1, m)),
                "exact_minimum_Q_on_K_m": fraction_payload(margin),
                "normalized_L2_norm_squared": fraction_payload(Fraction(1)),
                "common_physical_support": "[-2,2]",
                "certificate_verified": verified,
            }
        )
        previous_margin = margin

    theorem = (
        "Let e0=2^(-1/2)1_[-1,1] and e1=2^(-1/2)"
        "1_([-2,-1] union [1,2]) in real-even L2(R). For 0<t<=1 put "
        "f_t=(t e0+e1)/sqrt(1+t^2), K={f_t:0<t<=1}, and "
        "Q(f)=|<f,e0>|^2. Then K is bounded, relatively compact, and jointly "
        "tight in physical and Fourier space; Q is continuous and Q(f)>0 "
        "for every f in K, but inf_K Q=0. The compact classes "
        "K_m={f_t:1/m<=t<=1} exhaust K and min_(K_m)Q=1/(m^2+1). "
        "More generally, for every nonempty relatively compact K and continuous "
        "Q>=0, inf_K Q>0 if and only if closure(K) is disjoint from Q^(-1)(0)."
    )
    proof = (
        "The two displayed indicator functions are normalized, real-even, "
        "orthogonal, and supported in [-2,2]. The map t->f_t extends "
        "continuously to [0,1], so closure(K)={f_t:0<=t<=1} is compact. "
        "TICKET-244 therefore gives joint physical-frequency tightness (it also "
        "follows directly from the fixed two-dimensional span). Orthogonality "
        "gives Q(f_t)=t^2/(1+t^2), which is positive for t>0, has infimum zero, "
        "and has minimum 1/(m^2+1) on K_m. For the general statement, continuity "
        "extends an infimum-zero sequence to a zero at a convergent subsequence "
        "in closure(K); conversely a zero in the closure is approached from K. "
        "If the compact closure avoids the closed zero set, Q attains a strictly "
        "positive minimum. Thus compactness plus pointwise positivity on a "
        "nonclosed exhaustive family cannot supply a uniform positive margin."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_exhaustion_margin_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "closure_zero_set_margin_criterion_proved": True,
            "joint_tightness_plus_pointwise_positivity_uniform_margin_refuted": True,
            "compact_exhaustion_classwise_margin_globalization_refuted": True,
            "actual_weil_functional_zero_free_on_closure_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The counterfamily is an abstract real-even L2 family, not the actual "
            "normalized Guinand-Weil admissible class. It refutes only the logical "
            "promotion from joint tightness and pointwise or classwise positivity "
            "to a uniform margin; it does not show that the genuine Weil closure "
            "contains a zero-functional test."
        ),
        "failure_count": failures,
    }


def fermat_quotient_mod_q_squared(base: int, prime: int) -> int:
    modulus = prime**3
    residue = pow(base, prime - 1, modulus)
    return ((residue - 1) // prime) % (prime * prime)


@lru_cache(maxsize=1)
def collatz_second_order_audit() -> dict[str, Any]:
    all_primes = [q for q in primes_up_to(FIRST_LAYER_SCAN_LIMIT) if q > 5]
    selected_primes = {7, 23, 109, 487, 1009, 10007, 49999}
    selected_rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    first_bad: list[int] = []
    first_comparison: list[int] = []
    third_depth_bad: list[int] = []
    third_depth_comparison: list[int] = []

    for q in all_primes:
        q2 = q * q
        f2 = ((pow(2, q - 1, q2) - 1) // q) % q
        f3 = ((pow(3, q - 1, q2) - 1) // q) % q
        bad_first = (5 * f2 - 3 * f3) % q == 0
        comparison_first = (f2 - f3) % q == 0
        if bad_first:
            first_bad.append(q)
        if comparison_first:
            first_comparison.append(q)

        if q <= SECOND_ORDER_SCAN_LIMIT:
            u = fermat_quotient_mod_q_squared(2, q)
            v = fermat_quotient_mod_q_squared(3, q)
            bad_second_digit = (
                5 * u - 3 * v + q * (10 * u * u - 3 * v * v)
            ) % q2
            comparison_second_digit = (u - v) % q2
            direct_bad_q3 = pow(32, q - 1, q**3) == pow(27, q - 1, q**3)
            direct_comparison_q3 = pow(2, q - 1, q**3) == pow(3, q - 1, q**3)
            verified = (
                (bad_second_digit == 0) == direct_bad_q3
                and (comparison_second_digit == 0) == direct_comparison_q3
                and ((5 * u - 3 * v) % q == 0) == bad_first
                and ((u - v) % q == 0) == comparison_first
            )
            failures += int(not verified)
            if direct_bad_q3:
                third_depth_bad.append(q)
            if direct_comparison_q3:
                third_depth_comparison.append(q)
            transcript.update(
                (
                    f"{q}:{u}:{v}:{bad_second_digit}:"
                    f"{comparison_second_digit}:{int(verified)}\n"
                ).encode("ascii")
            )
            if q in selected_primes:
                selected_rows.append(
                    {
                        "prime_q": q,
                        "Qq2_mod_q_squared": u,
                        "Qq3_mod_q_squared": v,
                        "bad_line_first_layer": bad_first,
                        "comparison_line_first_layer": comparison_first,
                        "bad_line_second_digit_mod_q_squared": bad_second_digit,
                        "comparison_second_digit_mod_q_squared": comparison_second_digit,
                        "q_cubed_divides_32_power_minus_27_power": direct_bad_q3,
                        "q_cubed_divides_2_power_minus_3_power": direct_comparison_q3,
                        "certificate_verified": verified,
                    }
                )

    theorem = (
        "For every prime q>5 define the integer Fermat quotients "
        "U=(2^(q-1)-1)/q and V=(3^(q-1)-1)/q, read modulo q^2. Then "
        "q^3 divides 32^(q-1)-27^(q-1) if and only if "
        "5U-3V+q(10U^2-3V^2)=0 modulo q^2, while q^3 divides "
        "2^(q-1)-3^(q-1) if and only if U-V=0 modulo q^2. Reduction "
        "modulo q recovers the TICKET-244 first-layer bad and comparison "
        "lines. These are exact second-order digit criteria, not an all-prime "
        "nonvanishing theorem."
    )
    proof = (
        "Write 2^(q-1)=1+qU and 3^(q-1)=1+qV. Modulo q^3, the binomial "
        "theorem gives (1+qU)^5=1+5qU+10q^2U^2 and "
        "(1+qV)^3=1+3qV+3q^2V^2. Subtracting and dividing by q proves "
        "the first criterion. Direct subtraction of 1+qU and 1+qV proves "
        "the second. Only U,V modulo q^2 are needed. The computation checks "
        "both criteria against independent modular exponentiation modulo q^3."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "selected_exact_second_order_rows": selected_rows,
        "adversarial_first_layer_scan": {
            "prime_limit": FIRST_LAYER_SCAN_LIMIT,
            "primes_scanned": len(all_primes),
            "bad_line_prime_count": len(first_bad),
            "bad_line_primes": first_bad,
            "comparison_line_prime_count": len(first_comparison),
            "comparison_line_primes": first_comparison,
        },
        "second_order_replay": {
            "prime_limit": SECOND_ORDER_SCAN_LIMIT,
            "primes_scanned": sum(q <= SECOND_ORDER_SCAN_LIMIT for q in all_primes),
            "q_cubed_bad_line_prime_count": len(third_depth_bad),
            "q_cubed_bad_line_primes": third_depth_bad,
            "q_cubed_comparison_prime_count": len(third_depth_comparison),
            "q_cubed_comparison_primes": third_depth_comparison,
            "failure_count": failures,
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "exact_second_order_digit_criteria_proved": True,
            "first_layer_bad_line_nonvanishing_through_finite_limit": len(first_bad) == 0,
            "all_prime_bad_line_nonvanishing_proved": False,
            "all_depth_fixed_base_domination_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "No first-layer bad prime occurs in the bounded scan, so the scan "
            "does not exercise the actual bad branch and cannot prove it empty. "
            "The formula decides depth three once q is supplied but gives no "
            "uniform control at arbitrary depth and no statement about general "
            "Collatz trajectories or nontrivial cycles."
        ),
        "failure_count": failures,
    }


def mod_one(value: Fraction) -> Fraction:
    return value - math.floor(value)


def klein_orbit(value: Fraction) -> tuple[Fraction, ...]:
    half = Fraction(1, 2)
    return tuple(
        sorted(
            {
                mod_one(value),
                mod_one(value + half),
                mod_one(-value),
                mod_one(half - value),
            }
        )
    )


def goldbach_klein_orbit_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for limit in FAREY_DENOMINATOR_LIMITS:
        seeds = {
            Fraction(a, q)
            for q in range(1, limit + 1)
            for a in range(q)
            if math.gcd(a, q) == 1
        }
        orbits = {klein_orbit(value) for value in seeds}
        closure = {value for orbit in orbits for value in orbit}
        size_two = sum(len(orbit) == 2 for orbit in orbits)
        size_four = sum(len(orbit) == 4 for orbit in orbits)
        canonical_quarter_representatives = {
            min(value, Fraction(1, 2) - value)
            for value in closure
            if Fraction(0) <= value <= Fraction(1, 2)
        }
        verified = (
            size_two == 2
            and size_two + size_four == len(orbits)
            and len(closure) == 2 * size_two + 4 * size_four
            and len(canonical_quarter_representatives) == len(orbits)
            and all(klein_orbit(value) in orbits for value in closure)
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{limit}:{len(seeds)}:{len(closure)}:{len(orbits)}:"
                f"{size_two}:{size_four}:{int(verified)}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "seed_denominator_limit_Q": limit,
                "reduced_rational_seed_count": len(seeds),
                "klein_closed_center_count": len(closure),
                "canonical_quarter_torus_orbit_count": len(orbits),
                "orbit_size_two_count": size_two,
                "orbit_size_four_count": size_four,
                "maximum_denominator_after_half_turn": max(
                    value.denominator for value in closure
                ),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let O_X(alpha)=sum_(3<=p<=X) exp(2 pi i p alpha) and, for even N, "
        "I_(X,N)(alpha)=O_X(alpha)^2 exp(-2 pi i N alpha) on R/Z. Let "
        "h(alpha)=alpha+1/2 and r(alpha)=-alpha. Then I after h equals I, "
        "and I after r equals the complex conjugate of I. Consequently, for "
        "every measurable E whose four Klein images E,hE,rE,hrE are disjoint "
        "up to null sets, the signed integral over their union is exactly "
        "4 Re integral_E I. Every rational center belongs to a Klein orbit "
        "with a representative in [0,1/4]; only the orbits of 0 and 1/4 "
        "have size two, and every other orbit has size four."
    )
    proof = (
        "TICKET-244 gives O_X(alpha+1/2)=-O_X(alpha), and even N removes the "
        "phase sign, proving h-invariance. Since O_X(-alpha) is the complex "
        "conjugate of O_X(alpha), the same is true for I under r. Haar measure "
        "is invariant under h and r, so the four integrals are J,J,conj(J),"
        "conj(J). Their sum is 4 Re J. The commuting involutions h and r form "
        "a Klein four-group. Folding first modulo h and then by reflection sends "
        "every center to [0,1/4]. Stabilizers occur only at alpha=0 modulo 1/2 "
        "or alpha=1/4 modulo 1/2, giving exactly the two size-two orbits."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_rational_center_orbit_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "klein_four_integrand_symmetry_proved": True,
            "four_arc_signed_integral_reduction_proved": True,
            "all_rational_centers_reduce_to_quarter_torus": True,
            "representative_arc_asymptotic_proved": False,
            "signed_residual_saving_proved": False,
            "strong_goldbach_resolved": False,
        },
        "no_go_scope": (
            "The theorem removes duplicate signed analysis among symmetry-related "
            "arcs only. It neither estimates one representative arc nor proves "
            "that a chosen collection of neighborhoods is disjoint. Denominators "
            "may double under the half turn, and minor-arc cancellation and a "
            "uniform positive Goldbach lower bound remain open."
        ),
        "failure_count": failures,
    }


def first_prime_in_progression(residue: int, modulus: int) -> int:
    candidate = residue
    if candidate < 2:
        candidate += modulus
    while not deterministic_is_prime(candidate):
        candidate += modulus
    return candidate


def twin_linnik_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for modulus, admissible in ((1, 0), (30, 11), (210, 11), (2310, 17), (30030, 17)):
        if modulus == 1:
            ell_one, ell_two = 3, 5
        else:
            ell_one = next_prime_after(modulus)
            ell_two = next_prime_after(2 * modulus)
        residue, combined = crt_pair(
            admissible % modulus, modulus, (-2) % ell_one, ell_one
        )
        residue, combined = crt_pair(
            residue, combined, (-2) % ell_two, ell_two
        )
        prime = first_prime_in_progression(residue, combined)
        cofactor = (prime + 2) // (ell_one * ell_two)
        verified = (
            math.gcd(admissible, modulus) == 1
            and math.gcd(admissible + 2, modulus) == 1
            and prime % modulus == admissible % modulus
            and deterministic_is_prime(prime)
            and prime + 2 == ell_one * ell_two * cofactor
            and cofactor >= 1
            and not deterministic_is_prime(prime + 2)
            and (modulus == 1 or combined < 8 * modulus**3)
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{modulus}:{admissible}:{ell_one}:{ell_two}:{residue}:"
                f"{combined}:{prime}:{cofactor}:{int(verified)}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "period_M": modulus,
                "admissible_residue_a": admissible,
                "bertrand_prime_ell_1": ell_one,
                "bertrand_prime_ell_2": ell_two,
                "crt_residue": residue,
                "crt_modulus_Q": combined,
                "Q_less_than_8M_cubed": modulus == 1 or combined < 8 * modulus**3,
                "first_prime_in_crt_class": prime,
                "forced_composite_successor": prime + 2,
                "successor_factorization": f"{ell_one}*{ell_two}*{cofactor}",
                "certificate_verified": verified,
            }
        )

    theorem = (
        "There are absolute constants C,L>0 such that for every integer M>=1, "
        "every residue a modulo M with gcd(a,M)=gcd(a+2,M)=1, and every feature "
        "F of (n,n+2) depending only on that pair modulo M, there is a prime "
        "p<=C M^(3L) with F(p,p+2)=F(a,a+2) but p+2 composite. Consequently, "
        "a globally prefix-sound pure M-periodic twin certificate that accepts "
        "an admissible class cannot remain sound through X>=C M^(3L); such a "
        "certificate through X must have M>(X/C)^(1/(3L))."
    )
    proof = (
        "For M>=2 choose primes M<ell_1<2M and 2M<ell_2<4M by Bertrand; "
        "use ell_1=3, ell_2=5 for M=1. CRT gives one reduced residue r modulo "
        "Q=M ell_1 ell_2 with r=a modulo M and r=-2 modulo both auxiliary "
        "primes. Here Q<8M^3 for M>=2. Linnik's theorem supplies an absolute "
        "C_0,L and a prime p congruent to r modulo Q with p<=C_0 Q^L; absorb "
        "8^L and the M=1 case into C. Since p+2 is a positive multiple of "
        "ell_1 ell_2, it is composite. Congruence modulo M preserves F. The "
        "prefix lower bound is the contrapositive of the same statement."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_polynomial_height_witness_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "polynomial_height_periodic_mimicry_proved": True,
            "global_prefix_period_lower_bound_proved": True,
            "scale_local_superpolylog_classifier_refuted": False,
            "nonperiodic_type_ii_cancellation_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The Linnik bound concerns a fixed globally reused period and an "
            "initial interval. It does not place the mimic in a prescribed "
            "dyadic block when M changes with that block, and it says nothing "
            "about nonperiodic features or signed Type-I/II Lambda correlation."
        ),
        "failure_count": failures,
    }


def proof_dag(
    code: str,
    prior_name: str,
    theorem_name: str,
    open_name: str,
    rejected_name: str | None = None,
    external_names: tuple[str, ...] = (),
) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T244", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T245", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-OPEN245", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T244", f"{code}-T245"],
        [f"{code}-T245", f"{code}-OPEN245"],
    ]
    if rejected_name:
        nodes.insert(1, {"id": f"{code}-N245", "label": rejected_name, "status": "disproved"})
        edges.insert(1, [f"{code}-T244", f"{code}-N245"])
        edges.insert(2, [f"{code}-N245", f"{code}-T245"])
    for index, external_name in enumerate(external_names, start=1):
        external_id = f"{code}-EXT245-{index}"
        nodes.insert(1, {"id": external_id, "label": external_name, "status": "external_theorem"})
        edges.insert(1, [external_id, f"{code}-T245"])
    return {"nodes": nodes, "edges": edges}


def section(
    problem_id: str,
    code: str,
    theorem_name: str,
    result_classification: str,
    computation: dict[str, Any],
    discarded: str,
    parked: list[str],
    retained: str,
    next_lemma: str,
    prior_name: str,
    logical_limit: str,
    claim_boundary: str,
    finite_boundary: str,
    rejected_name: str | None = None,
    external_names: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{code}-TICKET-245",
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
            "parked": parked,
            "retain": retained,
            "next_single_lemma": next_lemma,
        },
        "stagnation_count": 0,
        "proof_dag": proof_dag(
            code, prior_name, theorem_name, next_lemma, rejected_name, external_names
        ),
        "claim_boundary": claim_boundary,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_closure_margin_audit()
    collatz = collatz_second_order_audit()
    goldbach = goldbach_klein_orbit_audit()
    twin = twin_linnik_audit()
    sections = {
        "riemann": section(
            "riemann", "RH", "ClosureZeroSetObstructionToUniformWeilMargin", "exact_no_go", riemann,
            "joint tightness plus pointwise positivity, or positive margins on each compact exhaustion stage, as sufficient for one uniform positive Weil margin",
            [],
            "joint tightness together with an explicit zero-free separation theorem on the closure of the genuine normalized admissible class",
            "ZeroFreeClosureSeparationForNormalizedAdmissibleWeilFunctional",
            "JointPhysicalFrequencyTightnessCharacterizesL2Precompactness",
            "No zero-free separation is known for the closure of the actual normalized admissible Weil class, and no signed arithmetic-tail positivity theorem or RH zero exclusion follows.",
            "No RH proof or disproof; one exact compactness-to-margin promotion obstruction in a real-even L2 model.",
            "Six exact rational compact-exhaustion margins; compactness and joint tightness of the infinite family are proved analytically, not inferred from the six rows.",
            "JointTightnessAndPointwisePositivityImplyUniformPositiveMargin",
        ),
        "collatz": section(
            "collatz", "CO", "SecondOrderFixedBaseFermatDigitCriterion", "partial_theorem", collatz,
            "none newly; the finite absence of bad-line primes is not promoted to an all-prime theorem",
            [],
            "exact higher q-adic digit formulas for the actual bases, while continuing adversarial search for a first bad-line prime",
            "FixedBaseAllPrimeRationalWieferichDepthDomination",
            "FixedBaseBadLineHarmonicSumEquivalence",
            "No all-prime argument excludes the first bad line, and the second-order formula does not control arbitrary q-adic depths or general Collatz dynamics.",
            "No Collatz proof, divergent orbit, or nontrivial cycle; an exact q^3 criterion and bounded adversarial replay only.",
            f"The first layer is scanned for all {len([q for q in primes_up_to(FIRST_LAYER_SCAN_LIMIT) if q > 5]):,} primes through {FIRST_LAYER_SCAN_LIMIT:,}; q^3 identities are replayed only through {SECOND_ORDER_SCAN_LIMIT:,}. Both use exact integer modular arithmetic, but neither finite boundary proves an all-prime statement.",
        ),
        "goldbach": section(
            "goldbach", "GB", "KleinFourOrbitReductionForEvenGoldbachArcs", "partial_theorem", goldbach,
            "independent signed estimation of all four half-turn/reflection-related rational arcs",
            [],
            "one canonical representative per rational-center orbit on the quarter torus, followed by a uniform representative-arc asymptotic and signed residual estimate",
            "UniformRepresentativeArcAsymptoticAndSignedResidualSavingOnQuarterTorus",
            "ExactParityArcFoldingForEvenBinaryGoldbach",
            "Symmetry removes duplicate arcs but supplies no estimate on a canonical representative, no disjoint-width theorem, and no signed minor-arc saving or positive representation lower bound.",
            "No strong Goldbach proof or counterexample; an exact Klein-four signed integral reduction and finite rational-center orbit certificates only.",
            "Five exact rational orbit enumerations for seed denominators through 128; they certify finite combinatorics, while the integral identity is an all-X, all-even-N algebraic theorem.",
            "SymmetryRelatedRationalArcsRequireIndependentSignedEstimates",
        ),
        "twin_prime": section(
            "twin-prime", "TP", "PolynomialHeightPeriodicMimicryFromLinnik", "exact_no_go", twin,
            "a fixed pure periodic twin classifier remaining globally prefix-sound beyond every polynomial height in its period",
            [],
            "scale-local nonperiodic parity-breaking information and signed Type-II Lambda cancellation",
            "ScaleLocalNonperiodicTypeIICancellationBeyondPeriodicHeightBarriers",
            "PolylogarithmicGrowingPeriodMimicryInEveryLargeDyadicBlock",
            "The theorem gives a polynomial height bound for each fixed global period but does not handle a period chosen anew for a prescribed dyadic block or any nonperiodic Type-I/II structure.",
            "No proof of infinitely many twin primes and no counterexample to the conjecture; one quantitative no-go for globally reused periodic certificates.",
            "Five exact CRT/primality/factorization witnesses; the universal polynomial-height conclusion depends on Bertrand's postulate and Linnik's theorem, not on these rows.",
            "FixedPeriodicTwinClassifierCanRemainSoundBeyondEveryPolynomialInItsPeriod",
            ("Bertrand's postulate", "Linnik's least-prime theorem"),
        ),
    }
    total_failures = sum(section["reproducible_computation"]["failure_count"] for section in sections.values())
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureClosureSecondOrderKleinLinnikAudit",
            "summary": "TICKET-245 proves two partial theorems and two exact route no-go theorems while leaving all four parent conjectures open.",
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
                "compactness": "https://arxiv.org/abs/2204.14237",
                "fermat_quotients": "https://arxiv.org/abs/1110.3113",
                "collatz": "https://arxiv.org/abs/1909.03562",
                "goldbach_major_arcs": "https://arxiv.org/abs/1205.5252",
                "linnik": "https://arxiv.org/abs/0906.2749",
                "twin_prime_parity": "https://arxiv.org/abs/1407.4897",
            },
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 2,
                "exact_no_go_count": 2,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "twin_prime",
                "stagnated_problem_count": 0,
                "first_layer_scan_limit": FIRST_LAYER_SCAN_LIMIT,
                "second_order_scan_limit": SECOND_ORDER_SCAN_LIMIT,
                "farey_denominator_limit": max(FAREY_DENOMINATOR_LIMITS),
                "twin_witness_count": len(twin["exact_polynomial_height_witness_rows"]),
                "total_failure_count": total_failures,
            },
        },
        "attempts": [
            {
                "problem_id": item["problem_id"],
                "ticket_id": item["ticket_id"],
                "declared_proposition": item["declared_proposition"],
                "new_result": item["theorem_name"],
                "result_classification": item["result_classification"],
                "status": STATUS,
                "bounded_result": {"audit_ref": f"#/{AUDIT_KEY}/{key}", "failure_count": item["reproducible_computation"]["failure_count"]},
                "discarded_route": item["route_decision"]["discard"],
                "parked_routes": item["route_decision"]["parked"],
                "remaining_gap": item["logical_limit"],
                "stagnation_count": item["stagnation_count"],
                "candidate_theorem": item["route_decision"]["next_single_lemma"],
            }
            for key, item in sections.items()
        ],
    }


def build_research_state(audit: dict[str, Any]) -> dict[str, Any]:
    root = audit[AUDIT_KEY]
    prior_results = {
        "riemann": ["PointwiseFiniteSectionMovingVectorNoGoAndCompactUniformTransfer", "BandlimitedEvenTestFamilyNoncompactnessAndFrequencyTightnessNoGo", "JointPhysicalFrequencyTightnessCharacterizesL2Precompactness"],
        "collatz": ["RationalWieferichOrderCoreReductionAndBoundedOrderNoGo", "UnboundedOrderPrincipalUnitTransferCountermodels", "FixedBaseBadLineHarmonicSumEquivalence"],
        "goldbach": ["ParsevalScaleObstructionToL2OnlyBinaryMinorArcCertificates", "OmittedHalfFrequencyArcCarriesNaturalBinaryEnergy", "ExactParityArcFoldingForEvenBinaryGoldbach"],
        "twin_prime": ["GrowingPeriodDiagonalCRTMimicryForShiftTwo", "FixedPeriodicMimicryInEverySufficientlyLargeDyadicBlock", "PolylogarithmicGrowingPeriodMimicryInEveryLargeDyadicBlock"],
    }
    prior_retired = {
        "riemann": ["frequency support or frequency tightness alone as compactness of a normalized even Weil-test family", "physical tightness alone, together with TICKET-243's frequency-tightness-alone route, as a compactness certificate"],
        "collatz": ["deducing the fixed-base 32/27 to 2/3 square-depth transfer from universal order, LTE, and principal-unit algebra"],
        "goldbach": ["placing the parity rational neighborhood around one half in a minor set while demanding an absolute-energy o(X/log^2 X) budget", "treating the zero and half-frequency arcs as analytically independent for the odd-prime even-target coefficient"],
        "twin_prime": ["using fixed periodic features even with eventual per-dyadic-scale sampling as a twin-prime certificate", "any pure periodic twin certificate whose scale-dependent period is bounded by a fixed power of log X"],
    }
    problems: dict[str, Any] = {}
    for key in ("riemann", "collatz", "goldbach", "twin_prime"):
        item = root[key]
        retired = list(prior_retired[key])
        if not item["route_decision"]["discard"].startswith("none newly"):
            retired.append(item["route_decision"]["discard"])
        problems[key] = {
            "problem_status": STATUS,
            "current_target": item["theorem_name"],
            "established_results": prior_results[key] + [item["theorem_name"]],
            "retired_routes": retired,
            "parked_routes": item["route_decision"]["parked"],
            "remaining_gap": item["logical_limit"],
            "next_single_lemma": item["route_decision"]["next_single_lemma"],
            "stagnation_count": item["stagnation_count"],
            "unresolved_dependencies": [node["label"] for node in item["proof_dag"]["nodes"] if node["status"] in {"assumption", "heuristic", "open"}],
            "finite_computation_boundary": item["finite_computation_boundary"],
            "proof_dag_status": "acyclic_with_one_open_frontier",
            "validation_status": {"generator_failure_count": item["reproducible_computation"]["failure_count"], "focused_tests_required": True, "remote_ci_status": "tracked_by_commit_workflow"},
        }
    return {
        "schema": "primeproject.four-problem-research-state.v1",
        "ticket": 245,
        "parent_ticket": 244,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "twin_prime",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(ROOT / "data/open-problem/ticket245-closure-second-order-klein-linnik.json", audit)
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-245-closure-zero-margin.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-245-second-order-fermat-digit.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-245-klein-rational-arc-orbits.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-245-linnik-polynomial-height-mimicry.json",
    }
    for key, path in paths.items():
        write_json(path, {"schema": SCHEMA, "generated_at": GENERATED_AT, "status": STATUS, **root[key]})
    write_json(ROOT / "data/open-problem/four-problem-research-state.json", build_research_state(audit))


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    machine = audit[AUDIT_KEY]["machine_audit"]
    print(json.dumps(machine, indent=2))
    return 0 if machine["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
