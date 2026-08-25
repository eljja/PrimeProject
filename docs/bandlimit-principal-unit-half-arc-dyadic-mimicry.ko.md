# TICKET-243: bandlimit, principal unit, half-arc energy, dyadic mimicry

상태: **open_not_proven**

회차 완료: **예**

상위 난제 해결 수: **0 / 4**

독립 검토 대기 후보 해결 수: **0**

집중 문제: **콜라츠 추측**

## 주장 경계

TICKET-243은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이
소수 추측을 증명하거나 반증하지 않는다. 정확한 no-go 정리 세 개와
부분정리 하나를 증명한다. 유한 계산 행은 무한 논증을 대신하지 않는 결정적
구현 certificate다.

기계 판독 감사:
`data/open-problem/ticket243-bandlimit-principal-unit-half-arc-dyadic-mimicry.json`.

영속 연구 상태:
`data/open-problem/four-problem-research-state.json`.

재현 명령:

```powershell
python scripts/ticket243_bandlimit_principal_unit_half_arc_dyadic_mimicry.py
python -m unittest tests.test_ticket243_bandlimit_principal_unit_half_arc_dyadic_mimicry -v
python scripts/verify_ticket243_structure.py
python scripts/verify_open_problem_structure.py
```

## 결과 원장

| 문제 | TICKET-243의 정확한 결과 | 분류 | 상위 상태 |
|---|---|---|---|
| 리만 | 정규화된 실수·짝수 함수족이 하나의 고정 Fourier support를 가지면서도 무한 직교열을 포함할 수 있으므로 compact하지 않다 | `exact_no_go` | `open_not_proven` |
| 콜라츠 | 보편적인 principal-unit order-core 전달은 모든 소수 `q>5`의 무계 order `(q-1)/2` 반례족에서 실패한다 | `exact_no_go` | `open_not_proven` |
| 강한 골드바흐 | parity 주파수 `1/2` 주위 폭 `1/(3X)` 전체 구간은 자연 이항 척도의 절대 에너지를 갖는다 | `exact_no_go` | `open_not_proven` |
| 쌍둥이 소수 | 모든 고정 주기 fingerprint는 모든 충분히 큰 dyadic block에서 소수·합성후속항 모방자를 갖는다 | `partial_theorem` | `open_not_proven` |

네 트랙 모두 새로운 정확한 정리 또는 더 날카로운 경계를 얻었으므로 정체
횟수는 `0`이다.

## 1. 리만 가설

### 이번 정확 명제

`n>=1`에 대해

```text
g_n(xi)=pi^(-1/2) cos(n xi),  -pi<=xi<=pi
```

라 하고 `f_n`을 그 역 Fourier 변환이라 하자. 모든 `f_n`은 정규화되고
실수이며 짝수이고 동일한 `[-pi,pi]`에 bandlimited다. 그러나

```text
<f_n,f_m>=delta_nm.
```

따라서 고정 Fourier support와 `L2` 정규화는 짝수 test family의 상대
compactness를 함의하지 않는다.

이 obstruction은 smooth test에도 남는다. 영이 아닌 실수·짝수
`phi in C_c^infinity((-R,R))`에 대해

```text
phi(xi) cos(t xi)
```

의 정규화된 역 Fourier 변환들은 `t`가 증가할 때 분리된 부분열을 갖는다.

### 증명

cosine 직교성으로

```text
integral_(-pi)^pi cos(n xi)cos(m xi) dxi=pi delta_nm.
```

Plancherel을 적용하면 서로 다른 두 함수의 거리 제곱은 `2`다. 따라서
Cauchy 부분열이 없다.

smooth `phi`의 경우 두 modulation의 내적은 `|phi|^2`의 `t-s`, `t+s`
주파수 Fourier coefficient의 합이다. Riemann-Lebesgue 보조정리에 의해
이 값은 0으로 가므로 재귀적으로 충분히 떨어진 분리 부분열을 선택할 수
있다. 역변환은 동일한 주파수 support를 갖는 실수·짝수 Schwartz 함수다.

### 재현 계산

