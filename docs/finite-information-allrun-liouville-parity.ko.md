# TICKET-201: 유한 정보, 전 반복수 콜라츠, Liouville 패리티

## 초록

TICKET-201은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 동시에 증명하거나 반증하려는 PrimeProject의 다음 반복이다. 네 문제
중 어느 것도 해결됐다고 주장하지 않는다. 이번 작업의 핵심은 TICKET-200이
남긴 다음 보조정리가 실제로 원문제보다 작은지 검증하는 것이다. 다음 네
가지 부분정리를 정확히 증명했다.

1. 하나의 콤팩트 영역에서 얻은 유한 차수 jet 정보만으로는 실수-짝 entire
   함수 전체에서 모든 영점이 실수라는 전역 성질을 강제할 수 없다.
2. 하나의 명시적 2-매개변수 콜라츠 단어족은 모든 규모, 모든 run-pair 수,
   모든 순환 회전에서 affine 나눗셈 조건에 실패한다.
3. 골드바흐의 소수/합성 반소수 채널은 Liouville 부호로 정확히 분해되며,
   TICKET-200의 반소수 채널 제거 목표는 Chen 채널이 양수인 곳에서
   골드바흐 명제와 동치다.
4. 쌍둥이 소수의 dyadic 채널도 같은 항등식을 가지므로 TICKET-200의 다음
   목표는 보조정리가 아니라 쌍둥이 소수 추측의 재표현이다.

기계 판독 결과는
[`ticket201-finite-information-allrun-liouville-parity.json`](../data/open-problem/ticket201-finite-information-allrun-liouville-parity.json)에
있다. 네 상태는 모두 `open_not_proven`이며 해결된 난제 수는 0이다.

## 결과표

| 문제 | 이번에 확정한 결과 | 폐기하거나 제한한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 가설 | `FiniteCompactJetDataCannotForceGlobalRealZeroProperty` (유한 콤팩트 jet 정보의 전역 실수영점 강제 불가능) | 고정된 Xi 콤팩트 인증 하나로 RH를 연결 | `CofinalXiRectangleRoucheMarginFromCompletedZetaStructure` |
| 콜라츠 | `AllRunPairPrimitiveFamilyAffineDivisibilityObstruction` (전 run-pair 원시 단어족 affine 나눗셈 배제) | 반복수를 하나씩 늘리는 계산 | `UniformBoundedL1NeighborhoodAffineObstructionAtOneThirdDensity` |
| 강한 골드바흐 | `GoldbachP2LiouvilleParitySaturationEquivalence` (P2 Liouville 패리티 포화 동치) | 반소수 전용 Chen 채널 제거를 더 쉬운 보조정리로 간주 | `UniformRelativeLiouvilleParityDefectOnPrimePlusP2GoldbachChannels` |
| 쌍둥이 소수 | `TwinP2LiouvilleParitySaturationEquivalence` (dyadic P2 Liouville 패리티 포화 동치) | 무한히 많은 twin-positive Chen 블록을 더 쉬운 보조정리로 간주 | `UniformRelativeLiouvilleParityDefectOnInfinitelyManyChenDyadicBlocks` |

## 1. 리만 트랙: 유한 정보 no-go 정리

`F`를 실수 계수의 짝 entire 함수라 하자. `R>0`, 유한 미분 차수 `M`,
`epsilon>0`, 그리고 `A>R`, `F(iA) != 0`을 고정한다. 다음을 정의한다.

```text
G_N(z) = F(z) - F(iA) z^(2N) / (iA)^(2N)
```

### 명제 RH-201

충분히 큰 모든 `N`에 대해 `G_N`은 실수-짝 entire 함수이고 `+iA`, `-iA`에
비실수 영점을 가지며 다음을 만족한다.

```text
max_{|z|<=R, 0<=j<=M} |G_N^(j)(z)-F^(j)(z)| < epsilon
```

`F(iA)`는 실수이고 perturbation 계수도 실수다. `iA`를 대입하면 영점이
생기고 짝대칭으로 `-iA`도 영점이다. 한편

