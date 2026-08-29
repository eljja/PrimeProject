# TICKET-255: packet 합계, 불완전 복원 불가능성, 홀수 반사, 세 소수 Thue obstruction

## 주장 경계

TICKET-255는 프로젝트 내부 보조명제 네 개를 증명한다. 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않았다. 해결 수는 여전히 `0 / 4`이다. 이번
deep-focus는 Twin 트랙의 지수 17 디오판토스 obstruction이다.

재현 명령은 다음과 같다.

```text
python scripts/ticket255_aggregate_incomplete_odd_local.py
python -m unittest tests.test_ticket255_aggregate_incomplete_odd_local -v
python scripts/verify_ticket255_structure.py
python -m unittest discover -s tests
python scripts/verify_open_problem_structure.py
node --check assets/ticket255-open-problem.js
node --check assets/open-problems.js
```

증명 certificate에는 정수와 `Fraction`만 쓴다. 난수는 없고 JSON의
`display_float`는 표시용일 뿐 증명에 쓰지 않는다.

| 문제 | 이번 정확 명제 | 분류 | 원래 문제 상태 |
|---|---|---|---|
| RH | `StrictDiagonalDominanceNecessityNoGo` | `exact_no_go` | `open_not_proven` |
| Collatz | `IncompleteAdditiveCharacterExactRecoveryNoGo` | `exact_no_go` | `open_not_proven` |
| 강한 Goldbach | `OddCyclotomicReflectionPrimePrefixExclusion` | `partial_theorem` | `open_not_proven` |
| Twin Prime | `ThreePrimeLocalObstructionReducesSeventeenTwistsToTwo` | `partial_theorem` | `open_not_proven` |

## 1. 리만 가설 트랙

### A. 정확한 명제

모든 정수 `L>=3`에 대해 전부 1인 행렬을 `J_L`이라 하고
`A_L=J_L+I_L/L`이라 하자. `A_L`은 양의 정부호이고 정규화한 all-ones
packet `d_L`은

```text
<d_L,A_L d_L>=L+1/L>0
```

을 만족하지만, `1+1/L<=L-1`이므로 엄격 대각우세가 아니다. 따라서
양의 packet 에너지에 엄격 대각우세가 필요하지 않다.

### B-D. 정의와 증명

`J_L`의 all-ones 방향 고윳값은 `L`, 직교여공간 고윳값은 0이다.
따라서 `A_L`의 고윳값은 `L+1/L`과 `1/L`이고 둘 다 양수다. 한 행의
대각은 `1+1/L`, 절대 비대각합은 `L-1`이다. 이것으로 모든 `L>=3`의
명제가 끝난다.

### E-G. 반례·계산·해석

`L=3,5,7,9,15,31,63,127` 여덟 rational block을 exact arithmetic으로
재생했고 실패는 0이다. 이 반례는 대각우세의 **필요성**만 부정한다.
실제 Guinand-Weil block이 우연히 대각우세일 가능성이나 그것이 충분조건일
가능성은 부정하지 않는다.

### H-K. 한계·분류·간극·다음 보조정리

실제 Weil 행렬을 계산하지 않았다. 분류는 `exact_no_go`이다. 남은
간극은 실제 packet Rayleigh 합계의 직접 하한이며 다음 단일 보조정리는

```text
ActualWeilDirichletPacketAggregateRowSumHasRequiredLowerBound
```

이다. transcript SHA-256은
`2ba4e6b1090ad6d74f803dc96b1762f0e0cf5057bd0f11f12ee81036d8b99493`이다.

## 2. 콜라츠 트랙

### A. 정확한 명제

소수 `q`와 진부분집합 `H subset F_q`에 대해 모든 `D in F_q`에서

```text
1_(D=0)=sum_(h in H) a_h exp(2 pi i hD/q)
```

가 되게 하는 복소수 계수 `a_h`는 존재하지 않는다. 부호 있는 계수를
허용해도 진짜 불완전 additive-character support로 slope incidence를
점별 exact 복원할 수 없다.

### B-D. 정의와 증명

`F_q` 위 additive character `q`개는 함수공간의 직교기저다. 원점
점질량의 모든 Fourier 계수는 `1/q`이다. `H` 밖의 `h0`를 택하면
`H`-support 합의 `h0` 계수는 0이어서 모순이다. 계수의 부호나 복소수
여부와 무관하다.

### E-G. 적대적 재생과 해석

7부터 47까지 소수 12개 각각에서 nonzero 전체, lower half, quadratic
residue, zero-only 네 support를 검사했다. 48개 certificate가 누락 주파수의
`1/q`와 0을 exact rational로 비교했고 실패는 0이다.

### H-K. 한계·분류·간극·다음 보조정리

근사복원, one-sided majorant, canonical Fermat-quotient residue에서만의
복원은 막지 않는다. 분류는 `exact_no_go`이다. 다음 단일 보조정리는

```text
SignedIncompleteSlopeKernelHasControlledCanonicalErrorAndCrossPrimeCancellation
```

이다. transcript SHA-256은
`cc49768b5030292430f99a91e8eef1047ac66704a68a859ea1e06cd4b86a9293`이다.

## 3. 강한 골드바흐 트랙

### A. 정확한 명제

`q>=5`가 소수, `m`이 홀수, `q`가 `m`을 나누지 않는다고 하자.

```text
c_r=sum_(0<=j<=m, j congruent r mod q)(-1)^j binom(m,j)
```

라 두고 `t=1-c_0>0`, 모든 `r`에서 `c_r+t>=0`, `T=qt`를 가정한다.
`lambda_q(r,k)`를 `r mod q`인 `k`번째 소수의 전체 소수열 index라 하자.
강제 count는 `N*_(m mod q)=2t-1`이다. 따라서

