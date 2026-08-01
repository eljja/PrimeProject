# TICKET-172: 구조적 KKT 관성, 콜라츠 다리의 동치성, Fourier L1 양성, dyadic 혼합 변동

## 초록

TICKET-172는 TICKET-171이 남긴 네 목표를 실제 증명 다리로 사용하기 전에
논리적 강도와 최소 반례를 다시 감사한다. 이번 티켓은 정확한 중간정리 네
개를 증명하지만 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측 중 어느 것도 해결하지 않는다.

핵심 개선은 구조 보존이다. saddle-point KKT 행렬은 전체 부정정 행렬의
작은 섭동을 요구하지 않고 primal 블록과 constraint 블록에서 인증할 수
있다. 콜라츠의 자연수 경로 배제 목표는 원 추측과 동치이므로 더 쉬운
다리라고 부를 수 없다. Fourier 역변환은 정확한 Goldbach 양성 조건을
주지만, 양의 4점 함수족은 크기 정보만으로 이 조건을 개선할 수 없음을
보인다. 마지막으로 fine/fine Haar 에너지가 dyadic 혼합 차분과 정확히
같음을 증명해 Twin Type-II 목표를 구체적인 산술 변동 추정으로 바꾼다.

| 문제 | TICKET-172의 정확한 결과 | 상태 | 폐기한 경로 | 다음 단일 보조정리 |
|---|---|---|---|---|
| 리만 | 구조적 KKT 블록 관성 인증 | `open_not_proven` | 전체 상대 KKT 노름 1 미만을 필요조건으로 사용 | `CofinalWeilPrimalBlockPositivityAndConstraintRankCertificate` |
| 콜라츠 | 자연수 지지 잔여 경로와 원 추측의 동치 | `open_not_proven` | 자연수 경로 배제를 Collatz보다 약한 명제로 취급 | `LeastCounterexampleCrossScaleCylinderHeightBound` |
| 골드바흐 | Fourier L1 anchor 인증과 최적성 | `open_not_proven` | shell 크기만으로 보편 점별 하한 개선 | `UniformPrimeSpecificSignedGoldbachFourierCancellationBelowMainTerm` |
| 쌍둥이 소수 | Haar/혼합 변동 항등식과 marginal no-go | `open_not_proven` | 행·열 합 상쇄를 혼합 Type-II 제어로 대체 | `PrimePairMatrixWeightedDyadicMixedVariationPowerSaving` |

## 1. 주장 등급

- `proved_exact`: 표시한 대수적 또는 유한차원 명제를 증명했다.
- `refuted_or_insufficient`: 명시적 반례가 있거나 원 추측과 동치여서 중간 다리로 부족하다.
- `open_not_proven`: 추측을 닫는 무한 정리가 없다.

유한 소수 계수와 유한 콜라츠 재생은 진단일 뿐이다. 유한 계산은 전역
추측의 증명으로 승격되지 않는다.

## 2. 리만 트랙: 구조적 KKT 관성

### 선언 명제

`A`가 `n x n` 양의 정부호 대칭행렬이고 `B`가 행 계수 `r`인 full-row-rank
행렬이면

\[
K=\begin{pmatrix}A&B^T\\B&0\end{pmatrix}
\]

의 관성은 `(n,r,0)`이다. 중심 `A0,B0`와 연산자 노름 반경
`rho_A,rho_B`에 대해

\[
\lambda_{\min}(A_0)>\rho_A,\qquad
\sigma_{\min}(B_0)>\rho_B
\]

이면 해당 구조적 구간 전체에서 같은 관성을 인증한다.

### 증명

정확한 블록 합동변환으로

\[
K\sim\operatorname{diag}(A,-BA^{-1}B^T)
\]

를 얻는다. 첫 블록은 양의 정부호이고 두 번째 블록은 음의 정부호다.
Sylvester 관성 법칙과 Weyl 섭동 부등식이 결론을 준다.

### 필요조건 no-go

`K0=[[1,1],[1,0]]`, `E_t=[[t,0],[0,0]]`로 두면 `t>=2`에서 TICKET-171
전체 상대 노름은 `2t/sqrt(5)>1`이다. 하지만 `det(K0+E_t)=-1`이므로
관성은 계속 `(1,1,0)`이다. 따라서 전체 상대 노름 조건은 충분조건이지
필요조건이 아니다.

남은 간극은 실제 고정 pole-neutral Guinand-Weil form core에서 primal
양성 및 constraint rank margin을 cofinal하게 인증하는 것이다. 이 2x2
예시는 zeta 영점 배제 정리가 아니다.

## 3. 콜라츠 트랙: 계산 전에 동치성 확인

### 선언 명제

accelerated odd map `T`에 대해 다음은 동치다.

1. 모든 홀수 `n>1`은 어떤 반복에서 `n`보다 작아진다.
2. 모든 접두어가 비하강인 무한 잔여 경로 중 양의 자연수가 지지하는 경로가 없다.
3. 모든 양의 정수는 `1`에 도달한다.

