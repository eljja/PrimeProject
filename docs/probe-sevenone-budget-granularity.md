# TICKET-191: Probe Topology, Seven-One Cycles, and Exact Arithmetic Targets

## 1. Claim boundary

TICKET-191 proves four exact intermediate statements but resolves none of the
Riemann, Collatz, strong Goldbach, or Twin Prime conjectures. It finds no
counterexample to any conjecture. The only new infinite-family closure is the
complete accelerated Collatz cycle stratum with exactly seven valuations equal
to one and every other valuation equal to two.

| problem | exact new result | route rejected or corrected | next single lemma |
|---|---|---|---|
| Riemann | `GaussianRationalProbePromotionAndCoordinateTestNoGo` | coordinate tests and premature operator-norm promotion | `PoleNeutralWeilQuadraticValuesConvergeOnGaussianRationalCoreAndExtendContinuouslyToAdmissibleTestFunctions` |
| Collatz | `ExactlySevenValuationOnesOtherwiseTwoCycleExclusion` | unbounded enumeration without a product cutoff | `NoContractingValuationWordWithExactlyEightOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| Goldbach | `ExactPrimePowerBudgetPointwiseReductionAndLinearScaleNoGo` | treating a fixed positive linear lower bound as necessary | `BinaryVonMangoldtCorrelationExceedsExplicitPrimePowerBudgetForEveryLargeEvenTarget` |
| Twin Prime | `ArithmeticBlockGranularityEquivalenceAndLinearDensityNoGo` | treating positive linear density as equivalent to infinitude | `ShiftTwoCorrelationExceedsExactPrimePowerContaminationOnInfinitelyManyDyadicBlocks` |

Reproduce the artifact with:

```powershell
python scripts\ticket191_probe_sevenone_budget_granularity.py
python -m unittest tests.test_ticket191_probe_sevenone_budget_granularity -v
python scripts\verify_open_problem_structure.py
```

The machine-readable result is
`data/open-problem/ticket191-probe-sevenone-budget-granularity.json`. Every
attempt remains `open_not_proven` and the resolution count is `0 / 4`.

## 2. Riemann Hypothesis

### 2.1 Exact proposition

Let `q_N` be Hermitian quadratic forms on nested finite-support cores. Suppose
`q_N(x)` is Cauchy for every Gaussian-rational finite-support vector `x`. The
pointwise limits preserve the quadratic identities. Complex polarization,

```text
B(x,y) = 1/4 [q(x+y)-q(x-y)+i q(x+iy)-i q(x-iy)],
```

therefore defines compatible matrix entries and one Hermitian form on `c_00`.
If, on each fixed core,

```text
q_N(x) >= -epsilon_N ||x||^2,   epsilon_N -> 0,
```

then the limiting form is positive semidefinite.

Coordinate positivity alone is not enough. For rational `a>1`,

```text
A_a = [[1,-a],[-a,1]]
```

has `q(e_1)=q(e_2)=1`, but `q(1,1)=2-2a<0`; its least eigenvalue is `1-a`.
The generated artifact verifies this exact counterfamily and a rational-probe
Cauchy example using rational arithmetic.

### 2.2 What remains open

No convergence, vanishing negative floor, or continuity estimate is proved for
the actual pole-neutral Weil/screw-function quadratic forms. Scalar convergence
on a countable core would also need continuity in the admissible test-function
topology before it could support an RH-equivalent positivity statement. This
ticket is an abstract promotion theorem, not an RH proof.

Recent work on Weil's quadratic form via the screw function develops a related
operator-limit program but states the decisive operator conclusion as a
conjectural or numerical target, not as a proof of RH: [Suzuki 2026](https://arxiv.org/abs/2606.09096),
[numerical operator study 2026](https://arxiv.org/abs/2607.24830).

## 3. Collatz conjecture

### 3.1 Exact proposition and analytic range

For an accelerated odd cycle

```text
x_(i+1) = (3x_i+1)/2^v_i
```

with exactly seven `v_i=1` and all other `v_i=2`, the total valuation is
`2h-7` and the affine denominator is

```text
D = 2^(2h-7)-3^h.
```

It is positive from `h=17`. A nontrivial positive odd cycle cannot contain one,
so every cycle value is at least three. Multiplying around the cycle gives

```text
1 = product_i (3+1/x_i)/2^v_i <= 128(5/6)^h.
```

At `h=27`, the exact upper bound is

```text
7450580596923828125 / 7996018508417728512 < 1,
```

and decreases thereafter. Hence no such cycle exists for `h>=27`.

### 3.2 Exact finite closure

For the remaining contracting horizons `17<=h<=26`, the generator evaluates
the affine numerator and `B mod D` for every word:

```text
sum_(h=17)^26 binomial(h,7)
  = binomial(27,8)-binomial(17,8)
  = 2,195,765.
