from __future__ import annotations

import sys
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DIRECT_EVIDENCE_ROLES = {
    "manifest",
    "readiness",
    "attribution_grid",
    "classifier_report",
    "baseline_acceptance",
    "collection_intake",
}

def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def public_evidence_artifact_args() -> list[str]:
    evidence = read_json(REPO_ROOT / "data/evidence_pack.json")
    return [
        f"{artifact['role']}={artifact['path']}"
        for artifact in evidence["artifacts"]
        if artifact["role"] not in DIRECT_EVIDENCE_ROLES
    ]

def run_cli(*args: str) -> list[str]:
    command = [sys.executable, "-m", "prime_audit.cli", *args]
    print("Running:", " ".join(command))
    subprocess.run(command, cwd=REPO_ROOT, check=True)
    return command

def main() -> int:
    generated_at = str(read_json(REPO_ROOT / "data/evidence_pack.json")["generated_at"])
    
    # 1. claim-language-audit
    run_cli(
        "claim-language-audit",
        "--generated-at",
        generated_at,
        "--output",
        "data/claim_language_audit.json",
    )
    
    # 2. evidence-pack
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
        "data/evidence_pack.json",
    )
    
    # 3. claim-ledger
    run_cli(
        "claim-ledger",
        "--evidence-pack",
        "data/evidence_pack.json",
        "--generated-at",
        generated_at,
        "--output",
        "data/claim_ledger.json",
    )
    
    # 4. artifact-lineage
    run_cli(
        "artifact-lineage",
        "--generated-at",
        generated_at,
        "--output",
        "data/artifact_lineage.json",
    )
    
    # 5. decision-protocol
    run_cli(
        "decision-protocol",
        "--evidence-pack",
        "data/evidence_pack.json",
        "--claim-ledger",
        "data/claim_ledger.json",
        "--artifact-lineage",
        "data/artifact_lineage.json",
        "--generated-at",
        generated_at,
        "--output",
        "data/decision_protocol.json",
    )
    
    # 6. falsification-battery
    run_cli(
        "falsification-battery",
        "--attribution-grid",
        "data/attribution_confound_grid.json",
        "--decision-protocol",
        "data/decision_protocol.json",
        "--generated-at",
        generated_at,
        "--output",
        "data/falsification_battery.json",
    )
    
    # 7. publication-consistency
    run_cli(
        "publication-consistency",
        "--evidence-pack",
        "data/evidence_pack.json",
        "--claim-ledger",
        "data/claim_ledger.json",
        "--decision-protocol",
        "data/decision_protocol.json",
        "--falsification-battery",
        "data/falsification_battery.json",
        "--generated-at",
        generated_at,
        "--output",
        "data/publication_consistency.json",
    )
    
    print("All publication files updated successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
