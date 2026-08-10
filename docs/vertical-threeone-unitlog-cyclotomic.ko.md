# TICKET-208: 수직 경계 하한, 세 개의 valuation-1, 단위 로그 증인, 순환 푸리에 상관

## 주장 상태

네 상위 추측은 모두 `open_not_proven`, 즉 미해결 상태다. TICKET-208은
정확한 부분정리 또는 no-go 정리 네 개를 증명하지만 리만 가설, 콜라츠
추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 증명하거나
반증하지 않는다.

표준 기계 판독 산출물은
[`ticket208-vertical-threeone-unitlog-cyclotomic.json`](../data/open-problem/ticket208-vertical-threeone-unitlog-cyclotomic.json)이다.

| 문제 | 새로 확립한 정확한 결과 | 해결 상태 | 폐기한 경로 | 남은 간극 | 다음 단일 보조정리 |
|---|---|---|---|---|---|
| 리만 | `Re(s)=2,-1` 두 수직변에서 완성 제타함수의 명시적 양의 하한 | 미해결 | 수직변도 미지의 경계로 취급하거나 수직변만으로 RH를 추론 | 무한히 커지는 수평변의 양의 하한 | `CertifiedCompletedXiTopEdgeClearanceOnCofinalAdmissibleHeights` |
| 콜라츠 | valuation-1이 정확히 세 개인 가속 주기 전체 배제 | 미해결 | 정확히 세 개의 1을 갖는 주기 영역 전체 | 1이 네 개 이상인 주기와 비주기 발산 | `UniformExclusionForPrimitiveValuationNecklacesWithExactlyFourOnes` |
| 골드바흐 | 모든 `c<1`에 대해 최소 증인이 `c log N`보다 큰 비유계 짝수 수열 | 미해결 | 고정된 1 미만 로그 증인 창 | 단위 로그 바깥 tail의 예외 개수 1 미만 상계 | `GoldbachTailExceptionalCountBelowOneBeyondAsymptoticallyUnitLogFloor` |
| 쌍둥이 소수 | 성장하는 Omega 순환 푸리에 projector의 정확 복원과 zero mode 완전 상쇄 | 미해결 | 양의 zero mode 또는 고정 차원 스펙트럼을 양의 하한으로 사용 | 부호 있는 비영 모드 나머지의 무한 규모 하한 | `CofinalDyadicOmegaPhaseRemainderStrictlyAboveMinusIntervalLength` |

이 정리들은 PrimeProject 내부에서 명제, 증명, 계산을 일치시킨 결과다.
학술적 우선권이나 신규성은 독립적인 전문가 및 문헌 검토를 거쳐야 한다.

## 1. 리만 가설

### 이번에 선언한 명제

완성 제타함수를

```text
xi(s) = (1/2)s(s-1) pi^(-s/2) Gamma(s/2) zeta(s)
```

라고 하자. 모든 `T>=0`, `|t|<=T`에 대해

```text
|xi(2+it)| >= B(T) > 0,

B(0) = pi/15,
B(T) = (pi/15) sqrt((pi T/2)/sinh(pi T/2))  (T>0)
```

가 성립한다. 함수방정식에 의해 `Re(s)=-1`에서도 같은 하한이 성립한다.
따라서 직사각형 `[-1,2] x [-T,T]`의 두 수직변은 명시적으로 영점을
갖지 않는다. TICKET-207에서 남긴 경계 문제는 수평변으로 축소된다.

### 증명

`sigma>1`에서는 Euler 곱이 절대수렴한다. 삼각부등식으로

```text
|zeta(s)|
 >= product_p (1+p^(-sigma))^(-1)
  = zeta(2 sigma)/zeta(sigma)
```

를 얻는다. `sigma=2`에서는

```text
|zeta(2+it)| >= zeta(4)/zeta(2) = pi^2/15.
```

또한

```text
|Gamma(1+iy)|^2 = pi y/sinh(pi y)
```

이고 `y/sinh(pi y)`는 `y>=0`에서 감소한다. 따라서 `|t|<=T`이면 감마
인자에도 `T`만으로 표현되는 양의 하한이 있다. 마지막으로
`|(2+it)(1+it)|>=2`를 곱하면 위의 `B(T)`가 나온다. `xi(s)=xi(1-s)`를
사용하면 왼쪽 수직변도 동시에 처리된다.

