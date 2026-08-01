# TICKET-172: structured KKT inertia, Collatz bridge equivalence, Fourier L1 positivity, and dyadic mixed variation

## Abstract

TICKET-172 audits the four open targets left by TICKET-171 before treating them
as proof bridges. It proves four exact intermediate theorems and resolves none
of the Riemann, Collatz, strong Goldbach, or Twin Prime conjectures.

The main correction is structural. A saddle-point KKT matrix can be certified
from its primal and constraint blocks without requiring a small perturbation of
the entire indefinite matrix. The proposed Collatz natural-ray exclusion is
proved equivalent to the original first-descent conjecture and therefore cannot
be advertised as an easier bridge. Fourier inversion gives an exact Goldbach
positivity gate, but a positive four-point family proves that magnitude-only
data cannot improve it. Finally, fine/fine Haar energy is identified exactly
with dyadic mixed differences, converting the Twin Type-II target into a
specific arithmetic variation estimate.

| Problem | Exact TICKET-172 result | Status | Rejected route | Next single lemma |
|---|---|---|---|---|
| Riemann | Structured KKT block-inertia certificate | `open_not_proven` | Whole relative KKT norm below one as a necessary condition | `CofinalWeilPrimalBlockPositivityAndConstraintRankCertificate` |
| Collatz | Natural-supported residual-ray equivalence | `open_not_proven` | Treating natural-ray exclusion as weaker than Collatz | `LeastCounterexampleCrossScaleCylinderHeightBound` |
| Goldbach | Fourier L1 anchor certificate and sharpness | `open_not_proven` | Improving the universal pointwise bound from shell magnitudes alone | `UniformPrimeSpecificSignedGoldbachFourierCancellationBelowMainTerm` |
| Twin Prime | Haar/mixed-variation identity and marginal no-go | `open_not_proven` | Replacing mixed Type-II control by row/column margins | `PrimePairMatrixWeightedDyadicMixedVariationPowerSaving` |

## 1. Claim discipline

The following labels are used literally:

- `proved_exact`: the displayed finite-dimensional or algebraic statement is proved.
- `refuted_or_insufficient`: a stated proof route has an explicit countermodel or is equivalent to the original conjecture.
- `open_not_proven`: the conjecture-level infinite bridge is absent.

Finite prime counts and finite Collatz replay are diagnostics. They neither
prove the conjectures nor upgrade an algebraic surrogate into a number-theoretic
theorem.

## 2. Riemann track: structured KKT inertia

### 2.1 Declared proposition

Let

\[
K=\begin{pmatrix}A&B^T\\B&0\end{pmatrix},
\]

where `A` is real symmetric positive definite of size `n` and `B` has full row
rank `r`. Then

\[
\operatorname{inertia}(K)=(n,r,0).
\]

For interval centers `A0,B0`, operator radii `rho_A,rho_B`, the computable
conditions

\[
\lambda_{\min}(A_0)>\rho_A,
\qquad
\sigma_{\min}(B_0)>\rho_B
\]

certify this inertia for every structured matrix in the two balls.

### 2.2 Proof

The exact block congruence gives

\[
K\sim
\operatorname{diag}\left(A,-BA^{-1}B^T\right).
\]

The second block is negative definite because `B` has full row rank. Sylvester's
law of inertia proves the claim. Weyl perturbation bounds preserve positivity of
`A` and full row rank of `B` under the stated margins.

### 2.3 Necessity no-go

Take

\[
K_0=\begin{pmatrix}1&1\\1&0\end{pmatrix},\qquad
E_t=\begin{pmatrix}t&0\\0&0\end{pmatrix}.
\]

For `t >= 2`, the TICKET-171 whole-matrix relative norm is

\[
\left\lVert |K_0|^{-1/2}E_t|K_0|^{-1/2}\right\rVert_2
=\frac{2t}{\sqrt 5}>1.
\]

Nevertheless `det(K0+E_t)=-1`, so the inertia remains `(1,1,0)`. Thus the
relative condition is sufficient, not necessary. This does not certify any
actual Guinand-Weil discretization.

### 2.4 Remaining gap

The project must prove cofinal primal positivity and constraint-rank margins on
one fixed pole-neutral Guinand-Weil form core. A proxy saddle-point matrix is
not a zeta-zero exclusion theorem.

## 3. Collatz track: equivalence before computation

### 3.1 Declared proposition

For the accelerated odd map `T`, the following are equivalent:

1. Every odd `n>1` has some `j` with `T^j(n)<n`.
2. No infinite prefixwise non-descending residual ray has positive-natural support.
3. Every positive integer reaches `1`.

### 3.2 Proof

A positive-natural-supported non-descending ray is precisely the valuation
itinerary of an `n>1` satisfying `T^j(n)>=n` for every `j`. Hence statements 1
and 2 exclude the same witness. Statement 1 implies statement 3 by strong
induction on `n`; statement 3 immediately implies statement 1.

This proves that the TICKET-171 next target was not an intermediate theorem. It
was a reformulation of Collatz.

### 3.3 Finite-prefix decision no-go

