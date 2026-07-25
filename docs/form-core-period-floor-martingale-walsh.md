# TICKET-143: Form Cores, Published Period Floors, Martingales, and Walsh Inversion

Date: 2026-07-25

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket143-form-core-period-floor-martingale-walsh.json`

## Publication boundary / 논문 제출용 경계

**English.** TICKET-143 proves four exact functional-analytic, combinatorial,
linear-transform, or Fourier-inversion statements. One Collatz conclusion is
explicitly conditional on a cited published odd-period lower bound; that bound
is not re-proved here. The results correct four proof targets but do not prove
or refute the Riemann Hypothesis, the Collatz conjecture, strong Goldbach, or
the Twin Prime conjecture. No literature-priority claim is made.

**한국어.** TICKET-143은 함수해석, 조합론, 선형변환, Fourier 역변환에
관한 네 개의 정확한 명제를 증명한다. Collatz 결론 하나는 인용한 공개
홀수 주기 하한을 명시적인 외부 전제로 사용하며, PrimeProject가 그 하한을
다시 증명한 것은 아니다. 결과는 네 증명 목표를 교정하지만 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측을 증명하거나
반증하지 않는다. 학계 최초성도 주장하지 않는다.

## Result table / 결과표

| Problem / 문제 | Exact result / 정확 결과 | Discarded route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `ClosedFormCoreFiniteSectionBridgeAndHilbertDenseNoGo` | Hilbert-dense finite-section positivity without a form-core contract / form-core 없이 Hilbert 조밀성만 사용하는 유한절단 양성 | `ExplicitWeilFormCoreCompressionCertificateFamily` |
| Collatz / 콜라츠 | `PublishedOddPeriodFloorRetiresPeriod15601AndCompositionExplosionNoGo` | period-15,601 enumeration as the decisive current branch / 15,601주기 열거를 현재 결정적 분기로 취급 | `PublishedFloorAwareAffineCappedNaturalCodeWellFoundedness` |
| Goldbach / 골드바흐 | `DyadicMartingaleResidualIdentityAndRootModeScalingNoGo` | a scale-independent cap on every orthonormal Haar coefficient / 모든 정규직교 Haar 계수의 척도 독립 상한 | `UniformBinaryGoldbachRootMeanPlusDyadicPathVariationBelow56` |
| Twin Prime / 쌍둥이 소수 | `WalshHadamardRoughPairInversionAndCircularGapNoGo` | the one-sided ledger gap as a distinct intermediate theorem / 단측 ledger gap을 별도 중간정리로 취급 | `UniformCubicRoughWalshL1ContractionBelowOne` |

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `q` be a closed lower-semibounded quadratic form on a Hilbert space `H`.
Let

```text
V_1 subset V_2 subset ... subset D(q)
```

be finite-dimensional subspaces whose union is a **form core**, meaning that
the union is dense in `D(q)` for one, hence every, form norm associated with a
lower bound of `q`. If

```text
q(v) >= 0 for every v in every V_N,
```

then

```text
q(u) >= 0 for every u in D(q).
```

Hilbert-space density of the union alone cannot replace the form-core
assumption.

한국어로, 닫힌 아래유계 quadratic form의 유한 압축 양성을 전체 양성으로
승격하려면 단순한 `H`-norm 조밀성이 아니라 form norm 조밀성이 필요하다.

### Positive bridge proof / 양성 승격 증명

For `u in D(q)`, choose `v_N` in the finite union with `v_N -> u` in form
norm. A closed semibounded form is continuous in its form norm, so

```text
q(u) = lim_N q(v_N) >= 0.
```

This is the complete abstract promotion argument. It does not require a
separate numerical tail estimate once all finite compressions belong to an
actual form core and are nonnegative.

### Explicit Hilbert-dense no-go family / 명시적 Hilbert 조밀성 반례족

Set

```text
H = C direct_sum l2(N),
D(q) = C direct_sum {y: sum n^2 |y_n|^2 < infinity},
q(a,y) = 2 sum_(n>=1) n^2 |y_n|^2 - |a|^2.
```

This form is closed and bounded below by `-||.||^2`. For

```text
f_n = (1,e_n),
V_N = span{f_1,...,f_N},
```

the Gram matrix of `q` on `V_N` is

```text
G_N = diag(2, 2*2^2, ..., 2*N^2) - 11^T.
```

The rank-one Schur criterion gives

```text
G_N > 0 iff sum_(n=1)^N 1/(2n^2) < 1.
```

The inequality is strict for every `N`, since for `n>=2`

```text
1/n^2 < 1/(n(n-1))
```

and therefore

```text
sum_(n>=1) 1/(2n^2)
 < (1/2)(1 + sum_(n>=2) 1/(n(n-1))) = 1.
```

The union of the `V_N` is Hilbert dense. Indeed, a vector `(alpha,z)`
orthogonal to every `f_n` obeys `z_n=-alpha` for every `n`; square summability
forces `alpha=0` and `z=0`. Nevertheless,

```text
q(1,0) = -1.
```

Thus every finite Gram matrix is strictly positive and the union is Hilbert
dense, while the full closed form is not nonnegative. The union is not a form
core.

### What the counterexample does and does not show / 반례의 정확한 범위

It refutes the inference

```text
positive finite compressions + Hilbert density
  => positive closed unbounded form.
