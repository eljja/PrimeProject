# TICKET-138: Correlation, Periodicity, and Scale Closure

Date: 2026-07-27

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket138-correlation-periodicity-and-scale-closure.json`

## Publication boundary / 논문 제출용 경계

**English.** TICKET-138 proves four exact intermediate or no-go statements.
They are new results inside PrimeProject, not claims of literature priority.
They do not prove or refute the Riemann Hypothesis, Collatz conjecture, strong
Goldbach conjecture, or Twin Prime conjecture. General proofs are stated
separately from finite audits. The finite tables test implementations and
examples; they are not substituted for universal arithmetic arguments.

**한국어.** TICKET-138은 정확한 중간정리 또는 한계 정리 네 개를 확정한다.
여기서 새 결과는 PrimeProject 내부의 새 결과라는 뜻이며 학계 최초라는
주장이 아니다. 어느 정리도 리만 가설, 콜라츠 추측, 강한 골드바흐 추측,
쌍둥이 소수 추측을 증명하거나 반증하지 않는다. 일반 증명과 유한 감사를
분리했으며, 유한 표는 구현과 예시를 검사할 뿐 무한 산술 논증을 대신하지
않는다.

## Result table / 결과표

| Problem / 문제 | Exact result / 정확 결과 | Discarded route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `CrossGramCorrelationBlockPositivityCriterion` | signed means as operator control | `ProjectedWeilCrossGramCorrelationBudgetBelowTailGap` |
| Collatz / 콜라츠 | `SubcriticalPeriodicValuationCodesHaveNoPositiveNaturalEmbedding` | subcritical periodic codes as positive counterexample codes | `AffineCappedNaturalCodeWellFoundedness` |
| Goldbach / 골드바흐 | `AllScaleOddSquarefreeWheelMomentBarrier` | near-full wheel scale alone escapes logarithmic moments | `PointwiseSignedBinaryGoldbachResidualK56` |
| Twin Prime / 쌍둥이 소수 | `IrrationalInjectivityWithoutRegularityIsTautologicalNoGo` | irrational injectivity alone breaks parity | `RegularAperiodicTypeIICancellationWithPositiveTwinMass` |

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let the rows of a finite matrix `B` be `b_i`, and define

```text
d = max_i ||b_i||_2^2,
c = max_i sum_{j != i} |<b_i,b_j>|.
```

Then

```text
||B||_2^2 <= d+c.
```

Therefore the self-adjoint block

```text
[ A   B  ]
[ B*  C  ]
```

is positive definite if `alpha>0`, `gamma>0`, `A>=alpha I`,
`C>=gamma I`, and `d+c<alpha*gamma`.

여기서 `alpha`와 `gamma`는 양수다. `d`는 각 행의 에너지이고 `c`는 다른 행들과의 signed inner product를
합친 상관 예산이다. 절댓값 entry를 먼저 합치는 Schur 방식과 달리,
`<b_i,b_j>` 안에서 일어나는 부호 상쇄를 보존한다.

### Proof / 증명

The matrices `B*B` and `BB*` have the same nonzero eigenvalues. The row Gram
matrix `G=BB*` has

```text
G_ii = ||b_i||_2^2,
G_ij = <b_i,b_j>.
```

The Hermitian Gershgorin bound gives `lambda_max(G)<=d+c`, proving the
operator estimate. The Schur complement satisfies

```text
C-B*A^(-1)*B >= gamma I-(||B||^2/alpha)I > 0,
```

which proves block positivity. `QED`

### Exact no-go / 정확한 한계

For balanced sign vectors `s,t` with `N/2` positive and `N/2` negative
entries, let

```text
B = s*t^T/N.
```

Every signed row sum and signed column sum is zero, but

```text
B = (s/sqrt(N)) (t/sqrt(N))^T
```

is rank one with singular value one. Signed means and total signed mass
therefore do not control the operator norm. Cross-Gram coherence detects this
example exactly because its off-diagonal row correlations sum to `(N-1)/N`.

균형 부호로 평균을 0으로 만드는 것은 충분하지 않다. 같은 방향으로 정렬된
행들의 coherence가 남으면 연산자 노름은 1일 수 있다. 따라서 다음 단계는
평균 상쇄가 아니라 projected Weil 행들의 실제 cross-Gram 상관을 tail
gap보다 작게 제어하는 정리다.

### Computation and boundary / 계산과 경계

Exact integer Hadamard products and the coherent rank-one counterfamily were
checked at dimensions `4,8,16,32,64,128`. All twelve rows pass. This is a
finite-dimensional criterion, not a projected Weil estimate, and supplies no
RH proof or counterexample.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

For a positive valuation word `(a_1,...,a_k)`, put

```text
S = a_1+...+a_k,
C = sum_{j=0}^{k-1} 3^(k-1-j) 2^S_j,
S_0=0.
```

The unique odd 2-adic start having the infinite periodic itinerary
`(a_1,...,a_k)^infinity` is

```text
n = C/(2^S-3^k).
```

If `2^S<=3^k`, then `n<0`. Hence a subcritical periodic valuation code has no
positive natural embedding.

양의 valuation 주기어가 자연수 Collatz 궤도를 나타내려면 반드시
`2^S>3^k`를 만족해야 한다. 이는 TICKET-137의 affine-capped survivor
language 중 임계 이하의 모든 정확 주기 branch를 period 크기와 무관하게
제거한다.

### Proof / 증명

Every finite valuation prefix determines one odd residue class modulo
`2^(S+1)`. The nested moduli tend to infinity, so an infinite itinerary has at
most one odd 2-adic start. Shifting a periodic itinerary by `k` symbols leaves
it unchanged; uniqueness therefore implies that its accelerated `k`-step
image equals its start.

Iterating the exact affine Collatz identity gives

```text
2^S n = 3^k n + C,
(2^S-3^k)n = C.
```

Every term of `C` is positive. Equality `2^S=3^k` is impossible for positive
`k`. If `2^S<3^k`, the denominator is negative and `n<0`. `QED`

### Computation and boundary / 계산과 경계

All `9,840` words over the alphabet `{1,2,3}` through period eight were
replayed using exact rational arithmetic:

- `819` are subcritical and have negative fixed points;
- the only positive integer fixed point at each audited period is the trivial
  `n=1` itinerary;
- no nontrivial positive integer cycle occurs in this finite audit;
- selected subcritical words also satisfy the TICKET-137 affine cap through
  four repeated periods.

이 유한 열거는 period 8을 넘는 비자명 주기를 배제하지 않는다. 일반 정리가
배제하는 대상은 모든 period의 `2^S<=3^k` 코드뿐이다. `2^S>3^k`인
supercritical periodic 코드와 모든 aperiodic 자연수 코드는 여전히
미해결이다. 다음 보조정리는 이 두 부류를 함께 다루는 자연수
well-foundedness 정리다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

Let `W` be odd and squarefree, `M>=1`, `X=2WM`, and let `H_W(X)` be the even
integers through `X` coprime to `W`. Then

```text
h = |H_W(X)| = M phi(W),
h >= sqrt(X/2).
```

Consequently a sharp normalized `L^p`-to-maximum promotion cannot have factor
at most `6/5` unless

```text
p >= (log X-log 2)/(2 log(6/5)) = Omega(log X).
```

이 하한은 subpower wheel뿐 아니라 `M=1`인 near-full complete-block
규모에도 적용된다.

### Proof / 증명

Writing each even integer as `N=2m`, oddness of `W` gives
`gcd(N,W)=gcd(m,W)`. Thus every complete block contributes `phi(W)` hard
residues. For odd squarefree `W`,

```text
phi(W)^2/W = product_{p|W} (p-1)^2/p >= 1.
```

Therefore

```text
h^2 = M^2 phi(W)^2
    >= M^2 W
     = M X/2
    >= X/2.
