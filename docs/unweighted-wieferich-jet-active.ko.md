# TICKET-248: 비가중 모멘트, generalized-Wieferich 분리, 중심 first jet, active 오염

## 상태 선언

- `iteration_complete`: true
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- `new_partial_theorem_count`: 3
- `exact_no_go_count`: 1
- `stagnated_problem_count`: 0
- deep focus: 강한 골드바흐 추측
- parent: TICKET-247
- 프로그램 상태: `open_not_proven`

이번 회차는 프로젝트 내부 보조정리 네 개를 증명했다. 리만 가설, 콜라츠
추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 증명하거나
반증하지 않았다.

## 재현 계약

```powershell
python scripts/ticket248_unweighted_wieferich_jet_active.py
python -m unittest tests.test_ticket248_unweighted_wieferich_jet_active -v
python scripts/verify_ticket248_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket248-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

인증서 계산은 정수 또는 `Fraction`만 사용한다. JSON의 부동소수점 값은 표시
전용이며 난수와 seed는 없다.

| 문제 | 새 결과 | 분류 | 상태 |
|---|---|---|---|
| 리만 | 비가중 무한 짝수 모멘트도 전체 정규화 even `L2` 구면에서 coercivity 하한이 0이다 | `exact_no_go` | `open_not_proven` |
| 콜라츠 | 실제 1차 나쁜 가지는 두 generalized-Wieferich 소수 집합의 차집합과 정확히 같다 | `partial_theorem` | `open_not_proven` |
| 강한 골드바흐 | 중심 first-jet 호 전개는 정확한 joint Parseval 에너지와 2차 나머지를 갖는다 | `partial_theorem` | `open_not_proven` |
| 쌍둥이 소수 | 실제 shift-2 소수거듭제곱 이웃을 가진 합성 소수거듭제곱만 정확 오염항에 들어간다 | `partial_theorem` | `open_not_proven` |

## 1. 리만 가설

### A. 정확한 명제: `UnweightedInfiniteMomentCoercivityNoGo`

```text
H=L2_even([-1,1]),
Q_0(f)=sum_(k>=0)|integral_(-1)^1 x^(2k)f(x)dx|^2
```

로 두고 `f_n=sqrt((4n+1)/2)P_(2n)`이라 하자. 그러면

```text
||f_n||_2=1,
첫 n개 짝수 모멘트=0,
Q_0(f_n)<=11/n -> 0.                              (RH-248)
```

비가중치는 `sum 2/(4k+1)`이 발산하므로 TICKET-247의 Hilbert-Schmidt
범위 밖이다. 그럼에도 전체 even `L2` 단위 구면에서는 양의 균일 coercivity를
주지 못한다.

### B-D. 증명

Legendre 직교성으로 소거 모멘트와 노름을 얻는다. `k>=n`이면 Rodrigues
적분으로

```text
mu_(n,k)=2/(2k+1) product_(j=1)^n (k-j+1)/(k+j+1/2)
```

이다. `1-u<=exp(-u)`를 각 인수에 적용하면

```text
mu_(n,k)<=2/(2k+1)exp(-n^2/(k+n+1)).
```

`k+n+1<=3k`이므로 정규화 모멘트 제곱은

```text
((4n+1)/2)k^(-2)exp(-2n^2/(3k))
```

이하이다. `g(x)=x^(-2)exp(-2n^2/(3x))`는 단봉이고
`sum g(k)<=integral g+2sup g`이다. 적분은 `3/(2n^2)`, 최댓값은
`9e^(-2)/n^4<9/(7n^4)`이므로 전체 합은 `11/n`보다 작다.

### E-G. 정확 계산

`n=1,2,4,8,16,32,64,128`에서 점화식과 Rodrigues 계수, 모든 소거
모멘트, 정확 노름, factorial/product 모멘트 공식, `k<=256` 부분 에너지를
독립 비교했다. 실패는 0건이다.

- transcript SHA-256:
  `faaba3834a933146319b810147b5d58136ae13d23bd6599297b292d2ba33c1bd`

### H-I. 한계와 분류

이 열이 실제 Guinand-Weil admissible closure에 속한다고 증명하지 않았다.
비대각 산술 특징도 다루지 않는다. 분류는 `exact_no_go`, RH는
`open_not_proven`이다.

### J-K. 다음 단일 보조정리

```text
ArithmeticOffDiagonalWeilCoercivityOnAdmissibleClosure
```

## 2. 콜라츠 추측

### A. 정확한 명제: `ActualBadBranchGeneralizedWieferichSeparation`

소수 `q>5`에 대해

```text
U_q=(2^(q-1)-1)/q,
V_q=(3^(q-1)-1)/q,
W_q(a,b)=((a^(q-1)-b^(q-1))/q) mod q
```

라 하면 TICKET-246의 `P_q`에 대해 정확히

```text
P_q(U_q,V_q)=W_q(32,27) mod q,
U_q-V_q=W_q(2,3) mod q.                           (CO-248)
```

따라서 실제 quotient 쌍의 1차 valuation 지배 위반 소수는

```text
{q: W_q(32,27)=0} minus {q: W_q(2,3)=0}
```

와 정확히 같다.

### B-D. 증명

TICKET-246의 정확 항등식

```text
32^(q-1)-27^(q-1)=qP_q(U_q,V_q),
2^(q-1)-3^(q-1)=q(U_q-V_q)
```

을 `q`로 나눈 뒤 다시 `q`로 줄이면 된다. 따라서 첫 차이는 `q^2`로
나뉘지만 둘째는 그렇지 않은 경우와 정확히 동치다.

### E-G. exact modular scan

`5<q<=1,000,000`인 소수 78,495개를 `q^2` 모듈러 거듭제곱으로 검사했다.

- `W_q(32,27)=0`: 0개
- `W_q(2,3)=0`: `q=23` 한 개
- separated hit: 0개
- 실패: 0건
- transcript SHA-256:
  `444834a2768b3e94e21d0f968aef0e93fd87f08c540ca52af08756480b6d2d25`

### H-I. 한계와 분류

유한 무적중은 전 소수 부재를 증명하지 않는다. 새 결과는 나쁜 실제 소수
집합의 정확한 환원이다. 분류는 `partial_theorem`, Collatz는
`open_not_proven`이다.

### J-K. 다음 단일 보조정리

```text
ExistenceOfSeparatedGeneralizedWieferichPrimeFor32Over27Against2Over3
```

그런 소수 하나를 찾으면 실제 valuation-domination 경로는 정확한 반례로
폐기되지만 Collatz 자체가 반증되는 것은 아니다.

## 3. 강한 골드바흐 추측 — deep focus

### A. 정확한 명제: `CenteredFirstJetParsevalArcBridge`

`q>=3`, `X>=3`을 고정한다. 축약 잉여류별 소수 개수와 합을 `n_r,m_r`라
하고

```text
P=sum n_r, M=sum m_r,
delta_r=n_r-P/phi(q), eta_r=m_r-M/phi(q),
D_0=sum delta_r^2, D_1=sum eta_r^2,
R_0(a)=sum delta_r exp(2pi iar/q),
R_1(a)=sum eta_r exp(2pi iar/q)
```

라 하자. 모든 실수 `t`에 대해

```text
sum_(a mod q)|R_0(a)+itR_1(a)|^2=q(D_0+t^2D_1).  (GB-248a)
```

또 `M_2=sum p^2`이면

```text
S*(a/q+beta)
=c_q(a)(P+2pi i beta M)/phi(q)
 +R_0(a)+2pi i beta R_1(a)+E(a,beta),
