# TICKET82: Fixed Mersenne Compensation-Window No-Go

## Claim boundary / 주장 경계

TICKET82 does **not** prove or disprove the Collatz conjecture and does not construct a divergent orbit. It proves that no exponent-independent finite number of accelerated steps after the initial Mersenne expansion can force descent for every Mersenne start.

TICKET82는 콜라츠 추측을 증명하거나 반증하지 않으며 발산 궤도도 만들지 않는다. 메르센 시작값의 초기 팽창 뒤에 상수 길이만큼 미래를 확인하는 방식으로는 모든 메르센 시작값의 하강을 강제할 수 없다는 제한 정리다.

## Setup / 설정

Use the accelerated odd Collatz map

\[
A(n)=\frac{3n+1}{2^{v_2(3n+1)}}
\]

and the Mersenne starts `N_k=2^k-1`. TICKET81 proved that, for odd `k`,

\[
x_0(k):=A^k(N_k)=\frac{3^k-1}{2}.
\]

For `t>=0`, write

\[
x_t(k):=A^{k+t}(N_k).
\]

TICKET81은 첫 보상 단계 하나가 충분하지 않음을 보였다. 이번 질문은 더 강하다. `H`를 하나의 상수로 고정했을 때 `x_0(k),...,x_H(k)` 중 하나가 모든 지수 `k`에서 반드시 시작값 아래로 내려가는가? 답은 아니다.

## Symbolic family / 기호 계열

Fix the reference exponent `k_0=3`. Its first post-compensation value is

\[
x_0(3)=13,
\]

and the accelerated path begins

\[
13\xrightarrow{v_2=3}5\xrightarrow{v_2=4}1
\xrightarrow{v_2=2}1\xrightarrow{v_2=2}\cdots.
\]

Thus the additional post-compensation valuation word is

\[
b_1=3,\qquad b_2=4,\qquad b_t=2\quad(t\ge3).
\]

For every exponent `k` realizing this finite word, induction gives

\[
x_t(k)=\frac{3^{k+t}+c_t}{2^{d_t}},
\]

where

\[
c_0=-1,\quad d_0=1,
\]

and

\[
c_{t+1}=3c_t+2^{d_t},
\qquad d_{t+1}=d_t+b_{t+1}.
\]

In particular,

\[
d_1=4,\quad d_2=8,\quad d_t=2t+4\quad(t\ge2).
\]

이 식은 수치 회귀가 아니라 accelerated map을 한 단계 대입하여 얻는 정확한 귀납식이다.

## Finite-prefix preservation / 유한 접두 보존

For `Q>=3`, the multiplicative order of `3` modulo `2^Q` is `2^{Q-2}`. Therefore

\[
k\equiv3\pmod{2^{Q-2}}
\]

implies

\[
3^{k+t}\equiv3^{3+t}\pmod{2^Q}
\]

for every fixed `t`.

To preserve exact numerator valuations through post-index `H`, it is enough to retain one bit beyond the largest denominator exponent:

\[
Q_H=\max_{0\le t\le H}(d_t+1).
\]

Hence the explicit exponent progressions are

\[
\begin{array}{ll}
H=0:&k\equiv3\pmod2,\\
H=1:&k\equiv3\pmod8,\\
H\ge2:&k\equiv3\pmod{2^{2H+3}}.
\end{array}
\]

Every exponent in the relevant progression has exactly the same post-compensation valuation prefix through `H` as the reference exponent.

중요한 점은 단순히 parity가 같다는 것이 아니다. 분자 `3^{k+t}+c_t`를 `2^{d_t+1}`까지 보존하므로 valuation이 정확히 `d_t`이고, 더 큰 2의 거듭제곱으로 나누어지는 경우도 배제한다.

## Archimedean escape / 실수 크기 방향의 이탈

For each fixed `t`, the constants `c_t,d_t` do not depend on `k`. A sufficient condition for `x_t(k)>N_k` is

\[
3^{k+t}>2^{k+d_t}+|c_t|.
\]

