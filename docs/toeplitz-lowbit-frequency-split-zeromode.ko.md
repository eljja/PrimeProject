# TICKET-178: Toeplitz 합가능성, Collatz 저비트, Goldbach 주파수 분할, 교차-Gram 영주파수

## 주장 상태

**네 추측은 모두 미해결입니다.** TICKET-178은 정확한 조건부 충분조건 또는
no-go 명제 네 개를 증명했습니다. 리만 가설, 콜라츠 추측, 강한 골드바흐
추측, 쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않았습니다. 아래
유한 계산은 회귀 검사와 경로 감사이며 무한 범위의 귀납 단계가 아닙니다.

| 문제 | 새로 확립한 결과 | 상태 | 폐기한 경로 | 남은 간극 | 다음 단일 보조정리 |
|---|---|---|---|---|---|
| 리만 | `합가능 Toeplitz 꼬리 인증 및 비합가능 프로필 no-go` | 미해결 | 감쇠 지수 `s <= 1`인 절댓값 Toeplitz 포락선 | 실제 whitening된 Weil 꼬리에 대한 합가능 산술 우세행렬이 없음 | `PoleNeutralWeilWhitenedTailHasSummableOffDiagonalProfileBelowCoreMargin` |
| 콜라츠 | `저비트 점유율 하강 기준 및 고정 지평 혼합 no-go` | 미해결 | 보편적인 고정 지평 저비트 혼합 | 모든 궤도의 적응형 점유율 교차와 비자명 주기 배제가 없음 | `EveryAperiodicNonDescendingOrbitCrossesLowBitOccupancyThreshold` |
| 골드바흐 | `주파수 분할 Sobolev 인증 및 전역 예산 no-go` | 미해결 | 하나의 전역 도함수·에너지 예산을 필요조건처럼 사용 | 모든 목표 짝수에 통하는 dyadic 산술 예산이 없음 | `ParityAliasedMinorHasUniformDyadicSplitSobolevBudgetBelowMajorMain` |
| 쌍둥이 소수 | `교차-Gram 영주파수 인증 및 절댓값 위상 소실 no-go` | 미해결 | 절댓값 교차-Gram을 충분통계로 사용 | 실제 소수쌍 Haar 블록의 부호 있는 영주파수 power saving이 없음 | `PrimePairHaarSignedCrossGramZeroModeHasPowerSavingRelativeToDiagonalEnergy` |

## 1. 리만 가설

### 이번에 선언한 정확한 명제

`E_N`이 `N x N` Hermitian 행렬이고

```text
|(E_N)_{ij}| <= C (1 + |i-j|)^(-s)
```

라고 하자. `s>1`이면 모든 `N`에 대해 균일하게

```text
||E_N||_2 <= C(2 zeta(s)-1)
```

이다. 따라서 whitening된 유한 core의 상대 Loewner 여유가 `delta`이고
`C(2 zeta(s)-1)<delta`이면 이 꼬리는 양성을 파괴하지 못한다. 반대로
`s<=1`이면 위 성분 상계를 등호로 만족하는 양의 Toeplitz 행렬의 spectral
radius는 `N`과 함께 무한히 커진다.

### 증명

Schur 행합 상계로

```text
||E_N||_2 <= max_i sum_j |(E_N)_{ij}|
           <= C(1 + 2 sum_{r>=1}(1+r)^(-s))
```

를 얻는다. 마지막 급수는 `2 zeta(s)-1`이며 정확히 `s>1`일 때 수렴한다.
역방향 반례족에서는 모든 성분을 양의 프로필 값으로 둔다. 정규화된 all-one
벡터의 Rayleigh 몫은

```text
R_N = C/N [N + 2 sum_{r=1}^{N-1}(N-r)/(1+r)^s]
```

이다. `s=1`이면 로그 크기로, `s<1`이면 `N^(1-s)` 크기로 발산한다.
따라서 이 형태의 **절댓값 프로필**은 합가능성 경계 아래에서 차원에 균일한
인증을 줄 수 없다.

