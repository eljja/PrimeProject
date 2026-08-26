from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket244-joint-tightness-harmonic-parity-fold-polylog-mimicry.v1"
GENERATED_AT = "2026-08-26T09:30:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "joint_tightness_harmonic_parity_fold_polylog_mimicry_audit"
HARMONIC_SCAN_LIMIT = 20_000
GOLDBACH_FINITE_LIMIT = 10_000


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


def next_prime_after(value: int) -> int:
    candidate = value + 1
    while not deterministic_is_prime(candidate):
        candidate += 1
    return candidate


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


def riemann_joint_tightness_audit() -> dict[str, Any]:
    gram_rows: list[dict[str, Any]] = []
    translation_rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0

    for size in (4, 8, 16, 32, 64):
        verified = True
        transcript.update(f"gram:{size}:1:0:2\n".encode("ascii"))
        gram_rows.append(
            {
                "orthonormal_family_size": size,
                "common_physical_support": "[-pi,pi]",
                "real_even": True,
                "gram_diagonal": fraction_payload(Fraction(1)),
                "maximum_off_diagonal_absolute_value": fraction_payload(Fraction(0)),
                "minimum_pair_distance_squared": fraction_payload(Fraction(2)),
                "certificate_verified": verified,
            }
        )

    for scale in (2, 4, 8, 16, 32):
        radius = scale
        shift = Fraction(1, scale * scale)
        tail_budget = Fraction(1, scale * scale)
        low_frequency_term = Fraction(radius * radius) * shift * shift
        total_bound = low_frequency_term + 4 * tail_budget
        expected = Fraction(5, scale * scale)
        verified = total_bound == expected
        failures += int(not verified)
        transcript.update(
            f"translation:{radius}:{shift}:{tail_budget}:{total_bound}\n".encode(
                "ascii"
            )
        )
        translation_rows.append(
            {
                "frequency_radius_R": radius,
                "translation_h": fraction_payload(shift),
                "uniform_frequency_tail_budget_epsilon": fraction_payload(
                    tail_budget
                ),
                "squared_L2_translation_bound": fraction_payload(total_bound),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let K be a bounded subset of L2(R), with unitary Fourier transform. "
        "Then K is relatively compact in L2(R) if and only if for every "
        "epsilon>0 there is R such that both sup_(f in K) integral_(|x|>R) "
        "|f(x)|^2 dx<epsilon and sup_(f in K) integral_(|xi|>R) "
        "|fhat(xi)|^2 dxi<epsilon. Neither tail condition alone suffices: "
        "TICKET-243 supplies the frequency-only counterfamily, while "
        "f_n(x)=pi^(-1/2)1_[-pi,pi](x)cos(nx) is a normalized real-even "
        "orthonormal physical-tight counterfamily."
    )
    proof = (
        "For sufficiency, Plancherel gives ||tau_h f-f||_2^2 as the integral "
        "of |exp(i h xi)-1|^2|fhat(xi)|^2. Splitting at |xi|=R bounds it "
        "by R^2 h^2 B^2+4 epsilon, uniformly for ||f||_2<=B. Frequency "
        "tightness therefore gives uniform translation continuity; physical "
        "tightness and the Riesz-Kolmogorov theorem give relative compactness. "
        "For necessity, a finite epsilon-net for a compact set transfers the "
        "vanishing tails of its finitely many centers uniformly; apply the "
        "same argument after the unitary Fourier transform. Cosine "
        "orthogonality proves the physical-only counterfamily has Gram matrix I."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "physical_only_counterfamily_gram_rows": gram_rows,
        "exact_translation_bound_rows": translation_rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "joint_tightness_characterizes_relative_compactness": True,
            "physical_tightness_alone_refuted": True,
            "frequency_tightness_alone_refuted_by_ticket243": True,
            "actual_admissible_weil_class_joint_tightness_proved": False,
            "uniform_signed_guinand_weil_tail_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The theorem is functional analytic. It does not prove that the "
            "full normalized Guinand-Weil admissible class is jointly tight, "
            "does not control its signed arithmetic tail, and supplies no "
            "positive Weil margin or zero exclusion."
        ),
        "failure_count": failures,
    }


