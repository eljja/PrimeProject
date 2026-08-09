# TICKET-199: 대칭 표본, 두 run 쌍 배제, squarefree-Lambda 필터

## 초록

TICKET-199는 네 난제 중 어느 것도 해결됐다고 주장하지 않는다. 이번
티켓에서 확정한 것은 다음 네 개의 정확한 중간 결과다.

1. 경계의 유한한 점들에서 함수값이 일치한다는 사실만으로는 실수계수
   짝함수 전체에서도 Rouché 무영점 인증을 할 수 없다.
2. TICKET-198에서 만든 `r=2` 원시 콜라츠 무한족은 모든 `k>=2`에서
   affine divisibility를 만족하지 못한다.
3. `P(n)=mu(n)^2 Lambda(n)`은 소수만 남기는 정확한 projector이므로
   골드바흐의 prime-power 충돌을 항등적으로 제거한다.
4. 같은 projector는 TICKET-198이 요구한 쌍둥이 소수용 prime-power-free
   국소 검출기를 정확히 구성한다.

네 추측의 상태는 모두 `open_not_proven`이고 해결 수는 0이다. 통합 JSON은
[`ticket199-symmetric-sampling-two-run-squarefree-filter.json`](../data/open-problem/ticket199-symmetric-sampling-two-run-squarefree-filter.json)이다.

## 결과 표

| 문제 | 이번에 확정한 결과 | 폐기·교정한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 가설 | `FiniteBoundarySamplingNoGoForRealEvenRoucheCertification` | 유한 점 평가만으로 Rouché 인증 | `IntervalBoundaryMeshWithDerivativeBoundCertifiesStrictRoucheMarginOnD3` |
| 콜라츠 추측 | `TwoRunPairPrimitiveFamilyAffineDivisibilityObstruction` | 명시적 `r=2` 무한족을 양의 cycle 후보로 유지 | `ThreeRunPairPrimitiveFamilyAffineDivisibilityObstructionForAllScales` |
| 강한 골드바흐 | `MobiusSquarefreeLambdaExactGoldbachPrimeProjector` | 최종 검출기에서도 proper prime power 충돌층을 별도로 취급 | `UniformPositiveLowerBoundForMobiusSquarefreeGoldbachCorrelationAtEverySufficientlyLargeEvenTarget` |
| 쌍둥이 소수 | `MobiusSquarefreeLambdaExactTwinPrimeDetector` | 정확한 소수 투영 뒤에도 prime-power 오염을 다시 빼는 경로 | `ParityBreakingPositiveLowerBoundForMobiusSquarefreeLambdaShiftTwoCorrelationOnInfinitelyManyDyadicBlocks` |

## 1. 리만 가설

### 선언 명제

`D_3^+` 경계에서 유한 표본집합 `S`를 잡고 부호와 켤레복소수에 대해
대칭화한다. 이 유한 궤도에 속하지 않고 `Im(a^2)!=0`인 내부점 `a`를
선택하면 다음을 만족하는 실수계수 짝다항식 `G`가 존재한다.

```text
모든 s in S에서 G(s)=1,
내부점 a에서 G(a)=0.
```

따라서 표본 사이의 함수값을 제어하는 구간 경계나 도함수 상계가 없다면,
점 표본의 개수가 아무리 많아도 무영점이나 엄격한 Rouché 부등식을
인증하지 못한다.

### 정확한 구성

표본점 제곱과 그 켤레들의 집합을 `R`이라 하고

```text
Q(z) = product_(rho in R) (z^2-rho)
```

로 둔다. `Q`는 실수계수 짝다항식이고 모든 표본점에서 0이다.
`Im(a^2)!=0`이므로 실수 `u,v`를 사용해

```text
u+v a^2 = -1/Q(a)
```

를 정확히 풀 수 있다. 그러면 `G(z)=1+Q(z)(u+v z^2)`가 원하는 반례다.
계산기는 `a=1+i`와 네 개의 유리수 경계 mesh를 사용하며 모든 등식을
`Fraction`으로 검증한다.

### 한계

`G`는 Xi가 아니므로 이는 RH 반례가 아니다. 구간산술, 도함수로 mesh
사이를 연결하는 방법, 전체 경계의 modulus 상계도 반박하지 않는다.
폐기되는 것은 유한 점 평가만으로 전체 경계 인증을 대신하는 경로뿐이다.

## 2. 콜라츠 추측

### 선언 명제

모든 `k>=2`에 대해

```text
w_k = 1^k 2^(2k) 1 2^2
```

를 생각한다. 이 단어는 TICKET-198의 `r=2` 원시 무한족이며 두 scalar
gate를 모두 통과한다. 그러나 이 단어와 모든 순환 이동은 양의 accelerated
Collatz cycle에 필요한 affine divisibility를 만족하지 못한다.

