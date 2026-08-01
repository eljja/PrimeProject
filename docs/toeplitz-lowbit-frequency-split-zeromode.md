# TICKET-178: Toeplitz summability, Collatz low bits, Goldbach frequency splits, and cross-Gram zero modes

## Claim status

**All four conjectures remain open.** TICKET-178 proves four exact conditional
criteria or no-go statements. It neither proves nor disproves the Riemann
Hypothesis, the Collatz conjecture, strong Goldbach, or the Twin Prime
conjecture. Finite computations below are regression tests and route audits,
not induction steps to infinity.

| Problem | Exact result | Status | Rejected route | Remaining gap | Next single lemma |
|---|---|---|---|---|---|
| Riemann | `SummableToeplitzTailCertificateAndNonsummableProfileNoGo` | open | an absolute Toeplitz envelope with decay exponent `s <= 1` | no such summable arithmetic majorant is known for the actual whitened Weil tail | `PoleNeutralWeilWhitenedTailHasSummableOffDiagonalProfileBelowCoreMargin` |
| Collatz | `LowBitOccupancyDescentCriterionAndFixedHorizonMixingNoGo` | open | a universal fixed-horizon low-bit mixing claim | no every-orbit adaptive occupancy crossing or nontrivial-cycle exclusion | `EveryAperiodicNonDescendingOrbitCrossesLowBitOccupancyThreshold` |
| Goldbach | `FrequencySplitSobolevCertificateAndGlobalBudgetNoGo` | open | treating one global derivative-energy budget as necessary or scale-stable | no every-target arithmetic dyadic budget below the major term | `ParityAliasedMinorHasUniformDyadicSplitSobolevBudgetBelowMajorMain` |
| Twin Prime | `CrossGramZeroModeCertificateAndAbsolutePhaseErasureNoGo` | open | absolute cross-Gram magnitudes as sufficient statistics | no signed all-plus zero-mode power saving for prime-pair Haar blocks | `PrimePairHaarSignedCrossGramZeroModeHasPowerSavingRelativeToDiagonalEnergy` |

## 1. Riemann Hypothesis

### Declared proposition

Let `E_N` be an `N x N` Hermitian matrix and suppose

```text
|(E_N)_{ij}| <= C (1 + |i-j|)^(-s).
```

If `s > 1`, then, uniformly in `N`,

```text
||E_N||_2 <= C(2 zeta(s) - 1).
```

Consequently, if a whitened finite core has relative Loewner margin `delta`
and `C(2 zeta(s)-1) < delta`, the tail cannot destroy positivity. For
`s <= 1`, the positive Toeplitz matrices having equality in the displayed
profile have spectral radius tending to infinity with `N`.

### Proof

The Schur row-sum bound gives

```text
||E_N||_2 <= max_i sum_j |(E_N)_{ij}|
           <= C(1 + 2 sum_{r>=1}(1+r)^(-s)).
```

The final series is `2 zeta(s)-1` and converges exactly when `s>1`. For the
converse family, take all entries positive and equal to the profile. The
Rayleigh quotient of the normalized all-ones vector is

```text
R_N = C/N [N + 2 sum_{r=1}^{N-1}(N-r)/(1+r)^s].
```

It diverges logarithmically when `s=1` and as a positive multiple of
`N^(1-s)` when `s<1`. Thus no dimension-uniform **absolute profile**
certificate of this form exists at or below the summability threshold.

### Reproducible computation

The audit uses `C=0.02`, `delta=0.25`, dimensions
`16, 64, 256, 1024, 4096`, and exponents `0.75, 1, 1.25, 2`.

- Both nonsummable profiles cross the core margin in the tested finite sections.
- Both summable profiles have rigorous integral-tail row bounds below the margin.
- Every all-ones Rayleigh lower bound is below its finite Schur upper bound.

### Logical limit

This is a sharp threshold for a phase-blind Toeplitz majorant, not a theorem
about the actual pole-neutral Weil tail. Signed oscillation could yield a good
operator bound without an absolute `l1` profile. The missing result is an
arithmetic construction of a predeclared summable profile with a certified
constant, or a phase-sensitive replacement.

## 2. Collatz conjecture

### Declared proposition

For an accelerated odd orbit prefix `n_0,...,n_{h-1}`, put

