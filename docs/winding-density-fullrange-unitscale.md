# TICKET-211: Winding Localization, Collatz Integrality, Full-Range Goldbach Exceptions, and Unit-Scale Twin Deserts

## Claim status

All four parent conjectures remain `open_not_proven`. TICKET-211 proves four
exact intermediate or no-go statements. It proves neither a parent conjecture
nor a counterexample to one. The canonical machine-readable record is
[`ticket211-winding-density-fullrange-unitscale.json`](../data/open-problem/ticket211-winding-density-fullrange-unitscale.json).

| Problem | New result | Status | Route retired | Remaining gap | Next single lemma |
|---|---|---|---|---|---|
| Riemann | Effective horizontal clearance and exact total winding still do not locate zeros | Open | Total winding plus symmetry implies critical-line location | Equality between total and critical-line zero counts | `EffectiveCriticalLineRectangleZeroCountEqualityCertificate` |
| Collatz | Every positive cycle must have valuation-one density at least `log_2(6/5)`; aggregate sufficiency is refuted | Open | Density, contraction, and product data without integrality | Uniform 2-adic obstruction above the density floor | `Uniform2AdicIntegralityObstructionForHighOneDensityWords` |
| Goldbach | A small-witness exceptional count cannot be the count driven below one | Open | Treating failure below a cutoff as complete nonrepresentation | Strictly subunit full-range exceptional count | `FullRangeBinaryGoldbachExceptionalCountStrictlyBelowOne` |
| Twin Prime | Factorial twin deserts reach every fixed coefficient `c<1` of `log X/log log X` | Open | A twin in every fixed subunit local window | Sparse dyadic positivity compatible with deserts | `SparseDyadicBilinearOmegaStrictPositivity` |

No literature-priority claim is made without independent specialist review.

## 1. Riemann Hypothesis

### Exact proposition

Put `z=s-1/2` and

```text
F(s)=cosh(2*pi*z)-cosh(pi/2).
```

Then `F` is entire, real symmetric, and satisfies `F(1-s)=F(s)`. Its zeros
are exactly

```text
s=1/2 +/- 1/4 + i*n,  n in Z.
```

On every cofinal horizontal line `Im(s)=n+1/2`,

```text
|F(s)| >= 1+cosh(pi/2).
```

Every rectangle `0<=Re(s)<=1`, `n-1/2<=Im(s)<=n+1/2` has boundary winding
two and contains two zeros, but neither zero is on `Re(s)=1/2`.

### Proof

The equation `cosh(w)=cosh(a)` is equivalent to
`w=+/-a+2*pi*i*n`, which gives the zero set. On the horizontal boundaries,

```text
cosh(2*pi*(x+i(n+1/2)))=-cosh(2*pi*x).
```

The displayed lower bound follows. The two zeros with ordinate `n` lie
strictly inside the rectangle, so the argument principle gives total winding
two. On the critical line,

```text
F(1/2+it)=cos(2*pi*t)-cosh(pi/2)<0,
```

so the critical-line zero count is zero.

### Consequence and limit

This exact model closes a logical gap left by TICKET-210: even computable
cofinal clearance and exact total winding do not locate zeros. It is not a
zeta model and has no Euler product. The next lemma must certify equality
between the total rectangle zero count and the critical-line zero count for
the actual completed zeta function.

## 2. Collatz Conjecture

### Exact proposition

For an accelerated positive integer cycle of length `h`, let `k` be the
number of valuation entries equal to one. Then

```text
k/h >= log_2(6/5) = 0.263034405834...
```

This necessary condition is not sufficient at the aggregate level. For every
`m>=1`, the repeated formal affine word `(1,2,2)^m` has density `1/3`, slope
`(27/32)^m`, and positive rational fixed point `23/5`.

### Proof and exact no-go family

After rotating a hypothetical integer cycle to its minimum `x_i>=3`, with
valuation sum `A`,

```text
2^A=product_i(3+1/x_i)<=(10/3)^h,
A>=2h-k.
```

Therefore `(6/5)^h<=2^k`, proving the density floor. One formal block has the
exact rational orbit

