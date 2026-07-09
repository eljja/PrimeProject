from __future__ import annotations

import json
from collections import Counter, defaultdict
from typing import Any, Callable

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


GENERATED_AT = "2026-07-09T12:10:00+09:00"
SCHEMA = "primeproject.ticket57-parametric-template-automaton-lab.v1"
LOW_BIT_LEVELS = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]


def key_for(certificate: dict[str, Any]) -> tuple[Any, ...] | None:
    return template_key(certificate, FAMILY) if certificate.get("status") == "needs_split" else None


def template_text(certificate: dict[str, Any]) -> str:
    key = key_for(certificate)
    return stringify_key(key) if key else str(certificate.get("status"))


def exact32_start_rows(example_limit: int = 8) -> list[dict[str, Any]]:
    target = (0, START_TAIL, START_RESIDUE_MOD_256, START_NEXT_VALUATION)
    rows: list[dict[str, Any]] = []

    for word in stream_open_words_with_tail(32):
        residue = residue_for_word(word)
        certificate = cert(residue, 32)
        if certificate.get("status") != "needs_split" or template_key(certificate, FAMILY) != target:
            continue

        depth = prefix_depth(residue, 32)
        matched = int(depth["matched_prefix_templates"])
        if matched == 15:
            coarse_outcome = "phase5_gate_terminal_tunnel"
            fine_outcome = coarse_outcome
            observed_next = "terminal_tunnel"
        else:
            observed_next = str(depth.get("observed_next_valuation"))
            coarse_outcome = f"fail_offset_{depth['failure_offset']}"
            fine_outcome = f"{coarse_outcome}_next_{observed_next}"

        rows.append(
            {
                "residue": residue,
                "bits": 32,
                "prefix_length": int(certificate.get("prefix_length", 0)),
                "consumed_bits": int(certificate.get("consumed_bits", 0)),
                "consumed_gap": 32 - int(certificate.get("consumed_bits", 0)),
                "tail4": list(certificate.get("prefix_word", [])[-4:]),
                "target_template": stringify_key(target),
                "coarse_outcome": coarse_outcome,
                "fine_outcome": fine_outcome,
                "matched_prefix_templates": matched,
                "failure_offset": depth.get("failure_offset"),
                "failure_reason": depth.get("reason"),
                "observed_next_valuation": observed_next,
                "prefix_word_tail": list(word[-12:]) if len(rows) < example_limit else [],
            }
        )
    return rows


def outcome_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    coarse = Counter(str(row["coarse_outcome"]) for row in rows)
    fine = Counter(str(row["fine_outcome"]) for row in rows)
    prefix_lengths = Counter(str(row["prefix_length"]) for row in rows)
    return {
        "total": len(rows),
        "coarse_outcome_counts": dict(sorted(coarse.items())),
        "top_fine_outcome_counts": [
            {"outcome": outcome, "count": count} for outcome, count in fine.most_common(12)
        ],
        "prefix_length_range": {
            "min": min((int(row["prefix_length"]) for row in rows), default=0),
            "max": max((int(row["prefix_length"]) for row in rows), default=0),
        },
        "top_prefix_lengths": [
            {"prefix_length": int(length), "count": count}
            for length, count in sorted(prefix_lengths.items(), key=lambda item: (-item[1], int(item[0])))[:10]
        ],
    }


def assess_abstraction(
    rows: list[dict[str, Any]],
    label: str,
    key_fn: Callable[[dict[str, Any]], tuple[Any, ...]],
    *,
    example_limit: int = 4,
) -> dict[str, Any]:
    groups: dict[tuple[Any, ...], Counter[str]] = defaultdict(Counter)
    examples: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = key_fn(row)
        outcome = str(row["coarse_outcome"])
        groups[key][outcome] += 1
        if len(examples[key]) < 4:
            examples[key].append(
                {
                    "residue": row["residue"],
                    "prefix_length": row["prefix_length"],
                    "coarse_outcome": row["coarse_outcome"],
                    "fine_outcome": row["fine_outcome"],
                    "failure_offset": row["failure_offset"],
                    "observed_next_valuation": row["observed_next_valuation"],
                }
            )

    collision_keys = [key for key, outcomes in groups.items() if len(outcomes) > 1]
    ambiguous_candidate_count = sum(sum(groups[key].values()) for key in collision_keys)
    largest_group = max((sum(outcomes.values()) for outcomes in groups.values()), default=0)
    max_outcomes = max((len(outcomes) for outcomes in groups.values()), default=0)
    collision_examples = []
    for key in collision_keys[:example_limit]:
        collision_examples.append(
            {
                "state_key": json.dumps(key, ensure_ascii=False, separators=(",", ":")),
                "outcome_counts": dict(sorted(groups[key].items())),
                "examples": examples[key],
            }
        )

    return {
        "abstraction": label,
        "state_count": len(groups),
        "collision_group_count": len(collision_keys),
        "ambiguous_candidate_count": ambiguous_candidate_count,
        "largest_group_size": largest_group,
        "max_outcomes_per_state": max_outcomes,
        "deterministic_for_exact32_coarse_outcome": len(collision_keys) == 0,
        "collision_examples": collision_examples,
    }


