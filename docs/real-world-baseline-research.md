# Real-World Baseline Research Track

작성일: 2026-05-22

## 목적

PrimeProject의 다음 단계는 합성 생성기 실험을 넘어서, 실제 암호 라이브러리와 wallet/library가 만든 수학적 객체에서 생성기 흔적을 찾는 것이다. 이 트랙은 OpenSSL, BoringSSL, Go, Bitcoin Core, wallet 샘플을 같은 manifest와 feature vector schema로 정리해 의심 데이터셋과 비교할 수 있게 만든다.

## 구현된 구조

```text
owned or public sample
  -> fingerprint-primes / bitcoin-signature-audit
  -> build-baseline or bitcoin-risk-report
  -> real-baseline-manifest
  -> export-feature-vectors
  -> collection-submission-contract
  -> collection-submission-lint
  -> collection-fixture-audit
  -> collection-intake
  -> crypto-classifier
```

## Manifest

`real-baseline-manifest`는 baseline 자체와 민감 데이터 처리를 분리한다. GitHub에 올리는 것은 private prime, wallet seed, private key가 아니라 aggregate fingerprint와 등록 정보다.

```powershell
python -m prime_audit.cli real-baseline-manifest `
  --output data/baselines/real_world/manifest.json
```

기본 registry에는 다음 기준군이 포함된다.

- OpenSSL RSA prime owned sample: planned, sensitive.
- BoringSSL RSA prime owned sample: planned, sensitive.
- Go crypto/rsa prime owned sample: planned, sensitive.
- Bitcoin Core / secp256k1 ECDSA signature metadata: planned.
- Bitcoin secp256k1 public constants: available.

## Feature Vector Export

`export-feature-vectors`는 fingerprint/baseline JSON을 classifier가 읽을 수 있는 고정 길이 벡터로 변환한다.

```powershell
python -m prime_audit.cli synthetic-feature-vectors `
  --limit 200000 `
  --samples-per-label 4 `
  --record-count 80 `
  --seed 20260523 `
  --gap-max-steps 1024 `
  --output data/feature_vectors.json

python -m prime_audit.cli export-feature-vectors `
  --fingerprints openssl=data/openssl_fingerprint.json suspicious=data/suspicious_fingerprint.json `
  --baselines go=data/baselines/go_owned.json `
  --claim-scope real_world `
  --output data/feature_vectors.json
```

현재 feature는 bit-length distribution moments, residue TV drift, low16 collision, next-prime exposure, local gap statistics를 포함한다.

현재 공개 번들에는 실세계 baseline이 아직 없으므로 `synthetic-feature-vectors`로 만든 12개 controlled synthetic vector가 들어 있다. 이 산출물의 `claim_scope`는 `controlled_synthetic_only`이며, classifier 파이프라인과 GitHub Pages 시각화를 검증하기 위한 기준군이다.

## Crypto-Classifier v1

`crypto-classifier`는 XGBoost나 Random Forest를 바로 넣기 전의 dependency-free baseline이다. nearest-centroid 모델에 interaction feature를 추가해서 다변량 교차 편향이 실제로 남는지 빠르게 검증한다.

```powershell
python -m prime_audit.cli crypto-classifier `
  --features data/feature_vectors.json `
  --feature-space interaction `
  --output data/crypto_classifier_report.json
```

이 모델은 최종 분류기가 아니라 연구 안전장치다. 여기서도 분리되지 않는 신호는 무거운 ML을 넣어도 과장될 가능성이 높다.

현재 번들 결과는 3개 label(`next_prime`, `rejection`, `wheel30_next`)과 12개 vector에서 leave-one-out 정확도 33.3%다. 이 수치는 실세계 분류 성능 주장이 아니라, fixed vector schema, interaction feature path, classifier gate가 end-to-end로 연결됐는지 확인하는 negative/controlled baseline이다. 따라서 `research-readiness`는 classifier 차원을 `scaffold_ready`로 두고 `real_world_claim_ready=false`를 유지한다.

## Collection Matrix

`collection-matrix`는 manifest에 등록된 baseline을 실제 수집 목표로 확장한다. 목적은 “어떤 라이브러리를 모을 것인가”가 아니라, claim을 강하게 만들기 전에 필요한 bit-length, sample count, public output 단위를 명시하는 것이다.

