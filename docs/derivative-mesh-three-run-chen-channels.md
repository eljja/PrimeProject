# TICKET-200: Derivative Meshes, a Three-Run Obstruction, and Chen Channels

## Abstract

TICKET-200 continues PrimeProject's simultaneous proof-or-counterexample program
for the Riemann Hypothesis, the Collatz conjecture, the strong Goldbach
conjecture, and the Twin Prime conjecture. It resolves none of them. It proves
four narrower statements:

1. a derivative-controlled finite boundary mesh is sufficient to propagate a
   strict Rouche margin over the complete boundary of the project rectangle;
2. every scale and cyclic rotation of one explicit primitive three-run-pair
   Collatz family fails the affine divisibility equation;
3. an explicit form of Chen's theorem splits exactly into Goldbach and
   composite-semiprime channels, reducing every possible large counterexample
   to the second channel; and
4. Chen's prime-plus-`P2` infinitude similarly splits into Twin Prime and
   composite-semiprime channels, making the remaining parity obstruction
   explicit.

The machine-readable record is
[`ticket200-derivative-mesh-three-run-chen-channels.json`](../data/open-problem/ticket200-derivative-mesh-three-run-chen-channels.json).
All four parent statuses remain `open_not_proven`, and the conjecture resolution
count is zero.

## Claim table

| Problem | Exact TICKET-200 result | Route rejected or limited | Single next lemma |
|---|---|---|---|
| Riemann Hypothesis | `DerivativeControlledBoundaryMeshRoucheCertificate` | floating or pointwise Xi margins without outward-rounded derivative and tail bounds | `OutwardRoundedXiTaylorRemainderAndDerivativeBoundsInstantiateD3MeshCertificate` |
| Collatz | `ThreeRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales` | retaining the explicit `r=3` family as a positive-cycle candidate | `FourRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales` |
| Strong Goldbach | `ChenGoldbachPrimeSemiprimeChannelReduction` | inferring prime-plus-prime positivity from Chen prime-plus-`P2` positivity | `SemiprimeOnlyChenGoldbachChannelIsEmptyForEveryEvenNAboveExp36` |
| Twin Prime | `ChenTwinPrimeSemiprimeChannelReduction` | identifying infinitely many Chen primes with infinitely many twin primes | `TwinChannelPositiveOnInfinitelyManyChenPositiveDyadicBlocks` |

## 1. Riemann track: closing the mesh-propagation implication

### Proposition RH-200

Partition the polygonal boundary of

```text
D_3^+ = {x+iy : -3 <= x <= 3, 1/3 <= y <= 3}
```

into straight segments of length at most `h`, sampling both endpoints. Let `P`
and `R` be analytic on a neighbourhood of the closed rectangle. Suppose

```text
|P(s)| - |R(s)| >= eta                      at every mesh node s,
sup_boundary (|P'(z)| + |R'(z)|) <= L,
eta - Lh/2 > 0.
```

Then `|R(z)| < |P(z)|` on the entire boundary. Consequently `P` and `P+R`
have the same number of zeros in `D_3^+`, counted with multiplicity.

### Proof

Every point `z` on a mesh segment is within `h/2` of one endpoint `s`. Integrate
`P'` and `R'` along the straight subsegment from `s` to `z`. Then

```text
|P(z)-P(s)| + |R(z)-R(s)| <= L |z-s| <= Lh/2.
```

The reverse triangle inequality gives

```text
|P(z)| - |R(z)|
  >= |P(s)| - |R(s)| - |P(z)-P(s)| - |R(z)-R(s)|
  >= eta - Lh/2
  > 0.
```

The strict boundary inequality is precisely the hypothesis needed for Rouche's
theorem. This proves the proposition.

### Exact regression instance

The generator uses `P(z)=20+z^2` and `R(z)=1/4` on the same `D_3^+` boundary.
There, `Re(P)=20+x^2-y^2 >= 11`, so every node has the exact conservative margin
`eta=43/4`. Also `|P'|=2|z|<=2(|x|+|y|)<=12`, hence `L=12`. Four segments per
edge give `h=3/2` and

```text
eta - Lh/2 = 43/4 - 9 = 7/4 > 0.
```

