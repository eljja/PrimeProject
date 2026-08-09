# TICKET-202: 정확 Hermite 데이터, 긴 run 변형, 패리티 척도

## 초록

TICKET-202는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 동시에 증명하거나 반증하려는 PrimeProject의 다음 반복이다. 네 문제
중 어느 것도 해결하지 못했다. 대신 TICKET-201이 남긴 목표의 강도를 다시
검사하여 다음 네 부분정리를 정확히 증명했다.

1. 유한 개의 정확한 Hermite 조건과 콤팩트 유한 jet 제어를 함께 사용해도
   실수-짝 entire 함수 전체에서 전역 실수영점 성질을 강제할 수 없다.
2. `1^k 2^(2k+t)(1 2^2)^(r-1)`로 주어진 3-매개변수 콜라츠 단어족은 모든
   매개변수와 모든 순환 회전에서 affine 나눗셈 조건에 실패한다.
3. 골드바흐 전체 `P2` 채널의 합산 상대 Liouville 결손은 0으로 가므로,
   모든 큰 입력에 고정된 양의 상대 결손을 요구하는 목표는 성립할 수 없다.
4. 쌍둥이 소수에서 고정 상대 결손과 Chen 차수의 채널 질량을 함께 증명하면
   단순 무한성보다 강한 Hardy-Littlewood 차수의 정량 하한이 따라온다.

기계 판독 기준 기록은
[`ticket202-exact-hermite-deformation-parity-scale.json`](../data/open-problem/ticket202-exact-hermite-deformation-parity-scale.json)이다.
네 상태는 모두 `open_not_proven`이고 해결 수는 0이다.

## 결과표

| 문제 | 이번에 확정한 결과 | 폐기하거나 재조정한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 가설 | `ExactFiniteHermiteAndCompactJetGlobalZeroNoGo` (정확 유한 Hermite·콤팩트 jet의 전역 영점 no-go) | 유한한 정확 Xi Hermite 조건을 추가하면 유한 정보 간극이 닫힌다는 경로 | `CompletedZetaCofinalContourMarginWithExactZeroCountTransfer` |
| 콜라츠 | `AllLongRunExtensionsPrimitiveFamilyAffineObstruction` (모든 긴 run 확장 원시 단어족 affine 배제) | 중앙 run 확장을 하나씩 계산 | `SignedTwoSiteValuationTransferAffineObstruction` |
| 강한 골드바흐 | `DyadicP2RelativeLiouvilleDefectDilutionNoGo` (dyadic P2 상대 결손 희석 no-go) | 전체 P2 채널의 고정 양의 상대 결손 | `PointwiseLogLogScaledLiouvilleDefectOnEveryLargeEvenInteger` |
| 쌍둥이 소수 | `RelativeChenDefectQuantitativeTwinStrengthCalibration` (상대 Chen 결손의 정량 강도 교정) | 고정 상대 결손을 단순 무한성 수준 보조정리로 취급 | `PrimeSemiprimeSeparatedChenSwitchingWeightWithPositivePrimeCoefficient` |

## 1. 리만 트랙: 정확한 유한 Hermite 데이터도 전역화되지 않는다

`F`를 실수 계수의 짝 entire 함수라 하자. 콤팩트 원판 `|z|<=R`, 유한한
실수 대칭 보간점 집합, 각 점에서 유한 개의 미분값, 그리고 `A>R`,
`F(iA)!=0`인 `iA`를 고정한다.

양의 보간점 `a_l`과 필요한 미분 차수 `m_l`에 대해

```text
P(z)   = product_l (z^2-a_l^2)^(m_l+1)
H_N(z) = z^(2N) P(z)
G_N(z) = F(z) - F(iA) H_N(z)/H_N(iA)
```

로 둔다. 원점의 미분 조건은 충분히 큰 `z^(2N)` 인자가 보존한다.

### 명제 RH-202

`G_N`은 지정한 모든 Hermite 값을 `F`와 정확히 같게 유지한다. 또한
실수-짝 entire 함수이고 `+iA`, `-iA`에 비실수 영점을 가지며, 임의의 고정된
유한 미분 차수 `M`에 대해

```text
max_{|z|<=R, 0<=j<=M} |G_N^(j)(z)-F^(j)(z)| -> 0
```

이다.

각 `(z^2-a_l^2)^(m_l+1)`은 `+a_l`, `-a_l`에서 필요한 중복도를 가진다.
따라서 perturbation의 지정된 미분값은 모두 0이다. `H_N(iA)`와 `F(iA)`가
실수이므로 계수도 실수이고, 대입하면 `G_N(iA)=0`이다. 한편
`H_N=z^(2N)P`에서 `P`는 고정 다항식이다. Leibniz 공식으로 콤팩트 원판의
각 고정 미분은 `N`의 다항식과 `(R/A)^(2N)`의 곱으로 제한되므로 0으로 간다.

정확 회귀는 다음을 사용한다.

