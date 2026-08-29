# TICKET-255: aggregate packets, incomplete recovery, odd reflection, and a three-prime Thue obstruction

## Claim boundary

TICKET-255 proves four project-local auxiliary statements. It does **not** prove
or disprove the Riemann hypothesis, Collatz conjecture, strong Goldbach
conjecture, or twin-prime conjecture. The resolution count remains `0 / 4`.
The deep-focus track is the exponent-17 Diophantine obstruction inside the
twin-prime proxy audit.

The exact replay is:

```text
python scripts/ticket255_aggregate_incomplete_odd_local.py
python -m unittest tests.test_ticket255_aggregate_incomplete_odd_local -v
python scripts/verify_ticket255_structure.py
python -m unittest discover -s tests
python scripts/verify_open_problem_structure.py
node --check assets/ticket255-open-problem.js
node --check assets/open-problems.js
```

All theorem certificates use integer or `Fraction` arithmetic. There is no
random seed and no floating-point value is used as proof. The JSON
`display_float` fields are presentation-only.

| Problem | Declared proposition | Classification | Parent status |
|---|---|---|---|
| RH | `StrictDiagonalDominanceNecessityNoGo` | `exact_no_go` | `open_not_proven` |
| Collatz | `IncompleteAdditiveCharacterExactRecoveryNoGo` | `exact_no_go` | `open_not_proven` |
| Strong Goldbach | `OddCyclotomicReflectionPrimePrefixExclusion` | `partial_theorem` | `open_not_proven` |
| Twin Prime | `ThreePrimeLocalObstructionReducesSeventeenTwistsToTwo` | `partial_theorem` | `open_not_proven` |

## 1. Riemann hypothesis track

### A. Exact proposition

For every integer `L >= 3`, let `J_L` be the all-ones matrix and

```text
A_L = J_L + I_L / L.
```

Then `A_L` is positive definite and the normalized all-ones packet `d_L`
satisfies

```text
<d_L, A_L d_L> = L + 1/L > 0,
```

but `A_L` is not strictly diagonally dominant because
`1 + 1/L <= L - 1`. Thus strict diagonal dominance is not necessary for
positive Dirichlet-packet energy, even in the positive-definite class.

### B-D. Definitions and proof

`J_L` has eigenvalue `L` on the all-ones line and eigenvalue `0` on its
orthogonal complement. Hence the spectrum of `A_L` is
`{L+1/L, 1/L}`, so it is positive definite. Its diagonal is `1+1/L`; the
absolute off-diagonal row sum is `L-1`. The inequality holds for every
`L >= 3`, while `d_L` is the first eigendirection.

### E-G. Adversarial replay and interpretation

Eight rational blocks `L=3,5,7,9,15,31,63,127` replay the two eigenvalues,
row sums, failure of strict dominance, and positive packet energy. All eight
certificates pass. This is a counterexample to *necessity*, not to the claim
that actual Weil blocks might happen to satisfy strict dominance.

### H-K. Limit, classification, gap, next lemma

The actual Guinand-Weil matrix entries were not computed. The TICKET-254
strict-dominance target is therefore retired only as a mandatory bridge and
parked as a possible sufficient certificate. Classification: `exact_no_go`.
The remaining gap is a direct lower bound for the actual packet Rayleigh
quantity. Next single lemma:

```text
ActualWeilDirichletPacketAggregateRowSumHasRequiredLowerBound
```

Transcript SHA-256:
`2ba4e6b1090ad6d74f803dc96b1762f0e0cf5057bd0f11f12ee81036d8b99493`.

## 2. Collatz track

### A. Exact proposition

Let `q` be prime and `H` a proper subset of `F_q`. There are no complex
coefficients `a_h` such that, for every `D in F_q`,

```text
1_(D=0) = sum_(h in H) a_h exp(2 pi i hD/q).
```

Thus arbitrary signs do not permit exact pointwise slope-incidence recovery
from genuinely incomplete additive-character support.

### B-D. Definitions and proof

The `q` additive characters form an orthonormal basis for functions on
`F_q`. Every Fourier coefficient of the point mass at zero is `1/q`. Choose
`h0` outside `H`. An `H`-supported sum has coefficient zero at `h0`, a direct
contradiction to `1/q`. This proof allows arbitrary complex coefficients, so
changing nonnegative weights to signed weights does not repair exact recovery.

### E-G. Adversarial replay and interpretation

For each of twelve primes from `7` through `47`, four proper supports are
checked exactly: all nonzero frequencies, a lower half-band, quadratic
residues, and zero alone. The resulting 48 certificates record a missing
frequency and compare exact coefficients `1/q` and `0`. All pass.

### H-K. Limit, classification, gap, next lemma

The theorem does not block approximation, one-sided majorants, or equality
only at the canonical Fermat-quotient residue. It therefore retires exact
pointwise incomplete recovery but not a controlled-error signed kernel.
Classification: `exact_no_go`. Next single lemma:

```text
SignedIncompleteSlopeKernelHasControlledCanonicalErrorAndCrossPrimeCancellation
```

Transcript SHA-256:
`cc49768b5030292430f99a91e8eef1047ac66704a68a859ea1e06cd4b86a9293`.

## 3. Strong Goldbach track

### A. Exact proposition

Let `q >= 5` be prime and let `m` be odd with `q` not dividing `m`. Define

