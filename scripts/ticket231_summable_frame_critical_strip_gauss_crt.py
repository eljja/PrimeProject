from __future__ import annotations

import cmath
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket230_quantitative_recurrence_necklace_fourier_centering import (
    canonical_necklace,
    collatz_denominator,
    collatz_numerator,
    quadratic_character,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket231-summable-frame-critical-strip-gauss-crt.v1"
GENERATED_AT = "2026-08-21T12:00:00+09:00"
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
            {"id": f"{prefix}-T230", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T231", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N231",
                "label": no_go,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN231",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T230", f"{prefix}-T231"],
            [f"{prefix}-T231", f"{prefix}-N231"],
            [f"{prefix}-T231", f"{prefix}-OPEN231"],
            [f"{prefix}-OPEN231", prefix],
        ],
    }


def first_primes(count: int) -> tuple[int, ...]:
    values: list[int] = []
    candidate = 2
    while len(values) < count:
        if all(candidate % prime for prime in values if prime * prime <= candidate):
            values.append(candidate)
        candidate += 1
    return tuple(values)


def simultaneous_collision(
    dilations: tuple[int, ...], partition: int
) -> tuple[int, list[float]]:
    dimension = len(dilations)
    alphas = [math.log(value) / (2.0 * math.pi) for value in dilations]
    boxes: dict[tuple[int, ...], int] = {}
    for index in range(partition**dimension + 1):
        coordinates = [(index * alpha) % 1.0 for alpha in alphas]
        box = tuple(
            min(partition - 1, int(coordinate * partition))
            for coordinate in coordinates
        )
        if box in boxes:
            witness = index - boxes[box]
            errors = [
                abs(witness * alpha - round(witness * alpha)) for alpha in alphas
            ]
            return witness, errors
        boxes[box] = index
    raise AssertionError("simultaneous pigeonhole collision missing")


def weighted_energy(
    dilations: tuple[int, ...], weights: tuple[Fraction, ...], frequency: int
) -> float:
    return sum(
        float(weight)
        * abs(1.0 - cmath.exp(-1j * frequency * math.log(dilation))) ** 2
        for dilation, weight in zip(dilations, weights, strict=True)
    )


