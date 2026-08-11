# TICKET-217: Relative Thresholds, Convergent Compression, Moment Support, and Critical Abel Tails

## Claim boundary

TICKET-217 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, strong Goldbach, or the Twin Prime conjecture. It proves four exact
partial, reduction, or no-go statements. All four parent problems remain
`open_not_proven`, and the machine resolution count is zero.

The ticket continues the four open lemmas from TICKET-216. Its main change is
to compare every observable with the scale of the discrete event that it must
detect, rather than with a fixed absolute tolerance.

| Problem | Exact result | Discarded route | Remaining gap | Next lemma |
| --- | --- | --- | --- | --- |
| Riemann | `MultiRadiusNormalizedDefectCertificateAndFinitePrecisionInvisibility` | finitely many fixed absolute-error Laplace samples | cofinal actual-zeta relative-precision enclosure | `CofinalRelativePrecisionExplicitFormulaEnvelopeBelowOne` |
| Collatz | `SingleMountainContinuedFractionCompressionAnd71356888Barrier` | linear scanning as the primary method | all upper convergents, then multi-run words and divergence | `EffectiveAllUpperConvergentScalingBarrierForSingleMountainWords` |
| Goldbach | `WeightedSecondMomentFullSupportCertificateAndSharpThresholdNoGo` | lowering the sharp Cauchy coefficient | pointwise lower-tail control beyond the certificate | `PointwiseGoldbachLowerTailBoundBeyondSecondMomentSupportBarrier` |
| Twin Prime | `SharpAdaptiveAbelTailPhaseTransitionAtTwoLogLog` | bounded offset as a negligible tail | actual Abel surplus over the critical constant | `TwinAbelLowerBoundWithExplicitSurplusAboveCriticalTailConstant` |

## 1. Riemann Hypothesis: normalized multi-radius detection

### Declared proposition

Let `C(H)` count off-critical zero symmetry pairs through height `H`, as in
TICKET-216, and let

```text
L(r) = integral r^t dC(t),       0 < r < 1.
```

For any finite family of radii `r_j`,

```text
C(H) <= floor(min_j L(r_j)/r_j^H).
```

The same conclusion holds with rigorous upper bounds `U_j>=L(r_j)`. Thus

```text
min_j U_j/r_j^H < 1
```

certifies `C(H)=0`.

Conversely, let finitely many positive absolute tolerances `epsilon_j` be
fixed. There is a finite `K` for which one atom at height `K` contributes

```text
r_j^K < epsilon_j
```

at every radius. Therefore no finite collection of fixed absolute-precision
Laplace observations can imply RH.

### Proof

TICKET-216 proved `C(H)r^H<=L(r)`. Apply the inequality to every radius,
divide by `r_j^H`, take the minimum, and use integrality of `C(H)`.

For the converse, `r_j^K` tends to zero for every `j`. Finiteness permits one
height larger than all individual tolerance thresholds. The unit atom at that
height is a nonzero defect measure hidden within every absolute error budget.

