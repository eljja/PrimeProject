# TICKET-171: 상대 KKT 기하, 콜라츠 유령 경로, 골드바흐 부호 위상, Haar Type II

## 초록

TICKET-171은 TICKET-170의 다음 보조정리 네 개를 더 큰 계산에 넣기 전에
명제 자체부터 검증한다. 이번 라운드에서는 정확한 목표 교정 정리 네 개를
증명했다. 그러나 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측 중 어느 것도 증명하거나 반증하지 않았다.

리만 트랙은 하나의 전역 절대 spectral gap 대신 방향별 크기를 반영하는
상대 KKT 인증 조건을 도입한다. 콜라츠 트랙은 전체 잔여 트리가
well-founded라는 다음 목표가 거짓임을 모든 valuation이 1인 무한 경로로
증명한다. 이 경로의 극한은 양의 자연수가 아니라 2-adic 정수 `-1`이다.
골드바흐 트랙은 Fourier 크기와 모든 dyadic shell 에너지가 같지만 점별
최댓값은 다른 비음수 제곱 신호를 만든다. 쌍둥이 소수 트랙은 Type-II
의존성을 2차원 Haar 좌표로 정확히 옮기고, 어떤 고정 최대 해상도도 다음
스케일 checkerboard를 놓친다는 것을 증명한다.

| 문제 | 이번에 확정한 결과 | 해결 상태 | 폐기한 경로 | 다음 단일 보조정리 |
|---|---|---:|---|---|
| 리만 | 상대 KKT sign-normalization 인증과 비등방 no-go | `open_not_proven` | 전역 최소 gap을 모든 방향의 필수 오차 척도로 요구 | `CofinalRelativeIntervalKKTSignNormalizationBelowOneOnFixedPoleNeutralWeilCore` |
| 콜라츠 | 2-adic 극한 `-1`을 갖는 무한 비하강 all-one 잔여 경로 | `open_not_proven` | 전체 잔여 접두어 트리의 well-foundedness | `NoPositiveNaturalStartSupportsAnInfiniteLeastRealizerNonDescendingResidualRay` |
| 골드바흐 | 동일 shell 에너지에서 발생하는 양의 위상 모호성 | `open_not_proven` | shell 크기/에너지만으로 점별 값을 날카롭게 인증 | `UniformSignedBinaryGoldbachAutocorrelationDualCertificateBelowAnchorMargin` |
| 쌍둥이 소수 | 완전한 Haar 좌표 연결과 고정 깊이 no-go | `open_not_proven` | 고정 dyadic 깊이로 모든 Type-II 의존성을 제어 | `UniformGrowingResolutionHaarTypeIIDecayWithPrimeProducingConstants` |

## 1. 리만 가설

### 선언 명제

실수 대칭 비특이 KKT 행렬 `K`에 대해

```text
J = sign(K),       T = |K|^(-1/2),       F = T E T
```

라고 하자. 그러면

```text
K+E = T^(-1)(J+F)T^(-1)
```

이므로

```text
||F||_2 < 1  =>  inertia(K+E)=inertia(K).                (1)
```

원래 기저에서 구간 오차가 `|E_ij|<=R_ij`로 주어지면

```text
|| |T| R |T|^T ||_F < 1                                 (2)
```

은 계산 가능한 충분조건이다.

### 증명

spectral calculus로 `K=T^(-1)JT^(-1)`를 얻는다. Sylvester 관성 법칙에
따라 `K+E`의 관성은 `J+F`의 관성과 같다. `J`의 모든 고윳값은 `+1` 또는
`-1`이므로 Weyl 부등식에서 `||F||_2<1`이면 어떤 고윳값도 0을 통과할 수
없다. 또한 원소별 삼각부등식으로

```text
|(TET)_ab| <= (|T|R|T|^T)_ab
```

를 얻고, Frobenius 노름은 연산자 노름을 지배하므로 (2)가 충분하다.

### 정확한 no-go

```text
K_n=diag(1/n,n^2,-1),       E_n=diag(0,n^2/2,0)
```

에서는 전역 최소 gap이 `1/n`이고 절대 오차는 `n^2/2`다. 따라서
TICKET-170의 절대 조건은 `n^3/2`배만큼 실패한다. 하지만 상대 오차는
항상 `1/2`이고 관성도 변하지 않는다.

