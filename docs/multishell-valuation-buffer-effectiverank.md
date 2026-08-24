# TICKET-238: Multishell Accumulation, Valuation Quantifiers, Mesoscopic Buffers, and Effective Rank

## Abstract and claim status

TICKET-238 continues PrimeProject's simultaneous proof-or-counterexample search
for the Riemann Hypothesis, Collatz conjecture, strong Goldbach conjecture, and
Twin Prime conjecture. **All four parent conjectures remain open.** This report
proves four narrower exact statements and rejects four insufficient proof
routes. It reports no unbounded counterexample and no parent-conjecture proof.

The machine-readable record is
[`ticket238-multishell-valuation-buffer-effectiverank.json`](../data/open-problem/ticket238-multishell-valuation-buffer-effectiverank.json).
The generator and tests are:

```powershell
python scripts/ticket238_multishell_valuation_buffer_effectiverank.py
python -m unittest tests.test_ticket238_multishell_valuation_buffer_effectiverank -v
```

| Problem | Exact TICKET-238 result | Route discarded | Next single lemma |
|---|---|---|---|
| Riemann | `MultishellNormalizedCrossRowSumCriterionAndPairwiseAngleNoGo` | pairwise principal-angle gaps alone imply global cofinal positivity | `ArithmeticWeilInnovationNormalizedCrossRowSumBelowOneOnCofinalDisjointLogarithmicShells` |
| Collatz | `AdaptiveValuationCriterionEquivalenceAndRunBlockClosure` | the all-necklace valuation target is weaker than affine nondivisibility | `RunBlockValuationWitnessEscapesEveryFixedFinitePrimePalette` |
| Goldbach | `MesoscopicBufferWidthNecessaryForInverseLogReflectedMargin` | any diverging endpoint buffer can support an inverse-log margin | `MesoscopicBufferedDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack` |
| Twin Prime | `DegreeTwoEnergyEffectiveRankEquivalenceAndSupportGrowthNoGo` | growing support alone forces degree-two CRT decorrelation | `PrimeWeightedDegreeTwoCRTGramEffectiveRankDivergesWithUniformDiagonalControl` |

## 1. Riemann track

### Declared proposition

Let `H=(H_ij)_(1<=i,j<=J)` be a Hermitian block matrix with `H_ii=I` and
`H_ij=K_ij=K_ji*`. Define

\[
\eta=\max_i\sum_{j\ne i}\lVert K_{ij}\rVert_{op}.
\]

If `eta<1`, then

\[
H\succeq (1-\eta)I. \tag{RH-238.1}
\]

Pairwise positive principal angles do not imply this global conclusion. For
the scalar family

\[
H_{ii}=1,\qquad H_{ij}=-\rho\quad(i\ne j),\qquad 0<\rho<1,
\]

every two-shell principal block has minimum eigenvalue `1-rho>0`, but the full
matrix has eigenvalues

\[
1-(J-1)\rho,\qquad 1+\rho\quad\text{(multiplicity }J-1\text{)}. \tag{RH-238.2}
\]

At `rho=1/3,J=4`, it is positive semidefinite with a zero constant-mode
value and is the Gram matrix of a regular simplex. This jointly realizable row
already refutes a **strict** global lower bound. The same abstract algebraic
family is indefinite when `(J-1)rho>1`; those larger rows are not claimed to be
joint Gram realizations.

### Proof

For a block vector `x=(x_i)`,

\[
\begin{aligned}
\langle Hx,x\rangle
&\ge \sum_i\lVert x_i\rVert^2
-2\sum_{i<j}\lVert K_{ij}\rVert\lVert x_i\rVert\lVert x_j\rVert\\
&\ge \sum_i\left(1-\sum_{j\ne i}\lVert K_{ij}\rVert\right)
\lVert x_i\rVert^2\\
&\ge (1-\eta)\lVert x\rVert^2,
\end{aligned}
\]

where the second line uses `2ab<=a^2+b^2`. Equation `(RH-238.2)` follows by
splitting scalar vectors into the constant mode and its orthogonal complement.

### Reproducible computation and limit

