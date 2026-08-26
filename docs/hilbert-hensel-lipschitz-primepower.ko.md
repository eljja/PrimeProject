# TICKET-247: Hilbert-Schmidt no-go, Hensel 반모형, 호 Lipschitz 전달, 정밀 소수거듭제곱 오염

## 상태 선언

- `iteration_complete`: true
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- `new_partial_theorem_count`: 2
- `exact_no_go_count`: 2
- `stagnated_problem_count`: 0
- deep focus: 리만 가설
- parent: TICKET-246
- 프로그램 상태: `open_not_proven`

이번 회차는 프로젝트 내부 보조정리 네 개를 증명했다. 리만 가설, 콜라츠
추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 증명하거나
반증하지 않았다. 기계 판독 기록은
`data/open-problem/ticket247-hilbert-hensel-lipschitz-primepower.json`이다.

## 재현 계약

```powershell
python scripts/ticket247_hilbert_hensel_lipschitz_primepower.py
python -m unittest tests.test_ticket247_hilbert_hensel_lipschitz_primepower -v
python scripts/verify_ticket247_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket247-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

정리의 근거가 되는 모든 계산은 정수 또는 `Fraction`을 사용한다. JSON의
부동소수점 동반값은 표시 전용이다. 난수는 없고 seed도 필요 없다.

| 문제 | 새 결과 | 분류 | 상태 |
|---|---|---|---|
| 리만 | 모든 Hilbert-Schmidt 가중 짝수 모멘트 특징 사상은 전체 정규화 짝함수 `L2` 구면에서 양의 coercivity 하한을 가질 수 없다 | `exact_no_go` | `open_not_proven` |
| 콜라츠 | 무제약 전소수 valuation 지배에는 모든 소수·깊이에서 유일한 Hensel 반모형 가지가 있다 | `exact_no_go` | `open_not_proven` |
| 강한 골드바흐 | 중심 Parseval 제어를 소수 1차 모멘트 Lipschitz 항과 함께 호로 옮기며, 중심값만의 균일 전달은 불가능하다 | `partial_theorem` | `open_not_proven` |
| 쌍둥이 소수 | 홀수 합성 소수거듭제곱을 지수별로 정확히 세어 오염 보정항을 줄인다 | `partial_theorem` | `open_not_proven` |

## 1. 리만 가설 — deep focus

### A. 정확한 명제: `HilbertSchmidtInfiniteMomentCoercivityNoGo`

다음을 정의한다.

```text
H = L2_even([-1,1]),
w_k >= 0,
sum_(k>=0) 2w_k/(4k+1) < infinity,
Q_w(f)=sum_(k>=0) w_k |integral_(-1)^1 x^(2k)f(x)dx|^2.
```

모든 `n>=1`에 대해 Legendre 다항식 `P_(2n)`으로

```text
f_n=sqrt((4n+1)/2)P_(2n)
```

을 두면

```text
||f_n||_2=1,
integral x^(2k)f_n(x)dx=0                         (0<=k<n),
Q_w(f_n)<=sum_(k>=n)2w_k/(4k+1) -> 0.
```

따라서

```text
inf {Q_w(f): f in H, ||f||_2=1}=0.                (RH-247)
```

즉 좌표가 `sqrt(w_k) integral x^(2k)f`인 특징 사상은
Hilbert-Schmidt이고 무한차원 단위 구면에서 아래로 유계일 수 없다.

### B-D. 정의, 전제, 증명

Legendre 직교성으로 `P_(2n)`은 차수가 `2n`보다 작은 모든 다항식,
특히 `k<n`인 `x^(2k)`와 직교한다. 또

```text
integral_(-1)^1 P_(2n)(x)^2dx=2/(4n+1).
```

따라서 정규화와 소거 모멘트가 정확하다. `k>=n`이면 Cauchy-Schwarz로

```text
|integral x^(2k)f_n|^2 <= integral x^(4k)dx=2/(4k+1).
```

가중합을 취하면 꼬리 상계가 나오고, 전제의 급수가 수렴하므로 그 꼬리는
0으로 간다. 같은 급수는 좌표 함수들의 노름 제곱합이므로 사상이
Hilbert-Schmidt라는 독립 확인도 된다. 표시용 가중치 `w_k=2^(-k)`에는

```text
Q_w(f_n)<=2^(2-n)/(4n+1)
```

이다. 이는 특정 실험의 실패가 아니라 명시한 모든 가중치에 대한 일반
no-go 정리다.

### E-G. 반례·경계 검사와 재현 계산

생성기는 `P_(2n)`을 3항 점화식과 Rodrigues 계수 공식으로 독립 생성한다.
`n=1,2,3,4,5,6,8,10,12,16`에서 두 계수열, 모든 소거 모멘트, 정확한
노름을 비교한다. 마지막 dyadic 상계는 `1/1064960`이다.

- 산술: 정확한 유리수
- 사례 수: Legendre 10행
- 알고리즘: 다항식 점화식과 정확한 convolution, 최대 차수에 대해 3차 이하
- 실패 수: 0
- transcript SHA-256:
  `6f96be5ca5ceffa5ed645e2eb17758ae151b079799bf89baaa00c605cce871a5`

### H-I. 유한 계산 한계와 분류

정리는 전체 짝함수 `L2` 공간에 관한 것이다. Legendre 열이 실제 정규화
Guinand-Weil admissible closure에 속한다고 증명하지 않았고,
non-Hilbert-Schmidt 산술 특징도 다루지 않는다. 분류는 `exact_no_go`다.
리만 가설은 `open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

