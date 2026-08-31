# TICKET-262: exact limsup threshold, finite-harmonic no-go, mod-8 tie obstruction, and third-order congruences

Status: **iteration complete; all four parent conjectures remain open and unproved.**

TICKET-262 establishes three partial theorems and one exact route no-go theorem. It proves or disproves none of the Riemann hypothesis, Collatz conjecture, strong Goldbach conjecture, or twin-prime conjecture. The canonical machine record is `data/open-problem/ticket262-limsup-finiteharmonic-mod8-thirdorder.json`.

| Problem | Exact proposition attacked | New result | Classification | Parent status |
|---|---|---|---|---|
| Riemann hypothesis | eventual positive packet lag has an exact abstract scaled-jump threshold | `liminf S_n=L-limsup J_n`; positive margin iff `limsup J_n<L` | `partial_theorem` | `open_not_proven` |
| Collatz conjecture | some fixed finite Weyl cutoff forces angular discrepancy to zero | counterfamily for every fixed finite cutoff | `exact_no_go` | `open_not_proven` |
| Strong Goldbach | a special q=3 tie has no stronger count congruence beyond product parity | a tie forces `N_2=4 mod 8`, with two sharpness models | `partial_theorem` | `open_not_proven` |
| Twin prime | second-order congruences are the sharpest finite jet on the exponent-17 branch | bidirectional third-order congruences and a 1,024-convergent certificate | `partial_theorem` | `open_not_proven` |

## Reproduction contract

```powershell
python scripts/ticket262_limsup_finiteharmonic_mod8_thirdorder.py
python -m unittest tests.test_ticket262_limsup_finiteharmonic_mod8_thirdorder
python scripts/verify_ticket262_structure.py
```

All proof-bearing calculations use integers or `Fraction`; no random seed or floating-point predicate is used. Each deterministic transcript has a SHA-256 digest in the JSON.

## 1. Riemann hypothesis

### Exact proposition

Let `E_n` be a real sequence with `E_n -> L>0`, and define

\[
J_n=n(E_n-E_{n+1}),\qquad S_n=(n+1)E_{n+1}-nE_n.
\]

Then, in the extended-real sense,

\[
\liminf S_n=L-\limsup J_n.
\]

Consequently, there are `delta>0` and `N` such that `S_n>=delta` for all `n>=N` if and only if `limsup J_n<L`.

### Proof and adversarial boundary

For every `n`, direct algebra gives

\[
S_n=E_{n+1}-J_n.
\]

Adding a convergent sequence shifts liminf/limsup by its limit, which proves the displayed identity. An eventual margin gives `liminf S_n>0`, hence `limsup J_n<L`. Conversely, if the limsup is strictly below `L`, split the positive gap in half and apply the definitions of convergence and limsup.

The exact replay checks `E_n=1+1/n` for `1<=n<=64`: `J_n=1/(n+1)` and `S_n=1`. The critical family uses `n=4^k`, `E_n=1`, `E_(n+1)=1-1/n`, for `1<=k<=12`: `J_n=1` but `S_n=-1/n`. Thus equality at the threshold is genuinely insufficient.

This equivalence identifies the minimal abstract target and retires stronger summability conditions as the target itself. It does not establish the strict bound for actual Guinand-Weil packet energies and therefore does not decide RH.

- Finite boundary: 64 strict and 12 critical exact rational rows; no actual Weil packet.
- Transcript: `1d0e796a1808951ac38617fabf4e338df387ff4653b8c1f9461e2e211b2c2e95`.
- Remaining gap: prove the strict arithmetic limsup inequality for actual packets.
- Next lemma: `ActualWeilPacketScaledDownwardJumpLimsupBelowLimit`.

## 2. Collatz conjecture — deep focus

### Exact proposition

For every integer `H>=1`, there are strictly increasing odd primes `q_j` and integers `1<=d_j<q_j` such that, for every nonzero `|h|<=H`,

\[
\frac1N\sum_{j\le N}e^{2\pi i h d_j/q_j}\longrightarrow0,
\]

while the star discrepancy of `d_j/q_j` has liminf at least `1/[4(H+1)]`. Hence no fixed finite Weyl-harmonic cutoff implies angular equidistribution for growing prime moduli.

### Construction and proof

Put `M=H+1`, cycle `r_j=(j-1) mod M`, and set

\[
y_j=\frac{2r_j+1}{2M}.
\]

Choose `q_j` as the least prime above `max(q_(j-1),j^3,8M)` and put `d_j=floor(q_j y_j)`. For `1<=|h|<=H`, every complete ideal `M`-block is a geometric sum of all `M`-th roots with a common half-step rotation, and is zero because `h` is not divisible by `M`.

Moreover `0<=y_j-d_j/q_j<1/q_j`, so the chord error is less than `8|h|/q_j`. Since `q_j>j^3`, the total error is summable; after normalization by `N`, it tends to zero.

The interval `[0,3/(4M))` contains exactly the `r_j=0` cluster. Its limiting empirical mass is `1/M`, whereas its length is `3/(4M)`, giving discrepancy at least `1/(4M)`.

