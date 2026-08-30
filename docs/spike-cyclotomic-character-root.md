# TICKET-257: Spike, cyclotomic, character, and root-neighbor audit

Status: **iteration complete; all four parent conjectures remain open**.

This report continues TICKET-256. It declares one exact target per problem, separates algebraic proof from finite computation, records a falsified route as a no-go whenever possible, and leaves exactly one next lemma per track. The machine-readable source is `data/open-problem/ticket257-spike-cyclotomic-character-root.json`; its four proof DAGs use only typed nodes and each has one open frontier.

## Executive boundary

| Problem | Exact TICKET-257 target | Classification | Parent problem |
|---|---|---|---|
| Riemann hypothesis | `PositiveConvergentPacketEnergyLagPartialSumNoGo` | exact no-go | open, not proved |
| Collatz conjecture | `DistinctPrimeCyclotomicPhaseExactCancellationNoGo` | exact no-go | open, not proved |
| Strong Goldbach conjecture | `QuadraticCharacterReflectionObstructionAndNextPrefixExclusion` | partial theorem | open, not proved |
| Twin-prime conjecture | `UniqueRealRootNeighborReductionAndBoundedExclusion` | partial theorem | open, not proved |

No row is a candidate resolution. Exact theorem count is four, candidate-resolution count is zero, and conjecture-resolution count is zero.

## 1. Riemann hypothesis

### A. Declared proposition

There is a real Toeplitz lag sequence whose normalized all-ones packet energies obey (E_L\geq 1/2) for every (L) and (E_L\to1), while its symmetric lag partial sums are unbounded below. Explicitly, prescribe

\[
E_L=\begin{cases}
1-2^{-k},&L=4^k,\quad k\geq1,\\
1,&\text{otherwise},
\end{cases}
\]

set (S_n=(n+1)E_{n+1}-nE_n), and reconstruct (a_0=S_0), (a_n=(S_n-S_{n-1})/2). Then (S_{4^k-1}=1-2^k\to-\infty). Thus positivity and convergence of packet energies alone cannot imply the uniform lower bound sought in TICKET-256.

A repaired sufficient condition is also proved: if

\[
\delta=\inf_LE_L>0,\qquad
V=\sup_L L(E_L-E_{L+1})_+<\delta,
\]

then (S_L\geq\delta-V>0) for every (L).

### B. Proof

TICKET-256 proved the exact Cesàro identity

\[
E_L=\frac1L\sum_{n=0}^{L-1}S_n.
\]

Taking differences gives the exact inverse (S_n=(n+1)E_{n+1}-nE_n), so the displayed reconstruction realizes the prescribed energy sequence. Its minimum is (1/2), and the exceptional deficit (2^{-k}) tends to zero; hence (E_L\to1). Immediately before a spike, with (L=4^k),

\[
S_{L-1}=LE_L-(L-1)E_{L-1}
=4^k(1-2^{-k})-(4^k-1)=1-2^k.
\]

For the repair, rewrite the inverse as

\[
S_L=E_{L+1}-L(E_L-E_{L+1})\geq\delta-V.
\]

This proof is algebraic for all (L), not an extrapolation from the eight replay rows.

### C. Reproducible adversarial computation

`python scripts/ticket257_spike_cyclotomic_character_root.py` reconstructs exact rational lags and directly recomputes the packet energy for (k=1,\ldots,8), through (L=65{,}536). It verifies (E_L=1-2^{-k}) and (S_{L-1}=1-2^k) with `Fraction` arithmetic. Random seed: none.

### D. Logical and finite boundary

The construction is an abstract Toeplitz lag sequence. It is not shown to arise from the Guinand-Weil form, so it neither proves nor disproves RH. The finite replay checks implementation consistency only; unboundedness and convergence come from the formulas.

### E. Route decision

- Discarded: deriving a uniform lag-partial-sum lower bound from positivity plus convergence alone.
- Retained: the scaled-downward-variation repair criterion.
- Next single lemma: `ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation`.

## 2. Collatz conjecture

### A. Declared proposition

Let (q_1,\ldots,q_N) be distinct odd primes, let (\zeta_q) be a primitive (q)-th root of unity, and choose any (d_j\bmod q_j). Then

\[
\sum_{j=1}^N\zeta_{q_j}^{d_j}\neq0.
\]

Consequently, no finite prefix of the canonical phases

