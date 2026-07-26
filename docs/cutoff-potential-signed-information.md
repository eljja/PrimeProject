# TICKET-156: Cutoff, Potential, Signed Mass, and Normalized Information

## Claim boundary / 주장 경계

This report does **not** prove or disprove the Riemann hypothesis, Collatz
conjecture, strong Goldbach conjecture, or Twin Prime conjecture. It proves
four exact bridge or no-go statements and reports bounded computations.
Every target conjecture remains `open_not_proven`.

이 보고서는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 증명하거나 반증하지 않는다. 네 개의 정확한 연결 정리 또는
불가능성 결과와 유한 계산을 제시할 뿐이다. 네 추측은 모두
`open_not_proven`, 즉 미해결 상태다.

| Problem / 문제 | New exact result / 새 정확 결과 | Discarded route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| Riemann / 리만 | Three independent errors are required for a spectral certificate; fixed-cutoff precision stability has no continuum-sign implication / spectral 인증에는 세 오차의 독립 상계가 필요하며, 고정 cutoff의 정밀도 안정성은 continuum 부호를 결정하지 못함 | Promote stable finite-cutoff eigenvalues without a cutoff error / cutoff 오차 없이 안정된 유한 고유값을 승격 | `ExplicitWeilGalerkinCoreAndUniformTwoAxisOperatorErrorBound` |
| Collatz / 콜라츠 | Exact weighted suffix potential equals the normalized affine constant; floor two is sufficient but not necessary / 가중 접미사 potential은 정규화 affine 상수와 정확히 같고 floor-two는 충분조건일 뿐 필요조건이 아님 | Require every first descent to satisfy floor two / 모든 첫 하강에 floor-two를 요구 | `EveryNaturalValuationRayCrossesItsWeightedSuffixPotential` |
| Goldbach / 골드바흐 | Only negative real minor phase mass is harmful; full Parseval energy overcharges helpful mass / 음의 실수 minor 위상 질량만 해로우며 전체 Parseval 에너지는 유리한 질량까지 손실로 계산 | Treat full minor energy as the necessary binary loss / 전체 minor 에너지를 필수 손실로 간주 | `UniformBinaryGoldbachMinorNegativePhaseMassBoundWithFiniteJoin` |
| Twin Prime / 쌍둥이 소수 | Rare-event transfer requires information normalized by selection mass / 희귀사건 전이에는 선택 질량으로 정규화한 정보량이 필요 | Use \(I(D;B)\to0\) without comparing it with \(P(B)\) / \(P(B)\)와 비교하지 않은 정보량 수렴 사용 | `ShiftTwoCubicRoughMutualInformationLittleOSelectionMass` |

Machine-readable source / 기계 판독 원본:
[`ticket156-cutoff-potential-signed-information.json`](../data/open-problem/ticket156-cutoff-potential-signed-information.json).

```text
python scripts/ticket156_cutoff_potential_signed_information.py
python -m unittest tests.test_ticket156_cutoff_potential_signed_information -v
```

## 1. Riemann hypothesis / 리만 가설

### 1.1 Declared proposition / 선언 명제

Let \(A\) be the target self-adjoint operator or exact core and let
\(A_{N,T,p}\) be a computed Hermitian approximation. Suppose

\[
\|A-A_{N,T,p}\|
\le \varepsilon_N+\varepsilon_T+\varepsilon_p,
\]

where \(N\) is the basis/core cutoff, \(T\) is the archimedean cutoff, and
\(p\) is working precision. Then

\[
\lambda_{\min}(A)
\ge \lambda_{\min}(A_{N,T,p})
   -\varepsilon_N-\varepsilon_T-\varepsilon_p.
\]

Therefore finite positivity is promoted only when the computed margin is
larger than the sum of all three independently justified errors.

한국어로는 계산 고유값이 양수라는 사실만으로 충분하지 않다. basis/core
절단 오차 \(\varepsilon_N\), archimedean 절단 오차 \(\varepsilon_T\),
반올림 오차 \(\varepsilon_p\)를 각각 상계하고 그 합보다 계산 margin이
커야 한다.

### 1.2 Proof and no-go / 증명과 no-go

Weyl's perturbation inequality gives

\[
|\lambda_{\min}(A)-\lambda_{\min}(A_{N,T,p})|
\le \|A-A_{N,T,p}\|.
\]

The displayed certificate follows by the triangle inequality. Precision
stability cannot replace \(\varepsilon_T\). For any finite cutoff ceiling,
choose \(M\) above it and consider the exact scalar Hermitian families

\[
A_T^+=1-\frac MT,\qquad A_T^-=-1+\frac MT.
\]

For every audited \(T<M\), \(A_T^+<0<A_T^-\), while

\[
\lim_{T\to\infty}A_T^+=1,\qquad
\lim_{T\to\infty}A_T^-=-1.
\]

