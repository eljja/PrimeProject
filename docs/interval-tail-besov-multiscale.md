# TICKET-170: interval gaps, Collatz tail closure, autocorrelation Besov control, and multiscale Type II

한국어 제목: **구간 KKT 간극, 콜라츠 꼬리 폐쇄, 자기상관 베소프 제어, 다중스케일 Type-II**

Status / 상태: `open_not_proven` for all four conjectures / 네 추측 모두 미해결

Generated / 생성: 2026-08-03 (Asia/Seoul)

## Abstract / 초록

TICKET-170 continues the four proof searches from the exact bridges of
TICKET-169. It proves four scale- or resolution-sensitive statements and
rejects four insufficient proof targets. It does **not** prove or disprove any
parent conjecture.

For the Riemann track, a spectral-gap criterion converts interval KKT errors
into a rigorous inertia certificate. A rank-one family proves that entrywise
interval radii tending to zero do not suffice when dimension grows. For
Collatz, every finite prefix has a computable valuation threshold beyond which
all children descend. The all-one prefix family proves that these thresholds
cannot be replaced by one global threshold guaranteeing immediate child
descent. For Goldbach, the full
autocorrelation certificate is decomposed into dyadic shell `L2` budgets. An
exact cosine pair proves that no fixed lag window controls pointwise size. For
Twin Prime, the centered spectral norm is identified with the worst `L2`
bilinear test, but an embedded checkerboard proves that a fixed coarse
partition can hide nonzero fine Type-II dependence completely.

TICKET-170은 TICKET-169가 만든 정확한 연결 정리에서 출발해 네 증명 경로의
스케일 문제를 검사한다. 네 개의 정확한 정리 또는 no-go를 증명하지만 상위
추측은 하나도 증명하거나 반증하지 않는다.

리만 트랙에서는 KKT 근사행렬의 스펙트럼 간극보다 구간 오차의 연산자 노름이
작으면 관성이 보존됨을 사용한다. 각 원소 오차가 0으로 가는 것만으로는 차원이
커질 때 충분하지 않다는 rank-one 반례도 준다. 콜라츠 트랙에서는 임의의 유한
접두어마다 충분히 큰 valuation을 붙인 모든 자식이 하강한다는 유효 임계값을
구한다. 그러나 `1^m` 접두어에서 이 임계값이 무한히 증가하므로 전역 고정
상한은 불가능하다. 골드바흐 트랙에서는 자기상관을 dyadic shell별 `L2` 예산으로
바꾸고, 고정 lag 창이 고주파 점별 spike를 놓친다는 정확한 반례를 제시한다.
쌍둥이 소수 트랙에서는 고정된 coarse partition이 fine Type-II 의존성을 완전히
숨길 수 있음을 보인다.

## Result ledger / 결과 원장

| Problem / 문제 | New exact result / 새 정확한 결과 | Resolution / 해결 | Decisive next lemma / 다음 핵심 보조정리 |
|---|---|---|---|
| Riemann / 리만 | `IntervalKKTGapStabilityAndVanishingEntrywiseRadiusNoGo` | open / 미해결 | `CofinalDimensionScaledIntervalKKTErrorBelowCertifiedSpectralGapOnFixedWeilCore` |
| Collatz / 콜라츠 | `PrefixwiseFiniteChildTailDescentAndGlobalImmediateDescentThresholdNoGo` | open / 미해결 | `WellFoundednessOfExactNonDescendingChildTreeAfterAnalyticTailClosure` |
| Goldbach / 골드바흐 | `AutocorrelationBesovPointwiseBridgeAndFixedLagWindowNoGo` | open / 미해결 | `UniformBinaryGoldbachAutocorrelationBesovOneBudgetBelowAnchorMargin` |
| Twin Prime / 쌍둥이 소수 | `TypeIISpectralBilinearBridgeAndFixedPartitionInvisibilityNoGo` | open / 미해결 | `UniformMultiscaleCubicRoughTypeIISpectralDecayWithPrimeProducingConstants` |

## Shared diagnosis / 공통 진단

All four tracks now exhibit the same quantifier failure:

```text
local accuracy or finite resolution
    does not imply
uniform control along a cofinal or infinite family.
```

구체적으로 원소별 KKT 오차, 접두어별 유한 분기, 고정 자기상관 lag 창, 고정
인수 bin은 각각 한 유한 단계에서는 유용하다. 그러나 전역 명제를 얻으려면
차원, 깊이, 주파수, partition 해상도에 대해 균일한 추정이 별도로 필요하다.
이 공통 구조는 비유가 아니라 아래 네 no-go 정리가 각각 정확히 보이는 논리적
경계다.

