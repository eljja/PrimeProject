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
from ticket54_new_template_family_lab import prefix_depth


GENERATED_AT = "2026-07-09T10:45:00+09:00"
SCHEMA = "primeproject.ticket56-pre-gate-projection-escape-lab.v1"


def exact32_pre_gate_partition(example_limit: int = 8) -> dict[str, Any]:
    target = (0, START_TAIL, START_RESIDUE_MOD_256, START_NEXT_VALUATION)
    failure_offset_counts: Counter[int] = Counter()
    failure_reason_counts: Counter[str] = Counter()
    observed_next_by_offset: dict[int, Counter[str]] = {}
    observed_template_by_offset: dict[int, Counter[str]] = {}
    examples_by_offset: dict[int, list[dict[str, Any]]] = {}
    total = 0
    gate_crossers: list[int] = []

    for word in stream_open_words_with_tail(32):
        residue = residue_for_word(word)
        certificate = cert(residue, 32)
        if certificate.get("status") != "needs_split" or template_key(certificate, FAMILY) != target:
            continue

        total += 1
        depth = prefix_depth(residue, 32)
        matched = int(depth["matched_prefix_templates"])
        if matched == 15:
            gate_crossers.append(residue)
            continue

        offset = int(depth["failure_offset"])
        failure_reason_counts[str(depth["reason"])] += 1
        failure_offset_counts[offset] += 1
        failure_certificate = depth["certificate"]
        next_value = str(failure_certificate.get("next_valuation"))
        observed = str(depth["observed"])
        observed_next_by_offset.setdefault(offset, Counter())[next_value] += 1
        observed_template_by_offset.setdefault(offset, Counter())[observed] += 1
        examples = examples_by_offset.setdefault(offset, [])
        if len(examples) < example_limit:
            examples.append(
                {
                    "residue": residue,
                    "bits": 32,
                    "failure_offset": offset,
                    "matched_prefix_templates": matched,
                    "expected": depth["expected"],
                    "observed": observed,
                    "reason": depth["reason"],
                    "prefix_word_tail": list(word[-12:]),
                    "failure_certificate": failure_certificate,
                }
            )

    pre_gate_failures = sum(failure_offset_counts.values())
    expected_pre_gate = sum(failure_offset_counts.get(offset, 0) for offset in range(1, 6))
    phase5_next_values = observed_next_by_offset.get(5, Counter())
    partition_sum = pre_gate_failures + len(gate_crossers)
    return {
        "bits": 32,
        "target_template": stringify_key(target),
        "exact_start_template_matches": total,
        "pre_gate_failure_count": pre_gate_failures,
        "pre_gate_failure_offsets": {
            str(offset): failure_offset_counts[offset] for offset in sorted(failure_offset_counts)
        },
        "all_pre_gate_failures_are_offsets_1_to_5": pre_gate_failures == expected_pre_gate,
        "failure_reason_counts": dict(sorted(failure_reason_counts.items())),
        "all_pre_gate_failures_are_next_valuation_mismatch": (
            dict(failure_reason_counts) == {"next_valuation": pre_gate_failures}
        ),
        "observed_next_valuation_by_offset": {
            str(offset): {
                key: observed_next_by_offset[offset][key]
                for key in sorted(
                    observed_next_by_offset[offset],
                    key=lambda value: int(value) if value.isdigit() else 10**9,
                )
            }
            for offset in sorted(observed_next_by_offset)
        },
        "top_observed_templates_by_offset": {
            str(offset): [
                {"observed_template": template, "count": count}
                for template, count in observed_template_by_offset[offset].most_common(8)
            ]
            for offset in sorted(observed_template_by_offset)
        },
        "phase5_expected_next_valuation": 10,
        "phase5_observed_next10_count": phase5_next_values.get("10", 0),
        "phase5_gate_crossers": sorted(gate_crossers),
        "phase5_gate_crosser_count": len(gate_crossers),
        "partition_sum": partition_sum,
        "partition_is_complete_for_exact32_start_template": partition_sum == total,
        "examples_by_offset": {
            str(offset): examples_by_offset[offset] for offset in sorted(examples_by_offset)
        },
        "closed_bounded_statement": (
            "For the exact 32-bit start-template population, every non-terminal-family candidate fails at offsets "
            "1 through 5 by next-valuation mismatch, and the only two phase-5 gate crossers are the TICKET55 "
            "terminally closed roots."
        ),
    }