The generated examples use exact rational arithmetic. The delayed atoms are
logical measures, not claimed zeta zeros. The result does not weaken rigorous
finite-height verification such as the interval-arithmetic work of Platt and
Trudgian
([Bulletin of the London Mathematical Society](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/blms.12460)),
nor the later generalized verification method of Hiary, Ireland, and Kyi
([arXiv:2408.00187](https://arxiv.org/abs/2408.00187)).

### Remaining gap

The correct target is not another radius at fixed accuracy. It is a cofinal
actual-zeta explicit-formula enclosure whose normalized upper error stays
strictly below the moving first-atom threshold.

## 2. Collatz: continued-fraction compression

### Declared proposition

Suppose a positive accelerated Collatz cycle has the single-mountain valuation
word `1^k 2^m`. Put

```text
alpha = log(3/2)/log(4/3).
```

Then the reduced fraction `p/q=m/k` is an upper continued-fraction convergent
of `alpha`. For an upper convergent `p/q`, define

```text
Delta_0 = 2^(q+2p) - 3^(q+p).
```

If `Delta_0>=3^q`, no positive multiple `(m,k)=(gp,gq)` can satisfy the cycle
near-collision condition.

An exact audit verifies this scaling barrier for all seven upper convergents
through

```text
p/q = 6,306,641 / 4,474,633.
```

The next upper convergent is

```text
100,571,885 / 71,356,888.
```

Consequently, no single-mountain cycle can have

```text
k < 71,356,888.
```

This is a bound for one valuation-word family, not a bound for all Collatz
cycles.

### Proof of the convergent reduction

TICKET-215 gives

```text
0 < Delta = 2^(k+2m)-3^(k+m) <= 3^k-2^k.
```

Let

```text
lambda = m log(4/3)-k log(3/2).
```

Since `Delta=3^(k+m)(exp(lambda)-1)`,

```text
0 < exp(lambda)-1 < 3^(-m),
0 < m/k-alpha < 3^(-m)/(k log(4/3)).
```

Here `alpha>1`, so `m>=k+1`. The elementary inequality

```text
2k < 3^(k+1) log(4/3)
```

holds at `k=1` and its right-to-left ratio increases thereafter. Hence

```text
0 < m/k-alpha < 1/(2k^2).
```

After reducing `m/k` to `p/q`, the error remains below `1/(2q^2)`.
Legendre's theorem makes `p/q` a convergent. Its sign makes it an upper one.

### Proof of the multiple exclusion

For the reduced fraction, write

```text
lambda_0 = p log(4/3)-q log(3/2) > 0.
```

The exact comparison `Delta_0>=3^q` is equivalent to

```text
exp(lambda_0)-1 >= 3^(-p).
```

A multiple `g` would require

```text
exp(g lambda_0)-1 < 3^(-gp).
```

The left side is at least `exp(lambda_0)-1`, while the right side is at most
`3^(-p)`, a contradiction.

The continued-fraction coefficients are certified with rational upper and
lower bounds obtained from the positive atanh series for `log(3/2)` and
`log(4/3)`. Every displayed power comparison uses exact integers. Continued
fractions and linear forms in logarithms are established tools for cycle
bounds; compare Simons and de Weger
([Acta Arithmetica record](https://eudml.org/doc/278746)). No novelty or
priority claim is made without independent mathematical review.

### Remaining gap

The next upper convergent is not audited. More importantly, single-mountain
words do not cover multiple valuation runs, entries above two, or nonperiodic
divergence. A complete Collatz proof would have to address all three.

## 3. Strong Goldbach: a sharp support-moment certificate

### Declared proposition

Let `A_i>=0` be the Goldbach representation counts for `B` targets, and let
`w_i>0` be arbitrary normalizers. Define

```text
y_i = A_i/w_i,
S = sum_i y_i,
Q = sum_i y_i^2.
```

If

```text
S^2 > (B-1)Q,
```

then every target has at least one representation.

### Proof and sharpness

If one coordinate vanishes, at most `B-1` coordinates contribute.
Cauchy-Schwarz gives

```text
S^2 <= |support(y)| Q <= (B-1)Q.
```

The contrapositive proves full support. The vector

```text
(1,1,...,1,0)
```

has equality, so the coefficient `B-1` cannot be replaced by any smaller
universal coefficient in this Cauchy-form test.

### Computation and no-go

The exact raw-count margin is negative on the five audited dyadic blocks
starting at `128, 512, 2048, 8192, 32768`, even though direct enumeration
shows every count is positive. A Hardy-Littlewood-shaped normalization moves
the diagnostic ratio toward one, reaching approximately `0.999533` on the
largest block, but still does not cross the strict threshold.

The normalized rows are floating diagnostics, not rigorous interval
certificates. The theorem does not say that every possible deduction from two
moments is impossible. It proves the displayed Cauchy certificate and shows
that its universal coefficient is sharp. Higher moments, targetwise estimates,
and circle-method cancellation remain open routes. Exceptional-set results do
not by themselves prove an empty exceptional set; see Li
([Quarterly Journal of Mathematics](https://academic.oup.com/qjmath/article-pdf/50/200/471/4354525/500471.pdf)).

## 4. Twin Prime: the sharp adaptive Abel-tail transition

### Declared proposition

Use the TICKET-216 coefficient-one odd tail at

```text
r_X = 1-1/X,
Y_X = floor(c_X X),
R_X = r_X^n0/(1-r_X^2),
```

where `n0` is the first odd integer above `Y_X`. If

```text
c_X = 2 log log X + a_X,
```

assume `0<=c_X=o(X)`. Then, for bounded `a_X`,

```text
R_X/(X/log^2 X) = (1/2) exp(-a_X)(1+o(1)).
```

The same calculation gives the extended regimes:

- `a_X -> +infinity`: the geometric tail is `o(X/log^2 X)`;
- bounded `a_X`: the tail remains a nonzero constant multiple of that scale;
- `a_X -> -infinity` while `c_X>=0`: the tail dominates that scale.

### Proof

The first odd integer above the horizon satisfies `n0/X=c_X+o(1)`. Also,

```text
log(1-1/X) = -1/X + O(1/X^2),
1-r_X^2 = 2/X + O(1/X^2).
```

Therefore

```text
R_X = (X/2) exp(-c_X)(1+o(1)).
```

Substitution and division by `X/log^2 X` prove all three regimes. Decimal
audits for offsets `a=-2,0,2` converge to `exp(-a)/2` through `X=10^12`.

This sharpens the TICKET-216 phrase "about `2 log log X`" to an exact phase
transition. It does not supply a lower bound for the actual twin-prime Abel
transform and does not break the sieve parity barrier recorded by Polymath8
([arXiv:1407.4897](https://arxiv.org/abs/1407.4897)).

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket217_relative_threshold_convergent_moment_tail.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket217_relative_threshold_convergent_moment_tail -v
```

Primary machine artifact:

```text
data/open-problem/ticket217-relative-threshold-convergent-moment-tail.json
```

Per-problem artifacts are stored under `data/open-problem/{problem}/`.

## Final status

| Problem | New result | Resolution | Discarded path | Remaining gap | Next lemma |
| --- | --- | --- | --- | --- | --- |
| Riemann | normalized multi-radius certificate | open | finite fixed absolute precision | actual-zeta cofinal relative enclosure | `CofinalRelativePrecisionExplicitFormulaEnvelopeBelowOne` |
| Collatz | convergent compression and `k<71,356,888` exclusion | open | linear diagonal scanning | all upper convergents, multi-run words, divergence | `EffectiveAllUpperConvergentScalingBarrierForSingleMountainWords` |
| Goldbach | sharp weighted second-moment support certificate | open | smaller universal Cauchy coefficient | pointwise lower-tail estimate | `PointwiseGoldbachLowerTailBoundBeyondSecondMomentSupportBarrier` |
| Twin Prime | exact `2 log log X` tail phase transition | open | bounded-offset tail removal | parity-sensitive Abel surplus | `TwinAbelLowerBoundWithExplicitSurplusAboveCriticalTailConstant` |
