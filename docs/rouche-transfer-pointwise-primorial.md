# TICKET-203: Rouché Transfer, Signed Valuation Transfer, and Pointwise Target Correction

## Claim status

`open_not_proven` for all four parent conjectures. TICKET-203 proves four
partial or no-go theorems. It proves neither a complete proof nor a
counterexample for the Riemann Hypothesis, Collatz conjecture, strong Goldbach
conjecture, or Twin Prime conjecture.

Canonical machine artifact:
[`ticket203-rouche-transfer-pointwise-primorial.json`](../data/open-problem/ticket203-rouche-transfer-pointwise-primorial.json).

The round advances TICKET-202 by checking whether each advertised “next lemma”
is both logically sufficient and realistically weaker than the parent
conjecture. Two targets survive after correction, and two are replaced by more
precise statements.

| Problem | Exact TICKET-203 result | Route decision | Remaining open lemma |
|---|---|---|---|
| Riemann | certified included zeros plus a Rouché count give exact exhaustion | retain the transfer, reject equal counts without inclusion | `CompletedZetaCofinalRelativeMarginCertificateFamily` |
| Collatz | exact signed two-site transfer identity; universal invariance has counterexample `(3,1)->(2,2)` | reject unconditional transfer invariance | `ScaleDependentTransferResidueBarrierOutsideAllTwoOrbit` |
| Goldbach | pointwise positive defect is exactly Goldbach positivity; a fixed `c/log log N` lower bound is stronger | reject the scaled bound as an “easier” lemma | `UniformPointwiseGoldbachMinorArcDominanceOverExplicitMajorArc` |
| Twin Prime | fixed primorial single-coordinate data cannot separate all primes from rough semiprimes | reject fixed-local separation, retain switching | `ScaleGrowingBilinearSwitchingWeightWithSignedPrimeSemiprimeCorrelation` |

## 1. Riemann Hypothesis

### Declared proposition

Let `X` and `P` be analytic on and inside a simple closed contour `Gamma`.
Assume:

1. `|X-P|<|P|` on `Gamma`;
2. `P` has exactly `m` interior zeros, counted with multiplicity;
3. an independently certified list already contains `m` interior zeros of
   `X`, counted with multiplicity.

Then the list exhausts all zeros of `X` inside `Gamma`.

### Proof

Rouché's theorem gives

```text
N_Gamma(X) = N_Gamma(P) = m.
```

The certified list is a submultiset of the interior zero multiset of `X` and
already has multiplicity `m`. Therefore no additional interior zero exists.

The independent inclusion premise is essential. Equality of total zero counts
alone says nothing about whether the counted zeros are the known real zeros or
different nonreal zeros.

For `Xi(z)=xi(1/2+iz)`, RH would follow if this contract were certified on a
cofinal family of rectangles covering `|Im z|<1/2`, and if every included zero
were independently certified on the real `z` axis. TICKET-203 proves this
logical implication. It does not construct the required Xi boundary margins.

### Exact regression

Take

```text
P(z) = (z^2-1)(z^2-4),
X(z) = P(z)(1+z^2/100),
Gamma = boundary of {|Re z|<=3, |Im z|<=1}.
```

On `Gamma`, `|z|^2<=10`, so

```text
|X-P|/|P| = |z|^2/100 <= 1/10 < 1.
```

Both functions contain the four listed zeros `-2,-1,1,2`. The two additional
zeros of `X`, `+/-10i`, lie outside the rectangle. The exact certified margin is
`9/10`.

### Boundary

This is a conditional zero-exhaustion theorem and a synthetic exact test. The
comparison does not supply a bound for the actual completed zeta function.
Finite verification up to a height, including rigorous interval work such as
Platt--Trudgian, is not a cofinal certificate.

## 2. Collatz Conjecture

### Declared proposition

For a positive accelerated valuation word

```text
a = (a_0,...,a_(h-1)),
P_m = a_0+...+a_(m-1),
B(a) = sum_m 3^(h-1-m) 2^P_m,
D(a) = 2^sum(a)-3^h,
```

fix `i<j`. If `a_i>=2` and one unit is moved from `i` to `j`, put
`a'=a-e_i+e_j`. Then

```text
D(a') = D(a),
B(a') = B(a) - Q_(i,j)/2,
Q_(i,j) = sum_(i<m<=j) 3^(h-1-m) 2^P_m.
```

If `a_j>=2` and the unit is moved in the reverse direction, then

```text
B(a+e_i-e_j) = B(a) + Q_(i,j).
```

### Proof

In the forward move, exactly the prefix exponents
`P_(i+1),...,P_j` decrease by one. Their powers of two are halved; every other
term is unchanged. Subtracting the two sums gives `-Q/2`. In the reverse move,
the same powers double and the difference is `+Q`. The total valuation is
unchanged, so the denominator is unchanged.

### Minimal no-go counterexample

The hoped-for universal conclusion “nondivisibility survives every signed
transfer” is false:

```text
a=(3,1),  D=2^4-3^2=7,  B(a)=11,
a'=(2,2), B(a')=7.
```

Thus `D` does not divide `11`, but it divides `7`. The target is the known
all-two accelerated fixed cycle, not a nontrivial Collatz cycle.

### Reproducible finite audit

For valuation alphabet `{1,2,3,4}`, positive denominators, and lengths `2` to
`7`, the implementation checks 310,103 forward transfers. The exact identity
has zero failures. The divisibility-hit counts are

```text
1, 3, 6, 10, 15, 21 = binomial(h,2),
```

and every hit in this bounded box targets the all-two word. This finite fact is
not promoted to an unbounded theorem.

### Boundary

The result neither excludes arbitrary periodic words nor addresses divergent
nonperiodic natural-number trajectories. The next route must remove the
all-two component and prove a scale-dependent residue barrier; it cannot rely
on transfer invariance alone.

## 3. Strong Goldbach Conjecture

### Declared proposition

For a Chen-positive even target `N`, let `R(N)` count ordered prime-prime
representations, let `S(N)` count ordered prime-semiprime representations, and
put

```text
C(N)=R(N)+S(N),
L(N)=S(N)-R(N),
delta(N)=1-L(N)/C(N).
```

Then

```text
delta(N)=2R(N)/C(N),
R(N)>0 iff delta(N)>0.
```

Consequently, a uniform bound `delta(N)>=c/log log N` for all sufficiently
large even `N` already implies Goldbach and is quantitatively stronger than
mere positivity.

### Exact channel countermodel

For powers of two `m`, let

```text
N=2^m, C=N/m, R=1, S=C-1, L=C-2.
```

All quantities are nonnegative integers and `R>0`, while

```text
delta = 2m/2^m.
```

Since `log log(2^m)<=m` for `m>=2`,

```text
delta log log N <= 2m^2/2^m -> 0.
```

Thus projector algebra plus one positive representation cannot imply a fixed
log-log-scaled lower bound. The model is not prime arithmetic and is not a
Goldbach counterexample.

### Corrected route

The previous target is not discarded as false for the primes; it is discarded
as a supposedly easier intermediate lemma. The retained analytic target is a
pointwise circle-method inequality in which an explicit major-arc lower bound
dominates the minor arcs for every sufficiently large even integer. Current
exceptional-set results and explicit major-arc formulas do not provide this
all-target domination in this project.

## 4. Twin Prime Conjecture

### Declared proposition

Fix `z` and `W=product_(p<=z)p`. No single-coordinate weight depending only on
`n mod W` can separate every prime from every semiprime whose factors exceed
`z`.

### Proof

For any reduced residue `a mod W`, Dirichlet's theorem gives arbitrarily large
primes in the residue classes `a` and `1`. Choose primes

```text
p = a mod W,
q = 1 mod W,
r = a mod W,
```

all above `z`. Then `p` is prime and `qr` is a rough semiprime, but
`p=qr=a mod W`. They have the same full residue and therefore the same small
prime divisibility signature. Every deterministic function of that fixed
signature assigns the same weight to both.

### Exact finite collisions

The machine artifact records collisions through `z=11`. At `W=2310`, for
example,

```text
2311 is prime,
4621 is prime,
2311*4621 = 10,679,131 is semiprime,
2311 = 10,679,131 = 1 (mod 2310).
```

### Boundary

This is a fixed-local, single-coordinate parity no-go. It does not cover
scale-growing sieve levels, bilinear switching, correlations with the first
prime coordinate, or distribution estimates. In particular it does not refute
the switching framework studied by Matomäki and Zuniga Alterman, and it does
not find a Twin Prime counterexample.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket203_rouche_transfer_pointwise_primorial.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket203_rouche_transfer_pointwise_primorial -v
```

Expected machine summary:

```text
exact partial theorems: 4
Collatz exact forward transfers: 310103
Goldbach actual targets: 4
Goldbach abstract countermodels: 5
Twin primorial collisions: 5
conjecture resolutions: 0
failures: 0
```

## Literature boundary

- D. Platt and T. Trudgian, [The Riemann hypothesis is true up to
  `3*10^12`](https://arxiv.org/abs/2004.09765), for rigorous finite-height zero
  certification.
- J. C. Lagarias, [The `3x+1` problem and its
  generalizations](https://doi.org/10.2307/2322189), for established Collatz
  affine and dynamical context.
- L. Grimmelt and G. Bhowmik, [The exceptional set of the Goldbach
  problem](https://arxiv.org/abs/2607.27282), for current exceptional-set
  context and an explicit major-arc formula.
- K. Matomäki and S. Zuniga Alterman, [Weighted sieves with
  switching](https://arxiv.org/abs/2405.19063), for the retained nonlocal Twin
  route.

No literature-priority claim is made for TICKET-203 without independent expert
review. The Rouché and fixed-sieve parity principles are established
mathematics; the project contribution claimed here is the exact proof contract,
route correction, reproducible regression, and explicit claim boundary.
