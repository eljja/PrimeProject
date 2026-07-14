# TICKET-114: Twin Ramanujan numerator-dispersion audit

## Claim boundary

TICKET-114 does **not** prove the Twin Prime Conjecture and does not certify a last-twin counterexample. It proves an exact algebraic decomposition and a sharp finite-dimensional support theorem under a stated weak coefficient contract. The scale rows use measured floating-point coefficient norms; they are not a uniform estimate in `X`.

## From denominator blocks to numerator dispersion

TICKET-113 grouped 162 Farey-cell endpoints into 31 right-denominator blocks. That grouping retained observed complex cancellation but did not explain why it should persist. TICKET-114 opens every block by its reduced numerator.

Let `P_{q,a}` be the unphased Abel endpoint coefficient of the minor cell immediately left of the reduced rational `a/q`. Move its endpoint phase to the exact rational phase

```text
rho_{q,a} = exp(4 pi i a/q).
```

The transfer error is retained exactly and bounded analytically by

```text
|P_{q,a}| |exp(4 pi i alpha)-rho_{q,a}|
  <= 4 pi |P_{q,a}| |alpha-a/q|.
```

Write `Re(P_{q,a})=m_q+x_{q,a}` with `sum_a x_{q,a}=0`. The rational-boundary real contribution becomes

```text
m_q sum_a cos(4 pi a/q)
  + sum_a [x_{q,a} cos(4 pi a/q) - Im(P_{q,a}) sin(4 pi a/q)].
```

For `q>2`, the half reduced-residue cosine sum is exactly `c_q(2)/2`, where `c_q` is the Ramanujan sum; for `q=2` it is `c_2(2)`. Across the audit, the floating evaluation of these half-cosine identities differs from the exact integer Ramanujan formula by at most `1.2e-15`; the complete per-block rational-boundary decomposition differs by at most `1.5e-11`.

## Sharp weak-contract bound

Define the centered coefficient vector

```text
d_q = (x_{q,a}, Im(P_{q,a}))_a
```

and the projected phase vector

```text
w_q = (cos(4 pi a/q)-mean_a cos(4 pi a/q), -sin(4 pi a/q))_a.
```

Because `sum_a x_{q,a}=0`, the centered contribution is the Euclidean inner product `<d_q,w_q>`. Therefore

```text
|<d_q,w_q>| <= ||d_q||_2 ||w_q||_2.
```

This bound is optimal under only the zero-real-mean and L2-norm constraints: choose `d_q` opposite to `w_q`. This gives an explicit abstract adversary attaining the negative support value. It is not claimed to satisfy the Möbius/divisor convolution identities of actual Vaughan coefficients.

Consequently, any stronger estimate must use additional arithmetic phase information or prove a smaller uniform centered norm from the Vaughan bilinear structure. Repartitioning the same vector or applying another generic Cauchy inequality cannot improve this contract.

## Finite results

| X | Ramanujan mean | mean abs. envelope | centered L2 envelope | boundary transfer | Abel variation | known term | signed-mean lower | sign-free lower | sign-free budget / known |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4,096 | -67.3 | 340.3 | 1,989.8 | 22.28 | 71.2 | 1,759.5 | -391.1 | -664.1 | 137.74% |
| 32,768 | -881.9 | 4,828.4 | 19,057.2 | 40.93 | 1,384.1 | 13,920.5 | -7,443.5 | -11,390.1 | 181.82% |
| 262,144 | -4,556.6 | 26,331.9 | 98,856.0 | 27.85 | 8,529.6 | 118,196.2 | 6,226.2 | -15,549.1 | 113.16% |
| 1,048,576 | -7,494.6 | 86,125.7 | 339,362.4 | 22.95 | 27,686.7 | 461,941.3 | 87,374.6 | 8,743.4 | 98.11% |
| 2,097,152 | 565.8 | 161,259.5 | 643,557.8 | 21.06 | 50,542.3 | 929,258.9 | 235,703.6 | 73,878.3 | 92.05% |
| 4,194,304 | 7,042.5 | 286,329.4 | 1,170,759.3 | 18.63 | 89,185.2 | 1,874,243.5 | 621,322.8 | 327,951.0 | 82.50% |

The signed-mean bound closes on four of six scales, beginning at 262K. The stronger sign-free bound treats every Ramanujan mean contribution adversarially and closes only on the last three scales, from 1M through 4M. Small-scale failures are retained; no monotonic or asymptotic conclusion is inferred from the terminal run.

At 4M the sign-free bound no longer reads the signs or magnitudes of the 31 final block sums. It uses only the per-denominator real means, centered L2 norms, exact rational geometry, and independent transfer/variation budgets. This is weaker information than TICKET-113 and a more plausible target for weighted large-sieve or dispersion methods.

## Retained theorem

The next target is

```text
EventuallySubcriticalVaughanCenteredFareyNumeratorDispersionBudget
```

Its required statement is: there exist `X0` and `delta>0` such that for every `X>=X0`,

```text
Ramanujan mean absolute envelope
+ centered projected-L2 envelope
+ rational-boundary Lipschitz envelope
+ Abel variation envelope
<= (1-delta) * known major-plus-Type-I-minor contribution.
```

The deterministic TICKET-114 inequality would then make the fixed-bump shift-two correlation positive for every sufficiently large `X`, allowing the existing contamination and infinitude bridge to apply. The missing work is to expand `P_{q,a}` into its Möbius/divisor bilinear coefficients and derive the centered second-moment budget with explicit constants.

## Literature boundary

Helfgott's minor-arc work combines Vaughan Type II sums with weighted large-sieve geometry and explicitly exploits Farey-fraction structure. Maynard and Lichtman establish strong mean-value estimates for primes in arithmetic progressions with well-factorable or spectral weights. These provide relevant proof architectures, but none states the project-specific endpoint second-moment inequality above.

- H. A. Helfgott, [Minor arcs for Goldbach's problem](https://arxiv.org/abs/1205.5252)
- J. Maynard, [Primes in arithmetic progressions to large moduli II: Well-factorable estimates](https://arxiv.org/abs/2006.07088)
- J. D. Lichtman, [Primes in arithmetic progressions to large moduli, and Goldbach beyond the square-root barrier](https://arxiv.org/abs/2309.08522)

## 한국어 요약

TICKET-114는 TICKET-113의 31개 분모 블록을 다시 분자 `a`별로 열어, Ramanujan 평균항과 분자 중심화 편차항으로 정확히 분해합니다. 중심화 편차에 대해서는 평균 0 조건을 반영한 최적 L2 경계를 사용합니다. 이 경계는 주어진 약한 정보만으로는 더 개선할 수 없으며, 반대 위상 벡터가 정확한 추상 극값을 만듭니다.

4M에서는 평균항의 부호까지 모두 불리하게 처리해도 유한 하한 `+327,951.0`이 남습니다. 그러나 4K와 32K에서는 실패하고, 부호 없는 하한은 1M 이후 세 규모에서만 양수입니다. 따라서 이것은 무한 증명이 아니라 다음 정리를 고르는 근거입니다.

다음 목표는 실제 Vaughan Type-II 계수를 Möbius/약수 이중합까지 전개해, 분자별 중심화 L2 예산이 알려진 양의 항보다 일정 비율 작다는 것을 모든 충분히 큰 `X`에서 증명하는 것입니다. 리만 가설, 콜라츠 추측, 골드바흐 추측, 쌍둥이 소수 추측은 모두 여전히 미해결입니다.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket114_twin_ramanujan_numerator_dispersion_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket114_twin_ramanujan_numerator_dispersion_audit
```
