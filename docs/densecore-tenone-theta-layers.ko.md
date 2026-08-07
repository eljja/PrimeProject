# TICKET-194: 조밀 코어 확장, 열-1 순환, 세타 층

## 1. 주장 경계

TICKET-194는 네 개의 중간 정리를 증명합니다. 리만 가설, 콜라츠 추측,
강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도 해결하지 않았고 부모
추측의 반례도 찾지 못했습니다. 이번에 새로 완전히 닫은 무한 부분족은
가속 콜라츠 valuation에서 정확히 열 항이 1이고 나머지 항이 모두 2인
순환층입니다.

| 문제 | 이번에 증명한 정확한 결과 | 폐기한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | `UniformlyBoundedDenseCoreQuadraticConvergenceExtendsEverywhere` (균일 유계 조밀 코어 이차형식 수렴의 전체공간 확장) | 조밀 코어에서의 양성·단조성을 균일 유계성 대신 사용하는 경로 | `PoleNeutralWeilFiniteSectionsAreUniformlyBoundedAndConvergeOnADenseCore` |
| 콜라츠 | `ExactlyTenValuationOnesOtherwiseTwoCycleExclusion` (정확히 열 번의 1과 나머지 2인 순환 배제) | 열-1/나머지-2 부분족을 순환 후보로 사용하는 경로 | `NoContractingValuationWordWithExactlyElevenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| 골드바흐 | `OddPrimePowerThetaLayerCompressionAndBinaryMassClassification` (홀수 소수거듭제곱 세타층 압축과 이진 질량 분류) | `O(sqrt(N) log^2 N)`을 본질적인 오염 규모로 보는 경로 | `BinaryCorrelationExceedsThetaLayerPrimePowerEnvelopeForEveryLargeEvenTarget` |
| 쌍둥이 소수 | `OddPrimePowerIntervalThetaLayerCompression` (구간 홀수 소수거듭제곱 세타층 압축) | `O(sqrt(X) log^2 X)`을 본질적인 간격-2 오염 규모로 보는 경로 | `ShiftTwoCorrelationExceedsThetaLayerOddLocalEnvelopeOnInfinitelyManyDyadicBlocks` |

재현 명령은 다음과 같습니다.

```powershell
D:\python\anaconda3\python.exe scripts\ticket194_densecore_tenone_theta_layers.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket194_densecore_tenone_theta_layers -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

통합 기계 판독 결과는
`data/open-problem/ticket194-densecore-tenone-theta-layers.json`에 있습니다.
네 시도 모두 `open_not_proven`, 즉 아직 증명되지 않은 상태이며 해결 수는
`0 / 4`입니다.

## 2. 리만 가설

### 2.1 선언한 명제

복소 힐베르트 공간 `H` 위의 연속 Hermitian 이차형식 `q_n`과 연관 형식
`B_n`을 생각하고 `D`가 `H`에서 조밀하다고 하겠습니다. 다음 두 조건을
가정합니다.

```text
sup_n ||B_n|| <= M < infinity,
q_n(u)는 모든 u in D에서 수렴한다.
```

그러면 `B_n(x,y)`와 `q_n(x)`는 모든 `x,y in H`에서 수렴합니다. 극한은
노름이 `M` 이하인 유계 Hermitian 형식이고 양성도 보존됩니다.

### 2.2 증명

복소 polarization 공식으로 `D` 위의 대각 수렴을 `D x D` 위의
`B_n(u,v)` 수렴으로 바꿉니다. `u,v in D`가 `x,y in H`를 근사하면

```text
|(B_n-B_m)(x,y)-(B_n-B_m)(u,v)|
 <= 2M(||x-u|| ||y|| + ||u|| ||y-v||).
```

먼저 `u,v`를 골라 오른쪽을 작게 만들고, 그 뒤 코어 수렴으로 `n,m`을
고르면 전체공간에서 Cauchy 조건이 성립합니다. 동일한 균일 노름 상계가
극한으로 전달됩니다.