### 닫힌식 증명

`x=32^k`, `y=27^k`, `z=18^k`라 두면

```text
D = 32x - 27y,
B = 50x + 27y - 54z,
R = 41x - 27z,
B = 2R (mod D).
```

`D`가 홀수이므로 `D|B`와 `D|R`은 동치다. `k>=5`에서는

```text
R-D  = 9(x+3y-3z) > 0,
2D-R = x[23-54(27/32)^k+27(18/32)^k] > 0.
```

두 번째 대괄호는 `k=5`에서 양수이고 이후 엄격히 증가한다. 따라서
`D<R<2D`라서 나누어떨어질 수 없다. 남은 세 규모의 정확한 나머지는
각각 `7066`, `151754`, `1746214`로 0이 아니다. 첫 valuation `v`를 끝으로
옮긴 왼쪽 순환 이동의 분자를 `B'`라 하면 직접 지표를 바꾸어

```text
2^v B' = 3B + D
```

를 얻는다. `gcd(6,D)=1`이므로 `D|B`와 `D|B'`는 동치다. 이 항등식을
반복하면 회전 불변성이 증명되어 회전류 전체가 배제된다. 계산기는
`k=128`까지 모든 회전도 회귀 검사한다.

### 한계

이 정리는 하나의 명시적 무한족만 닫는다. 두 run 쌍을 갖는 임의의 단어,
세 run 쌍 이상, 비주기 궤도는 여전히 열려 있다. parity word와 balanced
word의 최신 연결은 연구 배경으로만 참고했으며 증명 입력은 아니다:
[Fernández--Ibáñez, 2026](https://arxiv.org/abs/2607.24844).

## 3. 강한 골드바흐 추측

### 정확한 소수 투영

```text
P(n) = mu(n)^2 Lambda(n)
```

로 둔다. von Mangoldt 함수는 소수 거듭제곱에서만 0이 아니고, squarefree
인자 `mu^2`는 `p`에서 1이지만 `p^k`, `k>=2`에서 0이다. 따라서

```text
P(n)=log p  if n=p is prime,
P(n)=0      otherwise.
```

결국

```text
G(N)=sum_(a+b=N)P(a)P(b)
```

는 `N`이 두 소수의 합일 때에만 양수다. TICKET-198에서 별도 난층으로
남겼던 `Q*Q` 충돌과 `2p^2` 대각선은 이 검출기에서 정확히 0이 된다.

계산기는 projector를 `2^23`까지 검사하고, `2^20` 이하의 모든
proper-prime-power 충돌 지지 짝수를 재생한다. support 불일치, 누출,
유한 골드바흐 실패는 0건이다. 그러나 유한 계산은 충분히 큰 모든 `N`의
양성을 증명하지 않는다.

이 필터는 장부를 교정했을 뿐 binary correlation 난제를 풀지 않는다.
고전적인 예외집합 결과도 모든 `N`에 대한 점별 하한은 제공하지 않는다:
[Montgomery--Vaughan, 1975](https://doi.org/10.4064/aa-27-1-353-370).

## 4. 쌍둥이 소수 추측

같은 projector로

```text
T(X)=sum_(X<=n<2X)P(n)P(n+2)
```

를 정의한다. 모든 항은 음이 아니고 proper prime power는 정확히 제거된다.

```text
T(X)>0  iff  [X,2X)에 쌍둥이 소수 시작점이 존재한다.
```

따라서 TICKET-198이 요구한 prime-power-free 국소 검출기의 구성 부분은
완료됐다. `2^23`까지 13개 dyadic block에서 실제 쌍과 support가 정확히
일치한다. 하지만 무한히 많은 블록에서 양수라는 정리는 전혀 얻지 못했다.
그것이 여전히 parity-breaking 핵심이다. Maynard의 bounded-gap 정리는
고정 간격 2를 주지 않으며, Ford--Maynard가 강조한 Type-I/II 정보의 필요도
남아 있다:
[Maynard, 2013](https://arxiv.org/abs/1311.4600),
[Ford--Maynard, 2024](https://arxiv.org/abs/2407.14368).

## 5. 증명 DAG와 재현

각 트랙의 상태는 다음과 같다.

```text
TICKET-198 미해결 목표
        |
        v
TICKET-199 정확한 정리 ---- 폐기·교정된 경로
        |
        v
다음 단일 보조정리 (highest_risk_open)
        |
        v
원래 추측 (open_not_proven)
```

재현 명령:

```powershell
D:\python\anaconda3\python.exe scripts\ticket199_symmetric_sampling_two_run_squarefree_filter.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket199_symmetric_sampling_two_run_squarefree_filter -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
node scripts\verify_pages.cjs
```

기대 경계는 `정확한 정리 4`, `해결된 추측 0`, `기계 실패 0`이다.
