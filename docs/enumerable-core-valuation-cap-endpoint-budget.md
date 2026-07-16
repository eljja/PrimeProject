# TICKET-129: Enumerable Core, Valuation Cap, and Endpoint Budget

## Abstract / 초록

TICKET-129 continues the four open-problem program without extending a finite
range and calling it evidence for an infinite theorem. It proves four exact
intermediate results:

1. a countable rational-bump core is dense **inside** the smooth compact-support
   autocorrelation image used by a Weil-positivity route;
2. any hypothetical least Collatz counterexample must obey an exact cumulative
   valuation cap for its first `2^29` accelerated odd steps;
3. the Goldbach finite-glue budget admits the weaker and therefore more useful
   pointwise residual target `K=56`, certified entirely with rational bounds;
4. the missing Twin Prime within-block estimate is exactly a signed increment
   synchronization bound, and endpoint monotonicity does not imply it.

TICKET-129는 유한 계산 범위만 늘리지 않고, 네 난제의 실제 미증명 전제를
더 작고 정확한 형태로 줄인다. RH에서는 전체 시험함수 공간이 아니라 Weil
자기상관상 안에서 열거 가능한 유리 bump 핵심집합의 조밀성을 증명한다.
Collatz에서는 가상의 최소 반례가 첫 `2^29` 가속 단계에서 만족해야 하는
누적 valuation 상한을 증명한다. Goldbach에서는 점별 잔차 충분조건을
`K=55`에서 `K=56`으로 개선하고 전 계산을 유리수로 인증한다. Twin Prime은
구간 내부 제어에 필요한 정확한 증분 결함을 분리하고, endpoint 단조성만으로
그 결함을 제어할 수 없다는 반례를 제시한다. 네 난제는 모두 미해결이다.

## 1. Claim discipline / 주장 규율

| Label | Meaning | 한국어 의미 |
|---|---|---|
| exact theorem | proved from the displayed assumptions | 표시된 전제에서 증명된 정리 |
| finite audit | exact computation over a named bounded domain | 명시된 유한 범위의 정확한 계산 |
| route countermodel | refutes one inference, not the conjecture | 특정 추론만 반박하며 가설의 반례는 아님 |
| open premise | still required for a conjecture-level conclusion | 난제 해결에 여전히 필요한 명제 |

No numerical survivor is called a counterexample. No dense subset is called a
proof until continuity and sign certification are both supplied. A sufficient
constant is not confused with a proved residual estimate.

수치 탐색의 생존자를 실제 반례라고 부르지 않는다. 조밀한 부분집합을 얻어도
연속성과 부호 인증이 없으면 증명이 아니다. 또한 “이 상수면 충분하다”는
명제와 “그 상수의 잔차 추정을 증명했다”는 명제를 구분한다.

## 2. Riemann Hypothesis / 리만 가설

Define the standard smooth bump

```text
b(x) = exp(-1/(1-x^2))  for |x|<1,
b(x) = 0                otherwise.
```

Let `C_Q` contain all finite sums

```text
g(x) = sum_j q_j b((x-a_j)/r_j),
```

where `q_j` is Gaussian rational, `a_j` is rational, and `r_j>0` is rational.

### Theorem RH-129: `EnumerableRationalBumpAutocorrelationCoreDensity`

`C_Q` is countable and dense in `C_c^infinity(R)` in the LF test-function
topology. Therefore

```text
{g * tilde(g) : g in C_Q}
```

is countable and dense, in the relative topology, in the smooth
compact-support autocorrelation image.

### Proof / 증명

For any `g in C_c^infinity(R)`, convolution with normalized copies of `b` at
rational scales converges to `g` in every derivative norm on one fixed enlarged
compact set. For a chosen finite derivative order, approximate the convolution
integral and all required derivatives by one Riemann sum. Rationally perturb
the centers and approximate the complex coefficients by Gaussian rationals.
A diagonal sequence handles every derivative order. Every approximant has a
finite rational tuple description, so the union is countable.

Reflection and convolution are continuous when all supports lie in one fixed
compact set. Thus `g_n -> g` implies

```text
g_n * tilde(g_n) -> g * tilde(g).
```

`QED`

한국어로는 다음과 같다. 표준 mollifier를 유리수 scale로 축소한 뒤 원래
함수와 합성곱하면 모든 도함수 노름에서 원래 함수로 수렴한다. 이 적분을
Riemann 합으로 바꾸고 중심과 복소 계수를 유리수로 근사하면 유한 개 유리
bump의 합을 얻는다. 도함수 차수를 대각선 방식으로 증가시키면
`C_c^infinity` 수렴을 얻는다. 반사와 합성곱의 연속성으로 자기상관도
수렴한다.

### What this closes / 닫힌 전제

TICKET-126 proved that the autocorrelation cone is not dense in the entire
ambient real test-function space when evaluation at the identity separates it.
TICKET-129 does **not** revive that false route. It proves relative density only
inside the autocorrelation image, which is the set relevant to the quadratic
form `Q_W(g)=W(g*tilde(g))`.

