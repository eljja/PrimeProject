# TICKET-227: Mellin, Block, and Buchstab Factor Lifts

Korean edition: [mellin-block-buchstab-lifts.ko.md](mellin-block-buchstab-lifts.ko.md)

## Abstract and claim boundary

TICKET-227 continues the four open branches left by TICKET-226. It proves four
exact structural lemmas. It does **not** prove or disprove the Riemann,
Collatz, strong Goldbach, or Twin Prime conjectures.

| Problem | New exact result | Route discarded or corrected | One next lemma |
|---|---|---|---|
| Riemann hypothesis | A single dilation ratio has infinitely many Mellin aliases; ratios `2` and `3` have no common nonconstant alias on `Re(s)=1` | One balanced dilation family separates all Mellin modes | `UniformDualDilationMellinFrameBoundOnExplicitDenseWeilCore` |
| Collatz conjecture | A fractional-linear endpoint criterion proves every `(1,1,3)^r,(4,2,1)` is a primitive noncycle | Finite repetition checks establish an infinite family | `UniversalPrimePowerWitnessForPrimitiveValuationWordNondivisibility` |
| Strong Goldbach conjecture | Cube-root rough-semiprime errors lift exactly to factor-resolved `N-qr` cells, with an explicit split when `q|N` | One-variable marginals estimate every pointwise cell | `UniformMovingResiduePrimeEstimateForCubeRootBuchstabCellsAtEveryEvenTarget` |
| Twin Prime conjecture | Shift-two errors lift exactly to `qr-2`, `qr+2`, and `pq+2=rs`; the two factor sets in every `SS` term are disjoint | Factor disjointness itself supplies cancellation | `UniformShiftTwoBilinearPrimeEstimateForQrPlusMinus2AcrossAllCubeRootCells` |

The common advance is a change of coordinates. Each coarse observable is
lifted to the coordinates in which its exact obstruction is visible: Mellin
frequency, Collatz affine composition, or prime-factor cells.

## 1. Riemann hypothesis

### Proposition RH-227

For `q>1`, `a>0`, and a suitable error function `E`, define

```text
B_q[E](a) = a integral_0^infinity
              E(x)(exp(-ax)-q exp(-qax)) dx.
```

For the Mellin mode `E_s(x)=x^(s-1)`, `Re(s)>0`,

```text
B_q[E_s](a) = a^(1-s) Gamma(s)(1-q^(1-s)).                 (RH-227.1)
```

On `s=1+i tau`, the `q=2` family is blind at every frequency

```text
tau = 2 pi k/log(2),  k in Z.                              (RH-227.2)
```

The joint `q=2` and `q=3` family has no common blind frequency except
`tau=0`.

### Proof

The Mellin-Laplace integral gives

```text
integral x^(s-1) exp(-cax) dx = Gamma(s)(ca)^(-s).
```

Apply it with `c=1` and `c=q` to obtain `(RH-227.1)`. On the line
`Re(s)=1`, the multiplier vanishes precisely when
`tau log(q)` is an integer multiple of `2 pi`. A nonzero common blind
frequency for `q=2,3` would give integers `k,l != 0` with

```text
k/log(2) = l/log(3),
```

and therefore `2^l=3^k`, contrary to unique prime factorization.

### Computation and limit

The artifact evaluates the first five `q=2` alias frequencies. The analytic
`q=2` multiplier vanishes while the corresponding `q=3` multiplier is
nonzero. A dependency-free log-coordinate composite Simpson quadrature
independently checks the first two frequencies to `1e-15` absolute error. At
higher frequencies `Gamma(1+i tau)` is exponentially small, so those rows use
the exact closed form rather than treating double-precision noise as evidence.

This proves mode-wise injectivity after combining two incommensurate ratios.
It does not prove a uniform lower frame bound for arbitrary superpositions,
does not control the zeta explicit formula on a dense Weil test core, and does
not establish Weil positivity. The constant mode remains invisible.

## 2. Collatz conjecture

### Proposition CO-227

Let `U=(1,1,3)`, whose accelerated affine data are `(A,C,B)=(27,32,19)`.
Let a fixed suffix `V` have data `(A_V,C_V,B_V)`. For

```text
w_r = U^r V,  r>=1,
```

the cycle denominator and intercept are

```text
D_r = C_V 32^r-A_V 27^r,
B_r = ((5B_V+19A_V)32^r-19A_V 27^r)/5.                    (CO-227.1)
```

Put `t=(27/32)^r`. If `D_r>0` and the values of `B_r/D_r` at `r=1` and
`r=infinity` lie strictly inside the same unit interval `(m,m+1)`, then
`D_r` does not divide `B_r` for every `r>=1`.

For `V=(4,2,1)`,

```text
B_1/D_1 = 4385/3367,
lim_(r->infinity) B_r/D_r = 559/320,
```

both in `(1,2)`. Thus every `(1,1,3)^r,(4,2,1)` is a primitive noncycle.

