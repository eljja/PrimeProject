from __future__ import annotations

from dataclasses import asdict
from math import gcd
from typing import Any

from .catalog import classify_public_prime, recognize_standard_prime
from .models import AuditReport, FeatureSet, Finding, KeyRecord
from .number_theory import (
    SMALL_PRIMES,
    distance_to_next_square,
    fermat_factor_if_close,
    is_probable_prime,
    product_tree_shared_factors,
)


SEVERITY_ORDER = {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def residue_fingerprint(value: int, primes: tuple[int, ...] = SMALL_PRIMES) -> dict[int, int]:
    return {prime: value % prime for prime in primes}


def extract_features(record: KeyRecord) -> FeatureSet:
    value = record.value
    recognized = None
    if record.algorithm in {"dh", "ffdhe", "modp", "ecc", "ec", "field-prime", "prime"}:
        recognized = recognize_standard_prime(value)
    distance = distance_to_next_square(value) if record.algorithm == "rsa" else None
    return FeatureSet(
        bit_length=value.bit_length(),
        low_bits_hex=hex(value & ((1 << 32) - 1)),
        residue_fingerprint=residue_fingerprint(value),
        near_square_distance_bits=distance.bit_length() if distance is not None else None,
        recognized_parameter=recognized,
    )


def audit_records(
    records: list[KeyRecord],
    *,
    fermat_max_steps: int = 100_000,
    include_sensitive_evidence: bool = False,
) -> AuditReport:
    features = {record.key_id: extract_features(record) for record in records}
    findings: list[Finding] = []
    findings.extend(_audit_rsa_records(records, fermat_max_steps, include_sensitive_evidence))
    findings.extend(_audit_public_prime_records(records))
    findings.sort(key=lambda finding: SEVERITY_ORDER[finding.severity], reverse=True)
    return AuditReport(records=records, features=features, findings=findings)


def _audit_rsa_records(
    records: list[KeyRecord],
    fermat_max_steps: int,
    include_sensitive_evidence: bool,
) -> list[Finding]:
    rsa_records = [record for record in records if record.algorithm == "rsa"]
    findings: list[Finding] = []
    seen_moduli: dict[int, str] = {}

    for record in rsa_records:
        if record.value in seen_moduli:
            findings.append(
                Finding(
                    key_id=record.key_id,
                    check="duplicate_modulus",
                    severity="critical",
                    message=f"RSA modulus is identical to {seen_moduli[record.value]}.",
                    evidence={"matching_key_id": seen_moduli[record.value]},
                )
            )
        else:
            seen_moduli[record.value] = record.key_id

        if record.public_exponent is not None and record.public_exponent % 2 == 0:
            findings.append(
                Finding(
                    key_id=record.key_id,
                    check="public_exponent_even",
                    severity="high",
                    message="RSA public exponent is even; normal RSA exponents should be odd.",
                    evidence={"public_exponent": record.public_exponent},
                )
            )

        if record.bit_length < 2048:
            findings.append(
                Finding(
                    key_id=record.key_id,
                    check="rsa_modulus_too_small",
                    severity="medium",
                    message="RSA modulus is below the common 2048-bit minimum.",
                    evidence={"bit_length": record.bit_length},
                )
            )

        close_factor = fermat_factor_if_close(record.value, fermat_max_steps)
        if close_factor is not None:
            p, q, steps = close_factor
            evidence: dict[str, Any] = {
                "fermat_steps": steps,
                "factor_distance_bits": abs(q - p).bit_length(),
            }
            if include_sensitive_evidence:
                evidence["p"] = hex(p)
                evidence["q"] = hex(q)
            findings.append(
                Finding(
                    key_id=record.key_id,
                    check="near_square_factorization",
                    severity="high",
                    message="RSA modulus is close enough to a square to factor with Fermat search.",
                    evidence=evidence,
                )
            )

        roca_score = roca_like_residue_score(record.value)
        if roca_score >= 0.95:
            findings.append(
                Finding(
                    key_id=record.key_id,
                    check="roca_like_residue_fingerprint",
                    severity="medium",
                    message="Residue fingerprint strongly matches a ROCA-like constrained residue model.",
                    evidence={"match_ratio": roca_score},
                )
            )

    values = [record.value for record in rsa_records]
    shared_by_index = product_tree_shared_factors(values) if values else {}
    for index, factor in shared_by_index.items():
        record = rsa_records[index]
        evidence = {"shared_factor_bits": factor.bit_length()}
        if include_sensitive_evidence:
            evidence["shared_factor"] = hex(factor)
        partner_ids = [
            other.key_id
            for other in rsa_records
            if other.key_id != record.key_id and gcd(record.value, other.value) == factor
        ]
        evidence["matching_key_ids"] = partner_ids
        findings.append(
            Finding(
                key_id=record.key_id,
                check="shared_prime_factor",
                severity="critical",
                message="RSA modulus shares a non-trivial factor with another modulus in this dataset.",
                evidence=evidence,
            )
        )

    return findings


def _audit_public_prime_records(records: list[KeyRecord]) -> list[Finding]:
    findings: list[Finding] = []
    for record in records:
        if record.algorithm not in {"dh", "ffdhe", "modp", "ecc", "ec", "field-prime", "prime"}:
            continue

        classification = classify_public_prime(record.value)
        recognized = classification["recognized_parameter"]
        if recognized:
            findings.append(
                Finding(
                    key_id=record.key_id,
                    check="standard_public_prime",
                    severity="info",
                    message=f"Public prime matches known parameter {recognized}.",
                    evidence=classification,
                )
            )
            continue

        if not classification["is_probable_prime"]:
            findings.append(
                Finding(
                    key_id=record.key_id,
                    check="public_parameter_not_prime",
                    severity="high",
                    message="Public field or DH parameter is not prime.",
                    evidence=classification,
                )
            )
        elif not classification["is_safe_prime"] and record.algorithm in {"dh", "ffdhe", "modp"}:
            findings.append(
                Finding(
                    key_id=record.key_id,
                    check="dh_prime_not_safe_prime",
                    severity="medium",
                    message="DH modulus is prime but does not satisfy the safe-prime condition.",
                    evidence=classification,
                )
            )
        else:
            findings.append(
                Finding(
                    key_id=record.key_id,
                    check="unknown_public_prime",
                    severity="low",
                    message="Public prime is not in the built-in standard catalog; manual provenance review is recommended.",
                    evidence=classification,
                )
            )

    return findings


def roca_like_residue_score(value: int) -> float:
    checks = 0
    matches = 0
    for prime in SMALL_PRIMES:
        if prime in {3, 5}:
            continue
        residue = value % prime
        subgroup = _powers_mod(65537 % prime, prime)
        if 1 < len(subgroup) < prime - 1:
            checks += 1
            if residue in subgroup:
                matches += 1
    return matches / checks if checks else 0.0


def _powers_mod(base: int, modulus: int) -> set[int]:
    if base == 0:
        return {0}
    result = set()
    value = 1
    while value not in result:
        result.add(value)
        value = (value * base) % modulus
    return result


def report_to_dict(report: AuditReport) -> dict[str, Any]:
    return {
        "summary": summarize_findings(report.findings),
        "records": [
            {
                "key_id": record.key_id,
                "algorithm": record.algorithm,
                "bit_length": record.bit_length,
                "source": record.source,
                "created_at": record.created_at,
                "issuer_or_vendor": record.issuer_or_vendor,
            }
            for record in report.records
        ],
        "features": {key_id: asdict(features) for key_id, features in report.features.items()},
        "findings": [asdict(finding) for finding in report.findings],
    }


def summarize_findings(findings: list[Finding]) -> dict[str, int]:
    summary = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for finding in findings:
        summary[finding.severity] += 1
    return summary

