# TICKET-190: Cauchy 코어, 여섯-1 주기, 양화사 전이

## 1. 주장 경계

TICKET-190은 TICKET-189의 열린 노드 네 개를 이어간다. 새로 증명한 것은
콜라츠의 무한 주기 부분족 배제 하나와 위상·양화사 경계 세 개다. 리만
가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않았다.

| 문제 | TICKET-190의 정확한 결과 | 폐기·교정한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | `DirectCoreCauchyPromotionAndAbsoluteSummabilityNoGo` | 인접 코어 변화량의 절대합 가능성을 수렴의 필요조건으로 취급 | `PoleNeutralGuinandWeilFixedCoresHaveCertifiedCauchyModulusAndVanishingNegativeFloor` |
| 콜라츠 | `ExactlySixValuationOnesOtherwiseTwoCycleExclusion` | 유한한 여섯-1 열거를 모든 길이에 외삽 | `NoContractingValuationWordWithExactlySevenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| 골드바흐 | `DensityOneAndAverageMassDoNotImplyEveryTargetGoldbach` | 밀도 1 또는 평균 양성을 모든 짝수로 승격 | `ExplicitMajorArcMainMinusMinorArcErrorExceedsSublinearPrimePowerBudgetForEveryLargeEvenTarget` |
| 쌍둥이 소수 | `CumulativeDyadicLinearTransferAndSparseMassNoGo` | 양의 선형 블록 하한을 무한성의 필요조건으로 취급 | `CumulativeShiftTwoCorrelationMinusExactPrimePowerContaminationHasUnboundedCertifiedLowerEnvelope` |

재현 명령은 다음과 같다.

```powershell
python scripts\ticket190_cauchy_sixone_quantifier_transfer.py
python -m unittest tests.test_ticket190_cauchy_sixone_quantifier_transfer -v
```

기계 판독 산출물은
`data/open-problem/ticket190-cauchy-sixone-quantifier-transfer.json`이다. 네
추측의 상태는 모두 `open_not_proven`, 즉 미해결이다.

## 2. 리만 가설

### 2.1 이번에 증명한 명제

서로 호환되는 Hermitian 고정 코어에 직접적인 Cauchy 계수가 있으면 유한
지지 수열 공간 `c_00` 위에 하나의 Hermitian 형식을 정의할 수 있다.
최소 고윳값의 음의 오차가 0으로 수렴하면 극한 형식은 양의 반정부호다.
인접 코어 변화량의 절대합 가능성은 충분조건이지만 필요조건은 아니다.

다음 스칼라 족을 보자.

```text
A_N = 2 + sum_(k=1)^N (-1)^(k+1)/k.
```

교대급수 나머지 정리에 의해

```text
|A_M-A_N| <= 1/(N+1),  M>N
```

이라는 직접 Cauchy 계수가 성립한다. 그러나 인접 변화량의 절댓값은
`1/(N+1)`이고 그 합은 조화급수이므로 발산한다.

호환되는 양의 코어 `Q_m`이

```text
sup_m ||Q_m|| <= M
```

을 만족하면 형식은 `l_2` 위의 유계 양의 자기수반 연산자로 유일하게
확장된다. 이 유계성은 연산자 결론에 필요하다. 실제로
`Q_m=diag(1,2,...,m)`은 `c_00` 위에서 호환되고 양이지만 유계 `l_2`
연산자로 확장될 수 없다.

### 2.2 증명

직접 Cauchy 계수는 각 유한차원 코어를 Cauchy 수열로 만든다. 코어 제한의
호환성은 극한에서도 유지되므로 유한 지지 벡터에 하나의 형식이 정의된다.
교대급수 나머지는 절대 변화량의 합이 발산해도 위 계수를 준다.

코어 노름이 균일하게 `M` 이하이면

```text
|Q(x,y)| <= M ||x||_2 ||y||_2
```

이고, 조밀한 부분공간 `c_00`에서 연속 확장한 뒤 Riesz 표현 정리를
적용할 수 있다. 반면 `diag(1,...,m)`의 확장이 존재한다면 모든 `m`에
대해 `||Qe_m||=m`이어야 하므로 유계성과 모순이다.

### 2.3 남은 간극

이 결과는 TICKET-189가 사용한 위상 조건을 교정할 뿐이다. 실제 pole-neutral
Guinand-Weil 코어에 대한 직접 Cauchy 계수나 소멸하는 음의 고윳값 하한은
증명하지 않았다. 따라서 리만 가설의 증명이 아니다. 다음 경로는 절대합
상한만 요구하지 말고 산술적 진동 상쇄를 허용해야 한다.

## 3. 콜라츠 추측

### 3.1 이번에 증명한 명제

가속 콜라츠 양의 순환 중 valuation이 정확히 여섯 번 `1`이고 나머지가
모두 `2`인 순환은 존재하지 않는다. 원시 주기와 비원시 주기를 모두
포함한다.

### 3.2 전 길이 곱셈 논증

```text
x_(i+1) = (3x_i+1)/2^v_i
```

라 하자. `v_i=1`이 여섯 개이고 나머지가 `2`이면 valuation 합은
`2h-6`이며 수축 구간은 `h=15`부터다.

순환은 `x_i=1`을 포함할 수 없다. 홀수 가속 궤도에서 1을 지나는 순환은
모든 valuation이 2인 자명한 고정점뿐이므로 여섯 개의 1과 양립하지 않는다.
따라서 모든 `x_i>=3`이다. 한 주기의 점화식을 곱하면

```text
1 = product_i (3+1/x_i)/2^v_i
  <= (10/3)^h / 2^(2h-6)
  = 64(5/6)^h.
