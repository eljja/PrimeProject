# TICKET-200: 도함수 mesh, 세 run 쌍 배제, Chen 채널

## 초록

TICKET-200은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 동시에 증명 또는 반증하려는 PrimeProject의 연구를 이어간다. 네
난제 중 해결된 것은 없다. 이번 티켓에서 정확히 확립한 내용은 다음 네
가지다.

1. 도함수 상계가 주어진 유한 경계 격자(mesh)는 경계 전체에 엄밀한
   Rouché 여유를 전달하기에 충분하다.
2. 명시적인 원시 세-run-쌍 콜라츠 무한족은 모든 규모와 모든 순환
   회전에서 affine 나눗셈 조건을 만족하지 않는다.
3. Chen의 명시적 정리를 골드바흐 소수 채널과 합성 반소수 채널로 정확히
   분해하면, 가능한 큰 반례는 반드시 두 번째 채널에만 놓여야 한다.
4. Chen의 `소수 + P2` 무한성도 쌍둥이 소수 채널과 합성 반소수 채널로
   정확히 분리되며, 남은 parity 장벽을 구체적인 명제로 표시할 수 있다.

기계 판독 원본은
[`ticket200-derivative-mesh-three-run-chen-channels.json`](../data/open-problem/ticket200-derivative-mesh-three-run-chen-channels.json)이다.
네 상위 추측의 상태는 모두 `open_not_proven`이며 해결 수는 0이다.

## 주장 요약

| 문제 | TICKET-200의 정확한 결과 | 폐기하거나 제한한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 가설 | `DerivativeControlledBoundaryMeshRoucheCertificate` (도함수 제어 경계 격자 Rouché 인증) | 바깥쪽 반올림 도함수·꼬리 상계 없이 Xi 부동소수점 값만 사용 | `OutwardRoundedXiTaylorRemainderAndDerivativeBoundsInstantiateD3MeshCertificate` |
| 콜라츠 | `ThreeRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales` (세 run 쌍 원시 무한족 전 규모 affine 나눗셈 배제) | 명시적 `r=3` 가족을 양의 주기 후보로 계속 유지 | `FourRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales` |
| 강한 골드바흐 | `ChenGoldbachPrimeSemiprimeChannelReduction` (Chen 골드바흐 소수·반소수 채널 환원) | Chen의 `소수+P2` 양성에서 `소수+소수` 양성을 바로 추론 | `SemiprimeOnlyChenGoldbachChannelIsEmptyForEveryEvenNAboveExp36` |
| 쌍둥이 소수 | `ChenTwinPrimeSemiprimeChannelReduction` (Chen 쌍둥이 소수·반소수 채널 환원) | Chen 소수가 무한하므로 쌍둥이 소수도 무한하다고 동일시 | `TwinChannelPositiveOnInfinitelyManyChenPositiveDyadicBlocks` |

## 1. 리만 트랙: 격자 사이 전달 논리를 닫기

### 명제 RH-200

다음 사각형의 다각형 경계를 생각한다.

```text
D_3^+ = {x+iy : -3 <= x <= 3, 1/3 <= y <= 3}
```

경계를 길이 `h` 이하인 선분으로 나누고 각 선분의 양 끝점을 표본화한다.
닫힌 사각형 근방에서 해석적인 함수 `P`, `R`이 다음을 만족한다고 하자.

```text
모든 격자점 s에서 |P(s)| - |R(s)| >= eta,
경계 전체에서 sup(|P'(z)| + |R'(z)|) <= L,
eta - Lh/2 > 0.
```

그러면 경계 전체에서 `|R(z)|<|P(z)|`이다. 따라서 `P`와 `P+R`은
`D_3^+` 내부에 중복도를 포함해 같은 수의 영점을 갖는다.

### 증명

한 경계 선분의 임의의 점 `z`는 두 끝점 중 하나인 `s`에서 `h/2` 이하
거리에 있다. `s`에서 `z`까지 직선 구간을 따라 도함수를 적분하면