## 1. Riemann hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `K_tilde` be a real symmetric approximation and put

```text
gamma = min_j |lambda_j(K_tilde)| > 0.
```

If `K=K_tilde+E` is symmetric and

```text
||E||_2 < gamma,                              (1)
```

then `K` and `K_tilde` have the same inertia. If interval arithmetic gives
entry radii `r_ij`, the computable condition

```text
sqrt(sum_ij r_ij^2) < gamma                   (2)
```

is sufficient because the Frobenius norm dominates the operator norm.

`K_tilde`의 모든 고유값이 0에서 `gamma` 이상 떨어져 있고 실제 행렬과의
오차 연산자 노름이 `gamma`보다 작으면 양, 음, 영 고유값 개수는 변하지 않는다.
구간 계산에서는 식 (2)가 보수적이지만 직접 검증 가능한 충분조건이다.

### Proof / 증명

Weyl's inequality gives

```text
|lambda_j(K)-lambda_j(K_tilde)| <= ||E||_2.
```

Under (1), no eigenvalue reaches zero, so no inertia count changes. Condition
(2) implies (1) because `||E||_2<=||E||_F` and every admissible interval error
has `||E||_F<=sqrt(sum r_ij^2)`.

### Entrywise no-go / 원소별 수렴 no-go

Consider the canonical inertia proxy

```text
K_tilde_n = diag(I_n,-I_r)
```

and perturb its positive block by

```text
E_n = -(2/n) J_n.
```

Every entry has size `2/n -> 0`. Nevertheless, `J_n` has one eigenvalue `n`,
so `I_n-(2/n)J_n` has eigenvalues `-1,1,...,1`. The inertia changes from
`(n,r,0)` to `(n-1,r+1,0)`. In contrast, `-(1/(2n))J_n` has operator norm
`1/2<gamma=1` and preserves inertia.

따라서 “모든 구간 원소 폭이 0으로 간다”는 사실만으로는 cofinal KKT 관성을
인증할 수 없다. 필요한 것은 차원을 포함한 연산자 또는 Frobenius 오차가 실제
스펙트럼 간극보다 작다는 인증이다.

### Computation and limit / 계산과 한계

Exact rows use `n=4,8,16,32,64,128`, `r=2`. The stable radius is exactly
`1/2`; the unstable entry radius decreases from `1/2` to `1/64`, while its
operator radius stays exactly `2` and flips one direction in every row.

이 반례는 KKT 관성의 canonical 좌표에서 정확하다. 실제 Guinand-Weil basis로
옮길 때 congruence의 condition number가 원소별 오차를 증폭할 수 있으므로,
실제 다음 보조정리는 고정된 pole-neutral core에서 basis와 interval enclosure를
함께 명시해야 한다. RH의 영점이 임계선 밖에 없다는 결론은 아직 전혀 얻지
못했다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

Let a finite accelerated prefix have affine data `(m,S,C)`, least natural
realizer `n_0`, and append valuation `a`. TICKET-169 proved that the child has

```text
C' = 3C + 2^S,
D'_a = 2^(S+a)-3^(m+1),
```

and that every child realizer `n'` satisfies `n'>=n_0`. Define `A(w)` as the
least positive integer satisfying

```text
n_0 D'_A > C'.                               (3)
```

Then every child with `a>=A(w)` strictly descends in the appended accelerated
step. Hence each prefix has only finitely many child valuations not closed by
this argument.

### Proof / 증명

The child endpoint is

```text
u' = (3^(m+1)n' + C') / 2^(S+a).
```

Therefore `u'<n'` is equivalent to `n'D'_a>C'`. For `a>=A(w)`, `D'_a` is
positive and increasing, and `n'>=n_0`; (3) gives the desired strict
inequality. Existence and effective computability of `A(w)` follow from the
exponential growth of `2^(S+a)`.

즉 한 접두어 아래 무한히 많은 valuation 자식 전체를 열거할 필요가 없다.
임계값 이상의 무한 꼬리는 하나의 부등식으로 동시에 닫히고, 작은 valuation
자식만 유한하게 남는다.

### Global one-step threshold no-go / 전역 한 단계 임계값 no-go

For the all-one word `w=1^m`, exact induction gives

```text
S=m,
C=3^m-2^m,
n_0=2^(m+1)-1.
```

Before (3) can hold, its denominator gap must be positive:

```text
2^(m+a) > 3^(m+1).                            (4)
```

For fixed `a`, the ratio of the two sides is

