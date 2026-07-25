# TICKET-147: Fiber Completeness, Compensation Cover, Phase Resolution, and Path Cuts

Date: 2026-07-27

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket147-fiber-compensation-phase-graph.json`

## Publication boundary / 논문 제출용 경계

**English.** TICKET-147 proves four exact intermediate statements. It does
not prove or disprove any target conjecture. For RH it proves that finitely
many generators and all their translates on one fixed lattice cannot be
complete in `L2(R)`. For Collatz it proves actual pointwise descent on a
first-run compensation family having exact relative odd-Haar mass `2/3`.
For Goldbach it gives a uniform endpoint-phase quantization error and proves
that fixed phase resolution cannot meet the `K56` scale through the crude
Parseval-energy route. For Twin Prime it converts the joint Liouville term to
a path-cut statistic and constructs an infinite same-support,
same-marginal counterfamily. No literature-priority claim is made.

**한국어.** TICKET-147은 네 난제 자체가 아니라 네 개의 정확한
중간정리를 증명한다. RH에서는 유한 개 generator와 하나의 고정 lattice
위 모든 shift만으로는 `L2(R)` 전체를 완전히 생성할 수 없음을 증명한다.
Collatz에서는 최초 valuation-one run과 보상 valuation으로 정의한 정확한
cylinder 중 상대적 odd-Haar 질량이 `2/3`인 부분에서 모든 양의 정수
`n>1`이 실제로 시작값 아래로 하강함을 증명한다. Goldbach에서는 endpoint
위상 양자화의 균일 오차를 구하고, 고정된 위상 해상도와 Parseval energy
만으로는 `K56` 규모를 맞출 수 없음을 보인다. Twin Prime에서는 joint
Liouville 항을 path cut으로 바꾸고 같은 support와 같은 marginal을
가졌지만 twin cell이 다른 무한 반례족을 만든다. 학계 최초성은 주장하지
않는다.

## Result table / 결과표

| Problem / 문제 | New exact result / 새 정확 결과 | Rejected route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `FiniteGeneratorLatticeShiftFiberIncompleteness` | finite lattice-shift core completeness / 유한 lattice-shift core 완전성 | `InfiniteMultiscaleWeilFiberCompletenessAndMatrixSchurBound` |
| Collatz / 콜라츠 | `FirstRunCompensationTwoThirdsPointwiseDescentCover` | first compensation covers every code / 최초 보상이 모든 code를 덮는다는 주장 | `ResidualThirdIteratedRunCompensationRenewalDescent` |
| Goldbach / 골드바흐 | `EndpointPhaseQuantizationEnergyBoundAndFixedResolutionNoGo` | fixed-resolution Parseval-only K56 / 고정 해상도 Parseval-only K56 | `ArithmeticPhaseSectorImbalanceBoundSummableK56` |
| Twin Prime / 쌍둥이 소수 | `GapTwoPathCutMarginalNoGoAndArithmeticLabelReduction` | support topology plus marginals control A11 / support와 marginal만으로 A11 제어 | `CubicRoughLiouvillePathSwitchDeficitTypeIIBound` |

The machine audit records four exact theorems, four rejected targets, four
three-node proof DAGs, zero conjecture resolutions, and zero failures.

기계 감사에는 정확한 정리 4개, 폐기 표적 4개, 세 노드 proof DAG 4개,
난제 해결 0개, 실패 0개가 기록된다.

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Fix `h>0` and finitely many functions

```text
f_1,...,f_K in L2(R).
```

Let

```text
V = closure span {f_j(x-nh): 1<=j<=K, n in Z}.
```

Then

```text
V != L2(R).                                      (1)
```

Thus even proving every Toeplitz or block-Toeplitz Gram section positive for
finitely many generator orbits on one lattice does not by itself establish
positivity on the full `L2` test space.

고정 간격 `h`에서 유한 개 함수의 모든 정수 shift를 취해도 `L2(R)`
전체에 조밀해질 수 없다. TICKET-146의 한 generator 결과뿐 아니라 유한
block generator로의 단순 확장도 같은 fiber 차원 장벽을 가진다.

### Proof / 증명

Use the unitary Fourier fiberization over

```text
I=[0,2*pi/h):

