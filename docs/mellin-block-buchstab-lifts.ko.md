# TICKET-227: Mellin·반복 블록·Buchstab 인수 분해

English edition: [mellin-block-buchstab-lifts.md](mellin-block-buchstab-lifts.md)

## 초록과 주장 경계

TICKET-227은 TICKET-226이 남긴 네 미해결 경로를 이어간다. 정확한 구조
보조정리 네 개를 증명했지만, 리만 가설·콜라츠 추측·강한 골드바흐
추측·쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않았다.

| 문제 | 새로 확립한 정확한 결과 | 폐기·교정한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 가설 | dilation 비율 하나에는 무한히 많은 Mellin 사각지대가 있지만, 비율 `2`와 `3`에는 `Re(s)=1` 위의 공통 비상수 사각지대가 없다 | 하나의 균형 dilation 족이 모든 Mellin mode를 분리한다는 가정 | `UniformDualDilationMellinFrameBoundOnExplicitDenseWeilCore` |
| 콜라츠 추측 | 분수선형 끝점 판정으로 모든 `(1,1,3)^r,(4,2,1)`이 원시 비순환임을 증명 | 유한한 `r` 검사로 무한족을 확정 | `UniversalPrimePowerWitnessForPrimitiveValuationWordNondivisibility` |
| 강한 골드바흐 | 세제곱근 거친 반소수 오차를 정확한 `N-qr` 소인수 cell로 분해하고 `q|N` 예외를 분리 | 한 변수 주변분포로 모든 pointwise cell을 추정 | `UniformMovingResiduePrimeEstimateForCubeRootBuchstabCellsAtEveryEvenTarget` |
| 쌍둥이 소수 | shift-two 오차를 `qr-2`, `qr+2`, `pq+2=rs`로 정확히 분해하고 모든 `SS` 항의 두 소인수 집합이 서로소임을 증명 | 소인수 비공유만으로 상쇄가 생긴다는 가정 | `UniformShiftTwoBilinearPrimeEstimateForQrPlusMinus2AcrossAllCubeRootCells` |

공통 진전은 좌표계를 바꾼 것이다. 거친 관측량을 Mellin 주파수, Collatz
affine 합성, 소인수 cell이라는 정확한 장애 좌표로 올렸다.

## 1. 리만 가설

### 명제 RH-227

`q>1`, `a>0`에 대해 다음 균형 대조량을 정의한다.

```text
B_q[E](a) = a integral_0^infinity
              E(x)(exp(-ax)-q exp(-qax)) dx.
```

Mellin mode `E_s(x)=x^(s-1)`, `Re(s)>0`에 대해서는

```text
B_q[E_s](a) = a^(1-s) Gamma(s)(1-q^(1-s)).                 (RH-227.1)
```

`s=1+i tau`에서 `q=2` 관측족은

```text
tau = 2 pi k/log(2),  k in Z                               (RH-227.2)
```

인 모든 주파수를 보지 못한다. 그러나 `q=2`와 `q=3`을 함께 사용하면
공통 사각지대는 상수 mode `tau=0`뿐이다.

### 증명

Mellin-Laplace 적분

```text
integral x^(s-1) exp(-cax) dx = Gamma(s)(ca)^(-s)
```

에 `c=1,q`를 대입하면 `(RH-227.1)`을 얻는다. `Re(s)=1`에서 multiplier가
0이라는 것은 `tau log(q)`가 `2 pi`의 정수배라는 뜻이다. `q=2,3`에
공통인 0이 아닌 주파수가 있다면 양의 정수 `k,l`에 대해
`2^l=3^k`가 되어야 하므로 소인수분해의 유일성에 모순이다.

### 계산과 한계

`q=2`의 첫 다섯 alias 주파수에서 닫힌형 multiplier를 계산했다. 모두
`q=2`에서는 0이고 `q=3`에서는 0이 아니다. 첫 두 주파수는 외부 의존성이
없는 로그 좌표 합성 Simpson 적분으로 절대 오차 `1e-15` 이내에서 독립
검산했다. 더 높은 주파수에서는 `Gamma(1+i tau)`가 지수적으로 작아지므로,
부동소수점 잡음을 증거로 취급하지 않고 정확한 닫힌형을 사용한다.

