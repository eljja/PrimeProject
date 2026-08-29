# TICKET-256: Cesaro lag sums, a sharp incomplete kernel, q-divisible reflection, and a GL2 survivor reduction

- parent: TICKET-255
- deep focus: twin-prime exponent-17 Diophantine obstruction
- `iteration_complete`: true
- `program_complete`: false
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- classifications: four `partial_theorem`
- all four parent problems: `open_not_proven`

TICKET-256 proves four project-local auxiliary statements. It does **not**
prove or disprove the Riemann hypothesis, Collatz conjecture, strong Goldbach
conjecture, or twin-prime conjecture. Completing this iteration means that its
declared propositions and artifacts pass the stated audit; it is not a parent
problem resolution.

## Reproduction contract

```powershell
python scripts/ticket256_cesaro_kernel_qdiv_gl2.py
python -m unittest tests.test_ticket256_cesaro_kernel_qdiv_gl2 -v
python scripts/verify_ticket256_structure.py
python -m unittest discover -s tests
python scripts/verify_open_problem_structure.py
node --check assets/ticket256-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

The generator is deterministic. Every proof certificate uses integers or
`Fraction`. Complex roots of unity are represented by exact residue exponents;
no floating-point complex value is used as proof. `display_float` fields in
the JSON are presentation-only. No random seed is used.

| Problem | Exact proposition | Classification | Parent status |
|---|---|---|---|
| Riemann | `ToeplitzPacketCesaroLagPartialSumCriterion` | `partial_theorem` | `open_not_proven` |
| Collatz | `SharpIncompleteKernelErrorAndDecayOnlyPrimeAverage` | `partial_theorem` | `open_not_proven` |
| Strong Goldbach | `QDivisibleReflectionAsymmetryPrimePrefixExclusion` | `partial_theorem` | `open_not_proven` |
| Twin Prime | `SurvivingTwistGL2EquivalenceAndSingleAbsoluteBranchReduction` | `partial_theorem` | `open_not_proven` |

## 1. Riemann hypothesis track

### A. Exact proposition

Let `(a_k)_(k>=0)` be real, let

```text
T_L=(a_|r-s|)_(0<=r,s<L),
d_L=L^(-1/2)(1,...,1),
E_L=<d_L,T_L d_L>,
S_n=a_0+2 sum_(k=1)^n a_k.
```

Then, for every integer `L>=1`,

```text
E_L = (1/L) sum_(n=0)^(L-1) S_n.                  (RH-256)
```

Thus `S_n>=c` for every `n` is sufficient for `E_L>=c` at every packet
size. It is not necessary: the infinite lag sequence

```text
a_0=1, a_1=-1, a_2=1, a_k=0 (k>=3)
```

has `S_1=-1`, but `E_1=1`, `E_2=0`, and `E_L=(L-2)/L>=0` for `L>=3`.

If true, the identity replaces the TICKET-255 matrix aggregate target by one
explicit scalar partial-sum target. If the sufficient condition were shown
false for actual Weil lags, only this sufficient route would fail; packet
positivity could still hold, as the counterexample to necessity shows.

### B-D. Definitions and proof

Lag `0` occurs `L` times in the quadratic sum, while lag `k>=1` occurs
`2(L-k)` times. Therefore

```text
E_L=a_0+2 sum_(k=1)^(L-1)(1-k/L)a_k.
```

Reversing the order in the sum of `S_n` gives

```text
sum_(n=0)^(L-1)S_n
=L a_0+2 sum_(k=1)^(L-1)(L-k)a_k
=L E_L.
```

This proves the identity and its lower-bound consequence without a limiting
argument. The displayed counterexample has partial sums `1,-1,1,1,...`; their
finite Cesaro means give the listed nonnegative energies. It exactly refutes
necessity, not sufficiency.

### E-G. Adversarial computation and interpretation

The generator replays `L=1,...,12` using exact rational arithmetic. Every row
recomputes the lag coefficients, all `S_n`, the direct Toeplitz packet energy,
and the Cesaro mean. Failures: `0`.

- algorithm: exact lag counting and rational summation;
- complexity: `O(sum L)` for the replay; the proof is algebraic for every `L`;
- checked cases: `12`;
- minimum adversarial partial sum: `-1`;
- transcript SHA-256:
  `a4d61abe3161c28b13f5f333e2fae644f2c9171107dde94d92e38adc6b8615d1`.

### H-I. Logical and finite limits; classification

The twelve rows only replay an all-`L` identity. More importantly, the
sequence in the counterexample is abstract. TICKET-256 neither identifies it
with actual Guinand-Weil lags nor estimates the actual signed archimedean and
prime-power terms. No zero-free region follows. Classification:
`partial_theorem`; RH remains `open_not_proven`.

### J-K. Minimum gap and next single lemma

Remaining gap: prove the required lower bound for the scalar partial sums of
the actual packet lags. Next:

```text
ActualWeilSymmetricLagPartialSumsHaveUniformLowerBound
```

## 2. Collatz conjecture track

### A. Exact proposition

For prime `q`, omitted frequency `h_0 in F_q`, and `D in F_q`, define

```text
K_(q,h_0)(D)=q^(-1) sum_(h!=h_0) exp(2 pi i hD/q).
```

Then

```text
K_(q,h_0)(D)=delta_0(D)-q^(-1)exp(2 pi i h_0D/q),   (CO-256a)
||delta_0-K_(q,h_0)||_infinity=1/q.                 (CO-256b)
```

The bound `1/q` is minimax-sharp over every approximation whose Fourier
support omits `h_0`. At the canonical residue

```text
D_q=5F_q(2)-3F_q(3) mod q,
F_q(a)=(a^(q-1)-1)/q mod q,
```

the unnormalized Cesaro average of the complex errors tends to zero in
absolute value. This last statement is decay-only; it does not prove
cancellation of the renormalized phases.

### B-D. Definitions and proof

The complete additive-character expansion of `delta_0` contains every
frequency with coefficient `1/q`. Removing `h_0` proves (CO-256a) and (b).
For an arbitrary kernel supported on a proper set missing `h_0`, the error's
Fourier coefficient at `h_0` remains `1/q`. A normalized Fourier coefficient
has magnitude at most the sup norm, so no such kernel has smaller uniform
error. The one-omission kernel attains the bound.

If `q_j` denotes the `j`th selected prime, then `q_j>=j+1`, so

```text
(1/n)sum_(j<=n)1/q_j <= (1/n)sum_(j<=n)1/(j+1) -> 0.
```

The triangle inequality proves decay of the canonical error average. It uses
no information about `D_q`; multiplying the error by `q` removes this decay.

### E-G. Adversarial computation and interpretation

For all 22 primes `7<=q<=97`, the generator computes `F_q(2)`, `F_q(3)`,
`D_q`, the exact magnitude `1/q`, and its running rational mean. The root of
unity is stored only as exponent `D_q mod q`. Failures: `0`.

- algorithm: modular exponentiation and exact rational accumulation;
- complexity: `O(sum log q)` modular multiplications for the replay;
- checked cases: `22` primes;
- transcript SHA-256:
  `e50be6fa63328562b64c1fa1023ad706493a60e47d84705d24aebec05d412de3`.

### H-I. No-go boundary and classification

Discarded: calling an unnormalized `O(1/q)` mean “cross-prime cancellation.”
The theorem controls an approximate kernel but says nothing about the
renormalized phases, occurrence of the projective Fermat-quotient slope, or
arbitrary Collatz trajectories. The finite rows do not establish a density
law. Classification: `partial_theorem`; Collatz remains `open_not_proven`.

### J-K. Minimum gap and next single lemma

The remaining arithmetic question begins only after the trivial `1/q` scale
is removed. Next:

```text
RenormalizedCanonicalSlopePhasesHaveNontrivialCrossPrimeCancellation
```

## 3. Strong Goldbach conjecture track

### A. Exact proposition

Let `q>=5` be prime, let `q|m`, and fold `(1-X)^m` modulo `X^q-1`:

```text
c_r=sum_(j congruent r mod q)(-1)^j binom(m,j).
```

Put `t=1-c_0` and suppose the TICKET-253 zero-residue compatibility conditions

```text
t>0,  c_r+t>=0 for every r
```

hold. Then `m` is even. Furthermore

```text
c_(-r)=c_r,
N*_r=c_r+t=N*_(-r).                                (GB-256)
```

Hence, with `T=qt`, any actual first-`T`-prime residue vector satisfying
`N_r(T)!=N_(-r)(T)` for at least one `r` cannot realize the candidate tail.

### B-D. Parity obstruction and reflection proof

The involution `j -> m-j` gives

```text
c_(m-r)=(-1)^m c_r.
```

If `q|m` and `m` were odd, then `c_(-r)=-c_r` and `c_0=0`. Thus `t=1`;
compatibility at both `r` and `-r` forces every integer `c_r` into `[-1,1]`,
so `sum c_r^2<=q`.

Parseval for the cyclic coefficients gives

```text
sum_r c_r^2 = q^(-1)sum_(a=0)^(q-1)|1-zeta_q^a|^(2m).
```

At `a=(q-1)/2`,

```text
|1-zeta_q^a|^2=4cos^2(pi/(2q))
              >=4cos^2(pi/10)=(5+sqrt(5))/2>3.
