# TICKET-188: Common Forms, Four-One Cycles, Prime-Power Contamination, and Dyadic Oracles

## 1. Claim boundary

TICKET-188 continues the four open nodes of TICKET-187. It proves one new
infinite Collatz cycle-stratum exclusion and three exact promotion or information
boundaries. It proves none of the Riemann, Collatz, strong Goldbach, or Twin Prime
conjectures, and it reports no counterexample to any of them.

| problem | exact TICKET-188 result | discarded or corrected route | next single lemma |
|---|---|---|---|
| Riemann | `CommonFormDefectPromotionAndMovingDirectionNoGo` | promote vanishing finite-matrix defect without exact nesting or convergence to one form | `PoleNeutralGuinandWeilMatricesConvergeToOneCommonFormWithCertifiedVanishingOperatorError` |
| Collatz | `ExactlyFourValuationOnesOtherwiseTwoCycleExclusion` | replace all remaining horizons by bounded enumeration | `NoContractingValuationWordWithExactlyFiveOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| Goldbach | `VonMangoldtPrimePowerContaminationBridge` | identify the full von Mangoldt convolution with prime-prime mass | `ExplicitBinaryGoldbachVonMangoldtLowerBoundDominatesPrimePowerContaminationForEveryLargeEvenTarget` |
| Twin Prime | `SubFourTwinIntervalExactCountOracleAndDyadicEquivalence` | treat a uniform interval width below four as a weak approximation target | `IndependentTypeIITwinProjectorLowerEndpointIsPositiveOnInfinitelyManyDyadicBlocks` |

Reproduce the project-owned results with:

```powershell
D:\python\anaconda3\python.exe scripts\ticket188_nested_fourone_primepower_dyadic.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket188_nested_fourone_primepower_dyadic -v
```

The principal machine artifact is
`data/open-problem/ticket188-nested-fourone-primepower-dyadic.json`. Every
conjecture status is `open_not_proven`.

## 2. Riemann Hypothesis

### 2.1 Declared proposition

Let `A_N` be exact nested principal restrictions of one Hermitian form and define

```text
delta_N = max(0, -lambda_min(A_N)).
```

Then `delta_N` is nondecreasing. If it tends to zero on any cofinal subsequence,
it is identically zero, so the underlying form is nonnegative on the algebraic
union of the finite sections.

There is also an approximate version. Suppose one fixed form `Q` satisfies, on
every fixed finite-support vector `f`,

```text
|Q(f) - <A_N f,f>| <= epsilon_N ||f||^2,
lambda_min(A_N) >= -eta_N,
epsilon_N + eta_N -> 0.
```

Then `Q(f)>=0` for every such `f`.

### 2.2 Proof

The Rayleigh-quotient domain for `A_N` embeds into that of `A_(N+1)`. Therefore
Cauchy interlacing gives

```text
lambda_min(A_(N+1)) <= lambda_min(A_N),
delta_(N+1) >= delta_N.
```

A nonnegative nondecreasing sequence with a cofinal subsequence converging to
zero must be zero at every index. For the approximate statement, fix `f`, take
`N` beyond its support, and pass to the limit in

```text
Q(f) >= -(epsilon_N + eta_N)||f||^2.
```

### 2.3 Exact no-go

The matrices

```text
A_N = diag(1,...,1,-1/N)
```

are indefinite at every dimension but have `delta_N=1/N -> 0`. Their negative
coordinate moves with `N`; adjacent matrices do not agree on their overlap.
Thus defect decay without exact nesting or certified convergence to one common
form is insufficient.

### 2.4 Remaining gap

PrimeProject has not proved that the cutoff-dependent pole-neutral
Guinand-Weil matrices are restrictions or certified approximations of one common
form. It has also not produced a cofinal family of independently verified interval
LDL certificates. This is the arithmetic and analytic gap, not an eigenvalue-plot
gap.

This distinction is consistent with Suzuki's operator/screw-function framework
and its still-conjectural limiting operator, and with later numerical realization
work that explicitly does not claim RH:
[Suzuki 2026](https://arxiv.org/abs/2606.09096),
[Kim et al. 2026](https://arxiv.org/abs/2607.24830).

## 3. Collatz conjecture

### 3.1 Declared proposition

No positive accelerated Collatz cycle has exactly four valuations equal to one
and every remaining valuation equal to two. Primitive and imprimitive words are
both excluded.

### 3.2 Exact cycle arithmetic

After cyclic rotation, write the four gaps as `a,b,c,d>=1`, with `d` largest and
`h=a+b+c+d`. For the accelerated map, the cycle denominator and ordered affine
numerator are

```text
D = 4^h/16 - 3^h,

B = 4^h/16 - 3^(h-1)
    + 4^a 3^(h-a-1)
    + 2*4^(a+b-1) 3^(c+d-1)
    + 4^(a+b+c-1) 3^(d-1).
