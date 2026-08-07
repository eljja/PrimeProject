# TICKET-193: Everywhere Convergence, Nine-One Cycles, and Parity Envelopes

## 1. Claim boundary

TICKET-193 proves four intermediate theorems. It proves none of the Riemann
Hypothesis, the Collatz conjecture, strong Goldbach, or the Twin Prime
conjecture, and it finds no counterexample to any parent conjecture. The new
complete infinite family closed here consists of accelerated Collatz valuation
periods with exactly nine entries equal to one and every other entry equal to
two.

| Problem | Exact result proved here | Route discarded | Next single lemma |
|---|---|---|---|
| Riemann | `EverywherePointwiseQuadraticConvergenceForcesUniformBoundedExtension` | invoking Banach-Steinhaus from convergence on a merely dense core | `PoleNeutralWeilFiniteSectionsConvergeOnEveryVectorOfACompleteAdmissibleHilbertCompletion` |
| Collatz | `ExactlyNineValuationOnesOtherwiseTwoCycleExclusion` | pairwise enumeration of 52,157,326 words | `NoContractingValuationWordWithExactlyTenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| Goldbach | `ParitySeparatedPrimePowerContaminationEnvelope` | charging powers of two by the same `log N` union bound as odd powers | `BinaryCorrelationExceedsParitySeparatedPrimePowerEnvelopeForEveryLargeEvenTarget` |
| Twin Prime | `OddOnlyShiftTwoContaminationEnvelope` | including powers of two in shift-two contamination for `X>=4` | `ShiftTwoCorrelationExceedsOddLocalWeightedEnvelopeOnInfinitelyManyDyadicBlocks` |

Reproduce with:

```powershell
D:\python\anaconda3\python.exe scripts\ticket193_everywhere_nineone_parity_envelope.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket193_everywhere_nineone_parity_envelope -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

The integrated machine-readable result is
`data/open-problem/ticket193-everywhere-nineone-parity-envelope.json`. All four
attempts remain `open_not_proven`; the resolution count is `0 / 4`.

## 2. Riemann Hypothesis

### 2.1 Declared proposition

Let `q_n` be continuous Hermitian quadratic forms on a complex Hilbert space
`H`, with associated bounded Hermitian forms `B_n`. If `q_n(x)` converges for
every `x in H`, then

```text
sup_n ||B_n|| < infinity,
```

`B_n(x,y)` converges for every `x,y`, and its limit is a bounded Hermitian form
whose diagonal is `lim_n q_n(x)`. Positivity passes to the limit.

### 2.2 Proof

Complex polarization recovers `B_n(x,y)` from four diagonal values
`q_n(x+i^k y)`. Everywhere diagonal convergence therefore gives scalar
convergence, hence pointwise boundedness, of `B_n(x,y)` for every `x,y`.

For fixed `x`, the bounded functionals `y -> B_n(x,y)` form a pointwise bounded
family. The uniform boundedness principle gives
`sup_n ||B_n(x,.)||<infinity`. Writing `B_n(x,y)=<T_n x,y>` by Riesz
representation now gives `sup_n ||T_n x||<infinity` for every `x`. A second
uniform-boundedness application yields `sup_n ||T_n||<infinity`. The pointwise
limit is consequently a bounded Hermitian form, and nonnegativity is preserved
on the diagonal.

### 2.3 Exact dense-core no-go

On `H=l^2`, `D=c_00`, define

```text
q_n(x)=n|x_n|^2.
```

For every finite-support vector, `q_n(x)` is eventually zero, yet
`||B_n||=n`. The missing complete-space point is explicit:

```text
x_(2^j)=sqrt(j/2^j),  x_n=0 otherwise.
```

Since `sum_j j/2^j=2`, this vector lies in `l^2`, while
`q_(2^j)(x)=j` diverges. Thus a dense-core convergence claim cannot invoke the
theorem.

### 2.4 Remaining gap