```text
F(z)=z^2-1
P(z)=(z^2-1)^3(z^2-4)^3
보간점={-2,-1,0,1,2}, 미분 차수 j=0,1,2
R=5, A=10, epsilon=1/100
```

최초 성공값은 `N=3`이다. 정확 계수는
`-1/11474737664000000`, 최대 원판 상계는
`224180121/35306885120 < 1/100`이다. 15개의 보간점-미분 조건에서
perturbation 값은 모두 정확히 0이다.

이 결과는 RH 반례가 아니다. `G_N`은 Xi가 아니며 감마 인자, Dirichlet
급수, 완성 제타함수의 함수방정식, Euler product 기원을 보존하지 않는다.
정확한 결론은 하나의 콤팩트 인증에 유한한 정확 데이터를 더하는 방식으로는
부족하다는 것이다. 이후에는 높이가 무한히 증가하는 cofinal contour와
완성 제타함수의 산술 구조가 필요하다.

## 2. 콜라츠 트랙: 무한한 변형 ray의 배제

`r>=2`, `k>=2`, `t>=0`에 대해 가속 콜라츠 지수 단어를

```text
w_(r,k,t) = 1^k 2^(2k+t) (1 2^2)^(r-1)
```

로 정의한다. `n=r-1`, `q=k+n`이라 둔다.

### 명제 CO-202

모든 `w_(r,k,t)`와 모든 순환 회전은 양의 콜라츠 순환에 필요한 affine
나눗셈 방정식에 실패한다.

순서가 있는 affine 분자를 `B`, `D=2^S-3^h`를 분모라 하면

```text
D = 4^t 32^q - 3^t 27^q

5B-23D = 2*27^n E_(k,t)

E_(k,t)
 = 14*3^t*27^k - 5*3^t*18^k - 9*4^t*32^k
 = -F_(k,t)
```

이고 모든 매개변수에서

```text
0 < F_(k,t) < D
```

이다. `t=0`은 TICKET-201의 잔차 부등식이다. `t>=1`에서는 가장 불리한
`(t,k)=(1,2)`부터 `9*4^t*32^k`가 양의 주항을 이기며, 이후 비율은 더
커진다. 또한

```text
D-F_(k,t)
 >= 23*4^t*32^k - 13*3^t*27^k - 5*3^t*18^k > 0
```

이다. `D`는 `6*27^n`과 서로소다. 따라서 `D|B`라면 항등식에 의해
`D|E_(k,t)`여야 하지만 `0<|E|<D`와 모순이다. 유일한 긴 `2`-run은 원시성을
보이고, 회전 recurrence가 모든 순환 회전에 같은 배제를 전달한다.

유한 회귀는 `2<=r,k<=10`, `0<=t<=8`의 `729`개 단어와 모든 회전을
검사한다. 이는 구현 회귀이며 전 매개변수 증명은 위 항등식과 부등식이다.

이 정리는 TICKET-201 단어마다 한쪽 방향으로 무한한 `L1` 변형 ray를 닫는다.
run 단축, 두 위치 사이 valuation 질량 이동, 임의의 multisite 변형, 임의
지수 단어, 비주기 발산은 여전히 열려 있다. 다음 목표는 부호가 있는 두 위치
질량 이동 항등식이다.

## 3. 골드바흐 트랙: 고정 상대 결손은 척도가 잘못됐다

짝수 `N`에 대해 TICKET-201의 채널을 유지한다.

```text
C(N)=R(N)+S(N)
L(N)=S(N)-R(N)
C(N)-L(N)=2R(N)
```

`R`은 소수-소수 채널, `S`는 소수-합성반소수 채널이다. 이를 `(X,2X]`의
짝수 `N`에 대해 합한 값을 `R_X`, `S_X`, `C_X`, `L_X`라 한다.

### 명제 GB-202

소수정리와 소인수 중복도를 포함해 정확히 두 개인 정수에 대한 Landau 정리를
사용하면

```text
R_X/S_X = O(1/log log X)

(C_X-L_X)/C_X = 2R_X/(R_X+S_X) -> 0
```

이다. 따라서 어떤 고정 `delta>0`도 모든 충분히 큰 Chen-positive 짝수에서

```text
L(N) <= (1-delta)C(N)
```

을 만족할 수 없다.

`R_X<=pi(2X)^2=O(X^2/log^2 X)`이다. `S_X`의 하한에서는 첫 홀수 소수 `p`와
홀수 합성반소수 `m`을 모두 `(X/2,X]`로 제한한다. 그러면 `p+m`은
`(X,2X]`에 있다. PNT는 약 `X/(2log X)`개의 소수를 주고, Landau 정리는 약
`X log log X/(2log X)`개의 홀수 반소수를 준다. 짝수 반소수는 낮은 차수다.
따라서

```text
S_X = Omega(X^2 log log X/log^2 X)
```

이고 정확한 projector 항등식으로 결론이 따른다. 고정된 pointwise `delta`가
존재하면 dyadic 블록에 합해도 같은 하한이 남아야 하므로 극한과 모순이다.

