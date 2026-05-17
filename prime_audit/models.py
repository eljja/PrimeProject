from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class KeyRecord:
    key_id: str
    algorithm: str
    value: int
    public_exponent: int | None = None
    source: str | None = None
    created_at: str | None = None
    issuer_or_vendor: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def bit_length(self) -> int:
        return self.value.bit_length()


@dataclass(frozen=True)
class FeatureSet:
    bit_length: int
    low_bits_hex: str
    residue_fingerprint: dict[int, int]
    near_square_distance_bits: int | None = None
    recognized_parameter: str | None = None


@dataclass(frozen=True)
class Finding:
    key_id: str
    check: str
    severity: str
    message: str
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AuditReport:
    records: list[KeyRecord]
    features: dict[str, FeatureSet]
    findings: list[Finding]

