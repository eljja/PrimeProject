# TICKET-188: 공통 형식, 네-1 콜라츠 순환, 소수 거듭제곱 오염, 이진 구간 oracle

## 1. 주장 경계

TICKET-188은 TICKET-187의 네 미해결 노드를 이어간다. 콜라츠에서 새로운
무한 순환 부분족 하나를 배제하고, 나머지 세 문제에서는 전역 승격 또는
정보 경계를 정확한 정리로 확정한다. 리만 가설, 콜라츠 추측, 강한 골드바흐
추측, 쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않았다.

| 문제 | TICKET-188의 정확한 결과 | 폐기·수정한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | `CommonFormDefectPromotionAndMovingDirectionNoGo` (공통 형식 결함 승격과 이동 방향 반례) | 정확한 중첩이나 하나의 형식으로의 수렴 없이 유한 행렬 결함 감소를 전역 양성으로 승격 | `PoleNeutralGuinandWeilMatricesConvergeToOneCommonFormWithCertifiedVanishingOperatorError` |
| 콜라츠 | `ExactlyFourValuationOnesOtherwiseTwoCycleExclusion` (정확히 네 번 1이고 나머지가 2인 순환 배제) | 남은 모든 길이를 유한 탐색으로 대신 | `NoContractingValuationWordWithExactlyFiveOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| 골드바흐 | `VonMangoldtPrimePowerContaminationBridge` (폰 망골트 소수 거듭제곱 오염 제거 다리) | 전체 폰 망골트 합을 소수-소수 질량과 동일시 | `ExplicitBinaryGoldbachVonMangoldtLowerBoundDominatesPrimePowerContaminationForEveryLargeEvenTarget` |
| 쌍둥이 소수 | `SubFourTwinIntervalExactCountOracleAndDyadicEquivalence` (폭 4 미만 구간의 정확 개수 판정과 이진 구간 동치) | 모든 블록에서 폭 4 미만 구간을 얻는 것을 약한 근사 목표로 간주 | `IndependentTypeIITwinProjectorLowerEndpointIsPositiveOnInfinitelyManyDyadicBlocks` |

재현 명령은 다음과 같다.

```powershell
D:\python\anaconda3\python.exe scripts\ticket188_nested_fourone_primepower_dyadic.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket188_nested_fourone_primepower_dyadic -v
```

주 기계 판독 산출물은
`data/open-problem/ticket188-nested-fourone-primepower-dyadic.json`이다. 네 문제의
상태는 모두 `open_not_proven`, 즉 미해결이다.

## 2. 리만 가설

### 2.1 이번에 증명한 명제

`A_N`이 하나의 에르미트 형식(Hermitian form)을 정확히 중첩한 주부분 행렬이고

```text
delta_N = max(0, -lambda_min(A_N))
```

이라 하자. 그러면 `delta_N`은 감소하지 않는다. 따라서 어떤 공종적 부분열에서
`delta_N -> 0`이면 모든 `delta_N`이 처음부터 0이며, 유한 지지 벡터 전체에서
원래 형식이 음이 아님을 알 수 있다.

근사형도 성립한다. 하나의 고정 형식 `Q`와 모든 고정 유한 지지 벡터 `f`에 대해

```text
|Q(f) - <A_N f,f>| <= epsilon_N ||f||^2,
lambda_min(A_N) >= -eta_N,
epsilon_N + eta_N -> 0
```

이면 `Q(f)>=0`이다.

### 2.2 증명

`A_N`의 레일리 몫(Rayleigh quotient) 영역은 `A_(N+1)`의 영역에 포함된다.
따라서 Cauchy 끼워넣기 정리로

```text
lambda_min(A_(N+1)) <= lambda_min(A_N),
delta_(N+1) >= delta_N
```

이다. 음이 아닌 비감소 수열이 공종적 부분열에서 0으로 가려면 모든 항이 0이어야
한다. 근사형에서는 `f`의 지지를 포함하는 `N`에 대해
`Q(f)>=-(epsilon_N+eta_N)||f||^2`를 얻고 극한을 취한다.

### 2.3 정확한 반례와 폐기 경로

```text
A_N = diag(1,...,1,-1/N)
```

은 모든 차원에서 부정부호이지만 결함은 `1/N -> 0`이다. 음의 좌표가 매번
이동하며 인접 행렬은 겹치는 좌표에서 일치하지 않는다. 따라서 공통 형식 계약이
없는 결함 감소만으로 Weil 형식의 전역 양성을 주장할 수 없다.

### 2.4 남은 간극

실제 pole-neutral Guinand-Weil 행렬들이 하나의 공통 형식의 제한이거나, 그 형식에
인증된 연산자 오차로 수렴한다는 사실을 증명하지 못했다. 이것이 다음 산술·해석
보조정리다. Suzuki의 screw-function 연산자 극한도 아직 추측 단계이며, 후속 수치
실현 연구도 RH를 증명했다고 주장하지 않는다:
[Suzuki 2026](https://arxiv.org/abs/2606.09096),
[Kim 외 2026](https://arxiv.org/abs/2607.24830).

## 3. 콜라츠 추측

### 3.1 이번에 증명한 명제

가속 콜라츠 순환의 valuation 주기에서 정확히 네 항이 1이고 나머지 항이 모두
2인 양의 정수 순환은 없다. 원시 주기와 반복 주기를 모두 포함한다.

### 3.2 정확한 순환식

순환 회전 후 네 간격을 `a,b,c,d>=1`이라 쓰고 `d`가 가장 크도록 잡는다.
`h=a+b+c+d`일 때 분모와 순서 의존 affine 분자는

```text
D = 4^h/16 - 3^h,

