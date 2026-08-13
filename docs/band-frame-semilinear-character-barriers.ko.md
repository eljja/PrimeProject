# TICKET-229: 대역 프레임·준선형 포괄·지표 방해

English edition: [band-frame-semilinear-character-barriers.md](band-frame-semilinear-character-barriers.md)

## 초록과 주장 경계

TICKET-229는 TICKET-228이 남긴 네 후속 보조정리를 직접 시험한다. 정확한
부분정리 또는 no-go 정리 네 개를 증명하고 재현 가능한 유한 검산을
기록했으며, 문제마다 다음 보조정리 하나를 선택했다. 리만 가설, 콜라츠
추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 증명하거나 반증한 것은
없다. 기계 판독 해결 수는 계속 `0/4`이다.

| 문제 | 이번에 확정한 결과 | 폐기·축소한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 가설 | 모든 유한 대역에서 이중 배율 에너지의 명시적인 양의 하한 | 지수적으로 작아지는 초등 하한을 다항식으로만 감소하는 절단 오차와 결합하는 경로 | `SubexponentialDualDilationLossMatchedToExplicitWeilCoreTail` (명시적 Weil 핵 꼬리와 맞는 준지수 이하 이중 배율 손실) |
| 콜라츠 추측 | 고정 접미사를 갖는 동일 기울기 언어는 `(h,S)` 아핀 직선 하나에 놓이고, 유한 합집합은 모든 원시 양의 분모 word를 종국적으로 덮지 못한다 | 유한 개 동일 기울기 언어로 충분히 긴 모든 순환 후보 word를 덮는 경로 | `OrderSensitiveNondivisibilityForAllPositiveDenominatorPrimitiveWords` (모든 양의 분모 원시 word에 대한 순서 민감 비나눗셈) |
| 강한 골드바흐 추측 | 목표 잉여류 한 주기를 완전히 평균하면 모든 비상수 국소 지표가 정확히 사라진다 | 목표 평균 상쇄를 각 고정 짝수 목표의 점별 상쇄로 승격하는 경로 | `PrimeWeightedPointwiseCharacterCancellationForEachGoldbachFactorCell` (각 골드바흐 인수 cell의 소수 가중 점별 지표 상쇄) |
| 쌍둥이 소수 추측 | shift-two 대칭은 홀 지표를 제거하지만 mod `5` 이차 지표는 정규화 크기 `1`로 그대로 남는다 | 가중치 없는 국소 인수를 더 텐서하면 모든 지표가 균일 수축한다는 경로 | `PrimeWeightedCancellationOfModuloFiveQuadraticShiftTwoMode` (mod `5` 이차 shift-two mode의 소수 가중 상쇄) |

공통 결론은 서로 다른 논리 단계를 분리해야 한다는 것이다. 유한 대역의
양성은 호환되는 꼬리 오차 없이는 유용한 점근 역변환이 아니고, 큰 정규
콜라츠 언어는 종국적 전면 포괄이 아니다. 평균 지표 상쇄는 점별 상쇄가
아니며, 이미 정규화 크기가 `1`인 국소 mode는 텐서 곱만으로 사라지지
않는다.

## 1. 리만 가설

### 명제 RH-229

```text
F(tau)=|1-2^(-i tau)|^2+|1-3^(-i tau)|^2
```

로 정의하자. `T >= pi/log(3)`이고
`pi/log(3) <= |tau| <= T`이면

```text
F(tau) >= 16 exp(-T log(2)log(3)/pi-log(3))
          / (log(2)^2+log(3)^2).                         (RH-229.1)
```

따라서 모든 유한 대역에는 완전히 명시적인 양의 프레임 하한이 있다.
하지만 이 인증값의 역수는 `T`에 대해 지수적으로 증가한다. 그러므로 이
특정 초등 하한은 `C T^(-k)` 정도로만 감소한다고 알려진 오차를 흡수할 수
없다.

### 증명

짝대칭이므로 `tau>0`만 보면 된다. 다음과 같이 두고 `n,m`을 각각 가장
가까운 정수로 잡는다.

