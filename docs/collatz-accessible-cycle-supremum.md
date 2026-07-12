# TICKET85: Accessible Cycle Coefficient Supremum

## Claim boundary / 주장 경계

TICKET85 proves a restricted optimization theorem for Mersenne post-expansion delay. It does not prove divergence, a universal Mersenne upper bound, or the Collatz conjecture.

TICKET85는 메르센 post-expansion 하강 지연의 제한적 최적화 정리다. 발산, 모든 메르센 지수의 상한, 콜라츠 추측을 증명하지 않는다.

## Accessible cycle family / 접근 가능한 주기 계열

For every `m>=2`, consider the valuation word

\[
w_m=(2,\underbrace{1,\ldots,1}_{m-1}).
\]

Its total valuation is `S_m=m+1`. The affine composition has constant

\[
C_m=5\cdot3^{m-1}-2^{m+1}
\]

and fixed point

\[
x_m=\frac{C_m}{2^{m+1}-3^m}.
\]

Let `y_m=(3x_m+1)/4`. Direct algebra gives

\[
y_m+1=\frac{2^m}{2^{m+1}-3^m}.
\]

The denominator is odd, so `v_2(y_m+1)=m`. Therefore the first valuation is exactly `2` and the following `m-1` valuations are exactly `1`. Thus `w_m` is an exact periodic accelerated word.

또한 `x_m=1 mod 8`이므로 `2x_m+1=3 mod 16`이다. 따라서 이 cycle은 홀수 2진 exponent image `x=(3^kappa-1)/2`에 접근 가능하다.

## Exact supremum / 정확한 supremum

The mean valuation and reciprocal mean are

\[
\overline a_m=\frac{m+1}{m},
\qquad
\alpha_m=\frac{m}{m+1}.
\]

Hence `alpha_m` approaches `1` from below. Conversely every accelerated valuation is at least one, so every finite word has reciprocal mean at most one. Therefore

\[
\boxed{\sup\alpha=1.}
\]

The supremum is not attained. Mean valuation one requires the all-ones word. Its cycle is `x=-1`, whose exponent target is `2x+1=-1=7 mod 8`; odd powers of `3` are `3 mod 8`. Thus the all-ones cycle is outside the exponent image.

supremum `1`은 정확하지만 유한한 접근 가능 주기에서는 달성되지 않는다. 이는 TICKET84의 `2/3`이 최적이 아니었음을 완전히 판정한다.

## Unit-log delay construction / 계수 1 로그 지연 구성

For each horizon `H>=2`, choose the cycle length `m=H`. Lift the target `2x_H+1` through precision `H+3` and let `r_H` be the unique odd exponent residue modulo `2^(H+1)`. Set

\[
k_H=r_H+2^{H+1}.
\]

Then

\[
2^{H+1}<k_H<2^{H+2}.
\]

The exact finite prefix is preserved, and the symbolic growth bounds from TICKET84 imply

\[
D(k_H)>H.
\]

Since `k_H<2^(H+2)`,

\[
\boxed{D(k_H)>H>\log_2 k_H-2.}
\]

Consequently every window `c log2(k)+C` with fixed `c<1` and arbitrary fixed `C` fails on infinitely many positive Mersenne exponents.

이는 coefficient-one보다 작은 모든 로그 창을 폐기하지만 `log2(k)+O(1)` 상한 자체를 반박하지는 않는다.

## Next target / 다음 목표

`CoefficientOneBoundary` must separate two questions:

1. improve the additive loss in explicit lower bounds `D(k)>=log2(k)-B(k)`;
2. prove or refute a universal Mersenne upper bound `D(k)<=log2(k)+O(1)`.

The lower construction gives no divergence statement. A trajectory may descend immediately after the certified prefix.

## Machine audit / 계산 감사

- horizons and cycle lengths: `2..256`;
- cases: 255;
- Hensel lift steps: 32,895;
- maximum precision: 259 bits;
- symbolic states: 33,150;
- failures: 0.

The finite audit checks the implementation. The family formulas and inequalities prove the result for arbitrary `H>=2`.

## Novelty boundary / 새로움의 경계

Finite parity words and 2-adic exponent lifting use established Collatz machinery. PrimeProject claims the explicit accessible cycle family, exact supremum corollary, coefficient-one-minus-two delay construction, and reproducible audit. Independent literature review and peer review remain necessary before a broader novelty claim.
