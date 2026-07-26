# TICKET-160: Exact Support, Natural Cylinders, Bilinear Phase, and Wheel Limits

## Abstract

TICKET-160 continues the four-conjecture program without claiming a solution.
It proves four exact reductions or no-go results and corrects one important
interpretation inherited from TICKET-159.

1. In the published finite Guinand-Weil dictionary, prime powers above the
   cutoff contribute exactly zero by Fourier support. The missing Riemann
   object is therefore not a decaying omitted-prime tail, but a certified
   transport from one common nested Weil core into cutoff-dependent Galerkin
   spaces. Raw spaces at different cutoffs have zero intersection.
2. Every finite accelerated-Collatz valuation word determines one exact odd
   residue cylinder. Contracting cylinders have cofinite descending natural
   tails. More sharply, an explicit infinite family has affine thresholds
   tending to infinity while every natural realizer still descends.
3. A Goldbach minor coefficient is an exact reflection bilinear form. A proxy
   defect factors before squaring and avoids an explicit dimension loss, but
   the Cauchy constant one is sharp on the ambient real-sequence class.
4. Fixed wheel residue features cannot uniformly distinguish twin primes from
   double composites by an exact CRT construction. On finite cubic-rough
   ranges, complete proper-factor separation occurs exactly at a measurable
   factor horizon, which approaches trial-division depth in the audited data.

Every proof DAG ends at `open_not_proven`. These are repository-level
syntheses and reductions. No external novelty or priority claim is made
without independent review.

## 초록

TICKET-160은 네 난제 중 어느 것도 해결됐다고 주장하지 않는다. 대신 네
문제에서 정확한 축소정리 또는 no-go 정리를 하나씩 확정하고, TICKET-159에서
이어진 중요한 해석 하나를 수정한다.

1. 공개된 유한 Guinand-Weil dictionary에서는 cutoff보다 큰 prime power가
   Fourier support 밖에 있으므로 기여가 정확히 0이다. 따라서 리만 가설의
   실제 병목은 감소하는 누락 소수 오차가 아니라, 하나의 공통 nested Weil
   core를 cutoff별 Galerkin 공간으로 옮기는 인증된 transport 정리다.
2. 모든 유한 Collatz valuation word는 정확히 하나의 홀수 residue cylinder를
   정한다. 수축 cylinder에서는 유한 개의 예외를 제외한 모든 자연수
   실현자가 하강한다. 더 나아가 threshold가 무한히 커지지만 모든 자연수
   실현자가 하강하는 명시적 무한 가족을 증명한다.
3. Goldbach minor coefficient를 reflection bilinear form으로 정확히 바꾸고,
   proxy 오차를 제곱하기 전에 인수분해한다. 그러나 일반 실수 수열 공간에서는
   Cauchy 상수 1이 최적이므로 산술 구조 없이 더 작은 상수는 얻을 수 없다.
4. 고정 wheel residue 특징은 CRT로 만든 double-composite 모방쌍 때문에
   twin pair를 균일하게 분리할 수 없다. 유한 cubic-rough 범위에서는 완전
   분리에 필요한 최소 인수 탐색 깊이를 정확한 factor horizon으로 계산한다.

모든 proof DAG는 `open_not_proven`에서 끝난다. 여기의 결과는 저장소 내부의
새로운 결합과 축소이며, 독립 검토 전에는 외부 학술적 최초성을 주장하지 않는다.

## 1. Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket160_exact_support_cylinder_bilinear_wheel.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket160_exact_support_cylinder_bilinear_wheel
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

Canonical machine-readable artifact:

`data/open-problem/ticket160-exact-support-cylinder-bilinear-wheel.json`

## 2. Riemann Hypothesis

### 2.1 Declared proposition

Fix \(c>1\), \(N\geq0\), and

\[
\Delta_c=\frac{\log c}{2\pi}.
\]

For the test function induced by a real even Galerkin vector \(v\), the finite
Guinand-Weil dictionary gives

\[
\operatorname{supp}\widehat g_{c,N,v}
\subseteq[-\Delta_c,\Delta_c].
\]

The omitted prime-power contribution is

\[
R_{c,N}(v)=
-\frac1\pi\sum_{q=p^k>c}
\frac{\Lambda(q)}{\sqrt q}\,
\widehat g_{c,N,v}
\left(\frac{\log q}{2\pi}\right).
\]