양의 자연수 지지 비하강 경로는 정확히 `T^j(n)>=n`을 모든 `j`에서
만족하는 `n>1`의 valuation itinerary다. 따라서 1과 2는 같은 반례를
배제한다. 1에서 3은 `n`에 대한 강한 귀납법으로 나오며 3에서 1은 즉시
따른다.

즉 TICKET-171의 다음 목표는 더 쉬운 중간정리가 아니라 Collatz의 동치
재진술이었다.

### 유한 접두어 판정 no-go

모든 `H`에 대해 `n_H=2^(H+1)-1`은 첫 `H`개의 valuation이 모두 1이고

\[
T^H(n_H)=2\cdot3^H-1>n_H
\]

이다. 같은 접두어에는 다음 두 연장이 있다.

- 계속 1을 선택해 2-adic `-1`로 가는 유령 경로
- `n_H`의 실제 자연수 궤도. 다음 valuation은 `1+v2(3^(H+1)-1)>1`

따라서 고정된 유한 접두어로 natural support를 판정할 수 없다. 계산은
`3`부터 `100,000`까지 홀수 49,999개의 first descent를 확인했지만 이는
유한 진단이다.

다음 목표는 가상의 최소 반례 높이에 대한 horizon-independent
Archimedean 상계다.

## 4. 골드바흐 트랙: 정확한 Fourier 점별 양성 조건

실함수 `g`의 정규화 Fourier 계수에 대해 역변환과 삼각부등식은

\[
g(x)\ge \widehat g(0)-\sum_{k\ne0}|\widehat g(k)|
\]

을 준다. 따라서 비영 주파수 L1 예산이 0주파수 anchor보다 작으면 모든
점에서 엄밀히 양수다.

`Z/4`에서

\[
\widehat g_+=(1,\varepsilon/2,\varepsilon,\varepsilon/2),\quad
\widehat g_-=(1,\varepsilon/2,-\varepsilon,\varepsilon/2)
\]

는 같은 크기 profile을 갖는다. 비영 L1 예산은 `2 epsilon`이고
`min g_-=1-2 epsilon`이 하한을 정확히 달성한다. 따라서 크기만 사용하는
보편 인증은 이 하한보다 강해질 수 없다. 이 함수족은 소수 지지 Goldbach
반례가 아니다.

64, 128, 256, 512개 연속 짝수에 대한 실제 ordered prime-pair 계수는
모두 양수였지만 일반 L1 하한은 음수였다. 남은 정리는 각 짝수 target에
대한 소수 산술 부호 상쇄다.

## 5. 쌍둥이 소수 트랙: 혼합 변동 좌표

`2x2` 블록의 separable orthonormal Haar fine/fine 계수는

\[
d=(a_{00}-a_{01}-a_{10}+a_{11})/2
\]

이다. 따라서 fine/fine 에너지 합은 혼합 차분 제곱합의 정확히 `1/4`이다.
정규화 coarse 블록에 재귀 적용하면 모든 dyadic scale에서 같은 항등식을
얻는다.

이 항등식은 TICKET-161의 네 Type-II 행렬과 TICKET-171의 변환 에너지를
모두 재현했다. 반면 교대 checkerboard는 모든 행·열 합이 0이지만
fine/fine 에너지가 전체 Frobenius 에너지 `N^2 a^2`와 같다. 1차원
marginal 상쇄는 혼합 변동 감쇠를 주지 않는다.

다음 목표는 sieve 해상도와 함께 증가하는 범위에서 prime-pair matrix의
가중 dyadic 혼합 변동에 power saving을 증명하는 것이다.

## 6. 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket172_structure_equivalence_l1_variation.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket172_structure_equivalence_l1_variation -v
```

주 기계 판독 산출물은
`data/open-problem/ticket172-structure-equivalence-l1-variation.json`이다.

## 7. 문헌 경계

- Connes와 Consani, *The Scaling Hamiltonian*, [arXiv:1910.14368](https://arxiv.org/abs/1910.14368): Weil 양성과 연산자 관점.
- Ernvall-Hytonen 외, *A finite Guinand-Weil dictionary and archimedean tail order*, [arXiv:2607.02828](https://arxiv.org/abs/2607.02828): 유한 Guinand-Weil 맥락.
- Tao, *Almost all orbits of the Collatz map attain almost bounded values*, [arXiv:1909.03562](https://arxiv.org/abs/1909.03562): almost-all first-passage 결과.
- Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*, [arXiv:2605.13886](https://arxiv.org/abs/2605.13886): 전역 Collatz 주장이 없는 유한 parity-vector 결과.
- Grimmelt와 Bhowmik, *The exceptional set of the Goldbach problem*, [arXiv:2607.27282](https://arxiv.org/abs/2607.27282): exceptional set 및 명시적 major-arc 맥락.
- Ford와 Maynard, *On the theory of prime producing sieves*, [arXiv:2407.14368](https://arxiv.org/abs/2407.14368): prime-producing sieve와 Type-II 정보.

이 문헌들은 연구 경계를 제공한다. 표준 Schur complement, Fourier 역변환,
강한 귀납법, Haar 항등식에 대해 PrimeProject의 우선권이나 신규성은
주장하지 않는다.
