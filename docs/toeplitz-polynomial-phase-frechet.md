# TICKET-146: Toeplitz Reflection, Polynomial Ranks, Fourier Phase, and Frechet Bounds

> Historical boundary: TICKET-147 supersedes the four next targets below.
> The TICKET-146 theorems remain valid with their stated scope.

Date: 2026-07-26

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket146-toeplitz-polynomial-phase-frechet.json`

## Publication boundary / 논문 제출용 경계

**English.** TICKET-146 proves four exact intermediate statements. It does
not prove or disprove any target conjecture. For a shift-generated
convolution-form core it derives a Toeplitz Gram family and the exact Levinson
reflection recurrence, then proves that no fixed lag of moments can certify
all future sections in the unrestricted Hermitian Toeplitz moment class
without extra structural constraints. It excludes every lower-bounded, finite-modulus,
piecewise-polynomial one-step Collatz rank. It proves that Fourier power
spectra do not determine a pointwise binary convolution and therefore cannot
by themselves supply signed Goldbach endpoint cancellation. Finally, it
proves the sharp Frechet bounds for the cubic-rough Liouville ledger and shows
that perfect marginal cancellation does not determine twin mass. No claim of
literature priority is made.

**한국어.** TICKET-146은 네 난제 자체가 아니라 네 개의 정확한
중간정리를 증명한다. shift로 생성된 convolution 형식 core의 Gram
행렬이 Toeplitz가 됨을 보이고 정확한 Levinson reflection 점화식을
도출한 뒤, 고정된 개수의 moment만 보는 규칙으로 모든 후속 절단의
양성을 인증할 수 없음을 추가 제약 없는 Hermitian Toeplitz moment
계열에서 증명한다. 콜라츠에서는 하방 유계이며 고정
유한 residue별 polynomial인 모든 1-step rank를 배제한다. 골드바흐에서는
Fourier power spectrum이 점별 이항 convolution을 결정하지 못하므로,
크기 정보만으로 부호 있는 endpoint 상쇄를 얻을 수 없음을 증명한다.
쌍둥이 소수에서는 cubic-rough Liouville ledger의 최적 Frechet 경계를
도출하고, 주변부 상쇄가 완벽해도 twin 질량은 결정되지 않음을 보인다.
학계 최초성은 주장하지 않는다.

## Result table / 결과표

| Problem / 문제 | New exact result / 새 정확 결과 | Rejected route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `ShiftGeneratedWeilToeplitzLevinsonReductionAndFiniteLagNoGo` | fixed-lag moment sign recurrence / 고정 lag moment 부호 점화식 | `ExplicitWeilShiftCoreReflectionCoefficientUnitDiskBound` |
| Collatz / 콜라츠 | `FiniteModulusPiecewisePolynomialCollatzRankNoGo` | finite-residue polynomial one-step rank / 유한 residue polynomial 1-step rank | `SymbolicCylinderAdaptiveBlockDescentBeyondPolynomialRanks` |
| Goldbach / 골드바흐 | `PowerSpectrumInsufficiencyForPointwiseBinaryConvolution` | magnitude-only or energy-only K56 envelope / 크기·에너지만 사용한 K56 envelope | `PhaseResolvedBinaryGoldbachScaleEnvelopeSummableK56` |
| Twin Prime / 쌍둥이 소수 | `FrechetMarginalLiouvilleNoGoAndOneSidedWalshReduction` | separate marginal Liouville cancellation / 분리된 주변 Liouville 상쇄 | `CubicRoughOneSidedJointLiouvilleTypeIIMargin` |

The machine audit records four exact theorems, four rejected targets, four
three-node proof DAGs, zero conjecture resolutions, and zero failures.

기계 감사에는 정확한 정리 4개, 폐기된 표적 4개, 세 노드 proof DAG
4개가 기록된다. 난제 해결 수와 실패한 검사는 모두 0이다.

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Work in logarithmic coordinates on an abelian convolution group. Let

```text
tilde(g)(x) = conjugate(g(-x)),
tau_a f(x) = f(x-a),
Q(f,g) = W(f * tilde(g)),
```

where `W` is the linear functional appearing in a Weil explicit-formula
criterion and is assumed to obey

```text
W(tilde(phi)) = conjugate(W(phi)).
```

Fix a real test function `f` and a step `h`. Then

```text
Q(tau_(jh)f, tau_(kh)f) = r_(j-k),
r_m = W(tau_(mh)(f*tilde(f))).
```

Thus the Gram matrix of

```text
f, tau_h f, ..., tau_((n-1)h) f
```

is real symmetric Toeplitz whenever the moments are real.

For nonzero preceding prediction errors, let `kappa_m` be the Levinson
reflection coefficient and `E_m` the next Schur pivot. Then

```text
E_m = E_(m-1)(1-kappa_m^2).                       (1)
```

If `E_0>0`, every nested Toeplitz section is positive definite exactly when

```text
|kappa_m| < 1 for every m>=1.                    (2)
```

한국어로, Weil 형식을 `Q(f,g)=W(f*tilde(g))`로 쓰면 두 test function을
동시에 같은 만큼 이동했을 때 convolution의 이동량이 소거된다. 따라서
하나의 함수를 일정 간격으로 이동시켜 만든 Gram 행렬은 두 index의
차이에만 의존하는 Toeplitz 행렬이다. 이 행렬의 Schur pivot은 Levinson
reflection 계수로 식 (1)처럼 정확히 갱신된다. 그러므로 이 shift core의
모든 절단 양성은 모든 reflection 계수가 열린 단위원 안에 있다는
명제로 환원된다.

### Exact derivation / 정확 유도

Translation and involution satisfy

```text
tilde(tau_b g) = tau_(-b) tilde(g),
(tau_a f) * (tau_b g) = tau_(a+b)(f*g).
```

Therefore

```text
(tau_(jh)f) * tilde(tau_(kh)f)
= tau_((j-k)h)(f*tilde(f)),
```

which proves the Toeplitz identity.

For real moments `r_0,...,r_m`, suppose the order `m-1` prediction polynomial
has coefficients `a_1,...,a_(m-1)` and error `E_(m-1)`. Define

```text
kappa_m
= -(r_m + sum_(j=1)^(m-1) a_j r_(m-j))/E_(m-1).
```

Reverse the old coefficients and update

```text
a_j(new) = a_j(old) + kappa_m a_(m-j)(old),
a_m(new) = kappa_m.
```

Block elimination of the Toeplitz matrix gives (1). The generator verifies
the recurrence against independently computed exact LDL Schur pivots for the
rational moment vector

```text
(2, 1, 3/4, 1/3, 1/5, 1/8, 1/13).
```

All seven exact pivots agree, and at least five reflection coefficients are
nonzero.

### Fixed-lag no-go / 고정 lag 불가능 정리

Fix any `L>=1` and set

```text
r_0=1,
r_1=...=r_L=0,
r_(L+1)=2.
```

Every Toeplitz section visible through lag `L` is the identity. Hence all
visible reflection coefficients are zero and all visible Schur pivots equal
one. The next section is

```text
I + 2(e_0 e_(L+1)^T + e_(L+1)e_0^T).
```

It has eigenvalues

```text
3, -1, 1, ..., 1.
```

Equivalently,

```text
kappa_(L+1)=-2,
E_(L+1)=1*(1-4)=-3.
```

Thus no rule that inspects only a fixed number of lags can certify every
future section in the unrestricted Hermitian Toeplitz moment class unless it
uses additional structural constraints. The machine audit verifies
`L=1,...,12` with exact rational arithmetic; the displayed matrix argument
proves every `L`.

임의의 고정 lag 수만큼은 identity moment와 완전히 같지만 바로 다음
moment에서 음의 고유값이 나타나는 반례족이다. 유한 계산은 12개 사례를
재생할 뿐이며, 증명은 모든 `L`에 적용된다. 다만 이 반례 moment들이
실제 Weil functional에서 나온다고 주장하지 않는다.

### Logical limit and next lemma / 논리적 한계와 다음 보조정리

This result computes the form of actual shift-core entries, but it does not
evaluate the resulting Weil moments at every order. It also does not assert
that the adversarial finite-lag moment family is realizable by the Weil
functional, or that one lattice orbit of one test function is dense in the
full Weil test space. Consequently it is not an RH proof.

다음 단일 보조정리는

```text
ExplicitWeilShiftCoreReflectionCoefficientUnitDiskBound
```

이다. 명시적인 test function과 shift 간격을 고정하고, Weil explicit
formula에서 모든 `r_m`을 도출한 뒤, 양성을 가정하지 않고
`|kappa_m|<1`을 모든 차수에서 증명해야 한다. 전체 test core로 승격하려면
별도의 density 또는 block-core 정리도 필요하다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

Fix `M>=1`. For every odd residue `r mod M`, let `P_r` be a real polynomial
and define

```text
R(n)=P_r(n) when n congruent to r mod M.
```

Assume `R` is bounded below on the positive odd integers. Then it is
impossible that

```text
R(T(n)) < R(n)                                    (3)
```

holds on every accelerated Collatz edge.

이 정리는 TICKET145의 affine rank 배제를 임의의 고정 차수 polynomial로
확장한다. residue마다 서로 다른 polynomial과 서로 다른 차수를 허용한다.

### Proof / 증명

For every `k>=1`, use the same-residue expanding family

```text
n_k=4Mk-1,
3n_k+1=2(6Mk-1),
T(n_k)=6Mk-1,
n_k congruent T(n_k) congruent -1 mod M.          (4)
```

Only `P_(-1)` appears on these edges. Since `R` is bounded below,
`P_(-1)(x)` is either constant or has positive leading coefficient on the
positive ray. If it is constant, then

```text
R(T(n_k))-R(n_k)=0,
```

contradicting strict descent. If it has degree `d>=1` and leading coefficient
`a_d>0`, then

```text
P_(-1)(6Mk-1)-P_(-1)(4Mk-1)
```

is a polynomial in `k` with leading coefficient

```text
a_d M^d (6^d-4^d) > 0.
```

It is therefore positive for every sufficiently large `k`, again
contradicting (3). `QED`

하방 유계 polynomial은 양의 방향에서 음의 leading coefficient를 가질
수 없다. 상수이면 rank가 그대로이고, 양의 leading coefficient이면
입력이 `4Mk` 규모에서 `6Mk` 규모로 커질 때 결국 rank도 증가한다.

### Reproducible computation / 재현 가능한 계산

The generator audits five moduli

```text
1, 2, 5, 16, 31
```

against constant through quintic profiles, including a quadratic with a large
negative linear coefficient that delays the counteredge. For each of the
30 rows it finds the first exact `k` at which the rank ceases to decrease and
checks (4). The symbolic leading-term proof, not the finite search, establishes
the all-polynomial theorem.

생성기는 작은 `k`에서 잠시 감소할 수 있는 polynomial도 포함한다. 이는
제한된 범위의 CEGIS에서 살아남는 후보가 무한 정리가 아님을 보여준다.

### Logical limit and next lemma / 논리적 한계와 다음 보조정리

The theorem does not exclude an oscillatory rank, an unbounded-state rank,
history dependence, or descent after a variable number of Collatz steps.
Moreover, a real-valued lower bound alone is not a well-foundedness proof.

이제 단순한 1-step 크기 함수의 차수를 높이는 경로는 중단한다. 다음
단일 보조정리는

```text
SymbolicCylinderAdaptiveBlockDescentBeyondPolynomialRanks
```

이다. 유한 residue polynomial이 아니라 valuation word와 lift cylinder를
상태로 사용하고, stopping time을 정의에 넣지 않은 독립적인 block
길이에서 엄격한 well-founded 감소를 증명해야 한다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

Let `f` be a real vector on the cyclic group `Z/qZ`. Define

```text
(f*f)(t) = sum_x f(x)f(t-x).
```

For a translation `g(x)=f(x-a)`,

```text
g_hat(k)=exp(-2 pi i k a/q) f_hat(k),
|g_hat(k)|=|f_hat(k)|,                            (5)
(g*g)(t)=(f*f)(t-2a).                             (6)
```

Thus the mean and full Fourier power spectrum do not determine a fixed
pointwise binary convolution.

한국어로, 입력을 이동하면 모든 Fourier 계수의 크기는 그대로이고 위상만
변한다. 그러나 이항 convolution의 endpoint는 이동량의 두 배만큼
옮겨진다. 따라서 power spectrum이나 frequency별 energy만으로는 특정
짝수 `N`에서의 이항 Goldbach형 convolution을 결정할 수 없다.

### Proof / 증명

The DFT translation rule gives (5). Direct substitution gives

```text
(g*g)(t)
= sum_x f(x-a)f(t-x-a)
= (f*f)(t-2a).
```

Equivalently, Fourier inversion for the binary convolution is

```text
(f*f)(N)
= q^(-1) sum_k f_hat(k)^2 exp(2 pi i kN/q).        (7)
```

The term is `f_hat(k)^2`, not `|f_hat(k)|^2`. The square retains twice the
complex phase needed to align the endpoint `N`.

### Exact counterexample / 정확 반례

For every audited prime `q>=11`, take

```text
f=1_{0,1},
a=2,
g=1_{2,3},
N=0.
```

Then

```text
(f*f)(0)=1,
(g*g)(0)=0.
```

The vectors have the same mean and identical cyclic autocorrelation at every
lag. Since the power spectrum is the DFT of the autocorrelation, their Fourier
magnitudes agree exactly at every frequency. The generator checks

```text
q in {11,13,17,19,23,29}
```

using integer arithmetic only.

이 벡터는 von Mangoldt 함수도 실제 Goldbach residual도 아니다. 반박하는
명제는 “동일한 Fourier magnitude 자료가 점별 convolution 또는 부호
상쇄를 결정한다”는 일반 추론이다.

### Logical limit and next lemma / 논리적 한계와 다음 보조정리

Magnitude estimates can still yield valid triangle-inequality upper bounds.
The no-go says that they cannot recover signed endpoint cancellation or
distinguish two endpoint values with the same power data. A tight

```text
|R(N)| <= 56 N/log N
```

budget cannot credit phase cancellation after the phase has been discarded.

다음 단일 보조정리는

```text
PhaseResolvedBinaryGoldbachScaleEnvelopeSummableK56
```

이다. 실제 `Lambda` exponential sum의 major/minor-arc 분해에서
`f_hat(alpha)^2 exp(-2 pi i N alpha)`의 복소 위상을 유지하고, 각 scale의
부호 있는 기여를 모든 충분히 큰 짝수 `N`에서 합산해 `K=56` 예산 안에
넣어야 한다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

On the exact cubic-rough support from TICKET142, let

```text
N_(s,t), s,t in {+1,-1},
```

be the Liouville sign table and let

```text
A00 = sum 1,
A10 = sum lambda(n),
A01 = sum lambda(n+2),
A11 = sum lambda(n)lambda(n+2).
```

Write

```text
u=(A00-A10)/2,
v=(A00-A01)/2.
```

These are the two negative-sign marginals. The exact Frechet bounds are

```text
max(0,u+v-A00) <= N_(-- ) <= min(u,v).             (8)
```

Both endpoints are sharp.

한국어로, 두 위치에서 각각 Liouville 부호가 음수인 개수만 알아서는 두
부호가 동시에 음수인 교집합을 결정할 수 없다. 가능한 최적 범위가 식
(8)이며, 이는 일반 확률 부등식이 아니라 네 category count에 대한 정확한
포함배제 결과다.

### Proof / 증명

The upper bound follows because an intersection cannot exceed either
marginal. Inclusion-exclusion gives

```text
N_(-- ) >= u+v-A00,
```

and nonnegativity gives the other lower bound. Tables that fill the overlap
first or avoid it first attain the endpoints, proving sharpness.

Walsh inversion separately gives

```text
N_(-- )=(A00-A10-A01+A11)/4.                      (9)
```

### Marginal-cancellation no-go / 주변부 상쇄 불가능 정리

Consider the two exact tables

```text
(N++,N+-,N-+,N--)=(0,50,50,0),
(N++,N+-,N-+,N--)=(25,25,25,25).
```

Both have

```text
(A00,A10,A01)=(100,0,0),
```

so each one-variable Liouville sum cancels perfectly. Nevertheless their
twin-class masses are respectively `0` and `25`; their joint coefficients are
`A11=-100` and `A11=0`.

따라서 `A10=o(A00)`과 `A01=o(A00)`을 각각 증명해도 `N-->0`은 나오지
않는다. 독립적인 두 Type II 추정만으로는 joint parity가 빠져 있다.

### One-sided sufficient reduction / 단측 충분조건 환원

Absolute values are stronger than needed. If nonnegative constants satisfy

```text
A10 <= epsilon_1 A00,
A01 <= epsilon_2 A00,
A11 >= -gamma A00,
epsilon_1+epsilon_2+gamma < 1,
```

then (9) gives

```text
N_(-- )
>= (1-epsilon_1-epsilon_2-gamma)A00/4
> 0.                                               (10)
```

Helpful negative marginal signs and a helpful positive joint sign need no
further control. The four finite cubic-rough rows at

```text
X=10^3,10^4,10^5,10^6
```

all happen to satisfy `A10<=0`, `A01<=0`, and `A11>=0`, so (10) certifies at
least `A00/4` twin-class mass on those finite rows. This finite sign pattern
is not an eventual theorem.

### Logical limit and next lemma / 논리적 한계와 다음 보조정리

The two countertables are abstract parity tables, not alternative Liouville
functions on the integers. The finite arithmetic rows do not prove an
all-scale sign theorem. The sieve parity obstruction has merely been isolated
in the joint `A11` direction.

다음 단일 보조정리는

```text
CubicRoughOneSidedJointLiouvilleTypeIIMargin
```

이다. twin count를 입력으로 사용하지 않고, 실제 cubic-rough Vaughan 또는
Type I/II 분해에서 위 세 단측 상수를 구해 그 합이 1보다 작음을 모든
충분히 큰 dyadic block에서 증명해야 한다.

## Proof DAG / 증명 의존성 그래프

Every problem has the same audited state transition:

```text
T146-REJECTED -> T146-CLOSED -> T146-OPEN
insufficient       exact theorem    next unproved lemma
```

The exact paths are:

```text
RH: fixed-lag moment sign recurrence
 -> Toeplitz-Levinson reduction and fixed-lag no-go
 -> all-order Weil reflection coefficient unit-disk bound

