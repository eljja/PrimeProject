from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
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
from scripts.ticket254_diagonal_weighted_reflection_thue import (
    fraction_record,
    is_prime,
    quadratic_multiply,
    quadratic_power,
    unit_powers_seventeen,
    write_json,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket255-aggregate-incomplete-odd-local.v1"
GENERATED_AT = "2026-08-29T18:10:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "aggregate_incomplete_odd_local_audit"

RIEMANN_BLOCK_DIMENSIONS = (3, 5, 7, 9, 15, 31, 63, 127)
COLLATZ_PRIMES = (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
GOLDBACH_PRIMES = (5, 7, 11, 13, 17, 19)
GOLDBACH_ODD_EXPONENT_LIMIT = 160
GOLDBACH_REPLAY_PREFIX_LIMIT = 50_000
TWIN_LOCAL_PRIMES = (103, 137, 409)
TWIN_EXPECTED_BAD = {
    103: (0, 3, 6, 7, 8, 9, 10, 11, 14),
    137: (0, 4, 5, 7, 8, 9, 10, 12, 13),
    409: (0, 2, 15),
}


@lru_cache(maxsize=1)
def riemann_strict_dominance_no_go_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for dimension in RIEMANN_BLOCK_DIMENSIONS:
        diagonal = Fraction(1) + Fraction(1, dimension)
        off_diagonal = Fraction(1)
        orthogonal_eigenvalue = Fraction(1, dimension)
        packet_eigenvalue = Fraction(dimension) + Fraction(1, dimension)
        off_diagonal_row_sum = Fraction(dimension - 1)
        strictly_dominant = diagonal > off_diagonal_row_sum
        verified = (
            orthogonal_eigenvalue > 0
            and packet_eigenvalue > 0
            and not strictly_dominant
            and diagonal + (dimension - 1) * off_diagonal == packet_eigenvalue
        )
        failures += int(not verified)
        transcript.update(
            f"{dimension}:{diagonal}:{off_diagonal}:{off_diagonal_row_sum}:"
            f"{orthogonal_eigenvalue}:{packet_eigenvalue}:{int(verified)}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "block_dimension_L": dimension,
                "diagonal_entry": fraction_record(diagonal),
                "common_off_diagonal_entry": fraction_record(off_diagonal),
                "absolute_off_diagonal_row_sum": fraction_record(
                    off_diagonal_row_sum
                ),
                "strictly_diagonally_dominant": strictly_dominant,
                "orthogonal_complement_eigenvalue": fraction_record(
                    orthogonal_eigenvalue
                ),
                "normalized_dirichlet_packet_energy": fraction_record(
                    packet_eigenvalue
                ),
                "positive_definite": True,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For every integer L>=3, let J_L be the all-ones matrix and set "
        "A_L=J_L+L^(-1)I_L. Then A_L is positive definite and the normalized "
        "all-ones packet d_L has <d_L,A_L d_L>=L+L^(-1)>0, but A_L is not "
        "strictly diagonally dominant: 1+L^(-1)<=L-1. Hence strict diagonal "
        "dominance is not a necessary condition for positive Dirichlet-packet "
        "energy, even among positive-definite blocks."
    )
    proof = (
        "J_L has eigenvalue L on the all-ones line and zero on its orthogonal "
        "complement. Therefore A_L has eigenvalues L+1/L and 1/L and is "
        "positive definite. Every diagonal entry is 1+1/L, while the sum of "
        "absolute off-diagonal entries in each row is L-1; the displayed "
        "inequality holds for L>=3. The packet energy is its eigenvalue "
        "L+1/L. This disproves necessity only; it neither computes actual "
        "Guinand-Weil blocks nor says strict dominance could not be a "
        "sufficient certificate for them."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_positive_block_rows": rows,
        "algorithm": "exact Fraction evaluation of the two eigenspaces and row sums of J_L+I_L/L",
        "complexity": "O(number of replay dimensions); the all-L statement is algebraic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "positive_definite_for_every_L_at_least_three": True,
            "positive_dirichlet_packet_energy_for_every_L_at_least_three": True,
            "strict_diagonal_dominance_necessary": False,
            "actual_weil_form_analyzed": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


def incomplete_frequency_families(prime: int) -> dict[str, tuple[int, ...]]:
    quadratic_residues = tuple(sorted({(value * value) % prime for value in range(prime)}))
    return {
        "nonzero_frequencies": tuple(range(1, prime)),
        "lower_half": tuple(range((prime + 1) // 2)),
        "quadratic_residues": quadratic_residues,
        "zero_frequency_only": (0,),
    }


@lru_cache(maxsize=1)
def collatz_incomplete_recovery_no_go_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for prime in COLLATZ_PRIMES:
        for family, support in incomplete_frequency_families(prime).items():
            support_set = set(support)
            missing_frequency = next(
                frequency for frequency in range(prime) if frequency not in support_set
            )
            target_coefficient = Fraction(1, prime)
            forced_coefficient = Fraction(0)
            verified = (
                len(support) < prime
                and missing_frequency not in support_set
                and target_coefficient != forced_coefficient
            )
            failures += int(not verified)
            transcript.update(
                f"{prime}:{family}:{','.join(map(str, support))}:"
                f"{missing_frequency}:{target_coefficient}:{forced_coefficient}:"
                f"{int(verified)}\n".encode("ascii")
            )
            rows.append(
                {
                    "prime_q": prime,
                    "support_family": family,
                    "frequency_support_H": list(support),
                    "support_size": len(support),
                    "missing_frequency_h0": missing_frequency,
                    "delta_zero_fourier_coefficient_at_h0": fraction_record(
                        target_coefficient
                    ),
                    "any_H_supported_sum_coefficient_at_h0": fraction_record(
                        forced_coefficient
                    ),
                    "exact_pointwise_recovery_impossible": True,
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "Let q be prime and let H be a proper subset of F_q. There are no "
        "complex coefficients (a_h)_(h in H) such that 1_(D=0)="
        "sum_(h in H) a_h exp(2 pi i hD/q) for every D in F_q. Thus signed "
        "weights do not permit exact pointwise recovery of the slope incidence "
        "from genuinely incomplete additive-character support."
    )
    proof = (
        "The q additive characters are an orthonormal basis for functions on "
        "F_q. The Fourier coefficient of the point mass 1_(D=0) at every "
        "frequency h is exactly 1/q. Choose h0 outside H. Every linear "
        "combination supported on H has Fourier coefficient zero at h0, "
        "contradicting 1/q. The argument allows arbitrary signed or complex "
        "coefficients. Approximate or one-sided recovery on only the canonical "
        "residues is not ruled out."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_missing_fourier_coefficient_rows": rows,
        "algorithm": "exact support-complement selection and rational Fourier-coefficient comparison",
        "complexity": "O(sum q) for the finite replay; Fourier-basis uniqueness proves the universal statement",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "prime_count": len(COLLATZ_PRIMES),
            "support_family_count": 4,
            "exact_replay_case_count": len(rows),
            "proper_incomplete_support_exact_recovery_possible": False,
            "approximate_or_canonical_only_recovery_rejected": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=None)
def kth_prime_in_residue(
    prime_modulus: int, residue: int, occurrence: int
) -> tuple[int, int]:
    hits = 0
    prime_index = 0
    value = 2
    while hits < occurrence:
        if is_prime(value):
            prime_index += 1
            if value % prime_modulus == residue:
                hits += 1
                if hits == occurrence:
                    return value, prime_index
        value += 1
    raise AssertionError("unreachable")


@lru_cache(maxsize=None)
def prefix_residue_count(prime_modulus: int, residue: int, prefix_length: int) -> int:
    count = 0
    prime_index = 0
    value = 2
    while prime_index < prefix_length:
        if is_prime(value):
            prime_index += 1
            if value % prime_modulus == residue:
                count += 1
        value += 1
    return count


@lru_cache(maxsize=1)
def goldbach_odd_reflection_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    scanned_pairs = 0
    compatible_nondivisible_pairs = 0
    skipped_large_prefix_pairs = 0
    for prime in GOLDBACH_PRIMES:
        for exponent in range(1, GOLDBACH_ODD_EXPONENT_LIMIT + 1, 2):
            scanned_pairs += 1
            coefficients = cyclic_binomial_coefficients(prime, exponent)
            shift = 1 - coefficients[0]
            compatible = coefficients[0] - min(coefficients) <= 1 and shift > 0
            residue = exponent % prime
            if not compatible or residue == 0:
                continue
            compatible_nondivisible_pairs += 1
            total = prime * shift
            if total > GOLDBACH_REPLAY_PREFIX_LIMIT:
                skipped_large_prefix_pairs += 1
                continue
            forced_count = 2 * shift - 1
            kth_prime, kth_global_index = kth_prime_in_residue(
                prime, residue, forced_count
            )
            actual_count = prefix_residue_count(prime, residue, total)
            reflection_identity = coefficients[residue] == -coefficients[0]
            threshold_met = total < kth_global_index
            excluded = (
                reflection_identity
                and coefficients[residue] + shift == forced_count
                and actual_count < forced_count
                and threshold_met
            )
            failures += int(not excluded)
            transcript.update(
                f"{prime}:{exponent}:{coefficients[0]}:{shift}:{total}:{residue}:"
                f"{coefficients[residue]}:{forced_count}:{actual_count}:{kth_prime}:"
                f"{kth_global_index}:{int(excluded)}\n".encode("ascii")
            )
            rows.append(
                {
                    "prime_modulus_q": prime,
                    "odd_cyclotomic_exponent_m": exponent,
                    "reflected_nonzero_residue_m_mod_q": residue,
                    "cyclic_coefficient_c0": coefficients[0],
                    "coefficient_at_m_mod_q": coefficients[residue],
                    "odd_reflection_identity_c_m_equals_minus_c0": reflection_identity,
                    "forced_uniform_shift_t": shift,
                    "forced_total_prime_count_T": total,
                    "forced_count_at_m_mod_q_2t_minus_1": forced_count,
                    "actual_first_T_prime_count_at_m_mod_q": actual_count,
                    "forced_count_th_residue_prime": kth_prime,
                    "global_index_lambda_of_forced_count_th_residue_prime": kth_global_index,
                    "threshold_T_strictly_below_lambda": threshold_met,
                    "unique_prime_prefix_excluded": excluded,
                    "certificate_verified": excluded,
                }
            )

    theorem = (
        "Let q>=5 be prime and m be odd with q not dividing m. Put c_r="
        "sum_(0<=j<=m,j congruent r mod q)(-1)^j binom(m,j). Suppose "
        "t=1-c_0>0 and c_r+t>=0 for every r, and put T=qt. The unique "
        "candidate prime-prefix counts force N*_(m mod q)=2t-1. If "
        "T<lambda_q(m mod q,2t-1), where lambda_q(r,k) is the global prime "
        "index of the kth prime congruent to r mod q, then the cyclotomic tail "
        "cannot equal the actual first-T-prime residue vector."
    )
    proof = (
        "For a_j=(-1)^j binom(m,j), the involution j->m-j gives "
        "a_(m-j)=-a_j because m is odd. Folding modulo q yields "
        "c_(m-r)=-c_r. At r=0, c_(m mod q)=-c_0, so the compatible shifted "
        "count there is -c_0+(1-c_0)=1-2c_0=2t-1. If T is strictly below "
        "the global index of the (2t-1)st prime in that class, the actual "
        "prefix has at most 2t-2 such primes. This contradicts the TICKET-253 "
        "unique-prefix criterion. No claim is made when q divides m or the "
        "strict threshold is unavailable."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_odd_reflection_prefix_exclusion_rows": rows,
        "algorithm": "exact cyclic binomial folding and deterministic prime enumeration to the required residue occurrence",
        "complexity": "O(sum m + sum lambda sqrt(p_lambda)) trial divisions for the bounded replay; the conditional reflection theorem is algebraic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "scanned_odd_pair_count": scanned_pairs,
            "compatible_non_q_divisible_odd_pair_count": compatible_nondivisible_pairs,
            "finite_prefix_certificate_count": len(rows),
            "skipped_large_prefix_pair_count": skipped_large_prefix_pairs,
            "all_replayed_pairs_excluded": bool(rows) and failures == 0,
            "odd_reflection_identity_proved": True,
            "q_divisible_compatible_tails_excluded": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


def least_square_root_two(prime: int) -> int:
    return next(value for value in range(prime) if value * value % prime == 2)


def split_thue_solution_counts(prime: int) -> tuple[int, list[int]]:
    square_root = least_square_root_two(prime)
    power_counts = Counter(pow(value, 17, prime) for value in range(prime))
    epsilon_plus = (1 + square_root) % prime
    epsilon_minus = (1 - square_root) % prime
    counts: list[int] = []
    for twist in range(17):
        plus_factor = pow(epsilon_plus, twist, prime)
        minus_factor = pow(epsilon_minus, twist, prime)
        minus_counts: Counter[int] = Counter()
        for power_value, multiplicity in power_counts.items():
            minus_counts[(minus_factor * power_value) % prime] += multiplicity
        solution_count = 0
        for power_value, multiplicity in power_counts.items():
            plus_value = (plus_factor * power_value) % prime
            solution_count += multiplicity * minus_counts[
                (plus_value - 2 * square_root) % prime
            ]
        counts.append(solution_count)
    return square_root, counts


@lru_cache(maxsize=1)
def twin_three_prime_local_obstruction_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    survivors = set(range(17))
    for prime in TWIN_LOCAL_PRIMES:
        square_root, solution_counts = split_thue_solution_counts(prime)
        soluble = tuple(
            twist for twist, count in enumerate(solution_counts) if count > 0
        )
        obstructed = tuple(
            twist for twist, count in enumerate(solution_counts) if count == 0
        )
        survivors.intersection_update(soluble)
        verified = (
            pow(square_root, 2, prime) == 2
            and obstructed == TWIN_EXPECTED_BAD[prime]
        )
        failures += int(not verified)
        transcript.update(
            f"{prime}:{square_root}:{','.join(map(str, solution_counts))}:"
            f"{','.join(map(str, obstructed))}:{','.join(map(str, sorted(survivors)))}:"
            f"{int(verified)}\n".encode("ascii")
        )
        rows.append(
            {
                "split_prime_p": prime,
                "least_square_root_s_of_two_mod_p": square_root,
                "solution_counts_by_unit_twist_j": solution_counts,
                "locally_soluble_twists": list(soluble),
                "locally_obstructed_twists": list(obstructed),
                "cumulative_surviving_twists": sorted(survivors),
                "represented_uv_residue_pairs_per_twist": prime * prime,
                "certificate_verified": verified,
            }
        )

    witnesses: list[dict[str, Any]] = []
    for twist, u, v in ((1, 1, 0), (16, -1, 1)):
        a_value, b_value = quadratic_multiply(
            unit_powers_seventeen()[twist], quadratic_power((u, v), 17)
        )
        reduced_y = (-1 if twist % 2 else 1) * (u * u - 2 * v * v)
        verified = b_value == 1 and reduced_y == -1
        failures += int(not verified)
        transcript.update(
            f"witness:{twist}:{u}:{v}:{a_value}:{b_value}:{reduced_y}:"
            f"{int(verified)}\n".encode("ascii")
        )
        witnesses.append(
            {
                "unit_twist_j": twist,
                "u": u,
                "v": v,
                "A_j_u_v": a_value,
                "B_j_u_v": b_value,
                "reduced_y": reduced_y,
                "admissible_positive_point": a_value > 0 and reduced_y > 0,
                "certificate_verified": verified,
            }
        )
    cover_verified = survivors == {1, 16}
    failures += int(not cover_verified)

    theorem = (
        "For the seventeen TICKET-254 equations B_j(u,v)=1, reduction modulo "
        "the split primes 103, 137, and 409 excludes every twist except "
        "j=1 and j=16. Precisely, their obstructed twist sets are "
        "{0,3,6,7,8,9,10,11,14}, {0,4,5,7,8,9,10,12,13}, and {0,2,15}; "
        "the intersection of the three locally soluble sets is {1,16}. "
        "Therefore every positive solution of x^2-2=y^17 must arise from one "
        "of those two twists. Coefficient-one congruences alone cannot remove "
        "the survivors, since (j,u,v)=(1,1,0) and (16,-1,1) are exact integer "
        "B_j=1 points, both inadmissible with reduced y=-1."
    )
    proof = (
        "For each listed p choose s with s^2=2 mod p. The split map "
        "u+v sqrt(2)->(u+sv,u-sv) is a bijection F_p[sqrt(2)] to F_p^2. "
        "Writing epsilon_+=1+s and epsilon_-=1-s, B_j(u,v)=1 is equivalent "
        "to epsilon_+^j z_+^17-epsilon_-^j z_-^17=2s. Exact convolution "
        "of the seventeenth-power multiplicities gives the recorded solution "
        "counts and zero sets; their union covers fifteen twists. The two "
        "displayed integer substitutions directly give B_j=1 and reduced "
        "y=-1, proving both survival and inadmissibility. The theorem does not "
        "exclude admissible integral points on j=1 or j=16."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_split_prime_local_obstruction_rows": rows,
        "surviving_twist_integer_witnesses": witnesses,
        "algorithm": "exact split-ring bijection and Counter convolution of seventeenth-power residues",
        "complexity": "O(17 sum p) dictionary operations after O(sum p) power tabulation",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "local_prime_count": len(TWIN_LOCAL_PRIMES),
            "represented_uv_twist_case_count": 17
            * sum(prime * prime for prime in TWIN_LOCAL_PRIMES),
            "locally_excluded_twist_count": 15,
            "surviving_twists": sorted(survivors),
            "three_prime_cover_verified": cover_verified,
            "coefficient_only_congruence_can_exclude_survivors": False,
            "surviving_twists_globally_solved": False,
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
    certificate_dependency: bool = False,
) -> dict[str, Any]:
    nodes = [
        {"id": f"{code}-T254", "label": prior_name, "status": "proved"},
        {
            "id": f"{code}-CERT255",
            "label": f"{theorem_name}ExactReplay",
            "status": "computed_finite",
        },
        {"id": f"{code}-T255", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-REJECT255", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN255", "label": open_name, "status": "open"},
    ]
    if certificate_dependency:
        edges = [
            [f"{code}-T254", f"{code}-CERT255"],
            [f"{code}-CERT255", f"{code}-T255"],
        ]
    else:
        edges = [
            [f"{code}-T254", f"{code}-T255"],
            [f"{code}-T255", f"{code}-CERT255"],
        ]
    edges.extend(
        [
            [f"{code}-T255", f"{code}-REJECT255"],
            [f"{code}-T255", f"{code}-OPEN255"],
        ]
    )
    return {
        "nodes": nodes,
        "edges": edges,
        "resolution_path": [f"{code}-T254", f"{code}-T255", f"{code}-OPEN255"],
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
    certificate_dependency: bool = False,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": f"{code}-TICKET-255",
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
            code,
            prior_name,
            theorem_name,
            rejected_name,
            next_lemma,
            certificate_dependency,
        ),
        "claim_boundary": claim_boundary,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_strict_dominance_no_go_audit()
    collatz = collatz_incomplete_recovery_no_go_audit()
    goldbach = goldbach_odd_reflection_audit()
    twin = twin_three_prime_local_obstruction_audit()
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "StrictDiagonalDominanceNecessityNoGo",
            "exact_no_go",
            riemann,
            "treating uniform strict diagonal dominance as a necessary condition for positive Dirichlet-packet energy",
            ["strict diagonal dominance as a sufficient certificate for actual Weil blocks"],
            "direct aggregate packet Rayleigh control rather than row-by-row dominance",
            "ActualWeilDirichletPacketAggregateRowSumHasRequiredLowerBound",
            "PositiveDiagonalDirichletPacketDominationNoGo",
            "StrictDiagonalDominanceIsNecessaryForDirichletPacketPositivity",
            "The matrices are abstract positive-definite blocks, not actual Guinand-Weil finite sections; no RH implication is proved.",
            "No RH proof or disproof; strict diagonal dominance is proved unnecessary for the packet-positivity subgoal.",
            f"{len(riemann['exact_positive_block_rows'])} exact rational blocks replay the all-L construction.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "IncompleteAdditiveCharacterExactRecoveryNoGo",
            "exact_no_go",
            collatz,
            "requiring exact pointwise slope-incidence recovery from a proper subset of additive characters, even with signed complex weights",
            ["approximate, one-sided, or canonical-residue-only incomplete kernels"],
            "controlled recovery error together with genuinely signed cross-prime cancellation",
            "SignedIncompleteSlopeKernelHasControlledCanonicalErrorAndCrossPrimeCancellation",
            "NonnegativeCrossPrimeCompleteDetectorAverageNoGo",
            "ProperIncompleteCharacterSupportCanExactlyRecoverPointMass",
            "Fourier uniqueness blocks exact recovery on all residues only; approximation or control on the canonical Fermat-quotient residues remains open.",
            "No Collatz proof or counterexample; one exact no-go for incomplete-support exact pointwise recovery.",
            f"{len(collatz['exact_missing_fourier_coefficient_rows'])} exact missing-coefficient certificates replay four support families over twelve primes.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "OddCyclotomicReflectionPrimePrefixExclusion",
            "partial_theorem",
            goldbach,
            "treating odd compatible non-q-divisible cyclotomic tails as having no exact reflection-based prime-prefix obstruction",
            [
                "odd rows above the finite replay limit",
                "compatible exponents divisible by q",
                "odd rows where the strict lambda threshold fails",
            ],
            "the odd reflection forced count 2t-1 and its exact residue-prime index threshold",
            "QDivisibleCompatibleTailPrimePrefixExclusion",
            "EvenCyclotomicReflectionPrimePrefixExclusion",
            "OddCompatibleTailsHaveNoReflectionPrefixConstraint",
            "The theorem is conditional on a strict prime-index threshold; only four bounded rows are enumerated and q-divisible exponents remain open.",
            "No strong Goldbach proof or counterexample; one universal conditional odd-reflection exclusion and four finite certificates.",
            f"{goldbach['aggregate']['scanned_odd_pair_count']} odd pairs scanned; {len(goldbach['exact_odd_reflection_prefix_exclusion_rows'])} bounded compatible rows have exact prime-prefix certificates.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "ThreePrimeLocalObstructionReducesSeventeenTwistsToTwo",
            "partial_theorem",
            twin,
            "treating all seventeen exponent-17 unit twists as equally open after the Thue reduction",
            [
                "coefficient-one congruence sieves as a complete method for the two surviving twists",
                "global admissible integral-point exclusion for twists 1 and 16",
            ],
            "the exact split-prime cover eliminating fifteen twists and the real-sign obstruction still needed for two survivors",
            "TwoSurvivingUnitTwistsHaveNoAdmissibleIntegralPoint",
            "ExponentSeventeenUnitTwistedThueReduction",
            "AllSeventeenTwistsSurviveTheThreePrimeLocalSieve",
            "The local certificates eliminate fifteen twists only. Exact integer B_j=1 witnesses show coefficient-only congruences cannot eliminate twists 1 and 16, and no global admissible-point exclusion is proved.",
            "No twin-prime proof or counterexample; exponent 17 is reduced from seventeen global Thue cases to two.",
            f"Three exact split primes represent {twin['aggregate']['represented_uv_twist_case_count']} (u,v,j) residue cases and leave twists 1 and 16.",
            True,
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
            "theorem_name": "FourConjectureAggregateIncompleteOddLocalAudit",
            "summary": "TICKET-255 proves two exact route no-gos and two partial theorems, including a three-prime reduction of seventeen exponent-17 Thue twists to two; all parent conjectures remain open.",
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
                "deep_focus_problem": "twin_prime",
                "stagnated_problem_count": 0,
                "riemann_block_case_count": len(riemann["exact_positive_block_rows"]),
                "collatz_missing_coefficient_case_count": len(
                    collatz["exact_missing_fourier_coefficient_rows"]
                ),
                "goldbach_odd_reflection_certificate_count": len(
                    goldbach["exact_odd_reflection_prefix_exclusion_rows"]
                ),
                "twin_local_prime_count": len(
                    twin["exact_split_prime_local_obstruction_rows"]
                ),
                "twin_locally_excluded_twist_count": twin["aggregate"][
                    "locally_excluded_twist_count"
                ],
                "twin_surviving_twist_count": len(
                    twin["aggregate"]["surviving_twists"]
                ),
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
                "generator_failure_count": item["reproducible_computation"][
                    "failure_count"
                ],
                "focused_tests_required": True,
                "remote_ci_status": "tracked_by_commit_workflow",
            },
        }
    return {
        "schema": "primeproject.four-problem-research-state.v1",
        "ticket": 255,
        "parent_ticket": 254,
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
        ROOT / "data/open-problem/ticket255-aggregate-incomplete-odd-local.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-255-strict-dominance-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-255-incomplete-recovery-no-go.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-255-odd-reflection-exclusion.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-255-three-prime-local-obstruction.json",
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
