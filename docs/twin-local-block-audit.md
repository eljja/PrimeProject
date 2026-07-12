# TICKET-103: Twin local-block Vaughan audit

## English

TICKET-103 corrects a hidden weakness in TICKET-102. The earlier dyadic audit evaluated every endpoint `x` in `(X/2,X]`, but each component correlation was cumulative from zero to `x`. Positive Type II mass below `X/2` could therefore hide a negative contribution in the current analytic block.

For each horizon `X`, TICKET-103 fixes one modulus `W_X`, one Vaughan decomposition `U(X),V(X)`, and computes the exact local identity on `n in (X/2,X]`:

```text
C_2(X/2,X] - M_X
  = (structured local correlation - M_X)
    + Type II local correlation.
```

Across the seven principal blocks from 125K through 8M, all Type II block sums are positive. The maximum required structured constant is `3.7617`, the maximum Type II constant is `0`, and the maximum joint constant is `0.6430`. All reconstruction and noncollapse contracts pass over 7,937,500 integers.

This positivity is not an identity. A small-scale sign oracle finds the exact counterexample `X=1000`: on `(500,1000]`, the Type II local correlation is `-174.7165` and requires `K_II=1.7515`. Therefore universal local Type II nonnegativity is false. The large-block sign pattern may motivate an eventual finite lower bound, but it cannot be promoted without analysis.

The retained sufficient theorem is `UniformDyadicLocalVaughanTwinBlockBudgets`: prove that some fixed finite `K_S,K_II` bound every sufficiently large local dyadic block. A positive linear local main then dominates proper-prime-power contamination `o(X)`, forcing genuine twin-prime weight in every sufficiently large block. Support density only prevents a collapsed decomposition; it is not the required bilinear estimate.

## 한국어

TICKET-102는 dyadic 구간의 모든 끝점 `x`를 검사했지만 상관합은 `0..x` 누적값이었습니다. 이전 절반의 양의 Type II 질량이 현재 블록의 음의 기여를 가릴 수 있으므로, TICKET-103은 `(X/2,X]` 자체의 국소 상관을 정확히 다시 계산합니다.

125K부터 8M까지 7개 주요 블록에서는 Type II 합이 모두 양수였습니다. 구조항 최대 필요 상수는 `3.7617`, 결합 잔차 최대는 `0.6430`이고 재구성 실패는 없습니다.

하지만 작은 규모에서 정확한 반례가 나왔습니다. `X=1000`, 즉 `(500,1000]`에서 Type II 국소 상관은 `-174.7165`, 필요 상수는 `1.7515`입니다. 따라서 “Type II 국소합은 항상 비음수”라는 명제는 거짓입니다. 남는 목표는 비음성이 아니라 충분히 큰 모든 dyadic 블록에서 성립하는 **고정 유한 하한**입니다.

네 난제는 여전히 미해결이며, 이 반례는 Twin Prime의 반례가 아니라 보조정리 후보의 반례입니다.

## Reproduce / 재현

```text
D:\python\anaconda3\python.exe scripts\ticket103_twin_local_block_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket103_twin_local_block_audit
```
