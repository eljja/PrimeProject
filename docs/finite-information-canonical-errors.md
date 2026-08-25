# TICKET-241: Finite Information, Canonical Errors, and Fixed-Base Search

## Claim boundary

TICKET-241 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, the strong Goldbach conjecture, or the twin-prime conjecture. It
proves four exact information-boundary theorems and reports finite computations
only on their stated domains. The parent-conjecture resolution count is zero.

Machine-readable audit:
`data/open-problem/ticket241-finite-information-canonical-errors.json`.

Reproduce and verify with:

```powershell
python scripts/ticket241_finite_information_canonical_errors.py
python -m unittest tests.test_ticket241_finite_information_canonical_errors -v
python scripts/verify_ticket241_structure.py
python scripts/verify_open_problem_structure.py
```

The generator scans every prime through `100,000,000`; the test suite reads the
committed audit and independently rechecks the smaller algebraic certificates.

## Results

| Problem | Exact TICKET-241 result | Route rejected or narrowed | Status |
|---|---|---|---|
| Riemann | A finite unsigned prime-cosine kernel has rank at most twice its prime support; diagonal positivity is artificial on its forced nullspace | Finite regularized Gram positivity as evidence for signed Weil positivity | `open_not_proven` |
| Collatz | Principal-unit algebra permits the bad depth pattern; the actual fixed bases have no candidate through `10^8` | LTE or local linear algebra alone proves all-prime depth domination | `open_not_proven` |
| Goldbach | Signed errors are tautological, while absolute-error certificates depend on a fixed decomposition and norm | An unspecified list of “all explicit errors” as a stable milestone | `open_not_proven` |
| Twin prime | Every finite periodic fingerprint has infinitely many prime/composite-successor mimics | Finite periodic feature enrichment eventually certifies twins | `open_not_proven` |

## 1. Riemann Hypothesis

### Declared proposition

Let `P` be finite, let `a_p>=0`, and let `t_1,...,t_J` be real. Define

```text
K_jk = sum_(p in P) a_p cos((t_j-t_k) log p).
```

Then `K` is positive semidefinite and `rank(K)<=2|P|`. Compression to the
orthogonal complement of the common vector does not increase rank. Therefore,
if `J-1>2|P|`, the compressed kernel is singular. For every `epsilon>0`, adding
`epsilon I` makes the eigenvalue on that forced kernel exactly `epsilon`.

### Proof

The identity

```text
cos(x-y)=cos(x)cos(y)+sin(x)sin(y)
```

realizes `K` as the Gram matrix of vectors with the `2|P|` coordinates

```text
sqrt(a_p) cos(t_j log p),  sqrt(a_p) sin(t_j log p).
```

Positive semidefiniteness and the rank bound follow immediately. Rank-nullity
gives at least `J-1-2|P|` null directions after common-mode removal. The
regularizer acts as `epsilon I` on those directions, so that lower bound was
inserted rather than derived from zeta arithmetic.

The four numerical rows use `|P|=3,5,8,12` and `J=2|P|+4`. Every row has at
least three forced null directions; adding `epsilon=2^-10` moves the smallest
compressed eigenvalue to `epsilon` within the stated floating-point tolerance.
The theorem itself is exact and does not depend on that numerical tolerance.

### Limit and next lemma

Unsigned prime-cosine PSD is not the Guinand-Weil quadratic form. It omits the
archimedean term, trivial zeros, signed prime-power contribution, admissibility
conditions, and the all-test-function quantifier. Connes and Consani discuss
the operator-theoretic Weil-positivity boundary and the limitations of an
operator construction; TICKET-241 does not claim their conjectural framework.

Next:
`SignedGuinandWeilFiniteSectionsConvergeWithoutArtificialDiagonalForEveryAdmissibleTestFamily`.

## 2. Collatz conjecture

### Declared proposition

TICKET-240 reduced the run-block lifting defect to the Fermat-quotient pair
`u=F_q(2)`, `v=F_q(3)`:

```text
x-depth >= 2  iff  5u-3v = 0 mod q,
y-depth >= 2  iff   u-v  = 0 mod q.
```

For every odd prime `q>5`, however, the principal units

```text
A=1+3q,  B=1+5q
```

satisfy `A^5=B^3 mod q^2` while `A!=B mod q^2`. More precisely,
`v_q(A^5-B^3)>=2` and `v_q(A-B)=1`.

### Proof and computation

The binomial theorem gives

```text
(1+3q)^5 = 1+15q mod q^2,
(1+5q)^3 = 1+15q mod q^2,
A-B      = -2q.
```

Thus principal-unit algebra realizes exactly the positive-defect pattern. The
fixed-base point `(F_q(2),F_q(3))` may still avoid it, but that would require
special arithmetic information not supplied by LTE or local group structure.

