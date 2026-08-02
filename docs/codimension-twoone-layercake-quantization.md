# TICKET-186: Codimension, Two-One Cycles, Survivor Layers, and Quantized Margins

## 1. Status and claim boundary

TICKET-186 continues the four terminal nodes of TICKET-185. It proves one new
infinite Collatz cycle exclusion and three exact target corrections. It proves
none of the Riemann, Collatz, strong Goldbach, or Twin Prime conjectures.

| problem | exact result in this ticket | discarded route | next single lemma |
|---|---|---|---|
| Riemann | `FiniteCodimensionCoercivityIsNotNecessaryForNonnegativity` | treating a uniform coercive gap after finitely many removed modes as necessary | `WeilQuadraticFormNonnegativityOnExplicitPoleNeutralCoreWithVanishingCertifiedDefect` |
| Collatz | `ExactlyTwoValuationOnesOtherwiseTwoCycleExclusion` | replacing an all-horizon proof by bounded enumeration | `NoContractingValuationWordWithExactlyThreeOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| Goldbach | `BadSurvivorLayerCakeAndNonnegativeSubhorizonNoGo` | cancelling composite contamination with nonnegative survivor occupancies | `SignedPrimeWeightedBadSurvivorCorrelationHasUniformSubHorizonPowerSaving` |
| Twin Prime | `QuantizedTwinProjectorAndFixedRelativeMarginNoGo` | requiring a fixed positive normalized projector margin | `PredeclaredCubicRoughSignedTypeIIMainDominatesRemainderOnInfinitelyManyDyadicBlocks` |

Reproduce the machine artifacts with:

```powershell
D:\python\anaconda3\python.exe scripts\ticket186_codimension_twoone_layercake_quantization.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket186_codimension_twoone_layercake_quantization -v
```

The principal output is
`data/open-problem/ticket186-codimension-twoone-layercake-quantization.json`.
Every conjecture status in that file is `open_not_proven`.

## 2. Riemann Hypothesis

### 2.1 Declared proposition

Let (H) have orthonormal basis ((e_n)), and define the positive injective
compact operator

\[
Ae_n=\frac1n e_n.
\]

For every finite-dimensional subspace (T\subset H),

\[
\inf_{\substack{x\perp T\\\|x\|=1}}\langle Ax,x\rangle=0. \tag{1}
\]

Thus nonnegativity and injectivity do not imply coercivity after quotienting
any finite list of nuisance or translation modes.

### 2.2 Proof

Let (P_T) be the orthogonal projection onto (T). Since (P_T) has finite
rank, `||P_T e_n|| -> 0`. Normalize

\[
x_n=\frac{(I-P_T)e_n}{\|(I-P_T)e_n\|}.
\]

Then (x_n\perp T), (x_n-e_n\to0), and boundedness of (A) gives

\[
\langle Ax_n,x_n\rangle-\langle Ae_n,e_n\rangle\to0.
\]

The second term is (1/n\to0). Positivity gives the reverse lower bound zero,
proving (1).

Coordinate quotients at dimensions `8,16,32,64,128,256` have exact smallest
values `1/N`; all finite sections are strictly positive while their gap tends
to zero.

### 2.3 Meaning and limit

TICKET-185 asked for Weil-form coercivity modulo spectral translations. The
operator theorem proves that such coercivity is not a logically necessary
consequence of positivity when only finitely many modes are removed. The
correct minimal target is nonnegativity on an explicit dense pole-neutral form
core, with any certified negative defect tending to zero.

This operator is not the zeta Weil operator. The result neither proves the
actual Weil form nonnegative nor excludes a zero off the critical line. Recent
work on the screw-function realization of the Weil quadratic form likewise
states no RH proof ([Suzuki, 2026](https://arxiv.org/abs/2606.09096)); numerical
operator realizations remain finite spectral evidence
([Kim et al., 2026](https://arxiv.org/abs/2607.24830)).

## 3. Collatz conjecture

### 3.1 Declared proposition

For the accelerated odd Collatz map, no positive cycle has a valuation period
containing exactly two `1` entries and all other entries equal to `2`.
After cyclic rotation every such word is

\[
w_{a,b}=(1,2^{a-1},1,2^{b-1}),\qquad a,b\ge1,\quad h=a+b.
\]

The statement includes primitive and imprimitive words.

### 3.2 Exact affine calculation

The affine numerator and cycle denominator are

\[
B_{a,b}=4^{h-1}-3^{h-1}+4^a3^{b-1},\qquad
D_h=4^{h-1}-3^h. \tag{2}
\]

The family is contracting exactly from (h=5). Equation (2) gives

\[
B_{a,b}-D_h=2\cdot3^{h-1}+4^a3^{b-1}>0. \tag{3}
\]

For fixed (h), the final term in (B_{a,b}) increases with (a), so

\[
B_{a,b}\le 2\cdot4^{h-1}-3^{h-1}.
\]

For (h\ge9), ((4/3)^{h-1}>8), which is exactly the inequality needed for

\[
1<\frac{B_{a,b}}{D_h}<3. \tag{4}
\]

Both integers in (2) are odd. If (D_h\mid B_{a,b}), the quotient in (4)
would be an odd integer strictly between one and three. The only integer there
is two, which is even, a contradiction. The remaining contracting horizons
`h=5,6,7,8` contain `22` possible cyclic separations; exact enumeration finds
zero divisibility hits. This finite check closes only the finite exception to
the analytic (h\ge9) proof.

### 3.3 Meaning and limit

This completes the exact next lemma from TICKET-185 and is a genuine infinite
cycle-stratum theorem. It does not address words with three or more `1`
entries, valuations at least `3`, or divergent nonperiodic natural-number
orbits. Almost-all orbit results do not supply those missing universal
quantifiers ([Tao, 2022](https://arxiv.org/abs/1909.03562)).

## 4. Strong Goldbach conjecture

### 4.1 Declared proposition

Fix an even (N\). For every bad odd pair ((a,N-a)), let

\[
\gamma_N(a)=\min(P^-(a),P^-(N-a)),
\]

where (P^-) is the least prime factor, and put

\[
\tau_N=\max_{\text{bad }a}\gamma_N(a),\qquad \max\varnothing:=0,
B_N(y)=\#\{\text{bad }a:\gamma_N(a)>y\}.
\]

Then

\[
B_N(y)\ge1\quad(0\le y<\tau_N), \tag{5}
\]

and the exact discrete layer-cake identity is

\[
\sum_{y=0}^{\tau_N-1}B_N(y)
=\sum_{\text{bad }a}\gamma_N(a). \tag{6}
\]

### 4.2 Proof and no-go consequence

A pair with gate `gamma` survives exactly the integer depths
`0,...,gamma-1`; exchanging the two finite sums proves (6). If `tau_N>0`, a
pair attaining the maximum gate survives every subhorizon depth, proving (5).
When there is no bad pair, `tau_N=0` and both (5) and (6) are vacuous.

For `tau_N>0` and nonnegative weights `w_y`, not all zero below `tau_N`,
equations (5)-(6) imply

\[
\sum_{y<\tau_N}w_yB_N(y)>0. \tag{7}
\]

Therefore nonnegative wheel occupancy cannot cancel every composite
impostor before the exact factor horizon. Signed prime-sensitive information
is necessary.

| `N` | `tau_N` | bad pairs | layer area | last bad layer | prime representations |
|---:|---:|---:|---:|---:|---:|
| 100 | 7 | 18 | 62 | 1 | 6 |
| 500 | 19 | 111 | 495 | 1 | 13 |
| 1,000 | 29 | 221 | 1,015 | 1 | 28 |
| 5,000 | 67 | 1,173 | 7,073 | 1 | 76 |
| 10,000 | 89 | 2,372 | 15,472 | 1 | 127 |
| 50,000 | 223 | 12,049 | 103,001 | 1 | 450 |

These finite representations are replay checks, not a Goldbach proof. The
missing result is a uniform signed von Mangoldt or parity-sensitive estimate.
The current exceptional-set literature still separates explicit major arcs
from an every-target conclusion
([Grimmelt and Bhowmik, 2026](https://arxiv.org/abs/2607.27282)).

## 5. Twin Prime conjecture

### 5.1 Declared proposition

On the cubic-rough support of TICKET-142, Walsh inversion gives

\[
\Delta=A_{00}-A_{10}-A_{01}+A_{11}=4C, \tag{8}
\]

where (C) is the integer twin count in the block. Hence

\[
\Delta>0\quad\Longleftrightarrow\quad\Delta\ge4. \tag{9}
\]

For any fixed predeclared partition into finite disjoint blocks that covers
all sufficiently large candidate starts, positivity in infinitely many blocks
is equivalent to Twin Prime infinitude. However, no fixed relative bound
`Delta >= delta A00` is logically necessary.

### 5.2 Proof of the fixed-margin no-go

For arbitrary `A00 >= 2`, the valid abstract parity table

\[
N_{--}=1,\quad N_{++}=A_{00}-1,\quad N_{+-}=N_{-+}=0
\]

has

\[
(A_{10},A_{01},A_{11})=(A_{00}-2,A_{00}-2,A_{00}),
\]

so `Delta=4` and `Delta/A00=4/A00 -> 0`. It retains one
positive twin class per block while defeating every fixed normalized margin.

Actual finite cubic-rough ledgers still reconstruct the direct twin counts:

| `X` | `A00` | `Delta` | direct count | `Delta/A00` |
|---:|---:|---:|---:|---:|
| 1,000 | 59 | 104 | 26 | 1.762712 |
| 10,000 | 358 | 548 | 137 | 1.530726 |
| 100,000 | 2,486 | 3,744 | 936 | 1.506034 |
| 1,000,000 | 17,634 | 26,808 | 6,702 | 1.520245 |

The counterledgers are not alternative Liouville values on the integers, and
the finite rows prove no eventual sign theorem. They only show that the next
analytic contract should clear the exact four-unit threshold without demanding
a fixed positive fraction. Substantial Type I/II information remains the
known general requirement for prime-producing lower-bound sieves
([Ford and Maynard, 2024](https://arxiv.org/abs/2407.14368)).

## 6. Proof DAG and final boundary

```text
RH T185 coercivity target
  -> finite-codimension coercivity no-go [proved]
  -> actual Weil nonnegativity with vanishing defect [open]

Collatz T185 exactly-two-one target
  -> all exactly-two-one/rest-two cycles excluded [proved]
  -> exactly-three-one/rest-two divisibility exclusion [open]

Goldbach T185 subhorizon target
  -> survivor layer-cake + nonnegative no-go [proved]
  -> signed prime-weighted subhorizon power saving [open]

Twin T185 one-sided margin target
  -> four-unit quantization + fixed-relative-margin no-go [proved]
  -> predeclared signed Type I/II domination infinitely often [open]
```

No complete proof or counterexample has been obtained. The exact new progress
is the full two-one Collatz cycle-stratum exclusion. The other three results
remove overstrong or sign-blind proof contracts and leave explicit arithmetic
lemmas rather than promoting finite evidence.
