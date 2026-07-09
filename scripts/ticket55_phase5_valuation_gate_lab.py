from __future__ import annotations

import json
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key, template_key
from ticket43_lift_constraint_measure_lab import FAMILY
from ticket50_phase_lift_exception_lab import LASSO_PREFIX
from ticket51_phase15_terminal_lift_lab import compact_certificate, mismatch_reason


GENERATED_AT = "2026-07-09T09:20:00+09:00"
SCHEMA = "primeproject.ticket55-phase5-valuation-gate-lab.v1"


def root_set(ticket53: dict[str, Any], ticket54: dict[str, Any]) -> list[dict[str, Any]]:
    collatz53 = next(attempt for attempt in ticket53["attempts"] if attempt["problem_id"] == "collatz")
    roots53 = collatz53["bounded_result"]["symbolic_terminal_theorem_audit"]["machine_checked_roots"]
    known = {
        (int(row["base_bits"]), int(row["residue"])): {
            "base_bits": int(row["base_bits"]),
            "residue": int(row["residue"]),
            "source_ticket": row.get("source_ticket", "TICKET-53"),
        }
        for row in roots53
    }
    collatz54 = next(attempt for attempt in ticket54["attempts"] if attempt["problem_id"] == "collatz")
    exact32 = collatz54["bounded_result"]["new_template_family_audit"]["exact_32bit_post_terminal_reaudit"]
    for residue in exact32.get("discarded_depth15_family_roots", []):
        known.setdefault(
            (32, int(residue)),
            {"base_bits": 32, "residue": int(residue), "source_ticket": "TICKET-54-exact32"},
        )
    return [known[key] for key in sorted(known)]


def key_for(certificate: dict[str, Any]) -> tuple[Any, ...] | None:
    return template_key(certificate, FAMILY) if certificate.get("status") == "needs_split" else None


def gate_tunnel_audit(row: dict[str, Any]) -> dict[str, Any]:
    residue = int(row["residue"])
    base_bits = int(row["base_bits"])
    gate_bits = base_bits + 5
    terminal_bits = base_bits + 15
    gate = cert(residue, gate_bits)
    gate_key = key_for(gate)
    gate_target = LASSO_PREFIX[5]
    gate_consumed = int(gate.get("consumed_bits", -1))
    gate_prefix_length = int(gate.get("prefix_length", -1))
    gate_word = tuple(gate.get("prefix_word", []))
    gate_next = int(gate.get("next_valuation", -1)) if gate.get("next_valuation") is not None else None

    tunnel_rows = []
    for offset in range(5, 15):
        bits = base_bits + offset
        certificate = cert(residue, bits)
        observed = key_for(certificate)
        expected = LASSO_PREFIX[offset]
        tunnel_rows.append(
            {
                "offset": offset,
                "bits": bits,
                "expected": stringify_key(expected),
                "observed": stringify_key(observed) if observed else str(certificate.get("status")),
                "matches_expected": observed == expected,
                "same_pending_certificate": (
                    certificate.get("status") == "needs_split"
                    and tuple(certificate.get("prefix_word", [])) == gate_word
                    and int(certificate.get("consumed_bits", -2)) == gate_consumed
                    and int(certificate.get("prefix_length", -2)) == gate_prefix_length
                    and int(certificate.get("next_valuation", -2)) == gate_next
                ),
                "certificate": compact_certificate(certificate),
            }
        )

    terminal = cert(residue, terminal_bits)
    terminal_key = key_for(terminal)
    terminal_target = LASSO_PREFIX[15]
    return {
        "source_ticket": row.get("source_ticket"),
        "base_bits": base_bits,
        "residue": residue,
        "gate_bits": gate_bits,
        "terminal_bits": terminal_bits,
        "gate_expected": stringify_key(gate_target),
        "gate_observed": stringify_key(gate_key) if gate_key else str(gate.get("status")),
        "gate_matches": gate_key == gate_target,
        "gate_consumed_bits": gate.get("consumed_bits"),
        "gate_prefix_length": gate.get("prefix_length"),
        "gate_next_valuation": gate.get("next_valuation"),
        "gate_consumed_equals_gate_bits": gate_consumed == gate_bits,
        "gate_next_reaches_terminal_bits": gate_next is not None and gate_consumed + gate_next == terminal_bits,
        "tunnel_offsets": tunnel_rows,
        "tunnel_all_offsets_match": all(item["matches_expected"] for item in tunnel_rows),
        "tunnel_all_offsets_same_pending_certificate": all(item["same_pending_certificate"] for item in tunnel_rows),
        "terminal_expected": stringify_key(terminal_target),
        "terminal_observed": stringify_key(terminal_key) if terminal_key else str(terminal.get("status")),
        "terminal_reason": mismatch_reason(terminal, terminal_target),
        "terminal_target_matched": terminal_key == terminal_target,
        "terminal_certificate": compact_certificate(terminal),
    }


