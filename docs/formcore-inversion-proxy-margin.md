# TICKET-157: Form Cores, Inversion Gain, Phase Proxies, and Information Margins

## Claim boundary / 주장 경계

This report does **not** prove or disprove the Riemann hypothesis, Collatz
conjecture, strong Goldbach conjecture, or Twin Prime conjecture. It proves
four exact reductions or no-go statements and reports bounded computations.
Every target conjecture remains `open_not_proven`.

이 보고서는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 증명하거나 반증하지 않는다. 네 개의 정확한 환원 또는
불가능성 결과와 유한 계산을 제시한다. 네 추측은 모두
`open_not_proven`, 즉 미해결 상태다.

| Problem / 문제 | New exact result / 새 정확 결과 | Discarded route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| Riemann / 리만 | Positivity on every member of a nested form core plus one uniform cutoff-form error promotes to the full closed form / nested form core 전체와 하나의 균일 cutoff-form 오차가 있으면 닫힌 form 전체로 양성을 승격 | Treat a finite Galerkin sweep as a continuum certificate, or demand a separate basis operator-norm error when a genuine form core exists / 유한 Galerkin sweep 승격, genuine form core가 있는데도 별도 basis operator-norm 오차를 필수화 | `UniformArchimedeanTailFormBoundOnNestedExplicitWeilCore` |
| Collatz / 콜라츠 | The exact benefit of natural valuation order is a telescoping adjacent-swap inversion gain / 자연 valuation 순서의 이득은 인접 교환 이득의 정확한 망원합 | Require every realized multiset to descend even in its descending worst order / 모든 valuation multiset이 최악의 내림차순 순서에서도 하강해야 한다고 요구 | `NaturalValuationInversionGainDominatesWorstOrderThresholdExcess` |
| Goldbach / 골드바흐 | Negative phase mass is one-Lipschitz in complex \(L^1\); an \(L^2\)-only proxy necessarily pays a sharp \(\sqrt m\) dimension factor / 음의 위상 질량은 복소 \(L^1\)에서 1-Lipschitz이고 \(L^2\)만 쓰면 정확히 \(\sqrt m\) 차원손실이 필요 | Suppress the dimension factor or promote target-fitted block means to analytic major-arc models / 차원손실 무시, target-fitted block mean을 해석적 major-arc 모형으로 승격 | `ArithmeticBinaryGoldbachPhaseProxyWithUniformL1ResidualAndFiniteJoin` |
| Twin Prime / 쌍둥이 소수 | The normalized information budget can be compared directly with the ambient semiprime margin; \(I=o(\rho)\) is sufficient but not necessary / 정규화 정보량 예산을 ambient semiprime margin과 직접 비교하며 \(I=o(\rho)\)는 충분하지만 필요하지 않음 | Require little-o as a necessary target or report \(I/\rho\) without comparing it with the target margin / little-o를 필요조건으로 요구하거나 target margin 비교 없이 \(I/\rho\)만 보고 | `UniformCubicRoughInformationBudgetBelowSemiprimeMarginAfterEffectiveCutoff` |

Machine-readable source / 기계 판독 원본:
[`ticket157-formcore-inversion-proxy-margin.json`](../data/open-problem/ticket157-formcore-inversion-proxy-margin.json).

```text
python scripts/ticket157_formcore_inversion_proxy_margin.py
python -m unittest tests.test_ticket157_formcore_inversion_proxy_margin -v
```

## 1. Riemann hypothesis / 리만 가설

### 1.1 Declared proposition / 선언 명제

Let \(q\) be a closed semibounded quadratic form on a Hilbert space \(H\).
Suppose

\[
V_1\subset V_2\subset\cdots
\]

and \(\bigcup_N V_N\) is a form core for \(q\). Let \(q_T\) be defined on
that union and suppose

\[
|q_T(f)-q(f)|\le \varepsilon_T\|f\|^2
\quad(f\in\bigcup_N V_N).
\]

If

\[
\inf_{\substack{f\in V_N\\\|f\|=1}}q_T(f)\ge\varepsilon_T
\quad\text{for every }N,
\]

then \(q(f)\ge0\) on the full form domain.

한국어로는 basis cutoff마다 별도의 operator-norm 오차를 계산하지
않아도 되는 경우를 정확히 분리한다. \(V_N\)들이 nested이고 그 합집합이
실제 form core이며, cutoff 오차가 그 합집합 전체에서 균일하게
통제된다면 모든 \(N\)의 finite positivity를 닫힌 form 전체로 옮길 수
있다.

