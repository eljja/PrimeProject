from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key, template_key
from ticket43_lift_constraint_measure_lab import FAMILY
from ticket50_phase_lift_exception_lab import (
    LASSO_PREFIX,
    START_NEXT_VALUATION,
    START_RESIDUE_MOD_256,
    START_TAIL,
    residue_for_word,
)
from ticket51_phase15_terminal_lift_lab import compact_certificate
from ticket52_frontier_budget_lab import (
    SAMPLE_BITS,
    SAMPLE_COUNT,
    SAMPLE_SEED,
    lasso_prefix_depth_at,
    random_debt_valid_word,
)
from ticket57_parametric_template_automaton_lab import exact32_start_rows


GENERATED_AT = "2026-07-09T13:45:00+09:00"
SCHEMA = "primeproject.ticket58-affine-boundary-lift-lab.v1"
BOUNDARY_LOW_BITS = 28
EXACT32_BITS = 32


def key_for(certificate: dict[str, Any]) -> tuple[Any, ...] | None:
    return template_key(certificate, FAMILY) if certificate.get("status") == "needs_split" else None


def template_text(certificate: dict[str, Any]) -> str:
    key = key_for(certificate)
    return stringify_key(key) if key else str(certificate.get("status"))


def high_outcome(depth: dict[str, Any]) -> str:
    matched = int(depth.get("matched_prefix_templates", 0))
    if matched >= len(LASSO_PREFIX):
        return "full_lasso_period_replay"
    if matched >= 15:
        return "phase5_gate_terminal_tunnel"
    failure = depth.get("first_failure") or {}
    return f"fail_offset_{failure.get('offset', matched)}"


def build_exact32_boundary() -> dict[str, Any]:
    rows = exact32_start_rows()
    mask = (1 << BOUNDARY_LOW_BITS) - 1
    boundary: dict[tuple[int, int], dict[str, Any]] = {}
    duplicates: list[dict[str, Any]] = []
    for row in rows:
        key = (int(row["prefix_length"]), int(row["residue"]) & mask)
        existing = boundary.get(key)
        if existing is not None and existing["coarse_outcome"] != row["coarse_outcome"]:
            duplicates.append(
                {
                    "boundary_key": [key[0], key[1]],
                    "left_residue": existing["residue"],
                    "left_outcome": existing["coarse_outcome"],
                    "right_residue": row["residue"],
                    "right_outcome": row["coarse_outcome"],
                }
            )
        boundary[key] = row
    return {
        "low_bits": BOUNDARY_LOW_BITS,
        "row_count": len(rows),
        "boundary_state_count": len(boundary),
        "collision_count": len(duplicates),
        "duplicates": duplicates[:8],
        "boundary": boundary,
    }


