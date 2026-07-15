from __future__ import annotations

import math
import statistics
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json


GENERATED_AT = "2026-07-15T04:30:00+09:00"
SCHEMA = "primeproject.ticket120-twin-low-divisor-pair-savings-audit.v1"
TOLERANCE = 1e-7


def _pair_budget(
    mean_left: float,
    mean_right: float,
    gram_left: float,
    gram_cross: float,
    gram_right: float,
    geometry_norm: float,
) -> dict[str, float]:
    left_norm = math.sqrt(max(gram_left, 0.0))
    right_norm = math.sqrt(max(gram_right, 0.0))
    pair_energy = gram_left + gram_right + 2.0 * gram_cross
    if pair_energy < -TOLERANCE:
        raise ValueError("pair Gram energy is negative beyond tolerance")
    pair_norm = math.sqrt(max(pair_energy, 0.0))
    singleton_mean = abs(mean_left) + abs(mean_right)
    paired_mean = abs(mean_left + mean_right)
    singleton_centered = geometry_norm * (left_norm + right_norm)
    paired_centered = geometry_norm * pair_norm
    singleton_budget = singleton_mean + singleton_centered
    paired_budget = paired_mean + paired_centered
    denominator_saving = singleton_budget - paired_budget
    gram_scale = math.sqrt(max(gram_left * gram_right, 0.0))
    cosine = gram_cross / gram_scale if gram_scale > 0 else None
    return {
        "singleton_mean": singleton_mean,
        "paired_mean": paired_mean,
        "mean_saving": singleton_mean - paired_mean,
        "singleton_centered": singleton_centered,
        "paired_centered": paired_centered,
        "centered_saving": singleton_centered - paired_centered,
        "singleton_budget": singleton_budget,
        "paired_budget": paired_budget,
        "total_saving": denominator_saving,
        "cauchy_excess": abs(gram_cross) - gram_scale,
        "centered_cosine": cosine,
    }


def _source_rows() -> list[dict[str, Any]]:
    ticket117 = read_json(
        ROOT
        / "data/open-problem/ticket117-twin-dyadic-mobius-endpoint-gram-audit.json"
    )["twin_dyadic_mobius_endpoint_gram_audit"]
    ticket118 = read_json(
        ROOT
        / "data/open-problem/ticket118-twin-canonical-adjacent-pair-holdout.json"
    )["twin_canonical_adjacent_pair_holdout"]
    ticket119 = read_json(
        ROOT
        / "data/open-problem/ticket119-twin-canonical-pair-doubling-holdout.json"
    )["twin_canonical_pair_doubling_holdout"]
    rows = [
        {
            "selection_status": "exploratory_ticket117",
            "row": row,
            "registered_group": None,
        }
        for row in ticket117["rows"]
    ]
    rows.extend(
        [
            {
                "selection_status": "preregistered_ticket118",
                "row": ticket118["holdout_row"],
                "registered_group": ticket118["canonical_partition"]["groups"][0],
            },
            {
                "selection_status": "preregistered_ticket119",
                "row": ticket119["holdout_row"],
                "registered_group": ticket119["canonical_partition"]["groups"][0],
            },
        ]
    )
    return rows