### 1.2 Proof / 증명

For every \(f\) in the form-core union,

\[
q(f)\ge q_T(f)-\varepsilon_T\|f\|^2\ge0.
\]

A closed semibounded form is continuous in its form norm. Form-core density
therefore extends this inequality to every \(f\) in the form domain.
Nestedness also implies that the finite Rayleigh minima are nonincreasing
with \(N\).

이 증명은 TICKET-156의 세 오차 중 basis/core 축을 무조건
operator-norm으로 처리할 필요가 없음을 보인다. 단, **모든 \(N\)** 과
form-core 합집합 전체에서 유효한 **균일한**
\(\varepsilon_T\)가 필요하다.

### 1.3 Finite-sweep no-go / 유한 sweep 불가능성

For any checked ceiling \(N_{\max}\), consider

\[
A=\operatorname{diag}(1,\ldots,1,-1)
\]

on \(\mathbb R^{N_{\max}+1}\). Every coordinate core of dimension at most
\(N_{\max}\) has minimum eigenvalue \(+1\), while the full operator has
minimum \(-1\). The script records this exact construction for
\(N_{\max}=4,8,16,32\).

따라서 finite Galerkin sweep의 길이나 정밀도만 늘리는 방식은
continuum positivity를 증명하지 못한다. 이 반례는 실제 Weil
연산자가 아니라, 해당 논리적 승격 규칙 자체를 반박한다.

### 1.4 Remaining gap / 남은 간극

PrimeProject has not supplied:

1. the actual nested test-function core for the Weil form;
2. a proof that it is a form core in the required topology;
3. a uniform archimedean tail-form estimate valid on its entire union.

PrimeProject는 실제 Weil form의 nested core, form-core 밀도, 그 합집합
전체에서 유효한 archimedean tail 오차를 아직 증명하지 않았다.

**Next lemma / 다음 보조정리**

`UniformArchimedeanTailFormBoundOnNestedExplicitWeilCore`

## 2. Collatz conjecture / 콜라츠 추측

### 2.1 Declared proposition / 선언 명제

For an accelerated odd Collatz valuation word

\[
w=(a_1,\ldots,a_m),\qquad S=\sum_{j=1}^m a_j,
\]

write

\[
T_w(n)=\frac{3^m n+C(w)}{2^S},
\qquad
C(w)=\sum_{j=1}^m3^{m-j}2^{a_1+\cdots+a_{j-1}}.
\]

Assume \(D=2^S-3^m>0\). Let \(w^\downarrow\) be the same valuations sorted
in nonincreasing order and put

\[
G(w)=C(w^\downarrow)-C(w).
\]

Then

\[
G(w)\ge0,\qquad
\theta(w)=\frac{C(w)}D
=\frac{C(w^\downarrow)}D-\frac{G(w)}D.
\]

A realizing start \(n\) descends after this prefix exactly when

\[
G(w)>C(w^\downarrow)-nD.
\]

### 2.2 Adjacent-swap proof / 인접 교환 증명

Suppose adjacent valuations \(x<y\) occur at positions \(i,i+1\). Swapping
them increases the final affine constant by

\[
3^{m-i-1}
\cdot 2^{a_1+\cdots+a_{i-1}}
(2^y-2^x),
\]

when positions are numbered from one. In zero-based code this is
\(3^{m-i-2}2^{\text{prefix}}(2^y-2^x)\). All other additive terms are
unchanged. Bubble sorting telescopes these positive gains to \(G(w)\).

한국어로는 큰 valuation을 앞쪽으로 옮길수록 affine 상수와 하강
임계값이 커진다. 실제 자연수 궤도의 valuation 순서가 최악의
내림차순보다 얼마나 유리한지를 \(G(w)\)가 정확히 측정한다.

### 2.3 Reproducible computation / 재현 계산

The odd starts \(3\le n\le100000\) give 49,999 first-descent prefixes.

| Result / 결과 | Count / 개수 |
|---|---:|
| Worst-order multiset threshold already below \(n\) / 최악 순서도 이미 하강 | 49,733 |
| Natural order inversion gain required / 실제 순서 이득이 필요 | 266 |
| Maximum first-descent length / 최대 첫 하강 길이 | 85 |

The first inversion-essential start is \(n=27\). Its actual threshold is
about \(8.7253\), but the descending-rearrangement threshold is about
\(66{,}806.78\). The exact inversion gain bridges this difference.

