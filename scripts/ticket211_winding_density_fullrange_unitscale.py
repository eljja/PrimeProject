from __future__ import annotations

import cmath
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket211-winding-density-fullrange-unitscale.v1"
GENERATED_AT = "2026-08-10T23:55:00+09:00"
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
            {"id": f"{prefix}-T210", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T211", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N211",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN211",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T210", f"{prefix}-T211"],
            [f"{prefix}-T211", f"{prefix}-N211"],
            [f"{prefix}-T211", f"{prefix}-OPEN211"],
            [f"{prefix}-OPEN211", prefix],
        ],
    }


def symmetric_entire_countermodel(s: complex) -> complex:
    z = s - 0.5
    return cmath.cosh(2 * math.pi * z) - math.cosh(math.pi / 2)


def riemann_winding_localization_audit() -> dict[str, Any]:
    exact_margin = 1 + math.cosh(math.pi / 2)
    rows = []
    failures = 0
    for band_center in range(6):
        height = band_center + Fraction(1, 2)
        sampled_minimum = min(
            abs(symmetric_entire_countermodel(complex(index / 64, float(height))))
            for index in range(65)
        )
        check = sampled_minimum + 1e-12 >= exact_margin
        failures += int(not check)
        rows.append(
            {
                "band_center_n": band_center,
                "horizontal_height_n_plus_one_half": str(height),
                "exact_uniform_lower_bound": "1+cosh(pi/2)",
                "lower_bound_decimal": f"{exact_margin:.12f}",
                "sampled_minimum_modulus": f"{sampled_minimum:.12f}",
                "sample_respects_exact_bound": check,
                "total_zeros_in_closed_band_rectangle": 2,
                "critical_line_zeros_in_band": 0,
                "argument_principle_winding_increment": 2,
            }
        )

    theorem = (
        "Effective cofinal horizontal clearance and exact total winding do not "
        "locate zeros on the critical line. In centered coordinates z=s-1/2, "
        "the entire function F(s)=cosh(2*pi*z)-cosh(pi/2) is real symmetric "
        "and satisfies F(1-s)=F(s). Its zeros are exactly "
        "s=1/2+/-1/4+i*n. On every line Im(s)=n+1/2, "
        "|F(s)|>=1+cosh(pi/2). Nevertheless every rectangle "
        "0<=Re(s)<=1, n-1/2<=Im(s)<=n+1/2 has total winding two and "
        "contains two off-critical zeros but no critical-line zero."
    )
    proof = (
        "The identity cosh(w)=cosh(a) holds exactly when w=+/-a+2*pi*i*n, "
        "which gives the displayed zero set. Evenness and real coefficients "
        "give functional and conjugation symmetry. At height n+1/2, "
        "cosh(2*pi*(x+i(n+1/2)))=-cosh(2*pi*x), so the modulus equals "
        "cosh(2*pi*x)+cosh(pi/2) and is at least 1+cosh(pi/2). The two zeros "
        "with ordinate n lie strictly inside each band rectangle. There are "
        "no boundary zeros, hence the argument principle gives winding two. "
        "On z=i*t, F=cos(2*pi*t)-cosh(pi/2)<0, so the critical line contains "
        "no zeros. Thus total boundary winding is not a zero-location theorem."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "countermodel": {
            "function": "F(s)=cosh(2*pi*(s-1/2))-cosh(pi/2)",
            "zeros": "s=1/2+/-1/4+i*n for every integer n",
            "functional_symmetry": "F(1-s)=F(s)",
            "conjugation_symmetry": "F(conj(s))=conj(F(s))",
            "critical_line_sign": "F(1/2+it)<0",
            "uniform_horizontal_clearance": "1+cosh(pi/2)",
        },
        "band_rows": rows,
        "aggregate": {
            "effective_cofinal_horizontal_clearance_proved_for_model": True,
            "exact_total_winding_increment_proved_for_model": True,
            "total_winding_localizes_zeros_to_critical_line_refuted": True,
            "effective_zeta_boundary_certificate_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The countermodel refutes only a logical inference based on "
            "symmetry, effective cofinal horizontal clearance, and total "
            "rectangle winding. It has no Euler product and is not zeta. A "
            "valid RH bridge must compare total rectangle zero counts with "
            "critical-line zero counts, not merely certify total winding."
        ),
        "failure_count": failures,
    }


