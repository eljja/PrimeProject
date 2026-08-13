# TICKET-225: 산술 나머지의 명시적 분해

## 상태와 주장 범위

TICKET-225는 TICKET-224의 네 proof DAG를 이어간다. 이전에 막연하게
남아 있던 오차를 실제 von Mangoldt 꼬리, 콜라츠 cyclic gcd 몫,
골드바흐·쌍둥이 소수의 cube-root rough semiprime 오염항으로 바꾼다.
상위 난제는 하나도 해결하지 않는다.

| 연구 트랙 | 정확한 새 결과 | 폐기 또는 제한한 경로 | 상위 난제 상태 |
|---|---|---|---|
| 리만 가설 | 실제 von Mangoldt Laplace band의 계산 가능한 꼬리 구간과 finite-band 비단사성 | 유한 개 소수 band 부호가 RH 판정이라는 경로 | 미해결 |
| 콜라츠 추측 | `D/gcd(D,B)`가 모든 cyclic rotation에서 불변 | 회전마다 독립 prime-power deficit을 누적하는 경로 | 미해결 |
| 강한 골드바흐 추측 | 세제곱근 체 생존 합성수는 정확히 rough semiprime이며 convolution이 네 항으로 분해됨 | 모든 cube-root wheel 표현이 prime-prime이라는 경로 | 미해결 |
| 쌍둥이 소수 추측 | cube-root 생존쌍을 `PP/PS/SP/SS`로 정확히 분류 | 모든 생존쌍이 쌍둥이 소수라는 경로 | 미해결 |

공통 진전은 해결이 아니라 나머지의 위치를 정확히 지정한 것이다. 다음
증명은 이제 이름 붙은 구체적 항을 제어해야 한다.

## 1. 리만 가설

### 이번에 증명한 정확한 명제

`a>0`에 대해 실제 소수 쪽 Laplace-band 결함을

```text
P(a)=sum_(n>=2) Lambda(n)[exp(-an)-exp(-2an)]-1/(2a)
```

로 정의한다. 모든 정수 `N>=2`와 `q=exp(-a)`에 대해 생략한 소수항은

```text
0 <= sum_(n>N) Lambda(n)[q^n-q^(2n)]
   <= q^(N+1)((N+1)-Nq)/(1-q)^2.                 (RH-225.1)
```

따라서 유한 von Mangoldt 합과 `(RH-225.1)`은 전체 band를 포함하는
명시적 구간을 제공한다.

반면 임의의 유한 band 함수족에는 공통 kernel에 놓이는 0이 아닌 유한
지지 부호 측도가 존재한다. 그러므로 유한 개 band 값이나 부호만으로
임의의 결함 측도를 복원할 수 없고, 이것만으로 RH 판정을 만들 수 없다.

### 수학적 논증

주항은 다음 적분과 정확히 같다.

```text
integral_0^infinity [exp(-ax)-exp(-2ax)] dx=1/(2a).
```

또한 `n>=2`에서

```text
0<=exp(-an)-exp(-2an)<=exp(-an),
Lambda(n)<=log n<=n.
```

따라서 꼬리는 `sum_(n>N)nq^n` 이하이고, 기하급수를 미분하면
`(RH-225.1)`의 닫힌 식을 얻는다.

유한 관측 no-go는 선형대수다. `m`개 band를 서로 다른 `m+1`개 원자에
평가하면 `R^(m+1)`에서 `R^m`으로 가는 선형사상이 된다. Rank-nullity에
의해 공통 kernel의 0이 아닌 원자 가중치가 존재한다. 이 결론은 추가
band도 사라진다는 주장이 아니라 유한 관측의 비단사성을 증명한다.

### 재현 계산

`a=2^-j`, `j=3,...,15`에서 `N=48*2^j`까지 계산했다. 13개 유한합은
명시적 양의 꼬리 상계를 더한 뒤에도 모두 음수다. 관측 band 3개부터
8개까지 만든 여섯 행렬은 수치적으로 full row rank이고, 관측 수보다
원자 하나를 더 둔 null vector의 최대 잔차는 `10^-10` 미만이다.

이는 이 소수 쪽 관측량의 유한 부호 인증서다. 제타 영점의 interval
검증도 아니고 RH 증명도 아니다.

### 한계, 폐기 경로, 다음 보조정리

- 폐기: 유한 개 실제 소수 band 부호를 RH 판정으로 사용.
- 유지: cofinal 소수 band 부등식을 명시공식을 통해 조밀한 Weil
  test-function core의 양성으로 옮기는 경로.