Every core element has compact support. TICKET-128 therefore reduces its prime
side to the finite list `p^m<=B`. The remaining decisive premise is now:

```text
Next: CertifiedWeilValuesOnRationalBumpCore
다음: 유리 bump 핵심집합의 Weil 값 구간 인증
```

An outward-rounded archimedean evaluator and a proof of nonnegativity on every
enumerated core element are still missing. Density alone does not prove RH.

외향 반올림을 사용하는 archimedean 항 계산기와 모든 핵심 원소에 대한
비음성 증명이 아직 없다. 따라서 RH는 미해결이다.

## 3. Collatz Conjecture / 콜라츠 추측

Use the accelerated odd map

```text
x_(i+1) = (3x_i+1)/2^a_i,
a_i = v_2(3x_i+1),
S_j = a_0+...+a_(j-1).
```

### Theorem CO-129: `LeastCounterexampleInitialValuationCap`

If a least positive Collatz counterexample `n` exists, then `n` is odd,
`n>=2^28`, and for every `1<=j<=2^29`,

```text
S_j <= ceil(j log_2 3) = bit_length(3^j).
```

### Proof / 증명

Minimality implies `x_i>=n` for every accelerated odd iterate. Otherwise the
smaller iterate converges and carries `n` with it. Multiplying the step
identities gives

```text
2^S_j
  = 3^j (n/x_j) product_(i<j)(1+1/(3x_i))
  <= 3^j (1+1/(3n))^j.
```

TICKET-128 verifies strict descent for every nontrivial odd start below `2^28`,
so put `n_0=2^28` and `m=3n_0`. The binomial theorem gives

```text
(1+1/m)^m < sum_(k>=0) 1/k! < 87/32 < 11/4.
```

The last bound is elementary: the sum through `k=3` is `8/3`, and the tail
from `1/4!` is at most `(1/24)/(1-1/5)=5/96`.

For `j<=2n_0=2^29`, `3j<=2m`, so

```text
(1+1/m)^(3j) < (11/4)^2 = 121/16 < 8,
(1+1/m)^j < 2.
```

Hence `2^S_j<2*3^j`, which forces
`S_j<=bit_length(3^j)`. `QED`

### Practical pruning / 실용적 가지치기

The exact dynamic program in the TICKET-129 artifact retains only valuation
words satisfying every prefix cap. At 256 steps the cap is `406`, and the
surviving cylinder mass is approximately `4.7634970603e-9`. This is a finite
language statistic, not a probability that Collatz is true.

이 상한은 실제 changing-prefix 탐색에서 강한 가지치기 조건으로 쓸 수 있다.
256단계에서 허용되는 누적 valuation은 `406` 이하이며, 모든 prefix 제약을
통과하는 잉여류 원통 질량은 약 `4.7635e-9`이다. 이 값은 유한 언어의
밀도이지 콜라츠가 참일 확률이 아니다.

TICKET80 already refuted finite-prefix compactness as a proof route. Repeating
its all-ones witness or merely enlarging the TICKET-128 scan is discarded.

```text
Next: LeastCounterexampleValuationCapLanguageExtinction
다음: 최소 반례 valuation-cap 언어의 전칭 소멸
```

Compatible finite words still exist, so no contradiction and no Collatz proof
has been obtained.

## 4. Goldbach Conjecture / 골드바흐 추측

TICKET-128 certified the weighted major coefficient floor

```text
A > 1.31917.
```

TICKET-126 certified the proper-prime-power contamination form. TICKET-129
removes all floating-point dependence from the endpoint budget.

### Lemma GB-129A: exact logarithm interval

For `H=4*10^18`, use

```text
log(H) = 56 log(2) + 18 log(5/4)
```

and

```text
log(x) = 2 sum_(k>=0) z^(2k+1)/(2k+1),
z=(x-1)/(x+1).
```

Three terms for `log(2)` (`z=1/3`) and two terms for `log(5/4)` (`z=1/9`),
with geometric tail bounds, prove exactly

```text
214/5 < log(H) < 43.
```

Also `H<2^62` and `1200^6<H`. Therefore the TICKET-126 coefficient satisfies

```text
B < 2(1+60/1200) = 21/10.
```

### Theorem GB-129B: `ExactRationalGoldbachResidualK56Sufficiency`

If every even `N>H` satisfies

```text
|R(N)| <= 56 N/log(N),
```

then the inherited weighted finite-glue inequality is strictly positive. The
exact conservative margin is

```text
131917/100000 - 140/107 - 38829/20000000000
= 23019645297/2140000000000
> 0.
```

Thus `K=56` is sufficient. Under the same coarse rational interval, `K=57`
has negative budget, so `56` is the largest integer certified by this
particular endpoint argument.

