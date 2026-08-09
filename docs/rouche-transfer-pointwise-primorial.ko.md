# TICKET-203: Rouché 전달, 부호 있는 valuation 이동, 점별 목표 교정

## 주장 상태

네 상위 추측의 상태는 모두 `open_not_proven`, 즉 **미해결**이다.
TICKET-203은 네 개의 부분정리 또는 no-go 정리를 증명하지만, 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 완전히
증명하거나 반증하지 않는다.

표준 기계 판독 산출물은
[`ticket203-rouche-transfer-pointwise-primorial.json`](../data/open-problem/ticket203-rouche-transfer-pointwise-primorial.json)이다.

이번 라운드는 TICKET-202가 제안한 각 “다음 보조정리”가 논리적으로 충분한지,
그리고 원래 추측보다 실제로 쉬운 목표인지 다시 검사한다. 그 결과 두 경로는
정확한 조건을 보강해 유지하고, 두 경로는 강도가 잘못 설정되어 교체한다.

| 문제 | TICKET-203에서 확립한 결과 | 경로 결정 | 다음 미해결 보조정리 |
|---|---|---|---|
| 리만 | 인증된 포함 영점과 Rouché 영점수가 합쳐지면 영역 내 영점 목록이 완전함 | 전달 논리는 유지, 포함 인증 없는 단순 영점수 비교는 폐기 | `CompletedZetaCofinalRelativeMarginCertificateFamily` |
| 콜라츠 | 두 위치 valuation 이동의 정확 항등식, 보편 불변성은 `(3,1)->(2,2)`로 반증 | 무조건적 transfer 불변성 폐기 | `ScaleDependentTransferResidueBarrierOutsideAllTwoOrbit` |
| 골드바흐 | 점별 양의 결손은 Goldbach 양성과 정확히 동치, 고정 `c/log log N` 하한은 더 강함 | scaled bound를 쉬운 보조정리로 취급하는 경로 폐기 | `UniformPointwiseGoldbachMinorArcDominanceOverExplicitMajorArc` |
| 쌍둥이 소수 | 고정 primorial의 단일 좌표 정보로 모든 소수와 rough 반소수를 분리할 수 없음 | 고정 local 분리 폐기, switching 유지 | `ScaleGrowingBilinearSwitchingWeightWithSignedPrimeSemiprimeCorrelation` |

## 1. 리만 가설

### 이번에 선언한 정확한 명제

단순 폐곡선 `Gamma`의 내부와 경계에서 해석적인 두 함수 `X`, `P`가 다음을
만족한다고 하자.

1. `Gamma` 위에서 `|X-P|<|P|`이다.
2. `P`는 내부에 중복도를 포함해 정확히 `m`개의 영점을 갖는다.
3. 별도의 엄밀한 인증으로 `X`의 내부 영점 `m`개가 이미 확인되어 있다.

그러면 이 인증 목록은 `Gamma` 내부의 `X` 영점을 모두 포함한다.

### 증명

Rouché 정리에 의해

```text
N_Gamma(X) = N_Gamma(P) = m
```

이다. 이미 확인한 `X`의 영점 목록은 전체 내부 영점 multiset의 부분집합이고,
중복도 합이 벌써 `m`이다. 따라서 추가 영점은 존재할 수 없다.

여기서 **독립적인 영점 포함 인증**이 핵심이다. 두 함수의 전체 영점수가 같다는
사실만으로는 그 영점이 알려진 실수 영점인지, 다른 비실수 영점인지 결정할 수
없다.

`Xi(z)=xi(1/2+iz)`에 대해 `|Im z|<1/2`를 덮는 cofinal rectangle 족마다 이
계약을 인증하고, 포함된 모든 영점이 실수 `z`축 위에 있음을 별도로 인증하면
RH가 따른다. TICKET-203은 이 **논리적 전달**을 증명한다. 실제 Xi의 경계
margin은 만들지 못했다.

### 정확 회귀 예제

```text
P(z) = (z^2-1)(z^2-4)
X(z) = P(z)(1+z^2/100)
Gamma = {|Re z|<=3, |Im z|<=1}의 경계
```

