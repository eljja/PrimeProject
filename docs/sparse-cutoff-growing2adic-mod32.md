# TICKET-265 — sparse-envelope and cutoff no-go theorems, a growing two-adic tie test, and a mod-32 Twin filter

## Verdict

TICKET-265 is complete, but none of the four parent conjectures is proved or disproved. The round establishes two `exact_no_go` results and two `partial_theorem` results. Collatz is the deep-focus track. The canonical machine artifact is `data/open-problem/ticket265-sparse-cutoff-growing2adic-mod32.json`; every problem also has a track-local JSON file and an acyclic proof DAG with one open frontier.

Reproduction:

```text
python scripts/ticket265_sparse_cutoff_growing2adic_mod32.py
python -m unittest tests.test_ticket265_sparse_cutoff_growing2adic_mod32 -v
python scripts/verify_ticket265_structure.py
```

All arithmetic in the generator is exact integer or `Fraction` arithmetic. The Twin continued fraction uses the previously certified rational root bracket. The three actual Goldbach rows are read from a SHA-256-pinned TICKET-260 certificate; this round runs no new prime sieve.

## 1. Riemann Hypothesis

### Declared proposition

`DensityOneReciprocalControlCannotReplaceLimsupEnvelope`.

Let `L>0` and `P,M>=0` with `P+M>L`. For all sufficiently large `k`, define

```text
a_(2^k)   = P/2^k,
a_(2^k+1) = -M/(2^k+1),
a_n       = 0 otherwise,
E_n       = L+a_n.
```

Then `E_n>0`, `E_n -> L`, the nonzero-error support has natural density zero and arbitrarily long zero-error gaps, but

```text
A_+ = limsup n(a_n)^+ = P,
A_- = limsup n(a_n)^- = M,
S_(2^k) = (2^k+1)E_(2^k+1)-2^k E_(2^k) = L-P-M < 0.
```

### Argument and computation

There are at most `2(log_2 X+1)` exceptional indices up to `X`, proving density zero. The scaled errors are exactly `P` and `M` on their respective spike subsequences and zero elsewhere. Direct substitution proves the negative lag identity. The replay fixes `L=1`, `P=3/4`, `M=1/2` and checks `k=2,...,17`; every lag is exactly `-1/4`.

### Boundary and route decision

This is an abstract sequence counterexample, not a Guinand–Weil packet. It rigorously discards density-one or sparse packet sampling as a sufficient replacement for the all-index TICKET-264 envelope. It neither proves nor disproves RH. The remaining gap is the arithmetic estimate `A_++A_-<L` for actual packet energies.

Next single lemma: `ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit`.

## 2. Collatz conjecture — deep focus

### Declared proposition

`UnboundedExplicitThresholdCutoffDoesNotImplyDivergence`.

There is an explicit sequence in `R/Z` for which the TICKET-264 threshold cutoff `K_N` is unbounded, but does not tend to infinity. Starting with the complete four-point grid, at each dyadic `q=2^r`, regard the preceding `q/2` grid as the even `q`-th roots, append first the `q/4` odd roots in the argument arc `(-pi/2,pi/2)`, and then append the other odd roots.

At the endpoint `N=q`, the prefix is the complete `q`-grid and `K_q=q-1`. At `N=3q/4`, the old first-harmonic sum is zero and the appended geometric sum has magnitude `csc(2pi/q)`. Since `sin x<x` and `pi<22/7`,

```text
|W_N(1)| > 7/33 > 1/6.
```

Thus harmonic `H=6` fails and `K_N<=5`. Therefore `limsup K_N=infinity` while `liminf K_N<=5`.

### Computation and no-go

The exact replay checks `q=8,...,2048` over nine powers of two, using integer enumeration and the rational comparison `7/33>1/6`; no floating-point trigonometry is treated as proof. This gives a genuine infinite construction, not merely a finite pattern.

The result discards the route “arbitrarily large finite cutoff certificates, or unbounded `K_N`, imply pointwise Weyl cancellation.” It does not concern the canonical fixed-base Fermat-quotient sequence, so Collatz remains open.

Next single lemma: `CanonicalFermatQuotientThresholdCutoffHasNoBoundedSubsequence`.

## 3. Strong Goldbach conjecture

### Declared proposition

