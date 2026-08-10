from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket210-cofinal-fiveone-primegap-scaledtwin.v1"
GENERATED_AT = "2026-08-10T23:30:00+09:00"
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
            {"id": f"{prefix}-T209", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T210", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N210",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN210",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T209", f"{prefix}-T210"],
            [f"{prefix}-T210", f"{prefix}-N210"],
            [f"{prefix}-T210", f"{prefix}-OPEN210"],
            [f"{prefix}-OPEN210", prefix],
        ],
    }


def symmetric_quartet_polynomial(s: complex) -> complex:
    z = s - 0.5
    return z**4 + (15 / 8) * z**2 + Fraction(289, 256)


def riemann_cofinal_countermodel_audit() -> dict[str, Any]:
    rows = []
    failures = 0
    for height in (2, 4, 8, 16, 32, 64):
        lower = (height * height - 1) ** 2
        grid_minimum = min(
            abs(symmetric_quartet_polynomial(complex(index / 32, height)))
            for index in range(-8, 41)
        )
        lower_holds_on_grid = grid_minimum + 1e-10 >= lower
        failures += int(not lower_holds_on_grid)
        rows.append(
            {
                "height_T": height,
                "exact_product_distance_lower_bound": str(lower),
                "sampled_minimum_modulus": f"{grid_minimum:.12f}",
                "sampled_minimum_respects_exact_lower_bound": lower_holds_on_grid,
            }
        )

    theorem = (
        "For every sufficiently large integer n there is T_n in (n,n+1) "
        "such that zeta(s) is nonzero on -1/4<=Re(s)<=5/4 at Im(s)=T_n; "
        "the minimum modulus on that compact segment is therefore positive. "
        "This existential cofinal nonvanishing does not imply RH. The real "
        "entire polynomial P(s)=z^4+(15/8)z^2+289/256, z=s-1/2, satisfies "
        "P(1-s)=P(s), has the four off-critical zeros "
        "1/2+/-1/4+/-i, and for every T>1 obeys "
        "min_sigma |P(sigma+iT)| >= (T^2-1)^2."
    )
    proof = (
        "Completed xi is a nonzero entire function, hence its zeros are "
        "isolated and every compact rectangle contains only finitely many. "
        "Remove from (n,n+1) the finitely many ordinates of zeros in the "
        "central strip and choose any remaining T_n. At positive height all "
        "elementary and gamma factors relating xi and zeta are nonzero, so "
        "zeta has no zero on the segment; compactness gives a positive, "
        "height-dependent minimum. For the countermodel, the zeros in the "
        "centered variable z are +/-1/4+/-i. Evenness gives P(1-s)=P(s) and "
        "real coefficients give conjugation symmetry. On Im(s)=T>1, each of "
        "the two roots at imaginary part +1 is at distance at least T-1 and "
        "each of the two roots at -1 is at distance at least T+1. Multiplying "
        "the four distances gives (T-1)^2(T+1)^2=(T^2-1)^2 despite the "
        "off-critical zeros."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "existential_zeta_statement": {
            "height_band": "T_n in (n,n+1)",
            "central_segment": "-1/4<=Re(s)<=5/4",
            "positive_minimum_exists": True,
            "effective_height_or_margin_constructed": False,
        },
        "symmetric_countermodel": {
            "polynomial": "P(s)=z^4+(15/8)z^2+289/256, z=s-1/2",
            "zeros": [
                "1/4+i",
                "3/4+i",
                "1/4-i",
                "3/4-i",
            ],
            "functional_symmetry": "P(1-s)=P(s)",
            "conjugation_symmetry": "P(conj(s))=conj(P(s))",
            "cofinal_horizontal_lower_bound": "|P(sigma+iT)|>=(T^2-1)^2 for T>1",
            "off_critical_zero_count": 4,
        },
        "countermodel_rows": rows,
        "aggregate": {
            "existential_cofinal_central_nonvanishing_proved": True,
            "effective_zeta_clearance_proved": False,
            "cofinal_nonvanishing_implies_rh_refuted": True,
            "boundary_winding_control_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The countermodel refutes only the inference from functional "
            "symmetry plus cofinal horizontal clearance to RH. It does not "
            "share zeta's Euler product and does not locate an off-line zeta "
            "zero. The existence proof supplies neither computable heights "
            "nor argument-principle winding increments."
        ),
        "failure_count": failures,
    }


