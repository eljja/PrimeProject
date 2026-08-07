# TICKET-195: 유한 jet 경계, 고정 부분족 결정가능성, 소수제곱 층

## 1. 주장 경계

TICKET-195는 네 개의 중간 정리를 증명합니다. 리만가설, 콜라츠 추측,
강한 골드바흐 추측, 쌍둥이 소수 추측 가운데 어느 것도 증명하거나
반증하지 않았습니다. 새로 완전히 닫힌 무한 부분족은 가속 콜라츠 valuation
중 정확히 열한 항이 1이고 나머지가 모두 2인 순환층입니다.

| 문제 | 이번에 증명한 정확한 결과 | 폐기한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만가설 | `FiniteEvenJetAmbiguityAndRoucheTailBridge` (유한 짝함수 jet 모호성과 Rouché 꼬리 연결) | 균일 꼬리 부류 없이 유한 Xi/Jensen 데이터만 승격 | `XiTaylorSectionsAdmitCertifiedRoucheTailBoundsOnAnExhaustingOffRealDomainFamily` |
| 콜라츠 | `FixedOneCountRestTwoDecidabilityAndElevenStratumExclusion` (고정 1-개수 부분족 결정가능성과 열한-1 층 배제) | 열한-1 층과 각 고정 층에 무한 탐색이 필요하다는 주장 | `NoPositiveAcceleratedCollatzCycleHasAllValuationsInTheSetOneTwo` |
| 골드바흐 | `PrimeSquareDominantThetaLayerDecomposition` (소수제곱 주도 세타층 분해) | 지수 3 이상 support를 완전히 삭제 | `BinaryCorrelationExceedsPrimeSquareLayerPlusCubicTailEnvelopeForEveryLargeEvenTarget` |
| 쌍둥이 소수 | `PrimeSquareDominantIntervalThetaLayerDecomposition` (소수제곱 주도 구간 세타층 분해) | 제곱 support를 전체 국소 오염 집합으로 간주 | `ShiftTwoCorrelationExceedsPrimeSquareLayerPlusCubicTailEnvelopeOnInfinitelyManyDyadicBlocks` |

재현 명령은 다음과 같습니다.

