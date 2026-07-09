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
from ticket63_mod16_automaton_cover_lab import audit_rows, chain_lift_rows


GENERATED_AT = "2026-07-09T20:45:00+09:00"
SCHEMA = "primeproject.ticket64-symbolic-mod16-transition-lab.v1"
PARENT_BITS = 60
TARGET_BITS = 64
QUOTIENT_BITS = 20


KeyFn = Callable[[Row], tuple[Any, ...]]


def build_chain_rows() -> dict[str, Any]:
    boundary_data = build_exact32_boundary()
    base = mixed_base_rows(boundary_data["boundary"])
    lifted_56 = lifted_rows_for_bits(base["mixed_rows"], 56, boundary_data["boundary"])
    chain_60 = chain_lift_rows(lifted_56["rows"], parent_bits=56, target_bits=PARENT_BITS, boundary=boundary_data["boundary"])
    chain_64 = chain_lift_rows(chain_60["rows"], parent_bits=PARENT_BITS, target_bits=TARGET_BITS, boundary=boundary_data["boundary"])
    return {
        "base": base,
        "lifted_56": lifted_56,
        "chain_60": chain_60,
        "chain_64": chain_64,
    }


def gate_candidate_rows(parent_rows: list[Row]) -> list[Row]:
    rows: list[Row] = []
    target = target_template(TARGET_BITS)
    low_mask = (1 << QUOTIENT_BITS) - 1
    extra_bits = TARGET_BITS - PARENT_BITS
    for parent_index, parent in enumerate(parent_rows):
        low40 = int(parent["low40_residue"])
        low20 = low40 & low_mask
        parent_residue = int(parent["residue"])
        for top_extension in range(1 << extra_bits):
            residue = parent_residue | (top_extension << PARENT_BITS)
            certificate = cert(residue, TARGET_BITS)
            is_start_template = key_for(certificate) == target
            rows.append(
                {
                    "bits": TARGET_BITS,
                    "parent_bits": PARENT_BITS,
                    "parent_index": parent_index,
                    "low40_residue": low40,
                    "low20_residue": low20,
                    "base_high_extension": int(parent["base_high_extension"]),
                    "base_mod16": int(parent["base_mod16"]),
                    "parent_top_extension": int(parent["top_extension"]),
                    "top_extension": top_extension,
                    "residue": residue,
                    "parent_residue": parent_residue,
                    "high_extension": residue >> CYLINDER_LOW_BITS,
                    "parent_failure_offset": parent["failure_offset"],
                    "gate_label": "start_template" if is_start_template else "non_start_template",
                    "outcome_label": "candidate_child",
                    "prediction_label": "start_template" if is_start_template else "non_start_template",
                    "failure_observed": "gate_only",
                    "failure_next_valuation": "gate_only",
                    "certificate_prefix_length": int(certificate.get("prefix_length", 0)),
                    "certificate_consumed_bits": int(certificate.get("consumed_bits", 0)),
                }
            )
    return rows


def gate_candidates() -> list[tuple[str, KeyFn]]:
    return [
        ("state20_base_mod16", lambda row: (row["low20_residue"], row["base_mod16"])),
        ("state20_base_mod16_top4", lambda row: (row["low20_residue"], row["base_mod16"], row["top_extension"])),
        ("state40_base_mod16", lambda row: (row["low40_residue"], row["base_mod16"])),
        ("state40_base_mod16_top4", lambda row: (row["low40_residue"], row["base_mod16"], row["top_extension"])),
        (
            "state40_base_mod16_parent_top4_top4",
            lambda row: (row["low40_residue"], row["base_mod16"], row["parent_top_extension"], row["top_extension"]),
        ),
        (
            "state40_base_high8_parent_top4_top4",
            lambda row: (
                row["low40_residue"],
                row["base_high_extension"],
                row["parent_top_extension"],
                row["top_extension"],
            ),
        ),
        (
            "parent_residue_mod_2^24_top4",
            lambda row: (int(row["parent_residue"]) & ((1 << 24) - 1), row["top_extension"]),
        ),
        (
            "parent_residue_mod_2^28_top4",
            lambda row: (int(row["parent_residue"]) & ((1 << 28) - 1), row["top_extension"]),
        ),
    ]


