# TICKET-205: winding 인증, cycle 극값, 유한 증인, Omega 가중치

## 주장 상태

네 상위 추측은 모두 `open_not_proven`, 즉 **미해결**이다. TICKET-205는 세
개의 정확한 환원·no-go 정리와 하나의 정확한 유한 골드바흐 정리를 증명한다.
리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않는다.

표준 기계 판독 산출물은
[`ticket205-winding-extremal-finite-omega.json`](../data/open-problem/ticket205-winding-extremal-finite-omega.json)이다.

| 문제 | TICKET-205의 정확 결과 | 폐기한 경로 | 결정적인 다음 보조정리 |
|---|---|---|---|
| 리만 | 구간별 도함수 상계로 표본 다각형의 winding과 해석함수 경계의 winding이 같음을 인증한다 | 유한 경계값만으로 winding을 추론 | `CompletedZetaCofinalZeroFreeContourWindingCertificate` |
| 콜라츠 | 비자명 양의 cycle의 최솟값에서는 valuation이 1, 최댓값에서는 2 이상이다. 모든 valuation이 2 이상인 word는 자명 cycle뿐이다 | 모든 valuation이 2 이상인 주기 영역 탐색 | `UniformNondivisibilityForPrimitiveMixedValuationNecklaces` |
| 골드바흐 | 10,000,000 이하 모든 짝수에 명시적 최소 소수 증인이 있고 전체 증인 stream의 SHA-256을 재현할 수 있다 | 유한 prefix를 무한 전칭 명제로 승격 | `ExplicitBinaryGoldbachTailExceptionalCountStrictlyBelowOne` |
| 쌍둥이 소수 | `W(n)=2-(3/2)Omega(n)`이 소수·반소수 부호를 구현하지만 shift-2 곱에는 무한한 합성수 거짓 양성이 있다 | 양수인 raw switching 곱을 twin 지시자로 사용 | `UniformCompositeCompositeCancellationForOmegaSwitchingCorrelation` |

## 1. 리만 가설

### 이번에 선언한 정확한 명제

`Gamma`를 양의 방향의 rectifiable Jordan contour(길이가 유한한 단순 닫힌
경계)라고 하고, 호의 길이에 대한 절대연속 매개화를 사용하자. `f`는 경계와
내부에서 해석적이다. 경계를 시작점 `z_j`, 길이 `h_j`인 호 `Gamma_j`로
나누고 다음을 가정한다.

```text
|f(z_j)| >= m_j > 0
|d(f o Gamma)/ds| <= M_j  (Gamma_j에서 거의 모든 점)
M_j h_j < m_j
```

그러면 각 해석적 image arc와 두 표본값을 잇는 chord(현)는 0을 피하면서
끝점을 고정한 채 연속 변형할 수 있다. 따라서

```text
wind(f(Gamma),0) = wind(표본 다각형,0)
```

이고, argument principle(편각 원리)에 따라 이 정수는 내부 영점의 중복도를
포함한 개수다.

### 증명

`Gamma_j` 위 임의의 `z`에 대해 절대연속성과 도함수 상계로

```text
|f(z)-f(z_j)| <= M_j h_j < m_j <= |f(z_j)|
```

를 얻는다. 따라서 실제 image arc 전체는 중심이 `f(z_j)`이고 0을 포함하지
않는 열린 원판 안에 있다. 끝점과 chord도 같은 볼록 원판에 있다. 각 arc를
chord로 바꿔도 0을 지나지 않으므로 winding은 보존된다.

### 정확한 회귀와 no-go

단위원에서 `f(z)=z^3`을 택하고 표본 24개를 둔다. 경계 도함수의 크기는
3이고 각 호의 길이는

```text
pi/12 <= 11/42
```

이므로 image 이동량은 `11/14` 이하, 0 회피 margin은 `3/14` 이상이다.
연속 표본값의 위상은 한 바퀴의 `1/8`씩 증가하므로 표본 다각형의 winding은
정확히 3이고 내부 영점 3개를 인증한다.

정칙성 정보는 필수다. 함수 `1`과 `z^8`은 모든 8차 단위근에서 같은 값을
갖지만 winding은 각각 0과 8이다. 유한 값만 보는 규칙은 둘을 구별할 수 없다.

### 남은 간극

완성 제타함수에 대해 0을 피하는 cofinal contour family와 구간별 도함수 상계를
구성하지 못했다. 유한 높이 영점 검증은 이 무한 정리를 대신하지 않는다.

## 2. 콜라츠 추측

### 이번에 선언한 정확한 명제

양의 accelerated cycle을

```text
x_(i+1)=(3x_i+1)/2^a_i
a_i=v_2(3x_i+1)
```

로 쓰자. 모든 비자명 cycle에서 다음이 성립한다.

1. 최솟값이 나타나는 모든 위치의 다음 valuation은 `1`이다.
2. 최댓값이 나타나는 모든 위치의 다음 valuation은 `2` 이상이다.

따라서 비자명 주기 valuation necklace에는 `1`과 `2` 이상의 항이 모두 있어야
한다. 모든 valuation이 2 이상인 양의 정수 cycle word는 `(2)`의 반복이고
고정 cycle `1`만 나타낸다.

### 증명

최솟값을 `m`, 다음 값을 `m'`이라 하자. valuation `a>=2`이면

