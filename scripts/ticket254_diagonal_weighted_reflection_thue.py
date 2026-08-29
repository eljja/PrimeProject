from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache
from math import comb, isqrt
from pathlib import Path
from typing import Any


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ticket251_interior_crt_cyclotomic_righteven import (
    cyclic_binomial_coefficients,
)
from scripts.ticket253_density_character_prefix_lebesgue import (
    fermat_quotient_mod_prime,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket254-diagonal-weighted-reflection-thue.v1"
GENERATED_AT = "2026-08-29T14:19:28+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "diagonal_weighted_reflection_thue_audit"

RIEMANN_PACKET_SIZES = (1, 2, 3, 4, 7, 15, 31, 63)
COLLATZ_PRIMES = (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
GOLDBACH_PRIMES = (5, 7, 11, 13, 17, 19)
GOLDBACH_EVEN_EXPONENT_LIMIT = 160
TWIN_BOX_RADIUS = 12


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


@lru_cache(maxsize=None)
def second_prime_in_residue(prime_modulus: int, residue: int) -> tuple[int, int, int]:
    hits: list[tuple[int, int]] = []
    prime_index = 0
    value = 2
    while len(hits) < 2:
        if is_prime(value):
            prime_index += 1
            if value % prime_modulus == residue:
                hits.append((value, prime_index))
        value += 1
    return hits[0][0], hits[1][0], hits[1][1]


@lru_cache(maxsize=1)
def riemann_positive_diagonal_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for half_width in RIEMANN_PACKET_SIZES:
        dimension = 2 * half_width + 1
        diagonal = Fraction(1)
        off_diagonal = -Fraction(1, dimension - 1)
        orthogonal_eigenvalue = Fraction(dimension, dimension - 1)
        packet_energy = diagonal + (dimension - 1) * off_diagonal
        verified = (
            diagonal > 0
            and packet_energy == 0
            and orthogonal_eigenvalue > 0
            and orthogonal_eigenvalue <= Fraction(3, 2)
        )
        failures += int(not verified)
        transcript.update(
            f"{half_width}:{dimension}:{diagonal}:{off_diagonal}:{packet_energy}:{orthogonal_eigenvalue}:{int(verified)}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "dirichlet_half_bandwidth_N": half_width,
                "block_dimension_L": dimension,
                "fourier_diagonal": fraction_record(diagonal),
                "common_off_diagonal": fraction_record(off_diagonal),
                "dirichlet_packet_energy": fraction_record(packet_energy),
                "orthogonal_complement_eigenvalue": fraction_record(
                    orthogonal_eigenvalue
                ),
                "operator_norm_upper_bound_three_halves": True,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For every N>=1 there is a bounded positive self-adjoint operator A_N "
        "on l2(Z), with <A_N e_n,e_n>=1 for every Fourier basis vector, but "
        "<A_N d_N,d_N>=0 for d_N=(2N+1)^(-1/2)sum_(|n|<=N)e_n. On the "
        "L=2N+1 packet block take A_N=L/(L-1)I-J/(L-1), and take the "
        "identity off that block. Its packet-block spectrum is {0,L/(L-1)}. "
        "Thus even a uniform strictly positive Fourier diagonal does not imply "
        "Dirichlet-packet domination without off-diagonal information."
    )
    proof = (
        "Every diagonal entry of L/(L-1)I-J/(L-1) is one. The all-ones "
        "vector is killed because J has eigenvalue L there; on its orthogonal "
        "complement J is zero and the eigenvalue is L/(L-1)>0. Direct sum "
        "with the identity gives a bounded positive self-adjoint operator on "
        "l2(Z). The normalized all-ones block vector is d_N, so its energy is "
        "zero. This counterexample addresses diagonal-only inference, not the "
        "actual Guinand-Weil form."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_block_operator_rows": rows,
        "algorithm": "exact Fraction evaluation of the two eigenspaces of an equicorrelated finite block embedded in l2(Z)",
        "complexity": "O(number of replay blocks); the all-N construction is algebraic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "positive_self_adjoint_operator_constructed_for_every_packet_size": True,
            "every_fourier_diagonal_equals_one": True,
            "selected_dirichlet_packet_energy_zero": True,
            "diagonal_only_domination_route_rejected": True,
            "actual_weil_form_analyzed": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


def complete_nontrivial_character_sum(prime: int, residue: int) -> int:
    return prime - 1 if residue % prime == 0 else -1


def separated_detector(prime: int, u: int, v: int) -> Fraction:
    residue = (5 * u - 3 * v) % prime
    character_sum = complete_nontrivial_character_sum(prime, residue)
    origin = int(u % prime == 0 and v % prime == 0)
    return Fraction(1 + character_sum, prime) - origin


@lru_cache(maxsize=1)
def collatz_weighted_complete_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    scenarios = ("canonical", "synthetic_hit", "synthetic_miss", "origin")
    scenario_values: dict[str, list[tuple[int, Fraction, int]]] = {
        name: [] for name in scenarios
    }
    for prime in COLLATZ_PRIMES:
        canonical = (
            fermat_quotient_mod_prime(2, prime),
            fermat_quotient_mod_prime(3, prime),
        )
        samples = {
            "canonical": canonical,
            "synthetic_hit": (3 % prime, 5 % prime),
            "synthetic_miss": (1, 1),
            "origin": (0, 0),
        }
        for name, (u, v) in samples.items():
            residue = (5 * u - 3 * v) % prime
            character_sum = complete_nontrivial_character_sum(prime, residue)
            detector = separated_detector(prime, u, v)
            incidence = int(residue == 0 and not (u == 0 and v == 0))
            verified = detector == incidence and detector >= 0
            failures += int(not verified)
            scenario_values[name].append((prime, detector, incidence))
            transcript.update(
                f"{prime}:{name}:{u}:{v}:{residue}:{character_sum}:{detector}:{incidence}:{int(verified)}\n".encode(
                    "ascii"
                )
            )
            rows.append(
                {
                    "prime_q": prime,
                    "scenario": name,
                    "U_q": u,
                    "V_q": v,
                    "slope_residue_D_q": residue,
                    "complete_character_sum": character_sum,
                    "normalized_separated_detector": fraction_record(detector),
                    "separated_incidence": bool(incidence),
                    "certificate_verified": verified,
                }
            )

    weighted_rows: list[dict[str, Any]] = []
    weight_families = {
        "unit": lambda q: Fraction(1),
        "prime": lambda q: Fraction(q),
        "reciprocal_prime": lambda q: Fraction(1, q),
    }
    for name in scenarios:
        for family, weight in weight_families.items():
            lhs = sum(
                (weight(prime) * detector for prime, detector, _ in scenario_values[name]),
                Fraction(0),
            )
            rhs = sum(
                (weight(prime) * incidence for prime, _, incidence in scenario_values[name]),
                Fraction(0),
            )
            verified = lhs == rhs and lhs >= 0
            failures += int(not verified)
            transcript.update(
                f"weighted:{name}:{family}:{lhs}:{rhs}:{int(verified)}\n".encode("ascii")
            )
            weighted_rows.append(
                {
                    "scenario": name,
                    "nonnegative_weight_family": family,
                    "weighted_complete_detector_sum": fraction_record(lhs),
                    "weighted_incidence_sum": fraction_record(rhs),
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "For every finite set Q of primes q>5, every nonnegative weights "
        "w_q, and arbitrary pairs (U_q,V_q) in F_q^2, let D_q=5U_q-3V_q "
        "and C_q(D)=sum_(h=1)^(q-1)exp(2pi ihD/q). Then "
        "sum_q w_q[(1+C_q(D_q))/q-1_(U_q=V_q=0)] equals exactly "
        "sum_q w_q 1_(D_q=0,(U_q,V_q)!=(0,0)). Every summand is "
        "nonnegative. Hence nonnegative cross-prime averaging of the complete "
        "detector creates no cancellation or smoothing; bounding it is exactly "
        "the original weighted incidence problem."
    )
    proof = (
        "Additive-character orthogonality gives (1+C_q(D))/q=1_(D=0) "
        "pointwise. Subtract the origin indicator and multiply by w_q>=0. "
        "Summing preserves equality and nonnegativity. Therefore a claimed "
        "cancellation estimate for this normalized complete detector cannot be "
        "an independent route to canonical slope avoidance. Signed incomplete "
        "kernels may still contain information and are not ruled out."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_detector_rows": rows,
        "exact_nonnegative_weighted_rows": weighted_rows,
        "algorithm": "exact q^2 Fermat quotients, integer character dichotomy, and Fraction-weighted identities",
        "complexity": "O(sum log q) modular multiplications for canonical rows; the weighted identity is algebraic for arbitrary finite Q",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "pointwise_separated_detector_identity_proved": True,
            "all_nonnegative_weighted_complete_averages_equal_incidence": True,
            "cross_prime_complete_detector_cancellation_route_rejected": True,
            "signed_incomplete_character_route_rejected": False,
            "canonical_cross_prime_distribution_controlled": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def goldbach_reflection_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    scanned_even_pairs = 0
    compatible_pairs = 0
    for prime in GOLDBACH_PRIMES:
        for exponent in range(2, GOLDBACH_EVEN_EXPONENT_LIMIT + 1, 2):
            scanned_even_pairs += 1
            coefficients = cyclic_binomial_coefficients(prime, exponent)
            shift = 1 - coefficients[0]
            compatible = (
                coefficients[0] - min(coefficients) <= 1 and shift > 0
            )
            reflected_residue = exponent % prime
            if not compatible or reflected_residue == 0:
                continue
            compatible_pairs += 1
            total = prime * shift
            first_residue_prime, second_residue_prime, second_prime_index = (
                second_prime_in_residue(prime, reflected_residue)
            )
            reflection_identity = (
                coefficients[reflected_residue] == coefficients[0]
            )
            forced_count = coefficients[reflected_residue] + shift
            threshold_met = total >= second_prime_index
            excluded = reflection_identity and forced_count == 1 and threshold_met
            verified = excluded
            failures += int(not verified)
            transcript.update(
                f"{prime}:{exponent}:{reflected_residue}:{coefficients[0]}:{shift}:{total}:{first_residue_prime}:{second_residue_prime}:{second_prime_index}:{forced_count}:{int(verified)}\n".encode(
                    "ascii"
                )
            )
            rows.append(
                {
                    "prime_modulus_q": prime,
                    "even_cyclotomic_exponent_m": exponent,
                    "reflected_nonzero_residue_m_mod_q": reflected_residue,
                    "cyclic_coefficient_c0": coefficients[0],
                    "reflected_coefficient_equals_c0": reflection_identity,
                    "forced_uniform_shift_t": shift,
                    "forced_total_prime_count_T": total,
                    "forced_count_at_reflected_residue": forced_count,
                    "first_prime_in_reflected_residue": first_residue_prime,
                    "second_prime_in_reflected_residue": second_residue_prime,
                    "global_index_of_second_residue_prime": second_prime_index,
                    "threshold_T_at_least_second_index": threshold_met,
                    "unique_prime_prefix_excluded": excluded,
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "Let q>=5 be prime, m be even with q not dividing m, and c_r be the "
        "cyclic coefficients of (1-X)^m modulo X^q-1. Suppose the tail is "
        "zero-residue compatible, set t=1-c_0 and T=qt, and put r=m mod q. "
        "Let kappa_q(r) be the global prime index of the second prime congruent "
        "to r modulo q. If T>=kappa_q(r), then the tail cannot be realized by "
        "the actual prime prefix. Indeed c_r=c_0 by even reflection, so the "
        "forced count N*_r=c_r+t is one, whereas the first T primes contain "
        "at least two primes in residue r."
    )
    proof = (
        "Writing a_j=(-1)^j binom(m,j), the involution j->m-j gives "
        "a_(m-j)=(-1)^m a_j. Folding modulo q therefore yields "
        "c_(m-r)=(-1)^m c_r. For even m and r=0 this says "
        "c_(m mod q)=c_0. Since q does not divide m, that residue is nonzero, "
        "and compatibility fixes its target count at c_0+(1-c_0)=1. If "
        "T reaches the second prime in that class, its actual prefix count is "
        "at least two, contradicting the TICKET-253 unique-prefix criterion. "
        "Odd m, q-divisible m, and T below the explicit threshold are not "
        "excluded by this argument."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_even_reflection_exclusion_rows": rows,
        "algorithm": "exact cyclic binomial folding plus deterministic enumeration of the first two primes in one nonzero residue class",
        "complexity": "O(sum m + sum kappa log kappa) integer operations for the finite replay; the reflection-threshold theorem is algebraic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "scanned_even_pair_count": scanned_even_pairs,
            "compatible_non_q_divisible_even_pair_count": compatible_pairs,
            "all_selected_pairs_excluded": bool(rows) and failures == 0,
            "largest_forced_prefix_length": max(
                (row["forced_total_prime_count_T"] for row in rows), default=0
            ),
            "even_reflection_identity_proved": True,
            "odd_or_q_divisible_compatible_tails_excluded": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def quadratic_multiply(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    a, b = left
    c, d = right
    return a * c + 2 * b * d, a * d + b * c


def quadratic_power(value: tuple[int, int], exponent: int) -> tuple[int, int]:
    result = (1, 0)
    base = value
    while exponent:
        if exponent & 1:
            result = quadratic_multiply(result, base)
        base = quadratic_multiply(base, base)
        exponent //= 2
    return result


def unit_powers_seventeen() -> list[tuple[int, int]]:
    rows: list[tuple[int, int]] = []
    value = (1, 0)
    for _ in range(17):
        rows.append(value)
        value = quadratic_multiply(value, (1, 1))
    return rows


def thue_coefficient_rows() -> list[dict[str, Any]]:
    rational = [0] * 18
    radical = [0] * 18
    for k in range(18):
        coefficient = comb(17, k)
        if k % 2 == 0:
            rational[k] = coefficient * 2 ** (k // 2)
        else:
            radical[k] = coefficient * 2 ** ((k - 1) // 2)
    rows: list[dict[str, Any]] = []
    for twist, (unit_a, unit_b) in enumerate(unit_powers_seventeen()):
        a_coefficients = [
            unit_a * rational[k] + 2 * unit_b * radical[k] for k in range(18)
        ]
        b_coefficients = [
            unit_a * radical[k] + unit_b * rational[k] for k in range(18)
        ]
        rows.append(
            {
                "unit_twist_j": twist,
                "unit_rational_part_a_j": unit_a,
                "unit_sqrt2_part_b_j": unit_b,
                "A_j_coefficients_for_u_power_17_minus_k_v_power_k": a_coefficients,
                "B_j_coefficients_for_u_power_17_minus_k_v_power_k": b_coefficients,
            }
        )
    return rows


def evaluate_homogeneous(coefficients: list[int], u: int, v: int) -> int:
    return sum(
        coefficient * u ** (17 - k) * v**k
        for k, coefficient in enumerate(coefficients)
    )


@lru_cache(maxsize=1)
def twin_thue_audit() -> dict[str, Any]:
    polynomial_rows = thue_coefficient_rows()
    transcript = hashlib.sha256()
    failures = 0
    grid_cases = 0
    coefficient_one_points: list[dict[str, int]] = []
    admissible_points: list[dict[str, int]] = []
    units = unit_powers_seventeen()
    for row in polynomial_rows:
        twist = row["unit_twist_j"]
        unit = units[twist]
        a_coefficients = row["A_j_coefficients_for_u_power_17_minus_k_v_power_k"]
        b_coefficients = row["B_j_coefficients_for_u_power_17_minus_k_v_power_k"]
        for u in range(-TWIN_BOX_RADIUS, TWIN_BOX_RADIUS + 1):
            for v in range(-TWIN_BOX_RADIUS, TWIN_BOX_RADIUS + 1):
                if u == 0 and v == 0:
                    continue
                grid_cases += 1
                direct_a, direct_b = quadratic_multiply(
                    unit, quadratic_power((u, v), 17)
                )
                polynomial_a = evaluate_homogeneous(a_coefficients, u, v)
                polynomial_b = evaluate_homogeneous(b_coefficients, u, v)
                reduced_y = (-1 if twist % 2 else 1) * (u * u - 2 * v * v)
                norm_verified = (
                    direct_a * direct_a - 2 * direct_b * direct_b
                    == reduced_y**17
                )
                verified = (
                    polynomial_a == direct_a
                    and polynomial_b == direct_b
                    and norm_verified
                )
                failures += int(not verified)
                if direct_b == 1:
                    point = {
                        "unit_twist_j": twist,
                        "u": u,
                        "v": v,
                        "A_j_u_v": direct_a,
                        "B_j_u_v": direct_b,
                        "reduced_y": reduced_y,
                    }
                    coefficient_one_points.append(point)
                    if direct_a > 0 and reduced_y > 0:
                        admissible_points.append(point)
                transcript.update(
                    f"{twist}:{u}:{v}:{direct_a}:{direct_b}:{reduced_y}:{int(verified)}\n".encode(
                        "ascii"
                    )
                )

    theorem = (
        "Positive integer solutions of x^2-2=y^17 are equivalent to admissible "
        "integer points on seventeen explicit homogeneous degree-17 equations. "
        "For 0<=j<17 write (1+sqrt(2))^j=a_j+b_j sqrt(2) and define "
        "A_j(u,v)+B_j(u,v)sqrt(2)=(a_j+b_j sqrt(2))(u+v sqrt(2))^17. "
        "A solution exists iff for some j,u,v, B_j(u,v)=1, A_j(u,v)>0, "
        "and y=(-1)^j(u^2-2v^2)>0; then x=A_j(u,v)."
    )
    proof = (
        "First y is odd: if y and x were even then v_2(x^2-2)=1, not a "
        "multiple of 17. Thus the conjugate factors x+sqrt(2) and x-sqrt(2) "
        "are coprime in Z[sqrt(2)]. This ring is norm-Euclidean, hence a UFD, "
        "so x+sqrt(2)=epsilon alpha^17. Its units are +/- "
        "(1+sqrt(2))^n; absorb a 17th unit power and the sign into alpha to "
        "leave the unique twist j modulo 17. Comparing sqrt(2) coefficients "
        "gives B_j=1, and norms give y=(-1)^j(u^2-2v^2). The converse follows "
        "by multiplying out and taking norms. The reduction is exact, but no "
        "global integral-point exclusion for the seventeen equations is proved."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_unit_twisted_thue_polynomials": polynomial_rows,
        "finite_box_audit": {
            "coordinate_radius": TWIN_BOX_RADIUS,
            "exact_grid_case_count": grid_cases,
            "coefficient_one_point_count": len(coefficient_one_points),
            "admissible_positive_point_count": len(admissible_points),
            "coefficient_one_points": coefficient_one_points,
            "admissible_positive_points": admissible_points,
        },
        "algorithm": "exact quadratic-ring binary exponentiation, explicit homogeneous coefficient evaluation, and integer norm identities",
        "complexity": "O(17 R^2 log 17) quadratic-ring multiplications for box radius R=12; the equivalence is algebraic for all integers",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "z_sqrt2_norm_euclidean_used": True,
            "unit_twist_count": 17,
            "coefficient_one_thue_equivalence_proved": True,
            "finite_box_contains_admissible_positive_solution": bool(admissible_points),
            "all_seventeen_thue_equations_solved": False,
            "exponent_seventeen_excluded": False,
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
) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T253", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T254", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-REJECT254", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN254", "label": open_name, "status": "open"},
    ]
    return {
        "nodes": nodes,
        "edges": [
            [f"{code}-T253", f"{code}-T254"],
            [f"{code}-T254", f"{code}-REJECT254"],
            [f"{code}-T254", f"{code}-OPEN254"],
        ],
        "resolution_path": [f"{code}-T253", f"{code}-T254", f"{code}-OPEN254"],
        "acyclic": True,
    }


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
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{code}-TICKET-254",
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
            code, prior_name, theorem_name, rejected_name, next_lemma
        ),
        "claim_boundary": claim_boundary,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_positive_diagonal_audit()
    collatz = collatz_weighted_complete_audit()
    goldbach = goldbach_reflection_audit()
    twin = twin_thue_audit()
    sections = {
        "riemann": section(
            "riemann", "RH", "PositiveDiagonalDirichletPacketDominationNoGo", "exact_no_go", riemann,
            "inferring a positive Dirichlet-packet lower bound from uniform positivity of Fourier diagonal entries alone",
            ["actual Weil-form block matrices and their off-diagonal row sums"],
            "the need for quantitative off-diagonal control on actual Weil blocks",
            "ActualWeilDirichletBlocksHaveUniformStrictDiagonalDominance",
            "DirichletPacketSpectralDensityLimit",
            "UniformPositiveFourierDiagonalImpliesDirichletPacketDomination",
            "The counterexample ranges over abstract positive operators and does not compute or refute the actual Guinand-Weil form.",
            "No RH proof or disproof; one exact no-go for diagonal-only packet domination.",
            f"{len(riemann['exact_block_operator_rows'])} exact rational blocks replay the all-N algebraic construction.",
        ),
        "collatz": section(
            "collatz", "CO", "NonnegativeCrossPrimeCompleteDetectorAverageNoGo", "exact_no_go", collatz,
            "using any nonnegative weighted cross-prime average of the normalized complete slope detector as an independent cancellation statistic",
            ["signed incomplete character kernels with a proved recovery inequality"],
            "character truncation or another signed transform not identical to incidence",
            "IncompleteSlopeCharacterKernelHasSignedRecoveryAndCrossPrimeCancellation",
            "CompleteSlopeCharacterSumDichotomyNoGo",
            "NonnegativeCompleteDetectorAveragingCreatesCrossPrimeCancellation",
            "The theorem blocks only normalized complete detectors with nonnegative weights; it says nothing about a genuinely signed incomplete transform or canonical occurrence.",
            "No Collatz proof or counterexample; one exact no-go for the proposed cross-prime complete-average implementation.",
            f"{len(collatz['exact_detector_rows'])} detector rows and {len(collatz['exact_nonnegative_weighted_rows'])} exact weighted rows replay the universal identity.",
        ),
        "goldbach": section(
            "goldbach", "GB", "EvenCyclotomicReflectionPrimePrefixExclusion", "partial_theorem", goldbach,
            "treating compatible even cyclotomic tails with q not dividing m as unconstrained after the unique-prefix reduction",
            ["odd compatible exponents", "compatible exponents divisible by q", "reflection rows below the second-residue-prime threshold"],
            "the exact reflection identity and second-residue-prime prefix obstruction",
            "OddOrQDivisibleCompatibleTailPrimePrefixExclusion",
            "PrimeOrderingUniquePrefixRealizabilityCriterion",
            "EveryCompatibleEvenTailCanSurviveActualPrimeOrdering",
            "The reflection theorem excludes only even m with q not dividing m and a verified prefix threshold. It is not a uniform theorem for every compatible tail and does not prove strong Goldbach.",
            "No strong Goldbach proof or counterexample; one infinite conditional exclusion theorem and finite certificates for selected compatible tails.",
            f"{goldbach['aggregate']['scanned_even_pair_count']} even pairs scanned; {len(goldbach['exact_even_reflection_exclusion_rows'])} compatible non-q-divisible rows have exact two-prime certificates.",
        ),
        "twin_prime": section(
            "twin-prime", "TP", "ExponentSeventeenUnitTwistedThueReduction", "partial_theorem", twin,
            "treating x^2-2=y^17 as one opaque two-variable exponential equation without exposing its finite unit-twist classes",
            ["global integral-point exclusion on the seventeen coefficient-one Thue equations"],
            "the exact Z[sqrt(2)] factorization and seventeen explicit homogeneous equations",
            "AllSeventeenUnitTwistedCoefficientOneThueEquationsHaveNoAdmissibleIntegralPoint",
            "RightEvenContaminationReducesToEightyFourLebesgueNagellExponents",
            "ExponentSeventeenRequiresInfinitelyManyIndependentUnitTwistEquations",
            "The reduction has seventeen equations but solves none globally. The finite box is only an implementation audit and cannot use the prior y>10^1000 bound as a proof.",
            "No twin-prime proof or counterexample; one exact exponent-17 Thue reduction with no admissible point found in a finite box.",
            f"17 exact polynomials and {twin['finite_box_audit']['exact_grid_case_count']} integer grid cases verify coefficient and norm identities; global integral points remain open.",
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
            "theorem_name": "FourConjectureDiagonalWeightedReflectionThueAudit",
            "summary": "TICKET-254 proves two exact route no-go theorems and two partial theorems while leaving all four parent conjectures open.",
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
                "collatz_fixed_representative_context": "https://arxiv.org/abs/1104.3909",
                "goldbach_major_arcs": "https://arxiv.org/abs/1205.5252",
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
                "deep_focus_problem": "goldbach",
                "stagnated_problem_count": 0,
                "riemann_block_case_count": len(riemann["exact_block_operator_rows"]),
                "collatz_detector_case_count": len(collatz["exact_detector_rows"]),
                "collatz_weighted_case_count": len(collatz["exact_nonnegative_weighted_rows"]),
                "goldbach_reflection_certificate_count": len(goldbach["exact_even_reflection_exclusion_rows"]),
                "twin_thue_polynomial_count": len(twin["exact_unit_twisted_thue_polynomials"]),
                "twin_thue_grid_case_count": twin["finite_box_audit"]["exact_grid_case_count"],
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
        "ticket": 254,
        "parent_ticket": 253,
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
        ROOT / "data/open-problem/ticket254-diagonal-weighted-reflection-thue.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-254-positive-diagonal-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-254-weighted-complete-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-254-even-reflection-exclusion.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-254-exponent17-thue.json",
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
