from __future__ import annotations

import json
from collections import Counter, defaultdict
from typing import Any, Callable

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key
from ticket52_frontier_budget_lab import SAMPLE_BITS, lasso_prefix_depth_at
from ticket58_affine_boundary_lift_lab import EXACT32_BITS, build_exact32_boundary, high_outcome, key_for
from ticket59_symbolic_lift_mismatch_lab import CYLINDER_LOW_BITS, prediction_for_projection, target_template
from ticket60_mixed_cylinder_separator_lab import Row, assess_separator, failure_signature
from ticket62_mod16_transition_cover_lab import mixed_base_rows, lifted_rows_for_bits


GENERATED_AT = "2026-07-09T19:35:00+09:00"
SCHEMA = "primeproject.ticket63-mod16-automaton-cover-lab.v1"
BASE_LIFT_BITS = (52, 56)
CHAIN_PARENT_BITS = 56
CHAIN_TARGET_BITS = 60
LABEL_FIELDS = ("failure_offset", "outcome_label", "prediction_label", "transition_label", "root_transition_label")


KeyFn = Callable[[Row], tuple[Any, ...]]


def classify_projection(residue: int, bits: int, observed: str, boundary: dict[tuple[int, int], dict[str, Any]]) -> tuple[str, str | None, str]:
    projection_residue = residue % (1 << EXACT32_BITS)
    projection_certificate, predicted = prediction_for_projection(projection_residue, boundary)
    projection_key = key_for(projection_certificate)
    projection_template = stringify_key(projection_key) if projection_key else str(projection_certificate.get("status"))
    if projection_key != target_template(EXACT32_BITS):
        return "projection_escape", predicted, projection_template
    if predicted == observed:
        return "boundary_match", predicted, projection_template
    return "boundary_mismatch", predicted, projection_template


def chain_lift_rows(
    parent_rows: list[Row],
    *,
    parent_bits: int,
    target_bits: int,
    boundary: dict[tuple[int, int], dict[str, Any]],
) -> dict[str, Any]:
    extra_bits = target_bits - parent_bits
    target = target_template(target_bits)
    rows: list[Row] = []
    stats: Counter[str] = Counter()
    parent_counts: Counter[tuple[int, int, int]] = Counter()
    full_period_examples: list[dict[str, Any]] = []

    for parent in parent_rows:
        low40 = int(parent["low40_residue"])
        base_high8 = int(parent["base_high_extension"])
        base_mod16 = int(parent["base_mod16"])
        parent_failure_offset = parent["failure_offset"]
        for top_extension in range(1 << extra_bits):
            stats["tested_chain_lifts"] += 1
            residue = int(parent["residue"]) | (top_extension << parent_bits)
            certificate = cert(residue, target_bits)
            if key_for(certificate) != target:
                stats["non_start_template_chain_lift"] += 1
                continue

            stats["start_template_chain_lift"] += 1
            parent_counts[(low40, base_high8, int(parent["top_extension"]))] += 1
            depth = lasso_prefix_depth_at(residue, target_bits)
            observed = high_outcome(depth)
            if observed == "full_lasso_period_replay":
                stats["full_lasso_period_replay"] += 1
                if len(full_period_examples) < 8:
                    full_period_examples.append(
                        {
                            "bits": target_bits,
                            "residue": residue,
                            "low40_residue": low40,
                            "base_high_extension": base_high8,
                            "parent_top_extension": parent["top_extension"],
                            "top_extension": top_extension,
                            "matched_prefix_templates": int(depth.get("matched_prefix_templates", 0)),
                        }
                    )
            prediction_label, predicted, projection_template = classify_projection(residue, target_bits, observed, boundary)
            stats[prediction_label] += 1
            signature = failure_signature(depth)
            rows.append(
                {
                    "bits": target_bits,
                    "parent_bits": parent_bits,
                    "low40_residue": low40,
                    "base_high_extension": base_high8,
                    "base_mod16": base_mod16,
                    "parent_top_extension": parent["top_extension"],
                    "top_extension": top_extension,
                    "high_extension": residue >> CYLINDER_LOW_BITS,
                    "residue": residue,
                    "parent_failure_offset": parent_failure_offset,
                    "base_failure_offset": parent["base_failure_offset"],
                    "outcome_label": observed,
                    "prediction_label": prediction_label,
                    "transition_label": f"{parent_failure_offset}->{signature['offset']}",
                    "root_transition_label": f"{parent['base_failure_offset']}->{signature['offset']}",
                    "matched_prefix_templates": int(depth.get("matched_prefix_templates", 0)),
                    "failure_offset": signature["offset"],
                    "failure_observed": signature["observed"],
                    "failure_next_valuation": signature["next_valuation"],
                    "failure_tail4": signature["tail4"],
                    "failure_prefix_length": signature["prefix_length"],
                    "certificate_prefix_length": int(certificate.get("prefix_length", 0)),
                    "certificate_consumed_bits": int(certificate.get("consumed_bits", 0)),
                    "projection32_template": projection_template,
                    "predicted_exact32_outcome": predicted,
                }
            )

    return {
        "bits": target_bits,
        "parent_bits": parent_bits,
        "extra_bits": extra_bits,
        "rows": rows,
        "statistics": dict(sorted(stats.items())),
        "parent_rows_with_start_template_chain_lift": len(parent_counts),
        "parent_extension_count_distribution": dict(sorted(Counter(parent_counts.values()).items())),
        "full_period_examples": full_period_examples,
    }


