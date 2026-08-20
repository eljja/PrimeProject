# TICKET-231: Summable Frames, the Collatz Critical Strip, a Gauss Counterfamily, and CRT Orthogonality

## Claim status

**Open, not proven.** TICKET-231 proves four exact partial or no-go results. It
does not prove or disprove the Riemann hypothesis, the Collatz conjecture,
strong Goldbach, or the twin-prime conjecture. The machine-readable resolution
count remains `0 / 4`.

This ticket also corrects two inherited targets. The TICKET-230 Goldbach spike
has a same-order aligned Fourier error, but its convolution is still positive;
it was not a counterexample to pointwise positivity. The literal Collatz target
"every primitive positive-denominator necklace is nondivisible" contains the
trivial divisible word `(2)`. The corrected statements below remove both
logical defects.

## Reproducible contract

- Generator: `scripts/ticket231_summable_frame_critical_strip_gauss_crt.py`
- Tests: `tests/test_ticket231_summable_frame_critical_strip_gauss_crt.py`
- Integrated JSON: `data/open-problem/ticket231-summable-frame-critical-strip-gauss-crt.json`
- Status: `open_not_proven`
- Exact partial/no-go theorems: `4`
- Corrected or discarded routes: `4`
- Parent conjectures resolved: `0`
- Machine failures: `0`

## 1. Riemann track

### Declared proposition

Let `q_j>1`, let `w_j>=0` with `sum_j w_j<infinity`, and suppose two
positive-weight dilations are multiplicatively independent. Define

\[
F(n)=\sum_{j\ge1}w_j|1-q_j^{-in}|^2.
\]

For every head size `M` and integer `Q>=2`, some `1<=n<=Q^M` satisfies

\[
F(n)\le {4\pi^2\over Q^2}\sum_{j\le M}w_j
       +4\sum_{j>M}w_j.
\]

Consequently,

\[
\liminf_{n\to\infty}F(n)=0.
\]

Thus no fixed absolutely summable infinite dilation family has a positive
uniform frame floor on all integer frequencies.

### Proof

Apply simultaneous pigeonhole approximation to the first `M` coordinates
`log(q_j)/(2 pi)`. The resulting integer `n` has all head phase distances at
most `1/Q`. The inequality

\[
|1-e^{-2\pi ix}|^2\le4\pi^2\|x\|^2
\]

bounds the head, while `|1-z|^2<=4` bounds the summable tail. Choose `M` so
the tail is arbitrarily small and then let `Q` grow. For fixed such `M`, the
witnesses are unbounded: otherwise one positive integer would recur and make
the two independent phases vanish exactly, contradicting multiplicative
independence.

### Result and limit

TICKET-230 ruled out a positive floor for every fixed finite family at a
quantified recurrence scale. TICKET-231 closes the naive repair by a fixed
absolutely summable infinite family. This is a scalar dilation-energy no-go,
not a positivity theorem for the Weil quadratic form.

**Discarded route:** a fixed absolutely summable infinite family with a
positive uniform frequency floor.

**Remaining gap:** construct a height-adaptive or nonsummable-renormalized
frame and prove that its explicit floor dominates the full Weil-tail error.

**Next lemma:**
`HeightAdaptiveRenormalizedWeilFrameWithExplicitTailDominance`.

## 2. Collatz track

### Declared proposition

For an accelerated odd Collatz cycle word `a=(a_0,...,a_(h-1))`, put

\[
S=\sum_j a_j,\quad D=2^S-3^h,
\]

and let `B(a)` be its standard cycle numerator. If `S>=2h`, a cyclic rotation
of `a` has every suffix valuation sum at least twice its length. For that
rotation,

\[
{B\over2^S}\le\sum_{r=1}^{h}{3^{r-1}\over4^r}
=1-\left({3\over4}\right)^h.
\]

Hence

\[
B\le2^S-2^{S-2h}3^h\le2^S-3^h=D,
\]

with equality only when every `a_j=2`. Therefore every nontrivial positive
cycle must satisfy the strict critical-strip condition

\[
h\log_2 3<S<2h.
\]

### Proof

Set `b_j=a_j-2`. Its total is nonnegative. Rotate immediately after a maximal
cumulative sum. Every suffix sum of the rotated `b` is then nonnegative, which
gives the termwise geometric bound above. Equality requires `S=2h` and every
suffix inequality to be equality, hence `a_j=2` for all `j`. Otherwise
`0<B<D`, so `D` cannot divide `B`. TICKET-230 proved that `D|B` is invariant
under cyclic rotation, so the certificate applies to the original necklace.

### Result and limit

This strictly strengthens the earlier pointwise condition "every valuation is
at least two": mixed words containing valuation `1` are also excluded whenever
their average is at least two. The exact audit checks all words over
`{1,...,5}` through height seven. The all-two word is the known trivial cycle
and is deliberately retained.

**Discarded route:** the unqualified claim that all primitive
positive-denominator necklaces are nondivisible.

**Remaining gap:** exclude nontrivial necklaces in
`log_2(3)<S/h<2`, then independently exclude divergent aperiodic trajectories.

**Next lemma:** `CriticalStripPrimitiveNecklaceNondivisibility`.

## 3. Strong Goldbach track

### Declared proposition

For every prime `p=3 (mod 4)`, let `w_p` be the indicator of the nonzero
quadratic residues in `Z/pZ`. Its mass is `W=(p-1)/2`, but