def audit_scale(source: dict[str, Any]) -> dict[str, Any]:
    row = source["row"]
    blocks = row["dyadic_block_profile"]
    if len(blocks) < 2:
        raise ValueError("low-divisor pair requires at least two dyadic blocks")
    denominator_rows: list[dict[str, Any]] = []
    for profile in row["dyadic_denominator_profile"]:
        means = profile["block_mean_signed_contributions"]
        gram = profile["real_gram_matrix"]
        pair = _pair_budget(
            float(means[0]),
            float(means[1]),
            float(gram[0][0]),
            float(gram[0][1]),
            float(gram[1][1]),
            float(profile["projected_phase_l2_norm"]),
        )
        denominator_rows.append(
            {
                "right_denominator": int(profile["right_denominator"]),
                "mean_sign_relation": (
                    "opposite"
                    if float(means[0]) * float(means[1]) < 0
                    else "same_or_zero"
                ),
                **pair,
            }
        )

    totals = {
        key: sum(float(item[key]) for item in denominator_rows)
        for key in (
            "singleton_mean",
            "paired_mean",
            "mean_saving",
            "singleton_centered",
            "paired_centered",
            "centered_saving",
            "singleton_budget",
            "paired_budget",
            "total_saving",
        )
    }
    active_cosines = [
        float(item["centered_cosine"])
        for item in denominator_rows
        if item["centered_cosine"] is not None
    ]
    registered_group = source["registered_group"]
    registered_error = (
        abs(
            float(registered_group["numerator_budget"])
            - totals["paired_budget"]
        )
        if registered_group is not None
        else None
    )
    total_saving_fraction = (
        totals["total_saving"] / totals["singleton_budget"]
        if totals["singleton_budget"] > 0
        else 0.0
    )
    return {
        "horizon": int(row["horizon"]),
        "selection_status": source["selection_status"],
        "first_block": str(blocks[0]["label"]),
        "second_block": str(blocks[1]["label"]),
        "actual_lower": int(blocks[0]["actual_lower"]),
        "actual_upper": int(blocks[1]["actual_upper"]),
        "known_without_type_ii_minor": float(
            row["known_without_type_ii_minor"]
        ),
        **totals,
        "paired_to_singleton_ratio": (
            totals["paired_budget"] / totals["singleton_budget"]
            if totals["singleton_budget"] > 0
            else 0.0
        ),
        "total_saving_fraction": total_saving_fraction,
        "mean_share_of_saving": (
            totals["mean_saving"] / totals["total_saving"]
            if totals["total_saving"] > 0
            else 0.0
        ),
        "paired_to_known_ratio": (
            totals["paired_budget"]
            / float(row["known_without_type_ii_minor"])
        ),
        "opposite_mean_denominator_count": sum(
            item["mean_sign_relation"] == "opposite"
            for item in denominator_rows
        ),
        "active_centered_denominator_count": len(active_cosines),
        "negative_centered_cosine_count": sum(
            cosine < 0 for cosine in active_cosines
        ),
        "centered_cosine_minimum": min(active_cosines, default=None),
        "centered_cosine_median": (
            statistics.median(active_cosines) if active_cosines else None
        ),
        "centered_cosine_maximum": max(active_cosines, default=None),
        "maximum_cauchy_excess": max(
            float(item["cauchy_excess"]) for item in denominator_rows
        ),
        "minimum_denominator_saving": min(
            float(item["total_saving"]) for item in denominator_rows
        ),
        "registered_group_reconstruction_error": registered_error,
        "denominator_profile": denominator_rows,
    }


