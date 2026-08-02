# TICKET-182: Sobolev, Divisibility, Translation, and Sibling Localization

## Status and claim boundary

TICKET-182 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, the strong Goldbach conjecture, or the Twin Prime conjecture. It
proves four exact refinements of the TICKET-181 bridges and adds finite
arithmetic diagnostics. The diagnostics do not replace universal estimates.

| Problem | Exact result | Resolution status |
|---|---|---|
| Riemann | `FejerH1TailCertificateAndRawPrimeEnergyNoGo` | exact theorem; RH open |
| Collatz | `AcceleratedCycleIffAffineDivisibility` | exact theorem; Collatz open |
| Goldbach | `WeightedTranslationModulusCertificateAndRmsSpikeNoGo` | exact theorem; Goldbach open |
| Twin Prime | `WeightedSiblingContrastIdentityAndMeanPathNoGo` | exact theorem; Twin Prime open |

No literature-priority claim is made for these elementary reductions without an
independent novelty review. Their role is to define proof obligations that are
both exact and machine-testable.

## What changed after TICKET-181

TICKET-181 identified four localization currencies. TICKET-182 makes each one
closer to the relevant representation:

```text
Riemann:    Lipschitz modulus -> Fourier-multiplier H1 energy
Collatz:   slack equality -> exact affine divisibility
Goldbach:  adjacent difference -> weighted uniform translations
Twin:      abstract path increments -> mass-weighted sibling contrasts
```

The recurring obstruction is concentration. Sampled values, scalar valuation
averages, RMS translations, and level-averaged tree increments can all hide one
decisive direction or exceptional path.

## 1. Riemann Hypothesis

### Declared proposition

Let

```text
f(theta) = sum_k a_k exp(i k theta)
```

be absolutely continuous and set

```text
D2^2 = integral[-pi,pi] |f'(theta)|^2 dtheta/(2*pi)
     = sum_k k^2 |a_k|^2.
```

For the order-`N` Fejer mean `sigma_N f`, define

```text
C_N^2 = 2 ((N-1)/N^2 + sum_(k>=N) 1/k^2).
```

Then

```text
||f-sigma_N f||_infinity <= C_N D2.
```

Consequently,

```text
||sigma_N f||_infinity + C_N D2 < delta
```

certifies `||f||_infinity<delta`.

### Proof

The residual Fejer multiplier is

```text
q_N(k) = min(|k|/N, 1),  k != 0.
```

Therefore, for every `theta`,

```text
|(f-sigma_N f)(theta)|
 <= sum_(k!=0) q_N(k)|a_k|
 <= (sum_(k!=0) q_N(k)^2/k^2)^(1/2)
    (sum_(k!=0) k^2|a_k|^2)^(1/2).
```

The first factor is exactly `C_N`, and Parseval identifies the second factor
with `D2`.

This global energy cannot be inferred from an `N`-point grid, even when both
values and derivatives are sampled. The function

```text
A(1-cos(N theta))
```

and its derivative vanish at every `theta=2*pi*j/N`, but the function has
uniform norm `2A` and normalized derivative energy `AN/sqrt(2)`.

### Raw-prime energy no-go

For the finite real proxy

```text
f_P(theta) = sum_(n<=P) Lambda(n)/sqrt(n) cos(n theta),
```

Parseval gives

```text
D2(P)^2 = (1/2) sum_(n<=P) n Lambda(n)^2.
```

This diverges along the infinitely many prime terms. Thus the raw unsmoothed
positive prime-coefficient proxy cannot have a uniform `H1` budget.

| `P` | `D2(P)^2` | `D2(P)` |
|---:|---:|---:|
| 100 | 8,918 | 94.4 |
| 1,000 | 1,572,496 | 1,254.0 |
| 10,000 | 217,628,540 | 14,752.2 |
| 100,000 | 27,527,213,831 | 165,913.3 |

The finite proxy is not the actual pole-neutral Weil symbol. It establishes a
no-go only for importing raw positive prime coefficients into this `H1`
certificate without smoothing or phase cancellation.

### Decision