### 수직변만 사용하는 경로의 no-go

```text
F(s)=(s-1/2)^2-1/9
```

는 두 수직변에서 0이 아니지만 내부의 `1/6`, `5/6`에 영점이 있다. 이
함수는 제타함수가 아니므로 RH의 반례가 아니다. 수직변의 양의 하한과
대칭만으로 내부 영점 위치를 결정할 수 없다는 반례다.

### 남은 간극

`s=sigma+iT`, `-1<=sigma<=2`인 위쪽 수평변에서 `|xi(s)|`의 양의 하한을
무한히 커지는 높이들에 대해 증명해야 한다. 유한 높이 계산은 이 보조정리를
대체하지 못한다.

## 2. 콜라츠 추측

### 이번에 선언한 명제

가속 홀수 사상

```text
T(x)=(3x+1)/2^v2(3x+1)
```

의 양의 비자명 주기 중 valuation-1이 정확히 세 번 나타나고 나머지가
모두 2 이상인 주기는 존재하지 않는다. TICKET-206, 207과 결합하면 가상의
비자명 양의 주기에는 valuation-1이 최소 네 번 있어야 한다.

### 길이의 전역적 유한화

주기의 최소 홀수값을 `m>=3`이라 하고 그 위치부터 시작하도록 회전한다.
첫 valuation이 2 이상이면 `(3m+1)/4<m`이므로 첫 값은 반드시 1이다.
마지막 valuation이 1이면 `(3x+1)/2>x>=m`이므로 `m`으로 돌아올 수 없다.

주기 길이를 `h`, valuation 총합을 `A`, 궤도값을 `x_i`라 하면

```text
2^A = product_i (3+1/x_i)
```

가 정확히 성립한다. 모든 `x_i>=3`이므로

```text
2^A 3^h <= 10^h.
```

1이 정확히 세 개이고 나머지가 2 이상이면 `A>=2h-3`이다. `h=12`에서
이미 `2^(2h-3)3^h>10^h`이고, 길이가 하나 늘 때 두 변의 비율은 `6/5`배
증가한다. 그러므로 `h>=12`는 모두 불가능하다.

### 185개 단어의 정확한 유한 증명

`4<=h<=11`에서는 같은 곱 부등식이 `A`의 정수 상한을 준다. 최소점 회전,
나머지 두 1의 위치, 남은 valuation 예산의 모든 약한 합성을 열거하면
정확히 185개 단어가 남는다.

각 단어의 합성은 유리수 계수의 일차식

```text
T_word(x)=alpha x+beta
```

이므로 가능한 주기 시작점은 `x=beta/(1-alpha)` 하나뿐이다. 185개 중
양의 홀수 정수인 고정점은 0개다. 이는 시작값을 임의 한계까지 검색한
결과가 아니라, 해당 valuation 영역 전체를 먼저 유한화한 완전한 검사다.

### 남은 간극

valuation-1이 네 개 이상인 주기는 아직 남아 있다. 비주기적으로 무한히
커질 수 있는 궤도도 이 정리로 배제되지 않는다.

## 3. 강한 골드바흐 추측

### 이번에 선언한 명제

`W(N)`을 `N-p`도 소수가 되는 가장 작은 소수 `p`라 하고, 표현이 없으면
`W(N)=infinity`라고 하자. 모든 실수 `c<1`에 대해 비유계한 짝수 `N`들이
존재하여

```text
W(N) > c log N
```

을 만족한다. 확장된 값의 의미에서

```text
limsup_(N even) W(N)/log N >= 1
```

이다.

### 증명

`eta>0`을 고정하고 큰 `B`를 잡는다. 소수정리에 의해 구간
`(B,(2+eta)B)`에는 결국 `pi(B)-1`개 이상의 소수가 있다. 각 홀수 소수
`p<=B`에 서로 다른 `q_p`를 배정하고 CRT 조건

```text
N = 0 (mod 2),
N = p (mod q_p)
```

를 동시에 만족시킨다. `M=2 product q_p`라 하면 같은 잉여류에서
`M<N<=3M`인 짝수를 선택할 수 있다. 모든 `p<=B`에 대해 `N-p`는
`q_p`의 진합성 배수이고 `N-2`도 짝수 합성수다. 따라서 `W(N)>B`다.

