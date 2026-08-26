# TICKET-247: Hilbert-Schmidt no-go, Hensel countermodels, arc Lipschitz transfer, and sharp prime-power contamination

## Status declaration

- `iteration_complete`: true
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- `new_partial_theorem_count`: 2
- `exact_no_go_count`: 2
- `stagnated_problem_count`: 0
- deep focus: Riemann hypothesis
- parent: TICKET-246
- program status: `open_not_proven`

This iteration proves four project-local auxiliary results. It proves or
disproves none of the Riemann hypothesis, Collatz conjecture, strong Goldbach
conjecture, or twin-prime conjecture. The machine record is
`data/open-problem/ticket247-hilbert-hensel-lipschitz-primepower.json`.

## Reproduction contract

```powershell
python scripts/ticket247_hilbert_hensel_lipschitz_primepower.py
python -m unittest tests.test_ticket247_hilbert_hensel_lipschitz_primepower -v
python scripts/verify_ticket247_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket247-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

All theorem-bearing computations use integers or `Fraction`. JSON floating
companions are display-only. The run is deterministic and has no random seed.

| Problem | new result | classification | status |
|---|---|---|---|
| Riemann | every Hilbert-Schmidt weighted even-moment feature map has zero lower coercivity on the full normalized even `L2` sphere | `exact_no_go` | `open_not_proven` |
| Collatz | the unrestricted all-prime valuation domination has a unique bad Hensel branch at every prime and depth | `exact_no_go` | `open_not_proven` |
| Strong Goldbach | exact center Parseval control extends to an arc with a prime-first-moment Lipschitz term, while center-only uniformity is impossible | `partial_theorem` | `open_not_proven` |
| Twin Prime | odd composite prime powers admit an exact exponent count and a sharper contamination correction | `partial_theorem` | `open_not_proven` |

## 1. Riemann hypothesis — deep focus

### A. Exact proposition: `HilbertSchmidtInfiniteMomentCoercivityNoGo`

Let

```text
H = L2_even([-1,1]),
w_k >= 0,
sum_(k>=0) 2 w_k/(4k+1) < infinity,
Q_w(f) = sum_(k>=0) w_k |integral_(-1)^1 x^(2k) f(x) dx|^2.
```

For every integer `n>=1`, let `P_(2n)` be the Legendre polynomial and put

```text
f_n = sqrt((4n+1)/2) P_(2n).
```

Then

```text
||f_n||_2 = 1,
integral x^(2k) f_n(x) dx = 0                    (0<=k<n),
Q_w(f_n) <= sum_(k>=n) 2 w_k/(4k+1) -> 0.
```

Hence

```text
inf { Q_w(f) : f in H, ||f||_2=1 } = 0.          (RH-247)
```

Equivalently, the feature operator with coordinates
`sqrt(w_k) integral x^(2k)f` is Hilbert-Schmidt and cannot be bounded below on
the infinite-dimensional unit sphere.

### B-D. Definitions and proof

Legendre orthogonality gives

```text
integral_(-1)^1 P_(2n)(x) x^(2k) dx = 0,  k<n,
integral_(-1)^1 P_(2n)(x)^2 dx = 2/(4n+1).
```

Thus the normalization and vanished moments are exact. For every `k>=n`,
Cauchy-Schwarz gives

```text
|integral x^(2k)f_n|^2
  <= ||f_n||_2^2 integral x^(4k) dx
  = 2/(4k+1).
