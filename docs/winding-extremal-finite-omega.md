# TICKET-205: Winding Certificates, Cycle Extrema, Finite Witnesses, and Omega Weights

## Claim status

All four parent conjectures remain `open_not_proven`. TICKET-205 proves three
exact reductions or no-go theorems and one exact finite Goldbach theorem. It
does not prove or disprove the Riemann, Collatz, strong Goldbach, or Twin Prime
conjecture.

The canonical machine-readable artifact is
[`ticket205-winding-extremal-finite-omega.json`](../data/open-problem/ticket205-winding-extremal-finite-omega.json).

| Problem | Exact TICKET-205 result | Discarded route | Decisive next lemma |
|---|---|---|---|
| Riemann | Segmentwise derivative bounds make a sampled polygon's winding equal the analytic contour winding | Winding inferred from finite contour values alone | `CompletedZetaCofinalZeroFreeContourWindingCertificate` |
| Collatz | A nontrivial positive cycle has valuation 1 at a minimum and valuation at least 2 at a maximum; all-`>=2` words give only the trivial cycle | Searching the all-`>=2` periodic stratum | `UniformNondivisibilityForPrimitiveMixedValuationNecklaces` |
| Goldbach | Every even integer through 10,000,000 has an explicit least-prime witness; the full witness stream has a reproducible SHA-256 | Promoting a finite prefix to the universal conjecture | `ExplicitBinaryGoldbachTailExceptionalCountStrictlyBelowOne` |
| Twin Prime | `W(n)=2-(3/2)Omega(n)` realizes the desired prime/semiprime signs, but its shift-two product has infinitely many composite false positives | Treating positive raw switching products as twin indicators | `UniformCompositeCompositeCancellationForOmegaSwitchingCorrelation` |

## 1. Riemann hypothesis

### Declared proposition

Let `Gamma` be a positively oriented rectifiable Jordan contour with an
absolutely continuous arclength parametrization. Let `f` be analytic on and
inside `Gamma`. Partition the contour into arcs `Gamma_j` of length `h_j`,
starting at `z_j`. Suppose

```text
|f(z_j)| >= m_j > 0,
|d(f o Gamma)/ds| <= M_j almost everywhere on Gamma_j,
M_j h_j < m_j.
```

Then the analytic image of each arc and the chord between its sampled endpoint
values are homotopic in `C\{0}`, relative to their endpoints. Consequently,

```text
wind(f(Gamma),0) = wind(sampled polygon,0).
```

The argument principle identifies this integer with the number of zeros of
`f` inside `Gamma`, counted with multiplicity.

### Proof

For every point `z` on `Gamma_j`, absolute continuity and the derivative bound
give

```text
|f(z)-f(z_j)| <= M_j h_j < m_j <= |f(z_j)|.
```

Thus the full image arc lies in an open disk centered at `f(z_j)` that excludes
zero. The endpoint and its chord lie in the same convex disk. Replacing the
arc by the chord therefore gives an endpoint-fixed, zero-avoiding homotopy.
Doing this on all arcs preserves winding.

### Exact regression and no-go

For `f(z)=z^3` on the unit circle, use 24 equally spaced samples. The contour
derivative has modulus 3 and each arc has length

```text
pi/12 <= 11/42.
```

Hence the image excursion is at most `11/14`, leaving zero-avoidance margin
`3/14`. Consecutive sampled values advance by `1/8` of a turn, so the sampled
polygon winds exactly three times and certifies the three interior zeros.

Regularity is indispensable. The functions `1` and `z^8` agree at all eighth
roots of unity but have winding numbers 0 and 8. No rule using only those
finite values can distinguish them.

### Remaining gap

PrimeProject has not constructed a cofinal family of completed-zeta contours
with certified nonvanishing and segmentwise derivative bounds. Finite-height
zero verification does not imply this cofinal theorem.

## 2. Collatz conjecture

### Declared proposition

For a positive accelerated cycle, write

```text
x_(i+1) = (3x_i+1)/2^a_i,
a_i = v_2(3x_i+1).
```

In every nontrivial cycle:

1. every occurrence of a minimum cycle value has outgoing valuation `1`;
2. every occurrence of a maximum cycle value has outgoing valuation at least
   `2`.

Therefore every nontrivial periodic valuation necklace contains both a `1`
and an entry at least `2`. Every positive integral cycle word with all
valuations at least `2` is a power of `(2)` and represents only the fixed
cycle `1`.

### Proof

Let `m` be a minimum and let its next value be `m'`. If its valuation `a` were
at least 2, then

```text
3m+1 = 2^a m' >= 4m,
```

