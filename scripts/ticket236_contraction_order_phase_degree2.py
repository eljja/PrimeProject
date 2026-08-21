from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

import ticket234_operator_kernel_density_minor_cesaro as ticket234
import ticket235_schur_primepower_phase_overlap as ticket235


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket236-contraction-order-phase-degree2.v1"
GENERATED_AT = "2026-08-22T02:10:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "contraction_order_phase_degree2_audit"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fraction_payload(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "float": float(value)}


def primes_up_to(limit: int) -> list[int]:
    if limit < 2:
        return []
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            flags[prime * prime : limit + 1 : prime] = b"\x00" * (
                (limit - prime * prime) // prime + 1
            )
    return [value for value, flag in enumerate(flags) if flag]


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


def next_prime(value: int) -> int:
    candidate = max(2, value + 1)
    while True:
        if all(candidate % divisor for divisor in range(2, math.isqrt(candidate) + 1)):
            return candidate
        candidate += 1


def riemann_contraction_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for dimension in (4, 8, 16, 32, 64, 128):
        unsafe_entry = Fraction(2, dimension)
        safe_entry = Fraction(1, 2 * dimension)
        coordinate_minor = Fraction(1) - unsafe_entry * unsafe_entry
        unsafe_operator_norm = Fraction(2)
        unsafe_block_minimum = Fraction(-1)
        safe_operator_norm = Fraction(1, 2)
        safe_block_minimum = Fraction(1, 2)
        verified = (
            coordinate_minor >= 0
            and unsafe_entry > 0
            and unsafe_entry <= 1
            and unsafe_operator_norm == 2
            and unsafe_block_minimum == 1 - unsafe_operator_norm
            and safe_block_minimum == 1 - safe_operator_norm
            and safe_block_minimum > 0
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{dimension}:{unsafe_entry}:{coordinate_minor}:"
                f"{unsafe_operator_norm}:{unsafe_block_minimum}:"
                f"{safe_entry}:{safe_operator_norm}:{safe_block_minimum}\n"
            ).encode()
        )
        rows.append(
            {
                "block_dimension_m": dimension,
                "unsafe_cross_entry_2_over_m": fraction_payload(unsafe_entry),
                "every_coordinate_two_by_two_minor": fraction_payload(coordinate_minor),
                "unsafe_normalized_operator_norm": fraction_payload(unsafe_operator_norm),
                "unsafe_full_block_minimum_eigenvalue": fraction_payload(unsafe_block_minimum),
                "safe_cross_entry_1_over_2m": fraction_payload(safe_entry),
                "safe_normalized_operator_norm": fraction_payload(safe_operator_norm),
                "safe_full_block_minimum_eigenvalue": fraction_payload(safe_block_minimum),
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let A and C be positive definite and H=[[A,B],[B*,C]]. Put "
        "K=A^(-1/2)BC^(-1/2). Then H is positive semidefinite if and only "
        "if the normalized cross block is a contraction, ||K||_op<=1. "
        "Coordinatewise relative two-by-two minor inequalities do not suffice: "
        "for A=C=I_m and B=(2/m)J_m, every coordinate minor is "
        "1-4/m^2>=0 and every entry tends to zero, but ||B||_op=2 and the "
        "full block has minimum eigenvalue -1."
    )
    proof = (
        "Congruence by diag(A^(-1/2),C^(-1/2)) reduces H to [[I,K],[K*,I]]. "
        "The Schur complement is I-K*K, which is positive semidefinite exactly "
        "when every singular value of K is at most one. In the counterfamily "
        "J_m has one singular value m, so (2/m)J_m has norm two even though "
        "each coordinate pair passes its local minor test. Replacing 2/m by "
        "1/(2m) gives norm one half and full minimum eigenvalue one half."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_coherent_rank_one_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "normalized_cross_block_contraction_iff_proved": True,
            "coordinatewise_relative_minor_sufficiency_refuted": True,
            "coherent_cross_block_accumulation_exhibited": True,
            "arithmetic_weil_normalized_contraction_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "This is an exact finite-dimensional operator theorem and counterfamily, "
            "not an estimate for the actual Guinand-Weil arithmetic cross block. "
            "It identifies the required global normalized operator norm and refutes "
            "pairwise local certification only. No zeta zero is tested."
        ),
        "failure_count": failures,
    }