\[
\exp(2\pi iD_q/q),\qquad D_q=5F_q(2)-3F_q(3),
\]

can cancel exactly. This is an exact obstruction to finite pairing or grouping, not a quantitative cancellation estimate.

### B. Proof

If every (d_j=0), the sum is (N\neq0). Otherwise choose (j) with (d_j\neq0), put (m=\prod_{i\neq j}q_i), and let (F=\mathbb Q(\zeta_m)). Coprimality of the conductors gives

\[
\mathbb Q(\zeta_m,\zeta_{q_j})=\mathbb Q(\zeta_{mq_j}).
\]

Euler-(\varphi) multiplicativity makes the compositum degree equal to ([F:\mathbb Q](q_j-1)), so (F\cap\mathbb Q(\zeta_{q_j})=\mathbb Q). A zero relation would express (\zeta_{q_j}^{d_j}) as an element of (F). Since (d_j\not\equiv0\pmod{q_j}), it is invertible modulo (q_j), so this would put (\zeta_{q_j}) in (F), a contradiction.

### C. Reproducible adversarial computation

Exact modular Fermat quotients are evaluated for the 22 primes (7\leq q\leq97). Every canonical exponent is nonzero:

`(7,6), (11,3), (13,4), (17,1), (19,18), (23,11), (29,18), (31,10), (37,25), (41,11), (43,33), (47,46), (53,5), (59,35), (61,19), (67,5), (71,56), (73,56), (79,12), (83,48), (89,47), (97,70)`.

The script also replays the conductor and cyclotomic degree products exactly. Roots of unity are represented symbolically by exponents; no floating-point near-zero decision is made.

### D. Logical and finite boundary

Nonzero finite sums may be arbitrarily small along a growing family. The theorem supplies no sublinear bound and no control of the infinite prime average. It therefore does not imply Collatz descent or decide the conjecture.

### E. Route decision

- Discarded: exact zero through finite pairing/grouping of one phase per distinct prime modulus.
- Retained: cyclotomic linear disjointness as the exact/non-asymptotic boundary.
- Next single lemma: `CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude`.

## 3. Strong Goldbach conjecture — deep-focus track

### A. Declared proposition

Let (q\geq5) be prime and let (N_r) count residues modulo (q) among the first (T) primes. Assume (q) occurs exactly once, so (N_0=1). If (N_r=N_{-r}) for every nonzero (r), then

\[
\prod_{p\leq p_T,\ p\neq q}\chi_q(p)
=\chi_q(-1)^{(T-1)/2}.
\]

A mismatch is therefore an exact reflection-asymmetry certificate. More generally, reflection symmetry is equivalent to the vanishing of every odd multiplicative-character moment

\[
\sum_{r\in\mathbb F_q^\times}N_r\chi(r)=0,
\qquad \chi(-1)=-1.
\]

For the next compatible (q)-divisible case ((q,m)=(11,22)), whose forced prefix length is (T=7{,}759{,}741), the actual quadratic product is (-1\equiv10\pmod{11}), while symmetry requires (+1). Thus that exact prime prefix is excluded.

### B. Proof

Under reflection symmetry, pair (r) with (-r). Their residue product contributes ((-r^2)^{N_r}), whose Legendre symbol is (\chi_q(-1)^{N_r}). Since (T-1=2\sum_{\{r,-r\}}N_r), multiplication gives the stated necessary value.

For the full criterion, every odd character annihilates a symmetric pair. Conversely, (A(r)=N_r-N_{-r}) belongs to the odd subspace of functions on (\mathbb F_q^\times). If all its odd Fourier coefficients vanish, multiplicative-character inversion gives (A=0), hence reflection symmetry.

### C. Reproducible adversarial computation

An exact odd-only segmented sieve counts residue vectors without storing all primes. The three cases are:

| ((q,m)) | (T) | Last prime | Actual residue counts | Quadratic mismatch |
|---|---:|---:|---|---|
| (5,10) | 1,255 | 10,243 | `[1,313,313,317,311]` | no |
| (7,14) | 24,017 | 274,783 | `[1,3993,3991,4003,3998,4016,4015]` | no |
| (11,22) | 7,759,741 | 137,141,243 | `[1,776123,776078,775943,775798,775646,776178,776150,775928,775841,776055]` | yes |

For (q=11), the reflection differences are

`[0,68,237,15,-352,-532,532,352,-15,-237,-68]`.

