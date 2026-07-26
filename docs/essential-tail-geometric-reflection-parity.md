# TICKET-153: Essential Tail, Geometric Cylinders, Reflection Energy, and Cubic-Rough Parity

Continued by / 다음 연구:
[TICKET-154 compact-suffix-wheel-leastfactor](compact-suffix-wheel-leastfactor.md).

## Claim boundary / 주장 경계

This document does **not** prove or disprove the Riemann hypothesis, the
Collatz conjecture, the strong Goldbach conjecture, or the Twin Prime
conjecture. It proves four exact intermediate or no-go theorems, reports
bounded computations, and identifies one open lemma per problem.

이 문서는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 증명하거나 반증하지 않는다. 네 개의 정확한 부분정리 또는
불가능성 정리(no-go theorem)를 증명하고, 유한 계산 결과와 문제별
다음 단일 미증명 보조정리를 구분해서 기록한다.

| Problem / 문제 | Exact TICKET-153 result / 정확한 새 결과 | Rejected route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| Riemann / 리만 | Positive essential tail Schur certificate and finite-rank norm no-go / 양의 essential tail Schur 인증과 유한랭크 노름근사 불가능성 | Approximate the whole positive essential tail by finite rank in small norm / 양의 essential tail 전체를 작은 노름의 유한랭크로 근사 | `ActualWeilPositiveTailDecompositionWithCertifiedSchurComplement` |
| Collatz / 콜라츠 | Exact countable geometric child law and negative mean log multiplier / 정확한 가산 기하분포 자식 법칙과 음의 평균 로그 계수 | Promote negative average or density-one behavior to every natural number / 음의 평균 또는 밀도 1 결과를 모든 자연수 명제로 승격 | `UniformAffineOffsetControlOnNaturalValuationRays` |
| Goldbach / 골드바흐 | Prime-theta reflection energy identity and symmetric-baseline no-go / 소수 theta 반사 에너지 항등식과 대칭 기준선 불가능성 | Remove the antisymmetric sector by changing a symmetric baseline / 대칭 기준선 변경으로 반대칭 성분 제거 | `ExplicitBinaryPrimeThetaMinorArcBoundBelowMajorArcReflectionGap` |
| Twin Prime / 쌍둥이 소수 | Cubic-rough Liouville sum equals `2(QQ-PP)` / cubic-rough Liouville 합은 정확히 `2(QQ-PP)` | Treat finite negative sums as an infinite theorem / 유한 음수 합을 무한 정리로 간주 | `UnboundedCubicRoughPrimePrimeExcessOverSemiprimePairs` |

The machine-readable record is
[`ticket153-essential-tail-geometric-reflection-parity.json`](../data/open-problem/ticket153-essential-tail-geometric-reflection-parity.json).

기계 판독 원본은 위 JSON이며, 모든 수치와 proof DAG는 이 파일에서
직접 재생성된다.

```text
python scripts/ticket153_essential_tail_geometric_reflection_parity.py
python -m unittest tests.test_ticket153_essential_tail_geometric_reflection_parity -v
```

## 1. Riemann hypothesis / 리만 가설

### 1.1 Declared proposition / 선언 명제

Let \(H=H_0\oplus H_1\), and let a bounded self-adjoint operator have block
form

\[
G=
\begin{pmatrix}
A&C^*\\
C&D
\end{pmatrix}.
\]

Assume \(D\ge\delta I\) for some \(\delta>0\). Then

\[
A\ge \frac{\lVert C\rVert^2}{\delta}I
\quad\Longrightarrow\quad
G\ge0.
\]

When \(D\) is invertible, the exact criterion is

\[
G\ge0
\quad\Longleftrightarrow\quad
D\ge0
\ \text{and}\
A-C^*D^{-1}C\ge0.
\]

On an infinite-dimensional Hilbert space, every finite-rank \(F\) satisfies

