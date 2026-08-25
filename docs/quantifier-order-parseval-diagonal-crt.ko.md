# TICKET-242: 양화사, order core, Parseval scale, diagonal CRT

상태: **open_not_proven**

상위 추측 해결 수: **0 / 4**

## 주장 경계

TICKET-242는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 증명하거나 반증하지 않는다. 이번 티켓은 네 개의 정확한
경로-경계 정리를 증명하고, 명시된 유한 범위의 계산만 보고한다.

기계 판독 감사:
`data/open-problem/ticket242-quantifier-order-parseval-diagonal-crt.json`.

재현 명령:

```powershell
python scripts/ticket242_quantifier_order_parseval_diagonal_crt.py
python -m unittest tests.test_ticket242_quantifier_order_parseval_diagonal_crt -v
python scripts/verify_ticket242_structure.py
python scripts/verify_open_problem_structure.py
```

## 결과 원장

| 문제 | TICKET-242의 정확한 결과 | 폐기한 경로 | 상태 |
|---|---|---|---|
| 리만 | 고정 test별 수렴·eventual positivity와 매 단계의 moving negative direction이 양립하며, compact-uniform transfer는 충분조건이다 | pointwise finite-section 수렴으로 growing test family positivity를 얻는 경로 | `open_not_proven` |
| 콜라츠 | 나쁜 Fermat-quotient line은 multiplicative-order core의 제곱인수와 정확히 동치이고 그 order들은 unbounded다 | bounded-order core 검사로 all-prime line avoidance를 닫는 경로 | `open_not_proven` |
| 골드바흐 | global Parseval minor bound는 `pi(X)` 규모여서 자연스러운 binary main scale보다 로그 한 개 크다 | global `L2` energy와 triangle inequality만으로 binary lower certificate를 닫는 경로 | `open_not_proven` |
| 쌍둥이 소수 | 임의의 growing-period classifier 열에도 strictly increasing prime/composite-successor mimic 열이 존재한다 | modulus growth 자체가 결국 twin을 분리한다는 경로 | `open_not_proven` |

## 1. 리만 가설

### 이번에 선언한 정확한 명제

`H=l2(N)`에서

```text
A_n = I - 2 <.,e_n> e_n
```

으로 둔다. 모든 고정된 `x in H`에 대해

```text
<A_n x,x> = ||x||^2 - 2|x_n|^2 -> ||x||^2
```

이고, `x!=0`이면 이 값은 충분히 큰 `n`에서 양수다. 그러나 모든 `n`에서

```text
inf_(||x||=1) <A_n x,x> = -1
```

이며 moving test `x=e_n`에서 등호가 성립한다.

반대로 `K`가 compact normalized test class이고, `q_n -> q`가 `K` 위에서
uniform하며 `inf_K q >= delta>0`이면 충분히 큰 `n`에서

```text
inf_K q_n >= delta/2
```

이다.

### 수학적 논증

제곱합 가능 수열은 `x_n->0`이므로 fixed-test 수렴이 성립한다. `x!=0`이면
결국 `2|x_n|^2<||x||^2`이므로 eventual positivity도 성립한다. 하지만
`e_n`을 대입하면 값은 정확히 `-1`이다. 즉

```text
모든 고정 test는 결국 양수
```

라는 양화사 순서는

```text
결국 growing family의 모든 test가 양수
```

를 함의하지 않는다. Compact transfer는

```text
q_n(x) >= q(x) - sup_K |q_n-q| >= delta/2
```

로 끝난다.

### 재현 가능한 계산

차원 `4, 8, 16, 32, 64, 128`의 여섯 exact diagonal section을 기록했다.
각 행은 다음을 만족한다.

- 최소 고윳값 `-1`;
- 음의 방향 정확히 하나;
- 고정된 앞쪽 coordinate probe 값 `+1`;
- `||A_n-I||=2`;
- normalized trace `1-2/n`은 `1`로 접근하지만 음의 방향은 사라지지 않음.

Transcript SHA-256:
`f694cbcb62bd7a5fbe6cb3ade6516ceddb753012675f000aa9970cad15226e4f`.