첫 사례 \(n=27\)은 multiset 자체만으로는 매우 나쁜 최악 임계값을
갖지만, 자연 궤도에서 발생한 valuation 순서가 그 손실을 정확히
상쇄한다. 이는 순서를 버린 worst-case multiset 조건이 필요조건이
아님을 보여준다.

### 2.4 Remaining gap / 남은 간극

The theorem exactly rewrites descent for a selected prefix. It does not
prove that every natural valuation ray eventually accumulates enough
inversion gain.

이 정리는 이미 선택한 prefix의 하강을 정확히 다시 표현한다. 모든
자연수 valuation ray가 언젠가 필요한 inversion gain을 얻는다는 전칭
명제는 아직 없다. 100,000까지의 계산은 전칭 증명이 아니다.

**Next lemma / 다음 보조정리**

`NaturalValuationInversionGainDominatesWorstOrderThresholdExcess`

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### 3.1 Declared proposition / 선언 명제

For complex minor-arc terms \(w_k\), define

\[
N_-(w)=\sum_k\max(-\Re w_k,0).
\]

For any proxy \(v_k\),

\[
N_-(w)\le N_-(v)+\sum_k|w_k-v_k|.
\]

The negative-part map on the real line is one-Lipschitz, and
\(|\Re(w_k-v_k)|\le|w_k-v_k|\), so the result follows term by term.

한국어로는 TICKET-156에서 분리한 해로운 음의 위상 질량을 직접
추정하는 대신, 해석적으로 계산 가능한 phase proxy와 실제 항 사이의
복소 \(L^1\) 오차를 제어하면 충분하다는 정확한 환원이다.

### 3.2 Sharp \(L^2\) no-go / 정확한 \(L^2\) 불가능성

If only

\[
\|w-v\|_2\le E
\]

is known on \(m\) coordinates, Cauchy-Schwarz gives

\[
N_-(w)\le N_-(v)+\sqrt m\,E.
\]

The factor \(\sqrt m\) cannot be removed in general. Take \(v=0\) and

\[
w_k=-\frac1{\sqrt m}
\quad(1\le k\le m).
\]

Then \(\|w\|_2=1\) and \(N_-(w)=\sqrt m\). The machine audit uses
\(m=4,16,64,256\), so every value is an exact rational number.

따라서 `L2 residual is small`이라는 문장만으로 차원에 독립적인
binary Goldbach 하한을 만들 수 없다. 위상 또는 산술 구조를 이용한
\(L^1\) 절약이 필요하다.

### 3.3 Block-proxy falsification / block proxy 반증

The script partitions the finite minor vectors into blocks of
8, 32, and 128 bins, replaces each block by its complex mean, and applies
the exact \(L^1\) stability bound at
\(N=1000,2000,\ldots,32000\).

All 18 target-fitted block-proxy certificates fail. These block means use
the target transform itself, so even a pass would be only a compression
diagnostic, not an a priori arithmetic theorem.

스크립트의 block mean은 target 데이터를 본 뒤 계산된다. 따라서
analytic major-arc proxy가 아니며, 실제 결과도 18개 조합 모두
실패한다. 이 경로는 폐기한다.

### 3.4 Remaining gap / 남은 간극

What remains is an arithmetic proxy fixed before seeing the target
transform, together with a uniform \(L^1\) residual estimate and an
effective finite join.

필요한 것은 target transform을 보기 전에 정해지는 산술적 phase
proxy, 균일한 복소 \(L^1\) 잔차 상계, 그리고 유한 검증과 무한 구간을
연결하는 effective cutoff다.

**Next lemma / 다음 보조정리**

`ArithmeticBinaryGoldbachPhaseProxyWithUniformL1ResidualAndFiniteJoin`

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### 4.1 Declared proposition / 선언 명제

Let \(d_L,d_R\) be the ambient semiprime fractions in the left and right
cubic-rough populations. Let \(\rho_L,\rho_R\) be the probabilities of
the shifted rough-partner selections and \(I_L,I_R\) the corresponding
mutual informations with the semiprime labels.

Combining the exact TICKET-155 transfer identity with TICKET-156 Pinsker
bounds gives

\[
\frac MR
\le d_L+d_R
 \sqrt{\frac{I_L}{2\rho_L}}
 \sqrt{\frac{I_R}{2\rho_R}}.
\]

Thus, with

\[
\eta=1-d_L-d_R,
\]

the sufficient target is

\[
\sqrt{\frac{I_L}{2\rho_L}}
+\sqrt{\frac{I_R}{2\rho_R}}<\eta.
\]

### 4.2 Proof / 증명

TICKET-155 proved

\[
\frac MR=d_L+d_R+\delta_L+\delta_R.
\]