```

Multiplication by `w_k` and summation proves the tail bound. The assumed
series converges, so its tails tend to zero. Its sum is also the sum of the
squared coordinate-functional norms, which independently identifies the
feature map as Hilbert-Schmidt and compact.

For the explicit display weights `w_k=2^(-k)`,

```text
Q_w(f_n) <= 2^(2-n)/(4n+1).
```

This is a no-go theorem, not a failed experiment: it covers every nonnegative
weight sequence satisfying the displayed summability condition.

### E-G. Adversarial and reproducible checks

The generator constructs `P_(2n)` twice: from the three-term recurrence and
independently from Rodrigues' coefficient formula. For
`n=1,2,3,4,5,6,8,10,12,16`, it checks coefficient equality, every vanished
moment, and the exact norm. The last dyadic upper bound is `1/1064960`.

- arithmetic: exact rational
- cases: 10 Legendre rows
- algorithm: polynomial recurrence and exact convolution, cubic in maximum degree
- failures: 0
- transcript SHA-256:
  `6f96be5ca5ceffa5ed645e2eb17758ae151b079799bf89baaa00c605cce871a5`

### H-I. Limit and classification

The theorem acts on the full even `L2` space. It does not prove that this
Legendre sequence lies in the genuine normalized Guinand-Weil admissible
closure. It also does not cover non-Hilbert-Schmidt arithmetic features.
Classification: `exact_no_go`. RH remains `open_not_proven`.

### J-K. Remaining gap and next single lemma

The remaining gap is an arithmetic, noncompact coercivity statement on the
actual admissible Weil closure, not another summable-moment embedding.

```text
NonHilbertSchmidtArithmeticWeilCoercivityOnAdmissibleClosure
```

## 2. Collatz conjecture

### A. Exact proposition: `FormalHenselBranchNoGoForValuationDomination`

For a prime `q>5`, use the TICKET-246 polynomial

```text
P_q(U,V)=5U-3V+q(10U^2-3V^2)+q^2(10U^3-V^3)+5q^3U^4+q^4U^5.
```

For every `r>=1`, there is a unique residue `V_r mod q^r` with
`V_r=5 mod q` such that, for `U=3`,

```text
P_q(3,V_r)=0 mod q^r,
3-V_r=-2 mod q.
```

Therefore

```text
v_q(P_q(3,V_r)) >= r > 0 = v_q(3-V_r).           (CO-247)
```

The assertion `v_q(P_q(U,V))<=v_q(U-V)` for unrestricted `q`-adic quotient
pairs is false at every prime `q>5` and arbitrary depth.

### B-D. Proof

Modulo `q`,

```text
P_q(3,V) = 15-3V,
```

so `V=5` is a root. The derivative is

```text
partial P_q/partial V = -3-6qV-3q^2V^2 = -3(1+qV)^2,
```

which is a unit modulo every `q>5`. Hensel lifting therefore gives one unique
compatible root modulo every `q^r`. The difference `3-V` stays `-2 mod q`,
so its valuation remains zero while the polynomial valuation is arbitrarily
large.

### E-G. Countermodels and exact replay

The generator lifts digit by digit. At depth `d`, it solves the unique linear
congruence for the next base-`q` digit using the inverse derivative and checks
the result directly modulo `q^(d+1)`.

- arithmetic: exact integer modular arithmetic
- input: all 1,226 primes `5<q<=10,000`
- depth: 8 digits for every prime
- complexity: `O(pi(10000) * 8 * log q)` modular operations
- failures: 0
- selected exact models: `q=7,11,23,101,1009,9973`
- transcript SHA-256:
  `bcb089ee91757f792ae7151212331f811f48a1cc771eea1386d4d4349ba04156`

### H-I. Limit and classification

These are formal `q`-adic pairs. They are not the actual Fermat quotients

```text
U_q=(2^(q-1)-1)/q,  V_q=(3^(q-1)-1)/q.
```

The result blocks an unrestricted-algebra proof of the desired valuation
domination; it does not refute an arithmetic theorem confined to actual
quotient pairs and says nothing by itself about Collatz trajectories.
Classification: `exact_no_go`. Collatz remains `open_not_proven`.

### J-K. Remaining gap and next single lemma

Any successful route must use arithmetic information that keeps the actual
Fermat quotient pair away from the Hensel branch.

```text
ArithmeticFermatQuotientExclusionOfPqHenselBranch
```

## 3. Strong Goldbach conjecture

### A. Exact proposition: `RationalCenterArcLipschitzBridgeAndCenterOnlyNoGo`

Fix `q>=3`, `X>=3`, and let `S*(alpha)` sum `exp(2 pi i alpha p)` over odd
primes `p<=X` coprime to `q`. Let `n_r` be their reduced-residue counts,
`P=sum n_r`, `delta_r=n_r-P/phi(q)`, `D=sum delta_r^2`, and `M=sum p` over the
same primes. Then, for every integer `a` and real `beta`,

```text
|S*(a/q+beta) - (P/phi(q)) c_q(a)|
  <= sqrt(phi(q)D) + 2 pi |beta| M,               (GB-247)