경계에서 `|z|^2<=10`이므로

```text
|X-P|/|P| = |z|^2/100 <= 1/10 < 1.
```

두 함수는 내부의 `-2,-1,1,2`를 공통 영점으로 갖고, `X`의 추가 영점
`+/-10i`는 영역 밖에 있다. 정확한 Rouché margin은 `9/10`이다.

### 한계

이것은 조건부 영점 소진 정리와 합성 회귀 예제다. 실제 완성 제타함수에 대한
비교함수나 경계 하한을 제공하지 않는다. Platt--Trudgian과 같은 엄밀한 유한
높이 검증도 그 자체로 cofinal 인증은 아니다.

## 2. 콜라츠 추측

### 이번에 선언한 정확한 명제

양의 accelerated valuation word를

```text
a=(a_0,...,a_(h-1))
P_m=a_0+...+a_(m-1)
B(a)=sum_m 3^(h-1-m)2^P_m
D(a)=2^sum(a)-3^h
```

로 두자. `i<j`, `a_i>=2`이고 valuation 질량 1을 `i`에서 `j`로 옮겨
`a'=a-e_i+e_j`라 하면

```text
D(a')=D(a)
B(a')=B(a)-Q_(i,j)/2
Q_(i,j)=sum_(i<m<=j)3^(h-1-m)2^P_m
```

이다. 반대로 `j`에서 `i`로 한 단위를 옮기면

```text
B(a+e_i-e_j)=B(a)+Q_(i,j)
```

이다.

### 증명

앞에서 뒤로 옮길 때 정확히 `P_(i+1),...,P_j`만 1씩 감소한다. 따라서 해당
항의 2의 거듭제곱만 절반이 되고 다른 항은 변하지 않는다. 두 affine 분자
합을 빼면 `-Q/2`가 된다. 반대 이동에서는 같은 항들이 두 배가 되어 `+Q`가
된다. valuation 총합은 보존되므로 분모도 보존된다.

### 보편 obstruction의 최소 반례

“비가분성은 모든 signed transfer에서 보존된다”는 기대는 거짓이다.

```text
a=(3,1), D=2^4-3^2=7, B(a)=11
a'=(2,2), B(a')=7
```

즉 `7`은 `11`을 나누지 않지만 `7`을 나눈다. 도착 word는 알려진 all-two
가속 고정주기이며, 새로운 비자명 콜라츠 주기는 아니다.

### 재현 가능한 유한 감사

valuation 알파벳 `{1,2,3,4}`, 양의 분모, 길이 2부터 7까지 310,103개의
forward transfer를 정확 정수 산술로 검사했다. 항등식 실패는 0개다.
divisibility hit 수는

```text
1, 3, 6, 10, 15, 21 = binomial(h,2)
```

이고, 이 유한 상자에서 모든 hit는 all-two word로 들어간다. 이 관찰을 무한
길이 정리로 주장하지 않는다.

### 한계

임의의 주기 word를 배제하지 않았고, 비주기적 발산 궤도는 전혀 다루지 않았다.
다음 경로는 all-two 성분을 분리한 뒤 scale-dependent residue barrier를
증명해야 한다. 단순 transfer 불변성에는 의존할 수 없다.

## 3. 강한 골드바흐 추측

### 이번에 선언한 정확한 명제

Chen-positive 짝수 `N`에 대해 ordered prime-prime 표현 수를 `R(N)`, ordered
prime-semiprime 표현 수를 `S(N)`라 하고

```text
C(N)=R(N)+S(N)
L(N)=S(N)-R(N)
delta(N)=1-L(N)/C(N)
```

라 두면

```text
delta(N)=2R(N)/C(N)
R(N)>0 iff delta(N)>0
```

이다. 따라서 모든 충분히 큰 짝수에 대해 `delta(N)>=c/log log N`을 보이는
것은 이미 Goldbach를 함의하며, 단순 양성보다 정량적으로 강하다.

### 정확 channel 반모형

2의 거듭제곱인 `m`에 대해

```text
N=2^m, C=N/m, R=1, S=C-1, L=C-2
```

