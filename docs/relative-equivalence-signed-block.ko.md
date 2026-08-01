# TICKET-175: 상대적 스펙트럼 해상도, 콜라츠 동치 zero-lift, 부호 있는 Farey minor, Haar block 연산자

## 주장 경계

TICKET-175는 TICKET-174가 남긴 네 OPEN 노드를 이어간다. 이번 결과는 네
개의 정확한 축약 또는 no-go 명제를 증명하지만, 리만 가설·콜라츠 추측·강한
골드바흐 추측·쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않는다.
모든 상태는 `open_not_proven`이며 기계 해결 수는 0이다.

| 문제 | TICKET-175 정확 결과 | 폐기 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | 절대 tail 오차와 작은 고유값 사이의 해상도 장벽 | 다항 cutoff 절대 노름으로 극소 스펙트럼 부호 결정 | `StructuredRelativeWeilCoreErrorPreservesNonnegativityBelowGroundStateScale` |
| 콜라츠 | eventual zero-lift 비하강 배제는 콜라츠와 동치 | 이를 더 약한 중간 보조정리로 취급 | `EveryAperiodicNaturalValuationRayCrossesItsCorrectedLogDescentBoundary` |
| 골드바흐 | 절대 minor budget은 양의 minor 질량을 정확히 두 번 잃음 | 고정 Farey L1 bound가 필요한 부호 상쇄를 보존 | `FixedFareySignedMinorDeficitPowerSavingBelowMajorMainUniformly` |
| 쌍둥이 소수 | 전체 연산자는 Haar block-norm scale 행렬로 지배됨 | 모든 scale pair가 개별 Frobenius 절약을 가져야만 합산 가능 | `PrimePairHaarBlockNormScaleMatrixHasUniformPowerSavingOperatorNorm` |

## 1. 리만: 절대 스펙트럼 해상도는 필요한 규모와 맞지 않는다

### 이번에 증명한 정확한 명제

Hermitian 연산자 `A`와 절단 근사 `A_T`가

```text
||A-A_T||_op <= B(T)
```

를 만족하면 Weyl 변분 부등식으로

```text
lambda_min(A) >= lambda_min(A_T)-B(T)
```

를 얻는다. 따라서 이 절대 오차 방식으로 비음이 아님을 인증하려면 엄밀한
유한 하한 margin이 오차 반지름보다 커야 한다. TICKET-174의 명시적 상계에
고정된 `k>1`과 `T=N^k`를 대입하면

```text
U_N(N^k) = O(N^(1-k) log N)
```

이다. 그러므로 모든 `N`의 역다항식보다 작은 margin은 이 인증으로 결정할
수 없다. 이는 정확한 Weil form이 아니라 이 특정 인증 방법에 대한 no-go다.

### 증명

Rayleigh quotient에 연산자 노름 섭동 상계를 적용하고 최솟값을 취하면 첫
부등식을 얻는다. 명시적 tail 식에서 `N/T=N^(1-k)`, `log T=k log N`이므로
두 번째 점근식이 나온다. 또한 근사 고유값 0과 절대 오차 `epsilon`은 정확한
고유값 `+epsilon`, `-epsilon` 모두와 양립하므로, margin이 오차보다 크지
않으면 부호를 정할 수 없다.

### 재현 가능한 해상도 계산

최근 공개 Galerkin 계산은 `c=100`에서 smallest-positive even-sector branch의
크기를 보고한다. 이는 인증된 하한이 아니라 수치값이며 Galerkin upper bound다.
TICKET-175는 이를 해상도 목표로만 사용하고, 로그 좌표에서
`U_N(T)=10^-d`를 푼다.

| N | 보고된 `d=-log10|lambda|` | `log10 U_N(N^2)` | `log10 U_N(N^3)` | 필요한 `log10 T` |
|---:|---:|---:|---:|---:|
| 100 | 190.92 | -1.240 | -3.084 | 195.319 |
| 150 | 247.19 | -1.386 | -3.403 | 251.874 |
| 200 | 294.31 | -1.490 | -3.631 | 299.194 |
| 250 | 333.68 | -1.571 | -3.808 | 338.714 |

이 표는 명시적 절대 상계 방식에 천문학적인 `T`가 필요함을 뜻한다. 정확한
tail이 실제로 그만큼 크다는 뜻도 아니고, 구조적·상대적 추정을 배제하지도
않는다.

### 남은 간극

다음 보조정리는 절대 노름으로 극소 고유값을 직접 해상하지 않고도 부호를
보존해야 한다. 상대 quadratic-form 부등식, 양의 factorization, pole-neutral
constraint core의 구조적 비교가 후보다.

