from __future__ import annotations

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


def main() -> int:
    audit = run_holdout()
    write_json(
        ROOT
        / "data/open-problem/ticket118-twin-canonical-adjacent-pair-holdout.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": "preregistered_holdout_evaluated_open",
            "claim_boundary": audit["proof_boundary"],
            "twin_canonical_adjacent_pair_holdout": audit,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