def state_key(row: Row) -> tuple[int, int]:
    return (int(row["low40_residue"]), int(row["base_mod16"]))


def transition_table(rows: list[Row], *, example_limit: int = 8) -> dict[str, Any]:
    states: dict[tuple[int, int], dict[str, Any]] = {}
    transition_counts: Counter[str] = Counter()
    outcome_counts: Counter[str] = Counter()
    prediction_counts: Counter[str] = Counter()
    failure_counts: Counter[str] = Counter()
    collision_states: list[dict[str, Any]] = []

    for row in rows:
        key = state_key(row)
        label_tuple = (
            str(row["failure_offset"]),
            str(row["outcome_label"]),
            str(row["prediction_label"]),
            str(row["transition_label"]),
            str(row["root_transition_label"]),
        )
        entry = states.setdefault(
            key,
            {
                "low40_residue": key[0],
                "base_mod16": key[1],
                "row_count": 0,
                "labels": Counter(),
                "examples": [],
            },
        )
        entry["row_count"] += 1
        entry["labels"][label_tuple] += 1
        if len(entry["examples"]) < 2:
            entry["examples"].append(
                {
                    "bits": row["bits"],
                    "residue": row["residue"],
                    "top_extension": row.get("top_extension"),
                    "failure_offset": row["failure_offset"],
                    "outcome_label": row["outcome_label"],
                    "prediction_label": row["prediction_label"],
                    "transition_label": row["transition_label"],
                    "root_transition_label": row["root_transition_label"],
                }
            )
        transition_counts[str(row["transition_label"])] += 1
        outcome_counts[str(row["outcome_label"])] += 1
        prediction_counts[str(row["prediction_label"])] += 1
        failure_counts[str(row["failure_offset"])] += 1

    for key, entry in states.items():
        if len(entry["labels"]) > 1:
            collision_states.append(
                {
                    "state": [key[0], key[1]],
                    "label_counts": {
                        json.dumps(label, ensure_ascii=False, separators=(",", ":")): count
                        for label, count in entry["labels"].items()
                    },
                    "examples": entry["examples"],
                }
            )

    largest_state = max((entry["row_count"] for entry in states.values()), default=0)
    sample_states = []
    for key in sorted(states)[:example_limit]:
        entry = states[key]
        labels = entry["labels"]
        sample_states.append(
            {
                "state": [key[0], key[1]],
                "row_count": entry["row_count"],
                "label_count": len(labels),
                "label_counts": {
                    json.dumps(label, ensure_ascii=False, separators=(",", ":")): count
                    for label, count in labels.items()
                },
                "examples": entry["examples"],
            }
        )

    return {
        "row_count": len(rows),
        "state_count": len(states),
        "deterministic": len(collision_states) == 0,
        "collision_state_count": len(collision_states),
        "largest_state_size": largest_state,
        "transition_label_counts": dict(transition_counts.most_common()),
        "outcome_counts": dict(outcome_counts.most_common()),
        "prediction_counts": dict(prediction_counts.most_common()),
        "failure_offset_counts": dict(failure_counts.most_common()),
        "collision_examples": collision_states[:example_limit],
        "sample_states": sample_states,
    }


def quotient_candidates() -> list[tuple[str, KeyFn]]:
    candidates: list[tuple[str, KeyFn]] = [
        ("base_mod16_only", lambda row: (row["base_mod16"],)),
    ]
    for bits in (8, 12, 16, 20, 24, 28, 32, 36, 40):
        mask = (1 << bits) - 1
        candidates.append(
            (
                f"low40_mod_2^{bits}_plus_base_mod16",
                lambda row, mask=mask, bits=bits: (bits, int(row["low40_residue"]) & mask, row["base_mod16"]),
            )
        )
    candidates.extend(
        [
            ("low40_plus_base_mod16", lambda row: (row["low40_residue"], row["base_mod16"])),
            ("low40_plus_base_high8", lambda row: (row["low40_residue"], row["base_high_extension"])),
            (
                "low40_plus_base_mod16_certificate_prefix_length",
                lambda row: (row["low40_residue"], row["base_mod16"], row["certificate_prefix_length"]),
            ),
        ]
    )
    return candidates


