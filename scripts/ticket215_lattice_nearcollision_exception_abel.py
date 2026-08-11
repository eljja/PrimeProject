from __future__ import annotations

import hashlib
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket214_cofinal_sevenone_exponential_cardinal import (
    goldbach_counts,
    prime_sieve,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket215-lattice-nearcollision-exception-abel.v1"
GENERATED_AT = "2026-08-13T01:00:00+09:00"
STATUS = "open_not_proven"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def even_lattice_candidates(lower: Fraction, upper: Fraction) -> list[int]:
    first = max(0, ceil_fraction(lower / 2))
    last = upper.numerator // (2 * upper.denominator)
    if first > last:
        return []
    return [2 * index for index in range(first, last + 1)]


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
            {"id": f"{prefix}-T214", "label": previous, "status": "closed"},
            {"id": f"{prefix}-T215", "label": closed, "status": "closed"},
            {
                "id": f"{prefix}-N215",
                "label": rejected,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN215",
                "label": open_lemma,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": target, "status": STATUS},
        ],
        "edges": [
            [f"{prefix}-T214", f"{prefix}-T215"],
            [f"{prefix}-T215", f"{prefix}-N215"],
            [f"{prefix}-T215", f"{prefix}-OPEN215"],
            [f"{prefix}-OPEN215", prefix],
        ],
    }


def riemann_even_lattice_audit() -> dict[str, Any]:
    fixtures = (
        (Fraction(-1, 2), Fraction(3, 2), [0]),
        (Fraction(3, 2), Fraction(5, 2), [2]),
        (Fraction(-1, 4), Fraction(9, 4), [0, 2]),
        (Fraction(7, 2), Fraction(9, 2), [4]),
    )
    rows = []
    failures = 0
    for lower, upper, expected in fixtures:
        candidates = even_lattice_candidates(lower, upper)
        row = {
            "lower": str(lower),
            "upper": str(upper),
            "width": str(upper - lower),
            "even_nonnegative_defect_candidates": candidates,
            "certifies_zero_defect": candidates == [0],
            "certifies_positive_defect": bool(candidates) and 0 not in candidates,
        }
        failures += int(candidates != expected)
        rows.append(row)

    persistent_pair_rows = []
    for line_multiplicity in (10**2, 10**4, 10**6, 10**8):
        total_multiplicity = line_multiplicity + 2
        persistent_pair_rows.append(
            {
                "critical_line_multiplicity_M": line_multiplicity,
                "total_multiplicity_N": total_multiplicity,
                "exact_defect_interval": [2, 2],
                "interval_width": 0,
                "relative_defect": str(Fraction(2, total_multiplicity)),
                "rectangle_RH": False,
            }
        )

    failures += int(not rows[0]["certifies_zero_defect"])
    failures += int(not rows[1]["certifies_positive_defect"])
    failures += int(any(row["interval_width"] != 0 for row in persistent_pair_rows))

    theorem = (
        "At every boundary-free height let D(T)=N(T)-M(T), so D(T) lies in "
        "the nonnegative even integers. If a certified interval I(T) contains "
        "D(T), then I(T) proves zero defect exactly when its intersection with "
        "2Z_{>=0} is {0}. In particular, a certified upper endpoint below two "
        "forces D(T)=0. Therefore such upper bounds on an unbounded sequence "
        "of heights imply the Riemann Hypothesis by TICKET-214. The constant "
        "two is sharp, and interval width alone is insufficient: a width-zero "
        "interval [2,2] can certify one persistent off-line symmetry pair."
    )
    proof = (
        "The symmetry identity from TICKET-213 places D on the lattice "
        "2Z_{>=0}. Intersecting a rigorous enclosure with that lattice gives "
        "the complete list of possible defects. An upper endpoint below two "
        "leaves only zero. Applying this at a cofinal sequence invokes the "
        "TICKET-214 monotonicity argument. Sharpness follows from the logical "
        "symmetric model with one off-line pair, for which D=2 at every later "
        "height even though the enclosure width is zero and D/N tends to zero."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "lattice_interval_rows": rows,
        "persistent_offline_pair_rows": persistent_pair_rows,
        "aggregate": {
            "strict_upper_endpoint_below_two_is_zero_defect_certificate": True,
            "cofinal_such_certificates_imply_RH": True,
            "interval_width_alone_sufficient": False,
            "threshold_two_is_sharp": True,
            "actual_zeta_cofinal_upper_bound_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The width-zero countermodel is not an off-line zero of the actual "
            "zeta function. It refutes precision-only promotion and leaves the "
            "one-sided actual-zeta estimate unproved."
        ),
        "failure_count": failures,
    }