라 두자. 모두 비음이 아닌 정수이고 `R>0`이지만

```text
delta=2m/2^m.
```

`m>=2`에서 `log log(2^m)<=m`이므로

```text
delta log log N <= 2m^2/2^m -> 0.
```

따라서 projector 항등식과 표현 하나의 양성만으로 고정된 log-log scaled
하한을 얻을 수 없다. 이 모형은 실제 소수가 아니며 Goldbach 반례도 아니다.

### 교정한 경로

기존 scaled 목표가 실제 소수에서 거짓이라고 증명한 것이 아니다. 이를
Goldbach보다 쉬운 중간 보조정리로 취급하는 논리를 폐기한 것이다. 다음 목표는
모든 충분히 큰 짝수에서 explicit major-arc lower bound가 minor arcs를
지배한다는 점별 circle-method 부등식이다. 최신 exceptional-set 연구와 explicit
major-arc 공식만으로는 이 프로젝트에서 all-target 지배가 확보되지 않았다.

## 4. 쌍둥이 소수 추측

### 이번에 선언한 정확한 명제

`z`를 고정하고 `W=product_(p<=z)p`라 하자. `n mod W` 하나에만 의존하는
single-coordinate weight로 모든 소수와 인수가 모두 `z`보다 큰 모든 반소수를
분리할 수 없다.

### 증명

`W`와 서로소인 임의의 `a mod W`에 대해 Dirichlet의 산술진행 소수 정리는
다음 합동류에 충분히 큰 소수들을 제공한다.

```text
p=a mod W
q=1 mod W
r=a mod W
```

그러면 `p`는 소수, `qr`은 rough 반소수이지만 `p=qr=a mod W`다. 두 수는 full
residue와 모든 작은 소수 divisibility signature가 같다. 따라서 이 고정
signature의 함수는 두 대상에 같은 weight를 줄 수밖에 없다.

### 정확 유한 collision

기계 산출물은 `z=11`, `W=2310`까지 예제를 저장한다.

```text
2311은 소수
4621은 소수
2311*4621 = 10,679,131은 반소수
2311 = 10,679,131 = 1 (mod 2310)
```

### 한계

이 no-go는 고정 local single-coordinate 정보에만 적용된다. scale-growing sieve
level, bilinear switching, 첫 번째 소수 좌표와의 상관, 분포 추정에는 적용되지
않는다. 따라서 Matomäki--Zuniga Alterman의 switching framework를 반박하지
않으며, 쌍둥이 소수의 반례도 찾지 않았다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket203_rouche_transfer_pointwise_primorial.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket203_rouche_transfer_pointwise_primorial -v
```

예상 요약은 다음과 같다.

```text
정확 부분정리: 4
Collatz exact forward transfer: 310103
Goldbach 실제 target: 4
Goldbach 추상 반모형: 5
Twin primorial collision: 5
해결된 추측: 0
감사 실패: 0
```

## 문헌 경계

- D. Platt, T. Trudgian, [The Riemann hypothesis is true up to
  `3*10^12`](https://arxiv.org/abs/2004.09765): 엄밀한 유한 높이 영점 인증.
- J. C. Lagarias, [The `3x+1` problem and its
  generalizations](https://doi.org/10.2307/2322189): 콜라츠 affine 및 동역학의
  기존 배경.
- L. Grimmelt, G. Bhowmik, [The exceptional set of the Goldbach
  problem](https://arxiv.org/abs/2607.27282): 최신 exceptional-set 맥락과
  explicit major-arc 공식.
- K. Matomäki, S. Zuniga Alterman, [Weighted sieves with
  switching](https://arxiv.org/abs/2405.19063): 유지할 비국소 Twin 경로.

독립적인 전문가 검토 전에는 TICKET-203에 대한 문헌 우선권을 주장하지 않는다.
Rouché 원리와 고정 sieve parity barrier는 기존 수학이다. 이 프로젝트가 현재
주장하는 기여는 정확한 proof contract, 잘못된 목표 강도의 교정, 재현 가능한
회귀, 명시적인 주장 경계다.