크기 `4, 8, 16, 32, 64`인 다섯 symbolic Gram certificate에서 대각은
`1`, 비대각은 `0`, 최소 거리 제곱은 `2`다.

SHA-256:
`6b52e81598d394e05fffe373733e2a7638a9de662610abd8f1b63c59e46e90cf`.

### exact no-go와 한계

다음 추론은 폐기된다.

```text
frequency tightness + normalization + evenness => compact test family.
```

하나의 고정 compact Fourier support조차 compactness를 주지 않는다.
물리공간의 번역 또는 대칭 번역쌍이 무한대로 빠져나갈 수 있기 때문이다.

이 함수족이 실제 Guinand-Weil admissible class에 속한다고 증명한 것은 아니다.
signed arithmetic tail, 양의 limit margin, zero exclusion, RH는 모두 열려 있다.

### 다음 단일 보조정리

`JointPhysicalFrequencyTightnessAndUniformSignedGuinandWeilTailWithPositiveMargin`.

## 2. 콜라츠 추측 — 집중 문제

### 이번 정확 명제

소수 `q>5`에 대해 primitive root `t mod q`와 Teichmuller lift

```text
T=t^q mod q^2
```

를 잡는다. `(Z/q^2 Z)^*`에서

```text
A=T(1+3q),
B=T(1+5q),
U=A/B,
V=A^5/B^3
```

라 하면

```text
ord_q(V)=(q-1)/2,
V^((q-1)/2)=1 mod q^2,
ord_q(U)=1,
U!=1 mod q^2.
```

실제로 `U=1-2q mod q^2`다. 따라서 `(5,-3)` order core의 square
depth는 무계 order `(q-1)/2`에서도 `(1,-1)` core로 보편적으로
전달되지 않는다.

### 증명

Euler 정리와 mod `q` 축약으로 `T^(q-1)=1 mod q^2`이고 `T`의 정확한
order는 `q-1`이다. 이항 전개로

```text
(1+3q)^5=1+15q mod q^2,
(1+5q)^(-3)=1-15q mod q^2.
```

따라서 `V=T^2 mod q^2`이고 order `(q-1)/2`에서 depth 2 이상이다.
반면

```text
U=(1+3q)/(1+5q)=1-2q mod q^2
```

이므로 `U-1`의 `q`-depth는 정확히 1이다. `(q-1)/2`는 무계다.

### 재현 계산

`5<q<=50,000`인 소수 `5,130`개를 exact modular arithmetic으로 모두
재생했다. 실패는 `0`, 최대 재생 order는 `q=49,999`에서 `24,999`다.

SHA-256:
`fa66801a2a9d21ff3f873a7ac22501d9e8193aea8a9404b42e2e318fdbdff59f`.

### exact no-go와 한계

arbitrary local unit에 유효한 항등식, multiplicative order, LTE,
principal-unit algebra만으로 고정기저 전달을 얻는 경로는 닫힌다.
TICKET-241의 order 1 반례를 TICKET-243이 무계 exact order로 강화했다.

그러나 `A,B`는 `q`에 따라 변하며 고정 정수 `2,3`이 아니다. 따라서

```text
q^2 | 32^d-27^d,  d=ord_q(32/27)
```

인 소수의 존재나 부재는 판정하지 못했다. 일반 necklace와 aperiodic
Collatz trajectory도 열려 있다.

### 다음 단일 보조정리

`FixedBaseRationalWieferichExclusionFor32Over27OnAllPrimeOrderCores`.

## 3. 강한 골드바흐 추측

### 이번 정확 명제

```text
S_X(alpha)=sum_(p<=X) exp(2 pi i p alpha)
```

라 하자. `X>=5`, `|beta|<=1/(6X)`이면

```text
|S_X(1/2+beta)| >= (pi(X)-3)/2.
```

따라서

```text
I_X=[1/2-1/(6X),1/2+1/(6X)]
```

에 대해

```text
integral_(I_X)|S_X(alpha)|^2 d alpha
  >=(pi(X)-3)^2/(12X)
  ~X/(12 log^2 X).
```

### 증명

