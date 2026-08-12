# TICKET-221: 네 난제의 날카로운 obstruction certificate

## 주장 상태

**리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측은
모두 미해결이다.** TICKET-221은 네 가설의 증명이나 반례를 제시하지
않는다. 대신 TICKET-220에서 다음 목표로 남긴 네 보조정리 중 어떤
형태가 정보 부족 때문에 충분할 수 없는지 정확한 정리로 확정한다.

기계 판독 상태는 `open_not_proven`, 상위 추측 해결 수는 `0`이다.

## 연구 질문

TICKET-220은 다음 네 목표를 남겼다.

1. 리만: 합이 1보다 작은 소수 측 이진 대역 envelope.
2. 콜라츠: 원시 다중-run valuation word에 대한 유효 Baker 분리.
3. 골드바흐: 표현 수를 직접 읽지 않는 공종 cross-fit 여유.
4. 쌍둥이 소수: 모든 고정 휠을 넘어서는 parity 민감 하계.

TICKET-221의 질문은 더 엄격하다. **그 목표의 현재 표현 자체가 필요한
정보를 보존하는가?** 답은 네 경우 모두 “추가 결합 정보가 필요하다”이다.

---

## 1. 리만 가설

### 선언 명제

`ScaleUniformDyadicEnvelopeDivergenceNoGo`

`H>0`, `j in Z`, `t>0`에 대해

```text
K_j(t;H) = exp(-2^(-j)t/H) - exp(-2^(1-j)t/H)
```

라 두자. 모든 `j`에 대해

```text
sup_(t>0) K_j(t;H) = 1/4.
```

따라서 가능한 모든 한 원자 양의 결함을 각 좌표에서 독립적으로
지배하는 envelope `U_j`는 모든 `j`에서 `U_j >= 1/4`를 만족한다.
그러므로 `sum_j U_j`는 발산한다.

### 증명

`x=2^(-j)t/H`라 두면 `t`가 양의 실수 전체를 움직일 때 `x`도 양의
실수 전체를 움직인다. 핵은

```text
k(x)=e^(-x)-e^(-2x)
```

가 된다. 미분하면 `k'(x)=-e^(-x)+2e^(-2x)`이고 유일한 내부 임계점은
`x=log 2`이다. 양 끝에서 핵은 0으로 가며,

```text
k(log 2)=1/2-1/4=1/4.
```

각 `j`마다 `t=H 2^j log 2`에 원자 하나를 놓으면 해당 대역의 값이
`1/4`가 된다. 모든 가능한 한 원자를 좌표별로 지배하는 `U_j`는 따라서
각 좌표에서 최소 `1/4`이고 합은 발산한다.

### 계산 재현

- `j=-12,...,12`의 25개 대역에서 최대값 `1/4`와 도함수 0을 100자리
  Decimal 산술로 재현했다.
- `[-R,R]`의 보편 envelope 하계는 정확히 `(2R+1)/4`이다.
- `R=1,2,4,8,16,32`에서 선형 발산을 유리수로 기록했다.

### 폐기 경로

각 스케일을 실제 소수 산술과 무관한 동일한 최악값으로 독립 지배한 뒤
그 합을 1보다 작게 만드는 경로.

### 남은 간극

이 정리는 실제 제타 explicit formula의 스케일 간 결합, 부호 상쇄,
Weil 양성 또는 Li 계수를 배제하지 않는다. 실제 소수 자료가 스케일
사이에 예산을 이전하도록 만드는 결합 상계가 필요하다.

**다음 보조정리:** `ArithmeticCoupledDyadicTailBudgetBelowOne`.

---

## 2. 콜라츠 추측

### 선언 명제

`OrderBlindLogarithmicSeparationNoGoForPrimitiveWords`

가속 Collatz valuation word `a=(a_1,...,a_h)`의 한 바퀴 affine map은

```text
(3^h n + B(a)) / 2^S,
S = sum_i a_i,
B(a) = sum_i 3^(h-i) 2^(a_1+...+a_(i-1)).
```

이다. 순열은 `h`, `S`, 기울기 `3^h/2^S`, Baker 선형형식
`S log 2-h log 3`을 보존하지만 `B(a)`는 보존하지 않는다.

인접한 서로 다른 `x,y`를 prefix 합 `s` 뒤에서 교환하면 intercept의
차이는 정확히

```text
3^(h-i-1) 2^s (2^x-2^y)
```

이다. 특히 두 원시 다중-run word

```text
(1,2,3,4), (3,4,2,1)
```

