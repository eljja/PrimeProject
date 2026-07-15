# TICKET-120: Low-divisor pair saving identity and weak-contract no-go

## Claim boundary / 주장 경계

TICKET-120 does **not** prove the Twin Prime Conjecture, a Vaughan arithmetic angle gap, or eventual endpoint closure. It proves an elementary two-block saving identity, reconstructs that identity on eight finite PrimeProject scales, and gives an exact counterexample to a proposed fixed-fraction strengthening under weak Gram hypotheses.

TICKET-120은 **쌍둥이 소수 추측, Vaughan 산술 angle gap, 충분히 큰 범위의 endpoint 폐쇄를 증명하지 않습니다.** 두 블록 pairing의 보편적 삼각부등식 항등식을 확인하고, 약한 Gram 가정만으로 고정 비율 절감이 생긴다는 잘못된 보조정리를 정확한 반례로 제거합니다.

## Why this ticket / 이 티켓이 필요한 이유

TICKET-119 found that the first canonical factor-four group contributes 59.14% of the 16M canonical numerator budget. Repeating a larger finite holdout would not explain why adjacent pairing helps. TICKET-120 therefore separates the saving into:

```text
scalar saving   = |m0| + |m1| - |m0 + m1|,
centered saving = w (||z0|| + ||z1|| - ||z0 + z1||).
```

Here `m0,m1` are denominator-block mean contributions, `z0,z1` are centered endpoint coefficient vectors, and `w` is the projected phase norm. Both terms are nonnegative by the scalar and Hilbert-space triangle inequalities. Summing over denominators gives the exact low-pair budget saving.

## Exact bounded theorem / 정확한 제한 정리

For every pair of scalar means and Hilbert vectors,

```text
paired budget <= singleton budget.
```

This statement is universal and does not use prime arithmetic. The machine audit checks 8 scales and 248 denominator rows:

| contract | result |
|---|---:|
| scale rows | 8 |
| denominator rows | 248 |
| maximum Gram Cauchy excess | 0 |
| minimum denominator saving | 0 |
| maximum registered-group reconstruction error | `9.31e-10` |
| contract failures | 0 |

This is an elementary lemma, not a new analytic-number-theory theorem. Its value is that it makes the source and limitation of the observed saving explicit.

## What actually saves the 16M budget / 16M 절감의 실제 원인

| horizon | low pair | paired / singleton | saving | scalar share of saving | paired / known | median centered cosine |
|---:|---|---:|---:|---:|---:|---:|
| 4,194,304 | `D128-D256` | 0.758787 | 24.1213% | 1.5315% | 0.494018 | -0.102944 |
| 8,388,608 | `D128-D256` | 0.729095 | 27.0905% | 1.7225% | 0.428842 | -0.358774 |
| 16,777,216 | `D256-D512` | 0.802774 | 19.7226% | 0.0069% | 0.451954 | -0.402811 |

At 16M only 1 of 31 denominator means has opposite signs, while 15 of 27 active centered blocks have negative cosine. Almost none of the saving comes from scalar mean cancellation. The useful finite geometry is centered-vector interaction.

16M에서는 mean 부호가 반대인 분모가 31개 중 1개뿐이며, 절감 중 scalar mean이 설명하는 비율도 `0.0069%`에 불과합니다. 따라서 “첫 두 Möbius shell의 평균 부호가 반대라서 절감된다”는 설명은 폐기합니다. 관측된 절감은 거의 전부 centered vector의 angle에서 발생합니다.

Negative median cosine is only a finite diagnostic. It does not provide a denominator-weighted all-scale bound, and the observed percentage cannot be inserted as a theorem constant.

## Exact counterexample to the weak strengthening / 약한 강화 명제의 정확한 반례

Consider the positive-semidefinite rank-one Gram model

```text
m0 = m1 = 1,
z0 = z1 = unit vector,
Gram = [[1,1],[1,1]].
```

Then singleton and paired budgets are both `4`; the saving is exactly zero. Therefore the following candidate is false:

```text
UniversalFixedFractionLowDivisorPairSavingUnderGramContract:
there exists eta>0 such that paired <= (1-eta) singleton
for every scalar pair and positive-semidefinite two-vector Gram system.
```

The same weak contract also permits complete cancellation with `m1=-m0` and `z1=-z0`. Thus Gram positivity alone allows every behavior from zero to full saving and cannot determine an arithmetic saving rate.

이 반례는 쌍둥이 소수 추측의 반례가 아니라, 제안된 약한 보조정리의 반례입니다. 이제 일반 Hilbert geometry에서 더 강한 절감률을 찾는 경로는 폐기해야 합니다.

## Retained arithmetic theorem / 유지할 산술 정리

```text
VaughanLowDivisorDenominatorSummedAngleGap
```

The required theorem must use the actual signed Möbius/divisor convolution and denominator phases. In schematic form it must produce fixed `eta>0` and `X0` such that every `X>=X0` has a denominator-summed mean-sign and centered-angle gap for the first canonical pair. It must then combine with tail, boundary, variation, comparison positivity, and prime-power contamination estimates.

필요한 것은 임의의 Gram matrix 정리가 아니라 실제 Vaughan 계수에 대한 산술 정리입니다. 첫 factor-four group을 signed Möbius/divisor bilinear sum으로 전개하고, 분모 전체를 합친 angle gap을 규모와 무관한 상수로 증명해야 합니다.

Counterexample route:

```text
construct an unbounded Vaughan-realizable sequence whose low-pair
paired/singleton ratio approaches one, or whose paired/known term
defeats every fixed full-budget margin.
```

One finite aligned Gram model refutes the weak lemma. Refuting the retained arithmetic theorem requires an admissible unbounded sequence, not an abstract PSD matrix.

## Literature boundary / 문헌상 경계

- [Lichtman, *Averages of the Möbius function on shifted primes*](https://arxiv.org/abs/2009.08969) proves cancellation averaged over sufficiently many shifts. It does not supply the fixed shift-two denominator-summed angle gap required here.
- [Ford and Maynard, *On the theory of prime producing sieves*](https://arxiv.org/abs/2407.14368) studies what Type I/II information can force and constructs complementary extremal sequences. It supports using explicit countermodels to test whether a proposed information contract is strong enough, but does not imply the PrimeProject inequality.
- [Helfgott, *The ternary Goldbach problem*](https://arxiv.org/abs/1501.05438) provides a rigorous model for explicit Type I/II minor-arc analysis in a different additive problem.

## Keep, discard, and next step / 유지·폐기·다음 단계

Keep:

- the exact scalar-plus-centered saving decomposition;
- centered covariance before norms;
- the aligned rank-one model as a mandatory falsification oracle;
- the finite scale ledger only as diagnostic evidence.

Discard:

- mean-sign cancellation as the main 16M explanation;
- any positive fixed saving fraction derived only from PSD Gram geometry;
- extrapolating the observed cosines or saving percentages;
- transferring this Twin-specific result to RH, Collatz, or Goldbach.

Next:

1. expand the first pair into its signed Möbius/divisor sums;
2. identify a denominator-averaged arithmetic covariance whose sign follows from those coefficients;
3. attack `VaughanLowDivisorDenominatorSummedAngleGap` with a matching admissible counterexample generator;
4. keep the full target `EventuallySubcriticalCanonicalAdjacentDyadicPairVaughanEndpointBudget` open.

## Reproduction

```powershell
python scripts/ticket120_twin_low_divisor_pair_savings_audit.py
python -m unittest tests.test_ticket120_twin_low_divisor_pair_savings_audit
```

Result: `data/open-problem/ticket120-twin-low-divisor-pair-savings-audit.json`.
