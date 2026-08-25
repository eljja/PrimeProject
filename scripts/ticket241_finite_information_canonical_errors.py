from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket241-finite-information-canonical-errors.v1"
GENERATED_AT = "2026-08-25T23:58:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "finite_information_canonical_error_audit"
PRIME_LIMIT = 100_000_000


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
    flags[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            flags[prime * prime : limit + 1 : prime] = b"\x00" * (
                (limit - prime * prime) // prime + 1
            )
    return flags


def riemann_prime_cosine_rank_audit() -> dict[str, Any]:
    all_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    epsilon = 2.0**-10
    rows: list[dict[str, Any]] = []
    failures = 0
    transcript = hashlib.sha256()

    for prime_count in (3, 5, 8, 12):
        primes = all_primes[:prime_count]
        dimension = 2 * prime_count + 4
        times = np.linspace(-2.5, 2.5, dimension)
        columns: list[np.ndarray] = []
        for prime in primes:
            weight = math.log(prime) / math.sqrt(prime)
            scale = math.sqrt(weight)
            columns.append(scale * np.cos(times * math.log(prime)))
            columns.append(scale * np.sin(times * math.log(prime)))
        feature = np.column_stack(columns)
        kernel = feature @ feature.T

        basis_seed = np.zeros((dimension, dimension - 1))
        basis_seed[: dimension - 1, :] = np.eye(dimension - 1)
        basis_seed[-1, :] = -1.0
        q_basis, _ = np.linalg.qr(basis_seed)
        restricted = q_basis.T @ kernel @ q_basis
        eigenvalues = np.linalg.eigvalsh(restricted)
        numerical_rank = int(np.count_nonzero(eigenvalues > 1e-9))
        numerical_nullity = dimension - 1 - numerical_rank
        forced_nullity = dimension - 1 - 2 * prime_count
        regularized_eigenvalues = np.linalg.eigvalsh(
            restricted + epsilon * np.eye(dimension - 1)
        )
        verified = (
            numerical_rank <= 2 * prime_count
            and numerical_nullity >= forced_nullity
            and abs(float(eigenvalues[0])) < 1e-10
            and abs(float(regularized_eigenvalues[0]) - epsilon) < 1e-10
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{prime_count}:{dimension}:{numerical_rank}:"
                f"{numerical_nullity}:{eigenvalues[0]:.17g}:"
                f"{regularized_eigenvalues[0]:.17g}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "prime_support_size_m": prime_count,
                "sample_dimension_J": dimension,
                "feature_rank_cap_2m": 2 * prime_count,
                "forced_nullity_on_common_mode_complement": forced_nullity,
                "numerical_rank": numerical_rank,
                "numerical_nullity": numerical_nullity,
                "smallest_unregularized_eigenvalue": float(eigenvalues[0]),
                "diagonal_regularizer_epsilon": epsilon,
                "smallest_regularized_eigenvalue": float(
                    regularized_eigenvalues[0]
                ),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let P be a finite prime set, a_p>=0, and t_1,...,t_J be real. "
        "The kernel K_jk=sum_(p in P) a_p cos((t_j-t_k)log p) is positive "
        "semidefinite and has rank at most 2|P|. Its compression to the "
        "orthogonal complement of the common vector has the same rank cap; "
        "therefore it is singular whenever J-1>2|P|. Adding epsilon I makes "
        "the compressed lower bound exactly epsilon on the forced nullspace. "
        "Thus finite unsigned prime-cosine Gram positivity, including a lower "
        "bound supplied only by diagonal regularization, is automatic and "
        "cannot by itself establish the signed Guinand-Weil positivity "
        "equivalent to the Riemann Hypothesis."
    )
    proof = (
        "Use cos(x-y)=cos(x)cos(y)+sin(x)sin(y). K is the Gram matrix of "
        "the 2|P|-dimensional real feature vectors with coordinates "
        "sqrt(a_p)cos(t_j log p) and sqrt(a_p)sin(t_j log p). Hence K is "
        "positive semidefinite with rank at most 2|P|. Compression cannot "
        "increase rank, so rank-nullity gives a kernel of dimension at least "
        "J-1-2|P| on the common-mode complement. On that kernel, K+epsilon I "
        "acts as epsilon I. None of these steps uses zeta zeros, the gamma "
        "factor, trivial zeros, or the signed prime-power term of the explicit "
        "formula."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "prime_cosine_rank_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "finite_prime_cosine_kernel_psd_proved": True,
            "finite_support_rank_cap_proved": True,
            "common_mode_removal_does_not_remove_forced_nullspace": True,
            "regularized_lower_bound_is_tautological": True,
            "signed_guinand_weil_lower_bound_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "This theorem rejects only unsigned finite prime-cosine Gram "
            "positivity and artificial diagonal regularization as RH evidence. "
            "It does not analyze the complete signed Guinand-Weil form."
        ),
        "failure_count": failures,
    }