```text
T<lambda_q(m mod q,2t-1)
```

이면 실제 첫 `T`개 소수 residue vector가 될 수 없다.

### B-D. 정의와 증명

`m`이 홀수이므로 `a_(m-j)=-a_j`이고 cyclic folding 뒤
`c_(m-r)=-c_r`이다. `r=0`을 넣으면 `c_(m mod q)=-c_0`, 따라서 shift
후 count는 `-c_0+(1-c_0)=2t-1`이다. 실제 prefix가 그 residue의
`(2t-1)`번째 소수보다 앞에서 끝나면 count는 최대 `2t-2`라서 TICKET-253
unique-prefix criterion과 모순이다.

### E-G. Exact 유한 certificate

`q in {5,7,11,13,17,19}`, 홀수 `1<=m<=160`의 480쌍을 스캔했다.
compatible non-q-divisible 행은 50개다. `T<=50,000`만 소수열을 exact
열거해 네 행을 인증했다.

| `(q,m)` | `t` | `T` | 강제 count | 실제 count | `lambda` index | 결과 |
|---|---:|---:|---:|---:|---:|---|
| `(5,9)` | 126 | 630 | 251 | 153 | 1,014 | 배제 |
| `(5,11)` | 451 | 2,255 | 901 | 561 | 3,633 | 배제 |
| `(7,13)` | 1,716 | 12,012 | 3,431 | 2,000 | 20,566 | 배제 |
| `(7,15)` | 6,420 | 44,940 | 12,839 | 7,464 | 77,008 | 배제 |

### H-K. 한계·분류·간극·다음 보조정리

나머지 46 compatible 행은 replay cap을 넘어서 계산으로 배제했다고
주장하지 않는다. 대수 정리는 threshold가 별도로 인증될 때만 적용된다.
`q|m`인 지수는 전혀 해결하지 않았다. 분류는 `partial_theorem`, 다음은

```text
QDivisibleCompatibleTailPrimePrefixExclusion
```

이다. transcript SHA-256은
`ab8cb879f9a4dbdc1825584e054a56687f770fc0b6c3a40f939be7f06dc2b3fb`이다.

## 4. 쌍둥이 소수 트랙: deep focus

### A. 정확한 명제

TICKET-254의 17개 `B_j(u,v)=1` 방정식을 `p=103,137,409`에서 줄이면
`j=1,16`만 남는다. 각 소수가 배제하는 twist는

```text
{0,3,6,7,8,9,10,11,14}
{0,4,5,7,8,9,10,12,13}
{0,2,15}
```

이다. 따라서 `x^2-2=y^17`의 양의 해가 있다면 두 twist 중 하나에서만
나와야 한다.

### B-D. Split-ring 증명

각 소수에서 `s^2=2`인 최소 `s`는 38, 31, 97이다. `2s`가 가역이므로

```text
u+v sqrt(2) -> (z_+,z_-)=(u+sv,u-sv)
```

는 전단사다. `epsilon_+=1+s`, `epsilon_-=1-s`라 하면 `B_j=1`은

```text
epsilon_+^j z_+^17-epsilon_-^j z_-^17=2s
```

와 동치다. 17제곱 residue multiplicity를 exact convolution하여 모든
`p^2` 쌍의 해 수를 센다. 세 zero set의 합집합이 15개 twist를 덮고
soluble set의 교집합은 정확히 `{1,16}`이다.

### E-G. 독립 감사와 no-go

split certificate는 `(u,v,j)` residue case 3,343,203개를 표현한다.
별도의 mod-103 direct enumeration `103^2*17`건이 첫 count vector를
그대로 재현한다. 두 생존 twist는 `B_j=1`만 보는 어떤 합동 sieve로도
제거할 수 없다. 실제 정수 witness가 있기 때문이다.

| `j` | `(u,v)` | `A_j` | `B_j` | reduced `y` | admissible? |
|---:|---|---:|---:|---:|---|
| 1 | `(1,0)` | 1 | 1 | -1 | 아니오 |
| 16 | `(-1,1)` | -1 | 1 | -1 | 아니오 |

두 점은 exact하지만 `y=-1`이어서 양의 해는 아니다. coefficient-only
합동 완료 경로에 대한 정확한 no-go이며, 15개 twist 배제 부분정리와
구분한다.

### H-K. 한계·분류·간극·다음 보조정리

local insolubility는 15개 방정식을 전역 배제하지만 local solubility는
정수해를 주지 않는다. `j=1,16`에서 `A_j>0` 및 reduced `y>0`인 정수점을
배제하지 못했다. 지수 17, right-even contamination, twin-prime 추측은
모두 미해결이다. 분류는 `partial_theorem`, 다음 단일 보조정리는

```text
TwoSurvivingUnitTwistsHaveNoAdmissibleIntegralPoint
```

이다. transcript SHA-256은
`3d89ca8e3ca658a6bff44a8e532a441a2be41ac89c5d8d46b2af84d8c84a6a63`이다.

## Proof DAG 및 해결 판정

각 DAG에는 TICKET-254 선행 노드, 새 proved 노드, exact finite replay,
disproved 경로, open frontier가 있고 모두 비순환이다. Twin 정리는 세
소수 finite certificate에 의존하며 나머지 보편 정리의 유한 재생은
정리의 결과다. 해결 경로에 `assumption`이나 `heuristic`은 없다. 그러나
네 원래 명제는 모두 `open_not_proven`, `iteration_complete=true`,
`program_complete=false`이다.
