from __future__ import annotations

import json
from collections import Counter, defaultdict
from typing import Any, Callable

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key
from ticket51_phase15_terminal_lift_lab import compact_certificate
from ticket52_frontier_budget_lab import SAMPLE_BITS, lasso_prefix_depth_at
from ticket58_affine_boundary_lift_lab import EXACT32_BITS, build_exact32_boundary, high_outcome, key_for
from ticket59_symbolic_lift_mismatch_lab import (
    CYLINDER_EXTENSION_BITS,
    CYLINDER_LOW_BITS,
    collect_replayed_seed_records,
    cylinder_status,
    prediction_for_projection,
    selected_cylinder_seeds,
    target_template,
)


GENERATED_AT = "2026-07-09T16:40:00+09:00"
SCHEMA = "primeproject.ticket60-mixed-cylinder-separator-lab.v1"
EXAMPLE_LIMIT = 8


Row = dict[str, Any]
KeyFn = Callable[[Row], tuple[Any, ...]]


def failure_signature(depth: dict[str, Any]) -> dict[str, Any]:
    failure = depth.get("first_failure") or {}
    certificate = failure.get("certificate") or {}
    return {
        "offset": failure.get("offset"),
        "bits": failure.get("bits"),
        "observed": failure.get("observed"),
        "next_valuation": certificate.get("next_valuation"),
        "tail4": list(certificate.get("tail_word", [])[-4:]),
        "prefix_length": certificate.get("prefix_length"),
        "consumed_bits": certificate.get("consumed_bits"),
    }


def enumerate_selected_start_rows(boundary: dict[tuple[int, int], dict[str, Any]]) -> dict[str, Any]:
    replay = collect_replayed_seed_records(boundary)
    seeds = selected_cylinder_seeds(replay["records"])
    target48 = target_template(SAMPLE_BITS)
    rows: list[Row] = []
    per_cylinder: dict[int, dict[str, Any]] = {}

    for seed in seeds:
        low40 = int(seed["low40_residue"])
        counts: Counter[str] = Counter()
        outcome_counts: Counter[str] = Counter()
        prediction_counts: Counter[str] = Counter()
        seed_kinds = sorted(str(kind) for kind in seed.get("seed_kinds", []))

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

            if projection_key != target_template(EXACT32_BITS):
                counts["projection_escape"] += 1
                prediction_label = "projection_escape"
            else:
                counts["projection_target"] += 1
                if predicted == observed:
                    counts["boundary_prediction_match"] += 1
                    prediction_label = "boundary_match"
                else:
                    counts["boundary_prediction_mismatch"] += 1
                    prediction_label = "boundary_mismatch"
            prediction_counts[prediction_label] += 1
            signature = failure_signature(depth)
            rows.append(
                {
                    "low40_residue": low40,
                    "low32_projection": projection_residue,
                    "high_extension": high_extension,
                    "residue": residue,
                    "seed_kinds": seed_kinds,
                    "outcome_label": observed,
                    "prediction_label": prediction_label,
                    "matched_prefix_templates": int(depth.get("matched_prefix_templates", 0)),
                    "failure_offset": signature["offset"],
                    "failure_observed": signature["observed"],
                    "failure_next_valuation": signature["next_valuation"],
                    "failure_tail4": signature["tail4"],
                    "failure_prefix_length": signature["prefix_length"],
                    "certificate_prefix_length": int(certificate.get("prefix_length", 0)),
                    "certificate_consumed_bits": int(certificate.get("consumed_bits", 0)),
                    "projection32_template": projection_template,
                    "predicted_exact32_outcome": predicted,
                }
            )

        status = cylinder_status(counts, outcome_counts)
        per_cylinder[low40] = {
            "low40_residue": low40,
            "seed_kinds": seed_kinds,
            "status": status,
            "statistics": dict(sorted(counts.items())),
            "outcome_counts": dict(sorted(outcome_counts.items())),
            "prediction_counts": dict(sorted(prediction_counts.items())),
        }

    return {
        "replayed_sample_statistics": replay["statistics"],
        "selected_seed_count": len(seeds),
        "rows": rows,
        "per_cylinder": per_cylinder,
    }


