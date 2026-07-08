from __future__ import annotations

import json
from collections import Counter
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
    stream_open_words_with_tail,
)
from ticket51_phase15_terminal_lift_lab import compact_certificate, mismatch_reason


GENERATED_AT = "2026-07-09T08:35:00+09:00"
SCHEMA = "primeproject.ticket54-new-template-family-lab.v1"


def prefix_depth(residue: int, base_bits: int) -> dict[str, Any]:
    matched = 0
    for index, expected in enumerate(LASSO_PREFIX):
        bits = base_bits + index
        certificate = cert(residue, bits)
        key = template_key(certificate, FAMILY) if certificate.get("status") == "needs_split" else None
        if key != expected:
            return {
                "matched_prefix_templates": matched,
                "failure_offset": index,
                "failure_bits": bits,
                "expected": stringify_key(expected),
                "observed": stringify_key(key) if key else str(certificate.get("status")),
                "observed_key": key,
                "observed_next_valuation": key[3] if key else certificate.get("status"),
                "reason": mismatch_reason(certificate, expected),
                "certificate": compact_certificate(certificate),
            }
        matched += 1
    return {
        "matched_prefix_templates": matched,
        "failure_offset": None,
        "failure_bits": None,
        "expected": None,
        "observed": None,
        "observed_key": None,
        "observed_next_valuation": None,
        "reason": "full_lasso_prefix_match",
        "certificate": None,
    }


def exact_32bit_post_terminal_reaudit(example_limit: int = 8) -> dict[str, Any]:
    target = (0, START_TAIL, START_RESIDUE_MOD_256, START_NEXT_VALUATION)
    depth_counts: Counter[int] = Counter()
    failure_reason_counts: Counter[str] = Counter()
    phase5_next_valuation_counts: Counter[str] = Counter()
    phase5_template_counts: Counter[str] = Counter()
    phase5_examples: list[dict[str, Any]] = []
    depth15_roots: list[int] = []
    strongest_remaining_examples: list[dict[str, Any]] = []
    total = 0
    max_remaining_depth = 0

    for word in stream_open_words_with_tail(32):
        residue = residue_for_word(word)
        certificate = cert(residue, 32)
        if certificate.get("status") != "needs_split" or template_key(certificate, FAMILY) != target:
            continue
        total += 1
        depth = prefix_depth(residue, 32)
        matched = int(depth["matched_prefix_templates"])
        depth_counts[matched] += 1
        failure_reason_counts[str(depth["reason"])] += 1

        if matched == 15:
            depth15_roots.append(residue)
            continue

        max_remaining_depth = max(max_remaining_depth, matched)
        if matched == 5:
            observed_key = depth.get("observed_key")
            observed_next = str(depth.get("observed_next_valuation"))
            observed_template = stringify_key(observed_key) if observed_key else str(depth.get("observed"))
            phase5_next_valuation_counts[observed_next] += 1
            phase5_template_counts[observed_template] += 1
            if len(phase5_examples) < example_limit:
                phase5_examples.append(
                    {
                        "residue": residue,
                        "bits": 32,
                        "observed_template": observed_template,
                        "observed_next_valuation": observed_next,
                        "failure_reason": depth["reason"],
                        "prefix_word_tail": list(word[-12:]),
                    }
                )

        if matched == max_remaining_depth and len(strongest_remaining_examples) < example_limit:
            strongest_remaining_examples.append(
                {
                    "residue": residue,
                    "bits": 32,
                    "matched_prefix_templates": matched,
                    "failure_offset": depth["failure_offset"],
                    "expected": depth["expected"],
                    "observed": depth["observed"],
                    "reason": depth["reason"],
                }
            )

    top_phase5_templates = [
        {"observed_template": template, "count": count}
        for template, count in phase5_template_counts.most_common(8)
    ]
    return {
        "bits": 32,
        "target_template": stringify_key(target),
        "exact_start_template_matches": total,
        "depth_counts": {str(depth): depth_counts[depth] for depth in sorted(depth_counts)},
        "discarded_depth15_family_roots": sorted(depth15_roots),
        "discarded_depth15_family_count": len(depth15_roots),
        "remaining_after_ticket53_discard": total - len(depth15_roots),
        "max_remaining_depth_after_ticket53_discard": max_remaining_depth,
        "phase5_gate_count": depth_counts.get(5, 0),
        "phase5_expected_template": stringify_key(LASSO_PREFIX[5]),
        "phase5_next_valuation_counts": {
            key: phase5_next_valuation_counts[key]
            for key in sorted(phase5_next_valuation_counts, key=lambda value: int(value) if value.isdigit() else 10**9)
        },
        "phase5_exact_next10_failure_count": phase5_next_valuation_counts.get("10", 0),
        "top_phase5_gate_templates": top_phase5_templates,
        "phase5_gate_examples": phase5_examples,
        "strongest_remaining_examples": strongest_remaining_examples,
    }