This all-`H` construction strictly generalizes the first-harmonic no-go from TICKET-261. It is noncanonical: it does not establish or refute Weyl cancellation for the Fermat-quotient angles arising in the Collatz reduction.

- Exact replay: `H=1,2,4,8,16`, 32 complete blocks each, 1,152 phase cases.
- Calculation: exact prime construction, rational point errors, symbolic root-of-unity cancellation, and rational chord envelopes.
- Transcript: `fc9aa7f31e40f14a0005fe7d75fc732aca63add7bee8ff6fa258f4e733f4d023`.
- Retired route: any fixed finite harmonic truncation as sufficient for discrepancy decay.
- Remaining gap: all nonzero harmonics of the canonical Fermat-quotient sequence.
- Next lemma: `CanonicalFermatQuotientWeylSumsVanishForEveryNonzeroH`.

## 3. Strong Goldbach conjecture

### Exact proposition

For `l>=0`, put

\[
T_l=6\cdot3^{6l+2}+3.
\]

If the nonzero mod-3 residue counts among the first `T_l` primes tie, then

\[
N_2=\frac{T_l-1}{2}=3^{6l+3}+1\equiv4\pmod 8,
\]

and therefore `v_2(N_2)=2`. Its contrapositive says that `N_2` not congruent to 4 modulo 8 exactly excludes a tie.

### Proof, countermodels, and finite certificates

The count formula follows from a tie and the single omitted zero residue. Since `6l+3` is odd, `3^(6l+3)=3 mod 8`; adding one proves the congruence and exact 2-adic valuation.

Two synthetic count-vector families delimit the claim:

1. If the tied count is `m`, then `(N_1,N_2)=(m-2,m+2)` is a non-tie with even `N_2` and residue-product `+1 mod 3`. Thus TICKET-261's product-minus-one certificate is sufficient, not necessary.
2. `(N_1,N_2)=(m-8,m+8)` is a non-tie with `N_2=4 mod 8`. Thus the new congruence is necessary, not sufficient.

At the three exactly computed actual levels `l=0,1,2`, the minus-one counts are `31`, `19705`, and `14349967`, with residues `7,1,7 mod 8`; each excludes the corresponding tie. Independent prime-residue algorithms agree. Three levels cannot prove the all-level assertion needed by the reduction.

- Transcript: `7c60dd5c0e26f01fcd138fba2088f29872ee60b43e25efe5fc6dbad0cce5e00f`.
- Retired route: requiring product `-1 mod 3` as a necessary characterization of non-tie.
- Remaining gap: exclude `N_2=4 mod 8` at every actual special prefix.
- Next lemma: `Q3SpecialMinusOneResidueCountNeverFourModuloEight`.

## 4. Twin-prime conjecture

### Exact proposition

Let `B_1(u,v)` be the degree-17 homogeneous coefficient form from TICKET-257. If `uv!=0` and `B_1(u,v)=epsilon` for `epsilon` in `{-1,1}`, then

\[
u^{17}+17u^{16}v+272u^{15}v^2\equiv\epsilon\pmod{v^3},
\]

and

\[
256v^{17}+4352uv^{16}+17408u^2v^{15}\equiv\epsilon\pmod{u^3}.
\]

### Proof and exact certificate

On the denominator side, the coefficients through `v`-degree two are

\[
1,\quad17,\quad {17\choose2}2=272;
\]

all later terms are divisible by `v^3`. At the opposite end, the coefficients through `u`-degree two are

\[
2^8=256,\quad17\cdot2^8=4352,\quad {17\choose15}2^7=17408;
\]

all remaining terms are divisible by `u^3`. Reduction proves both necessary congruences.

For both signs on each of the first 1,024 certified continued-fraction convergents of the unique real root, the truncated residues are independently compared with the full exact `B_1` value modulo `v^3` and `|u|^3`. There are no denominator-side, numerator-side, or joint third-order passes, and no direct unit coefficient hit. The final denominator has 519 decimal digits.

This is a finite certificate, not a proof over all convergents. It neither closes the exponent-17 Diophantine branch nor proves the twin-prime conjecture.

- Transcript: `50287b950ca162a0f762bbe7b4ba0d0898871947e950e7e1f52168d4f5e197cd`.
- Retired route: treating second order as the sharpest available finite jet.
- Remaining gap: exclude the joint third-order pair on every later unique-root convergent.
- Next lemma: `NoUniqueRootConvergentSatisfiesBothThirdOrderCongruences`.

## Proof DAG and completion boundary

Each track has the same audited shape:

```text
TICKET-261 result -> TICKET-262 theorem -> exact finite replay
                                      \-> disproved shortcut
                                      \-> one open next lemma
```

Every DAG is acyclic and has exactly one open frontier. Machine totals are: 4 exact theorems, 3 partial theorems, 1 exact no-go, 0 candidate resolutions, 0 conjecture resolutions, 4 proof DAGs, and 4 next lemmas. `iteration_complete=true` and `program_complete=false`.

This iteration is complete, but none of the four conjectures has been resolved.
