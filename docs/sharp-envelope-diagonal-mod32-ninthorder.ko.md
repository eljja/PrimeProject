# TICKET-263 — sharp envelope, diagonal Weyl cutoff, mod-32 phase, ninth-order exactness

## 판정

이번 회차는 네 개의 새 부분정리를 확립한다. 리만 가설, 콜라츠 추측,
강한 골드바흐 추측, 쌍둥이 소수 추측 중 해결된 것은 없다. 정준 기계
기록은 `data/open-problem/ticket263-sharp-envelope-diagonal-mod32-ninthorder.json`이다.

| 문제 | 정확 명제 | 결과 | 분류 | 상태 | 다음 단일 보조정리 |
|---|---|---|---|---|---|
| 리만 가설 | `A=limsup n|E_n-L|`이면 `limsup J_n<=2A`, `liminf S_n>=L-2A`; 상수 2는 최적 | sharp reciprocal envelope | `partial_theorem` | `open_not_proven` | `ActualWeilPacketReciprocalEnvelopeBelowHalfLimit` |
| 콜라츠 | 모든 고정 비영 조화성분의 Weyl 소멸 iff 어떤 증가 cutoff에서의 균일 소멸 | diagonal quantifier reduction | `partial_theorem` | `open_not_proven` | `CanonicalFermatQuotientGrowingCutoffUniformWeylCancellation` |
| 강한 골드바흐 | q=3 특수 동률이면 `l mod 4`에 따라 `N_2 mod 32`가 `28,4,12,20` | four-phase tie obstruction | `partial_theorem` | `open_not_proven` | `Q3SpecialMinusOneResidueCountAvoidsLevelPhasedModuloThirtyTwo` |
| 쌍둥이 소수 | 명시적 root cone과 문턱 이후 양방향 9차 합동 iff `B_1(u,v)=epsilon` | ninth-order tail exactness | `partial_theorem` | `open_not_proven` | `NoUniqueRootConvergentSatisfiesJointNinthOrderCongruences` |

## 재현 계약

```text
python scripts/ticket263_sharp_envelope_diagonal_mod32_ninthorder.py
python -m unittest tests.test_ticket263_sharp_envelope_diagonal_mod32_ninthorder -v
python scripts/verify_ticket263_structure.py
```

모든 증명 의존 계산은 정수 또는 `Fraction`이다. 난수와 부동소수점
판정은 없다. 각 계산 transcript의 SHA-256은 통합 JSON과 문제별 JSON에
기록된다.

## 1. 리만 가설

### A-B. 정확 명제와 정의

실수열 `E_n -> L>0`에 대해

```text
A   = limsup n |E_n-L|,
J_n = n(E_n-E_(n+1)),
S_n = (n+1)E_(n+1)-nE_n
```

로 둔다. 그러면 확장실수 의미에서

```text
limsup J_n <= 2A,             liminf S_n >= L-2A.
```

따라서 `A<L/2`이면 어떤 `delta>0`, `N`이 존재하여 모든 `n>=N`에서
`S_n>=delta`이다. 상수 2는 개선할 수 없다.

### C-E. 증명과 sharpness 반례

`a_n=E_n-L`이라 쓰면

```text
J_n <= n|a_n| + n|a_(n+1)|
    = n|a_n| + [n/(n+1)](n+1)|a_(n+1)|.
```

양변의 limsup를 취하면 첫 부등식이 나온다. TICKET-262의 정확 항등식
`S_n=E_(n+1)-J_n`을 적용하면 두 번째 부등식이 나온다.

모든 `L,A>0`에 대해

```text
E_n=L+(-1)^n A/n
```

이면

```text
J_n=(-1)^n A(2n+1)/(n+1),
S_n=L-2(-1)^n A.
```

따라서 `limsup J_n=2A`, `liminf S_n=L-2A`이다. 특히 `A=L/2`에서는
짝수 행의 lag가 정확히 0이므로 positive margin이 없다. 이는 오차율
정보만으로 상수 2를 더 작게 만드는 모든 보편 명제를 반증한다.

### F-K. 계산, 한계, 다음 간극

