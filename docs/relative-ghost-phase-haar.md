# TICKET-171: relative KKT geometry, a Collatz ghost ray, signed Goldbach phase, and Haar Type II

## Abstract

TICKET-171 audits the four open lemmas left by TICKET-170 before extending
their computations. It proves four exact target-correction results. None is a
proof or counterexample for the Riemann Hypothesis, the Collatz conjecture,
the strong Goldbach conjecture, or the Twin Prime conjecture.

The Riemann track replaces one global absolute spectral gap by a
direction-sensitive relative KKT certificate. The Collatz track proves that
the proposed residual-tree well-foundedness lemma is false by constructing an
infinite all-one ray whose projective limit is the 2-adic integer `-1`, not a
positive natural orbit. The Goldbach track constructs nonnegative squared
signals with identical Fourier magnitudes and dyadic shell energies but
different pointwise maxima. The Twin Prime track gives an exact two-dimensional
Haar reparameterization of Type-II dependence and proves that every fixed
maximum resolution misses a next-scale checkerboard.

| Problem | Exact result | Resolution | Discarded route | Single next lemma |
|---|---|---:|---|---|
| Riemann | Relative KKT sign-normalization certificate and anisotropic no-go | `open_not_proven` | Requiring the global minimum gap as a necessary error scale | `CofinalRelativeIntervalKKTSignNormalizationBelowOneOnFixedPoleNeutralWeilCore` |
| Collatz | Infinite non-descending all-one residual ray with 2-adic limit `-1` | `open_not_proven` | Well-foundedness of the entire residual prefix tree | `NoPositiveNaturalStartSupportsAnInfiniteLeastRealizerNonDescendingResidualRay` |
| Goldbach | Positive phase ambiguity with identical shell energies | `open_not_proven` | Shell magnitude/energy alone as a sharp pointwise certificate | `UniformSignedBinaryGoldbachAutocorrelationDualCertificateBelowAnchorMargin` |
| Twin Prime | Complete Haar-coordinate bridge and finite-depth no-go | `open_not_proven` | Any fixed dyadic depth as complete Type-II control | `UniformGrowingResolutionHaarTypeIIDecayWithPrimeProducingConstants` |

## 1. Riemann Hypothesis

### 1.1 Declared proposition

Let `K` be a real symmetric nonsingular KKT matrix, let

```text
J = sign(K),       T = |K|^(-1/2),       F = T E T.
```

Then

```text
K + E = T^(-1) (J + F) T^(-1).
```

Consequently,

```text
||F||_2 < 1  =>  inertia(K+E) = inertia(K).                 (1)
```

If an interval computation gives entry radii `|E_ij| <= R_ij`, define

```text
R_rel = |T| R |T|^T.
```

The computable condition `||R_rel||_F < 1` is sufficient for (1).

### 1.2 Proof

The spectral calculus identity `K=T^(-1)JT^(-1)` proves the displayed
congruence. Sylvester's law of inertia reduces the problem to `J+F`. Every
eigenvalue of `J` is `+1` or `-1`; Weyl's inequality therefore prevents an
eigenvalue from crossing zero when `||F||_2<1`.

For the interval form, entrywise triangle inequality gives

```text
|(TET)_ab| <= sum_ij |T_ai| R_ij |T_jb| = (|T|R|T|^T)_ab.
```

The Frobenius norm of this nonnegative radius matrix dominates the operator
norm of every admissible `F`.

### 1.3 Exact no-go family

For `n>=2`, take

```text
K_n = diag(1/n, n^2, -1),       E_n = diag(0, n^2/2, 0).
```

The TICKET-170 absolute test uses the global minimum gap `gamma_n=1/n` and
fails by the factor

```text
||E_n||_2 / gamma_n = n^3/2.
```

However,

```text
|| |K_n|^(-1/2) E_n |K_n|^(-1/2) ||_2 = 1/2,
```

so the relative certificate proves unchanged inertia for every `n`. This does
not invalidate the absolute gap test as a sufficient condition. It proves that
requiring that test is unnecessarily strong in anisotropic KKT geometry.

### 1.4 Remaining gap

