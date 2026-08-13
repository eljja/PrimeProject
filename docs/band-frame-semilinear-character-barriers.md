# TICKET-229: Band Frames, Semilinear Coverage, and Character Barriers

Korean edition: [band-frame-semilinear-character-barriers.ko.md](band-frame-semilinear-character-barriers.ko.md)

## Abstract and claim boundary

TICKET-229 tests the four successor lemmas left by TICKET-228. It proves four
exact partial or no-go theorems, records reproducible finite audits, and selects
one remaining lemma per problem. It proves or disproves none of the Riemann,
Collatz, strong Goldbach, or Twin Prime conjectures. The machine resolution
count remains `0/4`.

| Problem | Exact result closed here | Route discarded or narrowed | Single next lemma |
|---|---|---|---|
| Riemann hypothesis | An explicit positive lower bound for the dual-dilation energy on every finite band | The elementary exponential lower bound can be matched by a merely polynomial truncation error | `SubexponentialDualDilationLossMatchedToExplicitWeilCoreTail` |
| Collatz conjecture | Every fixed-suffix equal-slope language lies on one affine `(h,S)` line; no finite union is cofinal among primitive positive-denominator words | Finitely many such languages can cover all sufficiently long cycle-candidate words | `OrderSensitiveNondivisibilityForAllPositiveDenominatorPrimitiveWords` |
| Strong Goldbach conjecture | Complete target-residue averaging annihilates every nonconstant local character exactly | Target averaging implies pointwise cancellation for each fixed even target | `PrimeWeightedPointwiseCharacterCancellationForEachGoldbachFactorCell` |
| Twin Prime conjecture | Shift-two symmetry kills odd characters, but the modulo-5 quadratic character survives at full normalized size | Tensoring additional unweighted local factors produces uniform character contraction | `PrimeWeightedCancellationOfModuloFiveQuadraticShiftTwoMode` |

The common result is a separation theorem. Finite-band positivity is not a
usable asymptotic inverse without a compatible tail estimate; a large regular
Collatz language is not a cofinal language; averaged character cancellation is
not pointwise cancellation; and local tensorization does not defeat a mode
already normalized to one.

## 1. Riemann hypothesis

### Proposition RH-229

Define

```text
F(tau)=|1-2^(-i tau)|^2+|1-3^(-i tau)|^2.
```

For `T >= pi/log(3)` and `pi/log(3) <= |tau| <= T`,

```text
F(tau) >= 16 exp(-T log(2)log(3)/pi-log(3))
          / (log(2)^2+log(3)^2).                         (RH-229.1)
```

Thus every finite band has a strictly positive explicit lower frame bound.
The reciprocal certificate grows exponentially with `T`. Consequently this
specific elementary certificate cannot absorb an error known only to decay as
`C T^(-k)` for fixed positive `C,k`.

### Proof

By evenness it suffices to take positive `tau`. Put

```text
x=tau log(2)/(2 pi),  y=tau log(3)/(2 pi),
```

and let `n,m` be nearest integers. Write `delta_2=|x-n|` and
`delta_3=|y-m|`. Both are at most `1/2`, and the chord bound
`|sin(pi u)| >= 2|u|` on that interval gives

```text
F(tau) >= 16(delta_2^2+delta_3^2).                       (RH-229.2)
```

Since `x log(3)=y log(2)`,

```text
Lambda=n log(3)-m log(2)
      =(n-x)log(3)-(m-y)log(2).
```

Cauchy-Schwarz bounds `|Lambda|` by the square root of the right side of
`(RH-229.2)/16` times `sqrt(log(2)^2+log(3)^2)`. The lower band endpoint makes
`m>=1`; also `n>=0`, and `3^n != 2^m` by unique factorization. For distinct
positive integers `A,B`,

```text
|log(A/B)| >= 1/max(A,B).
```

Moreover,

```text
max(3^n,2^m)
 <= exp(T log(2)log(3)/(2 pi)+log(3)/2).
```

Combining these inequalities and squaring proves `(RH-229.1)`. Finally,
`exp(-cT)=o(T^(-k))` for every fixed `k`, so a positive polynomial error is
eventually larger than this lower bound.

