from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import evaluate_policy, audit_records, report_to_dict
from .attribution import run_synthetic_attribution_benchmark
from .baselines import build_generator_baseline, compare_fingerprint_to_baselines
from .bitcoin import audit_bitcoin_signatures, secp256k1_constants_report
from .conjecture_lab import run_lab
from .fingerprints import analyze_prime_generator_fingerprints
from .io import load_records, write_report_json
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
    attribution_parser.add_argument("--output", required=True)

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