- 남은 간극: 인증한 부호에서 전체 Weil quadratic form 양성이나
  임계선 밖 영점 부재로 가는 정리가 없다.
- 다음 단일 보조정리:
  `ExplicitFormulaTransferFromCofinalPrimeBandMarginsToWeilCorePositivity`.

## 2. 콜라츠 추측

### 이번에 증명한 정확한 명제

양의 accelerated Collatz valuation word `a=(a_1,...,a_h)`에 대해

```text
S=sum a_i,
D=2^S-3^h>0
```

로 두고 `B_i`를 `i`번째 cyclic rotation의 affine intercept라 하자.
인접 회전은

```text
2^(a_i)B_(i+1)=3B_i+D                             (CO-225.1)
```

를 만족한다. 따라서

```text
gcd(D,B_i)=gcd(D,B_(i+1))
```

이고 residual obstruction `R=D/gcd(D,B_i)`는 모든 회전에서 같다. 어떤
회전 하나라도 `0<B_i<D`이면 그 word는 cycle이 아니다.

### 수학적 논증

첫 항을 분리해

```text
B_i=3^(h-1)+2^(a_i)C
```

로 쓰면 다음 회전은 `B_(i+1)=3C+2^(S-a_i)`다. `2^(a_i)`를 곱하면

```text
2^(a_i)B_(i+1)=3(B_i-3^(h-1))+2^S=3B_i+D.
```

`D`는 2, 3과 모두 서로소이므로 `D`와 gcd를 취하면 불변성이 따른다.
TICKET-222의 exact condition은 cycle이면 `D|B_i`임을 요구하므로,
`0<B_i<D`는 즉시 noncycle 인증서다.

### 재현 계산

높이 `2..7`, alphabet `{1,2,3,4,5}`의 모든 word를 열거했다. `D>0`인
원시 word 97,016개에서 655,188개 인접 회전 항등식과 모든 gcd 불변식의
실패는 0개다. Minimum-intercept 검사는 96,127개를 noncycle로 인증했다.
비자명 cycle은 발견되지 않았지만 889개 word는 이 충분조건만으로
해결되지 않았다.

TICKET-224의 `(1,1,2,4,3)`은 모든 회전에서

```text
gcd(D,B_i)=95,  D/gcd(D,B_i)=19
```

이다. 회전을 늘려도 독립적인 소수 거듭제곱 정보가 생기지 않는다.

### 한계, 폐기 경로, 다음 보조정리

- 폐기: 회전을 독립 prime-power deficit 표본으로 누적.
- 유지: 가장 작은 cyclic intercept를 전역 cycle 방해로 사용하고,
  비주기 궤도는 별도 하강 정리로 처리.
- 남은 간극: 모든 비자명 원시 word에서 `min_i B_i<D`라는 균일 정리와
  비주기 하강 정리가 없다.
- 다음 단일 보조정리:
  `UniformCyclicInterceptDescentOrAperiodicOrbitDescent`.

## 3. 강한 골드바흐 추측

### 이번에 증명한 정확한 명제

`z^3>=X`라 하자. `Q_z(m)`이 소수와 `z` 이하 소인수가 없는 수를
통과시킨다고 하자. `X` 이하에서 통과한 모든 합성수는 정확히

```text
m=r*s,  r,s는 z보다 큰 소수
```

이며 중복을 허용한다. `P`를 소수 indicator, `S_z`를 이 rough-semiprime
indicator라 하면 `[2,X]`에서

```text
Q_z=P+S_z.                                         (GB-225.1)
```

모든 짝수 `N<=X`에 대해 ordered convolution은 정확히

```text
Q_z*Q_z(N)
=P*P(N)+P*S_z(N)+S_z*P(N)+S_z*S_z(N).             (GB-225.2)
```

### 수학적 논증

통과한 합성수의 모든 소인수는 `z`보다 크다. 소인수가 중복도를 포함해
세 개 이상이면 `m>z^3>=X`가 되어 모순이다. 따라서 정확히 두 개다.
역은 즉시 성립한다. `(P+S_z)*(P+S_z)`를 전개하면 `(GB-225.2)`를 얻는다.

### 재현 계산

`X=1,000`, `10,000`, `100,000` 전체를 분류했고 factorization 및 분류
오류는 0개다. `N=X`에서 ordered count는 다음과 같다.

