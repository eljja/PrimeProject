# TICKET-175: relative spectral resolution, Collatz-equivalent zero lifts, signed Farey minors, and Haar block operators

## Claim boundary

TICKET-175 continues the four OPEN nodes left by TICKET-174. It proves four
exact reductions or no-go statements. It does **not** prove or disprove the
Riemann Hypothesis, the Collatz conjecture, strong Goldbach, or the Twin Prime
conjecture. Every problem remains `open_not_proven`; the machine resolution
count is zero.

| Problem | Exact TICKET-175 result | Rejected route | Next single lemma |
|---|---|---|---|
| Riemann | absolute tail-margin resolution barrier | polynomial-cutoff absolute norm resolves a super-small spectral edge | `StructuredRelativeWeilCoreErrorPreservesNonnegativityBelowGroundStateScale` |
| Collatz | eventual zero-lift non-descent exclusion is Collatz-equivalent | treating that exclusion as a weaker intermediate lemma | `EveryAperiodicNaturalValuationRayCrossesItsCorrectedLogDescentBoundary` |
| Goldbach | an absolute minor budget loses exactly twice the positive minor mass | fixed-Farey L1 minor control retains signed cancellation | `FixedFareySignedMinorDeficitPowerSavingBelowMajorMainUniformly` |
| Twin Prime | the full operator is dominated by a Haar block-norm scale matrix | every scale pair must separately satisfy a Frobenius-energy saving | `PrimePairHaarBlockNormScaleMatrixHasUniformPowerSavingOperatorNorm` |

## 1. Riemann: absolute spectral resolution is the wrong scale

### Declared proposition

Let `A` be Hermitian and let a truncated approximation `A_T` satisfy

```text
||A-A_T||_op <= B(T).
```

Weyl's variational inequality gives

```text
lambda_min(A) >= lambda_min(A_T)-B(T).
```

Consequently this absolute-error route certifies nonnegativity only when a
rigorous finite lower margin exceeds the error radius. For the explicit
TICKET-174 bound and a fixed `k>1`, substituting `T=N^k` gives

```text
U_N(N^k) = O(N^(1-k) log N).
```

It therefore cannot resolve a margin that is smaller than every inverse power
of `N`. This statement concerns this certificate, not the exact Weil form.

### Proof

The first inequality follows by minimizing the Rayleigh quotient after applying
the operator-norm perturbation bound. The displayed asymptotic follows directly
from the explicit Corollary 3.3 tail expression because `N/T=N^(1-k)` and
`log T=k log N`. A scalar approximate eigenvalue zero with absolute error
`epsilon` is compatible with both exact values `+epsilon` and `-epsilon`, so no
sign follows without a margin larger than the radius.

### Reproducible scale audit

The recent public Galerkin calculation reports smallest-positive even-sector
branch magnitudes at `c=100`. They are numerical values and Galerkin upper
bounds, not certified lower margins. TICKET-175 uses them only as target
resolution scales and solves the explicit tail equation `U_N(T)=10^-d` in log
coordinates.

| N | reported `d=-log10|lambda|` | `log10 U_N(N^2)` | `log10 U_N(N^3)` | required `log10 T` |
|---:|---:|---:|---:|---:|
| 100 | 190.92 | -1.240 | -3.084 | 195.319 |
| 150 | 247.19 | -1.386 | -3.403 | 251.874 |
| 200 | 294.31 | -1.490 | -3.631 | 299.194 |
| 250 | 333.68 | -1.571 | -3.808 | 338.714 |

The calculation says that this particular explicit absolute upper-bound route
would need astronomical `T`. It does not say that the exact tail is that large,
and it does not exclude structured or relative estimates.

### Remaining gap

The next lemma must preserve sign without resolving a tiny spectral edge in
absolute norm. Plausible forms include a relative quadratic-form inequality, a
positive factorization, or a structure-aware comparison on the pole-neutral
constraint core.

## 2. Collatz: the selected OPEN node is the conjecture in disguise

### Declared proposition

For the accelerated odd Collatz map `T`, the following are equivalent:

1. every positive integer reaches `1`;
2. every odd `n>1` has an `h` such that `T^h(n)<n`;
3. no natural accelerated orbit remains at least its start at every time.

After a natural cylinder ray stabilizes at `n`, its next edge is precisely the
unique zero-lift child from TICKET-174. Therefore

```text
NoNonDescendingRayEventuallyFollowsUniqueZeroLiftChildren
```

is Collatz-equivalent, rather than a strictly easier intermediate theorem.

### Proof

If the Collatz conjecture holds, the orbit reaches `1<n`. Conversely, assume
every odd `n>1` reaches a smaller odd integer. Strong induction on `n` then
sends every odd integer to `1`; removing powers of two handles even integers.
Negating the descent statement gives an orbit that never goes below its start.

For a natural valuation prefix, once its cylinder modulus exceeds `n`, the
integer `n` is the least positive representative of that residue class. Every
later actual extension consequently has lift quotient zero, and TICKET-174
proves that this child is unique.

The exact logarithmic coordinate used by the computation is

```text
log2(T^h(n)/n)
  = h log2(3) - S_h
    + sum_(i<h) log2(1 + 1/(3 T^i(n))).
```

Descent occurs exactly when the right-hand side becomes negative.

### Reproducible finite audit

| odd start limit | odd starts checked | failures to descend | largest first-descent horizon | record start |
|---:|---:|---:|---:|---:|
| 1,000 | 499 | 0 | 51 | 703 |
| 10,000 | 4,999 | 0 | 51 | 703 |
| 100,000 | 49,999 | 0 | 85 | 35,655 |
| 1,000,000 | 499,999 | 0 | 111 | 626,331 |

