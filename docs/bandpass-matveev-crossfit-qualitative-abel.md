# TICKET-219: Band-pass defects, Matveev closure, cross-fitted moments, and qualitative Abel growth

Korean edition: [bandpass-matveev-crossfit-qualitative-abel.ko.md](bandpass-matveev-crossfit-qualitative-abel.ko.md)

## Claim status

TICKET-219 does **not** prove or disprove the Riemann Hypothesis, the Collatz
Conjecture, the Strong Goldbach Conjecture, or the Twin Prime Conjecture. It
proves four narrower statements. One infinite Collatz word family is closed;
the other three tracks improve the logical or experimental interface and state
the remaining theorem explicitly.

| Problem | New exact result | Status | Next single lemma |
|---|---|---|---|
| Riemann | `PositiveDyadicBandpassDefectCertificateAndEquivalenceAudit` | parent open | `PrimeSideDyadicBandpassDefectEnclosureBelowKernelFloor` |
| Collatz | `ExplicitMatveevClosureOfAllPositiveSingleMountainCycles` | one infinite word family closed; parent open | `EffectiveBakerSeparationForAllPositiveCycleValuationWords` |
| Goldbach | `LeakageFreeCrossFittedEighthMomentSupportCertificate` | ten finite held-out folds certified; parent open | `CofinalCrossFittedGoldbachEighthMomentBelowFoldwiseZeroBarrier` |
| Twin Prime | `QualitativeAbelInfinitudeEquivalenceAndDensityScaleNoGo` | parent open | `UnboundedParityCorrectedTwinAbelTransform` |

## 1. Riemann: a positive dyadic band-pass certificate

Let `C` be the locally finite nonnegative integer-valued off-critical defect
measure used by TICKET-217 and TICKET-218, and put

```text
L(s) = integral exp(-s t) dC(t),
W(H) = L(1/H) - L(2/H).
```

Then

```text
W(H) = integral exp(-t/H)(1-exp(-t/H)) dC(t).
```

On the closed band `H <= t <= 2H`, the positive kernel is at least

```text
c = exp(-2)(1-exp(-2)).
```

Therefore

```text
C([H,2H]) <= floor(W(H)/c),
W(H) < c  =>  C([H,2H]) = 0.
```

### Proof

For `x=t/H` in `[1,2]`, `f(x)=exp(-x)(1-exp(-x))` has derivative
`exp(-x)(2exp(-x)-1)<0`. Its minimum on the band is therefore `f(2)=c`.
Integrating this pointwise lower bound and using integrality proves the count
certificate. Dyadic bands cover every height above a finite base cutoff.

### What changed

The transform difference suppresses both very low and very high defects and is
better localized than the single-radius statistic of TICKET-218. It is also an
honest strength audit: finite verification below `H0` plus `W(2^j H0)<c` for
every `j` is equivalent to `C=0` in this model. Calling the missing inequality
an “envelope” does not make it weaker than RH.

The next non-circular task is a rigorous prime-side explicit-formula interval
enclosure of the actual transform difference. The synthetic replay only checks
the proved counting inequality; it contains no zeta-zero evidence.

## 2. Collatz: closing every positive single-mountain cycle

TICKET-217 proves that a positive accelerated Collatz cycle with valuation word
`1^k 2^m` yields, after reducing `(m,k)=g(p,q)`, an upper convergent `p/q` of

```text
alpha = log(3/2) / log(4/3)
```

and must satisfy

```text
0 < Lambda = (4/3)^p (3/2)^(-q) - 1 < 3^(-p).
```

For the positive rationals `4/3` and `3/2`, the project uses the conservative
Matveev specialization

```text
log Lambda > -K(1+log(2p)),
K = 1.4 * 30^5 * 2^4.5 * log(4) * log(3).
```

Exact rational logarithm intervals certify that the first integer satisfying

```text
p log 3 > K(1+log(2p))
```

is

```text
p0 = 27,456,680,737.
```

The certified margin at `p0` is positive, the margin at `p0-1` is negative,
and the derivative lower bound is positive thereafter. Thus every `p>=p0`
contradicts the necessary inequality `Lambda<3^(-p)`.

