# TICKET-125: Infinite Bridge Contracts

## 1. Claim boundary

TICKET-125 does not prove or refute the Riemann Hypothesis, the Collatz
conjecture, the strong Goldbach conjecture, or the Twin Prime conjecture. It
proves four conditional bridge lemmas, constructs exact countermodels to
weaker versions, and turns each missing infinite step into a falsifiable
mathematical contract.

TICKET-125는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 증명하거나 반증하지 않는다. 이번 단계에서 증명한 것은 네 개의
조건부 연결 정리다. 약한 전제의 논리적 실패를 보이는 정확한 반례도 함께
제시하여, 각 난제에서 여전히 필요한 무한 단계가 무엇인지 검증 가능한
계약으로 바꾼다.

The distinction is essential:

1. a bridge theorem proves that explicit premises imply the conjecture;
2. a complete proof must additionally prove every premise without assuming an
   equivalent form of the conjecture;
3. finite experiments may test a premise candidate but cannot quantify over the
   unobserved tail.

이 구분이 핵심이다. 연결 정리는 명시된 전제가 난제를 함의한다는 뜻이다.
완전 증명을 위해서는 그 전제를 난제의 동치 명제를 몰래 사용하지 않고 따로
증명해야 한다. 유한 실험은 전제 후보를 반증할 수 있지만, 보지 않은 무한
꼬리 구간을 증명하지는 못한다.

## 2. Riemann Hypothesis: continuous dense-cone extension

Let `V` be a completed test-function space for an exact RH-equivalent Weil
positivity criterion, let `C` be a dense cone in `V`, and let `H:V->R` be the
associated continuous quadratic form.

### Theorem RH-125

If `H(c)>=0` for every `c in C`, then `H(v)>=0` for every `v in V`.

### Proof

For arbitrary `v in V`, density gives a sequence `c_n in C` with `c_n -> v`.
Continuity gives

```text
H(v) = lim_(n->infinity) H(c_n) >= 0.
```

This proves the extension lemma. It does not prove any of the three
problem-specific premises: the exact topology and RH equivalence, density of a
concrete arithmetic cone, or non-circular positivity on that cone.

한국어 해설: 정확히 RH와 동치인 완비 시험함수 공간 `V`, 그 안에서 조밀한
원뿔 `C`, 연속 이차형식 `H`가 있고 `C` 전체에서 양성을 증명했다면, 극한을
취해 `V` 전체의 양성이 따라온다. 그러나 PrimeProject는 아직 실제 제타
명시공식에 대해 이 세 전제를 증명하지 않았다.

### Exact no-go models

- **No density:** `H(x,y)=x^2-y^2` is nonnegative on the x-axis but
  `H(0,1)=-1`.
- **No continuity:** choose a discontinuous Hamel-linear functional `L` with
  dense kernel and set `H=-L^2`. Then `H=0` on a dense set but is negative
  elsewhere.
- **Finite Gram checks:** on `R^(m+1)`, set
  `H_m(x)=sum_(j<=m)x_j^2-x_(m+1)^2`. Every checked direction in the first
  `m` coordinates is positive, while the first unseen direction has value
  `-1`.

따라서 유한 영점 표본, 유한 Gram 행렬, 조밀성이 증명되지 않은 작은 커널
족, 연속성이 없는 극한 논증은 모두 폐기한다. 다음 목표
`AdmissibleKernelConeDensityAndPositivity`는 네 조건을 같은 정확한 공간에서
동시에 증명해야 한다.

## 3. Collatz: adaptive residue finite-stopping cover

Let `T` denote the usual Collatz map. The following criterion is exact.

### Theorem CO-125A

Assuming the standard `1 -> 4 -> 2 -> 1` basin, Collatz holds if and only if
every integer `n>1` has a finite iterate below `n`.

### Proof

The forward implication is immediate because a convergent orbit reaches `1`.
For the reverse implication, use strong induction. A finite iterate of `n`
equals some `m<n`; by induction `m` reaches `1`, hence so does `n`.

한국어 해설: 모든 수가 언젠가 자기보다 작은 수로 내려간다는 명제만
증명하면 강한 귀납법으로 콜라츠가 따라온다. 평균적 감소나 밀도 1 감소가
아니라 **모든 양의 정수**에 대한 유한 하강이 필요하다.

### Theorem CO-125B: exact lifted-cylinder certificate

