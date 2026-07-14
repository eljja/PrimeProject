# TICKET-116: Twin Möbius-sign cyclotomic audit

## Claim boundary

TICKET-116 does **not** prove the Twin Prime Conjecture and does not certify a last-twin counterexample. It proves an exact finite lift of the TICKET-115 half-Farey endpoint coefficients into the actual positive and negative outer-Möbius layers of Vaughan's Type-II identity. It also proves the corresponding centered polarization identity and audits a deliberately weaker contract that bounds the two sign layers independently.

The six scale rows use measured finite DFTs through `X=4,194,304`. They do not establish a uniform estimate in `X`.

## Exact Vaughan sign lift

For the project cutoffs `U(X),V(X)`, write the Type-II sequence as

```text
II(n) = II+(n) - II-(n),
```

where `II+` sums the outer divisors with `mu(d)=+1` and `II-` sums those with `mu(d)=-1`:

```text
II±(n) = sum_{d>U, mu(d)=±1} sum_{r>V, drm=n} Lambda(r).
```

Both layers are nonnegative before subtraction. Linearity of the DFT, cross-spectrum, minor-cell prefix sum, and Farey endpoint map gives

```text
P_{q,a} = P+_{q,a} - P-_{q,a}.
```

After complex centering in each sign layer,

```text
M_q = M_q+ - M_q-,
Z_q = Z_q+ - Z_q-.
```

The six rows reconstruct the time-domain Type-II sequence, all 31 denominator profiles, and the inherited TICKET-115 numerator budget within the registered floating-point tolerances.

## Exact polarization identity

The centered norm has the exact identity

```text
||Z_q||_2^2
  = ||Z_q+||_2^2 + ||Z_q-||_2^2
    - 2 Re <Z_q+, Z_q->.
```

The cross covariance is not assumed positive. Its denominator-summed value is negative at `4K` and `32K`, then positive at `262K`, `1M`, `2M`, and `4M`. This sign change blocks any claim that favorable covariance is automatic. When it is positive it reduces the signed centered norm; when negative it enlarges it.

## Independent-sign no-go

Consider the proof contract that pays the two Möbius sign layers independently:

```text
sum_q (|Re(M_q+ H_q)| + |Re(M_q- H_q)|)
+ sum_q (||Z_q+||_2 + ||Z_q-||_2)
          ||rho_q-mean(rho_q)||_2.
```

By the scalar and vector triangle inequalities this budget is always at least the signed TICKET-115 budget. The finite audit shows that it is strictly worse on all six rows and closes none of them.

| X | signed numerator budget | independent-sign budget | ratio | signed lower | independent lower | covariance sign |
|---:|---:|---:|---:|---:|---:|:---:|
| 4,096 | 2,274.3 | 3,237.5 | 1.424 | -608.3 | -1,571.5 | - |
| 32,768 | 23,508.3 | 33,347.8 | 1.419 | -11,012.8 | -20,852.3 | - |
| 262,144 | 123,805.2 | 240,181.1 | 1.940 | -14,166.4 | -130,542.4 | + |
| 1,048,576 | 423,229.7 | 989,662.0 | 2.338 | 11,001.9 | -555,430.4 | + |
| 2,097,152 | 799,975.8 | 2,021,804.7 | 2.527 | 78,719.7 | -1,143,109.2 | + |
| 4,194,304 | 1,449,516.0 | 4,187,038.4 | 2.889 | 335,523.7 | -2,401,998.7 | + |

At 4M, the mean envelope grows from `286,446.6` to `918,944.0`, while the centered envelope grows from `1,163,069.4` to `3,268,094.4`. The independent treatment therefore adds `2,737,522.4` to the numerator budget.

This does not show that every Möbius-based approach fails. It shows that expanding the exact Vaughan sum and then taking separate absolute values of its positive and negative Möbius layers cannot recover the retained finite budget.

## Retained theorem

The next target is

```text
EventuallySubcriticalSignedVaughanMobiusCyclotomicDispersionBudget
```

A valid proof must derive the scalar mean and centered endpoint estimates from the signed outer-Möbius sum before applying norms. Equivalently, a covariance-based route must prove a denominator-summed lower bound for

```text
sum_q Re <Z_q+, Z_q->
```

strong enough to keep the complete mean, centered, boundary-transfer, and Abel-variation budget below an independently established positive major-plus-Type-I-minor scale for every sufficiently large `X`.

A valid negative result would construct an unbounded sequence of actual Vaughan sign layers for which the scalar cancellation and centered covariance violate every fixed subcritical margin. Abstract vectors that do not satisfy the divisor-convolution identity are not counterexamples to this target.

## Literature boundary

Helfgott's Type-II treatment gives a relevant bilinear and large-sieve architecture. Lichtman proves averaged cancellation results for Möbius on shifted primes, and Ford-Maynard identify the need for substantial Type-I/II information in general prime-producing sieves. None supplies the fixed-shift, denominator-summed endpoint covariance required here.

- H. A. Helfgott, [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438)
- J. D. Lichtman, [Averages of the Möbius function on shifted primes](https://arxiv.org/abs/2009.08969)
- K. Ford and J. Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368)

## 한국어 요약

TICKET-116은 TICKET-115의 Farey endpoint 계수를 실제 Vaughan Type-II의 바깥 Möbius 부호에 따라 `양의 층 - 음의 층`으로 정확히 분해합니다. 시간영역 Type-II, 주파수 교차 스펙트럼, 31개 Farey 분모 블록에서 이 차이가 원래 계수를 재구성함을 검증했습니다.

핵심 항등식은 중심화 벡터의 편극식입니다.

```text
||Z||^2 = ||Z+||^2 + ||Z-||^2 - 2 Re<Z+,Z->.
```

교차 공분산은 4K와 32K에서 음수이고 이후 네 규모에서 양수입니다. 따라서 공분산이 항상 유리하다고 가정할 수 없습니다. 하지만 양·음 Möbius 층을 각각 절댓값 처리하면 평균 상쇄와 편극 항을 모두 잃습니다. 그 결과 독립 부호층 예산은 여섯 규모 전부 악화되고 양성 하한을 하나도 남기지 못합니다. 4M에서는 기존 `+335,523.7` 하한이 `-2,401,998.7`로 무너집니다.

폐기할 경로는 명확합니다. Möbius 부호층을 전개한 뒤 각 층에 독립 삼각부등식을 적용해서는 안 됩니다. 다음 정리는 실제 signed Möbius 합을 끝까지 보존한 bilinear dispersion 경계 또는 충분히 강한 분모 합산 공분산 하한을 모든 충분히 큰 `X`에서 증명해야 합니다. 네 난제는 모두 여전히 미해결입니다.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket116_twin_mobius_sign_cyclotomic_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket116_twin_mobius_sign_cyclotomic_audit
```