The exact rational audit uses `rho=1/3` and `J=2,...,8`. Every pair remains
positive with minimum `2/3`; the global constant eigenvalue is zero at `J=4`
and negative from `J=5`. The `J=4` row is the realizable regular-simplex
Gram obstruction; `J=5,...,8` only expose abstract block accumulation. A
comparison family `K_ij=1/(4J)` has `eta=(J-1)/(4J)<1` and passes
`(RH-238.1)`.

This proves a linear-algebraic accumulation requirement, not an arithmetic
Weil estimate. No actual Guinand-Weil innovation shells are shown to satisfy
the row-sum bound, and no zeta zero is computed or excluded. The
[Clay Mathematics Institute](https://www.claymath.org/riemann/) still lists RH
as an unsolved Millennium problem.

- Discard: pairwise shell-angle control as a complete global certificate.
- Retain: a summable normalized cross-shell interaction estimate.
- Next lemma:
  **ArithmeticWeilInnovationNormalizedCrossRowSumBelowOneOnCofinalDisjointLogarithmicShells**.

## 2. Collatz track

### Declared proposition

For positive integers `D,B`, unique factorization gives

\[
D\nmid B
\quad\Longleftrightarrow\quad
\exists q\text{ prime}:v_q(D)>v_q(B). \tag{CO-238.1}
\]

TICKET-197 proved for every `k>=1` that

\[
D_k=32^k-27^k\nmid
B_k=32^k+27^k-2\cdot18^k.
\]

Combining it with `(CO-238.1)` proves that every binary run block
`1^k 2^(2k)` has a word-dependent prime-power valuation witness.

Conversely, imposing `(CO-238.1)` on **every** primitive binary density-band
necklace is exactly universal affine nondivisibility on that class. The
valuation formulation exposes a certificate, but it does not remove the
missing universal quantifier and is therefore not a weaker intermediate
theorem.

### Proof and exact audit

Writing `D=product_q q^(e_q)`, divisibility `D|B` is equivalent to
`v_q(B)>=e_q` for every `q|D`; negation proves `(CO-238.1)`. TICKET-197's
closed-form inequality supplies `D_k not dividing B_k`, so a valuation witness
exists for every `k` without factoring `D_k`.

The audit gives an explicit witness for every `1<=k<=20`. Examples include
`q=5` at `k=1`, `q=59` at `k=2`, `q=41` at `k=8`, and `q=43` at `k=14`.
Every row checks `v_q(D_k)>v_q(B_k)` with exact integer arithmetic. These rows
replay the certificate format; the all-`k` statement comes from TICKET-197 plus
unique factorization, not from extrapolation.

The result remains inside one periodic run-block family. General necklaces,
valuation words containing entries above two, and aperiodic divergence remain
open. Recent finite-verification algorithms, such as
[Angeltveit's 2026 algorithm](https://arxiv.org/abs/2602.10466), do not replace
the infinite quantifier.

- Discard: presenting the universal necklace valuation target as a smaller
  lemma than universal affine nondivisibility.
- Retain: identify a mechanism forcing witnesses to escape fixed palettes,
  first on the already closed run-block family.
- Next lemma: **RunBlockValuationWitnessEscapesEveryFixedFinitePrimePalette**.

## 3. Strong Goldbach track

### Declared proposition

Let `x_X` be the indicator of primes at most `X`, and let `g_X=x_X*x_X` be its
ordered additive convolution. For `0<=h<=X-2`,

\[
g_X(2X-h)\le h+1. \tag{GB-238.1}
\]

Consequently a normalized inverse-log margin

\[
{g_X(2X-h)\over\pi(X)}\ge {c\over\log X},\qquad c>0,
\]

requires

\[
h+1\ge {c\pi(X)\over\log X}
=(c+o(1)){X\over(\log X)^2}. \tag{GB-238.2}
\]

Thus a buffer `h=o(X/(log X)^2)` is geometrically too thin for the TICKET-237
inverse-log target, regardless of any Fourier decomposition.

### Proof and computation

If `p,q<=X` and `p+q=2X-h`, then `X-h<=p<=X`. There are at most `h+1`
possible integers `p`, proving `(GB-238.1)`. Divide by `pi(X)` and use the prime
number theorem to obtain `(GB-238.2)`.

The exact audit checks `X=100,1000,10000,100000` and `h=0,1,floor(sqrt X)`.
For each row it records the admissible integer interval, the actual ordered
prime-pair count, and the ceiling `(h+1)/pi(X)`. All 12 rows pass.

This is only a necessary near-endpoint scale. It does not prove that a buffer
of order `X/(log X)^2` is sufficient, does not bound the actual reflected
minor term, and does not find a Goldbach counterexample. Exceptional-set
results concern average coverage and still require a pointwise upgrade; see
the current primary context in
[Grimmelt--Bhowmik](https://arxiv.org/abs/2607.27282).

- Discard: “any buffer tending to infinity is enough” for inverse-log gain.
- Retain: a mesoscopic buffer at least on the `X/(log X)^2` scale plus an
  independent pointwise minor slack.
- Next lemma:
  **MesoscopicBufferedDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack**.

## 4. Twin Prime track

### Declared proposition

Let `C` be the Gram matrix of `m` centered variance-one coordinates, and set

\[
E_{m,2}={1\over\binom m2}\sum_{i<j}|C_{ij}|^2,
\qquad
r_{eff}(C)={\operatorname{tr}(C)^2\over\lVert C\rVert_F^2}.
\]

Then

\[
r_{eff}(C)={m\over1+(m-1)E_{m,2}},
\qquad
E_{m,2}={m/r_{eff}(C)-1\over m-1}. \tag{TP-238.1}
\]

For `m` tending to infinity,

\[
E_{m,2}\to0
\quad\Longleftrightarrow\quad
r_{eff}(C)\to\infty. \tag{TP-238.2}
\]

Growing support alone is not sufficient. Repeat each of two orthonormal
centered modes `m/2` times while embedding them in a support of size `m+1`.
Then

\[
r_{eff}=2,
\qquad
E_{m,2}={m/2-1\over m-1}\longrightarrow {1\over2}. \tag{TP-238.3}
\]

### Proof and computation

Because `C_ii=1`,

\[
\lVert C\rVert_F^2
=m+2\sum_{i<j}|C_{ij}|^2
=m+m(m-1)E_{m,2}.
\]

Substitution proves `(TP-238.1)`. It also gives
`1/r_eff=1/m+(1-1/m)E_(m,2)`, proving `(TP-238.2)`. In the repeated-mode
family the only nonzero Gram eigenvalues are `m/2,m/2`, which proves
`(TP-238.3)`. Exact rows for `m=4,8,16,32,64` preserve `r_eff=2` even though
the support grows from 5 to 65.

This theorem sharpens TICKET-237's support-rank necessity but is still abstract
Gram geometry. Prime-weighted effective-rank divergence, uniform diagonal
control, positive principal mass, and parity breaking are not proved.
Maynard's [small-gap theorem](https://annals.math.princeton.edu/2015/181-1/p07)
provides bounded gaps, not fixed gap two.

- Discard: support growth alone as a decorrelation certificate.
- Retain: arithmetic divergence of normalized CRT Gram effective rank.
- Next lemma:
  **PrimeWeightedDegreeTwoCRTGramEffectiveRankDivergesWithUniformDiagonalControl**.

## Integrated proof DAG

```text
RH-T237 -> RH-T238 -> RH-N238 [discarded]
                    -> RH-OPEN238 -> RH [open]

CO-T197 + CO-T237 -> CO-T238 -> CO-N238 [discarded]
                               -> CO-OPEN238 -> periodic exclusion -> CO [open]

GB-T237 -> GB-T238 -> GB-N238 [discarded]
                    -> GB-OPEN238 -> GB [open]

TP-T237 -> TP-T238 -> TP-N238 [discarded]
                    -> TP-OPEN238 -> parity/main-mass gate -> TP [open]
```

## Final boundary

TICKET-238 contains four exact partial or no-go theorems, four route
corrections, four machine-readable proof DAGs, zero computation failures, and
zero parent-conjecture resolutions. The finite rows verify formulas and
certificate implementations. Only the displayed algebraic arguments support
statements beyond those finite rows. Independent expert review is required
before making any novelty or publication-priority claim.