def valuation(value: int, prime: int, cap: int = 8) -> int:
    depth = 0
    while depth < cap and value % prime == 0:
        value //= prime
        depth += 1
    return depth


def collatz_fermat_line_audit(flags: bytearray) -> dict[str, Any]:
    local_rows: list[dict[str, Any]] = []
    failures = 0
    for prime in (7, 11, 13, 17, 19, 23, 29, 31):
        modulus = prime * prime
        unit_a = 1 + 3 * prime
        unit_b = 1 + 5 * prime
        x_difference = pow(unit_a, 5) - pow(unit_b, 3)
        y_difference = unit_a - unit_b
        verified = (
            pow(unit_a, 5, modulus) == pow(unit_b, 3, modulus)
            and unit_a % modulus != unit_b % modulus
            and valuation(x_difference, prime) >= 2
            and valuation(y_difference, prime) == 1
        )
        failures += int(not verified)
        local_rows.append(
            {
                "prime_q": prime,
                "unit_A_1_plus_3q": unit_a,
                "unit_B_1_plus_5q": unit_b,
                "A5_equals_B3_mod_q2": pow(unit_a, 5, modulus)
                == pow(unit_b, 3, modulus),
                "A_not_equal_B_mod_q2": unit_a % modulus != unit_b % modulus,
                "v_q_A5_minus_B3": valuation(x_difference, prime),
                "v_q_A_minus_B": valuation(y_difference, prime),
                "certificate_verified": verified,
            }
        )

    scanned = 0
    scanned_through_twenty_million = 0
    x_depth_two_primes: list[int] = []
    positive_candidates: list[dict[str, Any]] = []
    checksum = 0
    mask = (1 << 64) - 1
    for prime in range(5, PRIME_LIMIT + 1, 2):
        if not flags[prime]:
            continue
        scanned += 1
        if prime <= 20_000_000:
            scanned_through_twenty_million += 1
        modulus = prime * prime
        difference = (
            pow(32, prime - 1, modulus) - pow(27, prime - 1, modulus)
        ) % modulus
        x_first = difference // prime
        checksum = (checksum * 1_000_003 + prime + 257 * x_first) & mask
        if x_first == 0:
            x_depth_two_primes.append(prime)
            y_difference = (
                pow(2, prime - 1, modulus) - pow(3, prime - 1, modulus)
            ) % modulus
            y_first = y_difference // prime
            if y_first != 0:
                positive_candidates.append(
                    {"prime_q": prime, "x_first": x_first, "y_first": y_first}
                )

    expected_prime_count = 5_761_453
    verified_scan = scanned == expected_prime_count and not positive_candidates
    failures += int(not verified_scan)
    theorem = (
        "For every odd prime q>5 the principal-unit residues A=1+3q and "
        "B=1+5q satisfy A^5=B^3 mod q^2 but A!=B mod q^2, with "
        "v_q(A^5-B^3)>=2 and v_q(A-B)=1. Consequently the first-order "
        "relation 5u=3v mod q does not imply u=v mod q inside the local "
        "principal-unit group. The desired fixed-base implication for "
        "A=2^(q-1), B=3^(q-1) therefore cannot follow from principal-unit "
        "algebra alone; it requires special arithmetic information about the "
        "Fermat-quotient pair (F_q(2),F_q(3))."
    )
    proof = (
        "The binomial theorem gives (1+3q)^5=1+15q mod q^2 and "
        "(1+5q)^3=1+15q mod q^2. Their difference is divisible by q^2, "
        "whereas A-B=-2q has q-adic valuation one. This is an exact local "
        "countermodel to the implication between the two linear forms, but "
        "not an actual fixed-base exceptional prime. The bounded scan tests "
        "the actual residues 32^(q-1) and 27^(q-1) for every prime through "
        "10^8."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "principal_unit_countermodel_rows": local_rows,
        "bounded_fixed_base_scan": {
            "prime_limit": PRIME_LIMIT,
            "odd_primes_scanned": scanned,
            "odd_primes_through_twenty_million": scanned_through_twenty_million,
            "x_depth_at_least_two_count": len(x_depth_two_primes),
            "x_depth_at_least_two_primes": x_depth_two_primes[:100],
            "positive_defect_candidate_count": len(positive_candidates),
            "positive_defect_candidates": positive_candidates[:100],
            "rolling_checksum_u64": str(checksum),
            "scope": (
                "This finite scan does not exclude an exceptional prime above "
                "100,000,000 and does not prove the all-prime statement."
            ),
        },
        "aggregate": {
            "principal_unit_implication_refuted": True,
            "fixed_base_scan_extended_to_one_hundred_million": True,
            "bounded_scan_has_no_positive_defect": not positive_candidates,
            "all_prime_fixed_base_line_avoidance_proved": False,
            "general_necklace_descent_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The local countermodel shows that LTE and principal-unit algebra "
            "alone cannot prove depth domination. It is not a Collatz cycle or "
            "an actual exceptional prime. The 10^8 search is bounded evidence."
        ),
        "failure_count": failures,
    }


