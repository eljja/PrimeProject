# TICKET84: Accessible 2-Adic Cycle and the Two-Thirds Log Delay Bound

## Claim boundary / 주장 경계

TICKET84 does **not** turn a negative 2-adic orbit into a natural-number counterexample. It uses that orbit only to generate exact finite valuation prefixes, then lifts those prefixes to positive ordinary Mersenne exponents. The result is a finite descent-delay lower bound, not divergence and not a Collatz proof or disproof.

TICKET84는 음의 2진 궤도를 자연수 반례라고 주장하지 않는다. 음의 궤도는 유한 valuation 접두 생성기로만 사용하고, 각 유한 접두를 양의 정수 메르센 지수로 들어 올린다. 결과는 유한 하강 지연의 하한이며 발산이나 콜라츠 증명·반증이 아니다.

## Why TICKET83 was not optimal / TICKET83의 한계

TICKET83 used the positive reference exponent `k=3`. Its post-block orbit reaches `1`, whose accelerated valuation is always `2`. The denominator precision therefore grows asymptotically as `2H`, producing the coefficient `1/2`.

고정 양의 기준 궤도는 결국 `1`에 도달하므로 평균 valuation이 `2`가 된다. 더 좋은 계수를 얻으려면 고정 양의 궤도를 반복하는 전략을 버리고, 더 낮은 평균 valuation을 갖는 completion-space 주기를 찾아야 한다.

## Accessible 2-adic exponent / 접근 가능한 2진 지수

Consider the odd 2-adic exponent `kappa` determined by

\[
3^\kappa=-13.
\]

This equation is solvable because odd powers of `3` modulo `2^Q` are exactly the residues congruent to `3 mod 8`, and `-13=3 mod 8`.

Its post-block value is

\[
x_0(\kappa)=\frac{3^\kappa-1}{2}=-7.
\]

Under the accelerated map,

\[
-7\xrightarrow{v_2=2}-5
\xrightarrow{v_2=1}-7.
\]

Thus the infinite valuation word is

\[
2,1,2,1,\ldots
\]

with mean valuation `3/2`. The negative cycle is a 2-adic proof object only.

## Exact finite lifts / 정확한 유한 lift

Let `d_H` be one plus the sum of the first `H` symbols of `2,1,2,1,...`. Explicitly,

\[
d_{2r}=1+3r,
\qquad
d_{2r+1}=3+3r.
\]

Set `Q_H=d_H+1`. There is a unique odd residue `r_H` modulo `2^(d_H-1)` satisfying

\[
3^{r_H}\equiv-13\pmod{2^{Q_H}}.
\]

It is constructed recursively. If `r` solves the equation modulo `2^Q`, exactly one of

\[
r,qquad r+2^{Q-2}
\]

solves it modulo `2^(Q+1)`. This is the discrete-log Hensel lift used by the audit.

Define the positive ordinary exponent

\[
k_H=r_H+2^{d_H-1}.
\]

Then

\[
2^{d_H-1}<k_H<2^{d_H},
\]

and its first `H` post-compensation valuations are exactly `2,1,2,1,...`. Only the finite residue is transferred; `kappa`, `-7`, and `-5` remain outside the positive natural domain.

## Symbolic growth / 기호 성장

For the lifted positive exponents,

\[
x_t(k)=A^{k+t}(2^k-1)=\frac{3^{k+t}+c_t}{2^{d_t}}.
\]

The affine constants obey

\[
c_{t+1}=3c_t+2^{d_t},
\qquad |c_t|<2^{2t+1}.
\]

The constant bound follows by induction because `d_t<=2t+1` and

\[
3\cdot2^{2t+1}+2^{2t+1}=2^{2t+3}.
\]

For `d>=4`,

\[
\left(\frac32\right)^{2^{d-1}+1}>2^{d+1}.
\]

The base `d=4` is `3^9>2^14`; the inequality propagates to the next `d` by squaring and dividing by `3/2`. Since `k_H>=2^(d_H-1)+1`, the multiplicative margin dominates both the denominator and the affine correction. Therefore

\[
x_t(k_H)>2^{k_H}-1
\qquad(0\le t\le H),
\]

and hence

\[
D(k_H)>H.
\]

## Two-thirds logarithmic bound / 3분의 2 로그 하한

Because `k_H<2^d_H` and

\[
d_H\le\frac32H+\frac32,
\]

we obtain

\[
\log_2 k_H<\frac32H+\frac32.
\]

Therefore

\[
\boxed{D(k_H)>H>\frac23\log_2 k_H-1.}
\]

Consequently every fixed `c<2/3` logarithmic Mersenne descent window fails on infinitely many positive exponents.

따라서 TICKET83의 계수 `1/2`는 최적이 아니며 `2/3`까지 엄밀하게 개선된다. 그러나 이 역시 최적 계수라고 주장하지 않는다.

## Next theorem / 다음 정리

The next target is `AccessibleCycleCoefficientSupremum`:

1. enumerate periodic accelerated valuation words;
2. solve the corresponding 2-adic cycles;
3. test whether each cycle lies in the exponent image `x=(3^kappa-1)/2`;
4. lift only finite prefixes to positive exponents;
5. maximize reciprocal mean valuation under these admissibility conditions.

평균 valuation이 더 작은 접근 가능한 주기가 존재하면 `2/3`보다 큰 하한 계수를 얻을 수 있다. 평균이 `log2(3)`에 접근한다면 가능한 계수는 `1/log2(3)` 근처까지 갈 수 있지만, 이는 아직 증명되지 않은 탐색 목표다.

## Machine audit / 계산 감사

- horizons: `H=2..256`;
- Hensel precisions: 384, through 386 bits;
- symbolic states: 33,150;
- lift, residue range, exact valuation, denominator, affine bound, growth, and logarithmic-bound failures: 0.

The theorem is symbolic for every `H>=2`; the finite audit verifies implementation consistency only.

## Literature and novelty / 문헌 및 새로움의 경계

The 2-adic conjugacy framework is established by Bernstein and Lagarias, [The 3x+1 Conjugacy Map](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13). Stopping-time and parity-vector methods go back to Terras, [A stopping time problem on the positive integers](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers).

PrimeProject claims only the accessible exponent-cycle construction, the explicit two-thirds logarithmic corollary, and the reproducible audit. Literature-wide novelty requires independent systematic review and peer review.
