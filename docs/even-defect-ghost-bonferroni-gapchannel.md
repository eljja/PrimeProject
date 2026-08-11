# TICKET-212: Even defect, 2-adic ghosts, full-witness products, and gap channels

## Claim status

All four parent conjectures remain `open_not_proven`. TICKET-212 proves four
exact partial or no-go theorems. It proves neither a parent conjecture nor a
counterexample to one. The canonical machine-readable record is
[`ticket212-even-defect-ghost-bonferroni-gapchannel.json`](../data/open-problem/ticket212-even-defect-ghost-bonferroni-gapchannel.json).

| Problem | Exact new result | Status | Discarded route | Remaining gap | Next single lemma |
|---|---|---|---|---|---|
| Riemann | Symmetry quantizes the unaccounted zero defect; `N-L<2` already forces simple critical-line zeros | Open | Requiring exact count equality as the minimal finite-rectangle threshold | An all-height defect bound for actual completed zeta | `UniformAllHeightCriticalLineDefectStrictlyBelowTwo` |
| Collatz | Every valuation word has a genuine `2`-adic ghost cycle | Open | A `Z_2`-membership obstruction for high-one-density words | Uniform ordinary odd-divisor nondivisibility | `UniformOddDivisorNondivisibilityForHighOneDensityWords` |
| Goldbach | The full exception indicator is an exact witness product; every fixed even Bonferroni truncation gives false exceptions | Open | Fixed-order unnormalized inclusion-exclusion below one | Uniformly controlled full-product resummation | `UniformFullWitnessProductResummationBelowOne` |
| Twin Prime | Infinite twins are exactly gap-two positivity on infinitely many dyadic blocks; bounded-gap aggregate mass cannot select gap two | Open | Promoting a finite gap aggregate to the `h=2` channel | Arithmetic gap-two channel positivity | `GapTwoDyadicChannelPositiveOnInfinitelyManyBlocks` |

No priority or novelty claim is made before independent specialist review.

## 1. Riemann Hypothesis

### Exact proposition

Let `R` be a rectangle in the upper half of the critical strip which is
invariant under

```text
s -> 1-conjugate(s)
```

and whose boundary contains no zero of the completed zeta function. Let `N`
be the number of zeros in `R`, counted with multiplicity. Suppose `L` disjoint
critical-line intervals have rigorously certified sign changes of the real
Hardy function. Then

```text
N - L < 2
```

implies that every zero in `R` is simple and lies on the critical line. The
constant `2` is sharp.

### Proof

Let `O` be the number of distinct critical-line zeros of odd multiplicity.
Every certified sign-change interval contains at least one such zero, hence
`O>=L`. Every off-line upper-half zero occurs with its reflected partner
`1-conjugate(rho)`. A line zero of multiplicity `m` contributes one sign
change precisely when `m` is odd. Therefore

```text
N-O
 = 2*(off-line paired multiplicity)
   + sum over line zeros of (m-(m mod 2)).
```

The right side is a nonnegative even integer. Since

```text
N-L = (N-O) + (O-L),
```

the strict sub-two bound forces `N-O=0`. Thus there is no off-line pair and
every line multiplicity is one. The remaining term `O-L` may be `0` or `1`,
so at most one simple line zero can be outside the certified intervals.

One reflected off-line pair has `N-L=2`. A double critical-line zero also has
defect `2` because it does not change sign. These examples prove sharpness.
The TICKET-211 entire countermodel lies exactly on this sharp boundary with
`N=2` and `L=0`.

### Computation and limit

The generator checks exact combinatorial zero configurations: all simple line
zeros, one uncertified simple line zero, one reflected off-line pair, one
double line zero, and the TICKET-211 band. This is not a computation of zeta.

Platt and Trudgian used interval arithmetic, Hardy-function sign changes, and
Turing's method to rigorously verify RH through height `3*10^12`. PrimeProject
does not repeat or extend that computation. The new theorem only identifies a
sharp integer threshold for a future all-height certificate.

## 2. Collatz Conjecture

### Exact proposition

For a nonempty accelerated-Collatz valuation word

```text
w=(a_1,...,a_h),  A=sum a_i,
```

define

```text
C = sum_(j=0)^(h-1) 3^(h-1-j) 2^(a_1+...+a_j),
```

where the prefix for `j=0` is empty. Composition of the affine branches gives

```text
T_w(x) = (3^h x+C)/2^A,
x_w = C/(2^A-3^h).
```

Both `C` and `D=2^A-3^h` are odd. Consequently every word has a unique fixed
point `x_w` in `Z_2`, and its cyclic orbit realizes the prescribed valuations
exactly. Membership in `Z_2` therefore excludes no valuation word.

A positive ordinary-integer cycle instead requires

```text
D>0 and D divides C in Z.
```

### Proof

The composition formula follows by induction. The first summand of `C` is odd
and all later summands are even. The denominator is even minus odd. Thus the
reduced denominator of `x_w` is odd, so `x_w` is a `2`-adic integer. Each
intermediate state is the corresponding cyclically rotated odd rational in
`Z_2`; hence `v_2(3x_i+1)=a_i`, and the orbit closes after `h` branches.

Ordinary positivity requires `D>0`. Because `D` is odd, ordinary integrality
is exactly the divisibility `D|C`, a condition not detected by `Z_2`
membership. The TICKET-211 family `(1,2,2)^m` has the same ghost `23/5` for
all `m`: it meets the density floor and all local `2`-adic branch conditions
but fails ordinary integrality.

### Computation and limit

