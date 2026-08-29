# TICKET-253: density packets, character-sum dichotomy, forced prime prefixes, and the 84-exponent frontier

- parent: TICKET-252
- `iteration_complete`: true
- `program_complete`: false
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- classifications: three `partial_theorem`, one `exact_no_go`
- deep focus: Twin Prime
- all four parent problems: `open_not_proven`

TICKET-253 proves four auxiliary propositions. It does not prove or disprove the
Riemann hypothesis, Collatz conjecture, strong Goldbach conjecture, or twin-prime
conjecture. The Twin result is a corollary of explicitly identified external
Lebesgue--Nagell results, not a new solution of that equation.

## Reproduction

```powershell
python scripts/ticket253_density_character_prefix_lebesgue.py
python -m unittest tests.test_ticket253_density_character_prefix_lebesgue -v
python scripts/verify_ticket253_structure.py
python scripts/verify_ticket252_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket253-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

All proof-bearing replay values are integers or rational numbers. No random seed
is used. Floating displays attached to rational records are not used in a proof.

| Problem | Exact TICKET-253 proposition | Classification | Parent status |
|---|---|---|---|
| Riemann | a normalized Dirichlet packet reads the symmetric density of a Fourier projection exactly in the limit | `partial_theorem` | `open_not_proven` |
| Collatz | the complete fixed-prime character sum is exactly the slope indicator and supplies no independent smoothing | `exact_no_go` | `open_not_proven` |
| Strong Goldbach | every compatible cyclotomic tail has one forced prime prefix; ten selected tails fail that exact test | `partial_theorem` | `open_not_proven` |
| Twin Prime | every prime factor of a surviving odd contamination exponent lies in an explicit 84-prime Lebesgue--Nagell frontier | `partial_theorem` | `open_not_proven` |

## 1. Riemann hypothesis

### A. Declared proposition: `DirichletPacketSpectralDensityLimit`

On `L2([-1,1])`, set

```text
e_n(x)=2^(-1/2) exp(pi i n x),
D_N=(2N+1)^(-1/2) sum_(|n|<=N) e_n.
```

For every symmetric `S subset Z`, let `P_S` be the orthogonal projection onto
the modes indexed by `S`. Then `D_N` is an even unit vector, concentrates at the
interior point zero, and

```text
<P_S D_N,D_N> = #(S intersect [-N,N])/(2N+1).       (RH-253)
```

If `S` has symmetric natural density `d`, the left side tends to `d`.

### B-D. Definitions, proof, and inference audit

Orthonormality proves the norm and coefficient-count identity. The normalized
Dirichlet-kernel formula is

```text
|D_N(x)|^2 =
 |sin((2N+1)pi x/2)/sin(pi x/2)|^2 /(2(2N+1)).
