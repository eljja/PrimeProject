# TICKET-184: 정보 충분성 검증과 증명 경로 교정

## 초록

TICKET-184는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 **증명하거나 반증하지 않았다**. 이번 단계는 TICKET-183의 네 열린
보조정리를 이어가되, 계산량을 늘리기 전에 두 질문을 먼저 검사한다.

1. 제안된 보조정리가 결론에 필요한 산술 정보를 충분히 보존하는가?
2. 그 보조정리가 원래 추측보다 불필요하게 강하지 않은가?

| 문제 | 이번에 확립한 정확한 결과 | 상태 |
|---|---|---|
| 리만 가설 | `유한 모멘트 소거만으로는 균일 Abel 평활 해제가 불가능함` | 정확한 불가능성 정리, 리만 가설 미해결 |
| 콜라츠 | `반례 이분법과 최소 순환 prefix 장벽` | 정확한 분해, 콜라츠 미해결 |
| 골드바흐 | `제곱인수 없는 wheel 인수분해와 합성수 위장 불가능성 경계` | 정확한 국소 정리, 골드바흐 미해결 |
| 쌍둥이 소수 | `양의 root 총량의 충분성과 Cantelli 예외질량의 날카로움` | 정확한 경로 교정, 쌍둥이 소수 미해결 |

독립적인 전문가 검토 전에는 이 초등적 환원들의 문헌상 최초성을 주장하지
않는다. 목적은 유한 계산이나 불충분한 보조정리가 무한 증명으로 잘못
승격되는 것을 막는 데 있다.

## 1. 연구 계약

각 문제는 다음 다섯 항목을 분리해 기록한다.

1. 양화사가 명시된 이번 명제
2. 수학적 증명 또는 반례
3. 재현 가능한 유한 계산
4. 유한 계산이 넘어설 수 없는 논리적 한계
5. 다음 단계의 단일 미해결 보조정리

네 추측의 기계 판독 상태는 모두 `open_not_proven`, 즉 **아직 증명되지
않음**이다. 유한 검색은 반례를 찾을 수 있지만, 제한 안에서 반례가 없다는
사실만으로 모든 정수 또는 무한히 많은 경우를 증명할 수는 없다.

## 2. 리만 가설

### 2.1 이번 명제

정수 `m>=1`, `M>=1`에 대해 다음 삼각다항식을 잡는다.

```text
f_(M,m)(theta) = 2^(-m) e^(i M theta) (1-e^(i theta))^m
```

주파수 `M+r`의 Fourier 계수는

```text
c_r = 2^(-m)(-1)^r binom(m,r),  0<=r<=m
```

이며, 아래 `m`개의 모멘트를 정확히 소거한다.

```text
sum_(r=0)^m c_r (M+r)^j = 0,  0<=j<m
```

그러나 원래 함수와 Abel 평활 함수의 크기는

```text
||f_(M,m)||_infinity = 1
||A_rho f_(M,m)||_infinity = rho^M ((1+rho)/2)^m
```

이고, `theta=pi`에서 평활화를 되돌릴 때의 오차는 정확히

```text
1-rho^M((1+rho)/2)^m
```

이다. `m`과 `rho<1`을 고정하고 `M`을 키우면 평활된 함수는 0으로 가지만
원래 함수의 최대 크기와 평활 해제 오차는 1로 간다.

### 2.2 증명

모멘트 합은 차수가 `m`보다 작은 다항식 `(M+x)^j`의 `m`차 유한차분이다.
따라서 정확히 0이다. 또한 `|1-e^(i theta)|`의 최댓값은 `theta=pi`에서
2이다. Abel 변환은 `M+r`번째 계수에 `rho^(M+r)`를 곱하므로 이항식을
다시 묶으면

```text
A_rho f_(M,m)(theta)
  = 2^(-m) rho^M e^(iMtheta)(1-rho e^(itheta))^m
```

을 얻는다. `|1-rho e^(itheta)|`의 최댓값도 `pi`에서 `1+rho`이므로 모든
식이 따라온다.

### 2.3 무엇을 폐기했는가

