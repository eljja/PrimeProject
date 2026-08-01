# TICKET-177: comparison majorants, six-wheel Collatz envelopes, Sobolev certificates, and signed cross-Gram data

## Claim boundary

TICKET-177 proves four exact refinements or no-go statements. It does not
prove or disprove the Riemann Hypothesis, the Collatz conjecture, strong
Goldbach, or the Twin Prime conjecture. All four statuses remain
`open_not_proven`; the machine resolution count and machine failure count are
both zero.

| Problem | Exact result | Route rejected | Next single lemma |
|---|---|---|---|
| Riemann | entrywise comparison-majorant certificate in one fixed relative basis | fitted weights and diagonal-only tail summaries | `PoleNeutralWeilWhitenedTailHasPredeclaredComparisonMajorantBelowCoreMargin` |
| Collatz | exact post-first-step six-wheel harmonic envelope | odd-only spacing or modulo-three exclusion as an iff test | `AperiodicNonDescendingValuationDiscrepancyExceedsSixWheelHarmonicEnvelope` |
| Goldbach | energy-plus-derivative pointwise positivity certificate | energy alone and the tested unsmoothed global certificate | `ParityAliasedMinorHasMultiscaleEnergyDerivativePowerSavingBelowMajorMain` |
| Twin Prime | signed cross-Gram identity and information-loss counterfamily | nonnegative block norms as sufficient cancellation statistics | `PrimePairHaarSignedCrossGramHasPowerSavingRelativeToDiagonalEnergy` |

## 1. Riemann: a predeclared relative comparison majorant

### Declared proposition

Let `G` be positive definite and let `A_T,A` be Hermitian. Suppose
`A_T >= delta G`. In one fixed `G`-orthonormal basis, write

```text
E = G^(-1/2)(A-A_T)G^(-1/2).
```

If a symmetric nonnegative matrix `M` satisfies `|E_ij| <= M_ij`, then

```text
A >= (delta-rho(M))G.
```

Every positive, predeclared weight `w` also gives

```text
rho(M) <= max_i (Mw)_i/w_i.
```

### Proof and no-go

For every vector `x`, componentwise `|Ex| <= M|x|`. Hence
`||E||_2 <= ||M||_2 = rho(M)`, because `M` is symmetric and nonnegative.
The variational principle gives `E >= -rho(M)I`, which proves the Loewner
bound after undoing the whitening.

The weighted row bound is the Collatz-Wielandt comparison after diagonal
scaling. For irreducible `M`, its infimum over all positive fitted weights is
exactly `rho(M)`. Unrestricted weight fitting is therefore circular: it
recomputes the unknown spectral target instead of proving an arithmetic tail
bound. A useful weight and comparison matrix must be fixed analytically before
examining the tail.

The reproducible tridiagonal comparison model has `delta=0.25`,
`rho(M)=0.1785640646`, and certified relative margin `0.0714359354`. The same
relative margin remains positive when the smallest metric scale ranges from
`10^-4` to `10^-128`. This validates the certificate, not the required Weil
tail premise.

### Remaining gap

No explicit symmetric comparison matrix currently majorizes every entry of
the whitened, pole-neutral arithmetic Weil tail below an independently
certified fixed-core margin.

## 2. Collatz: use the six-wheel after the first accelerated step

### Declared proposition

For the accelerated odd map

```text
T(n) = (3n+1)/2^v2(3n+1),
```

every state after the first step is odd and not divisible by `3`. If an orbit
is aperiodic and does not descend below its odd start `n`, its first `h`
post-first-step states are distinct members of the six-wheel. Ordering these
states gives a correction envelope with logarithmic coefficient

```text
1/(9 ln 2),
```

instead of TICKET-176's odd-only coefficient `1/(6 ln 2)`. The ratio is
exactly `2/3`.

### Proof and no-go

An accelerated image is odd by construction. It cannot be `0 mod 3`, because
`3n+1` is `1 mod 3` and division by a power of two preserves a nonzero residue
modulo `3`. Aperiodicity makes all states distinct. The `j`th eligible
six-wheel integer above the start is at least `n+3j-2`; applying
`log2(1+x) <= x/ln 2` and an integral bound to the resulting reciprocal sum
proves the sharper envelope.

The modulo-three restriction is not an iff criterion. All `49,999` odd starts
from `3` through `100,000` descend in the finite audit, but start `63` descends
at step `34` without crossing the sharper sufficient envelope. Thus the wheel
removes an avoidable density loss but does not force descent. Nontrivial cycles
must also be excluded separately.

### Remaining gap

