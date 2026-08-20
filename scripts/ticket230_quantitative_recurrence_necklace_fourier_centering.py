from __future__ import annotations

import cmath
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket226_signal_transfer_same_order_obstructions import is_primitive_word


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket230-quantitative-recurrence-necklace-fourier-centering.v1"
GENERATED_AT = "2026-08-20T12:00:00+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def proof_dag(
    prefix: str,
    previous: str,
    closed: str,
    no_go: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T229", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T230", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N230",
                "label": no_go,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN230",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T229", f"{prefix}-T230"],
            [f"{prefix}-T230", f"{prefix}-N230"],
            [f"{prefix}-T230", f"{prefix}-OPEN230"],
            [f"{prefix}-OPEN230", prefix],
        ],
    }


def torus_distance(value: float) -> float:
    return abs(value - round(value))


def certificate_float(value: float) -> float:
    """Normalize diagnostic floats across conforming Python/libm builds."""
    return float(format(value, ".14g"))


def dual_dilation_energy(primes: tuple[int, ...], frequency: int) -> float:
    return sum(
        4.0 * math.sin(0.5 * frequency * math.log(prime)) ** 2
        for prime in primes
    )


def pigeonhole_witness(primes: tuple[int, ...], partition: int) -> dict[str, Any]:
    dimension = len(primes)
    alphas = [math.log(prime) / (2.0 * math.pi) for prime in primes]
    boxes: dict[tuple[int, ...], int] = {}
    maximum_index = partition**dimension
    for index in range(maximum_index + 1):
        coordinates = [(index * alpha) % 1.0 for alpha in alphas]
        box = tuple(
            min(partition - 1, int(math.floor(coordinate * partition)))
            for coordinate in coordinates
        )
        previous = boxes.get(box)
        if previous is None:
            boxes[box] = index
            continue
        witness = index - previous
        phase_errors = [torus_distance(witness * alpha) for alpha in alphas]
        energy = dual_dilation_energy(primes, witness)
        bound = 4.0 * math.pi**2 * dimension / partition**2
        sequence_bound = 4.0 * math.pi**2 * dimension * witness ** (-2.0 / dimension)
        return {
            "primes": list(primes),
            "dimension_m": dimension,
            "partition_Q": partition,
            "maximum_index_Q_to_m": maximum_index,
            "collision_indices": [previous, index],
            "witness_frequency_n": witness,
            "maximum_phase_error": max(phase_errors),
            "phase_errors": phase_errors,
            "dual_energy": certificate_float(energy),
            "dirichlet_energy_bound": bound,
            "sequence_rate_bound": sequence_bound,
            "phase_bound_verified": max(phase_errors) <= 1.0 / partition + 1e-12,
            "energy_bound_verified": energy <= bound + 1e-11,
            "frequency_bound_verified": 1 <= witness <= maximum_index,
            "sequence_rate_verified": energy <= sequence_bound + 1e-11,
        }
    raise AssertionError("pigeonhole collision missing")


