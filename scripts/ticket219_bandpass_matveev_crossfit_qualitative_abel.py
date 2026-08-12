from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, ROUND_FLOOR, getcontext, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket162_formnorm_explicitbaker_integral_multiscale import (
    atanh_log_interval,
    log_integer_interval,
    matveev_constant_interval,
)
from ticket218_adaptive_radius_spike_residual_surplus import (
    collatz_spike_barrier_audit,
    goldbach_counts,
    prime_sieve,
    rounded_model_weight,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket219-bandpass-matveev-crossfit-qualitative-abel.v1"
GENERATED_AT = "2026-08-13T09:30:00+09:00"
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
            {"id": f"{prefix}-T218", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T219", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N219",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN219",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T218", f"{prefix}-T219"],
            [f"{prefix}-T219", f"{prefix}-N219"],
            [f"{prefix}-T219", f"{prefix}-OPEN219"],
            [f"{prefix}-OPEN219", prefix],
        ],
    }


def decimal_string(value: Decimal, digits: int = 24) -> str:
    return format(value, f".{digits}E")


def riemann_dyadic_bandpass_audit() -> dict[str, Any]:
    getcontext().prec = 90
    one = Decimal(1)
    kernel_floor = (-Decimal(2)).exp() * (one - (-Decimal(2)).exp())
    synthetic_atoms = (3, 7, 19, 44, 91, 173)
    rows = []
    failures = 0
    for height in (2, 4, 8, 16, 32, 64, 128):
        h = Decimal(height)
        transform = Decimal(0)
        for atom in synthetic_atoms:
            value = (-Decimal(atom) / h).exp()
            transform += value * (one - value)
        exact_band_count = sum(height <= atom <= 2 * height for atom in synthetic_atoms)
        certified_upper = int(
            (transform / kernel_floor).to_integral_value(rounding=ROUND_FLOOR)
        )
        failures += int(certified_upper < exact_band_count)
        rows.append(
            {
                "H": height,
                "synthetic_atom_count_in_closed_band_H_2H": exact_band_count,
                "bandpass_transform_W_H": decimal_string(transform),
                "kernel_floor_c": decimal_string(kernel_floor),
                "integer_count_upper_bound_floor_W_over_c": certified_upper,
                "upper_bound_covers_exact_band_count": (
                    certified_upper >= exact_band_count
                ),
            }
        )

    theorem = (
        "Let C be a locally finite nonnegative integer-valued defect measure "
        "on (0,infinity), L(s)=integral exp(-s t)dC(t), and "
        "W(H)=L(1/H)-L(2/H). Then W(H)=integral "
        "exp(-t/H)(1-exp(-t/H))dC(t). On H<=t<=2H the kernel is at "
        "least c=exp(-2)(1-exp(-2)), so "
        "C([H,2H])<=floor(W(H)/c). Therefore W(H)<c certifies an empty "
        "dyadic defect band. Finite verification below H0 plus this strict "
        "bound for every H=2^j H0 proves C=0. Conversely C=0 makes every "
        "W(H) zero, so the cofinal actual-defect condition is equivalent to "
        "RH inside the established defect-measure model, not an independent "
        "proof of RH."
    )
    proof = (
        "Subtract the two Laplace transforms to obtain the positive kernel. "
        "For x=t/H in [1,2], f(x)=exp(-x)(1-exp(-x)) is decreasing because "
        "f'(x)=exp(-x)(2exp(-x)-1)<0; hence its minimum is f(2)=c. "
        "Integrating over the band gives c C([H,2H])<=W(H), and integrality "
        "gives the floor. Dyadic bands cover [H0,infinity). The converse is "
        "immediate. Unlike a single Laplace radius, the difference suppresses "
        "both low-height and high-height contamination, but no prime-side "
        "interval enclosure for the actual defect difference is constructed."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "kernel": "exp(-t/H)*(1-exp(-t/H))",
        "kernel_floor_on_closed_band": decimal_string(kernel_floor),
        "synthetic_replay_rows": rows,
        "aggregate": {
            "positive_dyadic_bandpass_certificate_proved": True,
            "low_and_high_tail_suppression_proved": True,
            "cofinal_actual_defect_condition_equivalent_to_RH": True,
            "prime_side_actual_zeta_enclosure_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "Renaming the cofinal inequality as an envelope does not weaken "
            "RH: in the defect model it is equivalent to the absence of all "
            "off-critical atoms. The new value is localization and a cleaner "
            "computational interface, not a resolution."
        ),
        "failure_count": failures,
    }


