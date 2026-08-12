# TICKET-220: Dyadic partition, primitive-word closure, refinement stability, and a finite-wheel CRT no-go

## Claim status

TICKET-220 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, the strong Goldbach conjecture, or the Twin Prime conjecture. It
proves four narrower statements, rejects four overstrong proof routes, and
records one explicit next lemma for each open problem. The machine-readable
resolution count remains `0`.

The new results are:

1. dyadic Laplace band kernels form a partition of total RH-defect
   multiplicity, while every finite band window misses a suitably remote atom;
2. the TICKET-219 Collatz single-mountain exclusion extends to every cyclic
   rotation and positive power of such a primitive word;
3. a cross-fitted Goldbach support certificate is stable under fold refinement
   whenever an exact Minkowski margin is positive;
4. every admissible class of every fixed finite twin wheel contains an infinite
   CRT progression on which both candidate integers are composite.

These statements are exact within their declared hypotheses. None bridges the
remaining infinite or parity-sensitive gap by itself.

## 1. Riemann track

### Declared proposition

Let (C) be a nonnegative integer-valued locally finite measure on
((0,\infty)), and write

\[
L(s)=\int_0^\infty e^{-st}\,dC(t).
\]

For (H>0) and (j\in\mathbb Z), define

\[
W_j(H)=L(2^{-j}/H)-L(2^{1-j}/H).
\]

Then

\[
\sum_{j=-M}^{N}W_j(H)
=L(2^{-N}/H)-L(2^{M+1}/H),
\]

and monotone convergence gives

\[
\sum_{j\in\mathbb Z}W_j(H)=C((0,\infty)),
\]

with the value (+\infty) allowed. For every finite set of indices (J) and
every (\varepsilon>0), there is a one-atom defect measure for which

\[
\sum_{j\in J}W_j(H)<\varepsilon.
\]

Therefore finitely many band values alone cannot certify (C=0).

### Proof

At a fixed (t>0), the (j)-th kernel is

\[
k_j(t)=e^{-2^{-j}t/H}-e^{-2^{1-j}t/H}\ge 0.
\]

Its finite sum telescopes. As (N\to\infty), the first boundary exponential
tends to one; as (M\to\infty), the second tends to zero. Thus
(\sum_j k_j(t)=1). Tonelli's theorem transfers the identity to (C).

For a fixed finite (J), every (k_j(t)) tends to zero as (t\downarrow0)
and as (t\to\infty). The finite sum has the same limits, so one atom can be
placed outside the observed scale window with total observed weight below any
prescribed epsilon.

### Reproducible computation

The audit uses six synthetic atoms and checks the telescope at symmetric
windows (M=N\in\{2,4,8,12,16\}) with 100-digit decimal arithmetic. It also
places atoms at (2^{-40}) and (2^{40}) and verifies that the window
(-4\le j\le4) sees less than (10^{-6}) of either atom. These calculations
replay the theorem; they are not evidence about actual zeta zeros.

### Closed route and remaining gap

**Discarded:** a fixed finite collection of dyadic defect bands is a global RH
certificate.

**Retained:** if rigorous prime-side bounds (U_j\ge W_j) can be constructed
with certified tails and

\[
\sum_{j\in\mathbb Z}U_j<1,
\]

then integrality forces the total defect count to be zero.

**Next lemma:** `PrimeSideSummableDyadicBandpassEnvelopeBelowOne`.

No such actual prime-side summable envelope is proved in TICKET-220.

## 2. Collatz track

### Declared proposition

Let (u) be a cyclic rotation of a binary accelerated-Collatz valuation word
(1^k2^m), where (k,m\ge1). No positive accelerated Collatz cycle has word
(u^r) for any integer (r\ge1).

### Proof

Align a hypothetical cycle at the start of one copy of (u). One block acts
by an affine rational map

\[
f(n)=\frac{An+B}{D},\qquad A=3^h,\quad D=2^S.
\]

Unique factorization gives (A\ne D). If (r) copies close, then
(f^r(n)=n). Writing (a=A/D>0),

\[
f^r(n)-n=(f(n)-n)(1+a+\cdots+a^{r-1}).
\]

The second factor is positive, so (f(n)=n). This would be a positive
single-mountain cycle, which TICKET-219 excludes. A cyclic rotation changes
only the selected base point of the same cycle.

### Reproducible computation

The script composes exact integer triples ((A,B,D)) for representative roots
and powers and verifies both the composition and fixed-point identities. It
also classifies all binary words of lengths 2 through 16 by primitive root and
cyclic transition count. This enumeration is a consistency check; the affine
argument proves the infinite family.

### Closed route and remaining gap

**Discarded:** treating rotations or repeated copies of a single-mountain word
as new independent cycle candidates.

**New closed family:** every positive power and rotation of every
single-mountain primitive root. This includes displayed words with arbitrarily
many runs, but only imprimitive ones.

