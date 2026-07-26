# TICKET-161: Common Cores, Baker Reduction, Reflection Angles, and Type II Incidence

## Abstract

TICKET-161 continues the four-conjecture program from TICKET-160. It does not
claim a proof or counterexample for any target conjecture. It proves four
smaller exact theorems and rejects four additional shortcuts.

1. A common compact \(H^1\) core can be transported into the mutually
   non-nested Riemann cutoff spaces in \(L^2\), provided the Fourier resolution
   satisfies \(N/L\to\infty\). A fixed or vanishing resolution ratio leaves a
   positive error for a tent function.
2. The minimally contracting front-loaded Collatz family descends for all
   sufficiently large lengths by combining its exact affine threshold with an
   effective lower bound for a linear form in \(\log 2,\log 3\). Any remaining
   failure must be a continued-fraction event.
3. The harmful part of a Goldbach minor coefficient is exactly a targetwise
   reflection angle. This strictly sharpens the unsigned energy bound, but
   average or RMS angle control cannot imply pointwise positivity.
4. Separate divisor marginals cannot detect a zero-marginal checkerboard,
   whereas a rank-one bilinear statistic detects it exactly. This isolates the
   Type II information needed beyond fixed or marginal Twin features.

All four proof DAGs end at `open_not_proven`. External theorems are identified
explicitly, and no priority claim is made without independent review.

## 초록

TICKET-161은 TICKET-160에서 남긴 네 보조정리를 더 작은 증명 의무로
축소한다. 네 난제 중 어느 것도 해결하거나 반증했다고 주장하지 않는다.

1. 서로 다른 Riemann cutoff 공간은 직접 중첩되지 않지만, 공통 compact
   \(H^1\) core는 \(N/L\to\infty\)인 Fourier 해상도에서 \(L^2\)로 옮길 수
   있다. 반대로 \(N/L\)이 유계이거나 0으로 가면 tent 함수의 오차가 남는다.
2. 최소 수축 front-loaded Collatz 가족은 충분히 큰 모든 길이에서
   자연수 실현자가 하강한다. 핵심은 정확한 affine threshold와
   \(\log 2,\log 3\) 선형형식에 대한 Baker-Wüstholz 하한의 결합이다.
   실패 가능 길이는 continued-fraction 근사에만 남는다.
3. Goldbach minor coefficient에서 실제로 해로운 양은 endpoint별
   reflection angle이다. 이는 unsigned energy보다 강하지만, 평균 또는
   RMS angle이 작다는 사실만으로 모든 endpoint의 양성을 보장할 수 없다.
4. 쌍둥이 소수 트랙에서는 row와 column marginal이 모두 0인
   checkerboard를 Type-I 정보가 볼 수 없지만 bilinear Type-II 통계는
   정확히 검출한다. 따라서 별도 divisor marginal만으로 parity 장벽을
   넘을 수 없다.

모든 proof DAG는 `open_not_proven`으로 끝난다. 유한 계산과 무한 정리를
명확히 분리하며, 외부 정리는 출처와 적용 범위를 함께 표시한다.

## 한국어 상세 결과

### 리만 가설: 공통 core 수송

\(0<a<L\)이고 \(f\in H^1_0(-a,a)\)를 \((-L,L)\)에 0으로
연장하며 \(P_{L,N}\)을 \(|k|\le N\) Fourier mode로의 직교사영이라
하자. Parseval 항등식과 미분 에너지로부터

\[
\|f-P_{L,N}f\|_2
\le
\frac{L}{\pi(N+1)}\|f'\|_2
\]

를 얻는다. 따라서 고정된 유한차원 compact \(H^1\) core는
\(N/L\to\infty\)인 schedule에서 공통 \(L^2\) 공간으로 유효하게
수송된다. 반대로 tent 함수 \(f(x)=\max(1-|x|,0)\)는 \(N/L\)이
유계이면 양의 Fourier tail을 남긴다. 15개 유한 audit row에서
\(N=L^2,L=32\)의 오차는 \(0.000791\)이다. 남은 단일 보조정리는
`UniformWeilFormGraphNormTransportOnResolvedCommonCore`이다.
\(L^2\) 수렴만으로 Weil 이차형식의 부호나 양의 margin은 보존되지
않으므로 이 결과는 RH 증명이 아니다.

