# TICKET-181: 정규화된 국소화와 양자화된 하강 여유

## 상태와 주장 경계

TICKET-181은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 **증명하거나 반증하지 않았다**. 이번에 정확히 증명한 것은
TICKET-180에서 확인한 국소화 실패를 한 단계 좁히는 네 중간 정리다.

| 문제 | 정확히 확립한 결과 | 해결 상태 |
|---|---|---|
| 리만 가설 | `LipschitzFejerTailCertificateAndSampledRegularityNoGo` | 중간 정리 증명, 리만 가설 미해결 |
| 콜라츠 추측 | `OddCylinderSlackQuantizationAndCycleEqualityObstruction` | 중간 정리 증명, 콜라츠 미해결 |
| 골드바흐 추측 | `DiscreteFejerExceptionRemovalCertificateAndSpikeModulusNoGo` | 중간 정리 증명, 골드바흐 미해결 |
| 쌍둥이 소수 추측 | `DyadicPathVariationLocalizationAndScaleL2NoGo` | 중간 정리 증명, 쌍둥이 소수 미해결 |

각 정리는 증명에 필요한 충분조건의 형태를 정확히 밝힌다. 그러나 실제 Weil
기호, 모든 콜라츠 원통, 실제 골드바흐 잔차, 실제 소수쌍 block이 그
충분조건을 만족한다는 산술 정리는 아직 없다. 별도 신규성 심사 없이 학계
최초라는 주장도 하지 않는다.

## TICKET-180에서 무엇이 달라졌는가

TICKET-180은 유한 주파수, 순서를 버린 궤도 요약, 거의 모든 표적에 대한
평균, 전역 block 평균만으로는 보편 명제를 얻을 수 없음을 보였다.
TICKET-181은 빠진 국소화 정보를 다음처럼 구체화한다.

```text
리만:       유한 Fejer 평균 + 증명된 전역 연속성 계수
콜라츠:     한 양자보다 작은 엄밀한 하계 + equality 배제
골드바흐:   이산 Fejer 저주파 + 인접 표적 변화율
쌍둥이 소수: root 기준값 + 경로별 l1 진동의 합 가능성
```

여기서 `Fejer 평균`은 Fourier 부분합을 비음수 kernel로 평균한 것이고,
`modulus` 또는 연속성 계수는 입력 위치가 변할 때 함수값이 얼마나 변할 수
있는지를 제한하는 전역 상계다.

## 1. 리만 가설

### 이번에 증명한 정확한 명제

`f`가 실수값 `2*pi` 주기 `L`-Lipschitz 함수라고 하자. 즉 두 점 사이
함수값 차이가 거리의 `L`배 이하라고 하자. `sigma_N f`를
`|k|<N` Fourier mode를 쓰는 Fejer 평균이라 하고

```text
mu_N = integral[-pi,pi] |t| F_N(t) dt / (2*pi)
     = pi/2 - (4/pi) sum_{1 <= k < N, k odd} (1-k/N)/k^2
```

로 두면

```text
||f - sigma_N f||_infinity <= L mu_N
```

이다. 따라서

```text
||sigma_N f||_infinity + L mu_N < delta
```

를 엄밀히 보이면 `||f||_infinity<delta`가 성립한다.

그러나 `Q`개 균일 표본에서 측정한 기울기를 전역 `L` 대신 쓸 수는 없다.
`0`과 `A sin(Q theta)`는 모든 표본 `theta_j=2*pi*j/Q`에서 값과 표본
차분이 모두 0이지만, 후자의 전체 노름은 `A`, 실제 Lipschitz 상수는
`AQ`다.

### 증명

Fejer kernel은 비음수이고 전체 질량이 1이다. 그러므로

```text
|f(theta)-sigma_N f(theta)|
 <= integral F_N(t)|f(theta)-f(theta-t)| dt/(2*pi)
 <= L integral F_N(t)|t| dt/(2*pi).
```

