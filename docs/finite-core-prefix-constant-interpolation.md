# TICKET-128: Finite Core, Prefix Closure, Constant Sharpening, and Interpolation

## 연구 상태 / Research status

**리만 가설, Collatz 추측, 강한 Goldbach 추측, 쌍둥이 소수 추측은 모두
미해결이다.** TICKET-128은 네 추측의 증명이나 반례를 주장하지 않는다.
목표는 TICKET-127이 남긴 전제를 실제로 줄이고, 유한 계산이 말하는 범위를
더 정확히 분리하는 것이다.

**RH, Collatz, strong Goldbach, and Twin Prime all remain open.** TICKET-128
claims neither a proof nor a counterexample to any conjecture. It proves four
intermediate results: one effective finite-sum reduction, one finite-prefix
closure, one rigorous constant improvement, and one interpolation no-go plus
repair theorem.

Machine-readable record:
`data/open-problem/ticket128-finite-core-prefix-constant-interpolation.json`.

## 1. 결과 요약 / Result matrix

| 문제 | TICKET-128에서 확립한 것 | 폐기하거나 교정한 해석 | 다음 미증명 정리 |
|---|---|---|---|
| RH | compact support 시험함수의 소수항을 `p^m<=B`인 유한 합으로 정확히 환원 | 무한 소수합을 임의 절단해 정확한 Weil 값으로 취급 | archimedean 구간 인증과 허용 핵심집합 조밀성 |
| Collatz | 28비트 미해결 원통 대표 4,027,109개를 직접 하강 인증 | 미해결 원통 대표를 실제 정수 반례 후보로 동일시 | 무한 prefix 폐쇄 또는 균일 well-founded rank |
| Goldbach | `2C2>1.31917`의 유리수 인증과 충분조건 `K=55` | 최종 주항 상수를 불필요하게 `A=1`로 고정 | 점별 잔차 `|R(N)|<=55N/log N` |
| Twin Prime | dyadic endpoint-only 추론의 명시적 반례와 all-scale envelope 정리 | endpoint 값 사이를 전제 없이 보간 | 실제 Vaughan 계수에서 `c=1`, `delta<0.08` |

모든 유한 결과는 정확한 bounded certificate이다. 어느 행도 무한 명제를
유한 계산만으로 닫지 않는다.

## 2. RH: compact support가 닫는 소수항

RH와 동치인 Weil explicit formula의 산술항이 소수 거듭제곱 `p^m`에 대해
`h(m log p)`를 포함한다고 하자. 정수 `B>=2`에 대해

```text
h(t)=0 whenever |t|>log B
```

인 compact-support 시험함수를 사용한다.

### Theorem RH-128: `CompactSupportFinitePrimeSideReduction`

산술항에서 0이 아닌 모든 항은 정확히

```text
m log p <= log B  iff  p^m <= B
```

를 만족한다. 따라서 소수항은 인증 가능한 유한 목록으로 환원된다.

### 증명 / Proof

`log`의 단조성으로 `p^m>B`이면 `m log p>log B`이고 해당 함수값은 0이다.
`B` 이하의 정수는 유한하므로 남는 `(p,m)` 쌍은 체 또는 인증된 소인수분해로
완전히 열거할 수 있다. `QED`

`B=1,000,000` 감사 결과는 다음과 같다.

| 항목 | 값 |
|---|---:|
| 소수 | 78,498 |
| 소수 거듭제곱 항 `(p,m)` | 78,734 |
| 최대 지수 | 19 |

이 결과는 TICKET-127의 interval evaluator 전제를 한 단계 줄인다. compact
support 핵심 원소에서는 **무한 소수 꼬리가 더 이상 없다.** 그러나 다음은
여전히 열려 있다.

1. 사용한 시험함수 핵심집합이 정확한 허용공간에서 조밀하다는 증명
2. archimedean 항과 함수값의 엄밀 구간 계산
3. Weil 기준의 정규화와 부호 규약
4. 모든 핵심 원소의 양성, 또는 실제 음의 반례 증인

```text
Next: ArchimedeanIntervalAndAdmissibleCoreDensity
다음: Archimedean 구간 인증 및 허용 핵심집합 조밀성
```

유한 핵심 원소에서 음수가 발견되면 후보 반례를 재생할 수 있다. 유한
비발견은 RH 증명이 아니다.

## 3. Collatz: 원통 미해결과 정수 미해결의 분리

