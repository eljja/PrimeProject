# TICKET-222: 손실 없는 결합과 편향 패리티 교정

영문판: [lossless-coupling-biased-parity.md](lossless-coupling-biased-parity.md)

## 주장 상태

**리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측은
모두 여전히 미해결이다.** TICKET-222는 네 개의 더 좁은 관측 유일성 또는
패리티 교정 정리를 증명한다. 어떤 상위 추측의 완전한 증명이나 반례도
제공하지 않는다.

기계 판독 상태는 `open_not_proven`이고 상위 추측 해결 개수는 `0`이다.

| 문제 | TICKET-222의 정확한 결과 | 폐기 또는 교정한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | 높이 0에서 떨어진 콤팩트 지지 유한 signed defect는 전체 이진 Laplace 대역 프로필로 유일하게 결정된다 | 전체 결합 프로필 자체가 정보를 잃는다는 주장, 또는 콤팩트 injectivity를 증명 없이 무한 꼬리에 적용하는 경로 | `ActualZetaCofinalDyadicEnclosureWithVanishingUnboundedTail` |
| 콜라츠 | `(h,S,B)`는 valuation word의 손실 없는 코드이고 `D>0`, `D|B`가 정확한 유한 단어 cycle 판정이다 | 정확한 ordered intercept 대신 비순서 scalar 요약량을 더 추가하는 경로 | `AllNontrivialPrimitiveCodesFailDivisibilityOrEveryAperiodicRayDescends` |
| 골드바흐 | 순서 있는 표현 개수의 패리티는 정확히 `N/2`의 소수 지시자다 | 표현 개수의 홀짝을 0/양성 판별기로 사용하는 경로 | `UniformCofinalPositiveGoldbachCountLowerBound` |
| 쌍둥이 소수 | 유한 wheel 나눗셈 패리티는 정확한 편향 곱 leakage 공식을 만족한다 | 균형 Boolean 직교성을 편향 wheel 변수에 그대로 적용하거나, 0이 아닌 leakage를 소수쌍 하한으로 해석하는 경로 | `ScaleGrowingBiasedParitySignalDominatesTypeIIRemainder` |

---

## 1. 리만 가설

### 1.1 선언 명제

`CompactSupportFullDyadicLaplaceProfileInjectivity`

`sigma`를 `0<a<b`인 `[a,b]`에 지지된 유한 signed Borel measure라고 하자.

```text
L_sigma(s) = integral exp(-s t) d sigma(t),
W_j(sigma) = L_sigma(2^(-j)) - L_sigma(2^(1-j)),  j in Z
```

로 놓는다. 모든 정수 `j`에 대해 `W_j(sigma)=0`이면 `sigma=0`이다.
따라서 이 measure class에서는 전체 양방향 이진 프로필이 measure를
유일하게 결정한다.

### 1.2 증명

`s_j=2^(-j)`로 놓는다. `W_j=0`은 모든 `j`에서

```text
L_sigma(s_j)=L_sigma(s_(j-1))
```

를 뜻하므로 이진 표본값은 모두 같은 상수다. `j`가 음의 무한대로 갈 때
`s_j`는 무한대로 간다. 지지가 양의 수 `a` 이상에 있으므로
`L_sigma(s_j)`는 0으로 간다. 따라서 모든 이진 표본값이 0이다.

콤팩트 지지 때문에 `L_sigma`는 entire function이다. 영점 `s_j`는 내부점
0에 모이므로 identity theorem에 의해 `L_sigma`는 항등적으로 0이다.
0에서 미분하면 모든 다항식 moment가 0이고, `[a,b]`에서 다항식이
연속함수에 조밀하므로 `sigma=0`이다.

### 1.3 무엇이 해결됐고 무엇이 남았는가

TICKET-221은 각 스케일을 독립적으로 최악화한 상계의 합이 발산함을
증명했다. TICKET-222는 그 실패 원인이 **전체 결합 관측량**의 정보 손실은
아님을 보인다. 선언한 콤팩트 measure class에서 전체 프로필은 손실이 없다.

그러나 실제 RH defect는 높이의 무한 꼬리를 다뤄야 한다. 프로젝트는 아직
실제 소수 explicit formula로부터 공종 콤팩트 소진과 소멸 꼬리를 동시에
보증하는 enclosure를 만들지 못했다. TICKET-220에 따라 유한 대역 창만으로는
여전히 충분하지 않다.

### 1.4 재현 계산

`[1,9]` 위의 총질량 4인 원자 measure 두 개를 100자리 Decimal로
`j=-12,...,12`에서 평가했다. 전체 프로필은 서로 다르다. 반경
`2,4,8,12,16,24,32`의 부분합은 선언한 허용오차에서 telescoping 경계식과
일치하고 총질량 4로 접근한다.

