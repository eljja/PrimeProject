# TICKET-165: Vanishing defects, logarithmic Collatz tails, Goldbach variation, and signed Haar duality

한국어 제목: **소멸 결함, 콜라츠 로그 꼬리, 골드바흐 변동, 부호 있는 Haar 쌍대성**

Status / 상태: `open_not_proven` for all four conjectures / 네 추측 모두 미해결

Generated / 생성: 2026-08-01 (Asia/Seoul)

## Abstract / 초록

TICKET-165 continues the four open nodes left by TICKET-164. It proves four
exact bridge or no-go statements. None is a proof or disproof of its parent
conjecture.

On the Riemann track, a vanishing-negative-defect limit theorem replaces the
unnecessarily strong demand for a cutoff-independent positive eigenvalue gap.
An exact path-Laplacian family is positive on every finite constraint core but
has minimum Rayleigh quotients tending to zero. On the Collatz track, the
infinite final-valuation tail at every first multiplicative crossing is reduced
uniformly to `O(log m)` excess values. A near-critical exact family proves that
no fixed excess cutoff can close all lengths through the same coarse envelope.
On the Goldbach track, a sparse-anchor plus variation theorem promotes sampled
deficit margins to a pointwise margin, while a unit-spike family proves that no
fixed finite normalized moment can exclude one exception. On the Twin Prime
track, weighted product-Haar duality gives a sign-uniform sufficient
certificate when the signed error budget lies below the main term; `H` and
`-H` prove that unsigned square energies alone cannot decide positivity.

TICKET-165는 TICKET-164가 남긴 네 open node를 이어서 네 개의 정확한
bridge 또는 no-go 명제를 증명한다. 어떤 결과도 상위 추측의 증명이나
반증이 아니다.

리만 트랙에서는 cutoff와 무관한 양의 고윳값 간극 대신 음의 결함이
0으로 가는 극한 정리를 사용한다. 정확한 path-Laplacian 족은 모든 유한
제약 core에서 양수지만 최소 Rayleigh quotient는 0으로 간다. 콜라츠
트랙에서는 첫 곱셈 수축 시점의 무한 마지막-valuation 꼬리를 모든
길이에서 `O(log m)`개의 excess 값으로 줄인다. 또한 하나의 고정 excess로
모든 길이를 닫을 수 없음을 near-critical 정확 족으로 보인다. 골드바흐
트랙에서는 sparse anchor와 국소 변동을 결합해 표본 margin을 점별
margin으로 승격하고, 단일 unit spike로 모든 고정 유한 moment 경로를
반박한다. 쌍둥이 소수 트랙에서는 부호 있는 product-Haar 쌍대 오차가
main term보다 작으면 부호와 무관한 충분조건이 됨을 분리하고, `H`와
`-H`가 같은 unsigned 에너지를 가지면서 서로 다른 positivity 결론을
낼 수 있음을 증명한다.

## Result ledger / 결과 원장

| Problem / 문제 | Exact result / 정확한 결과 | Resolution / 해결 | Decisive next lemma / 다음 보조정리 |
|---|---|---|---|
| Riemann / 리만 | `VanishingDefectCoreLimitBridgeAndUniformGapNoGo` | open / 미해결 | `ExplicitGuinandWeilCoreApproximationWithVanishingNegativeDefect` |
| Collatz / 콜라츠 | `UniformLogarithmicFinalExcessReductionAndConstantExcessNoGo` | open / 미해결 | `UniformResidueSlackForLogarithmicFirstCrossingExcessWindow` |
| Goldbach / 골드바흐 | `SparseAnchorVariationPointwiseBridgeAndFiniteMomentSpikeNoGo` | open / 미해결 | `UniformDyadicMinorDeficitAnchorMarginAndVariationDecay` |
| Twin Prime / 쌍둥이 소수 | `SignedProductHaarDualityAndUnsignedEnergyNoGo` | open / 미해결 | `PrimeWeightedSignedProductCarlesonDualMarginBeyondParity` |

## 1. Riemann hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `D` be a dense admissible core, let `P_N(D) subset D`, and suppose
`P_N f -> f` in a norm for which the quadratic form `Q` is continuous. If

```text
Q(P_N f) >= -epsilon_N ||P_N f||^2,    epsilon_N -> 0,
```

for every `f in D`, then `Q(f)>=0` on `D`.

조밀한 허용 core `D`와 `D`를 보존하는 투영 `P_N`을 잡자. `Q`가
연속인 norm에서 `P_N f -> f`이고 위 음의 결함 상계가 성립하면
`Q(f)>=0`이다. 따라서 cutoff-free 비음성을 얻는 데 필요한 것은 반드시
양의 균일 spectral gap이 아니라, form 수렴과 0으로 가는 음의 결함이다.

### Proof / 증명

