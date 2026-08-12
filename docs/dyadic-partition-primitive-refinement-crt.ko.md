# TICKET-220: 이진 분할, 원시 단어 폐쇄, 정제 안정성, 유한 휠 CRT 한계

## 주장 상태

TICKET-220은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 **증명하거나 반증하지 않았다**. 대신 범위가 정확히 제한된 네
정리를 증명하고, 과도한 네 증명 경로를 폐기하며, 각 난제에서 다음에
증명해야 할 보조정리 하나를 지정한다. 기계 판독 해결 수는 계속 `0`이다.

이번에 확정한 결과는 다음과 같다.

1. 리만 결함용 이진 라플라스 대역 커널의 합은 전체 결함 중복도를 정확히
   복원하지만, 유한 대역 창은 충분히 멀리 있는 결함 원자를 놓친다.
2. TICKET-219의 콜라츠 단일 봉우리 배제는 그 원시 단어의 모든 순환 이동과
   양의 거듭제곱으로 확장된다.
3. 교차 적합 골드바흐 지지집합 인증은 정확한 Minkowski 여유가 양수이면
   fold를 더 세분해도 유지된다.
4. 모든 고정 유한 쌍둥이 휠의 모든 허용 잉여류 안에는 두 수가 모두
   합성수인 무한 CRT 수열이 존재한다.

각 명제는 선언한 가정 안에서 정확하다. 그러나 어느 명제도 혼자서 남은
무한 범위 또는 parity 장벽을 건너지 못한다.

## 1. 리만 트랙

### 선언 명제

(C)를 ((0,\infty)) 위의 음이 아닌 정수값 국소 유한 측도라 하고

\[
L(s)=\int_0^\infty e^{-st}\,dC(t)
\]

로 둔다. (H>0), (j\in\mathbb Z)에 대해

\[
W_j(H)=L(2^{-j}/H)-L(2^{1-j}/H)
\]

를 정의하면

\[
\sum_{j=-M}^{N}W_j(H)
=L(2^{-N}/H)-L(2^{M+1}/H)
\]

이고, 단조 수렴으로

\[
\sum_{j\in\mathbb Z}W_j(H)=C((0,\infty))
\]

를 얻는다. 값 (+\infty)도 허용한다. 또한 임의의 유한 지수 집합 (J)와
(\varepsilon>0)에 대해

\[
\sum_{j\in J}W_j(H)<\varepsilon
\]

가 되도록 원자 하나를 배치할 수 있다. 따라서 유한 개 대역값만으로
(C=0)을 인증할 수 없다.

### 증명

고정된 (t>0)에서 (j)번째 커널은

\[
k_j(t)=e^{-2^{-j}t/H}-e^{-2^{1-j}t/H}\ge0
\]

이다. 유한 합은 망원합이 된다. (N\to\infty)이면 첫 경계 지수함수는
1로, (M\to\infty)이면 둘째 경계 지수함수는 0으로 간다. 따라서
(\sum_jk_j(t)=1)이고, Tonelli 정리로 이 등식을 (C)에 적분할 수 있다.

유한 (J)를 고정하면 모든 (k_j(t))는 (t\downarrow0)과
(t\to\infty)에서 0으로 간다. 유한 합도 마찬가지이므로 관측 스케일보다
충분히 아래나 위에 원자를 두면 관측 질량을 임의로 작게 만들 수 있다.

### 재현 계산

여섯 합성 원자에 대해 (M=N\in\{2,4,8,12,16\})인 망원합을 100자리
십진 정밀도로 확인한다. 또 (2^{-40}), (2^{40})에 원자를 두고
(-4\le j\le4) 창에서 보이는 질량이 각각 (10^{-6}) 미만임을 확인한다.
이 계산은 정리를 재현할 뿐 실제 제타 영점에 대한 증거가 아니다.

### 폐기 경로와 남은 간극

**폐기:** 고정된 유한 이진 결함 대역만으로 전역 리만 가설을 인증한다.

**유지:** 엄밀한 소수 측 상계 (U_j\ge W_j)와 꼬리 상계를 구성하여

