# TICKET-256: Cesàro lag 합, 최적 불완전 핵, q-배수 반사, GL2 생존 분기 환원

- 부모 회차: TICKET-255
- 심층 초점: 쌍둥이 소수 트랙의 지수 17 디오판토스 obstruction
- `iteration_complete`: true
- `program_complete`: false
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- 결과 분류: 네 문제 모두 `partial_theorem`
- 네 원 명제 상태: 모두 `open_not_proven`

TICKET-256은 프로젝트 내부의 보조정리 네 개를 증명했다. 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 가운데 어느 것도
증명하거나 반증하지 않았다. 이번 회차 완료는 선언 명제와 산출물의
검증 완료만 뜻하며 원 문제 해결을 뜻하지 않는다.

## 재현 계약

```powershell
python scripts/ticket256_cesaro_kernel_qdiv_gl2.py
python -m unittest tests.test_ticket256_cesaro_kernel_qdiv_gl2 -v
python scripts/verify_ticket256_structure.py
python -m unittest discover -s tests
python scripts/verify_open_problem_structure.py
node --check assets/ticket256-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

생성기는 결정적이다. 증명 certificate는 정수와 `Fraction`만 사용한다.
복소 단위근은 정확한 나머지 지수로만 기록하며 부동소수점 복소수를
증명에 사용하지 않는다. JSON의 `display_float`는 표시용이다. 난수 seed는
없다.

| 문제 | 이번 정확 명제 | 결과 분류 | 원 문제 상태 |
|---|---|---|---|
| 리만 | `ToeplitzPacketCesaroLagPartialSumCriterion` | `partial_theorem` | `open_not_proven` |
| 콜라츠 | `SharpIncompleteKernelErrorAndDecayOnlyPrimeAverage` | `partial_theorem` | `open_not_proven` |
| 강한 골드바흐 | `QDivisibleReflectionAsymmetryPrimePrefixExclusion` | `partial_theorem` | `open_not_proven` |
| 쌍둥이 소수 | `SurvivingTwistGL2EquivalenceAndSingleAbsoluteBranchReduction` | `partial_theorem` | `open_not_proven` |

## 1. 리만 가설 트랙

### A. 정확한 명제

실수열 `(a_k)_(k>=0)`에 대해

```text
T_L=(a_|r-s|)_(0<=r,s<L),
d_L=L^(-1/2)(1,...,1),
E_L=<d_L,T_L d_L>,
S_n=a_0+2 sum_(k=1)^n a_k
```

라 하자. 모든 정수 `L>=1`에 대해

```text
E_L = (1/L) sum_(n=0)^(L-1) S_n.                  (RH-256)
```

따라서 모든 `n`에서 `S_n>=c`이면 모든 패킷 크기에서 `E_L>=c`이다.
하지만 이 조건은 필요조건이 아니다. 무한 lag 열

```text
a_0=1, a_1=-1, a_2=1, a_k=0 (k>=3)
```

은 `S_1=-1`이지만 `E_1=1`, `E_2=0`, `E_L=(L-2)/L>=0 (L>=3)`이다.

### B-D. 정의와 증명

lag 0은 이차합에 `L`회, lag `k>=1`은 `2(L-k)`회 나타난다. 그러므로

```text
E_L=a_0+2 sum_(k=1)^(L-1)(1-k/L)a_k.
```

한편 `S_n`의 합에서 합 순서를 바꾸면

```text
sum_(n=0)^(L-1)S_n
=L a_0+2 sum_(k=1)^(L-1)(L-k)a_k
=L E_L
```

이 되어 항등식과 충분조건이 증명된다. 반례의 부분합은
`1,-1,1,1,...`이므로 그 유한 Cesàro 평균이 위의 비음수 에너지다.
이는 필요성만 정확히 반증하며 충분성은 반증하지 않는다.

### E-G. 적대적 계산과 해석

`L=1,...,12`에서 lag 계수, 모든 `S_n`, 직접 계산한 패킷 에너지,
Cesàro 평균을 유리수로 독립 재계산했다. 실패 `0`, 최소 부분합 `-1`이다.

- 계산 복잡도: 재생은 `O(sum L)`, 전 `L` 증명은 대수적;
- 검사 사례: 12개;
- transcript SHA-256:
  `a4d61abe3161c28b13f5f333e2fae644f2c9171107dde94d92e38adc6b8615d1`.

### H-I. 논리·유한 한계와 분류

12행은 전 `L` 항등식을 재생할 뿐이다. 실제 Guinand-Weil lag의 부호나
크기는 계산하지 않았고 signed 소수 거듭제곱 항과 archimedean 항의
하계를 주지 않는다. 따라서 영점 배제 결론은 없다. 결과 분류는
`partial_theorem`, RH는 `open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

