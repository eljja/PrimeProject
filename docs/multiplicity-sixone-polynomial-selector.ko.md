# TICKET-213: 중복도, 여섯-1 주기, 다항식 상계, 간격 선택자

> **연구 상태:** 네 상위 난제 모두 `open_not_proven`, 즉 미해결입니다.<br>
> **기계 판독 산출물:**
> [`ticket213-multiplicity-sixone-polynomial-selector.json`](../data/open-problem/ticket213-multiplicity-sixone-polynomial-selector.json)<br>
> **재현 스크립트:**
> [`ticket213_multiplicity_sixone_polynomial_selector.py`](../scripts/ticket213_multiplicity_sixone_polynomial_selector.py)

TICKET-213은 새 계산을 추가하기 전에 TICKET-212가 남긴 논리적 목표가
원래 난제와 정확히 일치하는지 먼저 검사합니다. 네 개의 정확한 부분정리
또는 경로 불가능성 정리를 증명하지만, 리만 가설·콜라츠 추측·강한
골드바흐 추측·쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않습니다.

| 문제 | 새로 증명한 정확한 결과 | 폐기한 경로 | 남은 간극 | 다음 단일 보조정리 |
|---|---|---|---|---|
| 리만 | `MultiplicityAwareCriticalLineCountEquivalenceAndSignChangeNoGo` | 단순성 정리 없이 홀수 중복도 부호변화를 RH와 동치인 계수로 사용 | 실제 제타 영점에 대한 전 높이 중복도 등식 | `UniformMultiplicityAwareCriticalLineDefectStrictlyBelowTwo` |
| 콜라츠 | `CompleteSixValuationOneCycleStratumExclusion` | `v2=1` 항이 정확히 6개인 모든 양의 주기 단어 | `1` 항이 7개 이상인 주기와 비주기 발산 | `UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastSeven` |
| 골드바흐 | `FixedDegreePolynomialWitnessMajorantNoGo` | 증인 개수의 고정 다항식을 점별 예외 상계로 사용 | 차수가 규모에 따라 증가하거나 비다항식인 1 미만 꼬리 상계 | `ScaleGrowingWitnessResummationWithUniformDyadicTailBelowOne` |
| 쌍둥이 소수 | `NonnegativeGapFunctionalIsolationIffSupportAtTwo` | 다른 간격이 섞인 모든 비음수 가중합 | 나머지가 통제된 부호 있는 산술 선택자 | `GapTwoSelectiveSignedFunctionalWithUniformArithmeticRemainder` |

## 1. 리만 가설

### 이번에 선언한 명제

경계에 영점이 없고

```text
rho -> 1 - conjugate(rho)
```

대칭인 임계띠 상반부 직사각형 `R`을 잡습니다. `N`은 중복도를 포함한
전체 영점 수, `M`은 임계선 `Re(s)=1/2` 위 영점 중복도의 합이라고
하겠습니다. 그러면

```text
N-M = 2 * (임계선 한쪽에 있는 비임계선 영점 중복도의 합)
```

이므로 `N-M`은 음이 아닌 짝수이고,

```text
N-M < 2  <=>  R의 모든 영점이 임계선 위에 있음
```

이 성립합니다. 이것이 중복도를 올바르게 반영한 유한 직사각형 RH
인증 조건입니다.

### TICKET-212의 부호변화 목표가 과도했던 이유

`O`를 Hardy 함수의 완전한 부호변화로 검출할 수 있는 서로 다른 홀수
중복도 임계선 영점 수라고 하면

```text
N-O = (N-M) + sum_line(m - (m mod 2))
```

입니다. 따라서 `N-O<2`는 모든 영점이 임계선 위에 있을 뿐 아니라
**모두 단순 영점**일 때만 성립합니다. 중복도 2인 임계선 영점은 RH와
양립하지만 `N-M=0`, `N-O=2`입니다. 그러므로 TICKET-213은 부호변화
결함을 최소 RH 동치 목표로 보던 경로를 폐기합니다.

생성기는 단순·이중·삼중 임계선 영점과 비임계선 대칭쌍의 유한 배치를
정확 산술로 검사합니다. 이는 제타 영점을 계산한 결과가 아닙니다. 실제
제타 함수에 대해 모든 높이에서 `N=M`임을 증명하지 못했습니다.

