# TICKET-180: 유한 정보의 국소화 가능성 감사

## 상태와 주장 경계

TICKET-180은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이
소수 추측을 **증명하거나 반증하지 않았다**. 이번 티켓에서 확립한 것은
현재 증명 표현이 어떤 결정적 정보를 잃는지 보여 주는 네 개의 정확한
중간 no-go 정리다. `no-go 정리`란 특정 접근이 충분조건이 될 수 없음을
명시적 반례로 증명한 결과를 뜻한다.

| 문제 | 정확히 확립한 결과 | 상태 |
|---|---|---|
| 리만 가설 | `FiniteToeplitzMomentIndeterminacyAndTailEnvelopeNecessity` | 정확히 증명, 리만 가설 미해결 |
| 콜라츠 추측 | `ValuationLayerPermutationNoGoAndOrderedAffinePrefixIdentity` | 정확히 증명, 콜라츠 미해결 |
| 골드바흐 추측 | `MeanSquareExceptionalSpikeNoGoForEveryTargetPositivity` | 정확히 증명, 골드바흐 미해결 |
| 쌍둥이 소수 추측 | `GlobalCenteredEnergyNoGoForUniformBlockCancellation` | 정확히 증명, 쌍둥이 소수 미해결 |

이 결과들은 증명과 실행 가능한 반례를 갖춘 PrimeProject 내부 결과다.
별도의 외부 신규성 심사 없이 학계 최초라는 주장은 하지 않는다.

## TICKET-179에서 왜 이 단계로 왔는가

TICKET-179는 정보를 지나치게 버리던 네 표현을 다음처럼 교체했다.

1. 리만: Fourier 계수 절댓값 합 대신 부호를 보존하는 유계 기호
2. 콜라츠: 고정 비트 깊이 대신 적응형 valuation 층
3. 골드바흐: 연속 구간 양성 대신 실제 이산 짝수 표적의 양성
4. 쌍둥이 소수: 쌍별 coherence 대신 전체 중심화 에너지

TICKET-180은 이 개선된 요약량이 추측에 필요한 위치에서 정보를
국소화하는지 묻는다. 결론은 네 경우 모두 아직 충분하지 않다는 것이다.

- 유한 moment는 무한 고주파 꼬리를 결정하지 못한다.
- valuation의 multiset, 즉 순서를 버린 중복집합은 궤도 순서를 결정하지
  못한다.
- 거의 모든 표적에 대한 평균 제어는 모든 표적의 양성을 보장하지 않는다.
- 전체 평균은 모든 dyadic block의 상쇄를 보장하지 않는다.

## 1. 리만 가설

### 이번에 증명한 정확한 명제

실수 유계 기호 `f`의 Fourier 계수로 만든 `N x N` Toeplitz 절단을
`T_N(f)`라 하자. 정수 `M >= N`과 `A > 0`에 대해

```text
g(theta) = f(theta) + A cos(M theta)
```

로 놓으면 다음이 성립한다.

```text
T_N(g) = T_N(f),
||g-f||_infinity = A,
||g||_infinity >= A - ||f||_infinity.
```

따라서 유한 개 Toeplitz moment만으로는 독립적인 고주파 envelope,
즉 미관측 계수를 제어하는 상계 없이 전체 `L-infinity` 노름을 인증할 수
없다.

### 증명

`T_N`의 성분은 `i-j`번째 Fourier mode를 사용하며
`|i-j| <= N-1`이다. 추가한 cosine의 Fourier support는 `+M`과 `-M`에만
있다. `M >= N`이면 이 두 mode는 유한 절단에 나타나지 않으므로 두 행렬은
완전히 같다. 노름 하계는 역삼각부등식에서 바로 나온다. 이는 수치 추세가
아니라 모든 `N`, `M`, `A`에 대한 정확한 반례족이다.

### 재현 계산

계산기는 `f(theta)=0.2 sign(cos theta)`, 핵심 여유 `delta=0.25`, 숨은
진폭 `A=1`, 숨은 주파수 `M=2N+1`을 사용한다.

| N | 관측 대역 | 숨은 M | 행렬 차이 | theta=0의 기호값 |
|---:|---:|---:|---:|---:|
| 8 | 7 | 17 | 0 | 1.2 |
| 16 | 15 | 33 | 0 | 1.2 |
| 32 | 31 | 65 | 0 | 1.2 |
| 64 | 63 | 129 | 0 | 1.2 |
| 128 | 127 | 257 | 0 | 1.2 |

