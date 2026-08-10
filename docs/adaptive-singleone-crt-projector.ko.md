# TICKET-206: 적응형 인증, 단일-1 주기, CRT 증인, Omega projector

## 주장 상태

네 상위 추측은 모두 `open_not_proven`, 즉 **미해결**이다. TICKET-206는 네
개의 정확한 부분정리 또는 no-go 정리를 증명한다. 리만 가설, 콜라츠 추측,
강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않는다.

표준 기계 판독 산출물은
[`ticket206-adaptive-singleone-crt-projector.json`](../data/open-problem/ticket206-adaptive-singleone-crt-projector.json)이다.

| 문제 | 새로 확정한 결과 | 해결 상태 | 폐기한 경로 | 남은 간극 | 다음 단일 보조정리 |
|---|---|---|---|---|---|
| 리만 | 영점이 없는 고정 compact 경계에는 유한한 도함수 인증 winding mesh가 존재하며, 고정 분할 예산은 clearance의 역수 규모에서 실패한다 | 미해결 | clearance와 무관한 고정 경계 분할 수 | cofinal 완성 제타 경계의 유효한 엄밀 상계 | `EffectiveCompletedZetaRectangleBoundsAndCofinalAdaptiveTermination` |
| 콜라츠 | valuation `1`이 정확히 한 번이고 나머지가 임의의 `>=2`인 양의 비자명 cycle은 없다 | 미해결 | 단일-`1` 주기 영역의 추가 탐색 | `1`이 둘 이상인 mixed 원시 necklace와 비주기 발산 | `UniformNondivisibilityForPrimitiveMixedNecklacesWithAtLeastTwoOnes` |
| 골드바흐 | 모든 `B`에 대해 Goldbach 증인이 존재한다면 반드시 `B`보다 커야 하는 무한 CRT 등차수열이 있다 | 미해결 | 고정된 유한 소수 증인 집합 | 증가하는 증인 cutoff를 갖는 tail 예외 개수 `1` 미만 상계 | `GrowingWitnessCutoffGoldbachTailExceptionalCountStrictlyBelowOne` |
| 쌍둥이 소수 | `Omega`의 이항 반전은 정확한 소수 projector지만 모든 유한 절단에는 무한한 양의 합성수-합성수 shift-2 거짓 양성이 있다 | 미해결 | 고정 유한 `Omega` 절단을 정확한 twin 지시자로 사용 | 무한 projector tail의 균일 상쇄 | `UniformTailCancellationForBinomialOmegaProjectorCorrelation` |

## 1. 리만 가설

### 이번에 증명한 정확한 명제

`gamma:[0,L]->C`를 단위속도 `C1` 닫힌 경계라 하고, 경계 근방에서 해석적인
`f`에 대해 `g=f o gamma`라 하자. 경계에서 `g`가 0이 아니면 compactness,
즉 닫혀 있고 유계인 구간의 연속성으로

```text
delta=min_t |g(t)|>0
K=max_t |g'(t)|<무한대
```

가 된다. `K>0`이면 균일 이분할을 반복하여 mesh 크기 `h<delta/K`를 얻을 수
있고, 모든 구간이 TICKET-205의 0 회피 원판 조건을 만족한다. 따라서 표본
다각형의 winding number(감김수)는 실제 해석함수 image의 winding과 정확히
같다. `K=0`이면 경계 image가 0이 아닌 상수다.

즉 엄밀한 양의 clearance와 도함수 상계를 공급할 수 있다는 조건 아래에서,
도함수 기반 winding 인증 문법은 모든 고정된 영점 없는 compact 경계에 대해
유한 종료한다.

### 증명

시작점 `t_j`인 한 구간에서 미적분학의 기본정리에 의해

```text
|g(t)-g(t_j)|<=K h<delta<=|g(t_j)|
```

이다. 실제 image 구간과 두 끝점을 잇는 현은 모두 0을 포함하지 않는 같은
볼록 원판에 있다. 모든 image 구간을 현으로 바꾸어도 winding이 보존된다.
이분할 mesh는 0으로 수렴하므로 유한 단계 뒤 `h<delta/K`가 된다.

### 정확한 복잡도 no-go

단위원에서 `epsilon=1/q`와

```text
f_epsilon(z)=z-(1-epsilon)
```

을 사용하자. 경계 clearance는 `epsilon`, 호의 길이에 대한 도함수 상계는
`1`, winding은 `1`이다. 전역 mesh 조건은

