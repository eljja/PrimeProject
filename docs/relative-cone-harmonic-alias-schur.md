# TICKET-176: relative cones, harmonic Collatz corrections, parity aliases, and weighted Schur circularity

## Claim boundary

TICKET-176 continues the four open nodes from TICKET-175. It proves four exact
structural statements and tests their finite consequences. It proves or
disproves none of the Riemann Hypothesis, the Collatz conjecture, strong
Goldbach, or the Twin Prime conjecture. Every conjecture remains
`open_not_proven`; the machine resolution count is zero.

| Problem | Exact new result | Rejected route | Next single lemma |
|---|---|---|---|
| Riemann | relative Loewner PSD-cone certificate | diagonal or absolute tail data stand in for a full form bound | `PoleNeutralWeilTailHasUniformCoreRelativeLoewnerBoundBelowTruncatedMargin` |
| Collatz | aperiodic non-descent correction is bounded by an explicit `O(log h)` envelope | fixed descent horizon or harmonic crossing as an iff test | `AperiodicNonDescendingValuationDiscrepancyExceedsDistinctStateHarmonicEnvelope` |
| Goldbach | exact parity-alias quotient on every even target | taking absolute values before merging equal even-target phases | `ParityAliasedFixedFareyMinorPolynomialHasUniformDeficitPowerSavingBelowMajorMain` |
| Twin Prime | optimized weighted Schur equals the block spectral norm | unrestricted fitted Schur weights as a simpler theorem | `PrimePairHaarBlocksAdmitExplicitArithmeticWeightsWithPowerSavingSchurSums` |

## 1. Riemann: preserve the PSD cone in a relative metric

### Declared proposition

Let `G` be positive definite and let `A_T,A` be Hermitian. If, in Loewner
order,

```text
A_T >= delta G,
-epsilon G <= A-A_T <= epsilon G,
```

then

```text
A >= (delta-epsilon)G.
```

Hence `delta>=epsilon` certifies positive semidefiniteness even when the
smallest Euclidean eigenvalue is too small for an absolute operator-norm
certificate.

### Proof and no-go

For every vector `x`, add

```text
x* A_T x >= delta x*Gx
x*(A-A_T)x >= -epsilon x*Gx.
```

This proves the result directly. Unlike TICKET-171's inertia theorem, this
statement includes the closed semidefinite boundary and uses a positive metric
instead of an invertible signed KKT core.

Diagonal tail data do not imply the premise. Add either the zero tail or
`[[0,1.25],[1.25,0]]` to the identity. Both tails have diagonal `(0,0)`, but
the resulting smallest eigenvalues are `1` and `-0.25`. A proof must therefore
control the complete quadratic form, not only diagonal entries.

### Reproducible scale audit

The metric `G=diag(10^-d,1)`, truncated core `A_T=0.25G`, and adverse tail
`E=-0.20G` give the following comparison.

| `d` | absolute Weyl lower bound | relative margin | exact smallest eigenvalue |
|---:|---:|---:|---:|
| 4 | about `-0.20` | `0.05` | `5e-6` |
| 16 | about `-0.20` | `0.05` | `5e-18` |
| 64 | about `-0.20` | `0.05` | `5e-66` |
| 128 | about `-0.20` | `0.05` | `5e-130` |

This is an exact model theorem, not a relative estimate for the arithmetic
Weil tail. The open lemma must prove both a positive truncated relative margin
and a smaller full tail bound on one fixed pole-neutral core.

## 2. Collatz: replace an orbit-dependent linear budget by a logarithmic one

### Declared proposition

For the accelerated odd orbit `n_i=T^i(n)`, let

```text
S_h = sum_(i<h) v2(3n_i+1),
C_h = sum_(i<h) log2(1+1/(3n_i)).
```

Assume the orbit is aperiodic and `n_i>=n` for `0<=i<h`. The states are then
distinct odd integers, so

```text
C_h <= 1/(3 ln 2) sum_(j<h) 1/(n+2j)
    <= H(n,h),

H(n,h) = 1/(3 ln 2) [1/n + 1/2 ln(1+2(h-1)/n)].
```

The exact affine identity is

```text
log2(n_h/n) = h log2(3) - S_h + C_h.
```

Consequently, every aperiodic orbit that never descends below its start must
satisfy

```text
S_h - h log2(3) <= H(n,h) = O(log h)
```

at every prefix.

### Proof and two corrected routes

Aperiodicity makes the states distinct. Sorting the first `h` states therefore
places the `j`th one at least at `n+2j`. Apply
`log2(1+x)<=x/ln 2`, then bound the decreasing harmonic sum by its first term
plus an integral. The affine identity proves the final necessary condition.

The envelope is sufficient, not equivalent, for descent. Start `63` reaches
`61<63` at step `34`; its centered valuation excess is about `0.1113`, while
`H(63,34)` is about `0.1800`. It descends without crossing the stronger bound.

There is also no universal fixed descent horizon. For `n=2^m-1`, the first
`m-1` accelerated steps all have valuation one and

```text
T^i(n) = 3^i 2^(m-i) - 1,
```

so every one of those steps increases. This is an exact unbounded-delay family,
not a divergent orbit.