`L=1`, `A=1/3,1/2,2/3`, `1<=n<=64`의 192행을 exact `Fraction`으로
재현했다. 실패 수는 0이다. 이 세 가족은 실제 Guinand-Weil packet이
아니며 RH를 결정하지 않는다.

- 폐기: reciprocal-rate-only 논증의 보편 상수를 2보다 작게 두는 경로.
- 보류: 실제 packet의 `limsup n|E_n-L|<L/2` 산술 추정.
- 남은 최소 간극: `ActualWeilPacketReciprocalEnvelopeBelowHalfLimit`.

## 2. 콜라츠 추측

### A-B. 정확 명제와 정의

`x_j in R/Z`와

```text
W_N(h)=N^(-1) sum_(j<=N) exp(2*pi*i*h*x_j)
```

에 대해 다음은 동치이다.

1. 모든 비영 정수 `h`에 대해 `W_N(h)->0`.
2. `H_N->infinity`인 비감소 정수열이 존재하여
   `max_(1<=|h|<=H_N)|W_N(h)|->0`.

고전 Weyl 판정법에 의해 어느 조건이든 star discrepancy 0을 함의한다.

### C-E. 양화사 대각화 증명

2에서 1은 고정 `h`가 결국 cutoff 안에 들어가므로 즉시 따른다. 1을
가정하자. 각 `m`에 대해 `N_m>N_(m-1)`을 충분히 크게 택해 모든
`N>=N_m`, `1<=|h|<=m`에서 `|W_N(h)|<=1/m`이 되게 한다. `H_N`을
`N_m<=N`인 가장 큰 `m`으로 두면 `H_N`은 비감소하고 무한대로 가며,
moving maximum은 `1/H_N` 이하이다.

이는 TICKET-262의 “고정 유한 cutoff는 불충분”과 모순되지 않는다.
이번 cutoff는 데이터에 의존하며 무한대로 증가한다.

### F-K. 계산, 한계, 다음 간극

완전 grid `j/M`, `M=4,8,16,32,64`에서 `1<=h<M`의 완전근 합이 0이고
star discrepancy가 정확히 `1/M`임을 119개 조화성분에서 정수로
재현했다. 이들은 triangular model이며 정준 Fermat quotient 위상이 아니다.

- 폐기: 전 고정 조화성분 극한을 하나의 growing cutoff로 묶을 수 없다는 경로.
- 보류: 정준 위상의 실제 quantitative schedule.
- 남은 최소 간극: `CanonicalFermatQuotientGrowingCutoffUniformWeylCancellation`.

## 3. 강한 골드바흐 추측

### A-B. 정확 명제

`T_l=6*3^(6l+2)+3`이라 하자. 첫 `T_l`개 소수에서 3을 제외한 두
비영 mod-3 잔여류 개수가 동률이면

```text
N_2=3^(6l+3)+1.
```

따라서 `l mod 4=0,1,2,3`에 대응하는 `N_2 mod 32`는 각각
`28,4,12,20`이다.

### C-E. 증명과 충분성 반례

동률이면 `T_l-1`개의 비영 잔여가 반씩 나뉜다. `3`의 mod-32 위수는
8이고 `6l+3 mod 8`은 `3,1,7,5`를 순환한다. 이에 1을 더하면 네
잔여가 나온다.

`l>=1`, `M=3^(6l+3)+1`에 대해

```text
(N_1,N_2)=(M-32,M+32)
```

는 비음수가 아니고 총합 `2M`과 필요한 `N_2 mod 32`를 보존하지만
동률이 아니다. 따라서 phased mod-32 조건은 필요조건이지 충분조건이 아니다.

### F-K. 계산과 한계

실제 `l=0,1,2`에서

```text
actual N_2 mod 32: 31,25,15
tie residue mod 32: 28, 4,12
```

이므로 세 동률을 대우로 배제했다. 두 독립 prime-residue count가
일치한다. 상징 위상은 `0<=l<=15`, 충분성 반례는 `1<=l<=15`에서
재현했지만 증명 자체의 위상식과 `l>=1` 반례족은 전 수준 명제다.

