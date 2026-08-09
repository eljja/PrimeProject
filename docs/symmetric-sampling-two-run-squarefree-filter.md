# TICKET-199: Symmetric Sampling, Two-Run Obstruction, and the Squarefree-Lambda Filter

## Abstract

TICKET-199 continues the four-track proof-or-counterexample program without
claiming a solution to any parent conjecture. It establishes four exact
project-local results.

1. Finite boundary point samples cannot, by themselves, certify a zero-free
   Rouché rectangle even among real even entire functions.
2. The explicit `r=2` primitive Collatz family introduced by TICKET-198 fails
   affine divisibility at every scale `k>=2`.
3. `P(n)=mu(n)^2 Lambda(n)` is an exact prime projector, so its additive
   convolution eliminates Goldbach prime-power collisions identically.
4. The same projector gives the exact prime-power-free localized Twin Prime
   detector requested by TICKET-198.

All four conjectures remain `open_not_proven`. The machine-readable result is
[`ticket199-symmetric-sampling-two-run-squarefree-filter.json`](../data/open-problem/ticket199-symmetric-sampling-two-run-squarefree-filter.json).

## Claim table

| Problem | Exact result | Rejected or corrected route | Single next lemma |
|---|---|---|---|
| RH | `FiniteBoundarySamplingNoGoForRealEvenRoucheCertification` | finitely many point evaluations as a standalone Rouché certificate | `IntervalBoundaryMeshWithDerivativeBoundCertifiesStrictRoucheMarginOnD3` |
| Collatz | `TwoRunPairPrimitiveFamilyAffineDivisibilityObstruction` | retaining the explicit `r=2` family as a possible positive cycle family | `ThreeRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales` |
| Goldbach | `MobiusSquarefreeLambdaExactGoldbachPrimeProjector` | treating proper-prime-power collision support as intrinsic to the final detector | `UniformPositiveLowerBoundForMobiusSquarefreeGoldbachCorrelationAtEverySufficientlyLargeEvenTarget` |
| Twin Prime | `MobiusSquarefreeLambdaExactTwinPrimeDetector` | subtracting prime-power contamination after exact prime projection | `ParityBreakingPositiveLowerBoundForMobiusSquarefreeLambdaShiftTwoCorrelationOnInfinitelyManyDyadicBlocks` |

## 1. Riemann Hypothesis

### Declared proposition

Let `S` be a finite subset of the boundary of `D_3^+`, enlarged under sign and
complex conjugation. Choose an interior point `a` outside that finite orbit with
`Im(a^2) != 0`. There is a real even polynomial `G` such that

```text
G(s) = 1 for every s in S,
G(a) = 0.
```

Therefore finite point samples, without a certified between-sample bound, do
not establish zero-freeness or a strict Rouché inequality.

### Exact construction

Let `R` contain the squared sample points and their conjugates and put

```text
Q(z) = product_(rho in R) (z^2-rho).
```

Then `Q` is real and even and vanishes at every sample. Since `1` and `a^2`
span the complex plane over the reals, there are unique real `u,v` satisfying

```text
u + v a^2 = -1/Q(a).
```

Thus `G(z)=1+Q(z)(u+v z^2)` has the required properties. The generator uses
`a=1+i` and four rational boundary meshes. Every equality is checked with
`Fraction`, not floating-point arithmetic.

### Boundary

This is not an RH counterexample because `G` is not Xi. It also does not reject
interval arithmetic, derivative-controlled meshes, or analytic modulus bounds.
It rejects only the promotion of finitely many point evaluations to a full
boundary certificate.

## 2. Collatz conjecture

### Declared proposition

For every `k>=2`, consider the TICKET-198 word

```text
w_k = 1^k 2^(2k) 1 2^2.
```

It is primitive, has two cyclic one-runs and two cyclic two-runs, and passes
both scalar cycle gates. Nevertheless, neither it nor any cyclic rotation can
satisfy the positive accelerated-Collatz affine divisibility equation.

### Closed-form proof

