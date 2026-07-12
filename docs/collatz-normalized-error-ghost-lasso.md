# TICKET90: Normalized-Error Ghost Lasso

## Claim boundary / 주장 경계

TICKET90 proves that every fixed-precision normalized-error automaton retains a non-target ghost lasso. It does not prove the valuation-excess-five theorem, additive-two delay, or the Collatz conjecture.

TICKET90은 모든 고정 정밀도 normalized-error automaton에 목표를 회피하는 ghost lasso가 남음을 증명한다. valuation 초과량 5의 무한 반복, 가산상수 2, 콜라츠 추측은 증명하지 않는다.

## Normalized error / 정규화 오차

For the least residue `r_H`, define the ordinary integer

\[
e_H=\frac{3^{r_H+1}+7}{2^{H+3}}.
\]

The next exponent bit is exactly

\[
b_{H+1}=e_H\pmod2.
\]

If `e_H` is even,

\[
r_{H+1}=r_H,
\qquad
e_{H+1}=\frac{e_H}{2}.
\]

If `e_H` is odd, define

\[
A_H=\frac{3^{2^{H+1}}-1}{2^{H+3}}.
\]

Then

\[
r_{H+1}=r_H+2^{H+1},
\qquad
e_{H+1}=\frac{e_H+3^{r_H+1}A_H}{2}.
\]

In particular, `e_H=0 mod 4` forces the next two lift bits to be `00`.

## Correction limit / 보정항의 극한

Squaring the defining identity gives

\[
\boxed{A_{H+1}=A_H+2^{H+2}A_H^2.}
\]

Therefore `A_H` converges 2-adically to

\[
\alpha=\frac{\log_{2\text{-adic}}(-3)}4.
\]

Since `3^(r_H+1)` converges to `-7`, the odd-branch forcing term satisfies

\[
B_H=3^{r_H+1}A_H\longrightarrow
\beta=-7\alpha.
\]

Moreover,

\[
B_H\equiv\beta\pmod {2^{H+2}}.
\]

## Limiting ghost / 극한 ghost

The limiting transition is

\[
F_\beta(e)=
\begin{cases}
e/2,&e\equiv0\pmod2,\\
(e+\beta)/2,&e\equiv1\pmod2.
\end{cases}
\]

The number `beta` is odd and

\[
F_\beta(\beta)=\beta.
\]

Thus the limiting completion map has a fixed point that never reaches `e=0 mod 4`. Reducing it modulo any fixed `2^m` gives a lasso in that fixed finite-state abstraction.

이 fixed point는 실제 양의 Collatz 궤도나 실제 `e_H`와 같다고 주장하지 않는다. 고정 정밀도 추상화가 목표를 강제하지 못한다는 반모형일 뿐이다.

## Fixed-precision no-go / 고정 정밀도 no-go

For every fixed precision `m`, the forcing term eventually agrees with `beta` at the precision needed by the transition. Hence increasing one fixed modulus to another fixed modulus never removes the ghost lasso.

Therefore no proof using only a fixed finite residue state of `e_H` can force infinitely many `e_H=0 mod 4` events. A valid proof must couple precision to height.

고정된 모듈러 상태 공간을 더 크게 만드는 방식만으로는 해결되지 않는다. 정밀도 `m(H)`가 높이와 함께 증가해야 한다.

## Machine audit / 계산 감사

- horizons `H=2..256`;
- 254 normalized-error transitions;
- 20-bit exact recurrence and forcing checks;
- fixed-point lassos at every precision `m=2..64`;
- correction, convergence, lift-bit, recurrence, and lasso failures: zero.

The audit verifies the implementation. The no-go theorem rests on the exact recurrence and limiting fixed-point argument.

## Next theorem / 다음 정리

The retained target is `GrowingPrecisionErrorGhostSeparation`:

> Assuming the eventual valuation-excess-four cap, derive an impossible lower bound on `v2(e_H-beta)` relative to `H`, or otherwise prove that the actual normalized-error orbit must enter `0 mod 4` infinitely often.

실제 오차 궤도가 ghost를 임의로 깊게 추적할 수 없음을 높이에 따라 증가하는 정밀도로 증명해야 한다.

## Novelty boundary / 새로움의 경계

PrimeProject treats the normalized-error recurrence and fixed-precision ghost-lasso formulation as candidate contributions. Independent review against p-adic dynamical-systems literature remains required. No open conjecture is claimed solved.