No theorem forces every aperiodic non-descending natural orbit's centered
valuation discrepancy above the six-wheel envelope.

## 3. Goldbach: a rigorous energy-to-pointwise bridge

### Declared proposition

Let `P` be a real, mean-zero, one-periodic function with

```text
||P'||_infinity <= D,       integral_0^1 |P|^2 = E.
```

For `A>0`, either condition

```text
A > D/2
```

or

```text
E < A^3/(4D)       (D>0)
```

implies `A+P(x)>0` for every `x`.

For a parity-aliased trigonometric polynomial
`P(x)=sum d_k exp(2 pi i kx)`, Parseval gives
`E=sum |d_k|^2`, and a computable derivative bound is
`D <= 2 pi sum |k d_k|`.

### Proof and no-go

The shortest circular distance is at most `1/2`, so the derivative bound and
mean zero imply `min P >= -D/2`; this proves the first route. If
`P(x_0) <= -A`, then Lipschitz continuity gives `|P| >= A/2` on a circular
interval of length at least `A/D`. Therefore `E >= A^3/(4D)`, and the
contrapositive proves the second route.

The raw fixed-Farey audits at prime supports `64,128,256,512,1024` pass this
global certificate in `0/5` cases. This is a negative diagnostic, not a
Goldbach counterexample. The cosine family `P_k(x)=-a cos(2 pi kx)` also shows
that `L2` energy alone cannot imply positivity: its energy is independent of
frequency while its pointwise negative excursion persists.

### Remaining gap

The project has no target-uniform multiscale arithmetic estimates that make
both the aliased-minor energy and derivative budget small enough relative to
an independently proved major-arc lower bound.

## 4. Twin Prime: signed cross-Gram information is indispensable

### Declared proposition

For operators `T_1,...,T_m` with compatible domain and codomain,

```text
||sum_j T_j||^2 = ||sum_(i,j) T_i^* T_j||.
```

Consequently, the component norms `||T_j||` do not determine the norm of their
sum. Signed cross-Gram operators must be retained to measure cross-scale
cancellation.

### Proof and no-go

Expand `(sum_j T_j)^*(sum_j T_j)` and use `||T||^2=||T^*T||`. The three exact
families `[I,I]`, `[I,-I]`, and two orthogonal projections all have component
norm summary `(1,1)`, while their aggregate norms are respectively `2`, `0`,
and `1`. Thus identical nonnegative block-norm data permit complete alignment,
complete cancellation, and orthogonality.

All four audited TICKET-161 Type-II rows lack signed cross-Gram data. Their
block norms can upper-bound an operator, but cannot certify the cancellation
needed for a power saving.

### Remaining gap

No arithmetic dataset or theorem currently proves power-saving off-diagonal
signed cross-Gram cancellation for the actual prime-pair Haar blocks.

## Proof DAG and finite-computation boundary

Every track has the same machine-readable dependency shape:

```text
REFUTED_OR_INSUFFICIENT -> PROVED_EXACT -> OPEN_NOT_PROVEN
```

The middle node is a partial theorem or no-go statement, never a conjecture
resolution. Finite calculations verify identities, expose insufficient
statistics, and search for counterexamples only inside their stated ranges.
They do not promote a finite range to a universal theorem.

## Primary-literature boundary

- Recent [truncated Weil-form numerics](https://arxiv.org/abs/2605.20224), [finite Guinand-Weil tail control](https://arxiv.org/abs/2607.02828), and [operator experiments](https://arxiv.org/abs/2607.24830) do not prove the RH tail majorant isolated here.
- [Tao's almost-all Collatz theorem](https://arxiv.org/abs/1909.03562) does not give an every-orbit six-wheel crossing theorem.
- Recent [Goldbach exceptional-set work](https://arxiv.org/abs/2607.27282) does not supply a uniform pointwise binary minor-arc bound for every even target.
- [Ford and Maynard's sieve work](https://arxiv.org/abs/2407.14368) illustrates why genuine Type-I/II information, rather than block norms alone, is required.

## Reproduction

```powershell
python scripts/ticket177_comparison_wheel_sobolev_crossgram.py
python -m unittest tests.test_ticket177_comparison_wheel_sobolev_crossgram -v
```

Machine-readable artifacts:

```text
data/open-problem/ticket177-comparison-wheel-sobolev-crossgram.json
data/open-problem/riemann/rh-ticket-177-comparison-majorant.json
data/open-problem/collatz/co-ticket-177-six-wheel-envelope.json
data/open-problem/goldbach/gb-ticket-177-sobolev-certificate.json
data/open-problem/twin-prime/tp-ticket-177-signed-crossgram.json
```