### 2.3 더 강한 조밀 코어 no-go

`H=l^2`, `D=c_00`에서

```text
q_n(x)=sum_(k<=n) k|x_k|^2
```

로 둡니다. 이 형식들은 양성이고 단조 증가하며 모든 유한 지지 벡터에서는
결국 일정해집니다. 그러나 `||B_n||=n`입니다. 다음 벡터는 `l^2`에
속합니다.

```text
|x_(2^j)|^2=2^(-j),  나머지는 0.
```

이 벡터의 노름 제곱은 1이지만 `q_(2^J)(x)=J`이므로 발산합니다. 따라서
양성, 단조성, 조밀 코어 수렴을 모두 합쳐도 균일 연산자 상계를 대신할 수
없습니다.

### 2.4 남은 간극

실제 pole-neutral Weil 유한 절단이 한 admissible Hilbert completion에서
균일 유계이고 조밀 코어에서 수렴한다는 사실은 증명하지 못했습니다. 이번
정리는 그 두 산술적 전제가 주어진 뒤의 확장 단계만 완성합니다.

## 3. 콜라츠 추측

### 3.1 선언한 명제

가속 콜라츠 순환의 valuation 주기에 정확히 열 항이 1이고 나머지 항이
모두 2인 양의 순환은 존재하지 않습니다. 원시 주기뿐 아니라 같은 주기를
반복해 표시한 비원시 주기도 포함합니다.

### 3.2 수축 가능 구간

길이가 `h`이면 valuation 합은 `2h-10`이고 affine 분모는

```text
D_h=2^(2h-10)-3^h
```

입니다. `h<=24`에서는 양수가 아니고 `h=25`부터 양수입니다. 열 개의
1 중 하나가 첫 위치에 오도록 회전해도 affine 나눗셈 가능성은 보존되므로
후보를 잃지 않습니다.

### 3.3 9개 경계항 분해와 정확한 5+4 MITM

정규화 위치를

```text
0=p_0<p_1<...<p_9<h
```

로 쓰면 recurrence 분자는 `h`에만 의존하는 상수 하나와 각 위치에만
의존하는 경계항 아홉 개의 합으로 정확히 분리됩니다. 구현은
`h=10,...,16`의 정규화 단어 8,008개 모두에서 이 식과 원래 affine
recurrence가 일치함을 확인합니다.

수축 가능한 유한 구간 `h=25,...,38`에서는 왼쪽 경계항 다섯 개와 오른쪽
네 개로 나눕니다. 오른쪽 첫 위치보다 마지막 위치가 작은 왼쪽 tuple만
활성화하므로 다음 개수의 모든 단어를 정확히 대표합니다.

```text
sum_(h=25)^38 C(h-1,9)
 = C(38,10)-C(24,10)
 = 470,772,500.
```

실제 계산은 왼쪽 tuple 2,626,085개와 오른쪽 질의 225,708개만 필요합니다.
임의 정밀도 정수와 정확한 나머지 hash membership을 사용했고 나눗셈
적중은 0개입니다. 각 `h`의 SHA-256 transcript도 저장합니다.

### 3.4 무한 꼬리

자명하지 않은 양의 홀수 순환의 모든 상태는 3 이상입니다. 한 주기의 비율을
곱하면

```text
1 <= 2^10(5/6)^h = 1024(5/6)^h
```

를 얻습니다. 오른쪽은 `h=38`에서 1보다 크지만 `h=39`부터 1보다 작고
계속 감소합니다. 따라서 유한 MITM과 해석적 꼬리가 모든 길이를 덮습니다.

### 3.5 남은 간극

1이 열한 번 이상 나타나는 층, 3 이상의 valuation, 비주기 발산은 여전히
남습니다. 순환 부분족을 계속 닫는 것만으로 모든 콜라츠 궤도의 수렴이
증명되지는 않습니다.

## 4. 강한 골드바흐 추측

### 4.1 정확한 세타층 항등식

`W_odd(Y)`를 `p^k<=Y`, `k>=2`인 홀수 proper prime power에 대해 `log p`를
합한 값이라고 하겠습니다. 그러면