| `X` | `P*P` | `P*S` | `S*P` | `S*S` | filter 전체 |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 56 | 19 | 19 | 4 | 98 |
| 10,000 | 254 | 118 | 118 | 34 | 524 |
| 100,000 | 1,620 | 759 | 759 | 294 | 3,432 |

명시적 rough-semiprime 대각쌍은 개별 filter witness가 반드시 prime-prime은
아님을 보여준다.

### 한계, 폐기 경로, 다음 보조정리

- 폐기: 모든 cube-root wheel 표현을 prime-prime으로 해석.
- 유지: 세 rough-semiprime convolution을 filter main term보다 작게 제한.
- 남은 간극: 모든 짝수에서 `P*P(N)>0`을 주는 균일 상계가 없다.
- 다음 단일 보조정리:
  `UniformCubeRootRoughSemiprimeErrorBelowGoldbachWheelMainTerm`.

## 4. 쌍둥이 소수 추측

### 이번에 증명한 정확한 명제

`z^3>=X`일 때 `n+2<=X`인 모든 gap-two 생존쌍 `(n,n+2)`은 정확히

```text
PP, PS, SP, SS
```

중 하나다. `P`는 소수, `S`는 `z`-rough semiprime이다. 따라서

```text
전체 생존쌍=PP+PS+SP+SS.                           (TP-225.1)
```

쌍둥이 소수는 `PP`뿐이다. 양의 생존쌍 개수나 개별 wheel 인증서는 그
자체로 쌍둥이 소수 인증서가 아니다.

### 수학적 논증

`(GB-225.1)`을 `n`, `n+2`에 각각 적용한다. 네 유형은 서로 겹치지 않고
전체를 덮으므로 indicator와 count가 정확히 합쳐진다. 명시적 `SS` pair는
두 filter가 모두 양성이면서 두 수 모두 합성수인 경우를 제공한다.

### 재현 계산

| `X` | `PP` | `PS` | `SP` | `SS` | 첫 `SS` pair |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 35 | 19 | 14 | 4 | `(527,529)` |
| 10,000 | 205 | 78 | 76 | 35 | `(1679,1681)` |
| 100,000 | 1,224 | 559 | 537 | 253 | `(4187,4189)` |

표시한 모든 pair는 두 rough semiprime으로 직접 소인수분해해 검증했다.

### 한계, 폐기 경로, 다음 보조정리

- 폐기: cube-root 생존쌍을 쌍둥이 소수 인증서로 사용.
- 유지: 세 contamination class를 모두 제어한 뒤 양의 `PP` 하한을 증명.
- 남은 간극: `PS+SP+SS`의 균일 점근 상계와 무한히 증가하는 `PP` 하한이
  없다.
- 다음 단일 보조정리:
  `PositiveTwinPrimeLowerBoundAfterCubeRootSemiprimeContaminationControl`.

## 네 트랙의 통합 결론

TICKET-225는 질적인 미해결 항목을 명시적 나머지로 바꿨다.

1. RH에는 고립된 band 부호를 더 계산하는 것이 아니라 명시공식 transfer가
   필요하다.
2. 콜라츠 회전은 하나의 gcd residual을 공유하므로 새 정보는 균일 크기
   부등식 또는 비주기 하강에서 나와야 한다.
3. 골드바흐 cube-root 체 오차는 정확히 세 rough-semiprime convolution이다.
4. 쌍둥이 소수의 cube-root parity contamination은 정확히 `PS+SP+SS`다.

이 결과들은 정확한 부분정리와 경로 폐기다. 리만 가설, 콜라츠 추측,
강한 골드바흐 추측, 무한 쌍둥이 소수 중 어느 것도 증명하지 않았다.

## 문헌 경계

- Connes와 Consani의 [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368)은 semi-local RH 관측량의 배경이다. `(RH-225.1)`은 그들의 RH 판정이 아니다.
- Tao의 [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)는 거의 모든 궤도와 모든 궤도 하강 사이의 남은 간극을 보여준다.
- Ford와 Maynard의 [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368)는 Type-I/Type-II 정보와 parity barrier의 최신 배경을 제공한다.

초등적 꼬리 상계, cyclic gcd 항등식, cube-root rough-semiprime 분류,
convolution 전개에 대해 문헌 우선권을 주장하지 않는다.

## 재현 방법

```powershell
python scripts/ticket225_arithmetic_remainder_localization.py
python -m unittest tests.test_ticket225_arithmetic_remainder_localization -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

주 기계 판독 산출물:

`data/open-problem/ticket225-arithmetic-remainder-localization.json`
