# TICKET-251: 내부 집중, 유한 소수 CRT, cyclotomic 집중, 우측 짝수지수의 mod 8 제약

- 부모: TICKET-250
- `iteration_complete`: true
- `program_complete`: false
- `resolved_count`: 0
- `candidate_resolution_count`: 0
- 분류: `exact_no_go` 3개, `partial_theorem` 1개
- 심층 집중: 강한 골드바흐 추측
- 네 상위 문제: 모두 `open_not_proven`

TICKET-251은 프로젝트 내부 보조정리 네 개를 증명한다. 리만 가설,
콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느 것도
증명하거나 반증하지 않았다. 회차 완료는 이번에 선언한 명제·계산·감사
산출물이 완성되었다는 뜻일 뿐이다.

## 재현 명령

```powershell
python scripts/ticket251_interior_crt_cyclotomic_righteven.py
python -m unittest tests.test_ticket251_interior_crt_cyclotomic_righteven -v
python scripts/verify_ticket251_structure.py
python scripts/verify_ticket250_structure.py
python scripts/verify_open_problem_structure.py
node --check assets/ticket251-open-problem.js
node --check assets/open-problems.js
node scripts/verify_pages.cjs
```

생성기는 결정적이며 난수를 쓰지 않는다. 정수와 `Fraction` 필드가 증명
인증서다. Goldbach 행의 삼각함수 소수값은 `display_only_nonproof`이고,
엄격한 비율 및 극한은 해석적으로 증명한다.

| 문제 | TICKET-251에서 결정한 정확한 명제 | 분류 | 상위 상태 |
|---|---|---|---|
| 리만 | 내부 영점을 가진 모든 연속·짝·비음수 국소 multiplier는 raw moment form의 전체 단위구 coercivity에 실패 | `exact_no_go` | `open_not_proven` |
| 콜라츠 | 임의의 유한 소수 집합에서 원하는 Fermat quotient 값을 2, 3의 lift와 CRT로 동시에 실현 가능 | `exact_no_go` | `open_not_proven` |
| 강한 골드바흐 | 비음수 정수 중심벡터가 full reduced Fourier support와 nonzero norm을 유지하면서 두 켤레 주파수로 에너지를 집중 가능 | `exact_no_go` | `open_not_proven` |
| 쌍둥이 소수 | `p^k+2=r^(2m)`이면 `k`가 홀수이고 `p=7 mod 8`; mod 8만으로 `k=1`은 강제 불가 | `partial_theorem` | `open_not_proven` |

## 1. 리만 가설

### A. 선언 명제: `InteriorZeroLocalMultiplierCoercivityNoGo`

`H=L2_even([-1,1])`이고

```text
Q0(f)=sum_(k>=0)|integral x^(2k)f(x)dx|^2
```

라 하자. `w`가 연속, 짝, 비음수, 비영이고 어떤 `x0 in [0,1)`에서
`w(x0)=0`이면 `M_w`는 bounded, self-adjoint, noncompact이지만

```text
inf_(||f||=1)(Q0(f)+<M_w f,f>)=0.                     (RH-251)
```

### B-D. 증명과 추론 감사

`rho<1`인 범위에서 `{−x0,x0}`의 축소 대칭 근방 `E_delta`를 잡고
`g_delta=1_E/sqrt(|E|)`로 둔다. 연속성으로

```text
<M_w g_delta,g_delta><=sup_E w ->0.
```

또 각 `k`에 대해

```text
|integral x^(2k)g_delta|^2<=|E|rho^(4k),
Q0(g_delta)<=|E|/(1-rho^4)->0.
```

비영 연속함수 `w`는 양의 측도를 가진 대칭 영역에서 아래로 양수이다.
그 영역을 서로소 대칭 부분집합으로 나눈 정규화 지시함수들의 상은
직교하고 norm이 0에서 떨어져 있으므로 `M_w`는 noncompact이다.

### E-G. 적대적·재현 계산

`w=(x^2-1/9)^2`, `x0=1/3`, `delta=2^(-s)`, `s=3,...,13`에 대해

```text
<M_w g,g><=(2delta/3+delta^2)^2,
Q0(g)<=4delta/(1-(1/3+delta)^4)
```