```text
W_odd(Y)=sum_(k>=2) theta_odd(floor(Y^(1/k)))
```

가 정확히 성립합니다. 유한한 소수 밑 합과 지수 합의 순서를 바꾸면 바로
얻습니다. 코드는 부동소수점 거듭제곱이 아니라 정확한 정수 `k`제곱근을
사용하므로 경계의 소수거듭제곱을 빠뜨리지 않습니다.

### 4.2 해석적 규모

여기서 사용하는 외부 해석 입력은 고전적인 Chebyshev 상계
`theta(t)=O(t)`뿐입니다. `k=2` 층은 `O(sqrt Y)`이고 나머지
`O(log Y)`개 층은 각각 `O(Y^(1/3))` 이하입니다. 또한

```text
Y^(1/3) log Y = O(sqrt Y)
```

이므로 `W_odd(Y)=O(sqrt Y)`입니다. TICKET-193의 정확한 parity 오염식에
대입하면 소수거듭제곱 오염은 `O(sqrt(N) log N)`입니다. 이전의 초등적
상계에서 로그 하나를 제거하지만 이 결과 자체는 이진 상관의 하한이
아닙니다.

### 4.3 2의 거듭제곱 질량의 정확한 이진 분류

짝수 `N>=6`에 대해 이진 표현의 유일성으로 다음을 얻습니다.

- `N`이 2의 거듭제곱이면 순서쌍 한 개,
- `N`의 이진 표현에 1비트가 정확히 두 개면 순서쌍 두 개,
- 그 밖에는 순서쌍이 없습니다.

각 순서쌍의 von Mangoldt 가중치는 `(log 2)^2`입니다. 직접 열거와 이진
규칙은 감사한 모든 표적에서 일치합니다.

### 4.4 유한 계산과 남은 간극

`2^10,...,2^20`의 11개 표적에서 세타층이 홀수 proper-power 질량을 정확히
복원하고 전체 상관은 정확한 오염식을 넘습니다. 이 유한 접두부는 충분히
큰 모든 짝수에서 같은 부등식이 성립함을 증명하지 않습니다. 그 보편적
점별 하한이 다음 보조정리입니다.

## 5. 쌍둥이 소수 추측

### 5.1 정확한 구간 항등식

두 누적 세타층 항등식을 빼면 모든 정수 구간 `[A,B)`에 대해

```text
W_odd([A,B))
 = sum_(k>=2) [
     theta_odd(floor((B-1)^(1/k)))
     -theta_odd(floor((A-1)^(1/k)))
   ]
```

을 얻습니다. 이를 `[X,2X)`와 `[X+2,2X+2)`에 적용하면 TICKET-193의
odd-only 오염량을 정확한 세타층으로 표현합니다. 두 누적 질량이
`O(sqrt X)`이므로 간격-2 오염식은 `O(sqrt X log X)`입니다.

### 5.2 유한 계산과 남은 간극

`X=2^j`, `j=4,...,19`의 16개 블록에서 왼쪽 구간과 2만큼 이동한 오른쪽
구간의 세타층 복원이 모두 정확하며 상관이 정확한 국소 오염식을 넘습니다.
유한한 블록 목록으로 무한히 많은 성공 블록을 증명할 수는 없습니다. 이
오염식을 넘는 하한을 무한히 증가하는 블록열에서 얻지 못했습니다.

## 6. 종합

TICKET-194는 서로 다른 세 양화사 축소를 명시합니다. 균일 유계성은 조밀
코어 수렴을 완비 힐베르트 공간으로 확장합니다. 경계항 분리는 4억 7천만
개의 콜라츠 단어를 coverage 손실 없이 압축합니다. 세타층은 소수거듭제곱
열거를 정확한 정수근 산술로 바꾸고 올바른 sublinear 오염 규모를
드러냅니다. 남은 전제들은 이전보다 날카로워졌지만 유한 계산으로 얻은 것은
아닙니다.
