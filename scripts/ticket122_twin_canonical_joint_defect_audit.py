from __future__ import annotations

import math
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket119_twin_canonical_pair_doubling_holdout import (
    canonical_adjacent_partition,
)
from ticket120_twin_low_divisor_pair_savings_audit import _source_rows
from ticket121_twin_balance_angle_defect_audit import balance_angle_row


GENERATED_AT = "2026-07-16T00:40:00+09:00"
SCHEMA = "primeproject.ticket122-twin-canonical-joint-defect-audit.v1"
TOLERANCE = 1e-7


def scalar_mean_row(left: float, right: float) -> dict[str, float | str]:
    left_abs = abs(left)
    right_abs = abs(right)
    singleton = left_abs + right_abs
    paired = abs(left + right)
    opposition = left * right < 0.0
    exact_formula = 2.0 * min(left_abs, right_abs) if opposition else 0.0
    return {
        "left_mean": left,
        "right_mean": right,
        "sign_relation": "opposite" if opposition else "same_or_zero",
        "singleton_mean": singleton,
        "paired_mean": paired,
        "mean_saving": singleton - paired,
        "mean_saving_formula": exact_formula,
        "mean_formula_error": abs(singleton - paired - exact_formula),
        "opposed_minimum_mass": min(left_abs, right_abs) if opposition else 0.0,
        "scalar_balance": (
            min(left_abs, right_abs) / singleton if singleton > 0 else 0.0
        ),
    }


def canonical_pair_row(
    left_mean: float,
    right_mean: float,
    gram_left: float,
    gram_cross: float,
    gram_right: float,
    geometry_norm: float,
) -> dict[str, Any]:
    scalar = scalar_mean_row(left_mean, right_mean)
    vector = balance_angle_row(
        gram_left,
        gram_cross,
        gram_right,
        geometry_norm,
    )
    singleton_budget = float(scalar["singleton_mean"]) + float(
        vector["singleton_centered"]
    )
    paired_budget = float(scalar["paired_mean"]) + float(
        vector["paired_centered"]
    )
    total_saving = singleton_budget - paired_budget
    lower_certificate = float(scalar["mean_saving"]) + float(
        vector["quadratic_lower_certificate"]
    )
    upper_certificate = float(scalar["mean_saving"]) + float(
        vector["quadratic_upper_certificate"]
    )
    return {
        **scalar,
        **vector,
        "singleton_budget": singleton_budget,
        "paired_budget": paired_budget,
        "total_saving": total_saving,
        "joint_lower_certificate": lower_certificate,
        "joint_upper_certificate": upper_certificate,
        "joint_lower_violation": lower_certificate - total_saving,
        "joint_upper_violation": total_saving - upper_certificate,
    }


def _sum(rows: list[dict[str, Any]], field: str) -> float:
    return sum(float(row[field]) for row in rows)


def _evaluate_partition_budget(
    partition: list[tuple[int, int]],
    denominator_profiles: list[dict[str, Any]],
) -> float:
    """Recompute the grouped budget without TICKET-117's NumPy dependency."""
    budget = 0.0
    for profile in denominator_profiles:
        means = profile["block_mean_signed_contributions"]
        gram = profile["real_gram_matrix"]
        geometry_norm = float(profile["projected_phase_l2_norm"])
        for start, end in partition:
            mean_cost = abs(
                sum(float(means[index]) for index in range(start, end))
            )
            energy = sum(
                float(gram[left][right])
                for left in range(start, end)
                for right in range(start, end)
            )
            budget += mean_cost + math.sqrt(max(energy, 0.0)) * geometry_norm
    return budget