### Finite audit

All `49,999` odd starts from `3` through `100,000` descend in the finite audit.
Exactly one, `63`, fails to cross the sufficient harmonic envelope before its
first descent. The result verifies the identities and the distinction between
sufficiency and equivalence; it is not an all-integer proof.

## 3. Goldbach: quotient by parity before taking absolute values

### Declared proposition

Let `L` be even and let `c_k` be the Fourier coefficients retained in a fixed
minor set. For an even target `n=2m`, frequencies `k` and `k+L/2` have the same
phase. Define

```text
d_r = c_r 1_minor(r) + c_(r+L/2) 1_minor(r+L/2).
```

Then the minor contribution has the exact quotient representation

```text
E_minor(2m) = sum_(r<L/2) d_r exp(2 pi i r m/(L/2)).
```

The aliased absolute envelope is never larger than the separate-bin envelope.
This merge is predeclared by target parity and loses no information relevant to
strong Goldbach.

### Proof and no-go

The phase ratio is `exp(2 pi i m)=1`; addition before taking absolute values is
therefore exact. Triangle inequality proves the envelope comparison.

The conjugate-symmetric coefficients

```text
c_1=1, c_7=-1, c_9=-1, c_15=1  (L=16)
```

vanish on every even target after aliasing, although their separate spectral
`l1` mass is `4`. Thus pre-alias absolute values can count a complete null
direction. This ambient real-sequence countermodel is not a prime sequence.

### Fixed-Farey diagnostic

For the predeclared `Q=16`, two-bin Farey mask:

| prime support | even targets | separate-bin certificates | parity-aliased certificates |
|---:|---:|---:|---:|
| 64 | 31 | 31 | 31 |
| 128 | 63 | 56 | 56 |
| 256 | 127 | 82 | 86 |
| 512 | 255 | 89 | 93 |
| 1,024 | 511 | 109 | 111 |

All `987` Fourier and alias identities pass. The quotient raises this finite
certificate count from `367` to `377`, but it does not prove a uniform
one-sided bound. The missing theorem is an arithmetic `L-infinity` deficit
estimate for the aliased polynomial below an independently proved major term.

## 4. Twin Prime: optimized Schur weights are spectrally circular

### Declared proposition

For a nonnegative block-norm matrix `B` and positive vectors `u,v`, put

```text
R = max_i (Bv)_i/u_i,
C = max_j (B^T u)_j/v_j.
```

Then

```text
||B||_2 <= sqrt(RC).
```

If `B` is strictly positive, the infimum over all positive `u,v` equals
`||B||_2`. Positive top singular vectors attain `R=C=||B||_2`.

### Proof and no-go

Weighted Cauchy-Schwarz gives

```text
(Bx)_i^2 <= (Bv)_i sum_j B_ij x_j^2/v_j.
```

Sum in `i`, apply `(Bv)_i<=Ru_i` and `(B^T u)_j<=Cv_j`, and obtain the norm
bound. Perron-Frobenius supplies positive top singular vectors for a strictly
positive matrix, which give equality.

Therefore numerically optimizing unrestricted weights does not simplify the
TICKET-175 block operator target; it solves the same spectral problem. A useful
theorem must prescribe weights from arithmetic scale geometry before seeing the
unknown singular vectors.

| `X` | block operator norm | optimized weighted Schur | unweighted Schur | unweighted ratio |
|---:|---:|---:|---:|---:|
| 10,000 | 128.95 | 128.95 | 155.94 | 1.21 |
| 100,000 | 4,797.48 | 4,797.48 | 5,263.68 | 1.10 |
| 1,000,000 | 100,752.42 | 100,752.42 | 118,015.62 | 1.17 |
| 10,000,000 | 4,516,032.93 | 4,516,032.93 | 5,074,494.72 | 1.12 |

These are finite rough-semiprime Type-II block matrices, not prime-pair
asymptotics. The next lemma must provide explicit arithmetic weights and prove
both directional sums save a power uniformly.

## Proof DAG and status

Each track records exactly three nodes:

```text
REJECTED/INSUFFICIENT -> PROVED EXACT REDUCTION -> OPEN NEXT LEMMA
```

The closed node is not the conjecture. The final node remains
`open_not_proven` in every track.

## Literature boundary

- Recent [truncated Weil-form numerical work](https://arxiv.org/abs/2605.20224), [explicit tail work](https://arxiv.org/abs/2607.02828), and [operator experiments](https://arxiv.org/abs/2607.24830) do not supply the relative continuum theorem isolated here.
- [Tao's almost-all Collatz theorem](https://arxiv.org/abs/1909.03562) does not imply an every-orbit harmonic-envelope crossing.
- Recent [Goldbach exceptional-set work](https://arxiv.org/abs/2607.27282) does not provide the uniform binary aliased-minor estimate.
- [Ford and Maynard on prime-producing sieves](https://arxiv.org/abs/2407.14368) reinforces that genuine Type-II information remains necessary.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket176_relative_cone_harmonic_alias_schur.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket176_relative_cone_harmonic_alias_schur -v
```

The canonical machine-readable artifact is
`data/open-problem/ticket176-relative-cone-harmonic-alias-schur.json`.
