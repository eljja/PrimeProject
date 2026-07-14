# TICKET-113: Twin Farey denominator endpoint audit

## Claim boundary

TICKET-113 does **not** prove the Twin Prime Conjecture and does not certify a last-twin counterexample. It proves exact identities in the implemented finite algebra, reports a floating-point holdout audit, and identifies the next uniform inequality. The positive numerical lower bounds are not interval-certified proofs.

## Frozen structural rule

TICKET-112 left 96.05% of its Abel envelope in 162 independent cell endpoints. At the exploratory scale `X=262,144`, TICKET-113 attaches each endpoint to the denominator of its immediate **right** Farey boundary and freezes that rule before evaluating the corresponding statistic at `X=4,194,304`. This choice is canonical for the implemented Abel orientation: the endpoint is the last minor frequency before the next major arc.

The 4M scale had appeared in earlier PrimeProject tracks; it is not globally unseen data. What was held out is the new 31-block right-denominator endpoint statistic. No denominator subset, sign, fitted weight, or saving exponent is selected. All right-boundary denominators `q=2,...,32` are retained. Adjacent boundaries satisfy the Farey determinant-one identity on all 162 cells.

The exploratory audit also inspected a left-boundary grouping, whose 262K envelope ratio was numerically smaller at 25.85% versus 28.40% for the right grouping. It was not selected: the discrete Abel endpoint is oriented toward the right boundary, while choosing the left rule after comparing the numbers would introduce an extra tuning choice. Unordered denominator pairs and reflection orbits were also rejected because they retained 100% and 98.84% of the independent envelope, respectively.

For cell endpoint `E_C`, define

```text
D_q = sum E_C over cells C whose right boundary has denominator q.
```

Then

```text
sum_C E_C = sum_{q=2}^{32} D_q
Re(sum_q D_q) >= -sum_q |D_q|.
```

The first line is an exact regrouping. The second line takes only 31 absolute values, preserving cancellation among cells with the same canonical denominator. The within-cell Abel variation remains bounded independently, exactly as in TICKET-112.

## Results

| X | split | 162-cell endpoint envelope | 31-block endpoint envelope | variation envelope | block/cell | known term | grouped lower bound |
|---:|---|---:|---:|---:|---:|---:|---:|
| 4,096 | replay | 2,744.5 | 1,058.4 | 71.2 | 38.56% | 1,759.5 | 629.9 |
| 32,768 | replay | 37,357.2 | 11,542.1 | 1,384.1 | 30.90% | 13,920.5 | 994.3 |
| 262,144 | exploratory selection scale | 219,448.2 | 62,333.0 | 8,529.6 | 28.40% | 118,196.2 | 47,333.7 |
| 1,048,576 | replay | 679,381.7 | 221,845.0 | 27,686.7 | 32.65% | 461,941.3 | 212,409.6 |
| 2,097,152 | replay | 1,229,823.0 | 421,224.6 | 50,542.3 | 34.25% | 929,258.9 | 457,492.0 |
| 4,194,304 | new holdout | 2,161,424.6 | 767,682.2 | 89,185.2 | 35.52% | 1,874,243.5 | 1,017,376.2 |

The frozen grouping survives the new endpoint-statistic holdout at 4M. Its endpoint envelope is 35.52% of the independent-cell envelope, and the resulting finite lower expression is `1,017,376.2`. The endpoint sum itself is `-16,617.3`; the Type II minor contribution after adding Abel variation is `-9,418.2`. Thus the bound is not succeeding because the holdout endpoint happened to have a favorable sign.

Both exact reconstructions remain numerically stable at 4M: the Abel reconstruction error is `3.14e-9`, and the denominator-group identity error is `6.51e-11`.

## Countermodel and no-go result

Right-denominator labels do not by themselves force cancellation. Replace every endpoint by `-|E_C|` while preserving:

- its cell and right-denominator label;
- every per-cell magnitude;
- each group count;
- every norm depending only on those magnitudes.

This adversary restores the independent endpoint envelope. At 4M it gives lower expression `-376,366.3`; the same magnitude-and-label route fails at all six audited scales. This is a logical countermodel to any proof using only those invariants. It is **not** asserted to be realizable by Vaughan coefficients.

Therefore the retained target is

```text
UniformRightFareyDenominatorEndpointBudgetForVaughanCrossSpectrum
```

A proof must derive the phase relation inside each `D_q` from the Möbius/divisor structure of the Vaughan Type II coefficients and obtain a uniform bound in `X`. A stronger falsification target is a Vaughan-realizable coefficient sequence that preserves the required convolution identities while aligning a denominator block negatively.

## Literature boundary

Helfgott develops Vaughan Type II minor-arc estimates and exploits large-sieve geometry in the tails of minor arcs. Grimmelt and Teräväinen combine circle-method and sieve-weight distribution estimates for a binary Goldbach problem with almost-twin constraints. These are relevant architectures, but neither source states the one-sided 31-block endpoint budget required for the exact shift-two correlation here.

- H. A. Helfgott, [Minor arcs for Goldbach's problem](https://arxiv.org/abs/1205.5252)
- L. Grimmelt and J. Teräväinen, [The Exceptional Set in Goldbach's Problem with Almost Twin Primes](https://arxiv.org/abs/2207.08805)

## 한국어 요약

TICKET-113은 TICKET-112가 남긴 162개 끝점을 오른쪽 Farey 경계의 분모별로 정확히 묶습니다. 끝점이 다음 major arc 직전에 놓이므로 오른쪽 경계는 구현된 Abel 방향에서 자연스럽고, 끝점의 부호를 보고 고른 규칙이 아닙니다. `q=2,...,32`를 모두 사용하므로 162개 절댓값 대신 31개 분모 블록의 절댓값만 취합니다.

4M 규모 자체는 이전 연구에서 사용된 적이 있지만, 새 31블록 끝점 통계는 규칙을 고를 때 확인하지 않았습니다. 이 선택 후 holdout에서 끝점 envelope는 `2,161,424.6`에서 `767,682.2`로 줄었습니다. 변동항 `89,185.2`를 더해도 알려진 항 `1,874,243.5`보다 작아서 유한 하한 `1,017,376.2`를 남깁니다. 하지만 이는 부동소수점 유한 계산이며 무한히 많은 `X`에 대한 증명이 아닙니다.

또한 각 끝점의 크기와 분모 라벨을 그대로 두고 위상만 모두 음수 방향으로 정렬하면 하한이 `-376,366.3`이 됩니다. 따라서 “같은 분모끼리 묶으면 상쇄된다”는 설명만으로는 증명할 수 없습니다. 다음 핵심은 Vaughan Type-II 계수의 산술적 위상 관계에서 31개 블록의 균일 상쇄 부등식을 유도하는 것입니다. 쌍둥이 소수 추측과 나머지 세 난제는 여전히 미해결입니다.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket113_twin_farey_denominator_endpoint_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket113_twin_farey_denominator_endpoint_audit
```
