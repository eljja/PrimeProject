# TICKET-140: Spectral Moments, Fixed-Floor Limits, Duality, and Rotation

Date: 2026-07-29

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket140-spectral-moments-fixed-floor-duality-rotation.json`

Current continuation / 최신 후속 연구:
[`TICKET-141`](one-sided-moving-floor-robust-dual-and-large-sieve.md)

## Publication boundary / 논문 제출용 경계

**English.** TICKET-140 proves four exact intermediate or proof-route no-go
statements. They are PrimeProject results, not claims of literature priority.
They do not prove or refute the Riemann Hypothesis, Collatz conjecture, strong
Goldbach conjecture, or Twin Prime conjecture. Every universal statement below
has a mathematical proof independent of its finite table. Computation is used
only to replay exact thresholds or illustrate a proved estimate.

**한국어.** TICKET-140은 정확한 중간정리 또는 증명 경로 한계 정리 네 개를
확정한다. 이는 PrimeProject 내부의 결과이며 학계 최초성을 주장하지 않는다.
리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않는다. 아래의 모든 일반 명제는 유한 표와 독립된
수학적 증명을 가지며, 계산은 정확한 임계값을 재생하거나 이미 증명된
부등식을 예시하는 데만 사용한다.

## Result table / 결과표

| Problem / 문제 | Exact result / 정확 결과 | Discarded route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `EvenTraceMomentSpectralCertificateAndLogOrderBarrier` | fixed moment order as a dimension-uniform spectral certificate | `ProjectedWeilLogOrderEvenTraceMomentBelowTailGap` |
| Collatz / 콜라츠 | `FixedCycleMinimumWindowEventuallyVacuousNoGo` | fixed `M=2^28` floor as an all-period window exclusion | `PeriodDependentCycleMinimumDiophantineSeparation` |
| Goldbach / 골드바흐 | `FiniteMeasurementDualCertificateAndPowerOfTwoNullspaceNoGo` | incomplete finite measurements as pointwise control | `ArithmeticK56DualCertificateOnPowerOfTwoHardStratum` |
| Twin Prime / 쌍둥이 소수 | `QuadraticIrrationalSobolevRotationCancellation` | unweighted rotation cancellation as a solution to the parity obstruction | `DiophantineSobolevTypeIIBilinearCancellationWithPositiveTwinMass` |

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `E` be an `r` by `r` self-adjoint matrix and let `m>=1`. Then

```text
rho(E)^(2m) <= tr(E^(2m)) <= r rho(E)^(2m).
```

If a self-adjoint base operator satisfies `A>=gI`, then

```text
tr(E^(2m)) < g^(2m)
```

implies `A+E>0`.

그러나 이 인증의 moment 차수를 고정할 수는 없다. `E=I_r`이면 실제
spectral radius는 1이지만 trace-root 추정은

```text
r^(1/(2m))
```

이다. 상대 오차를 `1+epsilon` 이하로 만들려면 최악의 경우

```text
m >= log(r) / (2 log(1+epsilon))
```

가 필요하다.

### Proof / 증명

`E`의 실수 고유값을 `lambda_1,...,lambda_r`라 하자. 자기수반성이므로

```text
tr(E^(2m)) = sum_i |lambda_i|^(2m).
```

오른쪽 합은 가장 큰 항 `rho(E)^(2m)` 이상이고, 각 항이 그 최댓값
이하이므로 `r rho(E)^(2m)` 이하이다. 따라서 strict trace inequality는
`||E||=rho(E)<g`를 준다. 모든 `x!=0`에 대해

```text
<x,(A+E)x> >= (g-||E||)||x||^2 > 0.
```

`E=I_r`을 대입하면 trace-root가 정확히 `r^(1/(2m))`가 되어 로그 차수
하한이 sharp한 worst-case 장벽임을 보인다. `QED`

### What changed / 무엇이 달라졌는가

TICKET-139는 절댓값 cross-Gram 행합이 signed spectral norm을 크게
과대평가할 수 있음을 증명했다. TICKET-140은 절댓값을 취하지 않고
`tr(E^(2m))`의 signed closed-walk expansion을 사용하는 계산 가능한
충분조건을 제시한다. 동시에 고정된 `m`으로는 차원 전체를 균일하게
제어할 수 없다는 새 no-go를 확정한다.

### Reproducible audit / 재현 계산

목표 factor를 `6/5`로 놓고

```text
r 5^(2m) <= 6^(2m)
```

을 정수로 검사했다.

| rank `r` | minimum `m` |
|---:|---:|
| 4 | 4 |
| 16 | 8 |
| 64 | 12 |
| 256 | 16 |
| 1,024 | 20 |
| 4,096 | 23 |

이 표는 일반 정리의 증명이 아니다. 정수 임계값 구현이 로그 차수 공식을
정확히 따르는지만 검사한다.

### Remaining gap / 남은 간극

실제 projected Weil Gram tail의 even trace moment를 계산하거나
산술적으로 상계하지 않았다. 양의 tail gap도 독립적으로 증명되지 않았다.
다음 단일 보조정리는
`ProjectedWeilLogOrderEvenTraceMomentBelowTailGap`이다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

고정된 최소 주기값 하한 `M>=1`을 택하고

```text
K = ceil(7(3M+1)/10)
```

이라 하자. 모든 `k>=K`에서

```text
(1+1/(3M))^k > 2.
```

한편

```text
S = ceil(k log_2 3)
```

이면 항상

```text
1 < 2^S/3^k < 2.
```

따라서 TICKET-139의 고정-floor 필요조건 창은 `k>=K`인 모든 period에서
valuation 합 하나를 허용한다.

### Proof / 증명

`x>0`에 대해

```text
log(1+x) >= x/(1+x)
```

이므로

```text
log(1+1/(3M)) >= 1/(3M+1).
```

`k>=7(3M+1)/10`이면 upper window의 로그는 `7/10` 이상이다. 지수급수의
앞 네 항만 사용해도

```text
exp(7/10)
> 1 + 7/10 + 49/200 + 343/6000
= 12013/6000
> 2.
```

또한 `log_2 3`은 무리수이므로 `3^k`는 2의 거듭제곱이 아니다.
`S=ceil(k log_2 3)`에 대해

```text
2^(S-1) < 3^k < 2^S,
```

따라서 candidate ratio는 정확히 `(1,2)` 안에 있다. `QED`

### Exact no-go / 정확한 한계

TICKET-139의 `M=2^28`은 `k<=20,000`에서 매우 강한 유한 배제를
제공했다. 그러나 `M`을 고정하면 window width가 period와 함께 증가한다.
이번 정리는 고정된 최소값 하한만으로 모든 period를 배제하려는 경로가
논리적으로 완결될 수 없음을 증명한다.

이 결과는 큰 주기나 Collatz 반례가 존재한다는 뜻이 아니다. window가
valuation 합 하나를 허용한다는 사실은 valuation word, 정수 시작값,
정확 나눗셈 조건, 실제 cycle을 전혀 구성하지 않는다.

### Reproducible audit / 재현 계산

작은 `M`에서는 exact integer powers로 최초 vacuity period를 계산하고,
일반 rational certificate와 비교했다.

| `M` | exact first vacuity period | certified `K` |
|---:|---:|---:|
| `2^4` | 34 | 35 |
| `2^6` | 134 | 136 |
| `2^8` | 533 | 539 |
| `2^10` | 2,130 | 2,152 |
| `2^12` | 8,518 | 8,603 |
| `2^28` | not expanded | 563,714,459 |

`2^28` 행은 거대한 정수 거듭제곱을 생성하지 않는다. 위 rational proof를
기계 판독 가능한 산술 조건으로 기록한다.

### Remaining gap / 남은 간극

cycle minimum에 period에 따라 성장하는 하한 `m>=M(k)`가 필요하며, 이를
`|S log 2-k log 3|`의 explicit separation과 결합해야 한다. 다음 단일
보조정리는 `PeriodDependentCycleMinimumDiophantineSeparation`이다.
그 이후에도 aperiodic orbit의 well-foundedness가 별도로 남는다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

`A`를 실수 `r` by `n` 측정 행렬이라 하자. 측정 제약

```text
|Af| <= b
```

만으로 좌표 `f_j`를 유계화할 수 있으려면 `e_j`가 `row(A)`에 속해야
한다.

- `e_j notin row(A)`이면 `z_j!=0`인 `z in ker(A)`가 존재하며
  `A(f+t z)=Af`이므로 `f_j`는 무한히 변할 수 있다.
- `e_j=A^T lambda`이면

```text
|f_j| <= sum_i |lambda_i| b_i.
```

### Proof / 증명

선형대수의 기본 직교 분해로

```text
row(A)^perp = ker(A).
```

`e_j`가 row space에 없으면 그 kernel projection `z`는
`z_j=<e_j,z>!=0`이다. 따라서 측정을 바꾸지 않고 좌표를 임의로 키울 수
있다. 반대로 `e_j=A^T lambda`이면

```text
f_j = <lambda,Af>
```

이고 weighted triangle inequality가 dual bound를 준다. `QED`

### Power-of-two specialization / 거듭제곱 2 특수화

`q+1`개 거듭제곱 2 점에서 차수 `0,...,q-1`의 `q`개 moment를 측정하자.
Vandermonde rank는 `q`이고 nullity는 1이다. TICKET-139의 barycentric
annihilator는 그 kernel에 있으며 모든 좌표가 0이 아니다. 따라서 이
측정들만으로는 어느 단일 좌표도 유계화할 수 없다.

차수 `q` moment를 하나 더 추가하면 Vandermonde 행렬은 invertible이 되고
Lagrange polynomial이 exact dual certificate를 제공한다. 그러나 support를
`[0,1]`로 정규화하면 첫 좌표 복원의 `L1` amplification은 빠르게 증가한다.

| `q` | support size | first-coordinate dual amplification |
|---:|---:|---:|
| 1 | 2 | `4` |
| 2 | 3 | `16` |
| 3 | 4 | `640/7` |
| 4 | 5 | `6144/7` |
| 6 | 7 | `784334848/1519` |
| 8 | 9 | `845112124899328/192913` |
| 10 | 11 | `1770193732618313822896128/3055934833` |

### Exact no-go / 정확한 한계

TICKET-139는 polynomial moments에 null signal이 있음을 보였다.
TICKET-140은 이를 일반적인 정보 충분성 정리로 승격한다. 점별 Goldbach
residual을 제어하려면 point evaluation이 실제 arithmetic measurement의
row space에 들어가야 하며, dual coefficient의 증폭까지 `K=56` 예산 안에
들어와야 한다.

null signal은 실제 Goldbach residual이 아니다. 이는 불완전한 측정에서
점별 양성을 추론하는 논리의 반례다.

### Remaining gap / 남은 간극

실제 major/minor-arc 또는 localized residual 측정으로
`A^T lambda=e_j`를 만족하는 arithmetic dual을 구성하지 않았다. 다음
단일 보조정리는
`ArithmeticK56DualCertificateOnPowerOfTwoHardStratum`이다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

평균 0인 삼각다항식을

```text
F(x) = sum_(0<|h|<=H) c_h exp(2 pi i h x)
```

라 하자. `alpha=sqrt(2)`에 대해

```text
||h alpha|| > 1/(4|h|).
```

그러므로 모든 `N`에서

```text
|sum_(n=1)^N F(n alpha)|
<= 2 sum_(0<|h|<=H) |h c_h|
<= 2 C_(s,H) ||F||_(H^s),
```

여기서

```text
C_(s,H)^2 = sum_(0<|h|<=H) |h|^(2-2s).
```

`s>3/2`이면 `H`가 증가해도 `C_(s,H)`는 유계다. 이는 `N`과 무관한
uniform cancellation이다.

### Proof / 증명

`p`를 `h sqrt(2)`에 가장 가까운 정수라 하자.

```text
|p^2-2h^2| >= 1.
```

또 `p<2h`, `sqrt(2)<2`이므로

```text
||h sqrt(2)||
= |p-h sqrt(2)|
= |p^2-2h^2|/(p+h sqrt(2))
> 1/(4h).
```

기하급수 공식과 `|sin(pi x)|>=2||x||`에서

```text
|sum_(n=1)^N exp(2 pi i h n sqrt(2))|
<= 1/(2||h sqrt(2)||)
< 2h.
```

Fourier mode를 합하고 Cauchy-Schwarz를 적용하면 선언한 Sobolev bound가
나온다. `sum h^(2-2s)`의 수렴 조건은 정확히 `s>3/2`이다. `QED`

### Reproducible audit / 재현 계산

대칭 coefficient `c_h=c_-h=1/h^3`에 대해 exact uniform bound는

```text
4 sum_(h=1)^H 1/h^2
```

이다. `N=10,100,1000,10000`에서 geometric sums를 계산했다.

| `H` | exact-bound decimal | largest observed sum |
|---:|---:|---:|
| 4 | 5.6944 | 1.6469 |
| 8 | 6.1097 | 1.6357 |
| 16 | 6.3374 | 1.6385 |
| 32 | 6.4567 | 1.6373 |
| 64 | 6.5178 | 1.6379 |

부동소수점 표는 증명이 아니다. Diophantine lower bound와 Sobolev 정리는
위의 정수 residual 논증으로 증명된다.

### Exact progress and boundary / 정확한 진전과 한계

TICKET-139는 scale-dependent Lipschitz lookup을 폐기했다. TICKET-140은
scale-uniform Sobolev regularity를 부여하면 순수 quadratic irrational
rotation sum에서 실제 uniform cancellation을 얻을 수 있음을 증명한다.

그러나 Vaughan 또는 Möbius bilinear coefficients를 삽입하지 않았고,
sieve parity를 깨지 않았으며, exact gap-two positive mass도 얻지 않았다.
다음 단일 보조정리는
`DiophantineSobolevTypeIIBilinearCancellationWithPositiveTwinMass`이다.

## Cross-problem conclusion / 네 문제의 공통 결론

TICKET-140에서 새로 닫힌 부분:

1. signed spectral norm을 even trace moments로 인증할 수 있다.
2. 고정 Collatz minimum floor 창은 큰 period에서 반드시 무력화된다.
3. 점별 Goldbach 제어는 정확한 row-space dual certificate 문제다.
4. uniform Sobolev 조건은 unweighted quadratic rotation에서 실제
   scale-uniform cancellation을 준다.

남아 있는 결정적 산술 입력:

1. projected Weil trace moments의 로그 차수 uniform bound,
2. period-dependent Collatz cycle minimum과 logarithmic separation,
3. 실제 Goldbach residual의 `K=56` arithmetic dual,
4. arithmetic Type II weights를 포함한 Sobolev bilinear cancellation과
   positive twin mass.

이 네 입력 중 어느 것도 이번 티켓에서 증명되지 않았다.

## Related-work boundary / 관련 연구 경계

- Connes and Consani, *Weil positivity and Trace formula, the archimedean
  place*, <https://arxiv.org/abs/2006.13771>. This motivates the operator and
  positivity setting; PrimeProject does not import an RH conclusion.
- Hercher, *There are no Collatz-m-Cycles with m <= 91*,
  <https://arxiv.org/abs/2201.00406>. This records modern cycle-exclusion
  context; TICKET-140 proves only the stated fixed-floor-window no-go.
- Helfgott, *The ternary Goldbach problem*,
  <https://arxiv.org/abs/1501.05438>. Its explicit major/minor-arc and Type II
  methodology is background, not a binary Goldbach theorem.
- Verschueren, *Diophantine Approximation of Anergodic Birkhoff Sums over
  Rotations*, <https://arxiv.org/abs/2304.00635>. It provides broader rotation
  context; the finite Fourier theorem above is proved directly.

## Reproduction / 재현 방법

```powershell
python scripts/ticket140_spectral_moments_fixed_floor_duality_rotation.py
python -m unittest tests.test_ticket140_spectral_moments_fixed_floor_duality_rotation
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Expected machine boundary:

```text
exact theorem count: 4
route correction count: 4
proof DAG count: 4
conjecture resolution count: 0
failure count: 0
```
