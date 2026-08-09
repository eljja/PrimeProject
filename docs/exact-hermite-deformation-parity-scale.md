# TICKET-202: Exact Hermite Data, Long-Run Deformations, and Parity Scale

## Abstract

TICKET-202 continues PrimeProject's simultaneous proof-or-counterexample
program for the Riemann Hypothesis, the Collatz conjecture, the strong Goldbach
conjecture, and the Twin Prime conjecture. It resolves none of them. It proves
four exact partial results and corrects the scale of two targets left by
TICKET-201:

1. finitely many exact Hermite constraints, even when combined with compact
   finite-jet control, cannot force a global real-zero property in the ambient
   class of real-even entire functions;
2. every parameter choice and cyclic rotation in the three-parameter Collatz
   family `1^k 2^(2k+t) (1 2^2)^(r-1)` fails affine divisibility;
3. the full Goldbach `P2` channel has an aggregate relative Liouville defect
   tending to zero, so a fixed positive pointwise relative defect cannot hold;
4. a fixed relative Twin defect, when paired with Chen-order channel mass,
   implies a Hardy-Littlewood-order quantitative twin lower bound and is
   strictly stronger than infinitude at the level of channel algebra.

The canonical machine-readable record is
[`ticket202-exact-hermite-deformation-parity-scale.json`](../data/open-problem/ticket202-exact-hermite-deformation-parity-scale.json).
Every conjecture status remains `open_not_proven`, and the resolution count is
zero.

## Result table

| Problem | Exact new result | Route rejected or recalibrated | Single next lemma |
|---|---|---|---|
| Riemann Hypothesis | `ExactFiniteHermiteAndCompactJetGlobalZeroNoGo` | finitely many exact Xi Hermite constraints close the finite-information gap | `CompletedZetaCofinalContourMarginWithExactZeroCountTransfer` |
| Collatz | `AllLongRunExtensionsPrimitiveFamilyAffineObstruction` | checking each central-run extension separately | `SignedTwoSiteValuationTransferAffineObstruction` |
| Strong Goldbach | `DyadicP2RelativeLiouvilleDefectDilutionNoGo` | a fixed positive relative defect in the full `P2` channel | `PointwiseLogLogScaledLiouvilleDefectOnEveryLargeEvenInteger` |
| Twin Prime | `RelativeChenDefectQuantitativeTwinStrengthCalibration` | a fixed relative Chen defect is only an infinitude-level lemma | `PrimeSemiprimeSeparatedChenSwitchingWeightWithPositivePrimeCoefficient` |

## 1. Riemann track: exact finite Hermite data still do not globalize

Let `F` be a real-even entire function. Fix a compact disk `|z|<=R`, a
finite symmetric set of real interpolation nodes, finitely many derivative
orders at those nodes, and a point `iA` with `A>R` and `F(iA) != 0`.

For positive nodes `a_l` and required derivative orders `m_l`, define

```text
P(z)   = product_l (z^2-a_l^2)^(m_l+1),
H_N(z) = z^(2N) P(z),
G_N(z) = F(z) - F(iA) H_N(z)/H_N(iA).
```

The even power at zero is chosen large enough to preserve all requested
derivatives there.

### Proposition RH-202

Every requested Hermite value of `G_N` equals that of `F` exactly. The function
`G_N` is real-even and entire, has non-real zeros at `+iA` and `-iA`, and for
every fixed finite derivative order `M`,

```text
max_{|z|<=R, 0<=j<=M} |G_N^(j)(z)-F^(j)(z)| -> 0.
```

### Proof

Each factor `(z^2-a_l^2)^(m_l+1)` has the required multiplicity at both
`+a_l` and `-a_l`; `z^(2N)` handles the node zero. Thus the perturbation and
all prescribed derivatives vanish at every node. Since `H_N(iA)` and `F(iA)`
are real, the coefficient is real and the perturbation remains real-even.
Substitution gives `G_N(iA)=0`, and evenness gives the second zero.

Write `H_N=z^(2N)P` with fixed `P`. Leibniz's rule bounds every fixed
derivative of `H_N/H_N(iA)` on the disk by a polynomial in `N` times
`(R/A)^(2N)`. The geometric factor dominates, proving uniform convergence.

The exact regression uses