phi(q)D = phi(q) sum_r n_r^2 - P^2 in Z_>=0.
```

Center values alone cannot give a frequency-uniform modulus: for

```text
F_N(beta)=exp(2 pi i N beta)-1,
```

one has `F_N(0)=0` but `|F_N(1/(2N))|=2` while `1/(2N)->0`.

### B-D. Proof

TICKET-246 supplies the exact center decomposition and
`|R(a)|<=sqrt(phi D)`. The displacement is bounded termwise by

```text
|exp(2 pi i beta p)-1| <= 2 pi |beta|p.
```

Summation and the triangle inequality give the result. Expanding the rational
`delta_r` expression yields the displayed exact integer. The counterfamily is
exact because `exp(pi i)=-1`.

### E-G. Exact computation and adversarial test

The audit covers all `q=3..64` at `X=10,000,100,000,500,000` and stores 27
selected rows. It uses the illustrative exact width `|beta|=1/X^2`, stores
`M/X^2` before the symbolic factor `2 pi`, and verifies the variance integer.
It also replays `N=10,100,1000,10000` for the center-only counterfamily.

- arithmetic: integer/rational; no complex floating point used as proof
- denominator cases: 186
- selected arc rows: 27
- center-only counterexamples: 4
- failures: 0
- largest selected-scale-free `M/X^2` summary at `X=500,000`:
  `9914236193/250000000000`
- transcript SHA-256:
  `314c9f28ab175a59fce98474b249cf6e8fbc9fb811f2258d8c344d1b113a89b4`

### H-I. Limit and classification

The Lipschitz term may be trivial-sized; it is not signed prime cancellation.
The finite rows prove no uniform growing-denominator variance decay. The
counterfamily concerns unrestricted trigonometric polynomials, so it blocks
only center-only inference. Classification: `partial_theorem`. Strong
Goldbach remains `open_not_proven`.

### J-K. Remaining gap and next single lemma

The next theorem must simultaneously save the center residual and the signed
prime first-moment displacement on the reduced quarter-torus arcs.

```text
UniformSignedResidueVarianceAndFirstMomentSavingOnQuarterTorus
```

## 4. Twin-prime conjecture

### A. Exact proposition: `SharpOddPrimePowerContaminationBound`

Retain `A_2(X)` and `pi_2(X)` from TICKET-246. Put `Y=X+2`,
`K=floor(log_2 Y)`, and let `pi_odd(t)` count odd primes at most `t`. If
`N_odd(Y)` counts odd composite prime powers at most `Y`, then

```text
N_odd(Y) = sum_(k=2)^K pi_odd(floor(Y^(1/k))),

0 <= A_2(X)-pi_2(X) <= 2N_odd(Y)
   <= 2pi_odd(floor(sqrt(Y)))
      +2(K-2)pi_odd(floor(cuberoot(Y))).           (TP-247)
```

### B-D. Proof

An odd composite prime power has a unique representation `p^k` with odd prime
`p` and `k>=2`; counting by exponent proves the equality. Every false
prime-power pair has such a number in one of two coordinates, giving the
factor-two union bound. The `k=2` term is exact, and each of the remaining
`K-2` terms is at most the `k=3` term.

### E-G. Exact enumeration

The generator independently counts odd composite powers by base/exponent and
by a prime-power support array. It also compares the sharper expression with
the TICKET-246 exponent-blind bound.

- arithmetic: exact integers
- scales: `100, 1,000, 10,000, 100,000, 1,000,000, 5,000,000, 10,000,000`
- complexity: sieve `O(Y log log Y)` plus linear support scan
- failures: 0
- at `X=10,000,000`: `A_2=59,129`, `pi_2=58,980`, contamination `149`,
  `N_odd=533`, new explicit bound `2,822`, old bound `139,128`
- transcript SHA-256:
  `7b336b5638d06b913ebee11fc89308a7a186953083f85cfe772a8a4971410d87`

### H-I. Limit and classification

The exact correction is smaller, but no theorem makes `A_2` exceed it on an
unbounded scale sequence. Finite enumeration supplies no Type-II cancellation
and no infinitude conclusion. Classification: `partial_theorem`. The
twin-prime conjecture remains `open_not_proven`.

### J-K. Remaining gap and next single lemma

```text
ScaleLocalTypeIILowerBoundBeyondSharpPrimePowerContamination
```

## Adversarial proof audit and proof DAG boundary

- Quantifiers are explicit: RH covers all summable weights but only the full
  even `L2` model; Collatz covers all primes/depths but unrestricted pairs.
- No finite replay is promoted to an infinite theorem. The infinite claims use
  orthogonality/tail convergence, Hensel lifting, termwise exponential bounds,
  or unique prime-power factorization.
- Denominators are positive; `q>5` makes the Hensel derivative a unit.
- Goldbach keeps the frequency-scale term that the counterfamily proves is
  necessary.
- Twin roots are integer floor roots, not floating approximations.
- Each of the four proof DAGs is acyclic and has exactly one `open` frontier.
- No theorem node depends on the parent conjecture it is intended to advance.

## Final boundary

TICKET-247 completes the four auxiliary results, deterministic certificates,
route decisions, and next lemmas. It does not pass any conjecture-resolution
gate. This iteration is complete, but none of the four conjectures is solved.
