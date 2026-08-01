# TICKET-179: signed symbols, adaptive valuation layers, discrete targets, and centered energy

## Claim boundary

**All four conjectures remain open.** TICKET-179 proves four exact representation
theorems or no-go results. It does not prove the Riemann Hypothesis, the Collatz
conjecture, strong Goldbach, or the Twin Prime conjecture, and it finds no
counterexample to any of them.

| Problem | Exact result proved here | Status | Route rejected | Remaining arithmetic gap | Next single lemma |
|---|---|---|---|---|---|
| Riemann | `BoundedToeplitzSymbolCertificateAndAbsoluteSummabilityNoGo` | open | absolute summability is necessary for uniform Toeplitz control | no bounded symbol is known for the actual whitened Weil tail below the core margin | `PoleNeutralWeilWhitenedTailHasBoundedRealFourierSymbolBelowCoreMargin` |
| Collatz | `AdaptiveValuationLayerCompletenessAndFixedDepthIncompleteness` | open | a fixed low-bit depth completely detects every first descent | no every-orbit adaptive surplus theorem or nontrivial-cycle exclusion | `EveryAperiodicNonDescendingOrbitAccumulatesAdaptiveValuationLayerSurplusBeyondExactCorrection` |
| Goldbach | `DiscreteTargetPositivityCertificateAndContinuousInterpolationNoGo` | open | continuous-circle positivity is necessary for discrete even targets | no target-uniform aliased-minor deficit below the major main term | `ParityAliasedMinorHasUniformDiscreteEvenTargetDeficitBelowMajorMain` |
| Twin Prime | `CrossGramCenteringIdentityAndPairwiseIncoherenceNoGo` | open | small pairwise coherence forces all-plus cancellation | no centered-energy saturation theorem for actual prime-pair Haar blocks | `PrimePairHaarCenteredEnergySaturatesDiagonalAtPowerSavingRate` |

The status field `open_not_proven` is part of every machine-readable attempt.
The resolution counter is zero.

## 1. Riemann: bounded signed symbols instead of absolute tails

### Declared proposition

Let `f` be a real function in `L-infinity(T)` and let

```text
a_r = (1 / 2 pi) integral f(theta) exp(-i r theta) d theta.
```

For every `N`, form the Hermitian Toeplitz section

```text
T_N = (a_(i-j))_(0 <= i,j < N).
```

Then

```text
||T_N||_op <= ||f||_infinity.
```

Thus a whitened positive core with margin `delta` remains positive whenever
the signed tail is represented by such an `f` with
`||f||_infinity < delta`. Absolute summability of `(a_r)` is not necessary.

### Proof

For `x in C^N`, put `p_x(z)=sum_j x_j z^j`. Fourier orthogonality gives

```text
x* T_N x
  = (1 / 2 pi) integral f(theta) |p_x(exp(i theta))|^2 d theta.
```

The absolute value is at most
`||f||_infinity ||x||_2^2`, proving the operator bound.

Take the bounded square-wave symbol

```text
f(theta) = C sign(cos theta).
```

Its nonzero Fourier coefficients are

```text
a_(plus/minus(2k+1)) = 2 C (-1)^k / [pi(2k+1)].
```

Their absolute sum diverges harmonically, while every finite Toeplitz section
has operator norm at most `C`. This is an infinite counterfamily to the claim
that the absolute summability condition isolated in TICKET-178 is necessary.

### Reproducible audit

The audit uses `C=0.2`, `delta=0.25`, and dimensions
`16, 32, 64, 128, 256, 512`. The bounded-symbol certificate passes at every
dimension. The absolute row-sum bound grows and crosses the core margin. The
all-ones Rayleigh quotient is a Fejer mean of the bounded symbol and remains
inside `[-C,C]`.

### Limit

