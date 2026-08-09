# TICKET-198: 검증 높이, 원시 단어, 양화사 강도

## 초록

TICKET-198은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 동시에 계속 공격한다. 이번 티켓은 네 개의 정확한 중간정리를
확립하지만 부모 난제는 하나도 해결하지 않는다.

1. Platt--Trudgian의 엄밀한 유한높이 RH 검증을 이용하면 모든 정수
   `2<=m<=3*10^12`에 대한 Xi 사각형의 존재적 Rouché 인증이 따라온다.
2. TICKET-183의 원시 root 환원을 적용한 뒤에도, 고정된 모든 cyclic run
   수마다 두 scalar gate를 통과하는 원시 `{1,2}` 단어가 무한히 남는다.
3. proper-prime-power 충돌이 없는 표적을 모두 해결해도 골드바흐 예외는
   `O(X/log^2 X)`로 줄어들 뿐, 0이 되지는 않는다.
4. 쌍둥이 소수의 전역 block mass로 prime-power 오염을 이기려는 목표는
   블록당 `sqrt(X)/log X` 규모의 쌍을 요구하므로 단순 무한성보다 훨씬
   강하다.

통합 기계 판독 결과는
[`ticket198-verified-height-primitive-word-quantifier-strength.json`](../data/open-problem/ticket198-verified-height-primitive-word-quantifier-strength.json)에
있다. 모든 상태는 `open_not_proven`이며 해결된 난제 수는 0이다.

## 주장 표

| 문제 | TICKET-198의 정확한 결과 | 폐기 또는 제한된 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 가설 | `FiniteHeightRHTransfersToFiniteXiRouchePrefix` | 존재적인 `D_3` 하나를 결정적 RH 연결로 보는 해석 | `StandaloneIntervalXiTaylorDegreeAndRoucheMarginOnD3WithoutImportingFiniteHeightRH` |
| 콜라츠 | `FixedRunCountLeavesInfinitePrimitiveAdmissibleFamilies` | 원시 정규화와 고정 run 수를 유한 탐색으로 보는 경로 | `UniformAffineDivisibilityObstructionForPrimitiveFixedRunCountOneTwoWordsInTheAdmissibleDensityWindow` |
| 골드바흐 | `CollisionFreeGoldbachMarginLeavesLogSquaredExceptionalSet` | 밀도 1 collision-free 제어를 모든 짝수로 승격 | `ExplicitGoldbachCorrelationMarginOnEveryLargeCollisionSupportedEvenTarget` |
| 쌍둥이 소수 | `TwinBlockMassDominanceForcesSquareRootScalePairCount` | 전역 오염 우세를 최소 무한성 목표로 사용 | `PrimePowerFreeLocalizedTwinDetectorHasPositiveMassOnInfinitelyManyDyadicBlocks` |

## 1. 리만 가설

### 1.1 선언 명제

다음을 두자.

```text
Xi(z) = xi(1/2 + i z),
D_m^+ = {z: |Re z| <= m, 1/m <= Im z <= m},
D_m^- = D_m^+의 켤레.
```

`0<|gamma|<=H`인 모든 비자명 영점 `beta+i gamma`가 `beta=1/2` 위에
있다고 가정하자. 그러면 모든 정수 `2<=m<=H`에 대해 Xi는 닫힌 두
`D_m` 사각형에서 영점이 없다. 따라서 각 사각형에는 엄격한 Rouché
부등식을 만족하는 Xi의 Taylor 절단이 존재한다.

