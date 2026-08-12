# TICKET-219: 대역 통과 결함, Matveev 폐쇄, 교차적합 모멘트, 정성적 Abel 성장

English edition: [bandpass-matveev-crossfit-qualitative-abel.md](bandpass-matveev-crossfit-qualitative-abel.md)

## 주장 상태

TICKET-219는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이
소수 추측을 증명하거나 반증하지 않았다. 더 좁은 명제 네 개를
증명했다. 콜라츠의 무한한 한 단어 가족은 완전히 닫았고, 나머지 세
트랙은 논리적·계산적 접점을 개선한 뒤 남은 정리를 정확히 지정했다.

| 문제 | 새로 확정한 결과 | 상태 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | `PositiveDyadicBandpassDefectCertificateAndEquivalenceAudit`(양의 이진 대역 통과 결함 인증과 동치성 감사) | 상위 문제 미해결 | `PrimeSideDyadicBandpassDefectEnclosureBelowKernelFloor`(핵 바닥값 아래의 소수 측 결함 구간 포락) |
| 콜라츠 | `ExplicitMatveevClosureOfAllPositiveSingleMountainCycles`(모든 양의 단일 봉우리 주기의 명시적 Matveev 폐쇄) | 한 무한 단어 가족 폐쇄, 상위 문제 미해결 | `EffectiveBakerSeparationForAllPositiveCycleValuationWords`(모든 양의 주기 valuation 단어의 유효 Baker 분리) |
| 골드바흐 | `LeakageFreeCrossFittedEighthMomentSupportCertificate`(누수 없는 교차적합 8차 모멘트 지지집합 인증) | 유한 holdout fold 10개 인증, 상위 문제 미해결 | `CofinalCrossFittedGoldbachEighthMomentBelowFoldwiseZeroBarrier`(fold별 영 좌표 장벽 아래의 공종 교차적합 8차 모멘트) |
| 쌍둥이 소수 | `QualitativeAbelInfinitudeEquivalenceAndDensityScaleNoGo`(정성적 Abel 무한성 동치와 밀도 척도 no-go) | 상위 문제 미해결 | `UnboundedParityCorrectedTwinAbelTransform`(무계인 parity 보정 쌍둥이 Abel 변환) |

## 1. 리만 가설: 양의 이진 대역 통과 인증

TICKET-217과 218의 임계선 밖 결함 측도 `C`를 사용하고 다음과 같이
둔다.

```text
L(s) = integral exp(-s t) dC(t),
W(H) = L(1/H) - L(2/H).
```

그러면

```text
W(H) = integral exp(-t/H)(1-exp(-t/H)) dC(t).
```

닫힌 띠 `H <= t <= 2H`에서 이 양의 핵은

```text
c = exp(-2)(1-exp(-2))
```

이상이다. 따라서

```text
C([H,2H]) <= floor(W(H)/c),
W(H) < c  =>  C([H,2H]) = 0.
```

### 증명

`x=t/H`가 `[1,2]`에 있을 때
`f(x)=exp(-x)(1-exp(-x))`의 도함수는
`exp(-x)(2exp(-x)-1)<0`이다. 따라서 띠에서의 최솟값은 `f(2)=c`다.
이를 적분하고 결함 개수가 정수라는 사실을 적용하면 인증식이 나온다.
이진 띠들은 유한한 시작 높이 이후의 모든 높이를 덮는다.

### 무엇이 개선되었는가

두 Laplace 변환의 차이는 매우 낮거나 매우 높은 결함의 영향을 모두
줄인다. TICKET-218의 한 반지름 통계보다 위치가 잘 국소화된다. 동시에
논리적 강도도 바로잡았다. 유한 높이 검증과 모든 `H=2^j H0`에서의
`W(H)<c`를 합친 조건은 이 결함 모형 안에서 `C=0`, 즉 RH와 동치다.
미해결 명제에 “포락선”이라는 이름을 붙여도 RH보다 약해지지 않는다.

다음 비순환 과제는 실제 제타 함수의 변환 차이를 소수 측 explicit
formula에서 엄밀한 구간으로 계산하는 것이다. 합성 원자 재생은 위의
개수 부등식만 검증하며 제타 영점의 증거가 아니다.

## 2. 콜라츠 추측: 모든 양의 단일 봉우리 주기 폐쇄

TICKET-217은 valuation 단어가 `1^k 2^m`인 양의 가속 콜라츠 주기가
있다면 `(m,k)=g(p,q)`로 기약했을 때

```text
alpha = log(3/2) / log(4/3)
```

의 상측 수렴분수 `p/q`가 생기며, 다음 부등식이 필요함을 증명했다.

```text
0 < Lambda = (4/3)^p (3/2)^(-q) - 1 < 3^(-p).
```

양의 유리수 `4/3`, `3/2`에 대한 보수적인 Matveev 명시 하계는

```text
log Lambda > -K(1+log(2p)),
K = 1.4 * 30^5 * 2^4.5 * log(4) * log(3)
```

이다. 정확한 유리수 로그 구간 계산으로

```text
p log 3 > K(1+log(2p))
```

를 처음 만족하는 정수가

```text
p0 = 27,456,680,737
```

임을 인증했다. `p0`에서 여유량은 양수이고 `p0-1`에서는 음수이며,
그 이후 도함수의 하계도 양수다. 따라서 모든 `p>=p0`는 필요한
`Lambda<3^(-p)`와 모순된다.

