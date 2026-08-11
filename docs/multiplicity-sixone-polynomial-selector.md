# TICKET-213: Multiplicity, Six-One Cycles, Polynomial Majorants, and Gap Selectors

> **Research status:** `open_not_proven` for all four parent conjectures.<br>
> **Machine artifact:**
> [`ticket213-multiplicity-sixone-polynomial-selector.json`](../data/open-problem/ticket213-multiplicity-sixone-polynomial-selector.json)<br>
> **Reproducer:**
> [`ticket213_multiplicity_sixone_polynomial_selector.py`](../scripts/ticket213_multiplicity_sixone_polynomial_selector.py)

TICKET-213 audits the logical target left by TICKET-212 before adding new
computation. It proves four exact partial or no-go theorems. It does not prove
or refute the Riemann Hypothesis, Collatz conjecture, strong Goldbach
conjecture, or Twin Prime conjecture.

| Problem | Exact new result | Discarded route | Remaining gap | Next single lemma |
|---|---|---|---|---|
| Riemann | `MultiplicityAwareCriticalLineCountEquivalenceAndSignChangeNoGo` | Treat odd-multiplicity sign changes as an RH-equivalent count without simplicity | An all-height multiplicity equality for actual zeta zeros | `UniformMultiplicityAwareCriticalLineDefectStrictlyBelowTwo` |
| Collatz | `CompleteSixValuationOneCycleStratumExclusion` | Every positive cycle word with exactly six valuation-one entries | Seven-or-more-one cycles and nonperiodic divergence | `UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastSeven` |
| Goldbach | `FixedDegreePolynomialWitnessMajorantNoGo` | Every fixed polynomial in the witness count as a pointwise exception majorant | A scale-growing or nonpolynomial uniformly subunit tail bound | `ScaleGrowingWitnessResummationWithUniformDyadicTailBelowOne` |
| Twin Prime | `NonnegativeGapFunctionalIsolationIffSupportAtTwo` | Every nonnegative aggregate contaminated by another gap | A signed arithmetic selector with a controlled remainder | `GapTwoSelectiveSignedFunctionalWithUniformArithmeticRemainder` |

## 1. Riemann Hypothesis

### Declared proposition

Let `R` be an upper-half critical-strip rectangle with no boundary zeros and
invariant under

```text
rho -> 1 - conjugate(rho).
```

Let `N` be the total zero count with multiplicity and let `M` be the total
multiplicity of zeros on the critical line. Then

```text
N - M = 2 * (off-line multiplicity on one side of the line).
```

Therefore `N-M` is a nonnegative even integer, and

```text
N-M < 2  iff  every zero in R lies on the critical line.
```

This is the exact finite-rectangle RH certificate.

### Why the TICKET-212 sign target was too strong

Let `O` count distinct odd-multiplicity critical-line zeros, the information
available from complete Hardy-function sign changes. Then

```text
N-O = (N-M) + sum_line(m - (m mod 2)).
```

Thus `N-O<2` is equivalent to all zeros being on the line **and simple**. A
double critical-line zero has `N-M=0` but `N-O=2`; it is compatible with RH but
rejected by the sign-change certificate. TICKET-213 therefore discards the
claim that the sign-change defect is a minimal RH-equivalent target.

### Reproducible computation and limit

The generator checks exact finite multiplicity configurations containing
simple, double, and triple line zeros and simple or multiple off-line pairs.
The table is a finite algebraic regression test, not a zeta-zero computation.
No all-height bound for the actual zeta function is proved.

### Proof DAG

```text
EvenCriticalLineDefectSubTwoSaturationCertificate
  -> MultiplicityAwareCriticalLineCountEquivalenceAndSignChangeNoGo
       -> [discard] SignChangeSubTwoIsExactlyRHEquivalent
       -> UniformMultiplicityAwareCriticalLineDefectStrictlyBelowTwo
            -> Riemann Hypothesis
```

## 2. Collatz Conjecture

### Declared proposition

No nontrivial positive accelerated Collatz cycle contains exactly six
valuation entries equal to one while all remaining entries are at least two.
Together with TICKET-210, a hypothetical nontrivial positive cycle must contain
at least seven valuation-one entries.

### Analytic finite reduction

Rotate a hypothetical cycle to its least odd element `m>=3`. The outgoing
valuation is one and the incoming valuation is at least two. For a length-`h`
cycle with valuation sum `A` and exactly `k` ones,

```text
A >= 2h-k,
2^A = product_i(3 + 1/x_i) <= (10/3)^h,
(6/5)^h <= 2^k.
```

For `k=6`, this proves `h<=22`. The same product bound gives a finite upper
bound on `A` at every remaining length.

### Exact enumeration

The generator fixes the forced first and last valuations, enumerates every
choice of the other five ones, and enumerates every weak composition of the
remaining valuation excess. For each word it computes

```text
C = sum_j 3^(h-1-j) 2^(a_1+...+a_j),
D = 2^A - 3^h,
x = C/D.
```