```text
|P(z)-P(s)| + |R(z)-R(s)| <= L|z-s| <= Lh/2.
```

역삼각부등식으로

```text
|P(z)| - |R(z)|
  >= |P(s)| - |R(s)| - |P(z)-P(s)| - |R(z)-R(s)|
  >= eta - Lh/2
  > 0
```

를 얻는다. 이것이 Rouché 정리의 엄격한 경계 조건이므로 결론이 따른다.

### 정확한 회귀 계산

생성기는 같은 `D_3^+` 경계에서 `P(z)=20+z^2`, `R(z)=1/4`인 합성 예제를
사용한다. 이 영역에서 `Re(P)=20+x^2-y^2>=11`이므로 보수적인 정확 여유는
`eta=43/4`이다. 또한 `|P'|=2|z|<=2(|x|+|y|)<=12`이므로 `L=12`이다.
한 변을 네 구간으로 나누면 `h=3/2`이고

```text
eta - Lh/2 = 43/4 - 9 = 7/4 > 0
```

이다. 정확한 유리수 계산은 변당 구간 수 `2, 4, 8, 16`을 검사한다. 첫
격자는 이 인증식에 너무 거칠고 나머지 세 격자는 엄격한 여유를 인증한다.

### 한계

이 결과는 TICKET-199가 요구한 격자 전달 보조정리를 증명했을 뿐 Xi의
영점 없는 사각형을 증명하지 않았다. 계산에 사용한 함수는 Xi가 아니다.
남은 작업은 Xi Taylor 다항식, 나머지, 두 도함수를 모든 경계 선분에서
바깥쪽 반올림 구간으로 포위하는 것이다. 고정밀 부동소수점 표본은 이
포위를 대체하지 못한다.

## 2. 콜라츠 트랙: 명시적인 세-run-쌍 무한족

`k>=2`에 대해 가속 콜라츠 지수 단어를

```text
w_k = 1^k 2^(2k) (1 2^2)^2
```

로 둔다. 이 단어에는 1-run과 2-run이 각각 세 개 있다. 다음 기호를 쓴다.

```text
x=32^k, y=27^k, z=18^k.
```

### 명제 CO-200

모든 `w_k`와 그 모든 순환 회전은 수축 gate와 곱 gate를 통과하지만,
affine 나눗셈 방정식을 만족하지 않는다. 따라서 이 명시적 무한족에는
양의 콜라츠 주기 코드가 없다.

### 닫힌식과 증명

단어 `A`의 순서 의존 affine 분자를 `N(A)`라 하면 이어 붙이기에 대해

```text
N(A || B) = 3^len(B) N(A) + 2^sum(A) N(B)
```

가 성립한다. 이전 단어 `A=1^k2^(2k)`에는 `N(A)=x+y-2z`이고 직접 계산하면
`N((122)^2)=1357`이다. 따라서 분모와 분자는

```text
D = 1024x - 729y,
B = 2086x + 729y - 1458z
```

이다. `k>=7`에서

```text
R = B-2D = 38x + 2187y - 1458z
```

로 두면 `R>0`이다. 한편

```text
D-R = 986x - 2916y + 1458z.
```

이를 `x`로 나눈 식의 전진 차분 부호는

```text
10(27/32)^k - 14(18/32)^k
```

의 부호와 같고 모든 `k>=1`에서 양수다. `k=7`에서는
`D-R=4,268,928,897,556>0`이다. 그러므로 모든 `k>=7`에서 `0<R<D`, 즉
`2D<B<3D`이다. `k=2,...,6`의 정확한 `B mod D` 비영 잔여는 다음과 같다.

```text
126573, 16583324, 362731012, 6001752716, 21418884868
```

따라서 어떤 `k>=2`에서도 `D`가 `B`를 나누지 않는다.

길이가 최소 4인 `2^(2k)` run은 단어 안에서 유일하므로 이 단어는 더 짧은
단어의 거듭제곱일 수 없고 원시적이다. 첫 지수 `v`를 끝으로 이동하는 한
번의 순환 회전에서 분자는

