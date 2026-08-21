# TICKET-236: 정규화 contraction, 위수 증인, reflected phase defect, 2차 CRT 환원

상태: `open_not_proven`
생성일: 2026-08-22
상위 추측 해결 수: `0 / 4`

TICKET-236은 TICKET-235가 남긴 네 최고위험 보조정리를 이어서 공격한다.
이번 결과는 네 개의 정확한 부분정리 또는 no-go 정리다. 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않았다. `parent conjecture claims blocked · open_not_proven`.

## 1. 리만 가설 트랙

### 선언 명제

`NormalizedCrossBlockContractionCriterionAndLocalMinorNoGo`.

\(A,C\)가 양의 정부호이고

\[
H=\begin{pmatrix}A&B\\B^*&C\end{pmatrix},\qquad
K=A^{-1/2}BC^{-1/2}
\]

라 하자. 그러면

\[
H\succeq0\iff\|K\|_{op}\le1.
\]

좌표별 상대 (2\times2) minor 조건만으로는 충분하지 않다.
(A=C=I_m, B=(2/m)J_m)이면 모든 좌표 minor는
(1-4/m^2\ge0)이고 각 원소는 0으로 가지만, 전체 normalized norm은
2이고 최소 고유값은 (-1)이다.

### 논증과 계산

\(\operatorname{diag}(A^{-1/2},C^{-1/2})\) 합동변환 뒤 Schur 보완은
\(I-K^*K\)다. 따라서 전체 양성은 정확히 contraction 조건과 동치다.
(J_m)의 유일한 비영 특이값이 (m)이므로 coherent rank-one 반례가
성립한다. (B=J_m/(2m))인 안전족은 norm (1/2), 최소 고유값
(1/2)다. (m=4,8,16,32,64,128)의 유리수 계산이 모든 식을 재현한다.

한계: 실제 Guinand-Weil 산술 꼬리가 아니라 추상 유한 Hermitian form이다.
zeta 영점은 계산하지 않았다.

폐기: 좌표별 상대 minor로 전체 form 양성을 인증하는 경로.
다음 보조정리:
`ArithmeticWeilNormalizedCrossBlockContractionBelowOneOnCofinalLogarithmicFrames`.

## 2. 콜라츠 트랙

### 선언 명제

`BinaryRunBlockThreePrimeOrderWitnessOutside28826Multiples`.

primitive 이진 단어 (w_k=1^k2^{2k})에 대해

\[
D_k=32^k-27^k,\qquad B_k=32^k+27^k-2\cdot18^k.
\]

(28826\nmid k)이면 (D_k)를 나누지만 (B_k)를 나누지 않는 소수를
다음처럼 명시적으로 고를 수 있다.

- (k)가 홀수이면 (q=5),
- (k)가 짝수이고 (58\nmid k)이면 (q=59),
- (58\mid k, 28826\nmid k)이면 (q=57653).

(28826\mid k)이면 세 소수가 모두 (D_k,B_k)를 함께 나누므로 이
고정 palette는 보편 증인이 아니다.

### 논증과 계산

TICKET-235의 공약수 위수 특성화와 다음 정확한 위수표를 사용한다.

\[
\begin{array}{c|ccc}
q&\operatorname{ord}(32/27)&\operatorname{ord}(3/2)&\operatorname{ord}(4)\\
5&1&2&2\\
59&2&58&29\\
57653&29&28826&28826.
\end{array}
\]

완전 주기 (1\le k\le28826)의 선택 수는
(14413,13916,496,1), 모듈러 실패는 0이다. 이는 단순 유한 추세가
아니라 위수로 주기성을 먼저 증명했기 때문에 모든 (k)에 대한 인증이다.

한계: TICKET-197이 run-block의 (D_k\nmid B_k) 자체는 이미 닫았다.
이번 새 결과는 28825개 잔여류의 prime-presence certificate다. 일반 이진
necklace, valuation 3 이상, 비주기 발산은 미해결이다.

폐기: 세 고정 소수가 모든 run-block을 덮는다는 경로.
다음 보조정리:
`UniformBinaryDensityBandFreshOrderSeparatedPrimeWitnessBeyondFinitePalettes`.

## 3. 강한 골드바흐 트랙

### 선언 명제

`ActualPrimeReflectedPhaseDefectIdentityAndUncoupledMarginNoGo`.

