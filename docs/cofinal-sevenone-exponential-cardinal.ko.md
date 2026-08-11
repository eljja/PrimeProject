# TICKET-214: 비유계 결함, 일곱-1 주기, 지수형 증인, cardinal 간격 선택

## 초록

TICKET-214는 TICKET-213에서 남긴 네 난제의 증명 탐색을 이어간다. 이
티켓은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중
어느 것도 해결하지 않는다. 대신 정확한 대상 선택과 아직 증명되지 않은
무한 산술 추정을 분리하는 네 개의 부분정리 또는 no-go 정리를 확립한다.

1. 경계에 영점이 없는 높이들의 어떤 무한 비유계 수열에서 중복도 결함이
   정확히 0인 것은 RH와 동치지만, 임계선 영점의 밀도가 1이라는 조건은
   충분하지 않다.
2. valuation-one 항이 정확히 7개인 모든 양의 가속 콜라츠 주기 단어를
   보통 정수 나눗셈으로 완전 배제한다.
3. 규모에 따라 변하는 지수형 골드바흐 선택자는 빈 목표를 정확히
   검출하지만, 그 합이 1 미만임을 보이는 일은 바로 블록 전체의 골드바흐
   표현 존재성을 증명하는 일이다. 총 증인 질량과 용량 상계만으로는
   충분하지 않다.
4. cardinal-sine 보간은 모든 짝수 간격에서 gap 2를 정확히 선택하지만,
   선택된 소수 간격 상관값이 무한히 커진다는 정리는 여전히 쌍둥이 소수
   추측의 핵심이다.

네 상위 추측의 상태는 모두 `open_not_proven`이며, 기계 판독 해결 개수는
0이다.

## 결과 원장

| 문제 | TICKET-214의 정확한 결과 | 폐기한 경로 | 남은 간극 | 다음 보조정리 |
|---|---|---|---|---|
| 리만 | `CofinalExactDefectEquivalenceAndDensityOneNoGo` | density-one 또는 상대 결함 수렴을 RH 판정으로 사용 | 실제 제타에 대한 비유계 높이 수열의 정확한 등식 | `CertifiedCofinalMultiplicityEqualityForActualZeta` |
| 콜라츠 | `CompleteSevenValuationOneExclusionAndFiniteStratumNoGo` | 모든 일곱-1 단어와 유한 개 고정 층을 완전 증명으로 승격 | 모든 `k>=8` 주기 층과 비주기 발산 | `UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastEight` |
| 골드바흐 | `DyadicExponentialSelectorEquivalenceAndOccupancyNoGo` | 선택자 구성 또는 총 증인 질량과 용량만으로 독립 증명 | 균일한 산술적 1 미만 추정 | `UniformArithmeticSubunitBoundForDyadicExponentialWitnessSelector` |
| 쌍둥이 소수 | `CardinalSineExactGapTwoSelectorAndPositivityCircularity` | 정확 선택자 구성만으로 증명하거나 고정차수 다항식으로 모든 간격 선택 | 선택된 채널의 비유계 산술 하한 | `UnboundedArithmeticMinorantForCardinalSinePrimeGapFunctional` |

## 1. 리만: 비유계 수열의 정확한 등식과 밀도 1의 차이

경계에 영점이 없는 상반평면 임계띠 직사각형에서 `N(T)`를 중복도를 포함한
전체 영점 수, `M(T)`를 임계선 영점의 총 중복도라 하자. TICKET-213은

```text
D(T) = N(T) - M(T)
     = 2 * (임계선 한쪽의 비임계선 영점 중복도)
```

를 증명했다.

### 정리 RH-TICKET-214

`D(T)`는 음이 아닌 짝수 값의 비감소 계단 함수다. 경계에 영점이 없는
높이들의 어떤 비유계 수열 `T_j`가 존재해 모든 `j`에서 `D(T_j)=0`인 것은
RH와 동치다.

### 증명

비임계선 대칭 영점쌍은 직사각형에 들어오는 순간 `D`에 양의 짝수를 더하며,
높이가 증가해도 사라지지 않는다. 비임계선 영점이 하나라도 있다면 그보다
높은 모든 직사각형에서 `D>=2`가 되어, 이후의 비유계 수열에서 `D=0`일 수
없다. 역방향은 RH 정의에서 바로 따른다.