```powershell
D:\python\anaconda3\python.exe scripts\ticket195_finitejet_elevenone_squarelayer.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket195_finitejet_elevenone_squarelayer -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

통합 기계 판독 결과는
`data/open-problem/ticket195-finitejet-elevenone-squarelayer.json`에 있습니다.
네 시도는 모두 `open_not_proven`, 즉 미해결이며 해결 수는 `0 / 4`입니다.

## 2. 리만가설

### 2.1 선택한 미해결 목표

TICKET-194는 실제 pole-neutral Weil 유한절단의 균일 유계성과 조밀 코어
수렴을 남겼습니다. 대체 경로로 실수 짝함수 entire 함수

```text
Xi(t)=xi(1/2+it)
```

의 Taylor/Jensen 데이터를 사용할 수 있습니다. RH는 `Xi(t)`의 모든 영점이
실수라는 명제와 동치입니다. 핵심 질문은 유한 짝수차 계수들을 별도 꼬리
정리 없이 무한 영점 명제로 승격할 수 있는가입니다.

### 2.2 유한 짝함수 jet 모호성 정리

임의의 실수 짝함수 유한 jet을

```text
J_m(z)=sum_(r=0)^m a_r z^(2r)
```

로 둡니다. `J_m(i)=sum a_r(-1)^r`는 실수이므로

```text
c=(-1)^m J_m(i),
P_m(z)=J_m(z)+c z^(2m+2)
```

로 놓을 수 있습니다. `P_m`은 `2m`차까지 모든 계수가 `J_m`과 같지만

```text
P_m(i)=J_m(i)+(-1)^m J_m(i)(-1)^(m+1)=0
```

입니다. 짝함수이므로 `P_m(-i)=0`도 성립합니다. 따라서 어떤 유한 실수
짝함수 jet도 비실수 영점을 가진 짝다항식과 양립합니다. 유한 Xi 계수,
유한 Jensen 다항식, 유한 Hankel 검사는 꼬리 부류 없이 전체 영점 명제를
인증할 수 없습니다.

계산은 `a_r=(-1)^r/(r+1)`, `m=0,...,12`인 유리수 예에서 모든
`P_m(i)=0`을 정확 분수로 확인합니다. 이 예들은 일반 대수 정리를 재생하기
위한 합성 jet이며 Xi 계수라고 주장하지 않습니다.

### 2.3 올바른 Rouché 연결

유계 영역의 경계를 `Gamma`라 하고 실제 entire 함수를 `F=P+R`로 쓰면

```text
sup_Gamma |R| < inf_Gamma |P|
```

일 때 Rouché 정리에 따라 `F`와 `P`의 영역 내부 영점 수가 같습니다.
기계 행은 단위원에서 `P=1`, `R=2^(-(m+1))z^(2m+2)`를 사용해 양의
유리수 여유를 확인합니다. 이는 유계 영역에 대한 올바른 인증 예입니다.

### 2.4 남은 간극

실제 Xi Taylor 절단에 대해 비실수 영역을 소진하는 contour family 전체의
꼬리 부등식을 증명하지 못했습니다. 유한 jet 모호성 정리는 실제 Xi의
비실수 영점을 찾은 것이 아닙니다. Rouché 정리는 고전 정리이며 그 자체의
문헌 독창성을 주장하지 않습니다.

## 3. 콜라츠 추측

### 3.1 고정 부분족 결정가능성 정리

`r>=1`을 고정하고 valuation에 정확히 `r`개의 1과 나머지 2만 있는 가속
콜라츠 word를 생각합니다. 길이가 `h`일 때 affine 분모는

```text
D_(r,h)=2^(2h-r)-3^h
```

입니다. 분모가 양수가 아닌 초기 길이는 수축 불가능합니다. 자명하지 않은
양의 홀수 순환의 모든 상태가 3 이상이라는 사실로 한 주기의 비율을 곱하면

```text
1 <= 2^r(5/6)^h
```

를 얻습니다. 고정 `r`에서 오른쪽은 0으로 가므로 충분히 큰 모든 `h`가
배제됩니다. 따라서 중간에 유한 개의 길이와 유한 개의 정규화 word만
남으며, 정확한 affine 나눗셈 계산으로 각 고정 부분족을 유한 시간에
결정할 수 있습니다.

이 정리는 `모든 고정 r마다 유한 결정이 있다`는 뜻이지, `모든 r을 하나의
유한 인증서가 결정한다`는 뜻이 아닙니다.

### 3.2 열한-1 층의 정확한 배제

`r=11`에서는 다음과 같습니다.

- `h<=26`: 비수축 구간,
- `h=27,...,41`: 정확 계산 구간,
- `h>=42`: `2048(5/6)^h<1`인 해석적 배제 구간.

첫 1 위치로 회전 정규화하면 경계항이 열 개입니다. 5+5 MITM 감사는

```text
sum_(h=27)^41 C(h-1,10)
 = C(41,11)-C(26,11)
 = 3,151,735,808
```

개 word를 정확히 대표합니다. 실제 계산량은 왼쪽 tuple 4,266,158개와
오른쪽 질의 1,893,528개이며, 정확한 정수 나눗셈 적중은 0개입니다.
`h=17`까지의 모든 정규화 word에서는 경계항 공식과 원래 recurrence도
직접 대조했습니다.

### 3.3 남은 간극

다음 목표는 고정 `r` 계산을 무한히 반복하는 대신 `{1,2}` valuation 전체를
한 번에 배제하는 균일 정리입니다. 3 이상의 valuation과 비주기 발산도
그대로 남습니다.

## 4. 강한 골드바흐 추측

### 4.1 소수제곱 주층

TICKET-194의 정확한 항등식에서 `k=2`를 분리하면

```text
W_odd(Y)
 = theta_odd(floor(sqrt Y))
 + R_>=3(Y),

R_>=3(Y)=sum_(k>=3) theta_odd(floor(Y^(1/k)))
```

입니다. 고전 Chebyshev 상계 `theta(t)=O(t)`를 사용하면 세제곱 층은
`O(Y^(1/3))`이고, 나머지 `O(log Y)`개 층은 각각 `O(Y^(1/4))`입니다.
`Y^(1/4)log Y=O(Y^(1/3))`이므로

```text
R_>=3(Y)=O(Y^(1/3)).
```

골드바흐 오염 상계는 다음 구조를 갖습니다.

```text
2log(N) theta_odd(floor(sqrt N))
 + O(N^(1/3)log N)
 + C_2(N).