```powershell
python -m prime_audit.cli collection-matrix `
  --manifest data/baselines/real_world/manifest.json `
  --output data/collection_matrix.json
```

현재 matrix는 다음 target을 요구한다.

- OpenSSL RSA prime: 2048/3072/4096-bit 각각 500개 이상의 aggregate sample.
- BoringSSL RSA prime: 2048/3072/4096-bit 각각 500개 이상의 aggregate sample.
- Go crypto/rsa prime: 2048/3072/4096-bit 각각 500개 이상의 aggregate sample.
- Bitcoin Core / wallet signature metadata: 256-bit ECDSA signature metadata 10,000개 이상.

private prime, private key, seed, wallet material은 공개 산출물이 아니다. 공개 단위는 aggregate fingerprint, baseline JSON, feature vector, nonce-risk summary로 제한한다. `claim_gate.status`가 `blocked`이면 GitHub Pages는 이를 Baseline Lab과 Evidence Pack에서 그대로 보여준다.

## Collection Power

`collection-power`는 collection target을 통계적 screening floor로 바꾼다. 이 단계의 목적은 표본 수를 과장하지 않는 것이다. 예를 들어 RSA prime 500개/bit-length는 빠른 screening에는 유용하지만, mod 210 residue TV drift 10% 수준의 보수적 claim에는 부족하다고 표시된다.

```powershell
python -m prime_audit.cli collection-power `
  --matrix data/collection_matrix.json `
  --output data/collection_power.json
```

현재 기본 해석은 다음과 같다.

- RSA 2048/3072/4096-bit 500개 target: `coarse`, 약 30% 수준의 보수적 TV floor.
- 10% TV drift claim을 보수적으로 다루려면 각 library/bit-length 조합당 약 4,514개 target이 필요.
- Bitcoin signature metadata 10,000개 target: `strong`, 64-bucket nonce fingerprint 기준 약 7.8% TV floor.

`--alpha`는 임의의 유의수준을 받을 수 있으며, 계산은 Python 표준 라이브러리의 정규분포 역누적값을 사용한다. 예를 들어 `--alpha 0.001`처럼 더 엄격한 계획을 쓰면 RSA mod 210의 10% TV floor가 4,514개에서 12,723개로 증가한다. `interval_label`, `class_shift_interval`, `conservative_tv_floor_interval`은 설정된 alpha의 신뢰수준을 따르고, 하위 호환 필드인 `class_shift_95`, `conservative_tv_floor_95`는 항상 실제 95% 기준으로 유지된다. `--target-tv`도 일반화되어 `target_tv_label`, `min_samples_for_target_tv`, `sample_gap_to_target_tv`로 기록된다. 예를 들어 5% TV floor는 같은 조건에서 18,055개가 필요하다. 하위 호환 필드인 `min_samples_for_10pct_tv`는 항상 실제 10% TV 기준으로 유지되므로, 설정된 target TV와 10% 기준을 혼동하지 않는다.

또한 `sensitivity.rows`는 object type별 bucket count에 대해 alpha `[0.10, 0.05, 0.01, 0.001]`와 target TV `[20%, 10%, 5%]` 조합의 sample floor를 함께 기록한다. 이 grid는 "4514개면 충분하다" 같은 단일 숫자 주장을 피하고, 500개 RSA sample이 어떤 claim 강도까지 가능한지 GitHub Pages에서 바로 비교하게 한다. 유효하지 않은 alpha나 target TV는 조용히 기본값으로 대체하지 않고 실패시킨다.

이 값은 attribution 증명이 아니라 수집 계획의 품질 경계다. GitHub Pages는 이 결과를 Baseline Lab에 표시해서 500개 RSA sample을 강한 실세계 claim으로 오해하지 않게 한다.

## Provenance Requirements

`provenance-requirements`는 실세계 baseline이 들어오기 전 반드시 채워야 할 재현성 metadata를 정의한다. 이 단계가 없으면 같은 라이브러리 이름을 쓰더라도 version, source commit, build flag, RNG source, generation command 차이 때문에 fingerprint 비교가 학술적으로 무의미해질 수 있다.

```powershell
python -m prime_audit.cli provenance-requirements `
  --manifest data/baselines/real_world/manifest.json `
  --output data/provenance_requirements.json
```