의 정확한 유리수 인증서 11개를 기록했다. 실패 0.

- SHA-256:
  `e79a0c6278dedf06d33bbd79125d059adf86c1f2ae1f252afbae78daf5d3ffcd`.

### H-I. no-go 범위와 유한 한계

폐기: 내부 영점이 있는 연속 비음수 **국소** multiplier를 전체 단위구
coercivity 복구로 쓰는 경로. `w>=c>0`, 끝점에만 영점이 있는 경우,
비국소 kernel, 실제 Guinand-Weil admissible closure는 다루지 않았다.
RH는 `open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

```text
NonlocalArithmeticWeilKernelExcludesInteriorConcentration
```

## 2. 콜라츠 추측

### A. 선언 명제: `FinitePrimeCanonicalLiftPatternCRTInterpolationNoGo`

`q>5`인 소수의 임의의 유한 비공집합 `S`와 임의의
`(u_q,v_q) in F_q^2`에 대해 `M=product q^2`를 법으로 하는 유일한
쌍 `(A,B)`가 존재하여

```text
A=2 mod q, B=3 mod q,
F_q(A)=u_q, F_q(B)=v_q,
F_q(x)=(x^(q-1)-1)/q mod q.                           (CO-251)
```

### B-D. 증명과 추론 감사

TICKET-250의 정확한 항등식은

```text
F_q(a+kq)=F_q(a)-k/a mod q.
```

따라서 유일한 lift 지수는

```text
k_q=2(F_q(2)-u_q), ell_q=3(F_q(3)-v_q) mod q.
```

`A=2+k_q q`, `B=3+ell_q q mod q^2`를 CRT로 결합하면 (CO-251)을
얻는다. `[3:5]` 위·밖의 target을 골라 임의의 유한 hit/avoidance 패턴을
실현할 수 있다.

### E-G. 적대적·재현 계산

크기 2~4의 소수 집합과 `(3,5)`, `(0,0)`, `(1,0)`, `(1,1)` target을
사용한 정확한 CRT 4건을 modular exponentiation으로 재검증했다. 실패 0.

- SHA-256:
  `c184a69eaebae32ffdc9e9043ca4864bf7615e5933a225721616dcda732e2fdc`.

### H-I. no-go 범위와 유한 한계

폐기: 유한 개 lift-compatible local 조건으로 canonical cross-prime 거동을
추론하는 경로. 구성한 `A,B`는 `S`에 의존하며 고정 대표 `2,3`이 아니다.
`(F_q(2),F_q(3))`의 occurrence, avoidance, density 또는 일반 Collatz
궤도는 결정하지 못한다. Collatz는 `open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

```text
CanonicalRepresentativeFermatQuotientDistributionBeyondFiniteCRTInterpolation
```

## 3. 강한 골드바흐 추측 — 심층 집중

### A. 선언 명제: `CyclotomicUnitFullSupportEnergyConcentrationNoGo`

홀수 소수 `q>=5`, `m>=1`에 대해

```text
c_r=sum_(j=r mod q)(-1)^j binom(m,j),
C=-min c_r, n_r=C+c_r, N=sum n_r, Delta_r=q n_r-N
```

로 두면 `n_r`은 비음수 정수, `sum Delta_r=0`이고

```text
F_m(a)=sum_r Delta_r zeta_q^(ar)=q(1-zeta_q^a)^m !=0,
product_(a=1)^(q-1)F_m(a)=q^(q-1+m).                  (GB-251a)
```

최대 켤레쌍 `A*={(q-1)/2,(q+1)/2}`에 대해

```text
E_out/E_A* <= (q-3)/2 rho_q^m ->0,
rho_q=cos^2(3pi/(2q))/cos^2(pi/(2q))<1.               (GB-251b)
```

### B-D. 증명과 추론 감사

`(1-X)^m mod (X^q-1)`의 계수가 `c_r`이고 그 합은 `(1-1)^m=0`이다.
그러므로 `N=qC`, `Delta_r=qc_r`이다. `zeta_q^a`에서 평가하면
(GB-251a)의 첫 식을 얻고 `product_a(1-zeta_q^a)=q`가 norm 식을 준다.
또

```text
|F_m(a)|^2=q^2(4sin^2(pi a/q))^m.
```

