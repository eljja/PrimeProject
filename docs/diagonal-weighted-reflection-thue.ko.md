# TICKET-254: 양의 대각 no-go, 가중 완전 검출기 no-go, 순환 반사, 지수 17 Thue 축약

- 부모 회차: TICKET-253
- 생성 시각: 2026-08-29 14:19:28 +09:00
- 심층 집중 문제: 강한 골드바흐 추측
- 추측 해결 수: 0
- 후보 해결 수: 0
- 결과 분류: `exact_no_go` 2개, `partial_theorem` 2개

## 주장 경계

TICKET-254는 프로젝트 내부의 보조정리 네 개를 증명한다. 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 가운데 어느 것도
증명하거나 반증하지 않는다. RH 결과는 추상 양의 연산자에 관한 반례이고,
콜라츠 결과는 완전 검출기 표현의 한계를 판정한다. 골드바흐 결과는
반사/임계값 부분류만 배제하며, 쌍둥이 소수 결과는 17개의 Thue 방정식으로
축약할 뿐 그 방정식들을 모두 풀지는 않는다.

## 재현

```powershell
python scripts/ticket254_diagonal_weighted_reflection_thue.py
python -m unittest tests.test_ticket254_diagonal_weighted_reflection_thue -v
python scripts/verify_ticket254_structure.py
python scripts/verify_open_problem_structure.py
python scripts/verify_open_problem_workbench.py
python scripts/reproduce_publication.py
node --check assets/ticket254-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
python -m unittest discover -s tests -p "test_*.py"
```

TICKET-254 생성기의 산술은 모두 정수 또는 `Fraction` 산술이다. 난수 시드와
부동소수점 추론은 사용하지 않는다.

## 기계 요약

| 문제 | 이번에 판정한 정확한 명제 | 분류 | 원 추측 상태 |
|---|---|---|---|
| RH | `PositiveDiagonalDirichletPacketDominationNoGo` | `exact_no_go` | `open_not_proven` |
| 콜라츠 | `NonnegativeCrossPrimeCompleteDetectorAverageNoGo` | `exact_no_go` | `open_not_proven` |
| 골드바흐 | `EvenCyclotomicReflectionPrimePrefixExclusion` | `partial_theorem` | `open_not_proven` |
| 쌍둥이 소수 | `ExponentSeventeenUnitTwistedThueReduction` | `partial_theorem` | `open_not_proven` |

## 1. 리만 가설

### A. 정확한 명제

모든 정수 `N>=1`에 대해 `L=2N+1` 및

```text
d_N=L^(-1/2) sum_(|n|<=N) e_n in l2(Z)
```

를 두자. 다음을 만족하는 유계 양의 자기수반 연산자 `A_N`이 존재한다.

```text
<A_N e_n,e_n>=1 (모든 n), 그러나 <A_N d_N,d_N>=0.  (RH-254)
```

패킷 블록에서는

```text
A_N = L/(L-1) I - 1/(L-1) J
```

를 쓰고 그 직교 여공간에서는 항등 연산자를 쓴다.

### B-D. 정의와 증명

표시한 블록의 대각 성분은 정확히 1이다. 전부 1인 벡터에서 `J`의 고윳값은
`L`이므로 `A_N`의 고윳값은 0이다. 그 직교 여공간에서는 `J=0`이고 고윳값은
`L/(L-1)>0`이다. 따라서 블록은 양의 준정부호이며, 항등 연산자와의 직합은
유계·양·자기수반이다. 연산자 노름은 모든 `N`에 대해 `3/2` 이하이다.

그러므로 다음 제안된 함의는 거짓이다.

```text
푸리에 대각의 균일한 양성 => Dirichlet 패킷의 양의 지배
```

이 반례는 실제 Guinand-Weil 이차형식에 부정적인 결론을 내리지 않는다.
대각 정보만으로는 TICKET-253의 목표를 증명할 수 없음을 확정한다.

