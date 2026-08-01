# TICKET-174: tail schedules, unique Collatz zero lifts, adaptive Goldbach selection, and sharp Haar scale aggregation

## Claim boundary

TICKET-174 continues the four open nodes left by TICKET-173. It proves four
finite or abstract quantitative statements. It does **not** prove or disprove the
Riemann Hypothesis, the Collatz conjecture, strong Goldbach, or the Twin Prime
conjecture. Every conjecture remains `open_not_proven`; the machine resolution
count is zero.

The contribution is narrower and checkable: it identifies one quantifier error
that must be avoided on each route and replaces the previous broad target by one
sharper open lemma.

| Problem | Exact TICKET-174 result | Status | Rejected route | Next single lemma |
|---|---|---|---|---|
| Riemann | diagonal tail-schedule transfer theorem | `open_not_proven` | linear or critical `N log N` cutoff closes the tail | `PoleNeutralQuadraticCutoffTruncatedCoreDefectConvergesToZero` |
| Collatz | exactly one zero-lift child per cylinder | `open_not_proven` | density-one positive lifts imply an every-ray result | `NoNonDescendingRayEventuallyFollowsUniqueZeroLiftChildren` |
| Goldbach | adaptive positive-frequency certificate iff positivity | `open_not_proven` | post-hoc positive frequencies form a non-circular major set | `FixedFareyMajorArcPositiveMassDominatesComplementSignedDeficitUniformly` |
| Twin Prime | `log2 N` maximum-scale aggregation bound is sharp | `open_not_proven` | remove scale loss using only maximum pair energy | `PrimePairEveryScalePairHaarEnergyPowerSavingUniformly` |

## 1. Riemann: a valid diagonal cutoff schedule

### Declared proposition

Let `V_N` be nested finite-dimensional spaces with dense union. Suppose a
truncated Hermitian form satisfies

```text
|q(v) - q_(N,T)(v)| <= B_N(T) ||v||^2,
lambda_min(q_(N,T)) >= -delta_(N,T)
```

on `V_N`. If one diagonal schedule `T_N` has

```text
delta_(N,T_N) + B_N(T_N) -> 0,
```

then `q` is nonnegative on the closure. Use the explicit certified
archimedean upper bound

```text
U_N(T) = 2(2N+1)rho/pi^2 *
         [log(T)/(T-rho N) + log(T/(T-rho N))/(rho N)],
rho = 2 pi / log(c),  T > max(rho N,7),
```

the sufficient schedule condition is

```text
T_N / (N log T_N) -> infinity.
```

Thus `T_N=N^2` makes this certified upper bound vanish, while `T_N=C N`
and `T_N=C N log N` do not certify tail closure through this bound.

### Proof

The perturbation inequality gives

```text
q(v) >= -[delta_(N,T)+B_N(T)] ||v||^2.
```

The TICKET-173 dense-core theorem then applies along the selected diagonal.
Under the sufficient schedule condition, `T-rho N` is asymptotic to `T`.
The two terms are therefore `O(N log T/T)` and `O(N/T)`. Both vanish for
`T=N^2`. The first grows logarithmically for `T=C N` and approaches a
positive constant for `T=C N log N`.

### Reproducible calculation

At `c=100`, the checked ladder `N=16,...,4096` gives:

| schedule | first budget | final budget | asymptotic verdict |
|---|---:|---:|---|
| `8N` | 0.495118 | 0.942321 | bound does not vanish |
| `8N log N` | 0.187333 | 0.114591 | positive-limit bound |
| `N^2` | 0.253306 | 0.002382 | bound vanishes |
| `N^3` | 0.020861 | 0.000000856 | bound vanishes |

These values evaluate Corollary 3.3's explicit upper bound, not only its
fixed-`N` leading asymptotic. A nonvanishing upper bound is inconclusive about
the exact tail; the values also do not estimate the missing arithmetic defect
`delta_(N,T)`.

### Remaining gap

The open statement is a certified lower-defect estimate for the actual
pole-neutral truncated Weil core at the quadratic cutoff. This is precisely the
sign information that the schedule theorem does not supply.

## 2. Collatz: the exceptional branch has density zero but cannot be ignored

### Declared proposition

For a finite accelerated-odd valuation word `w`, let `r_w` be its least
positive cylinder representative, `M_w` its modulus, and `y=T^H(r_w)`. Among
all children `wa`, exactly one has zero lift:

```text
a* = v_2(3y+1),
r_(wa*) = r_w.
```

Every other child has

```text
r_(wa) = r_w + k_a M_w,  k_a > 0.
```

Among `a<=A`, at most `1/A` of the children are zero-lift. Nevertheless, an
eventually stabilized natural ray follows the unique zero-lift child forever.

### Proof

Every child cylinder refines its parent, hence its representative differs by a
nonnegative multiple of `M_w`. The integer `r_w` has one exact next valuation
`a*`, so it realizes `wa*` and is its least representative. It cannot realize a
second next valuation. This proves uniqueness. The density bound follows by
counting. Equality of consecutive representatives after stabilization forces
every later edge to be the unique zero-lift edge.

### Reproducible calculation