F(g)(xi) = (g_hat(xi+2*pi*k/h))_(k in Z).
```

This identifies

```text
L2(R) with L2(I; ell2(Z)).
```

Translation by `nh` multiplies every coordinate in the fiber by the same
scalar

```text
exp(-i*n*h*xi),
```

because the alias factor `exp(-2*pi*i*n*k)` is one. Therefore, at almost
every `xi`, all lattice shifts of the `K` generators lie in

```text
span {F(f_1)(xi),...,F(f_K)(xi)},
```

whose dimension is at most `K`. The ambient fiber `ell2(Z)` has infinite
dimension. A measurable fiber range of dimension at most `K` cannot equal
the full infinite-dimensional fiber almost everywhere, proving (1).

Fourier 영역에서 `2*pi/h`만큼 떨어진 frequency들을 하나의 alias fiber로
묶으면 lattice shift는 fiber 전체에 같은 scalar만 곱한다. 따라서
generator가 `K`개이면 각 fiber에서 생성 가능한 방향도 최대 `K`개다.
반면 전체 `L2` fiber는 무한 차원이다.

### Reproducible exact computation / 재현 가능한 정확 계산

For `K=1,...,8`, use `K+1` finite aliases and the Vandermonde generator
fibers

```text
v_j=(1,j,j^2,...,j^K), 1<=j<=K.
```

The coefficient vector of

```text
p(x)=product_(j=1)^K (x-j)
```

is a nonzero exact integer vector orthogonal to every `v_j`. Exact rational
elimination verifies rank `K`, alias dimension `K+1`, and zero residual in
all eight rows.

이 유한 계산은 무한차원 정리의 증명이 아니라 fiber 차원 논증을 exact
integer 모형에서 독립적으로 재생하는 회귀 검사다.

### Rejected route and logical limit / 폐기 경로와 논리적 한계

Discard:

```text
positivity on finitely many fixed-lattice generator orbits
=> positivity on the full L2 test space.
```

The theorem is about `L2(R)`. A Weil criterion may use a more specific test
class and topology, and a non-dense family could conceivably be determining
under additional analytic structure. No actual Weil moment or reflection
coefficient is bounded here.

이 결과를 곧바로 Weil test space의 불완전성으로 확대하면 안 된다.
해당 test class의 topology와 `L2` closure의 관계를 별도로 증명해야 한다.

The next single lemma is

```text
InfiniteMultiscaleWeilFiberCompletenessAndMatrixSchurBound.
```

It must provide an infinite multiscale or non-lattice family, prove
completeness in the actual Weil test topology, and bound the associated
matrix Schur complements without assuming RH positivity.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

For a positive odd integer `n`, let `r>=0` be the number of initial
accelerated valuations equal to one, and let `b>=2` be the next valuation:

```text
a_1=...=a_r=1, a_(r+1)=b.
```

Every positive integer has a finite such `r`. If

```text
b>=r+2,                                         (2)
```

then for every `n>1` realizing the word,

```text
T^(r+1)(n)<n.                                   (3)
```

The union of these exact finite cylinders has relative odd-Haar mass

```text
2/3.                                            (4)
```

이는 확률적 평균 하강이 아니다. 조건 (2)를 만족하는 각 cylinder 안의
모든 양의 정수에 대해 실제 pointwise 하강 (3)을 증명한다.

### Exact formula / 정확 공식

The initial run of ones is equivalent to

```text
n+1=2^(r+1)q, q odd.
```

After the run and its first compensation,

```text
T^(r+1)(n)
 = (3^(r+1)(n+1)-2^(r+1))/2^(r+b)
 = (3^(r+1)q-1)/2^(b-1).                       (5)
```

An infinite run of ones would require `2^(r+1)` to divide the fixed positive
integer `n+1` for every `r`, which is impossible. Hence `b` exists.

### Pointwise descent proof / pointwise 하강 증명

Put `m=r+1`. The largest right side of (5) under (2) occurs at `b=r+2`,
so it is enough to show

```text
(3^m q-1)/2^m < 2^m q-1.
```

This is equivalent to

```text
q(4^m-3^m)>2^m-1.                               (6)
```

For `m>=2`,

```text
4^m-3^m
 = 4^(m-1)+4^(m-2)3+...+3^(m-1)
 >=4^(m-1)>=2^m>2^m-1.
```

For `m=1`, both bare differences equal one, and (6) is strict exactly when
`q>1`; the excluded equality `q=1` is `n=1`. This proves (3).

### Exact two-thirds mass / 정확한 2/3 질량

Under relative Haar measure on odd 2-adic integers, a valuation word of
total valuation `S` has mass `2^-S`. Therefore

```text
mass(1^r,b)=2^(-(r+b)).
```

Summing the pointwise descent cylinders gives

```text
sum_(r>=0) sum_(b>=r+2) 2^(-(r+b))
 = sum_(r>=0) 2^(-(2r+1))
 = 2/3.