Then

\[
\boxed{R_{c,N}(v)=0}
\]

for every \(c,N,v\). If \(q=c\) is a prime power, the endpoint contribution is
also zero.

Let \(\mathcal F_{c,N}\) be the raw cutoff Galerkin function space: finite
trigonometric polynomials on the cutoff interval \(I_c\), embedded into
\(L^2(\mathbb R)\) by zero extension. If \(1<c_1<c_2\), then

\[
\boxed{
\mathcal F_{c_1,N_1}\cap\mathcal F_{c_2,N_2}=\{0\}.
}
\]

### 2.2 Proof

For every \(q>c\),

\[
\frac{\log q}{2\pi}>
\frac{\log c}{2\pi}=\Delta_c,
\]

so its Fourier weight is zero term by term. At \(q=c\), the induced Volterra
kernel is evaluated at zero and also vanishes.

For the cross-cutoff result, suppose \(f\) belongs to both raw spaces. In its
larger-interval representation, \(f\) is a finite trigonometric polynomial.
Its smaller-interval zero extension vanishes on a nonempty outer open interval.
A finite trigonometric polynomial is real analytic, so vanishing on an open
interval forces it to vanish identically.

### 2.3 What this corrects

TICKET-159's abstract diagonal-selector theorem remains valid. Its proposed
finite-dictionary instantiation treated a prime-band remainder \(A_{c,N}\) as a
quantity that still needed to decay. For the published support formula,

\[
A_{c,N}=0
\]

already. The real missing object is a common nested form core and a certified
transport into the mutually non-nested raw spaces.

### 2.4 Finite audit

| \(c\) | interior prime powers | boundary | outside through \(4c\) | maximum omitted weight |
|---:|---:|---:|---:|---:|
| 4 | 2 | 1 | 7 | 0 |
| 16 | 9 | 1 | 17 | 0 |
| 64 | 26 | 1 | 43 | 0 |
| 256 | 69 | 1 | 128 | 0 |

For the constant-vector \(N=0\) profile and \(c_1=4,c_2=16\),

\[
\frac{\widehat g_4(\Delta_4/2)}{\pi}=1,\qquad
\frac{\widehat g_{16}(\Delta_4/2)}{\pi}=\frac32,
\]

while

\[
\frac{\widehat g_4(3\Delta_4/2)}{\pi}=0,\qquad
\frac{\widehat g_{16}(3\Delta_4/2)}{\pi}=\frac12.
\]

This finite row validates the support calculation. It is not evidence for RH.

### 2.5 Rejected route and remaining gap

Discard:

- searching for a decaying omitted-prime tail in this exact dictionary;
- treating matrices at different \(c\) as nested compressions;
- applying min-max monotonicity across cutoffs without a transport theorem.

Limit:

The result supplies neither a common form core nor positive Weil margins and
does not exclude an off-critical zero.

Next lemma:

`EffectiveCommonNestedWeilCoreTransport`

Construct explicit \(V_1\subset V_2\subset\cdots\) dense in the Weil form norm
and computable maps

\[
J_m:V_m\longrightarrow\mathcal F_{c_m,N_m}
\]

whose uniform form-norm transport error tends effectively to zero.

## 3. Collatz Conjecture

### 3.1 Unique valuation cylinders

Let \(A\) be the accelerated odd map and let

\[
w=(a_1,\ldots,a_m),\qquad S(w)=\sum_{j=1}^m a_j.
\]

Then \(w\) is realized by exactly one odd residue class

\[
\boxed{
n\equiv r_w\pmod {2^{S(w)+1}}.
}
\]

Its natural density relative to odd integers is \(2^{-S(w)}\).

If

\[
D(w)=2^{S(w)}-3^m>0,
\]

then the exact affine iterate is

\[
A^m(n)=\frac{3^m n+C(w)}{2^{S(w)}},
\]

and therefore

\[
\boxed{
A^m(n)<n\iff D(w)n>C(w).
}
\]

All but finitely many positive members of the cylinder descend.

### 3.2 Cylinder proof

Assume a prefix with total valuation \(S\) determines one residue modulo
\(2^{S+1}\). Appending valuation \(a\) examines its \(2^a\) lifts modulo
\(2^{S+a+1}\). After applying the old prefix, those lifts differ by
\(2\cdot3^m\), an odd multiple of 2, and therefore run through every odd
residue modulo \(2^{a+1}\). Exactly one satisfies \(v_2(3y+1)=a\).

