from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, ROUND_FLOOR, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket214_cofinal_sevenone_exponential_cardinal import goldbach_counts, prime_sieve


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket217-relative-threshold-convergent-moment-tail.v1"
GENERATED_AT = "2026-08-13T03:00:00+09:00"
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
    rejected: str,
    open_lemma: str,
    target: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T216", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T217", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N217",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN217",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T216", f"{prefix}-T217"],
            [f"{prefix}-T217", f"{prefix}-N217"],
            [f"{prefix}-T217", f"{prefix}-OPEN217"],
            [f"{prefix}-OPEN217", prefix],
        ],
    }


def defect_transform(atoms: list[tuple[int, int]], radius: Fraction) -> Fraction:
    return sum(
        (multiplicity * radius**height for height, multiplicity in atoms),
        start=Fraction(0),
    )


def first_hidden_height(
    radii: list[Fraction], tolerances: list[Fraction]
) -> int:
    height = max(
        1,
        max(
            int(math.log(float(tolerance)) / math.log(float(radius))) + 1
            for radius, tolerance in zip(radii, tolerances)
        ),
    )
    while any(radius**height >= tolerance for radius, tolerance in zip(radii, tolerances)):
        height += 1
    while height > 1 and all(
        radius ** (height - 1) < tolerance
        for radius, tolerance in zip(radii, tolerances)
    ):
        height -= 1
    return height


def fraction_scientific(value: Fraction) -> str:
    return format(
        Decimal(value.numerator) / Decimal(value.denominator),
        ".18E",
    )