### no-go, 한계, 다음 보조정리

fixed-test finite-section 수렴, fixed-test eventual positivity, 평균 진단량의
수렴만으로 uniform signed Weil lower bound를 주장하는 경로를 폐기한다.

이 대각 형식은 추상적인 양화사 반례이지 Guinand-Weil 형식이 아니다. 실제
admissible test class의 compactness, frequency tightness, uniform arithmetic
tail, positive limit margin은 증명되지 않았다.

다음 단일 보조정리:

`UniformSignedGuinandWeilTailBoundOnFrequencyTightNormalizedAdmissibleTestClasses`.

## 2. 콜라츠 추측

### 이번에 선언한 정확한 명제

소수 `q>5`에 대해

```text
d = ord_q(32/27)
```

로 두면

```text
v_q(32^(q-1)-27^(q-1)) = v_q(32^d-27^d)
```

이다. 따라서 나쁜 Fermat-quotient line

```text
5 F_q(2) = 3 F_q(3) mod q
```

은

```text
q^2 | 32^d-27^d
```

와 정확히 동치다. 또한 `ord_q(32/27)`은 소수 `q`에 따라 unbounded다.

### 수학적 논증

`q-1=dk`라 쓰면 `1<=k<q`이므로 `q`는 `k`를 나누지 않는다. LTE로

```text
v_q((32^d)^k-(27^d)^k)
  = v_q(32^d-27^d)+v_q(k)
  = v_q(32^d-27^d).
```

만약 모든 order가 `D` 이하라면 모든 소수 `q>5`가 고정된 비영 정수

```text
product_(1<=d<=D) (32^d-27^d)
```

를 나누게 된다. 이는 이 정수가 유한 개의 소인수만 갖는다는 사실과 소수의
무한성에 모순이다.

### 재현 가능한 계산

`5<q<=200,000`인 `17,981`개 소수 전체에서 order-core depth와 full
exponent `q-1` depth가 정확히 일치했다. 나쁜 line 후보는 없었다. 그러나
TICKET-241은 이미 `10^8`까지 검색했으므로 이번 작은 scan은 검색 범위
확장이 아니라 LTE identity의 독립 replay다.

관측한 최대 order:

| 소수 상한 | 최대 order | 증인 소수 |
|---:|---:|---:|
| 100 | 82 | 83 |
| 1,000 | 990 | 991 |
| 10,000 | 9,966 | 9,967 |
| 100,000 | 99,970 | 99,971 |
| 200,000 | 199,998 | 199,999 |

Transcript SHA-256:
`ede3279e2ec7d5e375ec2e3ea65349459e401f9174c8eee13b7b697aacc70fec`.

### no-go, 한계, 다음 보조정리

고정 order cutoff로 모든 소수를 덮는 경로는 확정적으로 폐기된다. 정확한
LTE 환원은 unbounded order core에서 제곱인수를 배제하지 못한다. 일반
necklace와 aperiodic Collatz descent도 그대로 열려 있다.

다음 단일 보조정리:

`UniformOrderCoreSquareDivisorTransferFrom32Over27To2Over3`.

## 3. 강한 골드바흐 추측

### 이번에 선언한 정확한 명제

```text
S_X(alpha) = sum_(p<=X) e(p alpha)
```

라 두면 Parseval에 의해

```text
integral_0^1 |S_X(alpha)|^2 d alpha = pi(X).
```

임의의 measurable minor-arc set `m`과 짝수 `N`에 대해

```text
|integral_m S_X(alpha)^2 e(-N alpha) d alpha|
  <= integral_m |S_X(alpha)|^2 d alpha
  <= pi(X).
```

따라서 minor estimate가 global Parseval bound뿐인 binary lower
certificate는 `M_X(N)=o(pi(X))`인 main term을 이길 수 없다. 특히 PNT로

```text
X/log^2 X = o(pi(X)).
```

### 수학적 논증

