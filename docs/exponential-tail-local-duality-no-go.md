# TICKET-223: Exponential Tails, Local Duality, and Fixed-Sieve No-Go Results

## Status and claim boundary

TICKET-223 continues the four-track open-problem program from TICKET-222.
It proves four exact bounded statements and resolves none of the parent
conjectures.

| Track | Exact result | Parent status |
|---|---|---|
| Riemann hypothesis | Exponential-tail dyadic injectivity and a uniform cofinal truncation bound | Open |
| Collatz conjecture | A primitive false positive for every fixed modular cycle sieve whose moduli are coprime to six | Open |
| Strong Goldbach conjecture | A uniform positive finite-wheel local margin | Open |
| Twin-prime conjecture | Infinitely many composite-pair countermodels for every fixed wheel | Open |

The Goldbach local margin and the twin-wheel survivor density are the same
finite Euler product. This is the main cross-track synthesis. It is a local
identity, not a transfer theorem between the two conjectures.

## 1. Riemann hypothesis

### Declared proposition

Let `sigma` be a finite signed Borel measure supported on `[a,infinity)`, where
`a>0`, and suppose

```text
integral exp(eta t) d|sigma|(t) < infinity
```

for some `eta>0`. Define

```text
L_sigma(s) = integral exp(-s t) d sigma(t),
W_j = L_sigma(2^(-j)) - L_sigma(2^(1-j)).
```

If `W_j=0` for every integer `j`, then `sigma=0`. If `sigma_T` is the
restriction to `[a,T]`, then every dyadic band satisfies

```text
|W_j(sigma) - W_j(sigma_T)|
  <= exp(-eta T) integral exp(eta t) d|sigma|(t),
```

uniformly in `j`.

### Proof

The exponential total-variation moment makes `L_sigma` holomorphic in the
open half-plane `Re(s)>-eta`. The band equations imply

```text
L_sigma(2^(-j)) = L_sigma(2^(1-j)),
```

so every dyadic sample has the same value. As `j` tends to minus infinity,
the sample point tends to infinity. Support above `a>0` forces the Laplace
transform to tend to zero there. Hence all dyadic samples vanish.

The sample points accumulate at `s=0`. Unlike the compact-only argument in
TICKET-222, zero is now an interior point of the holomorphy domain because of
the exponential moment. The identity theorem therefore gives
`L_sigma identically zero`; uniqueness of the Laplace transform gives
`sigma=0`.

For the cofinal truncation, Markov's inequality for the weighted variation
gives

```text
|sigma|([T,infinity))
  <= exp(-eta T) integral exp(eta t) d|sigma|(t).
```

The absolute value of the band kernel is at most one, proving the uniform
bound.

### Reproducible calculation

The audit uses the unbounded atomic model

```text
t_n = n,
w_n = (-1)^n 4^(-n),
eta = log(2).
```

Its weighted norm is exactly one. Closed geometric tails are evaluated for
six cutoffs and nineteen dyadic scales. Every observed band tail lies below
both the exact total-variation tail and the theorem's exponential bound.

### Limit and route decision

This theorem closes an abstract analytic tail step. It does not construct an
RH-equivalent zeta-zero defect measure with the required exponential moment,
and it does not enclose the corresponding bands from prime-side data.

- Discard: the assertion that compact support is essential for complete
  dyadic-profile injectivity.
- Retain: an RH-equivalent weighted defect whose dyadic bands have rigorous
  prime-side representations.
- Next lemma:
  `RHEquivalentExponentiallyWeightedDefectWithPrimeSideDyadicBands`.

## 2. Collatz conjecture

### Declared proposition

Fix any integer `M>1` coprime to six. Let

```text
r = ord_M(2),
h = ord_M(4 * 3^(-1)),
a = (2+r, 2, ..., 2) of length h.
```

For the accelerated Collatz word, put

```text
S = sum a_i,
D = 2^S - 3^h,
B = sum_i 3^(h-i) 2^(a_1+...+a_(i-1)).
```

Then `a` is primitive and non-all-two, `M` divides both `D` and `B`, but

```text
0 < B < D.
```

Consequently `D` does not divide `B`; this word is a provable non-cycle that
passes the fixed modular test. Replacing `M` by the least common multiple
gives one simultaneous false positive for every finite fixed family of
moduli coprime to six.

### Proof

Every exponent in the word is congruent to two modulo `r`. Thus

```text
2^S = 2^(2h+r) = 4^h 2^r = 4^h (mod M),
```

and the definition of `h` gives `4^h=3^h (mod M)`. Hence `M|D`.

Every prefix power in `B` is congruent to the corresponding all-two prefix,
so

```text
B = sum_i 3^(h-i)4^(i-1)
  = 4^h - 3^h
  = 0 (mod M).
```

Here the displayed equality is a congruence for the constructed word. Exact
summation, retaining the enlarged first exponent, gives

```text
D - B = 4(2^r - 1)3^(h-1) > 0.
```

The single enlarged entry also prevents the word from being a repetition of
a shorter block. Therefore it is primitive and nontrivial.

### Reproducible calculation

The construction is checked for all 66 integers `M` between 5 and 199 that
are coprime to six. Three least-common-multiple families are also checked.
Every witness satisfies the two modular tests, the closed gap formula, and
`0<B<D`; none satisfies exact cycle divisibility.

### No-go result and route decision

No finite fixed modular sieve on `(D,B)` whose moduli are coprime to six can
exclude every nontrivial primitive valuation word. This does not rule out
code-adaptive moduli,
Archimedean bounds, or descent arguments for aperiodic trajectories.