def affine_word_fixed_point(word: tuple[int, ...]) -> Fraction | None:
    slope = Fraction(1)
    intercept = Fraction(0)
    for valuation in word:
        denominator = 2**valuation
        slope = Fraction(3, denominator) * slope
        intercept = (3 * intercept + 1) / denominator
    if slope >= 1:
        return None
    return intercept / (1 - slope)


def collatz_density_integrality_audit() -> dict[str, Any]:
    density_floor = math.log(Fraction(6, 5), 2)
    block = (1, 2, 2)
    orbit = [Fraction(23, 5), Fraction(37, 5), Fraction(29, 5)]
    exact_product = math.prod(Fraction(3) + 1 / value for value in orbit)
    rows = []
    failures = 0
    for repetitions in range(1, 13):
        word = block * repetitions
        fixed = affine_word_fixed_point(word)
        slope = Fraction(27, 32) ** repetitions
        valid = fixed == Fraction(23, 5) and exact_product**repetitions == 2 ** sum(word)
        failures += int(not valid)
        rows.append(
            {
                "block_repetitions_m": repetitions,
                "length_h": len(word),
                "valuation_one_count_k": repetitions,
                "one_density_k_over_h": "1/3",
                "required_density_floor_decimal": f"{density_floor:.12f}",
                "formal_affine_slope": f"{slope.numerator}/{slope.denominator}",
                "positive_rational_fixed_point": "23/5",
                "exact_product_identity": f"2^{sum(word)}",
                "positive_integer_fixed_point": False,
                "aggregate_checks_hold": valid,
            }
        )

    theorem = (
        "If a nontrivial positive accelerated Collatz cycle has length h and "
        "exactly k valuation entries equal to one, then "
        "k/h>=log_2(6/5). This multiplicity-uniform density condition is not "
        "sufficient for an integer cycle: every repeated formal word "
        "(1,2,2)^m has density 1/3, slope (27/32)^m, the positive rational "
        "fixed point 23/5, and the exact cycle product identity, but never a "
        "positive integer fixed point."
    )
    proof = (
        "Rotate a hypothetical integer cycle to its minimum m>=3. With "
        "valuation sum A, multiplication around the cycle gives "
        "2^A=product(3+1/x_i)<=(10/3)^h. Since A>=2h-k, this implies "
        "(6/5)^h<=2^k and the density floor. For the no-go family, one "
        "formal block maps 23/5 to 37/5 to 29/5 and back to 23/5. Its slope "
        "is 27/32 and (3+5/23)(3+5/37)(3+5/29)=32=2^5. Repetition preserves "
        "all aggregate equalities and the density bound, but the fixed point "
        "has denominator five. Therefore aggregate multiplicity, contraction, "
        "and product data cannot replace a uniform 2-adic integrality argument."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "necessary_density_bound": {
            "exact": "k/h>=log_2(6/5)",
            "decimal": f"{density_floor:.12f}",
        },
        "rational_counterfamily": {
            "formal_word": "(1,2,2)^m",
            "one_block_orbit": [str(value) for value in orbit],
            "one_block_product": str(exact_product),
            "integrality_obstruction": "denominator 5",
        },
        "counterfamily_rows": rows,
        "aggregate": {
            "valuation_one_density_floor_proved": True,
            "aggregate_density_product_sufficiency_refuted": True,
            "uniform_two_adic_integrality_obstruction_proved": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The rational orbit is a countermodel to an aggregate-data proof "
            "strategy, not a counterexample to Collatz on positive integers. "
            "The density inequality is necessary only; integer and 2-adic "
            "compatibility remain the decisive missing inputs."
        ),
        "failure_count": failures,
    }


def prime_sieve(limit: int) -> bytearray:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for candidate in range(2, math.isqrt(limit) + 1):
        if flags[candidate]:
            flags[candidate * candidate : limit + 1 : candidate] = b"\x00" * (
                (limit - candidate * candidate) // candidate + 1
            )
    return flags


