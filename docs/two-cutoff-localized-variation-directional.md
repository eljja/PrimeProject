# TICKET-158: Two Cutoffs, Localized Gain, Phase Variation, and Directional Information

## Abstract

TICKET-158 continues PrimeProject's simultaneous attack on the Riemann
Hypothesis, the Collatz conjecture, the strong Goldbach conjecture, and the
Twin Prime conjecture. It proves four exact intermediate results and resolves
none of the conjectures.

For the Riemann track, it composes a positive archimedean tail with a separate
prime/band remainder and proves that controlling only the first cutoff cannot
promote finite positivity to the full Weil form. For Collatz, it constructs an
infinite valuation-word family proving that ordinary inversion count does not
determine the exact affine inversion gain, even after fixing length, valuation
sum, and multiset. For Goldbach, it proves a sharp cyclic moving-average
residual bound in terms of phase variation. For Twin Prime, it replaces an
absolute information budget by a one-sided positive-shift budget and proves
that unsigned mutual information cannot determine the shift direction.

Every proof DAG ends at `open_not_proven`. The machine audit records four exact
results, four rejected routes, zero conjecture resolutions, and zero failed
checks.

## 초록

TICKET-158은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 동시에 공격한다. 이번 회차는 정확한 중간 결과 네 개를
증명하지만 어떤 추측도 해결하지 않는다.

리만 가설 트랙에서는 양의 archimedean 꼬리와 별도의 prime/band
나머지를 합성하며, 첫 번째 cutoff만 제어해서는 유한 양성을 전체 Weil
form으로 승격할 수 없음을 증명한다. 콜라츠 트랙에서는 길이, valuation
합, multiset, 보통 inversion 수가 모두 같아도 정확한 affine inversion
gain이 달라지는 무한 valuation-word 반례군을 만든다. 골드바흐
트랙에서는 순환 이동평균의 잔차를 phase total variation으로 제어하는
날카로운 부등식을 증명한다. 쌍둥이 소수 트랙에서는 절댓값 정보 예산을
양의 조건부 편향만 세는 단방향 예산으로 교체하고, 부호 없는 mutual
information만으로는 편향 방향을 결정할 수 없음을 반례로 증명한다.

모든 proof DAG의 마지막 상태는 `open_not_proven`이다. 기계 감사는
정확 결과 4개, 폐기 경로 4개, 난제 해결 0개, 실패 0개를 기록한다.

---

## 1. Research protocol / 연구 프로토콜

Each track follows the same rule:

1. declare one exact proposition;
2. prove it algebraically;
3. run a reproducible finite audit;
4. construct a counterexample when the proposed shortcut is false;
5. separate the closed result from the remaining infinite theorem.

각 트랙은 다음 규칙을 따른다.

1. 정확한 명제를 먼저 선언한다.
2. 대수적으로 증명한다.
3. 재현 가능한 유한 감사를 실행한다.
4. 제안한 지름길이 틀리면 반례를 만든다.
5. 닫힌 결과와 남은 무한 정리를 분리한다.

The canonical artifact is:

`data/open-problem/ticket158-two-cutoff-localized-variation-directional.json`

Regeneration:

```powershell
python scripts/ticket158_two_cutoff_localized_variation_directional.py
python -m unittest tests.test_ticket158_two_cutoff_localized_variation_directional
```

---

## 2. Riemann Hypothesis

### 2.1 Exact proposition

Let `V_N` be a nested form core. On `V_N`, suppose

```text
0 <= q_{c,N,infinity}(f) - q_{c,N,T}(f)
   <= B_{c,N,T} ||f||^2
```

and

```text
|q(f) - q_{c,N,infinity}(f)| <= A_{c,N} ||f||^2.
```

Then

```text
q(f) >= q_{c,N,T}(f) - A_{c,N} ||f||^2
```

and

```text
q(f) <= q_{c,N,T}(f)
        + (A_{c,N} + B_{c,N,T}) ||f||^2.
```

Consequently:

- positivity of every finite form above `A_{c,N}` promotes to positivity on
  the full closed form domain;
- a finite value below `-(A_{c,N}+B_{c,N,T})` certifies a negative direction;
- driving only `B_{c,N,T}` to zero does not close the proof when `A_{c,N}` is
  uncontrolled.

### 2.2 Proof

The archimedean tail is positive, so

```text
q_{c,N,infinity}(f) >= q_{c,N,T}(f).
```

Subtracting the absolute prime/band remainder gives the lower bound. The tail
budget also gives

```text
q_{c,N,infinity}(f)
<= q_{c,N,T}(f) + B_{c,N,T} ||f||^2.
```

Adding the prime/band error gives the upper bound. If the lower bound is
nonnegative on every member of the nested form core, form-core density extends
it to the full domain.

### 2.3 Exact no-go

The scalar family in the artifact fixes the finite archimedean value at `+1`
and lets the positive tail budget tend to zero. An uncontrolled prime/band
remainder still sends the full value to `-1`. Therefore archimedean convergence
alone cannot imply full Weil positivity.