### density-one no-go

더 약한 조건

```text
M(T) / N(T) -> 1
```

은 RH를 함의하지 않는다. 비임계선 대칭쌍 하나를 계속 유지하면서 임계선
영점 수만 증가시키는 논리적 대칭 영점 모형에서는 `D(T)=2`이지만
`D(T)/N(T)->0`이다. JSON 감사는 임계선 중복도 `10^2`부터 `10^8`까지
이 현상을 정확 유리수로 기록한다.

이것은 논리적 함의에 대한 반례 모형이지, 실제 제타 함수의 비임계선 영점을
발견했다는 주장이 아니다.

### 남은 간극

```text
CertifiedCofinalMultiplicityEqualityForActualZeta
```

실제 제타 영점에 대해 이런 비유계 수열의 정확한 등식은 증명되지 않았다.

## 2. 콜라츠: 일곱-1 층의 완전 배제

양의 가속 콜라츠 주기의 valuation 단어를 `a_0,...,a_(h-1)`, 합을
`A=sum a_i`라 하고, 정확히 `k`개 항이 1이라고 하자. 최소 원소에서 시작하도록
회전하면 `a_0=1`, `a_(h-1)>=2`이며 표준 곱 경계로

```text
A >= 2h-k,
(6/5)^h <= 2^k
```

를 얻는다. `k=7`이면 `8<=h<=26`이고 `A`도 유한하게 제한된다.

### 정리 CO-TICKET-214

valuation-one 항이 정확히 7개인 비자명 양의 가속 콜라츠 주기는 없다.

### 정확 계산

각 허용 길이에서 나머지 여섯 개의 1 위치와 `2h-7` 기준선 위 valuation
초과분의 모든 약한 합성을 열거했다. 각 단어에 대해 보통 정수 방정식

```text
(2^A - 3^h) x = C(a_0,...,a_(h-1))
```

을 검사했다.

```text
후보 단어                         4,349,349
보통 정수 나눗셈 후보                     0
양의 홀수 고정점                           0
기계 실패                                  0
```

길이별 SHA-256 전사 해시는 기계 판독 JSON에 저장된다. 이전 층의 결과와
합치면, 가상의 비자명 양의 주기는 valuation-one 항을 최소 8개 가져야 한다.

### 고정 층 열거 no-go

길이 `h=2k`의 기준 단어만으로도 후보가 적어도

```text
C(2k-2,k-1)
```

개다. 직접 후보 수는 `k=7`에서 4,349,349개, `k=8`에서 49,565,886개,
`k=9`에서 623,355,008개, `k=10`에서 8,498,724,659개로 증가한다. 유한한
개수의 `k` 층만 배제해서는 더 큰 모든 층이 남는다. 이는 현재의 직접 완전
열거를 반복하는 경로의 한계이지, 균일한 구조 정리의 가능성을 부정하지 않는다.

### 남은 간극

```text
UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastEight
```

비주기 발산도 여전히 통제되지 않는다.

## 3. 골드바흐: 규모 증가형 정확 선택자

`B`개의 짝수 목표로 이루어진 유한 블록에서 `A_i`를 순서 없는 골드바흐
표현 개수라 하자. `2^k_B>B`를 만족하는 최소 정수 `k_B`를 택하고

```text
E_B = sum_i 2^(-k_B A_i)
```

로 둔다.

### 정리 GB-TICKET-214, 선택자 동치

```text
E_B < 1  <=>  모든 A_i >= 1.
```

어떤 `A_i=0`이면 해당 항이 1이다. 모든 개수가 양수이면 각 항은
`2^(-k_B)` 이하이므로 `E_B<=B/2^k_B<1`이다.

이는 TICKET-213이 요구한 규모 증가형 비다항식 선택자를 구성한다. 그러나
모든 dyadic 블록에서 합이 1 미만임을 증명하지는 않는다. 그 부등식 자체가
바로 해당 블록의 골드바흐 표현 존재성과 동치다.

### 날카로운 점유 용량 경계

