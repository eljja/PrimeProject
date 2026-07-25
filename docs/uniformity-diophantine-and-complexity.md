# TICKET-139: Uniformity, Diophantine Windows, and Complexity

Date: 2026-07-28

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket139-uniformity-diophantine-complexity.json`

## Publication boundary / 논문 제출용 경계

**English.** TICKET-139 proves four exact intermediate or proof-route no-go
statements. They are new results inside PrimeProject, not claims of literature
priority. They do not prove or refute the Riemann Hypothesis, Collatz
conjecture, strong Goldbach conjecture, or Twin Prime conjecture. A general
algebraic theorem is never replaced by a finite table. The Collatz period
audit and the irrational-rotation table are explicitly bounded computations.

**한국어.** TICKET-139는 정확한 중간정리 또는 증명 경로 한계 정리 네 개를
확정한다. 여기서 새 결과는 PrimeProject 내부에서 새로 확정한 결과라는
뜻이며 학계 최초라는 주장이 아니다. 리만 가설, 콜라츠 추측, 강한
골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지
않는다. 일반 대수 정리를 유한 표로 대체하지 않으며, Collatz 주기 감사와
무리수 회전 표는 명시된 범위 안의 계산이다.

## Result table / 결과표

| Problem / 문제 | Exact result / 정확 결과 | Discarded route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `TwoMutuallyUnbiasedBasesCrossGramL1NoGo` | absolute cross-Gram row sums as a dimension-sharp criterion | `ProjectedWeilSignedGramSpectralRadiusBelowTailGap` |
| Collatz / 콜라츠 | `CollatzCycleDiophantineWindowAndVerifiedFloorExclusion` | bounded period exclusion as global convergence | `AllPeriodSupercriticalCycleDiophantineExclusion` |
| Goldbach / 골드바흐 | `PowerOfTwoBarycentricMomentAnnihilatorNoGo` | finitely many polynomial moments imply pointwise K=56 | `LocalizedPowerOfTwoSignedGoldbachResidualK56` |
| Twin Prime / 쌍둥이 소수 | `FiniteIrrationalOrbitLipschitzLookupComplexityNoGo` | scale-dependent Lipschitz interpolation as Type II information | `UniformSobolevAperiodicTypeIICancellationWithPositiveTwinMass` |

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `H` be a real Hadamard matrix of square order `N`. Form a `2N` by `N`
matrix `B` by stacking the rows of

```text
I/sqrt(2)       and       H/sqrt(2N).
```

Then

```text
B*B = I,
||B||_2^2 = 1.
```

Every row has squared norm `1/2`, but the TICKET-138 absolute cross-Gram
row budget is

```text
d+c = (1+sqrt(N))/2.
```

따라서 TICKET-138의 cross-Gram 기준은 올바른 충분조건이지만 필요조건이
아니다. 실제 연산자 노름은 항상 1인데 절댓값 상관 행합은 `sqrt(N)`
규모로 증가한다.

### Proof / 증명

Hadamard orthogonality gives

```text
H^T H = N I.
```

Consequently

```text
B*B = I/2 + H^T H/(2N) = I.
```

Rows inside either basis are orthogonal. A standard-basis row and a
Hadamard-basis row have inner product

```text
+/- 1/(2 sqrt(N)).
```

Each row meets `N` rows from the other basis, so its absolute off-diagonal
correlation budget is `sqrt(N)/2`. Adding the row energy `1/2` proves the
formula. Its ratio to the true norm squared tends to infinity. `QED`

### Exact no-go / 정확한 한계

This construction is a union of two mutually unbiased orthonormal bases,
scaled to a Parseval tight frame. It shows that taking absolute values after
the row inner products can still destroy decisive spectral cancellation.
TICKET-138 repaired entrywise Schur loss, but an additional `l1` aggregation
loss remains.

이 결과는 cross-Gram 정리 자체를 반박하지 않는다. 그 정리는 여전히
충분조건이다. 다만 projected Weil 행렬에서 이 충분조건을 만족시키는
것이 실제 양성보다 훨씬 강할 수 있으므로, 다음 단계는 절댓값 행합이
아니라 signed Gram 연산자의 spectral radius를 산술적으로 추정해야 한다.

### Computation and boundary / 계산과 경계

Sylvester-Hadamard orders `4,16,64,256` were checked with exact integer inner
products. The true norm squared remains one while the row budget is
`3/2,5/2,9/2,17/2`. This is an exact auxiliary matrix family, not the actual
projected Weil operator. It gives neither an RH proof nor a negative Weil
witness.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

Consider a positive accelerated Collatz cycle with odd values
`n_0,...,n_(k-1)`, exact valuations `a_i`, total valuation `S`, and minimum
cycle value `m`. Then

```text
2^S / 3^k = product_i (1 + 1/(3 n_i)),
1 < 2^S / 3^k <= (1 + 1/(3m))^k.
```

If a verified lower bound gives `m>=M`, a necessary condition for period `k`
is that a power of two lies in this explicit Diophantine window.

양의 비자명 주기는 단순히 `2^S>3^k`만 만족해서는 안 된다. 두 수의
비율이 `m`이 정하는 매우 좁은 창 안에 있어야 한다. 이는 TICKET-138에서
남은 supercritical 주기 코드를 정량적으로 제한한다.

### Proof / 증명

Each accelerated step satisfies

```text
2^(a_i) n_(i+1) = 3 n_i + 1
                 = 3 n_i (1 + 1/(3n_i)).