```

It is not a counterexample to RH and is not a Weil explicit-formula model.
The actual arithmetic work must specify the Weil form, its domain, a genuine
form-core basis, exact Gram entries, and positivity certificates for every
section.

Next single lemma:
`ExplicitWeilFormCoreCompressionCertificateFamily`.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

TICKET-142 selected the odd period

```text
k = 15,601, S = 24,727
```

because it was the only period at most 20,000 not eliminated by an internal
minimum-window calculation using the old internal floor `2^28`.

Hercher's 2022 paper records the published lower bound that every nontrivial
Collatz cycle has more than

```text
K = 7.2 * 10^10
```

odd members. Taking that published theorem as an external premise,
`15,601 < 72,000,000,000`, so period 15,601 cannot be a nontrivial Collatz
cycle. The TICKET-142 period-specific numerator search is therefore not a live
academic frontier.

한국어로, 저장소 내부의 오래된 `2^28` 하한 때문에 남았던 15,601주기
분기는 공개된 홀수 주기 하한보다 훨씬 작다. 인용 정리를 전제로 하면 이
분기는 이미 닫혀 있으며, 해당 주기를 대규모 열거하는 것은 현재
Collatz 장벽을 줄이지 않는다.

### Exact raw word count / 정확한 원시 word 수

Even before minimum-compatibility and exact-valuation constraints, words with

```text
a_0=1, a_i>=1, length=15,601, sum a_i=24,727
```

number

```text
binom(24,725, 15,599).
```

This integer has exactly 7,069 decimal digits and

```text
log_2 count = 23,480.649978850703...
```

The count is a raw positive-composition count, not a cycle count and not a
lower bound against every symbolic algorithm.

### Order-sensitivity no-go / 순서 민감성 no-go

For a valuation word `a=(a_0,...,a_(k-1))`, define

```text
C(a) = sum_(j=0)^(k-1) 3^(k-1-j) 2^(a_0+...+a_(j-1)).
```

Then

```text
T^k(n) = (3^k n + C(a))/2^S.
```

Words `(1,1,4)` and `(1,2,3)` have the same length `3` and sum `6`, but

```text
C(1,1,4)=19,
C(1,2,3)=23,
2^6-3^3=37.
```

Thus `(k,S)` alone cannot determine the affine numerator. Any valid symbolic
compression must retain enough ordering information or prove an invariant
that controls all orders.

### Remaining gap / 남은 간극

The cited odd-period bound does not exclude:

1. nontrivial cycles beyond the published floor;
2. aperiodic divergent trajectories;
3. the absence of a well-founded descent rank for every natural valuation
   code.

PrimeProject imports, but does not re-prove, the published period bound.

Next single lemma:
`PublishedFloorAwareAffineCappedNaturalCodeWellFoundedness`.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

Let `rho=(rho_0,...,rho_(2^d-1))` be a real or rational dyadic residual
vector. For each dyadic interval `I`, write

```text
mu_I = average of rho on I,
Delta_I = (mu_(left I)-mu_(right I))/2.
```

For every point `j`,

```text
rho_j = mu_root
        + sum_(dyadic I containing j) sigma(I,j) Delta_I,       (1)
