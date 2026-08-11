# TICKET-217: 상대 임계값, 연분수 후보 압축, 모멘트 지지집합, 임계 아벨 꼬리

## 주장 경계

TICKET-217은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이
소수 추측을 **증명하거나 반증하지 않았다**. 이번 티켓은 정확한 부분정리,
축소정리 또는 한계정리 네 개를 증명한다. 네 원래 문제의 상태는 모두
`open_not_proven`, 즉 미해결이며 기계 판정의 해결 개수는 0이다.

TICKET-216이 남긴 네 보조정리를 직접 공격했다. 핵심 변화는 고정된 절대
오차를 보는 대신, 실제로 탐지해야 하는 이산 사건의 크기와 관측 오차를
비교한 것이다.

| 문제 | 이번에 확정한 결과 | 폐기한 경로 | 남은 간극 | 다음 보조정리 |
| --- | --- | --- | --- | --- |
| 리만 | `MultiRadiusNormalizedDefectCertificateAndFinitePrecisionInvisibility` | 유한 개의 고정 절대오차 라플라스 표본 | 실제 제타 함수의 공종적 상대정밀도 구간 | `CofinalRelativePrecisionExplicitFormulaEnvelopeBelowOne` |
| 콜라츠 | `SingleMountainContinuedFractionCompressionAnd71356888Barrier` | `k`를 하나씩 훑는 선형 탐색 | 모든 상측 수렴분수, 다중 run, 발산 | `EffectiveAllUpperConvergentScalingBarrierForSingleMountainWords` |
| 골드바흐 | `WeightedSecondMomentFullSupportCertificateAndSharpThresholdNoGo` | Cauchy 인증식의 날카로운 계수를 낮추는 시도 | 점별 하단 꼬리 제어 | `PointwiseGoldbachLowerTailBoundBeyondSecondMomentSupportBarrier` |
| 쌍둥이 소수 | `SharpAdaptiveAbelTailPhaseTransitionAtTwoLogLog` | 유계 보정항이면 꼬리를 무시할 수 있다는 주장 | 임계상수보다 큰 실제 아벨 잉여 | `TwinAbelLowerBoundWithExplicitSurplusAboveCriticalTailConstant` |

## 1. 리만 가설: 정규화한 다중 반지름 인증

### 선언한 명제

TICKET-216처럼 높이 `H` 이하의 임계선 밖 영점 대칭쌍 개수를 `C(H)`라
하고 다음 라플라스 변환을 둔다.

```text
L(r) = integral r^t dC(t),       0 < r < 1.
```

유한 개의 반지름 `r_j`를 동시에 사용하면

```text
C(H) <= floor(min_j L(r_j)/r_j^H)
```

가 성립한다. `L(r_j)` 대신 엄밀한 상계 `U_j`를 사용해도 같다. 따라서

```text
min_j U_j/r_j^H < 1
```

이면 `C(H)=0`을 인증한다.

반대로 양의 절대 허용오차 `epsilon_j`를 유한 개 고정하면, 모든 `j`에서

```text
r_j^K < epsilon_j
```

가 되는 유한 높이 `K`가 존재한다. 높이 `K`에 질량 1인 원자 하나를 놓으면
결함 측도는 0이 아니지만 모든 관측 오차 안에 숨는다. 그러므로 유한 개의
고정 절대정밀도 라플라스 관측만으로는 RH를 도출할 수 없다.

### 증명

TICKET-216의 `C(H)r^H<=L(r)`를 각 반지름에 적용하고 `r_j^H`로 나눈 뒤
최솟값을 취한다. `C(H)`가 음이 아닌 정수이므로 우변이 1보다 작으면
`C(H)=0`이다.

각 `0<r_j<1`에 대해 `r_j^K`는 0으로 수렴한다. 반지름 개수가 유한하므로
각 허용오차에 필요한 높이 중 최댓값보다 큰 하나의 `K`를 선택할 수 있다.

