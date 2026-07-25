# TICKET-144: Schur Pivots, Rank Equivalence, Martingale Variation, and Adverse Walsh Control

Date: 2026-07-26

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket144-schur-rank-equivalence-variation-adverse-walsh.json`

## Publication boundary / 논문 제출용 경계

**English.** TICKET-144 proves four exact auxiliary statements. It does not
prove or refute the Riemann Hypothesis, the Collatz conjecture, strong
Goldbach, or the Twin Prime conjecture. Its contribution is narrower: it
replaces one infinite matrix target by exact scalar Schur certificates, proves
that an unrestricted Collatz rank is equivalent to the conjecture itself,
constructs a bounded dyadic counterfamily to a generic absolute-variation
argument, and weakens a two-sided Walsh balance condition to a one-sided
adverse-part condition. The finite computations are reproducible audits, not
proofs of unbounded claims. No claim of literature priority is made.

**한국어.** TICKET-144는 네 개의 정확한 보조 명제를 증명하지만 리만
가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 자체를
증명하거나 반증하지 않는다. 이번 결과의 범위는 더 좁고 명확하다. 무한
행렬 양성 목표를 정확한 스칼라 Schur 인증으로 바꾸고, 제약 없는
콜라츠 순위 함수가 추측 자체와 동치임을 증명하며, 일반적인 절대변동
논리를 반박하는 bounded dyadic 반례족을 만들고, 모든 Walsh 성분의
양방향 균형 조건을 twin 부류에 불리한 성분만 제어하는 조건으로
약화한다. 유한 계산은 재현 가능한 감사 결과일 뿐 무한 명제의 증명이
아니다. 학계 최초성도 주장하지 않는다.

## Result table / 결과표

| Problem / 문제 | New exact result / 새 정확 결과 | Route removed / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `NestedGramSchurPivotCertificateAndFinitePrefixExtensionNoGo` | bounded positive prefixes imply all-section positivity / 유한 개 양성 prefix에서 모든 절단 양성을 추론 | `ExplicitWeilFormCoreSchurPivotLowerBound` |
| Collatz / 콜라츠 | `GlobalWellFoundedRankIffCollatzTermination` | unrestricted rank or observed hitting time as a weaker lemma / 제약 없는 rank나 관측 도달시간을 더 약한 보조정리로 취급 | `ExplicitLiftClosedFiniteDescriptionCollatzRank` |
| Goldbach / 골드바흐 | `BoundedSignalLinearAbsoluteMartingaleVariationNoGo` | bounded signal alone gives a uniform absolute path budget / bounded 신호만으로 균일 절대 경로 예산을 도출 | `ArithmeticBinaryGoldbachSignedMartingaleCancellationK56` |
| Twin Prime / 쌍둥이 소수 | `WalshL1SimplexBalanceIdentityAndAdversePartReduction` | full two-sided Walsh `L1` balance as the primary target / 전체 양방향 Walsh `L1` 균형을 주 표적으로 사용 | `UniformCubicRoughAdverseWalshPartContraction` |

The machine audit contains four exact theorems, four route corrections, four
proof DAGs, zero conjecture resolutions, and zero failed audit checks.

기계 감사에는 정확한 정리 4개, 경로 교정 4개, proof DAG 4개가 있으며
난제 해결 수와 실패한 감사 검사는 모두 0이다.

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let the nested Hermitian matrices satisfy

```text
G_(N+1) = [[G_N, b_N], [b_N*, c_N]],  G_N > 0.
```

Define the exact Schur pivot

```text
delta_(N+1) = c_N - b_N* G_N^(-1) b_N.
```

Then

```text
G_(N+1) > 0  iff  delta_(N+1) > 0,
delta_(N+1) = det(G_(N+1)) / det(G_N).
```

Consequently, every matrix in a nested family is positive definite exactly
when every pivot is positive. However, no bounded positive prefix can certify
the infinite family: for every positive `G_N`, the extension
`diag(G_N,-1)` preserves the complete audited prefix and has negative next
pivot.

한국어로, 중첩 Hermitian 행렬족 전체의 양성은 각 단계 Schur pivot의
양성과 정확히 동치다. 하지만 유한 개 절단이 모두 양수라는 사실만으로
무한 가족을 증명할 수는 없다. 마지막에 `-1` 블록을 붙이면 기존 prefix를
전혀 바꾸지 않으면서 다음 단계에서 양성을 깨뜨릴 수 있기 때문이다.

### Proof / 증명

Block elimination gives

```text
[[I, 0], [-b*G^(-1), 1]]
[[G, b], [b*, c]]
[[I, -G^(-1)b], [0, 1]]
= diag(G, c-b*G^(-1)b).
```

The two outer factors are invertible and adjoint to one another. Sylvester
inertia is therefore preserved, proving the positivity equivalence. Taking
determinants gives the pivot ratio. Applying the result inductively proves the
all-section certificate. The negative block extension supplies the finite
prefix no-go.

블록 소거의 양쪽 행렬은 서로 수반이고 가역이므로 관성 지수가 보존된다.
따라서 `G_(N+1)`의 양성은 `G_N`과 새 Schur pivot의 양성으로 정확히
분해된다. 행렬식을 취하면 determinant ratio를 얻는다. 이 명제를
귀납적으로 적용하면 모든 절단 양성이 모든 pivot 양성과 동치임을 얻고,
`diag(G_N,-1)`이 유한 prefix 승격 논리의 반례가 된다.

### Exact computation / 정확 계산

The rational implementation evaluates Hilbert matrices

```text
H_N(i,j) = 1/(i+j-1),  1 <= i,j <= N
```

for `N=1,...,10`. Their last pivots match

```text
delta_N = 1 / ((2N-1) * binom(2N-2,N-1)^2).
```

At `N=10`,

```text
delta_10 = 1/44,914,183,600.
```

Five separate negative extensions at prefix dimensions `1,2,4,8,16` preserve
the old prefix and create pivot `-1`. All 15 exact rows pass.

Hilbert 행렬은 실제 Weil form이 아니라 정확 유리수 LDL 계산과 작은
pivot의 수치 안정성을 확인하는 대조군이다. `N=10`에서 마지막 pivot은
이미 약 `2.22647e-11`이므로 부동소수점 고유값만으로 인증하지 않고
유리수 pivot을 저장한다.

### Logical limit and next lemma / 논리적 한계와 다음 보조정리

No Weil explicit-formula Gram entry and no all-`N` arithmetic pivot lower
bound has been derived. The result changes the certificate grammar; it does
not establish a zeta-zero statement.

실제 Weil 명시공식의 Gram 원소나 모든 `N`에 통하는 산술적 pivot 하한은
아직 없다. 따라서 다음 단일 목표는

```text
ExplicitWeilFormCoreSchurPivotLowerBound
```

이다: 명시적인 form-core 기저에서 실제 Weil Gram 행렬을 구성하고,
각 Schur pivot에 대해 기호적으로 양의 하한을 증명해야 한다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

Let `T` be the accelerated map on positive odd integers, with `1` treated as
the terminal state. The following statements are equivalent.

1. Every positive odd orbit reaches `1`.
2. There are a well-ordered set `W` and a map `R` from positive odd integers
   to `W` such that `R(T(n)) < R(n)` for every `n != 1`.

한국어로, 모든 가속 콜라츠 궤도가 `1`에 도달한다는 명제와 `1` 밖에서
항상 엄격히 감소하는 well-order 값 순위 함수가 존재한다는 명제는
동치다.

### Proof / 증명

Assume termination. Define

```text
R(n) = min{k >= 0 : T^k(n)=1}.
```

Then `R(T(n))=R(n)-1` for every nonterminal `n`, so natural numbers themselves
give the required well-order. Conversely, if an orbit never reaches `1`, then

```text
R(n) > R(T(n)) > R(T^2(n)) > ...
```

is an infinite strictly descending chain in a well-order, a contradiction.

종료를 가정하면 최소 도달시간이 자연수 값 rank를 즉시 만든다. 반대로
종료하지 않는 궤도가 있으면 rank 값이 well-order 안에서 무한히 엄격
감소하므로 모순이다. 양방향이 모두 성립하므로 이는 보조정리가 아니라
콜라츠 추측의 정확한 재표현이다.

### Exact computation / 정확 계산

The bounded audit computes accelerated hitting times for all `50,000` odd
starts at most `100,000`, memoizing `79,504` encountered states. The largest
input rank is

```text
R(77,031) = 129.
```

Eight selected rows verify `R(T(n))=R(n)-1`. The published lower bound of more
than `7.2e10` odd elements in a nontrivial cycle, imported in TICKET-143,
remains recorded as an external premise. It is not used in the rank
equivalence and says nothing about divergent aperiodic orbits.

`100,000` 이하 홀수 시작점 `50,000`개를 계산한 결과는 모두 종료했고
선택한 8개 행에서 rank가 정확히 1씩 감소했다. 그러나 이 rank는 각
유한 궤도가 실제로 `1`에 도달한 뒤 역으로 계산한 값이다. 독립적인 전역
rank 공식을 제공하지 않는다.

### No-go and next lemma / 폐기 경로와 다음 보조정리

Discard:

```text
"Find some unrestricted well-founded rank"
```

and any rank defined by already observed stopping time. Both hide the original
conjecture. Retain only a rank with independently checkable restricted
structure: a finite symbolic description, exact residue/affine semantics,
closure under every lift, and strict descent proved without assuming
termination.

폐기 대상은 제약 없는 well-founded rank와 관측 도달시간으로 정의한
rank다. 다음 단일 목표는

```text
ExplicitLiftClosedFiniteDescriptionCollatzRank
```

이다. 유한 기술 가능한 residue/affine 상태, 모든 자연수 lift에 대한
닫힘, 종료를 전제하지 않는 엄격 감소 증명이 함께 필요하다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

Uniformly bounded dyadic leaf values do **not** force a scale-independent
absolute martingale path-variation bound. More precisely, for every depth
`d`, there is a vector on `2^d` leaves with sup norm at most one such that the
all-left path has signed endpoint in `{0,1/2}` but absolute variation `d/2`.

한국어로, dyadic leaf 값이 모두 `[-1,1]`에 있어도 한 경로의 절대
martingale 변동은 깊이에 비례해 증가할 수 있다. bounded 신호만으로
TICKET-143의 척도 독립 절대변동 예산을 얻을 수 없다는 정확한
반례족이다.

### Construction and proof / 구성과 증명

Along the all-left path define conditional means

```text
m_l = 0       if l is even,
m_l = 1/2     if l is odd.
```

At level `l`, assign the sibling subtree the constant value

```text
s_l = 2m_l - m_(l+1).
```

Because `s_l` is `-1/2` or `1`, every leaf is in `[-1,1]`. The parent mean is
exactly `(m_(l+1)+s_l)/2=m_l`, so the construction is a consistent dyadic
martingale. Along the selected path,

```text
sum_(l<d) (m_(l+1)-m_l) = m_d-m_0 in {0,1/2},
sum_(l<d) |m_(l+1)-m_l| = d/2.
```

각 단계 sibling subtree의 상수값을 부모 평균 보존식으로 정하면 실제
leaf 벡터가 존재한다. 부호 있는 증분은 telescoping되어 끝점만 남지만
절댓값을 먼저 취하면 모든 단계의 `1/2`가 누적된다.

### Exact computation / 정확 계산

Nine exact rows at depths

```text
4, 8, 16, 32, 64, 111, 112, 113, 128
```

verify the construction. Absolute variation reaches `56` at depth `112`,
exceeds it at depth `113` with value `113/2=56.5`, and reaches `64` at depth
`128`, while the signed endpoint remains `0` or `1/2`.

### Logical limit and next lemma / 논리적 한계와 다음 보조정리

This vector family is not a binary Goldbach residual. It does not refute a
`K=56` theorem for the arithmetic residual and is not a Goldbach
counterexample. It refutes only the generic inference

```text
bounded dyadic signal => uniformly bounded absolute path variation.
```

따라서 버려야 하는 것은 절대변동을 bounded transform의 자동 결과로
취급하는 경로다. 실제 골드바흐 잔차에만 존재하는 부호 상쇄와 rough
산술 부류를 이용해야 한다. 다음 단일 목표는

```text
ArithmeticBinaryGoldbachSignedMartingaleCancellationK56
```

이다: 실제 이항 골드바흐 residual에 대해 root mean과 **signed**
martingale cancellation을 결합하여 TICKET-129의 `K=56` 충분 예산을
모든 dyadic 척도에서 증명해야 한다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

Let `N_(s,t)` be the four parity-class counts on one cubic-rough pair block,
and let

```text
A00 = N++ + N+- + N-+ + N--,
A10 = N++ + N+- - N-+ - N--,
A01 = N++ - N+- + N-+ - N--,
A11 = N++ - N+- - N-+ + N--.
```

Then the exact simplex identity is

```text
|A10|+|A01|+|A11| = max_(s,t) |4N_(s,t)-A00|.
```

Define the adverse part for the twin class `N--` by

```text
B = max(A10,0) + max(A01,0) + max(-A11,0).
```

Walsh inversion gives the targeted lower bound

```text
N-- = (A00-A10-A01+A11)/4 >= (A00-B)/4.
```

따라서 전체 Walsh `L1`을 제어하는 것은 네 parity 부류 모두가
`A00/4` 근처에 있어야 한다는 양방향 균형 조건이다. 쌍둥이 부류의
양성만 필요하다면 `A10`, `A01`, `-A11`의 양의 부분만 제어하면 된다.

### Proof / 증명

Walsh inversion expresses each `4N_(s,t)-A00` as one of the four signed sums
of `A10,A01,A11`. The maximum over the four parity classes also covers the
negatives of those sums through absolute value. The elementary identity

```text
|x|+|y|+|z| = max_(epsilon_i in {+1,-1}) |epsilon_1 x + epsilon_2 y + epsilon_3 z|
```

then proves the simplex equality. Finally,

```text
A10+A01-A11 <= A10_+ + A01_+ + (-A11)_+ = B,
```

which proves the adverse-part lower bound.

### Exact computation and strict weakening / 정확 계산과 조건 약화

At `X=10^3,10^4,10^5,10^6`, all four exact source rows satisfy the simplex
identity and have `B=0`. At `X=10^6`,

```text
(A00,A10,A01,A11) = (17634,-3970,-3992,1212),
N-- = 6702,
(A00-B)/4 = 8817/2.
```

A synthetic count vector

```text
(N++,N+-,N-+,N--) = (90,5,4,1)
```

has a positive twin class, but

```text
(A00,A10,A01,A11) = (100,90,88,82),
|A10|+|A01|+|A11| = 260 > A00.
```

Thus full Walsh `L1` contraction is sufficient but not necessary for twin
positivity. The adverse-part target is strictly weaker and directionally
matched to `N--`.

유한 네 척도에서 adverse part가 0인 것은 흥미로운 관측이지만 eventual
sign theorem은 아니다. 합성 예시는 twin 부류가 양수여도 전체 `L1`
수축은 크게 실패할 수 있음을 보여 주므로 기존 조건이 과도했음을
확정한다.

### Logical limit and next lemma / 논리적 한계와 다음 보조정리

No all-scale estimate controls `B`; four finite blocks cannot cross the sieve
parity barrier. The next single target is

```text
UniformCubicRoughAdverseWalshPartContraction
```

meaning: prove that for some fixed `delta>0` and every sufficiently large
cubic-rough pair block,

```text
B <= (1-delta) A00.
```

This would force `N-- >= delta*A00/4 > 0` on each such block. It remains an
unproved arithmetic correlation theorem, not a consequence of the finite
rows.

모든 충분히 큰 cubic-rough pair block에서 위 부등식을 증명하면 해당
block마다 twin 부류가 양수가 된다. 그러나 현재는 그 균일 상관 추정이
없으며 sieve parity 장벽도 제거되지 않았다.

## Proof DAG / 증명 의존성 그래프

```text
RH-T144-CLOSED  -> RH-T144-OPEN
Schur certificate  -> Explicit Weil pivot lower bound

