from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .models import KeyRecord
from .number_theory import parse_int


def load_records(path: str | Path) -> list[KeyRecord]:
    source_path = Path(path)
    if source_path.suffix.lower() == ".json":
        return _load_json(source_path)
    if source_path.suffix.lower() == ".csv":
        return _load_csv(source_path)
    raise ValueError(f"Unsupported input format: {source_path.suffix}")


def _load_json(path: Path) -> list[KeyRecord]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload["records"] if isinstance(payload, dict) else payload
    return [_record_from_mapping(row) for row in rows]


def _load_csv(path: Path) -> list[KeyRecord]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [_record_from_mapping(row) for row in csv.DictReader(handle)]


def _record_from_mapping(row: dict[str, Any]) -> KeyRecord:
    value = row.get("value") or row.get("modulus") or row.get("prime")
    if value is None:
        raise ValueError("record requires one of value, modulus, or prime")
    public_exponent = row.get("public_exponent") or row.get("e")
    metadata = {
        key: value
        for key, value in row.items()
        if key
        not in {
            "key_id",
            "algorithm",
            "value",
            "modulus",
            "prime",
            "public_exponent",
            "e",
            "source",
            "created_at",
            "issuer_or_vendor",
        }
    }
    return KeyRecord(
        key_id=str(row.get("key_id") or row.get("id")),
        algorithm=str(row.get("algorithm") or "rsa").lower(),
        value=parse_int(value),
        public_exponent=parse_int(public_exponent) if public_exponent else None,
        source=row.get("source"),
        created_at=row.get("created_at"),
        issuer_or_vendor=row.get("issuer_or_vendor"),
        metadata=metadata,
    )


def write_report_json(report: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

