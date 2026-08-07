# TICKET-190: Cauchy Cores, Six-One Cycles, and Quantifier Transfer

## 1. Claim boundary

TICKET-190 continues the four open nodes of TICKET-189. It proves one new
infinite Collatz cycle-stratum exclusion and three exact topology or quantifier
boundaries. It proves none of the Riemann, Collatz, strong Goldbach, or Twin
Prime conjectures and finds no counterexample to any of them.

| problem | exact TICKET-190 result | discarded or corrected route | next single lemma |
|---|---|---|---|
| Riemann | `DirectCoreCauchyPromotionAndAbsoluteSummabilityNoGo` | treat absolute summability of adjacent core drift as necessary | `PoleNeutralGuinandWeilFixedCoresHaveCertifiedCauchyModulusAndVanishingNegativeFloor` |
| Collatz | `ExactlySixValuationOnesOtherwiseTwoCycleExclusion` | extrapolate finite six-one enumeration to every horizon | `NoContractingValuationWordWithExactlySevenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| Goldbach | `DensityOneAndAverageMassDoNotImplyEveryTargetGoldbach` | promote density-one or average positivity to every even target | `ExplicitMajorArcMainMinusMinorArcErrorExceedsSublinearPrimePowerBudgetForEveryLargeEvenTarget` |
| Twin Prime | `CumulativeDyadicLinearTransferAndSparseMassNoGo` | treat a positive linear block bound as necessary for infinitude | `CumulativeShiftTwoCorrelationMinusExactPrimePowerContaminationHasUnboundedCertifiedLowerEnvelope` |

Reproduce the results with:

```powershell
python scripts\ticket190_cauchy_sixone_quantifier_transfer.py
python -m unittest tests.test_ticket190_cauchy_sixone_quantifier_transfer -v
```

The machine artifact is
`data/open-problem/ticket190-cauchy-sixone-quantifier-transfer.json`. All four
conjecture statuses remain `open_not_proven`.

## 2. Riemann Hypothesis

### 2.1 Declared proposition

Compatible Hermitian fixed cores with a direct Cauchy modulus define one
Hermitian form on finite-support sequences. A vanishing negative eigenvalue
floor makes the form positive semidefinite. Absolute summability of adjacent
core drifts is sufficient, but it is not necessary.

The scalar family

```text
A_N = 2 + sum_(k=1)^N (-1)^(k+1)/k
```

has the direct tail modulus

```text
|A_M-A_N| <= 1/(N+1),  M>N,
```

while its adjacent drift norms are `1/(N+1)` and have divergent total sum.

If compatible positive core forms `Q_m` satisfy

```text
sup_m ||Q_m|| <= M,
```

their form extends uniquely to a bounded positive self-adjoint operator on
`l_2`. Uniform boundedness is essential for this operator conclusion:
`Q_m=diag(1,2,...,m)` is compatible and positive on `c_00`, but no bounded
operator on `l_2` can restrict to all these cores.

### 2.2 Proof

A direct modulus makes each finite-dimensional core Cauchy. Compatibility of
the finite sections passes to their limits, so vectors with finite support see
one well-defined Hermitian form. The alternating-series remainder theorem gives
the stated modulus even though the absolute drift series is harmonic.

Under the uniform bound, the form obeys

```text
|Q(x,y)| <= M ||x||_2 ||y||_2
```

on the dense subspace `c_00`. Continuous extension and Riesz representation
produce the bounded operator. For the counterfamily, any extension would have
`||Qe_m||=m` for all `m`, contradicting boundedness.

### 2.3 Remaining gap

This corrects the topology of the TICKET-189 target. It does not prove a direct
Cauchy modulus or a vanishing negative floor for the actual pole-neutral
Guinand-Weil cores. It therefore does not prove RH. The next route should allow
oscillatory cancellation instead of requiring an absolute drift majorant.

## 3. Collatz conjecture

### 3.1 Declared proposition

No positive accelerated Collatz cycle has exactly six valuations equal to one
and every remaining valuation equal to two. Primitive and imprimitive periods
are both excluded.

### 3.2 All-horizon product argument

Let

```text
x_(i+1) = (3x_i+1)/2^v_i,
```

with exactly six `v_i=1` and all other `v_i=2`. The total valuation is
`2h-6`, and contraction starts at `h=15`.

The orbit cannot contain `x_i=1`: an odd accelerated orbit through one is the
trivial all-two fixed cycle, incompatible with six valuation-one entries.
Thus every cycle value is at least three. Multiplying one period gives

```text
1 = product_i (3+1/x_i)/2^v_i
  <= (10/3)^h / 2^(2h-6)
  = 64(5/6)^h.
