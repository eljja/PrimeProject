# TICKET-237: principal angle, 유한 palette no-go, dyadic endpoint, Welch floor

상태: **open_not_proven**
생성일: 2026-08-24
상위 추측 해결 수: **0 / 4**

TICKET-237은 TICKET-236이 남긴 네 최고위험 보조정리를 직접 점검한다.
이번 결과는 네 개의 정확한 부분정리 또는 no-go 정리다. 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않았다.

## 1. 리만 가설 트랙

### 이번 선언 명제

**PrincipalAngleCriterionAndNestedCofinalFrameNoGo.**

유한차원 Hilbert 공간에서 injective synthesis map
\(U:\mathbb C^m\to\mathcal H\), \(V:\mathbb C^n\to\mathcal H\)를 잡고

\[
A=U^*U,\qquad B=U^*V,\qquad C=V^*V,\qquad
K=A^{-1/2}BC^{-1/2}
\]

라 하자. \(K\)의 특이값은 \(\operatorname{ran}U\)와
\(\operatorname{ran}V\) 사이 principal angle의 cosine이다. 따라서

\[
\|K\|_{\mathrm{op}}=1
\iff \operatorname{ran}U\cap\operatorname{ran}V\ne\{0\},
\]

\[
\|K\|_{\mathrm{op}}<1
\iff \text{두 span의 최소 principal angle이 양수다}.
\]

특히 두 frame span이 nonzero이고 nested이면 normalized cross norm은
정확히 1이다. 공통 mode를 제거하지 않은 nested cofinal frame으로
TICKET-236의 strict contraction을 얻을 수 없다.

### 논증

\[
Q_U=U(U^*U)^{-1/2},\qquad Q_V=V(V^*V)^{-1/2}
\]

는 각 span 위의 isometry이고 \(K=Q_U^*Q_V\)다. 이것이 principal-angle
행렬이다. \(\|K\|=1\)이면 어떤 단위벡터 \(Q_Vy\)의
\(\operatorname{ran}U\) 위 projection norm이 1이므로 그 벡터가 두 span의
교집합에 속한다. 역은 자명하다.

정확한 innovation 비교족은 서로 직교하는 isometry \(Q,W\)에 대해

\[
U=Q,\qquad V=(3Q+4W)/5
\]

로 둔다. 그러면 \(V\)도 isometry이고 두 span의 교집합은 0이며
\(K=(3/5)I\)다. normalized block의 최소 고유값은 \(1-3/5=2/5\)다.

### 재현 계산과 한계

\(m=2,4,8,16,32\)에서 nested norm \(1\), 최소 고유값 \(0\), innovation
norm \(3/5\), 최소 고유값 \(2/5\)를 유리수로 검산했다.

이 정리는 추상 Gram 기하 정리다. 실제 Guinand-Weil 산술 block이 위
innovation 족이라는 것을 증명하지 않았고, 균일한 산술 angle gap도
확보하지 않았다. zeta 영점은 계산하지 않았다.

- 폐기한 경로: 공통 mode를 포함하는 nested cofinal frame 자체에서 strict
  contraction을 얻는 경로
- 유지할 경로: 공통 span을 quotient한 뒤 서로 다른 logarithmic shell의
  innovation block을 추정
- 다음 단일 보조정리:
  **ArithmeticWeilInnovationCrossBlockAngleGapOnDisjointLogarithmicShells**

## 2. 콜라츠 트랙

### 이번 선언 명제

**NoFinitePrimePaletteUniversallySeparatesBinaryRunBlocks.**

\(w_k=1^k2^{2k}\)에 대해

\[
D_k=32^k-27^k,\qquad B_k=32^k+27^k-2\cdot18^k
\]

라 하자. 임의의 유한 소수 집합 \(S\)에 대해 어떤 \(L\ge1\)가 존재하여,
모든 \(L\)의 양의 배수 \(k\)와 모든 \(q\in S\)에서

\[
q\nmid D_k\quad\text{또는}\quad q\mid B_k
\]

가 성립한다. 즉 \(S\) 안에는 \(q\mid D_k,\ q\nmid B_k\)인
prime-presence witness가 없다. \(q>3\)에 대해

\[
L=\operatorname{lcm}_{q\in S,\ q>3}
\left(\operatorname{ord}_q(32/27),\operatorname{ord}_q(3/2)\right)
\]

