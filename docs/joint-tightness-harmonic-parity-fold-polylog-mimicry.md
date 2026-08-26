# TICKET-244: Joint Tightness, Harmonic Bad Lines, Parity Folding, and Polylog Mimicry

## Claim boundary

TICKET-244 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, strong Goldbach, or the twin-prime conjecture. It proves three
partial theorems and one exact route no-go. The iteration is complete; the
four parent problems remain `open_not_proven`, with zero candidate resolutions.

The integrated machine record is
`data/open-problem/ticket244-joint-tightness-harmonic-parity-fold-polylog-mimicry.json`.
The persistent state advances exactly from TICKET-243 to TICKET-244. The
deep-focus track is Twin Prime because uniform arithmetic progressions let us
upgrade fixed-period mimicry to every period bounded by a fixed power of the
scale logarithm.

## Reproduction contract

```text
python scripts/ticket244_joint_tightness_harmonic_parity_fold_polylog_mimicry.py
python -m unittest tests.test_ticket244_joint_tightness_harmonic_parity_fold_polylog_mimicry -v
python scripts/verify_ticket244_structure.py
```

There is no random seed: every computation is deterministic. RH certificates
use exact rational or symbolic values. Collatz uses integer modular arithmetic.
Goldbach uses an integer sieve and direct ordered-pair counts. Twin uses CRT and
the deterministic 64-bit Miller-Rabin bases recorded in the generator. Floating
point values are not used in any proof.

| Problem | Exact TICKET-244 result | Classification | Parent status |
|---|---|---|---|
| Riemann | Joint physical-frequency tightness exactly characterizes relative compactness in bounded `L2(R)` families; either tail condition alone fails | `partial_theorem` | `open_not_proven` |
| Collatz | The fixed-base Fermat-quotient bad line is exactly a relation between the half and third harmonic sums modulo `q` | `partial_theorem` | `open_not_proven` |
| Strong Goldbach | The odd-prime even-target integrand is exactly half-periodic, so the `0` and `1/2` arcs fold together | `partial_theorem` | `open_not_proven` |
| Twin Prime | Every periodic fingerprint with period `M_X <= (log X)^A` has prime/composite-successor mimics in every sufficiently large dyadic block | `exact_no_go` | `open_not_proven` |

## 1. Riemann Hypothesis

### A. Exact proposition

Use the unitary Fourier transform on `L2(R)`. Let `K` be bounded. Then `K` is
relatively compact if and only if, for every `epsilon>0`, some `R` satisfies

```text
sup_(f in K) integral_(|x|>R) |f(x)|^2 dx       < epsilon,
sup_(f in K) integral_(|xi|>R) |fhat(xi)|^2 dxi < epsilon.       (RH-244.1)
```

Neither condition alone is sufficient. TICKET-243 supplied the frequency-only
counterfamily. For the new physical-only direction,

```text
f_n(x)=pi^(-1/2) 1_[-pi,pi](x) cos(nx),  n>=1,                 (RH-244.2)
```

is normalized, real, even, physically supported in one fixed interval, and
orthonormal.

### B-D. Definitions, proof, and grounds

Let `||f||_2<=B` on `K`. Plancherel gives

```text
||tau_h f-f||_2^2
 = integral |exp(i h xi)-1|^2 |fhat(xi)|^2 dxi
 <= R^2 h^2 B^2 + 4 epsilon.                                  (RH-244.3)
```

The first term is the contribution of `|xi|<=R`, using
`|exp(iu)-1|<=|u|`; the second is the Fourier tail. Thus frequency tightness
implies uniform translation continuity. Together with physical tightness, the
Riesz-Kolmogorov criterion implies relative compactness.

Conversely, cover a compact closure by a finite `epsilon`-net. Each center has
a vanishing physical tail, so one radius works for all centers and hence the
whole set. The Fourier transform is unitary and sends a compact set to a compact
set, so the same finite-net argument proves the frequency tail. Finally,
cosine orthogonality makes the Gram matrix of (RH-244.2) exactly the identity,
with pairwise squared distance `2`.