**고정된 유한 개수의 다항식 주파수 모멘트만으로** Abel 평활화를 균일하게
되돌리는 경로를 폐기한다. 계산은 `m={1,2,4,8}`과
`M={16,32,64}`의 12개 경우에서 정수 모멘트 합을 정확히 0으로 확인했다.
`rho=0.9`일 때 가장 작은 평활 norm은 약 `7.82e-4`이지만 평활 해제 오차의
하계는 `0.9992`보다 크다.

이 반례족은 Weil 판정법 자체의 반례가 아니다. 실제 Weil 시험함수 원뿔은
Mellin 지지집합, 양성, 극점 중화 조건을 함께 요구한다. Connes와
Consani의 연산자 이론에서도 이 조건들이 유지된다
([The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368)). 이번 결과는
그 전체 구조를 유한 모멘트 몇 개로 대체할 수 없다는 뜻이다.

### 2.4 남은 간극

**다음 보조정리:**
`NormalizedWeilAdmissibleConeHasUniformFourierTailTightnessFromFullMellinConstraints`

한국어로는 “정규화된 Weil 허용 원뿔이 전체 Mellin 조건으로부터 균일한
고주파 꼬리 긴밀성을 갖는다”이다. 또 다른 유한 모멘트 부등식만으로는 이
간극을 닫을 수 없다.

## 3. 콜라츠 추측

### 3.1 이번 명제

홀수에 대한 가속 사상

```text
T(n) = (3n+1)/2^v,  v=v_2(3n+1)
```

의 반례가 존재한다면 정확히 두 종류 중 하나다.

1. 1이 아닌 주기 궤도
2. 상극한이 무한대인 비유계 궤도

주기 valuation word를 `w=(v_0,...,v_(h-1))`라 하고

```text
S_k = v_0+...+v_(k-1)
B_k = sum_(j<k) 3^(k-1-j) 2^S_j
D_k = 2^S_k-3^k
```

로 둔다. 비자명 순환을 가장 작은 홀수 원소 `n=B_h/D_h`에서 시작하도록
회전하면

```text
v_0 = 1
B_k D_h >= D_k B_h  (모든 1<=k<=h)
```

를 만족해야 한다. 그러나 이 prefix 장벽은 충분조건이 아니다. `(1,3)`은
모든 장벽을 통과하지만 `B=5`, `D=7`이므로 `D`가 `B`를 나누지 못한다.

### 3.2 증명

양의 정수에서 유계인 궤도는 유한 집합 안에 있으므로 어떤 값이 반복되고,
결정론적 사상에서는 그 뒤가 주기적이다. 따라서 주기적이지 않은 반례는
상극한이 무한대여야 한다. 비자명 순환의 최소 원소 `n>1`에서 첫 valuation이
2 이상이면

```text
T(n) <= (3n+1)/4 < n
```

이 되어 최소성에 모순이다. 또한 prefix의 affine 식

```text
n_k = (3^k n+B_k)/2^S_k >= n
```

에 `n=B_h/D_h`를 대입하고 분모를 제거하면 prefix 장벽이 나온다.

### 3.3 경로 교정과 계산

TICKET-183은 **순환 분기**를 valuation 1을 포함하는 원시 수축 word로
정확히 좁혔다. 그러나 이 word를 모두 배제해도 비유계 발산 궤도 분기가
남는다. 따라서 “비자명 순환이 없음”만으로 콜라츠 추측을 증명했다고 할 수
없다.

알파벳 `{1,...,5}`, 길이 7까지 정확히 열거했을 때 최소원소 prefix 장벽은
통과하지만 affine 나눗셈은 실패하는 word가 `5,036`개였다. 장벽은 유용한
필터이지만 인증서가 아니다. 별도로 `1,000,000` 이하 홀수 시작점
`499,999`개는 모두 시작값보다 작은 홀수 값에 도달했다. 가장 긴 최초 하강은
시작값 `626331`의 `111`단계였다. 이 결과는 유한 정수 계산이며 모든 시작값에
대한 정리가 아니다.