는 서로 순환 이동으로 동치가 아니며 모두 `h=4`, `S=10`, `A=81`,
`D=1024`, `D-A=943`을 가지지만, intercept는 각각 `133`, `995`이다.
유리 고정점은 `133/943<1`과 `995/943>1`로 1의 반대편에 놓인다.

### 증명

`n -> (3n+1)/2^a`를 반복 합성하면 표시된 `B(a)` 공식이 귀납적으로
나온다. 인접 교환 전후에는 두 위치 이후의 prefix 합이 다시 같아진다.
따라서 intercept 합에서 바뀌는 국소항만 빼면 위 교환 항등식이 나온다.
두 증인에 공식을 직접 대입하면 공통 분모와 서로 다른 두 고정점을 얻는다.

따라서 `h,S`만 사용하는 Baker 하계는 원시 word의 순서 정보를 잃으며,
유리 고정점이 1보다 큰지조차 결정하지 못한다. 이는 Baker 이론 자체의
부정이 아니라 **Baker scalar만으로는 충분하지 않다**는 정리다.

### 계산 재현

- 네 valuation multiset의 모든 서로 다른 순열을 열거했다.
- 모든 순열에서 `(A,D)`가 같고 `B`가 여러 값을 갖는지 확인했다.
- 모든 가능한 인접 불등 교환에서 intercept 차이 항등식을 정수로
  검증했다.
- 핵심 증인의 공통 분모 943과 고정점 `133/943`, `995/943`을 정확히
  기록했다.

### 폐기 경로

`|S log 2-h log 3|`의 하계만으로 임의 원시 다중-run word의 cycle
폐쇄를 결정하는 경로.

### 남은 간극

순서가 있는 `B(a)`에 대해 `(2^S-3^h) | B(a)`를 배제하거나, 정확한
2-adic valuation admissibility를 이용해 하강을 증명해야 한다. 비주기
발산 궤도도 여전히 다뤄지지 않는다.

**다음 보조정리:**
`OrderSensitiveDivisibilityOrDescentForPrimitiveValuationWords`.

---

## 3. 강한 골드바흐 추측

### 선언 명제

`SharpLpDistanceToGoldbachZeroSet`

모든 좌표가 양수인 모델 벡터 `m`과, 하나 이상의 좌표가 0인 비음수
벡터 집합 `Z`를 생각하자. 모든 `1<=p<=infinity`에 대해

```text
dist_p(m,Z) = min_i m_i.
```

따라서 `||r-m||_p < min_i m_i`이면 모든 `r_i>0`이고 이 strict 상수는
최적이다.

### 증명

`z in Z`에서 `z_k=0`인 좌표를 택하면

```text
||z-m||_p >= |z_k-m_k| = m_k >= min_i m_i.
```

반대로 최소 모델 좌표 하나만 0으로 바꾸면 등호가 달성된다. sup norm도
같다. 따라서 양의 orthant에서 zero set까지의 정확한 반경은 최소
모델 좌표다.

어떤 유한 prefix가 완벽히 맞더라도 새 양의 모델 좌표와 관측값 0을
붙이면 기존 통계는 전혀 바뀌지 않고 확장 벡터는 zero set에 닿는다.
유한 블록 성공만으로 공종 양성을 얻을 수 없는 이유가 정확히 드러난다.

### 계산 재현

- 세 유리수 모델과 `p=1,2,4,8`의 12개 sharp witness를 검증했다.
- 길이 `4,8,16,32,64`인 완전 prefix 뒤에 zero coordinate를 추가해
  새 장벽에 정확히 닿는 것을 검증했다.
- TICKET-220의 `p=8` 직접 fold `150/150`, 정제 bridge `140/140`과
  최악 비율 약 `0.9670275612`를 다시 계산했다.

### 폐기 경로

유한 cross-fit 성공, 더 큰 moment 차수 또는 유한 partition 정제만으로
모든 충분히 큰 짝수의 표현 수가 양수라고 승격하는 경로.

### 남은 간극

실제 소수 분포로부터 모든 충분히 큰 dyadic block에서 정규화 residual
비율이 1보다 엄격히 작다는 공종 추정이 필요하다. 이 정리는 circle
method나 transference 추정을 배제하지 않는다.

**다음 보조정리:** `UniformCofinalLpMarginBelowOneFromPrimeDistribution`.

---

## 4. 쌍둥이 소수 추측

### 선언 명제

`LowDegreeBooleanParityOrthogonalityNoGo`

