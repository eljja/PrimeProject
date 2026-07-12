# TICKET-102: Twin dyadic Vaughan holdout and threshold correction

## English

TICKET-102 converts the TICKET-101 Twin Prime observation into a scale-local falsification contract. For each dyadic horizon `X`, it fixes

```text
U(X) = round(X^(1/3)),
V(X) = round(0.84 U(X)),
```

without reading the correlation at that horizon, then audits every `x` in `(X/2,X]`. Doubling horizons make these blocks cover a complete finite tail rather than isolated checkpoints.

The registered TICKET-101 budgets do not survive selection-independent testing. At `X=2,000,000`, all 1,000,000 points in the holdout block violate the structured `K_S=1.40` budget; the maximum required constant is `1.9532`. The Type II `K_II=0.18` budget has no failures. This is a counterexample to the proposed finite envelope, not to the Twin Prime conjecture.

The failure exposes a more important logical correction. The proof does not require `K_S+K_II<=1.6`. For any fixed finite constants,

```text
structured >= -K_S M/log(x),
Type II    >= -K_II M/log(x)
```

imply

```text
C_2(x) >= M(x) (1-(K_S+K_II)/log(x)).
```

TICKET-99 gives a linear external local main up to lower-order modulus loss, while TICKET-93 bounds proper-prime-power contamination by `o(x)`. Therefore any uniform finite `K_S+K_II`, not specifically `1.6`, is asymptotically sufficient. The real open theorem is existence of horizon-independent finite constants with a noncollapsed Type II range.

After observing the failure below 4M, TICKET-102 pre-registers the coarse rescue budgets `K_S=4`, `K_II=1` and evaluates the previously unseen 8M block. All 4,000,000 points pass. The maximum structured constant is `3.3068`; the Type II contribution is nonnegative throughout the block; Type II support remains `24.31%`. This is fresh finite evidence, not a uniform theorem.

TICKET-103 correction: these endpoint correlations are cumulative from zero. Exact local-block auditing finds that Type II nonnegativity is not an identity: the block `(500,1000]` has negative Type II correlation. The large-block eventual finite-bound route remains open.

The literature boundary remains severe. Ford and Maynard show that substantial Type I/II information, used with its full geometry, is necessary in general prime-producing lower-bound sieves. Green and Tao explicitly exclude affinely related binary forms such as Twin Prime and Goldbach from their finite-complexity linear-forms theorem. PrimeProject's support-count guard only prevents decomposition collapse; it is not an analytic Type II estimate. See [Ford–Maynard](https://arxiv.org/abs/2407.14368) and [Green–Tao](https://annals.math.princeton.edu/2010/171-3/p08).

## 한국어

TICKET-102는 TICKET-101에서 고른 상수를 같은 데이터로 다시 확인하지 않습니다. 각 dyadic 규모 `X`에서 관측값과 독립적으로 `U(X),V(X)`를 정하고 `(X/2,X]`의 모든 정수를 검사합니다.

기존 구조항 상수 `1.40`은 `X=2M`에서 반박됐습니다. holdout 100만 점이 모두 실패했고 필요한 최대 상수는 `1.9532`였습니다. 이는 쌍둥이 소수 추측의 반례가 아니라 우리가 제안한 유한 부등식의 반례입니다.

또한 합이 `1.6`보다 작아야 한다는 기존 목표는 불필요하게 강했습니다. 규모와 무관한 유한 상수 `K_S,K_II`가 존재하기만 하면 `1-(K_S+K_II)/log x`가 결국 1에 가까워지고, 선형 주항이 `o(x)`인 소수거듭제곱 오염을 이깁니다. 따라서 최적화 대상은 `1.6`이 아니라 **고정된 유한 상수의 전 규모 존재성**입니다.

이 교정 후 새 8M 구간을 열기 전에 `K_S=4`, `K_II=1`을 등록했습니다. 400만 점 전부가 통과했고 Type II 지지는 `24.31%`로 유지됐습니다. 그러나 유한 검증은 무한 정리가 아니며 parity barrier를 넘는 해석적 Type II 추정도 아닙니다.

TICKET-103 교정: 이 값들은 `0..x` 누적 상관입니다. 실제 `(X/2,X]` 국소 블록에서는 `X=1000`에 음의 Type II 반례가 있으므로 전역 비음성 경로는 폐기합니다.

## Reproduce / 재현

```text
D:\python\anaconda3\python.exe scripts\ticket102_twin_dyadic_vaughan_holdout.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket102_twin_dyadic_vaughan_holdout
```