```text
A_2(h) = #{i<h : n_i = 1 mod 4},
A_3(h) = #{i<h : n_i = 5 mod 8}.
```

Then

```text
sum_{i<h} v2(3n_i+1) >= h + A_2(h) + A_3(h).
```

If the prefix is aperiodic and never falls below `n_0`, the TICKET-177
six-wheel correction bound `H_6(n_0,h)` implies the necessary condition

```text
A_2(h)+A_3(h) <= (log2(3)-1)h + H_6(n_0,h).
```

Therefore strict violation of this inequality certifies descent.

### Proof

For odd `n`, direct congruence solving gives

```text
v2(3n+1) >= 2  iff n = 1 mod 4,
v2(3n+1) >= 3  iff n = 5 mod 8.
```

The layer-cake expansion of a positive integer valuation proves the lower
bound. The exact orbit identity is

```text
log2(n_h/n_0)
= h log2(3) - sum_{i<h} v2(3n_i+1) + C_h.
```

Non-descent makes the left side nonnegative, while TICKET-177 gives
`C_h <= H_6(n_0,h)`. Combining the inequalities proves the criterion.

### Fixed-horizon no-go family

For `n_0=2^m-1`, the first `m-2` relevant states satisfy

```text
n_i = 3^i 2^(m-i) - 1 = 7 mod 8,
v2(3n_i+1) = 1,
n_i >= n_0.
```

As `m` is arbitrary, every fixed horizon admits a natural non-descending
prefix with no `A_2` or `A_3` contribution. A universal fixed-horizon mixing
lemma is therefore false.

### Reproducible computation

For all `49,999` odd starts from `3` through `100,000`:

- every start reached a smaller value within the bounded search;
- `44,537` prefixes crossed the low-bit sufficient boundary by first descent;
- `5,462` descended without crossing it;
- the largest first-descent horizon was `85`;
- exact Mersenne-prefix checks passed for `m=8,16,32,64`.

These numbers do not prove Collatz for starts above the limit.

### Logical limit

Uniform distribution on the eight six-wheel classes would suggest
`A_2/h=1/2`, `A_3/h=1/4`, leaving asymptotic margin
`0.75-(log2(3)-1) ~= 0.165`. No theorem supplies that adaptive occupancy for
every hypothetical non-descending orbit. Nontrivial cycles also require a
separate exclusion argument.

## 3. Strong Goldbach conjecture

### Declared proposition

Let `P=L+H` be a real, mean-zero, one-periodic function split into
conjugate-symmetric frequency bands, with no zero mode in `H`. Suppose

```text
||H||_infinity <= B < A,
||L'||_infinity <= D,
integral_0^1 L(x)^2 dx <= E.
```

Then `A+P` is strictly positive if either

```text
A-B > D/2
```

or

```text
E < (A-B)^3/(4D).
```

For Fourier coefficients `d_k`, the computable bounds are

```text
B <= sum_high |d_k|,
E = sum_low |d_k|^2,
D <= 2 pi sum_low |k d_k|.
```

### Proof

First use `H(x)>=-B`. The low band has mean zero, so the TICKET-177 Sobolev
pointwise lemma applies to `L` with the residual major term `A-B`. Parseval,
termwise differentiation, and the triangle inequality give the displayed
Fourier budgets.

### Global-budget no-go family

For `K>=16`, define

```text
F_K(x) = 1 + 0.2 cos(2 pi x) + 0.1 cos(2 pi Kx).
```

The elementary lower bound is `F_K>=0.7`. Nevertheless the unsplit derivative
bound grows linearly in `K`, so the global TICKET-177 certificate fails for all
tested `K=16,64,256,1024`. Splitting off the high band with sup bound `0.1`
leaves residual major `0.9`; the low-band derivative certificate passes. Thus
the unsplit test is sufficient but not necessary and can degrade solely because
of harmless high-frequency content.

### Reproducible computation

The predeclared dyadic split audit uses prime supports
`64,128,256,512,1024` and the same fixed Farey mask as TICKET-177.

- Support `64` has at least one passing split.
- Supports `128,256,512,1024` have no passing tested split.
- Exact finite Goldbach counts remain positive on all five supports.

The final item checks only a bounded range and is not evidence of a uniform
binary Goldbach theorem.

