# TICKET-173: finite-section defects, Collatz cylinder stabilization, target-aligned Goldbach phase, and tensor-Haar scale pairs

## Abstract

TICKET-173 continues the four open nodes left by TICKET-172. It proves four
exact structural theorems, rejects four over-strong or incomplete routes, and
resolves none of the Riemann, Collatz, strong Goldbach, or Twin Prime
conjectures.

The Riemann track proves that asymptotically nonnegative lower bounds on a
nested dense family of finite sections suffice for global nonnegativity; a
positive compact diagonal operator proves that a uniform spectral gap is not
necessary. The Collatz track gives an exact modular formula for every valuation
cylinder and proves that positive-natural support is equivalent to eventual
stabilization of its least representatives. The all-one cylinders show that no
horizon-only subexponential height bound can work. The Goldbach track retains
the target-aligned signs of the squared prime Fourier transform and proves an
exact positivity certificate, then gives a nonnegative weighted countermodel
showing that the certificate is not necessary. The Twin Prime track completes
the scale geometry: zero margins leave all tensor-Haar wavelet pairs, including
unequal row and column scales. A rank-one cross-scale family refutes control of
same-scale mixed variation alone.

| Problem | Exact TICKET-173 result | Status | Rejected route | Next single lemma |
|---|---|---|---|---|
| Riemann | Dense finite-section lower-defect theorem | `open_not_proven` | Uniform positive finite-section gap as necessary | `PoleNeutralWeilFiniteSectionLowerDefectConvergesToZero` |
| Collatz | Natural support iff cylinder representatives stabilize | `open_not_proven` | Horizon-only subexponential cylinder height | `EveryPrefixwiseNonDescendingRayHasUnboundedCylinderRepresentatives` |
| Goldbach | Target-aligned signed-spectrum positivity certificate | `open_not_proven` | Negative budget below anchor as necessary | `UniformMajorArcPositiveMassDominatesMinorArcSignedDeficit` |
| Twin Prime | Complete two-parameter tensor-Haar energy theorem | `open_not_proven` | Same-scale mixed variation as complete Type-II control | `PrimePairMatrixAllScalePairHaarEnergyPowerSaving` |

## 1. Claim discipline

- `proved_exact` means the displayed functional-analytic, modular, Fourier, or
  Haar statement has a complete argument.
- `refuted_or_insufficient` means an explicit family violates the proposed
  implication or proves that the condition is unnecessarily strong.
- `open_not_proven` means the named arithmetic estimate needed for the
  conjecture remains absent.

The finite computations audit formulas and expose failed gates. They are not
extrapolated to infinite ranges.

## 2. Riemann track: vanishing lower defect, not uniform coercivity

### 2.1 Declared proposition

Let `q` be a continuous Hermitian form on a Hilbert space `H`. Let

\[
V_1\subseteq V_2\subseteq\cdots
\]

have dense union, and let `A_N` be the exact matrix of the restriction of `q`
to `V_N` in an orthonormal basis. Suppose a computed matrix `Atilde_N` satisfies

\[
\|A_N-\widetilde A_N\|\leq\rho_N,
\qquad
\lambda_{\min}(\widetilde A_N)-\rho_N\geq-\eta_N,
\qquad
\eta_N\to0.
\]

Then `q(v)>=0` for every `v` in `H`.

If `B:H->R^r` is continuous and one exact restriction `B|V_N` is surjective,
all later restrictions are surjective. An interval condition

\[
\sigma_{\min}(\widetilde B_N)>\|B_N-\widetilde B_N\|
\]

certifies that one-stage rank statement.

### 2.2 Proof

Fix `v` in `V_M`. For every `N>=M`, the lower certificate applies to the same
vector and gives

\[
q(v)\geq-\eta_N\|v\|^2.
\]

Letting `N` tend to infinity gives `q(v)>=0`. Continuity and density extend the
inequality to `H`. For the constraint map, the range on a later nested domain
contains the already-surjective earlier range.