```text
F(z)=z^2-1,
P(z)=(z^2-1)^3(z^2-4)^3,
nodes={-2,-1,0,1,2}, derivatives j=0,1,2,
R=5, A=10, epsilon=1/100.
```

The first successful value is `N=3`. The exact coefficient is
`-1/11474737664000000`; the largest disk bound is
`224180121/35306885120 < 1/100`. All fifteen node-derivative constraints are
exactly zero for the perturbation.

### Boundary

This is not an RH counterexample. `G_N` is not Xi and need not preserve the
gamma factor, Dirichlet series, functional equation as a completed zeta
function, or Euler-product origin. The result closes an exact-interpolation
loophole: no finite augmentation of one compact local certificate is enough in
the ambient symmetry class. The surviving route must be cofinal and
completed-zeta-specific.

## 2. Collatz track: an unbounded deformation ray

For integers `r>=2`, `k>=2`, and `t>=0`, define the accelerated exponent word

```text
w_(r,k,t) = 1^k 2^(2k+t) (1 2^2)^(r-1).
```

Put `n=r-1` and `q=k+n`.

### Proposition CO-202

Every `w_(r,k,t)` and every cyclic rotation fails the affine divisibility
equation required by a positive Collatz cycle.

### Exact identity

If `B` is the ordered affine numerator and `D=2^S-3^h`, then

```text
D = 4^t 32^q - 3^t 27^q,

5B-23D
 = 2*27^n E_(k,t),

E_(k,t)
 = 14*3^t*27^k - 5*3^t*18^k - 9*4^t*32^k
 = -F_(k,t).
```

For all allowed parameters,

```text
0 < F_(k,t) < D.
```

For `t=0`, this is the TICKET-201 residual inequality. For `t>=1`, the
negative `9*4^t*32^k` term already dominates the positive term at the worst
case `(t,k)=(1,2)`, and the dominance increases thereafter. Moreover,

```text
D-F_(k,t)
 >= 23*4^t*32^k - 13*3^t*27^k - 5*3^t*18^k > 0.
```

The denominator is coprime to `6*27^n`. If `D` divided `B`, the master identity
would force `D` to divide `E_(k,t)`, contradicting the strict bound. The unique
long `2`-run proves primitivity. The rotation recurrence preserves the
divisibility obstruction.

The finite regression contains `729` independent rows:
`2<=r,k<=10`, `0<=t<=8`, with every cyclic rotation checked. It is a
regression for the symbolic theorem, not its quantifier proof.

### Boundary

This closes an unbounded one-sided `L1` deformation ray from each TICKET-201
word. It does not cover shortening the run, moving valuation mass between two
positions, arbitrary multisite perturbations, arbitrary exponent words, or
nonperiodic divergence. The next algebraic target is a signed two-site transfer
identity.

## 3. Goldbach track: the fixed relative defect has the wrong scale

For even `N`, retain TICKET-201's ordered channel counts

```text
C(N)=R(N)+S(N),
L(N)=S(N)-R(N),
C(N)-L(N)=2R(N),
```

where `R` is the prime-prime channel and `S` is the
prime-composite-semiprime channel. Sum them over even `N` in `(X,2X]` to obtain
`R_X`, `S_X`, `C_X`, and `L_X`.

### Proposition GB-202

Using the prime number theorem and Landau's theorem for integers with exactly
two prime factors,

```text
R_X / S_X = O(1/log log X),

(C_X-L_X)/C_X = 2R_X/(R_X+S_X) -> 0.
```

Consequently there is no fixed `delta>0` such that

```text
L(N) <= (1-delta) C(N)
```

for every sufficiently large Chen-positive even `N`.

### Proof

The crude upper bound `R_X<=pi(2X)^2` is `O(X^2/log^2 X)`. For a lower bound on
`S_X`, restrict both the first odd prime `p` and the odd composite semiprime
`m` to `(X/2,X]`. Then `p+m` lies in `(X,2X]`. PNT gives asymptotically
`X/(2 log X)` choices for `p`. Landau's theorem gives asymptotically
`X log log X/(2 log X)` odd semiprimes in the same interval; even semiprimes
are lower order. Therefore

```text
S_X = Omega(X^2 log log X/log^2 X).
```

The exact projector identity proves the aggregate limit. If a fixed pointwise
`delta` held eventually, summing it over every sufficiently large dyadic block
would give an aggregate defect at least `delta`, a contradiction.