```text
c_r = sum_(0<=j<=m, j congruent r mod q) (-1)^j binom(m,j).
```

Assume `t=1-c_0>0` and `c_r+t>=0` for every residue, and put `T=qt`. Let
`lambda_q(r,k)` denote the global prime index of the `k`th prime congruent to
`r mod q`. The unique candidate prefix count at `r=m mod q` is `2t-1`.
If

```text
T < lambda_q(m mod q, 2t-1),
```

then the tail cannot be the actual first-`T`-prime residue vector.

### B-D. Definitions and proof

For `a_j=(-1)^j binom(m,j)`, the involution `j -> m-j` gives
`a_(m-j)=-a_j`. After cyclic folding,

```text
c_(m-r) = -c_r.
```

Taking `r=0` gives `c_(m mod q)=-c_0`, so its shifted target count is
`-c_0+(1-c_0)=2t-1`. If `T` lies strictly before the corresponding residue
prime occurrence, the actual prefix count is at most `2t-2`, contradicting
the TICKET-253 unique-prefix criterion.

### E-G. Exact finite certificates

The generator scans 480 odd `(q,m)` pairs with
`q in {5,7,11,13,17,19}` and `1<=m<=160`. Fifty are compatible,
non-`q`-divisible rows. Exact prime enumeration is deliberately capped at
`T<=50,000`; four rows qualify:

| `(q,m)` | `t` | `T` | forced count | actual count | `lambda` index | result |
|---|---:|---:|---:|---:|---:|---|
| `(5,9)` | 126 | 630 | 251 | 153 | 1,014 | excluded |
| `(5,11)` | 451 | 2,255 | 901 | 561 | 3,633 | excluded |
| `(7,13)` | 1,716 | 12,012 | 3,431 | 2,000 | 20,566 | excluded |
| `(7,15)` | 6,420 | 44,940 | 12,839 | 7,464 | 77,008 | excluded |

### H-K. Limit, classification, gap, next lemma

The other 46 compatible rows exceed the replay cap; they are not declared
excluded by computation. The algebraic implication remains valid whenever
its exact threshold is separately certified. Exponents divisible by `q` are
untouched. Classification: `partial_theorem`. Next single lemma:

```text
QDivisibleCompatibleTailPrimePrefixExclusion
```

Transcript SHA-256:
`ab8cb879f9a4dbdc1825584e054a56687f770fc0b6c3a40f939be7f06dc2b3fb`.

## 4. Twin-prime track: deep focus

### A. Exact proposition

For the seventeen TICKET-254 equations `B_j(u,v)=1`, local reduction at
`p=103,137,409` excludes every twist except `j=1,16`. Their zero-solution
sets are respectively

```text
{0,3,6,7,8,9,10,11,14}
{0,4,5,7,8,9,10,12,13}
{0,2,15}.
```

Consequently any positive solution of `x^2-2=y^17` must arise from twist
`1` or `16`.

### B-D. Split-ring proof

For each prime, choose `s^2=2 mod p`: the least roots are `38,31,97`.
The map

```text
u+v sqrt(2) -> (z_+,z_-)=(u+sv,u-sv)
```

is a bijection because `2s` is invertible. With
`epsilon_+=1+s`, `epsilon_-=1-s`, coefficient one is equivalent to

```text
epsilon_+^j z_+^17 - epsilon_-^j z_-^17 = 2s.
```

An exact multiplicity convolution of the seventeenth-power residues gives all
`p^2` solution counts for each twist. The three obstructed sets cover fifteen
twists and the soluble-set intersection is exactly `{1,16}`.

### E-G. Independent adversarial check and no-go boundary

The split convolution represents `3,343,203` `(u,v,j)` residue cases. An
independent direct enumeration of all `103^2*17` cases reproduces the first
solution-count vector. The two survivors cannot be removed by any congruence
test of `B_j=1` alone because there are exact global integer witnesses:

| `j` | `(u,v)` | `A_j` | `B_j` | reduced `y` | admissible? |
|---:|---|---:|---:|---:|---|
| 1 | `(1,0)` | 1 | 1 | -1 | no |
| 16 | `(-1,1)` | -1 | 1 | -1 | no |

This is an exact no-go for coefficient-only congruence completion, embedded
inside the partial reduction theorem.

### H-K. Limit, classification, gap, next lemma

Local insolubility removes fifteen Thue equations globally, but local
solubility never proves an integral point. Neither surviving equation has been
globally solved under `A_j>0` and reduced `y>0`. Hence exponent 17, the
right-even contamination problem, and the twin-prime conjecture all remain
open. Classification: `partial_theorem`. Next single lemma:

```text
TwoSurvivingUnitTwistsHaveNoAdmissibleIntegralPoint
```

Transcript SHA-256:
`3d89ca8e3ca658a6bff44a8e532a441a2be41ac89c5d8d46b2af84d8c84a6a63`.

## Proof-DAG and resolution audit

Each problem has an acyclic DAG with the TICKET-254 predecessor, the new
proved node, an exact finite replay node, one disproved route claim, and one
open frontier. The Twin theorem depends on its finite split-prime certificate;
the other universal theorems imply their finite replays. No `assumption` or
`heuristic` node lies on a claimed resolution path. Every parent status is
`open_not_proven`, `iteration_complete=true`, and `program_complete=false`.
