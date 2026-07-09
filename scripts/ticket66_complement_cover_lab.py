from __future__ import annotations

import json
from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key
from ticket58_affine_boundary_lift_lab import key_for
from ticket59_symbolic_lift_mismatch_lab import target_template
from ticket65_start_template_chain_extinction_lab import START_BITS, build_chain, make_gate_candidate_rows


GENERATED_AT = "2026-07-09T23:40:00+09:00"
SCHEMA = "primeproject.ticket66-complement-cover-lab.v1"
TOP_LIMIT = 12
EXAMPLE_LIMIT = 8


def counter_rows(counter: Counter[str], *, limit: int = TOP_LIMIT) -> list[dict[str, Any]]:
    return [{"key": key, "count": count} for key, count in counter.most_common(limit)]


def classify_open_reason(key: tuple[Any, ...], target: tuple[Any, ...]) -> str:
    _, tail4, residue_mod, next_valuation = key
    _, target_tail4, target_residue_mod, target_next_valuation = target
    if tuple(tail4) == tuple(target_tail4) and residue_mod == target_residue_mod and next_valuation != target_next_valuation:
        return "open_target_tail_wrong_next_valuation"
    if tuple(tail4) == tuple(target_tail4) and residue_mod != target_residue_mod:
        return "open_target_tail_wrong_residue_mod_256"
    if tuple(tail4) != tuple(target_tail4) and residue_mod == target_residue_mod:
        return "open_wrong_tail_target_residue_mod_256"
    return "open_wrong_tail_or_residue"


def compact_certificate(certificate: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": certificate.get("status"),
        "residue": certificate.get("residue"),
        "modulus_bits": certificate.get("modulus_bits"),
        "prefix_length": certificate.get("prefix_length"),
        "consumed_bits": certificate.get("consumed_bits"),
        "next_valuation": certificate.get("next_valuation"),
        "coefficient_log2_debt": certificate.get("coefficient_log2_debt"),
        "coefficient_log2_margin": certificate.get("coefficient_log2_margin"),
        "threshold_min_n_for_descent": certificate.get("threshold_min_n_for_descent"),
        "prefix_tail8": list(certificate.get("prefix_word", [])[-8:]),
    }


