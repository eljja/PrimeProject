from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache
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
from scripts.ticket254_diagonal_weighted_reflection_thue import (
    fraction_record,
    is_prime,
    quadratic_multiply,
    quadratic_power,
    unit_powers_seventeen,
    write_json,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket256-cesaro-kernel-qdiv-gl2.v1"
GENERATED_AT = "2026-08-29T21:40:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "cesaro_kernel_qdiv_gl2_audit"

RIEMANN_REPLAY_DIMENSIONS = tuple(range(1, 13))
COLLATZ_PRIMES = tuple(q for q in range(7, 98) if is_prime(q))
GOLDBACH_PRIMES = (5, 7, 11, 13, 17, 19)
GOLDBACH_EXPONENT_LIMIT = 160
GOLDBACH_PREFIX_LIMIT = 100_000
TWIN_BOX_RADIUS = 64


def symmetric_lag_partial_sums(coefficients: list[Fraction]) -> list[Fraction]:
    if not coefficients:
        raise ValueError("at least a_0 is required")
    rows = [coefficients[0]]
    for coefficient in coefficients[1:]:
        rows.append(rows[-1] + 2 * coefficient)
    return rows


def normalized_packet_energy(coefficients: list[Fraction]) -> Fraction:
    dimension = len(coefficients)
    if dimension == 0:
        raise ValueError("at least a_0 is required")
    return coefficients[0] + 2 * sum(
        Fraction(dimension - lag, dimension) * coefficients[lag]
        for lag in range(1, dimension)
    )


@lru_cache(maxsize=1)
def riemann_cesaro_lag_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for dimension in RIEMANN_REPLAY_DIMENSIONS:
        coefficients = [Fraction(1)]
        if dimension >= 2:
            coefficients.append(Fraction(-1))
        if dimension >= 3:
            coefficients.append(Fraction(1))
        coefficients.extend([Fraction(0)] * (dimension - len(coefficients)))
        partial_sums = symmetric_lag_partial_sums(coefficients)
        energy = normalized_packet_energy(coefficients)
        cesaro = sum(partial_sums, Fraction(0)) / dimension
        verified = energy == cesaro and energy >= 0
        failures += int(not verified)
        transcript.update(
            f"{dimension}:{','.join(map(str, coefficients))}:"
            f"{','.join(map(str, partial_sums))}:{energy}:{cesaro}:"
            f"{int(verified)}\n".encode("ascii")
        )
        rows.append(
            {
                "packet_dimension_L": dimension,
                "lag_coefficients_a_0_through_a_L_minus_1": [
                    fraction_record(value) for value in coefficients
                ],
                "symmetric_lag_partial_sums_S_0_through_S_L_minus_1": [
                    fraction_record(value) for value in partial_sums
                ],
                "minimum_partial_sum": fraction_record(min(partial_sums)),
                "normalized_packet_energy": fraction_record(energy),
                "cesaro_mean_of_partial_sums": fraction_record(cesaro),
                "all_partial_sums_nonnegative": min(partial_sums) >= 0,
                "packet_energy_nonnegative": energy >= 0,
                "identity_verified": verified,
            }
        )

    theorem = (
        "Let (a_k)_(k>=0) be a real sequence and let T_L=(a_|r-s|)_"
        "(0<=r,s<L). For the normalized all-ones packet d_L, put "
        "E_L=<d_L,T_L d_L> and S_n=a_0+2 sum_(k=1)^n a_k. Then for "
        "every L>=1, E_L=L^(-1)sum_(n=0)^(L-1)S_n. Consequently, "
        "S_n>=c for every n implies E_L>=c for every L. This condition "
        "is not necessary: a_0=1,a_1=-1,a_2=1,a_k=0 for k>=3 has "
        "S_1=-1 but E_L>=0 for every L."
    )
    proof = (
        "Counting the L diagonal entries and the 2(L-k) entries at lag k "
        "gives E_L=a_0+2 sum_(k=1)^(L-1)(1-k/L)a_k. On the other hand, "
        "sum_(n=0)^(L-1)S_n=L a_0+2 sum_(k=1)^(L-1)(L-k)a_k, proving "
        "the identity and the lower-bound transfer. For the displayed "
        "counterexample the partial sums are 1,-1,1,1,...; hence E_1=1, "
        "E_2=0, and E_L=(L-2)/L for L>=3. This is an abstract Toeplitz "
        "identity. No actual Guinand-Weil lag is estimated."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_packet_cesaro_rows": rows,
        "algorithm": "exact Fraction evaluation of Toeplitz lag counts, partial sums, and their Cesaro mean",
        "complexity": "O(sum L) for the replay; the all-L identity is algebraic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "packet_energy_cesaro_identity_proved": True,
            "uniform_partial_sum_lower_bound_is_sufficient": True,
            "uniform_partial_sum_lower_bound_is_necessary": False,
            "necessity_counterexample_negative_partial_sum": -1,
            "actual_weil_lag_partial_sums_analyzed": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def collatz_sharp_incomplete_kernel_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    reciprocal_sum = Fraction(0)
    failures = 0
    for index, prime in enumerate(COLLATZ_PRIMES, start=1):
        u = fermat_quotient_mod_prime(2, prime)
        v = fermat_quotient_mod_prime(3, prime)
        canonical_slope = (5 * u - 3 * v) % prime
        error_magnitude = Fraction(1, prime)
        reciprocal_sum += error_magnitude
        mean_absolute_error = reciprocal_sum / index
        verified = (
            prime > 5
            and is_prime(prime)
            and prime * error_magnitude == 1
            and 0 <= canonical_slope < prime
        )
        failures += int(not verified)
        transcript.update(
            f"{index}:{prime}:{u}:{v}:{canonical_slope}:{error_magnitude}:"
            f"{mean_absolute_error}:{int(verified)}\n".encode("ascii")
        )
        rows.append(
            {
                "prime_index_in_replay": index,
                "prime_q": prime,
                "fermat_quotient_F_q_2": u,
                "fermat_quotient_F_q_3": v,
                "canonical_slope_D_q": canonical_slope,
                "slope_hit": canonical_slope == 0,
                "omitted_frequency_h0": 1,
                "support_size_q_minus_one": prime - 1,
                "canonical_error_phase_exponent_mod_q": canonical_slope,
                "exact_error_magnitude": fraction_record(error_magnitude),
                "running_mean_absolute_error": fraction_record(
                    mean_absolute_error
                ),
                "renormalized_error_has_unit_modulus": True,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For prime q and h_0 in F_q define K_(q,h_0)(D)=q^(-1) "
        "sum_(h!=h_0) exp(2 pi i hD/q). Then K_(q,h_0)(D)=delta_0(D)-"
        "q^(-1)exp(2 pi i h_0D/q), so its uniform error is exactly 1/q. "
        "Moreover 1/q is minimax-sharp among all kernels supported on any "
        "proper H missing h_0: the error has Fourier coefficient 1/q at "
        "h_0, whence its sup norm is at least 1/q. At the canonical Collatz "
        "slope D_q=5F_q(2)-3F_q(3), the unnormalized prime-Cesaro average "
        "of the errors tends to zero in absolute value, but only because "
        "the mean of 1/q tends to zero."
    )
    proof = (
        "Subtract the omitted character from the complete Fourier expansion "
        "of delta_0. Fourier inversion gives the exact pointwise error and "
        "its modulus. For any H-supported approximation, the missing error "
        "coefficient is 1/q; a normalized Fourier coefficient is bounded by "
        "the sup norm, proving sharpness. If q_j is the jth replayed prime, "
        "then q_j>=j+1, so n^(-1)sum_(j<=n)1/q_j is at most "
        "n^(-1)sum_(j<=n)1/(j+1), which tends to zero. The same triangle "
        "bound applies at D_q. This proves decay, not cancellation of the "
        "renormalized phases exp(2 pi i D_q/q), and supplies no Collatz "
        "trajectory theorem."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_canonical_incomplete_kernel_rows": rows,
        "algorithm": "exact modular Fermat quotients and Fraction error magnitudes; complex phases are stored only by their exact residue exponents",
        "complexity": "O(sum log q) modular exponentiation for replay; Fourier uniqueness and the harmonic bound prove the universal statements",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "prime_count": len(rows),
            "uniform_error_exactly_one_over_q": True,
            "one_missing_frequency_minimax_sharp": True,
            "unnormalized_canonical_prime_average_tends_to_zero": True,
            "decay_only_not_nontrivial_phase_cancellation": True,
            "renormalized_cross_prime_cancellation_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def first_primes(count: int) -> list[int]:
    values: list[int] = []
    candidate = 2
    while len(values) < count:
        if is_prime(candidate):
            values.append(candidate)
        candidate += 1
    return values


@lru_cache(maxsize=1)
def goldbach_qdiv_reflection_audit() -> dict[str, Any]:
    compatible_rows: list[tuple[int, int, list[int], int, int]] = []
    scanned_pairs = 0
    scanned_odd_pairs = 0
    odd_compatible_pairs = 0
    for prime in GOLDBACH_PRIMES:
        for exponent in range(prime, GOLDBACH_EXPONENT_LIMIT + 1, prime):
            scanned_pairs += 1
            coefficients = cyclic_binomial_coefficients(prime, exponent)
            shift = 1 - coefficients[0]
            compatible = shift > 0 and min(coefficients) + shift >= 0
            if exponent % 2:
                scanned_odd_pairs += 1
                odd_compatible_pairs += int(compatible)
            if compatible:
                compatible_rows.append(
                    (prime, exponent, coefficients, shift, prime * shift)
                )

    bounded = [row for row in compatible_rows if row[4] <= GOLDBACH_PREFIX_LIMIT]
    prefix = first_primes(max((row[4] for row in bounded), default=0))
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for prime, exponent, coefficients, shift, total in bounded:
        target = [value + shift for value in coefficients]
        actual = [0] * prime
        for value in prefix[:total]:
            actual[value % prime] += 1
        asymmetry = [actual[r] - actual[(-r) % prime] for r in range(prime)]
        witness = next((r for r in range(1, prime) if asymmetry[r]), None)
        target_symmetric = all(target[r] == target[(-r) % prime] for r in range(prime))
        excluded = target_symmetric and witness is not None and target != actual
        verified = (
            exponent % prime == 0
            and exponent % 2 == 0
            and target[0] == 1
            and sum(target) == total
            and sum(actual) == total
            and excluded
        )
        failures += int(not verified)
        transcript.update(
            f"{prime}:{exponent}:{shift}:{total}:"
            f"{','.join(map(str, target))}:{','.join(map(str, actual))}:"
            f"{','.join(map(str, asymmetry))}:{witness}:{int(verified)}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "prime_modulus_q": prime,
                "q_divisible_even_exponent_m": exponent,
                "cyclic_coefficients": coefficients,
                "forced_uniform_shift_t": shift,
                "forced_total_prime_count_T": total,
                "forced_symmetric_residue_counts": target,
                "actual_first_T_prime_residue_counts": actual,
                "actual_reflection_differences_N_r_minus_N_minus_r": asymmetry,
                "least_asymmetry_witness_residue": witness,
                "last_prime_in_prefix": prefix[total - 1],
                "forced_target_is_reflection_symmetric": target_symmetric,
                "unique_prime_prefix_excluded": excluded,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let q>=5 be prime, q divide m, and let c_r=sum_(j congruent r mod q) "
        "(-1)^j binom(m,j). Put t=1-c_0 and suppose t>0 and c_r+t>=0 "
        "for every r. Then m is even. For even m, c_(-r)=c_r, so the forced "
        "candidate vector N*_r=c_r+t is reflection-symmetric. Therefore any "
        "actual first-T-prime residue vector, T=qt, with N_r(T)!=N_(-r)(T) "
        "for some r cannot equal this tail."
    )
    proof = (
        "The binomial involution j->m-j gives c_(m-r)=(-1)^m c_r. Since "
        "q divides m, odd m would give c_(-r)=-c_r and c_0=0. Compatibility "
        "then has t=1 and forces every integer c_r into [-1,1], hence "
        "sum c_r^2<=q. Parseval for (1-X)^m modulo X^q-1 gives "
        "sum c_r^2=q^(-1)sum_a |1-zeta_q^a|^(2m). At a=(q-1)/2, the "
        "squared modulus is 4cos^2(pi/(2q))>=4cos^2(pi/10)=(5+sqrt(5))/2>3. "
        "Thus sum c_r^2>3^m/q>=3^q/q>q, since 3^q>q^2 for q>=5, a "
        "contradiction. Hence m is even, and the same involution proves "
        "reflection symmetry. TICKET-253's unique-prefix criterion then "
        "turns any exact actual asymmetry into an exclusion. The finite "
        "replay proves asymmetry only for the displayed bounded rows."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_q_divisible_prefix_exclusion_rows": rows,
        "algorithm": "exact cyclic binomial folding plus deterministic enumeration of the required prime prefixes and integer residue comparison",
        "complexity": "O(sum m) for the scan plus trial division through the largest bounded prefix; the parity and reflection theorem is algebraic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "scanned_q_divisible_pair_count": scanned_pairs,
            "scanned_odd_q_divisible_pair_count": scanned_odd_pairs,
            "compatible_q_divisible_pair_count": len(compatible_rows),
            "odd_q_divisible_compatible_pair_count": odd_compatible_pairs,
            "odd_q_divisible_compatibility_impossible_proved": True,
            "bounded_prefix_limit_T": GOLDBACH_PREFIX_LIMIT,
            "bounded_prefix_certificate_count": len(rows),
            "all_bounded_prefixes_excluded": bool(rows) and failures == 0,
            "all_q_divisible_compatible_tails_excluded": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures + odd_compatible_pairs,
    }


def surviving_twist_transform(u: int, v: int) -> tuple[int, int]:
    return -u - 2 * v, u + v


def inverse_surviving_twist_transform(u: int, v: int) -> tuple[int, int]:
    return u + 2 * v, -u - v


@lru_cache(maxsize=1)
def twin_gl2_survivor_audit() -> dict[str, Any]:
    units = unit_powers_seventeen()
    transcript = hashlib.sha256()
    failures = 0
    coefficient_one_points: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    samples = {(-7, 3), (-2, -1), (-1, 1), (0, 0), (1, 0), (2, -3), (5, 8)}
    case_count = 0
    for u in range(-TWIN_BOX_RADIUS, TWIN_BOX_RADIUS + 1):
        for v in range(-TWIN_BOX_RADIUS, TWIN_BOX_RADIUS + 1):
            case_count += 1
            transformed_u, transformed_v = surviving_twist_transform(u, v)
            recovered = inverse_surviving_twist_transform(
                transformed_u, transformed_v
            )
            a1, b1 = quadratic_multiply(units[1], quadratic_power((u, v), 17))
            a16, b16 = quadratic_multiply(
                units[16], quadratic_power((transformed_u, transformed_v), 17)
            )
            reduced_y_1 = -(u * u - 2 * v * v)
            reduced_y_16 = transformed_u**2 - 2 * transformed_v**2
            verified = (
                recovered == (u, v)
                and a16 == -a1
                and b16 == b1
                and reduced_y_16 == reduced_y_1
            )
            failures += int(not verified)
            transcript.update(
                f"{u}:{v}:{transformed_u}:{transformed_v}:{a1}:{b1}:"
                f"{a16}:{b16}:{reduced_y_1}:{reduced_y_16}:{int(verified)}\n".encode(
                    "ascii"
                )
            )
            row = {
                "u": u,
                "v": v,
                "transformed_u": transformed_u,
                "transformed_v": transformed_v,
                "A_1_u_v": a1,
                "B_1_u_v": b1,
                "A_16_transformed": a16,
                "B_16_transformed": b16,
                "reduced_y": reduced_y_1,
                "identities_verified": verified,
            }
            if (u, v) in samples:
                sample_rows.append(row)
            if b1 == 1:
                coefficient_one_points.append(
                    {
                        **row,
                        "negative_norm_condition": reduced_y_1 > 0,
                        "admissible_absolute_branch": b1 == 1
                        and reduced_y_1 > 0,
                    }
                )

    theorem = (
        "Let epsilon=1+sqrt(2), define epsilon^j(u+v sqrt(2))^17="
        "A_j(u,v)+B_j(u,v)sqrt(2), and set T(u,v)=(-u-2v,u+v). Then "
        "T is in GL_2(Z), B_16(T(u,v))=B_1(u,v), A_16(T(u,v))=-A_1(u,v), "
        "and N(T(u,v))=-N(u,v). Consequently the admissible points on the "
        "two TICKET-255 surviving twists j=1,16 are in bijection with the "
        "single absolute branch B_1(u,v)=1 and -(u^2-2v^2)>0; the associated "
        "x is |A_1(u,v)|."
    )
    proof = (
        "The matrix of T is [[-1,-2],[1,1]], has determinant one, and inverse "
        "[[1,2],[-1,-1]]. If alpha=u+v sqrt(2), then T(alpha)="
        "epsilon^(-1) conjugate(alpha). Since conjugate(epsilon)="
        "-epsilon^(-1), epsilon^16 T(alpha)^17=-conjugate(epsilon alpha^17), "
        "which proves the A/B identities. Norm(epsilon)=-1 proves the norm "
        "identity and preservation of reduced y. A positive-A point on twist "
        "1 stays in the positive sign branch; a negative-A point maps to a "
        "positive-A twist-16 point, and the inverse handles the converse. If "
        "B_1=1 and -N(alpha)>0, then A_1^2-2=(-N(alpha))^17>0, so A_1 is "
        "nonzero and |A_1| is valid. This reduces two equations to one but "
        "does not prove the remaining branch has no integral point."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "transformation_matrix": [[-1, -2], [1, 1]],
        "inverse_transformation_matrix": [[1, 2], [-1, -1]],
        "determinant": 1,
        "exact_sample_rows": sample_rows,
        "finite_box_audit": {
            "coordinate_radius": TWIN_BOX_RADIUS,
            "exact_grid_case_count": case_count,
            "coefficient_one_point_count": len(coefficient_one_points),
            "admissible_absolute_branch_point_count": sum(
                point["admissible_absolute_branch"]
                for point in coefficient_one_points
            ),
            "coefficient_one_points": coefficient_one_points,
        },
        "algorithm": "exact integer quadratic-ring exponentiation and GL2 forward/inverse replay",
        "complexity": "O(R^2 log 17) integer-ring multiplications for radius R; the all-integer bijection is algebraic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "two_surviving_twists_gl2_equivalent": True,
            "independent_surviving_branch_count": 1,
            "single_absolute_branch_globally_solved": False,
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
        {"id": f"{code}-T255", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T256", "label": theorem_name, "status": "proved"},
        {
            "id": f"{code}-CERT256",
            "label": f"{theorem_name}ExactReplay",
            "status": "computed_finite",
        },
        {"id": f"{code}-REJECT256", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN256", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T255", f"{code}-T256"],
        [f"{code}-T256", f"{code}-CERT256"],
        [f"{code}-T256", f"{code}-REJECT256"],
        [f"{code}-T256", f"{code}-OPEN256"],
    ]
    return {
        "nodes": nodes,
        "edges": edges,
        "resolution_path": [f"{code}-T255", f"{code}-T256", f"{code}-OPEN256"],
        "acyclic": True,
    }


def section(
    problem_id: str,
    code: str,
    theorem_name: str,
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
        "ticket_id": f"{code}-TICKET-256",
        "theorem_name": theorem_name,
        "declared_proposition": computation["theorem"],
        "mathematical_argument": computation["proof"],
        "result_classification": "partial_theorem",
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
    riemann = riemann_cesaro_lag_audit()
    collatz = collatz_sharp_incomplete_kernel_audit()
    goldbach = goldbach_qdiv_reflection_audit()
    twin = twin_gl2_survivor_audit()
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "ToeplitzPacketCesaroLagPartialSumCriterion",
            riemann,
            "treating nonnegative symmetric lag partial sums as necessary for nonnegative Dirichlet-packet energies",
            ["direct estimates of the actual Guinand-Weil lag partial sums"],
            "the exact Cesaro transfer from scalar lag partial sums to every packet size",
            "ActualWeilSymmetricLagPartialSumsHaveUniformLowerBound",
            "StrictDiagonalDominanceNecessityNoGo",
            "NonnegativeLagPartialSumsAreNecessaryForPacketPositivity",
            "The transfer is exact, but no lower bound is proved for the actual Guinand-Weil lag partial sums, so no zero-free conclusion follows.",
            "No RH proof or disproof; the packet aggregate is reduced to one explicit scalar partial-sum frontier.",
            f"{len(riemann['exact_packet_cesaro_rows'])} rational rows replay one necessity counterexample; the identity itself holds for every real lag sequence.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "SharpIncompleteKernelErrorAndDecayOnlyPrimeAverage",
            collatz,
            "counting decay of an unnormalized O(1/q) error average as arithmetic cross-prime phase cancellation",
            ["renormalized canonical phase cancellation for the fixed bases 2 and 3"],
            "the minimax-sharp one-frequency omission and its exact canonical residue phase",
            "RenormalizedCanonicalSlopePhasesHaveNontrivialCrossPrimeCancellation",
            "IncompleteAdditiveCharacterExactRecoveryNoGo",
            "UnnormalizedCrossPrimeDecayImpliesRenormalizedPhaseCancellation",
            "The exact 1/q error is optimal and its average vanishes trivially; no cancellation is proved after multiplying by q, and no Collatz orbit is controlled.",
            "No Collatz proof or counterexample; controlled error is achieved but the claimed cross-prime cancellation is shown to be decay-only.",
            f"{len(collatz['exact_canonical_incomplete_kernel_rows'])} exact modular rows store phases by residue exponent; no floating complex value is used.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "QDivisibleReflectionAsymmetryPrimePrefixExclusion",
            goldbach,
            "retaining odd q-divisible compatible cyclotomic tails",
            ["even q-divisible compatible prefixes above the exact replay limit"],
            "the parity obstruction plus the exact reflection-asymmetry prefix test",
            "EveryQDivisibleCompatibleEvenTailHasPrimePrefixReflectionAsymmetry",
            "OddCyclotomicReflectionPrimePrefixExclusion",
            "OddQDivisibleCompatibleCyclotomicTailExists",
            "Odd q-divisible compatibility is ruled out, but the universal actual-prefix asymmetry needed for every even compatible exponent remains unproved.",
            "No strong Goldbach proof or counterexample; one infinite parity theorem, one conditional prefix exclusion, and two bounded certificates.",
            f"{goldbach['aggregate']['scanned_q_divisible_pair_count']} q-divisible pairs were scanned through m={GOLDBACH_EXPONENT_LIMIT}; only {len(goldbach['exact_q_divisible_prefix_exclusion_rows'])} rows with T<={GOLDBACH_PREFIX_LIMIT} were enumerated as prime prefixes.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "SurvivingTwistGL2EquivalenceAndSingleAbsoluteBranchReduction",
            twin,
            "treating the two surviving exponent-17 unit twists as independent global Thue branches",
            ["global integral-point exclusion on the remaining absolute coefficient-one branch"],
            "the determinant-one conjugation-unit bijection reducing two sign branches to one equation",
            "SingleCoefficientOneBranchHasNoNegativeNormIntegralPoint",
            "ThreePrimeLocalObstructionReducesSeventeenTwistsToTwo",
            "TwoSurvivingUnitTwistsAreIndependentIntegralPointProblems",
            "The GL2 bijection halves the global branch count but does not exclude a negative-norm integral point of B_1=1, so exponent 17 and twin primes remain open.",
            "No twin-prime proof or counterexample; the two surviving exponent-17 branches are proved equivalent and reduced to one absolute branch.",
            f"{twin['finite_box_audit']['exact_grid_case_count']} exact grid points replay the all-integer identities; absence of an admissible point in that box is not an infinite exclusion.",
        ),
    }
    total_failures = sum(
        item["reproducible_computation"]["failure_count"]
        for item in sections.values()
    )
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureCesaroKernelQDivGL2Audit",
            "summary": "TICKET-256 proves four project-local partial theorems: a packet-Cesaro identity, a sharp incomplete kernel, a q-divisible Goldbach reflection obstruction, and a GL2 reduction of two Thue survivors to one; every parent conjecture remains open.",
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
                "collatz_fixed_representative_context": "https://arxiv.org/abs/1104.3909",
                "goldbach_major_arcs": "https://arxiv.org/abs/1205.5252",
                "twin_prime_parity": "https://arxiv.org/abs/1407.4897",
            },
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 4,
                "exact_no_go_count": 0,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "twin_prime",
                "stagnated_problem_count": 0,
                "riemann_packet_case_count": len(
                    riemann["exact_packet_cesaro_rows"]
                ),
                "collatz_prime_case_count": len(
                    collatz["exact_canonical_incomplete_kernel_rows"]
                ),
                "goldbach_q_divisible_scan_count": goldbach["aggregate"][
                    "scanned_q_divisible_pair_count"
                ],
                "goldbach_bounded_certificate_count": len(
                    goldbach["exact_q_divisible_prefix_exclusion_rows"]
                ),
                "twin_exact_grid_case_count": twin["finite_box_audit"][
                    "exact_grid_case_count"
                ],
                "twin_independent_surviving_branch_count": twin["aggregate"][
                    "independent_surviving_branch_count"
                ],
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
                "generator_failure_count": item["reproducible_computation"][
                    "failure_count"
                ],
                "focused_tests_required": True,
                "remote_ci_status": "tracked_by_commit_workflow",
            },
        }
    return {
        "schema": "primeproject.four-problem-research-state.v1",
        "ticket": 256,
        "parent_ticket": 255,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "twin_prime",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    write_json(
        ROOT / "data/open-problem/ticket256-cesaro-kernel-qdiv-gl2.json", audit
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-256-cesaro-lag-criterion.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-256-sharp-incomplete-kernel.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-256-qdiv-reflection-exclusion.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-256-gl2-survivor-reduction.json",
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
