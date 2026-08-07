# TICKET-196: Rouché Exhaustion, Collatz Density, and Overlap-Corrected Prime-Power Budgets

## Abstract

TICKET-196 continues PrimeProject's simultaneous attack on the Riemann
Hypothesis (RH), the Collatz conjecture, the strong Goldbach conjecture, and
the Twin Prime conjecture. It does **not** resolve any parent conjecture. It
proves four exact statements that correct the proof search:

1. an exhausting zero-free Rouché certificate for the Taylor sections of an
   entire function is equivalent to the assertion that the function has no
   nonreal zeros, so the former RH target was not a weaker intermediate lemma;
2. the two scalar inequalities available for Collatz valuation words in
   `{1,2}` leave the infinite family `(h,r)=(3k,k)` admissible;
3. Goldbach proper-prime-power contamination admits an exact overlap
   subtraction `(Q*Q)(N)`;
4. the corresponding shift-two contamination admits the local subtraction
   `sum Q(n)Q(n+2)`.

All parent statuses remain `open_not_proven`. The machine-readable result is
[`ticket196-rouche-density-overlap.json`](../data/open-problem/ticket196-rouche-density-overlap.json).

## Claim discipline

| Problem | Exact result in this ticket | Not established |
|---|---|---|
| RH | Rouché-exhaustion equivalence | an actual Xi certificate, RH, or an off-line zero |
| Collatz | scalar-density no-go and an infinite surviving count-profile family | affine divisibility, a nontrivial cycle, or global convergence |
| Goldbach | exact inclusion-exclusion and a smaller contamination envelope | an every-large-even correlation lower bound |
| Twin Prime | exact shift-two inclusion-exclusion and a smaller local envelope | a parity-breaking lower bound on infinitely many blocks |

Finite computation below checks identities and witnesses. It is not promoted
to an infinite conclusion.

## 1. Riemann Hypothesis track

### 1.1 Declared proposition

Let `F` be a real entire function and let `S_n` be its Taylor sections. For
`m>=2`, set

```text
D_m^+ = { z : |Re z| < m and 1/m < Im z < m },
D_m^- = conjugate(D_m^+).
```

Then the following are equivalent:

1. every zero of `F` is real;
2. for every `m` and each sign there is a section `S_n` with zero count zero
   in `D_m^sign` and

```text
sup_{boundary D_m^sign} |F-S_n|
  < inf_{boundary D_m^sign} |S_n|.
```

For the Riemann Xi function, statement 2 is therefore equivalent to RH. It is
not a strictly weaker intermediate target.

### 1.2 Proof

Assume first that all zeros of `F` are real. The compact closure of every
`D_m^sign` is disjoint from the zero set, so

```text
delta_m = min_{closure D_m^sign} |F| > 0.
```

Taylor sections converge uniformly on compact sets. Choose `n` such that
`sup |F-S_n| < delta_m/3` on the closure. Then
`|S_n| > 2 delta_m/3` there. Thus `S_n` has zero count zero and the strict
Rouché inequality holds.

Conversely, each certificate gives `F` and `S_n` the same zero count in its
rectangle, hence zero. The rectangles exhaust `C\R`, so `F` has no nonreal
zero.

### 1.3 Reproducible check and limit

For `m=2,...,12`, the generator compares:

- `F_real(z)=z^2-1`, whose exact degree-two section has no off-real zero and
  satisfies the boundary lower bound `|F_real(z)|>=1/m^2`;
- `F_nonreal(z)=z^2+1`, whose section contains `i` in `D_m^+` and `-i` in
  `D_m^-`.

This synthetic check validates the quantifiers. It says nothing about a
Taylor remainder or zero count for the actual Xi function.

### 1.4 Route decision

- **Discarded:** calling a complete exhausting Xi Rouché family a weaker
  intermediate lemma.
- **Retained:** certify one bounded rational rectangle for the actual Xi
  function at a time.
- **Next lemma:**
  `ActualXiTaylorSectionHasCertifiedZeroCountOnFirstOffRealRationalRectangle`.

## 2. Collatz track

### 2.1 Declared proposition

Suppose a positive accelerated Collatz cycle has `h` valuations in `{1,2}`
and exactly `r` entries equal to one. The TICKET-195 contraction and product
conditions imply

```text
log_2(6/5) <= r/h < 2-log_2(3).
```

This interval contains `1/3`. For every `k>=1`, the count profile
`(h,r)=(3k,k)` passes both scalar gates exactly:

```text
2^(2h-r) = 2^(5k) = 32^k > 27^k = 3^h,
2^r(5/6)^h = (125/108)^k > 1.
```

Therefore these two scalar inequalities alone cannot exclude all `{1,2}`
cycle words.

### 2.2 Proof and computation

Taking base-two logarithms gives the density window. The displayed integer
inequalities prove an infinite family of surviving profiles without numerical
approximation. The generator replays `k=1,...,64`, records
`C(3k-1,k-1)` linear words per profile whose first coordinate is fixed to one,
and hashes the exact integers. This count is not claimed to be the number of
cyclic rotation classes.

The profiles are not Collatz cycles. The computation deliberately records
`affine_divisibility_verified=false`; the order-dependent numerator and
positive fixed-point integrality remain unproved.