## 2. 콜라츠: 선택한 OPEN 노드는 원 추측을 바꿔 쓴 것이다

### 이번에 증명한 정확한 명제

가속 홀수 Collatz map `T`에 대해 다음은 동치다.

1. 모든 양의 정수가 1에 도달한다.
2. 모든 홀수 `n>1`에 대해 `T^h(n)<n`인 `h`가 존재한다.
3. 모든 가속 iterate가 시작값 이상인 자연수 궤도는 존재하지 않는다.

자연수 cylinder ray가 `n`으로 안정화한 뒤의 edge는 TICKET-174의 유일한
zero-lift 자식과 정확히 같다. 따라서

```text
NoNonDescendingRayEventuallyFollowsUniqueZeroLiftChildren
```

은 더 쉬운 중간 정리가 아니라 Collatz와 동치다.

### 증명

Collatz가 참이면 궤도는 `1<n`에 도달한다. 반대로 모든 홀수 `n>1`이 더 작은
홀수로 내려간다고 하자. `n`에 대한 강한 귀납법으로 모든 홀수는 1에 도달하고,
짝수는 2의 거듭제곱을 제거하면 홀수가 된다. descent 명제의 부정은 시작값
아래로 한 번도 내려가지 않는 궤도와 정확히 같다.

자연수 valuation prefix의 modulus가 `n`보다 커진 뒤에는 `n`이 해당 residue
class의 최소 양의 대표다. 이후 실제 valuation extension의 lift quotient는
모두 0이며 TICKET-174에서 그 자식의 유일성을 증명했다.

계산에 사용한 정확한 로그 좌표는 다음과 같다.

```text
log2(T^h(n)/n)
  = h log2(3) - S_h
    + sum_(i<h) log2(1 + 1/(3 T^i(n))).
```

오른쪽이 음수가 되는 것과 descent는 동치다.

### 재현 가능한 유한 계산

| 홀수 시작값 상한 | 검사한 홀수 | descent 실패 | 최대 first-descent 길이 | 기록 시작값 |
|---:|---:|---:|---:|---:|
| 1,000 | 499 | 0 | 51 | 703 |
| 10,000 | 4,999 | 0 | 51 | 703 |
| 100,000 | 49,999 | 0 | 85 | 35,655 |
| 1,000,000 | 499,999 | 0 | 111 | 626,331 |

이 유한 결과는 모든 정수에 대한 증명이 아니다. 정확 좌표를 검증하고, 동치인
재서술을 진전으로 잘못 계산하지 않게 하는 역할만 한다.

### 남은 간극

다음 목표는 aperiodic 자연 valuation ray가 정확한 보정 로그 경계를 한 번은
넘는다는 명제다. 비자명 cycle 배제는 별도의 간극으로 남는다.

## 3. 골드바흐: minor 절대값을 취할 때 잃는 양의 질량

### 이번에 증명한 정확한 명제

target의 정렬 부호를 보기 전에 Fourier major set `M`을 고정하자. 짝수 target의
정확 convolution을

```text
R = Major + P_minor - N_minor
```

로 쓰자. 여기서 `P_minor,N_minor>=0`은 minor의 양·음 정렬 질량이다. 삼각
부등식 인증의 margin은

```text
Major - P_minor - N_minor = R - 2 P_minor
```

이다. 즉 L1 minor 상계는 도움이 되는 양의 minor 항을 정확히 두 번 잃는다.

### 증명

첫 식은 고정 major mask와 그 여집합을 부호별로 나눈 Fourier inversion이다.
정확한 signed 식에서 절대 minor lower bound를 빼면 `2 P_minor`가 남는다.
확률적 또는 점근적 가정은 없다.

### 고정 Farey 계산

mask는 `q<=Q`인 기약 유리수 중심에서 주파수 bin 두 칸 안을 major로 정한다.
각 target phase를 보기 전에 mask가 고정된다.

| 소수 support | target 수 | Q=16 절대 인증 | 통과 비율 |
|---:|---:|---:|---:|
| 64 | 31 | 31 | 1.000 |
| 128 | 63 | 56 | 0.889 |
| 256 | 127 | 82 | 0.646 |
| 512 | 255 | 89 | 0.349 |
| 1,024 | 511 | 109 | 0.213 |

987개 target의 Fourier 재구성과 double-loss 항등식은 모두 통과했다. 유한
통과율 감소가 고정 Farey 체계의 점근 실패를 증명하지는 않는다. 정리 수준의
결론은 L1 치환이 signed cancellation에서 양의 minor를 두 번 잃는다는 것뿐이다.