Tao의 “거의 모든 궤도” 결과도 같은 양화사 경계를 보여 준다. 밀도 정리는
매우 강하지만 모든 궤도의 수렴을 뜻하지 않는다
([Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)).

### 3.4 남은 간극

**다음 보조정리:**
`EveryPositiveOddIntegerAboveOneHasAnAcceleratedIterateBelowItsStart`

한국어로는 “1보다 큰 모든 양의 홀수는 유한 번의 가속 반복 후 시작값보다
작아진다”이다. 이 정리가 증명되면 강한 귀납법으로 전체 콜라츠 추측이
따라온다. 어떤 유한 cutoff도 이 정리를 대신하지 못한다.

## 4. 강한 골드바흐 추측

### 4.1 이번 명제

`Q`를 서로 다른 홀수 소수의 곱이라 하고 `U_Q`를 `Q`와 서로소인 잉여류
집합이라 하자. 다음 국소 표현 수를 정의한다.

```text
R_Q(n) = #{a mod Q : a in U_Q and n-a in U_Q}
```

그러면 정확히

```text
R_Q(n) = product_(p|Q) [p|n이면 p-1, 아니면 p-2]
```

이다. 따라서 모든 표적 잉여류에 양의 wheel 여유가 있다. 그러나 각
`r in U_Q`마다 `r mod Q`에 속하는 합성수 `x_r`를 만들 수 있다. 즉 단위
잉여류의 분포를 소수 없이도 완전히 복제할 수 있다.

### 4.2 증명

소수 `p|Q`에 대해 제외되는 잉여류는 `0`과 `n`이다. `p|n`이면 둘이 같아
`p-1`개가 남고, 아니면 서로 달라 `p-2`개가 남는다. 중국인의 나머지
정리에 의해 소수별 개수가 곱해진다.

불가능성 반례는 다음과 같이 만든다. `Q`를 나누지 않는 소수 `ell`을 고르고

```text
ell t congruent r (mod Q)
```

를 푼다. 필요하면 `t`를 `t+Q`로 바꾸어 `t>=2`로 만든다. 그러면
`x_r=ell t`는 알려진 진약수 `ell`을 가진 합성수이면서 잉여류 `r`을 그대로
유지한다.

### 4.3 재현 결과와 한계

`Q=15,105,1155`에서 모든 표적 잉여류에 대해 곱셈 공식을 전수 검사했다.
`Q=1155`에서는 480개 단위 잉여류 각각을 알려진 진약수를 가진 합성수로
복제했다. 따라서 고정 wheel의 양성은 정확한 국소 사실이지만 소수와 합성수
위장 자료를 구별하지 못한다.

