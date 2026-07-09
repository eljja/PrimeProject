from __future__ import annotations

import json
from collections import Counter
from typing import Any, Callable

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket59_symbolic_lift_mismatch_lab import CYLINDER_EXTENSION_BITS, CYLINDER_LOW_BITS
from ticket58_affine_boundary_lift_lab import build_exact32_boundary
from ticket60_mixed_cylinder_separator_lab import (
    Row,
    assess_separator,
    enumerate_selected_start_rows,
)


GENERATED_AT = "2026-07-09T17:35:00+09:00"
SCHEMA = "primeproject.ticket61-symbolic-failure-offset-lab.v1"


KeyFn = Callable[[Row], tuple[Any, ...]]
LABEL_FIELDS = ("failure_offset", "outcome_label", "prediction_label")


def pre_replay_candidate_separators() -> list[tuple[str, KeyFn]]:
    candidates: list[tuple[str, KeyFn]] = [
        ("low40_only", lambda row: (row["low40_residue"],)),
        (
            "low40_plus_certificate_prefix_length",
            lambda row: (row["low40_residue"], row["certificate_prefix_length"]),
        ),
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
    candidates.append(
        (
            "low40_plus_high_extension_mod_2^4_certificate_prefix_length",
            lambda row: (
                row["low40_residue"],
                row["high_extension"] & 0x0F,
                row["certificate_prefix_length"],
            ),
        )
    )
    return candidates


def label_ladder(rows: list[Row], *, label_field: str) -> list[dict[str, Any]]:
    return [
        assess_separator(rows, label, key_fn, label_field=label_field)
        for label, key_fn in pre_replay_candidate_separators()
    ]


def joint_ladder(rows: list[Row]) -> dict[str, Any]:
    candidates = pre_replay_candidate_separators()
    ladders = {
        label_field: [
            assess_separator(rows, label, key_fn, label_field=label_field)
            for label, key_fn in candidates
        ]
        for label_field in LABEL_FIELDS
    }
    joint_rows: list[dict[str, Any]] = []
    for index, (label, _) in enumerate(candidates):
        row = {
            "separator": label,
            "row_count": len(rows),
            "deterministic_for_all_labels": all(ladders[field][index]["deterministic"] for field in LABEL_FIELDS),
            "state_count": ladders[LABEL_FIELDS[0]][index]["state_count"],
            "collision_groups": {
                field: ladders[field][index]["collision_group_count"]
                for field in LABEL_FIELDS
            },
            "ambiguous_rows": {
                field: ladders[field][index]["ambiguous_row_count"]
                for field in LABEL_FIELDS
            },
        }
        joint_rows.append(row)
    first_joint = next((row for row in joint_rows if row["deterministic_for_all_labels"]), None)
    first_failure = next((row for row in ladders["failure_offset"] if row["deterministic"]), None)
    first_outcome = next((row for row in ladders["outcome_label"] if row["deterministic"]), None)
    first_prediction = next((row for row in ladders["prediction_label"] if row["deterministic"]), None)
    first_top_joint = next(
        (
            row
            for row in joint_rows
            if row["deterministic_for_all_labels"] and "_top_" in row["separator"]
        ),
        None,
    )
    return {
        "row_count": len(rows),
        "failure_offset_ladder": ladders["failure_offset"],
        "outcome_ladder": ladders["outcome_label"],
        "prediction_ladder": ladders["prediction_label"],
        "joint_ladder": joint_rows,
        "first_failure_offset_deterministic_separator": first_failure["separator"] if first_failure else None,
        "first_outcome_deterministic_separator": first_outcome["separator"] if first_outcome else None,
        "first_prediction_deterministic_separator": first_prediction["separator"] if first_prediction else None,
        "first_joint_deterministic_separator": first_joint["separator"] if first_joint else None,
        "first_top_bit_joint_deterministic_separator": first_top_joint["separator"] if first_top_joint else None,
    }


def collatz_attempt(ticket60: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket60["attempts"] if attempt["problem_id"] == "collatz")
    prior_audit = prior.get("bounded_result", {}).get("mixed_cylinder_separator_audit", {})
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
    all_ladder = joint_ladder(rows)
    mixed_ladder = joint_ladder(mixed_rows)
    status_counts = Counter(str(cylinder.get("status")) for cylinder in per_cylinder.values())
    failure_counts = Counter(str(row["failure_offset"]) for row in rows)
    mixed_failure_counts = Counter(str(row["failure_offset"]) for row in mixed_rows)
    mod16_mixed = next(
        row
        for row in mixed_ladder["joint_ladder"]
        if row["separator"] == "low40_plus_high_extension_mod_2^4"
    )
    top6_mixed = next(
        row
        for row in mixed_ladder["joint_ladder"]
        if row["separator"] == "low40_plus_high_extension_top_6_bits"
    )

    audit = {
        "source_ticket": prior["ticket_id"],
        "source_replay_separator": prior_audit.get("mixed_cylinder_separator_ladder", {}).get(
            "first_joint_deterministic_separator"
        ),
        "theorem_name": "SymbolicFailureOffsetPredictorOrCountedCover",
        "selected_low40_cylinder_count": len(per_cylinder),
        "selected_start_template_lift_count": len(rows),
        "mixed_cylinder_count": len(mixed_low40),
        "mixed_start_template_lift_count": len(mixed_rows),
        "cylinder_status_counts": dict(sorted(status_counts.items())),
        "failure_offset_counts": dict(sorted(failure_counts.items())),
        "mixed_failure_offset_counts": dict(sorted(mixed_failure_counts.items())),
        "separator_scope": {
            "low_bits": CYLINDER_LOW_BITS,
            "extension_bits": CYLINDER_EXTENSION_BITS,
            "pre_replay_key_rule": (
                "Keys may use low40 cylinder identity, certificate prefix length, and high-extension bits. "
                "They may not use replay-derived failure_offset, failure_observed, or first_failure certificate data."
            ),
            "replayed_sample_statistics": rich["replayed_sample_statistics"],
        },
        "all_selected_pre_replay_separator_ladder": all_ladder,
        "mixed_pre_replay_separator_ladder": mixed_ladder,
        "mod16_mixed_joint_row": mod16_mixed,
        "top6_mixed_joint_row": top6_mixed,
        "discarded_route": (
            "Use low40+failure_offset from TICKET60 as if it were a proof coordinate. That is circular because "
            "failure_offset is learned only after replaying the trajectory to failure."
        ),
        "retained_route": (
            "Replace the replay-derived coordinate with a pre-replay symbolic coordinate. In the selected data, "
            "low40 plus high_extension modulo 16 already determines failure_offset, outcome, and boundary-match "
            "status for every mixed start-template lift."
        ),
        "candidate_theorem": (
            "For every selected mixed low40 cylinder, the mod-16 high-extension residue determines the first "
            "failure offset and the boundary prediction label; extend this to a symbolic transition theorem or "
            "an automaton-counted cover that excludes full-period nondecreasing cycles."
        ),
        "counterexample_target": (
            "A selected or newly lifted mixed cylinder whose failure_offset remains ambiguous under low40 plus "
            "high_extension mod 16, or a full-period replay inside a mod-16-separated cylinder."
        ),
        "next_theorem_target": "Mod16FailureOffsetTransitionOrAutomatonCountedCover",
        "proof_boundary": (
            "This is finite selected-cylinder evidence. It removes one replay-derived separator from the immediate "
            "candidate route, but it does not prove Collatz and does not certify a Collatz counterexample."
        ),
    }
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-61",
        "route": "SymbolicFailureOffsetPredictorOrCountedCover",
        "status": "symbolic_failure_offset_open_no_resolution",
        "proof_or_counterexample_mode": "pre-replay separator audit over selected mixed cylinders",
        "attempt": (
            "Continue from TICKET60 by forbidding replay-derived separator keys and asking whether a pre-replay "
            "higher-bit coordinate predicts the failure offset that previously separated the mixed cylinders."
        ),
        "bounded_result": {"symbolic_failure_offset_audit": audit},
        "obstruction": (
            "The mod-16 separator is still an empirical coordinate on a selected finite cover. It becomes proof "
            "material only if a symbolic transition theorem proves that the coordinate is complete under lifts "
            "and decreases or enters a counted terminal cover."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": (
            "Generate CO-TICKET-62 by deriving the mod-16 high-extension transition table symbolically, then "
            "testing whether it closes under larger cylinder lifts or exposes an ambiguous lift."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    symbolic_gate: str,
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
        "proof_or_counterexample_mode": "pre-replay separator transfer",
        "attempt": (
            "Transfer TICKET61's stricter rule: a separator that is discovered after replay is not a proof "
            "coordinate. Replace it with a pre-observable symbolic coordinate, or promote the failure to a "
            "counterexample search target."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket61_transfer": route,
            "symbolic_gate": symbolic_gate,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "A finite separator is useful only when its key is available before replay and has a symbolic "
                "transition law. Otherwise it remains a diagnostic coordinate, not a proof bridge."
            ),
        },
        "obstruction": (
            "This is a proof-discipline transfer and does not solve the target problem. It upgrades the next "
            "experiment from diagnostic separation to symbolic transition closure."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Build the problem-specific pre-replay separator table and test symbolic transition closure.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket60 = read_json(ROOT / "data/open-problem/ticket60-mixed-cylinder-separator-lab.json")
    attempts = [
        transfer_attempt(
            ticket60,
            "riemann",
            "RH-TICKET-61",
            "ZeroKernelSymbolicSeparatorTransition",
            "spectral separator keys must be defined before zero-kernel replay or height-window evaluation",
            (
                "Every mixed zero-kernel lift cylinder has a pre-replay spectral coordinate with a closed "
                "positivity transition law, or yields an off-critical packet with stable sign obstruction."
            ),
            "a zero-kernel cylinder whose positivity ambiguity survives all pre-replay symbolic separator keys",
        ),
        collatz_attempt(ticket60),
        transfer_attempt(
            ticket60,
            "goldbach",
            "GB-TICKET-61",
            "GoldbachSymbolicMarginSeparator",
            "margin separator keys must be computable before evaluating the exceptional even packet",
            (
                "Every mixed Goldbach margin cylinder has a pre-replay character/error coordinate with a closed "
                "cutoff transition law, or yields a cutoff-stable exceptional even packet."
            ),
            "a residue/cutoff cylinder whose positive-margin ambiguity survives all pre-replay character keys",
        ),
        transfer_attempt(
            ticket60,
            "twin-prime",
            "TP-TICKET-61",
            "TwinPrimeSymbolicSieveSeparator",
            "sieve separator keys must be computable before measuring retained exact-gap mass",
            (
                "Every mixed exact-gap sieve cylinder has a pre-replay parity/error coordinate with a closed "
                "sieve-level transition law, or yields a stable exact-gap mass leak."
            ),
            "a sieve cylinder whose gap-2 mass ambiguity survives all pre-replay parity/error keys",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "symbolic_failure_offset_open_no_resolution",
        "claim_boundary": (
            "Ticket 61 replaces TICKET60's replay-derived separator with pre-replay separator tests and transfers "
            "that stricter rule to RH, Goldbach, and Twin Prime. It does not prove or disprove any of the four "
            "open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket61-symbolic-failure-offset-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-61-symbolic-separator.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-61-symbolic-failure-offset.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-61-symbolic-margin-separator.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-61-symbolic-sieve-separator.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