def riemann_summable_frame_audit() -> dict[str, Any]:
    primes = first_primes(12)
    rows = []
    failures = 0
    schedules = ((2, 64), (3, 24), (4, 10), (5, 6), (6, 4), (7, 3))
    for head_size, partition in schedules:
        head = primes[:head_size]
        weights = tuple(Fraction(1, 2**index) for index in range(1, head_size + 1))
        witness, errors = simultaneous_collision(head, partition)
        head_mass = sum(weights, Fraction(0))
        tail_mass = Fraction(1, 2**head_size)
        observed_head = weighted_energy(head, weights, witness)
        head_bound = 4.0 * math.pi**2 * float(head_mass) / partition**2
        total_upper_bound = head_bound + 4.0 * float(tail_mass)
        verified = (
            1 <= witness <= partition**head_size
            and max(errors) <= 1.0 / partition + 1e-12
            and observed_head <= head_bound + 1e-11
        )
        failures += int(not verified)
        rows.append(
            {
                "head_size_M": head_size,
                "partition_Q": partition,
                "dilations": list(head),
                "weights": [str(value) for value in weights],
                "head_weight_mass": str(head_mass),
                "exact_tail_weight_mass": str(tail_mass),
                "witness_frequency_n": witness,
                "maximum_frequency_Q_to_M": partition**head_size,
                "maximum_phase_error": max(errors),
                "observed_head_energy": observed_head,
                "head_energy_bound": head_bound,
                "full_infinite_energy_upper_bound": total_upper_bound,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "Let q_j>1 and w_j>=0 satisfy sum_j w_j<infinity, and suppose two "
        "positive-weight q_j are multiplicatively independent. Put "
        "F(n)=sum_j w_j|1-q_j^(-in)|^2. For every head size M and integer "
        "Q>=2 there is 1<=n<=Q^M with F(n)<=4*pi^2*Q^(-2)*"
        "sum_(j<=M)w_j+4*sum_(j>M)w_j. Consequently liminf_(n->infinity) "
        "F(n)=0. No fixed absolutely summable infinite dilation family has "
        "a positive uniform frame floor on the integer frequencies."
    )
    proof = (
        "Apply simultaneous pigeonhole approximation to the first M phase "
        "coordinates. The head contribution is at most 4*pi^2/Q^2 times "
        "its weight mass, while |1-z|^2<=4 bounds the tail. First choose M "
        "so the summable tail is arbitrarily small and then let Q grow. "
        "The witnesses are unbounded: otherwise a fixed positive integer "
        "would recur while the two independent positive-weight phases tend "
        "to zero, forcing both phases to vanish exactly and the ratio of "
        "their logarithms to be rational."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "weighted_head_tail_rows": rows,
        "aggregate": {
            "summable_infinite_dilation_liminf_zero_proved": True,
            "positive_uniform_floor_for_fixed_summable_frame_refuted": True,
            "height_adaptive_or_renormalized_frame_proved": False,
            "weil_positivity_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The result closes the naive fixed absolutely summable extension "
            "of TICKET-230. It concerns the dilation phase energy, not the "
            "full Weil quadratic form. Height-adaptive weights, a "
            "nonsummable renormalized family, and explicit Weil-tail "
            "dominance remain open."
        ),
        "failure_count": failures,
    }


def suffix_dominating_rotation(word: tuple[int, ...]) -> tuple[int, ...]:
    centered = tuple(value - 2 for value in word)
    cumulative = 0
    maximum = 0
    cut = 0
    for index, value in enumerate(centered, start=1):
        cumulative += value
        if cumulative > maximum:
            maximum = cumulative
            cut = index
    cut %= len(word)
    return word[cut:] + word[:cut]


def suffix_condition(word: tuple[int, ...]) -> bool:
    return all(
        sum(word[index:]) >= 2 * (len(word) - index)
        for index in range(len(word))
    )


def collatz_critical_strip_audit() -> dict[str, Any]:
    failures = 0
    height_rows = []
    samples = []
    for height in range(1, 8):
        tested = 0
        strict_exclusions = 0
        equality_words = []
        necklace_count: set[tuple[int, ...]] = set()
        for word in itertools.product(range(1, 6), repeat=height):
            if sum(word) < 2 * height:
                continue
            tested += 1
            rotated = suffix_dominating_rotation(word)
            denominator = collatz_denominator(rotated)
            numerator = collatz_numerator(rotated)
            suffix_ok = suffix_condition(rotated)
            if word == (2,) * height:
                equality_ok = numerator == denominator
                equality_words.append(word)
                row_ok = suffix_ok and equality_ok
            else:
                row_ok = suffix_ok and 0 < numerator < denominator
                strict_exclusions += int(row_ok)
            failures += int(not row_ok)
            necklace_count.add(canonical_necklace(word))
            if len(samples) < 24 and (1 in word or max(word) >= 4):
                samples.append(
                    {
                        "word": list(word),
                        "certificate_rotation": list(rotated),
                        "height_h": height,
                        "valuation_sum_S": sum(word),
                        "denominator_D": denominator,
                        "numerator_B": numerator,
                        "all_suffix_averages_at_least_two": suffix_ok,
                        "strict_B_between_zero_and_D": 0 < numerator < denominator,
                    }
                )
        height_rows.append(
            {
                "height_h": height,
                "alphabet": [1, 2, 3, 4, 5],
                "words_with_S_at_least_2h": tested,
                "necklace_count": len(necklace_count),
                "strict_nontrivial_exclusions": strict_exclusions,
                "all_two_equality_word_count": len(equality_words),
            }
        )

    theorem = (
        "For a positive accelerated Collatz cycle word a of height h, let "
        "S=sum a_j, D=2^S-3^h, and B be its cycle numerator. If S>=2h, "
        "then a cyclic rotation has every suffix valuation sum at least "
        "twice its length. For that rotation B/2^S<=1-(3/4)^h. Hence "
        "B<=2^S-2^(S-2h)3^h<=D, with equality only when every a_j=2. "
        "By necklace invariance, every non-all-two word with S>=2h has "
        "0<B<D and cannot satisfy D|B. Thus every nontrivial positive "
        "cycle must lie in h*log_2(3)<S<2h."
    )
    proof = (
        "Apply the maximum-partial-sum rotation lemma to b_j=a_j-2; its "
        "total is nonnegative. The rotation after a maximal cumulative sum "
        "has all suffix sums of b nonnegative. Dividing B by 2^S and "
        "reading suffixes gives a termwise bound by "
        "sum_(r=1)^h 3^(r-1)/4^r=1-(3/4)^h. The two comparisons are "
        "strict unless S=2h and every suffix inequality is equality, which "
        "forces a_j=2 for all j. TICKET-230 proves D|B is invariant under "
        "rotation, so the certificate applies to the original necklace."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "height_rows": height_rows,
        "mixed_word_certificate_samples": samples,
        "aggregate": {
            "average_valuation_at_least_two_nontrivial_cycles_excluded": True,
            "nontrivial_cycle_critical_strip_proved": True,
            "all_two_trivial_cycle_retained": True,
            "critical_strip_nondivisibility_proved": False,
            "aperiodic_descent_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This excludes all nontrivial cycle words with average valuation "
            "at least two and corrects the literal TICKET-230 target, which "
            "included the divisible trivial word (2). It does not exclude "
            "cycle necklaces in log_2(3)<S/h<2 or divergent aperiodic "
            "trajectories."
        ),
        "failure_count": failures,
    }


def nonzero_quadratic_residues(prime: int) -> set[int]:
    return {value * value % prime for value in range(1, prime)}


def cyclic_convolution_at_zero(weights: list[int]) -> int:
    modulus = len(weights)
    return sum(weights[value] * weights[-value % modulus] for value in range(modulus))


def goldbach_gauss_counterfamily_audit() -> dict[str, Any]:
    failures = 0
    rows = []
    for prime in (7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83):
        residues = nonzero_quadratic_residues(prime)
        weights = [int(value in residues) for value in range(prime)]
        mass = sum(weights)
        convolution_zero = cyclic_convolution_at_zero(weights)
        coefficients = [
            sum(
                weight * cmath.exp(-2j * math.pi * mode * value / prime)
                for value, weight in enumerate(weights)
            )
            for mode in range(prime)
        ]
        magnitudes = [abs(value) for value in coefficients[1:]]
        predicted_magnitude = math.sqrt(prime + 1.0) / 2.0
        maximum_formula_error = max(
            abs(value - predicted_magnitude) for value in magnitudes
        )
        signed_aggregate = sum(value * value for value in coefficients[1:]) / prime
        expected_aggregate = -Fraction(mass * mass, prime)
        ratio = predicted_magnitude / mass
        bound_ratio = (1.0 + math.sqrt(prime)) / (prime - 1)
        verified = (
            prime % 4 == 3
            and mass == (prime - 1) // 2
            and convolution_zero == 0
            and maximum_formula_error < 1e-10
            and abs(signed_aggregate.real - float(expected_aggregate)) < 1e-9
            and abs(signed_aggregate.imag) < 1e-9
            and ratio <= bound_ratio + 1e-12
        )
        failures += int(not verified)
        rows.append(
            {
                "prime_p": prime,
                "nonzero_quadratic_residue_count_W": mass,
                "convolution_at_zero": convolution_zero,
                "nonprincipal_coefficient_magnitude": predicted_magnitude,
                "maximum_mode_to_mass_ratio": ratio,
                "elementary_upper_bound_ratio": bound_ratio,
                "signed_nonprincipal_aggregate_at_zero": signed_aggregate.real,
                "exact_expected_signed_aggregate": str(expected_aggregate),
                "maximum_dft_formula_error": maximum_formula_error,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For every prime p congruent to 3 modulo 4, let w_p be the indicator "
        "of the nonzero quadratic residues in Z/pZ. Its mass is W=(p-1)/2, "
        "but (w_p*w_p)(0)=0. For k nonzero, "
        "w_hat_p(k)=(-1+chi(k)tau_p)/2, where |tau_p|=sqrt(p) and "
        "tau_p^2=-p. Hence every nonprincipal magnitude is sqrt(p+1)/2 "
        "and max|w_hat_p(k)|/W=sqrt(p+1)/(p-1), which tends to zero. The "
        "signed nonprincipal aggregate at zero is exactly -W^2/p and "
        "cancels the principal term. Thus modewise relative Fourier decay "
        "does not imply pointwise positivity."
    )
    proof = (
        "Because chi(-1)=-1, the negative of a nonzero quadratic residue "
        "is a nonresidue, proving the zero convolution. Writing the residue "
        "indicator as (1+chi)/2 away from zero gives the Gauss-sum formula. "
        "For p=3 mod 4 the quadratic Gauss sum is purely imaginary with "
        "square -p, so both signs have magnitude sqrt(p+1)/2. Fourier "
        "inversion at zero and the already proved zero convolution force "
        "the exact negative aggregate."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "quadratic_residue_counterfamily_rows": rows,
        "ticket230_correction": (
            "The TICKET-230 spike family proves same-order aligned Fourier "
            "error, but its convolution remains positive at every target. "
            "It therefore did not by itself refute the positivity inference. "
            "This quadratic-residue family supplies the required genuine "
            "zero-convolution counterfamily."
        ),
        "aggregate": {
            "true_zero_convolution_counterfamily_proved": True,
            "modewise_relative_decay_without_pointwise_positivity_proved": True,
            "exact_negative_aggregate_cancellation_proved": True,
            "ticket230_spike_positivity_overclaim_corrected": True,
            "prime_specific_minor_arc_bound_proved": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The weights are quadratic-residue indicators, not primes, so "
            "this is an inference-rule counterexample and not a Goldbach "
            "counterexample. The remaining task is a one-sided aggregate "
            "minor-arc bound for actual prime weights below the positive "
            "singular-series main term."
        ),
        "failure_count": failures,
    }


def allowed_residues(prime: int, shift: int) -> tuple[int, ...]:
    return tuple(
        value
        for value in range(prime)
        if value != 0 and (value + shift) % prime != 0
    )


def centered_character_values(prime: int, shift: int) -> dict[int, Fraction]:
    allowed = allowed_residues(prime, shift)
    mean = Fraction(-quadratic_character(-shift, prime), prime - 2)
    return {
        value: Fraction(quadratic_character(value, prime), 1) - mean
        for value in allowed
    }


def twin_crt_orthogonality_audit() -> dict[str, Any]:
    shift = 2
    failures = 0
    local_rows = []
    for prime in (3, 5, 7, 11, 13, 17, 19):
        values = centered_character_values(prime, shift)
        mean = sum(values.values(), Fraction(0)) / len(values)
        variance = sum((value * value for value in values.values()), Fraction(0)) / len(values)
        expected = Fraction(1) - Fraction(1, (prime - 2) ** 2)
        verified = mean == 0 and variance == expected
        failures += int(not verified)
        local_rows.append(
            {
                "prime_l": prime,
                "allowed_count_l_minus_2": len(values),
                "centered_mean": str(mean),
                "centered_variance": str(variance),
                "expected_variance": str(expected),
                "degenerate_zero_mode": variance == 0,
                "certificate_verified": verified,
            }
        )

    product_rows = []
    for primes in ((5,), (5, 7), (5, 7, 11), (5, 7, 11, 13)):
        local_values = {prime: centered_character_values(prime, shift) for prime in primes}
        tuples = list(itertools.product(*(local_values[prime] for prime in primes)))
        subsets = tuple(
            subset
            for size in range(len(primes) + 1)
            for subset in itertools.combinations(primes, size)
        )

        def mode_value(residues: tuple[int, ...], subset: tuple[int, ...]) -> Fraction:
            by_prime = dict(zip(primes, residues, strict=True))
            result = Fraction(1)
            for prime in subset:
                result *= local_values[prime][by_prime[prime]]
            return result

        vectors = {
            subset: [mode_value(residues, subset) for residues in tuples]
            for subset in subsets
        }
        diagonal: dict[str, str] = {}
        maximum_off_diagonal = Fraction(0)
        row_ok = True
        for left in subsets:
            for right in subsets:
                inner = sum(
                    (a * b for a, b in zip(vectors[left], vectors[right], strict=True)),
                    Fraction(0),
                ) / len(tuples)
                if left == right:
                    expected = math.prod(
                        Fraction(1) - Fraction(1, (prime - 2) ** 2)
                        for prime in left
                    )
                    row_ok &= inner == expected
                    diagonal["*".join(map(str, left)) or "constant"] = str(inner)
                else:
                    maximum_off_diagonal = max(maximum_off_diagonal, abs(inner))
                    row_ok &= inner == 0
        failures += int(not row_ok)
        product_rows.append(
            {
                "active_primes": list(primes),
                "crt_admissible_tuple_count": len(tuples),
                "orthogonal_mode_count": len(subsets),
                "diagonal_norm_squared": diagonal,
                "maximum_exact_off_diagonal": str(maximum_off_diagonal),
                "gram_identity_verified": row_ok,
            }
        )

    theorem = (
        "For odd primes l not dividing h, let A_l exclude 0 and -h, let "
        "chi_l be quadratic, mu_l=-chi_l(-h)/(l-2), and "
        "phi_l=chi_l-mu_l on A_l. Under the uniform CRT product measure, "
        "Phi_S=product_(l in S)phi_l is orthogonal to Phi_T whenever "
        "S differs from T. Its squared norm is product_(l in S)"
        "(1-1/(l-2)^2). The l=3 mode is identically zero; after removing "
        "such degenerate factors, the normalized Phi_S form an orthonormal "
        "dictionary of centered local interactions."
    )
    proof = (
        "TICKET-230 gives E(phi_l)=0. Also chi_l^2=1 on A_l, so "
        "E(phi_l^2)=1-mu_l^2. If S differs from T, a prime in their "
        "symmetric difference occurs to the first power in the product "
        "Phi_S Phi_T; independence of CRT coordinates factors out its zero "
        "mean. The diagonal factors into the stated local variances."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "local_centered_rows": local_rows,
        "crt_product_gram_rows": product_rows,
        "aggregate": {
            "centered_crt_interaction_orthogonality_proved": True,
            "exact_tensor_norm_formula_proved": True,
            "modulo_three_degenerate_mode_identified": True,
            "full_local_function_basis_claimed": False,
            "prime_weighted_growing_modulus_saving_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This removes deterministic local admissibility bias and "
            "diagonalizes one quadratic-character interaction dictionary. "
            "It is not a complete basis for all local functions, says "
            "nothing by itself about prime-weighted coefficients, and does "
            "not overcome the sieve parity barrier or prove twin infinitude."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_summable_frame_audit()
    collatz = collatz_critical_strip_audit()
    goldbach = goldbach_gauss_counterfamily_audit()
    twin = twin_crt_orthogonality_audit()
    root: dict[str, Any] = {
        "theorem_name": "SummableFrameCriticalStripGaussAndCRTCorrections",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-231 proves four exact partial or no-go theorems, "
            "corrects the TICKET-230 Goldbach positivity overclaim and the "
            "literal Collatz all-necklace target, and resolves none of the "
            "four parent conjectures."
        ),
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-231",
            "theorem_name": "SummableInfiniteDilationUniformFloorNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": riemann["no_go_scope"],
            "route_decision": {
                "discard": "a fixed absolutely summable infinite dilation family as a source of a positive uniform frequency floor",
                "retain": "height-adaptive or nonsummable-renormalized dilation frames whose floor is compared with an explicit Weil tail",
                "next_single_lemma": "HeightAdaptiveRenormalizedWeilFrameWithExplicitTailDominance",
            },
            "proof_dag": proof_dag(
                "RH",
                "QuantitativeFiniteDilationRecurrenceRateNoGo",
                "SummableInfiniteDilationUniformFloorNoGo",
                "FixedAbsolutelySummablePositiveUniformFrameFloor",
                "HeightAdaptiveRenormalizedWeilFrameWithExplicitTailDominance",
                "RiemannHypothesis",
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-231",
            "theorem_name": "AverageValuationTwoCycleExclusionAndCriticalStrip",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": collatz["no_go_scope"],
            "route_decision": {
                "discard": "the literal claim that every primitive positive-denominator necklace is nondivisible, which includes the trivial word (2)",
                "retain": "attack only nontrivial necklaces in the exact critical strip h*log_2(3)<S<2h and treat aperiodic descent separately",
                "next_single_lemma": "CriticalStripPrimitiveNecklaceNondivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "CollatzCycleDivisibilityNecklaceInvariance",
                "AverageValuationTwoCycleExclusionAndCriticalStrip",
                "AllPrimitivePositiveDenominatorNecklacesAreNondivisible",
                "CriticalStripPrimitiveNecklaceNondivisibility",
                "CollatzConjecture",
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-231",
            "theorem_name": "QuadraticResidueGaussZeroConvolutionCounterfamily",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": goldbach["no_go_scope"],
            "route_decision": {
                "discard": "using the positive TICKET-230 spike convolution as a counterexample to pointwise positivity",
                "retain": "bound the negative target-aligned aggregate for actual prime weights below the positive singular-series main term",
                "next_single_lemma": "UniformNegativeBinaryPrimeMinorArcAggregateBelowSingularSeriesMainTerm",
            },
            "proof_dag": proof_dag(
                "GB",
                "ModewiseFourierDecaySameOrderAggregateExample",
                "QuadraticResidueGaussZeroConvolutionCounterfamily",
                "TICKET230SpikeFamilyRefutesPointwisePositivity",
                "UniformNegativeBinaryPrimeMinorArcAggregateBelowSingularSeriesMainTerm",
                "StrongGoldbachConjecture",
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-231",
            "theorem_name": "CenteredCRTQuadraticInteractionOrthogonality",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": twin["no_go_scope"],
            "route_decision": {
                "discard": "treating raw local character correlations or the degenerate modulo-three mode as global prime evidence",
                "retain": "project prime-weighted data onto normalized centered CRT interactions and seek uniform energy saving as the modulus grows",
                "next_single_lemma": "PrimeWeightedGrowingCRTInteractionEnergySavingAtTwinSieveScale",
            },
            "proof_dag": proof_dag(
                "TP",
                "ShiftAdmissibleCharacterMeanAndModuloFiveCenteringCorrection",
                "CenteredCRTQuadraticInteractionOrthogonality",
                "RawLocalCharacterBiasAsPrimeWeightedCancellation",
                "PrimeWeightedGrowingCRTInteractionEnergySavingAtTwinSieveScale",
                "TwinPrimeConjecture",
            ),
        },
    }
    tracks = ("riemann", "collatz", "goldbach", "twin_prime")
    root["machine_audit"] = {
        "exact_partial_theorem_count": 4,
        "refuted_or_corrected_route_count": 4,
        "next_single_lemma_count": 4,
        "proof_dag_count": 4,
        "conjecture_resolution_count": 0,
        "total_failure_count": sum(
            root[key]["reproducible_computation"]["failure_count"] for key in tracks
        ),
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
                    "audit_ref": f"#/summable_frame_critical_strip_gauss_crt_audit/{key}",
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
            "TICKET-231 proves four exact partial results and resolves none "
            "of the four parent conjectures."
        ),
        "summable_frame_critical_strip_gauss_crt_audit": root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit["summable_frame_critical_strip_gauss_crt_audit"]
    write_json(
        ROOT / "data/open-problem/ticket231-summable-frame-critical-strip-gauss-crt.json",
        audit,
    )
    destinations = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-231-summable-frame-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-231-critical-strip-cycle.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-231-gauss-residue-counterfamily.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-231-centered-crt-orthogonality.json",
    }
    for key, destination in destinations.items():
        write_json(
            destination,
            {"schema": SCHEMA, "generated_at": GENERATED_AT, "status": STATUS, **root[key]},
        )


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    machine = audit["summable_frame_critical_strip_gauss_crt_audit"]["machine_audit"]
    print(json.dumps(machine, indent=2))
    if machine["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
