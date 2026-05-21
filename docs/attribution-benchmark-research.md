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
  --control-mode bit_length `
  --output data/attribution_benchmark.json
```

```powershell
python -m prime_audit.cli attribution-grid `
  --limits 50000 200000 1000000 `
  --train-counts 40 80 `
  --test-counts 20 40 `
  --trials 3 `
  --output data/attribution_confound_grid.json
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
- `control`: confound 통제 모드와 train/test bit-length bucket 계획.
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

## Confound Control

`--control-mode bit_length`는 train/test 샘플에서 모든 생성기가 동일한 bit-length bucket 분포를 갖도록 강제한다. 이 모드는 attribution이 단순히 “큰 수를 더 자주 뽑은 생성기”를 맞히는 상황을 제거한다.

특히 `bit_length_only` ablation이 높은 정확도를 보이면 두 가지 가능성이 있다.

- 실제 생성기 흔적이 아니라 샘플링 범위 차이를 학습했을 가능성.
- 특정 생성기가 같은 관측 공간 안에서도 bit-length 경계 근처를 다르게 가중했을 가능성.

통제 모드에서 `bit_length_only` 정확도는 낮아지고, `residue_only` 또는 `gap_only` 신호가 남아야 더 강한 연구 주장으로 이어진다. 따라서 실제 OpenSSL/BoringSSL/Bitcoin Core/wallet sample 비교 전에는 반드시 uncontrolled 결과와 controlled 결과를 함께 보고해야 한다.

## Confound Grid

`attribution-grid`는 같은 `limit`, `train_count`, `test_count` 조합에서 uncontrolled run과 bit-length-controlled run을 쌍으로 실행한다. 출력은 다음 연구 판단을 자동화한다.

- `rows`: 각 run의 profile별 accuracy.
- `deltas`: 같은 설정에서 uncontrolled accuracy와 controlled accuracy의 차이.
- `summary.profiles`: profile별 평균 drop과 interpretation count.
- `most_confound_sensitive_profiles`: bit-length 통제로 성능이 많이 떨어진 profile 순위.

해석 기준은 보수적으로 둔다. controlled accuracy가 random baseline보다 충분히 높으면 `survives_bit_length_control`, uncontrolled에서만 높으면 `control_sensitive`, `bit_length_only`가 통제 후 떨어지면 `bit_length_confound`로 표시한다.

GitHub Pages의 Attribution Grid 패널은 `data/attribution_confound_grid.json`을 읽어서 profile별 mean controlled accuracy와 accuracy drop을 보여준다. 이 뷰의 목적은 “예측 성공률”을 과장하는 것이 아니라, 남는 신호와 사라지는 신호를 분리해서 다음 실험 설계를 정하는 것이다.

## 해석

이 실험은 실제 라이브러리 attribution을 증명하는 최종 결과가 아니다. 하지만 다음을 검증하는 최소 과학적 장치다.

- fingerprint feature가 생성기 차이를 어느 정도 담는가.
- 표본 수가 줄어들 때 confidence가 어떻게 떨어지는가.
- `next_prime` 편향과 `wheel30_next` 편향이 rejection 기준선과 구별되는가.
- baseline distance가 단순한 시각화가 아니라 재현 가능한 분류 실험으로 이어지는가.

## 다음 단계

1. 실제 OpenSSL/BoringSSL owned sample을 baseline으로 추가.
2. 실제 library sample에서도 같은 delta report를 생성.
3. train/test split을 여러 seed로 반복해 confidence interval을 추가.
4. GitHub Pages에서 profile별 confidence interval과 confusion matrix를 함께 표시.
