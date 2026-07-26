# TICKET-150: Relative Form Bounds, Delayed Collatz Escape, Sharp Endpoint Holes, and Parity Equivalence

> Continued by
> [TICKET-151: Negative Spectrum, Affine Thresholds, Reflection Transversals,
> and the Log-Two Bias](negative-affine-transversal-logtwo.md). TICKET-151
> tightens each next lemma while keeping all four conjectures open.
>
> 후속 연구는
> [TICKET-151: 음의 스펙트럼, affine 임계값, 반사 transversal,
> log-two 편향](negative-affine-transversal-logtwo.md)이다. 네 다음
> 보조정리를 더 정확히 수정했으며, 네 난제는 여전히 모두 미해결이다.

**Status:** four exact intermediate or no-go theorems; all four conjectures
remain open.

**상태:** 네 개의 정확한 중간 정리 또는 no-go 정리만 확립했다. 네 난제는
모두 미해결이다.

## Abstract / 초록

**English.** TICKET-150 attacks the four open nodes left by TICKET-149. For
the Riemann hypothesis it proves the sharp abstract relative-form threshold
and corrects an impossible ambient-coercivity requirement: a positive compact
reference cannot be uniformly coercive on an infinite-dimensional ambient
Hilbert space. For Collatz it separates the three exact exits from the
`-5` shadow. Exit types `r=1` and `r=3` contract locally, but the `r=2` type
admits an arbitrarily long post-exit valuation-one expansion forced by the
Chinese remainder theorem. For strong Goldbach it computes the exact
nonnegative `L2` distance from a squarefree-wheel baseline to an endpoint
hole, and proves that the relative sharp radius tends to zero along primorial
wheels. For Twin Prime it proves that the proposed semiprime-cover deficit is
exactly `twin edges - double-semiprime edges`, so it is a parity-sensitive
comparison rather than an unsigned shortcut. None of these statements proves
or disproves a target conjecture.

**한국어.** TICKET-150은 TICKET-149가 남긴 네 열린 노드를 직접 공격한다.
리만 가설에서는 추상 이차형식의 상대 perturbation 임계값을 정확히
증명하고, 무한차원 공간에서 양의 compact 기준 작용소가 ambient norm에
대해 균일 coercive일 수 없음을 보인다. 콜라츠에서는 `-5` shadow의 세
종료형을 분리한다. `r=1`, `r=3`은 종료점보다 국소적으로 내려가지만,
`r=2`에서는 중국인의 나머지 정리로 종료 후 임의로 긴 valuation-one
팽창을 강제할 수 있다. 강한 골드바흐에서는 squarefree wheel 기준에서
특정 endpoint를 잃는 비음수 가중치까지의 정확한 `L2` 거리를 계산하고,
primorial wheel을 키우면 그 상대 반지름이 0으로 감을 증명한다. 쌍둥이
소수에서는 semiprime cover deficit가 정확히
`쌍둥이 간선 수 - 양끝 semiprime 간선 수`임을 증명한다. 따라서 이는
부호 없는 우회로가 아니라 parity-sensitive 비교이다. 어느 결과도 네
난제의 증명이나 반증이 아니다.

## 1. Result ledger / 결과 원장

| Problem / 문제 | Exact TICKET-150 result / 정확한 결과 | Rejected route / 폐기 경로 | Next single lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `RelativeFormThresholdAndCompactAmbientCoercivityNoGo` | compact ambient `L2` coercivity or absolute tail norm | `ActualWeilPrimeArchimedeanRelativeFormBoundAtMostOne` |
| Collatz / 콜라츠 | `ThreeExitLocalCompensationAndTypeTwoArbitraryDelayNoGo` | every fixed post-shadow window | `TypeTwoAdaptiveValuationSurplusDescentBelowShadowEntry` |
| Goldbach / 골드바흐 | `SharpWheelEndpointHoleRadiusAndGrowingRelativeL2NoGo` | wheel-independent relative `L2` transfer | `VonMangoldtEndpointReflectionMassRetentionK56` |
| Twin Prime / 쌍둥이 소수 | `SemiprimeCoverDeficitExactParityEquivalence` | unsigned cover deficit avoids parity | `PositiveCubicRoughMassAndOneSidedLiouvilleMarginalGap` |