so `m<=1`. Positivity and oddness force `m=1`; the same equation then forces
`a=2` and `m'=1`. Determinism makes the whole cycle trivial. Thus a nontrivial
minimum has `a=1`.

At a maximum `M`, valuation 1 would give

```text
M'=(3M+1)/2 > M,
```

which is impossible. Hence its valuation is at least 2.

TICKET-204 proved cyclic divisibility invariance. Thus if the affine
denominator `D>0` divides the affine numerator `B`, every cyclic state `B/D`
is a positive odd integer and the word is an exact accelerated cycle. The
extremal theorem then excludes every all-`>=2` word except all-2 repetitions.

### Reproducible audit and remaining gap

As a regression, the generator checks all 87,380 words of lengths 1 through 8
over `{2,3,4,5}`. Exactly eight words pass the divisibility test, one all-2
word at each length; no non-all-2 word passes. The universal exclusion comes
from the extremal proof, not from this finite enumeration.

The remaining periodic search space consists of primitive mixed necklaces.
The result says nothing about nonperiodic divergent trajectories.

## 3. Strong Goldbach conjecture

### Exact finite theorem

Every even integer `N` with

```text
4 <= N <= 10,000,000
```

has an explicit prime-pair representation. For each of the 4,999,999 targets,
the generator stores in a stream the least prime `p<=N/2` such that `N-p` is
prime. The stream is regenerated rather than committed in full; its stable
identifier is

```text
SHA-256 ed31375c2d840a190345e901dfaf52e322424d40d7b4afa33ec7977cf0b791dd
```

The largest least witness is `751`, first required at `N=3,807,404`. For the
last target,

```text
10,000,000 = 29 + 9,999,971.
```

The digest is a reproducibility identifier, not a substitute for rerunning
the witness checks.

### Finite-prefix no-go

For any finite verified bound `B`, two Boolean models can agree on every even
target through `B` and differ first at `B+2`. Therefore no finite prefix,
regardless of size, determines strong Goldbach's infinite tail.

### Remaining gap

TICKET-204 proved that an explicit tail exceptional count strictly below one
would close the conjecture. TICKET-205 moves the independently reproducible
finite boundary to ten million but proves no tail exceptional-set estimate and
no pointwise major/minor-arc dominance theorem.

## 4. Twin Prime conjecture

### Declared proposition

Let `Q(d)=1` when `d=p^k` is a prime power with `k>=1`, and zero otherwise.
Then

```text
Omega(n) = sum_(d|n) Q(d).
```

Consequently the factor-pair-free arithmetic weight

```text
W(n)=2-(3/2)Omega(n)
```

realizes the formal TICKET-204 signs:

```text
W(p)=1/2       for every prime p,
W(pq)=-1       for every semiprime pq, including p=q.
```

### Proof and parity no-go

If `n=product p^e`, its prime-power divisors associated with `p` are exactly
`p,p^2,...,p^e`; they contribute `e` to the divisor sum. Summing over primes
gives `Omega(n)`.

The sign realization does not isolate twin primes. For every integer `k>=2`,

```text
n=3+15k,       n+2=5+15k.
```

The first is a proper multiple of 3 and the second a proper multiple of 5, so
both are composite with `Omega>=2`. Both weights are negative and
`W(n)W(n+2)>0`. This supplies an infinite composite-composite false-positive
family for the raw product criterion.

### Remaining gap

TICKET-205 converts the exposed-factor kernel from TICKET-204 into an exact
function of `n`, but the weight is unbounded below as `Omega(n)` grows and its
correlation contains composite-composite mass. A useful theorem must cancel
that mass with a uniform remainder smaller than a positive prime-prime main
term. No such estimate is proved here.

## Reproduction

```bash
python scripts/ticket205_winding_extremal_finite_omega.py
python -m unittest tests.test_ticket205_winding_extremal_finite_omega
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Expected machine status:

```text
exact_partial_theorem_count = 4
refuted_or_limited_route_count = 4
conjecture_resolution_count = 0
total_failure_count = 0
```

## Primary-source context

- D. Platt and T. Trudgian, [The Riemann hypothesis is true up to `3*10^12`](https://arxiv.org/abs/2004.09765).
- J. C. Lagarias, [The 3x+1 problem and its generalizations](https://doi.org/10.2307/2322189).
- L. Grimmelt and G. Bhowmik, [The exceptional set of the Goldbach problem](https://arxiv.org/abs/2607.27282).
- K. Matomäki and S. Zuniga Alterman, [Weighted sieves with switching](https://arxiv.org/abs/2405.19063).

These references establish context and known boundaries. TICKET-205 makes no
claim of peer-reviewed novelty or resolution without independent expert review.
