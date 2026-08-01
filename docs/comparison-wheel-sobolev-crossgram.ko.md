# TICKET-177: 비교 우세행렬, Collatz 6-휠, Sobolev 인증, 부호 있는 교차 Gram

## 주장 경계

TICKET-177은 정확한 부분정리 또는 no-go 명제 네 개를 증명했습니다. 그러나
리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않았습니다. 네 상태는 모두 `open_not_proven`이며, 기계
검사에서 해결 수와 실패 수는 모두 0입니다.

| 문제 | 이번에 확립한 결과 | 폐기한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | 하나의 고정 상대 기저에서 성립하는 성분별 비교 우세행렬 인증 | 계산 후 맞춘 가중치와 대각선만의 꼬리 요약 | `PoleNeutralWeilWhitenedTailHasPredeclaredComparisonMajorantBelowCoreMargin` |
| 콜라츠 | 첫 가속 단계 이후의 정확한 6-휠 조화 포락선 | 홀수 간격 또는 mod 3 배제를 필요충분조건으로 해석 | `AperiodicNonDescendingValuationDiscrepancyExceedsSixWheelHarmonicEnvelope` |
| 골드바흐 | 에너지와 도함수로 점별 양성을 보증하는 정리 | 에너지 단독 사용과 시험한 비평활 전역 인증 | `ParityAliasedMinorHasMultiscaleEnergyDerivativePowerSavingBelowMajorMain` |
| 쌍둥이 소수 | 부호 있는 교차 Gram 항등식과 정보 손실 반례군 | 비음수 블록 노름을 상쇄의 충분통계로 사용 | `PrimePairHaarSignedCrossGramHasPowerSavingRelativeToDiagonalEnergy` |

## 1. 리만 가설: 미리 정한 상대 비교 우세행렬

### 선언 명제

`G`가 양의 정부호이고 `A_T,A`가 Hermitian 행렬이라고 하자.
`A_T >= delta G`라 하고, 하나의 고정된 `G`-정규직교 기저에서

```text
E = G^(-1/2)(A-A_T)G^(-1/2)
```

라 쓰자. 대칭 비음수 행렬 `M`이 모든 성분에서 `|E_ij| <= M_ij`를
만족하면

```text
A >= (delta-rho(M))G
```

가 성립한다. 미리 정한 모든 양의 가중치 `w`에 대해서도

```text
rho(M) <= max_i (Mw)_i/w_i
```

이다.

### 증명과 no-go

모든 벡터 `x`에 대해 성분별로 `|Ex| <= M|x|`이므로
`||E||_2 <= ||M||_2 = rho(M)`이다. 따라서 변분원리에 의해
`E >= -rho(M)I`이고, whitening을 되돌리면 명제가 성립한다.

가중 행 합 상계는 대각 스케일링한 Collatz-Wielandt 비교이다. 그러나
기약행렬 `M`에 대해 모든 양의 가중치를 자유롭게 최적화한 하한은 정확히
`rho(M)`이다. 즉 데이터를 본 뒤 가중치를 맞추는 방법은 미지의 spectral
target을 다시 계산하는 순환 논증이다. 산술적 비교행렬과 가중치는 꼬리를
보기 전에 해석적으로 선언되어야 한다.

재현 가능한 삼중대각 비교모형에서는 `delta=0.25`,
`rho(M)=0.1785640646`, 인증된 상대 여유는 `0.0714359354`이다. 가장 작은
metric scale을 `10^-4`에서 `10^-128`까지 바꾸어도 상대 여유는 양수다.
이는 비교 정리의 검증이지 실제 Weil 꼬리 전제의 증명이 아니다.

### 남은 간극

pole-neutral arithmetic Weil 꼬리를 whitening한 뒤 모든 성분을 지배하면서,
독립적으로 인증한 고정 core 여유보다 spectral radius가 작은 명시적 대칭
비음수 비교행렬을 아직 만들지 못했다.

## 2. 콜라츠 추측: 첫 단계 뒤에는 6-휠을 사용한다

### 선언 명제

가속 홀수 사상

```text
T(n) = (3n+1)/2^v2(3n+1)
```

에서 첫 단계 이후의 모든 상태는 홀수이며 3의 배수가 아니다. 궤도가
비주기이고 시작 홀수 `n` 아래로 내려가지 않는다면, 첫 `h`개의 상태는 서로
다른 6-휠 원소다. 따라서 affine 보정항의 조화 포락선에서 로그 계수는
TICKET-176의 홀수 전용 `1/(6 ln 2)`에서

```text
1/(9 ln 2)
```

로 줄어들며, 그 비율은 정확히 `2/3`이다.

### 증명과 no-go

가속 사상의 출력은 정의상 홀수다. 또한 `3n+1`은 mod 3에서 1이고 2의
거듭제곱으로 나누어도 0이 되지 않으므로 출력은 3의 배수가 아니다.
비주기성 때문에 상태들은 서로 다르다. 정렬했을 때 시작점 위의 `j`번째
6-휠 후보는 적어도 `n+3j-2`이므로, `log2(1+x) <= x/ln 2`와 적분 상계를
적용하면 더 날카로운 포락선을 얻는다.

하지만 mod 3 배제는 하강의 필요충분조건이 아니다. `3`부터 `100,000`까지
홀수 시작점 `49,999`개는 유한 검사에서 모두 하강했지만, `63`은 더 날카로운
충분 포락선을 넘지 않고 34단계에서 하강한다. 6-휠은 밀도 손실을 줄일 뿐
모든 궤도의 하강을 강제하지 않는다. 비자명 주기도 별도로 배제해야 한다.

### 남은 간극