### 증명 의존 그래프

```text
EvenCriticalLineDefectSubTwoSaturationCertificate
  -> MultiplicityAwareCriticalLineCountEquivalenceAndSignChangeNoGo
       -> [폐기] SignChangeSubTwoIsExactlyRHEquivalent
       -> UniformMultiplicityAwareCriticalLineDefectStrictlyBelowTwo
            -> 리만 가설
```

## 2. 콜라츠 추측

### 이번에 선언한 명제

가속 콜라츠 변환의 양의 비자명 주기에는 `v2(3x+1)=1`인 항이 정확히
6개이고 나머지 valuation이 모두 2 이상인 경우가 존재하지 않습니다.
TICKET-210과 합치면, 가상의 양의 비자명 주기는 valuation-one 항을 최소
7개 포함해야 합니다.

### 유한화 논증

가상 주기를 가장 작은 홀수 `m>=3`에서 시작하도록 회전합니다. 나가는
단계의 valuation은 1이고 들어오는 단계는 2 이상입니다. 길이가 `h`,
valuation 합이 `A`, valuation-one 항이 정확히 `k`개이면

```text
A >= 2h-k,
2^A = product_i(3 + 1/x_i) <= (10/3)^h,
(6/5)^h <= 2^k.
```

`k=6`이면 `h<=22`입니다. 같은 곱 상계가 각 길이에서 `A`도 유한하게
제한합니다.

### 정확 전수조사

스크립트는 강제되는 첫 valuation과 마지막 valuation을 고정하고, 나머지
다섯 개의 `1` 위치 및 valuation 초과량의 모든 약한 합성(weak
composition)을 열거합니다. 각 단어에 대해

```text
C = sum_j 3^(h-1-j) 2^(a_1+...+a_j),
D = 2^A - 3^h,
x = C/D
```

를 정수로 정확히 계산합니다. 길이 `7..22`의 후보 `376,788`개 중 양의
`D`가 `C`를 나누는 경우가 하나도 없습니다. 길이별 SHA-256 기록 해시도
JSON에 저장됩니다.

이것은 정확히 여섯-1인 **주기 층 하나**에 대한 완전 증명입니다. `1`이
7개 이상인 주기와 비주기 발산 가능성에는 아무 결론도 주지 않습니다.

### 증명 의존 그래프

```text
TwoAdicGhostUniversalityAndOddDivisibilityCorrection
  -> CompleteSixValuationOneCycleStratumExclusion
       -> [폐기] SixValuationOnePositiveCycleStratum
       -> UniformPrimitiveOddDivisorWitnessForAllOneCountsAtLeastSeven
            -> 콜라츠 추측의 주기 분기
```

## 3. 강한 골드바흐 추측

### 이번에 선언한 명제

`A(N)`을 짝수 `N`의 순서 없는 골드바흐 표현 개수라고 합시다. 다음을
동시에 만족하는 고정 실수 다항식 `P`는 존재하지 않습니다.

```text
P(0) >= 1,
표현 가능한 모든 짝수 N에 대해 0 <= P(A(N)) < 1.
```

TICKET-212는 소수정리와 정확한 소수쌍 비둘기집 계산으로 실제로 나타나는
양의 `A(N)` 값이 위로 제한되지 않음을 증명했습니다. 비상수 다항식은 그
무한 부분수열에서 최고차항 부호에 따라 양의 무한대 또는 음의 무한대로
갑니다. 상수 다항식도 0에서 1 이상이면서 표현 가능한 값에서 1 미만일 수
없습니다.

또한 `A=0,1,...,M`에서 정확한 0-지시함수와 일치하는 다항식은
`1,...,M`이라는 서로 다른 근 `M`개를 가지므로 차수가 최소 `M`입니다.
최소 차수는

```text
Q_M(A) = product_(j=1)^M (1 - A/j)
```

가 달성합니다. 스크립트는 `M=1..12`에 대해 유리수로 정확히 검증합니다.
따라서 고정 Bonferroni 차수의 실패는 특정 기저의 문제가 아니라 모든
고정 다항식에 공통된 점별 장애입니다.

