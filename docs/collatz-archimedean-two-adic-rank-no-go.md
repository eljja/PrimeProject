# TICKET79: Archimedean-Two-Adic One-Step Rank No-Go

## Claim boundary / 주장 경계

TICKET79 does **not** prove or disprove the Collatz conjecture. It proves a restricted no-go theorem for a natural class of proposed one-step ranking functions. The result removes an invalid proof route and identifies the stronger object that remains necessary.

TICKET79는 콜라츠 추측을 증명하거나 반증하지 않는다. 대신 자연스럽게 시도할 수 있는 일단계 순위 함수의 한 부류가 성립할 수 없음을 증명한다. 이 결과의 역할은 잘못된 증명 경로를 제거하고 다음 증명 의무를 정확히 만드는 것이다.

## Accelerated map / 가속 사상

For odd positive integers define

\[
A(n)=\frac{3n+1}{2^{v_2(3n+1)}}.
\]

홀수 양의 정수만 추적하며, `3n+1`에서 가능한 모든 2의 인수를 한 번에 제거한다.

## Exact witness families / 정확한 증인 가족

### Arbitrarily long expansion blocks / 임의로 긴 팽창 구간

For `m,q >= 1`, let

\[
E_{m,q}=2^{m+1}q-1.
\]

Direct induction gives, for `0 <= j <= m`,

\[
A^j(E_{m,q})=3^j2^{m+1-j}q-1.
\]

Therefore every one of the first `m` accelerated valuations equals 1, and

\[
\frac{A^m(E_{m,q})}{E_{m,q}}>\left(\frac32\right)^m.
\]

즉 실제 양의 정수 궤도에는 원하는 길이만큼 계속 커지는 구간이 존재한다. 이는 확률적 모형이나 2진 유령 궤도가 아니라 명시적인 자연수 무한 가족이다.

### Unbounded nonterminal contractions / 끝점이 1이 아닌 무한 수축

For `r >= 1`, let

\[
D_r=\frac{5\cdot2^{2r+1}-1}{3}.
\]

Then `D_r` is an odd positive integer and

\[
3D_r+1=5\cdot2^{2r+1},\qquad A(D_r)=5.
\]

따라서 임의로 큰 수가 한 단계에 5로 내려온다. 끝점이 1이 아니므로 “terminal 진입 간선은 감소 의무에서 제외한다”는 예외로 이 반례를 피할 수 없다.

## Theorem / 정리

Let `S` be finite, `s` map odd positive integers to `S`, and `b:S -> R`. For a fixed real `alpha`, define

\[
R(n)=\alpha\log n+b(s(n)).
\]

There is no choice of `alpha`, `S`, `s`, and `b` for which `R(A(n)) < R(n)` holds at every required accelerated edge with source `n>1`.

고정 실수 `alpha`, 유한 상태 집합 `S`, 상태 함수 `s`, 보정값 `b`를 어떻게 선택해도 위 형태의 순위는 모든 필요한 가속 간선에서 엄격히 감소할 수 없다.

### Proof / 증명

Let `W=max(b)-min(b)`.

1. If `alpha>0`, use an expansion block of length `m`. Its total rank change is greater than

   \[
   \alpha m\log(3/2)-W.
   \]

   This is positive for sufficiently large `m`, contradicting strict decrease on every edge.

2. If `alpha<0`, use `D_r -> 5`. Its rank change is at least

   \[
   -\alpha\log(D_r/5)-W,
   \]

   which is positive for sufficiently large `r`.

3. If `alpha=0` and `|S|=K`, use an expansion block with `K` edges. Its `K+1` vertices contain two with the same state. Strict decrease along all intervening edges would give two different values of `b` for that same state, a contradiction.

For `alpha != 0`, finiteness of `S` is unnecessary: the same proof applies to any bounded correction term, including one computed from growing 2-adic precision.

`alpha != 0`이면 상태 집합이 유한할 필요도 없다. 증가하는 2진 정밀도를 사용하더라도 보정항 전체가 bounded라면 같은 반증이 적용된다.

## What is discarded / 폐기할 경로

- `positive log height + bounded residue correction`
- `negative log height + bounded residue correction`
- `zero log coefficient + fixed finite-state correction`
- bounded lookup tables fitted to a finite residue horizon
- a universal one-step Lyapunov claim that ignores arbitrarily long natural expansion blocks

## What remains / 남은 경로

The surviving proof route must use at least one of the following:

- an adaptive multi-step stopping time;
- an unbounded correction with a separately proved global lower bound;
- a genuinely well-founded ordinal or combinatorial rank;
- a minimal-counterexample contradiction using exact valuation-prefix inequalities and congruences.

다음 후보는 `MinimalCounterexampleValuationSurplusContradiction`이다. 최소 반례 `N`이 존재한다고 가정하면 모든 접두 궤도가 `N` 아래로 내려갈 수 없으므로

\[
2^{S_m}N\le 3^mN+C_m

\]

이 모든 `m`에 대해 성립해야 한다. 다음 단계는 이 부등식과 TICKET78의 정확한 valuation-cylinder 합동식을 결합하여 가능한 무한 접두사를 제거하거나, 제거되지 않는 호환 접두사를 반례 후보로 구성하는 것이다.

“모든 `n>1`은 언젠가 `n`보다 작아진다”를 증명하는 것은 강한 귀납법에 의해 이미 콜라츠 추측과 동치다. 따라서 이를 중간 정리가 해결된 것처럼 표현해서는 안 된다.

## Machine audit / 계산 감사

- expansion families: 1,024 cases;
- exact accelerated step replays: 131,584;
- nonterminal contraction families: 128 cases;
- coefficient/bounded-correction threshold certificates: 35;
- formula, valuation, growth, replay, and threshold failures: 0.

The computation checks the implementation and examples. The theorem is established by the symbolic argument above, not by the finite audit.

계산은 구현과 예시를 검증할 뿐이다. 정리의 근거는 유한 표본이 아니라 위의 기호적 증명이다.

## Literature and novelty / 문헌 및 새로움의 경계

Finite parity-prefix realizability and the 2-adic conjugacy are established mathematics; see Bernstein and Lagarias, [The 3x+1 Conjugacy Map](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13). Tao's [almost-all result](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/almost-all-orbits-of-the-collatz-map-attain-almost-bounded-values/1008CC2DF91AF87F66D190C5E01C907F) is important context but does not supply an all-integer descent theorem.

PrimeProject does not claim those established principles as new. The contribution claimed here is the explicit two-family no-go formulation for this bounded Archimedean-plus-2-adic rank class, its reproducible audit, and its integration into the proof-search ledger.