This finite result is not an all-integer theorem. Its role is to verify the
coordinate identity and prevent an equivalent restatement from being counted
as progress.

### Remaining gap

The next target isolates aperiodic rays and asks for one prefix crossing of the
exact corrected logarithmic boundary. Nontrivial cycles remain a separate gap.

## 3. Goldbach: the exact price of taking absolute minor mass

### Declared proposition

Fix a Fourier major set `M` before inspecting target-aligned signs. Write the
exact convolution at an even target as

```text
R = Major + P_minor - N_minor,
```

where `P_minor,N_minor>=0` are the positive and negative aligned minor masses.
The triangle-inequality certificate has margin

```text
Major - P_minor - N_minor = R - 2 P_minor.
```

Thus an L1 minor bound charges every helpful positive minor term twice.

### Proof

The first identity is Fourier inversion split over a predeclared major mask and
the signs of its complement. Subtracting the absolute-minor lower bound from
the exact signed expression gives `2 P_minor`. No probabilistic or asymptotic
assumption is used.

### Fixed Farey calculation

The masks contain bins within two frequency cells of reduced rational centers
with denominator `q<=Q`. The masks are chosen before each target phase.

| prime support | targets | Q=16 absolute certificates | pass fraction |
|---:|---:|---:|---:|
| 64 | 31 | 31 | 1.000 |
| 128 | 63 | 56 | 0.889 |
| 256 | 127 | 82 | 0.646 |
| 512 | 255 | 89 | 0.349 |
| 1,024 | 511 | 109 | 0.213 |

All 987 exact Fourier reconstructions and double-loss identities passed. The
decreasing finite fraction does not prove asymptotic failure. The theorem-level
conclusion is only that replacing signed minor cancellation by its full L1 mass
loses exactly the positive minor contribution twice.

### Remaining gap

A valid binary Goldbach route needs a target-uniform positive major main term
and a genuinely signed minor-deficit estimate. Exact finite signed sums cannot
serve as the analytic estimate because they already contain the desired answer.

## 4. Twin Prime: compress all scale pairs before bounding them

### Declared proposition

Decompose the nonconstant Haar domain and range into orthogonal scale spaces and
let `A_jk` be the corresponding operator blocks. Define the scalar matrix

```text
B_jk = ||A_jk||_op.
```

Then

```text
||A||_op <= ||B||_op.
```

This can recover the full `log2 N` loss in TICKET-174. A projection onto one
wavelet at each matched scale has physical norm one and `B=I`, while the prior
largest-block aggregation bound equals `log2 N`.

### Proof

Write `x` as orthogonal scale components `x_k` and set `y_k=||x_k||`. The norm
of output block `j` is at most `sum_k B_jk y_k`. Taking the Euclidean norm over
all output scales gives

```text
||Ax|| <= ||B y|| <= ||B||_op ||x||.
```

For the matched projection, Haar coordinates make both the full operator and
the scale matrix orthogonal projections. Haar conjugation preserves operator
norm and exclusion of the constant coordinate gives zero row and column sums.

### Finite Type-II diagnostics

| X | physical norm | block-scale norm | Frobenius norm |
|---:|---:|---:|---:|
| 10,000 | 127.62 | 128.95 | 130.42 |
| 100,000 | 4,325.60 | 4,797.48 | 4,897.25 |
| 1,000,000 | 92,730.91 | 100,752.42 | 100,972.27 |
| 10,000,000 | 4,499,308.11 | 4,516,032.93 | 4,792,699.11 |

These are finite centered rough-semiprime matrices, not prime-pair asymptotics.
They verify the block domination and show that the block-scale norm can be
closer to the physical norm than the Frobenius aggregation.

### Remaining gap

The next lemma asks for a uniform power saving in the operator norm of the
arithmetic block-norm scale matrix. It is weaker than separate Frobenius savings
for every scale pair but still requires genuine Type-II information.

## Cross-problem conclusion

All four corrections preserve structure before taking an absolute bound:

1. RH needs relative or sign-preserving spectral control, not only absolute error.
2. Collatz needs a genuinely weaker intermediate statement, not an equivalent rename.
3. Goldbach needs signed minor cancellation, not complete L1 loss.
4. Twin Prime can aggregate scale blocks through their operator geometry.

## Literature boundary

- [Groskin, High-Precision Approximation of Riemann Zeros via the Truncated Weil Form](https://arxiv.org/abs/2605.20224) reports the finite branch scales and explicitly makes no RH claim.
- [Groskin, finite Guinand-Weil dictionary and archimedean tail order](https://arxiv.org/abs/2607.02828) provides the explicit tail upper bound.
- [Lagarias, The 3x+1 Problem: An Overview](https://arxiv.org/abs/2111.02635) surveys stopping-time formulations; [Tao](https://arxiv.org/abs/1909.03562) proves an almost-all result rather than every-input descent.
- [Grimmelt and Bhowmik, The exceptional set of the Goldbach problem](https://arxiv.org/abs/2607.27282) gives explicit major-arc context but not the signed uniform binary estimate above.
- [Ford and Maynard, On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368) establishes the need for substantial Type-II information.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket175_relative_equivalence_signed_block.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket175_relative_equivalence_signed_block -v
```

The canonical machine-readable artifact is
`data/open-problem/ticket175-relative-equivalence-signed-block.json`.
