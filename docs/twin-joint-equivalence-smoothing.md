# TICKET-108: Twin joint equivalence no-go and smoothed excess bridge

## English

TICKET-108 audits the novelty of TICKET-107's retained target before attempting another estimate. Since

```text
Lambda = I + II_sparse + II_dense,
```

the proposed three-component hard-cutoff lower bound is term-for-term the original correlation residual bound. The two expressions agree through 8M, with maximum audited absolute error below `4.2e-9`. `JointStructuredSparseDenseTwinDispersion` is therefore an exact restatement, not a weaker intermediate theorem, and is discarded as a no-reduction route.

The replacement uses the fixed nonnegative bump

```text
W(t)=16(t-1/2)(1-t),  1/2<=t<=1,
```

and zero outside that interval. It satisfies `0<=W<=1`. Define

```text
S_W(X)=sum_n W(n/X)Lambda(n)Lambda(n+2).
```

The proper-prime-power contribution is nonnegative and bounded by the TICKET-93 contamination bound `B(X)`. Hence

```text
limsup_X (S_W(X)-B(X))=+infinity
```

implies infinitely many twin primes. The contrapositive is exact: if only finitely many twin primes exist, every sufficiently large bump window contains no genuine twin pair and `S_W(X)<=B(X)`.

Smoothing is not retained because it looks numerically better. It improves the required finite constant on only two of six audited blocks and worsens it on all four blocks from 1M through 8M. At 8M the hard constant is `0.3691` and the smooth constant is `0.4226`. Its value is analytic: the fixed bump removes hard endpoints and admits Fourier/Mellin transforms without changing the nonnegative contamination logic.

The next target is `SmoothedShiftTwoTypeIICorrelationExcess`. No such uniform signed Type II estimate is currently proved.

## 한국어

TICKET-108은 TICKET-107의 다음 목표가 실제로 더 약한 정리인지 먼저 검사합니다. `Lambda=I+II_sparse+II_dense`이므로 세 성분을 전부 합친 hard-cutoff 하한은 원래 상관 잔차 하한과 항별로 완전히 같습니다. 800만까지 두 식의 최대 오차는 `4.2e-9`보다 작습니다. 따라서 `JointStructuredSparseDenseTwinDispersion`은 새로운 환원이 아니라 원래 문제의 재표기이며 폐기합니다.

대신 `[1/2,1]`에서 `W(t)=16(t-1/2)(1-t)`인 비음수 bump를 사용합니다. `0<=W<=1`이므로 가중된 소수 거듭제곱 오염은 기존 명시적 상계 `B(X)`를 넘지 않습니다. 따라서 `S_W(X)-B(X)`가 위로 무한히 커진다면 쌍둥이 소수는 무한합니다. 쌍둥이 소수가 유한하다고 가정하면 충분히 큰 모든 bump 구간에는 실제 쌍둥이 소수가 없고 `S_W(X)<=B(X)`가 되어 모순입니다.

Smoothing은 유한 수치가 좋아서 선택한 것이 아닙니다. 6개 블록 중 2개에서만 상수가 개선됐고 100만부터 800만까지 4개에서는 악화됐습니다. 800만에서 hard 상수는 `0.3691`, smooth 상수는 `0.4226`입니다. 유지 이유는 경계 불연속을 제거하여 Fourier/Mellin 분석이 가능한 고정 커널을 제공하기 때문입니다.

다음 목표는 `SmoothedShiftTwoTypeIICorrelationExcess`입니다. 이는 아직 증명되지 않았으며 네 난제의 증명이나 반례도 아닙니다.
