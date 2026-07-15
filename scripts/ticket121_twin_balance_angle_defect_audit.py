from __future__ import annotations

import math
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket120_twin_low_divisor_pair_savings_audit import _source_rows


GENERATED_AT = "2026-07-15T23:55:00+09:00"
SCHEMA = "primeproject.ticket121-twin-balance-angle-defect-audit.v1"
TOLERANCE = 1e-7
BALANCE_THRESHOLD = 1.0 / 8.0
ANGLE_GAP_THRESHOLD = 1.0 / 2.0
MASS_THRESHOLD = 1.0 / 2.0
CERTIFIED_FRACTION = (
    BALANCE_THRESHOLD * ANGLE_GAP_THRESHOLD * MASS_THRESHOLD
)


def balance_angle_row(
    gram_left: float,
    gram_cross: float,
    gram_right: float,
    geometry_norm: float,
) -> dict[str, float | bool | None]:
    left_norm = math.sqrt(max(gram_left, 0.0))
    right_norm = math.sqrt(max(gram_right, 0.0))
    norm_sum = left_norm + right_norm
    pair_energy = gram_left + gram_right + 2.0 * gram_cross
    if pair_energy < -TOLERANCE:
        raise ValueError("pair Gram energy is negative beyond tolerance")
    pair_norm = math.sqrt(max(pair_energy, 0.0))
    singleton = geometry_norm * norm_sum
    paired = geometry_norm * pair_norm
    actual_saving = singleton - paired
    norm_product = left_norm * right_norm
    gram_defect = norm_product - gram_cross
    cosine = gram_cross / norm_product if norm_product > 0 else None
    balance = norm_product / norm_sum**2 if norm_sum > 0 else 0.0
    angle_gap = 1.0 - cosine if cosine is not None else 0.0
    normalized_defect = balance * angle_gap
    rationalized_saving = (
        2.0 * geometry_norm * gram_defect / (norm_sum + pair_norm)
        if norm_sum + pair_norm > 0
        else 0.0
    )
    lower_certificate = (
        geometry_norm * gram_defect / norm_sum if norm_sum > 0 else 0.0
    )
    upper_certificate = 2.0 * lower_certificate
    qualifies = bool(
        singleton > 0
        and balance + TOLERANCE >= BALANCE_THRESHOLD
        and angle_gap + TOLERANCE >= ANGLE_GAP_THRESHOLD
    )
    return {
        "left_norm": left_norm,
        "right_norm": right_norm,
        "pair_norm": pair_norm,
        "geometry_norm": geometry_norm,
        "singleton_centered": singleton,
        "paired_centered": paired,
        "actual_centered_saving": actual_saving,
        "gram_cross": gram_cross,
        "gram_defect": gram_defect,
        "centered_cosine": cosine,
        "norm_balance": balance,
        "angle_gap": angle_gap,
        "normalized_balance_angle_defect": normalized_defect,
        "rationalized_saving": rationalized_saving,
        "quadratic_lower_certificate": lower_certificate,
        "quadratic_upper_certificate": upper_certificate,
        "rationalization_error": abs(actual_saving - rationalized_saving),
        "lower_bound_violation": lower_certificate - actual_saving,
        "upper_bound_violation": actual_saving - upper_certificate,
        "qualifies_balanced_decorrelated_mass": qualifies,
    }


