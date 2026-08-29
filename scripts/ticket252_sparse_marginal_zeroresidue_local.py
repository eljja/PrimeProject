from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache
from math import isqrt
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket251_interior_crt_cyclotomic_righteven import (
    cyclic_binomial_coefficients,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket252-sparse-marginal-zeroresidue-local.v1"
GENERATED_AT = "2026-08-29T04:30:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "sparse_marginal_zeroresidue_local_audit"

RIEMANN_DELTA_POWERS = tuple(range(3, 15))
COLLATZ_PRIMES = (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)
GOLDBACH_PRIMES = (5, 7, 11, 13)
GOLDBACH_EXPONENTS = tuple(range(1, 18))
TWIN_MODULI = (1, 3, 5, 7, 11, 30, 210, 2310)


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
def riemann_sparse_fourier_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures = 0
    transcript = hashlib.sha256()
    previous: Fraction | None = None
    for power in RIEMANN_DELTA_POWERS:
        delta = Fraction(1, 2**power)
        low_frequency_upper = 2 * delta * (power + 1)
        tail_upper = 2 * delta / 27
        projection_upper = low_frequency_upper + tail_upper
        moment_upper = 2 * delta / (1 - delta**4)
        combined_upper = projection_upper + moment_upper
        verified = previous is None or combined_upper < previous
        failures += int(not verified)
        transcript.update(
            (
                f"{power}:{delta}:{low_frequency_upper}:{tail_upper}:"
                f"{projection_upper}:{moment_upper}:{combined_upper}:"
                f"{int(verified)}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "delta_power": power,
                "delta": fraction_record(delta),
                "sparse_frequency_pair_count_below_inverse_scale": power + 1,
                "proved_low_frequency_energy_upper": fraction_record(
                    low_frequency_upper
                ),
                "proved_tail_energy_upper_using_pi_squared_gt_9": fraction_record(
                    tail_upper
                ),
                "proved_sparse_projection_energy_upper": fraction_record(
                    projection_upper
                ),
                "proved_raw_moment_energy_upper": fraction_record(moment_upper),
                "proved_combined_upper": fraction_record(combined_upper),
                "certificate_verified": verified,
            }
        )
        previous = combined_upper

    theorem = (
        "Let H=L2_even([-1,1]), Q0(f)=sum_(k>=0)|integral x^(2k)f(x)dx|^2, "
        "and let S be an infinite symmetric subset of the nonzero integers with "
        "#(S intersect [-N,N])=o(N). For the orthogonal Fourier projection P_S "
        "onto {2^(-1/2) exp(pi i n x): n in S}, P_S is bounded, positive, "
        "self-adjoint, noncompact, and is not a multiplication operator, yet "
        "inf_(||f||=1)(Q0(f)+<P_S f,f>)=0. Thus even a noncompact nonlocal "
        "positive operator can fail to exclude interior concentration."
    )
    proof = (
        "Use g_delta=(2 delta)^(-1/2)1_[-delta,delta]. Its nth normalized "
        "Fourier coefficient has square delta*sinc(pi n delta)^2. Split S at "
        "A/delta. The low part is delta*o(1/delta), while the full-integer tail "
        "is O(1/A); first let delta tend to zero and then A tend to infinity. "
        "Hence <P_S g_delta,g_delta> tends to zero. Also "
        "Q0(g_delta)<=2 delta/(1-delta^4). Infinite rank proves noncompactness; "
        "positivity and self-adjointness follow from orthogonal projection. Since "
        "0 is not in S, P_S(1)=0 but P_S is nonzero, so it cannot be a "
        "multiplication operator. For S={plus or minus 2^j}, delta=2^(-s), "
        "the low-frequency contribution is at most 2 delta(s+1); the geometric "
        "tail is at most 2 delta/(3 pi^2)<2 delta/27, giving the exact replay."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_sparse_projection_rows": rows,
        "algorithm": "exact Fraction upper bounds for dyadic-frequency Fourier projections and centered indicator packets",
        "complexity": "O(E) exact rational operations for E replay rows; the zero-density theorem is analytic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "zero_density_projection_escape_proved": True,
            "operator_positive_selfadjoint_noncompact_proved": True,
            "operator_nonmultiplication_proved": True,
            "actual_weil_kernel_controlled": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def collatz_marginal_joint_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures = 0
    transcript = hashlib.sha256()
    for q in COLLATZ_PRIMES:
        hit_points = [((3 * t) % q, (5 * t) % q) for t in range(q)]
        miss_points = [(t, t) for t in range(q)]
        hit_u = [0] * q
        hit_v = [0] * q
        miss_u = [0] * q
        miss_v = [0] * q
        for u, v in hit_points:
            hit_u[u] += 1
            hit_v[v] += 1
        for u, v in miss_points:
            miss_u[u] += 1
            miss_v[v] += 1
        hit_separated = sum(
            (5 * u - 3 * v) % q == 0 and (u != 0 or v != 0)
            for u, v in hit_points
        )
        miss_separated = sum(
            (5 * u - 3 * v) % q == 0 and (u != 0 or v != 0)
            for u, v in miss_points
        )
        verified = (
            hit_u == hit_v == miss_u == miss_v == [1] * q
            and hit_separated == q - 1
            and miss_separated == 0
        )
        failures += int(not verified)
        transcript.update(
            f"{q}:{hit_separated}:{miss_separated}:{int(verified)}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "prime_q": q,
                "hit_graph": "(U,V)=(3t,5t)",
                "miss_graph": "(U,V)=(t,t)",
                "each_of_four_marginals_is_exactly_uniform": verified,
                "hit_graph_separated_target_count": hit_separated,
                "miss_graph_separated_target_count": miss_separated,
                "hit_graph_target_mass": fraction_record(Fraction(q - 1, q)),
                "miss_graph_target_mass": fraction_record(Fraction(0, 1)),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For every prime q>5 there are two probability measures on F_q^2 with "
        "identical exactly uniform U- and V-marginals but radically different "
        "mass on the separated projective target [3:5]: the uniform measure on "
        "(3t,5t) has mass (q-1)/q, while the uniform measure on (t,t) has mass "
        "zero. Therefore marginal equidistribution of F_q(2) and F_q(3), even "
        "if exact, cannot by itself prove occurrence, avoidance, or density of "
        "the canonical joint slope [3:5]."
    )
    proof = (
        "Multiplication by 3 and by 5 permutes F_q, so both coordinates of the "
        "hit graph are uniform. Both coordinates of the diagonal miss graph are "
        "also uniform. Every nonzero hit-graph point equals t(3,5), yielding "
        "q-1 separated targets. On the miss graph the target equation is "
        "5t-3t=2t=0, so q>5 forces t=0, which is not separated. For the actual "
        "canonical pair (U_q,V_q), the exact detector is "
        "1_(5U_q-3V_q=0)-1_(U_q=0,V_q=0); additive-character orthogonality "
        "shows that a joint, not marginal, character estimate is required."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_uniform_marginal_countermodel_rows": rows,
        "canonical_exact_indicator": "1_(5U_q-3V_q=0)-1_(U_q=0 and V_q=0)",
        "algorithm": "exact finite-field graph enumeration and integer marginal counts",
        "complexity": "O(sum q) integer operations for replay rows; the theorem is algebraic for every prime q>5",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "uniform_marginals_do_not_control_joint_slope_proved": True,
            "joint_character_control_required": True,
            "canonical_fixed_pair_distribution_controlled": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def goldbach_zero_residue_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures = 0
    transcript = hashlib.sha256()
    low_degree_excluded = 0
    compatible_rows = 0
    for q in GOLDBACH_PRIMES:
        for m in GOLDBACH_EXPONENTS:
            c = cyclic_binomial_coefficients(q, m)
            gap = c[0] - min(c)
            compatible = gap <= 1
            epsilon = 1 if compatible else None
            shift = 1 - c[0] if compatible else None
            counts = [shift + value for value in c] if compatible else None
            verified = (
                (not compatible or (min(counts) >= 0 and counts[0] == 1))
                and (m >= q or not compatible)
            )
            failures += int(not verified)
            low_degree_excluded += int(m < q and not compatible)
            compatible_rows += int(compatible)
            transcript.update(
                f"{q}:{m}:{gap}:{int(compatible)}:{int(verified)}\n".encode(
                    "ascii"
                )
            )
            rows.append(
                {
                    "prime_modulus_q": q,
                    "exponent_m": m,
                    "cyclic_coefficients_c": c,
                    "c0_minus_min_c": gap,
                    "zero_residue_compatibility": compatible,
                    "compatible_zero_residue_epsilon": epsilon,
                    "compatible_uniform_shift": shift,
                    "compatible_nonnegative_integer_vector": counts,
                    "low_degree_m_less_than_q_excluded": m < q and not compatible,
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "Let q>=5 be prime, m>=1, and c_r be the cyclic coefficients of "
        "(1-X)^m modulo X^q-1. If an unweighted prime-count vector N_r(X) has "
        "the same centered nonzero Fourier data q(1-zeta_q^a)^m as the "
        "TICKET-251 cyclotomic family, then N_r=c_r+t for one integer t. Since "
        "N_0(X) is 0 or 1, such a nonnegative integer vector is compatible with "
        "the prime zero-residue constraint if and only if c_0-min_r c_r<=1. "
        "Consequently every 1<=m<q is excluded. This constraint alone does not "
        "exclude the tail: at (q,m)=(5,8), c=(-55,20,20,-55,70) and adding "
        "56 gives (1,76,76,1,126), which passes the zero-residue constraint."
    )
    proof = (
        "Equality of all nonzero Fourier coefficients and equality of the zero "
        "sum imply by Fourier inversion that qN_r-N=q c_r for every r. Thus "
        "N_r=c_r+t, where t=N/q is an integer because both sides are integral. "
        "Only the prime q lies in residue zero, so epsilon=N_0 is in {0,1} and "
        "t=epsilon-c_0. Nonnegativity is possible exactly when "
        "epsilon-c_0+min c>=0, which for some epsilon in {0,1} is equivalent "
        "to c_0-min c<=1. If m<q then c_0=1 and c_1=-m, so the gap is at least "
        "m+1>=2. The displayed (5,8) vector is an exact counterexample to using "
        "the zero-residue constraint alone for every m; it is not asserted to "
        "be an actual prime-count vector."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_zero_residue_criterion_rows": rows,
        "algorithm": "exact cyclic binomial folding, integer gap criterion, and exact compatible-vector construction",
        "complexity": "O(sum_(q,m)(q+m)) integer operations for replay rows; the compatibility criterion is analytic for all q,m",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "zero_residue_compatibility_iff_proved": True,
            "all_low_degree_m_less_than_q_excluded": True,
            "low_degree_excluded_replay_count": low_degree_excluded,
            "compatible_tail_replay_count": compatible_rows,
            "zero_residue_only_global_exclusion_refuted": True,
            "actual_prime_count_vectors_fully_excluded": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor <= isqrt(value):
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def first_prime_in_class(modulus: int, residue: int, forbidden: int | None = None) -> int:
    value = residue % modulus
    if value < 2:
        value += ((2 - value + modulus - 1) // modulus) * modulus
    while not is_prime(value) or value == forbidden:
        value += modulus
    return value


@lru_cache(maxsize=1)
def twin_finite_congruence_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures = 0
    transcript = hashlib.sha256()
    for index, modulus in enumerate(TWIN_MODULI):
        combined = 8 * modulus
        p = first_prime_in_class(combined, combined - 1)
        r = first_prime_in_class(combined, 1, forbidden=p)
        k = 2 * (index % 3) + 3
        m = index % 3 + 1
        congruence_residual = (pow(p, k, modulus) + 2 - pow(r, 2 * m, modulus)) % modulus
        verified = (
            is_prime(p)
            and is_prime(r)
            and p != r
            and p % combined == combined - 1
            and r % combined == 1
            and p % 8 == 7
            and k % 2 == 1
            and congruence_residual == 0
        )
        failures += int(not verified)
        transcript.update(
            f"{modulus}:{p}:{r}:{k}:{m}:{congruence_residual}:{int(verified)}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "modulus_M": modulus,
                "combined_modulus_8M": combined,
                "prime_p_minus_one_class": p,
                "prime_r_plus_one_class": r,
                "odd_left_exponent_k": k,
                "right_half_exponent_m": m,
                "equation_residual_mod_M": congruence_residual,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For every integer M>=1 and every odd k>=3 and m>=1, there are "
        "infinitely many pairs of distinct odd primes p,r such that p=7 modulo "
        "8 and p^k+2=r^(2m) modulo M. Hence the Diophantine equation "
        "p^k+2=r^(2m) has prime-residue local solutions modulo every fixed "
        "finite collection of moduli, and no fixed-modulus local-insolubility "
        "argument can prove the required all-X exclusion."
    )
    proof = (
        "Let L=8M. The reduced residue classes -1 and 1 modulo L each contain "
        "infinitely many primes by Dirichlet's theorem. Choose distinct primes "
        "p=-1 mod L and r=1 mod L. Since k is odd, p^k+2=-1+2=1 mod M, "
        "while r^(2m)=1 mod M; also p=7 mod 8. A finite list of congruence "
        "moduli is absorbed into their least common multiple M. This proves "
        "local compatibility only and supplies no integer equality or twin-prime "
        "lower bound."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_finite_modulus_rows": rows,
        "external_theorem": {
            "name": "Dirichlet theorem on primes in reduced arithmetic progressions",
            "statement_used": "If gcd(a,L)=1, then a modulo L contains infinitely many primes.",
            "status": "external_theorem",
            "dependency_boundary": "Only local prime-residue existence uses Dirichlet; no Diophantine equality is imported.",
        },
        "algorithm": "deterministic trial-division primality and first-prime search in plus/minus one residue classes",
        "complexity": "finite replay uses trial division through sqrt(candidate); the all-M result uses Dirichlet's theorem",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "prime_residue_local_solutions_for_every_fixed_modulus_proved": True,
            "fixed_finite_congruence_obstruction_excluded": True,
            "global_integer_equation_solved": False,
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
        {"id": f"{code}-T251", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T252", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-REJECT252", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN252", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T251", f"{code}-T252"],
        [f"{code}-T252", f"{code}-REJECT252"],
        [f"{code}-T252", f"{code}-OPEN252"],
    ]
    path = [f"{code}-T251", f"{code}-T252", f"{code}-OPEN252"]
    if external:
        external_id, label = external
        nodes.insert(1, {"id": external_id, "label": label, "status": "external_theorem"})
        edges.insert(0, [external_id, f"{code}-T252"])
        path.insert(1, external_id)
    return {"nodes": nodes, "edges": edges, "resolution_path": path, "acyclic": True}


def section(
    problem_id: str,
    code: str,
    theorem_name: str,
    classification: str,
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
        "ticket_id": f"{code}-TICKET-252",
        "theorem_name": theorem_name,
        "declared_proposition": computation["theorem"],
        "mathematical_argument": computation["proof"],
        "result_classification": classification,
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
    riemann = riemann_sparse_fourier_audit()
    collatz = collatz_marginal_joint_audit()
    goldbach = goldbach_zero_residue_audit()
    twin = twin_finite_congruence_audit()
    sections = {
        "riemann": section(
            "riemann", "RH", "SparseFourierProjectionInteriorConcentrationNoGo", "exact_no_go", riemann,
            "using noncompactness and nonlocality alone, or a zero-density spectral projection, as a certificate that an arithmetic operator excludes interior concentration",
            ["abstract Fourier projections not identified with the actual Weil operator"],
            "a quantitative spectral-thickness property tied to the actual arithmetic Weil kernel",
            "ActualWeilKernelHasPositiveDensityAgainstEveryInteriorWavePacket",
            "InteriorZeroLocalMultiplierCoercivityNoGo",
            "EveryPositiveNoncompactNonlocalOperatorExcludesInteriorConcentration",
            "The sparse projection is an abstract periodic Fourier operator, not the actual Weil form. The missing step is a proved positive-density or stronger lower bound for the genuine arithmetic kernel on every admissible concentration packet.",
            "No RH proof or disproof; one exact noncompact nonlocal operator no-go theorem.",
            f"{len(RIEMANN_DELTA_POWERS)} exact rational dyadic rows replay S={{plus/minus 2^j}}; the zero-density conclusion is analytic.",
        ),
        "collatz": section(
            "collatz", "CO", "UniformMarginalsCannotDetectProjectiveFermatSlopeNoGo", "exact_no_go", collatz,
            "deducing occurrence, avoidance, or density of [3:5] from separate marginal equidistribution statements for F_q(2) and F_q(3)",
            ["one-coordinate Fermat-quotient statistics without joint character information"],
            "joint additive-character cancellation for the canonical pair on the linear form 5U_q-3V_q",
            "JointFermatQuotientCharacterCancellationAtSlopeThreeFifths",
            "FinitePrimeCanonicalLiftPatternCRTInterpolationNoGo",
            "ExactMarginalEquidistributionForcesCanonicalSlopeDensity",
            "The countermodels are probability measures on F_q^2, not the actual cross-prime distribution of (F_q(2),F_q(3)); they prove only that marginal information is logically insufficient.",
            "No Collatz orbit proof or counterexample; one exact joint-versus-marginal distribution no-go theorem.",
            f"{len(COLLATZ_PRIMES)} exact finite-field graph rows replay the universal algebraic theorem; no canonical-prime occurrence is inferred.",
        ),
        "goldbach": section(
            "goldbach", "GB", "PrimeCountZeroResidueCyclotomicCompatibilityCriterion", "partial_theorem", goldbach,
            "using only the fact N_0(X) is zero or one to exclude every cyclotomic-unit exponent m",
            ["zero-residue compatible tail exponents with c_0-min(c)<=1"],
            "the exact zero-residue criterion and complete exclusion of every low-degree exponent 1<=m<q",
            "ActualPrimeOrderingExcludesZeroResidueCompatibleCyclotomicTail",
            "CyclotomicUnitFullSupportEnergyConcentrationNoGo",
            "PrimeZeroResidueConstraintExcludesEveryCyclotomicExponent",
            "Low degrees m<q are excluded, but compatible tail vectors such as (q,m)=(5,8) need not be actual prime counts. Prime ordering and quantitative discrepancy constraints remain unproved.",
            "No strong Goldbach proof or counterexample; one exact compatibility iff and an all-q low-degree exclusion.",
            f"{len(GOLDBACH_PRIMES)*len(GOLDBACH_EXPONENTS)} exact integer rows replay the criterion; only the stated all-q low-degree theorem is infinite.",
        ),
        "twin_prime": section(
            "twin-prime", "TP", "FiniteCongruenceLocalSolubilityNoGoForRightEvenPrimePowers", "exact_no_go", twin,
            "proving x^2-2=p^k has no odd-prime-power solutions by a fixed finite collection of congruence obstructions",
            ["pure fixed-modulus congruence sieves for the all-X Diophantine equation"],
            "a global archimedean, unit-equation, or primitive-divisor obstruction beyond local congruence compatibility",
            "QuadraticUnitCoefficientOneExcludesOddPrimeExponents",
            "RightEvenModuloEightConstraintAndSharpness",
            "SomeFixedFiniteModulusLocallyExcludesAllRightEvenCandidates",
            "Local solutions modulo every fixed M are not integer solutions. The all-X equation, a Type-II lower bound, and twin-prime infinitude remain open.",
            "No twin-prime proof or counterexample; one Dirichlet-dependent exact local-solubility no-go theorem.",
            f"{len(TWIN_MODULI)} exact prime residue rows replay selected moduli; the every-M conclusion uses Dirichlet's theorem.",
            external=("TP-EXT-DIRICHLET", "Dirichlet primes in reduced arithmetic progressions"),
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
            "theorem_name": "FourConjectureSparseMarginalZeroResidueLocalAudit",
            "summary": "TICKET-252 proves three exact route no-go theorems and one partial theorem while leaving all four parent conjectures open.",
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
                "collatz_fixed_representative_context": "https://arxiv.org/abs/1104.3909",
                "goldbach_major_arcs": "https://arxiv.org/abs/1205.5252",
                "twin_prime_parity": "https://arxiv.org/abs/1407.4897",
                "dirichlet_theorem": "https://encyclopediaofmath.org/wiki/Dirichlet_theorem",
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
                "riemann_sparse_projection_case_count": len(riemann["exact_sparse_projection_rows"]),
                "collatz_marginal_countermodel_case_count": len(collatz["exact_uniform_marginal_countermodel_rows"]),
                "goldbach_zero_residue_case_count": len(goldbach["exact_zero_residue_criterion_rows"]),
                "twin_finite_modulus_case_count": len(twin["exact_finite_modulus_rows"]),
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
        established = list(old.get("established_results", []))
        if item["theorem_name"] not in established:
            established.append(item["theorem_name"])
        retired = list(old.get("retired_routes", []))
        if item["route_decision"]["discard"] not in retired:
            retired.append(item["route_decision"]["discard"])
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
        "ticket": 252,
        "parent_ticket": 251,
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
        ROOT / "data/open-problem/ticket252-sparse-marginal-zeroresidue-local.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-252-sparse-fourier-projection.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-252-marginal-joint-slope.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-252-zero-residue-compatibility.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-252-finite-congruence-local-solubility.json",
    }
    for key, path in paths.items():
        write_json(
            path,
            {"schema": SCHEMA, "generated_at": GENERATED_AT, "status": STATUS, **root[key]},
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