def collatz_attempt(ticket53: dict[str, Any], ticket54: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket54["attempts"] if attempt["problem_id"] == "collatz")
    roots = root_set(ticket53, ticket54)
    audits = [gate_tunnel_audit(row) for row in roots]
    all_gate_match = all(row["gate_matches"] for row in audits)
    all_tunnel = all(row["tunnel_all_offsets_match"] for row in audits)
    all_same_pending = all(row["tunnel_all_offsets_same_pending_certificate"] for row in audits)
    all_terminal_closed = all(not row["terminal_target_matched"] for row in audits)
    ticket54_audit = prior["bounded_result"]["new_template_family_audit"]
    exact32 = ticket54_audit["exact_32bit_post_terminal_reaudit"]
    sample48 = ticket54_audit["sampled_48bit_post_terminal_summary"]
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-55",
        "route": "Phase5ValuationGateTheoremOrCounterexample",
        "status": "local_phase5_gate_tunnel_closed_open_problem_open",
        "proof_or_counterexample_mode": "symbolic gate-to-terminal tunnel",
        "attempt": (
            "Do not enlarge the sample. Prove the local tunnel: a root that reaches the phase-5 gate with "
            "consumed_bits equal to the gate modulus keeps the same pending valuation through phases 6-14 and "
            "must hit the TICKET53 terminal mismatch at phase 15."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "phase5_gate_tunnel_audit": {
                "family": FAMILY,
                "theorem_name": "Phase5GateToTerminalTunnel",
                "premises": [
                    "cert(r, b+5) matches [5,[1,1,1,1],103,10]",
                    "cert(r, b+5) has consumed_bits = b+5",
                    "the same low-lift residue r is tested at b+6 through b+15",
                ],
                "symbolic_argument": (
                    "Because the pending valuation is 10 and the phase-5 certificate has consumed exactly b+5 "
                    "bits, increasing the modulus by one bit cannot consume the pending valuation until b+15. "
                    "Therefore offsets 6 through 14 preserve the same prefix word, consumed bit count, residue "
                    "class, and next valuation while only the phase coordinate changes. At b+15 the pending "
                    "valuation 10 is consumed, so the terminal certificate either closes by descent or has tail "
                    "[1,1,1,10], not the target tail [1,1,1,1]."
                ),
                "machine_checked_roots": audits,
                "gate_match_count": sum(1 for row in audits if row["gate_matches"]),
                "tunnel_match_count": sum(1 for row in audits if row["tunnel_all_offsets_match"]),
                "same_pending_certificate_count": sum(
                    1 for row in audits if row["tunnel_all_offsets_same_pending_certificate"]
                ),
                "terminal_target_match_count": sum(1 for row in audits if row["terminal_target_matched"]),
                "all_gate_roots_tunnel_to_terminal_no_go": all_gate_match
                and all_tunnel
                and all_same_pending
                and all_terminal_closed,
                "bounded_32bit_closure": {
                    "exact_start_template_matches": exact32.get("exact_start_template_matches"),
                    "failed_before_or_at_phase5": int(exact32.get("remaining_after_ticket53_discard", 0)),
                    "gate_crossers": exact32.get("discarded_depth15_family_count"),
                    "gate_crossers_terminally_closed": sum(
                        1 for row in audits if int(row["base_bits"]) == 32 and not row["terminal_target_matched"]
                    ),
                    "interpretation": (
                        "Within the exact 32-bit start-template population, every candidate either fails before or "
                        "at the phase-5 gate, or crosses the gate and then tunnels into the TICKET53 terminal no-go."
                    ),
                },
                "sampled_48bit_closure": {
                    "sample_count": sample48.get("sample_count"),
                    "post_discard_max_depth": sample48.get("max_remaining_depth_after_ticket53_discard"),
                    "phase5_gate_sample_count": sample48.get("phase5_gate_sample_count"),
                    "gate_crossers_terminally_closed": sum(
                        1 for row in audits if int(row["base_bits"]) == 48 and not row["terminal_target_matched"]
                    ),
                    "sample_boundary": sample48.get("sample_boundary"),
                },
                "next_frontier": (
                    "CO-TICKET-56 should either prove a residue-class theorem for all phase-compatible starts that "
                    "fail before or at phase 5, or find a root outside the current low-lift start-template model."
                ),
                "proof_boundary": (
                    "No Collatz proof and no Collatz counterexample. TICKET55 proves a local gate-to-terminal "
                    "tunnel for the extracted low-lift family and closes the exact 32-bit start-template lasso "
                    "route, but it does not cover all possible Collatz trajectories, all base moduli, or all "
                    "template families."
                ),
            },
        },
        "obstruction": (
            "Crossing the phase-5 next_valuation=10 gate does not create a new counterexample route in the "
            "extracted family; it forces the same pending valuation through phase 14 and then hits the phase-15 "
            "terminal mismatch."
        ),
        "candidate_theorem": (
            "Globalize the phase-5 gate: every phase-compatible start outside the extracted low-lift family must "
            "also fail before or at a finite valuation gate, or enter a separately terminally closed family."
        ),
        "next_experiment": "Generate CO-TICKET-56 by attacking the pre-gate failure population or by escaping the current low-lift template model.",
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
        "proof_or_counterexample_mode": "gate-to-terminal tunnel transfer",
        "attempt": (
            "Transfer TICKET55's rule: if the strongest remaining family crosses a finite gate, prove whether that "
            "gate forces it into a known terminal no-go family before searching a larger sample."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior.get("route"),
            "ticket55_transfer": route,
            "candidate_theorem": candidate_theorem,
            "frontier_rule": (
                "A gate-crosser should be promoted only if it avoids every known terminal no-go tunnel."
            ),
        },
        "obstruction": (
            "This transfer is methodological. It does not solve the target problem; it turns a gate crossing into a "
            "terminal/no-go theorem obligation before treating it as a counterexample candidate."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Prove the problem-specific gate-to-terminal tunnel or exhibit a gate-crosser that avoids all known no-go tunnels.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket53 = read_json(ROOT / "data/open-problem/ticket53-symbolic-terminal-theorem-lab.json")
    ticket54 = read_json(ROOT / "data/open-problem/ticket54-new-template-family-lab.json")
    attempts = [
        transfer_attempt(
            ticket54,
            "riemann",
            "RH-TICKET-55",
            "ZeroGateToTerminalNoGoTunnel",
            "If a strongest off-critical zero family crosses its finite gate, prove it tunnels into a known sign or boundary no-go family, or produce a zero witness that avoids that tunnel.",
        ),
        collatz_attempt(ticket53, ticket54),
        transfer_attempt(
            ticket54,
            "goldbach",
            "GB-TICKET-55",
            "ExceptionalGateToPositiveMarginTunnel",
            "If a strongest exceptional residue family crosses a finite margin gate, prove it tunnels into a positive-margin theorem or produce an explicit exceptional even witness.",
        ),
        transfer_attempt(
            ticket54,
            "twin-prime",
            "TP-TICKET-55",
            "GapGateToTerminalNoGoTunnel",
            "If a strongest exact-gap selector family crosses a finite gate, prove it tunnels into a known leakage/no-go family or produce a replayable gap-2 witness.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "phase5_gate_tunnel_open_no_resolution",
        "claim_boundary": (
            "Ticket 55 proves a local gate-to-terminal tunnel for the extracted Collatz family. It does not prove "
            "or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket55-phase5-valuation-gate-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-55-gate-terminal-tunnel.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-55-phase5-gate-tunnel.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-55-gate-terminal-tunnel.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-55-gate-terminal-tunnel.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
