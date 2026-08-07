# TICKET-191: 탐침 위상, 7-1 콜라츠 주기, 정확한 산술 목표

## 1. 주장 경계

TICKET-191은 정확한 중간 정리 네 개를 증명하지만, 리만 가설·콜라츠
추측·강한 골드바흐 추측·쌍둥이 소수 추측 중 어느 것도 해결하지
않았습니다. 반례도 찾지 못했습니다. 새로 완전히 닫힌 무한 계열은
가속 콜라츠 주기에서 `v=1`이 정확히 7개이고 나머지가 모두 `v=2`인
층 하나입니다.

| 문제 | 이번에 확정한 결과 | 폐기하거나 교정한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 가설 | `GaussianRationalProbePromotionAndCoordinateTestNoGo` (가우스 유리수 탐침 승격 및 좌표 검사 불충분 정리) | 좌표축만 검사하거나 스칼라 수렴 전에 연산자 노름 수렴을 요구 | `PoleNeutralWeilQuadraticValuesConvergeOnGaussianRationalCoreAndExtendContinuouslyToAdmissibleTestFunctions` |
| 콜라츠 추측 | `ExactlySevenValuationOnesOtherwiseTwoCycleExclusion` (`v=1` 7개·나머지 2인 주기 배제) | 곱 부등식 없이 끝없이 열거 | `NoContractingValuationWordWithExactlyEightOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| 강한 골드바흐 | `ExactPrimePowerBudgetPointwiseReductionAndLinearScaleNoGo` (정확한 소수 거듭제곱 예산 축소) | 고정된 양의 선형 하한을 필수 조건으로 취급 | `BinaryVonMangoldtCorrelationExceedsExplicitPrimePowerBudgetForEveryLargeEvenTarget` |
| 쌍둥이 소수 | `ArithmeticBlockGranularityEquivalenceAndLinearDensityNoGo` (산술 블록 입도 동치 및 선형 밀도 불필요 정리) | 양의 선형 밀도를 무한성과 동치로 취급 | `ShiftTwoCorrelationExceedsExactPrimePowerContaminationOnInfinitelyManyDyadicBlocks` |

재현 명령은 다음과 같습니다.

```powershell
python scripts\ticket191_probe_sevenone_budget_granularity.py
python -m unittest tests.test_ticket191_probe_sevenone_budget_granularity -v
python scripts\verify_open_problem_structure.py
```

기계 판독 결과는
`data/open-problem/ticket191-probe-sevenone-budget-granularity.json`에 있습니다.
네 시도 상태는 모두 `open_not_proven`(미증명)이고 해결 수는 `0 / 4`입니다.

## 2. 리만 가설

### 2.1 정확한 명제

유한 지지 벡터 공간이 증가할 때 에르미트 이차형식 `q_N`을 생각합니다.
가우스 유리수(실수부와 허수부가 모두 유리수) 좌표를 가진 모든 유한
지지 벡터 `x`에 대해 `q_N(x)`가 코시 수열이면, 그 극한은 이차형식
항등식을 보존합니다. 복소 편극 공식

```text
B(x,y) = 1/4 [q(x+y)-q(x-y)+i q(x+iy)-i q(x-iy)]
```

으로 각 유한 차원의 행렬 원소를 복원할 수 있으므로 `c_00` 전체에
하나의 호환되는 에르미트 형식을 정의합니다. 또한 각 고정 코어에서

```text
q_N(x) >= -epsilon_N ||x||^2,   epsilon_N -> 0
```

이면 극한 형식은 양의 준정부호입니다.

그러나 좌표축만 양수인지 보는 검사는 부족합니다. 유리수 `a>1`에 대해

```text
A_a = [[1,-a],[-a,1]]
```

은 `q(e_1)=q(e_2)=1`이지만 `q(1,1)=2-2a<0`이고 최소 고윳값은
`1-a`입니다. 생성된 JSON은 이 정확한 반례 계열과 유리수 탐침 코시
예제를 유리수 연산으로 검증합니다.

### 2.2 아직 증명하지 못한 것

실제 극점 중화 Weil/스크루 함수 이차형식에 대해 수렴, 음의 하한의
소멸, 연속성 중 어느 것도 증명하지 못했습니다. 가산 코어에서 스칼라
수렴을 얻더라도 허용 시험함수 위상으로 확장할 연속성 추정이 필요합니다.
따라서 이는 추상 승격 정리이지 리만 가설의 증명이 아닙니다.

최근 연구도 관련 연산자 극한을 구성하지만 결정적 결론은 추측 또는
수치 목표로 남겨 둡니다: [Suzuki 2026](https://arxiv.org/abs/2606.09096),
[2026년 수치 연산자 연구](https://arxiv.org/abs/2607.24830).

## 3. 콜라츠 추측

### 3.1 정확한 명제와 무한 구간

가속 홀수 궤도

```text
x_(i+1) = (3x_i+1)/2^v_i
```

에서 `v_i=1`이 정확히 7개이고 나머지가 모두 2인 길이 `h`의 주기를
생각합니다. 총 2진 지수는 `2h-7`이고 아핀 분모는

```text
D = 2^(2h-7)-3^h
```

입니다. `D>0`은 `h=17`부터 성립합니다. 자명하지 않은 양의 홀수 주기는
1을 포함할 수 없으므로 모든 궤도 값은 3 이상입니다. 한 주기를 곱하면

```text
1 = product_i (3+1/x_i)/2^v_i <= 128(5/6)^h.
```

`h=27`에서 우변은 정확히

```text
7450580596923828125 / 7996018508417728512 < 1
```

이고 이후 계속 감소합니다. 따라서 `h>=27`에는 이런 주기가 없습니다.

### 3.2 유한 예외 구간의 완전 검사

남은 수축 구간 `17<=h<=26`에서는 모든 단어에 대해 아핀 분자와
`B mod D`를 정확한 정수 연산으로 계산했습니다.

```text
sum_(h=17)^26 binomial(h,7)
  = binomial(27,8)-binomial(17,8)
  = 2,195,765.
