# TICKET-130: Computability, Cap-Language No-Go, and Route Optimality

## Abstract / 초록

TICKET-130 preserves the useful results of TICKET-129 while correcting one
impossible next target. It proves five exact intermediate results:

1. every rational-bump core value of the fixed Weil functional is a computable
   real, so strict-negative RH witnesses are semidecidable on the explicit core;
2. the Collatz valuation-cap language cannot become empty at any finite depth;
3. that same cap language nevertheless has an explicit exponentially decaying
   odd-cylinder mass;
4. `K=56` is the largest integer available to the fixed-cutoff, uniform-main-
   coefficient Goldbach endpoint architecture;
5. the Twin Prime within-block defect is exactly an endpoint ratio times a
   dimensionless relative-increment imbalance, whose critical threshold is
   `2/23`.

TICKET-130은 TICKET-129의 유효한 결과를 유지하면서 달성 불가능한 다음 목표
하나를 폐기한다. RH에서는 열거 가능한 유리 bump 핵심 원소의 Weil 값이
계산 가능한 실수임을 증명하여 엄격한 음수 반례 탐색을 반결정 절차로 만든다.
Collatz에서는 valuation-cap 언어가 어떤 유한 깊이에서도 소멸할 수 없음을
증명하는 동시에 그 원통 질량이 지수적으로 0에 접근함을 증명한다. Goldbach는
현재 고정 cutoff와 균일 주항 계수 구조에서 `K=56`이 최적 정수임을 보이고,
Twin Prime은 필요한 `0.08` 결함을 무차원 상대 증분 임계값 `2/23`으로
환원한다. 네 난제는 모두 미해결이다.

Machine-readable record:
`data/open-problem/ticket130-computability-cap-language-optimality.json`.

> **TICKET-131 correction / 정정:** two proposed next targets below have been
> narrowed. The Collatz strict cap was proved by TICKET-129 only through
> `2^29` steps, so excluding every infinite strict-cap path is not known to cover
> every hypothetical least counterexample. For Twin Prime, `R(Y)` is exactly the
> positive within-block supremum of `Q_X/Q_Y-1`, so `R<2/23` alone is a
> reparameterization rather than a simpler analytic theorem. The TICKET-130
> intermediate identities and finite-language results remain valid. See
> [TICKET-131](proof-viability-and-target-correction.md).
>
> **한국어:** 아래의 다음 목표 두 개는 TICKET-131에서 교정되었다. Collatz
> strict cap은 `2^29` 단계까지만 최소 반례의 필요조건으로 증명되었으므로
> 모든 무한 strict-cap 경로 배제가 가상 반례 전체를 덮는다는 정리가 없다. Twin
> Prime의 `R<2/23`은 all-scale 비율 제어를 다시 쓴 식이므로 실제 Vaughan
> 계수의 새 부등식 없이 난점을 줄이지 않는다.

## 1. Claim discipline / 주장 규율

| Label | Meaning | 한국어 의미 |
|---|---|---|
| exact theorem | follows from the displayed assumptions | 표시된 전제에서 증명된 정리 |
| computable value | arbitrary rational enclosures exist algorithmically | 임의 정밀도의 유리 구간을 알고리즘으로 계산 가능 |
| semidecision | halts on every strict negative witness, not necessarily otherwise | 엄격한 음수일 때 정지하지만 그 외에는 정지를 보장하지 않음 |
| route no-go | refutes one proposed proof target, not the conjecture | 한 증명 목표만 반박하며 추측의 반례가 아님 |
| route optimality | optimal only inside a named proof architecture | 명시한 증명 구조 내부에서만 최적 |

No density-zero statement is called emptiness. No computable real is assumed to
have a decidable sign. No endpoint constant is confused with a proved
pointwise analytic estimate.

밀도 0을 공집합이라고 부르지 않는다. 계산 가능한 실수라고 해서 부호가 항상
결정 가능하다고 가정하지 않는다. 끝점 상수 개선과 실제 점별 해석 추정을
구분한다.

## 2. Riemann Hypothesis / 리만 가설

Let `C_Q` be the TICKET-129 core of finite Gaussian-rational sums of the
standard bump