### 2.3 Uniform-gap no-go

On `l2`, define

\[
Qe_j=\frac1j e_j.
\]

Then `<Qv,v>>0` for every nonzero `v`, but the first `N` coordinates have
minimum eigenvalue `1/N`. Thus a uniform positive finite-section gap proves
coercivity, which is strictly stronger than nonnegativity.

The machine audit uses `Atilde_N=A_N-(1/N)I`. Its certified lower bound is
`-1/N`, which converges to zero exactly.

### 2.4 Remaining gap

This is an abstract closure theorem. PrimeProject has not constructed one fixed
dense pole-neutral Guinand-Weil core whose certified lower defects tend to
zero. Doing that would confront the actual Weil criterion; the diagonal model
does not.

## 3. Collatz track: natural support is cross-scale stabilization

### 3.1 Declared proposition

For a finite accelerated-odd valuation word

\[
w=(a_1,\ldots,a_H),\qquad S=\sum_j a_j,
\]

write

\[
2^S T^H(n)=3^Hn+C(w).
\]

Exactly one odd residue modulo `2^(S+1)` realizes the word:

\[
r_w\equiv(2^S-C(w))3^{-H}\pmod{2^{S+1}}.
\]

Along an infinite word, the least positive representatives are compatible
under reduction. The infinite word is the valuation itinerary of one positive
natural integer if and only if these representatives are bounded, equivalently
eventually constant.

### 3.2 Proof

Exact realization requires the endpoint to be odd. Therefore

\[
3^Hn+C(w)\equiv2^S\pmod{2^{S+1}}.
\]

Since `3` is invertible modulo every power of two, the residue is unique.
Reducing the affine identity at every prefix gives divisibility by the required
`2^(S_j)`. The affine constant of the remaining nonempty suffix is odd, so each
prefix quotient is odd and each prescribed valuation is exact. Adding one
valuation therefore refines the previous cylinder and the representatives are
nested. A bounded compatible sequence modulo strictly increasing powers of two
must eventually stop changing. Its stable value realizes every finite prefix.
Conversely, once the modulus exceeds a supporting natural start `n`, the least
representative equals `n` forever.

### 3.3 Height no-go

For the all-one word of length `H`,

\[
r_H=2^{H+1}-1.
\]

Its first `H` iterates are all at least `r_H`. Hence any bound that covers all
non-descending cylinders using only `H` must be at least exponential. The audit
checks all `5,460` words over valuations `{1,2,3,4}` through length six and
checks the exact all-one family through `H=64`.

This family consists of different finite natural starts. It is not one
divergent natural orbit.

### 3.4 Remaining gap

The decisive statement is now explicit: every infinite prefixwise
non-descending ray must have unbounded cylinder representatives. By the
stabilization theorem this would exclude positive-natural support and prove
Collatz. No such every-ray estimate is proved here.

## 4. Goldbach track: target-aligned positive and negative mass

### 4.1 Declared proposition

Let `f>=0` on `Z/q`, use the unnormalized Fourier transform `F`, and define

\[
c_k(n)=\frac1q\Re\left(F(k)^2e(kn/q)\right).
\]

For nonzero frequencies put

\[
P(n)=\sum_{k\ne0}\max(c_k(n),0),\qquad
N(n)=\sum_{k\ne0}\max(-c_k(n),0).
\]

Then

\[
(f*f)(n)=\frac{F(0)^2}{q}+P(n)-N(n).
\]

Thus `F(0)^2/q>N(n)` is a rigorous target-specific positivity certificate.
It is at least as strong as dropping the phase of every nonzero coefficient.

### 4.2 Exact necessity no-go

On `Z/8`, let

\[
f=(0,0,0,0,0,0,1,2).
\]

At target `4`, direct convolution gives `(f*f)(4)=1`. The zero-mode anchor is
`9/8`, while the seven aligned nonzero contributions are