```

No divisibility hit occurs. Per-horizon SHA-256 transcripts certify deterministic
replay. Primitive and imprimitive words are both included.

This closes one periodic valuation stratum only. Eight-or-more-one strata,
valuations at least three, and aperiodic divergence remain open; it is not a
proof of the Collatz conjecture.

## 4. Strong Goldbach conjecture

### 4.1 Quantifier-matched reduction

Let `R_Lambda(N)` be the binary von Mangoldt correlation. With
`L=floor(log_2 N)`, define the explicit proper-prime-power budget

```text
B_pp(N) = 2 [floor(sqrt N)+(L-2)_+ floor(N^(1/3))] (log N)^2.
```

TICKET-189 proves that every convolution term involving at least one proper
prime power has total weight at most this budget. Therefore

```text
R_Lambda(N) > B_pp(N)
```

at an even target implies positive prime-prime mass and hence a Goldbach
representation at that target.

Furthermore,

```text
B_pp(N) <= 2(1+L)sqrt(N)(log N)^2 = o(N).
```

Thus a fixed positive linear lower bound is sufficient but is not necessary
for the prime-power-removal step. The exact pointwise budget is the weaker,
logically matched target.

### 4.2 Missing theorem

The ticket does not prove `R_Lambda(N)>B_pp(N)` for every sufficiently large
even `N`. That is the unresolved binary major/minor-arc cancellation problem;
finite data and exceptional-set estimates cannot supply the universal
quantifier. Helfgott's ternary theorem explicitly separates the tractable
three-prime problem from this binary obstacle: [Helfgott 2015](https://arxiv.org/abs/1501.05438).
Recent power-saving exceptional-set results likewise do not prove every-target
binary Goldbach: [Grimmelt and Teräväinen 2025](https://arxiv.org/abs/2508.16400).

## 5. Twin Prime conjecture

### 5.1 Exact block equivalence

On `[2^j,2^(j+1))`, subtract from the shift-two von Mangoldt correlation every
term involving a proper prime power. The exact remainder is

```text
b_j = sum_(2^j<=p<2^(j+1), p and p+2 prime) log p log(p+2).
```

Consequently `b_j>0` exactly when the block contains a twin-prime pair. If it
is positive, then

```text
b_j >= (j log 2)^2.
```

The Twin Prime conjecture is therefore equivalent to positivity of `b_j` for
infinitely many `j`, and also to unbounded cumulative exact excess.

### 5.2 Linear-density no-go

Positive linear cumulative density is stronger than infinitude. The formal
arithmetic-scale sequence

```text
b_j = (j log 2)^2  if j is a power of two,
b_j = 0            otherwise
```

has infinitely many positive blocks and unbounded cumulative mass, while its
cumulative mass through `J` is at most `O(J^2 log J)` and hence is `o(2^J)`.
This is a logical comparison sequence, not prime data.

No argument here proves actual positivity on infinitely many blocks. Bounded
gap results do not force exact gap two; see [Zhang 2014](https://annals.math.princeton.edu/2014/179-3/p07)
and [Maynard 2015](https://annals.math.princeton.edu/2015/181-1/p07).

## 6. Conclusion

The durable TICKET-191 advance is target minimization without claim inflation.
The RH track identifies a countable scalar-probe gateway, Collatz closes one
new infinite valuation stratum, Goldbach reduces the required scale to an
explicit sublinear pointwise budget, and Twin Prime identifies exact block
positivity as the conjecture-equivalent target. The remaining obligations are
explicit, infinite, and unproved.
