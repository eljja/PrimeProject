# TICKET-243: Bandlimit, Principal Units, Half-Arc Energy, and Dyadic Mimicry

Status: **open_not_proven**

Iteration complete: **yes**

Parent-conjecture resolutions: **0 / 4**

Candidate resolutions pending independent review: **0**

Deep-focus problem: **Collatz**

## Claim boundary

TICKET-243 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, the strong Goldbach conjecture, or the twin-prime conjecture. It
proves three exact no-go theorems and one exact partial theorem. Its finite rows
are deterministic implementation certificates, not replacements for the
infinite arguments.

Machine-readable audit:
`data/open-problem/ticket243-bandlimit-principal-unit-half-arc-dyadic-mimicry.json`.

Persistent state:
`data/open-problem/four-problem-research-state.json`.

Reproduce and verify with:

```powershell
python scripts/ticket243_bandlimit_principal_unit_half_arc_dyadic_mimicry.py
python -m unittest tests.test_ticket243_bandlimit_principal_unit_half_arc_dyadic_mimicry -v
python scripts/verify_ticket243_structure.py
python scripts/verify_open_problem_structure.py
```

## Result ledger

| Problem | Exact TICKET-243 result | Classification | Parent status |
|---|---|---|---|
| Riemann | A normalized real-even family can have one fixed Fourier support and still contain an infinite orthonormal, hence noncompact, sequence | `exact_no_go` | `open_not_proven` |
| Collatz | Universal principal-unit order-core transfer fails at the unbounded orders `(q-1)/2` for every prime `q>5` | `exact_no_go` | `open_not_proven` |
| Strong Goldbach | A full `1/(3X)` neighborhood of the parity frequency `1/2` carries absolute energy of natural binary scale | `exact_no_go` | `open_not_proven` |
| Twin prime | Every fixed periodic fingerprint has prime/composite-successor mimics in every sufficiently large dyadic block | `partial_theorem` | `open_not_proven` |

All four stagnation counters remain zero because every track obtains a new
exact theorem or a strictly sharper route boundary.

## 1. Riemann Hypothesis

### Exact proposition declared

For `n>=1`, put

```text
g_n(xi) = pi^(-1/2) cos(n xi),  -pi <= xi <= pi,
```

and let `f_n` be the inverse Fourier transform of `g_n`. Then every `f_n` is
normalized, real, even, and bandlimited to the same interval. Moreover,

```text
<f_n,f_m> = delta_nm.
```

Consequently, fixed Fourier support and `L2` normalization do not make an even
test family relatively compact.

The obstruction persists for smooth bandlimited tests. If nonzero real-even
`phi` belongs to `C_c^infinity((-R,R))`, normalized inverse transforms of

```text
phi(xi) cos(t xi)
```

contain a separated subsequence as `t` tends to infinity.

### Proof

Cosine orthogonality gives

```text
integral_(-pi)^pi cos(n xi) cos(m xi) dxi = pi delta_nm.
```

Plancherel transfers the Gram matrix to the inverse transforms. Thus distinct
members have squared distance `2`, and no subsequence is Cauchy.

For smooth `phi`, inner products of two modulated copies reduce to Fourier
coefficients of `|phi|^2` at frequencies `t-s` and `t+s`. The
Riemann-Lebesgue lemma makes these coefficients tend to zero. Choose the
parameters recursively far enough apart to obtain a uniformly separated
subsequence. The inverse transforms are real-even Schwartz functions with one
fixed frequency support.

### Reproducible computation

Five symbolic Gram certificates, of sizes `4, 8, 16, 32, 64`, record:

- diagonal entries `1`;
- off-diagonal entries `0`;
- minimum pairwise squared distance `2`;
- one common Fourier support `[-pi,pi]`.

Transcript SHA-256:
`6b52e81598d394e05fffe373733e2a7638a9de662610abd8f1b63c59e46e90cf`.

### Exact no-go and limitation

The rejected inference is:

```text
frequency tightness + normalization + evenness => compact test family.
```

