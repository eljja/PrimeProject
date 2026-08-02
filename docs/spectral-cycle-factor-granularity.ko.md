# TICKET-185: 스펙트럼 이탈, 순환 배제, 인수 지평, 정수 해상도

## 초록

TICKET-185는 TICKET-184의 네 열린 노드를 이어간다. 이 문서는 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측을 **증명하거나 반증하지
않는다**. 대신 정확한 중간 정리 네 개를 증명하고, 콜라츠 경로에서 과거에
이미 확인한 동치 명제를 다시 작은 보조정리처럼 올린 논리적 후퇴를 수정한다.

| 문제 | 정확한 새 결과 | 상태 |
|---|---|---|
| 리만 가설 | `TwoNeutralMomentAutocorrelationSpectralEscapeNoGo` | 명시 모형의 정확한 no-go, RH 미해결 |
| 콜라츠 | `SingleValuationOneOtherwiseTwoCycleExclusion` | 무한 순환 부분족 하나 배제, 추측 미해결 |
| 골드바흐 | `TargetSpecificGoldbachFactorHorizonEquivalence` | 유한 목표별 정확한 임계값, 추측 미해결 |
| 쌍둥이 소수 | `IntegerGranularityAndOneSidedBlockCertificate` | 인증 조건의 정확한 교정, 추측 미해결 |

여기서 “새 결과”는 PrimeProject 내부에서 새로 확정했다는 뜻이다. 독립적인
전문가 검토 전에는 학계 최초나 문헌상 우선권을 주장하지 않는다. 아래 유한
계산은 표시한 항등식과 제한된 데이터만 검사하며 무한 명제의 증거로 승격하지
않는다.

## 1. 재현 계약

```powershell
D:\python\anaconda3\python.exe scripts\ticket185_spectral_cycle_factor_granularity.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket185_spectral_cycle_factor_granularity -v
```

기계 판독 기준 산출물:

`data/open-problem/ticket185-spectral-cycle-factor-granularity.json`

예상되는 기계 원장:

```json
{
  "exact_theorem_count": 4,
  "rejected_target_count": 4,
  "proof_dag_count": 4,
  "finite_arithmetic_diagnostic_count": 4,
  "decisive_route_correction_count": 3,
  "conjecture_resolution_count": 0,
  "total_failure_count": 0
}
```

## 2. 리만 가설

### 2.1 선언 명제

다음과 같이 명시한 로그 좌표 자기상관 모형을 사용한다. `A>0`을 고정하고
`g in L2([-A,A])`에 두 중립 선형 조건을 부과한다.

```text
integral g(x)e^(x/2) dx  = 0,
integral g(x)e^(-x/2) dx = 0.
```

다음을 만족하는 정규화된 양의 정부호 자기상관 함수열이 존재한다.

```text
F_M = g_M * tilde(g_M),   F_M(0)=1.
```

각 `F_M`은 콤팩트 지지를 갖지만 그 푸리에 확률 측도는 모든 고정된 유계
주파수 구간 밖으로 이탈한다. 따라서 콤팩트 지지, 양의 정부호성, 정규화,
위 두 중립 모멘트만으로는 균일한 푸리에 꼬리 긴밀성을 얻을 수 없다.

### 2.2 증명

```text
h_M(x) = 1_[-A,A](x) cos(Mx)
```

로 두고, `P`를 `span{e^(x/2),e^(-x/2)}` 위 직교사영이라 하자.

```text
g_M = (I-P)h_M.
```

두 중립 모멘트는 구성상 정확히 0이다. Riemann-Lebesgue 보조정리에 의해
사영 계수는 0으로 가지만

```text
||h_M||_2^2 = A + sin(2MA)/(2M)
```

은 0에서 떨어져 있다. 정규화된 자기상관은 양의 정부호이고 지지는
`[-2A,2A]`에 들어간다. 푸리에 밀도는

```text
|hat(g_M)(xi)|^2 / ||g_M||_2^2
```

이다. 코사인의 두 sideband는 `+M`, `-M`으로 이동하고, 0으로 가는 사영
보정은 고정 주파수 구간에 양의 질량을 남길 수 없다. 따라서 스펙트럼 이탈이
성립한다.

### 2.3 재현 계산

`A=1`, 고정 구간 `[-4,4]`에서 `M=8,16,32,64`를 계산했다. `M=64`의
정규화된 저주파 질량은 `0.0005611473`, 구간 밖 질량은
`0.9994388527`이다. 모든 경우 두 중립 잔차는 `1e-12`보다 작다.

수치 적분은 이탈 속도를 표시할 뿐이다. 스펙트럼 이탈 자체는 위 해석적
논증으로 증명한다.

### 2.4 폐기 경로와 남은 간극

다음을 폐기한다.

- 콤팩트 지지, 양의 정부호성, 정규화, 두 중립 모멘트만으로 균일 꼬리
  콤팩트성을 얻는 경로
- 자기상관 대리 모형을 실제 Weil 이차형식과 동일시하는 경로

