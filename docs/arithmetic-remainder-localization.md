# TICKET-225: Arithmetic Remainder Localization

## Status and claim boundary

TICKET-225 continues the four proof DAGs from TICKET-224. It replaces four
coarse open remainders by explicit arithmetic objects: a von Mangoldt tail, a
cyclic Collatz gcd quotient, and cube-root rough-semiprime contamination for
Goldbach and Twin Prime. It proves no parent conjecture.

| Track | Exact result | Refuted or limited route | Parent status |
|---|---|---|---|
| Riemann hypothesis | Computable tail interval for an actual von Mangoldt Laplace band; finite-band noninjectivity | Finitely many prime-band signs form an RH criterion | Open |
| Collatz conjecture | The quotient `D/gcd(D,B)` is invariant under cyclic rotation | Rotations accumulate independent prime-power deficits | Open |
| Strong Goldbach conjecture | At cube-root sieve depth, every surviving composite is exactly a rough semiprime; exact four-term convolution split | Every cube-root wheel representation is prime-prime | Open |
| Twin-prime conjecture | Exact `PP/PS/SP/SS` classification of cube-root survivor pairs | Every cube-root survivor pair certifies twin primality | Open |

The common advance is localization, not resolution. Each previously unnamed
error is turned into a concrete term that a future proof must control.

## 1. Riemann hypothesis

### Declared proposition

For `a>0`, define the actual prime-side Laplace-band defect

```text
P(a) = sum_(n>=2) Lambda(n)[exp(-an)-exp(-2an)] - 1/(2a).
```

For every integer `N>=2`, put `q=exp(-a)`. The omitted prime contribution is
nonnegative and satisfies

```text
0 <= sum_(n>N) Lambda(n)[q^n-q^(2n)]
   <= q^(N+1)((N+1)-Nq)/(1-q)^2.                 (RH-225.1)
```

Thus the finite von Mangoldt sum and `(RH-225.1)` give an explicit interval
containing the full band. However, any finite set of band functionals has a
nonzero finitely supported signed measure in its common kernel. Therefore a
finite list of band values or signs cannot identify an arbitrary signed
defect measure and is not an RH criterion.

### Proof

The subtracted main term is exact because

```text
integral_0^infinity [exp(-ax)-exp(-2ax)] dx = 1/(2a).
```

For every integer `n>=2`,

```text
0 <= exp(-an)-exp(-2an) <= exp(-an),
Lambda(n) <= log n <= n.
```

The tail is therefore bounded by `sum_(n>N)nq^n`. Differentiating the
geometric series yields the closed form in `(RH-225.1)`.

For the finite-family no-go, evaluate `m` chosen band functionals on `m+1`
distinct atoms. This is a linear map from `R^(m+1)` to `R^m`, so rank-nullity
provides a nonzero signed atomic measure annihilated by every observed band.
This argument does not assert that every extra band also vanishes; it proves
that the finite observations are not injective.

### Reproducible calculation

The calculator evaluates dyadic scales `a=2^-j`, `j=3,...,15`, truncating at
`N=48*2^j`. All 13 finite sums remain negative after adding the explicit
positive tail bound. Six matrices with three through eight observed bands
and one more atom than observations have full row rank numerically and a
nonzero null vector with residual below `10^-10`.

These are finite numerical sign certificates for this prime-side observable.
They are not interval-arithmetic verification of zeta zeros and are not an RH
proof.

### Limit, route decision, and next lemma

- Discard: treating finitely many actual prime-band signs as an RH criterion.
- Retain: transfer cofinal prime-band inequalities through the explicit
  formula to positivity on a dense Weil test-function core.
- Missing implication: no theorem currently maps the certified signs to the
  full Weil quadratic form or excludes an off-critical zero.
- Next lemma:
  `ExplicitFormulaTransferFromCofinalPrimeBandMarginsToWeilCorePositivity`.

## 2. Collatz conjecture

### Declared proposition

Let `a=(a_1,...,a_h)` be a positive accelerated Collatz valuation word,

```text
S = sum a_i,
D = 2^S - 3^h > 0,
```

and let `B_i` be the affine intercept of its `i`th cyclic rotation. Then
consecutive rotations satisfy

```text
2^(a_i) B_(i+1) = 3B_i + D.                         (CO-225.1)
```

Consequently,

```text
gcd(D,B_i) = gcd(D,B_(i+1))
```

and the residual obstruction `R=D/gcd(D,B_i)` is invariant around the whole
cycle. If one rotation has `0<B_i<D`, the word cannot encode a cycle.

### Proof

Write the first intercept as

```text
B_i = 3^(h-1) + 2^(a_i) C,
```

where `C` is the suffix intercept. After moving `a_i` to the end,

```text
B_(i+1) = 3C + 2^(S-a_i).
```

Multiplication by `2^(a_i)` gives

```text
2^(a_i)B_(i+1)
  = 3(B_i-3^(h-1)) + 2^S
  = 3B_i + D.
```

The odd integer `D=2^S-3^h` is coprime to both 2 and 3. Taking gcd with `D`
proves invariance. TICKET-222's exact condition says a cycle requires `D|B_i`;
therefore a positive intercept smaller than `D` is a noncycle certificate.

### Reproducible calculation

All words of heights `2..7` over `{1,2,3,4,5}` were enumerated. Among 97,016
primitive words with `D>0`, 655,188 consecutive-rotation identities and all
gcd invariance checks had zero failures. The minimum-intercept test certifies
96,127 of these words as noncycles. No nontrivial cycle was found, but 889
words remain unresolved by that sufficient test.

