# TICKET-198: Verified Height, Primitive Words, and Quantifier Strength

## Abstract

TICKET-198 continues PrimeProject's simultaneous attack on the Riemann
Hypothesis, the Collatz conjecture, the strong Goldbach conjecture, and the
Twin Prime conjecture. It proves four exact intermediate statements and
resolves none of the parent conjectures.

1. The rigorous Platt--Trudgian finite-height RH verification transfers to an
   existential Rouché certificate for every integer rectangle level
   `2 <= m <= 3*10^12`.
2. Even after the TICKET-183 primitive-root reduction, every fixed cyclic run
   count contains an explicit infinite family of primitive `{1,2}` words that
   passes both exact scalar cycle gates.
3. A Goldbach margin on every collision-free target would leave an
   `O(X/log^2 X)` exceptional set rather than prove strong Goldbach.
4. Dominating the Twin Prime prime-power contamination by global block mass
   forces a square-root-scale pair count and is much stronger than one positive
   pair per block.

The integrated machine-readable result is
[`ticket198-verified-height-primitive-word-quantifier-strength.json`](../data/open-problem/ticket198-verified-height-primitive-word-quantifier-strength.json).
All statuses remain `open_not_proven`; the conjecture resolution count is zero.

## Claim table

| Problem | Exact TICKET-198 result | Route rejected or limited | Single next lemma |
|---|---|---|---|
| RH | `FiniteHeightRHTransfersToFiniteXiRouchePrefix` | treating a single existential `D_3` closure as the decisive RH bridge | `StandaloneIntervalXiTaylorDegreeAndRoucheMarginOnD3WithoutImportingFiniteHeightRH` |
| Collatz | `FixedRunCountLeavesInfinitePrimitiveAdmissibleFamilies` | treating primitive normalization plus fixed run count as a finite search | `UniformAffineDivisibilityObstructionForPrimitiveFixedRunCountOneTwoWordsInTheAdmissibleDensityWindow` |
| Goldbach | `CollisionFreeGoldbachMarginLeavesLogSquaredExceptionalSet` | promoting density-one collision-free control to all-even control | `ExplicitGoldbachCorrelationMarginOnEveryLargeCollisionSupportedEvenTarget` |
| Twin Prime | `TwinBlockMassDominanceForcesSquareRootScalePairCount` | treating global contamination dominance as a minimal infinitude target | `PrimePowerFreeLocalizedTwinDetectorHasPositiveMassOnInfinitelyManyDyadicBlocks` |

## 1. Riemann Hypothesis

### 1.1 Declared proposition

Let

```text
Xi(z) = xi(1/2 + i z),
D_m^+ = {z: |Re z| <= m, 1/m <= Im z <= m},
D_m^- = conjugate(D_m^+).
```

Assume every nontrivial zero `beta+i gamma` with `0<|gamma|<=H` lies on
`beta=1/2`. Then `Xi` has no zero on either closed `D_m` rectangle for every
integer `2<=m<=H`. A Taylor section satisfying the strict Rouché inequality
therefore exists for every such rectangle.