마지막 적분이 `mu_N`이다. `|t|`의 Fourier 전개를 적분하면 위 유한합
공식을 얻는다. 표본 반례족은 `sin(2*pi*j)=0`에서 즉시 나온다.

### 재현 계산

매끄러운 진단 모델 `f(theta)=0.1 cos(theta)`와 `delta=0.25`를 사용했다.

| N | `mu_N` | 인증된 전체 노름 상계 |
|---:|---:|---:|
| 8 | 0.345946 | 0.122095 |
| 16 | 0.200627 | 0.113813 |
| 32 | 0.114113 | 0.108286 |
| 64 | 0.063952 | 0.104833 |
| 128 | 0.035424 | 0.102761 |
| 256 | 0.019436 | 0.101553 |

여섯 모델은 모두 인증되며, 숨은 sine은 표본에는 보이지 않지만 전역
연속성 예산에서는 사라지지 않는다. 이 모델은 부등식을 점검하는 witness,
즉 진단용 예시일 뿐 실제 산술 Weil 기호가 아니다.

### 경로 판정

- **폐기:** 표본 기울기나 관측 Fourier mode를 증명된 전역 연속성 계수로
  대체하는 경로
- **유지:** 유한 Fejer 평균과 실제 pole-neutral 기호의 독립적으로 증명된
  전역 modulus를 결합하는 경로
- **남은 간극:** 실제 기호의 Fejer 꼬리 예산이 핵심 양성 여유보다 작다는
  산술 상계가 없다.
- **다음 단일 보조정리:**
  `PoleNeutralWeilSymbolHasCertifiedModulusWhoseFejerBudgetFitsBelowCoreMargin`