### 남은 간극

유효한 binary Goldbach 경로에는 target-uniform 양의 major main term과 실제
signed minor-deficit 추정이 함께 필요하다. 정확한 유한 signed 합은 이미 답을
포함하므로 해석적 상계를 대신할 수 없다.

## 4. 쌍둥이 소수: 각 scale을 따로 세기 전에 block으로 압축한다

### 이번에 증명한 정확한 명제

nonconstant Haar domain과 range를 서로 직교인 scale 공간으로 분해하고 해당
연산자 block을 `A_jk`라 하자. scalar scale 행렬을

```text
B_jk = ||A_jk||_op
```

로 정의하면

```text
||A||_op <= ||B||_op
```

이다. 이 방식은 TICKET-174의 `log2 N` 손실 전체를 회수할 수도 있다. matched
scale마다 wavelet 하나를 고른 projection은 물리 연산자 노름과 `B=I`의 노름이
모두 1이지만, 이전 최대-block 합산 상계는 `log2 N`이다.

### 증명

`x`를 서로 직교인 scale 성분 `x_k`로 쓰고 `y_k=||x_k||`라 하자. 출력 scale
`j`의 norm은 `sum_k B_jk y_k` 이하이다. 모든 출력 scale에 대해 Euclidean
norm을 취하면

```text
||Ax|| <= ||B y|| <= ||B||_op ||x||
```

을 얻는다. matched projection은 Haar 좌표에서 직교 projection이고, Haar
conjugation은 연산자 노름을 보존한다. constant 좌표를 쓰지 않아 행·열 합도 0이다.

### 유한 Type-II 진단

| X | 물리 연산자 노름 | block-scale 노름 | Frobenius 노름 |
|---:|---:|---:|---:|
| 10,000 | 127.62 | 128.95 | 130.42 |
| 100,000 | 4,325.60 | 4,797.48 | 4,897.25 |
| 1,000,000 | 92,730.91 | 100,752.42 | 100,972.27 |
| 10,000,000 | 4,499,308.11 | 4,516,032.93 | 4,792,699.11 |

이는 유한 centered rough-semiprime 행렬이지 소수쌍 점근 정리가 아니다. block
지배를 검증하고, block-scale 노름이 Frobenius 합산보다 실제 물리 노름에 더
가까울 수 있음을 보여준다.

### 남은 간극

다음 보조정리는 arithmetic block-norm scale 행렬의 연산자 노름에 uniform
power saving이 있음을 요구한다. 모든 scale pair의 Frobenius energy를 따로
줄이는 것보다 약하지만 여전히 진짜 Type-II 정보가 필요하다.

## 네 문제의 공통 결론

이번 교정은 절대값을 취하기 전에 구조를 보존한다.

1. 리만에는 절대 오차만이 아니라 상대적·부호 보존형 스펙트럼 제어가 필요하다.
2. 콜라츠에는 원 추측의 동치 재서술이 아닌 실제로 더 약한 중간 명제가 필요하다.
3. 골드바흐에는 전체 L1 손실이 아니라 signed minor cancellation이 필요하다.
4. 쌍둥이 소수의 scale pair는 block 연산자 기하로 먼저 합산할 수 있다.

## 문헌 경계

- [Groskin, High-Precision Approximation of Riemann Zeros via the Truncated Weil Form](https://arxiv.org/abs/2605.20224)은 유한 branch scale을 보고하며 RH 증명을 주장하지 않는다.
- [Groskin, finite Guinand-Weil dictionary and archimedean tail order](https://arxiv.org/abs/2607.02828)은 사용한 명시적 tail 상계를 제공한다.
- [Lagarias, The 3x+1 Problem: An Overview](https://arxiv.org/abs/2111.02635)은 stopping-time 정식화를 정리하고, [Tao](https://arxiv.org/abs/1909.03562)는 every-input이 아닌 almost-all 결과를 증명한다.
- [Grimmelt와 Bhowmik, The exceptional set of the Goldbach problem](https://arxiv.org/abs/2607.27282)은 명시적 major-arc 문맥을 주지만 여기 필요한 signed uniform binary 추정은 주지 않는다.
- [Ford와 Maynard, On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368)은 상당한 Type-II 정보가 필요함을 보인다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket175_relative_equivalence_signed_block.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket175_relative_equivalence_signed_block -v
```

정본 기계 판독 artifact는
`data/open-problem/ticket175-relative-equivalence-signed-block.json`이다.
