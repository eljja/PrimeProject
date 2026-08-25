# TICKET-240: 경로 교정, Wieferich 깊이, 소수 가중 CRT

## 주장 경계

TICKET-240은 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 **증명하거나 반증하지 않았습니다**. 정확한 부분정리 또는
불가능성 정리 네 개를 증명했고, 유한 계산은 범위가 제한된 증거로 따로
표시했으며, 문제마다 다음 단일 증명 의무를 하나씩 남겼습니다.

기계 판독 결과:
`data/open-problem/ticket240-route-corrections-wieferich-prime-crt.json`.

재현 및 검증 명령:

```powershell
python scripts/ticket240_route_corrections_wieferich_prime_crt.py
python -m unittest tests.test_ticket240_route_corrections_wieferich_prime_crt -v
python scripts/verify_ticket240_structure.py
```

## 결과 요약

| 문제 | TICKET-240의 정확한 결과 | 폐기하거나 우선순위를 낮춘 경로 | 상태 |
|---|---|---|---|
| 리만 가설 | Cotlar 제곱근 중첩 합이 발산해도 Gram 하한은 균일하게 양수일 수 있음 | 절대 Cotlar 가합성을 필요조건 또는 부호 상쇄 도구로 보는 경로 | `open_not_proven` |
| 콜라츠 | run-block 결함을 유리수 Wieferich 깊이 차로 정확히 환원, `20,000,000`까지 검사 | 유한 범위 무후보 결과를 전 소수 정리로 승격하는 경로 | `open_not_proven` |
| 골드바흐 | 음의 DC를 넘는 부호 잔차는 정수성 때문에 표현 존재와 정확히 동치 | 부호 잔차 여유를 더 약한 중간 목표로 보는 경로 | `open_not_proven` |
| 쌍둥이 소수 | 모든 유한 CRT 패턴에 소수/합성수-후속 쌍이 무한히 존재 | 한쪽 소수 가중치와 유한 CRT 정보만으로 쌍둥이 질량을 얻는 경로 | `open_not_proven` |

## 1. 리만 가설 트랙

### 이번에 증명한 명제

`0<C<1`에 대해

```text
R_ij = 1/(1+|i-j|),
G    = (1-C)I + C R
```

로 둡니다. 모든 유한 절단에서 `G_J >= (1-C)I`입니다. `G`를 Gram
행렬로 갖는 단위벡터를 `w_j`, 그 1차원 사영을 `P_j`라고 하면

```text
||P_i P_j||^(1/2) = sqrt(C)/sqrt(1+|i-j|)  (i != j)
```

이고 Cotlar 행합은 발산합니다.

### 논증과 경로 교정

`(n+1)^(-1)=integral_0^1 t^n dt`이므로 `R`은
`[t^|i-j|]`의 양의 혼합입니다. `0<=t<1`에서 이 Toeplitz kernel의
이차형식은 음이 아닌 Poisson kernel에 대한
`|sum_j z_j exp(ij theta)|^2`의 적분이고, `t=1`은 극한으로 얻습니다.
따라서 양의 준정부호이며 Gram 하한이 나옵니다. 반면 제곱근 중첩
행합은 `sum d^(-1/2)`을 포함하므로 발산합니다. 또한 사영 norm은
내적의 위상을 버리므로 Weil 형식에 필요한 부호 상쇄를 자체적으로
기록하지 못합니다.

즉, 실제 산술 shell이 Cotlar 추정을 만족한다면 여전히 유용한
**충분조건**이지만, 절대 operator norm 합은 부호 상쇄를 담지 못하고
양성의 필요조건도 아닙니다. 다음 핵심 보조정리는
`ArithmeticWeilSignedBlockOperatorSymbolHasUniformPositiveLowerBoundAfterCommonModeRemoval`
입니다.

`J=16,...,1024`를 계산했고 `J=1024`에서 Cotlar 합은 `60.5829977`이지만
정확한 Gram 하한은 계속 `1/2`입니다. 이는 추상 반례족이며 zeta 영점
정보를 포함하지 않습니다.

## 2. 콜라츠 추측 트랙

### 이번에 증명한 명제

홀수 소수 `q>3`에 대해 TICKET-239의 정의를 유지합니다.

```text
ell_q = lcm(ord_q(32/27), ord_q(2/3)),
a_q   = v_q(32^ell_q-27^ell_q),
c_q   = v_q(2^ell_q-3^ell_q)
```

`r=(q-1)/ell_q`라 두면 각 `(U,V)`에 대해 `q`는 홀수이고, `q | U-V`, `q`는 `UV`를 나누지 않으며 `1<=r<q`입니다. 따라서 LTE의 `v_q(U^r-V^r)=v_q(U-V)+v_q(r)=v_q(U-V)`에서

```text
a_q = v_q(32^(q-1)-27^(q-1)),
c_q = v_q(2^(q-1)-3^(q-1))
```

를 얻습니다. 따라서 defect `a_q-c_q`는 정확히 유리수 Wieferich 깊이의
차입니다. `F_q(b)=(b^(q-1)-1)/q mod q`라 하면

```text
a_q >= 2  iff  5F_q(2)-3F_q(3) = 0 mod q,
c_q >= 2  iff   F_q(2)- F_q(3) = 0 mod q
```

입니다.

### 계산과 한계

