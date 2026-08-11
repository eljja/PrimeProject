# TICKET-216: Laplace Defects, Cross-Power GCDs, Radix Histograms, and Tauberian Tails

## Claim boundary

TICKET-216 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, strong Goldbach, or the Twin Prime conjecture. It proves four
smaller statements, records four failed promotion routes, and leaves one
explicit arithmetic lemma open for each problem. The machine resolution count
is zero.

The aim of this ticket is not to enlarge a finite search range. It exposes the
first discrete threshold that each transform or reduction must cross before it
can affect the parent conjecture.

| Problem | Exact result in this ticket | Discarded route | Remaining gap | Next lemma |
| --- | --- | --- | --- | --- |
| Riemann | `OffLineDefectLaplaceFirstAtomCertificateAndFixedToleranceNoGo` | fixed positive transform tolerance | actual-zeta cofinal upper bounds below the first-atom threshold | `CofinalActualZetaOffLineLaplaceUpperBoundsBelowFirstAtomThreshold` |
| Collatz | `SingleMountainCrossPowerGCDNecessityAndFiniteDiagonalAudit` | finite gcd audit as a full proof | all-`k` strict gcd gap, then multi-run extension | `UniformStrictCrossPowerGCDGapAtEverySingleMountainCrossing` |
| Goldbach | `RadixSelectorFullRepresentationHistogramAndPrecisionDepthNoGo` | lossless encoding as an arithmetic proof | independent all-block interval separating the zero digit | `ArithmeticRadixSelectorIntervalSeparatesTheZeroDigitOnEveryDyadicBlock` |
| Twin Prime | `QuantitativeAbelCountBracketAndFixedDilationTailNoGo` | fixed-dilation coefficient-one tail at twin scale | parity-breaking Abel lower bound above an adaptive tail | `ParityBreakingAbelLowerBoundDominatesAdaptiveGeometricTail` |

## 1. Riemann Hypothesis: a first-atom transform certificate

### Declared proposition

At a boundary-free height `T`, let `N(T)` count all nontrivial zeta zeros and
let `M(T)` count critical-line zeros, both with multiplicity. Set

```text
D(T) = N(T) - M(T),        C(T) = D(T)/2.
```

Critical-line zeros increase `N` and `M` together. An off-line zero is paired
with its reflection across the critical line, so `C` is a nonnegative,
integer-valued, nondecreasing step function that counts off-line symmetry
pairs. For `0<r<1`, define

```text
L(r) = integral r^t dC(t).
```

Then, for every `H`,

```text
C(H) r^H <= L(r).
```

Consequently, a rigorous upper bound `U(r)<r^H` proves that there is no
off-line zero with ordinate at most `H`. Such certificates for an unbounded
sequence of `H` imply RH.

### Proof

Every atom of `dC` at height `t<=H` has integer mass at least one and weight
`r^t>=r^H`. Summing these contributions gives the inequality. If
`U(r)<r^H`, then `C(H)<1`; integrality forces `C(H)=0`. Cofinal heights exclude
every possible finite ordinate.

The threshold is sharp for this information: one pair at height `H`
contributes exactly `r^H`.

### No-go and limit

No fixed positive tolerance can prove RH. For every `epsilon>0`, one logical
off-line pair can be placed high enough that its transform contribution is
below `epsilon`. The generated fixtures verify this exactly at `r=1/2`.
These delayed atoms are logical defect measures, not zeta zeros.

PrimeProject does not produce the needed actual-zeta transform bound. Rigorous
finite-height verification remains a separate achievement; Platt and Trudgian
verified RH through height `3*10^12` using interval arithmetic
([Bulletin of the London Mathematical Society](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/blms.12460)).

## 2. Collatz: exact cross-power GCD necessity

### Declared proposition

Consider a positive accelerated Collatz cycle whose cyclic valuation word is
`1^k 2^m`. Put

```text
Delta = 2^(k+2m) - 3^(k+m) > 0,
C     = 3^k - 2^k,
E     = 4^m - 3^m.
```

TICKET-215 proved that integer closure forces `Delta|C`. TICKET-216 strengthens
this to the exact necessary identity

```text
Delta = gcd(C,E) = gcd(3^k-2^k, 4^m-3^m).
```

### Proof

There is an exact integer identity

```text
Delta = 2^k E - 3^m C.
```

Hence `gcd(C,E)|Delta`. Conversely, `Delta|C`; the same identity gives
`Delta|2^k E`. Since `Delta` is odd, `Delta|E`. Therefore
`Delta|gcd(C,E)`, and equality follows.

### Computation and limit

For each `1<=k<=4096`, the generator finds the unique first `m` for which
`Delta>0` and computes the two exponential differences and their gcd with
arbitrary-precision integers. No gcd equality occurs. The transcript is
hashed in the committed JSON.