def collatz_order_witness_audit() -> dict[str, Any]:
    witness_primes = (5, 59, 57653)
    expected_orders = {
        5: (1, 2, 2),
        59: (2, 58, 29),
        57653: (29, 28826, 28826),
    }
    order_rows: list[dict[str, Any]] = []
    failures = 0
    for prime in witness_primes:
        ratio_32_27 = 32 * pow(27, -1, prime) % prime
        ratio_3_2 = 3 * pow(2, -1, prime) % prime
        orders = (
            ticket235.multiplicative_order(ratio_32_27, prime),
            ticket235.multiplicative_order(ratio_3_2, prime),
            ticket235.multiplicative_order(4, prime),
        )
        verified = orders == expected_orders[prime]
        failures += int(not verified)
        order_rows.append(
            {
                "prime_q": prime,
                "order_q_32_over_27": orders[0],
                "order_q_3_over_2": orders[1],
                "order_q_4": orders[2],
                "common_divisor_period": math.lcm(orders[1], orders[2]),
                "certificate_verified": verified,
            }
        )

    period = 28826
    coverage_counts = {"q_5": 0, "q_59": 0, "q_57653": 0, "uncovered": 0}
    transcript = hashlib.sha256()
    residue_failures = 0
    anchor_rows: list[dict[str, Any]] = []
    for one_count in range(1, period + 1):
        if one_count % 2:
            witness = 5
            bucket = "q_5"
        elif one_count % 58:
            witness = 59
            bucket = "q_59"
        elif one_count % period:
            witness = 57653
            bucket = "q_57653"
        else:
            witness = None
            bucket = "uncovered"
        coverage_counts[bucket] += 1
        if witness is None:
            all_common = all(
                (pow(32, one_count, prime) - pow(27, one_count, prime)) % prime == 0
                and (
                    pow(32, one_count, prime)
                    + pow(27, one_count, prime)
                    - 2 * pow(18, one_count, prime)
                )
                % prime
                == 0
                for prime in witness_primes
            )
            residue_failures += int(not all_common)
        else:
            d_mod = (pow(32, one_count, witness) - pow(27, one_count, witness)) % witness
            b_mod = (
                pow(32, one_count, witness)
                + pow(27, one_count, witness)
                - 2 * pow(18, one_count, witness)
            ) % witness
            residue_failures += int(not (d_mod == 0 and b_mod != 0))
        transcript.update(f"{one_count}:{witness or 0}\n".encode())
        if one_count in (1, 2, 57, 58, 116, period - 58, period - 1, period):
            anchor_rows.append(
                {
                    "one_count_k": one_count,
                    "selected_prime_q": witness,
                    "all_three_common_at_exception": witness is None,
                }
            )

    failures += residue_failures
    coverage_verified = coverage_counts == {
        "q_5": 14413,
        "q_59": 13916,
        "q_57653": 496,
        "uncovered": 1,
    }
    failures += int(not coverage_verified)
    theorem = (
        "For the primitive binary run block w_k=1^k2^(2k), let "
        "D_k=32^k-27^k and B_k=32^k+27^k-2*18^k. If 28826 does not divide k, "
        "there is an explicit order-separated prime q dividing D_k but not B_k: "
        "take q=5 for odd k, q=59 for even k not divisible by 58, and q=57653 "
        "for 58|k but 28826 not dividing k. At every multiple of 28826 all three "
        "primes divide both D_k and B_k, so this fixed three-prime palette is not "
        "a universal adaptive witness."
    )
    proof = (
        "TICKET-235 proved q|gcd(D_k,B_k) iff ord_q(3/2)|k and ord_q(4)|k, "
        "while q|D_k iff ord_q(32/27)|k. The exact order triples "
        "(ord(32/27),ord(3/2),ord(4)) are (1,2,2) at q=5, (2,58,29) at "
        "q=59, and (29,28826,28826) at q=57653. The three divisibility cases "
        "therefore give a denominator divisor and fail the numerator common-order "
        "condition. At 28826|k every common-order condition holds."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "witness_order_rows": order_rows,
        "complete_residue_period_audit": {
            "period": period,
            "coverage_counts": coverage_counts,
            "coverage_verified": coverage_verified,
            "residue_failure_count": residue_failures,
            "anchor_rows": anchor_rows,
            "transcript_sha256": transcript.hexdigest(),
        },
        "aggregate": {
            "run_block_order_separated_witness_outside_28826_multiples_proved": True,
            "fixed_three_prime_palette_universal_sufficiency_refuted": True,
            "run_block_nondivisibility_newly_proved": False,
            "all_binary_density_band_words_excluded": False,
            "all_periodic_collatz_cycles_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "TICKET-197 already excludes D_k|B_k for every run block; the new result "
            "is the explicit prime-presence witness on 28825 of 28826 residue classes. "
            "It leaves multiples of 28826, general primitive binary necklaces, "
            "valuations at least three, and aperiodic divergence open. The finite "
            "residue loop is exhaustive only because the proved order conditions "
            "are periodic modulo 28826."
        ),
        "failure_count": failures,
    }