Platt and Trudgian rigorously verified the premise with interval arithmetic for
`H=3*10^12` in
[The Riemann hypothesis is true up to 3*10^12](https://doi.org/10.1112/blms.12460).
PrimeProject imports that theorem. It does not independently repeat their zero
verification.

### 1.2 Proof

For `z=x+i y`,

```text
s = 1/2 + i z = (1/2-y) + i x.
```

A zero in `D_m^+` or `D_m^-` has `|Im s|<=m<=H` and is separated from the
critical line by at least `1/m`. The imported theorem excludes it. On the real
segment `0<s<1`, the alternating eta series is positive and
`zeta(s)=eta(s)/(1-2^(1-s))` is nonzero; the endpoints are also not xi zeros.
Thus each compact rectangle is zero-free. Compact-uniform Taylor convergence
then gives a section `S_n` with

```text
sup |Xi-S_n| < min |Xi| / 3,
inf |S_n| > 2 min |Xi| / 3.
```

Rouché's theorem gives zero count zero.

### 1.3 Exact advance and limit

- Rectangle levels transferred: `2,999,999,999,999`.
- `D_3` enters the edge portions of the open critical strip.
- The transfer remains existential: no Taylor degree or interval margin is
  produced.
- Every ordinate above `3*10^12` remains outside this finite theorem.

The next task is a standalone interval certificate on `D_3`, useful as a
reproducible implementation milestone but not as a claim of RH progress beyond
the imported height theorem.

## 2. Collatz conjecture

### 2.1 Declared proposition

TICKET-183 already proved the exact primitive-root reduction. TICKET-198 uses
that result as an input and does not re-claim it. For every fixed integer
`r>=2` and every `k>=2`, define

```text
w_(r,k) = 1^k 2^(2k) (1 2^2)^(r-1).
```

Then `w_(r,k)` is primitive, has exactly `r` cyclic one-runs and `r` cyclic
two-runs, has one-density `1/3`, and passes both exact scalar cycle gates.
Consequently, primitive normalization and a fixed run count do not turn the
remaining scalar-admissible search into a finite enumeration.

### 2.2 Proof and computation

Put `q=k+r-1`. The word has

```text
number of ones = q,
number of twos = 2q,
horizon h = 3q,
valuation sum S = 5q.
```

The two gates hold exactly:

```text
2^S = 32^q > 27^q = 3^h,
2^q (5/6)^(3q) = (125/108)^q > 1.
```

Its cyclic run lengths are

```text
(k, 2k, 1, 2, ..., 1, 2).
```

For `k>=2`, the one-run of length `k` and the two-run of length `2k` are each
unique. A nontrivial word power would repeat every cyclic run-length pattern,
contradicting uniqueness. Hence the word is primitive. Letting `k` grow gives
infinitely many distinct words for every fixed `r`.

The generator checks `r=2,...,8` and `k=2,...,64`, totaling 441 words. It
verifies primitivity, the exact run count, and both scalar gates. This finite
scan is a regression check; the all-`r`, all-`k` statement follows from the
symbolic argument.

### 2.3 Route decision

- **Discard:** treating primitive normalization plus a fixed run count as a
  finite search space.
- **Keep:** derive a uniform all-length affine divisibility obstruction for
  each fixed run count.
- **Limit:** no affine divisibility hit is proved or refuted for the infinite
  families; valuations above two and aperiodic trajectories remain open.

## 3. Strong Goldbach conjecture

### 3.1 Declared proposition

Let `C` be the even targets on which the proper-prime-power overlap `Q*Q` is
positive, and let `E` be the actual strong-Goldbach exceptional set. Suppose a
future theorem proves every sufficiently large even target outside `C` is a sum
of two primes. Then

```text
E \ C is finite,
|E intersect [1,X]| = O(X/log^2 X).
```

The second conclusion uses the TICKET-197 support bound. It does not imply
`E=empty`.

### 3.2 Exact no-go witness

For every odd prime `p`,

```text
2p^2 = p^2 + p^2
```

lies in `C`. Hence `S={2p^2}` is an explicit infinite subset of the unresolved
stratum. An abstract nonnegative indicator that is zero on `S` and positive
off `C` satisfies collision-free positivity but has infinitely many failures.
This is a countermodel to the inference, not a counterexample to Goldbach and
not the actual prime representation function.

The finite replay through `2^20` finds 17,411 collision-supported targets and
127 diagonal targets; all are actually Goldbach-represented in that finite
range. This finite fact is not promoted to the infinite diagonal.

### 3.3 Route decision

The old next lemma becomes only the collision-free half of a two-stratum
argument. The decisive complementary target is pointwise positivity on every
sufficiently large collision-supported even target.

## 4. Twin Prime conjecture

### 4.1 Declared proposition

Let `T(X)` count twin-prime starts in `[X,2X)` and let

```text
M(X) = sum log(p) log(p+2)
```

over those pairs. Since each summand is at most `log(2X+2)^2`,

```text
M(X) <= T(X) log(2X+2)^2.
```

Thus a contamination-dominating bound

```text
M(X) >= K sqrt(X) log X
```

forces

```text
T(X) >= K sqrt(X) log X / log(2X+2)^2,
```

which tends to infinity. The target asks for much more than one twin pair.

### 4.2 Computation and inference boundary

Thirteen blocks from `[2^10,2^11)` through `[2^22,2^23)` replay the exact
mass-count inequality. The last block contains 22,643 observed pairs, while a
unit-constant `sqrt(X)log X` mass threshold would force at least 123 pairs.
These finite observations do not imply an unbounded theorem.

An abstract one-atom sequence on blocks `X_j=2^(2^j)` remains infinite while
its maximum logarithmic mass divided by `sqrt(X_j)log X_j` tends to zero. This
does not model the primes or prove formal independence. It isolates the missing
quantitative information in an inference from bare infinitude.

### 4.3 Route decision

- **Discard as minimal target:** globally dominate all prime-power
  contamination.
- **Keep:** a localized nonnegative detector that vanishes on prime-power
  contamination and whose positivity directly witnesses one genuine gap-two
  pair.
- **Open:** proving such positivity on infinitely many blocks.

## 5. Proof DAG

Each track records the same audited shape:

```text
TICKET-197 open target
        |
        v
TICKET-198 exact theorem ---- refuted/overstrong route
        |
        v
single revised lemma (open_not_proven)
```

No path reaches a parent-conjecture `proved` node.

## 6. Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket198_verified_height_primitive_word_quantifier_strength.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket198_verified_height_primitive_word_quantifier_strength -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
node scripts\verify_pages.cjs
```

Expected machine boundary:

```text
exact theorem count: 4
Collatz fixed-run primitive words: 441
Goldbach cutoff rows: 13
Twin dyadic rows: 13
parent conjectures resolved: 0
failures: 0
```
