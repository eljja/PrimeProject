# TICKET-98: Growing-modulus leakage audit

## English

TICKET-98 tests the next target left by TICKET-97: let the residue modulus grow with the numerical scale. The result is a precise rejection criterion, not a proof of any open conjecture.

For a finite dataset `x_0,...,x_{L-1}`, let `P_W x` be the fitted residue-class mean modulo `W`. If `W>=L`, the map `n -> n mod W` is injective on the dataset. Every occupied class then contains one observation, so

```text
P_W x = x,                 E_W = x-P_W x = 0.
```

Any correlation lower bound based on this zero residual equals the already observed exact correlation. It is an in-sample replay, not a theorem about an unseen scale.

The machine audit follows the primorial chain

```text
2, 6, 30, 210, 2310, 30030, 510510, 9699690
```

at `N=10,000`, `100,000`, and `1,000,000`. At every scale, the first Goldbach and shift-two norm certificates occur exactly at the first row-unique modulus:

| N | first certificate | observations per occupied residue | interpretation |
|---:|---:|---:|---|
| 10,000 | 30,030 | 1 | exact-data replay |
| 100,000 | 510,510 | 1 | exact-data replay |
| 1,000,000 | 9,699,690 | 1 | exact-data replay |

No non-row-unique projection certifies either sharp prime-power contamination budget. In particular, `W=510,510` at `N=1,000,000` leaves at most two observations in each occupied residue and still fails both lower bounds.

The retained target is stronger and falsifiable: choose or estimate the growing projection independently of the target statistic, keep a nondegenerate occupancy regime, and prove a signed binary residual estimate uniform in scale. Suggested theorem names are `OutOfSampleGrowingModulusBinaryResidualCancellation` and `OutOfSampleGrowingModulusShiftTwoResidualCancellation`.

## 한국어

TICKET-98은 TICKET-97이 남긴 다음 경로, 즉 수치 범위와 함께 residue modulus를 키우는 방법을 검사합니다. 결론은 난제의 증명이 아니라 **데이터 누출을 판별하는 정확한 기준**입니다.

길이 `L`인 유한 데이터에서 `W>=L`이면 서로 다른 두 index가 같은 `mod W` residue를 가질 수 없습니다. 따라서 각 residue 평균은 그 한 관측값 자체이고, `P_W x=x`, residual `E_W=0`이 됩니다. 이때 residual norm이 0이라는 사실은 새로운 소거 정리가 아니라 이미 본 데이터를 residue label로 그대로 외운 결과입니다.

실험에서는 위 primorial 사슬을 `10^4`, `10^5`, `10^6`까지 추적했습니다. Goldbach와 Twin 상관합의 최초 인증은 세 범위 모두 각 residue에 관측값이 하나만 남는 최초 지점에서 발생했습니다. row-unique 이전의 인증은 0건입니다. 따라서 “모듈러스를 충분히 키우면 증명된다”는 경로는 폐기합니다.

다음 단계는 학습 구간과 평가 구간을 분리하거나 외부의 산술 정리로 projection을 정하고, 각 산술 cell에 충분한 표본이 남는 상태에서 signed residual convolution 또는 shift-two correlation을 균일하게 제어하는 것입니다. 현재 결과는 Goldbach, Twin Prime, RH, Collatz의 증명도 반례도 아닙니다.

## Reproduce / 재현

```text
D:\python\anaconda3\python.exe scripts\ticket98_growing_modulus_leakage_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket98_growing_modulus_leakage_audit
```