B = 4^h/16 - 3^(h-1)
    + 4^a 3^(h-a-1)
    + 2*4^(a+b-1) 3^(c+d-1)
    + 4^(a+b+c-1) 3^(d-1)
```

이다. 정수 순환에는 `D | B`가 필요하다. 수축 범위는 `h>=10`이며 `B>D`,
`B,D`는 모두 홀수다.

### 3.3 모든 길이에 대한 부등식

`u=3/4`로 두면 `B<3D`에 충분한 조건은

```text
(16/3)u^(h-a) + (8/3)u^(c+d) + (4/3)u^d + (128/3)u^h < 2
```

이다. `d`가 최대 간격이므로

```text
d >= ceil(h/4),
c+d >= ceil(h/4)+1,
h-a >= ceil((h+2)/2)
```

이고, 이로 얻는 전체 단어 majorant는 감소한다. `h=16`에서 이미

```text
63175275 / 33554432 < 2
```

이므로 모든 `h>=16`에서 `1<B/D<3`이다. 나눗셈이 성립하면 홀수 몫이어야 하지만
1과 3 사이에는 홀수 정수가 없다.

### 3.4 유한 범위와 한계

`h=10,...,15`의 남은

```text
sum binomial(h,4) = 4116
```

단어는 정수 연산으로 전수검사했으며 나눗셈 적중이 0이다. 이것은 새로운 무한
주기 부분족을 닫지만, 1이 다섯 번 이상인 단어, 3 이상의 valuation, 비주기 발산은
다루지 않는다. 2-adic ghost cycle 연구는 국소 순환식만으로 양의 정수 순환을
구분하기 어렵다는 별도의 장벽을 보여준다:
[Dhiman-Pandey 2026](https://arxiv.org/abs/2601.12772).

## 4. 강한 골드바흐 추측

### 4.1 이번에 증명한 명제

짝수 `N`에 대해 이항 폰 망골트 합을

```text
R_Lambda(N) = sum Lambda(m)Lambda(N-m)
            = P_Lambda(N) + E_pp(N)