This condition holds for all sufficiently large `k` because `(3/2)^k` tends to infinity. It is also persistent: if it holds at `k`, then multiplication of the left side by `3` and the leading right side by `2` makes it hold at `k+1`.

For a fixed `H`, take the maximum of the finitely many thresholds for `0<=t<=H`. Every sufficiently large exponent in the explicit progression then satisfies

\[
x_t(k)>N_k\qquad(0\le t\le H).
\]

`H`가 고정되어 있으므로 임계값도 유한하다. 해당 합동류에는 임계값보다 큰 지수가 무한히 많으므로 무한 반례 계열이 얻어진다.

## Theorem / 정리

For every fixed integer `H>=0`, infinitely many odd exponents `k` satisfy

\[
A^{k+t}(2^k-1)>2^k-1
\qquad\text{for every }0\le t\le H.
\]

Consequently, the post-expansion stopping delay of Mersenne starts is unbounded. No constant compensation-window length can prove descent for all Mersenne starts.

모든 고정 `H`에 대해 첫 보상 이후 `H`단계 동안 시작값 아래로 내려가지 않는 메르센 시작값이 무한히 많다. 따라서 메르센 계열만 보더라도 필요한 미래 관찰 길이는 상수로 제한될 수 없다.

## What is rejected / 폐기되는 경로

- 첫 보상 대신 2단계, 10단계, 또는 임의의 고정 단계만 더 보면 항상 하강한다는 주장;
- 유한 parity/valuation 접두를 모든 메르센 지수의 전역 거동으로 승격하는 주장;
- bounded lookahead만으로 최소 반례 모순을 만들려는 주장.

This is an infinite symbolic obstruction, not a finite computational counterexample list.

이는 유한 범위에서 실패 사례를 모은 결과가 아니라 모든 고정 `H`에 적용되는 무한 합동류 구성이다.

## Retained route / 유지하는 경로

The next admissible theorem is `MersenneGrowingWindowDescent`: construct an explicit unbounded `L(k)` and prove

\[
\min_{0\le t\le L(k)}A^{k+t}(2^k-1)<2^k-1.
\]

The useful questions are now quantitative:

- what lower bound on `L(k)` is forced by finite-prefix replication;
- whether a sublinear, linear, or larger upper bound can be proved;
- whether cumulative valuation surplus can be controlled without importing empirical stopping times.

다음 단계에서는 고정 길이를 더 이상 후보로 사용하지 않는다. 지수에 따라 증가하는 `L(k)`의 하한과 상한을 분리하여 공격해야 한다.

## Machine audit / 계산 감사

- post horizons: `H=0..128`;
- horizon cases: 129;
- symbolic states checked: 8,385;
- transition conditions checked: 8,256;
- congruence, formula, valuation-word, progression, and growth-guard failures: 0.

At `H=128`, the exact progression is `k=3 mod 2^259`; the first stored certified exponent is enormous because the theorem constructs sparse arithmetic progressions. No integer of size `2^k` is materialized. Modular exponentiation verifies the exact valuation conditions, while the displayed integer inequality certifies eventual dominance.

`H=128`의 거대한 지수는 실용적인 콜라츠 계산 범위를 뜻하지 않는다. 정리의 무한성과 합동류의 희소성을 투명하게 보여 주는 기호 인증 값이다.

## Literature and novelty / 문헌 및 새로움의 경계

Finite parity-prefix and stopping-time methods are established in Terras, [A stopping time problem on the positive integers](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers). The 2-adic conjugacy and finite-prefix framework are established by Bernstein and Lagarias, [The 3x+1 Conjugacy Map](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13). See also Lagarias, [The 3x+1 Problem: An Overview](https://arxiv.org/abs/2111.02635).

PrimeProject does not claim those principles as new. The project-specific result is the explicit Mersenne-exponent progression corollary, its fixed-window no-go interpretation, and the reproducible symbolic audit. A claim that the corollary itself is absent from all prior literature requires a dedicated systematic review and peer review.

유한 parity 접두와 2진 연속성 자체는 기존 이론이다. 프로젝트는 이를 메르센 지수 합동류에 적용한 명시적 귀결과 증명 경로 제거만 주장한다.
