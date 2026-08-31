# TICKET-263 — sharp envelope, diagonal Weyl cutoff, mod-32 phase, ninth-order exactness

## Decision

This iteration establishes four new partial theorems. It proves or disproves
none of the Riemann hypothesis, Collatz conjecture, strong Goldbach conjecture,
or twin-prime conjecture. The canonical machine record is
`data/open-problem/ticket263-sharp-envelope-diagonal-mod32-ninthorder.json`.

| Problem | Exact proposition | Result | Classification | Status | Next single lemma |
|---|---|---|---|---|---|
| Riemann hypothesis | `A=limsup n|E_n-L|` gives `limsup J_n<=2A`, `liminf S_n>=L-2A`, with optimal factor two | sharp reciprocal envelope | `partial_theorem` | `open_not_proven` | `ActualWeilPacketReciprocalEnvelopeBelowHalfLimit` |
| Collatz | cancellation of every fixed nonzero Weyl harmonic iff uniform cancellation on some growing cutoff | diagonal quantifier reduction | `partial_theorem` | `open_not_proven` | `CanonicalFermatQuotientGrowingCutoffUniformWeylCancellation` |
| Strong Goldbach | a special q=3 tie forces `N_2 mod 32` to be `28,4,12,20` according to `l mod 4` | four-phase tie obstruction | `partial_theorem` | `open_not_proven` | `Q3SpecialMinusOneResidueCountAvoidsLevelPhasedModuloThirtyTwo` |
| Twin prime | beyond an explicit threshold on a root cone, the bidirectional ninth-order pair is equivalent to `B_1(u,v)=epsilon` | ninth-order tail exactness | `partial_theorem` | `open_not_proven` | `NoUniqueRootConvergentSatisfiesJointNinthOrderCongruences` |

## Reproduction contract

```text
python scripts/ticket263_sharp_envelope_diagonal_mod32_ninthorder.py
python -m unittest tests.test_ticket263_sharp_envelope_diagonal_mod32_ninthorder -v
python scripts/verify_ticket263_structure.py
```

Every proof-dependent computation uses integers or `Fraction`. There is no
random seed and no floating-point decision. Transcript SHA-256 values are
stored in the integrated and per-problem JSON records.

## 1. Riemann hypothesis

### Declared proposition

Let `E_n -> L>0` be real and put

```text
A   = limsup n |E_n-L|,
J_n = n(E_n-E_(n+1)),
S_n = (n+1)E_(n+1)-nE_n.
```

Then, in the extended-real sense,

```text
limsup J_n <= 2A,             liminf S_n >= L-2A.
```

Thus `A<L/2` supplies an eventual positive lag margin. The factor two is
optimal.

### Proof and sharp counterfamily

Writing `a_n=E_n-L` gives

```text
J_n <= n|a_n| + [n/(n+1)](n+1)|a_(n+1)|.
```

Taking upper limits proves the first bound. TICKET-262's exact identity
`S_n=E_(n+1)-J_n` proves the second. For every `L,A>0`, the family

```text
E_n=L+(-1)^n A/n
```

satisfies

```text
J_n=(-1)^n A(2n+1)/(n+1),    S_n=L-2(-1)^n A.
```

It attains both constants. At `A=L/2` every even lag is exactly zero, so a
positive margin does not follow. This refutes every smaller universal factor
based only on the reciprocal envelope.

### Computation and limit

The exact replay uses `L=1`, `A=1/3,1/2,2/3`, and `1<=n<=64`, for 192
`Fraction` rows and zero failures. These are not actual Guinand-Weil energies.

- Discard: a universal reciprocal-envelope factor below two.
- Park: arithmetic control of actual packet energies at constant below `L/2`.
- Next lemma: `ActualWeilPacketReciprocalEnvelopeBelowHalfLimit`.

## 2. Collatz conjecture

### Declared proposition

For `x_j in R/Z`, let

```text
W_N(h)=N^(-1) sum_(j<=N) exp(2*pi*i*h*x_j).
```

The following are equivalent:

1. `W_N(h)->0` for every nonzero integer `h`;
2. there is a nondecreasing integer sequence `H_N->infinity` such that
   `max_(1<=|h|<=H_N)|W_N(h)|->0`.

Either condition implies star discrepancy tending to zero by the classical
Weyl criterion.

### Diagonal proof

Condition 2 implies condition 1 because a fixed harmonic eventually lies
below the cutoff. Conversely, for every `m`, choose increasing `N_m` so that
all `N>=N_m` and `1<=|h|<=m` have magnitude at most `1/m`. Define `H_N` as
the largest `m` with `N_m<=N`. Then the moving maximum is at most `1/H_N`.

This does not contradict TICKET-262: the new cutoff depends on the sequence
and grows, while every fixed finite cutoff remains insufficient by itself.

### Computation and limit