def gate_ladder(rows: list[Row]) -> dict[str, Any]:
    ladder = [
        assess_separator(rows, label, key_fn, label_field="gate_label")
        for label, key_fn in gate_candidates()
    ]
    first = next((row for row in ladder if row["deterministic"]), None)
    return {
        "row_count": len(rows),
        "start_template_count": sum(1 for row in rows if row["gate_label"] == "start_template"),
        "non_start_template_count": sum(1 for row in rows if row["gate_label"] != "start_template"),
        "first_gate_deterministic_separator": first["separator"] if first else None,
        "state20_gate_row": next(row for row in ladder if row["separator"] == "state20_base_mod16"),
        "state20_top4_gate_row": next(row for row in ladder if row["separator"] == "state20_base_mod16_top4"),
        "gate_ladder": ladder,
    }


def summarize_formula(rows60: list[Row], rows64: list[Row]) -> dict[str, Any]:
    transition64 = Counter(str(row["transition_label"]) for row in rows64)
    root_transition64 = Counter(str(row["root_transition_label"]) for row in rows64)
    parent_offsets = Counter(str(row["parent_failure_offset"]) for row in rows64)
    child_offsets = Counter(str(row["failure_offset"]) for row in rows64)
    outcomes = Counter(str(row["outcome_label"]) for row in rows64)
    predictions = Counter(str(row["prediction_label"]) for row in rows64)
    rows60_offsets = Counter(str(row["failure_offset"]) for row in rows60)
    return {
        "candidate_formula": "admitted_60_to_64_child => failure_offset'=0 and transition_label=0->0",
        "scope": "Only admitted start-template children inside the finite TICKET63 60-bit survivor cover.",
        "parent_60_failure_offsets": dict(rows60_offsets.most_common()),
        "parent_failure_offsets_on_64": dict(parent_offsets.most_common()),
        "child_64_failure_offsets": dict(child_offsets.most_common()),
        "transition_label_counts": dict(transition64.most_common()),
        "root_transition_label_counts": dict(root_transition64.most_common()),
        "outcome_counts": dict(outcomes.most_common()),
        "prediction_counts": dict(predictions.most_common()),
        "admitted_child_formula_holds": (
            bool(rows64)
            and set(parent_offsets) == {"0"}
            and set(child_offsets) == {"0"}
            and set(transition64) == {"0->0"}
        ),
        "admitted_child_formula_fails": not (
            bool(rows64)
            and set(parent_offsets) == {"0"}
            and set(child_offsets) == {"0"}
            and set(transition64) == {"0->0"}
        ),
    }


