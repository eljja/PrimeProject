# Baseline Comparison Research Track

작성일: 2026-05-21

## 목적

Generator fingerprint는 단독 리포트보다 기준군과 비교할 때 가치가 커진다. 목표는 OpenSSL, BoringSSL, Bitcoin Core, wallet/library 샘플을 같은 fingerprint schema로 만들고, 의심 데이터셋과의 거리를 계산하는 것이다.

```text
known-good sample
  -> fingerprint-primes
  -> build-baseline

suspicious sample
  -> fingerprint-primes
  -> compare-baselines
```

## 구현된 CLI

기준군 생성:

```powershell
python -m prime_audit.cli build-baseline `
  --fingerprint data/openssl_fingerprint.json `
  --name openssl-owned-sample `
  --source owned-lab `
  --output data/baselines/openssl_owned.json
```

의심 데이터셋 비교:

```powershell
python -m prime_audit.cli compare-baselines `
  --fingerprint data/suspicious_fingerprint.json `
  --baselines data/baselines/openssl_owned.json data/baselines/bitcoin_core_owned.json `
  --output data/baseline_comparison.json
```

## 거리 구성요소

현재 baseline distance는 다음 성분을 결합한다.

- `bit_length`: bit length 분포 차이.
- `residue_tv`: `mod 30`, `210`, `2310` residue drift 차이.
- `low16_collision`: low-bit collision rate 차이.
- `next_prime_exposure`: `left_gap / log(p)` 기반 next-prime 노출 차이.
- `right_gap`: `right_gap / log(p)` 차이.
- `large_left_gap`: 큰 left gap 비율 차이.

출력은 nearest baseline과 성분별 drift를 함께 보여준다.

## 표본 신뢰도

거리값만으로 생성기를 단정하면 위험하다. 현재 구현은 target과 baseline 각각에 대해 다음 품질 점수를 계산한다.

- `sample_size_score`: 강한 기준군으로 보기 위한 200개 레코드 대비 표본 수.
- `minimum_sample_score`: 최소 권장 30개 레코드 대비 표본 수.
- `gap_coverage`: 주변 prime gap context가 계산된 비율.
- `feature_completeness`: 거리 계산에 쓰는 feature가 채워진 비율.
- `overall_confidence`: 위 항목을 결합한 신뢰도.

비교 결과에는 `confidence`가 함께 출력된다. 신뢰도가 낮은 nearest match는 attribution이 아니라 “후보 방향”으로만 해석한다.

## 해석

`distance`는 0에 가까울수록 baseline과 비슷하다. 값이 높으면 다음 중 하나일 수 있다.

- 생성 라이브러리가 다르다.
- 같은 라이브러리지만 옵션 또는 버전이 다르다.
- 표본이 너무 작다.
- 특정 residue/low-bit/gap 제약이 있는 생성기다.
- 데이터가 공개 고정 parameter와 랜덤 생성 prime을 섞고 있다.
- 표본이 너무 작아서 confidence가 낮다.

## 다음 단계

1. OpenSSL RSA prime generation owned sample.
2. BoringSSL owned sample.
3. Bitcoin Core ECDSA/Schnorr nonce metadata sample.
4. Wallet별 signature metadata baseline.
5. baseline registry와 GitHub Pages 비교 시각화.