```text
b(x)=exp(-1/(1-x^2)) for |x|<1, and b(x)=0 otherwise.
```

For `g in C_Q`, put `h=g*tilde(g)` and fix one published normalization of the
Weil functional `W`. Write `Q_W(g)=W(h)`.

### Theorem RH-130: `ComputableWeilCoreValueAndNegativeWitnessSemidecision`

For every finite core description `g` and every integer `s>=1`, there is an
algorithm that returns rational numbers `L_s<=U_s` such that

```text
Q_W(g) in [L_s,U_s],   U_s-L_s < 2^(-s).
```

Consequently, if the RH-equivalent sign convention is

```text
RH iff Q_W(g)>=0 for every g in C_c^infinity(R),
```

then RH falsity is semidecidable by dovetailing all core descriptions and all
precisions.

### Proof / 증명

A core element is a finite rational tuple. The standard bump is computably
smooth, including its flat boundary extension. Rational translation and scale,
finite linear combinations, reflection, and compact convolution preserve
computable smoothness. Thus `h` and all derivative bounds needed below are
effective.

If the support of `g` is contained in `[L,U]`, then

```text
supp(h) subset [L-U,U-L].
```

Put `A=U-L`. Since `log 3>1`, the exact integer

```text
B=3^ceil(A)
```

satisfies `log B>A`. TICKET-128 therefore makes the arithmetic side of the
explicit Weil formula the finite list `p^m<=B`.

The remaining archimedean expression uses elementary computable constants and
kernels. Near the apparent origin singularity, smooth Taylor expansion of `h`
supplies an outward rational remainder bound. On a compact interval away from
zero, interval quadrature with derivative bounds gives arbitrary precision.
The residual elementary kernel has an explicit exponential envelope, giving a
computable tail bound. Adding these intervals to the finite prime-power terms
produces `[L_s,U_s]`.

If `Q_W(g)<0`, eventually `U_s<0`. TICKET-127 proves that continuity plus a
dense enumerable core transfers every genuine negative witness to a core
witness; TICKET-129 supplies that core in the relevant autocorrelation image.
Dovetailing therefore halts on every strict violation. `QED`

한국어 핵심은 “실제 값이 존재한다”에서 “임의 정밀도로 외향 구간을 만들 수
있다”로 한 단계를 닫았다는 것이다. 다만 값이 정확히 0이면 유한 시간에
부호를 결정하지 못할 수 있으므로 이는 결정 절차가 아니라 반결정 절차다.

```text
Next: UniversalNonnegativeWeilCoreCertificate
다음: 모든 유리 bump 핵심 원소의 Weil 비음성 인증
```

Computability does not imply universal nonnegativity. No negative interval has
been found or certified here, and RH remains open.

## 3. Collatz Conjecture / 콜라츠 추측

For `j>=1`, define

```text
C_j = ceil(j log_2 3) = bit_length(3^j),   C_0=0,
a_j = C_(j+1)-C_j  for j>=0.
```

### Theorem CO-130A: `CapLanguageNonExtinction`

Every `a_j` is `1` or `2`, and

```text
a_0+...+a_(j-1)=C_j
```

for every `j>=1`. Therefore the TICKET-129 prefix-cap language is nonempty at
every finite depth. By TICKET-78, every one of these finite words is realized
by infinitely many positive integers.

### Proof / 증명

The initial value is `a_0=C_1-C_0=2`. For `j>=1`, if `3^j` has binary length
`C_j`, multiplication by three increases that length by at least one and at
most two. Hence every later `a_j` is `1` or `2`. The prefix equality telescopes.
TICKET-78 proves that every positive accelerated valuation word of sum `S`
determines one nonempty residue class modulo `2^(S+1)`, containing infinitely
many positive representatives. `QED`

This formally retires the TICKET-129 target
`LeastCounterexampleValuationCapLanguageExtinction`. The target is impossible,
not merely computationally difficult.

이 결과는 매우 중요한 방향 교정이다. cap을 만족하는 단어가 “아직 계산에서
남아 있다”가 아니라 모든 유한 깊이에서 정확히 구성된다. 따라서 유한 깊이를
늘려 언어가 사라지기를 기다리는 전략은 폐기해야 한다.