이 결과는 개별 Mellin mode의 분리성이다. 임의 중첩에 대한 균일한 frame
하한, 조밀한 Weil 시험함수 핵에서의 명시공식 제어, Weil 양성을 주지
않는다. 상수 mode도 여전히 보이지 않는다.

## 2. 콜라츠 추측

### 명제 CO-227

가속 Collatz word `U=(1,1,3)`의 affine 자료는 `(A,C,B)=(27,32,19)`다.
고정 suffix `V`의 자료를 `(A_V,C_V,B_V)`라 하고

```text
w_r = U^r V,  r>=1
```

라 두면 cycle 분모와 intercept는

```text
D_r = C_V 32^r-A_V 27^r,
B_r = ((5B_V+19A_V)32^r-19A_V 27^r)/5.                    (CO-227.1)
```

이다. `D_r>0`이고 `r=1` 및 `r->infinity`에서의 `B_r/D_r`가 같은 열린
단위 구간 `(m,m+1)` 안에 있으면, 모든 `r>=1`에 대해 `D_r`는 `B_r`를
나누지 않는다.

`V=(4,2,1)`에서는

```text
B_1/D_1 = 4385/3367,
lim_(r->infinity) B_r/D_r = 559/320
```

이며 둘 다 `(1,2)` 안에 있다. 따라서 모든 `(1,1,3)^r,(4,2,1)`은
원시 비순환 word다.

### 증명

Affine 합성과 `U^r`의 등비합으로 `(CO-227.1)`을 얻는다. 분자와 분모를
`32^r`으로 나누고 `t=(27/32)^r`라 두면 `B_r/D_r`는 `t`의 분수선형
함수다. `0<=t<=27/32`에서 극이 없으므로 단조이거나 상수이며 두 끝점
사이에 머문다. 선택한 suffix에서는

```text
1 < B_r/D_r < 2
```

이므로 정수가 될 수 없고 `D_r`는 `B_r`를 나누지 않는다. 지수 `4`가
정확히 한 번만 나오므로 더 짧은 word의 반복일 수도 없다.

### 계산과 한계

길이 `4` 이하, 지수 `1,...,6`인 suffix를 유리수로 완전 탐색해 끝점
인증 `1,425`개를 찾았다. 이 탐색은 후보 발견용이며 선택한 무한족의
증명은 위의 기호 논증이다. `r=1,...,40`에서는 직접 affine 합성도
닫힌형과 일치했다.

끝점 사이에 정수가 끼는 suffix는 이 판정으로 다룰 수 없다. 모든 원시
valuation word의 `D|B`를 배제하지 않았고, 비주기 자연수 궤도의 하강도
증명하지 않았다.

## 3. 강한 골드바흐 추측

### 명제 GB-227

`z=ceil(X^(1/3))`라 하자. `z` 이하 소인수가 없는 합성수 `m<=X`는
유일하게

```text
m=qr,  z<q<=r,  q,r은 소수                              (GB-227.1)
```

로 표현된다. 따라서 짝수 `N`의 `PS` 채널은 정확히

```text
sum_(z<q<=sqrt(N)) sum_(q<=r, qr<=N-2)
  1_prime(N-qr)                                             (GB-227.2)
```

이고 `SP`도 대칭인 식을 가진다. `SS`는 두 소인수 cell의 합성곱이다.
`(GB-227.2)`에서 `q|N`이면 소수 `N-qr`도 `q`로 나누어지므로
`N-qr=q`, 즉 `r=N/q-1`인 후보 하나만 남는다.

### 증명

