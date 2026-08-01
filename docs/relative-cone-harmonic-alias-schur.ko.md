# TICKET-176: 상대 원뿔, 콜라츠 조화 보정, parity alias, 가중 Schur 순환성

## 주장 경계

TICKET-176은 TICKET-175의 네 미해결 노드를 이어간다. 네 개의 정확한 구조
정리와 그 유한 결과를 검증했지만 리만 가설, 콜라츠 추측, 강한 골드바흐
추측, 쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않았다. 네 상태는
모두 `open_not_proven`이며 기계 해결 수는 0이다.

| 문제 | 새로 확정한 결과 | 폐기한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | 상대 Loewner 양의 준정부호 원뿔 인증 | 대각 또는 절대 tail 자료로 전체 form 상계를 대신함 | `PoleNeutralWeilTailHasUniformCoreRelativeLoewnerBoundBelowTruncatedMargin` |
| 콜라츠 | 비주기 비하강 궤도의 보정항을 명시적 `O(log h)`로 상계 | 고정 하강 시간 또는 조화 경계를 필요충분조건으로 사용 | `AperiodicNonDescendingValuationDiscrepancyExceedsDistinctStateHarmonicEnvelope` |
| 골드바흐 | 모든 짝수 표적에 대한 정확한 parity-alias 몫 | 같은 짝수 위상을 합치기 전에 절댓값을 취함 | `ParityAliasedFixedFareyMinorPolynomialHasUniformDeficitPowerSavingBelowMajorMain` |
| 쌍둥이 소수 | 최적 가중 Schur는 block 스펙트럼 노름과 같음 | 자유 가중치 최적화를 더 쉬운 보조정리로 취급 | `PrimePairHaarBlocksAdmitExplicitArithmeticWeightsWithPowerSavingSchurSums` |

## 1. 리만 가설: 상대 metric에서 양의 준정부호 원뿔을 보존한다

### 이번에 증명한 정확한 명제

`G`가 양의 정부호이고 `A_T,A`가 Hermitian 행렬이라고 하자. Loewner 순서로

```text
A_T >= delta G,
-epsilon G <= A-A_T <= epsilon G
```

이면

```text
A >= (delta-epsilon)G
```

이다. 따라서 `delta>=epsilon`이면 가장 작은 Euclidean 고유값이 극도로
작아도 `A`가 양의 준정부호임을 인증한다.

### 증명과 no-go

임의의 벡터 `x`에 대해

```text
x* A_T x >= delta x*Gx,
x*(A-A_T)x >= -epsilon x*Gx
```

를 더하면 바로 결론을 얻는다. TICKET-171은 가역인 부호 KKT core의 inertia,
즉 양·음 고유값 개수를 보존했다. 이번 정리는 양의 metric을 기준으로 0
고유값 경계를 포함하는 닫힌 양의 준정부호 원뿔을 다룬다는 점이 다르다.

tail의 대각 원소만으로는 이 전제를 얻을 수 없다. 단위행렬에 zero tail을
더한 경우와 `[[0,1.25],[1.25,0]]`을 더한 경우는 tail 대각이 모두 `(0,0)`이다.
그러나 결과의 최소 고유값은 각각 `1`, `-0.25`이다. 실제 증명에는 대각이
아닌 전체 quadratic form 제어가 필요하다.

### 재현 가능한 scale 계산

`G=diag(10^-d,1)`, `A_T=0.25G`, `E=-0.20G`를 쓰면 다음과 같다.

| `d` | 절대 Weyl 하한 | 상대 margin | 정확한 최소 고유값 |
|---:|---:|---:|---:|
| 4 | 약 `-0.20` | `0.05` | `5e-6` |
| 16 | 약 `-0.20` | `0.05` | `5e-18` |
| 64 | 약 `-0.20` | `0.05` | `5e-66` |
| 128 | 약 `-0.20` | `0.05` | `5e-130` |

이는 정확한 모델 정리이지 실제 Weil tail 추정이 아니다. 남은 보조정리는 하나의
고정 pole-neutral core에서 양의 truncated 상대 margin과 그보다 작은 전체
tail 상대 상계를 함께 증명해야 한다.

## 2. 콜라츠 추측: 궤도 의존 선형 보정을 로그 상계로 바꾼다