The square wave is a functional-analysis counterexample, not the Weil tail.
The missing arithmetic step is to identify the pole-neutral whitened Weil tail
as Fourier coefficients of a real bounded symbol and prove that its essential
supremum lies below the finite-core margin. Recent truncated-Weil computations
provide exact finite dictionaries and explicit archimedean tail budgets, but
explicitly stop short of RH or this infinite symbol estimate
([Groskin 2026](https://arxiv.org/abs/2607.02828),
[Kim et al. 2026](https://arxiv.org/abs/2607.24830)).

## 2. Collatz: adaptive layers are exact; fixed depth is incomplete

### Declared proposition

For the accelerated odd map, write

```text
3 n_i + 1 = 2^(v_i) n_(i+1)
```

and define the layer occupancy

```text
A_k(h) = #{0 <= i < h : v_i >= k}.
```

Then

```text
sum_(i<h) v_i = sum_(k>=1) A_k(h)
```

and a completed prefix descends exactly when

```text
sum_(k>=1) A_k(h)
  > h log2(3) + sum_(i<h) log2(1 + 1/(3 n_i)).
```

For every fixed depth `K`, there exists an infinite natural-number cylinder
whose first descent is recognized by the adaptive sum but not by the truncated
sum `sum_(k<=K) A_k(h)`.

### Proof

The layer identity counts each `v_i` once at every level `k<=v_i`. Multiplying
the exact orbit equations yields

```text
n_h / n_0
  = 3^h 2^(-sum v_i) product_(i<h)(1 + 1/(3 n_i)),
```

which proves the descent equivalence.

Fix `K` and choose `h` so that

```text
h - 1 + K <= h log2(3).
```

Choose `M` with `h-1+M > h log2(3)` and use the valuation word

```text
(1, 1, ..., 1, M).
```

Every positive finite valuation word defines one odd residue class modulo
`2^(sum v_i+1)`. Adding multiples of that modulus preserves the word. The first
`h-1` valuation-one steps strictly increase. Since
`2^(h-1+M)>3^h`, sufficiently large representatives descend at the terminal
step. The exact adaptive sum crosses the boundary, while the `K`-truncated sum
cannot even exceed `h log2(3)`.

### Reproducible audit

The generated cylinders test `K=2,4,8,16`. All four have an increasing prefix,
a terminal first descent, exact layer-cake equality, and failure of the fixed
depth certificate. The largest tested example starts at `3,760,646,520,831`
with valuation word consisting of 26 ones followed by 17.

### Limit

Adaptive layers are complete only after a finite prefix is available. The
result does not force an unknown orbit to create the required high layer and
does not exclude a nontrivial cycle. Recent one-bit and parity-vector work also
isolates orbit-level balance rather than proving it for every orbit
([Chang 2026](https://arxiv.org/abs/2603.25753),
[Niu 2026](https://arxiv.org/abs/2605.13886)).

## 3. Goldbach: certify the target grid, not an arbitrary interpolant

### Declared proposition

On a cyclic grid `G_M={j/M}`, characters whose frequencies agree modulo `M`
have identical values. Coefficient aliasing modulo `M`, followed by inverse DFT
evaluation, is therefore an exact positivity certificate on the target grid.
Continuous positivity of a chosen trigonometric interpolant is sufficient but
not necessary.

### Proof and no-go family

For even `M`, define

```text
F_M(x) = A_M + cos(2 pi x + pi/M),
A_M    = [1 + cos(pi/M)] / 2.
```

Its grid and continuous minima are

```text
min_(x in G_M) F_M(x) =  [1 - cos(pi/M)] / 2 > 0,
min_(x in T)   F_M(x) = -[1 - cos(pi/M)] / 2 < 0.
```

Thus every grid target is positive while the continuous interpolant is
negative between targets. A failed continuous Sobolev certificate cannot be a
Goldbach counterexample.

### Reproducible audit

The interpolation counterfamily is checked at grid sizes `8,16,32,64`.
Independent exact prime convolutions verify every even integer through `1024`
has a representation, grouped into five declared finite limits. These counts
are finite evidence only.

### Limit

The missing estimate remains binary and target-uniform: after exact parity and
cyclic aliasing, the minor contribution must stay below a proved major term at
every sufficiently large even integer. Exceptional-set estimates do not remove
every possible exceptional target; this distinction remains explicit in recent
work on the Goldbach exceptional set
([Goldbach exceptional set, 2026](https://arxiv.org/abs/2607.27282)).

## 4. Twin Prime: zero-mode saving is centered-energy saturation

### Declared proposition

For Hilbert-space components `T_1,...,T_m`, define

```text
D = sum_j ||T_j||^2,
Z = ||sum_j T_j||^2,
bar(T) = (1/m) sum_j T_j,
V = sum_j ||T_j - bar(T)||^2.
```

Then

```text
V = D - Z/m.
```

Consequently

```text
Z <= eta D  iff  V >= (1 - eta/m)D.
```

Pairwise incoherence alone cannot imply this power saving.

### Proof and no-go families

Expanding the centered squares gives
`V=D-m||bar(T)||^2=D-Z/m`. An orthonormal family has pairwise coherence zero,
but `Z=D`, so it has no saving with `eta<1`. Conversely, scalar roots of unity
have pairwise coherence one but `Z=0`. The required object is collective signed
centering, not generic pairwise decorrelation.

### Reproducible audit

Aligned, roots-of-unity, and orthonormal families are evaluated for
`m=4,8,16,32`. The centering identity holds within `1e-12`; every orthonormal
family has zero coherence and zero-mode ratio one, while every roots-of-unity
family cancels its zero mode below `1e-25`.

### Limit

No computation here uses actual prime-pair Haar blocks. A Twin Prime proof
would still require a prime-producing main term and arithmetic Type-II control
strong enough to force centered-energy saturation with a power-saving defect.
Existing prime-producing sieve research does not remove this arithmetic parity
barrier ([Matomaki and Merikoski 2024](https://arxiv.org/abs/2407.14368)).

## Cross-problem conclusion

TICKET-179 identifies a common failure mode: the wrong representation can make
a sufficient condition look like the conjecture itself. Absolute coefficients,
fixed bit depth, continuous interpolation, and pairwise coherence respectively
erase phase, rare high valuations, the discrete target set, and collective
signed cancellation.

The replacements proved exact here are bounded signed symbols, adaptive layer
sums, cyclic target evaluation, and centered-energy saturation. None of the
four corresponding arithmetic uniformity lemmas is proved.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket179_symbol_adaptive_discrete_centering.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket179_symbol_adaptive_discrete_centering -v
```

Primary machine-readable artifact:

```text
data/open-problem/ticket179-symbol-adaptive-discrete-centering.json
```
