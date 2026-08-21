# TICKET-234: Operator Kernels, Binary Sieve False Positives, Goldbach Half-Channels, and Poisson CRT Noise

## Claim status

**Open, not proven.** This ticket proves four exact partial, equivalence, or
no-go results. It resolves none of the Riemann hypothesis, the Collatz
conjecture, strong Goldbach, or the twin-prime conjecture. The machine-readable
resolution count is `0 / 4`.

External status and context were checked on 2026-08-21 against the
[Clay list of unsolved Millennium problems](https://www.claymath.org/problem/unsolved/),
the current [Collatz finite-verification algorithm](https://arxiv.org/abs/2602.10466),
the recent [Goldbach exceptional-set and major-arc work](https://arxiv.org/abs/2607.27282),
the [Thorner--Zaman Siegel--Walfisz input](https://arxiv.org/abs/2108.10878),
and [Maynard's bounded-gap theorem](https://annals.math.princeton.edu/2015/181-1/p07).
External results are used only where named below.

## Reproducible contract

- Generator: `scripts/ticket234_operator_kernel_density_minor_cesaro.py`
- Tests: `tests/test_ticket234_operator_kernel_density_minor_cesaro.py`
- Integrated JSON: `data/open-problem/ticket234-operator-kernel-density-minor-cesaro.json`
- Exact partial/equivalence/no-go theorems: `4`
- Discarded route families: `4`
- Parent conjectures resolved: `0`
- Machine failures: `0`

## 1. Riemann track

### Declared proposition

`ScalarDiagonalFrameRankAndSignedTailTransferNoGo`.

Let the `M x T` adaptive dilation-analysis matrix be

\[
V_{j,n}=\sqrt{w_j/W}\,(1-e^{-in\theta_j}),\qquad 1\le n\le T.
\]

If `T>M`, then `rank(V)<=M`, so the Gram form `G=V*V` has a nonzero
kernel even if every scalar diagonal `G_nn` is bounded below by one. For every
unit `u in ker(V)` and every `epsilon>0`, the Hermitian signed perturbation

\[
H_\varepsilon=G-\varepsilon uu^*
\]

has perturbation operator norm `epsilon`, every perturbation entry has
magnitude at most `epsilon`, and

\[
u^*H_\varepsilon u=-\varepsilon.
\]

Thus the TICKET-233 pure-frequency scalar floor does not, by itself, transfer
to positivity of the full signed Guinand--Weil quadratic form.

### Proof and exact computation

Rank-nullity is the main proof. TICKET-233 has
`M=ceil(8 log(2T))<T` from `T=35` onward, while its seeded constructions have
all pure-frequency energies at least one. A positive diagonal is therefore
compatible with an exact null direction. An arbitrarily small negative
rank-one tail on that direction destroys positivity.

The rational-phase examples also admit an explicit kernel polynomial. If `Z`
is the set of distinct nontrivial phase roots, put

\[
C(x)=x(x-1)\prod_{z\in Z}(x-z)=\sum_{n\ge1}c_nx^n.
\]

Then

\[
\sum_nc_n(1-z_j^n)=C(1)-C(z_j)=0.
\]

The generator reduces this formal identity modulo an auxiliary prime with a
primitive `P`-th root, so every residual is checked with exact integer
arithmetic.

| `T` | `M` | nullity lower bound | auxiliary prime | kernel degree |
|---:|---:|---:|---:|---:|
| 64 | 39 | 25 | 269 | 34 |
| 256 | 50 | 206 | 1543 | 51 |
| 1024 | 61 | 963 | 2063 | 61 |
| 4096 | 73 | 4023 | 73783 | 75 |

All modular residuals are zero.

**Discarded route.** Transferring a logarithmic scalar diagonal floor to full
Weil positivity using only a norm-small or entrywise-small tail estimate.

**Logical limit.** The adverse rank-one tail is an abstract Hermitian tail,
not the actual arithmetic Weil tail. Special arithmetic alignment on the
kernel may still save the approach. The computation says nothing about the
location of zeta zeros.

**Next single lemma.**
`ArithmeticWeilTailKernelCompatibilityAndPositiveSchurComplement`.

## 2. Collatz track

### Declared proposition

`UniformBinaryDensityBandFixedFiniteAffineSieveNoGo`.

For every `K>=13` and every nonempty finite family of moduli `M>1` coprime to
six, infinitely many `k>=K` have the following property. The primitive binary
word

\[
w_k=1^k2^{2k}
\]

and all its cyclic rotations lie in the TICKET-233 necessary density band,
every fixed test reports `M|D` and `M|B`, but the exact cycle condition fails:

\[
D\nmid B.
\]

### Proof and exact computation

On `Z/MZ`, put

\[
F_a(x)=2^{-a}(3x+1),\qquad a\in\{1,2\}.
\]

These are affine permutations. Let `r_1,r_2` be their finite orders and take
`k` to be an arbitrarily large multiple of their common least common multiple,
simultaneously over the finite modulus family. Then

\[
F_{w_k}=F_2^{2k}\circ F_1^k=\mathrm{id}.
\]

The general affine iterate is

\[
F_a(x)=2^{-S}(3^hx+B(a)),
\]

so the identity forces every fixed modulus to divide both `D=2^S-3^h` and
`B`. The word is primitive because it has exactly two cyclic symbol
transitions. Its density is `k/h=1/3`, and it is in the required band because
`216<250` and `27<32`.

TICKET-197's closed forms give

\[
D_k=32^k-27^k,
\qquad
B_k=32^k+27^k-2\cdot18^k,
\]

\[
B_k-D_k=2\cdot9^k(3^k-2^k).
\]

Since `gcd(D_k,18)=1`, divisibility would force
`D_k|(3^k-2^k)`. This is impossible because

\[
0<3^k-2^k<5\cdot27^{k-1}\le D_k.
\]

The rotation recurrence `2^(a_0)B'=3B+D` preserves both the modular false
positive and exact nondivisibility.

The exact audit checked all `66` moduli `5<=M<200` coprime to six. The maximum
base `k` was `198`; every affine order, direct prefix numerator, closed form,
density condition, and divisibility flag passed. Simultaneous families
`(5,7)`, `(5,7,11)`, and `(5,7,11,13)` also passed with zero failures.

A separate exact factor scan of `1,893,010` binary density-band words through
height `22` retained `90,272` primitive necklaces and found no case with
`rad(D)|B` but `D` not dividing `B`. This is finite successor evidence only.

**Discarded route.** Any fixed finite affine-modulus or fixed finite
prime-power sieve as a cofinal proof of binary density-band nondivisibility.

**Logical limit.** Adaptive moduli or prime divisors depending on the word are
not ruled out. The radical scan does not reach the current `k>=13` frontier.
Valuations at least three and aperiodic divergence remain open.

**Next single lemma.** `UniformBinaryDensityBandAdaptiveRadicalDeficit`:
every remaining primitive binary candidate has a prime `q|D` with `q` not
dividing `B`.

## 3. Strong Goldbach track

### Declared proposition

`MinorArcMarginGoldbachEquivalenceAndPrimeHalfChannelCancellationNoGo`.

For

\[
S_N(\alpha)=\sum_{p\le N}\log p\,e(p\alpha),
\qquad
G_\theta(N)=\int_0^1S_N(\alpha)^2e(-N\alpha)d\alpha,
\]

split any symmetric major/minor partition into real contributions `M_N,m_N`.
If `M_N>0`, then

\[
m_N>-M_N\quad\Longleftrightarrow\quad G_\theta(N)>0.
\]

The proposed strict full minor margin is therefore the weighted Goldbach
endpoint itself, not a weaker auxiliary lemma.

There is also an exact structural no-go. Split primes below and above `N/2`
into `L_N,U_N`, with a separate midpoint term. Then

\[
[e(N\alpha)]L_N^2=[e(N\alpha)]U_N^2=0,
\]

but each square has positive central-major mass of order `N` and hence exactly
the opposite negative minor mass.

### Proof, reflection, and computation

For the central arc `||alpha||<=1/(4N)`, the exact integral kernel is

\[
K_N(d)=\frac{\sin(\pi d/(2N))}{\pi d}
\]

with its continuous value `1/(2N)` at zero. Concavity of sine gives
`K_N(d)>=1/(pi N)` for a same-half offset. Thus, with half masses `W_L,W_U`,

\[
M_{LL}\ge {W_L^2\over\pi N},
\qquad
M_{UU}\ge {W_U^2\over\pi N}.
\]

The full same-half target coefficients are zero, so the complementary minor
integrals are exactly `-M_LL,-M_UU`. The prime number theorem makes each at
most `-(1/(4*pi)+o(1))N`.

Reflect the upper half around the target:

\[
V_N(\alpha)=\sum_{m<N/2\atop N-m\ \mathrm{prime}}
\log(N-m)e(m\alpha).
\]

Then `U_N(alpha)e(-N alpha)=conjugate(V_N(alpha))` and

\[
G_\theta(N)=2\langle L_N,V_N\rangle
+1_{N/2\ \mathrm{prime}}\log^2(N/2).
\]

The missing information is therefore target-dependent reflected cross phase,
not a marginal shell or norm. Both half channels still satisfy the
TICKET-233 polylogarithmic rational-center asymptotic by applying
Siegel--Walfisz at `N` and `N/2`.

| `N` | central `LL` | central `UU` | central `LU` | full reflection cross |
|---:|---:|---:|---:|---:|
| 100 | 7.550355 | 8.210933 | 8.627483 | 73.090775 |
| 1000 | 100.463917 | 102.698832 | 112.386938 | 911.522295 |
| 10000 | 1070.810337 | 1099.953125 | 1203.390134 | 8371.568403 |

**Discarded route.** Treating the strict full minor margin as a weaker lemma;
promoting rational-center control or separate dyadic square-channel norms to
targetwise minor signs.

**Logical limit.** This does not refute a correctly structured full-prime
minor-arc estimate. The finite arc values use floating logarithms and sine;
only Fourier cancellation is exact. The cross-channel inverse-log coherence
bound remains unproved.

**Next single lemma.**
`ComplementaryHalfPrimeReflectionMinorCoherenceAtInverseLogScale`.

## 4. Twin-prime track

### Declared proposition

`PoissonizedFixedDegreeCesaroCriterionAndMovingPrimeNoGo`.

For the normalized centered quadratic CRT signs of TICKET-233, let

\[
E_{m,k}={1\over {m\choose k}}\sum_{|S|=k}|b_{m,S}|^2,
\qquad
D_m=\sum_{S\ne\varnothing}m^{-|S|}|b_{m,S}|^2.
\]

For probability measures, or signed measures of total variation at most one,

\[
D_m\to0
\quad\Longleftrightarrow\quad
E_{m,k}\to0\text{ for every fixed }k.
\]

### Proof, Poissonization, and countermodel

Grouping by degree gives

\[
D_m=\sum_{k=1}^m{m\choose k}m^{-k}E_{m,k}.
\]

For fixed `k`, the weight tends to `1/k!` and is at most `1/k!`. The normalized
signs have square at most two, so `E_(m,k)<=2^k`; the summable bound `2^k/k!`
proves the equivalence by dominated triangular convergence. Selecting each
coordinate independently with probability `1/(m+1)` gives an exact identity
whose degree converges to `Poisson(1)`.

Fixed-labelled coefficient decay is insufficient. On the last half of the
coordinates, the positive normalized density

\[
g_m=\prod_{i>\lfloor m/2\rfloor}(1+\psi_i/2)
\]

has every fixed labelled coefficient eventually zero, while

\[
D_m=\left(1+{1\over4m}\right)^{\lceil m/2\rceil}-1
\longrightarrow e^{1/8}-1>0.
\]

Exact countermodel values for `m=4,8,16,32` run from `33/256` to
`0.132598...`. A separate exact rational audit on observed twin starts gave
`D_4=12301/5222912` at `X=10^4`, and `D_6=0.000612907...`,
`D_8=0.000560975...` at `X=10^5`.

**Discarded route.** Pointwise decay of each fixed labelled CRT coefficient as
sufficient for critical-noise decay.

**Logical limit.** The moving-half density is not a prime weight. The finite
twin-start audit conditions on already observed twins and is not asymptotic.
Even critical-noise decay leaves parity retention and positive principal mass
open.

**Next single lemma.**
`PrimeWeightedFixedDegreeCesaroCRTCorrelationDecayAtTwinScale`.

## Consolidated proof DAG

```text
RH-T233 -> RH-T234 -> RH-N234 [refuted]
                   -> RH-OPEN234 -> RH [open]

CO-T197 + CO-T223 + CO-T233 -> CO-T234 -> CO-N234 [refuted]
                                         -> CO-OPEN234 -> periodic/aperiodic gaps -> CO [open]

GB-T233 + PNT -> GB-T234 -> GB-N234 [refuted]
                           -> GB-OPEN234 -> GB [open]

TP-T233 -> TP-T234 -> TP-N234 [refuted]
                   -> TP-OPEN234 -> parity/principal-mass gaps -> TP [open]
```

## Final boundary

The new results identify four stronger obstructions or exact reformulations.
They do not prove or disprove any parent conjecture. Finite computations audit
the displayed identities and countermodels; only the stated algebraic and
asymptotic arguments extend beyond the computed ranges.
