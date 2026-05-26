# PrimeProject

[![PrimeProject CI](https://github.com/eljja/PrimeProject/actions/workflows/ci.yml/badge.svg)](https://github.com/eljja/PrimeProject/actions/workflows/ci.yml)

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
- Calibrates controlled attribution profiles against a row-structured random-label null with family-wise correction across multiple profiles.
- Audits setting-level replication so null-calibrated profiles must repeat across limit, train-count, and test-count cells.
- Registers real-world baseline manifests for OpenSSL, BoringSSL, Go, Bitcoin Core, and wallet/library samples without publishing sensitive key material.
- Defines a real-world collection matrix for matched OpenSSL/BoringSSL/Go RSA-prime targets and Bitcoin signature metadata before stronger claims are allowed.
- Estimates sample-size power floors so collection targets are marked as coarse screening or stronger evidence before publication claims.
- Generates and audits provenance contracts for real-world baselines so library version, build flags, RNG source, commands, aggregate artifact hashes, and forbidden public sensitive fields are checked before attribution claims.
- Combines availability, provenance, and sample-power tiers into baseline acceptance gates before a real-world baseline can support attribution claims.
- Produces a baseline promotion plan that identifies the shortest collection/provenance path from blocked baselines to accepted real-world evidence.
- Converts the promotion path into a public-safe collection handoff packet with prioritized tasks, sample floors, provenance blockers, and forbidden raw-material fields.
- Publishes a machine-readable collection submission contract with task templates, required record fields, checksum rules, optional record identity binding, public feature-vector path policy, provenance identity binding, feature-vector schema rules, and forbidden public fields.
- Lints candidate public collection submissions against that contract before intake so collectors can fix task, checksum, feature-vector, duplicate, sample-floor, and public-safety errors locally.
- Audits public-safe submission fixtures that prove the linter's pass, warning, missing-feature, forbidden-field, provenance-identity, feature-label, record-identity, feature-path, and reused-checksum behavior before real collection records are accepted.
- Validates submitted collection artifacts with an intake gate for sample floors, checksums, provenance records, embedded public feature-vector contracts, claim scope, duplicate task submissions, reused aggregate hashes, and forbidden public fields.
- Exports fixed-length fingerprint vectors and runs a dependency-free Crypto-Classifier baseline before heavier ML experiments.
- Scores end-to-end research readiness across Sim-to-Real baselines, attribution validation, classifier data, and Bitcoin integration.
- Bundles checksummed evidence packs that state publication gates and claim limits.
- Builds a claim ledger that maps each public-facing research claim to the gates and artifacts that allow, qualify, or block it.
- Builds an artifact lineage graph that audits public JSON dependencies, Evidence Pack checksums, and cyclic dependency risk.
- Audits public README/docs/GitHub Pages language so visible claims cannot exceed the current evidence boundary.
- Applies a pre-registered decision protocol that separates public demo, controlled synthetic, real-world attribution, and Bitcoin nonce-risk claim promotion.
- Runs a falsification battery with paired controls, negative controls, bit-length confound guards, and claim-promotion guards before stronger attribution claims can advance.
- Runs a publication consistency audit that checks Evidence Pack, Claim Ledger, Decision Protocol, and Falsification Battery agree on the same high-risk claim boundary.
- Audits Bitcoin secp256k1 constants and ECDSA signature metadata for defensive nonce-risk indicators.

## Interactive Conjecture Lab

Open the GitHub Pages app: [https://eljja.github.io/PrimeProject/](https://eljja.github.io/PrimeProject/)

Open problem subpages:

- [Riemann Workbench](https://eljja.github.io/PrimeProject/open-problems/riemann.html)
- [Collatz Workbench](https://eljja.github.io/PrimeProject/open-problems/collatz.html)
- [Goldbach Workbench](https://eljja.github.io/PrimeProject/open-problems/goldbach.html)
- [Twin Prime Workbench](https://eljja.github.io/PrimeProject/open-problems/twin-prime.html)

You can also open `index.html` locally for an offline smoke view. In direct `file://` mode the header shows `Offline fallback data`; use a local static HTTP server or GitHub Pages when you need the current public `data/*.json` artifact bundle. The lab compares `rejection`, `next_prime`, and `wheel30_next` observation measures over prime gaps and residue classes.

The live browser experiment can compute directly up to 10M with a logarithmic search-limit slider. Larger local runs can also be bundled as static Research Snapshots on GitHub Pages, so visitors can inspect precomputed SVG charts without recalculating them in the browser. The Bias Ranking Lab orders next-prime candidates with a toy density/residue/gap score for generator-bias analysis; it is not a cryptographic prime prediction engine.

The Project Evolution panel reads `data/project_evolution.json` and now presents a condensed research narrative: six decisive metrics, a five-step visual change trail, a Hardening Map for recent collection-contract fixes, one Evidence Spine for artifact-backed readiness, and a claim-boundary view that separates supported controlled-synthetic results from blocked real-world and Bitcoin attribution claims. Its publication layer includes the post-pack consistency audit so the visible research history does not stop one governance step before the Evidence Pack panel.

The Open Problem Proof Workbench adds four GitHub Pages subpages for the Riemann Hypothesis, Collatz conjecture, Goldbach conjecture, and Twin Prime conjecture. These pages deliberately keep `open_not_proven` status visible: PrimeProject shows a proof verdict, bounded computation, Merkle-rooted bounded certificates, proof-attempt ledgers, proof attack maps, machine proof-status gates, proof execution protocols, proof frontier probes, known-barrier audits, formal replay packages, proof review dockets, proof reduction contracts, proof candidate intake rules, proof attempt execution logs, proof obligation DAGs, formal skeleton audits, Lean-oriented formal proof contracts, proof milestone queues, decisive lemma labs with certified automated falsification probes, proof-gap taxonomies with work orders, proof gates, and candidate strategies, but it does not claim a solution until an independently checkable infinite argument exists.

The bundled Crypto-Classifier panel is intentionally scoped to `controlled_synthetic_only`: it proves the feature-vector and classifier plumbing on synthetic generator fingerprints, then keeps real-world attribution blocked until OpenSSL, BoringSSL, Go, and suspicious labelled baselines are collected with provenance.

The Attribution Grid panel displays a bundled paired benchmark from `data/attribution_confound_grid.json`, `data/null_calibration.json`, and `data/replication_audit.json`, highlighting which fingerprint profiles survive bit-length control, which ones are likely range confounds, whether the strongest controlled profiles survive random-label null simulation after family-wise profile selection, and whether those profiles replicate across settings.

The Baseline Lab panel reads `data/baselines/real_world/manifest.json`, `data/collection_matrix.json`, `data/collection_power.json`, `data/provenance_requirements.json`, `data/provenance_audit.json`, `data/baseline_acceptance.json`, `data/baseline_promotion_plan.json`, `data/collection_handoff.json`, `data/collection_submission_contract.json`, `data/collection_submission_lint.json`, `data/collection_fixture_audit.json`, and `data/collection_intake.json` to show which real-world baseline families are registered, whether targets are only coarse screening or strong enough for tighter claims, which baselines still block publication, which public-safe collection tasks should be executed first, what collectors must submit, what pre-intake lint would reject, whether lint behavior is covered by pass/warn/block fixtures, and whether submitted aggregate artifacts are acceptable without feature-vector contract failures, identity mismatches, non-public feature-vector paths, duplicate submission collisions, or reused aggregate checksums.

The Research Readiness panel reads `data/research_readiness.json` and surfaces blocking gaps before any real-world attribution claim is treated as strong.

The Evidence Pack panel reads `data/evidence_pack.json`, `data/claim_language_audit.json`, `data/claim_ledger.json`, `data/artifact_lineage.json`, `data/decision_protocol.json`, `data/falsification_battery.json`, and `data/publication_consistency.json` to show checksums, semantic publication gates, the maximum safe claim level, which public claims are currently allowed or blocked, whether public wording stays inside the evidence boundary, whether the public artifact dependency graph is acyclic and checksum-consistent, which claim-promotion decisions are pre-registered as allowed or blocked, which falsification checks prevent overclaiming, and whether all public governance artifacts agree on the same high-risk claim boundary. The fixture-audit gate now checks `quality_gate.status`, fixture count, public-safety count, and failed expectation count instead of only checking that the file exists.

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
python -m prime_audit.cli provenance-audit --requirements data/provenance_requirements.json --output data/provenance_audit.json
python -m prime_audit.cli baseline-acceptance --manifest data/baselines/real_world/manifest.json --matrix data/collection_matrix.json --power data/collection_power.json --provenance-audit data/provenance_audit.json --output data/baseline_acceptance.json
python -m prime_audit.cli baseline-promotion-plan --acceptance data/baseline_acceptance.json --power data/collection_power.json --output data/baseline_promotion_plan.json
python -m prime_audit.cli synthetic-feature-vectors --limit 200000 --samples-per-label 4 --record-count 80 --seed 20260523 --gap-max-steps 1024 --output data/feature_vectors.json
python -m prime_audit.cli export-feature-vectors --fingerprints openssl=data/openssl_fingerprint.json suspicious=data/suspicious_fingerprint.json --claim-scope real_world --output data/feature_vectors.json
python -m prime_audit.cli crypto-classifier --features data/feature_vectors.json --feature-space interaction --output data/crypto_classifier_report.json
python -m prime_audit.cli collection-handoff --manifest data/baselines/real_world/manifest.json --matrix data/collection_matrix.json --power data/collection_power.json --provenance-requirements data/provenance_requirements.json --provenance-audit data/provenance_audit.json --baseline-acceptance data/baseline_acceptance.json --promotion-plan data/baseline_promotion_plan.json --classifier-report data/crypto_classifier_report.json --output data/collection_handoff.json
python -m prime_audit.cli collection-submission-contract --handoff data/collection_handoff.json --output data/collection_submission_contract.json
python -m prime_audit.cli collection-submission-lint --contract data/collection_submission_contract.json --output data/collection_submission_lint.json
python -m prime_audit.cli collection-fixture-audit --contract data/collection_submission_contract.json --output data/collection_fixture_audit.json
python -m prime_audit.cli collection-intake --handoff data/collection_handoff.json --output data/collection_intake.json
python -m prime_audit.cli claim-language-audit --generated-at 2026-05-24T16:56:40+00:00 --output data/claim_language_audit.json
python -m prime_audit.cli research-readiness --manifest data/baselines/real_world/manifest.json --attribution-grid data/attribution_confound_grid.json --classifier-report data/crypto_classifier_report.json --output data/research_readiness.json
python -m prime_audit.cli evidence-pack --manifest data/baselines/real_world/manifest.json --readiness data/research_readiness.json --attribution-grid data/attribution_confound_grid.json --baseline-acceptance data/baseline_acceptance.json --collection-intake data/collection_intake.json --classifier-report data/crypto_classifier_report.json --artifact project_evolution=data/project_evolution.json snapshot_manifest=data/snapshots/manifest.json collection_matrix=data/collection_matrix.json collection_power=data/collection_power.json provenance_requirements=data/provenance_requirements.json provenance_audit=data/provenance_audit.json baseline_promotion_plan=data/baseline_promotion_plan.json collection_handoff=data/collection_handoff.json collection_submission_contract=data/collection_submission_contract.json collection_submission_lint=data/collection_submission_lint.json collection_fixture_audit=data/collection_fixture_audit.json claim_language_audit=data/claim_language_audit.json null_calibration=data/null_calibration.json replication_audit=data/replication_audit.json feature_vectors=data/feature_vectors.json --generated-at 2026-05-24T16:56:40+00:00 --output data/evidence_pack.json
python -m prime_audit.cli claim-ledger --evidence-pack data/evidence_pack.json --generated-at 2026-05-24T16:56:40+00:00 --output data/claim_ledger.json
python -m prime_audit.cli artifact-lineage --generated-at 2026-05-24T16:56:40+00:00 --output data/artifact_lineage.json
python -m prime_audit.cli decision-protocol --evidence-pack data/evidence_pack.json --claim-ledger data/claim_ledger.json --artifact-lineage data/artifact_lineage.json --generated-at 2026-05-24T16:56:40+00:00 --output data/decision_protocol.json
python -m prime_audit.cli falsification-battery --attribution-grid data/attribution_confound_grid.json --decision-protocol data/decision_protocol.json --generated-at 2026-05-24T16:56:40+00:00 --output data/falsification_battery.json
python -m prime_audit.cli publication-consistency --evidence-pack data/evidence_pack.json --claim-ledger data/claim_ledger.json --decision-protocol data/decision_protocol.json --falsification-battery data/falsification_battery.json --generated-at 2026-05-24T16:56:40+00:00 --output data/publication_consistency.json
python -m prime_audit.cli null-calibration --attribution-grid data/attribution_confound_grid.json --iterations 5000 --output data/null_calibration.json
python -m prime_audit.cli replication-audit --attribution-grid data/attribution_confound_grid.json --null-calibration data/null_calibration.json --output data/replication_audit.json
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

To audit the current publication bundle without overwriting files, run:

```bash
python scripts/reproduce_publication.py
```

The script starts by regenerating `data/claim_language_audit.json` in a temporary directory and compares it with the public artifact, so stale public wording checks cannot pass unnoticed. Add `--report publication_reproduction_report.json` to save the compared canonical JSON hashes, raw file hashes, and command trace with temporary output paths normalized to `{tmp}`. Local reproduction reports matching `publication_reproduction_report*.json` are ignored by git so audit scratch output does not enter the public evidence bundle by accident.

To verify the GitHub Pages surface, run:

```bash
node scripts/verify_pages.cjs
```

The verifier serves the repository over local HTTP, so it exercises the same `data/*.json` fetch path used by GitHub Pages instead of the `file://` fallback constants.

To verify the open-problem bounded certificates, run:

```bash
python scripts/verify_open_problem_workbench.py
```

The bundled Codex runtime Python can also run the same commands.

## Continuous Verification

GitHub Actions now runs the publication guard on pushes and pull requests to `main`: Python compile checks, publication-critical unit checks, publication artifact reproduction, JavaScript syntax checks, Playwright-based GitHub Pages verification, and a final committed-artifact drift check. This keeps the public research bundle from silently diverging from the audited evidence files. Run `python -m unittest discover -s tests -p "test_*.py"` locally for the full suite.

## Boundary

This project is for defensive quality auditing and controlled experiments. It does not scan external targets, and recovered factors are omitted from reports unless `--include-sensitive-evidence` is explicitly used for owned test data.

## License

Apache License 2.0. See [LICENSE](LICENSE).
