from __future__ import annotations

import base64
import csv
import json
import re
from pathlib import Path
from typing import Any

from .models import KeyRecord
from .number_theory import parse_int

RSA_ENCRYPTION_OID = "1.2.840.113549.1.1.1"
ASN1_SEQUENCE = 0x30
ASN1_INTEGER = 0x02
ASN1_BIT_STRING = 0x03
ASN1_OBJECT_IDENTIFIER = 0x06
ASN1_CONTEXT_0 = 0xA0


def load_records(path: str | Path) -> list[KeyRecord]:
    source_path = Path(path)
    if source_path.suffix.lower() == ".json":
        return _load_json(source_path)
    if source_path.suffix.lower() == ".csv":
        return _load_csv(source_path)
    if source_path.suffix.lower() in {".pem", ".crt", ".cer", ".csr", ".der"}:
        return _load_key_material(source_path)
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


def _load_key_material(path: Path) -> list[KeyRecord]:
    data = path.read_bytes()
    text = data.decode("ascii", errors="ignore")
    pem_blocks = list(_iter_pem_blocks(text))
    records: list[KeyRecord] = []
    if pem_blocks:
        for index, (label, der) in enumerate(pem_blocks, start=1):
            records.append(_record_from_der(path, der, index=index, pem_label=label))
        return records
    return [_record_from_der(path, data, index=1, pem_label=None)]


def _iter_pem_blocks(text: str) -> list[tuple[str, bytes]]:
    pattern = re.compile(
        r"-----BEGIN ([^-]+)-----(.*?)-----END \1-----",
        flags=re.DOTALL,
    )
    blocks: list[tuple[str, bytes]] = []
    for match in pattern.finditer(text):
        label = match.group(1).strip()
        body = re.sub(r"\s+", "", match.group(2))
        blocks.append((label, base64.b64decode(body, validate=True)))
    return blocks


def _record_from_der(path: Path, der: bytes, *, index: int, pem_label: str | None) -> KeyRecord:
    attempts = (
        ("rsa-public-key", _parse_pkcs1_rsa_public_key),
        ("subject-public-key-info", _parse_subject_public_key_info),
        ("certificate-request", _parse_certification_request),
        ("certificate", _parse_certificate),
    )
    errors: list[str] = []
    for input_type, parser in attempts:
        try:
            modulus, public_exponent = parser(der)
            suffix = "" if index == 1 else f"-{index}"
            return KeyRecord(
                key_id=f"{path.stem}{suffix}",
                algorithm="rsa",
                value=modulus,
                public_exponent=public_exponent,
                source=str(path),
                metadata={
                    "input_type": input_type,
                    "pem_label": pem_label,
                },
            )
        except ValueError as exc:
            errors.append(f"{input_type}: {exc}")
    raise ValueError(f"Unsupported RSA key material in {path}: {'; '.join(errors)}")


def _parse_certificate(der: bytes) -> tuple[int, int]:
    certificate = _expect_single(der, ASN1_SEQUENCE)
    tbs_certificate, offset = _read_tlv(certificate, 0, ASN1_SEQUENCE)
    _expect_end(certificate, offset, allow_trailing=True)

    offset = 0
    if offset < len(tbs_certificate) and tbs_certificate[offset] == ASN1_CONTEXT_0:
        _, offset = _read_tlv(tbs_certificate, offset, ASN1_CONTEXT_0)
    for _ in range(5):
        _, offset = _read_any(tbs_certificate, offset)
    subject_public_key_info, offset = _read_tlv(tbs_certificate, offset, ASN1_SEQUENCE)
    return _parse_subject_public_key_info(_wrap_tlv(ASN1_SEQUENCE, subject_public_key_info))


def _parse_certification_request(der: bytes) -> tuple[int, int]:
    request = _expect_single(der, ASN1_SEQUENCE)
    request_info, offset = _read_tlv(request, 0, ASN1_SEQUENCE)
    _expect_end(request, offset, allow_trailing=True)

    offset = 0
    _, offset = _read_tlv(request_info, offset, ASN1_INTEGER)
    _, offset = _read_any(request_info, offset)
    subject_public_key_info, offset = _read_tlv(request_info, offset, ASN1_SEQUENCE)
    return _parse_subject_public_key_info(_wrap_tlv(ASN1_SEQUENCE, subject_public_key_info))