def exact32_determinism_ladder(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ladder = [
        assess_abstraction(rows, "template_only", lambda row: ("target",)),
        assess_abstraction(
            rows,
            "template_plus_prefix_length",
            lambda row: ("target", int(row["prefix_length"])),
        ),
    ]
    for low_bits in LOW_BIT_LEVELS:
        mask = (1 << low_bits) - 1
        ladder.append(
            assess_abstraction(
                rows,
                f"template_plus_prefix_length_residue_mod_2^{low_bits}",
                lambda row, mask=mask, low_bits=low_bits: (
                    "target",
                    int(row["prefix_length"]),
                    low_bits,
                    int(row["residue"]) & mask,
                ),
            )
        )

    deterministic = [
        item for item in ladder if item.get("deterministic_for_exact32_coarse_outcome")
    ]
    return {
        "ladder": ladder,
        "first_deterministic_abstraction": deterministic[0]["abstraction"] if deterministic else None,
        "first_deterministic_low_bits": next(
            (
                int(item["abstraction"].split("^")[-1])
                for item in ladder
                if item["abstraction"].startswith("template_plus_prefix_length_residue_mod_2^")
                and item.get("deterministic_for_exact32_coarse_outcome")
            ),
            None,
        ),
        "interpretation": (
            "The exact 32-bit population is not deterministic under the extracted template alone. "
            "A proof route needs additional boundary coordinates, and those coordinates must then be proved "
            "stable under higher-bit lifts instead of fitted only to the 32-bit partition."
        ),
    }


def replay_lasso_root(residue: int, base_bits: int, source: str) -> dict[str, Any]:
    matched = 0
    rows = []
    for offset, expected in enumerate(LASSO_PREFIX):
        bits = base_bits + offset
        certificate = cert(residue, bits)
        observed = key_for(certificate)
        match = observed == expected
        row = {
            "offset": offset,
            "bits": bits,
            "expected": stringify_key(expected),
            "observed": stringify_key(observed) if observed else str(certificate.get("status")),
            "matches": match,
            "reason": "match" if match else mismatch_reason(certificate, expected),
            "certificate": compact_certificate(certificate),
        }
        rows.append(row)
        if not match:
            break
        matched += 1
    return {
        "source": source,
        "base_bits": base_bits,
        "residue": residue,
        "matched_prefix_templates": matched,
        "full_lasso_period_replayed": matched == len(LASSO_PREFIX),
        "first_nonmatch": None if matched == len(LASSO_PREFIX) else rows[-1],
        "prefix_sample": rows[:6],
    }


def known_root_replay_audit(ticket55: dict[str, Any], ticket56: dict[str, Any]) -> dict[str, Any]:
    collatz55 = next(attempt for attempt in ticket55["attempts"] if attempt["problem_id"] == "collatz")
    audit55 = collatz55["bounded_result"]["phase5_gate_tunnel_audit"]
    roots: dict[tuple[int, int], str] = {}
    for row in audit55.get("machine_checked_roots", []):
        roots[(int(row["base_bits"]), int(row["residue"]))] = str(row.get("source_ticket", "ticket55"))

    collatz56 = next(attempt for attempt in ticket56["attempts"] if attempt["problem_id"] == "collatz")
    projection = (
        collatz56.get("bounded_result", {})
        .get("pre_gate_projection_escape_audit", {})
        .get("projection_escape_audit", {})
    )
    for witness in projection.get("escape_witnesses", []):
        roots[(int(witness["bits"]), int(witness["residue"]))] = "ticket56_projection_escape_witness"

    replays = [
        replay_lasso_root(residue, bits, source)
        for (bits, residue), source in sorted(roots.items())
    ]
    return {
        "known_root_count": len(replays),
        "target_period_template_count": len(LASSO_PREFIX),
        "max_replayed_prefix_depth": max((int(row["matched_prefix_templates"]) for row in replays), default=0),
        "full_lasso_period_replay_count": sum(1 for row in replays if row["full_lasso_period_replayed"]),
        "replay_rows": replays,
        "cycle_status": (
            "no_known_root_replays_full_lasso_period"
            if not any(row["full_lasso_period_replayed"] for row in replays)
            else "full_lasso_replay_witness_found"
        ),
        "interpretation": (
            "The known near-lasso roots remain terminal or pre-terminal obstructions. None is a replayable "
            "Collatz counterexample cycle; a real disproof route would need a compatible infinite lift, not just "
            "a finite template prefix."
        ),
    }


def projection_escape_carry_forward(ticket56: dict[str, Any]) -> dict[str, Any]:
    collatz56 = next(attempt for attempt in ticket56["attempts"] if attempt["problem_id"] == "collatz")
    audit = collatz56["bounded_result"]["pre_gate_projection_escape_audit"]
    projection = audit["projection_escape_audit"]
    exact32 = audit["exact32_pre_gate_partition"]
    target32 = exact32["target_template"]
    escape_rows = []
    for witness in projection.get("escape_witnesses", []):
        projected = witness.get("projection32", {})
        escape_rows.append(
            {
                "residue": witness.get("residue"),
                "bits": witness.get("bits"),
                "lasso_prefix_depth": witness.get("lasso_prefix_depth"),
                "projection_template": projected.get("template"),
                "projection_matches_exact32_target": projected.get("template") == target32,
                "escape_class": "tail_or_pending_valuation_projection_escape",
            }
        )
    return {
        "exact32_target_template": target32,
        "simple_projection_closure_status": projection.get("simple_projection_closure_status"),
        "sample_count": projection.get("sample_count"),
        "sample_start_template_matches": projection.get("sample_start_template_matches"),
        "escape_witness_count": len(escape_rows),
        "escape_witnesses": escape_rows,
        "required_upgrade": (
            "Replace fixed exact32 projection closure with a boundary-state relation that records how tail word "
            "and pending valuation transform under projection and lift."
        ),
    }


def collatz_attempt(ticket55: dict[str, Any], ticket56: dict[str, Any]) -> dict[str, Any]:
    rows = exact32_start_rows()
    determinism = exact32_determinism_ladder(rows)
    projection = projection_escape_carry_forward(ticket56)
    replay = known_root_replay_audit(ticket55, ticket56)
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-57",
        "route": "ParametricTemplateAutomatonOrEscapeCycle",
        "status": "parametric_state_obstruction_open_no_resolution",
        "proof_or_counterexample_mode": "state-abstraction falsification plus replayable-cycle search",
        "attempt": (
            "Keep the TICKET56 local theorem, but attack its globalization route. Measure how much boundary "
            "state is needed even to make the exact 32-bit partition deterministic, carry forward the 48-bit "
            "projection escape, and test whether known near-lasso roots replay a full template period."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-56",
            "parametric_template_automaton_audit": {
                "family": FAMILY,
                "theorem_name": "AffineBoundaryTemplateStateOrEscapeCycle",
                "exact32_outcome_summary": outcome_summary(rows),
                "exact32_state_determinism": determinism,
                "projection_escape_carry_forward": projection,
                "known_root_replay_audit": replay,
                "discarded_routes": [
                    "template-only rank or transition relation",
                    "exact32 finite partition promoted by simple projection closure",
                    "near-lasso prefix treated as a counterexample without full-period replay and lift compatibility",
                ],
                "retained_route": (
                    "A parametric affine-boundary automaton over phase, tail word, residue modulo 2^k, prefix "
                    "length, consumed-bit gap, and pending valuation; or a replayable escape cycle that survives "
                    "one full lasso period and avoids known terminal tunnels."
                ),
                "candidate_theorem": (
                    "For every phase-compatible start cylinder, a boundary-state transition either reaches a "
                    "finite next-valuation failure gate, enters the Phase5GateToTerminalTunnel, or strictly "
                    "decreases a well-founded rank defined on the full affine boundary state."
                ),
                "counterexample_target": (
                    "Find a higher-bit root whose full affine boundary state returns after one lasso period with "
                    "nondecreasing rank and whose trajectory is not covered by TICKET53, TICKET55, or TICKET56."
                ),
                "proof_boundary": (
                    "No Collatz proof and no certified Collatz counterexample. TICKET57 rejects weaker finite "
                    "state abstractions and finds no replayable cycle among known near-lasso roots; the remaining "
                    "obligation is a parametric affine-boundary lift theorem or a new full-period escape witness."
                ),
            },
        },
        "obstruction": (
            "The exact 32-bit partition needs hidden boundary coordinates to become deterministic, and the known "
            "48-bit depth-15 witness projects outside the exact32 target template. The known near-lasso roots do "
            "not replay a full lasso period."
        ),
        "candidate_theorem": (
            "AffineBoundaryTemplateStateOrEscapeCycle: prove deterministic, lift-closed transitions for the full "
            "boundary state with a decreasing rank, or produce a full-period escape cycle."
        ),
        "next_experiment": (
            "Generate CO-TICKET-58 by synthesizing the affine-boundary transition relation and checking whether "
            "the first deterministic exact32 boundary level is stable under 40/48-bit lifts."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    state_variables: list[str],
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
        "proof_or_counterexample_mode": "parametric-boundary-state transfer",
        "attempt": (
            "Transfer TICKET57's rule: a finite partition is not a proof until the boundary coordinates that make "
            "it deterministic are specified and proved stable under the natural lift. A counterexample candidate "
            "must replay under those same coordinates, not only under a quotient visualization."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket57_transfer": route,
            "required_state_variables": state_variables,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "Promote neither a finite closure nor a stress witness unless it survives the parametric boundary "
                "state gate: lift-closure, deterministic transition, and replayable obstruction must be checked in "
                "the same coordinate system."
            ),
        },
        "obstruction": (
            "This transfer is methodological and does not solve the target problem. It prevents quotient-level "
            "evidence from being mistaken for a theorem over the unbounded object."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Build the problem-specific boundary-state transition relation or find a replayable escape object.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket55 = read_json(ROOT / "data/open-problem/ticket55-phase5-valuation-gate-lab.json")
    ticket56 = read_json(ROOT / "data/open-problem/ticket56-pre-gate-projection-escape-lab.json")
    attempts = [
        transfer_attempt(
            ticket56,
            "riemann",
            "RH-TICKET-57",
            "ZeroKernelBoundaryStateOrOffCriticalEscapeCycle",
            [
                "zero height window",
                "explicit-formula kernel boundary",
                "positivity deficit",
                "lift/projection height map",
            ],
            (
                "Every off-critical zero-kernel packet has a lift-closed boundary state whose positivity measure "
                "strictly improves, or it yields a replayable off-critical escape cycle."
            ),
            "a height-lift-stable off-critical zero packet with non-improving positivity deficit",
        ),
        collatz_attempt(ticket55, ticket56),
        transfer_attempt(
            ticket56,
            "goldbach",
            "GB-TICKET-57",
            "ExceptionalMarginBoundaryStateOrCounterexample",
            [
                "even cutoff scale",
                "major/minor arc margin",
                "exceptional residue class",
                "singular-series lower-bound slack",
            ],
            (
                "Every exceptional-residue packet has a lift-closed positive-margin boundary state, or it yields "
                "an explicit even counterexample packet that survives cutoff lifting."
            ),
            "a cutoff-stable even packet whose certified Goldbach margin remains nonpositive",
        ),
        transfer_attempt(
            ticket56,
            "twin-prime",
            "TP-TICKET-57",
            "ParityBoundarySieveStateOrGapCycle",
            [
                "sieve level",
                "admissible residue selector",
                "parity leakage mass",
                "gap-2 retained mass versus wider-gap leakage",
            ],
            (
                "Every exact gap-2 selector has a lift-closed parity-boundary state with retained positive mass, "
                "or it yields a replayable leakage cycle that absorbs all gap-2 mass."
            ),
            "a sieve-lift-stable leakage cycle that keeps gap-2 mass nonpositive at every scale",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "parametric_boundary_state_open_no_resolution",
        "claim_boundary": (
            "Ticket 57 hardens the proof/disproof program by rejecting finite quotient shortcuts and requiring "
            "boundary-state lift closure or replayable escape cycles. It does not prove or disprove RH, Collatz, "
            "Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket57-parametric-template-automaton-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-57-boundary-state-model.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-57-parametric-template-automaton.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-57-boundary-margin-model.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-57-boundary-sieve-model.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