생성기는 이 비교를 정확한 유리수 연산으로 검증한다. 숨긴 원자는 논리적
결함 측도이며 실제 제타 영점이라고 주장하지 않는다. 이 한계정리는 Platt와
Trudgian의 엄밀한 유한 높이 검증
([Bulletin of the London Mathematical Society](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/blms.12460))이나
Hiary, Ireland, Kyi의 일반화된 검증법
([arXiv:2408.00187](https://arxiv.org/abs/2408.00187))을 약화하지 않는다.

### 남은 간극

새 반지름을 더 추가하는 것만으로는 충분하지 않다. 실제 제타 함수의
explicit formula, 즉 명시적 공식을 이용해 높이가 커질 때마다 첫 원자
규모보다 작은 **상대 오차**를 보장해야 한다.

## 2. 콜라츠 추측: 연분수로 후보 압축

### 선언한 명제

양의 accelerated Collatz 주기의 valuation word가 단일 산형
`1^k 2^m`이라고 가정한다. 다음 상수를 둔다.

```text
alpha = log(3/2)/log(4/3).
```

그러면 기약분수 `p/q=m/k`는 `alpha`의 상측 연분수 수렴분수여야 한다.
상측 수렴분수 `p/q`마다

```text
Delta_0 = 2^(q+2p) - 3^(q+p)
```

를 계산한다. `Delta_0>=3^q`이면 그 수렴분수의 모든 양의 배수
`(m,k)=(gp,gq)`가 주기 근접충돌 조건을 만족하지 못한다.

정확한 계산으로 다음 마지막 수렴분수까지 상측 수렴분수 7개를 배제했다.

```text
p/q = 6,306,641 / 4,474,633
```

그 다음 상측 수렴분수는

```text
100,571,885 / 71,356,888
```

이다. 따라서 단일 산형 주기는 다음 범위에 존재하지 않는다.

```text
k < 71,356,888
```

이 수치는 모든 콜라츠 주기에 대한 하한이 아니라 `1^k2^m` 한 word 족의
하한이다.

### 수렴분수 축소의 증명

TICKET-215가 증명한 주기 필요조건은 다음과 같다.

```text
0 < Delta = 2^(k+2m)-3^(k+m) <= 3^k-2^k.
```

다음을 두면

```text
lambda = m log(4/3)-k log(3/2),
Delta = 3^(k+m)(exp(lambda)-1)
```

이므로

```text
0 < exp(lambda)-1 < 3^(-m),
0 < m/k-alpha < 3^(-m)/(k log(4/3)).
```

`alpha>1`이므로 `m>=k+1`이다. `k=1`에서 직접 확인하고 비율의 단조성을
쓰면

```text
2k < 3^(k+1) log(4/3)
```

이다. 따라서

```text
0 < m/k-alpha < 1/(2k^2).
```

`m/k`를 `p/q`로 기약해도 오차는 `1/(2q^2)`보다 작다. Legendre 정리에
의해 `p/q`는 연분수 수렴분수이고, 오차 부호가 양수이므로 상측
수렴분수다.

### 모든 배수를 한 번에 배제하는 증명

기약 수렴분수에 대해

```text
lambda_0 = p log(4/3)-q log(3/2) > 0
```

이라 하자. 정확한 정수 비교 `Delta_0>=3^q`는

```text
exp(lambda_0)-1 >= 3^(-p)
```

와 같다. 한편 배수 `g`가 주기 후보라면

```text
exp(g lambda_0)-1 < 3^(-gp)
```

여야 한다. 왼쪽은 `exp(lambda_0)-1` 이상이고 오른쪽은 `3^(-p)`
이하이므로 모순이다.

연분수 계수는 `log(3/2)`와 `log(4/3)`의 양의 atanh 급수로 만든 유리수
상·하한을 사용해 인증했다. 거듭제곱 비교에는 arbitrary-precision exact
integer, 즉 임의 정밀도 정확 정수만 사용했다. 연분수와 로그 선형형식은
기존 주기 연구에서도 쓰이는 도구다. Simons와 de Weger의 연구
([Acta Arithmetica record](https://eudml.org/doc/278746))와 비교할 수 있다.
독립적인 전문가 검토 전에는 새로움이나 우선권을 주장하지 않는다.

### 남은 간극

다음 상측 수렴분수부터는 아직 검사하지 않았다. 더 큰 문제는 단일 산형
word가 여러 valuation run, 3 이상의 valuation, 비주기 발산을 포함하지
않는다는 점이다. 콜라츠 추측 전체를 증명하려면 이 세 영역도 닫아야 한다.

## 3. 강한 골드바흐 추측: 날카로운 지지집합 모멘트 인증

### 선언한 명제

`B`개 짝수 목표의 골드바흐 표현 개수를 `A_i>=0`, 임의의 양의 정규화
가중치를 `w_i>0`이라 하자.

```text
y_i = A_i/w_i,
S = sum_i y_i,
Q = sum_i y_i^2.
```

다음 부등식이 성립하면 모든 목표가 표현된다.

```text
S^2 > (B-1)Q.
```

### 증명과 날카로움

표현되지 않는 목표가 하나라도 있으면 `y`의 지지집합 크기는 `B-1`
이하다. Cauchy-Schwarz 부등식으로

```text
S^2 <= |support(y)|Q <= (B-1)Q
```

이다. 대우를 취하면 선언한 인증식을 얻는다.

벡터

```text
(1,1,...,1,0)
```

은 `S^2=(B-1)Q`를 만족한다. 따라서 이 Cauchy 형태의 보편 인증식에서
`B-1`을 더 작은 계수로 바꿀 수 없다.

### 계산 결과와 한계

시작점 `128, 512, 2048, 8192, 32768`인 다섯 dyadic 블록의 정확한 원시
표현 개수에 인증식을 적용하면 모두 실패한다. 직접 열거한 최솟값은 모두
양수지만, 두 모멘트만 사용한 이 충분조건은 이를 인증하지 못한다.

Hardy-Littlewood 주항 형태로 정규화한 진단 비율은 블록 크기가 커지면서
1에 접근하고 마지막 블록에서 약 `0.999533`이지만 여전히 엄격한 문턱을
넘지 않는다. 이 정규화 행은 부동소수 진단이며 엄밀 구간 인증이 아니다.

이 정리는 두 모멘트로 가능한 모든 추론을 반박하지 않는다. 정확히 증명한
것은 표시한 Cauchy 인증식과 그 보편 계수의 날카로움이다. 고차 모멘트,
목표별 하한, 원 방법의 상쇄는 여전히 가능하다. 예외집합 정리는 예외집합이
비었다는 결론을 자동으로 주지 않는다. Li의 논문을 참고할 수 있다
([Quarterly Journal of Mathematics](https://academic.oup.com/qjmath/article-pdf/50/200/471/4354525/500471.pdf)).

## 4. 쌍둥이 소수 추측: 적응형 아벨 꼬리의 정확한 상전이

### 선언한 명제

TICKET-216의 홀수 계수-1 꼬리에서

```text
r_X = 1-1/X,
Y_X = floor(c_X X),
R_X = r_X^n0/(1-r_X^2)
```

라 하자. `n0`는 `Y_X`보다 큰 첫 홀수다. 배율을

```text
c_X = 2 log log X + a_X
```

로 두고 `0<=c_X=o(X)`라 가정하자. `a_X`가 유계일 때

```text
R_X/(X/log^2 X) = (1/2) exp(-a_X)(1+o(1))
```

이다. 같은 계산으로 세 영역을 정확히 나눈다.

- `a_X -> +infinity`: 기하 꼬리는 `o(X/log^2 X)`이다.
- `a_X`가 유계: 꼬리는 그 규모의 0이 아닌 상수배로 남는다.
- `a_X -> -infinity`이고 `c_X>=0`인 범위: 꼬리가 그 규모를 압도한다.

### 증명

`Y_X` 다음 첫 홀수는 `n0/X=c_X+o(1)`을 만족한다. 또한

```text
log(1-1/X) = -1/X + O(1/X^2),
1-r_X^2 = 2/X + O(1/X^2).
```

따라서

```text
R_X = (X/2) exp(-c_X)(1+o(1))
```

이다. `c_X`를 대입하고 `X/log^2 X`로 나누면 세 영역이 모두 나온다.
`a=-2,0,2`에 대한 Decimal 감사값은 `X=10^12`까지 각각
`exp(-a)/2`로 수렴한다.

이는 TICKET-216의 "약 `2 log log X`"를 정확한 상전이 상수로 강화한다.
그러나 실제 쌍둥이 소수 아벨 변환의 하한은 제공하지 않는다. Polymath8이
기록한 정확한 gap 2의 패리티 장벽도 넘지 않는다
([arXiv:1407.4897](https://arxiv.org/abs/1407.4897)).

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket217_relative_threshold_convergent_moment_tail.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket217_relative_threshold_convergent_moment_tail -v
```

통합 기계 판독 산출물:

```text
data/open-problem/ticket217-relative-threshold-convergent-moment-tail.json
```

각 문제별 산출물은 `data/open-problem/{problem}/` 아래에 있다.

## 최종 상태

| 문제 | 새 결과 | 해결 상태 | 폐기한 경로 | 남은 간극 | 다음 보조정리 |
| --- | --- | --- | --- | --- | --- |
| 리만 | 정규화 다중 반지름 인증 | 미해결 | 유한 고정 절대정밀도 | 실제 제타의 공종적 상대 구간 | `CofinalRelativePrecisionExplicitFormulaEnvelopeBelowOne` |
| 콜라츠 | 연분수 압축과 `k<71,356,888` 배제 | 미해결 | 선형 대각 탐색 | 모든 상측 수렴분수, 다중 run, 발산 | `EffectiveAllUpperConvergentScalingBarrierForSingleMountainWords` |
| 골드바흐 | 날카로운 가중 2차 모멘트 지지집합 인증 | 미해결 | 더 작은 보편 Cauchy 계수 | 점별 하단 꼬리 추정 | `PointwiseGoldbachLowerTailBoundBeyondSecondMomentSupportBarrier` |
| 쌍둥이 소수 | 정확한 `2 log log X` 꼬리 상전이 | 미해결 | 유계 보정항으로 꼬리 제거 | 패리티 민감 아벨 잉여 | `TwinAbelLowerBoundWithExplicitSurplusAboveCriticalTailConstant` |
