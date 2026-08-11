# TICKET-215: 격자 인증, 거듭제곱 근접충돌, 예외 개수, Abel 경계

## 초록

TICKET-215는 TICKET-214에서 남긴 네 난제의 증명 탐색을 이어간다. 리만
가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측을 증명하거나
반증하지 않는다. 대신 이전의 무한 단계 간극을 더 명시적인 정량 목표로
바꾸는 네 결과를 증명한다.

1. RH 결함을 엄밀한 구간과 음이 아닌 짝수 격자의 교집합으로 인증한다.
   비유계 높이에서 상단이 2보다 작으면 RH가 따르지만 구간 폭만으로는
   부족하다.
2. 순환 valuation word가 `1^k 2^m`인 콜라츠 주기는 하나의 매우 좁은
   지수 근접충돌을 강제한다. 각 `k`에 가능한 `m`은 최대 하나이며
   `1<=k<=4096`에서 후보가 없다.
3. 골드바흐 지수 선택자의 정수부가 유한 블록의 정확한 예외 개수를
   복원한다. 보편적인 온도 임계값도 최적이다.
4. 정확한 간격 2 채널의 Abel 변환은 반지름 1에서 발산할 때 그리고 그때만
   쌍둥이 소수가 무한하다. 1에서 떨어진 유한 개 반지름 표본은 충분하지
   않다.

네 상위 문제의 상태는 모두 `open_not_proven`이며 해결 수는 0이다.

## 결과 원장

| 문제 | TICKET-215의 정확한 결과 | 폐기한 경로 | 남은 간극 | 다음 보조정리 |
|---|---|---|---|---|
| 리만 | `EvenLatticeOneSidedCofinalCertificationAndSharpTwoBarrier` | 2 미만 단측 상계가 없는 구간 폭·상대 정밀도 | 실제 제타의 비유계 결함 상계 | `CofinalActualZetaDefectUpperBoundStrictlyBelowTwo` |
| 콜라츠 | `SingleMountainCycleNearCollisionReductionAndFiniteDiagonalAudit` | 유한 단일-산 대각선 검사를 전체 증명으로 승격 | 모든 `k`, 다중 run, 2 초과 valuation, 발산 | `NoSingleMountainPowerNearCollisionForAllK` |
| 골드바흐 | `ExponentialSelectorExactExceptionCountAndSharpTemperature` | 선택자 정수부 항등식 자체를 덮개 증명으로 사용 | 모든 블록의 산술적 1 미만 상계 | `ArithmeticExactExceptionSelectorBelowOneOnEveryDyadicBlock` |
| 쌍둥이 소수 | `CardinalSelectedAbelBoundaryEquivalenceAndFiniteRadiusNoGo` | 고정 또는 유한 반지름 자료로 무한성을 결론 | 반지름 1 근처의 parity-breaking 발산 | `ParityBreakingLowerBoundForCardinalSelectedAbelTransformNearOne` |

## 1. 리만 가설: 날카로운 짝수 격자 인증

경계에 영점이 없는 높이에서 다음을 둔다.

```text
D(T) = N(T) - M(T)
```

`N`은 임계띠 상반부의 전체 영점 중복도이고 `M`은 임계선 영점
중복도이다. TICKET-213에서 다음을 증명했다.

```text
D(T)는 0 이상의 짝수이다.
```

엄밀 계산이 `D(T)`를 포함하는 구간 `I(T)=[L,U]`를 반환한다고 하자.
가능한 결함은 정확히 다음 교집합이다.

```text
I(T)와 {0,2,4,...}의 교집합
```

### 정리 RH-TICKET-215

`U<2`이면 `D(T)=0`이다. 이 조건이 경계에 영점이 없는 비유계 높이
수열에서 성립하면 TICKET-214의 단조성과 비유계 수열 동치에 의해 RH가 따른다.

상수 2는 날카롭다. 임계선 밖 대칭쌍 하나가 영구히 존재하는 논리 모형은
`D(T)=2`이며, 폭이 0인 정확한 구간 `[2,2]`조차 RH를 인증하지 않는다.
따라서 필요한 것은 단순 정밀도, 구간 폭, 상대오차가 아니라 2보다 작은
단측 상계이다.

유리수 구간 fixture는 영결함 전용, 양의 결함 전용, 모호한 격자 교집합을
정확히 검사한다. 실제 제타 영점 계산은 아니다.

### 남은 간극

```text
CofinalActualZetaDefectUpperBoundStrictlyBelowTwo
```

