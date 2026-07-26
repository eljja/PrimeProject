# TICKET-159: Diagonal Selection, Affine Thresholds, Fourier Phase, and Parity

## Abstract

TICKET-159 continues PrimeProject's simultaneous attack on the Riemann
Hypothesis, the Collatz conjecture, the strong Goldbach conjecture, and the
Twin Prime conjecture. It proves four exact intermediate results and resolves
none of the conjectures.

The Riemann track proves that a preassigned uniform cutoff rate is not logically
necessary: effective per-core error majorants can be searched diagonally. It
also proves that pointwise convergence alone supplies no preassigned schedule.
The Collatz track proves the exact affine threshold for every contracting
valuation cylinder and shows that positive average contraction does not
uniformly bound that threshold. The Goldbach track proves an exact minor-arc
energy coefficient bound but constructs equal-energy spectra with opposite
coefficient signs. The Twin Prime track proves that all low-prime divisibility
information is identically zero inside a rough survivor fiber, even though
that fiber contains both twin-prime pairs and double-composite pairs.

Every proof DAG ends at `open_not_proven`. The machine audit records four exact
results, four rejected routes, zero conjecture resolutions, and zero failed
checks.

## 초록

TICKET-159는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 동시에 공격한다. 이번 회차는 네 개의 정확한 중간 결과를
증명하지만 어떤 추측도 해결하지 않는다.

리만 트랙에서는 미리 정한 하나의 균일 cutoff 속도가 논리적으로
필수적이지 않음을 보인다. 각 유한 core의 계산 가능한 오차 상계가
있다면 cutoff를 대각선 방식으로 따로 찾을 수 있다. 반대로 단순한
점별 수렴만으로는 미리 정한 cutoff 스케줄을 얻을 수 없음을 정확한
반례군으로 증명한다. 콜라츠 트랙에서는 수축 valuation cylinder의
정확한 affine 임계값을 유도하고, 평균 수축량이 양수라는 사실만으로
그 임계값을 균일하게 제한할 수 없음을 증명한다. 골드바흐 트랙에서는
minor arc 계수에 대한 정확한 에너지 상계를 증명하지만, 같은
에너지를 가지면서 계수 부호가 반대인 스펙트럼을 구성한다. 쌍둥이
소수 트랙에서는 rough survivor fiber 안에서 작은 소수의 나눗셈
정보가 모두 0이지만, 그 fiber 안에 쌍둥이 소수와 두 수가 모두
합성수인 쌍이 동시에 존재함을 확인한다.

모든 proof DAG의 마지막 상태는 `open_not_proven`이다. 기계 감사는
정확 결과 4개, 폐기 경로 4개, 난제 해결 0개, 실패 0개를 기록한다.

---

## 1. Reproduction / 재현

Canonical artifact:

`data/open-problem/ticket159-diagonal-threshold-phase-parity.json`

```powershell
python scripts/ticket159_diagonal_threshold_phase_parity.py
python -m unittest tests.test_ticket159_diagonal_threshold_phase_parity
```

The generator writes one global artifact and one artifact for each conjecture.
All rational identities are stored as exact numerator/denominator strings.
Floating-point FFT calculations have explicit reconstruction tolerances and
are not promoted to infinite statements.

생성기는 종합 JSON 하나와 문제별 JSON 네 개를 만든다. 유리수 항등식은
분자와 분모를 정확한 문자열로 저장한다. 부동소수점 FFT 계산에는
명시적인 역변환 재구성 오차 기준을 적용하며, 그 결과를 무한 정리로 승격하지
않는다.

---

## 2. Riemann Hypothesis

### 2.1 Declared proposition

Let `V_N` be a nested form core and let `mu_N>0` be a certified rational
margin. Suppose `A_N(c)` and `B_N(T)` are computable, rational, monotone
majorants that tend to zero for each fixed `N`.

A doubling search finds finite `c_N,T_N` such that

```text
A_N(c_N) <= mu_N/4,
B_N(T_N) <= mu_N/4.
```

If the finite form minimum obeys

```text
lambda(c_N,N,T_N) >= mu_N + A_N(c_N),
```

then the positive-tail composition from TICKET-158 gives

```text
q(f) >= mu_N ||f||^2  on V_N.
```

A uniform-in-`N` convergence rate is not required for this diagonal
selection.

Conversely, pointwise convergence alone supplies no preassigned schedule. For
any proposed `g(N)`, define

```text
A_g(c,N) = 1  if c <= g(N),
           0  if c > g(N).
```

