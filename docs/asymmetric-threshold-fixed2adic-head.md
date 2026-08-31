# TICKET-264 — asymmetric envelope, explicit threshold cutoff, fixed two-adic no-go, and finite-head closure

## A. Verdict

TICKET-264 is complete, but the long program is not. It establishes three
`partial_theorem` results and one `exact_no_go`. The Riemann Hypothesis,
Collatz conjecture, strong Goldbach conjecture, and Twin Prime conjecture all
remain `open_not_proven`; both resolution counters are zero.

Canonical machine record:
`data/open-problem/ticket264-asymmetric-threshold-fixed2adic-head.json`.
This round deliberately gives the Riemann track the deepest attention: it
strictly weakens the sharp abstract packet-rate hypothesis left by TICKET-263.

## B. Reproduction

```text
python scripts/ticket264_asymmetric_threshold_fixed2adic_head.py
python -m unittest tests.test_ticket264_asymmetric_threshold_fixed2adic_head -v
python scripts/verify_ticket264_structure.py
```

The generator uses no random seed. It writes the integrated audit, four
problem-specific JSON files, the persistent research state, and four embedded
acyclic proof DAGs. The declared replay comprises 192 exact rational RH rows,
252 complete-root harmonic threshold cases, 16 two-adic phase-period rows plus
242 shifted-count countermodels, and 39 certified Twin convergents through the
first threshold crossing. All generator failure counts are zero.

## C. Riemann Hypothesis — exact proposition first

### Proposition `AsymmetricReciprocalEnvelopeForScaledJumpMargin`

Let (E_n\to L>0), (a_n=E_n-L), and

\[
A_+=\limsup_{n\to\infty}n\max(a_n,0),\qquad
A_-=\limsup_{n\to\infty}n\max(-a_n,0).
\]

For (J_n=n(E_n-E_{n+1})) and
(S_n=(n+1)E_{n+1}-nE_n), if (A_+,A_-<\infty), then

\[
\limsup J_n\le A_++A_-,\qquad
\liminf S_n\ge L-A_+-A_-.
\]

Thus (A_++A_-<L) supplies an eventual positive lag margin. The coefficient
one on each one-sided envelope is jointly optimal.

### Proof

Since

\[
a_n-a_{n+1}\le a_n^+ + a_{n+1}^-,
\]

we have

\[
J_n\le n a_n^++\frac{n}{n+1}(n+1)a_{n+1}^-.
\]

The limsup inequality follows. The identity
(S_n=E_{n+1}-J_n), together with (E_{n+1}\to L), gives the second
inequality. For sharpness choose arbitrary (P,M\ge0) and put
(a_n=P/n) at even (n), (a_n=-M/n) at odd (n). Then
(A_+=P,A_-=M), the even subsequence has (J_n\to P+M) and
(S_n=L-P-M), while the odd subsequence has (S_n=L+P+M). The critical
case (P+M=L) therefore has zero lag infinitely often.

### What changed and what did not

This strictly improves the symmetric TICKET-263 condition
(\limsup n|E_n-L|<L/2): asymmetric errors may have one envelope above
(L/2) while their sum stays below (L). The exact replay uses
((P,M)=(1/4,1/2),(1/3,2/3),(3/4,1/2)) for the strict, critical, and
supercritical regimes. These are abstract sequences. No actual
Guinand-Weil packet coefficient or one-sided rate was computed.

- Discarded: the claim that the symmetric max-envelope bound is the sharpest
  rate-only formulation.
- Remaining gap: prove the one-sided envelope sum bound for actual packets.
- Next single lemma:
  `ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit`.

## D. Collatz conjecture — exact proposition first

### Proposition `PointwiseWeylCancellationIffExplicitThresholdCutoffDiverges`

For a sequence (x_j\in\mathbb R/\mathbb Z), define

\[
W_N(h)=\frac1N\sum_{j\le N}e^{2\pi i h x_j},\quad
E_N(H)=\max_{1\le |h|\le H}|W_N(h)|,
\]

and the finite-data functional

\[
K_N=\max\bigl(\{0\}\cup
\{1\le H\le N:E_N(H)\le 1/H\}\bigr).
\]

Then (W_N(h)\to0) for every fixed nonzero integer (h) if and only if
(K_N\to\infty). Whenever (K_N\ge1), the uniform error at that cutoff is
at most (1/K_N).

### Proof and exact replay

The admissible (H)'s form an initial segment because (E_N(H)) is
nondecreasing and (1/H) is decreasing. Fixed-h cancellation makes every
fixed finite maximum tend to zero, so eventually (K_N\ge H) for every
fixed (H). Conversely, if (K_N\to\infty), each fixed (h) is eventually
inside the cutoff and
(|W_N(h)|\le E_N(K_N)\le1/K_N\to0).

For the complete (M)-point rational grid the root sum vanishes exactly for
(1\le|h|<M) and has magnitude one at (h=M). Hence (K_M=M-1). The audit
checks (M=4,8,16,32,64,128), including the failing next harmonic.

- Discarded: the assertion that TICKET-263's diagonal cutoff can only be an
  existential, non-data-defined object.
- Finite limit: complete grids are not canonical Fermat-quotient prefixes.
- Remaining gap and next single lemma:
  `CanonicalFermatQuotientThresholdCutoffDiverges`.