Machine-readable audit:
[`ticket150-relative-delay-hole-parity.json`](../data/open-problem/ticket150-relative-delay-hole-parity.json).

Reproduction:

```powershell
D:\python\anaconda3\python.exe scripts\ticket150_relative_delay_hole_parity.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket150_relative_delay_hole_parity -v
```

## 2. Riemann hypothesis / 리만 가설

### 2.1 Declared proposition / 선언 명제

Let `P` be a nonnegative self-adjoint operator with trivial kernel and form
domain `Q(P)`. Write

```text
p[v,w] = <P^(1/2)v, P^(1/2)w>.
```

Let `k` be a symmetric form on `Q(P)`. Suppose there is a bounded
self-adjoint operator `B` such that

```text
k[v,w] = <P^(1/2)v, B P^(1/2)w>.
```

1. If `||B||<=1`, then `p+k` is nonnegative.
2. If `||B||<1`, then

   ```text
   p+k >= (1-||B||)p.
   ```

3. The threshold is sharp. If `Pe_j=p_j e_j`, `p_j>0`, `p_j->0`, then for
   every `q>1`

   ```text
   K_j = -q p_j <.,e_j> e_j
   ```

   has absolute norm `q p_j->0` but makes `P+K_j` negative on `e_j`.
4. An injective positive compact `P` on an infinite-dimensional Hilbert
   space cannot satisfy `P>=cI` for any `c>0`.

`P`를 kernel이 자명한 비음수 자기수반 작용소라 하고, `Q(P)`를 그 form
domain이라 하자. 대칭 form `k`가 bounded 자기수반 작용소 `B`를 통해
`k[v,w]=<P^(1/2)v,BP^(1/2)w>`로 표현된다고 가정한다. `||B||`가 `1`
이하이면 `p+k`는 비음수이고, `1`보다 작으면
`(1-||B||)p`라는 양의 상대 하한을 갖는다.
반면 `q>1`에서는 tail 한 방향만 바꾸는 유한 rank perturbation으로
절대 norm을 얼마든지 작게 하면서 음의 방향을 만들 수 있다. 또한 compact
양의 작용소의 고윳값은 0으로 가므로 ambient `L2`에서 일정한 양의 하한을
가질 수 없다.

### 2.2 Proof / 증명

For `v in Q(P)`, put `u=P^(1/2)v`. Then

```text
(p+k)[v] = <u,(I+B)u>
          >= (1-||B||)||u||^2.
```

This proves the two sufficient statements. For sharpness, the displayed
rank-one `K_j` has relative norm `q`, absolute norm `q p_j`, and combined
eigenvalue `(1-q)p_j`. For compact `P`, the positive eigenvalues tend to zero;
therefore every proposed ambient lower bound `c` is violated by a sufficiently
late eigenvector.

`u=P^(1/2)v`로 놓으면 위 부등식이 즉시 나온다. 임계값의 sharpness는
rank-one 예에서 합성 고윳값이 `(1-q)p_j`임을 계산하면 된다. compact
작용소의 고윳값이 0으로 가므로 `P>=cI`도 불가능하다.

### 2.3 What changed / 무엇이 바뀌었는가

TICKET-149 correctly required a **relative** estimate, but its phrase
"coercive positive reference on the tail" could be read as ambient `L2`
coercivity. TICKET-150 removes that ambiguity. A compact reference may only be
coercive in its own energy/form norm; it cannot have an ambient positive
spectral floor.

TICKET-149는 절대 tail norm 대신 상대 추정이 필요하다는 방향은 맞았다.
그러나 tail의 coercivity를 ambient `L2` 하한으로 읽으면 불가능하다.
TICKET-150은 올바른 공간이 `P`가 만드는 energy/form topology임을
명시한다.

### 2.4 Boundary / 한계

The proof is abstract. It does not construct `P` and `K` for the actual Weil
quadratic form, does not verify the exact form domain, and controls no zeta
zero. The next theorem must estimate the actual prime and archimedean pieces,
not a synthetic diagonal operator.

