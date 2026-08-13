# TICKET-224: Sharp Completeness Thresholds

## Status and claim boundary

TICKET-224 continues the four proof DAGs from TICKET-223. It proves four
exact bounded theorems, gives explicit countermodels to four insufficient
routes, and resolves none of the parent conjectures.

| Track | Exact result | Refuted or limited route | Parent status |
|---|---|---|---|
| Riemann hypothesis | Optimal `1/4` exponential tail envelope and a strict band-sign certificate | The earlier factor-one envelope is sharp, or an abstract sign certificate is already an RH criterion | Open |
| Collatz conjecture | Exact prime-power valuation criterion for finite cycles | Radical-only adaptive divisibility is sufficient | Open |
| Strong Goldbach conjecture | Square-root wheel exactness at a finite horizon | A fixed or incomplete wheel count is the prime count | Open |
| Twin-prime conjecture | Square-root pair-filter exactness and subthreshold CRT countermodels | Sub-square-root wheel survival certifies twin primality | Open |

The common theme is a completeness threshold. A finite observation can become
an exact decision rule only after it contains enough information. Reaching
that threshold does not prove a universal or infinitude statement.

## 1. Riemann hypothesis

### Declared proposition

Let `sigma` be a finite signed Borel measure on `(0,infinity)` with

```text
||sigma||_eta = integral exp(eta t) d|sigma|(t) < infinity,
```

where `eta>0`. Define the dyadic band

```text
W_j(sigma)
  = integral [exp(-2^(-j)t) - exp(-2^(1-j)t)] d sigma(t).
```

For the tail supported on `[T,infinity)`,

```text
sup_j |W_j(sigma_tail)|
  <= (1/4) exp(-eta T) ||sigma||_eta.                 (RH-224.1)
```

The constant `1/4` is optimal uniformly in `j` and `T`. Therefore, if a
truncated band has absolute value strictly larger than the right side of
`(RH-224.1)`, the full band has the same sign.

### Proof

Put `u=2^(-j)t`. The unsigned band kernel is

```text
k(u) = exp(-u) - exp(-2u).
```

It is positive for `u>0`, and

```text
k'(u) = -exp(-u) + 2 exp(-2u).
```

The unique critical point is `u=log 2`, where `k(log 2)=1/4`; the endpoint
limits are zero. Hence `0<=k(u)<=1/4`. It follows that

```text
|W_j(sigma_tail)|
 <= (1/4) |sigma|([T,infinity))
 <= (1/4) exp(-eta T) ||sigma||_eta.
```

For any integer `j`, set `T=2^j log 2` and

```text
sigma = exp(-eta T) delta_T.
```

Its weighted norm is one and its `j`th band equals
`exp(-eta T)/4`. Equality proves uniform optimality. The sign certificate is
the reverse triangle inequality. At the extremal margin, an oppositely signed
tail atom can cancel the truncated band, so the strict inequality cannot be
removed uniformly.

### Reproducible calculation

The calculator checks six cutoffs for the unbounded alternating atomic model
from TICKET-223 and nine extremal atoms with `T=2^j log 2`. Every model tail
obeys the quarter envelope and every extremal row attains equality exactly.

### Limit, route decision, and next lemma

This improves an abstract truncation constant. It does not construct a
measure equivalent to the zeta zero defect, prove that such a measure has the
required exponential moment, or establish a prime-side band margin.

- Discard: using the nonsharp factor-one envelope, or promoting abstract band
  control to RH.
- Retain: derive rigorous prime-side bands and compare their margins with the
  optimal envelope.
- Next lemma:
  `PrimeSideDyadicBandMarginsExceedSharpQuarterTailEnvelopeAtCofinalCutoffs`.

## 2. Collatz conjecture

### Declared proposition

For a positive accelerated Collatz valuation word `a=(a_1,...,a_h)`, let

```text
S = sum a_i,
D = 2^S - 3^h > 0,
B = sum_i 3^(h-i) 2^(a_1+...+a_(i-1)).
```

TICKET-222 proved that `D|B` is the exact finite-cycle condition. If

```text
D = product_(q|D) q^(e_q),
```

then

```text
D|B  iff  v_q(B) >= e_q for every q|D.               (CO-224.1)
```

Checking only `rad(D)|B` is insufficient. The primitive word

```text
a = (1,1,2,4,3)
```

has

```text
D = 2^11 - 3^5 = 1805 = 5*19^2,
B = 475 = 5^2*19.
```

Thus `rad(D)=95` divides `B`, while `D` does not.

### Proof

Equivalence `(CO-224.1)` is unique factorization. A divisibility failure has a
certificate consisting of any prime `q|D` for which `v_q(B)<v_q(D)`.

For the displayed word, direct substitution gives `D=1805` and `B=475`.
Its length is prime and the word is nonconstant, so it cannot be a repetition
of a shorter block and is primitive. At `q=19`,

```text
v_19(D)=2 > 1=v_19(B),
```

although both primes in `rad(D)=5*19` divide `B`. This is an exact
counterexample to radical-only sufficiency.

### Reproducible calculation

The audit enumerates all 1,360 words of heights `2..5` over the alphabet
`{1,2,3,4}`. Among the 1,295 primitive words with `D>0`, the prime-power
criterion has zero mismatches with direct `D|B`. It finds five radical-only
false positives, the five rotations of the displayed word.

### Limit, route decision, and next lemma

Factoring `D` completely produces an exact certificate but merely decomposes
the original divisibility condition. It does not prove that every nontrivial
primitive word has a deficit, bound where a deficit prime power must occur,
or address aperiodic divergent trajectories.

