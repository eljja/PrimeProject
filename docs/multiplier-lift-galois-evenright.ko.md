# TICKET-250: multiplier 도주·lift 추이성·Galois support·짝수 왼쪽 지수 분류

- 부모: TICKET-249
- `iteration_complete`: true
- `program_complete`: false
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- 분류: `exact_no_go` 2건, `partial_theorem` 2건
- 집중 문제: 강한 골드바흐 추측
- 네 상위 문제 상태: 모두 `open_not_proven`

TICKET-250은 프로젝트 내부 보조 결과 네 개를 증명한다. 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않는다. “회차 완료”는 이번 회차가 선언한 명제,
계산, 감사, 산출물이 완성됐다는 뜻이며 상위 추측 해결을 뜻하지 않는다.

## 재현 명령

```powershell
python scripts/ticket250_multiplier_lift_galois_evenright.py
python -m unittest tests.test_ticket250_multiplier_lift_galois_evenright -v
python scripts/verify_ticket250_structure.py
python scripts/verify_ticket249_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket250-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

생성기는 결정론적이며 난수 시드가 없다. 대수적 인증은 정수와
`Fraction`만 사용한다. JSON의 부동소수점 값은 표시용이며 증명의
전제가 아니다.

| 문제 | TICKET-250에서 판정한 정확한 명제 | 분류 | 상위 상태 |
|---|---|---|---|
| 리만 | 비compact multiplier `M_(x^2)`는 Legendre 도주를 막지만 중심 집중열에서는 여전히 coercivity를 잃는다 | `exact_no_go` | `open_not_proven` |
| 콜라츠 | 2와 3의 local Fermat-quotient lift는 추이적으로 움직이며 모든 lift fiber가 slope `[3:5]` 대표를 정확히 `q-1`개 포함한다 | `exact_no_go` | `open_not_proven` |
| 강한 골드바흐 | 소수 modulus의 모든 비상수 유리 residue vector는 모든 reduced frequency에서 Fourier 계수가 0이 아니고 Galois norm도 0이 아닌 정수다 | `partial_theorem` | `open_not_proven` |
| 쌍둥이 소수 | 왼쪽 지수가 짝수인 모든 right-active 쌍은 정확히 `25 -> 27`이다 | `partial_theorem` | `open_not_proven` |

## 1. 리만 가설

### A. 선언 명제: `NoncompactMultiplierLegendreEscapeInsufficiencyNoGo`

```text
H = L2_even([-1,1]),
Q0(f) = sum_(k>=0) |integral_(-1)^1 x^(2k) f(x) dx|^2,
phi_l = sqrt((2l+1)/2) P_l,
K = M_(x^2)
```

라 하자. `K`는 bounded, self-adjoint, noncompact이고 짝수
`l=2n`에 대해

```text
<K phi_l,phi_l>
 = (l+1)^2/((2l+1)(2l+3)) + l^2/((2l-1)(2l+1))
 -> 1/2.                                                   (RH-250a)
```

따라서 TICKET-249의 Legendre weak-null 도주는 막힌다. 그러나

```text
g_epsilon=(2 epsilon)^(-1/2)1_[-epsilon,epsilon]
```

에 대해

```text
||g_epsilon||=1,
<K g_epsilon,g_epsilon>=epsilon^2/3,
Q0(g_epsilon)<=2 epsilon/(1-epsilon^4)->0.                 (RH-250b)
```

그러므로 하나의 비compact 보정이 Legendre 열에서 양의 극한을 갖는다는
사실만으로 단위구 전체의 coercivity를 결론낼 수 없다.

### B-D. 수학적 논증과 추론 감사

Legendre 삼항 점화식으로 `x^2P_l`의 `P_l` 계수를 계산하면
(RH-250a)가 나온다. `[1/2,1]` 안의 서로 겹치지 않는 양의 측도
구간들의 정규화 indicator를 택하면 그 `K`-상은 서로 직교하고 각
norm이 적어도 `1/4`이므로 `K`는 compact가 아니다.

직접 적분하면

```text
|integral x^(2k)g_epsilon(x)dx|^2
 = 2 epsilon^(4k+1)/(2k+1)^2.