균등 Boolean cube `{-1,1}^m`에서 parity character를

```text
P(x)=product_i x_i
```

라 하자. 모든 proper subset `S`에 대해

```text
E[P(x) product_(i in S)x_i] = 0,
```

이고 전체 좌표를 사용하면 correlation은 1이다. 따라서 Walsh 차수가
`m`보다 작은 모든 다항식은 parity와 직교한다.

### 증명

proper `S` 밖의 좌표 `k`를 하나 고른다. 각 `x`를 `x_k`의 부호만
뒤집은 점과 짝지으면 `S` monomial은 변하지 않고 `P`만 부호가 바뀐다.
모든 항이 상쇄된다. 전체 좌표 monomial은 `P` 자체이므로 곱은
`P(x)^2=1`이다.

### 계산 재현

- `m=2,...,12`에서 cube의 모든 점을 열거했다.
- 각 `m`에서 `2^m-1`개의 모든 proper Walsh monomial을 검사했다.
- 모든 저차 correlation 정수합은 0, 전체 차수 합은 정확히 `2^m`이었다.

### 폐기 경로

선택된 소수들의 proper 저차 상호작용만 가진 국소 sieve observable이
factor parity를 감지한다고 주장하는 경로.

### 남은 간극

Boolean 모델 밖의 실제 산술에서 parity를 깨는 Type II 정보 또는 shifted
von Mangoldt correlation의 양의 하계가 필요하다. 이 정리는 Maynard
weight나 모든 bilinear form을 저차라고 분류하지 않는다.

**다음 보조정리:**
`VonMangoldtPairLowerBoundWithParityBreakingTypeIIInput`.

---

## 문헌 경계

- 리만: X.-J. Li의 원래 positivity criterion은 RH와 전역 양성의 등가를
  제시한다. TICKET-221의 이진 핵 최대값 정리는 그 criterion의 새 증명이
  아니다.
- 콜라츠: Baker의 선형 로그 하계와 J. L. Simons의 Syracuse cycle 연구는
  scalar separation의 문헌 배경이다. 프로젝트 결과는 ordered intercept가
  별도 정보임을 확인한다.
- 골드바흐: circle method와 exceptional-set 연구가 실제 공종 추정을
  담당한다. 여기의 정리는 유한차원 `L^p` 기하이다.
- 쌍둥이 소수: Heath-Brown의 sieve parity 연구와 Maynard의 bounded-gap
  방법이 분석적 경계를 제공한다. Boolean cube는 정확한 stress model일
  뿐 실제 소수 하계가 아니다.

참조:

- [Li, The Positivity of a Sequence of Numbers and the Riemann Hypothesis](https://doi.org/10.1006/jnth.1997.2137)
- [Baker, Linear forms in the logarithms of algebraic numbers](https://doi.org/10.1112/S0025579300003971)
- [Simons, On the (non-)existence of m-cycles for generalized Syracuse sequences](https://eudml.org/doc/278414)
- [Grimmelt and Bhowmik, The exceptional set of the Goldbach problem](https://arxiv.org/abs/2607.27282)
- [Heath-Brown, A parity problem from sieve theory](https://doi.org/10.1112/S0025579300012109)
- [Maynard, Small gaps between primes](https://arxiv.org/abs/1311.4600)

문헌 우선권이나 신규성은 주장하지 않는다.

## 결론

| 문제 | 새 결과 | 폐기한 경로 | 남은 단일 보조정리 |
|---|---|---|---|
| 리만 | 스케일별 보편 envelope가 좌표당 최소 `1/4`라 발산 | 독립 최악값을 합해 1 미만으로 만듦 | `ArithmeticCoupledDyadicTailBudgetBelowOne` |
| 콜라츠 | 동일 Baker 데이터가 순서에 따라 고정점 1의 양쪽으로 갈림 | scalar separation만으로 원시 word 폐쇄 | `OrderSensitiveDivisibilityOrDescentForPrimitiveValuationWords` |
| 골드바흐 | positive model에서 zero set까지 `L^p` 거리가 정확히 최소 좌표 | 유한 moment 성공을 공종 양성으로 승격 | `UniformCofinalLpMarginBelowOneFromPrimeDistribution` |
| 쌍둥이 소수 | 저차 Walsh observable은 parity와 정확히 직교 | 저차 국소 sieve가 parity 감지 | `VonMangoldtPairLowerBoundWithParityBreakingTypeIIInput` |

주 기계 판독 감사 파일:

`data/open-problem/ticket221-sharp-obstruction-certificates.json`