For every horizon `H`, let

\[
n_H=2^{H+1}-1.
\]

Its first `H` accelerated valuations are all one and its endpoint is

\[
T^H(n_H)=2\cdot3^H-1>n_H.
\]

The same prefix has two different continuations:

- the all-one 2-adic ghost converging to `-1`;
- the natural orbit of `n_H`, whose next valuation is
  `1+v2(3^(H+1)-1)>1`.

No fixed prefix decides natural support. The finite diagnostic verifies first
descent for all 49,999 odd starts from `3` through `100,000`, but this remains a
finite check.

### 3.4 Remaining gap

The retained target is an Archimedean cross-scale height bound for a hypothetical
least counterexample. Such a bound must be independent of prefix horizon and
must overlap a separately certified finite verification range.

## 4. Goldbach track: exact Fourier positivity gate

### 4.1 Declared proposition

For a real function `g` on `Z/q` with normalized Fourier coefficients,

\[
g(x)=\sum_k \widehat g(k)e(kx/q),
\]

Fourier inversion gives

\[
g(x)\geq \widehat g(0)-\sum_{k\ne0}|\widehat g(k)|.
\]

Therefore

\[
\sum_{k\ne0}|\widehat g(k)|<\widehat g(0)
\]

is a rigorous pointwise positivity certificate.

### 4.2 Sharpness no-go

On `Z/4`, use the TICKET-171 pair

\[
\widehat g_+=(1,\varepsilon/2,\varepsilon,\varepsilon/2),\qquad
\widehat g_-=(1,\varepsilon/2,-\varepsilon,\varepsilon/2).
\]

The magnitude profiles are identical. The nonzero L1 budget is `2 epsilon`, and

\[
\min g_-=1-2\varepsilon
\]

attains the triangle lower bound for every `0<epsilon<=1/2`. Consequently no
universally valid certificate using only these magnitudes can improve the bound.
The family is nonnegative but is not a prime-supported Goldbach counterexample.

### 4.3 Prime diagnostic and remaining gap

For 64, 128, 256, and 512 consecutive even targets, all ordered prime-pair
counts are positive. The generic Fourier L1 lower bounds are nevertheless
nonpositive. The missing theorem must exploit target-dependent signed arithmetic
cancellation, not merely a finer magnitude shell partition.

## 5. Twin Prime track: mixed variation is the missing coordinate

### 5.1 Declared proposition

For an even-sided matrix `A`, the finest fine/fine coefficient of a `2x2` block
under the separable orthonormal Haar transform is

\[
d=\frac{a_{00}-a_{01}-a_{10}+a_{11}}{2}.
\]

Thus

\[
\sum d^2=\frac14\sum
(a_{00}-a_{01}-a_{10}+a_{11})^2.
\]

Applying the same identity recursively to normalized coarse blocks gives an
exact multiscale mixed-variation representation.

### 5.2 Finite bridge and no-go

The identity reproduces the TICKET-171 fine/fine energies of all four TICKET-161
centered Type-II matrices (`X=10^4,10^5,10^6,10^7`).

For the alternating `N x N` checkerboard of amplitude `a`, every row and column
sum is zero, but every local mixed difference is `4a`. Hence

\[
E_{ff}=N^2a^2=\lVert A\rVert_F^2.
\]

One-dimensional marginal cancellation therefore gives no fine/fine decay.

### 5.3 Remaining gap

The exact next target is a prime-pair-specific weighted dyadic mixed-variation
power saving, uniform through a sieve-compatible growing resolution. The Haar
identity names the required estimate; it does not prove it.

## 6. Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket172_structure_equivalence_l1_variation.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket172_structure_equivalence_l1_variation -v
```

Primary machine-readable artifact:
`data/open-problem/ticket172-structure-equivalence-l1-variation.json`.

## 7. Literature boundary

- Connes and Consani, *The Scaling Hamiltonian*, [arXiv:1910.14368](https://arxiv.org/abs/1910.14368): Weil positivity and operator-theoretic context.
- Ernvall-Hytonen et al., *A finite Guinand-Weil dictionary and archimedean tail order*, [arXiv:2607.02828](https://arxiv.org/abs/2607.02828): current finite Guinand-Weil context.
- Tao, *Almost all orbits of the Collatz map attain almost bounded values*, [arXiv:1909.03562](https://arxiv.org/abs/1909.03562): almost-all first-passage context.
- Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*, [arXiv:2605.13886](https://arxiv.org/abs/2605.13886): sharp finite parity-vector context without a Collatz claim.
- Grimmelt and Bhowmik, *The exceptional set of the Goldbach problem*, [arXiv:2607.27282](https://arxiv.org/abs/2607.27282): exceptional-set and explicit major-arc context.
- Ford and Maynard, *On the theory of prime producing sieves*, [arXiv:2407.14368](https://arxiv.org/abs/2407.14368): prime-producing sieve and Type-II context.

These references supply context. PrimeProject makes no priority or novelty claim
for standard Schur complements, Fourier inversion, strong induction, or Haar
identities.