TICKET-127의 4,027,109개는 28비트 adaptive certificate가 모든 lift를 한 번에
닫지 못한 **원통 대표**였다. 이것을 실제 Collatz 반례 후보 수로 읽으면
안 된다. 한 원통 전체에 대한 공통 증명이 실패해도 그 최소 대표 정수의
실제 궤도는 유한 시간에 하강할 수 있다.

### Theorem CO-128: `FinitePrefixEventuallyLowExclusion`

정밀도 `k`에서 모든 미해결 홀수 대표 `1<n<2^k`가 유한 strict descent를
가지면, `2^k` 아래에서 안정화되는 비자명 eventually-low 경로는 Collatz
반례를 부호화하지 못한다.

### 증명 / Proof

eventually-low 이진 잉여류 경로는 high refinement를 유한 번만 가지므로 한
양의 홀수 `n`에서 안정화된다. `n<2^k`이면 level `k`의 대표도 `n`이다.
adaptive frontier 밖의 대표는 원통 인증서가 닫고, frontier 안의 대표는
직접 strict-descent 인증서가 닫는다. 짝수는 즉시 더 작은 홀수 부분으로
내려간다. `QED`

### 28비트 정확 감사 / Exact 28-bit audit

| 항목 | 값 |
|---|---:|
| adaptive 미해결 원통 | 4,027,110 |
| 고정 `n=1` 경로 | 1 |
| 직접 검사한 비자명 대표 | 4,027,109 |
| strict descent 인증 | 4,027,109 |
| 단계 제한 생존자 | 0 |
| 최대 가속 단계 | 249 |
| 최대 단계 증인 | 217,740,015 |
| 최대 peak | 2,134,932,387,040,421 |
| 최대 peak 시작값 | 210,964,383 |

따라서 로컬 인증 체계 안에서 모든 `n<2^28`은 하강한다. 이 범위는 알려진
외부 계산 기록과 경쟁하기 위한 것이 아니라, adaptive 원통 의미를 바로잡고
두 인증 방식을 정확히 결합하기 위한 것이다.

무한 결론에는 여전히 다음 중 하나가 필요하다.

```text
1. 모든 k를 덮는 unbounded prefix closure theorem
2. 모든 비자명 eventually-low path를 배제하는 well-founded rank
3. 실제 단계 제한 생존자 또는 재생 가능한 cycle/divergence witness
```

```text
Next: UnboundedPrefixClosureOrUniformNontrivialPathRank
다음: 무한 prefix 폐쇄 또는 비자명 경로의 균일 순위함수
```

## 4. Goldbach: 특이급수 하한의 강화

쌍둥이 소수 상수형 곱을

```text
C2 = product_{p>2} (1-1/(p-1)^2)
```

로 둔다. 짝수 `N`의 Goldbach 특이급수는 모든 국소 보정인자가 1 이상이므로
`S(N)>=2C2`이다.

### Theorem GB-128: `ExplicitTwinConstantTailLowerBound`

모든 정수 `M>=3`에 대해

```text
C2 >= product_{3<=p<=M}(1-1/(p-1)^2) * (M-1)/M.
```

### 증명 / Proof

`p<=M`인 인자를 분리한다. 남은 소수 인덱스 `m=p-1`은 `m>=M`인 모든
정수의 부분집합이다. 각 인자가 `(0,1)`에 있으므로 소수 부분집합의 곱은
모든 정수 꼬리의 곱보다 작지 않다. 후자는

```text
product_{m=M}^infinity (1-1/m^2) = (M-1)/M
```

으로 망원곱된다. `QED`

`M=1000`에서 거대한 분자와 분모를 문자열로 보존한 정확한 유리수 인증은

```text
2C2 >= A_1000 = 1.3191709964536598... > 1.31917
```

을 준다. 따라서 TICKET-126의 `B<2.1`, `H=4*10^18`, 그리고 초등적 구간
`42<log H<43`을 사용하면

```text
A_1000 - 55/log(H) - B log(H)^2/sqrt(H)
  > 1.31917 - 55/42 - 2.1*43^2/(2*10^9)
  = 0.0096442490... > 0.
```

즉 다음 점별 정리를 증명하면 강한 Goldbach의 해석적 꼬리가 닫힌다.

```text
|R(N)| <= 55 N/log N for every even N>4*10^18.
```

TICKET-127의 `K<42.83274372223497`보다 약한, 즉 증명하기 쉬운 목표다. 더
정밀한 부동소수 진단상의 경계는 약 `56.503739488756246`이지만, TICKET-128은
엄밀한 여유가 큰 `K=55`만 채택한다.