```

`h=23`에서 오른쪽은 정확히

```text
11920928955078125 / 12339534735212544 < 1
```

이고 이후 계속 감소한다. 따라서 `h>=23`인 순환은 모순이다.

### 3.3 유한 예외의 완전 검사

남은 수축 길이는 정확한 정수 연산으로 모두 검사했다.

```text
sum_(h=15)^22 binomial(h,6) = 238722.
```

각 valuation 단어에 대해 affine 분자 `B`, 분모
`D=2^(2h-6)-3^h`, 나머지 `B mod D`를 계산했다. 나누어떨어지는 단어는
0개다. 길이별 SHA-256 transcript를 JSON에 기록해 유한 검사를 재현할 수
있다.

### 3.4 한계

정확히 여섯-1/나머지-2인 주기 부분족 하나만 닫았다. 일곱 개 이상의 1,
3 이상의 valuation, 비주기적 발산 가능성은 다루지 않았다. 콜라츠 추측은
여전히 미해결이다.

## 4. 강한 골드바흐 추측

### 4.1 이번에 증명한 no-go 정리

밀도 1의 양성과 점근적으로 완전한 평균 선형 질량만으로 모든 짝수에서의
양성을 결론 낼 수 없다. 짝수 `N>=4`에 대해

```text
F(N) = 0  (N이 2의 거듭제곱),
F(N) = N  (그 밖의 경우)
```

로 두자. `F`는 무한히 많은 짝수에서 정확히 0이다. 하지만 `X`까지의
구멍 수는 `O(log X)=o(X)`이고, 빠진 질량은

```text
sum_(2^k<=X) 2^k < 2X = o(X^2)
```

이다. 따라서 전체가 양인 기준 모형과 같은 이차 주항을 가지며 평균 상대
오차도 0으로 간다.

### 4.2 의미와 한계

이것은 소수 상관함수의 모형이 아니라 논리적 반례다. 예외집합의 밀도나
평균적인 원 방법 추정만으로 강한 골드바흐의 전칭 양화사 “모든 짝수”를
닫을 수 없음을 증명한다. TICKET-189의 준선형 소수 거듭제곱 예산을 모든
충분히 큰 짝수에서 점별로 이기는 하한과 남은 유한 범위의 정확 검증이
여전히 필요하다.

## 5. 쌍둥이 소수 추측

### 5.1 이번에 증명한 전이 정리

dyadic 블록 질량 `b_j>=0`와 누적 질량

```text
W_J = sum_(j<J) b_j
```

를 두자. 다음 두 조건은 동치다.

```text
limsup_(J->infinity) W_J/2^J > 0,
어떤 c>0에 대해 b_j>=c2^j인 j가 무한히 많다.
```

TICKET-189의 정확한 소수 거듭제곱 제거를 적용하면

```text
b_j = shift-2 von Mangoldt 질량 - 소수 거듭제곱 오염항
    = 가중 쌍둥이 소수 질량
```

이다. 따라서 양의 선형 누적 초과량은 무한히 많은 양의 선형 dyadic 블록
하한으로 정확히 전이된다.

### 5.2 증명과 no-go

충분히 큰 모든 `j`에서 `b_j<c2^j`이면 기하급수 합으로
`limsup W_J/2^J<=c`이다. 양의 limsup보다 작은 `c`를 택하면 한 방향이
증명된다. 반대로 `b_j>=c2^j`이면 같은 부분수열에서
`W_(j+1)/2^(j+1)>=c/2`다.

그러나 선형 성장은 무한성의 필요조건이 아니다. `b_j=1`이면 누적 질량
`W_J=J`는 무한히 커지지만 블록 및 누적 정규화 질량은 모두 0으로 간다.
따라서 TICKET-189의 양의 선형 목표는 강한 충분조건이지 쌍둥이 소수
추측과 동치인 조건이 아니다.

### 5.3 남은 간극

정확한 오염항을 뺀 누적 가중 질량이 무한히 커진다는 명제는 쌍둥이 소수가
무한히 많다는 명제와 동치다. TICKET-190은 이 무한성을 증명하지 않았다.
다음 보조정리는 누적 정확 초과량에 대해 무한히 증가하는 인증된 하한을
제공해야 한다. 양의 선형 limsup는 더 강한 선택적 분석 목표로 남긴다.

## 6. 증명 상태 결론

TICKET-190은 정확한 명제 네 개를 증명했다. 콜라츠에서는 여섯-1/나머지-2
전체 주기층을 닫았다. 리만에서는 불필요하게 강한 절대합 조건을 제거했고,
골드바흐에서는 희소 구멍 양화사 no-go를, 쌍둥이 소수에서는 누적–dyadic
전이와 무한성·선형 밀도의 엄격한 차이를 확정했다. 난제 해결 수는 여전히
`0 / 4`다.