\[
\sum_{j\in\mathbb Z}U_j<1
\]

을 보이면 전체 결함 수의 정수성 때문에 결함은 0이어야 한다.

**다음 보조정리:** `PrimeSideSummableDyadicBandpassEnvelopeBelowOne`.

TICKET-220은 실제 소수 측 가합 포락을 구성하지 못했다.

## 2. 콜라츠 트랙

### 선언 명제

(u)가 (k,m\ge1)인 이진 가속 콜라츠 valuation 단어 (1^k2^m)의 순환
이동이라고 하자. 어떤 (r\ge1)에 대해서도 (u^r)을 valuation 단어로
갖는 양의 가속 콜라츠 주기는 존재하지 않는다.

### 증명

가정한 주기를 (u) 한 묶음의 시작점에 맞춘다. 한 묶음은

\[
f(n)=\frac{An+B}{D},\qquad A=3^h,\quad D=2^S
\]

인 유리 affine 사상으로 작용한다. 소인수분해의 유일성으로 (A\ne D)다.
(r)개 묶음이 닫히면 (f^r(n)=n)이다. (a=A/D>0)라 쓰면

\[
f^r(n)-n=(f(n)-n)(1+a+\cdots+a^{r-1})
\]

이다. 두 번째 인수는 양수이므로 (f(n)=n)이다. 이는 TICKET-219가
배제한 양의 단일 봉우리 주기와 모순이다. 순환 이동은 같은 주기에서
시작점만 바꾼다.

### 재현 계산

대표 원시근과 거듭제곱에 대해 정수 삼중항 ((A,B,D))를 정확히 합성하고,
합성 및 고정점 항등식을 검사한다. 길이 2부터 16까지 모든 이진 단어를
원시근과 순환 전이 횟수로 분류한다. 유한 열거는 일관성 검사이고, 무한
족의 증명은 affine 논증이 담당한다.

### 폐기 경로와 남은 간극

**폐기:** 단일 봉우리 단어의 순환 이동이나 반복을 독립적인 새 주기
후보로 계속 열거한다.

**새로 닫힌 무한 족:** 모든 단일 봉우리 원시근의 모든 양의 거듭제곱과
순환 이동. 표시상 run 수가 임의로 커질 수 있지만 비원시 단어에 한한다.

**남은 간극:** 원시 다중 run valuation 단어와 비주기 발산 궤도.

**다음 보조정리:** `EffectiveBakerSeparationForPrimitiveMultiRunValuationWords`.

## 3. 강한 골드바흐 트랙

### 선언 명제