이는 전역 gap 조건이 충분조건이라는 사실을 반박하지 않는다. 그 조건을
모든 비등방 KKT 방향에서 반드시 만족해야 한다고 요구하는 것이 지나치게
강하다는 것만 증명한다. 실제 고정 dense pole-neutral Weil core에서 상대
구간 반지름이 1보다 작다는 cofinal 정리는 아직 없다.

## 2. 콜라츠 추측

### 선언 명제

TICKET-170이 다음 목표로 둔

```text
WellFoundednessOfExactNonDescendingChildTreeAfterAnalyticTailClosure
```

는 거짓이다. `w_m=1^m`에 대해

```text
C_m=3^m-2^m,
n_m=2^(m+1)-1,
u_m=(3^m n_m+C_m)/2^m=2*3^m-1.                (3)
```

모든 `m>=1`에서 `u_m>n_m`이다. valuation 1을 하나 더 붙이면
`w_(m+1)`이 되며

```text
n_(m+1) = n_m  (mod 2^(m+1)).                 (4)
```

따라서 이 노드들은 하나의 무한 호환 비하강 잔여 경로를 이룬다.

### 증명과 의미

`C'=3C+2^m`에 대한 귀납으로 correction 공식을 얻고, 직접 대입하면 (3)이
나온다. `3^m>2^m`이므로 비하강이며, `n_m`의 닫힌식에서 (4)를 바로 얻는다.

이 경로의 residue 조건은

```text
n = -1 (mod 2^(m+1)).                           (5)
```

이고 2-adic 극한은 `-1`이다. 양의 자연수 `n` 하나가 모든 접두어를
실현한다면 `n+1`이 임의로 큰 2의 거듭제곱으로 나누어져야 한다. 거듭제곱이
`n+1`보다 커지면 불가능하다.

즉, 이것은 symbolic 잔여 트리의 실제 무한 경로이지만 자연수 콜라츠 발산
궤도는 아니다. 전체 symbolic 트리의 well-foundedness는 콜라츠 추측이
필요로 하는 것보다 강한 거짓 목표였다.

### 계산과 남은 간극

길이 `1,2,4,8,16,32,64`에서 닫힌식, child 호환성, valuation 1이 분석적
tail threshold 아래에 남는지를 정확한 정수 계산으로 확인했다. `10^6`
이하에서는 가장 큰 all-one 대표가 `524287`이고 접두어 길이는 `18`이다.
이 유한 수치는 설명용일 뿐이며, 무한 명제는 위 divisibility 증명으로
성립한다.

수정된 다음 목표는 양의 자연수 하나와 호환되는 무한 비하강 잔여 경로를
배제하는 것이다. 이 명제는 아직 증명되지 않았고 사실상 first-descent
종결부에 가깝다. 이번 유령 경로는 콜라츠의 증명도 반례도 아니다.

## 3. 강한 골드바흐 추측

### 선언 명제

`Z/4`에서 `0<e<=1/2`일 때

```text
g_+(t)=1+e cos(t)+e cos(2t),
g_-(t)=1+e cos(t)-e cos(2t)
```

를 정의한다. 표본 벡터와 정규화 DFT는 각각

```text
g_+=(1+2e,1-e,1,1-e),       G_+=(1,e/2, e,e/2),
g_-=(1,1+e,1-2e,1+e),       G_-=(1,e/2,-e,e/2).          (6)
```

두 `g`는 모두 비음수이고 모든 주파수에서 `|G_+|=|G_-|`다. 따라서 모든
dyadic shell 에너지도 같다. 그러나

```text
max g_+=1+2e,       max g_-=1+e.                         (7)
```

`e=1/4`에서는 두 최댓값이 정확히 `3/2`, `5/4`다.

### no-go의 범위

이 정리는 TICKET-170의 shellwise Cauchy 상계를 무효화하지 않는다. 그
상계는 가능한 최악의 위상을 취하므로 안전하다. 다만 shell 에너지만으로는
유리한 상쇄를 이용하거나 점별 값을 날카롭게 판정할 수 없음을 보인다.

이 신호들은 prime exponential sum이 아니며 골드바흐 반례도 아니다. 다음
보조정리는 실제 소수 spectrum의 부호 위상을 보존하는 target-uniform
autocorrelation dual 상계를 독립적으로 증명된 major-arc anchor margin 아래로
내려야 한다.

## 4. 쌍둥이 소수 추측

### 선언 명제