유한 Guinand-Weil 공식은 엄밀한 유한 계산을 제공하지만 리만 가설을
주장하지 않는다. 이번 정리는 유한 사전 밖의 전역 연속성 추정이 왜 별도로
필요한지 명시한다 ([Groskin 2026](https://arxiv.org/abs/2607.02828)).

## 2. 콜라츠 추측

### 이번에 증명한 정확한 명제

양의 가속 valuation 단어 `w=(v_0,...,v_(h-1))`에 대해

```text
S = sum v_j,
B = sum_j 3^(h-1-j) 2^(v_0+...+v_(j-1)),
D = 2^S - 3^h
```

로 놓자. 이 단어를 실현하는 자연수 원통의 가장 작은 양의 홀수를 `r`,
원통 주기를 `M=2^(S+1)`, `h`단계 뒤 홀수 끝점을
`u=(3^h r+B)/2^S`라 하자. 하강 여유를

```text
H = rD-B = 2^S(r-u)
```

로 정의하면 `H`는 항상 `M`의 정수배다. 따라서 엄밀한 `H>-M`은
`H>=0`을 뜻한다. `H=0`을 별도로 배제하면 `H>=M>0`이 되고, `D>0`인
경우 같은 원통의 모든 뒤 자연수 `r+kM`도 `h`단계 뒤 엄격히 감소한다.

### 증명

끝점의 정수성에서 `3^h r+B=2^S u`이므로
`H=2^S(r-u)`이다. `r`과 `u`가 모두 홀수이므로 그 차는 짝수이고,
따라서 `2^(S+1)=M`이 `H`를 나눈다. `r`을 `r+kM`으로 바꾸면 하강
여유는 `H+kMD`가 되므로 `D>0`에서 양성이 유지된다.

equality를 무시하면 안 된다. 한 단계 단어 `(2)`는 `r=u=1`, `D=1`,
`H=0`이며 고정점이다. 따라서 한 양자보다 큰 하계만으로는 비증가만
얻고 엄격 하강은 얻지 못한다.

### 재현 계산

valuation 알파벳 `{1,2,3,4}`의 모든 단어를 깊이 8까지 정확히 계산했다.

| 깊이 h | 전체 단어 | 비종단 수축 단어 | 양의 slack 양자 | 0 | 음수 |
|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 2 | 2 | 0 | 0 |
| 2 | 16 | 12 | 12 | 0 | 0 |
| 3 | 64 | 59 | 59 | 0 | 0 |
| 4 | 256 | 240 | 240 | 0 | 0 |
| 5 | 1,024 | 1,002 | 1,002 | 0 | 0 |
| 6 | 4,096 | 4,011 | 4,011 | 0 | 0 |
| 7 | 16,384 | 16,060 | 16,060 | 0 | 0 |
| 8 | 65,536 | 65,048 | 65,048 | 0 | 0 |

총 87,380개 단어와 고정점 경계에서 산술 항등식 실패는 없었다. 그러나
valuation 5 이상과 깊이 9 이상을 포함하지 않는 유한 증거이므로 일반
증명이 아니다.

### 경로 판정

- **폐기:** exact enclosure와 equality 배제 없는 근사 slack 하계
- **유지:** 한 양자 단위의 엄밀한 enclosure와 별도의 cycle equality 방해
- **남은 간극:** 모든 깊이의 첫 수축 비종단 원통에 양의 양자가 존재한다는
  정리가 없고 비자명 주기도 배제되지 않았다.
- **다음 단일 보조정리:**
  `EveryFirstContractingNonterminalCylinderHasPositiveSlackQuantum`

Tao의 결과는 로그 밀도 의미에서 거의 모든 궤도를 다루지만 모든 원통과
가능한 주기를 다루지 않으므로 이 보조정리를 주지 않는다
([Tao 2019/2026](https://arxiv.org/abs/1909.03562)).

## 3. 강한 골드바흐 추측

### 이번에 증명한 정확한 명제

순환 표적 공간 `Z/LZ`의 실수 잔차열을 `e`라 하고 인접 표적 최대 변화량을
`D=max_j |e_(j+1)-e_j|`라 하자. `2K<L`인 이산 Fejer kernel `w`로
`sigma_K e=w*e`를 만들고, 순환 거리를 `d_L`이라 할 때

```text
mu_(K,L) = sum_t w_t d_L(0,t),
||e-sigma_K e||_infinity <= D mu_(K,L).
```

따라서 major 수열 `A`가

```text
min_j(A_j+sigma_K e_j) > D mu_(K,L)
```

를 만족하면 모든 표적에서 `A_j+e_j>0`이다.

### 증명

인접 차분을 이어 붙이면
`|e_j-e_(j-t)|<=D d_L(0,t)`이다. 비음수이고 질량이 1인 kernel로 이를
평균하면 균일 근사 부등식이 나온다. 저주파 양성 여유에서 이 오차 예산을
빼면 모든 표적의 양성을 얻는다.

TICKET-180의 한 점 spike는 큰 인접 변화량을 가지므로 이 기준에서 숨지
않고 정확히 탈락한다.

### 재현 계산

| L | K | 매끄러운 모델의 인증 여유 | spike의 인증 여유 |
|---:|---:|---:|---:|
| 32 | 5 | 0.374506 | -1.583437 |
| 64 | 8 | 0.379760 | -2.673095 |
| 128 | 11 | 0.383199 | -4.737762 |
| 256 | 16 | 0.386795 | -7.628441 |
| 512 | 22 | 0.389393 | -12.454936 |

매끄러운 진단 모델은 모두 통과하고 모든 예외 spike는 거부된다. 별도의
정확한 소수 체는 4부터 100,000까지 짝수 49,999개에서 반례를 찾지
못했다. 이는 명시된 유한 범위의 검증일 뿐 무한 명제의 증명이 아니다.

### 경로 판정

- **폐기:** 표적 공간의 modulus가 없는 저주파 또는 거의 모든 값 제어
- **유지:** 이산 Fejer 저주파와 엄밀한 인접 표적 잔차 상계의 결합
- **남은 간극:** 실제 parity-aliased 골드바흐 잔차가 모든 충분히 큰
  block에서 인증 여유 아래에 있다는 산술 상계가 없다.
- **다음 단일 보조정리:**
  `ParityAliasedGoldbachResidualHasCertifiedDiscreteModulusBelowFejerMarginOnEveryLargeBlock`

현재 예외 집합·major arc 연구는 예외 표적을 허용하므로 필요한 균일
modulus를 제공하지 않는다
([Grimmelt·Bhowmik 2026](https://arxiv.org/abs/2607.27282)).

## 4. 쌍둥이 소수 추측

### 이번에 증명한 정확한 명제

root가 있는 dyadic block tree에서 정규화 통계량을 `r(B)`라 하자. 깊이
`j`로 들어가는 모든 edge의
`|r(C)-r(parent(C))|` 최댓값을 `epsilon_j`라 하면, 깊이 `ell`의 모든
block은

```text
|r(B)| <= |r(root)| + sum_{j=1}^ell epsilon_j
```

를 만족한다. 따라서 root 상계와 모든 경로의 합 가능한 `l1` 진동은
모든 block의 균일 국소화를 준다. 반면 edge 최댓값이 0으로 가거나 경로
`l2` 진동이 0으로 가는 것만으로는 부족하다.

### 증명과 반례족

root에서 `B`까지 유일한 경로를 따라 차이를 telescoping하고 삼각부등식을
적용하면 된다. 깊이 `L`의 선택된 한 경로에 `j/L`을 놓고, 그 경로에서
벗어나는 모든 가지에서는 부모값을 그대로 유지하자. 그러면

```text
최대 edge = 1/L -> 0,
경로 l2 = 1/sqrt(L) -> 0,
경로 l1 = 1,
선택된 leaf = 1.
```

따라서 약한 두 조건 아래에서도 나쁜 leaf가 남고, `l1` 상계는 정확히
포화된다.

| 깊이 L | 최대 edge | 경로 l2 | 경로 l1 | 나쁜 leaf |
|---:|---:|---:|---:|---:|
| 8 | 0.125000 | 0.353553 | 1 | 1 |
| 16 | 0.062500 | 0.250000 | 1 | 1 |
| 32 | 0.031250 | 0.176777 | 1 | 1 |
| 64 | 0.015625 | 0.125000 | 1 | 1 |
| 128 | 0.007812 | 0.088388 | 1 | 1 |

### 경로 판정

- **폐기:** scale별 최대 진동 또는 제곱합 진동의 소멸만으로 모든 block
  상쇄를 결론 내리는 경로
- **유지:** root 기준값과 모든 dyadic 경로의 합 가능한 `l1` 진동
- **남은 간극:** 실제 소수쌍 block 통계에 이 상계를 증명하지 못했고,
  국소화 정리 자체는 parity barrier를 넘는 양의 하계가 아니다.
- **다음 단일 보조정리:**
  `PrimePairBlockZeroModeRatioHasSummableDyadicPathOscillationBelowCancellationMargin`

소수를 생성하는 sieve 결과도 실제 Type-II 정보가 필요하며 이 추상
국소화 조건에서 간격 2의 양성을 자동으로 주지 않는다
([Ford·Maynard 2024](https://arxiv.org/abs/2407.14368)).

## 재현 및 반증 계약

```powershell
D:\python\anaconda3\python.exe scripts\ticket181_regularized_localization_quantized_slack.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket181_regularized_localization_quantized_slack -v
```

기계 판독 결과:

- `data/open-problem/ticket181-regularized-localization-quantized-slack.json`
- `data/open-problem/riemann/rh-ticket-181-fejer-modulus.json`
- `data/open-problem/collatz/co-ticket-181-slack-quantum.json`
- `data/open-problem/goldbach/gb-ticket-181-discrete-fejer.json`
- `data/open-problem/twin-prime/tp-ticket-181-tree-variation.json`

각 문제의 proof DAG, 즉 증명 의존성 그래프는 다음 세 노드를 가진다.

```text
반증되거나 불충분한 경로 -> TICKET-181 정확한 정리 -> 열린 다음 보조정리
```

기계 계약은 중간 정리 4개, 폐기 경로 4개, proof DAG 4개, 감사 실패 0개,
난제 해결 0개를 요구한다.
