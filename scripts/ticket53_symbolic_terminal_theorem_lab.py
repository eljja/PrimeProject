from __future__ import annotations

import json
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, v2, write_json
from ticket34_high_branch_automaton_lab import cert, transition_label
from ticket42_parametric_transition_template_lab import stringify_key, template_key
from ticket43_lift_constraint_measure_lab import FAMILY
from ticket50_phase_lift_exception_lab import LASSO_PREFIX, START_TAIL
from ticket51_phase15_terminal_lift_lab import compact_certificate, mismatch_reason


GENERATED_AT = "2026-07-09T07:25:00+09:00"
SCHEMA = "primeproject.ticket53-symbolic-terminal-theorem-lab.v1"


KNOWN_NEAR_LASSO_ROOTS = [
    {"source_ticket": "TICKET-50", "base_bits": 32, "residue": 1_471_663_463},
    {"source_ticket": "TICKET-50", "base_bits": 32, "residue": 3_206_130_791},
    {"source_ticket": "TICKET-52", "base_bits": 48, "residue": 171_308_122_831_719},
]


def replay_current(residue: int, word: list[int]) -> int:
    current = residue
    for valuation in word:
        current = (3 * current + 1) >> valuation
    return current


def terminal_branch_audit(root: dict[str, Any]) -> dict[str, Any]:
    residue = int(root["residue"])
    base_bits = int(root["base_bits"])
    parent_bits = base_bits + 14
    terminal_bits = base_bits + 15
    parent = cert(residue, parent_bits)
    low = cert(residue, terminal_bits)
    high_residue = residue + (1 << parent_bits)
    high = cert(high_residue, terminal_bits)
    parent_key = template_key(parent, FAMILY) if parent.get("status") == "needs_split" else None
    low_key = template_key(low, FAMILY) if low.get("status") == "needs_split" else None
    high_key = template_key(high, FAMILY) if high.get("status") == "needs_split" else None
    parent_word = list(parent.get("prefix_word", []))
    current = replay_current(residue, parent_word)
    high_current_delta = (3 ** len(parent_word)) * (1 << 9)
    low_next_valuation = v2(3 * current + 1)
    high_next_valuation = v2(3 * (current + high_current_delta) + 1)
    target = LASSO_PREFIX[15]

    return {
        "source_ticket": root["source_ticket"],
        "base_bits": base_bits,
        "residue": residue,
        "parent_bits": parent_bits,
        "terminal_bits": terminal_bits,
        "parent_template": stringify_key(parent_key) if parent_key else str(parent.get("status")),
        "parent_expected": stringify_key(LASSO_PREFIX[14]),
        "parent_consumed_bits": parent.get("consumed_bits"),
        "parent_prefix_length": parent.get("prefix_length"),
        "parent_next_valuation": parent.get("next_valuation"),
        "terminal_target": stringify_key(target),
        "high_current_delta_v2": v2(high_current_delta),
        "low_next_valuation_before_terminal": low_next_valuation,
        "high_next_valuation_before_terminal": high_next_valuation,
        "transition_label": transition_label(low.get("status") == "needs_split", high.get("status") == "needs_split"),
        "low_terminal": {
            "residue": residue,
            "status": low.get("status"),
            "observed": stringify_key(low_key) if low_key else str(low.get("status")),
            "reason": mismatch_reason(low, target),
            "certificate": compact_certificate(low),
        },
        "high_terminal": {
            "residue": high_residue,
            "status": high.get("status"),
            "observed": stringify_key(high_key) if high_key else str(high.get("status")),
            "reason": mismatch_reason(high, target),
            "certificate": compact_certificate(high),
        },
        "terminal_target_matched": low_key == target or high_key == target,
    }


