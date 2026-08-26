# TICKET-249: compact 보정·projective Fermat quotient·Parseval spike·활성 거듭제곱 분류

- `iteration_complete`: true
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- `new_partial_theorem_count`: 2
- `exact_no_go_count`: 2
- `stagnated_problem_count`: 0
- deep focus: 쌍둥이 소수 추측
- parent: TICKET-248
- 프로그램 상태: `open_not_proven`

TICKET-249는 프로젝트 내부 보조 결과 네 개를 증명한다. 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않았다.

## 재현 계약

```powershell
python scripts/ticket249_compact_projective_parseval_lebesgue.py
python -m unittest tests.test_ticket249_compact_projective_parseval_lebesgue -v
python scripts/verify_ticket249_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket249-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

생성기는 결정적이며 random seed는 없다. 유한 증명 certificate는 정수 또는
`Fraction`만 사용한다. JSON의 부동소수점 값은 표시용일 뿐이다. Goldbach
certificate에서도 삼각함수 부동소수점 계산을 쓰지 않는다.

| 문제 | 이번에 판정한 정확한 명제 | 분류 | 원 추측 상태 |
|---|---|---|---|
| 리만 | 전체 even `L2` 모형에서 compact off-diagonal 보정은 TICKET-248 Legendre 도주열의 coercivity 소실을 복구하지 못한다 | `exact_no_go` | `open_not_proven` |
| 콜라츠 | separated generalized-Wieferich 조건은 정확히 0이 아닌 projective Fermat-quotient 점 `[3:5]`이다 | `partial_theorem` | `open_not_proven` |
| 강한 골드바흐 | 중심 first-jet Parseval 에너지는 두 reduced numerator에 정확히 집중될 수 있으므로 Parseval만으로 균일 제어를 만들 수 없다 | `exact_no_go` | `open_not_proven` |
| 쌍둥이 소수 | 밑이 `3`이 아닌 왼쪽 활성 짝수 지수 오염은 `(25,27)` 하나뿐이다 | `partial_theorem` | `open_not_proven` |

## 1. 리만 가설

### A. 정확한 명제: `CompactOffDiagonalMomentCoercivityNoGo`

다음을 정의한다.

```text
H=L2_even([-1,1]),
f_n=sqrt((4n+1)/2) P_(2n),
Q0(f)=sum_(k>=0) |integral_(-1)^1 x^(2k)f(x)dx|^2.
```

모든 bounded compact 연산자 `K:H->H`에 대해

```text
||f_n||=1,
Q0(f_n)<=11/n,
<Kf_n,f_n> -> 0.                                  (RH-249)
```

따라서 모든 `f in H`에서

```text
Q0(f)+Re<Kf,f> >= c||f||^2
```

를 만족하는 `c>0`은 존재하지 않는다.

### B-D. 정의·증명·추론 근거

Legendre 직교성으로 `(f_n)`은 정규직교열이고 따라서 약하게 0으로
수렴한다. compact 연산자는 bounded weak-null 열을 norm-null 열로 보낸다.
그렇지 않다면 `Kf_n`의 norm 수렴 부분열이 0이 아닌 극한을 가져야 하지만,
boundedness와 약수렴으로 그 극한의 모든 내적은 0이므로 모순이다. 따라서

```text
|<Kf_n,f_n>| <= ||Kf_n|| -> 0.
```

TICKET-248의 해석적 정리 `Q0(f_n)<=11/n`과 결합해 coercivity 식에
대입하면 `c<=0`이 되어 모순이다.

### E-G. 적대적·재현 가능 계산

`n=2,4,8,16,32,64,128,256`에서 `f_n`을 앞의 `n`개 정규화 even
Legendre 모드에 투영하면 에너지가 정확히 0이다. 각 `n`의 첫 여덟 개
비영 모멘트 에너지를 유리수로 합산해 `11/n` 이하임도 검사한다.

- 행: 8;
- 산술: exact rational;
- 실패: 0;
- transcript SHA-256:
  `eaaa5e2eccd9fa1fcb32504240f86c5ecff7d815eb4d218a5eb22e9248bb999a`.

유한 rank 행은 독립 점검이며 임의 compact `K`에 대한 증명은 약수렴
논증이다.

### H-I. 유한 한계와 분류

이 정리는 전체 even `L2` 모형에 적용된다. 실제 Guinand-Weil 산술 보정이
compact임을 증명하지 않았고 Legendre 열을 실제 admissible closure에 넣지도
않았다. 분류는 `exact_no_go`, RH는 `open_not_proven`이다.

### J-K. 최소 남은 간극과 다음 보조정리

```text
NoncompactArithmeticWeilFormOrLegendreExclusion
```

실제 허용 폐포에서 genuinely noncompact인 산술 Weil form을 제어하거나,
Legendre 도주열이 그 폐포에서 근사될 수 없음을 증명해야 한다.

## 2. 콜라츠 추측

### A. 정확한 명제: `SeparatedWieferichProjectiveSlopeCriterion`

소수 `q>5`에 대해

```text
U_q=((2^(q-1)-1)/q) mod q,
V_q=((3^(q-1)-1)/q) mod q
```

라 하자. TICKET-248의 bad 조건

```text
W_q(32,27)=0 and W_q(2,3)!=0
```

은 유일한 `t in F_q^*`가 존재해

```text
(U_q,V_q)=t(3,5)                                   (CO-249)
```

가 되는 것과 정확히 동치다. 즉 원점이 아닌 projective 목표 `[3:5]`이다.

### B-D. 증명

Fermat quotient의 `q_q(a^m)=m q_q(a) mod q`로

```text
W_q(32,27)=5U_q-3V_q,
W_q(2,3)=U_q-V_q.
```

첫 식은 `U_q=3t`, `V_q=5t`, `t=U_q/3`일 때 정확히 0이다. 이
직선에서 `U_q-V_q=-2t`이고 `q>5`이므로 이는 정확히 `t!=0`일 때
0이 아니다.

### E-G. 반례 탐색과 exact replay

두 독립 검사를 수행한다.

1. `q=7,11,23,101`의 모든 `(u,v) in F_q^2`, 총 10,900쌍을
   전수 검사했다. 영점 직선은 `q`개, 0이 아닌 projective 점은 `q-1`개다.
2. 모든 소수 `5<q<=10,000,000`을 `q^2` 모듈러 거듭제곱으로 검사했다.

실제 소수 664,576개에서 `W_q(32,27)` 영점은 없고,
`W_q(2,3)` 영점은 `q=23` 하나이며 separated hit는 없다.

- 복잡도: `O(B log log B + pi(B) log B)`와 작은 유한체 전수 검사;
- 산술: exact integer modular;
- 실패: 0;
- transcript SHA-256:
  `db860c5bef6ae1b016d468346b1b9941eac90c375f93d4f7c4f67c8ee8e881b7`.

### H-I. 유한 한계와 분류

projective 기준은 모든 소수에 대한 대수 정리다. 무검출 스캔은 유한
certificate일 뿐 `[3:5]`의 전역 회피나 출현을 증명하지 않는다. 이 valuation
branch를 결정해도 모든 Collatz 궤적은 제어되지 않는다. 분류는
`partial_theorem`, Collatz는 `open_not_proven`이다.

### J-K. 최소 남은 간극과 다음 보조정리

```text
OccurrenceOrAvoidanceOfProjectiveFermatQuotientSlopeThreeFifths
```

두 합동식을 독립 조건으로 보는 경로는 폐기한다. 실제 남은 산술 문제는
고정 projective 점에 대한 분포 정리 또는 정확한 한 번의 출현이다.

## 3. 강한 골드바흐 추측

### A. 정확한 명제: `CenteredJetParsevalSpikeNoGo`

`q>=3`, reduced `a0 mod q`를 고정하고 모든 residue `r`에서

```text
delta_r=cos(2*pi*a0*r/q),
eta_r=c delta_r,
J_a(t)=sum_r (delta_r+i t eta_r) exp(2*pi*i*a*r/q)
```

라 하자. 그러면 `delta`, `eta`는 중심화되고

```text
D0=q/2,  D1=c^2q/2,
J_a(t)=0 unless a=+a0 or -a0,
|J_(+/-a0)(t)|^2=q(D0+t^2D1)/2.                  (GB-249)
```

따라서 중심화와 TICKET-248 Parseval 항등식만으로 reduced numerator 전체의
`o(sqrt(q(D0+t^2D1)))` 균일 상계를 얻을 수 없다.

### B-D. exact 반례 증명

`zeta=exp(2*pi*i/q)`라 두면

```text
2delta_r=zeta^(a0 r)+zeta^(-a0 r).
```

root-of-unity 직교성으로 `2R0(a)`는 `a=+/-a0`에서 `q`, 나머지에서
0이다. 두 주파수는 `q>=3`의 reduced `a0`에서 서로 다르다. 따라서 전체
에너지는 `q^2/2`, 각 spike는 `q^2/4`다. `eta=c delta`이므로
`1+itc`가 모든 에너지를 `1+t^2c^2`배 한다.

### E-G. 적대적 exact replay

생성기는 복소 부동소수점 대신 다음 정수 규칙을 사용한다.

```text
sum_(r mod q) zeta^(kr) = q if q divides k, and 0 otherwise.
```

`3<=q<=128`의 모든 reduced `a0`를 검사했다.

- 사례: 5,020;
- 선택 행: 13;
- 각 spike/전체 제곱에너지 비: 정확히 `1/2`;
- 산술: 정수와 유리수만 사용;
- 실패: 0;
- transcript SHA-256:
  `439a6562998de91c99533ceacb5ac53d177af9e48165ee51c4eed6ec782d59fe`.

### H-I. 적용 범위와 분류

반례는 실수 중심 residue 벡터이지 실제 소수 개수나 소수 1차 모멘트 벡터가
아니다. abstract centeredness와 Parseval 에너지만으로 균일 제어를 만드는
논리만 반증한다. 소수 고유의 산술 anti-concentration은 반증하지 않았다.
분류는 `exact_no_go`, 강한 Goldbach는 `open_not_proven`이다.

### J-K. 최소 남은 간극과 다음 보조정리

```text
PrimeSpecificReducedNumeratorJetAntiConcentration
```

다음 단계는 동일한 평균 에너지 변형이 아니라 임의 중심 벡터에는 없는
소수 분포의 산술 구조를 사용해야 한다.

## 4. 쌍둥이 소수 추측 — deep focus

### A. 정확한 명제: `EvenExponentLeftActiveContaminationClassification`

`p,r`가 홀수 소수이고 `m,ell>=1`이라 하자. 만약

```text
p!=3 and p^(2m)+2=r^ell
```

이면

```text
(p,m,r,ell)=(5,1,3,3).                            (TP-249)
```

따라서 TICKET-248 왼쪽 활성 오염 중 짝수 지수이고 밑이 `3`이 아닌 항은
정확히 `(25,27)` 하나다.

```text
L_even,p!=3(X)=1_(X>=25).
```

### B-D. 증명과 외부 의존성

`x=p^m`이라 하자. `p!=3`이므로 `x^2=1 mod 3`, 따라서 `x^2+2`는
3의 배수다. 우변이 소수 거듭제곱이므로 `r=3`이다. `ell=1,2`는 각각
`x=1`, `x^2=7`을 주어 불가능하다. `ell>=3`에서는 고전적인 `D=2`
Lebesgue-Nagell 분류를 사용한다.

```text
x^2+2=y^n, x,y>0, n>=3  =>  (x,y,n)=(5,3,3).
```

따라서 `p^m=5`, 즉 `p=5,m=1`이다. 외부 결과는 PrimeProject가 새로
증명한 것으로 취급하지 않고 proof DAG의 `external_theorem` 노드에 둔다.
`1<=D<=100`의 `x^2+D=y^n`을 해결한 현대 1차 자료는 Bugeaud,
Mignotte, Siksek의 [Compositio Mathematica 142 (2006), 31-62](https://doi.org/10.1112/S0010437X05001739)이다.

### E-G. exact 활성 support replay

exact 소수 거듭제곱 표현 표로 `X=10,000,000` 이하의 모든 shift-two 활성
쌍을 열거하고 왼쪽 합성 항을 다음으로 분리했다.

```text
짝수 지수, base !=3;
짝수 지수, base =3;
홀수 지수.
```

`X=10,000,000`에서 각 개수는 `1,5,8`, 합계 `L=14`이며 오른쪽 활성
개수는 `R=136`이다. 첫 범주의 유일한 witness는 `(25,27)`이다.

- 규모: 7;
- 산술: exact integer;
- 복잡도: `O(X log log X)` 시간, `O(X)` support 메모리;
- 실패: 0;
- transcript SHA-256:
  `6df796f1387e44725a337fc60d5fe44a94e2521496caf1cdc39e30bba96f6fd9`.

### H-I. 유한·논리 한계

모든 `X`에 대한 분류는 천만 이하 스캔이 아니라 외부 Diophantine 정리에서
나온다. 왼쪽 활성 중 짝수 지수·base-not-3 부분만 제어한다. 오른쪽 활성
항은 훨씬 크고 prime-power proxy의 scale-local Type-II 하한도 없다. 분류는
`partial_theorem`, 쌍둥이 소수 추측은 `open_not_proven`이다.

### J-K. 최소 남은 간극과 다음 보조정리

```text
ScaleLocalRightActivePrimePowerContaminationBound
```

다음에는 활성 shift-two 쌍 오른쪽의 합성 소수 거듭제곱을 scale-local하게
상계해야 한다. 그 correction을 제어한 뒤에야 비주기 Type-II proxy 하한과
비교할 수 있다.

## Proof DAG와 적대적 감사

네 문제의 proof DAG는 모두 비순환이고 `open` frontier가 하나다. Twin DAG는
`D=2` Lebesgue-Nagell 분류를 `external_theorem`으로 명시한다. 어떤
`assumption`, `heuristic`, `open` 노드도 원 추측 해결 경로의 proved 노드로
계산하지 않는다.

| 트랙 | proved TICKET-249 노드 | disproved 경로 | open frontier |
|---|---|---|---|
| RH | compact 보정 no-go | compact한 전체 구면 coercivity 복구 | noncompact Weil form 또는 Legendre 배제 |
| Collatz | projective slope 기준 | 두 독립 좌표 합동식 | `[3:5]` 출현/회피 |
| Goldbach | exact 두-spike 반례 | Parseval-only 균일 승격 | prime-specific jet anti-concentration |
| Twin | even-left 활성 분류 | 임의 away-from-3 even-left family | 오른쪽 활성 오염 상계 |

유한 스캔을 무한 명제로 승격하지 않았고 평균을 실제 소수의 점별 명제로
승격하지 않았으며 외부 Diophantine 의존성을 분리했다. 해결과 해결 후보
개수는 모두 0이다.