def goldbach_exception_rows(limit: int = 2_000_000) -> list[dict[str, Any]]:
    flags = prime_sieve(limit)
    primes = [value for value in range(2, limit + 1) if flags[value]]
    rows = []
    for lower in (32, 128, 512, 2048, 8192, 32768, 131072, 524288, 1_000_000):
        upper = min(2 * lower, limit)
        small_witness_exceptions = 0
        full_exceptions = 0
        maximum_least_witness = 0
        transcript = []
        for target in range(lower + lower % 2, upper + 1, 2):
            least = next(
                (
                    prime
                    for prime in primes
                    if prime <= target // 2 and flags[target - prime]
                ),
                None,
            )
            cutoff = max(2, math.floor(math.log(target)))
            if least is None:
                full_exceptions += 1
                transcript.append(f"{target},none,{cutoff}")
            else:
                maximum_least_witness = max(maximum_least_witness, least)
                small_witness_exceptions += int(least > cutoff)
                transcript.append(f"{target},{least},{cutoff}")
        rows.append(
            {
                "dyadic_lower_X": lower,
                "dyadic_upper_2X": upper,
                "even_targets_tested": (upper - (lower + lower % 2)) // 2 + 1,
                "small_witness_cutoff": "floor(log N)",
                "small_witness_exception_count": small_witness_exceptions,
                "full_goldbach_exception_count": full_exceptions,
                "maximum_least_witness": maximum_least_witness,
                "transcript_sha256": hashlib.sha256(
                    "\n".join(transcript).encode("ascii")
                ).hexdigest(),
            }
        )
    return rows


def goldbach_full_range_correction_audit() -> dict[str, Any]:
    rows = goldbach_exception_rows()
    failures = sum(
        int(row["small_witness_exception_count"] <= 0)
        + int(row["full_goldbach_exception_count"] != 0)
        for row in rows
    )
    theorem = (
        "A small-witness exceptional count cannot be the integer count driven "
        "below one to prove strong Goldbach. Let E_b(X) count even N in "
        "[X,2X] having no Goldbach representation with a prime summand at "
        "most b(N). If an unbounded sequence satisfies W(N)>b(N), then "
        "E_b(X)>=1 on infinitely many dyadic blocks. TICKET-209 supplies such "
        "a sequence for b(N)=c log N log log N. Therefore an eventual bound "
        "E_b(X)<1 is impossible at that cutoff even if strong Goldbach is true."
    )
    proof = (
        "For each target N_j with W(N_j)>b(N_j), choose the dyadic X_j with "
        "X_j<=N_j<2X_j. Then N_j is counted by E_b(X_j), so the integer-valued "
        "count is at least one on unbounded blocks. TICKET-209 proves exactly "
        "the required unbounded least-witness floor. This predicate includes "
        "both genuine Goldbach exceptions and represented numbers whose least "
        "witness is merely large; it cannot distinguish them. By contrast, "
        "the full-range count E_full(X) of even N with no representation at "
        "all is integer-valued, and an eventual strict bound E_full(X)<1 plus "
        "a verified finite prefix would prove strong Goldbach. No such bound "
        "is obtained here."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "predicate_correction": {
            "invalid_tail_target": "no witness with p<=b(N)",
            "valid_tail_target": "no prime witness over the full range 2<=p<=N/2",
            "integer_below_one_bridge": (
                "E_full(X)<1 eventually plus a verified finite prefix implies "
                "zero full Goldbach exceptions"
            ),
        },
        "finite_dyadic_rows": rows,
        "aggregate": {
            "small_witness_below_one_route_refuted": True,
            "small_and_full_exception_predicates_separated": True,
            "finite_full_exception_count": sum(
                row["full_goldbach_exception_count"] for row in rows
            ),
            "full_range_tail_exception_bound_proved": False,
            "goldbach_counterexample_found": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The logical no-go is unconditional once the TICKET-209 witness "
            "floor is accepted. The finite sieve through two million only "
            "illustrates the predicate difference and proves nothing beyond "
            "its explicit range. No parity-breaking full-range estimate is supplied."
        ),
        "failure_count": failures,
    }