첫 부등식은 target Fourier coefficient에 triangle inequality를 적용한
것이고, 적분 영역을 전체 원으로 늘리면 Parseval energy `pi(X)`를 얻는다.
`M_X=o(pi(X))`이면 결국 `M_X-pi(X)<0`이다. PNT의
`pi(X)~X/log X`를 쓰면 두 scale의 비는 `log X` 크기다.

### 재현 가능한 계산

`10^3<=X<=10^6`의 일곱 prime count와 sample even-target convolution을
감사했다. 비율

```text
pi(X)/(X/log^2 X)
```

은 `8.0165`에서 `14.9828`로 증가했다. 모든 행에서 global `L2` bound가
관측된 ordered representation count 전체보다 크거나 같았다.

Transcript SHA-256:
`fa85d668b1b025ab2a81b01ed957cc2ada5f4758a99e0a39874434521ac05280`.

### no-go, 한계, 다음 보조정리

global `L2`와 triangle inequality만 쓰는 경로만 폐기한다. targetwise
signed cancellation, restriction estimate, Type I/II decomposition 또는 더
정교한 fixed major/minor arc 구조는 반증하지 않았다. Goldbach 반례도 없다.

다음 단일 보조정리:

`FixedBinaryPrimeMinorArcCoefficientIsLittleOOfTargetMainUniformlyOnBufferedEvenTargets`.

## 4. 쌍둥이 소수 추측

### 이번에 선언한 정확한 명제

임의의 양의 period 열 `(M_j)`를 잡고 각 `j`에서

```text
gcd(a_j,M_j)=gcd(a_j+2,M_j)=1
```

인 `a_j mod M_j`와 `M_j`-periodic feature `F_j`를 잡는다. 그러면
strictly increasing prime 열 `(p_j)`가 존재하여

```text
F_j(p_j,p_j+2)=F_j(a_j,a_j+2)
```

이면서 `p_j+2`는 composite다.

### 수학적 논증

각 단계에서 `2M_j`를 나누지 않는 소수 `ell_j`를 고르고

```text
p_j = a_j mod M_j,
p_j = -2  mod ell_j
```

를 동시에 부과한다. CRT는 modulo `M_j ell_j`의 reduced residue class를
준다. Dirichlet 정리로 그 class에는 소수가 무한히 많으므로
`p_j>max(p_(j-1),ell_j)`를 선택할 수 있다. Periodicity는 `F_j`를 보존하고,
`ell_j | p_j+2`는 successor를 proper composite로 만든다.

### 재현 가능한 계산

`30`에서 `9,699,690`까지 여섯 growing period를 사용했다. Exact increasing
prime witness는

```text
131, 1,901, 48,527, 1,651,667, 6,126,149, 902,071,199
```

이다. 마지막 단계에서는

```text
p+2 = 23 * 39,220,487.
```

Transcript SHA-256:
`5cc91d6440bc282199fd9b5f348d758fa23b256a593c890d2199e49f75c1ed79`.

### no-go, 한계, 다음 보조정리

modulus growth만으로 twin certificate를 얻는 경로를 폐기한다. 그러나 이
구성은 CRT class 뒤에 scale을 선택한다. 미리 선언된 dyadic block 안에
counterfeit를 놓지 않으며 quantitative least-prime estimate도 주지 않는다.
진정한 nonperiodic signed Type II 정보는 no-go 바깥에 남는다.

다음 단일 보조정리:

`ScaleLocalGrowingModulusTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass`.

## proof DAG 요약

각 트랙은 다음 의존성 구조를 갖는다.

```text
TICKET-241 closed input
  -> TICKET-242 rejected inference
  -> TICKET-242 exact theorem
  -> one highest-risk open lemma
```

상위 추측의 증명 또는 반증으로 표시된 DAG node는 없다.

## 최종 경계

TICKET-242는 네 개의 정확한 부분정리 또는 no-go 정리를 확립했다. 남은
보조정리는 각각 uniform signed Weil tail, all-order rational Wieferich
square-divisor transfer, targetwise signed binary minor-arc cancellation,
scale-local parity-sensitive Type II estimate를 요구한다. 네 상위 추측은 모두
미해결이다.