실제 패킷 lag의 스칼라 부분합에 필요한 하계를 증명해야 한다.

```text
ActualWeilSymmetricLagPartialSumsHaveUniformLowerBound
```

## 2. 콜라츠 추측 트랙

### A. 정확한 명제

소수 `q`, 빠진 주파수 `h_0 in F_q`, `D in F_q`에 대해

```text
K_(q,h_0)(D)=q^(-1) sum_(h!=h_0) exp(2 pi i hD/q)
```

라 하면

```text
K_(q,h_0)(D)=delta_0(D)-q^(-1)exp(2 pi i h_0D/q),
||delta_0-K_(q,h_0)||_infinity=1/q.                (CO-256)
```

`h_0`를 support에서 뺀 모든 근사 핵 가운데 `1/q`는 minimax 최적이다.
정준 나머지

```text
D_q=5F_q(2)-3F_q(3) mod q
```

에서도 비정규화 error의 소수 Cesàro 평균은 절댓값으로 0에 간다. 다만
이것은 `1/q` 크기의 자동 감쇠이지 정규화한 위상의 상쇄 정리가 아니다.

### B-D. 증명

`delta_0`의 완전 additive-character 전개에서 `h_0` 항 하나를 빼면
점별 error와 그 크기가 즉시 나온다. 임의의 `H`-supported 근사에서는
빠진 주파수의 error Fourier 계수가 `1/q`로 남는다. 정규화 Fourier
계수의 절댓값은 sup norm 이하이므로 더 작은 균일 error는 불가능하다.

선택한 소수를 `q_j`라 하면 `q_j>=j+1`이므로

```text
(1/n)sum_(j<=n)1/q_j <= (1/n)sum_(j<=n)1/(j+1) -> 0.
```

삼각부등식이 정준 error 평균에도 그대로 적용된다. 이 증명은 `D_q`의
산술 분포를 전혀 쓰지 않으며 `q`를 곱우면 자동 감쇠가 사라진다.

### E-G. 적대적 계산과 해석

`7<=q<=97`의 소수 22개에서 `F_q(2)`, `F_q(3)`, `D_q`, 정확한 `1/q`,
누적 유리수 평균을 계산했다. 단위근은 `D_q mod q` 지수로 저장했다.
실패는 0이다.

- 복잡도: 재생용 modular exponentiation `O(sum log q)`;
- transcript SHA-256:
  `e50be6fa63328562b64c1fa1023ad706493a60e47d84705d24aebec05d412de3`.

### H-I. 폐기 경계와 분류