TICKET-218 independently excludes the first 49 upper convergents. The next
upper numerator is

```text
16,672,027,258,049,147,969,018,986,102,532,625,254,200,541,727,292,
```

far above `p0`. Numerators of continued-fraction convergents increase, so the
finite prefix and Matveev tail meet without a gap.

**Partial theorem.** No positive accelerated Collatz cycle has valuation word
`1^k 2^m`.

This is a complete theorem for one infinite family, not the Collatz Conjecture.
General cyclic valuation words have multiple runs, and nonperiodic divergence
is not a cycle. The next lemma must retain phase information while extending
the Baker separation to every positive cyclic valuation word.

The explicit lower bound follows Matveev's published rational-logarithm bound:
E. M. Matveev, “An explicit lower bound for a homogeneous rational linear form
in the logarithms of algebraic numbers. II,” *Izvestiya: Mathematics* 64
(2000), 1217-1269, https://doi.org/10.1070/im2000v064n06ABEH000314.

## 3. Goldbach: held-out eighth-moment support

Let a finite index set be partitioned into folds. For each held-out fold `F`,
fit a positive model

```text
M_i = (P_F/Q_F) w_i
```

using only coordinates outside `F`. If

```text
sum_{i in F} |A_i Q_F - P_F w_i|^p
  < (P_F min_{i in F} w_i)^p,
```

then every `A_i` in `F` is positive. A zero coordinate would contribute at
least the entire right-hand side by itself. Certifying every fold certifies the
full vector.

The exact replay uses two parity folds on each of five dyadic blocks
`[X,2X)`, with `X=128,512,2048,8192,32768`. The integer model shape is

```text
round(10^6 n product_{odd p|n}(p-1)/(p-2)).
```

All ten held-out folds pass at `p=8`; only one passes at `p=4`. Training and
test indices are disjoint in every fold. This improves TICKET-218 by preventing
the held-out coordinate from influencing its model scale.

It remains a finite certificate because the residuals are computed from the
actual held-out Goldbach counts. The missing theorem is a cofinal arithmetic
eighth-moment bound that does not enumerate those counts.

## 4. Twin Prime: remove an overstrong density premise

For any binary sequence, define

```text
F(r) = sum_n a_n r^n.
```

The support is infinite if and only if `F(r)` is unbounded as `r` tends to one
from below. Finite support bounds `F` by the support size. Conversely, any `K`
supported terms have a finite partial sum tending to `K` as `r` tends to one.

For the twin-prime indicator this gives the exact qualitative equivalence

```text
infinitely many twin primes
  iff the actual twin Abel transform is unbounded.
```

The TICKET-218 condition

```text
liminf F(1-1/X)/(X/log^2 X) > 1/2
```

is a useful sufficient quantitative theorem, but it is not necessary for
abstract infinitude. The infinite odd support `n_j=2^j+1` satisfies
`F(1-1/X)=O(log X)`, hence its normalized liminf is zero. This countermodel is
not a prime model and makes no claim against the Hardy-Littlewood prediction.

A finite lower certificate remains available:

```text
F(1-1/X) >= T(X)/4,  X>=2,
```

because every supported `n<=X` contributes at least
`(1-1/X)^X>=1/4`. The next useful target is qualitative unboundedness of a
parity-corrected actual twin transform, not an assumed density-scale constant.

## Reproduce

```powershell
D:\python\anaconda3\python.exe scripts\ticket219_bandpass_matveev_crossfit_qualitative_abel.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket219_bandpass_matveev_crossfit_qualitative_abel
```

Machine-readable outputs:

- `data/open-problem/ticket219-bandpass-matveev-crossfit-qualitative-abel.json`
- `data/open-problem/riemann/rh-ticket-219-dyadic-bandpass.json`
- `data/open-problem/collatz/co-ticket-219-matveev-single-mountain.json`
- `data/open-problem/goldbach/gb-ticket-219-cross-fitted-eighth-moment.json`
- `data/open-problem/twin-prime/tp-ticket-219-qualitative-abel.json`