The exact rational audit checks segment counts `2, 4, 8, 16`; the first is too
coarse for this certificate and the last three certify it.

### Limit

This proves the propagation lemma requested by TICKET-199, not an RH rectangle.
The regression functions are synthetic, not Xi. The missing work is an
outward-rounded interval enclosure for an Xi Taylor polynomial, its remainder,
and both derivatives on every boundary segment. High-precision floating-point
samples are not substitutes for those enclosures.

## 2. Collatz track: the explicit three-run-pair family

For `k>=2`, define the accelerated-Collatz exponent word

```text
w_k = 1^k 2^(2k) (1 2^2)^2.
```

It has three one-runs and three two-runs. Put

```text
x=32^k, y=27^k, z=18^k.
```

### Proposition CO-200

Every `w_k`, and every cyclic rotation of it, passes the contraction and product
gates but fails the affine divisibility equation. Thus this explicit infinite
family contains no positive Collatz cycle code.

### Closed form

If `N(A)` is the ordered affine numerator of a word `A`, concatenation satisfies

```text
N(A || B) = 3^len(B) N(A) + 2^sum(A) N(B).
```

The earlier family `A=1^k2^(2k)` has `N(A)=x+y-2z`, while direct evaluation
gives `N((122)^2)=1357`. Therefore

```text
D = 1024x - 729y,
B = 2086x + 729y - 1458z.
```

For `k>=7`, set

```text
R = B-2D = 38x + 2187y - 1458z.
```

The quantity `R` is positive. Moreover

```text
D-R = 986x - 2916y + 1458z.
```

After division by `x`, its forward difference has the sign of

```text
10(27/32)^k - 14(18/32)^k,
```

which is positive for every `k>=1`. At `k=7`, `D-R=4,268,928,897,556>0`.
Hence `0<R<D`, or equivalently `2D<B<3D`, for every `k>=7`. The exact
nonzero residues `B mod D` for `k=2,...,6` are

```text
126573, 16583324, 362731012, 6001752716, 21418884868.
```

Thus `D` never divides `B`.

The run `2^(2k)` is the unique two-run of length at least four, so the word
cannot be a proper power and is primitive. Moving a first valuation `v` to the
end transforms numerators by

```text
2^v B' = 3B + D.
```

Since `D` is coprime to `6`, `D|B` if and only if `D|B'`. The obstruction is
therefore invariant under all cyclic rotations. Finally, with `q=k+2`, the word
has `h=3q`, `S=5q`, and `q` entries equal to one. The two scalar gates reduce to
`32^q>27^q` and `(125/108)^q>1`.

### Limit

The theorem closes one structured `r=3` family only. It does not cover all
three-run-pair words, arbitrary fixed run counts, nonperiodic divergent
trajectories, or the full Collatz conjecture.

## 3. Goldbach track: exact Chen channels

Let `I_P(n)` be the prime indicator and let `I_2(n)` indicate composite numbers
having exactly two prime factors counted with multiplicity, including squares.
For even `N`, define the ordered channels

```text
R(N) = sum_a I_P(a) I_P(N-a),
S(N) = sum_a I_P(a) I_2(N-a),
C(N) = R(N) + S(N).
```

### Proposition GB-200

The identity `C=R+S` is a disjoint exact support decomposition. Bordignon's
explicit version of Chen's theorem states that every even `N>exp(36)` is a
prime plus a product of at most two primes. Hence `C(N)>0` there. Consequently,
any Goldbach counterexample above that threshold, if one exists, must obey

```text
R(N)=0 < S(N).
```

That is, it must be a semiprime-only Chen target.

### Proof and no-go statement

A product of at most two primes is either prime or a composite semiprime, and
the two cases are disjoint. Splitting the second summand of every Chen
representation proves the identity. Chen positivity then proves the stated
conditional classification.

It does **not** prove `R(N)>0`. The exact logical model `R=0, S=1, C=1` satisfies
`C=R+S` and `C>0` while failing `R>0`. This is a countermodel to the inference,
not an arithmetic Goldbach counterexample.

