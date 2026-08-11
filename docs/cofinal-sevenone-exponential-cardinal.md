# TICKET-214: Cofinal Defects, Seven-One Cycles, Exponential Witnesses, and Cardinal Gap Selection

## Abstract

TICKET-214 continues the four-conjecture proof-search program from TICKET-213.
It does not resolve the Riemann Hypothesis, the Collatz Conjecture, the Strong
Goldbach Conjecture, or the Twin Prime Conjecture. It proves four narrower
statements that separate exact target selection from the still-missing
infinite arithmetic estimate.

1. An exact multiplicity equality on one unbounded sequence of boundary-free
   heights is equivalent to RH, while critical-line density one is not.
2. Every positive accelerated Collatz cycle word with exactly seven
   valuation-one entries is excluded by exhaustive ordinary-integer
   divisibility testing.
3. A scale-growing exponential Goldbach selector detects an empty dyadic
   target exactly, but proving its sum below one is equivalent to proving
   coverage; aggregate witness mass and a capacity bound are insufficient.
4. Cardinal-sine interpolation selects gap two exactly on all even integer
   gaps, but unboundedness of the selected prime-gap correlation remains
   precisely the Twin Prime problem.

All four parent conjectures remain `open_not_proven`. The machine resolution
count is zero.

## Result ledger

| Problem | Exact TICKET-214 result | Route discarded | Remaining gap | Next lemma |
|---|---|---|---|---|
| Riemann | `CofinalExactDefectEquivalenceAndDensityOneNoGo` | density-one or relative-defect convergence as an RH certificate | exact equality for actual zeta on an unbounded sequence | `CertifiedCofinalMultiplicityEqualityForActualZeta` |
| Collatz | `CompleteSevenValuationOneExclusionAndFiniteStratumNoGo` | all seven-one words; any finite list of fixed strata as a complete proof | every `k>=8` cycle stratum and nonperiodic divergence | `UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastEight` |
| Goldbach | `DyadicExponentialSelectorEquivalenceAndOccupancyNoGo` | selector construction or total witness mass plus a cap as an independent proof | a uniform arithmetic subunit estimate | `UniformArithmeticSubunitBoundForDyadicExponentialWitnessSelector` |
| Twin Prime | `CardinalSineExactGapTwoSelectorAndPositivityCircularity` | exact selector construction alone and fixed-degree polynomial all-gap filters | an unbounded arithmetic lower bound for the selected channel | `UnboundedArithmeticMinorantForCardinalSinePrimeGapFunctional` |

## 1. Riemann: exact cofinal equality versus density one

Let `N(T)` count zeros with multiplicity in an expanding, boundary-free
upper-half critical-strip rectangle, and let `M(T)` count critical-line zero
multiplicity in the same rectangle. TICKET-213 proved

```text
D(T) = N(T) - M(T)
     = 2 * (off-line multiplicity on one side).
```

### Theorem RH-TICKET-214

`D(T)` is a nonnegative, even, nondecreasing step function. RH is equivalent
to the existence of an unbounded sequence of boundary-free heights `T_j` for
which `D(T_j)=0`.

### Proof

An off-line symmetry pair contributes a positive even amount when it enters
the rectangle and never leaves as the height increases. Thus `D` is
nondecreasing. If an off-line zero existed, every sufficiently high rectangle
would have `D>=2`, contradicting equality at a later member of an unbounded
zero-defect sequence. The converse follows directly from RH.

### Density-one no-go

The weaker condition

```text
M(T) / N(T) -> 1
```

does not imply RH. A logical symmetric zero multiset can contain one persistent
off-line pair and an increasing number of critical-line zeros. Then `D(T)=2`
but `D(T)/N(T)->0`. The JSON audit uses line multiplicities from `10^2` through
`10^8`; every row violates the finite-rectangle RH condition while its
relative defect decreases to zero.

This is a countermodel to a logical implication, not an off-critical zero of
the actual zeta function.

### Remaining gap

No exact cofinal equality is proved for actual zeta zeros. The next single
lemma is:

```text
CertifiedCofinalMultiplicityEqualityForActualZeta
```

## 2. Collatz: complete seven-one exclusion

For an accelerated positive Collatz cycle, write the valuation word as
`a_0,...,a_(h-1)`, let `A=sum a_i`, and suppose exactly `k` entries equal one.
Minimum rotation forces `a_0=1` and `a_(h-1)>=2`. The standard product bound
gives

```text
A >= 2h-k,
(6/5)^h <= 2^k.
```

For `k=7`, this implies `8<=h<=26` and gives a finite bound on `A`.

### Theorem CO-TICKET-214

No nontrivial positive accelerated Collatz cycle has exactly seven
valuation-one entries.

### Exact computation

For each allowed length, the generator enumerates every placement of the
remaining six one-valuations and every weak composition of the valuation
excess above the `2h-7` baseline. Each word is tested in

```text
(2^A - 3^h) x = C(a_0,...,a_(h-1)).
```

