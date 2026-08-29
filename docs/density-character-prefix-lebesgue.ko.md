# TICKET-253: 밀도 packet, character 합 이분법, 강제 prime prefix, 84개 지수 frontier

- 부모: TICKET-252
- `iteration_complete`: true
- `program_complete`: false
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- 분류: `partial_theorem` 3개, `exact_no_go` 1개
- 심층 집중: 쌍둥이 소수 추측
- 네 상위 문제: 모두 `open_not_proven`

TICKET-253은 프로젝트 내부 보조명제 네 개를 확정한다. 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않았다. 쌍둥이 소수 트랙의 결과는 명시한 외부
Lebesgue--Nagell 정리의 따름정리이며 그 방정식의 새 완전해가 아니다.

## 재현 명령

```powershell
python scripts/ticket253_density_character_prefix_lebesgue.py
python -m unittest tests.test_ticket253_density_character_prefix_lebesgue -v
python scripts/verify_ticket253_structure.py
python scripts/verify_ticket252_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket253-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

증명에 쓰인 재생 값은 모두 정수 또는 유리수다. random seed는 없다.
유리수 record의 float 표시는 증명에 사용하지 않는다.

| 문제 | TICKET-253의 정확 명제 | 분류 | 상위 상태 |
|---|---|---|---|
| 리만 | normalized Dirichlet packet은 Fourier projection의 대칭 밀도를 극한에서 정확히 읽음 | `partial_theorem` | `open_not_proven` |
| 콜라츠 | 고정 소수의 complete character 합은 slope indicator 그 자체라 독립 smoothing을 주지 않음 | `exact_no_go` | `open_not_proven` |
| 강한 골드바흐 | 각 compatible cyclotomic tail에는 유일한 prime prefix가 강제되며 선택한 10개 tail은 모두 불일치 | `partial_theorem` | `open_not_proven` |
| 쌍둥이 소수 | 살아남는 홀수 오염 지수의 모든 소인수는 명시적 84개 Lebesgue--Nagell frontier에 속함 | `partial_theorem` | `open_not_proven` |

## 1. 리만 가설

### A. 선언 명제: `DirichletPacketSpectralDensityLimit`

`L2([-1,1])`에서

```text
e_n(x)=2^(-1/2) exp(pi i n x),
D_N=(2N+1)^(-1/2) sum_(|n|<=N) e_n
```

으로 둔다. 모든 대칭 집합 `S subset Z`와 그 mode에 대한 직교 projection
`P_S`에 대해 `D_N`은 짝인 단위벡터이고 내부점 0에 집중하며

```text
<P_S D_N,D_N> = #(S intersect [-N,N])/(2N+1).       (RH-253)
```

`S`의 대칭 natural density가 `d`이면 좌변은 정확히 `d`로 수렴한다.

### B-D. 정의·증명·추론 감사

직교정규성으로 norm과 계수 개수 항등식을 얻는다. normalized Dirichlet
kernel 공식은

```text
|D_N(x)|^2 =
 |sin((2N+1)pi x/2)/sin(pi x/2)|^2 /(2(2N+1)).
```

고정 `epsilon>0`에 대해 `epsilon<=|x|<=1`의 적분은

```text
1 / ((2N+1) sin(pi epsilon/2)^2)
```

이하이므로 0으로 간다. (RH-253)에 대칭 밀도의 정의를 적용하면 결론이
나온다. 점별 수렴을 균일 수렴으로 바꾸는 단계는 없다.

### E-G. 적대적·재현 계산

대칭 주기 집합

```text
S={n in Z : n mod 6 is 1 or 5}, density(S)=1/3
```

과 `N=2^s-1`, `s=3,...,13`의 11개 band를 exact count했다. 모든 행에서

```text
|3 #(S intersect [-N,N])-(2N+1)| <= 3
```

을 확인했다. 실패 0. SHA-256:
`00bebb686b3544d67b49612c512f28feee544d678ceab6c5fa269f64e9e16299`.

### H-I. 유한 한계와 분류

11개 행은 한 periodic set의 재생일 뿐이며 all-density 결론은 해석적
항등식이다. 실제 signed Guinand--Weil form을 Fourier projection과
동일시하지 않았다. 분류는 `partial_theorem`; RH는 `open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