The diagonal family is a canonical exact model, not an actual Guinand-Weil
matrix. The next lemma must produce a cofinal interval family on one fixed,
dense, pole-neutral Weil core and prove that its transformed radius is below
one. Finite matrix inertia alone cannot exclude off-critical zeros.

## 2. Collatz conjecture

### 2.1 Declared proposition

The TICKET-170 next lemma,

```text
WellFoundednessOfExactNonDescendingChildTreeAfterAnalyticTailClosure,
```

is false. Let `w_m=1^m` be the accelerated valuation word consisting of `m`
ones. Its affine correction, least positive realizer, and endpoint are

```text
C_m = 3^m - 2^m,
n_m = 2^(m+1) - 1,
u_m = (3^m n_m + C_m)/2^m = 2*3^m - 1.       (2)
```

For every `m>=1`, `u_m>n_m`. Appending valuation one maps `w_m` to
`w_(m+1)`, and

```text
n_(m+1) = n_m  (mod 2^(m+1)).                 (3)
```

Thus these nodes form an infinite compatible non-descending residual ray.

### 2.2 Proof and interpretation

The correction formula follows from `C'=3C+2^m`. Substitution gives (2), and
`3^m>2^m` gives strict non-descent. Congruence (3) is immediate from the
closed form for `n_m`.

The cylinder condition is

```text
n = -1 (mod 2^(m+1)).                           (4)
```

These residues converge to `-1` in the 2-adic integers. No positive natural
integer realizes every prefix: if a fixed `n` did, then `n+1` would be
divisible by arbitrarily large powers of two. This is impossible once the
power exceeds `n+1`.

The ray is therefore a genuine infinite path in the symbolic residual tree
but not a divergent natural Collatz orbit. It is a ghost obstruction showing
that symbolic well-foundedness is stronger than the conjecture requires.

### 2.3 Computation and remaining gap

The generator verifies the formulas at lengths `1,2,4,8,16,32,64`, including
exact child compatibility and membership of appended valuation one below the
TICKET-170 analytic tail threshold. For positive starts at most `1,000,000`,
the largest all-one representative is `524,287` and its prefix length is `18`.
That finite row is illustrative only; the divisibility proof supplies the
infinite statement.

The corrected next lemma is not residual-tree well-foundedness. It is the
natural-compatibility statement:

```text
NoPositiveNaturalStartSupportsAnInfiniteLeastRealizerNonDescendingResidualRay.
```

This remains open and is close to the true first-descent endgame. The ghost
ray neither proves nor disproves Collatz.

## 3. Strong Goldbach conjecture

### 3.1 Declared proposition

Autocorrelation magnitudes and all dyadic shell energies do not determine the
pointwise norm, even within nonnegative squared signals. On `Z/4`, for
`0<epsilon<=1/2`, define

```text
g_+(t) = 1 + epsilon cos(t) + epsilon cos(2t),
g_-(t) = 1 + epsilon cos(t) - epsilon cos(2t).
```

Their sampled vectors are

```text
g_+ = (1+2e, 1-e, 1, 1-e),
g_- = (1, 1+e, 1-2e, 1+e),                     (5)
```

and their normalized DFTs are

```text
G_+ = (1, e/2,  e, e/2),
G_- = (1, e/2, -e, e/2).                       (6)
```

### 3.2 Proof and no-go scope

Equation (5) proves nonnegativity. Equation (6) proves equality of every
Fourier magnitude and therefore every dyadic shell energy. Nevertheless,

```text
max g_+ = 1+2e,       max g_- = 1+e.            (7)
```

At `e=1/4`, the exact maxima are `3/2` and `5/4`. The five machine rows use
`e=1/16,1/8,1/4,3/8,1/2` and verify every identity with rational arithmetic.

This result does not invalidate the TICKET-170 shellwise Cauchy upper bound.
That bound is safe precisely because it takes the worst phase. The no-go says
that shell energy alone cannot supply a sharp pointwise decision or exploit
helpful cancellation. The constructed signals are not prime exponential sums
and are not Goldbach counterexamples.

### 3.3 Remaining gap

The proof target must retain signed arithmetic phase. The next lemma asks for
a target-uniform signed autocorrelation dual certificate below an independently
proved major-arc anchor margin. A finite subunit shell plot or an unsigned
Besov budget cannot replace that theorem.