def direct_matveev_constant_interval() -> tuple[Fraction, Fraction]:
    lower, upper = matveev_constant_interval()
    # h(4/3)=log(4)=2 log(2), while h(3/2)=log(3).
    return 2 * lower, 2 * upper


def direct_matveev_threshold() -> dict[str, Any]:
    with localcontext() as context:
        context.prec = 80
        log_three = Decimal(3).ln()
        constant = (
            Decimal("1.4")
            * Decimal(30) ** 5
            * Decimal(2) ** Decimal("4.5")
            * Decimal(4).ln()
            * log_three
        )

        def condition(value: int) -> bool:
            number = Decimal(value)
            return number * log_three > constant * (1 + (2 * number).ln())

        low = 1
        high = 2
        while not condition(high):
            high *= 2
        while low + 1 < high:
            middle = (low + high) // 2
            if condition(middle):
                high = middle
            else:
                low = middle

    threshold = high
    constant_lower, constant_upper = direct_matveev_constant_interval()
    log_three_lower, log_three_upper = atanh_log_interval(3)
    log_threshold_lower, log_threshold_upper = log_integer_interval(2 * threshold)
    log_previous_lower, log_previous_upper = log_integer_interval(
        2 * (threshold - 1)
    )
    threshold_margin_lower = (
        threshold * log_three_lower
        - constant_upper * (1 + log_threshold_upper)
    )
    previous_margin_upper = (
        (threshold - 1) * log_three_upper
        - constant_lower * (1 + log_previous_lower)
    )
    derivative_lower = log_three_lower - constant_upper / threshold
    checks = {
        "threshold_condition_certified_positive": threshold_margin_lower > 0,
        "previous_integer_certified_nonpositive": previous_margin_upper < 0,
        "condition_increasing_from_threshold": derivative_lower > 0,
    }
    return {
        "matveev_constant": {
            "formula": "1.4*30^5*2^4.5*log(4)*log(3)",
            "lower_decimal": float(constant_lower),
            "upper_decimal": float(constant_upper),
        },
        "first_certified_numerator_p": threshold,
        "threshold_margin_lower": float(threshold_margin_lower),
        "previous_margin_upper": float(previous_margin_upper),
        "derivative_lower_at_threshold": float(derivative_lower),
        "checks": checks,
    }


def collatz_matveev_closure_audit() -> dict[str, Any]:
    previous = collatz_spike_barrier_audit()
    threshold = direct_matveev_threshold()
    threshold_p = int(threshold["first_certified_numerator_p"])
    next_upper = previous["next_unaudited_upper_convergent"]
    prefix_closed = previous["aggregate"]["all_audited_upper_convergents_excluded"]
    tail_starts_after_threshold = int(next_upper["p"]) >= threshold_p
    checks = {
        **threshold["checks"],
        "ticket218_prefix_closed": prefix_closed,
        "first_unaudited_upper_convergent_exceeds_matveev_threshold": (
            tail_starts_after_threshold
        ),
        "all_later_upper_numerators_exceed_threshold_by_monotonicity": (
            tail_starts_after_threshold
        ),
    }
    failures = sum(not value for value in checks.values())
    theorem = (
        "No positive accelerated Collatz cycle has a single-mountain valuation "
        "word 1^k 2^m. Indeed TICKET-217 reduces any such cycle, after "
        "gcd(m,k) reduction, to an upper convergent p/q of "
        "alpha=log(3/2)/log(4/3) satisfying "
        "0<(4/3)^p(3/2)^(-q)-1<3^(-p). Matveev's explicit rational "
        "two-logarithm estimate gives log Lambda>-K(1+log(2p)), with "
        "K=1.4*30^5*2^4.5*log(4)*log(3). Exact rational log intervals "
        "certify that p>=27,456,680,737 makes the lower bound at least "
        "3^(-p), a contradiction. TICKET-218 exactly excludes all 49 upper "
        "convergents before the first unaudited one, whose numerator is "
        "16,672,027,258,049,147,969,018,986,102,532,625,254,200,541,727,292 "
        "and already exceeds the Matveev threshold. Monotonicity of convergent "
        "numerators closes every later candidate."
    )
    proof = (
        "Because log(3/2)>log(4/3), an upper convergent has p>q, so the "
        "Matveev coefficient parameter is B=p. The rational heights are "
        "log(4) and log(3), yielding the displayed conservative constant. "
        "For p at or above the certified threshold, "
        "p log 3>K(1+log(2p)); hence Matveev gives Lambda>3^(-p), contrary "
        "to the necessary near-collision inequality. The exact interval "
        "certificate also proves the threshold inequality is increasing "
        "thereafter. TICKET-218 covers every earlier upper convergent, so the "
        "two ranges meet without a gap. This excludes one valuation-word "
        "family only; arbitrary multi-run words and nonperiodic divergence "
        "are untouched."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "matveev_threshold_certificate": threshold,
        "ticket218_audited_upper_convergent_count": previous["aggregate"][
            "audited_upper_convergent_count"
        ],
        "first_unaudited_upper_convergent": next_upper,
        "range_glue_checks": checks,
        "aggregate": {
            "explicit_exponential_partial_quotient_bound_proved": True,
            "ticket218_finite_prefix_and_matveev_tail_meet_without_gap": True,
            "all_positive_single_mountain_cycles_excluded": True,
            "all_multi_run_cycles_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "A complete theorem for the word family 1^k2^m has zero "
            "combinatorial coverage of general long valuation words. It must "
            "not be promoted to the Collatz conjecture."
        ),
        "failure_count": failures,
    }


