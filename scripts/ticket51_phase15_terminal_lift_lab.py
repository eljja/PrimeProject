from __future__ import annotations

import json
from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, transition_label
from ticket42_parametric_transition_template_lab import edge_delta, stringify_key, template_key
from ticket43_lift_constraint_measure_lab import FAMILY
from ticket50_phase_lift_exception_lab import LASSO_PREFIX


GENERATED_AT = "2026-07-09T05:30:00+09:00"
SCHEMA = "primeproject.ticket51-phase15-terminal-lift-lab.v1"


def compact_certificate(certificate: dict[str, Any]) -> dict[str, Any]:
    key = template_key(certificate, FAMILY) if certificate.get("status") == "needs_split" else None
    return {
        "status": certificate.get("status"),
        "residue": certificate.get("residue"),
        "modulus_bits": certificate.get("modulus_bits"),
        "template": stringify_key(key) if key else None,
        "prefix_length": certificate.get("prefix_length"),
        "consumed_bits": certificate.get("consumed_bits"),
        "next_valuation": certificate.get("next_valuation"),
        "coefficient_log2_margin": certificate.get("coefficient_log2_margin"),
        "threshold_min_n_for_descent": certificate.get("threshold_min_n_for_descent"),
        "tail_word": list(certificate.get("prefix_word", [])[-8:]),
    }


def mismatch_reason(certificate: dict[str, Any], expected: tuple[Any, ...]) -> str:
    if certificate.get("status") != "needs_split":
        return str(certificate.get("status"))
    observed = template_key(certificate, FAMILY)
    labels = []
    for index, name in enumerate(("phase", "tail_word", "residue_mod_256", "next_valuation")):
        if observed[index] != expected[index]:
            labels.append(name)
    return "+".join(labels) if labels else "matched"


def extract_depth15_roots(source: dict[str, Any]) -> list[int]:
    collatz = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == "collatz")
    audit = collatz["bounded_result"]["phase_lift_exception_audit"]
    scan32 = next(scan for scan in audit["phase_scans"] if int(scan["bits"]) == 32)
    roots = []
    for example in scan32.get("strongest_near_lasso_examples", []):
        if int(example.get("lasso_prefix_depth", 0)) == 15:
            roots.append(int(example["residue"]))
    return sorted(set(roots))


def terminal_lift_audit(roots: list[int]) -> dict[str, Any]:
    states = [{"root_residue": residue, "residue": residue, "bits": 32, "path": []} for residue in roots]
    rows = []
    best_depth = 0
    best_paths: list[dict[str, Any]] = []

    for step, expected in enumerate(LASSO_PREFIX[1:], start=1):
        next_states = []
        mismatch_counter: Counter[str] = Counter()
        mismatch_examples = []
        transition_count = 0
        match_count = 0

        for state in states:
            residue = int(state["residue"])
            bits = int(state["bits"])
            parent = cert(residue, bits)
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            label = transition_label(low.get("status") == "needs_split", high.get("status") == "needs_split")
            for direction, child_residue, child in (("low", residue, low), ("high", high_residue, high)):
                transition_count += 1
                key = template_key(child, FAMILY) if child.get("status") == "needs_split" else None
                if key == expected:
                    match_count += 1
                    delta = edge_delta(parent, child)
                    new_path = [
                        *state["path"],
                        {
                            "step": step,
                            "direction": direction,
                            "label": label,
                            "parent_residue": residue,
                            "child_residue": child_residue,
                            "bits": bits + 1,
                            "expected_template": stringify_key(expected),
                            "observed_template": stringify_key(key),
                            **delta,
                        },
                    ]
                    next_state = {
                        "root_residue": state["root_residue"],
                        "residue": child_residue,
                        "bits": bits + 1,
                        "path": new_path,
                    }
                    next_states.append(next_state)
                    if len(new_path) > best_depth:
                        best_depth = len(new_path)
                        best_paths = [next_state]
                    elif len(new_path) == best_depth and len(best_paths) < 8:
                        best_paths.append(next_state)
                    continue

                reason = mismatch_reason(child, expected)
                mismatch_counter[reason] += 1
                if len(mismatch_examples) < 10:
                    mismatch_examples.append(
                        {
                            "step": step,
                            "direction": direction,
                            "root_residue": state["root_residue"],
                            "parent_residue": residue,
                            "child_residue": child_residue,
                            "bits": bits + 1,
                            "expected_template": stringify_key(expected),
                            "observed": stringify_key(key) if key else str(child.get("status")),
                            "reason": reason,
                            "certificate": compact_certificate(child),
                        }
                    )

        rows.append(
            {
                "step": step,
                "expected_template": stringify_key(expected),
                "input_states": len(states),
                "tested_branches": transition_count,
                "matching_branches": match_count,
                "surviving_states": len(next_states),
                "mismatch_counts": dict(sorted(mismatch_counter.items())),
                "mismatch_examples": mismatch_examples,
            }
        )
        states = next_states
        if not states:
            break

    terminal_row = rows[-1] if rows else {}
    return {
        "family": FAMILY,
        "source_roots": roots,
        "base_bits": 32,
        "target_prefix_length": len(LASSO_PREFIX) - 1,
        "rows": rows,
        "terminal_step": terminal_row.get("step"),
        "terminal_mismatch_counts": terminal_row.get("mismatch_counts", {}),
        "final_surviving_states": len(states),
        "full_lasso_completion_count": len(states) if len(rows) == len(LASSO_PREFIX) - 1 else 0,
        "best_edge_depth": best_depth,
        "best_template_depth": best_depth + 1 if roots else 0,
        "best_paths": [
            {
                "root_residue": path["root_residue"],
                "final_residue": path["residue"],
                "final_bits": path["bits"],
                "directions": [step["direction"] for step in path["path"]],
                "path_sample": path["path"][:6],
            }
            for path in best_paths
        ],
        "closed_bounded_statement": (
            "Starting from the two TICKET50 32-bit depth-15 near-lasso roots, the exact low/high lift tree has no "
            "survivor at the phase-15 template. Two branches fail by tail_word+next_valuation shift and two branches "
            "close by all_lift_descent."
        ),
        "proof_boundary": (
            "No Collatz proof and no Collatz counterexample. TICKET51 closes the terminal lift tree for the two "
            "known 32-bit near-lasso roots only. It does not exclude new 48-bit roots outside this ancestry and does "
            "not prove a global descent theorem."
        ),
    }


