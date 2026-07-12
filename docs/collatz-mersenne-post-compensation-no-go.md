# TICKET81: Mersenne First-Compensation No-Go

## Claim boundary / 주장 경계

TICKET81 does **not** prove or disprove the Collatz conjecture. It proves an exact theorem about the restricted Mersenne family `N_k=2^k-1`: after its initial valuation-one expansion block, the first larger 2-adic valuation fails to force descent for infinitely many `k`.

TICKET81은 콜라츠 추측을 증명하거나 반증하지 않는다. 메르센 계열 `N_k=2^k-1`에 한정하여, 처음의 긴 `v_2=1` 팽창 구간 뒤에 나타나는 첫 번째 큰 2진 지수가 무한히 많은 `k`에서 시작값 아래로의 하강을 강제하지 못한다는 정확한 정리다.

## Setup / 설정

For odd positive integers, use the accelerated Collatz map

\[
A(n)=\frac{3n+1}{2^{v_2(3n+1)}}.
\]

Fix `k>=2` and set

\[
N_k=2^k-1.
\]

The question rejected here is precise: once the exact valuation cylinder has already stabilized at the positive integer `N_k`, must the first valuation larger than one repay the preceding expansion and send the orbit below `N_k`? The answer is no.

여기서 폐기하는 후보 명제는 다음과 같다. 정확한 valuation cylinder의 최소 비음수 잔여가 이미 양의 정수 `N_k`로 안정화된 뒤라면, 처음 등장하는 `1`보다 큰 valuation이 앞선 팽창을 상쇄하여 궤도를 `N_k` 아래로 보내는가? 답은 아니다.

## Lemma 1: exact expansion block / 보조정리 1: 정확한 팽창 구간

For every `0<=j<=k-1`,

\[
A^j(N_k)=3^j2^{k-j}-1.
\]

Proof is by induction. If the formula holds at `j<k-1`, then

\[
3A^j(N_k)+1=2\left(3^{j+1}2^{k-j-1}-1\right),
\]

and the parenthesized factor is odd. Hence the next valuation is exactly one and the displayed formula follows at `j+1`.

Moreover, for `1<=j<=k-1`,

\[
A^j(N_k)>N_k
\]

because `3^j>2^j`. Thus all first `k-1` accelerated steps are strict expansions relative to the start.

괄호 안의 수가 홀수이므로 처음 `k-1`단계의 valuation은 정확히 모두 `1`이다. 또한 `3^j>2^j`이므로 이 구간의 모든 iterate는 시작값보다 크다.

## Lemma 2: the cylinder is already stabilized / 보조정리 2: cylinder 안정화

The exact word `a_1=...=a_{k-1}=1` determines the odd starting residue

\[
n\equiv-1\pmod{2^k}.
\]

Its least nonnegative residue is `2^k-1=N_k`. The modulus is already larger than `N_k`, so the positive-integer stabilization criterion from TICKET80 is met for this fixed start at depth `k-1`.

즉, 이번 반례 계열은 TICKET80에서 나타난 `-1`로 도망가는 비안정 잔여가 아니다. 깊이 `k-1`에서 최소 잔여가 실제 양의 정수 `N_k`로 고정된 뒤에도 한 번의 보상만으로는 하강이 보장되지 않는다.

## Lemma 3: exact first compensation / 보조정리 3: 첫 보상 단계의 정확식

At the end of the expansion block,

\[
A^{k-1}(N_k)=2\cdot3^{k-1}-1,
\]

so the next numerator is

\[
3A^{k-1}(N_k)+1=2(3^k-1).
\]

The lifting-the-exponent lemma gives

\[
v_2(3^k-1)=
\begin{cases}
1,&k\text{ odd},\\
2+v_2(k),&k\text{ even}.
\end{cases}
\]

Therefore

\[
a_k=
\begin{cases}
2,&k\text{ odd},\\
3+v_2(k),&k\text{ even},
\end{cases}
\qquad
A^k(N_k)=\operatorname{oddpart}(3^k-1).
\]

보상 valuation은 홀수 `k`에서 항상 `2`, 짝수 `k`에서도 `3+v_2(k)`에 불과하다. 앞선 팽창 길이 `k-1`에 비해 일반적으로 매우 작다.

## Theorem: complete first-compensation classification / 정리: 첫 보상 단계의 완전 분류

The first post-block iterate lies below its start exactly for

\[
k\in\{2,4,8\}.
\]

It does not descend for every odd `k>=3`, for `k=6`, and for every even `k>=10`.

### Odd exponents / 홀수 지수