def first_positive_single_mountain_m(k: int, seed: int = 1) -> int:
    m = max(1, seed)
    while 2 ** (k + 2 * m) <= 3 ** (k + m):
        m += 1
    return m


def collatz_single_mountain_audit(limit_k: int = 4096) -> dict[str, Any]:
    checkpoints = set(range(8, 17)) | {
        32,
        64,
        128,
        256,
        512,
        1024,
        2048,
        4096,
    }
    rows = []
    failures = 0
    near_collision_count = 0
    transcript = hashlib.sha256()
    m = 1
    for k in range(1, limit_k + 1):
        m = first_positive_single_mountain_m(k, m)
        delta = 2 ** (k + 2 * m) - 3 ** (k + m)
        divisor_ceiling = 3**k - 2**k
        previous_delta = 2 ** (k + 2 * (m - 1)) - 3 ** (k + m - 1)
        is_near_collision = delta <= divisor_ceiling
        near_collision_count += int(is_near_collision)
        failures += int(delta <= 0)
        failures += int(previous_delta > 0)
        transcript.update(
            f"{k}:{m}:{delta.bit_length()}:{divisor_ceiling.bit_length()}:"
            f"{int(is_near_collision)}\n".encode("ascii")
        )
        if k in checkpoints:
            rows.append(
                {
                    "valuation_one_count_k": k,
                    "unique_possible_m": m,
                    "delta_bit_length": delta.bit_length(),
                    "divisor_ceiling_bit_length": divisor_ceiling.bit_length(),
                    "near_collision_inequality_holds": is_near_collision,
                }
            )

    failures += int(near_collision_count != 0)
    theorem = (
        "Suppose a positive accelerated Collatz cycle has a cyclic valuation "
        "word 1^k 2^m with k,m>=1. Put Delta=2^(k+2m)-3^(k+m). Integer "
        "closure forces 0<Delta<=3^k-2^k. For each k at most one m can "
        "satisfy this inequality, namely the first m for which Delta is "
        "positive. An exact integer audit finds no such near-collision for "
        "1<=k<=4096, and therefore excludes every single-mountain word in "
        "that range."
    )
    proof = (
        "Iterating T_1(x)=(3x+1)/2 k times and T_2(x)=(3x+1)/4 m times "
        "gives Delta*x=C with C=Delta+2*3^m(3^k-2^k). Hence an integer x "
        "requires Delta to divide 2*3^m(3^k-2^k). Delta is odd and coprime "
        "to three, so Delta divides 3^k-2^k, proving the near-collision "
        "bound. Once Delta_m>0, Delta_(m+1)=3Delta_m+2^(k+2m)>3^k, so no "
        "later m can satisfy the bound. The finite audit uses exact powers "
        "and comparisons only."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "valuation_word_family": "cyclic rotations of 1^k 2^m",
        "near_collision_condition": "0<2^(k+2m)-3^(k+m)<=3^k-2^k",
        "audited_k_min": 1,
        "audited_k_max": limit_k,
        "near_collision_candidate_count": near_collision_count,
        "checkpoint_rows": rows,
        "transcript_sha256": transcript.hexdigest(),
        "aggregate": {
            "single_mountain_words_through_k_4096_excluded": True,
            "one_m_per_k_reduction_proved": True,
            "all_k_near_collision_exclusion_proved": False,
            "multi_run_cycle_words_excluded": False,
            "nonperiodic_divergence_excluded": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The exact diagonal audit is finite and the divisibility reduction "
            "covers only one contiguous run of one-valuations followed by one "
            "run of two-valuations. It does not cover multi-run words, entries "
            "above two, or nonperiodic trajectories."
        ),
        "failure_count": failures,
    }


