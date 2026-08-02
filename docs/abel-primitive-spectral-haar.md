# TICKET-183: Abel Transfer, Primitive Collatz Words, Fourier Margins, and Haar Paths

## Abstract

TICKET-183 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, the strong Goldbach conjecture, or the Twin Prime conjecture. It
continues the four open nodes of TICKET-182 and proves four exact intermediate
results:

1. an Abel-Fejer-H1 certificate must include an explicit desmoothing remainder;
2. repeated Collatz valuation words reduce exactly to their primitive root, and
   the entire `v_j >= 2` stratum contains only the fixed point;
3. a finite Fourier major/minor decomposition has an exact pointwise positivity
   margin, while a constant-density sparse model is blocked by Parseval;
4. weighted Haar energy equals leaf variance, but positivity requires pathwise
   negative square-function control rather than global energy.

Each section declares the proposition, proves it, gives a reproducible finite
diagnostic, identifies a rejected inference, and states one next lemma. All four
conjecture-resolution counters remain zero.

## Status ledger

| Problem | Exact result closed here | Rejected route | Decisive remaining lemma |
|---|---|---|---|
| Riemann | `AbelFejerDesmoothingCertificateAndHighFrequencyNoGo` | smoothed H1 energy without desmoothing control | `PoleNeutralWeilTestConeHasUniformAbelDesmoothingModulus` |
| Collatz | `PrimitiveWordReductionAndMonotoneValuationExclusion` | repeated-word counting or any fixed search horizon | `NoPrimitiveContractingValuationWordContainingOneSatisfiesAffineDivisibility` |
| Goldbach | `ExactFourierErrorIdentityAndSparseDensityNoGo` | constant prime density plus an absolute spectral budget | `GoldbachMajorMinorPhaseErrorIsUniformlyBelowSingularSeriesMargin` |
| Twin Prime | `WeightedHaarVarianceIdentityAndNegativePathSquareCertificate` | global Haar energy as every-path control | `PrimePairNegativeHaarPathSquareStaysBelowRootMargin` |

## 1. Riemann Hypothesis

### Declared proposition

Let

```text
f(theta) = sum_k a_k exp(i k theta)
```

have absolutely summable Fourier coefficients, and let `A_rho f` be its Abel
regularization with coefficients `rho^|k| a_k`, where `0 < rho < 1`. For the
Fejer mean `sigma_N`, define

```text
D_rho^2 = sum_k k^2 rho^(2|k|) |a_k|^2,
R_rho   = sum_k |1-rho^|k|| |a_k|.
```

Then

```text
||f||_infinity
  <= ||sigma_N A_rho f||_infinity + C_N D_rho + R_rho,

C_N^2 = 2 ((N-1)/N^2 + sum_(k>=N) 1/k^2).
```

The term `R_rho` cannot be removed. For fixed `rho < 1`, `N < M`, and
`f_M(theta)=cos(M theta)`, the low-pass term vanishes and `D_rho` tends to zero
as `M` tends to infinity, while `||f_M||_infinity=1` and
`R_rho=1-rho^M` tends to one.

### Proof

Insert the regularized function and its Fejer mean:

```text
f = (f-A_rho f) + (A_rho f-sigma_N A_rho f) + sigma_N A_rho f.
```

The triangle inequality gives three terms. Absolute summability bounds the first
by `R_rho`. Parseval identifies the normalized derivative energy of `A_rho f`
with `D_rho^2`; the TICKET-182 Fejer multiplier argument bounds the second term
by `C_N D_rho`. This proves the certificate.

For the counterfamily, Abel regularization multiplies the cosine by `rho^M`.
When `M >= N`, its Fejer mean is zero and its derivative norm is
`M rho^M/sqrt(2)`, which converges to zero. The original norm remains one. Thus
small regularized energy is not a certificate for the unregularized function.

### Reproducible diagnostic

At `rho=0.9` and `N=16`:

| M | Smoothed-only certificate | Desmoothing remainder | Full upper bound |
|---:|---:|---:|---:|
| 32 | 0.385494 | 0.965663 | 1.351157 |
| 64 | 0.026473 | 0.998821 | 1.025294 |
| 128 | 0.000062 | 0.999999 | 1.000061 |
| 256 | `1.74e-10` | `1-1.93e-12` | 1.0000000002 |

