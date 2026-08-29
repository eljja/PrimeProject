# TICKET-252: 희소 스펙트럼 도주, marginal-joint no-go, 0 residue 호환성, 유한 합동 국소해

- 부모: TICKET-251
- `iteration_complete`: true
- `program_complete`: false
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- 분류: `exact_no_go` 3개, `partial_theorem` 1개
- 심층 집중: 강한 골드바흐 추측
- 네 상위 문제: 모두 `open_not_proven`

TICKET-252는 프로젝트 내부 보조정리 네 개를 증명한다. 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않았다. 회차 완료는 이번 명제·계산·proof DAG·공개
산출물이 명시한 검증 계약을 통과했다는 뜻일 뿐이다.

## 재현 명령

```powershell
python scripts/ticket252_sparse_marginal_zeroresidue_local.py
python -m unittest tests.test_ticket252_sparse_marginal_zeroresidue_local -v
python scripts/verify_ticket252_structure.py
python scripts/verify_ticket251_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket252-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

모든 재생 계산은 정수 또는 유리수이고 random seed는 없다. rational
record의 float 표시는 증명에 쓰지 않으며 테스트는 numerator와
denominator만 사용한다.

| 문제 | TICKET-252에서 판정한 정확한 명제 | 분류 | 상위 상태 |
|---|---|---|---|
| 리만 | 무한·대칭·영밀도 Fourier projection도 positive/noncompact/nonlocal이면서 내부 집중 도주를 허용 | `exact_no_go` | `open_not_proven` |
| 콜라츠 | 두 좌표 marginal이 정확히 균등해도 결합 projective slope `[3:5]`의 질량은 결정되지 않음 | `exact_no_go` | `open_not_proven` |
| 강한 골드바흐 | prime 0-residue 조건은 `c_0-min c<=1`과 동치이며 모든 `1<=m<q`를 배제하지만 tail 전체는 배제하지 못함 | `partial_theorem` | `open_not_proven` |
| 쌍둥이 소수 | 모든 고정 `M`에서 `p^k+2=r^(2m) mod M`인 prime residue 후보가 존재하므로 유한 합동 obstruction만으로 all-X 방정식을 닫을 수 없음 | `exact_no_go` | `open_not_proven` |

## 1. 리만 가설

### A. 선언 명제: `SparseFourierProjectionInteriorConcentrationNoGo`

```text
H=L2_even([-1,1]),
Q0(f)=sum_(k>=0)|integral x^(2k)f(x)dx|^2
```

라 하자. 비영 정수의 무한 대칭 집합 `S`가

```text
#(S intersect [-N,N])=o(N)
```

을 만족하고 `P_S`가 normalized Fourier mode
`2^(-1/2)exp(pi i n x)`, `n in S`로의 직교 projection이면, `P_S`는
bounded, positive, self-adjoint, noncompact이고 multiplication operator가
아니지만

```text
inf_(||f||=1)(Q0(f)+<P_S f,f>)=0.                    (RH-252)
```

### B-D. 정의·증명·추론 감사

`g_delta=(2delta)^(-1/2)1_[-delta,delta]`로 두면 짝이고 norm이 1이며

```text
|<g_delta,e_n>|^2=delta sinc(pi n delta)^2.
```

`S`를 `A/delta`에서 나누면 낮은 주파수 합은
`delta o(1/delta)=o(1)`이고 전체 정수로 넓힌 tail은

```text
(1/(pi^2 delta))sum_(|n|>A/delta)1/n^2=O(1/A).
```

먼저 `delta->0`, 이어 `A->infinity`로 보내면 projection energy가 0으로
간다. 동시에 `Q0(g_delta)<=2delta/(1-delta^4)->0`이다. `S`가 무한이므로
projection은 infinite rank라 noncompact이다. `0 notin S`이므로
`P_S(1)=0`이지만 `P_S!=0`; 따라서 multiplication operator일 수 없다.

### E-G. 적대적·재현 계산

`S={plus/minus 2^j}`와 `delta=2^(-s)`, `s=3,...,14`에서

```text
low <=2delta(s+1), tail <2delta/27,
Q0<=2delta/(1-delta^4)
```

의 정확한 유리수 upper bound 12개를 검증했다. 전부 감소하고 실패는 0.

- SHA-256:
  `3e7c26600452d330e977e7880ca71b028709cad8966df6c63c41be6a1e910294`.

### H-I. no-go 범위와 유한 한계

폐기: noncompact/nonlocal이라는 사실 또는 무한 희소 spectral support만으로
내부 집중 배제를 주장하는 경로. 이 abstract periodic projection은 실제
Weil form이 아니다. RH는 `open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