### 콜라츠 추측: 최소 front-loaded 가족

\(\alpha=\log_2 3\), \(S_m=\lceil m\alpha\rceil\),
\(b_m=S_m-m+1\), \(w_m=(b_m,1,\ldots,1)\)로 둔다. 모든 자연수
실현자는 한 양의 \(t\bmod3\) residue class에서

\[
n=\frac{2^{S_m+1}t-2^{b_m}-1}{3}
\]

로 주어지고, \(m\)회의 가속 odd step 뒤 값은
\(2\cdot3^{m-1}t-1\)이다. 하강은

\[
(2^{S_m}-3^m)t>2^{b_m-1}-1
\]

과 정확히 동치다. \(m\ge4\)에서 실패하면
\(0<S_m/m-\alpha<1/(2m^2)\)이므로 기약분수 \(S_m/m\)은
Legendre 판정에 따라 \(\alpha\)의 연분수 수렴분수여야 한다. 동시에
실패는 \(\Lambda_m=S_m\log2-m\log3=O(2^{-m})\)을 강제하지만,
Baker-Wüstholz 하계는 \(|\Lambda_m|>c m^{-C}\)를 준다. 따라서 이
한 가족의 모든 자연수 실현자는 충분히 큰 \(m\)에서 하강한다.

\(2\le m\le50{,}000\) 정수 audit에서는 실패가 0건이고 최소 하강비는
\(m=5\)의 \(13/7\)이다. 일반 Baker 상수의 명시적 수치 임계값과 그
아래 유한 폐쇄는 아직 없으며, 이 가족은 모든 자연수 궤도를 덮지
않는다. 다음 보조정리는
`ExplicitBakerThresholdAndFiniteClosureForMinimalFrontLoadedFamily`이다.

### 강한 골드바흐 추측: targetwise reflection angle

대칭 minor-frequency 사영을 \(P\), \(h=Pf\), target reflection을
\(R_N\)이라 하고
\(\rho_N=\langle h,R_Nh\rangle/\|h\|_2^2\)로 두면

\[
G_f(N)=M(N)+\rho_N\|h\|_2^2.
\]

\(\eta_N=\max(0,-\rho_N)\)는
\(G_f(N)\ge M(N)-\eta_N\|h\|_2^2\)라는 정확한 하한을 준다. 그러나
\((\delta_0-\delta_1)/\sqrt2\)는 한 target에서 coefficient \(-1\)을
가지면서 평균 절댓값 \(2/L\)과 RMS \(\sqrt{3/(2L)}\)는 0으로 간다.
따라서 평균 또는 RMS angle을 점별 양성으로 승격하는 경로는
폐기된다.

다섯 prime DFT 범위에서는 energy-only 인증이 0건이고 phase-aware
항등식은 15,495개 target을 재구성한다. 이 angle은 같은 prime DFT에서
계산한 진단값이므로 독립적인 해석적 상계가 아니다. 다음 보조정리는
`UniformPrimeMinorReflectionAngleBelowMajorArcMargin`이다.

### 쌍둥이 소수 추측: zero-marginal Type-II 필요성

\[
H_a=\begin{pmatrix}a&-a\\-a&a\end{pmatrix}
\]

는 모든 행·열 주변합이 0이어서 주변합만 사용하는 가법적 Type-I
통계에 보이지 않지만
\((1,-1)H_a(1,-1)^\mathsf T=4a\)이므로 bilinear 상관은 남는다.
일반 joint count matrix \(C\), total \(T\), row margin \(r\), column
margin \(c\)에 대해 \(H=TC-rc^\mathsf T\)도 정확히 zero-marginal이다.

cubic-rough double-semiprime pair의 least-factor incidence를 10M까지
계산한 normalized top singular ratio는
\(0.10418,0.05363,0.01541,0.01237\)이다. 이 감소는 네 유한 점의
관찰이며 균일 Type-II 정리도 양의 twin-prime 하계도 아니다. 다음
보조정리는 `UniformCubicRoughCenteredIncidenceSpectralDecay`이다.