### Theorem CO-130B: `CapLanguageExponentialDensityZero`

Under relative odd-cylinder measure,

```text
mass(L_j) <= (65/48) rho^j,
rho^41 = 65^65/(41^41 2^137 3^24) < 1,
rho = 0.9466204159695351...
```

where `L_j` is the set of valuation words satisfying every prefix cap through
depth `j`.

### Proof / 증명

The exact cylinder law is `P(a=k)=2^(-k)` for `k>=1`. For `0<t<1`,

```text
P(S_j<=C_j)
 <= t^(-C_j) E[t^S_j]
 =  t^(-C_j) (t/(2-t))^j.
```

The prefix event `L_j` is contained in the final-cap event. Exact integer
comparison gives

```text
3^41 < 2^65,
C_j <= 65j/41+1.
```

Set `t=48/65`; then `t/(2-t)=24/41`. Collecting powers gives the displayed
`rho^41`, whose numerator is strictly smaller than its denominator. `QED`

At depth 256 this general bound is about `1.0782e-6`; the exact dynamic program
gives the sharper prefix mass `4.7635e-9`. Both are density statements, not
proofs that no natural trajectory survives.

```text
Superseded by TICKET-131:
NoEventuallyStableNaturalPathUnderExactNoDescentEnvelope

TICKET-131로 교체:
정확한 전시간 no-descent envelope 아래에서 안정화된 자연수 경로 배제
```

The surviving nested words define 2-adic paths. TICKET-131 proves that one
infinite word is generated by a fixed positive integer exactly when its
canonical nested residues eventually stabilize. It also corrects the scope:
the strict TICKET-129 cap is not established as an all-time necessary condition. Collatz
remains open.

## 4. Goldbach Conjecture / 골드바흐 추측

For even `N`, use the standard binary singular series

```text
S(N)=2 C2 product_(p|N,p>2) (p-1)/(p-2),
C2=product_(p>2) (1-1/(p-1)^2).
```

### Theorem GB-130: `K56OptimalIntegerForFixedUniformCoefficientGlue`

At the fixed cutoff `H=4*10^18`, `K=56` is the largest integer that can pass
the TICKET-129 endpoint inequality if `S(N)` is replaced by one uniform main
coefficient `A` valid for every even `N>H`.

### Proof / 증명

For powers of two, `S(N)=2C2`. There are arbitrarily large such `N`, so every
uniform coefficient must satisfy `A<=2C2`. Since all omitted Euler factors are
strictly below one,

```text
2C2 < 2 product_(3<=p<=47) (1-1/(p-1)^2)
     = 3041106216468949733/2294196982052290560
     < 57/43.
```

The last strict gap is exactly

```text
1660668815723401/98650470228248494080 > 0.
```

TICKET-129 proves `log H<43`; hence

```text
57/log H > 57/43 > A.
```

Thus the `K=57` endpoint is negative even before proper-prime-power
contamination. TICKET-129 separately proves that `K=56` has exact positive
margin

```text
23019645297/2140000000000.
```

Therefore `56` is optimal inside this named architecture. `QED`

이 정리는 `|R(N)|<=56N/log N`을 증명하지 않는다. 다만 같은 cutoff, 같은
균일 주항 계수, 같은 끝점 부등식 안에서 상수를 더 다듬어 `57`로 올리는 작업은
불가능함을 증명한다. cutoff를 더 높이거나 `N`별 특이급수 구조를 사용하면
`K=57`이 다른 구조에서 충분할 가능성은 배제하지 않는다.

```text
Next: PointwiseBinaryGoldbachResidualK56
다음: 점별 이항 Goldbach 잔차 K=56 정리
```

The project should now spend effort on signed pointwise cancellation, not on
further polishing of this fixed endpoint constant. Strong Goldbach remains
open.

## 5. Twin Prime Conjecture / 쌍둥이 소수 추측

Fix a block left endpoint `Y`. Let

```text
q=Q_Y=A_Y/K_Y>0,
a=(A_X-A_Y)/A_Y,
k=(K_X-K_Y)/K_Y.
```

### Theorem TP-130: `DimensionlessRelativeIncrementReduction`

For every `X` in the block,

```text
Q_X-q = q (a-k)/(1+k).
```

