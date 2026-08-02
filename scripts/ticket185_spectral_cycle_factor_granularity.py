from __future__ import annotations

import cmath
import json
import math
from typing import Any, Callable

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket180_finite_information_localization import ordered_affine_numerator


GENERATED_AT = "2026-08-02T17:30:00+09:00"
SCHEMA = "primeproject.ticket185-spectral-cycle-factor-granularity.v1"
STATUS = "four_exact_resolution_barriers_and_route_corrections_all_open"


def proof_dag(
    problem_code: str,
    previous_name: str,
    closed_name: str,
    rejected_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T184-INPUT",
                "label": previous_name,
                "status": "proved_exact_input",
            },
            {
                "id": f"{problem_code}-T185-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T185-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_overstrong",
            },
            {
                "id": f"{problem_code}-T185-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T184-INPUT", f"{problem_code}-T185-CLOSED"],
            [f"{problem_code}-T185-CLOSED", f"{problem_code}-T185-OPEN"],
            [f"{problem_code}-T185-REJECTED", f"{problem_code}-T185-OPEN"],
        ],
    }


def integral_exp(exponent: complex, support_radius: float = 1.0) -> complex:
    if abs(exponent) < 1e-14:
        return complex(2.0 * support_radius)
    return 2.0 * cmath.sinh(exponent * support_radius) / exponent


def solve_symmetric_two_by_two(
    matrix: tuple[tuple[float, float], tuple[float, float]],
    rhs: tuple[float, float],
) -> tuple[float, float]:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2
    if determinant <= 0.0:
        raise ValueError("positive Gram matrix required")
    return (
        (rhs[0] * matrix[1][1] - rhs[1] * matrix[0][1]) / determinant,
        (matrix[0][0] * rhs[1] - matrix[0][1] * rhs[0]) / determinant,
    )


def trapezoid_integral(
    function: Callable[[float], float], left: float, right: float, steps: int
) -> float:
    if steps < 2:
        raise ValueError("at least two quadrature steps required")
    width = (right - left) / steps
    total = 0.5 * (function(left) + function(right))
    total += sum(function(left + index * width) for index in range(1, steps))
    return total * width


def neutral_autocorrelation_escape_row(
    frequency: int,
    *,
    support_radius: float = 1.0,
    low_frequency_radius: float = 4.0,
    quadrature_steps: int = 12_000,
) -> dict[str, object]:
    if frequency <= low_frequency_radius:
        raise ValueError("frequency must lie outside the audited low band")
    exponents = (0.5, -0.5)
    gram = tuple(
        tuple(integral_exp(a + b, support_radius).real for b in exponents)
        for a in exponents
    )
    moments = tuple(
        (
            integral_exp(a + 1j * frequency, support_radius)
            + integral_exp(a - 1j * frequency, support_radius)
        ).real
        / 2.0
        for a in exponents
    )
    coefficients = solve_symmetric_two_by_two(gram, moments)
    residuals = tuple(
        moments[row]
        - sum(gram[row][column] * coefficients[column] for column in range(2))
        for row in range(2)
    )
    base_norm_squared = support_radius + math.sin(
        2.0 * frequency * support_radius
    ) / (2.0 * frequency)
    projected_norm_squared = base_norm_squared - sum(
        coefficients[index] * moments[index] for index in range(2)
    )
    if projected_norm_squared <= 0.0:
        raise AssertionError("projection unexpectedly removed the entire function")

    def transform(argument: float) -> complex:
        cosine_transform = 0.5 * (
            integral_exp(1j * (frequency - argument), support_radius)
            + integral_exp(-1j * (frequency + argument), support_radius)
        )
        correction = sum(
            coefficients[index]
            * integral_exp(exponents[index] - 1j * argument, support_radius)
            for index in range(2)
        )
        return cosine_transform - correction

    low_band_energy = trapezoid_integral(
        lambda argument: abs(transform(argument)) ** 2,
        -low_frequency_radius,
        low_frequency_radius,
        quadrature_steps,
    )
    low_band_mass = low_band_energy / (
        2.0 * math.pi * projected_norm_squared
    )
    return {
        "carrier_frequency_M": frequency,
        "support_interval": [-support_radius, support_radius],
        "neutral_exponents": list(exponents),
        "projection_coefficients": list(coefficients),
        "neutral_moment_residuals": list(residuals),
        "projected_l2_norm_squared": projected_norm_squared,
        "normalized_autocorrelation_value_at_zero": 1.0,
        "audited_low_frequency_band": [
            -low_frequency_radius,
            low_frequency_radius,
        ],
        "normalized_low_band_spectral_mass": low_band_mass,
        "normalized_outside_band_spectral_mass": 1.0 - low_band_mass,
        "checks": {
            "two_neutral_constraints_hold": max(abs(value) for value in residuals)
            < 1e-12,
            "positive_definite_by_autocorrelation_construction": True,
            "compact_support_preserved": True,
            "normalization_is_nonzero": projected_norm_squared > 0.0,
            "spectral_mass_is_a_probability_up_to_quadrature": 0.0
            <= low_band_mass
            <= 1.0001,
        },
    }


