# TICKET-155: Range Exactness, Initial-Prefix Descent, Sublinear Wheels, and Conditional Transfer

## Claim boundary / 주장 경계

This document does **not** prove or disprove the Riemann hypothesis, the
Collatz conjecture, the strong Goldbach conjecture, or the Twin Prime
conjecture. It proves four exact route-correction or no-go results. Every
target conjecture remains `open_not_proven`.

이 문서는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 증명하거나 반증하지 않는다. 기존 경로의 논리적 또는 정량적
약점을 교정하는 네 개의 정확한 정리와 불가능성 결과를 증명한다.
네 추측은 모두 `open_not_proven`이다.

| Problem / 문제 | Exact TICKET-155 result / 정확한 결과 | Rejected route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| Riemann / 리만 | A finite-core coupling is closed exactly by its range projection, while coordinate-tail decay can follow any prescribed convergent profile / finite core coupling은 range projection으로 정확히 닫히지만 좌표 tail 속도는 임의로 느릴 수 있음 | Treat compactness or basis coefficients as a canonical arithmetic rate / compactness나 basis 계수를 산술적 유효 속도로 간주 | `ActualWeilFiniteCoreRangeConstructionAndPositiveSchurMatrix` |
| Collatz / 콜라츠 | Reverse-suffix certification is an initial-prefix record condition; later local descent need not fall below the original start / reverse-suffix 인증은 initial-prefix record 조건이며 이후 local descent는 시작값 아래 하강을 보장하지 않음 | Use a later local descent block as a strong-induction descent / 중간 local descent를 강한 귀납 하강으로 사용 | `EveryNaturalStartCrossesAnInitialAffineDescentThreshold` |
| Goldbach / 골드바흐 | Every wheel with \(W_N\le N^{1-\varepsilon}\) captures a vanishing fraction of prime-theta energy / 모든 고정 거듭제곱 이하 wheel의 theta 에너지 비율은 0으로 수렴 | Grow the wheel at a fixed sublinear power and retain the same \(L^2\) certificate / sublinear wheel로 기존 에너지 인증 유지 | `EffectiveGoldbachMajorMinorArcReflectionLowerBoundWithFiniteJoin` |
| Twin Prime / 쌍둥이 소수 | Exact conditional-semiprime transfer identity and rare-event covariance no-go / 조건부 semiprime 전이 항등식과 희귀 사건 covariance no-go | Use unnormalized covariance \(o(1)\) under vanishing-probability conditioning / 희귀 조건에서 비정규화 covariance 수렴만 사용 | `ShiftTwoCubicRoughSemiprimeRelativeCovarianceSaving` |

Machine-readable source / 기계 판독 원본:
[`ticket155-range-prefix-sublinear-conditional.json`](../data/open-problem/ticket155-range-prefix-sublinear-conditional.json).

```text
python scripts/ticket155_range_prefix_sublinear_conditional.py
python -m unittest tests.test_ticket155_range_prefix_sublinear_conditional -v
```

## 1. Riemann hypothesis / 리만 가설

### 1.1 Declared proposition / 선언 명제

Let \(H_0\) be \(d\)-dimensional and let \(K:H_0\to H_1\). Then

\[
\operatorname{rank}K\le d.
\]

If \(Q_R\) is the orthogonal projection onto
\(\overline{\operatorname{Ran}K}\), then

\[
(I-Q_R)K=0.
\]

Thus the TICKET-154 Schur tail is closed exactly by a projection of rank
\(\operatorname{rank}K\).

However, coordinate-tail convergence has no basis-invariant rate. Let
\((e_N)_{N\ge0}\) be any nonincreasing sequence with

\[
e_0=1,\qquad e_N\longrightarrow0.
\]

There is a unit vector \(v\in\ell^2\) such that for the standard coordinate
projection \(P_N\),

\[
\|(I-P_N)v\|^2=e_N.
\]

Consequently, even a rank-one compact coupling can realize any prescribed
convergent coordinate-tail profile.

한국어로는 finite core의 실제 coupling range를 알면 tail 문제는
유한차원에서 정확히 끝난다. 반대로 basis만 고정하고 coefficient
tail을 관찰하면 compact 또는 rank-one이라는 사실만으로는 속도를
얻을 수 없다.

### 1.2 Proof / 증명

The range statement follows from finite-dimensional linear algebra. For the
profile theorem, define

\[
|v_j|^2=e_{j-1}-e_j.
\]