```text
3m+1=2^a m' >= 4m
```

이므로 `m<=1`이다. 양의 홀수이므로 `m=1`이고, 같은 식에서 `a=2`, `m'=1`이
강제된다. 결정론적 궤도 전체가 자명 cycle이므로 비자명 최솟값에서는 `a=1`이다.

최댓값 `M`에서 `a=1`이면

```text
M'=(3M+1)/2>M
```

이어서 모순이다. 따라서 `a>=2`다.

TICKET-204는 순환 회전에 대한 가분성 불변성을 증명했다. 그러므로 affine
분모 `D>0`가 분자 `B`를 나누면 모든 순환 상태 `B/D`가 양의 홀수 정수이고
해당 word는 정확한 accelerated cycle이다. 위 극값 정리가 all-`>=2` word를
all-2 반복만 남기고 전부 배제한다.

### 재현 감사와 남은 간극

회귀 검사로 `{2,3,4,5}` 위 길이 1∼8의 word 87,380개를 모두 계산했다.
가분 word는 길이마다 all-2 하나씩 총 8개이고 non-all-2 적중은 0개다. 전 길이
배제는 이 유한 계산이 아니라 극값 증명에서 나온다.

남은 주기 영역은 `1`과 더 큰 valuation을 함께 갖는 원시 mixed necklace다.
비주기적 발산 궤도는 전혀 배제하지 못했다.

## 3. 강한 골드바흐 추측

### 정확한 유한 정리

다음 범위의 모든 짝수 `N`은 두 소수의 합이다.

```text
4 <= N <= 10,000,000
```

총 4,999,999개 대상마다 `N-p`도 소수가 되는 가장 작은 `p<=N/2`를 찾았다.
전체 증인 stream은 실행할 때 다시 만들며, 안정적인 식별자는 다음과 같다.

```text
SHA-256 ed31375c2d840a190345e901dfaf52e322424d40d7b4afa33ec7977cf0b791dd
```

가장 큰 최소 증인은 `N=3,807,404`에서 처음 필요한 `p=751`이다. 마지막
대상은

```text
10,000,000 = 29 + 9,999,971
```

이다. 해시는 재현 실행을 식별할 뿐, 증인 검사를 다시 수행하는 것을 대신하는
압축 증명이 아니다.

### 유한 prefix no-go

임의의 유한 상한 `B`에 대해 `B` 이하 모든 짝수에서 일치하고 `B+2`에서
처음 달라지는 두 Boolean 모형을 만들 수 있다. 따라서 아무리 큰 유한 prefix도
골드바흐의 무한 tail을 결정하지 않는다.

### 남은 간극

TICKET-204는 명시적 tail 예외 개수 상계가 엄격히 1보다 작으면 추측이
닫힌다는 정수 승격 정리를 증명했다. TICKET-205는 독립 재현 가능한 유한
경계를 천만으로 올렸지만 tail exceptional-set 상계나 점별 major/minor-arc
지배를 전혀 증명하지 못했다.

## 4. 쌍둥이 소수 추측

### 이번에 선언한 정확한 명제

`d=p^k`, `k>=1`인 소수 거듭제곱일 때 `Q(d)=1`, 아니면 0으로 두면

```text
Omega(n)=sum_(d|n) Q(d)
```

이다. 따라서 인수 쌍을 미리 노출하지 않는 산술 가중치

```text
W(n)=2-(3/2)Omega(n)
```

는 TICKET-204의 형식 부호를 정확히 구현한다.

```text
W(p)=1/2       (소수 p)
W(pq)=-1       (p=q인 경우를 포함한 반소수 pq)
```

### 증명과 parity no-go

`n=product p^e`라 하자. 한 소수 `p`에 속하면서 `n`을 나누는 소수 거듭제곱은
정확히 `p,p^2,...,p^e`이므로 divisor sum에 `e`를 더한다. 모든 소수에 대해
합하면 `Omega(n)`이다.

그러나 이 부호 구현은 쌍둥이 소수를 분리하지 못한다. 모든 `k>=2`에 대해

```text
n=3+15k, n+2=5+15k
```

이다. 첫 수는 3의 진약수 배수, 둘째 수는 5의 진약수 배수이므로 둘 다
합성수이고 `Omega>=2`다. 두 가중치가 모두 음수여서 `W(n)W(n+2)>0`이다.
따라서 raw product 판정에는 무한한 합성수-합성수 거짓 양성 계열이 있다.

### 남은 간극

TICKET-205는 TICKET-204의 exposed-factor kernel을 정확한 `n`의 함수로
바꿨다. 그러나 가중치는 `Omega(n)`이 커질수록 아래로 유계가 아니고,
상관합에는 합성수-합성수 질량이 섞인다. 이 질량을 제거하고 양의 소수-소수
main term보다 작은 uniform remainder를 증명해야 한다. 그런 정리는 아직 없다.

## 재현 방법

```bash
python scripts/ticket205_winding_extremal_finite_omega.py
python -m unittest tests.test_ticket205_winding_extremal_finite_omega
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

예상 기계 상태:

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

이 자료들은 알려진 연구 경계를 설정한다. 독립 전문가 검토 없이 TICKET-205를
동료심사를 거친 신규성 주장이나 난제 해결로 제시하지 않는다.