```text
ActualWeilFormDominatesPositiveDensityProjectionOnDirichletPackets
```

## 2. 콜라츠 추측

### A. 선언 명제: `CompleteSlopeCharacterSumDichotomyNoGo`

소수 `q>5`, `D in F_q`에 대해

```text
C_q(D)=sum_(h=1)^(q-1) exp(2 pi i hD/q)
```

라 하면

```text
C_q(D)=q-1  (D=0), C_q(D)=-1  (D!=0),
(1+C_q(D))/q = 1_(D=0).                             (CO-253)
```

`D_q=5F_q(2)-3F_q(3)`에 대입하고 원점 indicator를 빼면 separated
projective slope `[3:5]` detector가 정확히 복원된다.

### B-D. 정의·증명·추론 감사

`D=0`이면 모든 항이 1이다. `D!=0`이면 `D`의 곱셈이 `F_q^*`를 순열하고
전체 `q`개 additive character 합이 0이므로 비영 index 합은 `-1`이다.
Fermat quotient 가법성으로

```text
D_q=0 iff 32^(q-1)=27^(q-1) mod q^2
```

도 얻는다. 따라서 complete 합은 목표를 부드럽게 만들지 않는다. target
prime에서는 위상이 항등적으로 0이므로 generic nondegenerate complete-sum
bound를 적용할 수 없다.

### E-G. 적대적·재현 계산

`7<=q<=47`의 소수 12개에서 canonical `F_q(2),F_q(3)`을 `q^2` 법 modular
exponentiation으로 재계산했다. character 이분법, rational-Wieferich 동치,
원점 제거와 separated detector를 exact integer로 검증했다. 실패 0.
SHA-256:
`455240ed72e4017bfbc63ba310348eb9e2618370d829ee093253e1d66e6883c2`.

### H-I. no-go 범위와 유한 한계

폐기: 고정 `q` complete orthogonality를 독립적인 smoothing statistic으로
취급하는 경로. 이는 정확한 route no-go지만 canonical `[3:5]`의 전역
출현·회피 정리가 아니다. 12개 행과 기존 대규모 no-hit scan은 무한
결론으로 승격하지 않는다. Collatz는 `open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

```text
CrossPrimeCanonicalSlopeCharacterAverageCancellation
```

## 3. 강한 골드바흐 추측

### A. 선언 명제: `PrimeOrderingUniquePrefixRealizabilityCriterion`

소수 `q>=5`, `(1-X)^m mod (X^q-1)`의 cyclic coefficient `c`가 TICKET-252의
zero-residue compatibility를 만족한다고 하자. 다음을 둔다.

```text
t=1-c_0, N*=c+t, T=qt.
```

실제 prime-count vector `N_r(X)`가 centered nonzero Fourier data
`q(1-zeta_q^a)^m`을 갖는 `X`가 존재할 필요충분조건은 처음 `T`개 소수의
residue-count vector가 정확히 `N*`인 것이다.

### B-D. 정의·증명·추론 감사

TICKET-252 Fourier inversion은 `N_r(X)=c_r+t`를 강제하고 `N_0(X)=1`은
`t=1-c_0`을 강제한다. 합하면 `pi(X)=qt=T`다. Prime count는
`p_T<=X<p_(T+1)`에서 일정하므로 검사할 prefix는 하나뿐이다. 반대로 그
prefix가 `N*`이면 이 구간의 모든 `X`가 원하는 vector와 Fourier data를
실현한다.

### E-G. 적대적·재현 계산

다음 compatible tail 10개를 검사했다.

```text
(q,m)=(5,8..12), (7,12..16).
```

가장 긴 강제 prefix는 소수 79,240개다. Exact Eratosthenes sieve와 integer
residue count로 모든 행을 배제했다. `(5,8)`에서 강제 vector
`(1,76,76,1,126)`와 처음 280개 소수 vector의 L1 거리는 `142`다. 실패 0.
SHA-256:
`a14b831094b7733f9186b166b2346c3e295617c705ded50c46ef38a62994e0ff`.

### H-I. 유한 한계와 분류

iff criterion은 각 compatible `(q,m)`에 대해 일반적이다. 계산으로 배제한
것은 명시한 10개뿐이다. 모든 compatible exponent에 대한 uniform
discrepancy 정리는 없다. 분류는 `partial_theorem`; 강한 Goldbach는
`open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