def audit_pair_group(
    row: dict[str, Any],
    left_index: int,
    right_index: int,
) -> dict[str, Any]:
    blocks = row["dyadic_block_profile"]
    denominator_rows: list[dict[str, Any]] = []
    for profile in row["dyadic_denominator_profile"]:
        means = profile["block_mean_signed_contributions"]
        gram = profile["real_gram_matrix"]
        denominator_rows.append(
            {
                "right_denominator": int(profile["right_denominator"]),
                **canonical_pair_row(
                    float(means[left_index]),
                    float(means[right_index]),
                    float(gram[left_index][left_index]),
                    float(gram[left_index][right_index]),
                    float(gram[right_index][right_index]),
                    float(profile["projected_phase_l2_norm"]),
                ),
            }
        )

    totals = {
        field: _sum(denominator_rows, field)
        for field in (
            "singleton_mean",
            "paired_mean",
            "mean_saving",
            "singleton_centered",
            "paired_centered",
            "actual_centered_saving",
            "quadratic_lower_certificate",
            "quadratic_upper_certificate",
            "singleton_budget",
            "paired_budget",
            "total_saving",
            "joint_lower_certificate",
            "joint_upper_certificate",
        )
    }
    centered_singleton = totals["singleton_centered"]
    qualifying_mass = sum(
        float(item["singleton_centered"])
        for item in denominator_rows
        if item["qualifies_balanced_decorrelated_mass"]
    )
    singleton_budget = totals["singleton_budget"]
    return {
        "left_block": str(blocks[left_index]["label"]),
        "right_block": str(blocks[right_index]["label"]),
        "actual_lower": int(blocks[left_index]["actual_lower"]),
        "actual_upper": int(blocks[right_index]["actual_upper"]),
        **totals,
        "total_saving_fraction": (
            totals["total_saving"] / singleton_budget
            if singleton_budget > 0
            else 0.0
        ),
        "mean_saving_fraction": (
            totals["mean_saving"] / totals["singleton_mean"]
            if totals["singleton_mean"] > 0
            else 0.0
        ),
        "centered_saving_fraction": (
            totals["actual_centered_saving"] / centered_singleton
            if centered_singleton > 0
            else 0.0
        ),
        "joint_certificate_fraction": (
            totals["joint_lower_certificate"] / singleton_budget
            if singleton_budget > 0
            else 0.0
        ),
        "qualifying_centered_mass_fraction": (
            qualifying_mass / centered_singleton
            if centered_singleton > 0
            else 0.0
        ),
        "opposite_mean_denominator_count": sum(
            item["sign_relation"] == "opposite"
            for item in denominator_rows
        ),
        "active_denominator_count": sum(
            float(item["singleton_budget"]) > 0
            for item in denominator_rows
        ),
        "maximum_mean_formula_error": max(
            float(item["mean_formula_error"]) for item in denominator_rows
        ),
        "maximum_vector_rationalization_error": max(
            float(item["rationalization_error"])
            for item in denominator_rows
        ),
        "maximum_joint_lower_violation": max(
            float(item["joint_lower_violation"])
            for item in denominator_rows
        ),
        "maximum_joint_upper_violation": max(
            float(item["joint_upper_violation"])
            for item in denominator_rows
        ),
        "denominator_profile": denominator_rows,
    }


def audit_singleton_group(
    row: dict[str, Any],
    block_index: int,
) -> dict[str, Any]:
    block = row["dyadic_block_profile"][block_index]
    mean_budget = 0.0
    centered_budget = 0.0
    for profile in row["dyadic_denominator_profile"]:
        mean_budget += abs(
            float(profile["block_mean_signed_contributions"][block_index])
        )
        gram = profile["real_gram_matrix"]
        centered_budget += float(profile["projected_phase_l2_norm"]) * math.sqrt(
            max(float(gram[block_index][block_index]), 0.0)
        )
    return {
        "block": str(block["label"]),
        "actual_lower": int(block["actual_lower"]),
        "actual_upper": int(block["actual_upper"]),
        "mean_budget": mean_budget,
        "centered_budget": centered_budget,
        "singleton_budget": mean_budget + centered_budget,
        "reason": "An odd final dyadic block has no canonical adjacent partner and receives no pair-saving certificate.",
    }