### 이번에 증명한 정확한 명제

가속 홀수 궤도 `n_i=T^i(n)`에 대해

```text
S_h = sum_(i<h) v2(3n_i+1),
C_h = sum_(i<h) log2(1+1/(3n_i))
```

라 하자. 궤도가 비주기적이고 `0<=i<h`에서 `n_i>=n`이라고 가정하면 상태들은
서로 다른 홀수이므로

```text
C_h <= 1/(3 ln 2) sum_(j<h) 1/(n+2j)
    <= H(n,h),

H(n,h) = 1/(3 ln 2) [1/n + 1/2 ln(1+2(h-1)/n)]
```

이다. 정확한 affine 항등식은

```text
log2(n_h/n) = h log2(3) - S_h + C_h
```

이다. 따라서 시작값 아래로 내려가지 않는 비주기 궤도는 모든 prefix에서

```text
S_h-h log2(3) <= H(n,h)=O(log h)
```

를 만족해야 한다.

### 증명과 두 경로의 교정

비주기성이 첫 `h`개 상태의 서로 다름을 보장한다. 이를 크기순으로 놓으면
`j`번째는 `n+2j` 이상이다. `log2(1+x)<=x/ln 2`와 감소함수의 적분 상계를
적용하면 결론이 나온다.

조화 경계 초과는 하강의 충분조건일 뿐 필요조건은 아니다. 시작값 `63`은
34단계에서 `61<63`으로 내려간다. 이때 중심화 valuation 초과는 약 `0.1113`,
`H(63,34)`는 약 `0.1800`이므로 더 강한 조화 경계를 넘지 않는다.

모든 시작값에 적용되는 고정 하강 시간도 없다. `n=2^m-1`이면 첫 `m-1`개
가속 단계의 valuation이 모두 1이고

```text
T^i(n)=3^i 2^(m-i)-1
```

이어서 모두 증가한다. 이는 임의로 긴 초기 지연을 주는 정확한 수열이지 발산
궤도가 아니다.

### 유한 계산

`3`부터 `100,000`까지 홀수 `49,999`개는 모두 유한 계산에서 하강했다. 첫
하강 전에 충분 조화 경계를 넘지 않은 시작값은 정확히 `63` 하나였다. 이 계산은
항등식과 충분·필요 조건의 차이를 검증하지만 모든 자연수에 대한 증명은 아니다.

## 3. 강한 골드바흐 추측: 절댓값 전에 parity로 합친다

### 이번에 증명한 정확한 명제

`L`이 짝수이고 `c_k`가 고정 minor 집합의 Fourier 계수라고 하자. 짝수 표적
`n=2m`에서는 `k`와 `k+L/2`의 위상이 같다. 따라서

```text
d_r = c_r 1_minor(r) + c_(r+L/2) 1_minor(r+L/2)
```

로 정의하면

```text
E_minor(2m) = sum_(r<L/2) d_r exp(2 pi i r m/(L/2))
```

가 정확히 성립한다. 이 parity alias는 모든 강한 골드바흐 표적에서 정보를
전혀 잃지 않으며, 합친 뒤의 절대 envelope는 bin별 envelope보다 클 수 없다.

### 증명과 no-go

두 주파수의 위상 비는 `exp(2 pi i m)=1`이다. 따라서 절댓값 전에 계수를
합칠 수 있고, envelope 비교는 삼각부등식이다.

`L=16`에서 conjugate symmetry를 갖는

```text
c_1=1, c_7=-1, c_9=-1, c_15=1
```

은 alias 뒤 모든 짝수 표적에서 0이지만, bin별 spectral `l1` 질량은 4다.
즉 alias 전에 절댓값을 취하면 짝수 표적에 완전히 보이지 않는 null direction도
센다. 이 반례는 실수 수열 공간의 반례이며 실제 소수 수열은 아니다.

### 고정 Farey 진단

미리 고정한 `Q=16`, 2-bin Farey mask에서:

| 소수 support | 짝수 표적 | bin별 인증 | parity-alias 인증 |
|---:|---:|---:|---:|
| 64 | 31 | 31 | 31 |
| 128 | 63 | 56 | 56 |
| 256 | 127 | 82 | 86 |
| 512 | 255 | 89 | 93 |
| 1,024 | 511 | 109 | 111 |