## 4. Twin Prime conjecture

### 4.1 Declared proposition

Let `A` be a centered square Type-II incidence matrix and `Q` an orthogonal
Haar transform. Set `B=Q A Q^T`. Then

```text
||B||_2 = ||A||_2,
||B||_F^2 = sum_(u,v) |B_uv|^2 = ||A||_F^2.     (8)
```

If all row and column sums of `A` vanish, the constant row and column of `B`
vanish. The complete nonconstant Haar matrix is therefore an exact multiscale
coordinate system for the same Type-II operator.

### 4.2 Proof and finite-depth no-go

Equation (8) follows from left and right orthogonal invariance. Zero margins
mean orthogonality to the constant Haar vector.

Fix any maximum controlled dyadic depth `J`. Inside one cell at depth `J+1`,
place

```text
[[ a, -a],
 [-a,  a]].                                      (9)
```

Every fine row and column sum vanishes. Every dyadic block aggregate through
level `J` also vanishes because each controlled block contains either all of
(9) or none of it. The next-scale Haar coefficient and top singular value are
both `2a`. Therefore no fixed finite resolution is complete.

### 4.3 Computation and remaining gap

The four TICKET-161 matrices at `X=10^4,10^5,10^6,10^7` were transformed by
the orthonormal `4x4` Haar basis. The script verifies the zero constant row and
column, Frobenius-energy equality, and operator-norm invariance. The fraction
of energy in the fine-by-fine block is respectively about
`0.72,0.49,0.08,0.18`. These non-monotone finite values are diagnostics, not
an asymptotic law.

Haar coordinates identify exactly where an estimate must act, but they do not
prove decay. The next lemma requires growing resolution, uniform operator
control, and constants strong enough for a prime-producing sieve. A Frobenius
estimate may lose a dimension factor and must not be silently substituted.

## 5. Proof DAG and claim boundary

```text
Riemann:
  global absolute minimum gap is necessary [REFUTED]
    -> relative sign-normalized KKT certificate [PROVED]
    -> actual cofinal relative interval bound on a fixed Weil core [OPEN]

Collatz:
  residual child tree is well founded [REFUTED]
    -> all-one non-descending 2-adic ghost ray [PROVED]
    -> exclude positive-natural compatible infinite residual rays [OPEN]

Goldbach:
  shell energies determine pointwise deficit [REFUTED]
    -> positive signed-phase ambiguity family [PROVED]
    -> uniform signed arithmetic dual certificate below anchor [OPEN]

Twin Prime:
  fixed dyadic depth controls all Type II dependence [REFUTED]
    -> exact Haar bridge plus next-scale checkerboard [PROVED]
    -> growing-resolution decay with sieve constants [OPEN]
```

Every terminal node remains `open_not_proven`. A finite computation can
falsify a universal shortcut or verify an exact formula, but it cannot prove
one of the four infinite conjectures.

## 6. Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket171_relative_ghost_phase_haar.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket171_relative_ghost_phase_haar -v
```

Outputs:

```text
data/open-problem/ticket171-relative-ghost-phase-haar.json
data/open-problem/riemann/rh-ticket-171-relative-kkt.json
data/open-problem/collatz/co-ticket-171-ghost-ray.json
data/open-problem/goldbach/gb-ticket-171-shell-phase.json
data/open-problem/twin-prime/tp-ticket-171-haar-resolution.json
```

## 7. Literature boundary

- [A finite Guinand-Weil dictionary and archimedean tail order](https://arxiv.org/abs/2607.02828) supplies the finite Weil and interval-certification context, not an RH proof.
- [Paradoxical behavior in Collatz sequences](https://arxiv.org/abs/2502.00948) supplies current finite parity-word context, not residual-ray exclusion.
- [The exceptional set of the Goldbach problem](https://arxiv.org/abs/2607.27282) supplies current exceptional-set and explicit major-arc context, not the signed certificate above.
- [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368) explains why substantial Type-II information matters in a broad sieve setting; the Haar coordinate identity does not provide that estimate.

These references define external context only. No priority or novelty claim is
made for the elementary matrix, Fourier, 2-adic, or Haar identities used here.