For every fixed `N`, this tends to zero, but it fails exactly at
`c=g(N)`.

### 2.2 Proof

Because the rational majorants are monotone and converge to zero, repeatedly
doubling the cutoff must eventually cross each positive rational target.
Substitution into the TICKET-158 lower bound

```text
q >= q(c,N,T) - A_N(c)
```

proves the core margin. The positive archimedean tail is not subtracted in
this direction.

For the no-go construction, fixing `N` makes `A_g(c,N)` zero after one finite
threshold, so pointwise convergence holds. At the proposed cutoff itself its
value is exactly one. Thus the quantifiers do not imply a previously chosen
polynomial, exponential, factorial, or other schedule.

### 2.3 Finite audit

The machine audit applies the selector to five nested dimensions:

```text
N in {1,2,4,8,16}.
```

It also instantiates the adversarial construction against four illustrative
schedules: linear, quadratic, single exponential, and factorial. These rows
verify the logic; they do not model the unknown actual Weil error.

### 2.4 한국어 해석과 한계

이번 결과는 “모든 `N`에 동시에 적용되는 예쁜 수렴 속도”를 먼저
찾아야 한다는 요구를 제거한다. 각 `N`에서 검증 가능한 오차 상계와
양의 최소 고유값 여유가 있으면 그때그때 충분한 cutoff를 찾으면 된다.

그러나 실제 Weil form에 필요한 `A_N(c)`와 양의 Galerkin margin은 아직
증명하지 못했다. 예제에서 cutoff를 찾았다는 사실은 실제 리만 가설의
오차 상계를 계산했다는 뜻이 아니다.

### 2.5 Rejected route

Discard:

```text
PointwiseCutoffConvergenceSuppliesAPreassignedJointRate
```

Next lemma:

```text
CertifiedPrimeBandMajorantAndPositiveGalerkinMarginOnEveryNestedWeilCore
```

---

## 3. Collatz conjecture

### 3.1 Declared proposition

For a valuation prefix `w=(a_1,...,a_m)`, put

```text
S = a_1+...+a_m,
C(w) = the exact affine constant,
D = 2^S - 3^m.
```

Every odd start `n` realizing this prefix satisfies

```text
T_w(n) = (3^m n + C(w))/2^S.
```

Therefore:

```text
T_w(n) < n  iff  D n > C(w).
```

If `D<=0`, that prefix cannot descend. If `D>0`, its exact affine threshold is

```text
theta(w) = C(w)/D.
```

All realizing starts above this threshold descend.

Positive average logarithmic contraction does not uniformly bound
`theta(w)`. Let

```text
S_m = ceil(m log_2 3),
D_m = 2^S_m - 3^m.
```

Every positive word of length `m` and total `S_m` satisfies

```text
theta(w) >= 3^(m-1)/D_m,
```

and the right-hand side is unbounded along a subsequence.

### 3.2 Proof

The affine recurrence gives the threshold identity directly. The first term
of `C(w)` is `3^(m-1)`, which proves the lower bound.

The number `log_2 3` is irrational: otherwise unique factorization would give
an equality between a power of two and a positive power of three. Irrational
rotations are dense modulo one, so `{m log_2 3}` approaches one from below
along a subsequence. Hence

```text
D_m/3^m
  = 2^(ceil(m log_2 3)-m log_2 3) - 1
  -> 0
```

along that subsequence. The threshold lower bound is therefore unbounded.

### 3.3 Finite audit

An exact-integer scan through word length `768` found 11 record lower bounds.
The last five records occur at:

| `m` | `S_m` | threshold lower bound |
| ---: | ---: | ---: |
| 94 | 149 | 35.3900 |
| 147 | 233 | 45.5794 |
| 200 | 317 | 63.9545 |
| 253 | 401 | 107.0018 |
| 306 | 485 | 325.9149 |

The irrational-rotation proof establishes unboundedness; the finite records
only make the obstruction inspectable.

### 3.4 한국어 해석과 한계

`2^S>3^m`은 곱셈 부분이 수축한다는 뜻이지만 `+1` 항들이 누적된
`C(w)`를 자동으로 이기지는 못한다. 평균 valuation이 충분히 크다는
사실만으로는 모든 시작값에 공통으로 적용되는 하강 임계값을 얻을 수
없다.

이 결과는 발산 궤도를 만들지 않는다. 실제 자연수 궤도가 언젠가 자기
prefix의 정확한 임계값을 넘는다는 명제가 여전히 필요하다. 모든
`n>1`에 대해 그런 더 작은 iterate가 존재하면 강한 귀납법으로
콜라츠 추측이 따라오므로, 다음 명제는 본질적인 증명 간극이다.