Even the stronger property of one fixed compact Fourier support does not imply
compactness: physical translations or symmetric pairs can escape to infinity.

This does not prove that the actual Guinand-Weil admissible class contains the
counterfamily. It proves no signed arithmetic-tail estimate, positive limiting
margin, zero exclusion, or RH implication.

### Next single lemma

`JointPhysicalFrequencyTightnessAndUniformSignedGuinandWeilTailWithPositiveMargin`.

## 2. Collatz conjecture — deep focus

### Exact proposition declared

Let `q>5` be prime. Choose a primitive root `t mod q` and define its
Teichmuller lift

```text
T = t^q mod q^2.
```

In `(Z/q^2 Z)^*`, put

```text
A = T(1+3q),
B = T(1+5q),
U = A/B,
V = A^5/B^3.
```

Then

```text
ord_q(V) = (q-1)/2,
V^((q-1)/2) = 1 mod q^2,
ord_q(U) = 1,
U != 1 mod q^2.
```

Indeed, `U=1-2q mod q^2`. Thus square depth for the `(5,-3)` order core
does not universally transfer to the `(1,-1)` core, even along the unbounded
orders `(q-1)/2`.

### Proof

Euler's theorem and reduction modulo `q` show

```text
T^(q-1) = 1 mod q^2
```

and that `T` has exact order `q-1` modulo `q^2`. Binomial expansion gives

```text
(1+3q)^5     = 1+15q mod q^2,
(1+5q)^(-3) = 1-15q mod q^2.
```

Therefore

```text
V = T^2 mod q^2.
```

Its reduction has order `(q-1)/2`, and raising to that order gives
`T^(q-1)=1 mod q^2`. On the other hand,

```text
U = (1+3q)/(1+5q) = 1-2q mod q^2,
```

so `q` divides `U-1` exactly once. The countermodel order `(q-1)/2` is
unbounded with `q`.

### Reproducible computation

All `5,130` primes `5<q<=50,000` were replayed with exact modular arithmetic.
There were zero construction failures. The largest replayed countermodel order
was `24,999`, at `q=49,999`.

Transcript SHA-256:
`fa66801a2a9d21ff3f873a7ac22501d9e8193aea8a9404b42e2e318fdbdff59f`.

### Exact no-go and limitation

This closes the proposed transfer when it is supposed to follow from identities
valid for arbitrary local units, multiplicative order, LTE, and principal-unit
algebra alone. TICKET-241 supplied an order-one local model; TICKET-243 proves
that the obstruction persists at unbounded exact orders.

The constructed `A` and `B` vary with `q`. They are not the fixed integers `2`
and `3`. Therefore the theorem neither exhibits nor excludes a prime satisfying

```text
q^2 | 32^d - 27^d,  d=ord_q(32/27).
```

It also does not control general Collatz necklaces or aperiodic trajectories.

### Next single lemma

`FixedBaseRationalWieferichExclusionFor32Over27OnAllPrimeOrderCores`.

## 3. Strong Goldbach conjecture

### Exact proposition declared

Let

```text
S_X(alpha) = sum_(p<=X) exp(2 pi i p alpha).
```

For `X>=5` and `|beta|<=1/(6X)`,

```text
|S_X(1/2+beta)| >= (pi(X)-3)/2.
```

Consequently, for

```text
I_X = [1/2-1/(6X), 1/2+1/(6X)],
```

one has the exact lower bound

```text
integral_(I_X) |S_X(alpha)|^2 d alpha
  >= (pi(X)-3)^2/(12X)
  ~ X/(12 log^2 X).
```

### Proof

At `alpha=1/2+beta`, every odd prime contributes
`-exp(2 pi i p beta)`. Since `|2 pi p beta|<=pi/3`, its cosine is at least
`1/2`. After multiplying the sum by `-1`, the odd primes contribute real part
at least `(pi(X)-1)/2`; the `p=2` term costs at most `1`. Hence the pointwise
floor is `(pi(X)-3)/2`. Squaring and integrating over the interval of length
`1/(3X)` proves the exact energy bound. The prime number theorem supplies the
asymptotic scale.