def quotient_ladder(rows: list[Row]) -> dict[str, Any]:
    candidates = quotient_candidates()
    ladders = {
        field: [assess_separator(rows, label, key_fn, label_field=field) for label, key_fn in candidates]
        for field in LABEL_FIELDS
    }
    joint_rows = []
    for index, (label, _) in enumerate(candidates):
        joint_rows.append(
            {
                "separator": label,
                "state_count": ladders["failure_offset"][index]["state_count"],
                "deterministic_for_all_labels": all(ladders[field][index]["deterministic"] for field in LABEL_FIELDS),
                "collision_groups": {
                    field: ladders[field][index]["collision_group_count"]
                    for field in LABEL_FIELDS
                },
                "ambiguous_rows": {
                    field: ladders[field][index]["ambiguous_row_count"]
                    for field in LABEL_FIELDS
                },
            }
        )
    first_joint = next((row for row in joint_rows if row["deterministic_for_all_labels"]), None)
    return {
        "row_count": len(rows),
        "joint_ladder": joint_rows,
        "first_joint_deterministic_separator": first_joint["separator"] if first_joint else None,
        "failure_offset_ladder": ladders["failure_offset"],
    }


def audit_rows(label: str, rows: list[Row]) -> dict[str, Any]:
    normalized_rows: list[Row] = []
    for row in rows:
        normalized = dict(row)
        normalized.setdefault("root_transition_label", normalized.get("transition_label"))
        normalized_rows.append(normalized)
    table = transition_table(normalized_rows)
    ladder = quotient_ladder(normalized_rows)
    return {
        "label": label,
        "row_count": len(normalized_rows),
        "state_table": table,
        "quotient_ladder": ladder,
        "first_quotient_separator": ladder["first_joint_deterministic_separator"],
    }