For an odd residue `r modulo 2^k`, write every lift as
`n=r+2^k t`, `t>=0`. Suppose the first `m` accelerated odd steps consume total
2-adic valuation `S<k`. Then the valuation word is fixed throughout the
cylinder and

```text
T_odd^m(r+2^k t)
  = T_odd^m(r) + 3^m 2^(k-S) t.
```

If `T_odd^m(r)<r`, positivity of the affine constant implies `3^m<2^S`.
Both the intercept and slope are then smaller than those of `r+2^k t`, so
every lift in the infinite cylinder strictly descends.

이 식은 대표값 하나가 아니라 그 잉여류에 속하는 무한히 많은 양의 정수
전체를 동시에 인증한다. `k=18` 전수 감사 결과는 다음과 같다.

| Quantity | Exact value |
| --- | ---: |
| Odd residue classes modulo `2^18` | 131,072 |
| Uniformly descending cylinders | 121,825 |
| Unresolved cylinders | 9,247 |
| Certified fraction | 0.9294509888 |
| Lift replay failures | 0 |

This is stronger than checking 121,825 individual integers: each certificate
covers infinitely many lifts. It is still incomplete because 9,247 cylinders
remain.

### Fixed-precision boundary

For every `k`, the odd residue

```text
r_k = -3^(-1) mod 2^k
```

satisfies `v_2(3r_k+1)>=k`. Therefore `k` bits do not determine even its first
accelerated valuation. The determined-word method has at least one refinement
boundary at every fixed precision.

이 경계는 고정 정밀도 방식의 완전성을 반박하지만, 모든 유한 모듈러
접근법을 반박하는 것은 아니다. 올바른 다음 목표는 고정 분할이 아니라
`AdaptiveResidueFiniteStoppingCover`: 미해결 원통만 재귀적으로 세분하면서
모든 양의 정수 가지가 유한 단계 안에 하강 인증서를 받는다는 정리다.

An almost-all theorem cannot replace this target. The artificial map
`F(2^j)=2^(j+1)` and `F(n)=1` off the powers of two has a density-one convergent
set and one sparse divergent chain.

## 4. Goldbach: explicit weighted finite glue

For even `N`, define

```text
G(N) = sum_(m=2)^(N-2) Lambda(m)Lambda(N-m).
```

Let `P(N)` be the nonnegative part in which at least one summand is a proper
prime power. Then `G(N)-P(N)>0` forces an actual prime-prime representation.

### Theorem GB-125

Let `H=4*10^18`. Suppose explicit constants `A>0`, `K>=0`, and `B>=0` satisfy,
for every even `N>H`,

```text
G(N) >= A N - K N/log N,
P(N) <= B sqrt(N) log(N)^2,
A - K/log H - B log(H)^2/sqrt(H) > 0.
```

Then every even `N>2` is a sum of two primes, using the published verification
through `H` for the finite portion.

### Proof

For `N>=H>e^4`, both `1/log N` and `log(N)^2/sqrt(N)` decrease. Hence the
strict endpoint inequality implies

```text
G(N)-P(N)
 >= N[A-K/log N-B log(N)^2/sqrt(N)]
 > 0
```

throughout the analytic tail. The finite and analytic ranges overlap at `H`.

한국어 해설: `4*10^18`까지의 계산을 무한 증명과 연결하려면, 계산 범위보다
큰 모든 짝수에서 주항이 Vaughan 잔차와 진짜 소수가 아닌 소수멱 항을
이겨야 한다. 끝점 `H`에서 한 번 엄격히 양수이고 두 오차 비율이 이후
단조감소하면 전체 꼬리가 닫힌다.

Numerically,

```text
log H = 42.8328260350,
log(H)^2/sqrt(H) = 9.1732549307e-7.
```

After normalizing `A=1`, a residual target `K=40` permits only
`B<72097.4182`. This is a target budget, not a proved estimate. The missing
work is to derive sourced, uniform, replayable `A`, `K`, and `B` from the
actual major term, joint signed Vaughan residual, and prime-power count.

## 5. Twin Prime: dyadic obstruction contraction

TICKET-124 defined the exact route obstruction

```text
Q_X = ((S_X-D_X)+E_X)/K_X.
```

### Theorem TP-125

If, for every sufficiently large dyadic `X`,

```text
Q_(2X) <= alpha Q_X + beta,
0 <= alpha < 1,
alpha + beta < 1,
```