## E. Strong Goldbach conjecture — exact proposition first

### No-go theorem `EveryFixedTwoAdicTieSignatureHasNonTieCountModels`

At the q=3 special prefix, a tie forces each nonzero residue count to be
(M_l=3^{6l+3}+1). For every (m\ge1), (M_l\bmod 2^m) has least level
period one for (m\le3), and (2^{m-3}) for (m\ge4). Nevertheless, for
every fixed (m) and every (l) with (M_l>2^m),

\[
(N_1,N_2)=(M_l-2^m,M_l+2^m)
\]

has total (2M_l), has (N_2\equiv M_l\pmod{2^m}), and is not tied.
Therefore no fixed two-adic tie signature together with the total can decide
the tie.

### Proof and interpretation

For (m\ge3), the order of (3\pmod{2^m}) is (2^{m-2}); equivalently
(v_2(3^{2^r}-1)=r+2). Increasing (l) adds six to the exponent, and
(v_2(6)=1), yielding least level period (2^{m-3}); the smaller moduli are
direct. The shifted pair is nonnegative under the stated inequality, keeps
the total, preserves the second residue, and differs by (2^{m+1}).

The 242 replayed pairs for (m=1,\ldots,16) and (l=0,\ldots,15) are
abstract integer count models. They do not assert that those pairs occur as
prime-residue counts. They conclusively kill the *fixed-modulus sufficiency*
route, not Goldbach.

- Discarded: climbing to any one fixed (2^m) congruence as a sufficient
  decision rule.
- Remaining gap: a noncongruential, all-level bound on the actual q=3 prime
  race.
- Next single lemma: `Q3SpecialPrimeRaceAbsoluteGapAtLeastTwo`.

## F. Twin Prime conjecture — exact proposition first

### Proposition `AllSubthresholdUniqueRootConvergentsAreUnitFree`

Let (p_n/q_n) be the certified convergents to the unique real root used by
the surviving degree-17 branch, and let

\[
V_0=188580743973175296.
\]

Every convergent with (q_n\le V_0) is among (n=0,\ldots,37), and none
satisfies (B_1(p_n,q_n)=\pm1). In fact

\[
q_{37}=110221790993960069\le V_0
 <q_{38}=309742427372962732.
\]

### Proof and exact replay

The certified rational root bracket fixes the first 39 continued-fraction
terms. The exact recurrence makes denominators strictly increase after the
initial repeated denominator one. Direct degree-17 integer evaluation gives
no unit among indices 0 through 37. The displayed threshold crossing and
monotonicity prove that no later convergent can return below (V_0).

This corrects and closes the finite-head subcase left open in TICKET-263. It
does not close the tail. TICKET-263 makes the joint ninth-order congruences
equivalent to the unit equation on the later root cone, but no recurrence or
global obstruction rules out every later congruence pass.

- Discarded: the possibility of an unexamined subthreshold convergent beyond
  the certified head.
- Remaining gap and next single lemma:
  `NoLaterUniqueRootConvergentSatisfiesJointNinthOrderCongruences`.

## G. Adversarial audit

1. The RH sharpness family is not a Weil packet and cannot be promoted to an
   RH proof.
2. The Collatz cutoff is computable from a finite prefix but may be expensive
   to evaluate exactly; its divergence on canonical data is unproved.
3. Goldbach countermodels preserve only the tested integer information; they
   need not be realizable by primes.
4. Twin monotonicity closes only denominators below (V_0); a 39-row
   certificate says nothing by itself about infinitely many later terms.
5. No finite computation establishes an infinite conjecture in this ticket.

## H. Proof DAG summary

Each problem-specific JSON embeds an acyclic DAG with this status pattern:

```text
T263 proved -> T264 proved -> exact finite replay (computed_finite)
                          -> rejected shortcut (disproved)
                          -> next single lemma (open)
```

There is exactly one open frontier per problem and no `heuristic` node on a
resolution path.

## I. Machine verdict

| Problem | New result | Classification | Parent status | Next lemma |
|---|---|---|---|---|
| RH | asymmetric one-sided envelope sum bound, sharp | partial theorem | open_not_proven | `ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit` |
| Collatz | explicit threshold cutoff iff fixed-h cancellation | partial theorem | open_not_proven | `CanonicalFermatQuotientThresholdCutoffDiverges` |
| Strong Goldbach | every fixed two-adic signature has non-tie models | exact no-go | open_not_proven | `Q3SpecialPrimeRaceAbsoluteGapAtLeastTwo` |
| Twin Prime | all subthreshold root convergents are unit-free | partial theorem | open_not_proven | `NoLaterUniqueRootConvergentSatisfiesJointNinthOrderCongruences` |

## J. Claim boundary

Allowed: the four exact bounded statements above, their symbolic proofs, the
declared finite replays, and the named discarded routes.

Blocked: any claim that an actual Weil envelope has been bounded, canonical
Fermat-quotient phases have been proved equidistributed, all q=3 special prime
races are nonzero, all Twin convergents are excluded, or any parent conjecture
has been resolved.

## K. Final status

The iteration is complete. The research program and all four conjectures are
not resolved.