Norm convergence makes `||P_N f||` bounded. Continuity gives
`Q(P_N f)->Q(f)`, while the lower bound tends to zero. Taking the lower limit
proves `Q(f)>=0`.

`P_N f`의 norm은 유계이고 `Q(P_N f)`는 `Q(f)`로 수렴한다. 우변
`-epsilon_N||P_Nf||^2`는 0으로 가므로 하극한을 취하면 결론이 나온다.

### Uniform-gap no-go / 균일 간극 no-go

For the `n`-point path Laplacian,

```text
Q_n(x) = sum_(i=0)^(n-2) (x_(i+1)-x_i)^2,
sum_i x_i = 0,
```

every finite constrained form is strictly positive. Its only zero vectors are
constant, and the sum-zero constraint removes them. However the exact integer
witness

```text
x_i = 2i-(n-1)
```

has

```text
||x||^2 = n(n^2-1)/3,
Q_n(x) = 4(n-1),
Q_n(x)/||x||^2 = 12/[n(n+1)] -> 0.
```

따라서 모든 유한 core가 엄밀히 양수라는 사실은 cutoff-independent 양의
최소 고윳값을 주지 않는다. 감사 행렬의 차원 `4,8,...,128`에서 위
유리수 공식을 정확히 확인했으며 마지막 상계는 `1/1376`이다.

### Limit / 한계

The path Laplacian is not the Guinand-Weil operator. TICKET-165 does not
construct the actual projections, prove form-core convergence, or derive an
explicit `epsilon_N`. The next obligation is
`ExplicitGuinandWeilCoreApproximationWithVanishingNegativeDefect`.

Path Laplacian은 Guinand-Weil 연산자가 아니다. 실제 투영과 form-core
수렴, 명시적인 `epsilon_N`을 얻지 못했으므로 RH 또는 영점 배제 결론은
없다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

For a first-crossing accelerated valuation word of length `m`, let `a_*` be
the least final valuation that makes the full multiplicative coefficient
contract, and write the actual final valuation as `a_*+t`. If

```text
9(2^t-1) > m,
```

then every natural odd realizer `n>=3` descends at that endpoint. Hence only
`O(log m)` final excess values remain at every length.

길이 `m`의 first-crossing word에서 최소 수축 마지막 valuation을 `a_*`,
추가 excess를 `t`라 하자. 위 부등식이 성립하면 모든 홀수 자연수
실현값 `n>=3`이 endpoint에서 하강한다. 따라서 길이가 아무리 커도
검사할 마지막 excess 값은 로그 개수만 남는다.

### Proof / 증명

For every proper prefix, `2^(S_j)<=3^j`. Therefore the affine correction

```text
C = sum_(j=0)^(m-1) 3^(m-1-j) 2^(S_j)
```

satisfies `C<=m*3^(m-1)`. If `D=2^S-3^m`, increasing the least crossing
valuation by `t` gives

```text
D > (2^t-1)3^m.
```

Thus `3D>C` whenever `9(2^t-1)>m`, and the exact endpoint numerator
`nD-C` is positive for every `n>=3`.

각 correction 항은 `3^(m-1)` 이하이므로 `C<=m3^(m-1)`이다. 반면
slope gap은 위와 같이 증가한다. 따라서 제시된 조건 아래에서는 실제
residue를 열거하지 않아도 모든 `n>=3`을 한꺼번에 닫는다.

The exact residual excess counts on the audited schedule are:

```text
m                 8  16  32  64  128  256  512  1024
residual count    1   2   3   4    4    5    6     7
```

### Constant-excess no-go / 고정 excess no-go

Set every proper prefix sum to `floor(j log_2 3)` and let the full sum be
`ceil(m log_2 3)+t`. This is an exact first-crossing word. Each correction
term is greater than `3^(m-1)/2`, whereas

```text
D < (2^(t+1)-1)3^m.
```

For `m>18(2^(t+1)-1)`, the coarse automatic criterion has `3D-C<0`.
TICKET-165 constructs this exactly for `t=0,...,5` at lengths
`19,55,127,271,559,1135`.

이는 실제 실현값이 하강하지 않는다는 반례가 아니다. 하나의 고정
excess와 보편 correction envelope만으로 모든 길이를 닫는 증명 전략의
no-go다. 남은 `O(log m)` 창의 정확 residue 구조는 여전히 미해결이다.

### Limit / 한계

This does not prove Terras's coefficient-stopping-time conjecture and does not
prove that every orbit reaches a multiplicatively contracting prefix. The next
obligation is `UniformResidueSlackForLogarithmicFirstCrossingExcessWindow`.

Terras의 coefficient-stopping-time 추측도, 모든 궤도가 수축 prefix에
도달한다는 명제도 증명하지 않았다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