## 1. Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket161_commoncore_baker_angle_typeii.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket161_commoncore_baker_angle_typeii
```

Expected machine contract:

```json
{
  "exact_theorem_count": 4,
  "rejected_target_count": 4,
  "proof_dag_count": 4,
  "conjecture_resolution_count": 0,
  "total_failure_count": 0
}
```

Canonical artifact:

`data/open-problem/ticket161-commoncore-baker-angle-typeii.json`

## 2. Riemann Hypothesis

### 2.1 Exact proposition

Let \(0<a<L\), let \(f\in H^1_0(-a,a)\), and extend \(f\) by zero to
\(I_L=(-L,L)\). Let \(P_{L,N}\) be the orthogonal projection onto

\[
\operatorname{span}\left\{
e^{i\pi kx/L}: |k|\le N
\right\}.
\]

Then

\[
\boxed{
\|f-P_{L,N}f\|_2
\le
\frac{L}{\pi(N+1)}\|f'\|_2.
}
\]

Consequently, every fixed finite-dimensional compact \(H^1\) core admits an
effective common \(L^2\) transport into the raw cutoff spaces whenever

\[
\frac{L}{N+1}\longrightarrow0.
\]

For the tent

\[
\tau(x)=\max(1-|x|,0),
\]

if \(N/L\) stays bounded, the projection misses a positive Fourier tail. If
\(N/L\to0\), its captured energy tends to zero.

### 2.2 Proof

Write \(c_k\) for the normalized Fourier coefficient on \(I_L\). Parseval for
the weak derivative gives

\[
\|f'\|_2^2
=
\sum_{k\in\mathbb Z}
\left(\frac{\pi k}{L}\right)^2|c_k|^2.
\]

Therefore

\[
\sum_{|k|>N}|c_k|^2
\le
\left(\frac{L}{\pi(N+1)}\right)^2\|f'\|_2^2.
\]

For the tent,

\[
c_0=\frac1{\sqrt{2L}},
\qquad
c_k=
\frac{2\left(1-\cos(\pi k/L)\right)}
     {(\pi k/L)^2\sqrt{2L}}
\quad(k\ne0).
\]

These coefficients produce the finite audit exactly. If \(N/L\to\tau<\infty\),
the Riemann sum captures only the bounded Fourier interval
\([-\pi\tau,\pi\tau]\). Since the tent is not band limited, the complementary
energy is positive. If \(N/L\to0\), then

\[
\sum_{|k|\le N}|c_k|^2
\le
\frac{2N+1}{2L}\|\tau\|_1^2
\longrightarrow0.
\]

### 2.3 Reproducible computation

| \(L\) | schedule | \(N\) | \(N/L\) | \(L^2\) error |
|---:|---|---:|---:|---:|
| 2 | resolved quadratic | 4 | 2 | 0.044404 |
| 4 | resolved quadratic | 16 | 4 | 0.017175 |
| 8 | resolved quadratic | 64 | 8 | 0.006260 |
| 16 | resolved quadratic | 256 | 16 | 0.002232 |
| 32 | resolved quadratic | 1,024 | 32 | 0.000791 |
| 4 | critical linear | 16 | 4 | 0.017175 |
| 8 | critical linear | 32 | 4 | 0.017174 |
| 16 | critical linear | 64 | 4 | 0.017174 |
| 32 | critical linear | 128 | 4 | 0.017174 |

The constant error on the linear schedule is not floating-point evidence for
RH. It is a numerical illustration of the exact finite-resolution theorem.

### 2.4 Rejected route

Discard:

- using bounded \(N/L\) as a common-core approximation schedule;
- treating \(L^2\) convergence as automatic convergence of the Weil form;
- importing positivity from one cutoff without a graph-norm estimate.

### 2.5 Remaining gap

The Weil form may be unbounded in the ambient \(L^2\) norm. An \(L^2\)-small
transport error therefore need not be small in form norm.

Next lemma:

`UniformWeilFormGraphNormTransportOnResolvedCommonCore`

It must bound the transported Weil quadratic form uniformly in the cutoff and
preserve a positive margin on a dense common core.

## 3. Collatz Conjecture

### 3.1 Exact proposition

Let

\[
\alpha=\log_2 3,\qquad
S_m=\lceil m\alpha\rceil,\qquad
b_m=S_m-m+1,
\]

and consider the minimally contracting front-loaded word

\[
w_m=(b_m,\underbrace{1,\ldots,1}_{m-1}).
\]

Put

\[
D_m=2^{S_m}-3^m.
\]

Every natural realizer is parameterized by

\[
\boxed{
n=
\frac{2^{S_m+1}t-2^{b_m}-1}{3},
}
\]

where \(t\) belongs to one positive residue class modulo 3. Its endpoint after
\(m\) accelerated odd steps is

\[
\boxed{
A^m(n)=2\cdot3^{m-1}t-1.
}
\]

Hence

\[
\boxed{
A^m(n)<n
\iff
D_mt>2^{b_m-1}-1.
}
\]

If this inequality fails for \(m\ge4\), then

\[
0<
\frac{S_m}{m}-\alpha
<
\frac1{2m^2}.
\]

After reduction, \(S_m/m\) must therefore be a continued-fraction convergent
of \(\alpha\).

Finally, the Baker-Wüstholz lower bound for the nonzero linear form

\[
\Lambda_m=S_m\log2-m\log3
\]

is polynomially small in \(m\), while failure requires an exponentially small
window \(O(2^{-m})\). Thus:

\[
\boxed{
\text{all natural realizers of }w_m
\text{ descend for every sufficiently large }m.
}
\]

This is an unconditional eventual theorem for this one family, not the Collatz
conjecture.

### 3.2 Proof

The valuation-one tail forces the first post-front value to be
\(2^mt-1\). Inverting the first step gives the formula for \(n\). The tail
recurrence \(x+1\mapsto3(x+1)/2\) gives the endpoint formula.

If descent fails, then

\[
D_m<2^{S_m-m}.
\]

Writing \(\Lambda_m=S_m\log2-m\log3\),

\[
1-e^{-\Lambda_m}<2^{-m}.
\]

Therefore

\[
\Lambda_m<-\log(1-2^{-m}),
\]

and for \(m\ge4\),

\[
\frac{\Lambda_m}{m\log2}<\frac1{2m^2}.
\]

Legendre's criterion reduces failure to a continued-fraction convergent.
Baker-Wüstholz supplies effective constants \(c,C>0\) such that

\[
|\Lambda_m|>c\,m^{-C}.
\]

Since \(m^{-C}\gg2^{-m}\), the failure inequality is impossible for all
sufficiently large \(m\).

### 3.3 Finite exact audit

The script checks every \(2\le m\le50{,}000\) with integer arithmetic.

- observed failures: 0;
- minimum observed descent ratio:
  \[
  \frac{D_mt}{2^{b_m-1}-1}=\frac{13}{7}
  \quad\text{at }m=5;
  \]
- every continued-fraction candidate in the scanned range descends;
- large integers are stored by bit length and decimal digit count when an
  exact decimal string would be unsafe for JSON or JavaScript.

This finite audit does not fill the interval up to the explicit
Baker-Wüstholz threshold.

### 3.4 Rejected route

Discard:

- treating average contraction as sufficient for the minimal word;
- scanning every length without isolating Diophantine candidates;
- treating the 50,000 scan as the eventual theorem.

### 3.5 Remaining gap

The effective constant supplied by a general logarithmic-form theorem is not
made computationally sharp here. The family is also only one valuation order
and does not cover arbitrary natural Collatz orbits.

Next lemma:

`ExplicitBakerThresholdAndFiniteClosureForMinimalFrontLoadedFamily`

It must produce a numerical threshold and verify every remaining candidate
below it.

## 4. Strong Goldbach Conjecture

### 4.1 Exact proposition

Let \(P\) be a symmetric minor-frequency projection on
\(\mathbb Z/L\mathbb Z\), let \(h=Pf\), and let

\[
(R_Nh)(x)=h(N-x).
\]

Define

\[
\rho_N=
\frac{\langle h,R_Nh\rangle}{\|h\|_2^2},
\qquad
\eta_N=\max(0,-\rho_N).
\]

If \(M(N)\) is the complementary major coefficient, then

\[
\boxed{
G_f(N)=M(N)+\rho_N\|h\|_2^2
}
\]

and

\[
\boxed{
G_f(N)\ge M(N)-\eta_N\|h\|_2^2.
}
\]

This is exact. Replacing \(\eta_N\) by 1 recovers the phase-blind Cauchy bound.

However, average control is insufficient. On \(\mathbb Z/L\mathbb Z\), let

\[
h=\frac{\delta_0-\delta_1}{\sqrt2}.
\]

Its reflection coefficients are \(1/2,-1,1/2\) at targets \(0,1,2\) and zero
elsewhere. Therefore

\[
\max_N(-\rho_N)_+=1,
\]

while

\[
\frac1L\sum_N|\rho_N|=\frac2L\to0,
\qquad
\left(\frac1L\sum_N|\rho_N|^2\right)^{1/2}
=\sqrt{\frac3{2L}}\to0.
\]

Thus neither mean nor RMS reflection-angle decay proves pointwise Goldbach
positivity.

### 4.2 Finite prime DFT audit

The finite audit uses prime indicators, a power-of-two transform, and a
Farey-denominator mask with \(Q=8\).

| even range | minor energy | max harmful angle | energy certificates | phase-aware identities |
|---:|---:|---:|---:|---:|
| 1,000 | 83.330 | 0.2012 | 0 | 499 / 499 |
| 2,000 | 164.403 | 0.1523 | 0 | 999 / 999 |
| 4,000 | 321.044 | 0.1185 | 0 | 1,999 / 1,999 |
| 8,000 | 622.655 | 0.1141 | 0 | 3,999 / 3,999 |
| 16,000 | 1,205.459 | 0.0776 | 0 | 7,999 / 7,999 |

The phase-aware count is not an independent proof: \(\rho_N\) is computed from
the same prime DFT as the target coefficient. Its purpose is to identify the
exact analytic quantity that a proof must bound without observing the answer.

### 4.3 Rejected route

Discard:

- unsigned minor energy as the final certificate;
- average harmful angle;
- RMS harmful angle;
- finite phase-aware replay as an infinite binary theorem.

### 4.4 Remaining gap

The targetwise negative reflection angle needs an independent arithmetic bound
smaller than the normalized major-arc margin for every sufficiently large even
integer.

Next lemma:

`UniformPrimeMinorReflectionAngleBelowMajorArcMargin`

## 5. Twin Prime Conjecture

### 5.1 Exact proposition

For \(a\ne0\), consider

\[
H_a=
\begin{pmatrix}
a&-a\\
-a&a
\end{pmatrix}.
\]

Every row sum and column sum is zero. Hence every additive statistic based only
on separate row and column marginals is blind to \(H_a\). But

\[
\boxed{
\begin{pmatrix}1&-1\end{pmatrix}
H_a
\begin{pmatrix}1\\-1\end{pmatrix}
=4a.
}
\]

This is an exact minimal model of Type-I marginal blindness and Type-II
bilinear visibility.

For a finite joint incidence matrix \(C\), total \(T\), row margins \(r\), and
column margins \(c\), define

\[
\boxed{
H=TC-rc^\mathsf T.
}
\]

Then every row and column sum of \(H\) is exactly zero. A nonzero singular
value of \(H\) is a bilinear dependence witness invisible to the marginals.

### 5.2 Cubic-rough finite audit

The audit retains pairs \(n,n+2\le X\) whose least factors exceed
\(\lfloor X^{1/3}\rfloor\). Every retained composite endpoint is therefore a
semiprime. Least factors are placed into four logarithmic bins.

| \(X\) | double-semiprime pairs | normalized top centered singular value |
|---:|---:|---:|
| 10,000 | 35 | 0.10418 |
| 100,000 | 284 | 0.05363 |
| 1,000,000 | 2,453 | 0.01541 |
| 10,000,000 | 19,074 | 0.01237 |

The decrease is a finite observation. It is not a Type-II theorem and does not
give a twin-prime lower bound.

### 5.3 Rejected route

Discard:

- separate divisor marginals as parity-breaking information;
- a fixed finite list of Type-I features;
- interpreting the observed four-scale spectral decrease as an asymptotic.

### 5.4 Remaining gap

The centered incidence observable must be bounded uniformly over a growing
range with arithmetic weights compatible with a prime-producing lower-bound
sieve.

Next lemma:

`UniformCubicRoughCenteredIncidenceSpectralDecay`

## 6. Literature boundary / 문헌 경계

- [Groskin, finite Guinand-Weil dictionary and archimedean tail
  order](https://arxiv.org/abs/2607.02828): supplies the external finite
  dictionary and tail setting. TICKET-161 proves only the Fourier-resolution
  transport reduction.
- [Baker and Wüstholz, *Logarithmic forms and group
  varieties*](https://doi.org/10.1515/crll.1993.442.19): supplies the
  established effective linear-form lower bound. The Collatz front-loaded
  application is a repository-level synthesis.
- [Tao, *Almost all orbits of the Collatz map attain almost bounded
  values*](https://arxiv.org/abs/1909.03562): establishes an almost-all result,
  not the pointwise theorem required here.
- [Helfgott, *The ternary Goldbach
  problem*](https://arxiv.org/abs/1501.05438): provides explicit Type I/II
  minor-arc machinery for ternary Goldbach. It is not a binary Goldbach
  theorem.
- [Ford and Maynard, *On the theory of prime producing
  sieves*](https://arxiv.org/abs/2407.14368): proves that substantial Type II
  information is necessary in their general lower-bound framework.
  TICKET-161 does not verify those hypotheses for twins.

한국어 경계: Baker-Wüstholz, Legendre criterion, Tao의 almost-all 정리,
Helfgott의 ternary minor-arc 분석, Ford-Maynard의 prime-producing sieve는
외부의 확립된 결과다. 이 문서는 그 정리들을 네 개의 현재 proof gap에
연결하지만, 외부 정리를 PrimeProject의 독창적 정리로 주장하지 않는다.

## 7. Proof DAG summary

```text
RH:
  refuted: L2TransportAlonePreservesWeilPositivity
  -> proved: ResolvedCommonCoreL2TransportAndFormNormNoGo
  -> open: UniformWeilFormGraphNormTransportOnResolvedCommonCore