def _parse_subject_public_key_info(der: bytes) -> tuple[int, int]:
    spki = _expect_single(der, ASN1_SEQUENCE)
    algorithm_identifier, offset = _read_tlv(spki, 0, ASN1_SEQUENCE)
    oid_value, _ = _read_tlv(algorithm_identifier, 0, ASN1_OBJECT_IDENTIFIER)
    oid = _decode_oid(oid_value)
    if oid != RSA_ENCRYPTION_OID:
        raise ValueError(f"unsupported public key algorithm OID {oid}")
    public_key_bits, offset = _read_tlv(spki, offset, ASN1_BIT_STRING)
    _expect_end(spki, offset)
    if not public_key_bits or public_key_bits[0] != 0:
        raise ValueError("unsupported BIT STRING padding")
    return _parse_pkcs1_rsa_public_key(public_key_bits[1:])


def _parse_pkcs1_rsa_public_key(der: bytes) -> tuple[int, int]:
    sequence = _expect_single(der, ASN1_SEQUENCE)
    modulus_bytes, offset = _read_tlv(sequence, 0, ASN1_INTEGER)
    exponent_bytes, offset = _read_tlv(sequence, offset, ASN1_INTEGER)
    _expect_end(sequence, offset)
    modulus = _decode_integer(modulus_bytes)
    public_exponent = _decode_integer(exponent_bytes)
    if modulus <= 0 or public_exponent <= 0:
        raise ValueError("RSA modulus and exponent must be positive")
    return modulus, public_exponent


def _expect_single(data: bytes, tag: int) -> bytes:
    value, offset = _read_tlv(data, 0, tag)
    _expect_end(data, offset)
    return value


def _read_any(data: bytes, offset: int) -> tuple[bytes, int]:
    if offset >= len(data):
        raise ValueError("unexpected end of DER")
    return _read_tlv(data, offset, data[offset])


def _read_tlv(data: bytes, offset: int, expected_tag: int) -> tuple[bytes, int]:
    if offset >= len(data):
        raise ValueError("unexpected end of DER")
    tag = data[offset]
    if tag != expected_tag:
        raise ValueError(f"expected tag 0x{expected_tag:02x}, found 0x{tag:02x}")
    offset += 1
    if offset >= len(data):
        raise ValueError("missing DER length")
    length_byte = data[offset]
    offset += 1
    if length_byte & 0x80:
        length_size = length_byte & 0x7F
        if length_size == 0:
            raise ValueError("indefinite DER lengths are not supported")
        if offset + length_size > len(data):
            raise ValueError("truncated DER length")
        length = int.from_bytes(data[offset : offset + length_size], "big")
        offset += length_size
    else:
        length = length_byte
    end = offset + length
    if end > len(data):
        raise ValueError("truncated DER value")
    return data[offset:end], end


def _expect_end(data: bytes, offset: int, *, allow_trailing: bool = False) -> None:
    if allow_trailing:
        if offset > len(data):
            raise ValueError("DER offset moved beyond input")
        return
    if offset != len(data):
        raise ValueError("trailing DER data")


def _wrap_tlv(tag: int, value: bytes) -> bytes:
    return bytes([tag]) + _encode_length(len(value)) + value


def _encode_length(length: int) -> bytes:
    if length < 0x80:
        return bytes([length])
    length_bytes = length.to_bytes((length.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(length_bytes)]) + length_bytes


def _decode_integer(value: bytes) -> int:
    if not value:
        raise ValueError("empty DER integer")
    return int.from_bytes(value, "big", signed=False)


def _decode_oid(value: bytes) -> str:
    if not value:
        raise ValueError("empty object identifier")
    first = value[0]
    parts = [first // 40, first % 40]
    accumulator = 0
    for byte in value[1:]:
        accumulator = (accumulator << 7) | (byte & 0x7F)
        if not byte & 0x80:
            parts.append(accumulator)
            accumulator = 0
    if accumulator:
        raise ValueError("truncated object identifier")
    return ".".join(str(part) for part in parts)


def write_report_json(report: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
