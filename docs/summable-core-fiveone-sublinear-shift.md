# TICKET-189: Summable Cores, Five-One Cycles, and Prime-Power Subtraction

## 1. Claim boundary

TICKET-189 continues the four open nodes of TICKET-188. It proves one new
infinite Collatz cycle-stratum exclusion and three exact promotion or subtraction
theorems. It proves none of the Riemann, Collatz, strong Goldbach, or Twin Prime
conjectures and finds no counterexample to them.

| problem | exact TICKET-189 result | discarded or corrected route | next single lemma |
|---|---|---|---|
| Riemann | `SummableFiniteCoreDriftConstructsCompatiblePositiveForm` | infer convergence from adjacent fixed-core drift merely tending to zero | `PoleNeutralGuinandWeilFixedCoreDriftHasCertifiedSummableOperatorMajorantAndVanishingNegativeFloor` |
| Collatz | `ExactlyFiveValuationOnesOtherwiseTwoCycleExclusion` | extrapolate bounded five-one enumeration to every horizon | `NoContractingValuationWordWithExactlySixOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| Goldbach | `ProperPrimePowerContaminationHasExplicitSublinearBudget` | treat sublinear contamination as if it lower-bounded the total convolution | `ExplicitMajorArcMainMinusMinorArcErrorExceedsSublinearPrimePowerBudgetForEveryLargeEvenTarget` |
| Twin Prime | `ShiftTwoVonMangoldtPrimePowerContaminationBridge` | infer a twin from positive shift-two von Mangoldt correlation without subtraction | `ShiftTwoVonMangoldtCorrelationHasPositiveLinearLowerBoundOnInfinitelyManyDyadicBlocks` |

Reproduce the results with:

```powershell
D:\python\anaconda3\python.exe scripts\ticket189_corefive_sublinear_shift.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket189_corefive_sublinear_shift -v
```

The machine artifact is
`data/open-problem/ticket189-corefive-sublinear-shift.json`. All four conjecture
statuses are `open_not_proven`.

## 2. Riemann Hypothesis

### 2.1 Declared proposition

Let `A_N` be Hermitian matrices. For each fixed `m`, let `A_N^[m]` denote the
leading `m x m` core and suppose

```text
||A_(N+1)^[m] - A_N^[m]|| <= d_(N,m),
sum_{N=m}^infinity d_(N,m) < infinity.
```

Then `A_N^[m]` converges in operator norm to a Hermitian matrix `Q_m`, with

```text
||Q_m - A_N^[m]|| <= sum_{k=N}^infinity d_(k,m).
```

The limits are compatible principal sections and define one Hermitian form `Q`
on finite-support sequences `c_00`. If also

```text
lambda_min(A_N) >= -eta_N,  eta_N -> 0,
```

then `Q` is positive semidefinite on `c_00`.

### 2.2 Proof and exact replay family

Summable drift makes every fixed core Cauchy in a finite-dimensional Banach
space. Summing the drift tail gives the quantitative error. Restriction commutes
with the limit, so `Q_(m+1)` restricts to `Q_m`. Cauchy interlacing gives
`lambda_min(A_N^[m])>=lambda_min(A_N)`. Passing to the norm limit and then
letting `eta_N` vanish proves `Q_m>=0`, hence `Q>=0` on `c_00`.

The rational replay family is

```text
A_N = diag(1+1/N, 1/2+1/N, ..., 1/N+1/N).
```

For every fixed core, the error is exactly `1/N`, adjacent drift is
`1/(N(N+1))`, and the remaining drift sum is exactly `1/N`. Its full minimum
eigenvalue is `2/N>0`.

### 2.3 No-go and remaining gap

The scalar family `A_N=H_N` has adjacent drift `1/(N+1)->0`, but the harmonic
sequence diverges. Thus “adjacent drift tends to zero” is not a convergence
criterion; a summable majorant or another certified Cauchy modulus is required.

This theorem is abstract. PrimeProject has not proved the summable core-drift
bound or vanishing negative floor for the actual pole-neutral Guinand-Weil
family. Recent screw-function and finite-section programs also stop short of an
RH proof: [Suzuki 2026](https://arxiv.org/abs/2606.09096),
[Kim et al. 2026](https://arxiv.org/abs/2607.24830), and
[Groskin 2026](https://arxiv.org/abs/2605.20224).

## 3. Collatz conjecture

### 3.1 Declared proposition

No positive accelerated Collatz cycle has exactly five valuations equal to one
and every remaining valuation equal to two. Primitive and imprimitive periods
are both excluded.

### 3.2 Exact affine arithmetic

After cyclic rotation, write the five positive gaps as `a,b,c,d,e`, with `e`
largest and `h=a+b+c+d+e`. The cycle denominator and ordered numerator are

```text
D = 4^h/32 - 3^h,