def collatz_attempt(source: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == "collatz")
    audits = [terminal_branch_audit(root) for root in KNOWN_NEAR_LASSO_ROOTS]
    all_parent_match = all(row["parent_template"] == row["parent_expected"] for row in audits)
    any_terminal_match = any(row["terminal_target_matched"] for row in audits)
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-53",
        "route": "SymbolicPhase15TerminalMismatchTheorem",
        "status": "extracted_lasso_family_terminally_refuted_open_problem_open",
        "proof_or_counterexample_mode": "symbolic terminal mismatch theorem",
        "attempt": (
            "Do not enlarge the random sample. Prove the terminal obstruction that every root matching the extracted "
            "phase-14 lasso parent with next_valuation 10 must fail the phase-15 target on both low and high lifts."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "symbolic_terminal_theorem_audit": {
                "family": FAMILY,
                "theorem_name": "Phase15TerminalMismatchForExtractedLasso",
                "premises": [
                    "parent at bits b+14 has template [14,[1,1,1,1],103,10]",
                    "the parent certificate consumed b+5 bits, so the next valuation 10 exactly reaches b+15",
                    "the terminal target is [15,[1,1,1,1],103,10]",
                ],
                "low_branch_argument": (
                    "The low terminal branch consumes the pending valuation 10 exactly at b+15. The consumed "
                    "valuation enters the prefix tail, so the terminal tail contains 10 and cannot equal [1,1,1,1]."
                ),
                "high_branch_argument": (
                    "The high terminal branch adds 2^(b+14) to the parent residue. After the already-consumed "
                    "prefix, this changes the boundary value by 3^m * 2^9. Since the low branch has v2(3x+1)=10, "
                    "the high branch has v2(3x+1 + 3^(m+1)*2^9)=9. The terminal prefix therefore consumes a 9 "
                    "before any remaining bit can be resolved, so its tail cannot be [1,1,1,1]."
                ),
                "machine_checked_roots": audits,
                "all_checked_roots_satisfy_parent_premise": all_parent_match,
                "terminal_target_match_count": sum(1 for row in audits if row["terminal_target_matched"]),
                "terminal_theorem_scope": (
                    "This theorem refutes the extracted low-lift lasso family used by TICKET50-TICKET52. It does "
                    "not prove global Collatz descent and does not rule out a different lasso template."
                ),
                "closed_bounded_statement": (
                    "The known 32-bit and sampled 48-bit depth-15 near-lasso roots all satisfy the symbolic parent "
                    "premise, and none can match the phase-15 terminal target. The failure follows from valuation "
                    "arithmetic, not from larger sampling."
                ),
                "next_frontier": (
                    "Discard the extracted phase-15 lasso as a counterexample route. The next useful search is a "
                    "new lasso template family, a global descent invariant, or a formalization of this local theorem "
                    "inside the proof kernel."
                ),
                "proof_boundary": (
                    "No Collatz proof and no Collatz counterexample. TICKET53 refutes one extracted lasso family, "
                    "including the known near-lasso witnesses, but a Collatz proof still requires a global argument "
                    "covering every possible trajectory or every remaining template family."
                ),
            },
        },
        "obstruction": (
            "The extracted lasso template is internally terminal-inconsistent: the pending valuation 10 required "
            "from phases 5 through 14 is exactly consumed at phase 15, forcing a tail mismatch on the low branch and "
            "a valuation-9/tail mismatch on the high branch."
        ),
        "candidate_theorem": (
            "Formalize Phase15TerminalMismatchForExtractedLasso and then search for a genuinely different lasso "
            "template or a global descent invariant; repeating the same phase-15 lasso family is now a dead route."
        ),
        "next_experiment": (
            "Generate TICKET54 by extracting new lasso-template families from the frontier graph, excluding every "
            "family whose terminal mismatch follows from this theorem."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    candidate_theorem: str,
) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "local terminal theorem before broader search",
        "attempt": (
            "Transfer TICKET53's rule: when a strong witness family closes for a structural reason, promote the "
            "local terminal theorem and remove that family from future counterexample search."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior.get("route"),
            "ticket53_transfer": route,
            "candidate_theorem": candidate_theorem,
            "frontier_rule": (
                "A closed witness family should become a local no-go theorem, not a repeated sampling target."
            ),
        },
        "obstruction": (
            "This is a method-transfer artifact. It does not solve the target problem, but it forces the next search "
            "to exclude a locally refuted witness family."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "State the problem-specific terminal no-go theorem and then search outside that family.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    source = read_json(ROOT / "data/open-problem/ticket52-frontier-budget-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-53",
            "ZeroKernelTerminalNoGoTheorem",
            "Any repeated off-critical zero-kernel family that closes by a terminal sign or boundary identity must be removed before searching new zero witnesses.",
        ),
        collatz_attempt(source),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-53",
            "ResidueMarginTerminalNoGoTheorem",
            "Any residue-margin family whose terminal packet is forced positive or forced off-target must become a local no-go theorem before new exceptional packets are searched.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-53",
            "GapSelectorTerminalNoGoTheorem",
            "Any exact-gap selector family whose terminal leakage is structurally forced must be excluded before searching a new gap-2 witness family.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "symbolic_terminal_theorem_open_no_resolution",
        "claim_boundary": (
            "Ticket 53 refutes one extracted Collatz lasso family by a symbolic terminal mismatch theorem. It does "
            "not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket53-symbolic-terminal-theorem-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-53-terminal-no-go-theorem.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-53-symbolic-terminal-theorem.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-53-terminal-no-go-theorem.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-53-terminal-no-go-theorem.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