def audit_scale(source: dict[str, Any]) -> dict[str, Any]:
    row = source["row"]
    blocks = row["dyadic_block_profile"]
    partition = canonical_adjacent_partition(len(blocks))
    pair_groups = [
        audit_pair_group(row, start, start + 1)
        for start, end in partition
        if end - start == 2
    ]
    residual_groups = [
        audit_singleton_group(row, start)
        for start, end in partition
        if end - start == 1
    ]
    pair_singleton = _sum(pair_groups, "singleton_budget")
    pair_paired = _sum(pair_groups, "paired_budget")
    pair_saving = _sum(pair_groups, "total_saving")
    mean_saving = _sum(pair_groups, "mean_saving")
    centered_saving = _sum(pair_groups, "actual_centered_saving")
    lower_certificate = _sum(pair_groups, "joint_lower_certificate")
    residual_budget = _sum(residual_groups, "singleton_budget")
    singleton_budget = pair_singleton + residual_budget
    canonical_budget = pair_paired + residual_budget
    evaluated_budget = _evaluate_partition_budget(
        partition,
        row["dyadic_denominator_profile"],
    )
    known = float(row["known_without_type_ii_minor"])
    boundary = float(row["boundary_phase_lipschitz_envelope"]) + float(
        row["variation_absolute_envelope"]
    )
    raw_saving_requirement = singleton_budget + boundary - known
    required_saving = max(0.0, raw_saving_requirement)
    finite_lower_bound = known - canonical_budget - boundary
    outer_groups = pair_groups[1:]
    outer_singleton = _sum(outer_groups, "singleton_budget")
    outer_saving = _sum(outer_groups, "total_saving")
    first_saving = float(pair_groups[0]["total_saving"])
    centered_singleton = _sum(pair_groups, "singleton_centered")
    qualifying_centered = sum(
        float(item["singleton_centered"])
        for group in pair_groups
        for item in group["denominator_profile"]
        if item["qualifies_balanced_decorrelated_mass"]
    )
    expected_singleton = float(row["independent_dyadic_numerator_budget"])
    return {
        "horizon": int(row["horizon"]),
        "selection_status": source["selection_status"],
        "block_count": len(blocks),
        "pair_group_count": len(pair_groups),
        "residual_group_count": len(residual_groups),
        "known_without_type_ii_minor": known,
        "boundary_and_variation_budget": boundary,
        "independent_singleton_budget": singleton_budget,
        "canonical_paired_budget": canonical_budget,
        "exact_total_saving": pair_saving,
        "exact_mean_saving": mean_saving,
        "exact_centered_saving": centered_saving,
        "joint_lower_certificate": lower_certificate,
        "total_saving_fraction": (
            pair_saving / singleton_budget if singleton_budget > 0 else 0.0
        ),
        "joint_certificate_fraction": (
            lower_certificate / singleton_budget
            if singleton_budget > 0
            else 0.0
        ),
        "pairable_singleton_budget_share": (
            pair_singleton / singleton_budget
            if singleton_budget > 0
            else 0.0
        ),
        "residual_singleton_budget": residual_budget,
        "residual_singleton_budget_share": (
            residual_budget / singleton_budget
            if singleton_budget > 0
            else 0.0
        ),
        "qualifying_centered_mass_fraction": (
            qualifying_centered / centered_singleton
            if centered_singleton > 0
            else 0.0
        ),
        "first_pair_saving_share": (
            first_saving / pair_saving if pair_saving > 0 else 0.0
        ),
        "outer_pair_saving_fraction": (
            outer_saving / outer_singleton if outer_singleton > 0 else None
        ),
        "raw_saving_requirement": raw_saving_requirement,
        "required_saving_for_finite_closure": required_saving,
        "saving_surplus_over_raw_requirement": pair_saving
        - raw_saving_requirement,
        "saving_surplus_over_positive_requirement": pair_saving
        - required_saving,
        "finite_lower_bound": finite_lower_bound,
        "closes_finite": bool(finite_lower_bound > 0),
        "singleton_reconstruction_error": abs(
            singleton_budget - expected_singleton
        ),
        "canonical_reconstruction_error": abs(
            canonical_budget - evaluated_budget
        ),
        "saving_identity_error": abs(
            pair_saving - (singleton_budget - canonical_budget)
        ),
        "certificate_lower_violation": lower_certificate - pair_saving,
        "minimum_pair_saving_fraction": min(
            float(group["total_saving_fraction"])
            for group in pair_groups
        ),
        "pair_groups": pair_groups,
        "residual_groups": residual_groups,
    }


