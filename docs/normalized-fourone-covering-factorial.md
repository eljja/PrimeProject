# TICKET-209: Normalized Boundaries, Four-One Cycles, Covering Congruences, and Factorial Twin Deserts

## Claim status

All four parent conjectures remain `open_not_proven`. TICKET-209 proves four
exact partial or no-go theorems. It does **not** prove or disprove the Riemann,
Collatz, strong Goldbach, or Twin Prime conjecture.

The canonical machine-readable artifact is
[`ticket209-normalized-fourone-covering-factorial.json`](../data/open-problem/ticket209-normalized-fourone-covering-factorial.json).

| Problem | New exact result | Resolution | Retired route | Remaining gap | Next single lemma |
|---|---|---|---|---|---|
| Riemann | Absolute completed-xi clearance on cofinal full boundaries cannot have a height-independent positive margin; gamma normalization clears the outer arithmetic edge | Open | Uniform absolute `xi` margin | Normalized central top-edge nonvanishing | `CofinalGammaNormalizedCentralTopEdgeNonvanishingCertificate` |
| Collatz | Every accelerated cycle with exactly four valuation-one entries is excluded | Open | The complete exactly-four-one periodic stratum | Five-or-more-one cycles and nonperiodic divergence | `UniformExclusionForPrimitiveValuationNecklacesWithExactlyFiveOnes` |
| Goldbach | Along unbounded even targets, `W(N) > c log N log log N` for an absolute `c>0`; hence `limsup W(N)/log N=infinity` | Open | Any constant-log universal least-witness ceiling | Exceptional-tail count beyond the covering floor | `GoldbachTailExceptionalCountBelowOneBeyondCoveringCongruenceFloor` |
| Twin Prime | Arbitrarily long factorial intervals have exact `R_I=-H` cyclotomic cancellation | Open | A positive phase margin on every interval | Independent averaged/selected dyadic phase lower bound | `IndependentBilinearOmegaPhaseLowerBoundOnInfinitelyManyDyadicIntervals` |

These are project-local theorem statements built from classical ingredients.
Correctness is tested and each proof is explicit. No academic priority or
novelty claim is made without independent specialist literature review.

## 1. Riemann hypothesis

### Declared proposition

Write

```text
xi(s) = (1/2)s(s-1) pi^(-s/2) Gamma(s/2) zeta(s).
```

No fixed `epsilon>0` can satisfy `|xi(s)|>=epsilon` on the full boundaries of
a cofinal sequence of rectangles `[-1,2] x [-T,T]`. The obstruction already
appears at the endpoint `s=2+iT`:

```text
|xi(2+iT)| <= U(T) -> 0,

U(T) = zeta(2)/(2 pi)
       sqrt((T^2+4)(T^2+1))
       sqrt((pi T/2)/sinh(pi T/2)).
```

After removing the nonzero polynomial and gamma factors,

```text
2 pi^(s/2) xi(s) / (s(s-1) Gamma(s/2)) = zeta(s),
|zeta(2+it)| >= zeta(4)/zeta(2) = pi^2/15.
```

Absolute completed-xi size is therefore the wrong cofinal invariant. The
remaining target is gamma-normalized arithmetic nonvanishing on the central
horizontal segment.

### Proof

At `s=2+iT`, absolute convergence gives `|zeta(s)|<=zeta(2)`. Also

```text
|s(s-1)| = sqrt((T^2+4)(T^2+1)),
|Gamma(1+iT/2)|^2 = pi(T/2)/sinh(pi T/2).
```

The first factor grows polynomially, while the gamma factor decays like a
polynomial times `exp(-pi T/4)`. Their product tends to zero. Since each full
top edge contains `2+iT`, a height-independent positive absolute margin is
impossible.

For the normalized quotient, the Euler product yields

```text
|zeta(2+it)|
 >= product_p (1+p^-2)^-1
  = zeta(4)/zeta(2)
  = pi^2/15.
```

For any fixed `delta>0`, the top-edge segment `Re(s)>=1+delta` is zero-free by
the Euler product. The functional equation transfers this to
`Re(s)<=-delta`. With `delta=1/4`, only `-1/4<=Re(s)<=5/4` remains in the
project's elementary reduction.

### No-go boundary

This does not refute height-dependent interval certificates. It also does not
show that a cofinal sequence of central horizontal edges is nonvanishing. No
Riemann zero is moved, found off the critical line, or globally counted here.

## 2. Collatz conjecture

### Declared proposition

For the accelerated odd map

```text
T(x)=(3x+1)/2^v2(3x+1),
```

no nontrivial positive cycle has exactly four valuation entries equal to one
and every other valuation at least two. Combined with TICKETS 206-208, every
hypothetical nontrivial positive cycle needs at least five valuation-one
entries.

### Infinite-to-finite reduction

Rotate a hypothetical cycle to its minimum odd value `m>=3`. Its first
valuation is one, while its last valuation is at least two. If the length is
`h` and the total valuation is `A`, multiplication around the cycle gives

```text
2^A = product_i (3+1/x_i) <= (10/3)^h.
```

Exactly four ones imply `A>=2h-4`. At `h=16`,

```text
2^28 3^16 = 11555266180939776 > 10^16.
```

The ratio increases by `6/5` for each larger `h`, so all `h>=16` are excluded.
For `5<=h<=15`, the same product inequality bounds `A`. Fixing the minimum
rotation leaves exactly 2,292 words. Exact affine composition gives one
rational fixed point per word; none is a positive odd integer.