### E-G. 적대적 계산

`N=1,2,3,4,7,15,31,63`인 정확 블록 8개에서 대각, 비대각, 패킷 에너지,
두 고윳값을 유리수 산술로 다시 계산했다. 패킷 에너지는 모두 정확히 0이고
실패는 0개이다.

- 알고리즘: 등상관 블록의 두 고유공간을 정확 계산
- 복잡도: 재현 행 하나당 `O(1)`; 모든 `N`에 대한 결론은 대수적 증명
- 기록 SHA-256: `0be64af7360d626405108d0fee5944f6132fdb6065fd57690c657f3e160df05c`

### H-I. 유한 계산의 한계와 분류

유한 행은 공식을 재현할 뿐이다. 더 중요한 한계는 `A_N`이 `N`마다 선택한
추상 연산자인 반면 실제 Weil 형식은 고정된 산술 형식이라는 점이다. 분류는
대각만 사용하는 경로에 대한 `exact_no_go`이며 RH에 대한 판정이 아니다.

### J-K. 남은 간극과 다음 단일 보조정리

실제 유한 Weil 블록의 비대각 성분을 정량적으로 통제해야 한다.

```text
ActualWeilDirichletBlocksHaveUniformStrictDiagonalDominance
```

## 2. 콜라츠 추측

### A. 정확한 명제

`q>5`인 소수의 유한 집합 `Q`, 임의의 `(U_q,V_q) in F_q^2`, 비음 유리수
가중치 `w_q`에 대해

```text
D_q=5U_q-3V_q,
C_q(D)=sum_(h=1)^(q-1) exp(2 pi i hD/q)
```

라 두면

```text
sum_q w_q [(1+C_q(D_q))/q - 1_(U_q=V_q=0)]
= sum_q w_q 1_(D_q=0 and (U_q,V_q)!=(0,0)).          (CO-254)
```

특히 모든 합항은 비음이다.

### B-D. 증명과 추론 감사

완전 가법 캐릭터 직교성으로 점별 항등식

```text
(1+C_q(D))/q = 1_(D=0)
```

을 얻는다. 원점을 빼고 `w_q>=0`을 곱한 뒤 합하면 (CO-254)가 증명된다.
따라서 제안된 비음 교차-소수 완전 평균에는 상쇄가 없다. 그 평균을 추정하는
일은 원래의 가중 발생 횟수 문제와 정확히 같다.

이는 TICKET-253의 점별 진단을 모든 유한 비음 가중으로 확장한다. 부호를 갖는
불완전 캐릭터 핵은 발생 지시함수가 아닐 수 있으므로 이 no-go의 대상이 아니다.

### E-G. 적대적 계산

`7<=q<=47`의 소수 12개에서 표준 Fermat-몫 쌍, 합성 `[3:5]` 적중, 비적중,
원점의 네 경우를 검사했다. 이어 가중치 `1`, `q`, `1/q`를 모든 시나리오에
적용했다.

- 검출기 행: 48
- 가중 행: 12
- 산술: `q^2` 법의 모듈러 거듭제곱, 정수, `Fraction`
- 실패: 0
- 기록 SHA-256: `6ce9f4399b2372016d2c0bb7d9aa02e8bc14b7b5ee124687ba55c6f76638be46`

### H-I. 유한 계산의 한계와 분류

계산은 대수 정리의 재현일 뿐이며, `q`가 변할 때 표준 쌍의 발생 또는 회피를
증명하지 않는다. 분류는 정규화 완전 검출기의 비음 평균 경로에 대한
`exact_no_go`이다.

### J-K. 남은 간극과 다음 단일 보조정리

유용한 변환이라면 실제로 부호가 변하면서도 발생을 복원해야 한다.

```text
IncompleteSlopeCharacterKernelHasSignedRecoveryAndCrossPrimeCancellation
```

## 3. 강한 골드바흐 추측 — 심층 집중

### A. 정확한 명제

