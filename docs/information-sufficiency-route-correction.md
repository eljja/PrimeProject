# TICKET-184: Information Sufficiency and Proof-Route Correction

## Abstract

TICKET-184 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, the strong Goldbach conjecture, or the Twin Prime conjecture. It
continues the four open nodes of TICKET-183 and asks a stricter question before
spending more computation: does the proposed intermediate statement contain
enough information, and is it no stronger than the parent conjecture requires?

Four exact results answer that question.

| Problem | Exact result | Status |
|---|---|---|
| Riemann | `FiniteMomentCancellationDoesNotGiveUniformAbelDesmoothing` | exact no-go; RH open |
| Collatz | `CounterexampleDichotomyAndMinimalCyclePrefixBarrier` | exact decomposition; Collatz open |
| Goldbach | `SquarefreeWheelFactorizationAndCompositeImpostorNoGo` | exact local theorem and no-go; Goldbach open |
| Twin Prime | `PositiveRootMassSufficesAndCantelliExceptionalMassIsSharp` | exact route correction; Twin Prime open |

No claim of literature priority is made for these elementary reductions without
independent expert review. Their role is to prevent an invalid proof route from
being confused with progress on the infinite conjecture.

## 1. Research contract

Each track records five separate objects:

1. a declared proposition with explicit quantifiers;
2. a mathematical proof or counterexample;
3. a reproducible finite computation;
4. the exact limit of that computation;
5. one next open lemma.

The machine status remains `open_not_proven` for all four conjectures. A finite
search can find a counterexample, but absence of a counterexample below a cutoff
does not prove a universal or infinitude statement.

## 2. Riemann Hypothesis

### 2.1 Declared proposition

Fix integers `m>=1` and `M>=1`, and set

```text
f_(M,m)(theta) = 2^(-m) e^(i M theta) (1-e^(i theta))^m.
```

Its Fourier coefficients are

```text
c_r = 2^(-m)(-1)^r binom(m,r),  0<=r<=m,
```

at frequencies `M+r`. They satisfy

```text
sum_(r=0)^m c_r (M+r)^j = 0,  0<=j<m.
```

Nevertheless,

```text
||f_(M,m)||_infinity = 1,
||A_rho f_(M,m)||_infinity = rho^M ((1+rho)/2)^m,
```

and at `theta=pi`,

```text
|f_(M,m)-A_rho f_(M,m)|
  = 1-rho^M((1+rho)/2)^m.
```

For fixed `m` and `rho<1`, the Abel mean tends uniformly to zero while the
original norm and desmoothing error tend to one.

### 2.2 Proof

The moment sum is the `m`-th finite difference of the polynomial
`x -> (M+x)^j`. It vanishes when `j<m`. Also,
`|1-e^(i theta)|<=2`, with equality at `theta=pi`. Abel multiplication replaces
each coefficient at frequency `M+r` by `rho^(M+r)`, so the binomial expansion
refactors as

```text
A_rho f_(M,m)(theta)
  = 2^(-m) rho^M e^(iMtheta)(1-rho e^(itheta))^m.
```

The maximum of `|1-rho e^(itheta)|` is `1+rho`, again at `pi`. This proves all
three formulas.

### 2.3 What this refutes

Any compactness argument based only on a **fixed finite list of polynomial
Fourier moments** still admits unit high-frequency mass hidden by Abel
regularization. The computation checks `m in {1,2,4,8}` and
`M in {16,32,64}` by exact integer moment sums. At `rho=0.9`, the smallest
smoothed norm is about `7.82e-4`, while the corresponding desmoothing lower
bound exceeds `0.9992`.

This is not a counterexample to the Weil criterion. The actual criterion uses a
constrained Mellin test cone with support, positivity, and pole-neutral
conditions. Connes and Consani explicitly retain such conditions in their
operator-theoretic formulation
([The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368)). The result only
shows that replacing that full structure by finitely many periodic moments is
insufficient.

### 2.4 Remaining gap

**Next lemma:**
`NormalizedWeilAdmissibleConeHasUniformFourierTailTightnessFromFullMellinConstraints`.