Define

```text
R(Y)=sup_(Y<=X<=2Y) max(0,a-k)/(1+k).
```

Then the TICKET-129 additive defect satisfies the exact identity

```text
D(Y)=Q_Y R(Y).
```

If

```text
limsup_j Q_(2^j) <= 23/25
and
limsup_j R(2^j) < 2/23,
```

then the all-scale limsup of `Q_X` is strictly below one.

### Proof / 증명

Substitute `A_X=A_Y(1+a)` and `K_X=K_Y(1+k)`. Taking positive parts and the
block supremum gives `D(Y)=Q_YR(Y)`. Also

```text
Q_X <= Q_Y(1+R(Y)).
```

The exact threshold identity is

```text
(23/25)(1+2/23)=1,
(23/25)(2/23)=2/25=0.08.
```

Strict limsup control below `2/23` therefore gives the required strict
all-scale bound. Equality shows that `2/23` is sharp for this product envelope.
`QED`

TICKET-129's midpoint countermodel has `a=1`, `k=0`, hence `R=1` and
`Q_X=46/25=1.84`. The new target is dimensionless and separates excess adverse
growth from denominator compensation.

```text
Refined by TICKET-131:
UniformSignedVaughanBlockTransportWithParityBridge

TICKET-131에서 정밀화:
실제 Vaughan 부호 수송의 균일 상계와 parity bridge
```

No such estimate is proved for the actual coefficients. TICKET-131 observes
that the relative imbalance is exactly `Q_X/Q_Y-1`; the threshold is useful
bookkeeping but not an independent complexity reduction. Parity and exact
gap-two positivity remain separate open barriers, so Twin Prime remains open.

## 6. Keep, discard, and next / 유지·폐기·다음 단계

| Problem | Keep / 유지 | Discard / 폐기 | Decisive next theorem / 다음 정리 |
|---|---|---|---|
| RH | certified strict-negative interval enumeration | finite non-discovery or finite Gram positivity as universal positivity | `WeilSpecificCoerciveTailOrMonotoneOperatorLimit` |
| Collatz | finite-horizon cap plus exact nested residues | finite cap-language extinction and all-time strict-cap promotion | `NoEventuallyStableNaturalPathUnderExactNoDescentEnvelope` |
| Goldbach | signed residual split by singular-series arithmetic type | more uniform constant polishing at fixed `H` | `PointwiseBinaryGoldbachResidualByRoughnessStratum` |
| Twin Prime | raw signed Vaughan block numerator | detached endpoint interpolation or ratio reparameterization alone | `UniformSignedVaughanBlockTransportWithParityBridge` |

## 7. Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket130_computability_cap_language_optimality.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket130_computability_cap_language_optimality
```

Generated artifacts:

- `data/open-problem/ticket130-computability-cap-language-optimality.json`
- `data/open-problem/riemann/rh-ticket-130-computable-weil-core.json`
- `data/open-problem/collatz/co-ticket-130-cap-language-density.json`
- `data/open-problem/goldbach/gb-ticket-130-k56-route-optimality.json`
- `data/open-problem/twin-prime/tp-ticket-130-relative-increment.json`

## 8. Literature boundary / 문헌 경계

- M. Suzuki, [Weil's quadratic form via the screw function](https://arxiv.org/abs/2606.09096), for the 2026 Weil-functional formulation. TICKET-130 proves effective core-value computability, not Weil positivity.
- T. Niu, [Parity vectors and paradoxical sequences in the accelerated Collatz map](https://arxiv.org/abs/2605.13886), for the sharp finitary parity-density boundary. TICKET-130's valuation-cap theorem does not imply Collatz.
- J. B. Friedlander, D. A. Goldston, H. Iwaniec, and A. I. Suriajaya, [Exceptional zeros and the Goldbach problem](https://doi.org/10.1016/j.jnt.2021.06.004), for weighted binary Goldbach and singular-series context.
- K. Ford and J. Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368), for the Type I/II sieve boundary. The relative-increment reduction supplies no parity theorem.

The cited papers define accepted formulations and boundaries. The TICKET-130
algebraic claims are proved above and replayed by repository tests; citations do
not replace the missing conjecture-level steps.