def selector_sum(counts: list[int], q: Fraction) -> Fraction:
    return sum((q**count for count in counts), start=Fraction(0))


def goldbach_exception_selector_audit() -> dict[str, Any]:
    failures = 0
    synthetic_rows = []
    for counts in ([0, 3, 0, 2], [1, 1, 1, 1], [2, 7, 1, 3, 4]):
        boxes = len(counts)
        q = Fraction(1, boxes + 1)
        exception_count = counts.count(0)
        value = selector_sum(list(counts), q)
        remainder = value - exception_count
        row = {
            "counts": list(counts),
            "B": boxes,
            "q": str(q),
            "exact_selector_sum": str(value),
            "exception_count_Z": exception_count,
            "positive_tail": str(remainder),
            "universal_tail_upper_bound": str((boxes - exception_count) * q),
            "floor_selector_equals_Z": value.numerator // value.denominator
            == exception_count,
        }
        failures += int(not row["floor_selector_equals_Z"])
        synthetic_rows.append(row)

    sharp_rows = []
    for boxes in (2, 3, 8, 32):
        counts = [1] * boxes
        q = Fraction(1, boxes)
        value = selector_sum(counts, q)
        sharp_rows.append(
            {
                "B": boxes,
                "q": str(q),
                "all_positive_selector_sum": str(value),
                "exception_count_Z": 0,
                "subunit_test_fails_at_Bq_equals_one": value == 1,
            }
        )
        failures += int(value != 1)

    starts = (128, 512, 2048, 8192, 32768)
    flags = prime_sieve(2 * max(starts))
    primes = [value for value in range(2, len(flags)) if flags[value]]
    block_rows = []
    for start in starts:
        counts = goldbach_counts(start, flags, primes)
        boxes = len(counts)
        q = Fraction(1, boxes + 1)
        exceptions = counts.count(0)
        tail_upper = (boxes - exceptions) * q
        digest = hashlib.sha256(
            ",".join(str(value) for value in counts).encode("ascii")
        ).hexdigest()
        block_rows.append(
            {
                "dyadic_start_X": start,
                "even_targets_B": boxes,
                "minimum_representation_count": min(counts),
                "maximum_representation_count": max(counts),
                "exception_count_Z": exceptions,
                "q": str(q),
                "exact_tail_upper_bound": str(tail_upper),
                "floor_selector_exception_count": exceptions,
                "representation_vector_sha256": digest,
            }
        )
        failures += int(tail_upper >= 1)
        failures += int(exceptions != 0)

    theorem = (
        "For nonnegative integer Goldbach counts A_1,...,A_B and 0<q<1, "
        "let E(q)=sum q^(A_i) and let Z be the number of zero counts. Then "
        "Z<=E(q)<=Z+(B-Z)q. Consequently Bq<1 implies floor(E(q))=Z, so "
        "the exponential selector reconstructs the exact number of Goldbach "
        "exceptions in a finite block. The universal threshold is sharp: at "
        "Bq=1 the all-one vector has Z=0 but E=1."
    )
    proof = (
        "Every zero count contributes exactly one. Every positive integer "
        "count contributes at most q, which proves the two-sided bound. If "
        "Bq<1, the positive tail lies in [0,1), and taking the integer floor "
        "recovers Z. Conversely, choosing A_i=1 for every i gives E=Bq, so "
        "no q with Bq>=1 can make E<1 a universal coverage test. The prime "
        "audit computes each finite representation vector exactly; it does "
        "not provide an all-block arithmetic upper bound."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "selector": "E_B(q)=sum_i q^(A_i)",
        "exact_exception_formula": "Bq<1 implies floor(E_B(q))=Z_B",
        "synthetic_exception_rows": synthetic_rows,
        "sharp_temperature_rows": sharp_rows,
        "dyadic_goldbach_rows": block_rows,
        "aggregate": {
            "finite_block_exception_count_reconstruction_proved": True,
            "universal_temperature_threshold_sharp": True,
            "audited_exception_count": 0,
            "uniform_arithmetic_selector_bound_proved": False,
            "goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The floor identity is an exact re-encoding of unknown Goldbach "
            "counts. It does not estimate E(q) arithmetically on unseen blocks."
        ),
        "failure_count": failures,
    }