This closes the finite-word realizability question exactly.

### 3.3 Infinite front-loaded natural-transfer theorem

For every \(m\ge2\), define

\[
w_m=(m+1,\underbrace{1,\ldots,1}_{m-1}),\qquad S_m=2m.
\]

Its affine constant and denominator are

\[
C_m=(2^{m+1}+1)3^{m-1}-4^m,\qquad
D_m=4^m-3^m.
\]

The threshold is unbounded because

\[
\frac{C_m}{D_m}>
\frac23\left(\frac32\right)^m+
\frac13\left(\frac34\right)^m-1
\longrightarrow\infty.
\]

Nevertheless, every positive natural realizer has

\[
n=
\frac{2^{2m+1}t-2^{m+1}-1}{3},
\]

where \(t=1+3q\) for odd \(m\) and \(t=3+3q\) for even \(m\). Its endpoint is

\[
A^m(n)=2\cdot3^{m-1}t-1.
\]

Direct comparison gives

\[
A^m(n)<n
\iff
(4^m-3^m)t>2^m-1.
\]

Since

\[
4^m-3^m>4^{m-1}\ge2^m,
\]

every positive natural realizer descends.

This is an exact no-go against the implication

```text
unbounded abstract affine threshold
  -> natural realizer below that threshold
  -> possible non-descent obstruction
```

### 3.4 Finite audits

For all valuation words with \(a_j\le5\):

| length \(m\) | words | contracting words | uncovered odd-density lower bound |
|---:|---:|---:|---:|
| 2 | 25 | 22 | 0.5615 |
| 3 | 125 | 121 | 0.4034 |
| 4 | 625 | 610 | 0.4630 |
| 5 | 3,125 | 3,104 | 0.3733 |

The front-loaded identity was audited with arbitrary-precision integers through
selected depths ending at \(m=1024\). The threshold grows from approximately
1.57 at \(m=2\) to \(1.38\times10^{180}\) at \(m=1024\), while every exact
natural-transfer check passes.

Finite Kraft mass below one proves that those bounded prefix families do not
cover every odd start. It does not estimate the uncovered orbit behavior.

### 3.5 Remaining gap

Discard:

- treating finite word realizability as the remaining obstruction;
- interpreting a large abstract threshold as natural non-descent;
- promoting a finite cylinder cover with mass below one to all integers.

Next lemma:

`MinimalContractingFrontLoadedNaturalTransfer`

For

\[
S_m=\lceil m\log_2 3\rceil,\qquad b_m=S_m-m+1,
\]

prove for the least admissible natural parameter \(t_m\) that

\[
\boxed{
(2^{S_m}-3^m)t_m>2^{b_m-1}-1
}
\]

for every \(m\ge2\). This would close the minimally contracting front-loaded
family, not the full Collatz conjecture.

## 4. Strong Goldbach Conjecture

### 4.1 Declared proposition

Let \(G=\mathbb Z/L\mathbb Z\), \(S=-S\) a conjugation-closed minor-frequency
set, \(P_S\) its Fourier projection, and

\[
(R_Nh)(x)=h(N-x).
\]

For real \(f,g\), define

\[
E_S(N;f,g)=
\frac1L\sum_{k\in S}
\widehat f(k)\widehat g(k)e^{2\pi ikN/L}.
\]

Then

\[
\boxed{
E_S(N;f,g)=\langle P_Sf,R_NP_Sg\rangle.
}
\]

For every real proxy \(p\),

\[
\boxed{
E_S(N;f,f)-E_S(N;p,p)
=
\langle P_S(f-p),R_NP_S(f+p)\rangle
}
\]

and

\[
\boxed{
|E_S(N;f,f)-E_S(N;p,p)|
\le
\|P_S(f-p)\|_2\|P_S(f+p)\|_2.
}
\]

### 4.2 Proof and improvement over TICKET-159

Fourier inversion proves the first identity. The reflection is a self-adjoint
unitary involution and commutes with a symmetric frequency projection. Expanding
the difference of quadratic forms cancels the cross terms; Cauchy-Schwarz proves
the bound.

