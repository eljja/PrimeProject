# TICKET-251: interior concentration, finite-prime CRT, cyclotomic concentration, and a right-even modulo-eight constraint

- parent: TICKET-250
- `iteration_complete`: true
- `program_complete`: false
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- classifications: three `exact_no_go`, one `partial_theorem`
- deep focus: strong Goldbach conjecture
- all four parent problems: `open_not_proven`

TICKET-251 proves four project-local auxiliary results. It does **not** prove
or disprove the Riemann hypothesis, Collatz conjecture, strong Goldbach
conjecture, or twin-prime conjecture. Completion means only that this
iteration's declared propositions and artifacts have passed their audit.

## Reproduction contract

```powershell
python scripts/ticket251_interior_crt_cyclotomic_righteven.py
python -m unittest tests.test_ticket251_interior_crt_cyclotomic_righteven -v
python scripts/verify_ticket251_structure.py
python scripts/verify_ticket250_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket251-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

The generator is deterministic. Integer and `Fraction` fields are proof
certificates. The trigonometric decimal in the Goldbach rows is explicitly
`display_only_nonproof`; the strict ratio and its limit are proved
analytically.

| Problem | Exact proposition decided in TICKET-251 | Classification | Parent status |
|---|---|---|---|
| Riemann | every continuous even nonnegative local multiplier with an interior zero fails full-sphere coercivity for the raw moment form | `exact_no_go` | `open_not_proven` |
| Collatz | arbitrary Fermat-quotient targets at any finite prime set can be realized simultaneously by CRT lifts of 2 and 3 | `exact_no_go` | `open_not_proven` |
| Strong Goldbach | nonnegative integer centered vectors can have full reduced Fourier support and nonzero norm while their energy concentrates on two conjugate frequencies | `exact_no_go` | `open_not_proven` |
| Twin Prime | `p^k+2=r^(2m)` implies `k` odd and `p=7 mod 8`; modulo eight alone cannot force `k=1` | `partial_theorem` | `open_not_proven` |

## 1. Riemann hypothesis

### A. Declared proposition: `InteriorZeroLocalMultiplierCoercivityNoGo`

Let

```text
H=L2_even([-1,1]),
Q0(f)=sum_(k>=0) |integral x^(2k)f(x)dx|^2.
```

If `w` is continuous, even, nonnegative and nonzero, and `w(x0)=0` for
some `x0 in [0,1)`, then `M_w` is bounded, self-adjoint and noncompact, but

```text
inf_(||f||=1) (Q0(f)+<M_w f,f>) = 0.                    (RH-251)
```

### B-D. Proof and inference audit

Choose `rho<1` and shrinking symmetric neighborhoods `E_delta` of
`{−x0,x0}`. With `g_delta=1_E/sqrt(|E|)`, continuity gives

```text
<M_w g_delta,g_delta> <= sup_(E_delta) w -> 0.
```

For each `k`,

```text
|integral x^(2k)g_delta|^2 <= |E_delta| rho^(4k),
Q0(g_delta) <= |E_delta|/(1-rho^4) -> 0.
```

Because nonzero continuous `w` is bounded below on a positive-measure
symmetric region, normalized indicators of countably many disjoint symmetric
subsets have mutually orthogonal images with norms bounded away from zero.
Thus `M_w` is noncompact. These arguments prove (RH-251) for the whole stated
class; the finite replay is not the basis of the theorem.

### E-G. Adversarial and reproducible computation

For `w(x)=(x^2-1/9)^2`, `x0=1/3`, and `delta=2^(-s)`, `s=3,...,13`, the
generator records the exact upper bounds

```text
<M_w g,g> <= (2 delta/3+delta^2)^2,
Q0(g) <= 4 delta/(1-(1/3+delta)^4).
```

All 11 rational certificates decrease; failures: 0.

- transcript SHA-256:
  `e79a0c6278dedf06d33bbd79125d059adf86c1f2ae1f252afbae78daf5d3ffcd`.

### H-I. No-go scope and finite limit

Discarded: every continuous nonnegative **local** multiplier having an
interior zero as a whole-unit-sphere coercivity repair. The theorem does not
cover a strictly positive multiplier (`w>=c>0` is trivially coercive), an
endpoint-only zero, a nonlocal kernel, or the actual Guinand-Weil admissible
closure. RH remains `open_not_proven`.

### J-K. Remaining gap and next single lemma

```text
NonlocalArithmeticWeilKernelExcludesInteriorConcentration
```

## 2. Collatz conjecture

### A. Declared proposition: `FinitePrimeCanonicalLiftPatternCRTInterpolationNoGo`

For a finite nonempty set `S` of primes `q>5` and arbitrary
`(u_q,v_q) in F_q^2`, there is a unique pair `(A,B)` modulo
`M=product_(q in S)q^2` satisfying

```text
A=2 mod q, B=3 mod q,
F_q(A)=u_q, F_q(B)=v_q,
F_q(x)=(x^(q-1)-1)/q mod q.                            (CO-251)
```

Hence one fixed pair of integers can interpolate every prescribed finite
hit/avoidance pattern for projective slope `[3:5]`.

### B-D. Proof and inference audit

The exact lift identity from TICKET-250 is

```text
F_q(a+kq)=F_q(a)-k/a mod q.
```

The unique lift indices are therefore

```text
k_q=2(F_q(2)-u_q),  ell_q=3(F_q(3)-v_q) mod q.
```

The congruences `A=2+k_q q` and `B=3+ell_q q mod q^2` have unique
simultaneous solutions modulo `M` by CRT. Targets on and off `[3:5]` give
arbitrary finite patterns.

### E-G. Adversarial and reproducible computation

Four exact cases use prime sets of sizes two through four and targets
`(3,5)`, `(0,0)`, `(1,0)`, and `(1,1)`. Modular exponentiation verifies
every local target after CRT. Failures: 0.

- transcript SHA-256:
  `c184a69eaebae32ffdc9e9043ca4864bf7615e5933a225721616dcda732e2fdc`.

### H-I. No-go scope and finite limit

Discarded: inferring canonical cross-prime behavior from a finite collection
of lift-compatible local conditions. The constructed `A,B` depend on `S` and
are not the canonical fixed integers `2,3`. Nothing here proves occurrence,
avoidance, or density for `(F_q(2),F_q(3))`, and nothing controls arbitrary
Collatz trajectories. Collatz remains `open_not_proven`.

### J-K. Remaining gap and next single lemma

```text
CanonicalRepresentativeFermatQuotientDistributionBeyondFiniteCRTInterpolation
```

## 3. Strong Goldbach conjecture — deep focus

### A. Declared proposition: `CyclotomicUnitFullSupportEnergyConcentrationNoGo`

Fix an odd prime `q>=5` and `m>=1`. Define

```text
c_r = sum_(0<=j<=m, j=r mod q) (-1)^j binom(m,j),
C=-min_r c_r, n_r=C+c_r, N=sum_r n_r, Delta_r=q n_r-N.
```

Then `n_r` are nonnegative integers, `sum Delta_r=0`, and for a primitive
`q`-th root `zeta_q`,

```text
F_m(a)=sum_r Delta_r zeta_q^(ar)=q(1-zeta_q^a)^m != 0,
product_(a=1)^(q-1) F_m(a)=q^(q-1+m).                 (GB-251a)
```

For the maximal conjugate pair `A*={(q-1)/2,(q+1)/2}`,

```text
E_out/E_A* <= (q-3)/2 * rho_q^m -> 0,
rho_q=cos^2(3pi/(2q))/cos^2(pi/(2q)) < 1.             (GB-251b)
```

### B-D. Proof and inference audit

Reducing `(1-X)^m` modulo `X^q-1` gives the `c_r`, and
`sum c_r=(1-1)^m=0`. Thus `N=qC` and `Delta_r=qc_r`. Evaluation at
`zeta_q^a` proves (GB-251a); the cyclotomic identity
`product_a(1-zeta_q^a)=q` proves the norm formula. Also

```text
|F_m(a)|^2=q^2(4 sin^2(pi a/q))^m.
```

The largest two values occur at `A*`; all others are at most the second
maximum with cosine `cos(3pi/(2q))`. This proves (GB-251b).

### E-G. Adversarial and reproducible computation

The generator folds binomial coefficients exactly for
`q=5,7,11,13` and `m=1,2,3,5,8,13,21,34`: 32 cases. It verifies
nonnegativity, centeredness, the exact Parseval integer
`q^3 sum_r c_r^2`, and norm `q^(q-1+m)`. Floating ratios are display-only;
the proof uses strict trigonometric ordering. Failures: 0.

- transcript SHA-256:
  `e3c9e81aab8500e964f265aa6ba8bd91105d40f67e1f5c7938f63bb88bcaa857`.

### H-I. No-go scope and finite limit

Discarded: obtaining quantitative Fourier anti-concentration solely from
centeredness, integrality, nonnegativity, full reduced support, and a nonzero
Galois norm. The vectors are structural countermodels, not proved to be
actual prime-count or logarithmically weighted residue vectors. Strong
Goldbach remains `open_not_proven`.

### J-K. Remaining gap and next single lemma

```text
ActualPrimeCountResidueVectorsExcludeCyclotomicUnitConcentration
```

## 4. Twin-prime conjecture

### A. Declared proposition: `RightEvenModuloEightConstraintAndSharpness`

For odd primes `p,r` and `k,m>=1`,

```text
p^k+2=r^(2m)  implies  k is odd and p=7 mod 8.         (TP-251a)
```

Conversely, every odd `k` and odd `p=7 mod 8` satisfies

```text
p^k+2=1 mod 8.                                        (TP-251b)
```

Thus modulo eight alone cannot force `k=1` or exclude odd composite left
powers. The converse is only congruence compatibility, not an integer
solution.

### B-D. Proof and withdrawn-source audit

Every odd square is `1 mod 8`. If `k` is even, then `p^k=1 mod 8`, so the
left side is `3 mod 8`, impossible. Hence `k` is odd. Then `p^k=p mod 8`,
so `p+2=1 mod 8` and `p=7 mod 8`. Conversely, odd `k` and `p=7 mod 8`
give `p^k+2=1 mod 8`, proving the limitation of the congruence route.

An earlier draft relied on [arXiv:2008.11515](https://arxiv.org/abs/2008.11515),
whose primary record says it was withdrawn for a major mistake. It is not a
proof dependency. The stronger all-X `k=1` classification has therefore been
removed rather than asserted.

### E-G. Adversarial and reproducible computation

Exact prime-power supports through `10,000,000` contain 124 right-even active
pairs. All happen to have left exponent one; examples include `7->9`,
`23->25`, `79->81`, and `727->729`. Every row obeys the proved modulo-eight
condition. The absence of a composite-left witness is finite evidence only.
Failures: 0.

- transcript SHA-256:
  `2881e5c20c714c52c8502ea5ec74617bed8bbc110c35069c488e960a4d711e85`.

### H-I. Partial-theorem scope and finite limit

Discarded: treating the withdrawn source as a theorem, and claiming that the
modulo-eight condition forces `k=1`. The remaining all-X equation
`x^2-2=p^k` for odd `k>=3` is not settled here. Neither the finite scan nor
the congruence theorem supplies a sieve lower bound or twin-prime infinitude.
The twin-prime conjecture remains `open_not_proven`.

### J-K. Remaining gap and next single lemma

```text
NoPositivePrimePowerSolutionsOfXSquareMinusTwoEqualsYOddPower
```

## Final classification

Newly established: three exact route no-go theorems and one elementary
partial theorem. Retired: the four routes explicitly named above.
Remaining: four proof-DAG frontiers, one per parent problem. No result is a
candidate parent-conjecture resolution, so no formal resolution audit is
triggered.
