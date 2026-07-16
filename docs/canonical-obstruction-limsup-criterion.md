# TICKET-124: Canonical Obstruction Limsup Criterion

Status: an exact necessary-and-sufficient criterion is proved for the selected canonical Vaughan budget route; the unnecessarily strong TICKET-123 modular target is retired; all four conjectures remain open.

상태: 선택한 정준 Vaughan 예산 경로 안에서 정확한 필요충분조건을 증명했고, 불필요하게 강했던 TICKET-123의 모듈형 목표를 폐기했다. 네 난제 자체는 모두 미해결이다.

## 1. Logical correction

TICKET-123 introduced three scale-dependent ratios

```text
eta_X     = D_X/S_X,
rho_X     = S_X/K_X,
epsilon_X = E_X/K_X,
```

where `K_X>0` is the independently positive comparison budget, `S_X` is the singleton budget, `D_X` is the exact canonical-pair saving, and `E_X` is the boundary-and-variation budget. It proved that compatible coordinatewise bounds are sufficient for closure.

That package is not necessary. Taking the worst value of each coordinate separately destroys compensation between the paired residual and the boundary term. A proof search that insists on the old package may therefore reject a valid joint estimate.

한국어: TICKET-123의 세 비율 상수는 충분조건이지만 필요조건이 아니었다. 스케일마다 pair 잔여항과 경계항이 서로 보상할 수 있는데, 각 좌표의 최악값을 따로 취하면 이 결합 구조가 사라진다. 따라서 세 상수를 반드시 각각 증명하려는 목표는 실제 증명보다 더 어려운 불필요한 요구였다.

## 2. Exact joint obstruction

Define

```text
Q_X = ((S_X-D_X)+E_X)/K_X
    = (1-eta_X)rho_X+epsilon_X.
```

The normalized route margin is exactly

```text
delta_X = [K_X-(S_X-D_X)-E_X]/K_X = 1-Q_X.       (1)
```

This is an identity, not an approximation. The machine audit reconstructs all eight inherited rows with maximum error `2.23e-16`.

`Q_X`는 알려진 양의 비교항 `K_X`에 비해 실제로 지불해야 하는 정준 pair 잔여 예산과 경계 예산이 얼마나 큰지를 한 숫자로 나타낸다. `Q_X<1`이면 해당 유한 스케일의 예산이 닫히고, `Q_X>=1`이면 닫히지 않는다.

## 3. Proved iff theorem

### EventualPositiveMarginIffLimsupObstructionBelowOne

For the actual budget sequence, the following statements are equivalent.

1. There are constants `delta>0` and `X_0` such that `delta_X>=delta` for every `X>=X_0`.
2. `limsup_(X->infinity) Q_X<1`.

### Forward direction

If `delta_X>=delta` eventually, equation (1) gives

```text
Q_X <= 1-delta
```

eventually. Therefore `limsup Q_X<=1-delta<1`.

### Reverse direction

Let `L=limsup Q_X<1` and choose

```text
delta = (1-L)/2 > 0.
```

By the definition of limsup, eventually

```text
Q_X <= (1+L)/2 = 1-delta.
```

Equation (1) then gives `delta_X>=delta`. This proves the equivalence.

한국어: 이 정리는 선택한 예산 경로에서 고정된 양의 여유가 충분히 큰 모든 규모에 존재하는 것과 `Q_X`의 상극한이 1보다 작은 것이 정확히 같은 조건임을 보인다. 단, 이 정리만으로 그 예산이 실제 gap-2 소수쌍의 양의 하한으로 전달된다는 해석학적 연결이나 parity barrier 극복이 증명되는 것은 아니다.

## 4. Why the old triple is not necessary

### 4.1 Alternating compensation

Alternate the two rows

```text
(eta,rho,epsilon) = (1/5,1,0),
(eta,rho,epsilon) = (1,1,4/5).
```

Every row has

```text
Q=(1-eta)rho+epsilon=4/5,
delta=1/5.
```

Thus the exact joint route closes uniformly. However, every valid coordinatewise envelope must have

```text
eta_floor <= 1/5,
rho_ceiling >= 1,
epsilon_ceiling >= 4/5,
```

so its best compatibility left side is at least

```text
(1-eta_floor)rho_ceiling+epsilon_ceiling >= 8/5 > 1.
```

No TICKET-123 compatible tuple exists. This is an exact counterexample to necessity of the old auxiliary target, not a counterexample to Twin Prime and not asserted to be Vaughan-realizable.

한국어: 홀수 스케일에서는 pair 잔여항만 0.8이고 경계항은 0, 짝수 스케일에서는 pair 잔여항은 0이고 경계항만 0.8인 경우를 생각하면 된다. 실제 합은 언제나 0.8이지만, 두 항의 최악값을 따로 더하면 1.6이 된다. 이것이 좌표별 상한이 결합 보상을 잃는 정확한 이유다.

### 4.2 Positive saving floor is not necessary

Set `K_X=1`, `S_X=1/X`, and `D_X=E_X=0`. Then `eta_X=0` at every scale, while `Q_X=1/X` tends to zero. Uniform closure can occur without any positive lower bound on `D_X/S_X` when the entire singleton ratio vanishes.

## 5. Sharp limits

### Endpoint

