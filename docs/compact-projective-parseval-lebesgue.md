# TICKET-249: Compact perturbations, projective Fermat quotients, Parseval spikes, and active-power classification

- `iteration_complete`: true
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- `new_partial_theorem_count`: 2
- `exact_no_go_count`: 2
- `stagnated_problem_count`: 0
- deep focus: twin-prime conjecture
- parent: TICKET-248
- program status: `open_not_proven`

TICKET-249 proves four project-local auxiliary results. It does **not** prove
or disprove the Riemann hypothesis, Collatz conjecture, strong Goldbach
conjecture, or twin-prime conjecture.

## Reproduction contract

```powershell
python scripts/ticket249_compact_projective_parseval_lebesgue.py
python -m unittest tests.test_ticket249_compact_projective_parseval_lebesgue -v
python scripts/verify_ticket249_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket249-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

The generator is deterministic and has no random seed. Every finite proof
certificate uses integers or `Fraction`; JSON floating companions are display
only. Trigonometric floating point is not used in the Goldbach certificate.

| Problem | Exact proposition decided in this ticket | Classification | Parent status |
|---|---|---|---|
| Riemann | every compact off-diagonal perturbation still has zero coercivity along the TICKET-248 Legendre escape sequence on the full even `L2` model | `exact_no_go` | `open_not_proven` |
| Collatz | the separated generalized-Wieferich condition is exactly the nonzero projective Fermat-quotient point `[3:5]` | `partial_theorem` | `open_not_proven` |
| Strong Goldbach | centered first-jet Parseval energy can concentrate exactly on two reduced numerators, blocking any Parseval-only uniform promotion | `exact_no_go` | `open_not_proven` |
| Twin Prime | left-active even-exponent contamination with base other than `3` is exactly the single pair `(25,27)` | `partial_theorem` | `open_not_proven` |

## 1. Riemann hypothesis

### A. Exact proposition: `CompactOffDiagonalMomentCoercivityNoGo`

Let

```text
H=L2_even([-1,1]),
f_n=sqrt((4n+1)/2) P_(2n),
Q0(f)=sum_(k>=0) |integral_(-1)^1 x^(2k)f(x)dx|^2.
```

For every bounded compact operator `K:H->H`,

```text
||f_n||=1,
Q0(f_n)<=11/n,
<Kf_n,f_n> -> 0.                                  (RH-249)
```

Consequently there is no `c>0` such that

```text
Q0(f)+Re<Kf,f> >= c||f||^2
```

for all `f in H`.

### B-D. Definitions, proof, and grounds for each inference

The sequence `(f_n)` is orthonormal by Legendre orthogonality and therefore
weakly null. A compact operator maps a bounded weakly null sequence to a
norm-null sequence. Indeed, if `||Kf_n||` did not tend to zero, compactness
would give a norm-convergent subsequence with a nonzero limit; boundedness of
`K` and weak convergence show every scalar product of that subsequence tends
to zero, forcing the limit to be zero. Hence

```text
|<Kf_n,f_n>| <= ||Kf_n|| -> 0.
```

TICKET-248 analytically proved `Q0(f_n)<=11/n`. Substituting `f_n` into a
putative coercive inequality and taking `n->infinity` gives `c<=0`, a
contradiction.

### E-G. Adversarial and reproducible computation

The exact replay uses `n=2,4,8,16,32,64,128,256`. For each `n`, it projects
`f_n` onto the first `n` normalized even Legendre modes and obtains projection
energy exactly zero. It also sums the first eight nonzero raw moment energies
as a `Fraction` and checks that this partial energy is below `11/n`.

- rows: 8;
- arithmetic: exact rational;
- failures: 0;
- transcript SHA-256:
  `eaaa5e2eccd9fa1fcb32504240f86c5ecff7d815eb4d218a5eb22e9248bb999a`.

The finite-rank rows are a second check, not the proof for arbitrary compact
`K`. The arbitrary-compact conclusion is the weak-convergence argument.

### H-I. Finite limit and classification

This theorem applies to the full even `L2` model. It neither proves that the
actual Guinand-Weil arithmetic correction is compact nor places the Legendre
sequence in the normalized admissible closure. Classification: `exact_no_go`;
RH remains `open_not_proven`.

### J-K. Minimal remaining gap and next lemma

```text
NoncompactArithmeticWeilFormOrLegendreExclusion
```

One must either control a genuinely noncompact arithmetic Weil form on the
actual admissible closure or prove that the Legendre escape sequence cannot be
approximated in that closure.

## 2. Collatz conjecture

### A. Exact proposition: `SeparatedWieferichProjectiveSlopeCriterion`

For a prime `q>5`, put

```text
U_q=((2^(q-1)-1)/q) mod q,
V_q=((3^(q-1)-1)/q) mod q.
```

The TICKET-248 bad condition

```text
W_q(32,27)=0 and W_q(2,3)!=0
```

holds exactly when there is a unique `t in F_q^*` such that

```text
(U_q,V_q)=t(3,5).                                  (CO-249)
```

Thus the bad set asks whether the actual Fermat-quotient projective point hits
the single target `[3:5]`, with the origin excluded.

### B-D. Proof

The Fermat quotient satisfies `q_q(a^m)=m q_q(a) mod q`. Therefore

```text
W_q(32,27)=5U_q-3V_q,
W_q(2,3)=U_q-V_q.
```

The first form vanishes exactly when `U_q=3t`, `V_q=5t`, where
`t=U_q/3` is unique. On this line, `U_q-V_q=-2t`, which is nonzero exactly
when `t!=0` because `q>5`.

### E-G. Counterexample search and exact replay

Two independent checks are recorded.

1. Exhaustive enumeration of every `(u,v) in F_q^2` for
   `q=7,11,23,101` checks 10,900 pairs. The zero line has `q` points and its
   nonzero projectivization has `q-1` points in every field.
2. Exact modular exponentiation modulo `q^2` scans every prime
   `5<q<=10,000,000`.

The actual scan covers 664,576 primes. It finds no zero of `W_q(32,27)`, the
single zero `q=23` of `W_q(2,3)`, and no separated hit.

- complexity: `O(B log log B + pi(B) log B)` plus the small-field checks;
- arithmetic: exact integer modular;
- failures: 0;
- transcript SHA-256:
  `db860c5bef6ae1b016d468346b1b9941eac90c375f93d4f7c4f67c8ee8e881b7`.

### H-I. Finite limit and classification

The projective criterion is an all-prime algebraic theorem. The no-hit scan is
only a finite certificate; it proves neither occurrence nor global avoidance
of `[3:5]`. Even deciding this valuation branch would not control every
Collatz trajectory. Classification: `partial_theorem`; Collatz remains
`open_not_proven`.

### J-K. Minimal remaining gap and next lemma

```text
OccurrenceOrAvoidanceOfProjectiveFermatQuotientSlopeThreeFifths
```

The older two-congruence view is retired. The actual arithmetic task is now a
distribution theorem or one exact occurrence for the fixed projective point.

## 3. Strong Goldbach conjecture

### A. Exact proposition: `CenteredJetParsevalSpikeNoGo`

Fix `q>=3` and a reduced `a0 mod q`. For all residues `r`, let

```text
delta_r=cos(2*pi*a0*r/q),
eta_r=c delta_r,
J_a(t)=sum_r (delta_r+i t eta_r) exp(2*pi*i*a*r/q).
```

Then `delta` and `eta` are centered,

```text
D0=q/2,  D1=c^2q/2,
J_a(t)=0 unless a=+a0 or -a0,
|J_(+/-a0)(t)|^2=q(D0+t^2D1)/2.                  (GB-249)
```

Hence centeredness and the TICKET-248 Parseval identity alone cannot imply a
uniform `o(sqrt(q(D0+t^2D1)))` bound over reduced numerators.

### B-D. Exact countermodel proof

With `zeta=exp(2*pi*i/q)`,

```text
2delta_r=zeta^(a0 r)+zeta^(-a0 r).
```

Root-of-unity orthogonality gives `2R0(a)=q` at `a=+/-a0` and zero
elsewhere. These frequencies are distinct because a reduced `a0` cannot
satisfy `2a0=0 mod q` for `q>=3`. Thus the total Parseval energy is `q^2/2`
and each spike carries `q^2/4`. Since `eta=c delta`, multiplication by
`1+itc` multiplies every energy by `1+t^2c^2`.

### E-G. Adversarial exact replay

The generator replaces roots of unity by the integer rule

```text
sum_(r mod q) zeta^(kr) = q if q divides k, and 0 otherwise.
```

It checks every reduced `a0` for `3<=q<=128`:

- reduced-frequency cases: 5,020;
- selected rows: 13;
- each spike/total squared-energy ratio: exactly `1/2`;
- arithmetic: integers and rational numbers only;
- failures: 0;
- transcript SHA-256:
  `439a6562998de91c99533ceacb5ac53d177af9e48165ee51c4eed6ec782d59fe`.

### H-I. Scope and classification

The countermodel is a real centered residue vector, not an actual vector of
prime counts or prime first moments. It refutes only the logical promotion
from abstract centeredness plus Parseval energy to uniform control. It does
not refute prime-specific arithmetic anti-concentration. Classification:
`exact_no_go`; strong Goldbach remains `open_not_proven`.

### J-K. Minimal remaining gap and next lemma

```text
PrimeSpecificReducedNumeratorJetAntiConcentration
```

Any successful next step must use arithmetic structure absent from arbitrary
centered vectors, rather than another manipulation of the same aggregate
energy identity.

## 4. Twin-prime conjecture — deep focus

### A. Exact proposition: `EvenExponentLeftActiveContaminationClassification`

Let `p,r` be odd primes and `m,ell>=1`. If

```text
p!=3 and p^(2m)+2=r^ell,
```

then

```text
(p,m,r,ell)=(5,1,3,3).                            (TP-249)
```

Consequently the TICKET-248 left-active contamination with even exponent and
base different from `3` is exactly the single pair `(25,27)`:

```text
L_even,p!=3(X) = 1_(X>=25).
```

### B-D. Proof and external dependency

Set `x=p^m`. Since `p!=3`, `x^2=1 mod 3`, so `x^2+2` is divisible by `3`.
Because the right side is a prime power, `r=3`. The cases `ell=1,2` give
`x=1` and `x^2=7`, respectively, and are impossible here. For `ell>=3`, use
the classical `D=2` Lebesgue-Nagell classification:

```text
x^2+2=y^n, x,y>0, n>=3  =>  (x,y,n)=(5,3,3).
```

It follows that `p^m=5`, hence `p=5,m=1`. The external result is represented
as an `external_theorem` node, not as a PrimeProject proof. A modern primary
source solving `x^2+D=y^n` for `1<=D<=100` is Bugeaud, Mignotte, and Siksek,
[Compositio Mathematica 142 (2006), 31-62](https://doi.org/10.1112/S0010437X05001739).

### E-G. Exact active-support replay

An exact prime-power representation table enumerates all shift-two active
pairs through `X=10,000,000` and splits left-composite terms into:

```text
even exponent, base !=3;
even exponent, base =3;
odd exponent.
```

At `X=10,000,000` the counts are respectively `1,5,8`, summing to `L=14`;
the right-active count is `R=136`. The unique first class witness is `(25,27)`.

- scales: 7;
- arithmetic: exact integer;
- complexity: `O(X log log X)` time and `O(X)` support memory;
- failures: 0;
- transcript SHA-256:
  `6df796f1387e44725a337fc60d5fe44a94e2521496caf1cdc39e30bba96f6fd9`.

### H-I. Finite and logical limits

The all-`X` classification follows from the external Diophantine theorem, not
from the ten-million replay. It controls only the left-active, even-exponent,
base-not-3 subclass. The right-active class remains much larger, and no
scale-local Type-II lower bound for the prime-power proxy has been proved.
Classification: `partial_theorem`; the twin-prime conjecture remains
`open_not_proven`.

### J-K. Minimal remaining gap and next lemma

```text
ScaleLocalRightActivePrimePowerContaminationBound
```

The next task is a scale-local upper bound for prime powers on the right of an
active shift-two pair; only after controlling the correction can it be
compared with a nonperiodic Type-II lower bound for the proxy.

## Proof DAG and adversarial audit

Every problem has an acyclic proof DAG with one `open` frontier. The Twin DAG
also contains the `external_theorem` node for the `D=2` Lebesgue-Nagell
classification. No `assumption`, `heuristic`, or `open` node is counted as a
proved parent-conjecture dependency.

| Track | Proved TICKET-249 node | Disproved route node | Open frontier |
|---|---|---|---|
| RH | compact perturbation no-go | compact repair of full-sphere coercivity | noncompact Weil form or Legendre exclusion |
| Collatz | projective slope criterion | two independent coordinate congruences | occurrence/avoidance of `[3:5]` |
| Goldbach | exact two-spike countermodel | Parseval-only uniform promotion | prime-specific jet anti-concentration |
| Twin | even-left active classification | arbitrary away-from-3 even-left family | right-active contamination bound |

Adversarial checks confirm that no finite scan was promoted to an infinite
claim, no average was promoted to a pointwise prime theorem, and the external
Diophantine dependency is explicit. Resolution and candidate-resolution
counts remain zero.