```text
2^v B' = 3B + D
```

를 만족한다. `gcd(6,D)=1`이므로 `D|B`와 `D|B'`는 동치이고, 배제는 모든
순환 회전에 보존된다. 마지막으로 `q=k+2`라 하면 `h=3q`, `S=5q`, 값이
1인 항은 `q`개다. 두 scalar gate는 각각 `32^q>27^q`와
`(125/108)^q>1`로 환원된다.

### 한계

이 정리는 구조화된 `r=3` 가족 하나만 닫는다. 임의의 세-run-쌍 단어,
모든 고정 run 수, 비주기 발산 궤도, 콜라츠 추측 전체는 포함하지 않는다.

## 3. 골드바흐 트랙: 정확한 Chen 채널

`I_P(n)`를 소수 지시함수, `I_2(n)`를 중복도를 포함해 소인수가 정확히 두
개인 합성수의 지시함수로 둔다. 따라서 소수 제곱도 `I_2`에 포함된다.
짝수 `N`에 대해 순서 있는 채널을

```text
R(N) = sum_a I_P(a) I_P(N-a),
S(N) = sum_a I_P(a) I_2(N-a),
C(N) = R(N) + S(N)
```

로 정의한다.

### 명제 GB-200

`C=R+S`는 서로 겹치지 않는 정확한 지지집합 분해다. Bordignon의 명시적
Chen 정리는 모든 짝수 `N>exp(36)`가 소수와 소수 최대 두 개의 곱의 합으로
표현된다고 말한다. 따라서 이 범위에서 `C(N)>0`이다. 그러므로 그 위에
골드바흐 반례가 존재한다면 반드시

```text
R(N)=0 < S(N)
```

이어야 한다. 즉 합성 반소수 채널만 남은 Chen target이어야 한다.

### 증명과 no-go

소수 최대 두 개의 곱은 소수이거나 합성 반소수이며 두 경우는 겹치지
않는다. Chen 표현의 두 번째 항을 이 둘로 나누면 항등식이 성립한다. 외부
정리가 `C(N)>0`을 주므로 `R(N)=0`이면 `S(N)>0`일 수밖에 없다.

그러나 이것은 `R(N)>0`을 증명하지 않는다. 정확한 논리 모형
`R=0, S=1, C=1`은 `C=R+S`와 `C>0`을 모두 만족하지만 `R>0`을 만족하지
않는다. 이것은 잘못된 추론의 반례이며 실제 정수론적 골드바흐 반례가
아니다.

체 회귀 계산은 `2^20` 이하의 짝수 `524,287`개를 모두 검사한다. 이 유한
범위에서 골드바흐 실패, Chen 실패, 반소수 전용 target은 모두 0개다. 이
수치는 구현을 검증할 뿐 유한 상계 밖에서 채널이 비어 있음을 증명하지
않는다.

### 한계

다음 결정적 명제는 모든 짝수 `N>exp(36)`에서 반소수 전용 채널이 비어
있다는 것이다. 수입한 Chen 정리와 이 명제가 결합되면 명시적 경계 위의
강한 골드바흐가 닫히고, 아래쪽은 유한 검증으로 처리할 수 있다.
TICKET-200은 이 명제를 증명하지 않았다.

## 4. 쌍둥이 소수 트랙: 고정 shift에서 같은 parity 채널

이진 블록 `[X,2X)`에 대해

```text
T_0(X) = #{p in [X,2X): p와 p+2가 모두 소수},
S_2(X) = #{p in [X,2X): p는 소수이고 p+2는 합성 반소수},
C_2(X) = T_0(X) + S_2(X)
```

로 둔다.

### 명제 TP-200

`T_0`와 `S_2`의 지지는 겹치지 않는다. Chen 정리에 의해 무한히 많은
이진 블록에서 `C_2(X)>0`이다. TICKET-199의 squarefree-Lambda 검출기는
정확히 `T_0(X)>0`일 때만 양수다. 따라서 남은 쌍둥이 소수 의무는 Chen
양성 자체가 아니라, 무한히 많은 Chen 양성 블록을 합성 반소수 채널이
전부 차지할 수 없음을 증명하는 것이다.