(F'\subset F)를 더 세분된 holdout fold라 하자. (F) 바깥에서 양의
모형 scale (\alpha)를, (F') 바깥에서 양의 scale (\beta)를 적합한다.
개수 (A_i), 양의 가중치 (w_i), 잔차 (e_i(\gamma)=A_i-\gamma w_i)에
대해

\[
\|e(\beta)\|_{\ell^p(F')}
\le
\|e(\alpha)\|_{\ell^p(F')}
+|\alpha-\beta|\,\|w\|_{\ell^p(F')}
\]

이다. 우변이 (\beta\min_{i\in F'}w_i)보다 작으면 (F') 위 모든 개수는
양수다.

### 증명

좌표별 항등식

\[
e_i(\beta)=e_i(\alpha)+(\alpha-\beta)w_i
\]

에 Minkowski 부등식을 적용한다. holdout 좌표 (j)에서 (A_j=0)이면

\[
|e_j(\beta)|=\beta w_j\ge\beta\min_{i\in F'}w_i
\]

이므로 엄격한 상계와 모순이다.

### 재현 계산

(X\in\{128,512,2048,8192,32768\})인 다섯 이진 블록에서 정확한 골드바흐
표현 수와 mod (2,4,8,16) 잉여 fold를 사용한다. 최소제곱 scale은 정확한
유리수다. 8제곱근은 (10^{-12}) 단위 유리수로 바깥쪽 반올림하므로 보고한
엄격 통과는 유한 데이터에 대해 엄밀하다.

- 직접 (p=8) 지지집합 인증: `150 / 150` fold
- 직접 (p=4) 지지집합 인증: `137 / 150` fold
- 중첩 정제 다리 (2\to4\to8\to16): `140 / 140`
- 가장 큰 인증 다리/장벽 비율: 약 `0.9670275612`

### 폐기 경로와 남은 간극

**폐기:** 유한 개의 점점 세밀한 fold 성공을 공종 골드바흐 증명으로
승격한다.

**유지:** 정제 부등식을 두 해석적 입력의 접점으로 사용한다. 필요한 입력은
공종 부모 잔차 상계와 scale 재적합 이동량 상계다.

**다음 보조정리:**
`CofinalCrossFitRefinementMarginWithoutRepresentationEnumeration`.

현재 감사는 실제 표현 수를 읽으므로 충분히 큰 모든 짝수의 표현 존재를
증명하지 못한다.

## 4. 쌍둥이 소수 트랙

### 선언 명제

(W)가 제곱인수가 없는 수이고 (a\pmod W)가
(\gcd(a(a+2),W)=1)을 만족한다고 하자. (n\equiv a\pmod W)이면서 (n)과
(n+2)가 모두 합성수인 (n)이 무한히 많다.

### 증명

(W)를 나누지 않는 서로 다른 소수 (q,r)을 고른다. 중국인의 나머지
정리(CRT)는

\[
n\equiv a\pmod W,\qquad n\equiv0\pmod q,\qquad n\equiv-2\pmod r
\]

를 동시에 푼다. 모든 해는 mod (Wqr)인 하나의 등차수열이다. 충분히 큰
항에서 (q)는 (n)의 진약수이고 (r)은 (n+2)의 진약수다. 동시에 원래
허용 휠 잉여류는 그대로 유지된다.

### 재현 계산

(W=30,210,2310,30030,510510)에 대해 정확한 CRT 증인을 생성한다. 각 행은
허용성, 두 진합성수 약수, 전체 등차수열의 합동 보존을 확인한다.

### 폐기 경로와 남은 간극

**폐기:** 고정 유한 휠을 통과했다는 사실만으로 쌍둥이 소수 한 쌍 또는
무한성을 인증한다.

**한계 범위:** 고정 유한 국소 나눗셈 정보만 배제한다. 성장하는 체,
쌍선형 형식, 분포 추정 또는 다른 전역 정보는 배제하지 않는다.

**다음 보조정리:** `ParitySensitiveBilinearLowerBoundBeyondEveryFiniteWheel`.

## 증명 DAG 요약

| 문제 | 닫힌 TICKET-220 노드 | 폐기한 경로 | 최고 위험 미해결 노드 |
|---|---|---|---|
| 리만 | `DyadicLaplacePartitionAndFiniteWindowNoGo` | 유한 창이 전역 결함 부재를 인증 | `PrimeSideSummableDyadicBandpassEnvelopeBelowOne` |
| 콜라츠 | `PrimitiveRootExtensionOfSingleMountainExclusion` | 반복근이 새 고정점을 생성 | `EffectiveBakerSeparationForPrimitiveMultiRunValuationWords` |
| 골드바흐 | `CrossFitPartitionRefinementStabilityCertificate` | 유한 정제가 공종 정리를 함의 | `CofinalCrossFitRefinementMarginWithoutRepresentationEnumeration` |
| 쌍둥이 소수 | `FiniteWheelTwinCertificationCRTNoGo` | 고정 휠 통과가 쌍둥이를 인증 | `ParitySensitiveBilinearLowerBoundBeyondEveryFiniteWheel` |

모든 최종 추측 노드는 계속 `open_not_proven`이다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket220_dyadic_partition_primitive_refinement_crt.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket220_dyadic_partition_primitive_refinement_crt -v
```

주 기계 판독 감사 파일:

`data/open-problem/ticket220-dyadic-partition-primitive-refinement-crt.json`

감사 파일은 정확한 명제, 증명문, 계산 행, 가능한 경우 SHA-256 실행 기록,
증명 DAG, 폐기 경로, 남은 간극, 상위 추측 해결 수 0을 함께 기록한다.