def sampled_48bit_post_terminal_summary(ticket52: dict[str, Any]) -> dict[str, Any]:
    collatz = next(attempt for attempt in ticket52["attempts"] if attempt["problem_id"] == "collatz")
    sample = collatz["bounded_result"]["frontier_budget_audit"]["sampled_48bit_frontier"]
    counts = {int(key): int(value) for key, value in sample["lasso_prefix_depth_counts"].items()}
    depth15 = int(counts.get(15, 0))
    remaining_depths = [depth for depth, count in counts.items() if depth != 15 and count > 0]
    strongest = []
    for row in sample.get("strongest_examples", []):
        if int(row.get("lasso_prefix_depth", 0)) == 15:
            continue
        failure = row.get("first_failure", {})
        strongest.append(
            {
                "sample_index": row.get("sample_index"),
                "residue": row.get("residue"),
                "bits": row.get("bits"),
                "matched_prefix_templates": row.get("lasso_prefix_depth"),
                "expected": failure.get("expected"),
                "observed": failure.get("observed"),
                "reason": mismatch_reason(failure.get("certificate", {}), LASSO_PREFIX[int(failure.get("offset", 0))])
                if isinstance(failure, dict) and failure.get("certificate") is not None
                else failure.get("reason"),
            }
        )
        if len(strongest) >= 8:
            break
    return {
        "bits": sample.get("bits"),
        "sample_seed": sample.get("sample_seed"),
        "sample_count": sample.get("sample_count"),
        "statistics": sample.get("statistics"),
        "depth_counts": sample.get("lasso_prefix_depth_counts"),
        "discarded_depth15_sample_count": depth15,
        "remaining_after_ticket53_discard": int(sample.get("statistics", {}).get("start_template_match", 0)) - depth15,
        "max_remaining_depth_after_ticket53_discard": max(remaining_depths) if remaining_depths else 0,
        "phase5_gate_sample_count": int(counts.get(5, 0)),
        "strongest_remaining_examples": strongest,
        "sample_boundary": (
            "The 48-bit numbers are a deterministic sample from TICKET52, not exhaustive coverage of the 48-bit "
            "frontier."
        ),
    }