\[
\lVert \delta I-F\rVert\ge\delta.
\]

따라서 양의 무한차원 tail이 존재한다면 그 tail 자체를 작은
operator norm의 유한랭크 오차로 취급할 수 없다. 양의 tail은 그대로
남겨 두고, 유한 core와 tail 사이의 결합 \(C\)를 Schur complement로
통제해야 한다.

### 1.2 Proof / 증명

Completing the square gives

\[
\begin{aligned}
\langle G(x,y),(x,y)\rangle
={}&
\langle(A-C^*D^{-1}C)x,x\rangle\\
&+\langle D(y+D^{-1}Cx),y+D^{-1}Cx\rangle.
\end{aligned}
\]

Since \(D^{-1}\le\delta^{-1}I\),

\[
C^*D^{-1}C\le\frac{\lVert C\rVert^2}{\delta}I.
\]

This proves the sufficient condition and the exact Schur criterion.

For the norm no-go, \(\ker F\) contains a unit vector because \(F\) has
finite rank while the space is infinite-dimensional. On that vector,

\[
\lVert(\delta I-F)x\rVert=\delta.
\]

한국어로는 첫 식이 핵심이다. 무한 tail의 양성은 \(D\)가 담당하고,
core에서 지불해야 할 정확한 결합 비용은 \(C^*D^{-1}C\)다. 유한랭크
\(F\)의 kernel 방향에서는 양의 identity tail이 전혀 상쇄되지
않으므로, 그 tail을 통째로 작은 norm remainder라고 부르는 경로는
원리적으로 실패한다.

### 1.3 Reproducible certificate / 재현 인증서

The audit checks five essential-norm witnesses and eight exact rational
Schur margins. Four pass and four fail. In every failed row, the vector

\[
y=-D^{-1}Cx
\]

has quadratic value

\[
\left(A-\frac{\lVert C\rVert^2}{\delta}\right)\lVert x\rVert^2<0.
\]

감사 데이터에는 essential-tail 거리 하계 5개와 정확 유리수 Schur
margin 8개가 포함된다. 실패 행은 단순한 수치 오차가 아니라 위
명시적 벡터가 만드는 음의 방향을 함께 저장한다.

### 1.4 No-go, limit, and next lemma / 폐기 경로, 한계, 다음 보조정리

**Rejected route.** Approximate a nonzero positive essential tail itself by
finite-rank operators with norm error tending to zero.

**폐기 경로.** 0이 아닌 양의 essential tail 전체를 operator norm에서
유한랭크로 0까지 근사하는 전략.

**Remaining gap.** PrimeProject has not constructed the actual Weil form
block \(A,C,D\), proved \(D\ge\delta I\), or bounded \(C^*D^{-1}C\).
The theorem is functional analysis for a future decomposition, not a
positivity proof for the zeta explicit formula.

**남은 간극.** 실제 Weil 형식에서 \(A,C,D\)를 구성하고, tail
coercivity와 coupling bound를 증명해야 한다. 현재 결과는
off-critical zero를 하나도 배제하지 않는다.

**Next lemma / 다음 보조정리**

`ActualWeilPositiveTailDecompositionWithCertifiedSchurComplement`

## 2. Collatz conjecture / 콜라츠 추측

### 2.1 Declared proposition / 선언 명제

For the accelerated odd map

\[
T(n)=\frac{3n+1}{2^{v_2(3n+1)}},
\]

fix any finite valuation word. Its cylinder is the disjoint countable union
of children indexed by the next valuation \(b\ge1\). Relative to the parent
cylinder,

\[
\Pr(a_{m+1}=b)=2^{-b},
\qquad
\Pr(a_{m+1}>B)=2^{-B}.
\]

Consequently a word \(a_1,\ldots,a_m\) has normalized cylinder mass

\[
\Pr(a_1,\ldots,a_m)=2^{-\sum_{j=1}^{m}a_j}.
\]