The sieve regression scans all `524,287` even targets through `2^20`. It finds
zero Goldbach failures, zero Chen failures, and zero semiprime-only targets in
that finite range. These counts validate the implementation only; they do not
eliminate the channel above the finite cutoff.

### Limit

The decisive next statement is that the semiprime-only channel is empty for
every even `N>exp(36)`. Given the imported Chen theorem, that statement would
close strong Goldbach above the explicit threshold, followed by a finite base
check. TICKET-200 does not prove it.

## 4. Twin Prime track: the same parity channel at fixed shift

For a dyadic block `[X,2X)`, let

```text
T_0(X) = #{p in [X,2X): p and p+2 are prime},
S_2(X) = #{p in [X,2X): p is prime and p+2 is a composite semiprime},
C_2(X) = T_0(X) + S_2(X).
```

### Proposition TP-200

The supports of `T_0` and `S_2` are disjoint. Chen's theorem implies that
`C_2(X)>0` for infinitely many dyadic `X`. The squarefree-Lambda detector from
TICKET-199 is positive exactly when `T_0(X)>0`. Therefore the remaining Twin
Prime obligation is not Chen positivity but proof that the composite-semiprime
channel does not exhaust all infinitely many Chen-positive blocks.

### Proof and no-go statement

Every Chen prime has `p+2` either prime or composite semiprime, giving the exact
decomposition. Infinitely many Chen primes are unbounded and therefore meet
infinitely many dyadic blocks. TICKET-199's nonnegative weighted detector has
the same support as `T_0`.

Again, `T_0=0, S_2=1, C_2=1` is an exact countermodel to the implication
`C_2>0 => T_0>0`; it is not a Twin Prime counterexample. The computation checks
13 blocks from `[2^10,2^11)` through `[2^22,2^23)`. In the last block it finds
`22,643` twin starts and `65,808` prime-composite-semiprime starts. Finite
positive blocks do not establish infinitude.

### Limit

This reduction exposes the sieve parity barrier in the exact detector language
of the project. It does not cross it. The next lemma must force the twin channel
to be positive on infinitely many Chen-positive blocks.

## Reproducibility

```powershell
D:\python\anaconda3\python.exe scripts\ticket200_derivative_mesh_three_run_chen_channels.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket200_derivative_mesh_three_run_chen_channels -v
```

The generator writes the integrated record plus one per-problem JSON artifact.
All integers and rational mesh bounds used in the proofs are serialized.

## Literature boundary

- Dave Platt and Tim Trudgian, [The Riemann hypothesis is true up to
  `3*10^12`](https://arxiv.org/abs/2004.09765), supplies the rigorous
  finite-height RH context. TICKET-200 performs no new zero verification.
- Carlos Fernandez and Santiago Ibanez,
  [Christoffel words as extremal structures in Collatz
  dynamics](https://arxiv.org/abs/2607.24844), is a 2026 preprint providing
  current adjacent work on cyclic words. TICKET-200's family calculation is
  narrower and makes no literature-priority claim.
- Matteo Bordignon, [An explicit version of Chen's
  theorem](https://doi.org/10.1017/S0004972721001301), supplies the explicit
  `exp(36)` Goldbach-side threshold.
- Jing-Run Chen, [On the representation of a large even integer as the sum of a
  prime and the product of at most two
  primes](https://doi.org/10.1360/YA1973-16-2-157), supplies the imported
  prime-plus-`P2` results.
- Lasse Grimmelt and Gautami Bhowmik, [The exceptional set of the Goldbach
  problem](https://arxiv.org/abs/2607.27282), is current 2026 context on
  exceptional-set and major-arc analysis. It is not used as a proof premise.

The mesh implication, channel identities, and logical countermodels are
elementary or project-local. No claim of academic novelty or priority is made
without independent expert review.

## Final boundary

TICKET-200 records four exact partial theorems, four limited or invalid
inferences, four proof DAGs, and four single next lemmas. It proves no complete
conjecture and exhibits no counterexample to one. Its main contribution is a
sharper map of the remaining obligations: one Xi interval enclosure, one next
Collatz run family, one pointwise Goldbach semiprime-channel exclusion, and one
parity-breaking Twin Prime channel theorem.