이 정리는 규모 의존 다항식, 유리함수, 지수함수, 기타 해석적 재합성은
배제하지 않으며 골드바흐 꼬리 양성을 증명하지도 않습니다.

### 증명 의존 그래프

```text
FullWitnessProductIdentityAndFixedBonferroniNoGo
  -> FixedDegreePolynomialWitnessMajorantNoGo
       -> [폐기] FixedPolynomialCanMajorizeAllGoldbachExceptionsBelowOne
       -> ScaleGrowingWitnessResummationWithUniformDyadicTailBelowOne
            -> 강한 골드바흐 추측
```

## 4. 쌍둥이 소수 추측

### 이번에 선언한 명제

간격 2를 포함하는 유한 간격 집합 `H`, 비음수 가중치 `w_h`, 비음수 채널
벡터 `t`에 대해

```text
L_w(t) = sum_(h in H) w_h t_h
```

라고 합시다. 모든 `t>=0`에 대해

```text
L_w(t)>0  <=>  t_2>0
```

가 성립할 필요충분조건은 `w_2>0`이고 모든 `h!=2`에서 `w_h=0`인
것입니다.

순수 gap-two 가중치에서는 자명합니다. 역으로 비음수 원뿔의 극단 광선
`e_2`를 대입하면 `w_2>0`이어야 하고, 각 `g!=2`의 `e_g`를 대입하면
`w_g=0`이어야 합니다. 따라서 아무리 작은 양의 가중치라도 다른 간격에
배정되면 보편적인 gap-two 선택 기능은 사라집니다.

유리수 계산은 순수 선택자, 균등 합, 작은 오염 가중치, gap-two 누락
가중치를 모든 기저 광선에서 검사합니다. 이는 추상 원뿔에 대한 정확한
정리이지 실제 소수의 gap-two 하한이 아닙니다. 부호 있는 산술 선택자는
음의 항과 나머지를 균일하게 통제할 때만 다음 후보가 됩니다.

### 증명 의존 그래프

```text
DyadicGapTwoEquivalenceAndFiniteGapAggregateNoGo
  -> NonnegativeGapFunctionalIsolationIffSupportAtTwo
       -> [폐기] ContaminatedNonnegativeWeightsCanSelectGapTwo
       -> GapTwoSelectiveSignedFunctionalWithUniformArithmeticRemainder
            -> 쌍둥이 소수 추측
```

## 재현 방법

```powershell
python scripts/ticket213_multiplicity_sixone_polynomial_selector.py
python -m unittest tests.test_ticket213_multiplicity_sixone_polynomial_selector -v
```

성공하면 통합 감사 JSON과 문제별 JSON 네 개가 생성되고 다음을 보고합니다.

```text
exact_partial_theorem_count = 4
conjecture_resolution_count = 0
total_failure_count = 0
```

## 선행 연구와의 경계

- Platt와 Trudgian의 [유한 높이 RH 검증](https://arxiv.org/abs/2004.09765)은
  외부 결과입니다. PrimeProject는 새로운 제타 구간연산 검증을 하지 않았습니다.
- 콜라츠 결과는 표준 가속 주기 방정식과 이 프로젝트의 앞선 원시 단어
  축약을 사용합니다. 비주기 분기에 대한 우선권이나 해결을 주장하지 않습니다.
- [`4*10^18`까지의 골드바흐 검증](https://doi.org/10.1090/S0025-5718-2013-02787-1)은
  이 프로젝트의 유한 진단보다 훨씬 강하지만 역시 무한 명제의 증명은 아닙니다.
- Maynard의 [유계 소수 간격 정리](https://doi.org/10.4007/annals.2015.181.1.7)는
  정확한 간격 2를 선택하지 않습니다.

## 주장 경계

TICKET-213은 올바른 증명 목표를 더 정확히 선택하고 콜라츠의 유한 주기 층
하나를 추가로 닫았습니다. 나머지 세 결과는 더 넓은 논리적 불가능성 또는
동치 정리입니다. 네 난제에 필요한 무한 산술 추정은 아직 없으며, 어느
결과도 난제의 해결로 표시하지 않습니다.
