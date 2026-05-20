from __future__ import annotations

from math import gcd, log
from statistics import mean
from typing import Any

from .catalog import recognize_standard_prime
from .models import KeyRecord
from .number_theory import is_probable_prime


PRIME_RECORD_ALGORITHMS = {"dh", "ffdhe", "modp", "ecc", "ec", "field-prime", "prime"}
FINGERPRINT_MODULI = (30, 210, 2310)


def analyze_prime_generator_fingerprints(
    records: list[KeyRecord],
    *,
    gap_max_steps: int = 4096,
) -> dict[str, Any]:
    prime_rows: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    seen_values: dict[int, str] = {}

    for record in records:
        if record.algorithm not in PRIME_RECORD_ALGORITHMS:
            continue
        row = fingerprint_prime_record(record, gap_max_steps=gap_max_steps)
        prime_rows.append(row)
        if not row["is_probable_prime"]:
            findings.append(
                {
                    "key_id": record.key_id,
                    "check": "non_prime_generator_object",
                    "severity": "high",
                    "message": "Record is marked as a prime-like object but does not pass probable-prime testing.",
                }
            )
        if record.value in seen_values:
            findings.append(
                {
                    "key_id": record.key_id,
                    "check": "repeated_prime_value",
                    "severity": "high",
                    "message": "Same prime-like value appears more than once; review parameter provenance.",
                    "evidence": {"matching_key_id": seen_values[record.value]},
                }
            )
        else:
            seen_values[record.value] = record.key_id
        if row["recognized_parameter"]:
            findings.append(
                {
                    "key_id": record.key_id,
                    "check": "recognized_public_parameter",
                    "severity": "info",
                    "message": f"Value matches known public parameter {row['recognized_parameter']}.",
                }
            )

    aggregate = aggregate_prime_fingerprints(prime_rows)
    findings.extend(generator_signal_findings(aggregate))
    return {
        "schema": "primeproject.generator-fingerprint.v1",
        "record_count": len(prime_rows),
        "gap_max_steps": gap_max_steps,
        "aggregate": aggregate,
        "records": prime_rows,
        "findings": findings,
    }


def fingerprint_prime_record(record: KeyRecord, *, gap_max_steps: int) -> dict[str, Any]:
    value = record.value
    is_prime = is_probable_prime(value)
    gap_context = prime_gap_context(value, max_steps=gap_max_steps) if is_prime else None
    return {
        "key_id": record.key_id,
        "algorithm": record.algorithm,
        "bit_length": value.bit_length(),
        "low16": value & 0xFFFF,
        "low32_hex": hex(value & 0xFFFFFFFF),
        "recognized_parameter": recognize_standard_prime(value),
        "is_probable_prime": is_prime,
        "residues": {str(modulo): value % modulo for modulo in FINGERPRINT_MODULI},
        "gap_context": gap_context,
    }


def prime_gap_context(value: int, *, max_steps: int) -> dict[str, Any]:
    previous_prime = previous_probable_prime(value, max_steps=max_steps)
    next_prime = next_probable_prime_after(value, max_steps=max_steps)
    left_gap = value - previous_prime if previous_prime is not None else None
    right_gap = next_prime - value if next_prime is not None else None
    expected_gap = log(max(value, 3))
    return {
        "previous_prime": previous_prime,
        "next_prime": next_prime,
        "left_gap": left_gap,
        "right_gap": right_gap,
        "left_gap_over_logp": left_gap / expected_gap if left_gap is not None else None,
        "right_gap_over_logp": right_gap / expected_gap if right_gap is not None else None,
    }


def previous_probable_prime(value: int, *, max_steps: int) -> int | None:
    if value <= 2:
        return None
    candidate = value - 1 if value % 2 == 0 else value - 2
    checked = 0
    while candidate >= 2 and checked <= max_steps:
        if is_probable_prime(candidate):
            return candidate
        candidate -= 1 if candidate == 3 else 2
        checked += 1
    return None


def next_probable_prime_after(value: int, *, max_steps: int) -> int | None:
    candidate = value + 1 if value % 2 == 0 else value + 2
    checked = 0
    while checked <= max_steps:
        if is_probable_prime(candidate):
            return candidate
        candidate += 1 if candidate == 2 else 2
        checked += 1
    return None