```text
ActualWeilKernelHasPositiveDensityAgainstEveryInteriorWavePacket
```

## 2. 콜라츠 추측

### A. 선언 명제: `UniformMarginalsCannotDetectProjectiveFermatSlopeNoGo`

모든 소수 `q>5`에 대해 `F_q^2` 위 다음 두 확률분포는 `U`, `V`
marginal이 모두 정확히 균등하지만 separated `[3:5]` 질량은 다르다.

```text
mu_hit:  (U,V)=(3t,5t), mass=(q-1)/q,
mu_miss: (U,V)=(t,t),   mass=0.                       (CO-252)
```

### B-D. 정의·증명·추론 감사

3과 5의 곱셈은 `F_q`의 순열이므로 hit graph의 두 marginal이 균등하다.
diagonal graph도 같다. 첫 graph의 비영점은 전부 `t(3,5)`이다. 두 번째
graph에서 target 식은 `5t-3t=2t=0`이어서 원점만 남고 separated target은
없다. 실제 canonical pair `U_q=F_q(2)`, `V_q=F_q(3)`의 exact detector는

```text
I_q=1_(5U_q-3V_q=0)-1_(U_q=0 and V_q=0).
```

따라서 필요한 것은 각 좌표 통계가 아니라 joint additive-character
estimate다.

### E-G. 적대적·재현 계산

`q=7,...,43`의 소수 11개에서 두 graph를 exact enumeration했다. 네
marginal count vector는 모두 all-one이고 target count는 `q-1`, 0이다.
실패 0.

- SHA-256:
  `d134c93741ae3151e80bc4443e7abbbbab5ba578292ade37cef147e17cfb324c`.

### H-I. no-go 범위와 유한 한계

폐기: 두 Fermat quotient의 별도 marginal distribution만으로 `[3:5]`를
결정하는 경로. 구성한 graph measure는 실제 fixed pair의 cross-prime
분포가 아니다. Collatz 궤도는 결정하지 못하며 추측은
`open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

```text
JointFermatQuotientCharacterCancellationAtSlopeThreeFifths
```

## 3. 강한 골드바흐 추측 — 심층 집중

### A. 선언 명제: `PrimeCountZeroResidueCyclotomicCompatibilityCriterion`

소수 `q>=5`, `m>=1`에 대해 `c_r`을
`(1-X)^m mod (X^q-1)`의 cyclic coefficient라 하자. 실제 prime-count를

```text
N_r(X)=#{p<=X:p prime, p=r mod q}, N=sum N_r
```

로 둔다. `N_r`의 centered nonzero Fourier data가 TICKET-251의
`q(1-zeta_q^a)^m`과 같다면, prime 0-residue 필요조건 `N_0 in {0,1}`을
만족하는 비음수 정수벡터가 존재할 필요충분조건은

```text
c_0-min_r c_r<=1.                                    (GB-252a)
```

이다. 모든 `1<=m<q`는 배제된다. 그러나 `(q,m)=(5,8)`에서는

```text
c=(-55,20,20,-55,70),
c+56=(1,76,76,1,126)                                 (GB-252b)
```

이므로 이 조건만으로 tail 전체는 배제할 수 없다. 두 번째 벡터를 실제
prime-count라고 주장하지 않는다.

### B-D. 정의·증명·추론 감사

실제 centered vector는 `Delta_r=qN_r-N`이다. nonzero Fourier coefficient가
같고 두 vector의 합이 0이므로 Fourier inversion으로

```text
qN_r-N=q c_r
```

이다. 따라서 `N_r=c_r+t`, `t=N/q`는 정수다. `epsilon=N_0 in {0,1}`이면
`t=epsilon-c_0`; 비음수성은 어떤 `epsilon`에 대해
`epsilon-c_0+min c>=0`인 것과 같고 이것이 (GB-252a)다. `m<q`이면
`c_0=1`, `c_1=-m`이므로 gap이 적어도 `m+1>=2`다.

### E-G. 적대적·재현 계산

`q=5,7,11,13`, `m=1,...,17`의 68건을 exact integer로 검증했다. 모든
`m<q`가 배제되고 compatible tail은 `(5,8)`부터 나타난다. 실패 0.

- SHA-256:
  `5c95a4a8bf5019dc499a4fc45abcd82b1c10ede06659f59d0d28ee036eb06717`.

### H-I. 부분정리 범위와 유한 한계

새로 전역 배제한 범위는 모든 소수 `q>=5`에 대한 `1<=m<q`다. 폐기한
경로는 0 residue만으로 모든 exponent를 배제한다는 주장이다. compatible
vector의 실제 prime 실현, prime ordering, `X`에 대한 monotonicity,
quantitative discrepancy는 남았다. Strong Goldbach는
`open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