### 3.5 Rejected route

Discard:

```text
PositiveAverageLogContractionUniformlyBoundsAffineThreshold
```

Next lemma:

```text
EveryNaturalOddOrbitHasARealizedPrefixAboveItsExactAffineThreshold
```

---

## 4. Strong Goldbach conjecture

### 4.1 Declared proposition

Let `F(k)` be the length-`L` DFT of a finite prime indicator and partition the
frequencies into major and minor sets. Fourier inversion gives

```text
r(n) = M(n) + E(n)
```

exactly, and

```text
|E(n)| <= (1/L) sum_(k in minor) |F(k)|^2.
```

Thus a finite positivity certificate is valid whenever

```text
M(n) > minor L2 energy.
```

However, minor energy cannot determine coefficient sign on the ambient class
of real sequences. Declare a symmetric two-frequency support `k=+/-1` to be
minor and consider the Hermitian spectra:

```text
F_+(+/-1) = (1,1),
F_-(+/-1) = (i,-i).
```

They have identical frequency magnitudes and energy. After pointwise
squaring, their zero Fourier coefficients are exact opposites.

### 4.2 Proof

The coefficient decomposition is Fourier inversion. The triangle inequality
and

```text
|F(k)^2| = |F(k)|^2
```

give the energy upper bound. The two displayed spectra are Hermitian and
therefore correspond to real sequences. Squaring changes both supported
values from `+1` to `-1` while preserving every magnitude, proving that the
energy summary loses the phase needed to know the coefficient sign. This is
a no-go for the summary statistic on real sequences, not a counterexample
constructed from the DFT of the primes. A prime-specific proof may use extra
arithmetic structure, but that structure is not contained in unsigned energy.

### 4.3 Finite audit

The DFT audit covers:

```text
N in {1000,2000,4000,8000}
Q in {4,8}
```

for eight total settings. FFT convolution agrees with direct ordered-prime
representation counts within `1e-7`. No even number in the tested ranges has
zero observed representations. The unsigned energy test certifies `0/8`
settings.

The zero certificate count is not evidence against Goldbach. It diagnoses an
overly expensive absolute bound: the actual minor coefficient is much smaller
than its energy envelope because of phase cancellation.

### 4.4 한국어 해석과 한계

minor arc 에너지는 안전한 상계이지만 모든 항의 절댓값을 더하므로
상쇄 위상을 버린다. 일반 실수열에서는 같은 에너지로도 목표 계수의
부호가 바뀌는 정확한 반례가 있다. 이것은 소수 DFT 자체의 반례가
아니라 energy-only 요약의 no-go다. 소수의 추가 산술 구조를 쓰는
경로는 남아 있지만 그 구조는 unsigned energy 안에 들어 있지 않다.

유한 범위에서 골드바흐 표현이 모두 존재한 것은 무한 증명이 아니다.
필요한 것은 실제 소수 지수합의 signed coefficient를 major margin보다
작게 만드는 산술적이고 위상 민감한 추정이다.

### 4.5 Rejected route

Discard:

```text
UnsignedMinorArcEnergyDeterminesCoefficientSign
```

Next lemma:

```text
PhaseSensitiveBilinearMinorArcCoefficientBelowExplicitSingularSeriesMargin
```

---

## 5. Twin Prime conjecture

### 5.1 Declared proposition

Let `D_z(n,n+2)` be the vector of divisibility bits by every prime `p<=z`.
On the rough stratum

```text
gcd(n(n+2), P(z)) = 1,
```

every bit in `D_z` is zero. Therefore

```text
I(Y;D_z | z-rough) = 0
```

for the twin-prime label `Y`. Every classifier measurable only from these
low-divisor bits is constant on the rough fiber. If that fiber contains both
a twin-prime pair and a non-twin pair, no such classifier can classify both
correctly.

### 5.2 Proof

The roughness condition is exactly the statement that no prime `p<=z` divides
either coordinate, so the feature vector is constant. A constant random
variable has zero mutual information with every label. Two examples with
different labels in the same feature fiber prove the classification no-go.

### 5.3 Finite audit

The bounded audit scans odd `n<250,000` for ten roughness bounds from `3` to
`31`. Every rough fiber contains both twin-prime and double-composite
witnesses. At `z=31`, for example:

| Metric | Value |
| --- | ---: |
| Rough pairs | 7,766 |
| Twin-prime pairs | 2,583 |
| Double-composite pairs | 1,389 |
| First twin witness | `(41,43)` |
| First double-composite witness | `(4181,4183)` |
| Conditional low-divisor information | `0 bits` |

