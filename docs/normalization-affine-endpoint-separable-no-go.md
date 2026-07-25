# TICKET-145: Normalization, Affine Ranks, Signed Endpoints, and Separable Walsh No-Go Theorems

Date: 2026-07-26

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket145-normalization-affine-endpoint-separable-no-go.json`

## Publication boundary / 논문 제출용 경계

**English.** TICKET-145 proves four exact structural statements, not any of
the four target conjectures. It shows that two proposed Schur-pivot margins are
coordinate-dependent or unnecessarily strong, excludes every lower-bounded
finite-modulus piecewise-affine one-step Collatz rank, proves that a signed
Goldbach martingale endpoint is exactly the original pointwise residual and
that aggregate cancellation is insufficient, and proves that the adverse
Walsh quantity is the smallest separable nonnegative majorant but is not a
necessary condition for positive twin mass. All finite computations are exact
audits of these statements. No claim of literature priority is made.

**한국어.** TICKET-145는 네 난제 자체가 아니라 네 개의 정확한 구조
명제를 증명한다. Schur pivot에 제안했던 두 margin 중 하나는 좌표에
의존하고 다른 하나는 필요 이상으로 강함을 보인다. 하방 유계인 모든
유한 modulus별 piecewise-affine 1-step Collatz rank를 배제한다. Goldbach
martingale의 부호 있는 endpoint가 원래 점별 잔차와 정확히 같고 전체
합의 상쇄만으로는 점별 상한을 얻지 못함을 증명한다. 마지막으로 adverse
Walsh 양이 최소 separable 비음수 majorant이지만 twin 질량 양성의
필요조건은 아님을 증명한다. 모든 유한 계산은 이 명제들의 정확 감사일
뿐이다. 학계 최초성은 주장하지 않는다.

## Result table / 결과표

| Problem / 문제 | New exact result / 새 정확 결과 | Rejected target / 폐기 표적 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `SchurPivotBasisScalingNoGoAndNormalizedAngleReduction` | uniform absolute or normalized pivot margin / 균일 절대 또는 정규화 pivot 여유 | `ExplicitWeilFormCoreNormalizedSchurSignRecurrence` |
| Collatz / 콜라츠 | `FiniteModulusPiecewiseAffineCollatzRankNoGo` | finite-modulus piecewise-affine lower-bounded one-step rank / 유한 residue별 affine 하방 유계 1-step rank | `NonlinearLiftClosedCollatzRankBeyondFiniteResidueAffine` |
| Goldbach / 골드바흐 | `SignedMartingaleEndpointEquivalenceAndAggregateCancellationNoGo` | signed endpoint renaming or aggregate cancellation / endpoint 이름 변경 또는 전체 상쇄 | `ArithmeticBinaryGoldbachScaleEnvelopeSummableK56` |
| Twin Prime / 쌍둥이 소수 | `AdverseWalshSlackIdentityAndMinimalSeparableMajorantNoGo` | adverse-part or any separable nonnegative Walsh contraction / adverse part 또는 separable 비음수 Walsh 수축 | `IndependentCubicRoughJointWalshTypeIIBound` |

The machine audit records four exact theorems, four rejected targets, four
three-node proof DAGs, zero conjecture resolutions, and zero failed checks.

기계 감사에는 정확한 정리 4개, 폐기된 표적 4개, 세 노드 proof DAG
4개가 기록된다. 난제 해결 수와 실패한 검사 수는 모두 0이다.

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `G_N` be the Gram matrix of ordered vectors
`v_1,...,v_N`, and let `delta_n` be its nth Schur pivot. Rescale the basis by
nonzero scalars `d_n`, so that

```text
G'_N = D_N* G_N D_N,  D_N=diag(d_1,...,d_N).
```

Then

```text
delta'_n = |d_n|^2 delta_n.
```

Consequently, absolute pivot lower bounds are basis-dependent. If all pivots
are positive, any prescribed positive sequence `t_n` can be realized by
choosing

```text
|d_n|^2 = t_n/delta_n.
```

The normalized pivot

```text
eta_n = delta_n / (G_n)_(n,n)
```

is invariant under every such diagonal rescaling. However, a uniform bound
`eta_n>=epsilon>0` is still not necessary for positivity of every finite
section.

한국어로, 기저의 `n`번째 벡터를 `d_n`배 하면 `n`번째 Schur pivot은
`|d_n|^2`배 된다. 따라서 절대 pivot 하한은 기저 정규화 없이 수학적
의미가 고정되지 않는다. `eta_n=delta_n/G_nn`으로 나누면 이 배율은
사라지지만, 모든 `eta_n`이 하나의 양수 `epsilon`보다 커야 한다는
조건도 모든 절단 양성에 필요한 조건은 아니다.

### Proof / 증명

Write the nth block as

```text
G_n = [[G_(n-1), b], [b*, c]].
```

After diagonal rescaling, the predecessor block is
`D*G_(n-1)D`, the cross vector is `D*b*d_n`, and the final diagonal is
`|d_n|^2 c`. Substitution into the Schur complement gives

```text
delta'_n
= |d_n|^2 c
  - conjugate(d_n) b* D* (D*G_(n-1)D)^(-1) D b d_n
