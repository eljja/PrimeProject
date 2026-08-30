# TICKET-258: Variation, character, and convergent audit

Status: `iteration_complete`; every parent conjecture remains `open_not_proven`.

TICKET-258 continues TICKET-257 without treating any finite computation as an infinite proof. The deep-focus track is Twin Prime because the last exponent-17 Thue branch now admits a qualitative reduction from all denominators to continued-fraction convergents.

## Result boundary

| Problem | Declared proposition | Classification | Resolution |
|---|---|---|---|
| Riemann | Positive convergent packet energies of finite total variation still need not have lag partial sums bounded below. | `exact_no_go` | open |
| Collatz | Nontrivial roots of distinct odd-prime orders, together with 1, are linearly independent over the rationals. | `exact_no_go` | open |
| Strong Goldbach | One primitive odd character detects every reflection asymmetry exactly when `q-1` is a power of two. | `partial_theorem` | open |
| Twin Prime | Every nonzero-denominator unit-coefficient solution on the surviving degree-17 branch is a continued-fraction convergent of its unique real root. | `partial_theorem` | open |

No candidate proof or candidate counterexample to any of the four conjectures is claimed.

## 1. Riemann hypothesis

### Exact proposition

Set

\[
E_{4^k}=1-2^{-k}\quad(k\ge1),\qquad E_L=1\quad\text{otherwise},
\]

and recover the symmetric lag partial sums by

\[
S_n=(n+1)E_{n+1}-nE_n.
\]

Then `E_L >= 1/2`, `E_L -> 1`, and

\[
\sum_{L\ge1}|E_{L+1}-E_L|
=2\sum_{k\ge1}2^{-k}=2,
\]

but

\[
S_{4^k-1}=1-2^k\longrightarrow-\infty.
\]

Thus ordinary bounded total variation does not repair TICKET-257's counterexample. The scale factor in

\[
\sup_L L(E_L-E_{L+1})_+
\]

cannot simply be discarded.

The generator replays 12 exact spike rows with `Fraction`. This is an abstract Toeplitz construction; no actual Guinand-Weil coefficient is calculated. The retained open lemma is:

`ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation`.

## 2. Collatz conjecture

### Exact proposition

Let `q_1,...,q_N` be distinct odd primes and `0 < d_j < q_j`. Then

\[
1,\zeta_{q_1}^{d_1},\ldots,\zeta_{q_N}^{d_N}
\]

are linearly independent over `Q`.

If a rational relation existed, choose a nonzero coefficient of `zeta_(q_j)^(d_j)`. Solving the relation would put that primitive root in the compositum of the other prime-conductor cyclotomic fields. Coprime conductors and degree multiplicativity give intersection `Q`, a contradiction.

The odd-prime and nontrivial-exponent hypotheses are essential: `zeta_2=-1` and an exponent zero gives the rational phase 1. Exact Fermat-quotient replay covers 166 primes through 997 and finds no zero canonical exponent in that finite range. The theorem is unrestricted for any finite family satisfying its hypotheses, but it gives no sublinear magnitude estimate.

The retired route is rationally weighted finite telescoping. The open lemma remains:

`CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude`.

## 3. Strong Goldbach conjecture

### Exact proposition

Let `q` be an odd prime, `n=q-1=2h`, `g` a primitive root, and choose the primitive odd character with `chi(g)=zeta_n`. For residue counts `N_r`, put

\[
A(x)=\sum_{0\le j<h}(N_{g^j}-N_{-g^j})x^j.
\]

The character moment is `A(zeta_n)`. A single primitive odd character detects every reflection asymmetry if and only if `n` is a power of two.

- If `n=2^a`, then `Phi_n(x)=x^h+1` has degree `h`; since `deg A<h`, `A(zeta_n)=0` forces `A=0`.
- Otherwise `n` has an odd prime divisor, so `phi(n)<n/2=h`. The coefficients of `Phi_n` give a nonzero antisymmetric vector of degree below `h` whose primitive moment is exactly zero. Splitting positive and negative coefficients produces nonnegative residue counts, so this is an exact detector counterexample.

For the actual `q=5`, `T=1255` prime prefix, the exact counts are

`[1, 313, 313, 317, 311]`.

With primitive root 2, the antisymmetric half-vector is `[2,-4]`, so the quartic moment is `2-4i`, nonzero. It detects the asymmetry missed by TICKET-257's quadratic bit.

This classifies the detector, not actual prime-prefix nonvanishing. The open lemma remains:

`EveryCompatibleEvenQDivisiblePrimePrefixHasNonzeroOddCharacterMoment`.

## 4. Twin-prime conjecture — deep focus

Let

\[
B_1(u,v)=[\sqrt2](1+\sqrt2)(u+v\sqrt2)^{17},
\qquad P(x)=B_1(x,1),
\]

and let `rho` be the unique root of `P` in `(-1,0)` from TICKET-257.

### Continued-fraction necessity theorem

TICKET-257 shows that a nonzero-denominator solution of `B_1(u,v)=1` reduces, after reflecting negative `v`, to a primitive rational `p/q in [-1,0]` with

\[
P(p/q)=\pm q^{-17}.
\]

From

\[
P'(x)=\frac{17}{2\sqrt2}
\left((1+\sqrt2)(x+\sqrt2)^{16}
+(\sqrt2-1)(x-\sqrt2)^{16}\right)
\]

the second positive term gives, on `[-1,0]`,

\[
P'(x)\ge2176(1-1/\sqrt2)>544.
\]

The mean-value theorem therefore yields

\[
|\rho-p/q|<\frac{1}{544q^{17}}<\frac{1}{2q^2}.
\]

Legendre's continued-fraction criterion forces every solution with `q>=2` to be a convergent of `rho`; `q=1` is checked directly.

The first 128 partial quotients are certified with exact rational root intervals and Möbius transforms. Every convergent is evaluated by integer degree-17 arithmetic. There are no `B_1=+1` or `B_1=-1` hits. Since convergent denominators increase, this excludes every nonzero solution through

`67,076,610,336,720,215,425,112,731,771,403,002,965,838,278,844,687,475,228,751,003`.

This is a 62-digit denominator boundary obtained from only 128 candidates, replacing the previous linear denominator scan by `O(log V)` candidates. Infinitely many later convergents remain. The next lemma is:

`EveryUniqueRootConvergentMissesUnitCoefficient`.

## Reproduction

```powershell
python scripts/ticket258_variation_character_convergent.py
python -m unittest tests.test_ticket258_variation_character_convergent
python scripts/verify_ticket258_structure.py
```

All computations are deterministic. Integers and `Fraction` are used; there is no random seed and no floating-point value is used as proof. The integrated and per-track JSON files contain transcript SHA-256 digests and acyclic proof DAGs with exactly one open frontier per problem.

## Logical limits

- The RH construction is not the actual Weil form.
- Cyclotomic rational independence does not imply analytic cancellation.
- Character-detector completeness does not force actual prime-prefix moments to be nonzero.
- A finite convergent certificate does not exclude all convergents.

Accordingly, TICKET-258 completes an iteration, not any of the four problems.
