# TICKET-201: Finite Information, All-Run Collatz, and Liouville Parity

## Abstract

TICKET-201 continues PrimeProject's simultaneous proof-or-counterexample program
for the Riemann Hypothesis, the Collatz conjecture, the strong Goldbach
conjecture, and the Twin Prime conjecture. It resolves none of them. Its purpose
is to audit whether the next lemmas left by TICKET-200 are genuine intermediate
steps. The audit proves four exact partial results:

1. finite-order jet data on one compact set cannot force a global real-zero
   property in the ambient class of real-even entire functions;
2. every scale, every run-pair count, and every cyclic rotation of one explicit
   two-parameter Collatz family fails affine divisibility;
3. the Goldbach prime and semiprime channels are exact Liouville-sign
   projectors, making the previous semiprime-elimination target equivalent to
   Goldbach wherever the Chen channel is positive; and
4. the corresponding dyadic identity makes the previous Twin target equivalent
   to the Twin Prime conjecture itself.

The machine-readable record is
[`ticket201-finite-information-allrun-liouville-parity.json`](../data/open-problem/ticket201-finite-information-allrun-liouville-parity.json).
Every parent status is `open_not_proven`; the conjecture resolution count is
zero.

## Result table

| Problem | Exact new result | Route rejected or limited | Single next lemma |
|---|---|---|---|
| Riemann Hypothesis | `FiniteCompactJetDataCannotForceGlobalRealZeroProperty` | one fixed compact Xi jet certificate implies RH | `CofinalXiRectangleRoucheMarginFromCompletedZetaStructure` |
| Collatz | `AllRunPairPrimitiveFamilyAffineDivisibilityObstruction` | increasing one fixed repetition count at a time | `UniformBoundedL1NeighborhoodAffineObstructionAtOneThirdDensity` |
| Strong Goldbach | `GoldbachP2LiouvilleParitySaturationEquivalence` | semiprime-only Chen elimination is a proper easier lemma | `UniformRelativeLiouvilleParityDefectOnPrimePlusP2GoldbachChannels` |
| Twin Prime | `TwinP2LiouvilleParitySaturationEquivalence` | infinitely many twin-positive Chen blocks is a proper easier lemma | `UniformRelativeLiouvilleParityDefectOnInfinitelyManyChenDyadicBlocks` |

## 1. Riemann track: a finite-information no-go theorem

Let `F` be a real-even entire function. Fix `R>0`, a finite derivative order
`M`, `epsilon>0`, and `A>R` with `F(iA) != 0`. For a positive integer `N`, set

```text
G_N(z) = F(z) - F(iA) z^(2N) / (iA)^(2N).
```

### Proposition RH-201

For all sufficiently large `N`, the function `G_N` is real-even and entire,
has non-real zeros at `+iA` and `-iA`, and obeys

```text
max_{|z|<=R, 0<=j<=M} |G_N^(j)(z)-F^(j)(z)| < epsilon.
```

### Proof

The value `F(iA)` is real because the Taylor series of a real-even entire
function has real coefficients and only even powers. The perturbation
coefficient is therefore real. Substitution gives `G_N(iA)=0`, and evenness
gives the second zero. On the compact disk,

```text
|G_N^(j)(z)-F^(j)(z)|
 <= |F(iA)| (2N)_j R^(2N-j) / A^(2N).
```

For each fixed `j`, the polynomial factor `(2N)_j` is dominated by the
geometric factor `(R/A)^(2N)`. The maximum over the finite set
`j=0,...,M` therefore tends to zero. This proves the proposition.

In particular, when `F` itself has only real zeros, the construction produces
arbitrarily close finite-jet data with prescribed non-real zeros. The exact
regression makes this non-vacuous by using `F(z)=z^2-1`, whose only zeros are
`-1` and `1`, with `R=5`, `A=10`, `M=2`, and `epsilon=1/100`. The first
successful value is `N=9`; its three derivative bounds are `101/262144`,
`909/655360`, and `15453/3276800`.

### Limit and route correction

This is not an RH counterexample. The perturbation preserves real-even
symmetry, entire-ness, and order at most one, but it does not preserve Xi's
gamma factor, Dirichlet series, functional equation as a completed zeta
function, or Euler-product origin. The result instead proves that TICKET-200's
fixed `D3` jet certificate cannot be a global RH bridge by local data alone.
The surviving route must be cofinal in height and must use completed-zeta
structure, not just compact approximation.

The rigorous finite-height boundary remains the interval-arithmetic
verification of Platt and Trudgian through height `3*10^12`; a finite-height
verification, however large, is not the universal statement.

## 2. Collatz track: all repetition counts at once

For integers `r>=2` and `k>=2`, define the accelerated-Collatz exponent word

```text
w_(r,k) = 1^k 2^(2k) (1 2^2)^(r-1).
```

Put `n=r-1`, `q=k+n`, `x=32^k`, `y=27^k`, and `z=18^k`.

### Proposition CO-201

Every `w_(r,k)` and every cyclic rotation passes both scalar gates but fails
the affine divisibility equation. Hence this complete two-parameter family
contains no positive Collatz cycle code.

### Proof

For the tail block `U=(1,2,2)`, exact concatenation gives

```text
N(U^n) = 23(32^n-27^n)/5,
D       = 32^(n+k)-27^(n+k),
B       = ((23*32^n-18*27^n)/5)x + 27^n y - 2*27^n z.
```

Eliminating `B` and `D` yields the master identity

