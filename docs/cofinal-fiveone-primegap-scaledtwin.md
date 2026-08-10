# TICKET-210: Cofinal Lines, Five-One Cycles, Prime-Gap Transfer, and Scaled Twin Deserts

## Claim status

All four parent conjectures remain `open_not_proven`. TICKET-210 proves four
partial or no-go theorems. It proves neither a parent conjecture nor a
counterexample to one. The canonical machine-readable record is
[`ticket210-cofinal-fiveone-primegap-scaledtwin.json`](../data/open-problem/ticket210-cofinal-fiveone-primegap-scaledtwin.json).

| Problem | New closed result | Status | Route retired | Remaining gap | Next single lemma |
|---|---|---|---|---|---|
| Riemann | Existential cofinal central zero avoidance, plus a symmetric off-critical countermodel | Open | Cofinal horizontal nonvanishing alone implies RH | Effective clearance and winding | `EffectiveCofinalCentralEdgeClearanceAndWindingIncrementCertificate` |
| Collatz | Every accelerated cycle word with exactly five valuation-one entries is excluded | Open | The entire five-one periodic stratum | Six-or-more-one cycles and nonperiodic divergence | `ValuationOneMultiplicityUniformCycleObstruction` |
| Goldbach | Exact prime-gap-to-least-witness transfer; the current large-gap input is asymptotically below the TICKET-209 floor | Open | Current prime-gap lower bounds improve the covering floor by themselves | Exceptional-tail count below one | `GoldbachTailExceptionalCountBelowOneBeyondCoveringCongruenceFloor` |
| Twin Prime | Factorial twin deserts have length at least `(1/4) log X/log log X` | Open | Positivity in every local window at this scale | A dyadic average that permits local deserts | `DyadicBilinearOmegaPhaseLowerBoundPermittingLogOverLogLogDeserts` |

No literature-priority claim is made without independent specialist review.

## 1. Riemann Hypothesis

### Exact proposition

For every sufficiently large integer `n`, there is a height `T_n` in
`(n,n+1)` such that

```text
zeta(s) != 0  for -1/4 <= Re(s) <= 5/4 and Im(s)=T_n.
```

The minimum modulus on that compact segment is positive. This property does
not imply RH, even when functional and conjugation symmetries are imposed.
Put `z=s-1/2` and

```text
P(s)=z^4+(15/8)z^2+289/256.
```

Then `P(1-s)=P(s)`, `P(conj(s))=conj(P(s))`, and its zeros are
`1/2 +/- 1/4 +/- i`, all off the critical line. Nevertheless, for `T>1`,

```text
min_sigma |P(sigma+iT)| >= (T^2-1)^2.
```

### Proof and calculation

Completed xi is a nonzero entire function. Its zeros are isolated, so a
compact strip in each unit height band contains finitely many zero ordinates.
Choose `T_n` outside that finite set. At positive height the factors relating
xi and zeta are nonzero; compactness then gives a positive minimum.

The polynomial roots occur in a functional-equation and conjugation quartet.
On the line `Im(s)=T>1`, the two roots at height `+1` are each at distance at
least `T-1`, and the two at `-1` are each at distance at least `T+1`.
Multiplication gives `(T^2-1)^2`. The generator checks the exact lower bound
against a reproducible grid at six heights, but the proof is the product
distance inequality, not the grid.

### Limit

The zeta height choice is existential, not effective. There is no computable
clearance, no certified argument variation, and no off-critical zeta zero.
The countermodel does not have zeta's Euler product. The next task must combine
effective interval clearance with an argument-principle winding increment.

## 2. Collatz Conjecture

### Exact proposition

For the accelerated odd map

```text
T(x)=(3x+1)/2^v2(3x+1),
```

no nontrivial positive cycle has exactly five valuation entries equal to one
and every other valuation at least two. This strictly extends TICKET-189,
which treated only the case in which every other valuation equals two.

### Infinite-to-finite reduction

Rotate a hypothetical cycle to its minimum odd value `m>=3`. Its first
valuation is one and its last is at least two. If the length is `h`, the
valuation sum is `A`, and exactly `k` entries are one, then