```

The generator checks the exact iterate identity through `200,001`, verifies
zero descent failures in every covered row, and constructs exact positive
representatives of the residual words

```text
1^r,2, 1<=r<=12.
```

For these residual words the first compensation does not descend. Each word
defines an infinite positive arithmetic progression, so the complement
cannot be discarded.

### Rejected route and logical limit / 폐기 경로와 논리적 한계

The theorem leaves an exact Haar mass `1/3`. Haar mass is not an all-natural
integer quantifier, and the residual cylinders contain infinitely many
positive integers. Therefore neither “most codes descend” nor “the first
compensation usually works” proves Collatz.

정확히 `2/3`을 덮었다는 사실은 큰 진전이지만 나머지 `1/3`을 0으로
취급할 수 없다. 특히 `b=2` 보상족은 임의로 큰 양의 정수를 포함한다.

The next single lemma is

```text
ResidualThirdIteratedRunCompensationRenewalDescent.
```

It must restart the same exact decomposition after a failed compensation and
prove that every positive integer in the residual third eventually enters a
pointwise descent block, without using the already observed stopping time.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

For a real function `f` on `Z/qZ`, write

```text
c_N=(f*f)(N)
    =q^(-1) sum_k z_k,

z_k=f_hat(k)^2 exp(2*pi*i*k*N/q).
```

Quantize the phase of every endpoint-aligned `z_k` to the nearest one of
`M` equally spaced sectors, preserving its magnitude. Let the resulting
convolution be `c_N^(M)`. Then

```text
|c_N-c_N^(M)|
 <= 22/(7M) sum_x |f(x)|^2.                     (7)
```

This retains the doubled Fourier phase that TICKET-146 proved was missing
from power-spectrum-only data.

### Proof / 증명

Nearest-sector angular error is at most `pi/M`. The chord inequality and
`pi<22/7` give

```text
|z_k-Q_M(z_k)| <= pi|z_k|/M <=22|z_k|/(7M).
```

After summing and applying Parseval,

```text
q^(-1)sum_k |z_k|
 =q^(-1)sum_k |f_hat(k)|^2
 =sum_x |f(x)|^2,
```

which proves (7).

위상을 버리는 대신 필요한 만큼 discretize하면 endpoint convolution의
손실을 전체 Fourier energy로 정확히 제한할 수 있다.

### `K56` scaling consequence / `K56` 규모 결과

For the von Mangoldt function supported on `[1,N]`,

```text
sum_(n<=N) Lambda(n)^2 <= N log(N)^2.
```

Thus the quantization error is at most

```text
22 N log(N)^2/(7M).
```

To make this no larger than

```text
56N/log(N),
```

it suffices to choose

```text
M >= ceil(11 log(N)^3/196).                      (8)
```

For fixed `M`, the ratio between this guarantee and the `K56` budget is

```text
11 log(N)^3/(196M),
```

which diverges. Therefore fixed phase resolution plus this uniform
Parseval-only estimate cannot certify `K56` at every scale.

생성기는 `N=10^3,...,10^12`의 충분 sector 수를 계산하고, 세 cyclic prime
indicator와 `M=8,16,32,64`에서 direct convolution, Fourier inversion,
양자화 오차, rational energy bound를 재현한다.

### Rejected route and logical limit / 폐기 경로와 논리적 한계

The fixed-resolution no-go concerns this separable uniform energy route. It
does not prove that actual `Lambda` phases have worst-case quantization error.
More importantly, approximating `c_N` does not bound the signed imbalance of
the quantized sectors or the other major/minor-arc errors.

고정 `M`의 실제 산술 상쇄 가능성을 반박한 것이 아니다. 정확히 폐기되는
것은 phase sector 사이의 산술 관계를 전혀 쓰지 않는 Parseval-only 인증이다.

The next single lemma is

```text
ArithmeticPhaseSectorImbalanceBoundSummableK56.
```

It must use the arithmetic structure of the squared von Mangoldt exponential
sum to control the adverse signed mass across a growing number of endpoint
phase sectors, uniformly in every sufficiently large even `N`.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

Make a graph whose vertices are the integers appearing in a finite
cubic-rough pair support and whose edges are the admitted pairs `(n,n+2)`.
This graph is a disjoint union of paths. Give vertex `n` the label

```text
sigma(n)=lambda(n) in {+1,-1}.
```

For the edge ledger,

```text
A00=sum_edges 1,
A10=sum_(n,n+2) sigma(n),
A01=sum_(n,n+2) sigma(n+2),
A11=sum_(n,n+2) sigma(n)sigma(n+2).
```

If `Cut` is the number of sign-changing edges, then exactly

```text
A11=A00-2*Cut.                                   (9)
```

The unsigned graph together with `A10` and `A01` does not determine `A11`
or the negative-negative edge count.

### Proof and infinite counterfamily / 증명과 무한 반례족

Every edge contributes `+1` to `A11` when its labels agree and `-1` when
they differ, immediately proving (9).

On the path with `4m` vertices compare:

```text
alternating: + - + - ... + -
single block: + ... + - ... -
              2m plus, 2m minus.
