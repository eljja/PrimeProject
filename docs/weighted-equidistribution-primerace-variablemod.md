# TICKET-260: weighted variation, fixed-modulus equidistribution, a mod-3 prime race, and a variable-denominator sieve

Date: 2026-08-31  
Status: `open_not_proven` for all four parent conjectures  
Deep focus: Twin-prime conjecture

This iteration establishes three partial theorems and one exact route no-go. It proves or disproves none of the four parent conjectures. The canonical machine record is `data/open-problem/ticket260-weighted-equidistribution-primerace-variablemod.json`. Every calculation is deterministic and uses integers or rational numbers; no floating-point value is used as proof.

## 1. Riemann hypothesis

### A. Exact proposition

`SummableScaledDownwardVariationForcesEventualLagPositivity`.

Let ((E_n)_{nge1}) be a positive real sequence with (E_n\to L>0). Define

\[
d_n=(E_n-E_{n+1})_+,
\qquad
S_n=(n+1)E_{n+1}-nE_n.
\]

If

\[
\sum_{n\ge1} n d_n<\infty,
\]

then

\[
\liminf_{n\to\infty}S_n\ge L,
\]

and consequently (S_n>0) for all sufficiently large (n).

If true, this gives an explicit sufficient condition that repairs the bounded-total-variation and critical-equality failures from TICKET-258 and TICKET-259. If false, the proposed weighted one-sided route would be retired.

### B–E. Definitions, proof, and adversarial checks

The exact identity

\[
S_n=E_{n+1}-n(E_n-E_{n+1})
\]

implies (S_n\ge E_{n+1}-nd_n). Because a convergent series of nonnegative terms has terms tending to zero, (nd_n\to0). Also (E_{n+1}\to L), so taking lower limits proves the proposition.

The quantifiers are pointwise in the sequence: the theorem asserts eventual positivity for each sequence satisfying the full infinite series hypothesis. It does not provide a uniform cutoff over a class of sequences. No positivity of an actual Weil form is assumed in the proof.

### F–H. Reproducible calculation and finite boundary

The exact replay uses

\[
E_{2^k+1}=1-2^{-3k},\qquad E_n=1\ \text{otherwise}.
\]

Its scaled downward variation is

\[
\sum_{k\ge1}2^k2^{-3k}=\sum_{k\ge1}4^{-k}=\frac13,
\]

and at (n=2^k),

\[
S_n=1-\frac{n+1}{n^3}>0.
\]

Sixteen exact `Fraction` rows are replayed. They check the implementation but are not the proof of the unrestricted theorem. No actual Guinand-Weil coefficient is computed.

### I–K. Classification, gap, and next lemma

- Classification: `partial_theorem`.
- Newly established: summable scaled downward variation is sufficient.
- Retired route: ordinary bounded total variation without the (n)-weighted one-sided condition; TICKET-258 already supplies the obstruction.
- Remaining minimum gap: prove the hypothesis for the actual packet energies.
- Next single lemma: `ActualWeilPacketScaledDownwardVariationIsSummable`.

## 2. Collatz conjecture

### A. Exact proposition

`FixedModulusExponentEquidistributionPhaseAlignmentNoGo`.

There exist distinct primes (q_j) and integers (1\le d_j<q_j) such that, for every fixed (M\ge2) and every (N\ge1), the counts of (d_1,\ldots,d_N) in the residue classes modulo (M) differ by at most one, but

\[
\frac1N\sum_{j\le N}\exp(2\pi i d_j/q_j)\longrightarrow1.
\]

This falsifies the route claiming that equidistribution of the exponents modulo every fixed integer forces cancellation when the ambient prime modulus grows.

### B–E. Construction, proof, and counterexample audit

Choose (q_j) recursively as the least prime exceeding both (q_{j-1}) and (j^3), starting after (3), and put (d_j=j). Infinitely many primes guarantee that the recursion is defined. Consecutive integers are balanced modulo every fixed (M), with prefix discrepancy at most one.

The chord estimate and (pi<4) give

\[
\left|e^{2\pi i j/q_j}-1\right|<\frac{8j}{q_j}<\frac8{j^2}.
\]

The elementary comparison

\[
\sum_{j\ge1}\frac1{j^2}
\le1+\sum_{j\ge2}\frac1{j(j-1)}=2
\]

therefore yields normalized deviation at most (16/N). All premises of the rejected implication hold, while its cancellation conclusion fails linearly.

The counterfamily deliberately does not use the canonical Fermat-quotient exponent. Therefore it blocks only the general fixed-modulus inference, not a theorem using arithmetic information specific to the canonical sequence.

### F–H. Reproducible calculation and finite boundary

The replay constructs 64 prime orders and exact rational chord envelopes, then checks moduli (2\) through (16). The asymptotic proof is symbolic; the finite rows only reproduce the construction. No complex floating-point root is evaluated.

### I–K. Classification, gap, and next lemma

- Classification: `exact_no_go`.
- Exact countermodel: fixed-modulus equidistribution coexists with normalized phase sum tending to one.
- Retired route: any inference based only on fixed-modulus exponent statistics.
- Remaining minimum gap: a moving-modulus angular distribution theorem for the canonical Fermat quotients.
- Next single lemma: `CanonicalFermatQuotientAngularDiscrepancyTendsToZero`.

## 3. Strong Goldbach conjecture

### A. Exact proposition

`Q3CompatibleFamilyPrimeRaceEquivalence`.

For every integer (ell\ge0), set

\[
q=3,\qquad m=12\ell+6,\qquad A=3^{6\ell+2}.
\]

The cyclic coefficients of ((1-X)^m\bmod(X^3-1)) are

