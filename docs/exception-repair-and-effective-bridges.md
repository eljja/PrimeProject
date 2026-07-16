# TICKET-127: Exception Repair and Effective Proof Bridges

## 연구 상태 / Research status

**리만 가설, Collatz 추측, 강한 Goldbach 추측, 쌍둥이 소수 추측은 모두
미해결이다.** 이 문서는 네 추측의 증명이나 반례를 주장하지 않는다.
TICKET-127은 이전 경로의 논리 오류 하나를 공개적으로 교정하고, 유한 계산을
실제 증명 또는 반례 탐색과 연결하는 정확한 중간정리 네 개를 확립한다.

**RH, Collatz, strong Goldbach, and Twin Prime all remain open.** This report
claims neither a proof nor a counterexample to any of them. TICKET-127 records
one public logical correction and proves four exact intermediate bridge
theorems that define what finite computation can and cannot establish.

Machine-readable record:
`data/open-problem/ticket127-exception-repair-effective-bridges.json`.

## 1. 결과 요약 / Result matrix

| 문제 | 이번에 정확히 확립한 것 | 폐기한 해석 | 다음 결정적 전제 |
|---|---|---|---|
| RH | 조밀한 열거 가능 핵심집합에서 음의 Weil 값 탐색은 조건부 반결정 절차 | 유한 비발견을 RH 증명으로 승격 | 구간 인증 가능한 조밀 Weil 핵심집합과 계산기 |
| Collatz | `n>1` 유한 하강 반례와 비자명 결국-low 경로의 동치 | `n=1` 경로까지 배제하는 불가능한 목표 | 비자명 결국-low 경로의 균일 배제 |
| Goldbach | 이항 Goldbach 특이급수 `S(N)>=1`, 정확한 정규화에서 `A=1` | 특이급수 계수를 미지의 적합 상수로 취급 | 명시적 점별 잔차 상수 `K<42.83274372223497` |
| Twin Prime | 정규화 점화식과 원시 Vaughan 예산 운송 부등식의 동치 | 다섯 유한 전이에서 균일 꼬리 점화식 추론 | 균일 원시 예산 운송, 전 구간 보간, parity 돌파 |

Every theorem below is separated from its unresolved premise. A zero in the
conjecture-resolution counter is intentional, not a missing result.

## 2. RH: 완전한 반례 탐색의 조건 / Effective RH counterexample search

부호를 고정한 RH-동치 Weil 판정식을 다음처럼 쓴다.

```text
RH  iff  Q(g) >= 0 for every admissible g in V.
```

여기서 `V`는 완비된 허용 시험함수 공간, `Q`는 연속 이차형식이라고 하자.
`D={d_0,d_1,...}`가 `V` 안에서 조밀하고 명시적으로 열거 가능하다고 가정한다.

### Theorem RH-127: `DenseCoreNegativeWitnessSemidecision`

`Q(g)<0`인 허용 함수가 하나라도 존재하면 `Q(d_j)<0`인 핵심 원소가 존재한다.
또한 모든 엄격한 음수 값에 대해 결국 음의 상계를 반환하는 구간 계산기가
있다면, `D`의 병렬 열거는 Weil 판정식 반례를 반결정한다.

### 증명 / Proof

연속성 때문에 `Q^{-1}((-infinity,0))`는 열린집합이다. 음의 증인 `g`를
포함하는 열린 근방 전체가 음의 영역 안에 들어간다. `D`의 조밀성으로 그
근방 안에 어떤 `d_j`가 존재한다. 엄격한 음수에 대해 완전한 구간 계산기는
유한 시간 후 상단 끝점이 0보다 작은 구간을 반환한다. 따라서 모든 계산을
병렬화하면 실제 반례가 있을 때 반드시 정지한다. `QED`

이 정리는 **반례가 없을 때 정지한다고 말하지 않는다.** 유한 개 원소에서
음수를 찾지 못한 사실은 RH 증명이 아니다. 또한 다음 세 전제는 아직
PrimeProject에서 증명되지 않았다.

