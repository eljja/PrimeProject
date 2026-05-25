from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generate_open_problem_workbench import build_payload


def canonical(payload: dict[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Recompute and verify open problem bounded certificates.")
    parser.add_argument("--input", type=Path, default=Path("data/open_problem_workbench.json"))
    args = parser.parse_args()

    public_payload = json.loads(args.input.read_text(encoding="utf-8"))
    rebuilt = build_payload(
        int(public_payload["search_limit"]),
        generated_at=str(public_payload["generated_at"]),
    )

    if canonical(public_payload) != canonical(rebuilt):
        public_by_id = {problem["id"]: problem for problem in public_payload.get("problems", [])}
        rebuilt_by_id = {problem["id"]: problem for problem in rebuilt.get("problems", [])}
        mismatches = []
        for problem_id, problem in rebuilt_by_id.items():
            if canonical(public_by_id.get(problem_id, {})) != canonical(problem):
                mismatches.append(problem_id)
        print(
            "Open problem workbench reproduction failed: "
            + (", ".join(mismatches) if mismatches else "top-level metadata"),
            file=sys.stderr,
        )
        return 1

    certificate_roots = {
        problem["id"]: problem["certificate"]["merkle_root"]
        for problem in rebuilt["problems"]
    }
    print(
        "Open problem bounded certificates reproduce exactly: "
        + ", ".join(f"{key}={value[:12]}" for key, value in certificate_roots.items())
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