```text
5B-23D = 2*27^n E_k,
E_k    = 14*27^k-9*32^k-5*18^k = -F_k.
```

Here `F_2=630`. For `k>=3`,

```text
14(27/32)^k < 14(27/32)^3 < 9,
```

so `F_k>0`. Also `D>=32^(k+1)-27^(k+1)` and

```text
32^(k+1)-27^(k+1)-F_k
  = 23*32^k-13*27^k-5*18^k > 0.
```

Thus `0<|E_k|=F_k<D`. The denominator is odd and coprime to `3`, so
`gcd(D,2*27^n)=1`. If `D` divided `B`, the master identity would force
`D|E_k`, a contradiction.

The unique run `2^(2k)` proves primitivity. Under one cyclic rotation the
numerators satisfy `2^v B'=3B+D`; because `gcd(D,6)=1`, divisibility is
rotation invariant. Finally `h=3q` and `S=5q`, so the two scalar gates reduce
to positive powers of `32/27` and `125/108`.

The computation checks all `225` pairs `2<=r,k<=16` plus every rotation, with
zero identity or divisibility failures. The grid is regression evidence; the
displayed inequalities prove the infinite parameter range.

### Limit and next lemma

This closes one rigid family, not arbitrary exponent words and not divergent
orbits. Repeating the same calculation for `r=4,5,...` is now discarded as
redundant. The next target asks whether the obstruction survives a fixed
`L1` neighborhood of the family among primitive words with `h=3q` and `S=5q`.

## 3. Goldbach track: exact Liouville saturation

Let `J(n)` indicate that `n` is either prime or a composite semiprime, and let
`lambda(n)=(-1)^Omega(n)`. On the support of `J`,

```text
I_prime(n)     = J(n)(1-lambda(n))/2,
I_semiprime(n) = J(n)(1+lambda(n))/2.
```

For even `N`, sum over prime first summands and define

```text
C(N) = sum_p J(N-p),
L(N) = sum_p J(N-p)lambda(N-p).
```

### Proposition GB-201

If `R(N)` and `S(N)` are the prime-prime and prime-composite-semiprime
channels, then exactly

```text
R(N) = (C(N)-L(N))/2,
S(N) = (C(N)+L(N))/2.
```

Consequently, at every target with `C(N)>0`, semiprime-only saturation is
equivalent to `L(N)=C(N)`, while Goldbach positivity is equivalent to
`L(N)<C(N)`.

This follows immediately by summing the two exact projectors. In particular,
TICKET-200's proposed statement that every Chen-positive target avoids the
semiprime-only channel is Goldbach itself on those targets, not a smaller
independent lemma.

The finite regression checks 16 selected even targets through `2^20`. At
`N=2^20`, it obtains `R=8478`, `S=22602`, `C=31080`, and `L=14124`, satisfying
`C-L=2R`. No sampled target saturates `L=C`; this finite observation is not a
proof for larger targets.

The corrected next target is a quantitative signed estimate: find explicit
`delta>0` and `N0` such that

```text
L(N) <= (1-delta) C(N)
```

for every relevant even `N>=N0`. This is stronger than mere positivity and
states precisely what unsigned P2 support cannot provide.

## 4. Twin Prime track: the dyadic parity identity

For primes `p` in `[X,2X)`, define

```text
C2(X) = sum J(p+2),
L2(X) = sum J(p+2)lambda(p+2).
```

### Proposition TP-201

If `T(X)` counts twin starts and `S(X)` counts prime-composite-semiprime
starts, then

```text
T(X) = (C2(X)-L2(X))/2,
S(X) = (C2(X)+L2(X))/2.
```

A Chen-positive block contains a twin exactly when `L2<C2`. Infinitely many
twin primes exist exactly when this strict inequality holds on infinitely many
dyadic blocks. The forward direction follows because infinitely many twin
starts occupy infinitely many finite blocks; the reverse direction supplies a
distinct twin start in each of infinitely many blocks.

Thus TICKET-200's proposed next lemma was the Twin Prime conjecture rewritten
in dyadic channel language. It is reclassified, not proved. The 13-block
regression ends at `[2^22,2^23)`, where `T=22643`, `S=65808`, `C2=88451`, and
`L2=43165`. Finite positive blocks do not establish infinitude.

The corrected target is to prove an explicit `delta>0` with

```text
L2(X) <= (1-delta) C2(X)
```

on infinitely many unbounded Chen-positive dyadic blocks.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket201_finite_information_allrun_liouville_parity.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket201_finite_information_allrun_liouville_parity
```

The generator writes one integrated JSON record and four problem-specific
records. Exact integers and rational strings are used for every new identity;
floating-point evidence is not used as a proof premise.

## Literature boundary

- Platt and Trudgian rigorously verified RH to finite height using interval
  arithmetic: <https://arxiv.org/abs/2004.09765>.
- The Polymath Selberg-sieve analysis gives a primary reference for the parity
  obstruction in bounded-gap methods: <https://arxiv.org/abs/1407.4897>.
- Pintz discusses Chen primes and the parity phenomenon near Twin Prime:
  <https://arxiv.org/abs/1004.1065>.
- Bordignon, Johnston, and Starichkova give an explicit Chen theorem:
  <https://arxiv.org/abs/2207.09452>.

PrimeProject imports those boundaries. It claims no novelty for the classical
parity barrier, the Liouville function, or finite-height verification. The new
project-local contributions in this ticket are the exact all-run family
identity, its proof audit, and the explicit reclassification of prior proof
obligations.
