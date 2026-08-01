# TICKET-180: Finite-Information Localization Audit

## Status and claim boundary

TICKET-180 does **not** prove or disprove the Riemann Hypothesis, the Collatz
conjecture, the strong Goldbach conjecture, or the Twin Prime conjecture. It
proves four exact intermediate no-go theorems about the information retained by
the current proof representations.

| Problem | Exact result | Status |
|---|---|---|
| Riemann | `FiniteToeplitzMomentIndeterminacyAndTailEnvelopeNecessity` | proved exact; RH open |
| Collatz | `ValuationLayerPermutationNoGoAndOrderedAffinePrefixIdentity` | proved exact; Collatz open |
| Goldbach | `MeanSquareExceptionalSpikeNoGoForEveryTargetPositivity` | proved exact; Goldbach open |
| Twin Prime | `GlobalCenteredEnergyNoGoForUniformBlockCancellation` | proved exact; Twin Prime open |

These are project results with explicit proofs and executable witnesses. No
claim of literature priority is made without an external novelty review.

## Why this ticket follows TICKET-179

TICKET-179 replaced four lossy representations with more faithful ones:

1. absolute RH coefficient bounds with a signed bounded symbol;
2. fixed Collatz bit depth with adaptive valuation layers;
3. continuous Goldbach positivity with discrete target positivity; and
4. pairwise Twin coherence with collective centered energy.

TICKET-180 asks the next question: do the improved summaries localize the
information at the quantifier required by the conjecture? The answer is no in
four precise senses:

- finite moments do not control an infinite tail;
- a multiset does not determine an ordered orbit;
- almost-all control does not imply every-target positivity; and
- a global average does not imply every-block cancellation.

## 1. Riemann Hypothesis

### Declared proposition

Let `T_N(f)` be the `N x N` Toeplitz section formed from the Fourier
coefficients of a real bounded symbol `f`. For every integer `M >= N` and every
`A > 0`, define

```text
g(theta) = f(theta) + A cos(M theta).
```

Then

```text
T_N(g) = T_N(f),
||g-f||_infinity = A,
||g||_infinity >= A - ||f||_infinity.
```

Consequently, finitely many Toeplitz moments cannot certify a global
`L-infinity` bound without an independent high-frequency envelope.

### Proof

An entry of `T_N(f)` has frequency `i-j`, where `|i-j| <= N-1`. The added
cosine has Fourier support only at `+M` and `-M`. If `M >= N`, neither mode
appears in the finite section, hence the two matrices are identical. The norm
bound follows from the reverse triangle inequality. This is an exact
indeterminacy theorem, not a numerical extrapolation.

### Reproducible witness

The generator uses `f(theta)=0.2 sign(cos theta)`, core margin `delta=0.25`,
hidden amplitude `A=1`, and hidden frequency `M=2N+1`.

| N | observed band | hidden M | matrix difference | value at theta=0 |
|---:|---:|---:|---:|---:|
| 8 | 7 | 17 | 0 | 1.2 |
| 16 | 15 | 33 | 0 | 1.2 |
| 32 | 31 | 65 | 0 | 1.2 |
| 64 | 63 | 129 | 0 | 1.2 |
| 128 | 127 | 257 | 0 | 1.2 |

### Route decision

- **Discard:** finite Toeplitz-section agreement as a certificate for the
  global bound of the actual Weil symbol.
- **Retain:** finite sections combined with an independently proved arithmetic
  high-frequency envelope.
- **Remaining gap:** no such envelope is known for the actual pole-neutral
  whitened Weil tail.
- **Next lemma:**
  `ArithmeticWeilTailHasCertifiedUniformHighFrequencyEnvelopeBeyondObservedBand`.

