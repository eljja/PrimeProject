from __future__ import annotations

import json
from collections import Counter, defaultdict
from typing import Any, Callable

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key
from ticket52_frontier_budget_lab import SAMPLE_BITS, lasso_prefix_depth_at
from ticket58_affine_boundary_lift_lab import EXACT32_BITS, build_exact32_boundary, high_outcome, key_for
from ticket59_symbolic_lift_mismatch_lab import (
    CYLINDER_LOW_BITS,
    prediction_for_projection,
    target_template,
)
from ticket60_mixed_cylinder_separator_lab import (
    Row,
    assess_separator,
    enumerate_selected_start_rows,
    failure_signature,
)


GENERATED_AT = "2026-07-09T18:30:00+09:00"
SCHEMA = "primeproject.ticket62-mod16-transition-cover-lab.v1"
EXTRA_BITS_TO_TEST = (4, 8)
LABEL_FIELDS = ("failure_offset", "outcome_label", "prediction_label", "transition_label")


KeyFn = Callable[[Row], tuple[Any, ...]]


def mixed_base_rows(boundary: dict[tuple[int, int], dict[str, Any]]) -> dict[str, Any]:
    rich = enumerate_selected_start_rows(boundary)
    per_cylinder = rich["per_cylinder"]
    mixed_low40 = {
        low40
        for low40, cylinder in per_cylinder.items()
        if cylinder.get("status") in {"mixed_outcome_cylinder", "mixed_prediction_cylinder", "mixed_escape_and_target_cylinder"}
    }
    rows = [row for row in rich["rows"] if int(row["low40_residue"]) in mixed_low40]
    return {
        "rich": rich,
        "mixed_low40": mixed_low40,
        "mixed_rows": rows,
    }


