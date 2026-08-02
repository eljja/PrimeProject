# TICKET-183: Abel 전이, 원시 Collatz 단어, Fourier 여유, Haar 경로

## 초록

TICKET-183은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 **증명하거나 반증하지 않았다**. 이번 티켓은 TICKET-182에서 남은
네 보조정리를 다시 다음 네 가지의 정확한 중간 결과로 분해한다.

1. Abel-Fejer-H1 인증에는 정규화 해제 오차가 반드시 포함되어야 한다.
2. 반복된 Collatz valuation word는 원시근으로 정확히 축약되며,
   `v_j >= 2`인 전체 부분족에는 고정점밖에 없다.
3. Fourier major/minor 분해는 점별 양성 여유를 정확히 주지만, 상수 밀도
   희소 모델은 Parseval 항등식 때문에 구조적으로 실패한다.
4. 가중 Haar 에너지는 잎 분산과 정확히 같지만, 모든 잎의 양성에는 전역
   평균이 아니라 경로별 음의 square function 제어가 필요하다.

각 절은 정확한 명제, 증명, 재현 가능한 유한 계산, 폐기할 추론, 다음 단일
보조정리를 구분한다. 네 문제의 해결 개수는 여전히 0이다.

## 결과 요약

| 문제 | 이번에 확정한 결과 | 폐기한 경로 | 다음 핵심 보조정리 |
|---|---|---|---|
| 리만 | Abel-Fejer-H1-정규화 해제 결합 상계 | 정규화 해제 없이 작은 평활 H1만 사용 | `PoleNeutralWeilTestConeHasUniformAbelDesmoothingModulus` |
| 콜라츠 | 반복 word 원시근 축약과 `v>=2` 부분족 완전 배제 | 반복 word 중복 계산과 고정 탐색 길이 | `NoPrimitiveContractingValuationWordContainingOneSatisfiesAffineDivisibility` |
| 골드바흐 | 정확한 Fourier 오차 항등식과 양성 여유 | 상수 소수 밀도와 절댓값 spectral 예산 | `GoldbachMajorMinorPhaseErrorIsUniformlyBelowSingularSeriesMargin` |
| 쌍둥이 소수 | 가중 Haar 분산 항등식과 경로 square 인증 | 전역 Haar 에너지로 모든 경로 제어 | `PrimePairNegativeHaarPathSquareStaysBelowRootMargin` |

## 1. 리만 가설

### 선언 명제

절대 합이 가능한 주기 Fourier 급수

```text
f(theta) = sum_k a_k exp(i k theta)
```

를 생각하자. `0<rho<1`에 대해 Abel 평활화 `A_rho f`의 계수는
`rho^|k| a_k`이다. 다음 두 값을 정의한다.

```text
D_rho^2 = sum_k k^2 rho^(2|k|) |a_k|^2,
R_rho   = sum_k |1-rho^|k|| |a_k|.
```

그러면 Fejer 평균 `sigma_N`에 대해

```text
||f||_infinity
  <= ||sigma_N A_rho f||_infinity + C_N D_rho + R_rho,

C_N^2 = 2 ((N-1)/N^2 + sum_(k>=N) 1/k^2).
```

마지막 항 `R_rho`, 즉 평활화를 되돌리는 오차는 제거할 수 없다. 고정된
`rho<1`, `N<M`에 대해 `f_M(theta)=cos(M theta)`로 두면 평활화된 저주파
항은 0이고 H1 꼬리도 0으로 수렴하지만, 원래 함수의 균등노름은 항상 1이다.

### 증명

다음과 같이 세 항으로 나눈다.

```text
f = (f-A_rho f) + (A_rho f-sigma_N A_rho f) + sigma_N A_rho f.
```

삼각부등식과 계수의 절대 합으로 첫 항은 `R_rho` 이하이다. Parseval
항등식과 TICKET-182의 Fejer multiplier 상계로 둘째 항은 `C_N D_rho`
이하이다. 이것으로 전체 상계가 증명된다.

반례 함수의 Abel 감쇠율은 `rho^M`, 정규화된 도함수 L2 노름은
`M rho^M/sqrt(2)`이다. 이는 0으로 가지만 평활화 해제 오차
`1-rho^M`은 1로 간다.

### 계산 결과와 한계

`rho=0.9`, `N=16`에서:

| M | 평활 H1만 쓴 상계 | 평활화 해제 오차 | 전체 상계 |
|---:|---:|---:|---:|
| 32 | 0.385494 | 0.965663 | 1.351157 |
| 64 | 0.026473 | 0.998821 | 1.025294 |
| 128 | 0.000062 | 0.999999 | 1.000061 |
| 256 | `1.74e-10` | 거의 1 | 1.0000000002 |

