from __future__ import annotations

import json
from collections import Counter
from typing import Any, Callable

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket58_affine_boundary_lift_lab import build_exact32_boundary, key_for
from ticket59_symbolic_lift_mismatch_lab import CYLINDER_LOW_BITS, target_template
from ticket60_mixed_cylinder_separator_lab import Row, assess_separator
from ticket62_mod16_transition_cover_lab import lifted_rows_for_bits, mixed_base_rows
from ticket63_mod16_automaton_cover_lab import chain_lift_rows


GENERATED_AT = "2026-07-09T22:45:00+09:00"
SCHEMA = "primeproject.ticket65-start-template-chain-extinction-lab.v1"
START_BITS = 56
CHAIN_TARGETS = (60, 64, 68, 72, 76, 80)
EXTRA_BITS = 4


KeyFn = Callable[[Row], tuple[Any, ...]]


def build_chain() -> dict[str, Any]:
    boundary_data = build_exact32_boundary()
    base = mixed_base_rows(boundary_data["boundary"])
    lifted_56 = lifted_rows_for_bits(base["mixed_rows"], START_BITS, boundary_data["boundary"])
    rows = lifted_56["rows"]
    steps: list[dict[str, Any]] = []
    parent_bits = START_BITS
    for target_bits in CHAIN_TARGETS:
        chain = chain_lift_rows(
            rows,
            parent_bits=parent_bits,
            target_bits=target_bits,
            boundary=boundary_data["boundary"],
        )
        steps.append(
            {
                "parent_bits": parent_bits,
                "target_bits": target_bits,
                "parent_rows": len(rows),
                "chain": chain,
            }
        )
        rows = chain["rows"]
        parent_bits = target_bits
    return {
        "boundary": boundary_data["boundary"],
        "base": base,
        "lifted_56": lifted_56,
        "steps": steps,
    }


def make_gate_candidate_rows(parent_rows: list[Row], *, parent_bits: int, target_bits: int) -> list[Row]:
    target = target_template(target_bits)
    rows: list[Row] = []
    for parent_index, parent in enumerate(parent_rows):
        parent_residue = int(parent["residue"])
        low40 = int(parent["low40_residue"])
        base_mod16 = int(parent["base_mod16"])
        parent_top = int(parent.get("top_extension", 0))
        parent_high = parent_residue >> CYLINDER_LOW_BITS
        for child_top in range(1 << (target_bits - parent_bits)):
            residue = parent_residue | (child_top << parent_bits)
            certificate = cert(residue, target_bits)
            start_template = key_for(certificate) == target
            rows.append(
                {
                    "bits": target_bits,
                    "parent_bits": parent_bits,
                    "parent_index": parent_index,
                    "low40_residue": low40,
                    "low20_residue": low40 & ((1 << 20) - 1),
                    "base_mod16": base_mod16,
                    "parent_top_extension": parent_top,
                    "top_extension": child_top,
                    "parent_residue": parent_residue,
                    "parent_high_extension": parent_high,
                    "residue": residue,
                    "high_extension": residue >> CYLINDER_LOW_BITS,
                    "gate_label": "start_template" if start_template else "non_start_template",
                    "outcome_label": "candidate_child",
                    "prediction_label": "start_template" if start_template else "non_start_template",
                    "failure_observed": "gate_only",
                    "failure_next_valuation": "gate_only",
                    "certificate_prefix_length": int(certificate.get("prefix_length", 0)),
                    "certificate_consumed_bits": int(certificate.get("consumed_bits", 0)),
                }
            )
    return rows