**중요:** PrimeProject는 `K=55` 잔차 정리를 아직 증명하지 않았다. 증명된
것은 `K=55`가 이제 충분하다는 끝점 예산이다.

```text
Next: PointwiseBinaryGoldbachResidualK55
다음: 점별 이항 Goldbach 잔차 K=55 정리
```

## 5. Twin Prime: endpoint-only 보간의 반례와 복구 정리

TICKET-127의 dyadic 후보는

```text
q_(j+1) <= alpha q_j + beta,
alpha=3/4, beta=23/100
```

이고 조건부 endpoint limsup은 `beta/(1-alpha)=23/25=0.92`이다.

### Proposition TP-128A: `DyadicEndpointInsufficiency`

dyadic endpoint 점화식만으로 모든 큰 `X`에서 `Q_X<1`을 결론낼 수 없다.

### 명시적 반례 / Explicit countermodel

`K_X=1`로 두고 모든 `j`에 대해

```text
Q_(2^j) = 23/25,
Q_(3*2^(j-1)) = 2
```

로 둔다. endpoint 점화식은 매번 등호로 성립하지만, 무한히 많은 중간
규모에서 `Q_X=2>1`이다. 이는 Twin Prime의 반례가 아니라 **endpoint-only
증명 경로의 반례**다.

### Theorem TP-128B: `DyadicToAllScaleEnvelope`

endpoint 점화식과 함께 모든 `2^j<=X<=2^(j+1)`에서

```text
Q_X <= c q_j + delta
```

가 성립하면

```text
limsup_{X->infinity} Q_X <= c*beta/(1-alpha)+delta.
```

### 증명 / Proof

endpoint 점화식을 반복하면 `limsup q_j<=beta/(1-alpha)`이다. 각 dyadic
block에 within-block envelope를 적용하고 block limsup을 취한다. `QED`

현재 동결 계수에서는 필요한 정확한 수치 조건이

```text
0.92 c + delta < 1.
```

특히 `c=1`이면 `delta<0.08`이 필요하다. `c=1, delta=0.07`은 대수적으로
`limsup Q<=0.99`를 주지만, 이 값들은 실제 Vaughan 계수에서 증명된 것이
아니다.

```text
Next: VaughanWithinDyadicBlockEnvelopeC1DeltaBelow008
다음: 실제 Vaughan 계수의 c=1, delta<0.08 구간 포락선
```

이 보간 정리까지 성립해도 parity 생존과 정확한 간격 2 양성은 별도의
미증명 전제다.

## 6. 재현 / Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket128_finite_core_prefix_constant_interpolation.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket128_finite_core_prefix_constant_interpolation
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
node scripts\verify_pages.cjs
```

기본 Collatz 실행은 28비트 frontier를 재구성하므로 일반 단위 테스트보다
오래 걸린다. 단위 테스트는 동일한 알고리즘을 작은 정밀도에서 검사하고,
공개 JSON은 28비트 전체 실행 결과를 보존한다.

## 7. 현재 증명 경계 / Current proof boundary

| 문제 | 닫힌 전제 | 열린 전제 |
|---|---|---|
| RH | compact-support 원소의 유한 소수항 | 조밀성, archimedean 구간, 전역 양성 |
| Collatz | `n<2^28`의 stabilized 대표 | 모든 `k`에 대한 균일 배제 |
| Goldbach | `A>1.31917`, `K=55` 충분조건 | 실제 점별 잔차 `K<=55` |
| Twin Prime | endpoint-only no-go와 all-scale 충분조건 | 실제 within-block 계수, parity, gap 2 |

네 추측의 해결 개수는 0이다. TICKET-128의 가치는 해결을 가장하는 데 있지
않고, 다음 시도가 공격해야 할 정량적이고 반증 가능한 명제를 더 작게 만든
데 있다.

## 8. 문헌 경계 / Literature boundary

- A. Connes and C. Consani, [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368). Weil explicit-formula context; no RH positivity result is imported.
- T. Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562). Almost-all context; it does not supply the universal prefix theorem.
- J. B. Friedlander, D. A. Goldston, H. Iwaniec, and A. I. Suriajaya, [Exceptional zeros and the Goldbach problem](https://doi.org/10.1016/j.jnt.2021.06.004). Binary Goldbach normalization context.
- K. Ford and J. Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368). Sieve and parity boundary; no exact-gap theorem is imported.

The finite-prime reduction, prefix audit, rational singular-series bound, and
interpolation countermodel are proved and machine-audited locally.
