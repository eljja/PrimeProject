# TICKET-248: unweighted moments, generalized-Wieferich separation, centered first jets, and active contamination

## Status declaration

- `iteration_complete`: true
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- `new_partial_theorem_count`: 3
- `exact_no_go_count`: 1
- `stagnated_problem_count`: 0
- deep focus: strong Goldbach conjecture
- parent: TICKET-247
- program status: `open_not_proven`

This ticket proves four project-local auxiliary results. It does not prove or
disprove the Riemann hypothesis, Collatz conjecture, strong Goldbach
conjecture, or twin-prime conjecture.

## Reproduction contract

```powershell
python scripts/ticket248_unweighted_wieferich_jet_active.py
python -m unittest tests.test_ticket248_unweighted_wieferich_jet_active -v
python scripts/verify_ticket248_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket248-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

All certificate computations use integers or `Fraction`. Floating companions
in JSON are display-only. The computation is deterministic and has no random
seed.

| Problem | New result | Classification | Status |
|---|---|---|---|
| Riemann | raw unweighted infinite even moments have zero coercivity on the full normalized even `L2` sphere | `exact_no_go` | `open_not_proven` |
| Collatz | the actual first-level bad branch is exactly a difference of two generalized-Wieferich prime sets | `partial_theorem` | `open_not_proven` |
| Strong Goldbach | a centered first-jet arc expansion has an exact joint Parseval energy identity and quadratic remainder | `partial_theorem` | `open_not_proven` |
| Twin Prime | only composite prime powers with an actual shift-two prime-power neighbor enter the exact contamination correction | `partial_theorem` | `open_not_proven` |

## 1. Riemann hypothesis

### A. Exact proposition: `UnweightedInfiniteMomentCoercivityNoGo`

Let

```text
H=L2_even([-1,1]),
Q_0(f)=sum_(k>=0) |integral_(-1)^1 x^(2k)f(x)dx|^2,
```

where `Q_0` may initially be infinite. For `n>=1`, put

```text
f_n=sqrt((4n+1)/2) P_(2n).
```

Then `||f_n||_2=1`, the first `n` even moments vanish, `Q_0(f_n)` is
finite, and

```text
Q_0(f_n) <= 11/n -> 0.                              (RH-248)
```

The unweighted family is outside the TICKET-247 Hilbert-Schmidt hypothesis
because `sum 2/(4k+1)` diverges. Nevertheless it still has no positive
uniform coercivity lower bound on the full even `L2` unit sphere.

### B-D. Definitions and proof

Legendre orthogonality gives the vanished moments and norm. For `k>=n`,
Rodrigues integration, independently checked by factorial and product forms,
gives

```text
mu_(n,k)=integral x^(2k)P_(2n)(x)dx
 = 2/(2k+1) product_(j=1)^n (k-j+1)/(k+j+1/2).
```

Every product factor is positive and

```text
(k-j+1)/(k+j+1/2)
 = 1-(2j-1/2)/(k+j+1/2).
```

Using `1-u<=exp(-u)` and summing the exponents yields

```text
mu_(n,k) <= 2/(2k+1) exp(-n^2/(k+n+1)).
```

Since `k+n+1<=3k`, the normalized squared moment is at most

```text
((4n+1)/2) k^(-2) exp(-2n^2/(3k)).
```

For the nonnegative unimodal function

```text
g(x)=x^(-2)exp(-2n^2/(3x)),
```

splitting the integer sum on the two sides of its maximum proves
`sum g(k)<=integral g+2 sup g`. The integral is `3/(2n^2)` and the
maximum is `9e^(-2)/n^4<9/(7n^4)` because `e^2>7`. Hence

```text
Q_0(f_n)
 <= (4n+1)/2 (3/(2n^2)+18/(7n^4))
 < 11/n.