필수 항목은 `baseline_id`, `library_version`, `bit_length`, `sample_count`, `collector`, `host_platform`, `source_commit`, `build_config`, `rng_source`, `generation_command`, `raw_material_policy`, `aggregate_artifact_sha256` 등을 포함한다. 공개 금지 항목은 `private_key`, `private_prime`, `wallet_seed`, `raw_signature_owner`다.

GitHub Pages의 Provenance Gate는 현재 missing field 수를 보여준다. Evidence Pack은 `provenance_requirements` artifact가 checksummed bundle에 없으면 medium severity gate를 실패시킨다.

## Provenance Audit

`provenance-audit`는 요구사항 문서를 실제 baseline provenance record에 적용한다. 누락 metadata, 잘못된 aggregate SHA-256 형식, 공개 산출물에 들어가면 안 되는 민감 필드명을 탐지한다. 민감 값 자체는 출력하지 않고 field path만 기록한다.

```powershell
python -m prime_audit.cli provenance-audit `
  --requirements data/provenance_requirements.json `
  --output data/provenance_audit.json
```

실제 수집 record가 있을 때는 `--records records.json`을 추가한다. 현재 public demo는 아직 실세계 record가 없으므로 4개 non-standard baseline row가 모두 `blocked`다. 이 blocked 상태는 의도적인 claim gate이며, 향후 OpenSSL/BoringSSL/Go/Bitcoin baseline이 채워질 때 public-safe 여부를 자동으로 검증하는 계약 역할을 한다.

## Baseline Acceptance

`baseline-acceptance`는 실세계 baseline을 실제 attribution 기준군으로 승격할 수 있는지 최종 판정한다. 입력은 manifest, collection matrix, collection power, provenance audit이다.

```powershell
python -m prime_audit.cli baseline-acceptance `
  --manifest data/baselines/real_world/manifest.json `
  --matrix data/collection_matrix.json `
  --power data/collection_power.json `
  --provenance-audit data/provenance_audit.json `
  --output data/baseline_acceptance.json
```

판정은 세 단계다.

- `blocked`: manifest target이 아직 available이 아니거나 provenance가 통과하지 못한 상태.
- `screening_only`: availability와 provenance는 통과했지만 sample power가 coarse라 강한 attribution claim에는 부족한 상태.
- `accepted`: availability, provenance, public-safety, sample-power tier가 모두 통과한 상태.

현재 public demo는 10개 target 모두 `blocked`다. 특히 RSA 500 sample 계획은 coarse screening으로만 취급되며, 10% TV drift를 보수적으로 주장하려면 bit length/library 조합당 약 4514개 sample 수준이 필요하다는 경계를 유지한다.

## Baseline Promotion Plan

`baseline-promotion-plan`은 blocked 상태에서 accepted evidence로 가는 최단 경로를 계산한다. 현재 계획에서는 OpenSSL 2048-bit와 BoringSSL 2048-bit를 우선 unlock target으로 잡고, 두 library를 10% TV floor 기준으로 승격하려면 총 9028개 aggregate RSA prime sample이 필요하다고 표시한다.

```powershell
python -m prime_audit.cli baseline-promotion-plan `
  --acceptance data/baseline_acceptance.json `
  --power data/collection_power.json `
  --output data/baseline_promotion_plan.json
```

이 산출물은 실제 수집 작업의 우선순위표다. 현재처럼 aggregate artifact 자체가 없을 때는 `collect_aggregate_baseline`이 먼저 나오고, artifact와 checksum이 생긴 뒤 `complete_provenance_record`가 다음 단계가 된다. raw private material은 local에 유지하며, 공개 artifact는 aggregate fingerprint와 checksum만 포함해야 한다. GitHub Pages의 Promotion Plan은 이 minimal unlock path를 그대로 표시한다.

## Collection Handoff

`collection-handoff`는 promotion plan을 실제 수집 실행 패킷으로 바꾼다. 목적은 “OpenSSL/BoringSSL을 모으자”가 아니라, 어떤 task가 P0인지, 몇 개 sample이 필요한지, 어떤 provenance field가 막고 있는지, 무엇을 절대 공개하면 안 되는지까지 public-safe JSON으로 고정하는 것이다.