= |d_n|^2 (c-b*G_(n-1)^(-1)b).
```

The predecessor scales cancel exactly. The final diagonal also acquires the
factor `|d_n|^2`, proving invariance of `eta_n`.

블록 Schur complement에 스케일된 원소를 직접 대입하면 이전 기저의
배율은 역행렬과 양쪽 곱에서 정확히 소거되고 새 벡터의 배율 제곱만
남는다. 마지막 대각 원소도 같은 배율 제곱을 가지므로 `eta_n`은
불변이다.

### Exact countercontrol / 정확 대조군

For the Hilbert matrix

```text
H_N(i,j)=1/(i+j-1),
```

the exact formulas are

```text
delta_N = 1 / ((2N-1) binom(2N-2,N-1)^2),
eta_N   = 1 / binom(2N-2,N-1)^2.
```

Every finite Hilbert section is positive definite, while `eta_N` tends to
zero. At `N=12`,

```text
eta_12 = 1/497,634,306,624.
```

The machine audit verifies dimensions `1,...,12` with exact rational
arithmetic. A separate dimension-eight audit rescales vector `n` by `n` and
checks both `delta'_n=n^2 delta_n` and `eta'_n=eta_n`.

Hilbert 행렬은 실제 Weil 형식이 아니라 명제의 필요조건 여부를 판정하는
정확 대조군이다. 모든 유한 절단이 양성이면서 정규화 pivot이 0으로
가므로 균일 정규화 margin은 양성의 필요조건이 아니다.

### Logical limit and next lemma / 논리적 한계와 다음 보조정리

This theorem does not compute one actual Weil form-core Gram entry. It removes
two invalid target formulations but does not prove any zeta-zero statement.
The next target is

```text
ExplicitWeilFormCoreNormalizedSchurSignRecurrence
```

meaning: choose an explicit dense form core, derive its actual normalized Gram
entries from the Weil explicit formula, and obtain a recurrence for the sign
of every Schur pivot without assuming positivity.

실제 Weil form-core의 정규화 Gram 원소와 모든 절단에 통하는 부호
점화식은 아직 없다. 다음 보조정리는 양성을 가정하지 않고 그 실제
점화식을 도출해야 한다. 이것이 증명되기 전까지 RH는 열려 있다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

Fix any integer `M>=1`. On positive odd integers, consider a
finite-modulus piecewise-affine rank

```text
R(n)=a_r n+b_r when n congruent to r (mod M).
```

Assume `R` is bounded below. There is no choice of the finitely many
coefficients for which

```text
R(T(n)) < R(n)
```

holds on every nonterminal accelerated Collatz edge.

한국어로, 임의의 고정 modulus `M`에 대해 residue별로 서로 다른 affine
식을 허용하더라도, 전체 양의 홀수에서 하방 유계이고 모든 가속 Collatz
간선에서 엄격 감소하는 1-step rank는 존재하지 않는다.

### Exact witness family and proof / 정확 증거족과 증명

For every `M,k>=1`, set

```text
n_(M,k)=4Mk-1.
```

Then

```text
3n_(M,k)+1 = 2(6Mk-1),
v2(3n_(M,k)+1)=1,
T(n_(M,k))=6Mk-1.
```

Both the start and successor are congruent to `-1 mod M`, but

```text
T(n_(M,k))-n_(M,k)=2Mk>0.
```

On this residue, boundedness below along arbitrarily large `n` forces
`a_(-1)>=0`. If the slope is zero, the rank is unchanged on every witness
edge. If it is positive, the rank increases by `2Mk a_(-1)`. Both cases
contradict strict descent.

증거족은 같은 residue 상태 안에서 크기가 증가한다. 해당 affine 식의
기울기가 음수면 입력이 커질수록 rank가 음의 무한대로 가므로 하방
유계가 아니다. 기울기가 0이면 rank가 같고, 양수면 rank가 증가한다.
가능한 세 경우가 모두 배제되므로 정리가 성립한다.

### Exact computation / 정확 계산

The audit evaluates

```text
M in {1,2,3,5,7,16,31,64},
k in {1,2,4,8,16,32}.
```

All 48 rows verify the valuation, successor formula, residue self-loop,
strict expansion, and exact difference. The computation illustrates the
symbolic theorem; the theorem itself is for every `M,k>=1`.

계산 표는 48개 사례이지만 증명은 이 표에 제한되지 않는다. 식을 직접
전개했으므로 모든 양의 `M,k`에 적용된다.

### Scope and next lemma / 범위와 다음 보조정리

This extends the TICKET-79 bounded-log-plus-local-correction obstruction in a
different direction: residue-specific slopes are now allowed. It still
excludes only lower-bounded one-step ranks that are affine on a fixed finite
residue partition. It does not exclude nonlinear ranks, unbounded state,
history dependence, or adaptive block descent.

TICKET-79와 달리 residue마다 다른 기울기를 허용하지만 고정된 유한
residue 분할의 affine 1-step rank만 배제한다. 따라서 다음 목표는

```text
NonlinearLiftClosedCollatzRankBeyondFiniteResidueAffine
```

이다. 이 rank는 위 동일 residue 확장 self-loop를 처리하고, 모든 lift에
닫혀 있으며, 종료를 가정하지 않고 well-founded descent를 증명해야
한다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

Let `rho_j` be any vector on a dyadic block. Let `mu_root` be its root mean
and `Delta_l(j)` the signed martingale increment on the unique path to leaf
`j`. Then

```text
rho_j = mu_root + sum_l Delta_l(j).
```

Therefore

```text
max_j |mu_root + sum_l Delta_l(j)| <= 56
```

is exactly the original pointwise `K=56` residual statement. Calling it
“signed martingale cancellation” does not create a weaker intermediate
lemma.

At every level,

```text
sum_j Delta_l(j)=0.
```

This aggregate cancellation is automatic and does not imply a pointwise
bound.

한국어로, 각 leaf까지의 부호 있는 martingale 증분합은 망원합되어 원래
leaf 값과 정확히 같다. 그러므로 그 endpoint의 절댓값을 56 이하로
제한하는 명제는 원래 점별 잔차 명제의 다른 표기일 뿐이다. 또한 한
level의 모든 증분을 합하면 0이 되는 것은 조건부 평균의 자동 항등식이며
점별 정보를 제공하지 않는다.

### Proof / 증명

If `m_l(j)` is the conditional mean at level `l`, then

```text
Delta_l(j)=m_l(j)-m_(l-1)(j).
```

Hence

```text
mu_root + sum_(l=1)^d Delta_l(j)
= m_0(j) + sum_(l=1)^d (m_l(j)-m_(l-1)(j))
= m_d(j)
= rho_j.
```

For the level identity, each child block mean is repeated once for every leaf
in that block. The weighted sum of child means equals the weighted sum of
parent means, so their difference sums to zero.

첫 식은 순수한 telescoping이다. 두 번째 식은 각 부모 평균이 두 자식
평균의 가중 평균이라는 정의에서 바로 나온다.

### Exact no-go family / 정확 no-go 반례족

On `2^d` leaves define

```text
rho_0 = 57,
rho_j = -57/(2^d-1) for j>0.
```

The root mean is zero. Every level aggregate signed increment is zero, and
every leaf endpoint telescopes exactly. Nevertheless,

```text
max_j |rho_j| = 57 > 56.
```

Depths `2,...,10` are audited with exact rational arithmetic. There are nine
rows and no failed endpoint or level-sum checks.

이 반례족은 실제 Goldbach 잔차가 아니다. 반박하는 명제는 “전체 부호
상쇄만으로 점별 `K56`을 얻는다”는 일반 추론이다. 실제 Goldbach
반례나 `K56` 산술 정리의 반례가 아니다.

### Next lemma / 다음 보조정리

The TICKET-144 target

```text
ArithmeticBinaryGoldbachSignedMartingaleCancellationK56
```

is retired because, if interpreted pointwise, it is the original target; if
interpreted in aggregate, it is insufficient. A non-circular sufficient
target is

```text
ArithmeticBinaryGoldbachScaleEnvelopeSummableK56.
```

It must derive, from the actual major/minor-arc arithmetic decomposition,
independent scale envelopes `c_l` such that every actual dyadic increment
satisfies `|Delta_l|<=c_l` and the root budget plus `sum_l c_l` is at most 56.
TICKET-144 showed this is not a generic bounded-signal fact; the estimate must
use arithmetic structure.

다음 보조정리는 실제 이진 Goldbach 잔차의 각 scale 증분을 독립적인
산술 추정으로 제어하고 그 envelope 합이 56 예산 안에 들어감을 보여야
한다. 현재 이 정리는 증명되지 않았다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

For the four Walsh coefficients, define the joint twin deficit

```text
C = A10+A01-A11
```

and the TICKET-144 adverse part

```text
B = (A10)_+ +(A01)_+ +(-A11)_+.
```

Then

```text
B-C = (-A10)_+ +(-A01)_+ +(A11)_+ = F >= 0.
```

Moreover, `B` is the pointwise-smallest nonnegative separable majorant of
`C`. Precisely, if nonnegative one-variable functions `f,g,h`, each vanishing
at zero, satisfy

```text
f(x)+g(y)+h(z) >= x+y-z
```

for all real `x,y,z`, then

```text
f(x)+g(y)+h(z) >= x_+ +y_+ +(-z)_+ = B.
```

Despite this optimality inside the separable class, `B<A00` is not necessary
for positive twin mass.

한국어로, adverse part `B`는 joint deficit `C`를 각 좌표별 비음수
함수의 합으로 majorize하는 방법 중 점별로 가장 작다. 그러나 그
separable 계열 자체가 joint cancellation을 버리므로 `B<A00`은 twin
질량 양성에 필요한 조건이 아니다.

### Proof / 증명

The slack identity follows from

```text
x_+-x=(-x)_+.
```

For minimality, set `y=z=0` in the assumed separable bound. Since `f` is
nonnegative, this forces `f(x)>=x_+`. Similarly, `g(y)>=y_+`. Setting
`x=y=0` forces `h(z)>=(-z)_+`. Adding the three inequalities proves that every
such separable majorant dominates `B`.

최소성은 다른 두 좌표를 0으로 두는 세 번의 대입만으로 증명된다.
따라서 `B`보다 더 날카로운 비음수 separable 좌표별 상계는 존재하지
않는다.

### Exact nonnecessity witness / 정확한 비필요성 증거

Take category counts

```text
(N++,N+-,N-+,N--)=(90,5,4,1).
```

Walsh transformation gives

```text
(A00,A10,A01,A11)=(100,90,88,82),
C=96,
B=178,
F=82.
```

Walsh inversion still gives

```text
N--=(A00-C)/4=1>0,
```

while `B>A00`. Thus adverse contraction fails even though the twin class is
positive. The exact grid audit checks the slack and majorization identities on
all `17^3=4,913` triples in `[-8,8]^3`. Four actual finite cubic-rough rows are
also replayed, but they do not imply an eventual theorem.

이 합성 count 벡터는 adverse 조건이 필요조건이 아님을 정확히 보인다.
실제 네 finite row에서 `B=0`인 관측은 보존하지만, 무한 척도 부호 정리로
승격하지 않는다.

### Logical limit and next lemma / 논리적 한계와 다음 보조정리

The exact inequality `C<A00` is itself equivalent to `N-->0`. Merely renaming
that inequality would be circular. The next theorem must derive a joint bound
from an independently specified arithmetic decomposition:

```text
IndependentCubicRoughJointWalshTypeIIBound.
```

It must retain the cancellation among `A10`, `A01`, and `A11`, express the
joint deficit through independently controlled Type I/II bilinear terms, and
obtain an eventual strict saving without using the twin count. This is where
the sieve parity barrier remains.

단순히 `C<A00`을 다음 목표로 쓰면 twin 양성의 재표현이 된다. 실제
진전은 twin count를 전제로 사용하지 않는 Type I/II 산술 분해에서 세
Walsh 성분의 joint cancellation을 보존해 strict saving을 도출하는
것이다.

## Proof DAG / 증명 의존성 그래프

Each problem now has three explicit node states:

```text
T145-REJECTED -> T145-CLOSED -> T145-OPEN
refuted/circular   exact theorem   next unproved lemma
```

The exact paths are:

```text
RH: uniform margin
 -> scaling/normalization no-go
 -> explicit normalized Weil Schur-sign recurrence

