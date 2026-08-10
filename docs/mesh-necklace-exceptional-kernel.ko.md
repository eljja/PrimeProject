# TICKET-204: 연속 인증, 원시 necklace, parity kernel

## 주장 상태

네 상위 추측은 모두 `open_not_proven`, 즉 **미해결**이다. TICKET-204는 네
개의 중간 정리 또는 no-go를 증명하지만, 리만 가설, 콜라츠 추측, 강한
골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않는다.

표준 기계 판독 산출물은
[`ticket204-mesh-necklace-exceptional-kernel.json`](../data/open-problem/ticket204-mesh-necklace-exceptional-kernel.json)이다.

| 문제 | TICKET-204의 정확 결과 | 폐기한 경로 | 결정적인 다음 보조정리 |
|---|---|---|---|
| 리만 | 도함수로 인증된 mesh가 표본 상대오차를 연속 Rouché 경계로 승격한다. 유한 표본만으로는 불가능하다 | 정칙성 상계 없는 유한 경계 표본 | `CompletedZetaCofinalAdaptiveRelativeDerivativeBound` |
| 콜라츠 | 회전과 word 반복은 affine cycle 몫을 보존하므로 주기 word를 원시 necklace로 축약할 수 있다 | 회전·반복을 독립적인 증거로 계산 | `UniformNondivisibilityForAllNonAllTwoPrimitiveValuationNecklaces` |
| 골드바흐 | tail 예외 개수의 엄밀한 `<1` 상계는 전칭 명제를 닫지만 밀도 0은 그렇지 않다 | 밀도 0 또는 유계 예외를 예외 없음으로 승격 | `ExplicitBinaryGoldbachTailExceptionalCountStrictlyBelowOne` |
| 쌍둥이 소수 | PSD kernel은 모든 반소수 채널을 음수로 만들 수 없다. indefinite rank-2 형식은 형식적 인수 채널에서 대수적으로 탈출한다 | PSD·제곱형 weight를 이용한 부호 parity 분리 | `ArithmeticRealizationOfIndefiniteRankTwoSwitchingKernelWithUniformRemainder` |

## 1. 리만 가설

### 이번에 선언한 정확한 명제

닫힌 경계 `Gamma`를 호의 길이 `s`로 매개화하자. `X`, `P`는 경계와 내부에서
해석적이고 `P`는 경계에서 0이 아니라고 하자. 다음 상대오차를 둔다.

```text
r(s)=(X-P)/P
```

유한 표본 집합의 covering radius가 `delta`이고, 모든 표본에서 `|r|<=q`,
전체 경계에서 `|dr/ds|<=M`이면

```text
sup_Gamma |r| <= q+M delta
```

이다. 따라서 `q+M delta<1`이면 엄밀한 Rouché 부등식이 성립하고,
TICKET-203의 영점 목록 소진 정리에 입력할 수 있다.

### 증명

임의의 경계점 `s`에서 거리가 `delta` 이하인 가장 가까운 표본 `s_j`를
고른다. 미적분학의 기본정리와 도함수 상계로

```text
|r(s)| <= |r(s_j)| + integral_[s_j,s] |r'(u)|du
       <= q+M delta
```

를 얻는다. 이것은 통계적 보간이 아니라 결정론적 연속 상계다.

### 정확한 인증 회귀

단위원에서 다음을 사용한다.

```text
P(z)=1, X(z)=1+z^2/10, r(z)=z^2/10
```

등간격 표본 16개에 대해 `q=1/10`, `M=1/5`이고 covering radius는
`pi/16<=11/56`이다. 그러므로

```text
sup |r| <= 1/10+(1/5)(11/56)=39/280<1
```

이며 Rouché margin은 적어도 `241/280`이다.

### 유한 표본 no-go

정칙성 상계가 없으면 유한 표본만으로 경계 전체를 인증할 수 없다. 단위원에서

```text
P(z)=1, X(z)=z^8, r(z)=z^8-1
```