def abstract_countermodels() -> dict[str, Any]:
    local_only = []
    centered_only = []
    for scale in (1.0, 10.0, 100.0, 1_000.0, 1_000_000.0):
        local_only.append(
            {
                "outer_scale": scale,
                "first_pair_singleton": 2.0,
                "first_pair_saving": 2.0,
                "aligned_outer_singleton": 2.0 * scale,
                "aligned_outer_saving": 0.0,
                "global_saving_fraction": 1.0 / (1.0 + scale),
            }
        )
        centered_only.append(
            {
                "mean_scale": scale,
                "centered_singleton": 2.0,
                "centered_saving": 2.0,
                "same_sign_mean_singleton": 2.0 * scale,
                "mean_saving": 0.0,
                "total_saving_fraction": 1.0 / (1.0 + scale),
            }
        )
    return {
        "first_pair_only_no_go": {
            "construction": "Use z0=u,z1=-u in the first pair, then append an outer pair z2=Mv,z3=Mv with zero means. The first pair saves 100%, but the global saving fraction is 1/(1+M).",
            "purpose": "Refutes every global fixed-saving theorem derived from a low-divisor pair condition without a tail-mass bound.",
            "sequence": local_only,
        },
        "centered_only_total_budget_no_go": {
            "construction": "Use z0=u,z1=-u with same-sign scalar means m0=m1=M. Centered saving is complete, mean saving is zero, and the total saving fraction is 1/(1+M).",
            "purpose": "Refutes every full-budget fixed-saving theorem based only on centered balance-angle mass without scalar-mean control or centered-budget dominance.",
            "sequence": centered_only,
        },
    }


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
        "proof_or_counterexample_mode": "preserve the independent target during the Twin canonical joint-defect audit",
        "attempt": "No Twin canonical-pair identity or no-go family is transferred to this problem.",
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "independent_target": target,
        },
        "obstruction": "TICKET122 supplies no new problem-specific infinite theorem here.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def build_audit() -> dict[str, Any]:
    scale_rows = [audit_scale(source) for source in _source_rows()]
    countermodels = abstract_countermodels()
    machine = {
        "scale_count": len(scale_rows),
        "pair_group_count": sum(
            int(row["pair_group_count"]) for row in scale_rows
        ),
        "pair_denominator_row_count": sum(
            len(group["denominator_profile"])
            for row in scale_rows
            for group in row["pair_groups"]
        ),
        "finite_closure_count": sum(
            int(row["closes_finite"]) for row in scale_rows
        ),
        "minimum_total_saving_fraction": min(
            float(row["total_saving_fraction"]) for row in scale_rows
        ),
        "minimum_joint_certificate_fraction": min(
            float(row["joint_certificate_fraction"])
            for row in scale_rows
        ),
        "minimum_pair_total_saving": min(
            float(group["total_saving"])
            for row in scale_rows
            for group in row["pair_groups"]
        ),
        "minimum_pair_saving_fraction": min(
            float(group["total_saving_fraction"])
            for row in scale_rows
            for group in row["pair_groups"]
        ),
        "maximum_residual_singleton_budget_share": max(
            float(row["residual_singleton_budget_share"])
            for row in scale_rows
        ),
        "maximum_singleton_reconstruction_error": max(
            float(row["singleton_reconstruction_error"])
            for row in scale_rows
        ),
        "maximum_canonical_reconstruction_error": max(
            float(row["canonical_reconstruction_error"])
            for row in scale_rows
        ),
        "maximum_saving_identity_error": max(
            float(row["saving_identity_error"]) for row in scale_rows
        ),
        "maximum_mean_formula_error": max(
            float(group["maximum_mean_formula_error"])
            for row in scale_rows
            for group in row["pair_groups"]
        ),
        "maximum_vector_rationalization_error": max(
            float(group["maximum_vector_rationalization_error"])
            for row in scale_rows
            for group in row["pair_groups"]
        ),
        "maximum_joint_lower_violation": max(
            float(group["maximum_joint_lower_violation"])
            for row in scale_rows
            for group in row["pair_groups"]
        ),
        "maximum_joint_upper_violation": max(
            float(group["maximum_joint_upper_violation"])
            for row in scale_rows
            for group in row["pair_groups"]
        ),
        "first_pair_no_go_terminal_fraction": countermodels[
            "first_pair_only_no_go"
        ]["sequence"][-1]["global_saving_fraction"],
        "centered_only_no_go_terminal_fraction": countermodels[
            "centered_only_total_budget_no_go"
        ]["sequence"][-1]["total_saving_fraction"],
        "total_failure_count": 0,
    }
    for field in (
        "maximum_singleton_reconstruction_error",
        "maximum_canonical_reconstruction_error",
        "maximum_saving_identity_error",
        "maximum_mean_formula_error",
        "maximum_vector_rationalization_error",
        "maximum_joint_lower_violation",
        "maximum_joint_upper_violation",
    ):
        machine["total_failure_count"] += int(
            float(machine[field]) > TOLERANCE
        )
    machine["total_failure_count"] += int(
        float(machine["minimum_pair_total_saving"]) < -TOLERANCE
    )

    return {
        "theorem_name": "CanonicalAdjacentPairScalarVectorDefectIdentityAndLocalOnlyNoGo",
        "source_ticket": "TICKET-121",
        "exact_joint_identity": {
            "notation": "m0,m1 are real block means; a=||z0||, b=||z1||, c=Re<z0,z1>, p=||z0+z1||, w>=0",
            "identity": "|m0|+|m1|-|m0+m1| + w(a+b-p) = 2*1_{m0*m1<0}*min(|m0|,|m1|) + 2w(ab-c)/(a+b+p)",
            "lower_certificate": "joint saving >= 2*1_{m0*m1<0}*min(|m0|,|m1|) + w(ab-c)/(a+b)",
            "summation_scope": "The identity and lower certificate sum exactly over every Farey denominator and every result-independent canonical adjacent dyadic pair.",
        },
        "scale_rows": scale_rows,
        "abstract_countermodels": countermodels,
        "discarded_candidates": [
            {
                "name": "LowDivisorBalancedDecorrelatedMassAloneControlsFullCanonicalBudget",
                "reason": "A perfectly cancelling first pair can carry vanishing global mass next to arbitrarily large aligned outer pairs.",
            },
            {
                "name": "CenteredBalanceAngleMassAloneControlsMeanPlusCenteredBudget",
                "reason": "Arbitrarily large same-sign scalar means can dilute complete centered cancellation to zero total saving fraction.",
            },
            {
                "name": "FiniteCanonicalClosureImpliesEventualCanonicalClosure",
                "reason": "The audited closures are finite identities. No monotonicity, limiting defect mass, or all-sufficiently-large-scale bound is proved.",
            },
        ],
        "retained_theorem": {
            "name": "VaughanCanonicalPairJointDefectAndResidualBudgetGap",
            "statement": "Prove constants delta>0 and X0 such that for every X>=X0, the denominator-summed exact joint saving over the fixed canonical adjacent Vaughan shell pairs exceeds independent_singleton_budget + boundary_and_variation - known_without_type_ii_minor by at least delta*known_without_type_ii_minor.",
            "equivalent_budget_form": "known_without_type_ii_minor - canonical_paired_budget - boundary_and_variation >= delta*known_without_type_ii_minor",
            "required_subconditions": "Control scalar opposite-sign balanced mass, centered balance-angle mass, the unpaired final shell, and every outer-pair tail uniformly in X. A theorem for only the first pair or only the centered component is insufficient.",
            "counterexample_route": "Construct an unbounded Vaughan-realizable sequence for which the exact saving surplus is nonpositive, or for which first-pair/centered defect remains positive but outer, mean, residual, or boundary mass makes the normalized surplus tend to zero.",
        },
        "literature_boundary": [
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Prime-producing lower bounds require the joint Type I/II information contract; the paper also constructs extremal sequences showing that weaker contracts can be optimal no-go regimes.",
            },
            {
                "citation": "Tao, The logarithmically averaged Chowla and Elliott conjectures for two-point correlations",
                "url": "https://arxiv.org/abs/1509.05422",
                "role": "Fixed-shift two-point Liouville cancellation is available with logarithmic averaging, not in the unweighted endpoint budget required by this Vaughan kernel.",
            },
            {
                "citation": "Sawin and Shusterman, On the Chowla and twin primes conjectures over F_q[T]",
                "url": "https://annals.math.princeton.edu/2022/196-2/p01",
                "role": "The function-field resolution combines strong distribution and geometric short-sum input unavailable over the integers; it is a model for the missing arithmetic input, not a transferable proof.",
            },
        ],
        "machine_audit": machine,
        "proof_boundary": "TICKET122 proves exact scalar-vector Hilbert identities and two abstract no-go families, then audits finite canonical budgets. It proves no conjecture and certifies no conjecture counterexample.",
    }


