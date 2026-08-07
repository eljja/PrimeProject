# TICKET-192: Uniform Extension, Eight-One Cycles, and Weighted Envelopes

## 1. Claim boundary

TICKET-192 proves four intermediate theorems and resolves none of the Riemann,
Collatz, strong Goldbach, or Twin Prime conjectures. It finds no counterexample
to a parent conjecture. Its one new infinite-family closure excludes every
accelerated Collatz cycle whose valuation word has exactly eight entries equal
to one and all remaining entries equal to two.

| problem | exact result proved here | route rejected or demoted | one next lemma |
|---|---|---|---|
| Riemann | `UniformBoundedCoreExtensionAndPointwiseCauchyNoGo` | pointwise dense-core convergence without a uniform continuity bound | `PoleNeutralWeilQuadraticValuesConvergeOnGaussianRationalCoreWithUniformAdmissibleNormBound` |
| Collatz | `ExactlyEightValuationOnesOtherwiseTwoCycleExclusion` | duplicate cyclic enumeration and enumeration beyond the product cutoff | `NoContractingValuationWordWithExactlyNineOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| Goldbach | `WeightedPrimePowerEnvelopeAndFactorTwoBudgetReduction` | an unweighted count budget as the primary sufficient target | `BinaryVonMangoldtCorrelationExceedsWeightedPrimePowerEnvelopeForEveryLargeEvenTarget` |
| Twin Prime | `LocalTwoSidedWeightedEnvelopeBridge` | a global count when only two local translated intervals can contaminate the block | `ShiftTwoCorrelationExceedsLocalWeightedPrimePowerEnvelopeOnInfinitelyManyDyadicBlocks` |

Reproduce the result with:

```powershell
D:\python\anaconda3\python.exe scripts\ticket192_uniform_eightone_weighted_envelope.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket192_uniform_eightone_weighted_envelope -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

The global artifact is
`data/open-problem/ticket192-uniform-eightone-weighted-envelope.json`.
Every attempt has status `open_not_proven`; the resolution count is `0 / 4`.

## 2. Riemann Hypothesis

### 2.1 Declared proposition

Let `D` be dense in a complex Hilbert space `H`, and let `q` be a Hermitian
quadratic form on `D`. Then `q` extends uniquely to a bounded Hermitian form on
`H` if and only if there is a finite `C` such that

```text
|q(x)| <= C ||x||^2                    (x in D).
```

If `q>=0` on `D`, its extension is positive. Pointwise Cauchy convergence of
finite sections on a countable dense core is not sufficient for this extension.

### 2.2 Proof and exact no-go

Necessity is immediate by restricting a bounded extension. Conversely, complex
polarization gives a sesquilinear form `B`. Applying the quadratic bound to the
four polarization terms and rescaling one argument gives

```text
|B(x,y)| <= 2 C ||x|| ||y||.
```

Thus `B` extends uniquely by density. Continuity transfers positivity from `D`
to `H`.

For the no-go, take `H=l^2`, `D=c_00`, and

```text
q_N(x) = sum_(k<=N) k |x_k|^2.
```

For every `x in c_00`, `q_N(x)` is eventually constant, and every `q_N` is
positive. Nevertheless the limit satisfies `q(e_k)=k`; no finite uniform bound
exists, so there is no bounded extension to all of `l^2`. The generated rows
replay the growing norms `2,4,8,16,32,64`.

### 2.3 Remaining gap

