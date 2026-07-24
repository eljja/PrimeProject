# TICKET-137: Cancellation, Entropy, and Information Budgets

Date: 2026-07-26

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket137-cancellation-entropy-and-information-budget.json`

## Publication boundary / 논문 제출용 경계

**English.** TICKET-137 proves four exact intermediate or no-go statements.
They are new results inside PrimeProject, not claims of literature priority.
They do not prove or refute the Riemann Hypothesis, Collatz conjecture, strong
Goldbach conjecture, or Twin Prime conjecture. The calculations replay exact
integer, rational, or orthogonality identities; finite rows are not substituted
for the missing infinite arithmetic theorems.

**한국어.** TICKET-137은 정확한 중간정리 또는 한계 정리 네 개를 확정한다.
여기서 새 결과란 PrimeProject 내부의 새 결과이며 학계 최초라는 뜻이 아니다.
어느 결과도 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측을
증명하거나 반증하지 않는다. 계산은 정수, 유리수, 직교성 항등식을 재생할
뿐이며, 유한 표를 미해결 무한 산술 정리 대신 사용하지 않는다.

## Result table / 결과표

| Problem / 문제 | Exact result / 정확 결과 | Discarded route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `HadamardCancellationSchurOverestimateNoGo` | absolute Schur sums as a necessary proxy for signed operator norm | `ProjectedWeilSignedCrossBlockCancellationWithPositiveMargin` |
| Collatz / 콜라츠 | `AffineCappedValuationCylinderMassDecay` | zero 2-adic mass implies no natural code | `ArithmeticEmptinessOfInfiniteAffineCappedNaturalCodeSet` |
| Goldbach / 골드바흐 | `SubpowerGrowingWheelLogMomentBarrier` | any growing wheel makes low moments pointwise | `NearFullScaleWheelOrPointwiseBinaryGoldbachResidualK56` |
| Twin Prime / 쌍둥이 소수 | `RationalFourierInformationBudgetLowerBound` | subcritical rational Fourier periods separate twin primality | `IrrationalOrSupercriticalAperiodicTypeIITwinSeparation` |

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

For every `N=2^m>=4`, let `H_N` be a Sylvester Hadamard matrix and set
`B_N=H_N/N`. Then

```text
max absolute row sum = max absolute column sum = 1
||B_N||_2^2 = 1/N.
```

For the block with `A=I` and `C=(2/N)I`, the true operator margin is `1/N>0`,
but the absolute Schur margin is `2/N-1<0`.

`N=2^m>=4`에서 `B_N=H_N/N`이라 하자. 절댓값 행합과 열합은 모두 1이지만
실제 연산자 노름 제곱은 `1/N`이다. `A=I`, `C=(2/N)I`인 블록의 실제 여유는
양수이나 절댓값 Schur 인증서는 음수를 낸다.

### Proof / 증명

Hadamard orthogonality gives `H_N H_N^T=N I`, so every singular value of
`H_N/N` is `1/sqrt(N)`. Each of its `N` entries in a row has magnitude `1/N`,
so the absolute row and column sums are one. Therefore

```text
alpha*gamma - ||B_N||^2 = 2/N - 1/N = 1/N > 0
alpha*gamma - R*S       = 2/N - 1 < 0.
```

This is an exact family for arbitrarily large dimension. `QED`

Hadamard 직교성으로 모든 singular value가 `1/sqrt(N)`이다. 반면 절댓값을
먼저 취하면 상쇄가 사라져 행합과 열합이 1이 된다. 따라서 TICKET-136의
절댓값 Schur 조건은 충분조건이지만 실제 연산자 노름의 필요한 근사는 아니다.

### Computation and boundary / 계산과 경계

Dimensions `4,8,16,32,64,128` were checked using exact integer inner products.
All true margins are positive and all absolute Schur margins are negative.
This does not estimate a projected Weil operator. The missing theorem is a
signed or cancellation-sensitive Weil cross-block estimate with a tail gap.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

For `B>=2`, define

```text
m_B(k) = max { s in Z : 2^s B^k <= (3B+1)^k }.
```

A least counterexample `n_0>=B` must satisfy `S_j<=m_B(j)` at every depth.
Under normalized Haar measure on odd 2-adic integers, a valuation word with
sum `s` has mass `2^-s`, so the terminal-cap mass is exactly

```text
sum_{s=k}^{m_B(k)} binom(s-1,k-1) 2^-s.
```

The set satisfying every prefix cap has no larger mass and its mass decays
exponentially in `k`.

`B>=2`인 최소 반례가 있다면 모든 깊이에서 누적 valuation이 정확한 affine
cap 아래에 있어야 한다. 홀수 2-adic 공간에서 합이 `s`인 valuation word의
질량은 `2^-s`이고, 합이 `s`인 양의 composition 수가
`binom(s-1,k-1)`이므로 위 합이 정확히 나온다.

### Proof / 증명

TICKET-136 gives the cap from non-descent. Every positive valuation word
`(a_1,...,a_k)` defines one odd residue class modulo `2^(S_k+1)`, hence relative
Haar mass `2^-S_k`. Summing over positive compositions proves the formula.
Imposing all prefix caps only removes cylinders.

For `lambda=log_2(3+1/B)` in `(1,2)`, the geometric valuation law
`P(a=r)=2^-r` and Chernoff's inequality give

```text
mass <= q(lambda)^k,
q(lambda) = (lambda/2)
            (lambda/(2(lambda-1)))^(lambda-1) < 1.