```text
(2^a/3)(2/3)^m -> 0.
```

Thus no fixed appended-valuation threshold makes this immediate one-step
descent argument work for every prefix. Exact thresholds
for `m=1,2,4,8,16,32,64` are

```text
3, 3, 4, 7, 11, 21, 40.
```

### Computation and limit / 계산과 한계

Eight mixed prefix words were audited. For each, the least threshold and the
next five child valuations have exact positive descent slack. This verifies
the implementation but is not needed for the general proof.

이 결과는 여러 단계를 묶는 다른 전역 귀납법까지 배제하지 않는다. 접두어별로
남은 자식 수가 유한하다는 사실만으로 무한 트리가 끝난다고 결론낼
수는 없다. 깊이가 증가하면서 각 노드의 유한한 위험 자식이 계속 이어질 수
있다. 다음 보조정리는 tail closure 이후 남는 정확한 non-descending child tree가
well-founded임을 보이거나, 그렇지 않다면 무한 경로 또는 주기 반례를 구성해야
한다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

On a cycle of length `L`, let `G_h` be the discrete Fourier coefficients of
`|f|^2`. Partition cyclic lags into dyadic shells `S_j`. Fourier inversion and
shellwise Cauchy-Schwarz give

```text
||f||_infinity^2
  <= L^(-1) sum_h |G_h|
  <= L^(-1) sum_j |S_j|^(1/2)
                   (sum_(h in S_j) |G_h|^2)^(1/2).     (5)
```

Taking square roots produces the autocorrelation Besov shell certificate.

TICKET-169의 전체 자기상관 `l1` 상계는 위상 정보를 보존하지만 모든 lag를
직접 더해야 했다. 식 (5)는 이를 dyadic shell별 `L2` 추정으로 환원한다. 따라서
산술적 exponential-sum 도구가 shell 에너지를 균일하게 제어할 수 있다면
점별 Goldbach deficit으로 연결할 수 있다.

### Proof / 증명

The first inequality is the triangle inequality applied to Fourier inversion
of `|f|^2`. On each shell,

```text
sum_(h in S_j)|G_h|
  <= |S_j|^(1/2)(sum_(h in S_j)|G_h|^2)^(1/2),
```

which proves (5).

### Fixed-window no-go / 고정 lag 창 no-go

Fix `H` and choose `q=H+1` with `q<L/2`. Define nonnegative squared signals

```text
|f_0(x)|^2 = 1,
|f_1(x)|^2 = 1 + cos(2 pi qx/L).
```

Their normalized Fourier coefficients agree at every `|h|<=H`: both have
mean one and every retained nonzero coefficient is zero. But

```text
||f_0||_infinity^2 = 1,
||f_1||_infinity^2 = 2.
```

The second signal hides coefficients `1/2` at lags `+q` and `-q`. Therefore no
fixed autocorrelation window controls every pointwise deficit.

### Computation and limit / 계산과 한계

For the repository's `L=16,384` deficit proxy, the shell bounds at bandwidths
`16,64,256,1024,4096` are

```text
0.47257, 0.46790, 0.46655, 0.46778, 0.41663.
```

They dominate the exact autocorrelation bounds and observed tails and are all
below one. 그러나 이 수치는 하나의 유한 sequence에 대한 진단이다. 강한
골드바흐 추측에는 target 크기에 균일한 shell 예산, independently proved
low-frequency positive anchor, 그리고 두 양의 margin 사이의 엄밀한 비교가
필요하다. 고정된 lag 수나 고정된 계산 범위는 이를 대신하지 못한다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

For a joint count matrix `C` with total `T`, row margins `r`, and column
margins `c`, define the centered numerator

```text
H = T C - r c^T.
```

Then

```text
||H||_2/T^2
  = sup_(||u||_2=||v||_2=1) |u^T H v|/T^2.    (6)
```

For four-bin sign vectors, `||u||_2=||v||_2=2`, so every normalized sign
deviation is at most `4||H||_2/T^2`.

식 (6)은 centered incidence spectral norm이 단순 시각화 지표가 아니라
해당 partition에서 가장 큰 `L2` bilinear dependence임을 정확히 말한다.

### Fixed-partition invisibility no-go / 고정 partition 비가시성 no-go

Suppose one coarse cell contains at least two fine rows and two fine columns.
Embed

```text
[[ a,-a],
 [-a, a]]
```

inside that cell and put zero elsewhere. Every fine row and column margin is
zero, and the sum over every coarse block is zero. Thus the coarse centered
matrix and its spectral norm are zero. The fine matrix nevertheless has top
singular value `2a` and sign witness `4a`.

