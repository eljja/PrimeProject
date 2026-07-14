# TICKET-117: Signed dyadic Möbius endpoint Gram audit

## Claim boundary

This ticket does **not** prove the Twin Prime Conjecture and does not certify a counterexample. It proves finite algebraic identities for the audited Vaughan Type-II arrays and compares deterministic finite envelopes. No trend or selected partition is promoted to an all-sufficiently-large-`X` theorem.

이 티켓은 **쌍둥이 소수 추측을 증명하지 않았고 반례도 인증하지 않았습니다.** 실제 Vaughan Type-II 유한 배열에 대한 정확한 대수 항등식과 결정론적 유한 경계만 검증합니다. 관측된 추세나 선택된 partition을 충분히 큰 모든 `X`에 대한 정리로 승격하지 않습니다.

## Exact lift

Let `B` run over the truncated dyadic shells of the actual outer divisor `d>U`. Keep the Möbius sign inside each block:

```text
II(n) = sum_B II_B(n).
```

Linearity of the DFT, fixed minor-cell sum, and half-Farey endpoint map gives

```text
P_(q,a) = sum_B P_(q,a)^(B),
M_q     = sum_B M_q^(B),
Z_q     = sum_B Z_q^(B).
```

For every denominator, the centered energy has the exact real-Gram representation

```text
||Z_q||_2^2 = sum_(B,C) Re <Z_q^(B), Z_q^(C)>.
```

The time-domain, endpoint-profile, complex-centering, and Gram reconstruction contracts pass on all six scales. This identity retains cross-block cancellation and reinforcement before any norm is applied.

실제 바깥 약수 `d>U`를 절단된 dyadic shell로 나누되 각 블록 안에서는 Möbius 부호를 유지했습니다. DFT, 고정 minor cell 합, half-Farey endpoint 사상은 선형이므로 시간영역 분해가 endpoint 평균과 중심 벡터까지 정확히 전달됩니다. 실수 Gram 행렬은 블록 내부 노름뿐 아니라 블록 사이의 상쇄와 강화를 모두 보존합니다.

## Finite results

| `X` | blocks | fully signed budget | singleton-dyadic budget | ratio | best width-2 lower |
|---:|---:|---:|---:|---:|---:|
| 4,096 | 5 | 2,274.3 | 4,689.9 | 2.062 | -1,689.6 |
| 32,768 | 6 | 23,508.3 | 42,298.6 | 1.799 | -19,936.4 |
| 262,144 | 7 | 123,805.2 | 225,511.8 | 1.822 | -63,546.4 |
| 1,048,576 | 8 | 423,229.7 | 763,938.4 | 1.805 | -128,296.3 |
| 2,097,152 | 8 | 799,975.8 | 1,262,612.9 | 1.578 | -112,746.7 |
| 4,194,304 | 8 | 1,449,516.0 | 2,325,858.6 | 1.605 | -1,236.3 |

Singleton dyadic triangles worsen the fully signed budget on all six rows and close none. They improve on TICKET-116's separated-sign budget on the last four rows, including a reduction from `4,187,038.4` to `2,325,858.6` at 4M, but this is still insufficient.

각 dyadic 블록에 독립 삼각부등식을 적용하면 여섯 규모 모두 완전 signed 예산보다 나빠지고 한 행도 폐쇄하지 못합니다. 다만 4M에서는 TICKET-116의 부호 분리 예산 `4,187,038.4`를 `2,325,858.6`으로 줄입니다. 즉 블록 내부 Möbius 상쇄는 중요하지만 singleton block 경계만으로는 부족합니다.

## Adjacent-pair frontier

We exhaustively evaluated every horizon-wide contiguous partition with at most two adjacent dyadic shells per group. The partition is fixed across all denominators; it is never optimized separately by `q`. At 4M the optimum is

```text
(D128,D256), (D512,D1024), (D2048,D4096), (D8192,D16384).
```

It is also selected at 2M. At 4M it lowers the numerator budget to `1,786,276.0`, only `1,236.3` above finite closure. The first pair contributes `925,909.7`, or 51.8% of the paired budget. This is a useful localization, not a proof: the same bound is substantially negative at smaller scales, the partition was selected from finite data, and no uniform bilinear estimate has been proved.

분모별로 따로 최적화하지 않고 한 규모 전체에 동일한 연속 partition을 적용했습니다. 각 그룹에 인접 shell을 최대 두 개만 허용한 전수 탐색에서 2M과 4M은 같은 pairing을 선택했습니다. 4M 유한 폐쇄 부족분은 `1,236.3`까지 줄었지만 여전히 음수입니다. 가장 낮은 첫 쌍이 전체 paired 예산의 51.8%를 차지하므로 다음 공격 대상은 이 저약수 signed bilinear block입니다.

## Cauchy and Gram no-go

Collapsing the denominator direction by Cauchy-Schwarz is valid but does not close any row. At 4M its numerator budget is `2,278,375.7` and its finite lower expression is `-493,336.0`. The geometry-weighted off-diagonal Gram energy is net adverse on every audited row; the largest 4M reinforcing interactions are among `D128`, `D256`, `D512`, and `D1024`.

Therefore discard:

- separate positive/negative Möbius triangles;
- singleton dyadic triangles as the final proof bound;
- denominator Cauchy collapse as a sufficient closure mechanism;
- any claim that the finite 2M/4M pairing is eventually stable.

분모 방향 Cauchy-Schwarz는 올바른 상계지만 한 행도 폐쇄하지 못합니다. 또한 geometry-weighted off-diagonal Gram 에너지는 여섯 행 모두 순상쇄가 아니라 순강화입니다. 따라서 개별 부호층, singleton dyadic block, 분모 Cauchy만으로 끝내는 경로는 폐기합니다.

## Retained theorem target

```text
EventuallySubcriticalAdjacentDyadicPairVaughanEndpointBudget
```

Required proof objects:

1. A denominator-summed bilinear estimate for the actual adjacent-pair outer-divisor sums, retaining Möbius signs before norms.
2. A fixed all-sufficiently-large-`X` margin below the independently proved major-plus-Type-I comparison scale.
3. A non-data-selected partition rule, or a theorem that controls every allowed width-two partition.
4. A counterexample oracle searching for an unbounded Vaughan-realizable sequence that defeats every fixed margin.

필요한 것은 4M pairing을 그대로 외삽하는 일이 아닙니다. 실제 인접 dyadic pair의 Möbius 부호를 보존한 분모 합산 bilinear 상계, 동일한 `X` 범위에서의 양의 비교항, 데이터 선택과 독립적인 partition 규칙이 필요합니다. 반례 경로는 모든 고정 margin을 깨는 무한한 Vaughan-realizable 규모 열을 구성하는 것입니다.

## Reproduction

```powershell
python scripts/ticket117_twin_dyadic_mobius_endpoint_gram_audit.py
python -m unittest tests.test_ticket117_twin_dyadic_mobius_endpoint_gram_audit
```

Machine-readable artifact: `data/open-problem/ticket117-twin-dyadic-mobius-endpoint-gram-audit.json`.
