# TICKET-105: Twin centered progression discrepancy

## English

TICKET-105 centers the TICKET-104 shifted-prime weight by an independent arithmetic-progression model. For `q=dr`, use the exact block count and the coprime progression mean

```text
E[Lambda(qm+2)] = q/phi(q)  if q is odd,
                    0       if q is even.
```

This gives the exact decomposition

```text
T_X = sum mu(d) A0_X(d)
    + sum mu(d) (A_X(d)-A0_X(d)).
```

`A0` does not read `Lambda(qm+2)`. The centered identity replays with error below `1.7e-10` through 2M. At 125K, 1M, and 2M, both the progression baseline component and centered discrepancy are positive.

Centering materially reduces the information-loss envelope. The termwise negative centered-mass constants are `4.50`, `5.15`, and `5.41`, compared with TICKET-104's uncentered negative-mass constants `21.75`, `34.79`, and `39.92`. Full-vector Cauchy-Schwarz still requires `26.69`, `37.12`, and `41.15`. These are finite observations, not uniform bounds.

The remaining object is now explicit:

```text
sum mu(d) Lambda(r)
    [Lambda(drm+2) - dr/phi(dr)]
```

over odd progressions in a dyadic block. The next target is `MobiusWeightedPrimeProgressionDiscrepancyBound`, using dispersion or bilinear large-sieve information before termwise absolute values or global Cauchy-Schwarz.

## 한국어

TICKET-105는 shifted-prime 가중치에서 합동조건을 반영한 독립 산술진행 주항을 먼저 제거합니다. 중심화 항등식은 2M까지 `1.7e-10` 이하 오차로 재생됩니다.

중심화 후 음의 항별 필요 상수는 `4.50→5.15→5.41`로, 중심화 전 `21.75→34.79→39.92`보다 크게 줄었습니다. 하지만 전체 벡터 Cauchy-Schwarz는 `26.69→37.12→41.15`가 필요합니다. 이는 유한 관측이며 균일 정리가 아닙니다.

남은 핵심은 `Λ(drm+2)-dr/φ(dr)`라는 소수 산술진행 분포 오차와 `μ(d)` 부호의 결합입니다. 다음 목표는 dispersion 또는 bilinear large sieve를 사용한 `MobiusWeightedPrimeProgressionDiscrepancyBound`입니다. 네 난제는 아직 미해결입니다.
