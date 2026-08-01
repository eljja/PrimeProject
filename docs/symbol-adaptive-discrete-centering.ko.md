# TICKET-179: 부호 기호, 적응형 valuation 층, 이산 표적, 중심화 에너지

## 주장 경계

**네 추측은 모두 미해결입니다.** TICKET-179은 네 개의 정확한 표현 정리
또는 no-go 결과를 증명합니다. 리만 가설, 콜라츠 추측, 강한 골드바흐
추측, 쌍둥이 소수 추측을 증명하거나 반증하지 않았습니다.

| 문제 | 이번에 증명한 정확한 결과 | 상태 | 폐기한 경로 | 남은 산술 간극 | 다음 단일 보조정리 |
|---|---|---|---|---|---|
| 리만 | `유계 Toeplitz 기호 인증과 절대합 필요성 no-go` | 미해결 | 균일 Toeplitz 제어에 절대합 가능성이 필요하다는 주장 | 실제 whitening된 Weil 꼬리의 유계 기호를 얻지 못함 | `PoleNeutralWeilWhitenedTailHasBoundedRealFourierSymbolBelowCoreMargin` |
| 콜라츠 | `적응형 valuation 층의 완전성과 고정 깊이의 불완전성` | 미해결 | 고정 저비트 깊이가 모든 최초 하강을 탐지한다는 주장 | 모든 궤도의 적응형 잉여와 비자명 주기 배제가 없음 | `EveryAperiodicNonDescendingOrbitAccumulatesAdaptiveValuationLayerSurplusBeyondExactCorrection` |
| 골드바흐 | `이산 표적 양성 인증과 연속 보간 no-go` | 미해결 | 이산 짝수 표적에 연속 원 전체 양성이 필요하다는 주장 | 모든 큰 짝수에 대한 minor deficit 상계가 없음 | `ParityAliasedMinorHasUniformDiscreteEvenTargetDeficitBelowMajorMain` |
| 쌍둥이 소수 | `교차-Gram 중심화 항등식과 쌍별 비상관 no-go` | 미해결 | 작은 쌍별 coherence가 영모드 상쇄를 강제한다는 주장 | 실제 소수쌍 Haar 블록의 중심화 에너지 포화 정리가 없음 | `PrimePairHaarCenteredEnergySaturatesDiagonalAtPowerSavingRate` |

모든 기계 판독 시도의 상태는 `open_not_proven`이며 해결 수는 0입니다.

## 1. 리만: 절댓값 꼬리 대신 부호를 보존한 유계 기호

### 이번에 선언한 명제

`f`를 단위원 위의 실수값 `L-infinity` 함수라 하고 그 Fourier 계수를

```text
a_r = (1 / 2 pi) integral f(theta) exp(-i r theta) d theta
```

라고 하겠습니다. 유한 Hermitian Toeplitz 절단

```text
T_N = (a_(i-j))_(0 <= i,j < N)
```

은 모든 `N`에 대해

```text
||T_N||_op <= ||f||_infinity
```

를 만족합니다. 따라서 whitening된 양의 core 여유가 `delta`일 때
`||f||_infinity<delta`이면 꼬리를 더해도 양성이 유지됩니다. 계수의
절대합 가능성은 필요조건이 아닙니다.

### 증명

`x in C^N`에 대해 `p_x(z)=sum_j x_j z^j`라고 두면 Fourier 직교성으로

```text
x* T_N x
  = (1 / 2 pi) integral f(theta)|p_x(exp(i theta))|^2 d theta
```

입니다. 절댓값은 `||f||_infinity||x||_2^2` 이하이므로 연산자 노름
상계가 성립합니다.

이제

```text
f(theta)=C sign(cos theta)
```

를 사용합니다. 0이 아닌 Fourier 계수는

```text
a_(plus/minus(2k+1))=2C(-1)^k/[pi(2k+1)]
```

입니다. 절댓값 합은 조화급수처럼 발산하지만 모든 유한 Toeplitz 절단의
연산자 노름은 `C` 이하입니다. 이는 TICKET-178에서 사용한 절대합 조건이
필요하다는 주장을 반증하는 무한 반례족입니다.

### 재현 계산