```

Because `m>=q>=5` and `3^q>q^2`, Parseval gives `sum c_r^2>q`, a
contradiction. Therefore `m` is even, and the same involution gives (GB-256).
The actual asymmetry conclusion then follows from the unique-prefix criterion.

### E-G. Exact prefix certificates

The scan uses `q in {5,7,11,13,17,19}`, every positive multiple `m<=160` of
`q`, and prime prefixes only when `T<=100,000`. It finds 97 scanned pairs,
49 odd pairs, 25 compatible pairs, no odd compatible pair, and two bounded
prime-prefix certificates:

| q | m | t | T | forced symmetric counts | actual first-T counts | asymmetry |
|---:|---:|---:|---:|---|---|---|
| 5 | 10 | 251 | 1,255 | `[1,451,176,176,451]` | `[1,313,313,317,311]` | `[0,2,-4,4,-2]` |
| 7 | 14 | 3,431 | 24,017 | `[1,6420,1520,4068,4068,1520,6420]` | `[1,3993,3991,4003,3998,4016,4015]` | `[0,-22,-25,5,-5,25,22]` |

All arithmetic is integral; failures: `0`. Trial division reaches the
24,017th prime, `274783`.

- complexity: `O(sum m)` for coefficient folding plus deterministic trial
  division through the largest prefix;
- transcript SHA-256:
  `6ded0f179c955a164110a035c40971e60b948905edbb9c3377af7ac985ef8619`.

### H-I. Finite boundary and classification

The parity obstruction and conditional reflection test are infinite algebraic
statements. Only two actual prefixes are enumerated. The other 23 compatible
rows in the scan already exceed the prefix limit, and exponents above 160 are
not scanned. Therefore the calculation cannot show that every even
`q`-divisible candidate has actual reflection asymmetry. Classification:
`partial_theorem`; strong Goldbach remains `open_not_proven`.

### J-K. Minimum gap and next single lemma

Remaining gap: force at least one actual residue-pair imbalance for every
compatible even `q`-divisible prefix. Next:

```text
EveryQDivisibleCompatibleEvenTailHasPrimePrefixReflectionAsymmetry
```

## 4. Twin-prime conjecture track — deep focus

### A. Exact proposition

Let `epsilon=1+sqrt(2)` and define

```text
epsilon^j(u+v sqrt(2))^17=A_j(u,v)+B_j(u,v)sqrt(2).
```

For the two TICKET-255 survivors `j=1,16`, put

```text
T(u,v)=(-u-2v,u+v).
```

Then `T in GL_2(Z)` and, for every `(u,v) in Z^2`,

```text
B_16(T(u,v))= B_1(u,v),
A_16(T(u,v))=-A_1(u,v),
N(T(u,v))   =-N(u,v).                               (TP-256)
```

Thus the union of admissible points on twists 1 and 16 is in bijection with
the single absolute branch

```text
B_1(u,v)=1,  -(u^2-2v^2)>0,
x=|A_1(u,v)|.
```

### B-D. Algebraic proof

The matrix and inverse are

```text
T    = [[-1,-2],[ 1, 1]],  det(T)=1,
T^-1 = [[ 1, 2],[-1,-1]].
```

For `alpha=u+v sqrt(2)`, direct multiplication gives

```text
T(alpha)=epsilon^(-1) conjugate(alpha).
```

Since `conjugate(epsilon)=-epsilon^(-1)`, we obtain

```text
epsilon^16 T(alpha)^17
=epsilon^(-1)conjugate(alpha)^17
=-conjugate(epsilon alpha^17),
```

which proves the `A/B` identities. Since `N(epsilon)=-1`, the norm identity
also follows. A positive `A_1` gives twist 1, while a negative `A_1` maps to a
positive `A_16`; the integral inverse proves surjectivity. Finally,
`B_1=1` and `-N(alpha)>0` imply

```text
A_1^2-2=(-N(alpha))^17>0,
```

so `A_1` is nonzero and the absolute-value branch is exact.

### E-G. Adversarial replay

Every integer pair in `[-64,64]^2` is checked using independent quadratic-ring
exponentiation for twists 1 and 16, plus forward and inverse matrix maps.
The test explicitly uses the correct sign
`N(T(u,v))=-N(u,v)`; this guards the sign error most likely to invalidate the
branch correspondence.

- exact grid cases: `16,641`;
- identity failures: `0`;
- coefficient-one points in the box: one, `(u,v)=(1,0)`;
- its reduced `y`: `-1`, hence it is inadmissible;
- admissible points in the box: `0`;
- complexity: `O(R^2 log 17)` quadratic-ring multiplications;
- transcript SHA-256:
  `b16cc63924090d6e214ecdaaa8c47018fced6bae337cc3445ed9cbd3a85eb7a9`.

### H-I. Logical and finite limits; classification

The algebraic bijection is valid for all integer pairs; the box is only a
replay. Absence inside the box is not evidence sufficient for an all-integer
exclusion. The result reduces two global branches to one but neither solves
`B_1=1` nor excludes exponent 17 from `x^2-2=y^17`. The proxy link therefore
does not decide twin primes. Classification: `partial_theorem`; the twin-prime
conjecture remains `open_not_proven`.

### J-K. Minimum gap and next single lemma

The exact remaining exponent-17 obligation is:

```text
SingleCoefficientOneBranchHasNoNegativeNormIntegralPoint
```

## Proof DAG and completion boundary

Each track has a five-node acyclic DAG: the proved TICKET-255 parent, the
proved TICKET-256 auxiliary theorem, a `computed_finite` replay, a `disproved`
shortcut, and one `open` next lemma. No `open`, `assumption`, or `heuristic`
node is relabeled as proved. The machine audit reports four DAGs, four open
frontiers, zero candidate resolutions, zero conjecture resolutions, and zero
replay failures.

Iteration completion is not problem resolution. TICKET-256 completes its
artifact and audit contract, but all four conjectures remain unresolved.
