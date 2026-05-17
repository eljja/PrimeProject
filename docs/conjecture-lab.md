# PrimeProject Conjecture Lab

작성일: 2026-05-17

## 목적

Conjecture Lab은 이미 해결된 소수 정리를 재현하는 도구가 아니다. 목표는 소수를 관측하는 알고리즘이 유도하는 새로운 측도와 편향을 정의하고, 그 편향이 prime gap, residue class, 생성기 attribution 문제와 어떻게 연결되는지 탐색하는 것이다.

## 핵심 관점

기존 질문:

```text
정수 전체에서 소수는 어떻게 분포하는가?
```

PrimeProject의 질문:

```text
알고리즘 G가 정수 후보를 소수로 사상할 때,
소수 집합 위에 어떤 관측 측도 mu_G가 유도되는가?
```

이 관점에서는 소수 `p`가 단순히 한 점이 아니라, 어떤 생성 절차에서 얼마나 자주 관측되는지를 가진다.

## 생성기 유도 소수 측도

구간 `[2, N]`에서 생성기 `G`가 후보 `x`를 뽑고 소수 `p`를 반환한다고 하자. 이때 소수 `p`의 관측 무게를 다음처럼 정의한다.

```text
mu_G(p) = Pr[G(x) = p]
```

초기 실험에서는 세 가지 생성기를 비교한다.

### 1. Rejection sampling

소수 후보를 균등하게 재샘플링해 소수만 채택한다고 보는 이상 모델이다.

```text
weight(p) = 1
```

이는 소수 counting measure에 가깝다.

### 2. next_prime sampling

균등한 정수 `x`를 선택한 뒤 `next_prime(x)`를 반환한다.

```text
weight(p_i) = p_i - p_{i-1}
```

따라서 큰 left gap 뒤의 소수일수록 더 자주 관측된다. 이것은 단순한 구현 세부사항이 아니라 소수 집합 위의 측도를 바꾸는 연산이다.

### 3. wheel-next sampling

후보를 작은 소수들로 먼저 걸러낸 wheel residue 공간에서 선택한 뒤 다음 소수로 이동한다.

```text
weight(p_i) = #{x : p_{i-1} < x <= p_i, gcd(x, 30) = 1}
```

이 모델은 실제 소수 생성기의 sieve 단계가 관측 분포를 어떻게 바꾸는지 보기 위한 단순화다.

## 새 연구 질문

### 질문 A: gap-weighted residue drift

`next_prime` 측도에서 residue class 분포는 Dirichlet식 균등 분포에 머무는가, 아니면 left gap과 residue class 사이의 상관 때문에 이동하는가?

측정값:

- residue별 weighted mass.
- uniform coprime residue 분포와의 total variation distance.
- generator별 drift 차이.

### 질문 B: 생성기 구분 가능성

동일한 구간의 소수라도 `rejection`, `next_prime`, `wheel-next` 측도로 관측하면 분포가 달라진다. 이 차이가 충분히 크면 공개 키셋에서 생성기 역추정의 근거가 된다.

측정값:

- weight entropy.
- effective support.
- gap-weight concentration.
- residue drift fingerprint.

### 질문 C: 약한 Cramer 연결

Cramer 추측 전체를 증명하지 않고도 다음 약한 실험 명제를 만들 수 있다.

```text
next_prime 관측 측도의 tail은 raw prime gap tail보다 left gap 가중 때문에 두꺼워진다.
```

이 명제는 증명 가능한 부분과 계산 실험 부분으로 분리할 수 있다.

## 첫 번째 정리 후보

정리 후보:

```text
구간 [2, N]에서 x를 균등 선택하고 G(x) = next_prime(x)라고 하자.
경계 효과를 제외하면 소수 p_i가 관측될 확률은 p_i - p_{i-1}에 비례한다.
```

의미:

- `next_prime` 생성기는 소수를 균일하게 샘플링하지 않는다.
- 선택된 소수의 분포는 left gap으로 가중된다.
- 이 가중은 residue drift와 생성기 attribution의 출발점이다.

## PrimeScore 예측 모델

PrimeProject의 예측은 “소수를 정확히 예언한다”가 아니라, 다음 소수가 될 후보를 실용적으로 정렬한다는 의미다. 현재 구현은 다음 hazard score를 사용한다.

```text
PrimeScore(c | x) =
  1 / log(c)
  * wheel_factor(c mod W)
  * residue_factor(c mod m)
  * exp(-(c - x) / log(x))
```

각 항의 의미:

- `1 / log(c)`: 소수정리 기반 지역 밀도.
- `wheel_factor`: 작은 소수로 나누어지지 않는 후보 공간 보정.
- `residue_factor`: `next_prime` 관측 측도에서 나타난 residue drift 보정.
- `exp(-(c - x) / log(x))`: 시작점 `x` 이후 아직 소수가 나오지 않았을 gap survival 근사.

이 점수는 암호 소수를 깨는 도구가 아니라, 후보 우선순위와 생성기 편향 해석을 위한 실험 도구다.

## 실험 도구

Python:

```powershell
python -m prime_audit.cli gap-lab --limit 100000 --modulo 30 --output data/conjecture_lab_100k.json
python -m prime_audit.cli predict --start 100000 --span 640 --modulo 210 --output data/prediction_100k.json
```

큰 범위는 브라우저에서 매번 재계산하지 않고, 로컬에서 compact summary와 SVG를 만들어 GitHub Pages가 정적 그림으로 제공한다.

```powershell
python -m prime_audit.cli snapshot --limit 10000000 --modulo 210 --output data/snapshots/prime_measure_10m.summary.json --assets-dir assets/snapshots --slug prime_measure_10m
python -m prime_audit.cli snapshot-manifest --inputs data/snapshots/prime_measure_1m.summary.json data/snapshots/prime_measure_10m.summary.json --output data/snapshots/manifest.json
```

현재 번들된 Research Snapshots:

- `1M`: 소수 78,498개, 최대 gap 114.
- `10M`: 소수 664,579개, 최대 gap 154.

Web:

```text
index.html
assets/styles.css
assets/app.js
data/snapshots/manifest.json
assets/snapshots/*.svg
```

GitHub Pages에서 루트 `index.html`을 바로 제공하면 인터랙티브 시각화가 열린다.