```

`(2k+1)^2>=1`로 낮춰 기하급수를 합하면 (RH-250b)를 얻는다.
무한열 결론은 유한 계산에서 외삽하지 않는다.

### E-G. 적대적 검증과 재현 계산

`n=1,...,256`의 정확한 Legendre 행 9개와
`epsilon=1/2,...,1/4096`의 집중 경계 12개를 검사했다. 마지막
기댓값은 `525311/1050621`, `1/2`와의 거리는
`1/2101242`이다. 실패 0건.

- transcript SHA-256:
  `20099dd1cab1cbcfa5ef4863e9f3c115c9f59af2da902d05bdbe029b5a8c507b`.

### H-I. no-go 범위와 유한 계산 한계

폐기 경로는 “한 비compact multiplier의 Legendre 대각 극한이 양수이면
full-sphere coercivity가 성립한다”이다. 실제 Guinand-Weil 산술 form과
admissible closure는 통제하지 못했다. RH는 `open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

```text
ArithmeticWeilFormCoercivityAgainstOscillationAndConcentrationEscapes
```

## 2. 콜라츠 추측

### A. 선언 명제: `LocalFermatQuotientLiftTransitivityNoGo`

소수 `q>5`에 대해

```text
F_q(a)=(a^(q-1)-1)/q mod q,
A_k=2+kq, B_l=3+lq
```

라 하면

```text
F_q(a+kq)=F_q(a)-k/a mod q.                         (CO-250a)
```

따라서 `(k,l)->(F_q(A_k),F_q(B_l))`는 `F_q^2`의 전단사다.
0이 아닌 slope `[3:5]`에 놓이는 lift 쌍은 정확히 `q-1`개이며
`t!=0`마다 유일한 쌍은

```text
k=2(F_q(2)-3t), l=3(F_q(3)-5t).                    (CO-250b)
```

### B-D. 수학적 논증

`(a+kq)^(q-1)`을 `q^2`로 보아 일차항까지만 전개하고 Fermat
정리를 적용하면 (CO-250a)가 된다. 두 좌표는 affine permutation이며,
목표 `(3t,5t)`를 대입하면 (CO-250b)가 되어 각 `t`마다 정확히 한
쌍을 준다.

### E-G. 반례 탐색과 재현 계산

`q=7,11,23,101,251`의 lift 쌍 73,901개를 exact exhaustive
검사했다. 각 영상은 `q^2`개이고 목표 수는 항상 `q-1`이다.
실패 0건.

- transcript SHA-256:
  `08ee2ee2080e127c58f7120621b39d20213ce2f6cf71987aaf01c7099ad528c2`.

### H-I. no-go 범위와 유한 계산 한계

2와 3의 residue class와 lift-invariant local 정보만으로 `[3:5]`를
배제하는 경로를 정확히 폐기했다. 그러나 `q`가 변할 때 고정된
canonical 대표 2와 3의 실제 발생/회피는 결정하지 못했고 전체 Collatz
궤도도 통제하지 못한다. 콜라츠는 `open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

```text
CanonicalRepresentativeFermatQuotientDistributionBeyondLiftTransitivity
```

## 3. 강한 골드바흐 추측 — 이번 집중 문제

### A. 선언 명제: `PrimeModulusRationalFourierFullSupportAndNormBarrier`

`q>=5`가 소수이고 정수 `n_0,...,n_(q-1)`에 대해

```text
N=sum_r n_r, Delta_r=q n_r-N,
F(a)=sum_r Delta_r zeta_q^(ar)
```

라 하자. `n`이 비상수이면

```text
F(a)!=0  (a=1,...,q-1),                             (GB-250a)
product_(a=1)^(q-1)F(a)는 0이 아닌 정수다.          (GB-250b)
```

따라서 그 절댓값은 적어도 1이다. TICKET-249의 정확한 두-frequency
cosine spike는 `q>=5` 소수 modulus의 정수/유리 residue-count
vector로 실현될 수 없다.

### B-D. 수학적 논증과 경계 반례

`P(X)=sum Delta_rX^r`라 하자. reduced `a`에서
`P(zeta_q^a)=0`이면 최소다항식
`Phi_q=1+X+...+X^(q-1)`가 `P`를 나눈다. 차수 때문에
`P=cPhi_q`인데 `P(1)=0`, `Phi_q(1)=q`이므로 `c=0`이다.
이는 `n`이 비상수라는 가정과 모순이다. 모든 `F(a)`는 `F(1)`의
Galois conjugate이므로 그 곱은 0이 아닌 algebraic-integer norm이다.

소수 modulus 가정은 필수다. `q=4`에서 `[1,0,-1,0]`은
frequency 1,3에만 support를 갖는다. `q=3`의 `[2,-1,-1]`은
두 reduced frequency밖에 없다. 이 exact boundary model은 composite
modulus로의 무근거 확장을 차단한다.

### E-G. 재현 가능한 계산

`X=100,1000,10000,100000,1000000` 및
`q=5,7,11,13,17,19,23`의 prime residue-count vector 35개를
exact 검사했다. Cyclotomic norm은 정수 곱셈행렬과 Bareiss determinant로
계산했다. 모든 비상수 vector가 full reduced support와 nonzero norm을
가졌고 관측된 최소 절댓값은 250,000이다. 경계 반례 2개도 재현했다.
실패 0건.

- transcript SHA-256:
  `684fea0b7645dea69f080eddb985918605ef6db23fde35646689556c8cf5c5a1`.

### H-I. 부분정리 범위와 유한 계산 한계

Galois symmetry는 nonvanishing만 증명하며 upper anti-concentration을
주지 않는다. norm이 0이 아니라도 한 conjugate가 매우 작고 나머지가
클 수 있다. 유한 prime-count 검사는 점근 추정이 아니고 log-weighted
prime도 아니며 minor-arc saving을 증명하지 않는다. 강한 골드바흐는
`open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

