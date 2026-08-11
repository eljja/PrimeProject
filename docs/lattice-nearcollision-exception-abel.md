# TICKET-215: Lattice Certificates, Power Near-Collisions, Exception Counts, and Abel Boundaries

## Abstract

TICKET-215 continues the four-conjecture program from TICKET-214. It does not
prove or disprove the Riemann Hypothesis, the Collatz Conjecture, the Strong
Goldbach Conjecture, or the Twin Prime Conjecture. It proves four narrower
results that turn the previous infinite gaps into more explicit quantitative
targets.

1. The RH defect can be certified by intersecting a rigorous interval with the
   nonnegative even lattice. A cofinal upper endpoint strictly below two would
   prove RH; interval width alone cannot.
2. Every Collatz cycle word cyclically equal to `1^k 2^m` forces one sharply
   constrained exponential near-collision. There is at most one candidate `m`
   per `k`, and none occurs for `1<=k<=4096`.
3. The Goldbach exponential selector recovers the exact number of exceptions
   in a finite block by an integer floor. The universal temperature threshold
   is sharp.
4. The exact gap-two channel has an Abel transform whose divergence at radius
   one is equivalent to Twin Prime infinitude. Any finite set of radii bounded
   away from one is logically insufficient.

All parent problems remain `open_not_proven`; the resolution count is zero.

## Result ledger

| Problem | Exact TICKET-215 result | Route discarded | Remaining gap | Next lemma |
|---|---|---|---|---|
| Riemann | `EvenLatticeOneSidedCofinalCertificationAndSharpTwoBarrier` | interval width or relative precision without a one-sided bound below two | actual-zeta cofinal defect upper bounds | `CofinalActualZetaDefectUpperBoundStrictlyBelowTwo` |
| Collatz | `SingleMountainCycleNearCollisionReductionAndFiniteDiagonalAudit` | finite single-mountain diagonal audit as a complete proof | all `k`, multi-run words, valuations above two, divergence | `NoSingleMountainPowerNearCollisionForAllK` |
| Goldbach | `ExponentialSelectorExactExceptionCountAndSharpTemperature` | selector floor identity as an independent coverage proof | arithmetic subunit bound on every block | `ArithmeticExactExceptionSelectorBelowOneOnEveryDyadicBlock` |
| Twin Prime | `CardinalSelectedAbelBoundaryEquivalenceAndFiniteRadiusNoGo` | fixed-radius or finite-radius evidence | parity-breaking divergence near radius one | `ParityBreakingLowerBoundForCardinalSelectedAbelTransformNearOne` |

## 1. Riemann: a sharp even-lattice certificate

At a boundary-free height, let

```text
D(T) = N(T) - M(T),
```

where `N` is the total upper-half strip multiplicity and `M` is the
critical-line multiplicity. TICKET-213 proved

```text
D(T) in 2 Z_{>=0}.
```

Suppose a rigorous calculation returns an interval `I(T)=[L,U]` containing
`D(T)`. The possible defects are exactly

```text
I(T) intersect 2 Z_{>=0}.
```

### Theorem RH-TICKET-215

If `U<2`, then `D(T)=0`. If this happens at an unbounded sequence of
boundary-free heights, RH follows from the monotonic cofinal equivalence in
TICKET-214.

The threshold is sharp. A logical symmetric zero model with one persistent
off-line pair has `D(T)=2`; even the exact width-zero interval `[2,2]` does not
certify RH. Thus precision, interval width, and relative error are not the
missing currency. The needed estimate is one-sided and strictly below two.

The interval fixtures test zero-only, positive-only, and ambiguous lattice
intersections with exact rational endpoints. They are theorem tests, not zeta
zero computations.

### Remaining gap

```text
CofinalActualZetaDefectUpperBoundStrictlyBelowTwo
```