```

즉 소수제곱이 주항이고 지수 3 이상은 더 작은 잔차입니다.

### 4.2 no-go와 유한 감사

지수 3 이상을 정확 support에서 삭제할 수는 없습니다.

```text
32=27+5=3^3+5
```

이 순서쌍은 `log(3)log(5)`의 오염을 만들지만 제곱 support에는 없습니다.
`2^10,...,2^21`의 열두 표적에서 세타층 분해와 직접 열거가 일치했고,
유한 전체 상관은 완전한 제곱+고차층 상계를 넘었습니다.

### 4.3 남은 간극

더 작은 우변을 얻었을 뿐, 모든 충분히 큰 짝수에 대한 이진 상관의 점별
하한은 얻지 못했습니다. 이것이 여전히 골드바흐 증명의 핵심 간극입니다.

## 5. 쌍둥이 소수 추측

### 5.1 구간 소수제곱 층

누적 항등식의 차를 취하면 모든 `[A,B)`에서 소수제곱 층과 지수 3 이상
잔차를 정확히 분리할 수 있습니다. 쌍둥이 소수 bridge의 두 이동 이진
구간에서는 고차층 국소 질량이 `O(X^(1/3))`이므로 오염 기여는

```text
O(X^(1/3)log X)
```

입니다. 소수제곱 구간층이 주된 proper-prime-power 항입니다.

### 5.2 no-go와 유한 감사

제곱 support만으로는 정확하지 않습니다. `[16,32)`에는

```text
(27,29)=(3^3,29)
```

가 있습니다. 이는 제곱 support가 누락하는 실제 간격-2 오염입니다.
`X=2^j`, `j=4,...,20`의 열일곱 블록에서 왼쪽/오른쪽 세타층 분해와 직접
열거가 일치했고 모든 유한 상관은 완전한 상계를 넘었습니다.

### 5.3 남은 간극

무한히 많은 비유계 블록에서 이 상계를 넘는 하한은 증명하지 못했습니다.
이 분해는 parity barrier를 극복하지 않으며 간격 2가 무한히 나타남을
증명하지 않습니다.

## 6. 2026-08-08 문헌 경계 대조

문제의 상태와 이번 결과의 범위는 다음 권위 자료 또는 1차 논문과
대조했습니다.

- [Clay Mathematics Institute 리만 가설 페이지](https://www.claymath.org/millennium/riemann-hypothesis/)는
  리만 가설을 여전히 미해결로 표시합니다. 유한 영점 검증은 무한 증명이
  아닙니다.
- Tao의 [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)
  (2026-07-16 개정 arXiv v7)는 로그 밀도 의미의 거의 모든 시작값 결과이며,
  모든 양의 시작값의 하강이나 모든 가능한 순환의 배제가 아닙니다.
- Oliveira e Silva, Herzog, Pardi의
  [강한 골드바흐 유한 검증](https://doi.org/10.1090/S0025-5718-2013-02787-1)은
  `4*10^18`까지의 유한 검증이며, 이 보고서에 필요한 전칭 상관 하한을
  제공하지 않습니다.
- Maynard의 [Small gaps between primes](https://doi.org/10.4007/annals.2015.181.1.7)는
  유계 소수 간격을 증명하지만 정확히 간격 2가 무한히 나타난다는 정리는
  아닙니다.

TICKET-195의 대수·조합 명제는 프로젝트 결과로 제시합니다. Rouché 정리,
Chebyshev 상계, 상속한 소수거듭제곱 항등식은 고전 또는 이전 입력이며 그
자체의 문헌 독창성을 주장하지 않습니다.

## 7. 종합

네 트랙은 같은 종류의 누락 양화사를 드러냅니다. 유한 jet에는 균일 꼬리
부류가 필요합니다. 무한히 많은 고정 `r` 결정에는 `r`에 균일한 정리가
필요합니다. 더 날카로운 sublinear 오염층에는 점별 또는 무한히 자주
성립하는 상관 하한이 필요합니다. TICKET-195는 이 간극들을 기계 검증
가능하게 분리하지만 난제 해결을 주장하지 않습니다.