CO: finite-description affine rank
 -> finite-modulus piecewise-affine rank no-go
 -> nonlinear lift-closed rank beyond finite residue affine

GB: signed martingale cancellation K56
 -> endpoint equivalence and aggregate cancellation no-go
 -> summable arithmetic scale envelope K56

TP: adverse Walsh contraction
 -> minimal separable majorant no-go
 -> independent joint Walsh Type II bound
```

Every final node has status `open_not_proven`. No node has a conjecture-proof
status.

각 마지막 노드는 `open_not_proven`이다. 난제 증명을 뜻하는 노드는
없다.

## Reproduction / 재현

```powershell
python scripts/ticket145_normalization_affine_endpoint_separable_no_go.py
python -m unittest tests.test_ticket145_normalization_affine_endpoint_separable_no_go
python scripts/verify_open_problem_structure.py
```

The generator writes the combined machine record and four problem records:

```text
data/open-problem/riemann/rh-ticket-145-normalized-schur-no-go.json
data/open-problem/collatz/co-ticket-145-piecewise-affine-rank-no-go.json
data/open-problem/goldbach/gb-ticket-145-signed-endpoint-no-go.json
data/open-problem/twin-prime/tp-ticket-145-separable-majorant-no-go.json
```

## Literature boundary / 문헌 경계

- Connes and Consani formulate RH-related Weil positivity and analyse limits
  of operator/compression approaches. TICKET-145 does not derive their missing
  global positivity estimate:
  [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368) and
  [Weil positivity and Trace formula](https://arxiv.org/abs/2006.13771).
- Tao proves an almost-all Collatz result, which does not imply termination of
  every natural orbit:
  [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562).
- Hercher excludes a large finite class of nontrivial Collatz cycles; this
  leaves longer cycles and aperiodic divergence open:
  [There are no Collatz m-cycles with m <= 91](https://arxiv.org/abs/2201.00406).
- Helfgott's ternary Goldbach proof and its discussion of the binary
  verification cutoff do not prove the strong binary conjecture:
  [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438).
- The Polymath bounded-gap work documents the parity limitation that remains
  relevant to a twin-prime Type II bridge:
  [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897).

이 문헌은 현재 알려진 수학적 경계를 설정하는 1차 자료다. TICKET-145의
정확 no-go 정리나 유한 감사가 이 문헌의 미해결 전역 명제를 해결했다고
해석해서는 안 된다.
