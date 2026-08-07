# TICKET-194: Dense-Core Extension, Ten-One Cycles, and Theta Layers

## 1. Claim boundary

TICKET-194 proves four intermediate theorems. It proves none of the Riemann
Hypothesis, the Collatz conjecture, strong Goldbach, or the Twin Prime
conjecture, and it finds no counterexample to a parent conjecture. The new
complete infinite family closed here is the accelerated Collatz valuation
stratum with exactly ten entries equal to one and every other entry equal to
two.

| Problem | Exact result proved here | Route discarded | Next single lemma |
|---|---|---|---|
| Riemann | `UniformlyBoundedDenseCoreQuadraticConvergenceExtendsEverywhere` | positivity and monotonicity on a dense core as a replacement for uniform boundedness | `PoleNeutralWeilFiniteSectionsAreUniformlyBoundedAndConvergeOnADenseCore` |
| Collatz | `ExactlyTenValuationOnesOtherwiseTwoCycleExclusion` | the ten-one/rest-two stratum as a cycle source | `NoContractingValuationWordWithExactlyElevenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| Goldbach | `OddPrimePowerThetaLayerCompressionAndBinaryMassClassification` | treating `O(sqrt(N) log^2 N)` as the intrinsic contamination scale | `BinaryCorrelationExceedsThetaLayerPrimePowerEnvelopeForEveryLargeEvenTarget` |
| Twin Prime | `OddPrimePowerIntervalThetaLayerCompression` | treating `O(sqrt(X) log^2 X)` as the intrinsic shift-two contamination scale | `ShiftTwoCorrelationExceedsThetaLayerOddLocalEnvelopeOnInfinitelyManyDyadicBlocks` |

Reproduce with:

```powershell
D:\python\anaconda3\python.exe scripts\ticket194_densecore_tenone_theta_layers.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket194_densecore_tenone_theta_layers -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

The integrated machine-readable result is
`data/open-problem/ticket194-densecore-tenone-theta-layers.json`. All four
attempts remain `open_not_proven`; the resolution count is `0 / 4`.

## 2. Riemann Hypothesis

### 2.1 Declared proposition

Let `q_n` be continuous Hermitian quadratic forms on a complex Hilbert space
`H`, with associated bounded Hermitian forms `B_n`. Let `D` be dense in `H`.
If

```text
sup_n ||B_n|| <= M < infinity
```

and `q_n(u)` converges for every `u in D`, then `B_n(x,y)` and `q_n(x)`
converge for every `x,y in H`. Their limit is a bounded Hermitian form of norm
at most `M`; positivity passes to the limit.

### 2.2 Proof

Complex polarization converts diagonal convergence on `D` into convergence of
`B_n(u,v)` for every `u,v in D`. For `u,v in D` approximating `x,y in H`,

```text
|(B_n-B_m)(x,y)-(B_n-B_m)(u,v)|
 <= 2M(||x-u|| ||y|| + ||u|| ||y-v||).
```

Choose `u,v` first so the right side is small, then choose `n,m` so the core
term is small. Thus `B_n(x,y)` is Cauchy everywhere. The same uniform norm
bound passes to the limit.

### 2.3 Stronger dense-core no-go

On `H=l^2` and `D=c_00`, define

```text
q_n(x)=sum_(k<=n) k|x_k|^2.
```

These forms are positive and increase monotonically. For each `x in c_00`
they eventually stabilize, but `||B_n||=n`. Define an all-space witness by

```text
|x_(2^j)|^2=2^(-j),  x_k=0 otherwise.
```

Its squared norm is one, whereas `q_(2^J)(x)=J`. Therefore positivity,
monotonicity, and dense-core convergence together do not replace the uniform
operator bound.

### 2.4 Remaining gap

The actual pole-neutral Weil finite sections have not been proved uniformly
bounded and convergent on a dense core of one admissible Hilbert completion.
The theorem completes the extension mechanism only after those arithmetic
premises are supplied.

## 3. Collatz conjecture

### 3.1 Declared proposition

No positive accelerated Collatz cycle has exactly ten valuations equal to one
and every other valuation equal to two, including primitive and imprimitive
displayed periods.

### 3.2 Contracting range

For a word of length `h`, the valuation sum is `2h-10` and the affine
denominator is

```text
D_h=2^(2h-10)-3^h.
```

It is nonpositive through `h=24` and positive from `h=25`. Rotate the word so
one of its ten ones is first. Since `D_h` is odd and cyclic shifts satisfy the
same affine divisibility condition, this normalization loses no candidate.