### 증명과 no-go

모든 Chen 소수 `p`에 대해 `p+2`는 소수 또는 합성 반소수이므로 정확한
분해가 성립한다. Chen 소수가 무한하면 위로 무한히 뻗고, 각 이진 블록은
유한하므로 무한히 많은 블록을 만난다. TICKET-199의 비음이 아닌 가중
검출기 지지는 `T_0`와 정확히 같다.

`T_0=0, S_2=1, C_2=1`은 다시 `C_2>0`에서 `T_0>0`을 추론하는 논리의
정확한 반례지만 쌍둥이 소수 추측의 반례는 아니다. 계산은
`[2^10,2^11)`부터 `[2^22,2^23)`까지 13개 블록을 검사한다. 마지막
블록에는 쌍둥이 소수 시작점 `22,643`개와 소수-합성반소수 시작점
`65,808`개가 있다. 유한한 양성 블록은 무한성을 증명하지 않는다.

### 한계

이 환원은 고전적인 체 parity 장벽을 프로젝트의 정확한 검출기 언어로
드러낸다. 장벽을 넘어선 것은 아니다. 다음 보조정리는 무한히 많은 Chen
양성 블록에서 쌍둥이 채널 자체가 양수임을 강제해야 한다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket200_derivative_mesh_three_run_chen_channels.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket200_derivative_mesh_three_run_chen_channels -v
```

생성기는 통합 JSON과 난제별 JSON 네 개를 기록한다. 증명에 쓰인 모든
정수와 유리수 격자 상계가 직렬화되어 있다.

## 문헌 경계

- Dave Platt와 Tim Trudgian의 [The Riemann hypothesis is true up to
  `3*10^12`](https://arxiv.org/abs/2004.09765)는 엄밀한 유한 높이 RH 문맥을
  제공한다. TICKET-200은 새 영점 검증을 하지 않았다.
- Carlos Fernandez와 Santiago Ibanez의 [Christoffel words as extremal
  structures in Collatz dynamics](https://arxiv.org/abs/2607.24844)는 순환
  단어에 관한 2026년 최신 인접 연구의 사전출판본이다. TICKET-200의 가족
  계산은 더 좁으며 문헌 우선권을 주장하지 않는다.
- Matteo Bordignon의 [An explicit version of Chen's
  theorem](https://doi.org/10.1017/S0004972721001301)에서 골드바흐 쪽의
  명시적 `exp(36)` 경계를 가져왔다.
- Jing-Run Chen의 [On the representation of a large even integer as the sum
  of a prime and the product of at most two
  primes](https://doi.org/10.1360/YA1973-16-2-157)에서 `소수+P2` 정리를
  가져왔다.
- Lasse Grimmelt와 Gautami Bhowmik의 [The exceptional set of the Goldbach
  problem](https://arxiv.org/abs/2607.27282)은 exceptional set과 major arc에
  관한 2026년 최신 문맥이다. 이번 증명의 전제로 사용하지 않았다.

격자 전달 명제, 채널 항등식, 논리 반례는 초등적이거나 프로젝트 내부의
결과다. 독립적인 전문가 검토 전에는 학술적 독창성이나 우선권을 주장하지
않는다.

## 최종 경계

TICKET-200은 정확한 부분정리 네 개, 제한되거나 잘못된 추론 네 개, 증명
DAG 네 개, 다음 단일 보조정리 네 개를 기록한다. 완전한 추측을 증명하지
않았고 실제 반례도 찾지 못했다. 얻은 진전은 남은 의무를 더 날카롭게
분리한 것이다. 남은 것은 Xi 구간 포위 하나, 다음 콜라츠 run 가족 하나,
골드바흐 반소수 채널의 점별 배제 하나, 쌍둥이 소수 parity-breaking 채널
정리 하나다.
