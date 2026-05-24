from __future__ import annotations

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
    generated_at = str(read_json(REPO_ROOT / "data/evidence_pack.json")["generated_at"])
    with tempfile.TemporaryDirectory(prefix="primeproject-publication-") as tmp_dir:
        tmp = Path(tmp_dir)
        outputs = {
            "evidence_pack": tmp / "evidence_pack.json",
            "claim_ledger": tmp / "claim_ledger.json",
            "artifact_lineage": tmp / "artifact_lineage.json",
            "decision_protocol": tmp / "decision_protocol.json",
            "falsification_battery": tmp / "falsification_battery.json",
        }

        run_cli(
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
        )
        run_cli(
            "claim-ledger",
            "--evidence-pack",
            str(outputs["evidence_pack"]),
            "--generated-at",
            generated_at,
            "--output",
            str(outputs["claim_ledger"]),
        )
        run_cli(
            "artifact-lineage",
            "--generated-at",
            generated_at,
            "--output",
            str(outputs["artifact_lineage"]),
        )
        run_cli(
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
        )
        run_cli(
            "falsification-battery",
            "--attribution-grid",
            "data/attribution_confound_grid.json",
            "--decision-protocol",
            str(outputs["decision_protocol"]),
            "--generated-at",
            generated_at,
            "--output",
            str(outputs["falsification_battery"]),
        )

        mismatches = [
            name
            for name, public_path in PUBLICATION_OUTPUTS.items()
            if read_json(outputs[name]) != read_json(REPO_ROOT / public_path)
        ]

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


def run_cli(*args: str) -> None:
    command = [sys.executable, "-m", "prime_audit.cli", *args]
    subprocess.run(command, cwd=REPO_ROOT, check=True)


if __name__ == "__main__":
    raise SystemExit(main())
