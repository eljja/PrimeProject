from __future__ import annotations

from collections import defaultdict
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, v2, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket73_lineage_pressure_forest_lab import extend_reentry_layer, reconstruct_second_layer_roots
from ticket74_coverage_leakage_escape_forest_lab import expand_open_pressure_layer


GENERATED_AT = "2026-07-10T23:35:00+09:00"
SCHEMA = "primeproject.ticket76-symbolic-boundary-recurrence-lab.v1"
EXAMPLE_LIMIT = 8
PRECISION_BITS = (5, 9, 13, 17, 21)


def replay_word(residue: int, word: tuple[int, ...]) -> tuple[int, int]:
    current = residue
    mismatch_count = 0
    for valuation in word:
        actual = v2(3 * current + 1)
        if actual != valuation:
            mismatch_count += 1
        current = (3 * current + 1) >> valuation
    return current, mismatch_count


def boundary_state(certificate: dict[str, Any]) -> dict[str, Any]:
    if certificate.get("status") != "needs_split":
        raise ValueError("boundary_state requires a needs_split certificate")
    residue = int(certificate["residue"])
    bits = int(certificate["modulus_bits"])
    certificate_word = tuple(int(value) for value in certificate.get("prefix_word", []))
    stable_word: list[int] = []
    consumed_bits = 0
    boundary_touching_valuation: int | None = None
    for valuation in certificate_word:
        if consumed_bits + valuation >= bits:
            boundary_touching_valuation = valuation
            break
        stable_word.append(valuation)
        consumed_bits += valuation
    word = tuple(stable_word)
    prefix_length = len(word)
    next_valuation = (
        boundary_touching_valuation
        if boundary_touching_valuation is not None
        else int(certificate["next_valuation"])
    )
    current, replay_mismatches = replay_word(residue, word)
    boundary_slack = bits - consumed_bits
    numerator = 3 * current + 1
    divisor = 1 << boundary_slack
    if numerator % divisor:
        raise RuntimeError("boundary quotient is not integral")
    quotient = numerator // divisor
    return {
        "residue": residue,
        "bits": bits,
        "prefix_length": prefix_length,
        "consumed_bits": consumed_bits,
        "word": word,
        "certificate_prefix_length": int(certificate["prefix_length"]),
        "rolled_back_boundary_touching_step": boundary_touching_valuation is not None,
        "current": current,
        "boundary_slack": boundary_slack,
        "boundary_quotient": quotient,
        "next_valuation": next_valuation,
        "replay_mismatch_count": replay_mismatches,
        "valuation_identity_holds": v2(quotient) == next_valuation - boundary_slack,
    }


def compact_formula_example(
    source: dict[str, Any],
    child: dict[str, Any],
    *,
    child_top: int,
    boundary: dict[str, Any],
    normalized_valuation: int,
    event: str,
) -> dict[str, Any]:
    return {
        "source_residue": int(source["residue"]),
        "source_bits": int(source["modulus_bits"]),
        "child_residue": int(child["residue"]),
        "child_bits": int(child["modulus_bits"]),
        "child_top": child_top,
        "prefix_length": int(boundary["prefix_length"]),
        "boundary_slack": int(boundary["boundary_slack"]),
        "boundary_quotient": int(boundary["boundary_quotient"]),
        "normalized_valuation": normalized_valuation,
        "predicted_first_new_valuation": int(boundary["boundary_slack"]) + normalized_valuation,
        "event": event,
        "child_status": str(child.get("status")),
    }


