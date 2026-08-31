# TICKET-261: sharpness, Weyl harmonics, special ties, and dual congruences

Status: **iteration complete; all four parent conjectures remain open and unproved.**

TICKET-261 establishes two exact route no-go theorems and two partial theorems. It proves or disproves none of the Riemann hypothesis, Collatz conjecture, strong Goldbach conjecture, or twin-prime conjecture. The canonical machine record is `data/open-problem/ticket261-sharpness-weyl-ties-dualcongruence.json`.

| Problem | Exact proposition attacked | Result | Classification | Parent status |
|---|---|---|---|---|
| Riemann hypothesis | eventual positive packet lag implies summable scaled downward variation | explicit reciprocal-tail counterfamily | `exact_no_go` | `open_not_proven` |
| Collatz conjecture | cancellation of the first growing-modulus Weyl harmonic forces angular discrepancy to zero | exact two-cluster prime-modulus counterfamily | `exact_no_go` | `open_not_proven` |
| Strong Goldbach | a special q=3 prime-race tie is compatible with an arbitrary nonzero residue product | tie forces product `+1 mod 3`; product `-1` excludes it | `partial_theorem` | `open_not_proven` |
| Twin prime | the remaining coefficient-one branch has only the denominator-side second-order congruence | a dual numerator-side congruence and a 1,024-convergent certificate | `partial_theorem` | `open_not_proven` |

## Reproduction contract

```powershell
python scripts/ticket261_sharpness_weyl_ties_dualcongruence.py
python -m unittest tests.test_ticket261_sharpness_weyl_ties_dualcongruence
python scripts/verify_ticket261_structure.py
```

All proof-bearing calculations use integers or `Fraction`. Display floats in fraction records are presentation fields only. There is no random seed. Every transcript has a SHA-256 digest in the machine JSON.

## 1. Riemann hypothesis

### A. Exact proposition

For arbitrary real `L,c>0`, define

\[
E_n=L+\frac{c}{n},\qquad
d_n=(E_n-E_{n+1})_+,\qquad
S_n=(n+1)E_{n+1}-nE_n.
\]

Then `E_n -> L`, every `S_n=L>0`, but

\[
\sum_{n\ge1}n d_n=\infty.
\]

This refutes the proposition that TICKET-260's summable scaled-downward-variation condition is necessary for eventual lag positivity.

### B–D. Definitions, proof, and justification

Direct subtraction gives

\[
d_n=\frac{c}{n(n+1)},\qquad nd_n=\frac{c}{n+1}.
\]

The harmonic series diverges, so the scaled downward variation is not summable. However

\[
nE_n=nL+c,qquad (n+1)E_{n+1}=(n+1)L+c,
\]

and therefore `S_n=L` for every `n`. Every quantifier is pointwise in this explicit infinite family; no finite computation is used to prove divergence or positivity.

### E. Counterexample and boundary attack

The counterfamily satisfies every abstract premise except summability while satisfying the desired conclusion with an exact constant margin. Thus summability cannot be promoted from a sufficient condition to a characterization.

It is not an actual Guinand-Weil packet family. Consequently it refutes only necessity of the abstract hypothesis, not its possible truth for actual packet energies and not RH.

### F–H. Exact replay and finite limit

The generator records `L=c=1` for `1<=n<=128`. Each row independently checks

\[
E_n=1+1/n,\quad d_n=1/[n(n+1)],\quad nd_n=1/(n+1),\quad S_n=1.
\]

The replay is `O(N)` exact rational arithmetic. The infinite conclusion comes from the displayed formulas and harmonic divergence, not from 128 rows. No actual Weil coefficient is computed.

Transcript: `8242a67f0d5c2c2b451cef1cb2c48100ffaa008fa05b402ac6274da8a88b670b`.

### I–K. Classification, remaining gap, and next lemma

- Classification: `exact_no_go`.
- Retired: treating summable scaled variation as necessary for eventual packet-lag positivity.
- Remaining gap: no weaker scaled-jump estimate is established for the actual Guinand-Weil packet energies.
- Next single lemma: `ActualWeilPacketScaledDownwardJumpLimsupBelowLimit`.

## 2. Collatz conjecture

### A. Exact proposition

There exist strictly increasing odd primes `q_j` and integers `1<=d_j<q_j` such that

\[
\frac1N\sum_{j\le N}\exp(2\pi i d_j/q_j)\longrightarrow0,
\]

but the star discrepancy of `x_j=d_j/q_j` has lower limit at least `1/6`. Therefore cancellation of the first Weyl harmonic alone does not imply angular equidistribution on growing prime moduli.

### B–D. Construction and proof

Choose `q_j` recursively as the least prime above `max(q_(j-1),j^3,13)`. Put

\[
d_j=\lfloor q_j/4\rfloor\quad(j\text{ odd}),\qquad
d_j=\lfloor3q_j/4\rfloor\quad(j\text{ even}).
\]