폐기: 비정규화 `O(1/q)` 평균의 감소를 cross-prime 산술 상쇄라고 부르는
경로. 정규화 위상, 정준 projective slope의 출현·회피, 임의 Collatz 궤도는
전혀 제어하지 못한다. 결과 분류는 `partial_theorem`, Collatz는
`open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

자동 감쇠를 제거한 뒤의 산술 상쇄가 실제 남은 의무다.

```text
RenormalizedCanonicalSlopePhasesHaveNontrivialCrossPrimeCancellation
```

## 3. 강한 골드바흐 추측 트랙

### A. 정확한 명제

소수 `q>=5`, `q|m`에 대해 `(1-X)^m`을 `X^q-1`로 접어

```text
c_r=sum_(j congruent r mod q)(-1)^j binom(m,j)
```

라 하자. `t=1-c_0`이고 TICKET-253 호환 조건

```text
t>0, c_r+t>=0 (모든 r)
```

이 성립하면 `m`은 짝수이다. 또한

```text
c_(-r)=c_r,
N*_r=c_r+t=N*_(-r).                                (GB-256)
```

따라서 `T=qt`번째까지의 실제 소수 잔여류 벡터가 어느 `r`에서라도
`N_r(T)!=N_(-r)(T)`이면 이 후보 tail과 같을 수 없다.

### B-D. 홀수 지수 obstruction과 반사 증명

`j -> m-j` 대합은 `c_(m-r)=(-1)^m c_r`를 준다. `q|m`이고 `m`이
홀수라고 가정하면 `c_(-r)=-c_r`, `c_0=0`, `t=1`이다. `r`과 `-r`의
호환 조건을 함께 쓰면 모든 정수 `c_r`가 `[-1,1]`에 있으므로
`sum c_r^2<=q`이다.

하지만 cyclic Parseval 항등식은

```text
sum_r c_r^2=q^(-1)sum_a|1-zeta_q^a|^(2m)
```

이고 `a=(q-1)/2`에서 제곱 크기는

```text
4cos^2(pi/(2q))>=4cos^2(pi/10)=(5+sqrt(5))/2>3.
```

`m>=q>=5`, `3^q>q^2`이므로 오른쪽은 `q`보다 커져 모순이다. 따라서
`m`은 짝수이고 동일 대합에서 반사 대칭이 나온다. 실제 prefix 비대칭은
TICKET-253의 유일 prefix 기준과 모순된다.

### E-G. exact prefix certificate

`q in {5,7,11,13,17,19}`와 `q`의 양의 배수 `m<=160`을 스캔하고,
`T<=100,000`인 경우만 소수 prefix를 열거했다. 전체 97쌍, 홀수 49쌍,
호환 25쌍, 홀수 호환 0쌍이며 아래 두 bounded 행이 배제됐다.

| q | m | t | T | 강제 대칭 count | 실제 첫 T개 count | 반사 차이 |
|---:|---:|---:|---:|---|---|---|
| 5 | 10 | 251 | 1,255 | `[1,451,176,176,451]` | `[1,313,313,317,311]` | `[0,2,-4,4,-2]` |
| 7 | 14 | 3,431 | 24,017 | `[1,6420,1520,4068,4068,1520,6420]` | `[1,3993,3991,4003,3998,4016,4015]` | `[0,-22,-25,5,-5,25,22]` |

가장 큰 prefix의 마지막 소수는 `274783`, 실패는 0이다.

- 복잡도: 계수 folding `O(sum m)`과 최대 prefix까지 결정적 trial division;
- transcript SHA-256:
  `6ded0f179c955a164110a035c40971e60b948905edbb9c3377af7ac985ef8619`.

### H-I. 유한 한계와 분류

홀수 지수 불가능성과 조건부 반사 배제는 무한 대수 정리다. 실제 소수
prefix는 두 개만 열거했다. 나머지 23개 호환 행은 이미 범위를 넘으며
`m>160`은 스캔하지 않았다. 그러므로 모든 짝수 `q`-배수 tail의 실제
비대칭을 결론 낼 수 없다. 결과 분류는 `partial_theorem`, 강한
골드바흐 추측은 `open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

```text
EveryQDivisibleCompatibleEvenTailHasPrimePrefixReflectionAsymmetry
```

## 4. 쌍둥이 소수 추측 트랙 — 심층 초점