`q>=5`가 소수이고 `m`이 짝수이며 `q`가 `m`을 나누지 않는다고 하자.
`c_r`를 `(1-X)^m mod (X^q-1)`의 순환 계수라 하자. TICKET-252의 0-잔여류
적합성을 가정하고

```text
t=1-c_0, T=qt, r=m mod q
```

라 두자. `kappa_q(r)`를 `r mod q`인 두 번째 소수의 전체 소수열 내 첨자라
하자. 만약

```text
T >= kappa_q(r),                                      (GB-254a)
```

이면 이 적합 꼬리는 실제 소수 접두 벡터가 아니다.

### B-D. 반사 증명과 전달

`a_j=(-1)^j binom(m,j)`라 두면 대합 `j -> m-j`로부터

```text
a_(m-j)=(-1)^m a_j
```

이고, 이를 `q` 법으로 접으면

```text
c_(m-r)=(-1)^m c_r.                                  (GB-254b)
```

`r=0`이고 `m`이 짝수이므로

```text
c_(m mod q)=c_0.
```

`q`가 `m`을 나누지 않으므로 이 잔여류는 0이 아니다. TICKET-253 벡터에서
그 잔여류의 강제 개수는

```text
N*_(m mod q)=c_0+(1-c_0)=1.                          (GB-254c)
```

이다. (GB-254a)가 성립하면 처음 `T`개 소수에는 이미 그 잔여류의 소수가
두 개 있으므로 실제 개수는 2 이상이다. 이는 (GB-254c) 및 TICKET-253의
유일 접두 실현가능성 필요충분조건과 모순이다.

대응 대상과 보존 성질도 명시적이다. 순환 이항계수는 반사로 대응되고,
`c_0`와의 같음은 균일 이동에서 보존되며, TICKET-253의 필요충분정리를 통해
실제 소수 접두 개수로 전달된다.

### E-G. 정확 인증서

다음 짝수 쌍들을 재현 검사했다.

```text
q in {5,7,11,13,17,19}, 2<=m<=160
```

480쌍 중 `q`가 `m`을 나누지 않는 적합 쌍은 50개였다. 모든 행에서 반사
항등식이 정확히 성립하고 반사 잔여류의 강제 개수는 1이며, 명시적인 두 번째
잔여류 소수가 강제 접두의 끝보다 앞에 있었다.

첫 인증서는 `(q,m)=(5,8)`이다. `r=3`, `T=280`이고, `3 mod 5`인 첫 두
소수는 `3,13`이며 두 번째 소수의 전체 첨자는 6이다. 표시한 가장 큰 `T`는
`35532145864654126766913393422907521619163005115`이지만 그 접두를 열거하지
않는다. 작은 잔여류 소수 증인 두 개만 필요하다.

- 알고리즘: 정확 순환 이항 접기와 결정적 소수 판정
- 복잡도: 접은 계수 개수에 선형 + 잔여류 소수 두 개의 짧은 탐색
- 실패: 0
- 기록 SHA-256: `253518284e5b939aa42449fd309978e3fe0c7bda7d83944ee96217eed38394f6`

### H-I. 경계와 분류

유한 검사는 인증서 50개를 제시하지만 일반 정리를 만드는 근거는 아니다.
정리는 정확한 가정을 만족하는 모든 쌍에 적용된다. 홀수 `m`, `q|m`, 또는
두 번째 소수 임계값보다 짧은 접두는 다루지 않는다. 분류는
`partial_theorem`이고 강한 골드바흐 추측은 미해결이다.

### J-K. 남은 간극과 다음 단일 보조정리

```text
OddOrQDivisibleCompatibleTailPrimePrefixExclusion
```

## 4. 쌍둥이 소수 추측

### A. 정확한 명제

`0<=j<17`에 대해

```text
(1+sqrt(2))^j=a_j+b_j sqrt(2)
```

라 쓰고 다음 식으로 정수 동차다항식 `A_j,B_j`를 정의한다.