\[
(c_0,c_1,c_2)=(-2A,A,A).
\]

The unique compatible forced prefix vector is

\[
(1,1+3A,1+3A)
\]

and has length (T_\ell=6A+3). It equals the residue vector of the first (T_\ell) primes if and only if

\[
\Delta_3(T_\ell):=N_1(T_\ell)-N_2(T_\ell)=0,
\]

where (N_r(T)) counts the first (T) primes congruent to (r\pmod3).

### B–E. Proof and edge cases

For a primitive cube root (zeta), the root-of-unity filter has zero contribution at (1). Since (m=12\ell+6),

\[
(1-\zeta)^m=(1-\bar\zeta)^m=-3^{m/2}.
\]

Fourier inversion gives (c_0=-2\cdot3^{m/2-1}=-2A) and (c_1=c_2=A). Thus the forced shift is (t=1-c_0=1+2A), proving the vector and length formulas.

Every prefix under consideration contains exactly one prime divisible by (3), namely (3). Hence the actual vector has zero-residue entry one, and the other (T_\ell-1) entries equal the forced pair precisely when their two counts tie. This proves both directions of the equivalence; no statistical prime-race heuristic is used.

### F–H. Reproducible calculation and finite boundary

Two independent exact algorithms—an integer quotient-state combinatorial sieve and a direct segmented sieve—agree:

| \(\ell\) | \(m\) | \(T_\ell\) | last prime | actual \((N_0,N_1,N_2)\) | \(\Delta_3\) |
|---:|---:|---:|---:|---:|---:|
| 0 | 6 | 57 | 269 | (1, 25, 31) | -6 |
| 1 | 18 | 39,369 | 471,749 | (1, 19,663, 19,705) | -42 |
| 2 | 30 | 28,697,817 | 547,035,959 | (1, 14,347,849, 14,349,967) | -2,118 |

These three nonzero values are finite certificates only. They do not imply nonvanishing for all (ell).

### I–K. Classification, gap, and next lemma

- Classification: `partial_theorem`.
- Newly established: the entire compatible (q=3) family is exactly one scalar prime-race problem.
- Retired route: treating this family as requiring the full higher-dimensional odd-character detector.
- Remaining minimum gap: exclude a tie at every special exponential index (6\cdot3^{6\ell+2}+3).
- Next single lemma: `Q3SpecialPrimeRaceNeverTiesAtSixTimesPowerOfThreePlusThree`.

## 4. Twin-prime conjecture — deep focus

### A. Exact proposition

`SecondOrderDenominatorCongruenceAnd256ConvergentCertificate`.

For integers (u,v) with (v\ge2) and (arepsilon\in\{-1,1\}),

\[
B_1(u,v)=\varepsilon
\]

forces

\[
u^{17}\equiv\varepsilon\pmod v
\]

and the stronger scale-dependent condition

\[
u^{17}+17u^{16}v\equiv\varepsilon\pmod {v^2}.
\]

Both signs fail the second condition on each of the first 256 certified continued-fraction convergents of the unique root isolated in TICKET-258.

### B–E. Proof, counterexamples, and adversarial audit

The exact form begins

\[
B_1(u,v)=u^{17}+17u^{16}v+v^2R(u,v)
\]

for an integer polynomial (R). Reduction modulo (v) and (v^2) proves the two necessary conditions. The statement does not reverse either implication: passing a congruence is not claimed to solve the Thue equation.

The weaker first-order condition is explicitly insufficient. Among the nontrivial tested convergents it accepts

\[
(u,v,\varepsilon)=(-1,13,-1),\quad(-1,14,-1),
\]

although their exact form values are respectively

\[
-95516898540708139236,
\qquad
168149422466766035245.
\]

Both fail modulo (v^2). These are exact counterexamples to using the first-order test as a complete filter, not counterexamples to the twin-prime conjecture.

For every convergent and both signs, modular exponentiation is independently cross-checked against the full integer (B_1(u,v)) modulo (v^2). The denominator-one convergents are checked directly. The proof DAG uses TICKET-258's unrestricted theorem that every unit-coefficient solution must be one of these convergents; it does not assume that the first 256 exhaust them.

### F–H. Reproducible calculation and finite boundary

The first 256 certified convergents are tested, reaching a 121-digit denominator. There are two first-order passes and zero second-order passes. This excludes only that finite prefix. Infinitely many later convergents remain, and no induction or periodicity of the algebraic continued fraction has been proved.

### I–K. Classification, gap, and next lemma

- Classification: `partial_theorem`.
- Newly established: an unrestricted, genuinely scale-dependent necessary condition modulo (v^2), plus a 256-convergent certificate.
- Retired route: first-order denominator congruence as a complete filter, by the two exact convergent counterexamples above.
- Remaining minimum gap: exclude the second-order condition on every later unique-root convergent.
- Next single lemma: `NoUniqueRootConvergentSatisfiesSecondOrderDenominatorCongruence`.

## Reproduction contract

```powershell
python scripts/ticket260_weighted_equidistribution_primerace_variablemod.py
python -m unittest tests.test_ticket260_weighted_equidistribution_primerace_variablemod
python scripts/verify_ticket260_structure.py
```

- Arithmetic: integers and `Fraction` only for proof-bearing calculations.
- Random seed: none; every algorithm is deterministic.
- Exact cases: RH 16 rows; Collatz 64 phases and 15 fixed moduli; Goldbach 3 prefixes with two algorithms; Twin 256 convergents times two signs.
- Failure count: zero in the committed certificate.
- Claim boundary: `iteration_complete` means the artifacts agree. It does not mean any parent conjecture is resolved.