```

This is an all-`n` proof, not an extrapolation from the finite table.

### E-G. Adversarial and reproducible checks

For half-degrees `1,2,4,8,16,32,64,128`, the generator:

- constructs `P_(2n)` by recurrence and Rodrigues coefficients;
- checks every required vanished moment and exact norm;
- compares the factorial and product moment formula at four indices;
- sums exact rational energy through `k=256`;
- records both a simple post-cutoff bound and the analytic `11/n` bound.

There are eight rows and zero failures. Transcript SHA-256:
`faaba3834a933146319b810147b5d58136ae13d23bd6599297b292d2ba33c1bd`.

### H-I. Limit and classification

The sequence belongs to the full even `L2` model. It has not been shown to
belong to the normalized Guinand-Weil admissible closure. The theorem also
does not exclude non-diagonal arithmetic features. Classification:
`exact_no_go`. RH remains `open_not_proven`.

### J-K. Remaining gap and next lemma

```text
ArithmeticOffDiagonalWeilCoercivityOnAdmissibleClosure
```

## 2. Collatz conjecture

### A. Exact proposition: `ActualBadBranchGeneralizedWieferichSeparation`

For every prime `q>5`, define

```text
U_q=(2^(q-1)-1)/q,
V_q=(3^(q-1)-1)/q,
W_q(a,b)=((a^(q-1)-b^(q-1))/q) mod q.
```

For the TICKET-246 polynomial `P_q`, exactly

```text
P_q(U_q,V_q) = W_q(32,27) mod q,
U_q-V_q       = W_q(2,3) mod q.                  (CO-248)
```

Thus the actual pair violates the first-level domination precisely for

```text
q in {W_q(32,27)=0} minus {W_q(2,3)=0}.
```

These are separated generalized-Wieferich primes for the two rational bases.

### B-D. Proof

TICKET-246 proved the exact integer identities

```text
32^(q-1)-27^(q-1)=qP_q(U_q,V_q),
2^(q-1)-3^(q-1)=q(U_q-V_q).
```

Divide by `q` and reduce modulo `q`. Therefore `v_q(P_q)>0` while
`v_q(U_q-V_q)=0` if and only if the first base difference is divisible by
`q^2` and the second is not. No unrestricted formal pair is used here.

### E-G. Exact modular scan

The generator scans all 78,495 primes `5<q<=1,000,000` with modular
exponentiation modulo `q^2`.

- `W_q(32,27)=0`: no hits;
- `W_q(2,3)=0`: `q=23` only;
- separated hits: none;
- arithmetic: exact integer modular arithmetic;
- complexity: `O(pi(B) log B)` modular multiplications;
- failures: zero;
- transcript SHA-256:
  `444834a2768b3e94e21d0f968aef0e93fd87f08c540ca52af08756480b6d2d25`.

### H-I. Limit and classification

The finite absence does not prove the separated set empty. The result is the
exact reduction, not an all-prime exclusion. Even an all-prime valuation
theorem would still lack a global Collatz trajectory argument. Classification:
`partial_theorem`; Collatz remains `open_not_proven`.

### J-K. Remaining gap and next lemma

```text
ExistenceOfSeparatedGeneralizedWieferichPrimeFor32Over27Against2Over3
```

Finding one such prime would close the proposed actual valuation-domination
route by exact counterexample; absence through any finite bound cannot do so.

## 3. Strong Goldbach conjecture — deep focus

### A. Exact proposition: `CenteredFirstJetParsevalArcBridge`

Fix `q>=3`, `X>=3`. For reduced residues `r mod q`, let `n_r` count odd
primes `p<=X` coprime to `q`, and let `m_r` be their sum. Put

```text
P=sum n_r,       M=sum m_r,
delta_r=n_r-P/phi(q),
eta_r=m_r-M/phi(q),
D_0=sum delta_r^2,
D_1=sum eta_r^2,
R_0(a)=sum delta_r exp(2pi i ar/q),
R_1(a)=sum eta_r exp(2pi i ar/q).
```

For every real `t`,

```text
sum_(a mod q)|R_0(a)+itR_1(a)|^2
 = q(D_0+t^2D_1).                                (GB-248a)
```

For every real `beta`, with `M_2=sum p^2`,

```text
S*(a/q+beta)
 = c_q(a)(P+2pi i beta M)/phi(q)
   +R_0(a)+2pi i beta R_1(a)+E(a,beta),