TICKET-156 proved

\[
|\delta_j|\le\sqrt{\frac{I_j}{2\rho_j}}.
\]

Adding the two one-sided upper bounds proves the displayed information
budget certificate.

이 결과는 `normalized information이 작다`를 보고하는 데서 멈추지
않고, 실제 필요한 ambient semiprime margin과 같은 단위로 비교한다.

### 4.3 Finite certificates / 유한 인증

| \(X\) | Information upper bound for \(M/R\) / 정보 상계 | Certified slack / 인증 여유 |
|---:|---:|---:|
| 1,000 | 0.650475 | 0.349525 |
| 10,000 | 0.578384 | 0.421616 |
| 100,000 | 0.666735 | 0.333265 |
| 1,000,000 | 0.704738 | 0.295262 |
| 10,000,000 | 0.721825 | 0.278175 |

All five finite rows certify \(M/R<1\) using the information bound rather
than the observed conditional ratio alone. They do not establish a
uniform theorem for all \(X\).

다섯 유한 규모는 모두 정보량 상계만으로 \(M/R<1\)을 인증한다. 그러나
이 결과는 \(X\le10^7\)의 유한 자료이며 모든 \(X\)에 대한 정리가 아니다.

### 4.4 Little-o necessity no-go / little-o 필요성 반증

For each \(k\), take a rare selection with \(\rho=2^{-k}\), ambient
semiprime fraction \(2/5\), and selected conditional fraction \(1/5\) on
each side. Then the actual two-side conditional sum is \(2/5<1\), but

\[
\frac{I}{\rho}
\longrightarrow
D_{\mathrm{KL}}\!\left(
\operatorname{Ber}(1/5)\,\|\,\operatorname{Ber}(2/5)
\right)>0.
\]

Therefore \(I=o(\rho)\) is sufficient but not necessary. Pinsker can also
be too loose: its two-side upper bound exceeds one in this family even
though the target ratio is \(2/5\).

따라서 TICKET-156의 little-o 표적은 안전한 충분조건이지만
필요조건은 아니다. 다음 정리는 정보량을 0으로 보내는 것보다 직접적인
margin separation을 목표로 해야 한다.

**Next lemma / 다음 보조정리**

`UniformCubicRoughInformationBudgetBelowSemiprimeMarginAfterEffectiveCutoff`

## 5. Literature boundary / 문헌 경계

These primary sources define context; none supplies the missing lemmas.

다음 1차 문헌은 연구 맥락을 정할 뿐, 남은 보조정리를 대신하지 않는다.

1. Alain Connes and Caterina Consani,
   [Weil positivity and Trace formula, the archimedean place](https://arxiv.org/abs/2006.13771).
2. Akiva Groskin,
   [High-Precision Approximation of Riemann Zeros via the Truncated Weil Form](https://arxiv.org/abs/2605.20224).
3. Terence Tao,
   [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562).
4. Tong Niu,
   [Parity vectors and paradoxical sequences in the accelerated Collatz map](https://arxiv.org/abs/2605.13886).
5. Harald Helfgott,
   [Minor arcs for Goldbach's problem](https://arxiv.org/abs/1205.5252).
6. Kevin Ford and James Maynard,
   [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).

The 2026 Riemann and Collatz preprints are used only as current
computational or valuation-vector context. Their finite observations are
not imported as proofs.

2026년 리만·콜라츠 preprint는 최신 계산 및 valuation-vector 맥락으로만
사용한다. 해당 문헌의 유한 관측이나 추측적 진술을 증명으로 가져오지
않는다.

## 6. Research decision / 연구 결정

TICKET-157 does not add a larger finite search and call it progress. It
changes the mathematical targets:

1. RH now needs one actual uniform tail-form estimate on a nested Weil core.
2. Collatz now needs a lower bound on natural valuation-order inversion gain.
3. Goldbach now needs an arithmetic phase proxy with a uniform \(L^1\)
   residual, not a dimension-blind \(L^2\) estimate.
4. Twin Prime now needs an information budget below the actual semiprime
   margin, not the unnecessarily strong requirement \(I=o(\rho)\).

TICKET-157은 계산 범위만 확장하지 않는다. RH는 실제 Weil core의 균일
tail-form bound, Collatz는 자연 valuation 순서의 inversion gain 하한,
Goldbach는 산술 phase proxy의 균일 \(L^1\) 잔차, Twin Prime은 실제
semiprime margin보다 작은 정보량 예산으로 표적을 좁힌다. 이 네
보조정리는 아직 모두 미해결이다.