- 폐기: phased mod-32 조건을 전 수준 충분조건으로 사용하는 경로.
- 보류: 실제 모든 특수 prefix의 위상 잔여 회피.
- 남은 최소 간극: `Q3SpecialMinusOneResidueCountAvoidsLevelPhasedModuloThirtyTwo`.

## 4. 쌍둥이 소수 추측 — deep focus

### A-B. 정확 명제

```text
a_k = C(17,k) 2^floor(k/2),
B_1(u,v) = sum_(k=0)^17 a_k u^(17-k)v^k,
A = sum a_k = 2744210,
V_0 = (A+1)16^9 = 188580743973175296.
```

`gcd(u,v)=1`, `uv!=0`, `v>V_0`, `1/16<=|u|/v<=1`,
`epsilon in {-1,1}`라 하자. 그러면 `B_1(u,v)=epsilon`일 필요충분조건은

```text
sum_(k=0)^8  a_k u^(17-k)v^k = epsilon (mod v^9),
sum_(k=9)^17 a_k u^(17-k)v^k = epsilon (mod u^9)
```

이다.

### C-E. 필요성과 충분성 증명

필요성은 각각 `v^9`, `u^9`으로 나뉘는 나머지 항을 버리면 된다.
역으로 두 합동과 coprimality에서

```text
(|uv|)^9 divides B_1(u,v)-epsilon.
```

계수가 양수이고 `|u|<=v`이므로

```text
|B_1-epsilon| <= (A+1)v^17.
```

root cone에서는

```text
(|uv|)^9 >= v^18/16^9.
```

`v>V_0`이면 오른쪽이 앞의 상계보다 엄밀히 크다. 따라서 차가 0이
아니면서 큰 정수로 나누어지는 경우는 불가능하고 `B_1=epsilon`이다.
9는 product divisor의 동차 차수 `2r`이 형식 차수 17을 처음 넘는
정수 차수이다. 이 크기 논증은 또 하나의 필요 jet가 아니라 tail의
필요충분 판정을 준다.

### F-H. exact 계산과 경계 감사

유일 실근의 인증 연분수 수렴분수 1,024개에 대해 양 부호와 차수
1부터 9까지 exact modular truncation을 검사했다.

- 비자명 joint 9차 통과: 0.
- root-cone size 정리 적용 행: 986.
- 최초 적용 term index: 38.
- 마지막 분모: 519자리.
- 최초 joint 실패 차수 histogram, 양 부호 합계:
  `r=1:2044`, `r=2:2`, `r=3..9:0`, `9까지 실패 없음:2`.

마지막 두 통과는 term 0의 `(-1,1)`에서 modulus가 1이어서 양 부호
합동이 자명한 두 경계 사례다. `v>V_0` 및 비자명 modulus 정의역 밖이며
별도 JSON certificate로 보존했다. `u=0` 초기 행도 정리의 `uv!=0`
밖으로 분리했다. 이 경계들을 삭제하거나 해결 증거로 세지 않았다.

### I-K. 분류와 남은 간극

결과는 `partial_theorem`이다. 1,024개 이후 수렴분수의 9차 합동 실패를
증명하지 않았고, 문턱 아래 모든 분모를 전역 탐색하지 않았다.

- 폐기: degree 17 뒤에도 더 높은 binomial jet가 계속 독립 정보를 준다는 경로.
- 보류: 모든 unique-root convergent의 joint 9차 배제.
- 남은 최소 간극: `NoUniqueRootConvergentSatisfiesJointNinthOrderCongruences`.

## 적대적 감사와 proof DAG

- 네 명제의 양화사와 정의역을 JSON에 고정했다.
- 유한 grid, 세 실제 Goldbach level, 1,024 Twin 수렴분수를 무한 결론으로
  승격하지 않았다.
- Twin modulus-one 통과와 `u=0` 경계를 명시적으로 분리했다.
- Collatz discrepancy 전달은 `external_theorem` 상태의 고전 Weyl 판정법이다.
- 네 DAG는 비순환이고 각 resolution path의 열린 frontier는 정확히 하나다.
- `candidate_resolution_count=0`, `resolved_count=0`, `program_complete=false`이다.

이번 회차는 완료되었지만 해당 추측은 해결되지 않았다.