이 반례군이 모든 기술적 Weil test cone 구현에 실제로 포함된다고 주장하지
않는다. 다만 TICKET-184의 균일 꼬리 경로에는 단순한 콤팩트성 주장이 아니라
추가적인 coercivity, 즉 강제 하한 전제가 필요함을 보인다.

**다음 단일 보조정리:**
`WeilQuadraticFormCoercivityModuloSpectralTranslationsOnExplicitPoleNeutralCore`.

실제 산술 이차형식을 평가하고 spectral translation을 몫공간으로 제거하거나
직접 제어해야 한다. Connes-Consani가 검토한 Weil 양성 시도의 실패는 연구
경계이지 빠진 전제가 아니다
([The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368)).

## 3. 콜라츠 추측

### 3.1 선언 명제

가속 콜라츠 양의 순환 중 valuation `1`이 정확히 한 번 나타나고 나머지가
모두 `2`인 primitive 주기는 존재하지 않는다. 순환 이동을 하면 모든 단어는

```text
w_h = (1,2,...,2),  h>=3
```

가 된다. 이 단어는 기울기상 수축하지만 affine 분자와 순환 분모가 서로소다.

### 3.2 증명

첫 valuation-one 단계 뒤에 `x -> (3x+1)/4`를 `h-1`번 반복하면

```text
B_h = 2*4^(h-1) - 3^(h-1),
D_h = 2*4^(h-1) - 3^h.
```

따라서

```text
B_h-D_h = 2*3^(h-1).
```

`D_h`는 홀수이며 modulo 3에서 2이다. 그러므로

```text
gcd(D_h,2*3^(h-1))=1,
gcd(B_h,D_h)=1.
```

`h>=3`이면 `D_h>=5`이므로 `D_h`는 `B_h`를 나눌 수 없다. 정확한 affine
나눗셈은 양의 순환의 필요조건이므로 이 무한 부분족 전체가 배제된다.

### 3.3 계산과 경로 교정

닫힌식을 `h=3,4,8,16,32,64,128`에서 큰 정수로 재생했다. 마지막 분모는
255비트이고 모든 최대공약수는 1이며 나눗셈 적중은 0이다. 그러나 정리는 이
유한 표 때문이 아니라 모든 `h>=3`에 대한 위 식으로 성립한다.

TICKET-184는 다음 문장을 후속 보조정리로 제안했다.

```text
EveryPositiveOddIntegerAboveOneHasAnAcceleratedIterateBelowItsStart
```

TICKET-172는 이미 강한 귀납법으로 이 문장이 콜라츠 추측과 동치임을 증명했다.
따라서 더 작은 보조정리가 아니다. TICKET-185는 원 추측을 다른 이름으로 숨기지
않고 엄밀한 부분 목표로 되돌린다.