The terms are nonnegative and telescope:

\[
\sum_{j\ge1}|v_j|^2=e_0-\lim_{N\to\infty}e_N=1.
\]

Moreover,

\[
\sum_{j>N}|v_j|^2=e_N.
\]

Taking \(Kx=xv\) produces a rank-one compact operator with exactly that
coordinate tail. Projection onto \(\operatorname{span}\{v\}\) has rank one
and zero omitted cost.

따라서 “compact이므로 coefficient tail이 충분히 빠르다”는 주장은
basis와 실제 \(K\)를 지정하지 않으면 정량적 의미가 없다. TICKET-154의
abstract compactness target은 actual Weil range construction으로
교체되어야 한다.

### 1.3 Exact computation / 정확 계산

Choose

\[
e_N=\frac1{N+1},\qquad
|v_j|^2=\frac1{j(j+1)}.
\]

| \(N\) | coordinate tail \(e_N\) | geometric comparison \(4^{-N}\) | range-projection tail |
|---:|---:|---:|---:|
| 1 | \(1/2\) | \(1/4\) | 0 |
| 2 | \(1/3\) | \(1/16\) | 0 |
| 4 | \(1/5\) | \(1/256\) | 0 |
| 8 | \(1/9\) | \(1/65536\) | 0 |
| 16 | \(1/17\) | \(1/4294967296\) | 0 |
| 32 | \(1/33\) | \(1/2^{64}\) | 0 |

This is not evidence against RH. It is a counterexample to extracting a
canonical effective rate from compactness or finite rank alone.

### 1.4 Remaining gap / 남은 간극

The semi-local Weil framework must first be converted into an actual block
decomposition with a justified finite core. Its coupling range must then be
constructed invariantly and the exact finite Schur matrix must be proved
positive. No such construction is supplied here.

**Next lemma / 다음 보조정리**

`ActualWeilFiniteCoreRangeConstructionAndPositiveSchurMatrix`

## 2. Collatz conjecture / 콜라츠 추측

### 2.1 Declared proposition / 선언 명제

For an initial valuation prefix \(a_1,\ldots,a_m\), define

\[
B_j=\sum_{i=1}^j(a_i-2),\qquad B_0=0.
\]

The TICKET-154 reverse-suffix floor-two condition is equivalent to

\[
B_m=\max_{0\le j\le m}B_j.
\]

When this condition holds, the entire prefix sends every realizing odd
start \(n>1\) below the **same initial \(n\)**.

Every positive odd start eventually has a one-step local descent. If
\(r=v_2(n+1)\), then the first \(r-1\) valuations are one and the \(r\)-th
valuation is at least two. But this does not imply descent below the
original start.

### 2.2 Record proof / record 조건 증명

A suffix from \(j+1\) through \(m\) has surplus

\[
\sum_{i=j+1}^m(a_i-2)=B_m-B_j.
\]

All reverse suffixes are nonnegative exactly when
\(B_m\ge B_j\) for every \(j\). TICKET-154's affine estimate then applies
to the entire initial prefix.

If \(n+1=2^r u\), with \(u\) odd, direct induction gives

\[
T^j(n)=3^j2^{r-j}u-1,\qquad 0\le j<r.
\]

Hence the first \(r-1\) valuations equal one and the next valuation is at
least two. This proves eventual **local** descent only.

### 2.3 Infinite no-go family / 무한 no-go 가족

Let

\[
n=4u-1,\qquad u\equiv3\pmod4.
\]

Then the first two odd Collatz iterates are

\[
n\longmapsto 6u-1\longmapsto\frac{9u-1}{2},
\]

with valuation word \((1,2)\). The second step decreases because

\[
\frac{9u-1}{2}<6u-1,
\]

but its endpoint is still above the initial value:

\[
\frac{9u-1}{2}>4u-1.
\]

| \(u\) | initial \(n\) | first iterate | local-descent endpoint | endpoint minus \(n\) |
|---:|---:|---:|---:|---:|
| 3 | 11 | 17 | 13 | 2 |
| 7 | 27 | 41 | 31 | 4 |
| 11 | 43 | 65 | 49 | 6 |
| 15 | 59 | 89 | 67 | 8 |
| 19 | 75 | 113 | 85 | 10 |
| 23 | 91 | 137 | 103 | 12 |

Thus a later certified block cannot be inserted into strong induction unless
the resulting value is also below the original start.

