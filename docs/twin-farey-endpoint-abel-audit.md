# TICKET-112: Twin Farey-cell endpoint Abel audit

## English

TICKET-112 continues the exact Type II minor cross-spectrum from TICKET-111 without returning to energy-only estimates. The fixed `Q=32` minor mask has 162 connected Farey cells. Inside each cell, exact discrete Abel summation gives

```text
sum_{k=a}^b z_k p_k
  = Z_b p_b + sum_{k=a}^{b-1} Z_k (p_k-p_{k+1}),
```

where `z_k` is the Vaughan Type II cross-spectrum, `p_k` is the shift-two phase, and `Z_k` is the cell-local prefix sum. The identity reconstructs the Type II minor contribution through the 2M holdout below the registered numerical tolerance.

This reduction preserves substantially more phase information than singleton-bin magnitudes. At 2M, the phase-blind envelope `7,596,484.2` falls to the Farey-Abel envelope `1,280,365.2`, an 83.15% reduction. It is still insufficient: against known major-plus-Type-I-minor contribution `929,258.9`, the lower bound is `-351,106.4`.

The loss is now sharply localized. The endpoint absolute envelope is `1,229,823.0`, or 96.05% of the Farey-Abel total, while within-cell phase variation costs only `50,542.3`. The actual signed endpoint contribution is `+11,146.8`, only 0.91% of its absolute envelope. Further smooth-phase refinement inside cells is therefore not the main problem; cancellation among cell endpoints is.

No new exponent was selected. Applying TICKET-111's frozen `X^(-1/6)` factor only to endpoint mass, while retaining the full variation envelope, leaves a positive finite lower expression on the 2M holdout. This is evidence for a narrower candidate, not a theorem.

The next target is `UniformFareyCellEndpointCancellationForVaughanCrossSpectrum`: prove a one-sided endpoint cancellation estimate uniformly in `X`, independently of the observed twin correlation, or construct an arithmetic coefficient countermodel that refutes it.

### Literature boundary

Farey dissection, Vaughan identity, smoothing, Abel summation, and weighted large-sieve bounds are established. Helfgott's minor-arc analysis explicitly combines Vaughan Type II sums with weighted large-sieve geometry, and Tao uses smoothed exponential sums with Vaughan parameter optimization. Neither paper gives this exact binary shift-two endpoint inequality.

- Harald A. Helfgott, [Minor arcs for Goldbach's problem](https://arxiv.org/abs/1205.5252).
- Terence Tao, [Every odd number greater than 1 is the sum of at most five primes](https://arxiv.org/abs/1201.6656).

## 한국어

TICKET-112는 TICKET-111의 Type-II minor 교차 스펙트럼을 에너지 경계로 되돌리지 않고, 고정 `Q=32` minor 영역의 162개 Farey cell 안에서 정확한 Abel summation을 적용합니다. 각 cell의 Type-II 합은 endpoint 항과 cell 내부의 부드러운 위상 변화 항으로 정확히 분리됩니다.

2M에서 위상을 모두 버린 envelope `7,596,484.2`는 Farey-Abel 경계를 사용하면 `1,280,365.2`로 83.15% 감소합니다. 그러나 알려진 major+Type-I minor는 `929,258.9`이므로 하한은 여전히 `-351,106.4`입니다.

손실 위치는 훨씬 명확해졌습니다. endpoint 절댓값 합은 `1,229,823.0`으로 전체 Abel 경계의 96.05%이고, cell 내부 variation은 `50,542.3`에 불과합니다. 실제 signed endpoint는 `+11,146.8`로 절댓값 envelope의 0.91%입니다. 따라서 cell 내부를 더 세밀하게 나누는 것이 아니라 162개 endpoint 사이의 산술적 상쇄를 증명해야 합니다.

새 지수를 고르지 않고 TICKET-111의 `X^-1/6`을 endpoint에만 적용한 후보는 2M 유한 holdout에서 양의 하한을 남깁니다. 하지만 이것은 무한 정리가 아닙니다. 다음 목표는 `UniformFareyCellEndpointCancellationForVaughanCrossSpectrum`이며 네 난제는 여전히 미해결입니다.

## Reproduce / 재현

```text
D:\python\anaconda3\python.exe scripts\ticket112_twin_farey_endpoint_abel_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket112_twin_farey_endpoint_abel_audit
```