def lifted_rows_for_bits(
    base_rows: list[Row],
    bits: int,
    boundary: dict[tuple[int, int], dict[str, Any]],
) -> dict[str, Any]:
    extra_bits = bits - SAMPLE_BITS
    target = target_template(bits)
    rows: list[Row] = []
    stats: Counter[str] = Counter()
    base_extension_counts: Counter[tuple[int, int]] = Counter()
    full_period_examples: list[dict[str, Any]] = []

    for base in base_rows:
        low40 = int(base["low40_residue"])
        base_high8 = int(base["high_extension"])
        base_mod16 = base_high8 & 0x0F
        base_key = (low40, base_high8)
        for top_extension in range(1 << extra_bits):
            stats["tested_lifts"] += 1
            residue = int(base["residue"]) | (top_extension << SAMPLE_BITS)
            certificate = cert(residue, bits)
            key = key_for(certificate)
            if key != target:
                stats["non_start_template_lift"] += 1
                continue

            stats["start_template_lift"] += 1
            base_extension_counts[base_key] += 1
            depth = lasso_prefix_depth_at(residue, bits)
            observed = high_outcome(depth)
            if observed == "full_lasso_period_replay":
                stats["full_lasso_period_replay"] += 1
                if len(full_period_examples) < 8:
                    full_period_examples.append(
                        {
                            "bits": bits,
                            "residue": residue,
                            "low40_residue": low40,
                            "base_high_extension": base_high8,
                            "top_extension": top_extension,
                            "matched_prefix_templates": int(depth.get("matched_prefix_templates", 0)),
                        }
                    )

            projection_residue = residue % (1 << EXACT32_BITS)
            projection_certificate, predicted = prediction_for_projection(projection_residue, boundary)
            projection_key = key_for(projection_certificate)
            projection_template = stringify_key(projection_key) if projection_key else str(projection_certificate.get("status"))
            if projection_key != target_template(EXACT32_BITS):
                stats["projection_escape"] += 1
                prediction_label = "projection_escape"
            else:
                stats["projection_target"] += 1
                if predicted == observed:
                    stats["boundary_prediction_match"] += 1
                    prediction_label = "boundary_match"
                else:
                    stats["boundary_prediction_mismatch"] += 1
                    prediction_label = "boundary_mismatch"

            signature = failure_signature(depth)
            total_high_extension = residue >> CYLINDER_LOW_BITS
            rows.append(
                {
                    "bits": bits,
                    "extra_bits": extra_bits,
                    "low40_residue": low40,
                    "low32_projection": projection_residue,
                    "base_high_extension": base_high8,
                    "base_mod16": base_mod16,
                    "high_extension": total_high_extension,
                    "top_extension": top_extension,
                    "residue": residue,
                    "base_outcome_label": base["outcome_label"],
                    "base_prediction_label": base["prediction_label"],
                    "base_failure_offset": base["failure_offset"],
                    "outcome_label": observed,
                    "prediction_label": prediction_label,
                    "transition_label": f"{base['failure_offset']}->{signature['offset']}",
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

    return {
        "bits": bits,
        "extra_bits": extra_bits,
        "rows": rows,
        "statistics": dict(sorted(stats.items())),
        "base_rows_with_start_template_extension": len(base_extension_counts),
        "base_extension_count_distribution": dict(sorted(Counter(base_extension_counts.values()).items())),
        "full_period_examples": full_period_examples,
    }


def transition_candidates(total_extension_bits: int) -> list[tuple[str, KeyFn]]:
    candidates: list[tuple[str, KeyFn]] = [
        ("low40_plus_base_mod16", lambda row: (row["low40_residue"], row["base_mod16"])),
        ("low40_plus_base_high8", lambda row: (row["low40_residue"], row["base_high_extension"])),
    ]
    for bits in range(4, total_extension_bits + 1):
        mask = (1 << bits) - 1
        candidates.append(
            (
                f"low40_plus_extended_high_mod_2^{bits}",
                lambda row, mask=mask, bits=bits: (row["low40_residue"], bits, row["high_extension"] & mask),
            )
        )
    for bits in range(1, total_extension_bits + 1):
        shift = total_extension_bits - bits
        candidates.append(
            (
                f"low40_plus_extended_high_top_{bits}_bits",
                lambda row, shift=shift, bits=bits: (row["low40_residue"], bits, row["high_extension"] >> shift),
            )
        )
    return candidates


def joint_transition_ladder(rows: list[Row], *, total_extension_bits: int) -> dict[str, Any]:
    candidates = transition_candidates(total_extension_bits)
    ladders = {
        field: [
            assess_separator(rows, label, key_fn, label_field=field)
            for label, key_fn in candidates
        ]
        for field in LABEL_FIELDS
    }
    joint_rows = []
    for index, (label, _) in enumerate(candidates):
        joint_rows.append(
            {
                "separator": label,
                "row_count": len(rows),
                "state_count": ladders["failure_offset"][index]["state_count"],
                "deterministic_for_all_labels": all(ladders[field][index]["deterministic"] for field in LABEL_FIELDS),
                "collision_groups": {
                    field: ladders[field][index]["collision_group_count"]
                    for field in LABEL_FIELDS
                },
                "ambiguous_rows": {
                    field: ladders[field][index]["ambiguous_row_count"]
                    for field in LABEL_FIELDS
                },
            }
        )
    first_joint = next((row for row in joint_rows if row["deterministic_for_all_labels"]), None)
    base_mod16 = next(row for row in joint_rows if row["separator"] == "low40_plus_base_mod16")
    base_high8 = next(row for row in joint_rows if row["separator"] == "low40_plus_base_high8")
    return {
        "row_count": len(rows),
        "label_ladders": ladders,
        "joint_ladder": joint_rows,
        "base_mod16_joint_row": base_mod16,
        "base_high8_joint_row": base_high8,
        "first_joint_deterministic_separator": first_joint["separator"] if first_joint else None,
    }


def summarize_lift_audit(base_rows: list[Row], boundary: dict[tuple[int, int], dict[str, Any]]) -> list[dict[str, Any]]:
    audits = []
    for extra_bits in EXTRA_BITS_TO_TEST:
        bits = SAMPLE_BITS + extra_bits
        lifted = lifted_rows_for_bits(base_rows, bits, boundary)
        rows = lifted["rows"]
        total_extension_bits = bits - CYLINDER_LOW_BITS
        ladder = joint_transition_ladder(rows, total_extension_bits=total_extension_bits)
        mod16 = ladder["base_mod16_joint_row"]
        base_high8 = ladder["base_high8_joint_row"]
        status = (
            "mod16_lift_obstruction_found"
            if mod16["collision_groups"]["failure_offset"] > 0
            else "mod16_transition_survives_bounded_lift"
        )
        audits.append(
            {
                "bits": bits,
                "extra_bits": extra_bits,
                "status": status,
                "statistics": lifted["statistics"],
                "base_rows_with_start_template_extension": lifted["base_rows_with_start_template_extension"],
                "base_extension_count_distribution": lifted["base_extension_count_distribution"],
                "base_mod16_joint_row": mod16,
                "base_high8_joint_row": base_high8,
                "first_joint_deterministic_separator": ladder["first_joint_deterministic_separator"],
                "joint_ladder": ladder["joint_ladder"][:16],
                "failure_offset_ladder": ladder["label_ladders"]["failure_offset"][:16],
                "full_period_examples": lifted["full_period_examples"],
            }
        )
    return audits


def collatz_attempt(ticket61: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket61["attempts"] if attempt["problem_id"] == "collatz")
    boundary_data = build_exact32_boundary()
    base = mixed_base_rows(boundary_data["boundary"])
    base_rows = base["mixed_rows"]
    lift_audits = summarize_lift_audit(base_rows, boundary_data["boundary"])
    obstruction_audits = [
        audit for audit in lift_audits if audit["status"] == "mod16_lift_obstruction_found"
    ]
    full_period_count = sum(int(audit["statistics"].get("full_lasso_period_replay", 0)) for audit in lift_audits)
    aggregate_status = (
        "mod16_lift_obstruction_open_no_resolution"
        if obstruction_audits
        else "bounded_mod16_transition_survives_open_no_resolution"
    )
    audit = {
        "source_ticket": prior["ticket_id"],
        "theorem_name": "Mod16FailureOffsetTransitionOrAutomatonCountedCover",
        "base_bits": SAMPLE_BITS,
        "base_mixed_cylinder_count": len(base["mixed_low40"]),
        "base_mixed_start_template_lift_count": len(base_rows),
        "tested_lift_bits": [audit["bits"] for audit in lift_audits],
        "lift_audits": lift_audits,
        "obstruction_count": len(obstruction_audits),
        "full_period_escape_count": full_period_count,
        "discarded_route": (
            "Promote TICKET61's mod16 separator directly to an infinite theorem without checking higher-bit lift "
            "closure. TICKET62 treats that as an unproved shortcut."
        ),
        "retained_route": (
            "Treat mod16 as a candidate state coordinate and test whether larger start-template lifts preserve "
            "deterministic failure-offset transitions. A collision becomes a theorem-obstruction witness; no "
            "collision becomes bounded evidence for a transition table, not a proof."
        ),
        "candidate_theorem": (
            "For every mixed low40 cylinder and every admissible higher lift, the low40 plus high-extension "
            "mod16 state either determines a closed failure-offset transition or enters a finite automaton cover "
            "with no full-period nondecreasing cycle."
        ),
        "counterexample_target": (
            "A higher start-template lift where low40 plus base mod16 admits two different failure offsets, "
            "or a full-period replay inside the tested lift family."
        ),
        "next_theorem_target": (
            "Mod16AutomatonCoverOrLiftCollision"
            if not obstruction_audits
            else "LiftCollisionRefinementOrNewCoordinate"
        ),
        "proof_boundary": (
            "This is a bounded lift-transition audit over selected mixed cylinders. It can refute a naive "
            "mod16 transition theorem or name the next automaton cover target, but it does not prove Collatz "
            "and does not certify a Collatz counterexample."
        ),
    }
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-62",
        "route": "Mod16FailureOffsetTransitionOrAutomatonCountedCover",
        "status": aggregate_status,
        "proof_or_counterexample_mode": "bounded higher-lift transition audit",
        "attempt": (
            "Continue from TICKET61 by lifting the selected mixed 48-bit start-template rows to 52 and 56 bits, "
            "then testing whether the pre-replay mod16 separator remains deterministic under those lifts."
        ),
        "bounded_result": {"mod16_transition_cover_audit": audit},
        "obstruction": (
            "Even when a finite lift audit survives, it is not an infinite transition theorem. If a collision "
            "appears, it refutes only the naive mod16 theorem and points to a new coordinate; it is not a Collatz "
            "counterexample unless it becomes a full-period nondecreasing orbit."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": (
            "Generate CO-TICKET-63 by either proving the retained transition table symbolically or adding the "
            "smallest new coordinate required by the first lift collision."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    transition_gate: str,
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
        "proof_or_counterexample_mode": "symbolic-transition transfer",
        "attempt": (
            "Transfer TICKET62's rule: after a pre-replay separator is found, the next proof obligation is a "
            "lift-stable transition law or an explicit collision witness, not another diagnostic separator."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket62_transfer": route,
            "transition_gate": transition_gate,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "A separator can support proof only if the lift/height/cutoff transition is closed in the same "
                "coordinates or every failure is promoted to a named obstruction."
            ),
        },
        "obstruction": (
            "This is a methodological transfer and does not solve the target problem. It raises the acceptance "
            "bar from finite separation to transition closure."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Construct the problem-specific transition table or report the first collision witness.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket61 = read_json(ROOT / "data/open-problem/ticket61-symbolic-failure-offset-lab.json")
    attempts = [
        transfer_attempt(
            ticket61,
            "riemann",
            "RH-TICKET-62",
            "ZeroKernelSeparatorTransitionClosure",
            "pre-replay spectral separator must be closed under height-window lift",
            (
                "Every pre-replay zero-kernel separator state has a closed positivity transition law, or yields "
                "an off-critical collision packet."
            ),
            "a height lift whose zero-kernel positivity label collides inside the same symbolic separator state",
        ),
        collatz_attempt(ticket61),
        transfer_attempt(
            ticket61,
            "goldbach",
            "GB-TICKET-62",
            "GoldbachMarginTransitionClosure",
            "pre-replay margin separator must be closed under cutoff lift",
            (
                "Every Goldbach margin separator state has a closed cutoff transition law, or yields a stable "
                "exceptional residue packet."
            ),
            "a cutoff lift whose positive-margin label collides inside the same character/error separator state",
        ),
        transfer_attempt(
            ticket61,
            "twin-prime",
            "TP-TICKET-62",
            "TwinPrimeSieveTransitionClosure",
            "pre-replay exact-gap separator must be closed under sieve-level lift",
            (
                "Every twin-prime sieve separator state has a closed retained-mass transition law, or yields a "
                "stable exact-gap mass leak."
            ),
            "a sieve-level lift whose exact-gap label collides inside the same parity/error separator state",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "mod16_transition_cover_open_no_resolution",
        "claim_boundary": (
            "Ticket 62 tests whether TICKET61's pre-replay mod16 separator behaves like a lift-transition "
            "coordinate and transfers that discipline to RH, Goldbach, and Twin Prime. It does not prove or "
            "disprove any of the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket62-mod16-transition-cover-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-62-transition-closure.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-62-mod16-transition-cover.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-62-margin-transition.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-62-sieve-transition.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