### Finite certificate

| `h` | minimum `A` | maximum `A` | words | positive odd integer fixed points |
|---:|---:|---:|---:|---:|
| 5 | 6 | 8 | 3 | 0 |
| 6 | 8 | 10 | 24 | 0 |
| 7 | 10 | 12 | 100 | 0 |
| 8 | 12 | 13 | 100 | 0 |
| 9 | 14 | 15 | 210 | 0 |
| 10 | 16 | 17 | 392 | 0 |
| 11 | 18 | 19 | 672 | 0 |
| 12 | 20 | 20 | 120 | 0 |
| 13 | 22 | 22 | 165 | 0 |
| 14 | 24 | 24 | 220 | 0 |
| 15 | 26 | 26 | 286 | 0 |

### Remaining gap

The result is complete only for one periodic stratum. It does not exclude
cycles containing at least five valuation-one entries and says nothing global
about a nonperiodic divergent orbit.

## 3. Strong Goldbach conjecture

### Declared proposition

Let `W(N)` be the least prime `p` for which `N-p` is prime, with
`W(N)=infinity` if no representation exists. There is an absolute `c>0` and an
unbounded sequence of even `N` such that

```text
W(N) > c log N log log N.
```

Consequently,

```text
limsup_(N even) W(N)/log N = infinity.
```

### Greedy covering proof

For large `B`, put `z=floor(B/(log B)^2)` and begin with all odd primes
`p<=B`. For each odd prime `q<=z`, choose the residue `r_q mod q` containing
the largest number of still-uncovered candidates. At most a fraction
`1-1/q` survives that step. Thus

```text
S <= pi(B) product_(3<=q<=z) (1-1/q)
  = O(B/(log B log z))
```

by Mertens' product theorem and the prime number theorem.

There are enough distinct primes `Q_p in (B,2B)` to assign one to each of the
`S` survivors. Apply CRT to

```text
N = 0   (mod 2),
N = r_q (mod q),
N = p   (mod Q_p) for every survivor p.
```

Choose the even representative `M<N<=2M`, where `M` is the product of all
moduli. Every `N-p` with prime `p<=B` is then a proper composite. Hence
`W(N)>B`. Moreover,

```text
log M <= theta(z) + S log(2B) = O(B/log B),
```

which rearranges to `B>=c log N log log N` for some absolute `c>0`.

### What this does not prove

The construction blocks only `p<=B`. A larger prime summand may still produce
a Goldbach representation. It is therefore not a Goldbach counterexample and
does not bound the exceptional set. Its role is to rule out an overstrong
constant-log least-witness ceiling and to raise the required tail theorem.

## 4. Twin Prime conjecture

### Declared proposition

For every `H>=1`, there is an interval of `H` consecutive lower candidates
containing no twin-prime pair. For the exact TICKET-208 identity

```text
M^2 T_I = H + R_I,
```

these intervals satisfy `T_I=0` and therefore `R_I=-H`. No estimate
`R_I>=-H+epsilon(H)` with `epsilon(H)>0` can hold on every interval.

### Proof

Set `K=H+3` and `N=K!`. For every `j=2,...,K-2`,

```text
j     divides N+j,
j+2   divides N+j+2.
```

Both numbers exceed their displayed divisors and are composite. There are
exactly `H` consecutive values of `j`, proving an arbitrarily long twin-free
interval. Substitution of `T_I=0` into the exact cyclotomic identity gives
`R_I=-H`.

### No-go boundary

Factorial windows are short compared with their location and are not the
expanding dyadic intervals required for infinitude. The counterfamily rules out
only all-interval positivity. Averaged or selected cofinal dyadic phase bounds
remain possible and unproved.

## Reproduction

```powershell
python scripts/ticket209_normalized_fourone_covering_factorial.py
python -m unittest tests.test_ticket209_normalized_fourone_covering_factorial -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

The generator writes the integrated audit and four track-local JSON files. The
test suite independently replays all 2,292 Collatz words, every covering-CRT
divisibility certificate, the factorial composite certificates, and all proof
status guards.

To keep GitHub Pages lightweight, the Goldbach JSON stores the greedy cover,
all survivor-to-forcing-prime assignments, the total certificate count, and a
SHA-256 transcript rather than duplicating one row per covered prime. The test
reconstructs and verifies every omitted `p<=B` divisibility certificate.

## Literature and priority boundary

- The Riemann status and target are described by the [Clay Mathematics Institute](https://www.claymath.org/millennium/riemann-hypothesis/); the gamma modulus identity is tabulated by [NIST DLMF](https://dlmf.nist.gov/5.4.E3).
- Tao's [almost-all Collatz theorem](https://doi.org/10.1017/fmp.2022.8) is a different quantified result and does not imply all-orbit descent.
- Finite Goldbach verification is documented by [Oliveira e Silva, Herzog, and Pardi](https://doi.org/10.1090/S0025-5718-2013-02787-1); finite verification is not an all-integer proof.
- Maynard's [bounded-gap theorem](https://doi.org/10.4007/annals.2015.181.1.7) does not force gap two.

The Collatz stratum closure and the Goldbach covering formulation should be
treated as project-local results until their mathematical correctness and
literature priority have been independently reviewed by specialists.
