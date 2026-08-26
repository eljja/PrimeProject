from __future__ import annotations

import hashlib
import json
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
from math import comb, prod
from pathlib import Path
from typing import Any


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket246_moment_alldepth_parseval_primepower import (
    prime_power_representation_table,
)
from scripts.ticket247_hilbert_hensel_lipschitz_primepower import primes_up_to


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket251-interior-crt-cyclotomic-righteven.v1"
GENERATED_AT = "2026-08-27T04:30:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "interior_crt_cyclotomic_righteven_audit"

RIEMANN_DELTA_POWERS = tuple(range(3, 14))
COLLATZ_CASES = (
    ((7, 11), "slope_hit", (3, 5)),
    ((7, 11, 13), "zero_pair", (0, 0)),
    ((11, 17, 23), "asymmetric", (1, 0)),
    ((7, 13, 19, 31), "slope_avoid", (1, 1)),
)
GOLDBACH_PRIMES = (5, 7, 11, 13)
GOLDBACH_EXPONENTS = (1, 2, 3, 5, 8, 13, 21, 34)
GOLDBACH_RHO_DISPLAY = {
    5: Decimal("0.3819660112501052"),
    7: Decimal("0.6431041321077906"),
    11: Decimal("0.8445351712043729"),
    13: Decimal("0.8871447816022119"),
}
TWIN_X_SCALES = (7, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000)


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "display_float": float(value),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