`Lambda(n)/sqrt(n)` cosine 계수를 사용한 유한 소수 proxy는 고정된 `rho`에서
H1 에너지가 유한하다. 그러나 cutoff 100,000에서 평활화 해제 `l1` 오차가
614보다 크다. 더 중요하게, 이 proxy는 극점을 제거한 실제 Weil 기호가
아니다.

Weil 양성 조건에는 제약된 시험함수와 moment 조건이 필요하다. Connes와
Consani의 정식화도 두 moment 조건을 명시적으로 유지한다
([The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368)). 따라서 이번
반례가 폐기하는 것은 Abel 평활화가 아니라 **정규화 해제 없는 평활화 승격**이다.

**다음 보조정리:**
`PoleNeutralWeilTestConeHasUniformAbelDesmoothingModulus`.

## 2. 콜라츠 추측

### 선언 명제

valuation word `u=(v_0,...,v_(h-1))`에 대해

```text
F_u(n) = (3^h n+B(u))/2^S,
S=sum_j v_j,
D(u)=2^S-3^h
```

로 두자. `w=u^r`가 `u`를 `r`번 반복한 word이면 동일한 양의 정수
`Q_r`에 대해

```text
D(w)=D(u)Q_r,    B(w)=B(u)Q_r.
```

따라서 `D(w)|B(w)`와 `D(u)|B(u)`는 동치이다. 또한 양의 가속 Collatz
순환에서 모든 `v_j>=2`이면 그 순환은 `n=1` 고정점이고 word는
`(2,...,2)`이다.

### 증명

`a=3^h`, `b=B(u)`, `c=2^S`로 쓰면 `F_u(n)=(an+b)/c`이다. 이를 `r`번
합성하면

```text
F_u^r(n)
 = (a^r n+b sum_(j=0)^(r-1) a^(r-1-j)c^j)/c^r.
```

동일한 기하급수 합이 `c^r-a^r`도 인수분해하므로 두 나눗셈 조건이
동치이다.

모든 `v>=2`이면 홀수 `n>1`에서

```text
(3n+1)/2^v <= (3n+1)/4 < n.
```

따라서 매 단계 엄격히 감소하므로 순환할 수 없다. `n=1`에서는
`3n+1=4`이므로 정확한 valuation은 2이고 고정된다.

### 계산 결과와 한계

- valuation `1,...,5`, 길이 8까지 488,280개 word를 분류했다.
- `v_j>=2`인 word 87,380개에서 비고정 divisibility hit는 0개였다.
- 원시·수축·`v=1` 포함 조건에 해당하는 검사 word는 399,524개였다.
- 반복 인수분해는 `(2)`, `(1,2,3)`, `(1,2,2)`에서 정확히 일치했다.

그러나 고정 길이 탐색은 완결될 수 없다. 모든 `h>=3`에 대해

```text
w_h=(1,2,...,2),   S=2h-1
```

는 원시 word이고 `2^S>3^h`인 수축 후보이다. 이 가족은 길이 32까지
예시로 생성했으며 임의로 계속된다. 이것은 순환 반례가 아니다.
`D(w_h)|B(w_h)`가 증명되지 않았기 때문이다.

Tao의 결과는 로그 밀도 의미의 거의 모든 궤도에 관한 정리이므로 이 남은
모든 원시 word를 배제하지 않는다
([Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)).

**다음 보조정리:**
`NoPrimitiveContractingValuationWordContainingOneSatisfiesAffineDivisibility`.

## 3. 강한 골드바흐 추측

### 선언 명제

유한 순환군 `Z/LZ`에서 정규화된 합성곱을 사용하고 `f=g+h`로 분해하자.
그러면

```text
f*f = g*g+E,
E_hat(k)=2 g_hat(k)h_hat(k)+h_hat(k)^2.
```

따라서

```text
min_x (g*g)(x)
 > sum_k |2 g_hat(k)h_hat(k)+h_hat(k)^2|
```

이면 모든 목표점에서 `f*f>0`이다.

밀도 `alpha`인 지시함수에 상수 모델 `g=alpha`를 사용하면 Parseval에 의해
오차 예산은 정확히 `alpha(1-alpha)`이고 모델 여유는 `alpha^2`이다.
그러므로 `alpha<=1/2`에서는 이 방식이 통과할 수 없다.

### 증명

합성곱 정리로 오차 Fourier 계수를 얻고, Fourier 역변환에 삼각부등식을
적용하면 모든 목표점의 오차가 계수 절댓값 합보다 작다. 상수 모델에서는
잔차 평균이 0이므로 교차항이 사라진다. Parseval 항등식

```text
sum_(k!=0)|h_hat(k)|^2=alpha(1-alpha)
```

이 희소 상수 모델의 실패를 정확히 증명한다.

