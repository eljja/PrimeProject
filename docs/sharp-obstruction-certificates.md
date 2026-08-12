# TICKET-221: Sharp obstruction certificates for four open problems

## Claim status

**The Riemann hypothesis, Collatz conjecture, strong Goldbach conjecture,
and Twin Prime conjecture all remain open.** TICKET-221 supplies neither a
proof nor a counterexample to a parent conjecture. It instead proves that
four formulations left open by TICKET-220 omit information that a successful
bridge must retain.

The machine-readable status is `open_not_proven`; parent-conjecture resolution
count is zero.

## Research question

TICKET-220 left four targets:

1. a prime-side summable dyadic envelope of total mass below one for RH;
2. effective Baker separation for primitive multi-run Collatz words;
3. a representation-free cofinal Goldbach cross-fit margin;
4. a parity-sensitive lower bound beyond every fixed Twin wheel.

TICKET-221 asks whether each target, as currently phrased, preserves enough
information. In all four cases an additional coupling variable is necessary.

---

## 1. Riemann hypothesis

### Declared proposition

`ScaleUniformDyadicEnvelopeDivergenceNoGo`

For `H>0`, `j in Z`, and `t>0`, put

```text
K_j(t;H) = exp(-2^(-j)t/H) - exp(-2^(1-j)t/H).
```

Then `sup_(t>0) K_j(t;H)=1/4` for every `j`. Any coordinatewise envelope
`U_j` dominating every possible one-atom positive defect therefore satisfies
`U_j>=1/4` at every scale, and `sum_j U_j` diverges.

### Proof

With `x=2^(-j)t/H`, the kernel becomes `k(x)=e^(-x)-e^(-2x)`. Its derivative
vanishes only at `x=log 2`, its endpoint limits are zero, and
`k(log 2)=1/4`. At scale `j`, place one atom at `t=H 2^j log 2`; this forces
`U_j>=1/4`. Infinitely many coordinates force divergence.

### Reproducible calculation

- 100-digit Decimal arithmetic checks the maximum and stationary point for
  all `j=-12,...,12`.
- The universal-envelope lower bound over `[-R,R]` is exactly `(2R+1)/4`.
- Exact rational rows record `R=1,2,4,8,16,32`.

### Discarded route

Applying the same arithmetic-free worst-case bound independently at every
scale and attempting to sum it below one.

### Remaining gap

The theorem does not exclude an envelope coupled through the actual prime
explicit formula, signed cancellation, Weil positivity, or Li positivity.

**Next lemma:** `ArithmeticCoupledDyadicTailBudgetBelowOne`.

---

## 2. Collatz conjecture

### Declared proposition

`OrderBlindLogarithmicSeparationNoGoForPrimitiveWords`

For an accelerated valuation word `a=(a_1,...,a_h)`, one turn is

```text
(3^h n+B(a))/2^S,
S=sum_i a_i,
B(a)=sum_i 3^(h-i)2^(a_1+...+a_(i-1)).
```

Permutation preserves `h`, `S`, the slope, and the Baker form
`S log 2-h log 3`, but not `B`. Swapping adjacent unequal values `x,y` after
prefix sum `s` changes `B` by exactly

```text
3^(h-i-1)2^s(2^x-2^y).
```

The cyclically inequivalent primitive multi-run words `(1,2,3,4)` and
`(3,4,2,1)` share `h=4,S=10,A=81,D=1024,D-A=943`, but have intercepts 133
and 995. Their rational fixed points are `133/943<1` and `995/943>1`.

### Proof

The intercept formula follows by induction through `n -> (3n+1)/2^a`.
After an adjacent swap, all later prefix sums agree; subtraction leaves the
displayed local term. Direct substitution gives the two witnesses. Scalar
Baker data therefore cannot even locate the rational fixed point relative to
one, much less decide divisibility and exact valuation admissibility.

### Reproducible calculation

- Every distinct permutation of four valuation multisets is enumerated.
- Slope invariance, intercept diversity, and every unequal adjacent-swap
  identity are checked with integers.
- The witness denominator and fixed points are stored as exact fractions.

### Discarded route

Using a bound for `|S log 2-h log 3|` alone as a complete primitive-word
cycle criterion.

### Remaining gap

One must combine logarithmic separation with ordered intercept divisibility,
exact 2-adic admissibility, or a global descent theorem. Divergent aperiodic
orbits remain untouched.

**Next lemma:**
`OrderSensitiveDivisibilityOrDescentForPrimitiveValuationWords`.

---

## 3. Strong Goldbach conjecture

### Declared proposition

`SharpLpDistanceToGoldbachZeroSet`