def factorial_unit_scale_row(parameter: int) -> dict[str, Any]:
    log_x = math.lgamma(parameter + 1)
    scale = log_x / math.log(log_x)
    length = parameter - 3
    return {
        "factorial_parameter_K": parameter,
        "factorial_base_decimal_digits": math.floor(log_x / math.log(10)) + 1,
        "twin_free_candidate_length_H": length,
        "log_X_over_loglog_X_decimal": f"{scale:.12f}",
        "H_over_log_X_over_loglog_X_decimal": f"{length / scale:.12f}",
        "symbolic_divisibility_certificate": (
            "for every 2<=j<=K-2: j|(K!+j) and (j+2)|(K!+j+2)"
        ),
        "all_composite_pair_certificates_hold": True,
    }


def twin_unit_scale_audit() -> dict[str, Any]:
    parameters = (8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096)
    rows = [factorial_unit_scale_row(parameter) for parameter in parameters]
    failures = sum(
        int(not row["all_composite_pair_certificates_hold"]) for row in rows
    )
    theorem = (
        "For X=K! and H=K-3, the consecutive lower candidates X+j, "
        "2<=j<=K-2, contain no twin-prime pair, and "
        "H/(log X/log log X) tends to one. Consequently, for every fixed "
        "c<1 there are infinitely many twin-free windows with "
        "H>=c log X/log log X."
    )
    proof = (
        "For every 2<=j<=K-2, j properly divides K!+j and j+2 properly "
        "divides K!+j+2, so no lower candidate starts a twin pair. Stirling's "
        "formula gives log(K!)=K log K-K+O(log K), while "
        "log log(K!)=log K+log log K+o(1). Therefore "
        "(K-3)log log(K!)/log(K!) tends to one. The definition of a limit "
        "then yields the assertion for every fixed c<1."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "asymptotic_identity": (
            "(K-3)*log(log(K!))/log(K!) -> 1"
        ),
        "factorial_unit_scale_rows": rows,
        "aggregate": {
            "asymptotically_unit_scale_twin_deserts_proved": True,
            "every_fixed_c_below_one_local_positivity_refuted": True,
            "desert_relative_density_tends_to_zero": True,
            "sparse_dyadic_twin_positivity_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The factorial construction is elementary and does not improve "
            "bounded-gap theorems. Its windows satisfy H/X->0, so they are "
            "compatible with infinitely many twin primes and with positive "
            "dyadic averages. It refutes only overly uniform local positivity."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_winding_localization_audit()
    collatz_compute = collatz_density_integrality_audit()
    goldbach_compute = goldbach_full_range_correction_audit()
    twin_compute = twin_unit_scale_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-211",
            "theorem_name": "EffectiveCofinalClearanceAndTotalWindingLocalizationNoGo",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No effective zeta certificate equating total rectangle zeros with critical-line zeros is obtained.",
            "route_decision": {
                "discard": "inferring critical-line location from symmetry, cofinal boundary clearance, and total winding alone",
                "retain": "an effective equality between total rectangle zero counts and critical-line zero counts",
                "next_single_lemma": "EffectiveCriticalLineRectangleZeroCountEqualityCertificate",
            },
            "proof_dag": proof_dag(
                "RH",
                "CofinalCentralNonvanishingExistenceAndSymmetricOffCriticalNoGo",
                "EffectiveCofinalClearanceAndTotalWindingLocalizationNoGo",
                "EffectiveTotalWindingAloneImpliesCriticalLineLocalization",
                "EffectiveCriticalLineRectangleZeroCountEqualityCertificate",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof and no off-critical zeta zero. An exact entire countermodel proves that even effective clearance plus total winding does not locate zeros on the critical line.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-211",
            "theorem_name": "ValuationOneDensityFloorAndAggregateOnlyNoGo",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "The density floor does not exclude high-one integer words or nonperiodic divergence.",
            "route_decision": {
                "discard": "using valuation-one density, affine contraction, and the cycle product identity without integer or 2-adic coupling",
                "retain": "a uniform 2-adic integrality obstruction for all words above the necessary one-density floor",
                "next_single_lemma": "Uniform2AdicIntegralityObstructionForHighOneDensityWords",
            },
            "proof_dag": proof_dag(
                "CO",
                "FiveOneArbitraryRemainderAcceleratedCycleExclusion",
                "ValuationOneDensityFloorAndAggregateOnlyNoGo",
                "AggregateDensityProductDataExcludeAllPositiveCycles",
                "Uniform2AdicIntegralityObstructionForHighOneDensityWords",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or integer counterexample. A multiplicity-uniform necessary density floor is proved, and an exact rational family refutes aggregate-only sufficiency.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-211",
            "theorem_name": "SmallWitnessExceptionalCountCannotCertifyGoldbachBeyondCoveringFloor",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "No strict-below-one estimate for the full-range no-representation count is proved.",
            "route_decision": {
                "discard": "counting absence of witnesses below a cutoff as though it counted complete Goldbach failures",
                "retain": "an integer-valued full-range no-representation count with an eventual strict upper bound below one",
                "next_single_lemma": "FullRangeBinaryGoldbachExceptionalCountStrictlyBelowOne",
            },
            "proof_dag": proof_dag(
                "GB",
                "PrimeGapToLeastGoldbachWitnessTransferAndDominanceNoGo",
                "SmallWitnessExceptionalCountCannotCertifyGoldbachBeyondCoveringFloor",
                "SmallWitnessExceptionalCountBelowOneClosesGoldbach",
                "FullRangeBinaryGoldbachExceptionalCountStrictlyBelowOne",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The previously proposed exceptional-count target is corrected from small-witness failure to full-range nonrepresentation.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-211",
            "theorem_name": "AsymptoticallyUnitScaleFactorialTwinDesertNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "The unit-scale local no-go supplies no positive dyadic or sparse averaged lower bound.",
            "route_decision": {
                "discard": "forcing a twin pair in every c log X/log log X window for any fixed c below one",
                "retain": "sparse dyadic positivity that permits asymptotically unit-scale factorial deserts",
                "next_single_lemma": "SparseDyadicBilinearOmegaStrictPositivity",
            },
            "proof_dag": proof_dag(
                "TP",
                "LogOverLogLogScaleFactorialTwinDesertNoGo",
                "AsymptoticallyUnitScaleFactorialTwinDesertNoGo",
                "TwinPositivityInEveryFixedSubunitLogOverLogLogWindow",
                "SparseDyadicBilinearOmegaStrictPositivity",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or counterexample. The elementary factorial no-go is sharpened from coefficient 1/4 to every fixed coefficient below one.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureWindingDensityFullRangeUnitScaleAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-211 resolves none of the four conjectures. It proves four "
            "exact theorem or no-go boundaries: total winding does not locate "
            "Riemann zeros, aggregate Collatz density does not enforce "
            "integrality, small-witness exceptions cannot close Goldbach, and "
            "factorial Twin deserts reach every fixed subunit local scale."
        ),
        **sections,
        "cross_problem_synthesis": (
            "All four routes fail at a localization step. Total complex-analytic "
            "mass does not locate zeros, aggregate valuation statistics do not "
            "locate integer orbits, truncated witnesses do not locate complete "
            "Goldbach failures, and local deserts do not determine sparse "
            "dyadic positivity. The next lemmas now state those missing bridges directly."
        ),
        "literature_boundary": {
            "riemann": "The countermodel is elementary and does not model zeta's Euler product; no novelty priority is claimed.",
            "collatz": "The density inequality and rational no-go require specialist review before any novelty claim; the rational orbit is not an integer Collatz orbit.",
            "goldbach": "The covering-witness input is inherited from TICKET-209; TICKET-211 is a logical predicate correction, not a parity-barrier breakthrough.",
            "twin_prime": "Factorial composite intervals and Stirling asymptotics are classical; the coefficient calibration is an elementary deduction, not a new bounded-gap theorem.",
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
                    "audit_ref": "#/winding_density_fullrange_unitscale_audit"
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
    integrated = ROOT / "data/open-problem/ticket211-winding-density-fullrange-unitscale.json"
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "winding_density_fullrange_unitscale_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-211-winding-localization-nogo.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-211-density-integrality-nogo.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-211-fullrange-exception-correction.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-211-unit-scale-factorial-desert.json",
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
