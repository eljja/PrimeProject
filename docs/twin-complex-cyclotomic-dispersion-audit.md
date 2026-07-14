# TICKET-115: Twin complex cyclotomic dispersion audit

## Claim boundary

TICKET-115 does **not** prove the Twin Prime Conjecture and does not certify a last-twin counterexample. It proves an exact finite complex decomposition, a sharp finite-dimensional support theorem under a stated weak contract, and a six-scale comparison of two mean-orientation contracts. The Vaughan coefficients in the scale rows are measured floating-point quantities, not a uniform estimate in `X`.

## Exact complex mean decomposition

TICKET-114 writes only the real part of each denominator block coefficient as a mean plus a centered remainder. TICKET-115 removes the full complex constant mode. For the endpoint coefficients attached to reduced numerators `0<a<=q/2`, write

```text
P_{q,a} = M_q + Z_{q,a},       sum_a Z_{q,a}=0.
```

Define the half-Farey cyclotomic phase sum

```text
H_q = sum_a exp(4 pi i a/q).
```

Its real part is the familiar half Ramanujan sum, `c_q(2)/2` for `q>2` and `c_2(2)` for `q=2`. Its imaginary part generally does not vanish and must not be discarded. The exact rational-boundary identity is

```text
Re sum_a P_{q,a} rho_{q,a}
  = Re(M_q H_q)
  + Re sum_a Z_{q,a}(rho_{q,a}-mean_a rho_{q,a}).
```

The projected phase geometry also has the exact identity

```text
||rho-mean(rho)||_2^2 = n_q - |H_q|^2/n_q.
```

Across all six scales, the maximum per-block decomposition error is below the registered `1e-7` tolerance, all denominator supports remain exactly `q=2,...,32`, and no contract failure occurs.

## Sharp centered support theorem

The centered term satisfies

```text
|Re sum_a Z_{q,a}(rho_{q,a}-mean rho_q)|
  <= ||Z_q||_2 ||rho_q-mean rho_q||_2.
```

This is optimal under only complex zero mean and a fixed L2 norm. Equality is attained by choosing `Z_q` proportional to the negative complex conjugate of the projected phase vector. This extremizer is abstract; it is not claimed to satisfy the Möbius/divisor convolution identities of actual Vaughan coefficients.

## Two mean contracts

The same decomposition produces two different proof contracts.

1. **Scalar-aware:** retain the actual scalar orientation and pay `sum_q |Re(M_q H_q)|`.
2. **Orientation-free:** discard the orientation and pay `sum_q |M_q||H_q|`.

The second contract looks more uniform but is strictly weaker. It enlarges the numerator budget on all six audited scales and removes the 1M finite closure. Complex centering alone is therefore not an improvement; the scalar cyclotomic mean orientation is essential information.

| X | TICKET114 budget | scalar-aware complex | retained | orientation-free complex | retained | scalar lower | free lower |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4,096 | 2,330.1 | 2,274.3 | 97.60% | 2,385.8 | 102.39% | -608.3 | -719.8 |
| 32,768 | 23,885.6 | 23,508.3 | 98.42% | 25,194.7 | 105.48% | -11,012.8 | -12,699.2 |
| 262,144 | 125,187.9 | 123,805.2 | 98.90% | 132,787.0 | 106.07% | -14,166.4 | -23,148.2 |
| 1,048,576 | 425,488.2 | 423,229.7 | 99.47% | 450,153.0 | 105.80% | 11,001.9 | -15,921.4 |
| 2,097,152 | 804,817.3 | 799,975.8 | 99.40% | 849,145.4 | 105.51% | 78,719.7 | 29,550.1 |
| 4,194,304 | 1,457,088.7 | 1,449,516.0 | 99.48% | 1,536,912.6 | 105.48% | 335,523.7 | 248,127.1 |

The scalar-aware contract improves the numerator budget at every row, but the improvement is modest and shrinks to `0.52%` at 4M. Its sign-free lower expression is positive only on the last three scales. Neither fact implies an asymptotic estimate.

## Retained theorem

The next target is

```text
EventuallySubcriticalVaughanCyclotomicMeanAndComplexCenteredNumeratorBudget
```

It must prove that, for some `X0` and `delta>0` and every `X>=X0`,

```text
sum_q |Re(M_q H_q)|
+ sum_q ||Z_q||_2 ||rho_q-mean rho_q||_2
+ rational-boundary transfer
+ Abel variation
<= (1-delta) * major-plus-Type-I-minor contribution.
```

The theorem must also establish the positive scale of the right-hand side; measured finite positivity cannot be imported as a premise. A negative result would be a Vaughan-realizable coefficient family that saturates the centered support or destroys every fixed margin.

## Literature boundary

Helfgott's minor-arc analysis and the mean-value methods of Maynard and Lichtman provide relevant Farey, large-sieve, and dispersion architectures. They do not state the project-specific half-Farey complex mean budget above.

- H. A. Helfgott, [Minor arcs for Goldbach's problem](https://arxiv.org/abs/1205.5252)
- J. Maynard, [Primes in arithmetic progressions to large moduli II: Well-factorable estimates](https://arxiv.org/abs/2006.07088)
- J. D. Lichtman, [Primes in arithmetic progressions to large moduli, and Goldbach beyond the square-root barrier](https://arxiv.org/abs/2309.08522)

## 한국어 요약

TICKET-115는 분자별 endpoint 계수에서 실수 평균뿐 아니라 복소 평균 전체를 분리합니다. 이때 오른쪽 경계 위상의 합 `H_q`는 실수 Ramanujan 합뿐 아니라 일반적으로 0이 아닌 허수 cyclotomic 성분을 가집니다.

실제 평균항 `Re(M_qH_q)`의 방향을 보존하면 여섯 규모에서 TICKET-114보다 예산이 조금 줄어듭니다. 4M 유한 하한은 `+335,523.7`입니다. 그러나 방향을 모두 버리고 `|M_q||H_q|`로 처리하면 여섯 규모에서 전부 악화되고 1M의 양성 하한도 사라집니다. 따라서 “복소 평균을 분리하기만 하면 더 강하다”는 경로는 폐기합니다.

남은 과제는 실제 Vaughan Type-II Möbius/약수 계수로부터 평균 스칼라 방향과 복소 중심화 L2 예산을 동시에 모든 충분히 큰 `X`에서 제어하는 것입니다. 리만 가설, 콜라츠 추측, 골드바흐 추측, 쌍둥이 소수 추측은 모두 여전히 미해결입니다.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket115_twin_complex_cyclotomic_dispersion_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket115_twin_complex_cyclotomic_dispersion_audit
```