Let `m` have strictly positive coordinates and let `Z` be the nonnegative
vectors with at least one zero coordinate. For every `1<=p<=infinity`,

```text
dist_p(m,Z)=min_i m_i.
```

Thus `||r-m||_p<min_i m_i` guarantees pointwise positivity, and the strict
constant is optimal.

### Proof

If `z_k=0`, then `||z-m||_p>=m_k>=min_i m_i`. Equality is attained by setting
only a minimum coordinate to zero. Appending a new positive model coordinate
and observed zero preserves every old finite-prefix certificate but lands on
the new zero barrier exactly.

### Reproducible calculation

- Twelve exact rational witnesses cover three models and `p=1,2,4,8`.
- Prefix lengths `4,8,16,32,64` are extended by one adversarial zero.
- TICKET-220's `150/150` eighth-moment folds and `140/140` refinement bridges
  are recomputed; their worst ratio remains about `0.9670275612`.

### Discarded route

Promoting finite cross-fit success, higher moment order, or finite partition
refinement to cofinal positivity without a uniform margin theorem.

### Remaining gap

Prime distribution must yield a strict residual ratio below one on every
sufficiently large block. Circle-method and transference routes remain open.

**Next lemma:** `UniformCofinalLpMarginBelowOneFromPrimeDistribution`.

---

## 4. Twin Prime conjecture

### Declared proposition

`LowDegreeBooleanParityOrthogonalityNoGo`

On the uniform cube `{-1,1}^m`, let `P(x)=product_i x_i`. For every proper
subset `S`,

```text
E[P(x) product_(i in S)x_i]=0,
```

whereas the full-degree correlation is one. Every polynomial of Walsh degree
below `m` is therefore orthogonal to parity.

### Proof

Choose a coordinate outside `S` and pair every point with the point obtained
by flipping that coordinate. The `S` monomial is unchanged and parity changes
sign. Full-degree correlation is `P(x)^2=1`.

### Reproducible calculation

- Every cube point is enumerated for `m=2,...,12`.
- All `2^m-1` proper Walsh monomials are checked at each dimension.
- Every low-degree integer correlation sum is zero; the full-degree sum is
  exactly `2^m`.

### Discarded route

Claiming parity detection from a local sieve observable whose selected-prime
interaction expansion contains only proper low-degree terms.

### Remaining gap

Actual arithmetic requires parity-breaking Type II information or a positive
shifted von Mangoldt correlation. The theorem does not classify Maynard
weights or all bilinear forms as low degree.

**Next lemma:** `VonMangoldtPairLowerBoundWithParityBreakingTypeIIInput`.

---

## Literature boundary

Li positivity, Baker logarithmic forms, Collatz cycle bounds, Goldbach
exceptional-set estimates, the sieve parity problem, and Maynard's bounded-gap
method define the external boundary. The four TICKET-221 theorems are project
obstruction or sharpness statements; no literature-priority claim is made.

- [Li, The Positivity of a Sequence of Numbers and the Riemann Hypothesis](https://doi.org/10.1006/jnth.1997.2137)
- [Baker, Linear forms in the logarithms of algebraic numbers](https://doi.org/10.1112/S0025579300003971)
- [Simons, On the (non-)existence of m-cycles for generalized Syracuse sequences](https://eudml.org/doc/278414)
- [Grimmelt and Bhowmik, The exceptional set of the Goldbach problem](https://arxiv.org/abs/2607.27282)
- [Heath-Brown, A parity problem from sieve theory](https://doi.org/10.1112/S0025579300012109)
- [Maynard, Small gaps between primes](https://arxiv.org/abs/1311.4600)

## Conclusion

| Problem | New exact result | Discarded route | Next single lemma |
|---|---|---|---|
| Riemann | universal per-scale envelope is at least `1/4` and diverges | summing independent worst-case bounds below one | `ArithmeticCoupledDyadicTailBudgetBelowOne` |
| Collatz | cyclically inequivalent words with identical Baker data can place fixed points on opposite sides of one | scalar separation alone closes primitive words | `OrderSensitiveDivisibilityOrDescentForPrimitiveValuationWords` |
| Goldbach | exact `L^p` distance to the zero set is the minimum model coordinate | finite moment success implies cofinal positivity | `UniformCofinalLpMarginBelowOneFromPrimeDistribution` |
| Twin Prime | every proper Walsh-degree observable is parity-orthogonal | low-degree local sieve detects parity | `VonMangoldtPairLowerBoundWithParityBreakingTypeIIInput` |

Primary machine-readable audit:

`data/open-problem/ticket221-sharp-obstruction-certificates.json`