- Discard: radical-only adaptive divisibility as a complete cycle test.
- Retain: a uniform missing prime-power theorem coupled to an aperiodic
  descent argument.
- Next lemma: `UniformPrimePowerDeficitOrUniversalAperiodicDescent`.

## 3. Strong Goldbach conjecture

### Declared proposition

For an integer cutoff `z`, define `Q_z(m)` by exact primality testing when
`m<=z`, and for `m>z` by

```text
Q_z(m)=1 iff no prime p<=z divides m.
```

If `z>=sqrt(X)`, then for every `2<=m<=X`,

```text
Q_z(m)=1 iff m is prime.                              (GB-224.1)
```

Consequently, for every even `N<=X`, the ordered convolution of `Q_z` at
`N` is exactly the ordered Goldbach representation count.

No arbitrary fixed cutoff has this property at all larger scales. Given
primes `r,s>z`, set `m=rs` and `N=2m`. Then `Q_z(m)=1` although `m` is
composite, so the filtered convolution contains the false diagonal `(m,m)`
and strictly exceeds the prime convolution.

### Proof

Every composite `m<=X` has a prime divisor at most
`sqrt(m)<=sqrt(X)<=z`. If `m>z`, the wheel rejects it; if `m<=z`, the exact
small-value clause rejects it. Every prime is accepted. This proves
`(GB-224.1)` and convolution equality.

Conversely, no prime at most `z` divides `rs` when `r,s>z`. The filter accepts
every prime representation and additionally accepts `(rs,rs)` at target
`2rs`, proving strict overcount.

### Reproducible calculation

For `X=100, 1000, 10000, 100000`, the ceiling square-root filter is compared
with exact primality on every integer through `X`; all four mismatch counts
are zero. For cutoffs `3,5,7,11,17,29`, explicit semiprime diagonals produce
strict filtered-count excesses.

### Limit, route decision, and next lemma

Square-root trial division is an exact finite algorithm, not an all-`N`
Goldbach proof. It consumes complete bounded primality information. The
research objective is to prove positivity using less than this complete
factor depth.

- Discard: identifying a fixed or incomplete wheel convolution with the
  prime convolution.
- Retain: a uniform prime-weighted error estimate below the positive local
  margin at a sub-square-root level.
- Next lemma:
  `SubSquareRootPrimeWeightedGoldbachRemainderBelowUniformLocalMargin`.

## 4. Twin-prime conjecture

### Declared proposition

With the same filter, if `z>=sqrt(X)` and `n+2<=X`, then

```text
Q_z(n)Q_z(n+2)=1
  iff n and n+2 are both prime.                       (TP-224.1)
```

For every fixed `z`, there are infinitely many larger false positives. Let
`W` be the product of primes at most `z`, choose `a mod W` avoiding `0` and
`-2` at every prime, and choose distinct primes `r,s>z`. CRT solves

```text
n = a  (mod W),
n = 0  (mod r),
n = -2 (mod s).
```

Every sufficiently large member of the resulting progression passes both
`Q_z` filters but has both entries composite.

### Proof

Statement `(TP-224.1)` follows by applying `(GB-224.1)` to both entries.
The CRT moduli are pairwise coprime. The first congruence supplies the full
wheel-survivor signature; the second and third supply proper factors outside
the wheel. Adding arbitrary multiples of `Wrs` gives infinitely many such
pairs.

### Reproducible calculation

The same four square-root exactness rows have zero mismatches. Six cutoffs
produce explicit CRT composite pairs, including `215,217` for `z=3` and
`2891,2893` for `z=5`. Each witness is above its factor and square-root
threshold and passes the incomplete filter.

### Limit, route decision, and next lemma

Exact bounded filtering cannot imply that successful candidates occur
infinitely often. Below complete square-root information, the CRT mass must be
separated from the prime-pair mass by genuinely analytic information.

- Discard: sub-square-root wheel survival as a twin-primality certificate.
- Retain: a uniform Type-II or bilinear estimate that removes the composite
  countermodel mass while preserving a positive gap-two main term.
- Next lemma: `UniformSubSquareRootTypeIIBilinearSeparationForGapTwo`.

## Cross-track conclusion

The four exact thresholds are different manifestations of the same logical
rule:

1. an RH band sign is certified only when signal exceeds the optimal tail;
2. Collatz divisibility is certified only when all prime multiplicities are
   retained;
3. Goldbach and Twin finite filters are exact after complete square-root
   factor information;
4. below a completeness threshold, explicit adversarial objects survive.

The new theorems improve proof hygiene and identify where new mathematics is
needed. They do not establish a zero-free theorem, every-orbit descent,
all-even Goldbach representation, or infinitely many twin primes.

## Literature boundary

- Connes and Consani, [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368), motivates semi-local RH observables. The quarter-kernel theorem here is elementary and is not an RH criterion.
- Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562), marks the almost-all versus every-orbit boundary.
- Oliveira e Silva, Herzog, and Pardi, [Empirical verification of the even Goldbach conjecture](https://doi.org/10.1090/S0025-5718-2013-02787-1), gives a much larger finite verification boundary.
- Ford and Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368), explains the need for substantial Type-I/Type-II information.

No literature-priority claim is made for the elementary optimization,
factorization criterion, square-root sieve identity, or CRT constructions.

## Reproduction

```powershell
python scripts/ticket224_sharp_completeness_thresholds.py
python -m unittest tests.test_ticket224_sharp_completeness_thresholds -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Primary machine-readable artifact:

`data/open-problem/ticket224-sharp-completeness-thresholds.json`
