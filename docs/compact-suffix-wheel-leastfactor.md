# TICKET-154: Compact Schur Tails, Reverse-Suffix Descent, Wheel Projection, and Least-Factor Deficit

## Claim boundary / 주장 경계

This document does **not** prove or disprove the Riemann hypothesis, the
Collatz conjecture, the strong Goldbach conjecture, or the Twin Prime
conjecture. It proves four exact intermediate or no-go results and leaves
one explicitly named infinite lemma open in each track.

이 문서는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 증명하거나 반증하지 않는다. 네 개의 정확한 부분정리 또는
불가능성 정리를 증명하고, 각 트랙에서 하나의 무한 보조정리를 열린
상태로 남긴다.

| Problem / 문제 | Exact TICKET-154 result / 정확한 새 결과 | Rejected route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| Riemann / 리만 | Compact-coupling finite-section promotion and hidden-tail no-go / compact coupling 유한 절단 승격과 숨은 tail 반례 | Trust a finite Schur margin without a certified omitted-tail norm / 생략 tail 노름 없이 유한 Schur margin을 신뢰 | `ActualWeilCompactCouplingWithEffectivePreconditionedTailRate` |
| Collatz / 콜라츠 | Reverse-suffix surplus gives an explicit affine descent threshold / 역방향 suffix 잉여가 명시적 affine 하강 임계값을 제공 | Use only final valuation surplus and ignore valuation order / valuation 순서를 버리고 최종 잉여만 사용 | `EveryNaturalValuationRayHitsAReverseSuffixSurplusDescentBlock` |
| Goldbach / 골드바흐 | Symmetric wheel-projection certificate and fixed-modulus energy no-go / 대칭 wheel 투영 인증과 고정 modulus 에너지 불가능성 | Expect one fixed wheel to dominate prime-theta energy at all scales / 하나의 고정 wheel이 모든 scale의 에너지를 지배한다고 가정 | `EffectiveGrowingWheelProjectionDominanceAtEveryLargeEvenEndpoint` |
| Twin Prime / 쌍둥이 소수 | Exact least-factor deficit `PP-QQ=R-M` and small-prime fingerprint collision / 최소소인수 deficit 항등식과 작은 소수 fingerprint 충돌 | Separate prime-prime from semiprime-semiprime using only primes at most \(z\) / \(z\) 이하 소수 정보만으로 PP와 QQ 분리 | `UnboundedCubicRoughMeanLeastFactorIncidenceBelowOne` |

Machine-readable source / 기계 판독 원본:
[`ticket154-compact-suffix-wheel-leastfactor.json`](../data/open-problem/ticket154-compact-suffix-wheel-leastfactor.json).

```text
python scripts/ticket154_compact_suffix_wheel_leastfactor.py
python -m unittest tests.test_ticket154_compact_suffix_wheel_leastfactor -v
```

## 1. Riemann hypothesis / 리만 가설

### 1.1 Declared proposition / 선언 명제

Let \(H_0\) be finite dimensional, let \(D\ge\delta I>0\) on \(H_1\),
and define the preconditioned coupling

\[
K=D^{-1/2}C.
\]

Let \(Q_N\) be finite-rank orthogonal projections on \(H_1\) converging
strongly to \(I\). Define

\[
S=A-K^*K,\qquad S_N=A-K^*Q_NK,
\qquad e_N=\lVert(I-Q_N)K\rVert^2.
\]

Then

\[
S=S_N-K^*(I-Q_N)K,\qquad
0\le K^*(I-Q_N)K\le e_NI,
\]

and \(e_N\to0\). Consequently,

\[
S_N\ge e_NI\quad\Longrightarrow\quad S\ge0.
\]

Combining this with TICKET-153's Schur criterion proves positivity of the
full block operator whenever the finite Schur margin pays the entire
preconditioned coupling tail.

한국어로는 실제 tail을 버리는 것이 아니라, \(D^{-1/2}C\)의 생략
부분이 만드는 Schur 비용을 정확히 지불해야 한다는 정리다. 유한
core \(H_0\) 때문에 \(K\)는 compact이고, strong projection convergence가
\(K\)의 compact image에서는 operator-norm convergence로 강화된다.

### 1.2 Proof / 증명

The image of the unit ball of finite-dimensional \(H_0\) under \(K\) has
compact closure. Strong convergence \(Q_N\to I\) is uniform on that compact
set, hence

\[
\lVert(I-Q_N)K\rVert\longrightarrow0.
\]

Adding and subtracting \(K^*Q_NK\) yields the exact Schur identity. For
every \(x\in H_0\),