- `5,460` words over valuations `{1,2,3,4}` through length six were checked.
- For every parent, next valuations `1..32` obeyed the exact lift rule.
- The zero-lift fraction fell from `0.234615` at `A=4` to exactly `1/64` at
  `A=64` on this sample.
- Eight natural starts, including `27`, `871`, and `6171`, followed only
  zero-lift edges after their cylinder representative stabilized.

### No-go and remaining gap

An almost-all argument may discard one child among many, but an infinite path
can select that one child at every depth. This formally explains why logarithmic
density results cannot simply be promoted to Collatz for every input. The next
lemma must exclude that exceptional path under the prefixwise non-descending
condition. It is still an every-orbit theorem and is not proved here.

## 3. Goldbach: post-hoc major frequencies are circular

### Declared proposition

Write a target-aligned Fourier representation as

```text
R = a + P - N,
P = p_1 + ... + p_m,  p_i > 0,
```

where the positive terms are sorted in descending order. Let `K*` be the least
`k` such that

```text
a + p_1 + ... + p_k > N.
```

Then `K*` exists if and only if `R>0`.

### Proof and no-go

If `K*` exists, the full positive mass is at least the selected prefix, so
`R>0`. If `R>0`, selecting all positive terms works, hence a least prefix
exists. Therefore selecting a target-dependent positive-frequency set after
observing all aligned signs is equivalent to knowing the desired positivity.
It is not a proof bridge.

The valid replacement is a family of arithmetic major arcs fixed by rational
approximation before the target-dependent sign realization is inspected. Their
positive main term must dominate the complementary signed deficit uniformly.

### Reproducible calculation

For prime supports `64,128,256,512,1024`, all `987` even targets were
zero-padded, Fourier reconstructed, and adaptively certified. The equivalence
failure count was zero and the maximum reconstruction error was below
`7.8e-12`. This finite success confirms the identity, not Goldbach. At support
`1024`, the median target needed 16 positive terms, while the hardest target
needed 1,328. The variation itself shows why the set cannot be chosen post hoc
and then called a uniform major arc.

## 4. Twin Prime: exact cost of combining all scale pairs

### Declared proposition

Let `A` be an `N by N` zero-margin matrix with `N=2^L`, and let `E_(j,k)` be
its tensor-Haar energy at row scale `j` and column scale `k`. Then

```text
||A||_op <= ||A||_F
          = sqrt(sum_(j,k) E_(j,k))
          <= L sqrt(max_(j,k) E_(j,k)).
```

The factor `L=log2 N` is sharp.

### Proof and sharp model

TICKET-173 Parseval gives the equality, and there are `L^2` scale pairs. For
sharpness, choose one normalized Haar wavelet from each scale and put coefficient
one on all selected row/column pairs. In Haar coordinates this is the rank-one
matrix `u v^T` with both vector norms `sqrt(L)`. Its operator norm is `L`, each
scale-pair energy is one, and omitting the constant coordinate makes all row and
column sums zero.

The construction was inverted to physical coordinates for `N=4,...,128`.
It saturated the bound at operator norms `2,3,4,5,6,7` with zero numerical
certificate failures. The four TICKET-161 finite prime-pair matrices also obeyed
the aggregation bound.

### Remaining gap

A true power saving uniform in both scale indices would survive the logarithmic
loss and close the full operator estimate. PrimeProject has not proved that
uniform arithmetic estimate.

## Cross-problem conclusion

The shared issue is quantifier-safe uniformity:

1. the RH cutoff must lie on one cofinal schedule whose total defect vanishes;
2. a density-zero Collatz branch still matters to an every-input statement;
3. Goldbach major arcs must be fixed independently of observed signs;
4. Twin cancellation must hold uniformly over every row/column scale pair.

This is a genuine narrowing of the search space, not a solution claim.

## Literature boundary

- [Groskin, finite Guinand-Weil dictionary and archimedean tail order, arXiv:2607.02828](https://arxiv.org/abs/2607.02828) provides the finite dictionary and tail order used by the RH schedule calculation and explicitly makes no RH claim.
- [Tao, almost all Collatz orbits attain almost bounded values, arXiv:1909.03562](https://arxiv.org/abs/1909.03562) is an almost-all logarithmic-density theorem, not the every-ray result required here.
- [Niu, parity vectors and paradoxical sequences, arXiv:2605.13886](https://arxiv.org/abs/2605.13886) supplies recent finite parity-vector context, not a global Collatz proof.
- [Grimmelt and Bhowmik, the exceptional set of the Goldbach problem, arXiv:2607.27282](https://arxiv.org/abs/2607.27282) provides major-arc and exceptional-set context, not the uniform binary domination named here.
- [Ford and Maynard, on the theory of prime producing sieves, arXiv:2407.14368](https://arxiv.org/abs/2407.14368) explains why substantial Type-II information is necessary; the Haar theorem only organizes that missing information.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket174_tail_lift_adaptive_scalepair.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket174_tail_lift_adaptive_scalepair -v
```

The canonical machine artifact is
`data/open-problem/ticket174-tail-lift-adaptive-scalepair.json`.