This is a finite exclusion for a one-run/one-run word family. It says nothing
about all `k`, multi-run valuation words, valuation entries above two, or
nonperiodic divergence. The next theorem must prove a strict gcd gap at every
first-positive crossing. Transcendence and Diophantine approximation are known
tools for cycle bounds, but do not automatically prove this new all-`k`
statement; compare Simons and de Weger
([Acta Arithmetica record](https://eudml.org/doc/278746)).

## 3. Strong Goldbach: one selector encodes the full histogram

### Declared proposition

For a finite block of `B` even targets, let `A_i` be the number of Goldbach
representations of target `i`. Put `b=B+1`, `U=max A_i`, and

```text
h_a = number of i for which A_i=a,
E   = sum_i b^(-A_i).
```

Then

```text
b^U E = sum_(a=0)^U h_a b^(U-a).
```

Because `0<=h_a<=B<b`, the base-`b` digits of this integer recover the entire
representation-count histogram. The leading digit `h_0` is the number of
Goldbach exceptions, while the later digits identify the weakest represented
targets and every other multiplicity layer.

### Proof

Group equal exponents in `E` and multiply by `b^U`. Each histogram coefficient
is already a valid base-`b` digit, so no carry occurs. Uniqueness of finite
radix expansions gives exact recovery.

The generator reconstructs every histogram for dyadic starts
`128, 512, 2048, 8192, 32768`. Their exception digit is zero, and the full
packed integers are committed by bit length and SHA-256 digest.

### No-go and limit

This is lossless encoding, not a new arithmetic estimate. It starts from the
exact counts. Moreover, the count vectors `[1,M]` and `[1,M+1]` have different
histograms but selector distance

```text
(b-1)/b^(M+1).
```

Thus fixed absolute precision cannot recover histogram digits at unbounded
depth. The unresolved theorem is an independent interval estimate that proves
the zero digit is absent on every future block. Exceptional-set results do not
make the set empty; this ticket does not improve the circle method. See, for
context, Li's published exceptional-set paper
([Quarterly Journal of Mathematics](https://academic.oup.com/qjmath/article-pdf/50/200/471/4354525/500471.pdf)).

## 4. Twin Prime: a quantitative Abel-to-count bracket

### Declared proposition

Let `a_n` be supported on odd integers with `0<=a_n<=1`, and define

```text
T(Y) = sum_(n<=Y) a_n,
F(r) = sum_n a_n r^n.
```

For `Y>=X` and `n0` the first odd integer above `Y`,

```text
r^X T(X) <= F(r) <= T(Y) + r^n0/(1-r^2).
```

Therefore any certified lower bound `L<=F(r)` yields

```text
T(Y) >= ceil(L - r^n0/(1-r^2)).
```

### Proof

For `n<=X`, `r^n>=r^X`, proving the lower bound. The terms through `Y` are at
most `T(Y)`. Replacing every later odd coefficient by one gives the displayed
geometric tail. Rearrangement and integrality of `T(Y)` complete the transfer.

For the twin-prime indicator and `r_X=1-1/X`, bounded computations recover
valid lower bounds `9, 35, 190, 1149` for `T(10X)` at
`X=100,1000,10000,100000`. These use known finite twin support and do not
establish an unseen pair.

### Fixed-dilation no-go

At `r_X=1-1/X` and `Y=cX`, the coefficient-one tail is asymptotic to

```text
(X/2) exp(-c).
```

For fixed `c`, this is order `X`, so this bracket alone cannot transfer an
`X/log^2 X` lower bound. A schedule

```text
Y/X = 2 log log X + omega(1)
```

makes the geometric tail `o(X/log^2 X)`. This does not break the parity
barrier; it only identifies the horizon at which a future parity-sensitive
Abel lower bound would become count-effective. Polymath8 explicitly records
the limit of purely sieve-theoretic bounded-gap methods
([arXiv:1407.4897](https://arxiv.org/abs/1407.4897)).

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket216_laplace_gcd_radix_tauberian.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket216_laplace_gcd_radix_tauberian -v
```

Primary machine artifact:

```text
data/open-problem/ticket216-laplace-gcd-radix-tauberian.json
```

Per-problem artifacts are stored under `data/open-problem/{problem}/`.

## Final status

| Problem | New result | Resolution status | Discarded path | Remaining proof gap | Next single lemma |
| --- | --- | --- | --- | --- | --- |
| Riemann | first-atom Laplace certificate | open | fixed tolerance | actual-zeta cofinal transform upper bound | `CofinalActualZetaOffLineLaplaceUpperBoundsBelowFirstAtomThreshold` |
| Collatz | exact cross-power gcd necessity | open | finite diagonal promotion | all-`k` gcd gap plus multi-run bridge | `UniformStrictCrossPowerGCDGapAtEverySingleMountainCrossing` |
| Goldbach | full radix histogram recovery | open | encoding as proof | independent zero-digit interval on every block | `ArithmeticRadixSelectorIntervalSeparatesTheZeroDigitOnEveryDyadicBlock` |
| Twin Prime | quantitative Abel-count bracket | open | fixed-dilation tail transfer | parity-breaking adaptive-tail domination | `ParityBreakingAbelLowerBoundDominatesAdaptiveGeometricTail` |
