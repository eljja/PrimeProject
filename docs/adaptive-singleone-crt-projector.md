# TICKET-206: Adaptive Certificates, Single-One Cycles, CRT Witnesses, and Omega Projectors

## Claim status

All four parent conjectures remain `open_not_proven`. TICKET-206 proves four
exact partial or no-go theorems. It does **not** prove or disprove the Riemann,
Collatz, strong Goldbach, or Twin Prime conjecture.

The canonical machine-readable artifact is
[`ticket206-adaptive-singleone-crt-projector.json`](../data/open-problem/ticket206-adaptive-singleone-crt-projector.json).

| Problem | New exact result | Resolution | Retired route | Remaining gap | Next single lemma |
|---|---|---|---|---|---|
| Riemann | A zero-free compact boundary admits a finite derivative-certified winding mesh; fixed budgets fail at inverse-clearance scale | Open | Fixed contour budget independent of clearance | Effective completed-zeta bounds on a cofinal contour family | `EffectiveCompletedZetaRectangleBoundsAndCofinalAdaptiveTermination` |
| Collatz | No positive nontrivial cycle has exactly one valuation `1` and all others arbitrary `>=2` | Open | Searching the exactly-one-`1` periodic stratum | Mixed primitive necklaces with at least two `1` entries; nonperiodic divergence | `UniformNondivisibilityForPrimitiveMixedNecklacesWithAtLeastTwoOnes` |
| Goldbach | For every `B`, an infinite CRT progression forces every Goldbach witness, if one exists, above `B` | Open | A fixed bounded set of small-prime witnesses | An exceptional-count bound below one with a growing witness cutoff | `GrowingWitnessCutoffGoldbachTailExceptionalCountStrictlyBelowOne` |
| Twin Prime | Binomial inversion of `Omega` is an exact prime projector, but every finite truncation has infinitely many positive composite-composite shift-two false positives | Open | Any fixed finite `Omega` truncation as an exact twin indicator | Uniform cancellation of the infinite projector tail | `UniformTailCancellationForBinomialOmegaProjectorCorrelation` |

## 1. Riemann hypothesis

### Declared proposition

Let `gamma:[0,L]->C` be a unit-speed `C1` closed contour and put
`g=f o gamma`, where `f` is analytic near the contour. If `g` is nonzero on
the boundary, then

```text
delta = min_t |g(t)| > 0,
K = max_t |g'(t)| < infinity.
```

If `K>0`, repeated uniform bisection eventually produces mesh
`h<delta/K`. Every segment then satisfies the TICKET-205 disk condition, so
the sampled polygon has exactly the same winding as the analytic image. If
`K=0`, the boundary image is constant and nonzero.

Thus the derivative-certified winding grammar is complete for every fixed
zero-free compact boundary, provided rigorous positive clearance and
derivative bounds can be supplied.

### Proof

Compactness and continuity give the displayed `delta` and `K`. On a segment
starting at `t_j`, the fundamental theorem of calculus gives

```text
|g(t)-g(t_j)| <= K h < delta <= |g(t_j)|.
```

The image segment and its chord lie in a convex disk excluding zero. Replacing
all image segments by their chords preserves winding. Dyadic mesh sizes tend
to zero, so bisection terminates after finitely many levels.

### Exact complexity no-go

For `epsilon=1/q`, consider

```text
f_epsilon(z)=z-(1-epsilon)
```

on the unit circle. Its boundary clearance is `epsilon`, its arclength
derivative bound is `1`, and its winding is one. The global mesh criterion is

```text
2*pi/N < epsilon.
```

Using only the exact rational bounds `3<pi<22/7`:

```text
N <= 6q  => the criterion fails,
N = 8q   => the criterion succeeds.
```

Therefore no fixed global segment budget certifies this family as
`epsilon -> 0`. The obstruction concerns this derivative/clearance certificate
criterion; it is not a lower bound against every conceivable analytic method.

### Remaining gap

The theorem does not provide an interval oracle proving positive clearance on
cofinal completed-zeta rectangles. Producing such bounds without assuming the
desired zero-free statement is the decisive open step.

## 2. Collatz conjecture

### Declared proposition

For the accelerated odd map

```text
T(x)=(3x+1)/2^v2(3x+1),
```

no positive nontrivial cycle has a valuation period containing exactly one
entry equal to `1` and all remaining entries at least `2`.

### Proof

Rotate a hypothetical period of length `h` to its minimum odd value `m`.
TICKET-205 proves that the outgoing valuation at a nontrivial minimum is `1`.
It is therefore the unique valuation-one step. Put

```text
y=(3m+1)/2,
F(x)=(3x+1)/4.
```

Every subsequent step is at most `F`. With `q=(3/4)^(h-1)`, return to `m`
implies

```text
m <= F^(h-1)(y)
  = 1-q/2+(3q/2)m,
m <= (1-q/2)/(1-3q/2).
```

For `h>=4`, `q<=27/64<1/2`, so the right side is strictly below `3`, while a
positive odd nontrivial minimum is at least `3`. This is a contradiction.

For the remaining lengths:

- `h=3`: the bound gives `m<=23/5`, hence `m=3`; but `3 -> 5 -> 1`.
- `h=2`: if the other valuation is `b>=2`, then
  `(2^(b+1)-9)m=5`, which has no positive integral solution.
- `h=1`: the valuation-one fixed-point equation gives `m=-1`.

The proof covers arbitrary remaining valuations, not a finite alphabet.
Enumeration of 167,481 words of lengths 1 through 8 over `{1,2,3,4,5}` with
exactly one `1` found zero integral cycle words and is only a regression check.

### Remaining gap

A hypothetical nontrivial positive cycle must now have at least two
valuation-one entries and at least one larger valuation. Those mixed necklaces
and every nonperiodic divergent orbit remain open.

## 3. Strong Goldbach conjecture

### Declared proposition

For every integer bound `B`, there is an infinite arithmetic progression of
even integers `N` such that `N-p` is composite for every prime `p<=B`.
Consequently no fixed finite set of prime summands can witness all sufficiently
large Goldbach targets. Conditional on strong Goldbach, the least prime
witness is unbounded.

### Proof

For each odd prime `p<=B`, choose a distinct odd prime `q_p>B`. The Chinese
remainder theorem gives one residue class satisfying

```text
N = 0 (mod 2),
N = p (mod q_p) for every odd prime p<=B.
```

Choose a representative larger than every `p+q_p`. Then `N-p` is a proper
multiple of `q_p`, hence composite. Also `N-2` is even and greater than two.
Adding any multiple of

```text
M=2*product_(p<=B, p odd) q_p
```

preserves all congruences, yielding an infinite progression.

### Logical limit

This is not a Goldbach counterexample. The construction suppresses witnesses
only through `B`; a larger prime may still represent every constructed target.
The theorem instead proves that any viable tail analysis must allow the
witness cutoff to grow with `N`. In particular, the maximum least witness `751`
seen through ten million in TICKET-205 cannot be promoted to a universal bound.

## 4. Twin Prime conjecture

### Declared proposition

For `m>=0`, define

```text
P_infinity(m)=sum_(j>=1) (-1)^(j-1) j binom(m,j).
```

The sum is pointwise finite and satisfies

```text
P_infinity(m)=1 if m=1, and 0 otherwise.
```

Therefore `P_infinity(Omega(n))` is the exact prime indicator. Its truncation

```text
P_R(m)=sum_(1<=j<=R) (-1)^(j-1) j binom(m,j)
```

is exact only for `m<=R`; for `m>R`,

```text
P_R(m)=(-1)^(R-1) m binom(m-2,R-1).
```

Every fixed `R` has an infinite arithmetic progression on which both `n` and
`n+2` have at least `R+1` distinct prime factors and
`P_R(Omega(n))P_R(Omega(n+2))>0`.

### Proof

Use

```text
j binom(m,j)=m binom(m-1,j-1).
```

The complete alternating sum is the derivative identity for `(1-x)^m` at
`x=1`. The standard finite alternating-binomial identity gives the displayed
closed form for `m>R`.

For the shift-two no-go, choose disjoint sets of `R+1` odd primes with products
`A` and `B`. CRT solves

```text
n=0 (mod A),
n=-2 (mod B).
```

All sufficiently large representatives make both endpoints composite with
`Omega>R`. Both truncated projectors have sign `(-1)^(R-1)`, so their product
is positive. This also shows why no polynomial of fixed degree in `Omega` can
equal the prime indicator on all integers: it would have infinitely many
integer roots while being nonzero at `1`.

### Remaining gap

The exact infinite projector is an identity, not an analytic twin-prime lower
bound. Interchanging, truncating, or estimating its shift-two correlation
requires a uniform tail-cancellation theorem. No such theorem is proved here.

## Proof DAGs

Each machine artifact contains the same five-state dependency pattern:

```text
TICKET-205 closed result
        |
        v
TICKET-206 exact theorem ---> refuted or limited route
        |
        v
single highest-risk open lemma
        |
        v
parent conjecture [open_not_proven]
```

The final node is deliberately open in all four DAGs.

## Reproduction

```bash
python scripts/ticket206_adaptive_singleone_crt_projector.py
python -m unittest tests.test_ticket206_adaptive_singleone_crt_projector
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Expected machine status:

```text
exact_partial_theorem_count = 4
refuted_or_limited_route_count = 4
proof_dag_count = 4
conjecture_resolution_count = 0
total_failure_count = 0
```

## Primary-source context

- D. Platt and T. Trudgian, [The Riemann hypothesis is true up to `3*10^12`](https://arxiv.org/abs/2004.09765).
- J. C. Lagarias, [The 3x+1 problem and its generalizations](https://doi.org/10.2307/2322189).
- L. Grimmelt and G. Bhowmik, [The exceptional set of the Goldbach problem](https://arxiv.org/abs/2607.27282).
- K. Matomäki and S. Zuniga Alterman, [Weighted sieves with switching](https://arxiv.org/abs/2405.19063).

These sources define established context and known boundaries. TICKET-206
makes no claim of peer-reviewed novelty or priority without independent expert
review.