이 증명은 추상 이차형식 정리이다. 실제 Weil 이차형식을 `P+K`로 분해하지
않았고 정확한 form domain도 확인하지 않았다. zeta 영점도 제어하지
않는다. 다음 단계는 실제 prime 항과 archimedean 항의 상대 form norm을
`1` 이하로 인증하는 것이다.

Current Weil-form context:
[Suzuki, *Weil's quadratic form via the screw function*](https://arxiv.org/abs/2606.09096).

## 3. Collatz conjecture / 콜라츠 추측

Use the accelerated odd map

```text
T(n) = (3n+1)/2^v2(3n+1).
```

After the maximal TICKET-149 shadow, write the exit as

```text
x_r = 2^r d - 5,   d odd,   r in {1,2,3}.
```

### 3.1 Exact local classification / 정확한 국소 분류

For a positive exit:

```text
r=1: T(2d-5) = oddpart(3d-7) <= 2d-5,
     equality only at d=3, x=1.

r=2: valuations begin (1,1),
     T^2(4d-5) = 9d-10 > 4d-5.

r=3: the first two valuations are (1, >=3),
     T^2(8d-5) = oddpart(9d-5) < 8d-5.
```

`r=1`과 `r=3` 종료형은 종료점보다 국소적으로 내려간다. `r=2`는 첫 두
단계가 모두 valuation `1`이고 두 번째 값 `9d-10`도 종료점보다 크다.

### 3.2 Arbitrary-delay theorem / 임의 지연 정리

For every shadow length `L>=0` and delay `H>=1`, choose

```text
d = 9^L c,
d = 1 (mod 2^(H+1)).
```

The moduli are coprime, so the Chinese remainder theorem supplies infinitely
many positive choices. Define

```text
n+5 = 2^(3L+2)c.
```

Then `n` follows the exact shadow word `(1,2)^L` and exits at

```text
x = 4d-5.
```

The first two post-exit valuations are `(1,1)` and

```text
T^2(x) = 9d-10 = -1 (mod 2^(H+1)).
```

Hence the next `H` valuations are all `1`. Every one of these `H+2`
post-exit iterates is above both `x` and the original start `n`.

모든 `L,H`에 대해 CRT로 `d`를 선택하면 실제 양의 시작점이 정확한
`(1,2)^L` shadow를 거친 뒤 `r=2`로 종료하고, 그 뒤 `(1,1,1^H)`를
따른다. 이 구간의 모든 값은 종료점과 원래 시작점보다 크다. 따라서
종료형만 보고 고정 길이 후처리 창을 정하는 모든 전략은 실패한다.

### 3.3 Boundary / 한계

An arbitrarily long finite delay is not an infinite divergent orbit. The local
contractions for `r=1` and `r=3` also need not repay the preceding
`(9/8)^L` shadow growth. What remains is an adaptive stopping-time theorem for
the `r=2` class that produces enough cumulative valuation surplus to descend
below the pre-shadow entry.

임의로 긴 유한 지연은 무한 발산 궤적이 아니다. `r=1`, `r=3`의 국소
하강도 앞선 `(9/8)^L` 팽창을 모두 상쇄한다는 뜻이 아니다. 남은 과제는
`r=2` 계열에서 shadow 진입점 아래로 내려갈 만큼 valuation surplus가
쌓이는 적응형 stopping-time 정리이다.

Parity-vector boundary:
[Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*](https://arxiv.org/abs/2605.13886).

## 4. Strong Goldbach conjecture / 강한 골드바흐 추측

Let `W` be even and squarefree, let

```text
G = {a mod W : gcd(a,W)=1},
g = 1_G,
tau_N(a) = N-a mod W.
```

Put

```text
m = (g*g)(N)
```

and let `h` be the number of fixed points of `tau_N` inside `G`.

### 4.1 Sharp endpoint-hole radius / 정확한 endpoint-hole 반지름

Among all nonnegative cyclic weights `f` satisfying

```text
(f*f)(N)=0,
```

the exact minimum is

```text
min ||f-g||_2^2 = (m+h)/2.                         (1)
```

Therefore

```text
||f-g||_2^2 < (m+h)/2
```

forces `(f*f)(N)>0`, and the threshold cannot be improved.

비음수 순환 가중치가 endpoint `N`을 완전히 잃기 위해 기준 wheel
가중치 `g`에서 움직여야 하는 최소 제곱거리는 정확히 `(m+h)/2`이다.
이보다 작은 거리에서는 endpoint convolution이 반드시 양수이고, 등호
거리에서는 실제 hole을 만들 수 있다.

### 4.2 Proof / 증명

The compatible reduced residues split into two-cycles and fixed points under
`tau_N`. Every term in the convolution is nonnegative. If the sum is zero,
each two-cycle must have at least one zero weight and each fixed point must
have zero weight. There are `(m-h)/2` two-cycles. The least distance is
therefore

```text
(m-h)/2 + h = (m+h)/2.
```

Set exactly one member of each two-cycle to zero, set every fixed point to
zero, and leave all other reduced residues at one. This attains equality.

`tau_N`의 각 2-cycle에서는 적어도 한쪽 가중치가 0이어야 하고 fixed
point에서는 그 가중치가 0이어야 한다. 기준값 `1`에서 0으로 하나를
내릴 때 제곱거리 비용은 `1`이다. 따라서 최소 비용은 정확히
`(m+h)/2`이고, 각 orbit에서 필요한 최소 개수만 0으로 만들면 등호가
달성된다.

### 4.3 Growing-wheel no-go / 성장 wheel no-go

Take the primorial wheel

```text
W_z = 2 product_(3<=p<=z) p
```

and endpoint `N=2`. Then

```text
h=1,
m=product_(3<=p<=z)(p-2),
phi(W_z)=product_(3<=p<=z)(p-1).
```

Thus the sharp **relative squared radius** is

```text
(m+1)/(2 phi(W_z)).
```

It tends to zero because

```text
m/phi(W_z)
 = product_(3<=p<=z)(1-1/(p-1)) -> 0,
```

using the divergence of the reciprocal-prime sum. Consequently there is no
fixed wheel-independent relative `L2` threshold that works uniformly even
for the single congruence endpoint `N=2 mod W` as the primorial wheel grows.
Equivalently, for every `epsilon>0` there is a primorial `W` and a
nonnegative `f` with

```text
||f-g||_2^2 < epsilon phi(W),   (f*f)(2)=0.
```

primorial wheel이 커질수록 endpoint hole까지의 상대 제곱거리가 0으로
간다. 따라서 `||f-g||/||g||`가 어떤 고정 작은 수보다 작다는 정보만으로
성장하는 모든 primorial wheel의 `N=2 mod W` endpoint 양성을 보장할 수
없다.

### 4.4 Boundary / 한계

This is a cyclic nonnegative-weight theorem. The extremizers are not
von Mangoldt weights, and `N=2 mod W` is not an interval counterexample to
Goldbach. The next theorem must retain arithmetic mass on the actual
reflection pairs `a,N-a` at the pointwise `K56` scale.

이 정리는 순환 비음수 가중치에 대한 것이다. 등호 가중치는 실제
von Mangoldt 가중치가 아니며 `N=2 mod W`도 골드바흐 반례가 아니다.
남은 과제는 실제 `a,N-a` 반사 쌍에서 산술 질량이 유지됨을 `K56`
규모로 증명하는 것이다.

Explicit minor-arc context:
[Helfgott, *Minor arcs for Goldbach's problem*](https://arxiv.org/abs/1205.5252).

## 5. Twin Prime conjecture / 쌍둥이 소수 추측

On the cubic-rough gap-two support, partition edges into:

```text
T : (prime, prime),
D : (semiprime, semiprime),
U : (semiprime, prime),
V : (prime, semiprime).
```

Then

```text
E = T+D+U+V,
L = D+U,
R = D+V.
```

### 5.1 Exact parity equivalence / 정확한 parity 등가식

Direct subtraction gives

```text
E-L-R = T-D.                                      (2)
```

Using the Liouville marginal sums from TICKET-142,

```text
L=(E+A10)/2,
R=(E+A01)/2,
```

so

```text
E-L-R = -(A10+A01)/2.                             (3)
```

Therefore the proposed all-scale cover deficit

```text
L+R <= (1-delta)E
```

is exactly

```text
T-D >= delta E
```

or equivalently

```text
A10+A01 <= -2 delta E.
```

semiprime endpoint cover의 양의 결손은 정확히 쌍둥이 간선이 양끝
semiprime 간선보다 고정 비율만큼 더 많다는 명제이다. 이는 부호 없는
rough 질량이나 단순 marginal counting만으로 자동으로 나오는 명제가
아니다.

### 5.2 Why this corrects the route / 경로 수정 이유

The cover condition remains a valid sufficient condition, but it is not a
parity-free simplification. A synthetic table with `T=1`, `D=2`, and no mixed
edges contains a twin while

```text
E-L-R = -1.
```

Thus even one twin in every interval would not by itself prove a positive
cover deficit. The missing theorem is the signed comparison `T>D`, not merely
the existence of rough edges or separate upper bounds interpreted without
their joint parity meaning.

cover 조건은 여전히 충분조건이지만 parity 문제를 제거한 쉬운 조건은
아니다. `T=1`, `D=2`인 표에는 실제 twin cell이 있지만 cover deficit는
음수다. 따라서 “구간에 twin이 하나 있다”보다도 `T>D`가 더 강하다.

### 5.3 Boundary / 한계

Equations (2) and (3) estimate nothing at infinite scale. The finite source
rows through `X=10^6` all have positive deficit, but this does not produce a
uniform `delta` or even prove positive rough mass at every large scale. The
next single lemma must combine positive rough mass with a one-sided Liouville
marginal gap.

식 (2), (3)은 항등식일 뿐 무한 규모 추정이 아니다. `X=10^6`까지의 유한
행에서는 양의 deficit가 관측되지만 고정 `delta`나 모든 큰 구간의 양의
rough 질량을 증명하지 않는다. 다음 보조정리는 실제 Type I/II 정보를
사용해 `A10+A01<=-2 delta A00`을 증명해야 한다.

Sieve boundary:
[Ford--Maynard, *On the theory of prime producing sieves*](https://arxiv.org/abs/2407.14368).

## 6. Proof DAG / 증명 의존성

Each problem uses the same three-state contract:

```text
rejected or insufficient route
              |
              v
exact TICKET-150 theorem
              |
              v
single open arithmetic/analytic lemma
```

각 DAG의 마지막 노드는 반드시 `open_not_proven`이다. 기계 감사의
`conjecture_resolution_count`는 `0`이며, 이 값은 UI와 테스트에서도
강제된다.

## 7. Finite computation boundary / 유한 계산의 경계

The generator audits:

- 96 exact RH diagonal threshold rows and 16 compact-coercivity witnesses;
- 3,000 local Collatz exits and 42 CRT arbitrary-delay witnesses;
- every even endpoint for `W=6,30,210,2310` plus 13 primorial radius rows;
- four inherited cubic-rough Twin scales and four synthetic separation tables.

These computations validate formulas and serialization. They do not promote a
finite range to an infinite theorem.

생성기는 RH 대각 임계값 96행과 compact witness 16개, Collatz 국소 종료
3,000개와 CRT 지연 witness 42개, `W=6,30,210,2310`의 모든 짝수 endpoint,
primorial 반지름 13행, Twin의 네 실제 규모와 네 합성 분리표를 검사한다.
이 계산은 식과 직렬화 계약을 검증할 뿐 유한 범위를 무한 정리로 승격하지
않는다.

## 8. Final boundary / 최종 경계

TICKET-150 establishes:

1. the correct sharp abstract relative-form threshold for an RH positivity
   route;
2. an exact arbitrary finite-delay obstruction for the sole expanding
   Collatz shadow exit type;
3. the sharp nonnegative endpoint-hole distance and a growing-wheel relative
   `L2` no-go for Goldbach models;
4. the exact parity meaning of the Twin semiprime-cover deficit.

TICKET-150 does **not** establish RH, Collatz, strong Goldbach, Twin Prime, or
the negation of any of them.

TICKET-150은 네 경로의 정확한 임계값과 장벽을 확정했지만 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 증명하거나
반증하지 않았다.