```

으로 정확히 나눈다. `P_Lambda`는 양 끝이 모두 소수인 질량이고, `E_pp`는 적어도
한쪽이 진정한 소수 거듭제곱인 오염 질량이다. `A(N)`을 `N` 이하 진정한 소수
거듭제곱의 수라 하면

```text
0 <= E_pp(N) <= 2 A(N) (log N)^2
```

이다. 따라서 `R_Lambda(N)>2A(N)(log N)^2`라는 엄밀한 하계가 있으면
`P_Lambda(N)>0`, 즉 골드바흐 표현이 존재한다.

### 4.2 증명과 반례

`Lambda(m)Lambda(N-m)`의 양 끝 지수를 1인지 2 이상인지에 따라 분할하면 정확한
항등식을 얻는다. 오염된 순서쌍은 왼쪽 또는 오른쪽에 진정한 소수 거듭제곱을
가지므로 최대 `2A(N)`개이며 각 가중치는 `(log N)^2` 이하이다.

`R_Lambda=P_Lambda`라는 동일시는 거짓이다. `N=18`에는 `9+9`가
`(log 3)^2`만큼 오염 항에 기여하며, `2+16`, `16+2`도 존재한다. 전체 가중 합의
양성을 소수-소수 질량의 양성으로 바꾸려면 오염 제거가 반드시 필요하다.

### 4.3 남은 간극

이번 정리는 충분조건만 주며 모든 짝수에 대한 `R_Lambda` 하계를 만들지 않는다.
`N<=100000` 유한 표는 분해를 재현할 뿐이다. 최신 exceptional-set 연구는 명시적
major-arc 공식을 제공하지만 모든 짝수의 예외를 제거하지 않는다:
[Grimmelt-Bhowmik 2026](https://arxiv.org/abs/2607.27282).
폰 망골트 가중치와 소수 거듭제곱 항의 구분은 표준 원 방법에서도 사용된다:
[Helfgott의 ternary Goldbach 연구](https://arxiv.org/abs/1501.05438).

## 5. 쌍둥이 소수 추측

### 5.1 이번에 증명한 명제

`C_j`를 `[2^j,2^(j+1))`에서 시작하는 쌍둥이 소수 쌍의 수라 하고
`Delta_j=4C_j`라 하자. `Delta_j`를 포함하는 신뢰 가능한 구간 `[L_j,U_j]`의
폭이 4보다 작으면 `4Z_>=0`의 점을 정확히 하나만 포함하므로 `C_j`를 정확히
복원한다. 또한

```text
L_j > 0  <=>  C_j > 0
```

이다. 폭 4의 `[0,4]`는 `C_j=0`과 `C_j=1`을 모두 허용하므로 경계가 날카롭다.

### 5.2 이진 구간 동치와 경로 수정

모든 쌍둥이 소수는 정확히 하나의 이진 구간에 들어가며 유한 개 구간은 유한 개
정수만 포함한다. 따라서 쌍둥이 소수 추측은 무한히 많은 이진 구간에서
`C_j>0`인 것과 동치다. 신뢰 가능한 인증구간 아래에서는 무한히 자주 `L_j>0`인
것과 동치다.

반면 모든 구간에서 폭 4 미만 인증을 만드는 것은 각 구간의 정확한 개수를
복원하는 oracle이다. 이는 약한 근사 목표가 아니라 필요 이상으로 강하다.
유의미한 다음 목표는 무한 부분열에서 한쪽 하계만 양수로 만드는 것이다.

### 5.3 계산과 한계

유한 ledger는 `j=4,...,19`의 16개 사전 선언 구간을 검사한다. 폭 `7/2` 구간은
직접 센 개수를 중심으로 만들었으므로 반올림 논리의 재현 자료일 뿐 독립적인
해석 인증이 아니다. 실제 하계를 만들려면 진정한 Type I/II 정보가 필요하다:
[Ford-Maynard 2024](https://arxiv.org/abs/2407.14368).

## 6. 증명 상태 결론

TICKET-188은 네 개의 정확한 정리를 증명했다. 새 무한 산술 부분족을 닫은 것은
콜라츠 결과 하나뿐이다. 다른 세 결과는 잘못된 승격 경로를 제거하고 다음
보조정리를 더 정확하게 만든다. 해결 수는 여전히 `0 / 4`다.