를 취할 수 있다. 따라서 어떤 고정 유한 prime palette도 모든 run block을
분리하지 못한다.

### 논증

2와 3은 \(D_k\)를 나누지 않는다. \(q>3\)이고 \(k\)가
\(\operatorname{ord}_q(32/27)\)의 배수이면 \(q\mid D_k\)다. 동시에
\(\operatorname{ord}_q(3/2)\mid k\)이면

\[
\frac{B_k}{27^k}
=(32/27)^k+1-2(2/3)^k
=1+1-2=0\pmod q.
\]

유한 집합의 위수를 lcm으로 묶으면 모든 후보 소수가 동시에 무력화된다.
모든 \(nL\)도 같은 조건을 만족하므로 각 palette마다 이런 \(k\)가
무한히 많다.

### 재현 계산과 한계

다음 네 palette를 정확 위수와 modular exponentiation으로 검산했다.

| palette | 공통 주기 \(L\) |
|---|---:|
| \(5\) | 2 |
| \(2,3,5,7,59\) | 174 |
| \(5,7,13,19,31,37,59\) | 5,220 |
| \(2,3,5,7,13,19,31,37,59,57653\) | 2,594,340 |

각 \(L,2L,3L\)에서 모든 palette 소수가 분리 증인으로 실패함을 확인했다.
유한 행은 일반 정리의 예시이고, 모든 유한 \(S\)에 대한 결론은 lcm
논증에서 나온다.

이 정리는 TICKET-197이 이미 비가분성을 닫은 run-block 안에 머문다.
fresh prime의 필요성만 증명하며, 모든 \(k\) 또는 일반 necklace에서
prime-presence/valuation-gap witness가 존재한다는 것은 증명하지 않는다.
비주기 Collatz 궤도에도 결론을 주지 않는다.

- 폐기한 경로: 크기는 커도 고정된 유한 prime palette를 보편 인증서로 사용
- 유지할 경로: word에 의존해 새 소수를 선택하고 presence보다 강한
  valuation gap을 증명
- 다음 단일 보조정리:
  **WordDependentPrimeValuationGapForEveryPrimitiveBinaryDensityBandNecklace**

## 3. 강한 골드바흐 트랙

### 이번 선언 명제

**TruncatedDyadicUpperEndpointObstructionAndBulkWindowNecessity.**

\(x_X\)를 \(X\) 이하 소수의 indicator, \(g_X=x_X*x_X\)를 ordered
representation count라 하자. 그러면 moving upper endpoint에서

\[
g_X(2X)=\mathbf 1_{\mathbb P}(X).
\]

따라서 TICKET-236의 normalized reflected-phase margin은 \(N=2X\)에서
0 또는 \(1/\pi(X)\)이고 항상

\[
\frac{g_X(2X)}{\pi(X)}
\le \frac1{\pi(X)}
=o(1/\log X).
\]

그러므로 \(N=2X\)를 포함하는 닫힌 dyadic target window에는 고정 양의
inverse-log margin이 존재할 수 없다. composite \(X\)에서는 strict
positivity조차 실패한다.

### 논증

\(p,q\le X\)이고 \(p+q=2X\)라고 하자. \(p<X\)이면 \(q>X\)이므로
모순이다. 따라서 가능한 쌍은 \(p=q=X\)뿐이다. TICKET-236의 항등식

\[
q_{\rm mod}g_X(N)=M_X-\Delta_X(N)
\]

에 대입하면 phase margin이 정확히 \(g_X(2X)/\pi(X)\)임을 얻는다.
PNT가 \(1/\pi(X)=o(1/\log X)\)를 주며, composite cutoff는 정확히
margin 0을 준다.

### 재현 계산과 한계

\(X=30,31,100,101,1000,1009,10000,10007\)을 사용했다. composite
cutoff 네 개의 표현 수는 0이고 prime cutoff 네 개의 표현 수는 1이다.
각 행에서 \(M_X-\Delta_X(2X)=q_{\rm mod}g_X(2X)\)를 정수로 재구성했다.

이 반례는 두 prime 변수를 \(X\)에서 자르면서 target을 \(2X\)까지
허용한 truncation geometry의 endpoint obstruction이다.
\(N\le(2-\eta)X\)인 고정 buffered bulk, cutoff를 \(N\) 이상으로 잡는
방법, target별 major/minor 분석은 반박하지 않는다. Goldbach 반례도 아니다.