TICKET-218은 앞의 상측 수렴분수 49개를 독립적으로 정확히 배제했다.
그 다음 분자의 값은

```text
16,672,027,258,049,147,969,018,986,102,532,625,254,200,541,727,292
```

로 `p0`보다 훨씬 크다. 수렴분수의 분자는 증가하므로 유한 앞부분과
Matveev 꼬리가 빈틈없이 만난다.

**부분정리.** valuation 단어가 `1^k 2^m`인 양의 가속 콜라츠 주기는
존재하지 않는다.

이 결과는 무한한 한 가족에 대한 완전한 정리이지만 콜라츠 추측은
아니다. 일반 주기 valuation 단어에는 여러 run이 있고, 비주기 발산은
주기가 아니다. 다음 보조정리는 위상 정보를 잃지 않으면서 Baker
분리를 모든 양의 주기 valuation 단어로 확장해야 한다.

명시적 하계는 Matveev의 출판된 유리 로그 하계를 특수화한다. E. M.
Matveev, “An explicit lower bound for a homogeneous rational linear form in
the logarithms of algebraic numbers. II,” *Izvestiya: Mathematics* 64 (2000),
1217-1269, https://doi.org/10.1070/im2000v064n06ABEH000314.

## 3. 골드바흐 추측: holdout 8차 모멘트 지지집합

유한 좌표 집합을 fold로 나눈다. 각 holdout fold `F`에 대해 `F` 밖의
좌표만 사용하여 양의 모형

```text
M_i = (P_F/Q_F) w_i
```

를 적합한다. 만약

```text
sum_{i in F} |A_i Q_F - P_F w_i|^p
  < (P_F min_{i in F} w_i)^p
```

이면 `F`의 모든 `A_i`가 양수다. 어떤 좌표가 0이면 그 좌표 하나의
잔차만으로도 우변 이상이 되기 때문이다. 모든 fold를 인증하면 전체
벡터의 지지집합이 양수다.

정확 재생은 `X=128,512,2048,8192,32768`인 다섯 이진 블록 `[X,2X)`에서
인덱스 짝·홀 두 fold를 사용한다. 정수 모형의 형태는

```text
round(10^6 n product_{odd p|n}(p-1)/(p-2))
```

이다. 10개 holdout fold 모두 `p=8`에서 통과했고, `p=4`에서는 1개만
통과했다. 모든 fold에서 학습 인덱스와 시험 인덱스는 서로소다. 이는
holdout 좌표가 자기 모형의 scale에 영향을 주지 못하게 하여
TICKET-218의 같은 표본 적합 문제를 제거한다.

하지만 holdout 잔차 자체는 실제 골드바흐 표현 개수를 열거해 계산한다.
따라서 여전히 유한 인증이다. 남은 정리는 그 개수를 열거하지 않고도
fold별 8차 모멘트 부등식을 공종적으로 증명하는 산술 추정이다.

## 4. 쌍둥이 소수 추측: 지나치게 강한 밀도 전제 제거

임의의 0-1 수열에 대해

```text
F(r) = sum_n a_n r^n
```

로 둔다. 지지집합이 무한일 필요충분조건은 `r`이 1로 왼쪽에서 갈 때
`F(r)`가 무계인 것이다. 유한 지지집합이면 `F`는 지지집합 크기 이하이고,
무한 지지집합이면 임의의 `K`개 지지점이 만드는 유한 부분합이 1 근처에서
`K`로 간다.

쌍둥이 소수 지시함수에는 다음 정확한 정성적 동치가 성립한다.

```text
쌍둥이 소수가 무한히 많다
  iff 실제 쌍둥이 Abel 변환이 무계다.
```

TICKET-218의 조건

```text
liminf F(1-1/X)/(X/log^2 X) > 1/2
```

은 유용한 충분조건이지만 추상적 무한성의 필요조건은 아니다. 무한한 홀수
지지집합 `n_j=2^j+1`은 `F(1-1/X)=O(log X)`이므로 정규화 하극한이 0이다.
이 반례 모형은 소수 모형이 아니며 실제 쌍둥이에 대한 Hardy-Littlewood
예측을 반박하지 않는다.

유한 하계 인증은 다음과 같이 남는다.

```text
F(1-1/X) >= T(X)/4,  X>=2.
```

`n<=X`인 각 지지점이 적어도 `(1-1/X)^X>=1/4`를 기여하기 때문이다.
다음 목표는 밀도 상수를 가정하는 대신 parity를 보정한 실제 쌍둥이
변환의 정성적 무계성을 증명하는 것이다.

## 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket219_bandpass_matveev_crossfit_qualitative_abel.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket219_bandpass_matveev_crossfit_qualitative_abel
```

기계 판독 결과:

- `data/open-problem/ticket219-bandpass-matveev-crossfit-qualitative-abel.json`
- `data/open-problem/riemann/rh-ticket-219-dyadic-bandpass.json`
- `data/open-problem/collatz/co-ticket-219-matveev-single-mountain.json`
- `data/open-problem/goldbach/gb-ticket-219-cross-fitted-eighth-moment.json`
- `data/open-problem/twin-prime/tp-ticket-219-qualitative-abel.json`
