# TICKET-107: Twin sparse-tail Vaughan recombination

## English

TICKET-107 continues the exact TICKET-106 modulus split, but refuses to treat each occupancy-one modulus as an independent observation. Every sparse modulus `q` is mapped to its unique integer `n=qm` in the dyadic block, repeated `n` values are combined, and the resulting vector is checked against an independently constructed Vaughan decomposition:

```text
II_X(n) = II_sparse,X(n) + II_dense,X(n),
C_X - M_X = (I_X - M_X) + <II_sparse,X,Lambda_shift> + <II_dense,X,Lambda_shift>.
```

All q-to-n, Vaughan-vector, and correlation identities pass through 8M. At 8M, 1,589,098 occupancy-one q cells compress to 1,099,268 n cells. There are 247,461 n cells with two sparse-q representations, and q-to-n grouping retains only `69.53%` of the sparse coefficient L1 mass. Thus occupancy-one q cells are not independent samples; cancellation remains after the modulus stage.

The signed component audit is more important. At 8M the structured residual is `-1,281,289.5`, sparse Type II is `+399,460.6`, and dense Type II is `+756,121.9`, producing a full residual of `-125,707.0`. The structured-plus-sparse one-sided constant rises to `2.59`, while the full joint constant is `0.37`. The centered sparse sign also changes across the audited horizons. These observations refute fixed-sign and standalone-triangle proof shortcuts, but they do not prove an asymptotic bound.

The retained target is `JointStructuredSparseDenseTwinDispersion`: use the sparse/dense split internally, but preserve all three signed components through the final uniform estimate. Assigning independent one-sided budgets can destroy the compensation needed by the exact identity.

## 한국어

TICKET-107은 TICKET-106의 희소 모듈러스 `q`를 독립 표본으로 취급하지 않고, 각 `q`가 블록에서 가리키는 유일한 정수 `n=qm`으로 다시 합칩니다. 그 결과를 별도로 계산한 Vaughan 분해 `Lambda=I+II`와 비교해 `II=II_sparse+II_dense` 및 전체 상관 항등식을 검증했습니다.

800만에서 표본 하나짜리 `q` 셀 1,589,098개는 실제 `n` 셀 1,099,268개로 줄어듭니다. 이 중 247,461개 `n`은 두 개의 희소 `q` 표현을 가지며, `n`별 결합 뒤 남는 L1 질량은 원래의 `69.53%`입니다. 즉, 표본 하나짜리 모듈러스라고 해서 서로 독립인 것은 아니며 모듈러스 결합 이후에도 추가 상쇄가 존재합니다.

800만 블록의 구조화 잔차는 `-1,281,289.5`, 희소 Type II는 `+399,460.6`, 조밀 Type II는 `+756,121.9`입니다. 세 항을 모두 합친 잔차는 `-125,707.0`입니다. 구조화+희소 항만 독립적으로 제한할 때 필요한 상수는 `2.59`지만 전체 공동 상수는 `0.37`입니다. 따라서 희소 꼬리, 조밀 항, 구조화 항에 각각 독립적인 단방향 예산을 배정하면 실제 상쇄를 잃을 수 있습니다.

다음 목표는 `JointStructuredSparseDenseTwinDispersion`입니다. 희소/조밀 구분은 내부 분석에 사용하되 최종 균일 추정까지 세 성분의 부호를 함께 보존해야 합니다. 이는 아직 쌍둥이 소수 추측의 증명이나 반례가 아닙니다.