모든 비주기 비하강 자연수 궤도의 중심화 valuation discrepancy가 6-휠
조화 포락선을 반드시 넘는다는 정리가 없다.

## 3. 강한 골드바흐: 에너지에서 점별 양성으로 가는 엄밀한 다리

### 선언 명제

`P`가 평균 0인 실수값 1-주기 함수이고

```text
||P'||_infinity <= D,       integral_0^1 |P|^2 = E
```

라 하자. `A>0`에 대해 다음 둘 중 하나가 성립하면 모든 `x`에서
`A+P(x)>0`이다.

```text
A > D/2
```

또는

```text
E < A^3/(4D)       (D>0).
```

parity alias를 적용한 삼각다항식 `P(x)=sum d_k exp(2 pi i kx)`에서는
Parseval 항등식으로 `E=sum |d_k|^2`이고,
`D <= 2 pi sum |k d_k|`를 계산할 수 있다.

### 증명과 no-go

원 위의 최단거리는 최대 `1/2`이므로 도함수 상계와 평균 0에서
`min P >= -D/2`가 되어 첫 조건을 얻는다. 만약 어떤 `x_0`에서
`P(x_0)<=-A`라면 Lipschitz 연속성 때문에 길이가 적어도 `A/D`인 원형
구간에서 `|P|>=A/2`다. 따라서 `E>=A^3/(4D)`이고, 대우로 두 번째 조건이
증명된다.

소수 support `64,128,256,512,1024`의 raw fixed-Farey 실험은 이 전역
인증을 `0/5`만 통과했다. 이는 강한 골드바흐의 반례가 아니라 현재 스케일링
경로의 실패다. `P_k(x)=-a cos(2 pi kx)` 반례군은 주파수가 달라도 에너지는
같고 음의 점별 진폭은 남으므로 `L2` 에너지 단독으로 양성을 증명할 수
없음도 보여준다.

### 남은 간극

모든 짝수 표적에 대해 aliased minor의 에너지와 도함수 예산을, 독립적으로
증명한 major-arc 하한보다 충분히 작게 만드는 다중스케일 산술 상계가 없다.

## 4. 쌍둥이 소수: 부호 있는 교차 Gram 정보가 필요하다

### 선언 명제

정의역과 공역이 맞는 연산자 `T_1,...,T_m`에 대해

```text
||sum_j T_j||^2 = ||sum_(i,j) T_i^* T_j||
```

이다. 그러므로 각 성분 노름 `||T_j||`만으로 합의 노름은 결정되지 않으며,
scale 사이의 상쇄를 측정하려면 부호와 위상을 보존한 교차 Gram 연산자가
필요하다.

### 증명과 no-go

`(sum_j T_j)^*(sum_j T_j)`를 전개하고 `||T||^2=||T^*T||`를 적용하면
항등식이 바로 나온다. `[I,I]`, `[I,-I]`, 서로 직교하는 두 projection은
모두 성분 노름 요약이 `(1,1)`이지만 합의 노름은 각각 `2`, `0`, `1`이다.
같은 비음수 블록 노름 자료가 완전 정렬, 완전 상쇄, 직교를 모두 허용한다.

감사한 TICKET-161 Type-II 행 네 개에는 signed cross-Gram 자료가 없다.
따라서 기존 블록 노름은 상계에는 쓸 수 있지만 power saving에 필요한
상쇄를 인증하지 못한다.

### 남은 간극

실제 prime-pair Haar 블록의 비대각 signed cross-Gram 항에 대해 대각
에너지보다 power saving이 생긴다는 산술 데이터와 정리가 없다.

## 증명 DAG와 유한 계산의 경계

네 트랙의 기계 판독 의존성은 모두 다음과 같다.

```text
REFUTED_OR_INSUFFICIENT -> PROVED_EXACT -> OPEN_NOT_PROVEN
```

가운데 노드는 부분정리 또는 no-go 정리이며 난제 해결 노드가 아니다. 유한
계산은 항등식을 검증하고, 부족한 통계량을 반박하며, 명시한 범위에서 반례를
탐색한다. 유한 범위를 무한 명제의 증명으로 승격하지 않는다.

## 최신 1차 문헌과의 경계

- 최근 [절단 Weil-form 수치 연구](https://arxiv.org/abs/2605.20224), [유한 Guinand-Weil 꼬리 제어](https://arxiv.org/abs/2607.02828), [연산자 실험](https://arxiv.org/abs/2607.24830)은 여기서 요구한 RH 비교 우세행렬을 증명하지 않는다.
- [Tao의 거의 모든 수에 대한 Collatz 정리](https://arxiv.org/abs/1909.03562)는 모든 궤도의 6-휠 경계 교차를 주지 않는다.
- 최근 [Goldbach 예외집합 연구](https://arxiv.org/abs/2607.27282)는 모든 짝수 표적에 대한 균일한 이항 minor-arc 점별 상계를 제공하지 않는다.
- [Ford와 Maynard의 체 연구](https://arxiv.org/abs/2407.14368)는 블록 노름만이 아니라 진짜 Type-I/II 정보가 필요함을 보여주는 관련 경계다.

## 재현

```powershell
python scripts/ticket177_comparison_wheel_sobolev_crossgram.py
python -m unittest tests.test_ticket177_comparison_wheel_sobolev_crossgram -v
```

기계 판독 파일:

```text
data/open-problem/ticket177-comparison-wheel-sobolev-crossgram.json
data/open-problem/riemann/rh-ticket-177-comparison-majorant.json
data/open-problem/collatz/co-ticket-177-six-wheel-envelope.json
data/open-problem/goldbach/gb-ticket-177-sobolev-certificate.json
data/open-problem/twin-prime/tp-ticket-177-signed-crossgram.json
```
