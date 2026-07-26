# TICKET-162: Form transport, explicit Baker closure, integral budgets, and multiscale Type II

한국어 제목: **형식 수송, 명시적 Baker 폐쇄, 적분 예산, 다중척도 Type II**

Status / 상태: `open_not_proven` for all four conjectures / 네 추측 모두 미해결

Generated / 생성: 2026-07-27 (Asia/Seoul)

## Abstract / 초록

TICKET-162 continues the four-track proof search without promoting finite
evidence to an infinite conclusion. It proves four intermediate results.
First, an `H2`-bounded compact source family can be transported through the
moving Fourier cutoffs in `H1`, while the full `H1` unit ball admits no
uniform projection rate. Second, the minimal front-loaded Collatz family
isolated in TICKET-161 is closed for every length `m >= 2` by combining an
explicit Matveev threshold with a certified continued-fraction enumeration;
the same theorem proves that this family has vanishing compositional
coverage. Third, a normalized negative-error second moment below one is an
exact pointwise Goldbach certificate, and the constant one is sharp. Fourth,
nested dyadic projections give an exact Type-II incidence energy
decomposition, while a checkerboard proves that any one fixed binning can
miss all fine dependence.

TICKET-162는 유한 계산을 무한 결론으로 승격하지 않으면서 네 난제의
증명 탐색을 계속한다. 이번 결과는 네 개의 중간 정리다. 첫째, `H2`
유계 compact 원천 함수족은 이동하는 Fourier cutoff 사이에서 `H1`으로
수송할 수 있지만, 전체 `H1` 단위공에는 균일 투영 속도가 존재하지
않는다. 둘째, TICKET-161에서 분리한 최소 전방집중 Collatz 계열은
명시적 Matveev 임계값과 인증 연분수 열거를 결합해 모든 `m >= 2`에서
하강함을 증명했다. 동시에 이 계열의 valuation 조합 점유율이 0으로
수렴하므로 전체 Collatz 추측을 덮지 못함도 증명했다. 셋째, 정규화된
음의 오차 2차 모멘트가 1보다 작으면 모든 Goldbach 표적이 양수라는
정확한 적분성 기준을 얻었고, 상수 1이 최적임을 보였다. 넷째, 중첩
dyadic 투영으로 Type-II incidence의 정확한 에너지 분해를 얻었으며,
checkerboard 반례로 고정된 하나의 binning이 미세 상관을 완전히 놓칠
수 있음을 증명했다.

## Result ledger / 결과 원장

| Problem / 문제 | Exact result / 정확한 결과 | Status / 상태 | Decisive remaining lemma / 결정적 남은 보조정리 |
|---|---|---|---|
| Riemann / 리만 | `ResolvedH2ToH1TransportAndUniformH1BallNoGo` | RH not proved / 미증명 | `UniformFiniteGuinandWeilH1ContinuityOnResolvedCommonCore` |
| Collatz / 콜라츠 | `ExplicitMinimalFrontLoadedFamilyClosureAndCoverageNoGo` | Collatz not proved / 미증명 | `EveryNaturalOddOrbitHitsAFrontLoadedDominatingDescentPrefix` |
| Goldbach / 골드바흐 | `IntegralExceptionalSetMomentBridgeAndUnitSpikeSharpness` | Goldbach not proved / 미증명 | `UniformNormalizedNegativeMinorMomentBelowOneAfterCutoff` |
| Twin Prime / 쌍둥이 소수 | `DyadicIncidenceEnergyDecompositionAndFixedBinNoGo` | Twin Prime not proved / 미증명 | `UniformMultiscaleCenteredIncidenceCarlesonBoundWithPrimeWeights` |

## 1. Riemann hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `P_(L,N)` retain the Fourier modes `|k| <= N` on `(-L,L)`. If a
zero-extended function satisfies `f in H2`, with `f=f'=0` at its compact
support boundary, then

```text
||f - P_(L,N)f||_H1
  <= L * sqrt(||f'||_2^2 + ||f''||_2^2) / (pi*(N+1)).
```

Therefore `N/L -> infinity` transports an `H2`-bounded compact source family
in `H1`. If a family of quadratic forms additionally satisfies the uniform
continuity estimate

```text
|Q_L(u)-Q_L(v)|
  <= C (||u||_H1 + ||v||_H1) ||u-v||_H1,
```

then the form values transport as well.

`P_(L,N)`이 `(-L,L)`에서 `|k| <= N` Fourier mode만 남긴다고 하자.
compact support 경계에서 `f=f'=0`인 영 연장 함수 `f in H2`에는 위
`H1` 오차 상계가 성립한다. 따라서 `N/L -> infinity`이면 `H2` 유계
원천 함수족을 `H1`으로 수송할 수 있다. 여기에 이차형식 `Q_L`의
균일 `H1` 연속성까지 증명하면 형식 값도 함께 수송된다.

### Proof and no-go / 증명과 불가능성

