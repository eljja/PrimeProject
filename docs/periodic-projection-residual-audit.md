# TICKET-97: Optimal periodic projection and residual-sign audit

## Status

TICKET-97 adds exact finite-modulus arithmetic information to the TICKET-96 Fourier targets. It proves and audits the L2-optimal residue-periodic decomposition, then constructs a zero-residue-mean signed countermodel whose Goldbach-type and shift-two correlations are both negative. It does not prove any open conjecture.

한국어: 단순 푸리에 에너지보다 강한 정보를 사용하기 위해 각 residue class의 실제 평균을 모두 보존한다. 이 정보로 만든 주기 모델은 같은 modulus를 쓰는 모든 모델 중 L2 오차가 가장 작다. 그런데도 residual의 이항 부호는 결정되지 않는다.

## Optimal finite-modulus projection

For a fixed modulus `W`, define `P_W Lambda(n)` as the average of `Lambda` over all audited integers congruent to `n mod W`. Then

```text
Lambda = P_W Lambda + E_W.
```

The projection is the unique finite-interval L2 minimizer among `W`-periodic functions. Its residual satisfies

```text
sum_{n=r mod W} E_W(n) = 0
```

for every residue `r`, and is orthogonal to every `W`-periodic function.

Both target correlations split exactly into a periodic main term, two signed cross terms, and one signed residual correlation. Exact reconstruction, residue orthogonality, and energy decomposition are machine checked.

## Finite audit

At `N=10,000` and `100,000`, TICKET-97 tests

```text
W in {2, 6, 30, 210, 2310}.
```

Every model is data-fitted and therefore stronger than a fixed theoretical wheel at the same modulus. Nevertheless:

- all exact decompositions pass;
- all residue residual sums vanish within numerical tolerance;
- every separate norm-only Goldbach lower bound is negative;
- every separate norm-only Twin lower bound is negative;
- no model certifies either TICKET-95 sharp contamination budget.

This does not prove that every growing-modulus or bilinear approach fails. It blocks fixed-modulus one-point information plus separate residual norms.

## Explicit residual countermodel

Consider

```text
e = [1, 1, -1, -1, -1, -1, 1, 1].
```

Its sum in each residue class modulo 2 is zero. Yet

```text
sum_n e(n)e(3-n) = -4,
sum_n e(n)e(n+2) = -2.
```

Thus exact residue means do not determine either binary additive or shift-two sign. This is a signed residual countermodel, not a prime sequence or a counterexample to Goldbach or Twin Prime.

한국어: mod 2 평균을 완벽히 맞춰도 두 점 상관은 음수가 될 수 있다. 한 점 분포와 두 점 결합분포는 다른 정보다. 따라서 residue equidistribution만으로는 부족하고 residual의 signed bilinear correlation을 직접 제어해야 한다.

## Retained targets

```text
Goldbach: GrowingModulusBinaryResidualCancellation
Twin:     GrowingModulusShiftTwoResidualCancellation
```

The modulus must grow with scale under independently proved prime-distribution estimates, while the residual correlation must be controlled through Type II or higher-order uniformity rather than separate L2 norms.

## Four-problem boundary

- Riemann Hypothesis: only a finite-conductor projection gate is transferred; no growing-conductor kernel theorem is proved.
- Collatz: only a finite-residue projection gate is transferred; no growing-residue natural-orbit theorem is proved.
- Goldbach: finite periodic optimality and a residual-sign no-go are proved; growing-modulus cancellation remains open.
- Twin Prime: finite periodic optimality and a residual-sign no-go are proved; growing-modulus shift-two cancellation remains open.

## Research context

Green and Tao's W-trick removes local obstructions from small primes but does not prove the binary prime-tuple cases: [The primes contain arbitrarily long arithmetic progressions](https://annals.math.princeton.edu/2008/167-2/p03). Ford and Maynard show that substantial Type I/II information is necessary for general prime-producing lower bounds: [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368). TICKET-97 claims neither result as new; its contribution is the optimal finite projection contract and explicit residual-sign countermodel.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket97_periodic_projection_residual_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket97_periodic_projection_residual_audit
```
