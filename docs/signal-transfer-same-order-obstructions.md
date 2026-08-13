# TICKET-226: Signal Transfer and Same-Order Obstructions

Korean edition: [signal-transfer-same-order-obstructions.ko.md](signal-transfer-same-order-obstructions.ko.md)

## Abstract and claim boundary

TICKET-226 audits the four continuation routes left by TICKET-225. It proves
four narrower theorems and resolves none of the Riemann, Collatz, strong
Goldbach, or Twin Prime conjectures.

| Problem | Exact TICKET-226 result | Route refuted or corrected | One next lemma |
|---|---|---|---|
| Riemann hypothesis | The actual prime band is a balanced, sign-changing Chebyshev-error contrast with negative and positive kernel masses `-1/4` and `+1/4` | A band sign directly supplies Weil positivity | `ExplicitFormulaControlOfBalancedChebyshevBandsOnDenseWeilCore` |
| Collatz conjecture | The infinite primitive family `(1,1,3)^r,2` consists of noncycles whose every cyclic intercept exceeds `D` | Every noncycle is certified by `min B_i<D` | `NoNontrivialPrimitiveValuationWordSatisfiesDDividesB` |
| Strong Goldbach conjecture | Cube-root rough semiprimes satisfy `S_z(X)~log(2)X/log X`, the same order as primes; finite `contamination<PP` is false | Treat rough-semiprime contamination as a lower-order marginal error | `FixedFareySignedMinorDeficitPowerSavingBelowMajorMainUniformly` |
| Twin Prime conjecture | The same marginal obstruction applies; exact finite gap-two rows refute pair contamination below `PP` at two horizons | Derive shifted separation from Type-I marginals alone | `ShiftedCubeRootParityTypeIIBilinearPowerSavingOnUnboundedBlocks` |

The common conclusion is about **signal transfer**. A computable observable may
be exact and still have the wrong sign geometry, while a precisely classified
error class may have the same asymptotic size as the intended signal.

## 1. Riemann hypothesis

### Proposition RH-226

Let

```text
psi(x) = sum_(n<=x) Lambda(n),
E(x)   = psi(x)-x,
P(a)   = sum_(n>=2) Lambda(n)[exp(-an)-exp(-2an)]-1/(2a).
```

For every `a>0`,

```text
P(a) = a integral_0^infinity E(x)[exp(-ax)-2exp(-2ax)] dx.   (RH-226.1)
```

Writing `u=ax`, the kernel `k(u)=exp(-u)-2exp(-2u)` changes sign at
`u=log 2`. Its two signed masses are exactly

```text
integral_0^log(2) k(u) du = -1/4,
integral_log(2)^infinity k(u) du = +1/4.                     (RH-226.2)
```

Thus `P(a)` is a zero-mass contrast between two regions of the Chebyshev
error. Its sign is not the value of a positive functional and cannot be read
directly as Weil positivity.

### Proof

Stieltjes partial summation gives, for `c>0`,

```text
sum Lambda(n)exp(-can) = ca integral_0^infinity psi(x)exp(-cax) dx.
```

Apply this with `c=1,2`, subtract, and use

```text
a integral x exp(-ax) dx       = 1/a,
2a integral x exp(-2ax) dx     = 1/(2a).
```

This proves `(RH-226.1)`. An antiderivative of `k` is
`-exp(-u)+exp(-2u)`, which proves `(RH-226.2)`.

### Reproducible calculation and limit

Eleven dyadic scales `a=2^-j`, `j=3,...,13`, were evaluated from actual von
Mangoldt prime powers with cutoff `48/a`. The direct prime sum and the
Chebyshev-kernel identity agree to below `10^-12`; all eleven negative signs
remain separated after the explicit TICKET-225 tail bound is added.

This explains the observable; it does not promote it to an RH criterion. In
particular, a positive atom below `log(2)/a` gives a negative band value and a
positive atom above the crossing gives a positive one. The complete band
profile may still be informative, as TICKET-222 and TICKET-223 established in
specified measure classes, but a quantitative explicit-formula bridge to a
dense Weil core remains absent.

## 2. Collatz conjecture

### Proposition CO-226

For every integer `r>=1`, define

```text
w_r = (1,1,3)^r,2.
```

This word is primitive. Its affine denominator and the least cyclic intercept
are

```text
D_r = 4*32^r-3*27^r,
B_r = (62*32^r-57*27^r)/5.                                  (CO-226.1)
```

Every cyclic intercept is at least `B_r`, and

```text
D_r < B_r < 4D_r,
D_r does not divide B_r.                                    (CO-226.2)
```

Hence every `w_r` is a certified noncycle, but none is certified by
`min_i B_i<D`. The TICKET-225 minimum-intercept test is sufficient, not
necessary, on an explicit infinite primitive family.

### Proof

The final exponent `2` occurs exactly once, so a nontrivial period is
impossible. The block `U=(1,1,3)` has affine data `(3^3,2^5,B)=(27,32,19)`.
Concatenating `U^r` and the final exponent gives `(CO-226.1)`.

Put `n_0=B_r/D_r`. Direct subtraction gives

```text
B_r-D_r       = 42(32^r-27^r)/5 > 0,
19D_r-5B_r    = 14*32^r > 0.
```

Thus `1<n_0<19/5`. Inside each `U`, the first two accelerated steps increase,
and the whole block maps