def assess_separator(
    rows: list[Row],
    label: str,
    key_fn: KeyFn,
    *,
    label_field: str,
    example_limit: int = EXAMPLE_LIMIT,
) -> dict[str, Any]:
    groups: dict[tuple[Any, ...], Counter[str]] = defaultdict(Counter)
    examples: dict[tuple[Any, ...], list[Row]] = defaultdict(list)
    for row in rows:
        key = key_fn(row)
        groups[key][str(row[label_field])] += 1
        if len(examples[key]) < 3:
            examples[key].append(row)

    collision_keys = [key for key, counts in groups.items() if len(counts) > 1]
    collision_examples = []
    for key in collision_keys[:example_limit]:
        collision_examples.append(
            {
                "state_key": json.dumps(key, ensure_ascii=False, separators=(",", ":")),
                "label_counts": dict(sorted(groups[key].items())),
                "examples": [
                    {
                        "low40_residue": row["low40_residue"],
                        "high_extension": row["high_extension"],
                        "outcome_label": row["outcome_label"],
                        "prediction_label": row["prediction_label"],
                        "failure_observed": row["failure_observed"],
                        "failure_next_valuation": row["failure_next_valuation"],
                    }
                    for row in examples[key]
                ],
            }
        )

    return {
        "separator": label,
        "label_field": label_field,
        "row_count": len(rows),
        "state_count": len(groups),
        "collision_group_count": len(collision_keys),
        "ambiguous_row_count": sum(sum(groups[key].values()) for key in collision_keys),
        "largest_state_size": max((sum(counts.values()) for counts in groups.values()), default=0),
        "max_labels_per_state": max((len(counts) for counts in groups.values()), default=0),
        "deterministic": len(collision_keys) == 0,
        "collision_examples": collision_examples,
    }


def candidate_separators() -> list[tuple[str, KeyFn]]:
    candidates: list[tuple[str, KeyFn]] = [
        ("low40_only", lambda row: (row["low40_residue"],)),
        ("low40_plus_projection32_template", lambda row: (row["low40_residue"], row["projection32_template"])),
        ("low40_plus_certificate_prefix_length", lambda row: (row["low40_residue"], row["certificate_prefix_length"])),
        ("low40_plus_failure_offset", lambda row: (row["low40_residue"], row["failure_offset"])),
        (
            "low40_plus_failure_offset_next_valuation",
            lambda row: (row["low40_residue"], row["failure_offset"], row["failure_next_valuation"]),
        ),
        ("low40_plus_failure_observed_template", lambda row: (row["low40_residue"], row["failure_observed"])),
    ]
    for bits in range(1, CYLINDER_EXTENSION_BITS + 1):
        mask = (1 << bits) - 1
        candidates.append(
            (
                f"low40_plus_high_extension_mod_2^{bits}",
                lambda row, mask=mask, bits=bits: (row["low40_residue"], bits, row["high_extension"] & mask),
            )
        )
    for bits in range(1, CYLINDER_EXTENSION_BITS + 1):
        shift = CYLINDER_EXTENSION_BITS - bits
        candidates.append(
            (
                f"low40_plus_high_extension_top_{bits}_bits",
                lambda row, shift=shift, bits=bits: (row["low40_residue"], bits, row["high_extension"] >> shift),
            )
        )
    return candidates