then

```text
limsup_(dyadic X) Q_X <= beta/(1-alpha) < 1.
```

### Proof

Iterating the affine recurrence gives

```text
Q_n <= alpha^j Q_(n-j) + beta(1-alpha^j)/(1-alpha).
```

The geometric term vanishes as `j` grows, leaving the fixed point
`beta/(1-alpha)`.

The frozen finite candidate is

```text
alpha = 3/4,
beta  = 23/100,
conditional limsup ceiling = 0.92,
conditional fixed margin   = 0.08.
```

All four available dyadic transitions from 1M through 16M pass, and the
largest certificate residual is `0.2203867095`, leaving finite slack
`0.0096132905`. The constants were selected from this same finite tail. There
is no unseen holdout and no uniform arithmetic proof.

한국어 해설: 이 수축 정리가 실제 Vaughan 계수에서 모든 충분히 큰 dyadic
규모에 대해 성립한다면 TICKET-124의 limsup 목표를 닫을 수 있다. 그러나
현재 네 전이는 후보를 만든 학습 자료일 뿐이다. 다음 32M 계산은 오직
사전등록된 반증용 holdout이며, 통과해도 무한 증명은 아니다.

Strictness is exact. At `beta=1-alpha`, the sequence `Q_n=1-1/n` can satisfy
the endpoint recurrence eventually while tending to one. Also, any finite
passing recurrence prefix can be followed by a failing unseen value.

Finally, dyadic control alone does not control every `X`. A complete route must
also prove a between-scale envelope on each interval `[2^n,2^(n+1))`, preserve
the actual Vaughan coefficient identities, survive the parity barrier, and
transfer positive route margin to exact gap two.

## 6. What is kept, discarded, and next

| Problem | Keep | Discard | TICKET-126 target |
| --- | --- | --- | --- |
| RH | continuous dense-cone extension | finite Gram or sampled-zero positivity | `AdmissibleKernelConeDensityAndPositivity` |
| Collatz | exact lifted cylinders and strong-induction descent | fixed-precision completeness and almost-all substitution | `AdaptiveResidueFiniteStoppingCover` |
| Goldbach | explicit weighted endpoint budget | invoking `4e18` without an analytic overlap | `ExplicitJointBalancedGoldbachCutoff` |
| Twin Prime | strict affine dyadic contraction | finite recurrence extrapolation and endpoint `alpha+beta=1` | `DyadicVaughanObstructionContractionAndInterpolation` |

## 7. Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket125_infinite_bridge_contracts.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket125_infinite_bridge_contracts
```

Machine-readable artifacts:

- `data/open-problem/ticket125-infinite-bridge-contracts.json`
- `data/open-problem/riemann/rh-ticket-125-density-positivity-extension.json`
- `data/open-problem/collatz/co-ticket-125-adaptive-residue-descent-cover.json`
- `data/open-problem/goldbach/gb-ticket-125-explicit-cutoff-budget.json`
- `data/open-problem/twin-prime/tp-ticket-125-dyadic-obstruction-contraction.json`

## 8. Literature boundary

- Connes and Consani, *The Scaling Hamiltonian*,
  <https://arxiv.org/abs/1910.14368>.
- Tao, *Almost all orbits of the Collatz map attain almost bounded values*,
  <https://arxiv.org/abs/1909.03562>.
- Oliveira e Silva, Herzog, and Pardi, *Empirical verification of the even
  Goldbach conjecture and computation of prime gaps up to `4*10^18`*,
  <https://doi.org/10.1090/S0025-5718-2013-02787-1>.
- Ford and Maynard, *On the theory of prime producing sieves*,
  <https://arxiv.org/abs/2407.14368>.

The established criteria, finite verification, and sieve frameworks are not
claimed as new. PrimeProject's contribution in this ticket is the integrated
four-problem contract, exact route countermodels, reproducible Collatz cylinder
frontier, explicit Goldbach endpoint budget, and the frozen Twin contraction
target with its selection boundary.

기존 문헌의 정리와 계산을 새 결과라고 주장하지 않는다. 이 티켓의 기여는
네 문제의 무한 연결 조건을 한 형식으로 통합하고, 약한 연결의 반례를
명시하며, 재현 가능한 Collatz 원통 경계·Goldbach 끝점 예산·Twin 수축
후보를 주장 경계와 함께 제공한 것이다.