### Computation and limit

The audit checks the phase inequalities on seven representative frequencies
and evaluates `(RH-229.1)` on eight bands through `T=5000`. The certified
base-10 lower bound decreases from about `-0.553` at `T=10` to about `-525.85`
at `T=5000`; a model `T^-12` error becomes larger than the certificate by
`T=500`.

The analytic inequalities, not those samples, prove RH-229. The theorem does
not construct the actual Weil quadratic-form core, prove its operator lower
bound, or supply a matching explicit truncation tail. It therefore proves no
RH implication. The next admissible target must obtain subexponential
conditioning or an explicit Weil-core tail small enough for the same loss.

## 2. Collatz conjecture

### Proposition CO-229

Represent a positive valuation word by its height `h` and valuation sum `S`.
A block of height `k` and sum `s` has normalized affine slope `3^k/2^s`.
Every language formed by concatenating blocks of one common normalized slope
and then appending one fixed suffix lies on one affine line in the integer
`(h,S)` plane. No finite union of such languages is cofinal among all primitive
positive-denominator valuation words.

More explicitly, after choosing an integer `c>=1` avoiding the finitely many
parallel intercepts, the words

```text
w_(h,c)=(c+2,2,...,2),  S=2h+c                            (CO-229.1)
```

are primitive and satisfy `D=2^S-3^h>0`. Every nonparallel language intersects
this family at most once, so all sufficiently large `h` give uncovered words.

### Proof

If two blocks have equal normalized slope, then

```text
3^k1/2^s1 = 3^k2/2^s2.
```

Unique factorization forces `k1=k2` and `s1=s2`. Concatenating `r` such blocks
and a fixed suffix `(h0,s0)` therefore gives

```text
(h,S)=(rk+h0, rs+s0),
```

which obeys one affine linear equation. A finite collection produces finitely
many lines. Select `c` so that `S=2h+c` is not one of the parallel lines. Each
remaining line meets it in at most one point.

For `h>=2`, `(CO-229.1)` has one exceptional entry and all other entries equal
to two, so it cannot be a nontrivial repetition. It is primitive. Also

```text
2^S=2^c 4^h > 3^h,
```

which proves `D>0`. Removing the finitely many intersections leaves an
unbounded family outside the proposed finite cover.

### Computation and limit

The audit instantiates three prior or independent equal-slope languages. For
`c=1`, the witness line meets one sample language only at `h=3`; every audited
height from `4` onward is outside all three. Exact integer checks verify
primitivity and `D>0`.

CO-229 is an infinite no-go theorem for a finite semilinear cover, not merely a
finite search result. However, an uncovered positive-denominator word need not
satisfy the exact cycle divisibility `D|B`, need not be realized by a natural
number orbit, and says nothing about descent of aperiodic orbits. The next lemma
must use order-sensitive intercept arithmetic to prove `D` does not divide `B`
for every remaining primitive positive-denominator word, or find an actual
divisibility counterexample.

## 3. Strong Goldbach conjecture

### Proposition GB-229

Let `l` be an odd prime, `G=(Z/lZ)^*`, `J` the all-ones operator, and

```text
M_a(u,v)=1_(uv != a mod l).
```

For nonzero `a`, write `M_a=J-P_a`, where `P_a` is the permutation
`v=a/u`. Then

```text
sum_(a mod l) M_a = (l-1)J.                               (GB-229.1)
```

Hence a complete target-residue period annihilates the zero-sum character
space exactly. For an average over `H` consecutive targets, its nonconstant
operator norm is at most `r/H<l/H`, where `r=H mod l`. In contrast, every
fixed nonzero target has nonconstant norm exactly one.

### Proof

For each unit pair `(u,v)`, exactly one nonzero residue `a=uv` is forbidden
among all `l` targets. Summing the masks therefore gives `(l-1)` in every
entry, proving `(GB-229.1)`. Since `J` vanishes on the zero-sum space, a
complete period contributes zero there.