Platt와 Trudgian은
[The Riemann hypothesis is true up to 3*10^12](https://doi.org/10.1112/blms.12460)에서
구간 산술로 `H=3*10^12`까지 이 전제를 엄밀하게 검증했다. PrimeProject는
그 정리를 가져와 proof DAG 언어로 옮긴다. 그들의 영점 검산을 새로
수행하거나 프로젝트 고유의 RH 진전이라고 주장하지 않는다.

### 1.2 증명

`z=x+i y`이면

```text
s = 1/2 + i z = (1/2-y) + i x.
```

`D_m^+` 또는 `D_m^-`의 영점은 `|Im s|<=m<=H`이면서 임계선에서 적어도
`1/m` 떨어져야 한다. 외부 유한높이 정리가 이를 배제한다. 실수 구간
`0<s<1`에서는 교대 eta 급수가 양수이고
`zeta(s)=eta(s)/(1-2^(1-s))`이므로 영점이 없다. 따라서 각 닫힌
사각형에서 Xi의 절댓값은 양의 최솟값을 가진다. compact-uniform Taylor
수렴과 Rouché 정리를 적용하면 영점 수가 0인 절단이 존재한다.

### 1.3 확립된 범위와 한계

- 전달된 정수 사각형 단계: `2,999,999,999,999`개.
- `D_3`은 열린 임계띠의 양 끝부분에 들어간다.
- Taylor 차수와 구간 산술 마진은 여전히 명시되지 않았다.
- `3*10^12`보다 높은 ordinate는 전혀 제어하지 않는다.

다음 목표는 외부 유한높이 정리를 가져오지 않고 `D_3`에서 차수와 마진을
직접 검증하는 독립 구간 인증이다. 이것은 구현 재현성 목표이지 RH 전체
해결 주장이 아니다.

## 2. 콜라츠 추측

### 2.1 선언 명제

TICKET-183은 이미 반복 단어의 정확한 원시 root 환원을 증명했다.
TICKET-198은 이를 기존 입력으로 사용하며 새 결과로 다시 주장하지 않는다.
모든 고정 정수 `r>=2`, `k>=2`에 대해

```text
w_(r,k) = 1^k 2^(2k) (1 2^2)^(r-1)
```

로 두자. 이 단어는 원시 단어이고, cyclic one-run과 two-run을 각각 정확히
`r`개 가지며, 1의 밀도는 `1/3`이고 두 scalar cycle gate를 모두 통과한다.
따라서 원시 정규화와 고정 run 수만으로 남은 탐색을 유한 열거로 만들 수
없다.

### 2.2 증명과 계산

`q=k+r-1`이면

```text
1의 수 = q,
2의 수 = 2q,
h = 3q,
S = 5q
```

이고 두 gate는 다음 정확한 정수 부등식으로 통과한다.

```text
2^S = 32^q > 27^q = 3^h,
2^q(5/6)^(3q) = (125/108)^q > 1.
```

cyclic run 길이는

```text
(k, 2k, 1, 2, ..., 1, 2)
```

이다. `k>=2`이면 길이 `k`인 one-run과 길이 `2k`인 two-run이 각각
유일하다. 비자명한 단어 거듭제곱이라면 모든 cyclic run 패턴이 반복되어야
하므로 이 유일성과 모순이다. 따라서 단어는 원시이다. 고정 `r`에서 `k`를
무한히 키우면 서로 다른 원시 단어가 무한히 생긴다.

생성기는 `r=2,...,8`, `k=2,...,64`의 441개 단어에 대해 원시성, run 수,
두 scalar gate를 정확 정수로 검사한다. 유한 검사는 구현 회귀 검사이고,
전체 `r,k` 명제는 위 기호 증명에서 나온다.

### 2.3 경로 판정

- **폐기:** 원시 정규화와 고정 run 수를 유한 탐색 공간으로 보는 방법.
- **유지:** 각 고정 run 수에 대해 모든 길이를 덮는 affine divisibility
  obstruction을 기호적으로 증명하는 방법.
- **한계:** 이 무한 단어족의 affine divisibility는 해결하지 않았고,
  valuation 3 이상과 비주기 발산 궤적도 남는다.

## 3. 강한 골드바흐 추측

### 3.1 선언 명제

proper-prime-power 중복 `Q*Q`가 양수인 짝수 표적 집합을 `C`, 실제
골드바흐 예외 집합을 `E`라고 하자. 충분히 큰 모든 `N not in C`가 두
소수의 합이라는 정리를 얻더라도 결론은

```text
E \ C는 유한,
|E intersect [1,X]| = O(X/log^2 X)
```

뿐이다. 두 번째 식은 TICKET-197의 `C` 지지집합 상계를 쓴다. 이로부터
`E=empty`는 나오지 않는다.

### 3.2 정확한 no-go 증인

모든 홀수 소수 `p`에 대해

```text
2p^2 = p^2 + p^2
```

이므로 `S={2p^2}`는 `C`의 명시적 무한 부분집합이다. `S`에서만 0이고
`C` 밖에서 양수인 추상 표현 지시함수는 collision-free 양성을
만족하면서 실패가 무한히 많다. 이것은 추론 규칙의 반례이지 실제
골드바흐 반례도 아니고 실제 소수 표현함수도 아니다.

`2^20`까지의 유한 재생에서는 collision 표적 17,411개와 대각선 표적
127개를 찾았고 모두 실제 골드바흐 표현을 가진다. 이 유한 사실은 무한
대각선으로 승격하지 않는다.

### 3.3 경로 판정

기존 collision-free 보조정리는 이제 두-stratum 증명의 절반으로만
유지한다. 나머지 결정적 목표는 충분히 큰 모든 collision-supported
짝수에서의 pointwise 양성이다.

## 4. 쌍둥이 소수 추측

### 4.1 선언 명제

`[X,2X)`의 쌍둥이 소수 시작점 개수를 `T(X)`, 가중 질량을

```text
M(X)=sum log(p)log(p+2)
```

라 하면 각 항이 `log(2X+2)^2` 이하이므로

```text
M(X) <= T(X)log(2X+2)^2.
```

따라서

```text
M(X) >= K sqrt(X)log X
```

라는 전역 오염 우세는

```text
T(X) >= K sqrt(X)log X / log(2X+2)^2
```

를 강제한다. 우변은 무한대로 가므로 이 목표는 한 쌍의 존재보다 훨씬
강하다.

### 4.2 계산과 추론 한계

`[2^10,2^11)`부터 `[2^22,2^23)`까지 13개 블록이 mass-count 부등식을
재생한다. 마지막 블록에는 22,643개의 관측 쌍이 있고, 상수 1의
`sqrt(X)log X` 질량은 최소 123개를 강제한다. 이 유한 관측은 무한
하한을 증명하지 않는다.

추상적으로 `X_j=2^(2^j)` 블록마다 양의 원자 하나만 두면 무한성은
유지되지만 가능한 로그 질량과 `sqrt(X_j)log X_j`의 비는 0으로 간다.
이것은 소수의 모형이나 형식적 독립성 증명이 아니다. 단순 무한성만으로
전역 정량 하한이 나오지 않는다는 정보 예산을 정확히 드러낸다.

### 4.3 경로 판정

- **최소 목표로는 폐기:** 모든 prime-power 오염을 전역 질량으로 압도.
- **유지:** prime-power 오염에서는 0이고 실제 gap-two 쌍 하나가 있으면
  양수가 되는 국소 비음수 검출기.
- **미해결:** 무한히 많은 블록에서 그 검출기의 양성을 증명하는 일.

## 5. Proof DAG

네 트랙은 다음 구조로 기록된다.

```text
TICKET-197 열린 목표
        |
        v
TICKET-198 정확 정리 ---- 반증되거나 과도한 경로
        |
        v
수정된 단일 보조정리 (open_not_proven)
```

어느 DAG에도 부모 난제로 이어지는 `proved` 경로가 없다.

## 6. 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket198_verified_height_primitive_word_quantifier_strength.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket198_verified_height_primitive_word_quantifier_strength -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
node scripts\verify_pages.cjs
```

예상 기계 경계:

```text
정확 정리: 4
Collatz 고정-run 원시 단어: 441
Goldbach cutoff 행: 13
Twin dyadic 행: 13
해결된 부모 난제: 0
실패: 0
```