def riemann_resolution_audit() -> dict[str, object]:
    rows = [neutral_autocorrelation_escape_row(value) for value in [8, 16, 32, 64]]
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(
        not all(
            rows[index + 1]["normalized_low_band_spectral_mass"]
            < rows[index]["normalized_low_band_spectral_mass"]
            for index in range(len(rows) - 1)
        )
    )
    return {
        "theorem": (
            "In the logarithmic autocorrelation model on [-A,A], impose the "
            "two neutral conditions integral g(x)e^(x/2)dx=0 and integral "
            "g(x)e^(-x/2)dx=0. There is a normalized sequence of compactly "
            "supported positive-definite autocorrelations F_M=g_M*tilde(g_M) "
            "whose Fourier probability measures escape every fixed compact "
            "frequency interval. Support, positive definiteness, normalization, "
            "and these two neutral moments therefore do not imply uniform "
            "Fourier-tail tightness."
        ),
        "proof": (
            "Start with h_M(x)=1_[-A,A](x)cos(Mx) and subtract its orthogonal "
            "projection onto span{e^(x/2),e^(-x/2)}. The projection coefficients "
            "tend to zero by the Riemann-Lebesgue lemma, while ||h_M||_2 stays "
            "bounded away from zero. The normalized autocorrelation is compactly "
            "supported and positive definite, and its Fourier density is "
            "|hat(g_M)|^2/||g_M||_2^2. The two cosine sidebands move to plus and "
            "minus M and the vanishing projection cannot retain mass in a fixed "
            "band, proving spectral escape."
        ),
        "spectral_escape_rows": rows,
        "aggregate": {
            "case_count": len(rows),
            "largest_carrier_frequency": rows[-1]["carrier_frequency_M"],
            "smallest_low_band_mass": min(
                row["normalized_low_band_spectral_mass"] for row in rows
            ),
            "largest_outside_band_mass": max(
                row["normalized_outside_band_spectral_mass"] for row in rows
            ),
            "all_neutral_constraints_hold": all(
                row["checks"]["two_neutral_constraints_hold"] for row in rows
            ),
        },
        "no_go_scope": (
            "This is an exact functional-analytic counterfamily for a stated "
            "logarithmic two-neutral-moment autocorrelation model. It is not a "
            "proof that every technical version of the full Weil test cone has "
            "the same closure, and it neither evaluates the Weil quadratic form "
            "nor excludes a zeta zero."
        ),
        "failure_count": failures,
    }