def goldbach_cross_fitted_moment_audit() -> dict[str, Any]:
    starts = (128, 512, 2048, 8192, 32768)
    flags = prime_sieve(2 * max(starts))
    primes = [value for value in range(2, len(flags)) if flags[value]]
    shape_scale = 1_000_000
    rows = []
    failures = 0
    transcript = hashlib.sha256()

    for start in starts:
        counts = goldbach_counts(start, flags, primes)
        targets = list(range(start, 2 * start, 2))
        weights = [
            rounded_model_weight(target, primes, shape_scale)
            for target in targets
        ]
        fold_rows = []
        for held_out_fold in (0, 1):
            train = [index for index in range(len(counts)) if index % 2 != held_out_fold]
            test = [index for index in range(len(counts)) if index % 2 == held_out_fold]
            fit_numerator = sum(counts[index] * weights[index] for index in train)
            fit_denominator = sum(weights[index] ** 2 for index in train)
            minimum_test_weight = min(weights[index] for index in test)
            moment_rows = []
            for order in (4, 8):
                residual_sum = sum(
                    abs(
                        counts[index] * fit_denominator
                        - fit_numerator * weights[index]
                    )
                    ** order
                    for index in test
                )
                threshold = (fit_numerator * minimum_test_weight) ** order
                passed = residual_sum < threshold
                moment_rows.append(
                    {
                        "order_p": order,
                        "exact_residual_integer_sum": str(residual_sum),
                        "exact_zero_coordinate_threshold": str(threshold),
                        "residual_to_threshold_ratio": decimal_string(
                            Decimal(residual_sum) / Decimal(threshold), 18
                        ),
                        "held_out_full_support_certificate_passed": passed,
                    }
                )
            eighth_passed = moment_rows[1][
                "held_out_full_support_certificate_passed"
            ]
            failures += int(not eighth_passed)
            transcript.update(
                (
                    f"{start}:{held_out_fold}:{fit_numerator}:{fit_denominator}:"
                    + ":".join(
                        f"{entry['order_p']}="
                        f"{int(entry['held_out_full_support_certificate_passed'])}"
                        for entry in moment_rows
                    )
                    + "\n"
                ).encode("ascii")
            )
            fold_rows.append(
                {
                    "held_out_fold": held_out_fold,
                    "training_index_parity": 1 - held_out_fold,
                    "training_and_test_disjoint": set(train).isdisjoint(test),
                    "training_count": len(train),
                    "held_out_count": len(test),
                    "least_squares_scale_numerator_P": str(fit_numerator),
                    "least_squares_scale_denominator_Q": str(fit_denominator),
                    "moment_rows": moment_rows,
                    "eighth_moment_held_out_support_certified": eighth_passed,
                }
            )
        rows.append(
            {
                "dyadic_start_X": start,
                "minimum_exact_representation_count": min(counts),
                "fold_rows": fold_rows,
                "both_folds_eighth_moment_certified": all(
                    fold["eighth_moment_held_out_support_certified"]
                    for fold in fold_rows
                ),
            }
        )

    theorem = (
        "Partition a finite coordinate set into folds. For each fold F, fit a "
        "positive model M_i=(P_F/Q_F)w_i using only coordinates outside F. "
        "If sum_{i in F}|A_i Q_F-P_F w_i|^p is strictly below "
        "(P_F min_{i in F}w_i)^p, then every A_i in F is positive. If this "
        "holds for every fold, the full vector has positive support. This is "
        "the sharp residual-moment argument of TICKET-218 with disjoint "
        "parameter fitting. Exact two-fold replay at five Goldbach dyadic "
        "blocks certifies all ten held-out folds at p=8; p=4 certifies only "
        "one of the ten folds."
    )
    proof = (
        "For a zero coordinate j in held-out fold F, its residual contribution "
        "equals (P_F w_j)^p and is at least the displayed threshold, a "
        "contradiction. The model parameters cannot read any held-out count "
        "because training and test index sets are disjoint. Taking the union "
        "over folds proves full support. The audit still enumerates the held-"
        "out residuals, so it is a finite certificate and not the missing "
        "cofinal circle-method estimate."
    )
    fold_entries = [fold for row in rows for fold in row["fold_rows"]]
    return {
        "theorem": theorem,
        "proof": proof,
        "cross_fit_contract": (
            "fit P_F/Q_F on complement of F; evaluate residual moment only on F"
        ),
        "dyadic_goldbach_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "cross_fitted_support_theorem_proved": True,
            "training_test_disjoint_for_every_fold": all(
                fold["training_and_test_disjoint"] for fold in fold_entries
            ),
            "exact_eighth_moment_held_out_folds_certified": sum(
                int(fold["eighth_moment_held_out_support_certified"])
                for fold in fold_entries
            ),
            "exact_fourth_moment_held_out_folds_certified": sum(
                int(
                    fold["moment_rows"][0][
                        "held_out_full_support_certificate_passed"
                    ]
                )
                for fold in fold_entries
            ),
            "cofinal_cross_fitted_eighth_moment_bound_proved": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "Cross-fitting removes same-coordinate scale leakage but does not "
            "replace held-out representation counts by an analytic bound. A "
            "finite pass cannot establish the cofinal foldwise inequality."
        ),
        "failure_count": failures,
    }