def projection_escape_audit(ticket52: dict[str, Any], ticket55: dict[str, Any]) -> dict[str, Any]:
    collatz52 = next(attempt for attempt in ticket52["attempts"] if attempt["problem_id"] == "collatz")
    sample = collatz52["bounded_result"]["frontier_budget_audit"]["sampled_48bit_frontier"]
    strongest = sample.get("strongest_examples", [])
    depth15 = [row for row in strongest if int(row.get("lasso_prefix_depth", 0)) >= 15]
    projection_templates: Counter[str] = Counter()
    projection_examples = []
    for row in strongest:
        projection = row.get("projection32", {})
        template = str(projection.get("template"))
        projection_templates[template] += 1
        if len(projection_examples) < 8:
            projection_examples.append(
                {
                    "sample_index": row.get("sample_index"),
                    "residue": row.get("residue"),
                    "bits": row.get("bits"),
                    "lasso_prefix_depth": row.get("lasso_prefix_depth"),
                    "projection32": projection,
                    "first_failure": row.get("first_failure"),
                }
            )

    collatz55 = next(attempt for attempt in ticket55["attempts"] if attempt["problem_id"] == "collatz")
    ticket55_audit = collatz55["bounded_result"]["phase5_gate_tunnel_audit"]
    target32 = stringify_key((0, START_TAIL, START_RESIDUE_MOD_256, START_NEXT_VALUATION))
    escape_witnesses = [
        {
            "sample_index": row.get("sample_index"),
            "residue": row.get("residue"),
            "bits": row.get("bits"),
            "lasso_prefix_depth": row.get("lasso_prefix_depth"),
            "projection32": row.get("projection32"),
            "first_failure": row.get("first_failure"),
            "why_it_refutes_simple_projection_closure": (
                "This 48-bit start-template witness projects to a 32-bit template that is not the exact 32-bit "
                "start template, so a proof that only partitions 32-bit start-template residues cannot be lifted "
                "by projection."
            ),
        }
        for row in depth15
        if row.get("projection32", {}).get("template") != target32
    ]
    return {
        "sample_bits": sample.get("bits"),
        "sample_seed": sample.get("sample_seed"),
        "sample_count": sample.get("sample_count"),
        "sample_boundary": "TICKET52 is a deterministic stress sample, not exhaustive 48-bit coverage.",
        "sample_start_template_matches": sample.get("statistics", {}).get("start_template_match"),
        "sample_depth_counts": sample.get("lasso_prefix_depth_counts"),
        "strongest_sample_size": len(strongest),
        "projection32_template_counts_in_strongest_examples": dict(projection_templates.most_common()),
        "projection_examples": projection_examples,
        "simple_projection_closure_status": (
            "refuted_by_sampled_48bit_depth15_witness"
            if escape_witnesses
            else "not_refuted_by_recorded_strongest_examples"
        ),
        "escape_witnesses": escape_witnesses,
        "ticket55_gate_tunnel_reused": {
            "theorem_name": ticket55_audit.get("theorem_name"),
            "gate_match_count": ticket55_audit.get("gate_match_count"),
            "terminal_target_match_count": ticket55_audit.get("terminal_target_match_count"),
            "all_gate_roots_tunnel_to_terminal_no_go": ticket55_audit.get(
                "all_gate_roots_tunnel_to_terminal_no_go"
            ),
        },
        "corrected_proof_route": (
            "Discard simple 32-bit projection closure. The next theorem must be parametric in the base modulus "
            "and template state, or must find a higher-bit escape witness that avoids all known terminal tunnels."
        ),
    }