Recent finite Guinand-Weil work provides exact finite dictionaries and explicit
tail budgets while explicitly making no RH claim. The present no-go explains
why a separate unobserved-band estimate is logically necessary
([Groskin 2026](https://arxiv.org/abs/2607.02828)).

## 2. Collatz conjecture

### Declared proposition

For a valuation word `v=(v_0,...,v_(h-1))`, put

```text
S = sum_j v_j,
B(v) = sum_j 3^(h-1-j) 2^(v_0+...+v_(j-1)).
```

The accelerated odd Collatz branch has the exact composition

```text
T_v(n) = (3^h n + B(v)) / 2^S.
```

Adaptive layer counts determine the valuation multiset and `S`, but they do not
determine `B(v)` or the first-descent time.

### Proof

The affine formula follows by induction through
`n -> (3n+1)/2^v`. Layer counts are invariant under permutation, whereas
`B(v)` contains ordered prefix sums. Every positive valuation word determines a
natural odd cylinder modulo `2^(S+1)`, so the distinction is visible on actual
integer prefixes rather than only on formal words.

The sharpest computed pair is

```text
word (2,1,1): layers (3,1), B=29, start 9,  states 9,7,11,17, descent time 1
word (1,2,1): layers (3,1), B=23, start 27, states 27,41,31,47, no descent by step 3
```

The generator verifies analogous order-sensitive pairs for high valuations
`2` through `8`.

### Route decision

- **Discard:** unordered adaptive layers as a complete first-descent or cycle
  certificate.
- **Retain:** ordered prefix sums and the exact affine numerator on natural
  cylinders.
- **Remaining gap:** no uniform transfer theorem forces every natural orbit to
  enter a descending ordered cylinder; nontrivial cycles are not excluded.
- **Next lemma:**
  `OrderedCylinderTransferHasUniformDescentOutsideExplicitFiniteExceptionalSet`.

Recent one-bit work also leaves the decisive residual statement at orbit level;
it does not prove the required orbit mixing
([Chang 2026](https://arxiv.org/abs/2603.25753)).

## 3. Strong Goldbach conjecture

### Declared proposition

Mean-square control or a vanishing exceptional density cannot prove positivity
at every even target. On `L` targets with major value `mu>0`, set the minor
error to `-(1+epsilon)mu` at one target and zero elsewhere. Then

```text
normalized RMS = (1+epsilon)mu / sqrt(L) -> 0,
exception density = 1/L -> 0,
minimum major-plus-minor value = -epsilon mu < 0.
```

### Proof

The squared error has one nonzero term, giving the displayed RMS exactly. The
same single term defeats positivity. Therefore an exceptional-set theorem or an
`L2` minor-arc estimate needs a separate pointwise exception-removal argument
before it can imply strong Goldbach.

The executable family uses `mu=1`, `epsilon=0.1`, and
`L=16,64,256,1024,4096`. The normalized RMS decreases from `0.275` to about
`0.0172`, while the exceptional target remains negative. An independent exact
prime sieve finds no Goldbach counterexample through `10,000`; this is explicitly
finite evidence only.

### Route decision

- **Discard:** mean-square minor control or exceptional density zero as
  sufficient for every-target positivity.
- **Retain:** target-wise `L-infinity` deficit plus an explicit
  exception-removal mechanism.
- **Remaining gap:** no arithmetic pointwise estimate beats the major term on
  every target in every sufficiently large block.
- **Next lemma:**
  `ParityAliasedMinorHasUniformLInfinityDeficitBelowMajorMainOnEveryDyadicBlock`.

The distinction matches the current exceptional-set literature, which permits
exceptions and therefore does not establish the strong every-target statement
([Grimmelt and Bhowmik 2026](https://arxiv.org/abs/2607.27282)).

## 4. Twin Prime conjecture

### Declared proposition

Global centered-energy saturation does not imply uniform blockwise zero-mode
cancellation. For `m` components, take `K` blocks whose scalar components are
the `m`-th roots of unity and one block whose components are all aligned. Then

```text
sum_b Z_b / sum_b D_b = m/(K+1) -> 0,
Z_bad / D_bad = m,
V_bad / D_bad = 0.
```

### Proof

Each cancelling block has `D=m`, `Z=0`, and `V=m`. The aligned block has
`D=m`, `Z=m^2`, and `V=0`. Summation gives the formulas. Thus an arbitrarily
strong global average can hide one completely non-cancelling scale.

The generator fixes `m=8` and checks `K=8,32,128,512,2048`. The global
zero-mode ratio falls below `0.004`, while the bad-block ratio remains `8`.

### Route decision

- **Discard:** global or averaged centered-energy saturation as sufficient for
  uniform scale cancellation.
- **Retain:** centered-energy saturation uniformly on every sufficiently large
  dyadic prime-pair block.
- **Remaining gap:** no such arithmetic blockwise theorem or positive sieve
  lower bound is proved.
- **Next lemma:**
  `PrimePairHaarCenteredEnergySaturatesDiagonalUniformlyOnEveryLargeDyadicBlock`.

Prime-producing sieve theory likewise requires substantial Type II information
for lower bounds and does not derive twin-prime positivity from a generic
averaged surrogate
([Ford and Maynard 2024](https://arxiv.org/abs/2407.14368)).

## Cross-problem conclusion

TICKET-180 identifies four quantifier failures:

```text
finite       != infinite tail
multiset     != ordered path
almost all   != every target
global mean  != every block
```

The next research stage must build uniform localization estimates rather than
increase finite sample sizes. Larger computation can test a candidate envelope,
ordered transfer rule, exception-removal estimate, or blockwise saturation law;
it cannot replace the missing universal theorem.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket180_finite_information_localization.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket180_finite_information_localization -v
```

Machine-readable outputs:

- `data/open-problem/ticket180-finite-information-localization.json`
- `data/open-problem/riemann/rh-ticket-180-hidden-frequency.json`
- `data/open-problem/collatz/co-ticket-180-ordered-prefix.json`
- `data/open-problem/goldbach/gb-ticket-180-exceptional-spike.json`
- `data/open-problem/twin-prime/tp-ticket-180-block-localization.json`

Every problem remains `open_not_proven`, and the conjecture-resolution count is
zero.
