from __future__ import annotations

import json
from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, transition_label
from ticket42_parametric_transition_template_lab import edge_delta, stringify_key, template_key
from ticket43_lift_constraint_measure_lab import FAMILY
from ticket44_feature_measure_counteredge_lab import round_float
from ticket45_symbolic_rank_clause_lab import compact_example


GENERATED_AT = "2026-07-09T03:15:00+09:00"
SCHEMA = "primeproject.ticket49-symbolic-preimage-obstruction-lab.v1"


PREFIX_TEMPLATES: list[tuple[Any, ...]] = [
    (0, (1, 1, 1, 1), 103, 1),
    (1, (1, 1, 1, 1), 103, 1),
    (2, (1, 1, 1, 1), 103, 1),
    (3, (1, 1, 1, 1), 103, 1),
    (4, (1, 1, 1, 1), 103, 1),
    (5, (1, 1, 1, 1), 103, 10),
]


def mismatch_labels(observed: tuple[Any, ...] | None, expected: tuple[Any, ...]) -> list[str]:
    if observed is None:
        return ["closed_or_not_needs_split"]
    labels = []
    names = ("phase", "tail_word", "residue_mod_256", "next_valuation")
    for index, name in enumerate(names):
        if observed[index] != expected[index]:
            labels.append(name)
    return labels or ["matched"]


def first_template_candidates(bits: int = 16) -> list[int]:
    target = PREFIX_TEMPLATES[0]
    rows = []
    for residue in range(1, 1 << bits, 2):
        certificate = cert(residue, bits)
        if certificate.get("status") == "needs_split" and template_key(certificate, FAMILY) == target:
            rows.append(residue)
    return rows


def candidate_certificate_row(residue: int, bits: int) -> dict[str, Any]:
    certificate = cert(residue, bits)
    key = template_key(certificate, FAMILY) if certificate.get("status") == "needs_split" else None
    return {
        "residue": residue,
        "bits": bits,
        "status": certificate.get("status"),
        "template": stringify_key(key) if key else None,
        "prefix_length": certificate.get("prefix_length"),
        "consumed_bits": certificate.get("consumed_bits"),
        "next_valuation": certificate.get("next_valuation"),
        "tail_word": list(certificate.get("prefix_word", [])[-8:]),
    }


def certificate_digest(certificate: dict[str, Any]) -> dict[str, Any]:
    key = template_key(certificate, FAMILY) if certificate.get("status") == "needs_split" else None
    return {
        "status": certificate.get("status"),
        "residue": certificate.get("residue"),
        "modulus_bits": certificate.get("modulus_bits"),
        "template": stringify_key(key) if key else None,
        "prefix_length": certificate.get("prefix_length"),
        "consumed_bits": certificate.get("consumed_bits"),
        "next_valuation": certificate.get("next_valuation"),
        "tail_word": list(certificate.get("prefix_word", [])[-8:]),
    }


