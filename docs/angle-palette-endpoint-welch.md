# TICKET-237: Principal Angles, Finite-Palette No-Go, Dyadic Endpoints, and Welch Floors

Status: **open_not_proven**
Generated: 2026-08-24
Parent-conjecture resolutions: **0 / 4**

TICKET-237 directly audits the four highest-risk lemmas left by TICKET-236.
It proves four exact partial or no-go theorems. It does not prove or disprove
the Riemann hypothesis, the Collatz conjecture, strong Goldbach, or the
twin-prime conjecture.

## 1. Riemann hypothesis track

### Declared proposition

**PrincipalAngleCriterionAndNestedCofinalFrameNoGo.**

Let \(U:\mathbb C^m\to\mathcal H\) and
\(V:\mathbb C^n\to\mathcal H\) be injective synthesis maps in a
finite-dimensional Hilbert space, and put

\[
A=U^*U,\qquad B=U^*V,\qquad C=V^*V,\qquad
K=A^{-1/2}BC^{-1/2}.
\]

The singular values of \(K\) are the cosines of the principal angles between
\(\operatorname{ran}U\) and \(\operatorname{ran}V\). Consequently

\[
\|K\|_{\mathrm{op}}=1
\iff \operatorname{ran}U\cap\operatorname{ran}V\ne\{0\},
\]

and strict contraction is equivalent to a positive smallest principal angle.
Every nonzero nested pair therefore has normalized cross norm exactly one.
Nested cofinal frames cannot provide the strict TICKET-236 gap unless their
common modes are removed.

### Argument and reproducible calculation

The maps

\[
Q_U=U(U^*U)^{-1/2},\qquad Q_V=V(V^*V)^{-1/2}
\]

are isometries onto the two spans and \(K=Q_U^*Q_V\), the principal-angle
matrix. Norm one means that a unit vector in one span has projection norm one
onto the other, which is equivalent to a nonzero intersection.

For orthogonal isometries \(Q,W\), take

\[
U=Q,\qquad V=(3Q+4W)/5.
\]

Then the spans are disjoint, \(K=(3/5)I\), and the normalized block minimum is
\(2/5\). Exact rational rows at \(m=2,4,8,16,32\) compare this innovation
family with nested frames, whose norm and block minimum are \(1\) and \(0\).

Limit: this is finite-dimensional Gram geometry, not an arithmetic estimate
for the Guinand-Weil cross block. It proves no uniform arithmetic angle gap
and tests no zeta zero.

- Discarded route: obtain strict contraction directly from nested cofinal
  frames containing common modes.
- Retained route: quotient the common span and estimate innovations on
  disjoint logarithmic shells.
- Next single lemma:
  **ArithmeticWeilInnovationCrossBlockAngleGapOnDisjointLogarithmicShells**

## 2. Collatz track

### Declared proposition

**NoFinitePrimePaletteUniversallySeparatesBinaryRunBlocks.**

For \(w_k=1^k2^{2k}\), write

\[
D_k=32^k-27^k,\qquad B_k=32^k+27^k-2\cdot18^k.
\]

For every finite set \(S\) of primes there is \(L\ge1\) such that, for every
positive multiple \(k\) of \(L\) and every \(q\in S\),

\[
q\nmid D_k\quad\text{or}\quad q\mid B_k.
\]

Thus no \(q\in S\) is a presence separator \(q\mid D_k,\ q\nmid B_k\). One
may take

\[
L=\operatorname{lcm}_{q\in S,\ q>3}
\left(\operatorname{ord}_q(32/27),\operatorname{ord}_q(3/2)\right).
\]

No fixed finite prime palette is universal.

### Argument and reproducible calculation

The primes 2 and 3 never divide \(D_k\). For \(q>3\), the first order
condition makes \(D_k=0\pmod q\). Under both order conditions,

\[
\frac{B_k}{27^k}
=(32/27)^k+1-2(2/3)^k
=1+1-2=0\pmod q.
\]

The lcm disables every palette prime simultaneously, and all positive
multiples of the lcm give infinitely many such blocks.

Exact order and modular-power audits give:

| finite palette | common period \(L\) |
|---|---:|
| \(5\) | 2 |
| \(2,3,5,7,59\) | 174 |
| \(5,7,13,19,31,37,59\) | 5,220 |
| \(2,3,5,7,13,19,31,37,59,57653\) | 2,594,340 |

Every palette is disabled at \(L,2L,3L\). The finite rows instantiate the
all-finite-set proof; they are not an inference from a finite trend.

Limit: the theorem stays inside the run-block family already excluded by
TICKET-197. It proves that fresh primes are necessary, not that a presence or
valuation-gap witness exists for every \(k\) or every primitive necklace. It
does not address aperiodic trajectories.

- Discarded route: any fixed finite prime palette, however large, as a
  universal certificate.
- Retained route: select a word-dependent fresh prime and prove a valuation
  gap rather than presence alone.
- Next single lemma:
  **WordDependentPrimeValuationGapForEveryPrimitiveBinaryDensityBandNecklace**

## 3. Strong Goldbach track

### Declared proposition