The cylinder coordinates therefore have the exact geometric finite-word
law. In particular,

\[
\mathbb E[a_j]=2,
\qquad
\mathbb E\log\left(\frac3{2^{a_j}}\right)
=\log3-2\log2
=\log\frac34<0.
\]

한국어로 말하면, TICKET-152에서 남아 있던 `countable extension +
uniform valuation tail` 부분은 정확히 닫힌다. 다음 valuation은
조건부로 \(2^{-b}\)이고, cap \(B\) 밖의 전체 질량은 정확히
\(2^{-B}\)다.

### 2.2 Proof of the cylinder law / cylinder 법칙의 증명

Fix a parent word and write its odd starts as \(n=n_0+2^Lk\). After
executing the parent word, the next odd numerator divided by two is an
affine function of \(k\) whose linear coefficient is odd. It is therefore
a permutation modulo \(2^B\). Among the \(2^B\) lift indices, exactly
\(2^{B-b}\) have next valuation \(b\) for \(1\le b\le B\), and exactly one
has valuation greater than \(B\). Dividing by \(2^B\), then letting \(B\)
vary, proves the disjoint countable partition and its conditional Haar
masses. Iteration proves the finite-word mass formula.

부모 word의 홀수 시작값을 \(n=n_0+2^Lk\)로 쓴다. 부모 word를 실행한
뒤 다음 홀수 numerator를 2로 나눈 값은 \(k\)의 affine 함수이고 그
일차항 계수는 홀수다. 따라서 이 함수는 modulo \(2^B\)에서 순열이다.
\(2^B\)개 lift 중 다음 valuation이 \(b\)인 것은 정확히
\(2^{B-b}\)개이고, \(B\)보다 큰 것은 정확히 하나다. 이를
\(2^B\)로 나누면 조건부 Haar 질량이 나오며, 반복하면 finite-word
공식이 나온다. 이 증명은 2-adic cylinder 측도에 관한 것이며,
각 무한 ray가 양의 자연수를 포함하는지를 자동으로 판정하지 않는다.

### 2.3 Exact finite-word tail / 정확한 유한 word 꼬리

Let \(S_m=a_1+\cdots+a_m\). The linear coefficient after \(m\) accelerated
steps is \(3^m/2^{S_m}\). Hence its noncontracting event is

\[
2^{S_m}\le3^m.
\]

The number of positive compositions of \(s\) into \(m\) parts is
\(\binom{s-1}{m-1}\), so

\[
\Pr(2^{S_m}\le3^m)
=
\sum_{s=m}^{\lfloor m\log_2 3\rfloor}
\binom{s-1}{m-1}2^{-s}.
\]

For \(c=\log_2 3\), the optimized exponential Markov bound is

\[
\Pr(S_m\le cm)
\le
\left[
(c-1)
\left(\frac{c}{2(c-1)}\right)^c
\right]^m
\approx 0.9465045768^m.
\]

이 확률은 선형 계수가 수축하지 않는 valuation word의 정확한
질량이다. affine Collatz 값 자체가 시작값 아래로 내려가는 확률과는
같지 않다. affine 상수항이 별도로 남기 때문이다.

### 2.4 Reproducible computation / 재현 계산

| \(m\) | \(\lfloor m\log_2 3\rfloor\) | exact noncontracting probability / 정확 확률 | Chernoff bound / 상계 |
|---:|---:|---:|---:|
| 4 | 6 | 0.3437500000 | 0.8025846945 |
| 8 | 12 | 0.1938476562 | 0.6441421918 |
| 16 | 25 | 0.1147614717 | 0.4149191633 |
| 32 | 50 | 0.0324543235 | 0.1721579121 |
| 64 | 101 | 0.0046675241 | 0.0296383467 |
| 128 | 202 | 0.0000886180 | 0.0008784316 |