The Abel-smoothed finite prime proxy with cosine coefficients
`Lambda(n)/sqrt(n)` has finite derivative energy at every fixed `rho < 1`, but
at cutoff 100,000 its derivative norm rises from about `4.42` at `rho=0.90` to
`71.41` at `rho=0.99`. Its finite-cutoff desmoothing `l1` remainder remains over
`614`. This proxy is not the pole-neutral Weil symbol and proves no zero
exclusion.

### Logical boundary

Weil positivity is posed on a constrained test-function cone; the moment
conditions cannot be dropped or assumed to survive regularization. Connes and
Consani explicitly retain two such conditions in their operator-theoretic
formulation ([The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368)).
TICKET-183 therefore rejects **smoothing-only transfer**, not Abel smoothing.

**Next lemma:**
`PoleNeutralWeilTestConeHasUniformAbelDesmoothingModulus`.

## 2. Collatz conjecture

### Declared proposition

For a positive valuation word `u=(v_0,...,v_(h-1))`, write

```text
F_u(n) = (3^h n + B(u))/2^S,
S = sum_j v_j,
D(u) = 2^S-3^h.
```

If `w=u^r` is the concatenation of `r` copies of `u`, then one positive integer
`Q_r` satisfies

```text
D(w) = D(u) Q_r,
B(w) = B(u) Q_r.
```

Consequently, `D(w) | B(w)` if and only if `D(u) | B(u)`. Moreover, if every
valuation in a positive accelerated cycle satisfies `v_j >= 2`, then the cycle
is the fixed point `n=1` and its word is `(2,...,2)`.

### Proof

Write `a=3^h`, `b=B(u)`, and `c=2^S`. Iterating
`F_u(n)=(a n+b)/c` gives

```text
F_u^r(n)
 = (a^r n + b sum_(j=0)^(r-1) a^(r-1-j)c^j)/c^r.
```

The same geometric sum factors `c^r-a^r`, proving both identities and the
divisibility equivalence.

For the second statement, an exact accelerated step with `v >= 2` obeys

```text
(3n+1)/2^v <= (3n+1)/4 < n       for odd n>1.
```

Every step from an odd value greater than one is strictly decreasing, which is
incompatible with a cycle. At `n=1`, `3n+1=4`, so the exact valuation is two and
the orbit remains fixed.

### Reproducible diagnostic

- The factorization was checked for primitive roots `(2)`, `(1,2,3)`, and
  `(1,2,2)` with repetition counts up to four or five.
- All 488,280 words over valuations `1,...,5` through length eight were
  classified.
- 87,380 words lie in the `v_j >= 2` stratum; no non-fixed divisibility hit
  occurs there.
- 399,524 checked words are primitive, contracting, and contain valuation one.

Finite search is not exhaustive. For every `h >= 3`, the word

```text
w_h = (1,2,...,2),   S=2h-1
```

is primitive and satisfies `2^S>3^h`. The family therefore supplies primitive
contracting candidates at unbounded horizons. It does not supply a cycle because
the required divisibility is not established.

### Logical boundary

The exact remaining stratum is now smaller but still infinite: primitive,
contracting words containing `v=1`. Almost-all orbit control does not exclude
every member of this arithmetic set; Tao's theorem is explicitly an almost-all
statement in logarithmic density
([Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)).

**Next lemma:**
`NoPrimitiveContractingValuationWordContainingOneSatisfiesAffineDivisibility`.

## 3. Strong Goldbach conjecture

### Declared proposition

On `Z/LZ`, use normalized convolution and Fourier transform. Write the prime
signal or another nonnegative signal as `f=g+h`, where `g` is a proposed major
model. Then

```text
f*f = g*g + E,
E_hat(k) = 2 g_hat(k) h_hat(k) + h_hat(k)^2.
```

Therefore every target has positive convolution whenever

```text
min_x (g*g)(x)
  > sum_k |2 g_hat(k) h_hat(k) + h_hat(k)^2|.
```

For an indicator `f` of density `alpha` and the constant model `g=alpha`, the
right-hand budget equals `alpha(1-alpha)` by Parseval, while the model margin is
`alpha^2`. This certificate cannot pass when `alpha <= 1/2`.

### Proof

The convolution theorem gives the coefficient identity. Fourier inversion and
the triangle inequality bound `|E(x)|` by the coefficient `l1` norm uniformly
in `x`. Subtracting this error from the minimum major-model convolution proves
the positivity certificate.

For the constant model, `h` has zero mean. The cross terms vanish, and
Parseval gives