```text
2^A = product_i (3+1/x_i) <= (10/3)^h,
A >= 2h-k,
(6/5)^h <= 2^k.
```

Therefore

```text
h <= floor(k log(2)/log(6/5)).
```

For `k=5`, `h<=19`; `h>=20` is impossible. For `6<=h<=19`, the same product
bound makes `A` finite. Fixing the minimum rotation and enumerating all weak
compositions gives exactly 29,758 words. Exact rational affine composition
finds zero positive odd integer fixed points.

### Limit

The complete five-one periodic stratum is closed, but cycles with six or more
ones and every nonperiodic divergent orbit remain open. Repeating one
multiplicity at a time is not a Collatz proof; the next lemma must be uniform
in the number of valuation-one entries.

## 3. Strong Goldbach Conjecture

### Exact proposition

Let `q<r` be consecutive odd primes, `g=r-q`, and `N=r-1`. If `W(N)` is the
least prime `p` for which `N-p` is prime, then

```text
W(N) > g-2.
```

For every prime `p<=g-2`, the complement satisfies

```text
q+1 <= N-p <= r-3,
```

so it lies strictly inside the prime gap and is composite.

The Ford-Green-Konyagin-Maynard-Tao theorem

```text
G(X) >> log X log_2 X log_4 X / log_3 X
```

therefore transfers to an independent sequence of even targets with the same
order of least-witness lower bound. However,

```text
log_4 N / log_3 N -> 0.
```

Thus this published large-gap input is asymptotically weaker than the
`c log N log_2 N` covering-congruence floor proved in TICKET-209. The transfer
is exact, but the proposed route does not improve the current project bound.

### Reproducible calculation and limit

The generator sieves through two million, extracts the last ten record prime
gaps, verifies every interior integer is composite, and independently finds
the actual least Goldbach witness. Each finite target has a witness above the
transferred floor, so none is a counterexample.

This comparison concerns the current published large-gap lower bound passed
through this transfer. It does not rule out stronger future gap theorems and
does not bound the Goldbach exceptional set. The retained task is still a
parity-breaking tail estimate with exceptional count below one.

## 4. Twin Prime Conjecture

### Exact proposition

For every integer `K>=8`, set `X=K!` and `H=K-3`. The consecutive lower
candidates `X+j`, `2<=j<=K-2`, contain no twin-prime pair, and

```text
H >= (1/4) log X/log log X.
```

### Proof

For every indicated `j`, `j` divides `X+j` and `j+2` divides `X+j+2`; both
are proper divisors. Also

```text
log X <= K log K,
log X >= (K/2) log(K/2),
log log X >= (1/2) log K       (K>=8).
```

Hence `log X/log log X<=2K`, while `H=K-3>=K/2`, proving the factor `1/4`.
The generator verifies all divisibility certificates and the scale inequality
for `K=8,16,32,64,128,256`.

### Limit

These windows are still negligible relative to `X`. They refute positivity in
every short local window at this scale, but they are compatible with positive
dyadic averages and with infinitely many twin primes. The next phase estimate
must explicitly permit these deserts.

## Reproduction

```powershell
python scripts/ticket210_cofinal_fiveone_primegap_scaledtwin.py
python -m unittest tests.test_ticket210_cofinal_fiveone_primegap_scaledtwin -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

The Collatz transcript is stored as per-length counts and
SHA-256 hashes rather than 29,758 repeated JSON rows.

## Literature boundary

- The [Ford-Green-Konyagin-Maynard-Tao long-gap theorem](https://doi.org/10.1090/jams/876) is an imported result, not a PrimeProject proof.
- The official RH status remains listed by the [Clay Mathematics Institute](https://www.claymath.org/millennium/riemann-hypothesis/).
- Finite Goldbach verification does not settle the infinite claim; see [Oliveira e Silva, Herzog, and Pardi](https://doi.org/10.1090/S0025-5718-2013-02787-1).
- Bounded prime gaps do not force gap two; see [Maynard](https://doi.org/10.4007/annals.2015.181.1.7).