Seven parent words were enumerated at caps \(B=4,8,12\). All 21 rows have
exact counts \(2^{B-b}\) for \(1\le b\le B\), plus one tail residue.

부모 word 7개와 cap 3개를 조합한 21개 전수검사에서 각 \(b\)의
개수는 정확히 \(2^{B-b}\), cap 밖 tail은 정확히 한 residue였다.

### 2.5 No-go, limit, and next lemma / 폐기 경로, 한계, 다음 보조정리

**Rejected route.** Negative mean log multiplier, exponential word-mass
decay, or a density-one conclusion implies descent for every natural start.

**폐기 경로.** 평균 로그 계수가 음수이거나 예외 cylinder의 측도가
0으로 가는 것만으로 모든 자연수 궤도가 내려간다고 결론 내리는
경로.

For a word \(a\),

\[
T^m(n)-n
=
\frac{C_a-(2^{S_m}-3^m)n}{2^{S_m}}.
\]

The coefficient may be contracting while the affine threshold

\[
\frac{C_a}{2^{S_m}-3^m}
\]

remains uncontrolled over all words. A measure-zero nested ray also is not
excluded by a Haar-mass argument.

선형 수축과 실제 하강 사이에는 위 affine threshold가 남는다.
측도 0의 예외 ray가 양의 자연수를 포함하지 않는다는 산술적 증명도
아직 없다.

**Next lemma / 다음 보조정리**

`UniformAffineOffsetControlOnNaturalValuationRays`

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### 3.1 Declared proposition / 선언 명제

For even \(N\), define the reflection

\[
(R_Nf)(a)=f(N-a)
\]

on \(1\le a<N\), and define the prime-only Chebyshev weight

\[
\theta(n)=
\begin{cases}
\log n,&n\text{ prime},\\
0,&\text{otherwise}.
\end{cases}
\]

For \(X\ge27\), let

\[
P_\pm=\frac{I\pm R_N}{2}.
\]

Then

\[
\sum_{a=1}^{N-1}\theta(a)\theta(N-a)
=
\langle\theta,R_N\theta\rangle
=
\lVert P_+\theta\rVert_2^2-\lVert P_-\theta\rVert_2^2.
\]

The left side is positive if and only if \(N\) is a sum of two primes.
Unlike a von Mangoldt convolution, this statement has no prime-power
contamination.

한국어로는 소수에만 양의 가중치를 주는 \(\theta\)를 사용하므로, 왼쪽
합의 양성은 강한 골드바흐 표현의 존재와 정확히 동치다. 반사 연산자의
대칭 에너지와 반대칭 에너지의 차이가 바로 Goldbach 계수다.

### 3.2 Symmetric-baseline no-go / 대칭 기준선 불가능성

For every symmetric baseline \(w=R_Nw\),

\[
P_-(\theta-w)=P_-\theta.
\]

Therefore

\[
\inf_{R_Nw=w}\lVert\theta-w\rVert_2^2
=
\lVert P_-\theta\rVert_2^2,
\]

and the unique minimizer is \(w=P_+\theta\).

어떤 대칭 baseline을 고르더라도 Goldbach 계수의 음의 방향인
반대칭 에너지는 변하지 않는다. 최적 대칭 근사조차 이 에너지를
그대로 오차로 남긴다. 따라서 baseline 선택만으로 binary endpoint
cancellation을 해결하려는 경로는 닫힌다.

### 3.3 Reproducible computation / 재현 계산

| \(N\) | unordered prime pairs / 순서 없는 소수쌍 | reflection gap divided by total energy / 정규화 반사 간극 | antisymmetric energy fraction / 반대칭 에너지 비율 |
|---:|---:|---:|---:|
| 1,000 | 28 | 0.320565 | 0.339717 |
| 10,000 | 127 | 0.205691 | 0.397154 |
| 100,000 | 810 | 0.168016 | 0.415992 |
| 1,000,000 | 5,402 | 0.137256 | 0.431372 |