### 계산 결과와 한계

길이 32, 64, 128인 유한 모형 세 개는 Fourier 항등식 오차
`1e-10` 이하로 양성 인증을 통과했다. 반면 순환 odd-prime 지시함수는:

| L | 밀도 | 상수 모델 여유 | Parseval 예산 | 예산/여유 |
|---:|---:|---:|---:|---:|
| 64 | 0.468750 | 0.219727 | 0.249023 | 1.1333 |
| 128 | 0.414063 | 0.171448 | 0.242615 | 1.4151 |
| 256 | 0.375000 | 0.140625 | 0.234375 | 1.6667 |
| 512 | 0.333984 | 0.111546 | 0.222439 | 1.9942 |

유한 정수 검사에서는 `6<=n<=50,000`인 모든 짝수에 대해 홀수 소수 표현을
찾았고 최소 표현 개수는 1이었다. 제외한 4는 별도로 `2+2`이다. 이 계산은
유한 검증이며 무한 명제를 증명하지 않는다.

이번 no-go는 상수 밀도와 위상을 버린 절댓값 예산만 폐기한다. 실제로 필요한
것은 singular series(특이급수) major term과 목표별 부호 상쇄이다. 최신
exceptional-set 연구도 major arc 공식과 모든 목표의 제어를 구분한다
([Grimmelt와 Bhowmik, 2026](https://arxiv.org/abs/2607.27282)).

**다음 보조정리:**
`GoldbachMajorMinorPhaseErrorIsUniformlyBelowSingularSeriesMargin`.

## 4. 쌍둥이 소수 추측

### 선언 명제

양의 질량 `m_i`와 비율 `r_i`를 가진 dyadic 잎을 생각하자. 부모 비율은
두 자식의 질량 가중 평균이다. 그러면

```text
sum_i m_i(r_i-r_root)^2
 = sum_(internal I) [m_L m_R/(m_L+m_R)](r_L-r_R)^2.
```

깊이 `d`인 한 경로에서

```text
Q_minus=sum_j min(r_child(j)-r_parent(j),0)^2
```

로 두면

```text
r_leaf >= r_root-sqrt(d Q_minus).
```

오른쪽이 양수이면 그 잎의 양성이 인증된다.

### 증명

첫 식은 두 자식에 대한 가중 전체분산 법칙을 트리 전체에 재귀 적용한
항등식이다. 둘째 식은 경로 증가량을 망원합한 뒤 음의 증가량에
Cauchy-Schwarz 부등식을 적용하면 얻는다.

전역 Haar 에너지만으로는 충분하지 않다. `2^d-1`개 잎의 비율을 1, 한
잎을 0, 모든 질량을 `2^(-d)`로 두면

```text
전역 Haar 에너지=(2^d-1)/2^(2d) -> 0
```

이지만 선택한 잎은 계속 0이고 음의 경로 square는 `1/3`으로 간다.

### 계산 결과와 한계

깊이 16에서 전역 에너지는 약 `1.53e-5`까지 감소하지만 나쁜 잎은 0이다.
실제 `[100000,362144)` 구간을 폭 1,024인 256개 잎으로 나누고
Hardy-Littlewood 기대 질량으로 정규화한 결과는 다음과 같다.

| 양 | 값 |
|---|---:|
| 실제 쌍둥이 소수쌍 | 2,298 |
| root 실제/기대 비율 | 1.000378 |
| 가중 잎 분산 | 0.078545 |
| Haar 에너지 합 | 0.078545 |
| 항등식 오차 | `2.78e-17` |
| 최대 음의 경로 square | 0.357149 |
| 최소 실제 잎 비율 | 0.119937 |
| 최소 인증 하한 | -0.689945 |

이 유한 구간의 모든 잎은 실제로 양수지만 경로 인증은 실패한다. 어느 쪽도
미래 블록의 하한이 아니다. Maynard의 정리·개관도 bounded gap 진전과
정확한 간격 2 명제를 구분한다
([On the Twin Prime Conjecture](https://arxiv.org/abs/1910.14674)).

**다음 보조정리:**
`PrimePairNegativeHaarPathSquareStaysBelowRootMargin`.

## 공통 결론

네 no-go의 공통 논리 구조는 다음과 같다.

```text
평활화되거나 평균화된 제어
  + 빠진 균등 전이항
  != 점별 산술 결론
```

TICKET-183은 각 표현에서 빠진 전이항이 무엇인지를 정확히 지정했다. 실제
산술 객체가 그 균등 상계를 만족한다는 정리는 아직 없다.

## 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket183_abel_primitive_spectral_haar.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket183_abel_primitive_spectral_haar -v
```

기계 판독 산출물은
`data/open-problem/ticket183-abel-primitive-spectral-haar.json`이다.