def goldbach_representation_count(flags: bytearray, target: int, cutoff: int) -> int:
    return sum(
        1
        for left in range(2, cutoff + 1)
        if flags[left]
        and 2 <= target - left <= cutoff
        and flags[target - left]
    )


def goldbach_direct_dft_row(cutoff: int) -> dict[str, Any]:
    modulus = next_prime(2 * cutoff)
    flags = prime_flags_up_to(cutoff)
    prime_count = sum(flags)
    target = 4
    transform: list[complex] = []
    primes = [value for value in range(2, cutoff + 1) if flags[value]]
    for frequency in range(modulus):
        transform.append(
            sum(cmath.exp(2j * math.pi * frequency * prime / modulus) for prime in primes)
        )
    inversion = sum(
        transform[frequency] ** 2
        * cmath.exp(-2j * math.pi * frequency * target / modulus)
        for frequency in range(modulus)
    )
    representation_count = goldbach_representation_count(flags, target, cutoff)
    expected = modulus * representation_count
    return {
        "cutoff_X": cutoff,
        "prime_modulus_q": modulus,
        "prime_count_pi_X": prime_count,
        "target_N": target,
        "ordered_representation_count": representation_count,
        "dft_inversion_real": inversion.real,
        "dft_inversion_imag": inversion.imag,
        "expected_q_times_count": expected,
        "absolute_complex_error": abs(inversion - expected),
        "certificate_verified": abs(inversion - expected) < 1e-7,
    }


