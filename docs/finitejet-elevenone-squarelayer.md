# TICKET-195: Finite-Jet Boundaries, Fixed-Stratum Decidability, and Prime-Square Layers

## 1. Claim boundary

TICKET-195 proves four intermediate theorems. It proves none of the Riemann
Hypothesis, Collatz conjecture, strong Goldbach conjecture, or Twin Prime
conjecture, and it finds no counterexample to a parent conjecture. The newly
closed infinite family is the accelerated Collatz valuation stratum with
exactly eleven entries equal to one and every other entry equal to two.

| Problem | Exact result proved here | Route discarded | Next single lemma |
|---|---|---|---|
| Riemann | `FiniteEvenJetAmbiguityAndRoucheTailBridge` | finite Xi/Jensen data without a uniform tail class | `XiTaylorSectionsAdmitCertifiedRoucheTailBoundsOnAnExhaustingOffRealDomainFamily` |
| Collatz | `FixedOneCountRestTwoDecidabilityAndElevenStratumExclusion` | the eleven-one stratum and the claim that each fixed stratum requires an infinite search | `NoPositiveAcceleratedCollatzCycleHasAllValuationsInTheSetOneTwo` |
| Goldbach | `PrimeSquareDominantThetaLayerDecomposition` | deleting exponent-at-least-three support | `BinaryCorrelationExceedsPrimeSquareLayerPlusCubicTailEnvelopeForEveryLargeEvenTarget` |
| Twin Prime | `PrimeSquareDominantIntervalThetaLayerDecomposition` | treating square support as the complete local contamination set | `ShiftTwoCorrelationExceedsPrimeSquareLayerPlusCubicTailEnvelopeOnInfinitelyManyDyadicBlocks` |

Reproduce with:

```powershell
D:\python\anaconda3\python.exe scripts\ticket195_finitejet_elevenone_squarelayer.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket195_finitejet_elevenone_squarelayer -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

The integrated result is
`data/open-problem/ticket195-finitejet-elevenone-squarelayer.json`. All four
attempts remain `open_not_proven`; the resolution count is `0 / 4`.

## 2. Riemann Hypothesis

### 2.1 Selected open target

TICKET-194 left the actual pole-neutral Weil uniform bound and dense-core
convergence open. A possible alternative is to use finite Taylor or Jensen
data for the even real entire function

```text
Xi(t)=xi(1/2+it).
```

RH is equivalent to all zeros of `Xi(t)` being real. The question is whether a
growing collection of finite even Taylor data can be promoted without a
separate tail theorem.

### 2.2 Finite-even-jet ambiguity theorem

Let

```text
J_m(z)=sum_(r=0)^m a_r z^(2r),  a_r in R.
```

Since `J_m(i)=sum a_r(-1)^r` is real, set

```text
c=(-1)^m J_m(i),
P_m(z)=J_m(z)+c z^(2m+2).
```

Then `P_m` has exactly the same declared coefficients through degree `2m`, but

```text
P_m(i)=J_m(i)+(-1)^m J_m(i)(-1)^(m+1)=0.
```

Evenness gives `P_m(-i)=0`. Thus every finite real even jet is compatible with
an even real polynomial having nonreal zeros. This is an exact no-go theorem:
finite Xi coefficients, finite Jensen polynomials, or finite Hankel checks do
not by themselves certify the all-zero statement.

The computation uses the rational sample jets

```text
a_r=(-1)^r/(r+1),  m=0,...,12,
```

and verifies `P_m(i)=0` with exact fractions in every row. These synthetic jets
illustrate the general algebraic theorem; they are not claimed to be Xi
coefficients.

### 2.3 Positive Rouché bridge

For a bounded domain with contour `Gamma`, write an actual entire function as
`F=P+R`. If

```text
sup_Gamma |R| < inf_Gamma |P|,
```

Rouché's theorem gives the same interior zero count for `F` and `P`. The
machine rows use `P=1` and
`R=2^(-(m+1))z^(2m+2)` on the unit circle and verify a strict rational margin.
This demonstrates a sound bounded-domain certificate.

### 2.4 Remaining gap

No such tail inequality is proved for actual Xi Taylor sections on an
exhausting family of off-real domains. The finite-jet ambiguity theorem does
not locate a nonreal Xi zero. Rouché's theorem is classical and no literature
novelty is claimed for it; the project contribution is the exact route audit
and machine contract.

## 3. Collatz conjecture

### 3.1 Fixed-stratum decidability theorem

Fix `r>=1`. Consider accelerated valuation words containing exactly `r` ones
and otherwise only twos. For a word of length `h`, the affine denominator is

```text
D_(r,h)=2^(2h-r)-3^h.
```

Nonpositive `D_(r,h)` removes an initial set of horizons. Every state in a
nontrivial positive odd cycle is at least three, so multiplying step ratios
gives

```text
1 <= 2^r(5/6)^h.
```

For fixed `r` the right side tends to zero, removing every sufficiently large
`h`. Only finitely many horizons and finitely many normalized words remain.
Exact affine divisibility therefore decides each fixed stratum in finite time.

This is a quantifier theorem, not a Collatz proof: it states
`for every fixed r, there is a finite decision`, not `one finite certificate
decides every r`.

### 3.2 Exact eleven-one exclusion

For `r=11`:

- `h<=26` is noncontracting;
- `h=27,...,41` is the finite exact range;
- `2048(5/6)^h<1` for every `h>=42`.

After rotating one valuation-one position to the start, there are ten boundary
terms. A 5+5 MITM audit represents exactly

```text
sum_(h=27)^41 C(h-1,10)
 = C(41,11)-C(26,11)
 = 3,151,735,808