```text
n -> (27n+19)/32.
```

This map increases every `n<19/5` and preserves that interval. Therefore
`n_0` is the least cyclic state. The upper inequality in `(CO-226.2)` follows
from `20D_r-5B_r=18*32^r-3*27^r>0`.

If `B_r/D_r` were an integer, it would be `2` or `3`. Those cases require,
respectively,

```text
22*32^r = 27*27^r,
2*32^r  = 12*27^r,
```

both impossible by unique prime factorization. Thus `D_r` does not divide
`B_r`.

### Reproducible calculation and limit

All rotations were checked for `r=1,...,40`; selected rows through height
`121` are stored in the JSON artifact. This finite check is regression
evidence for the displayed all-`r` proof.

The result neither constructs a Collatz counterexample nor excludes all
nontrivial cycles. It removes one proposed universal size certificate. Exact
divisibility `D|B` and aperiodic orbit descent remain separate obligations.

## 3. Strong Goldbach conjecture

### Proposition GB-226

Let `z=X^(1/3)` and let `S_z(X)` count integers `pq<=X` with primes
`z<p<=q`. Then

```text
S_z(X) = sum_(z<p<=sqrt(X)) [pi(X/p)-pi(p-1)]                (GB-226.1)
```

and, by the prime number theorem,

```text
S_z(X) ~ (log 2) X/log X,
S_z(X)/pi(X) -> log 2.                                      (GB-226.2)
```

Cube-root rough semiprimes are therefore of the same marginal asymptotic order
as primes. They cannot be discarded as `o(P)` before additive correlation is
analyzed.

### Proof

Every rough semiprime has a unique smaller factor `p`, giving `(GB-226.1)`.
The subtraction contributes `O(X/log^2 X)`. Uniformly for
`X^(1/3)<p<=X^(1/2)`, the argument `X/p` is at least `sqrt(X)`, so PNT and
prime partial summation give

```text
S_z(X)
  ~ X integral_(X^(1/3))^(X^(1/2))
       dt/[t log(t) log(X/t)]
  = (X/log X) integral_(1/3)^(1/2) du/[u(1-u)]
  = (log 2)X/log X.
```

### Finite route counterexample

For the exact TICKET-225 decomposition at target `N=X`, let
`E=PS+SP+SS`.

| `N` | `PP` | `E` | `E/PP` | `E<PP` |
|---:|---:|---:|---:|---:|
| 10,000 | 254 | 270 | 1.063 | false |
| 100,000 | 1,620 | 1,812 | 1.119 | false |
| 1,000,000 | 10,804 | 14,882 | 1.377 | false |

Every row still has `PP>0`. These are counterexamples to the stronger
domination route, not to Goldbach. The PNT theorem is marginal and does not
give a pointwise convolution asymptotic. The retained route must obtain
signed arithmetic cancellation, for example a uniform major/minor-arc
inequality, rather than rely on semiprime sparsity.

## 4. Twin Prime conjecture

### Proposition TP-226

The marginal theorem `(GB-226.2)` also applies to the endpoints of the
TICKET-225 gap-two decomposition. It follows that Type-I marginal density
alone cannot make `PS`, `SP`, and `SS` lower order. It does **not** follow that
their shifted pair counts have any stated asymptotic; that requires Type-II
correlation information.

Complete finite classifications give:

| `X` | `PP` | `PS+SP+SS` | contamination/`PP` | contamination below `PP` |
|---:|---:|---:|---:|---:|
| 10,000 | 205 | 189 | 0.922 | true |
| 100,000 | 1,224 | 1,349 | 1.102 | false |
| 1,000,000 | 8,169 | 11,135 | 1.363 | false |

Thus even finite pair domination fails beyond the first listed horizon while
many twin primes remain. No asymptotic for the contamination pair count is
claimed. The remaining lemma asks for a genuine shifted Type-II bilinear power
saving on unbounded blocks; marginal PNT information is insufficient.

## Cross-track conclusion

TICKET-226 makes three route corrections and one exact reformulation:

1. RH requires transfer of a balanced contrast, not promotion of its sign.
2. Collatz minimum-intercept descent is not a universal noncycle criterion.
3. Goldbach rough-semiprime contamination has the same marginal order as the
   prime signal.
4. Twin separation consequently needs shifted Type-II information, not only
   Type-I marginals.

These results narrow the search space. They are not evidence that any parent
conjecture has been solved or disproved.

## Literature boundary

- Connes and Consani, [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368), gives the semi-local explicit-formula and Weil-positivity context. The balanced kernel identity here is not their RH criterion.
- Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562), proves an almost-all result and leaves the every-orbit gap open.
- Helfgott, [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438), supplies primary circle-method context; it does not prove strong binary Goldbach.
- Ford and Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368), explains why substantial Type-II information is necessary for prime-producing lower bounds.
- The Polymath project, [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897), is a primary reference for bounded gaps and the exact-gap parity boundary.

No literature-priority claim is made for the elementary kernel calculation,
the explicit Collatz counterfamily, or the rough-semiprime counting
application of PNT.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket226_signal_transfer_same_order_obstructions.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket226_signal_transfer_same_order_obstructions -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
node scripts\verify_pages.cjs
```

Primary machine-readable artifact:

`data/open-problem/ticket226-signal-transfer-same-order-obstructions.json`