@lru_cache(maxsize=1)
def riemann_interior_zero_audit() -> dict[str, Any]:
    a = Fraction(1, 3)
    rows: list[dict[str, Any]] = []
    failures = 0
    transcript = hashlib.sha256()
    previous: Fraction | None = None
    for power in RIEMANN_DELTA_POWERS:
        delta = Fraction(1, 2**power)
        measure = 4 * delta
        rho = a + delta
        multiplier_upper = (2 * a * delta + delta * delta) ** 2
        moment_upper = measure / (1 - rho**4)
        combined = multiplier_upper + moment_upper
        verified = rho < 1 and (previous is None or combined < previous)
        failures += int(not verified)
        transcript.update(
            (
                f"{power}:{delta}:{measure}:{rho}:{multiplier_upper}:"
                f"{moment_upper}:{combined}:{int(verified)}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "delta_power": power,
                "delta": fraction_record(delta),
                "symmetric_support_measure": fraction_record(measure),
                "support_radius_rho": fraction_record(rho),
                "proved_multiplier_energy_upper": fraction_record(multiplier_upper),
                "proved_raw_moment_energy_upper": fraction_record(moment_upper),
                "proved_combined_upper": fraction_record(combined),
                "certificate_verified": verified,
            }
        )
        previous = combined

    theorem = (
        "Let H=L2_even([-1,1]) and Q0(f)=sum_(k>=0)|integral x^(2k)f(x)dx|^2. "
        "If w is continuous, even, nonnegative, nonzero, and w(x0)=0 for some "
        "x0 in [0,1), then K=M_w is bounded, self-adjoint, and noncompact, yet "
        "inf_{||f||=1}(Q0(f)+<Kf,f>)=0. Hence no such interior-zero local "
        "multiplier can supply full-unit-sphere coercivity for Q0."
    )
    proof = (
        "Choose rho<1 and shrinking symmetric measurable neighborhoods E_delta "
        "of {−x0,x0}, and put g_delta=1_E/sqrt(|E|). Then g_delta is even and "
        "normalized. Continuity gives <M_w g_delta,g_delta><=sup_E w ->0. "
        "For every k, |integral x^(2k)g_delta|^2<=|E|rho^(4k), so "
        "Q0(g_delta)<=|E|/(1-rho^4)->0. Noncompactness follows because w is "
        "bounded below on a positive-measure symmetric region and normalized "
        "indicators of disjoint symmetric subsets have images separated in L2. "
        "For the replay w=(x^2-(1/3)^2)^2 and E_delta is the union of the two "
        "delta-neighborhoods, giving the exact rational bounds recorded below."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_interior_concentration_rows": rows,
        "sharp_boundary": "The theorem requires an interior zero. If w>=c>0 everywhere, <M_w f,f>>=c||f||^2 gives trivial coercivity; an endpoint-only zero is not decided by this construction.",
        "algorithm": "exact Fraction bounds for w(x)=(x^2-1/9)^2 on normalized symmetric indicator concentrations",
        "complexity": "O(E) exact rational operations for E replay rows; the all-w conclusion is analytic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "all_continuous_even_nonnegative_interior_zero_multipliers_excluded": True,
            "noncompactness_proved": True,
            "strictly_positive_multiplier_excluded": False,
            "endpoint_only_zero_excluded": False,
            "actual_weil_form_controlled": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


def fermat_quotient(value: int, prime: int) -> int:
    return ((pow(value, prime - 1, prime * prime) - 1) // prime) % prime


def crt(residues: list[int], moduli: list[int]) -> tuple[int, int]:
    modulus = prod(moduli)
    value = 0
    for residue, local_modulus in zip(residues, moduli):
        partial = modulus // local_modulus
        value += residue * partial * pow(partial, -1, local_modulus)
    return value % modulus, modulus


@lru_cache(maxsize=1)
def collatz_finite_prime_crt_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures = 0
    transcript = hashlib.sha256()
    for primes, label, target in COLLATZ_CASES:
        residues_a: list[int] = []
        residues_b: list[int] = []
        local_rows: list[dict[str, Any]] = []
        for q in primes:
            u, v = target[0] % q, target[1] % q
            base_two = fermat_quotient(2, q)
            base_three = fermat_quotient(3, q)
            k = (2 * (base_two - u)) % q
            ell = (3 * (base_three - v)) % q
            residue_a = 2 + k * q
            residue_b = 3 + ell * q
            local_ok = (
                residue_a % q == 2
                and residue_b % q == 3
                and fermat_quotient(residue_a, q) == u
                and fermat_quotient(residue_b, q) == v
            )
            failures += int(not local_ok)
            residues_a.append(residue_a)
            residues_b.append(residue_b)
            local_rows.append(
                {
                    "prime_q": q,
                    "target_u": u,
                    "target_v": v,
                    "lift_k": k,
                    "lift_ell": ell,
                    "A_mod_q_squared": residue_a,
                    "B_mod_q_squared": residue_b,
                    "certificate_verified": local_ok,
                }
            )
        moduli = [q * q for q in primes]
        A, modulus = crt(residues_a, moduli)
        B, modulus_b = crt(residues_b, moduli)
        global_ok = modulus == modulus_b and all(
            A % (q * q) == ra and B % (q * q) == rb
            for q, ra, rb in zip(primes, residues_a, residues_b)
        )
        failures += int(not global_ok)
        transcript.update(
            f"{label}:{primes}:{target}:{A}:{B}:{modulus}:{int(global_ok)}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "case": label,
                "prime_set": list(primes),
                "common_target_pair": list(target),
                "CRT_modulus": modulus,
                "least_nonnegative_A": A,
                "least_nonnegative_B": B,
                "local_constraints": local_rows,
                "certificate_verified": global_ok,
            }
        )

    theorem = (
        "For every finite nonempty set S of primes q>5 and arbitrary pairs "
        "(u_q,v_q) in F_q^2, there is a unique pair (A,B) modulo "
        "M=product_(q in S)q^2 such that A=2 and B=3 modulo q and "
        "F_q(A)=u_q, F_q(B)=v_q for all q in S, where "
        "F_q(x)=(x^(q-1)-1)/q modulo q. Therefore every prescribed finite "
        "hit/avoidance pattern for the projective slope [3:5] can be "
        "interpolated by fixed integers A,B; finite-prime lift-compatible "
        "local data alone cannot determine the canonical pair A=2,B=3."
    )
    proof = (
        "The binomial theorem modulo q^2 gives "
        "F_q(a+kq)=F_q(a)-k/a modulo q. Thus the unique lift indices are "
        "k_q=2(F_q(2)-u_q) and ell_q=3(F_q(3)-v_q) modulo q. The congruences "
        "A=2+k_q q and B=3+ell_q q modulo q^2 have unique simultaneous "
        "solutions modulo M by the Chinese remainder theorem. Choosing target "
        "pairs on or off [3:5] realizes any finite pattern. The interpolated "
        "integers depend on S and the targets, so this does not decide the "
        "cross-prime behavior of the canonical fixed representatives 2 and 3."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_CRT_interpolation_rows": rows,
        "algorithm": "mod-q^2 exponentiation, affine lift inversion, and exact pairwise-coprime CRT",
        "complexity": "O(sum_(q in S) log q) modular multiplications plus quasi-linear big-integer CRT overhead per case",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "arbitrary_finite_prime_patterns_interpolated": True,
            "unique_pair_mod_product_q_squared_proved": True,
            "canonical_fixed_pair_distribution_controlled": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def cyclic_binomial_coefficients(prime: int, exponent: int) -> list[int]:
    coefficients = [0] * prime
    for j in range(exponent + 1):
        coefficients[j % prime] += (-1 if j % 2 else 1) * comb(exponent, j)
    return coefficients


@lru_cache(maxsize=1)
def goldbach_cyclotomic_concentration_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures = 0
    transcript = hashlib.sha256()
    for q in GOLDBACH_PRIMES:
        previous_upper: Decimal | None = None
        rho_display = GOLDBACH_RHO_DISPLAY[q]
        for m in GOLDBACH_EXPONENTS:
            coefficients = cyclic_binomial_coefficients(q, m)
            shift = -min(coefficients)
            counts = [shift + value for value in coefficients]
            centered = [q * value for value in coefficients]
            parseval_integer = q**3 * sum(value * value for value in coefficients)
            norm_integer = q ** (q - 1 + m)
            with localcontext() as context:
                context.prec = 60
                ratio_upper = Decimal(q - 3) / 2 * rho_display**m
            ratio_display = format(ratio_upper, ".24E")
            verified = (
                sum(coefficients) == 0
                and min(counts) == 0
                and all(value >= 0 for value in counts)
                and sum(centered) == 0
                and norm_integer > 0
                and parseval_integer > 0
                and (previous_upper is None or ratio_upper < previous_upper)
            )
            failures += int(not verified)
            transcript.update(
                (
                    f"{q}:{m}:{coefficients}:{counts}:{parseval_integer}:"
                    f"{norm_integer}:{ratio_display}:{int(verified)}\n"
                ).encode("ascii")
            )
            rows.append(
                {
                    "prime_modulus_q": q,
                    "exponent_m": m,
                    "cyclic_coefficients_c": coefficients,
                    "nonnegative_counts_n": counts,
                    "centered_coefficients_Delta": centered,
                    "exact_reduced_fourier_energy_by_parseval": str(parseval_integer),
                    "exact_galois_norm": str(norm_integer),
                    "outside_pair_to_max_pair_energy_upper_display": ratio_display,
                    "floating_value_role": "display_only_nonproof",
                    "certificate_verified": verified,
                }
            )
            previous_upper = ratio_upper

    theorem = (
        "Fix an odd prime q>=5 and m>=1. Let "
        "c_r=sum_{0<=j<=m, j=r mod q}(-1)^j binom(m,j), C=-min_r c_r, "
        "n_r=C+c_r, N=sum_r n_r, and Delta_r=q n_r-N. Then n_r are "
        "nonnegative integers, sum Delta_r=0, and for every reduced frequency "
        "a, F_m(a)=sum_r Delta_r zeta_q^(ar)=q(1-zeta_q^a)^m is nonzero. "
        "Its Galois norm is q^(q-1+m), while the Fourier energy outside the "
        "maximal conjugate pair a=(q±1)/2 divided by the energy on that pair "
        "is at most ((q-3)/2)rho_q^m ->0, where "
        "rho_q=cos^2(3pi/(2q))/cos^2(pi/(2q))<1."
    )
    proof = (
        "Reduction of (1-X)^m modulo X^q-1 gives the integers c_r and "
        "sum c_r=(1-1)^m=0; the vector is nonzero, so C>0 and n is "
        "nonnegative. Since N=qC, Delta_r=qc_r. Evaluation at zeta_q^a "
        "gives F_m(a)=q(1-zeta_q^a)^m, hence full support. Multiplying over "
        "a=1,...,q-1 and using product_a(1-zeta_q^a)=q gives the exact norm. "
        "Also |F_m(a)|^2=q^2(4sin^2(pi a/q))^m. The maximal values form the "
        "stated pair; every other value is bounded by the second maximum "
        "cos^2(3pi/(2q)), proving the ratio bound. Thus centeredness, "
        "integrality, nonnegativity, exact full support, and a nonzero norm do "
        "not imply quantitative Fourier-energy anti-concentration."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_cyclotomic_unit_rows": rows,
        "algorithm": "exact cyclic binomial folding, integer centering, Parseval integer, and cyclotomic norm; floating trigonometry is display-only",
        "complexity": "O(sum_(q,m)(q+m)) integer operations for replay rows; the concentration limit is analytic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "nonnegative_integer_full_support_concentration_family_proved": True,
            "exact_norm_formula_proved": True,
            "structural_only_quantitative_anti_concentration_refuted": True,
            "actual_prime_count_vectors_excluded_from_family": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def twin_right_even_audit() -> dict[str, Any]:
    upper = max(TWIN_X_SCALES) + 2
    primes = primes_up_to(upper)
    prime_flags = bytearray(upper + 1)
    for prime in primes:
        prime_flags[prime] = 1
    power_flags, representations = prime_power_representation_table(upper, primes)
    witnesses: list[dict[str, Any]] = []
    failures = 0
    transcript = hashlib.sha256()
    for n in range(3, upper - 1, 2):
        if not (power_flags[n] and power_flags[n + 2]):
            continue
        left_base, left_exponent = representations[n]
        right_base, right_exponent = representations[n + 2]
        if right_exponent % 2:
            continue
        verified = left_exponent % 2 == 1 and left_base % 8 == 7
        failures += int(not verified)
        witnesses.append(
            {
                "p_power": n,
                "right_even_power": n + 2,
                "left_prime_p": left_base,
                "left_exponent_k": left_exponent,
                "right_prime_r": right_base,
                "right_exponent_2m": right_exponent,
                "classification_verified": verified,
            }
        )

    rows: list[dict[str, Any]] = []
    for limit in TWIN_X_SCALES:
        active = [row for row in witnesses if row["p_power"] <= limit]
        verified = all(
            row["left_exponent_k"] % 2 == 1 and row["left_prime_p"] % 8 == 7
            for row in active
        )
        failures += int(not verified)
        transcript.update(f"{limit}:{len(active)}:{int(verified)}\n".encode("ascii"))
        rows.append(
            {
                "limit_X": limit,
                "right_even_active_pair_count": len(active),
                "left_exponent_at_least_two_count": sum(
                    row["left_exponent_k"] >= 2 for row in active
                ),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For odd primes p,r and integers k,m>=1, if p^k+2=r^(2m), then "
        "k is odd and p=7 modulo 8. Conversely, every odd k and odd p=7 "
        "modulo 8 satisfies p^k+2=1 modulo 8, so modulo eight alone cannot "
        "force k=1 or exclude composite left powers."
    )
    proof = (
        "Every odd square is 1 modulo 8. If k is even, then p^k=1 modulo "
        "8 and p^k+2=3 modulo 8, impossible. Hence k is odd; for an odd "
        "exponent p^k=p modulo 8, so p+2=1 modulo 8 and p=7 modulo 8. "
        "Conversely, if k is odd and p=7 modulo 8, then p^k+2=1 modulo 8. "
        "This last congruence supplies compatibility only, not an integer "
        "solution, and proves the asserted sharp limitation of this route."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_scale_rows": rows,
        "selected_witnesses": witnesses,
        "withdrawn_source_audit": {
            "source": "https://arxiv.org/abs/2008.11515",
            "status": "withdrawn_major_mistake",
            "used_as_dependency": False,
            "impact": "The stronger k=1 all-X classification was removed; only the elementary modulo-eight theorem is retained.",
        },
        "algorithm": "Eratosthenes sieve, exact odd-prime-power support, and an elementary modulo-eight certificate",
        "complexity": "O(X log log X) time and O(X) memory for finite replay; the universal result is an elementary congruence argument",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "right_even_modulo_eight_constraint_proved": True,
            "modulo_eight_alone_excludes_odd_composite_left_exponents": False,
            "finite_scan_composite_left_witness_count": sum(
                row["left_exponent_k"] >= 2 for row in witnesses
            ),
            "withdrawn_source_used_as_dependency": False,
            "twin_prime_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def proof_dag(
    code: str,
    prior_name: str,
    theorem_name: str,
    rejected_name: str,
    open_name: str,
    external: tuple[str, str] | None = None,
) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T250", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T251", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-REJECT251", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN251", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T250", f"{code}-T251"],
        [f"{code}-T251", f"{code}-REJECT251"],
        [f"{code}-T251", f"{code}-OPEN251"],
    ]
    resolution_path = [f"{code}-T250", f"{code}-T251", f"{code}-OPEN251"]
    if external:
        external_id, label = external
        nodes.insert(1, {"id": external_id, "label": label, "status": "external_theorem"})
        edges.insert(0, [external_id, f"{code}-T251"])
        resolution_path.insert(1, external_id)
    return {
        "nodes": nodes,
        "edges": edges,
        "resolution_path": resolution_path,
        "acyclic": True,
    }


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
    rejected_name: str,
    logical_limit: str,
    claim_boundary: str,
    finite_boundary: str,
    external: tuple[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{code}-TICKET-251",
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
            code, prior_name, theorem_name, rejected_name, next_lemma, external
        ),
        "claim_boundary": claim_boundary,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_interior_zero_audit()
    collatz = collatz_finite_prime_crt_audit()
    goldbach = goldbach_cyclotomic_concentration_audit()
    twin = twin_right_even_audit()
    sections = {
        "riemann": section(
            "riemann", "RH", "InteriorZeroLocalMultiplierCoercivityNoGo", "exact_no_go", riemann,
            "using any continuous nonnegative local multiplier with an interior zero as a full-unit-sphere coercivity repair for the raw moment form",
            ["endpoint-only zero multipliers and strictly positive local floors"],
            "a genuinely nonlocal arithmetic kernel that controls interior concentration without assuming a positive local floor",
            "NonlocalArithmeticWeilKernelExcludesInteriorConcentration",
            "NoncompactMultiplierLegendreEscapeInsufficiencyNoGo",
            "InteriorZeroLocalMultiplierCanBeCoerciveOnTheWholeUnitSphere",
            "The no-go concerns an abstract raw-moment model and local multiplication operators; it neither identifies the actual Weil admissible closure nor proves a sign criterion equivalent to RH.",
            "No RH proof or disproof; one exact analytic no-go theorem for every continuous even nonnegative local multiplier having an interior zero.",
            f"{len(RIEMANN_DELTA_POWERS)} exact rational rows replay w=(x^2-1/9)^2; the universal conclusion is analytic, not inferred from the finite rows.",
        ),
        "collatz": section(
            "collatz", "CO", "FinitePrimeCanonicalLiftPatternCRTInterpolationNoGo", "exact_no_go", collatz,
            "deducing the cross-prime behavior of the canonical Fermat-quotient pair from any finite collection of lift-compatible local constraints",
            ["statistical extrapolation from interpolated noncanonical representatives"],
            "distribution information genuinely tied to the same fixed representatives 2 and 3 over an unbounded prime set",
            "CanonicalRepresentativeFermatQuotientDistributionBeyondFiniteCRTInterpolation",
            "LocalFermatQuotientLiftTransitivityNoGo",
            "FinitePrimeLiftDataDeterminesCanonicalCrossPrimeSlopeBehavior",
            "CRT constructs integers that depend on the finite prime set; it gives no occurrence, avoidance, or density result for F_q(2),F_q(3) as q varies and does not control Collatz trajectories.",
            "No Collatz proof, divergent orbit, or nontrivial cycle; one exact finite-prime interpolation no-go theorem.",
            f"{len(COLLATZ_CASES)} exact CRT certificates are replayed; the theorem for every finite prime set is algebraic.",
        ),
        "goldbach": section(
            "goldbach", "GB", "CyclotomicUnitFullSupportEnergyConcentrationNoGo", "exact_no_go", goldbach,
            "deriving a quantitative Fourier-energy anti-concentration bound from centeredness, integrality, nonnegativity, exact reduced-frequency support, and a nonzero Galois norm alone",
            [],
            "prime-specific arithmetic constraints strong enough to rule out the cyclotomic-unit concentration family for actual prime-count or logarithmically weighted residue vectors",
            "ActualPrimeCountResidueVectorsExcludeCyclotomicUnitConcentration",
            "PrimeModulusRationalFourierFullSupportAndNormBarrier",
            "StructuralFullSupportAndNonzeroNormForceQuantitativeEnergyAnticoncentration",
            "The countermodels are admissible nonnegative integer residue vectors, not proved realizable as actual prime-count vectors; excluding them arithmetically remains open and Goldbach is untouched.",
            "No strong Goldbach proof or counterexample; one exact countermodel family closes a structural-only anti-concentration route.",
            f"{len(GOLDBACH_PRIMES)*len(GOLDBACH_EXPONENTS)} exact integer rows replay the family; trigonometric decimals are display-only and the all-m limit is analytic.",
        ),
        "twin_prime": section(
            "twin-prime", "TP", "RightEvenModuloEightConstraintAndSharpness", "partial_theorem", twin,
            "using the withdrawn x^2-2=y^n source as a dependency, or claiming modulo eight forces the left exponent to equal one",
            ["the all-X Diophantine exclusion x^2-2=y^k for odd k>=3"],
            "the elementary necessary congruence k odd and p=7 modulo 8, with finite prime-power replay kept strictly observational",
            "NoPositivePrimePowerSolutionsOfXSquareMinusTwoEqualsYOddPower",
            "AllBaseEvenLeftRightActiveClassification",
            "ModuloEightConstraintForcesLeftExponentOne",
            "The congruence theorem does not exclude odd composite left exponents, and the absence of such witnesses in a finite scan cannot be promoted to an all-X result. No sieve lower bound or twin-prime infinitude follows.",
            "No twin-prime proof or counterexample; one elementary all-X congruence theorem plus a finite scan with no composite-left witness.",
            f"Exact prime-power support is enumerated at {len(TWIN_X_SCALES)} scales through {max(TWIN_X_SCALES):,}; no conclusion beyond that bound is inferred from the scan.",
        ),
    }
    total_failures = sum(
        item["reproducible_computation"]["failure_count"] for item in sections.values()
    )
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureInteriorCRTConcentrationRightEvenAudit",
            "summary": "TICKET-251 proves three exact route no-go theorems and one elementary partial theorem while leaving all four parent conjectures open.",
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
                "collatz_fixed_representative_context": "https://arxiv.org/abs/1104.3909",
                "goldbach_major_arcs": "https://arxiv.org/abs/1205.5252",
                "twin_prime_parity": "https://arxiv.org/abs/1407.4897",
                "withdrawn_x2_minus_2_notice": "https://arxiv.org/abs/2008.11515",
            },
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 1,
                "exact_no_go_count": 3,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "goldbach",
                "stagnated_problem_count": 0,
                "riemann_concentration_case_count": len(riemann["exact_interior_concentration_rows"]),
                "collatz_CRT_case_count": len(collatz["exact_CRT_interpolation_rows"]),
                "goldbach_cyclotomic_case_count": len(goldbach["exact_cyclotomic_unit_rows"]),
                "twin_active_scale_count": len(twin["exact_scale_rows"]),
                "twin_right_even_witness_count": len(twin["selected_witnesses"]),
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
                "bounded_result": {
                    "audit_ref": f"#/{AUDIT_KEY}/{key}",
                    "failure_count": item["reproducible_computation"]["failure_count"],
                },
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
    previous = json.loads(
        (ROOT / "data/open-problem/four-problem-research-state.json").read_text(
            encoding="utf-8"
        )
    )
    root = audit[AUDIT_KEY]
    problems: dict[str, Any] = {}
    for key in ("riemann", "collatz", "goldbach", "twin_prime"):
        item = root[key]
        old = previous["problems"][key]
        established = [
            name for name in old.get("established_results", [])
            if name != "RightEvenActivePrimePowerClassification"
        ]
        if item["theorem_name"] not in established:
            established.append(item["theorem_name"])
        retired = list(old.get("retired_routes", []))
        discarded = item["route_decision"]["discard"]
        if discarded and discarded not in retired:
            retired.append(discarded)
        parked = list(old.get("parked_routes", []))
        for route in item["route_decision"]["parked"]:
            if route not in parked:
                parked.append(route)
        problems[key] = {
            "problem_status": STATUS,
            "current_target": item["theorem_name"],
            "established_results": established,
            "retired_routes": retired,
            "parked_routes": parked,
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
                "generator_failure_count": item["reproducible_computation"]["failure_count"],
                "focused_tests_required": True,
                "remote_ci_status": "tracked_by_commit_workflow",
            },
        }
    return {
        "schema": "primeproject.four-problem-research-state.v1",
        "ticket": 251,
        "parent_ticket": 250,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "goldbach",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(
        ROOT / "data/open-problem/ticket251-interior-crt-cyclotomic-righteven.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-251-interior-zero-local-multiplier.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-251-finite-prime-crt-interpolation.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-251-cyclotomic-unit-concentration.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-251-right-even-classification.json",
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