All `376,788` admissible candidates at lengths `7..22` are tested with exact
integer arithmetic. No positive `D` divides `C`. Per-length SHA-256 transcript
hashes make the enumeration independently replayable.

This is a complete proof only for the exactly-six-one periodic stratum. It
says nothing about cycles with at least seven ones or nonperiodic divergence.

### Proof DAG

```text
TwoAdicGhostUniversalityAndOddDivisibilityCorrection
  -> CompleteSixValuationOneCycleStratumExclusion
       -> [discard] SixValuationOnePositiveCycleStratum
       -> UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastSeven
            -> Collatz Conjecture (periodic branch only; divergence is separate)
```

## 3. Strong Goldbach Conjecture

### Declared proposition

Let `A(N)` be the number of unordered Goldbach witnesses of an even target.
There is no fixed real polynomial `P` satisfying

```text
P(0) >= 1,
0 <= P(A(N)) < 1 for every represented even N.
```

TICKET-212 proved that positive attained values of `A(N)` are unbounded using
the prime number theorem and an exact pair-count pigeonhole argument. Along an
unbounded positive sequence, every nonconstant polynomial tends to positive or
negative infinity according to its leading coefficient. A constant polynomial
cannot be at least one at zero and strictly below one on represented targets.

### Finite interpolation lower bound

Any polynomial that equals the exact zero indicator on `A=0,1,...,M` has `M`
distinct roots and nonzero value at zero, so its degree is at least `M`. The
bound is attained by

```text
Q_M(A) = product_(j=1)^M (1 - A/j).
```

The exact rational audit verifies this identity for `M=1..12`, including the
first out-of-range value. Hence fixed-degree Bonferroni failure is not an
artifact of the binomial basis: every fixed polynomial has the same global
pointwise obstruction.

This no-go theorem does not reject scale-dependent, rational, exponential, or
other analytic resummations and supplies no Goldbach tail theorem.

### Proof DAG

```text
FullWitnessProductIdentityAndFixedBonferroniNoGo
  -> FixedDegreePolynomialWitnessMajorantNoGo
       -> [discard] FixedPolynomialCanMajorizeAllGoldbachExceptionsBelowOne
       -> ScaleGrowingWitnessResummationWithUniformDyadicTailBelowOne
            -> Strong Goldbach Conjecture
```

## 4. Twin Prime Conjecture

### Declared proposition

For a finite gap set `H` containing two, let `w_h>=0` and

```text
L_w(t) = sum_(h in H) w_h t_h,  t_h>=0.
```

Then

```text
for every t>=0, L_w(t)>0 iff t_2>0
```

holds exactly when `w_2>0` and every `w_h` for `h!=2` is zero.

The forward direction is immediate for a pure gap-two weight. Conversely,
testing the nonnegative cone's extreme ray `e_2` forces `w_2>0`, while testing
each `e_g`, `g!=2`, forces `w_g=0`. Any positive contamination by another gap
therefore destroys universal gap-two isolation, even if the weight is tiny.

The rational audit tests pure, uniform, suppressed-contamination, and
gap-two-missing weight vectors on every basis ray. This is an abstract exact
cone theorem, not a lower bound for primes. Signed arithmetic selectors remain
possible only if their negative contributions and remainders are controlled.

### Proof DAG

```text
DyadicGapTwoEquivalenceAndFiniteGapAggregateNoGo
  -> NonnegativeGapFunctionalIsolationIffSupportAtTwo
       -> [discard] ContaminatedNonnegativeWeightsCanSelectGapTwo
       -> GapTwoSelectiveSignedFunctionalWithUniformArithmeticRemainder
            -> Twin Prime Conjecture
```

## Reproduction

```powershell
python scripts/ticket213_multiplicity_sixone_polynomial_selector.py
python -m unittest tests.test_ticket213_multiplicity_sixone_polynomial_selector -v
```

A successful run writes the integrated audit plus one standalone artifact per
problem and reports:

```text
exact_partial_theorem_count = 4
conjecture_resolution_count = 0
total_failure_count = 0
```

## Literature boundary

- Platt and Trudgian's [finite-height RH verification](https://arxiv.org/abs/2004.09765)
  is imported context; PrimeProject performs no new zeta interval verification.
- The Collatz proof uses the standard accelerated cycle equation and the
  project's earlier exact primitive-word reductions; it makes no claim about
  the nonperiodic branch.
- The published [Goldbach verification through `4*10^18`](https://doi.org/10.1090/S0025-5718-2013-02787-1)
  is much stronger than this project's finite diagnostics but remains finite.
- Maynard's [bounded-gap theorem](https://doi.org/10.4007/annals.2015.181.1.7)
  does not isolate exact gap two.

## Claim boundary

TICKET-213 advances theorem selection and closes one additional finite Collatz
cycle stratum. It also proves three broader logical no-go or equivalence
theorems. None supplies the missing infinite arithmetic estimate required by
the four parent conjectures, and none is presented as their solution.