def collatz_attempt(source: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == "collatz")
    roots = extract_depth15_roots(source)
    audit = terminal_lift_audit(roots)
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-51",
        "route": "Phase15TerminalLiftClosure",
        "status": "known_depth15_roots_terminally_closed_open_problem_open",
        "proof_or_counterexample_mode": "terminal lift tree closure",
        "attempt": (
            "Do not treat the TICKET50 depth-15 residues as counterexamples. Start exactly from those two roots, "
            "open every low/high branch through the missing phase-15 edge, and classify the terminal failure."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "phase15_terminal_lift_audit": audit,
        },
        "obstruction": (
            "The two strongest 32-bit near-lasso witnesses do not complete the lasso. At the terminal phase, one "
            "ancestry shifts the tail/next-valuation pattern and the other closes by all_lift_descent."
        ),
        "candidate_theorem": (
            "Every future full-lasso candidate must either originate from a different 48-bit root outside the two "
            "TICKET50 depth-15 ancestries, or prove that the phase-15 tail shift can be repaired by an independent "
            "periodic replay theorem."
        ),
        "next_experiment": (
            "Generate TICKET52 by searching for genuinely new 48-bit or 64-bit start-template roots with lasso-prefix "
            "depth at least 15, instead of relifting the two closed TICKET50 roots."
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
        "proof_or_counterexample_mode": "terminal witness closure discipline",
        "attempt": (
            "Transfer TICKET51's rule: a strong finite witness must be terminally classified before it can be used "
            "as evidence for a proof or counterexample route."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior.get("route"),
            "ticket51_transfer": route,
            "candidate_theorem": candidate_theorem,
        },
        "obstruction": (
            "This transfer is methodological. It does not solve the target problem; it states how to close or promote "
            "the strongest finite witness without overclaiming."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Apply terminal witness closure to the problem-specific strongest surviving lasso/counterexample packet.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    source = read_json(ROOT / "data/open-problem/ticket50-phase-lift-exception-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-51",
            "ZeroKernelTerminalWitnessClosure",
            "Any strongest off-critical zero-kernel packet must be terminally classified as sign closure, boundary escape, or replayable zero witness.",
        ),
        collatz_attempt(source),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-51",
            "ResidueMarginTerminalWitnessClosure",
            "Any strongest Goldbach residue-margin packet must be terminally classified as positive margin, cutoff escape, or explicit even counterexample witness.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-51",
            "GapSelectorTerminalWitnessClosure",
            "Any strongest gap-2 selector packet must be terminally classified as leakage, sieve closure, or replayable exact-gap witness.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "phase15_terminal_lift_closed_open_no_resolution",
        "claim_boundary": (
            "Ticket 51 closes the terminal low/high lift tree for the two known 32-bit Collatz near-lasso roots. "
            "It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket51-phase15-terminal-lift-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-51-terminal-witness-closure.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-51-phase15-terminal-lift.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-51-terminal-witness-closure.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-51-terminal-witness-closure.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