`alpha=1/2+beta`에서 모든 홀수 소수 항은 `-exp(2 pi i p beta)`다.
`|2 pi p beta|<=pi/3`이므로 cosine은 `1/2` 이상이다. 합에 `-1`을
곱하면 홀수 소수들의 실수부는 `(pi(X)-1)/2` 이상이고 `p=2` 항의
손실은 최대 `1`이다. 이를 제곱해 길이 `1/(3X)`인 구간에서 적분하면
정확한 하한을 얻는다. PNT가 점근 척도를 준다.

### 재현 계산

`X=1,000`부터 `1,000,000`까지 일곱 행에서 prime count, 유리수 arc
폭, pointwise floor, energy floor를 exact하게 기록했다.

SHA-256:
`db3723c1a9cdabd673471f1564af46489235e620f7384d6dcae6f3d3f1446392`.

### exact no-go와 한계

minor set이 전체 `I_X`를 포함한다면 그 절대 `L2` energy는
`o(X/log^2 X)`일 수 없다. 따라서 parity rational frequency는 올바른
폭으로 major arc에 포함되어야 한다.

올바르게 제거된 residual minor arc의 signed target coefficient는 추정하지
못했다. Goldbach representation 하한이나 반례도 얻지 못했다.

### 다음 단일 보조정리

`CompleteSmallDenominatorMajorArcCoverageAndSignedResidualBinaryCoefficientSaving`.

## 4. 쌍둥이 소수 추측

### 이번 정확 명제

`M>=1`과

```text
gcd(a,M)=gcd(a+2,M)=1
```

인 `a mod M`, 그리고 mod `M` 주기 feature `F`를 고정한다. `2M`을
나누지 않는 소수 `ell`을 골라

```text
r=a mod M,
r=-2 mod ell
```

을 푼다. 어떤 `X_0=X_0(M,a,ell)`가 존재하여 모든 `X>=X_0`의
`[X,2X]`에는

```text
F(p,p+2)=F(a,a+2)
```

이면서 `p+2`가 합성수인 소수 `p`가 존재한다.

### 증명

CRT는 `Q=M ell`의 reduced residue class를 준다. 고정 modulus에 대한
PNT in arithmetic progressions로

```text
pi(2X;Q,r)-pi(X;Q,r)~X/(phi(Q)log X)>0.
```

따라서 모든 충분히 큰 dyadic block에 그 class의 소수가 있다. `ell|p+2`
이고 충분히 큰 `p`에서 이는 proper composite다.

### 재현 계산

주기 `30, 210, 2,310, 30,030` 각각의 네 dyadic start에 대해 총 16개
exact witness를 검증했다.

SHA-256:
`3858c95f26b5cf54bc5873b288814a47c38add509e0adf65068b79cf85f8fadd`.

### 부분정리와 한계

TICKET-241의 고정 주기 무한 모방자를 모든 충분히 큰 dyadic block의
모방자로 강화했다. 따라서 eventual scale sampling도 고정 주기 classifier를
구제하지 못한다.

임계값은 고정 modulus에 의존한다. `M=M(X)`가 증가하는 경우의 균일성이나
`Lambda(n)Lambda(n+2)`의 signed Type-II 상쇄는 없다. 쌍둥이 소수의
무한성 또는 유한성을 판정하지 못했다.

### 다음 단일 보조정리

`ScaleLocalGrowingModulusTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass`.

## proof DAG와 적대적 감사

모든 문제의 DAG는 다음 비순환 구조를 갖는다.

```text
TICKET-242 proved input
  + 필요할 때 명시한 external theorem
  -> TICKET-243 disproved inference
  -> TICKET-243 proved theorem
  -> 하나의 open successor lemma
```

허용 상태는 `proved`, `disproved`, `computed_finite`, `external_theorem`,
`assumption`, `heuristic`, `open`뿐이며 각 트랙에는 open frontier가 정확히
하나 있다. 상위 추측 해결 노드는 없다.

## 최종 경계

TICKET-243 회차는 완료되었다. 정확한 no-go 세 개와 부분정리 하나를
증명했지만 상위 난제를 증명하거나 반증하지 않았다. 네 문제 모두
`open_not_proven`이다.
