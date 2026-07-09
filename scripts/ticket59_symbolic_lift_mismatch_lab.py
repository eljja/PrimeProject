from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key
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
from ticket58_affine_boundary_lift_lab import (
    BOUNDARY_LOW_BITS,
    EXACT32_BITS,
    build_exact32_boundary,
    high_outcome,
    key_for,
)


GENERATED_AT = "2026-07-09T15:20:00+09:00"
SCHEMA = "primeproject.ticket59-symbolic-lift-mismatch-lab.v1"
CYLINDER_LOW_BITS = 40
CYLINDER_EXTENSION_BITS = SAMPLE_BITS - CYLINDER_LOW_BITS
MAX_PROJECTION_ESCAPE_CYLINDERS = 64
EXAMPLE_LIMIT = 8


def target_template(bits: int) -> tuple[Any, ...]:
    return (bits % 16, START_TAIL, START_RESIDUE_MOD_256, START_NEXT_VALUATION)


def prediction_for_projection(
    projection_residue: int,
    boundary: dict[tuple[int, int], dict[str, Any]],
) -> tuple[dict[str, Any], str | None]:
    projection_certificate = cert(projection_residue, EXACT32_BITS)
    projection_key = key_for(projection_certificate)
    if projection_key != target_template(EXACT32_BITS):
        return projection_certificate, None

    projection_prefix = int(projection_certificate.get("prefix_length", 0))
    boundary_key = (projection_prefix, projection_residue & ((1 << BOUNDARY_LOW_BITS) - 1))
    exact_row = boundary.get(boundary_key)
    predicted = str(exact_row["coarse_outcome"]) if exact_row else None
    return projection_certificate, predicted


def collect_replayed_seed_records(boundary: dict[tuple[int, int], dict[str, Any]]) -> dict[str, Any]:
    rng = random.Random(SAMPLE_SEED)
    target48 = target_template(SAMPLE_BITS)
    stats: Counter[str] = Counter()
    records: list[dict[str, Any]] = []

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
        observed = high_outcome(depth)
        projection_residue = residue % (1 << EXACT32_BITS)
        projection_certificate, predicted = prediction_for_projection(projection_residue, boundary)
        projection_key = key_for(projection_certificate)

        if projection_key != target_template(EXACT32_BITS):
            stats["projection_escape"] += 1
            seed_kind = "projection_escape"
        else:
            stats["projection_target"] += 1
            if predicted == observed:
                stats["boundary_prediction_match"] += 1
                seed_kind = "boundary_match"
            else:
                stats["boundary_prediction_mismatch"] += 1
                seed_kind = "boundary_mismatch"

        records.append(
            {
                "sample_index": sample_index,
                "seed_kind": seed_kind,
                "residue": residue,
                "low40_residue": residue & ((1 << CYLINDER_LOW_BITS) - 1),
                "projection32_residue": projection_residue,
                "projection32_template": (
                    stringify_key(projection_key) if projection_key else str(projection_certificate.get("status"))
                ),
                "predicted_exact32_outcome": predicted,
                "observed_48bit_outcome": observed,
                "matched_prefix_templates": int(depth.get("matched_prefix_templates", 0)),
                "first_failure": depth.get("first_failure"),
            }
        )

    return {
        "sample_bits": SAMPLE_BITS,
        "sample_seed": SAMPLE_SEED,
        "sample_count": SAMPLE_COUNT,
        "statistics": dict(sorted(stats.items())),
        "records": records,
    }