def riemann_quantitative_recurrence_audit() -> dict[str, Any]:
    rows = []
    failures = 0
    schedules = {
        (2, 3): (4, 8, 16, 32, 64, 128),
        (2, 3, 5): (4, 6, 8, 12, 16, 24),
    }
    for primes, partitions in schedules.items():
        for partition in partitions:
            row = pigeonhole_witness(primes, partition)
            rows.append(row)
            failures += int(
                not (
                    row["phase_bound_verified"]
                    and row["energy_bound_verified"]
                    and row["frequency_bound_verified"]
                    and row["sequence_rate_verified"]
                )
            )

    theorem = (
        "Let q_1,...,q_m be fixed integers greater than one, with m at least "
        "two and with two multiplicatively independent members, and put "
        "F(t)=sum_j |1-q_j^(-it)|^2. For every integer Q at least two there "
        "is an integer 1<=n<=Q^m such that F(n)<=4*pi^2*m/Q^2. These "
        "witnesses contain an unbounded subsequence and hence "
        "F(n)<=4*pi^2*m*n^(-2/m) along an unbounded sequence. Therefore no "
        "global lower floor L(t) with t^(2/m)L(t) tending to infinity can "
        "hold for a fixed finite dilation family."
    )
    proof = (
        "Apply the simultaneous Dirichlet pigeonhole argument to the Q^m+1 "
        "points k(log q_1/(2*pi),...,log q_m/(2*pi)) modulo one, partitioned "
        "into Q^m cubes of side 1/Q. The difference n of two points in one "
        "cube has every phase distance at most 1/Q. Since "
        "|1-exp(-2*pi*i*x)|^2=4*sin^2(pi*x)<=4*pi^2||x||^2, the stated "
        "energy bound follows. The witnesses cannot remain bounded as "
        "Q grows: otherwise a fixed positive n would have zero energy, "
        "forcing log(q_a)/log(q_b) rational for two multiplicatively "
        "independent members. Finally n<=Q^m implies Q^(-2)<=n^(-2/m)."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "pigeonhole_rows": rows,
        "exact_constants": {
            "energy_bound": "4*pi^2*m/Q^2",
            "unbounded_sequence_bound": "4*pi^2*m*n^(-2/m)",
        },
        "aggregate": {
            "quantitative_finite_dilation_recurrence_proved": True,
            "slower_than_T_minus_2_over_m_global_floor_refuted": True,
            "qualitative_subexponential_label_is_sufficient_refuted": True,
            "infinite_or_adaptive_weil_frame_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "This theorem concerns the scalar dilation phase energy, not the "
            "full Weil quadratic form. It gives a necessary recurrence-scale "
            "compatibility condition; it neither constructs an infinite or "
            "adaptive frame nor bounds the actual Weil-core tail."
        ),
        "failure_count": failures,
    }


def collatz_denominator(word: tuple[int, ...]) -> int:
    return 2 ** sum(word) - 3 ** len(word)


def collatz_numerator(word: tuple[int, ...]) -> int:
    total = 0
    prefix = 0
    height = len(word)
    for index, exponent in enumerate(word):
        total += 3 ** (height - index - 1) * 2**prefix
        prefix += exponent
    return total


def rotate_left(word: tuple[int, ...], amount: int = 1) -> tuple[int, ...]:
    amount %= len(word)
    return word[amount:] + word[:amount]