|E(a,beta)|<=2pi^2 beta^2 M_2.                   (GB-248b)
```

### B-D. 증명

`|exp(iu)-1-iu|<=u^2/2`를 각 소수항에 적용하면 2차 나머지가 나온다.
가법 직교성으로

```text
sum_a|R_0|^2=qD_0,
sum_a|R_1|^2=qD_1,
sum_a R_0 conjugate(R_1)=q sum_r delta_r eta_r
```

이고 마지막 값은 실수다. 따라서 `it`가 만드는 교차항의 전체 실수부가
0이어서 joint Parseval 항등식이 성립한다.

### E-G. exact 계산

`X=10,000,100,000,500,000`, 모든 `q=3..96`에서

```text
phi D_0=phi sum n_r^2-P^2,
phi D_1=phi sum m_r^2-M^2,
phi C=phi sum n_rm_r-PM
```

을 정수로 계산하고 centered `Fraction` 합과 독립 비교했다.

- 전체 분모 사례: 282
- 저장 행: 36
- 실패: 0건
- transcript SHA-256:
  `49d39cfb54e21607b0ad1e39ddf0734d30d646bab71b90b82fb746a3f80cc18a`

### H-I. 한계와 분류

Parseval은 분자 `a` 평균을 제어할 뿐 모든 분자의 균일 절약을 주지 않는다.
유한 표는 증가하는 `q`의 점근 추정을 증명하지 않는다. 분류는
`partial_theorem`, 강한 Goldbach는 `open_not_proven`이다.

### J-K. 다음 단일 보조정리

```text
UniformReducedNumeratorCenteredFirstJetSavingOnQuarterTorus
```

## 4. 쌍둥이 소수 추측

### A. 정확한 명제: `ExactActivePrimePowerContaminationIdentity`

`PP(n)`을 홀수 소수거듭제곱 지시자, `P(n)`을 홀수 소수 지시자,
`C(n)=PP(n)-P(n)`이라 하자. 홀수 `n<=X`에서

```text
A_2=sum PP(n)PP(n+2), pi_2=sum P(n)P(n+2),
L=sum C(n)PP(n+2), R=sum PP(n)C(n+2),
B=sum C(n)C(n+2)
```

라 하면 모든 `X>=3`에 대해

```text
A_2-pi_2=L+R-B<=L+R.                              (TP-248)
```

### B-D. 증명

소수거듭제곱 쌍 안에서 거짓 twin은 “왼쪽이 합성”과 “오른쪽이 합성”의
합집합이다. 두 사건의 포함배제를 각 쌍에 적용하고 합하면 된다. shift-2
소수거듭제곱 이웃이 없는 합성 소수거듭제곱은 세 active 항 어디에도 없다.

### E-G. 정확 열거

`X=10,000,000`에서

```text
A_2=59,129, pi_2=58,980,
L=14, R=136, B=1,
A_2-pi_2=L+R-B=149,
L+R=150.
```

같은 규모의 TICKET-247 상계는 2,822였다. `10^7`까지 7개 규모의 실패는
0건이다. transcript SHA-256:
`85f69edcdb7bc23ce3a41d770918c5a4589b4b50a4e003145c47874fa2bd1741`.

### H-I. 한계와 분류

active correction은 정확하지만 그보다 큰 비주기 Type-II 하한을 주지 않는다.
유한 twin 개수는 무한성을 뜻하지 않는다. 분류는 `partial_theorem`, 쌍둥이
소수 추측은 `open_not_proven`이다.

### J-K. 다음 단일 보조정리

```text
ScaleLocalTypeIILowerBoundBeyondActivePrimePowerContamination
```

## 적대적 증명 감사

- RH의 full-`L2` 열을 실제 Weil 허용함수로 바꾸지 않았다.
- Collatz의 78,495개 무적중을 무한 부재로 확대하지 않았다.
- Goldbach 평균제어를 균일제어로 교환하지 않았다.
- Twin의 7개 유한 규모를 무한성으로 확대하지 않았다.
- 모든 유한 인증서는 exact arithmetic이며 proof DAG는 비순환이고 `open`
  frontier가 문제마다 하나다.

## 최종 경계

TICKET-248은 exact no-go 1건, 부분정리 3건, 결정적 인증서와 다음 보조정리
4개를 완료했다. 어느 추측의 해결 게이트도 통과하지 않았다.

이번 회차는 완료되었지만 해당 추측은 해결되지 않았다.