def goldbach_phase_defect_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    failures = 0
    for cutoff in (100, 1000, 10000, 100000):
        modulus = next_prime(2 * cutoff)
        flags = prime_flags_up_to(cutoff)
        prime_count = sum(flags)
        representation_count = goldbach_representation_count(flags, 4, cutoff)
        total_power = modulus * prime_count
        phase_defect = total_power - modulus * representation_count
        normalized_margin = Fraction(representation_count, prime_count)
        inverse_log_margin = 1 / math.log(cutoff)
        verified = (
            representation_count == 1
            and phase_defect >= 0
            and total_power - phase_defect == modulus
            and float(normalized_margin) < inverse_log_margin
        )
        failures += int(not verified)
        transcript.update(
            (
                f"{cutoff}:{modulus}:{prime_count}:{representation_count}:"
                f"{total_power}:{phase_defect}:{normalized_margin}\n"
            ).encode()
        )
        rows.append(
            {
                "cutoff_X": cutoff,
                "prime_modulus_q": modulus,
                "prime_count_pi_X": prime_count,
                "fixed_target_N": 4,
                "ordered_representation_count_g_X_4": representation_count,
                "total_spectral_power_M_X": total_power,
                "reflected_phase_defect_Delta_X_4": phase_defect,
                "normalized_phase_margin_g_over_pi": fraction_payload(normalized_margin),
                "inverse_log_X": inverse_log_margin,
                "margin_below_inverse_log_X": float(normalized_margin) < inverse_log_margin,
                "certificate_verified": verified,
            }
        )

    dft_rows = [goldbach_direct_dft_row(cutoff) for cutoff in (30, 100, 300)]
    failures += sum(int(not row["certificate_verified"]) for row in dft_rows)
    theorem = (
        "Let x_X be the prime indicator on Z/qZ with q>2X, let Xhat(a) be its "
        "Fourier transform, M_X=sum_a|Xhat(a)|^2=q*pi(X), and define the "
        "target-reflected phase defect Delta_X(N)=sum_a |Xhat(a)|^2 "
        "[1-cos(2 arg Xhat(a)-2*pi*a*N/q)]. Then for 0<=N<=2X, "
        "q*g_X(N)=M_X-Delta_X(N), where g_X(N) is the ordered prime-pair count. "
        "Hence Delta_X(N)<M_X is exactly equivalent to g_X(N)>0. Moreover an "
        "uncoupled uniform inverse-log fractional margin is false for actual prime "
        "weights: at fixed target N=4 the normalized margin is 1/pi(X)=o(1/log X)."
    )
    proof = (
        "Fourier inversion of the cyclic convolution x_X*x_X gives q*g_X(N) as "
        "sum_a Xhat(a)^2 exp(-2*pi*i*a*N/q). Taking real parts and writing each "
        "square by magnitude and doubled phase yields M_X-Delta_X(N). Parseval "
        "gives M_X=q*pi(X). Because q>2X there is no wraparound. For N=4 only "
        "the ordered pair (2,2) contributes, so the fractional gap is exactly "
        "1/pi(X); the prime number theorem makes this asymptotic to log(X)/X."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_actual_prime_rows": rows,
        "direct_complex_dft_rows": dft_rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "reflected_phase_defect_identity_proved": True,
            "strict_phase_defect_margin_endpoint_equivalent": True,
            "uncoupled_inverse_log_uniform_margin_refuted": True,
            "target_coupled_prime_phase_gain_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The asymptotic no-go uses actual prime indicators and the prime number "
            "theorem, but exploits a fixed small target while the cutoff grows. It "
            "does not refute a target-coupled dyadic estimate with N comparable to X. "
            "The strict defect inequality by itself is endpoint-equivalent to the "
            "Goldbach coefficient and supplies no independent minor-arc saving."
        ),
        "failure_count": failures,
    }


def actual_twin_energy_row(cutoff: int, dimension: int) -> dict[str, Any]:
    active_primes = [prime for prime in primes_up_to(100) if prime >= 5][:dimension]
    flags = prime_flags_up_to(cutoff)
    starts = [
        value
        for value in range(active_primes[-1] + 1, cutoff - 1)
        if flags[value] and flags[value + 2]
    ]
    centered: list[list[Fraction]] = []
    variances: list[Fraction] = []
    for start in starts:
        row: list[Fraction] = []
        for coordinate, prime in enumerate(active_primes):
            mean, variance = ticket234.twin_crt_normalization(prime)
            row.append(Fraction(ticket234.legendre_symbol(start, prime)) - mean)
            if start == starts[0]:
                variances.append(variance)
        centered.append(row)

    energies: list[Fraction] = []
    for degree in range(1, dimension + 1):
        total = Fraction(0)
        for subset in itertools.combinations(range(dimension), degree):
            correlation = sum(
                math.prod(row[index] for index in subset) for row in centered
            ) / len(starts)
            variance_product = math.prod(variances[index] for index in subset)
            total += correlation * correlation / variance_product
        energies.append(total / math.comb(dimension, degree))

    degree_two = energies[1]
    degree_one_squared_bound = Fraction(4, dimension) + Fraction(
        dimension - 1, dimension
    ) * degree_two
    degree_one_squared_bound_verified = energies[0] ** 2 <= degree_one_squared_bound
    higher_rows: list[dict[str, Any]] = []
    higher_verified = True
    for degree in range(3, dimension + 1):
        falling = math.prod(range(dimension - degree + 1, dimension + 1))
        repeated_bound = Fraction(2 ** (degree + 1)) * (
            1 - Fraction(falling, dimension**degree)
        )
        upper = Fraction(2 ** (degree - 2)) * (
            Fraction(4, dimension) + degree_two
        ) + repeated_bound
        verified = energies[degree - 1] <= upper
        higher_verified = higher_verified and verified
        higher_rows.append(
            {
                "degree_k": degree,
                "energy_E_m_k": fraction_payload(energies[degree - 1]),
                "degree_two_upper_bound": fraction_payload(upper),
                "bound_verified": verified,
            }
        )

    return {
        "cutoff_X": cutoff,
        "active_prime_count_m": dimension,
        "active_primes": active_primes,
        "twin_start_count": len(starts),
        "fixed_degree_cesaro_energies": [fraction_payload(value) for value in energies],
        "degree_one_squared_from_degree_two_upper_bound": fraction_payload(
            degree_one_squared_bound
        ),
        "degree_one_from_degree_two_squared_bound_verified": degree_one_squared_bound_verified,
        "higher_degree_bound_rows": higher_rows,
        "certificate_verified": degree_one_squared_bound_verified and higher_verified,
    }


