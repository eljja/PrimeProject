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
- Benchmarks generator attribution against synthetic ground-truth samples with accuracy, confusion matrices, feature ablation, bit-length confound control, and paired confound-grid deltas.
- Registers real-world baseline manifests for OpenSSL, BoringSSL, Go, Bitcoin Core, and wallet/library samples without publishing sensitive key material.
- Defines a real-world collection matrix for matched OpenSSL/BoringSSL/Go RSA-prime targets and Bitcoin signature metadata before stronger claims are allowed.
- Estimates sample-size power floors so collection targets are marked as coarse screening or stronger evidence before publication claims.
- Generates provenance requirements for real-world baselines so library version, build flags, RNG source, commands, and aggregate artifact hashes are captured before attribution claims.
- Exports fixed-length fingerprint vectors and runs a dependency-free Crypto-Classifier baseline before heavier ML experiments.
- Scores end-to-end research readiness across Sim-to-Real baselines, attribution validation, classifier data, and Bitcoin integration.
- Bundles checksummed evidence packs that state publication gates and claim limits.
- Audits Bitcoin secp256k1 constants and ECDSA signature metadata for defensive nonce-risk indicators.

## Interactive Conjecture Lab

Open the GitHub Pages app: [https://eljja.github.io/PrimeProject/](https://eljja.github.io/PrimeProject/)

You can also open `index.html` locally. The lab compares `rejection`, `next_prime`, and `wheel30_next` observation measures over prime gaps and residue classes.

The live browser experiment can compute directly up to 10M with a logarithmic search-limit slider. Larger local runs can also be bundled as static Research Snapshots on GitHub Pages, so visitors can inspect precomputed SVG charts without recalculating them in the browser. The Bias Ranking Lab orders next-prime candidates with a toy density/residue/gap score for generator-bias analysis; it is not a cryptographic prime prediction engine.

The Project Evolution panel reads `data/project_evolution.json` and visualizes how the work moved from prime-measure experiments to controlled attribution, real-world baseline scaffolding, readiness gates, and evidence packs.

The Attribution Grid panel displays a bundled paired benchmark from `data/attribution_confound_grid.json`, highlighting which fingerprint profiles survive bit-length control and which ones are likely range confounds.

The Baseline Lab panel reads `data/baselines/real_world/manifest.json`, `data/collection_matrix.json`, `data/collection_power.json`, and `data/provenance_requirements.json` to show which real-world baseline families are registered, whether targets are only coarse screening or strong enough for tighter claims, and which provenance fields are still missing.

The Research Readiness panel reads `data/research_readiness.json` and surfaces blocking gaps before any real-world attribution claim is treated as strong.

The Evidence Pack panel reads `data/evidence_pack.json` and shows checksums, publication gates, and the maximum safe claim level for the bundled artifacts.

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
python -m prime_audit.cli real-baseline-manifest --output data/baselines/real_world/manifest.json
python -m prime_audit.cli collection-matrix --manifest data/baselines/real_world/manifest.json --output data/collection_matrix.json
python -m prime_audit.cli collection-power --matrix data/collection_matrix.json --output data/collection_power.json
python -m prime_audit.cli provenance-requirements --manifest data/baselines/real_world/manifest.json --output data/provenance_requirements.json
python -m prime_audit.cli export-feature-vectors --fingerprints openssl=data/openssl_fingerprint.json suspicious=data/suspicious_fingerprint.json --output data/feature_vectors.json
python -m prime_audit.cli crypto-classifier --features data/feature_vectors.json --output data/crypto_classifier_report.json
python -m prime_audit.cli research-readiness --manifest data/baselines/real_world/manifest.json --attribution-grid data/attribution_confound_grid.json --output data/research_readiness.json
python -m prime_audit.cli evidence-pack --manifest data/baselines/real_world/manifest.json --readiness data/research_readiness.json --attribution-grid data/attribution_confound_grid.json --artifact project_evolution=data/project_evolution.json snapshot_manifest=data/snapshots/manifest.json collection_matrix=data/collection_matrix.json collection_power=data/collection_power.json provenance_requirements=data/provenance_requirements.json --output data/evidence_pack.json
python -m prime_audit.cli attribution-benchmark --limit 200000 --train-count 80 --test-count 40 --trials 3 --control-mode bit_length --output data/attribution_benchmark.json
python -m prime_audit.cli attribution-grid --limits 50000 200000 --train-counts 40 80 --test-counts 20 40 --trials 3 --repeats 3 --output data/attribution_confound_grid.json
python -m prime_audit.cli gap-lab --limit 100000 --modulo 30 --output data/conjecture_lab_100k.json
python -m prime_audit.cli bias-rank --start 100000 --span 640 --modulo 210 --output data/bias_rank_100k.json
python -m prime_audit.cli bitcoin-constants --output data/bitcoin_constants.json
python -m prime_audit.cli bitcoin-signature-audit --input data/bitcoin_signatures.json --output data/bitcoin_signature_audit.json
python -m prime_audit.cli bitcoin-risk-report --signature-audit data/bitcoin_signature_audit.json --manifest data/baselines/real_world/manifest.json --output data/bitcoin_generator_risk_report.json
python -m prime_audit.cli snapshot --limit 10000000 --modulo 210 --output data/snapshots/prime_measure_10m.summary.json --assets-dir assets/snapshots --slug prime_measure_10m
python -m prime_audit.cli snapshot-manifest --inputs data/snapshots/prime_measure_1m.summary.json data/snapshots/prime_measure_10m.summary.json --output data/snapshots/manifest.json
python scripts/benchmark_shared_factors.py --count 1000 --bits 128 --output data/shared_factor_benchmark.json
```

The bundled Codex runtime Python can also run the same commands.

## Boundary

This project is for defensive quality auditing and controlled experiments. It does not scan external targets, and recovered factors are omitted from reports unless `--include-sensitive-evidence` is explicitly used for owned test data.

## License

Apache License 2.0. See [LICENSE](LICENSE).