def gate_separator_candidates() -> list[tuple[str, KeyFn]]:
    candidates: list[tuple[str, KeyFn]] = [
        ("state20_base_mod16", lambda row: (row["low20_residue"], row["base_mod16"])),
        (
            "state20_base_mod16_child_top4",
            lambda row: (row["low20_residue"], row["base_mod16"], row["top_extension"]),
        ),
        ("low40_child_top4", lambda row: (row["low40_residue"], row["top_extension"])),
        (
            "low40_base_child_top4",
            lambda row: (row["low40_residue"], row["base_mod16"], row["top_extension"]),
        ),
        (
            "low40_base_parent_top_child_top4",
            lambda row: (
                row["low40_residue"],
                row["base_mod16"],
                row["parent_top_extension"],
                row["top_extension"],
            ),
        ),
    ]
    for high_bits in (0, 2, 4, 6, 8, 10, 12):
        mask = (1 << high_bits) - 1
        candidates.append(
            (
                f"low40_parent_high{high_bits}_child_top4",
                lambda row, high_bits=high_bits, mask=mask: (
                    row["low40_residue"],
                    high_bits,
                    int(row["parent_high_extension"]) & mask,
                    row["top_extension"],
                ),
            )
        )
        candidates.append(
            (
                f"low40_parent_top_parent_high{high_bits}_child_top4",
                lambda row, high_bits=high_bits, mask=mask: (
                    row["low40_residue"],
                    row["parent_top_extension"],
                    high_bits,
                    int(row["parent_high_extension"]) & mask,
                    row["top_extension"],
                ),
            )
        )
    for residue_bits in (44, 48, 52):
        mask = (1 << residue_bits) - 1
        candidates.append(
            (
                f"parent_residue_mod_2^{residue_bits}_child_top4",
                lambda row, residue_bits=residue_bits, mask=mask: (
                    residue_bits,
                    int(row["parent_residue"]) & mask,
                    row["top_extension"],
                ),
            )
        )
    return candidates


def certificate_diagnostic_candidates() -> list[tuple[str, KeyFn]]:
    return [
        ("certificate_prefix_only", lambda row: (row["certificate_prefix_length"],)),
        ("certificate_consumed_only", lambda row: (row["certificate_consumed_bits"],)),
        (
            "certificate_prefix_consumed_pair",
            lambda row: (row["certificate_prefix_length"], row["certificate_consumed_bits"]),
        ),
        (
            "low40_certificate_pair_child_top4",
            lambda row: (
                row["low40_residue"],
                row["certificate_prefix_length"],
                row["certificate_consumed_bits"],
                row["top_extension"],
            ),
        ),
    ]


def summarize_separator_rows(rows: list[dict[str, Any]], *, row_count: int) -> dict[str, Any]:
    first_deterministic = next((row for row in rows if row["deterministic"]), None)
    first_compressed = next(
        (
            row
            for row in rows
            if row["deterministic"]
            and int(row["state_count"]) < row_count
            and int(row["largest_state_size"]) > 1
        ),
        None,
    )
    first_row_unique = next(
        (
            row
            for row in rows
            if row["deterministic"]
            and int(row["state_count"]) == row_count
            and int(row["largest_state_size"]) == 1
        ),
        None,
    )
    near_misses = [
        row
        for row in rows
        if not row["deterministic"] and int(row["state_count"]) < row_count
    ]
    near_misses.sort(
        key=lambda row: (
            int(row["collision_group_count"]),
            int(row["ambiguous_row_count"]),
            -int(row["state_count"]),
        )
    )
    return {
        "first_deterministic_separator": first_deterministic["separator"] if first_deterministic else None,
        "first_compressed_deterministic_separator": first_compressed["separator"] if first_compressed else None,
        "first_row_unique_deterministic_separator": first_row_unique["separator"] if first_row_unique else None,
        "best_compressed_near_miss": near_misses[0] if near_misses else None,
    }


def gate_audit(parent_rows: list[Row], *, parent_bits: int, target_bits: int) -> dict[str, Any]:
    gate_rows = make_gate_candidate_rows(parent_rows, parent_bits=parent_bits, target_bits=target_bits)
    ladder = [
        assess_separator(gate_rows, label, key_fn, label_field="gate_label", example_limit=4)
        for label, key_fn in gate_separator_candidates()
    ]
    certificate_ladder = [
        assess_separator(gate_rows, label, key_fn, label_field="gate_label", example_limit=4)
        for label, key_fn in certificate_diagnostic_candidates()
    ]
    summary = summarize_separator_rows(ladder, row_count=len(gate_rows))
    certificate_summary = summarize_separator_rows(certificate_ladder, row_count=len(gate_rows))
    return {
        "parent_bits": parent_bits,
        "target_bits": target_bits,
        "candidate_child_rows": len(gate_rows),
        "start_template_count": sum(1 for row in gate_rows if row["gate_label"] == "start_template"),
        "non_start_template_count": sum(1 for row in gate_rows if row["gate_label"] != "start_template"),
        "pre_replay_summary": summary,
        "pre_replay_ladder": ladder,
        "certificate_diagnostic_summary": certificate_summary,
        "certificate_diagnostic_ladder": certificate_ladder,
        "compressed_gate_found": summary["first_compressed_deterministic_separator"] is not None,
        "row_unique_gate_only": (
            summary["first_compressed_deterministic_separator"] is None
            and summary["first_row_unique_deterministic_separator"] is not None
        ),
    }