The zero information value is exact because the conditioned feature is
constant, not because of a floating-point estimate.

### 5.4 한국어 해석과 한계

작은 소수로 나누어지는지를 모두 검사한 뒤 살아남은 rough 집합에서는
그 나눗셈 정보가 전부 0이다. 따라서 같은 정보로는 진짜 소수쌍과
큰 소인수만 가진 합성수쌍을 구별할 수 없다. TICKET-158에서 사용한
mutual information도 입력 특징이 이 저소수 정보에만 국한되면 rough
fiber 내부에서는 정확히 0이 된다.

이 결과는 모든 가능한 방법이 실패한다는 정리가 아니다. Type II
합, bilinear correlation, Möbius/Liouville 부호처럼 비국소적이고
parity에 민감한 정보는 이 sigma algebra 밖에 있다. 바로 그 추가
정보에 대한 균일한 하한이 아직 없다.

### 5.5 Rejected route

Discard:

```text
LowDivisorInformationSeparatesPrimeAndSemiprimeRoughPairs
```

Next lemma:

```text
NonlocalTypeIIOrParitySensitiveCorrelationSeparatesPrimePairsFromRoughCompositePairsUniformly
```

---

## 6. Literature boundary / 문헌 경계

- [Groskin, finite Guinand-Weil dictionary and archimedean tail
  order](https://arxiv.org/abs/2607.02828): external fixed-`(c,N)` tail
  context; it does not supply PrimeProject's missing prime/band majorant.
- [Tao, Almost all Collatz orbits attain almost bounded
  values](https://arxiv.org/abs/1909.03562): an almost-all theorem, not the
  pointwise threshold-crossing lemma.
- [Helfgott, The ternary Goldbach
  problem](https://arxiv.org/abs/1501.05438): primary explicit
  major/minor-arc and large-sieve context; ternary estimates are not silently
  reused for binary Goldbach.
- [Ford and Maynard, On the theory of prime producing
  sieves](https://arxiv.org/abs/2407.14368): primary evidence that substantial
  Type II information is necessary for prime lower bounds.
- [Liao, Prime Event
  Languages](https://arxiv.org/abs/2606.08395): recent finite empirical
  information analysis; its short-range signal is not a Twin Prime proof.

문헌의 정리와 PrimeProject의 새 결과는 분리한다. 특히 최근 논문의
수치 실험이나 정보 신호를 무한 정리로 취급하지 않으며, 외부 정리를
프로젝트의 독창적 증명으로 주장하지 않는다.

---

## 7. Proof DAG summary / 증명 DAG 요약

| Problem | Rejected | Proved in TICKET-159 | Open next lemma |
| --- | --- | --- | --- |
| RH | Preassigned rate from pointwise convergence | Effective diagonal selector and schedule no-go | Certified actual error and positive core margin |
| Collatz | Average contraction gives a uniform threshold | Exact cylinder threshold and unboundedness no-go | Realized threshold crossing for every odd orbit |
| Goldbach | Unsigned energy determines coefficient sign | Exact energy bound and phase-blindness counterpair | Phase-sensitive bilinear minor coefficient bound |
| Twin Prime | Low-divisor information separates rough survivors | Constant-fiber zero-information theorem | Uniform nonlocal parity-sensitive separation |

The four open nodes are not administrative follow-ups. Each names the exact
mathematical input that would have to be proved before the corresponding
conjecture can move beyond `open_not_proven`.

네 open node는 단순한 개발 할 일이 아니다. 각 항목은 해당 추측을
`open_not_proven`에서 이동시키기 위해 실제로 필요한 수학 정리를
정확히 지정한다.

## 8. Final claim boundary / 최종 주장 경계

TICKET-159 proves:

1. effective diagonal cutoff selection under explicit computable majorants;
2. an exact no-go for deriving a preassigned rate from pointwise convergence;
3. the Collatz affine cylinder threshold and an unbounded average-excess
   threshold family;
4. an exact Goldbach minor-energy coefficient bound and phase-blindness
   counterpair;
5. exact zero conditional information for low-divisor features on the Twin
   rough fiber.

TICKET-159 does not prove or disprove any of the four conjectures.

TICKET-159가 증명한 것은 cutoff 선택 논리, affine 임계값, 위상 맹목성,
rough fiber 정보 소실에 관한 부분정리와 no-go 정리다. 네 난제 중
어느 것도 증명하거나 반증하지 않았다.