또한 \(n=2^L-1\)은 처음 \(L-1\)개의 valuation이 모두 1이다. 따라서
local descent조차 모든 시작값에 대해 하나의 고정된 step 수 안에서
발생한다고 주장할 수 없다.

### 2.4 Correction to TICKET-154 / TICKET-154 교정

TICKET-154 stated that universal occurrence of a later reverse-suffix block,
combined with strong induction, would prove Collatz. That statement omitted
the need to compare the block endpoint with the original start. TICKET-155
withdraws that implication.

TICKET-154의 “궤도에서 block을 만나면 strong induction으로 충분하다”는
표현은 block 시작점과 최초 시작값을 혼동했다. 정확한 목표는 최초
시작값을 기준으로 한 initial-prefix descent이다.

**Next lemma / 다음 보조정리**

`EveryNaturalStartCrossesAnInitialAffineDescentThreshold`

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### 3.1 Declared proposition / 선언 명제

Fix \(\varepsilon>0\). Let \(W_N<N\) satisfy

\[
W_N\le N^{1-\varepsilon}.
\]

Let \(u_{N,W_N}\) be the TICKET-154 orthogonal projection of the prime-only
theta vector onto reflection-symmetric residue-orbit cells modulo \(W_N\).
Then

\[
\frac{\|u_{N,W_N}\|^2}{\|\theta_N\|^2}\longrightarrow0.
\]

A growing wheel at any fixed sublinear power therefore still cannot satisfy
the TICKET-154 energy-dominance certificate for every sufficiently large
endpoint.

### 3.2 Proof / 증명

Each reflection orbit contains at most two residue classes. For a coprime
class, Brun--Titchmarsh gives

\[
\pi(N;W,r)\ll
\frac{N}{\varphi(W)\log(N/W)}.
\]

Its theta mass is therefore at most

\[
O\!\left(
\frac{N\log N}{\varphi(W)\log(N/W)}
\right).
\]

Each nonempty residue cell contains \(\Omega(N/W)\) integers. Summing its
squared mean contribution over the coprime cells yields

\[
\|u_{N,W}\|^2
\ll
N\frac{W}{\varphi(W)}
\left(\frac{\log N}{\log(N/W)}\right)^2.
\]

Noncoprime cells contain only the finitely many primes dividing \(W\) and
are negligible. Meanwhile,

\[
\|\theta_N\|^2
=\sum_{p<N}(\log p)^2
\sim N\log N.
\]

Since \(W/\varphi(W)=O(\log\log W)\) and
\(\log(N/W)\ge\varepsilon\log N\), the energy ratio tends to zero.

### 3.3 Finite schedule / 유한 schedule

| \(N\) | growing \(W\) | \(\log W/\log N\) | projection-energy fraction | certificate |
|---:|---:|---:|---:|---|
| 10,000 | 30 | 0.369280 | 0.338758 | fail |
| 100,000 | 210 | 0.464444 | 0.294422 | fail |
| 1,000,000 | 2,310 | 0.560602 | 0.257925 | fail |

Every endpoint has positive actual Goldbach correlation. `fail` means only
that this sufficient \(L^2\) projection certificate remains too coarse.

### 3.4 Route squeeze / 경로 압축

TICKET-154 excluded fixed wheels. TICKET-155 excludes every wheel bounded by
\(N^{1-\varepsilon}\). A modulus near \(N\) creates almost row-unique cells
and loses out-of-sample content, as earlier PrimeProject audits already
showed. The retained route must therefore control the binary correlation
directly through major and minor arcs rather than through residue-cell
energy dominance.

**Next lemma / 다음 보조정리**

`EffectiveGoldbachMajorMinorArcReflectionLowerBoundWithFiniteJoin`

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### 4.1 Declared proposition / 선언 명제

Within the left and right cubic-rough populations, let

- \(d_L,d_R\) be the ambient semiprime fractions;
- \(\rho_L,\rho_R\) be the probabilities that the shifted partner is also
  rough;
- \(c_L,c_R\) be the covariances between the semiprime label and the
  shifted-partner roughness event.

Then the TICKET-154 incidence ratio satisfies exactly

\[
\frac{M}{R}
=d_L+d_R+\frac{c_L}{\rho_L}+\frac{c_R}{\rho_R}.
\]

Therefore

\[
\frac{M}{R}<1
\]

follows if and only if the total conditional shift is below the ambient
margin:

\[
\frac{c_L}{\rho_L}+\frac{c_R}{\rho_R}
<
1-d_L-d_R.
\]

### 4.2 Proof / 증명

On the left rough population, let \(D_L\) be the semiprime indicator and
\(B_L\) the event that the right partner is rough. Then

\[
\Pr(D_L\mid B_L)-\Pr(D_L)
=
\frac{\operatorname{Cov}(D_L,B_L)}{\Pr(B_L)}
=\frac{c_L}{\rho_L}.
\]

The same identity holds on the right. Adding the two conditional semiprime
fractions gives \(M/R\).

한국어로는 필요한 것은 단순한 \(c_L,c_R\to0\)가 아니라 희귀 사건의
확률 \(\rho_L,\rho_R\)로 나눈 뒤에도 남는 **relative covariance
saving**이다.

### 4.3 Rare-event covariance no-go / 희귀 사건 covariance no-go

For each \(k\), take a finite uniform universe of size \(5\cdot2^k\).
Let the selected event have size \(5\), the semiprime-labelled set have size
\(2\cdot2^k\), and their intersection have size \(3\). Then

\[
\rho=2^{-k},\qquad
\Pr(D)=\frac25,\qquad
\Pr(D\mid B)=\frac35.
\]

Thus

\[
\operatorname{Cov}(D,B)=\frac{\rho}{5}\longrightarrow0,
\]

while

\[
\frac{\operatorname{Cov}(D,B)}{\rho}=\frac15
\]

does not decrease. Absolute covariance decay is therefore insufficient.

### 4.4 Finite arithmetic audit / 유한 산술 감사

| \(X\) | ambient sum \(d_L+d_R\) | conditional \(M/R\) | conditional shift | deficit \(1-M/R\) |
|---:|---:|---:|---:|---:|
| 1,000 | 0.555066 | 0.585714 | 0.030648 | 0.414286 |
| 10,000 | 0.571930 | 0.574359 | 0.002429 | 0.425641 |
| 100,000 | 0.651271 | 0.651623 | 0.000352 | 0.348377 |
| 1,000,000 | 0.700337 | 0.704187 | 0.003850 | 0.295813 |
| 10,000,000 | 0.721315 | 0.720860 | -0.000454 | 0.279140 |

These rows are finite evidence. They do not prove that the relative
covariance saving persists on unbounded scales.

**Next lemma / 다음 보조정리**

`ShiftTwoCubicRoughSemiprimeRelativeCovarianceSaving`

## 5. Literature boundary / 문헌 경계

The following primary sources define context, not imported conclusions.

다음 1차 문헌은 연구 경계를 정할 뿐, 미해결 결론을 본 프로젝트의
정리로 가져오지 않는다.

1. Alain Connes and Caterina Consani,
   [Weil positivity and Trace formula, the archimedean place](https://arxiv.org/abs/2006.13771),
   revised in 2026. Its semi-local compression and finite-rank spectral
   approximation are not identified here with the abstract finite-core
   Schur block.
2. Terence Tao,
   [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562),
   v7 (2026). An almost-all logarithmic-density theorem is distinct from
   every-start initial-prefix descent.
3. Ping Xi and Junren Zheng,
   [On the Brun--Titchmarsh theorem](https://arxiv.org/abs/2404.01003).
   PrimeProject uses the classical arithmetic-progression upper-bound shape
   only for the sublinear-wheel no-go.
4. Kevin Ford and James Maynard,
   [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).
   Their Type I/II framework explains why a relative shifted saving is
   materially stronger than one-dimensional marginal information.

## 6. Final status / 최종 상태

TICKET-155 establishes:

- range-exact finite-core Schur truncation and arbitrary coordinate-tail
  profiles;
- the exact Collatz initial-prefix record criterion and an infinite family
  refuting the later-local-descent shortcut;
- uniform energy vanishing for every fixed-power sublinear Goldbach wheel;
- an exact Twin conditional-transfer identity and rare-event covariance
  countermodel.

TICKET-155는 finite core의 range exactness, Collatz initial-prefix 교정,
sublinear Goldbach wheel의 에너지 한계, Twin의 relative covariance
의무를 확정했다.

It does **not** establish an actual Weil positive Schur matrix, every-start
Collatz prefix descent, a binary Goldbach lower bound, or a shifted
cubic-rough relative covariance saving. No conjecture has been solved or
refuted.
