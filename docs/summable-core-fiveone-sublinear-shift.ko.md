# TICKET-189: 합 가능한 코어, 다섯-1 순환, 소수 거듭제곱 제거

## 1. 주장 경계

TICKET-189는 TICKET-188에 남은 네 개의 열린 노드를 이어간다. 이번
티켓은 콜라츠 순환의 새로운 무한 계층 하나와, 세 개의 정확한 승격 또는
오염항 제거 정리를 증명한다. 리만 가설, 콜라츠 추측, 강한 골드바흐
추측, 쌍둥이 소수 추측 중 어느 것도 해결하지 않았고 반례도 찾지 못했다.

| 문제 | TICKET-189의 정확한 결과 | 폐기하거나 교정한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | `SummableFiniteCoreDriftConstructsCompatiblePositiveForm` (합 가능한 유한 코어 변동으로 양의 공통 형식 구성) | 인접 코어 차이가 0으로 간다는 사실만으로 수렴을 결론 | `PoleNeutralGuinandWeilFixedCoreDriftHasCertifiedSummableOperatorMajorantAndVanishingNegativeFloor` |
| 콜라츠 | `ExactlyFiveValuationOnesOtherwiseTwoCycleExclusion` (정확히 다섯 개가 1이고 나머지가 2인 순환 배제) | 유한 높이 열거를 모든 높이로 외삽 | `NoContractingValuationWordWithExactlySixOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| 골드바흐 | `ProperPrimePowerContaminationHasExplicitSublinearBudget` (진소수 거듭제곱 오염항의 명시적 준선형 예산) | 오염항이 준선형이라는 사실을 전체 합의 하한으로 오인 | `ExplicitMajorArcMainMinusMinorArcErrorExceedsSublinearPrimePowerBudgetForEveryLargeEvenTarget` |
| 쌍둥이 소수 | `ShiftTwoVonMangoldtPrimePowerContaminationBridge` (간격 2 폰 망골트 합의 소수 거듭제곱 제거 다리) | 오염항을 빼지 않고 양의 상관합에서 쌍둥이 소수를 결론 | `ShiftTwoVonMangoldtCorrelationHasPositiveLinearLowerBoundOnInfinitelyManyDyadicBlocks` |

재현 명령은 다음과 같다.

```powershell
D:\python\anaconda3\python.exe scripts\ticket189_corefive_sublinear_shift.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket189_corefive_sublinear_shift -v
```

주 기계 판독 자료는
`data/open-problem/ticket189-corefive-sublinear-shift.json`이다. 네 문제의
상태는 모두 `open_not_proven`, 즉 미해결이다.

## 2. 리만 가설

### 2.1 이번에 증명한 정확한 명제

`A_N`을 에르미트 행렬이라 하고, `A_N^[m]`을 고정된 앞쪽 `m x m`
코어라 하자. 다음을 가정한다.

```text
||A_(N+1)^[m] - A_N^[m]|| <= d_(N,m),
sum_{N=m}^infinity d_(N,m) < infinity.
```

그러면 각 고정 코어는 연산자 노름에서 에르미트 행렬 `Q_m`으로 수렴하며,

```text
||Q_m - A_N^[m]|| <= sum_{k=N}^infinity d_(k,m)
```

이라는 정량 오차가 성립한다. `Q_m`들은 서로 호환되는 주부분행렬이므로
유한 지지 수열 공간 `c_00` 위의 하나의 에르미트 형식 `Q`를 정의한다.
또한

```text
lambda_min(A_N) >= -eta_N,  eta_N -> 0
```

이면 `Q`는 `c_00`에서 양의 준정부호이다.

### 2.2 증명과 재현 계산

변동 상계의 합이 유한하므로 각 고정 코어는 유한 차원 연산자 노름에서
코시 수열이다. 변동의 꼬리합을 더하면 위 오차 상계가 나온다. 코어 제한과
극한은 교환되므로 `Q_(m+1)`의 앞쪽 코어가 `Q_m`이다. 코시 끼워넣기
정리로 `lambda_min(A_N^[m])>=lambda_min(A_N)`이고, 노름 극한과
`eta_N->0`을 적용하면 각 `Q_m`이 양의 준정부호이다.

정확 유리수 재현 모형은

```text
A_N = diag(1+1/N, 1/2+1/N, ..., 1/N+1/N)
```

이다. 고정 코어 오차는 정확히 `1/N`, 인접 변동은 `1/(N(N+1))`, 남은
변동의 합은 정확히 `1/N`이며 전체 최소 고윳값은 `2/N>0`이다.

### 2.3 폐기한 경로와 남은 간극

스칼라 코어 `A_N=H_N`은 인접 차이가 `1/(N+1)->0`이지만 조화급수라서
발산한다. 따라서 “인접 변동이 0으로 간다”는 수렴 조건이 아니다. 합
가능한 상계나 다른 인증된 코시 모듈러스가 필요하다.

이 정리는 추상적인 승격 정리이다. 실제 극점 중화 Guinand-Weil 행렬에
대해 합 가능한 코어 변동과 사라지는 음의 하한을 증명하지 못했다. 최근의
나사 함수와 유한 절단 연구도 리만 가설 증명을 주장하지 않는다:
[Suzuki 2026](https://arxiv.org/abs/2606.09096),
[Kim 등 2026](https://arxiv.org/abs/2607.24830),
[Groskin 2026](https://arxiv.org/abs/2605.20224).

## 3. 콜라츠 추측

### 3.1 이번에 증명한 정확한 명제

가속 콜라츠 사상의 양의 정수 순환 중 `v_2(3n+1)` 값이 정확히 다섯
번 1이고 나머지는 모두 2인 순환은 없다. 원시 주기와 반복된 비원시
주기를 모두 포함한다.

### 3.2 정확한 아핀 산술

다섯 개의 1 사이 양의 순환 간격을 `a,b,c,d,e`라 하고, 회전하여 `e`가
가장 크도록 한다. `h=a+b+c+d+e`일 때 순환 분모와 순서 있는 아핀
분자는 다음과 같다.

```text
D = 4^h/32 - 3^h,