유한 행렬은 전혀 변하지 않지만 전체 기호는 `0.25` 여유를 크게 넘는다.

### 경로 판정

- **폐기:** 유한 Toeplitz 절단의 일치만으로 실제 Weil 기호의 전체 유계를
  인증하는 경로
- **유지:** 유한 절단과 독립적으로 증명된 산술적 고주파 envelope의 결합
- **남은 간극:** 실제 pole-neutral whitened Weil 꼬리의 미관측 고주파를
  제어하는 envelope가 없다.
- **다음 단일 보조정리:**
  `ArithmeticWeilTailHasCertifiedUniformHighFrequencyEnvelopeBeyondObservedBand`

최근 유한 Guinand-Weil 연구는 정확한 유한 사전과 명시적 꼬리 예산을
제공하지만 리만 가설 증명을 주장하지 않는다. 이번 결과는 왜 미관측 대역에
대한 별도 정리가 필요한지 보여 준다
([Groskin 2026](https://arxiv.org/abs/2607.02828)).

## 2. 콜라츠 추측

### 이번에 증명한 정확한 명제

valuation 단어 `v=(v_0,...,v_(h-1))`에 대해

```text
S = sum_j v_j,
B(v) = sum_j 3^(h-1-j) 2^(v_0+...+v_(j-1))
```

로 놓으면 가속 홀수 콜라츠 분기의 합성은 정확히

```text
T_v(n) = (3^h n + B(v)) / 2^S
```

이다. 적응형 layer count는 valuation multiset과 총합 `S`를 결정하지만,
순서가 들어가는 `B(v)`와 최초 하강 시점은 결정하지 못한다.

### 증명

각 단계 `(3n+1)/2^v`를 귀납적으로 합성하면 위 affine 식을 얻는다.
layer count는 valuation을 순열로 바꾸어도 같지만, `B(v)`의 2의 지수는
순서 있는 prefix 합이므로 달라진다. 모든 양의 valuation 단어는
`2^(S+1)`을 법으로 하는 실제 홀수 자연수 원통으로 실현된다.

가장 강한 자연수 반례쌍은 다음과 같다.

```text
(2,1,1): layers (3,1), B=29, 시작 9,  상태 9,7,11,17, 1단계 하강
(1,2,1): layers (3,1), B=23, 시작 27, 상태 27,41,31,47, 3단계 내 하강 없음
```

두 궤도는 valuation 총합과 모든 적응형 layer가 같지만 최초 하강 행동은
다르다. 계산기는 큰 valuation `2`부터 `8`까지 같은 순서 민감성을 검증한다.

### 경로 판정

- **폐기:** 순서를 버린 적응형 valuation layer만으로 최초 하강이나 주기를
  완전히 판정하는 경로
- **유지:** 자연수 원통 위의 순서 있는 prefix 합과 정확한 affine numerator
- **남은 간극:** 모든 자연수 궤도를 하강하는 순서 원통으로 보내는 균일
  transfer 정리가 없고 비자명 주기도 배제되지 않았다.
- **다음 단일 보조정리:**
  `OrderedCylinderTransferHasUniformDescentOutsideExplicitFiniteExceptionalSet`

최근 one-bit 연구 역시 남은 핵심을 개별 궤도의 mixing 문제로 남긴다
([Chang 2026](https://arxiv.org/abs/2603.25753)).

## 3. 강한 골드바흐 추측

### 이번에 증명한 정확한 명제

평균제곱 제어나 예외 집합 밀도가 0으로 간다는 사실만으로는 모든 짝수
표적의 양성을 증명할 수 없다. `L`개 표적의 major 값이 `mu>0`일 때 한
표적에만 minor 오차 `-(1+epsilon)mu`를 놓고 나머지는 0으로 두면

```text
정규화 RMS = (1+epsilon)mu / sqrt(L) -> 0,
예외 밀도 = 1/L -> 0,
최솟값 = -epsilon mu < 0.
```

### 증명

오차 제곱합에는 항이 하나뿐이므로 RMS 식은 정확하다. 그러나 같은 한 항이
major term을 넘어 부호를 뒤집는다. 따라서 exceptional-set 정리나 `L2`
minor-arc 추정은 강한 골드바흐를 주기 전에 별도의 점별 예외 제거 정리가
필요하다.

계산기는 `mu=1`, `epsilon=0.1`,
`L=16,64,256,1024,4096`을 사용한다. RMS는 `0.275`에서 약 `0.0172`로
감소하지만 예외 표적은 계속 음수다. 별도의 정확한 소수 체는 `10,000`
이하에서 반례를 찾지 못했다. 이는 유한 검증일 뿐 무한 범위의 증명이 아니다.

### 경로 판정

- **폐기:** 평균제곱 minor 제어나 예외 밀도 0만으로 모든 표적의 양성을
  결론 내리는 경로
- **유지:** 명시적 예외 제거를 포함한 표적별 `L-infinity` 결손 상계
- **남은 간극:** 모든 충분히 큰 dyadic block의 모든 짝수에서 minor가
  major보다 작다는 산술 정리가 없다.
- **다음 단일 보조정리:**
  `ParityAliasedMinorHasUniformLInfinityDeficitBelowMajorMainOnEveryDyadicBlock`

현재 exceptional-set 문헌도 예외를 허용하므로 강한 골드바흐의 모든 표적
명제를 주지 않는다
([Grimmelt·Bhowmik 2026](https://arxiv.org/abs/2607.27282)).

## 4. 쌍둥이 소수 추측

### 이번에 증명한 정확한 명제

전체 중심화 에너지 포화는 모든 block의 zero-mode 상쇄를 보장하지 않는다.
`m`개 성분을 가진 block 중 `K`개는 `m`차 단위근 성분으로 완전히 상쇄하고,
하나의 block은 모든 성분을 같은 방향으로 정렬하자. 그러면

```text
sum_b Z_b / sum_b D_b = m/(K+1) -> 0,
Z_bad / D_bad = m,
V_bad / D_bad = 0.
```

### 증명

상쇄 block마다 `D=m`, `Z=0`, `V=m`이다. 정렬 block은
`D=m`, `Z=m^2`, `V=0`이다. 합하면 전체 식이 즉시 나온다. 따라서 전역
평균은 임의로 좋아져도 완전히 상쇄되지 않는 규모 하나를 숨길 수 있다.

계산기는 `m=8`, `K=8,32,128,512,2048`을 검사한다. 전체 zero-mode
비율은 `0.004` 아래로 내려가지만 나쁜 block의 비율은 항상 `8`이다.

### 경로 판정

- **폐기:** 전역 또는 평균 중심화 에너지 포화만으로 모든 규모의 상쇄를
  결론 내리는 경로
- **유지:** 실제 소수쌍 수열의 모든 충분히 큰 dyadic block에 대한 균일
  중심화 에너지 포화
- **남은 간극:** 이런 blockwise 산술 정리도, parity barrier를 넘는 양의
  sieve 하계도 없다.
- **다음 단일 보조정리:**
  `PrimePairHaarCenteredEnergySaturatesDiagonalUniformlyOnEveryLargeDyadicBlock`

소수를 실제로 만들어 내는 sieve 이론도 양의 하계를 위해 충분한 Type II
정보가 필요하며 일반적인 평균 상쇄량만으로 쌍둥이 소수 하계를 만들지 않는다
([Ford·Maynard 2024](https://arxiv.org/abs/2407.14368)).

## 네 문제의 공통 결론

TICKET-180은 다음 네 양화사 오류를 확정했다.

```text
유한 정보     != 무한 꼬리
중복집합      != 순서 있는 경로
거의 모든 값  != 모든 표적
전역 평균     != 모든 block
```

따라서 다음 연구는 단순히 표본 크기를 늘리는 것이 아니라 **균일 국소화
정리**를 만들어야 한다. 대규모 계산은 고주파 envelope, 순서 원통 transfer,
예외 제거 상계, blockwise 포화 법칙의 후보를 반증하거나 지지할 수 있지만,
보편 명제를 대신할 수는 없다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket180_finite_information_localization.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket180_finite_information_localization -v
```

기계 판독 산출물:

- `data/open-problem/ticket180-finite-information-localization.json`
- `data/open-problem/riemann/rh-ticket-180-hidden-frequency.json`
- `data/open-problem/collatz/co-ticket-180-ordered-prefix.json`
- `data/open-problem/goldbach/gb-ticket-180-exceptional-spike.json`
- `data/open-problem/twin-prime/tp-ticket-180-block-localization.json`

모든 문제의 상태는 `open_not_proven`이며 난제 해결 수는 0이다.
