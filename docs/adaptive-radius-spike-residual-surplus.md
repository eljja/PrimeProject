# TICKET-218: Adaptive Radii, Exponential Spikes, Residual Moments, and Abel Surplus

## Claim boundary

TICKET-218 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, strong Goldbach, or the Twin Prime conjecture. It proves four exact
partial, reduction, or no-go statements. Every parent problem remains
`open_not_proven`, and the machine resolution count is zero.

This ticket attacks the four open lemmas left by TICKET-217. It replaces each
qualitative request for "more precision" with one explicit strict margin that
would be sufficient for promotion to an infinite result.

| Problem | Exact result | Discarded route | Remaining gap | Next lemma |
| --- | --- | --- | --- | --- |
| Riemann | `ScaleAdaptiveRadiusCertificateAndSignalPhaseTransition` | a radius schedule whose first-atom signal vanishes against fixed absolute error | an actual-zeta cofinal bound below `exp(-tau)` | `ActualZetaScaleAdaptiveDefectEnvelopeBelowExpMinusTau` |
| Collatz | `ExponentialNextDenominatorSpikeBarrierAnd49ConvergentExclusion` | constructing every enormous cross-power difference | all future exponential partial-quotient spikes, then multi-run words and divergence | `EffectiveExponentialPartialQuotientBoundForCollatzLogRatio` |
| Goldbach | `SharpResidualMomentSupportCertificateAndExactEighthMomentAudit` | the failed uncentered second moment and a non-strict residual threshold | a cofinal arithmetic eighth-moment estimate independent of enumeration | `CofinalGoldbachEighthResidualMomentBelowZeroCoordinateBarrier` |
| Twin Prime | `SharpAbelSurplusToTwinCountTransferAtCriticalConstant` | equality at the critical Abel coefficient | an actual twin Abel liminf strictly above `1/2` | `ActualTwinAbelLiminfCoefficientGreaterThanOneHalf` |

## 1. Riemann Hypothesis: a nonvanishing-signal radius schedule

### Declared proposition

Within the defect-measure formulation inherited from TICKET-216 and
TICKET-217, let `C(H)` count off-critical symmetry pairs through height `H`
and let

```text
L(r) = integral r^t dC(t),       0 < r < 1.
```

For fixed `tau>0`, choose the moving radius

```text
r_H = exp(-tau/H).
```

Then

```text
r_H^H = exp(-tau),
C(H) <= floor(exp(tau) L(r_H)).
```

The same conclusion holds with a rigorous upper bound `U_H>=L(r_H)`. Thus

```text
U_H < exp(-tau)
```

certifies `C(H)=0`. If this holds on a cofinal sequence of heights, every
finite height is eventually covered and `C` is identically zero. Under the
already stated equivalence between `C=0` and absence of off-critical zeros,
this would imply RH.

More generally, put `beta_H=-log r_H`. The first-atom signal is

```text
r_H^H = exp(-H beta_H).
```

It has a positive uniform lower bound when `H beta_H` is bounded above, and it
vanishes when `H beta_H` tends to infinity.

### Proof and computation

TICKET-217 proves `C(H)r_H^H<=L(r_H)`. Substitute the displayed identity,
divide, and use integrality of `C(H)`. Cofinality promotes the finite-height
certificates because every fixed height lies below a later certified height.
The schedule dichotomy follows directly from the exponential identity.

The generator checks `tau=1,2` and heights through `10^9` at 90 decimal
digits. These rows verify the implementation of the identity; they are not
zeta computations.

### No-go and remaining gap

If `H(-log r_H)` tends to infinity, the signal of one defect at height `H`
again tends to zero. A fixed positive absolute error floor therefore cannot
close that schedule. The adaptive schedule avoids this information loss, but
the project does not derive the required rigorous upper bound from the actual
zeta explicit formula. No off-critical zero is found, and no zero-free region
is improved.

## 2. Collatz: only an exponential partial-quotient spike can escape

### Declared proposition

Let

```text
alpha = log(3/2)/log(4/3)
```

and let `p_n/q_n` be an upper continued-fraction convergent of `alpha`. Write
`q_(n+1)` for the next convergent denominator. If

```text
4(q_n + q_(n+1)) < 3^p_n,
```

