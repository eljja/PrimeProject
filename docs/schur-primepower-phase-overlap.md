# TICKET-235: Schur Complements, Prime-Power Deficits, Phase Retrieval, and CRT Overlaps

## Claim status

**Open, not proven.** This ticket proves four exact partial or no-go results. It
resolves none of the Riemann hypothesis, the Collatz conjecture, strong
Goldbach, or the twin-prime conjecture. The machine-readable resolution count
is `0 / 4`.

External status was checked on 2026-08-21 against the [Clay Riemann hypothesis
page](https://www.claymath.org/millennium/Riemann-Hypothesis/), the current
[Collatz verification algorithm](https://arxiv.org/abs/2602.10466) and its
[live verification record](https://pcbarina.fit.vut.cz/), recent
[Goldbach exceptional-set work](https://arxiv.org/abs/2607.27282), and
[Maynard's bounded-gap theorem](https://annals.math.princeton.edu/2015/181-1/p07).
These sources confirm the surrounding frontier; none is treated as a proof of
one of the four conjectures.

## Reproducible contract

- Generator: `scripts/ticket235_schur_primepower_phase_overlap.py`
- Tests: `tests/test_ticket235_schur_primepower_phase_overlap.py`
- Integrated JSON: `data/open-problem/ticket235-schur-primepower-phase-overlap.json`
- Exact partial/no-go theorems: `4`
- Refuted route families: `4`
- Parent conjectures resolved: `0`
- Machine failures: `0`

All displayed rational certificates are generated with Python integers and
`Fraction`. The calculations instantiate exact all-parameter arguments; they
do not turn a finite search into an asymptotic proof.

## 1. Riemann track

### Declared proposition

`ExactKernelSchurComplementCriterionAndCrossBlockNoGo`.

Let a finite Hermitian truncation of the TICKET-234 Weil-form route be written
on `R direct-sum K`, where `K=ker(G)`, as

\[
H=G+E=\begin{pmatrix}A&B\\B^*&C\end{pmatrix},\qquad A>0.
\]

Then

\[
H\ge0\quad\Longleftrightarrow\quad C-B^*A^{-1}B\ge0.
\]

Positive kernel compression `C>0` plus absolute `B=o(1)` is not sufficient.
For

\[
G=\operatorname{diag}(I_M,0_d),\quad C=T^{-2}I_d,
\quad B=(2/T)e_1f_1^*,
\]

the affected Schur eigenvalue is `-3/T^2`, although `C>0` and every entry of
`B` tends to zero.

### Proof and exact computation

Completing the square gives

\[
\langle H(r,k),(r,k)\rangle
=\langle A(r+A^{-1}Bk),r+A^{-1}Bk\rangle
+\langle(C-B^*A^{-1}B)k,k\rangle.
\]

This is an equivalence, not merely a sufficient estimate. In the rank-one
family the Schur minimum is exactly `epsilon-delta^2`. The same kernel scale
with `delta=1/(2T)` gives the positive value `3/(4T^2)`, identifying the
missing requirement as a *relative* cross-block estimate.

| `T` | `M=ceil(8 log(2T))` | kernel dimension | adverse Schur minimum | safe Schur minimum |
|---:|---:|---:|---:|---:|
| 64 | 39 | 25 | `-3/4096` | `3/16384` |
| 256 | 50 | 206 | `-3/65536` | `3/262144` |
| 1024 | 61 | 963 | `-3/1048576` | `3/4194304` |
| 4096 | 73 | 4023 | `-3/16777216` | `3/67108864` |

**Discarded route.** Kernel-compression positivity together with absolute
entrywise or operator-norm smallness of the cross block.

**Logical limit.** The matrices are abstract Hermitian truncations, not the
actual arithmetic Guinand--Weil tail. No zeta zeros are computed, and no
arithmetic relative form bound is proved.

**Next single lemma.**
`ArithmeticWeilTailRelativeCrossBlockSchurDominanceOnCofinalLogarithmicFrames`.

## 2. Collatz track

### Declared proposition

`BinaryRunBlockPrimitiveDivisorOrderCharacterizationAndSelectionNoGo`.

For a valuation word `a=(a_0,...,a_(h-1))`, put

\[
D=2^{\sum a_i}-3^h,qquad
B=\sum_{j=0}^{h-1}3^{h-1-j}2^{\sum_{i<j}a_i}.
\]

**Lineage correction.** TICKET-224 already proved that prime-presence-only
exclusion fails for general valuation words. Its primitive witness
word

\[
a=(1,1,2,4,3)
\]

has

\[
D=1805=5\cdot19^2,qquad B=475=5^2\cdot19.
\]

has `rad(D)=95` dividing `B` while `D` does not divide `B`. This is retained as
an `already_closed_regression_only` row and is not counted as a new result.

The new TICKET-235 theorem is the following order characterization inside the
binary frontier. For
`w_k=1^k2^(2k)`, TICKET-197 gives

\[
D_k=32^k-27^k,qquad B_k=32^k+27^k-2\cdot18^k.
\]

For every prime `q` not dividing six,

\[
q\mid\gcd(D_k,B_k)
\Longleftrightarrow
\operatorname{ord}_q(3/2)\mid k
\quad\text{and}\quad
\operatorname{ord}_q(4)\mid k.
\]

At `k=14`, `q=29` is a primitive divisor of `D_14`, because
`ord_29(32/27)=14`, but it also divides `B_14` because the other two orders
are `7` and `14`. Choosing an arbitrary primitive divisor is therefore not a
valid nondivisibility certificate.

### Proof and exact computation

The first counterexample is direct factorization. For the binary identity,
subtracting `D_k` from `B_k` modulo `q` gives `(3/2)^k=1`. Since
`32/27=4(3/2)^(-3)`, the equation `D_k=0` then gives `4^k=1`. Reversing these
steps proves the converse.

The extended lineage-regression scan used canonical primitive necklaces over
`{1,2,3,4,5}`, heights `2..8`, and retained only `D>1`:

| canonical words | primitive necklaces | `rad(D)|B`, `D` not dividing `B` |
|---:|---:|---:|
| 63,426 | 63,185 | 1 |

The unique row is the already-known TICKET-224 word. The new modular-order audit used all
primes up to `5000` and `13<=k<=256`; it found zero failures in the exact
order characterization and `56` primitive divisors that also divide `B_k`.

**Discarded route.** Reopening the already-closed TICKET-224 radical target,
and selecting an arbitrary primitive divisor in the binary density band.

**Logical limit.** The radical counterexample contains valuations `3,4`, so it
does not refute the binary `{1,2}` adaptive-radical successor. The primitive
divisor row does not rule out a different, order-separated prime. Unbounded
words, valuations at least three in general, and aperiodic behavior remain
open.

**Next single lemma.**
`UniformBinaryDensityBandOrderSeparatedAdaptivePrimeWitness`.

## 3. Strong Goldbach track

### Declared proposition

`CompleteMarginalPowerSpectrumPhaseRetrievalNoGo`.

Complete separate marginal Fourier powers still do not determine a
target-reflected cross coefficient. On `Z/qZ`, for every odd `q>=5`, let

\[
x=1_{\{0,1\}},\quad y_0=1_{\{0,-1\}},\quad y_2=1_{\{1,2\}}.
\]

The measure `y_2` is a translate of `y_0`, so their full autocorrelations and
all Fourier powers agree:

\[
|\widehat y_0(a)|^2=|\widehat y_2(a)|^2\quad\text{for every }a.
\]

The masses and `L2` norms are also identical, while

\[
(x*y_0)(0)=2,qquad (x*y_2)(0)=0.
\]

### Proof and exact computation

Translation multiplies a Fourier transform by a unit phase and hence preserves
every power. Equivalently, its cyclic autocorrelation is unchanged. But target
zero convolution is `sum_t x(t)y(-t)`: both `t=0,1` contribute for `y_0`, and
neither contributes for `y_2`.

The generator checked all `24` primes `5<=q<=101` using exact integer cyclic
autocorrelations. Every marginal coordinate agreed, while the target values
were always `2` and `0`.

**Discarded route.** Recovering the TICKET-234 reflected low-high coherence
from complete *separate* power spectra, shell energies, or autocorrelations.

**Logical limit.** These are finite-group two-point measures, not prime
weights. The result does not refute a joint arithmetic phase estimate that
uses `p+(N-p)=N`, and it is not a Goldbach counterexample.

**Next single lemma.**
`ActualPrimeReflectedCrossSpectrumPhaseLockingAtInverseLogScale`.

## 4. Twin-prime track

### Declared proposition

`FixedDegreeCesaroOverlapMomentReductionAndDegreeOneNoGo`.

For centered normalized CRT coordinates, let

\[
b_S=\mathbb E_\nu\prod_{i\in S}\psi_i,qquad
E_{m,k}={1\over{m\choose k}}\sum_{|S|=k}b_S^2.
\]

Take independent `X,Y` with law `nu`, put
`z_i=psi_i(X)psi_i(Y)` and `R_m=m^(-1)sum_i z_i`. Then

\[
E_{m,k}=\mathbb E\frac{e_k(z_1,\ldots,z_m)}{{m\choose k}}
\]

exactly, and

\[
|E_{m,k}-\mathbb E R_m^k|
\le 2^{k+1}\left(1-{(m)_k\over m^k}\right)
\le {2^k k(k-1)\over m}.
\]

Degree one is not sufficient. On the Rademacher product space, take

\[
\nu={1\over2}\delta_{(+1,\ldots,+1)}
+{1\over2}\delta_{(-1,\ldots,-1)}.
\]

Then every singleton coefficient is zero but every pair coefficient is one:
`E_(m,1)=0`, `E_(m,2)=1` for all `m`.

### Proof and exact computation

Expanding `b_S^2` with two independent samples and averaging over all
`k`-subsets gives the elementary-symmetric identity. `R_m^k` samples ordered
coordinates with replacement; the Cesaro expression samples without
replacement. Their mismatch probability is `1-(m)_k/m^k`, and both products
are at most `2^k` in absolute value.

An exact diagnostic row conditioned on the `202` twin starts below `10,000`
and CRT primes `(5,7,11,13)` reproduced all four TICKET-234 Cesaro energies:

| degree | Cesaro energy = elementary overlap moment |
|---:|---:|
| 1 | `3257/1958592` |
| 2 | `9265/5875776` |
| 3 | `6301/3917184` |
| 4 | `9/81608` |

**Discarded route.** Degree-one Cesaro decay, or mean pair overlap alone, as a
surrogate for every fixed interaction degree.

**Logical limit.** The Rademacher mixture is not an arithmetic prime weight.
The twin-start row is finite and conditions on the objects whose infinitude is
at issue. Type-II overlap concentration, parity transfer, and positive main
mass all remain open.

**Next single lemma.**
`PrimeWeightedCRTPairOverlapMomentConcentrationAtTwinScale`.

## Proof DAG and final boundary

Each machine-readable DAG has one `closed` TICKET-235 node, one precisely
`refuted_or_limited` route, one `highest_risk_open` successor, and an
`open_not_proven` parent conjecture. The integrated JSON is authoritative for
node and edge identifiers.

The new results are structural reductions and certified no-go theorems. They
do not constitute a proof or disproof of any of the four conjectures.