def abstract_countermodels() -> list[dict[str, Any]]:
    models = [
        {
            "model": "aligned_same_sign_zero_saving",
            "means": (1.0, 1.0),
            "gram": ((1.0, 1.0), (1.0, 1.0)),
            "geometry_norm": 1.0,
            "purpose": "refutes every universal fixed positive pair-saving fraction under only scalar triangle and positive-semidefinite Gram hypotheses",
        },
        {
            "model": "anti_aligned_full_cancellation",
            "means": (1.0, -1.0),
            "gram": ((1.0, -1.0), (-1.0, 1.0)),
            "geometry_norm": 1.0,
            "purpose": "shows that the same weak contract permits complete cancellation and therefore does not determine an arithmetic saving rate",
        },
    ]
    output: list[dict[str, Any]] = []
    for model in models:
        gram = model["gram"]
        result = _pair_budget(
            model["means"][0],
            model["means"][1],
            gram[0][0],
            gram[0][1],
            gram[1][1],
            model["geometry_norm"],
        )
        output.append(
            {
                **model,
                **result,
                "gram_determinant": (
                    gram[0][0] * gram[1][1] - gram[0][1] ** 2
                ),
                "positive_semidefinite": bool(
                    gram[0][0] >= 0
                    and gram[1][1] >= 0
                    and gram[0][0] * gram[1][1] - gram[0][1] ** 2 >= 0
                ),
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
        "proof_or_counterexample_mode": "preserve the independent target during the Twin low-divisor structural audit",
        "attempt": "No Twin Gram or low-divisor saving result is transferred to this problem.",
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "independent_target": target,
        },
        "obstruction": "TICKET120 supplies no new problem-specific infinite theorem here.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    scale_rows = [audit_scale(source) for source in _source_rows()]
    countermodels = abstract_countermodels()
    machine = {
        "scale_count": len(scale_rows),
        "denominator_row_count": sum(
            len(row["denominator_profile"]) for row in scale_rows
        ),
        "maximum_cauchy_excess": max(
            row["maximum_cauchy_excess"] for row in scale_rows
        ),
        "minimum_denominator_saving": min(
            row["minimum_denominator_saving"] for row in scale_rows
        ),
        "maximum_registered_group_reconstruction_error": max(
            (
                row["registered_group_reconstruction_error"]
                for row in scale_rows
                if row["registered_group_reconstruction_error"] is not None
            ),
            default=0.0,
        ),
        "abstract_countermodel_count": len(countermodels),
        "weak_fixed_fraction_counterexample_ratio": (
            countermodels[0]["paired_budget"]
            / countermodels[0]["singleton_budget"]
        ),
        "total_failure_count": 0,
    }
    if machine["maximum_cauchy_excess"] > TOLERANCE:
        machine["total_failure_count"] += 1
    if machine["minimum_denominator_saving"] < -TOLERANCE:
        machine["total_failure_count"] += 1
    if machine["maximum_registered_group_reconstruction_error"] > TOLERANCE:
        machine["total_failure_count"] += 1
    if abs(machine["weak_fixed_fraction_counterexample_ratio"] - 1.0) > TOLERANCE:
        machine["total_failure_count"] += 1

    audit = {
        "theorem_name": "LowDivisorCanonicalPairSavingsIdentityAndWeakContractNoGo",
        "source_ticket": "TICKET-119",
        "exact_identity": {
            "scalar": "|m0|+|m1|-|m0+m1| >= 0",
            "centered": "w(||z0||+||z1||-||z0+z1||) >= 0",
            "combined": "singleton low-pair budget - paired low-pair budget = scalar saving + centered saving >= 0",
            "scope": "universal for two scalar means and two vectors in a real or complex Hilbert space",
        },
        "scale_rows": scale_rows,
        "abstract_countermodels": countermodels,
        "discarded_candidate": {
            "name": "UniversalFixedFractionLowDivisorPairSavingUnderGramContract",
            "claim": "there exists eta>0 such that paired_budget <= (1-eta) singleton_budget under only the triangle and positive-semidefinite Gram contracts",
            "status": "refuted_by_exact_weak_contract_countermodel",
            "witness": "aligned_same_sign_zero_saving",
            "reason": "the witness has positive-semidefinite rank-one Gram matrix and paired/singleton ratio exactly one",
        },
        "retained_theorem": {
            "name": "VaughanLowDivisorDenominatorSummedAngleGap",
            "quantifiers": "there exist eta>0 and X0 such that every X>=X0 satisfies an arithmetic denominator-summed mean-sign and centered-angle gap for the actual first canonical Vaughan pair",
            "required_input": "signed Mobius/divisor convolution, denominator phases, and scale-uniform coefficient estimates not implied by Gram positivity",
            "role": "first sublemma toward EventuallySubcriticalCanonicalAdjacentDyadicPairVaughanEndpointBudget",
            "counterexample_route": "construct an unbounded Vaughan-realizable sequence whose low-pair paired/singleton ratio approaches one or whose paired-to-known contribution defeats every fixed full-budget margin",
        },
        "machine_audit": machine,
        "proof_boundary": "TICKET120 proves an elementary universal pair-saving identity and refutes a weak-contract fixed-fraction lemma. The scale rows are finite diagnostics. It does not prove a Vaughan arithmetic angle gap, eventual endpoint closure, or the Twin Prime Conjecture.",
    }
    ticket119 = read_json(
        ROOT
        / "data/open-problem/ticket119-twin-canonical-pair-doubling-holdout.json"
    )
    attempts = [
        preserved_attempt(
            ticket119,
            "riemann",
            "RH-TICKET-120",
            "NonCircularKernelPositivityPreserved",
            "NonCircularExplicitFormulaKernelPositivity",
        ),
        preserved_attempt(
            ticket119,
            "collatz",
            "CO-TICKET-120",
            "GoldenMeanEscapePreserved",
            "GoldenMeanInvariantSetEscape",
        ),
        preserved_attempt(
            ticket119,
            "goldbach",
            "GB-TICKET-120",
            "JointBalancedGoldbachPreserved",
            "JointBalancedVaughanGoldbachResidualEnvelope",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-120",
            "status": "exact_pair_identity_proved_weak_fraction_refuted_open",
            "route": "LowDivisorCanonicalPairSavingsIdentity",
            "proof_or_counterexample_mode": "prove the exact weak identity, then falsify unjustified uniform strengthening",
            "attempt": "Decompose the first canonical pair saving into scalar sign and centered Hilbert-angle terms at every denominator, then test whether Gram positivity alone forces a fixed fractional saving.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-119",
                "audit_ref": "twin_low_divisor_pair_savings_audit",
            },
            "obstruction": "The exact aligned rank-one countermodel has zero pair saving, so any positive uniform saving must use arithmetic Vaughan structure absent from the weak Gram contract.",
            "candidate_theorem": audit["retained_theorem"]["name"],
            "next_experiment": "Expand the first factor-four pair into signed Mobius/divisor sums and seek a denominator-summed arithmetic angle gap, while using the aligned model as the mandatory falsification oracle.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    write_json(
        ROOT / "data/open-problem/ticket120-twin-low-divisor-pair-savings-audit.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": "exact_finite_identity_and_weak_contract_nogo_open",
            "claim_boundary": audit["proof_boundary"],
            "twin_low_divisor_pair_savings_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-120-kernel-positivity-preserved.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-120-golden-mean-preserved.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-120-joint-balanced-preserved.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-120-low-divisor-pair-savings-audit.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return machine["total_failure_count"]


if __name__ == "__main__":
    raise SystemExit(main())
