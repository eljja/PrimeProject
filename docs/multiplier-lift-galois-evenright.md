# TICKET-250: multiplier escape, lift transitivity, Galois support, and even-left classification

- parent: TICKET-249
- `iteration_complete`: true
- `program_complete`: false
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- classifications: two `exact_no_go`, two `partial_theorem`
- deep focus: strong Goldbach conjecture
- all four parent problems: `open_not_proven`

TICKET-250 proves four project-local auxiliary results. It does **not** prove
or disprove the Riemann hypothesis, Collatz conjecture, strong Goldbach
conjecture, or twin-prime conjecture. “Iteration complete” means that this
ticket's declared propositions, computations, audits, and artifacts are
complete; it does not mean that a parent conjecture is resolved.

## Reproduction contract

```powershell
python scripts/ticket250_multiplier_lift_galois_evenright.py
python -m unittest tests.test_ticket250_multiplier_lift_galois_evenright -v
python scripts/verify_ticket250_structure.py
python scripts/verify_ticket249_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket250-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

The generator is deterministic and has no random seed. Algebraic certificates
use integers and `Fraction`. Floating companions in JSON are display values,
not proof premises.

| Problem | Exact proposition decided in TICKET-250 | Classification | Parent status |
|---|---|---|---|
| Riemann | the noncompact multiplier `M_(x^2)` defeats the Legendre escape but still fails coercivity on a centered concentration sequence | `exact_no_go` | `open_not_proven` |
| Collatz | local Fermat-quotient lifts of residues 2 and 3 act transitively, so every lift fiber contains exactly `q-1` representatives of slope `[3:5]` | `exact_no_go` | `open_not_proven` |
| Strong Goldbach | every nonconstant rational residue vector at a prime modulus has nonzero Fourier coefficient at every reduced frequency and a nonzero integer Galois norm | `partial_theorem` | `open_not_proven` |
| Twin Prime | every right-active pair with even left exponent is exactly `25 -> 27` | `partial_theorem` | `open_not_proven` |

## 1. Riemann hypothesis

### A. Declared proposition: `NoncompactMultiplierLegendreEscapeInsufficiencyNoGo`

Let

```text
H = L2_even([-1,1]),
Q0(f) = sum_(k>=0) |integral_(-1)^1 x^(2k) f(x) dx|^2,
phi_l = sqrt((2l+1)/2) P_l,
K = M_(x^2).
```

The operator `K` is bounded, self-adjoint, and noncompact. For even
`l=2n`,

```text
<K phi_l, phi_l>
 = (l+1)^2/((2l+1)(2l+3)) + l^2/((2l-1)(2l+1))
 -> 1/2.                                                   (RH-250a)
```

Thus `K` blocks the TICKET-249 Legendre weak-null escape. Nevertheless, for

```text
g_epsilon = (2 epsilon)^(-1/2) 1_[-epsilon,epsilon],
```

```text
||g_epsilon|| = 1,
<K g_epsilon,g_epsilon> = epsilon^2/3,
Q0(g_epsilon) <= 2 epsilon/(1-epsilon^4) -> 0.             (RH-250b)
```

Therefore positivity on the Legendre sequence for one noncompact correction
does not imply coercivity on the unit sphere.

### B-D. Proof and inference audit

The three-term Legendre recurrence gives (RH-250a) after retaining the
`P_l` coefficient in `x^2P_l`. Multiplication by `x^2` is noncompact:
choose normalized indicators on countably many disjoint positive-measure
intervals inside `[1/2,1]`. Their images are orthogonal and each has norm at
least `1/4`, so the image sequence has no norm-convergent subsequence.

For `g_epsilon`, direct integration gives

```text
|integral x^(2k) g_epsilon(x) dx|^2
 = 2 epsilon^(4k+1)/(2k+1)^2.