It must use genuinely infinite-dimensional Weil admissibility. Proving another
finite-moment estimate cannot close this node.

## 3. Collatz conjecture

### 3.1 Declared proposition

For the accelerated odd map

```text
T(n) = (3n+1)/2^v,  v=v_2(3n+1),
```

every counterexample has one of two types:

1. a nontrivial periodic orbit;
2. an orbit unbounded in limsup.

For a periodic valuation word `w=(v_0,...,v_(h-1))`, write

```text
S_k = v_0+...+v_(k-1),
B_k = sum_(j<k) 3^(k-1-j) 2^S_j,
D_k = 2^S_k-3^k.
```

Rotate a nontrivial cycle to its least odd member `n=B_h/D_h`. Then

```text
v_0 = 1,
B_k D_h >= D_k B_h  for every 1<=k<=h.
```

These prefix barriers are necessary but not sufficient. The word `(1,3)` has
`B=5`, `D=7`, passes all barriers, and fails `D|B`.

### 3.2 Proof

A bounded positive-integer orbit takes values in a finite set, so determinism
forces a repetition and hence a cycle. A nonperiodic counterexample must
therefore be unbounded in limsup. At the least member `n>1` of a nontrivial
cycle, `v_0>=2` would imply

```text
T(n) <= (3n+1)/4 < n,
```

a contradiction. Finally,

```text
n_k = (3^k n+B_k)/2^S_k >= n
```

gives `B_k >= D_k n`; substituting `n=B_h/D_h` gives the cross-multiplied
barrier.

### 3.3 Route correction and computation

TICKET-183 narrowed the **cycle branch** to primitive contracting words that
contain valuation one. That is valid, but excluding those words would not
exclude a divergent orbit. A cycle-only program is therefore not a complete
Collatz proof program.

Exact enumeration over alphabet `{1,...,5}` through length seven found `5,036`
primitive, contracting, first-valuation-one words that satisfy every prefix
barrier but fail affine divisibility. This proves that the barrier is a useful
filter, not a cycle certificate. Separately, all `499,999` odd starts at most
`1,000,000` attained a smaller odd value; the largest observed first-descent
time was `111`, at start `626331`. That finite statement is not a universal
descent theorem.

Tao's almost-all result illustrates the same quantifier boundary: density
control is deep, but it does not establish every-orbit convergence
([Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)).

### 3.4 Remaining gap

**Next lemma:**
`EveryPositiveOddIntegerAboveOneHasAnAcceleratedIterateBelowItsStart`.

Strong induction would turn this lemma into the full Collatz conjecture. No
finite cutoff proves it.

## 4. Strong Goldbach conjecture

### 4.1 Declared proposition

Let `Q` be a squarefree product of odd primes and let `U_Q` be its unit residue
classes. Define

```text
R_Q(n) = #{a mod Q : a in U_Q and n-a in U_Q}.
```

Then

```text
R_Q(n) = product_(p|Q) [p-1 if p|n, otherwise p-2].
```

Every local target therefore has positive wheel margin. However, for every
`r in U_Q` there is a composite integer `x_r congruent r (mod Q)`. Consequently
a residue histogram identical to the unit wheel can be supported entirely on
composites.

### 4.2 Proof

Modulo a prime `p|Q`, the two forbidden residues are `0` and `n`. They coincide
when `p|n`, leaving `p-1` choices; otherwise they are distinct, leaving `p-2`.
The Chinese remainder theorem multiplies the local counts.

For the no-go, choose a prime `ell` not dividing `Q` and solve

```text
ell t congruent r (mod Q).
```

If necessary replace `t` by `t+Q` so that `t>=2`. Then `x_r=ell t` is composite
and remains in residue `r`.

### 4.3 Reproducible boundary

The factorization was checked for every target modulo `15`, `105`, and `1155`.
For `Q=1155`, all `480` unit residues were reproduced by explicit composites
with known proper divisors. Thus fixed-wheel positivity is exact but cannot
distinguish primes from a composite impostor.

