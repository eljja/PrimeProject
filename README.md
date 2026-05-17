# PrimeProject

`PrimeProject` explores practical regularity analysis for cryptographic primes. The current implementation focuses on defensive audits of owned key material and synthetic experiments.

## What it does

- Loads RSA modulus and public prime records from JSON or CSV.
- Extracts bit-length, low-bit, and small-prime residue fingerprints.
- Checks RSA datasets for duplicate moduli, shared prime factors, small modulus size, near-square factorization risk, and ROCA-like constrained residue fingerprints.
- Recognizes selected ECC field primes.
- Generates synthetic toy RSA datasets for validation experiments.
- Explores algorithm-induced prime measures in the PrimeProject Conjecture Lab.
- Audits Bitcoin secp256k1 constants and ECDSA signature metadata for defensive nonce-risk indicators.

## Interactive Conjecture Lab

Open the GitHub Pages app: [https://eljja.github.io/PrimeProject/](https://eljja.github.io/PrimeProject/)

You can also open `index.html` locally. The lab compares `rejection`, `next_prime`, and `wheel30_next` observation measures over prime gaps and residue classes.

The live browser experiment is intentionally bounded for responsiveness. Larger local runs are bundled as static Research Snapshots on GitHub Pages, so visitors can inspect 1M and 10M precomputed SVG charts without recalculating them in the browser. The Prediction Lab ranks next-prime candidates with a practical hazard score rather than claiming deterministic prime prediction.

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

`algorithm` can be `rsa`, `dh`, `ffdhe`, `modp`, `ecc`, `ec`, `field-prime`, or `prime`.

## Usage

```powershell
python -m prime_audit.cli simulate --output data/synthetic_keys.json --bits 128 --include-standards
python -m prime_audit.cli audit --input data/synthetic_keys.json --output data/audit_report.json
python -m prime_audit.cli gap-lab --limit 100000 --modulo 30 --output data/conjecture_lab_100k.json
python -m prime_audit.cli predict --start 100000 --span 640 --modulo 210 --output data/prediction_100k.json
python -m prime_audit.cli bitcoin-constants --output data/bitcoin_constants.json
python -m prime_audit.cli bitcoin-signature-audit --input data/bitcoin_signatures.json --output data/bitcoin_signature_audit.json
python -m prime_audit.cli snapshot --limit 10000000 --modulo 210 --output data/snapshots/prime_measure_10m.summary.json --assets-dir assets/snapshots --slug prime_measure_10m
python -m prime_audit.cli snapshot-manifest --inputs data/snapshots/prime_measure_1m.summary.json data/snapshots/prime_measure_10m.summary.json --output data/snapshots/manifest.json
```

The bundled Codex runtime Python can also run the same commands.

## Boundary

This project is for defensive quality auditing and controlled experiments. It does not scan external targets, and recovered factors are omitted from reports unless `--include-sensitive-evidence` is explicitly used for owned test data.

## License

Apache License 2.0. See [LICENSE](LICENSE).