중심화 Type-II 행렬 `A`와 직교 Haar 변환 `Q`에 대해 `B=QAQ^T`라 하면

```text
||B||_2=||A||_2,
||B||_F^2=sum_(u,v)|B_uv|^2=||A||_F^2.          (8)
```

`A`의 모든 행과 열의 합이 0이면 `B`의 constant row와 column도 0이다.
따라서 nonconstant Haar coefficient 전체는 같은 Type-II 연산자를 정확히
표현하는 다중해상도 좌표계다.

### 고정 깊이 no-go

어떤 최대 제어 깊이 `J`를 고정해도 다음 스케일의 한 셀 안에

```text
[[ a,-a],
 [-a, a]]                                             (9)
```

를 넣을 수 있다. 모든 세부 행/열 합과 `J` 이하 모든 dyadic block 합은
0이지만, 다음 스케일 Haar 계수와 top singular value는 `2a`다. 따라서 고정
유한 해상도는 완전한 Type-II 제어가 될 수 없다.

### 계산과 남은 간극

TICKET-161의 `X=10^4,10^5,10^6,10^7` 행렬을 직교 `4x4` Haar 기저로
변환했다. constant row/column 소멸, Frobenius 에너지 보존, operator norm
보존을 검증했다. fine-by-fine 에너지 비율은 약
`0.72,0.49,0.08,0.18`로 단조롭지 않다. 이는 유한 진단이지 점근 법칙이
아니다.

Haar 좌표는 필요한 추정의 위치를 정확히 보여주지만 decay 자체를 주지
않는다. 다음 정리는 해상도를 증가시키면서 균일 operator decay와 실제
prime-producing sieve에 충분한 상수를 증명해야 한다. Frobenius 상계에는
차원 손실이 생길 수 있으므로 조용히 대체해서는 안 된다.

## 5. 증명 DAG와 주장 경계

```text
리만: 전역 절대 gap 필수 [반박]
  -> 상대 sign-normalized KKT 인증 [증명]
  -> 실제 고정 Weil core의 cofinal 상대 구간 상계 [미해결]

콜라츠: 전체 잔여 트리 well-founded [반박]
  -> all-one 비하강 2-adic 유령 경로 [증명]
  -> 양의 자연수 호환 무한 잔여 경로 배제 [미해결]

골드바흐: shell 에너지가 점별 deficit 결정 [반박]
  -> 양의 부호 위상 모호성 패밀리 [증명]
  -> anchor 아래의 균일 signed 산술 dual 인증 [미해결]

쌍둥이 소수: 고정 dyadic 깊이가 모든 Type II 제어 [반박]
  -> 정확한 Haar 연결과 다음 스케일 checkerboard [증명]
  -> sieve 상수를 갖는 증가 해상도 decay [미해결]
```

네 terminal node는 모두 `open_not_proven`이다. 유한 계산은 보편적 지름길의
반례를 찾거나 정확한 공식을 검증할 수 있지만 네 무한 추측을 증명하지는
못한다.

## 6. 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket171_relative_ghost_phase_haar.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket171_relative_ghost_phase_haar -v
```

기계 판독 결과는 통합 JSON 하나와 문제별 JSON 네 개에 기록된다.

## 7. 문헌 경계

- [유한 Guinand-Weil 사전과 archimedean tail](https://arxiv.org/abs/2607.02828)은 유한 Weil/구간 인증 맥락을 제공하지만 RH 증명은 제공하지 않는다.
- [콜라츠 수열의 paradoxical behavior](https://arxiv.org/abs/2502.00948)는 유한 parity-word 맥락을 제공하지만 자연수 잔여 경로 배제는 증명하지 않는다.
- [골드바흐 문제의 exceptional set](https://arxiv.org/abs/2607.27282)은 최신 exceptional-set 및 major-arc 맥락을 제공하지만 여기 필요한 signed 인증은 제공하지 않는다.
- [Prime-producing sieve 이론](https://arxiv.org/abs/2407.14368)은 폭넓은 sieve 환경에서 실질적인 Type-II 정보가 필요함을 설명하지만 Haar 항등식만으로 그 추정을 얻을 수는 없다.

위 문헌은 외부 맥락을 정하는 용도다. 여기 사용한 기본 행렬, Fourier,
2-adic, Haar 항등식 자체에 대한 우선권이나 독창성 주장은 하지 않는다.
