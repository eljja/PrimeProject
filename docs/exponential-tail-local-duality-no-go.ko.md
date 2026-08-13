# TICKET-223: 지수 꼬리, 국소 쌍대성, 고정 체의 한계 정리

## 상태와 주장 범위

TICKET-223은 TICKET-222에서 남긴 네 개의 핵심 보조정리를 이어서
공격한다. 이번 티켓은 정확한 부분정리 또는 한계 정리(no-go theorem)
네 개를 증명하지만, 상위 난제는 하나도 해결하지 않는다.

| 연구 트랙 | 이번에 확정한 결과 | 상위 난제 상태 |
|---|---|---|
| 리만 가설 | 지수 꼬리를 갖는 측도까지 dyadic 단사성과 균일 절단 오차를 확장 | 미해결 |
| 콜라츠 추측 | 6과 서로소인 모듈러스로 만든 모든 고정 주기 체를 통과하는 원시 거짓 양성 구성 | 미해결 |
| 강한 골드바흐 추측 | 유한 wheel의 균일한 양의 국소 밀도 하한 | 미해결 |
| 쌍둥이 소수 추측 | 모든 고정 wheel에 무한히 많은 합성수 쌍 반례 모형 구성 | 미해결 |

골드바흐의 최소 국소 밀도와 쌍둥이 소수의 wheel 생존 밀도는 동일한
유한 오일러 곱(Euler product)이다. 이것이 이번 티켓의 핵심 연결이다.
다만 이는 국소적 항등식일 뿐, 두 추측 사이의 증명 환원은 아니다.

## 1. 리만 가설

### 이번에 증명한 정확한 명제

`a>0`이고 `[a,infinity)`에 지지된 유한 부호 보렐 측도 `sigma`가 어떤
`eta>0`에 대해 다음 지수 총변동 모멘트(exponential total-variation
moment)를 가진다고 하자.

```text
integral exp(eta t) d|sigma|(t) < infinity
```

다음을 정의한다.

```text
L_sigma(s) = integral exp(-s t) d sigma(t),
W_j = L_sigma(2^(-j)) - L_sigma(2^(1-j)).
```

모든 정수 `j`에서 `W_j=0`이면 `sigma=0`이다. 또한 `sigma`를 높이 `T`
이하로 절단한 측도를 `sigma_T`라 하면 모든 dyadic band에서

```text
|W_j(sigma) - W_j(sigma_T)|
  <= exp(-eta T) integral exp(eta t) d|sigma|(t)
```

가 `j`와 무관하게 성립한다.

### 수학적 논증

지수 총변동 모멘트 때문에 `L_sigma`는 반평면 `Re(s)>-eta`에서 정칙이다.
band 방정식은 이웃한 dyadic 표본이 모두 같음을 뜻한다. `j`가 음의
무한대로 갈 때 표본점은 양의 무한대로 가고, 지지가 `a>0` 위에 있으므로
Laplace 변환은 0으로 수렴한다. 따라서 모든 dyadic 표본이 0이다.

이 표본들은 `s=0`에 축적된다. 지수 모멘트 덕분에 0은 정칙 영역 내부에
있으므로 항등정리(identity theorem)를 적용할 수 있고, `L_sigma` 전체가
0이다. Laplace 변환의 유일성으로 `sigma=0`을 얻는다.

꼬리 절단의 경우 가중 총변동에 Markov 부등식을 적용하면

```text
|sigma|([T,infinity))
  <= exp(-eta T) integral exp(eta t) d|sigma|(t)
```

를 얻는다. band kernel의 절댓값이 1 이하이므로 균일 오차 경계가 따른다.

### 재현 계산

다음 무한 원자 측도 모형을 사용했다.

```text
t_n = n,
w_n = (-1)^n 4^(-n),
eta = log(2).
```

가중 노름은 정확히 1이다. 6개의 절단 높이와 19개의 dyadic scale에서
닫힌형식 기하급수 꼬리를 계산했고, 모든 band 꼬리가 정확한 총변동
꼬리 및 지수 경계 아래에 있음을 확인했다.

### 한계와 다음 단계

이 정리는 추상적인 해석적 꼬리 문제만 닫는다. 리만 가설과 동치인
제타 영점 결함 측도가 이 지수 모멘트를 가진다는 사실도, 해당 band를
소수 쪽 자료로 엄밀히 계산할 수 있다는 사실도 증명하지 않았다.

- 폐기: 완전한 dyadic profile 단사성에 콤팩트 지지가 반드시 필요하다는
  주장.