남은 간극은 또 하나의 summable 모멘트 매장이 아니라 실제 Weil closure의
비콤팩트 산술 coercivity다.

```text
NonHilbertSchmidtArithmeticWeilCoercivityOnAdmissibleClosure
```

## 2. 콜라츠 추측

### A. 정확한 명제: `FormalHenselBranchNoGoForValuationDomination`

소수 `q>5`에 대해 TICKET-246의 다항식을 쓴다.

```text
P_q(U,V)=5U-3V+q(10U^2-3V^2)+q^2(10U^3-V^3)+5q^3U^4+q^4U^5.
```

모든 `r>=1`에 대해 `V_r=5 mod q`이고 다음을 만족하는 `V_r mod q^r`가
유일하게 존재한다.

```text
P_q(3,V_r)=0 mod q^r,
3-V_r=-2 mod q.
```

따라서

```text
v_q(P_q(3,V_r))>=r>0=v_q(3-V_r).                 (CO-247)
```

무제약 `q`진 quotient 쌍 전체에서 `v_q(P_q(U,V))<=v_q(U-V)`라는 명제는
모든 `q>5`, 임의 깊이에서 거짓이다.

### B-D. 증명

`q`를 법으로 보면 `P_q(3,V)=15-3V`이므로 `V=5`가 근이다. `V` 미분은

```text
partial P_q/partial V=-3-6qV-3q^2V^2=-3(1+qV)^2
```

이고 모든 `q>5`에서 unit이다. Hensel lifting은 모든 `q^r`에 유일한
compatible 근을 준다. 이 가지에서 `3-V=-2 mod q`이므로 그 valuation은
0이지만 다항식 valuation은 원하는 만큼 커진다.

### E-G. 정확한 반모형과 재현 계산

깊이 `d`에서 생성기는 역미분을 사용해 다음 base-`q` 숫자의 유일한 선형
합동식을 풀고, 결과를 `q^(d+1)`로 직접 재검사한다.

- 산술: 정확한 정수 모듈러 산술
- 입력: `5<q<=10,000`인 소수 1,226개 전부
- 깊이: 각 소수에서 8자리
- 복잡도: `O(pi(10000)*8*log q)` 모듈러 연산
- 실패 수: 0
- 선택 반모형: `q=7,11,23,101,1009,9973`
- transcript SHA-256:
  `bcb089ee91757f792ae7151212331f811f48a1cc771eea1386d4d4349ba04156`