B = 4^h/32 - 3^(h-1)
    + 4^a 3^(h-a-1)
    + 2*4^(a+b-1) 3^(c+d+e-1)
    + 4^(a+b+c-1) 3^(d+e-1)
    + 2*4^(a+b+c+d-2) 3^(e-1).
```

정수 순환에는 `D | B`가 필요하다. 수축 영역은 `h=13`부터 시작한다.
또한 `B>D`이고 `B,D`는 모두 홀수이다.

### 3.3 모든 높이에 대한 배제

`u=3/4`라 두면 `B<3D`의 충분조건은

```text
(32/3)u^(h-a) + (16/3)u^(c+d+e) + (8/3)u^(d+e)
+ (4/3)u^e + (256/3)u^h < 2
```

이다. 최대 간격 회전으로

```text
e >= ceil(h/5),
d+e >= ceil(h/5)+1,
c+d+e >= ceil(h/5)+2,
h-a >= ceil((h+3)/2)
```

를 얻는다. 따라서 모든 단어에 공통인 상계는 `h`에 대해 감소하며
`h=22`에서

```text
131155153587 / 68719476736 < 2
```

이다. 그러므로 모든 `h>=22`에서 `1<B/D<3`이다. 나누어떨어진다면 이
몫은 1과 3 사이의 홀수 정수여야 하지만 그런 정수는 없다. 남은 범위는

```text
sum_{h=13}^{21} binomial(h,5) = 72897
```

개의 단어를 정확히 전수 검사했고 나눗셈 해는 0개였다. 각 높이의 나머지
기록 해시, 닫힌식 검증, 순환 회전 항등식은 JSON에 저장한다.

### 3.4 한계

이번 결과는 하나의 무한 주기 계층만 닫는다. 1이 여섯 개 이상인 단어,
3 이상의 valuation(2진 지수)을 포함한 단어, 비주기 발산은 여전히
열려 있다. 최근 패리티 벡터와 2진 유령 순환 연구도 기호적 국소 조건과
양의 정수 궤도를 구분한다:
[Niu 2026](https://arxiv.org/abs/2605.13886),
[Dhiman-Pandey 2026](https://arxiv.org/abs/2601.12772).

## 4. 강한 골드바흐 추측

### 4.1 이번에 증명한 정확한 명제

`A(N)`을 `N` 이하의 서로 다른 진소수 거듭제곱, 즉 지수가 2 이상인
`p^k`의 개수라 하고 `L=floor(log_2 N)`이라 하자. 그러면

```text
A(N) <= sum_{k=2}^L floor(N^(1/k))
     <= floor(sqrt N) + max(L-2,0) floor(N^(1/3)).