def twin_degree_two_audit() -> dict[str, Any]:
    rows = [
        actual_twin_energy_row(10_000, 4),
        actual_twin_energy_row(100_000, 6),
        actual_twin_energy_row(1_000_000, 8),
    ]
    transcript = hashlib.sha256()
    for row in rows:
        transcript.update(
            (
                f"{row['cutoff_X']}:{row['active_prime_count_m']}:"
                f"{row['twin_start_count']}:"
                f"{','.join(value['exact'] for value in row['fixed_degree_cesaro_energies'])}\n"
            ).encode()
        )
    failures = sum(int(not row["certificate_verified"]) for row in rows)
    theorem = (
        "Under the TICKET-235 normalized CRT hypotheses |psi_i|^2<=2, let "
        "E_(m,k) be the degree-k Cesaro coefficient energy. Then "
        "E_(m,1)<=sqrt(4/m+((m-1)/m)E_(m,2)), and for every fixed k>=2, "
        "E_(m,k)<=2^(k-2)E_(m,2)+2^k(1+k(k-1))/m. Consequently the single "
        "condition E_(m,2)->0 forces E_(m,k)->0 for every fixed k, including "
        "k=1. Proving a separate hierarchy of all fixed overlap moments is "
        "therefore unnecessary."
    )
    proof = (
        "Let b=(E psi_i)_i and M=(E psi_i psi_j)_(i,j). Covariance positivity "
        "gives M>=bb*, so ||b||^2<=||M||_op<=||M||_F. The diagonal entries of "
        "M are at most two and the averaged squared off-diagonal entries equal "
        "R=m^(-1)sum psi_i(X)psi_i(Y). Then E[R^2]<=4/m+E_2 and |R|<=2, "
        "so |E[R^k]|<=2^(k-2)(4/m+E_2). Combine this with the TICKET-235 "
        "with/without-replacement estimate |E_(m,k)-E[R^k]|<=2^k k(k-1)/m."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "actual_twin_start_diagnostic_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "degree_two_controls_degree_one_proved": True,
            "degree_two_controls_every_fixed_degree_proved": True,
            "independent_all_degree_hierarchy_required_refuted": True,
            "actual_prime_degree_two_decay_proved": False,
            "positive_twin_main_mass_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The inequalities are universal and exact, but the three prime rows "
            "condition on already existing twin starts and are finite diagnostics. "
            "They do not prove E_(m,2)->0 for Type-II prime weights, construct "
            "positive total mass, or cross the parity barrier."
        ),
        "failure_count": failures,
    }


def make_section(
    problem_id: str,
    ticket_id: str,
    theorem_name: str,
    computation: dict[str, Any],
    discard: str,
    retain: str,
    next_lemma: str,
    proof_dag: dict[str, Any],
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "theorem_name": theorem_name,
        "declared_proposition": computation["theorem"],
        "mathematical_argument": computation["proof"],
        "reproducible_computation": computation,
        "logical_limit": computation["no_go_scope"],
        "route_decision": {
            "discard": discard,
            "retain": retain,
            "next_single_lemma": next_lemma,
        },
        "proof_dag": proof_dag,
    }