This does not challenge the circle method. It identifies why the modulus must
grow and why prime-weighted minor-arc control is indispensable. Current work on
Goldbach exceptional sets likewise separates explicit major arcs from the
remaining uniform control
([Grimmelt and Bhowmik, 2026](https://arxiv.org/abs/2607.27282)).

### 4.4 Remaining gap

**Next lemma:**
`GrowingWheelPrimeWeightedMinorErrorIsUniformlyBelowTheLocalSingularMargin`.

The quantifiers over target and scale are essential. A larger but fixed wheel is
still defeated by the same composite-impostor construction.

## 5. Twin Prime conjecture

### 5.1 Declared proposition

Partition candidate first coordinates into finite disjoint blocks. Let
`E_j>0` be an expected twin-pair mass and let `C_j` count starts `p` in block
`j` for which both `p` and `p+2` are prime. The root ratio is

```text
R = (sum_j C_j)/(sum_j E_j).
```

Then `R>0` if and only if the union contains a twin-pair start. If this holds on
infinitely many pairwise disjoint intervals escaping to infinity, there are
infinitely many twin primes. Positivity of every leaf is not required.

For normalized block masses `mu_j`, ratios `r_j`, mean `r_bar`, and variance
`V`, Cantelli's inequality gives

```text
mu{r_j <= r_bar-t} <= V/(V+t^2),  t>0.
```

The bound is sharp for one zero leaf and all other leaves equal to one.

### 5.2 Proof and route correction

The root denominator is positive, so the root is positive exactly when the
total actual count is positive. Pairwise disjoint positive blocks provide
distinct twin pairs. Cantelli follows from a shifted-square Markov bound,
optimized over the shift. For one zero leaf of mass `epsilon` and background
one, the mean is `1-epsilon`, variance is `epsilon(1-epsilon)`, and setting
`t=1-epsilon` makes both sides equal `epsilon`.

TICKET-183's every-path Haar certificate is a valid sufficient condition, but
it is stronger than the Twin Prime conjecture needs. In the finite interval
`[100000,362144)`, the project counts `2,298` twin pairs and root ratio
`1.000378...`, while the every-leaf certificate fails. The right proof target is
recurring positive **total** block mass, not positivity of every subdivision.

The parity barrier still blocks that lower bound. Maynard's survey explains the
gap between bounded-gap progress and exact gap two
([On the Twin Prime Conjecture](https://arxiv.org/abs/1910.14674)).

### 5.3 Remaining gap

**Next lemma:**
`PrimePairBlockMainTermDominatesParityRemainderOnAnUnboundedDisjointSequence`.

Haar and Cantelli statistics may locate exceptional blocks, but only an
arithmetic, parity-breaking remainder estimate can prove the recurring positive
root.

## 6. Proof DAG summary

```text
RH-T183 Abel transfer
  -> finite-moment no-go [proved]
  -> full Weil-cone tail tightness [open]

CO-T183 primitive cycle words
  -> failure dichotomy + prefix barrier [proved]
  -> universal finite descent [open]

GB-T183 exact Fourier margin
  -> squarefree wheel + composite impostor [proved]
  -> growing prime-weighted margin domination [open]

TP-T183 Haar path certificate
  -> positive root suffices + sharp Cantelli bound [proved]
  -> positive block total on unbounded disjoint scales [open]
```

## 7. Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket184_information_sufficiency_route_correction.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket184_information_sufficiency_route_correction
```

Machine-readable outputs:

```text
data/open-problem/ticket184-information-sufficiency-route-correction.json
data/open-problem/riemann/rh-ticket-184-finite-moment-no-go.json
data/open-problem/collatz/co-ticket-184-dichotomy-prefix-barrier.json
data/open-problem/goldbach/gb-ticket-184-wheel-impostor.json
data/open-problem/twin-prime/tp-ticket-184-root-cantelli.json
```

The machine audit records four exact theorems, four rejected or corrected
routes, two decisive-target corrections, zero failures, and zero conjecture
resolutions.