```text
x=tau log(2)/(2 pi),  y=tau log(3)/(2 pi).
```

`delta_2=|x-n|`, `delta_3=|y-m|`라 하면 둘 다 `1/2` 이하이다.
`|sin(pi u)| >= 2|u|`를 적용하면

```text
F(tau) >= 16(delta_2^2+delta_3^2).                       (RH-229.2)
```

또한 `x log(3)=y log(2)`이므로

```text
Lambda=n log(3)-m log(2)
      =(n-x)log(3)-(m-y)log(2).
```

코시-슈바르츠 부등식으로 `|Lambda|`를 `(RH-229.2)`의 거리와 연결한다.
대역의 아래끝 때문에 `m>=1`이고 `n>=0`이다. 소인수분해의 유일성으로
`3^n != 2^m`이다. 서로 다른 양의 정수 `A,B`에는

```text
|log(A/B)| >= 1/max(A,B)
```

가 성립한다. 가장 가까운 정수의 크기에서

```text
max(3^n,2^m)
 <= exp(T log(2)log(3)/(2 pi)+log(3)/2)
```

를 얻는다. 이 부등식들을 결합하고 제곱하면 `(RH-229.1)`이 나온다.
마지막으로 모든 고정 `k`에 대해 `exp(-cT)=o(T^(-k))`이므로 양의 다항
오차는 결국 이 하한보다 커진다.

### 계산과 한계

감사 코드는 대표 주파수 7개에서 위상 부등식을 확인하고 `T=5000`까지
대역 8개의 하한을 계산한다. 밑 `10` 로그 하한은 `T=10`에서 약
`-0.553`, `T=5000`에서 약 `-525.85`이다. 모형 오차 `T^-12`는
`T=500`부터 인증 하한보다 커진다.

유한 표가 아니라 위 해석적 부등식이 RH-229를 증명한다. 그러나 실제 Weil
이차형식 핵, 그 연산자 하한, 호환되는 명시적 절단 꼬리는 만들지 못했다.
따라서 리만 가설로 가는 함의는 없다. 다음 목표는 준지수 이하의 조건 손실을
얻거나 같은 지수 손실보다 더 작은 실제 Weil 핵 꼬리를 증명하는 것이다.

## 2. 콜라츠 추측

### 명제 CO-229

양의 valuation word의 길이를 `h`, 지수 합을 `S`라 하자. 길이 `k`, 합
`s`인 블록의 정규화 아핀 기울기는 `3^k/2^s`이다. 하나의 공통 기울기를
갖는 블록들을 이어 붙이고 고정 접미사 하나를 붙인 모든 언어는 정수
`(h,S)` 평면의 아핀 직선 하나에 놓인다. 이런 언어의 유한 합집합은 모든
원시 양의 분모 valuation word를 종국적으로 덮지 못한다.

평행선의 유한한 절편을 피하도록 정수 `c>=1`을 고르면

```text
w_(h,c)=(c+2,2,...,2),  S=2h+c                            (CO-229.1)
```

는 원시적이고 `D=2^S-3^h>0`이다. 평행하지 않은 각 언어는 이 족과 많아야
한 번 만나므로 충분히 큰 모든 `h`에서 덮이지 않은 word가 생긴다.

### 증명

두 블록의 정규화 기울기가 같으면

```text
3^k1/2^s1 = 3^k2/2^s2
```

이다. 소인수분해의 유일성으로 `k1=k2`, `s1=s2`이다. 이런 블록 `r`개와
고정 접미사 `(h0,s0)`를 붙이면

```text
(h,S)=(rk+h0, rs+s0)
```

가 되어 한 아핀 일차식을 만족한다. 유한 개 언어는 유한 개 직선을 준다.
`S=2h+c`가 그중 어느 평행선도 아니게 `c`를 고르면, 나머지 각 직선은 이
직선과 많아야 한 점에서 만난다.