def sample_lift_stability(boundary_data: dict[str, Any], example_limit: int = 10) -> dict[str, Any]:
    boundary = boundary_data["boundary"]
    mask = (1 << BOUNDARY_LOW_BITS) - 1
    rng = random.Random(SAMPLE_SEED)
    target48 = (SAMPLE_BITS % 16, START_TAIL, START_RESIDUE_MOD_256, START_NEXT_VALUATION)
    target32 = (0, START_TAIL, START_RESIDUE_MOD_256, START_NEXT_VALUATION)
    stats: Counter[str] = Counter()
    depth_counts: Counter[int] = Counter()
    high_outcome_counts: Counter[str] = Counter()
    projection_template_counts: Counter[str] = Counter()
    prediction_counts: Counter[str] = Counter()
    boundary_groups: dict[tuple[Any, ...], Counter[str]] = defaultdict(Counter)
    projection_escape_examples: list[dict[str, Any]] = []
    prediction_mismatch_examples: list[dict[str, Any]] = []
    boundary_missing_examples: list[dict[str, Any]] = []
    full_period_examples: list[dict[str, Any]] = []

    for sample_index in range(1, SAMPLE_COUNT + 1):
        word = random_debt_valid_word(SAMPLE_BITS, rng)
        if word is None:
            stats["invalid_tail_debt"] += 1
            continue
        residue = residue_for_word(word)
        certificate = cert(residue, SAMPLE_BITS)
        if certificate.get("status") != "needs_split" or tuple(certificate.get("prefix_word", [])) != word:
            stats["unverified_canonical_word"] += 1
            continue
        stats["verified_open_word"] += 1
        if key_for(certificate) != target48:
            continue

        stats["start_template_match"] += 1
        depth = lasso_prefix_depth_at(residue, SAMPLE_BITS)
        matched = int(depth.get("matched_prefix_templates", 0))
        depth_counts[matched] += 1
        outcome = high_outcome(depth)
        high_outcome_counts[outcome] += 1
        if outcome == "full_lasso_period_replay" and len(full_period_examples) < example_limit:
            full_period_examples.append(
                {
                    "sample_index": sample_index,
                    "residue": residue,
                    "bits": SAMPLE_BITS,
                    "prefix_word_tail": list(word[-12:]),
                    "depth": matched,
                }
            )

        projection_residue = residue % (1 << EXACT32_BITS)
        projection_certificate = cert(projection_residue, EXACT32_BITS)
        projection_key = key_for(projection_certificate)
        projection_template = stringify_key(projection_key) if projection_key else str(projection_certificate.get("status"))
        projection_template_counts[projection_template] += 1

        if projection_key != target32:
            stats["projection_escape"] += 1
            if len(projection_escape_examples) < example_limit:
                projection_escape_examples.append(
                    {
                        "sample_index": sample_index,
                        "residue": residue,
                        "bits": SAMPLE_BITS,
                        "high_outcome": outcome,
                        "matched_prefix_templates": matched,
                        "projection32": {
                            "residue": projection_residue,
                            "template": projection_template,
                            "certificate": compact_certificate(projection_certificate),
                        },
                        "first_failure": depth.get("first_failure"),
                    }
                )
            continue

        stats["projection_target"] += 1
        projection_prefix = int(projection_certificate.get("prefix_length", 0))
        boundary_key = (projection_prefix, projection_residue & mask)
        boundary_group_key = (projection_template, projection_prefix, projection_residue & mask)
        boundary_groups[boundary_group_key][outcome] += 1
        exact_row = boundary.get(boundary_key)
        if exact_row is None:
            stats["boundary_missing"] += 1
            prediction_counts["missing"] += 1
            if len(boundary_missing_examples) < example_limit:
                boundary_missing_examples.append(
                    {
                        "sample_index": sample_index,
                        "residue": residue,
                        "projection_residue": projection_residue,
                        "boundary_key": [projection_prefix, projection_residue & mask],
                        "high_outcome": outcome,
                    }
                )
            continue

        predicted = str(exact_row["coarse_outcome"])
        if predicted == outcome:
            stats["boundary_prediction_match"] += 1
            prediction_counts["match"] += 1
        else:
            stats["boundary_prediction_mismatch"] += 1
            prediction_counts["mismatch"] += 1
            if len(prediction_mismatch_examples) < example_limit:
                prediction_mismatch_examples.append(
                    {
                        "sample_index": sample_index,
                        "residue": residue,
                        "bits": SAMPLE_BITS,
                        "projection_residue": projection_residue,
                        "boundary_key": [projection_prefix, projection_residue & mask],
                        "exact32_residue": exact_row["residue"],
                        "predicted_exact32_outcome": predicted,
                        "observed_48bit_outcome": outcome,
                        "matched_prefix_templates": matched,
                        "first_failure": depth.get("first_failure"),
                        "projection_certificate": compact_certificate(projection_certificate),
                    }
                )

    collision_groups = [
        (key, outcomes)
        for key, outcomes in boundary_groups.items()
        if len(outcomes) > 1
    ]
    collision_examples = [
        {
            "boundary_key": json.dumps(key, ensure_ascii=False, separators=(",", ":")),
            "outcome_counts": dict(sorted(outcomes.items())),
        }
        for key, outcomes in collision_groups[:example_limit]
    ]
    projection_target = stats.get("projection_target", 0)
    mismatch_count = stats.get("boundary_prediction_mismatch", 0)
    projection_escape_count = stats.get("projection_escape", 0)
    return {
        "sample_bits": SAMPLE_BITS,
        "sample_seed": SAMPLE_SEED,
        "sample_count": SAMPLE_COUNT,
        "sampler": "replayed_ticket52_deterministic_weighted_valuation_sampler_not_exhaustive",
        "target48_template": stringify_key(target48),
        "target32_template": stringify_key(target32),
        "boundary_low_bits": BOUNDARY_LOW_BITS,
        "statistics": dict(sorted(stats.items())),
        "depth_counts": {str(key): depth_counts[key] for key in sorted(depth_counts)},
        "high_outcome_counts": dict(sorted(high_outcome_counts.items())),
        "projection32_template_counts": dict(projection_template_counts.most_common(12)),
        "prediction_counts": dict(sorted(prediction_counts.items())),
        "projection_target_prediction_rate": (
            stats.get("boundary_prediction_match", 0) / projection_target if projection_target else None
        ),
        "projection_escape_examples": projection_escape_examples,
        "boundary_prediction_mismatch_examples": prediction_mismatch_examples,
        "boundary_missing_examples": boundary_missing_examples,
        "full_period_examples": full_period_examples,
        "sampled_boundary_collision_group_count": len(collision_groups),
        "sampled_boundary_collision_examples": collision_examples,
        "lift_stability_status": (
            "refuted_by_sampled_boundary_prediction_mismatch"
            if mismatch_count
            else (
                "blocked_by_projection_escape_without_target_mismatch"
                if projection_escape_count
                else "not_refuted_in_replayed_sample"
            )
        ),
        "full_period_escape_status": (
            "sampled_full_period_escape_found"
            if full_period_examples
            else "no_sampled_full_period_escape_found"
        ),
        "proof_boundary": (
            "This is a deterministic replay of the TICKET52 sample, not exhaustive 48-bit coverage. A mismatch "
            "or projection escape refutes a proposed finite lift shortcut, but the absence of a full-period "
            "sampled escape does not prove Collatz."
        ),
    }