```powershell
python -m prime_audit.cli collection-handoff `
  --manifest data/baselines/real_world/manifest.json `
  --matrix data/collection_matrix.json `
  --power data/collection_power.json `
  --provenance-requirements data/provenance_requirements.json `
  --provenance-audit data/provenance_audit.json `
  --baseline-acceptance data/baseline_acceptance.json `
  --promotion-plan data/baseline_promotion_plan.json `
  --classifier-report data/crypto_classifier_report.json `
  --output data/collection_handoff.json
```

현재 handoff는 10개 collection task를 만들고, P0는 OpenSSL 2048-bit와 BoringSSL 2048-bit 두 개다. 두 P0 target은 10% TV floor 기준 총 9028개 sample이 필요하며, 공개 계약은 `aggregate fingerprint JSON`, `baseline JSON`, `feature vector JSON`, `provenance record JSON`, `SHA-256 checksum`으로 제한한다. `private_key`, `private_prime`, `wallet_seed`, raw key file은 공개 금지 필드로 남는다.

## Collection Submission Contract

`collection-submission-contract`는 handoff를 실제 제출자가 따라야 할 machine-readable 계약으로 변환한다. handoff가 “무엇을 수집할지”를 정의한다면, submission contract는 “어떤 JSON record가 intake를 통과할 수 있는지”를 미리 고정한다.

```powershell
python -m prime_audit.cli collection-submission-contract `
  --handoff data/collection_handoff.json `
  --output data/collection_submission_contract.json
```

현재 계약은 10개 task template을 만들고, 각 제출 record에 `task_id`, `sample_count`, `claim_scope`, `aggregate_artifact_sha256`, `provenance_record`, `feature_vector_path`, `feature_vector_summary` 7개 필드를 요구한다. `feature_vector_summary`는 `generator-feature-vector.v1` schema, 14개 scalar feature, `record_count == sample_count`, task bit length와 맞는 `bit_length_mean`, finite numeric value 조건을 만족해야 한다.

이 단계의 실용적 가치는 두 가지다. 첫째, OpenSSL/BoringSSL/Go/wallet 수집자가 private material을 공개하지 않고도 재현 가능한 aggregate artifact를 제출할 수 있는 템플릿을 제공한다. 둘째, intake 전에 checksum 재사용, feature-vector 누락, claim scope 오류, forbidden field 노출 같은 실패 조건을 공개 산출물로 고정해 “나중에 결과를 보고 기준을 바꾸는” 위험을 줄인다. GitHub Pages의 Baseline Lab은 이 계약을 Submission Contract 블록으로 표시하고, Evidence Pack은 `collection_submission_contract_gate`로 체크섬 포함 여부를 검사한다.

## Collection Submission Lint

`collection-submission-lint`는 제출 후보 record를 intake에 넣기 전에 계약 위반을 미리 찾는 로컬/공개-safe 검증 단계다. intake는 claim gate 판정에 가깝고, lint는 collector 피드백 도구다.

```powershell
python -m prime_audit.cli collection-submission-lint `
  --contract data/collection_submission_contract.json `
  --records records/submission_candidates.json `
  --output data/collection_submission_lint.json
```

검사 항목은 known task ID, 필수 record field, `real_world` claim scope, planned sample floor, 10% TV screening floor warning, SHA-256 checksum 형식과 task 간 재사용, provenance record, feature vector schema/feature/record_count/bit_length 정합성, 중복 제출, forbidden public field scan이다. 현재 공개 번들은 제출 후보가 없으므로 `waiting` 상태이며, 10개 task가 `awaiting_submission`으로 표시된다. 실제 수집자가 record를 넣으면 이 단계에서 `blocked`, `warning`, `pass`를 먼저 확인한 뒤 `collection-intake`로 넘길 수 있다.

## Collection Fixture Audit

`collection-fixture-audit`는 실제 collector 제출 전에 lint가 의도대로 작동하는지 검증하는 public-safe regression suite다. 정상 제출, 10% TV floor 미달 경고, feature-vector 누락, forbidden field 노출, aggregate checksum 재사용 사례를 synthetic fixture로 만들고, 각 fixture의 expected status와 실제 lint status를 비교한다.

```powershell
python -m prime_audit.cli collection-fixture-audit `
  --contract data/collection_submission_contract.json `
  --output data/collection_fixture_audit.json
```