한국어 핵심은 `K=56` 잔차 정리를 증명했다는 뜻이 아니라, 그 정리가 참일
경우 유한 검증 구간과 무한 해석 구간을 연결하기에 충분하다는 뜻이다.
기존 목표 `K=55`보다 약한 조건이므로 실제 분석 과제는 조금 쉬워졌다.

```text
Next: PointwiseBinaryGoldbachResidualK56
다음: 점별 이항 Goldbach 잔차 K=56 정리
```

This pointwise theorem remains open; therefore strong Goldbach remains open.

## 5. Twin Prime Conjecture / 쌍둥이 소수 추측

Let the cumulative obstruction and known budgets be `A_X` and `K_X>0`, and
write `Q_X=A_X/K_X`. Fix a dyadic left endpoint `Y` and put `q=Q_Y`.

### Theorem TP-129: `ExactWithinBlockIncrementSynchronizationCriterion`

For every `X>=Y`,

```text
Q_X-q = (Delta A-q Delta K)/K_X.
```

Consequently

```text
Q_X <= q+delta throughout [Y,2Y]
```

if and only if

```text
Delta A-q Delta K <= delta K_X throughout [Y,2Y].
```

This follows by substituting `A_X=A_Y+Delta A` and
`K_X=K_Y+Delta K` and cancelling. `QED`

The smallest admissible additive defect is therefore

```text
D(Y) = sup_(Y<=X<=2Y) max(0,Delta A-Q_Y Delta K)/K_X.
```

TICKET-128 gives `limsup_j Q_(2^j)<=0.92`; it does not assert
`Q_(2^j)<=0.92` at every finite endpoint. At `c=1` the exact missing theorem is

```text
limsup_(j->infinity) D(2^j) < 0.08.
```

An eventual uniform bound `D(2^j)<=delta` for one fixed `delta<0.08` is a
sufficient stronger form.

### Stronger countermodel / 강화된 반례

Endpoint control remains insufficient even after adding monotonicity and exact
denominator doubling:

| scale | `A` | `K` | `Q=A/K` |
|---|---:|---:|---:|
| `Y` | `23/25` | `1` | `0.92` |
| `3Y/2` | `46/25` | `1` | `1.84` |
| `2Y` | `46/25` | `2` | `0.92` |

Both `A` and `K` are nondecreasing, the denominator doubles, and both endpoints
equal `0.92`, yet the midpoint exceeds one. The missing fact is synchronization
of signed increments, not interpolation smoothness.

`A`와 `K`가 각각 단조 증가하고 오른쪽 endpoint에서 분모가 정확히 두 배가
되어도 중간점 비율은 `1.84`까지 올라갈 수 있다. 따라서 실제 Vaughan
계수에 대해 `Delta A-Q_Y Delta K`를 직접 제어해야 한다.

```text
Next: AsymptoticVaughanIncrementSynchronizationBelow008
다음: Vaughan 증분 동기화 결함의 점근적 0.08 미만 정리
```

The actual coefficient bound, parity survival, and exact gap-two positivity are
not proved. Twin Prime remains open.

## 6. Result matrix / 결과 행렬

| Problem | Exact TICKET-129 result | Decisive open premise |
|---|---|---|
| RH | enumerable dense core inside autocorrelation image | certified nonnegative Weil values on the core |
| Collatz | least-counterexample valuation cap through `2^29` steps | extinction of every compatible changing-prefix path |
| Goldbach | exact rational sufficiency of `K=56` | pointwise residual bound with `K<=56` |
| Twin Prime | exact increment synchronization criterion | actual Vaughan `limsup D(2^j)<0.08`, parity, gap two |

## 7. Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket129_enumerable_core_valuation_cap_endpoint_budget.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket129_enumerable_core_valuation_cap_endpoint_budget
```

Generated artifacts:

- `data/open-problem/ticket129-enumerable-core-valuation-cap-endpoint-budget.json`
- `data/open-problem/riemann/rh-ticket-129-enumerable-bump-core.json`
- `data/open-problem/collatz/co-ticket-129-valuation-cap.json`
- `data/open-problem/goldbach/gb-ticket-129-k56-endpoint.json`
- `data/open-problem/twin-prime/tp-ticket-129-increment-synchronization.json`

## 8. Literature boundary / 문헌 경계

- M. Suzuki, [Weil's quadratic form via the screw function](https://arxiv.org/abs/2606.09096), for the current `C_c^infinity(R)` formulation of Weil positivity. TICKET-129 does not claim positivity.
- T. Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562), for the almost-all versus universal boundary.
- T. Oliveira e Silva, S. Herzog, and S. Pardi, [Empirical verification of the even Goldbach conjecture and computation of prime gaps up to `4*10^18`](https://doi.org/10.1090/S0025-5718-2013-02787-1), for the finite verification endpoint.
- K. Ford and J. Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368), for the sieve-theoretic boundary; TICKET-129 does not remove parity.

These references fix the accepted problem formulations and known boundaries.
The TICKET-129 lemmas are proved in this document and replayed by repository
tests; citations are not substitutes for the missing conjecture-level steps.
