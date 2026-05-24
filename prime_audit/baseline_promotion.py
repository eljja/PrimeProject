from __future__ import annotations

from typing import Any


BASELINE_PROMOTION_SCHEMA = "primeproject.baseline-promotion-plan.v1"

RSA_LIBRARY_ORDER = {
    "OpenSSL": 0,
    "BoringSSL": 1,
    "Go crypto/rsa": 2,
}


def build_baseline_promotion_plan(
    *,
    acceptance: dict[str, Any],
    power: dict[str, Any],
) -> dict[str, Any]:
    power_rows = {
        power_key(row.get("library"), row.get("object_type"), row.get("bit_length")): row
        for row in power.get("rows", [])
    }
    rows = [promotion_row(row, power_rows) for row in acceptance.get("rows", [])]
    p0_rows = [row for row in rows if row["priority"] == "P0" and row["promotion_state"] != "ready"]
    unlock = minimal_unlock_targets(rows)
    return {
        "schema": BASELINE_PROMOTION_SCHEMA,
        "row_count": len(rows),
        "summary": {
            "ready_count": sum(1 for row in rows if row["promotion_state"] == "ready"),
            "p0_target_count": len(p0_rows),
            "minimal_unlock_target_count": len(unlock),
            "projected_samples_for_minimal_unlock": sum(row["target_samples_for_10pct_tv"] or 0 for row in unlock),
            "dominant_next_step": dominant_next_step(rows),
        },
        "minimal_unlock_targets": unlock,
        "rows": rows,
        "claim_gate": {
            "status": "open" if acceptance.get("claim_gate", {}).get("status") == "open" else "blocked",
            "message": "Promotion plan identifies the shortest public-safe path from blocked baselines to accepted real-world evidence.",
        },
    }


def promotion_row(row: dict[str, Any], power_rows: dict[tuple[Any, Any, Any], dict[str, Any]]) -> dict[str, Any]:
    power = power_rows.get(power_key(row.get("library"), row.get("object_type"), row.get("bit_length")), {})
    target_samples = power.get("min_samples_for_10pct_tv")
    current_samples = int(row.get("sample_count") or 0)
    planned_target = int(row.get("sample_target") or 0)
    blockers = list(row.get("blocking_reasons") or [])
    state = promotion_state(row, power)
    return {
        "baseline_id": row.get("baseline_id"),
        "library": row.get("library"),
        "object_type": row.get("object_type"),
        "bit_length": row.get("bit_length"),
        "priority": priority(row),
        "current_acceptance": row.get("acceptance"),
        "promotion_state": state,
        "next_step": next_step(blockers, row, power),
        "current_samples": current_samples,
        "planned_sample_target": planned_target,
        "target_samples_for_10pct_tv": target_samples,
        "remaining_samples_to_10pct_tv": max(0, int(target_samples or 0) - current_samples),
        "power_tier": row.get("power_tier"),
        "blocking_reasons": blockers,
    }


def promotion_state(row: dict[str, Any], power: dict[str, Any]) -> str:
    if row.get("acceptance") == "accepted":
        return "ready"
    if row.get("blocking_reasons"):
        return "collect_and_document"
    if row.get("acceptance") == "screening_only" or power.get("power_tier") == "coarse":
        return "increase_power"
    return "review"


def next_step(blockers: list[str], row: dict[str, Any], power: dict[str, Any]) -> str:
    if "forbidden_public_fields" in blockers:
        return "remove_forbidden_public_fields"
    if "manifest_not_available" in blockers or "target_not_available" in blockers:
        return "collect_aggregate_baseline"
    if "provenance_not_passed" in blockers:
        return "complete_provenance_record"
    if row.get("acceptance") == "screening_only" or power.get("power_tier") == "coarse":
        return "raise_sample_count_to_power_floor"
    return "ready_for_claim_gate"


def minimal_unlock_targets(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rsa_rows = [
        row
        for row in rows
        if row.get("object_type") == "rsa-prime" and row.get("library") in RSA_LIBRARY_ORDER
    ]
    rsa_rows.sort(key=lambda row: (RSA_LIBRARY_ORDER[row["library"]], int(row.get("bit_length") or 0)))
    selected = []
    seen_libraries: set[str] = set()
    for row in rsa_rows:
        library = row["library"]
        if library in seen_libraries:
            continue
        selected.append(row)
        seen_libraries.add(library)
        if len(selected) == 2:
            break
    return selected


def dominant_next_step(rows: list[dict[str, Any]]) -> str | None:
    counts: dict[str, int] = {}
    for row in rows:
        step = row.get("next_step")
        if step and step != "ready_for_claim_gate":
            counts[step] = counts.get(step, 0) + 1
    if not counts:
        return None
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def priority(row: dict[str, Any]) -> str:
    if row.get("object_type") == "rsa-prime" and row.get("library") in RSA_LIBRARY_ORDER:
        return "P0"
    return "P1"


def power_key(library: Any, object_type: Any, bit_length: Any) -> tuple[Any, Any, Any]:
    return (library, object_type, bit_length)