현재 bundled fixture audit은 6개 fixture 모두 expectation을 만족한다. 이 산출물의 의미는 “실제 OpenSSL/BoringSSL 데이터가 수집됐다”가 아니라, 실제 데이터가 들어오기 전에 제출 계약과 lint의 실패/경고 경계가 재현 가능하게 고정됐다는 것이다. GitHub Pages의 Baseline Lab은 Fixture Audit 블록으로 이 결과를 보여주고, Evidence Pack은 `collection_fixture_audit_gate`로 해당 검증 산출물이 포함됐는지뿐 아니라 `quality_gate.status == pass`, 실패 fixture 0개, public-safe fixture 수 일치까지 확인한다.

## Collection Intake

`collection-intake`는 handoff 이후 실제 aggregate artifact가 제출됐을 때 통과 여부를 판정한다. 이 단계는 "데이터가 있다"를 곧바로 "real-world baseline이 생겼다"로 승격하지 않는다. 각 제출물은 handoff task와 매칭되어야 하고, sample floor, SHA-256 checksum, provenance record, feature vector path, `real_world` claim scope, forbidden public field scan을 모두 지나야 한다.

```powershell
python -m prime_audit.cli collection-intake `
  --handoff data/collection_handoff.json `
  --output data/collection_intake.json
```

현재 공개 번들은 raw 실세계 제출물이 없으므로 `0 submitted / 0 accepted / 10 blocked` 상태다. 특히 OpenSSL 2048-bit와 BoringSSL 2048-bit P0 task 두 개가 아직 막혀 있으며, 10% TV floor 기준으로 총 9028개 aggregate sample이 남아 있다. 이 게이트가 중요한 이유는 실세계 수집 이후에도 private prime, wallet seed, raw key file 같은 민감 필드가 공개 artifact에 섞이는 것을 자동으로 차단하고, feature vector가 없는 artifact가 classifier claim으로 넘어가는 것을 막기 때문이다. 이제 제출 record는 `feature_vector_path`뿐 아니라 공개 가능한 `feature_vector_summary` 계약도 포함해야 하며, intake는 schema, 14개 scalar feature, numeric 값, sample count, bit-length 정합성을 검사한다. 또한 동일 task_id로 제출된 중복 intake record와 서로 다른 기준군이 같은 aggregate checksum을 공유하는 artifact 재사용을 차단해, 제출 충돌이나 데이터셋 재포장으로 baseline claim이 오염되는 경로를 막는다. Evidence Pack은 이 결과를 `collection_intake_gate`로 다시 평가하므로, intake가 blocked인 동안 real-world generator attribution 승격도 자동으로 blocked 상태를 유지한다.

## Research Readiness

`research-readiness`는 현재 연구 도구가 실세계 attribution 주장에 얼마나 가까운지 점수화한다. 입력은 real-world baseline manifest, attribution grid, classifier report, Bitcoin risk report다.

```powershell
python -m prime_audit.cli research-readiness `
  --manifest data/baselines/real_world/manifest.json `
  --attribution-grid data/attribution_confound_grid.json `
  --classifier-report data/crypto_classifier_report.json `
  --bitcoin-risk-report data/bitcoin_generator_risk_report.json `
  --output data/research_readiness.json
```

GitHub Pages의 Research Readiness 패널은 이 JSON을 읽어 다음 네 차원을 표시한다.

- `sim_to_real`: OpenSSL, BoringSSL, Go, Bitcoin/wallet baseline 등록 및 공개 가능성.
- `attribution_validation`: bit-length control 후에도 남는 fingerprint profile.
- `classifier`: labelled feature vector 수, label 수, leave-one-out 분류 결과.
- `bitcoin_integration`: nonce fingerprint와 Bitcoin baseline 연결 상태.

중요한 원칙은 “좋은 점수”보다 “blocking gap”이다. 현재처럼 real-world available baseline이 부족하거나 classifier label이 없으면, 페이지는 이를 명시적으로 high-priority gap으로 남긴다. 특히 `sim_to_real`은 coverage와 collection plan이 충분해 보여도 available aggregate generator baseline이 2개 미만이면 `scaffold_ready`로 상한 처리한다. Bitcoin secp256k1 공개 상수처럼 유용한 public control은 `public_control_count`로 따로 세며, 실세계 attribution에 쓸 수 있는 available baseline으로 계산하지 않는다.

## Null Calibration

`null-calibration`은 controlled attribution profile이 무작위 label 환경에서도 나올 수 있는지 확인한다. 기존 binomial p-value는 profile별로 유용하지만, 여러 feature profile을 본 뒤 가장 좋아 보이는 profile을 고르는 선택 효과를 충분히 반영하지 못한다. 이 모듈은 각 controlled row의 total 구조를 유지하고 random baseline 확률로 correct count를 시뮬레이션한 뒤, 매 iteration마다 profile lift의 최대값을 저장해 family-wise p-value를 계산한다.

```powershell
python -m prime_audit.cli null-calibration `
  --attribution-grid data/attribution_confound_grid.json `
  --iterations 5000 `
  --output data/null_calibration.json
```