def analyze_complement() -> dict[str, Any]:
    chain = build_chain()
    parent_rows = chain["lifted_56"]["rows"]
    parent_bits = START_BITS
    per_lift: list[dict[str, Any]] = []
    global_status: Counter[str] = Counter()
    global_reasons: Counter[str] = Counter()
    global_templates: Counter[str] = Counter()
    global_tail4: Counter[str] = Counter()
    global_next: Counter[str] = Counter()
    descent_examples: list[dict[str, Any]] = []
    open_examples: list[dict[str, Any]] = []
    smallest_open_residue: dict[str, Any] | None = None

    for step in chain["steps"]:
        target_bits = int(step["target_bits"])
        target = target_template(target_bits)
        candidates = make_gate_candidate_rows(parent_rows, parent_bits=parent_bits, target_bits=target_bits)
        non_start = [row for row in candidates if row["gate_label"] != "start_template"]
        status_counts: Counter[str] = Counter()
        reason_counts: Counter[str] = Counter()
        templates: Counter[str] = Counter()
        tail4_counts: Counter[str] = Counter()
        next_counts: Counter[str] = Counter()

        for row in non_start:
            residue = int(row["residue"])
            certificate = cert(residue, target_bits)
            status = str(certificate.get("status"))
            status_counts[status] += 1
            global_status[status] += 1
            key = key_for(certificate)

            if status == "all_lift_descent":
                reason = "closed_all_lift_descent"
                if len(descent_examples) < EXAMPLE_LIMIT:
                    descent_examples.append(
                        {
                            "lift": f"{parent_bits}->{target_bits}",
                            "parent_index": row["parent_index"],
                            "child_top": row["top_extension"],
                            "residue": residue,
                            "certificate": compact_certificate(certificate),
                        }
                    )
            elif status == "needs_split" and key is not None:
                reason = classify_open_reason(key, target)
                template_text = stringify_key(key)
                templates[template_text] += 1
                global_templates[template_text] += 1
                tail_text = ",".join(str(value) for value in key[1])
                tail4_counts[tail_text] += 1
                global_tail4[tail_text] += 1
                next_counts[str(key[3])] += 1
                global_next[str(key[3])] += 1
                example = {
                    "lift": f"{parent_bits}->{target_bits}",
                    "parent_index": row["parent_index"],
                    "child_top": row["top_extension"],
                    "residue": residue,
                    "template": template_text,
                    "reason": reason,
                    "certificate": compact_certificate(certificate),
                }
                if len(open_examples) < EXAMPLE_LIMIT:
                    open_examples.append(example)
                if smallest_open_residue is None or residue < int(smallest_open_residue["residue"]):
                    smallest_open_residue = example
            else:
                reason = f"open_or_unknown_{status}"

            reason_counts[reason] += 1
            global_reasons[reason] += 1

        per_lift.append(
            {
                "parent_bits": parent_bits,
                "target_bits": target_bits,
                "candidate_child_rows": len(candidates),
                "start_template_count": sum(1 for row in candidates if row["gate_label"] == "start_template"),
                "non_start_template_count": len(non_start),
                "status_counts": dict(status_counts.most_common()),
                "reason_counts": dict(reason_counts.most_common()),
                "unique_open_templates": len(templates),
                "top_open_templates": counter_rows(templates, limit=8),
                "top_tail4": counter_rows(tail4_counts, limit=8),
                "next_valuation_counts": counter_rows(next_counts, limit=8),
            }
        )
        parent_rows = step["chain"]["rows"]
        parent_bits = target_bits

    total_non_start = sum(int(row["non_start_template_count"]) for row in per_lift)
    open_needs_split = int(global_status.get("needs_split", 0))
    descent_closed = int(global_status.get("all_lift_descent", 0))
    coverage_rate = descent_closed / total_non_start if total_non_start else 0.0
    open_rate = open_needs_split / total_non_start if total_non_start else 0.0
    largest_template = counter_rows(global_templates, limit=1)
    return {
        "theorem_name": "ComplementCoverForStartTemplateExit",
        "source_ticket": "CO-TICKET-65",
        "tested_lifts": [{"parent_bits": row["parent_bits"], "target_bits": row["target_bits"]} for row in per_lift],
        "total_non_start_template_candidates": total_non_start,
        "descent_closed_count": descent_closed,
        "open_needs_split_count": open_needs_split,
        "descent_coverage_rate": round(coverage_rate, 12),
        "open_needs_split_rate": round(open_rate, 12),
        "unique_open_template_count": len(global_templates),
        "global_status_counts": dict(global_status.most_common()),
        "global_reason_counts": dict(global_reasons.most_common()),
        "top_global_templates": counter_rows(global_templates),
        "top_global_tail4": counter_rows(global_tail4),
        "global_next_valuation_counts": counter_rows(global_next),
        "largest_open_template_family": largest_template[0] if largest_template else None,
        "per_lift": per_lift,
        "descent_closed_examples": descent_examples,
        "open_template_examples": open_examples,
        "smallest_open_residue": smallest_open_residue,
        "complement_cover_status": "open_complement_not_covered",
        "discarded_route": (
            "Assume that every branch leaving the TICKET65 start-template chain is already handled by the existing descent or "
            "terminal-family closures. The audit refutes that shortcut: only 55 of 17,189 complement candidates close by immediate "
            "all-lift descent."
        ),
        "retained_route": (
            "Treat the 17,134 open complement instances as a finite template frontier. A useful next proof attempt must either prove a "
            "rank/measure theorem over these 491 template families or extract a compatible infinite lift that would become a true "
            "counterexample target."
        ),
        "candidate_theorem": (
            "OpenTemplateFamilyRankOrComplementCounterexample: every open template family left by ComplementCoverForStartTemplateExit "
            "admits a well-founded symbolic rank after a finite split, or there exists a compatible infinite lift preserving one "
            "nondecreasing template family."
        ),
        "counterexample_target": (
            "A compatible infinite lift through one of the 491 open complement template families, starting with the smallest open "
            "residue or one of the largest families such as [12,[1,1,1,1],103,5]."
        ),
        "next_theorem_target": "OpenTemplateFamilyRankOrComplementCounterexample",
        "proof_boundary": (
            "TICKET66 does not prove Collatz. It shows that the currently available complement cover is insufficient: most branches "
            "leaving the TICKET65 start-template chain remain open needs_split template families."
        ),
    }