```

For fixed `epsilon>0`, integration over `epsilon<=|x|<=1` is bounded by

```text
1 / ((2N+1) sin(pi epsilon/2)^2),
```

which tends to zero. Equation (RH-253) then turns the density definition into
the asserted limit. There is no interchange of pointwise and uniform limits.

### E-G. Adversarial and reproducible computation

For the symmetric periodic set

```text
S={n in Z : n mod 6 is 1 or 5}, density(S)=1/3,
```

11 bands `N=2^s-1`, `s=3,...,13`, were counted exactly. Every row satisfies

```text
|3 #(S intersect [-N,N])-(2N+1)| <= 3.
```

Failures: zero. SHA-256:
`00bebb686b3544d67b49612c512f28feee544d678ceab6c5fa269f64e9e16299`.

### H-I. Finite boundary and classification

The 11 rows only replay one periodic set; the all-density conclusion is the
analytic coefficient identity. The theorem does not identify the actual signed
Guinand--Weil form with a Fourier projection. Classification: `partial_theorem`.
RH remains `open_not_proven`.

### J-K. Minimum gap and next single lemma

The missing step is a proved lower domination of a positive-density spectral
component by the actual Weil form on an admissible packet family:

```text
ActualWeilFormDominatesPositiveDensityProjectionOnDirichletPackets
```

## 2. Collatz conjecture

### A. Declared proposition: `CompleteSlopeCharacterSumDichotomyNoGo`

For prime `q>5` and `D in F_q`, define

```text
C_q(D)=sum_(h=1)^(q-1) exp(2 pi i hD/q).
```

Then

```text
C_q(D)=q-1 if D=0, and C_q(D)=-1 otherwise,
(1+C_q(D))/q = 1_(D=0).                             (CO-253)
```

For `D_q=5F_q(2)-3F_q(3)`, subtracting the origin indicator gives the
separated projective `[3:5]` detector exactly.

### B-D. Definitions, proof, and inference audit

At `D=0` every term is one. For `D!=0`, multiplication by `D` permutes
`F_q^*`; the sum of all `q` additive characters is zero, so the nonzero-index
sum is `-1`. Fermat-quotient additivity also gives

```text
D_q=0 iff 32^(q-1)=27^(q-1) mod q^2.
```

Thus this complete sum does not soften the target. A pointwise square-root
bound would already exclude all sufficiently large target primes and cannot be
obtained by invoking a generic nondegenerate complete-sum estimate: at a target
prime the phase is identically zero.

### E-G. Adversarial and reproducible computation

The canonical pairs `F_q(2),F_q(3)` were recomputed modulo `q` for 12 primes
`7<=q<=47`, using modular exponentiation modulo `q^2`. The character dichotomy,
rational-Wieferich equivalence, origin subtraction, and separated detector were
checked by exact integer arithmetic. Failures: zero. SHA-256:
`455240ed72e4017bfbc63ba310348eb9e2618370d829ee093253e1d66e6883c2`.

### H-I. No-go scope and finite boundary

Discarded: treating fixed-`q` complete orthogonality as an independently
smoothed statistic. This is an exact route no-go, not a theorem that canonical
slopes occur or are avoided as `q` varies. The 12 rows are replay only; prior
larger finite no-hit scans are not infinite evidence. Collatz remains
`open_not_proven`.

### J-K. Minimum gap and next single lemma

The arithmetic data must genuinely vary across primes before cancellation can
be informative:

```text
CrossPrimeCanonicalSlopeCharacterAverageCancellation
```

## 3. Strong Goldbach conjecture

### A. Declared proposition: `PrimeOrderingUniquePrefixRealizabilityCriterion`

Let `q>=5` be prime, let `c` be the cyclic coefficients of `(1-X)^m` modulo
`X^q-1`, and suppose the TICKET-252 zero-residue compatibility criterion holds.
Set

```text
t=1-c_0, N*=c+t, T=qt.
```

There exists `X` for which the actual prime-count vector `N_r(X)` has centered
nonzero Fourier data `q(1-zeta_q^a)^m` if and only if the residue-count vector
of the first `T` primes is exactly `N*`.

### B-D. Definitions, proof, and inference audit

TICKET-252 Fourier inversion forces `N_r(X)=c_r+t`, while `N_0(X)=1` forces
`t=1-c_0`. Summation gives `pi(X)=qt=T`. Prime counts are constant for
`p_T<=X<p_(T+1)`, so there is exactly one prefix vector to test. Conversely, if
that prefix equals `N*`, any `X` in that interval realizes the required vector
and therefore its centered Fourier data.

### E-G. Adversarial and reproducible computation

Ten compatible tails were tested:

```text
(q,m)=(5,8..12), (7,12..16).
```

The largest forced prefix has `79,240` primes. An exact Eratosthenes sieve and
integer residue counts reject every row. At `(5,8)`, the forced vector
`(1,76,76,1,126)` differs from the first-280-prime residue vector by L1 distance
`142`. Failures: zero. SHA-256:
`a14b831094b7733f9186b166b2346c3e295617c705ded50c46ef38a62994e0ff`.

### H-I. Finite boundary and classification

The iff criterion is general for each compatible `(q,m)`. Only the ten listed
tails are computationally rejected. No uniform discrepancy estimate covers all
compatible exponents. Classification: `partial_theorem`; strong Goldbach
remains `open_not_proven`.

### J-K. Minimum gap and next single lemma

```text
UniformPrimePrefixDiscrepancyExcludesEveryCompatibleCyclotomicTail
```

## 4. Twin-prime conjecture -- deep focus

### A. Declared proposition: `RightEvenContaminationReducesToEightyFourLebesgueNagellExponents`

Use the external results explicitly summarized in Katz and Pratt,
[On the Lebesgue--Nagell equation x^2-2=y^p](https://arxiv.org/abs/2507.12397v2):
nontrivial positive solutions are excluded for prime exponent `ell<=13` and
`ell>911`; Chen's cited congruence theorem leaves only
`ell=13,17,19,23 mod 24`; and every nontrivial base exceeds `10^1000`.

If odd primes `p,r`, odd `k>=3`, and `m>=1` satisfy

```text
p^k+2=r^(2m),
```

then every prime divisor `ell` of `k` lies in

```text
P={ell prime: 17<=ell<=911,
                  ell mod 24 in {13,17,19,23}},     (TP-253)
```

where `#P=84`, and `p^(k/ell)>10^1000`.

### B-D. Definitions, proof, and external-dependency audit

Put `x=r^m`. For any prime `ell|k`, put `y=p^(k/ell)>0`. The contamination
equation becomes `x^2-2=y^ell`, a nontrivial Lebesgue--Nagell solution. Applying
the cited exponent restrictions and lower bound yields (TP-253). Since `ell`
was arbitrary, every prime factor of `k` lies in `P`.

The external source is arXiv v2 dated 25 July 2025. PrimeProject independently
checks only the factor-reduction logic and enumeration of `P`; it does not
reprove the paper's linear-forms, Thue-equation, or cited modular inputs. The
paper explicitly says the 84 prime exponents remain unresolved.

### E-G. Adversarial and reproducible computation

Trial-division primality and residue filtering independently enumerate all 84
members. Counts by residue `13,17,19,23 mod 24` are `20,20,23,21`. A separate
factor scan classifies all 4,999 odd exponents `3<=k<=9999`: 331 are supported
only on `P`, while 4,668 are rejected by the factor condition. This finite scan
is illustration, not the all-`k` proof. Failures: zero. SHA-256:
`b98e7851ac77f39a65148a17da8a40600d25774928d13483a1fcef4d4b7b8bb6`.

### H-I. Finite and logical boundary

The new theorem rigorously narrows the contamination frontier but does not
exclude any of the 84 remaining prime-exponent equations. It depends on a
checked primary preprint and is classified `partial_theorem`, not an independent
solution of the Lebesgue--Nagell equation. The Type-II twin-prime lower bound is
also untouched. Twin Prime remains `open_not_proven`.

### J-K. Minimum gap and next single lemma

Attack the smallest remaining prime exponent rather than all exponents at once:

```text
LebesgueNagellExponent17HasNoPositiveSolution
```

## Final classification

Newly established: three partial theorems and one exact no-go. All four proof
DAGs are acyclic and have one open frontier each. Candidate resolutions: zero.
Resolved parent conjectures: zero.
