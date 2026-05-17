from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import audit_records, report_to_dict
from .io import load_records, write_report_json
from .simulators import add_standard_public_primes, generate_synthetic_rsa_dataset, records_to_jsonable


def main() -> int:
    parser = argparse.ArgumentParser(description="Defensive crypto prime audit toolkit.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate_parser = subparsers.add_parser("simulate", help="Generate synthetic validation data.")
    simulate_parser.add_argument("--output", required=True, help="Path to write JSON records.")
    simulate_parser.add_argument("--bits", type=int, default=128, help="Toy RSA modulus size.")
    simulate_parser.add_argument("--seed", type=int, default=20260517)
    simulate_parser.add_argument("--include-standards", action="store_true")

    audit_parser = subparsers.add_parser("audit", help="Audit JSON or CSV records.")
    audit_parser.add_argument("--input", required=True, help="Input JSON/CSV file.")
    audit_parser.add_argument("--output", required=True, help="Output JSON report path.")
    audit_parser.add_argument("--fermat-max-steps", type=int, default=100_000)
    audit_parser.add_argument(
        "--include-sensitive-evidence",
        action="store_true",
        help="Include recovered toy factors in the report. Use only for owned test data.",
    )

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
        write_report_json(report_to_dict(report), args.output)
        return 0

    parser.error(f"unknown command {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

