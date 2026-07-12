# TICKET-95: Sharp contamination budgets and the equivalence gate

## Status

TICKET-95 proves sharper proper-prime-power contamination bounds for the Twin Prime and binary Goldbach correlation bridges. It also corrects the progress ledger: the TICKET-94 signed-remainder target is algebraically equivalent to the original Twin correlation target, so the decomposition is not by itself a reduction of the open problem. No conjecture is solved.

한국어: TICKET-95는 기존 연구를 폐기하지 않고 논리적 강도를 다시 분류한다. 정확한 항등식은 유효하지만, 미해결 명제를 다른 기호로 다시 쓴 것만으로는 증명 진전이 아니다. 반면 소수 거듭제곱 오염 상계는 실제로 더 작고 엄밀한 상계로 개선한다.

## Weighted proper-prime-power mass

Define

```text
H(y) = sum_{m<=y, m=p^k, k>=2} Lambda(m).
```

Unlike the old bound, `H(y)` counts the actual von Mangoldt mass rather than charging `sqrt(y)` possible values for every exponent.

For Twin Prime,

```text
E_pp(x) <= log(x+2) (H(x)+H(x+2)) = B_#(x).
```

For Goldbach,

```text
E_pp(N) <= 2 log(N) H(N) = B_#G(N).
```

Both follow by charging every contaminated term to a proper-prime-power endpoint and bounding the opposite `Lambda` factor by the relevant logarithm.

한국어: 이전 상계는 가능한 지수마다 `sqrt(N)`개의 후보가 있다고 세어 지나치게 컸다. 새 상계는 실제 proper prime power가 가진 `Lambda` 가중 질량만 누적한다. 이는 계산 편법이 아니라 모든 항을 덮는 엄밀한 union bound다.

## Twin Prime: equivalence is not reduction

TICKET-94 writes

```text
C_2 = alpha_R^2 S_R + D_R.
```

Therefore

```text
D_R >= -alpha_R^2 S_R + B_# + omega
```

is exactly equivalent to

```text
C_2 >= B_# + omega.
```

The reformulation is valid and may still guide an independent Type II estimate, but it cannot be counted as a weaker theorem or a proof bridge without such an estimate. TICKET-95 removes that overstatement.

한국어: `D_R` 하한은 틀린 명제가 아니라 원래 `C_2` 하한과 같은 명제다. 따라서 새로운 정보가 추가된 것이 아니다. 다음 단계는 `C_2`의 실제 값을 입력으로 사용하지 않는 독립적인 부호 상쇄 정리여야 한다.

Next target:

```text
IndependentShiftTwoCorrelationExcess.
```

## Goldbach: improved finite screen

At `N=100, 1,000, 10,000, 100,000, 1,000,000`, the new bound is smaller than the old envelope and the exact checkpoint correlation has a positive sharp margin. A double-precision FFT screen over every even `N<=1,000,000` finds ten nonpositive criterion margins, all at `N<=38`; each has a direct Goldbach witness. The observed criterion margin is positive for every screened even `N>=40`.

This is not an interval-arithmetic or symbolic proof. FFT values are directly recomputed at every nonpositive case, at the minimum positive case, and at scale checkpoints. The infinite theorem remains:

```text
UniformBinaryMinorArcDominance:
M(N) - |R(N)| > 2 log(N) H(N)
```

for every sufficiently large even `N`, with an explicit finite cutoff.

한국어: 백만 이하 전 구간 화면은 강한 유한 증거지만 무한 증명이 아니다. 특히 부동소수점 FFT를 정리로 승격하지 않는다. 필요한 것은 major arc 주항이 minor arc 오차와 새 오염 상계를 모든 큰 짝수에서 동시에 이긴다는 균일 정리다.

## Four-problem boundary

- Riemann Hypothesis: only the independent-information gate is transferred; no new zero estimate is proved.
- Collatz: only the independent-information gate is transferred; no transition-complete drift theorem is proved.
- Goldbach: the contamination theorem is improved; the uniform lower bound remains open.
- Twin Prime: the contamination theorem is improved and an equivalent reformulation is downgraded; the parity-breaking lower bound remains open.

## Research context and novelty boundary

- Maynard's bounded-gap sieve proves bounded prime gaps but does not isolate exact gap 2: [Small gaps between primes](https://annals.math.princeton.edu/2015/181-1/p07).
- Ford and Maynard's prime-producing sieve framework identifies substantial Type I/II information as necessary for general nontrivial prime lower bounds: [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).
- Helfgott's ternary Goldbach work demonstrates the power of explicit circle-method budgets, but it does not provide the binary uniform minor-arc inequality required here: [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438).

The candidate PrimeProject contribution in TICKET-95 is the endpoint-weighted contamination contract, its machine-audited integration, and the explicit equivalence/no-reduction gate. Established sieve, circle-method, and von Mangoldt-correlation theory are background, not claimed as new.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket95_sharp_contamination_and_equivalence_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket95_sharp_contamination_and_equivalence_audit
```
