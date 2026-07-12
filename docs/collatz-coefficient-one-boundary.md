# TICKET86: Infinite Coefficient-One Mersenne Delay

## Claim boundary / 주장 경계

TICKET86 proves an infinite-subsequence theorem about the descent delay of Mersenne starts. It does **not** prove that any positive Collatz orbit diverges, and it does not prove the Collatz conjecture.

TICKET86은 메르센 시작값의 하강 지연에 관한 무한 부분수열 정리만 증명한다. 양의 콜라츠 궤도의 발산도, 콜라츠 추측도 증명하지 않는다.

## What changed after TICKET85 / TICKET85 이후의 변화

TICKET85 used the positive exponent

\[
k_H=r_H+2^{H+1},
\]

which always lies below `2^(H+2)`. This guaranteed growth but lost two additive units:

\[
D(k_H)>H>\log_2 k_H-2.
\]

TICKET86 asks when the least positive residue `r_H` itself is already large enough. The answer is: not at every audited height, but at infinitely many rigorously defined top-bit heights.

TICKET85는 안전하게 양의 지수를 만들기 위해 잉여류에 주기 하나를 더했다. TICKET86은 그 추가 주기를 제거할 수 있는 높이를 찾는다. 모든 높이라고 주장하지 않고, 새 최상위 비트가 생기는 무한히 많은 높이만 사용한다.

## Exact reduction / 정확한 환원

For the accessible cycle word `w_H=(2,1,...,1)`, the exponent target is

\[
\tau_H=\frac{7\cdot3^{H-1}-2^{H+1}}{2^{H+1}-3^H}.
\]

The least odd residue `r_H` is defined modulo `2^(H+1)` by

\[
3^{r_H}\equiv\tau_H\pmod {2^{H+3}}.
\]

After clearing the odd denominator, the difference is

\[
2^{H+1}(3^{r_H}+1)-3^{H-1}(3^{r_H+1}+7).
\]

Because `r_H` is odd, `3^r_H+1` is divisible by `4`. The first term therefore vanishes modulo `2^(H+3)`, and the odd factor `3^(H-1)` is invertible. Hence

\[
\boxed{3^{r_H+1}\equiv-7\pmod {2^{H+3}}.}
\]

복잡해 보이던 주기점의 유리수 목표는 높이와 무관한 하나의 2진 이산로그로 축약된다. 이 항등식이 TICKET86의 핵심이다.

## Infinite top-bit lemma / 최상위 비트 무한성 보조정리

Uniqueness of the lift gives

\[
r_{H+1}\in\{r_H,\ r_H+2^{H+1}\}.
\]

Suppose the second alternative occurred only finitely often. Then `r_H` would eventually stabilize at an ordinary positive integer `r`. The reduced congruence would imply

\[
2^{H+3}\mid 3^{r+1}+7
\]

for arbitrarily large `H`. A fixed nonzero positive integer cannot be divisible by arbitrarily high powers of two. Equivalently, stabilization would force the impossible integer equality `3^(r+1)=-7`.

Therefore the top bit is added infinitely often. At every such height,

\[
2^H\le r_H<2^{H+1}.
\]

즉 유한 계산에서 비트가 자주 나타난다는 관찰을 무한성의 근거로 쓰지 않는다. 잉여류가 안정될 경우 생기는 정수론적 모순으로 무한성을 증명한다.

## Growth lemma / 성장 보조정리

For `0<=t<=H`, the exact accelerated state has the affine form

\[
x_t(k)=\frac{3^{k+t}+c_t}{2^{d_t}},
\qquad d_t\le t+2,
\qquad |c_t|<2^{2t+1}.
\]

At a top-bit height set `k=r_H`. Since `H>=2`, `k>=2^H`, and `t<=H`,

\[
\left(\frac32\right)^{k+t}\ge\left(\frac32\right)^4=\frac{81}{16}
>\frac92
\ge 4+2^{t+1-k}.
\]

Thus

\[
3^{k+t}>2^{k+t+2}+2^{2t+1},
\]

and the affine lower bound gives

\[
x_t(k)>2^k>2^k-1
\qquad(0\le t\le H).
\]

Therefore `D(k)>H`.

## Restricted theorem / 제한 정리

There are infinitely many positive odd exponents `k` such that

\[
2^H\le k<2^{H+1}
\quad\text{and}\quad
D(k)>H.
\]

Since `D(k)` is an integer,

\[
\boxed{D(k)\ge H+1>\log_2 k}
\]

for infinitely many `k`.

따라서 모든 메르센 지수에 대해 `D(k)<=log2(k)`라고 하는 계수 1, 가산상수 0의 보편 상한은 거짓이다. 그러나 `D(k)<=log2(k)+C`인 어떤 양의 상수 `C`의 존재까지 반박한 것은 아니다.

## What remains open / 남은 장벽

The next question is controlled by ordinary binary runs in the fixed 2-adic exponent solving `3^(r+1)=-7`:

1. Can usable zero runs be proved unbounded?
2. Can the affine growth estimate remain valid through those runs?
3. Would this force `D(k)-log2(k)` to be unbounded?

This is the `TwoAdicDigitRunBoundary`. Treating the first 1,023 audited prefixes as an infinite proof is explicitly rejected.

다음 단계는 2진 지수의 0비트 연속 구간과 실제 성장 구간을 연결하는 것이다. 이 연결을 증명해야만 임의의 고정 가산상수까지 넘어설 수 있다.

## Machine audit / 계산 감사

The generated artifact checks nested lifts and both congruence forms through `H=1024`, and checks exact symbolic valuation states at top-bit heights through `H=256`. These checks validate the implementation; the infinite theorem rests on the algebraic proof above.

생성 데이터는 `H=1024`까지 중첩 lift와 두 합동식의 일치를, `H=256`까지 최상위 비트 높이의 기호 valuation 상태를 검사한다. 계산은 증명의 대체물이 아니라 구현 감사다.

## Novelty boundary / 새로움의 경계

PrimeProject records the exact reduction and infinite-subsequence corollary as a candidate result. A systematic literature search, independent proof checking, and peer review are required before any novelty or publication claim.

The surrounding framework is not new: Bernstein and Lagarias developed the 2-adic conjugacy, Terras established the stopping-time framework, and Sinyor explicitly discusses Mersenne starts and the identity connecting `2^k-1` to `3^k-1`. TICKET86 claims only the narrower fixed-log reduction and its restricted corollary, subject to independent comparison with that literature.

- Daniel J. Bernstein and Jeffrey C. Lagarias, [The 3x+1 Conjugacy Map](https://doi.org/10.4153/CJM-1996-060-x), *Canadian Journal of Mathematics* 48 (1996), 1154-1169.
- Riho Terras, [A stopping time problem on the positive integers](https://doi.org/10.4064/aa-30-3-241-252), *Acta Arithmetica* 30 (1976), 241-252.
- Joseph Sinyor, [The 3x+1 Problem as a String Rewriting System](https://doi.org/10.1155/2010/458563), *International Journal of Mathematics and Mathematical Sciences* (2010).

주변 도구 자체는 새롭지 않다. 2진 공액, stopping time, 메르센 시작값의 초기 성장은 선행 연구에 있다. TICKET86이 독립 검토 대상으로 남기는 것은 고정 이산로그 환원과 그 제한적 귀결뿐이다.