def riemann_multiradius_audit() -> dict[str, Any]:
    atoms = [(17, 1), (53, 2)]
    radii = [Fraction(1, 2), Fraction(2, 3), Fraction(9, 10)]
    transforms = [defect_transform(atoms, radius) for radius in radii]
    rows = []
    failures = 0
    for height in (10, 16, 17, 40, 52, 53):
        normalized = [value / radius**height for value, radius in zip(transforms, radii)]
        best_integer_upper = min(value.numerator // value.denominator for value in normalized)
        actual_count = sum(
            multiplicity
            for atom_height, multiplicity in atoms
            if atom_height <= height
        )
        failures += int(actual_count > best_integer_upper)
        rows.append(
            {
                "H": height,
                "normalized_transform_bounds": [str(value) for value in normalized],
                "best_integer_upper_for_C_H": best_integer_upper,
                "actual_synthetic_pair_count_C_H": actual_count,
                "zero_certified": best_integer_upper == 0,
            }
        )

    precision_scenarios = [
        (
            [Fraction(1, 2), Fraction(2, 3)],
            [Fraction(1, 10**8), Fraction(1, 10**8)],
        ),
        (
            [Fraction(3, 5), Fraction(4, 5), Fraction(9, 10)],
            [Fraction(1, 10**12), Fraction(1, 10**16), Fraction(1, 10**20)],
        ),
        (
            [Fraction(99, 100), Fraction(999, 1000)],
            [Fraction(1, 10**18), Fraction(1, 10**24)],
        ),
    ]
    invisibility_rows = []
    for scenario_radii, tolerances in precision_scenarios:
        hidden_height = first_hidden_height(scenario_radii, tolerances)
        contributions = [radius**hidden_height for radius in scenario_radii]
        hidden = all(
            contribution < tolerance
            for contribution, tolerance in zip(contributions, tolerances)
        )
        failures += int(not hidden)
        invisibility_rows.append(
            {
                "radii": [str(value) for value in scenario_radii],
                "absolute_tolerances": [str(value) for value in tolerances],
                "first_simultaneously_hidden_height": hidden_height,
                "one_atom_contributions_decimal": [
                    fraction_scientific(value) for value in contributions
                ],
                "hidden_at_every_radius": hidden,
            }
        )

    theorem = (
        "Let C be the nonnegative integer-valued off-critical-pair counting "
        "measure from TICKET-216 and L(r)=integral r^t dC(t). For every H "
        "and every finite family 0<r_j<1, C(H)<=floor(min_j "
        "L(r_j)/r_j^H). Hence rigorous upper bounds U_j with "
        "min_j U_j/r_j^H<1 certify C(H)=0. Conversely, for every finite "
        "family of radii and positive absolute tolerances epsilon_j, one "
        "nonzero atom can be placed at a finite height K so that "
        "r_j^K<epsilon_j for all j. Thus finitely many fixed absolute-error "
        "Laplace observations cannot imply RH; the required accuracy must "
        "track the moving first-atom scale."
    )
    proof = (
        "TICKET-216 gives C(H)r_j^H<=L(r_j) for each j. Divide, take the "
        "minimum, and use integrality. For invisibility, r_j^K tends to zero "
        "for each of finitely many radii. Choose K larger than every "
        "individual threshold. The unit atom delta_K is nonzero but changes "
        "every observed transform by less than its prescribed tolerance."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "normalized_certificate": "C(H)<=floor(min_j U_j(r_j)/r_j^H)",
        "synthetic_atoms": [
            {"height": height, "pair_multiplicity": multiplicity}
            for height, multiplicity in atoms
        ],
        "normalized_certificate_rows": rows,
        "finite_absolute_precision_invisibility_rows": invisibility_rows,
        "aggregate": {
            "multi_radius_normalized_certificate_proved": True,
            "finite_absolute_precision_family_sufficient_for_RH": False,
            "cofinal_relative_precision_actual_zeta_bound_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The hidden atoms are admissible logical defect measures, not "
            "zeros of the actual zeta function. The theorem rejects only "
            "finite fixed absolute-error promotion."
        ),
        "failure_count": failures,
    }


def log_rational_interval(
    numerator: int, denominator: int, terms: int = 180
) -> tuple[Fraction, Fraction]:
    y = Fraction(numerator - denominator, numerator + denominator)
    partial = Fraction(0)
    for index in range(terms):
        exponent = 2 * index + 1
        partial += 2 * y**exponent / exponent
    first_omitted = 2 * terms + 1
    remainder = (
        2
        * y**first_omitted
        / (first_omitted * (1 - y * y))
    )
    return partial, partial + remainder


def interval_continued_fraction(
    lower: Fraction, upper: Fraction, maximum_terms: int = 24
) -> list[int]:
    coefficients: list[int] = []
    for _ in range(maximum_terms):
        lower_floor = lower.numerator // lower.denominator
        upper_floor = upper.numerator // upper.denominator
        if lower_floor != upper_floor:
            break
        coefficients.append(lower_floor)
        lower_fraction = lower - lower_floor
        upper_fraction = upper - upper_floor
        if lower_fraction <= 0:
            break
        lower, upper = 1 / upper_fraction, 1 / lower_fraction
    return coefficients


def convergents(coefficients: list[int]) -> list[tuple[int, int]]:
    p_previous_previous, p_previous = 0, 1
    q_previous_previous, q_previous = 1, 0
    rows = []
    for coefficient in coefficients:
        p = coefficient * p_previous + p_previous_previous
        q = coefficient * q_previous + q_previous_previous
        rows.append((p, q))
        p_previous_previous, p_previous = p_previous, p
        q_previous_previous, q_previous = q_previous, q
    return rows


def collatz_convergent_compression_audit() -> dict[str, Any]:
    log_three_halves = log_rational_interval(3, 2)
    log_four_thirds = log_rational_interval(4, 3)
    alpha_lower = log_three_halves[0] / log_four_thirds[1]
    alpha_upper = log_three_halves[1] / log_four_thirds[0]
    coefficients = interval_continued_fraction(alpha_lower, alpha_upper, 24)
    all_convergents = convergents(coefficients)
    classified = []
    failures = 0
    for numerator_m, denominator_k in all_convergents:
        value = Fraction(numerator_m, denominator_k)
        if value > alpha_upper:
            side = "upper"
        elif value < alpha_lower:
            side = "lower"
        else:
            side = "uncertified"
            failures += 1
        classified.append((numerator_m, denominator_k, side))

    tested_ceiling = 4_474_633
    upper_convergents = [row for row in classified if row[2] == "upper"]
    tested = [row for row in upper_convergents if row[1] <= tested_ceiling]
    later = [row for row in upper_convergents if row[1] > tested_ceiling]
    next_upper = later[0]
    transcript = hashlib.sha256()
    rows = []
    for numerator_m, denominator_k, _ in tested:
        delta = (
            1 << (denominator_k + 2 * numerator_m)
        ) - 3 ** (denominator_k + numerator_m)
        scaling_barrier = 3**denominator_k
        blocks_all_multiples = delta >= scaling_barrier
        failures += int(not blocks_all_multiples)
        transcript.update(
            f"{numerator_m}:{denominator_k}:{delta.bit_length()}:"
            f"{scaling_barrier.bit_length()}:{int(blocks_all_multiples)}\n".encode(
                "ascii"
            )
        )
        rows.append(
            {
                "reduced_upper_convergent_m": numerator_m,
                "reduced_upper_convergent_k": denominator_k,
                "delta_bit_length": delta.bit_length(),
                "three_pow_k_bit_length": scaling_barrier.bit_length(),
                "delta_at_least_three_pow_k": blocks_all_multiples,
                "all_positive_multiples_excluded": blocks_all_multiples,
            }
        )

    theorem = (
        "If a positive accelerated Collatz cycle has single-mountain word "
        "1^k 2^m, then the reduced fraction p/q=m/k is an upper continued-"
        "fraction convergent of alpha=log(3/2)/log(4/3). If for such p/q, "
        "2^(q+2p)-3^(q+p)>=3^q, then no positive multiple (m,k)=(gp,gq) "
        "can satisfy the cycle near-collision. A rigorous rational-interval "
        "continued-fraction computation and exact integer audit exclude all "
        "upper convergents through q=4,474,633. The next possible reduced "
        "denominator is q=71,356,888; consequently no single-mountain cycle "
        "can have k<71,356,888."
    )
    proof = (
        "Put lambda=m log(4/3)-k log(3/2). The TICKET-215 necessity gives "
        "0<exp(lambda)-1<3^(-m), hence "
        "0<m/k-alpha<3^(-m)/(k log(4/3))<1/(2k^2). The last inequality "
        "uses m>=k+1 and 2k<3^(k+1)log(4/3). Legendre's theorem makes the "
        "reduced fraction a convergent, necessarily from above. For a fixed "
        "upper reduced p/q, write lambda_0>0. A multiple g would require "
        "exp(g lambda_0)-1<3^(-gp). If the audited base difference is at "
        "least 3^q, then exp(lambda_0)-1>=3^(-p), contradicting that "
        "inequality for every g>=1. Exact atanh-series intervals certify "
        "the continued-fraction coefficients; powers are compared as exact "
        "integers."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "alpha_definition": "log(3/2)/log(4/3)",
        "alpha_interval_decimal": [
            format(float(alpha_lower), ".16g"),
            format(float(alpha_upper), ".16g"),
        ],
        "certified_continued_fraction_coefficients": coefficients,
        "audited_upper_convergent_rows": rows,
        "next_unaudited_upper_convergent": {
            "m": next_upper[0],
            "k": next_upper[1],
        },
        "single_mountain_k_exclusive_upper_bound": next_upper[1],
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "near_collision_implies_upper_convergent_proved": True,
            "positive_multiple_exclusion_proved": True,
            "audited_upper_convergent_count": len(rows),
            "single_mountain_cycles_with_k_below_71356888_excluded": True,
            "all_single_mountain_cycles_excluded": False,
            "multi_run_cycle_words_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The result concerns one 1-run and one 2-run. It neither audits "
            "the next upper convergent nor covers multi-run words, valuation "
            "entries above two, or divergent nonperiodic trajectories."
        ),
        "failure_count": failures,
    }