def twin_abel_boundary_audit() -> dict[str, Any]:
    getcontext().prec = 50
    limits = (100, 1000, 10_000, 100_000, 1_000_000)
    flags = prime_sieve(max(limits) + 2)
    twin_lower = [
        value
        for value in range(3, max(limits) + 1, 2)
        if flags[value] and flags[value + 2]
    ]
    rows = []
    failures = 0
    for limit in limits:
        lowers = [value for value in twin_lower if value <= limit]
        radius = Decimal(limit - 1) / Decimal(limit)
        weighted = sum((radius**value for value in lowers), start=Decimal(0))
        lower_factor = radius**limit
        count = len(lowers)
        lower_bound = lower_factor * count
        row = {
            "X": limit,
            "radius_r_X": f"{limit - 1}/{limit}",
            "twin_lower_endpoint_count_T_X": count,
            "scheduled_partial_Abel_sum_decimal": str(weighted),
            "exact_lower_factor": f"(({limit - 1})/{limit})^{limit}",
            "lower_factor_decimal": str(lower_factor),
            "lower_bound_decimal": str(lower_bound),
            "weighted_sum_between_lower_bound_and_count": (
                weighted + Decimal("1e-40") >= lower_bound
                and weighted <= Decimal(count)
            ),
        }
        failures += int(not row["weighted_sum_between_lower_bound_and_count"])
        rows.append(row)

    radii = (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(9, 10))
    epsilon = Fraction(1, 1000)
    maximum_radius = max(radii)
    start = 3
    while maximum_radius**start / (1 - maximum_radius**2) >= epsilon:
        start += 2
    indistinguishability_rows = []
    for radius in radii:
        tail_bound = radius**start / (1 - radius**2)
        indistinguishability_rows.append(
            {
                "radius": str(radius),
                "infinite_odd_tail_start_N": start,
                "exact_infinite_tail_bound": str(tail_bound),
                "below_epsilon": tail_bound < epsilon,
            }
        )
        failures += int(tail_bound >= epsilon)

    theorem = (
        "Let a_n be one when n and n+2 are prime and zero otherwise, and "
        "F(r)=sum_(odd n>=3) a_n r^n for 0<r<1. The Twin Prime Conjecture "
        "is equivalent to F(r) tending to infinity as r increases to one. "
        "However, every fixed-radius value is finite, and any finite set of "
        "radii bounded away from one cannot distinguish a finite sequence "
        "from an infinite odd-support extension: the extension can be placed "
        "far enough out to change every sampled value by less than epsilon."
    )
    proof = (
        "If there are finitely many twins, F has a finite limit at one. If "
        "there are infinitely many, then for every K the first K nonzero "
        "terms tend individually to one, so monotone convergence makes F "
        "unbounded. At a fixed r<1, F(r)<=r^3/(1-r^2). For finitely many "
        "sample radii let r_* be their maximum and append ones at every odd "
        "index N,N+2,...; its contribution is at most r_*^N/(1-r_*^2), "
        "which is below any prescribed epsilon for large odd N. This is a "
        "logical support countermodel, not a construction of prime pairs."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "Abel_transform": "F(r)=sum_(odd n>=3) 1_P(n)1_P(n+2) r^n",
        "finite_prime_rows": rows,
        "finite_radius_indistinguishability_rows": indistinguishability_rows,
        "epsilon": str(epsilon),
        "aggregate": {
            "boundary_divergence_equivalent_to_twin_infinitude": True,
            "fixed_radius_finiteness_informative": False,
            "finite_radius_samples_sufficient": False,
            "parity_breaking_boundary_lower_bound_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The infinite odd-support extension need not be prime-supported. "
            "It refutes finite-radius inference, not the Twin Prime Conjecture."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann_compute = riemann_even_lattice_audit()
    collatz_compute = collatz_single_mountain_audit()
    goldbach_compute = goldbach_exception_selector_audit()
    twin_compute = twin_abel_boundary_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-215",
            "theorem_name": "EvenLatticeOneSidedCofinalCertificationAndSharpTwoBarrier",
            "declared_proposition": riemann_compute["theorem"],
            "mathematical_argument": riemann_compute["proof"],
            "reproducible_computation": riemann_compute,
            "logical_limit": "No certified actual-zeta defect upper bound below two is proved on an unbounded height sequence.",
            "route_decision": {
                "discard": "interval precision or shrinking relative error without a one-sided defect upper endpoint below two",
                "retain": "cofinal certified actual-zeta defect enclosures whose upper endpoints are strictly below two",
                "next_single_lemma": "CofinalActualZetaDefectUpperBoundStrictlyBelowTwo",
            },
            "proof_dag": proof_dag(
                "RH",
                "CofinalExactDefectEquivalenceAndDensityOneNoGo",
                "EvenLatticeOneSidedCofinalCertificationAndSharpTwoBarrier",
                "WidthOnlyOrRelativeErrorDefectCertification",
                "CofinalActualZetaDefectUpperBoundStrictlyBelowTwo",
                "Riemann Hypothesis",
            ),
            "claim_boundary": "No RH proof and no off-line zeta zero. A sharp certification interface is proved; the required actual-zeta bound is open.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-215",
            "theorem_name": "SingleMountainCycleNearCollisionReductionAndFiniteDiagonalAudit",
            "declared_proposition": collatz_compute["theorem"],
            "mathematical_argument": collatz_compute["proof"],
            "reproducible_computation": collatz_compute,
            "logical_limit": "The near-collision is not excluded for every k, and multi-run words, valuations above two, and divergence remain open.",
            "route_decision": {
                "discard": "single-mountain valuation words with k through 4096 and finite diagonal testing as a complete Collatz proof",
                "retain": "an all-k Diophantine exclusion of the unique power near-collision diagonal, followed by a multi-run extension",
                "next_single_lemma": "NoSingleMountainPowerNearCollisionForAllK",
            },
            "proof_dag": proof_dag(
                "CO",
                "CompleteSevenValuationOneExclusionAndFiniteStratumNoGo",
                "SingleMountainCycleNearCollisionReductionAndFiniteDiagonalAudit",
                "FiniteSingleMountainDiagonalAuditProvesCollatz",
                "NoSingleMountainPowerNearCollisionForAllK",
                "Collatz Conjecture",
            ),
            "claim_boundary": "No Collatz proof or divergent orbit. One infinite word family is reduced to a one-dimensional exponential near-collision and checked only through k=4096.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-215",
            "theorem_name": "ExponentialSelectorExactExceptionCountAndSharpTemperature",
            "declared_proposition": goldbach_compute["theorem"],
            "mathematical_argument": goldbach_compute["proof"],
            "reproducible_computation": goldbach_compute,
            "logical_limit": "No target-uniform arithmetic estimate bounds the selector below one on every future block.",
            "route_decision": {
                "discard": "treating exact exception-count reconstruction or a non-sharp temperature as an independent Goldbach proof",
                "retain": "an arithmetic upper bound for the exact selector at a universally sharp scale Bq<1",
                "next_single_lemma": "ArithmeticExactExceptionSelectorBelowOneOnEveryDyadicBlock",
            },
            "proof_dag": proof_dag(
                "GB",
                "DyadicExponentialSelectorEquivalenceAndOccupancyNoGo",
                "ExponentialSelectorExactExceptionCountAndSharpTemperature",
                "ExactSelectorFloorIdentityAloneProvesCoverage",
                "ArithmeticExactExceptionSelectorBelowOneOnEveryDyadicBlock",
                "Strong Goldbach Conjecture",
            ),
            "claim_boundary": "No Goldbach proof or counterexample. The selector exactly counts finite exceptions, but its all-block arithmetic bound remains the conjectural content.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-215",
            "theorem_name": "CardinalSelectedAbelBoundaryEquivalenceAndFiniteRadiusNoGo",
            "declared_proposition": twin_compute["theorem"],
            "mathematical_argument": twin_compute["proof"],
            "reproducible_computation": twin_compute,
            "logical_limit": "No parity-breaking lower bound forces the exact gap-two Abel transform to diverge near radius one.",
            "route_decision": {
                "discard": "fixed-radius values or any finite radius sample as evidence sufficient for Twin Prime infinitude",
                "retain": "a uniform arithmetic lower bound diverging as the cardinal-selected Abel radius tends to one",
                "next_single_lemma": "ParityBreakingLowerBoundForCardinalSelectedAbelTransformNearOne",
            },
            "proof_dag": proof_dag(
                "TP",
                "CardinalSineExactGapTwoSelectorAndPositivityCircularity",
                "CardinalSelectedAbelBoundaryEquivalenceAndFiniteRadiusNoGo",
                "FiniteRadiusAbelEvidenceProvesTwinInfinitude",
                "ParityBreakingLowerBoundForCardinalSelectedAbelTransformNearOne",
                "Twin Prime Conjecture",
            ),
            "claim_boundary": "No Twin Prime proof or last-twin counterexample. Boundary divergence is an exact reformulation; finite-radius inference is refuted only by a logical support model.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "LatticeNearCollisionExceptionAbelAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-215 proves four exact partial, reduction, or no-go "
            "theorems and resolves none of the parent conjectures. It gives "
            "a sharp even-lattice RH certificate, reduces single-mountain "
            "Collatz cycles to one power near-collision per k, upgrades the "
            "Goldbach selector to exact exception counting, and moves exact "
            "twin selection to an Abel boundary-divergence target."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The next useful object is not another finite success row but a "
            "uniform one-sided estimate at the correct boundary: below two "
            "for RH defect, outside the Collatz power near-collision, below "
            "one for Goldbach exception mass, and divergent near one for the "
            "twin Abel transform."
        ),
        "literature_boundary": {
            "riemann": "Platt-Trudgian rigorously verify a finite height using interval arithmetic; TICKET-215 does not reproduce or extend that height.",
            "collatz": "Hercher's cycle lower bounds concern local minima and verified ranges; the single-mountain near-collision reduction here is narrower and carries no priority claim.",
            "goldbach": "The published verification through 4e18 is finite; the selector theorem is elementary and does not improve binary circle-method estimates.",
            "twin_prime": "Ford-Maynard explain the need for substantial Type II information in general prime-producing lower bounds; the Abel reformulation does not supply such information.",
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
                    "audit_ref": "#/lattice_nearcollision_exception_abel_audit"
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
    integrated = ROOT / "data/open-problem/ticket215-lattice-nearcollision-exception-abel.json"
    write_json(
        integrated,
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "lattice_nearcollision_exception_abel_audit": audit,
            "attempts": build_attempts(audit),
        },
    )
    targets = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-215-even-lattice-interval.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-215-single-mountain-near-collision.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-215-exact-exception-selector.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-215-abel-boundary.json",
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