```text
|G_N^(j)-F^(j)| <= |F(iA)|(2N)_j R^(2N-j)/A^(2N)
```

이며 고정된 `j`에 대해 우변은 `(R/A)^(2N)` 때문에 0으로 간다. 유한한
`j=0,...,M`에 최댓값을 취해도 동일하다.

특히 `F` 자체의 모든 영점이 실수일 때도 이 구성은 유한 jet 정보로는
임의로 가까우면서 지정된 비실수 영점을 갖는 함수를 만든다. 이 결론이
공허하지 않도록 정확 회귀는 영점이 `-1`, `1`뿐인 `F(z)=z^2-1`, `R=5`,
`A=10`, `M=2`, `epsilon=1/100`을 사용한다. 최초 성공값은 `N=9`이고 세
상계는 `101/262144`, `909/655360`, `15453/3276800`이다.

이것은 RH의 반례가 아니다. 새 함수는 실수-짝 대칭과 entire 차수는
보존하지만 Xi의 gamma factor, Dirichlet 급수, Euler product 기원은 보존하지
않는다. 정확한 결론은 고정된 `D3`의 유한 jet 인증만으로 전역 RH를 도출할
수 없다는 것이다. 이후에는 높이가 무한히 증가하는 cofinal 인증과 완성
제타함수의 전역 산술 구조가 필요하다.

## 2. 콜라츠 트랙: 모든 반복수를 하나의 항등식으로 처리

`r>=2`, `k>=2`에 대해 가속 콜라츠 지수 단어를 정의한다.

```text
w_(r,k) = 1^k 2^(2k) (1 2^2)^(r-1)
```

`n=r-1`, `q=k+n`, `x=32^k`, `y=27^k`, `z=18^k`라 두자.

### 명제 CO-201

모든 `w_(r,k)`와 모든 순환 회전은 두 scalar gate를 통과하지만 affine
나눗셈 방정식에는 실패한다. 따라서 이 2-매개변수 무한 단어족에는 양의
콜라츠 순환 코드가 없다.

꼬리 블록 `U=(1,2,2)`에 대해 연결 공식을 정확히 계산하면

```text
N(U^n) = 23(32^n-27^n)/5,
D       = 32^(n+k)-27^(n+k),
B       = ((23*32^n-18*27^n)/5)x + 27^n y - 2*27^n z.
```

그리고 핵심 항등식은

```text
5B-23D = 2*27^n E_k,
E_k    = 14*27^k-9*32^k-5*18^k = -F_k.
```

`F_2=630>0`이다. `k>=3`에서는
`14(27/32)^k<14(27/32)^3<9`이므로 `F_k>0`이다. 또한

```text
32^(k+1)-27^(k+1)-F_k
 = 23*32^k-13*27^k-5*18^k > 0,
```

따라서 `0<F_k<D`이다. `gcd(D,2*27^n)=1`이므로 `D|B`라면 핵심
항등식에서 `D|E_k`가 되어 모순이다. 유일하게 긴 `2^(2k)` run은 단어가
원시적임을 보이며 `2^v B'=3B+D`는 모든 순환 회전에서 배제가 유지됨을
보인다. `h=3q`, `S=5q`이므로 scalar gate도 `32/27`, `125/108`의 양의
거듭제곱으로 통과한다.

계산 회귀는 `2<=r,k<=16`의 225개 단어와 모든 회전을 확인해 실패 0을
얻었다. 유한 격자가 무한 범위를 증명하는 것이 아니라 위 항등식과 부등식이
무한 범위를 증명한다.

한계는 임의 지수 단어를 다루지 못한다는 것이다. 다음 목표는 같은 `h=3q`,
`S=5q`를 가진 원시 단어 중 이 단어족의 고정된 `L1` 근방까지 배제를
확장하는 것이다.

## 3. 골드바흐 트랙: Liouville 포화의 정확한 의미

`J(n)`을 소수 또는 합성 반소수의 지시함수, `lambda(n)=(-1)^Omega(n)`라
하자. `J`의 지지집합에서

