# TICKET-216: 라플라스 결함, 교차 거듭제곱 GCD, 진법 히스토그램, 타우버 꼬리

## 주장 경계

TICKET-216은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 **증명하거나 반증하지 않았다**. 이번 티켓은 네 개의 더 작은
명제를 증명하고, 네 개의 잘못된 승격 경로를 폐기하며, 문제마다 다음에
증명해야 할 산술 보조정리 하나를 남긴다. 기계 판독 해결 개수는 0이다.

이번 작업의 목적은 유한 계산 범위를 단순히 늘리는 것이 아니다. 각
변환이나 환원이 상위 난제에 영향을 주려면 실제로 넘어야 하는 첫 이산
임계값을 드러내는 데 있다.

| 문제 | 이번 티켓의 정확한 결과 | 폐기한 경로 | 남은 간극 | 다음 보조정리 |
| --- | --- | --- | --- | --- |
| 리만 | `OffLineDefectLaplaceFirstAtomCertificateAndFixedToleranceNoGo` | 고정된 양의 변환 허용오차 | 실제 제타에 대한 첫 원자 임계값 미만의 공종 상계 | `CofinalActualZetaOffLineLaplaceUpperBoundsBelowFirstAtomThreshold` |
| 콜라츠 | `SingleMountainCrossPowerGCDNecessityAndFiniteDiagonalAudit` | 유한 GCD 감사만으로 전체 증명 | 모든 `k`의 엄격한 GCD 간극과 다중 run 확장 | `UniformStrictCrossPowerGCDGapAtEverySingleMountainCrossing` |
| 골드바흐 | `RadixSelectorFullRepresentationHistogramAndPrecisionDepthNoGo` | 무손실 인코딩을 산술 증명으로 승격 | 모든 블록에서 0번 자릿수를 분리하는 독립 구간 | `ArithmeticRadixSelectorIntervalSeparatesTheZeroDigitOnEveryDyadicBlock` |
| 쌍둥이 소수 | `QuantitativeAbelCountBracketAndFixedDilationTailNoGo` | 고정 배율 꼬리로 쌍둥이 규모 질량 전달 | 적응형 꼬리를 넘는 패리티 민감 아벨 하한 | `ParityBreakingAbelLowerBoundDominatesAdaptiveGeometricTail` |

## 1. 리만 가설: 첫 원자 검출 변환

### 이번에 증명한 명제

경계에 영점이 없는 높이 `T`에서 `N(T)`를 모든 비자명 영점 수,
`M(T)`를 임계선 위 영점 수라고 하자. 둘 다 중복도를 센다. 다음을 둔다.

```text
D(T) = N(T) - M(T),        C(T) = D(T)/2
```

임계선 영점은 `N`과 `M`을 함께 증가시킨다. 임계선 밖 영점은 임계선에
관한 반사 영점과 쌍을 이루므로, `C`는 임계선 밖 대칭쌍을 세는 음이 아닌
정수값 비감소 계단함수다. `0<r<1`에서

```text
L(r) = integral r^t dC(t)
```

로 두면 모든 `H`에 대해

```text
C(H) r^H <= L(r)
```

이다. 따라서 엄밀한 상계 `U(r)<r^H`를 얻으면 높이 `H` 이하에는 임계선
밖 영점이 없다. `H`가 무한히 커지는 공종 인증을 얻으면 리만 가설이
따른다.

### 논증

`t<=H`에 있는 `dC`의 각 원자는 질량이 최소 1이고 가중치는
`r^t>=r^H`다. 이를 더하면 부등식이 나온다. `U(r)<r^H`이면
`C(H)<1`이고, `C(H)`가 정수이므로 `C(H)=0`이다. 공종 높이열은 가능한
모든 유한 세로좌표를 배제한다.

높이 `H`에 대칭쌍 하나가 있으면 정확히 `r^H`를 기여하므로 임계값은
날카롭다.

### 폐기한 경로와 한계

고정된 양의 허용오차는 리만 가설을 증명할 수 없다. 임의의
`epsilon>0`에 대해 논리적 대칭쌍 하나를 충분히 높은 곳으로 보내면 그
변환 기여를 `epsilon`보다 작게 만들 수 있다. 생성기는 `r=1/2`에서 이를
정확한 유리수로 검증한다. 이 지연 원자는 실제 제타 영점이 아니라
고정-허용오차 추론을 반박하는 논리 모형이다.