- 유지: 리만 가설과 동치인 가중 결함 측도와 소수 쪽 band 표현 구성.
- 다음 단일 보조정리:
  `RHEquivalentExponentiallyWeightedDefectWithPrimeSideDyadicBands`.

## 2. 콜라츠 추측

### 이번에 증명한 정확한 명제

6과 서로소인 임의의 `M>1`에 대해

```text
r = ord_M(2),
h = ord_M(4 * 3^(-1)),
a = (2+r, 2, ..., 2), 길이 h
```

로 둔다. 가속 콜라츠 valuation word에 대해

```text
S = sum a_i,
D = 2^S - 3^h,
B = sum_i 3^(h-i) 2^(a_1+...+a_(i-1))
```

를 정의하면 `a`는 비자명 원시 word이고, `M`은 `D`와 `B`를 모두
나누지만 `0<B<D`이다. 따라서 실제 주기 조건 `D|B`는 실패한다. 유한한
6과 서로소인 여러 모듈러스를 동시에 사용할 때는 그 최소공배수를
`M`으로 선택하면 동일한 거짓 양성을 얻는다.

### 수학적 논증

모든 지수는 `r`을 법으로 2와 합동이다. 따라서

```text
2^S = 2^(2h+r) = 4^h (mod M).
```

`h`의 정의로 `4^h=3^h (mod M)`이므로 `M|D`이다. `B`의 모든 prefix
거듭제곱도 all-two word의 prefix와 합동이므로 기하합에서 `M|B`를 얻는다.

정확한 정수 합을 유지하면

```text
D-B = 4(2^r-1)3^(h-1) > 0
```

이다. 첫 항만 커졌기 때문에 더 짧은 block의 반복일 수도 없다. 따라서
고정 모듈러 검사를 통과하지만 주기가 아닌 비자명 원시 word가 된다.

### 재현 계산

5부터 199까지 6과 서로소인 66개 모듈러스와 3개의 결합 최소공배수
가족을 검사했다. 모든 구성에서 `M|D`, `M|B`, 닫힌형식 차이 공식,
`0<B<D`가 확인됐고 실제 `D|B`를 만족한 구성은 없었다.

### 확정한 no-go와 다음 단계

6과 서로소인 모듈러스로 만든 고정 유한 합동 검사만으로 모든 비자명
콜라츠 주기를 배제할 수는 없다. 이 정리는 code에 따라 커지는
모듈러스, 실수 크기 추정,
비주기 궤도의 하강 논증까지 배제하지는 않는다.

- 폐기: 고정된 유한 합동 검사 목록을 완전한 콜라츠 주기 증명으로 사용.
- 유지: code 크기에 따라 커지는 큰 소수 방해 또는 모든 비주기 궤도의
  첫 하강 정리.
- 다음 단일 보조정리:
  `CodeAdaptiveLargePrimeObstructionOrUniversalAperiodicDescent`.

## 3. 강한 골드바흐 추측

### 이번에 증명한 정확한 명제

`W`를 홀수 소수들의 squarefree 곱이라 하자. `a`와 `N-a`가 모두
`W`와 서로소인 잉여류 `a modulo W`의 개수를 `A_W(N)`이라 하면

```text
A_W(N)
 = product_(p|W,p|N) (p-1)
   product_(p|W,p not|N) (p-2).
```

독립 서로소 밀도 `(phi(W)/W)^2`로 정규화하면

```text
(A_W(N)/W) / (phi(W)/W)^2 >= C_W,
C_W = product_(p|W) p(p-2)/(p-1)^2.
```

등호는 `gcd(N,W)=1`일 때 정확히 성립한다. 모든 유한 `C_W`는 양의
무한 곱 `C_*`보다 크거나 같다.

### 수학적 논증

각 `p|W`에서 금지되는 잉여류는 `0`과 `N`이다. `p|N`이면 두 금지류가
같아서 `p-1`개가 남고, 그렇지 않으면 서로 달라 `p-2`개가 남는다. CRT가
이 국소 개수를 곱한다.

정규화한 국소 인자는 각각

```text
p/(p-1),                  p|N,
p(p-2)/(p-1)^2,           p not|N
```

이고 첫 번째가 더 크다. 또한 두 번째 인자의 1로부터의 차이는
`1/(p-1)^2`이며 그 합이 수렴하므로 무한 곱은 양수다.

### 재현 계산

`W=3*5*7*11=1155`에서 모든 목표 잉여류와 모든 후보 잉여류를 직접
열거했다. 최소 정규화 비율은 정확히 `693/1024`였으며, `W`와 서로소인
정확히 `phi(W)`개의 목표류에서 등호가 성립했다. 소수 43까지의 prefix
곱도 정확한 유리수로 생성했다.