These are abstract counterfamilies, not truncated Weil matrices. They prove
only that digits and a finite cutoff sweep have no general continuum-sign
implication.

이 반례 가족은 실제 Weil 행렬이 아니다. “고정 \(T\)에서 자릿수를
늘렸더니 부호가 안정됐다” 또는 “큰 유한 범위에서 같은 부호였다”라는
논리만으로 cutoff-free 부호를 결론낼 수 없음을 보이는 일반적 no-go다.

### 1.3 Reproducible audit / 재현 감사

With \(M=4096\), the script checks \(T=64,\ldots,2048\). Every value is an
exact rational number and has the finite sign opposite to its limit. It
also checks two three-axis budgets: a computed margin \(1/2\) minus total
error \(7/16\) certifies \(1/16>0\), whereas margin \(1/4\) does not.

**Remaining gap / 남은 간극:** construct the actual Weil Galerkin core and
prove uniform basis and archimedean-tail operator bounds. No such
construction is supplied.

## 2. Collatz conjecture / 콜라츠 추측

### 2.1 Exact weighted potential / 정확 가중 potential

For an accelerated odd-map valuation word \(a_1,\ldots,a_m\), write

\[
T^m(n)=\frac{3^m n+C}{2^S},\qquad S=\sum_{i=1}^m a_i.
\]

Let \(A_r\) be the sum of the final \(r\) valuations and define

\[
\Phi(a_1,\ldots,a_m)
=\sum_{r=1}^{m}\frac{3^{r-1}}{2^{A_r}}.
\]

Unrolling the affine recurrence proves the exact identity

\[
\Phi=\frac{C}{2^S}.
\]

When \(2^S>3^m\), define

\[
\theta=\frac{C}{2^S-3^m}
=\frac{\Phi}{1-3^m/2^S}.
\]

Every odd start realizing the word satisfies \(T^m(n)<n\) exactly when
\(n>\theta\).

### 2.2 Floor-two is not necessary / floor-two는 필요조건이 아님

If every reverse suffix satisfies \(A_r\ge2r\), then

\[
\Phi\le\sum_{r=1}^m\frac{3^{r-1}}{4^r}
=1-\left(\frac34\right)^m
\]

and \(1-3^m/2^S\) is at least the same quantity. Hence
\(\theta\le1\). This proves that the TICKET-154 floor-two rule is sufficient.

It is not necessary. The actual odd orbit

\[
7\to11\to17\to13\to5
\]

has valuation word \((1,1,2,3)\). Its full suffix has sum \(7<8\), but

\[
C=73,\quad 2^S-3^m=47,\quad
\theta=\frac{73}{47}<7.
\]

따라서 정확한 하강 조건은 floor-two라는 조합적 외피가 아니라
\(n>\theta\)라는 가중 affine 조건이다.

### 2.3 Finite scan / 유한 스캔

The deterministic audit checks all 49,999 odd starts
\(3\le n\le100000\). Every start reaches a smaller odd value in the audited
run. Among the first-descent prefixes, 12,991, about 25.98%, fail the
floor-two sufficient condition. The maximum first-descent length in this
finite range is 85.

이 계산은 콜라츠 추측의 증명이 아니다. 검사 범위 밖의 시작값에 대해
아무것도 강제하지 않으며, 모든 자연수 valuation ray가 결국 자신의
정확한 \(\theta\)를 넘는 prefix에 도달한다는 전칭 정리가 남아 있다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### 3.1 One-sided signed certificate / 단측 부호 인증

Let \(F_k\) be the DFT of a zero-padded prime-only theta vector, with
\(L>2N\). For a conjugation-closed major set \(\mathcal M\), put

\[
z_k=\frac1L\operatorname{Re}
\left(F_k^2 e^{2\pi i kN/L}\right).
\]

Define

\[
M_N=\sum_{k\in\mathcal M}z_k,\qquad
P_N^+=\sum_{k\notin\mathcal M}\max(z_k,0),\qquad
N_N^-=\sum_{k\notin\mathcal M}\max(-z_k,0).
\]

The inverse DFT gives

\[
R_2(N)=M_N+P_N^+-N_N^-\ge M_N-N_N^-.
\]

Thus \(M_N>N_N^-\) is a sufficient certificate. In contrast, the
phase-blind budget

\[
A_N=\frac1L\sum_{k\notin\mathcal M}|F_k|^2
\]

also charges helpful positive mass and is generally much larger.

### 3.2 Finite result and second no-go / 유한 결과와 두 번째 no-go

The fixed audit uses Farey denominators \(q\le8\), two bins on each side,
and prime-only theta weights.

| \(N\) | \(M_N-N_N^-\) | \(M_N-A_N\) | unordered prime pairs |
|---:|---:|---:|---:|
| 1,000 | 736.73 | -1,294.48 | 28 |
| 2,000 | 648.42 | -4,125.31 | 37 |
| 4,000 | 922.22 | -10,600.07 | 65 |
| 8,000 | -203.89 | -27,067.24 | 106 |
| 16,000 | -2,594.88 | -64,479.37 | 191 |
| 32,000 | -13,858.44 | -151,123.27 | 312 |

