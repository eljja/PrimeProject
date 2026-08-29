# TICKET-252: sparse spectral escape, marginal joint no-go, zero-residue compatibility, and finite congruence solubility

- parent: TICKET-251
- `iteration_complete`: true
- `program_complete`: false
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- classifications: three `exact_no_go`, one `partial_theorem`
- deep focus: strong Goldbach conjecture
- all four parent problems: `open_not_proven`

TICKET-252 proves four project-local auxiliary results. It does **not** prove
or disprove the Riemann hypothesis, Collatz conjecture, strong Goldbach
conjecture, or twin-prime conjecture. Completion means that this iteration's
declared propositions, computations, proof DAGs, and public artifacts pass
their stated verification contract.

## Reproduction contract

```powershell
python scripts/ticket252_sparse_marginal_zeroresidue_local.py
python -m unittest tests.test_ticket252_sparse_marginal_zeroresidue_local -v
python scripts/verify_ticket252_structure.py
python scripts/verify_ticket251_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket252-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

All replay arithmetic is integer or rational. There is no random seed.
Floating displays in rational records are nonproof conveniences; every test
uses the exact numerator and denominator.

| Problem | Exact proposition decided in TICKET-252 | Classification | Parent status |
|---|---|---|---|
| Riemann | every infinite symmetric zero-density Fourier projection admits normalized interior concentration escape despite being positive, noncompact, and nonlocal | `exact_no_go` | `open_not_proven` |
| Collatz | exact uniformity of both one-coordinate marginals does not control mass on the joint projective slope `[3:5]` | `exact_no_go` | `open_not_proven` |
| Strong Goldbach | the prime zero-residue constraint is compatible with the cyclotomic family iff `c_0-min c<=1`; it excludes every `1<=m<q` but not every tail exponent | `partial_theorem` | `open_not_proven` |
| Twin Prime | prime-residue candidates solve `p^k+2=r^(2m) mod M` for every fixed `M`; fixed finite congruence obstructions cannot close the all-X equation | `exact_no_go` | `open_not_proven` |

## 1. Riemann hypothesis

### A. Declared proposition: `SparseFourierProjectionInteriorConcentrationNoGo`

Let

```text
H=L2_even([-1,1]),
Q0(f)=sum_(k>=0)|integral_[-1,1] x^(2k) f(x) dx|^2.
```

Let `S` be an infinite symmetric subset of the nonzero integers satisfying

```text
#(S intersect [-N,N])=o(N).
```

Let `P_S` be the orthogonal projection onto the normalized Fourier modes
`2^(-1/2) exp(pi i n x)`, `n in S`. Then `P_S` is bounded, positive,
self-adjoint, noncompact, preserves the even subspace, and is not a
multiplication operator, but

```text
inf_(||f||_2=1) (Q0(f)+<P_S f,f>)=0.                 (RH-252)
```

### B-D. Definitions, proof, and inference audit

For `0<delta<1`, put

```text
g_delta=(2delta)^(-1/2) 1_[-delta,delta].
```

It is even and normalized. Its normalized Fourier coefficient satisfies

```text
|<g_delta,e_n>|^2=delta sinc(pi n delta)^2.
```

Split `S` at `A/delta`. The low-frequency contribution is
`delta o(1/delta)=o(1)`. The tail is bounded by the tail over every integer:

```text
(1/(pi^2 delta)) sum_(|n|>A/delta) 1/n^2 = O(1/A).
```

First let `delta->0`, then `A->infinity`; hence
`<P_S g_delta,g_delta>->0`. Also

```text
Q0(g_delta)<=2delta/(1-delta^4)->0.
```

The projection has infinite rank and is therefore noncompact. Orthogonal
projection gives positivity and self-adjointness. Since `0` is not in `S`,
`P_S(1)=0`; a multiplication operator with this property is zero, whereas
`P_S` is nonzero. Thus it is genuinely nonmultiplicative in the precise
operator sense used here.

### E-G. Adversarial and reproducible computation

Take `S={plus or minus 2^j:j>=0}` and `delta=2^(-s)`, `s=3,...,14`.
The exact proof bounds are

```text
low frequency <= 2delta(s+1),
tail <= 2delta/(3pi^2) < 2delta/27,
Q0 <= 2delta/(1-delta^4).
```

All 12 combined rational bounds decrease. Failures: 0.

- transcript SHA-256:
  `3e7c26600452d330e977e7880ca71b028709cad8966df6c63c41be6a1e910294`.

### H-I. No-go scope and finite limit

Discarded: noncompactness and nonlocality alone, or an infinite sparse
spectral support, as a certificate that an operator blocks interior
concentration. The theorem is about an abstract periodic Fourier projection;
it does not identify `P_S` with the Weil form or its admissible closure. RH
remains `open_not_proven`.

### J-K. Remaining minimum gap and next single lemma

```text
ActualWeilKernelHasPositiveDensityAgainstEveryInteriorWavePacket
```

## 2. Collatz conjecture

### A. Declared proposition: `UniformMarginalsCannotDetectProjectiveFermatSlopeNoGo`

For every prime `q>5`, there are two probability measures on `F_q^2` with
the same exactly uniform `U` and `V` marginals but different separated mass
on `[3:5]`:

```text
mu_hit:  (U,V)=(3t,5t), t uniform in F_q,  mass=(q-1)/q;
mu_miss: (U,V)=(t,t),   t uniform in F_q,  mass=0.   (CO-252)
```

Therefore even exact marginal equidistribution of `F_q(2)` and `F_q(3)`
cannot alone prove occurrence, avoidance, or density of their canonical
joint projective slope.

### B-D. Definitions, proof, and inference audit

Multiplication by 3 and 5 permutes `F_q`, so both hit-graph marginals are
uniform; the diagonal graph also has uniform marginals. Every nonzero point
of the first graph is `t(3,5)`. On the diagonal, the target equation becomes

```text
5t-3t=2t=0 mod q,
```

so only the excluded origin occurs. For the actual canonical point
`U_q=F_q(2)`, `V_q=F_q(3)`, the exact separated detector is

```text
I_q=1_(5U_q-3V_q=0)-1_(U_q=0 and V_q=0).
```

Additive-character orthogonality rewrites each delta exactly. Thus a joint
character estimate is required; one-coordinate information is logically
insufficient.

### E-G. Adversarial and reproducible computation

Eleven primes `q=7,...,43` replay both graphs by exact enumeration. Every one
of the four marginal count vectors is the all-one vector; target counts are
exactly `q-1` and zero. Failures: 0.

- transcript SHA-256:
  `d134c93741ae3151e80bc4443e7abbbbab5ba578292ade37cef147e17cfb324c`.

### H-I. No-go scope and finite limit

Discarded: any proof that uses only separate marginal distribution theorems
for the two Fermat quotients. The graph measures are not asserted to be the
actual cross-prime distribution of `(F_q(2),F_q(3))`. Nothing here proves a
cycle, divergence, or canonical slope occurrence. Collatz remains
`open_not_proven`.

### J-K. Remaining minimum gap and next single lemma

```text
JointFermatQuotientCharacterCancellationAtSlopeThreeFifths
```

## 3. Strong Goldbach conjecture — deep focus

### A. Declared proposition: `PrimeCountZeroResidueCyclotomicCompatibilityCriterion`

Fix prime `q>=5`, `m>=1`, and let `c_r` be the cyclic coefficients of
`(1-X)^m mod (X^q-1)`. Let

```text
N_r(X)=#{p<=X:p prime and p=r mod q},
N=sum_r N_r.
```

Suppose the centered nonzero Fourier data of `N_r` equal the TICKET-251
cyclotomic data `q(1-zeta_q^a)^m`. Then a nonnegative integer vector satisfying
the necessary prime zero-residue condition `N_0 in {0,1}` is possible if and
only if

```text
c_0-min_r c_r <= 1.                                  (GB-252a)
```

Every `1<=m<q` violates (GB-252a) and is excluded. The constraint is not a
global tail exclusion: for `(q,m)=(5,8)`,

```text
c=(-55,20,20,-55,70),
c+56=(1,76,76,1,126).                                (GB-252b)
```

The second vector passes the zero-residue constraint but is not claimed to
be an actual prime-count vector.

### B-D. Definitions, proof, and inference audit

The actual centered vector is `Delta_r=qN_r-N`. Equality of all nonzero
Fourier coefficients, together with zero sums, implies by Fourier inversion

```text
qN_r-N=q c_r for every r.
```

Consequently `N_r=c_r+t`, with integer `t=N/q`. Put
`epsilon=N_0 in {0,1}`. Then `t=epsilon-c_0`. Nonnegativity is possible iff

```text
epsilon-c_0+min c >=0
```

for an `epsilon` in `{0,1}`, which is exactly (GB-252a). If `m<q`, no cyclic
wrap occurs at indices zero and one, so `c_0=1`, `c_1=-m`; hence
`c_0-min c>=m+1>=2`.

### E-G. Adversarial and reproducible computation

For `q=5,7,11,13` and `m=1,...,17`, 68 exact integer rows recompute the cyclic
coefficients and the iff criterion. Every tested `m<q` is excluded. Compatible
tail rows begin with `(5,8)` and independently reproduce (GB-252b).
Failures: 0.

- transcript SHA-256:
  `5c95a4a8bf5019dc499a4fc45abcd82b1c10ede06659f59d0d28ee036eb06717`.

### H-I. Partial-theorem scope and finite limit

Newly excluded: the complete infinite parameter regime `1<=m<q` for every
prime `q>=5`. Discarded: claiming the zero residue alone excludes every
cyclotomic exponent. Compatible vectors need not be realizable by primes;
prime ordering, monotonicity in `X`, and quantitative residue discrepancy are
not controlled. Strong Goldbach remains `open_not_proven`.

### J-K. Remaining minimum gap and next single lemma

```text
ActualPrimeOrderingExcludesZeroResidueCompatibleCyclotomicTail
```

## 4. Twin-prime conjecture

### A. Declared proposition: `FiniteCongruenceLocalSolubilityNoGoForRightEvenPrimePowers`

For every integer `M>=1`, odd `k>=3`, and `m>=1`, there are infinitely many
pairs of distinct odd primes `p,r` such that

```text
p=7 mod 8,
p^k+2=r^(2m) mod M.                                  (TP-252)
```

Thus no fixed finite collection of congruence moduli can prove local
insolubility of the remaining right-even prime-power equation.

### B-D. Proof and external dependency audit

Set `L=8M`. The classes `-1` and `1 mod L` are reduced. By Dirichlet's theorem
on primes in reduced arithmetic progressions, choose distinct primes

```text
p=-1 mod L,  r=1 mod L.
```

For odd `k`, `p^k+2=-1+2=1 mod M`, while `r^(2m)=1 mod M`; also
`p=7 mod 8`. A finite list of moduli is absorbed into its least common
multiple. The exact external node is only Dirichlet's theorem; its required
coprimality holds for `plus or minus 1`. The referenced statement is recorded
by the [Encyclopedia of Mathematics](https://encyclopediaofmath.org/wiki/Dirichlet_theorem).

### E-G. Adversarial and reproducible computation

Eight moduli from `1` through `2310` use deterministic trial-division
primality and the first primes in the `plus or minus 1 mod 8M` classes.
Every modular residual is exactly zero. Failures: 0.

- transcript SHA-256:
  `079a60fde7d3f69814681f455edadebbe8b8d0aaf199e7821a0dad94d3ee02b4`.

### H-I. No-go scope and finite limit

Discarded: a fixed-modulus local-insolubility proof for the all-X equation.
Local solubility is not integer equality; the theorem gives no solution to
`x^2-2=p^k`, no Type-II lower bound, and no twin-prime infinitude. The
twin-prime conjecture remains `open_not_proven`.

### J-K. Remaining minimum gap and next single lemma

```text
QuadraticUnitCoefficientOneExcludesOddPrimeExponents
```

## Final classification

Newly established: three exact route no-go theorems and one partial theorem.
Every proof DAG is acyclic and has one open frontier. Candidate parent-problem
resolutions: zero. Conjecture resolutions: zero.