then the TICKET-217 scaling barrier holds, so no positive multiple of
`p_n/q_n` can be the exponent ratio of a single-mountain Collatz cycle
`1^k 2^m`.

Consequently, any upper convergent not excluded by this sufficient test must
satisfy the exponential spike condition

```text
4(q_n + q_(n+1)) >= 3^p_n.
```

The exact rational-interval computation certifies 100 continued-fraction
coefficients. It excludes the first 49 upper convergents: the first by the
TICKET-217 exact base-difference comparison and the next 48 by the new
neighbor-denominator inequality. The next unaudited upper convergent is

```text
p = 16672027258049147969018986102532625254200541727292
q = 11828991589305104738667316989568711874512497900863.
```

Therefore no single-mountain cycle has

```text
k < 11828991589305104738667316989568711874512497900863.
```

### Proof

The standard continued-fraction inequality is

```text
|alpha-p_n/q_n| > 1/(q_n(q_n+q_(n+1))).
```

For an upper convergent, put

```text
lambda_n = p_n log(4/3)-q_n log(3/2) > 0.
```

Multiplication of the continued-fraction lower bound by
`q_n log(4/3)` gives

```text
lambda_n > log(4/3)/(q_n+q_(n+1)).
```

The elementary inequality `log(1+x)>x/(1+x)` gives
`log(4/3)>1/4`. Hence the integer condition implies

```text
lambda_n > 3^(-p_n),
exp(lambda_n)-1 > 3^(-p_n).
```

TICKET-217 proved that this excludes every positive scaling of the reduced
convergent. Negating the sufficient integer condition yields the spike
necessity for any candidate that this argument cannot exclude.

The implementation never materializes astronomical powers when unnecessary.
It uses the exact implication

```text
4(q+q_next) < 2^p < 3^p
```

whenever the integer bit length proves the first inequality. The certified
continued fraction comes from rational upper and lower bounds for the positive
atanh series of both logarithms.

### Remaining gap

No theorem here bounds every future partial quotient of this logarithmic
ratio. A single exponentially large next denominator could evade the new
sufficient test. More importantly, the single-mountain word family excludes
neither multiple valuation runs nor nonperiodic divergence. The very large
finite lower bound must not be described as a Collatz proof.

## 3. Strong Goldbach: a centered residual-moment certificate

### Declared proposition

Let `A_i>=0` be representation counts on a finite block and let `M_i>0` be
any positive model. For every real `p>0`, define

```text
E_p = sum_i |A_i-M_i|^p,
m   = min_i M_i.
```

If

```text
E_p < m^p,
```

then every `A_i` is positive. The strict threshold is sharp over
nonnegative vectors.

For the finite audit, use the positive integer shape

```text
w(n) = round(10^6 n product_{odd prime l | n} (l-1)/(l-2))
```

and the rational least-squares scale

```text
M_i = (P/Q) w_i,
P = sum_i A_i w_i,
Q = sum_i w_i^2.
```

The certificate becomes the exact integer inequality

```text
sum_i |A_i Q-Pw_i|^p < (P min_i w_i)^p.
```

For `p=8`, this inequality holds on all five audited dyadic blocks beginning
at `128, 512, 2048, 8192, 32768`. For `p=4`, it fails on all five.

### Proof and exact audit

If some `A_j=0`, its residual alone is

```text
|A_j-M_j|^p = M_j^p >= m^p,
```

contradicting the strict inequality. If `j` is a minimum-model coordinate,
the vector with `A_j=0` and `A_i=M_i` elsewhere gives equality, proving that
`<` cannot be replaced by `<=` in the universal real-vector statement.
Multiplication by `Q^p` proves the integer form used by the audit.

Every prime flag, representation count, rounded model weight, residual, and
threshold comparison in the generated artifact uses exact integer or rational
arithmetic. The displayed minimum count is included only as an independent
finite cross-check.

### What changed and what did not

TICKET-217's uncentered second-moment support condition failed on all five
blocks. Centering at a positive arithmetic model and using the eighth residual
moment succeeds on exactly those blocks. This is a genuine finite certificate,
but the scale `P/Q` is fitted from the complete finite count vector. It is not
an independent asymptotic estimate.

