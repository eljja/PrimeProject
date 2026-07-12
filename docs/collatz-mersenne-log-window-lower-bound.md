# TICKET83: Mersenne Half-Log Delay Lower Bound

## Claim boundary / 주장 경계

TICKET83 does **not** prove divergence and does not solve Collatz. It quantifies the TICKET82 obstruction: on an explicit infinite sequence of Mersenne exponents, the number of accelerated post-expansion steps required before descent can grow at least as one half of the binary logarithm of the exponent.

TICKET83은 발산이나 콜라츠 추측을 증명하지 않는다. TICKET82의 고정 창 반박을 정량화하여, 명시적인 메르센 지수 부분수열에서 시작값 아래 하강에 필요한 post-expansion 단계가 최소한 지수의 이진 로그 절반 규모까지 커질 수 있음을 증명한다.

## Delay definition / 지연 정의

Let `N_k=2^k-1` and define

\[
D(k)=\min\{t\ge0:A^{k+t}(N_k)<N_k\},
\]

with `D(k)=infinity` if the set is empty. The first `k-1` expansion steps are not counted in `D`; `t=0` is the first post-expansion compensation value from TICKET81.

`D(k)`는 전체 stopping time이 아니라 초기 메르센 팽창이 끝난 뒤 시작값 아래로 내려갈 때까지의 추가 accelerated-step 지연이다.

## Explicit sequence / 명시적 지수 수열

For every `H>=2`, set

\[
k_H=3+2^{2H+3}.
\]

Then

\[
k_H\equiv3\pmod{2^{2H+3}}.
\]

TICKET82 therefore preserves the exact post-compensation valuation word

\[
3,4,\underbrace{2,\ldots,2}_{H-2\text{ entries}}
\]

through post-index `H`.

## Symbolic bounds / 기호 상계

The preserved iterates are

\[
x_t(k)=A^{k+t}(N_k)=\frac{3^{k+t}+c_t}{2^{d_t}},
\]

where

\[
d_0=1,\quad d_1=4,\quad d_t=2t+4\quad(t\ge2).
\]

The constants satisfy

\[
|c_t|<2^{d_t}.
\]

The cases `t=0,1,2` are direct. For `t>=2`, `c_t` is positive and

\[
c_{t+1}=3c_t+2^{d_t}<4\cdot2^{d_t}=2^{d_t+2}=2^{d_{t+1}}.
\]

Thus for every `t<=H`, `d_t<=2H+4` and the additive affine correction is strictly smaller than its denominator power.

## Growth inequality / 성장 부등식

For `H>=2`,

\[
k_H\ge4H+11.
\]

Also

\[
\left(\frac32\right)^4>2^2,
\qquad
\left(\frac32\right)^{11}>2^5.
\]

Therefore

\[
\left(\frac32\right)^{k_H}
\ge\left(\frac32\right)^{4H+11}
>2^{2H+5}
\ge2^{d_t+1}.
\]

It follows that

\[
3^{k_H+t}>2^{k_H+d_t}+|c_t|,
\]

so

\[
x_t(k_H)>2^{k_H}>N_{k_H}
\qquad(0\le t\le H).
\]

Hence

\[
D(k_H)>H.
\]

이 과정은 거대한 `3^k`를 계산한 것이 아니라, 정수 지수 부등식과 기호 상수 상계로 모든 `H>=2`를 처리한 것이다.

## Half-log theorem / 절반 로그 정리

Since

\[
k_H=3+2^{2H+3}<2^{2H+4},
\]

we have

\[
H>\frac12\log_2 k_H-2.
\]

Combining the inequalities gives

\[
\boxed{D(k_H)>H>\frac12\log_2 k_H-2.}
\]

Consequences:

- every universal Mersenne window `L(k)=o(log k)` fails on infinitely many `k_H`;
- every fixed `c<1/2` window `L(k)<=c log2(k)` eventually fails on this sequence;
- a successful universal Mersenne descent window must operate at least at logarithmic scale on this obstruction family.

따라서 단순히 상수 창을 버리는 것으로 부족하다. `log k`보다 느린 모든 증가 창과 계수 `1/2` 미만의 로그 창도 무한 부분수열에서 실패한다.

## What remains open / 남은 문제

The coefficient `1/2` is a certified lower coefficient produced by the reference word `3,4,2,2,...`; it is not claimed optimal. The next target is `MersenneLogWindowDichotomy`:

1. optimize the delayed-prefix construction to improve the lower coefficient `alpha`;
2. determine whether any finite `beta` satisfies `D(k)<=beta log2(k)+O(1)` for every Mersenne exponent that eventually descends;
3. keep lower-delay theorems separate from divergence and upper-descent theorems.

계수 `1/2`의 최적성은 아직 모른다. 더 낮은 평균 valuation을 갖는 지수 접두를 구성하면 하한 계수를 높일 가능성이 있다. 반대로 모든 메르센 지수에 대한 유한 로그 상한은 훨씬 강한 미해결 목표다.

## Machine audit / 계산 감사

- horizons: `H=2..256`;
- horizon cases: 255;
- symbolic states: 33,150;
- progression, denominator, constant, prefix, growth, and logarithmic-bound failures: 0.

The audit checks the algebraic contract. The theorem follows from the exact formulas and inequalities for arbitrary `H>=2`, not from the finite maximum 256.

감사는 구현 일치성을 확인한다. 정리의 무한 범위는 기호 증명에서 나오며 256까지의 실행에서 나오지 않는다.

## Literature and novelty / 문헌 및 새로움의 경계

Stopping-time and parity-prefix methods are established by Terras, [A stopping time problem on the positive integers](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers). Modern logarithmic-scale context includes Inselmann, [An approximation of the Collatz map and a lower bound for the average total stopping time](https://arxiv.org/abs/2402.03276). The 2-adic prefix framework used by TICKET82 comes from Bernstein and Lagarias, [The 3x+1 Conjugacy Map](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13).

PrimeProject claims only the explicit `k_H` quantitative corollary, its half-log no-go interpretation, and reproducible audit. A claim of literature-wide novelty requires independent systematic review and peer review.