```

Dropping `(2k+1)^2 >= 1` and summing a geometric series proves (RH-250b).
No finite calculation is used to infer either all-sequence statement.

### E-G. Adversarial and reproducible computation

Nine exact Legendre rows, `n=1,...,256`, verify the recurrence. Twelve exact
concentration rows, `epsilon=1/2,...,1/4096`, verify the decreasing upper
bound. The final Legendre expectation is `525311/1050621`, at distance
`1/2101242` from `1/2`. Failures: 0.

- transcript SHA-256:
  `20099dd1cab1cbcfa5ef4863e9f3c115c9f59af2da902d05bdbe029b5a8c507b`.

### H-I. No-go scope and finite limit

Discarded route: treating a positive diagonal limit on the Legendre sequence
for one noncompact multiplier as a certificate of full-sphere coercivity.
This is an exact counterexample to that route. It says nothing decisive about
the actual Guinand-Weil arithmetic form or its admissible closure. RH remains
`open_not_proven`.

### J-K. Remaining gap and next single lemma

```text
ArithmeticWeilFormCoercivityAgainstOscillationAndConcentrationEscapes
```

The next form estimate must control both oscillatory Legendre escape and
spatial concentration escape on the genuine admissible closure.

## 2. Collatz conjecture

### A. Declared proposition: `LocalFermatQuotientLiftTransitivityNoGo`

For a prime `q>5`, set

```text
F_q(a) = (a^(q-1)-1)/q mod q,
A_k = 2+kq, B_l = 3+lq            (k,l in F_q).
```

Then

```text
F_q(a+kq) = F_q(a)-k/a mod q.                         (CO-250a)
```

Consequently `(k,l) -> (F_q(A_k),F_q(B_l))` is a bijection of
`F_q^2`. Exactly `q-1` pairs lie on the nonzero projective line
`[3:5]`; for each `t!=0` the unique pair is

```text
k = 2(F_q(2)-3t),   l = 3(F_q(3)-5t).                (CO-250b)
```

Thus residue classes 2 and 3 modulo `q`, together with lift-invariant local
Fermat-quotient structure, cannot exclude the target slope.

### B-D. Proof and inference audit

Expanding `(a+kq)^(q-1)` modulo `q^2` leaves the constant term and first
binomial term:

```text
(a+kq)^(q-1) = a^(q-1)+(q-1)a^(q-2)kq mod q^2.
```

After subtracting one and dividing by `q`, Fermat's theorem gives
(CO-250a). Both coordinate maps are affine permutations. Substituting the
target `(3t,5t)` gives (CO-250b), hence exactly one lift pair for each of the
`q-1` nonzero values of `t`.

### E-G. Adversarial and reproducible computation

Exact exhaustive arithmetic checks `q=7,11,23,101,251`: 73,901 lift pairs.
Every image contains `q^2` distinct points and every target count is
`q-1`. Failures: 0.

- transcript SHA-256:
  `08ee2ee2080e127c58f7120621b39d20213ce2f6cf71987aaf01c7099ad528c2`.

### H-I. No-go scope and finite limit

This exact no-go eliminates only a **lift-invariant local** exclusion route.
The Collatz obstruction uses the canonical fixed representatives 2 and 3 as
`q` varies. Local transitivity neither proves occurrence nor avoidance for
those canonical representatives and does not control arbitrary trajectories.
Collatz remains `open_not_proven`.

### J-K. Remaining gap and next single lemma

```text
CanonicalRepresentativeFermatQuotientDistributionBeyondLiftTransitivity
```

## 3. Strong Goldbach conjecture — deep focus

### A. Declared proposition: `PrimeModulusRationalFourierFullSupportAndNormBarrier`

Let `q>=5` be prime, let `n_0,...,n_(q-1)` be integers, put

```text
N=sum_r n_r,  Delta_r=q n_r-N,
F(a)=sum_(r=0)^(q-1) Delta_r zeta_q^(ar).
```

If the vector `n` is nonconstant, then

```text
F(a) != 0 for every a=1,...,q-1,                    (GB-250a)
product_(a=1)^(q-1) F(a) is a nonzero integer.      (GB-250b)
```

In particular its absolute value is at least one. The exact two-frequency
cosine spike from TICKET-249 cannot be an integer or rational residue-count
vector at a prime modulus `q>=5`.

### B-D. Proof and inference audit

Let `P(X)=sum Delta_r X^r`. If `P(zeta_q^a)=0` for a reduced `a`, the
minimal polynomial `Phi_q=1+X+...+X^(q-1)` divides `P`. Since both degrees
are at most `q-1`, `P=c Phi_q`. But `P(1)=sum Delta_r=0` whereas
`Phi_q(1)=q`; hence `c=0`, all `Delta_r=0`, and `n` is constant, a
contradiction. This proves (GB-250a). The conjugates of `F(1)` are exactly
`F(a)`, so their product is its algebraic-integer norm, proving (GB-250b).

The prime-modulus assumption is structural. At `q=4`, the rational vector
`[1,0,-1,0]` has support only at frequencies 1 and 3. At `q=3`, the
nonconstant vector `[2,-1,-1]` naturally has the only two reduced
frequencies. These exact boundary models prevent an unjustified composite-
modulus extension.

### E-G. Adversarial and reproducible computation

Prime residue-count vectors are built exactly for
`X=100,1000,10000,100000,1000000` and
`q=5,7,11,13,17,19,23`: 35 cases. The cyclotomic norm is evaluated as an
exact multiplication-matrix determinant with Bareiss elimination. Every
nonconstant vector has full reduced support and nonzero norm; the smallest
observed absolute norm is 250,000. The two boundary countermodels are also
replayed. Failures: 0.

- transcript SHA-256:
  `684fea0b7645dea69f080eddb985918605ef6db23fde35646689556c8cf5c5a1`.

### H-I. Partial-theorem scope and finite limit

Galois symmetry proves nonvanishing, not upper anti-concentration. A nonzero
integer norm permits one conjugate to be tiny when others are large. The
finite prime-count audit is not an asymptotic estimate, uses unweighted
counts rather than logarithmic weights, and does not establish a minor-arc
saving. Strong Goldbach remains `open_not_proven`.

### J-K. Remaining gap and next single lemma

```text
QuantitativePrimeCountFourierEnergyAntiConcentrationAtPrimeModuli
```

The needed result is a uniform upper bound, not merely exact support or a
lower bound on the product of conjugates.

## 4. Twin-prime conjecture

### A. Declared proposition: `AllBaseEvenLeftRightActiveClassification`

For odd primes `p,r`, `m>=1`, and `ell>=2`,

```text
p^(2m)+2=r^ell
```

has the unique solution

```text
(p,m,r,ell)=(5,1,3,3), i.e. 25+2=27.               (TP-250)
```

Hence every right-active composite prime-power pair whose left member has an
even exponent is exactly `25 -> 27`, and its scale count is
`1_[X>=25]`.

### B-D. Proof and external dependency

If `ell=2`, reduction modulo 8 gives `p^(2m)+2=3 mod 8`, impossible for
an odd square. For `ell>=3`, apply the published `D=2` generalized
Lebesgue-Nagell classification to `x^2+2=y^n`, with `x=p^m`,
`y=r`, and `n=ell`. It gives the unique positive solution
`x=5,y=3,n=3`.

This dependency is an explicit `external_theorem` node in the proof DAG:
Y. Bugeaud, M. Mignotte, and S. Siksek, “Classical and modular approaches to
exponential Diophantine equations II. The Lebesgue-Nagell equation,”
*Compositio Mathematica* 142 (2006),
<https://doi.org/10.1112/S0010437X05001739>.

### E-G. Adversarial and reproducible computation

Nine exact scale rows from `X=24` through `10,000,000` enumerate
prime-power support. The even-left count changes from 0 to 1 at 25 and never
changes again. At ten million, the full right-active count is 136: one
even-left witness and 135 odd-left witnesses. Failures: 0.

- transcript SHA-256:
  `0cf8bd40771dca2cc7e0da725f6bffbaefb50d81c3d73d72731917568fa4dcda`.

### H-I. Partial-theorem scope and finite limit

The external theorem proves the all-scale even-left classification; finite
enumeration is only a replay. It does not control the odd-left subclass, the
full prime-pair correlation, or the Type-II lower bound needed by the twin
proxy. The twin-prime conjecture remains `open_not_proven`.

### J-K. Remaining gap and next single lemma

```text
ScaleLocalOddLeftRightActiveContaminationBound
```

## Proof DAG summary

Each track has one TICKET-249 proved predecessor, one TICKET-250 proved node,
one disproved route, and exactly one open frontier. The twin track additionally
has the explicit external Lebesgue-Nagell theorem node. All four DAGs are
acyclic.

| Track | Proved node | Disproved route | Open frontier |
|---|---|---|---|
| RH | `NoncompactMultiplierLegendreEscapeInsufficiencyNoGo` | Legendre-only noncompact validation | `ArithmeticWeilFormCoercivityAgainstOscillationAndConcentrationEscapes` |
| Collatz | `LocalFermatQuotientLiftTransitivityNoGo` | lift-invariant local slope exclusion | `CanonicalRepresentativeFermatQuotientDistributionBeyondLiftTransitivity` |
| Goldbach | `PrimeModulusRationalFourierFullSupportAndNormBarrier` | rational realization of the exact two-spike model | `QuantitativePrimeCountFourierEnergyAntiConcentrationAtPrimeModuli` |
| Twin | `AllBaseEvenLeftRightActiveClassification` | any extra even-left contaminant | `ScaleLocalOddLeftRightActiveContaminationBound` |

## Formal completion decision

No proof DAG reaches a parent conjecture or its negation. No candidate
resolution exists. TICKET-250 is complete as an iteration and incomplete as a
four-conjecture program.