To prove strong Goldbach by this route one would need an explicit cutoff and a
cofinal analytic estimate of the form

```text
sum_{X<=n<2X, n even} |R(n)Q_X-P_X w(n)|^8
  < (P_X min w)^8
```

without first enumerating every `R(n)`. That circle-method or dispersion input
is the next open lemma. The ticket neither proves that estimate nor removes
the known exceptional-set-to-empty-set gap.

## 4. Twin Prime: strict Abel surplus transfers to a count

### Declared proposition

For any sequence `0<=a_n<=1` supported on odd integers, define

```text
F(r) = sum_n a_n r^n,
T(Y) = sum_{n<=Y} a_n.
```

Let `R(r,Y)` be the coefficient-one odd geometric tail after `Y`. Then

```text
T(Y) >= F(r)-R(r,Y).
```

Set

```text
r_X = 1-1/X,
Y_X = floor((2 log log X+a)X)
```

for fixed `a`. If

```text
liminf F(r_X)/(X/log^2 X) >= A
```

with

```text
A > exp(-a)/2,
```

then

```text
liminf T(Y_X)/(X/log^2 X) >= A-exp(-a)/2 > 0.
```

For the twin-prime indicator this would imply infinitely many twin primes.

### Proof and sharpness

Split `F` at `Y`. The initial part is at most `T(Y)` because `r^n<=1`; the
tail is at most `R` because `a_n<=1`. Rearrangement proves the finite
inequality. TICKET-217 gives

```text
R(r_X,Y_X)/(X/log^2 X) -> exp(-a)/2.
```

Taking the liminf yields the quantitative conclusion. Since
`X/log^2 X` tends to infinity, a positive normalized lower bound forces
unboundedly many nonzero terms.

The strict constant is sharp for this transfer information. At any fixed
horizon, the logical sequence that is zero through `Y` and one at every later
odd index satisfies

```text
T(Y)=0, F(r)=R(r,Y).
```

Thus equality at the critical coefficient cannot imply a positive count from
this upper-envelope argument alone. This logical sequence is not claimed to
be a prime sequence.

### Finite diagnostic and remaining gap

At offset `a=0`, direct twin enumeration through the adaptive horizons for
`X=10^3,10^4,10^5,10^6` gives positive partial Abel surplus over the
coefficient-one tail. The normalized partial Abel values decrease from about
`1.64` to `1.48`, while the tail approaches `0.5`. These deterministic
double-precision rows are diagnostics, not interval certificates and not an
asymptotic lower bound.

The missing theorem is now a single strict statement:

```text
liminf F_twin(1-1/X)/(X/log^2 X) > 1/2.
```

The project has not proved it. In particular, the reduction does not overcome
the sieve parity barrier.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket218_adaptive_radius_spike_residual_surplus.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket218_adaptive_radius_spike_residual_surplus -v
```

Primary machine artifact:

```text
data/open-problem/ticket218-adaptive-radius-spike-residual-surplus.json
```

Per-problem artifacts are stored under `data/open-problem/{problem}/`.

## Final status

| Problem | New result | Resolution | Discarded path | Remaining gap | Next lemma |
| --- | --- | --- | --- | --- | --- |
| Riemann | adaptive radius certificate and signal phase transition | open | vanishing signal with fixed absolute precision | actual-zeta cofinal envelope below `exp(-tau)` | `ActualZetaScaleAdaptiveDefectEnvelopeBelowExpMinusTau` |
| Collatz | exponential next-denominator barrier; 49 upper convergents excluded | open | enormous direct cross-power construction | future exponential spikes, multi-run words, divergence | `EffectiveExponentialPartialQuotientBoundForCollatzLogRatio` |
| Goldbach | sharp residual-moment theorem; five exact `p=8` block certificates | open | uncentered second moment and non-strict threshold | cofinal arithmetic eighth-moment estimate | `CofinalGoldbachEighthResidualMomentBelowZeroCoordinateBarrier` |
| Twin Prime | sharp Abel-surplus-to-count transfer | open | equality at the critical coefficient | actual Abel liminf strictly above `1/2` | `ActualTwinAbelLiminfCoefficientGreaterThanOneHalf` |