The generator enumerates every word of length at most `8` over valuations
`1..4`. For positive contracting words above the TICKET-211 one-density floor,
it replays the exact rational orbit and verifies automatic `Z_2` membership.
This finite table is a regression test. The parity proof covers every finite
word; the table is not its logical basis.

A 2026 preprint by Dhiman and Pandey independently develops `2`-adic ghost
cycles and proves a non-semilinearity result for the ordinary divisibility
predicate. Accordingly, PrimeProject makes no priority claim for ghost-cycle
universality. The new project decision is to abandon `Z_2` membership as the
next obstruction and target the ordinary odd divisor directly.

## 3. Strong Goldbach Conjecture

### Exact proposition

For an even target `N`, let

```text
y_p = 1_P(N-p),  for primes p<=N/2,
A(N) = sum y_p.
```

Then the full nonrepresentation indicator is exactly

```text
I_0(N) = product_(p<=N/2) (1-y_p).
```

For a fixed even truncation order `2r`, its Bonferroni upper bound is

```text
B_2r(A) = sum_(j=0)^(2r) (-1)^j binomial(A,j).
```

For every integer `A>=1`,

```text
B_2r(A) = binomial(A-1,2r).
```

Thus every represented target with `A>=2r+1` contributes at least one false
exception. The prime number theorem plus an exact pair-count pigeonhole
argument shows that `A(N)` is unbounded. Consequently no fixed even-order
unnormalized Bonferroni sum can make every sufficiently large dyadic
full-exception upper bound strictly smaller than one.

### Proof

The witness product is one exactly when all witness bits vanish. Expanding it
gives full inclusion-exclusion. Pascal's identity gives

```text
sum_(j=0)^k (-1)^j binomial(A,j)
  = (-1)^k binomial(A-1,k),  A>=1.
```

At even order this is a nonnegative upper bound. Once `A>2r`, it is at least
one, although the exact exception indicator is zero. Higher representation
multiplicity therefore makes this fixed-order bound worse rather than better.

For completeness, let `P=pi(x)-1` be the number of odd primes at most `x`.
The `P(P+1)/2` unordered pairs of odd primes are distributed among at most
`x-2` even sums from `6` through `2x`. Hence some even `N<=2x` satisfies

```text
A(N) >= ceil(P(P+1)/(2(x-2))).
```

By the prime number theorem this lower bound is asymptotic to
`x/(2 log(x)^2)` and tends to infinity. Thus, for every fixed `r`, arbitrarily
large represented targets have `A(N)>=2r+1`; the fixed truncation contributes
at least one false exception in the dyadic block containing each such target.

### Computation and limit

The generator sieves through `2,000,000`, computes full unordered witness
counts at six targets, and verifies the identity for witness counts `0..12`
and orders `0,2,4,6`. It also records the exact pair-count pigeonhole lower
bound at five prime cutoffs. All sampled targets are represented, while their
fixed Bonferroni upper bounds become large positive false exceptions.

This imports the prime number theorem but does not improve the published
verification through `4*10^18`, and it does not estimate a minor arc. It
rejects only fixed-order, unnormalized inclusion-exclusion. A proof still
needs a uniformly controlled resummation of the complete witness product
whose dyadic total is strictly below one.

## 4. Twin Prime Conjecture

### Exact proposition

Let `T_(j,h)` count prime pairs `p,p+h` with

```text
2^j <= p < 2^(j+1)
```

for even `h` in a fixed finite set `H` containing `2`. Then the Twin Prime
Conjecture is equivalent to

```text
T_(j,2)>0 for infinitely many j.
```

If

```text
sum_(h in H) T_(j,h)>0
```

for infinitely many `j`, finite pigeonhole proves only that some `h` occurs
infinitely often. It does not select `h=2`. The exact channel model

```text
T_(j,6)=1 and T_(j,h)=0 for h!=6
```

has positive finite-gap aggregate in every block but no twin channel.

### Proof

Each twin pair lies in one dyadic block, and every bounded block is finite.
Thus infinitely many twins are equivalent to gap-two positivity on infinitely
many dyadic indices. If a finite sum of nonnegative gap channels is positive
on infinitely many blocks, one channel recurs infinitely often. Pigeonhole
does not name that channel, as the gap-six countermodel shows.

### Computation and limit

The generator sieves through `10,000,000` and records the channels
`h=2,4,...,30` on each complete dyadic block. Every finite gap-two block in
the table is positive. This is bounded evidence only.

Maynard's bounded-gap theorem proves that some bounded prime gap recurs; it
does not isolate gap `2`. The new proof target is therefore explicitly
gap-two-specific rather than a further aggregate bounded-gap statistic.

## Reproduction

```powershell
python scripts/ticket212_even_defect_ghost_bonferroni_gapchannel.py
python -m unittest tests.test_ticket212_even_defect_ghost_bonferroni_gapchannel -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

The integrated JSON and four track JSON files contain the propositions,
proofs, finite transcripts and SHA-256 hashes, route decisions, claim
boundaries, and proof DAGs. The conjecture resolution count remains zero.

## Literature boundary

- Platt and Trudgian, [The Riemann hypothesis is true up to `3*10^12`](https://arxiv.org/abs/2004.09765).
- Dhiman and Pandey, [2-Adic Obstructions to Presburger-Definable Characterizations of Collatz Cycles](https://arxiv.org/abs/2601.12772), a 2026 preprint.
- Oliveira e Silva, Herzog, and Pardi, [Empirical verification of the even Goldbach conjecture and computation of prime gaps up to `4*10^18`](https://doi.org/10.1090/S0025-5718-2013-02787-1).
- Maynard, [Small gaps between primes](https://doi.org/10.4007/annals.2015.181.1.7).
