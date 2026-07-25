# TICKET-141: One-Sided Spectra, Moving Floors, Robust Duals, and Large Sieve

Date: 2026-07-30

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket141-one-sided-moving-floor-robust-dual-large-sieve.json`

> Superseded target notice / 후속 목표 교정: TICKET-142 proves that the
> Collatz product window gives an upper, not lower, bound on a hypothetical
> cycle minimum; it also replaces three underspecified or circular next
> targets with typed effective-rank, Haar, and Liouville ledgers. See
> [TICKET-142](effective-rank-cycle-direction-haar-liouville.md). The exact
> TICKET-141 theorems below remain valid, but its proposed next targets are
> historical rather than current.

## Publication boundary / 논문 제출용 경계

**English.** TICKET-141 proves three elementary exact theorems and one exact
corollary of the classical analytic large sieve. It makes no literature-priority
claim. It does not prove or refute the Riemann Hypothesis, Collatz conjecture,
strong Goldbach conjecture, or Twin Prime conjecture. The finite tables replay
the formulas and stress numerical implementations; they do not promote a finite
calculation to a universal proof.

**한국어.** TICKET-141은 세 개의 기본적 정확 정리와 고전적 analytic
large sieve의 정확한 따름정리 하나를 확정한다. 학계 최초성을 주장하지
않으며 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중
어느 것도 증명하거나 반증하지 않는다. 유한 표는 공식을 재생하고 구현을
검사할 뿐, 유한 계산을 무한 명제의 증명으로 승격하지 않는다.

## Result table / 결과표

| Problem / 문제 | Exact result / 정확 결과 | Discarded route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `ShiftedTraceMomentOneSidedCertificateAndSignBlindnessNoGo` | unshifted even moments as a complete positivity decision | `ProjectedWeilShiftedLogMomentBelowTailGap` |
| Collatz / 콜라츠 | `PeriodDependentFloorLinearGrowthBarrier` | subcritical-linear minimum floors in the relaxed window | `CycleMinimumAboveExactPowerOfTwoWindowThreshold` |
| Goldbach / 골드바흐 | `PowerOfTwoRawMomentDualQuadraticExponentialConditioningNoGo` | high-order raw monomial moments as a robust pointwise certificate | `LocalizedOrthogonalArithmeticK56DualCertificate` |
| Twin Prime / 쌍둥이 소수 | `QuadraticIrrationalBilinearLargeSieveCancellation` | one fixed irrational phase as an exact-gap-two lower bound | `UniformMinorArcVaughanBilinearCancellationWithPositiveTwinMass` |

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `E` be self-adjoint, `lambda_max(E)<=R`, and `A>=gI`. For every integer
`m>=1`,

```text
tr((RI-E)^(2m)) < (R+g)^(2m)
```

implies `A+E>0`.

However, unshifted even moments cannot completely decide positivity. For
`c>g`, the matrices `E_+=cI` and `E_-=-cI` satisfy

```text
tr(E_+^(2m)) = tr(E_-^(2m))
```

for every `m`, while `gI+E_+>0` and `gI+E_-` is not positive.

한국어로, 이동된 행렬 `RI-E`의 짝수 moment는 `E`의 음의 spectral
edge를 본다. 반면 이동하지 않은 짝수 moment는 `E`와 `-E`를 구별하지
못하므로 positivity의 필요충분 판정기가 될 수 없다.

### Proof / 증명

`F=RI-E`의 고유값은 `R-lambda_i(E)`이고 모두 음이 아니다. 따라서

```text
rho(F)^(2m) <= tr(F^(2m)).
```

선언한 strict inequality에서

```text
R-lambda_min(E)=rho(F)<R+g
```

이므로 `lambda_min(E)>-g`다. Weyl 하계로

```text
lambda_min(A+E) >= g+lambda_min(E)>0.
```

부호 맹목성 반례는 `E=+cI,-cI`를 직접 대입하면 된다. `QED`

### Reproducible audit / 재현 계산

`g=1`, `c=R=6/5`와 rank `4,16,64,256,1024,4096`을 사용했다.
두 family의 unshifted even trace는 정확히 같지만, positive spike의 shifted
trace는 0이고 negative spike는 threshold 이상이다. 행 수는 6이고 exact
check failure는 0이다.

### No-go and remaining gap / 폐기 경로와 남은 간극

폐기되는 것은 “unshifted even moments만으로 positivity를 완전히
판정한다”는 경로다. TICKET-140의 충분조건 자체는 여전히 참이다.
실제 projected Weil operator에 대한 `lambda_max(E)<=R`, shifted
log-order moment 상계, 양의 tail gap은 모두 미증명이다.

다음 단일 보조정리:
`ProjectedWeilShiftedLogMomentBelowTailGap`.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

가상 양의 `k`-cycle의 최솟값에 대한 하한을 `M_k>=1`이라 하자.
TICKET-139의 완화 product window 상단은

```text
U_k=(1+1/(3M_k))^k.
```

또한

```text
q_k=2^ceil(k log_2 3)/3^k
```

는 항상 `1<q_k<2`다. 따라서 `U_k>=2`이면 이 필요조건은 `q_k`를
자동으로 허용한다. 이 자동 무력화를 피하기 위한 필요조건은 정확히

```text
M_k > 1/(3(2^(1/k)-1)).
```

임계값을 `k`로 나눈 극한은

```text
1/(3 log 2) = 0.480898...
```

이다.

### Proof / 증명

`log_2 3`의 무리성 때문에 `q_k`는 1과 2 사이에 있다. `U_k>=2`이면
`q_k<=U_k`이므로 완화 창으로는 해당 valuation sum을 배제하지 못한다.
`M`에 대한 `U_k`의 단조 감소를 사용하면 `U_k<2`와 선언한 threshold가
동치다. 마지막 극한은

```text
k(2^(1/k)-1) -> log 2
```

에서 바로 얻는다. `QED`

### Exact integer replay / 정확 정수 재생

`(3M+1)^k < 2(3M)^k`를 큰 정수로 직접 비교했다.

| period `k` | minimum integer `M` making `U_k<2` | `M/k` |
|---:|---:|---:|
| 16 | 8 | 0.500000 |
| 64 | 31 | 0.484375 |
| 256 | 123 | 0.480469 |
| 1,024 | 493 | 0.481445 |
| 4,096 | 1,970 | 0.480957 |
| 16,384 | 7,879 | 0.480896 |

각 행은 해당 `M`에서 strict inequality가 성립하고 `M-1`에서는
실패함을 exact integer arithmetic으로 확인한다.

### No-go and remaining gap / 폐기 경로와 남은 간극

이는 cycle을 만들지도, cycle이 없음을 증명하지도 않는다. 정확한 결론은
기울기가 `1/(3 log 2)`보다 작은 period-dependent floor가 이 완화 창에서
결국 무력해진다는 것이다. 실제 배제에는 `q_k` 자체에 맞춘 더 강한
cycle-minimum 하한이 필요하다. 비주기 발산 궤도도 별도 문제로 남는다.

다음 단일 보조정리:
`CycleMinimumAboveExactPowerOfTwoWindowThreshold`.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

`q+1`개의 정규화된 거듭제곱 2 점

```text
x_i=2^(i-q), 0<=i<=q
```

에서 0차부터 `q`차 raw moment로 첫 좌표를 추정하는 Lagrange dual을
`lambda`라 하자. 최고차 계수의 절댓값은

```text
2^(q^2) / product_(j=1)^q (2^j-1)
```

이고, 따라서

```text
||lambda||_1 > 2^(q(q-1)/2).
```

각 moment의 독립 오차가 `epsilon` 이하이면 최악의 첫 좌표 추정 오차는
정확히 `epsilon||lambda||_1`이다.

### Proof / 증명

첫 Lagrange basis polynomial은

```text
L_0(x)=product_(j=1)^q (x-x_j)/(x_0-x_j).
```

`x_j-x_0=(2^j-1)/2^q`이므로 최고차 계수 공식이 나온다.
각 `2^j-1`을 더 큰 `2^j`로 바꾸면

```text
2^(q^2-q(q+1)/2)=2^(q(q-1)/2)
```

보다 strict하게 크다는 하계가 나온다. dual 계수의 부호에 맞춰 moment
오차를 택하면 triangle inequality의 상계가 정확히 달성된다. `QED`

### Reproducible audit / 재현 계산

`q=2,4,6,8,10,12,16,56`에서 exact rational interpolation, 닫힌식,
`l1` 하계와 adversarial error equality를 재생했다. `q=56`은 원시
moment 차수이며 Goldbach cutoff 기호 `K=56`과 동일한 수학적 객체가
아니다. 이 stress row에서 증폭 하계 지수는

```text
q(q-1)/2 = 1540.
```

### No-go and remaining gap / 폐기 경로와 남은 간극

이 dual과 null vector는 실제 Goldbach residual이 아니다. 폐기되는 것은
power-of-two hard stratum에서 고차 raw monomial moments를 안정적인
점별 인증으로 쓰는 좌표계다. localized 또는 orthogonal 측정으로 바꾸고,
그 dual norm이 이미 확정된 산술적 `K=56` margin 안에 들어감을 증명해야
한다.

다음 단일 보조정리:
`LocalizedOrthogonalArithmeticK56DualCertificate`.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

임의의 복소 계수 `a_1,...,a_M`, `b_1,...,b_N`에 대해

```text
|sum_(m<=M,n<=N) a_m b_n e(sqrt(2)mn)|
  <= sqrt(M+4N)||a||_2||b||_2.