The normalized points lie within `1/q_j` of `1/4` and `3/4`. Their ideal first-harmonic phases are `i,-i,i,-i,...` and cancel in pairs. Using `pi<4` and the chord bound,

\[
|e^{2\pi i d_j/q_j}-e^{2\pi i/4}|\le 8/q_j
\]

on odd indices, with the analogous even bound. Since `q_j>j^3` and `sum j^(-3)<2`, the non-ideal total error is bounded by `16`; after division by `N`, the first harmonic tends to zero.

Exactly `ceil(N/2)` points lie in `[0,1/3)`. Hence

\[
D_N^*\ge \frac{\lceil N/2\rceil}{N}-\frac13\longrightarrow\frac16.
\]

This is an exact countermodel on the declared growing-prime-modulus domain.

### E. Adversarial and canonical checks

The construction is deliberately not the canonical Fermat-quotient sequence. It proves that a proposed one-harmonic implication is invalid; it does not determine the canonical sequence.

For a separate exact finite diagnostic, define for each prime `q>5`

\[
F_q(a)=\frac{a^{q-1}-1}{q}\pmod q,qquad
D_q=5F_q(2)-3F_q(3)\pmod q.
\]

The star discrepancy of the first `2^k` canonical points `D_q/q` is computed exactly for `k=3,...,14`. It is not monotone on these dyadic prefixes: the first increase is from 2,048 to 4,096, and another occurs at 16,384. This is a finite counterexample to monotone-prefix extrapolation, not evidence against eventual discrepancy decay.

### F–H. Reproducible calculation and finite limit

- Countermodel: 128 exact prime-modulus rows and rational chord envelopes.
- Canonical diagnostic: 16,384 primes through `q=180539`, 12 exact dyadic discrepancies.
- Exact values include `D_2048*=111589/7366144` and `D_4096*=656411/39704576`, with the latter larger.
- Complexity: deterministic prime search plus `O(P log P)` exact fraction sorting and modular exponentiation.
- No complex floating-point root is evaluated.

Transcript: `35619c4243f9a4fa6ba7eff5764787d0ee3212d8f9decca0e85938e01b2de750`.

The finite canonical table cannot prove a limiting discrepancy statement.

### I–K. Classification, remaining gap, and next lemma

- Classification: `exact_no_go`.
- Retired: deriving angular discrepancy decay from only the first growing-modulus Weyl harmonic.
- Remaining gap: no cancellation theorem exists for every nonzero harmonic of the canonical Fermat-quotient angles.
- Next single lemma: `CanonicalFermatQuotientWeylSumsVanishForEveryNonzeroH`.

## 3. Strong Goldbach conjecture

### A. Exact proposition

For `l>=0`, let

\[
T_l=6\cdot3^{6l+2}+3
\]

and let `P_l` be the product modulo 3 of the first `T_l` primes after omitting the prime 3. If the mod-3 prime race ties at `T_l`, then

\[
P_l\equiv1\pmod3.
\]

Contrapositively, `P_l=-1 mod 3` is a sufficient exact certificate excluding the compatible prefix from TICKET-260.

### B–D. Definitions and proof

Beyond the prime 3, every prime has residue `+1` or `-1` modulo 3. A tie has

\[
N_1=N_2=(T_l-1)/2=3\cdot3^{6l+2}+1.
\]

Because `3^(6l+2)` is odd, this common count is even. Therefore the product of all nonzero residue symbols is

\[
(+1)^{N_1}(-1)^{N_2}=+1\pmod3.
\]

The contrapositive supplies the advertised product-minus-one certificate.

### E. Density-only no-go

Prepend one zero symbol and then alternate `+1,-1` forever. Every ordinary prefix discrepancy is at most one and both nonzero symbol densities tend to one half. Nevertheless `T_l-1` is even for every `l`, so every special prefix is an exact tie and has product `+1`.

Thus PNT-in-progressions-scale density balance, even strengthened to bounded discrepancy in this abstract residue model, cannot by itself exclude exact sparse ties. This sequence is not claimed to be the prime residue sequence.

### F–H. Exact certificates and finite limit

The two independent TICKET-260 residue algorithms are reused at `l=0,1,2`. Their actual counts give odd `N_2` and hence `P_l=-1 mod 3` in all three cases:

| `l` | `T_l` | endpoint | `(N_0,N_1,N_2)` | `P_l mod 3` |
|---:|---:|---:|---:|---:|
| 0 | 57 | 269 | `(1,25,31)` | 2 |
| 1 | 39,369 | 471,749 | `(1,19,663,19,705)` | 2 |
| 2 | 28,697,817 | 547,035,959 | `(1,14,347,849,14,349,967)` | 2 |

Sixteen symbolic alternating levels replay the all-level no-go. The actual prime calculation still covers only three levels.

