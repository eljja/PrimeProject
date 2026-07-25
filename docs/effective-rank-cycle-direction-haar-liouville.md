# TICKET-142: Effective Rank, Cycle Direction, Haar Duals, and Liouville Parity

Date: 2026-07-25

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket142-effective-rank-cycle-direction-haar-liouville.json`

## Publication boundary / 논문 제출용 경계

**English.** TICKET-142 proves four exact intermediate or proof-route no-go
theorems. It also corrects two malformed TICKET-141 targets: the Collatz product
window supplies an upper bound on a hypothetical cycle minimum, not a lower
bound, and positive twin mass cannot be appended to a generic minor-arc estimate
without supplying the parity-sensitive theorem that is essentially missing.
No literature-priority claim is made. None of the four conjectures is proved or
refuted.

**한국어.** TICKET-142는 네 개의 정확한 중간정리 또는 증명 경로
no-go 정리를 확정한다. 동시에 TICKET-141의 잘못 설정된 두 목표를
수정한다. 콜라츠 product window는 가상 순환 최솟값의 하한이 아니라
상한을 주며, 일반적인 minor-arc 상계 뒤에 양의 쌍둥이 소수 질량을
추가하려면 바로 그 미해결 parity-sensitive 정리를 별도로 공급해야 한다.
학계 최초성을 주장하지 않으며 네 추측 중 어느 것도 증명하거나
반증하지 않는다.

## Result table / 결과표

| Problem / 문제 | Exact result / 정확 결과 | Discarded route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `EffectiveRankShiftedMomentIdentityAndSharpLogCoefficientNoGo` | coefficient-free `O(log rank)` shifted-moment promotion | `ExplicitProjectedWeilFiniteSectionAndTailConvergenceContract` |
| Collatz / 콜라츠 | `PrimitiveCycleSuccessorDistinctProductUpperBoundAndTargetCollapseNoGo` | extracting a minimum lower bound from the product window | `Period15601AffineNumeratorNondivisibilityCertificate` |
| Goldbach / 골드바흐 | `RobustDualBasisChangeInvarianceAndHaarK56Reduction` | treating orthogonalization alone as a robustness gain | `UniformEvenGoldbachHaarScaleBudgetBelow56` |
| Twin Prime / 쌍둥이 소수 | `CubicRoughnessLiouvilleExactTwinProjector` | unsigned minor-arc cancellation as positive gap-two mass | `OneSidedCubicRoughLiouvilleLedgerGap` |

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `E=E*`, `lambda_max(E)<=R`, `g>0`, `T=R+g`, and

```text
F=RI-E >= 0,  q=2m,  s=||F||.
```

For `s>0`, define the `q`-effective rank

```text
kappa_q = tr(F^q)/s^q.
```

Then

```text
1 <= kappa_q <= rank(F)
tr(F^q) = s^q kappa_q.
```

If `A=gI` and `eta=1-s/T`, then

```text
A+E>0       iff eta>0,
tr(F^q)<T^q iff (1-eta)^q kappa_q<1.
```

Consequently, if only `kappa_q<=r` is known, the condition

```text
q > log(r)/(-log(1-eta))
```

is sufficient, and its rank coefficient is sharp for scalar `F`.

한국어로, shifted moment의 크기는 spectral edge와 유효 rank의 정확한
곱이다. 단순히 차수가 `O(log r)`이라고 쓰는 것만으로는 충분하지 않고,
그 계수와 상대 spectral margin 또는 `kappa_q` 상계가 필요하다.

### Proof / 증명

`F`의 고유값을 `0<=mu_i<=s`라 하자. 하나 이상의 고유값은 `s`이므로

```text
kappa_q = sum_i (mu_i/s)^q
```

는 1과 rank 사이에 있고 trace 항등식은 정의에서 바로 나온다. 또한

```text
lambda_min(gI+E)=g+R-s=T-s=eta T.
```

마지막 동치는 trace 항등식을 `T^q`로 나누면 얻는다. `F=sI_r`이면
`kappa_q=r`이므로 rank만 사용하는 최악 경우 계수는 개선할 수 없다.
`QED`

### Exact no-go family / 정확 no-go 반례족

모든 `k>=1`에 대해

```text
r=4^k, R=0, g=1, A=I_r, E=-(1/2)I_r, m=k
```

로 둔다. `A+E=(1/2)I_r>0`이지만

```text
tr((-E)^(2m)) = 4^k (1/2)^(2k) = 1
```

이므로 strict certificate는 경계에서 실패한다. `m=k+1`에서는 정확히
`1/4`이 되어 통과한다. 따라서 “양의 margin과 `O(log r)` 차수면
자동으로 충분하다”는 계수 없는 경로를 폐기한다.

### Remaining gap / 남은 간극

저장소에는 아직 실제 projected Weil 유한절단 `(A_r,E_r)`, 투영 기저,
`g_r,R_r`, tail 규칙, 유한절단 양성에서 전체 Weil core 양성으로 가는
수렴 정리가 정의되어 있지 않다. 기존 `formal/*/InfiniteBridge.lean`은
proof DAG 상태 문자열이며 Lean 증명 그 자체가 아니다.

다음 단일 보조정리:
`ExplicitProjectedWeilFiniteSectionAndTailConvergenceContract`.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

가속 홀수 Collatz 사상

```text
T(n)=(3n+1)/2^v2(3n+1)
```

의 원시 비자명 양의 `k`-cycle이 있다고 가정하고 그 서로 다른 홀수
항의 최솟값을 `m`이라 하자. 다음을 정의한다.

```text
s_k=ceil(k log_2 3)
q_k=2^s_k/3^k
B_k=1/(3(q_k^(1/k)-1)).
```

그러면 반드시

```text
m < B_k,  m = 3 mod 4.
```

또한 `u=(3m+1)/2`이고, `A_k(m)`을 `m,u`를 포함하는 가장 작은 서로
다른 홀수 `k`개로 만들면

```text
2^s_k product_(x in A_k(m)) x
 <= product_(x in A_k(m)) (3x+1).                 (1)
```

### Proof / 증명

각 순환 단계 `2^a_i n_(i+1)=3n_i+1`을 모두 곱하면

```text
2^S/3^k = product_i (1+1/(3n_i)) > 1.
```

따라서 `S>=s_k`이고

```text
q_k <= product_i (1+1/(3n_i))
    < (1+1/(3m))^k,
```

여기서 마지막 strict 부등식은 비자명 원시 순환의 항들이 모두 `m`일 수
없기 때문이다. 이를 `m`에 대해 풀면 `m<B_k`다.

최솟값 직후의 valuation이 2 이상이면

```text
T(m) <= (3m+1)/4 < m
```

이므로 모순이다. 따라서 valuation은 정확히 1이고
`u=(3m+1)/2`, `m=3 mod 4`다. 함수 `1+1/(3x)`가 감소하므로 실제
서로 다른 순환 항의 곱은 `A_k(m)`에서 최대가 된다. 여기에 `q_k` 하계를
대입하고 `3^k`를 소거하면 (1)을 얻는다. `QED`

### Direction correction / 방향 교정

TICKET-141의 다음 목표였던 “cycle minimum이 exact window threshold보다
크다”는 명제는 product-window에서 도출할 수 없다. product-window가
주는 것은 반대 방향인 `m<B_k`다. `1 -> 1`을 포함하면 원래 문장은
즉시 거짓이고, 원시 비자명 cycle로 제한한 뒤 `m>B_k`를 증명하는 것은
필요조건과 모순을 만들어 cycle 자체를 배제하는 종결 명제이지 독립적인
중간 하한이 아니다.

### Exact computation / 정확 계산

`s_k=(3^k).bit_length()`와 정수 곱의 부호만 사용했다.

| `k` | `s_k` | (1)을 만족하는 최대 `m=3 mod 4` |
|---:|---:|---:|
| 16 | 26 | 3 |
| 64 | 102 | 11 |
| 256 | 406 | 279 |
| 1,024 | 1,624 | 31 |
| 4,096 | 6,493 | 131 |
| 15,601 | 24,727 | 285,795,879 |
| 16,384 | 25,969 | 579 |
| 20,000 | 31,700 | 1,847 |

기존 검증 하한 `2^28`과 결합해도 `k=15,601`에서는
`268,435,459 <= m <= 285,795,879`에 `4,340,106`개의 최솟값 후보가
남는다. 이는 valuation word 수나 cycle 수가 아니다.

다음 단일 보조정리:
`Period15601AffineNumeratorNondivisibilityCertificate`.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

측정행렬 `A`, 공동 오차집합 `U`, 목표 좌표 `j`에 대해

```text
C_j(A,U)=sup{|f_j|: Af in U}
```

라 하자. 모든 가역행렬 `T`에 대해

```text
C_j(TA,TU)=C_j(A,U).
```

또한 직교행렬 `Q`, `c=Q rho`, `|c_k|<=epsilon_k`이면

```text
sup |rho_j| = sum_k |Q_kj| epsilon_k.
```

`n=2^d` 정규직교 Haar 기저의 각 점에는 scaling 함수 하나와 척도별
wavelet 하나만 작용하므로 균일 계수 예산 `epsilon`의 점별 증폭은

```text
L_d epsilon,
L_d=2^(-d/2)+sum_(ell=1)^d 2^(-ell/2) < 1+sqrt(2).
```

따라서 계수 예산 23은 모든 dyadic 크기에서 점별 56 미만을 준다.

### Proof / 증명

첫 항등식은

```text
Af in U iff TAf in TU
```

에서 즉시 나온다. 두 번째 항등식의 상계는 `rho=Q^T c`의 삼각부등식,
등호는 각 `c_k`를 `Q_kj`의 부호에 맞춰 선택하면 얻는다. Haar row의
비영 계수를 척도별로 합하면 `L_d`가 나온다.

```text
23(1+sqrt(2))<56
```

은 `23sqrt(2)<33`, 즉 `2*23^2=1058<1089=33^2`와 동치다.
반면 `24(1+sqrt(2))>56`이고 실제 `d=9`부터 24 예산은 56을 넘는다.
조밀한 Hadamard 직교기저의 row `l1`은 `sqrt(n)`이므로 직교성만으로는
충분하지 않다. `QED`

### K=56 boundary / K=56 경계

여기서 `K=56`은 moment 차수도 cutoff도 아니다. 프로젝트가 요구하는
정규화 Goldbach 점별 잔차 상수다.

```text
|R(N)| <= 56 N/log N.
```

TICKET-129의 endpoint 여유는 정확히

```text
131917/100000 - 140/107 - 38829/20000000000
 = 23019645297/2140000000000 > 0.
```

raw moment를 단순 직교화하면서 실제 transformed joint error set 대신
새로운 작은 독립 box를 가정하는 것은 기저변환이 아니라 새로운 산술
정리를 몰래 추가하는 것이다.

### Remaining gap / 남은 간극

실제 Goldbach 잔차의 Haar scaling coefficient와 각 wavelet scale
maximum을 필요한 예산 아래에 두는 정리가 없다. scaling mode를 빼면
상수 잔차가 보이지 않으므로 반드시 포함해야 한다.

다음 단일 보조정리:
`UniformEvenGoldbachHaarScaleBudgetBelow56`.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

`X>=2`, `z=(2X+2)^(1/3)`라 하자. `R_X(m)`은 `m`의 모든 소인수가
`z`보다 클 때 1인 roughness 지시자이고, `lambda(m)=(-1)^Omega(m)`는
Liouville 함수다. 모든 `X<=n<=2X`에서

```text
1_prime(n)1_prime(n+2)
 = R_X(n)R_X(n+2)
   (1-lambda(n))(1-lambda(n+2))/4.
```

따라서

```text
4 pi_2[X,2X] = A00-A10-A01+A11,
Aij=sum R_X(n)R_X(n+2) lambda(n)^i lambda(n+2)^j.
```

### Proof / 증명

`m<=2X+2`가 `z`-rough인데 중복도를 포함한 소인수가 세 개 이상이면
그 곱은 `z^3=2X+2`보다 커져 모순이다. 따라서 `Omega(m)`은 1 또는
2다. 이 support에서는 `lambda(m)=-1`과 `Omega(m)=1`, 즉 `m`이
소수라는 조건이 동치다. 두 좌표의 projector를 곱하고 전개하면 ledger
항등식을 얻는다. `QED`

### Reproducible finite ledger / 재현 가능한 유한 ledger

| `X` | `A00` | `A10` | `A01` | `A11` | 복원된 twin 수 |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 59 | -17 | -19 | 9 | 26 |
| 10,000 | 358 | -104 | -84 | 2 | 137 |
| 100,000 | 2,486 | -564 | -556 | 138 | 936 |
| 1,000,000 | 17,634 | -3,970 | -3,992 | 1,212 | 6,702 |

SPF와 재귀식 `lambda(n)=-lambda(n/spf(n))`만 사용했으며 직접 센
쌍둥이 소수 개수와 모든 행에서 정확히 일치한다.

### Parity and minor-arc no-go / parity 및 minor-arc no-go

동일한 rough support에 parity 표지를 모두 `+1`로 주면 projector
질량은 0이고, 모두 `-1`로 주면 rough-pair 질량 전체가 남는다. 따라서
unsigned divisor 정보만으로는 혼합항 `A10,A01,A11`을 결정할 수 없다.
이는 실제 Liouville 함수의 반례가 아니라 parity-blind 정보 클래스의
반례다.

또한 `c_X(n)=1_(3 divides n)`은 gap 2 pair가 정확히 0이지만
`||3 alpha||>=delta`인 minor arc에서는 기하급수 공식으로

```text
|sum c_X(n)e(alpha n)| <= 1/(2 delta).
```

즉 generic minor-arc power saving만으로 양의 gap-two mass는 나오지
않는다. denominator 3의 major arc와 parity-sensitive 부호가 필요하다.

다음 단일 보조정리:
`OneSidedCubicRoughLiouvilleLedgerGap`.

## Cross-problem conclusion / 문제 간 결론

**English.** TICKET-142 replaces four underspecified or over-compressed targets
with typed quantitative objects: effective spectral rank, an upper cycle
window with affine divisibility, a Haar coefficient ledger, and a one-sided
Liouville parity ledger. The gain is not a conjecture resolution; it is the
removal of one direction error, two undefined contracts, and one circular
positive-mass target.

**한국어.** TICKET-142는 불완전하거나 과도하게 압축된 네 목표를
정량 객체로 교체했다. 각각 유효 spectral rank, affine divisibility와
결합한 순환 상한, Haar 계수 ledger, 단측 Liouville parity ledger다.
이는 난제 해결이 아니라 부등호 방향 오류 하나, 미정의 계약 두 개,
순환적인 양의 질량 목표 하나를 제거한 결과다.

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket142_effective_rank_cycle_direction_haar_liouville.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket142_effective_rank_cycle_direction_haar_liouville
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

Expected machine summary:

```text
exact_theorem_count=4
route_correction_count=4
proof_dag_count=4
conjecture_resolution_count=0
total_failure_count=0
```

## Literature boundary / 문헌 경계

- RH remains an official Millennium Prize problem:
  [Clay Mathematics Institute](https://www.claymath.org/millennium-problems/riemann-hypothesis/).
- Tao's theorem concerns almost all Collatz orbits in logarithmic density, not
  every orbit:
  [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562).
- Helfgott proves ternary Goldbach; the binary pointwise problem attacked here
  is different:
  [The ternary Goldbach conjecture is true](https://arxiv.org/abs/1312.7748).
- The large-sieve input retained from TICKET-141 is classical:
  [Montgomery and Vaughan, *The large sieve*](https://doi.org/10.1112/S0025579300004708).
- The parity obstruction in bounded-gap sieve work is discussed in:
  [Polymath, Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897).

These references delimit standard inputs and the current state of adjacent
work. PrimeProject claims only the explicit TICKET-142 synthesis, exact replay,
target corrections, and machine-audited proof boundaries.