**TruncatedDyadicUpperEndpointObstructionAndBulkWindowNecessity.**

Let \(x_X\) be the indicator of primes at most \(X\) and let
\(g_X=x_X*x_X\) be the ordered representation count. At the moving upper
endpoint,

\[
g_X(2X)=\mathbf 1_{\mathbb P}(X).
\]

The TICKET-236 normalized reflected-phase margin is therefore zero or
\(1/\pi(X)\), and always

\[
\frac{g_X(2X)}{\pi(X)}
\le\frac1{\pi(X)}
=o(1/\log X).
\]

No fixed positive inverse-log margin can hold on a closed dyadic target
window containing \(2X\); for composite \(X\), even strict positivity fails.

### Argument and reproducible calculation

If \(p,q\le X\) and \(p+q=2X\), then \(p<X\) would force \(q>X\).
Thus \(p=q=X\) is the only candidate. Substitution in the TICKET-236 identity

\[
q_{\rm mod}g_X(N)=M_X-\Delta_X(N)
\]

gives the exact phase margin. The prime number theorem yields the asymptotic
no-go, while composite cutoffs already yield exact zero.

At \(X=30,31,100,101,1000,1009,10000,10007\), the four composite rows have
count zero and the four prime rows count one. Every row reconstructs
\(M_X-\Delta_X(2X)=q_{\rm mod}g_X(2X)\) exactly.

Limit: this is a truncation-geometry endpoint obstruction. It does not refute
a fixed buffered window \(N\le(2-\eta)X\), a cutoff at least \(N\), or a
target-specific major/minor argument. It is not a Goldbach counterexample.

- Discarded route: a uniform inverse-log margin on a closed window including
  \(2X\).
- Retained route: remove a fixed upper-endpoint buffer and make the major gain
  dominate an independently bounded minor loss in the bulk.
- Next single lemma:
  **BufferedDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack**

## 4. Twin-prime track

### Declared proposition

**FiniteSupportWelchFloorForDegreeTwoCRTOverlap.**

Let \(\nu\) be supported on \(s\) atoms and let
\(\mathbb E_\nu\phi_i^2=1\) for \(i=1,\ldots,m\). Define

\[
C_{ij}=\mathbb E_\nu(\phi_i\phi_j),\qquad
E_{m,2}={1\over\binom m2}\sum_{i<j}C_{ij}^2.
\]

With \(r=\min(m,s)\),

\[
E_{m,2}\ge {m-r\over r(m-1)}.
\]

If the functions are centered, one may take \(r=\min(m,s-1)\). If
\(\alpha\le C_{ii}\le\beta\), then

\[
E_{m,2}\ge
\max\left(0,{m\alpha^2/r-\beta^2\over m-1}\right).
\]

Hence degree-two decay with nondegenerate diagonals and \(m\to\infty\)
forces the support size to grow.

### Argument and reproducible calculation

The matrix \(C\) is a positive-semidefinite Gram matrix of rank at most \(s\).
For its nonzero eigenvalues,

\[
\|C\|_F^2=\sum_j\lambda_j^2
\ge {(\operatorname{tr}C)^2\over r}.
\]

In the unit-diagonal case,
\(\|C\|_F^2=m+m(m-1)E_{m,2}\), giving the Welch bound. Centering places the
columns in the mean-zero hyperplane and lowers the rank cap to \(s-1\).
The \(\alpha,\beta\) form follows from the trace and diagonal-square bounds.
Repeated nonconstant Walsh columns attain the centered bound exactly.

The exact sharp rows are

\[
(s,m,E_{m,2})=(4,6,1/5),(4,12,3/11),(8,14,1/13),
(8,28,1/9),(16,30,1/29).
\]

Finite actual twin-start diagnostics are:

| \(X\) | \(m\) | support \(s\) | standardized \(E_{m,2}\) | Welch floor |
|---:|---:|---:|---:|---:|
| 100 | 6 | 4 | 0.2099807… | \(1/10\) |
| 200 | 12 | 9 | 0.0919019… | \(1/33\) |
| 300 | 18 | 11 | 0.0934479… | \(7/187\) |

Limit: the actual rows condition on already known twin starts and empirically
rescale every coordinate. They cannot prove support growth. Uniform diagonal
control under the local CRT normalization, arithmetic \(E_2\) decay, positive
principal mass, and the parity barrier remain open.

- Discarded route: interpret bounded-support finite samples as evidence that
  degree-two energy can decay.
- Retained route: include support growth and diagonal nondegeneracy in the
  prime-weighted degree-two estimate.
- Next single lemma:
  **PrimeWeightedDegreeTwoCRTDecayWithGrowingSupportAndUniformDiagonalControl**

## Proof DAG and claim boundary

Each track contains one TICKET-237 **closed** theorem, one
**refuted_or_limited** route, one **highest_risk_open** successor, and an
**open_not_proven** parent boundary. The canonical DAG, exact fractions, and
transcript hashes are in
data/open-problem/ticket237-angle-palette-endpoint-welch.json.

Finite computations certify only the displayed identities and ranges. The
all-parameter statements come from the separately stated linear-algebra,
order, and combinatorial arguments. The parent resolution count remains zero.