현재 결과는 `gap_only`와 `all`이 family-wise null에서도 살아남고, `bit_length_only`, `low_bits_only`, `residue_only`는 near-null로 남는다. 이는 합성 generator fingerprint 신호가 단순 random fluctuation보다 강하다는 근거를 보강하지만, claim floor는 여전히 `controlled_synthetic_only`다. 실세계 OpenSSL/BoringSSL/Go/Bitcoin attribution은 별도 baseline, provenance, classifier evidence가 생기기 전까지 차단된다.

## Replication Audit

`replication-audit`은 null calibration을 통과한 profile이 특정 설정 하나에만 기대는지 확인한다. 같은 attribution grid를 limit, train-count, test-count 설정별로 다시 묶고, 각 설정에서 controlled accuracy lift가 random baseline보다 충분히 높은지 검사한다.

```powershell
python -m prime_audit.cli replication-audit `
  --attribution-grid data/attribution_confound_grid.json `
  --null-calibration data/null_calibration.json `
  --output data/replication_audit.json
```

현재 결과는 `gap_only`와 `all`이 8개 설정 모두에서 replicated 상태이며 null calibration도 통과한다. 반대로 `bit_length_only`, `low_bits_only`, `residue_only`는 0/8 설정에서 replicated로 남아 negative control 역할을 유지한다. 이 단계는 합성 실험 claim을 조금 더 강하게 만들지만, 역시 실세계 attribution claim을 열지는 않는다.

## Evidence Pack

`evidence-pack`은 공개 산출물의 재현성과 주장 한계를 묶는 최종 출판 단위다. 입력 JSON의 SHA-256, schema, byte size를 기록하고 publication gate를 통과했는지 표시한다.

```powershell
python -m prime_audit.cli evidence-pack `
  --manifest data/baselines/real_world/manifest.json `
  --readiness data/research_readiness.json `
  --attribution-grid data/attribution_confound_grid.json `
  --baseline-acceptance data/baseline_acceptance.json `
  --collection-intake data/collection_intake.json `
  --artifact project_evolution=data/project_evolution.json snapshot_manifest=data/snapshots/manifest.json collection_matrix=data/collection_matrix.json collection_power=data/collection_power.json provenance_requirements=data/provenance_requirements.json provenance_audit=data/provenance_audit.json baseline_promotion_plan=data/baseline_promotion_plan.json collection_handoff=data/collection_handoff.json collection_submission_contract=data/collection_submission_contract.json collection_submission_lint=data/collection_submission_lint.json collection_fixture_audit=data/collection_fixture_audit.json null_calibration=data/null_calibration.json replication_audit=data/replication_audit.json feature_vectors=data/feature_vectors.json `
  --classifier-report data/crypto_classifier_report.json `
  --generated-at 2026-05-24T16:56:40+00:00 `
  --output data/evidence_pack.json
```

현재 claim level은 `public_demo_only`로 남는다. 이는 실패가 아니라 의도적인 안전장치다. OpenSSL/BoringSSL/Go aggregate baseline과 labelled feature vector가 생기기 전에는 “실세계 생성기 attribution을 증명했다”고 말하지 않도록 막는다.

## Claim Ledger

`claim-ledger`는 Evidence Pack을 입력으로 받아 공개 문장 단위의 주장 허용 상태를 계산한다. 목적은 “프로젝트가 무엇을 할 수 있는가”를 홍보 문장으로 쓰기 전에, 각 문장이 어떤 gate와 artifact에 의해 허용되는지 확인하는 것이다.