def collatz_attempt(ticket63: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket63["attempts"] if attempt["problem_id"] == "collatz")
    chains = build_chain_rows()
    rows60 = chains["chain_60"]["rows"]
    rows64 = chains["chain_64"]["rows"]
    gate_rows = gate_candidate_rows(rows60)
    gate = gate_ladder(gate_rows)
    audit64 = audit_rows("64_bit_chained_from_60_survivors", rows64)
    formula = summarize_formula(rows60, rows64)
    state20_obstructed = not bool(gate["state20_gate_row"]["deterministic"])
    formula_obstructed = bool(formula["admitted_child_formula_fails"])
    status = (
        "symbolic_transition_gate_and_formula_obstruction_open_no_resolution"
        if state20_obstructed or formula_obstructed
        else "symbolic_transition_candidate_open_no_resolution"
    )
    symbolic_audit = {
        "source_ticket": prior["ticket_id"],
        "theorem_name": "SymbolicMod16AutomatonTransitionProof",
        "parent_bits": PARENT_BITS,
        "target_bits": TARGET_BITS,
        "parent_60_rows": len(rows60),
        "target_64_rows": len(rows64),
        "candidate_child_rows": len(gate_rows),
        "chain_64_statistics": chains["chain_64"]["statistics"],
        "chain_64_parent_rows_with_start_template_lift": chains["chain_64"]["parent_rows_with_start_template_chain_lift"],
        "chain_64_parent_extension_count_distribution": chains["chain_64"]["parent_extension_count_distribution"],
        "gate_ladder": gate,
        "admitted_child_audit": audit64,
        "symbolic_formula_pressure": formula,
        "state20_gate_obstruction": state20_obstructed,
        "admitted_child_formula_obstruction": formula_obstructed,
        "discarded_route": (
            "Promote the TICKET63 quotient state low40 mod 2^20 + base_mod16 directly to a symbolic transition theorem. "
            "TICKET64 rejects that shortcut twice: the same state admits both start-template and non-start-template children, and "
            "the next admitted children no longer follow the optimistic 0->0 transition."
        ),
        "retained_route": (
            "Replace the optimistic 0->0 continuation by a symbolic start-template gate plus an offset-transition family that "
            "allows 0->1, 0->2, 0->3, 0->4, and 0->5 in the observed 64-bit admitted subcover."
        ),
        "candidate_theorem": (
            "For every admissible lift, a symbolic gate predicate first selects start-template children; inside that selected "
            "subcover an explicit offset-transition relation is closed and a separate well-founded cover excludes full-period cycles."
        ),
        "counterexample_target": (
            "A pair of candidate children sharing low40 mod 2^20 + base_mod16 but disagreeing on start-template admissibility, "
            "or a future admitted child pair sharing the refined symbolic state but disagreeing on the offset-transition label."
        ),
        "next_theorem_target": "SymbolicStartTemplateGateAndOffsetTransition",
        "proof_boundary": (
            "TICKET64 does not prove Collatz. It finds that the retained quotient state is not enough to predict the next "
            "start-template gate and that the optimistic 0->0 admitted-child transition already fails at 64 bits in this finite audit."
        ),
    }
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-64",
        "route": "SymbolicMod16AutomatonTransitionProof",
        "status": status,
        "proof_or_counterexample_mode": "symbolic transition pressure plus admissibility-gate falsification",
        "attempt": (
            "Continue from TICKET63 by testing whether the retained quotient state can symbolically select 64-bit admissible "
            "children and preserve the admitted-child transition law."
        ),
        "bounded_result": {"symbolic_mod16_transition_audit": symbolic_audit},
        "obstruction": (
            "The old quotient state does not by itself define the next admissibility gate, and admitted 64-bit children split "
            "into nonzero offset transitions. This blocks the direct symbolic proof and forces a gate predicate plus an "
            "offset-transition relation."
        ),
        "candidate_theorem": symbolic_audit["candidate_theorem"],
        "next_experiment": "Generate a symbolic start-template gate plus offset-transition relation, or find the first refined-state collision.",
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    gate_name: str,
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
        "proof_or_counterexample_mode": "symbolic-gate transfer",
        "attempt": (
            "Transfer TICKET64's lesson: a finite automaton table is not enough unless the next admissibility gate is also "
            "symbolically closed or an explicit gate collision is reported."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket64_transfer": route,
            "gate_name": gate_name,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "A proof route must prove the gate predicate and the transition relation together. A gate collision refutes "
                "the proposed abstraction even when no conjecture counterexample exists."
            ),
        },
        "obstruction": "This is a transfer discipline, not a solution.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Build the problem-specific gate predicate or expose the first gate collision.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket63 = read_json(ROOT / "data/open-problem/ticket63-mod16-automaton-cover-lab.json")
    attempts = [
        transfer_attempt(
            ticket63,
            "riemann",
            "RH-TICKET-64",
            "ZeroKernelGatePredicateOrHeightCollision",
            "zero-kernel admissible height gate",
            (
                "Every admissible height lift is selected by a symbolic zero-kernel gate and then follows a "
                "positivity-preserving transition, or a height collision is produced."
            ),
            "two height lifts with the same zero-kernel gate state but different admissibility or positivity labels",
        ),
        collatz_attempt(ticket63),
        transfer_attempt(
            ticket63,
            "goldbach",
            "GB-TICKET-64",
            "GoldbachCutoffGatePredicateOrMarginCollision",
            "large-even cutoff admissibility gate",
            (
                "Every cutoff lift is selected by an explicit margin gate before the positive representation "
                "transition is applied, or a stable margin collision is produced."
            ),
            "two cutoff lifts with the same margin-gate state but conflicting positive-margin labels",
        ),
        transfer_attempt(
            ticket63,
            "twin-prime",
            "TP-TICKET-64",
            "TwinPrimeParityGatePredicateOrMassLeak",
            "exact-gap parity admissibility gate",
            (
                "Every sieve-level lift is selected by an exact-gap parity gate before retained mass is propagated, "
                "or a parity collision produces a stable exact-gap mass leak."
            ),
            "two sieve lifts with the same parity-gate state but conflicting exact-gap retained-mass labels",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "symbolic_mod16_transition_open_no_resolution",
        "claim_boundary": (
            "Ticket 64 pressures the TICKET63 automaton table by adding the missing admissibility-gate test. It does not "
            "prove or disprove any of the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket64-symbolic-mod16-transition-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-64-gate-predicate.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-64-symbolic-mod16-transition.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-64-cutoff-gate.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-64-parity-gate.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
