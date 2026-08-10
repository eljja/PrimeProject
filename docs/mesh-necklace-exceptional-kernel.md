# TICKET-204: Continuous Certificates, Primitive Necklaces, and Parity Kernels

## Claim status

All four parent conjectures remain `open_not_proven`. TICKET-204 proves four
intermediate theorems or no-go results. It proves or disproves none of the
Riemann, Collatz, strong Goldbach, or Twin Prime conjectures.

The canonical machine-readable artifact is
[`ticket204-mesh-necklace-exceptional-kernel.json`](../data/open-problem/ticket204-mesh-necklace-exceptional-kernel.json).

| Problem | Exact TICKET-204 result | Discarded route | Decisive next lemma |
|---|---|---|---|
| Riemann | A derivative-certified mesh promotes sampled relative error to a continuous Rouché bound; finite samples alone cannot | Unregularized finite contour sampling | `CompletedZetaCofinalAdaptiveRelativeDerivativeBound` |
| Collatz | Rotation and word powers preserve the affine cycle quotient, reducing periodic words to primitive necklaces | Counting rotations and repetitions as independent evidence | `UniformNondivisibilityForAllNonAllTwoPrimitiveValuationNecklaces` |
| Goldbach | A tail exceptional-count bound strictly below one closes the universal quantifier; density zero does not | Promoting density-zero or bounded exceptional sets to no exceptions | `ExplicitBinaryGoldbachTailExceptionalCountStrictlyBelowOne` |
| Twin Prime | PSD kernels cannot negatively weight every semiprime factor channel; an indefinite rank-two formal kernel escapes algebraically | PSD/square-form signed parity separation | `ArithmeticRealizationOfIndefiniteRankTwoSwitchingKernelWithUniformRemainder` |

## 1. Riemann hypothesis

### Declared proposition

Let a closed contour `Gamma` be parameterized by arclength `s`. Suppose `X`
and `P` are analytic on and inside `Gamma`, and `P` is nonzero on the contour.
Set

```text
r(s) = (X-P)/P.
```

Assume a finite sample set has covering radius `delta`, every sample satisfies
`|r| <= q`, and the full contour satisfies `|dr/ds| <= M`. Then

```text
sup_Gamma |r| <= q + M delta.
```

Consequently, `q+M delta<1` certifies the strict Rouché inequality and can be
fed into the zero-exhaustion theorem from TICKET-203.

### Proof

For any `s`, choose a sampled point `s_j` with arclength distance at most
`delta`. The fundamental theorem of calculus gives

```text
|r(s)| <= |r(s_j)| + integral_[s_j,s] |r'(u)| du
       <= q + M delta.
```

This estimate is deterministic and continuous; it is not a statistical
interpolation claim.

### Exact certificate regression

On the unit circle take

```text
P(z)=1,  X(z)=1+z^2/10,  r(z)=z^2/10.
```

For 16 equally spaced samples, `q=1/10`, `M=1/5`, and the covering radius is
at most `pi/16 <= 11/56`. Hence

```text
sup |r| <= 1/10 + (1/5)(11/56) = 39/280 < 1,
```

with certified Rouché margin at least `241/280`.

### Finite-sampling no-go

Finite samples without a regularity bound cannot certify the contour. On the
unit circle let

```text
P(z)=1,  X(z)=z^8,  r(z)=z^8-1.
```

At all eight sampled eighth roots of unity, `r=0`. At the intervening point
`z=exp(pi i/8)`, however, `|r|=2`. Moreover, `P` has zero interior zeros and
`X` has eight. A sample-only rule would therefore certify a false zero-count
transfer on this exact polynomial fixture.

### Remaining gap

No comparison function for the actual completed zeta function and no cofinal
bound for the derivative of `(Xi-P)/P` has been constructed. Rigorous finite
height verification, such as Platt and Trudgian's verification through height
`3*10^12`, does not by itself supply this cofinal analytic bound.

## 2. Collatz conjecture

### Declared proposition

For a positive accelerated valuation word `a=(a_0,...,a_(h-1))`, let

```text
B(a) = sum_m 3^(h-1-m) 2^P_m,
D(a) = 2^sum(a)-3^h,
P_m = a_0+...+a_(m-1).
```

If `rho(a)` is the left cyclic rotation, then

```text
2^a_0 B(rho(a)) = 3B(a)+D(a).
```

Since `D` is coprime to 2 and 3,

```text
D | B(a)  iff  D | B(rho(a)).
```

If `a=u^k`, where `u` has length `r` and valuation sum `s`, then