`5<=q<=20,000,000`의 소수 `1,270,605`개를 모두 검사했습니다.
`a_q>=2`인 소수는 없었고 `c_q>=2`인 소수는 `q=23` 하나였습니다. 따라서
이 유한 범위에는 양의 defect가 없습니다. 그러나 이것은 전 소수에 대한
증명이 아닙니다.

새 열린 보조정리는
`RationalWieferichDepthDominationFor32Over27Versus2Over3AtEveryOddPrime`
입니다. 이것을 증명해도 binary run-block finite-palette 경로만 닫히며,
일반 necklace와 비주기 궤도 하강은 남습니다.

## 3. 강한 골드바흐 추측 트랙

### 이번에 증명한 명제

TICKET-239의 반사 항등식을

```text
R_A(h)=DC_A+S_A(h),    DC_A=|A|^2/M
```

로 씁니다. `R_A(h)`는 음이 아닌 정수이므로

```text
S_A(h)>-DC_A  iff  R_A(h)>=1
```

입니다. 더 일반적으로 고정된 `0<eta<=1`에 대해
`S_A(h)>=eta-DC_A`도 같은 표현 존재 명제와 동치입니다.

### 의미와 남은 간극

따라서 TICKET-239의 “부호 있는 Fourier 잔차가 음의 DC를 균일한 여유로
넘는다”는 목표는 더 쉬운 중간 명제가 아닙니다. 정수성 때문에 이미
점별 표현 존재와 같습니다. 유효한 다음 목표는 양의 산술 주항과 서로
독립적으로 검증 가능한 오차를 분리해야 합니다. 다만 아래 정리도
이진 골드바흐의 핵심 parity 장벽을 사실상 그대로 포함할 수 있으며,
TICKET-240은 이것이 상위 추측보다 쉽다고 주장하지 않습니다.

`BinaryPrimeMajorArcMainTermMinusAllExplicitErrorsIsAtLeastOneForEverySufficientlyLargeEvenTarget`

`X=10^3,...,10^7`의 15개 prime-window 행을 검사했습니다. `X=1000`, 배율
`1`인 제한 창에서는 반사 계수가 0입니다. 이는 선택한 창 안의 0일 뿐,
골드바흐 반례가 아닙니다.

## 4. 쌍둥이 소수 추측 트랙

### 이번에 증명한 명제

`3`보다 큰 소수의 임의 유한 집합 `Q`를 잡고
`1_(q does not divide p+2)`의 모든 이진 패턴을 지정합니다. 0 bit에는
`p=-2 mod q`, 1 bit에는 `p=1 mod q`를 배정하고, `Q` 밖의 새 소수
`ell`에 대해 `p=-2 mod ell`도 요구합니다.

CRT는 `ell product(Q)`에 대한 기약 잉여류를 만들고, Dirichlet 정리는
그 잉여류에 소수 `p`가 무한히 많음을 보장합니다. 동시에 충분히 큰
모든 `p+2`는 `ell`로 나누어져 합성수입니다.

따라서 **한쪽만 소수로 가중한** 완전한 유한 CRT 패턴 정보도 쌍둥이
소수 질량을 보장하지 않습니다. 첫 항이 실제 소수라는 점에서
TICKET-239의 균등 합성수쌍 모형보다 강한 no-go입니다.

`Q={5,7,11}`의 8개 패턴 모두에 정확한 CRT 증인을 기록했습니다. 실제
소수 `p in [X/2,X]`의 중심화 CRT Gram도 계산했습니다. `X=10^7`에서
12개 좌표의 경험적 유효랭크는 `11.9998924`입니다. 이 유한
근직교성으로 무한성을 결론 내릴 수는 없습니다.

다음 보조정리는
`ParityBreakingTwoSidedLambdaLambdaMainTermDominatesGrowingCRTErrorOnCofinalDyadicBlocks`
입니다.
이 양측 추정은 쌍둥이 소수 추측의 핵심 parity 장애를 포함할 수 있으며,
유한 Gram 행에서 이 정리를 유도했다고 주장하지 않습니다.

## 네 트랙의 결론

TICKET-240은 잘못 설정된 중간 목표 세 개를 제거하고 하나를 정밀화했습니다.

1. 절대 Cotlar 합은 부호 있는 Weil 양성이 아닙니다.
2. 콜라츠 defect는 단순 order scan이 아니라 유리수 Wieferich 깊이 비교입니다.
3. 골드바흐의 음의 DC 여유는 이미 정수 표현 양성 그 자체입니다.
4. 한쪽 소수성과 모든 유한 CRT 패턴도 합성수 후속항을 배제하지 못합니다.

네 추측은 모두 `open_not_proven`이고 기계 판독 해결 개수는 0입니다.

## 1차 연구 기준

- [Clay Mathematics Institute: 리만 가설](https://www.claymath.org/millennium/riemann-hypothesis/)
- [Tao, Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)
- [Sondow, Fermat quotients and Wieferich primes](https://arxiv.org/abs/1110.3113)
- [Helfgott, The ternary Goldbach problem](https://arxiv.org/abs/1501.05438)
- [Maynard, Small gaps between primes](https://arxiv.org/abs/1311.4600)

이 문헌은 용어와 학계의 현재 경계를 확인하기 위한 기준입니다. 위 네
프로젝트 정리를 해당 문헌의 기존 결과라고 주장하지 않습니다.