This is an application of the classical Riesz-Kolmogorov compactness boundary;
it is not claimed as a new theorem in functional analysis. A modern source
states the `L2` and Paley-Wiener scope explicitly: [Mitkovski, Stockdale,
Wagner, and Wick](https://arxiv.org/abs/2204.14237).

### E-H. Adversarial checks, computation, interpretation, and finite limit

- Quantifiers are uniform over `K`; no pointwise-to-uniform exchange is made.
- Boundedness is explicit. Without it, tail conditions do not control norm.
- Five physical-support Gram rows have sizes `4,8,16,32,64`, diagonal `1`,
  off-diagonal `0`, and minimum squared distance `2`.
- Five rational translation rows take `R=n`, `h=1/n^2`, `epsilon=1/n^2`,
  `B=1`; (RH-244.3) is exactly `5/n^2` for `n=2,4,8,16,32`.
- Transcript SHA-256:
  `ba395b597b5ad65a2e1542934cb1781646c445f36e3b2828931e423fde04b07b`.
- These ten rows illustrate exact formulas. The infinite compactness theorem
  rests on Plancherel and Riesz-Kolmogorov, not on a finite sample.

### I-K. Classification, gap, and next single lemma

Classification: `partial_theorem`.

Newly retired route: physical tightness alone. Together with TICKET-243, each
one-sided tightness shortcut is now closed. The actual normalized admissible
Guinand-Weil class has not been proved jointly tight or exhaustive, and no
uniform signed arithmetic tail or positive limiting margin is known. The RH
itself remains open; Clay still lists it as a Millennium problem
([official problem page](https://www.claymath.org/millennium/Riemann-Hypothesis/)).

Next single lemma:
`UniformSignedGuinandWeilTailWithPositiveMarginOnExhaustiveJointlyTightAdmissibleClasses`.

## 2. Collatz conjecture

### A. Exact proposition

For a prime `q>5`, define

```text
F_q(a) = (a^(q-1)-1)/q mod q,
H_m    = sum_(1<=k<=m) k^(-1) mod q.
```

Then

```text
2F_q(2) = -H_((q-1)/2),
3F_q(3) = -2H_floor(q/3).                                     (CO-244.1)
```

Consequently

```text
5F_q(2)=3F_q(3)  iff  4H_floor(q/3)=5H_((q-1)/2),             (CO-244.2)
 F_q(2)= F_q(3)  iff  4H_floor(q/3)=3H_((q-1)/2).             (CO-244.3)
```

On the line (CO-244.2), equation (CO-244.3) holds exactly when the half
harmonic sum is zero. Hence a **first-order** positive-defect candidate is
exactly (CO-244.2) plus `H_((q-1)/2) != 0`. If both first-layer lines vanish,
higher `q`-adic valuations are not decided by this theorem.

### B-D. Definitions, proof, and grounds

For a general integer `m` coprime to `q`, multiplication by `m` permutes the
nonzero residues modulo `q`. Write

```text
mk = r_k + q floor(mk/q),  1<=r_k<=q-1.
```

Comparing the products modulo `q^2`, then grouping the floor values, gives
Lerch's elementary formula

```text
mF_q(m) = -sum_(j=1)^(m-1) H_floor(jq/m) mod q.               (CO-244.4)
```

At `m=2` this gives the first identity in (CO-244.1). At `m=3`, reflection
`k -> q-k` gives `H_floor(2q/3)=H_floor(q/3) mod q`, proving the second.
Substitution proves (CO-244.2)-(CO-244.3). On (CO-244.2), the second line
becomes `5H_half=3H_half`; since `q` is odd, this is equivalent to
`H_half=0`.

Fermat and Wieferich quotients are standard external objects; for background
and explicit claim boundaries see [Sondow](https://arxiv.org/abs/1110.3113).
The derivation of (CO-244.4) is included here, so no unproved distribution
claim is imported.

### E-H. Adversarial checks, computation, interpretation, and finite limit

- The result is at the first modulo-`q^2` layer. It does not compare valuations
  when both Fermat-quotient residues vanish.
- Exact integer arithmetic checks all `2,259` primes `5<q<=20,000`.
- The inverse recurrence `k^(-1)=-(q div k)(q mod k)^(-1) mod q` computes both
  harmonic prefixes. Complexity is
  `O(sum_(q<=Q, q prime) q)` integer operations plus `O(pi(Q))` modular powers.
- The replay verifies (CO-244.1)-(CO-244.3), the direct `q^2` congruence, and
  the first-order-candidate equivalence. It has zero identity failures, zero
  bad-line primes, and zero first-order positive candidates.
- Transcript SHA-256:
  `bf5611e2479fe672d7d3a6b8d746f99c79bfee67bc7f894075681ca39b6723a2`.
- The absence through `20,000` is not a new range record and is not an
  all-prime theorem. TICKET-241 already scanned the exponent form much farther.

### I-K. Classification, gap, and next single lemma

Classification: `partial_theorem`.

No new route is retired. The harmonic representation is retained because it
replaces a `q^2` exponent condition by a finite-field prefix-sum identity and
exposes a sharp falsifiable next statement. No proof excludes the bad line for
all primes. Even its exclusion would settle only the current run-block local
defect, not general necklaces, divergent orbits, or nontrivial cycles. Tao's
almost-all-orbits result illustrates how far such density statements remain
from the all-orbit conjecture ([primary paper](https://arxiv.org/abs/1909.03562)).

Next single lemma:
`FixedBaseHarmonicBadLineNonvanishingForEveryPrime`.

## 3. Strong Goldbach conjecture

### A. Exact proposition

Put `e(t)=exp(2 pi i t)` and

```text
O_X(alpha)=sum_(3<=p<=X) e(p alpha).
```

Then

```text
O_X(alpha+1/2) = -O_X(alpha).                                 (GB-244.1)
```

For every even target `N`,

```text
O_X(alpha)^2 e(-N alpha)
```

is exactly `1/2`-periodic. Thus any arc around `1/2` has the same signed
integral as its translate around `0`. For every even `N>=6`, the full-prime
and odd-prime binary coefficients are equal.

### B-D. Definitions, proof, and grounds

Every prime in `O_X` is odd, so translation by `1/2` contributes `-1` to
each summand. The square removes this sign, while the target phase gains
`e(-N/2)=1` for even `N`. This proves exact half-periodicity, including the
sign of the Fourier coefficient rather than merely its absolute energy.

Write the full sum as `S_X=O_X+e(2alpha)`. The difference `S_X^2-O_X^2`
encodes representations having a summand `2`, or `2+2`. For even `N>=6`, a
representation `2+(N-2)` would require the even integer `N-2>=4` to be prime;
therefore its coefficient is zero. This proves the full/odd coefficient
identity.

### E-H. Adversarial checks, computation, interpretation, and finite limit

- The restrictions `N` even and `N>=6` are essential. At `N=4`, `2+2`
  contributes; for odd `N`, the target phase changes sign under the half-turn.
- Five exact sieve rows check all even targets from `6` to
  `X=100,500,1000,5000,10000`, for `8,290` target cases in total.
- Direct ordered-pair counts give zero full-vs-odd coefficient failures.
  Integer phase exponents on an even cyclic grid give zero half-turn failures.
- Complexity is `O(sum_X X*pi(X))` elementary integer tests in this reference
  implementation. Randomness and floating point are absent.
- Transcript SHA-256:
  `ba16a10093eb8fe103469b86dec9e5768dcfed91fccc7944168c6c775a0d3c61`.
- The bounded positive representation counts are ordinary finite checks, not a
  proof of strong Goldbach. The analytic theorem is the folding identity.

### I-K. Classification, gap, and next single lemma

Classification: `partial_theorem`.

The route treating the zero and half-frequency odd-prime arcs as independent
signed problems is retired: they are exact translates. This does not control
the other small denominators or the residual minor arcs. Helfgott's ternary
Goldbach work is a primary reference for the rigorous major/minor-arc boundary,
but it does not prove binary strong Goldbach
([paper](https://arxiv.org/abs/1205.5252)).

Next single lemma:
`CompleteDenominatorAtLeastThreeMajorArcExtractionAndSignedResidualSavingAfterParityFolding`.

## 4. Twin-prime conjecture — deep focus

### A. Exact proposition

Fix `A>0`. For every sufficiently large `X`, let

```text
1 <= M_X <= (log_2 X)^A,
gcd(a_X,M_X)=gcd(a_X+2,M_X)=1,
```

and let `F_X(n,n+2)` depend only on the pair modulo `M_X`. Then every
sufficiently large dyadic interval `[X,2X]` contains a prime `p` such that

```text
F_X(p,p+2)=F_X(a_X,a_X+2),
```

but `p+2` is composite.

This refutes the whole route of pure periodic twin classifiers whose
scale-dependent periods are bounded by any fixed power of `log X`.

### B-D. Definitions, proof, and grounds

For `M_X>=2`, Bertrand's postulate supplies a prime

```text
M_X < ell_X < 2M_X;
```

take `ell_X=3` for `M_X=1`. CRT produces the reduced class

```text
r_X = a_X mod M_X,
r_X = -2  mod ell_X,
Q_X = M_X ell_X < 2M_X^2 <= 2(log_2 X)^(2A).                 (TP-244.1)
```

Siegel-Walfisz is uniform over moduli bounded by any fixed logarithmic power.
For this varying `Q_X` and reduced `r_X`, it gives

```text
pi(2X;Q_X,r_X)-pi(X;Q_X,r_X)
 ~ (Li(2X)-Li(X))/phi(Q_X) > 0                               (TP-244.2)
```

uniformly for all sufficiently large `X`. Choose such a prime `p`. The first
CRT congruence preserves `F_X`; the second makes `ell_X | p+2`. Since
`X>ell_X` eventually, this is a proper divisor and `p+2` is composite.

The required logarithmic uniformity follows from the standard
Siegel-Walfisz theorem; a modern primary treatment deriving it from a uniform
PNT in progressions is [Thorner and Zaman](https://arxiv.org/abs/2108.10878).

### E-H. Adversarial checks, computation, interpretation, and finite limit

- `A` is fixed before `X` tends to infinity. The theorem does not allow
  `A=A(X)` to grow.
- The residue is reduced modulo `Q_X`: admissibility handles the `M_X` part,
  and `r_X=-2 mod ell_X` is nonzero because `ell_X` is odd.
- The use of Siegel-Walfisz is uniform in both the varying modulus and residue.
  A fixed-modulus PNT would not suffice here.
- Four deterministic rows use `A=4`, periods `30,210,2310,30030`, the least
  prime greater than each period, and block start `X=1000Q_X`.
- All four rows satisfy the exact bit-length check
  `M_X<=floor(log_2 X)^4`, contain a certified prime mimic, and factor `p+2`
  by `ell_X`. The largest witness is `p=905230686377`, with
  `p+2=30047*30127157`.
- Complexity of a finite row is linear in the number of progression candidates
  tried, with deterministic primality testing. Transcript SHA-256:
  `506feb7368986984fd026ada7be00bb70d5049766f2ab1d0c02ee24686cb8d7c`.
- The four rows do not prove the infinite statement; (TP-244.2) does.

### I-K. Classification, gap, and next single lemma

Classification: `exact_no_go` for the specified periodic-classifier route.

Newly retired route: every pure periodic fingerprint with period bounded by a
fixed logarithmic power, even when its period and accepted residue may vary
with the scale. This theorem says nothing about superpolylogarithmic periods,
nonperiodic features, signed von Mangoldt correlations, or Type-I/II estimates.
It neither proves nor disproves infinitely many twin primes.

Next single lemma:
`SuperPolylogarithmicScaleLocalTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass`.

## Proof DAG and adversarial audit

Each machine DAG is acyclic and has exactly one `open` frontier. External
compactness and arithmetic-progression theorems are marked `external_theorem`,
not silently promoted to project proofs.

```text
RH-T243 + Plancherel + Riesz-Kolmogorov
  -> RH-N244 disproved (physical tightness alone)
  -> RH-T244 proved
  -> RH-OPEN244

CO-T243
  -> CO-T244 proved (first-layer harmonic equivalence)
  -> CO-OPEN244

GB-T243
  -> GB-N244 disproved (independent 0 and 1/2 odd-prime arcs)
  -> GB-T244 proved
  -> GB-OPEN244

TP-T243 + Bertrand + Siegel-Walfisz
  -> TP-N244 disproved (polylog periods escape mimicry)
  -> TP-T244 proved
  -> TP-OPEN244
```

No DAG path reaches a parent-conjecture `proved` or `disproved` node. The
resolution count and candidate-resolution count are both zero.

## Final boundary

TICKET-244 is iteration-complete. It establishes three partial theorems and
one exact no-go, with zero machine failures and zero stagnated tracks. It does
not resolve any of the four conjectures.

**This iteration is complete, but the conjectures are not resolved.**