The exact finite regression covers blocks `[2^10,2^11]` through
`[2^20,2^21]`. The observed defect decreases from `25598/36655` to
`18844127294/35051527549`. This monotone finite behavior is not used to prove
the asymptotic theorem.

### Boundary and corrected target

This no-go does not refute Goldbach. A relative defect can tend to zero while
remaining positive at every integer. The corrected natural scale is roughly
`1/log log N`; TICKET-202 proves no pointwise lower bound at that scale and
does not remove a sparse exceptional set. The next target is therefore a
pointwise, log-log-scaled signed estimate rather than a fixed relative margin.

## 4. Twin Prime track: a fixed defect is much stronger than infinitude

For a dyadic block, TICKET-201 proved

```text
C2(X)-L2(X)=2T(X),
```

where `T(X)` counts twin starts and `C2(X)` counts twin or
prime-composite-semiprime starts. Define

```text
delta_X = 1-L2(X)/C2(X) = 2T(X)/C2(X).
```

### Proposition TP-202

If, on infinitely many blocks,

```text
C2(X) >= a X/(log_2 X)^2
and
delta_X >= d > 0,
```

then on those blocks

```text
T(X) >= (ad/2) X/(log_2 X)^2.
```

Thus a fixed relative defect combined with Chen-order mass is a quantitative
Hardy-Littlewood-order lower bound, not merely an infinitude-level lemma.

### Proof and exact non-implication model

The displayed lower bound follows immediately by multiplying
`T=(delta_X/2)C2`. To show that channel algebra plus twin positivity does not
force fixed `delta`, let

```text
T(X)=1,
C2(X)=floor(X/(log_2 X)^2),
L2(X)=C2(X)-2.
```

Then `C2-L2=2T` and every block is twin-positive, but
`delta_X=2/C2(X)->0`. This is a logical channel countermodel, not a model of
the primes and not a Twin Prime proof.

The actual finite regression covers thirteen blocks through `[2^22,2^23)` and
checks the normalized transfer identity exactly. The abstract regression uses
twenty-one blocks through `X=2^30`.

### Boundary and corrected mechanism

TICKET-202 neither proves nor refutes a fixed relative defect for actual prime
channels. It proves that treating the target as a modest intermediate lemma
understates its strength. The next useful mechanism is a parity-sensitive
switching weight that separates prime from semiprime mass while tolerating a
vanishing relative defect.

## Reproducibility

```powershell
D:\python\anaconda3\python.exe scripts\ticket202_exact_hermite_deformation_parity_scale.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket202_exact_hermite_deformation_parity_scale -v
```

The generator writes an integrated artifact and four per-problem artifacts.
All polynomial coefficients, Hermite evaluations, Collatz integers, channel
counts, relative defects, and proof DAGs are serialized.

## Literature boundary

- Dave Platt and Tim Trudgian, [The Riemann hypothesis is true up to
  `3*10^12`](https://arxiv.org/abs/2004.09765), remains rigorous finite-height
  context. No new Xi zero is computed here.
- Edmund Landau, [*Handbuch der Lehre von der Verteilung der
  Primzahlen*](https://doi.org/10.1007/BF01742852), supplies the classical
  `Omega(n)=2` counting asymptotic used in GB-202.
- Lasse Grimmelt and Gautami Bhowmik, [The exceptional set of the Goldbach
  problem](https://arxiv.org/abs/2607.27282), gives current exceptional-set and
  explicit-major-arc context but not the pointwise theorem left open here.
- Jing-Run Chen, [On the representation of a large even integer as the sum of
  a prime and the product of at most two
  primes](https://doi.org/10.1360/YA1973-16-2-157), supplies Chen's classical
  almost-prime context.
- Kaisa Matomaki and Sebastian Zuniga Alterman, [Weighted sieves with
  switching](https://arxiv.org/abs/2405.19063), is current adjacent context for
  the surviving Twin switching-weight route; it does not prove the required
  prime/semiprime separation.

The Hermite perturbation and channel-strength identities are elementary. The
Collatz family identity is project-local. No academic priority claim is made
without independent expert review.

## Final boundary

TICKET-202 proves four partial theorems, records four route decisions, supplies
four proof DAGs, and leaves all four conjectures open. It does not contain a
complete proof or a counterexample to any parent problem.