```text
23/5 -> 37/5 -> 29/5 -> 23/5
```

under valuations `(1,2,2)`, and

```text
(3+5/23)(3+5/37)(3+5/29)=32=2^5.
```

Repetition preserves the product identity, contraction, and density bound,
but the fixed point always has denominator five.

### Consequence and limit

The rational family is not a Collatz counterexample. It proves that valuation
density, affine contraction, and the aggregate product identity cannot by
themselves exclude integer cycles. The missing bridge is a word-uniform
2-adic or divisibility obstruction. Nonperiodic divergence remains untouched.

## 3. Strong Goldbach Conjecture

### Exact proposition

Let `W(N)` be the least prime summand in a Goldbach representation, with
`W(N)=infinity` if no representation exists. Let `E_b(X)` count even `N` in
`[X,2X]` for which no representation has a prime summand at most `b(N)`.
If an unbounded sequence satisfies `W(N)>b(N)`, then `E_b(X)>=1` on infinitely
many dyadic blocks.

TICKET-209 proves such an unbounded sequence for
`b(N)=c log N log log N` with some absolute `c>0`. Hence an eventual strict
bound `E_b(X)<1` is impossible for this small-witness predicate, regardless
of whether strong Goldbach is true.

### Proof and predicate correction

For every exceptional target `N_j`, choose the power of two `X_j` satisfying
`X_j<=N_j<2X_j`. Then `N_j` is counted by `E_b(X_j)`. Since this count is an
integer, it cannot be strictly below one on all sufficiently large blocks.

The correct closing predicate is instead

```text
E_full(X)=#{even N in [X,2X]: N has no prime-plus-prime representation}.
```

An eventual `E_full(X)<1`, combined with a verified finite prefix, would prove
strong Goldbach. No such estimate is proved here.

### Reproducible calculation and limit

The generator sieves through `2,000,000`. In nine explicit dyadic blocks it
records many failures below the illustrative cutoff `floor(log N)` and zero
full Goldbach failures. This finite table demonstrates that the predicates
differ; it does not prove the infinite conjecture or a tail estimate.

## 4. Twin Prime Conjecture

### Exact proposition

Set `X=K!` and `H=K-3`. The consecutive lower candidates `X+j`,
`2<=j<=K-2`, contain no twin-prime pair, and

```text
H / (log X/log log X) -> 1.
```

Therefore, for every fixed `c<1`, infinitely many such windows satisfy

```text
H >= c log X/log log X.
```

### Proof

For every indicated `j`, `j` properly divides `K!+j`, and `j+2` properly
divides `K!+j+2`. Stirling's formula gives

```text
log(K!)=K log K-K+O(log K),
log log(K!)=log K+log log K+o(1).
```

Substitution proves the limit. The generated rows at
`K=8,16,...,4096` are numerical checks of the convergence expression; the
proof is the divisibility identity plus Stirling asymptotics.

### Consequence and limit

TICKET-210's coefficient `1/4` is sharpened to every fixed coefficient below
one. This refutes only an overly uniform local-positivity strategy. Since
`H/X->0`, the deserts remain compatible with a positive dyadic average and
with infinitely many twin primes.

## Reproduction

```powershell
python scripts/ticket211_winding_density_fullrange_unitscale.py
python -m unittest tests.test_ticket211_winding_density_fullrange_unitscale -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

The JSON stores theorem statements, proof DAGs, finite transcripts and hashes,
route decisions, and one open lemma per problem. All four resolution counters
remain zero.

## Literature boundary

- The official RH status remains listed by the [Clay Mathematics Institute](https://www.claymath.org/millennium/riemann-hypothesis/).
- Tao's [almost-all Collatz result](https://arxiv.org/abs/1909.03562) is not a pointwise termination proof and is not reproved here.
- Finite Goldbach verification, such as [Oliveira e Silva, Herzog, and Pardi](https://doi.org/10.1090/S0025-5718-2013-02787-1), does not settle the infinite claim.
- Bounded prime gaps do not force gap two; see [Maynard](https://doi.org/10.4007/annals.2015.181.1.7).