CO-T144-CLOSED  -> CO-T144-OPEN
rank equivalence    -> explicit lift-closed finite-description rank

GB-T144-CLOSED  -> GB-T144-OPEN
variation no-go     -> arithmetic signed cancellation K56

TP-T144-CLOSED  -> TP-T144-OPEN
adverse reduction   -> uniform adverse-part contraction
```

The exact node labels, statuses, and edges are stored under each problem's
`proof_dag` field. Every open node is `open_not_proven`.

각 문제의 정확한 노드명, 상태, 간선은 기계 판독 JSON의 `proof_dag`
필드에 저장된다. 네 open 노드는 모두 `open_not_proven`이며 해결을
뜻하는 노드는 없다.

## Reproduction / 재현

```powershell
python scripts/ticket144_schur_rank_equivalence_variation_adverse_walsh.py
python -m unittest tests.test_ticket144_schur_rank_equivalence_variation_adverse_walsh
python scripts/verify_open_problem_structure.py
```

The generator writes the combined machine record and four problem-specific
records:

```text
data/open-problem/riemann/rh-ticket-144-schur-pivots.json
data/open-problem/collatz/co-ticket-144-rank-equivalence.json
data/open-problem/goldbach/gb-ticket-144-variation-no-go.json
data/open-problem/twin-prime/tp-ticket-144-adverse-walsh.json
```

## Literature boundary / 문헌 경계

- Connes and Consani place Weil positivity in an operator/form framework and
  analyse finite Toeplitz compressions; their work does not supply the
  TICKET-144 all-pivot arithmetic bound:
  [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368) and
  [Weil positivity and Trace formula](https://arxiv.org/abs/2006.13771).
- Hercher's verified odd-cycle lower bound is an imported premise, not a
  PrimeProject theorem:
  [There are no Collatz m-cycles with m <= 91](https://arxiv.org/abs/2201.00406).
- Tao proves an almost-all result for Collatz, not termination of every orbit:
  [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562).
- Helfgott proves weak ternary Goldbach, not the strong binary conjecture:
  [The ternary Goldbach conjecture](https://arxiv.org/abs/1312.7748).
- The Polymath bounded-gap work explicitly records the remaining parity
  limitation of sieve-only methods:
  [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897).

이 문헌들은 각 난제의 현재 수학적 경계를 설정하기 위한 1차 자료다.
TICKET-144의 유한 계산이나 보조정리를 기존 문헌의 미해결 전역 명제보다
강한 결과로 해석해서는 안 된다.