계산은 구현 검산이고 injectivity의 근거는 위 해석학적 증명이다.

**남은 간극:** 실제 zeta에 대한 소수 측 공종 enclosure와 엄밀한 무한 꼬리
소멸이 없다.

**다음 보조정리:**
`ActualZetaCofinalDyadicEnclosureWithVanishingUnboundedTail`.

---

## 2. 콜라츠 추측

### 2.1 선언 명제

`SlopeInterceptLosslessValuationCodeAndExactCycleReduction`

양의 가속 valuation word `a=(a_1,...,a_h)`에 대해

```text
S = sum_i a_i,
B_h(a) = sum_(i=1)^h 3^(h-i) 2^(a_1+...+a_(i-1)),
D = 2^S - 3^h
```

로 놓는다. 그러면 `(h,S,B_h)`는 ordered word를 유일하게 결정한다. 또한
이 word가 양의 정수 accelerated cycle을 실현하는 것과

```text
D>0 and D divides B_h
```

는 동치다.

### 2.2 손실 없는 복호기

Affine intercept는 다음 재귀식을 만족한다.

```text
B_h(a_1,...,a_h)
  = 3^(h-1) + 2^(a_1) B_(h-1)(a_2,...,a_h).
```

양의 단어의 tail intercept는 항상 홀수이므로

```text
a_1 = v_2(B_h-3^(h-1))
```

이다. 해당 2의 거듭제곱으로 나누면 tail intercept가 나오고, 재귀적으로
`a_1,...,a_(h-1)`을 복원한다. 마지막 valuation은 `S`에서 복원한 prefix
합을 빼면 된다.

따라서 intercept는 단순히 순서에 민감한 정도가 아니다. `h,S`와 함께
보존하면 단어 정보를 전혀 잃지 않는다.

### 2.3 정확한 cycle 판정

`B_i`를 위치 `i`에서 시작하는 cyclic rotation의 intercept라 하면

```text
2^(a_i) B_(i+1)=3B_i+D
```

이다. `D`는 6과 서로소이므로 `D|B_i`는 rotation에 불변이다. `D|B_0`이면
모든 `n_i=B_i/D`는 양의 홀수이고

```text
3n_i+1=2^(a_i)n_(i+1)
```

이다. 다음 값이 홀수이므로 `a_i`가 정확한 2-adic valuation이고 궤도는
닫힌다. 역방향은 cycle의 affine 고정점 식에서 바로 나온다.

### 2.4 재현 계산

valuation `{1,2,3,4,5}`에서 길이 8 이하의 488,280개 단어를 전수
검사했다.

- 고정 길이 `(S,B)` 코드 충돌: `0`;
- 재귀 복호 실패: `0`;
- `D|B`인데 정확한 cycle replay가 실패한 경우: `0`.

유한 개수는 구현 검산이다. 재귀 증명은 모든 유한 양의 단어에 적용된다.

### 2.5 남은 간극

손실 없는 코딩은 환원이지 cycle 배제가 아니다. all-two가 아닌 모든
primitive code에서 `D`가 `B`를 나누지 않음을 증명하거나 실제 나눗셈
반례를 찾아야 한다. 주기 cycle을 완전히 분류하더라도 비주기 발산 branch는
별도로 남는다.

**다음 보조정리:**
`AllNontrivialPrimitiveCodesFailDivisibilityOrEveryAperiodicRayDescends`.

---

## 3. 강한 골드바흐 추측

### 3.1 선언 명제

`OrderedGoldbachCountParityEqualsDiagonalPrimeIndicator`

짝수 `N>=6`에 대해

```text
R_ord(N) = #{(p,q): p,q are odd primes and p+q=N}
```

로 놓고 순서를 구분한다. 그러면

```text
R_ord(N) mod 2 = 1_P(N/2)
```

이다.

### 3.2 증명과 no-go

대칭 변환 `(p,q)->(q,p)`는 모든 비대각 표현을 두 개씩 짝짓는다. 고정점은
`p=q=N/2`뿐이고, 이는 `N/2`가 홀수 소수일 때 정확히 존재한다.

따라서 표현 개수의 패리티는 0 검출기가 아니다. 예를 들어

```text
20=3+17=7+13
```

은 순서 있는 표현이 네 개라 패리티가 0이다. 가상의 반례도 개수 0이므로
같은 패리티를 갖는다. 이로써 TICKET-221의 엄격한 `L^p` 양성 반경을 count
parity 한 비트로 대체하는 경로를 폐기한다.

### 3.3 재현 계산