```

Multiply around the cycle. The products of the `n_i` cancel and give the
identity. Every correction factor is strictly greater than one and no larger
than `1+1/(3m)`, proving the window. `QED`

For a fixed `k`, the smallest possible `S` has

```text
S = ceil(k log_2 3).
```

Higher `S` only move farther above the window. With `m>=M`, the candidate is
tested without logarithmic floating point by the exact integer inequality

```text
2^S (3M)^k <= [3(3M+1)]^k.
```

### Exact bounded corollary / 정확한 유한 따름정리

PrimeProject's stored finite certificate implies that a nontrivial cycle
minimum satisfies `m>=2^28`. Using this floor:

- all periods `1<=k<=20,000` were checked with exact integers;
- `19,999` periods fail the necessary window;
- the only period not excluded by this test is `k=15,601`;
- its only candidate total valuation is `S=24,727`.

`k=15,601`은 주기를 발견했다는 뜻이 아니다. valuation 순서, 정수 시작값,
정확한 나눗셈 조건은 전혀 구성되지 않았다. 단지 이 하나의
`(k,S)` 쌍에서는 현재의 최소값 창만으로 모순이 나오지 않는다는 뜻이다.

### Boundary / 한계

The product-window theorem is universal for positive cycles, but the
`20,000`-period exclusion is finite and uses the internal `2^28` floor.
Cycles of larger period and all divergent aperiodic orbits remain open.
Finite cycle exclusion cannot prove Collatz convergence. The next single
lemma is an all-period lower bound for

```text
|S log 2 - k log 3|
```

strong enough to contradict the cycle window.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

For distinct nodes `x_0,...,x_q`, define barycentric weights

```text
w_i = 1 / product_(j != i) (x_i-x_j).
```

Then

```text
sum_i w_i x_i^r = 0    for 0 <= r < q,
sum_i w_i x_i^q = 1.
```

After clearing denominators, this produces a nonzero primitive integer vector
whose first `q` signed polynomial moments vanish exactly.

Take

```text
x_i = 2^(i+1).
```

All support points then lie in the powers-of-two Goldbach hard stratum.

### Proof / 증명

The Lagrange basis polynomial

```text
L_i(x) = product_(j != i) (x-x_j)/(x_i-x_j)
```

has leading coefficient `w_i`. Interpolate the polynomial `x^r` on the
`q+1` nodes. If `r<q`, its coefficient of `x^q` is zero, so the sum of the
leading coefficients on the interpolation side is zero. For `r=q`, that
coefficient is one. Clearing denominators preserves the zero identities.
`QED`

### Exact no-go / 정확한 한계

For every fixed number of polynomial moments there is a nonzero pointwise
signal, supported entirely on powers of two, that all those moments fail to
see. Therefore no inequality of the form

```text
pointwise maximum
  <= C * maximum of finitely many signed polynomial moments
