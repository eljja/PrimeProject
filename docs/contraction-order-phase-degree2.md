# TICKET-236: Normalized Contractions, Order Witnesses, Reflected Phase Defects, and Degree-Two CRT Reduction

Status: `open_not_proven`
Generated: 2026-08-22
Parent-conjecture resolutions: `0 / 4`

TICKET-236 continues the exact open nodes left by TICKET-235. It proves four
narrower operator, arithmetic, Fourier, or probability statements. It does not
prove or disprove the Riemann hypothesis, the Collatz conjecture, strong
Goldbach, or the twin-prime conjecture.

## 1. Riemann hypothesis track

### Declared proposition

`NormalizedCrossBlockContractionCriterionAndLocalMinorNoGo`.

Let (A,C) be positive definite and

\[
H=\begin{pmatrix}A&B\\B^*&C\end{pmatrix},\qquad
K=A^{-1/2}BC^{-1/2}.
\]

Then

\[
H\succeq0 \quad\Longleftrightarrow\quad \|K\|_{op}\le1.
\]

Coordinatewise relative (2\times2) minor inequalities are not sufficient.
For (A=C=I_m) and (B=(2/m)J_m), every coordinate minor is
(1-4/m^2\ge0) and every entry tends to zero, but
(|B|_{op}=2), so the full block has minimum eigenvalue (-1).

### Argument

Congruence by
\(\operatorname{diag}(A^{-1/2},C^{-1/2})\) reduces the form to
\(\begin{pmatrix}I&K\\K^*&I\end{pmatrix}\). Its Schur complement is
\(I-K^*K\), hence positivity is equivalent to the contraction bound. Since
\(J_m\) has one singular value \(m\), the coherent rank-one counterfamily has
normalized norm two even though all entries are (2/m). The safe comparison
(B=J_m/(2m)) has norm (1/2) and minimum eigenvalue (1/2).

### Reproducible computation and limit

Exact rational rows for (m=4,8,16,32,64,128) verify the local minors,
unsafe eigenvalue (-1), and safe eigenvalue (1/2). These are abstract
Hermitian forms, not the actual Guinand-Weil arithmetic tail. No zeta zero is
tested.

Discarded route: coordinatewise relative minors certify the full form.
Next lemma:
`ArithmeticWeilNormalizedCrossBlockContractionBelowOneOnCofinalLogarithmicFrames`.

## 2. Collatz track

### Declared proposition

`BinaryRunBlockThreePrimeOrderWitnessOutside28826Multiples`.

For the primitive binary word (w_k=1^k2^{2k}), TICKET-197 gives

\[
D_k=32^k-27^k,\qquad B_k=32^k+27^k-2\cdot18^k.
\]

If (28826\nmid k), an explicit prime divides (D_k) but not (B_k):

- (q=5) when (k) is odd;
- (q=59) when (k) is even but (58\nmid k);
- (q=57653) when (58\mid k) but (28826\nmid k).

At (28826\mid k), all three primes divide both (D_k) and (B_k), so this
fixed palette is not universal.

### Argument

TICKET-235 proved that \(q\mid\gcd(D_k,B_k)\) exactly when
\(\operatorname{ord}_q(3/2)\mid k\) and
\(\operatorname{ord}_q(4)\mid k\), while \(q\mid D_k\) exactly when
\(\operatorname{ord}_q(32/27)\mid k\). The three exact order triples are

\[
\begin{array}{c|ccc}
q&\operatorname{ord}(32/27)&\operatorname{ord}(3/2)&\operatorname{ord}(4)\\
5&1&2&2\\
59&2&58&29\\
57653&29&28826&28826.
\end{array}
\]

These orders prove the selector for every integer (k), not merely the tested
range.

### Reproducible computation and limit

The complete period (1\le k\le28826) has coverage counts
(14413,13916,496,1) and zero modular failures. The loop is exhaustive because
the proof establishes period (28826). TICKET-197 already excluded the whole
run-block family; the new contribution is a prime-presence certificate on
28825 residue classes. General binary necklaces, valuations at least three,
and aperiodic trajectories remain open.

Discarded route: the fixed three-prime palette is universal.
Next lemma: `UniformBinaryDensityBandFreshOrderSeparatedPrimeWitnessBeyondFinitePalettes`.

## 3. Strong Goldbach track

### Declared proposition