B = 4^h/32 - 3^(h-1)
    + 4^a 3^(h-a-1)
    + 2*4^(a+b-1) 3^(c+d+e-1)
    + 4^(a+b+c-1) 3^(d+e-1)
    + 2*4^(a+b+c+d-2) 3^(e-1).
```

An integer cycle requires `D | B`. Contraction starts at `h=13`. Also `B>D`,
and both `B` and `D` are odd.

### 3.3 All-horizon exclusion

Put `u=3/4`. A sufficient condition for `B<3D` is

```text
(32/3)u^(h-a) + (16/3)u^(c+d+e) + (8/3)u^(d+e)
+ (4/3)u^e + (256/3)u^h < 2.
```

The largest-gap rotation gives

```text
e >= ceil(h/5),
d+e >= ceil(h/5)+1,
c+d+e >= ceil(h/5)+2,
h-a >= ceil((h+3)/2).
```

The resulting all-word majorant is nonincreasing and at `h=22` is

```text
131155153587 / 68719476736 < 2.
```

Therefore `1<B/D<3` for every `h>=22`; divisibility would require an odd integer
strictly between one and three, which does not exist. Exact enumeration covers

```text
sum_{h=13}^{21} binomial(h,5) = 72897
```

remaining words and finds no divisibility hit. Per-horizon transcript hashes,
closed-form checks, and cyclic rotation identities are recorded in JSON.

### 3.4 Limitation

This closes one infinite periodic valuation stratum. It does not address words
with six or more ones, valuations at least three, or aperiodic divergence.
Parity-vector and 2-adic ghost-cycle work likewise distinguishes local symbolic
constraints from positive integer dynamics:
[Niu 2026](https://arxiv.org/abs/2605.13886),
[Dhiman-Pandey 2026](https://arxiv.org/abs/2601.12772).

## 4. Strong Goldbach conjecture

### 4.1 Declared proposition

Let `A(N)` count distinct proper prime powers at most `N` and
`L=floor(log_2 N)`. Then

```text
A(N) <= sum_{k=2}^L floor(N^(1/k))
     <= floor(sqrt N) + max(L-2,0) floor(N^(1/3)).
```

Combining this with the TICKET-188 decomposition gives

```text
E_pp(N) <= 2 A(N)(log N)^2 = o(N).
```

Hence any certified lower bound `R_Lambda(N)>=cN` for all sufficiently large
even `N`, for a fixed `c>0`, eventually exceeds contamination and forces a
Goldbach prime pair. The remaining finite range could then be checked exactly.

### 4.2 Proof and no-go

Every proper prime power `p^k<=N` is counted by the `k`-th root term. The square
term is at most `sqrt N`; every term with `k>=3` is at most `N^(1/3)`, and there
are at most `L-2` of them. Dividing the contamination bound by `N` leaves

```text
O(log^2(N)/sqrt(N) + log^3(N)/N^(2/3)) -> 0.
```

This is only an upper bound on an error term. It does not prove a positive lower
bound for the full convolution. Finite declining ratios are diagnostics, not a
replacement for uniform minor-arc control. Current exceptional-set results do
not close that every-target gap:
[Grimmelt-Bhowmik 2026](https://arxiv.org/abs/2607.27282). The weighted
prime-power distinction is standard in circle-method work such as
[Helfgott 2015](https://arxiv.org/abs/1501.05438).

## 5. Twin Prime conjecture

### 5.1 Declared proposition

For `X=2^j`, define

```text
S_Lambda(X) = sum_{X<=n<2X} Lambda(n)Lambda(n+2)
            = P_2(X) + E_2pp(X),
```

where `P_2` contains genuine twin-prime terms. Then

```text
0 <= E_2pp(X) <= 2 A(2X+2)(log(2X+2))^2 = o(X).
```

Thus a sound lower bound above this budget proves a twin in the block. In
particular, if `S_Lambda(2^j)>=c2^j` for a fixed `c>0` on infinitely many
unbounded `j`, then infinitely many blocks contain twins.

### 5.2 Exact no-go and limitation

A contaminated term has a proper prime power at `n` or `n+2`, yielding the
factor `2A(2X+2)` and the stated weight bound. Positivity alone is false as a
twin certificate: `n=25` gives

```text
(25,27) = (5^2,3^3),
Lambda(25)Lambda(27) = log(5)log(3) > 0,
```

but neither endpoint is prime.

The finite dyadic rows only replay the exact decomposition. No independent
Type I/II estimate gives the required positive linear lower bound on infinitely
many blocks. This remains the arithmetic gap identified by prime-producing
sieve theory: [Ford-Maynard 2024](https://arxiv.org/abs/2407.14368).

## 6. Proof-status conclusion

TICKET-189 proves four exact statements. Only the Collatz statement closes a new
infinite arithmetic family. The RH theorem identifies a sufficient convergence
contract, while Goldbach and Twin Prime now share one explicit sublinear
prime-power subtraction. The resolution count remains `0 / 4`.