```powershell
python -m prime_audit.cli claim-ledger `
  --evidence-pack data/evidence_pack.json `
  --generated-at 2026-05-24T16:56:40+00:00 `
  --output data/claim_ledger.json
```

현재 ledger는 5개 claim을 추적한다. Prime-measure visualization, synthetic generator attribution, public-safety/reproducibility claim은 허용되지만, real-world generator attribution과 Bitcoin nonce-risk attribution은 차단된다. 차단 이유는 real baseline, classifier, baseline acceptance, Bitcoin risk report가 아직 충분하지 않기 때문이다.

Claim Ledger는 Evidence Pack에서 파생되지만 Evidence Pack 내부 체크섬 목록에는 넣지 않는다. 같은 pack에 ledger checksum을 넣으면 evidence pack -> ledger -> evidence pack의 순환 산출물이 되기 때문이다. 대신 GitHub Pages의 Evidence 패널에서 Evidence Pack 옆에 별도 publication ledger로 표시한다.

## Artifact Lineage

`artifact-lineage`는 공개 JSON 산출물의 dependency DAG를 만들고, Evidence Pack에 기록된 artifact checksum이 현재 파일과 일치하는지 다시 확인한다. 이 단계는 논문식 재현성 표에 가깝다. 어떤 산출물이 어떤 입력에서 파생됐는지 보이고, missing artifact, checksum mismatch, invalid edge, cycle을 별도 finding으로 만든다.

```powershell
python -m prime_audit.cli artifact-lineage `
  --generated-at 2026-05-24T16:56:40+00:00 `
  --output data/artifact_lineage.json
```

현재 lineage는 22개 artifact node와 52개 dependency edge를 추적한다. `feature_vectors`와 `classifier_report`는 `readiness`와 `evidence_pack`의 입력으로 연결되고, `collection_handoff`는 manifest, collection matrix/power, provenance, acceptance, promotion, classifier scope를 묶는 sim-to-real 실행 산출물로 연결된다. `collection_fixture_audit`는 submission contract와 lint 사이의 pass/warn/block 경계를 고정하고, `collection_intake`는 그 handoff task에 실제 제출 aggregate artifact가 맞는지 검증한 뒤 `readiness`와 `evidence_pack`으로 이어지는 안전 게이트다. `evidence_pack`은 checksummed bundle의 중심이고, `claim_ledger`와 `artifact_lineage`는 그 이후에 생성되는 post-pack audit 산출물이다. 따라서 lineage 자체는 Evidence Pack checksum 목록에 넣지 않는다. 이 순서를 지켜야 evidence_pack -> claim_ledger/artifact_lineage -> evidence_pack 형태의 순환 재현성 문제가 생기지 않는다.

## Decision Protocol

`decision-protocol`은 Evidence Pack, Claim Ledger, Artifact Lineage를 입력으로 받아 claim promotion 여부를 사전 등록된 규칙으로 판정한다. 목적은 결과를 본 뒤 claim 기준을 바꾸는 것을 막는 것이다.

```powershell
python -m prime_audit.cli decision-protocol `
  --evidence-pack data/evidence_pack.json `
  --claim-ledger data/claim_ledger.json `
  --artifact-lineage data/artifact_lineage.json `
  --generated-at 2026-05-24T16:56:40+00:00 `
  --output data/decision_protocol.json
```

현재 protocol은 4개 결정을 고정한다. public demo와 controlled synthetic signal report는 허용된다. real-world generator attribution과 Bitcoin nonce-risk attribution promotion은 차단된다. 차단 이유는 각각 accepted real-world baselines/classifier/baseline acceptance, Bitcoin nonce-risk report가 아직 없기 때문이다.

## Falsification Battery

`falsification-battery`는 attribution 결과를 claim으로 승격하기 전에 반증 조건을 먼저 실행한다. 목적은 “맞혔다”는 지표를 늘리는 것이 아니라, 어떤 조건에서 주장을 내려야 하는지 자동으로 남기는 것이다.

```powershell
python -m prime_audit.cli falsification-battery `
  --attribution-grid data/attribution_confound_grid.json `
  --decision-protocol data/decision_protocol.json `
  --generated-at 2026-05-24T16:56:40+00:00 `
  --output data/falsification_battery.json
```

현재 배터리는 5개 체크를 실행한다.

