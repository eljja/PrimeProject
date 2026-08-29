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
SCHEMA = "primeproject.ticket253-density-character-prefix-lebesgue.v1"
GENERATED_AT = "2026-08-29T13:07:59+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "density_character_prefix_lebesgue_audit"

RIEMANN_PACKET_SIZES = tuple(2**power - 1 for power in range(3, 14))
COLLATZ_PRIMES = (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
GOLDBACH_COMPATIBLE_PAIRS = (
    (5, 8), (5, 9), (5, 10), (5, 11), (5, 12),
    (7, 12), (7, 13), (7, 14), (7, 15), (7, 16),
)
TWIN_EXPONENT_SCAN_LIMIT = 10_000
KATZ_PRATT_URL = "https://arxiv.org/abs/2507.12397v2"


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


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors.append(remaining)
    return factors


@lru_cache(maxsize=None)
def first_n_primes(count: int) -> tuple[int, ...]:
    if count <= 0:
        return ()
    limit = max(32, 20 * count)
    while True:
        sieve = bytearray(b"\x01") * (limit + 1)
        sieve[0:2] = b"\x00\x00"
        for prime in range(2, isqrt(limit) + 1):
            if sieve[prime]:
                start = prime * prime
                sieve[start : limit + 1 : prime] = b"\x00" * (
                    ((limit - start) // prime) + 1
                )
        primes = tuple(index for index, flag in enumerate(sieve) if flag)
        if len(primes) >= count:
            return primes[:count]
        limit *= 2


@lru_cache(maxsize=1)
def riemann_density_packet_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    density = Fraction(1, 3)
    for size in RIEMANN_PACKET_SIZES:
        selected = sum(
            1 for frequency in range(-size, size + 1)
            if frequency % 6 in {1, 5}
        )
        total = 2 * size + 1
        energy = Fraction(selected, total)
        error = abs(energy - density)
        discrepancy_numerator = abs(3 * selected - total)
        verified = discrepancy_numerator <= 3
        failures += int(not verified)
        transcript.update(
            f"{size}:{selected}:{total}:{energy}:{error}:{discrepancy_numerator}:{int(verified)}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "dirichlet_half_bandwidth_N": size,
                "frequency_count_2N_plus_1": total,
                "selected_residues_mod_6": [1, 5],
                "selected_frequency_count": selected,
                "exact_projection_energy": fraction_record(energy),
                "limiting_spectral_density": fraction_record(density),
                "exact_absolute_density_error": fraction_record(error),
                "integer_discrepancy_abs_3count_minus_total": discrepancy_numerator,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let e_n(x)=2^(-1/2)exp(pi i n x) on [-1,1] and let "
        "D_N=(2N+1)^(-1/2) sum_(|n|<=N)e_n. Then D_N is an even unit vector "
        "whose L2 mass outside every fixed neighborhood of zero tends to zero. "
        "For every symmetric S subset Z and its Fourier projection P_S, "
        "<P_S D_N,D_N>=#(S intersect [-N,N])/(2N+1). Consequently, if S has "
        "symmetric natural density d, the projection energy tends exactly to d. "
        "Positive spectral density therefore blocks the zero-energy escape of "
        "this canonical interior-concentrating packet family, while zero density "
        "recovers the TICKET-252 escape."
    )
    proof = (
        "Orthonormality gives norm one, evenness, and the displayed projection "
        "identity by counting coefficients. The Dirichlet-kernel formula gives "
        "|D_N(x)|^2=|sin((2N+1)pi x/2)/sin(pi x/2)|^2/(2(2N+1)). "
        "For epsilon<=|x|<=1 its integral is at most "
        "1/((2N+1)sin(pi epsilon/2)^2), hence the mass concentrates at zero. "
        "The density conclusion is now the definition of symmetric natural "
        "density. For the replay set S={n:n mod 6 is 1 or 5}, elementary "
        "residue counting gives density 1/3 and |3#S_N-(2N+1)|<=3."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_periodic_density_rows": rows,
        "algorithm": "exact integer residue counts and Fraction projection energies for normalized Dirichlet packets",
        "complexity": "O(sum N) direct replay operations; the density and concentration statements are analytic",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "dirichlet_packet_concentrates_at_interior_zero_proved": True,
            "projection_energy_equals_symmetric_frequency_density_proved": True,
            "positive_density_blocks_this_packet_escape_proved": True,
            "actual_weil_form_dominates_projection": False,
            "riemann_hypothesis_resolved": False,
        },
        "failure_count": failures,
    }


def fermat_quotient_mod_prime(base: int, prime: int) -> int:
    residue = pow(base, prime - 1, prime * prime)
    return ((residue - 1) // prime) % prime


def complete_nontrivial_linear_character_sum(prime: int, residue: int) -> int:
    return prime - 1 if residue % prime == 0 else -1


@lru_cache(maxsize=1)
def collatz_complete_character_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    canonical_hits = 0
    separated_hits = 0
    for prime in COLLATZ_PRIMES:
        u = fermat_quotient_mod_prime(2, prime)
        v = fermat_quotient_mod_prime(3, prime)
        slope_residue = (5 * u - 3 * v) % prime
        character_sum = complete_nontrivial_linear_character_sum(
            prime, slope_residue
        )
        full_average = Fraction(1 + character_sum, prime)
        slope_hit = slope_residue == 0
        origin = u == 0 and v == 0
        separated = slope_hit and not origin
        rational_wieferich = (
            pow(32, prime - 1, prime * prime)
            == pow(27, prime - 1, prime * prime)
        )
        verified = (
            full_average == int(slope_hit)
            and slope_hit == rational_wieferich
            and separated == (slope_hit and (u - v) % prime != 0)
        )
        canonical_hits += int(slope_hit)
        separated_hits += int(separated)
        failures += int(not verified)
        transcript.update(
            f"{prime}:{u}:{v}:{slope_residue}:{character_sum}:{full_average}:{int(origin)}:{int(separated)}:{int(verified)}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "prime_q": prime,
                "canonical_U_q": u,
                "canonical_V_q": v,
                "slope_residue_D_q": slope_residue,
                "complete_nontrivial_character_sum_exact_integer": character_sum,
                "full_orthogonality_average": fraction_record(full_average),
                "rational_wieferich_32_over_27": rational_wieferich,
                "origin_double_wieferich": origin,
                "separated_projective_slope_hit": separated,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For every prime q>5 and D in F_q, let "
        "C_q(D)=sum_(h=1)^(q-1) exp(2 pi i hD/q). Then C_q(D)=q-1 when "
        "D=0 and C_q(D)=-1 otherwise, so (1+C_q(D))/q=1_(D=0) exactly. "
        "For D_q=5F_q(2)-3F_q(3), subtracting the origin indicator gives the "
        "separated [3:5] detector. Thus the complete h-character sum proposed "
        "after TICKET-252 is not a softened statistic: pointwise cancellation "
        "is exactly equivalent to canonical slope avoidance. Generic complete "
        "character-sum bounds cannot supply new information without a separate "
        "cross-prime estimate that varies the arithmetic data."
    )
    proof = (
        "If D=0 every summand is one. If D is nonzero, multiplication by D "
        "permutes F_q^*, and the sum of all q additive characters is zero, so "
        "the nonzero-h sum is -1. Fermat-quotient additivity gives "
        "D_q=F_q(32)-F_q(27), hence D_q=0 exactly when "
        "32^(q-1)=27^(q-1) modulo q^2. On this line U_q-V_q=-2t, so removing "
        "U_q=V_q=0 is exactly the separated condition. The dichotomy also "
        "shows why a square-root bound for this complete sum would already "
        "assume the desired avoidance at every sufficiently large target prime."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_canonical_character_rows": rows,
        "algorithm": "exact modular exponentiation modulo q^2 plus the algebraic complete-linear-character dichotomy",
        "complexity": "O(sum log q) modular multiplications for replay rows; the character identity is algebraic for every prime q>5",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "complete_character_sum_is_exact_indicator_proved": True,
            "generic_pointwise_character_cancellation_route_rejected": True,
            "canonical_replay_slope_hit_count": canonical_hits,
            "canonical_replay_separated_hit_count": separated_hits,
            "cross_prime_distribution_controlled": False,
            "collatz_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def goldbach_prime_prefix_audit() -> dict[str, Any]:
    pair_data: list[tuple[int, int, list[int], int, list[int]]] = []
    maximum_total = 0
    for prime, exponent in GOLDBACH_COMPATIBLE_PAIRS:
        coefficients = cyclic_binomial_coefficients(prime, exponent)
        shift = 1 - coefficients[0]
        target = [value + shift for value in coefficients]
        total = prime * shift
        pair_data.append((prime, exponent, coefficients, shift, target))
        maximum_total = max(maximum_total, total)
    primes = first_n_primes(maximum_total)

    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    accidental_matches = 0
    for prime, exponent, coefficients, shift, target in pair_data:
        total = prime * shift
        prefix = primes[:total]
        actual = [0] * prime
        for value in prefix:
            actual[value % prime] += 1
        differences = [actual[index] - target[index] for index in range(prime)]
        l1 = sum(abs(value) for value in differences)
        linf = max(abs(value) for value in differences)
        first_mismatch = next(
            (index for index, value in enumerate(differences) if value), None
        )
        compatible = (
            coefficients[0] - min(coefficients) <= 1
            and min(target) >= 0
            and target[0] == 1
            and sum(target) == total
        )
        match = actual == target
        verified = compatible and sum(actual) == total and not match
        accidental_matches += int(match)
        failures += int(not verified)
        transcript.update(
            f"{prime}:{exponent}:{shift}:{total}:{','.join(map(str,target))}:{','.join(map(str,actual))}:{l1}:{linf}:{first_mismatch}:{int(verified)}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "prime_modulus_q": prime,
                "cyclotomic_exponent_m": exponent,
                "cyclic_coefficients_c": coefficients,
                "forced_uniform_shift_t": shift,
                "forced_total_prime_count_qt": total,
                "forced_prime_count_vector": target,
                "actual_first_qt_prime_residue_counts": actual,
                "difference_actual_minus_forced": differences,
                "l1_discrepancy": l1,
                "linfinity_discrepancy": linf,
                "first_mismatch_residue": first_mismatch,
                "actual_prefix_match": match,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let q>=5 be prime and let c be the cyclic coefficient vector of "
        "(1-X)^m modulo X^q-1. Suppose c is zero-residue compatible, and set "
        "t=1-c_0, N*=c+t, and T=qt. Then there exists X for which the actual prime-count vector N_r(X) "
        "has the cyclotomic centered nonzero Fourier data q(1-zeta_q^a)^m if "
        "and only if the residue-count vector of the first T primes is exactly "
        "N*. Equivalently one need test the unique prefix p_T<=X<p_(T+1); there "
        "is no free choice of X. Exact prefix computation rejects all ten "
        "selected compatible tails (q,m)=(5,8..12),(7,12..16)."
    )
    proof = (
        "TICKET-252 Fourier inversion gives N_r(X)=c_r+t and the prime-zero "
        "condition forces t=1-c_0. Summing gives pi(X)=qt=T. Prime counts are "
        "constant precisely between the T-th and (T+1)-st primes, so their "
        "residue vector is the vector of the first T primes. This proves both "
        "directions of the criterion. The ten finite rejections use a sieve to "
        "enumerate those exact prefixes and compare integer vectors; no claim "
        "is made for untested compatible pairs or all exponents."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_compatible_tail_prefix_rows": rows,
        "algorithm": "exact cyclic binomial folding, Eratosthenes prime-prefix enumeration, and integer residue-vector comparison",
        "complexity": "O(B log log B + sum T) bit operations for the finite replay; the unique-prefix criterion is exact for every compatible q,m",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "actual_realizability_iff_unique_prime_prefix_match_proved": True,
            "selected_compatible_tail_count": len(rows),
            "selected_compatible_tails_excluded": accidental_matches == 0,
            "accidental_prefix_match_count": accidental_matches,
            "maximum_prime_prefix_length": maximum_total,
            "all_compatible_tail_exponents_excluded": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "failure_count": failures,
    }


@lru_cache(maxsize=1)
def twin_lebesgue_nagell_audit() -> dict[str, Any]:
    admissible = tuple(
        exponent
        for exponent in range(17, 912)
        if is_prime(exponent) and exponent % 24 in {13, 17, 19, 23}
    )
    admissible_set = set(admissible)
    residue_counts = {
        str(residue): sum(exponent % 24 == residue for exponent in admissible)
        for residue in (13, 17, 19, 23)
    }
    failures = int(len(admissible) != 84)
    transcript = hashlib.sha256()
    rows: list[dict[str, Any]] = []
    for index, exponent in enumerate(admissible, start=1):
        verified = (
            is_prime(exponent)
            and 17 <= exponent <= 911
            and exponent % 24 in {13, 17, 19, 23}
        )
        failures += int(not verified)
        transcript.update(
            f"candidate:{index}:{exponent}:{exponent % 24}:{int(verified)}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "candidate_index": index,
                "prime_exponent_ell": exponent,
                "residue_mod_24": exponent % 24,
                "certificate_verified": verified,
            }
        )

    allowed_scan: list[int] = []
    rejected_scan = 0
    for exponent in range(3, TWIN_EXPONENT_SCAN_LIMIT + 1, 2):
        factors = prime_factors(exponent)
        allowed = bool(factors) and all(factor in admissible_set for factor in factors)
        if allowed:
            allowed_scan.append(exponent)
        else:
            rejected_scan += 1
        transcript.update(
            f"scan:{exponent}:{','.join(map(str,factors))}:{int(allowed)}\n".encode(
                "ascii"
            )
        )

    theorem = (
        "Assume the verified external results summarized in Katz-Pratt, "
        "arXiv:2507.12397v2: for x^2-2=y^ell with ell an odd prime and y>0, "
        "there is no solution for ell<=13 or ell>911, Chen's congruence theorem "
        "leaves only ell=13,17,19,23 modulo 24, and any nontrivial y exceeds "
        "10^1000. If odd primes p,r and odd k>=3,m>=1 satisfy "
        "p^k+2=r^(2m), then every prime divisor ell of k belongs to the exact "
        "84-element set P={17<=ell<=911 prime: ell mod 24 in {13,17,19,23}}, "
        "and p^(k/ell)>10^1000. Thus the right-even contamination frontier is "
        "reduced from all odd k to exponents supported on P; it is not solved."
    )
    proof = (
        "Put x=r^m. For any prime ell dividing k, put y=p^(k/ell)>0. Then "
        "x^2-2=y^ell is a nontrivial Lebesgue-Nagell solution. Applying the "
        "external exponent bounds, congruence restriction, and lower bound "
        "places ell in P and gives y>10^1000. Since ell was an arbitrary prime "
        "divisor of k, every prime factor of k lies in P. Direct primality and "
        "residue enumeration independently confirms that P has 84 elements. "
        "The external paper explicitly leaves those 84 prime exponents open, "
        "so this corollary cannot be promoted to a Diophantine exclusion."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_remaining_prime_exponent_rows": rows,
        "remaining_prime_exponents": list(admissible),
        "residue_class_counts": residue_counts,
        "finite_odd_exponent_factor_scan": {
            "limit": TWIN_EXPONENT_SCAN_LIMIT,
            "tested_odd_exponent_count": (TWIN_EXPONENT_SCAN_LIMIT - 1) // 2,
            "allowed_exponent_count": len(allowed_scan),
            "rejected_exponent_count": rejected_scan,
            "first_twenty_allowed_exponents": allowed_scan[:20],
        },
        "external_theorem": {
            "name": "Katz-Pratt and cited Chen reduction for x^2-2=y^ell",
            "source": KATZ_PRATT_URL,
            "source_version": "arXiv:2507.12397v2, 25 July 2025",
            "statement_used": "Nontrivial positive solutions are excluded for prime ell<=13 and ell>911; only 84 primes ell in 17..911 with ell mod 24 in {13,17,19,23} remain; every nontrivial y exceeds 10^1000.",
            "status": "external_theorem",
            "dependency_boundary": "PrimeProject proves only the factor-reduction corollary and independently enumerates the 84 exponents; it does not independently reprove the paper's Diophantine theorems.",
        },
        "algorithm": "deterministic trial-division primality, exact residue filtering, and exact odd-exponent factor scanning",
        "complexity": "O(911 sqrt(911)+K sqrt(K)) integer operations for K=10000; the all-k reduction relies on the cited external theorem",
        "random_seed": None,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "remaining_prime_exponent_count": len(admissible),
            "all_prime_factors_of_k_restricted_to_remaining_set": True,
            "nontrivial_reduced_base_lower_bound_10_power_1000": True,
            "all_remaining_84_prime_exponents_excluded": False,
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
        {"id": f"{code}-T252", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T253", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-REJECT253", "label": rejected_name, "status": "disproved"},
        {"id": f"{code}-OPEN253", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T252", f"{code}-T253"],
        [f"{code}-T253", f"{code}-REJECT253"],
        [f"{code}-T253", f"{code}-OPEN253"],
    ]
    path = [f"{code}-T252", f"{code}-T253", f"{code}-OPEN253"]
    if external:
        external_id, label = external
        nodes.insert(1, {"id": external_id, "label": label, "status": "external_theorem"})
        edges.insert(0, [external_id, f"{code}-T253"])
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
        "ticket_id": f"{code}-TICKET-253",
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
    riemann = riemann_density_packet_audit()
    collatz = collatz_complete_character_audit()
    goldbach = goldbach_prime_prefix_audit()
    twin = twin_lebesgue_nagell_audit()
    sections = {
        "riemann": section(
            "riemann", "RH", "DirichletPacketSpectralDensityLimit", "partial_theorem", riemann,
            "treating the TICKET-252 zero-density escape as representative after imposing positive symmetric spectral density on normalized Dirichlet packets",
            ["extension from periodic Fourier projections to the signed arithmetic Weil form"],
            "the exact packet-energy identity and positive-density threshold",
            "ActualWeilFormDominatesPositiveDensityProjectionOnDirichletPackets",
            "SparseFourierProjectionInteriorConcentrationNoGo",
            "PositiveSpectralDensityStillAllowsZeroEnergyForNormalizedDirichletPackets",
            "The theorem concerns Fourier projections and one canonical concentrating family. No domination by the signed Guinand-Weil form, admissible-form-core transfer, or all-packet lower bound is proved.",
            "No RH proof or disproof; one exact density-to-packet-energy transfer theorem.",
            f"{len(RIEMANN_PACKET_SIZES)} exact rational periodic-density rows illustrate the analytic all-density theorem; spatial concentration uses a proved Dirichlet-kernel bound.",
        ),
        "collatz": section(
            "collatz", "CO", "CompleteSlopeCharacterSumDichotomyNoGo", "exact_no_go", collatz,
            "treating the complete additive-character sum over h as an independently smooth statistic to which generic square-root cancellation can be applied",
            ["cross-prime averages whose arithmetic data genuinely vary with q"],
            "a nontrivial cross-prime joint estimate rather than fixed-q orthogonality",
            "CrossPrimeCanonicalSlopeCharacterAverageCancellation",
            "UniformMarginalsCannotDetectProjectiveFermatSlopeNoGo",
            "CompleteFixedPrimeCharacterOrthogonalitySoftensTheCanonicalSlopeIndicator",
            "The exact dichotomy diagnoses a circular complete-sum route but does not prove occurrence or avoidance of [3:5] for the canonical pair as q varies.",
            "No Collatz orbit proof or counterexample; one exact no-go for a proposed character-sum implementation.",
            f"{len(COLLATZ_PRIMES)} canonical exact modular rows replay the identity; prior scans to much larger q remain finite and are not promoted.",
        ),
        "goldbach": section(
            "goldbach", "GB", "PrimeOrderingUniquePrefixRealizabilityCriterion", "partial_theorem", goldbach,
            "treating actual prime ordering as an unstructured extra condition with no exact finite realization test for a fixed compatible cyclotomic tail",
            ["compatible cyclotomic exponents outside the ten certified prime prefixes"],
            "the unique-prefix iff criterion and exact rejection of ten compatible tails",
            "UniformPrimePrefixDiscrepancyExcludesEveryCompatibleCyclotomicTail",
            "PrimeCountZeroResidueCyclotomicCompatibilityCriterion",
            "ACompatibleCyclotomicTailCanBeRealizedAtSomeUnconstrainedChoiceOfXWithoutMatchingOneForcedPrimePrefix",
            "Each fixed compatible pair is decidable by one finite prefix, but no uniform discrepancy theorem over all q,m is proved. Strong Goldbach is untouched beyond this auxiliary spectral route.",
            "No strong Goldbach proof or counterexample; one exact realizability iff and ten finite nonrealization certificates.",
            f"{len(GOLDBACH_COMPATIBLE_PAIRS)} exact prime-prefix rows, maximum prefix length {goldbach['aggregate']['maximum_prime_prefix_length']}; untested compatible tails remain open.",
        ),
        "twin_prime": section(
            "twin-prime", "TP", "RightEvenContaminationReducesToEightyFourLebesgueNagellExponents", "partial_theorem", twin,
            "treating every odd exponent k>=3 as an equally open right-even contamination case after the equation is reduced to x^2-2=y^k",
            ["the 84 remaining prime-exponent Lebesgue-Nagell equations and exponents supported on them"],
            "the external-theorem factor reduction, exact 84-exponent frontier, and y>10^1000 lower boundary",
            "LebesgueNagellExponent17HasNoPositiveSolution",
            "FiniteCongruenceLocalSolubilityNoGoForRightEvenPrimePowers",
            "EveryOddPrimeExponentRemainsASeparateRightEvenContaminationCase",
            "The corollary depends on a checked 2025 arXiv primary source and does not independently reprove its deep Diophantine inputs. That source explicitly leaves 84 prime exponents unresolved; twin-prime infinitude and Type-II estimates remain open.",
            "No twin-prime proof or counterexample; one external-theorem corollary that rigorously narrows the Diophantine contamination frontier.",
            f"84 exact prime-exponent rows and {twin['finite_odd_exponent_factor_scan']['tested_odd_exponent_count']} finite odd-k factor rows replay the filter; the all-k conclusion relies on the cited external theorems.",
            external=("TP-EXT-KATZ-PRATT", "Katz-Pratt v2 exponent bounds, Chen congruence reduction, and y>10^1000 bound"),
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
            "theorem_name": "FourConjectureDensityCharacterPrefixLebesgueAudit",
            "summary": "TICKET-253 proves three partial theorems and one exact route no-go while leaving all four parent conjectures open.",
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
                "collatz_fixed_representative_context": "https://arxiv.org/abs/1104.3909",
                "goldbach_major_arcs": "https://arxiv.org/abs/1205.5252",
                "twin_prime_parity": "https://arxiv.org/abs/1407.4897",
                "lebesgue_nagell_2025": KATZ_PRATT_URL,
            },
            "machine_audit": {
                "exact_theorem_count": 4,
                "new_partial_theorem_count": 3,
                "exact_no_go_count": 1,
                "candidate_resolution_count": 0,
                "conjecture_resolution_count": 0,
                "proof_dag_count": 4,
                "next_single_lemma_count": 4,
                "deep_focus_problem": "twin_prime",
                "stagnated_problem_count": 0,
                "riemann_density_packet_case_count": len(riemann["exact_periodic_density_rows"]),
                "collatz_character_case_count": len(collatz["exact_canonical_character_rows"]),
                "goldbach_prime_prefix_case_count": len(goldbach["exact_compatible_tail_prefix_rows"]),
                "twin_remaining_prime_exponent_count": len(twin["exact_remaining_prime_exponent_rows"]),
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
        "ticket": 253,
        "parent_ticket": 252,
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
        ROOT / "data/open-problem/ticket253-density-character-prefix-lebesgue.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-253-density-packet.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-253-complete-character-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-253-prime-prefix-criterion.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-253-lebesgue-nagell-reduction.json",
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