def main() -> int:
    audit = build_audit()
    source = read_json(
        ROOT
        / "data/open-problem/ticket121-twin-balance-angle-defect-audit.json"
    )
    attempts = [
        preserved_attempt(
            source,
            "riemann",
            "RH-TICKET-122",
            "NonCircularKernelPositivityPreserved",
            "NonCircularExplicitFormulaKernelPositivity",
        ),
        preserved_attempt(
            source,
            "collatz",
            "CO-TICKET-122",
            "GoldenMeanEscapePreserved",
            "GoldenMeanInvariantSetEscape",
        ),
        preserved_attempt(
            source,
            "goldbach",
            "GB-TICKET-122",
            "JointBalancedGoldbachPreserved",
            "JointBalancedVaughanGoldbachResidualEnvelope",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-122",
            "status": "canonical_joint_identity_proved_local_only_routes_refuted_open",
            "route": "CanonicalPairJointScalarVectorDefect",
            "proof_or_counterexample_mode": "exact all-pair identity, two abstract no-go families, and finite full-budget audit",
            "attempt": "Extend the first-pair centered defect to every canonical adjacent pair, include scalar mean cancellation and residual shells, and compare exact saving with the full finite closure requirement.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-121",
                "audit_ref": "twin_canonical_joint_defect_audit",
            },
            "obstruction": "First-pair or centered-only conditions cannot control the full budget. The corrected joint surplus condition remains unproved for all sufficiently large scales and for the actual integer Vaughan kernel.",
            "candidate_theorem": "VaughanCanonicalPairJointDefectAndResidualBudgetGap",
            "next_experiment": "Expand the exact joint surplus by outer-divisor ranges and seek a uniform Type I/II or large-sieve bound for the adverse outer-pair, residual-shell, and boundary mass; in parallel search for a Vaughan-realizable escaping sequence.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "exact_canonical_joint_identity_and_local_only_nogos_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_canonical_joint_defect_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/ticket122-twin-canonical-joint-defect-audit.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-122-kernel-positivity-preserved.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-122-golden-mean-preserved.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-122-joint-balanced-preserved.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-122-canonical-joint-defect-audit.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