Parseval bounds the `L2` tail using `f'` and the derivative tail using
`f''`; adding the two bounds proves the estimate. The condition cannot be
weakened to uniform convergence over the full `H1` unit ball. The normalized
mode `N+1` has `H1` norm one, is annihilated by `P_(L,N)`, and retains error
one for every cutoff.

Parseval 등식에서 `L2` 꼬리는 `f'`으로, 도함수 꼬리는 `f''`으로
제어된다. 두 상계를 더하면 명제가 나온다. 반면 정규화한 `N+1`번째
mode는 `H1` norm이 1이고 투영 결과가 0이므로 모든 cutoff에서 오차가
1이다. 따라서 전체 `H1` 단위공의 균일 수렴 경로는 폐기한다.

The computation uses
`f(x)=cos^2(pi*x/2)` on `[-1,1]`. Under `N=L^2`, its measured `H1`
projection error decreases from about `0.158583` at `L=2` to `0.002256` at
`L=32`. These values verify the bound; they do not verify the actual
Guinand-Weil continuity assumption.

계산에서는 `[-1,1]`의 `f(x)=cos^2(pi*x/2)`를 사용했다. `N=L^2`
schedule의 `H1` 오차는 `L=2`에서 약 `0.158583`, `L=32`에서 약
`0.002256`으로 감소한다. 이 수치는 Sobolev 상계를 검증할 뿐 실제
Guinand-Weil 형식의 균일 연속성을 검증하지 않는다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

Put

```text
alpha = log_2(3),
S_m = ceil(m*alpha),
b_m = S_m-m+1,
w_m = (b_m,1,...,1).
```

Every natural realizer of `w_m` descends for every `m >= 2`.

위와 같이 최소 수축 총 valuation `S_m`과 전방집중 word `w_m`을
정의하면, `w_m`을 실현하는 모든 자연수는 모든 `m >= 2`에서 시작값
아래로 하강한다.

### Explicit closure / 명시적 폐쇄

TICKET-161 reduced any failure to an upper continued-fraction convergent of
`alpha`. For

```text
Lambda = 2^S * 3^(-m) - 1,
```

failure implies `0 < Lambda < 2^(1-m)`. The rational Matveev specialization
gives

```text
log |Lambda| >
  -K(1+log(2m)),
K = 1.4*30^5*2^4.5*log(2)*log(3).
```

Exact rational log enclosures certify that

```text
M = 21,554,214,227
```

is the first integer satisfying the conservative Matveev separation
condition, and the condition is increasing thereafter. Below `M`, exact
atanh-series intervals certify the complete continued fraction. Only ten
primitive upper convergents with denominator at least five require testing.
The reduced denominator `q=1` cannot occur for `m>=4`: `3^3<2^5` gives
`alpha<5/3`, so `S_m<alpha*m+1<2m`, whereas an integer `S_m/m>alpha`
would have to be at least two.
The `q=5` case closes by an integer margin. Every `q>=41` case closes from

```text
p/q-alpha > 1/(q(q+q_next))
and
2^(q-2) > q+q_next.
```

If a primitive `(p,q)` descends, every admissible multiple `(kp,kq)`
descends because, for `A=2^p`, `B=3^q`, and `C=2^(p-q)`,

```text
A-B > C-1  implies  A^k-B^k > C^k-1.
```

TICKET-161은 실패가 생기면 `S_m/m`의 기약분수가 `alpha`의 상측
연분수 수렴분수여야 함을 증명했다. 이번에는 Matveev 명시 상수로
`m >= M`을 모두 배제하고, `m < M`에서는 모든 `m`을 훑지 않고 위험
가능성이 있는 원시 수렴분수 10개만 인증했다. 작은 하나는 정확한
정수 차이로, 나머지는 연속 수렴분수 분모 하계로 닫았다. 원시
경우의 하강이 모든 허용 배수로 상속됨도 위 거듭제곱 차이 항등식으로
증명했다.

### Coverage no-go / 포괄성 불가능성

At fixed length `m` and total valuation `S_m`, there are
`binom(S_m-1,m-1)` positive valuation compositions. The closed family selects
one. Its share is therefore

```text
1 / binom(S_m-1,m-1) -> 0.
```

길이 `m`, 총 valuation `S_m`인 양의 valuation word는
`binom(S_m-1,m-1)`개인데, 닫힌 계열은 그중 하나다. 따라서 이번
무한 정리는 실제로 새롭고 유효하지만, 전체 자연수 궤도 포괄성을
제공하지 않는다. 다음 증명 의무는 “모든 자연수 궤도가 이 계열 또는
그보다 강한 하강 prefix에 도달한다”는 전이 정리다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

For a finite target set `A`, let `G_N` be nonnegative integer representation
counts, `M_N>0`, and `G_N=M_N+E_N`. Then

```text
#{N in A : G_N=0}
  <= sum_(N in A) (E_N^-/M_N)^2.
```

Thus a total normalized negative-error budget strictly below one proves
`G_N>0` for every target in `A`.

