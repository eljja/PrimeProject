# TICKET-186: 유한 여차원, 두 개의 1 주기, 생존층, 양자화된 여유량

## 1. 상태와 주장 경계

TICKET-186은 TICKET-185의 네 열린 노드를 이어간다. 이번 회차에서는 콜라츠
순환의 무한 부분족 하나를 새로 완전히 배제하고, 나머지 세 문제의 과도하거나
부호를 잃은 증명 목표를 정확히 교정했다. 리만 가설, 콜라츠 추측, 강한
골드바흐 추측, 쌍둥이 소수 추측 중 완전히 해결된 문제는 없다.

| 문제 | 이번 정확한 결과 | 폐기한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | `FiniteCodimensionCoercivityIsNotNecessaryForNonnegativity` (유한 여차원 제거 뒤의 강제 양의 하한은 비음성에 필수가 아님) | 유한 개 모드를 제거하면 균일한 양의 틈이 생긴다는 가정 | `WeilQuadraticFormNonnegativityOnExplicitPoleNeutralCoreWithVanishingCertifiedDefect` |
| 콜라츠 | `ExactlyTwoValuationOnesOtherwiseTwoCycleExclusion` (정확히 두 개의 valuation 1, 나머지 2인 주기 전부 배제) | 유한 길이 열거를 모든 길이의 증명처럼 사용 | `NoContractingValuationWordWithExactlyThreeOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| 골드바흐 | `BadSurvivorLayerCakeAndNonnegativeSubhorizonNoGo` (나쁜 생존쌍의 층별 합 항등식과 비음수 정보의 한계) | 비음수 wheel 생존 개수만으로 합성수 오염 상쇄 | `SignedPrimeWeightedBadSurvivorCorrelationHasUniformSubHorizonPowerSaving` |
| 쌍둥이 소수 | `QuantizedTwinProjectorAndFixedRelativeMarginNoGo` (projector의 4단위 양자화와 고정 비율 여유량의 불필요성) | 고정 양의 정규화 여유량을 무한성의 필요조건으로 요구 | `PredeclaredCubicRoughSignedTypeIIMainDominatesRemainderOnInfinitelyManyDyadicBlocks` |

재현 명령은 다음과 같다.

```powershell
D:\python\anaconda3\python.exe scripts\ticket186_codimension_twoone_layercake_quantization.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket186_codimension_twoone_layercake_quantization -v
```

주 기계 판독 결과는
`data/open-problem/ticket186-codimension-twoone-layercake-quantization.json`에
있다. 네 문제의 상태는 모두 `open_not_proven`, 즉 미증명이다.

## 2. 리만 가설

### 2.1 이번에 증명한 명제

무한차원 Hilbert 공간의 정규직교기저를 `e_n`이라 하고 다음 양의 단사 compact
연산자를 생각한다.

```text
A e_n = e_n / n
```

임의의 유한차원 부분공간 `T`를 제거해도 다음 하한은 0이다.

```text
inf { <Ax,x> : x perpendicular to T, ||x||=1 } = 0.        (1)
```

따라서 이차형식이 음수가 아니고 영벡터 외에는 0이 아니더라도, 유한 개의
방해 모드 또는 이동 모드를 몫공간으로 제거하는 것만으로 균일한 양의 하한
`<Ax,x> >= c ||x||^2`, `c>0`이 생기지는 않는다.

### 2.2 증명

`P_T`를 `T`로의 직교사영이라 하자. 유한랭크이므로
`||P_T e_n|| -> 0`이다. 다음 벡터를 정규화한다.

```text
x_n = (I-P_T)e_n / ||(I-P_T)e_n||.
```

그러면 `x_n`은 `T`에 수직이고 `x_n-e_n -> 0`이다. `A`가 유계이므로

```text
<A x_n,x_n> - <A e_n,e_n> -> 0.
```

오른쪽의 두 번째 항은 `1/n -> 0`이다. `A`의 양성 때문에 하한은 0보다
작을 수 없으므로 식 (1)이 성립한다.

좌표 모드 3개를 제거한 `N=8,16,32,64,128,256` 유한 절단에서는 최소값이
정확히 `1/N`이다. 각 유한 절단은 엄격히 양수지만 그 양의 틈은 0으로 간다.

### 2.3 의미와 한계

TICKET-185의 `coercivity`는 강제 양의 하한을 뜻한다. 그러나 RH와 동치인
Weil 기준의 핵심은 비음성이다. 독립적으로 양의 spectral gap을 증명하지 않은
상태에서 coercivity를 필수 목표로 요구하면 원래 문제보다 강한 명제를 쫓게
된다. 따라서 실제 최소 목표는 하나의 명시적이고 조밀한 pole-neutral 형식
core에서 Weil 이차형식의 비음성을 증명하고, 유한 인증의 음의 결손이 0으로
가는 것을 보이는 것이다.

여기서 사용한 대각 연산자는 실제 제타 Weil 연산자가 아니다. 따라서 실제
Weil 양성이나 임계선 밖 영점 배제를 증명하지 않는다. 2026년 screw-function
형식화도 RH를 증명하지 않으며
([Suzuki, 2026](https://arxiv.org/abs/2606.09096)), 수치 연산자 실현은 유한
스펙트럼 증거다
([Kim 외, 2026](https://arxiv.org/abs/2607.24830)).

## 3. 콜라츠 추측

### 3.1 이번에 증명한 명제

가속된 홀수 콜라츠 사상에서 valuation 값 `1`이 정확히 두 번 나오고 나머지가
전부 `2`인 양의 순환은 존재하지 않는다. 순환 이동을 하면 모든 단어는 다음
꼴이다.

```text
w_(a,b) = (1, 2^(a-1), 1, 2^(b-1)),
a,b >= 1, h=a+b.
```

이 명제는 primitive 주기뿐 아니라 더 짧은 주기의 반복인 imprimitive 단어도
포함한다.

### 3.2 정확한 affine 계산

이 valuation 단어의 affine 분자 `B`와 순환 분모 `D`는 다음과 같다.

```text
B_(a,b) = 4^(h-1) - 3^(h-1) + 4^a 3^(b-1),
D_h     = 4^(h-1) - 3^h.                                  (2)
```

수축 범위는 정확히 `h>=5`이다. 또한

```text
B_(a,b)-D_h = 2*3^(h-1) + 4^a 3^(b-1) > 0.               (3)
```

고정된 `h`에서 `B`는 `a=h-1`일 때 최대이므로

```text
B_(a,b) <= 2*4^(h-1)-3^(h-1).
```

`h>=9`이면 `(4/3)^(h-1)>8`이고, 이것은 정확히 다음을 준다.

```text
1 < B_(a,b)/D_h < 3.                                      (4)
```

`B`와 `D`는 모두 홀수다. 만약 `D`가 `B`를 나누면 식 (4)의 몫은 1과 3
사이의 홀수 정수여야 한다. 그 구간의 유일한 정수 2는 짝수이므로 모순이다.

남은 수축 길이 `h=5,6,7,8`에서는 가능한 두 `1` 사이의 거리 22개를 모두
정확한 정수로 검사했고 나눗셈 성립 수는 0이다. 이 유한 계산은 `h>=9`를
외삽하는 것이 아니라, 무한 부등식 증명에서 남은 유한 예외만 닫는다.

### 3.3 의미와 한계

이는 TICKET-185가 제시한 다음 보조정리를 완전히 증명한 실제 무한 부분정리다.
그러나 `1`이 세 번 이상인 단어, `3` 이상의 valuation이 섞인 단어, 주기적이지
않은 발산 자연수 궤도는 다루지 못한다. almost-all, 즉 거의 모든 궤도에 대한
정리는 이 전칭 간극을 채우지 않는다
([Tao, 2022](https://arxiv.org/abs/1909.03562)).

## 4. 강한 골드바흐 추측

### 4.1 이번에 증명한 명제

짝수 `N`을 고정한다. 소수-소수 쌍이 아닌 홀수 후보쌍 `(a,N-a)`에 대해
두 수의 최소소인수 중 작은 값을 `gamma_N(a)`라 하자. 모든 나쁜 쌍의 최대
gate를 `tau_N`이라 하되, 나쁜 쌍이 없으면 `tau_N=0`으로 정의한다. 깊이
`y`에서도 남아 있는 나쁜 쌍의 수를 `B_N(y)`라 하면

```text
B_N(y) >= 1                 for 0 <= y < tau_N,           (5)
sum_(y=0)^(tau_N-1) B_N(y) = sum_bad gamma_N(a).          (6)
```

식 (6)은 나쁜 생존쌍의 정확한 이산 layer-cake, 즉 층별 합 항등식이다.

### 4.2 증명과 no-go 결론

gate가 `gamma`인 쌍은 정확히 깊이 `0,...,gamma-1`에서 생존한다. 쌍을 먼저
더하는 순서와 깊이를 먼저 더하는 순서를 바꾸면 식 (6)을 얻는다. `tau_N>0`
이면 최대 gate `tau_N`을 갖는 쌍은 모든 `y<tau_N`에서 남으므로 식 (5)가
성립한다. 나쁜 쌍이 없으면 `tau_N=0`이고 식 (5)-(6)은 공허하게 성립한다.

따라서 `tau_N>0`이고 그 아래에서 0이 아닌 비음수 가중치 `w_y`를 사용하면

```text
sum_(y<tau_N) w_y B_N(y) > 0.                             (7)
```

즉 비음수 wheel 점유량의 조합만으로는 정확한 인수 지평 이전에 합성수 오염을
모두 상쇄할 수 없다. 부호 있는 소수 가중치나 parity에 민감한 상관정보가
필요하다.

| `N` | `tau_N` | 나쁜 쌍 | 층별 합 | 마지막 나쁜 층 | 소수 표현 수 |
|---:|---:|---:|---:|---:|---:|
| 100 | 7 | 18 | 62 | 1 | 6 |
| 500 | 19 | 111 | 495 | 1 | 13 |
| 1,000 | 29 | 221 | 1,015 | 1 | 28 |
| 5,000 | 67 | 1,173 | 7,073 | 1 | 76 |
| 10,000 | 89 | 2,372 | 15,472 | 1 | 127 |
| 50,000 | 223 | 12,049 | 103,001 | 1 | 450 |

표의 소수 표현은 유한 재현 검사이지 골드바흐 증명이 아니다. 남은 핵심은
모든 충분히 큰 목표에 통하는 부호 있는 von Mangoldt 가중 상쇄 또는 minor
arc 상계다. 최신 exceptional-set 연구도 명시적 major arc와 모든 짝수에 대한
결론을 구분한다
([Grimmelt-Bhowmik, 2026](https://arxiv.org/abs/2607.27282)).

## 5. 쌍둥이 소수 추측

### 5.1 이번에 증명한 명제

TICKET-142의 cubic-rough 지지집합에서 Walsh 역변환은 다음 정확한 식을 준다.

```text
Delta = A00-A10-A01+A11 = 4C,                            (8)
```

여기서 `C`는 블록 안 쌍둥이 소수의 정수 개수다. 따라서

```text
Delta > 0  if and only if  Delta >= 4.                   (9)
```

충분히 큰 모든 후보 시작점을 덮도록 미리 정한 유한 서로소 블록 분할에서,
무한히 많은 블록에 식 (9)가 성립하는 것은 쌍둥이 소수의 무한성과 동치다. 그러나
`Delta >= delta*A00`, `delta>0` 같은 고정 비율 하한은 필요조건이 아니다.

### 5.2 고정 비율 여유량 no-go 증명

임의의 `A00>=2`에 대해 다음 추상 parity 표를 만들 수 있다.

```text
N--=1, N++=A00-1, N+-=N-+=0.
```

이 표에서는

```text
(A10,A01,A11)=(A00-2,A00-2,A00),
Delta=4,
Delta/A00=4/A00 -> 0.
```

즉 각 블록에 twin 부류 하나를 유지하면서도 모든 고정 양의 정규화 여유량을
깨뜨릴 수 있다.

실제 유한 cubic-rough ledger에서는 직접 센 개수를 정확히 복원한다.

| `X` | `A00` | `Delta` | 직접 센 수 | `Delta/A00` |
|---:|---:|---:|---:|---:|
| 1,000 | 59 | 104 | 26 | 1.762712 |
| 10,000 | 358 | 548 | 137 | 1.530726 |
| 100,000 | 2,486 | 3,744 | 936 | 1.506034 |
| 1,000,000 | 17,634 | 26,808 | 6,702 | 1.520245 |

추상 표는 실제 정수의 Liouville 함수값을 바꾼 반례가 아니다. 고정 비율
여유량이 쌍둥이 소수 무한성보다 강하다는 논리적 반례다. 유한 실제 표도
무한 블록의 부호 정리를 주지 않는다. 다음 산술 계약은 고정 비율을 요구하지
않되, 미리 정한 Type I/II 분해의 단측 하한이 정확한 4단위 문턱을 무한히
자주 넘음을 보여야 한다. 소수 생성 하계 체에서 상당한 Type I/II 정보가
필요하다는 일반 장벽은 여전히 남아 있다
([Ford-Maynard, 2024](https://arxiv.org/abs/2407.14368)).

## 6. 증명 DAG와 최종 경계

```text
리만 T185 coercivity 목표
  -> 유한 여차원 coercivity no-go [증명]
  -> 실제 Weil 비음성과 0으로 가는 인증 결손 [열림]

콜라츠 T185 정확히 두 개의 1 목표
  -> 두-1/rest-two 순환 전부 배제 [증명]
  -> 세-1/rest-two affine 나눗셈 배제 [열림]

골드바흐 T185 지평 이전 상쇄 목표
  -> 생존층 항등식과 비음수 정보 no-go [증명]
  -> 부호 있는 소수 가중 subhorizon power saving [열림]

쌍둥이 소수 T185 단측 여유량 목표
  -> 4단위 양자화와 고정 비율 no-go [증명]
  -> 미리 정한 signed Type I/II 주항 우세 [열림]
```

완전한 증명이나 반례는 얻지 못했다. 새 수학적 진전은 콜라츠의 두-1/rest-two
무한 순환 부분족 전체를 배제한 것이다. 나머지 세 결과는 유한 증거를 전칭
명제로 승격하지 않고, 과도하거나 부호를 잃은 계약을 제거해 다음 산술
보조정리를 정확하게 만든다.