def separator_ladder(rows: list[Row]) -> dict[str, Any]:
    candidates = candidate_separators()
    outcome_ladder = [
        assess_separator(rows, label, key_fn, label_field="outcome_label")
        for label, key_fn in candidates
    ]
    prediction_ladder = [
        assess_separator(rows, label, key_fn, label_field="prediction_label")
        for label, key_fn in candidates
    ]
    first_outcome = next((row for row in outcome_ladder if row["deterministic"]), None)
    first_prediction = next((row for row in prediction_ladder if row["deterministic"]), None)
    strict_candidates = []
    for (label, _), outcome, prediction in zip(candidates, outcome_ladder, prediction_ladder):
        if outcome["deterministic"] and prediction["deterministic"]:
            strict_candidates.append(
                {
                    "separator": label,
                    "outcome_state_count": outcome["state_count"],
                    "prediction_state_count": prediction["state_count"],
                }
            )
    return {
        "row_count": len(rows),
        "outcome_ladder": outcome_ladder,
        "prediction_ladder": prediction_ladder,
        "first_outcome_deterministic_separator": first_outcome["separator"] if first_outcome else None,
        "first_prediction_deterministic_separator": first_prediction["separator"] if first_prediction else None,
        "first_joint_deterministic_separator": strict_candidates[0]["separator"] if strict_candidates else None,
        "joint_deterministic_candidates": strict_candidates[:8],
    }