```

where `sigma=+1` on the left child and `-1` on the right child. Hence

```text
|rho_j| <= |mu_root| + sum_(I containing j) |Delta_I|.          (2)
```

### Proof / 증명

At each level,

```text
mu_left  = mu_parent + Delta_parent,
mu_right = mu_parent - Delta_parent.
```

Following the unique dyadic path from the root to the singleton `{j}`
telescopes to (1). The triangle inequality gives (2). The generator replays
this identity at every point of exact rational vectors of sizes 4 through 64.

### Relation to orthonormal Haar coefficients / 정규직교 Haar 계수와의 관계

For the normalized Haar basis,

```text
c_root = sqrt(n) mu_root,
c_I    = sqrt(|I|) Delta_I.
```

Therefore the scale-normalized quantities entering (1) are

```text
c_root/sqrt(n), c_I/sqrt(|I|),
```

not the raw orthonormal coefficients themselves.

### Exact root-mode no-go / 정확 root-mode no-go

For the constant vector `rho_j=1`,

```text
mu_root=1,
all Delta_I=0,
c_root=sqrt(n),
all wavelet coefficients=0.
```

The pointwise signal remains below the Goldbach target `K=56`, but the raw
root coefficient exceeds 23 at the first audited dyadic size `n=2^10=1024`.
Thus a uniform cap of 23 on every raw orthonormal coefficient is a sufficient
linear-algebra condition but is not a scale-natural formulation of the
pointwise problem.

This auxiliary constant vector is not claimed to be an actual Goldbach
residual. It refutes only the use of a raw scale-independent Haar cap as the
primary or necessary arithmetic target.

### Remaining gap / 남은 간극

For the actual normalized binary Goldbach residual, no theorem here bounds
either

```text
|mu_root|
```

or every pointwise path sum

```text
sum_(I containing j) |Delta_I|
```

with total below 56 on every sufficiently large even dyadic block.

Next single lemma:
`UniformBinaryGoldbachRootMeanPlusDyadicPathVariationBelow56`.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

On the TICKET-142 cubic-rough pair support, let `N_(s,t)` count pairs with

```text
(lambda(n),lambda(n+2))=(s,t), s,t in {+1,-1}.
```

Define the Walsh coefficients

```text
A00 = sum 1,
A10 = sum lambda(n),
A01 = sum lambda(n+2),
A11 = sum lambda(n)lambda(n+2).
```

Then exact Walsh-Hadamard inversion gives

```text
N_(s,t) = (A00+s A10+t A01+st A11)/4.             (3)
```

### Proof / 증명

The four functions `1,s,t,st` are the character table of
`{+1,-1}^2`. Orthogonality of these four characters gives (3).

At cubic roughness, `lambda=-1` is equivalent to primality. Therefore

```text
N_(-1,-1) = pi_2[X,2X]
```

and

```text
A00-A10-A01+A11 = 4 pi_2[X,2X].                   (4)
```

### Circular-gap no-go / 순환 gap no-go

The TICKET-142 target

```text
A10+A01-A11 < A00
```

is, by (4), exactly equivalent to

```text
pi_2[X,2X] > 0.
```

It is not a weaker intermediate bridge. Proving it on every sufficiently
large dyadic block is already a blockwise form of the Twin Prime conclusion.
Calling the missing statement a “one-sided ledger gap” does not reduce its
logical strength.

### Stronger but non-circular sufficient condition / 더 강하지만 비순환적인 충분조건

The triangle inequality in (3) gives every parity class the lower bound

```text
N_(s,t) >= (A00-|A10|-|A01|-|A11|)/4.
```

Consequently, a fixed `delta>0` satisfying

```text
|A10|+|A01|+|A11| <= (1-delta) A00                (5)
```

for every sufficiently large block would force all four parity classes,
including twins, to be nonempty.

The finite exact rows give positive `(A00-L1)/A00` margins:

| `X` | `A00` | `|A10|+|A01|+|A11|` | exact positive margin ratio |
|---:|---:|---:|---:|
| 1,000 | 59 | 45 | `14/59` |
| 10,000 | 358 | 190 | `84/179` |
| 100,000 | 2,486 | 1,258 | `614/1243` |
| 1,000,000 | 17,634 | 9,174 | `1410/2939` |

These rows are finite evidence only. They do not prove a uniform positive
`delta`, and proving (5) for actual Liouville correlations still confronts the
sieve parity barrier.

Next single lemma:
`UniformCubicRoughWalshL1ContractionBelowOne`.

## Cross-problem conclusion / 문제 간 결론

**English.** TICKET-143 removes four hidden equivalences or topology errors:

1. RH finite sections require form-core density, not Hilbert density.
2. Collatz period 15,601 is below a published odd-period floor and should not
   consume the next computation budget.
3. Goldbach Haar coefficients must be normalized back to root means and
   martingale differences before they express a scale-stable pointwise target.
4. The Twin one-sided ledger gap is exactly the blockwise twin count, while a
   Walsh `L1` contraction is a genuinely stronger sufficient condition.

**한국어.** TICKET-143은 네 숨은 동치 또는 위상 오류를 제거한다.

1. RH 유한절단에는 Hilbert 조밀성이 아니라 form-core 조밀성이 필요하다.
2. Collatz 15,601주기는 공개 홀수 주기 하한보다 작아 다음 계산 예산을
   투입할 대상이 아니다.
3. Goldbach Haar 계수는 root 평균과 martingale 차이로 척도 정규화해야
   점별 목표가 된다.
4. Twin의 단측 ledger gap은 블록 쌍둥이 수와 정확히 같고, Walsh `L1`
   수축은 더 강하지만 실제로 비순환적인 충분조건이다.

The gain is proof-route precision, not a conjecture resolution.

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket143_form_core_period_floor_martingale_walsh.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket143_form_core_period_floor_martingale_walsh
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

Expected machine summary:

```text
exact_theorem_count=4
route_correction_count=4
proof_dag_count=4
conjecture_resolution_count=0
total_failure_count=0
```

## Literature boundary / 문헌 경계

- Christian Hercher,
  [There are no Collatz m-Cycles with m<=91](https://arxiv.org/abs/2201.00406).
  PrimeProject uses the paper's recorded `K>7.2*10^10` odd-member lower bound
  only as an external premise.
- Terence Tao,
  [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562).
  This almost-all theorem does not supply universal natural-code descent.
- Harald Helfgott,
  [The ternary Goldbach conjecture is true](https://arxiv.org/abs/1312.7748).
  Ternary Goldbach does not close the binary pointwise residual used here.
- D. H. J. Polymath,
  [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897).
  The parity discussion delimits why the Walsh contraction remains difficult.

PrimeProject claims only the exact TICKET-143 statements, replayable finite
rows, target corrections, and machine-audited claim boundaries.