```

나눗셈 적중은 0개입니다. 각 `h`별 SHA-256 전사 해시로 재현성을
확인하며, 원시 주기와 반복된 비원시 주기를 모두 포함합니다.

닫힌 것은 이 주기 층 하나뿐입니다. `v=1`이 8개 이상인 층, 3 이상의
valuation(2로 나누어지는 정확한 횟수), 비주기 발산은 여전히 열려
있으므로 콜라츠 추측의 증명이 아닙니다.

## 4. 강한 골드바흐 추측

### 4.1 실제로 필요한 점별 축소

`R_Lambda(N)`을 이항 폰 망골트 상관합이라 하고 `L=floor(log_2 N)`이라
합니다. 진 소수 거듭제곱 오염의 명시적 예산을

```text
B_pp(N) = 2 [floor(sqrt N)+(L-2)_+ floor(N^(1/3))] (log N)^2
```

로 둡니다. TICKET-189는 적어도 한 항이 진 소수 거듭제곱인 모든 합성곱
항의 총 가중치가 이 예산 이하임을 증명했습니다. 따라서 짝수 `N`에서

```text
R_Lambda(N) > B_pp(N)
```

이면 소수-소수 부분의 가중치가 양수이고, 그 `N`은 두 소수의 합입니다.
또한

```text
B_pp(N) <= 2(1+L)sqrt(N)(log N)^2 = o(N).
```

즉 고정된 양의 선형 하한은 충분하지만 이 오염 제거 단계의 필수 조건은
아닙니다. 더 약하고 정확한 목표는 모든 충분히 큰 짝수에서 점별 예산을
넘는 것입니다.

### 4.2 남은 증명 간극

이번 작업은 모든 충분히 큰 짝수 `N`에 대해 `R_Lambda(N)>B_pp(N)`을
증명하지 못했습니다. 이것이 이항 원호법의 주호·부호 상쇄 문제이며,
유한 계산이나 예외집합 정리만으로는 “모든 짝수” 양화사를 채울 수
없습니다. Helfgott의 세 소수 정리는 이항 문제가 별도 장애임을 분명히
구분합니다: [Helfgott 2015](https://arxiv.org/abs/1501.05438).
최근의 거듭제곱 절약 예외집합 결과도 모든 짝수의 이항 골드바흐를
증명하지는 않습니다: [Grimmelt·Teräväinen 2025](https://arxiv.org/abs/2508.16400).

## 5. 쌍둥이 소수 추측

### 5.1 정확한 블록 동치

이진 블록 `[2^j,2^(j+1))`에서 간격 2 폰 망골트 상관합 중 진 소수
거듭제곱이 관여한 항을 정확히 빼면 다음이 남습니다.

```text
b_j = sum_(2^j<=p<2^(j+1), p와 p+2가 모두 소수) log p log(p+2).
```

따라서 `b_j>0`과 해당 블록에 쌍둥이 소수가 존재한다는 명제는 정확히
동치입니다. 양수이면 한 쌍만 있어도

```text
b_j >= (j log 2)^2
```

입니다. 그러므로 쌍둥이 소수 추측은 무한히 많은 `j`에서 `b_j>0`인
것과 동치이고, 누적 정확 초과량이 무한대로 커지는 것과도 동치입니다.

### 5.2 선형 밀도가 필수가 아님을 보이는 no-go

양의 선형 누적 밀도는 무한성보다 강합니다. 다음 형식적 산술 규모
수열을 생각합니다.

```text
b_j = (j log 2)^2  (j가 2의 거듭제곱일 때),
b_j = 0            (그 밖의 경우).
```

양의 블록이 무한히 많고 누적 질량도 발산하지만 `J`까지의 누적량은
`O(J^2 log J)`이므로 `2^J`에 비하면 0으로 갑니다. 이는 최소 산술
가중치 규모를 지키는 논리적 비교 수열이지 실제 소수 데이터가 아닙니다.

실제 정확 초과량이 무한히 많은 블록에서 양수라는 증명은 아직 없습니다.
유계 소수 간격 정리는 정확한 간격 2를 강제하지 않습니다:
[Zhang 2014](https://annals.math.princeton.edu/2014/179-3/p07),
[Maynard 2015](https://annals.math.princeton.edu/2015/181-1/p07).

## 6. 결론

TICKET-191의 실질적 진전은 주장을 부풀리지 않고 증명 목표를 필요한
최소 양화사와 크기로 줄인 것입니다. 리만 경로는 가산 스칼라 탐침
관문을, 콜라츠 경로는 새 무한 valuation 층의 완전 배제를, 골드바흐
경로는 명시적 아선형 점별 예산을, 쌍둥이 소수 경로는 무한히 많은
양의 정확 블록을 남깁니다. 이 남은 의무들은 모두 명시적이지만 아직
증명되지 않았습니다.