`B`, 총 증인 질량 `S=sum A_i`, 양의 용량 상계 `0<=A_i<=U`와 `U>0`만 안다고 하자. 영인
개수를 `Z`라 하면

```text
Z <= B - ceil(S/U)
```

이며 날카롭다. 질량 `S`를 담으려면 적어도 `ceil(S/U)`개의 양수 칸이
필요하고, 마지막 하나를 제외한 칸을 용량까지 채우면 경계가 달성된다.
집계 정보만으로 `Z=0`을 강제하려면 `S>(B-1)U`가 필요하다.

시작점 `128, 512, 2048, 8192, 32768`의 정확 dyadic 감사에서는 실제 예외가
없었지만, 집계량만으로 허용되는 최대 영 개수는 각각 `33, 143, 638, 2719,
10992`였다. 따라서 총 증인 질량은 목표별 anti-concentration, 즉 증인의
과도한 집중을 막는 정리를 대신할 수 없다.

### 남은 간극

```text
UniformArithmeticSubunitBoundForDyadicExponentialWitnessSelector
```

필요한 추정은 총 질량과 목표별 상계보다 강한 산술 구조를 사용해야 한다.

## 4. 쌍둥이 소수: cardinal-sine 정확 선택

다음을 정의한다.

```text
S(h) = sinc(h/2 - 1),
sinc(x) = sin(pi x)/(pi x),  sinc(0)=1.
```

`(2,3)` 이후의 소수 간격은 모두 짝수다. `h=2r`에서 `r-1`은 정수이므로

```text
S(2)=1,
S(2r)=0  (모든 정수 r>=2).
```

### 정리 TP-TICKET-214

예외 간격 `(2,3)`을 제외한 유한한 연속 홀수 소수 간격에서 크기 `h`인
간격의 개수를 `t_h`라 하면

```text
sum_h S(h)t_h = t_2.
```

이 선택자는 짝수 정수 간격 격자에서 나머지가 정확히 0이다. `10^2, 10^3,
10^4, 10^5`까지의 감사에서 함수값은 각각 `8, 35, 205, 1224`였고 실제 gap
2 개수와 정확히 같았다.

이 누적 함수가 비유계라는 명제는 쌍둥이 소수가 무한히 많다는 명제와
동치다. 따라서 보간 항등식은 채널 선택을 해결하지만 산술적 양의 하한을
해결하지 않는다.

### 다항식 선택자 no-go

gap `2M`까지는 차수 `M-1`의 Lagrange 선택자

```text
P_M(2r) = product_(j=2)^M (r-j)/(1-j)
```

를 쓸 수 있다. 이 함수는 `r=1`에서 1, `2<=r<=M`에서 0이고 꼬리는

```text
P_M(2r) = (-1)^(M-1) C(r-2,M-1),  r>M
```

이다. 0이 아닌 고정 다항식은 모든 정수 `r>=2`에서 사라질 수 없다. cutoff를
키우면 차수와 통제되지 않은 꼬리 크기가 함께 증가한다. cardinal-sine은
표현 오차를 없애지만 소수쌍 상관의 하한을 만들어 주지는 않는다.

### 남은 간극

```text
UnboundedArithmeticMinorantForCardinalSinePrimeGapFunctional
```

## 문제 간 결론

TICKET-214의 공통 결론은 다음과 같다.

```text
정확한 대상 선택 != 양의 무한 산술 통제
```

밀도 1은 RH 결함을 0으로 만들지 않는다. 유한 개의 콜라츠 층은 무한한
valuation 복잡도를 덮지 않는다. 정확한 골드바흐 선택자는 스스로 1 미만
상계를 주지 않는다. 정확한 gap-two 선택자는 선택된 채널이 비유계임을
증명하지 않는다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket214_cofinal_sevenone_exponential_cardinal.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket214_cofinal_sevenone_exponential_cardinal -v
```

주 기계 판독 산출물:

```text
data/open-problem/ticket214-cofinal-sevenone-exponential-cardinal.json
```

네 상위 추측은 모두 미해결이다. 독립적인 수학 검토 전에는 문헌상 최초성도
주장하지 않는다.