def collatz_attempt(ticket53: dict[str, Any], ticket52: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket53["attempts"] if attempt["problem_id"] == "collatz")
    terminal = prior["bounded_result"]["symbolic_terminal_theorem_audit"]
    exact32 = exact_32bit_post_terminal_reaudit()
    sample48 = sampled_48bit_post_terminal_summary(ticket52)
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-54",
        "route": "NewTemplateFamilyExtractionOrGlobalDescentInvariant",
        "status": "post_terminal_family_pruned_new_gate_family_open_problem_open",
        "proof_or_counterexample_mode": "post-terminal family extraction",
        "attempt": (
            "Do not re-sample the TICKET53 terminal family. Remove that family, then ask what the strongest "
            "remaining concrete family is and what theorem would be required to turn it into a proof or a "
            "counterexample."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "new_template_family_audit": {
                "family": FAMILY,
                "discarded_family": {
                    "source_theorem": terminal.get("theorem_name"),
                    "checked_roots": [
                        {"base_bits": row.get("base_bits"), "residue": row.get("residue")}
                        for row in terminal.get("machine_checked_roots", [])
                    ],
                    "terminal_target_match_count": terminal.get("terminal_target_match_count"),
                    "reason": "low branch consumes valuation 10; high branch forces valuation 9",
                },
                "exact_32bit_post_terminal_reaudit": exact32,
                "sampled_48bit_post_terminal_summary": sample48,
                "new_candidate_family": {
                    "name": "Phase5ValuationGate",
                    "evidence": (
                        "After the TICKET53 phase-15 family is removed, the exact 32-bit start-template search has "
                        f"max remaining lasso-prefix depth {exact32['max_remaining_depth_after_ticket53_discard']}, "
                        f"with {exact32['phase5_gate_count']} roots stopped at the phase-5 next-valuation gate. "
                        "The deterministic 48-bit sample shows the same post-discard max remaining depth 5."
                    ),
                    "candidate_theorem": (
                        "Every phase-compatible start that reaches the first five lasso templates either belongs to "
                        "the discarded phase-15 terminal family, closes by descent, or fails the phase-5 "
                        "next_valuation=10 gate."
                    ),
                    "counterexample_target": (
                        "Find a root outside the TICKET53 terminal family that reaches phase 5 with "
                        "next_valuation=10 and then survives into a different replayable lasso template."
                    ),
                },
                "global_invariant_candidate": {
                    "source": "TICKET43 finite template rank",
                    "status": "retained_as_bounded_measure_not_global_proof",
                    "needed_upgrade": (
                        "Prove that future template lifts preserve an acyclic rank order or replace the finite rank "
                        "table with a parametric measure. A blind one-horizon extension was deprioritized because "
                        "it does not by itself create an infinite theorem."
                    ),
                },
                "discarded_routes": [
                    "repeating random samples inside the TICKET53 terminal family",
                    "treating the 26-bit finite template-rank measure as a Collatz proof",
                    "blindly enlarging the template graph without a parametric closure theorem",
                ],
                "next_frontier": (
                    "CO-TICKET-55 should attack the Phase5ValuationGate theorem directly: either prove the gate "
                    "for every remaining phase-compatible lift or produce a concrete root outside the discarded "
                    "family that crosses the gate."
                ),
                "proof_boundary": (
                    "No Collatz proof and no Collatz counterexample. TICKET54 only prunes one terminal family and "
                    "extracts the next finite family to attack. The phase-5 gate still needs an all-lift theorem or "
                    "a genuine counterexample witness."
                ),
            },
        },
        "obstruction": (
            "After removing the terminally impossible phase-15 family, the remaining bounded frontier collapses to "
            "a phase-5 next-valuation gate. That gate is still finite evidence, not an infinite descent theorem."
        ),
        "candidate_theorem": (
            "Phase5ValuationGate: every remaining phase-compatible start either closes, enters the discarded "
            "terminal family, or fails next_valuation=10 at phase 5."
        ),
        "next_experiment": "Generate CO-TICKET-55 by proving or refuting the Phase5ValuationGate theorem.",
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
        "proof_or_counterexample_mode": "post-terminal family triage",
        "attempt": (
            "Transfer TICKET54's rule: after a local no-go theorem removes one witness family, recompute the "
            "remaining strongest family instead of continuing to sample the discarded route."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior.get("route"),
            "ticket54_transfer": route,
            "candidate_theorem": candidate_theorem,
            "frontier_rule": (
                "The next theorem must be stated on the strongest remaining family after every known no-go family "
                "has been removed."
            ),
        },
        "obstruction": (
            "This transfer is a proof-search discipline. It does not solve the target problem, but it prevents a "
            "closed witness family from consuming the next search budget."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Extract the strongest remaining problem-specific family after excluding the current local no-go family.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket53 = read_json(ROOT / "data/open-problem/ticket53-symbolic-terminal-theorem-lab.json")
    ticket52 = read_json(ROOT / "data/open-problem/ticket52-frontier-budget-lab.json")
    attempts = [
        transfer_attempt(
            ticket53,
            "riemann",
            "RH-TICKET-54",
            "PostNoGoZeroFamilyTriage",
            "After any off-critical zero-kernel family is locally excluded, prove the strongest remaining zero family is impossible or produce a replayable zero witness.",
        ),
        collatz_attempt(ticket53, ticket52),
        transfer_attempt(
            ticket53,
            "goldbach",
            "GB-TICKET-54",
            "PostNoGoExceptionalFamilyTriage",
            "After a residue-margin family is locally excluded, identify the strongest remaining exceptional family and prove a positive lower bound for it.",
        ),
        transfer_attempt(
            ticket53,
            "twin-prime",
            "TP-TICKET-54",
            "PostNoGoGapFamilyTriage",
            "After a gap-selector family is locally excluded, identify the strongest remaining exact-gap family and prove an unconditional gap-2 lower bound for it.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "new_template_family_extracted_open_no_resolution",
        "claim_boundary": (
            "Ticket 54 extracts the next finite family after TICKET53. It does not prove or disprove RH, Collatz, "
            "Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket54-new-template-family-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-54-post-nogo-family-triage.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-54-new-template-family.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-54-post-nogo-family-triage.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-54-post-nogo-family-triage.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