소수정리는 동시에

```text
log M <= log 2+(pi(B)-1)log((2+eta)B) = (1+o(1))B
```

를 준다. 따라서 `log N<=(1+o(1))B`이고 모든 고정 `c<1`에 대해 충분히
큰 `B`에서 `c log N<B<W(N)`이다.

### 논리적 한계

`p<=B`인 증인만 막았다. 더 큰 소수로 표현될 가능성은 그대로 남는다.
골드바흐 반례도, 남은 tail 예외 개수의 1 미만 상계도 얻지 못했다.

## 4. 쌍둥이 소수 추측

### 이번에 선언한 명제

정수 `H`개를 포함하는 구간 `I`에 대해

```text
L=floor(log_2(max(I)+2)),
M=L+1,
omega=exp(2 pi i/M)
```

라고 하자. `Omega(n)<=L`이므로 순환군 문자 직교성은 다음 정확한 소수
projector를 준다.

```text
1_{Omega(n)=1}
 = (1/M) sum_(j=0)^(M-1) omega^(j(Omega(n)-1)).
```

`n`, `n+2`의 두 projector를 곱하면 구간 안 쌍둥이 소수 개수 `T_I`가
`M x M` 부호 있는 순환 푸리에 상관으로 정확히 복원된다.

### zero mode의 정확한 상쇄

`(0,0)`을 제외한 모든 주파수쌍의 원시 합을 `R_I`라고 하면 zero mode는
정확히 `H`이므로

```text
M^2 T_I = H+R_I,
R_I = M^2 T_I-H.
```

쌍둥이가 없는 구간에서는 `R_I=-H`다. 즉 양의 zero mode가 비영 모드에
의해 정확히 전부 상쇄된다. zero mode만으로 양의 하한을 만들 수 없다.

### 고정 차원 경로의 no-go

`M`을 고정하면 필터는 `Omega(n)=1 mod M`인 모든 수를 통과시킨다.
`Omega(2^(M+1))=M+1`이므로 명시적인 합성수가 소수와 같은 값을 갖는다.
정확한 projector가 되려면 `M`이 구간에서 가능한 최대 `Omega`보다 크게
성장해야 한다.

### 남은 간극

무한히 많은 이중 구간에서 `R_I>-H`를 증명해야 `T_I>0`을 얻는다. 현재는
성장하는 비영 Omega 위상 상관에 대한 독립적인 산술 하한이 없다. 따라서
이 항등식은 유한 인수분해 정보의 재표현이지 parity barrier 해결이 아니다.

## 최신 문헌과의 경계

아래 1차 자료는 현재 결과가 어디까지인지 구분하기 위한 비교 기준이다.
위의 정확한 산술 증명이 이 논문들의 결과를 가정하는 것은 아니다.

- Platt와 Trudgian의 구간연산 검증은 RH를 높이 `3*10^12`까지 확인한
  유한 결과다: <https://arxiv.org/abs/2004.09765>.
- Tao의 결과는 로그 밀도 의미의 거의 모든 콜라츠 궤도에 대한 정리이며
  모든 궤도 정리는 아니다: <https://doi.org/10.1017/fmp.2022.8>.
- Angeltveit의 2026년 알고리즘은 유한한 `2^N` 범위 검증을 개선한다:
  <https://arxiv.org/abs/2602.10466>.
- Oliveira e Silva, Herzog, Pardi는 이진 골드바흐를 `4*10^18`까지 검증했다:
  <https://doi.org/10.1090/S0025-5718-2013-02787-1>.
- Maynard의 유계 소수 간격 정리는 고정 간격 2를 선택하지 않는다:
  <https://doi.org/10.4007/annals.2015.181.1.7>.

## 재현 방법

```powershell
python scripts/ticket208_vertical_threeone_unitlog_cyclotomic.py
python -m unittest tests.test_ticket208_vertical_threeone_unitlog_cyclotomic -v
```

생성기는 통합 JSON 하나와 문제별 JSON 네 개를 기록한다. 네 상위 추측의
해결 카운터는 모두 0으로 유지된다.