\[
(w_p*w_p)(0)=0.
\]

For `k!=0`, with quadratic character `chi` and Gauss sum `tau_p`,

\[
\widehat w_p(k)={-1+\chi(k)\tau_p\over2},\qquad
|\tau_p|=\sqrt p,\quad\tau_p^2=-p.
\]

Therefore

\[
\max_{k\ne0}{|\widehat w_p(k)|\over W}
={\sqrt{p+1}\over p-1}\longrightarrow0,
\]

while the signed nonprincipal aggregate at zero equals `-W^2/p` and exactly
cancels the principal term.

### Proof

Since `chi(-1)=-1`, the negative of a nonzero quadratic residue is a
nonresidue, proving the zero convolution. Expressing the residue indicator as
`(1+chi)/2` away from zero gives the Fourier formula. For `p=3 (mod 4)`, the
quadratic Gauss sum is purely imaginary and has square `-p`, giving the exact
magnitude. Fourier inversion at zero then forces the stated signed aggregate.

### Correction and limit

This is the genuine counterfamily that TICKET-230 intended but did not supply.
It proves that modewise relative Fourier decay alone cannot imply pointwise
positivity. It is still **not** a Goldbach counterexample: quadratic-residue
indicators are not prime weights.

**Discarded route:** using the positive TICKET-230 spike convolution as a
counterexample to positivity.

**Remaining gap:** prove a one-sided bound for the target-aligned negative
minor-arc aggregate of actual prime weights below the positive singular-series
main term.

**Next lemma:**
`UniformNegativeBinaryPrimeMinorArcAggregateBelowSingularSeriesMainTerm`.

## 4. Twin-prime track

### Declared proposition

For an odd prime `l` not dividing the shift `h`, let

\[
A_l=\{r\pmod l:r\ne0,\ r+h\ne0\},\qquad
\mu_l={-\chi_l(-h)\over l-2},
\]

and set `phi_l=chi_l-mu_l` on `A_l`, where `chi_l` is quadratic. Under the
uniform CRT product measure define

\[
\Phi_S=\prod_{l\in S}\phi_l.
\]

If `S!=T`, then

\[
\mathbb E(\Phi_S\Phi_T)=0,
\]

and

\[
\|\Phi_S\|_2^2=\prod_{l\in S}
\left(1-{1\over(l-2)^2}\right).
\]

The modulo-three centered mode is identically zero. After removing degenerate
factors, normalized tensor modes form an orthonormal dictionary of centered
quadratic local interactions.

### Proof

TICKET-230 gives `E(phi_l)=0`. On `A_l`, `chi_l^2=1`, hence
`E(phi_l^2)=1-mu_l^2`. For distinct subsets, a coordinate in their symmetric
difference occurs to the first power. CRT independence factors out its zero
mean. Diagonal norms factor into the local variances.

### Result and limit

This separates deterministic local admissibility bias from prime-weighted
correlation and supplies an exact diagonal coordinate system for one family of
interactions. It is not a complete basis for all local functions and supplies
no prime cancellation estimate.

**Discarded route:** treating raw local bias, or the degenerate modulo-three
mode, as global prime evidence.

**Remaining gap:** uniformly bound the prime-weighted coefficients of growing
CRT interactions at the twin-sieve main scale and separately obtain a positive
principal lower bound despite the parity barrier.

**Next lemma:**
`PrimeWeightedGrowingCRTInteractionEnergySavingAtTwinSieveScale`.

## Proof DAG summary

| Problem | New exact result | Refuted or corrected | Highest-risk open lemma | Parent status |
|---|---|---|---|---|
| Riemann | summable infinite-frame liminf is zero | fixed summable positive floor | adaptive renormalized frame with Weil-tail dominance | open |
| Collatz | every nontrivial cycle lies in the valuation critical strip | unqualified all-necklace nondivisibility | critical-strip necklace nondivisibility | open |
| Goldbach | Gauss zero-convolution counterfamily | T230 spike as positivity counterexample | negative prime minor-arc aggregate below main term | open |
| Twin prime | centered CRT interaction orthogonality | raw local bias as global cancellation | prime-weighted growing-CRT energy saving | open |

## Reproduction

```powershell
python scripts\ticket231_summable_frame_critical_strip_gauss_crt.py
python -m unittest tests.test_ticket231_summable_frame_critical_strip_gauss_crt -v
```

## Literature boundary

The ingredients used here are classical. PrimeProject does not claim academic
priority for simultaneous approximation, Collatz cycle formulas and the cycle
lemma, quadratic Gauss sums, or CRT tensor orthogonality. The exact synthesis,
formal route corrections, machine contract, and project-specific successor
lemmas are the new repository artifacts. Primary or author-hosted context:

- Connes and Consani, [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368) and [Weil positivity and Trace formula](https://arxiv.org/abs/2006.13771).
- Lagarias, [The 3x+1 problem: an annotated bibliography](https://arxiv.org/abs/math/0309224) and [Part II](https://arxiv.org/abs/math/0608208).
- Helfgott, [Minor arcs for Goldbach's problem](https://arxiv.org/abs/1205.5252), for prime exponential-sum context; it does not settle binary Goldbach.
- Maynard, [Small gaps between primes](https://arxiv.org/abs/1311.4600), for the distinction between bounded gaps and gap two.