### H-I. 유한 계산 한계와 분류

이 쌍들은 형식적 `q`진 쌍이지 실제 Fermat quotient

```text
U_q=(2^(q-1)-1)/q, V_q=(3^(q-1)-1)/q
```

가 아니다. 따라서 다항식 항등식만으로 지배를 얻는 경로는 폐기하지만,
실제 quotient 쌍만의 산술 정리를 반증하지 않고 Collatz 궤도도 판정하지
않는다. 분류는 `exact_no_go`, Collatz는 `open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

실제 Fermat quotient 쌍이 이 Hensel 가지에 접근하지 못하게 하는 산술
정보가 필요하다.

```text
ArithmeticFermatQuotientExclusionOfPqHenselBranch
```

## 3. 강한 골드바흐 추측

### A. 정확한 명제: `RationalCenterArcLipschitzBridgeAndCenterOnlyNoGo`

`q>=3`, `X>=3`을 고정한다. `S*(alpha)`는 `q`와 서로소인 홀수 소수
`p<=X`에 대한 `exp(2 pi i alpha p)`의 합이다. 축약 잉여류 개수를 `n_r`,
`P=sum n_r`, `delta_r=n_r-P/phi(q)`, `D=sum delta_r^2`, 같은 소수들의
합을 `M`이라 하면 모든 정수 `a`, 실수 `beta`에 대해

```text
|S*(a/q+beta)-(P/phi(q))c_q(a)|
 <=sqrt(phi(q)D)+2pi|beta|M,                      (GB-247)

phi(q)D=phi(q)sum_r n_r^2-P^2 in Z_>=0.
```

한편 `F_N(beta)=exp(2pi iN beta)-1`은 `F_N(0)=0`이지만
`|F_N(1/(2N))|=2`이고 `1/(2N)->0`이다. 따라서 중심값만으로 최대 주파수와
무관한 균일 연속성 modulus를 얻을 수 없다.

### B-D. 증명

TICKET-246의 중심 분해와 `|R(a)|<=sqrt(phi D)`를 사용한다. 각 소수항에

```text
|exp(2pi i beta p)-1|<=2pi|beta|p
```

를 적용해 합하면 호 이동 상계가 나온다. `delta_r`를 전개하면 정확한 정수
분산식이 나온다. 반례족은 `exp(pi i)=-1`이므로 정확하다.

### E-G. 정확 계산과 적대적 검사

`X=10,000,100,000,500,000`, 모든 `q=3..64`를 검사하고 27개 선택행을
저장했다. 표시 폭은 정확한 `|beta|=1/X^2`이며, 기호적 `2pi` 앞의
`M/X^2`를 유리수로 저장했다. 중심-only 반례족은
`N=10,100,1000,10000`에서 재생한다.

- 산술: 정수·유리수, 복소 부동소수점을 증명에 쓰지 않음
- 분모 사례: 186
- 선택 호 행: 27
- 중심-only 반례: 4
- 실패 수: 0
- `X=500,000` 요약의 최대 `M/X^2`:
  `9914236193/250000000000`
- transcript SHA-256:
  `314c9f28ab175a59fce98474b249cf6e8fbc9fb811f2258d8c344d1b113a89b4`

### H-I. 유한 계산 한계와 분류

Lipschitz 항은 자명 크기일 수 있고 signed 소수 상쇄가 아니다. 유한행은
증가하는 분모에 대한 분산 감쇠를 증명하지 않는다. 반례족은 일반 삼각
다항식에 대한 것이므로 중심값-only 추론만 막는다. 분류는
`partial_theorem`, 강한 골드바흐는 `open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

축약 quarter-torus 호에서 중심 잔차와 signed 소수 1차 모멘트를 동시에
절약해야 한다.