The one-sided bound is strictly sharper at every row and certifies the first
three endpoints, while the phase-blind bound certifies none. However, the
same fixed mask fails from 8,000 onward even though representations exist.

이는 두 가지를 동시에 확정한다. 전체 minor 에너지를 손실로 세는 경로는
지나치게 강하다. 하지만 음의 위상 질량만 분리했다고 해서 고정된 작은
major mask가 자동으로 충분해지는 것도 아니다. 필요한 것은 endpoint에
따라 조정되는 major/minor 분해와 \(N_N^-\)의 균일한 산술적 상계다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### 4.1 Rare-event information inequality / 희귀사건 정보 부등식

Let \(D\) be a Bernoulli label, \(B\) a selected event,
\(\rho=P(B)>0\), \(d=P(D=1)\), and

\[
\delta=P(D=1\mid B)-d.
\]

The mutual-information decomposition is

\[
I(D;B)=
\rho\,D_{\mathrm{KL}}(P_{D\mid B}\|P_D)
+(1-\rho)\,D_{\mathrm{KL}}(P_{D\mid B^c}\|P_D).
\]

Pinsker's inequality in natural-log units yields

\[
I(D;B)\ge2\rho\delta^2,\qquad
|\delta|\le\sqrt{\frac{I(D;B)}{2\rho}}.
\]

Therefore \(I(D;B)=o(\rho)\) is sufficient for the conditional shift to
vanish. The unnormalized statement \(I(D;B)\to0\) is not sufficient.

### 4.2 Exact rare-event no-go / 정확 희귀사건 no-go

Use the TICKET-155 probability family with

\[
\rho=2^{-k},\quad P(D=1)=\frac25,\quad
P(D=1\mid B)=\frac35.
\]

Then \(\delta=1/5\) for every \(k\), while \(I(D;B)\to0\). However,

\[
\frac{I(D;B)}{\rho}
\longrightarrow
D_{\mathrm{KL}}\!\left(
\operatorname{Ber}\!\left(\frac35\right)
\middle\|
\operatorname{Ber}\!\left(\frac25\right)
\right)
\approx0.0810930216>0.
\]

즉 희귀한 rough-pair 선택에서는 정보량 자체가 0으로 가는지가 아니라,
그 정보량이 선택확률보다 더 빠르게 0으로 가는지가 핵심이다.

### 4.3 Arithmetic diagnostic / 산술 진단

The script evaluates the exact \(2\times2\) contingency tables for left and
right cubic-rough semiprime labels through \(X=10^7\). Every row satisfies
the Pinsker inequality. The observed normalized information is small but
nonmonotone at intermediate scales, and the \(10^7\) row cannot be promoted
to \(o(\rho)\).

이 수치는 다음 정리의 후보를 찾는 진단 데이터다. 유한한 작은 값이나
일시적 감소는 쌍둥이 소수 추측을 증명하지 않는다.

## 5. What changed / 무엇이 바뀌었나

TICKET-156 does not add another generic heuristic. It changes the four proof
obligations to quantities that match the actual logical loss:

1. RH: certify cutoff error separately from numerical precision.
2. Collatz: test the exact affine threshold, not a sufficient ballot rule.
3. Goldbach: bound harmful negative phase mass, not all minor energy.
4. Twin Prime: measure dependence relative to the rare selection mass.

TICKET-156은 “유한 계산이 잘 보인다”는 진술을 증명으로 승격하지 않는다.
각 계산이 어느 무한 보조정리를 요구하는지, 어떤 경로가 반례로
폐기되었는지, 그리고 어떤 유한 관찰이 아직 논리적 간극을 남기는지를
proof DAG에 분리한다.

## References / 참고문헌

- A. Groskin, *High-Precision Approximation of Riemann Zeros via the
  Truncated Weil Form*, 2026, <https://arxiv.org/abs/2605.20224>.
- A. Connes and C. Consani, *Weil positivity and Trace formula, the
  archimedean place*, <https://arxiv.org/abs/2006.13771>.
- T. Tao, *Almost all orbits of the Collatz map attain almost bounded
  values*, <https://arxiv.org/abs/1909.03562>.
- H. Helfgott, *The ternary Goldbach problem*,
  <https://arxiv.org/abs/1501.05438>.
- K. Ford and J. Maynard, *On the theory of prime producing sieves*,
  <https://arxiv.org/abs/2407.14368>.

These references delimit established context. None is cited as proving the
new open lemmas or any of the four conjectures.

위 문헌은 기존 학술 맥락과 알려진 장벽을 구분하기 위한 1차 자료다.
새 보조정리나 네 추측의 해결을 해당 문헌에 귀속하지 않는다.
