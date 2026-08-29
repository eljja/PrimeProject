# TICKET-254: positive-diagonal no-go, weighted complete-detector no-go, cyclotomic reflection, and exponent-17 Thue reduction

- parent: TICKET-253
- generated: 2026-08-29 14:19:28 +09:00
- deep focus: Strong Goldbach
- resolution count: 0
- candidate resolution count: 0
- classification count: two `exact_no_go`, two `partial_theorem`

## Claim boundary

TICKET-254 proves four project-local auxiliary results. It does **not** prove or
disprove the Riemann Hypothesis, Collatz conjecture, Strong Goldbach
conjecture, or Twin Prime conjecture. The RH construction is an abstract
positive operator, the Collatz theorem diagnoses a complete-detector
representation rather than canonical prime behavior, the Goldbach result
covers only a reflection/threshold subclass, and the Twin result reduces but
does not solve seventeen Thue equations.

## Reproduction

```powershell
python scripts/ticket254_diagonal_weighted_reflection_thue.py
python -m unittest tests.test_ticket254_diagonal_weighted_reflection_thue -v
python scripts/verify_ticket254_structure.py
python scripts/verify_open_problem_structure.py
python scripts/verify_open_problem_workbench.py
python scripts/reproduce_publication.py
node --check assets/ticket254-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
python -m unittest discover -s tests -p "test_*.py"
```

All arithmetic in the TICKET-254 generator is integer or `Fraction`
arithmetic. There is no random seed and no floating-point inference.

## Machine summary

| Problem | Exact proposition decided | Classification | Parent status |
|---|---|---|---|
| RH | `PositiveDiagonalDirichletPacketDominationNoGo` | `exact_no_go` | `open_not_proven` |
| Collatz | `NonnegativeCrossPrimeCompleteDetectorAverageNoGo` | `exact_no_go` | `open_not_proven` |
| Goldbach | `EvenCyclotomicReflectionPrimePrefixExclusion` | `partial_theorem` | `open_not_proven` |
| Twin Prime | `ExponentSeventeenUnitTwistedThueReduction` | `partial_theorem` | `open_not_proven` |

## 1. Riemann Hypothesis

### A. Exact proposition

For every integer `N>=1`, put `L=2N+1` and let

```text
d_N=L^(-1/2) sum_(|n|<=N) e_n in l2(Z).
```

There is a bounded positive self-adjoint operator `A_N` such that

```text
<A_N e_n,e_n>=1 for every n, but <A_N d_N,d_N>=0.       (RH-254)
```

On the packet block use

```text
A_N = L/(L-1) I - 1/(L-1) J,
```

and use the identity on the orthogonal exterior.

### B-D. Definitions and proof

The diagonal of the displayed block is exactly one. The all-ones vector is an
eigenvector of `J` with eigenvalue `L`, so its `A_N` eigenvalue is zero. On the
orthogonal complement, `J=0` and the eigenvalue is `L/(L-1)>0`. Therefore the
block is positive semidefinite and its direct sum with the identity is bounded,
positive, and self-adjoint. Its norm is at most `3/2`, uniformly in `N`.

This disproves the proposed implication

```text
uniform positive Fourier diagonal => positive Dirichlet-packet domination.
```

The counterexample does not assert anything negative about the actual
Guinand-Weil quadratic form. It proves that diagonal information alone cannot
establish the TICKET-253 target.

### E-G. Adversarial computation

Eight exact blocks with `N=1,2,3,4,7,15,31,63` recompute the diagonal,
off-diagonal, packet energy, and two eigenvalues using rational arithmetic.
Every packet energy is exactly zero; failures: zero.

- algorithm: exact evaluation of an equicorrelated block's two eigenspaces;
- complexity: `O(1)` per replay row; the all-`N` proof is algebraic;
- transcript SHA-256:
  `0be64af7360d626405108d0fee5944f6132fdb6065fd57690c657f3e160df05c`.

### H-I. Limit and classification

The finite rows only replay the formula. More importantly, the formula ranges
over abstract operators chosen with `N`; the actual Weil form is one fixed
arithmetic form. Classification: `exact_no_go` for the diagonal-only route,
not RH.

### J-K. Remaining gap and next lemma

The actual finite Weil blocks require quantitative off-diagonal control:

```text
ActualWeilDirichletBlocksHaveUniformStrictDiagonalDominance
```