로 두자. 여덟 개의 8차 단위근 표본에서는 모두 `r=0`이다. 그러나 중간점
`z=exp(pi i/8)`에서는 `|r|=2`다. 또한 `P`의 내부 영점은 0개, `X`는
중복도 8의 영점을 갖는다. 표본만 사용하는 규칙은 이 정확한 다항식 예제에서
잘못된 영점수 전달을 인증하게 된다.

### 남은 간극

실제 완성 제타함수에 대한 비교함수도, `(Xi-P)/P`의 cofinal 도함수 상계도
구성하지 못했다. Platt--Trudgian의 높이 `3*10^12`까지의 엄밀한 유한 검증은
중요한 계산 결과지만, 그 자체로 이 무한 analytic 상계를 주지는 않는다.

## 2. 콜라츠 추측

### 이번에 선언한 정확한 명제

양의 accelerated valuation word `a=(a_0,...,a_(h-1))`에 대해

```text
B(a)=sum_m 3^(h-1-m)2^P_m
D(a)=2^sum(a)-3^h
P_m=a_0+...+a_(m-1)
```

로 둔다. `rho(a)`가 왼쪽 순환 회전이면

```text
2^a_0 B(rho(a))=3B(a)+D(a)
```

이다. `D`는 2, 3과 서로소이므로

```text
D | B(a) iff D | B(rho(a))
```

이다. 또한 `a=u^k`, `u`의 길이가 `r`, valuation 합이 `s`이면

```text
B(a)=B(u)G
D(a)=D(u)G
G=sum_(j=0)^(k-1)3^(r(k-1-j))2^(sj)
```

이다. 따라서 유리 cycle 값 `B/D`와 정수성은 word 반복으로 변하지 않는다.
모든 주기 valuation 후보는 하나의 원시 순환 necklace로 정확히 축약된다.

### 증명

가속 단계 하나는 `x=B(a)/D`를 `(3x+1)/2^a_0`으로 보내며, 이 값은 회전된
word의 cycle 값이다. 공통 분모를 제거하면 회전 항등식을 얻는다. 한편

```text
F_u(x)=(3^r x+B(u))/2^s
```

를 `k`번 합성하면 분자와 분모에 같은 등비 합 `G`가 나타난다.

### 재현 가능한 감사

valuation `{1,2,3,4}`, 길이 2∼8, 양의 `D`를 갖는 raw word 86,439개를
정확 정수 산술로 검사했다. 회전 항등식 실패와 반복 인수분해 실패는 모두
0개다. 전체 길이를 합치면 순환 necklace 11,445개가 서로 다른 원시 root
11,336개로 줄어 109개의 길이 간 반복을 제거한다. 각 검사 길이에서 가분
word는 all-two 하나뿐이지만, 이 마지막 관찰은 유한 계산 결과일 뿐이다.

### no-go와 남은 간극

회전과 반복은 독립적인 cycle 배제 증거로 셀 수 없다. 이 축약은 주기 word만
다룬다. 모든 길이의 non-all-two 원시 necklace에 대한 비가분성을 증명하지
않았고 비주기적 발산 궤도도 다루지 않았다.

## 3. 강한 골드바흐 추측

### 이번에 선언한 정확한 명제

`E(X)`를 `X` 이하의 짝수 골드바흐 예외 개수라고 하자. `X_0`까지 정확히
검증했고 모든 `X>=X_0`에서

```text
0<=E(X)-E(X_0)<1
```

인 엄밀한 tail 상계가 있으면 tail 예외 개수는 항상 정수 0이다. 따라서 강한
골드바흐 추측이 따른다.

### 정확한 임계값 증명

tail 예외 개수는 음이 아닌 정수다. 1보다 작은 유일한 값은 0이다. 엄격한
부등식이 핵심이다. 예외가 정확히 하나인 모형은 `E(X)<=1`이고
`E(X)/X->0`이지만 전칭 명제는 거짓이다. 2의 거듭제곱마다 예외를 둔 모형은
무한히 많은 실패를 가지면서도 예외 밀도가 0으로 간다.