The result is:

```text
candidate words                         4,349,349
ordinary divisibility candidates               0
positive odd integer fixed points              0
machine failures                               0
```

Per-length SHA-256 transcript hashes are stored in the machine-readable
artifact. Combined with the earlier strata, a hypothetical nontrivial
positive cycle must now contain at least eight valuation-one entries.

### Fixed-stratum enumeration no-go

At length `h=2k`, baseline words alone provide at least

```text
C(2k-2,k-1)
```

candidates. The direct counts grow from `4,349,349` at `k=7` to `49,565,886`
at `k=8`, `623,355,008` at `k=9`, and `8,498,724,659` at `k=10`. Excluding any
finite list of `k` values leaves every larger stratum untouched. This rejects
finite repetition of the current exhaustive method as a complete proof, not
the possibility of a uniform structural argument.

### Remaining gap

```text
UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastEight
```

Nonperiodic divergence is also untouched.

## 3. Goldbach: a scale-growing exact selector

For a finite block of `B` even targets, let `A_i` be the unordered Goldbach
representation count. Choose the least integer `k_B` with `2^k_B>B` and set

```text
E_B = sum_i 2^(-k_B A_i).
```

### Theorem GB-TICKET-214, selector equivalence

```text
E_B < 1  if and only if  every A_i >= 1.
```

If some `A_i=0`, its summand is one. If all counts are positive, every summand
is at most `2^(-k_B)`, hence `E_B<=B/2^k_B<1`.

This constructs the scale-growing nonpolynomial selector requested by
TICKET-213. It does not prove its subunit bound on all dyadic blocks: that
bound is exactly equivalent to Goldbach coverage on those blocks.

### Sharp occupancy bound

Suppose only `B`, the total witness mass `S=sum A_i`, and a positive cap
`0<=A_i<=U` with `U>0` are known. If `Z` is the number of zero counts, then

```text
Z <= B - ceil(S/U),
```

and this is sharp. At least `ceil(S/U)` nonzero boxes are needed; filling all
but one of them to capacity attains the bound. Aggregate information forces
`Z=0` only if `S>(B-1)U`.

The exact dyadic audit found no exceptions for starts `128, 512, 2048, 8192,
32768`, but the sharp aggregate bounds still permitted respectively `33, 143,
638, 2719, 10992` zero targets. Thus total witness mass cannot replace local
anti-concentration.

### Remaining gap

```text
UniformArithmeticSubunitBoundForDyadicExponentialWitnessSelector
```

The required estimate must use arithmetic structure beyond total mass and a
per-target cap.

## 4. Twin Prime: cardinal-sine exact selection

Define

```text
S(h) = sinc(h/2 - 1),
sinc(x) = sin(pi x)/(pi x),  sinc(0)=1.
```

Every prime gap after `(2,3)` is even. At `h=2r`, the argument `r-1` is an
integer, so

```text
S(2)=1,
S(2r)=0 for every integer r>=2.
```

### Theorem TP-TICKET-214

For every finite range of consecutive odd-prime gaps, with the exceptional
gap `(2,3)` omitted, let `t_h` count gaps of size `h`. Then

```text
sum_h S(h)t_h = t_2.
```

The selector has zero remainder on the even integer gap lattice. Audits through
`10^2, 10^3, 10^4, 10^5` produced exact functional values `8, 35, 205, 1224`,
identical to the observed gap-two counts.

Unboundedness of this cumulative functional is equivalent to twin-prime
infinitude. The interpolation identity therefore solves channel selection,
not arithmetic positivity.

### Polynomial selector no-go

For gaps through `2M`, the degree-`M-1` Lagrange selector is

```text
P_M(2r) = product_(j=2)^M (r-j)/(1-j).
```

It equals one at `r=1`, zero for `2<=r<=M`, and has tail

```text
P_M(2r) = (-1)^(M-1) C(r-2,M-1),  r>M.
```

No fixed nonzero polynomial can vanish at every integer `r>=2`. Increasing the
cutoff increases the degree and amplifies the uncontrolled tail. Cardinal-sine
interpolation removes that representation error but does not create a prime
correlation lower bound.

### Remaining gap

```text
UnboundedArithmeticMinorantForCardinalSinePrimeGapFunctional
```

## Cross-problem conclusion

TICKET-214 identifies a common obstruction:

```text
exact target selection != positive infinite arithmetic control.
```

Density-one evidence does not force zero RH defect. Finitely many Collatz
strata do not cover unbounded valuation complexity. An exact Goldbach selector
does not bound itself below one. An exact gap-two selector does not prove that
its selected channel is unbounded.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket214_cofinal_sevenone_exponential_cardinal.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket214_cofinal_sevenone_exponential_cardinal -v
```

Primary machine artifact:

```text
data/open-problem/ticket214-cofinal-sevenone-exponential-cardinal.json
```

The four parent conjectures remain open. No literature-priority claim is made
without independent mathematical review.