- **Discard:** raw unsmoothed prime `H1` energy and grid-sampled derivative
  estimates.
- **Retain:** a smoothed, phase-preserving pole-neutral symbol with a rigorous
  global derivative-energy bound.
- **Remaining gap:** no such arithmetic `H1` budget is below the core margin.
- **Next lemma:**
  `SmoothedPoleNeutralWeilSymbolHasWeightedH1EnergyBelowCoreMargin`.

Recent finite Weil-operator computations also state that their evidence is
numerical rather than an RH proof ([Kim et al. 2026](https://arxiv.org/abs/2607.24830),
[Groskin 2026](https://arxiv.org/abs/2605.20224)).

## 2. Collatz conjecture

### Declared proposition

For a positive accelerated valuation word `w=(v_0,...,v_(h-1))`, let

```text
S = sum_j v_j,
B(w) = sum_j 3^(h-1-j) 2^(v_0+...+v_(j-1)),
D = 2^S-3^h.
```

Then `w` is the exact valuation word of a positive odd accelerated Collatz cycle
if and only if

```text
D > 0 and D divides B(w).
```

If `w_j` is the `j`-th cyclic rotation and `B_j=B(w_j)`, its cycle values are

```text
n_j = B_j/D.
```

### Proof

A cycle satisfies

```text
2^S n_0 = 3^h n_0+B(w),
```

so `Dn_0=B(w)`. Conversely, the rotation numerators obey the exact identity

```text
3B_j+D = 2^(v_j) B_(j+1).
```

Because `D` is odd, `D|B_0` propagates through every rotation. Hence each
`n_j=B_j/D` is a positive odd integer and

```text
3n_j+1 = 2^(v_j)n_(j+1).
```

The displayed power of two is exact because `n_(j+1)` is odd.

### Reproducible finite audit

Every word over `{1,2,3,4,5}` through horizon eight was tested exactly.

| `h` | words | contracting | `D|B` hits | trivial `(2,...,2)` | nontrivial |
|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 4 | 1 | 1 | 0 |
| 2 | 25 | 22 | 1 | 1 | 0 |
| 3 | 125 | 121 | 1 | 1 | 0 |
| 4 | 625 | 610 | 1 | 1 | 0 |
| 5 | 3,125 | 3,104 | 1 | 1 | 0 |
| 6 | 15,625 | 15,541 | 1 | 1 | 0 |
| 7 | 78,125 | 77,795 | 1 | 1 | 0 |
| 8 | 390,625 | 390,130 | 1 | 1 | 0 |

The total is 488,280 words. All eight divisibility hits are fixed-point
repetitions. This is finite evidence only.

### No-go and decision

The average `S/h` cannot exclude equality: `(2,...,2)` has positive `D` and
`D|B` at every length. A nontrivial-cycle proof must use the ordered numerator,
not only average valuation surplus.

- **Discard:** average valuation surplus or bounded slack audits as a universal
  cycle-exclusion argument.
- **Retain:** exact affine divisibility for every ordered valuation word.
- **Remaining gap:** nondivisibility is unproved for arbitrary nonconstant words.
- **Next lemma:**
  `OnlyConstantTwoValuationWordsSatisfyPositiveAffineCycleDivisibility`.

Almost-all orbit results do not imply this every-word divisibility exclusion
([Tao 2019/2026](https://arxiv.org/abs/1909.03562)).

## 3. Strong Goldbach conjecture

### Declared proposition

Let `e` be real on `Z/LZ`, and let `sigma_w e=w*e` for a nonnegative kernel
with `sum_t w_t=1`. Define the uniform translation modulus

```text
omega_e(t) = max_j |e_j-e_(j-t)|.
```

Then

```text
||e-sigma_w e||_infinity <= sum_t w_t omega_e(t).
```

This is at least as sharp as TICKET-181 because

```text
omega_e(t) <= D d_L(0,t)
```

when `D` is the maximum adjacent difference.

### Proof and RMS no-go

For each target,

```text
e_j-(w*e)_j = sum_t w_t(e_j-e_(j-t)).
```

The triangle inequality proves the certificate. It retains actual long-shift
cancellation instead of replacing every shift by a telescoped adjacent bound.

RMS translations cannot replace `omega_e`. A one-site spike of height `A` has
nonzero-shift RMS `A sqrt(2/L)`, while its Fejer residual at the spike is
`A(1-w_0)`. With degree `o(L)`, the former tends to zero and the latter to `A`.

The five model sizes `L=64,...,1024` satisfy the uniform certificate. Their RMS
spike budget-to-error ratio falls from about `0.18` to `0.04`, demonstrating the
wrong inference direction.

### Finite arithmetic diagnostic

Unordered odd-prime representation counts were computed for even targets through
20,000. On the 5,000 targets from 10,002 through 20,000, the count was normalized
by its empirical block mean. Uniform translation moduli for shifts
`2,4,8,16,32,64` are about `2.00` to `2.07`, while RMS moduli are about `0.66` to
`0.67`.

The empirical block mean is not a proved circle-method major term. These values
diagnose concentration but prove no asymptotic bound.

### Decision

- **Discard:** RMS or average translation regularity as every-target control.
- **Retain:** Fejer-weighted uniform translation moduli for the actual residual.
- **Remaining gap:** the required arithmetic bound is unproved on every large
  block.
- **Next lemma:**
  `GoldbachResidualHasWeightedUniformTranslationModulusBelowLowPassMarginOnEveryLargeBlock`.

Exceptional-set results still allow exceptional targets and therefore do not
supply this uniform modulus ([Grimmelt and Bhowmik 2026](https://arxiv.org/abs/2607.27282)).

## 4. Twin Prime conjecture

### Declared proposition

Let sibling blocks have positive masses `m_L,m_R`, additive statistics
`S_L,S_R`, and ratios `r_L=S_L/m_L`, `r_R=S_R/m_R`. Then

```text
r_P = (m_L r_L+m_R r_R)/(m_L+m_R),
r_L-r_P = m_R(r_L-r_R)/(m_L+m_R),
r_R-r_P = m_L(r_R-r_L)/(m_L+m_R).
```

Thus every path increment is exactly a mass-weighted sibling contrast.

### Mean-path no-go

Put unit signal on one leaf of a uniform depth-`L` tree and zero elsewhere.
The root ratio is `2^(-L)`, the selected leaf ratio is one, and the selected
path variation is `1-2^(-L)`. However, the mean absolute increment at every
level is only `2^(-L)`, so the sum of level means is

```text
L/2^L -> 0.
```

Consequently, averaged tree regularity cannot replace a uniform path budget.

### Finite prime-pair diagnostic

On `[100000,362144)`, the generator finds 2,298 actual twin-prime starts. Using
the Hardy-Littlewood expected mass as the positive block mass gives:

| Quantity | Value |
|---|---:|
| root actual/expected ratio | 1.00038 |
| highest 1,024-point leaf ratio | 1.94275 |
| selected path `l1` variation | 1.08179 |
| sibling identity numerical error | `1.2e-16` or less |

This is one finite tree and not a future-block lower bound.

### Decision

- **Discard:** level-averaged oscillation and isolated favorable finite trees.
- **Retain:** mass-weighted sibling contrasts controlled on every dyadic path.
- **Remaining gap:** no arithmetic uniform path budget or parity-breaking positive
  lower bound is known.
- **Next lemma:**
  `PrimePairSiblingContrastHasUniformCarlesonPathBudgetBelowCancellationMargin`.

## Cross-problem conclusion

TICKET-182 establishes four exact statements and four sharp inference barriers.
It does not close an infinite arithmetic premise:

```text
RH:        smoothed arithmetic H1 energy below the core margin
Collatz:  D does not divide B(w) for every nonconstant positive word
Goldbach: weighted uniform residual translations below every low-pass margin
Twin:     uniform sibling-contrast path budget plus parity-breaking positivity
```

The generated JSON records `4` exact theorems, `4` rejected routes, `4` proof
DAGs, `0` machine failures, and `0` conjecture resolutions.