```text
sum_(k != 0) |h_hat(k)|^2 = alpha(1-alpha).
```

Comparing this exact budget with `alpha^2` proves the no-go.

### Reproducible diagnostic

Three smooth finite models at lengths 32, 64, and 128 pass the exact
certificate with Fourier reconstruction error below `1e-10`. Cyclic odd-prime
indicators give the following constant-model obstruction:

| L | Density | Model margin | Parseval budget | Budget / margin |
|---:|---:|---:|---:|---:|
| 64 | 0.468750 | 0.219727 | 0.249023 | 1.1333 |
| 128 | 0.414063 | 0.171448 | 0.242615 | 1.4151 |
| 256 | 0.375000 | 0.140625 | 0.234375 | 1.6667 |
| 512 | 0.333984 | 0.111546 | 0.222439 | 1.9942 |

Exact enumeration found no counterexample for even targets `6 <= n <= 50,000`;
the minimum unordered odd-prime representation count is one. The omitted target
four is separately `2+2`. This bounded computation is not an infinite proof.

### Logical boundary

The no-go rules out only a phase-blind constant model. It points toward the
arithmetic singular series and signed target phases, not away from the circle
method. Current exceptional-set work still distinguishes major-arc formulas from
control of every target
([Grimmelt and Bhowmik, 2026](https://arxiv.org/abs/2607.27282)).

**Next lemma:**
`GoldbachMajorMinorPhaseErrorIsUniformlyBelowSingularSeriesMargin`.

## 4. Twin Prime conjecture

### Declared proposition

Let dyadic leaves carry masses `m_i>0` and ratios `r_i`. Every parent ratio is
the mass-weighted mean of its children. Then

```text
sum_i m_i (r_i-r_root)^2
 = sum_(internal I) [m_L m_R/(m_L+m_R)] (r_L-r_R)^2.
```

For a root-to-leaf path of depth `d`, let

```text
Q_minus = sum_j min(r_child(j)-r_parent(j),0)^2.
```

The leaf satisfies

```text
r_leaf >= r_root-sqrt(d Q_minus).
```

Thus a positive right-hand side certifies positivity of that leaf.

### Proof

The two-child identity is the weighted law of total variance. Recursion over the
tree proves the global Haar formula. Along a path, discard positive increments
and apply Cauchy-Schwarz to at most `d` negative increments. This proves the
path certificate.

Global energy cannot replace the path hypothesis. Give `2^d-1` leaves ratio one,
one leaf ratio zero, and every leaf mass `2^(-d)`. The root tends to one and

```text
global Haar energy = (2^d-1)/2^(2d) -> 0,
```

but the selected leaf remains zero and its negative path-square tends to `1/3`.

### Reproducible diagnostic

The counterfamily was checked at depths 4, 8, 12, and 16. At depth 16, global
energy is about `1.53e-5`, while the bad leaf is still zero and its negative
path-square is about `0.3333333333`.

For actual twin-prime starts in `[100000,362144)`, grouped into 256 leaves of
width 1,024 and normalized by Hardy-Littlewood expected mass:

| Quantity | Value |
|---|---:|
| actual twin pairs | 2,298 |
| root actual/expected ratio | 1.000378 |
| weighted leaf variance | 0.078545 |
| summed Haar energy | 0.078545 |
| identity error | `2.78e-17` |
| maximum negative path-square | 0.357149 |
| minimum actual leaf ratio | 0.119937 |
| minimum certified lower bound | -0.689945 |

The leaves happen to be positive in this finite interval, but the uniform path
certificate fails. Neither observation is a future-block lower bound. Maynard's
survey documents the gap between bounded-gap advances and the exact twin-prime
claim ([On the Twin Prime Conjecture](https://arxiv.org/abs/1910.14674)).

**Next lemma:**
`PrimePairNegativeHaarPathSquareStaysBelowRootMargin`.

## Cross-problem conclusion

The four no-go results have the same logical form:

```text
regularized / averaged control
        + missing uniform transfer term
        != pointwise arithmetic conclusion.
```

TICKET-183 identifies that transfer term in each representation. It does not
prove that any arithmetic object satisfies the required uniform estimate.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket183_abel_primitive_spectral_haar.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket183_abel_primitive_spectral_haar -v
```

Machine artifact:
`data/open-problem/ticket183-abel-primitive-spectral-haar.json`.