### 2.3 Route decision

- **Discarded:** scalar contraction and product-density closure of all
  `{1,2}` valuation words.
- **Retained:** a uniform order-sensitive divisibility obstruction inside the
  exact density window.
- **Next lemma:**
  `UniformAffineDivisibilityObstructionForOneTwoWordsInTheAdmissibleDensityWindow`.

## 3. Strong Goldbach track

### 3.1 Declared proposition

On odd integers, decompose the von Mangoldt support as

```text
Lambda_o = P + Q,
```

where `P` is supported on odd primes and `Q` on odd proper prime powers. For
even `N`, let `E_o(N)` be the weighted terms in
`(Lambda_o*Lambda_o)(N)` with at least one `Q` coordinate. Then

```text
E_o(N) = 2(Q*Lambda_o)(N) - (Q*Q)(N).
```

If `W_Q(N)=sum_{q<N} Q(q)`, this yields the corrected sufficient envelope

```text
E(N) <= 2 log(N) W_Q(N) - (Q*Q)(N) + B_2(N),
```

where `B_2(N)` is the exact power-of-two contribution from TICKET-194.

### 3.2 Proof and witness

Expanding `(P+Q)^2-P^2` gives `PQ+QP+Q^2`. Commutativity gives
`2Q(P+Q)-Q^2`. The older union bound charged `Q^2` twice; subtracting it once
is exact. Since a partner von Mangoldt weight is at most `log N`, the stated
upper envelope follows.

The exact witness is

```text
18 = 9 + 9 = 3^2 + 3^2.
```

Its positive overlap weight is `(log 3)^2`. Eighteen targets, including
`18,34,52` and powers of two through `2^20`, replay the support decomposition,
inclusion-exclusion identity, parity split, and corrected envelope.

### 3.3 Route decision

- **Discarded:** treating left and right proper-power charges as disjoint.
- **Retained:** insert exact overlap subtraction into an explicit major/minor
  arc inequality.
- **Next lemma:**
  `ExplicitGoldbachMajorArcMainTermDominatesMinorArcAbsoluteErrorAndCollisionCorrectedContaminationForEveryLargeEvenTarget`.

## 4. Twin Prime track

### 4.1 Declared proposition

For a dyadic block `[X,2X)`, the exact proper-power contamination in the
shift-two correlation is

```text
E_X = sum Q(n)Lambda(n+2)
    + sum Lambda(n)Q(n+2)
    - sum Q(n)Q(n+2)
    + E_X,even.
```

Consequently the local union envelope improves by subtracting the exact
`Q(n)Q(n+2)` collision mass.

### 4.2 Proof and witness

The identity follows pointwise from `Lambda=P+Q`. Bounding the first two sums
by `log(2X+2)` times their interval `Q` masses and retaining the even term
exactly gives the corrected envelope. The overlap witness is

```text
(25,27) = (5^2,3^3) in [16,32).
```

Its positive correction is `log(5)log(3)`. Seventeen dyadic blocks from
`2^4` through `2^20` replay the exact identity and reference correlation.

### 4.3 Route decision

- **Discarded:** treating left-shift and right-shift proper-power charges as
  disjoint.
- **Retained:** use the corrected budget, then confront the parity-sensitive
  prime-pair lower bound directly.
- **Next lemma:**
  `ParityBreakingShiftTwoLowerBoundDominatesCollisionCorrectedContaminationOnInfinitelyManyDyadicBlocks`.

## 5. Proof DAG summary

```text
TICKET-195 open target
        |
        v
TICKET-196 exact theorem ---- rejected surrogate
        |
        v
single next lemma (open_not_proven)
```

Each problem-specific JSON contains the full nodes and edges. No DAG contains
a `proved` path to a parent conjecture.

## 6. Reproduction

```powershell
python scripts/ticket196_rouche_density_overlap.py
python -m unittest tests.test_ticket196_rouche_density_overlap
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Expected machine boundary:

```text
exact theorem count:                 4
Rouché target equivalences:          1
scalar-density no-go theorems:       1
collision-corrected envelopes:       2
conjecture resolutions:              0
machine failures:                    0
```

## 7. Literature boundary

- The [Clay Mathematics Institute RH statement](https://www.claymath.org/millennium/riemann-hypothesis/)
  remains the governing target. Compact Taylor convergence and Rouché's
  theorem are classical; no new Xi estimate is claimed.
- Tao proves an almost-all logarithmic-density Collatz result, not universal
  convergence ([arXiv:1909.03562](https://arxiv.org/abs/1909.03562)). Recent
  parity-vector work also explicitly stops short of the conjecture
  ([arXiv:2605.13886](https://arxiv.org/abs/2605.13886)).
- The strong Goldbach computation through `4*10^18` is finite, not universal
  ([Mathematics of Computation 83 (2014)](https://doi.org/10.1090/S0025-5718-2013-02787-1)).
- Maynard's bounded-gap theorem does not establish exact gap two
  ([Annals of Mathematics 181 (2015)](https://doi.org/10.4007/annals.2015.181.1.7)).

The elementary equivalences and inclusion-exclusion identities in this
ticket are presented as project-level route corrections, not literature
novelty claims.