Let `d_i` be nonnegative normalized deficits on a finite interval and choose
anchors that partition it. For a point between two anchors, measure the
smaller accumulated absolute first-difference variation to either anchor. If
`rho` is the largest such value, then

```text
max_i d_i <= max_(anchor a) d_a + rho.
```

Therefore `anchor_max+rho<1` is a rigorous pointwise no-exception
certificate.

유한 deficit 열에서 anchor 사이 각 점을 좌·우 anchor 중 총변동 거리가
더 작은 쪽으로 연결하자. 최대 anchor 값과 최대 변동 반경의 합이 1보다
작으면 모든 점별 deficit이 1보다 작다.

### Proof / 증명

Telescope from the chosen anchor and apply the triangle inequality. The
maximum over all points gives the displayed bound.

선택한 anchor에서 해당 점까지 차분을 망원합하고 삼각부등식을 적용하면
된다. 이 정리는 평균을 점별로 바꾸지 않는다. 점별 승격에 필요한
추가 정보가 바로 국소 변동임을 명시한다.

### Finite diagnostic / 유한 진단

The existing fixed Farey DFT on the shell `(32768,65536]` has maximum deficit
approximately `0.215888`. The floating-point sparse-net diagnostic passes for
anchor strides `1,2,4,8,16`; at stride `16` its computed upper envelope is
approximately `0.915038`. It fails at stride `32` with envelope approximately
`1.552377`. These decimal values are not interval-arithmetic certificates.

기존 Farey DFT의 마지막 dyadic shell에서 실제 최대 deficit은 약
`0.215888`이다. 새 variation 인증은 even-target anchor stride 16까지
`<1`을 보장하지만 32부터는 보장하지 못한다. 이는 유한 FFT 진단이며
무한 Goldbach 정리가 아니다.

### Finite-moment spike no-go / 유한 moment spike no-go

Put one deficit equal to one and every other deficit equal to zero in a block
of length `L`. For every fixed finite `p`,

```text
(L^(-1) sum d_i^p)^(1/p) = L^(-1/p) -> 0,
max d_i = 1,
exception count = 1.
```

따라서 정규화된 어떤 고정 유한 `Lp` 평균도 단일 Goldbach 예외를
배제하지 못한다. 이 반례는 TICKET-164의 “shell L2는 필요조건이 아니다”를
보완해, 작아지는 평균 자체도 점별 충분조건이 아님을 확정한다.

### Limit / 한계

No uniform anchor margin or variation decay is proved for the true binary
minor arcs. The next obligation is
`UniformDyadicMinorDeficitAnchorMarginAndVariationDecay`.

실제 binary minor arc에 대한 균일 anchor margin과 variation 감소를
증명하지 못했으므로 강한 골드바흐 추측은 그대로 미해결이다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

Expand a centered error `H` and target weight `W` in the complete
product-Haar basis. For positive weights `alpha_R`, weighted Cauchy-Schwarz
gives

```text
|<H,W>|
 <= (sum_R alpha_R |c_R|^2)^(1/2)
    (sum_R |w_R|^2/alpha_R)^(1/2).
```

If the twin-pair count is `M+<H,W>`, this bound gives a sign-uniform sufficient
certificate of strict positivity when the dual budget is strictly below the
positive main term `M`. It is not a necessary condition for a favorable signed
error.

중심화 오차와 표적 weight를 완전한 product-Haar 기저에서 전개하면 위
가중 Cauchy-Schwarz 쌍대 상계를 얻는다. 따라서 양의 main term을 실제
양의 쌍둥이 소수 count로 승격하려면 부호 있는 오차의 쌍대 예산이
main term보다 엄밀히 작으면 부호와 무관한 충분조건을 얻는다. 이는
유리한 부호의 오차까지 포함한 일반적 필요조건은 아니다.

### Unsigned-energy no-go / 무부호 에너지 no-go

Let `H=u tensor v` be the anisotropic witness from TICKET-164 and normalize
`W=H/||H||_F^2`. Then

```text
<H,W> = 1,       <-H,W> = -1.
```

The matrices `H` and `-H` have identical squared product-Haar coefficients,
identical Frobenius energy, and identical unsigned Carleson square profiles.
With `M=1`, however, the two model counts are exactly `2` and `0`. The audit
checks dimensions `8,16,32,64,128`; the Cauchy budget is exactly one in every
case.

`H`와 `-H`는 모든 무부호 Haar 에너지가 같지만 signed pairing은 반대다.
따라서 unsigned 에너지만으로 positivity를 결론 내리는 경로를 정확히
폐기한다. 이는 prime-weighted estimate의 반례가 아니라, 부호와 main-term
비교를 제거한 결정 규칙의 반례다.

### Limit / 한계