1. 사용한 판정식과 RH의 정확한 동치 및 부호 규약
2. 완비 허용공간 안의 열거 가능 조밀 핵심집합
3. 모든 엄격한 음수 핵심값에 완전한 검증 구간 계산기

```text
Next: IntervalCertifiedWeilCoreEvaluator
다음: 구간 인증 가능한 Weil 핵심집합 계산기
```

## 3. Collatz: `n=1` 예외의 공개 교정

가속 홀수 사상은

```text
T_odd(n) = (3n+1) / 2^v2(3n+1)
```

이다. TICKET-126의 경로 동치 정리 자체는 `n=1`을 포함해 정확하다. 그러나
초기 보고서의 따름정리는 “결국-low 경로가 전혀 없어야 한다”고 적어
`n>1` 조건을 누락했다. `n=1`은 자기 자신보다 작은 엄격한 반복값이 없고,
모든 정밀도의 미해결 트리에 남으며, 매번 low 자식을 선택한다. 따라서
기존의 `UniformEventuallyLowPathExclusion` 목표는 애초에 성립할 수 없다.

### Theorem CO-127: `NontrivialEventuallyLowPathIffFiniteStoppingCounterexample`

양의 홀수 `n>1`에 대해 다음 두 명제는 동치다.

1. `n`의 유한 반복 중 `n`보다 작은 값이 없다.
2. `n`의 호환 잉여류 경로는 적응형 미해결 트리의 비자명 결국-low 무한
   경로다.

TICKET-126의 정확한 경로 동치를 `n>1`에 제한하고, TICKET-125의 강한 귀납
유한하강 정리와 결합하면 바로 얻어진다. 따라서 올바른 전역 동치는

```text
Collatz
iff every n>1 has finite strict descent
iff no nontrivial eventually-low path survives.
```

### 28비트 정확 감사 / Exact 28-bit audit

| 항목 | 값 |
|---|---:|
| 홀수 잉여류 전체 | 134,217,728 |
| 미해결 전체 | 4,027,110 |
| 알려진 고정 경로 `n=1` | 1 |
| 비자명 미해결 | 4,027,109 |
| 전체 최장 low 연속 길이 | 24 (`n=1`) |
| 비자명 최장 low 연속 길이 | 23 |
| 비자명 최장 증인 | `27`, `31` |

이는 유한 영역의 정확한 분류일 뿐이다. `27`, `31`은 Collatz 반례가 아니라
28비트 인증기가 아직 닫지 못한 긴 경로 증인이다.

```text
Next: UniformNontrivialEventuallyLowPathExclusion
다음: 비자명 결국-low 경로의 균일 배제
```

## 4. Goldbach: 특이급수 하한과 남은 잔차

짝수 `N`의 표준 이항 Goldbach 특이급수를

```text
S(N) = 2 C2 product_{p|N, p>2} (p-1)/(p-2),
C2   = product_{p>2} (1 - 1/(p-1)^2)
```

로 둔다. 가중 합과 정확한 잔차는

```text
G(N) = sum_{m=1}^{N-1} Lambda(m)Lambda(N-m),
R(N) = G(N) - S(N)N
```

로 정의한다. 이 `R` 정의는 항등식이며 근사 가정이 아니다.

### Theorem GB-127: `UniformBinaryGoldbachSingularSeriesLowerBound`

모든 양의 짝수 `N`에 대해 `S(N)>=1`이다.

### 증명 / Proof

모든 보정인자 `(p-1)/(p-2)`는 1 이상이다. 한편 `M>=2`에 대해
`C2`의 `p-1<=M` 소수 인덱스 인자들은 `2<=m<=M`인 인자
`1-1/m^2`의 부분집합이다. 모든 인자가 `(0,1)`에 있으므로 부분집합의 곱은
전체 곱보다 작지 않다. 전체 곱은 망원곱으로

```text
product_{m=2}^M (1-1/m^2) = (M+1)/(2M) > 1/2.
```

소수 부분곱의 수렴하는 감소 극한을 취하면 `C2>=1/2`, 따라서
`S(N)>=2*(1/2)=1`이다. `QED`

그 결과 정확히

```text
G(N) = S(N)N + R(N) >= N - |R(N)|.
```