These four positive coefficients are bounded checks only. Their decrease
also shows why a coarse relative-error certificate loses resolution as
\(N\) grows.

네 endpoint의 양성은 유한 검증일 뿐이다. 정규화 간극이 작아지는
현상은 큰 \(N\)에서 더 정밀한 endpoint별 상쇄 추정이 필요하다는
실험적 압력이지, 점근 정리가 아니다.

### 3.4 No-go, limit, and next lemma / 폐기 경로, 한계, 다음 보조정리

**Rejected route.** Eliminate the endpoint antisymmetric sector by changing
one symmetric baseline for another.

**폐기 경로.** 대칭 baseline을 다른 대칭 baseline으로 바꾸면
반대칭 오차가 사라진다는 가정.

**Remaining gap.** Prove that the binary major-arc contribution exceeds the
minor-arc coefficient with explicit constants at every sufficiently large
even endpoint, then join that theorem to a certified finite range.

**남은 간극.** 충분히 큰 모든 짝수 \(N\)에서 major-arc 주항이
minor-arc coefficient의 절댓값보다 크다는 명시적 상계를 증명하고,
나머지 유한 범위와 결합해야 한다.

**Next lemma / 다음 보조정리**

`ExplicitBinaryPrimeThetaMinorArcBoundBelowMajorArcReflectionGap`

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### 4.1 Declared proposition / 선언 명제

Let

\[
z=\lfloor X^{1/3}\rfloor
\]

and retain \(2\le n\le X-2\) such that both \(n\) and \(n+2\) have no
prime factor at most \(z\). Every retained value is either prime or
semiprime.

Let:

- \(PP\): both \(n,n+2\) are prime;
- \(QQ\): both are semiprime;
- \(PQ+QP\): one is prime and the other semiprime.

Then

\[
\sum_{\substack{n\le X-2\\P^-(n(n+2))>z}}
\bigl(\lambda(n)+\lambda(n+2)\bigr)
=2(QQ-PP).
\]

한국어로는 cubic-rough 조건 아래 각 수의 소인수 개수가 최대 2이므로
Liouville 부호가 `소수=-1`, `반소수=+1`로 정확히 분류된다.
소수-소수 쌍은 \(-2\), 혼합쌍은 0, 반소수-반소수 쌍은 \(+2\)를
기여한다.

### 4.2 Proof and implication / 증명과 함의

Every prime factor is at least \(z+1\). Three such factors would have
product at least

\[
(z+1)^3>X,
\]

which is impossible for \(n,n+2\le X\). This proves the prime-or-semiprime
classification and the identity.

If \(PP>QQ\) for an unbounded sequence of \(X\), then \(PP>0\) on those
scales. Every retained twin pair has smaller prime greater than \(z\), and
\(z\to\infty\). Therefore the Twin Prime conjecture follows.

\(PP>QQ\)가 무한히 큰 scale에서 성립하면 매 scale마다
\(z\)보다 큰 새 쌍둥이 소수가 존재하므로 쌍둥이 소수가 무한하다.
그러나 이 부등식 자체는 아직 증명되지 않았다.

### 4.3 Reproducible computation / 재현 계산

| \(X\) | \(z\) | \(PP\) | \(QQ\) | mixed / 혼합 | \(PP-QQ\) | symmetrized Liouville sum / 대칭 Liouville 합 |
|---:|---:|---:|---:|---:|---:|---:|
| 1,000 | 10 | 33 | 4 | 33 | 29 | -58 |
| 10,000 | 21 | 201 | 35 | 154 | 166 | -332 |
| 100,000 | 46 | 1,218 | 284 | 1,179 | 934 | -1,868 |
| 1,000,000 | 100 | 8,161 | 2,453 | 8,682 | 5,708 | -11,416 |
| 10,000,000 | 215 | 58,965 | 19,074 | 64,868 | 39,891 | -79,782 |