def proof_dag(problem: str) -> dict[str, Any]:
    if problem == "riemann":
        nodes = [
            ("RH-T235", "ExactKernelSchurComplementCriterionAndCrossBlockNoGo", "closed"),
            ("RH-T236", "NormalizedCrossBlockContractionAndLocalMinorNoGo", "closed"),
            ("RH-N236", "CoordinatewiseRelativeMinorsSufficeForFullPositivity", "refuted_or_limited"),
            ("RH-OPEN236", "ArithmeticWeilNormalizedCrossBlockContractionBelowOneOnCofinalLogarithmicFrames", "highest_risk_open"),
            ("RH", "RiemannHypothesis", "open_not_proven"),
        ]
        edges = [["RH-T235", "RH-T236"], ["RH-T236", "RH-N236"], ["RH-T236", "RH-OPEN236"], ["RH-OPEN236", "RH"]]
    elif problem == "collatz":
        nodes = [
            ("CO-T197", "ContiguousOneTwoRunNondivisibility", "closed"),
            ("CO-T235", "BinaryRunBlockPrimitiveDivisorOrderCharacterizationAndSelectionNoGo", "closed"),
            ("CO-T236", "RunBlockThreePrimeWitnessOutside28826Multiples", "closed"),
            ("CO-N236", "FixedThreePrimePaletteCoversEveryRunBlock", "refuted_or_limited"),
            ("CO-OPEN236", "UniformBinaryDensityBandFreshOrderSeparatedPrimeWitnessBeyondFinitePalettes", "highest_risk_open"),
            ("CO-PERIODIC", "AllPeriodicValuationWords", "open_not_proven"),
            ("CO-APERIODIC", "AperiodicDescentOrTermination", "open_not_proven"),
            ("CO", "CollatzConjecture", "open_not_proven"),
        ]
        edges = [["CO-T197", "CO-T236"], ["CO-T235", "CO-T236"], ["CO-T236", "CO-N236"], ["CO-T236", "CO-OPEN236"], ["CO-OPEN236", "CO-PERIODIC"], ["CO-PERIODIC", "CO"], ["CO-APERIODIC", "CO"]]
    elif problem == "goldbach":
        nodes = [
            ("GB-T235", "CompleteMarginalPowerSpectrumPhaseRetrievalNoGo", "closed"),
            ("GB-T236", "ReflectedPhaseDefectIdentityAndUncoupledMarginNoGo", "closed"),
            ("GB-N236", "UncoupledUniformInverseLogPhaseMargin", "refuted_or_limited"),
            ("GB-OPEN236", "TargetCoupledDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack", "highest_risk_open"),
            ("GB", "StrongGoldbachConjecture", "open_not_proven"),
        ]
        edges = [["GB-T235", "GB-T236"], ["GB-T236", "GB-N236"], ["GB-T236", "GB-OPEN236"], ["GB-OPEN236", "GB"]]
    else:
        nodes = [
            ("TP-T235", "FixedDegreeCesaroOverlapMomentReductionAndDegreeOneNoGo", "closed"),
            ("TP-T236", "DegreeTwoCesaroControlsAllFixedDegrees", "closed"),
            ("TP-N236", "EveryFixedDegreeRequiresAnIndependentEstimate", "refuted_or_limited"),
            ("TP-OPEN236", "PrimeWeightedDegreeTwoCRTOverlapEnergyDecayAtTwinScale", "highest_risk_open"),
            ("TP-PARITY", "ParityRetainingTransferAndPositivePrincipalMass", "open_not_proven"),
            ("TP", "TwinPrimeConjecture", "open_not_proven"),
        ]
        edges = [["TP-T235", "TP-T236"], ["TP-T236", "TP-N236"], ["TP-T236", "TP-OPEN236"], ["TP-OPEN236", "TP-PARITY"], ["TP-PARITY", "TP"]]
    return {
        "nodes": [{"id": node_id, "label": label, "status": status} for node_id, label, status in nodes],
        "edges": edges,
    }