## 2. Collatz conjecture

### A. Exact proposition

For a finite set `Q` of primes `q>5`, arbitrary `(U_q,V_q)` in `F_q^2`, and
nonnegative rational weights `w_q`, put

```text
D_q=5U_q-3V_q,
C_q(D)=sum_(h=1)^(q-1) exp(2 pi i hD/q).
```

Then

```text
sum_q w_q [(1+C_q(D_q))/q - 1_(U_q=V_q=0)]
= sum_q w_q 1_(D_q=0 and (U_q,V_q)!=(0,0)).          (CO-254)
```

Every summand is nonnegative.

### B-D. Proof and inference audit

Complete additive-character orthogonality gives

```text
(1+C_q(D))/q = 1_(D=0)
```

pointwise. Subtracting the origin, multiplying by `w_q>=0`, and summing proves
(CO-254). Thus the proposed nonnegative cross-prime complete average contains
no cancellation: estimating it is exactly the original weighted incidence
problem.

This extends the TICKET-253 pointwise diagnosis to every finite nonnegative
weighting. It does not block signed incomplete character kernels, because
those terms need not be incidence indicators.

### E-G. Adversarial computation

For 12 primes `7<=q<=47`, four cases were checked: the canonical Fermat-
quotient pair, a synthetic `[3:5]` hit, a miss, and the origin. Three exact
weight families—`1`, `q`, and `1/q`—were then applied to every scenario.

- detector rows: 48;
- weighted rows: 12;
- arithmetic: modular exponentiation modulo `q^2`, integers, and `Fraction`;
- failures: zero;
- transcript SHA-256:
  `6ce9f4399b2372016d2c0bb7d9aa02e8bc14b7b5ee124687ba55c6f76638be46`.

### H-I. Limit and classification

The computation is replay only; the theorem is algebraic. Neither one proves
canonical occurrence or avoidance as `q` varies. Classification:
`exact_no_go` for nonnegative averages of the normalized complete detector.

### J-K. Remaining gap and next lemma

Any useful transform must be genuinely signed and still recover incidence:

```text
IncompleteSlopeCharacterKernelHasSignedRecoveryAndCrossPrimeCancellation
```

## 3. Strong Goldbach conjecture -- deep focus

### A. Exact proposition

Let `q>=5` be prime, let `m` be even with `q` not dividing `m`, and let `c_r`
be the cyclic coefficients of `(1-X)^m mod (X^q-1)`. Assume TICKET-252
zero-residue compatibility, and set

```text
t=1-c_0, T=qt, r=m mod q.
```

Let `kappa_q(r)` be the global prime index of the second prime congruent to
`r mod q`. If

```text
T >= kappa_q(r),                                      (GB-254a)
```

then the compatible tail is not an actual prime-prefix vector.

### B-D. Reflection proof and transfer

Write `a_j=(-1)^j binom(m,j)`. The involution `j -> m-j` gives

```text
a_(m-j)=(-1)^m a_j.
```

After folding modulo `q`,

```text
c_(m-r)=(-1)^m c_r.                                  (GB-254b)
```

Taking `r=0` and even `m` yields

```text
c_(m mod q)=c_0.
```

Because `q` does not divide `m`, this is a nonzero residue. Its forced count
in the TICKET-253 vector is

```text
N*_(m mod q)=c_0+(1-c_0)=1.                          (GB-254c)
```

If (GB-254a) holds, the first `T` primes already contain two primes in that
residue, so their actual count is at least two. This contradicts (GB-254c)
and the unique-prefix realizability criterion.

The mapped objects and preserved property are exact: cyclic binomial
coefficients map under reflection, equality with `c_0` is preserved by the
uniform shift, and the result transfers to the actual prime-prefix count via
the TICKET-253 iff theorem.

### E-G. Exact certificates

The replay scans the even pairs

```text
q in {5,7,11,13,17,19}, 2<=m<=160.
```

Among 480 pairs, 50 are compatible with `q` not dividing `m`. For every one,
the exact reflection identity holds, the forced reflected count is one, and
the explicit second residue prime occurs before the forced prefix ends.

The first certificate is `(q,m)=(5,8)`: `r=3`, `T=280`, while the first two
primes `3 mod 5` are `3` and `13`, with the second at global prime index 6.
The largest displayed `T` is
`35532145864654126766913393422907521619163005115`; it is never enumerated.
Only the two small residue-prime witnesses are needed.

