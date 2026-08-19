# TICKET-230: Quantitative Recurrence, Necklace Invariance, Fourier Aggregation, and Local Centering

## Claim status

**Open, not proven.** TICKET-230 proves four exact structural or no-go
statements. It does not prove or disprove the Riemann hypothesis, the Collatz
conjecture, strong Goldbach, or the twin-prime conjecture. The machine
resolution count remains `0 / 4`.

This ticket audits the four successor lemmas left by TICKET-229. One of those
targets, raw modulo-five quadratic cancellation for shift two, was malformed:
the correct local mean is `1/3`, not zero. Correcting a target before spending
analytic effort on it is the main methodological result of this iteration.

## Reproducible contract

- Generator: `scripts/ticket230_quantitative_recurrence_necklace_fourier_centering.py`
- Tests: `tests/test_ticket230_quantitative_recurrence_necklace_fourier_centering.py`
- Integrated JSON: `data/open-problem/ticket230-quantitative-recurrence-necklace-fourier-centering.json`
- Status: `open_not_proven`
- Exact partial/no-go theorems: `4`
- Corrected or discarded routes: `4`
- Parent conjectures resolved: `0`
- Machine failures: `0`

## 1. Riemann track

### Declared proposition

Fix integers `q_1,...,q_m > 1`, where `m >= 2` and at least two members are
multiplicatively independent, and define

\[
F(t)=\sum_{j=1}^m |1-q_j^{-it}|^2.
\]

For every integer `Q >= 2`, there is an integer `1 <= n <= Q^m` such that

\[
F(n)\le \frac{4\pi^2m}{Q^2}.
\]

The witnesses contain an unbounded subsequence, and on that subsequence

\[
F(n)\le 4\pi^2m\,n^{-2/m}.
\]

Consequently, a fixed finite dilation family cannot have a global lower floor
`L(t)` for which `t^(2/m)L(t) -> infinity`.

### Proof

Partition the `m`-torus into `Q^m` cubes of side `1/Q` and place the `Q^m+1`
points

\[
k\left(\frac{\log q_1}{2\pi},\ldots,\frac{\log q_m}{2\pi}\right)\pmod 1,
\qquad 0\le k\le Q^m.
\]

Two points occupy one cube. Their index difference `n` satisfies
`||n log(q_j)/(2 pi)|| <= 1/Q` for every `j`. The inequality

\[
|1-e^{-2\pi ix}|^2=4\sin^2(\pi x)\le4\pi^2\|x\|^2
\]

gives the bound. If all witnesses stayed bounded while `Q` grew, one fixed
positive `n` would have zero energy. Two zero phases would make a ratio of
logs rational and contradict multiplicative independence. Finally,
`n <= Q^m` implies `Q^(-2) <= n^(-2/m)`.

### Result and limit

This strengthens the earlier qualitative near-alias theorem by supplying an
explicit unavoidable recurrence rate. It also shows that the word
"subexponential" alone is not a sufficient frame specification: the proposed
floor and the actual Weil-core tail must be compared at the recurrence scale.

It does **not** provide Weil positivity, an infinite weighted frame, or a bound
for the actual Weil-core truncation tail. The Riemann hypothesis remains open.

**Discarded route:** any fixed finite-family lower floor that decays more
slowly than `T^(-2/m)`.

**Next lemma:**
`AdaptiveInfiniteDilationFrameWithWeilTailDominanceBelowRecurrenceScale`.

## 2. Collatz track

### Declared proposition

For an accelerated odd Collatz valuation word
`a=(a_0,...,a_(h-1))`, put

\[
S=\sum_j a_j,\qquad D=2^S-3^h,
\]

and

\[
B(a)=\sum_{j=0}^{h-1}3^{h-1-j}2^{a_0+\cdots+a_{j-1}}.
\]

Let `rho(a)` be the left cyclic rotation. Then

\[
2^{a_0}B(\rho a)=3B(a)+D.
\]

If `D>0`, then

\[
\gcd(D,B(\rho a))=\gcd(D,B(a))
\]

and `D | B(rho a)` if and only if `D | B(a)`.

### Proof

Write `B(a)=3^(h-1)+2^(a_0)C`. Expanding the rotated numerator gives
`B(rho a)=3C+2^(S-a_0)`. Multiplying by `2^(a_0)` yields
`3B(a)+2^S-3^h`. The integer `D` is odd and is coprime to `3` because
`D = 2^S (mod 3)`. Multiplication by `2^(a_0)` and by `3` is therefore
invertible modulo `D`, proving both invariances.

### Result and limit

Cycle divisibility is a necklace invariant. Testing all cyclic rotations of a
word is duplicated evidence, not independent evidence. The exact finite audit
checks primitive positive-denominator words over the alphabet `{1,...,5}`
through height six and reduces `15,402` height-six words to `2,567` necklace
representatives with no identity failures.

The bounded search is not a proof that every primitive necklace fails `D | B`.
Even a complete nondivisibility theorem would rule out nontrivial cycles but
would not rule out divergent aperiodic trajectories.

**Discarded route:** treating cyclic rotations as independent cycle tests.