def goldbach_error_contract_audit(flags: bytearray) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures = 0
    represented_absolute_failures = 0
    transcript = hashlib.sha256()
    for cutoff in (1_000, 10_000, 100_000, 1_000_000, 10_000_000):
        base_buffer = cutoff / (math.log(cutoff) ** 2)
        for multiplier in (1, 2, 4):
            buffer_width = max(2, 2 * math.ceil(multiplier * base_buffer / 2))
            modulus = 2 * buffer_width + 1
            offsets = {
                offset
                for offset in range(buffer_width + 1)
                if cutoff - offset >= 2 and flags[cutoff - offset]
            }
            count = sum(
                1 for offset in offsets if buffer_width - offset in offsets
            )
            main = Fraction(len(offsets) ** 2, modulus)
            error = Fraction(count) - main
            represented = count >= 1
            signed_certificate = main + error >= 1
            absolute_certificate = main - abs(error) >= 1
            split_size = abs(error) + main + count + 1
            split_left = error + split_size
            split_right = -split_size
            split_preserves_error = split_left + split_right == error
            split_budget_increases = abs(split_left) + abs(split_right) > abs(error)
            verified = (
                signed_certificate == represented
                and (not absolute_certificate or represented)
                and split_preserves_error
                and split_budget_increases
            )
            failures += int(not verified)
            represented_absolute_failures += int(represented and not absolute_certificate)
            transcript.update(
                (
                    f"{cutoff}:{multiplier}:{count}:{main}:{error}:"
                    f"{absolute_certificate}:{split_left}:{split_right}\n"
                ).encode("ascii")
            )
            rows.append(
                {
                    "cutoff_X": cutoff,
                    "buffer_scale_multiplier": multiplier,
                    "target_N": 2 * cutoff - buffer_width,
                    "representation_count_R": count,
                    "dc_main_M": fraction_payload(main),
                    "signed_error_E": fraction_payload(error),
                    "signed_identity_certificate_M_plus_E_at_least_one": signed_certificate,
                    "absolute_certificate_M_minus_abs_E_at_least_one": absolute_certificate,
                    "representation_exists": represented,
                    "canceling_split_E1": fraction_payload(split_left),
                    "canceling_split_E2": fraction_payload(split_right),
                    "split_preserves_total_error": split_preserves_error,
                    "split_strictly_increases_absolute_budget": split_budget_increases,
                    "certificate_verified": verified,
                }
            )

    theorem = (
        "Let an integer representation count be decomposed as "
        "R(N)=M(N)+sum_i E_i(N), with M(N)>0. The signed inequality "
        "M+sum_i E_i>=1 is exactly R>=1 and is therefore not an intermediate "
        "result. The triangle certificate M-sum_i|E_i|>=1 is sufficient but "
        "not necessary, and is not invariant under algebraically harmless "
        "refinement: replacing E by (E+L)+(-L) preserves R while increasing "
        "the absolute budget arbitrarily. Hence a binary-Goldbach error theorem "
        "must freeze an arithmetic arc decomposition and its norm before any "
        "data are inspected; an unspecified 'all explicit errors' target is "
        "either tautological or decomposition-dependent."
    )
    proof = (
        "The signed claim follows by substitution. The triangle inequality "
        "gives R>=M-sum|E_i|, proving sufficiency of the absolute certificate. "
        "For any L, E=(E+L)+(-L); taking |L| large makes "
        "|E+L|+|L| arbitrarily large without changing R. Thus absolute error "
        "budgets have mathematical content only after a canonical decomposition "
        "and norm are fixed independently. The finite rows use the exact prime "
        "window DFT identity from TICKET-240 and exhibit represented targets "
        "where the DC absolute certificate fails."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "prime_window_error_contract_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "signed_error_target_is_exact_representation_claim": True,
            "absolute_error_certificate_is_sufficient_not_necessary": True,
            "absolute_budget_refinement_invariance_refuted": True,
            "represented_rows_failing_absolute_certificate": represented_absolute_failures,
            "row_count": len(rows),
            "canonical_binary_arc_lower_bound_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This does not refute a fixed classical major/minor-arc proof. It "
            "rejects only an unspecified or adaptively refined absolute-error "
            "target. Restricted-window zeros are not Goldbach counterexamples."
        ),
        "failure_count": failures,
    }