즉 TICKET-125의 정규화된 주항 계수 `A=1`은 구조적으로 닫힌다. 그러나 이는
원 방법이 “주항을 근사했다”는 주장이 아니다. 모든 해석적 어려움은 이제
명시적으로 `R(N)`에 남는다. TICKET-126의 소수 거듭제곱 오염 상수와
`H=4e18` 유한 검증을 결합하려면 아직 다음 점별 정리가 필요하다.

```text
|R(N)| <= K N/log N for every even N>H,
K < 42.83274372223497.
```

평균값 상계, 거의 모든 `N`에 대한 상계, 수치 적합은 이 전칭 점별 전제를
대체하지 못한다.

```text
Next: ExplicitPointwiseBinaryGoldbachResidualConstant
다음: 명시적 점별 이항 Goldbach 잔차 상수
```

## 5. Twin Prime: 정규화 그래프를 원시 계수 계약으로 환원

유한 Vaughan 감사에서 양의 기준 예산을 `K_X>0`, 인증 후 남는 불리한 원시
분자를 `A_X>=0`, 정규화 장애량을 `Q_X=A_X/K_X`로 둔다.

### Theorem TP-127: `RawBudgetTransportIffNormalizedAffineContraction`

`K_X,K_2X>0`일 때

```text
Q_2X <= alpha Q_X + beta
```

와

```text
A_2X <= alpha (K_2X/K_X) A_X + beta K_2X
```

는 동치다. 첫 부등식에 양수 `K_2X`를 곱하고 `Q=A/K`를 대입하면 되며,
역방향은 `K_2X`로 나누면 된다.

추가로 `A_2X<=u A_X+v K_2X`, `K_2X>=gamma K_X`,
`K_X>0`, `A_X,u>=0`, `gamma>0`이면

```text
Q_2X <= (u/gamma) Q_X + v.
```

따라서 다음 공격 대상은 정규화 산점도의 모양이 아니라 실제 계수에서
`u`, `gamma`, `v`를 균일하게 얻는 정리다.

### 사전등록 16M -> 32M 원시 감사

| 항목 | 값 |
|---|---:|
| 기준 예산 성장 `gamma` | 2.0115420952456007 |
| 불리한 분자 성장 `u` | 1.8603305083667954 |
| 인증 정규화 잔차 | 0.1458729009339482 |
| paired 기여 | 0.1413515108429004 |
| boundary 기여 | 0.004521390091047683 |
| 원시 운송 여유 | 1,268,424.8319815714 |

잔차 분해는 정확한 항등식 감사다. 다섯 개 유한 전이가 균일 꼬리 부등식을
증명하지 않으며, dyadic 점화식만으로 모든 `X`를 덮지도 않는다. 더구나 이
계약이 성립해도 정확한 간격 2의 양의 하한으로 연결하려면 parity 장벽을
넘는 별도 정리가 필요하다.

```text
Next: UniformVaughanRawBudgetTransportAndInterpolation
다음: 균일 Vaughan 원시 예산 운송 및 전 구간 보간
```

## 6. 재현 / Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket126_route_correction_audit.py
D:\python\anaconda3\python.exe scripts\ticket127_exception_repair_effective_bridges.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket126_route_correction_audit tests.test_ticket127_exception_repair_effective_bridges
node scripts\verify_pages.cjs
```

The aggregate JSON records zero conjecture resolutions and fails generation if
any exact identity audit fails.

## 7. 문헌 경계 / Literature boundary

- A. Connes and C. Consani, [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368). Primary Weil-autocorrelation criterion context; no RH result is imported.
- T. Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562). Primary almost-all result; it does not establish the universal `n>1` target.
- J. B. Friedlander, D. A. Goldston, H. Iwaniec, and A. I. Suriajaya, [Exceptional zeros and the Goldbach problem](https://doi.org/10.1016/j.jnt.2021.06.004). Primary binary Goldbach singular-series normalization.
- K. Ford and J. Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368). Primary sieve context; no exact-gap parity theorem is imported.

These references establish definitions and known boundaries. The elementary
lower bound, exception repair, semidecision lemma, and raw-transport identity
are proved and machine-audited locally.