def support_moment_margin(values: list[float]) -> tuple[float, float, float, float]:
    total = sum(values)
    square_total = sum(value * value for value in values)
    margin = total * total - (len(values) - 1) * square_total
    ratio = total * total / ((len(values) - 1) * square_total)
    return total, square_total, margin if math.isfinite(margin) else float("nan"), ratio


def singular_factor(value: int, primes: list[int]) -> float:
    remaining = value
    factor = 1.0
    for prime in primes:
        if prime * prime > remaining:
            break
        if remaining % prime == 0:
            if prime > 2:
                factor *= (prime - 1) / (prime - 2)
            while remaining % prime == 0:
                remaining //= prime
    if remaining > 2:
        factor *= (remaining - 1) / (remaining - 2)
    return factor


def goldbach_second_moment_audit() -> dict[str, Any]:
    failures = 0
    synthetic_rows = []
    for values in ([1.0] * 8, [1.0] * 7 + [0.0], [3.0] * 7 + [0.0]):
        total, square_total, margin, ratio = support_moment_margin(list(values))
        full_support = all(value > 0 for value in values)
        certified = margin > 0
        failures += int(certified and not full_support)
        synthetic_rows.append(
            {
                "values": list(values),
                "sum_S": total,
                "square_sum_Q": square_total,
                "support_margin_S2_minus_Bminus1Q": margin,
                "moment_ratio": ratio,
                "full_support": full_support,
                "full_support_certified": certified,
            }
        )

    starts = (128, 512, 2048, 8192, 32768)
    flags = prime_sieve(2 * max(starts))
    primes = [value for value in range(2, len(flags)) if flags[value]]
    block_rows = []
    raw_passes = 0
    normalized_passes = 0
    for start in starts:
        counts = goldbach_counts(start, flags, primes)
        targets = list(range(start, 2 * start, 2))
        total = sum(counts)
        square_total = sum(value * value for value in counts)
        exact_margin = total * total - (len(counts) - 1) * square_total
        raw_ratio = total * total / ((len(counts) - 1) * square_total)
        raw_certified = exact_margin > 0
        raw_passes += int(raw_certified)

        normalized = []
        for count, target in zip(counts, targets):
            model = (
                singular_factor(target, primes)
                * target
                / (math.log(target) ** 2)
            )
            normalized.append(count / model)
        _, _, normalized_margin, normalized_ratio = support_moment_margin(normalized)
        normalized_certified = normalized_margin > 0
        normalized_passes += int(normalized_certified)
        block_rows.append(
            {
                "dyadic_start_X": start,
                "target_count_B": len(counts),
                "minimum_exact_representation_count": min(counts),
                "raw_exact_margin": exact_margin,
                "raw_moment_ratio": raw_ratio,
                "raw_second_moment_certificate_passed": raw_certified,
                "hardy_littlewood_shape_diagnostic_ratio": normalized_ratio,
                "hardy_littlewood_shape_diagnostic_margin": normalized_margin,
                "hardy_littlewood_shape_diagnostic_passed": normalized_certified,
                "diagnostic_is_not_rigorous_interval": True,
            }
        )
        failures += int(raw_certified and min(counts) == 0)
        failures += int(normalized_certified and min(counts) == 0)

    theorem = (
        "For B nonnegative Goldbach counts A_i and arbitrary positive "
        "normalizers w_i, put y_i=A_i/w_i, S=sum y_i, and Q=sum y_i^2. "
        "If S^2>(B-1)Q, then every A_i is positive. The coefficient B-1 "
        "and strict threshold are sharp: a vector with B-1 equal positive "
        "coordinates and one zero has S^2=(B-1)Q. Therefore no universal "
        "certificate of this Cauchy form can replace B-1 by a smaller "
        "coefficient. Exact raw-moment audits and a separately "
        "labelled Hardy-Littlewood-shape diagnostic both fail the threshold "
        "on the five tested dyadic blocks, despite their known zero "
        "exception count."
    )
    proof = (
        "If one coordinate vanishes, at most B-1 coordinates contribute. "
        "Cauchy-Schwarz gives S^2<=|supp(y)|Q<=(B-1)Q. The contrapositive "
        "proves the certificate. Equality for (1,...,1,0), and its weighted "
        "rescalings A_i=w_i y_i, proves sharpness for information consisting "
        "only of S and Q."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "support_certificate": "(sum_i A_i/w_i)^2>(B-1)sum_i(A_i/w_i)^2",
        "synthetic_sharpness_rows": synthetic_rows,
        "dyadic_goldbach_rows": block_rows,
        "aggregate": {
            "weighted_second_moment_full_support_certificate_proved": True,
            "two_moment_threshold_sharpness_proved": True,
            "raw_dyadic_blocks_certified": raw_passes,
            "hl_shape_diagnostic_blocks_certified": normalized_passes,
            "pointwise_arithmetic_lower_tail_proved": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The theorem rejects only lowering the universal coefficient in "
            "this Cauchy-form certificate or treating a failed inequality as "
            "a certificate. The normalized rows use floating diagnostics and "
            "are not interval certificates. Other deductions from moments, "
            "higher moments, targetwise estimates, and circle-method "
            "cancellation remain available."
        ),
        "failure_count": failures,
    }


