# TICKET-242: Quantifiers, Order Cores, Parseval Scale, and Diagonal CRT

Status: **open_not_proven**

Parent-conjecture resolutions: **0 / 4**

## Claim boundary

TICKET-242 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, the strong Goldbach conjecture, or the twin-prime conjecture. It
proves four exact route-boundary theorems and reports bounded computations only
on their declared domains.

Machine-readable audit:
`data/open-problem/ticket242-quantifier-order-parseval-diagonal-crt.json`.

Reproduce and verify with:

```powershell
python scripts/ticket242_quantifier_order_parseval_diagonal_crt.py
python -m unittest tests.test_ticket242_quantifier_order_parseval_diagonal_crt -v
python scripts/verify_ticket242_structure.py
python scripts/verify_open_problem_structure.py
```

## Result ledger

| Problem | Exact TICKET-242 result | Rejected route | Status |
|---|---|---|---|
| Riemann | Fixed-test convergence and eventual positivity can coexist with one moving negative direction at every finite section; compact-uniform transfer is sufficient | Pointwise finite-section convergence proves positivity on a growing test family | `open_not_proven` |
| Collatz | The bad Fermat-quotient line is exactly a square divisor of the multiplicative-order core, and those orders are unbounded | Bounded-order core checks settle the all-prime line avoidance | `open_not_proven` |
| Goldbach | A global Parseval minor bound has size `pi(X)`, asymptotically one logarithm above the natural binary scale | Global `L2` energy and triangle inequality close a binary lower certificate | `open_not_proven` |
| Twin prime | Any sequence of growing periodic classifiers has a strictly increasing diagonal sequence of prime/composite-successor mimics | Modulus growth alone eventually separates twins | `open_not_proven` |

## 1. Riemann Hypothesis

### Exact proposition declared for this ticket

On `H=l2(N)`, define

```text
A_n = I - 2 <.,e_n> e_n.
```

Then, for every fixed `x in H`,

```text
<A_n x,x> = ||x||^2 - 2|x_n|^2 -> ||x||^2.
```

For every nonzero fixed `x`, this quadratic form is eventually positive.
Nevertheless,

```text
inf_(||x||=1) <A_n x,x> = -1
```

for every `n`, attained at the moving test `x=e_n`.

Conversely, let `K` be a compact normalized test class. If `q_n -> q`
uniformly on `K` and `inf_K q >= delta > 0`, then

```text
inf_K q_n >= delta/2
```

for all sufficiently large `n`.

### Proof

Every square-summable sequence has `x_n -> 0`, giving fixed-test convergence.
For nonzero `x`, eventually `2|x_n|^2 < ||x||^2`, giving eventual positivity.
But direct substitution of `e_n` gives `-1`; `A_n` is diagonal with exactly one
negative entry. The compact transfer is the one-line estimate

```text
q_n(x) >= q(x) - sup_(y in K)|q_n(y)-q(y)| >= delta/2.
```

This separates two quantifier orders:

```text
for every fixed test, eventually positive
```

does not imply

```text
eventually, every test in the growing family is positive.
```

### Reproducible computation

Six exact diagonal sections, of dimensions `4, 8, 16, 32, 64, 128`, were
recorded. Every row has:

- smallest eigenvalue `-1`;
- exactly one negative direction;
- fixed early-coordinate value `+1`;
- operator-norm distance `||A_n-I||=2`;
- normalized trace `1-2/n`, tending to `1` despite the persistent negative
  direction.

The transcript SHA-256 is
`f694cbcb62bd7a5fbe6cb3ade6516ceddb753012675f000aa9970cad15226e4f`.

### No-go, limitation, and next lemma

The rejected route is fixed-test finite-section convergence, fixed-test
eventual positivity, or convergent averaged diagnostics as evidence for a
uniform signed Weil lower bound.

The countermodel is abstract and is not the Guinand-Weil quadratic form. No
compactness theorem, frequency-tightness theorem, uniform arithmetic tail
estimate, or positive limit margin is established for the actual admissible
test class.

Next single lemma:

`UniformSignedGuinandWeilTailBoundOnFrequencyTightNormalizedAdmissibleTestClasses`.

## 2. Collatz conjecture

### Exact proposition declared for this ticket

Let `q>5` be prime and put

```text
d = ord_q(32/27).
```

Then

```text
v_q(32^(q-1)-27^(q-1)) = v_q(32^d-27^d).
```

Consequently the bad Fermat-quotient line

```text
5 F_q(2) = 3 F_q(3) mod q
```

is equivalent to

```text
q^2 | 32^d-27^d.
```

Moreover, the orders `ord_q(32/27)` are unbounded as `q` varies.

### Proof

Write `q-1=dk`. Since `1<=k<q`, `q` does not divide `k`. LTE gives

```text
v_q((32^d)^k-(27^d)^k)
  = v_q(32^d-27^d) + v_q(k)
  = v_q(32^d-27^d).
```

If all orders were bounded by `D`, every prime `q>5` would divide the fixed
nonzero integer

```text
product_(1<=d<=D) (32^d-27^d),
```

which has only finitely many prime divisors. This contradicts the infinitude of
primes.

### Reproducible computation

All `17,981` primes `5<q<=200,000` were checked. The order-core depth agreed
with the full exponent `q-1` in every row. This ticket found no bad-line
candidate in that bounded replay; TICKET-241 already searched much farther, to
`10^8`, so this smaller scan is not advertised as an extension.

