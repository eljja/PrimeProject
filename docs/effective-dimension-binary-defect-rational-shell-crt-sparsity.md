# TICKET-232: Effective Dimension, Binary Collatz Defects, Rational Goldbach Shells, and CRT Sparsity

## Claim status

**Open, not proven.** TICKET-232 proves four exact partial or no-go theorems.
It proves or disproves none of the Riemann hypothesis, the Collatz conjecture,
strong Goldbach, or the twin-prime conjecture. The machine-readable resolution
count is `0 / 4`.

The external status was checked on 2026-08-21 against the
[Clay Riemann-hypothesis page](https://www.claymath.org/riemann/),
[Tao's Collatz paper](https://arxiv.org/abs/1909.03562), the recent
[Goldbach exceptional-set survey and major-arc formula](https://arxiv.org/abs/2607.27282),
and [Maynard's small-gap theorem](https://annals.math.princeton.edu/2015/181-1/p07).
Those sources supply context only; no external unproved claim is used as a
premise of the four elementary theorems below.

## Reproducible contract

- Generator: `scripts/ticket232_effective_dimension_binary_defect_rational_shell_crt_sparsity.py`
- Tests: `tests/test_ticket232_effective_dimension_binary_defect_rational_shell_crt_sparsity.py`
- Integrated JSON: `data/open-problem/ticket232-effective-dimension-binary-defect-rational-shell-crt-sparsity.json`
- Exact partial/no-go theorems: `4`
- Discarded continuation routes: `4`
- Parent conjectures resolved: `0`
- Machine failures: `0`

## 1. Riemann track

### Declared proposition

At height `T`, let `q_j(T)>1`, let `w_j(T)>=0` have finite positive total
mass `W_T`, and set

\[
F_T(n)=\sum_j w_j(T)|1-q_j(T)^{-in}|^2.
\]

For every head length `M` and integer `Q>=2` with `Q^M<=T`, some
`1<=n<=T` satisfies

\[
{F_T(n)\over W_T}\le {4\pi^2\over Q^2}+4\delta_T(M),
\qquad
\delta_T(M)={\sum_{j>M}w_j(T)\over W_T}.
\]

Consequently, suppose `F_T(n)>=c W_T` on every integer `1<=n<=T`. If
`delta_T(M)<=c/8` and `Q` is an integer with `4*pi^2/Q^2<c/2`, then

\[
Q^M>T,
\qquad
M>{\log T\over\log Q}.
\]

A fixed positive normalized adaptive floor therefore requires at least
logarithmically many effective coordinates.

### Proof and computation

Apply simultaneous Dirichlet pigeonhole approximation to the first `M`
phases `log(q_j(T))/(2*pi)`. The difference of two multiples in one of the
`Q^M` boxes is an integer `n<=Q^M`; its head energy is at most
`4*pi^2/Q^2` times the head mass. The tail uses `|1-z|^2<=4`. Combining
this witness with a hypothetical `c`-floor gives the strict contradiction.
No multiplicative independence is required.

The generator records five collision witnesses. It also checks the explicit
corollary `c=1/2`, tail ratio `1/16`, `Q=13`, giving
`M>log(T)/log(13)`.

**Discarded route:** height adaptation with sublogarithmic effective
dimension as a repair of the TICKET-231 frame obstruction.

**Finite-computation limit:** the witnesses check the implementation only.
The infinite dimension necessity follows from the pigeonhole argument.

**Remaining gap:** construct a logarithmically dense adaptive frame, prove a
positive floor, and dominate the actual Weil tail. This theorem still concerns
scalar dilation phase energy, not the full Weil quadratic form.

**Next lemma:**
`LogarithmicEffectiveDimensionAdaptiveWeilFrameWithExplicitTailDominance`.

## 2. Collatz track

### Declared proposition

For `a in {1,2}^h`, put

\[
B(a)=\sum_{j=0}^{h-1}3^{h-1-j}2^{a_0+\cdots+a_{j-1}},
\qquad
D(a)=2^{\sum a_j}-3^h.
\]

If `D(a)>0` and `a` contains one, two, or three entries equal to `1`, then

\[
D(a)\nmid B(a).
\]

Hence any nontrivial positive accelerated cycle whose valuation word is
binary must contain at least four `1`s. The all-`2` word is the known trivial
cycle and is not excluded.

For the cyclic rotation `a'=(a_1,...,a_(h-1),a_0)`, one has
`2^(a_0)B(a')=3B(a)+D(a)`. Since `gcd(D,6)=1`, the condition `D|B` is
rotation invariant, which justifies the canonical gap rotations below.

### Proof

With one `1`, rotate to `(1,2,...,2)`. Then

\[
B-D=2\,3^{h-1}.
\]

Since `gcd(D,6)=1` and `D>=5`, divisibility is impossible.

With two `1`s, rotate to
`(1,2^(r-1),1,2^(h-r-1))`, `1<=r<=floor(h/2)`. Direct summation gives

\[
B-D=3^{h-r-1}(2\,3^r+4^r).
\]

The small factor is strictly between `0` and `D` for `h>=6`, by the two-step
induction

\[
U_{h+2}<4U_h<4D_h<D_{h+2}.
\]

The only boundary height `h=5` has `D=13` and remainders `10,34`.

With three `1`s, let their cyclic gaps be `r,s,t>=1` and rotate so `t` is
largest. Then

\[
B-D=3^{t-1}Q_{r,s},
\quad
Q_{r,s}=2\,3^{r+s}+4^r3^s+{4^{r+s}\over2}.
\]

Since `r+s<=floor(2h/3)`, a three-step induction gives `0<Q<D` after the
base heights `9,10,11`; height `8` is checked exactly. Since `gcd(D,3)=1`,
all three cases are nondivisible.

The exact-integer audit checks all displayed factorizations through height
24 with zero failures.

**Discarded route:** extending the TICKET-231 `0<B<D` size certificate into
the critical strip. The one-defect family has `B>D` in every rotation, so
the residue factorization is essential.

**Finite-computation limit:** the scan validates formulas and boundary
cases; the induction proves the infinite families. Binary words with four or
more `1`s, words using valuations at least `3`, and aperiodic divergence are
untouched.

**Next lemma:** `BinaryFourOneCriticalStripNondivisibility`.

## 3. Strong Goldbach track

### Declared proposition

Let `l` be odd prime and let nonnegative weights `omega_p` be supported on
actual primes `p<=X`, initially excluding `p=l`. Define

\[
S(\alpha)=\sum_p\omega_p e(p\alpha),\quad
W_r=\sum_{p\equiv r\pmod l}\omega_p,\quad
W=\sum_rW_r,
\]

`mu=W/(l-1)`, `delta_r=W_r-mu`, and `n=N mod l`. Then the complete
denominator-`l` rational shell is exactly

\[
T_l(N)=\sum_{a=1}^{l-1}S(a/l)^2e(-aN/l)
=l\!\sum_{r+s\equiv N\pmod l}W_rW_s-W^2.
\]

If `l|N`,

\[
T_l(N)={W^2\over l-1}+l\sum_r\delta_r\delta_{-r}.
\]

If `n!=0`,

\[
T_l(N)=-{W^2\over(l-1)^2}
+l\left(\sum_{r\ne n}\delta_r\delta_{n-r}-2\mu\delta_n\right).
\]

Writing `E=sum delta_r^2` gives the respective error bounds `lE` and
`l(E-delta_n^2+2mu|delta_n|)`. The omitted local prime is restored exactly:
if `b=omega_l`, add `2b(lW_n-W)+b^2 c_l(N)`.

### Proof, no-go, and computation

Expand the shell and use the prime Ramanujan sum

\[
\sum_{a=1}^{l-1}e(at/l)=l\,1_{l\mid t}-1.
\]

Substitution of `W_r=mu+delta_r` proves the identities; Cauchy proves the
bounds.

There is also a rigorous inference counterfamily. Set `n=1`, `mu=1`,
`epsilon=l^(-1/2)`,

\[
W_1=1-\epsilon,
\qquad
W_r=1+{\epsilon\over l-2}\quad(r\ne1).
\]

Every weight is positive and the maximum classwise relative discrepancy
tends to zero, but the uniform shell equals `-1` while

\[
T_l(1)=-1+l\left(2\epsilon+{\epsilon^2\over l-2}\right)>0.
\]

Thus classwise relative equidistribution `o(1)` alone does not control the
size or sign of growing rational shells. This is a residue-weight
counterfamily, not a Goldbach counterexample.

The exact audit checks 40 actual-prime indicator rows. At
`X=100,l=5,N=66`, the residue masses `[5,7,7,5]` give exact shell `19`,
whereas the uniform singular coefficient predicts `-36`; the autocorrelation
correction is `+55`.

**Discarded route:** replacing growing rational shells by their singular
coefficient using only classwise `o(1)` relative equidistribution.

**Remaining gap:** rational-arc neighborhoods, composite denominators,
actual-prime autocorrelation estimates uniform in the denominator, and the
signed aggregate over denominators remain open.

**Next lemma:**
`UniformGrowingDenominatorPrimeResidueAutocorrelationAtSingularCoefficientScale`.

## 4. Twin-prime track

### Declared proposition

For finite `L` of primes `l>=5`, let `A_l` exclude `0,-2`, let `U` be the
uniform CRT product measure, and normalize the centered quadratic signs to
`psi_l`. Give nonnegative weights to at most `N` admissible CRT points and
let `b_S` be the normalized coefficient of `psi_S=product_(l in S)psi_l`.
For the quadratic-sign pushforwards `nu_Y,U_Y`,

\[
\sum_{\varnothing\ne S\subseteq L}b_S^2
=\chi^2(\nu_Y\Vert U_Y)
\ge\max\left(0,{1\over Nu_L}-1\right),
\]

where

\[
u_L=\max_yU_Y(y)
=\prod_{l\in L}{l-1\over2(l-2)}.
\]

For `L={5<=l<=sqrt(X)}` and `N<=X`, this lower bound tends to infinity.

### Proof, no-go, and computation

Each `{1,psi_l}` is an orthonormal basis of its two-point sign space, so the
tensor products are a complete basis. Parseval gives the chi-square identity.
If the pushforward support is `B`, Cauchy gives

\[
1\le(\chi^2+1)U_Y(B)\le(\chi^2+1)Nu_L.
\]

The prime number theorem and
`u_L<=2^(-m)exp(m/3)`, `m=pi(sqrt(X))-2`, prove divergence.
The exact lower bounds at `X=10^4,10^5,10^6` are approximately
`266.01`, `2.35e13`, and `2.00e43`.

A second counterfamily has `m=k^2`, `epsilon=1/k`, and density
`product_l(1+epsilon psi_l)`. Every nonconstant coefficient tends to zero,
but the full energy tends to `e-1`. Coefficientwise decay therefore cannot
be naively summed over all `2^m` modes.

**Discarded route:** full, unweighted, positive growing-CRT interaction
energy `o(principal^2)` at twin-sieve scale. This does not refute decay for
any fixed or suitably damped family of coefficients.

**Remaining gap:** no positive twin mass is created. Entropy-matched degree
damping, a signed Type-II aggregate estimate, and a separate positive
principal lower bound remain open.

**Next lemma:** `EntropyMatchedSignedCRTInteractionLargeSieveAtTwinScale`.

## Proof DAG summary

| Problem | New exact result | Discarded route | Highest-risk next lemma | Parent status |
|---|---|---|---|---|
| Riemann | adaptive positive floor needs logarithmic effective dimension | sublog adaptive repair | logarithmic adaptive Weil frame with explicit tail dominance | open |
| Collatz | binary critical-strip words with at most three `1`s are nondivisible | unchanged `B<D` extension | four-`1` binary nondivisibility | open |
| Goldbach | exact prime rational-shell autocorrelation identity | classwise `o(1)` implies shell control | uniform prime autocorrelation at singular scale | open |
| Twin prime | full CRT energy equals chi-square and has a sparsity lower bound | full unweighted positive energy saving | entropy-matched signed CRT large sieve | open |

## Final boundary

The new theorems are infinite where their proofs say so; the finite rows only
reproduce formulas and constants. None supplies the missing positivity,
descent, or cancellation needed to resolve a parent conjecture.