\[
\langle K^*(I-Q_N)Kx,x\rangle
=\lVert(I-Q_N)Kx\rVert^2
\le e_N\lVert x\rVert^2.
\]

Thus \(S_N\ge e_NI\) implies \(S\ge0\).

유한차원 domain에서 compactness가 자동으로 생기는 점이 핵심이다.
그러나 이 정리는 actual Weil form의 \(D,C\)를 구성해 주지 않는다.
실제 산술 operator가 이 가정들을 만족한다는 별도 증명이 필요하다.

### 1.3 Exact computation / 정확 계산

For the scalar-core model \(K_i=2^{-i}\),

\[
\lVert K\rVert^2=\sum_{i\ge1}4^{-i}=\frac13,\qquad
e_N=\sum_{i>N}4^{-i}=\frac1{3\cdot4^N}.
\]

Taking \(A=1/3\), the finite Schur margin equals \(e_N\) exactly and the
certified full margin is zero.

| \(N\) | omitted cost \(e_N\) / 생략 비용 | finite margin / 유한 margin | certified full margin / 전체 margin |
|---:|---:|---:|---:|
| 1 | \(1/12\) | \(1/12\) | 0 |
| 2 | \(1/48\) | \(1/48\) | 0 |
| 4 | \(1/768\) | \(1/768\) | 0 |
| 8 | \(1/196608\) | \(1/196608\) | 0 |
| 12 | \(1/50331648\) | \(1/50331648\) | 0 |
| 16 | \(1/12884901888\) | \(1/12884901888\) | 0 |

### 1.4 No-go and remaining gap / 폐기 경로와 남은 간극

For any isolated cutoff \(N\), take scalar \(H_0\), let

\[
Kx=xe_{N+1},\qquad A=\frac12.
\]

The observed coupling is zero, so the finite margin is \(1/2\). But
\(K^*K=1\), and the full Schur margin is \(-1/2\). The coupling is rank
one and therefore compact.

어떤 단일 유한 cutoff도 생략 tail의 정량적 bound가 없으면 양성을
인증하지 못한다. “compact이므로 언젠가 작아진다”는 정성적 문장도
현재 cutoff의 오차를 주지 않는다.

**Remaining gap / 남은 간극**

Construct the actual Weil block decomposition, prove \(D\ge\delta I\),
prove \(D^{-1/2}C\) compact, and obtain an effective \(e_N\) below the
finite Schur margin. No off-critical zero is excluded here.

**Next lemma / 다음 보조정리**

`ActualWeilCompactCouplingWithEffectivePreconditionedTailRate`

## 2. Collatz conjecture / 콜라츠 추측

### 2.1 Declared proposition / 선언 명제

For a valuation word \(a=(a_1,\ldots,a_m)\), write

\[
T^m(n)=\frac{3^mn+C_a}{2^S},
\qquad
S=\sum_{i=1}^m a_i.
\]

If every reverse suffix of length \(k\) satisfies

\[
\sum_{i=m-k+1}^m a_i\ge qk
\quad(1\le k\le m)
\]

for an integer \(q\ge2\), then

\[
\frac{C_a}{2^S-3^m}\le\frac1{2^q-3}.
\]

For \(q=2\), every odd \(n>1\) realizing the word satisfies

\[
T^m(n)<n.
\]

### 2.2 Proof / 증명

Let \(S_j=a_1+\cdots+a_j\), with \(S_0=0\). Iterating the affine map gives

\[
C_a=\sum_{j=0}^{m-1}3^{m-1-j}2^{S_j}.
\]

Indexing by reverse suffix length \(k=m-j\),

\[
\frac{C_a}{2^S}
=\sum_{k=1}^m
\frac{3^{k-1}}{2^{S-S_{m-k}}}
\le
\sum_{k=1}^m\frac{3^{k-1}}{2^{qk}}
=
\frac{1-(3/2^q)^m}{2^q-3}.
\]

The full-word suffix condition also gives

\[
\frac{3^m}{2^S}\le\left(\frac3{2^q}\right)^m.
\]

Dividing the two bounds proves the threshold inequality.

한국어로는 마지막 valuation들부터 충분한 2-adic 잉여가 누적되면,
affine 상수항의 각 과거 기여가 역방향 기하급수로 눌린다. \(q=2\)이면
threshold가 1 이하이므로 모든 홀수 \(n>1\)에서 실제 strict descent가
발생한다.

### 2.3 Exact geometric coverage / 정확한 기하분포 coverage

Under TICKET-153's exact cylinder law,

\[
\Pr(a_i=b)=2^{-b}.
\]

Reversal does not change word mass. The increments \(a_i-2\) form a
critical skip-free walk, and the ballot identity gives