따라서 TICKET-161의 고정 4-bin spectral ratio가 감소한다는 사실만으로는
실제 Type-II 의존성이 감소한다고 결론낼 수 없다. 더 미세한 인수 스케일에서
coarse bin이 보지 못하는 checkerboard 상관이 남을 수 있다.

### Computation and limit / 계산과 한계

The exact sign search on TICKET-161's four finite matrices gives normalized
maximal sign deviations

```text
0.28408, 0.14313, 0.05066, 0.04369
```

at `X=10^4,10^5,10^6,10^7`; each satisfies its spectral bound. These are
finite factorization diagnostics, not an asymptotic theorem.

다음 보조정리는 해상도가 증가하는 partition 계열을 명시하고 모든 관련
bilinear test에 균일한 decay를 증명해야 한다. 그 상수는 실제 prime-producing
sieve의 양의 하한에 충분해야 한다. 이 조건 없이 고정 bin 추세를 외삽하는
경로는 폐기한다.

## Proof DAG / 증명 DAG

```text
Riemann:
  vanishing entrywise intervals preserve cofinal KKT inertia [REFUTED]
    -> gap-relative operator-norm inertia certificate [PROVED]
    -> dimension-scaled interval error below the Weil-core gap [OPEN]

Collatz:
  one global threshold forces immediate child descent at every prefix [REFUTED]
    -> every prefix has an analytically closed large-valuation tail [PROVED]
    -> residual non-descending child tree is well founded [OPEN]

Goldbach:
  one fixed autocorrelation lag window controls pointwise deficit [REFUTED]
    -> dyadic autocorrelation Besov pointwise bridge [PROVED]
    -> uniform arithmetic shell budget below anchor margin [OPEN]

Twin Prime:
  one fixed coarse partition controls all Type-II dependence [REFUTED]
    -> spectral bilinear bridge plus exact invisibility family [PROVED]
    -> uniform multiscale Type-II decay with sieve constants [OPEN]
```

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket170_interval_tail_besov_multiscale.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket170_interval_tail_besov_multiscale -v
```

Machine-readable artifacts / 기계 판독 결과:

```text
data/open-problem/ticket170-interval-tail-besov-multiscale.json
data/open-problem/riemann/rh-ticket-170-interval-gap.json
data/open-problem/collatz/co-ticket-170-child-tail.json
data/open-problem/goldbach/gb-ticket-170-autocorrelation-besov.json
data/open-problem/twin-prime/tp-ticket-170-multiscale-typeii.json
```

## Literature boundary / 문헌 경계

- Riemann: [arXiv:2607.02828](https://arxiv.org/abs/2607.02828) provides a
  finite Guinand-Weil and interval-LDL context. The gap-relative KKT theorem
  here is project-local and does not exclude off-critical zeros.
- Collatz: [Rozier-Terracol, arXiv:2502.00948](https://arxiv.org/abs/2502.00948)
  studies finite parity-vector phenomena. It does not prove well-foundedness
  of PrimeProject's residual child tree.
- Goldbach: [arXiv:2607.27282](https://arxiv.org/abs/2607.27282) gives
  exceptional-set and major-arc context, not the uniform autocorrelation
  Besov budget required here.
- Twin Prime: [Ford-Maynard, arXiv:2407.14368](https://arxiv.org/abs/2407.14368)
  identifies substantial Type-II information in a broad prime-producing sieve
  framework. TICKET-170 proves no such asymptotic estimate.

These citations delimit context; they do not establish academic novelty of
the elementary bridge and no-go statements in this ticket.

위 문헌은 연구 맥락과 남은 병목을 구분하기 위한 것이다. 이번 ticket의
초등적 bridge/no-go가 학계 최초라는 주장은 하지 않는다.

## Claim boundary / 주장 경계

No proof or counterexample is claimed for the Riemann hypothesis, Collatz
conjecture, strong Goldbach conjecture, or Twin Prime conjecture. The machine
field `conjecture_resolution_count` is exactly zero. Finite calculations check
implementations and measure candidate inequalities; they do not establish an
infinite statement.

리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
해결했다고 주장하지 않는다. 반례도 발견하지 않았다. 기계 판독 필드
`conjecture_resolution_count`는 정확히 0이다. 이번에 확정된 내용은 위 네
정확한 정리/no-go와 재현 가능한 유한 진단으로 제한된다.
strictly descends after the appended accelerated step. Hence each prefix has
only finitely many child valuations not closed by this argument.