```text
QuantitativePrimeCountFourierEnergyAntiConcentrationAtPrimeModuli
```

## 4. 쌍둥이 소수 추측

### A. 선언 명제: `AllBaseEvenLeftRightActiveClassification`

홀수 소수 `p,r`, `m>=1`, `ell>=2`에 대해

```text
p^(2m)+2=r^ell
```

의 유일한 해는

```text
(p,m,r,ell)=(5,1,3,3), 즉 25+2=27.                 (TP-250)
```

따라서 왼쪽 지수가 짝수인 right-active composite prime-power 쌍은
`25->27` 하나이고 scale count는 `1_[X>=25]`이다.

### B-D. 논증과 외부 정리 의존성

`ell=2`이면 modulo 8에서 좌변은 3이어서 홀수 제곱일 수 없다.
`ell>=3`이면 `x=p^m,y=r,n=ell`을 대입하여 `D=2`
generalized Lebesgue-Nagell 분류를 적용한다. 유일한 양의 해는
`x=5,y=3,n=3`이다.

proof DAG에는 다음 논문을 `external_theorem` 노드로 명시했다:
Y. Bugeaud, M. Mignotte, S. Siksek, *Compositio Mathematica* 142
(2006), <https://doi.org/10.1112/S0010437X05001739>.

### E-G. 재현 계산

`X=24`부터 `10,000,000`까지 9개 scale에서 prime-power support를
exact 열거했다. even-left count는 25에서 0에서 1로 바뀐 뒤 유지된다.
천만에서 전체 right-active count는 136이며 even-left 1개,
odd-left 135개다. 실패 0건.

- transcript SHA-256:
  `0cf8bd40771dca2cc7e0da725f6bffbaefb50d81c3d73d72731917568fa4dcda`.

### H-I. 부분정리 범위와 유한 계산 한계

all-scale even-left 분류는 외부 정리가 증명하고 유한 열거는 replay다.
odd-left subclass, 전체 소수쌍 상관, Type-II 하한은 통제하지 못했다.
쌍둥이 소수 추측은 `open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

```text
ScaleLocalOddLeftRightActiveContaminationBound
```

## Proof DAG와 완료 판정

각 트랙은 TICKET-249 proved 선행 노드, TICKET-250 proved 노드,
disproved 경로, open frontier 하나를 갖는다. Twin 트랙은 외부
Lebesgue-Nagell 노드가 하나 더 있다. 네 DAG는 모두 acyclic이다.

| 트랙 | 이번 proved 노드 | 폐기한 경로 | open frontier |
|---|---|---|---|
| RH | `NoncompactMultiplierLegendreEscapeInsufficiencyNoGo` | Legendre-only 비compact 검증 | `ArithmeticWeilFormCoercivityAgainstOscillationAndConcentrationEscapes` |
| Collatz | `LocalFermatQuotientLiftTransitivityNoGo` | lift-invariant local slope 배제 | `CanonicalRepresentativeFermatQuotientDistributionBeyondLiftTransitivity` |
| Goldbach | `PrimeModulusRationalFourierFullSupportAndNormBarrier` | exact two-spike의 유리 실현 | `QuantitativePrimeCountFourierEnergyAntiConcentrationAtPrimeModuli` |
| Twin | `AllBaseEvenLeftRightActiveClassification` | 추가 even-left 오염 후보 | `ScaleLocalOddLeftRightActiveContaminationBound` |

상위 추측 또는 그 부정에 도달한 DAG는 없다. 해결 후보도 없다.
TICKET-250은 한 회차로서는 완료됐지만 네 난제 연구 프로그램은
완료되지 않았다.