```text
2*pi/N<epsilon
```

이다. 정확한 유리수 상계 `3<pi<22/7`만 사용하면

```text
N<=6q  이면 조건 실패
N=8q   이면 조건 성공
```

이다. 따라서 `epsilon`이 0으로 가까워질 때 하나의 고정된 전역 분할 예산은
이 계열을 인증하지 못한다. 이는 해당 도함수/clearance 인증 조건의 복잡도
하한이며, 모든 가능한 해석적 방법에 대한 하한은 아니다.

### 남은 간극

완성 제타 함수의 cofinal rectangle family에 대해 양의 clearance를 엄밀하게
출력하는 interval oracle을 만들지 못했다. 원하는 영점 부재를 가정하지 않고
그 상계를 만드는 것이 결정적인 미해결 단계다.

## 2. 콜라츠 추측

### 이번에 증명한 정확한 명제

accelerated odd map(짝수 나눗셈을 한 번에 수행한 홀수 콜라츠 사상)

```text
T(x)=(3x+1)/2^v2(3x+1)
```

의 양의 비자명 cycle 중 valuation `1`이 정확히 한 번이고 나머지 valuation이
모두 `2` 이상인 cycle은 없다.

### 증명

길이 `h`인 가상 cycle을 최소 홀수 `m`에서 시작하도록 회전한다. TICKET-205에
따라 비자명 최솟값의 다음 valuation은 `1`이며, 가정상 이것이 유일한 `1`이다.

```text
y=(3m+1)/2
F(x)=(3x+1)/4
```

로 두자. 뒤의 모든 단계는 valuation이 2 이상이므로 `F` 이하이다.
`q=(3/4)^(h-1)`라 하면 `m`으로 돌아오기 위해

```text
m<=F^(h-1)(y)=1-q/2+(3q/2)m
m<=(1-q/2)/(1-3q/2)
```

가 필요하다. `h>=4`이면 `q<=27/64<1/2`이므로 오른쪽은 엄격히 `3`보다
작다. 그러나 양의 비자명 최소 홀수는 적어도 `3`이어서 모순이다.

남은 짧은 길이는 직접 닫힌다.

- `h=3`: `m<=23/5`이므로 `m=3`뿐이지만 `3 -> 5 -> 1`이다.
- `h=2`: 다른 valuation을 `b>=2`라 하면 `(2^(b+1)-9)m=5`인데 양의 정수해가 없다.
- `h=1`: valuation-1 고정점 식은 `m=-1`을 준다.

증명은 나머지 valuation의 크기에 상한을 두지 않는다. `{1,2,3,4,5}`에서
길이 1∼8이고 `1`이 정확히 하나인 word 167,481개의 정수 cycle 적중 수가
0인 계산은 증명이 아니라 회귀 검사다.

### 남은 간극

가상 비자명 양의 cycle은 이제 valuation `1`을 적어도 두 번 포함하고,
`2` 이상인 항도 포함해야 한다. 이 mixed necklace들과 모든 비주기 발산 궤도는
여전히 미해결이다.

## 3. 강한 골드바흐 추측

### 이번에 증명한 정확한 명제

모든 정수 상한 `B`에 대해, 모든 소수 `p<=B`에 대한 `N-p`가 합성수인 짝수
`N`의 무한 등차수열이 존재한다. 따라서 고정된 유한 소수 집합만으로 모든 큰
Goldbach 대상을 표현할 수 없다. 강한 골드바흐가 참이라면 최소 소수 증인의
크기는 무한히 커져야 한다.

### 증명

각 홀수 소수 `p<=B`마다 서로 다른 홀수 소수 `q_p>B`를 고른다. 중국인의
나머지 정리(CRT)에 의해 다음 합동식을 동시에 만족하는 하나의 residue class가
존재한다.

```text
N=0 (mod 2)
N=p (mod q_p), 모든 홀수 소수 p<=B
```

대표값을 모든 `p+q_p`보다 크게 고르면 `N-p`는 `q_p`의 진배수이므로
합성수다. `N-2`도 2보다 큰 짝수이므로 합성수다. 다음 modulus의 배수를 더해도
모든 조건이 보존된다.

```text
M=2*product_(p<=B, p는 홀수 소수) q_p
```

따라서 이런 `N`이 무한히 많다.

### 논리적 한계