Transcript: `7c01ec5d388159c3ba032b8f87459f71cbd4bc339f2f181ef6bc6113075d810c`.

### I–K. Classification, remaining gap, and next lemma

- Classification: `partial_theorem`.
- Retired: density balance alone as an exact non-tie certificate.
- Remaining gap: no theorem gives `P_l=-1 mod 3` at every special prime prefix.
- Next single lemma: `Q3SpecialPrimePrefixProductIsMinusOneModuloThree`.

## 4. Twin-prime conjecture — deep focus

### A. Exact proposition

Let `B_1(u,v)` be the integer coefficient of `sqrt(2)` in

\[
(1+\sqrt2)(u+v\sqrt2)^{17}.
\]

For integers `u,v` with `uv!=0` and `epsilon in {-1,1}`, the equality `B_1(u,v)=epsilon` forces both

\[
u^{17}+17u^{16}v\equiv\epsilon\pmod{v^2}
\]

and

\[
256v^{17}+4352uv^{16}\equiv\epsilon\pmod{u^2}.
\]

Both signs fail the joint condition on the first 1,024 certified continued-fraction convergents of the unique root isolated in TICKET-258.

### B–D. Expansion and proof

At the low-`v` end of the homogeneous form,

\[
B_1(u,v)=u^{17}+17u^{16}v+v^2R(u,v).
\]

At the low-`u` end, the last two binomial coefficients are

\[
2^8v^{17}=256v^{17},\qquad 17\cdot2^8uv^{16}=4352uv^{16},
\]

so

\[
B_1(u,v)=256v^{17}+4352uv^{16}+u^2Q(u,v).
\]

Reduction modulo `v^2` and `u^2` proves the two necessary conditions. No root approximation is used in these congruence derivations.

### E. Counterexamples to the weaker route

The denominator first-order condition still admits `(-1,13,-1)` and `(-1,14,-1)`. The nontrivial numerator first-order condition admits `(-3,41,-1)`, which fails modulo `u^2`. Hence first-order numerator/denominator filtering is not a complete replacement for the second-order pair.

None of these witnesses satisfies `B_1(u,v)=epsilon`; they are exact counterexamples only to completeness of the necessary first-order filter.

### F–H. Reproducible calculation and finite limit

For each of 1,024 certified convergents and each sign, the generator:

1. computes both first-order residues;
2. computes the truncated residues modulo `v^2` and `u^2`;
3. independently evaluates the full integer `B_1`;
4. checks both truncated residues against the full value;
5. hashes the full coefficient and records the rational root bracket.

The final denominator has 519 digits. Counts are:

- denominator first-order nontrivial passes: 2;
- denominator second-order passes: 0;
- numerator first-order nontrivial passes: 1;
- numerator second-order nontrivial passes: 0;
- joint second-order passes: 0.

Complexity is linear in the number of certified convergents, with modular operations on growing exact integers. The absence of a hit in 1,024 rows is a finite certificate only.

Transcript: `3327f229884ca78a1b95a3b2336cc245e4e99cbfff8f2020a24db3299754b70e`.

### I–K. Classification, remaining gap, and next lemma

- Classification: `partial_theorem`.
- Retired: using both first-order congruences as a complete convergent filter.
- Remaining gap: infinitely many later unique-root convergents remain uncontrolled.
- Next single lemma: `NoUniqueRootConvergentSatisfiesBothSecondOrderCongruences`.

## Adversarial proof audit

- Quantifiers: every unrestricted statement is proved symbolically; all finite prefixes are explicitly labelled finite.
- Uniformity: no pointwise conclusion is promoted to a uniform actual-Weil, canonical-angle, all-level prime-race, or all-convergent theorem.
- Domains: the Collatz no-go uses genuine distinct prime moduli but noncanonical exponents; the Goldbach alternating sequence is explicitly abstract; the Twin congruences use nonzero integer `u,v`.
- Denominators: `u=0` is separately outside the dual congruence statement and cannot solve `B_1(u,v)=±1`; modulus signs use `|u|` and positive `v` on the certified branch.
- Independent checks: Goldbach retains two residue algorithms; Twin compares two truncations to the full form; Collatz recomputes exact Fermat quotients and sorted discrepancy witnesses.
- Proof DAG: each track has one proved predecessor, one proved TICKET-261 theorem, one finite certificate, one disproved route, and exactly one open frontier. All four DAGs are acyclic.

## Final claim boundary

Newly established: two exact route no-go theorems and two partial theorems. Retired: necessity of RH scaled-variation summability, one-harmonic Collatz discrepancy transfer, density-only Goldbach tie exclusion, and bidirectional first-order Twin filtering. Unproved: every actual-Weil estimate, every all-harmonic canonical Fermat-quotient estimate, the all-level q=3 product sign, the all-convergent second-order exclusion, and all four parent conjectures.
