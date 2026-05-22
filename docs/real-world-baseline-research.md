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
python -m prime_audit.cli export-feature-vectors `
  --fingerprints openssl=data/openssl_fingerprint.json suspicious=data/suspicious_fingerprint.json `
  --baselines go=data/baselines/go_owned.json `
  --output data/feature_vectors.json
```

현재 feature는 bit-length distribution moments, residue TV drift, low16 collision, next-prime exposure, local gap statistics를 포함한다.

## Crypto-Classifier v1

`crypto-classifier`는 XGBoost나 Random Forest를 바로 넣기 전의 dependency-free baseline이다. nearest-centroid 모델에 interaction feature를 추가해서 다변량 교차 편향이 실제로 남는지 빠르게 검증한다.

```powershell
python -m prime_audit.cli crypto-classifier `
  --features data/feature_vectors.json `
  --feature-space interaction `
  --output data/crypto_classifier_report.json
```

이 모델은 최종 분류기가 아니라 연구 안전장치다. 여기서도 분리되지 않는 신호는 무거운 ML을 넣어도 과장될 가능성이 높다.

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

이 값은 attribution 증명이 아니라 수집 계획의 품질 경계다. GitHub Pages는 이 결과를 Baseline Lab에 표시해서 500개 RSA sample을 강한 실세계 claim으로 오해하지 않게 한다.

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

중요한 원칙은 “좋은 점수”보다 “blocking gap”이다. 현재처럼 real-world available baseline이 부족하거나 classifier label이 없으면, 페이지는 이를 명시적으로 high-priority gap으로 남긴다.

## Evidence Pack

`evidence-pack`은 공개 산출물의 재현성과 주장 한계를 묶는 최종 출판 단위다. 입력 JSON의 SHA-256, schema, byte size를 기록하고 publication gate를 통과했는지 표시한다.

```powershell
python -m prime_audit.cli evidence-pack `
  --manifest data/baselines/real_world/manifest.json `
  --readiness data/research_readiness.json `
  --attribution-grid data/attribution_confound_grid.json `
  --artifact project_evolution=data/project_evolution.json snapshot_manifest=data/snapshots/manifest.json collection_matrix=data/collection_matrix.json collection_power=data/collection_power.json `
  --classifier-report data/crypto_classifier_report.json `
  --bitcoin-risk-report data/bitcoin_generator_risk_report.json `
  --output data/evidence_pack.json
```

현재 claim level은 `public_demo_only`로 남는다. 이는 실패가 아니라 의도적인 안전장치다. OpenSSL/BoringSSL/Go aggregate baseline과 labelled feature vector가 생기기 전에는 “실세계 생성기 attribution을 증명했다”고 말하지 않도록 막는다.

## Project Evolution View

GitHub Pages의 Project Evolution 패널은 `data/project_evolution.json`을 읽어 지금까지의 변화 자체를 연구 산출물로 시각화한다.

- 연구 단계: regularity plan -> Conjecture Lab -> snapshots -> fingerprint baseline -> attribution grid -> real-world registry -> collection matrix -> collection power -> readiness -> evidence pack.
- 현황 지표: 10M live compute limit, snapshot 수, real-world baseline 등록 수, collection target 수, sample power tier, attribution grid row 수, claim level.
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
4. classifier report를 Attribution Grid처럼 GitHub Pages에서 시각화.
5. 충분한 label replicate가 쌓이면 XGBoost/Random Forest backend를 선택적 dependency로 추가.