Complete grids `j/M`, `M=4,8,16,32,64`, replay 119 exact geometric root sums
and star discrepancy `1/M`. They are triangular models, not canonical
Fermat-quotient prefixes.

- Discard: the claim that all pointwise harmonic limits cannot be packaged
  into any growing uniform cutoff.
- Park: a quantitative schedule for the canonical phases.
- Next lemma: `CanonicalFermatQuotientGrowingCutoffUniformWeylCancellation`.

## 3. Strong Goldbach conjecture

### Declared proposition and proof

Put `T_l=6*3^(6l+2)+3`. A tie between the two nonzero modulo-three residue
counts among the first `T_l` primes forces

```text
N_2=3^(6l+3)+1.
```

The powers of 3 modulo 32 have period eight, while `6l+3` cycles through
`3,1,7,5` modulo eight. Hence the forced residues for `l mod 4=0,1,2,3`
are respectively `28,4,12,20`.

For every `l>=1`, let `M=3^(6l+3)+1`. The pair

```text
(N_1,N_2)=(M-32,M+32)
```

is nonnegative, has the correct total and the same phased `N_2 mod 32`, but
is not tied. The condition is therefore necessary and non-sufficient.

### Exact computation and limit

At actual levels `l=0,1,2`, the observed residues are `31,25,15`, whereas a
tie requires `28,4,12`. Two independent prime-residue counts agree. Symbolic
phase rows cover `0<=l<=15` and replay countermodels cover `1<=l<=15`; the
algebraic phase theorem and the `l>=1` counterfamily are not finite claims.

- Discard: phased modulo 32 as a sufficient all-level tie condition.
- Park: all-level avoidance by actual special prime prefixes.
- Next lemma: `Q3SpecialMinusOneResidueCountAvoidsLevelPhasedModuloThirtyTwo`.

## 4. Twin-prime conjecture — deep focus

### Declared proposition

Define

```text
a_k = C(17,k) 2^floor(k/2),
B_1(u,v) = sum_(k=0)^17 a_k u^(17-k)v^k,
A = sum a_k = 2744210,
V_0 = (A+1)16^9 = 188580743973175296.
```

For coprime nonzero integers `u,v` with `v>V_0` and
`1/16<=|u|/v<=1`, and for `epsilon in {-1,1}`, the equation
`B_1(u,v)=epsilon` is equivalent to

```text
sum_(k=0)^8  a_k u^(17-k)v^k = epsilon (mod v^9),
sum_(k=9)^17 a_k u^(17-k)v^k = epsilon (mod u^9).
```

### Proof

Necessity follows by deleting terms divisible by the ninth power of the
corresponding variable. Conversely, the two congruences and coprimality imply

```text
(|uv|)^9 divides B_1(u,v)-epsilon.
```

Since the coefficients are positive and `|u|<=v`,

```text
|B_1-epsilon| <= (A+1)v^17.
```

The root cone gives `(|uv|)^9>=v^18/16^9`, strictly larger than the upper
bound once `v>V_0`. The difference must therefore be zero. Order nine is the
first product-divisor order whose homogeneous degree `2r` exceeds 17; here it
becomes an exact tail test rather than one more necessary jet.

### Exact computation, adversarial boundary, and limit

Both signs and orders one through nine were tested on 1,024 certified
continued-fraction convergents of the unique real root.

- nontrivial joint ninth-order passes: 0;
- rows where the root-cone size theorem applies: 986;
- first applicable term index: 38;
- final denominator length: 519 digits;
- first joint failure histogram across both signs:
  `r=1:2044`, `r=2:2`, `r=3..9:0`, `no failure through 9:2`.

The last two passes are the two signs at term 0, `(-1,1)`, where the modulus
is one and every congruence is vacuous. They are outside `v>V_0` and the
nontrivial-modulus domain and are retained in a separate JSON certificate.
The initial `u=0` row is also explicitly outside `uv!=0`. Neither boundary is
deleted or counted as a solution.

The computation does not exclude later convergents or every denominator below
the explicit threshold.

- Discard: indefinitely increasing binomial jet order beyond a degree-17 form
  as new independent information.
- Park: all-convergent joint ninth-order exclusion.
- Next lemma: `NoUniqueRootConvergentSatisfiesJointNinthOrderCongruences`.

## Adversarial audit and proof DAG

- Quantifier order and theorem domains are explicit in JSON.
- Finite grids, three actual Goldbach levels, and 1,024 convergents are not
  promoted to infinite conclusions.
- The Twin modulus-one passes and the `u=0` boundary are separated explicitly.
- The Collatz discrepancy transfer is an `external_theorem` node for the
  classical Weyl criterion.
- All four DAGs are acyclic and contain exactly one open resolution frontier.
- `candidate_resolution_count=0`, `resolved_count=0`, and
  `program_complete=false`.

This iteration is complete, but none of the conjectures has been resolved.