```

The exact cycle condition requires `D | B`. Contraction starts at `h=10`.
Moreover `B>D`, and both `B` and `D` are odd.

### 3.3 All-horizon bound

Put `u=3/4`. The inequality `B<3D` follows from

```text
(16/3)u^(h-a) + (8/3)u^(c+d) + (4/3)u^d + (128/3)u^h < 2.
```

Since `d` is largest,

```text
d >= ceil(h/4),
c+d >= ceil(h/4)+1,
h-a >= ceil((h+2)/2).
```

The resulting all-word majorant is nonincreasing and at `h=16` equals

```text
63175275 / 33554432 < 2.
```

Thus `1<B/D<3` for every `h>=16`. If `B/D` were integral, oddness would force it
to be an odd integer strictly between one and three, which is impossible.

### 3.4 Finite closure and limitation

Exact enumeration checks every one of

```text
sum_{h=10}^{15} binomial(h,4) = 4116
```

remaining words and finds zero divisibility hits. The transcript hash for each
horizon is stored in the machine artifact. This proves an infinite periodic
stratum, but says nothing about words with five or more ones, valuations at least
three, or aperiodic divergence. Recent 2-adic work also illustrates why local
cycle equations alone do not isolate positive integer cycles:
[Dhiman-Pandey 2026](https://arxiv.org/abs/2601.12772).

## 4. Strong Goldbach conjecture

### 4.1 Declared proposition

For even `N`, split the binary von Mangoldt convolution as

```text
R_Lambda(N) = sum_{m=2}^{N-2} Lambda(m)Lambda(N-m)
            = P_Lambda(N) + E_pp(N),
```

where `P_Lambda` contains terms in which both endpoints are primes and `E_pp`
contains terms with at least one proper prime power. If `A(N)` is the number of
proper prime powers at most `N`, then

```text
0 <= E_pp(N) <= 2 A(N) (log N)^2.
```

Consequently, a rigorous bound

```text
R_Lambda(N) > 2 A(N) (log N)^2
```

forces `P_Lambda(N)>0` and therefore a Goldbach representation.

### 4.2 Proof and corrected route

Partition the nonzero convolution terms by the exponents of their prime-power
endpoints. A contaminated ordered pair has a proper prime power in its left or
right endpoint. Each endpoint position supplies at most `A(N)` choices, and each
weight is at most `(log N)^2`. This proves the bound.

The equality `R_Lambda=P_Lambda` is false: at `N=18`, the term `9+9` contributes
`(log 3)^2` to `E_pp`; `2+16` and `16+2` also contribute. A positive total
weighted convolution cannot simply be relabeled prime-prime mass without the
subtraction.

### 4.3 Remaining gap

The theorem supplies a sufficient threshold but no every-target lower bound for
`R_Lambda`. The finite rows through `N=100000` only replay the exact support
decomposition. Current exceptional-set work gives an explicit major-arc formula,
not the missing universal minor-arc/error domination:
[Grimmelt-Bhowmik 2026](https://arxiv.org/abs/2607.27282). The treatment of
von Mangoldt weights and prime-power terms follows the standard circle-method
distinction used, for example, in
[Helfgott's ternary Goldbach monograph](https://arxiv.org/abs/1501.05438).

## 5. Twin Prime conjecture

### 5.1 Declared proposition

Let `C_j` count twin-prime starts in `[2^j,2^(j+1))` and let
`Delta_j=4C_j`. If a sound interval `[L_j,U_j]` contains `Delta_j` and has
width strictly below four, it contains exactly one point of `4 Z_>=0` and hence
recovers `C_j` exactly. Furthermore,

```text
L_j > 0  iff  C_j > 0.
```

Width four is sharp because `[0,4]` is compatible with both `C_j=0` and `C_j=1`.

### 5.2 Dyadic equivalence

Every twin belongs to exactly one dyadic block, and finitely many bounded blocks
contain only finitely many integers. Therefore the Twin Prime conjecture is
equivalent to occupied dyadic blocks occurring infinitely often. Under sound
intervals this is equivalent to `L_j>0` infinitely often.

This also identifies an overstrong route: uniformly constructing intervals of
width below four would recover every block count exactly. It is not merely a
coarse relaxation of the conjecture. A one-sided positive lower endpoint on an
infinite subsequence is the weaker, relevant target.

### 5.3 Computation and limitation

The finite ledger covers 16 predeclared blocks, `j=4,...,19`. Its width-`7/2`
intervals are centered on direct counts, so they test only the exact rounding
logic and are not independent analytic certificates. Prime-producing sieve
methods require genuine Type I and Type II information; the interval theorem
does not supply it:
[Ford-Maynard 2024](https://arxiv.org/abs/2407.14368).

## 6. Proof-status conclusion

TICKET-188 proves four exact statements. Only the Collatz statement closes a new
infinite arithmetic family. The other three results prevent an invalid promotion
and specify a sharper next lemma. The resolution count remains `0 / 4`.