```text
ActualPrimeOrderingExcludesZeroResidueCompatibleCyclotomicTail
```

## 4. 쌍둥이 소수 추측

### A. 선언 명제: `FiniteCongruenceLocalSolubilityNoGoForRightEvenPrimePowers`

모든 `M>=1`, 홀수 `k>=3`, `m>=1`에 대해 서로 다른 홀수 소수 `p,r`의
쌍이 무한히 많아

```text
p=7 mod 8, p^k+2=r^(2m) mod M.                       (TP-252)
```

따라서 고정된 유한 합동 modulus만으로 남은 right-even 방정식의 local
insolubility를 증명할 수 없다.

### B-D. 증명과 외부 의존성 감사

`L=8M`으로 둔다. `plus/minus 1 mod L`은 reduced residue class다.
Dirichlet의 산술진행 소수 정리로 `p=-1 mod L`, `r=1 mod L`인 서로 다른
소수를 고른다. `k`가 홀수이므로 `p^k+2=1 mod M`, `r^(2m)=1 mod M`이고
`p=7 mod 8`이다. 유한 modulus 목록은 lcm 하나로 합친다. 외부 노드는
[Encyclopedia of Mathematics의 Dirichlet 정리](https://encyclopediaofmath.org/wiki/Dirichlet_theorem)에
명시된 reduced arithmetic progression의 무한 소수 정리 하나뿐이다.

### E-G. 적대적·재현 계산

`M=1,...,2310`의 선택된 8개 modulus에서 `plus/minus 1 mod 8M`의 첫
소수를 deterministic trial division으로 찾았다. 모든 residual이 정확히
0이다. 실패 0.

- SHA-256:
  `079a60fde7d3f69814681f455edadebbe8b8d0aaf199e7821a0dad94d3ee02b4`.

### H-I. no-go 범위와 유한 한계

폐기: fixed-modulus local insolubility로 all-X 방정식을 닫는 경로. local
solution은 정수 등식이 아니다. `x^2-2=p^k`, Type-II lower bound,
twin-prime infinitude는 모두 열려 있다. 쌍둥이 소수 추측은
`open_not_proven`이다.

### J-K. 남은 최소 간극과 다음 단일 보조정리

```text
QuadraticUnitCoefficientOneExcludesOddPrimeExponents
```

## 최종 분류

새로 확정: exact route no-go 3개와 partial theorem 1개. 네 proof DAG는
acyclic이고 각각 open frontier 하나를 가진다. 상위 난제 해결 후보 0,
해결 0이다.