`h>=2`에서 `(CO-229.1)`은 예외 항을 정확히 하나만 가지므로 비자명한
반복 word가 아니며 원시적이다. 또한

```text
2^S=2^c 4^h > 3^h
```

이므로 `D>0`이다. 유한한 교점을 제거해도 높이가 무한히 커지는 미포괄
족이 남는다.

### 계산과 한계

감사 코드는 기존 연구와 독립 예시에서 가져온 동일 기울기 언어 세 개를
검사한다. `c=1`인 witness 직선은 표본 언어 하나와 `h=3`에서만 만나며,
감사한 `h>=4`에서는 세 언어 모두의 밖에 있다. 원시성과 `D>0`은 정확한
정수 연산으로 확인한다.

CO-229는 유한 준선형 포괄에 대한 무한 no-go 정리이지 단순한 유한 검색이
아니다. 그러나 밖에 남은 양의 분모 word가 정확한 순환 나눗셈 `D|B`를
만족한다는 뜻은 아니고, 자연수 궤도로 실현된다는 뜻도 아니며, 비주기
궤도의 하강도 말하지 않는다. 다음 정리는 순서에 민감한 절편 산술을 사용해
남은 모든 원시 word에서 `D`가 `B`를 나누지 않음을 증명하거나 실제
나눗셈 반례를 찾아야 한다.

## 3. 강한 골드바흐 추측

### 명제 GB-229

홀수 소수 `l`, `G=(Z/lZ)^*`, 전부 `1`인 연산자 `J`에 대해

```text
M_a(u,v)=1_(uv != a mod l)
```

로 두자. `a!=0`이면 `M_a=J-P_a`이고 `P_a`는 `v=a/u`인 순열이다.
그러면

```text
sum_(a mod l) M_a = (l-1)J.                               (GB-229.1)
```

따라서 목표 잉여류의 완전한 한 주기는 합이 `0`인 지표 공간을 정확히
소거한다. 연속 목표 `H`개의 평균에서 비상수 연산자 노름은
`r/H<l/H`, `r=H mod l` 이하이다. 반면 고정된 각 비영 목표의 비상수
노름은 정확히 `1`이다.

### 증명

각 단위 쌍 `(u,v)`에는 `l`개 목표 중 정확히 하나의 비영 잉여류
`a=uv`만 금지된다. 따라서 마스크 합의 모든 성분은 `l-1`이고
`(GB-229.1)`이 성립한다. 합이 `0`인 공간에서 `J`는 영 연산자이므로 완전
주기 기여는 사라진다.

길이 `H`인 연속 구간을 완전 주기들과 길이 `r`인 나머지로 나눈다.
영합 공간에서 비영 `a`에는 `M_a=-P_a`, `a=0`에는 `M_0=J=0`이다.
각 비영 나머지 항의 노름이 `1`이므로 삼각부등식으로 `r/H<l/H`를 얻는다.
하지만 고정 비영 `a` 하나에서는 `-P_a`가 등거리 변환이므로 점별 노름
`1` 방해가 정확히 남는다.

### 계산과 한계

홀수 소수 `43`까지 정확한 유한군 행렬로 완전 주기 항등식을 확인했다.
`H`가 `10,25,100,1000`인 연속 창에서 정확한 나머지와 `r/H` 상한도
검산했다.

증명은 모든 홀수 소수 `l`에 대해 정확하며 유한 행렬은 회귀 검산이다.
강한 골드바흐는 각 짝수 목표에 대한 점별 명제지만 GB-229의 상쇄는 목표
잉여류를 평균할 때만 생긴다. 고정 목표의 소수 가중 minor arc 또는 인수
cell 추정은 없다. 다음 보조정리는 바로 그 점별 지표 상쇄여야 한다.

## 4. 쌍둥이 소수 추측

### 명제 TP-229

홀수 소수 `l>3`과 `G=(Z/lZ)^*`에 대해 동시 shift-two 생존 연산자를

```text
S=J-P_2-P_(-2)
```

로 두자. 모든 비주 지표 `chi`에 대해