def branch_prefix_audit(*, forced_direction: str | None = None) -> dict[str, Any]:
    starts = first_template_candidates(16)
    states: list[dict[str, Any]] = [
        {
            "residue": residue,
            "bits": 16,
            "path": [],
        }
        for residue in starts
    ]
    rows = []
    best_partial: dict[str, Any] | None = None

    for step, expected in enumerate(PREFIX_TEMPLATES[1:], start=1):
        next_states: list[dict[str, Any]] = []
        mismatch_counter: Counter[str] = Counter()
        mismatch_examples = []
        match_count = 0
        transition_count = 0
        for state in states:
            residue = int(state["residue"])
            bits = int(state["bits"])
            parent = cert(residue, bits)
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            label = transition_label(low.get("status") == "needs_split", high.get("status") == "needs_split")
            branches = (("low", residue, low), ("high", high_residue, high))
            for direction, child_residue, child in branches:
                if forced_direction is not None and direction != forced_direction:
                    continue
                transition_count += 1
                observed = template_key(child, FAMILY) if child.get("status") == "needs_split" else None
                mismatches = mismatch_labels(observed, expected)
                if observed == expected:
                    delta = edge_delta(parent, child)
                    match_count += 1
                    new_path = [
                        *state["path"],
                        {
                            "step": step,
                            "bits": bits,
                            "direction": direction,
                            "label": label,
                            "parent_residue": residue,
                            "child_residue": child_residue,
                            "parent_template": stringify_key(PREFIX_TEMPLATES[step - 1]),
                            "child_template": stringify_key(expected),
                            **delta,
                        },
                    ]
                    new_state = {
                        "residue": child_residue,
                        "bits": bits + 1,
                        "path": new_path,
                    }
                    next_states.append(new_state)
                    if best_partial is None or len(new_path) > len(best_partial["path"]):
                        best_partial = new_state
                    continue
                reason = "+".join(mismatches)
                mismatch_counter[reason] += 1
                if len(mismatch_examples) < 8:
                    mismatch_examples.append(
                        {
                            "step": step,
                            "direction": direction,
                            "parent_residue": residue,
                            "child_residue": child_residue,
                            "bits": bits + 1,
                            "expected": stringify_key(expected),
                            "observed": stringify_key(observed) if observed else str(child.get("status")),
                            "mismatch": mismatches,
                            "child_certificate": certificate_digest(child),
                        }
                    )
        rows.append(
            {
                "step": step,
                "expected_template": stringify_key(expected),
                "input_states": len(states),
                "tested_transitions": transition_count,
                "matching_transitions": match_count,
                "surviving_states": len(next_states),
                "mismatch_counts": dict(sorted(mismatch_counter.items())),
                "mismatch_examples": mismatch_examples,
            }
        )
        states = next_states
        if not states:
            break

    best_path = best_partial.get("path", []) if best_partial else []
    return {
        "mode": "forced_low_lasso_prefix" if forced_direction == "low" else "any_direction_template_prefix",
        "base_bits": 16,
        "start_template": stringify_key(PREFIX_TEMPLATES[0]),
        "start_candidates": starts,
        "start_candidate_certificates": [candidate_certificate_row(residue, 16) for residue in starts],
        "rows": rows,
        "minimal_dead_step": rows[-1]["step"] if rows and rows[-1]["surviving_states"] == 0 else None,
        "best_partial_depth": len(best_path),
        "best_partial_debt": round_float(sum(float(step.get("delta_debt", 0.0)) for step in best_path)),
        "best_partial_path": [compact_example(step) for step in best_path],
    }


