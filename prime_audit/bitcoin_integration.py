from __future__ import annotations

from typing import Any


BITCOIN_RESEARCH_REPORT_SCHEMA = "primeproject.bitcoin-generator-risk-report.v1"


def build_bitcoin_generator_risk_report(
    signature_audit: dict[str, Any],
    baseline_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    signature_count = int(signature_audit.get("signature_count") or 0)
    unique_r_count = int(signature_audit.get("unique_r_count") or 0)
    reused_r_group_count = int(signature_audit.get("reused_r_group_count") or 0)
    findings = signature_audit.get("findings", [])
    nonce_fingerprint = {
        "signature_count": signature_count,
        "unique_r_ratio": unique_r_count / signature_count if signature_count else None,
        "reused_r_group_rate": reused_r_group_count / signature_count if signature_count else None,
        "high_s_rate": finding_rate(findings, "high_s", signature_count),
        "invalid_range_rate": (
            count_findings(findings, "invalid_r") + count_findings(findings, "invalid_s")
        ) / signature_count if signature_count else None,
    }
    return {
        "schema": BITCOIN_RESEARCH_REPORT_SCHEMA,
        "source_schema": signature_audit.get("schema"),
        "nonce_fingerprint": nonce_fingerprint,
        "finding_counts": finding_counts(findings),
        "risk_level": bitcoin_risk_level(signature_audit),
        "related_baselines": related_bitcoin_baselines(baseline_manifest or {}),
        "research_actions": bitcoin_research_actions(signature_audit, baseline_manifest or {}),
    }


def finding_counts(findings: list[dict[str, Any]]) -> dict[str, Any]:
    by_check: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    for finding in findings:
        check = str(finding.get("check") or "unknown")
        severity = str(finding.get("severity") or "unknown")
        by_check[check] = by_check.get(check, 0) + 1
        by_severity[severity] = by_severity.get(severity, 0) + 1
    return {
        "by_check": by_check,
        "by_severity": by_severity,
    }


def count_findings(findings: list[dict[str, Any]], check: str) -> int:
    return sum(1 for finding in findings if finding.get("check") == check)


def finding_rate(findings: list[dict[str, Any]], check: str, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return count_findings(findings, check) / denominator


def bitcoin_risk_level(signature_audit: dict[str, Any]) -> str:
    findings = signature_audit.get("findings", [])
    severities = {finding.get("severity") for finding in findings}
    if "critical" in severities:
        return "critical"
    if "high" in severities:
        return "high"
    if signature_audit.get("reused_r_group_count", 0):
        return "high"
    if "warning" in severities:
        return "medium"
    return "low"


def related_bitcoin_baselines(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    related = []
    for entry in manifest.get("entries", []):
        text = " ".join(
            str(entry.get(field) or "")
            for field in ("baseline_id", "library", "algorithm", "object_type", "notes")
        ).lower()
        if "bitcoin" in text or "secp256k1" in text or entry.get("object_type") in {"ecdsa-signature", "schnorr-signature"}:
            related.append(
                {
                    "baseline_id": entry.get("baseline_id"),
                    "library": entry.get("library"),
                    "object_type": entry.get("object_type"),
                    "status": entry.get("status"),
                    "sample_count": entry.get("sample_count"),
                    "sensitive": entry.get("sensitive"),
                }
            )
    return related


def bitcoin_research_actions(signature_audit: dict[str, Any], manifest: dict[str, Any]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    if signature_audit.get("reused_r_group_count", 0):
        actions.append(
            {
                "priority": "P0",
                "track": "nonce-reuse",
                "action": "Isolate repeated-r groups by public key and wallet provenance using owned metadata.",
            }
        )
    if count_findings(signature_audit.get("findings", []), "high_s"):
        actions.append(
            {
                "priority": "P2",
                "track": "policy-drift",
                "action": "Compare high-s rate by wallet/library release window before attributing generator weakness.",
            }
        )
    if not related_bitcoin_baselines(manifest):
        actions.append(
            {
                "priority": "P1",
                "track": "baseline-gap",
                "action": "Register Bitcoin Core, libsecp256k1, and wallet signature metadata baselines.",
            }
        )
    else:
        actions.append(
            {
                "priority": "P1",
                "track": "fingerprint-distance",
                "action": "Convert nonce fingerprint metrics into feature vectors and compare against registered wallet baselines.",
            }
        )
    return actions