def audit_scale(source: dict[str, Any]) -> dict[str, Any]:
    row = source["row"]
    blocks = row["dyadic_block_profile"]
    denominator_rows: list[dict[str, Any]] = []
    for profile in row["dyadic_denominator_profile"]:
        gram = profile["real_gram_matrix"]
        result = balance_angle_row(
            float(gram[0][0]),
            float(gram[0][1]),
            float(gram[1][1]),
            float(profile["projected_phase_l2_norm"]),
        )
        denominator_rows.append(
            {
                "right_denominator": int(profile["right_denominator"]),
                **result,
            }
        )

    total_singleton = sum(
        float(item["singleton_centered"]) for item in denominator_rows
    )
    total_paired = sum(
        float(item["paired_centered"]) for item in denominator_rows
    )
    actual_saving = sum(
        float(item["actual_centered_saving"]) for item in denominator_rows
    )
    rationalized_saving = sum(
        float(item["rationalized_saving"]) for item in denominator_rows
    )
    lower_certificate = sum(
        float(item["quadratic_lower_certificate"])
        for item in denominator_rows
    )
    upper_certificate = sum(
        float(item["quadratic_upper_certificate"])
        for item in denominator_rows
    )
    active = [
        item for item in denominator_rows if item["singleton_centered"] > 0
    ]
    qualifying = [
        item
        for item in active
        if item["qualifies_balanced_decorrelated_mass"]
    ]

    def weighted_average(field: str) -> float:
        if total_singleton <= 0:
            return 0.0
        return sum(
            float(item["singleton_centered"]) * float(item[field])
            for item in active
        ) / total_singleton

    weighted_balance = weighted_average("norm_balance")
    weighted_angle_gap = weighted_average("angle_gap")
    weighted_product = weighted_average(
        "normalized_balance_angle_defect"
    )
    qualifying_mass = sum(
        float(item["singleton_centered"]) for item in qualifying
    )
    qualifying_certificate = sum(
        float(item["quadratic_lower_certificate"])
        for item in qualifying
    )
    return {
        "horizon": int(row["horizon"]),
        "selection_status": source["selection_status"],
        "first_block": str(blocks[0]["label"]),
        "second_block": str(blocks[1]["label"]),
        "actual_lower": int(blocks[0]["actual_lower"]),
        "actual_upper": int(blocks[1]["actual_upper"]),
        "centered_singleton": total_singleton,
        "centered_paired": total_paired,
        "actual_centered_saving": actual_saving,
        "rationalized_centered_saving": rationalized_saving,
        "quadratic_lower_certificate": lower_certificate,
        "quadratic_upper_certificate": upper_certificate,
        "actual_centered_saving_fraction": (
            actual_saving / total_singleton if total_singleton else 0.0
        ),
        "certified_lower_fraction": (
            lower_certificate / total_singleton if total_singleton else 0.0
        ),
        "certificate_to_actual_ratio": (
            lower_certificate / actual_saving if actual_saving else 0.0
        ),
        "weighted_norm_balance": weighted_balance,
        "weighted_angle_gap": weighted_angle_gap,
        "weighted_balance_angle_defect": weighted_product,
        "balance_angle_covariance": (
            weighted_product - weighted_balance * weighted_angle_gap
        ),
        "qualifying_denominator_count": len(qualifying),
        "active_denominator_count": len(active),
        "qualifying_mass_fraction": (
            qualifying_mass / total_singleton if total_singleton else 0.0
        ),
        "qualifying_certificate_fraction": (
            qualifying_certificate / total_singleton
            if total_singleton
            else 0.0
        ),
        "maximum_rationalization_error": max(
            float(item["rationalization_error"])
            for item in denominator_rows
        ),
        "maximum_lower_bound_violation": max(
            float(item["lower_bound_violation"])
            for item in denominator_rows
        ),
        "maximum_upper_bound_violation": max(
            float(item["upper_bound_violation"])
            for item in denominator_rows
        ),
        "minimum_gram_defect": min(
            float(item["gram_defect"]) for item in denominator_rows
        ),
        "denominator_profile": denominator_rows,
    }


def abstract_countermodels() -> dict[str, Any]:
    anti_aligned_imbalance = []
    for epsilon in (1.0, 0.1, 0.01, 0.001, 0.000001):
        balance = epsilon / (1.0 + epsilon) ** 2
        anti_aligned_imbalance.append(
            {
                "epsilon": epsilon,
                "norm_balance": balance,
                "cosine": -1.0,
                "angle_gap": 2.0,
                "normalized_defect": 2.0 * balance,
                "actual_centered_saving_fraction": (
                    2.0 * epsilon / (1.0 + epsilon)
                ),
            }
        )
    balanced_near_alignment = []
    for theta in (1.0, 0.1, 0.01, 0.001, 0.000001):
        cosine = math.cos(theta)
        balanced_near_alignment.append(
            {
                "theta": theta,
                "norm_balance": 0.25,
                "cosine": cosine,
                "angle_gap": 1.0 - cosine,
                "normalized_defect": 0.25 * (1.0 - cosine),
                "actual_centered_saving_fraction": (
                    1.0 - math.cos(theta / 2.0)
                ),
            }
        )
    return {
        "anti_aligned_norm_imbalance": {
            "purpose": "refutes every fixed saving fraction derived from a cosine gap alone: the angle gap stays maximal while one adjacent-shell norm vanishes",
            "sequence": anti_aligned_imbalance,
        },
        "balanced_near_alignment": {
            "purpose": "refutes every fixed saving fraction derived from norm balance alone: balance stays maximal while the vectors align",
            "sequence": balanced_near_alignment,
        },
    }