`C=0.2`, core 여유 `delta=0.25`, 차원
`16,32,64,128,256,512`를 사용했습니다. 유계 기호 인증은 모두 통과하고,
절대 행합 상계는 증가하여 core 여유를 초과합니다. 한편 all-ones
Rayleigh 몫은 유계 기호의 Fejer 평균이므로 계속 `[-C,C]` 안에 있습니다.

### 한계

사각파는 함수해석 반례이지 실제 Weil 꼬리가 아닙니다. 실제
pole-neutral whitening 꼬리를 실수 유계 기호의 Fourier 계수로 나타내고
그 본질적 상한이 core 여유보다 작음을 보여야 합니다. 최근의 truncated
Weil 연구도 유한 dictionary와 tail 예산을 제공하지만 이 무한 기호 상계나
RH는 증명하지 않습니다
([Groskin 2026](https://arxiv.org/abs/2607.02828),
[Kim 외 2026](https://arxiv.org/abs/2607.24830)).

## 2. 콜라츠: 적응형 층은 정확하지만 고정 깊이는 불완전하다

### 이번에 선언한 명제

가속 홀수 Collatz 사상에서

```text
3 n_i + 1 = 2^(v_i) n_(i+1)
```

라 쓰고

```text
A_k(h)=#{0 <= i < h : v_i >= k}
```

를 정의합니다. 그러면 layer-cake 항등식

```text
sum_(i<h) v_i=sum_(k>=1) A_k(h)
```

이 성립하며, 완성된 prefix의 하강은 다음 조건과 정확히 동치입니다.

```text
sum_(k>=1) A_k(h)
  > h log2(3) + sum_(i<h) log2(1+1/(3n_i)).
```

그러나 임의의 고정 깊이 `K`에 대해 `k<=K` 층만으로는 탐지할 수 없는
최초 하강 자연수 cylinder가 무한히 존재합니다.

### 증명

각 `v_i`는 `k<=v_i`인 모든 층에서 한 번씩 세어지므로 첫 항등식이
성립합니다. 궤도 식을 곱하면

```text
n_h/n_0
 = 3^h 2^(-sum v_i) product_(i<h)(1+1/(3n_i))
```

이므로 정확한 하강 경계가 나옵니다.

고정 `K`에 대해 `h-1+K<=h log2(3)`인 `h`를 고르고,
`h-1+M>h log2(3)`인 `M`을 고릅니다. valuation 단어

```text
(1,1,...,1,M)
```

을 사용합니다. 모든 유한 양의 valuation 단어는
`2^(sum v_i+1)`을 법으로 하는 하나의 홀수 잔여류를 정합니다. 그 법의
배수를 더해도 단어는 변하지 않습니다. 처음 `h-1`개의 valuation 1 단계는
엄격히 증가하고, `2^(h-1+M)>3^h`이므로 충분히 큰 대표는 마지막 단계에서
처음으로 시작값 아래로 내려갑니다. 적응형 합은 경계를 넘지만 `K` 절단
합은 `h log2(3)`도 넘지 못합니다.

### 재현 계산

`K=2,4,8,16`을 검사했습니다. 네 경우 모두 증가 prefix, 마지막 최초
하강, 정확한 layer-cake 등식, 고정 깊이 인증 실패를 확인했습니다. 가장
큰 예시는 `3,760,646,520,831`에서 시작하고 valuation 1이 26번 나온 뒤
17이 나옵니다.

### 한계

적응형 층은 유한 prefix가 이미 주어졌을 때만 완전합니다. 미지의 무한
궤도가 필요한 고층 valuation을 반드시 만들도록 강제하지 못하고 비자명
주기도 배제하지 못합니다. 최근 one-bit 및 parity-vector 연구 역시 사상
전체의 균형과 궤도별 균형을 구분하며 후자를 증명하지 않습니다
([Chang 2026](https://arxiv.org/abs/2603.25753),
[Niu 2026](https://arxiv.org/abs/2605.13886)).

## 3. 골드바흐: 임의의 연속 보간이 아니라 실제 표적 격자를 인증한다

### 이번에 선언한 명제

순환 격자 `G_M={j/M}`에서는 주파수가 `M`을 법으로 같은 character가
완전히 같은 값을 갖습니다. 따라서 계수를 `M`으로 alias한 뒤 inverse
DFT로 계산하면 표적 격자 위의 양성을 정확히 판정합니다. 선택한 연속
삼각다항식 보간의 양성은 충분조건이지만 필요조건은 아닙니다.

### 증명과 no-go 반례족

짝수 `M`마다

```text
F_M(x)=A_M+cos(2 pi x+pi/M),
A_M=[1+cos(pi/M)]/2
```

라고 두면

```text
min_(x in G_M) F_M(x)= [1-cos(pi/M)]/2 > 0,
min_(x in T)   F_M(x)=-[1-cos(pi/M)]/2 < 0.
```

즉 모든 격자 표적은 양수이지만 표적 사이에서는 보간 함수가 음수가
됩니다. 연속 Sobolev 인증 실패는 골드바흐 반례가 될 수 없습니다.

### 재현 계산

격자 크기 `8,16,32,64`에서 반례족을 검사했습니다. 별도의 정확한 소수
convolution으로 `1024` 이하의 모든 짝수에 표현이 있음을 다섯 개의 선언된
유한 범위에서 확인했습니다. 이 유한 계산은 무한 증명이 아닙니다.

### 한계

정확한 parity 및 cyclic alias 이후에도 모든 충분히 큰 짝수 표적에서
minor 항이 증명된 major 주항보다 작다는 이항 산술 상계가 필요합니다.
예외집합 추정은 가능한 모든 예외 표적을 제거하지 않으므로 이 간극을
닫지 않습니다
([Goldbach exceptional set, 2026](https://arxiv.org/abs/2607.27282)).

## 4. 쌍둥이 소수: 영모드 절약은 중심화 에너지 포화와 동치다

### 이번에 선언한 명제

Hilbert 공간 성분 `T_1,...,T_m`에 대해

```text
D=sum_j||T_j||^2,
Z=||sum_j T_j||^2,
bar(T)=(1/m)sum_j T_j,
V=sum_j||T_j-bar(T)||^2
```

라고 두면

```text
V=D-Z/m
```

입니다. 따라서

```text
Z<=eta D  iff  V>=(1-eta/m)D.
```

쌍별 비상관만으로는 이 power saving을 얻을 수 없습니다.

### 증명과 no-go 반례족

중심화 제곱을 전개하면 `V=D-m||bar(T)||^2=D-Z/m`입니다. 직교정규족은
쌍별 coherence가 0이지만 `Z=D`이므로 `eta<1`인 절약이 없습니다. 반대로
1의 복소근으로 이루어진 스칼라족은 coherence가 1이지만 `Z=0`입니다.
필요한 것은 일반적인 쌍별 decorrelation이 아니라 집단적인 부호 중심화입니다.

### 재현 계산

정렬족, 1의 복소근족, 직교정규족을 `m=4,8,16,32`에서 계산했습니다.
중심화 항등식 오차는 `1e-12` 미만입니다. 모든 직교정규족은 coherence
0과 영모드 비율 1을 보이고, 복소근족은 영모드를 `1e-25` 아래로 상쇄합니다.

### 한계

실제 소수쌍 Haar 블록을 사용한 결과가 아닙니다. 쌍둥이 소수 증명에는
양의 prime-producing 주항과 함께 실제 블록의 중심화 에너지가 power-saving
결손으로 포화된다는 산술 Type-II 제어가 필요합니다. 기존 prime-producing
sieve 연구도 이 parity 장벽을 제거하지 못했습니다
([Matomaki와 Merikoski 2024](https://arxiv.org/abs/2407.14368)).

## 네 문제의 공통 결론

TICKET-179은 잘못된 표현을 쓰면 충분조건이 추측 자체처럼 보일 수 있음을
확정했습니다. 절댓값 계수, 고정 비트 깊이, 연속 보간, 쌍별 coherence는
각각 위상, 희귀한 고 valuation, 이산 표적 구조, 집단적 부호 상쇄를
잃습니다.

이번에 정확한 대체 계약으로 증명한 것은 유계 부호 기호, 적응형 층 합,
순환 표적 평가, 중심화 에너지 포화입니다. 이 네 계약에 필요한 실제 산술
균일성 보조정리는 모두 아직 미해결입니다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket179_symbol_adaptive_discrete_centering.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket179_symbol_adaptive_discrete_centering -v
```

주 기계 판독 산출물:

```text
data/open-problem/ticket179-symbol-adaptive-discrete-centering.json
```