이는 골드바흐 반례가 아니다. 구성은 `B` 이하의 증인만 막으며, 더 큰 소수가
각 `N`을 표현할 수 있다. 정확한 결론은 tail 분석의 증인 cutoff가 `N`과 함께
증가해야 한다는 것이다. TICKET-205에서 천만 이하 최대 최소 증인이 `751`인
사실도 보편 상계로 승격할 수 없다.

## 4. 쌍둥이 소수 추측

### 이번에 증명한 정확한 명제

`m>=0`에 대해

```text
P_infinity(m)=sum_(j>=1) (-1)^(j-1) j binom(m,j)
```

라 하자. 각 `m`에서 합은 유한하고

```text
P_infinity(m)=1  (m=1)
P_infinity(m)=0  (m!=1)
```

이다. 따라서 `P_infinity(Omega(n))`은 정확한 소수 지시함수(projector)다.
그러나 `j<=R`에서 자른 유한 절단

```text
P_R(m)=sum_(1<=j<=R) (-1)^(j-1) j binom(m,j)
```

은 `m<=R`에서만 정확하고, `m>R`이면

```text
P_R(m)=(-1)^(R-1) m binom(m-2,R-1)
```

이다. 모든 고정 `R`에 대해 `n`과 `n+2`가 모두 적어도 `R+1`개의 서로 다른
소인수를 가지며 `P_R(Omega(n))P_R(Omega(n+2))>0`인 무한 등차수열이 있다.

### 증명

다음 항등식을 쓴다.

```text
j binom(m,j)=m binom(m-1,j-1)
```

완전한 교대합은 `(1-x)^m`을 미분하고 `x=1`을 대입한 항등식이다. 유한
교대 이항합 공식은 `m>R`에서 위 닫힌식을 준다.

shift-2 no-go를 위해 서로 겹치지 않는 `R+1`개 홀수 소수 집합 둘의 곱을
`A`, `B`라 하자. CRT는

```text
n=0 (mod A)
n=-2 (mod B)
```

를 동시에 푼다. 충분히 큰 대표값에서는 양 끝이 모두 합성수이고
`Omega>R`이다. 두 절단 projector의 부호가 모두 `(-1)^(R-1)`이므로 곱은
양수다. 또한 `Omega`의 고정 차수 다항식으로 정확한 소수 지시함수를 만들 수
없다. 그런 다항식은 `0,2,3,...`에서 무한히 많은 근을 가지면서 `1`에서는
1이어야 하므로 모순이다.

### 남은 간극

정확한 무한 projector는 소수성을 다시 쓴 항등식일 뿐 쌍둥이 소수 하한이
아니다. shift-2 상관에서 합의 순서를 바꾸거나 유한 절단을 사용하려면 tail의
균일 상쇄 정리가 필요하다. 이번 결과는 그 정리를 증명하지 못했다.

## Proof DAG(증명 의존성 그래프)

각 기계 산출물은 다음 다섯 상태를 그대로 저장한다.

```text
TICKET-205에서 닫힌 결과
        |
        v
TICKET-206 정확 정리 ---> 폐기 또는 제한한 경로
        |
        v
가장 위험한 단일 미해결 보조정리
        |
        v
상위 추측 [open_not_proven]
```

네 DAG 모두의 마지막 노드는 의도적으로 미해결 상태다.

## 재현 방법

```bash
python scripts/ticket206_adaptive_singleone_crt_projector.py
python -m unittest tests.test_ticket206_adaptive_singleone_crt_projector
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

예상 기계 상태:

```text
exact_partial_theorem_count = 4
refuted_or_limited_route_count = 4
proof_dag_count = 4
conjecture_resolution_count = 0
total_failure_count = 0
```

## 1차 자료 배경

- D. Platt, T. Trudgian, [높이 `3*10^12`까지의 리만 가설 검증](https://arxiv.org/abs/2004.09765).
- J. C. Lagarias, [3x+1 문제와 그 일반화](https://doi.org/10.2307/2322189).
- L. Grimmelt, G. Bhowmik, [골드바흐 문제의 exceptional set](https://arxiv.org/abs/2607.27282).
- K. Matomäki, S. Zuniga Alterman, [switching을 이용한 weighted sieve](https://arxiv.org/abs/2405.19063).

이 자료들은 알려진 연구 경계를 설정한다. 독립 전문가 검토 없이 TICKET-206을
동료심사를 거친 신규성 주장이나 난제 해결로 제시하지 않는다.