### Proof

Affine composition and the geometric sum for `U^r` yield `(CO-227.1)`.
After dividing numerator and denominator by `32^r`, the ratio is a
fractional-linear function of `t`. It has no pole on
`0<=t<=27/32`, so it is monotone or constant and remains between its two
endpoint values. In the selected family this proves

```text
1 < B_r/D_r < 2.
```

If `D_r|B_r`, the ratio would be an integer, which is impossible in that
open interval. The symbol `4` occurs exactly once, so the word cannot be a
nontrivial repetition and is primitive.

### Computation and limit

An exact rational search over suffix lengths at most `4` and exponents
`1,...,6` found `1,425` endpoint certificates. This search discovered
candidates; it is not the proof of the selected family. Direct affine
composition was also checked for `r=1,...,40` and agrees with the all-`r`
formula.

The criterion does not cover suffixes whose endpoint ratios cross an integer,
does not exclude `D|B` for every primitive valuation word, and says nothing
about descent of aperiodic natural-number orbits.

## 3. Strong Goldbach conjecture

### Proposition GB-227

Let `z=ceil(X^(1/3))`. Every retained composite `m<=X` with no prime factor
at most `z` has a unique representation

```text
m=qr,  z<q<=r,  q and r prime.                              (GB-227.1)
```

Consequently the `PS` channel for an even target `N` is exactly

```text
sum_(z<q<=sqrt(N)) sum_(q<=r, qr<=N-2)
  1_prime(N-qr),                                            (GB-227.2)
```

with the analogous formula for `SP`; `SS` is the corresponding two-cell
factor convolution. If `q|N` in `(GB-227.2)`, a prime `N-qr` must equal `q`,
so only `r=N/q-1` can contribute.

### Proof

Three factors greater than `z` have product greater than `z^3>=X`.
Thus a retained composite below `X` has exactly two prime factors, and ordering
them proves uniqueness. Substitution gives the factor lifts. If `q|N`, then
`q|(N-qr)`; a positive prime divisible by `q` is `q` itself, proving the
exception formula.

### Computation and limit

At `N=10^4,10^5,10^6`, exact least-factor bins reproduce all TICKET-226
`PS`, `SP`, and `SS` totals and the full rough decomposition. The stored
four-bin matrices are a machine-readable target for future bilinear estimates.

This is an exact localization, not a lower bound for `PP`. The unresolved
step is a uniform estimate for primes `N-qr` in moving nonzero residue classes
for every even target. One-variable PNT or marginal semiprime density does not
supply that estimate.

## 4. Twin Prime conjecture

### Proposition TP-227

Under the same cutoff, the shifted error channels are exactly

```text
PS: qr-2 is prime,
SP: qr+2 is prime,
SS: pq+2=rs,
```

where every displayed factor exceeds `z`. In each `SS` term,

```text
{p,q} intersection {r,s} = empty.                           (TP-227.1)
```

### Proof

The unique factor representation `(GB-227.1)` gives the three equations by
substitution. If an odd prime factor occurred on both sides of an `SS` term,
it would divide both `n=pq` and `n+2=rs`, hence divide `2`, a contradiction.

### Computation and limit

Exact factor-cell tables at `X=10^4,10^5,10^6` reproduce the TICKET-226
channel totals. Every enumerated `SS` term has disjoint factor sets. These
finite identities do not prove cancellation, a power saving, or infinitely
many `PP` terms. The next lemma must uniformly estimate the shifted
`qr-2` and `qr+2` prime sums across all cube-root factor cells.

## Literature and priority boundary

- Connes and Consani, [Weil positivity and Trace formula, the archimedean place](https://arxiv.org/abs/2006.13771), provides the Weil-positivity context. RH-227 is not a positivity theorem.
- Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562), proves an almost-all theorem, not every-orbit descent.
- Helfgott, [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438), is primary circle-method context and does not prove binary Goldbach.
- Ford and Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368), explains why substantial Type-I and Type-II information matters for prime lower bounds.
- The Polymath project, [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897), is a primary bounded-gap reference and does not prove gap exactly two.

Buchstab decomposition, Mellin-Laplace transforms, and affine Collatz word
composition are classical tools. PrimeProject claims no literature priority
for those ingredients. Its contribution here is the explicit integration of
the four exact lemmas into a falsifiable proof ledger with reproducible
factor-cell and alias audits.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket227_mellin_block_buchstab_lifts.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket227_mellin_block_buchstab_lifts -v
```

Machine-readable artifacts:

- `data/open-problem/ticket227-mellin-block-buchstab-lifts.json`
- `data/open-problem/riemann/rh-ticket-227-dual-dilation-mellin.json`
- `data/open-problem/collatz/co-ticket-227-block-suffix-interval.json`
- `data/open-problem/goldbach/gb-ticket-227-buchstab-factor-lift.json`
- `data/open-problem/twin-prime/tp-ticket-227-shift-two-factor-lift.json`