- algorithm: exact cyclic binomial folding and deterministic primality checks;
- complexity: linear in the folded coefficient count plus the short search for
  two residue primes;
- failures: zero;
- transcript SHA-256:
  `253518284e5b939aa42449fd309978e3fe0c7bda7d83944ee96217eed38394f6`.

### H-I. Boundary and classification

The finite scan demonstrates 50 certificates but does not create the general
theorem. The proof covers every pair satisfying its exact hypotheses. It does
not cover odd `m`, `q|m`, or a prefix below the second-prime threshold.
Classification: `partial_theorem`; Strong Goldbach remains open.

### J-K. Remaining gap and next lemma

```text
OddOrQDivisibleCompatibleTailPrimePrefixExclusion
```

## 4. Twin Prime conjecture

### A. Exact proposition

For `0<=j<17`, write

```text
(1+sqrt(2))^j=a_j+b_j sqrt(2)
```

and define homogeneous integer polynomials `A_j,B_j` by

```text
A_j(u,v)+B_j(u,v)sqrt(2)
=(a_j+b_j sqrt(2))(u+v sqrt(2))^17.                  (TP-254a)
```

Positive integer solutions of

```text
x^2-2=y^17                                          (TP-254b)
```

exist if and only if some integers `j,u,v` satisfy

```text
B_j(u,v)=1,
A_j(u,v)>0,
y=(-1)^j(u^2-2v^2)>0.                               (TP-254c)
```

Then `x=A_j(u,v)`.

### B-D. Quadratic-ring proof

If `y` were even, then `x` would be even and `v_2(x^2-2)=1`, contradicting the
17th power. Thus `x,y` are odd. In `Z[sqrt(2)]`, the two conjugate factors
`x+sqrt(2)` and `x-sqrt(2)` are coprime: a common divisor divides `2sqrt(2)`,
but its norm must divide the odd number `y^17`, hence it is a unit.

The ring is norm-Euclidean. For a quotient `r+s sqrt(2)`, choose nearest
integers to `r,s`; the remainder has
`|r^2-2s^2|<=1/2<1`. Hence it is a UFD. Coprimality and (TP-254b) imply

```text
x+sqrt(2)=epsilon (u+v sqrt(2))^17.
```

The standard Pell-unit descent gives all units as
`+/- (1+sqrt(2))^n`. Absorb a 17th unit power and the sign into `(u,v)`,
leaving one residue `j mod 17`. Comparing the `sqrt(2)` coefficient and taking
norms gives (TP-254c). Multiplying out proves the converse.

### E-G. Adversarial exact computation

All 17 pairs of degree-17 coefficient arrays are emitted explicitly. The box
`|u|,|v|<=12`, excluding `(0,0)`, gives 10,608 exact twist-points. For each,
binary quadratic-ring exponentiation, direct polynomial evaluation, and

```text
A_j(u,v)^2-2B_j(u,v)^2
= [(-1)^j(u^2-2v^2)]^17
```

agree exactly. Two points have `B_j=1`, but both have negative reduced `y`;
there are zero admissible positive points in the box.

- failures: zero;
- random seed: none;
- transcript SHA-256:
  `1cc60a2de6cbf63644bb1751a558602cdf696651b181a1a14606b62ec457fcf3`.

### H-I. Boundary and classification

The finite box is not evidence against solutions beyond the box—TICKET-253's
external lower bound in fact places any nontrivial base far beyond it. The new
result is the exact finite family of equations, not the empty finite search.
Classification: `partial_theorem`; exponent 17 and Twin Prime remain open.

### J-K. Remaining gap and next lemma

```text
AllSeventeenUnitTwistedCoefficientOneThueEquationsHaveNoAdmissibleIntegralPoint
```

## Proof-DAG and completion audit

Each problem has an acyclic four-node DAG: the TICKET-253 predecessor, the new
proved theorem, a disproved route, and exactly one open next lemma. No
assumption or heuristic node is placed on a completed path. Machine failures,
candidate resolutions, and conjecture resolutions are all zero.

Iteration completion means that the code, exact outputs, reports, DAGs, Pages,
and tests reproduce. It does not mean that a parent conjecture is resolved.