def first_odd_after(value: int) -> int:
    return value + 1 if value % 2 == 0 else value + 2


def twin_tail_ratio(scale: int, offset: Decimal) -> tuple[int, Decimal, Decimal]:
    x = Decimal(scale)
    log_x = x.ln()
    dilation = Decimal(2) * log_x.ln() + offset
    horizon = int((dilation * x).to_integral_value(rounding=ROUND_FLOOR))
    radius = Decimal(scale - 1) / x
    first_odd = first_odd_after(horizon)
    tail = (Decimal(first_odd) * radius.ln()).exp() / (
        Decimal(1) - radius * radius
    )
    twin_scale = x / (log_x * log_x)
    return horizon, tail / twin_scale, dilation


def twin_critical_tail_audit() -> dict[str, Any]:
    getcontext().prec = 80
    scales = (1_000, 100_000, 100_000_000, 1_000_000_000_000)
    offsets = (Decimal(-2), Decimal(0), Decimal(2))
    rows = []
    failures = 0
    for offset in offsets:
        limiting_ratio = (-offset).exp() / Decimal(2)
        for scale in scales:
            horizon, ratio, dilation = twin_tail_ratio(scale, offset)
            rows.append(
                {
                    "X": scale,
                    "offset_a": str(offset),
                    "dilation_c_X": str(dilation),
                    "Y_floor_c_X_X": horizon,
                    "tail_over_X_log2X": str(ratio),
                    "predicted_limit_half_exp_minus_a": str(limiting_ratio),
                    "absolute_limit_error": str(abs(ratio - limiting_ratio)),
                }
            )
        largest_ratio = Decimal(rows[-1]["tail_over_X_log2X"])
        failures += int(abs(largest_ratio - limiting_ratio) > Decimal("0.000001"))

    theorem = (
        "Let r_X=1-1/X and let Y_X=floor(c_X X), with the odd geometric "
        "tail R_X=r_X^n0/(1-r_X^2) from TICKET-216. If "
        "c_X=2 log log X+a_X and 0<=c_X=o(X), then "
        "R_X/(X/log^2 X)=(1/2)exp(-a_X)(1+o(1)) whenever a_X is bounded, "
        "with the corresponding extended limits for a_X tending to plus "
        "or minus infinity while c_X remains nonnegative. Thus a bounded "
        "offset leaves a nonzero critical "
        "tail constant, a_X tending to plus infinity is necessary and "
        "sufficient for this geometric envelope to be little-o of the twin "
        "scale, and a_X tending to minus infinity makes it dominate."
    )
    proof = (
        "The first odd n0 above Y_X satisfies n0/X=c_X+o(1). Also "
        "log(1-1/X)=-1/X+O(1/X^2) and "
        "1-r_X^2=2/X+O(1/X^2). Hence R_X=(X/2)exp(-c_X)(1+o(1)). "
        "Substituting c_X=2 log log X+a_X and dividing by X/log^2 X "
        "gives the formula and all three regimes."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "critical_schedule": "Y/X=2 log log X+a_X",
        "critical_limit": "tail/(X/log^2 X)~exp(-a_X)/2",
        "critical_limit_rows": rows,
        "aggregate": {
            "sharp_adaptive_tail_phase_transition_proved": True,
            "bounded_offset_makes_tail_negligible": False,
            "positive_diverging_offset_removes_geometric_tail": True,
            "actual_twin_Abel_surplus_above_tail_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This is sharp only for the coefficient-one odd geometric tail "
            "used in TICKET-216. It is not a parity-breaking estimate for "
            "the actual twin-prime Abel transform."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_multiradius_audit()
    collatz_compute = collatz_convergent_compression_audit()
    goldbach_compute = goldbach_second_moment_audit()
    twin_compute = twin_critical_tail_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-217",
            "theorem_name": "MultiRadiusNormalizedDefectCertificateAndFinitePrecisionInvisibility",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No cofinal actual-zeta explicit-formula enclosure is proved with error below the moving first-atom threshold.",
            "route_decision": {
                "discard": "any finite family of fixed absolute-precision Laplace observations as a global RH certificate",
                "retain": "cofinal normalized actual-zeta bounds with relative error strictly below one at the first-atom scale",
                "next_single_lemma": "CofinalRelativePrecisionExplicitFormulaEnvelopeBelowOne",
            },
            "proof_dag": proof_dag(
                "RH",
                "OffLineDefectLaplaceFirstAtomCertificateAndFixedToleranceNoGo",
                "MultiRadiusNormalizedDefectCertificateAndFinitePrecisionInvisibility",
                "FiniteAbsolutePrecisionLaplaceFamilyImpliesRH",
                "CofinalRelativePrecisionExplicitFormulaEnvelopeBelowOne",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof and no off-line zeta zero. The normalized multi-radius certificate is exact, but its actual-zeta relative-precision input is open.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-217",
            "theorem_name": "SingleMountainContinuedFractionCompressionAnd71356888Barrier",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "The next upper convergent, all later convergents, multi-run valuation words, and nonperiodic divergence remain uncontrolled.",
            "route_decision": {
                "discard": "linear scanning in k as the primary single-mountain method",
                "retain": "rigorous continued-fraction candidate compression followed by exact scaling-barrier tests and an effective all-convergent bound",
                "next_single_lemma": "EffectiveAllUpperConvergentScalingBarrierForSingleMountainWords",
            },
            "proof_dag": proof_dag(
                "CO",
                "SingleMountainCrossPowerGCDNecessityAndFiniteDiagonalAudit",
                "SingleMountainContinuedFractionCompressionAnd71356888Barrier",
                "FiniteLinearDiagonalScanIsTheOnlyAvailableExclusion",
                "EffectiveAllUpperConvergentScalingBarrierForSingleMountainWords",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or divergent orbit. The exact k<71,356,888 exclusion applies only to single-mountain words 1^k2^m.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-217",
            "theorem_name": "WeightedSecondMomentFullSupportCertificateAndSharpThresholdNoGo",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "The sharp two-moment inequality fails on every audited block and no pointwise arithmetic lower-tail estimate is proved.",
            "route_decision": {
                "discard": "lowering the sharp universal coefficient in the Cauchy support test or treating failure of that test as coverage",
                "retain": "targetwise or higher-order arithmetic control that separates the zero-count tail beyond the two-moment barrier",
                "next_single_lemma": "PointwiseGoldbachLowerTailBoundBeyondSecondMomentSupportBarrier",
            },
            "proof_dag": proof_dag(
                "GB",
                "RadixSelectorFullRepresentationHistogramAndPrecisionDepthNoGo",
                "WeightedSecondMomentFullSupportCertificateAndSharpThresholdNoGo",
                "TwoWeightedMomentsAlwaysSeparateTheGoldbachZeroDigit",
                "PointwiseGoldbachLowerTailBoundBeyondSecondMomentSupportBarrier",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The Cauchy support certificate and its sharpness are exact; the actual audited blocks do not satisfy it.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-217",
            "theorem_name": "SharpAdaptiveAbelTailPhaseTransitionAtTwoLogLog",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No lower bound for the actual twin-prime Abel transform supplies a positive surplus above the critical geometric tail on cofinal radii.",
            "route_decision": {
                "discard": "treating a bounded additive offset beyond 2 log log X as a negligible Abel tail",
                "retain": "an explicit parity-sensitive Abel lower surplus over the exact critical constant, then a diverging-offset transfer",
                "next_single_lemma": "TwinAbelLowerBoundWithExplicitSurplusAboveCriticalTailConstant",
            },
            "proof_dag": proof_dag(
                "TP",
                "QuantitativeAbelCountBracketAndFixedDilationTailNoGo",
                "SharpAdaptiveAbelTailPhaseTransitionAtTwoLogLog",
                "BoundedOffsetBeyondTwoLogLogMakesTheTailNegligible",
                "TwinAbelLowerBoundWithExplicitSurplusAboveCriticalTailConstant",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or last-twin counterexample. The geometric tail transition is sharp, but the parity-breaking Abel surplus is open.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "RelativeThresholdConvergentMomentCriticalTailAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-217 proves four exact partial, reduction, or no-go "
            "theorems and resolves none of the parent conjectures. It "
            "normalizes the RH transform threshold across finitely many "
            "radii, compresses single-mountain Collatz candidates to "
            "continued-fraction convergents and excludes k<71,356,888, "
            "proves the sharp Goldbach two-moment support threshold, and "
            "identifies the exact Twin Abel-tail phase transition."
        ),
        **sections,
        "cross_problem_synthesis": (
            "All four routes now use the scale of the discrete event rather "
            "than an absolute numerical tolerance: an RH first atom, a "
            "Collatz exponential rational approximation, a missing "
            "Goldbach support coordinate, and a Twin critical tail. The "
            "remaining gaps require arithmetic estimates at those relative "
            "scales."
        ),
        "literature_boundary": {
            "riemann": "Rigorous zero verification methods certify finite heights; this finite-observation no-go neither reproduces nor extends a verified height.",
            "collatz": "Continued fractions and linear forms in logarithms are established cycle tools; the theorem here is a narrow single-mountain reduction and carries no priority claim.",
            "goldbach": "Second-moment support bounds are elementary Cauchy consequences and do not improve binary circle-method exceptional-set estimates.",
            "twin_prime": "The critical tail calculation does not overcome the parity limitation of sieve-theoretic exact-gap-two estimates.",
        },
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_limited_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = []
    for section_key, problem_id in (
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin_prime", "twin-prime"),
    ):
        section = audit[section_key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "status": STATUS,
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "bounded_result": {"audit_ref": "#/relative_threshold_convergent_moment_tail_audit"},
            }
        )
    return attempts


def standalone_payload(section: dict[str, Any], problem_id: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "ticket_id": section["ticket_id"],
        "problem_id": problem_id,
        "status": STATUS,
        "theorem_name": section["theorem_name"],
        "declared_proposition": section["declared_proposition"],
        "mathematical_argument": section["mathematical_argument"],
        "reproducible_computation": section["reproducible_computation"],
        "discarded_route": section["route_decision"]["discard"],
        "remaining_gap": section["logical_limit"],
        "candidate_theorem": section["route_decision"]["next_single_lemma"],
        "claim_boundary": section["claim_boundary"],
        "proof_dag": section["proof_dag"],
    }


def write_outputs(audit: dict[str, Any]) -> None:
    integrated = ROOT / "data/open-problem/ticket217-relative-threshold-convergent-moment-tail.json"
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "relative_threshold_convergent_moment_tail_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-217-multiradius-relative-precision.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-217-convergent-compression.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-217-second-moment-support.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-217-critical-abel-tail.json",
    }
    problem_ids = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin_prime": "twin-prime",
    }
    for section_key, path in targets.items():
        write_json(path, standalone_payload(audit[section_key], problem_ids[section_key]))


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {
                "schema": SCHEMA,
                "status": STATUS,
                "machine_audit": audit["machine_audit"],
            },
            indent=2,
        )
    )
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