이는 원방법을 반박하는 결과가 아니다. 오히려 modulus가 커져야 하고,
소수 가중치가 있는 minor arc 오차 제어가 반드시 필요함을 밝힌다. 최근의
골드바흐 예외집합 연구도 명시적인 major arc와 남은 균일 오차를 구분한다
([Grimmelt와 Bhowmik, 2026](https://arxiv.org/abs/2607.27282)).

### 4.4 남은 간극

**다음 보조정리:**
`GrowingWheelPrimeWeightedMinorErrorIsUniformlyBelowTheLocalSingularMargin`

한국어로는 “성장하는 wheel에서 소수 가중 minor 오차가 모든 표적의 국소
singular 여유보다 균일하게 작다”이다. 아무리 커도 고정된 wheel은 같은
합성수 위장 구성에 막힌다.

## 5. 쌍둥이 소수 추측

### 5.1 이번 명제

쌍둥이 소수의 첫 항 후보 좌표를 서로 겹치지 않는 유한 block으로 나누자.
`E_j>0`를 기대 쌍둥이 소수 질량, `C_j`를 block `j` 안에서 `p`와 `p+2`가
모두 소수인 시작점 `p`의 개수라 하자. root 비율은

```text
R = (sum_j C_j)/(sum_j E_j)
```

이다. `R>0`인 것과 전체 구간에 쌍둥이 소수 시작점이 하나 이상 있는 것은
동치다. 무한대로 멀어지는 서로 겹치지 않는 구간에서 이 조건이 무한히
반복되면 쌍둥이 소수는 무한히 많다. 모든 leaf가 양수일 필요는 없다.

정규화된 block 질량 `mu_j`, 비율 `r_j`, 평균 `r_bar`, 분산 `V`에 대해
Cantelli의 한쪽 꼬리 부등식은

```text
mu{r_j <= r_bar-t} <= V/(V+t^2),  t>0
```

를 준다. 한 leaf만 0이고 나머지가 모두 1인 경우 이 상계는 정확히
달성된다.

### 5.2 증명과 경로 교정

root의 분모는 양수이므로 root가 양수인 것과 실제 개수의 합이 양수인 것이
동치다. 서로 겹치지 않는 양의 구간들은 서로 다른 쌍둥이 소수 쌍을 제공한다.
Cantelli 부등식은 평행 이동한 제곱에 Markov 부등식을 적용하고 이동량을
최적화하면 얻는다. 질량 `epsilon`인 한 leaf가 0이고 배경이 1이면 평균은
`1-epsilon`, 분산은 `epsilon(1-epsilon)`이다. `t=1-epsilon`을 넣으면
부등식 양변이 모두 `epsilon`이 되어 날카로움이 확인된다.

TICKET-183의 모든 Haar 경로 인증은 올바른 충분조건이지만 쌍둥이 소수
추측에 필요한 것보다 강하다. 실제 `[100000,362144)` 구간에는 쌍둥이 소수
`2,298`쌍이 있고 root 비율은 `1.000378...`이지만 모든 leaf 인증은
실패한다. 결정적 목표는 모든 세분 구간의 양성이 아니라 무한히 반복되는
**전체 block 질량의 양성**이다.

그러나 sieve의 parity 장벽은 여전히 그 하계를 막는다. Maynard의 해설은
유계 간격 성과와 정확한 간격 2 사이의 간극을 설명한다
([On the Twin Prime Conjecture](https://arxiv.org/abs/1910.14674)).

### 5.3 남은 간극

**다음 보조정리:**
`PrimePairBlockMainTermDominatesParityRemainderOnAnUnboundedDisjointSequence`

한국어로는 “무한대로 가는 서로 겹치지 않는 구간열에서 소수쌍 주항이 parity
나머지보다 커진다”이다. Haar와 Cantelli는 예외 block을 찾는 진단 도구로
유지하지만, 반복되는 양의 root는 산술적 parity 돌파 오차 정리로 증명해야
한다.

## 6. 증명 의존성 요약

```text
리만 T183 Abel 전이
  -> 유한 모멘트 불가능성 [증명됨]
  -> 전체 Weil 원뿔의 꼬리 긴밀성 [미증명]

콜라츠 T183 원시 순환 word
  -> 반례 이분법과 prefix 장벽 [증명됨]
  -> 모든 시작값의 유한 하강 [미증명]

골드바흐 T183 정확한 Fourier 여유
  -> 제곱인수 없는 wheel과 합성수 위장 [증명됨]
  -> 성장 modulus의 소수 가중 오차 지배 [미증명]

쌍둥이 T183 Haar 경로 인증
  -> 양의 root 충분성과 날카로운 Cantelli [증명됨]
  -> 무한히 먼 구간에서 양의 전체 질량 [미증명]
```

## 7. 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket184_information_sufficiency_route_correction.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket184_information_sufficiency_route_correction
```

기계 판독 결과:

```text
data/open-problem/ticket184-information-sufficiency-route-correction.json
data/open-problem/riemann/rh-ticket-184-finite-moment-no-go.json
data/open-problem/collatz/co-ticket-184-dichotomy-prefix-barrier.json
data/open-problem/goldbach/gb-ticket-184-wheel-impostor.json
data/open-problem/twin-prime/tp-ticket-184-root-cantelli.json
```

기계 감사 결과는 정확한 정리 4개, 폐기 또는 교정한 경로 4개, 결정적 목표
교정 2개, 계산 실패 0개, 해결된 추측 0개다.