```text
A_j(u,v)+B_j(u,v)sqrt(2)
=(a_j+b_j sqrt(2))(u+v sqrt(2))^17.                  (TP-254a)
```

양의 정수 해

```text
x^2-2=y^17                                          (TP-254b)
```

가 존재할 필요충분조건은 어떤 정수 `j,u,v`가

```text
B_j(u,v)=1,
A_j(u,v)>0,
y=(-1)^j(u^2-2v^2)>0                                (TP-254c)
```

을 만족하는 것이다. 이때 `x=A_j(u,v)`이다.

### B-D. 이차 정수환 증명

`y`가 짝수이면 `x`도 짝수이고 `v_2(x^2-2)=1`이 되어 17제곱과 모순이다.
따라서 `x,y`는 홀수이다. `Z[sqrt(2)]`에서 두 켤레 인자 `x+sqrt(2)`와
`x-sqrt(2)`는 서로소이다. 공약수는 `2sqrt(2)`를 나누지만 그 노름은 홀수
`y^17`도 나누어야 하므로 단위뿐이다.

이 환은 노름 유클리드 환이다. 몫 `r+s sqrt(2)`의 두 계수를 가장 가까운
정수로 반올림하면 나머지 노름의 절댓값이 `1/2<1` 이하이다. 따라서 UFD이며,
서로소성과 (TP-254b)에서

```text
x+sqrt(2)=epsilon (u+v sqrt(2))^17
```

을 얻는다. 표준 Pell 단위 하강으로 모든 단위는 `+/- (1+sqrt(2))^n`이다.
17제곱 단위와 부호를 `(u,v)`에 흡수하면 `j mod 17` 하나만 남는다.
`sqrt(2)` 계수 비교와 노름 계산이 (TP-254c)를 주고, 역방향은 전개로 즉시
성립한다.

### E-G. 적대적 정확 계산

차수 17 계수 배열 17쌍을 모두 명시적으로 출력한다. `(u,v)=(0,0)`을 뺀
`|u|,|v|<=12` 상자는 10,608개의 정확 twist 점을 준다. 각 점에서 이진
이차환 거듭제곱, 다항식 직접 평가, 그리고

```text
A_j(u,v)^2-2B_j(u,v)^2
= [(-1)^j(u^2-2v^2)]^17
```

이 정확히 일치했다. `B_j=1`인 점은 2개였지만 둘 다 축약된 `y`가 음수였고,
상자 안의 허용 가능한 양의 점은 0개였다.

- 실패: 0
- 난수 시드: 없음
- 기록 SHA-256: `1cc60a2de6cbf63644bb1751a558602cdf696651b181a1a14606b62ec457fcf3`

### H-I. 경계와 분류

유한 상자가 그 밖의 해에 대한 반증 근거는 아니다. 실제로 TICKET-253의 외부
하한은 비자명 밑을 이 상자보다 훨씬 멀리 둔다. 새 결과는 빈 유한 탐색이
아니라 정확한 유한 방정식족이다. 분류는 `partial_theorem`이며 지수 17
방정식과 쌍둥이 소수 추측은 모두 미해결이다.

### J-K. 남은 간극과 다음 단일 보조정리

```text
AllSeventeenUnitTwistedCoefficientOneThueEquationsHaveNoAdmissibleIntegralPoint
```

## proof DAG와 회차 완료 감사

각 문제의 DAG는 TICKET-253 선행 노드, 새 증명 노드, 반증된 경로, 정확히
하나의 열린 다음 보조정리로 이루어진 비순환 네 노드 그래프이다. 가정이나
휴리스틱 노드는 완료 경로에 놓지 않았다. 기계 실패, 후보 해결, 추측 해결은
모두 0개이다.

회차 완료는 코드, 정확 출력, 보고서, DAG, Pages, 테스트가 재현된다는 뜻이다.
원 추측이 해결되었다는 뜻은 아니다.
