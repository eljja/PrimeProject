# TICKET-104: Twin Type II weighted-Möbius anatomy

## English

TICKET-104 expands the exact local Type II term from TICKET-103. For a dyadic block `(X/2,X]`, Vaughan's identity gives

```text
T_X = sum_{d>U} mu(d) A_X(d),
```

where every `A_X(d)` is nonnegative and sums shifted-prime mass `Lambda(r)Lambda(drm+2)` over `r>V` and `drm` in the block. The identity reconstructs the direct Type II correlation to absolute error at most `4.1e-11` on the audited horizons.

This identifies the real analytic object: a weighted Möbius sum whose weights depend on the shifted-prime sequence. Unweighted Mertens cancellation does not by itself control these weights.

Two information-losing bounds are audited:

1. Sum every negative outer-divisor term independently.
2. Apply Abel summation, then take absolute values of every Mertens-prefix contribution.

At horizons 125K, 1M, and 2M, the direct Type II term is positive and needs `K=0`. The negative-term bound requires `K=21.75`, `34.79`, and `39.92`; the Abel-triangle bound requires `K=354.06`, `799.04`, and `1088.15`. At `X=1000`, the actual negative Type II term needs only `K=1.7515`, while the Abel-triangle envelope needs `61.83`.

These finite rows do not prove that either envelope diverges. They show exactly where those templates lose the observed cancellation and prevent presenting them as completed Type II estimates. The retained target is `WeightedMobiusShiftedPrimeDyadicCancellation`: exploit joint structure between `mu(d)` and `A_X(d)` before applying absolute values.

This aligns with Ford and Maynard's conclusion that substantial Type II information and its geometry are essential in general prime-producing lower-bound sieves. See [Ford–Maynard](https://arxiv.org/abs/2407.14368).

## 한국어

TICKET-104는 TICKET-103의 국소 Type II 항을 정확한 가중 Möbius 합으로 분해합니다.

```text
T_X = Σ μ(d) A_X(d),  A_X(d)≥0
```

`A_X(d)`는 shifted-prime 질량을 포함하므로 일반적인 Mertens 함수 크기만으로는 필요한 상쇄를 보존하지 못합니다. 실제 Type II 항은 큰 감사 블록에서 양수였지만, 음의 항을 각각 제어하면 필요 상수가 `21.75 → 34.79 → 39.92`, Abel summation 뒤 삼각부등식을 적용하면 `354 → 799 → 1088`로 커집니다.

이 유한 결과가 상수의 발산을 증명하는 것은 아닙니다. 다만 항별 절댓값과 Abel-triangle 경로가 실제 상쇄를 어디서 잃는지 정확히 보여줍니다. 따라서 다음 목표는 unweighted Mertens bound가 아니라 shifted-prime 가중치와 Möbius 부호를 함께 다루는 `WeightedMobiusShiftedPrimeDyadicCancellation`입니다.

네 난제는 여전히 미해결입니다.

## Reproduce / 재현

```text
D:\python\anaconda3\python.exe scripts\ticket104_twin_typeii_mobius_anatomy.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket104_twin_typeii_mobius_anatomy
```