- Discard: a finite fixed list of congruence tests as a complete Collatz cycle
  proof.
- Retain: a large-prime obstruction whose modulus grows with the code, or a
  universal first-descent theorem.
- Next lemma:
  `CodeAdaptiveLargePrimeObstructionOrUniversalAperiodicDescent`.

## 3. Strong Goldbach conjecture

### Declared proposition

Let `W` be a squarefree product of odd primes. Let `A_W(N)` count residues
`a modulo W` for which both `a` and `N-a` are coprime to `W`. Then

```text
A_W(N)
 = product_(p|W,p|N) (p-1)
   product_(p|W,p not|N) (p-2).
```

Normalize by the independent coprime density `(phi(W)/W)^2`. Then

```text
(A_W(N)/W) / (phi(W)/W)^2 >= C_W,
C_W = product_(p|W) p(p-2)/(p-1)^2.
```

Equality holds exactly when `gcd(N,W)=1`. The finite products `C_W` are
bounded below by the positive infinite odd-prime product `C_*`.

### Proof

For each odd prime `p|W`, the forbidden residues are `0` and `N`. They
coincide if `p|N`, leaving `p-1` admissible residues; otherwise they are
distinct, leaving `p-2`. CRT multiplies these counts.

After normalization, the local factor is

```text
p/(p-1)                  if p|N,
p(p-2)/(p-1)^2           if p does not divide N.
```

The first is strictly larger, giving the floor and equality condition. Since

```text
1 - p(p-2)/(p-1)^2 = 1/(p-1)^2
```

and the sum of these deficits converges, the infinite product is positive.

### Reproducible calculation

For `W=3*5*7*11=1155`, all target residues and all candidate residues are
enumerated exactly. The minimum normalized ratio is

```text
693/1024,
```

and it occurs in exactly `phi(W)` target classes, precisely the classes
coprime to `W`. Exact prefix products are also generated through prime 43.

### Limit and route decision

This closes local congruence admissibility with a uniform normalized margin.
It does not bound the prime-weighted minor-arc or global remainder, so it does
not prove even one new cofinal Goldbach range.

- Discard: searching for a finite local congruence obstruction to even
  Goldbach targets.
- Retain: prove that the global prime-weighted remainder is strictly smaller
  than the uniform local main term.
- Next lemma:
  `PrimeWeightedGoldbachRemainderStrictlyBelowUniformLocalMargin`.

## 4. Twin-prime conjecture

### Declared proposition

Fix a finite squarefree odd wheel `W` and a survivor residue `a` that avoids
`0` and `-2` modulo every prime dividing `W`. There are infinitely many
`n=a (mod W)` for which both `n` and `n+2` are composite.

Choose distinct primes `r,s` not dividing `W` and solve

```text
n = a  (mod W),
n = 0  (mod r),
n = -2 (mod s).
```

CRT gives an infinite arithmetic progression. Every sufficiently large member
is a proper multiple of `r`, while its shift by two is a proper multiple of
`s`.

The normalized wheel-survivor density is

```text
(product_(p|W)(p-2)/W) / (phi(W)/W)^2
 = product_(p|W) p(p-2)/(p-1)^2
 = C_W.
```

This is exactly the minimum normalized Goldbach local factor.

### Reproducible calculation

Explicit composite-pair progressions are constructed for thirteen wheel
prefixes through prime 43. Every witness has the all-survivor wheel signature,
while prescribed external primes divide the two shifted values.

### No-go result and route decision

A fixed wheel can have a nonzero biased parity signal, as shown in TICKET-222,
but that signal cannot certify twin primality. Composite pairs reproduce the
same complete fixed-wheel signature.

- Discard: any fixed finite-wheel signature as a twin-prime certificate.
- Retain: wheel or Type-I/II information growing with the search scale, with a
  remainder bound uniform in that growth.
- Next lemma:
  `ScaleGrowingWheelSignalWithUniformTypeIIRemainderDominance`.

## Cross-track conclusion

The finite Euler product `C_W` has two exact meanings:

1. the worst normalized local Goldbach convolution density;
2. the normalized twin-pair wheel-survivor density.

This identifies a shared local arithmetic geometry. It also isolates the
shared failure: local admissibility does not control prime-weighted global
correlation. The Goldbach and twin-prime tracks now meet at a common analytic
remainder problem, but neither conjecture follows from the identity.

## Literature boundary

- Connes and Consani's semi-local operator framework motivates coupled RH
  observables; TICKET-223's Laplace theorem is elementary and is not an RH
  criterion: <https://arxiv.org/abs/1910.14368>.
- Tao proves an almost-all Collatz descent statement, revised through v7 in
  2026; it does not imply every-orbit descent:
  <https://arxiv.org/abs/1909.03562>.
- The published Goldbach verification through `4*10^18` is much stronger than
  this finite replay: <https://doi.org/10.1090/S0025-5718-2013-02787-1>.
- Ford and Maynard explain why substantial Type-II information is necessary
  for nontrivial prime-producing lower bounds:
  <https://arxiv.org/abs/2407.14368>.

No literature-priority claim is made for the elementary identities or CRT
constructions in this ticket.

## Reproduction

```powershell
python scripts/ticket223_exponential_tail_local_duality_no_go.py
python -m unittest tests.test_ticket223_exponential_tail_local_duality_no_go -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Primary machine-readable artifact:

`data/open-problem/ticket223-exponential-tail-local-duality-no-go.json`
