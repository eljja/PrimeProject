# TICKET88: Why Two-Sided Digit Infinitude Does Not Prove Run Length Two

## Claim boundary / 주장 경계

TICKET88 does not prove the desired `100` pattern recurrence. It proves that the TICKET87 argument is insufficient for that promotion and rejects a natural bit-complement workaround by exact computation.

TICKET88은 `100` 패턴의 무한 반복을 증명하지 않는다. TICKET87의 논리만으로 그 결론을 얻을 수 없음을 반모형으로 증명하고, 자연스러운 비트 보수 대안도 정확한 궤도 계산으로 폐기한다.

## The logical gap / 논리적 간극

TICKET87 proves that the fixed 2-adic exponent has infinitely many zero bits and infinitely many one bits. This forces infinitely many `10` transitions, but it does not force `100`.

Define a binary 2-adic digit sequence by

\[
b_n=0\quad\text{exactly when}\quad n=m^2,\ m\ge2,
\]

and set `b_n=1` otherwise. It has infinitely many zeros and ones. Consecutive square indices differ by `2m+1>1`, so it contains no `00`. Its zero gaps are unbounded, so it is not eventually periodic.

따라서 두 비트가 모두 무한히 나타나고 이진 전개가 비주기적이라는 조건만으로도 `00`은 전혀 보장되지 않는다. 이는 실제 고정 로그가 `00`을 갖지 않는다는 뜻이 아니라, 현재 논증의 전제가 부족하다는 뜻이다.

## Exact run formulation / 정확한 run 문제

For the actual exponent, a `100` pattern beginning at height `H` is equivalent to a zero run of length at least two after a top-bit lift. TICKET87 converts such a run into

\[
D(k)-\log_2 k>2.
\]

The missing statement is not generic irrationality. It is the target-specific theorem

\[
\forall H_0\ \exists H\ge H_0:\quad r_Hr_{H+1}r_{H+2}=100.
\]

## Rejected complement route / 폐기한 보수 경로

Let `s=-r`. Since `r` is odd, every binary digit above bit zero is complemented:

\[
s_h=1-r_h\qquad(h\ge1).
\]

This appears useful because an infinite supply of `11` in `r` becomes `00` in `s`. But the analytic geometry is not preserved. From `3^(r+1)=-7`,

\[
3^s=-\frac37,
\qquad
x_0(s)=\frac{3^s-1}{2}=-\frac57.
\]

The exact accelerated orbit is

\[
-\frac57\xrightarrow{3}-\frac17
\xrightarrow{2}\frac17
\xrightarrow{1}\frac57
\xrightarrow{1}\frac{11}{7}
\xrightarrow{3}\frac57.
\]

Its eventual valuation word is `(1,3)`, with mean valuation `2` and reciprocal mean `1/2`. The original coefficient-one geometry is lost. Therefore bit complementation cannot transfer a double-one recurrence into the desired additive-two theorem.

비트 조합은 뒤집히지만, 하강 지연을 만드는 valuation 주기는 보존되지 않는다. 이 대안은 계수 1 경계에서 사용할 수 없다.

## Finite evidence is not recurrence / 유한 자료는 반복 정리가 아니다

The 262,144-height TICKET87 artifact contains 32,753 completed zero runs of length at least two and a maximum observed length of 16. These are exact finite certificates. They do not prove that another length-two run occurs beyond every bound.

262,144 높이 안에서 `100` 패턴이 많이 발견되었다는 사실은 무한 반복의 증명이 아니다.

## Retained route / 유지할 경로

The next target is `FixedLogGoldenMeanExclusion`:

1. treat eventual avoidance of `00` as membership in the golden-mean subshift;
2. exploit the specific equation `log(1-8)/log(1+8)`, not generic irrationality;
3. derive a contradiction from that subshift constraint or identify a stronger required theorem;
4. keep every finite prefix search as falsification evidence only.

다음 단계는 고정 2-adic 로그가 결국 `00`을 금지하는 symbolic subshift 안에 들어갈 수 없음을 증명하는 것이다.

## Literature boundary / 문헌 경계

Low-complexity and finite-type subshifts contain many aperiodic sequences, so symbolic complexity alone does not supply the missing arithmetic exclusion. The relation between this specific p-adic logarithm ratio and a forbidden-word subshift requires a dedicated literature review and independent proof analysis.

PrimeProject claims only the explicit logical countermodel, complement-orbit calculation, and resulting proof-route no-go. It claims no additive-two infinite theorem and no Collatz resolution.