- `paired_control_presence`: uncontrolled run과 bit-length-controlled run이 모두 있는지 확인한다.
- `controlled_signal_above_random`: bit-length control 후에도 `all`, `gap_only` 같은 비자명 profile이 random baseline을 넘는지 확인한다.
- `bit_length_confound_guard`: `bit_length_only` profile이 control 후 random floor 근처로 무력화되는지 확인한다.
- `negative_control_floor`: low-bit/residue-only profile이 비정상적으로 높은 정확도를 보이지 않는지 확인한다.
- `claim_promotion_guard`: real-world attribution과 Bitcoin nonce-risk attribution promotion이 필요한 evidence 없이 열리지 않는지 확인한다.

현재 결과는 `5 pass / 0 fail`이지만 claim floor는 `controlled_synthetic_only`다. 이는 실세계 OpenSSL/BoringSSL/Go/Bitcoin attribution을 증명했다는 뜻이 아니라, 합성 생성기 조건에서 남는 신호를 보고해도 되는 최소 안전 조건이 갖춰졌다는 뜻이다. GitHub Pages의 Evidence Pack 패널은 이 결과를 Decision Protocol 아래에 표시한다.

## Project Evolution View

GitHub Pages의 Project Evolution 패널은 `data/project_evolution.json`을 읽어 지금까지의 변화 자체를 연구 산출물로 시각화하되, 중복 나열을 줄이고 의사결정에 필요한 근거만 남긴다.

- 연구 단계: regularity plan -> Conjecture Lab -> snapshots -> fingerprint baseline -> attribution grid -> null calibration -> replication audit -> crypto-classifier -> real-world registry -> collection matrix -> collection power -> provenance gate -> provenance audit -> baseline acceptance -> promotion plan -> collection handoff -> submission contract -> submission lint -> fixture audit -> collection intake -> readiness -> evidence pack -> claim ledger -> artifact lineage -> decision protocol -> falsification battery.
- 현황 지표: scale, controlled signal, attribution-ready generator baseline, public control, collection intake, checksummed evidence, claim level만 상단에 남겨 현재 판단에 직접 필요한 수치로 제한한다.
- Visual Change Trail: prime regularity demo, 10M scale lift, controlled attribution, sim-to-real gates, publication guardrails만 release-style milestone로 보여준다.
- Evidence Spine: Scale, Signal, Sim-to-Real, Governance, Publication 축으로 기존 산출물을 한 번만 재배치한다. 각 축은 점수, 상태, artifact 개수와 짧은 artifact 이름, gate 문장, 현재 proof를 함께 표시한다.
- Claim Boundaries: before/current/next와 claim lane만 남긴다. public demo와 controlled synthetic signal은 allowed로 보이지만, real-world generator attribution과 Bitcoin wallet/library attribution은 accepted baseline, classifier vector, nonce-risk report가 없기 때문에 blocked로 남긴다.
- 남은 gap: real-world baseline, classifier label, Bitcoin nonce-risk report.

## Bitcoin 통합

`bitcoin-risk-report`는 기존 ECDSA signature audit 결과와 real-world manifest를 결합한다.

```powershell
python -m prime_audit.cli bitcoin-signature-audit `
  --input data/bitcoin_signatures.json `
  --output data/bitcoin_signature_audit.json

python -m prime_audit.cli bitcoin-risk-report `
  --signature-audit data/bitcoin_signature_audit.json `
  --manifest data/baselines/real_world/manifest.json `
  --output data/bitcoin_generator_risk_report.json
```

출력은 `r` 재사용, high-s 비율, invalid range 비율을 nonce fingerprint로 요약하고, 연결 가능한 Bitcoin/wallet baseline을 함께 보여준다.

## 다음 구현 우선순위

1. OpenSSL/BoringSSL/Go를 로컬에서 실제로 빌드해 2048/3072/4096-bit RSA prime aggregate baseline 생성.
2. 동일한 sample count와 bit-length 조건으로 library 간 fingerprint distance 측정.
3. owned wallet 또는 공개 메타데이터에서 ECDSA/Schnorr signature baseline 생성.
4. OpenSSL/BoringSSL/Go aggregate baseline을 `real_world` claim scope의 feature vector로 export하고 classifier gate를 실제 label replicate 기준으로 재평가.
5. 충분한 label replicate가 쌓이면 XGBoost/Random Forest backend를 선택적 dependency로 추가.