987개 Fourier 및 alias 항등식이 모두 통과했다. 유한 인증 수는 367개에서
377개로 늘었다. 그러나 이는 점근적 one-sided bound가 아니다. 남은 정리는
실제 소수 계수의 aliased polynomial에 대해 독립적으로 증명한 major main보다
작은 균일 `L-infinity` deficit 상계를 주어야 한다.

## 4. 쌍둥이 소수 추측: 최적 Schur 가중치는 스펙트럼 문제와 같다

### 이번에 증명한 정확한 명제

음이 아닌 block-norm 행렬 `B`와 양의 벡터 `u,v`에 대해

```text
R=max_i (Bv)_i/u_i,
C=max_j (B^T u)_j/v_j
```

라 하면

```text
||B||_2 <= sqrt(RC)
```

이다. `B`가 모든 원소에서 양수이면 모든 양의 `u,v`에 대한 우변의 최솟값은
`||B||_2`와 정확히 같다. 양의 좌·우 최대 singular vector가
`R=C=||B||_2`를 달성한다.

### 증명과 no-go

가중 Cauchy-Schwarz로

```text
(Bx)_i^2 <= (Bv)_i sum_j B_ij x_j^2/v_j
```

를 얻는다. `i`에 대해 합하고 `(Bv)_i<=Ru_i`, `(B^T u)_j<=Cv_j`를 적용하면
노름 상계가 나온다. 모든 원소가 양수인 행렬에는 Perron-Frobenius 정리에 의해
양의 최대 singular vector가 존재하며 이 벡터들이 등호를 만든다.

따라서 자유로운 Schur 가중치를 수치적으로 최적화하는 것은 TICKET-175의 block
operator 문제를 단순화하지 않는다. 같은 스펙트럼 문제를 다시 푸는 것이다.
유효한 보조정리는 미지의 singular vector를 보기 전에 산술적 scale 구조로
가중치를 정해야 한다.

| `X` | block 연산자 노름 | 최적 가중 Schur | 무가중 Schur | 무가중 비율 |
|---:|---:|---:|---:|---:|
| 10,000 | 128.95 | 128.95 | 155.94 | 1.21 |
| 100,000 | 4,797.48 | 4,797.48 | 5,263.68 | 1.10 |
| 1,000,000 | 100,752.42 | 100,752.42 | 118,015.62 | 1.17 |
| 10,000,000 | 4,516,032.93 | 4,516,032.93 | 5,074,494.72 | 1.12 |

이 값들은 유한 rough-semiprime Type-II 행렬이지 소수쌍 점근 정리가 아니다.
다음 보조정리는 명시적 산술 가중치를 제시하고 두 방향의 가중합 모두에 균일한
power saving이 있음을 증명해야 한다.

## Proof DAG와 상태

각 문제의 DAG는 세 노드를 정확히 구분한다.

```text
폐기/불충분 -> 정확히 증명한 축약 -> 미증명 다음 보조정리
```

가운데 노드는 원 추측의 증명이 아니다. 마지막 노드는 네 문제 모두
`open_not_proven`이다.

## 문헌 경계

- 최근 [truncated Weil-form 수치 연구](https://arxiv.org/abs/2605.20224), [명시적 tail 연구](https://arxiv.org/abs/2607.02828), [연산자 실험](https://arxiv.org/abs/2607.24830)은 이번에 필요한 상대 continuum 정리를 제공하지 않는다.
- [Tao의 almost-all 콜라츠 정리](https://arxiv.org/abs/1909.03562)는 모든 궤도의 조화 경계 초과를 뜻하지 않는다.
- 최근 [골드바흐 예외집합 연구](https://arxiv.org/abs/2607.27282)는 균일 binary aliased-minor 상계를 제공하지 않는다.
- [Ford-Maynard의 prime-producing sieve 연구](https://arxiv.org/abs/2407.14368)는 실제 Type-II 정보가 여전히 필요함을 보여준다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket176_relative_cone_harmonic_alias_schur.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket176_relative_cone_harmonic_alias_schur -v
```

정본 기계 판독 artifact는
`data/open-problem/ticket176-relative-cone-harmonic-alias-schur.json`이다.
