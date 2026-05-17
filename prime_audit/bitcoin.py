from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .number_theory import is_probable_prime, parse_int


SECP256K1_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
SECP256K1_A = 0
SECP256K1_B = 7
SECP256K1_GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
SECP256K1_GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


@dataclass(frozen=True)
class BitcoinSignatureRecord:
    signature_id: str
    r: int
    s: int
    public_key: str | None = None
    txid: str | None = None
    input_index: int | None = None
    sighash_type: int | None = None


def secp256k1_constants_report() -> dict[str, Any]:
    return {
        "schema": "primeproject.bitcoin-constants.v1",
        "curve": "secp256k1",
        "field_prime_p": {
            "hex": f"{SECP256K1_P:x}",
            "decimal": str(SECP256K1_P),
            "bit_length": SECP256K1_P.bit_length(),
            "formula": "2^256 - 2^32 - 977",
            "is_probable_prime": is_probable_prime(SECP256K1_P),
        },
        "group_order_n": {
            "hex": f"{SECP256K1_N:x}",
            "decimal": str(SECP256K1_N),
            "bit_length": SECP256K1_N.bit_length(),
            "is_probable_prime": is_probable_prime(SECP256K1_N),
        },
        "curve_equation": "y^2 = x^3 + 7 mod p",
        "base_point": {
            "gx": f"{SECP256K1_GX:x}",
            "gy": f"{SECP256K1_GY:x}",
        },
    }


def audit_bitcoin_signatures(rows: list[dict[str, Any]]) -> dict[str, Any]:
    records = [signature_record_from_mapping(row, index) for index, row in enumerate(rows)]
    findings: list[dict[str, Any]] = []
    r_groups: dict[int, list[BitcoinSignatureRecord]] = {}

    for record in records:
        r_groups.setdefault(record.r, []).append(record)
        if not 1 <= record.r < SECP256K1_N:
            findings.append(_finding(record, "invalid_r", "critical", "ECDSA r is outside the secp256k1 group order."))
        if not 1 <= record.s < SECP256K1_N:
            findings.append(_finding(record, "invalid_s", "critical", "ECDSA s is outside the secp256k1 group order."))
        elif record.s > SECP256K1_N // 2:
            findings.append(_finding(record, "high_s", "warning", "Signature is valid-range but not low-s normalized."))

    for r_value, group in sorted(r_groups.items(), key=lambda item: item[0]):
        if len(group) < 2:
            continue
        public_keys = sorted({record.public_key for record in group if record.public_key})
        severity = "critical" if len(public_keys) <= 1 else "high"
        findings.append(
            {
                "check": "reused_r",
                "severity": severity,
                "message": "Repeated ECDSA r indicates nonce reuse or nonce correlation risk. Private-key recovery evidence is intentionally omitted.",
                "evidence": {
                    "r_hex": f"{r_value:x}",
                    "signature_ids": [record.signature_id for record in group],
                    "public_keys": public_keys,
                },
            }
        )

    return {
        "schema": "primeproject.bitcoin-signature-audit.v1",
        "signature_count": len(records),
        "unique_r_count": len(r_groups),
        "reused_r_group_count": sum(1 for group in r_groups.values() if len(group) > 1),
        "findings": findings,
    }


def signature_record_from_mapping(row: dict[str, Any], index: int = 0) -> BitcoinSignatureRecord:
    signature_id = str(row.get("signature_id") or row.get("id") or f"sig-{index + 1}")
    sighash_type = row.get("sighash_type")
    if "der" in row or "signature_der" in row:
        r, s, parsed_sighash = parse_der_signature(str(row.get("der") or row.get("signature_der")))
        if sighash_type is None:
            sighash_type = parsed_sighash
    else:
        r = parse_int(row["r"])
        s = parse_int(row["s"])
    input_index = row.get("input_index")
    return BitcoinSignatureRecord(
        signature_id=signature_id,
        r=r,
        s=s,
        public_key=row.get("public_key"),
        txid=row.get("txid"),
        input_index=int(input_index) if input_index is not None else None,
        sighash_type=int(sighash_type) if sighash_type is not None else None,
    )


def parse_der_signature(value: str) -> tuple[int, int, int | None]:
    data = bytes.fromhex(value.removeprefix("0x").strip())
    if len(data) < 8 or data[0] != 0x30:
        raise ValueError("ECDSA signature must be DER sequence")
    sequence_length = data[1]
    expected_total = 2 + sequence_length
    sighash_type = None
    if len(data) == expected_total + 1:
        sighash_type = data[-1]
        data = data[:-1]
    elif len(data) != expected_total:
        raise ValueError("DER sequence length mismatch")
    cursor = 2
    if data[cursor] != 0x02:
        raise ValueError("DER r integer missing")
    r_length = data[cursor + 1]
    r_start = cursor + 2
    r_end = r_start + r_length
    r = int.from_bytes(data[r_start:r_end], "big")
    cursor = r_end
    if cursor + 2 > len(data) or data[cursor] != 0x02:
        raise ValueError("DER s integer missing")
    s_length = data[cursor + 1]
    s_start = cursor + 2
    s_end = s_start + s_length
    if s_end != len(data):
        raise ValueError("DER s integer length mismatch")
    s = int.from_bytes(data[s_start:s_end], "big")
    return r, s, sighash_type


def _finding(record: BitcoinSignatureRecord, check: str, severity: str, message: str) -> dict[str, Any]:
    return {
        "signature_id": record.signature_id,
        "check": check,
        "severity": severity,
        "message": message,
        "evidence": {
            "txid": record.txid,
            "input_index": record.input_index,
            "public_key": record.public_key,
        },
    }