def single_one_cycle_row(horizon: int) -> dict[str, object]:
    if horizon < 3:
        raise ValueError("the contracting family starts at horizon three")
    word = (1,) + (2,) * (horizon - 1)
    numerator = 2 * 4 ** (horizon - 1) - 3 ** (horizon - 1)
    denominator = 2 * 4 ** (horizon - 1) - 3**horizon
    direct_numerator = ordered_affine_numerator(word)
    common_divisor = math.gcd(numerator, denominator)
    return {
        "horizon_h": horizon,
        "word_description": "(1,2^(h-1))",
        "affine_numerator_B": str(numerator),
        "cycle_denominator_D": str(denominator),
        "B_minus_D": str(numerator - denominator),
        "gcd_B_D": common_divisor,
        "denominator_bit_length": denominator.bit_length(),
        "checks": {
            "closed_form_matches_recurrence": numerator == direct_numerator,
            "contracting": denominator > 0,
            "primitive": True,
            "gcd_is_one": common_divisor == 1,
            "affine_divisibility_fails": numerator % denominator != 0,
        },
    }


def collatz_resolution_audit() -> dict[str, object]:
    rows = [single_one_cycle_row(horizon) for horizon in [3, 4, 8, 16, 32, 64, 128]]
    failures = sum(not check for row in rows for check in row["checks"].values())
    return {
        "theorem": (
            "No positive accelerated Collatz cycle has a primitive valuation "
            "period containing exactly one valuation one and all remaining "
            "valuations equal to two. After cyclic rotation such a word is "
            "w_h=(1,2,...,2). For every h>=3 it is contracting, but its affine "
            "numerator B_h and cycle denominator D_h are coprime, so D_h does "
            "not divide B_h."
        ),
        "proof": (
            "Iterating x maps to (3x+1)/4 after the initial valuation-one step "
            "gives B_h=2*4^(h-1)-3^(h-1) and D_h=2*4^(h-1)-3^h. Hence "
            "B_h-D_h=2*3^(h-1). The odd number D_h is congruent to two modulo "
            "three, so gcd(D_h,2*3^(h-1))=1 and therefore gcd(B_h,D_h)=1. "
            "Also D_h>=5 for h>=3. Thus D_h cannot divide B_h. Any period with "
            "one valuation one can be rotated to this form."
        ),
        "single_one_cycle_rows": rows,
        "aggregate": {
            "infinite_family_proved": True,
            "finite_rows_replayed": len(rows),
            "largest_replayed_horizon": rows[-1]["horizon_h"],
            "largest_denominator_bit_length": rows[-1]["denominator_bit_length"],
            "divisibility_hits": sum(
                not row["checks"]["affine_divisibility_fails"] for row in rows
            ),
        },
        "route_correction": (
            "TICKET-184's universal first-descent target is equivalent to the "
            "full Collatz conjecture, as already proved in TICKET-172. It is not "
            "a smaller auxiliary lemma. TICKET-185 restores a strict partial "
            "target by closing one infinite primitive-cycle stratum."
        ),
        "no_go_scope": (
            "The theorem excludes only periods with exactly one valuation one "
            "and all other valuations two. Periods with two or more valuation-one "
            "entries, valuations at least three, and the divergent-orbit branch "
            "remain open."
        ),
        "failure_count": failures,
    }


def smallest_prime_factors(limit: int) -> list[int]:
    factors = list(range(limit + 1))
    if limit >= 1:
        factors[1] = 1
    for value in range(2, math.isqrt(limit) + 1):
        if factors[value] != value:
            continue
        for multiple in range(value * value, limit + 1, value):
            if factors[multiple] == multiple:
                factors[multiple] = value
    return factors