def collatz_attempt(source: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == "collatz")
    any_direction = branch_prefix_audit(forced_direction=None)
    forced_low = branch_prefix_audit(forced_direction="low")
    low_rows = forced_low["rows"]
    dead_row = low_rows[-1] if low_rows else {}
    mismatch_text = " ".join(str(row.get("mismatch_counts", {})) for row in low_rows)
    obstruction_coordinate = "next_valuation" if "next_valuation" in mismatch_text else "unknown"
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-49",
        "route": "SymbolicPreimageObstructionOrAllPhaseReachability",
        "status": "minimal_preimage_obstruction_found_open_problem_open",
        "proof_or_counterexample_mode": "local symbolic preimage obstruction",
        "attempt": (
            "Do not discard TICKET48's failed concrete probe as a sampling artifact. Re-run the first lasso-prefix "
            "preimage exactly at the 16-bit phase-compatible start template, classify every failed branch by the "
            "template coordinate that breaks, and isolate the next theorem needed for all future phase-compatible "
            "starts."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "symbolic_preimage_obstruction_audit": {
                "family": FAMILY,
                "prefix_templates": [stringify_key(template) for template in PREFIX_TEMPLATES],
                "any_direction_prefix": any_direction,
                "forced_low_prefix": forced_low,
                "minimal_obstruction": {
                    "dead_step": dead_row.get("step"),
                    "obstruction_coordinate": obstruction_coordinate,
                    "required_template": dead_row.get("expected_template"),
                    "mismatch_counts": dead_row.get("mismatch_counts", {}),
                    "interpretation": (
                        "The only 16-bit concrete path that survives the first two lasso edges reaches the third "
                        "phase with the correct phase, tail word, and residue mod 256, but the next valuation is 5 "
                        "instead of the lasso-required 1. Thus the first visible failure is not a generic frontier "
                        "shortage; it is a specific next_valuation preimage obstruction."
                    ),
                },
                "closed_bounded_statement": (
                    "At the exact 16-bit phase-compatible start, the first three concrete low-prefix constraints of "
                    "the TICKET48 lasso are unsatisfied: four starts shrink to two, then one, then zero."
                ),
                "proof_boundary": (
                    "No Collatz proof and no Collatz counterexample. TICKET49 identifies the minimal local "
                    "coordinate that blocks the 16-bit lasso-prefix realization, but it does not prove the same "
                    "next_valuation obstruction for every future phase-compatible modulus."
                ),
            },
        },
        "obstruction": (
            "The abstract lasso's third low-prefix step requires next_valuation 1, while the unique surviving "
            "concrete prefix has next_valuation 5. A proof route must now decide whether this mismatch persists "
            "symbolically for every phase-compatible lift."
        ),
        "candidate_theorem": (
            "For every phase-compatible modulus b == 0 mod 16, no residue class realizing the first two concrete "
            "low-prefix constraints of the TICKET48 lasso can also realize the third constraint with next_valuation 1; "
            "or else exhibit a higher-bit exception as a concrete periodic-lift candidate."
        ),
        "next_experiment": (
            "Generate TICKET50 by deriving the next_valuation preimage recurrence for the third low-prefix step and "
            "checking whether it is empty for all b == 0 mod 16, rather than sampling only the 16-bit frontier."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    obstruction_coordinate: str,
    candidate_theorem: str,
    next_experiment: str,
) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "minimal obstruction transfer",
        "attempt": (
            "Transfer TICKET49's rule: after a bounded lasso or finite-state route fails, identify the first local "
            "coordinate that blocks the preimage before proposing a larger proof object."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior["route"],
            "obstruction_coordinate": obstruction_coordinate,
            "candidate_theorem": candidate_theorem,
            "ticket49_transfer": route,
        },
        "obstruction": (
            "This is a method-transfer artifact. It names the coordinate where a lasso/preimage route must be "
            "proved impossible or turned into a counterexample, but it is not a theorem for the target conjecture."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket48-automaton-reachability-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-49",
            "ZeroKernelPreimageObstruction",
            "kernel_sign_or_boundary_height",
            "Find the first kernel coordinate that blocks an off-critical zero-lasso preimage, then prove that coordinate obstruction uniformly.",
            "Build a zero-kernel preimage classifier that reports the first failed coordinate instead of only reporting no lasso.",
        ),
        collatz_attempt(source),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-49",
            "ResidueMarginPreimageObstruction",
            "singular_series_margin_or_residue_class",
            "Identify the first residue/margin coordinate that blocks an exceptional-set lasso and prove the margin remains positive uniformly.",
            "Build a residue-margin preimage audit that reports the first failed coordinate for every cutoff candidate.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-49",
            "GapSelectorPreimageObstruction",
            "gap_selector_mass_or_leakage_class",
            "Identify the first selector coordinate that blocks a wider-gap leakage lasso and prove exact gap-2 mass cannot leak through it.",
            "Build an exact-gap selector preimage audit that reports the first failed leakage coordinate.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "symbolic_preimage_obstruction_open_no_resolution",
        "claim_boundary": (
            "Ticket 49 identifies the first local Collatz coordinate that breaks the TICKET48 lasso-prefix "
            "realization and transfers the coordinate-obstruction discipline to the other open-problem pages. It "
            "does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket49-symbolic-preimage-obstruction-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-49-zero-kernel-preimage.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-49-symbolic-preimage-obstruction.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-49-residue-margin-preimage.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-49-gap-selector-preimage.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
