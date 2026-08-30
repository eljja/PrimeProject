# TICKET-259: Critical threshold, aligned phases, exact compatibility, and local congruence no-go

Date: 2026-08-31
Status: `open_not_proven` for all four parent conjectures
Deep focus: Strong Goldbach conjecture

This iteration establishes three exact route no-go theorems and one partial theorem. It proves or disproves none of the parent conjectures. The canonical machine record is `data/open-problem/ticket259-critical-alignment-compatibility-local.json`; every track also has a separate JSON record and an acyclic proof DAG with exactly one open frontier.

## Riemann hypothesis

### Declared proposition

`CriticalScaledDownwardJumpEqualityNoGo`. There is a positive sequence \(E_L\to1\), of total variation \(2/3\), for which
\[
\sup_{n\ge1}n(E_n-E_{n+1})_+=1,\qquad
S_n=(n+1)E_{n+1}-nE_n<0
\]
infinitely often. Equality at the critical scaled-drop constant therefore cannot replace a strict margin in the repaired packet criterion.

Set \(E_{4^k+1}=1-4^{-k}\) and \(E_L=1\) otherwise. The isolated down/up jumps give
\[
\operatorname{Var}(E)=2\sum_{k\ge1}4^{-k}=2/3.
\]
At \(n=4^k\), the scaled drop is \(n(E_n-E_{n+1})=1\), while \(S_n=(n+1)(1-1/n)-n=-1/n\). The generator replays 12 exact rational rows; the formulas, not finite extrapolation, prove the all-\(k\) statement.

Established: the non-strict critical threshold is insufficient in the abstract packet model.
Discarded: replacing the strict actual-Weil margin by a non-strict inequality.
Not established: any estimate for actual Guinand-Weil coefficients, or RH.
Next single lemma: `ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation`.

## Collatz conjecture

### Declared proposition

`DistinctPrimePhaseAlignmentLinearGrowthNoGo`. Let \(q_j\) be the \(j\)-th prime at least five and \(z_j=e^{2\pi i/q_j}\). Although \(1,z_1,z_2,\ldots\) have the distinct-prime rational-independence property established in TICKET-258,
\[
\frac1N\sum_{j\le N}z_j\longrightarrow1.
\]
Thus distinct orders, nontriviality, and rational independence do not imply sublinear phase sums.

The chord bound and \(\pi<4\) give \(|z_j-1|<8/q_j\). Since \(q_j\ge j+4\),
\[
\left|\frac1N\sum_{j\le N}z_j-1\right|
\le \frac8N\sum_{j\le N}\frac1{q_j}
\le \frac{8H_N}{N}\to0.
\]
The replay uses no floating-point roots: it stores exact rational envelopes for all 166 primes from 5 through 997.

Established: a linearly growing aligned counterfamily satisfying the earlier structural hypotheses.
Discarded: deriving cancellation from conductor data and rational independence alone.
Not established: a distribution theorem for the canonical Fermat-quotient exponents \(D_q\), or Collatz.
Next single lemma: `CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude`.

## Strong Goldbach conjecture

### Declared proposition

`QDivisibleCompatibilityIffTwoModuloFourAndQ13Certificate`. Let \(q\) be an odd prime, \(m=qs>0\), and let \(c_r\) be the cyclic coefficients of \((1-X)^m\bmod(X^q-1)\). Put \(t=1-c_0\). Then
\[
t>0,\quad c_r+t\ge0\ (0\le r<q)
\]
if and only if \(s\equiv2\pmod4\). The first new case \((q,m)=(13,26)\) is also excluded by an exact prime-prefix certificate.

TICKET-256 implies that compatibility forces \(m\) even, hence \(s=2k\). For \(a\ne0\), the root filter and \(q\mid m\) give
\[
(1-\zeta_q^a)^m=(-1)^k|1-\zeta_q^a|^m.
\]
If \(k\) is even, \(c_0\) is a positive integer and \(t\le0\). If \(k\) is odd, \(c_0<0\), and
\[
c_r-c_0=\frac1q\sum_{a=1}^{q-1}|1-\zeta_q^a|^m
\bigl(1-\cos(2\pi ar/q)\bigr)\ge0.
\]
Thus \(t>0\) and \(c_r+t\ge1\). This is an infinite classification; the 208 rows for \(3\le q\le43,\ 1\le s\le16\) are only exact replay checks.

For \(q=13,m=26\), the forced total is \(T=135,207,787\), whose exact final prime is \(2,798,637,773\). A residue-vector combinatorial sieve and an independent direct segmented sieve agree on
\[
(1,11267061,11268282,11267049,11267171,11266891,11267204,
11267666,11267232,11267306,11266978,11266998,11267948).
\]
The reflection differences are
\[
(0,-887,1284,71,-135,-341,-462,462,341,135,-71,-1284,887),
\]
and the primitive odd-character remainder modulo \(\Phi_{12}\) is
\[
(-958,1746,-64,-121)\ne0.
\]
Therefore the forced symmetric prefix for this compatible pair is not the actual first-\(T\)-prime residue vector.

Established: the infinite compatibility classification and one independently reproduced 135-million-prime exclusion.
Discarded: treating compatibility as an unexplained finite-scan phenomenon.
Not established: nonzero odd-character discrepancy for every \(q\) and every \(s\equiv2\pmod4\), or strong Goldbach. No induction promotes the finite prefix.
Next single lemma: `EveryTwoModuloFourQDivisiblePrimePrefixHasNonzeroOddCharacterMoment`.

## Twin-prime conjecture

### Declared proposition

`FiniteCongruenceFixedRootWindowNoGo`. For the degree-17 form \(B_1(u,v)\) from TICKET-258, every modulus \(M\ge2\), and every nonempty rational interval \(I\subset(-1,0)\), infinitely many primitive pairs satisfy
\[
v>0,\quad u/v\in I,\quad u^2-2v^2<0,\quad B_1(u,v)\equiv1\pmod M.
\]
Thus fixed finite coefficient congruences, even with primitivity, negative norm, and a fixed root window, cannot eliminate the branch.

Replace a finite modulus family by its least common multiple \(M\). For arbitrarily large \(N\), set \(v=M^N\). The interval \(vI\) eventually has length greater than \(M\), so it contains \(u\equiv1\pmod M\). Then \(\gcd(u,v)=1\), the norm is negative because \(|u/v|<1\), and every non-leading monomial of \(B_1\) contains \(v\). Hence \(B_1(u,v)\equiv u^{17}\equiv1\pmod M\). The replay constructs witnesses for \(M=2,\ldots,31\).

Established: infinitely many primitive admissible local witnesses for every fixed finite modulus family and fixed window.
Discarded: closing exponent 17 by fixed congruences plus a fixed interval.
Not established: exclusion of scale-dependent \(v^{-17}\) approximants or twin primes; variable-modulus arguments are not covered.
Next single lemma: `EveryUniqueRootConvergentMissesUnitCoefficient`.

## Reproduction and finite boundary

```powershell
python scripts/ticket259_critical_alignment_compatibility_local.py
python -m unittest tests.test_ticket259_critical_alignment_compatibility_local
python scripts/verify_ticket259_structure.py
```

The generator is deterministic. Both prime-residue algorithms return exact integer vectors. Completing this iteration means the calculations, tests, JSON, documentation, and Pages contract agree; it does not resolve any parent conjecture.
