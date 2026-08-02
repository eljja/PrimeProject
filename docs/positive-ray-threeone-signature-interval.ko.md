# TICKET-187: 유한 Weil 인증 출처, 세-1 콜라츠 순환, 생존 서명, 양자화 구간

## 1. 주장 경계

TICKET-187은 TICKET-186의 네 미해결 노드를 이어간다. 콜라츠에서는 새로운
무한 순환 부분족 하나를 완전히 배제하고, 나머지 세 문제에서는 인증 또는
정보의 정확한 경계를 증명한다. 리만 가설, 콜라츠 추측, 강한 골드바흐 추측,
쌍둥이 소수 추측 중 해결된 문제는 없다.

| 문제 | 이번에 확정한 결과 | 폐기·교정한 경로 | 다음 단일 보조정리 |
|---|---|---|---|
| 리만 | `PublishedFiniteWeilLDLTProvenanceAndOneSectionNoGo` (공개된 유한 Weil LDLT 출처 감사와 단일 절단 불충분성) | 보고된 유한 양성 블록 하나를 전역 Weil 양성으로 승격 | `CofinalPoleNeutralGuinandWeilIntervalLDLCertificatesHaveVanishingNegativeDefect` |
| 콜라츠 | `ExactlyThreeValuationOnesOtherwiseTwoCycleExclusion` (정확히 세 개의 valuation 1, 나머지 2인 모든 순환 배제) | 남은 모든 길이를 유한 열거로 대신 | `NoContractingValuationWordWithExactlyFourOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| 골드바흐 | `SignedSubhorizonSurvivorSignatureIndistinguishability` (부호를 허용해도 동일한 인수 지평 아래 생존 서명은 구분 불가) | 같은 roughness bit에 부호·비선형 처리를 추가하면 소수성 정보가 복구된다는 가정 | `SignedVonMangoldtSubhorizonResidualIsBelowExplicitMajorMainForEveryLargeEvenTarget` |
| 쌍둥이 소수 | `QuantizedTwinProjectorIntervalRoundingCertificate` (양자화 projector의 정확한 구간 반올림 인증) | `Delta in 4Z`를 사용하기 전에 해석적 하계가 4까지 도달해야 한다는 요구 | `CertifiedStrictlyPositiveTwinProjectorLowerEndpointOnInfinitelyManyPredeclaredDyadicBlocks` |

재현 명령은 다음과 같다.

```powershell
D:\python\anaconda3\python.exe scripts\ticket187_positive_ray_threeone_signature_interval.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket187_positive_ray_threeone_signature_interval -v
```

대표 기계 판독 파일은
`data/open-problem/ticket187-positive-ray-threeone-signature-interval.json`이다.
네 문제의 상태는 모두 `open_not_proven`, 즉 미해결이다.

## 2. 리만 가설

### 2.1 이번에 확인한 정확한 명제

Groskin의 유한 Guinand-Weil 연구에 포함된 고정된 provenance 파일은
`c=100`, `N=200`인 cutoff-free 블록에 대해 다음 interval `LDL^T` 결과를
보고한다.

| 항목 | 공개 파일의 값 |
|---|---:|
| 차원 | 401 |
| 정밀도 | 9,000 bit |
| 양의 pivot | 401 |
| 음의 pivot | 0 |
| 판정 불능 pivot | 없음 |
| 양의 정부호 인증 보고 | 참 |

TICKET-187은 원본 URL과 SHA-256을 고정하고 이 필드들의 내부 일관성을
검사한다. 그러나 PrimeProject가 9000-bit Arb 계산 자체를 다시 실행한 것은
아니다. 따라서 이것은 공개 인증서의 출처·내용 감사이지 독립 interval 증명이
아니다.

같은 공개 패키지의 `c=29`, `N=6` pole-neutral 벡터는 다음 두 양의 수치값을
제공한다.

```text
닫힌식 경로       = 0.028981466814873948251427313471228345
source-side 경로  = 0.028981466814884184353882396894187551
두 값의 차이      = 1.0236102455...e-14
보고된 source tail 잔여 상계 = 1.07788e-12
```

원본의 `guard_K`, `guard_g`는 함수의 닫힌식과 수치적분을 비교한 값이다.
이차형식 값의 엄밀한 구간 반경이 아니다. 따라서 이 행은 수치 재생으로만
기록하며 interval certificate라고 부르지 않는다.

### 2.2 단일 유한 절단의 정확한 no-go

공개된 유한 양의 정부호 인증을 그대로 받아들여도 전역 양성은 나오지 않는다.
임의의 양의 정부호 유한행렬 `M`에 대해

```text
diag(M, -1)
```

은 기존 인증 공간에서는 `M`과 완전히 같지만 새로운 직교 방향에서는 음수다.
따라서 하나의 유한 차원 결과로는 부족하며, 하나의 명시적인 조밀한
pole-neutral core를 따라가는 cofinal 절단열과 올바른 형식 극한이 필요하다.

### 2.3 남은 간극

다음 보조정리는 한 cofinal pole-neutral Guinand-Weil 절단열 전체에서 독립
재생 가능한 interval `LDL^T` 인증을 만들고, 인증된 음의 결손이 0으로 감을
보여야 한다. 현재의 provenance 감사와 한 벡터의 양의 수치값은 전역 Weil
비음성이나 임계선 밖 영점 배제를 증명하지 않는다.

1차 출처는 [Groskin의 finite Guinand-Weil dictionary 논문](https://arxiv.org/abs/2607.02828)이다.
선택한 공개 필드는 CC BY 4.0에 따라 출처를 표시했으며, 저자의 보증을
의미하지 않는다.

## 3. 콜라츠 추측

### 3.1 선언 명제

가속 홀수 콜라츠 사상에는 valuation 주기에서 정확히 세 항만 `1`이고 나머지
항이 모두 `2`인 양의 순환이 없다. 원시 주기와 비원시 반복 주기를 모두
포함한다.

순환 회전 뒤 valuation word를 다음처럼 쓴다.

```text
w(a,b,c) = (1, 2^(a-1), 1, 2^(b-1), 1, 2^(c-1)),
a,b,c >= 1, h=a+b+c.
```

세 순환 간격 중 가장 큰 것을 `c`로 오게 회전한다. 수축 범위 `h>=8`에서는
항상 `c>=3`이다.

### 3.2 정확한 affine 닫힌식

word를 합성하면 분자와 분모는 정확히

```text
B = 2^(2h-3) - 3^(h-1)
    + 4^a 3^(h-a-1)
    + 2*4^(a+b-1) 3^(c-1),