`ActualPrimeReflectedPhaseDefectIdentityAndUncoupledMarginNoGo`.

Let \(x_X\) be the actual prime indicator on \(\mathbb Z/q\mathbb Z\), where
\(q>2X\), and let

\[
M_X=\sum_a|\widehat x_X(a)|^2=q\pi(X).
\]

For target (N\), define

\[
\Delta_X(N)=\sum_a|\widehat x_X(a)|^2
\left[1-\cos\left(2\arg\widehat x_X(a)-\frac{2\pi aN}{q}\right)\right].
\]

Then, for (0\le N\le2X),

\[
qg_X(N)=M_X-\Delta_X(N),
\]

where \(g_X(N)\) is the ordered prime-pair count. Thus
\(\Delta_X(N)<M_X\) is exactly equivalent to \(g_X(N)>0\), not a smaller
auxiliary lemma. Moreover a cutoff-independent all-target inverse-log margin is
false: at \(N=4\), the normalized margin is
\(g_X(4)/\pi(X)=1/\pi(X)=o(1/\log X)\).

### Argument

Fourier inversion of (x_X*x_X) gives
(qg_X(N)=\sum_a\widehat x_X(a)^2e(-aN/q)). Taking real parts yields the
defect identity; Parseval yields (M_X=q\pi(X)). Because (q>2X), cyclic
wraparound is absent. Only ((2,2)) represents 4, and the prime number theorem
gives (1/\pi(X)\sim\log X/X).

### Reproducible computation and limit

For (X=100,1000,10000,100000), the exact margins are respectively
(1/25,1/168,1/1229,1/9592). Direct complex DFT audits at
(X=30,100,300) agree with the integer inversion identity to below
(5\times10^{-10}). The no-go deliberately decouples a fixed small target from
the growing cutoff; it does not refute a dyadic estimate with (N\asymp X).

Discarded route: an uncoupled all-target (1/\log X) phase margin, or the raw
strict phase inequality as an independent auxiliary.
Next lemma: `TargetCoupledDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack`.

## 4. Twin-prime track

### Declared proposition

`DegreeTwoCesaroEnergyControlsEveryFixedDegree`.

Under the normalized CRT hypotheses of TICKET-235, let (E_{m,k}) be the
degree-(k) Cesàro coefficient energy and assume (|\psi_i|^2\le2). Then

\[
E_{m,1}\le
\sqrt{\frac4m+\frac{m-1}{m}E_{m,2}},
\]

and for every fixed (k\ge2),

\[
E_{m,k}\le
2^{k-2}E_{m,2}+\frac{2^k(1+k(k-1))}{m}.
\]

Consequently (E_{m,2}\to0) forces every fixed-degree energy, including
degree one, to tend to zero.

### Argument

Let \(b_i=\mathbb E_\nu\psi_i\) and
\(M_{ij}=\mathbb E_\nu(\psi_i\psi_j)\). Covariance positivity gives
\(M\succeq bb^*\). Therefore
\(|b|^2\le\|M\|_{op}\le\|M\|_F\). The diagonal entries are at most two,
while the mean squared off-diagonal entries equal (E_{m,2}), proving the
first inequality.

For independent \(X,Y\), put
\(R=m^{-1}\sum_i\psi_i(X)\psi_i(Y)\). Then
\(\mathbb E R^2\le4/m+E_{m,2}\) and \(|R|\le2\). The TICKET-235
with/without-replacement estimate completes the higher-degree bound.

### Reproducible computation and limit

Actual finite twin-start diagnostics use
((X,m,N)=(10^4,4,202),(10^5,6,1220),(10^6,8,8164)). Every rational
degree-one and higher-degree inequality passes. These rows condition on already
existing twin starts and do not prove the required Type-II asymptotic, positive
mass, or a parity-breaking transfer.

Discarded route: estimate every fixed degree independently.
Next lemma: `PrimeWeightedDegreeTwoCRTOverlapEnergyDecayAtTwinScale`.

## Proof DAG and claim boundary

Each track contains one `closed` TICKET-236 theorem, one
`refuted_or_limited` route, one `highest_risk_open` successor, and an
`open_not_proven` parent boundary. The canonical machine DAG is stored in
`data/open-problem/ticket236-contraction-order-phase-degree2.json`.

The exact calculations are finite certificates or instances of separately
proved all-parameter identities. They do not promote numerical evidence into
an infinite conclusion. Resolution count remains zero.