def deterministic_is_prime(value: int) -> bool:
    if value < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if value % prime == 0:
            return value == prime
    exponent = value - 1
    power_of_two = 0
    while exponent % 2 == 0:
        exponent //= 2
        power_of_two += 1
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % value == 0:
            continue
        witness = pow(base, exponent, value)
        if witness in (1, value - 1):
            continue
        for _ in range(power_of_two - 1):
            witness = witness * witness % value
            if witness == value - 1:
                break
        else:
            return False
    return True


def crt_pair(a: int, modulus: int, b: int, other: int) -> tuple[int, int]:
    step = ((b - a) * pow(modulus, -1, other)) % other
    combined_modulus = modulus * other
    return (a + modulus * step) % combined_modulus, combined_modulus


def first_prime_in_progression(residue: int, modulus: int, lower: int) -> int:
    multiplier = max(0, (lower - residue + modulus - 1) // modulus)
    while True:
        candidate = residue + multiplier * modulus
        if deterministic_is_prime(candidate):
            return candidate
        multiplier += 1


def twin_periodic_fingerprint_audit() -> dict[str, Any]:
    cases = [
        (30, 11, 7),
        (210, 11, 11),
        (2310, 17, 13),
        (30030, 17, 17),
        (510510, 29, 19),
    ]
    rows: list[dict[str, Any]] = []
    failures = 0
    transcript = hashlib.sha256()
    for modulus, admissible_residue, outside_prime in cases:
        residue, combined = crt_pair(
            admissible_residue, modulus, -2 % outside_prime, outside_prime
        )
        prime = first_prime_in_progression(residue, combined, 2 * combined)
        successor = prime + 2
        feature_before = hashlib.sha256(
            f"{admissible_residue % modulus}:{(admissible_residue + 2) % modulus}:{modulus}".encode(
                "ascii"
            )
        ).hexdigest()[:16]
        feature_after = hashlib.sha256(
            f"{prime % modulus}:{successor % modulus}:{modulus}".encode("ascii")
        ).hexdigest()[:16]
        verified = (
            math.gcd(admissible_residue, modulus) == 1
            and math.gcd(admissible_residue + 2, modulus) == 1
            and math.gcd(residue, combined) == 1
            and deterministic_is_prime(prime)
            and successor % outside_prime == 0
            and successor > outside_prime
            and feature_before == feature_after
        )
        failures += int(not verified)
        transcript.update(
            f"{modulus}:{admissible_residue}:{outside_prime}:{residue}:{prime}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "period_M": modulus,
                "admissible_residue_a": admissible_residue,
                "outside_prime_ell": outside_prime,
                "combined_crt_residue_b": residue,
                "combined_modulus_M_ell": combined,
                "prime_witness_p": prime,
                "forced_composite_successor_p_plus_2": successor,
                "successor_cofactor": successor // outside_prime,
                "periodic_feature_hash_before": feature_before,
                "periodic_feature_hash_at_witness": feature_after,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let F be any finite collection of features of (n,n+2), each periodic "
        "with a fixed modulus, and let M be a common period. For every residue "
        "a mod M with gcd(a,M)=gcd(a+2,M)=1, there are infinitely many primes "
        "p for which F(p,p+2)=F(a,a+2) while p+2 is composite. Choose a prime "
        "ell not dividing 2M, impose p=a mod M and p=-2 mod ell, and apply "
        "Dirichlet to the resulting reduced CRT class. Therefore no finite "
        "periodic fingerprint, even conditioned on p being prime and local "
        "admissibility of p+2, can certify twin-prime mass."
    )
    proof = (
        "CRT gives b modulo M ell. Since a is reduced modulo M and -2 is "
        "nonzero modulo ell, gcd(b,M ell)=1. Dirichlet's theorem gives "
        "infinitely many primes p=b mod M ell. Periodicity gives the same "
        "feature vector as a modulo M, while ell divides p+2; for all "
        "sufficiently large such primes, p+2 is a proper composite multiple "
        "of ell. A finite family of periods is replaced by their lcm."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "periodic_fingerprint_crt_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "arbitrary_finite_periodic_fingerprint_mimicry_proved": True,
            "prime_conditioned_composite_successor_mimicry_proved": True,
            "finite_periodic_twin_classifier_sufficiency_refuted": True,
            "growing_nonperiodic_parity_sensitive_bound_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem does not show that twins are finite. It excludes only "
            "fixed finite periodic features as a sufficient certificate. "
            "Growing moduli and signed Type II information remain outside it."
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
            {"id": f"{code}-T240", "label": input_name, "status": "closed_input"},
            {
                "id": f"{code}-N241",
                "label": rejected_name,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{code}-T241",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{code}-OPEN241",
                "label": open_name,
                "status": "highest_risk_open",
            },
        ],
        "edges": [
            [f"{code}-T240", f"{code}-N241"],
            [f"{code}-T240", f"{code}-T241"],
            [f"{code}-N241", f"{code}-T241"],
            [f"{code}-T241", f"{code}-OPEN241"],
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
        "ticket_id": f"{code}-TICKET-241",
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
    flags = prime_flags_up_to(PRIME_LIMIT)
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "FinitePrimeCosineRankNoGoForRegularizedWeilPositivity",
            riemann_prime_cosine_rank_audit(),
            "finite unsigned prime-cosine Gram positivity or an artificial diagonal floor as evidence for RH",
            "the complete signed Guinand-Weil form with archimedean and prime-power terms and no artificial floor",
            "SignedGuinandWeilFiniteSectionsConvergeWithoutArtificialDiagonalForEveryAdmissibleTestFamily",
            "CotlarNormSummabilityNoGoForUniformGramLowerBounds",
            "UnsignedPrimeCosineGramLowerBoundRepresentsSignedWeilPositivity",
            "No lower bound is proved for the complete signed Guinand-Weil quadratic form over every admissible test function.",
            "No RH proof, disproof, or zero exclusion; one exact finite-support rank theorem and four numerical rank audits only.",
        ),
        "collatz": section(
            "collatz",
            "CO",
            "PrincipalUnitFermatLineIndependenceNoGoAndHundredMillionAudit",
            collatz_fermat_line_audit(flags),
            "deriving fixed-base rational Wieferich-depth domination from principal-unit algebra or LTE alone",
            "special arithmetic control of the actual Fermat quotient pair, with bounded searches labeled finite",
            "FixedBaseFermatQuotientLineAvoidanceFor5Fq2Equals3Fq3UnlessFq2EqualsFq3",
            "RunBlockDefectFermatQuotientReductionAndTwentyMillionAudit",
            "PrincipalUnitLinearizationForcesFixedBaseDepthDomination",
            "The fixed-base all-prime line avoidance, general necklaces, and aperiodic descent remain open.",
            "No Collatz proof or cycle; one local principal-unit countermodel and an actual fixed-base scan through one hundred million only.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "CanonicalErrorContractAndRefinementInstabilityNoGo",
            goldbach_error_contract_audit(flags),
            "an unspecified signed or absolute collection of 'all explicit errors' as a decomposition-independent milestone",
            "a canonical arithmetic major/minor-arc split and norm fixed before target data, followed by a uniform lower certificate",
            "FixedBinaryPrimeArcDecompositionHasUniformTargetwisePositiveLowerCertificate",
            "SignedFourierSlackIntegralityEquivalenceAndIntermediateTargetNoGo",
            "AnyExplicitErrorDecompositionDefinesAStableIntermediateGoldbachTarget",
            "No canonical target-uniform binary-prime major/minor-arc lower certificate is proved.",
            "No Goldbach proof or counterexample; one exact decomposition theorem and fifteen restricted-window audits only.",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "FinitePeriodicPrimeFingerprintMimicryForShiftTwo",
            twin_periodic_fingerprint_audit(),
            "any fixed finite periodic fingerprint, even after conditioning the first entry to be prime, as a twin certificate",
            "growing nonperiodic parity-sensitive bilinear information for the actual shift-two Lambda correlation",
            "GrowingModulusParitySensitiveTypeIIBoundForShiftTwoLambdaOnInfinitelyManyDyadicBlocks",
            "OneSidedPrimeWeightedCRTFullSupportAndCompositeSuccessorNoGo",
            "FinitePeriodicFeatureEnrichmentEventuallySeparatesTwinPairs",
            "No growing-modulus signed Type II lower bound for Lambda(n)Lambda(n+2) is proved.",
            "No twin-prime proof or counterexample; one exact periodic-feature no-go theorem and five CRT witnesses only.",
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
        "bounded_prime_scan_limit": PRIME_LIMIT,
        "total_failure_count": total_failures,
    }
    audit: dict[str, Any] = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureFiniteInformationCanonicalErrorAudit",
            "summary": (
                "TICKET-241 proves four exact information-boundary theorems, "
                "extends the actual Collatz fixed-base search to 10^8, and "
                "leaves all four parent conjectures open."
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
        ROOT / "data/open-problem/ticket241-finite-information-canonical-errors.json",
        audit,
    )
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-241-prime-cosine-rank-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-241-fermat-line-local-no-go.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-241-error-contract-no-go.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-241-periodic-fingerprint-no-go.json",
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