def collatz_attempt(ticket62: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket62["attempts"] if attempt["problem_id"] == "collatz")
    boundary_data = build_exact32_boundary()
    base = mixed_base_rows(boundary_data["boundary"])
    base_rows = base["mixed_rows"]
    lifted_52 = lifted_rows_for_bits(base_rows, 52, boundary_data["boundary"])
    lifted_56 = lifted_rows_for_bits(base_rows, 56, boundary_data["boundary"])
    chain_60 = chain_lift_rows(
        lifted_56["rows"],
        parent_bits=CHAIN_PARENT_BITS,
        target_bits=CHAIN_TARGET_BITS,
        boundary=boundary_data["boundary"],
    )
    row_audits = [
        audit_rows("52_bit_direct_lift", lifted_52["rows"]),
        audit_rows("56_bit_direct_lift", lifted_56["rows"]),
        audit_rows("60_bit_chained_from_56_survivors", chain_60["rows"]),
    ]
    collision_audits = [
        audit for audit in row_audits if not audit["state_table"]["deterministic"]
    ]
    full_period_count = int(chain_60["statistics"].get("full_lasso_period_replay", 0))
    status = (
        "mod16_automaton_collision_open_no_resolution"
        if collision_audits
        else "mod16_automaton_candidate_open_no_resolution"
    )
    audit = {
        "source_ticket": prior["ticket_id"],
        "theorem_name": "Mod16AutomatonCoverOrLiftCollision",
        "base_bits": SAMPLE_BITS,
        "base_mixed_cylinder_count": len(base["mixed_low40"]),
        "base_mixed_start_template_lift_count": len(base_rows),
        "direct_lift_statistics": {
            "52": lifted_52["statistics"],
            "56": lifted_56["statistics"],
        },
        "chain_lift_statistics": chain_60["statistics"],
        "chain_parent_bits": CHAIN_PARENT_BITS,
        "chain_target_bits": CHAIN_TARGET_BITS,
        "chain_parent_rows": len(lifted_56["rows"]),
        "chain_target_rows": len(chain_60["rows"]),
        "chain_parent_rows_with_start_template_lift": chain_60["parent_rows_with_start_template_chain_lift"],
        "chain_parent_extension_count_distribution": chain_60["parent_extension_count_distribution"],
        "row_audits": row_audits,
        "collision_audit_count": len(collision_audits),
        "full_period_escape_count": full_period_count,
        "discarded_route": (
            "Treat low40+base_mod16 determinism as a proof. TICKET63 keeps it as a finite automaton table and "
            "requires either symbolic closure or a higher-lift collision witness."
        ),
        "retained_route": (
            "Use the deterministic finite state table as a candidate automaton cover: first minimize quotient "
            "coordinates, then prove all future lifts preserve the transition relation or expose the first "
            "collision."
        ),
        "candidate_theorem": (
            "There exists a finite automaton over pre-replay states refining low40+base_mod16 whose transition "
            "relation covers every admissible higher lift and whose accepting classes exclude full-period "
            "nondecreasing Collatz cycles."
        ),
        "counterexample_target": (
            "Two admissible higher lifts sharing the same proposed automaton state but producing different "
            "failure/outcome/transition labels, or a full-period replay inside the automaton cover."
        ),
        "next_theorem_target": (
            "SymbolicMod16AutomatonTransitionProof"
            if not collision_audits
            else "FirstAutomatonCollisionRefinement"
        ),
        "proof_boundary": (
            "This is a finite automaton-table and targeted 60-bit chain-lift audit. It does not prove Collatz "
            "and does not certify a Collatz counterexample; it only sharpens the next symbolic automaton-cover "
            "or collision-refinement obligation."
        ),
    }
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-63",
        "route": "Mod16AutomatonCoverOrLiftCollision",
        "status": status,
        "proof_or_counterexample_mode": "finite automaton table plus targeted chain-lift audit",
        "attempt": (
            "Continue from TICKET62 by extracting the mod16 transition table, testing quotient reductions, and "
            "lifting the 56-bit survivor rows one more targeted step to 60 bits."
        ),
        "bounded_result": {"mod16_automaton_cover_audit": audit},
        "obstruction": (
            "No finite automaton table proves Collatz until all future lifts are symbolically covered. A collision "
            "would refute only the proposed automaton state, not Collatz itself, unless it yields a full-period orbit."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": (
            "Generate CO-TICKET-64 by proving the symbolic transition relation for the retained automaton states "
            "or by extending targeted lift search until the first quotient collision appears."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    automaton_gate: str,
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
        "proof_or_counterexample_mode": "automaton-cover transfer",
        "attempt": (
            "Transfer TICKET63's rule: a stable separator must become an explicit automaton table with transition "
            "closure and collision tests before it can support any theorem claim."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket63_transfer": route,
            "automaton_gate": automaton_gate,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "The next useful artifact is an explicit state table plus a proof of closure or a first collision. "
                "Heuristic separator stability is not enough."
            ),
        },
        "obstruction": (
            "This is a transfer discipline, not a solution. It raises the target from bounded separator survival "
            "to automaton closure."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Build the problem-specific automaton table and quotient/collision audit.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket62 = read_json(ROOT / "data/open-problem/ticket62-mod16-transition-cover-lab.json")
    attempts = [
        transfer_attempt(
            ticket62,
            "riemann",
            "RH-TICKET-63",
            "ZeroKernelAutomatonCoverOrHeightCollision",
            "zero-kernel separator states need an explicit height-transition automaton",
            (
                "A finite zero-kernel automaton covers every height lift with positivity-preserving transitions, "
                "or a height collision produces an off-critical obstruction packet."
            ),
            "two height lifts with the same zero-kernel automaton state but conflicting positivity labels",
        ),
        collatz_attempt(ticket62),
        transfer_attempt(
            ticket62,
            "goldbach",
            "GB-TICKET-63",
            "GoldbachMarginAutomatonCoverOrCutoffCollision",
            "margin separator states need an explicit cutoff-transition automaton",
            (
                "A finite Goldbach margin automaton covers every cutoff lift with positive-margin transitions, "
                "or a cutoff collision produces a stable exceptional packet."
            ),
            "two cutoff lifts with the same margin automaton state but conflicting positive-margin labels",
        ),
        transfer_attempt(
            ticket62,
            "twin-prime",
            "TP-TICKET-63",
            "TwinPrimeSieveAutomatonCoverOrParityCollision",
            "exact-gap separator states need an explicit sieve-level transition automaton",
            (
                "A finite twin-prime sieve automaton covers every sieve-level lift with retained gap-2 mass, "
                "or a parity collision produces a stable exact-gap mass leak."
            ),
            "two sieve-level lifts with the same parity automaton state but conflicting exact-gap labels",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "mod16_automaton_cover_open_no_resolution",
        "claim_boundary": (
            "Ticket 63 extracts a finite automaton table from TICKET62's mod16 transition evidence and transfers "
            "the automaton-cover discipline to RH, Goldbach, and Twin Prime. It does not prove or disprove any "
            "of the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket63-mod16-automaton-cover-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-63-automaton-cover.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-63-mod16-automaton-cover.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-63-margin-automaton.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-63-sieve-automaton.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