### 2.4 New literature boundary

Groskin's July 2026 paper proves a positive fixed-`(c,N)` archimedean tail and
an explicit finite certification budget. PrimeProject treats that theorem as
external prior work. TICKET-158 adds the separate composition audit and does
not claim the published theorem as new:

- [A finite Guinand-Weil dictionary and archimedean tail order](https://arxiv.org/abs/2607.02828)
- [Weil's quadratic form via the screw function](https://arxiv.org/abs/2606.09096)

The displayed leading-order `B_T` values in the JSON are scaling indicators,
not replacements for the paper's exact interval certificates.

### 2.5 한국어 해석

2026년 7월 결과는 고정된 `(c,N)`에서 archimedean 적분 꼬리를 다루는
중요한 진전이다. 그러나 이것만으로 prime cutoff `c`, band `N`, 전체
form domain을 동시에 제거하지는 못한다. TICKET-158은 이 차이를
`A_{c,N}`과 `B_{c,N,T}`라는 서로 다른 오차축으로 분리했다.

### 2.6 Remaining gap

```text
UniformPrimeBandRemainderOnExplicitNestedWeilCoreWithJointCutoffSchedule
```

This requires an actual nested Weil core, a uniform prime/band remainder, and
a joint `(c,N,T)` schedule. No such theorem is proved here.

---

## 3. Collatz conjecture

### 3.1 Exact proposition

For every integer `K>=6`, define

```text
A_K = (K,1,1,1,2)
B_K = (2,1,1,K,1).
```

These words have the same:

- length `m=5`;
- valuation sum `S=K+5`;
- valuation multiset;
- ordinary inversion count `3`.

Nevertheless,

```text
C(A_K) = 81 + 65*2^K
C(B_K) = 309 + 16*2^K.
```

Their common descending arrangement has

```text
C_max = 81 + 103*2^K,
```

so their exact localized inversion gains are

```text
G(A_K) = 38*2^K
G(B_K) = 87*2^K - 228.
```

With the common contracting denominator

```text
D = 2^(K+5) - 243,
```

the abstract affine word `B_K` descends at `n=1`, while `A_K` does not.

### 3.2 Proof

Insert both words into

```text
C(w) = sum_j 3^(m-j) 2^(a_1+...+a_(j-1)).
```

The closed forms follow by collecting powers of two. Subtraction from the
common descending constant gives the gain formulas. For `K>=6`,

```text
309 + 16*2^K < 2^(K+5) - 243,
```

whereas

```text
81 + 65*2^K > 2^(K+5) - 243.
```

Thus the four coarse statistics do not determine the affine descent decision.

### 3.3 Natural finite audit

For the 49,999 odd starts `3<=n<=100000`, the first-descent valuation words
produce:

| Metric | Value |
| --- | ---: |
| Coarse signatures | 3,862 |
| Signatures with multiple exact gains | 677 |
| Conjecture resolutions | 0 |

The finite collision audit confirms that the obstruction occurs in naturally
realized first-descent words, not only in the parametric abstract family.
However, this finite scan is not a proof for all starts.

### 3.4 한국어 해석

단순 inversion 개수는 “큰 valuation이 작은 valuation 뒤에 몇 번
나오는가”만 센다. 실제 gain은 각 swap의 위치와 그 앞 prefix 합에
따라 `3`과 `2`의 가중치가 달라진다. 따라서 동일한 multiset과 동일한
inversion 수를 가진 두 word도 하강 threshold가 달라질 수 있다.

이 결과는 기존 exact gain을 폐기하지 않는다. 오히려 exact gain의
위치 정보가 반드시 필요함을 증명한다.

### 3.5 Remaining gap

```text
NaturalValuationPrefixLocalizedGainCrossesAffineThresholdOnEveryRay
```

No theorem proves eventual threshold crossing for every natural valuation
ray. The parametric word family is not a divergent Collatz orbit.

---

## 4. Strong Goldbach conjecture

### 4.1 Exact proposition

For a cyclic complex sequence `w=(w_k)` of length `L`, define the trailing
moving average

```text
(A_b w)_k = (1/b) sum_{j=0}^{b-1} w_{k-j}
```

and cyclic total variation

```text
TV(w) = sum_k |w_k-w_{k-1}|.
```

Then

```text
||w-A_b w||_1 <= ((b-1)/2) TV(w).
```

Combining this with TICKET-157 gives

```text
N_-(w) <= N_-(A_b w) + ((b-1)/2) TV(w).
```

### 4.2 Proof

Expand

```text
w_k-(A_b w)_k
= (1/b) sum_{j=1}^{b-1} (w_k-w_{k-j}).
```

Each difference is bounded by the sum of its `j` adjacent cyclic increments.
Summing over `k` and `j` gives

```text
(1/b) sum_{j=1}^{b-1} j TV(w)
= ((b-1)/2) TV(w).
```

The negative-part map is one-Lipschitz, so the second inequality follows.

### 4.3 Sharpness and finite audit

For an alternating `+1,-1` sequence and `b=2`, the moving average is zero,
the residual `L1` norm is `L`, and `TV(w)=2L`. Equality holds, so the
variation constant cannot be reduced without additional arithmetic
structure.

The binary-Goldbach finite DFT audit tests endpoints `1,000` through `32,000`
and widths `2,4,8`. All 18 raw variation certificates fail. This is a
useful no-go: smoothing does not make the residual free. It transfers the
problem to an arithmetic phase-variation estimate.

### 4.4 한국어 해석

이동평균은 위상을 부드럽게 만들지만 원래 신호와의 차이를 공짜로
줄여주지 않는다. 그 비용은 total variation으로 정확히 나타나며,
교대 부호 수열은 이 비용이 날카롭다는 것을 보여준다. 실제
Goldbach minor arc에서 이 variation이 major margin보다 작다는 산술
정리는 아직 없다.

### 4.5 Remaining gap

```text
ArithmeticMinorArcPhaseVariationBelowMajorMarginWithEffectiveFiniteJoin
```

The finite variation values are observations, not uniform analytic bounds.
No even counterexample and no Goldbach proof is produced.

---

## 5. Twin Prime conjecture

### 5.1 Exact proposition

For each left/right cubic-rough population, write

```text
q_i = p_i + delta_i,
```

where `p_i` is the ambient semiprime fraction and `q_i` is the conditional
fraction after the shifted rough-pair event. Then

```text
M/R = sum_i p_i + sum_i delta_i.
```

Only positive shifts can increase this upper-bound target. Therefore

```text
M/R
<= sum_i p_i
   + sum_{delta_i>0} sqrt(I_i/(2 rho_i)).
```

This directional budget is never larger than the TICKET-157 absolute
Pinsker budget.

### 5.2 Direction-blindness no-go

Mutual information does not determine the shift sign. Set

```text
p = rho = 1/2
q_+ = 1/2 + delta
q_- = 1/2 - delta.
```

The complement conditional is `1-q`. Both tables have mutual information

```text
KL(Ber(q)||Ber(1/2)),
```

which is invariant under `q -> 1-q`, while their shifts are `+delta` and
`-delta`.

Consequently, an information-only proof cannot claim a favorable
anticorrelation sign. It must either prove the sign independently or retain a
positive-shift budget.

### 5.3 Finite audit

| Metric | Value |
| --- | ---: |
| Audited scales | 5 |
| Directional finite certificates | 5 |
| Rows with strict budget saving | 4 |
| Direction-blind counterpairs | 3 |

At `X=10,000,000`, both observed shifts are negative, so the finite
directional budget is zero and the upper ratio equals the ambient semiprime
sum. This remains a finite observation.

### 5.4 한국어 해석

조건부 semiprime 비율이 ambient 비율보다 낮으면 그 차이는 쌍둥이
소수 상계에 유리하다. 기존 절댓값 Pinsker 예산은 이 유리한 음의
편향도 손실로 계산했다. TICKET-158은 양의 편향만 비용으로 세도록
정확히 수정했다.

그러나 mutual information은 편향의 크기 정보만 제공하며 방향은
결정하지 못한다. 따라서 유한 데이터에서 관측된 음의 부호를 무한
정리로 승격해서는 안 된다.

### 5.5 Remaining gap

```text
UniformPositiveCubicRoughInformationBudgetOrSemiprimeAnticorrelationAfterEffectiveCutoff
```

One must prove either a uniform positive-shift information budget or eventual
semiprime anticorrelation. Five finite scales do not prove either statement.

---

## 6. Proof DAG summary / 증명 DAG 요약

Each track has exactly three states:

```text
refuted_or_insufficient
        |
        v
proved_exact
        |
        v
open_not_proven
```

| Problem | Rejected route | Exact result | Open theorem |
| --- | --- | --- | --- |
| RH | archimedean tail alone closes RH | two-cutoff form composition | uniform prime/band remainder with joint schedule |
| Collatz | coarse inversion count determines gain | localized gain no-go | every natural ray crosses its affine threshold |
| Goldbach | smoothing has an unpaid small residual | sharp variation proxy theorem | arithmetic minor phase-variation bound |
| Twin Prime | information determines shift sign | signed budget and direction no-go | uniform positive budget or anticorrelation |

## 7. Claim boundary / 주장 경계

English:

- no Riemann Hypothesis proof and no off-critical zero;
- no Collatz proof and no divergent orbit;
- no Goldbach proof and no even counterexample;
- no Twin Prime proof and no counterexample;
- finite computations validate only the stated finite contracts.

한국어:

- 리만 가설 증명과 임계선 밖 영점은 없다.
- 콜라츠 증명과 발산 궤도는 없다.
- 골드바흐 증명과 짝수 반례는 없다.
- 쌍둥이 소수 증명과 반례는 없다.
- 유한 계산은 명시된 유한 계약만 검증한다.

The progress in TICKET-158 is sharper target selection: one error axis is no
longer confused with another, coarse Collatz order statistics are formally
discarded, Goldbach smoothing receives its exact variation price, and Twin
information is made directional without inferring a sign it cannot contain.