TICKET-159 retained only unsigned energy after squaring. TICKET-160 moves the
proxy comparison before the bilinear operation. This removes an explicit
\(\sqrt{|S|}\) loss from the abstract defect estimate.

### 4.3 Sharp ambient no-go

If \(S\) contains \(\{k,-k\}\), define normalized centered functions

\[
f_+(x)=\sqrt{\frac2L}
\cos\left(\frac{2\pi k(x-N/2)}L\right),
\]

\[
f_-(x)=\sqrt{\frac2L}
\sin\left(\frac{2\pi k(x-N/2)}L\right).
\]

They satisfy

\[
R_Nf_+=f_+,\qquad R_Nf_-=-f_-,
\]

and therefore

\[
E_S(N;f_+,f_+)=1,\qquad E_S(N;f_-,f_-)=-1.
\]

With \(p=0\), the Cauchy bound is saturated. No universal constant \(c<1\)
can replace 1 over all real sequences.

These signed trigonometric functions are not prime DFTs and are not Goldbach
counterexamples. The no-go applies only to ambient Hilbert-space geometry.

### 4.4 Finite audit

| \(L\) | \(N\) | \(k\) | positive form | negative form | off-pair DFT leakage |
|---:|---:|---:|---:|---:|---:|
| 11 | 4 | 1 | 1 | -1 | \(2.8\times10^{-15}\) |
| 12 | 7 | 2 | 1 | -1 | \(6.6\times10^{-15}\) |
| 17 | 10 | 3 | 1 | -1 | \(7.6\times10^{-15}\) |
| 32 | 18 | 5 | 1 | -1 | \(1.1\times10^{-14}\) |

Four additional deterministic finite-vector rows validate the projection,
factorization, and Cauchy inequalities.

### 4.5 Remaining gap

Discard:

- expecting phase-sensitive Hilbert geometry alone to supply a uniform
  constant below one.

Next lemma:

`PrimeRestrictedMinorProxyDefectBelowExplicitSingularSeriesMargin`

Construct effective \(S_N\), arithmetic proxies \(p_N\), and a rigorous major
lower bound \(M_{\mathrm{low}}(N)\) such that

\[
\|P_{S_N}(\theta_N-p_N)\|_2
\|P_{S_N}(\theta_N+p_N)\|_2
-E_{S_N}(N;p_N,p_N)
<M_{\mathrm{low}}(N)
\]

for every sufficiently large even \(N\). This remains open.

## 5. Twin Prime Conjecture

### 5.1 Fixed-wheel CRT no-go

Let \(M\ge1\) and let \((p,p+2)\) be a twin pair with
\(\gcd(p(p+2),M)=1\). Choose distinct primes \(q,r\nmid M\). CRT gives
infinitely many \(n\) satisfying

\[
n\equiv p\pmod M,\qquad
n\equiv0\pmod q,\qquad
n\equiv-2\pmod r.
\]

Taking a sufficiently large representative makes \(n\) and \(n+2\) proper
composites while

\[
n\bmod M=p\bmod M.
\]

Thus no function of one fixed wheel residue can classify all twin pairs and
all double-composite pairs correctly.

At \(z=31\),

- \(M=200560490130\);
- the twin witness is \((41,43)\);
- the CRT composite witness is
  \((448252695440591,448252695440593)\);
- both starts are \(41\bmod M\).

### 5.2 Exact finite factor horizon

Let

\[
z=\lfloor X^{1/3}\rfloor
\]

and retain pairs for which both endpoints have least prime factor above \(z\).
Cubic roughness makes every retained endpoint either prime or semiprime.

For \(z\le y\le\sqrt X\), let \(\Phi_{X,y}\) record proper prime divisors
\(z<p\le y\) of the two endpoints. Define

\[
\tau_X=
\max_{\substack{n,n+2\text{ both composite}\\
P^-(n),P^-(n+2)>z}}
\min(P^-(n),P^-(n+2)).
\]

Then

\[
\boxed{
\Phi_{X,y}\text{ separates every PP from every QQ}
\iff y\ge\tau_X.
}
\]

Every PP has the zero proper-factor vector. A QQ also has the zero vector
exactly when both least factors exceed \(y\). The stated maximum is therefore
the exact necessary and sufficient horizon.

### 5.3 Finite audit