```text
I_prime(n)     = J(n)(1-lambda(n))/2,
I_semiprime(n) = J(n)(1+lambda(n))/2.
```

짝수 `N`에 대해 첫 항을 소수 `p`로 합산하고

```text
C(N) = sum_p J(N-p),
L(N) = sum_p J(N-p)lambda(N-p)
```

라 하면 다음 항등식이 성립한다.

```text
R(N) = (C(N)-L(N))/2,
S(N) = (C(N)+L(N))/2.
```

따라서 `C(N)>0`인 곳에서 반소수 전용 포화는 `L=C`와 동치이고,
골드바흐 양성은 `L<C`와 동치다. 즉 TICKET-200의 “모든 반소수 전용 Chen
채널 제거”는 해당 입력에서 골드바흐 자체이지 더 작은 보조정리가 아니다.

16개 표본을 `2^20`까지 정확히 계산했다. `N=2^20`에서 `R=8478`,
`S=22602`, `C=31080`, `L=14124`이고 `C-L=2R`이다. 표본에서 `L=C`가
없다는 사실은 무한 범위의 증명이 아니다.

수정된 다음 목표는 명시적 `delta>0`, `N0`에 대해 충분히 큰 모든 관련
짝수에서 `L(N)<=(1-delta)C(N)`을 증명하는 것이다. 이것이 P2의 unsigned
지지집합만으로는 얻을 수 없는 부호 상관 추정이다.

## 4. 쌍둥이 소수 트랙: dyadic 패리티 항등식

`[X,2X)`의 소수 `p`에 대해

```text
C2(X) = sum J(p+2),
L2(X) = sum J(p+2)lambda(p+2)
```

라 하자. 쌍둥이 시작 수를 `T(X)`, 소수-합성반소수 시작 수를 `S(X)`라
하면 정확히

```text
T(X) = (C2(X)-L2(X))/2,
S(X) = (C2(X)+L2(X))/2.
```

Chen-positive 블록에 쌍둥이가 존재할 필요충분조건은 `L2<C2`이다. 무한히
많은 dyadic 블록에서 이 부등식이 성립하는 것은 쌍둥이 소수가 무한하다는
것과 동치다. 따라서 TICKET-200의 다음 목표는 추측의 dyadic 재표현이었다.

13개 블록 회귀의 마지막 `[2^22,2^23)`에서 `T=22643`, `S=65808`,
`C2=88451`, `L2=43165`를 얻었다. 유한한 양성 블록은 무한성을 증명하지
않는다. 수정된 목표는 명시적 `delta>0`에 대해 무한히 많은 unbounded
Chen-positive 블록에서 `L2<=(1-delta)C2`를 증명하는 것이다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket201_finite_information_allrun_liouville_parity.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket201_finite_information_allrun_liouville_parity
```

생성기는 통합 JSON 하나와 문제별 JSON 네 개를 기록한다. 새 항등식은 모두
정수 및 유리수 문자열로 검증하며 부동소수점 관측을 증명의 전제로 쓰지
않는다.

## 문헌 경계

- Platt-Trudgian의 엄밀한 유한 높이 RH 검증:
  <https://arxiv.org/abs/2004.09765>
- Polymath의 Selberg sieve 패리티 장벽 분석:
  <https://arxiv.org/abs/1407.4897>
- Pintz의 Chen 소수와 패리티 현상 연구:
  <https://arxiv.org/abs/1004.1065>
- Bordignon-Johnston-Starichkova의 명시적 Chen 정리:
  <https://arxiv.org/abs/2207.09452>

PrimeProject는 이 결과를 외부 경계로 가져오며 고전적인 패리티 장벽이나
Liouville 함수에 대한 독창성 우선권을 주장하지 않는다. 이번 티켓의
프로젝트 내부 성과는 전 반복수 Collatz 항등식과 증명 감사, 그리고 이전
증명 의무가 원문제와 동치였음을 명시적으로 분류한 것이다.