Split a consecutive interval of length `H` into complete periods and a
remainder of length `r`. On the zero-sum space, `M_a=-P_a` for every nonzero
`a`, and `M_0=J=0`. Each nonzero remainder term has norm one, so the triangle
inequality gives `r/H<l/H`. But for one fixed nonzero `a`, `-P_a` is an
isometry, proving the exact pointwise norm-one obstruction.

### Computation and limit

Exact finite-group matrices verify the complete-period identity for the first
odd primes through `43`. Consecutive windows with `H` in
`{10,25,100,1000}` verify the exact remainder and the certified `r/H` bound.

The proof is exact for every odd prime `l`; the finite matrices are regression
checks. Strong Goldbach is pointwise in each even target, whereas GB-229 gains
cancellation only by averaging target residues. It supplies no prime-weighted
minor-arc or factor-cell estimate for a fixed target. That precise pointwise
character cancellation is the next lemma.

## 4. Twin Prime conjecture

### Proposition TP-229

For an odd prime `l>3`, define the simultaneous shift-two survival operator on
`G=(Z/lZ)^*` by

```text
S=J-P_2-P_(-2).
```

For every nonprincipal multiplicative character `chi`,

```text
S chi = -chi(2)(1+chi(-1)) chi^(-1).                      (TP-229.1)
```

Thus odd characters have singular value zero, even nonprincipal characters
have singular value two, and the constant singular value is `l-3`. For `l=5`,
the quadratic character is even and has normalized ratio
`2/(5-3)=1`. Tensoring additional normalized local factors cannot contract a
global character supported only on this modulo-5 component.

### Proof

The forbidden products `2` and `-2` are distinct for `l>3`, giving the stated
operator. For `P_a f(u)=f(a/u)`,

```text
P_a chi = chi(a) chi^(-1).
```

The all-ones operator kills every nonprincipal character. Since
`chi(-2)=chi(-1)chi(2)`, equation `(TP-229.1)` follows. Character parity makes
`1+chi(-1)` equal to zero or two. The constant row sum is `l-3`. At `l=5`,
the unique quadratic nonprincipal character is even, so its singular value
equals the constant singular value. A tensor character may be principal at
all other local primes, preserving normalized ratio one.

### Computation and limit

The exact character action is audited for odd primes through `43`; modulo `5`
is the unique tested local factor with worst normalized nonconstant ratio one.
Five squarefree tensor examples verify that adding other local factors does
not remove a mode supported only at `5`.

TP-229 identifies an exact parity projection and an exact obstruction. It does
not estimate prime-weighted shift-two sums, overcome the sieve parity problem,
or prove infinitely many gap-two primes. The next lemma is deliberately narrow:
obtain cancellation of the explicit modulo-5 quadratic mode across the actual
prime-weighted factor cells.

## Literature and priority boundary

- Connes and Consani, [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368), gives operator-theoretic Weil-positivity context. RH-229 is only an elementary two-frequency bound and tail-mismatch result.
- Lagarias, [The 3x+1 problem: an overview](https://arxiv.org/abs/2111.02635), and Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562), delimit the gap between word arithmetic, almost-all behavior, and every-orbit convergence.
- Helfgott, [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438), provides circle-method context but does not imply strong binary Goldbach.
- Ford and Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368), and the Polymath project, [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897), provide modern sieve context; bounded gaps do not prove infinitely many gaps of exactly two.

Nearest-integer logarithmic-form bounds, semilinear lattice arguments, and
finite-group character diagonalization are classical tools. PrimeProject does
not claim literature priority for those ingredients or for TICKET-229 without
an independent exhaustive literature review and peer review. The durable
contribution here is the explicit theorem/no-go ledger, proof dependencies,
machine-reproducible audit, and narrowed successor statements.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket229_band_frame_semilinear_character_barriers.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket229_band_frame_semilinear_character_barriers -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

Machine-readable artifacts:

- `data/open-problem/ticket229-band-frame-semilinear-character-barriers.json`
- `data/open-problem/riemann/rh-ticket-229-band-frame-bound.json`
- `data/open-problem/collatz/co-ticket-229-semilinear-coverage-no-go.json`
- `data/open-problem/goldbach/gb-ticket-229-target-period-cancellation.json`
- `data/open-problem/twin-prime/tp-ticket-229-character-parity-obstruction.json`