```

The norm comparison `||x||_infinity<=h^(1/p)||x||_p` is sharp for a
one-point spike, yielding the logarithmic moment lower bound. `QED`

### Computation and boundary / 계산과 경계

Twenty exact rows combine five wheels
`3,15,105,1155,15015` with `M=1,2,5,10`. The direct residue count, totient
bound, all-scale square bound, and exact integer `6/5` moment threshold all
pass.

이 정리는 wheel 규모만 바꾸어 arbitrary residual의 worst-case moment를
점별 양성으로 올리는 경로를 폐기한다. 실제 Goldbach residual이 one-point
spike라는 뜻은 아니며, 추가 산술 정보를 가진 analytic wheel 사용까지
배제하지 않는다. 남은 단일 핵심은 wheel cardinality가 아닌
`PointwiseSignedBinaryGoldbachResidualK56`이다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

For irrational `alpha`, define

```text
phi_alpha(n) = exp(2 pi i alpha n).
```

This map is injective on the integers. Consequently every predicate
`P:Z->{0,1}` factors on the image as

```text
P = F o phi_alpha,
F(phi_alpha(n)) = P(n).
```

Without a regularity, computability, or complexity restriction on `F`, this
factorization is only a lookup-table restatement of `P`.

무리수 위상은 정수를 유일하게 식별할 수 있지만, 유일 식별과 쌍둥이
소수의 산술적 분리는 같은 명제가 아니다. 임의 lookup을 허용하면 원래
소수 판정을 feature에 그대로 저장할 수 있으므로 parity barrier를
해결한 것이 아니다.

### Proof / 증명

If `phi_alpha(m)=phi_alpha(n)`, then `alpha(m-n)` is an integer.
Irrationality forces `m=n`, proving injectivity. Injectivity makes
`F(phi_alpha(n))=P(n)` well-defined for every predicate `P`; no estimate or
algorithm has been derived. `QED`

For `alpha=sqrt(2)`, Pell convergents satisfy

```text
p_j^2-2q_j^2 = +/-1,
|q_j sqrt(2)-p_j| = 1/(p_j+q_j sqrt(2)) -> 0.
```

Thus exact injectivity coexists with arbitrarily close phase returns.
Numerical robustness cannot be inferred from injectivity either.

### Computation and boundary / 계산과 경계

Twelve Pell convergents were generated. Every exact residual has magnitude
one, no exact rational collision occurs, and the phase error decreases at
every row. The table illustrates the theorem but does not prove irrationality
or the infinite Pell recurrence.

이 결과는 analytic irrational phase가 무용하다는 정리가 아니다. 임의
lookup expressivity만으로는 증명이 되지 않는다는 no-go다. 남은 보조정리는
계산 가능한 정칙성 클래스, uniform signed Type II cancellation, 그리고
positive exact-gap-two mass로의 transport를 함께 요구한다.

## 5. Cross-problem synthesis / 교차 문제 결론

TICKET-138 identifies a common failure:

1. Signed means do not control cross-Gram coherence.
2. A large infinite code language does not make subcritical periodic codes
   natural.
3. A near-full wheel does not remove worst-case logarithmic moment pressure.
4. An injective aperiodic representation does not provide arithmetic
   regularity.

표현을 더 풍부하게 만드는 것만으로는 증명이 전진하지 않는다. 실제로
필요한 것은 correlation, well-foundedness, pointwise residual, regular
analytic transport와 같은 정량적 구조다.

## 6. Reproduction / 재현

```powershell
python scripts/ticket138_correlation_periodicity_and_scale_closure.py
python -m unittest tests.test_ticket138_correlation_periodicity_and_scale_closure
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Generated artifacts:

- `data/open-problem/ticket138-correlation-periodicity-and-scale-closure.json`
- `data/open-problem/riemann/rh-ticket-138-cross-gram-correlation-criterion.json`
- `data/open-problem/collatz/co-ticket-138-subcritical-periodic-code-no-go.json`
- `data/open-problem/goldbach/gb-ticket-138-all-scale-wheel-barrier.json`
- `data/open-problem/twin-prime/tp-ticket-138-irrational-injectivity-no-go.json`

## 7. Literature boundary / 문헌 경계

The project continues to treat all four conjectures as open. RH status is
recorded by the
[Clay Mathematics Institute](https://www.claymath.org/millennium/Riemann-Hypothesis/).
For Collatz, almost-all orbit control remains distinct from every-orbit
convergence; see Tao's
[almost-bounded-orbits theorem](https://arxiv.org/abs/1909.03562).
For Goldbach, the strong binary conjecture remains distinct from the proved
ternary theorem; see Helfgott's
[ternary Goldbach monograph](https://arxiv.org/abs/1501.05438).
For Twin Prime, bounded-gap methods do not yield exact gap two; see the
[bounded-interval survey](https://arxiv.org/abs/1410.8400).

Gershgorin bounds, Schur complements, exact accelerated Collatz identities,
Euler totient products, norm comparison, irrational rotations, and Pell
equations are standard tools. PrimeProject claims only this explicit
four-track synthesis, its exact contracts, and the revised proof-DAG
boundaries.