정확 유한 회귀는 `[2^10,2^11]`부터 `[2^20,2^21]`까지 계산한다. 관측 결손은
`25598/36655`에서 `18844127294/35051527549`로 감소했다. 이 유한 단조성은
점근 정리의 증명에 사용하지 않는다.

이 no-go는 골드바흐를 반증하지 않는다. 상대 결손은 0으로 가면서도 모든
정수에서 양수일 수 있다. 자연스러운 교정 척도는 대략 `1/log log N`이다.
이번 작업은 그 척도의 pointwise 하한을 증명하지 않았고 희소 exceptional
set도 제거하지 않았다.

## 4. 쌍둥이 소수 트랙: 고정 결손은 단순 무한성보다 훨씬 강하다

dyadic 블록에서 TICKET-201은

```text
C2(X)-L2(X)=2T(X)
```

를 증명했다. `T(X)`는 쌍둥이 소수 시작점 수, `C2(X)`는 쌍둥이 또는
소수-합성반소수 시작점 수다. 다음을 정의한다.

```text
delta_X = 1-L2(X)/C2(X) = 2T(X)/C2(X)
```

### 명제 TP-202

무한히 많은 블록에서

```text
C2(X) >= a X/(log_2 X)^2
delta_X >= d > 0
```

이면 그 블록들에서

```text
T(X) >= (ad/2) X/(log_2 X)^2
```

이다. 따라서 고정 상대 결손과 Chen 차수 질량의 결합은 단순 무한성 보조정리가
아니라 Hardy-Littlewood 차수의 정량 하한이다.

증명은 `T=(delta_X/2)C2`를 대입하면 즉시 나온다. 채널 대수와 twin 양성만으로
고정 `delta`가 나오지 않음을 보이기 위해 다음 정확한 논리 반모형을 둔다.

```text
T(X)=1
C2(X)=floor(X/(log_2 X)^2)
L2(X)=C2(X)-2
```

그러면 모든 블록에서 `C2-L2=2T`이고 twin-positive이지만
`delta_X=2/C2(X)->0`이다. 이것은 소수의 산술 모형이 아니라 잘못된 논리적
함의를 깨는 채널 반모형이다.

실제 유한 회귀는 `[2^22,2^23)`까지 13개 블록의 normalized transfer
identity를 정확히 확인한다. 논리 반모형 회귀는 `X=2^30`까지 21개 블록이다.

TICKET-202는 실제 소수 채널의 고정 상대 결손을 증명하거나 반증하지 않는다.
고정 결손을 작은 중간 단계로 취급하던 강도 평가만 폐기한다. 다음 유의미한
메커니즘은 상대 결손이 0으로 가는 상황에서도 소수와 반소수 질량을 분리하는
parity-sensitive switching weight다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket202_exact_hermite_deformation_parity_scale.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket202_exact_hermite_deformation_parity_scale -v
```

생성기는 통합 JSON 하나와 문제별 JSON 네 개를 쓴다. 다항식 계수, Hermite
평가값, 콜라츠 정수 항등식, 채널 수, 상대 결손, proof DAG가 모두 직렬화된다.

## 문헌 경계

- Dave Platt와 Tim Trudgian의 [The Riemann hypothesis is true up to
  `3*10^12`](https://arxiv.org/abs/2004.09765)는 엄밀한 유한 높이 문맥이다.
  이번 작업은 새로운 Xi 영점을 계산하지 않았다.
- Edmund Landau의 [*Handbuch der Lehre von der Verteilung der
  Primzahlen*](https://doi.org/10.1007/BF01742852)은 GB-202에서 사용하는
  고전적 `Omega(n)=2` 계수 점근식을 제공한다.
- Lasse Grimmelt와 Gautami Bhowmik의 [The exceptional set of the Goldbach
  problem](https://arxiv.org/abs/2607.27282)은 최신 exceptional-set 및
  명시적 major-arc 문맥이지만 이번에 남은 pointwise 정리를 주지 않는다.
- Jing-Run Chen의 [On the representation of a large even integer as the sum
  of a prime and the product of at most two
  primes](https://doi.org/10.1360/YA1973-16-2-157)은 고전적 거의소수 문맥이다.
- Kaisa Matomaki와 Sebastian Zuniga Alterman의 [Weighted sieves with
  switching](https://arxiv.org/abs/2405.19063)은 남은 Twin switching-weight
  경로와 인접한 최신 연구지만 필요한 소수/반소수 분리를 증명하지 않는다.

Hermite perturbation과 채널 강도 항등식은 초등적이다. Collatz 단어족 항등식은
프로젝트 내부 결과다. 독립 전문가 검토 전에는 학술적 우선권을 주장하지 않는다.

## 최종 경계

TICKET-202는 네 부분정리, 네 경로 결정, 네 proof DAG를 기록한다. 네 난제는
모두 열려 있으며 완전한 증명이나 반례는 없다.