\(q>2X\)이고 \(x_X\)가 실제 소수 indicator일 때

\[
M_X=\sum_a|\widehat x_X(a)|^2=q\pi(X)
\]

와 target reflected phase defect

\[
\Delta_X(N)=\sum_a|\widehat x_X(a)|^2
\left[1-\cos\left(2\arg\widehat x_X(a)-\frac{2\pi aN}{q}\right)\right]
\]

를 정의한다. 그러면 (0\le N\le2X)에서

\[
qg_X(N)=M_X-\Delta_X(N).
\]

따라서 \(\Delta_X(N)<M_X\)는 \(g_X(N)>0\)와 정확히 동치다. 또한
cutoff와 target을 결합하지 않은 전 target (1/\log X) margin은
실제 소수에서도 거짓이다. \(N=4\)의 정규화 margin은
\(1/\pi(X)=o(1/\log X)\)다.

### 논증과 계산

순환 convolution의 Fourier 역변환과 Parseval을 적용한다. (q>2X)이므로
wraparound는 없다. 4의 표현은 ((2,2)) 하나뿐이며 PNT가 asymptotic
no-go를 준다. (X=100,1000,10000,100000)의 exact margin은 각각
(1/25,1/168,1/1229,1/9592)다. (X=30,100,300)의 complex DFT 직접
검산 오차는 (5\times10^{-10})보다 작다.

한계: 고정 target과 성장 cutoff를 의도적으로 분리한 반례다.
(N\asymp X)인 target-coupled dyadic 추정은 반박하지 않는다. strict
phase inequality 자체는 Goldbach endpoint와 동치여서 독립 절약이 아니다.

폐기: 결합되지 않은 전 target inverse-log margin 및 raw strict phase
inequality를 더 작은 보조정리로 취급하는 경로.
다음 보조정리:
`TargetCoupledDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack`.

## 4. 쌍둥이 소수 트랙

### 선언 명제

`DegreeTwoCesaroEnergyControlsEveryFixedDegree`.

TICKET-235의 normalized CRT 조건과 (|\psi_i|^2\le2) 아래에서

\[
E_{m,1}\le\sqrt{\frac4m+\frac{m-1}{m}E_{m,2}},
\]

그리고 고정 (k\ge2)에 대해

\[
E_{m,k}\le2^{k-2}E_{m,2}+\frac{2^k(1+k(k-1))}{m}.
\]

따라서 (E_{m,2}\to0) 하나가 1차를 포함한 모든 고정 차수의 소멸을
강제한다.

### 논증과 계산

\(b_i=\mathbb E_\nu\psi_i\),
\(M_{ij}=\mathbb E_\nu(\psi_i\psi_j)\)라 하자. covariance 양성으로
\(M\succeq bb^*\)이고
\(|b|^2\le\|M\|_{op}\le\|M\|_F\)다. 대각항은 2 이하이고 비대각항
제곱평균은 (E_{m,2})이므로 첫 부등식이 나온다. 독립 표본 overlap
\(R\)에는 \(\mathbb E R^2\le4/m+E_{m,2}\), \(|R|\le2\)를 적용하고
TICKET-235의 with/without-replacement bound를 결합한다.

실제 유한 twin-start 행은
((X,m,N)=(10^4,4,202),(10^5,6,1220),(10^6,8,8164))이며 모든 유리수
상계가 통과한다.

한계: 이미 존재하는 twin start에 조건을 건 순환적 유한 진단이다. 실제
Type-II (E_{m,2}\to0), 양의 총질량, parity barrier는 미해결이다.

폐기: 모든 고정 차수를 각각 독립 증명해야 한다는 경로.
다음 보조정리: `PrimeWeightedDegreeTwoCRTOverlapEnergyDecayAtTwinScale`.

## Proof DAG와 주장 경계

각 트랙에는 `closed` TICKET-236 정리 하나, `refuted_or_limited` 경로 하나,
`highest_risk_open` 후속 보조정리 하나, `open_not_proven` 상위 경계가 있다.
기계 판독 DAG는
`data/open-problem/ticket236-contraction-order-phase-degree2.json`에 있다.

유한 계산은 명시된 식과 범위의 재현 인증일 뿐 무한 명제를 대신하지 않는다.
상위 추측 해결 수는 계속 0이다.