valuation `1`이 둘 이상인 단어, valuation `3` 이상을 포함한 단어, 발산 궤도
분기는 여전히 열려 있다. 최근의 exponent-code 연구도 유한 계산을 콜라츠
증명으로 주장하지 않는다
([Kramer, 2026](https://arxiv.org/abs/2607.10041)).

**다음 단일 보조정리:**
`NoPrimitiveContractingValuationWordWithExactlyTwoOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility`.

## 4. 강한 골드바흐 추측

### 4.1 선언 명제

짝수 `N>=6`에 대해 다음 순서 없는 홀수 후보쌍을 본다.

```text
a+(N-a)=N,  3<=a<=N/2.
```

`P^-(m)`을 `m`의 최소소인수라 하자. prime-prime이 아닌 각 쌍의 제거 gate를

```text
gamma_N(a)=min(P^-(a),P^-(N-a))
```

로 두고, 모든 나쁜 쌍에 대한 최대값을 `tau_N`이라 하자. 나쁜 쌍이 없으면
`tau_N=0`으로 정의한다. `y>=0`에서 양쪽 수를 `y` 이하의 모든 소수로
체질했을 때 생존쌍이 모두 prime-prime일 필요충분조건은

```text
y>=tau_N
```

이다.

### 4.2 증명

후보쌍이 깊이 `y`에서 살아남을 필요충분조건은 양쪽 최소소인수가 모두
`y`보다 큰 것이다. 나쁜 쌍은 `y`가 자신의 제거 gate에 도달할 때 정확히
제거된다. gate의 최대값을 취하면 양방향이 즉시 성립한다. 나쁜 쌍이 있으면
`tau_N-1`에서 최대 gate를 갖는 쌍이 살아 있고 `tau_N`에서 모두 제거된다.
나쁜 쌍이 없으면 `tau_N=0` 관례로 동치가 즉시 성립한다.

나쁜 쌍에는 합성수 endpoint가 적어도 하나 있다. 그 최소소인수는 해당 수의
제곱근 이하이다. 다른 endpoint가 작은 소수라면 최소값은 더 작아진다. 따라서
`tau_N`은 제곱근 스케일 이하이다.

### 4.3 유한 지평 감사

| `N` | `tau_N` | `tau_N/sqrt(N)` | `tau_N`에서 남은 소수쌍 |
|---:|---:|---:|---:|
| 100 | 7 | 0.700 | 5 |
| 500 | 19 | 0.850 | 12 |
| 1,000 | 29 | 0.917 | 24 |
| 5,000 | 67 | 0.948 | 71 |
| 10,000 | 89 | 0.890 | 125 |
| 50,000 | 223 | 0.997 | 440 |

모든 감사 목표에서 지평 직전에는 나쁜 생존쌍이 존재하고, 정확한 지평에서는
나쁜 생존쌍이 0이다. 이는 제한된 목표의 정확한 계산이며 `tau_N`의 점근
정리가 아니다.

### 4.4 폐기 경로와 남은 간극

wheel이 `tau_N`에 도달하면 해당 목표에 대해 최소소인수 판정기가 된다. 검증에는
유용하지만 거의 `sqrt(N)`까지 trial division을 수행하는 것은 골드바흐의
해석적 설명이 아니다. 필요한 것은 이 지평 **이전**에 나쁜 생존쌍의 부호 있는
상쇄를 증명하는 것이다.

**다음 단일 보조정리:**
`SubHorizonPrimeWeightedBadSurvivorCancellationBelowTargetMargin`.

최근 exceptional-set 연구도 major arc의 명시식과 모든 목표에 대한 binary
정리를 구분한다
([Grimmelt-Bhowmik, 2026](https://arxiv.org/abs/2607.27282)).

## 5. 쌍둥이 소수 추측

### 5.1 선언 명제

유한 블록의 실제 개수 `C`를 0 이상의 정수, 제안된 주항을 `M>0`, 나머지를
`R=C-M`이라 하자. 그러면

```text
|R|<M  iff  0<C<2M,
R>-M   iff  C>0.
```

따라서 대칭 절대 나머지 지배는 양의 블록 질량보다 엄격하다. 특히 `M<=1/2`
이면 어떤 정수 개수도 절대 인증을 통과할 수 없다.

### 5.2 증명

절대부등식을 전개하면

```text
-M<C-M<M,
0<C<2M
```

이다. 단측 부등식은 바로 `C>0`이 된다. `M<=1/2`이면 열린 구간 `(0,2M)`에
양의 정수가 없다. 이는 확률 모형과 무관한 정확한 정수 해상도 장벽이다.

### 5.3 유한 블록 감사

실제 twin start를 `[100000,362144)`에서 개수를 보기 전에 정한 폭으로
분할했다.

| 폭 | 양의 블록 | 절대 인증 | 양수지만 절대 인증 실패 |
|---:|---:|---:|---:|
| 16 | 2,246 | 0 | 2,246 |
| 32 | 2,122 | 0 | 2,122 |
| 64 | 1,876 | 1,498 | 378 |
| 128 | 1,461 | 1,288 | 173 |
| 256 | 940 | 891 | 49 |
| 512 | 508 | 501 | 7 |
| 1,024 | 256 | 256 | 0 |

모든 폭을 합쳐 양의 블록 `4,975`개가 대칭 인증에는 실패한다. 기대질량이
1/2 이하인 모든 블록의 절대 인증 통과 수는 정확히 0이다. 이 표는 인증기의
해상도를 측정할 뿐 미래 블록을 예측하지 않는다.

### 5.4 경로 교정과 남은 간극

무한히 많은 서로소 블록에서 양의 개수를 얻는 명제는 쌍둥이 소수의 무한성과
동치이지 더 약한 보조정리가 아니다. 대칭 오차 제어는 불필요한 개수 상한까지
추가한다. 실제로 필요한 새 산술 입력은 부호를 보존한 단측 parity 추정이다.

**다음 단일 보조정리:**
`CubicRoughOneSidedJointLiouvilleBlockMarginOnUnboundedScales`.

Ford-Maynard의 일반 소수 생성 하계 체는 상당한 Type I/II 정보가 왜 필요한지
보여준다. PrimeProject는 exact gap 2에 필요한 그 입력을 아직 증명하지 못했다
([On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368)).

## 6. 증명 DAG 요약

```text
RH T184 유한 모멘트 no-go
  -> 두 중립 자기상관의 스펙트럼 이탈 [증명]
  -> spectral translation을 제어한 실제 Weil coercivity [열림]

Collatz T184 순환/발산 분해
  -> 한-개-one/rest-two 무한 순환 부분족 배제 [증명]
  -> 정확히 두-개-one/rest-two affine 나눗셈 배제 [열림]

Goldbach T184 고정 wheel 합성수 모조
  -> 목표별 정확한 인수 지평 [증명]
  -> 지평 이전의 부호 있는 나쁜 생존쌍 상쇄 [열림]

Twin T184 양의 root 충분성
  -> 정수 해상도와 단측 조건 교정 [증명]
  -> 단측 joint Liouville 블록 margin [열림]
```

## 7. 최종 경계

TICKET-185는 콜라츠의 실제 무한 순환 부분족 하나를 닫고, 나머지 세 문제에서
정확한 경로 교정 정리를 증명했다. 제타함수 영점 배제, 모든 콜라츠 시작값의
하강, 모든 짝수의 골드바흐 표현, 무한히 많은 쌍둥이 소수는 증명하지 않았다.
네 상태는 모두 `open_not_proven`이다.