```

Both have

```text
(A00,A10,A01)=(4m-1,1,-1).
```

But

```text
alternating:
  A11=-(4m-1), N--=0;

single block:
  A11=4m-3, N--=2m-1.
```

The generator verifies this family for `m=1,...,16`. It also reads the four
exact cubic-rough rows from TICKET-142 and converts each observed `A11` into
the exact Liouville switch count

```text
Cut=(A00-A11)/2.
```

같은 gap-two path, 같은 두 endpoint marginal, 같은 전체 부호 균형을
유지해도 joint parity와 twin cell은 양 극단으로 달라질 수 있다.

### Rejected route and logical limit / 폐기 경로와 논리적 한계

An alternating labeling achieves `A11=-A00` on any path component. Hence no
uniform

```text
A11>=-gamma*A00, gamma<1,
```

can follow from unsigned support topology alone. The counterlabels are
abstract labels, not alternative values of the Liouville function. They
refute an information implication, not the Twin Prime conjecture.

실제 Liouville label에는 multiplicativity라는 추가 산술 구조가 있다.
따라서 graph topology를 버리는 것이 아니라 topology만으로 충분하다는
주장을 버리고, 실제 label의 switch deficit을 증명해야 한다.

The next single lemma is

```text
CubicRoughLiouvillePathSwitchDeficitTypeIIBound.
```

It must prove, from the arithmetic decomposition of the actual Liouville
labels and without using the twin count, a uniform upper bound on adverse
sign switches strong enough to give the TICKET-146 one-sided joint margin.

## Proof DAG / 증명 의존성 그래프

Every track uses the audited transition

```text
T147-REJECTED -> T147-CLOSED -> T147-OPEN
insufficient       exact theorem    next unproved lemma
```

The exact paths are:

```text
RH:
finite lattice-shift core completeness
 -> finite-generator fiber incompleteness
 -> infinite multiscale completeness plus matrix Schur bound

CO:
first compensation covers every natural code
 -> exact pointwise two-thirds compensation cover
 -> residual-third iterated renewal descent

GB:
fixed-resolution Parseval-only K56
 -> phase quantization bound and fixed-resolution no-go
 -> arithmetic growing-sector imbalance bound

TP:
unsigned path topology plus marginals control joint parity
 -> path-cut counterfamily and arithmetic-label reduction
 -> cubic-rough Liouville switch-deficit Type II bound
```

Every final node has status `open_not_proven`.

각 마지막 노드는 `open_not_proven`이며 완전 증명이나 추측의 반례를
뜻하는 노드는 없다.

## Reproduction / 재현

```powershell
python scripts/ticket147_fiber_compensation_phase_graph.py
python -m unittest tests.test_ticket147_fiber_compensation_phase_graph
python scripts/verify_open_problem_structure.py
```

Generated records:

```text
data/open-problem/ticket147-fiber-compensation-phase-graph.json
data/open-problem/riemann/rh-ticket-147-finite-shift-fiber-no-go.json
data/open-problem/collatz/co-ticket-147-run-compensation-cover.json
data/open-problem/goldbach/gb-ticket-147-phase-quantization.json
data/open-problem/twin-prime/tp-ticket-147-path-cut-no-go.json
```

## Literature boundary / 문헌 경계

- Shift-invariant spaces and their Fourier/fiber descriptions are established
  theory. PrimeProject claims only this exact proof-route integration and its
  finite exact regression model:
  [Invariance of a Shift-Invariant Space](https://arxiv.org/abs/0804.1597).
- Tao's almost-all Collatz theorem uses a first-passage and renewal framework
  at a much deeper level. The `2/3` pointwise cylinder theorem here is not an
  all-orbit consequence of that work:
  [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562).
- Helfgott's work illustrates that Goldbach estimates require the actual
  Fourier exponential sums and major/minor-arc arithmetic, not only generic
  energy:
  [Major arcs for Goldbach's problem](https://arxiv.org/abs/1305.2897).
- Two-point Liouville correlation is a genuine arithmetic problem. The
  logarithmically averaged result does not directly supply the unweighted,
  cubic-rough, one-sided switch bound required here:
  [The logarithmically averaged Chowla and Elliott conjectures for two-point correlations](https://arxiv.org/abs/1509.05422).

이 문헌은 각 도구의 알려진 이론적 배경을 설명한다. TICKET-147의
부분정리와 no-go를 리만 가설, 콜라츠 추측, 강한 골드바흐 추측,
쌍둥이 소수 추측의 해결로 해석해서는 안 된다.
