from __future__ import annotations

import hashlib
import json
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json


GENERATED_AT = "2026-07-15T03:45:00+09:00"
SCHEMA = "primeproject.ticket119-canonical-pair-doubling-holdout.v1"
PREREGISTRATION_SCHEMA = (
    "primeproject.ticket119-canonical-pair-doubling-preregistration.v1"
)
SOURCE_COMMIT = "2852b1a086233523aaca78526e16d31ef4b4c221"
PREREGISTRATION_COMMIT = "87bdcf9b16c5e57581e9a411aa61290ef2eea173"
HOLDOUT_HORIZON = 16_777_216
RULE_ID = "canonical_adjacent_shell_pairs_v1"


def canonical_adjacent_partition(block_count: int) -> list[tuple[int, int]]:
    return [
        (start, min(start + 2, block_count))
        for start in range(0, block_count, 2)
    ]


def canonical_payload_sha256(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def preregistration_contract() -> dict[str, Any]:
    preregistration = read_json(
        ROOT
        / "data/open-problem/ticket119-canonical-pair-doubling-preregistration.json"
    )
    if preregistration.get("schema") != PREREGISTRATION_SCHEMA:
        raise ValueError("TICKET119 preregistration schema changed")
    if preregistration.get("source_commit") != SOURCE_COMMIT:
        raise ValueError("TICKET119 source commit changed")
    if int(preregistration.get("holdout_horizon", -1)) != HOLDOUT_HORIZON:
        raise ValueError("TICKET119 holdout horizon changed")
    if preregistration.get("rule_id") != RULE_ID:
        raise ValueError("TICKET119 canonical rule changed")
    if int(preregistration.get("execution_policy", {}).get("runs", -1)) != 1:
        raise ValueError("TICKET119 execution count changed")
    return preregistration


def run_holdout() -> dict[str, Any]:
    from ticket117_twin_dyadic_mobius_endpoint_gram_audit import (
        audit_dyadic_mobius_endpoint_gram,
        evaluate_partition,
    )

    preregistration = preregistration_contract()
    row = audit_dyadic_mobius_endpoint_gram(
        HOLDOUT_HORIZON,
        None,
        "post_registration_canonical_pair_doubling_holdout",
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
    known = float(row["known_without_type_ii_minor"])
    canonical["budget_ratio_to_signed"] = (
        float(canonical["numerator_budget"])
        / float(row["signed_numerator_budget_reconstructed"])
    )
    canonical["adverse_budget"] = (
        float(canonical["numerator_budget"]) + boundary_and_variation
    )
    canonical["lower_bound"] = known - float(canonical["adverse_budget"])
    canonical["closes_finite"] = bool(float(canonical["lower_bound"]) > 0)
    canonical["adverse_to_known_ratio"] = (
        float(canonical["adverse_budget"]) / known
    )
    canonical["normalized_margin"] = float(canonical["lower_bound"]) / known

    reference = preregistration["registered_reference"]
    reference_margin = float(reference["normalized_margin"])
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
        "theorem_name": "PreregisteredCanonicalAdjacentDyadicPairSixteenMillionHoldout",
        "source_ticket": "TICKET-118",
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
            "interpretation": "This is exactly one post-registration 16M finite test. It is not an all-sufficiently-large-X theorem.",
        },
        "scale_comparison": {
            "reference_horizon": int(reference["horizon"]),
            "reference_normalized_margin": reference_margin,
            "holdout_normalized_margin": canonical["normalized_margin"],
            "normalized_margin_change": (
                canonical["normalized_margin"] - reference_margin
            ),
            "normalized_margin_non_decreasing": bool(
                canonical["normalized_margin"] >= reference_margin
            ),
            "interpretation": "The direction comparison is a registered secondary endpoint. It neither fits nor proves a scaling exponent.",
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
        "proof_boundary": "TICKET119 is a preregistered finite persistence test. A pass does not prove eventual positivity or Twin Prime; a failure refutes only the frozen 8M-to-16M dyadic-persistence claim.",
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
        "proof_or_counterexample_mode": "preserve the independent target during the Twin 16M persistence holdout",
        "attempt": "Preserve the existing infinite target; no Twin scale-persistence result is transferred.",
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "independent_target": target,
        },
        "obstruction": "TICKET119 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    audit = run_holdout()
    ticket118 = read_json(
        ROOT
        / "data/open-problem/ticket118-twin-canonical-adjacent-pair-holdout.json"
    )
    attempts = [
        preserved_attempt(
            ticket118,
            "riemann",
            "RH-TICKET-119",
            "NonCircularKernelPositivityPreserved",
            "NonCircularExplicitFormulaKernelPositivity",
        ),
        preserved_attempt(
            ticket118,
            "collatz",
            "CO-TICKET-119",
            "GoldenMeanEscapePreserved",
            "GoldenMeanInvariantSetEscape",
        ),
        preserved_attempt(
            ticket118,
            "goldbach",
            "GB-TICKET-119",
            "JointBalancedGoldbachPreserved",
            "JointBalancedVaughanGoldbachResidualEnvelope",
        ),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-119",
            "status": (
                "preregistered_dyadic_persistence_passed_finite_open"
                if audit["primary_result"]["passes_registered_endpoint"]
                else "preregistered_dyadic_persistence_refuted_finite_open"
            ),
            "route": "CanonicalAdjacentDyadicPairScalePersistence",
            "proof_or_counterexample_mode": "preregistered 16M falsification attempt of the frozen 8M canonical-pair persistence claim",
            "attempt": "Apply the unchanged canonical adjacent-shell rule at the first unseen doubled scale and report the first result without retuning.",
            "bounded_result": {
                "source_ticket": "TP-TICKET-118",
                "audit_ref": "twin_canonical_pair_doubling_holdout",
            },
            "obstruction": "Even two consecutive dyadic closures would not prove an eventual bound; a finite failure would refute only this persistence route, not Twin Prime.",
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Use the 16M group profile to state a result-independent denominator-summed bilinear lemma, or preregister the next dyadic falsification scale without changing the rule.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    write_json(
        ROOT
        / "data/open-problem/ticket119-twin-canonical-pair-doubling-holdout.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": "preregistered_doubling_holdout_evaluated_open",
            "claim_boundary": audit["proof_boundary"],
            "twin_canonical_pair_doubling_holdout": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-119-kernel-positivity-preserved.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-119-golden-mean-preserved.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-119-joint-balanced-preserved.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-119-canonical-pair-doubling-holdout.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