```

TICKET-188의 분해와 결합하면 이항 폰 망골트 합의 소수 거듭제곱 오염항은

```text
E_pp(N) <= 2 A(N)(log N)^2 = o(N)
```

이다. 따라서 어떤 고정 `c>0`에 대해 모든 충분히 큰 짝수에서
`R_Lambda(N)>=cN`을 인증하면, 결국 오염항을 이기고 소수-소수 질량이
양수가 된다. 남은 유한 범위는 정확 계산으로 확인할 수 있다.

### 4.2 증명, 폐기한 경로, 남은 간극

모든 `p^k<=N`은 `k`번째 근 항에 포함된다. 제곱 항은 `sqrt N` 이하이고,
`k>=3`인 각 항은 `N^(1/3)` 이하이며 그런 지수는 최대 `L-2`개이다.
오염 상계를 `N`으로 나누면

```text
O(log^2(N)/sqrt(N) + log^3(N)/N^(2/3)) -> 0
```

이다.

그러나 이는 오차항의 상계일 뿐 전체 합의 양의 하한이 아니다. 유한 계산에서
비율이 작아지는 현상은 진단 자료이며 모든 짝수에 대한 소호-오차 제어를
대체하지 못한다. 현재의 예외 집합 결과도 이 전칭 간극을 닫지 않는다:
[Grimmelt-Bhowmik 2026](https://arxiv.org/abs/2607.27282).
가중치와 소수 거듭제곱을 분리하는 이유는
[Helfgott 2015](https://arxiv.org/abs/1501.05438)의 원 방법에서도
확인할 수 있다.

## 5. 쌍둥이 소수 추측

### 5.1 이번에 증명한 정확한 명제

`X=2^j`인 이진 구간에서

```text
S_Lambda(X) = sum_{X<=n<2X} Lambda(n)Lambda(n+2)
            = P_2(X) + E_2pp(X)
```

로 분해한다. `P_2`는 실제 쌍둥이 소수 항이고, 나머지 오염항은

```text
0 <= E_2pp(X) <= 2 A(2X+2)(log(2X+2))^2 = o(X)
```

이다. 따라서 전체 상관합의 인증 하한이 이 예산보다 크면 그 구간에
쌍둥이 소수가 있다. 특히 고정 `c>0`에 대해 무한히 많은 비유계 `j`에서
`S_Lambda(2^j)>=c2^j`이면 쌍둥이 소수 추측이 따라온다.

### 5.2 정확한 반박 예와 남은 간극

오염된 항은 `n` 또는 `n+2`가 진소수 거듭제곱이므로 가능한 시작점이 최대
`2A(2X+2)`개이고 각 가중치는 `log^2(2X+2)` 이하이다. 그러나 상관합의
양성만으로는 쌍둥이 소수를 결론 내릴 수 없다. `n=25`이면

```text
(25,27) = (5^2,3^3),
Lambda(25)Lambda(27) = log(5)log(3) > 0
```

이지만 두 끝점 모두 소수가 아니다.

유한 이진 구간 자료는 정확 분해를 재현할 뿐 독립적인 Type I/II 추정을
제공하지 않는다. 무한히 많은 비유계 구간에서 양의 선형 하한을 증명하지
못했다. 이 분포론적 간극은 소수 생성 체 연구가 요구하는 핵심 입력이다:
[Ford-Maynard 2024](https://arxiv.org/abs/2407.14368).

## 6. 증명 상태 결론

TICKET-189는 네 개의 정확한 명제를 증명한다. 그중 콜라츠 결과만 새로운
무한 산술 계층을 닫는다. 리만 결과는 충분한 수렴 계약을 제시하고,
골드바흐와 쌍둥이 소수는 하나의 명시적 준선형 소수 거듭제곱 제거 경계를
공유한다. 네 난제의 해결 수는 여전히 `0 / 4`이다.
