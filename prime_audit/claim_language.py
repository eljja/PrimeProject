from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


CLAIM_LANGUAGE_AUDIT_SCHEMA = "primeproject.claim-language-audit.v1"

DEFAULT_PUBLIC_PATHS = (
    "README.md",
    "PrimeProject_Strategic_Review.md",
    "index.html",
    "assets/app.js",
    "docs/*.md",
)


@dataclass(frozen=True)
class LanguageRule:
    rule_id: str
    severity: str
    trigger: re.Pattern[str]
    guard: re.Pattern[str]
    message: str


LANGUAGE_RULES = (
    LanguageRule(
        rule_id="cryptographic_break_or_key_recovery",
        severity="critical",
        trigger=re.compile(
            r"\b(break|crack|recover private keys?|key recovery|키 유출|복원)\b",
            re.IGNORECASE,
        ),
        guard=re.compile(
            r"\b(not|cannot|does not|without|blocked|risk|toy|owned|no)\b|"
            r"불가능|이어지지 않|부족|금지|차단|위험",
            re.IGNORECASE,
        ),
        message="Security-break or key-recovery wording must be explicitly scoped as blocked, impossible, toy, or defensive.",
    ),
    LanguageRule(
        rule_id="unsupported_real_world_attribution",
        severity="high",
        trigger=re.compile(
            r"(real[- ]world.{0,80}attribution|attribution.{0,80}real[- ]world|실세계.{0,80}attribution)",
            re.IGNORECASE,
        ),
        guard=re.compile(
            r"\b(blocked|gate|gated|not|missing|before|until|candidate|cautious|accepted|scope|"
            r"scaffold|only|claim_id|decision_id|blocked_claim_ids|required_blocked_decisions|"
            r"phase_ids|promote|not supported)\b|"
            r"차단|없|전까지|기준군|승격|부족|막|주장|뜻이 아니라|점수화|열지는 않는다",
            re.IGNORECASE,
        ),
        message="Real-world attribution language must remain gated until accepted real baselines and labelled vectors exist.",
    ),
    LanguageRule(
        rule_id="unsupported_bitcoin_attribution",
        severity="high",
        trigger=re.compile(
            r"(bitcoin.{0,120}attribution|비트코인.{0,120}attribution|비트코인.{0,120}Attribution)",
            re.IGNORECASE,
        ),
        guard=re.compile(
            r"\b(blocked|gate|gated|not|missing|before|until|risk|metadata|constants|public control|"
            r"claim_id|decision_id|blocked_claim_ids|required_blocked_decisions|promote|not supported)\b|"
            r"차단|없|전까지|상수|논스|metadata",
            re.IGNORECASE,
        ),
        message="Bitcoin attribution wording must be tied to nonce-risk evidence and stay blocked without wallet/library metadata.",
    ),
    LanguageRule(
        rule_id="unsupported_proof_or_guarantee",
        severity="high",
        trigger=re.compile(
            r"\b(proves?|proven|guarantees?)\b.{0,120}\b(real[- ]world|bitcoin|cryptographic|security)\b",
            re.IGNORECASE,
        ),
        guard=re.compile(r"\b(not|does not|cannot|blocked|scoped|only)\b|차단|아니", re.IGNORECASE),
        message="Proof or guarantee wording cannot be attached to high-risk real-world, Bitcoin, or security claims.",
    ),
    LanguageRule(
        rule_id="sensitive_material_publication",
        severity="critical",
        trigger=re.compile(
            r"\b(private_key|private_prime|wallet_seed|raw_signature_owner|raw key file|raw_key_file)\b",
            re.IGNORECASE,
        ),
        guard=re.compile(
            r"\b(must_not|must_not_publish|must not|forbidden|forbidden_public_fields|forbidden_field_names|"
            r"collector_contract|not publish|stays local|local|public[- ]safe|never publish)\b|"
            r"금지|공개 금지|절대 공개|로컬|민감",
            re.IGNORECASE,
        ),
        message="Sensitive-material field names may appear only as forbidden/local handling policy, never as public payload claims.",
    ),
)


def build_claim_language_audit(
    *,
    root: str | Path = ".",
    paths: Iterable[str] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    scan_paths = list(paths or DEFAULT_PUBLIC_PATHS)
    files = resolve_scan_files(root_path, scan_paths)
    findings: list[dict[str, Any]] = []
    scanned = []
    line_count = 0

    for file_path in files:
        relative = file_path.relative_to(root_path).as_posix()
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            findings.append(
                {
                    "rule_id": "unreadable_text_file",
                    "severity": "high",
                    "path": relative,
                    "line": None,
                    "status": "fail",
                    "snippet": "",
                    "message": "Public claim-language audit could not decode the file as UTF-8 text.",
                }
            )
            continue
        scanned.append({"path": relative, "line_count": len(lines)})
        line_count += len(lines)
        findings.extend(scan_lines(relative, lines))

    fail_count = sum(1 for finding in findings if finding["status"] == "fail")
    status = "pass" if fail_count == 0 else "fail"
    return {
        "schema": CLAIM_LANGUAGE_AUDIT_SCHEMA,
        "generated_at": generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "summary": {
            "status": status,
            "scanned_file_count": len(scanned),
            "scanned_line_count": line_count,
            "rule_count": len(LANGUAGE_RULES),
            "finding_count": len(findings),
            "fail_count": fail_count,
        },
        "quality_gate": {
            "status": status,
            "message": (
                "Public claim language stays within the current evidence boundary."
                if status == "pass"
                else "Public claim language contains unsupported high-risk wording."
            ),
        },
        "policy": {
            "scope": "README, docs, GitHub Pages HTML, and bundled frontend copy",
            "claim_boundary": "public_demo_only plus controlled_synthetic_only signal; real-world and Bitcoin attribution remain blocked",
            "sensitive_material_policy": "Private keys, private primes, seeds, raw key files, and owner-identifying signature material must stay local.",
        },
        "scanned_files": scanned,
        "rules": [
            {
                "rule_id": rule.rule_id,
                "severity": rule.severity,
                "message": rule.message,
            }
            for rule in LANGUAGE_RULES
        ],
        "findings": findings,
    }


def resolve_scan_files(root: Path, path_patterns: Iterable[str]) -> list[Path]:
    files: set[Path] = set()
    for pattern in path_patterns:
        matches = sorted(root.glob(pattern))
        for match in matches:
            if match.is_file():
                files.add(match.resolve())
    return sorted(files)


def scan_lines(relative_path: str, lines: list[str]) -> list[dict[str, Any]]:
    findings = []
    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        context = " ".join(
            item.strip()
            for item in lines[max(0, line_number - 4) : min(len(lines), line_number + 3)]
        )
        for rule in LANGUAGE_RULES:
            if not rule.trigger.search(stripped):
                continue
            if rule.guard.search(context):
                continue
            findings.append(
                {
                    "rule_id": rule.rule_id,
                    "severity": rule.severity,
                    "path": relative_path,
                    "line": line_number,
                    "status": "fail",
                    "snippet": compact_snippet(stripped),
                    "message": rule.message,
                }
            )
    return findings


def compact_snippet(value: str, limit: int = 180) -> str:
    collapsed = " ".join(value.split())
    if len(collapsed) <= limit:
        return collapsed
    return f"{collapsed[: limit - 3]}..."
