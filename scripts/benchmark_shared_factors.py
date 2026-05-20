from __future__ import annotations

import argparse
import json
import time
import tracemalloc
from random import Random
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from prime_audit.number_theory import product_tree_shared_factors, random_prime


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Benchmark shared-prime detection over synthetic RSA moduli."
    )
    parser.add_argument("--count", type=int, default=1000, help="Number of moduli to generate.")
    parser.add_argument("--bits", type=int, default=128, help="Approximate RSA modulus size.")
    parser.add_argument("--seed", type=int, default=20260519)
    parser.add_argument("--shared-pairs", type=int, default=1)
    parser.add_argument("--output", default=None, help="Optional JSON output path.")
    args = parser.parse_args()

    if args.count < args.shared_pairs * 2:
        raise ValueError("count must be at least twice shared-pairs")
    if args.bits < 32:
        raise ValueError("bits must be at least 32")

    rng = Random(args.seed)
    moduli = build_synthetic_moduli(args.count, args.bits, args.shared_pairs, rng)

    tracemalloc.start()
    started = time.perf_counter()
    shared = product_tree_shared_factors(moduli)
    elapsed_seconds = time.perf_counter() - started
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result = {
        "schema": "primeproject.shared-factor-benchmark.v1",
        "count": args.count,
        "bits": args.bits,
        "seed": args.seed,
        "shared_pairs": args.shared_pairs,
        "elapsed_seconds": elapsed_seconds,
        "peak_memory_bytes": peak_bytes,
        "detected_shared_moduli": len(shared),
    }
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text)
    return 0


def build_synthetic_moduli(count: int, bits: int, shared_pairs: int, rng: Random) -> list[int]:
    prime_bits = bits // 2
    moduli: list[int] = []
    for _ in range(shared_pairs):
        shared_prime = random_prime(prime_bits, rng)
        moduli.append(shared_prime * random_prime(prime_bits, rng))
        moduli.append(shared_prime * random_prime(prime_bits, rng))
    while len(moduli) < count:
        moduli.append(random_prime(prime_bits, rng) * random_prime(prime_bits, rng))
    rng.shuffle(moduli)
    return moduli


if __name__ == "__main__":
    raise SystemExit(main())