def collatz_attempt(ticket59: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket59["attempts"] if attempt["problem_id"] == "collatz")
    boundary_data = build_exact32_boundary()
    rich = enumerate_selected_start_rows(boundary_data["boundary"])
    per_cylinder = rich["per_cylinder"]
    rows = rich["rows"]
    mixed_low40 = {
        low40
        for low40, cylinder in per_cylinder.items()
        if cylinder.get("status") in {"mixed_outcome_cylinder", "mixed_prediction_cylinder", "mixed_escape_and_target_cylinder"}
    }
    mixed_rows = [row for row in rows if int(row["low40_residue"]) in mixed_low40]
    all_ladder = separator_ladder(rows)
    mixed_ladder = separator_ladder(mixed_rows)
    status_counts = Counter(str(cylinder.get("status")) for cylinder in per_cylinder.values())
    outcome_counts = Counter(str(row["outcome_label"]) for row in rows)
    prediction_counts = Counter(str(row["prediction_label"]) for row in rows)
    mixed_examples = [
        per_cylinder[low40]
        for low40 in sorted(mixed_low40)[:EXAMPLE_LIMIT]
    ]

    audit = {
        "source_ticket": prior["ticket_id"],
        "theorem_name": "MixedCylinderSeparatorOrAutomatonCountedCover",
        "selected_low40_cylinder_count": len(per_cylinder),
        "selected_start_template_lift_count": len(rows),
        "mixed_cylinder_count": len(mixed_low40),
        "mixed_start_template_lift_count": len(mixed_rows),
        "cylinder_status_counts": dict(sorted(status_counts.items())),
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "prediction_counts": dict(sorted(prediction_counts.items())),
        "separator_scope": {
            "low_bits": CYLINDER_LOW_BITS,
            "extension_bits": CYLINDER_EXTENSION_BITS,
            "replayed_sample_statistics": rich["replayed_sample_statistics"],
        },
        "all_selected_separator_ladder": all_ladder,
        "mixed_cylinder_separator_ladder": mixed_ladder,
        "mixed_cylinder_examples": mixed_examples,
        "discarded_route": (
            "Assume low40 cylinder identity is enough to classify higher-bit outcomes. TICKET60 rejects this because "
            "58 selected cylinders remain mixed under low40 alone."
        ),
        "retained_route": (
            "Use the first deterministic separator as a candidate symbolic coordinate, then prove that coordinate "
            "is computable and well-founded under lift transitions instead of replay-derived."
        ),
        "candidate_theorem": (
            "Every mixed low40 cylinder is separated by a bounded higher-coordinate signature, and that signature "
            "extends to an automaton-counted cover with no full-period nondecreasing cycle."
        ),
        "counterexample_target": (
            "A mixed cylinder whose ambiguity survives every bounded separator short of exact high-extension identity, "
            "or a full-period replay inside a separated cylinder."
        ),
        "proof_boundary": (
            "This separator audit is still finite and replay-derived. It can name missing coordinates and refute "
            "under-specified boundary proofs, but it does not prove Collatz and does not certify a Collatz counterexample."
        ),
    }
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-60",
        "route": "MixedCylinderSeparatorOrAutomatonCountedCover",
        "status": "mixed_cylinder_separator_open_no_resolution",
        "proof_or_counterexample_mode": "separator ladder over counted low40-to-48 cylinders",
        "attempt": (
            "Continue from TICKET59 by testing candidate coordinates that split the 58 mixed low40 cylinders. "
            "The goal is not more sampling; it is to identify the smallest coordinate family that makes the selected "
            "lift outcomes deterministic enough to become a symbolic theorem target."
        ),
        "bounded_result": {"mixed_cylinder_separator_audit": audit},
        "obstruction": (
            "Any separator that depends on replaying to the first failure is diagnostic, not yet a non-circular proof. "
            "It must be replaced by a symbolic transition theorem or an automaton-counted cover."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": (
            "Generate CO-TICKET-61 by proving the retained separator symbolically or by converting it into an "
            "automaton-counted cover over a larger cylinder family."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    separator_gate: str,
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
        "proof_or_counterexample_mode": "separator-ladder transfer",
        "attempt": (
            "Transfer TICKET60's rule: when a finite boundary cylinder remains mixed, do not promote it. "
            "Search for a named separator coordinate and then prove that coordinate symbolically."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket60_transfer": route,
            "separator_gate": separator_gate,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "A mixed finite cylinder is either evidence for a missing coordinate or a counterexample target. "
                "It is never a proof until a symbolic separator and infinite bridge are supplied."
            ),
        },
        "obstruction": (
            "This is a proof-discipline transfer, not a solution. It prevents finite mixed evidence from being "
            "misread as an infinite theorem."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Build the problem-specific separator ladder and reject any route that leaves mixed cylinders unexplained.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket59 = read_json(ROOT / "data/open-problem/ticket59-symbolic-lift-mismatch-lab.json")
    attempts = [
        transfer_attempt(
            ticket59,
            "riemann",
            "RH-TICKET-60",
            "ZeroKernelMixedCylinderSeparator",
            "mixed height-window zero-kernel cylinders need a spectral separator before positivity can be promoted",
            (
                "Every mixed zero-kernel lift cylinder is split by a named spectral coordinate with a strict "
                "positivity rank, or yields an off-critical escape packet."
            ),
            "a zero-kernel cylinder whose positivity ambiguity survives every tested separator",
        ),
        collatz_attempt(ticket59),
        transfer_attempt(
            ticket59,
            "goldbach",
            "GB-TICKET-60",
            "GoldbachMixedMarginSeparator",
            "mixed residue/cutoff margin cylinders need a character/error separator before a lower bound can be promoted",
            (
                "Every mixed Goldbach margin cylinder is split by an explicit character or error-budget coordinate, "
                "or yields a cutoff-stable exceptional packet."
            ),
            "a residue/cutoff cylinder whose positive-margin ambiguity survives every tested separator",
        ),
        transfer_attempt(
            ticket59,
            "twin-prime",
            "TP-TICKET-60",
            "TwinPrimeMixedSieveSeparator",
            "mixed exact-gap sieve cylinders need a parity/error separator before gap-2 mass can be promoted",
            (
                "Every mixed exact-gap sieve cylinder is split by an explicit parity-leakage coordinate, or yields "
                "a stable exact-gap mass leak."
            ),
            "a sieve cylinder whose exact gap-2 mass ambiguity survives every tested separator",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "mixed_cylinder_separator_open_no_resolution",
        "claim_boundary": (
            "Ticket 60 searches for separator coordinates for the mixed TICKET59 cylinders and transfers that "
            "discipline to RH, Goldbach, and Twin Prime. It does not prove or disprove any of the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket60-mixed-cylinder-separator-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-60-mixed-cylinder-separator.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-60-mixed-cylinder-separator.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-60-mixed-margin-separator.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-60-mixed-sieve-separator.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