def collatz_attempt(ticket57: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket57["attempts"] if attempt["problem_id"] == "collatz")
    boundary = build_exact32_boundary()
    sample = sample_lift_stability(boundary)
    boundary_public = {key: value for key, value in boundary.items() if key != "boundary"}
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-58",
        "route": "AffineBoundaryLiftStabilityOrFullPeriodEscape",
        "status": "sampled_affine_boundary_lift_obstruction_open_no_resolution",
        "proof_or_counterexample_mode": "sampled lift-stability falsification plus full-period escape search",
        "attempt": (
            "Continue from TICKET57's first deterministic exact32 boundary. Rebuild that boundary classifier, then "
            "replay the deterministic TICKET52 48-bit sample to test whether projection-target lifts preserve the "
            "exact32 outcome and whether any sampled root replays a full lasso period."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "affine_boundary_lift_audit": {
                "family": FAMILY,
                "theorem_name": "AffineBoundaryLiftStabilityOrFullPeriodEscape",
                "exact32_boundary": boundary_public,
                "sampled_48bit_lift_stability": sample,
                "discarded_route": (
                    "Promote the exact32 deterministic boundary to a global theorem without proving projection "
                    "inclusion and lift-stable outcome preservation."
                ),
                "retained_route": (
                    "Prove a parametric lift relation for the affine boundary coordinates, or promote a sampled "
                    "projection escape/lift mismatch into a symbolic counterexample target."
                ),
                "candidate_theorem": (
                    "For every 48-bit and then every higher phase-compatible start, either projection leaves the "
                    "exact32 model in a separately classified way, or the affine boundary transition preserves the "
                    "finite gate outcome and decreases a well-founded rank."
                ),
                "counterexample_target": (
                    "Find a higher-bit start whose projection lies in the deterministic exact32 boundary but whose "
                    "lift outcome differs, then extend it to a full-period nondecreasing affine-boundary cycle."
                ),
                "proof_boundary": (
                    "No Collatz proof and no certified Collatz counterexample. TICKET58 tests lift stability on "
                    "the replayed deterministic 48-bit sample and searches for full-period escapes, but it is not "
                    "an exhaustive 48-bit theorem and not a global trajectory proof."
                ),
            },
        },
        "obstruction": (
            "The first deterministic exact32 affine boundary must still pass two higher-bit gates: projection "
            "inclusion and lift-stable outcome preservation. The replayed sample quantifies those gates and keeps "
            "full-period escape search separate from proof claims."
        ),
        "candidate_theorem": (
            "AffineBoundaryLiftStability: prove projection inclusion or a complete escape classification, then "
            "prove outcome-preserving lift transitions with a decreasing rank."
        ),
        "next_experiment": (
            "Generate CO-TICKET-59 by turning any sampled projection escape or lift mismatch into a symbolic "
            "cylinder theorem; if no mismatch is present, expand from sampled replay to a counted 40-bit boundary "
            "cover."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    lift_gate: str,
    candidate_theorem: str,
    counterexample_target: str,
) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "boundary-lift-stability transfer",
        "attempt": (
            "Transfer TICKET58's rule: once a finite boundary state is chosen, test whether the natural lift keeps "
            "objects inside that boundary and preserves the decisive outcome before calling it a theorem."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket58_transfer": route,
            "lift_gate": lift_gate,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "A boundary model can support a proof only if lift inclusion, outcome preservation, and a "
                "well-founded rank are checked in the same coordinates; otherwise the lift escape becomes the "
                "next counterexample target."
            ),
        },
        "obstruction": (
            "This transfer is methodological and does not solve the target problem. It prevents a finite boundary "
            "model from being promoted while the lift map can change the decisive outcome."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Build the problem-specific lift gate or promote a lift escape witness.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket57 = read_json(ROOT / "data/open-problem/ticket57-parametric-template-automaton-lab.json")
    attempts = [
        transfer_attempt(
            ticket57,
            "riemann",
            "RH-TICKET-58",
            "ZeroKernelLiftStabilityOrOffCriticalEscape",
            "height-window lift must preserve the sign/positivity boundary state",
            (
                "Every off-critical zero-kernel boundary state remains in a lift-stable positivity class with "
                "strict improvement, or yields a height-stable off-critical escape packet."
            ),
            "a height lift that preserves the boundary state but reverses or stalls the positivity outcome",
        ),
        collatz_attempt(ticket57),
        transfer_attempt(
            ticket57,
            "goldbach",
            "GB-TICKET-58",
            "MarginLiftStabilityOrExceptionalEscape",
            "larger cutoff lift must preserve the positive-margin boundary classification",
            (
                "Every exceptional residue/margin boundary state lifts to a positive-margin state after a finite "
                "cutoff, or yields a cutoff-stable exceptional even packet."
            ),
            "a larger cutoff lift whose certified margin outcome differs from the finite boundary prediction",
        ),
        transfer_attempt(
            ticket57,
            "twin-prime",
            "TP-TICKET-58",
            "SieveBoundaryLiftStabilityOrGapEscape",
            "sieve-level lift must preserve exact gap-2 retained mass against parity leakage",
            (
                "Every parity-boundary sieve state lifts with positive retained gap-2 mass, or yields a stable "
                "leakage packet that absorbs exact-gap mass at every level."
            ),
            "a sieve-level lift whose parity leakage changes the exact gap-2 outcome predicted by the boundary state",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "affine_boundary_lift_open_no_resolution",
        "claim_boundary": (
            "Ticket 58 tests whether the first deterministic Collatz affine boundary is stable under a replayed "
            "48-bit lift sample and transfers the lift-stability gate to RH, Goldbach, and Twin Prime. It does not "
            "prove or disprove any of the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket58-affine-boundary-lift-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-58-zero-kernel-lift-stability.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-58-affine-boundary-lift.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-58-margin-lift-stability.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-58-sieve-boundary-lift.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