```text
S chi = -chi(2)(1+chi(-1)) chi^(-1).                      (TP-229.1)
```

따라서 홀 지표의 특이값은 `0`, 짝 비주 지표의 특이값은 `2`, 상수
특이값은 `l-3`이다. `l=5`에서 이차 지표는 짝 지표이고 정규화 비율은
`2/(5-3)=1`이다. 정규화한 다른 국소 인수를 텐서해도 mod `5` 성분에만
지지된 전역 지표를 수축시킬 수 없다.

### 증명

`l>3`에서는 금지된 곱 `2`, `-2`가 서로 달라 위 연산자가 나온다.
`P_a f(u)=f(a/u)`이면

```text
P_a chi = chi(a) chi^(-1).
```

전부 `1`인 연산자는 모든 비주 지표를 죽인다. 또한
`chi(-2)=chi(-1)chi(2)`이므로 `(TP-229.1)`이 성립한다. 지표의 홀짝성에
따라 `1+chi(-1)`은 `0` 또는 `2`이고, 상수 행합은 `l-3`이다. mod
`5`의 유일한 이차 비주 지표는 짝 지표이므로 그 특이값과 상수 특이값이
같다. 다른 국소 소수에서 주 지표를 택한 텐서 지표는 이 정규화 비율
`1`을 보존한다.

### 계산과 한계

홀수 소수 `43`까지 정확한 지표 작용을 감사했다. 검사한 국소 인수 중
mod `5`만 최악의 정규화 비상수 비율이 `1`이다. 정방인수가 없는 텐서
예시 다섯 개도 다른 국소 인수를 추가해 mod `5` 전용 mode를 없앨 수
없음을 확인한다.

TP-229는 정확한 홀짝 투영과 정확한 방해 mode를 찾았다. 그러나 소수
가중 shift-two 합을 추정하지 않고, 체의 parity problem을 넘지 않으며,
간격 `2`인 소수가 무한히 많음을 증명하지 않는다. 다음 보조정리는 실제
소수 가중 인수 cell에서 이 명시적 mod `5` 이차 mode를 상쇄하는 것이다.

## 문헌과 우선권 경계

- Connes와 Consani의 [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368)은 연산자론적 Weil 양성 맥락을 제공한다. RH-229는 초등적인 두 주파수 하한과 꼬리 불일치 결과일 뿐이다.
- Lagarias의 [The 3x+1 problem: an overview](https://arxiv.org/abs/2111.02635)와 Tao의 [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)는 word 산술, 거의 모든 궤도, 모든 궤도 수렴 사이의 차이를 보여 준다.
- Helfgott의 [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438)은 원 방법의 맥락을 제공하지만 강한 이항 골드바흐를 함의하지 않는다.
- Ford와 Maynard의 [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368), Polymath의 [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897)는 현대 체 이론의 맥락을 제공한다. 유계 소수 간격은 간격이 정확히 `2`인 경우가 무한함을 증명하지 않는다.

최근접 정수 로그 선형형 하한, 준선형 격자 논증, 유한군 지표 대각화는
고전적 도구이다. PrimeProject는 독립적인 전면 문헌 조사와 동료 평가
없이 이 재료나 TICKET-229의 우선권을 주장하지 않는다. 여기서 보존할
기여는 명시적 정리/no-go 원장, 증명 의존성, 기계 재현 감사, 그리고 더
좁아진 후속 명제이다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket229_band_frame_semilinear_character_barriers.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket229_band_frame_semilinear_character_barriers -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

기계 판독 산출물:

- `data/open-problem/ticket229-band-frame-semilinear-character-barriers.json`
- `data/open-problem/riemann/rh-ticket-229-band-frame-bound.json`
- `data/open-problem/collatz/co-ticket-229-semilinear-coverage-no-go.json`
- `data/open-problem/goldbach/gb-ticket-229-target-period-cancellation.json`
- `data/open-problem/twin-prime/tp-ticket-229-character-parity-obstruction.json`