```text
UniformSignedResidueVarianceAndFirstMomentSavingOnQuarterTorus
```

## 4. 쌍둥이 소수 추측

### A. 정확한 명제: `SharpOddPrimePowerContaminationBound`

TICKET-246의 `A_2(X)`, `pi_2(X)`를 유지한다. `Y=X+2`,
`K=floor(log_2Y)`, `pi_odd(t)`를 `t` 이하 홀수 소수 개수라 하자.
`N_odd(Y)`가 `Y` 이하 홀수 합성 소수거듭제곱 개수이면

```text
N_odd(Y)=sum_(k=2)^K pi_odd(floor(Y^(1/k))),

0<=A_2(X)-pi_2(X)<=2N_odd(Y)
 <=2pi_odd(floor(sqrt(Y)))
   +2(K-2)pi_odd(floor(cuberoot(Y))).              (TP-247)
```

### B-D. 증명

홀수 합성 소수거듭제곱은 홀수 소수 `p`와 `k>=2`에 대해 `p^k`로 유일하게
표현되므로 지수별 합이 정확하다. 거짓 소수거듭제곱 쌍은 두 좌표 중 하나에
그런 수를 포함하므로 factor-two union bound가 나온다. `k=2` 항은 정확하고
나머지 `K-2`개 항은 각각 `k=3` 항 이하이다.

### E-G. 정확 열거

생성기는 base/exponent 방식과 소수거듭제곱 support 배열 방식으로
`N_odd`를 독립 계산하고 새 상계를 TICKET-246의 exponent-blind 상계와
비교한다.

- 산술: 정확한 정수
- 범위: `100,1,000,10,000,100,000,1,000,000,5,000,000,10,000,000`
- 복잡도: 체 `O(Y log log Y)`와 선형 support scan
- 실패 수: 0
- `X=10,000,000`: `A_2=59,129`, `pi_2=58,980`, 오염 `149`,
  `N_odd=533`, 새 상계 `2,822`, 이전 상계 `139,128`
- transcript SHA-256:
  `7b336b5638d06b913ebee11fc89308a7a186953083f85cfe772a8a4971410d87`

### H-I. 유한 계산 한계와 분류

정확 보정항은 작아졌지만 `A_2`가 이를 넘는 무한 scale 열은 증명하지
못했다. 유한 열거는 Type-II 상쇄나 무한성을 주지 않는다. 분류는
`partial_theorem`, 쌍둥이 소수 추측은 `open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

```text
ScaleLocalTypeIILowerBoundBeyondSharpPrimePowerContamination
```

## 적대적 증명 감사와 proof DAG 경계

- RH는 모든 summable 가중치를 다루지만 정의역은 전체 짝함수 `L2` 모형임을
  분리했다. Collatz는 모든 소수·깊이를 다루지만 쌍은 무제약임을 분리했다.
- 유한 재생을 무한 결론으로 확대하지 않았다. 무한 명제는 각각 직교성·꼬리
  수렴, Hensel lifting, 지수함수 항별 상계, 소수거듭제곱 유일분해로 증명했다.
- 모든 분모는 양수이고 `q>5`가 Hensel 미분을 unit으로 만든다.
- Goldbach에는 반례족이 필요성을 입증한 주파수-scale 항을 남겼다.
- Twin의 제곱근·세제곱근은 부동소수점이 아닌 정수 floor root다.
- 네 proof DAG는 비순환이고 각각 `open` frontier가 정확히 하나다.
- 어떤 proved 노드도 목표인 원 추측을 전제로 사용하지 않는다.

## 최종 경계

TICKET-247의 네 보조정리, 결정적 인증서, 경로 판정, 다음 보조정리는
완료됐다. 어떤 추측의 해결 게이트도 통과하지 않았다.

이번 회차는 완료되었지만 해당 추측은 해결되지 않았다.