- 폐기한 경로: \(2X\)를 포함하는 닫힌 dyadic window의 uniform
  inverse-log phase margin
- 유지할 경로: upper endpoint를 고정 비율로 제거하고 bulk에서 major gain이
  독립 minor loss를 이기게 함
- 다음 단일 보조정리:
  **BufferedDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack**

## 4. 쌍둥이 소수 트랙

### 이번 선언 명제

**FiniteSupportWelchFloorForDegreeTwoCRTOverlap.**

\(s\)개 atom 위의 확률측도 \(\nu\)와
\(\mathbb E_\nu\phi_i^2=1\)인 실함수 \(\phi_1,\ldots,\phi_m\)에 대해

\[
C_{ij}=\mathbb E_\nu(\phi_i\phi_j),\qquad
E_{m,2}={1\over\binom m2}\sum_{i<j}C_{ij}^2
\]

라 하자. \(r=\min(m,s)\)이면

\[
E_{m,2}\ge {m-r\over r(m-1)}.
\]

모든 \(\phi_i\)가 \(\nu\)-centered이면 \(r=\min(m,s-1)\)로 강화된다.
대각 second moment가 \(\alpha\le C_{ii}\le\beta\)이면

\[
E_{m,2}\ge
\max\left(0,{m\alpha^2/r-\beta^2\over m-1}\right).
\]

따라서 diagonal nondegeneracy 아래 \(m\to\infty\)이고
\(E_{m,2}\to0\)이면 support size가 반드시 무한히 증가한다.

### 논증

\(C\)는 rank가 최대 \(s\)인 positive semidefinite Gram matrix다.
nonzero eigenvalue를 \(\lambda_j\)라 하면

\[
\|C\|_F^2=\sum_j\lambda_j^2
\ge {(\operatorname{tr}C)^2\over r}.
\]

unit diagonal에서는

\[
\|C\|_F^2=m+m(m-1)E_{m,2},
\]

이므로 Welch 하한이 즉시 나온다. centered column은 \(s\)-차원 값공간의
mean-zero hyperplane에 놓여 rank가 \(s-1\) 이하가 된다.
\(\alpha,\beta\)형은 \(\operatorname{tr}C\ge m\alpha\)와
\(\sum_iC_{ii}^2\le m\beta^2\)를 사용한다.

nonconstant Walsh column을 같은 횟수만큼 반복하면 centered 하한을 정확히
달성하므로 상수는 sharp하다.

### 재현 계산과 한계

Walsh equality 행은

\[
(s,m,E_{m,2})=(4,6,1/5),(4,12,3/11),(8,14,1/13),
(8,28,1/9),(16,30,1/29)
\]

이다. 실제 twin-start를 이미 알고 있다는 조건 아래 계산한 행은

| \(X\) | \(m\) | support \(s\) | 표준화 \(E_{m,2}\) | Welch floor |
|---:|---:|---:|---:|---:|
| 100 | 6 | 4 | 0.2099807… | \(1/10\) |
| 200 | 12 | 9 | 0.0919019… | \(1/33\) |
| 300 | 18 | 11 | 0.0934479… | \(7/187\) |

실제 행은 이미 존재하는 twin start에 조건을 걸고 각 coordinate를 표본
second moment로 다시 정규화한 순환적 진단이다. local CRT normalization의
uniform diagonal control, 산술적 \(E_2\) decay, 양의 주항, parity barrier는
모두 미해결이다.

- 폐기한 경로: bounded-support finite sample이 \(E_2\to0\)를 인증할 수
  있다는 해석
- 유지할 경로: support 성장과 diagonal nondegeneracy를 명시적으로 포함한
  prime-weighted degree-two 추정
- 다음 단일 보조정리:
  **PrimeWeightedDegreeTwoCRTDecayWithGrowingSupportAndUniformDiagonalControl**

## Proof DAG와 주장 경계

각 트랙에는 TICKET-237 **closed** 정리 하나, **refuted_or_limited** 경로 하나,
**highest_risk_open** 후속 보조정리 하나, **open_not_proven** 상위 경계가 있다.
기계 판독 DAG와 모든 정확 분수·해시는
data/open-problem/ticket237-angle-palette-endpoint-welch.json에 있다.

유한 계산은 명시된 식과 범위를 재현하는 인증서다. 일반 매개변수 결론은
별도로 적은 선형대수·위수·조합 논증에서만 나온다. 상위 추측 해결 수는
계속 0이다.