PrimeProject는 아직 실제 제타 변환 상계를 만들지 못했다. Platt와
Trudgian은 구간 산술로 높이 `3*10^12`까지 리만 가설을 엄밀하게
검증했다. 이번 티켓은 그 높이를 재현하거나 확장하지 않는다
([Bulletin of the London Mathematical Society](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/blms.12460)).

## 2. 콜라츠: 정확한 교차 거듭제곱 GCD 필요조건

### 이번에 증명한 명제

순환 valuation 단어가 `1^k 2^m`인 양의 가속 콜라츠 주기를 생각하자.

```text
Delta = 2^(k+2m) - 3^(k+m) > 0
C     = 3^k - 2^k
E     = 4^m - 3^m
```

TICKET-215는 정수 주기 닫힘이 `Delta|C`를 강제함을 증명했다. 이번에는
이를 다음 정확한 필요조건으로 강화했다.

```text
Delta = gcd(C,E) = gcd(3^k-2^k, 4^m-3^m)
```

### 논증

다음 정수 항등식이 성립한다.

```text
Delta = 2^k E - 3^m C
```

따라서 `gcd(C,E)|Delta`다. 반대로 `Delta|C`이고 같은 항등식에서
`Delta|2^k E`를 얻는다. `Delta`는 홀수이므로 `Delta|E`다. 따라서
`Delta|gcd(C,E)`이고 두 수는 같다.

### 계산과 한계

`1<=k<=4096`의 각 `k`에 대해 생성기는 `Delta>0`이 되는 첫 번째이자
유일한 후보 `m`을 찾고, 임의 정밀도 정수로 두 거듭제곱 차와 GCD를
계산했다. GCD 등식 후보는 0개다. 실행 전사 해시는 JSON에 저장된다.