### 재현 계산

`C=0.02`, `delta=0.25`, 차원 `16,64,256,1024,4096`, 지수
`0.75,1,1.25,2`를 사용했다.

- 비합가능 프로필 두 개는 시험한 유한 절단에서 core 여유를 넘어섰다.
- 합가능 프로필 두 개는 적분 꼬리를 포함한 무한 행합 상계가 core 여유보다 작았다.
- all-one Rayleigh 하한은 모든 행에서 유한 Schur 상계 이하임을 확인했다.

### 남은 논리적 간극

이는 위상을 버린 Toeplitz 우세행렬의 정확한 임계값이지 실제 pole-neutral
Weil 꼬리에 대한 정리가 아니다. 부호 상쇄가 있으면 절댓값 `l1` 프로필 없이도
좋은 연산자 상계가 가능하다. 실제 산술 꼬리에 대해 충분히 작은 상수를 가진
선험적 합가능 프로필을 만들거나 위상 민감 상계로 대체해야 한다.

## 2. 콜라츠 추측

### 이번에 선언한 정확한 명제

가속 홀수 궤도 접두어 `n_0,...,n_{h-1}`에 대해

```text
A_2(h) = #{i<h : n_i = 1 mod 4},
A_3(h) = #{i<h : n_i = 5 mod 8}
```

라 두면

```text
sum_{i<h} v2(3n_i+1) >= h + A_2(h) + A_3(h)
```

이다. 접두어가 비주기적이며 한 번도 `n_0` 아래로 내려가지 않는다면
TICKET-177의 6-휠 보정 상계 `H_6(n_0,h)` 때문에 반드시

```text
A_2(h)+A_3(h) <= (log2(3)-1)h + H_6(n_0,h)
```

이어야 한다. 따라서 이 부등식의 엄격한 위반은 하강을 인증한다.

### 증명

홀수 `n`에 대한 합동식 계산으로

```text
v2(3n+1) >= 2  <=> n = 1 mod 4,
v2(3n+1) >= 3  <=> n = 5 mod 8
```

을 얻는다. 양의 정수 valuation의 layer-cake 전개가 첫 부등식을 준다. 정확한
궤도 항등식은

```text
log2(n_h/n_0)
= h log2(3) - sum_{i<h} v2(3n_i+1) + C_h
```

이다. 비하강이면 좌변이 음수가 아니고, TICKET-177에서 `C_h<=H_6`를
증명했으므로 결과가 따른다.

### 고정 지평을 폐기하는 무한 반례족

`n_0=2^m-1`이면 처음 `m-2`개의 관련 상태는

```text
n_i = 3^i 2^(m-i)-1 = 7 mod 8,
v2(3n_i+1)=1,
n_i >= n_0
```

을 만족한다. `m`을 임의로 크게 할 수 있으므로 모든 고정 지평에서 `A_2`와
`A_3` 기여가 전혀 없는 자연수 비하강 접두어가 존재한다. 보편적인 고정
지평 저비트 혼합 보조정리는 거짓이다.

### 재현 계산

`3`부터 `100,000`까지 홀수 시작값 `49,999`개를 감사했다.

- 제한된 탐색 안에서 모두 더 작은 값에 도달했다.
- `44,537`개는 첫 하강 시점까지 저비트 충분조건을 교차했다.
- `5,462`개는 그 충분조건을 교차하지 않고도 하강했다.
- 가장 긴 첫 하강 지평은 `85`였다.
- `m=8,16,32,64`인 Mersenne 접두어의 닫힌형 검사가 모두 통과했다.

이 수치는 `100,000`보다 큰 시작값이나 무한 범위를 증명하지 않는다.

### 남은 논리적 간극