```

can hold for arbitrary residual vectors.

이는 실제 Goldbach 잔차가 이 barycentric 벡터라는 뜻이 아니다. 반대모형은
“고정된 유한 모멘트 정보만으로 점별 K=56을 논리적으로 강제한다”는
추론을 반박한다. 실제 잔차에 특유한 소수 산술, 국소 최대 부등식,
all-frequency 제어는 여전히 유효한 연구 경로다.

### Computation and boundary / 계산과 경계

Orders `q=1,...,10` were replayed with exact rational and integer arithmetic.
All declared moments vanish, the `q`-th moment equals the exact normalization,
and every primitive vector has nonzero pointwise amplitude. At `q=10`, the
largest coefficient is `70,300,024,700,928`.

The next lemma must estimate the actual binary Goldbach residual locally on
powers of two with `K<=56`; another fixed list of global moments is
insufficient.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

Let `z_1,...,z_N` be distinct points on the unit circle with minimum geodesic
separation `delta`.

1. Every binary labeling of these points has a tent interpolant `F` with
   `Lip(F)<=2/delta`.
2. There is a binary labeling, obtained by separating a closest pair, for
   which every interpolant has `Lip(F)>=1/delta`.
3. For `N` points of an irrational rotation, `delta<=1/N`.

따라서 유한 무리수 궤도에서 Lipschitz 상수를 scale에 따라
`1/delta`만큼 키우는 것을 허용하면 여전히 임의 lookup을 구현할 수 있다.
정칙성이라는 이름만 추가해서는 TICKET-138의 동어반복 문제가 사라지지
않는다.

### Proof / 증명

Place at each positively labeled point a geodesic tent of radius `delta/2`
and height one. Distinct tent interiors are disjoint and every slope has
magnitude at most `2/delta`, giving the upper bound.

Assign labels zero and one to a closest pair. The Lipschitz quotient across
that pair is exactly `1/delta`, proving the lower bound.

The `N` circular gaps between ordered rotation points sum to one. At least one
gap is at most `1/N`, proving the final statement. `QED`

### Exact no-go / 정확한 한계

Scale-dependent Lipschitz interpolation is not by itself arithmetic Type II
information. A useful regularity hypothesis must have a norm budget fixed
independently of the search horizon, and that uniform class must support a
signed bilinear estimate.

이 정리는 실제 쌍둥이 소수 라벨이 큰 Lipschitz 상수를 필요로 한다고
증명하지 않는다. 가장 가까운 두 점의 실제 라벨이 다르다는 보장이 없기
때문이다. 정리는 worst-case lookup을 배제하려면 uniform complexity가
필요하다는 것만 확정한다.

### Computation and boundary / 계산과 경계

For the rotation by `sqrt(2)`, orbit sizes from `8` through `2,048` were
audited at 90-decimal precision. Closest returns occur at Pell denominators;
the required worst-label Lipschitz lower bound grows from about `14.07` to
`2,786.00`. These rows illustrate the separation scale. They are not a
Vaughan Type II estimate and provide no positive exact-gap-two mass.

## 5. Cross-problem synthesis / 교차 문제 결론

TICKET-139 isolates a shared failure of non-uniform certificates:

1. RH: absolute Gram budgets grow with frame redundancy while the spectrum
   stays bounded.
2. Collatz: finite period exclusion leaves an unbounded-period and aperiodic
   quantifier.
3. Goldbach: every fixed number of moments has an exact annihilator.
4. Twin Prime: finite labels can be interpolated if regularity cost may grow
   with the horizon.

공통적으로 필요한 것은 “각 유한 크기에서 무엇인가 존재한다”가 아니라
dimension, period, localization, analytic norm에 대해 균일한 정량
부등식이다.

## 6. Reproduction / 재현

```powershell
python scripts/ticket139_uniformity_diophantine_and_complexity.py
python -m unittest tests.test_ticket139_uniformity_diophantine_and_complexity
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Generated artifacts:

- `data/open-problem/ticket139-uniformity-diophantine-complexity.json`
- `data/open-problem/riemann/rh-ticket-139-tight-frame-l1-no-go.json`
- `data/open-problem/collatz/co-ticket-139-cycle-window.json`
- `data/open-problem/goldbach/gb-ticket-139-moment-annihilator.json`
- `data/open-problem/twin-prime/tp-ticket-139-lipschitz-complexity.json`

## 7. Literature and novelty boundary / 문헌·독창성 경계

Hadamard matrices, mutually unbiased bases, tight frames, Collatz cycle
product identities, Diophantine approximation, Lagrange interpolation,
barycentric weights, irrational rotations, Pell approximants, and Lipschitz
interpolation are established mathematics. PrimeProject does not claim these
ingredients as new.

PrimeProject claims only the explicit four-track synthesis, exact
countermodels, machine-readable contracts, bounded audits, and revised proof
DAG. In particular:

- the RH frame family is not a Weil-kernel counterexample;
- the Collatz period bound is not a global cycle result;
- the Goldbach annihilator is not an arithmetic residual;
- the Twin interpolation theorem is not a Type II cancellation theorem.