```

At `h=23`, the exact upper bound is

```text
11920928955078125 / 12339534735212544 < 1,
```

and it decreases thereafter. This is impossible, so every `h>=23` is excluded.

### 3.3 Finite exception closure

The remaining contracting horizons are checked with exact integer arithmetic:

```text
sum_(h=15)^22 binomial(h,6) = 238722.
```

For each valuation word the code computes the affine numerator `B`, denominator
`D=2^(2h-6)-3^h`, and remainder `B mod D`. No divisibility hit occurs.
Per-horizon SHA-256 transcripts make this finite closure reproducible.

### 3.4 Limitation

This closes one periodic valuation stratum only. Words with seven or more ones,
any valuation at least three, and divergent aperiodic natural-number orbits
remain untreated. The Collatz conjecture remains open.

## 4. Strong Goldbach conjecture

### 4.1 Declared no-go theorem

Density-one positivity and an asymptotically complete average linear mass do
not imply positivity at every even target. On even `N>=4`, define

```text
F(N) = 0  if N is a power of two,
F(N) = N  otherwise.
```

Then `F` has infinitely many exact zero targets. Nevertheless, up to `X`, the
number of holes is `O(log X)=o(X)`, and their total missing mass is

```text
sum_(2^k<=X) 2^k < 2X = o(X^2).
```

Thus the cumulative mass of `F` has the same quadratic leading term as the
fully positive model, with relative average error tending to zero.

### 4.2 Meaning and limitation

This is a logical countermodel, not a model of the prime correlation. It proves
that exceptional-set density and average circle-method estimates cannot by
themselves close strong Goldbach's universal quantifier. The TICKET-189
sublinear prime-power budget still has to be beaten pointwise for every
sufficiently large even target, followed by exact finite verification.

## 5. Twin Prime conjecture

### 5.1 Declared transfer theorem

Let `b_j>=0` be dyadic block masses and

```text
W_J = sum_(j<J) b_j.
```

Then

```text
limsup_(J->infinity) W_J/2^J > 0
```

if and only if there is a fixed `c>0` such that `b_j>=c2^j` for infinitely many
`j`. For the arithmetic application, TICKET-189 gives the exact block identity

```text
b_j = shift-two von Mangoldt mass - proper-prime-power contamination
    = weighted twin-prime mass.
```

Therefore a positive linear cumulative excess transfers exactly to infinitely
many positive linear dyadic blocks.

### 5.2 Proof and no-go

If `b_j<c2^j` eventually, geometric summation gives
`limsup W_J/2^J<=c`. Choosing `c` below a positive limsup proves one direction.
Conversely, `b_j>=c2^j` gives `W_(j+1)/2^(j+1)>=c/2` along the same subsequence.

But linear growth is not necessary for infinitude. The exact model `b_j=1`
has unbounded cumulative mass `W_J=J`, while both normalized block and
cumulative masses tend to zero. Hence the positive-linear TICKET-189 target is
a strong sufficient route, not an equivalent formulation of the Twin Prime
conjecture.

### 5.3 Remaining gap

After exact prime-power subtraction, unbounded cumulative weighted twin mass is
equivalent to infinitely many twin primes. TICKET-190 does not prove that
unboundedness. The next lemma must provide a certified unbounded lower envelope
for the cumulative exact excess; a positive linear limsup remains an optional,
stronger analytic target.

## 6. Proof-status conclusion

TICKET-190 proves four exact statements. The Collatz track closes the complete
six-one/rest-two periodic stratum. The RH track removes an unnecessarily strong
absolute-summability requirement, Goldbach receives an exact sparse-hole
quantifier no-go, and Twin Prime receives a cumulative-to-dyadic transfer with
a strict separation between infinitude and linear density. Resolution remains
`0 / 4`.