**Remaining gap:** primitive multi-run valuation words and nonperiodic divergent
orbits.

**Next lemma:** `EffectiveBakerSeparationForPrimitiveMultiRunValuationWords`.

## 3. Strong Goldbach track

### Declared proposition

Let (F'\subset F) be a refined held-out fold. Fit a positive model scale
(\alpha) outside (F) and a positive scale (\beta) outside (F'). For
counts (A_i), weights (w_i>0), and residuals
(e_i(\gamma)=A_i-\gamma w_i),

\[
\|e(\beta)\|_{\ell^p(F')}
\le
\|e(\alpha)\|_{\ell^p(F')}
+|\alpha-\beta|\,\|w\|_{\ell^p(F')}.
\]

If the right-hand side is strictly below
(\beta\min_{i\in F'}w_i), then every count on (F') is positive.

### Proof

The coordinate identity

\[
e_i(\beta)=e_i(\alpha)+(\alpha-\beta)w_i
\]

and Minkowski's inequality give the norm bound. If (A_j=0) for one held-out
coordinate, then

\[
|e_j(\beta)|=\beta w_j\ge\beta\min_{i\in F'}w_i,
\]

contradicting the strict upper bound.

### Reproducible computation

The audit uses exact Goldbach representation counts on five dyadic blocks,
(X\in\{128,512,2048,8192,32768\}), and residue folds modulo
(2,4,8,16). Least-squares scales are exact rational numbers. Eighth roots
are rounded outward to rational multiples of (10^{-12}), so a reported
strict pass remains rigorous for the finite data.

- direct (p=8) support certificates: `150 / 150` folds;
- direct (p=4) support certificates: `137 / 150` folds;
- nested refinement bridges (2\to4\to8\to16): `140 / 140`;
- largest certified bridge-to-barrier ratio: approximately `0.9670275612`.

### Closed route and remaining gap

**Discarded:** treating success under finitely many increasingly fine folds as
a cofinal proof of Goldbach.

**Retained:** use the refinement inequality as an interface for two analytic
inputs: a cofinal parent residual bound and a cofinal bound on scale-refit
drift.

**Next lemma:**
`CofinalCrossFitRefinementMarginWithoutRepresentationEnumeration`.

The present audit reads the representation counts and therefore cannot prove
that every sufficiently large even integer has a representation.

## 4. Twin Prime track

### Declared proposition

Let (W) be squarefree and let (a\pmod W) satisfy
(\gcd(a(a+2),W)=1). There are infinitely many integers (n\equiv a\pmod W)
for which both (n) and (n+2) are composite.

### Proof

Choose distinct primes (q,r\nmid W). The Chinese remainder theorem solves

\[
n\equiv a\pmod W,\qquad n\equiv0\pmod q,\qquad n\equiv-2\pmod r.
\]

All solutions form one progression modulo (Wqr). Every sufficiently large
member has (q) as a proper divisor of (n) and (r) as a proper divisor of
(n+2). It remains in the original admissible wheel class.

### Reproducible computation

Exact CRT witnesses are generated for
(W=30,210,2310,30030,510510). Each row verifies admissibility, both proper
composite divisors, and preservation of the full progression.

### Closed route and remaining gap

**Discarded:** survival of a fixed finite wheel is sufficient to certify a twin
prime or twin infinitude.

**Scope of the no-go:** only fixed finite local divisibility information. It
does not rule out growing sieves, bilinear forms, distribution estimates, or
other global information.

**Next lemma:** `ParitySensitiveBilinearLowerBoundBeyondEveryFiniteWheel`.

## Proof DAG summary

| Problem | Closed TICKET-220 node | Rejected route | Highest-risk open node |
|---|---|---|---|
| Riemann | `DyadicLaplacePartitionAndFiniteWindowNoGo` | finite window certifies global absence | `PrimeSideSummableDyadicBandpassEnvelopeBelowOne` |
| Collatz | `PrimitiveRootExtensionOfSingleMountainExclusion` | repeated roots create new fixed points | `EffectiveBakerSeparationForPrimitiveMultiRunValuationWords` |
| Goldbach | `CrossFitPartitionRefinementStabilityCertificate` | finite refinements imply a cofinal theorem | `CofinalCrossFitRefinementMarginWithoutRepresentationEnumeration` |
| Twin Prime | `FiniteWheelTwinCertificationCRTNoGo` | fixed-wheel survival certifies twins | `ParitySensitiveBilinearLowerBoundBeyondEveryFiniteWheel` |

Every final conjecture node remains `open_not_proven`.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket220_dyadic_partition_primitive_refinement_crt.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket220_dyadic_partition_primitive_refinement_crt -v
```

Primary machine-readable audit:

`data/open-problem/ticket220-dyadic-partition-primitive-refinement-crt.json`

The audit records exact propositions, proof text, calculation rows, SHA-256
transcripts where applicable, proof DAGs, rejected routes, remaining gaps, and
zero parent-conjecture resolutions.