The actual congruence

```text
32^(q-1) = 27^(q-1) mod q^2
```

was tested for all `5,761,453` primes `5<=q<=100,000,000`. No solution and no
positive-defect candidate occurred. This extends the TICKET-240 bound by a
factor of five. It is a finite certificate, not an all-prime theorem.

### Limit and next lemma

The local countermodel is not an actual exceptional prime, Collatz orbit, or
cycle. Conversely, the bounded absence of a fixed-base exception does not
exclude one above `10^8`. Even all-prime run-block depth domination would not
settle general necklaces or aperiodic descent.

Next:
`FixedBaseFermatQuotientLineAvoidanceFor5Fq2Equals3Fq3UnlessFq2EqualsFq3`.

## 3. Strong Goldbach conjecture

### Declared proposition

For any exact decomposition

```text
R(N)=M(N)+sum_i E_i(N),  M(N)>0,
```

where `R(N)` is an integer representation count:

1. `M+sum E_i>=1` is exactly `R>=1` and is not an intermediate theorem.
2. `M-sum |E_i|>=1` is sufficient but not necessary.
3. The absolute certificate is not invariant under refinement, since
   `E=(E+L)+(-L)` preserves `R` but makes the absolute budget arbitrarily
   large as `|L|` grows.

### Proof and computation

The first statement is substitution. The second follows from the triangle
inequality. The canceling split proves the third statement. Consequently the
words “all explicit errors” do not define a mathematical target until the arc
decomposition, smoothing, error grouping, and norm have been fixed independently
of the observed target.

Fifteen exact restricted prime-window DFT rows from `X=10^3` through `10^7`
were audited. Fourteen represented rows fail the DC absolute certificate even
though the signed identity correctly reports representation. This finite model
does not refute a classical major/minor-arc proof; it proves that the certificate
is sufficient rather than necessary and that arbitrary error refinement is
invalid.

### Limit and next lemma

No pointwise lower bound is proved for the actual binary-prime major and minor
arcs. Helfgott's major- and minor-arc estimates provide a rigorous architecture
for ternary Goldbach, not the missing binary all-even estimate.

Next:
`FixedBinaryPrimeArcDecompositionHasUniformTargetwisePositiveLowerCertificate`.

## 4. Twin-prime conjecture

### Declared proposition

Let `F` be any finite collection of features of `(n,n+2)`, each periodic with
a fixed modulus. Let `M` be a common period and choose `a mod M` with

```text
gcd(a,M)=gcd(a+2,M)=1.
```

There are infinitely many primes `p` satisfying

```text
F(p,p+2)=F(a,a+2)
```

while `p+2` is composite.

### Proof and computation

Choose a prime `ell` not dividing `2M` and impose

```text
p=a mod M,  p=-2 mod ell.
```

CRT gives a reduced residue class modulo `M ell`. Dirichlet's theorem gives
infinitely many primes in the class. Periodicity preserves every feature, while
`ell | p+2`; all sufficiently large successors are proper composite multiples
of `ell`.

Five exact witnesses are recorded for periods from `30` through `510,510`.
The largest witness is `p=25,525,529`, with `p+2=19*1,343,449`. The theorem is
infinite; the rows only verify the implementation.

### Limit and next lemma

The theorem does not disprove twin primes. It excludes fixed finite periodic
classifiers, including arbitrary deterministic post-processing of their feature
vectors, as sufficient certificates. Growing moduli, switching weights, and
signed Type II information are not periodic with one fixed modulus and remain
outside the no-go. This is consistent with the parity limitation discussed in
the Polymath bounded-gap work.

Next:
`GrowingModulusParitySensitiveTypeIIBoundForShiftTwoLambdaOnInfinitelyManyDyadicBlocks`.

## Proof DAG summary

```text
TICKET-240 input
  -> TICKET-241 rejected inference
  -> TICKET-241 exact theorem
  -> one highest-risk open lemma
```

Every track JSON contains the expanded four-node DAG. All four final nodes are
`highest_risk_open`; no node records a parent-conjecture proof.

## Primary research baselines

- Connes and Consani, [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368).
- Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562), revised 2026.
- Sondow, [Lerch Quotients, Lerch Primes, Fermat-Wilson Quotients, and the Wieferich-non-Wilson Primes](https://arxiv.org/abs/1110.3113).
- Helfgott, [Minor arcs for Goldbach's problem](https://arxiv.org/abs/1205.5252) and [Major arcs for Goldbach's problem](https://arxiv.org/abs/1305.2897).
- D. H. J. Polymath, [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897).

These sources define the accepted frontier. The four theorem names above are
PrimeProject route-audit results and are not attributed to those papers.