The observed maximum order grew as follows:

| Prime cutoff | Largest order observed | Witness prime |
|---:|---:|---:|
| 100 | 82 | 83 |
| 1,000 | 990 | 991 |
| 10,000 | 9,966 | 9,967 |
| 100,000 | 99,970 | 99,971 |
| 200,000 | 199,998 | 199,999 |

The transcript SHA-256 is
`ede3279e2ec7d5e375ec2e3ea65349459e401f9174c8eee13b7b697aacc70fec`.

### No-go, limitation, and next lemma

The bounded-order route is closed: no fixed order cutoff can cover all primes.
The exact LTE reduction does not exclude square divisors on unbounded order
cores. It also proves nothing for general necklaces or aperiodic Collatz
descent.

Next single lemma:

`UniformOrderCoreSquareDivisorTransferFrom32Over27To2Over3`.

## 3. Strong Goldbach conjecture

### Exact proposition declared for this ticket

Let

```text
S_X(alpha) = sum_(p<=X) e(p alpha).
```

Parseval gives

```text
integral_0^1 |S_X(alpha)|^2 d alpha = pi(X).
```

For any measurable minor-arc set `m` and even target `N`,

```text
|integral_m S_X(alpha)^2 e(-N alpha) d alpha|
  <= integral_m |S_X(alpha)|^2 d alpha
  <= pi(X).
```

Therefore a binary lower certificate whose only minor estimate is the global
Parseval bound cannot close against any proposed main term
`M_X(N)=o(pi(X))`. In particular,

```text
X/log^2 X = o(pi(X))
```

by the prime number theorem.

### Proof

The first inequality is the triangle inequality applied to the target Fourier
coefficient. Enlarging the domain gives the global Parseval energy. If
`M_X=o(pi(X))`, then `M_X-pi(X)<0` eventually. Since
`pi(X)~X/log X`, the global energy exceeds the natural binary scale by a factor
asymptotic to `log X`.

### Reproducible computation

Seven exact prime counts and sample even-target convolutions were audited for
`10^3<=X<=10^6`. The ratio

```text
pi(X) / (X/log^2 X)
```

grew from `8.0165` to `14.9828`. In every row the global `L2` bound was at
least the entire observed ordered representation count, confirming how coarse
the norm-only certificate is at finite scale.

The transcript SHA-256 is
`fa85d668b1b025ab2a81b01ed957cc2ada5f4758a99e0a39874434521ac05280`.

### No-go, limitation, and next lemma

This closes only the global-`L2` plus triangle-inequality route. It does not
exclude targetwise signed cancellation, restriction estimates, Type I/II
decompositions, or a sharper fixed major/minor-arc architecture. No Goldbach
counterexample is produced.

Next single lemma:

`FixedBinaryPrimeMinorArcCoefficientIsLittleOOfTargetMainUniformlyOnBufferedEvenTargets`.

## 4. Twin-prime conjecture

### Exact proposition declared for this ticket

Let `(M_j)` be any sequence of positive periods. For each `j`, choose
`a_j mod M_j` satisfying

```text
gcd(a_j,M_j)=gcd(a_j+2,M_j)=1,
```

and let `F_j` be any feature periodic modulo `M_j`. There is a strictly
increasing sequence of primes `(p_j)` such that

```text
F_j(p_j,p_j+2)=F_j(a_j,a_j+2)
```

while `p_j+2` is composite.

### Proof

For each stage, choose a prime `ell_j` not dividing `2M_j` and solve

```text
p_j = a_j mod M_j,
p_j = -2  mod ell_j.
```

CRT produces a reduced residue class modulo `M_j ell_j`. Dirichlet's theorem
provides infinitely many primes in that class, so choose one larger than both
`p_(j-1)` and `ell_j`. Periodicity preserves `F_j`, while `ell_j | p_j+2`
makes the successor properly composite.

### Reproducible computation

Six growing periods from `30` to `9,699,690` were used. The exact increasing
prime witnesses are

```text
131, 1,901, 48,527, 1,651,667, 6,126,149, 902,071,199.
```

At the final stage,

```text
p+2 = 23 * 39,220,487.
```

The transcript SHA-256 is
`5cc91d6440bc282199fd9b5f348d758fa23b256a593c890d2199e49f75c1ed79`.

### No-go, limitation, and next lemma

Growing modulus alone is not a certificate. The construction selects its scale
after the CRT class, however: it does not place a counterfeit in a predeclared
dyadic block and supplies no quantitative least-prime estimate. Genuinely
nonperiodic signed Type II information remains outside the no-go.

Next single lemma:

`ScaleLocalGrowingModulusTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass`.

## Proof DAG summary

Each track uses the same guarded dependency pattern:

```text
TICKET-241 closed input
  -> TICKET-242 rejected inference
  -> TICKET-242 exact theorem
  -> one highest-risk open lemma
```

No DAG node records a proof or disproof of a parent conjecture.

## Final boundary

TICKET-242 establishes four exact partial or no-go theorems. The remaining
lemmas require, respectively, a uniform signed Weil tail, an all-order rational
Wieferich square-divisor transfer, targetwise signed binary minor-arc
cancellation, and a scale-local parity-sensitive Type II estimate. All four
parent conjectures remain open.