D = 2^(2h-3) - 3^h
```

가 된다. `D>0`인 범위는 정확히 `h>=8`이다. 또한

```text
B-D = 2*3^(h-1) + 4^a 3^(h-a-1)
      + 2*4^(a+b-1) 3^(c-1) > 0
```

이고 `B,D`는 모두 홀수다.

### 3.3 모든 큰 길이를 닫는 부등식

`u=3/4`, `Q=4^h/8`이라 두면 `B<3D`는 다음 부등식과 같다.

```text
(8/3)u^(b+c) + (4/3)u^c + (64/3)u^h < 2.       (1)
```

`c>=3`, `b+c>=4`이므로 앞의 두 항은 최대

```text
(8/3)(3/4)^4 + (4/3)(3/4)^3 = 45/32
```

이다. `h=13`에서 마지막 항은

```text
(64/3)(3/4)^13 = 531441/1048576 < 19/32
```

이고 이후 계속 감소한다. 따라서 `h>=13`에서 항상 `1<B/D<3`이다.
만약 `D`가 `B`를 나누면 몫은 1과 3 사이의 홀수 정수여야 하는데 그런 정수는
없다.

순환 회전도 안전하다. 첫 valuation이 `v`일 때 회전한 분자를 `B_shift`라 하면

```text
2^v B_shift = 3B + D
```

이다. `D`는 홀수이므로 `D|B` 여부는 회전해도 보존된다.

### 3.4 유한 예외의 완전 검사

남은 수축 길이 `h=8,...,12`에는

```text
sum C(h,3) = 56+84+120+165+220 = 645
```

개의 valuation word가 있다. Python의 정확한 정수 연산으로 모두 검사했으며
나눗셈 적중은 0개다. 각 길이는 모든 위치와 나머지 transcript의 SHA-256을
저장한다. 유한 계산은 해석 부등식 아래의 유한 예외만 닫으며 무한 범위로
외삽되지 않는다.

### 3.5 남은 간극

이는 실제로 새로운 무한 순환 부분족을 닫은 결과다. 그러나 `1`이 네 개 이상인
word, valuation이 `3` 이상인 경우, 비주기 발산 자연수 궤도는 남는다. 다음
단일 목표는 정확히 네 개의 `1`, 나머지 `2`인 word 전체의 affine 나눗셈
배제다.

## 4. 강한 골드바흐 추측

### 4.1 선언 명제

소수쌍 표현과 나쁜 홀수 후보쌍이 모두 있는 짝수 `N`을 고정한다. 다음을
정의한다.

```text
tau_N   = 나쁜 쌍의 최소소인수 gate 중 최댓값,
rho_N   = 소수쌍 표현에서 작은 끝점의 최댓값,
sigma_N = min(tau_N, rho_N).
```

모든 정수 깊이 `Y<sigma_N`에서 소수쌍 하나와 나쁜 합성수 포함 쌍 하나가
동일한 작은 인수 생존 서명을 갖는다.

### 4.2 증명과 강화된 no-go

`tau_N`을 실현하는 나쁜 쌍과 `rho_N`을 실현하는 소수쌍을 고른다. 두 쌍은
`sigma_N`보다 작은 모든 깊이에서 trial divisor로 제거되지 않는다. 따라서
두 서명은 같은 all-one vector다. 동일한 입력에는 어떤 결정함수도 동일한
출력을 낸다.

따라서 TICKET-186의 비음수 가중치 no-go보다 강하다. 임의의 부호 가중치,
비선형 분류기, 그 밖의 어떤 후처리를 사용해도 **같은 truncated roughness
bit만 재사용한다면** 두 witness를 정확히 구분할 수 없다.

| `N` | `sigma_N` | 구분 불가능한 마지막 `Y` | 소수쌍 수 | 나쁜 쌍 수 |
|---:|---:|---:|---:|---:|
| 100 | 7 | 6 | 6 | 18 |
| 500 | 19 | 18 | 13 | 111 |
| 1,000 | 29 | 28 | 28 | 221 |
| 5,000 | 67 | 66 | 76 | 1,173 |
| 10,000 | 89 | 88 | 127 | 2,372 |
| 50,000 | 223 | 222 | 450 | 12,049 |
| 100,000 | 311 | 310 | 810 | 24,189 |

이 표는 이미 유한 소수쌍 표현이 있는 목표를 사용한다. 따라서 새로운
골드바흐 사례를 증명하는 표가 아니라 정보 충분성의 실패를 재생하는 표다.

### 4.3 남은 간극

다음 단계는 roughness transcript에 없던 정보를 추가해야 한다. 예를 들어
von Mangoldt 가중 진폭이나 목표 정렬 위상을 사용하고, 그 signed residual이
모든 충분히 큰 짝수에서 명시적인 양의 major main보다 작음을 증명해야 한다.
[Grimmelt와 Bhowmik의 2026년 exceptional-set 연구](https://arxiv.org/abs/2607.27282)는
이 every-target 결론을 주지 않는다.

## 5. 쌍둥이 소수 추측

### 5.1 선언 명제

정확한 cubic-rough 지지집합에서

```text
Delta = A00-A10-A01+A11 = 4C
```

이고 `C`는 블록의 음이 아닌 정수 쌍둥이 소수 개수다. 엄밀한 닫힌 구간
`[L,U]`가 `Delta`를 포함하면 가능한 `C`의 범위는 정확히

```text
ceil(max(L,0)/4) <= C <= floor(U/4).              (2)
```

이다. 따라서

1. `L>0`이면 `L<4`여도 `C>=1`이 인증된다.
2. `U<4`이면 `C=0`이 인증된다.
3. `[0,4]`는 `C=0`과 `C=1`을 모두 허용하며 이 경계는 sharp하다.

### 5.2 증명

`[L,U]`와 격자 `4 Z_{>=0}`의 교집합을 구한 뒤 4로 나누면 된다. 천장함수와
바닥함수가 식 (2)를 정확히 준다. 4만 포함하는 구간, 0만 포함하는 구간,
0과 4를 모두 포함하는 구간이 각각 양성·영·모호성의 sharpness를 보인다.

따라서 해석적 목표는 “하단이 4 이상”에서 “하단이 엄밀히 0보다 큼”으로
낮아진다. 정수 양자화가 마지막 4단위 승격을 수행한다.

`X=10^3,10^4,10^5,10^6`의 실제 cubic-rough ledger에 반 단위 구간을 씌워
직접 twin count를 모두 정확히 복원했다. 이 유한 행들은 식의 일관성 검사이며
무한히 많은 양의 블록을 증명하지 않는다.

### 5.3 남은 간극

무한히 많은 미리 선언한 unbounded block에서 양의 하단을 주는 산술 추정은
아직 없다. 다음 보조정리는 최소 계약 `L_X>0`을 만족하는 parity-sensitive
Type I/II 추정이어야 한다. 구간 반올림은 그 해석적 추정을 만들어 주지 않는다.
[Ford와 Maynard의 prime-producing sieve 연구](https://arxiv.org/abs/2407.14368)가
필요한 Type I/II 맥락을 제공하지만 쌍둥이 소수 추측을 증명하지 않는다.

## 6. Proof DAG와 최종 경계

```text
리만 T186 전역 Weil 비음성 목표
  -> 공개 유한 LDL provenance 고정, 독립 재실행은 아님 [감사]
  -> 유한 양성 절단 하나로 전역 양성을 얻을 수 없음 [no-go 증명]
  -> cofinal pole-neutral interval-LDL + 소멸 음의 결손 [열림]

콜라츠 T186 정확히 세-1 목표
  -> 정확히 세-1/나머지-2인 모든 순환 배제 [증명]
  -> 정확히 네-1/나머지-2인 affine 나눗셈 배제 [열림]

골드바흐 T186 signed survivor 목표
  -> 같은 subhorizon 서명은 어떤 후처리로도 구분 불가 [증명]
  -> von Mangoldt signed residual < every-target major main [열림]

쌍둥이 소수 T186 4단위 문턱
  -> 정확한 구간-격자 반올림과 [0,4] sharpness [증명]
  -> 무한히 많은 dyadic block의 엄밀한 양의 하단 [열림]
```

완전한 증명이나 반례는 없다. 이번의 실제 새 산술 진전은 세-1 콜라츠 순환
부분족 전체 배제다. 리만 결과는 외부 출처 감사와 유한 절단 no-go이고,
골드바흐·쌍둥이 소수 결과는 더 정확한 정보·인증 계약이지 존재 정리가 아니다.