This theorem identifies the missing topology but supplies no bound for the
actual pole-neutral Weil quadratic form. The next lemma must prove both scalar
convergence on the Gaussian-rational core and one uniform admissible-norm bound.
Recent screw-function work formulates the decisive limiting-operator statement
as conjectural rather than an RH proof: [Suzuki 2026](https://arxiv.org/abs/2606.09096).

## 3. Collatz conjecture

### 3.1 Declared proposition

No positive accelerated Collatz cycle has exactly eight valuations `v_i=1`
and every remaining valuation `v_i=2`, including primitive and imprimitive
periods.

### 3.2 Complete range split

For a word of length `h`, its total valuation is `2h-8`, and the cycle equation
has denominator

```text
D = 2^(2h-8) - 3^h.
```

For `h<20`, `D<=0`, so no positive cycle can occur. For `20<=h<=30`, rotate a
word so one valuation-one position is first. Divisibility is invariant under
rotation because

```text
2^v B_shift = 3B + D,
```

and `D` is odd. It is therefore enough to inspect

```text
sum_(h=20)^30 C(h-1,7)
  = C(30,8)-C(19,8)
  = 5,777,343
```

rotation-normalized words. Exact integer computation finds zero `D|B` hits;
each horizon has a deterministic SHA-256 remainder transcript.

A nontrivial positive odd cycle in this stratum cannot contain one, so all its
values are at least three. Multiplication around the cycle gives

```text
1 <= 256 (5/6)^h.
```

At `h=31`, the right side is exactly `256*5^31/6^31<1` and decreases with `h`.
This contradicts every `h>=31` cycle and completes the full stratum.

### 3.3 Remaining gap

This does not control valuation words with nine or more ones, any valuation at
least three, or aperiodic divergent trajectories. Recent parity-vector work
also explicitly makes no claim to prove Collatz: [Niu 2026](https://arxiv.org/abs/2605.13886).

## 4. Strong Goldbach conjecture

### 4.1 Declared proposition

Let

```text
W_pp(X) = sum_(p^k<=X, k>=2) log p
```

and let `E_pp(N)` be the part of the binary von Mangoldt correlation containing
at least one proper prime power. Then

```text
E_pp(N) <= 2 log(N) W_pp(N).
```

If `A(N)` counts proper prime powers at most `N`, then

```text
W_pp(N) <= A(N) log(N)/2,
E_pp(N) <= A(N)(log N)^2.
```

The latter removes a factor two from the corresponding TICKET-191 count-based
sufficient budget.

### 4.2 Proof and finite diagnostic

Charge each contaminated ordered pair to a proper prime power in its left or
right coordinate. The partner contributes at most `log N`. If `q=p^k` with
`k>=2`, then `log p=log(q)/k<=log(N)/2`, proving both inequalities.

Therefore

```text
R_Lambda(N) > 2 log(N) W_pp(N)
```

forces positive prime-prime mass and a Goldbach representation. Exact finite
decompositions at eight targets from `64` through `1,048,576` all exceed the
new envelope. This is a replay diagnostic only, not a universal theorem.

### 4.3 Remaining gap

No proof establishes the displayed strict inequality for every sufficiently
large even `N`. Exceptional-set progress does not provide this universal binary
quantifier; see [Grimmelt and Teravainen 2025](https://arxiv.org/abs/2508.16400).

## 5. Twin Prime conjecture

### 5.1 Declared proposition

On a dyadic block `[X,2X)`, let `S_2(X)` be the shift-two von Mangoldt
correlation. Its proper-prime-power contamination is at most

```text
U_2(X) = log(2X+2) [
  W_pp([X,2X)) + W_pp([X+2,2X+2))
].
```

Hence `S_2(X)>U_2(X)` forces a twin-prime pair in that block. The local weighted
envelope also removes at least the same factor two from the earlier global
count envelope.

### 5.2 Proof and finite diagnostic

Every contaminated term has `n` or `n+2` equal to a proper prime power. Charge
it to the corresponding one of the two displayed intervals; the other factor
is at most `log(2X+2)`. This proves the envelope. Subtracting it from the full
correlation leaves positive prime-prime mass.

The exact finite replay covers `j=4,...,19` and all 16 blocks satisfy the
sufficient inequality. These are finite blocks containing known twin primes;
the computation has no force at unbounded scales.

### 5.3 Remaining gap

The Twin Prime conjecture would follow if the sufficient inequality held on
infinitely many unbounded dyadic blocks. No such estimate is proved here.
Bounded-gap theorems do not force gap two: [Zhang 2014](https://annals.math.princeton.edu/2014/179-3/p07),
[Maynard 2015](https://annals.math.princeton.edu/2015/181-1/p07).

## 6. Cross-problem conclusion

The common object introduced in the two prime-correlation tracks is the
weighted proper-prime-power mass `W_pp`. It preserves the actual von Mangoldt
weight discarded by count-only budgets and yields stricter local targets. The
common obstruction across all four tracks is still an infinite uniformity
statement: a form bound, a larger valuation stratum, every-target additive
excess, or infinitely-many-block shift excess. None is inferred from finite
data.