def compact_step(step: dict[str, Any]) -> dict[str, Any]:
    chain = step["chain"]
    rows = chain["rows"]
    return {
        "parent_bits": step["parent_bits"],
        "target_bits": chain["bits"],
        "parent_rows": step["parent_rows"],
        "tested_chain_lifts": int(chain["statistics"].get("tested_chain_lifts", 0)),
        "start_template_chain_lift": int(chain["statistics"].get("start_template_chain_lift", 0)),
        "non_start_template_chain_lift": int(chain["statistics"].get("non_start_template_chain_lift", 0)),
        "boundary_match": int(chain["statistics"].get("boundary_match", 0)),
        "boundary_mismatch": int(chain["statistics"].get("boundary_mismatch", 0)),
        "full_lasso_period_replay": int(chain["statistics"].get("full_lasso_period_replay", 0)),
        "transition_label_counts": dict(Counter(str(row["transition_label"]) for row in rows).most_common()),
        "failure_offset_counts": dict(Counter(str(row["failure_offset"]) for row in rows).most_common()),
    }


def collatz_attempt(ticket64: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket64["attempts"] if attempt["problem_id"] == "collatz")
    chain = build_chain()
    steps = chain["steps"]
    compact_steps = [compact_step(step) for step in steps]
    survivor_sequence = [{"bits": START_BITS, "rows": len(chain["lifted_56"]["rows"])}] + [
        {"bits": step["target_bits"], "rows": len(step["chain"]["rows"])}
        for step in steps
    ]
    full_period_count = sum(int(step["chain"]["statistics"].get("full_lasso_period_replay", 0)) for step in steps)
    extinction_observed = len(steps[-1]["chain"]["rows"]) == 0
    last_nonempty = next((item for item in reversed(survivor_sequence) if int(item["rows"]) > 0), None)
    gate64 = gate_audit(steps[0]["chain"]["rows"], parent_bits=60, target_bits=64)
    gate68 = gate_audit(steps[1]["chain"]["rows"], parent_bits=64, target_bits=68)
    audit = {
        "source_ticket": prior["ticket_id"],
        "theorem_name": "SymbolicStartTemplateGateAndOffsetTransition",
        "tested_chain_bits": [step["target_bits"] for step in compact_steps],
        "survivor_sequence": survivor_sequence,
        "chain_steps": compact_steps,
        "extinction_observed": extinction_observed,
        "extinction_at_bits": steps[-1]["target_bits"] if extinction_observed else None,
        "last_nonempty_bits": last_nonempty["bits"] if last_nonempty else None,
        "last_nonempty_rows": last_nonempty["rows"] if last_nonempty else 0,
        "full_lasso_period_replay_count": full_period_count,
        "gate_audits": [gate64, gate68],
        "gate_compression_obstruction": (
            not gate64["compressed_gate_found"]
            and bool(gate64["row_unique_gate_only"])
            and not gate68["compressed_gate_found"]
            and bool(gate68["row_unique_gate_only"])
        ),
        "bounded_branch_closed": extinction_observed and full_period_count == 0,
        "discarded_route": (
            "Treat the TICKET63/TICKET64 start-template survivor chain as evidence for a compact repeating automaton. "
            "TICKET65 closes that concrete chain by 80 bits and finds that the deterministic gate separators collapse to row-unique states."
        ),
        "retained_route": (
            "A useful proof route must now prove a genuine symbolic start-template predicate over the complement, not merely replay the "
            "TICKET63 survivor chain. The next object should cover the non-start-template complement or derive a non-row-unique gate."
        ),
        "candidate_theorem": (
            "StartTemplateChainExtinctionOrComplementCover: every branch in the current start-template cover either exits the cover in "
            "finite symbolic time or is captured by a non-row-unique gate predicate with a well-founded offset transition."
        ),
        "counterexample_target": (
            "A 4-bit lift branch beyond the current cover that re-enters a start-template lasso with a repeated non-row-unique gate state, "
            "or a compressed gate separator that remains deterministic past the 80-bit extinction audit."
        ),
        "next_theorem_target": "StartTemplateChainExtinctionOrComplementCover",
        "proof_boundary": (
            "TICKET65 does not prove Collatz. It closes the currently tracked TICKET63/TICKET64 start-template chain through 80 bits, "
            "but it does not prove that every integer enters this chain or that every complement branch descends."
        ),
    }
    status = (
        "targeted_start_template_chain_extinct_global_open_no_resolution"
        if audit["bounded_branch_closed"]
        else "targeted_start_template_chain_open_no_resolution"
    )
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-65",
        "route": "StartTemplateChainExtinctionOrComplementCover",
        "status": status,
        "proof_or_counterexample_mode": "bounded chain extinction plus gate-compression obstruction",
        "attempt": (
            "Continue from TICKET64 by following the admitted start-template chain through 80 bits and testing whether the gate can be "
            "represented by a compressed pre-replay state instead of a row-unique lookup."
        ),
        "bounded_result": {"start_template_chain_extinction_audit": audit},
        "obstruction": (
            "The tracked start-template survivor branch dies at 80 bits, while deterministic gate separators found at 64 and 68 bits "
            "are row-unique rather than compressed symbolic automata. This closes the branch but not the global Collatz problem."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": "Build a complement-cover audit for branches that exit the start-template chain, or find a non-row-unique symbolic gate.",
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
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
        "proof_or_counterexample_mode": "branch-extinction transfer",
        "attempt": (
            "Transfer the TICKET65 lesson: a finite branch can be closed, but the proof route only improves if the complement is also "
            "covered by an explicit symbolic predicate or if a true counterexample branch is isolated."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket65_transfer": route,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "Do not promote branch extinction to a theorem unless the complement is covered. A finite closed branch is useful pruning, "
                "not a proof of the open conjecture."
            ),
        },
        "obstruction": "This is a transfer discipline, not a solution.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Construct the problem-specific complement cover or expose a branch that violates the proposed cover.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket64 = read_json(ROOT / "data/open-problem/ticket64-symbolic-mod16-transition-lab.json")
    attempts = [
        transfer_attempt(
            ticket64,
            "riemann",
            "RH-TICKET-65",
            "ZeroKernelBranchExtinctionOrComplementCover",
            (
                "Every finite zero-kernel height branch either exits the admissible zero window or is covered by a positivity-preserving "
                "complement theorem."
            ),
            "a zero-kernel branch that remains admissible while violating the proposed positivity/complement cover",
        ),
        collatz_attempt(ticket64),
        transfer_attempt(
            ticket64,
            "goldbach",
            "GB-TICKET-65",
            "CutoffBranchExtinctionOrComplementCover",
            (
                "Every finite cutoff branch either exits the low-margin zone or is covered by an explicit positive lower-bound theorem "
                "for the complement."
            ),
            "a large-even cutoff branch whose margin remains low after the proposed complement cover should apply",
        ),
        transfer_attempt(
            ticket64,
            "twin-prime",
            "TP-TICKET-65",
            "ExactGapBranchExtinctionOrParityComplementCover",
            (
                "Every exact-gap sieve branch either exits the parity obstruction window or is covered by a parity-sensitive retained-mass "
                "lower-bound theorem."
            ),
            "a sieve branch that keeps exact-gap mass in the obstruction window while evading the complement cover",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "start_template_chain_extinction_open_no_resolution",
        "claim_boundary": (
            "Ticket 65 closes one tracked Collatz start-template chain through 80 bits and records gate-compression obstruction. "
            "It does not prove or disprove any of the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket65-start-template-chain-extinction-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-65-branch-extinction.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-65-start-template-chain-extinction.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-65-cutoff-complement.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-65-parity-complement.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
