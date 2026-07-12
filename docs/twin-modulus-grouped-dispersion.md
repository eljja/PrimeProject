# TICKET-106: Twin modulus-grouped dispersion and sparse leakage

## English

TICKET-106 groups all TICKET-105 factorizations `q=dr` before applying norms:

```text
centered Type II = sum_q c_X(q) Delta_X(q).
```

The exact grouped identity replays below `4.3e-10` through 2M. Grouping is mathematically necessary, but naive grouped norms are worse: at 2M the outer-`d` Cauchy constant `41.15` becomes grouped `249.12`, and the negative-mass constant `5.41` becomes `55.29`.

The occupancy audit exposes a more serious issue. At 2M, 400,315 supported moduli, `72.31%` of all support, contain at most one block sample. They supply `64,933.8` of the total centered contribution `67,608.8`. Moduli with at most two samples account for `85.27%` of support. This is a sparse-modulus replay regime, not evidence for a dense arithmetic-progression theorem.

The retained target is `NonSparseModulusTwinDispersionWithSparseTailControl`: prove a dispersion estimate in a nondegenerate occupancy range and control the sparse large-modulus tail separately without treating one-row cells as averaged progression data.

### Literature boundary

Sparse-modulus distribution theorems already exist, so TICKET-106 does **not** claim that sparse-modulus dispersion is new. Baier and Zhao prove Bombieri-Vinogradov and Barban-Davenport-Halberstam type results for specified sparse sets of moduli. Helfgott's Type II analysis also states explicitly that very large `q`, equivalently very small `x/q`, requires separate treatment and can make elementary error terms dominate. The unresolved object here is narrower: the Vaughan-dependent signed coefficients `c_X(q)`, moduli extending almost to `X`, and a shifted-prime block whose observed support is dominated by occupancy-one cells. Applying an existing sparse-modulus theorem would require a proved reduction matching its modulus range, weights, averaging measure, and uniformity hypotheses; no such reduction is currently established.

## 한국어

TICKET-106은 같은 modulus `q=dr`의 여러 표현을 먼저 합친 뒤 dispersion 벡터를 만듭니다. 항등식은 정확히 재생되지만 단순 grouped Cauchy는 오히려 `K=249.12`, 음의 질량 경계는 `55.29`로 악화됩니다.

더 중요한 한계는 희소 modulus입니다. 2M에서 support의 `72.31%`가 블록 표본 1개 이하이며 전체 중심화 기여 `67,608.8` 중 `64,933.8`을 공급합니다. 이는 산술진행 평균이 아니라 개별 shifted-prime 행을 거의 그대로 보는 구간입니다.

따라서 다음 목표는 조밀 progression의 dispersion과 희소 tail을 분리하는 `NonSparseModulusTwinDispersionWithSparseTailControl`입니다. 네 난제는 아직 미해결입니다.

### 기존 문헌과의 경계

희소 모듈러스 분포 정리 자체는 이미 존재하므로 TICKET-106은 그것을 새 결과라고 주장하지 않습니다. Baier-Zhao는 특정 희소 모듈러스 집합에 대한 Bombieri-Vinogradov형 및 Barban-Davenport-Halberstam형 정리를 증명했습니다. Helfgott의 Type II 분석도 `q`가 매우 커서 `x/q`가 작아지는 구간은 별도 처리가 필요하고 단순 오차항이 지배할 수 있음을 설명합니다. 이 프로젝트에서 아직 남은 문제는 Vaughan 분해에 따라 달라지는 부호 가중치 `c_X(q)`, 거의 `X`까지 올라가는 모듈러스, 그리고 점유도 1인 셀이 지배하는 shifted-prime 블록을 동시에 다루는 것입니다. 기존 정리를 적용하려면 모듈러스 범위, 가중치, 평균 방식, 균일성 가정을 모두 만족하는 환원 정리가 먼저 필요하며, 현재 그런 환원은 증명되지 않았습니다.

## Primary references

- Stephan Baier and Liangyi Zhao, "Bombieri-Vinogradov Type Theorem for Sparse Sets of Moduli," *Acta Arithmetica* 125 (2006), 187-201. https://arxiv.org/abs/math/0602116
- Harald A. Helfgott, *The Ternary Goldbach Problem*, Chapter 5, especially Section 5.2 on Type II sums, large sieve, primes, and tails. https://arxiv.org/abs/1501.05438