def full_budget_bridge(scale_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scale_map = {int(row["horizon"]): row for row in scale_rows}
    sources = (
        (
            8_388_608,
            "TICKET-118",
            "data/open-problem/ticket118-twin-canonical-adjacent-pair-holdout.json",
            "twin_canonical_adjacent_pair_holdout",
        ),
        (
            16_777_216,
            "TICKET-119",
            "data/open-problem/ticket119-twin-canonical-pair-doubling-holdout.json",
            "twin_canonical_pair_doubling_holdout",
        ),
    )
    output = []
    for horizon, ticket_id, path, key in sources:
        audit = read_json(ROOT / path)[key]
        canonical = audit["canonical_partition"]
        row = audit["holdout_row"]
        low = scale_map[horizon]
        first_group = canonical["groups"][0]
        other_budget = (
            float(canonical["numerator_budget"])
            - float(first_group["numerator_budget"])
        )
        boundary = (
            float(row["boundary_phase_lipschitz_envelope"])
            + float(row["variation_absolute_envelope"])
        )
        singleton_mean = sum(
            abs(float(profile["block_mean_signed_contributions"][0]))
            + abs(float(profile["block_mean_signed_contributions"][1]))
            for profile in row["dyadic_denominator_profile"]
        )
        centered_singleton = float(low["centered_singleton"])
        known = float(row["known_without_type_ii_minor"])
        eta_numerator = (
            singleton_mean
            + centered_singleton
            + other_budget
            + boundary
            - known
        )
        eta_required = max(0.0, eta_numerator / centered_singleton)
        candidate_adverse = (
            singleton_mean
            + (1.0 - CERTIFIED_FRACTION) * centered_singleton
            + other_budget
            + boundary
        )
        output.append(
            {
                "horizon": horizon,
                "source_ticket": ticket_id,
                "known_without_type_ii_minor": known,
                "other_canonical_group_budget": other_budget,
                "boundary_and_variation_budget": boundary,
                "low_pair_singleton_mean": singleton_mean,
                "low_pair_centered_singleton": centered_singleton,
                "eta_required_with_other_finite_budgets_frozen": (
                    eta_required
                ),
                "candidate_eta": CERTIFIED_FRACTION,
                "candidate_finite_lower_bound": known - candidate_adverse,
                "candidate_closes_finite": bool(known > candidate_adverse),
                "interpretation": "This freezes every non-low-pair finite budget. It is a bridge-strength diagnostic, not an asymptotic theorem.",
            }
        )
    return output


def preserved_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    target: str,
) -> dict[str, Any]:
    prior = next(
        attempt
        for attempt in source["attempts"]
        if attempt["problem_id"] == problem_id
    )
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve the independent target during the Twin balance-angle correction",
        "attempt": "No Twin low-divisor balance-angle result is transferred to this problem.",
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "independent_target": target,
        },
        "obstruction": "TICKET121 supplies no new problem-specific infinite theorem here.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    scale_rows = [audit_scale(source) for source in _source_rows()]
    countermodels = abstract_countermodels()
    bridge = full_budget_bridge(scale_rows)
    machine = {
        "scale_count": len(scale_rows),
        "denominator_row_count": sum(
            len(row["denominator_profile"]) for row in scale_rows
        ),
        "active_denominator_row_count": sum(
            int(row["active_denominator_count"]) for row in scale_rows
        ),
        "minimum_qualifying_mass_fraction": min(
            float(row["qualifying_mass_fraction"]) for row in scale_rows
        ),
        "minimum_certified_lower_fraction": min(
            float(row["certified_lower_fraction"]) for row in scale_rows
        ),
        "maximum_rationalization_error": max(
            float(row["maximum_rationalization_error"])
            for row in scale_rows
        ),
        "maximum_lower_bound_violation": max(
            float(row["maximum_lower_bound_violation"])
            for row in scale_rows
        ),
        "maximum_upper_bound_violation": max(
            float(row["maximum_upper_bound_violation"])
            for row in scale_rows
        ),
        "minimum_gram_defect": min(
            float(row["minimum_gram_defect"]) for row in scale_rows
        ),
        "angle_only_countermodel_terminal_saving_fraction": (
            countermodels["anti_aligned_norm_imbalance"]["sequence"][-1][
                "actual_centered_saving_fraction"
            ]
        ),
        "balance_only_countermodel_terminal_saving_fraction": (
            countermodels["balanced_near_alignment"]["sequence"][-1][
                "actual_centered_saving_fraction"
            ]
        ),
        "candidate_bridge_finite_closure_count": sum(
            int(item["candidate_closes_finite"]) for item in bridge
        ),
        "total_failure_count": 0,
    }
    machine["total_failure_count"] += int(
        machine["maximum_rationalization_error"] > TOLERANCE
    )
    machine["total_failure_count"] += int(
        machine["maximum_lower_bound_violation"] > TOLERANCE
    )
    machine["total_failure_count"] += int(
        machine["maximum_upper_bound_violation"] > TOLERANCE
    )
    machine["total_failure_count"] += int(
        machine["minimum_gram_defect"] < -TOLERANCE
    )
    machine["total_failure_count"] += int(
        machine["minimum_qualifying_mass_fraction"] < MASS_THRESHOLD
    )

    audit = {
        "theorem_name": "LowDivisorBalanceAngleRationalizationAndSingleFactorNoGo",
        "source_ticket": "TICKET-120",
        "exact_rationalization": {
            "notation": "a=||z0||, b=||z1||, c=Re<z0,z1>, p=||z0+z1||, w>=0",
            "identity": "w(a+b-p)=2w(ab-c)/(a+b+p)",
            "quadratic_sandwich": "w(ab-c)/(a+b) <= w(a+b-p) <= 2w(ab-c)/(a+b)",
            "normalized_defect": "b_q(1-kappa_q)=(ab/(a+b)^2)(1-c/(ab))=(ab-c)/(a+b)^2",
            "denominator_sum": "actual centered saving fraction is at least the singleton-weighted mean of b_q(1-kappa_q)",
        },
        "balanced_decorrelated_mass_certificate": {
            "balance_threshold": BALANCE_THRESHOLD,
            "angle_gap_threshold": ANGLE_GAP_THRESHOLD,
            "mass_threshold": MASS_THRESHOLD,
            "conclusion": "If at least half of centered singleton mass has b_q>=1/8 and 1-kappa_q>=1/2, then the centered pair saving fraction is at least 1/32.",
            "certified_fraction": CERTIFIED_FRACTION,
            "selection_boundary": "The implication is universal, but the displayed rational thresholds were chosen during TICKET121 as an interpretable exploratory audit and were not preregistered or tested on a new holdout.",
            "scope": "universal sufficient condition for the first-pair centered envelope; the eight-row threshold pass is exploratory and it does not control other canonical groups, boundary, variation, or the comparison main term",
        },
        "scale_rows": scale_rows,
        "abstract_countermodels": countermodels,
        "discarded_candidates": [
            {
                "name": "FixedSavingFromDenominatorSummedCosineGapAlone",
                "reason": "Maximal anti-alignment with norm ratio epsilon has angle gap 2 but saving fraction 2epsilon/(1+epsilon), which tends to zero.",
            },
            {
                "name": "FixedSavingFromAdjacentShellNormBalanceAlone",
                "reason": "Equal norms have maximal balance 1/4, but near-aligned vectors have saving fraction tending to zero.",
            },
            {
                "name": "PositiveLowPairConstantAloneClosesEveryFiniteScale",
                "reason": "The natural 1/32 certificate closes the frozen 16M budget but not the frozen 8M budget; full closure also needs eventual control of the remaining groups and boundary terms.",
            },
        ],
        "retained_theorem": {
            "name": "VaughanLowDivisorWeightedBalanceAngleDefectGap",
            "statement": "Prove fixed beta,gamma,rho>0 and X0 such that for every X>=X0, at least rho of the first canonical pair centered singleton mass lies on Farey denominators with norm balance at least beta and cosine at most 1-gamma.",
            "consequence": "The first-pair centered saving fraction is at least rho*beta*gamma. This must be combined with an eventually subcritical estimate for all remaining canonical groups and boundary terms.",
            "arithmetic_expansion": "For each q, c_q is the signed double sum over d in B0 and e in B1 of mu(d)mu(e) times the centered Farey endpoint kernel inner product. The missing step is a fixed-shift arithmetic decorrelation theorem for that realizable kernel, not a generic Hilbert-space inequality.",
            "counterexample_route": "Construct an unbounded Vaughan-realizable scale sequence on which balanced-decorrelated denominator mass tends to zero, or on which the remaining canonical budget defeats every resulting fixed margin.",
        },
        "full_budget_bridge": bridge,
        "literature_boundary": [
            {
                "citation": "Lichtman, Averages of the Mobius function on shifted primes",
                "url": "https://arxiv.org/abs/2009.08969",
                "role": "Cancellation is proved after averaging over sufficiently many shifts, not for the fixed shift-two denominator kernel required here.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Type I/II information must be used jointly and admits extremal comparison sequences; weak information contracts require explicit no-go models.",
            },
            {
                "citation": "Maynard, Primes in arithmetic progressions to large moduli II",
                "url": "https://arxiv.org/abs/2006.07088",
                "role": "Strong distribution estimates use suitably well-factorable weights; PrimeProject has not proved that its adjacent-shell endpoint kernel has the required factorability.",
            },
        ],
        "machine_audit": machine,
        "proof_boundary": "TICKET121 proves an elementary rationalization and two exact abstract no-go families, then records finite balance-angle diagnostics. It proves no conjecture and certifies no conjecture counterexample.",
    }

    source = read_json(
        ROOT
        / "data/open-problem/ticket120-twin-low-divisor-pair-savings-audit.json"
    )
    attempts = [
        preserved_attempt(
            source,
            "riemann",
            "RH-TICKET-121",
            "NonCircularKernelPositivityPreserved",
            "NonCircularExplicitFormulaKernelPositivity",
        ),
        preserved_attempt(
            source,
            "collatz",
            "CO-TICKET-121",
            "GoldenMeanEscapePreserved",
            "GoldenMeanInvariantSetEscape",
        ),
        preserved_attempt(
            source,
            "goldbach",
            "GB-TICKET-121",
            "JointBalancedGoldbachPreserved",
            "JointBalancedVaughanGoldbachResidualEnvelope",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-121",
            "status": "balance_angle_identity_proved_single_factor_routes_refuted_open",
            "route": "LowDivisorWeightedBalanceAngleDefect",
            "proof_or_counterexample_mode": "exact rationalization, abstract no-go families, and finite bridge-strength audit",
            "attempt": "Replace the underspecified angle-gap target by a product of norm balance, angular decorrelation, and denominator mass, then test the exact sufficient condition and its failure modes.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-120",
                "audit_ref": "twin_low_divisor_balance_angle_audit",
            },
            "obstruction": "Neither angle gap nor norm balance alone yields a fixed saving. The corrected product condition is only finite evidence until proved for the actual Vaughan kernel on all sufficiently large scales and combined with the remaining budgets.",
            "candidate_theorem": "VaughanLowDivisorWeightedBalanceAngleDefectGap",
            "next_experiment": "Expand the cross Gram as a signed outer-divisor kernel and prove balanced-decorrelated mass on a result-independent denominator set, or construct a Vaughan-realizable escaping sequence.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    write_json(
        ROOT
        / "data/open-problem/ticket121-twin-balance-angle-defect-audit.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": "exact_balance_angle_identity_and_single_factor_nogos_open",
            "claim_boundary": audit["proof_boundary"],
            "twin_low_divisor_balance_angle_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-121-kernel-positivity-preserved.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-121-golden-mean-preserved.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-121-joint-balanced-preserved.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-121-balance-angle-defect-audit.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