def canonical_necklace(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(rotate_left(word, amount) for amount in range(len(word)))


def collatz_necklace_rotation_audit() -> dict[str, Any]:
    failures = 0
    height_rows = []
    sample_rows = []
    for height in range(1, 7):
        primitive_positive = []
        necklaces: dict[tuple[int, ...], tuple[int, ...]] = {}
        divisible_necklaces: set[tuple[int, ...]] = set()
        for word in itertools.product(range(1, 6), repeat=height):
            if not is_primitive_word(word):
                continue
            denominator = collatz_denominator(word)
            if denominator <= 0:
                continue
            numerator = collatz_numerator(word)
            primitive_positive.append(word)
            necklace = canonical_necklace(word)
            necklaces.setdefault(necklace, word)
            if numerator % denominator == 0:
                divisible_necklaces.add(necklace)

            current = word
            current_numerator = numerator
            base_gcd = math.gcd(denominator, numerator)
            rotation_ok = True
            for _ in range(height):
                rotated = rotate_left(current)
                rotated_numerator = collatz_numerator(rotated)
                identity_ok = (
                    2 ** current[0] * rotated_numerator
                    == 3 * current_numerator + denominator
                )
                gcd_ok = math.gcd(denominator, rotated_numerator) == base_gcd
                divisibility_ok = (
                    current_numerator % denominator == 0
                ) == (rotated_numerator % denominator == 0)
                rotation_ok &= identity_ok and gcd_ok and divisibility_ok
                current = rotated
                current_numerator = rotated_numerator
            failures += int(not rotation_ok)
            if len(sample_rows) < 24:
                sample_rows.append(
                    {
                        "word": list(word),
                        "height_h": height,
                        "valuation_sum_S": sum(word),
                        "denominator_D": denominator,
                        "numerator_B": numerator,
                        "canonical_necklace": list(necklace),
                        "gcd_D_B": base_gcd,
                        "D_divides_B": numerator % denominator == 0,
                        "all_rotation_identities_verified": rotation_ok,
                    }
                )
        height_rows.append(
            {
                "height_h": height,
                "alphabet": [1, 2, 3, 4, 5],
                "primitive_positive_denominator_word_count": len(primitive_positive),
                "canonical_necklace_count": len(necklaces),
                "divisible_necklace_count": len(divisible_necklaces),
                "rotation_reduction_factor": (
                    len(primitive_positive) / len(necklaces) if necklaces else 0.0
                ),
            }
        )

    theorem = (
        "For an accelerated Collatz valuation word a=(a_0,...,a_(h-1)), "
        "write S=sum a_j, D=2^S-3^h, and "
        "B=sum_(j=0)^(h-1) 3^(h-1-j)2^(a_0+...+a_(j-1)). If rho a is "
        "the left cyclic rotation, then 2^(a_0)B(rho a)=3B(a)+D. When "
        "D>0, gcd(D,B(rho a))=gcd(D,B(a)), and D divides B(rho a) if and "
        "only if D divides B(a). Thus cycle divisibility is a necklace "
        "invariant and checking every rotation supplies no independent "
        "evidence."
    )
    proof = (
        "Separate the first term of B(a): B(a)=3^(h-1)+2^(a_0)C. Directly "
        "expanding the rotated numerator gives B(rho a)=3C+2^(S-a_0). "
        "Multiplication by 2^(a_0) yields 3B(a)+2^S-3^h=3B(a)+D. The odd "
        "integer D is coprime to 2, and D is also coprime to 3 because "
        "D is congruent to 2^S modulo 3. Multiplication by 2^(a_0) or by "
        "3 is therefore invertible modulo D, proving both invariances."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "height_rows": height_rows,
        "sample_rotation_rows": sample_rows,
        "aggregate": {
            "rotation_numerator_identity_proved": True,
            "cycle_divisibility_necklace_invariance_proved": True,
            "gcd_necklace_invariance_proved": True,
            "independent_rotation_search_information_refuted": True,
            "all_primitive_necklaces_excluded": False,
            "aperiodic_descent_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem quotients the finite-cycle search by cyclic symmetry. "
            "It does not prove D does not divide B for every primitive "
            "positive-denominator necklace, and even that stronger result "
            "would not exclude divergent aperiodic trajectories."
        ),
        "failure_count": failures,
    }


def direct_cyclic_convolution(weights: list[int], target: int) -> int:
    modulus = len(weights)
    return sum(
        weights[index] * weights[(target - index) % modulus]
        for index in range(modulus)
    )


def goldbach_modewise_counterexample_audit() -> dict[str, Any]:
    failures = 0
    rows = []
    for spike_scale in (2, 3, 4, 5, 8, 16, 32):
        modulus = spike_scale**2
        spike_location = 1
        weights = [1] * modulus
        weights[spike_location] += spike_scale
        mass = sum(weights)
        target = 2 * spike_location
        convolution = direct_cyclic_convolution(weights, target)
        principal = mass * mass // modulus
        aligned_error = convolution - principal
        expected_convolution = 2 * spike_scale**2 + 2 * spike_scale
        expected_principal = (spike_scale + 1) ** 2
        expected_error = spike_scale**2 - 1

        sample_modes = range(1, min(modulus, 17))
        mode_errors = []
        for mode in sample_modes:
            transform = sum(
                value * cmath.exp(-2j * math.pi * mode * index / modulus)
                for index, value in enumerate(weights)
            )
            mode_errors.append(abs(abs(transform) - spike_scale))
        fourier_verified = max(mode_errors or [0.0]) < 1e-9
        row_ok = (
            convolution == expected_convolution
            and principal == expected_principal
            and aligned_error == expected_error
            and fourier_verified
        )
        failures += int(not row_ok)
        rows.append(
            {
                "spike_scale_m": spike_scale,
                "cyclic_modulus_L_equals_m_squared": modulus,
                "total_mass_W": mass,
                "nonprincipal_mode_magnitude": spike_scale,
                "maximum_mode_to_mass_ratio": str(Fraction(1, spike_scale + 1)),
                "target_2a_convolution": convolution,
                "principal_term_W_squared_over_L": principal,
                "target_aligned_nonprincipal_error": aligned_error,
                "error_to_principal_ratio": str(Fraction(aligned_error, principal)),
                "sampled_fourier_formula_verified": fourier_verified,
            }
        )

    theorem = (
        "Modewise relative Fourier decay does not imply pointwise positivity "
        "of a growing cyclic convolution. For L=m^2 and "
        "w_m(x)=1+m*1_(x=a) on Z/LZ, the mass is W=m^2+m and every "
        "nonprincipal Fourier coefficient has magnitude m, so "
        "max|w_hat(k)|/W=1/(m+1) tends to zero. Nevertheless at target 2a, "
        "(w_m*w_m)(2a)=2m^2+2m while the principal term W^2/L is "
        "m^2+2m+1; all nonprincipal phases align and their error is m^2-1, "
        "of the same order as the main term."
    )
    proof = (
        "The transform of the constant background vanishes at every "
        "nonzero frequency, while the spike contributes "
        "m*exp(-2*pi*i*k*a/L). At target 2a, squaring this coefficient and "
        "multiplying by the inverse-transform phase cancels the phase for "
        "every k. The L-1 aligned terms contribute "
        "m^2(L-1)/L=m^2-1. Direct expansion of the convolution gives the "
        "same formula. Hence a separate o(W) estimate for each mode has no "
        "uniform pointwise consequence when the number of modes grows."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "counterexample_rows": rows,
        "aggregate": {
            "modewise_relative_decay_counterexample_proved": True,
            "target_phase_alignment_same_order_error_proved": True,
            "modewise_o_of_mass_implies_pointwise_positivity_refuted": True,
            "prime_specific_signed_minor_arc_bound_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The counterfamily is an information-theoretic obstruction, not "
            "a model of the primes and not a Goldbach counterexample. It "
            "shows that the remaining estimate must control the signed, "
            "target-aligned aggregate after a major/minor-arc decomposition; "
            "individual small modes are insufficient."
        ),
        "failure_count": failures,
    }


def quadratic_character(value: int, prime: int) -> int:
    residue = value % prime
    if residue == 0:
        return 0
    symbol = pow(residue, (prime - 1) // 2, prime)
    return -1 if symbol == prime - 1 else symbol


def prime_sieve(limit: int) -> bytearray:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if not sieve[prime]:
            continue
        start = prime * prime
        sieve[start : limit + 1 : prime] = b"\x00" * (
            (limit - start) // prime + 1
        )
    return sieve


def twin_local_centering_audit() -> dict[str, Any]:
    failures = 0
    local_rows = []
    for prime in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        shift = 2
        allowed = [
            residue
            for residue in range(prime)
            if residue % prime != 0 and (residue + shift) % prime != 0
        ]
        raw_sum = sum(quadratic_character(residue, prime) for residue in allowed)
        predicted_sum = -quadratic_character(-shift, prime)
        local_mean = Fraction(raw_sum, len(allowed))
        centered_sum = sum(
            Fraction(quadratic_character(residue, prime), 1) - local_mean
            for residue in allowed
        )
        verified = (
            len(allowed) == prime - 2
            and raw_sum == predicted_sum
            and centered_sum == 0
        )
        failures += int(not verified)
        local_rows.append(
            {
                "prime_l": prime,
                "shift_h": shift,
                "allowed_start_residues": allowed,
                "allowed_count_l_minus_2": len(allowed),
                "raw_quadratic_character_sum": raw_sum,
                "predicted_sum_minus_chi_of_minus_h": predicted_sum,
                "raw_local_mean": str(local_mean),
                "centered_character_sum": str(centered_sum),
                "identity_verified": verified,
            }
        )

    limit = 1_000_000
    sieve = prime_sieve(limit + 2)
    bounded_rows = []
    for checkpoint in (100, 1_000, 10_000, 100_000, 1_000_000):
        starts = [
            prime
            for prime in range(7, checkpoint - 1)
            if sieve[prime] and sieve[prime + 2]
        ]
        raw_sum = sum(quadratic_character(prime, 5) for prime in starts)
        count = len(starts)
        centered_sum = Fraction(raw_sum, 1) - Fraction(count, 3)
        allowed_verified = all(prime % 5 in (1, 2, 4) for prime in starts)
        failures += int(not allowed_verified)
        bounded_rows.append(
            {
                "search_limit": checkpoint,
                "twin_starts_above_five": count,
                "raw_mod5_quadratic_sum": raw_sum,
                "raw_sample_mean": str(Fraction(raw_sum, count)) if count else "n/a",
                "centered_sum_raw_minus_count_over_3": str(centered_sum),
                "all_starts_in_admissible_residues": allowed_verified,
                "finite_sample_only_not_asymptotic_proof": True,
            }
        )

    theorem = (
        "Let l be an odd prime, h nonzero modulo l, and let chi be a "
        "nonprincipal multiplicative character extended by chi(0)=0. On the "
        "shift-h admissible start set A={r: r is nonzero and r+h is "
        "nonzero}, one has sum_(r in A) chi(r)=-chi(-h), so the local mean "
        "is -chi(-h)/(l-2), generally not zero. For l=5, h=2, and the "
        "quadratic character, A={1,2,4} and the raw mean is 1/3. Therefore "
        "the uncentered target 'modulo-five quadratic cancellation to zero' "
        "is false already for complete admissible residue blocks."
    )
    proof = (
        "A is the complete residue system with 0 and -h removed. The sum of "
        "a nonprincipal multiplicative character over all residues is zero, "
        "and chi(0)=0, leaving -chi(-h). For l=5 and h=2, the quadratic "
        "values on 1,2,4 are 1,-1,1. Subtracting the mean 1/3 gives a "
        "centered observable with exact zero sum on every complete local "
        "block. This is a local identity only; it does not establish the "
        "distribution or infinitude of actual twin primes."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "local_character_rows": local_rows,
        "bounded_twin_sample_rows": bounded_rows,
        "mod5_exact_row": next(row for row in local_rows if row["prime_l"] == 5),
        "aggregate": {
            "shift_admissible_character_mean_formula_proved": True,
            "mod5_raw_quadratic_mean_equals_one_third_proved": True,
            "uncentered_zero_cancellation_target_refuted": True,
            "centered_prime_weighted_typeII_saving_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem corrects the local centering of the surviving mode. "
            "The finite twin counts are illustrative only. A proof still "
            "needs prime-weighted cancellation of the centered observable at "
            "the sieve main scale and an independent positive principal-mass "
            "lower bound overcoming the parity barrier."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_quantitative_recurrence_audit()
    collatz = collatz_necklace_rotation_audit()
    goldbach = goldbach_modewise_counterexample_audit()
    twin = twin_local_centering_audit()
    root = {
        "theorem_name": "QuantitativeRecurrenceNecklaceFourierAndCenteringCorrections",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-230 proves four exact structural or no-go theorems, "
            "corrects one malformed successor target, and resolves none of "
            "the four parent conjectures. Finite computations audit formulas "
            "and are not promoted to infinite claims."
        ),
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-230",
            "theorem_name": "QuantitativeFiniteDilationRecurrenceRateNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": riemann["no_go_scope"],
            "route_decision": {
                "discard": "treating a qualitative subexponential finite-family frame floor as sufficient without comparing it to the unavoidable T^(-2/m) recurrence scale",
                "retain": "use an infinite, weighted, or band-adaptive dilation family and compare its explicit floor against the actual Weil-core tail",
                "next_single_lemma": "AdaptiveInfiniteDilationFrameWithWeilTailDominanceBelowRecurrenceScale",
            },
            "proof_dag": proof_dag(
                "RH",
                "ExplicitFiniteBandDualDilationBoundAndPolynomialTailMismatch",
                "QuantitativeFiniteDilationRecurrenceRateNoGo",
                "SlowerThanTMinusTwoOverMFixedFamilyFrameFloor",
                "AdaptiveInfiniteDilationFrameWithWeilTailDominanceBelowRecurrenceScale",
                "RiemannHypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-230",
            "theorem_name": "CollatzCycleDivisibilityNecklaceInvariance",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": collatz["no_go_scope"],
            "route_decision": {
                "discard": "counting cyclic rotations of one valuation word as independent cycle-divisibility evidence",
                "retain": "quotient primitive positive-denominator words by necklaces before attacking D nondivisibility",
                "next_single_lemma": "NecklaceRepresentativeNondivisibilityForEveryPrimitivePositiveDenominatorWord",
            },
            "proof_dag": proof_dag(
                "CO",
                "FiniteEqualSlopeLanguageSemilinearCoverageNoGo",
                "CollatzCycleDivisibilityNecklaceInvariance",
                "IndependentCyclicRotationCycleEvidence",
                "NecklaceRepresentativeNondivisibilityForEveryPrimitivePositiveDenominatorWord",
                "CollatzConjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-230",
            "theorem_name": "ModewiseFourierDecayPointwisePositivityNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": goldbach["no_go_scope"],
            "route_decision": {
                "discard": "deducing pointwise Goldbach positivity from separate o(W) bounds for each of a growing number of Fourier modes",
                "retain": "control the target-aligned signed aggregate after an explicit major/minor-arc decomposition of prime weights",
                "next_single_lemma": "UniformBinaryPrimeMinorArcSignedAggregateBelowSingularSeriesMainTerm",
            },
            "proof_dag": proof_dag(
                "GB",
                "CompleteTargetPeriodCharacterCancellationAndPointwiseNoGo",
                "ModewiseFourierDecayPointwisePositivityNoGo",
                "ModewiseLittleOImpliesPointwiseBinaryConvolutionPositivity",
                "UniformBinaryPrimeMinorArcSignedAggregateBelowSingularSeriesMainTerm",
                "StrongGoldbachConjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-230",
            "theorem_name": "ShiftAdmissibleCharacterMeanAndModuloFiveCenteringCorrection",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": twin["no_go_scope"],
            "route_decision": {
                "discard": "forcing the raw modulo-five quadratic shift-two mode to cancel to zero instead of its admissibility mean one third",
                "retain": "subtract the exact local mean and seek a prime-weighted Type-II saving for the centered observable together with a positive principal lower bound",
                "next_single_lemma": "CenteredModFiveQuadraticTypeIISavingAtTwinSieveMainScale",
            },
            "proof_dag": proof_dag(
                "TP",
                "ShiftTwoParityProjectionAndModuloFiveQuadraticObstruction",
                "ShiftAdmissibleCharacterMeanAndModuloFiveCenteringCorrection",
                "RawModuloFiveQuadraticCancellationToZero",
                "CenteredModFiveQuadraticTypeIISavingAtTwinSieveMainScale",
                "TwinPrimeConjecture",
            ),
        },
    }
    tracks = ("riemann", "collatz", "goldbach", "twin_prime")
    total_failures = sum(
        root[key]["reproducible_computation"]["failure_count"] for key in tracks
    )
    root["machine_audit"] = {
        "exact_partial_theorem_count": 4,
        "refuted_or_corrected_route_count": 4,
        "next_single_lemma_count": 4,
        "proof_dag_count": 4,
        "conjecture_resolution_count": 0,
        "total_failure_count": total_failures,
    }
    attempts = []
    for key in tracks:
        track = root[key]
        attempts.append(
            {
                "problem_id": track["problem_id"],
                "ticket_id": track["ticket_id"],
                "status": STATUS,
                "declared_proposition": track["declared_proposition"],
                "mathematical_argument": track["mathematical_argument"],
                "new_result": track["theorem_name"],
                "bounded_result": {
                    "audit_ref": f"#/quantitative_recurrence_necklace_fourier_centering_audit/{key}",
                    "failure_count": track["reproducible_computation"]["failure_count"],
                },
                "discarded_route": track["route_decision"]["discard"],
                "remaining_gap": track["logical_limit"],
                "candidate_theorem": track["route_decision"]["next_single_lemma"],
                "proof_dag": track["proof_dag"],
            }
        )
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": (
            "TICKET-230 proves four exact partial results and resolves none "
            "of the four parent conjectures."
        ),
        "quantitative_recurrence_necklace_fourier_centering_audit": root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit["quantitative_recurrence_necklace_fourier_centering_audit"]
    write_json(
        ROOT
        / "data/open-problem/ticket230-quantitative-recurrence-necklace-fourier-centering.json",
        audit,
    )
    destinations = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-230-quantitative-recurrence.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-230-necklace-invariance.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-230-fourier-aggregate-no-go.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-230-local-centering-correction.json",
    }
    for key, destination in destinations.items():
        write_json(
            destination,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": STATUS,
                **root[key],
            },
        )


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    machine = audit["quantitative_recurrence_necklace_fourier_centering_audit"][
        "machine_audit"
    ]
    print(json.dumps(machine, indent=2))
    if machine["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