CO: finite-residue piecewise-polynomial one-step rank
 -> polynomial rank no-go
 -> symbolic-cylinder adaptive block descent

GB: magnitude-only arithmetic scale envelope
 -> power-spectrum endpoint phase no-go
 -> phase-resolved summable K56 scale envelope

TP: independent marginal Liouville cancellation
 -> sharp Frechet no-go and one-sided Walsh reduction
 -> one-sided joint cubic-rough Type II margin
```

Every final node has status `open_not_proven`.

각 마지막 노드는 `open_not_proven`이며 난제 증명을 뜻하는 노드는 없다.

## Reproduction / 재현

```powershell
python scripts/ticket146_toeplitz_polynomial_phase_frechet.py
python -m unittest tests.test_ticket146_toeplitz_polynomial_phase_frechet
python scripts/verify_open_problem_structure.py
```

Generated machine-readable records:

```text
data/open-problem/ticket146-toeplitz-polynomial-phase-frechet.json
data/open-problem/riemann/rh-ticket-146-toeplitz-levinson.json
data/open-problem/collatz/co-ticket-146-piecewise-polynomial-rank-no-go.json
data/open-problem/goldbach/gb-ticket-146-power-spectrum-phase-no-go.json
data/open-problem/twin-prime/tp-ticket-146-frechet-marginal-no-go.json
```

## Literature boundary / 문헌 경계

- Connes and Consani formulate RH-related Weil positivity and trace-formula
  problems. TICKET146 does not prove their missing global positivity estimate:
  [Weil positivity and Trace formula](https://arxiv.org/abs/2006.13771).
- Levinson-type reflection recurrences are standard Toeplitz algebra.
  TICKET146's contribution inside PrimeProject is the exact shift-core
  reduction and the fixed-lag adversarial family, not a priority claim for
  the recurrence:
  [Generalized Reflection Coefficients and Levinson Algorithm](https://arxiv.org/abs/math/0404119).
- Tao's almost-all Collatz theorem does not supply an all-orbit adaptive block
  descent certificate:
  [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562).
- Helfgott's circle-method treatment makes explicit why Fourier phases,
  major arcs, and Type I/II minor arcs are arithmetic data rather than a
  power-spectrum-only problem:
  [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438).
- The Polymath bounded-gap work records the sieve parity limitation relevant
  to the remaining joint Liouville term:
  [Variants of the Selberg sieve](https://arxiv.org/abs/1407.4897).

이 문헌은 알려진 전역 경계를 설명한다. TICKET146의 정확 환원과 반례족을
리만 가설, 콜라츠, 강한 골드바흐, 쌍둥이 소수 추측의 해결로 해석해서는
안 된다.