### A. 정확한 명제

`epsilon=1+sqrt(2)`이고

```text
epsilon^j(u+v sqrt(2))^17=A_j(u,v)+B_j(u,v)sqrt(2)
```

라 하자. TICKET-255의 두 생존 twist `j=1,16`에 대해

```text
T(u,v)=(-u-2v,u+v)
```

를 정의하면 `T in GL_2(Z)`이고 모든 정수 `(u,v)`에서

```text
B_16(T(u,v))= B_1(u,v),
A_16(T(u,v))=-A_1(u,v),
N(T(u,v))   =-N(u,v).                               (TP-256)
```

따라서 두 twist의 admissible 점 합집합은 단일 absolute branch

```text
B_1(u,v)=1,  -(u^2-2v^2)>0,  x=|A_1(u,v)|
```

와 전단사다.

### B-D. 대수적 증명

```text
T    = [[-1,-2],[ 1, 1]], det(T)=1,
T^-1 = [[ 1, 2],[-1,-1]].
```

`alpha=u+v sqrt(2)`라 하면 직접 곱셈으로
`T(alpha)=epsilon^(-1)conjugate(alpha)`이다. 또한
`conjugate(epsilon)=-epsilon^(-1)`이므로

```text
epsilon^16 T(alpha)^17=-conjugate(epsilon alpha^17).
```

여기서 A/B 항등식이 나온다. `N(epsilon)=-1`이므로 norm 항등식도
성립한다. 양의 `A_1`은 twist 1, 음의 `A_1`은 T로 옮긴 양의 `A_16`에
해당하고 정수 역변환이 전사성을 준다. `B_1=1`, `-N(alpha)>0`이면

```text
A_1^2-2=(-N(alpha))^17>0
```

이어서 `A_1!=0`, 따라서 절댓값 분기가 정확하다.

### E-G. 적대적 재생

`[-64,64]^2`의 모든 정수쌍에서 twist 1과 16을 독립 quadratic-ring
거듭제곱으로 계산하고 정·역변환을 함께 검사했다. 특히 가장 위험한
부호 오류를 막기 위해 `N(T(u,v))=-N(u,v)`를 직접 회귀 검사한다.

- exact grid: 16,641개;
- 항등식 실패: 0;
- box 안의 `B_1=1` 점: `(1,0)` 하나;
- 그 점의 reduced `y`: `-1`, 따라서 부적격;
- box 안 admissible 점: 0;
- 복잡도: 반경 R에서 `O(R^2 log 17)`;
- transcript SHA-256:
  `b16cc63924090d6e214ecdaaa8c47018fced6bae337cc3445ed9cbd3a85eb7a9`.

### H-I. 논리·유한 한계와 분류

GL2 전단사는 전 정수쌍에서 증명됐지만 box는 단지 재생이다. box 안에
점이 없다는 사실은 전 정수 배제가 아니다. 두 global branch를 하나로
줄였을 뿐 `B_1=1`을 풀지 못했고 `x^2-2=y^17`의 지수 17을 배제하지
못했다. 따라서 twin-prime proxy도 닫히지 않는다. 결과 분류는
`partial_theorem`, 쌍둥이 소수 추측은 `open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

```text
SingleCoefficientOneBranchHasNoNegativeNormIntegralPoint
```

## Proof DAG와 완료 경계

각 트랙은 TICKET-255 선행 정리, TICKET-256 증명 정리, `computed_finite`
재생, `disproved` shortcut, `open` 다음 보조정리의 5개 노드로 이루어진
비순환 DAG다. `open`, `assumption`, `heuristic` 노드를 proved로 올리지
않았다. 기계 감사는 DAG 4개, 열린 frontier 4개, 후보 해결 0개,
추측 해결 0개, 재생 실패 0개를 기록한다.

이번 회차는 완료되었지만 해당 추측은 해결되지 않았다.