For odd `k>=3`,

\[
A^k(N_k)=\frac{3^k-1}{2}>2^k-1=N_k.
\]

The inequality holds at `k=3` and remains strict after increasing `k`, or follows directly from `3^k+1>2^{k+1}`.

### Even exponents at least ten / 10 이상의 짝수 지수

Since `2^{v_2(k)}<=k`,

\[
2^{2+v_2(k)}\le4k.
\]

For `k>=10`,

\[
\frac{3^k-1}{2^k-1}>
\frac89\left(\frac32\right)^k>4k.
\]

The last inequality holds at `k=10` because `(3/2)^10>45`, and `(3/2)^k/k` is increasing for `k>=3`. Consequently,

\[
A^k(N_k)=\frac{3^k-1}{2^{2+v_2(k)}}
\ge\frac{3^k-1}{4k}>2^k-1.
\]

Only `k=2,4,6,8` remain. Exact evaluation gives post-block iterates `1,5,91,205`; these descend for `k=2,4,8`, while `91>63` for `k=6`.

따라서 예외 집합 `{2,4,8}`은 계산 범위에서 추측한 것이 아니라, 무한한 홀수 계열과 `k>=10`인 모든 짝수 계열을 기호 부등식으로 처리한 뒤 남은 네 경우만 직접 계산하여 얻은 완전 분류다.

## What is rejected / 폐기되는 증명 경로

- “긴 `v_2=1` 구간 뒤 첫 큰 valuation은 반드시 하강을 만든다.”
- “양의 정수 cylinder가 안정화되면 바로 다음 보상에서 하강한다.”
- “한 번의 LTE valuation 급증이 길이 `k-1`의 누적 팽창 부채를 갚는다.”

All three fail on explicit infinite subfamilies. This is stronger than a finite counterexample search because the obstruction is symbolic and unbounded.

세 명제 모두 명시적인 무한 부분계열에서 실패한다. 따라서 이는 유한 탐색에서 우연히 실패 사례를 찾은 결과보다 강하다.

## Retained route / 유지하는 경로

The next admissible target is `MersenneAdaptiveCompensationWindow`: find an explicit window length `L(k)` and prove that cumulative valuations after the expansion block force some iterate below `N_k`. Such a theorem would be a genuine infinite-family result, but still not the full Collatz conjecture.

다음 목표는 `MersenneAdaptiveCompensationWindow`다. 첫 보상 한 번이 아니라 이후 `L(k)`단계의 누적 valuation 잉여를 분석하여 어느 iterate가 `N_k` 아래로 내려가는지 증명한다. 메르센 시작값 전체에 성공하면 무한 계열 정리이지만, 모든 홀수에 대한 콜라츠 증명은 아니다.

## Machine audit / 계산 감사

- exponents: `k=2..1024`;
- Mersenne starts: 1,023;
- exact expansion-step replays: 523,776;
- first-compensation non-descents: 1,020;
- descent exponents: exactly `2,4,8`;
- formula, valuation, stabilization, classification, and symbolic-partition failures: 0.

The audit checks implementation and guards the artifact. The theorem is proved for every `k>=2` by the formulas and inequalities above, not by terminating the computation at 1,024.

계산 감사는 구현의 일치성을 확인한다. 모든 `k>=2`에 대한 정리의 근거는 위의 귀납식, LTE, 무한 구간 부등식이며 `k=1024`까지의 계산 자체가 아니다.

## Literature and novelty / 문헌 및 새로움의 경계

Parity cylinders and the 2-adic Collatz conjugacy are established; see Bernstein and Lagarias, [The 3x+1 Conjugacy Map](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13). Tao's [almost-all orbit theorem](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/almost-all-orbits-of-the-collatz-map-attain-almost-bounded-values/1008CC2DF91AF87F66D190C5E01C907F) is context for why an explicit family theorem is not an all-integer theorem.

The Mersenne trajectory identity and LTE are elementary established tools. PrimeProject claims only this explicit stabilized-cylinder first-compensation classification, its no-go interpretation, reproducible audit, and integration into the proof-search program. A broader novelty claim requires a dedicated literature review and peer review.

메르센 궤도 항등식과 LTE 자체를 새 결과라고 주장하지 않는다. 프로젝트의 기여 범위는 안정화 cylinder에서의 첫 보상 완전 분류, 잘못된 증명 경로의 제거, 재현 가능한 감사, 후속 누적 보상 문제의 명세다. 더 강한 독창성 주장은 별도의 문헌 조사와 동료 검토가 필요하다.