유한 표적 집합 `A`에서 `G_N`을 음이 아닌 정수 표현 개수,
`M_N>0`, `G_N=M_N+E_N`이라 하자. 표현이 0인 표적에서는 반드시
`E_N=-M_N`이므로 해당 정규화 항이 정확히 1이다. 따라서 정규화된
음의 오차 예산 총합이 1보다 작으면 모든 표적에 Goldbach 표현이
존재한다.

### Sharpness and finite audit / 최적성과 유한 감사

The constant one is sharp: one target with `(M,E,G)=(1,-1,0)` has budget
exactly one. Hence an `L2` or average estimate whose normalized total remains
at least one cannot exclude a single exceptional even integer.

상수 1은 최적이다. 한 표적에서 `(M,E,G)=(1,-1,0)`이면 예산이
정확히 1이다. 그러므로 정규화 총합이 1 이상인 평균 또는 `L2`
추정만으로는 단 하나의 예외도 배제할 수 없다.

The reproducible prime DFT audit uses one finite Farey mask through
`N=16,000`. Its budgets grow from approximately `7.13` to `135.36`; all
finite representation counts are positive, but the analytic gate fails at
every tested scale. The direct counts are evidence, not a proof of the
unbounded statement.

재현 계산은 `N=16,000`까지 하나의 유한 Farey mask를 사용한다.
예산은 약 `7.13`에서 `135.36`으로 증가한다. 유한 범위의 실제 표현
개수는 모두 양수지만 분석적 `<1` gate는 한 번도 통과하지 못한다.
직접 계산은 무한 명제의 증명이 아니다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

Let `P_j` be Frobenius-orthogonal projections of a centered incidence matrix
`H` onto nested dyadic blocks with `2^j` bins per axis. Then

```text
||P_J H||_F^2
 = ||P_0 H||_F^2
   + sum_(j=1)^J ||P_j H-P_(j-1)H||_F^2.
```

중심화 incidence 행렬 `H`를 축마다 `2^j`개인 중첩 dyadic block에
투영한 것을 `P_j H`라 하면 위 Pythagorean 에너지 분해가 정확히
성립한다. 각 차이 항은 해당 scale에서 새로 드러난 상관 에너지다.

### Fixed-bin no-go / 고정 bin 불가능성

The alternating `4x4` checkerboard has zero row and column margins, zero
projection onto the coarse `2x2` block partition, and fine energy `16`.
Therefore small centered energy at one fixed resolution says nothing about
unresolved finer scales.

교대 부호 `4x4` checkerboard는 모든 행·열 합이 0이고, 거친 `2x2`
block 투영도 0이지만, 미세 에너지는 `16`이다. 따라서 하나의 고정
해상도에서 중심화 에너지가 작다는 사실만으로 더 미세한 Type-II
상관을 배제할 수 없다.

The finite cubic-rough audit computes exact `16x16` incidence matrices at
`100K`, `1M`, and `10M`, with `284`, `2,453`, and `19,074`
double-semiprime pairs. Every dyadic energy telescopes exactly. These finite
profiles do not establish a uniform Carleson estimate or construct
prime-producing weights.

유한 cubic-rough 감사는 `100K`, `1M`, `10M`에서 정확한 `16x16`
incidence 행렬을 계산하며 이중 semiprime pair는 각각 `284`,
`2,453`, `19,074`개다. 모든 dyadic 에너지는 정확히 telescoping
된다. 그러나 이 유한 profile은 균일 Carleson 상계도, 실제
prime-producing weight도 제공하지 않는다.

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket162_formnorm_explicitbaker_integral_multiscale.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket162_formnorm_explicitbaker_integral_multiscale
```

The generator writes one global JSON and four per-problem JSON files under
`data/open-problem/`. Every proof DAG has exactly three states:
`refuted_or_insufficient`, `proved_exact`, and `open_not_proven`.

생성기는 `data/open-problem/` 아래에 전체 JSON 하나와 문제별 JSON
네 개를 기록한다. 각 proof DAG는 `폐기 또는 불충분`, `정확히
증명됨`, `아직 미증명`의 세 상태를 강제로 구분한다.

## Literature boundary / 문헌 경계

- E. M. Matveev, “An explicit lower bound for a homogeneous rational linear
  form in logarithms of algebraic numbers,” *Izvestiya: Mathematics* 62
  (1998), 723-772. <https://doi.org/10.1070/im1998v062n04ABEH000190>
- A. Groskin, “A finite Guinand-Weil dictionary and archimedean tail order
  for the truncated Weil quadratic form” (2026).
  <https://arxiv.org/abs/2607.02828>
- H. Li, “The exceptional set of Goldbach numbers (II),” *Acta
  Arithmetica* 92 (2000), 71-88.
  <https://eudml.org/doc/207380>
- K. Ford and J. Maynard, “On the theory of prime producing sieves”
  (2024/2026). <https://arxiv.org/abs/2407.14368>

These sources provide external theorems or motivation. They do not establish
the four next lemmas named in this document. / 이 문헌들은 외부 입력
정리 또는 연구 동기를 제공할 뿐, 이 문서가 지정한 네 개의 다음
보조정리를 증명하지 않는다.