6-휠의 여덟 residue class에 균등하다면 `A_2/h=1/2`, `A_3/h=1/4`이고
보정항을 제외한 여유는 `0.75-(log2(3)-1) ~= 0.165`이다. 그러나 모든 가상
비하강 궤도에 이 적응형 점유율을 강제하는 정리는 없다. 비자명 주기도 별도
논증으로 배제해야 한다.

## 3. 강한 골드바흐 추측

### 이번에 선언한 정확한 명제

실수값, 평균 0인 1-주기 함수 `P=L+H`를 켤레대칭 주파수 band로 나누고
`H`에는 영주파수가 없다고 하자. 다음을 가정한다.

```text
||H||_infinity <= B < A,
||L'||_infinity <= D,
integral_0^1 L(x)^2 dx <= E.
```

`A-B>D/2`이거나 `E<(A-B)^3/(4D)`이면 `A+P`는 모든 점에서 양수이다.
Fourier 계수 `d_k`에 대해서는

```text
B <= sum_high |d_k|,
E = sum_low |d_k|^2,
D <= 2 pi sum_low |k d_k|
```

로 계산할 수 있다.

### 증명

먼저 `H(x)>=-B`를 적용한다. low band `L`은 평균 0이므로 잔여 major
`A-B`에 TICKET-177의 Sobolev 점별 보조정리를 적용한다. Parseval 항등식,
항별 미분, 삼각부등식이 Fourier 예산을 준다.

### 전역 예산을 폐기하는 양의 반례족

`K>=16`에 대해

```text
F_K(x)=1+0.2 cos(2 pi x)+0.1 cos(2 pi Kx)
```

라 두면 초등적 하한은 `F_K>=0.7`이다. 하지만 분할하지 않은 도함수 상계는
`K`에 선형으로 증가하여 `K=16,64,256,1024` 모두에서 전역 TICKET-177
인증이 실패한다. high band의 sup 상계를 `0.1`로 분리하면 잔여 major는
`0.9`이고 low-band 도함수 인증은 통과한다. 즉 전역 검사는 충분조건이지만
필요조건이 아니며 무해한 고주파 성분만으로도 악화될 수 있다.

### 재현 계산

소수 지지범위 `64,128,256,512,1024`와 TICKET-177의 고정 Farey mask를
사용하여 선험적 dyadic split 전체를 감사했다.

- 지지범위 `64`는 통과하는 분할이 하나 이상 있었다.
- `128,256,512,1024`에는 통과하는 시험 분할이 없었다.
- 다섯 유한 범위에서 정확한 골드바흐 표현 수는 모두 양수였다.

마지막 항목은 유한 범위 확인일 뿐 모든 큰 짝수에 대한 정리가 아니다.

### 남은 논리적 간극

새 정리는 진단 방식의 결함을 고쳤지만 필요한 산술 추정을 만들지 않는다.
모든 큰 짝수에 대해 high-band sup 예산과 low-band Sobolev 예산을 독립적으로
증명한 major-arc 하한 아래에 넣는 하나의 선험적 dyadic 분해가 필요하다.

## 4. 쌍둥이 소수 추측

### 이번에 선언한 정확한 명제

유한차원 연산자 `T_0,...,T_{m-1}`에 대해 부호 있는 scalar
Hilbert-Schmidt 교차-Gram 행렬을

```text
H_ij=<T_i,T_j>_HS
```

로 정의하면

```text
1* H 1 = ||sum_j T_j||_HS^2,
||sum_j T_j||_op^2 <= 1* H 1
```

이다. 따라서

```text
1* H 1 <= eta sum_j ||T_j||_HS^2
```

는 합 연산자의 power saving을 보증하는 충분조건이다.

### 증명과 위상 소실 no-go

