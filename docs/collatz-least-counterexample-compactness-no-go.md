# TICKET80: Least-Counterexample Finite-Prefix Compactness No-Go

## Claim boundary / 주장 경계

TICKET80 does **not** prove or disprove the Collatz conjecture. It proves that a least-counterexample argument using only finitely many prefix non-descent inequalities and exact 2-adic cylinders cannot produce a contradiction, regardless of the finite horizon or prescribed finite lower bound.

TICKET80은 콜라츠 추측을 증명하거나 반증하지 않는다. 최소 반례의 유한 접두 비감소 부등식과 정확한 2진 cylinder만 사용하는 논증은 깊이와 유한 하한을 아무리 키워도 모순을 만들 수 없다는 제한적 no-go 정리다.

## Necessary condition / 최소 반례의 필요조건

Let the accelerated odd Collatz map be

\[
A(n)=\frac{3n+1}{2^{v_2(3n+1)}}.
\]

If a least positive counterexample `N` exists, then every accelerated iterate must satisfy

\[
A^j(N)\ge N.
\]

Otherwise an iterate below `N` converges by minimality, forcing `N` to converge as well. For a valuation prefix with total valuation `S_j` and affine constant `C_j`, this is equivalent to

\[
2^{S_j}N\le 3^jN+C_j.
\]

이 부등식은 최소 반례의 필요조건이지만 충분조건은 아니다. 유한 구간 동안 시작값 아래로 내려가지 않았다는 사실만으로 그 수가 실제 반례가 되지는 않는다.

## Exact finite witnesses / 정확한 유한 증인

For every finite horizon `H>=1` and every lower bound `B>=1`, choose

\[
q=\left\lceil\frac{B+1}{2^{H+1}}\right\rceil,
\qquad n=2^{H+1}q-1.
\]

Then `n>=B`, and for every `0<=j<=H`,

\[
A^j(n)=3^j2^{H+1-j}q-1.
\]

Consequently:

\[
v_2(3A^j(n)+1)=1\quad(0\le j<H),
\]

and, for `1<=j<=H`,

\[
A^j(n)>n
\]

because `3^j>2^j`. The exact cylinder is

\[
n\equiv-1\pmod{2^{H+1}},
\]

and the all-ones affine constant is `C_j=3^j-2^j`.

따라서 어떤 유한 검증 하한 `B`를 선택해도 그 위에서 최소반례의 유한 접두 비감소 필요조건을 모두 만족하는 양의 정수를 만들 수 있다. 이 수들은 실제 반례가 아니라 유한 필요조건에 대한 반례 오라클이다.

## Theorem / 정리

Every finite subsystem consisting of:

- exact accelerated valuation-cylinder congruences;
- prefix non-descent inequalities required of a least counterexample;
- an arbitrary finite lower bound on the starting integer;

has a positive-integer solution. Therefore no contradiction can be obtained from a fixed finite truncation of only these constraints.

위 세 종류의 조건으로 이루어진 모든 유한 부분계는 양의 정수 해를 갖는다. 따라서 이 조건들만 유한하게 절단해 최소 반례의 부재를 증명할 수 없다.

## Dual-topology escape / 두 위상에서의 이탈

Set

\[
x_H=2^{H+1}-1.
\]

Then

\[
x_H\to+\infty
\]

in the ordinary Archimedean topology, while

\[
v_2(x_H+1)=H+1
\]

implies

\[
x_H\to-1
\]

in `Z_2`. Moreover `A(-1)=-1` with valuation 1. Thus 2-adic compactness extracts the nonpositive fixed point `-1`, not a positive Collatz counterexample.

양의 정수 증인들은 실수 크기로는 무한대로 도망가지만 2진 위상에서는 `-1`로 수렴한다. 그러므로 “모든 유한 깊이에 해가 있으니 compactness로 양의 무한 해를 얻는다”는 추론은 잘못이다.

## Positive-integer stabilization criterion / 양의 정수 안정화 판정

Consider nested compatible cylinders whose moduli tend to infinity, and let `r_H` be their least nonnegative residues. Their 2-adic limit is a positive ordinary integer if and only if `r_H` is eventually constant at one positive value.

- If the limit is the positive integer `n`, every modulus larger than `n` has least residue `n`.
- If the least residues eventually equal `n>0`, compatibility identifies the 2-adic limit with that ordinary integer.

중첩 cylinder의 최소 비음수 residue가 결국 하나의 양의 정수로 고정되어야만 그 극한을 자연수로 승격할 수 있다. 단순한 2진 수렴만으로는 부족하다.

## Discarded routes / 폐기할 경로

- finite non-descent prefix contradiction;
- increasing a finite verified lower bound and repeating the same prefix search;
- promoting finite satisfiability to a positive counterexample by 2-adic compactness alone;
- treating `-1` or another nonpositive 2-adic completion as a natural-number orbit.

## Retained route / 유지할 경로

A valid least-counterexample proof must track one fixed ordinary integer through all horizons and produce at least one of the following:

- a horizon-independent Archimedean upper bound `N<=U` overlapping a certified finite verification range;
- eventual stabilization of the least cylinder residue at one positive value plus a separate contradiction;
- a decisive valuation-surplus prefix forcing an iterate below `N`.

다음 목표는 `LeastCounterexampleUniformHeightBound`다. 모든 접두 제약을 동시에 만족하는 하나의 고정된 양의 정수 `N`에 대해 horizon과 무관한 명시적 상한을 도출해야 한다. 단, “모든 안정화된 양의 정수 경로가 결국 시작값 아래로 내려간다”는 명제는 coefficient-stopping-time 형태의 콜라츠 추측과 동치이므로 중간 성과로 가장해서는 안 된다.

## Machine audit / 계산 감사

- horizons: `1..512`;
- lower-bound regimes: 5, including `2^68`, `2^128`, and `10^100` as synthetic stress bounds;
- finite witness cases: 2,560;
- accelerated step replays: 656,640;
- lower-bound, residue, formula, valuation, non-descent, affine-inequality failures: 0;
- dual-topology and `-1` fixed-point failures: 0.

The audit validates the implementation. The theorem follows from the displayed exact formulas for arbitrary `H` and `B`, not from stopping at 512.

계산은 구현을 감사할 뿐이며, 정리는 임의의 `H,B`에 대한 기호식으로 증명된다.

## Literature and novelty / 문헌 및 새로움의 경계

Finite parity-prefix realizability and 2-adic conjugacy are established; see Bernstein and Lagarias, [The 3x+1 Conjugacy Map](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13). Recent finite parity-vector and paradoxical-sequence results are discussed by Niu, [Parity vectors and paradoxical sequences in the accelerated Collatz map](https://arxiv.org/abs/2605.13886). Tao's [almost-all theorem](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/almost-all-orbits-of-the-collatz-map-attain-almost-bounded-values/1008CC2DF91AF87F66D190C5E01C907F) remains distinct from an all-integer result.

PrimeProject does not claim those principles as new. The project-specific contribution is the explicit least-counterexample finite-satisfiability no-go, the residue-stabilization guard, the dual-topology audit, and their integration with TICKET78-79.