이는 한 개의 1-run과 한 개의 2-run으로 된 단어족에 대한 유한 배제다.
모든 `k`, 다중 run, 2보다 큰 valuation, 비주기 발산을 다루지 않는다.
다음 정리는 모든 첫 양의 교차점에서 엄격한 GCD 간극을 증명해야 한다.
초월수론과 디오판토스 근사는 콜라츠 주기 하한에 사용된 바 있지만 이
새로운 모든-`k` 명제를 자동으로 주지는 않는다. 배경은 Simons와 de
Weger의 연구를 참조한다
([Acta Arithmetica 기록](https://eudml.org/doc/278746)).

## 3. 강한 골드바흐: 선택자 하나가 전체 히스토그램을 담는다

### 이번에 증명한 명제

`B`개의 짝수로 된 유한 블록에서 `A_i`를 각 짝수의 골드바흐 표현 수라고
하자. `b=B+1`, `U=max A_i`로 두고

```text
h_a = A_i=a인 대상의 개수
E   = sum_i b^(-A_i)
```

로 정의한다. 그러면

```text
b^U E = sum_(a=0)^U h_a b^(U-a)
```

이다. `0<=h_a<=B<b`이므로 이 정수의 `b`진법 자릿수는 표현 수의 전체
히스토그램을 정확히 복원한다. 첫 자릿수 `h_0`은 골드바흐 예외 수이고,
뒤 자릿수는 가장 표현이 적은 대상부터 모든 중복도 층을 기록한다.

### 논증

`E`에서 같은 지수를 묶고 `b^U`를 곱한다. 각 히스토그램 계수는 이미
유효한 `b`진법 자릿수이므로 올림이 발생하지 않는다. 유한 진법 표현의
유일성으로 정확한 복원이 성립한다.

생성기는 시작점 `128, 512, 2048, 8192, 32768`인 이진 블록의 전체
히스토그램을 복호화했다. 예외 자릿수는 모두 0이며, 압축 정수는 비트
길이와 SHA-256 해시로 저장한다.

### 폐기한 경로와 한계

이 결과는 무손실 인코딩이지 새로운 산술 추정이 아니다. 정확한 표현
수에서 출발한다. 또한 `[1,M]`과 `[1,M+1]`은 히스토그램이 다르지만
선택자 차이는

```text
(b-1)/b^(M+1)
```

뿐이다. 따라서 고정 절대 정밀도로는 깊이가 무한히 커지는 히스토그램을
복원할 수 없다. 남은 정리는 미래의 모든 블록에서 0번 자릿수가 없음을
독립적으로 인증하는 산술 구간 추정이다. 예외집합 정리는 예외집합을
공집합으로 만들지 않는다. 이번 티켓은 원방법을 개선하지 않는다. 배경은
Li의 예외집합 논문을 참조한다
([Quarterly Journal of Mathematics](https://academic.oup.com/qjmath/article-pdf/50/200/471/4354525/500471.pdf)).

## 4. 쌍둥이 소수: 정량적 아벨-개수 부등식

### 이번에 증명한 명제

홀수에서만 지지되고 `0<=a_n<=1`인 수열에 대해

```text
T(Y) = sum_(n<=Y) a_n
F(r) = sum_n a_n r^n
```

로 둔다. `Y>=X`이고 `n0`가 `Y`보다 큰 첫 홀수이면

```text
r^X T(X) <= F(r) <= T(Y) + r^n0/(1-r^2)
```

이다. 따라서 인증된 하한 `L<=F(r)`은

```text
T(Y) >= ceil(L - r^n0/(1-r^2))
```

를 준다.

### 논증

`n<=X`이면 `r^n>=r^X`이므로 왼쪽 부등식이 나온다. `Y` 이하 항은
최대 `T(Y)`이고, 이후 모든 홀수 계수를 1로 바꾸면 오른쪽의 기하급수
꼬리가 된다. 식을 이항하고 `T(Y)`의 정수성을 쓰면 개수 하한을 얻는다.

쌍둥이 소수 지시수열과 `r_X=1-1/X`에 대해 유한 데이터는
`X=100,1000,10000,100000`에서 `T(10X)`의 유효 하한
`9, 35, 190, 1149`를 되찾았다. 이는 이미 알려진 유한 쌍둥이 지지를
사용한 것이며, 보지 못한 새 쌍을 증명하지 않는다.

### 고정 배율 no-go

`r_X=1-1/X`, `Y=cX`이면 계수 1 기하 꼬리는 점근적으로

```text
(X/2) exp(-c)
```

이다. 고정 `c`에서는 `X` 차수이므로 이 부등식만으로
`X/log^2 X` 규모 하한을 전달할 수 없다. 반면

```text
Y/X = 2 log log X + omega(1)
```

이면 기하 꼬리는 `o(X/log^2 X)`가 된다. 이는 패리티 장벽을 깨는 결과가
아니다. 미래의 패리티 민감 아벨 하한이 실제 개수 하한으로 변환될 수
있는 지평을 정한 것이다. Polymath8은 순수 체 방법의 패리티 한계를
명시한다
([arXiv:1407.4897](https://arxiv.org/abs/1407.4897)).

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket216_laplace_gcd_radix_tauberian.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket216_laplace_gcd_radix_tauberian -v
```

주 기계 판독 산출물:

```text
data/open-problem/ticket216-laplace-gcd-radix-tauberian.json
```

문제별 산출물은 `data/open-problem/{problem}/` 아래에 있다.

## 최종 상태

| 문제 | 새 결과 | 해결 상태 | 폐기한 경로 | 남은 증명 간극 | 다음 단일 보조정리 |
| --- | --- | --- | --- | --- | --- |
| 리만 | 첫 원자 라플라스 인증 | 미해결 | 고정 허용오차 | 실제 제타 공종 변환 상계 | `CofinalActualZetaOffLineLaplaceUpperBoundsBelowFirstAtomThreshold` |
| 콜라츠 | 정확한 교차 거듭제곱 GCD 필요조건 | 미해결 | 유한 대각선 승격 | 모든-`k` GCD 간극과 다중 run 연결 | `UniformStrictCrossPowerGCDGapAtEverySingleMountainCrossing` |
| 골드바흐 | 전체 진법 히스토그램 정확 해독 | 미해결 | 인코딩을 증명으로 오인 | 모든 블록의 독립 0번 자릿수 구간 | `ArithmeticRadixSelectorIntervalSeparatesTheZeroDigitOnEveryDyadicBlock` |
| 쌍둥이 소수 | 정량 아벨-개수 부등식 | 미해결 | 고정 배율 꼬리 전달 | 적응형 꼬리를 넘는 패리티 하한 | `ParityBreakingAbelLowerBoundDominatesAdaptiveGeometricTail` |