정확한 sieve로 `6<=N<=100000`의 모든 짝수에 대해 순서 있는 홀수 소수
표현 개수를 계산했다.

- 패리티 항등식 실패: `0`;
- 이 범위의 골드바흐 반례: `0`;
- 양성이면서 짝수 패리티인 target: `N=20`을 포함해 다수.

이는 구현 진단일 뿐이다. 이미 출판된 계산 검증 범위는 `4*10^18`이므로
TICKET-222는 새로운 검증 기록을 주장하지 않는다.

### 3.4 남은 간극

모든 충분히 큰 짝수에서 전체 표현 개수가 양수라는 one-sided 하한을
증명하거나, 정수인 꼬리 예외 개수를 엄격히 1 아래로 내려 기존 유한 검증과
연결해야 한다.

**다음 보조정리:** `UniformCofinalPositiveGoldbachCountLowerBound`.

---

## 4. 쌍둥이 소수 추측

### 4.1 선언 명제

`FiniteWheelBiasedParityLeakageProductFormula`

서로 다른 홀수 소수 `q_1,...,q_m`을 택하고 `W=product q_i`라 하자.
`n`을 `W` modulo에서 균일하게 택하고

```text
X_q(n) = -1  if q divides n(n+2),
          1  otherwise,
P(n) = product_q X_q(n)
```

로 놓는다. 모든 부분집합 `S`에 대해

```text
E[P product_(q in S)X_q]
  = product_(q not in S)(1-4/q)
```

이다.

### 4.2 증명

홀수 소수 `q`에서 `q|n(n+2)`인 residue는 `0,-2` 두 개다. 따라서

```text
E[X_q]=(q-2-2)/q=1-4/q.
```

CRT는 `W` modulo의 균일 residue를 각 `q` modulo 균일 residue의 곱으로
바꾸므로 부호들이 독립이다. `P`와 `S` monomial을 곱하면 선택한 좌표는
제곱되어 1이 되고, 빠진 좌표만 평균을 기여하므로 공식이 나온다.

### 4.3 TICKET-221의 범위 교정

균형 cube에서는 모든 proper Walsh monomial이 parity와 정확히 직교한다.
그러나 실제 유한 wheel 나눗셈 변수는 균형이 아니다. 모든 홀수 소수에서
`mu_q=1-4/q`가 0이 아니므로 모든 proper **uncentered** monomial에 0이 아닌
parity leakage가 있다.

이는 TICKET-221 stress model의 적용 범위를 교정하지만 sieve parity 문제를
없애지 않는다. 고정 wheel에는 여전히 두 수가 모두 합성수인 CRT 등차수열이
있고, `P`는 선택한 작은 소인수 개수의 parity이지 primality가 아니다. 0이
아닌 leakage만으로 `Lambda(n)Lambda(n+2)`의 양의 하한은 나오지 않는다.

### 4.4 재현 계산

`W=3*5*7*11=1155`에서 모든 residue와 16개 부분집합 `S`를 전수 검사했다.
모든 유리수 상관값이 곱 공식과 정확히 일치했다. 소수 `43`까지의 prefix도
exact fraction으로 계산해, 고정 차수 leakage가 빠진 모든 국소 bias의 곱으로
감쇠하는 양상을 기록했다.

### 4.5 남은 간극

스케일과 함께 산술 정보를 키우고, 보존된 편향 parity 신호가 signed Type-II
및 tail remainder를 무한히 많은 탈출 block에서 지배함을 증명해야 한다.

**다음 보조정리:**
`ScaleGrowingBiasedParitySignalDominatesTypeIIRemainder`.

---

## 문헌 경계

외부 문헌은 범위를 교정하기 위해 사용하며 우선권 주장에 사용하지 않는다.

- Connes와 Consani, [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368): 결합 Weil positivity 경계.
- Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562): 거의 모든 궤도와 모든 궤도의 양화사 차이.
- Oliveira e Silva, Herzog, Pardi, [Empirical verification of the even Goldbach conjecture and computation of prime gaps up to `4*10^18`](https://doi.org/10.1090/S0025-5718-2013-02787-1): 유한 계산 검증 경계.
- Ford와 Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368): 일반 prime-producing 하한에서 충분한 Type-I/Type-II 정보의 필요성.

독립된 전문가 검토 전에는 TICKET-222에 대한 문헌 우선권을 주장하지 않는다.

## 재현

```powershell
python scripts/ticket222_lossless_coupling_biased_parity.py
python -m unittest tests.test_ticket222_lossless_coupling_biased_parity -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

기본 기계 판독 artifact:

`data/open-problem/ticket222-lossless-coupling-biased-parity.json`