For the TICKET-224 witness `(1,1,2,4,3)`, every rotation has

```text
gcd(D,B_i)=95,  D/gcd(D,B_i)=19.
```

Hence rotating the word does not reveal independent missing prime powers.

### Limit, route decision, and next lemma

- Discard: treating rotations as independent prime-power deficit samples.
- Retain: use the smallest cyclic intercept as a global cycle obstruction,
  while treating aperiodic trajectories separately.
- Missing implication: no uniform proof shows `min_i B_i<D` for every
  nontrivial primitive word, and no aperiodic descent theorem follows.
- Next lemma: `UniformCyclicInterceptDescentOrAperiodicOrbitDescent`.

## 3. Strong Goldbach conjecture

### Declared proposition

Let `z^3>=X`. Define `Q_z(m)` to accept primes and numbers having no prime
divisor at most `z`. Every accepted composite `m<=X` is exactly

```text
m = r*s,  r and s prime, r>z, s>z,
```

with multiplicity allowed. Let `P` be the prime indicator and `S_z` this
rough-semiprime indicator. Then on `[2,X]`,

```text
Q_z = P + S_z.                                      (GB-225.1)
```

For every even `N<=X`, ordered convolution gives the exact decomposition

```text
Q_z*Q_z(N)
 = P*P(N) + P*S_z(N) + S_z*P(N) + S_z*S_z(N).      (GB-225.2)
```

### Proof

All prime factors of an accepted composite exceed `z`. If it had at least
three prime factors, counting multiplicity, then `m>z^3>=X`, a contradiction.
It therefore has exactly two. Conversely, a product of two primes above `z`
has no sieving prime divisor. This proves `(GB-225.1)`. Expanding
`(P+S_z)*(P+S_z)` proves `(GB-225.2)`.

### Reproducible calculation

The complete classification was checked for `X=1,000`, `10,000`, and
`100,000`, with zero factorization or classification mismatches. At target
`N=X`, the ordered counts are:

| `X` | `P*P` | `P*S` | `S*P` | `S*S` | filtered total |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 56 | 19 | 19 | 4 | 98 |
| 10,000 | 254 | 118 | 118 | 34 | 524 |
| 100,000 | 1,620 | 759 | 759 | 294 | 3,432 |

Explicit rough-semiprime diagonals verify that an individual filtered witness
need not be prime-prime.

### Limit, route decision, and next lemma

- Discard: reading every cube-root wheel representation as prime-prime.
- Retain: bound the three explicit rough-semiprime convolutions below the
  filtered main term.
- Missing implication: the identity gives no uniform all-even bound proving
  `P*P(N)>0`.
- Next lemma:
  `UniformCubeRootRoughSemiprimeErrorBelowGoldbachWheelMainTerm`.

## 4. Twin-prime conjecture

### Declared proposition

Under `z^3>=X`, each gap-two survivor pair `(n,n+2)`, `n+2<=X`, belongs to
exactly one type:

```text
PP, PS, SP, SS,
```

where `P` means prime and `S` means `z`-rough semiprime. Consequently,

```text
survivor pairs = PP + PS + SP + SS.                 (TP-225.1)
```

Only `PP` counts twin primes. A positive survivor count or a termwise wheel
certificate is therefore not itself a twin-prime certificate.

### Proof

Apply `(GB-225.1)` independently to `n` and `n+2`. The four types are
disjoint and exhaustive, so their indicators and counts add exactly.
Explicit `SS` pairs show that both filter decisions can be positive while
both integers are composite.

### Reproducible calculation

| `X` | `PP` | `PS` | `SP` | `SS` | first `SS` pair |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 35 | 19 | 14 | 4 | `(527,529)` |
| 10,000 | 205 | 78 | 76 | 35 | `(1679,1681)` |
| 100,000 | 1,224 | 559 | 537 | 253 | `(4187,4189)` |

Every listed pair was factored and verified as two rough semiprimes.

### Limit, route decision, and next lemma

- Discard: treating a cube-root survivor pair as a twin-prime certificate.
- Retain: prove a positive `PP` lower bound after controlling all three
  contamination classes.
- Missing implication: no uniform asymptotic control of `PS+SP+SS` and no
  unbounded lower bound for `PP` is proved.
- Next lemma:
  `PositiveTwinPrimeLowerBoundAfterCubeRootSemiprimeContaminationControl`.

## Cross-track conclusion

TICKET-225 changes the open obligations from qualitative labels to explicit
remainders:

1. RH needs an explicit-formula transfer, not more isolated band signs.
2. Collatz rotations share one gcd residual, so useful new information must
   come from a uniform size inequality or aperiodic descent.
3. Goldbach's cube-root sieve error is exactly three rough-semiprime
   convolutions.
4. Twin Prime's cube-root parity obstruction is exactly `PS+SP+SS`.

These are exact partial theorems and route-pruning results. They do not prove
RH, Collatz, strong Goldbach, or infinitely many twin primes.

## Literature boundary

- Connes and Consani, [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368), supplies context for semi-local RH observables; `(RH-225.1)` is not their RH criterion.
- Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562), marks the unresolved gap between almost-all and every-orbit descent.
- Ford and Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368), provides current context for Type-I/Type-II information and parity barriers.

No literature-priority claim is made for the elementary tail bound, cyclic gcd
identity, cube-root rough-semiprime classification, or convolution expansions.

## Reproduction

```powershell
python scripts/ticket225_arithmetic_remainder_localization.py
python -m unittest tests.test_ticket225_arithmetic_remainder_localization -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Primary machine-readable artifact:

`data/open-problem/ticket225-arithmetic-remainder-localization.json`