Platt and Trudgian rigorously verified RH to height `3*10^12` using interval
arithmetic. That is an important finite certificate, not the cofinal bound
required here: [The Riemann hypothesis is true up to 3*10^12](https://arxiv.org/abs/2004.09765).

## 2. Collatz: a single-mountain power near-collision

Write `T_a(x)=(3x+1)/2^a`. Consider a positive cycle whose cyclic valuation
word is

```text
1^k 2^m,  k,m>=1.
```

Direct affine iteration gives

```text
T_1^k(x) = [3^k x + (3^k-2^k)] / 2^k,
T_2^m(y) = [3^m y + (4^m-3^m)] / 4^m.
```

Set

```text
Delta(k,m) = 2^(k+2m) - 3^(k+m).
```

The fixed-point equation becomes

```text
Delta x = Delta + 2*3^m*(3^k-2^k).
```

### Theorem CO-TICKET-215

Positive integer closure forces

```text
0 < Delta(k,m) <= 3^k - 2^k.
```

Indeed, `Delta` is odd and coprime to three, so divisibility of the right-hand
remainder forces `Delta | (3^k-2^k)`. Moreover,

```text
Delta(k,m+1) = 3 Delta(k,m) + 2^(k+2m) > 3^k
```

after the first positive `Delta`. Therefore each `k` has at most one possible
`m`: the first one where the two powers cross.

The exact audit checks this unique diagonal through `k=4096`. It finds zero
near-collisions. The transcript hash is

```text
7e480e162ad783a841d71778b6a916460ab5d3414d229d0b2cf1120b4d69d5d8
```

This excludes every `1^k2^m` cycle in the audited range, but not all `k`,
multi-run words, valuations above two, or divergent trajectories.

### Remaining gap

```text
NoSingleMountainPowerNearCollisionForAllK
```

Hercher's stronger cycle literature uses different parameters such as local
minima and verified starting ranges. TICKET-215 does not reproduce or improve
those published bounds: [There are no Collatz m-cycles with m<=91](https://arxiv.org/abs/2201.00406).

## 3. Goldbach: exact exception counting

For a block of `B` even targets, let `A_i` be the unordered Goldbach
representation counts, and let

```text
E_B(q) = sum_i q^(A_i),
Z_B    = #{i : A_i=0},
0<q<1.
```

### Theorem GB-TICKET-215

```text
Z_B <= E_B(q) <= Z_B + (B-Z_B)q.
```

Every zero count contributes one; every positive integer count contributes at
most `q`. Hence

```text
Bq < 1  implies  floor(E_B(q)) = Z_B.
```

The condition is universally sharp. At `Bq=1`, the all-one count vector has
`Z_B=0` but `E_B=1`, so the subunit test fails despite complete coverage.

The exact prime audit on dyadic starts `128, 512, 2048, 8192, 32768` finds no
exceptions. The minimum representation counts are respectively
`3, 10, 25, 75, 223`. These finite rows validate the implementation, not an
all-block estimate.

### Remaining gap

```text
ArithmeticExactExceptionSelectorBelowOneOnEveryDyadicBlock
```

The published finite verification through `4*10^18` remains much larger than
the local audit, but still does not control every integer:
[Empirical verification of the even Goldbach conjecture](https://www.ams.org/mcom/2014-83-288/S0025-5718-2013-02787-1/).

## 4. Twin Prime: an Abel boundary target

Let

```text
a_n = 1 if n and n+2 are prime, and 0 otherwise,
F(r) = sum_(odd n>=3) a_n r^n,  0<r<1.
```

The cardinal-sine selector from TICKET-214 shows that `a_n` is the exact
gap-two channel, not a bounded-gap surrogate.

### Theorem TP-TICKET-215

The Twin Prime Conjecture is equivalent to

```text
F(r) -> infinity as r -> 1 from below.
```

If only finitely many twins exist, the boundary limit is their finite count.
If infinitely many exist, the first `K` terms tend to one for every `K`, so
monotone convergence forces divergence.

This does not make fixed-radius data decisive. For each fixed `r<1`,

```text
F(r) <= r^3/(1-r^2).
```

For finitely many sampled radii with maximum `r_*<1`, append an infinite odd
support beginning at a sufficiently large odd `N`. Its total contribution is

```text
r_*^N/(1-r_*^2).
```

It can be smaller than any prescribed error. The exact fixture uses radii
`1/2, 2/3, 3/4, 9/10`, error `1/1000`, and `N=83`. This is a logical support
countermodel, not an infinite prime-pair construction.

The finite prime audit through `10^6` gives cumulative twin counts
`8, 35, 205, 1224, 8169` and checks the scheduled Abel bounds at
`r_X=1-1/X`.

### Remaining gap

```text
ParityBreakingLowerBoundForCardinalSelectedAbelTransformNearOne
```

Ford and Maynard's general sieve framework explains why substantial Type II
information is needed for nontrivial prime lower bounds. The Abel identity
does not supply that missing parity-breaking input:
[On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).

## Cross-problem conclusion

TICKET-215 replaces four vague infinite requirements by four boundary
inequalities:

```text
RH:        certified defect upper endpoint < 2 cofinally
Collatz:   no power near-collision on the unique single-mountain diagonal
Goldbach:  arithmetic exception-selector value < 1 on every block
Twin:      parity-breaking Abel lower bound -> infinity as r -> 1
```

None of these inequalities is proved in the required all-scale form.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket215_lattice_nearcollision_exception_abel.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket215_lattice_nearcollision_exception_abel -v
```

Primary machine artifact:

```text
data/open-problem/ticket215-lattice-nearcollision-exception-abel.json
```

No literature-priority claim is made without independent expert review.