The identity is exact; the sign persistence is finite evidence. No
extrapolation from these five rows is admitted as proof.

항등식은 증명된 정리지만, 다섯 행에서 음수가 유지된다는 사실은 유한
증거다. 이를 무한 scale로 외삽하지 않는다.

### 4.4 No-go, limit, and next lemma / 폐기 경로, 한계, 다음 보조정리

**Rejected route.** A negative shifted Liouville sum through a large finite
cutoff is already an infinite Twin Prime theorem.

**폐기 경로.** 큰 유한 범위에서 Liouville 합이 음수라는 사실을
쌍둥이 소수 무한성으로 승격.

**Remaining gap.** Obtain a parity-breaking lower bound for \(PP-QQ\) at
unbounded scales. Standard nonnegative sieve weights do not distinguish the
two parity classes strongly enough.

**남은 간극.** 표준 비음수 sieve가 구분하지 못하는 소수-소수와
반소수-반소수 계층 사이에 무한 scale의 양의 차이를 증명해야 한다.

**Next lemma / 다음 보조정리**

`UnboundedCubicRoughPrimePrimeExcessOverSemiprimePairs`

## 5. Literature boundary / 문헌 경계

TICKET-153 uses the following primary sources only as context. None of their
open conclusions is imported as a theorem proved by PrimeProject.

TICKET-153은 다음 1차 문헌을 연구 경계로 사용한다. 해당 문헌의 미해결
결론을 PrimeProject가 증명한 결과로 가져오지 않는다.

1. Alain Connes and Caterina Consani,
   [Weil positivity and Trace formula, the archimedean place](https://arxiv.org/abs/2006.13771).
   This supplies the Hilbert-space Weil-positivity context, not the block
   decomposition required here.
   / Hilbert 공간 Weil 양성 맥락을 제공하지만, 본 문서가 요구하는
   실제 block 분해를 제공한 것으로 간주하지 않는다.
2. Terence Tao,
   [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562).
   This fixes the modern almost-all boundary.
   / 현대적인 almost-all 결과와 전칭 명제 사이의 경계를 고정한다.
3. Harald Helfgott,
   [Minor arcs for Goldbach's problem](https://arxiv.org/abs/1205.5252).
   This supplies explicit circle-method context for the remaining binary
   minor-arc target.
   / 남은 binary minor-arc 표적의 명시적 circle-method 맥락이다.
4. James Maynard,
   [On the Twin Prime Conjecture](https://arxiv.org/abs/1910.14674).
   This documents the sieve parity barrier that the \(PP-QQ\) inequality
   must overcome.
   / \(PP-QQ\) 부등식이 넘어야 하는 sieve parity 장벽의 1차 문헌이다.

## 6. Final status / 최종 상태

TICKET-153 establishes:

- one exact positive-tail Schur theorem and essential-norm no-go;
- one exact countable Collatz cylinder law and negative-drift formula;
- one exact prime-only Goldbach reflection criterion;
- one exact cubic-rough Twin parity identity.

TICKET-153가 확정한 것은 다음 네 가지다.

- 양의 tail Schur 정리와 essential-norm 불가능성 정리;
- 가산 Collatz cylinder 법칙과 음의 drift 공식;
- 소수 전용 Goldbach 반사 기준;
- cubic-rough 쌍둥이 소수 parity 항등식.

TICKET-153 does **not** establish:

- positivity of the actual Weil form;
- descent of every natural Collatz orbit;
- positivity of every even prime-theta reflection coefficient;
- \(PP>QQ\) on unbounded cubic-rough scales.

즉 실제 Weil 형식의 양성, 모든 자연수 Collatz 하강, 모든 짝수
Goldbach 반사 계수의 양성, 무한 scale의 \(PP>QQ\)는 모두 열린
증명 간극이다. 네 난제의 해결 상태는 모두 `open_not_proven`이다.
