# TICKET-100: Extended residual and Vaughan joint-cancellation audit

## English

TICKET-100 attacks the actual sufficient residual theorem left by TICKET-99.

The finite counterexample search now covers every even Goldbach target through six million and every cumulative shift-two target through ten million. It includes the first schedule transition

```text
W=210 -> W=2310 at n=2310^2=5,336,100.
```

No counterexample to the finite `K=1.6` envelope appears. Goldbach's largest required constant remains `1.5791` at `N=2804`; after the `W=2310` transition the maximum is `0.6209`. Twin's global maximum remains `1.3890` at `x=1018`; its post-transition maximum is `0.3506`. These are finite numerical results, not asymptotic proofs.

The audit then uses the exact Vaughan identity

```text
Lambda = mu_<=U*log - mu_<=U*Lambda_<=V*1
       + Lambda_<=V + mu_>U*Lambda_>V*1
       = I_(U,V) + II_(U,V).
```

Substituting only one Lambda factor gives

```text
C-M = (<I,Lambda_shift>-M) + <II,Lambda_shift>.
```

This avoids the 16-term expansion produced by decomposing both factors. Direct convolution replay verifies the identity and Type II kernel.

The main new no-go is explicit. At `N=930,930`, `W=210`, the Goldbach Type II component alone needs `K=7.9099`, although the joint residual still satisfies `K=1.6`. Therefore separate one-sided or absolute-value bounds on the structured and Type II pieces are not a valid route. Their signed compensation must be retained in a joint dispersion estimate.

The contrapositive is exact. A sufficiently large Goldbach counterexample would force `C_G<=B_G`, hence `R_G/M_G` close to `-1`. Finitely many twin primes would similarly force `C_2<=B_2+O(1)`. Either conclusion contradicts a proved `-K/log n` joint lower envelope because the external local main is linear and the contamination budgets are sublinear.

Vaughan's identity is a standard mechanism for reducing prime sums to Type I and Type II expressions; the difficult term is bilinear. See the [Vaughan identity reference](https://encyclopediaofmath.org/wiki/Vaughan_identity). The need for joint Type I/II information is also consistent with [Ford–Maynard](https://arxiv.org/abs/2407.14368).

## 한국어

TICKET-100은 TICKET-99의 충분조건을 직접 공격합니다. Goldbach는 6M까지 모든 짝수, Twin은 10M까지 모든 누적 target을 검사했고 `W=210`에서 `2310`으로 바뀌는 첫 전환도 포함했습니다. `K=1.6`의 유한 반례는 없었지만 이는 증명이 아닙니다.

정확한 Vaughan identity로 Lambda를 구조적인 Type I 부분과 bilinear Type II 부분으로 분해했습니다. 중요한 결과는 Goldbach `N=930,930`에서 Type II 항만 따로 `K=1.6`으로 하한화하는 명제가 실제로 거짓이라는 점입니다. 필요한 상수는 `7.91`이며 구조항의 양의 보상이 있어야 전체 residual이 살아남습니다.

따라서 각 항에 절댓값을 취하거나 별도 하한을 증명하는 경로는 폐기합니다. 다음 목표는 `structured + Type II`의 결합 부호를 유지하는 `JointVaughanGoldbachResidualEnvelope`와 `JointVaughanShiftTwoResidualEnvelope`입니다. 이 결과는 proof strategy의 반례이지 네 난제의 반례가 아니며, RH와 Collatz에는 결합 성분 원칙만 전이됩니다.

## Reproduce / 재현

```text
D:\python\anaconda3\python.exe scripts\ticket100_extended_residual_vaughan_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket100_extended_residual_vaughan_audit
```
