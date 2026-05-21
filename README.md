# PrimeProject

`PrimeProject` explores practical regularity analysis for cryptographic primes. The current implementation focuses on defensive audits of owned key material, key-quality policy checks, and synthetic generator-bias experiments.

## What it does

- Loads RSA modulus and public prime records from JSON, CSV, PEM, DER, certificate, and CSR inputs.
- Extracts bit-length, low-bit, and small-prime residue fingerprints.
- Checks RSA datasets for duplicate moduli, shared prime factors, small modulus size, near-square factorization risk, and ROCA-like constrained residue fingerprints.
- Recognizes selected ECC field primes.
- Generates synthetic toy RSA datasets for validation experiments.
- Explores algorithm-induced prime measures and next-prime candidate ranking in the PrimeProject Conjecture Lab.
- Extracts generator fingerprints from prime-like parameters, including residues, low bits, and local prime-gap context.
- Builds known-good generator baselines and compares suspicious datasets by fingerprint distance with sample-quality confidence.
- Benchmarks generator attribution against synthetic ground-truth samples with accuracy, confusion matrices, and feature ablation.
- Audits Bitcoin secp256k1 constants and ECDSA signature metadata for defensive nonce-risk indicators.

## Interactive Conjecture Lab

Open the GitHub Pages app: [https://eljja.github.io/PrimeProject/](https://eljja.github.io/PrimeProject/)

You can also open `index.html` locally. The lab compares `rejection`, `next_prime`, and `wheel30_next` observation measures over prime gaps and residue classes.

The live browser experiment can compute directly up to 10M with a logarithmic search-limit slider. Larger local runs can also be bundled as static Research Snapshots on GitHub Pages, so visitors can inspect precomputed SVG charts without recalculating them in the browser. The Bias Ranking Lab orders next-prime candidates with a toy density/residue/gap score for generator-bias analysis; it is not a cryptographic prime prediction engine.

## Input format

```json
{
  "records": [
    {
      "key_id": "example",
      "algorithm": "rsa",
      "value": "0x...",
      "public_exponent": 65537,
      "source": "owned-test"
    }
  ]
}
```

`algorithm` can be `rsa`, `dh`, `ffdhe`, `modp`, `ecc`, `ec`, `field-prime`, or `prime`. PEM, DER, X.509 certificate, and CSR inputs currently extract RSA public modulus and exponent records.

## Usage

```powershell
python -m prime_audit.cli simulate --output data/synthetic_keys.json --bits 128 --include-standards
python -m prime_audit.cli audit --input data/synthetic_keys.json --output data/audit_report.json --fail-on high
python -m prime_audit.cli fingerprint-primes --input data/synthetic_keys.json --output data/generator_fingerprints.json
python -m prime_audit.cli build-baseline --fingerprint data/generator_fingerprints.json --name openssl-owned-sample --output data/baselines/openssl_owned.json
python -m prime_audit.cli compare-baselines --fingerprint data/generator_fingerprints.json --baselines data/baselines/openssl_owned.json --output data/baseline_comparison.json
python -m prime_audit.cli attribution-benchmark --limit 200000 --train-count 80 --test-count 40 --trials 3 --output data/attribution_benchmark.json
python -m prime_audit.cli gap-lab --limit 100000 --modulo 30 --output data/conjecture_lab_100k.json
python -m prime_audit.cli bias-rank --start 100000 --span 640 --modulo 210 --output data/bias_rank_100k.json
python -m prime_audit.cli bitcoin-constants --output data/bitcoin_constants.json
python -m prime_audit.cli bitcoin-signature-audit --input data/bitcoin_signatures.json --output data/bitcoin_signature_audit.json
python -m prime_audit.cli snapshot --limit 10000000 --modulo 210 --output data/snapshots/prime_measure_10m.summary.json --assets-dir assets/snapshots --slug prime_measure_10m
python -m prime_audit.cli snapshot-manifest --inputs data/snapshots/prime_measure_1m.summary.json data/snapshots/prime_measure_10m.summary.json --output data/snapshots/manifest.json
python scripts/benchmark_shared_factors.py --count 1000 --bits 128 --output data/shared_factor_benchmark.json
```

The bundled Codex runtime Python can also run the same commands.

## Boundary

This project is for defensive quality auditing and controlled experiments. It does not scan external targets, and recovered factors are omitted from reports unless `--include-sensitive-evidence` is explicitly used for owned test data.

## License

Apache License 2.0. See [LICENSE](LICENSE).