첫 항등식은 Hilbert-Schmidt 제곱을 전개하면 되고, 두 번째는
`||.||_op<=||.||_HS`이다. scalar 연산자에서 정렬 위상 `T_j=1`과
`m`차 단위근 `T_j=exp(2 pi i j/m)`을 비교하자. 두 족은 성분 노름이 모두
1이고 절댓값 교차-Gram의 모든 성분도 1이다. 그러나 부호 있는 all-plus
영주파수는 각각 `m^2`과 `0`이다. 절댓값을 취하면 산술 합에 필요한 위상을
정확히 잃는다.

### 재현 계산

`m=4,8,16,32`를 검사했다.

- 두 절댓값 교차-Gram 행렬은 부동소수점 허용오차 안에서 같았다.
- 정렬 영주파수는 `m^2`이었다.
- 단위근 영주파수는 `1e-25`보다 작았다.
- 두 족의 대각 에너지는 모두 `m`이었다.

### 남은 논리적 간극

이는 올바른 충분조건과 데이터 계약을 제시할 뿐이다. 실제 소수쌍 Haar
블록의 부호 있는 영주파수가 대각 에너지보다 power saving만큼 작다는 정리는
없다. Hilbert-Schmidt 대각 에너지 자체가 너무 클 수도 있으므로 산술 rank와
scale 성장도 함께 제어해야 한다. 쌍둥이 소수 하한은 아직 얻지 못했다.

## 네 문제를 관통하는 결론

네 트랙의 공통 장애물은 양화사의 불일치다. 유한 절단, 고정 지평, 전역
주파수 예산, 절댓값 위상 요약은 추측에 필요한 하나의 무한 또는 목표별 mode를
제어하지 못한다. TICKET-178은 이를 네 개의 정량화된 다음 보조정리로
교체했지만 실제 산술 객체에 대해 그 보조정리들을 증명하지는 못했다.

## 최신 문헌과의 경계

- 최근 계산 가능한 Weil 형식과 명시적 꼬리 연구는 유한 절단과 꼬리 상계를
  제공하지만 여기서 필요한 summable whitening 프로필은 제공하지 않는다:
  [arXiv:2605.20224](https://arxiv.org/abs/2605.20224),
  [arXiv:2607.02828](https://arxiv.org/abs/2607.02828),
  [arXiv:2607.24830](https://arxiv.org/abs/2607.24830).
- Tao의 결과는 로그 밀도 의미의 almost-all 정리이며 모든 궤도 정리가 아니다:
  [arXiv:1909.03562](https://arxiv.org/abs/1909.03562). 최근 one-bit 환원은
  저비트 목표에 동기를 주지만 해결로 취급하지 않는다:
  [arXiv:2603.25753](https://arxiv.org/abs/2603.25753).
- Helfgott의 minor-arc 연구는 ternary Goldbach를 다루고, 최근 binary 연구도
  exceptional set을 남긴다:
  [arXiv:1205.5252](https://arxiv.org/abs/1205.5252),
  [arXiv:2607.27282](https://arxiv.org/abs/2607.27282).
- 현대 prime-producing sieve도 강한 Type-II 분포 입력을 요구하며 위 영주파수
  보조정리를 제공하지 않는다:
  [arXiv:1910.14674](https://arxiv.org/abs/1910.14674),
  [arXiv:2407.14368](https://arxiv.org/abs/2407.14368).

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts/ticket178_toeplitz_lowbit_split_zeromode.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket178_toeplitz_lowbit_split_zeromode -v
```

기계 판독 산출물:

```text
data/open-problem/ticket178-toeplitz-lowbit-split-zeromode.json
data/open-problem/riemann/rh-ticket-178-toeplitz-threshold.json
data/open-problem/collatz/co-ticket-178-lowbit-occupancy.json
data/open-problem/goldbach/gb-ticket-178-frequency-split.json
data/open-problem/twin-prime/tp-ticket-178-zeromode-crossgram.json
```

정리 내부 검사가 하나라도 실패하면 생성기는 비정상 종료한다. JSON 계약은 네
시도의 상태를 모두 `open_not_proven`, 해결 수를 `0`으로 고정한다.