Put `x=32^k`, `y=27^k`, and `z=18^k`. Direct concatenation gives

```text
D = 32x - 27y,
B = 50x + 27y - 54z,
R = 41x - 27z,
B = 2R (mod D).
```

The odd denominator implies `D|B` exactly when `D|R`. For `k>=5`,

```text
R-D  = 9(x+3y-3z) > 0,
2D-R = x[23-54(27/32)^k+27(18/32)^k] > 0.
```

The second bracket is positive at `k=5` and strictly increases thereafter.
Hence `D<R<2D`, which excludes divisibility. The exact residues for the three
remaining scales are

```text
k=2: 7066
k=3: 151754
k=4: 1746214.
```

If a left rotation moves the first valuation `v` to the end and has numerator
`B'`, direct reindexing gives

```text
2^v B' = 3B + D.
```

Because `gcd(6,D)=1`, `D|B` if and only if `D|B'`. Iterating this identity
proves rotation invariance, so the entire rotation class is excluded. The
generator also replays every rotation through `k=128` as a regression check.

### Boundary

This closes one explicit infinite family, not all words with two run pairs.
It says nothing about general run counts or divergent trajectories. Recent
work relating Collatz parity words to balanced and Christoffel words provides
useful context but is not used as an input to this proof:
[Fernández--Ibáñez, 2026](https://arxiv.org/abs/2607.24844).

## 3. Strong Goldbach conjecture

### Exact prime projection

Define

```text
P(n) = mu(n)^2 Lambda(n).
```

The von Mangoldt function is supported on prime powers. The squarefree factor
is one at `p` and zero at `p^k` for `k>=2`. Consequently,

```text
P(n) = log p  if n=p is prime,
P(n) = 0      otherwise.
```

Therefore

```text
G(N) = sum_(a+b=N) P(a)P(b)
```

is positive exactly when `N` has a Goldbach representation. The previous
`Q*Q` collision support, including `2p^2`, contributes exactly zero after this
projection.

### Computation and limit

The generator checks the projector through `2^23`, and replays every
proper-prime-power collision-supported even target through `2^20`. It finds no
support mismatch, no proper-power leakage, and no finite Goldbach failure.
These finite facts do not imply eventual positivity.

The exact filter corrects the project's bookkeeping, but the pointwise lower
bound for `G(N)` remains the binary Goldbach problem. Classical exceptional-set
work likewise does not provide an every-`N` lower bound; see
[Montgomery--Vaughan, 1975](https://doi.org/10.4064/aa-27-1-353-370).

## 4. Twin Prime conjecture

Using the same projector, define the dyadic detector

```text
T(X) = sum_(X<=n<2X) P(n)P(n+2).
```

Every summand is nonnegative, proper prime powers contribute zero, and

```text
T(X)>0  iff  [X,2X) contains a twin-prime start.
```

This constructs the prime-power-free localized detector requested by
TICKET-198. Thirteen dyadic blocks through `2^23` reproduce its support exactly.
The missing statement is positivity on infinitely many blocks, which is still
the parity-breaking core of the Twin Prime conjecture. Bounded-gap results such
as [Maynard, 2013](https://arxiv.org/abs/1311.4600) do not supply fixed gap two;
the Type-I/II requirements emphasized by
[Ford--Maynard, 2024](https://arxiv.org/abs/2407.14368) remain relevant.

## 5. Proof DAG and reproduction

Each track has the audited form

```text
TICKET-198 open target
        |
        v
TICKET-199 exact theorem ---- rejected/corrected route
        |
        v
single next lemma (highest_risk_open)
        |
        v
parent conjecture (open_not_proven)
```

Reproduce with:

```powershell
D:\python\anaconda3\python.exe scripts\ticket199_symmetric_sampling_two_run_squarefree_filter.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket199_symmetric_sampling_two_run_squarefree_filter -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
node scripts\verify_pages.cjs
```

Expected boundary:

```text
exact theorems: 4
conjectures resolved: 0
machine failures: 0
```