The witnesses are deterministic centered matrices. No prime-weighted signed
dual estimate and no parity-breaking input is proved. The next obligation is
`PrimeWeightedSignedProductCarlesonDualMarginBeyondParity`.

실제 소수 가중치에서 signed dual 오차를 main term 아래로 내리지 못했고
parity barrier도 넘지 못했으므로 쌍둥이 소수 추측은 미해결이다.

## Proof DAG / 증명 의존성

Each artifact stores exactly three nodes:

```text
REJECTED: false or insufficient shortcut
   -> CLOSED: exact TICKET-165 theorem
   -> OPEN: one decisive next lemma
```

각 문제별 JSON은 폐기 경로, 이번에 정확히 닫힌 정리, 다음 단일 미증명
보조정리를 분리한다. 네 `OPEN` node 중 닫힌 것은 없고 conjecture
resolution count는 `0`이다.

## Relation to primary literature / 1차 문헌과의 관계

- Akiva Groskin, [A finite Guinand-Weil dictionary and archimedean tail order
  for the truncated Weil quadratic form](https://arxiv.org/abs/2607.02828),
  supplies the finite Guinand-Weil/Galerkin setting and an explicit
  archimedean-tail budget. TICKET-165 does not reproduce that theorem; it
  isolates the different limit obligation that remains after finite forms
  are assembled.
- Lynn E. Garner, [On the Collatz `3n+1`
  algorithm](https://www.ams.org/journals/proc/1981-082-01/S0002-9939-1981-0603593-2/S0002-9939-1981-0603593-2.pdf),
  records the stopping-time formulation used to separate first descent from
  total convergence. TICKET-165's logarithmic excess reduction is an internal
  deduction for the accelerated first-crossing affine model.
- Lasse Grimmelt and Gautami Bhowmik, [The exceptional set of the Goldbach
  problem](https://arxiv.org/abs/2607.27282), surveys exceptional-set bounds
  and gives an explicit major-arc formula. TICKET-165 instead proves a finite
  deterministic anchor-variation implication and does not import an
  exceptional-set estimate as a pointwise theorem.
- Kevin Ford and James Maynard, [On the theory of prime producing
  sieves](https://arxiv.org/abs/2407.14368), shows the central role of Type I
  and Type II information in prime lower bounds. TICKET-165's signed-Haar
  dual target is a proposed proof obligation; it is not a consequence of
  their sieve theorem and does not cross the parity barrier.

한국어 경계: 위 문헌은 문제의 정식 배경과 현재 가능한 도구를 제공한다.
TICKET-165의 네 정리는 저장소 코드와 본문에 제시된 자체 유한·추상
논증이며, 외부 논문의 결과를 네 추측의 해결로 승격하지 않는다.

## Reproduction / 재현

```powershell
python scripts/ticket165_vanishing_defect_logtail_variation_signed_dual.py
python -m unittest tests.test_ticket165_vanishing_defect_logtail_variation_signed_dual
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Machine-readable artifacts / 기계 판독 산출물:

```text
data/open-problem/ticket165-vanishing-defect-logtail-variation-signed-dual.json
data/open-problem/riemann/rh-ticket-165-vanishing-defect.json
data/open-problem/collatz/co-ticket-165-logarithmic-excess.json
data/open-problem/goldbach/gb-ticket-165-anchor-variation.json
data/open-problem/twin-prime/tp-ticket-165-signed-dual.json
```

## Literature boundary / 문헌 경계

- The finite Guinand-Weil setting and its very small finite spectral scales
  are described in [A finite Guinand-Weil dictionary and archimedean tail
  order](https://arxiv.org/abs/2607.02828). TICKET-165 does not import a
  positivity proof from it.
- The Collatz open node is related to the coefficient stopping time introduced
  in classical stopping-time work and discussed in Lynn E. Garner,
  [On the Collatz 3n+1 algorithm](https://www.ams.org/journals/proc/1981-082-01/S0002-9939-1981-0603593-2/).
  The logarithmic excess reduction does not settle that conjecture.
- Current binary Goldbach exceptional-set context is represented by
  [The exceptional set of the Goldbach problem](https://arxiv.org/abs/2607.27282).
  Exceptional-set bounds do not supply the pointwise anchor and variation
  margins required here.
- The Type I/II and parity context for prime-producing sieves is represented
  by Ford and Maynard,
  [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).
  Product-Haar duality alone is not a parity-breaking estimate.

These sources set the external context only. The exact bridge theorems,
countermodels, and finite diagnostics claimed here are generated inside
PrimeProject. No citation is treated as a proof of any of the four
conjectures.

위 문헌은 외부 연구 맥락만 제공한다. 본 문서의 정확한 bridge 정리,
반례 모델, 유한 진단은 PrimeProject 내부에서 생성된다. 어떤 인용도 네
추측의 증명으로 취급하지 않는다.