For `Q_n=1-1/n`, every finite row satisfies `Q_n<1`, but `limsup Q_n=1` and the margin `1/n` tends to zero. Strict inequality in the limsup theorem cannot be weakened.

### Finite prefix

After any finite prefix with `Q=1/2`, the first unseen row can have `Q=5/4`. The eight observed rows therefore cannot estimate the true limsup without an independent arithmetic tail theorem.

이 두 수열은 “모든 유한 행이 통과했다”와 “충분히 큰 모든 행에서 동일한 양의 여유가 있다”가 전혀 다른 명제임을 보여 준다.

## 6. Finite ledger

| `X` | exact `Q_X` | certified `Q_X` | exact margin | certified margin |
|---:|---:|---:|---:|---:|
| 4,096 | 1.960 | 2.102 | -0.960 | -1.102 |
| 32,768 | 2.432 | 2.562 | -1.432 | -1.562 |
| 262,144 | 1.538 | 1.616 | -0.538 | -0.616 |
| 1,048,576 | 1.278 | 1.360 | -0.278 | -0.360 |
| 2,097,152 | 1.121 | 1.173 | -0.121 | -0.173 |
| 4,194,304 | 1.001 | 1.054 | -0.0007 | -0.054 |
| 8,388,608 | 0.958 | 1.011 | +0.042 | -0.011 |
| 16,777,216 | 0.803 | 0.834 | +0.197 | +0.166 |

The last exact and certified rows close, but no trend, monotonicity, or limsup estimate follows from this finite table. The observed tail maxima displayed on GitHub Pages are diagnostics only.

마지막 행의 exact `Q`는 약 0.8027이고 certificate `Q`는 약 0.8344다. 이는 16M 한 행의 결과일 뿐, 실제 상극한이 1보다 작다는 증거로 승격하지 않는다.

## 7. Corrected next theorem

Retire as unnecessarily strong:

```text
VaughanCanonicalDefectRatioTriple
```

Retain:

```text
VaughanCanonicalObstructionLimsup
```

For the actual Vaughan-realizable budgets, prove

```text
limsup_(X->infinity) Q_X < 1,
```

or construct an unbounded Vaughan-realizable subsequence with `Q_X>=1`. The estimate must control the paired residual and boundary term jointly on dyadic blocks. Fitting the eight finite rows is not admissible.

The remaining Twin bridge is still substantial: one must prove that the asymptotic budget really lower-bounds the exact gap-two correlation and survives the parity obstruction.

## 8. Four-problem route correction

### Riemann Hypothesis

`NonCircularExplicitFormulaKernelPositivity` remains open, but it must specify an exact RH-equivalent all-test-function class and derive positivity from hypotheses independent of zero placement. Finite kernel positivity is not the infinite bridge.

리만가설: 유한 개 kernel이나 Gram matrix의 양성은 전체 test-function class를 덮지 않는다. 다음 목표는 정확한 admissible kernel class, 비순환적 positivity, density bridge를 함께 명시해야 한다.

### Collatz conjecture

`GoldenMeanInvariantSetEscape` concerns one fixed 2-adic exponent in the Mersenne-delay route. Even if proved, it would not cover every positive integer orbit. It is retained as a route-specific lemma, while the global target returns to `ResidueRankDescentCover`.

콜라츠: 황금평균 불변집합 탈출은 흥미로운 2-adic 보조문제지만 콜라츠 전체의 충분조건이 아니다. 모든 양의 정수 궤도를 덮는 residue partition과 well-founded rank가 직접 연결 목표다.

### Goldbach conjecture

`JointBalancedVaughanGoldbachResidualEnvelope` is useful only inside a theorem that also supplies an explicit positive major term, an explicit cutoff, and finite overlap below that cutoff. The finite verification through `4*10^18` cannot replace the tail theorem.

골드바흐: signed residual 제어만으로는 충분하지 않다. 상수 `K`, cutoff `N_0`, main term positivity, `N_0` 아래의 유한 검증 연결이 하나의 정리로 닫혀야 한다.

### Twin Prime conjecture

The limsup theorem is exact only for the selected canonical budget sequence. It removes an overstrong intermediate target but does not prove the arithmetic tail estimate, exact-gap transfer, or parity survival.

## 9. Literature boundary

- Connes and Consani explain Weil positivity as an RH-equivalent all-test-function condition: <https://arxiv.org/abs/1910.14368>
- Tao proves an almost-all logarithmic-density Collatz result, not universal descent: <https://arxiv.org/abs/1909.03562>
- Oliveira e Silva, Herzog, and Pardi verify even Goldbach through `4*10^18`: <https://doi.org/10.1090/S0025-5718-2013-02787-1>
- Ford and Maynard show why joint Type I/II information and extremal countermodels matter in prime-producing sieves: <https://arxiv.org/abs/2407.14368>

## 10. Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket124_canonical_obstruction_limsup_criterion.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket124_canonical_obstruction_limsup_criterion
```

## 11. Claim boundary

TICKET-124 proves an exact iff theorem for one normalized budget route and exact countermodels to necessity of the prior modular package. It does not prove or refute the Riemann Hypothesis, Collatz conjecture, Goldbach conjecture, or Twin Prime conjecture.

TICKET-124는 증명 목표를 더 약하고 정확한 필요충분조건으로 교정했다. 이것은 실제 진전이지만 네 난제의 증명 또는 반례는 아니다.