| \(X\) | \(z\) | PP | QQ | \(\tau_X\) | \(\tau_X/\sqrt X\) |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 10 | 33 | 4 | 17 | 0.538 |
| 10,000 | 21 | 201 | 35 | 71 | 0.710 |
| 100,000 | 46 | 1,218 | 284 | 251 | 0.794 |
| 1,000,000 | 100 | 8,161 | 2,453 | 811 | 0.811 |
| 10,000,000 | 215 | 58,965 | 19,074 | 3,037 | 0.960 |

At \(X=10^7\), the critical collision is

\[
9770027=3083\cdot3169,\qquad
9770029=3037\cdot3217.
\]

For \(y<3037\), this QQ and a PP both have the zero feature. At \(y=3037\),
all audited QQ pairs become visible.

The increasing ratios are finite observations only. No convergence of
\(\tau_X/\sqrt X\) is proved.

### 5.4 Rejected route and remaining gap

Discard:

- fixed wheel residues and all characters factoring through one fixed
  modulus as uniform classifiers;
- calling unrestricted proper-factor search a parity-breaking feature.

Searching to \(\sqrt X\) separates primes from composites because it performs
trial division. It is not a prime-producing lower-bound theorem.

Next lemma:

`IndependentCubicRoughBilinearIncidenceDeficit`

Prove from independent Type I/II estimates, without consulting PP/QQ labels or
complete factorization, that the cubic-rough least-factor incidence is below
the rough-pair mass by a fixed positive proportion on infinitely many scales.
That would convert the exact identity from TICKET-154 into a positive PP
excess. It remains open.

## 6. Literature boundary / 문헌 경계

- [Groskin, finite Guinand-Weil dictionary and exact support
  formula](https://arxiv.org/abs/2607.02828) supplies the primary support
  identity. TICKET-160 does not claim the paper's theorem as a new result.
- [Suzuki, Weil's quadratic form via the screw
  function](https://arxiv.org/abs/2606.09096) supplies continuous Weil-form
  context. The common nested transport lemma is not imported from it.
- [Bernstein and Lagarias, The 3x+1 Conjugacy
  Map](https://doi.org/10.4153/CJM-1996-060-x) is primary background for
  finite parity coding and 2-adic conjugacy.
- [Tao, Almost all Collatz orbits attain almost bounded
  values](https://arxiv.org/abs/1909.03562) is an almost-all theorem, not the
  universal natural-transfer statement.
- [Helfgott, Minor arcs for Goldbach's
  problem](https://arxiv.org/abs/1205.5252) supplies explicit large-sieve and
  bilinear context for ternary Goldbach. It does not imply the binary lemma.
- [Ford and Maynard, On the theory of prime producing
  sieves](https://arxiv.org/abs/2407.14368) explains why substantial Type II
  information is necessary for nontrivial prime lower bounds.

## 7. Proof DAG summary / 증명 DAG 요약

### Riemann

```text
misidentified: decaying prime tail + raw nested cutoff spaces
  -> proved: exact prime support closure + cross-cutoff nesting no-go
  -> open: EffectiveCommonNestedWeilCoreTransport
```

### Collatz

```text
refuted: unbounded abstract threshold implies natural non-descent
  -> proved: unique cylinders + front-loaded natural transfer
  -> open: MinimalContractingFrontLoadedNaturalTransfer
```

### Goldbach

```text
refuted: ambient bilinear geometry gives a saving below one
  -> proved: bilinear proxy identity + sharp reflection no-go
  -> open: PrimeRestrictedMinorProxyDefectBelowExplicitSingularSeriesMargin
```

### Twin Prime

```text
refuted: fixed wheel or unrestricted factor feature breaks parity
  -> proved: fixed-wheel CRT blindness + exact factor horizon
  -> open: IndependentCubicRoughBilinearIncidenceDeficit
```

## 8. Final claim boundary / 최종 주장 경계

TICKET-160 establishes:

- four exact theorem or no-go packages;
- four explicit discarded routes;
- four single next lemmas;
- exact integer, rational, Fourier, CRT, and finite-factor audits;
- zero machine failures.

It does not establish:

- the Riemann hypothesis or an off-critical zero;
- universal Collatz descent or a divergent orbit;
- strong Goldbach or an even counterexample;
- infinitely many twin primes or a terminal obstruction.

The four conjecture-resolution counter remains exactly zero.
