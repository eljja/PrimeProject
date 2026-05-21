# Attribution Benchmark Research Track

작성일: 2026-05-21

## 목적

Generator fingerprint와 baseline distance가 실제로 생성기를 구분하는 데 도움이 되는지 검증하려면 ground truth가 필요하다. 이 트랙은 합성 생성기 `rejection`, `next_prime`, `wheel30_next`에서 샘플을 만들고, train/test로 분리해 attribution 성능을 측정한다.

## CLI

```powershell
python -m prime_audit.cli attribution-benchmark `
  --limit 200000 `
  --train-count 80 `
  --test-count 40 `
  --trials 3 `
  --output data/attribution_benchmark.json
```

## 실험 흐름

```text
build prime observations up to N
  -> sample train primes from each generator-induced measure
  -> fingerprint train samples
  -> build one baseline per generator
  -> sample held-out test primes
  -> compare each test fingerprint to all baselines
  -> report accuracy and confusion matrix
```

## 출력

- `accuracy`: 전체 attribution 정확도.
- `confusion_matrix`: 실제 생성기와 예측 생성기 간 혼동행렬.
- `ablation`: feature group별 정확도와 혼동행렬.
- `baseline_quality`: 각 baseline의 sample quality.
- `trials_detail`: trial별 nearest baseline, distance, confidence, component drift.

## Ablation

현재 benchmark는 기본적으로 다음 profile을 함께 평가한다.

- `all`: 모든 fingerprint component.
- `residue_only`: residue total variation만 사용.
- `gap_only`: left/right/local gap 계열만 사용.
- `low_bits_only`: low16 collision만 사용.
- `bit_length_only`: bit length 분포만 사용.

이 값은 “어떤 feature가 generator attribution에 실제로 기여하는가”를 보기 위한 최소 실험이다. 실제 연구에서는 표본 크기와 범위를 바꿔 ablation curve를 만들어야 한다.

## 해석

이 실험은 실제 라이브러리 attribution을 증명하는 최종 결과가 아니다. 하지만 다음을 검증하는 최소 과학적 장치다.

- fingerprint feature가 생성기 차이를 어느 정도 담는가.
- 표본 수가 줄어들 때 confidence가 어떻게 떨어지는가.
- `next_prime` 편향과 `wheel30_next` 편향이 rejection 기준선과 구별되는가.
- baseline distance가 단순한 시각화가 아니라 재현 가능한 분류 실험으로 이어지는가.

## 다음 단계

1. 합성 실험을 여러 `limit`, `train_count`, `test_count` grid로 자동 반복.
2. 실제 OpenSSL/BoringSSL owned sample을 baseline으로 추가.
3. component ablation: residue만, gap만, low bits만 썼을 때 정확도 비교.
4. GitHub Pages에 confusion matrix heatmap 추가.