```

`|a_m|,|b_n|<=1`이면 자명한 `MN` 상계에 대한 비율은

```text
sqrt(1/N+4/M)
```

이하이고, `M=N=L`이면 `sqrt(5/L)`이다.

### Proof / 증명

`x_n={n sqrt(2)}`라 하자. `1<=|h|<N`에 대해 TICKET-140의 이차무리수
하계가

```text
||h sqrt(2)||>1/(4|h|)>1/(4N)
```

을 준다. 따라서 점들은 `delta>1/(4N)`로 분리된다. well-spaced points에
대한 analytic large sieve를 적용하면

```text
sum_(m<=M)|sum_(n<=N)b_n e(mx_n)|^2
  <= (M-1+delta^(-1))||b||_2^2
  < (M+4N)||b||_2^2.
```

마지막으로 `m`에 Cauchy-Schwarz를 적용하면 선언 명제를 얻는다. `QED`

사용한 표준 입력은 Montgomery와 Vaughan의 analytic large sieve다.
이 논문은 PrimeProject 결과의 최초성 근거가 아니라 표준 정리의 출처다:
[Montgomery–Vaughan, *The large sieve*, Mathematika 20 (1973),
119–134](https://doi.org/10.1112/S0025579300004708).

### Reproducible diagnostic / 재현 진단

`M=N=8,16,32,64,128` phase matrix에 deterministic power iteration을
적용했다. 마지막 행에서 관측 operator norm squared는 약 `205.751`,
이론 상계는 `640`이다. 이 수치 계산은 large-sieve 정리의 증명이 아니라
구현과 위상 행렬을 검사하는 진단이다.

### No-go and remaining gap / 폐기 경로와 남은 간극

TICKET-140의 비가중 회전합보다 강한 쌍선형 상쇄를 얻었지만 위상은
`sqrt(2)` 하나뿐이다. 실제 twin-prime 공격에는 필요한 모든 minor arc,
Vaughan 또는 Mobius 계수, smoothing과 cutoff, signed main-term transport,
양의 exact-gap-two 질량이 동시에 필요하다. 이 정리는 sieve parity
obstruction을 해결하지 않는다.

다음 단일 보조정리:
`UniformMinorArcVaughanBilinearCancellationWithPositiveTwinMass`.

## Cross-problem conclusion / 문제 간 결론

**English.** TICKET-141 adds directional and robustness requirements. RH needs
a one-sided shifted spectral estimate, Collatz needs a minimum floor that tracks
the exact Diophantine window, Goldbach needs a well-conditioned arithmetic dual,
and Twin Prime needs uniform arithmetic minor-arc transport. None of these
problem-specific infinite inputs has been proved.

**한국어.** TICKET-141의 공통 결론은 단순한 “더 큰 계산”이 아니라 방향성과
강건성이다. RH는 단측 이동 spectral 추정, 콜라츠는 정확한 Diophantine
창을 따라가는 최솟값 하한, 골드바흐는 조건수가 통제된 산술 dual,
쌍둥이 소수는 모든 필요한 minor arc에 대한 산술적 전달 정리가 필요하다.
이 네 무한 입력은 아직 어느 것도 증명되지 않았다.

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket141_one_sided_moving_floor_robust_dual_large_sieve.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket141_one_sided_moving_floor_robust_dual_large_sieve
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

Expected machine summary:

```text
exact theorem count: 4
route correction count: 4
proof DAG count: 4
conjecture resolution count: 0
total failure count: 0
```