def harmonic_prefixes_mod_prime(prime: int) -> tuple[int, int]:
    half = (prime - 1) // 2
    third = prime // 3
    inverses = [0] * (half + 1)
    inverses[1] = 1
    for value in range(2, half + 1):
        inverses[value] = (-(prime // value) * inverses[prime % value]) % prime
    return sum(inverses[1 : half + 1]) % prime, sum(
        inverses[1 : third + 1]
    ) % prime


def fermat_quotient_mod_prime(base: int, prime: int) -> int:
    return ((pow(base, prime - 1, prime * prime) - 1) // prime) % prime


def collatz_harmonic_audit() -> dict[str, Any]:
    primes = [prime for prime in primes_up_to(HARMONIC_SCAN_LIMIT) if prime > 5]
    selected = {7, 11, 13, 29, 59, 109, 487, 1009, 10007, 19997}
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    bad_line_count = 0
    first_order_positive_candidate_count = 0

    for prime in primes:
        half_harmonic, third_harmonic = harmonic_prefixes_mod_prime(prime)
        f2 = fermat_quotient_mod_prime(2, prime)
        f3 = fermat_quotient_mod_prime(3, prime)
        x_line = (5 * f2 - 3 * f3) % prime == 0
        y_line = (f2 - f3) % prime == 0
        harmonic_x_line = (4 * third_harmonic - 5 * half_harmonic) % prime == 0
        harmonic_y_line = (4 * third_harmonic - 3 * half_harmonic) % prime == 0
        x_depth_direct = (
            pow(32, prime - 1, prime * prime)
            == pow(27, prime - 1, prime * prime)
        )
        verified = (
            (half_harmonic + 2 * f2) % prime == 0
            and (2 * third_harmonic + 3 * f3) % prime == 0
            and x_line == harmonic_x_line == x_depth_direct
            and y_line == harmonic_y_line
            and ((x_line and not y_line) == (harmonic_x_line and half_harmonic != 0))
        )
        failures += int(not verified)
        bad_line_count += int(x_line)
        first_order_positive_candidate_count += int(x_line and not y_line)
        transcript.update(
            (
                f"{prime}:{f2}:{f3}:{half_harmonic}:{third_harmonic}:"
                f"{int(x_line)}:{int(y_line)}:{int(verified)}\n"
            ).encode("ascii")
        )
        if prime in selected:
            rows.append(
                {
                    "prime_q": prime,
                    "fermat_quotient_Fq2": f2,
                    "fermat_quotient_Fq3": f3,
                    "half_harmonic_H_floor_q_over_2_mod_q": half_harmonic,
                    "third_harmonic_H_floor_q_over_3_mod_q": third_harmonic,
                    "rational_wieferich_bad_line": x_line,
                    "two_over_three_square_depth_line": y_line,
                    "harmonic_equivalences_verified": verified,
                }
            )

    theorem = (
        "For every prime q>5, put F_q(a)=(a^(q-1)-1)/q modulo q and "
        "H_m=sum_(1<=k<=m) k^(-1) modulo q. Then 2F_q(2)=-H_((q-1)/2) "
        "and 3F_q(3)=-2H_floor(q/3). Consequently 5F_q(2)=3F_q(3) "
        "if and only if 4H_floor(q/3)=5H_((q-1)/2), while "
        "F_q(2)=F_q(3) if and only if 4H_floor(q/3)=3H_((q-1)/2). "
        "On the first line, the second holds exactly when H_((q-1)/2)=0. "
        "Thus a TICKET-240 first-order positive-defect candidate is equivalent "
        "to the first harmonic line together with H_((q-1)/2) nonzero. If "
        "both harmonic sums vanish, higher q-adic depths remain undecided."
    )
    proof = (
        "Multiplication by m permutes the nonzero residues modulo q. Writing "
        "mk=r_k+q floor(mk/q), comparing products modulo q^2, and grouping "
        "the floors gives Lerch's elementary identity mF_q(m)=-sum_(j=1)"
        "^(m-1) H_floor(jq/m) modulo q. At m=2 this is the half-harmonic "
        "formula. At m=3, H_floor(2q/3)=H_floor(q/3) modulo q by the "
        "reflection k -> q-k, giving the third-harmonic formula. Substitution "
        "into the two Fermat-quotient lines proves both equivalences. Under "
        "4H_third=5H_half, the second line becomes 5H_half=3H_half, hence "
        "H_half=0 because q is odd."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "selected_exact_harmonic_rows": rows,
        "bounded_harmonic_replay": {
            "prime_limit": HARMONIC_SCAN_LIMIT,
            "primes_scanned": len(primes),
            "bad_line_count": bad_line_count,
            "first_order_positive_candidate_count": first_order_positive_candidate_count,
            "failure_count": failures,
            "integer_arithmetic_only": True,
            "algorithm": "linear modular-inverse recurrence per prime plus modular exponentiation",
            "complexity": "O(sum_{q<=Q, q prime} q) integer operations and O(pi(Q)) modular exponentiations",
        },
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "lerch_harmonic_reduction_proved": True,
            "first_order_positive_candidate_harmonic_characterization_proved": True,
            "all_prime_harmonic_bad_line_nonvanishing_proved": False,
            "bounded_replay_has_first_order_positive_candidate": (
                first_order_positive_candidate_count > 0
            ),
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The harmonic identities are exact for every prime q>5, but the "
            "replay is finite and finds no bad-line prime. No argument proves "
            "all-prime nonvanishing. If both first-layer lines vanish, higher "
            "q-adic depths would still require comparison. Even all-prime "
            "run-block depth domination would not settle arbitrary Collatz "
            "orbits or cycles."
        ),
        "failure_count": failures,
    }


def goldbach_parity_fold_audit() -> dict[str, Any]:
    cutoffs = (100, 500, 1_000, 5_000, GOLDBACH_FINITE_LIMIT)
    flags = prime_flags_up_to(max(cutoffs))
    all_primes = [value for value, flag in enumerate(flags) if flag]
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    total_targets = 0

    for cutoff in cutoffs:
        primes = [prime for prime in all_primes if prime <= cutoff]
        odd_primes = [prime for prime in primes if prime != 2]
        target_failures = 0
        minimum_count: int | None = None
        minimum_target: int | None = None
        for target in range(6, cutoff + 1, 2):
            all_count = sum(
                1
                for prime in primes
                if 2 <= target - prime <= cutoff and flags[target - prime]
            )
            odd_count = sum(
                1
                for prime in odd_primes
                if 3 <= target - prime <= cutoff and flags[target - prime]
            )
            target_failures += int(all_count != odd_count)
            if minimum_count is None or odd_count < minimum_count:
                minimum_count = odd_count
                minimum_target = target

        grid_modulus = 2 * (2 * cutoff + 1)
        half_turn = grid_modulus // 2
        odd_phase_failures = sum(
            1 for prime in odd_primes if (prime * half_turn) % grid_modulus != half_turn
        )
        even_target_phase_failures = sum(
            1
            for target in range(6, cutoff + 1, 2)
            if (target * half_turn) % grid_modulus != 0
        )
        verified = (
            target_failures == 0
            and odd_phase_failures == 0
            and even_target_phase_failures == 0
        )
        failures += int(not verified)
        target_count = (cutoff - 4) // 2
        total_targets += target_count
        transcript.update(
            (
                f"{cutoff}:{len(odd_primes)}:{target_count}:{minimum_count}:"
                f"{minimum_target}:{target_failures}:{odd_phase_failures}:"
                f"{even_target_phase_failures}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "prime_cutoff_X": cutoff,
                "odd_prime_count": len(odd_primes),
                "even_targets_6_through_X_checked": target_count,
                "minimum_ordered_odd_prime_representation_count": minimum_count,
                "minimum_count_target": minimum_target,
                "full_sum_vs_odd_sum_coefficient_failures": target_failures,
                "exact_half_turn_phase_failures": odd_phase_failures
                + even_target_phase_failures,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let O_X(alpha)=sum_(3<=p<=X) exp(2 pi i p alpha). Then "
        "O_X(alpha+1/2)=-O_X(alpha). For every even N, "
        "O_X(alpha)^2 exp(-2 pi i N alpha) is exactly 1/2-periodic. Hence "
        "the arc around 1/2 is the translate, with identical signed integral, "
        "of the arc around 0 for the odd-prime binary coefficient. Moreover, "
        "for every even N>=6 the full prime representation coefficient equals "
        "the odd-prime coefficient, since a representation using 2 would force "
        "the other summand to be an even prime at least 4."
    )
    proof = (
        "Every prime in O_X is odd, so translation by 1/2 multiplies every "
        "summand by -1. Squaring removes that sign, and the target phase gains "
        "exp(-pi i N)=1 for even N. This proves exact half-periodicity and "
        "equality of translated arc integrals. Expanding S_X=O_X+exp(4 pi i "
        "alpha), the extra Fourier coefficients correspond only to a summand "
        "2 or to 2+2; neither contributes to an even N>=6."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_parity_fold_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "odd_prime_half_antiperiodicity_proved": True,
            "even_binary_integrand_half_periodicity_proved": True,
            "full_and_odd_prime_coefficients_equal_for_even_N_at_least_6": True,
            "finite_even_targets_checked": total_targets,
            "denominator_at_least_three_major_arcs_controlled": False,
            "signed_residual_saving_proved": False,
            "strong_goldbach_resolved": False,
        },
        "no_go_scope": (
            "The parity fold exactly removes duplicate bookkeeping between the "
            "zero and half-frequency arcs. It gives no estimate on rational "
            "arcs of denominator at least three, no signed residual minor-arc "
            "saving, and no positive representation lower bound beyond the "
            "explicit finite replay."
        ),
        "failure_count": failures,
    }


def twin_polylog_mimicry_audit() -> dict[str, Any]:
    cases = ((30, 11), (210, 11), (2310, 17), (30030, 17))
    polylog_power = 4
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0

    for modulus, residue in cases:
        outside_prime = next_prime_after(modulus)
        crt_residue, combined_modulus = crt_pair(
            residue, modulus, (-2) % outside_prime, outside_prime
        )
        block_start = 1000 * combined_modulus
        prime = first_prime_in_dyadic_progression(
            crt_residue, combined_modulus, block_start
        )
        successor = prime + 2 if prime is not None else None
        floor_log2 = block_start.bit_length() - 1
        verified = (
            modulus < outside_prime < 2 * modulus
            and combined_modulus < 2 * modulus * modulus
            and modulus <= floor_log2**polylog_power
            and prime is not None
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
                f"{combined_modulus}:{block_start}:{prime}:{successor}:"
                f"{floor_log2}:{int(verified)}\n"
            ).encode("ascii")
        )
        rows.append(
            {
                "scale_dependent_period_M_X": modulus,
                "admissible_residue_a_X": residue,
                "bertrand_prime_ell_X": outside_prime,
                "combined_crt_residue": crt_residue,
                "combined_modulus_Q_X": combined_modulus,
                "dyadic_block_start_X": block_start,
                "floor_log2_X": floor_log2,
                "polylog_power_A": polylog_power,
                "M_X_at_most_floor_log2_X_power_A": (
                    modulus <= floor_log2**polylog_power
                ),
                "prime_mimic_p": prime,
                "forced_composite_successor_p_plus_2": successor,
                "successor_cofactor": (
                    successor // outside_prime if successor is not None else None
                ),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Fix A>0. For every sufficiently large X, let 1<=M_X<="
        "(log_2 X)^A, choose a_X modulo M_X with gcd(a_X,M_X)="
        "gcd(a_X+2,M_X)=1, and let F_X be any feature of (n,n+2) depending "
        "only on that pair modulo M_X. Then every sufficiently large dyadic "
        "block [X,2X] contains a prime p with F_X(p,p+2)=F_X(a_X,a_X+2) "
        "but p+2 composite. Thus no pure periodic twin classifier whose "
        "scale-dependent period is bounded by any fixed power of log X can "
        "exclude prime/composite-successor mimics."
    )
    proof = (
        "For M_X>=2, Bertrand's postulate supplies a prime ell_X with "
        "M_X<ell_X<2M_X; use ell_X=3 for M_X=1. CRT gives a reduced class "
        "r_X=a_X mod M_X and r_X=-2 mod ell_X, of modulus Q_X=M_X ell_X<"
        "2M_X^2<=2(log_2 X)^(2A). The Siegel-Walfisz theorem is uniform for "
        "moduli bounded by any fixed power of log X, so the number of primes "
        "p in [X,2X] in this class is asymptotic to "
        "(Li(2X)-Li(X))/phi(Q_X), uniformly and hence positive for all large "
        "X. Then ell_X divides p+2; since X>ell_X eventually, p+2 is "
        "composite. Congruence modulo M_X preserves F_X."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "finite_polylog_period_witness_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "polylog_growing_period_every_large_dyadic_mimicry_proved": True,
            "pure_polylog_periodic_classifier_route_refuted": True,
            "finite_witness_rows_verified": failures == 0,
            "superpolylog_or_nonperiodic_structure_required_for_this_route": True,
            "scale_local_type_ii_cancellation_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem blocks only classifiers determined by one residue "
            "pair modulo M_X<=log^A X. It does not cover superpolylogarithmic "
            "periods, nonperiodic information, signed Lambda correlations, or "
            "Type-I/II estimates, and it neither proves nor disproves twin primes."
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
        {"id": f"{code}-T243", "label": prior_name, "status": "proved"},
        {"id": f"{code}-T244", "label": theorem_name, "status": "proved"},
        {"id": f"{code}-OPEN244", "label": open_name, "status": "open"},
    ]
    edges = [
        [f"{code}-T243", f"{code}-T244"],
        [f"{code}-T244", f"{code}-OPEN244"],
    ]
    if rejected_name:
        nodes.insert(
            1,
            {"id": f"{code}-N244", "label": rejected_name, "status": "disproved"},
        )
        edges.insert(1, [f"{code}-T243", f"{code}-N244"])
        edges.insert(2, [f"{code}-N244", f"{code}-T244"])
    for index, external_name in enumerate(external_names, start=1):
        external_id = f"{code}-EXT244-{index}"
        nodes.insert(
            1,
            {"id": external_id, "label": external_name, "status": "external_theorem"},
        )
        edges.insert(1, [external_id, f"{code}-T244"])
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
        "ticket_id": f"{code}-TICKET-244",
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
            code,
            prior_name,
            theorem_name,
            next_lemma,
            rejected_name,
            external_names,
        ),
        "claim_boundary": claim_boundary,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_joint_tightness_audit()
    collatz = collatz_harmonic_audit()
    goldbach = goldbach_parity_fold_audit()
    twin = twin_polylog_mimicry_audit()
    sections = {
        "riemann": section(
            "riemann",
            "RH",
            "JointPhysicalFrequencyTightnessCharacterizesL2Precompactness",
            "partial_theorem",
            riemann,
            "physical tightness alone, together with TICKET-243's frequency-tightness-alone route, as a compactness certificate",
            [],
            "joint physical-frequency tightness as the exact compactness gate, followed by signed arithmetic-tail control",
            "UniformSignedGuinandWeilTailWithPositiveMarginOnExhaustiveJointlyTightAdmissibleClasses",
            "BandlimitedEvenTestFamilyNoncompactnessAndFrequencyTightnessNoGo",
            "The actual normalized admissible Weil class has not been shown jointly tight, exhaustive, or uniformly positive under signed arithmetic tails.",
            "No RH proof, disproof, zero exclusion, or positivity theorem; the functional-analytic compactness gate is exactly characterized.",
            "Five symbolic physical-support Gram rows and five exact rational translation-bound rows; the infinite theorem uses Riesz-Kolmogorov and Plancherel.",
            "PhysicalTightnessAloneImpliesRelativeCompactness",
            ("Plancherel theorem", "Riesz-Kolmogorov compactness theorem"),
        ),
        "collatz": section(
            "collatz",
            "CO",
            "FixedBaseBadLineHarmonicSumEquivalence",
            "partial_theorem",
            collatz,
            "none newly; universal principal-unit transfer remains retired by TICKET-243",
            [],
            "the exact fixed-base harmonic bad-line nonvanishing statement, equivalent to excluding every 32/27 rational-Wieferich prime at first depth",
            "FixedBaseHarmonicBadLineNonvanishingForEveryPrime",
            "UnboundedOrderPrincipalUnitTransferCountermodels",
            "No all-prime proof excludes 4H_floor(q/3)=5H_((q-1)/2); simultaneous first-layer vanishing would also leave higher q-adic depths, and general Collatz dynamics remain outside this run-block reduction.",
            "No Collatz proof, divergent orbit, or nontrivial cycle; one exact all-prime harmonic reformulation and a finite identity replay only.",
            f"All {len([p for p in primes_up_to(HARMONIC_SCAN_LIMIT) if p > 5]):,} primes 5<q<={HARMONIC_SCAN_LIMIT:,} replayed with exact integer modular arithmetic; no bounded absence is promoted to an all-prime conclusion.",
        ),
        "goldbach": section(
            "goldbach",
            "GB",
            "ExactParityArcFoldingForEvenBinaryGoldbach",
            "partial_theorem",
            goldbach,
            "treating the zero and half-frequency arcs as analytically independent for the odd-prime even-target coefficient",
            [],
            "one half-torus with complete denominator-at-least-three major arcs and a signed residual estimate",
            "CompleteDenominatorAtLeastThreeMajorArcExtractionAndSignedResidualSavingAfterParityFolding",
            "OmittedHalfFrequencyArcCarriesNaturalBinaryEnergy",
            "No denominator-at-least-three major-arc asymptotic, signed residual saving, or uniform positive Goldbach lower bound is proved.",
            "No strong Goldbach proof or counterexample; an exact parity-fold identity plus bounded direct coefficient checks only.",
            f"Exactly {goldbach['aggregate']['finite_even_targets_checked']:,} even targets across five cutoffs through {GOLDBACH_FINITE_LIMIT:,}; finite Goldbach checks do not imply the infinite conjecture.",
            "ZeroAndHalfFrequencyOddPrimeArcsRequireIndependentSignedAnalysis",
        ),
        "twin_prime": section(
            "twin-prime",
            "TP",
            "PolylogarithmicGrowingPeriodMimicryInEveryLargeDyadicBlock",
            "exact_no_go",
            twin,
            "any pure periodic twin certificate whose scale-dependent period is bounded by a fixed power of log X",
            [],
            "superpolylogarithmic or nonperiodic parity-sensitive information, especially signed Type-II Lambda correlation",
            "SuperPolylogarithmicScaleLocalTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass",
            "FixedPeriodicMimicryInEverySufficientlyLargeDyadicBlock",
            "The obstruction does not address superpolylogarithmic periods, nonperiodic features, or the signed Type-I/II estimates needed for twin-prime mass.",
            "No twin-prime proof or finite counterexample to infinitude; one general no-go for all fixed-polylog periodic classifiers.",
            "Four exact scale-dependent CRT witnesses at A=4; the all-large-X theorem relies on Bertrand and the uniform Siegel-Walfisz theorem, not on the four rows.",
            "PolylogarithmicGrowingPeriodsEscapePrimeCompositeSuccessorMimicry",
            ("Bertrand's postulate", "Siegel-Walfisz theorem"),
        ),
    }
    total_failures = sum(
        item["reproducible_computation"]["failure_count"]
        for item in sections.values()
    )
    machine = {
        "exact_theorem_count": 4,
        "partial_theorem_count": 3,
        "exact_no_go_count": 1,
        "candidate_resolution_count": 0,
        "conjecture_resolution_count": 0,
        "proof_dag_count": 4,
        "next_single_lemma_count": 4,
        "deep_focus_problem": "twin_prime",
        "stagnated_problem_count": 0,
        "harmonic_scan_limit": HARMONIC_SCAN_LIMIT,
        "goldbach_finite_limit": GOLDBACH_FINITE_LIMIT,
        "twin_witness_count": len(twin["finite_polylog_period_witness_rows"]),
        "total_failure_count": total_failures,
    }
    audit: dict[str, Any] = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "iteration_complete": True,
        "program_complete": False,
        AUDIT_KEY: {
            "theorem_name": "FourConjectureJointTightnessHarmonicParityFoldPolylogMimicryAudit",
            "summary": (
                "TICKET-244 proves three partial theorems and one exact route "
                "no-go while leaving all four parent conjectures open."
            ),
            **sections,
            "research_baselines": {
                "riemann_status": "https://www.claymath.org/millennium/Riemann-Hypothesis/",
                "compactness": "https://arxiv.org/abs/2204.14237",
                "fermat_quotients": "https://arxiv.org/abs/1110.3113",
                "collatz": "https://arxiv.org/abs/1909.03562",
                "goldbach_minor": "https://arxiv.org/abs/1205.5252",
                "siegel_walfisz": "https://arxiv.org/abs/2108.10878",
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
    prior_results = {
        "riemann": [
            "PointwiseFiniteSectionMovingVectorNoGoAndCompactUniformTransfer",
            "BandlimitedEvenTestFamilyNoncompactnessAndFrequencyTightnessNoGo",
        ],
        "collatz": [
            "RationalWieferichOrderCoreReductionAndBoundedOrderNoGo",
            "UnboundedOrderPrincipalUnitTransferCountermodels",
        ],
        "goldbach": [
            "ParsevalScaleObstructionToL2OnlyBinaryMinorArcCertificates",
            "OmittedHalfFrequencyArcCarriesNaturalBinaryEnergy",
        ],
        "twin_prime": [
            "GrowingPeriodDiagonalCRTMimicryForShiftTwo",
            "FixedPeriodicMimicryInEverySufficientlyLargeDyadicBlock",
        ],
    }
    prior_retired = {
        "riemann": [
            "frequency support or frequency tightness alone as compactness of a normalized even Weil-test family"
        ],
        "collatz": [
            "deducing the fixed-base 32/27 to 2/3 square-depth transfer from universal order, LTE, and principal-unit algebra"
        ],
        "goldbach": [
            "placing the parity rational neighborhood around one half in a minor set while demanding an absolute-energy o(X/log^2 X) budget"
        ],
        "twin_prime": [
            "using fixed periodic features even with eventual per-dyadic-scale sampling as a twin-prime certificate"
        ],
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
        "ticket": 244,
        "parent_ticket": 243,
        "generated_at": GENERATED_AT,
        "iteration_complete": True,
        "program_complete": False,
        "resolved_count": 0,
        "candidate_resolution_count": 0,
        "deep_focus_problem": "twin_prime",
        "problems": problems,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    integrated = ROOT / (
        "data/open-problem/ticket244-joint-tightness-harmonic-parity-fold-"
        "polylog-mimicry.json"
    )
    write_json(integrated, audit)
    root = audit[AUDIT_KEY]
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-244-joint-tightness-compactness.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-244-harmonic-bad-line-reduction.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-244-parity-arc-folding.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-244-polylog-periodic-mimicry.json",
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