```

normalized words. It evaluates 4,266,158 left tuples and 1,893,528 right
queries with exact integers. There are no affine divisibility hits. The
boundary formula is also checked directly against the original recurrence on
all normalized words through `h=17`.

### 3.3 Remaining gap

The next target is one uniform theorem excluding every `{1,2}` valuation word,
not an infinite sequence of fixed-`r` computations. Valuations at least three
and aperiodic divergent trajectories also remain open.

## 4. Strong Goldbach conjecture

### 4.1 Prime-square leading layer

TICKET-194 proved

```text
W_odd(Y)=sum_(k>=2) theta_odd(floor(Y^(1/k))).
```

Separating `k=2` gives the exact identity

```text
W_odd(Y)
 = theta_odd(floor(sqrt Y))
 + R_>=3(Y),

R_>=3(Y)=sum_(k>=3) theta_odd(floor(Y^(1/k))).
```

Using the classical Chebyshev estimate `theta(t)=O(t)`, the cubic layer is
`O(Y^(1/3))`. The `O(log Y)` remaining layers are each `O(Y^(1/4))`, and
`Y^(1/4)log Y=O(Y^(1/3))`. Therefore

```text
R_>=3(Y)=O(Y^(1/3)).
```

The sufficient Goldbach contamination envelope becomes

```text
2log(N) theta_odd(floor(sqrt N))
 + O(N^(1/3)log N)
 + C_2(N).
```

This identifies the prime-square leading contribution and a lower-order
higher-exponent tail.

### 4.2 No-go and finite audit

Higher layers cannot be deleted from an exact support argument:

```text
32=27+5=3^3+5.
```

The ordered pair contributes `log(3)log(5)` to proper-prime-power
contamination but is absent from square-only support. Exact theta-layer
splitting and direct prime-power enumeration agree for the twelve targets
`2^10,...,2^21`; every finite total correlation exceeds the full envelope.

### 4.3 Remaining gap

The sharpened hierarchy only reduces the right side. It supplies no pointwise
lower bound for every sufficiently large even target, which remains the entire
Goldbach proof gap.

## 5. Twin Prime conjecture

### 5.1 Interval square layer

Subtracting cumulative identities at interval endpoints gives an exact square
layer plus exponent-at-least-three remainder on every `[A,B)`. On the two
shifted dyadic intervals used by the Twin bridge, the higher-layer local mass
is `O(X^(1/3))`, so its contamination contribution is

```text
O(X^(1/3)log X).
```

The prime-square interval layer is the leading proper-prime-power term.

### 5.2 No-go and finite audit

Square-only support is not exact because the block `[16,32)` contains

```text
(27,29)=(3^3,29).
```

This is genuine shift-two prime-power contamination omitted by a square-only
support set. Exact left/right interval splitting agrees with direct enumeration
on all seventeen blocks `X=2^j`, `j=4,...,20`, and every finite correlation
exceeds the complete square-plus-higher-layer envelope.

### 5.3 Remaining gap

No lower bound above that full envelope is proved on infinitely many unbounded
blocks. The decomposition does not overcome the parity barrier and does not
prove exact gap two infinitely often.

## 6. Literature boundary checked on 2026-08-08

The status and scope statements were checked against authoritative or primary
sources:

- The [Clay Mathematics Institute RH page](https://www.claymath.org/millennium/riemann-hypothesis/)
  still lists RH as unsolved. Finite zero verification is not an infinite proof.
- Tao's [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)
  (arXiv v7, revised 2026-07-16) proves a logarithmic-density almost-all
  statement, not descent for every positive starting value and not the
  exclusion of every possible cycle.
- Oliveira e Silva, Herzog, and Pardi's
  [empirical verification of even Goldbach](https://doi.org/10.1090/S0025-5718-2013-02787-1)
  is a finite verification through `4*10^18`; it does not supply the universal
  correlation lower bound required here.
- Maynard's [Small gaps between primes](https://doi.org/10.4007/annals.2015.181.1.7)
  proves a bounded prime-gap result, not infinitely many gaps exactly equal to
  two.

The algebraic and combinatorial statements proved in TICKET-195 are presented
as project results. Rouché's theorem, the Chebyshev estimate, and the inherited
prime-power identities are classical or previously established inputs; no
literature novelty is claimed for them.

## 7. Synthesis

The four tracks expose one common obstruction. Finite jets require a uniform
tail class. Infinitely many fixed-`r` finite decisions require a theorem
uniform in `r`. Sharper sublinear contamination layers require pointwise or
infinitely-often correlation lower bounds. TICKET-195 makes these missing
quantifiers explicit and machine-checkable without claiming a conjecture
resolution.
