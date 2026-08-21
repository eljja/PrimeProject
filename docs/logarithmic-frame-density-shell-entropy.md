# TICKET-233: Logarithmic Frames, a Twelve-One Collatz Closure, Squarefree Goldbach Shells, and CRT Entropy

## Claim status

**Open, not proven.** This ticket proves four exact partial/asymptotic/no-go
results. It resolves none of the Riemann hypothesis, the Collatz conjecture,
strong Goldbach, or the twin-prime conjecture; the machine-readable resolution
count is `0 / 4`.

External status and context were checked on 2026-08-21 against the
[Clay list of unsolved Millennium problems](https://www.claymath.org/problem/unsolved/),
the current [Collatz finite-verification algorithm](https://arxiv.org/abs/2602.10466),
the recent [Goldbach exceptional-set and major-arc work](https://arxiv.org/abs/2607.27282),
the [Thorner--Zaman Siegel--Walfisz input](https://arxiv.org/abs/2108.10878),
and [Maynard's bounded-gap theorem](https://annals.math.princeton.edu/2015/181-1/p07).
The external theorems are used only where explicitly identified below.

## Reproducible contract

- Generator: `scripts/ticket233_logarithmic_frame_density_shell_entropy.py`
- Tests: `tests/test_ticket233_logarithmic_frame_density_shell_entropy.py`
- Integrated JSON: `data/open-problem/ticket233-logarithmic-frame-density-shell-entropy.json`
- Exact partial/asymptotic/no-go theorems: `4`
- Corrected or discarded routes: `4`
- Parent conjectures resolved: `0`
- Machine failures: `0`

## 1. Riemann track

### Declared proposition

`LogarithmicAdaptiveScalarFrameExistenceAndSharpDimensionThreshold`.
For every integer `T>=2`, every prime `P>T`, and

\[
M=\lceil 8\log(2T)\rceil,
\]

there are residues `r_1,...,r_M (mod P)` such that, simultaneously for
`1<=n<=T`,

\[
{1\over M}\sum_{j=1}^{M}
  \left|1-e^{-2\pi i n r_j/P}\right|^2\ge 1.
\]

Replacing the zero residue representative by the real phase `1` and putting
`q_j=exp(2*pi*alpha_j)>1` gives an adaptive scalar dilation frame with a
uniform unit floor and `O(log T)` coordinates. Together with TICKET-232's
`Omega(log T)` necessity theorem, the scalar effective-dimension threshold is
therefore `Theta(log T)`.

### Argument and reproducible computation

Choose the residues independently and uniformly modulo `P`. Because `P>T`,
multiplication by each fixed `1<=n<=T` permutes the residue classes. Hence

\[
X_j=|1-e^{-2\pi i n r_j/P}|^2\in[0,4],\qquad \mathbb E X_j=2.
\]

Hoeffding gives

\[
\Pr\left({1\over M}\sum_jX_j<1\right)\le e^{-M/8}.
\]

A union bound over the `T` frequencies is at most
`T exp(-M/8)<=1/2`, so a common frame exists. The generator also records
deterministic seeded witnesses for `T=16,64,256,1024,4096`; every minimum
normalized energy is at least `1`.

**Discarded route.** Any claim that scalar phase energy itself needs
superlogarithmic adaptive dimension.

**Logical and finite-computation limit.** The probabilistic proof is an
existence theorem; the five seeded rows merely audit it. The scalar energy is
not the signed Guinand--Weil quadratic form, and no arithmetic tail domination
is proved.

**Next single lemma.**
`LogarithmicAdaptiveScalarFrameToWeilKernelTransferWithExplicitSignedTailDominance`.

## 2. Collatz track

### Declared proposition

`BinaryLineageCorrectionTwelveOneExclusionAndFixedStratumNoGo`.

For a valuation word `a in {1,2}^h`, let `k` be its number of ones and

\[
D(a)=2^{2h-k}-3^h,
\qquad
B(a)=\sum_{j=0}^{h-1}3^{h-1-j}2^{a_0+\cdots+a_{j-1}}.
\]

TICKET-182 identifies `D>0` and `D|B` with realization of a positive
accelerated cycle. The TICKET-232 successor with four ones was not open:
the binary layer was already closed by TICKET-188 and the stronger
arbitrary-tail layer by TICKET-209. In fact TICKETS 188--195 already close
all binary multiplicities `4<=k<=11`.

This ticket closes the first genuinely open binary fixed stratum:

> No positive accelerated Collatz cycle has exactly twelve valuation ones
> and every other valuation equal to two.

Thus any hypothetical binary cycle has `k>=13`; the stronger arbitrary-tail
lineage TICKETS 206--210, 213, and 214 gives `k>=8` for a general valuation
cycle. Every hypothetical binary cycle may be reduced to a primitive necklace
and must satisfy

\[
\log_2(6/5)\le{k\over h}<2-\log_2 3.
\]

### Exact proof and computation

Normalize the first one to `p_0=0<p_1<...<p_11<h`. Telescoping the step
function that counts prior ones gives the exact separable numerator

\[
B=C_h+\sum_{i=1}^{11}E_{i,h}(p_i).
\]

The formula was exhaustively compared with direct prefix summation on all
`18,564` normalized words for `12<=h<=18`, plus `2,176` deterministic samples
in the decision range, with zero mismatches.

Contraction first holds at `h=29`. The necessary positive-cycle product bound

\[
1\le 2^{12}(5/6)^h
\]

holds at `h=45` but fails at `h=46`, so only `29<=h<=45` remains. Split the
eleven free boundary terms into `5+6`. Left residues are activated exactly
when `p_5<p_6`; each right residue is matched against its complement modulo
`D`. Vandermonde's identity verifies complete coverage

\[
\sum_{h=29}^{45}{h-1\choose11}
={45\choose12}-{28\choose12}=28,729,599,990.
\]

The exact-integer MITM finds zero divisibility hits. It stores per-height
coverage counts and SHA-256 transcripts. No probabilistic inference is used.

There is also a strict no-go for repeated fixed strata. For every `m>=1`,
the primitive word `1^m2^(2m)` has `(h,k)=(3m,m)` and lies in the density
band because `216<250` and `27<32`. For prime `k`, the `h=3k` slice contains
exactly

\[
{1\over3k}\left({3k\choose k}-3\right)
\]

primitive necklaces. Therefore a finite fixed-`k` ladder is noncofinal even
after quotienting by rotation, although this does not rule out a uniform
analytic theorem.

**Discarded route.** Reopening the already closed four-one node, or promoting
an indefinitely repeated finite fixed-multiplicity enumeration into a cofinal
proof strategy.

**Logical and finite-computation limit.** The `k=12` computation is exhaustive
only because independent inequalities reduce the infinite stratum to the
finite range `29..45`. The height-22 density scan (`1,893,010` raw words,
`90,272` primitive necklaces, zero hits) is regression-only. Binary `k>=13`,
valuations at least three, and aperiodic divergence remain open.

**Next single lemma.**
`UniformBinaryDensityBandPrimitiveNecklaceNondivisibility`.

## 3. Strong Goldbach track

### Declared proposition

`PolylogarithmicSquarefreePrimeShellAsymptoticAndSparseDenominatorNoGo`.
Let `q` be odd and squarefree, let `W_r>=0` be masses on reduced residue
classes, let `W=sum_r W_r`, `mu=W/phi(q)`,
`delta_r=W_r-mu`, and
`epsilon=max_r |delta_r|/mu`. For the reduced rational shell,

\[
T_q(N)=\sum_{(a,q)=1}S(a/q)^2e(-aN/q),
\]

one has

\[
T_q(N)=\mu^2c_q(N)+R_q(N),
\]

\[
|R_q(N)|\le \mu^2\left(2\phi(q)^2\epsilon+
\phi(q)^3\epsilon^2\right).
\]

For logarithmic prime weights, Siegel--Walfisz therefore yields, for every
fixed `B`, uniformly over odd squarefree `q<=(log X)^B` and every target `N`,

\[
T_{q,X}(N)=\mu^2c_q(N)+o_B(\mu^2)
=\mu^2c_q(N)(1+o_B(1)).
\]

### Argument, Parseval identity, and no-go

For a reduced frequency `a` and squarefree `q`, `c_q(a)` is the Möbius
function of `q`. Writing the residue Fourier transform as
`mu * Mobius(q)+D_a` gives
`|D_a|<=phi(q) epsilon mu`; expansion and summation prove the deterministic
bound. Siegel--Walfisz gives
`epsilon=O_B(q exp(-c_B sqrt(log X)))`, which is enough throughout the stated
polylogarithmic range. Squarefree Ramanujan sums do not vanish.

For a prime denominator `l`, the correction has the exact spectral audit

\[
R_l(n)=\sum_{a=1}^{l-1}(S(a/l)^2-\mu^2)e(-an/l),
\]

\[
\sum_{n\bmod l}|R_l(n)|^2
=l\sum_{a=1}^{l-1}|S(a/l)^2-\mu^2|^2.
\]

Thus spectral energy `o(mu^4)` gives an RMS/most-target statement, while
`o(mu^4/l)` is a sufficient energy-only condition for uniform maximum
control. It is not asserted to be necessary.

An actual-prime counterfamily rules out unrestricted denominator growth.
For any `X>=2`, choose a prime `l>2X+1`, put `n=2X+1`, and take the even
target `N=l+n`. No primes `p,q<=X` have `p+q congruent n (mod l)`, hence

\[
T_l(N)=-W^2,
\qquad
{|R_l(N)|\over\mu^2}=l(l-2)\longrightarrow\infty.
\]

This is not a Goldbach counterexample: deliberately `X<N/2`.

**Discarded route.** Any rational-shell asymptotic uniform in a growing
denominator without a denominator--cutoff--target coupling, and any automatic
promotion from RMS energy to all targets.

**Logical and finite-computation limit.** The exact rows audit squarefree
algebra, Parseval, and the sparse family. Siegel--Walfisz is ineffective here.
Arc neighborhoods, targetwise minor-arc negative mass, and a positive lower
bound for every even target remain unproved.

**Next single lemma.**
`UniformTargetAlignedBinaryPrimeMinorArcNegativeMassBelowPolylogMajorArcMargin`.

## 4. Twin-prime track

### Declared proposition

`CriticalEntropyDampedSignedCRTLargeSieveAndParityRetentionNoGo`.
Use TICKET-232's normalized centered CRT signs `psi_l`, with
`b_S=E_nu psi_S`. For `0<=x_l<=1`, put `x_S=product_(l in S)x_l` and
`c_l=(l-1)/(l-3)<=2`. Then

\[
D_x:=\sum_{S\ne\varnothing}x_Sb_S^2
\le\prod_l(1+c_lx_l)-1.
\]

For arbitrary signs `|sigma_S|<=1`,

\[
\left|\sum_{S\ne\varnothing}\sigma_Sx_Sb_S\right|^2
\le
\left(\prod_l(1+x_l)-1\right)
\left(\prod_l(1+c_lx_l)-1\right).
\]

Thus `sum_l x_l=o(1)` forces a universal signed saving.

### Proof and two no-go conclusions

The two squared values of `psi_l` are `(l-3)/(l-1)` and
`(l-1)/(l-3)`. Jensen bounds `b_S^2` by `E_nu psi_S^2`; expanding the
product proves the energy bound, and Cauchy proves the signed bound.

At critical damping `x_l=tau/m`, however, the nonnegative normalized density

\[
g={1\over2}\prod_l(1+\psi_l/2)
  +{1\over2}\prod_l(1-\psi_l/2)
\]

has every singleton and every odd-degree coefficient equal to zero, while
`b_S=2^{-|S|}` in even degree. Its all-positive signed aggregate tends to
`cosh(tau/2)-1>0`. Local centering plus critical entropy therefore does not
give the desired saving.

If the full parity multiplier `x_L` must remain at least `eta>0`, AM--GM and
`1+x>=2sqrt(x)` force

\[
\sum_lx_l\ge m\eta^{1/m},
\qquad
\prod_l(1+x_l)-1\ge2^m\sqrt\eta-1.
\]

Bounded product entropy and full parity retention cannot hold simultaneously.

**Discarded route.** Critical product damping plus centered marginals as a
universal signed-saving theorem, or bounded product entropy together with
full-parity retention.

**Logical and finite-computation limit.** The counterfamily is a CRT
probability model, not actual prime weights. It proves neither positive twin
mass nor the presence or absence of infinitely many twin primes.

**Next single lemma.**
`PrimeWeightedCriticalNoiseCRTChiSquareDecayAtTwinScale`.

## Proof DAG

- `RH-T232 -> RH-T233 -> RH-OPEN233 -> RH`
- `CO-T182,T188,T195,T209,T214 -> CO-T233`; the former `CO-OPEN232` is
  recorded as the refuted lineage node `CO-N232`; then `CO-T233 -> CO-OPEN233`
  feeds the still-open all-periodic boundary, while the separate aperiodic
  boundary also remains necessary before `CO`.
- `GB-T232, Siegel--Walfisz -> GB-T233 -> GB-OPEN233 -> GB`.
- `TP-T232 -> TP-T233 -> TP-OPEN233 -> TP`.

Every parent-conjecture node remains `open_not_proven`.