이 no-go는 exceptional-set 상계에서 전칭 명제로 넘어가는 논리에 관한 것이다.
두 모형은 실제 소수 산술도 아니고 골드바흐 반례도 아니다.

### 재현 가능한 유한 산술

정확한 sieve로 10,000 이하의 모든 짝수를 검사했다. 예외는 0개다. ordered
표현 수의 최솟값은 1, 10,000 이하 최댓값은 658이다. 이 유한 계산은 구현을
검증할 뿐 무한 tail을 통제하지 않는다.

### 남은 간극

현재의 exceptional-set 추정이나 밀도 0 결론은 엄격한 subunit 임계값에
도달하지 않는다. 필요한 다음 결과는 1보다 작은 명시적 tail 예외 상계 또는
동치인 점별 major-arc/minor-arc 지배 정리다. 2026년 Grimmelt--Bhowmik의
연구는 명시적 major-arc 공식과 power-saving exceptional-set 결과의 경계를
제공하지만, 여기서 요구하는 all-target subunit 상계를 증명하지 않는다.

## 4. 쌍둥이 소수 추측

### 이번에 선언한 정확한 명제

`K(a,b)`를 형식적 인수 label 위의 대칭 positive-semidefinite(PSD, 양의
준정부호) kernel이라고 하자. 모든 반소수 채널에 엄격한 음수 부호를 주려면
소수 제곱 `p^2`에 대해

```text
K(p,p)<0
```

이어야 한다. 그러나 PSD diagonal은 `K(p,p)>=0`이다. 따라서 PSD 또는
제곱형 bilinear kernel은 소수와 모든 `P_2` 채널을 엄격한 부호로 분리할 수
없다.

### indefinite rank-2 대수적 탈출

인수 쌍이 노출된 형식적 채널에서

```text
s(1)=1, s(p)=-1/2
K(a,b)=s(a)+s(b)
```

로 둔다. 그러면

```text
K(1,p)=1/2>0
K(p,q)=-1<0
```

이다. 행렬은 `s 1^T+1 s^T`이므로 rank가 2 이하이다. `{1,p}` 주부분행렬의
determinant는

```text
2(-1)-(1/2)^2=-9/4
```

이므로 이 탈출 kernel은 PSD가 아니라 indefinite다. `{1,2,3,5,7,11}`에
대한 정확 행렬의 rank는 2이며 위 부호를 모두 만족한다.

### no-go와 남은 간극

이 탈출은 인수 쌍을 이미 알고 있는 형식적 대수 결과다. `n`만으로 계산되는
weight가 아니며 sieve 분해, level of distribution, switching remainder 상계를
제공하지 않는다. 현대 weighted switching 연구는 bilinear 인수 구조가 왜
중요한지 보여 주지만 거의소수를 검출할 뿐 쌍둥이 소수 하한을 증명하지 않는다.
다음 보조정리는 indefinite 인수 kernel을 산술적으로 구현하고 양의 main term보다
작은 uniform remainder를 증명해야 한다.

## 재현 방법

```bash
python scripts/ticket204_mesh_necklace_exceptional_kernel.py
python -m unittest tests.test_ticket204_mesh_necklace_exceptional_kernel
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

예상 기계 상태는 다음과 같다.

```text
exact_partial_theorem_count = 4
refuted_or_limited_route_count = 4
conjecture_resolution_count = 0
total_failure_count = 0
```

## 1차 자료 배경

- D. Platt, T. Trudgian, [높이 `3*10^12`까지의 리만 가설 검증](https://arxiv.org/abs/2004.09765).
- J. C. Lagarias, [3x+1 문제와 그 일반화](https://doi.org/10.2307/2322189).
- L. Grimmelt, G. Bhowmik, [골드바흐 문제의 exceptional set](https://arxiv.org/abs/2607.27282).
- K. Matomäki, S. Zuniga Alterman, [switching을 이용한 weighted sieve](https://arxiv.org/abs/2405.19063).

이 자료들은 알려진 연구 경계를 설정하기 위해 사용했다. 이 문서의 결과를 상위
난제의 해결이나 동료심사를 거친 신규 정리라고 주장하지 않는다.