`z`보다 큰 인수 세 개의 곱은 `z^3>=X`다. 따라서 범위 안의 거친 합성수는
정확히 두 소인수를 가지며, 작은 인수를 먼저 쓰면 표현이 유일하다. 이를
대입하면 각 factor lift가 나온다. `q|N`일 때 `q|(N-qr)`이고 소수
`N-qr`가 `q`의 배수라면 그 소수는 `q` 자체여야 한다.

### 계산과 한계

`N=10^4,10^5,10^6`에서 작은 소인수 지수 범위 `[1/3,1/2]`를 네 cell로
나눴다. 모든 `PS`, `SP`, `SS` bin과 행렬의 합이 TICKET-226 정수 개수와
정확히 일치한다. 이 표는 향후 bilinear 추정이 실제로 제어해야 할 대상을
기계 판독 형태로 고정한다.

정확한 분해는 `PP>0` 하한이 아니다. 모든 짝수에서 움직이는 비영 잉여류
`N-qr`가 소수인 경우를 균일하게 추정하는 정리가 남아 있다. 한 변수 PNT와
주변 반소수 밀도만으로는 이 추정을 얻을 수 없다.

## 4. 쌍둥이 소수 추측

### 명제 TP-227

같은 cutoff에서 shift-two 오차 채널은 정확히

```text
PS: qr-2가 소수,
SP: qr+2가 소수,
SS: pq+2=rs
```

로 올라간다. 모든 인수는 `z`보다 크다. 각 `SS` 항에서

```text
{p,q} intersection {r,s} = empty.                           (TP-227.1)
```

### 증명

`(GB-227.1)`의 유일한 두 소인수 표현을 대입하면 세 식을 얻는다. `SS`의
양쪽에 공통 홀수 소인수가 있다면 그 수는 `n=pq`와 `n+2=rs`를 모두
나누므로 `2`도 나누어야 한다. 이는 불가능하다.

### 계산과 한계

`X=10^4,10^5,10^6`의 factor-cell 표가 TICKET-226의 모든 채널 정수 개수를
재현했고, 열거된 `SS` 항의 공통 소인수 충돌은 0이다. 그러나 서로소라는
사실만으로 상쇄, power saving, 또는 무한히 많은 `PP`를 얻을 수 없다.
다음 보조정리는 모든 세제곱근 cell에서 `qr-2`, `qr+2` 소수 합을 균일하게
추정해야 한다.

## 문헌 및 우선권 경계

- Connes와 Consani의 [Weil positivity and Trace formula, the archimedean place](https://arxiv.org/abs/2006.13771)는 Weil 양성의 배경이다. RH-227은 양성 정리가 아니다.
- Tao의 [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)는 거의 모든 궤도에 관한 정리이며 모든 궤도 하강 정리가 아니다.
- Helfgott의 [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438)는 원방법의 1차 문헌이지만 이항 강한 골드바흐를 증명하지 않는다.
- Ford와 Maynard의 [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368)는 소수 하한에서 충분한 Type-I·Type-II 정보가 왜 필요한지 설명한다.
- Polymath의 [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897)는 bounded-gap 1차 문헌이며 정확한 gap `2`를 증명하지 않는다.

Buchstab 분해, Mellin-Laplace 변환, Collatz affine word 합성은 고전적
도구다. PrimeProject는 이 재료 자체의 문헌 우선권을 주장하지 않는다.
이번 기여는 네 정확한 보조정리를 반증 가능한 증명 ledger, alias 표,
factor-cell 행렬로 통합했다는 데 있다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket227_mellin_block_buchstab_lifts.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket227_mellin_block_buchstab_lifts -v
```

기계 판독 결과:

- `data/open-problem/ticket227-mellin-block-buchstab-lifts.json`
- `data/open-problem/riemann/rh-ticket-227-dual-dilation-mellin.json`
- `data/open-problem/collatz/co-ticket-227-block-suffix-interval.json`
- `data/open-problem/goldbach/gb-ticket-227-buchstab-factor-lift.json`
- `data/open-problem/twin-prime/tp-ticket-227-shift-two-factor-lift.json`
