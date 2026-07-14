# TICKET-118: Preregistered canonical adjacent-pair 8M holdout

## Claim boundary

TICKET-118 does **not** prove the Twin Prime Conjecture, an eventual endpoint bound, or an asymptotic pairing law. It records one finite post-registration test of a rule and primary endpoint committed before the 8M coefficients were computed.

TICKET-118은 **쌍둥이 소수 추측, eventual endpoint 경계, 점근적 pairing 법칙을 증명하지 않습니다.** 8M 계수를 계산하기 전에 규칙과 1차 판정식을 Git에 고정한 뒤 수행한 단 한 번의 유한 holdout입니다.

## Registration

The preregistration was pushed as commit `5b52d4d58873afc512555ba6079d4280f61757ae`. At that commit the result artifact did not exist. The registered inputs were:

- horizon `X=8,388,608`;
- list every nonempty truncated outer-divisor dyadic shell in increasing order;
- pair shell indices `(0,1),(2,3),...`, retaining an odd final shell alone;
- use exactly the same partition for every right-Farey denominator `q=2,...,32`;
- do not optimize partitions, signs, subsets, weights, exponents, or denominator-specific groups after observing 8M;
- pass only when the finite lower expression is strictly positive.

사전등록 커밋에서는 결과 JSON이 존재하지 않았습니다. 낮은 shell부터 인접한 두 개씩 묶고 마지막 shell이 남으면 단독으로 두는 규칙을 모든 분모에 동일하게 적용했습니다. 8M 결과를 본 뒤 partition이나 임계값을 바꾸지 않았습니다.

Machine-readable registration: `data/open-problem/ticket118-canonical-adjacent-pair-preregistration.json`.

## Primary result

The registered endpoint passed:

```text
known comparison term                         3,727,382.4078
canonical adjacent-pair numerator budget     3,412,519.6296
rational-boundary envelope                         17.6934
Abel variation envelope                        158,118.1148
finite lower expression                        156,726.9700
```

The canonical budget is `1.193875` times the fully signed numerator budget `2,858,354.9111`. This is a valid finite closure for the frozen 8M statistic. It is not a proof that the lower expression stays positive for all sufficiently large `X`.

사전등록한 1차 판정값은 `+156,726.9700`으로 통과했습니다. canonical paired 예산은 완전 signed 예산의 `1.193875배`입니다. 이는 고정된 8M 통계량의 유한 폐쇄이며, 충분히 큰 모든 `X`에서 양수라는 뜻이 아닙니다.

## Secondary checks

The 8M shell count is nine. The canonical groups are

```text
(D128,D256), (D512,D1024), (D2048,D4096),
(D8192,D16384), (D32768).
```

The preregistered canonical partition equals the post-hoc best width-two contiguous partition. This was a secondary endpoint and did not alter the primary test. Group budgets are:

| group | actual outer divisors | numerator budget |
|---|---:|---:|
| `D128-D256` | 204-511 | 1,598,458.4 |
| `D512-D1024` | 512-2,047 | 1,124,933.6 |
| `D2048-D4096` | 2,048-8,191 | 433,536.2 |
| `D8192-D16384` | 8,192-32,767 | 211,787.5 |
| `D32768` | 32,768-48,770 | 43,803.9 |

The first group contributes 46.84% of the paired budget. Time-domain, endpoint-profile, phase, and Gram reconstruction contracts remain within registered tolerances. The singleton-dyadic budget is `4,426,756.9`; denominator Cauchy gives `4,271,193.7`. The canonical pairing is materially better than both.

8M에서도 낮은 외측 약수 두 쌍이 예산 대부분을 차지합니다. canonical partition은 사후 최적 폭-2 partition과 같았지만, 이 일치는 2차 관측일 뿐 규칙 선택에 사용하지 않았습니다.

## What was learned

Retain:

- signed cancellation inside factor-four outer-divisor groups;
- one partition fixed across all denominators;
- the low-divisor group as the first analytic target;
- preregistered finite holdouts as selection-bias controls.

Discard:

- claims that repeated finite closure proves eventual positivity;
- data-dependent regrouping by denominator;
- singleton dyadic and denominator-Cauchy bounds as terminal arguments;
- transfer of this Twin-specific result to RH, Collatz, or Goldbach.

## Next theorem

```text
EventuallySubcriticalCanonicalAdjacentDyadicPairVaughanEndpointBudget
```

The next proof attempt must expand each canonical factor-four group into the actual signed Möbius/divisor bilinear form and prove a denominator-summed bound with a fixed margin on one all-sufficiently-large-`X` range. The major-plus-Type-I comparison term must be positive on that same range. A valid negative result is an unbounded Vaughan-realizable scale sequence that defeats every fixed margin.

다음 단계는 8M 계산을 반복하는 것이 아닙니다. 각 factor-four canonical group의 실제 Möbius bilinear 합을 전개하고, 분모 합산 상계를 충분히 큰 모든 규모에서 고정 margin으로 증명해야 합니다. 반례 방향은 모든 고정 margin을 깨는 무한 Vaughan-realizable 규모 열입니다.

## Reproduction

```powershell
python scripts/ticket118_twin_canonical_adjacent_pair_holdout.py
python -m unittest tests.test_ticket118_twin_canonical_adjacent_pair_preregistration
```

Result artifact: `data/open-problem/ticket118-twin-canonical-adjacent-pair-holdout.json`.