최댓값 두 개 이외에는 `cos^2(3pi/(2q))` 이하이므로 (GB-251b)가
성립한다.

### E-G. 적대적·재현 계산

`q=5,7,11,13`, `m=1,2,3,5,8,13,21,34`의 32건에서 순환 이항계수,
비음수성, 중심성, exact Parseval integer `q^3 sum c_r^2`, norm
`q^(q-1+m)`을 검증했다. 삼각함수 소수값은 표시 전용이다. 실패 0.

- SHA-256:
  `e3c9e81aab8500e964f265aa6ba8bd91105d40f67e1f5c7938f63bb88bcaa857`.

### H-I. no-go 범위와 유한 한계

폐기: centeredness, integrality, nonnegativity, full reduced support,
nonzero Galois norm만으로 정량 Fourier anti-concentration을 얻는 경로.
이 벡터가 실제 prime-count 또는 logarithmic-weight residue vector인 것은
증명하지 않았다. 강한 Goldbach는 `open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

```text
ActualPrimeCountResidueVectorsExcludeCyclotomicUnitConcentration
```

## 4. 쌍둥이 소수 추측

### A. 선언 명제: `RightEvenModuloEightConstraintAndSharpness`

홀수 소수 `p,r`, `k,m>=1`에 대해

```text
p^k+2=r^(2m)이면 k는 홀수이고 p=7 mod 8이다.          (TP-251a)
```

역방향의 합동 수준에서는 모든 홀수 `k`와 `p=7 mod 8`에 대해

```text
p^k+2=1 mod 8.                                        (TP-251b)
```

따라서 mod 8만으로 `k=1`을 강제하거나 홀수 합성지수 왼쪽 항을 배제할
수 없다. 역방향은 합동 적합성일 뿐 정수해의 존재 주장이 아니다.

### B-D. 증명과 철회 출처 감사

모든 홀수 제곱은 `1 mod 8`이다. `k`가 짝수이면 `p^k=1 mod 8`이므로
좌변이 `3 mod 8`이라 모순이다. 따라서 `k`는 홀수다. 이때
`p^k=p mod 8`이므로 `p+2=1 mod 8`, 즉 `p=7 mod 8`이다. 반대로 홀수
`k`와 `p=7 mod 8`이면 `p^k+2=1 mod 8`이어서 이 합동 경로의 한계가
정확히 드러난다.

이전 초안이 의존했던 [arXiv:2008.11515](https://arxiv.org/abs/2008.11515)의
원 기록은 major mistake로 철회되었다고 명시한다. 이를 증명 의존성으로
사용하지 않으며, 더 강한 all-X `k=1` 분류 주장은 제거했다.

### E-G. 적대적·재현 계산

천만 이하 exact prime-power support에서 right-even active pair는 124개이며
우연히 모두 왼쪽 지수가 1이다. 예: `7->9`, `23->25`, `79->81`,
`727->729`. 모든 행은 증명된 mod 8 조건을 만족한다. 합성 왼쪽 항이
발견되지 않은 사실은 유한 증거일 뿐이다. 실패 0.

- SHA-256:
  `2881e5c20c714c52c8502ea5ec74617bed8bbc110c35069c488e960a4d711e85`.

### H-I. 부분정리 범위와 유한 한계

폐기: 철회된 출처를 정리로 사용하거나 mod 8 조건이 `k=1`을 강제한다고
주장하는 경로. 홀수 `k>=3`에 대한 all-X 방정식 `x^2-2=p^k`는 여기서
해결하지 못했다. 유한 스캔과 합동 정리는 sieve lower bound나 쌍둥이
소수 무한성을 주지 않는다. 쌍둥이 소수 추측은 `open_not_proven`이다.

### J-K. 남은 간극과 다음 단일 보조정리

```text
NoPositivePrimePowerSolutionsOfXSquareMinusTwoEqualsYOddPower
```

## 최종 분류

새로 확정: exact route no-go 3개와 초등적 partial theorem 1개.
폐기: 위에서 명시한 네 경로. 남음: 문제마다 하나씩인 proof-DAG open
frontier 4개. 상위 난제의 candidate resolution은 0개이므로 형식적 해결
감사를 시작하지 않는다.