### Reproducible computation

Seven exact rows use `X=1,000` through `1,000,000`. They record exact prime
counts, rational arc widths, pointwise floors, and rational energy floors.

Transcript SHA-256:
`db3723c1a9cdabd673471f1564af46489235e620f7384d6dcae6f3d3f1446392`.

### Exact no-go and limitation

If an alleged minor set contains the whole interval `I_X`, its absolute
`L2` energy cannot be `o(X/log^2 X)`. Thus the parity rational frequency must
be covered by the major-arc architecture at its natural width before an
absolute minor-energy certificate can close.

This says nothing about the signed target Fourier coefficient on the correctly
defined residual minor arcs. It proves no positive lower bound for the binary
representation count and produces no Goldbach counterexample.

### Next single lemma

`CompleteSmallDenominatorMajorArcCoverageAndSignedResidualBinaryCoefficientSaving`.

## 4. Twin-prime conjecture

### Exact proposition declared

Fix `M>=1` and `a mod M` satisfying

```text
gcd(a,M)=gcd(a+2,M)=1.
```

Let `F` be any feature periodic modulo `M`. Choose a prime `ell` not dividing
`2M`, and solve

```text
r = a  mod M,
r = -2 mod ell.
```

There is `X_0=X_0(M,a,ell)` such that every dyadic interval `[X,2X]` with
`X>=X_0` contains a prime `p` for which

```text
F(p,p+2)=F(a,a+2)
```

and `p+2` is composite.

### Proof

CRT gives a reduced residue class `r mod Q`, where `Q=M ell`. The prime number
theorem in arithmetic progressions for this fixed modulus gives

```text
pi(2X;Q,r)-pi(X;Q,r) ~ X/(phi(Q) log X)>0.
```

Thus every sufficiently large dyadic block contains a prime in the class.
Periodicity preserves `F`, while `ell | p+2`; increasing `X_0` beyond `ell`
makes the successor a proper composite multiple.

### Reproducible computation

Sixteen exact witnesses cover four periods `30, 210, 2,310, 30,030` and four
dyadic starts for each. Every witness is prime, belongs to the declared block
and residue class, and has a certified composite successor.

Transcript SHA-256:
`3858c95f26b5cf54bc5873b288814a47c38add509e0adf65068b79cf85f8fadd`.

### Partial theorem and limitation

TICKET-241 proved infinitely many mimics for a fixed periodic fingerprint;
TICKET-243 strengthens this to a mimic in **every sufficiently large dyadic
block**. Therefore eventual scale sampling does not rescue a fixed-period
classifier.

The threshold depends on the fixed modulus. The argument is not uniform when
`M=M(X)` grows with the scale and gives no signed Type-II estimate for
`Lambda(n)Lambda(n+2)`. It does not disprove twin primes.

### Next single lemma

`ScaleLocalGrowingModulusTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass`.

## Proof DAG and adversarial audit

Every problem has an acyclic DAG of the form

```text
TICKET-242 proved input
  + named external theorem when needed
  -> TICKET-243 rejected inference
  -> TICKET-243 proved theorem
  -> one open successor lemma
```

Node statuses are restricted to `proved`, `disproved`, `computed_finite`,
`external_theorem`, `assumption`, `heuristic`, and `open`. Every track has
exactly one open frontier. No node is marked as a parent-conjecture resolution.

The research baselines are the Clay Mathematics Institute's current RH page,
Mitkovski--Stockdale--Wagner--Wick on Riesz-Kolmogorov compactness, Tao's
Collatz work, Helfgott's minor-arc work, Thorner--Zaman on primes in arithmetic
progressions, and the Polymath parity discussion. These sources delimit the
accepted frontier; the theorem names in this ticket are PrimeProject route
audits and are not attributed to those papers.

## Final boundary

TICKET-243 is iteration-complete. It proves three exact no-go results and one
partial theorem, but none is a proof or disproof of a parent conjecture. All
four problems remain `open_not_proven`.