|E(a,beta)| <= 2pi^2 beta^2 M_2.                 (GB-248b)
```

### B-D. Proof

The integral Taylor remainder gives

```text
|exp(iu)-1-iu|<=u^2/2.
```

Apply it with `u=2pi beta p` and sum over primes to get (GB-248b).
Additive orthogonality gives

```text
sum_a |R_0(a)|^2=qD_0,
sum_a |R_1(a)|^2=qD_1,
sum_a R_0(a)conjugate(R_1(a))=q sum_r delta_r eta_r.
```

The last quantity is real. Consequently the cross term introduced by the
factor `it` has zero total real part, proving (GB-248a). Markov's inequality
then bounds the number of exceptional numerators for any chosen threshold.

### E-G. Exact computation

For `X=10,000,100,000,500,000` and every `q=3..96`, the generator computes

```text
phi D_0=phi sum n_r^2-P^2,
phi D_1=phi sum m_r^2-M^2,
phi C  =phi sum n_rm_r-PM
```

as exact integers, independently reconstructs the three centered rational
sums, and checks `C^2<=D_0D_1` after clearing denominators.

- denominator cases: 282;
- selected rows: 36;
- failures: zero;
- random seed: none;
- transcript SHA-256:
  `49d39cfb54e21607b0ad1e39ddf0734d30d646bab71b90b82fb746a3f80cc18a`.

### H-I. Limit and classification

Parseval controls the average over numerators, not every numerator. No
uniform growing-denominator bound for `D_0`, `D_1`, or their Fourier spikes is
proved. The finite table therefore proves neither major-arc positivity nor
strong Goldbach. Classification: `partial_theorem`; status
`open_not_proven`.

### J-K. Remaining gap and next lemma

```text
UniformReducedNumeratorCenteredFirstJetSavingOnQuarterTorus
```

## 4. Twin-prime conjecture

### A. Exact proposition: `ExactActivePrimePowerContaminationIdentity`

Let `PP(n)` indicate an odd prime power, `P(n)` an odd prime, and
`C(n)=PP(n)-P(n)`. For odd `n<=X`, define

```text
A_2=sum PP(n)PP(n+2),
pi_2=sum P(n)P(n+2),
L=sum C(n)PP(n+2),
R=sum PP(n)C(n+2),
B=sum C(n)C(n+2).
```

Then for every `X>=3`,

```text
A_2(X)-pi_2(X)=L(X)+R(X)-B(X)<=L(X)+R(X).        (TP-248)
```

### B-D. Proof

Inside the prime-power-pair support, a false twin pair is the union of the
events “left coordinate is composite” and “right coordinate is composite.”
Two-event inclusion-exclusion gives its indicator as

```text
C(n)PP(n+2)+PP(n)C(n+2)-C(n)C(n+2).
```

Summation proves the identity. Composite prime powers without a shift-two
prime-power neighbor are absent from all three active terms.

### E-G. Exact enumeration

At `X=10,000,000`, exact support scans give

```text
A_2=59,129, pi_2=58,980,
L=14, R=136, B=1,
A_2-pi_2=L+R-B=149,
L+R=150.
```

The TICKET-247 correction was 2,822 at the same scale. Seven exact scales
through `10^7` have zero failures. Transcript SHA-256:
`85f69edcdb7bc23ce3a41d770918c5a4589b4b50a4e003145c47874fa2bd1741`.

### H-I. Limit and classification

The active correction is exact but depends on shift-two prime-power support;
no analytic lower bound makes `A_2` exceed it on unbounded scales. Finite twin
counts do not prove infinitude. Classification: `partial_theorem`; status
`open_not_proven`.

### J-K. Remaining gap and next lemma

```text
ScaleLocalTypeIILowerBoundBeyondActivePrimePowerContamination
```

## Adversarial proof audit

- RH does not move a full-`L2` Legendre sequence into the genuine Weil class.
- Collatz does not turn 78,495 finite misses into an all-prime statement.
- Goldbach does not exchange mean-square control for a uniform numerator
  estimate.
- Twin does not infer infinitude from seven finite scales.
- All denominators are positive, all finite certificates use exact arithmetic,
  and no conjecture is used as an assumption in its own proof DAG.
- Each proof DAG is acyclic with exactly one `open` frontier.

## Final boundary

TICKET-248 completes one exact route no-go, three partial theorems, their
deterministic certificates, and four sharper next lemmas. None of the four
conjecture-resolution gates is passed.
