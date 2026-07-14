from __future__ import annotations

import hashlib
import json
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket117_twin_dyadic_mobius_endpoint_gram_audit import (
    audit_dyadic_mobius_endpoint_gram,
    evaluate_partition,
)


GENERATED_AT = "2026-07-15T02:05:00+09:00"
SCHEMA = "primeproject.ticket118-canonical-adjacent-pair-holdout.v1"
PREREGISTRATION_SCHEMA = (
    "primeproject.ticket118-canonical-adjacent-pair-preregistration.v1"
)
SOURCE_COMMIT = "c6d6ee13d9d53b87c6b672572444c07d53dd04ab"
PREREGISTRATION_COMMIT = "5b52d4d58873afc512555ba6079d4280f61757ae"
HOLDOUT_HORIZON = 8_388_608
RULE_ID = "canonical_adjacent_shell_pairs_v1"


def canonical_adjacent_partition(block_count: int) -> list[tuple[int, int]]:
    return [
        (start, min(start + 2, block_count))
        for start in range(0, block_count, 2)
    ]


def preregistration_contract() -> dict[str, Any]:
    preregistration = read_json(
        ROOT
        / "data/open-problem/ticket118-canonical-adjacent-pair-preregistration.json"
    )
    if preregistration.get("schema") != PREREGISTRATION_SCHEMA:
        raise ValueError("TICKET118 preregistration schema changed")
    if preregistration.get("source_commit") != SOURCE_COMMIT:
        raise ValueError("TICKET118 source commit changed")
    if int(preregistration.get("holdout_horizon", -1)) != HOLDOUT_HORIZON:
        raise ValueError("TICKET118 holdout horizon changed")
    if preregistration.get("rule_id") != RULE_ID:
        raise ValueError("TICKET118 canonical rule changed")
    return preregistration


def canonical_payload_sha256(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def run_holdout() -> dict[str, Any]:
    preregistration = preregistration_contract()
    row = audit_dyadic_mobius_endpoint_gram(
        HOLDOUT_HORIZON,
        None,
        "post_registration_canonical_pair_holdout",
    )
    partition = canonical_adjacent_partition(int(row["dyadic_block_count"]))
    canonical = evaluate_partition(
        partition,
        row["dyadic_denominator_profile"],
        row["dyadic_block_profile"],
    )
    boundary_and_variation = (
        float(row["boundary_phase_lipschitz_envelope"])
        + float(row["variation_absolute_envelope"])
    )
    canonical["budget_ratio_to_signed"] = (
        float(canonical["numerator_budget"])
        / float(row["signed_numerator_budget_reconstructed"])
    )
    canonical["adverse_budget"] = (
        float(canonical["numerator_budget"]) + boundary_and_variation
    )
    canonical["lower_bound"] = (
        float(row["known_without_type_ii_minor"])
        - float(canonical["adverse_budget"])
    )
    canonical["closes_finite"] = bool(float(canonical["lower_bound"]) > 0)
    best_width_two = row["best_width_two_contiguous_partition"]
    canonical_signature = [
        (group["first_block"], group["last_block"])
        for group in canonical["groups"]
    ]
    best_signature = [
        (group["first_block"], group["last_block"])
        for group in best_width_two["groups"]
    ]
    primary_status = (
        "pass_finite_closure"
        if canonical["closes_finite"]
        else "fail_no_finite_closure"
    )
    row.pop("independent_sign_numerator_budget", None)
    row.pop("dyadic_to_sign_budget_ratio", None)
    return {
        "theorem_name": "PreregisteredCanonicalAdjacentDyadicPairEightMillionHoldout",
        "source_ticket": "TICKET-117",
        "source_commit": SOURCE_COMMIT,
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "preregistration_payload_sha256": canonical_payload_sha256(
            preregistration
        ),
        "rule_id": RULE_ID,
        "preregistration": preregistration,
        "primary_result": {
            "status": primary_status,
            "holdout_horizon": HOLDOUT_HORIZON,
            "finite_lower_bound": canonical["lower_bound"],
            "passes_registered_endpoint": canonical["closes_finite"],
            "interpretation": "This is exactly one post-registration finite test. It is not an all-sufficiently-large-X theorem.",
        },
        "canonical_partition": canonical,
        "best_width_two_comparison": {
            "same_partition": canonical_signature == best_signature,
            "canonical_signature": canonical_signature,
            "best_width_two_signature": best_signature,
            "best_width_two_numerator_budget": best_width_two[
                "numerator_budget"
            ],
            "comparison_is_secondary": True,
        },
        "holdout_row": row,
        "next_theorem_target": "EventuallySubcriticalCanonicalAdjacentDyadicPairVaughanEndpointBudget",
        "proof_boundary": "TICKET118 is a preregistered finite holdout. A pass does not prove an eventual bound or the Twin Prime Conjecture; a failure does not disprove Twin Prime and only refutes finite closure of the frozen rule at 8M.",
    }


def transferred_attempt(
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
        "proof_or_counterexample_mode": "preserve the independent target during the Twin preregistered 8M holdout",
        "attempt": "Preserve the existing infinite target; no Twin canonical-pair holdout result is transferred.",
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "independent_target": target,
        },
        "obstruction": "TICKET118 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    audit = run_holdout()
    ticket117 = read_json(
        ROOT
        / "data/open-problem/ticket117-twin-dyadic-mobius-endpoint-gram-audit.json"
    )
    attempts = [
        transferred_attempt(
            ticket117,
            "riemann",
            "RH-TICKET-118",
            "NonCircularKernelPositivityPreserved",
            "NonCircularExplicitFormulaKernelPositivity",
        ),
        transferred_attempt(
            ticket117,
            "collatz",
            "CO-TICKET-118",
            "GoldenMeanEscapePreserved",
            "GoldenMeanInvariantSetEscape",
        ),
        transferred_attempt(
            ticket117,
            "goldbach",
            "GB-TICKET-118",
            "JointBalancedGoldbachPreserved",
            "JointBalancedVaughanGoldbachResidualEnvelope",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-118",
            "status": "preregistered_canonical_pair_holdout_passed_finite_open",
            "route": "CanonicalAdjacentDyadicPairVaughanEndpointBudget",
            "proof_or_counterexample_mode": "preregistered post-selection holdout with frozen canonical grouping and primary endpoint",
            "attempt": "Freeze the canonical adjacent-shell pairing and positive finite lower expression before computing its 8M endpoint coefficients, then report the result without retuning.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-117",
                "audit_ref": "twin_canonical_adjacent_pair_holdout",
            },
            "obstruction": "One preregistered 8M closure does not prove eventual closure, a uniform bilinear estimate, or positivity of the comparison term on all sufficiently large scales.",
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Expand each canonical factor-four outer-divisor group into its signed Mobius bilinear form and prove a denominator-summed uniform bound, or find an unbounded Vaughan-realizable failure sequence.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    write_json(
        ROOT
        / "data/open-problem/ticket118-twin-canonical-adjacent-pair-holdout.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": "preregistered_holdout_evaluated_open",
            "claim_boundary": audit["proof_boundary"],
            "twin_canonical_adjacent_pair_holdout": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-118-kernel-positivity-preserved.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-118-golden-mean-preserved.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-118-joint-balanced-preserved.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-118-canonical-adjacent-pair-holdout.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