def sparse_abel_value(scale: int) -> tuple[float, int]:
    radius = 1.0 - 1.0 / scale
    total = 0.0
    term_count = 0
    exponent = 1
    while exponent < 2048:
        support = (1 << exponent) + 1
        term = radius**support
        total += term
        term_count += 1
        if support > scale and term < 1e-20:
            break
        exponent += 1
    return total, term_count


def twin_qualitative_abel_audit() -> dict[str, Any]:
    scales = (1_000, 10_000, 100_000, 1_000_000)
    flags = prime_sieve(max(scales) + 3)
    twin_starts = [
        value
        for value in range(3, len(flags) - 2, 2)
        if flags[value] and flags[value + 2]
    ]
    rows = []
    failures = 0
    for scale in scales:
        radius = 1.0 - 1.0 / scale
        bounded_twins = [value for value in twin_starts if value <= scale]
        actual_partial_abel = math.fsum(radius**value for value in bounded_twins)
        sparse_value, sparse_terms = sparse_abel_value(scale)
        normalization = scale / math.log(scale) ** 2
        quarter_count_lower = len(bounded_twins) / 4.0
        checks = {
            "actual_partial_abel_dominates_quarter_count": (
                actual_partial_abel + 1e-12 >= quarter_count_lower
            ),
            "sparse_normalized_coefficient_below_one_half": (
                sparse_value / normalization < 0.5
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "X": scale,
                "actual_twin_count_through_X": len(bounded_twins),
                "actual_partial_Abel_sum_through_X": actual_partial_abel,
                "quarter_of_bounded_twin_count": quarter_count_lower,
                "sparse_support_2_pow_j_plus_1_Abel_value": sparse_value,
                "sparse_terms_numerically_summed": sparse_terms,
                "sparse_Abel_over_X_log2X": sparse_value / normalization,
                "checks": checks,
                "floating_values_are_diagnostics_not_interval_proofs": True,
            }
        )

    theorem = (
        "For any 0-1 sequence a_n, F(r)=sum a_n r^n is unbounded as r tends "
        "to one from below if and only if the support of a is infinite. "
        "Applied to the twin-prime indicator, unboundedness of the actual "
        "Abel transform is exactly equivalent to the Twin Prime Conjecture. "
        "The quantitative TICKET-218 condition liminf F(1-1/X)/(X/log^2 X)>"
        "1/2 is sufficient but not a necessary qualitative infinitude "
        "criterion: the infinite odd support n_j=2^j+1 has F(1-1/X)=O(log X) "
        "and hence normalized liminf zero. Moreover, for any support count "
        "T(X), F(1-1/X)>=T(X)/4 for X>=2."
    )
    proof = (
        "Finite support makes F bounded by its support size. For infinite "
        "support, choose any K supported indices; their finite partial sum "
        "tends to K as r tends to one, so F is unbounded. For n_j=2^j+1, "
        "there are O(log X) terms below X, while the terms above X are at "
        "most a convergent sum of exp(-2^k), giving F=O(log X). Finally, "
        "for n<=X and X>=2, (1-1/X)^n>=(1-1/X)^X>=1/4, proving the "
        "finite lower certificate. This refutes necessity only for abstract "
        "binary supports, not the Hardy-Littlewood prediction for actual "
        "twins."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "qualitative_equivalence": (
            "infinitely many twin primes iff the actual twin Abel transform is unbounded"
        ),
        "finite_and_sparse_diagnostic_rows": rows,
        "aggregate": {
            "qualitative_abel_infinitude_equivalence_proved": True,
            "ticket218_density_scale_condition_not_necessary_for_abstract_infinitude": True,
            "finite_quarter_count_lower_certificate_proved": True,
            "actual_twin_abel_transform_unbounded_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The sparse sequence is not a model of the primes and does not "
            "disprove the TICKET-218 condition for actual twins. It proves "
            "only that requiring a Hardy-Littlewood-scale coefficient is an "
            "overstrong route to qualitative infinitude."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_dyadic_bandpass_audit()
    collatz_compute = collatz_matveev_closure_audit()
    goldbach_compute = goldbach_cross_fitted_moment_audit()
    twin_compute = twin_qualitative_abel_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-219",
            "theorem_name": "PositiveDyadicBandpassDefectCertificateAndEquivalenceAudit",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No rigorous prime-side interval enclosure bounds the actual dyadic defect difference below its positive kernel floor on every dyadic band.",
            "route_decision": {
                "discard": "treating the TICKET-218 cofinal defect envelope as a theorem weaker than RH",
                "retain": "the positive dyadic band-pass kernel as a localized, tail-suppressing target for explicit-formula interval arithmetic",
                "next_single_lemma": "PrimeSideDyadicBandpassDefectEnclosureBelowKernelFloor",
            },
            "proof_dag": proof_dag(
                "RH",
                "ScaleAdaptiveRadiusCertificateAndSignalPhaseTransition",
                "PositiveDyadicBandpassDefectCertificateAndEquivalenceAudit",
                "CofinalDefectEnvelopeIsStrictlyWeakerThanRH",
                "PrimeSideDyadicBandpassDefectEnclosureBelowKernelFloor",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof and no off-line zero. TICKET-219 proves a localized exact certificate and explicitly records that its cofinal actual-defect premise is RH-equivalent.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-219",
            "theorem_name": "ExplicitMatveevClosureOfAllPositiveSingleMountainCycles",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "The theorem covers only valuation words 1^k2^m; arbitrary multi-run cycles and nonperiodic divergent trajectories remain uncontrolled.",
            "route_decision": {
                "discard": "continued enumeration of single-mountain convergents after the explicit Matveev tail already closes them",
                "retain": "lift the near-collision/Baker mechanism from one run to arbitrary cyclic valuation words without losing phase information",
                "next_single_lemma": "EffectiveBakerSeparationForAllPositiveCycleValuationWords",
            },
            "proof_dag": proof_dag(
                "CO",
                "ExponentialNextDenominatorSpikeBarrierAnd49ConvergentExclusion",
                "ExplicitMatveevClosureOfAllPositiveSingleMountainCycles",
                "SingleMountainFamilyClosureImpliesCollatz",
                "EffectiveBakerSeparationForAllPositiveCycleValuationWords",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or divergent orbit. A complete infinite single-mountain cycle family is excluded, but its share of general valuation words vanishes.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-219",
            "theorem_name": "LeakageFreeCrossFittedEighthMomentSupportCertificate",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "No cofinal arithmetic estimate proves the cross-fitted eighth residual moment inequality without enumerating the held-out Goldbach counts.",
            "route_decision": {
                "discard": "using a scale fitted on the same target coordinates as independent evidence for the Hardy-Littlewood model",
                "retain": "foldwise externalized model fitting plus a cofinal eighth-moment bound and finite verification below an analytic cutoff",
                "next_single_lemma": "CofinalCrossFittedGoldbachEighthMomentBelowFoldwiseZeroBarrier",
            },
            "proof_dag": proof_dag(
                "GB",
                "SharpResidualMomentSupportCertificateAndExactEighthMomentAudit",
                "LeakageFreeCrossFittedEighthMomentSupportCertificate",
                "SameBlockLeastSquaresFitIsIndependentArithmeticEvidence",
                "CofinalCrossFittedGoldbachEighthMomentBelowFoldwiseZeroBarrier",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. Ten held-out folds pass exactly at p=8, but the cofinal arithmetic moment estimate is open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-219",
            "theorem_name": "QualitativeAbelInfinitudeEquivalenceAndDensityScaleNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No parity-sensitive argument proves that the actual twin-prime Abel transform is unbounded, or equivalently that infinitely many dyadic blocks contain a twin.",
            "route_decision": {
                "discard": "requiring a positive Hardy-Littlewood-scale Abel liminf as though it were necessary for qualitative twin infinitude",
                "retain": "the exact unbounded-Abel criterion, connected to parity-corrected positive twin blocks rather than an assumed density scale",
                "next_single_lemma": "UnboundedParityCorrectedTwinAbelTransform",
            },
            "proof_dag": proof_dag(
                "TP",
                "SharpAbelSurplusToTwinCountTransferAtCriticalConstant",
                "QualitativeAbelInfinitudeEquivalenceAndDensityScaleNoGo",
                "PositiveNormalizedAbelLiminfIsNecessaryForTwinInfinitude",
                "UnboundedParityCorrectedTwinAbelTransform",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or last-twin counterexample. The density-scale requirement is demoted to a sufficient quantitative route; qualitative Abel unboundedness remains open and equivalent to infinitude.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "BandpassMatveevCrossFitQualitativeAbelAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-219 proves four exact partial or no-go theorems and resolves "
            "none of the parent conjectures. It localizes RH defects with a "
            "positive dyadic band-pass certificate while proving the cofinal "
            "actual-defect premise is RH-equivalent; combines an explicit "
            "Matveev threshold with the TICKET-218 prefix to exclude every "
            "positive single-mountain Collatz cycle; removes same-fold model "
            "fitting from the finite Goldbach eighth-moment certificates; and "
            "replaces an overstrong normalized Twin Abel target by the exact "
            "qualitative unboundedness criterion."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The audit separates computational interfaces from theorem strength. "
            "Only the Collatz subfamily closes completely. RH and Twin targets "
            "are marked when they are equivalent to the parent problem, and the "
            "Goldbach finite statistic is made out-of-fold before any cofinal "
            "claim is considered."
        ),
        "literature_boundary": {
            "riemann": "The Laplace-kernel inequality is elementary inside the project defect formalism and is not a new zero-free region.",
            "collatz": "The tail uses Matveev's published explicit lower bound specialized to two positive rationals; project novelty is limited to the exact range glue for this word family.",
            "goldbach": "Cross-fitting is an experimental-design correction, not a new circle-method estimate.",
            "twin_prime": "The Abel/support equivalence is elementary and does not overcome the sieve parity barrier.",
        },
        "machine_audit": {
            "exact_partial_theorem_count": 4,
            "refuted_or_limited_route_count": 4,
            "closed_infinite_subfamily_count": 1,
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
                "bounded_result": {
                    "audit_ref": "#/bandpass_matveev_crossfit_qualitative_abel_audit"
                },
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
    integrated = (
        ROOT
        / "data/open-problem/ticket219-bandpass-matveev-crossfit-qualitative-abel.json"
    )
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "bandpass_matveev_crossfit_qualitative_abel_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-219-dyadic-bandpass.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-219-matveev-single-mountain.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-219-cross-fitted-eighth-moment.json",
        "twin_prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-219-qualitative-abel.json",
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