def weak_compositions(total: int, parts: int) -> Iterable[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


def total_valuation_upper_bound(length: int) -> int:
    exponent = 0
    while 2 ** (exponent + 1) * 3**length <= 10**length:
        exponent += 1
    return exponent


def cycle_fixed_point(word: tuple[int, ...]) -> Fraction | None:
    slope = Fraction(1)
    intercept = Fraction(0)
    for valuation in word:
        denominator = 2**valuation
        slope = Fraction(3, denominator) * slope
        intercept = (3 * intercept + 1) / denominator
    if slope >= 1:
        return None
    return intercept / (1 - slope)


def five_one_words(length: int, maximum_total: int) -> Iterator[tuple[int, ...]]:
    baseline_total = 2 * length - 5
    if baseline_total > maximum_total:
        return
    for other_ones in combinations(range(1, length - 1), 4):
        one_positions = {0, *other_ones}
        non_one_positions = [
            index for index in range(length) if index not in one_positions
        ]
        for extra_total in range(maximum_total - baseline_total + 1):
            for extras in weak_compositions(extra_total, len(non_one_positions)):
                word = [
                    1 if index in one_positions else 2 for index in range(length)
                ]
                for index, extra in zip(non_one_positions, extras, strict=True):
                    word[index] += extra
                yield tuple(word)


def collatz_five_one_audit() -> dict[str, Any]:
    rows = []
    total_words = 0
    candidate_count = 0
    failures = 0
    for length in range(6, 20):
        maximum_total = total_valuation_upper_bound(length)
        baseline_total = 2 * length - 5
        digest = hashlib.sha256()
        local_words = 0
        local_candidates = 0
        for word in five_one_words(length, maximum_total):
            local_words += 1
            digest.update((",".join(map(str, word)) + "\n").encode("ascii"))
            fixed = cycle_fixed_point(word)
            if (
                fixed is not None
                and fixed.denominator == 1
                and fixed.numerator >= 3
                and fixed.numerator % 2 == 1
            ):
                local_candidates += 1
        total_words += local_words
        candidate_count += local_candidates
        failures += local_candidates
        rows.append(
            {
                "length_h": length,
                "minimum_total_valuation_2h_minus_5": baseline_total,
                "maximum_total_valuation_from_minimum_bound": maximum_total,
                "enumerated_word_count": local_words,
                "positive_odd_integer_fixed_point_count": local_candidates,
                "valuation_word_sha256": digest.hexdigest(),
            }
        )

    multiplicity = 5
    exact_length_cap = math.floor(
        multiplicity * math.log(2) / math.log(Fraction(6, 5))
    )
    threshold = exact_length_cap + 1
    threshold_left = 2 ** (2 * threshold - multiplicity) * 3**threshold
    threshold_right = 10**threshold
    long_exclusion = threshold_left > threshold_right
    failures += int(total_words != 29758)
    failures += int(candidate_count != 0)
    failures += int(not long_exclusion)

    theorem = (
        "No nontrivial positive accelerated Collatz cycle has exactly five "
        "valuation entries equal to one and every remaining valuation at "
        "least two. More generally, exactly k ones force "
        "(6/5)^h<=2^k and therefore "
        "h<=floor(k log(2)/log(6/5)). For k=5 this gives h<=19; exact "
        "affine enumeration of all 29,758 minimum-rotated words of lengths "
        "6 through 19 finds no positive odd integer fixed point. Hence a "
        "hypothetical nontrivial positive cycle contains at least six ones."
    )
    proof = (
        "Rotate a cycle to its minimum odd value m>=3. Its first valuation is "
        "one, since valuation at least two would send m below itself; its last "
        "valuation is at least two, since valuation one would send the "
        "predecessor above itself to m. Multiplication around a length-h cycle "
        "with valuation sum A gives 2^A=product_i(3+1/x_i)<=(10/3)^h. If "
        "exactly k entries are one and all others are at least two, A>=2h-k, "
        "so (6/5)^h<=2^k. For k=5, h<=19 and the same product inequality "
        "bounds A at every remaining h. The fixed first and last positions, "
        "the other four one-positions, and all weak compositions of A-(2h-5) "
        "enumerate every possible minimum rotation exactly. Rational affine "
        "composition rejects every one of the 29,758 words."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "general_k_one_length_cap": (
            "h<=floor(k*log(2)/log(6/5)) for a cycle with exactly k ones"
        ),
        "k": multiplicity,
        "exact_length_cap_h": exact_length_cap,
        "exact_enumeration_rows": rows,
        "total_exact_words_enumerated": total_words,
        "positive_odd_integer_fixed_point_count": candidate_count,
        "length_at_least_twenty_exclusion": {
            "threshold_h": threshold,
            "left_2_pow_35_times_3_pow_20": str(threshold_left),
            "right_10_pow_20": str(threshold_right),
            "left_exceeds_right": long_exclusion,
            "growth_factor_per_extra_length": "6/5",
        },
        "aggregate": {
            "exactly_five_valuation_one_cycle_stratum_excluded": True,
            "minimum_required_valuation_one_multiplicity_in_nontrivial_cycle": 6,
            "six_or_more_one_necklaces_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This closes the full five-one periodic stratum, with arbitrary "
            "remaining valuations >=2. It does not exclude cycles containing "
            "six or more ones and says nothing about nonperiodic divergence."
        ),
        "failure_count": failures,
    }


def prime_sieve(limit: int) -> list[bool]:
    flags = [True] * (limit + 1)
    flags[0:2] = [False, False]
    for candidate in range(2, math.isqrt(limit) + 1):
        if flags[candidate]:
            flags[candidate * candidate : limit + 1 : candidate] = [False] * (
                (limit - candidate * candidate) // candidate + 1
            )
    return flags


def record_prime_gap_rows(limit: int = 2_000_000) -> list[dict[str, Any]]:
    flags = prime_sieve(limit)
    primes = [value for value in range(2, limit + 1) if flags[value]]
    rows = []
    record = 0
    for left, right in zip(primes, primes[1:]):
        gap = right - left
        if gap <= record or left == 2:
            continue
        record = gap
        target = right - 1
        blocked_through = gap - 2
        witness_checks = [
            prime
            for prime in primes
            if prime <= blocked_through and flags[target - prime]
        ]
        least_witness = next(
            (
                prime
                for prime in primes
                if prime <= target - 2 and flags[target - prime]
            ),
            None,
        )
        rows.append(
            {
                "left_prime": left,
                "right_prime": right,
                "record_gap_g": gap,
                "even_target_N": target,
                "transferred_strict_lower_bound_W_gt": blocked_through,
                "violating_witness_count_at_or_below_bound": len(witness_checks),
                "actual_least_witness_in_finite_fixture": least_witness,
                "interior_all_composite": all(
                    not flags[value] for value in range(left + 1, right)
                ),
            }
        )
    return rows[-10:]


def goldbach_prime_gap_transfer_audit() -> dict[str, Any]:
    rows = record_prime_gap_rows()
    failures = sum(
        int(not row["interior_all_composite"])
        + int(row["violating_witness_count_at_or_below_bound"] != 0)
        + int(
            row["actual_least_witness_in_finite_fixture"]
            <= row["transferred_strict_lower_bound_W_gt"]
        )
        for row in rows
    )
    theorem = (
        "If q<r are consecutive odd primes with gap g=r-q and N=r-1, then "
        "N is even and its least Goldbach witness satisfies W(N)>g-2. "
        "Combining this transfer with the Ford-Green-Konyagin-Maynard-Tao "
        "large-gap theorem gives an independent unbounded sequence with "
        "W(N) >> log N log_2 N log_4 N / log_3 N. This does not improve "
        "TICKET-209's stronger c log N log_2 N floor, because "
        "log_4 N/log_3 N tends to zero; it proves that importing the current "
        "large-prime-gap lower bound alone cannot advance that floor."
    )
    proof = (
        "For every prime p<=g-2, q+1<=N-p<=r-3. This lies strictly between "
        "the consecutive primes q and r and is therefore composite, proving "
        "W(N)>g-2. At endpoints of record prime gaps, the published theorem "
        "G(X)>>log X log_2 X log_4 X/log_3 X applies with X=r. Since N=r-1, "
        "the iterated logarithms are asymptotically unchanged. Finally "
        "log_4 N/log_3 N tends to zero, so this transferred published bound "
        "is asymptotically below the TICKET-209 covering-congruence floor."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "exact_transfer": (
            "consecutive primes q<r, g=r-q, N=r-1 imply W(N)>g-2"
        ),
        "imported_large_gap_theorem": {
            "statement": "G(X)>>log X log_2 X log_4 X/log_3 X",
            "authors": "Ford, Green, Konyagin, Maynard, Tao",
            "journal_doi": "https://doi.org/10.1090/jams/876",
            "primary_preprint": "https://arxiv.org/abs/1412.5029",
            "project_claims_original_proof_of_imported_theorem": False,
        },
        "finite_record_gap_rows": rows,
        "aggregate": {
            "prime_gap_to_least_witness_transfer_proved": True,
            "independent_iterated_log_witness_sequence_obtained": True,
            "improves_ticket209_covering_floor": False,
            "current_prime_gap_route_alone_advances_covering_floor": False,
            "goldbach_counterexample_found": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The dominance comparison concerns only the currently published "
            "large-gap lower bound passed through this exact transfer. It is "
            "not a theorem that every future prime-gap method is weaker. Each "
            "constructed N may have, and in the finite rows does have, a "
            "larger Goldbach witness."
        ),
        "failure_count": failures,
    }


def factorial_scale_row(parameter: int) -> dict[str, Any]:
    base = math.factorial(parameter)
    length = parameter - 3
    log_x = math.lgamma(parameter + 1)
    loglog_x = math.log(log_x)
    scale = log_x / loglog_x
    transcript = []
    all_certified = True
    for offset in range(2, parameter - 1):
        lower = base + offset
        upper = lower + 2
        certified = (
            lower % offset == 0
            and upper % (offset + 2) == 0
            and lower > offset
            and upper > offset + 2
        )
        all_certified &= certified
        transcript.append(f"{offset},{int(certified)}")
    return {
        "factorial_parameter_K": parameter,
        "factorial_base_decimal_digits": len(str(base)),
        "twin_free_candidate_length_H": length,
        "log_X_over_loglog_X_decimal": f"{scale:.12f}",
        "H_over_log_X_over_loglog_X_decimal": f"{length / scale:.12f}",
        "H_at_least_one_quarter_scale": length >= scale / 4,
        "all_composite_pair_certificates_hold": all_certified,
        "certificate_count": length,
        "certificate_sha256": hashlib.sha256(
            "\n".join(transcript).encode("ascii")
        ).hexdigest(),
    }


def twin_scaled_factorial_audit() -> dict[str, Any]:
    rows = [factorial_scale_row(k) for k in (8, 16, 32, 64, 128, 256)]
    failures = sum(
        int(not row["H_at_least_one_quarter_scale"])
        + int(not row["all_composite_pair_certificates_hold"])
        for row in rows
    )
    theorem = (
        "For every integer K>=8, put X=K! and H=K-3. The H consecutive "
        "lower candidates X+j, 2<=j<=K-2, contain no twin-prime pair, and "
        "H >= (1/4) log X/log log X. Consequently there are infinitely many "
        "twin-free local windows at least a fixed multiple of the "
        "log X/log log X scale. Any proof requiring a twin pair in every "
        "window at or below this scale is false."
    )
    proof = (
        "For 2<=j<=K-2, j divides X+j and j+2 divides X+j+2, and both "
        "divisors are proper. Thus all H=K-3 lower candidates are twin-free. "
        "Also log X<=K log K. The last K/2 factors in K! are at least K/2, "
        "so log X>=(K/2)log(K/2), which for K>=8 implies "
        "log log X>=(1/2)log K. Hence log X/log log X<=2K, while "
        "H=K-3>=K/2, giving H>=(1/4)log X/log log X."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "scale_inequality": "K-3 >= (1/4)*log(K!)/log(log(K!)) for K>=8",
        "factorial_scale_rows": rows,
        "aggregate": {
            "log_over_loglog_scale_twin_deserts_proved": True,
            "subscale_every_window_positivity_refuted": True,
            "dyadic_average_phase_lower_bound_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "These windows remain negligible compared with X and do not "
            "contradict a positive dyadic average or twin-prime infinitude. "
            "The result calibrates the forbidden local-window scale only."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_cofinal_countermodel_audit()
    collatz_compute = collatz_five_one_audit()
    goldbach_compute = goldbach_prime_gap_transfer_audit()
    twin_compute = twin_scaled_factorial_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-210",
            "theorem_name": "CofinalCentralNonvanishingExistenceAndSymmetricOffCriticalNoGo",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No effective zeta clearance or certified winding increment is obtained.",
            "route_decision": {
                "discard": "inferring RH from functional symmetry plus existential cofinal horizontal nonvanishing",
                "retain": "effective central-edge interval clearance coupled to argument-principle winding",
                "next_single_lemma": "EffectiveCofinalCentralEdgeClearanceAndWindingIncrementCertificate",
            },
            "proof_dag": proof_dag(
                "RH",
                "CompletedXiAbsoluteCofinalClearanceNoGoAndGammaNormalizedOuterEdgeReduction",
                "CofinalCentralNonvanishingExistenceAndSymmetricOffCriticalNoGo",
                "ExistentialCofinalHorizontalNonvanishingImpliesRH",
                "EffectiveCofinalCentralEdgeClearanceAndWindingIncrementCertificate",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof and no off-critical zeta zero. Existential cofinal central nonvanishing is proved but shown insufficient by an exact symmetric countermodel.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-210",
            "theorem_name": "FiveOneArbitraryRemainderAcceleratedCycleExclusion",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "Cycles with at least six ones and every nonperiodic divergent orbit remain open.",
            "route_decision": {
                "discard": "every accelerated cycle word with exactly five valuation-one entries",
                "retain": "a multiplicity-uniform obstruction plus an independent all-orbit descent theorem",
                "next_single_lemma": "ValuationOneMultiplicityUniformCycleObstruction",
            },
            "proof_dag": proof_dag(
                "CO",
                "FourOneAcceleratedCycleFiniteEnumerationExclusion",
                "FiveOneArbitraryRemainderAcceleratedCycleExclusion",
                "ExactlyFiveValuationOnesCanSupportAPositiveCycle",
                "ValuationOneMultiplicityUniformCycleObstruction",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof. The complete exactly-five-one periodic stratum, with arbitrary remaining valuations at least two, is excluded.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-210",
            "theorem_name": "PrimeGapToLeastGoldbachWitnessTransferAndDominanceNoGo",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "No exceptional-count upper bound or Goldbach counterexample is produced.",
            "route_decision": {
                "discard": "using the current published large-prime-gap lower bound alone to improve the TICKET-209 witness floor",
                "retain": "parity-breaking exceptional-tail control beyond the covering-congruence floor",
                "next_single_lemma": "GoldbachTailExceptionalCountBelowOneBeyondCoveringCongruenceFloor",
            },
            "proof_dag": proof_dag(
                "GB",
                "CoveringCongruenceSuperLogarithmicLeastWitnessLowerBound",
                "PrimeGapToLeastGoldbachWitnessTransferAndDominanceNoGo",
                "CurrentLargePrimeGapLowerBoundImprovesCoveringWitnessFloor",
                "GoldbachTailExceptionalCountBelowOneBeyondCoveringCongruenceFloor",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The prime-gap transfer is exact, but its current published asymptotic input is weaker than the TICKET-209 floor.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-210",
            "theorem_name": "LogOverLogLogScaleFactorialTwinDesertNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No averaged or selected dyadic phase lower bound is proved.",
            "route_decision": {
                "discard": "forcing a twin pair in every local window of length at most a fixed log X/log log X scale",
                "retain": "dyadic average positivity that explicitly permits calibrated local deserts",
                "next_single_lemma": "DyadicBilinearOmegaPhaseLowerBoundPermittingLogOverLogLogDeserts",
            },
            "proof_dag": proof_dag(
                "TP",
                "ArbitrarilyLongTwinFreeIntervalsAndLocalCyclotomicMarginNoGo",
                "LogOverLogLogScaleFactorialTwinDesertNoGo",
                "TwinPositivityInEveryLogOverLogLogLocalWindow",
                "DyadicBilinearOmegaPhaseLowerBoundPermittingLogOverLogLogDeserts",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. Factorial deserts are now calibrated at a fixed log X/log log X local scale.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureCofinalFiveOnePrimeGapScaledTwinAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-210 resolves none of the four conjectures. It proves "
            "existential cofinal zeta nonvanishing but refutes its sufficiency, "
            "excludes the full five-one Collatz cycle stratum, proves an exact "
            "prime-gap-to-Goldbach-witness transfer while diagnosing its "
            "current asymptotic ceiling, and calibrates factorial Twin deserts "
            "at the log X/log log X local scale."
        ),
        **sections,
        "cross_problem_synthesis": (
            "Each result separates existence from quantitative control: a "
            "zero-avoiding line lacks winding data, a finite cycle stratum "
            "lacks multiplicity-uniform descent, a lower-witness obstruction "
            "lacks tail exclusion, and long local deserts remain compatible "
            "with positive dyadic averages."
        ),
        "literature_boundary": {
            "riemann": "Isolated zeros of a nonzero entire function are classical; the symmetric polynomial is an exact no-go model, not a zeta model.",
            "collatz": "The finite exact stratum exclusion is project-local and requires independent specialist review before any novelty claim.",
            "goldbach": "The large-gap input is explicitly imported from Ford-Green-Konyagin-Maynard-Tao; only the elementary transfer and route comparison are proved here.",
            "twin_prime": "Factorial composite intervals are classical; the scale calibration is an elementary project deduction, not a bounded-gap improvement.",
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
                "bounded_result": {
                    "audit_ref": "#/cofinal_fiveone_primegap_scaledtwin_audit"
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
    integrated = ROOT / "data/open-problem/ticket210-cofinal-fiveone-primegap-scaledtwin.json"
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "cofinal_fiveone_primegap_scaledtwin_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-210-cofinal-countermodel.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-210-five-one-general.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-210-prime-gap-transfer.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-210-scaled-factorial-desert.json",
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
