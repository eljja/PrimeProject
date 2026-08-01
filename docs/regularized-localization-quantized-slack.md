# TICKET-181: Regularized Localization and Quantized Slack

## Status and claim boundary

TICKET-181 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, the strong Goldbach conjecture, or the Twin Prime conjecture. It
proves four exact intermediate statements that refine the localization failures
identified by TICKET-180.

| Problem | Exact result | Resolution status |
|---|---|---|
| Riemann | `LipschitzFejerTailCertificateAndSampledRegularityNoGo` | exact theorem; RH open |
| Collatz | `OddCylinderSlackQuantizationAndCycleEqualityObstruction` | exact theorem; Collatz open |
| Goldbach | `DiscreteFejerExceptionRemovalCertificateAndSpikeModulusNoGo` | exact theorem; Goldbach open |
| Twin Prime | `DyadicPathVariationLocalizationAndScaleL2NoGo` | exact theorem; Twin Prime open |

The proofs below are elementary once the relevant representation has been
chosen. Their value is architectural: they state exactly what estimate would
turn a finite or averaged computation into the universal conclusion required by
each conjecture. No claim of literature priority is made without independent
novelty review.

## From impossibility to a conditional bridge

TICKET-180 showed that finite frequencies, unordered orbit summaries,
almost-all bounds, and global averages are insufficient. TICKET-181 supplies a
different currency for each missing localization step:

```text
Riemann:     finite Fejer mean + proved global modulus
Collatz:    rigorous sub-quantum bound + equality exclusion
Goldbach:   discrete Fejer low pass + adjacent-target modulus
Twin Prime: root anchor + summable pathwise l1 oscillation
```

These are conditional bridges. The project has not proved that the actual Weil
symbol, Collatz cylinders, Goldbach residual, or prime-pair blocks satisfy the
new arithmetic hypotheses.

## 1. Riemann Hypothesis

### Declared proposition

Let `f` be a real, `2*pi`-periodic, `L`-Lipschitz function. Let `sigma_N f` be
its Fejer mean with Fourier modes `|k|<N`, and let

```text
mu_N = integral[-pi,pi] |t| F_N(t) dt / (2*pi)
     = pi/2 - (4/pi) sum_{1 <= k < N, k odd} (1-k/N)/k^2.
```

Then

```text
||f - sigma_N f||_infinity <= L mu_N.
```

Consequently,

```text
||sigma_N f||_infinity + L mu_N < delta
```

is a valid certificate for `||f||_infinity < delta`.

The global constant `L` cannot be replaced by a slope inferred only from `Q`
uniform samples. The functions `0` and `A sin(Q theta)` agree at every point
`theta_j=2*pi*j/Q`; their sampled adjacent differences are both zero, while the
second function has uniform norm `A` and Lipschitz constant `AQ`.

### Proof

The Fejer kernel `F_N` is nonnegative and has normalized mass one. Therefore

```text
|f(theta)-sigma_N f(theta)|
 <= integral F_N(t)|f(theta)-f(theta-t)| dt/(2*pi)
 <= L integral F_N(t)|t| dt/(2*pi).
```

The displayed formula for `mu_N` follows by integrating the Fourier expansion
of `|t|` against `F_N`. The sampled counterfamily follows from
`sin(2*pi*j)=0`. This proves both the positive certificate and the no-go for a
post-hoc grid estimate.

### Reproducible diagnostics

For the smooth witness `f(theta)=0.1 cos(theta)` and `delta=0.25`:

| N | `mu_N` | certified norm |
|---:|---:|---:|
| 8 | 0.345946 | 0.122095 |
| 16 | 0.200627 | 0.113813 |
| 32 | 0.114113 | 0.108286 |
| 64 | 0.063952 | 0.104833 |
| 128 | 0.035424 | 0.102761 |
| 256 | 0.019436 | 0.101553 |

All six model certificates pass. The hidden sine counterfamily is invisible on
the selected grids but pays the correct nonzero global regularity budget. These
models validate the inequality; they are not the arithmetic Weil symbol.

### Decision and remaining gap

- **Discard:** sampled slopes or observed Fourier modes as a substitute for a
  proved global modulus.
- **Retain:** a finite Fejer certificate with an independently proved modulus
  for the actual pole-neutral symbol.
- **Remaining gap:** no such arithmetic modulus is proved below the core
  positivity margin.