`GrowingTwoAdicTieSignatureIsSharpAndDecisive`.

Let `M>=1` and let nonnegative integers `N_1,N_2` satisfy `N_1+N_2=2M`. The congruence

```text
N_2 = M (mod 2^m)
```

forces `N_1=N_2=M` for every such pair if and only if `2^m>M`.

Indeed, write `N_1=M-d`, `N_2=M+d`. Then `|d|<=M` and `2^m|d`. If `2^m>M`, only `d=0` is possible. If `2^m<=M`, `d=2^m` is an explicit non-tie countermodel.

For the special-prefix value `M_l=3^(6l+3)+1`, the least decisive exponent is therefore `m_l=bit_length(M_l)`. Exponent `m_l-1` is always insufficient, witnessed by `(M_l-2^(m_l-1), M_l+2^(m_l-1))`.

### Computation and boundary

The generator checks the sharp threshold and countermodel for all `l=0,...,31`. It also replays the three certified actual levels `l=0,1,2` from TICKET-260 and confirms decisive-residue mismatch there. Those three levels do not imply all-level mismatch.

This repairs a logical overreading of TICKET-264: fixed two-adic information is insufficient, but a sufficiently growing modulus decides the abstract equality exactly. The open arithmetic gap is to show that the actual modulo-three prime count avoids the decisive residue for every level.

Next single lemma: `Q3ActualMinusCountAvoidsLeastDecisiveTwoAdicTieResidue`.

## 4. Twin prime conjecture

### Declared proposition

`PrimitiveTwinUnitSolutionsObeyMod32DiagonalFilter`.

For

```text
B_1(u,v)=sum_(k=0)^17 C(17,k) 2^floor(k/2) u^(17-k)v^k,
```

if `gcd(u,v)=1` and `B_1(u,v)=epsilon` with `epsilon in {+1,-1}`, then `u` is odd, `v` is even, and

```text
u+v = epsilon (mod 32).
```

Modulo two, the other primitive parity classes make `B_1` even. For odd `u` and even `v`, `u^16=1 (mod 32)`. The `k=0,1` terms reduce to `u+v`, while each `k>=2` term has two-adic valuation at least five. Hence `B_1(u,v)=u+v (mod 32)`.

The condition is not sufficient. For every `t>=1`, `(1,32t)` is primitive and passes the `+1` filter but has `B_1>1`; odd-degree homogeneity gives the corresponding negative countermodel `(-1,-32t)`.

### Computation and boundary

The replay checks the 16 coefficient valuations, 32 paired countermodels, and the first 1,024 certified unique-root convergents. Of these convergents, 332 have even denominator; 21 pass the `+1` diagonal, 14 pass the `-1` diagonal, and 35 pass either. Thirty-three survivors lie in the open `n>=38` tail. These are filter survivors, not unit solutions.

The mod-32 filter is a rigorous cheap front end, but its sufficiency route is refuted. The infinite tail still requires the exact ninth-order congruence exclusions from TICKET-263.

Next single lemma: `EveryLaterMod32FilterPassFailsJointNinthOrderCongruences`.

## Classification summary

| Problem | New result | Classification | Parent status | Discarded route | Remaining gap | Next lemma |
|---|---|---|---|---|---|---|
| RH | Density-one reciprocal control cannot replace the all-index envelope | exact no-go | open | density-one/sparse sampling suffices | actual packet `A_++A_-<L` | `ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit` |
| Collatz | unbounded `K_N` need not diverge | exact no-go | open | sparse good prefixes imply cancellation | canonical `K_N` has no bounded subsequence | `CanonicalFermatQuotientThresholdCutoffHasNoBoundedSubsequence` |
| Strong Goldbach | least growing two-adic modulus decides abstract tie sharply | partial theorem | open | fixed-modulus no-go excludes all growing signatures | actual decisive-residue avoidance for all levels | `Q3ActualMinusCountAvoidsLeastDecisiveTwoAdicTieResidue` |
| Twin prime | primitive unit solutions satisfy a necessary mod-32 diagonal | partial theorem | open | local mod-32 filter is sufficient | ninth-order exclusion of every later survivor | `EveryLaterMod32FilterPassFailsJointNinthOrderCongruences` |

Iteration complete does not mean conjecture resolved. Resolution count and candidate-resolution count are both zero.