def audit_source_family(
    sources: list[dict[str, Any]],
    *,
    depth: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    formula_failure_count = 0
    source_replay_mismatch_count = 0
    source_valuation_identity_failure_count = 0
    old_prefix_lift_mismatch_count = 0
    affine_current_identity_failure_count = 0
    first_new_valuation_failure_count = 0
    unresolved_child_count = 0
    resolved_boundary_child_count = 0
    examples: list[dict[str, Any]] = []
    identity_failure_examples: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []

    for source_index, source_entry in enumerate(sources):
        source = source_entry["row"]["child_certificate"]
        boundary = boundary_state(source)
        source_replay_mismatch_count += int(boundary["replay_mismatch_count"])
        if not boundary["valuation_identity_holds"]:
            source_valuation_identity_failure_count += 1
        bits = int(source["modulus_bits"])
        prefix_length = int(boundary["prefix_length"])
        boundary_slack = int(boundary["boundary_slack"])
        boundary_quotient = int(boundary["boundary_quotient"])
        unit = 3 ** (prefix_length + 1)
        expected_current_step = (3**prefix_length) * (1 << boundary_slack)

        for child_top in range(16):
            child_residue = int(source["residue"]) | (child_top << bits)
            child = cert(child_residue, bits + 4)
            child_boundary_current, old_prefix_mismatches = replay_word(
                child_residue,
                tuple(int(value) for value in boundary["word"]),
            )
            old_prefix_lift_mismatch_count += old_prefix_mismatches
            affine_identity_holds = (
                child_boundary_current - int(boundary["current"]) == child_top * expected_current_step
            )
            if not affine_identity_holds:
                affine_current_identity_failure_count += 1

            lifted_boundary = boundary_quotient + child_top * unit
            normalized_valuation = v2(lifted_boundary)
            predicted_first_new_valuation = boundary_slack + normalized_valuation
            if normalized_valuation > 4:
                event = "unresolved_same_prefix"
                unresolved_child_count += 1
                event_holds = (
                    child.get("status") == "needs_split"
                    and int(child.get("prefix_length", -1)) == prefix_length
                    and int(child.get("consumed_bits", -1)) == int(boundary["consumed_bits"])
                    and int(child.get("next_valuation", -1)) == predicted_first_new_valuation
                )
                next_boundary_quotient = lifted_boundary // 16
            else:
                event = f"resolved_normalized_v{normalized_valuation}"
                resolved_boundary_child_count += 1
                child_word = tuple(int(value) for value in child.get("prefix_word", []))
                event_holds = (
                    len(child_word) > prefix_length
                    and child_word[:prefix_length] == tuple(boundary["word"])
                    and child_word[prefix_length] == predicted_first_new_valuation
                )
                next_boundary_quotient = None
            if not event_holds:
                first_new_valuation_failure_count += 1
            row_formula_holds = old_prefix_mismatches == 0 and affine_identity_holds and event_holds
            if not row_formula_holds:
                formula_failure_count += 1
                if len(identity_failure_examples) < EXAMPLE_LIMIT:
                    identity_failure_examples.append(
                        {
                            "source_residue": int(source["residue"]),
                            "source_bits": bits,
                            "certificate_prefix_length": int(boundary["certificate_prefix_length"]),
                            "stable_prefix_length": prefix_length,
                            "stable_consumed_bits": int(boundary["consumed_bits"]),
                            "rolled_back_boundary_touching_step": bool(
                                boundary["rolled_back_boundary_touching_step"]
                            ),
                            "child_top": child_top,
                            "old_prefix_mismatch_count": old_prefix_mismatches,
                            "affine_identity_holds": affine_identity_holds,
                            "event_holds": event_holds,
                            "observed_boundary_current": child_boundary_current,
                            "predicted_boundary_current": int(boundary["current"])
                            + child_top * expected_current_step,
                        }
                    )
            if len(examples) < EXAMPLE_LIMIT:
                examples.append(
                    compact_formula_example(
                        source,
                        child,
                        child_top=child_top,
                        boundary=boundary,
                        normalized_valuation=normalized_valuation,
                        event=event,
                    )
                )
            rows.append(
                {
                    "depth": depth,
                    "source_index": source_index,
                    "root_id": int(source_entry["root_id"]),
                    "source_residue": int(source["residue"]),
                    "source_bits": bits,
                    "prefix_length": prefix_length,
                    "boundary_slack": boundary_slack,
                    "boundary_quotient": boundary_quotient,
                    "child_top": child_top,
                    "normalized_valuation": normalized_valuation,
                    "event": event,
                    "next_boundary_quotient": next_boundary_quotient,
                    "child_residue": child_residue,
                    "child_bits": bits + 4,
                    "child_status": str(child.get("status")),
                }
            )

    return {
        "depth": depth,
        "source_count": len(sources),
        "row_count": len(rows),
        "unresolved_same_prefix_child_count": unresolved_child_count,
        "resolved_boundary_child_count": resolved_boundary_child_count,
        "source_replay_mismatch_count": source_replay_mismatch_count,
        "source_valuation_identity_failure_count": source_valuation_identity_failure_count,
        "old_prefix_lift_mismatch_count": old_prefix_lift_mismatch_count,
        "affine_current_identity_failure_count": affine_current_identity_failure_count,
        "first_new_valuation_failure_count": first_new_valuation_failure_count,
        "formula_failure_count": formula_failure_count,
        "examples": examples,
        "identity_failure_examples": identity_failure_examples,
    }, rows


def precision_closure_audit(rows: list[dict[str, Any]], precision_bits: int) -> dict[str, Any]:
    fixed_profiles: dict[tuple[Any, ...], dict[int, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    lookahead_profiles: dict[tuple[Any, ...], set[int]] = defaultdict(set)
    unresolved_rows = [row for row in rows if row["event"] == "unresolved_same_prefix"]
    prefix_period = 1 << (precision_bits + 2)
    source_mask = (1 << precision_bits) - 1
    lookahead_mask = (1 << (precision_bits + 4)) - 1

    for row in unresolved_rows:
        prefix_class = int(row["prefix_length"]) % prefix_period
        source_quotient = int(row["boundary_quotient"])
        child_quotient = int(row["next_boundary_quotient"])
        child_top = int(row["child_top"])
        fixed_key = (prefix_class, source_quotient & source_mask, child_top)
        fixed_profiles[fixed_key][child_quotient & source_mask].append(row)
        lookahead_key = (prefix_class, source_quotient & lookahead_mask, child_top)
        lookahead_profiles[lookahead_key].add(child_quotient & source_mask)

    collision_keys = [key for key, targets in fixed_profiles.items() if len(targets) > 1]
    lookahead_collision_keys = [key for key, targets in lookahead_profiles.items() if len(targets) > 1]
    examples = []
    for key in collision_keys[:EXAMPLE_LIMIT]:
        targets = fixed_profiles[key]
        target_values = sorted(targets)
        left = targets[target_values[0]][0]
        right = targets[target_values[1]][0]
        examples.append(
            {
                "source_coordinate": {
                    "prefix_modulus": prefix_period,
                    "prefix_class": key[0],
                    "boundary_quotient_modulus": 1 << precision_bits,
                    "boundary_quotient_class": key[1],
                    "child_top": key[2],
                },
                "left_source": {
                    "residue": left["source_residue"],
                    "bits": left["source_bits"],
                    "boundary_quotient": left["boundary_quotient"],
                    "next_boundary_quotient": left["next_boundary_quotient"],
                    "next_class": int(left["next_boundary_quotient"]) & source_mask,
                },
                "right_source": {
                    "residue": right["source_residue"],
                    "bits": right["source_bits"],
                    "boundary_quotient": right["boundary_quotient"],
                    "next_boundary_quotient": right["next_boundary_quotient"],
                    "next_class": int(right["next_boundary_quotient"]) & source_mask,
                },
            }
        )

    return {
        "precision_bits": precision_bits,
        "unresolved_same_prefix_row_count": len(unresolved_rows),
        "fixed_precision_transition_key_count": len(fixed_profiles),
        "fixed_precision_collision_key_count": len(collision_keys),
        "lookahead_precision_bits": precision_bits + 4,
        "lookahead_transition_key_count": len(lookahead_profiles),
        "lookahead_collision_key_count": len(lookahead_collision_keys),
        "fixed_precision_successor_sufficient_on_observed_rows": not collision_keys,
        "four_extra_bits_successor_sufficient_on_observed_rows": not lookahead_collision_keys,
        "collision_examples": examples,
    }


def reconstruct_source_layers() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    roots, original_mixed_keys, objects = reconstruct_second_layer_roots()
    root_sources = [{"root_id": index, "row": row} for index, row in enumerate(roots)]
    _, third = extend_reentry_layer(root_sources, objects=objects, mixed_keys=original_mixed_keys, depth=3)
    _, fourth = extend_reentry_layer(third, objects=objects, mixed_keys=original_mixed_keys, depth=4)
    fifth_summary, fifth = expand_open_pressure_layer(
        fourth,
        objects=objects,
        original_mixed_keys=original_mixed_keys,
        depth=5,
        retain_open_pressure=True,
    )
    return fourth, fifth, {
        "root_count": len(roots),
        "fourth_source_count": len(fourth),
        "fifth_open_pressure_count": len(fifth),
        "fifth_summary": fifth_summary,
    }


def analyze_symbolic_boundary_recurrence() -> dict[str, Any]:
    fourth, fifth, reconstruction = reconstruct_source_layers()
    fifth_audit, fifth_rows = audit_source_family(fourth, depth=5)
    sixth_audit, sixth_rows = audit_source_family(fifth, depth=6)
    rows = [*fifth_rows, *sixth_rows]
    precision_audits = [precision_closure_audit(rows, precision) for precision in PRECISION_BITS]
    fixed_collision_precisions = [
        audit["precision_bits"] for audit in precision_audits if audit["fixed_precision_collision_key_count"] > 0
    ]
    lookahead_failures = [
        audit["precision_bits"] for audit in precision_audits if audit["lookahead_collision_key_count"] > 0
    ]
    total_formula_failures = int(fifth_audit["formula_failure_count"]) + int(sixth_audit["formula_failure_count"])
    status = (
        "symbolic_formula_verified_fixed_precision_closure_refuted_on_tested_precisions_no_global_resolution"
        if total_formula_failures == 0 and fixed_collision_precisions and not lookahead_failures
        else "symbolic_boundary_recurrence_audit_inconclusive_no_global_resolution"
    )
    return {
        "theorem_name": "FourBitBoundaryQuotientRecurrenceAndFixedPrecisionLoss",
        "source_ticket": "CO-TICKET-75",
        "source_status": "all_tested_finite_preoutcome_coordinates_leak_or_cycle_no_global_resolution",
        "symbolic_objects": {
            "accelerated_map": "T(n) = (3*n + 1) / 2^v2(3*n + 1) on odd n",
            "prefix_affine_identity": "T^m(r + h*2^b) = T^m(r) + h*3^m*2^(b-s)",
            "boundary_definitions": "d = b-s; A = (3*T^m(r)+1)/2^d; u = 3^(m+1)",
            "first_new_valuation_formula": "v_new = d + v2(A + h*u)",
            "unresolved_recurrence": "if v2(A+h*u) > 4, then A_next = (A+h*u)/16",
            "precision_loss": "A_next mod 2^q generally requires A mod 2^(q+4), so a fixed q-bit quotient projection is not algebraically successor-closed without extra restrictions.",
        },
        "reconstruction": reconstruction,
        "fifth_formula_audit": fifth_audit,
        "sixth_formula_audit": sixth_audit,
        "combined_formula_row_count": len(rows),
        "combined_formula_failure_count": total_formula_failures,
        "precision_closure_audits": precision_audits,
        "fixed_precision_collision_precisions": fixed_collision_precisions,
        "lookahead_failure_precisions": lookahead_failures,
        "symbolic_recurrence_status": status,
        "bounded_lemma": (
            "The four-bit first-boundary valuation formula holds on every audited fifth- and sixth-layer child. "
            "For each tested precision q, observed unresolved branches contain exact witnesses showing that q quotient bits "
            "do not determine the next q quotient bits, while q+4 lookahead bits do."
        ),
        "discarded_route": (
            "Repair TICKET75 by appending a fixed number q of low boundary-quotient bits. The exact unresolved recurrence divides "
            "by 16 and exposes four previously unseen bits; observed reachable witnesses collide at every tested q."
        ),
        "retained_route": (
            "Treat the full boundary quotient as a 2-adic transducer state and search for a separate well-founded arithmetic "
            "rank, or prove that reachable states satisfy an additional restriction that makes a finite quotient closed."
        ),
        "candidate_theorem": (
            "ReachableBoundaryRestrictionOrTwoAdicPressurePath: reachable Collatz boundary quotients obey a uniform arithmetic "
            "restriction yielding finite successor closure and strict descent, or their exact 2-adic recurrence admits an "
            "all-depth compatible pressure path requiring separate dynamical classification."
        ),
        "next_theorem_target": "ReachableBoundaryRestrictionOrTwoAdicPressurePath",
        "proof_boundary": (
            "TICKET76 proves an exact recurrence identity and bounded collision statements for the audited rows. It does not "
            "prove Collatz, construct a divergent integer orbit, or exclude every possible infinite-state rank."
        ),
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
        "proof_or_counterexample_mode": "symbolic recurrence proof discipline",
        "attempt": (
            "Transfer only the TICKET76 requirement that a state quotient must have an exact successor formula and account for "
            "information lost by normalization. No Collatz arithmetic or counts are transferred."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "ticket76_transfer": route,
            "candidate_theorem": candidate_theorem,
        },
        "obstruction": "No problem-specific symbolic recurrence computation was performed for this problem.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Derive a problem-specific exact successor or scale recurrence before proposing a finite quotient.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket75 = read_json(ROOT / "data/open-problem/ticket75-escape-coordinate-closure-lab.json")
    collatz_audit = analyze_symbolic_boundary_recurrence()
    attempts = [
        transfer_attempt(
            ticket75,
            "riemann",
            "RH-TICKET-76",
            "ExplicitFormulaInformationLossAudit",
            "An actual-zeta explicit-formula state has a uniform all-height successor bound with no hidden tail information loss.",
        ),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-76",
            "route": "SymbolicBoundaryRecurrenceOrFixedPrecisionCounteredge",
            "status": collatz_audit["symbolic_recurrence_status"],
            "proof_or_counterexample_mode": "exact symbolic identity plus reachable fixed-precision counteredges",
            "attempt": (
                "Derive the exact four-bit boundary recurrence, verify it on every fifth- and sixth-layer child, and test whether "
                "a fixed number of boundary-quotient bits is recursively sufficient."
            ),
            "bounded_result": {"source_ticket": "CO-TICKET-75", "symbolic_boundary_recurrence_audit": collatz_audit},
            "obstruction": (
                "An unresolved four-bit lift divides its boundary quotient by 16 after an affine odd correction, exposing four "
                "higher bits that no fixed low-bit projection carries."
            ),
            "candidate_theorem": collatz_audit["candidate_theorem"],
            "next_experiment": "Characterize restrictions on reachable boundary quotients or construct an exact all-depth 2-adic pressure path.",
            "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
        },
        transfer_attempt(
            ticket75,
            "goldbach",
            "GB-TICKET-76",
            "AnalyticScaleInformationLossAudit",
            "A finite analytic state propagates an explicit positive representation margin across every larger scale without hidden exceptional data.",
        ),
        transfer_attempt(
            ticket75,
            "twin-prime",
            "TP-TICKET-76",
            "SieveRefinementInformationLossAudit",
            "An exact-gap projection has a closed refinement recurrence retaining all parity-sensitive information needed for a positive lower bound.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "symbolic_boundary_recurrence_open_no_resolution",
        "claim_boundary": "Ticket 76 proves a bounded symbolic recurrence audit but does not solve any open problem.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket76-symbolic-boundary-recurrence-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-76-symbolic-boundary-recurrence.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-76-symbolic-boundary-recurrence.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-76-symbolic-boundary-recurrence.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-76-symbolic-boundary-recurrence.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