def collatz_attempt(ticket65: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket65["attempts"] if attempt["problem_id"] == "collatz")
    audit = analyze_complement()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-66",
        "route": "ComplementCoverForStartTemplateExit",
        "status": "complement_cover_failed_open_no_resolution",
        "proof_or_counterexample_mode": "bounded complement-cover falsification plus open-template frontier",
        "attempt": (
            "Test the theorem demanded by TICKET65: whether branches that exit the start-template chain are already covered by the "
            "known descent/terminal machinery, or whether they form new open template families."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "complement_cover_audit": audit,
        },
        "obstruction": (
            "The complement is not closed by the current machinery. Among 17,189 non-start-template candidates, only 55 are immediate "
            "all-lift descent closures and 17,134 remain needs_split instances across 491 open template families."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": (
            "Attack the 491 open template families with a rank search that uses only pre-replay symbolic coordinates, then try to lift "
            "the surviving family into either a proof obligation or a counterexample candidate."
        ),
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
        "proof_or_counterexample_mode": "complement-cover frontier transfer",
        "attempt": (
            "Transfer the TICKET66 lesson: a closed branch is useful only after its complement is either covered by a symbolic theorem "
            "or converted into an explicit counterexample-search frontier."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket66_transfer": route,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "Do not promote a branch closure, cutoff, or finite detector into a proof unless the complement is explicitly covered. "
                "The complement must have its own rank theorem, positivity theorem, or counterexample construction."
            ),
        },
        "obstruction": "This is a transfer discipline and open theorem target, not a solution.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Construct the problem-specific complement frontier and rank/positivity theorem, or find a branch that evades it.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket65 = read_json(ROOT / "data/open-problem/ticket65-start-template-chain-extinction-lab.json")
    attempts = [
        transfer_attempt(
            ticket65,
            "riemann",
            "RH-TICKET-66",
            "ZeroKernelComplementCoverOrPersistentBranch",
            (
                "Every zero-kernel branch outside the currently pruned window has a uniform positivity/rank cover, or there is a "
                "persistent off-critical branch candidate that the detector cannot eliminate."
            ),
            "a persistent zero-kernel branch that survives the complement cover while remaining compatible with all tested positivity constraints",
        ),
        collatz_attempt(ticket65),
        transfer_attempt(
            ticket65,
            "goldbach",
            "GB-TICKET-66",
            "GoldbachCutoffComplementCoverOrPersistentLowMargin",
            (
                "Every large-even branch outside the closed cutoff window has an explicit positive margin cover, or a persistent "
                "low-margin branch survives the cutoff theorem."
            ),
            "a large-even branch whose local margin remains below the explicit lower-bound budget after the complement cover should apply",
        ),
        transfer_attempt(
            ticket65,
            "twin-prime",
            "TP-TICKET-66",
            "TwinPrimeParityComplementCoverOrPersistentLeak",
            (
                "Every exact-gap branch outside the closed selector window has a parity-sensitive retained-mass cover, or a persistent "
                "selector leak survives all current parity filters."
            ),
            "an exact-gap branch that keeps retained mass in the parity obstruction window while evading the complement cover",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "complement_cover_open_no_resolution",
        "claim_boundary": (
            "Ticket 66 refutes the shortcut that TICKET65's complement is already covered. It does not prove or disprove any of the "
            "four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket66-complement-cover-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-66-complement-cover.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-66-complement-cover.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-66-complement-cover.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-66-complement-cover.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