- **Next lemma:**
  `PoleNeutralWeilSymbolHasCertifiedModulusWhoseFejerBudgetFitsBelowCoreMargin`.

Finite Guinand-Weil dictionaries provide rigorous finite formulae but do not
claim RH; the missing global regularity estimate remains external to the finite
dictionary ([Groskin 2026](https://arxiv.org/abs/2607.02828)).

## 2. Collatz conjecture

### Declared proposition

For a positive accelerated valuation word `w=(v_0,...,v_(h-1))`, define

```text
S = sum v_j,
B = sum_j 3^(h-1-j) 2^(v_0+...+v_(j-1)),
D = 2^S - 3^h.
```

Let `r` be the least positive odd representative of its natural cylinder,
whose modulus is `M=2^(S+1)`, and let the odd endpoint be
`u=(3^h r+B)/2^S`. The descent slack

```text
H = rD-B = 2^S(r-u)
```

belongs to `M*Z`. Hence the rigorous inequality `H>-M` implies `H>=0`. If
`H=0` is independently excluded, then `H>=M>0`. When `D>0`, every later member
`r+kM` of the same cylinder also strictly descends after `h` accelerated steps.

### Proof

Endpoint integrality gives `3^h r+B=2^S u`, so subtraction from `2^S r`
gives `H=2^S(r-u)`. Both `r` and `u` are odd, hence `r-u` is even and
`2^(S+1)` divides `H`. For `D>0`, replacing `r` by `r+kM` changes the slack to
`H+kMD`, which preserves strict positivity.

Equality cannot be ignored. The one-step word `(2)` has `r=u=1`, `D=1`, and
`H=0`; it is the fixed point. Thus a sub-quantum lower bound alone proves only
nonincrease, not strict descent.

### Reproducible diagnostics

Every word over `{1,2,3,4}` through horizon eight was evaluated exactly.

| h | words | nonterminal contracting | positive quantum | zero | negative |
|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 2 | 2 | 0 | 0 |
| 2 | 16 | 12 | 12 | 0 | 0 |
| 3 | 64 | 59 | 59 | 0 | 0 |
| 4 | 256 | 240 | 240 | 0 | 0 |
| 5 | 1,024 | 1,002 | 1,002 | 0 | 0 |
| 6 | 4,096 | 4,011 | 4,011 | 0 | 0 |
| 7 | 16,384 | 16,060 | 16,060 | 0 | 0 |
| 8 | 65,536 | 65,048 | 65,048 | 0 | 0 |

The 87,380 listed words plus the fixed-point boundary contain no arithmetic
identity failure. Their positive counts are finite evidence only: valuations
larger than four and horizons larger than eight remain untested.

### Decision and remaining gap

- **Discard:** a near-nonnegative floating-point slack estimate without exact
  enclosure and equality exclusion.
- **Retain:** exact one-quantum enclosure plus a separate obstruction to cycle
  equality.
- **Remaining gap:** no all-horizon argument establishes a positive quantum for
  every first-contracting nonterminal cylinder; nontrivial cycles remain open.
- **Next lemma:** `EveryFirstContractingNonterminalCylinderHasPositiveSlackQuantum`.

Tao's almost-all result controls almost every orbit in logarithmic density, not
every cylinder or possible cycle, so it does not supply this lemma
([Tao 2019/2026](https://arxiv.org/abs/1909.03562)).

## 3. Strong Goldbach conjecture

### Declared proposition

Let `e` be a real sequence on `Z/LZ`, let
`D=max_j |e_(j+1)-e_j|`, and let `sigma_K e=w*e` be the discrete Fejer mean,
where `2K<L`, `w_t>=0`, and `sum_t w_t=1`. With cyclic distance `d_L`, set

```text
mu_(K,L) = sum_t w_t d_L(0,t).
```

Then

```text
||e-sigma_K e||_infinity <= D mu_(K,L).
```

For a declared major sequence `A`, the inequality

```text
min_j (A_j + sigma_K e_j) > D mu_(K,L)
```

therefore proves `A_j+e_j>0` at every target.

### Proof

The adjacent-target bound telescopes to
`|e_j-e_(j-t)|<=D d_L(0,t)`. Averaging with the nonnegative unit-mass kernel
proves the uniform approximation inequality. Subtracting that error budget from
the low-pass margin proves every-target positivity.

The one-site counterexample from TICKET-180 is not hidden by this criterion: a
spike has a large adjacent-target modulus, so its certificate margin is
nonpositive.

### Reproducible diagnostics

| L | K | smooth certificate margin | spike certificate margin |
|---:|---:|---:|---:|
| 32 | 5 | 0.374506 | -1.583437 |
| 64 | 8 | 0.379760 | -2.673095 |
| 128 | 11 | 0.383199 | -4.737762 |
| 256 | 16 | 0.386795 | -7.628441 |
| 512 | 22 | 0.389393 | -12.454936 |

All smooth witnesses pass and every exceptional spike is rejected. A separate
exact sieve finds no strong-Goldbach counterexample for the 49,999 even targets
from 4 through 100,000. That search is a bounded certificate, not a proof of the
infinite statement.

### Decision and remaining gap

- **Discard:** low-frequency or almost-all control without a target-space
  modulus.
- **Retain:** discrete Fejer values plus a rigorous adjacent-target residual
  modulus.
- **Remaining gap:** no arithmetic bound places the actual parity-aliased
  Goldbach residual below this margin on every sufficiently large block.
- **Next lemma:**
  `ParityAliasedGoldbachResidualHasCertifiedDiscreteModulusBelowFejerMarginOnEveryLargeBlock`.

Current exceptional-set and major-arc work still permits exceptional targets
and therefore does not provide the required uniform modulus
([Grimmelt and Bhowmik 2026](https://arxiv.org/abs/2607.27282)).

## 4. Twin Prime conjecture

### Declared proposition

Let `r(B)` be a real normalized statistic on a rooted dyadic block tree. Let
`epsilon_j` be the supremum of
`|r(C)-r(parent(C))|` over edges entering depth `j`. Every block `B` at depth
`ell` satisfies

```text
|r(B)| <= |r(root)| + sum_{j=1}^ell epsilon_j.
```

Thus a root bound and summable pathwise `l1` oscillation yield uniform block
localization. Vanishing maximum edge size or vanishing pathwise `l2` variation
alone does not.

### Proof and counterfamily

Telescoping along the unique root-to-`B` path and applying the triangle
inequality proves the bound. For depth `L`, assign values `j/L` along one path
and freeze the parent value on every branch leaving that path. Then

```text
maximum edge = 1/L -> 0,
path l2 = 1/sqrt(L) -> 0,
path l1 = 1,
selected leaf = 1.
```

The desired bad leaf therefore survives both weaker hypotheses, while the `l1`
bound is sharp.

| depth L | max edge | path l2 | path l1 | bad leaf |
|---:|---:|---:|---:|---:|
| 8 | 0.125000 | 0.353553 | 1 | 1 |
| 16 | 0.062500 | 0.250000 | 1 | 1 |
| 32 | 0.031250 | 0.176777 | 1 | 1 |
| 64 | 0.015625 | 0.125000 | 1 | 1 |
| 128 | 0.007812 | 0.088388 | 1 | 1 |

### Decision and remaining gap

- **Discard:** vanishing per-scale or square-summed oscillation as sufficient
  for every-block cancellation.
- **Retain:** a root anchor and summable `l1` oscillation along every dyadic
  path.
- **Remaining gap:** no such estimate is proved for actual prime-pair block
  statistics, and localization does not itself cross the parity barrier.
- **Next lemma:**
  `PrimePairBlockZeroModeRatioHasSummableDyadicPathOscillationBelowCancellationMargin`.

Prime-producing sieve results require genuine Type-II information and do not
derive exact gap-two positivity from this abstract localization condition
([Ford and Maynard 2024](https://arxiv.org/abs/2407.14368)).

## Reproduction and falsification contract

```powershell
D:\python\anaconda3\python.exe scripts\ticket181_regularized_localization_quantized_slack.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket181_regularized_localization_quantized_slack -v
```

Machine-readable outputs:

- `data/open-problem/ticket181-regularized-localization-quantized-slack.json`
- `data/open-problem/riemann/rh-ticket-181-fejer-modulus.json`
- `data/open-problem/collatz/co-ticket-181-slack-quantum.json`
- `data/open-problem/goldbach/gb-ticket-181-discrete-fejer.json`
- `data/open-problem/twin-prime/tp-ticket-181-tree-variation.json`

Every per-problem artifact contains a three-node proof DAG:

```text
refuted or insufficient route -> exact TICKET-181 theorem -> open next lemma
```

The machine contract requires four exact intermediate theorems, four rejected
targets, four proof DAGs, zero audit failures, and exactly zero conjecture
resolutions.