```

Thus the 2-adic survivor mass tends to zero. `QED`

### Exact no-go / 정확한 한계

Every finite valuation cylinder is one odd residue class modulo
`2^(S_k+1)`. It contains `r+t*2^(S_k+1)` for arbitrarily large positive `t`.
Therefore finite-depth cylinder thinning, and even a limiting measure-zero
statement, does not prove that no natural integer code survives all depths.

모든 유한 cylinder에는 임의로 큰 양의 정수가 있다. 또한 자연수 한 점의
Haar 질량 자체가 0이므로 “질량 0”에서 “자연수 코드 없음”으로 넘어갈 수
없다. 다음 단계는 측도 정리가 아니라 무한 survivor set과 자연수 embedding의
교집합이 공집합임을 보이는 결정론적 산술 정리다.

The machine audit covers `B=2,10,1000,10^6`, depths through `64`, and exact
finite-cylinder representatives. It is not a Collatz proof.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

Let `W` be odd and squarefree, `X=2WM`, and let `H_W(X)` be the even integers
through `X` coprime to `W`. Then

```text
|H_W(X)| = M phi(W),
phi(W)^2 >= W.
```

If `0<epsilon<=1` and `W<=X^(1-epsilon)`, then

```text
|H_W(X)| >= X^((1+epsilon)/2)/2.
```

Consequently the sharp normalized `L^p`-to-maximum factor cannot be at most
`6/5` unless `p=Omega(log X)`.

### Proof / 증명

Write every even `N` as `2m`. Since `W` is odd,
`gcd(N,W)=gcd(m,W)`, so each complete block of `W` consecutive values of `m`
contributes `phi(W)` hard residues. For odd
squarefree `W`,

```text
phi(W)^2/W
  = product_{p|W} (p-1)^2/p
  >= 1,