**Next lemma:**
`NecklaceRepresentativeNondivisibilityForEveryPrimitivePositiveDenominatorWord`.

## 3. Strong Goldbach track

### Declared proposition

Modewise relative Fourier decay does not imply pointwise positivity in a
growing cyclic group. Let `L=m^2` and, on `Z/LZ`, define

\[
w_m(x)=1+m\,1_{x=a}.
\]

Its mass is `W=m^2+m`, and every nonprincipal Fourier coefficient has
magnitude `m`. Thus

\[
\max_{k\ne0}\frac{|\widehat w_m(k)|}{W}=\frac1{m+1}\longrightarrow0.
\]

Nevertheless,

\[
(w_m*w_m)(2a)=2m^2+2m,
\qquad \frac{W^2}{L}=m^2+2m+1,
\]

so the target-aligned nonprincipal error is `m^2-1`, the same order as the
principal term.

### Proof

The constant background has zero transform at every nonzero mode. The spike
contributes `m exp(-2 pi i k a/L)`. At target `2a`, its square and the inverse
transform phase cancel exactly for every nonprincipal `k`, so all `L-1` modes
align. Their normalized total is `m^2(L-1)/L=m^2-1`. Direct convolution gives
the same result.

### Result and limit

This is a counterexample to an inference rule, not a Goldbach counterexample.
It proves that separate `o(W)` bounds for a growing number of modes do not
control their signed, target-aligned sum. The prime-weighted problem requires
an explicit major/minor-arc decomposition and aggregate phase control.

The constructed weights are not prime weights. No pointwise lower bound for
binary prime convolution is proved.

**Discarded route:** promoting individual mode bounds to pointwise Goldbach
positivity without a uniform aggregate estimate.

**Next lemma:**
`UniformBinaryPrimeMinorArcSignedAggregateBelowSingularSeriesMainTerm`.

## 4. Twin-prime track

### Declared proposition

Let `l` be an odd prime, `h != 0 (mod l)`, and let `chi` be a nonprincipal
multiplicative character extended by `chi(0)=0`. For the admissible shift set

\[
A=\{r\pmod l:r\ne0,\ r+h\ne0\},
\]

one has

\[
\sum_{r\in A}\chi(r)=-\chi(-h),
\qquad
\frac1{|A|}\sum_{r\in A}\chi(r)=\frac{-\chi(-h)}{l-2}.
\]

For `l=5`, `h=2`, and the quadratic character, `A={1,2,4}` and the raw mean
is `1/3`, not zero.

### Proof

The admissible set removes `0` and `-h` from a complete residue system. A
nonprincipal character sums to zero on that system and `chi(0)=0`; the sum
left after removing `-h` is `-chi(-h)`. Modulo five, the values on `1,2,4`
are `1,-1,1`.

### Result and limit

TICKET-229 correctly identified a full-size modulo-five quadratic mode, but
its raw-zero successor target was incorrectly centered. The correct observable
is the quadratic character minus its local mean `1/3`. The committed finite
twin counts through `10^6` audit only admissible residues and do not prove an
asymptotic distribution.

This local identity neither proves infinitely many twin primes nor overcomes
the sieve parity barrier. A principal lower bound is still independently
required.

**Discarded route:** raw modulo-five quadratic cancellation to zero.

**Next lemma:**
`CenteredModFiveQuadraticTypeIISavingAtTwinSieveMainScale`.

## Proof DAG summary

| Problem | Closed in TICKET-230 | Refuted or corrected | Highest-risk open lemma | Parent status |
|---|---|---|---|---|
| Riemann | quantitative finite-dilation recurrence | slower-than-`T^(-2/m)` finite-family floor | adaptive/infinite frame matched to Weil tail | open |
| Collatz | necklace invariance of `D|B` and `gcd(D,B)` | independent rotation evidence | all primitive positive-denominator necklace representatives fail divisibility | open |
| Goldbach | aligned Fourier counterfamily | modewise `o(W)` implies pointwise positivity | signed minor-arc aggregate below singular-series main term | open |
| Twin prime | exact admissible character mean | raw mod-5 mean zero | centered Type-II saving at sieve main scale | open |

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket230_quantitative_recurrence_necklace_fourier_centering.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket230_quantitative_recurrence_necklace_fourier_centering -v
```

## Literature boundary

The ticket combines classical tools and project-specific route auditing. It
does not claim academic priority for simultaneous Dirichlet approximation,
Collatz cycle numerators, cyclic Fourier inversion, or local character sums.
The exact synthesis, machine contract, and route corrections are the new
PrimeProject artifacts. Relevant primary or author-hosted research context:

- Connes and Consani, [Weil positivity and Trace formula, the archimedean place](https://arxiv.org/abs/2006.13771).
- Lagarias, [The 3x+1 problem: an annotated bibliography](https://arxiv.org/abs/math/0309224) and [Part II](https://arxiv.org/abs/math/0608208).
- Helfgott, [The ternary Goldbach conjecture is true](https://arxiv.org/abs/1312.7748), for circle-method and prime exponential-sum context; this does not settle binary Goldbach.
- Maynard, [Small gaps between primes](https://arxiv.org/abs/1311.4600), for the distinction between bounded gaps and gap two.