```text
B(a)=B(u)G,
D(a)=D(u)G,
G=sum_(j=0)^(k-1) 3^(r(k-1-j))2^(sj).
```

Thus the rational cycle value `B/D` and its integrality are unchanged by word
powers. Every periodic valuation candidate reduces exactly to one primitive
cyclic necklace.

### Proof

One accelerated step maps `x=B(a)/D` to `(3x+1)/2^a_0`, which is the cycle
value for the rotated word. Clearing the common denominator proves the
rotation identity. Iterating the affine map

```text
F_u(x)=(3^r x+B(u))/2^s
```

produces the same geometric factor `G` in the numerator and denominator,
proving the power identity.

### Reproducible audit

The exact audit enumerates valuations in `{1,2,3,4}`, lengths 2 through 8,
and positive `D`. It checks 86,439 raw words. Rotation identity failures and
power-factorization failures are both zero. Across the tested lengths, 11,445
cyclic necklaces reduce to 11,336 distinct primitive roots, removing 109
cross-length repetitions. The only divisible raw word at each tested length is
the all-two word; this last observation is finite evidence, not a theorem for
unbounded length.

### No-go and remaining gap

Rotations and powers cannot be counted as independent support for cycle
exclusion. The reduction addresses periodic words only. It does not prove
nondivisibility for every non-all-two primitive necklace and has no bearing on
nonperiodic divergent trajectories.

## 3. Strong Goldbach conjecture

### Declared proposition

Let `E(X)` be the integer number of even Goldbach exceptions up to `X`. If all
targets through `X_0` are verified and a rigorous tail estimate satisfies

```text
0 <= E(X)-E(X_0) < 1  for every X>=X_0,
```

then the tail count is the integer zero for every `X`, and strong Goldbach
follows.

### Exact threshold proof

The tail count is a nonnegative integer. The only such integer strictly below
one is zero. The strict inequality is essential. A model with exactly one
exception has `E(X)<=1` and `E(X)/X -> 0`, yet fails the universal statement.
A model with exceptions at powers of two has infinitely many exceptions while
also having density zero.

The no-go concerns logical promotion. Neither model is prime arithmetic and
neither is a Goldbach counterexample.

### Reproducible finite arithmetic

An exact sieve checks every even target through 10,000. It finds zero
exceptions. The smallest ordered representation count is one and the largest
through 10,000 is 658. This finite computation validates the implementation
only; it does not control the infinite tail.

### Remaining gap

Current exceptional-set estimates and a density-zero conclusion do not reach
the strict subunit threshold. The needed next result is an explicit tail bound
below one, or an equivalent pointwise major-arc/minor-arc dominance theorem.
The 2026 Grimmelt--Bhowmik work provides an explicit major-arc formula and a
survey of power-saving exceptional-set results, but does not establish the
subunit all-target bound used here.

## 4. Twin Prime conjecture

### Declared proposition

Let `K(a,b)` be a symmetric positive-semidefinite kernel on formal factor
labels. A strict signed separator that is negative on every semiprime channel
would require

```text
K(p,p)<0
```

for each prime square `p^2`. This contradicts the PSD diagonal constraint
`K(p,p)>=0`. Therefore a PSD or square-form bilinear kernel cannot strictly
separate primes from every `P_2` channel.

### Indefinite rank-two algebraic escape

On exposed factor pairs define

```text
s(1)=1,  s(p)=-1/2 for primes p,
K(a,b)=s(a)+s(b).
```

Then

```text
K(1,p)=1/2>0,
K(p,q)=-1<0.
```

The matrix is `s 1^T + 1 s^T`, so its rank is at most two. Its principal
minor on `{1,p}` is

```text
2(-1)-(1/2)^2 = -9/4,
```

which proves that the escape kernel is indefinite. The exact finite matrix on
labels `{1,2,3,5,7,11}` has rank two and the stated signs.

### No-go and remaining gap

The escape is purely algebraic and assumes that the factor pair is exposed.
It is not a function of `n` alone and does not provide a sieve decomposition,
a level of distribution, or a controlled switching remainder. Modern weighted
switching results show why bilinear factor structure matters, but they detect
almost-primes rather than proving a twin-prime lower bound. The next lemma must
realize an indefinite factor-channel kernel arithmetically with a uniform error
smaller than its positive main term.

## Reproduction

```bash
python scripts/ticket204_mesh_necklace_exceptional_kernel.py
python -m unittest tests.test_ticket204_mesh_necklace_exceptional_kernel
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

These sources establish context and known boundaries. No theorem in this
document is represented as a solution of a parent conjecture or as a
peer-reviewed novelty claim.