### Logical limit

The theorem repairs a diagnostic defect but does not create the needed
arithmetic estimates. A proof still needs one predeclared, target-uniform
dyadic decomposition whose high-band sup budget and low-band Sobolev budget
both fit below an independently proved major-arc lower bound.

## 4. Twin Prime conjecture

### Declared proposition

For finite-dimensional operators `T_0,...,T_{m-1}`, define the scalar signed
Hilbert-Schmidt cross-Gram matrix

```text
H_ij = <T_i,T_j>_HS.
```

Then

```text
1* H 1 = ||sum_j T_j||_HS^2,
||sum_j T_j||_op^2 <= 1* H 1.
```

Hence

```text
1* H 1 <= eta sum_j ||T_j||_HS^2
```

is a sufficient aggregate operator power-saving certificate.

### Proof and phase-erasure no-go

The identity follows by expanding the Hilbert-Schmidt square; the inequality
is `||.||_op <= ||.||_HS`. For scalar operators compare

```text
T_j = 1
```

with

```text
T_j = exp(2 pi i j/m).
```

Both families have all component norms equal to one and all absolute
cross-Gram entries equal to one. Their signed all-plus zero modes are `m^2`
and `0`. Absolute cross-Gram magnitudes therefore lose exactly the phase
needed by the arithmetic aggregate.

### Reproducible computation

The audit checks `m=4,8,16,32`. At every size:

- the two absolute cross-Gram matrices agree to floating-point tolerance;
- aligned zero mode equals `m^2`;
- the roots-of-unity zero mode is below `1e-25`;
- diagonal energy is `m` for both families.

### Logical limit

This only states the correct sufficient data contract. The actual prime-pair
Haar blocks have not been shown to satisfy a signed zero-mode power saving.
Their Hilbert-Schmidt diagonal energy may also be too large unless arithmetic
rank and scale growth are controlled. No Twin Prime lower bound follows.

## Cross-problem conclusion

The four tracks now share one precise obstruction: a summary that is valid on
finite sections, fixed horizons, global frequency budgets, or absolute phases
does not control the one infinite or target-specific mode needed by the
conjecture. TICKET-178 replaces those summaries with four quantified next
lemmas. It does not establish any of them for the underlying arithmetic object.

## Literature boundary

- Recent computable Weil-form and explicit-tail projects provide finite
  sections and tail estimates, not the summable whitened profile required here:
  [arXiv:2605.20224](https://arxiv.org/abs/2605.20224),
  [arXiv:2607.02828](https://arxiv.org/abs/2607.02828), and
  [arXiv:2607.24830](https://arxiv.org/abs/2607.24830).
- Tao proves an almost-all logarithmic-density Collatz result, not an
  every-orbit occupancy theorem: [arXiv:1909.03562](https://arxiv.org/abs/1909.03562).
  A recent one-bit reduction motivates the low-bit target but is not treated as
  a resolution: [arXiv:2603.25753](https://arxiv.org/abs/2603.25753).
- Helfgott's minor-arc work concerns ternary Goldbach, while recent explicit
  binary work still uses exceptional sets:
  [arXiv:1205.5252](https://arxiv.org/abs/1205.5252) and
  [arXiv:2607.27282](https://arxiv.org/abs/2607.27282).
- Modern prime-producing sieves retain demanding Type-II distribution inputs;
  they do not supply the zero-mode lemma above:
  [arXiv:1910.14674](https://arxiv.org/abs/1910.14674) and
  [arXiv:2407.14368](https://arxiv.org/abs/2407.14368).

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts/ticket178_toeplitz_lowbit_split_zeromode.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket178_toeplitz_lowbit_split_zeromode -v
```

Machine-readable outputs:

```text
data/open-problem/ticket178-toeplitz-lowbit-split-zeromode.json
data/open-problem/riemann/rh-ticket-178-toeplitz-threshold.json
data/open-problem/collatz/co-ticket-178-lowbit-occupancy.json
data/open-problem/goldbach/gb-ticket-178-frequency-split.json
data/open-problem/twin-prime/tp-ticket-178-zeromode-crossgram.json
```

The generator exits nonzero if an internal theorem check fails. The JSON
contract fixes every attempt to `open_not_proven` and the conjecture resolution
count to zero.