def selected_cylinder_seeds(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[int, dict[str, Any]] = {}
    by_kind: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_kind[str(record["seed_kind"])].append(record)

    ordered = [
        *by_kind.get("boundary_mismatch", []),
        *by_kind.get("boundary_match", []),
        *by_kind.get("projection_escape", [])[:MAX_PROJECTION_ESCAPE_CYLINDERS],
    ]
    for record in ordered:
        low40 = int(record["low40_residue"])
        existing = grouped.get(low40)
        if existing is None:
            grouped[low40] = {
                "low40_residue": low40,
                "seed_kinds": [record["seed_kind"]],
                "seed_examples": [record],
            }
            continue
        if record["seed_kind"] not in existing["seed_kinds"]:
            existing["seed_kinds"].append(record["seed_kind"])
        if len(existing["seed_examples"]) < 3:
            existing["seed_examples"].append(record)

    return list(grouped.values())


def cylinder_status(counts: Counter[str], outcome_counts: Counter[str]) -> str:
    if counts["start_template_match"] == 0:
        return "empty_start_template_cylinder"
    if counts["full_lasso_period_replay"] > 0:
        return "full_period_escape_found"
    if counts["projection_target"] == 0 and counts["projection_escape"] > 0:
        return "projection_escape_only_cylinder"
    if counts["projection_escape"] > 0 and counts["projection_target"] > 0:
        return "mixed_escape_and_target_cylinder"
    if counts["boundary_prediction_mismatch"] == counts["projection_target"]:
        return "uniform_boundary_mismatch_cylinder"
    if counts["boundary_prediction_match"] == counts["projection_target"]:
        return "uniform_boundary_match_cylinder"
    if len(outcome_counts) > 1:
        return "mixed_outcome_cylinder"
    return "mixed_prediction_cylinder"


def enumerate_low40_cylinder(
    seed: dict[str, Any],
    boundary: dict[tuple[int, int], dict[str, Any]],
) -> dict[str, Any]:
    low40 = int(seed["low40_residue"])
    target48 = target_template(SAMPLE_BITS)
    counts: Counter[str] = Counter()
    outcome_counts: Counter[str] = Counter()
    projection_template_counts: Counter[str] = Counter()
    mismatch_examples: list[dict[str, Any]] = []
    escape_examples: list[dict[str, Any]] = []

    for high_extension in range(1 << CYLINDER_EXTENSION_BITS):
        residue = low40 | (high_extension << CYLINDER_LOW_BITS)
        certificate = cert(residue, SAMPLE_BITS)
        key = key_for(certificate)
        if key != target48:
            counts["non_start_template_lift"] += 1
            continue

        counts["start_template_match"] += 1
        depth = lasso_prefix_depth_at(residue, SAMPLE_BITS)
        observed = high_outcome(depth)
        outcome_counts[observed] += 1
        if observed == "full_lasso_period_replay":
            counts["full_lasso_period_replay"] += 1

        projection_residue = residue % (1 << EXACT32_BITS)
        projection_certificate, predicted = prediction_for_projection(projection_residue, boundary)
        projection_key = key_for(projection_certificate)
        projection_template = stringify_key(projection_key) if projection_key else str(projection_certificate.get("status"))
        projection_template_counts[projection_template] += 1

        if projection_key != target_template(EXACT32_BITS):
            counts["projection_escape"] += 1
            if len(escape_examples) < EXAMPLE_LIMIT:
                escape_examples.append(
                    {
                        "residue": residue,
                        "high_extension": high_extension,
                        "projection32_residue": projection_residue,
                        "projection32_template": projection_template,
                        "observed_48bit_outcome": observed,
                        "matched_prefix_templates": int(depth.get("matched_prefix_templates", 0)),
                    }
                )
            continue

        counts["projection_target"] += 1
        if predicted == observed:
            counts["boundary_prediction_match"] += 1
        else:
            counts["boundary_prediction_mismatch"] += 1
            if len(mismatch_examples) < EXAMPLE_LIMIT:
                mismatch_examples.append(
                    {
                        "residue": residue,
                        "high_extension": high_extension,
                        "projection32_residue": projection_residue,
                        "predicted_exact32_outcome": predicted,
                        "observed_48bit_outcome": observed,
                        "matched_prefix_templates": int(depth.get("matched_prefix_templates", 0)),
                        "first_failure": depth.get("first_failure"),
                        "certificate": compact_certificate(certificate),
                    }
                )

    status = cylinder_status(counts, outcome_counts)
    return {
        "low40_residue": low40,
        "low32_projection": low40 & ((1 << EXACT32_BITS) - 1),
        "seed_kinds": sorted(seed.get("seed_kinds", [])),
        "seed_examples": seed.get("seed_examples", [])[:2],
        "tested_48bit_extensions": 1 << CYLINDER_EXTENSION_BITS,
        "statistics": dict(sorted(counts.items())),
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "projection32_template_counts": dict(projection_template_counts.most_common(8)),
        "status": status,
        "boundary_prediction_mismatch_examples": mismatch_examples,
        "projection_escape_examples": escape_examples,
    }


def collatz_attempt(ticket58: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket58["attempts"] if attempt["problem_id"] == "collatz")
    boundary_data = build_exact32_boundary()
    boundary = boundary_data["boundary"]
    replay = collect_replayed_seed_records(boundary)
    seeds = selected_cylinder_seeds(replay["records"])
    cylinders = [enumerate_low40_cylinder(seed, boundary) for seed in seeds]

    aggregate: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    for cylinder in cylinders:
        status_counts[str(cylinder["status"])] += 1
        aggregate["tested_48bit_extensions"] += int(cylinder["tested_48bit_extensions"])
        for key, value in cylinder.get("statistics", {}).items():
            aggregate[key] += int(value)

    mismatch_cylinders = [
        cylinder for cylinder in cylinders if "boundary_mismatch" in cylinder.get("seed_kinds", [])
    ]
    mixed_cylinders = [
        cylinder
        for cylinder in cylinders
        if cylinder.get("status") in {"mixed_prediction_cylinder", "mixed_outcome_cylinder", "mixed_escape_and_target_cylinder"}
    ]

    cylinder_cover = {
        "source_ticket": prior["ticket_id"],
        "family": FAMILY,
        "theorem_name": "SymbolicLiftMismatchCylinderOrCounted40BitCover",
        "cylinder_low_bits": CYLINDER_LOW_BITS,
        "cylinder_extension_bits": CYLINDER_EXTENSION_BITS,
        "selected_cylinder_count": len(cylinders),
        "selected_seed_policy": (
            "All replayed boundary-mismatch and boundary-match low40 cylinders are included; projection-escape "
            f"cylinders are capped at {MAX_PROJECTION_ESCAPE_CYLINDERS} because TICKET58 already counted 3,086 escapes."
        ),
        "replayed_sample_statistics": replay["statistics"],
        "aggregate_cylinder_statistics": dict(sorted(aggregate.items())),
        "cylinder_status_counts": dict(sorted(status_counts.items())),
        "boundary_mismatch_seed_cylinders": len(mismatch_cylinders),
        "boundary_mismatch_seed_cylinders_uniform": sum(
            1 for cylinder in mismatch_cylinders if cylinder.get("status") == "uniform_boundary_mismatch_cylinder"
        ),
        "mixed_or_unstable_cylinder_count": len(mixed_cylinders),
        "full_period_escape_count": aggregate.get("full_lasso_period_replay", 0),
        "representative_cylinders": cylinders[:16],
        "mismatch_cylinder_examples": [
            cylinder for cylinder in mismatch_cylinders[:EXAMPLE_LIMIT]
        ],
        "discarded_route": (
            "Treat one 48-bit mismatch as an isolated anecdote, or assume low40 cylinders are stable without "
            "enumerating their 48-bit extensions."
        ),
        "retained_route": (
            "Promote only counted low40 cylinder facts, then search for a symbolic rule explaining which cylinders "
            "are uniform mismatch, uniform match, projection escape, or mixed."
        ),
        "candidate_theorem": (
            "Every projection-target lift cylinder is either uniformly closed by the exact32 boundary prediction, "
            "uniformly refutes that prediction, or carries an explicit higher coordinate that separates the outcomes."
        ),
        "counterexample_target": (
            "A counted or symbolic cylinder with full-period replay, or a mixed cylinder that forces an additional "
            "coordinate not present in the current affine boundary."
        ),
        "proof_boundary": (
            "This is an exact enumeration of selected low40-to-48 cylinders induced by the TICKET58 replay, not an "
            "exhaustive 40-bit or 48-bit theorem. It can refute weaker lift shortcuts and guide the next symbolic "
            "theorem, but it does not prove Collatz and does not certify a Collatz counterexample."
        ),
    }

    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-59",
        "route": "SymbolicLiftMismatchCylinderOrCounted40BitCover",
        "status": "selected_cylinder_cover_open_no_resolution",
        "proof_or_counterexample_mode": "counted low40-to-48 cylinder audit",
        "attempt": (
            "Continue from TICKET58 by replaying the same deterministic 48-bit sample, extracting every "
            "projection-target mismatch cylinder seen at low40, and exhaustively enumerating its 256 possible "
            "48-bit extensions. This tests whether the mismatch is stable at cylinder scale or whether another "
            "coordinate is required."
        ),
        "bounded_result": {"selected_low40_cylinder_cover": cylinder_cover},
        "obstruction": (
            "The selected cylinder cover is stronger than a point sample but still does not cover the 527,682,754 "
            "40-bit valuation-word frontier or the 83,401,400,116 48-bit frontier."
        ),
        "candidate_theorem": cylinder_cover["candidate_theorem"],
        "next_experiment": (
            "Generate CO-TICKET-60 by learning a symbolic separator for the mixed/uniform cylinder statuses, or by "
            "expanding from selected low40 cylinders to an automaton-counted cover."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    cylinder_gate: str,
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
        "proof_or_counterexample_mode": "counted-cylinder transfer",
        "attempt": (
            "Transfer TICKET59's rule: after a finite boundary lift mismatch appears, group nearby lifted objects "
            "into counted cylinders before proposing an infinite theorem."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket59_transfer": route,
            "cylinder_gate": cylinder_gate,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "A proof candidate must show that every boundary cylinder is uniformly good, uniformly bad, or "
                "split by a named higher coordinate. Otherwise the finite boundary is under-specified."
            ),
        },
        "obstruction": (
            "This is a methodology transfer, not a solution. It blocks promotion of finite boundary evidence until "
            "the lifted cylinder family is counted or symbolically partitioned."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Define the problem-specific cylinder coordinates and search for a stable counter-cylinder.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket58 = read_json(ROOT / "data/open-problem/ticket58-affine-boundary-lift-lab.json")
    attempts = [
        transfer_attempt(
            ticket58,
            "riemann",
            "RH-TICKET-59",
            "ZeroKernelCountedLiftCylinder",
            "height-window zero-kernel cylinders must preserve the positivity boundary or expose an off-critical packet",
            (
                "Every zero-kernel lift cylinder is uniformly positive, uniformly escaping, or split by a named "
                "spectral coordinate with a strict rank."
            ),
            "a counted height cylinder where the positivity boundary prediction changes sign or stalls",
        ),
        collatz_attempt(ticket58),
        transfer_attempt(
            ticket58,
            "goldbach",
            "GB-TICKET-59",
            "GoldbachMarginCountedLiftCylinder",
            "residue/cutoff cylinders must preserve the positive-margin class or expose an exceptional packet",
            (
                "Every Goldbach residue-margin lift cylinder is uniformly positive, uniformly exceptional, or split "
                "by an explicit character/error coordinate."
            ),
            "a counted even-residue cylinder whose lower-bound margin changes sign under cutoff lift",
        ),
        transfer_attempt(
            ticket58,
            "twin-prime",
            "TP-TICKET-59",
            "TwinPrimeSieveCountedLiftCylinder",
            "sieve-level cylinders must preserve exact gap-2 retained mass or expose parity leakage",
            (
                "Every exact-gap sieve lift cylinder is uniformly gap-retaining, uniformly leaking, or split by a "
                "named parity/error coordinate."
            ),
            "a counted sieve cylinder where exact gap-2 mass is absorbed by a higher-level parity leak",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "symbolic_lift_mismatch_open_no_resolution",
        "claim_boundary": (
            "Ticket 59 turns the TICKET58 sampled lift mismatch into selected counted low40-to-48 cylinder audits "
            "and transfers the cylinder gate to RH, Goldbach, and Twin Prime. It does not prove or disprove any of "
            "the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket59-symbolic-lift-mismatch-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-59-counted-lift-cylinder.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-59-symbolic-lift-mismatch.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-59-counted-margin-cylinder.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-59-counted-sieve-cylinder.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