```

because every odd-prime factor is at least one. Substitution into
`M=X/(2W)` proves the size bound. Since
`||x||_infinity<=h^(1/p)||x||_p` is sharp for a one-point spike,
`h^(1/p)<=6/5` requires `p>=log h/log(6/5)`. `QED`

고정 wheel뿐 아니라 `W<=X^(1-epsilon)`인 모든 subpower squarefree wheel도
hard stratum을 충분히 작게 만들지 못한다. 따라서 growing wheel이라는
사실만으로 sublogarithmic moment를 점별 양성으로 승격할 수 없다.
여기서 `W`는 홀수여야 한다. 짝수 `W`를 사용하면 모든 짝수 `N`이 인수
`2`를 공유하여 `gcd(N,W)=1`이라는 hard-stratum 정의가 공집합이 된다.

### Computation and boundary / 계산과 경계

The exact count, totient inequality, and integer moment threshold were checked
for `W=3,15,105,1155,15015`, including direct enumeration of one complete
residue block; the final row records the exact integer threshold for the chosen
scale. This proves no binary Goldbach residual estimate. A near-full-scale
wheel with all complementary strata controlled, or a direct pointwise signed
residual theorem with `K<=56`, remains open.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

At scale `X`, let a finite rational Fourier pair-feature map use frequencies
`a_j/q_j`, and put `L=lcm(q_j)`. For every locally admissible class modulo `L`
and distinct primes `r,s` not dividing `2L`, CRT produces a proper composite
pair with the same transcript as every integer in that residue class and

```text
n < 2 L r s.
```

Hence if `2Lrs<=X`, no locally admissible transcript is by itself a sound
sufficient certificate of twin primality on `[1,X]`. Any zero-false-positive
separator depending only on these rational transcripts must have
`L>X/(2rs)` for that outside prime pair, or use information that is not a
finite rational period.

### Proof / 증명

All phases at `n` and `n+2` factor through `n mod L`. Impose

```text
n = a mod L,
n = 0 mod r,
n = -2 mod s.
```

CRT gives one class modulo `Lrs`. Adding `Lrs` once when needed makes both
divisors proper and keeps the witness below `2Lrs`. The rational Fourier pair
transcript is unchanged. `QED`

유리 Fourier 특성의 수가 scale과 함께 늘더라도 denominator lcm이
`X/(2rs)` 이하인 정보 예산에서는 동일한 특성을 가진 합성수 쌍이 범위 안에
남는다. 이는 쌍둥이 소수의 반례가 아니라 transcript만으로 충분 인증을
시도하는 분리기 클래스의 반례다. 외부 산술 증명이나 추가 인수 정보까지
배제하는 정리가 아니다.

### Computation and boundary / 계산과 경계

Four denominator families and 108 admissible-class collisions were verified
exactly, with zero failures. Irrational phases, supercritical denominator
growth, genuine Type II cancellation, and positive exact-gap-two mass remain
untouched.

## 5. Cross-problem synthesis / 교차 문제 결론

The four failures share a precise pattern:

1. Absolute magnitude loses signed cancellation in RH.
2. Small measure loses arithmetic emptiness in Collatz.
3. Low moments lose pointwise positivity in Goldbach.
4. Finite rational periods lose factor-sensitive information in Twin Prime.

네 경우 모두 요약 통계가 강해 보여도 원래 명제가 요구하는 부호, 자연수
공집합, 점별 양성, 비주기적 인수 정보를 잃는다. 다음 TICKET은 더 큰 유한
계산이 아니라 이 손실된 정보를 보존하는 보조정리를 공격해야 한다.

## 6. Reproduction / 재현

```powershell
python scripts/ticket137_cancellation_entropy_and_information_budget.py
python -m unittest tests.test_ticket137_cancellation_entropy_and_information_budget
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Generated artifacts:

- `data/open-problem/ticket137-cancellation-entropy-and-information-budget.json`
- `data/open-problem/riemann/rh-ticket-137-hadamard-schur-no-go.json`
- `data/open-problem/collatz/co-ticket-137-affine-cap-mass-decay.json`
- `data/open-problem/goldbach/gb-ticket-137-subpower-wheel-barrier.json`
- `data/open-problem/twin-prime/tp-ticket-137-fourier-information-budget.json`

## 7. Literature boundary / 문헌 경계

The project continues to treat all four targets as open. The current status of
RH is recorded by the
[Clay Mathematics Institute](https://www.claymath.org/millennium/Riemann-Hypothesis/).
For Collatz, the relevant distinction between almost-all and every orbit is
visible in Tao's
[almost-bounded-orbits theorem](https://arxiv.org/abs/1909.03562).
For Goldbach, the strong binary conjecture remains distinct from the proved
ternary theorem; see Helfgott's
[ternary Goldbach monograph](https://arxiv.org/abs/1501.05438).
For Twin Prime, bounded-gap results do not imply exact gap two; see the
[bounded-interval survey](https://arxiv.org/abs/1410.8400).

Hadamard orthogonality, Haar cylinder mass, Chernoff bounds, Euler totient
identities, norm comparison, and CRT are standard tools. PrimeProject claims
only the explicit four-track synthesis, exact audit contracts, and revised
proof-DAG boundaries.