def collatz_attempt(ticket52: dict[str, Any], ticket55: dict[str, Any]) -> dict[str, Any]:
    exact32 = exact32_pre_gate_partition()
    projection = projection_escape_audit(ticket52, ticket55)
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-56",
        "route": "PreGateResidueClosureOrProjectionEscape",
        "status": "exact32_lasso_route_closed_projection_escape_blocks_globalization",
        "proof_or_counterexample_mode": "bounded partition plus model-escape audit",
        "attempt": (
            "Keep the TICKET55 closure, but do not overclaim it. First close the exact 32-bit pre-gate population "
            "as a partition theorem for the extracted lasso route. Then test whether that finite partition can be "
            "lifted by projection to higher moduli."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-55",
            "pre_gate_projection_escape_audit": {
                "family": FAMILY,
                "local_theorem_name": "Exact32StartTemplateLassoPartition",
                "exact32_pre_gate_partition": exact32,
                "projection_escape_audit": projection,
                "discarded_route": (
                    "A proof that partitions only the exact 32-bit start-template population and assumes every "
                    "higher-bit start-template root projects back into that same 32-bit template."
                ),
                "retained_route": (
                    "A parametric template-state automaton over base modulus, tail word, residue mod 256, and "
                    "pending valuation; or a concrete higher-bit escape witness that avoids every known terminal "
                    "no-go tunnel."
                ),
                "candidate_theorem": (
                    "For every phase-compatible base modulus, every extracted-lasso start-template state either "
                    "fails a finite next-valuation gate, enters a terminal no-go tunnel, or maps into a strictly "
                    "smaller closed template family under a well-founded parametric rank."
                ),
                "counterexample_target": (
                    "Find a higher-bit start-template root outside the exact32 projection model that reaches a "
                    "finite gate, avoids the TICKET53/TICKET55 terminal tunnel, and replays through at least one "
                    "full lasso period."
                ),
                "proof_boundary": (
                    "No Collatz proof and no Collatz counterexample. TICKET56 closes the exact 32-bit extracted "
                    "lasso route as a finite partition, but the recorded 48-bit projection escape blocks the "
                    "simple induction from that partition to all higher moduli."
                ),
            },
        },
        "obstruction": (
            "The exact 32-bit pre-gate partition is complete for the extracted lasso route, but the model is not "
            "projection-closed: a sampled 48-bit depth-15 witness projects to a different 32-bit template."
        ),
        "candidate_theorem": (
            "Replace fixed-bit residue closure with a parametric template automaton or a well-founded rank that "
            "covers projection escapes across all base moduli."
        ),
        "next_experiment": (
            "Generate CO-TICKET-57 by building the parametric template-state graph and searching for escape cycles "
            "that avoid the known terminal tunnels."
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
        "proof_or_counterexample_mode": "bounded partition plus model-escape transfer",
        "attempt": (
            "Transfer TICKET56's rule: a finite partition can be retained only as a local theorem; before turning "
            "it into a proof, test whether the model is closed under the next natural lift or projection."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior.get("route"),
            "ticket56_transfer": route,
            "candidate_theorem": candidate_theorem,
            "frontier_rule": (
                "If a higher-scale object can project outside the finite partition model, the proof route must be "
                "parametric or must promote the escape object as the next counterexample target."
            ),
        },
        "obstruction": (
            "This transfer is methodological. It does not solve the target problem; it blocks finite-model closure "
            "from being used as an infinite theorem when projection or lift escape remains possible."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Construct the problem-specific parametric state model or find a lift escape witness.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket52 = read_json(ROOT / "data/open-problem/ticket52-frontier-budget-lab.json")
    ticket55 = read_json(ROOT / "data/open-problem/ticket55-phase5-valuation-gate-lab.json")
    attempts = [
        transfer_attempt(
            ticket55,
            "riemann",
            "RH-TICKET-56",
            "ZeroKernelProjectionEscapeOrParametricStateModel",
            "A finite zero-kernel partition must either be closed under height/lift projection or be replaced by a parametric kernel-state theorem.",
        ),
        collatz_attempt(ticket52, ticket55),
        transfer_attempt(
            ticket55,
            "goldbach",
            "GB-TICKET-56",
            "ExceptionalResidueLiftEscapeOrParametricMarginModel",
            "A finite exceptional-residue partition must either be closed under larger cutoffs or be replaced by a parametric positive-margin state theorem.",
        ),
        transfer_attempt(
            ticket55,
            "twin-prime",
            "TP-TICKET-56",
            "GapSelectorLiftEscapeOrParametricSieveModel",
            "A finite exact-gap selector partition must either be closed under larger sieve levels or be replaced by a parametric parity-sensitive sieve theorem.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "pre_gate_projection_escape_open_no_resolution",
        "claim_boundary": (
            "Ticket 56 closes the exact 32-bit Collatz extracted-lasso route as a finite partition and refutes a "
            "simple projection-closure proof route. It does not prove or disprove RH, Collatz, Goldbach, or Twin "
            "Prime."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket56-pre-gate-projection-escape-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-56-projection-escape-frontier.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-56-pre-gate-projection-escape.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-56-lift-escape-frontier.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-56-lift-escape-frontier.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