\[
\left(
\frac18+\frac{\sqrt2}4,-\frac38,
\frac18-\frac{\sqrt2}4,\frac18,
\frac18-\frac{\sqrt2}4,-\frac38,
\frac18+\frac{\sqrt2}4
\right).
\]

The negative budget is `(1+sqrt(2))/2`, which exceeds `9/8` because
`4sqrt(2)>5`. The negative-budget gate therefore fails although the
convolution is positive. Positive aligned frequencies are indispensable.

### 4.3 Prime diagnostic

Zero-padded transforms avoid cyclic wraparound for prime supports through
`64,128,256,512,1024`. Across `987` even targets, exact Fourier reconstruction
matches ordered prime-pair counts and every count is positive. The sufficient
negative-budget gate passes only one target. This is bounded evidence that the
gate is too strong, not a Goldbach proof.

### 4.4 Remaining gap

A pointwise binary Goldbach proof needs a uniform lower bound for positive
major-arc mass together with an upper bound for the signed minor-arc deficit.
Exceptional-set estimates do not automatically provide this for every target.

## 5. Twin Prime track: two scale indices are necessary

### 5.1 Declared proposition

Let `H_N` be the complete orthonormal discrete Haar basis and

\[
C=H_NAH_N^T.
\]

If all row and column sums of `A` vanish, every coefficient involving the
constant Haar vector vanishes. Parseval therefore gives

\[
\|A\|_F^2=\sum_{j,k\geq1}E_{j,k},
\]

where the row scale `j` and column scale `k` are independent.

### 5.2 Same-scale no-go

For every dyadic `N>=4`, choose normalized Haar wavelets `u` and `v` at two
different scales and set

\[
A=uv^T.
\]

The matrix has zero row and column sums and operator and Frobenius norm one.
Its Haar transform has one coefficient at the off-diagonal scale pair of `u`
and `v`. Consequently every same-scale energy `E_(j,j)` is zero while the full
Type-II energy is one.

The finite TICKET-161 matrices are also decomposed into the four scale pairs of
the `4x4` Haar basis. This identifies how much finite energy is already
cross-scale, but does not establish asymptotic decay.

### 5.3 Remaining gap

TICKET-172's same-scale mixed differences were exact but incomplete as a full
Type-II certificate. The corrected target must control all row-scale and
column-scale pairs with prime-producing constants and a sieve-compatible power
saving.

## 6. Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket173_finite_section_cylinder_phase_tensor.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket173_finite_section_cylinder_phase_tensor -v
```

Primary artifact:
`data/open-problem/ticket173-finite-section-cylinder-phase-tensor.json`.

## 7. Literature boundary

- Connes and Consani, *The Scaling Hamiltonian*, [arXiv:1910.14368](https://arxiv.org/abs/1910.14368): Weil positivity and pole-neutral test-function context.
- Groskin, *A finite Guinand-Weil dictionary and archimedean tail order for the truncated Weil quadratic form*, [arXiv:2607.02828](https://arxiv.org/abs/2607.02828): finite Galerkin and tail-budget context with no RH claim.
- Tao, *Almost all orbits of the Collatz map attain almost bounded values*, [arXiv:1909.03562](https://arxiv.org/abs/1909.03562): almost-all logarithmic-density result, not an every-orbit theorem.
- Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*, [arXiv:2605.13886](https://arxiv.org/abs/2605.13886): finite parity-vector results with an explicit non-claim boundary.
- Grimmelt and Bhowmik, *The exceptional set of the Goldbach problem*, [arXiv:2607.27282](https://arxiv.org/abs/2607.27282): explicit major-arc and exceptional-set context.
- Ford and Maynard, *On the theory of prime producing sieves*, [arXiv:2407.14368](https://arxiv.org/abs/2407.14368): necessity of substantial Type-I/II information.

The dense-core closure theorem, modular cylinder identity, Fourier inversion,
and tensor-Haar Parseval identity are standard structures. PrimeProject claims
no priority for them. Its contribution in this ticket is the audited
keep/discard decision and the explicit corrected proof obligations.