\[
\Pr\left(
\sum_{i=1}^k(a_i-2)\ge0
\text{ for every }k\le m
\right)
=\frac{\binom{2m}{m}}{4^m}
\sim\frac1{\sqrt{\pi m}}.
\]

| \(m\) | exact certificate mass / 정확 질량 | \(\sqrt{\pi m}\) scaled |
|---:|---:|---:|
| 1 | 0.500000 | 0.886227 |
| 2 | 0.375000 | 0.939986 |
| 4 | 0.273438 | 0.969311 |
| 8 | 0.196381 | 0.984506 |
| 16 | 0.139950 | 0.992219 |
| 32 | 0.099347 | 0.996102 |
| 64 | 0.070386 | 0.998049 |
| 128 | 0.049819 | 0.999024 |

The sufficient certificate is exact, but its fixed-length cylinder mass
tends to zero. This is not a universal occurrence theorem.

충분조건 자체는 정확하지만 길이가 커질수록 해당 word 집합의 Haar
질량은 0으로 간다. 따라서 이 결과만으로 모든 자연수 ray를 덮을 수
없다.

### 2.4 Total-surplus no-go / 최종 잉여만 쓰는 경로의 반례

The two words

\[
(1,3),\qquad(3,1)
\]

have the same length, total valuation, multiset, and linear multiplier
\(9/16\). Their affine thresholds differ:

\[
\tau_{(1,3)}=\frac57,\qquad
\tau_{(3,1)}=\frac{11}7.
\]

Only \((1,3)\) satisfies the reverse-suffix floor-two condition. More
generally, an adjacent swap changes only one prefix term in \(C_a\);
placing the larger valuation first increases \(C_a\). Therefore ascending
order minimizes the affine constant and descending order maximizes it.

같은 최종 surplus라도 valuation 순서에 따라 affine threshold가
달라진다. 최종 \(S\), 평균 valuation, linear multiplier만 사용하는
전략은 이 차이를 볼 수 없으므로 폐기한다.

**Remaining gap / 남은 간극**

Prove that every natural Collatz valuation ray reaches a finite contiguous
block satisfying the reverse-suffix floor-two condition. Such a theorem,
combined with strict descent and strong induction, would prove Collatz.
No such universal occurrence theorem is established here.

**Next lemma / 다음 보조정리**

`EveryNaturalValuationRayHitsAReverseSuffixSurplusDescentBlock`

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### 3.1 Declared proposition / 선언 명제

For even \(N\), work in \(\mathbb R^{N-1}\) with reflection

\[
(R_Nf)(a)=f(N-a).
\]

Fix a squarefree wheel \(W\). Let \(U_{N,W}\) be the subspace of functions
that are reflection-symmetric and constant on each residue orbit generated
by

\[
a\bmod W,\qquad N-a\bmod W.
\]

Let \(u\) be the orthogonal projection of the prime-only theta vector onto
\(U_{N,W}\), and set \(e=\theta-u\). Then

\[
\langle\theta,R_N\theta\rangle
=
\lVert u\rVert^2
+\lVert P_+e\rVert^2
-\lVert P_-e\rVert^2.
\]

Therefore

\[
\lVert u\rVert^2>\lVert e\rVert^2
\quad\Longrightarrow\quad
\langle\theta,R_N\theta\rangle>0,
\]

which certifies a Goldbach representation.

### 3.2 Proof / 증명

The space \(U_{N,W}\) lies in the \(+1\) eigenspace of \(R_N\).
Orthogonal projection gives \(u\perp e\), and hence
\(u\perp P_+e\). Expanding the reflection quadratic form gives the exact
identity. Since

\[
\lVert P_+e\rVert^2-\lVert P_-e\rVert^2
\ge-\lVert e\rVert^2,
\]

the norm inequality is sufficient.

대칭 wheel model이 잡아낸 에너지가 전체 orthogonal residual보다 크면
Goldbach coefficient가 양수다. 이 명제는 정확하지만 충분조건이지
필요조건은 아니다.

### 3.3 Fixed-modulus no-go / 고정 modulus 불가능성

For fixed \(W\), the prime number theorem in arithmetic progressions gives
bounded residue-cell means:

\[
\frac{\sum_{\substack{a<N\\a\equiv r\pmod W}}\theta(a)}
{\#\{a<N:a\equiv r\pmod W\}}
=O_W(1).
\]

There are finitely many residue orbits, so

\[
\lVert u\rVert^2=O_W(N).
\]

By partial summation,

\[
\lVert\theta\rVert^2
=\sum_{p<N}(\log p)^2
\sim N\log N.
\]

Consequently,

\[
\frac{\lVert u\rVert^2}{\lVert\theta\rVert^2}
\longrightarrow0.
\]

Thus no fixed wheel can satisfy the energy-dominance certificate at all
large endpoints.

고정 wheel은 소수의 local admissibility는 정확히 표현하지만, 커지는
\(\log p\) 에너지와 endpoint별 fluctuation을 담지 못한다. 따라서
modulus를 고정한 채 이 \(L^2\) 인증을 무한 scale로 승격하는 경로는
정리 수준에서 폐기된다.

### 3.4 Local support and finite computation / local support와 유한 계산

The number of locally admissible residues is exactly

\[
A_W(N)=
\prod_{p\mid W}
\begin{cases}
p-1,&p\mid N,\\
p-2,&p\nmid N.
\end{cases}
\]

This follows prime by prime and then from the Chinese remainder theorem.
All 9 direct counts for \(W=6,30,210\) and
\(N=10^4,10^5,10^6\) match the formula.

| \(N\) | \(W\) | projection energy fraction / 투영 에너지 비율 | certificate |
|---:|---:|---:|---|
| 10,000 | 6 | 0.271036 | fail |
| 10,000 | 30 | 0.338758 | fail |
| 10,000 | 210 | 0.374059 | fail |
| 100,000 | 6 | 0.213510 | fail |
| 100,000 | 30 | 0.266887 | fail |
| 100,000 | 210 | 0.294422 | fail |
| 1,000,000 | 6 | 0.175323 | fail |
| 1,000,000 | 30 | 0.219153 | fail |
| 1,000,000 | 210 | 0.241528 | fail |

Every tested endpoint actually has Goldbach representations. The failed
certificate says only that these fixed wheel spaces are too coarse.

모든 endpoint의 실제 Goldbach coefficient는 양수다. `fail`은 반례가
아니라 fixed-wheel 충분조건이 해당 양성을 인증하지 못했다는 뜻이다.

**Remaining gap / 남은 간극**

Construct a growing, endpoint-adaptive major-arc subspace whose symmetric
projection energy exceeds its orthogonal residual for every sufficiently
large even \(N\), with a certified finite join.

**Next lemma / 다음 보조정리**

`EffectiveGrowingWheelProjectionDominanceAtEveryLargeEvenEndpoint`

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### 4.1 Declared proposition / 선언 명제

Let \(X\ge27\), \(z=\lfloor X^{1/3}\rfloor\), and retain
\(2\le n\le X-2\) such that

\[
P^-(n(n+2))>z.
\]

Define

\[
\ell_X(n)=
\begin{cases}
0,&n\text{ prime},\\
1,&n\text{ composite}.
\end{cases}
\]

Cubic roughness makes every retained composite a semiprime. Its unique
least prime factor lies in \((z,\sqrt n]\), so \(\ell_X\) is a
medium-least-factor incidence.

Let \(R\) be the total number of retained gap-two pairs and

\[
M=\sum_{\text{retained }n}
\bigl(\ell_X(n)+\ell_X(n+2)\bigr).
\]

Then

\[
R-M=PP-QQ,\qquad M=2QQ+PQ+QP.
\]

Therefore

\[
PP>QQ
\quad\Longleftrightarrow\quad
\frac MR<1.
\]

### 4.2 Proof / 증명

On a retained pair,

\[
1-\ell_X(n)-\ell_X(n+2)
\]

equals \(+1\) for prime-prime, \(0\) for a mixed pair, and \(-1\) for
semiprime-semiprime. Summation proves the first identity. Counting one
incidence for each semiprime side proves the second.

한국어로는 TICKET-153의 \(PP-QQ\) 부호를 “gap-two rough population당
중간 최소소인수의 평균 발생 횟수가 1보다 작은가?”라는 하나의 평균
부등식으로 바꾼 것이다.

### 4.3 Small-prime fingerprint no-go / 작은 소수 fingerprint 불가능성

Every retained number has no prime divisor at most \(z\). Hence its entire
divisibility fingerprint over primes \(p\le z\) is the all-zero vector.
This vector is identical for prime and semiprime members.

At every audited scale the program finds both a PP and a QQ pair with this
same fingerprint:

| \(X\) | \(z\) | PP example / PP 예 | QQ example / QQ 예 |
|---:|---:|---:|---:|
| 1,000 | 10 | (11, 13) | (527, 529) |
| 10,000 | 21 | (29, 31) | (1679, 1681) |
| 100,000 | 46 | (59, 61) | (4187, 4189) |
| 1,000,000 | 100 | (101, 103) | (24287, 24289) |
| 10,000,000 | 215 | (227, 229) | (59987, 59989) |

Therefore a classifier or nonnegative sieve using only small-prime
roughness bits cannot distinguish the parity classes.

\(z\) 이하 소수의 나눗셈 정보만으로는 PP와 QQ가 완전히 같은
fingerprint를 가진다. 필요한 정보는 \((z,\sqrt X]\)의 최소소인수
발생률 또는 그와 동등한 Type II 상관 정보다.

### 4.4 Finite incidence audit / 유한 incidence 검사

| \(X\) | rough pairs \(R\) | incidence \(M\) | \(M/R\) | \(R-M=PP-QQ\) |
|---:|---:|---:|---:|---:|
| 1,000 | 70 | 41 | 0.585714 | 29 |
| 10,000 | 390 | 224 | 0.574359 | 166 |
| 100,000 | 2,681 | 1,747 | 0.651623 | 934 |
| 1,000,000 | 19,296 | 13,588 | 0.704187 | 5,708 |
| 10,000,000 | 142,907 | 103,016 | 0.720860 | 39,891 |

The independence heuristic suggests

\[
2\sum_{X^{1/3}<p\le X^{1/2}}\frac1p
\approx2\log\frac32
=0.810930\ldots<1.
\]

This value is a heuristic comparison, not a proved asymptotic for the
conditioned gap-two population.

독립성 heuristic은 양의 여유를 제안하지만, 실제 rough gap-two
population에서 필요한 uniform upper bound는 증명되지 않았다. 표의
다섯 행도 무한 명제로 외삽하지 않는다.

**Remaining gap / 남은 간극**

Prove \(M/R<1\) on an unbounded sequence of cubic-rough scales. By the
exact identity, this would force \(PP>QQ\), and TICKET-153 then yields
infinitely many twin primes.

**Next lemma / 다음 보조정리**

`UnboundedCubicRoughMeanLeastFactorIncidenceBelowOne`

## 5. Literature boundary / 문헌 경계

These primary sources fix the boundary of known theory. TICKET-154 does
not import any open conclusion as a PrimeProject theorem.

다음 1차 문헌은 알려진 이론의 경계를 정할 뿐이며, 미해결 결론을
PrimeProject의 정리로 가져오지 않는다.

1. Alain Connes and Caterina Consani,
   [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368).
   It motivates an operator-theoretic Weil framework; it does not supply
   the compact coupling and effective tail rate required here.
   / operator-theoretic Weil 맥락이지만 본 TICKET의 compact coupling
   가정을 증명한 것으로 사용하지 않는다.
2. Terence Tao,
   [Almost all orbits of the Collatz map attain almost bounded values,
   v7 (2026)](https://arxiv.org/abs/1909.03562).
   Its logarithmic-density result remains distinct from the universal
   natural-ray occurrence theorem required here.
   / 최신 v7의 almost-all 결과와 모든 자연수 ray 명제를 구분한다.
3. Harald Helfgott,
   [Major arcs for Goldbach's problem](https://arxiv.org/abs/1305.2897).
   It provides explicit major-arc context, not the binary growing-space
   energy dominance asserted as the next lemma.
   / 명시적 major-arc 맥락이며 다음 binary 정리를 제공하지 않는다.
4. Kevin Ford and James Maynard,
   [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).
   Its Type I/II framework explains why substantial bilinear information
   is needed for lower bounds; the present least-factor incidence target
   remains open.
   / lower bound에 필요한 Type I/II 정보의 맥락이며 incidence
   부등식은 여전히 열려 있다.

## 6. Final status / 최종 상태

TICKET-154 establishes:

- an exact compact-coupling Schur promotion theorem and a hidden-tail
  finite-cutoff counterexample;
- an exact reverse-suffix affine descent certificate, its ballot-law
  coverage, and a total-surplus no-go;
- an exact symmetric wheel-projection certificate and a fixed-modulus
  asymptotic energy no-go;
- an exact cubic-rough least-factor deficit identity and explicit
  small-prime fingerprint collisions.

TICKET-154가 확정한 것은 compact Schur 승격 조건, Collatz의
reverse-suffix affine 하강 조건, Goldbach의 fixed-wheel 한계, Twin의
least-factor deficit 항등식이다.

It does **not** establish:

- the required actual-Weil compact coupling;
- universal occurrence of Collatz descent blocks;
- growing-major-arc dominance for every large even endpoint;
- \(M/R<1\) on unbounded cubic-rough scales.

따라서 네 난제의 해결 상태는 모두 `open_not_proven`이며, 완전한
증명이나 반례는 없다.