### 한계와 다음 단계

국소 합동 장애가 없고 정규화된 양의 margin이 있다는 사실은 실제 소수
두 개의 표현을 보장하지 않는다. 소수 가중 전역 오차 또는 minor arc
오차를 main term보다 작게 만드는 작업이 남아 있다.

- 폐기: 짝수 골드바흐 목표를 막는 유한 국소 합동 장애 탐색.
- 유지: 소수 가중 전역 remainder를 균일 국소 main term 아래로 제한.
- 다음 단일 보조정리:
  `PrimeWeightedGoldbachRemainderStrictlyBelowUniformLocalMargin`.

## 4. 쌍둥이 소수 추측

### 이번에 증명한 정확한 명제

고정된 squarefree 홀수 wheel `W`와, 모든 `p|W`에 대해 `0`, `-2`를
피하는 생존 잉여류 `a`를 선택하자. `n=a (mod W)`이면서 `n`과 `n+2`가
모두 합성수인 `n`이 무한히 많다.

`W`를 나누지 않는 서로 다른 소수 `r,s`를 선택해

```text
n = a  (mod W),
n = 0  (mod r),
n = -2 (mod s)
```

를 CRT로 동시에 푼다. 얻은 산술진행의 충분히 큰 항에서 `n`은 `r`의
진배수이고 `n+2`는 `s`의 진배수다.

wheel 생존 밀도를 독립 서로소 밀도의 제곱으로 정규화하면

```text
product_(p|W) p(p-2)/(p-1)^2 = C_W
```

이며, 이는 바로 골드바흐 트랙의 최소 국소 인자와 같다.

### 재현 계산

소수 43까지 13개의 wheel prefix에 대해 명시적인 합성수 쌍 산술진행을
구성했다. 모든 witness는 wheel 안에서는 완전 생존 signature를 보이지만,
wheel 밖에서 지정한 소수들이 두 수를 각각 나눈다.

### 확정한 no-go와 다음 단계

TICKET-222에서 증명한 고정 wheel의 편향 parity 신호는 실제로 존재한다.
그러나 같은 signature를 합성수 쌍도 재현하므로 그 신호만으로 쌍둥이
소수를 인증할 수 없다.

- 폐기: 고정된 유한 wheel signature를 쌍둥이 소수 인증서로 사용.
- 유지: 탐색 scale과 함께 증가하는 wheel 또는 Type-I/II 정보와 균일한
  꼬리 오차 경계.
- 다음 단일 보조정리:
  `ScaleGrowingWheelSignalWithUniformTypeIIRemainderDominance`.

## 두 소수 문제의 새로운 연결

유한 오일러 곱 `C_W`는 정확히 두 의미를 가진다.

1. 골드바흐 convolution의 최악 정규화 국소 밀도
2. 쌍둥이 소수 wheel 생존쌍의 정규화 밀도

두 문제는 동일한 국소 산술 구조를 공유한다. 동시에 동일한 한계도
드러난다. 국소 admissibility(허용 가능성)는 소수 가중 전역 correlation을
제어하지 못한다. 따라서 두 트랙의 다음 핵심은 공통적으로 전역 remainder
제어지만, 이 항등식만으로 어느 추측도 다른 추측에서 따라오지 않는다.

## 문헌 경계

- Connes와 Consani의 semi-local 연산자 틀은 결합된 RH 관측량의 동기를
  제공한다. 이번 Laplace 정리는 초등적 부분정리이며 RH 판정법이 아니다:
  <https://arxiv.org/abs/1910.14368>.
- Tao의 논문은 2026년 v7까지 갱신된 almost-all(거의 모든 수) 콜라츠
  하강 결과를 제공하지만 모든 궤도의 하강을 뜻하지 않는다:
  <https://arxiv.org/abs/1909.03562>.
- 공개된 골드바흐 `4*10^18` 검증은 이번 유한 재현보다 훨씬 강하다:
  <https://doi.org/10.1090/S0025-5718-2013-02787-1>.
- Ford와 Maynard는 소수 생성 하한에 실질적인 Type-II 정보가 필요함을
  설명한다: <https://arxiv.org/abs/2407.14368>.

이번 티켓의 초등 항등식과 CRT 구성에 대해 문헌 최초성은 주장하지 않는다.

## 재현 방법

```powershell
python scripts/ticket223_exponential_tail_local_duality_no_go.py
python -m unittest tests.test_ticket223_exponential_tail_local_duality_no_go -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

주 기계 판독 산출물:

`data/open-problem/ticket223-exponential-tail-local-duality-no-go.json`
