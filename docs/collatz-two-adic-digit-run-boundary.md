# TICKET87: Two-Adic Digit Runs and the Additive-One Boundary

## Claim boundary / 주장 경계

TICKET87 proves that the Mersenne post-expansion descent delay exceeds `log2(k)+1` for infinitely many positive exponents. It does **not** construct a divergent positive orbit and does not prove or disprove the Collatz conjecture.

TICKET87은 메르센 초기 팽창 뒤의 하강 지연이 `log2(k)+1`보다 큰 양의 지수가 무한히 존재함을 증명한다. 양의 발산 궤도나 콜라츠 추측 자체를 증명하지 않는다.

## Fixed 2-adic exponent / 고정된 2진 지수

TICKET86 reduced every horizon target to one nested exponent `r` satisfying

\[
3^{r+1}=-7
\]

in the 2-adic exponent image. Writing `a=(r+1)/2` gives

\[
9^a=-7,
\qquad
a=\frac{\log_{2\text{-adic}}(-7)}{\log_{2\text{-adic}}(9)}
=\frac{\log(1-8)}{\log(1+8)}.
\]

This identity provides an efficient independent computation of the binary prefix; the infinite proof below does not depend on observed digit frequencies.

이 항등식은 Hensel lift와 독립적인 접두 계산법이다. 계산된 비트의 빈도를 무한 정리의 근거로 사용하지 않는다.

## Exact run identity / 정확한 run 항등식

Let `H<J` be consecutive heights at which the nested least residue gains a new top bit, and set `k=r_H`. Then

\[
2^H\le k<2^{H+1}.
\]

The same residue remains valid at the intervening heights. Exactly,

\[
v_2(3^{k+1}+7)=J+2,
\]

and the number of zero lift bits between the two top bits is

\[
L=J-H-1.
\]

따라서 이진 0비트 연속 길이는 휴리스틱 값이 아니라 하나의 정수에 대한 정확한 2진 valuation이다.

## Both digits occur infinitely often / 두 비트의 무한 출현

The one bits occur infinitely often by TICKET86. Otherwise the least residues stabilize at a nonnegative integer `r`, and divisibility by every power of two forces the impossible ordinary equality `3^(r+1)=-7`.

The zero bits also occur infinitely often. If only finitely many zero bits occurred, the 2-adic binary expansion would eventually consist entirely of ones. Such a 2-adic integer is a negative ordinary integer `R`. The continuous exponent equation would then become

\[
3^{R+1}=-7
\]

as an equality in the rationals embedded in `Q_2`. If `R+1>=0`, the left side is positive. If `R+1<0`, clearing the positive power of three gives `1=-7*3^m`. Both are impossible.

Hence both digits occur infinitely often. A binary sequence with infinitely many zeros and ones has infinitely many transitions `1 -> 0`.

0과 1이 모두 무한히 나타나므로 `1→0` 전환도 무한히 많다. 이 부분은 통계적 정상성이나 무작위성 가정을 사용하지 않는다.

## Growth through a zero run / 0비트 구간의 성장

For a zero run of length `L` after height `H`, the same positive exponent `k` preserves the exact valuation prefix through `H+L`. The affine state bounds from TICKET86 remain valid through

\[
U=\min(L,k-H-2).
\]

Thus

\[
D(k)>H+U.
\]

Since `D(k)` is integral and `log2(k)<H+1`,

\[
D(k)-\log_2 k>U.
\]

At every sufficiently large `1 -> 0` transition, `L>=1` and `k-H-2>=1`, so `U>=1`.

## Restricted theorem / 제한 정리

There are infinitely many positive odd exponents `k` satisfying

\[
\boxed{D(k)>\log_2 k+1.}
\]

This refutes the universal Mersenne bound `D(k)<=log2(k)+1`. It does not refute `D(k)<=log2(k)+C` for some larger constant and does not imply divergence.

즉 가산상수 1의 보편 상한까지 무한 부분수열에서 반박했다. 더 큰 모든 상수를 반박하려면 긴 0비트 run의 무한 반복을 별도로 증명해야 한다.

## Finite high-precision audit / 고정밀 유한 감사

The independent 2-adic logarithm computation audits 262,144 lift bits. It cross-checks the first 1,024 horizons against the bit-by-bit Hensel implementation. The longest observed zero run has length 16 and begins at `H=38326`, producing one exact finite certificate with

\[
D(k)-\log_2 k>16.
\]

This record is finite evidence only. It does not prove unbounded run length or binary normality.

262,144비트 감사에서 길이 16의 기록을 찾았지만, 이를 무한 비유계성으로 해석하지 않는다.

## Next theorem / 다음 정리

The next target is `TwoAdicRunLengthTwoInfinitude`: prove that the pattern `100` occurs infinitely often in the fixed exponent, or derive an exact obstruction. Success would yield infinitely many exponents with `D(k)>log2(k)+2`. Unbounded additive excess requires a hierarchy of fixed-run recurrence theorems or an unbounded-run theorem.

다음에는 길이 2의 0비트 run이 무한히 반복되는지를 먼저 공격한다. 유한 prefix에서 많이 보인다는 사실만으로는 충분하지 않다.

## Literature and novelty boundary / 문헌과 새로움의 경계

The 2-adic conjugacy and stopping-time frameworks are established in Bernstein-Lagarias and Terras, and Mersenne starts are discussed by Sinyor. PrimeProject treats only the two-sided digit-infinitude reduction and additive-one corollary as candidate results pending systematic literature review and independent verification.

- Daniel J. Bernstein and Jeffrey C. Lagarias, [The 3x+1 Conjugacy Map](https://doi.org/10.4153/CJM-1996-060-x).
- Riho Terras, [A stopping time problem on the positive integers](https://doi.org/10.4064/aa-30-3-241-252).
- Joseph Sinyor, [The 3x+1 Problem as a String Rewriting System](https://doi.org/10.1155/2010/458563).