Platt와 Trudgian은 구간 산술로 높이 `3*10^12`까지 RH를 엄밀 검증했다.
이는 중요한 유한 인증이지만 여기 필요한 비유계 상계는 아니다:
[The Riemann hypothesis is true up to 3*10^12](https://arxiv.org/abs/2004.09765).

## 2. 콜라츠 추측: 단일-산 거듭제곱 근접충돌

`T_a(x)=(3x+1)/2^a`로 두고, 순환 valuation word가 다음인 양의 주기를
생각한다.

```text
1^k 2^m,  k,m>=1
```

아핀 변환을 반복하면 다음을 얻는다.

```text
T_1^k(x) = [3^k x + (3^k-2^k)] / 2^k
T_2^m(y) = [3^m y + (4^m-3^m)] / 4^m
```

다음을 정의한다.

```text
Delta(k,m) = 2^(k+2m) - 3^(k+m)
```

고정점 방정식은 다음과 같다.

```text
Delta x = Delta + 2*3^m*(3^k-2^k)
```

### 정리 CO-TICKET-215

양의 정수 주기가 닫히려면 반드시 다음이 성립한다.

```text
0 < Delta(k,m) <= 3^k - 2^k
```

`Delta`는 홀수이고 3과 서로소이므로 우변 나머지의 나눗셈 조건은
`Delta | (3^k-2^k)`를 강제한다. 또한 첫 양의 `Delta` 이후에는

```text
Delta(k,m+1) = 3 Delta(k,m) + 2^(k+2m) > 3^k
```

이므로 각 `k`에서 가능한 `m`은 두 거듭제곱이 처음 교차하는 한 값뿐이다.

정확 정수 감사는 이 유일한 대각선을 `k=4096`까지 검사했고 근접충돌을
하나도 찾지 못했다. transcript 해시는 다음과 같다.

```text
7e480e162ad783a841d71778b6a916460ab5d3414d229d0b2cf1120b4d69d5d8
```

감사 범위의 모든 `1^k2^m` 주기를 배제하지만, 모든 `k`, 다중 run word,
2보다 큰 valuation, 비주기 발산은 다루지 못한다.

### 남은 간극

```text
NoSingleMountainPowerNearCollisionForAllK
```

Hercher의 더 강한 주기 문헌은 국소 최솟값 개수와 검증 범위 등 다른
매개변수를 사용한다. TICKET-215는 해당 출판 경계를 재현하거나 개선하지
않는다: [There are no Collatz m-cycles with m<=91](https://arxiv.org/abs/2201.00406).

## 3. 강한 골드바흐 추측: 정확한 예외 개수

짝수 목표 `B`개의 블록에서 `A_i`를 순서 없는 골드바흐 표현 개수라 하고
다음을 둔다.

```text
E_B(q) = sum_i q^(A_i)
Z_B    = A_i=0인 목표의 개수
0<q<1
```

### 정리 GB-TICKET-215

```text
Z_B <= E_B(q) <= Z_B + (B-Z_B)q
```

표현이 0인 항은 정확히 1을 기여하고, 양의 정수 표현 개수는 최대 `q`를
기여한다. 따라서

```text
Bq < 1이면 floor(E_B(q)) = Z_B
```

이다. 조건은 보편적으로 최적이다. `Bq=1`일 때 모든 `A_i=1`인 벡터는
예외가 없지만 `E_B=1`이므로 1 미만 검사가 실패한다.

`128, 512, 2048, 8192, 32768`에서 시작하는 dyadic 블록의 정확 소수
감사는 예외를 찾지 못했다. 최소 표현 개수는 각각
`3, 10, 25, 75, 223`이다. 이는 구현 검증이지 모든 블록의 상계가 아니다.

### 남은 간극

```text
ArithmeticExactExceptionSelectorBelowOneOnEveryDyadicBlock
```

출판된 `4*10^18`까지의 유한 검증은 이 로컬 감사보다 훨씬 크지만 여전히
모든 정수를 통제하지 않는다:
[Empirical verification of the even Goldbach conjecture](https://www.ams.org/mcom/2014-83-288/S0025-5718-2013-02787-1/).

## 4. 쌍둥이 소수 추측: Abel 경계 목표

다음을 정의한다.

```text
a_n = n과 n+2가 모두 소수이면 1, 아니면 0
F(r) = sum_(홀수 n>=3) a_n r^n,  0<r<1
```

TICKET-214의 cardinal-sine 선택자에 의해 `a_n`은 bounded-gap 대리변수가
아니라 정확한 간격 2 채널이다.

### 정리 TP-TICKET-215

쌍둥이 소수 추측은 다음과 동치이다.

```text
r이 1로 증가할 때 F(r)이 무한대로 발산한다.
```

쌍둥이 소수가 유한하면 경계 극한은 그 유한 개수이다. 무한하면 임의의
`K`개 비영 항이 각각 1로 접근하므로 단조수렴에 의해 `F`가 비유계이다.

그러나 고정 반지름 자료는 결정적이지 않다. 모든 `r<1`에서

```text
F(r) <= r^3/(1-r^2)
```

이다. 유한 표본 반지름의 최댓값을 `r_*<1`이라 하고 충분히 큰 홀수
`N`부터 모든 홀수 위치에 1을 추가하면 전체 기여는

```text
r_*^N/(1-r_*^2)
```

이므로 원하는 오차보다 작게 만들 수 있다. 정확 fixture는 반지름
`1/2, 2/3, 3/4, 9/10`, 오차 `1/1000`, `N=83`을 사용한다. 이는 논리적
support 반례이지 무한 소수쌍의 구성이 아니다.

`10^6`까지의 유한 소수 감사는 누적 쌍둥이 소수 개수
`8, 35, 205, 1224, 8169`를 얻고 `r_X=1-1/X`의 Abel 상하계를 검사한다.

### 남은 간극

```text
ParityBreakingLowerBoundForCardinalSelectedAbelTransformNearOne
```

Ford와 Maynard의 일반 체 이론은 비자명한 소수 하한에 상당한 Type II
정보가 필요한 이유를 보여준다. Abel 항등식은 그 parity-breaking 입력을
제공하지 않는다:
[On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).

## 공통 결론

TICKET-215는 네 모호한 무한 요구를 네 경계 부등식으로 바꾼다.

```text
RH:        비유계 높이에서 인증된 결함 상단 < 2
콜라츠:    유일한 단일-산 대각선에 거듭제곱 근접충돌이 없음
골드바흐:  모든 블록에서 산술적 예외 선택자 값 < 1
쌍둥이:    r->1에서 parity-breaking Abel 하한이 무한대로 발산
```

필요한 전 범위 형태의 부등식은 어느 것도 증명하지 못했다.

## 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket215_lattice_nearcollision_exception_abel.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket215_lattice_nearcollision_exception_abel -v
```

주 기계 판독 산출물:

```text
data/open-problem/ticket215-lattice-nearcollision-exception-abel.json
```

독립적인 전문가 검토 전에는 문헌 최초성 주장을 하지 않는다.
