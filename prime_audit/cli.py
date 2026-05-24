from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import evaluate_policy, audit_records, report_to_dict
from .artifact_lineage import build_artifact_lineage
from .attribution import run_attribution_confound_grid, run_synthetic_attribution_benchmark
from .baseline_acceptance import build_baseline_acceptance
from .baseline_promotion import build_baseline_promotion_plan
from .baselines import build_generator_baseline, compare_fingerprint_to_baselines
from .bitcoin import audit_bitcoin_signatures, secp256k1_constants_report
from .bitcoin_integration import build_bitcoin_generator_risk_report
from .claim_ledger import build_claim_ledger
from .collection_contract import build_collection_submission_contract
from .collection_handoff import build_collection_handoff
from .collection_intake import build_collection_intake, load_intake_records
from .collection_fixture_audit import build_collection_fixture_audit
from .collection_lint import build_collection_submission_lint
from .conjecture_lab import run_lab
from .crypto_classifier import run_crypto_classifier
from .decision_protocol import build_decision_protocol
from .collection_matrix import build_collection_matrix
from .collection_power import build_collection_power
from .evidence_pack import build_evidence_pack
from .feature_vectors import (
    build_controlled_synthetic_feature_vectors,
    build_feature_vector_payload,
    load_feature_vectors_from_files,
)
from .falsification import build_falsification_battery
from .fingerprints import analyze_prime_generator_fingerprints
from .io import load_records, write_report_json
from .null_calibration import build_null_calibration
from .provenance import build_provenance_audit, build_provenance_requirements, load_provenance_records
from .real_baselines import build_real_baseline_manifest, load_real_baseline_entries
from .replication_audit import build_replication_audit
from .research_readiness import build_research_readiness_report
from .bias_lab import rank_next_prime_candidates
from .simulators import add_standard_public_primes, generate_synthetic_rsa_dataset, records_to_jsonable
from .snapshots import build_snapshot, render_snapshot_svgs, write_manifest, write_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Defensive crypto prime audit toolkit.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate_parser = subparsers.add_parser("simulate", help="Generate synthetic validation data.")
    simulate_parser.add_argument("--output", required=True, help="Path to write JSON records.")
    simulate_parser.add_argument("--bits", type=int, default=128, help="Toy RSA modulus size.")
    simulate_parser.add_argument("--seed", type=int, default=20260517)
    simulate_parser.add_argument("--include-standards", action="store_true")

    audit_parser = subparsers.add_parser("audit", help="Audit key records or RSA key material.")
    audit_parser.add_argument("--input", required=True, help="Input JSON/CSV/PEM/DER/CSR file.")
    audit_parser.add_argument("--output", required=True, help="Output JSON report path.")
    audit_parser.add_argument("--fermat-max-steps", type=int, default=100_000)
    audit_parser.add_argument(
        "--fail-on",
        choices=("none", "low", "medium", "high", "critical"),
        default="none",
        help="Exit non-zero when findings at or above this severity are present.",
    )
    audit_parser.add_argument(
        "--include-sensitive-evidence",
        action="store_true",
        help="Include recovered toy factors in the report. Use only for owned test data.",
    )

    gap_lab_parser = subparsers.add_parser(
        "gap-lab",
        help="Run algorithm-induced prime measure experiments.",
    )
    gap_lab_parser.add_argument("--limit", type=int, default=100_000)
    gap_lab_parser.add_argument("--modulo", type=int, default=30)
    gap_lab_parser.add_argument("--output", required=True)

    bias_rank_parser = subparsers.add_parser(
        "bias-rank",
        help="Rank next-prime candidates as a generator-bias experiment.",
    )
    _add_bias_rank_arguments(bias_rank_parser)

    predict_parser = subparsers.add_parser(
        "predict",
        help="Deprecated alias for bias-rank.",
    )
    _add_bias_rank_arguments(predict_parser)

    bitcoin_constants_parser = subparsers.add_parser(
        "bitcoin-constants",
        help="Write secp256k1 field and group-order constants.",
    )
    bitcoin_constants_parser.add_argument("--output", required=True)

    bitcoin_signature_parser = subparsers.add_parser(
        "bitcoin-signature-audit",
        help="Audit Bitcoin ECDSA signature metadata for nonce-risk indicators.",
    )
    bitcoin_signature_parser.add_argument("--input", required=True)
    bitcoin_signature_parser.add_argument("--output", required=True)

    fingerprint_parser = subparsers.add_parser(
        "fingerprint-primes",
        help="Extract generator fingerprints from prime-like public parameters.",
    )
    fingerprint_parser.add_argument("--input", required=True)
    fingerprint_parser.add_argument("--output", required=True)
    fingerprint_parser.add_argument("--gap-max-steps", type=int, default=4096)

    baseline_parser = subparsers.add_parser(
        "build-baseline",
        help="Build a named generator baseline from a fingerprint report.",
    )
    baseline_parser.add_argument("--fingerprint", required=True)
    baseline_parser.add_argument("--name", required=True)
    baseline_parser.add_argument("--source", default=None)
    baseline_parser.add_argument("--output", required=True)

    compare_baselines_parser = subparsers.add_parser(
        "compare-baselines",
        help="Compare a fingerprint report against one or more generator baselines.",
    )
    compare_baselines_parser.add_argument("--fingerprint", required=True)
    compare_baselines_parser.add_argument("--baselines", nargs="+", required=True)
    compare_baselines_parser.add_argument("--output", required=True)

    real_baseline_manifest_parser = subparsers.add_parser(
        "real-baseline-manifest",
        help="Build a safe manifest for real-world crypto object baselines.",
    )
    real_baseline_manifest_parser.add_argument("--entries", nargs="*", default=[])
    real_baseline_manifest_parser.add_argument("--no-defaults", action="store_true")
    real_baseline_manifest_parser.add_argument("--output", required=True)

    collection_matrix_parser = subparsers.add_parser(
        "collection-matrix",
        help="Build a real-world sample collection matrix from the baseline manifest.",
    )
    collection_matrix_parser.add_argument("--manifest", required=True)
    collection_matrix_parser.add_argument("--output", required=True)

    collection_power_parser = subparsers.add_parser(
        "collection-power",
        help="Estimate statistical screening power for real-world collection targets.",
    )
    collection_power_parser.add_argument("--matrix", required=True)
    collection_power_parser.add_argument("--modulo", type=int, default=210)
    collection_power_parser.add_argument("--alpha", type=float, default=0.05)
    collection_power_parser.add_argument("--target-tv", type=float, default=0.10)
    collection_power_parser.add_argument("--output", required=True)

    provenance_parser = subparsers.add_parser(
        "provenance-requirements",
        help="Build provenance requirements for real-world baseline collection.",
    )
    provenance_parser.add_argument("--manifest", required=True)
    provenance_parser.add_argument("--output", required=True)

    provenance_audit_parser = subparsers.add_parser(
        "provenance-audit",
        help="Audit filled provenance records for completeness and public-safety.",
    )
    provenance_audit_parser.add_argument("--requirements", required=True)
    provenance_audit_parser.add_argument("--records", nargs="*", default=[])
    provenance_audit_parser.add_argument("--output", required=True)

    baseline_acceptance_parser = subparsers.add_parser(
        "baseline-acceptance",
        help="Combine availability, power, and provenance into real-baseline acceptance gates.",
    )
    baseline_acceptance_parser.add_argument("--manifest", required=True)
    baseline_acceptance_parser.add_argument("--matrix", required=True)
    baseline_acceptance_parser.add_argument("--power", required=True)
    baseline_acceptance_parser.add_argument("--provenance-audit", required=True)
    baseline_acceptance_parser.add_argument("--output", required=True)

    baseline_promotion_parser = subparsers.add_parser(
        "baseline-promotion-plan",
        help="Plan the shortest path from blocked baselines to accepted real-world evidence.",
    )
    baseline_promotion_parser.add_argument("--acceptance", required=True)
    baseline_promotion_parser.add_argument("--power", required=True)
    baseline_promotion_parser.add_argument("--output", required=True)

    collection_handoff_parser = subparsers.add_parser(
        "collection-handoff",
        help="Build an execution handoff packet for real-world baseline collection.",
    )
    collection_handoff_parser.add_argument("--manifest", required=True)
    collection_handoff_parser.add_argument("--matrix", required=True)
    collection_handoff_parser.add_argument("--power", required=True)
    collection_handoff_parser.add_argument("--provenance-requirements", required=True)
    collection_handoff_parser.add_argument("--provenance-audit", required=True)
    collection_handoff_parser.add_argument("--baseline-acceptance", required=True)
    collection_handoff_parser.add_argument("--promotion-plan", required=True)
    collection_handoff_parser.add_argument("--classifier-report", default=None)
    collection_handoff_parser.add_argument("--output", required=True)

    collection_intake_parser = subparsers.add_parser(
        "collection-intake",
        help="Validate submitted real-world collection artifacts against a handoff packet.",
    )
    collection_intake_parser.add_argument("--handoff", required=True)
    collection_intake_parser.add_argument("--records", nargs="*", default=[])
    collection_intake_parser.add_argument("--output", required=True)

    collection_contract_parser = subparsers.add_parser(
        "collection-submission-contract",
        help="Build a machine-readable public submission contract for collection handoff tasks.",
    )
    collection_contract_parser.add_argument("--handoff", required=True)
    collection_contract_parser.add_argument("--output", required=True)

    collection_lint_parser = subparsers.add_parser(
        "collection-submission-lint",
        help="Lint candidate public collection submissions against the submission contract before intake.",
    )
    collection_lint_parser.add_argument("--contract", required=True)
    collection_lint_parser.add_argument("--records", nargs="*", default=[])
    collection_lint_parser.add_argument("--output", required=True)

    collection_fixture_audit_parser = subparsers.add_parser(
        "collection-fixture-audit",
        help="Audit public-safe submission fixtures against the pre-intake collection linter.",
    )
    collection_fixture_audit_parser.add_argument("--contract", required=True)
    collection_fixture_audit_parser.add_argument("--output", required=True)

    feature_vector_parser = subparsers.add_parser(
        "export-feature-vectors",
        help="Export flattened generator fingerprint vectors for classifier experiments.",
    )
    feature_vector_parser.add_argument("--fingerprints", nargs="*", default=[])
    feature_vector_parser.add_argument("--baselines", nargs="*", default=[])
    feature_vector_parser.add_argument("--claim-scope", default="unspecified")
    feature_vector_parser.add_argument("--output", required=True)

    synthetic_feature_vector_parser = subparsers.add_parser(
        "synthetic-feature-vectors",
        help="Generate controlled synthetic generator feature vectors for classifier plumbing checks.",
    )
    synthetic_feature_vector_parser.add_argument("--limit", type=int, default=200_000)
    synthetic_feature_vector_parser.add_argument("--samples-per-label", type=int, default=4)
    synthetic_feature_vector_parser.add_argument("--record-count", type=int, default=80)
    synthetic_feature_vector_parser.add_argument("--seed", type=int, default=20260523)
    synthetic_feature_vector_parser.add_argument("--gap-max-steps", type=int, default=1024)
    synthetic_feature_vector_parser.add_argument("--output", required=True)

    crypto_classifier_parser = subparsers.add_parser(
        "crypto-classifier",
        help="Evaluate labelled feature vectors with a dependency-free classifier baseline.",
    )
    crypto_classifier_parser.add_argument("--features", required=True)
    crypto_classifier_parser.add_argument(
        "--feature-space",
        choices=("linear", "interaction"),
        default="interaction",
    )
    crypto_classifier_parser.add_argument("--claim-scope", default=None)
    crypto_classifier_parser.add_argument("--output", required=True)

    bitcoin_risk_parser = subparsers.add_parser(
        "bitcoin-risk-report",
        help="Combine Bitcoin signature audit output with registered generator baselines.",
    )
    bitcoin_risk_parser.add_argument("--signature-audit", required=True)
    bitcoin_risk_parser.add_argument("--manifest", default=None)
    bitcoin_risk_parser.add_argument("--output", required=True)

    research_readiness_parser = subparsers.add_parser(
        "research-readiness",
        help="Assess end-to-end readiness of the real-world generator fingerprint research pipeline.",
    )
    research_readiness_parser.add_argument("--manifest", required=True)
    research_readiness_parser.add_argument("--attribution-grid", default=None)
    research_readiness_parser.add_argument("--classifier-report", default=None)
    research_readiness_parser.add_argument("--bitcoin-risk-report", default=None)
    research_readiness_parser.add_argument("--output", required=True)

    evidence_pack_parser = subparsers.add_parser(
        "evidence-pack",
        help="Bundle checksums, readiness gates, and publication limits for research artifacts.",
    )
    evidence_pack_parser.add_argument("--manifest", required=True)
    evidence_pack_parser.add_argument("--readiness", required=True)
    evidence_pack_parser.add_argument("--attribution-grid", default=None)
    evidence_pack_parser.add_argument("--classifier-report", default=None)
    evidence_pack_parser.add_argument("--bitcoin-risk-report", default=None)
    evidence_pack_parser.add_argument("--baseline-acceptance", default=None)
    evidence_pack_parser.add_argument("--collection-intake", default=None)
    evidence_pack_parser.add_argument(
        "--artifact",
        nargs="*",
        default=[],
        help="Additional checksummed artifact in role=path form.",
    )
    evidence_pack_parser.add_argument("--output", required=True)

    claim_ledger_parser = subparsers.add_parser(
        "claim-ledger",
        help="Map public research claims to the evidence gates and artifacts that support or block them.",
    )
    claim_ledger_parser.add_argument("--evidence-pack", required=True)
    claim_ledger_parser.add_argument("--output", required=True)

    artifact_lineage_parser = subparsers.add_parser(
        "artifact-lineage",
        help="Build a dependency and checksum lineage report for public research artifacts.",
    )
    artifact_lineage_parser.add_argument(
        "--artifact",
        nargs="*",
        default=[],
        help="Override or add artifact role=path entries. Defaults cover the bundled public artifacts.",
    )
    artifact_lineage_parser.add_argument(
        "--dependency",
        nargs="*",
        default=[],
        help="Override dependency edges as role:dep1,dep2.",
    )
    artifact_lineage_parser.add_argument("--output", required=True)

    decision_protocol_parser = subparsers.add_parser(
        "decision-protocol",
        help="Apply pre-registered publication and claim-promotion decisions to the current evidence bundle.",
    )
    decision_protocol_parser.add_argument("--evidence-pack", required=True)
    decision_protocol_parser.add_argument("--claim-ledger", required=True)
    decision_protocol_parser.add_argument("--artifact-lineage", required=True)
    decision_protocol_parser.add_argument("--output", required=True)

    falsification_parser = subparsers.add_parser(
        "falsification-battery",
        help="Run negative-control and claim-downgrade checks before promoting attribution claims.",
    )
    falsification_parser.add_argument("--attribution-grid", required=True)
    falsification_parser.add_argument("--decision-protocol", required=True)
    falsification_parser.add_argument("--output", required=True)

    null_calibration_parser = subparsers.add_parser(
        "null-calibration",
        help="Calibrate controlled attribution profiles against a row-structured random-label null.",
    )
    null_calibration_parser.add_argument("--attribution-grid", required=True)
    null_calibration_parser.add_argument("--iterations", type=int, default=5000)
    null_calibration_parser.add_argument("--seed", type=int, default=20260523)
    null_calibration_parser.add_argument("--output", required=True)

    replication_audit_parser = subparsers.add_parser(
        "replication-audit",
        help="Audit whether controlled attribution profiles replicate across limit/train/test settings.",
    )
    replication_audit_parser.add_argument("--attribution-grid", required=True)
    replication_audit_parser.add_argument("--null-calibration", default=None)
    replication_audit_parser.add_argument("--lift-threshold", type=float, default=0.10)
    replication_audit_parser.add_argument("--minimum-replicated-ratio", type=float, default=0.75)
    replication_audit_parser.add_argument("--output", required=True)

    attribution_parser = subparsers.add_parser(
        "attribution-benchmark",
        help="Evaluate generator fingerprint attribution on synthetic ground-truth samples.",
    )
    attribution_parser.add_argument("--limit", type=int, default=200_000)
    attribution_parser.add_argument("--train-count", type=int, default=80)
    attribution_parser.add_argument("--test-count", type=int, default=40)
    attribution_parser.add_argument("--trials", type=int, default=3)
    attribution_parser.add_argument("--seed", type=int, default=20260521)
    attribution_parser.add_argument("--gap-max-steps", type=int, default=1024)
    attribution_parser.add_argument(
        "--control-mode",
        choices=("none", "bit_length"),
        default="none",
        help="Hold selected nuisance variables constant across generators.",
    )
    attribution_parser.add_argument("--no-ablation", action="store_true")
    attribution_parser.add_argument("--output", required=True)

    attribution_grid_parser = subparsers.add_parser(
        "attribution-grid",
        help="Run paired uncontrolled/bit-length-controlled attribution experiments.",
    )
    attribution_grid_parser.add_argument("--limits", type=int, nargs="+", required=True)
    attribution_grid_parser.add_argument("--train-counts", type=int, nargs="+", required=True)
    attribution_grid_parser.add_argument("--test-counts", type=int, nargs="+", required=True)
    attribution_grid_parser.add_argument("--trials", type=int, default=3)
    attribution_grid_parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="Repeat each paired grid cell with independent seeds for confidence intervals.",
    )
    attribution_grid_parser.add_argument("--seed", type=int, default=20260521)
    attribution_grid_parser.add_argument("--gap-max-steps", type=int, default=1024)
    attribution_grid_parser.add_argument("--no-ablation", action="store_true")
    attribution_grid_parser.add_argument("--output", required=True)

    snapshot_parser = subparsers.add_parser(
        "snapshot",
        help="Precompute a compact research snapshot and static SVG charts.",
    )
    snapshot_parser.add_argument("--limit", type=int, required=True)
    snapshot_parser.add_argument("--modulo", type=int, default=210)
    snapshot_parser.add_argument("--bins", type=int, default=48)
    snapshot_parser.add_argument("--output", required=True)
    snapshot_parser.add_argument("--assets-dir", default=None)
    snapshot_parser.add_argument("--slug", default=None)

    manifest_parser = subparsers.add_parser(
        "snapshot-manifest",
        help="Create a manifest from precomputed snapshot JSON files.",
    )
    manifest_parser.add_argument("--inputs", nargs="+", required=True)
    manifest_parser.add_argument("--output", required=True)

    args = parser.parse_args()
    if args.command == "simulate":
        records = generate_synthetic_rsa_dataset(bits=args.bits, seed=args.seed)
        if args.include_standards:
            records = add_standard_public_primes(records)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(records_to_jsonable(records), indent=2), encoding="utf-8")
        return 0

    if args.command == "audit":
        records = load_records(args.input)
        report = audit_records(
            records,
            fermat_max_steps=args.fermat_max_steps,
            include_sensitive_evidence=args.include_sensitive_evidence,
        )
        report_dict = report_to_dict(report)
        report_dict["policy"] = evaluate_policy(report.findings, fail_on=args.fail_on)
        write_report_json(report_dict, args.output)
        return 0 if report_dict["policy"]["passed"] else 1

    if args.command == "gap-lab":
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(run_lab(args.limit, args.modulo), indent=2), encoding="utf-8")
        return 0

    if args.command in {"bias-rank", "predict"}:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = rank_next_prime_candidates(
            args.start,
            span=args.span,
            modulo=args.modulo,
            top=args.top,
            training_limit=args.training_limit,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "bitcoin-constants":
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(secp256k1_constants_report(), indent=2), encoding="utf-8")
        return 0

    if args.command == "bitcoin-signature-audit":
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        rows = payload["signatures"] if isinstance(payload, dict) else payload
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(audit_bitcoin_signatures(rows), indent=2), encoding="utf-8")
        return 0

    if args.command == "fingerprint-primes":
        records = load_records(args.input)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = analyze_prime_generator_fingerprints(records, gap_max_steps=args.gap_max_steps)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "build-baseline":
        fingerprint = json.loads(Path(args.fingerprint).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_generator_baseline(fingerprint, name=args.name, source=args.source)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "compare-baselines":
        fingerprint = json.loads(Path(args.fingerprint).read_text(encoding="utf-8"))
        baselines = [json.loads(Path(path).read_text(encoding="utf-8")) for path in args.baselines]
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = compare_fingerprint_to_baselines(fingerprint, baselines)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "real-baseline-manifest":
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        entries = load_real_baseline_entries(args.entries) if args.entries else []
        payload = build_real_baseline_manifest(
            entries,
            include_default_entries=not args.no_defaults,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "collection-matrix":
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(build_collection_matrix(manifest), indent=2), encoding="utf-8")
        return 0

    if args.command == "collection-power":
        matrix = json.loads(Path(args.matrix).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_collection_power(
            matrix,
            modulo=args.modulo,
            alpha=args.alpha,
            target_tv=args.target_tv,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "provenance-requirements":
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(build_provenance_requirements(manifest), indent=2), encoding="utf-8")
        return 0

    if args.command == "provenance-audit":
        requirements = json.loads(Path(args.requirements).read_text(encoding="utf-8"))
        records = load_provenance_records(args.records) if args.records else None
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(build_provenance_audit(requirements, records), indent=2), encoding="utf-8")
        return 0

    if args.command == "baseline-acceptance":
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        matrix = json.loads(Path(args.matrix).read_text(encoding="utf-8"))
        power = json.loads(Path(args.power).read_text(encoding="utf-8"))
        provenance_audit = json.loads(Path(args.provenance_audit).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_baseline_acceptance(
            manifest=manifest,
            matrix=matrix,
            power=power,
            provenance_audit=provenance_audit,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "baseline-promotion-plan":
        acceptance = json.loads(Path(args.acceptance).read_text(encoding="utf-8"))
        power = json.loads(Path(args.power).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_baseline_promotion_plan(acceptance=acceptance, power=power)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "collection-handoff":
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        matrix = json.loads(Path(args.matrix).read_text(encoding="utf-8"))
        power = json.loads(Path(args.power).read_text(encoding="utf-8"))
        provenance_requirements = json.loads(Path(args.provenance_requirements).read_text(encoding="utf-8"))
        provenance_audit = json.loads(Path(args.provenance_audit).read_text(encoding="utf-8"))
        baseline_acceptance = json.loads(Path(args.baseline_acceptance).read_text(encoding="utf-8"))
        promotion_plan = json.loads(Path(args.promotion_plan).read_text(encoding="utf-8"))
        classifier_report = (
            json.loads(Path(args.classifier_report).read_text(encoding="utf-8")) if args.classifier_report else None
        )
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_collection_handoff(
            manifest=manifest,
            matrix=matrix,
            power=power,
            provenance_requirements=provenance_requirements,
            provenance_audit=provenance_audit,
            baseline_acceptance=baseline_acceptance,
            promotion_plan=promotion_plan,
            classifier_report=classifier_report,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "collection-intake":
        handoff = json.loads(Path(args.handoff).read_text(encoding="utf-8"))
        records = load_intake_records(args.records) if args.records else None
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_collection_intake(handoff=handoff, records=records)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "collection-submission-contract":
        handoff = json.loads(Path(args.handoff).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_collection_submission_contract(handoff=handoff)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "collection-submission-lint":
        contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
        records = load_intake_records(args.records) if args.records else None
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_collection_submission_lint(contract=contract, records=records)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "collection-fixture-audit":
        contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_collection_fixture_audit(contract=contract)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "export-feature-vectors":
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        vectors = load_feature_vectors_from_files(
            fingerprint_specs=args.fingerprints,
            baseline_specs=args.baselines,
        )
        payload = build_feature_vector_payload(vectors)
        payload["claim_scope"] = args.claim_scope
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "synthetic-feature-vectors":
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_controlled_synthetic_feature_vectors(
            limit=args.limit,
            samples_per_label=args.samples_per_label,
            record_count=args.record_count,
            seed=args.seed,
            gap_max_steps=args.gap_max_steps,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "crypto-classifier":
        feature_payload = json.loads(Path(args.features).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = run_crypto_classifier(
            feature_payload,
            feature_space=args.feature_space,
            claim_scope=args.claim_scope,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "bitcoin-risk-report":
        signature_audit = json.loads(Path(args.signature_audit).read_text(encoding="utf-8"))
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8")) if args.manifest else None
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_bitcoin_generator_risk_report(signature_audit, manifest)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "research-readiness":
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        attribution_grid = (
            json.loads(Path(args.attribution_grid).read_text(encoding="utf-8"))
            if args.attribution_grid
            else None
        )
        classifier_report = (
            json.loads(Path(args.classifier_report).read_text(encoding="utf-8"))
            if args.classifier_report
            else None
        )
        bitcoin_risk_report = (
            json.loads(Path(args.bitcoin_risk_report).read_text(encoding="utf-8"))
            if args.bitcoin_risk_report
            else None
        )
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_research_readiness_report(
            manifest=manifest,
            attribution_grid=attribution_grid,
            classifier_report=classifier_report,
            bitcoin_risk_report=bitcoin_risk_report,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "evidence-pack":
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        readiness = json.loads(Path(args.readiness).read_text(encoding="utf-8"))
        attribution_grid = (
            json.loads(Path(args.attribution_grid).read_text(encoding="utf-8"))
            if args.attribution_grid
            else None
        )
        classifier_report = (
            json.loads(Path(args.classifier_report).read_text(encoding="utf-8"))
            if args.classifier_report
            else None
        )
        bitcoin_risk_report = (
            json.loads(Path(args.bitcoin_risk_report).read_text(encoding="utf-8"))
            if args.bitcoin_risk_report
            else None
        )
        baseline_acceptance = (
            json.loads(Path(args.baseline_acceptance).read_text(encoding="utf-8"))
            if args.baseline_acceptance
            else None
        )
        collection_intake = (
            json.loads(Path(args.collection_intake).read_text(encoding="utf-8"))
            if args.collection_intake
            else None
        )
        paths = {
            "manifest": args.manifest,
            "readiness": args.readiness,
        }
        if args.attribution_grid:
            paths["attribution_grid"] = args.attribution_grid
        if args.classifier_report:
            paths["classifier_report"] = args.classifier_report
        if args.bitcoin_risk_report:
            paths["bitcoin_risk_report"] = args.bitcoin_risk_report
        if args.baseline_acceptance:
            paths["baseline_acceptance"] = args.baseline_acceptance
        if args.collection_intake:
            paths["collection_intake"] = args.collection_intake
        for artifact in args.artifact:
            if "=" not in artifact:
                raise ValueError(f"artifact requires role=path, got {artifact!r}")
            role, artifact_path = artifact.split("=", 1)
            paths[role.strip()] = artifact_path.strip()
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_evidence_pack(
            manifest=manifest,
            readiness=readiness,
            attribution_grid=attribution_grid,
            classifier_report=classifier_report,
            bitcoin_risk_report=bitcoin_risk_report,
            baseline_acceptance=baseline_acceptance,
            collection_intake=collection_intake,
            file_paths=paths,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "claim-ledger":
        evidence_pack = json.loads(Path(args.evidence_pack).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_claim_ledger(evidence_pack)
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "artifact-lineage":
        artifact_paths = {}
        for artifact in args.artifact:
            if "=" not in artifact:
                raise ValueError(f"artifact requires role=path, got {artifact!r}")
            role, artifact_path = artifact.split("=", 1)
            artifact_paths[role.strip()] = artifact_path.strip()
        dependencies = {}
        for dependency in args.dependency:
            if ":" not in dependency:
                raise ValueError(f"dependency requires role:dep1,dep2, got {dependency!r}")
            role, dependency_values = dependency.split(":", 1)
            dependencies[role.strip()] = [
                item.strip()
                for item in dependency_values.split(",")
                if item.strip()
            ]
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_artifact_lineage(
            artifact_paths=artifact_paths,
            dependencies=dependencies,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "decision-protocol":
        evidence_pack = json.loads(Path(args.evidence_pack).read_text(encoding="utf-8"))
        claim_ledger = json.loads(Path(args.claim_ledger).read_text(encoding="utf-8"))
        artifact_lineage = json.loads(Path(args.artifact_lineage).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_decision_protocol(
            evidence_pack=evidence_pack,
            claim_ledger=claim_ledger,
            artifact_lineage=artifact_lineage,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "falsification-battery":
        attribution_grid = json.loads(Path(args.attribution_grid).read_text(encoding="utf-8"))
        decision_protocol = json.loads(Path(args.decision_protocol).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_falsification_battery(
            attribution_grid=attribution_grid,
            decision_protocol=decision_protocol,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "null-calibration":
        attribution_grid = json.loads(Path(args.attribution_grid).read_text(encoding="utf-8"))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_null_calibration(
            attribution_grid=attribution_grid,
            iterations=args.iterations,
            seed=args.seed,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "replication-audit":
        attribution_grid = json.loads(Path(args.attribution_grid).read_text(encoding="utf-8"))
        null_calibration = (
            json.loads(Path(args.null_calibration).read_text(encoding="utf-8"))
            if args.null_calibration
            else None
        )
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = build_replication_audit(
            attribution_grid=attribution_grid,
            null_calibration=null_calibration,
            lift_threshold=args.lift_threshold,
            minimum_replicated_ratio=args.minimum_replicated_ratio,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "attribution-benchmark":
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = run_synthetic_attribution_benchmark(
            limit=args.limit,
            train_count=args.train_count,
            test_count=args.test_count,
            trials=args.trials,
            seed=args.seed,
            gap_max_steps=args.gap_max_steps,
            include_ablation=not args.no_ablation,
            control_mode=args.control_mode,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "attribution-grid":
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = run_attribution_confound_grid(
            limits=args.limits,
            train_counts=args.train_counts,
            test_counts=args.test_counts,
            trials=args.trials,
            repeats=args.repeats,
            seed=args.seed,
            gap_max_steps=args.gap_max_steps,
            include_ablation=not args.no_ablation,
        )
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return 0

    if args.command == "snapshot":
        snapshot = build_snapshot(args.limit, args.modulo, args.bins)
        write_snapshot(snapshot, args.output)
        if args.assets_dir:
            render_snapshot_svgs(snapshot, args.assets_dir, args.slug)
        return 0

    if args.command == "snapshot-manifest":
        snapshots = [json.loads(Path(path).read_text(encoding="utf-8")) for path in args.inputs]
        write_manifest(snapshots, args.output)
        return 0

    parser.error(f"unknown command {args.command}")
    return 2


def _add_bias_rank_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--span", type=int, default=512)
    parser.add_argument("--modulo", type=int, default=210)
    parser.add_argument("--top", type=int, default=12)
    parser.add_argument("--training-limit", type=int, default=None)
    parser.add_argument("--output", required=True)


if __name__ == "__main__":
    raise SystemExit(main())