### 3.3 Nine-boundary decomposition and exact 5+4 MITM

For normalized positions

```text
0=p_0<p_1<...<p_9<h,
```

the recurrence numerator separates exactly into one horizon-dependent constant
and nine one-position boundary terms. The implementation validates this
identity against the original affine recurrence on all 8,008 normalized words
for `h=10,...,16`.

The finite contracting range `h=25,...,38` is then split into five left and
four right boundary terms. A residue table activates exactly those left tuples
whose last position precedes the first right position. Consequently the number
of represented words is exactly

```text
sum_(h=25)^38 C(h-1,9)
 = C(38,10)-C(24,10)
 = 470,772,500.
```

Only 2,626,085 left tuples and 225,708 right queries are required. Exact Python
integers and hash membership are used. No divisibility hit occurs; per-horizon
SHA-256 transcripts make the finite decision reproducible.

### 3.4 Infinite tail

Every state in a nontrivial positive odd cycle is at least three. Multiplying
the step ratios gives

```text
1 <= 2^10(5/6)^h = 1024(5/6)^h.
```

The right side is still above one at `h=38`, is strictly below one at `h=39`,
and decreases thereafter. Thus the finite MITM and analytic tail cover every
length.

### 3.5 Remaining gap

Exactly eleven or more ones, valuations at least three, and aperiodic divergent
trajectories remain untreated. Closing a growing list of periodic strata does
not by itself prove global Collatz convergence.

## 4. Strong Goldbach conjecture

### 4.1 Exact theta-layer identity

Let

```text
W_odd(Y)=sum log p,
```

where the sum runs over odd proper prime powers `p^k<=Y`, `k>=2`. Then

```text
W_odd(Y)=sum_(k>=2) theta_odd(floor(Y^(1/k))).
```

This is an exact finite identity: exchange the finite sums over prime bases and
exponents. The code uses exact integer `k`th roots, so a prime power lying on a
root boundary cannot be lost by floating-point rounding.

### 4.2 Analytic scale

The only external analytic input here is the classical Chebyshev estimate
`theta(t)=O(t)`. The `k=2` layer is `O(sqrt Y)`. There are `O(log Y)` remaining
layers, each at most `O(Y^(1/3))`, and

```text
Y^(1/3) log Y = O(sqrt Y).
```

Therefore

```text
W_odd(Y)=O(sqrt Y).
```

Inserted into the exact TICKET-193 parity envelope, proper-prime-power
contamination is `O(sqrt(N) log N)`. This removes one logarithm from the
earlier elementary majorant, but it does not estimate the binary correlation
from below.

### 4.3 Exact binary mass

For even `N>=6`, binary uniqueness gives the exact power-of-two contribution:

- one ordered pair if `N` is a power of two;
- two ordered pairs if the binary expansion of `N` has exactly two one-bits;
- no pair otherwise.

Each ordered pair has von Mangoldt weight `(log 2)^2`. Direct enumeration and
the binary rule agree on every audited target.

### 4.4 Finite computation and remaining gap

The theta layers exactly reconstruct the odd proper-power mass for all eleven
targets `2^10,...,2^20`; every finite correlation exceeds its exact envelope.
This finite prefix does not prove that every sufficiently large even target
does so. That universal pointwise lower bound is the next lemma.

## 5. Twin Prime conjecture

### 5.1 Exact interval identity

Subtracting two cumulative theta-layer identities gives, for every integer
interval `[A,B)`,

```text
W_odd([A,B))
 = sum_(k>=2) [
     theta_odd(floor((B-1)^(1/k)))
     -theta_odd(floor((A-1)^(1/k)))
   ].
```

Applied to `[X,2X)` and `[X+2,2X+2)`, this is the exact odd-only contamination
input from TICKET-193. Both cumulative masses are `O(sqrt X)`, so the
shift-two contamination envelope is

```text
O(sqrt X log X).
```

### 5.2 Finite computation and remaining gap

All sixteen blocks `X=2^j`, `j=4,...,19`, have exact left and translated right
theta reconstructions, and their correlations exceed the exact local
envelopes. A finite list cannot establish infinitely many successful blocks.
No lower bound above this envelope is proved on an unbounded block sequence.

## 6. Synthesis

TICKET-194 makes three different quantifier reductions explicit. Uniform
boundedness promotes dense-core convergence to a complete Hilbert space.
Boundary separation compresses 470 million Collatz words without weakening
coverage. Theta layers convert prime-power enumeration into exact root-scale
arithmetic and identify the correct sublinear contamination scale. The open
premises are now sharper, but none is supplied by finite computation.