The product is independently recomputed from the count vector using Euler's criterion. The (q=5) and (q=7) rows are adversarial controls: their vectors are asymmetric although the quadratic product matches the symmetric value. Hence a single quadratic character is sufficient but not necessary.

### D. Logical and finite boundary

Only three compatible rows are counted, with maximum prefix length (7{,}759{,}741). A finite prefix exclusion cannot establish the universal statement needed for strong Goldbach. Character inversion proves a reformulation, not nonvanishing for every compatible prefix.

### E. Route decision

- Discarded: treating the quadratic-character bit as a complete detector of asymmetry; (q=5,7) are exact counterexamples.
- Retained: the one-bit obstruction, the full odd-character equivalence, and the new (q=11) exclusion.
- Next single lemma: `EveryCompatibleEvenQDivisiblePrimePrefixHasNonzeroOddCharacterMoment`.

## 4. Twin-prime conjecture

### A. Declared proposition

Let (B_1(u,v)) be the (\sqrt2)-coefficient of

\[
(1+\sqrt2)(u+v\sqrt2)^{17},
\]

and set (P(x)=B_1(x,1)). Then (P) is strictly increasing and has one irrational real root (\rho\in(-1,0)). Every integral solution (B_1(u,v)=1) is either ((1,0)), or

\[
u=\lceil\rho v\rceil\quad(v>0),\qquad
u=-\lfloor\rho|v|\rfloor\quad(v<0).
\]

Every solution with (v\neq0) is primitive and satisfies

\[
v\mid u^{17}-1,\qquad u\mid256v^{17}-1.
\]

The exact bracket

\[
-0.073255<\rho<-0.07325499
\]

reduces all (0<|v|\leq200{,}000) to 400,399 exact integer evaluations; none equals one.

### B. Proof

Writing (\varepsilon=1+\sqrt2), conjugation gives

\[
P(x)=\frac{\varepsilon(x+\sqrt2)^{17}+\varepsilon^{-1}(x-\sqrt2)^{17}}{2\sqrt2}.
\]

Its derivative is 17 times a sum of positive even powers, hence is positive everywhere. Exact values (P(-1)=-470832) and (P(0)=256) give a unique root in ((-1,0)); the rational-root theorem makes it irrational.

For fixed (v>0), (B_1(u,v)=v^{17}P(u/v)) is a strictly increasing integer sequence in (u). Its first positive value is at (u=\lceil\rho v\rceil), and every later value is at least two, so only that first value can equal one. Odd homogeneity gives the negative-(v) formula. Homogeneity also forces (\gcd(u,v)=1), and reducing the form modulo (v) and modulo (u) yields the two divisibility conditions.

The rational bracket is checked by clearing the denominator. Its width times 200,000 is less than one, so at most two neighbor integers per sign must be evaluated.

### C. Reproducible adversarial computation

The script evaluates the cleared polynomial signs exactly and scans the candidate-complete one-dimensional sequence. It performs 400,399 degree-17 integer evaluations, finds no (v\neq0) solution, and records the sole (v=0) solution ((u,v)=(1,0)), whose reduced norm value is (-1) and is inadmissible for the target branch. Random seed: none.

### D. Logical and finite boundary

The candidate reduction is global, but the exclusion is only through (|v|=200{,}000). It does not prove that every denominator misses coefficient one, does not exclude exponent 17 globally, and does not prove the twin-prime conjecture.

### E. Route decision

- Discarded: treating this branch as an intrinsically two-dimensional (O(V^2)) box search.
- Retained: the exact one-dimensional root-neighbor sequence and primitive divisibility filters.
- Next single lemma: `EveryNonzeroDenominatorUniqueRootNeighborMissesCoefficientOne`.

## Reproduction and audit

```text
python scripts/ticket257_spike_cyclotomic_character_root.py
python -m unittest tests.test_ticket257_spike_cyclotomic_character_root -v
python scripts/verify_ticket257_structure.py
```

The generator uses exact integers and rational arithmetic for theorem certificates. The Goldbach sieve is finite and deterministic. Transcript SHA-256 values, bounds, counts, proof DAGs, route decisions, and claim boundaries are stored in the integrated JSON and duplicated in the four per-track JSON files.

## Final decision

The iteration produced two exact no-go theorems and two partial theorems. It neither proved nor refuted RH, Collatz, strong Goldbach, or the twin-prime conjecture.

This iteration is complete, but the conjectures are not solved.