def aggregate_prime_fingerprints(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "record_count": 0,
            "bit_lengths": {},
            "residue_total_variation": {},
            "low16_unique_ratio": 0.0,
            "gap_statistics": {},
            "generator_signals": {},
        }
    bit_lengths: dict[str, int] = {}
    for row in rows:
        key = str(row["bit_length"])
        bit_lengths[key] = bit_lengths.get(key, 0) + 1
    residue_tv = {
        str(modulo): residue_total_variation(rows, modulo)
        for modulo in FINGERPRINT_MODULI
    }
    low16_unique_ratio = len({row["low16"] for row in rows}) / len(rows)
    gap_rows = [row for row in rows if row["gap_context"] and row["gap_context"]["left_gap"] is not None]
    left_scaled = [row["gap_context"]["left_gap_over_logp"] for row in gap_rows]
    right_scaled = [
        row["gap_context"]["right_gap_over_logp"]
        for row in gap_rows
        if row["gap_context"]["right_gap_over_logp"] is not None
    ]
    gap_statistics = {
        "covered_records": len(gap_rows),
        "mean_left_gap_over_logp": mean(left_scaled) if left_scaled else None,
        "mean_right_gap_over_logp": mean(right_scaled) if right_scaled else None,
        "large_left_gap_records": sum(1 for value in left_scaled if value >= 2.0),
    }
    generator_signals = {
        "max_residue_tv": max(residue_tv.values()) if residue_tv else 0.0,
        "low16_collision_rate": 1 - low16_unique_ratio,
        "next_prime_exposure_score": gap_statistics["mean_left_gap_over_logp"],
    }
    return {
        "record_count": len(rows),
        "bit_lengths": bit_lengths,
        "residue_total_variation": residue_tv,
        "low16_unique_ratio": low16_unique_ratio,
        "gap_statistics": gap_statistics,
        "generator_signals": generator_signals,
    }


def residue_total_variation(rows: list[dict[str, Any]], modulo: int) -> float:
    residues = [residue for residue in range(modulo) if gcd(residue, modulo) == 1]
    if not residues:
        return 0.0
    counts = {residue: 0 for residue in residues}
    observed = 0
    for row in rows:
        residue = row["residues"][str(modulo)]
        if residue in counts:
            counts[residue] += 1
            observed += 1
    if observed == 0:
        return 0.0
    uniform = 1 / len(residues)
    return 0.5 * sum(abs((counts[residue] / observed) - uniform) for residue in residues)


def generator_signal_findings(aggregate: dict[str, Any]) -> list[dict[str, Any]]:
    signals = aggregate.get("generator_signals", {})
    record_count = aggregate.get("record_count") or 0
    gap_count = aggregate.get("gap_statistics", {}).get("covered_records") or 0
    findings: list[dict[str, Any]] = []
    max_residue_tv = signals.get("max_residue_tv") or 0.0
    if record_count >= 8 and max_residue_tv >= 0.35:
        findings.append(
            {
                "check": "residue_drift_generator_signal",
                "severity": "medium",
                "message": "Residue distribution is far from uniform; review generator, sieve, or fixed-parameter provenance.",
                "evidence": {"max_residue_tv": max_residue_tv},
            }
        )
    exposure = signals.get("next_prime_exposure_score")
    if gap_count >= 5 and exposure is not None and exposure >= 1.6:
        findings.append(
            {
                "check": "next_prime_exposure_signal",
                "severity": "low",
                "message": "Mean left gap is high relative to log(p), which is consistent with next-prime exposure bias.",
                "evidence": {"next_prime_exposure_score": exposure},
            }
        )
    collision_rate = signals.get("low16_collision_rate") or 0.0
    if record_count >= 8 and collision_rate >= 0.25:
        findings.append(
            {
                "check": "low_bits_collision_signal",
                "severity": "low",
                "message": "Low-bit collisions are elevated for this sample; review deterministic templates or small sample effects.",
                "evidence": {"low16_collision_rate": collision_rate},
            }
        )
    return findings