def goldbach_factor_horizon_row(
    target: int, is_prime: list[bool], least_factor: list[int]
) -> dict[str, object]:
    if target < 6 or target % 2:
        raise ValueError("even target at least six required")
    pairs = [(left, target - left) for left in range(3, target // 2 + 1, 2)]
    bad_rows = []
    prime_pairs = []
    for left, right in pairs:
        if is_prime[left] and is_prime[right]:
            prime_pairs.append((left, right))
            continue
        gate = min(least_factor[left], least_factor[right])
        bad_rows.append((gate, left, right))
    if bad_rows:
        horizon, witness_left, witness_right = max(bad_rows)
        witness: list[int] = [witness_left, witness_right]
    else:
        horizon = 0
        witness_left = witness_right = 0
        witness = []

    def survivor_counts(depth: int) -> tuple[int, int, int]:
        survivors = [
            (left, right)
            for left, right in pairs
            if least_factor[left] > depth and least_factor[right] > depth
        ]
        good = sum(is_prime[left] and is_prime[right] for left, right in survivors)
        return len(survivors), good, len(survivors) - good

    before_total, before_good, before_bad = survivor_counts(max(horizon - 1, 0))
    at_total, at_good, at_bad = survivor_counts(horizon)
    return {
        "even_target_N": target,
        "unordered_odd_candidate_pairs": len(pairs),
        "unordered_prime_representation_count": len(prime_pairs),
        "exact_bad_pair_factor_horizon_tau_N": horizon,
        "tau_over_sqrt_N": horizon / math.sqrt(target),
        "last_bad_survivor_witness": witness,
        "last_bad_survivor_gate": horizon,
        "survivors_before_horizon": before_total,
        "prime_survivors_before_horizon": before_good,
        "bad_survivors_before_horizon": before_bad,
        "survivors_at_horizon": at_total,
        "prime_survivors_at_horizon": at_good,
        "bad_survivors_at_horizon": at_bad,
        "checks": {
            "bad_witness_survives_one_step_before": not bad_rows
            or min(least_factor[witness_left], least_factor[witness_right])
            > horizon - 1,
            "all_bad_pairs_removed_at_horizon": at_bad == 0,
            "horizon_is_minimal_or_bad_set_is_empty": before_bad > 0
            or not bad_rows,
            "factor_horizon_is_zero_exactly_for_empty_bad_set": (horizon == 0)
            == (not bad_rows),
            "horizon_is_at_most_square_root_scale": horizon
            <= math.isqrt(target) + 1,
            "finite_target_has_goldbach_representation": len(prime_pairs) > 0,
        },
    }


def goldbach_resolution_audit() -> dict[str, object]:
    targets = [100, 500, 1_000, 5_000, 10_000, 50_000]
    primality = prime_sieve(max(targets))
    least_factor = smallest_prime_factors(max(targets))
    rows = [
        goldbach_factor_horizon_row(target, primality, least_factor)
        for target in targets
    ]
    failures = sum(not check for row in rows for check in row["checks"].values())
    return {
        "theorem": (
            "For an even target N>=6, let tau_N be zero when there is no bad "
            "odd candidate pair, and otherwise the maximum, over every "
            "unordered odd candidate pair a+(N-a)=N that is not prime-prime, "
            "of min(P^-(a),P^-(N-a)). Sieving both endpoints by every prime at "
            "most y leaves only prime-prime pairs if and only if y>=tau_N. "
            "Thus a positive survivor count beyond tau_N is an exact Goldbach "
            "certificate, while every y<tau_N leaves a composite-contaminated "
            "survivor. Moreover tau_N is at most square-root scale."
        ),
        "proof": (
            "For y>=0, a candidate pair survives depth y exactly when both least prime "
            "factors exceed y. A bad pair is therefore removed exactly when y "
            "reaches the smaller of its two least factors. Taking the maximum "
            "of these gates proves both directions; when the bad set is empty, "
            "the convention tau_N=0 makes the claim immediate. In every bad pair at least "
            "one endpoint is composite; if the other endpoint is a large prime, "
            "the composite endpoint is below N and has least factor at most its "
            "square root, while a small prime endpoint only lowers the gate."
        ),
        "target_factor_horizon_rows": rows,
        "aggregate": {
            "target_count": len(rows),
            "largest_target": rows[-1]["even_target_N"],
            "largest_factor_horizon": max(
                row["exact_bad_pair_factor_horizon_tau_N"] for row in rows
            ),
            "largest_tau_over_sqrt_N": max(
                row["tau_over_sqrt_N"] for row in rows
            ),
            "bad_survivors_at_exact_horizon": sum(
                row["bad_survivors_at_horizon"] for row in rows
            ),
        },
        "no_go_scope": (
            "The factor horizon is an exact finite decision threshold obtained "
            "from least-factor information. Reaching it by trial division is "
            "not a uniform analytic Goldbach proof. The theorem shows precisely "
            "where a pure growing-wheel route becomes equivalent to resolving "
            "the composite support it was meant to avoid."
        ),
        "failure_count": failures,
    }


TWIN_CONSTANT = 0.6601618158468696


def expected_twin_mass(left: int, right: int) -> float:
    return sum(
        2.0 * TWIN_CONSTANT / (math.log(value) ** 2)
        for value in range(max(left, 3), right)
    )


def twin_granularity_rows() -> list[dict[str, object]]:
    start = 100_000
    stop = start + 2**18
    primality = prime_sieve(stop + 2)
    rows = []
    for width in [16, 32, 64, 128, 256, 512, 1_024]:
        block_rows = []
        for left in range(start, stop, width):
            right = min(left + width, stop)
            count = sum(
                primality[value] and primality[value + 2]
                for value in range(left, right)
            )
            expected = expected_twin_mass(left, right)
            remainder = count - expected
            block_rows.append(
                {
                    "expected": expected,
                    "count": count,
                    "one_sided": remainder > -expected,
                    "absolute": abs(remainder) < expected,
                }
            )
        subhalf = [row for row in block_rows if row["expected"] <= 0.5]
        rows.append(
            {
                "block_width": width,
                "block_count": len(block_rows),
                "minimum_expected_mass": min(row["expected"] for row in block_rows),
                "maximum_expected_mass": max(row["expected"] for row in block_rows),
                "positive_actual_blocks": sum(row["count"] > 0 for row in block_rows),
                "one_sided_certified_blocks": sum(row["one_sided"] for row in block_rows),
                "absolute_dominance_blocks": sum(row["absolute"] for row in block_rows),
                "positive_but_absolute_fails": sum(
                    row["count"] > 0 and not row["absolute"] for row in block_rows
                ),
                "subhalf_expected_blocks": len(subhalf),
                "subhalf_absolute_dominance_blocks": sum(
                    row["absolute"] for row in subhalf
                ),
                "checks": {
                    "one_sided_is_exactly_positive_count": all(
                        row["one_sided"] == (row["count"] > 0)
                        for row in block_rows
                    ),
                    "subhalf_absolute_certificate_is_impossible": all(
                        not row["absolute"] for row in subhalf
                    ),
                },
            }
        )
    return rows


def twin_resolution_audit() -> dict[str, object]:
    rows = twin_granularity_rows()
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(not any(row["positive_but_absolute_fails"] > 0 for row in rows))
    return {
        "theorem": (
            "Let C be a nonnegative integer block count, M>0 a proposed main "
            "term, and R=C-M. Then |R|<M holds exactly when 0<C<2M, whereas "
            "the one-sided inequality R>-M holds exactly when C>0. Hence an "
            "absolute main-term domination certificate is strictly stronger "
            "than positive block mass. If M<=1/2, no integer C can satisfy the "
            "absolute certificate at all."
        ),
        "proof": (
            "Expanding |C-M|<M gives -M<C-M<M, hence 0<C<2M. The "
            "one-sided inequality C-M>-M reduces to C>0. If M<=1/2, the "
            "interval (0,2M) contains no positive integer. This is an exact "
            "integer-granularity obstruction, independent of any probabilistic "
            "model."
        ),
        "finite_prime_pair_block_rows": rows,
        "aggregate": {
            "audited_interval": [100_000, 100_000 + 2**18],
            "audited_width_count": len(rows),
            "smallest_block_width": rows[0]["block_width"],
            "largest_block_width": rows[-1]["block_width"],
            "positive_but_absolute_failure_count": sum(
                row["positive_but_absolute_fails"] for row in rows
            ),
            "subhalf_absolute_pass_count": sum(
                row["subhalf_absolute_dominance_blocks"] for row in rows
            ),
        },
        "route_correction": (
            "Positive counts on infinitely many disjoint blocks are equivalent "
            "to Twin Prime infinitude, not a weaker intermediate theorem. An "
            "absolute remainder bound adds an unnecessary upper-count condition. "
            "The missing arithmetic input must be a signed one-sided parity "
            "estimate, not a symmetric norm bound."
        ),
        "no_go_scope": (
            "The theorem calibrates certificate resolution and rejects symmetric "
            "absolute-error promotion. It proves no one-sided estimate for the "
            "actual prime-pair remainder on unbounded blocks and does not cross "
            "the sieve parity barrier."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_resolution_audit()
    collatz = collatz_resolution_audit()
    goldbach = goldbach_resolution_audit()
    twin = twin_resolution_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-185",
            "theorem_name": "TwoNeutralMomentAutocorrelationSpectralEscapeNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "The construction is a logarithmic two-neutral-moment model and does not evaluate the actual Weil quadratic form or prove that every full-cone formulation contains this sequence.",
            "route_decision": {
                "discard": "uniform spectral-tail compactness derived only from compact support, positive definiteness, normalization, and two neutral moments",
                "retain": "direct Weil quadratic-form coercivity on an explicit pole-neutral core after quotienting or controlling spectral translations",
                "next_single_lemma": "WeilQuadraticFormCoercivityModuloSpectralTranslationsOnExplicitPoleNeutralCore",
            },
            "proof_dag": proof_dag(
                "RH",
                "FiniteMomentCancellationDoesNotGiveUniformAbelDesmoothing",
                "TwoNeutralMomentAutocorrelationSpectralEscapeNoGo",
                "SupportPositivityAndTwoNeutralMomentsForceSpectralTailTightness",
                "WeilQuadraticFormCoercivityModuloSpectralTranslationsOnExplicitPoleNeutralCore",
            ),
            "claim_boundary": "No RH proof, off-critical zero exclusion, or actual Weil-form coercivity theorem; one exact spectral-escape counterfamily in a declared neutral autocorrelation model only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-185",
            "theorem_name": "SingleValuationOneOtherwiseTwoCycleExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Only one infinite primitive cycle stratum is excluded; multi-one words, valuations at least three, and divergent orbits remain.",
            "route_decision": {
                "discard": "presenting universal first descent as a smaller post-TICKET-184 auxiliary lemma; TICKET-172 already proved it equivalent to Collatz",
                "retain": "exact affine divisibility exclusion on increasingly broad primitive contracting word strata, kept separate from divergent-orbit analysis",
                "next_single_lemma": "NoPrimitiveContractingValuationWordWithExactlyTwoOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "CounterexampleDichotomyAndMinimalCyclePrefixBarrier",
                "SingleValuationOneOtherwiseTwoCycleExclusion",
                "UniversalFirstDescentIsAStrictlyWeakerLemmaThanCollatz",
                "NoPrimitiveContractingValuationWordWithExactlyTwoOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            ),
            "claim_boundary": "No Collatz proof, complete cycle exclusion, or divergent-orbit exclusion; one infinite primitive valuation stratum is excluded exactly.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-185",
            "theorem_name": "TargetSpecificGoldbachFactorHorizonEquivalence",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "The exact horizon is targetwise factor information; no sub-root prime-weighted cancellation or uniform all-target bound is proved.",
            "route_decision": {
                "discard": "treating a growing wheel as an analytic breakthrough when it reaches the target's exact least-factor decision horizon",
                "retain": "sub-horizon wheel localization combined with signed prime-weighted cancellation of the remaining bad survivors",
                "next_single_lemma": "SubHorizonPrimeWeightedBadSurvivorCancellationBelowTargetMargin",
            },
            "proof_dag": proof_dag(
                "GB",
                "SquarefreeWheelFactorizationAndCompositeImpostorNoGo",
                "TargetSpecificGoldbachFactorHorizonEquivalence",
                "SubRootWheelOccupancyAloneCertifiesPrimeSupportUniformly",
                "SubHorizonPrimeWeightedBadSurvivorCancellationBelowTargetMargin",
            ),
            "claim_boundary": "No Goldbach proof, counterexample, or uniform minor-arc theorem; one exact finite target-specific wheel completeness threshold only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-185",
            "theorem_name": "IntegerGranularityAndOneSidedBlockCertificate",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No signed prime-pair remainder bound is proved on unbounded blocks; the parity barrier is unchanged.",
            "route_decision": {
                "discard": "symmetric absolute remainder domination as though it were the minimal positive-root condition, especially below half-unit expected mass",
                "retain": "one-sided signed parity estimates on blocks whose resolution is chosen before inspecting prime-pair counts",
                "next_single_lemma": "CubicRoughOneSidedJointLiouvilleBlockMarginOnUnboundedScales",
            },
            "proof_dag": proof_dag(
                "TP",
                "PositiveRootMassSufficesAndCantelliExceptionalMassIsSharp",
                "IntegerGranularityAndOneSidedBlockCertificate",
                "AbsoluteRemainderDominanceIsEquivalentToPositiveBlockMass",
                "CubicRoughOneSidedJointLiouvilleBlockMarginOnUnboundedScales",
            ),
            "claim_boundary": "No Twin Prime proof, infinitude result, or parity-breaking estimate; one exact certificate-granularity theorem and bounded block audit only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureResolutionBarrierAndRouteCorrectionAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-185 resolves none of the four conjectures. It proves one "
            "spectral-escape no-go, excludes one infinite Collatz cycle stratum, "
            "identifies an exact Goldbach factor horizon, and derives the exact "
            "integer resolution limit of symmetric Twin block certificates."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The decisive missing information is signed and scale-sensitive: "
            "spectral translation evades compactness, Collatz needs exact affine "
            "divisibility across broader words plus a separate divergence route, "
            "Goldbach needs cancellation before trial-division depth, and Twin "
            "needs a one-sided parity estimate rather than an absolute norm."
        ),
        "literature_boundary": {
            "riemann": "Weil positivity remains a quadratic-form problem on a constrained test space; this model counterfamily is not imported as a statement about every published cone realization.",
            "collatz": "Finite exponent-code and density theorems do not exclude all primitive cycles or divergent natural orbits.",
            "goldbach": "Exceptional-set and major-arc advances do not supply an every-target binary minor-arc bound.",
            "twin_prime": "Prime-producing lower-bound sieves require substantial Type I/II information; no exact-gap-two one-sided margin is supplied here.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "rejected_target_count": 4,
            "proof_dag_count": 4,
            "finite_arithmetic_diagnostic_count": 4,
            "decisive_route_correction_count": 3,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, object]]:
    attempts = []
    for problem_id, section_key in [
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin-prime", "twin_prime"),
    ]:
        section = audit[section_key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "status": "open_not_proven",
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": section["route_decision"]["next_single_lemma"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    write_json(
        ROOT / "data" / "open-problem" / "ticket185-spectral-cycle-factor-granularity.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "resolution_barrier_route_correction_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-185-neutral-autocorrelation-escape.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-185-single-one-cycle-exclusion.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-185-target-factor-horizon.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-185-integer-granularity.json",
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    by_problem = {attempt["problem_id"]: attempt for attempt in attempts}
    for problem_id, path in paths.items():
        section = audit[section_keys[problem_id]]
        attempt = by_problem[problem_id]
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "ticket_id": section["ticket_id"],
                "problem_id": problem_id,
                "status": "open_not_proven",
                "theorem_name": section["theorem_name"],
                "declared_proposition": section["declared_proposition"],
                "mathematical_argument": section["mathematical_argument"],
                "reproducible_computation": section["reproducible_computation"],
                "discarded_route": attempt["discarded_route"],
                "remaining_gap": attempt["remaining_gap"],
                "candidate_theorem": attempt["candidate_theorem"],
                "claim_boundary": attempt["claim_boundary"],
                "proof_dag": attempt["proof_dag"],
            },
        )


def main() -> None:
    audit = build_audit()
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(
            "TICKET-185 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