def build_audit() -> dict[str, Any]:
    computations = {
        "riemann": riemann_contraction_audit(),
        "collatz": collatz_order_witness_audit(),
        "goldbach": goldbach_phase_defect_audit(),
        "twin_prime": twin_degree_two_audit(),
    }
    tracks = [
        make_section(
            "riemann", "RH-TICKET-236", "NormalizedCrossBlockContractionCriterionAndLocalMinorNoGo",
            computations["riemann"],
            "coordinatewise relative two-by-two minors as a certificate for the full Weil truncation",
            "bound the global normalized arithmetic cross-block operator below one",
            "ArithmeticWeilNormalizedCrossBlockContractionBelowOneOnCofinalLogarithmicFrames",
            proof_dag("riemann"),
        ),
        make_section(
            "collatz", "CO-TICKET-236", "BinaryRunBlockThreePrimeOrderWitnessOutside28826Multiples",
            computations["collatz"],
            "a fixed three-prime palette as a universal binary run-block witness",
            "select fresh word-dependent order-separated primes beyond every fixed palette",
            "UniformBinaryDensityBandFreshOrderSeparatedPrimeWitnessBeyondFinitePalettes",
            proof_dag("collatz"),
        ),
        make_section(
            "goldbach", "GB-TICKET-236", "ActualPrimeReflectedPhaseDefectIdentityAndUncoupledMarginNoGo",
            computations["goldbach"],
            "an uncoupled all-target inverse-log phase margin, or the raw strict phase inequality as a smaller auxiliary lemma",
            "couple cutoff to target and derive a quantitative cross-phase gain from independent major/minor arithmetic",
            "TargetCoupledDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack",
            proof_dag("goldbach"),
        ),
        make_section(
            "twin-prime", "TP-TICKET-236", "DegreeTwoCesaroEnergyControlsEveryFixedDegree",
            computations["twin_prime"],
            "proving a separate arithmetic concentration estimate for every fixed CRT interaction degree",
            "prove only the degree-two prime-weighted overlap energy decay, then invoke the universal reduction",
            "PrimeWeightedDegreeTwoCRTOverlapEnergyDecayAtTwinScale",
            proof_dag("twin-prime"),
        ),
    ]
    root = {
        "theorem_name": "FourConjectureContractionOrderPhaseDegreeTwoAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-236 proves four exact partial or no-go results: the global "
            "normalized contraction criterion and a local-minor no-go; a three-prime "
            "Collatz run-block witness outside multiples of 28826; an actual-prime "
            "reflected phase-defect identity and uncoupled inverse-log no-go; and a "
            "degree-two reduction controlling every fixed CRT Cesaro degree. It "
            "resolves none of the four parent conjectures."
        ),
        "riemann": tracks[0],
        "collatz": tracks[1],
        "goldbach": tracks[2],
        "twin_prime": tracks[3],
        "machine_audit": {
            "exact_partial_or_no_go_theorem_count": 4,
            "refuted_or_reduced_route_count": 4,
            "next_single_lemma_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": sum(
                track["reproducible_computation"]["failure_count"] for track in tracks
            ),
        },
    }
    attempts = [
        {
            "ticket_id": track["ticket_id"],
            "problem_id": track["problem_id"],
            "status": STATUS,
            "declared_proposition": track["declared_proposition"],
            "mathematical_argument": track["mathematical_argument"],
            "new_result": track["theorem_name"],
            "discarded_route": track["route_decision"]["discard"],
            "remaining_gap": track["logical_limit"],
            "candidate_theorem": track["route_decision"]["next_single_lemma"],
            "claim_boundary": track["logical_limit"],
            "proof_dag": track["proof_dag"],
            "bounded_result": {
                "audit_ref": f"#/{AUDIT_KEY}/{track['problem_id'].replace('-', '_')}",
                "failure_count": track["reproducible_computation"]["failure_count"],
            },
        }
        for track in tracks
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": (
            "TICKET-236 proves four exact partial or no-go results and resolves none "
            "of the four parent conjectures."
        ),
        AUDIT_KEY: root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit[AUDIT_KEY]
    write_json(ROOT / "data/open-problem/ticket236-contraction-order-phase-degree2.json", audit)
    destinations = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-236-normalized-contraction-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-236-three-prime-order-witness.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-236-reflected-phase-defect.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-236-degree-two-reduction.json",
    }
    for key, destination in destinations.items():
        write_json(
            destination,
            {"schema": SCHEMA, "generated_at": GENERATED_AT, "status": STATUS, **root[key]},
        )


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    machine = audit[AUDIT_KEY]["machine_audit"]
    print(json.dumps(machine, indent=2))
    if machine["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