Collatz:
  refuted: AverageDriftClosesMinimalFrontLoadedTransfer
  -> proved: AsymptoticMinimalFrontLoadedDescentAndConvergentReduction
  -> open: ExplicitBakerThresholdAndFiniteClosureForMinimalFrontLoadedFamily

Goldbach:
  refuted: AverageMinorReflectionAngleImpliesPointwisePositivity
  -> proved: TargetwiseReflectionAngleCriterionAndAverageAngleNoGo
  -> open: UniformPrimeMinorReflectionAngleBelowMajorArcMargin

Twin Prime:
  refuted: SeparateDivisorMarginalsSupplyTwinParityBreaking
  -> proved: ZeroMarginalCheckerboardAndTypeIIBilinearNecessity
  -> open: UniformCubicRoughCenteredIncidenceSpectralDecay
```

## 8. Final claim boundary / 최종 주장 경계

Established:

- four exact theorem or no-go results;
- one unconditional eventual theorem for one explicit Collatz word family;
- one exact continued-fraction reduction;
- one constructive \(L^2\) common-core transport;
- one exact Goldbach targetwise phase criterion;
- one exact Type-I marginal blindness theorem;
- reproducible finite audits with zero machine failures.

Not established:

- RH or an off-critical zero;
- the Collatz conjecture or a divergent orbit;
- strong Goldbach or an even counterexample;
- infinitely many twin primes or a terminal counterexample;
- a uniform Weil graph-norm transport;
- a numerically closed Baker threshold;
- a uniform binary minor-angle theorem;
- a uniform Twin Type-II spectral decay theorem.
