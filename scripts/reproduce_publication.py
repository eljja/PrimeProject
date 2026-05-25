from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_OUTPUTS = {
    "evidence_pack": "data/evidence_pack.json",
    "claim_ledger": "data/claim_ledger.json",
    "artifact_lineage": "data/artifact_lineage.json",
    "decision_protocol": "data/decision_protocol.json",
    "falsification_battery": "data/falsification_battery.json",
}
DIRECT_EVIDENCE_ROLES = {
    "manifest",
    "readiness",
    "attribution_grid",
    "classifier_report",
    "baseline_acceptance",
    "collection_intake",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Reproduce and compare PrimeProject publication artifacts.")
    parser.add_argument("--report", default=None, help="Optional path to write a machine-readable audit report.")
    args = parser.parse_args()

    generated_at = str(read_json(REPO_ROOT / "data/evidence_pack.json")["generated_at"])
    commands: list[list[str]] = []
    comparisons: list[dict[str, Any]] = []
    tmp_root = ""
    with tempfile.TemporaryDirectory(prefix="primeproject-publication-") as tmp_dir:
        tmp = Path(tmp_dir)
        tmp_root = str(tmp)
        outputs = {
            "evidence_pack": tmp / "evidence_pack.json",
            "claim_ledger": tmp / "claim_ledger.json",
            "artifact_lineage": tmp / "artifact_lineage.json",
            "decision_protocol": tmp / "decision_protocol.json",
            "falsification_battery": tmp / "falsification_battery.json",
        }

        commands.append(run_cli(
            "evidence-pack",
            "--manifest",
            "data/baselines/real_world/manifest.json",
            "--readiness",
            "data/research_readiness.json",
            "--attribution-grid",
            "data/attribution_confound_grid.json",
            "--classifier-report",
            "data/crypto_classifier_report.json",
            "--baseline-acceptance",
            "data/baseline_acceptance.json",
            "--collection-intake",
            "data/collection_intake.json",
            "--artifact",
            *public_evidence_artifact_args(),
            "--generated-at",
            generated_at,
            "--output",
            str(outputs["evidence_pack"]),
        ))
        commands.append(run_cli(
            "claim-ledger",
            "--evidence-pack",
            str(outputs["evidence_pack"]),
            "--generated-at",
            generated_at,
            "--output",
            str(outputs["claim_ledger"]),
        ))
        commands.append(run_cli(
            "artifact-lineage",
            "--generated-at",
            generated_at,
            "--output",
            str(outputs["artifact_lineage"]),
        ))
        commands.append(run_cli(
            "decision-protocol",
            "--evidence-pack",
            str(outputs["evidence_pack"]),
            "--claim-ledger",
            str(outputs["claim_ledger"]),
            "--artifact-lineage",
            str(outputs["artifact_lineage"]),
            "--generated-at",
            generated_at,
            "--output",
            str(outputs["decision_protocol"]),
        ))
        commands.append(run_cli(
            "falsification-battery",
            "--attribution-grid",
            "data/attribution_confound_grid.json",
            "--decision-protocol",
            str(outputs["decision_protocol"]),
            "--generated-at",
            generated_at,
            "--output",
            str(outputs["falsification_battery"]),
        ))

        comparisons = [
            compare_artifact(name, outputs[name], REPO_ROOT / public_path)
            for name, public_path in PUBLICATION_OUTPUTS.items()
        ]

    json_mismatches = [row["artifact"] for row in comparisons if not row["json_equal"]]
    byte_mismatches = [row["artifact"] for row in comparisons if not row["byte_equal"]]
    mismatches = sorted(set(json_mismatches + byte_mismatches))
    report = {
        "schema": "primeproject.publication-reproduction-audit.v1",
        "generated_at": generated_at,
        "reproducible": not mismatches,
        "json_reproducible": not json_mismatches,
        "byte_reproducible": not byte_mismatches,
        "command_count": len(commands),
        "command_path_policy": "Temporary output paths are normalized to {tmp}.",
        "commands": [format_command(command, tmp_root=tmp_root) for command in commands],
        "comparisons": comparisons,
        "json_mismatches": json_mismatches,
        "byte_mismatches": byte_mismatches,
        "mismatches": mismatches,
    }
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if mismatches:
        print("Publication reproduction failed:", ", ".join(mismatches), file=sys.stderr)
        return 1
    print(f"Publication artifacts reproduce exactly at generated_at={generated_at}.")
    return 0


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def public_evidence_artifact_args() -> list[str]:
    evidence = read_json(REPO_ROOT / "data/evidence_pack.json")
    return [
        f"{artifact['role']}={artifact['path']}"
        for artifact in evidence["artifacts"]
        if artifact["role"] not in DIRECT_EVIDENCE_ROLES
    ]


def compare_artifact(name: str, reproduced: Path, public: Path) -> dict[str, Any]:
    reproduced_bytes = reproduced.read_bytes()
    public_bytes = public.read_bytes()
    return {
        "artifact": name,
        "public_path": str(public.relative_to(REPO_ROOT)).replace("\\", "/"),
        "json_equal": read_json(reproduced) == read_json(public),
        "byte_equal": reproduced_bytes == public_bytes,
        "reproduced_sha256": hashlib.sha256(reproduced_bytes).hexdigest(),
        "public_sha256": hashlib.sha256(public_bytes).hexdigest(),
    }


def run_cli(*args: str) -> list[str]:
    command = [sys.executable, "-m", "prime_audit.cli", *args]
    subprocess.run(command, cwd=REPO_ROOT, check=True)
    return command


def format_command(command: list[str], *, tmp_root: str) -> list[str]:
    normalized = []
    for index, value in enumerate(command):
        if index == 0:
            normalized.append("python")
            continue
        normalized.append(value.replace(tmp_root, "{tmp}") if tmp_root else value)
    return normalized


if __name__ == "__main__":
    raise SystemExit(main())
