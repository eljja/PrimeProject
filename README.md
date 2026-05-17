# PrimeProject

`PrimeProject` explores practical regularity analysis for cryptographic primes. The current implementation focuses on defensive audits of owned key material and synthetic experiments.

## What it does

- Loads RSA modulus and public prime records from JSON or CSV.
- Extracts bit-length, low-bit, and small-prime residue fingerprints.
- Checks RSA datasets for duplicate moduli, shared prime factors, small modulus size, near-square factorization risk, and ROCA-like constrained residue fingerprints.
- Recognizes selected ECC field primes.
- Generates synthetic toy RSA datasets for validation experiments.
- Explores algorithm-induced prime measures in the PrimeProject Conjecture Lab.

## Interactive Conjecture Lab

Open `index.html` locally or publish this repository with GitHub Pages to view the interactive visualization. The lab compares `rejection`, `next_prime`, and `wheel30_next` observation measures over prime gaps and residue classes.

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
```

The bundled Codex runtime Python can also run the same commands.

## Boundary

This project is for defensive quality auditing and controlled experiments. It does not scan external targets, and recovered factors are omitted from reports unless `--include-sensitive-evidence` is explicitly used for owned test data.

## License

Apache License 2.0. See [LICENSE](LICENSE).