PrimeProject has not proved that the actual pole-neutral Weil finite sections
converge on every vector of one complete admissible Hilbert completion. Recent
screw-function work still treats the decisive limiting operator as
conjectural: [Suzuki 2026](https://arxiv.org/abs/2606.09096).

## 3. Collatz conjecture

### 3.1 Declared proposition

No positive accelerated Collatz cycle has exactly nine valuations equal to one
and every other valuation equal to two, whether the displayed period is
primitive or imprimitive.

### 3.2 Contracting range and boundary decomposition

For period length `h`, the valuation sum is `2h-9` and the affine denominator
is

```text
D_h=2^(2h-9)-3^h.
```

It is nonpositive through `h=21` and positive from `h=22`. Rotate a word so one
of its nine ones is first. Divisibility is rotation invariant because `D_h` is
odd and

```text
2^v B_shift=3B+D_h.
```

For normalized positions `0=p_0<p_1<...<p_8<h`, define

```text
P_r(t)=sum_(0<=j<t, 2j>=r) 3^(h-1-j)2^(2j-r),
C_h=3^(h-1)+P_9(h)-P_1(1),
d_i(p)=P_i(p+1)-P_(i+1)(p+1).
```

The recurrence numerator is exactly

```text
B_h(p_1,...,p_8)=C_h+sum_(i=1)^8 d_i(p_i).
```

The implementation exhaustively compares this formula with the original
recurrence for every normalized word at `h=9,...,15`.

### 3.3 Complete 4+4 meet-in-the-middle audit

Store the left residues

```text
C_h+d_1(p_1)+...+d_4(p_4) mod D_h.
```

When the first right position is `p_5=c`, activate exactly those left tuples
with `p_4<c` and query the residue opposite to
`d_5(p_5)+...+d_8(p_8)`. Exact Python integers and exact hash-set membership
are used; there is no floating-point tolerance.

Each right tuple represents `C(c-1,4)` compatible left tuples. The full
coverage identity is

```text
sum_(h=22)^34 C(h-1,8)
  = C(34,9)-C(21,9)
  = 52,157,326.
```

No divisibility hit occurs. A SHA-256 transcript records every right-side
query per horizon. This is a complete finite decision for the stated range,
not random sampling.

### 3.4 Infinite tail

A nontrivial positive odd cycle contains no `1`, hence every state is at least
three. Multiplying the cycle ratios gives

```text
1 <= 512(5/6)^h.
```

The right side remains above one at `h=34`, is strictly below one at `h=35`,
and decreases thereafter. Thus every `h>=35` is impossible, completing the
nine-one/rest-two stratum.

### 3.5 Remaining gap

Valuation words with ten or more ones, valuations at least three, and
aperiodic divergence remain untreated. Recent accelerated-map work does not
claim a global Collatz proof: [Niu 2026](https://arxiv.org/abs/2605.13886).

## 4. Strong Goldbach conjecture

### 4.1 Declared proposition

Let `W_odd(N)` be the sum of `log p` over odd proper prime powers
`p^k<=N`, `k>=2`. Let `C_2(N)` be the exact von Mangoldt mass from ordered
solutions

```text
2^a+2^b=N,  a,b>=1, max(a,b)>=2.
```

For every even `N>=6`, proper-prime-power contamination satisfies

```text
E_pp(N) <= 2 log(N) W_odd(N)+C_2(N),
C_2(N) <= 2(log 2)^2.
```

### 4.2 Parity separation

Two summands of an even target have equal parity. An even integer in von
Mangoldt support is a power of two, so all even-even contamination is exactly
`C_2(N)`. Uniqueness of binary representation permits at most two ordered
exponent pairs.

Every remaining contaminated pair contains an odd proper prime power. Charge
the pair to that coordinate; the partner has weight at most `log N`, and two
coordinate positions give the displayed bound. This is never larger than the
TICKET-192 envelope that overcharged every power of two by `log N`.

### 4.3 Prime-base compression

Put `y=floor(sqrt N)`. For an odd prime `p<=y`, let
`K=floor(log_p N)`. All proper powers from that base contribute

```text
(K-1)log p <= log N-log p.
```

Consequently

```text
W_odd(N)
 <= (pi(y)-1)log N-(theta(y)-log 2)
 <= sqrt(N)log N.
```

The parity-separated envelope is therefore explicitly
`O(sqrt(N)log^2 N)`. All eleven finite targets from `2^10` through `2^20`
exceed the new envelope. This finite replay is not an all-even theorem.

### 4.4 Remaining gap

One must prove the binary von Mangoldt correlation exceeds
`2log(N)W_odd(N)+C_2(N)` for every sufficiently large even `N`.
Exceptional-set results do not provide that quantifier:
[Grimmelt--Teravainen 2025](https://arxiv.org/abs/2508.16400).

## 5. Twin Prime conjecture

### 5.1 Declared proposition

For `X>=4`, any von Mangoldt-supported pair `n,n+2` with `X<=n<2X` is odd.
Hence shift-two proper-prime-power contamination is at most

```text
log(2X+2)[
  W_odd([X,2X))+W_odd([X+2,2X+2))
].
```

Correlation above this odd-only local envelope forces a twin prime in the
block.

### 5.2 Excluding even support

An even supported pair would have `n=2^a`, `n+2=2^b`, giving

```text
2^a(2^(b-a)-1)=2.
```

Thus `a=1` and the only pair is `{2,4}`, which cannot occur when `X>=4`.
Every supported block pair is odd-odd, so contamination can be charged only to
odd proper prime powers.

All sixteen finite dyadic blocks `j=4,...,19` exceed the odd-only envelope.
Finite success does not imply infinitely many successful blocks.

### 5.3 Remaining gap

The shift-two correlation must exceed the odd-only envelope on infinitely many
unbounded blocks. Bounded prime-gap theorems do not force exact gap two:
[Zhang 2014](https://annals.math.princeton.edu/2014/179-3/p07) and
[Maynard 2015](https://annals.math.princeton.edu/2015/181-1/p07).

## 6. Synthesis

The common move in TICKET-193 is to identify the exact global structure rather
than retain a coarse surrogate. Completeness, not dense-core convergence,
activates uniform boundedness in the RH track. Parity, not the full prime-power
set, controls additive and shift-two contamination. In the Collatz track, an
eight-boundary decomposition removes pairwise enumeration while preserving the
full combinatorial coverage of 52,157,326 words. None of these advances removes
the remaining infinite quantifier in a parent conjecture.