```text
UniformPrimePrefixDiscrepancyExcludesEveryCompatibleCyclotomicTail
```

## 4. 쌍둥이 소수 추측 — 심층 집중

### A. 선언 명제: `RightEvenContaminationReducesToEightyFourLebesgueNagellExponents`

Katz--Pratt의 1차 자료
[On the Lebesgue--Nagell equation x^2-2=y^p](https://arxiv.org/abs/2507.12397v2)에
명시된 외부 결과를 사용한다. 양의 비자명해는 소수 지수 `ell<=13` 및
`ell>911`에서 배제되고, 논문이 인용한 Chen 합동 정리를 합치면
`ell=13,17,19,23 mod 24`만 남으며, 모든 비자명 base는 `10^1000`보다 크다.

홀수 소수 `p,r`, 홀수 `k>=3`, `m>=1`이

```text
p^k+2=r^(2m)
```

을 만족하면 `k`의 모든 소인수 `ell`은

```text
P={ell prime: 17<=ell<=911,
                  ell mod 24 in {13,17,19,23}},     (TP-253)
```

에 속한다. `#P=84`이고 `p^(k/ell)>10^1000`이다.

### B-D. 정의·증명·외부 의존성 감사

`x=r^m`으로 둔다. 임의의 소인수 `ell|k`에 대해 `y=p^(k/ell)>0`으로 두면
오염식은 `x^2-2=y^ell`인 비자명 Lebesgue--Nagell 해가 된다. 인용한 지수
제한·합동 제한·하한을 적용하면 (TP-253)을 얻는다. `ell`이 임의였으므로
`k`의 모든 소인수가 `P`에 속한다.

외부 자료는 2025-07-25의 arXiv v2다. PrimeProject는 factor reduction과
`P`의 열거만 독립 검증하며 논문의 linear forms, Thue equation, modular
입력을 재증명하지 않는다. 원 논문도 84개 소수 지수를 미해결로 명시한다.

### E-G. 적대적·재현 계산

Trial-division primality와 residue filter로 84개를 독립 열거했다. 합동류
`13,17,19,23 mod 24`별 개수는 `20,20,23,21`이다. 별도 factor scan은
`3<=k<=9999`의 홀수 4,999개를 분류해 331개가 `P`의 소인수만 갖고,
4,668개가 factor 조건으로 배제됨을 확인했다. 이 유한 scan은 all-`k`
증명이 아니다. 실패 0. SHA-256:
`b98e7851ac77f39a65148a17da8a40600d25774928d13483a1fcef4d4b7b8bb6`.

### H-I. 유한·논리 한계

새 정리는 오염 frontier를 엄밀히 줄이지만 남은 84개 prime-exponent
방정식 중 어느 것도 배제하지 않는다. 검토한 1차 preprint에 의존하는
`partial_theorem`이며 Lebesgue--Nagell 방정식의 독립 완전해가 아니다.
Type-II twin lower bound도 손대지 않았다. Twin Prime은
`open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

```text
LebesgueNagellExponent17HasNoPositiveSolution
```

## 최종 분류

새로 확정: partial theorem 3개와 exact no-go 1개. 네 proof DAG는 모두
acyclic이고 open frontier가 하나씩 있다. 해결 후보 0, 해결 0이다.
