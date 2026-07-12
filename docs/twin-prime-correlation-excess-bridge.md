# TICKET-93: Exact twin-correlation excess bridge

## Claim status

TICKET-93 proves a sufficient bridge from an explicit von Mangoldt correlation excess to infinitely many twin primes, and rejects a common truncated-divisor shortcut. It does not prove the required excess estimate or the Twin Prime Conjecture.

한국어: TICKET-93은 정확한 상관합 하한이 어떤 조건을 만족하면 쌍둥이 소수 무한성으로 이어지는지 증명한다. 그러나 그 하한 자체는 아직 증명하지 않는다.

## Exact target correlation

Define

```text
C_2(x) = sum_{n<=x} Lambda(n)Lambda(n+2).
```

The von Mangoldt function is supported on prime powers, not only primes. Split

```text
C_2(x) = T_2(x) + E_pp(x),
```

where `T_2` contains genuine prime-prime pairs and every term of `E_pp` contains at least one proper prime power `p^a`, `a>=2`.

For `y>=2`, the number of proper prime powers up to `y` satisfies

```text
Q(y) <= sum_{2<=a<=log2(y)} y^(1/a)
     <= sqrt(y) floor(log2(y)).
```

Charging a contaminated shifted pair to either position and bounding each weight by `log^2(y)` gives

```text
0 <= E_pp(x) <= B(x),
B(x) = 2 sqrt(x+2) floor(log2(x+2)) log^2(x+2).
```

Therefore:

```text
limsup_{x->infinity} (C_2(x)-B(x)) = +infinity
```

implies infinitely many twin primes. If only finitely many twin pairs existed, their total `T_2` weight would eventually be constant, contradicting unbounded excess. In particular, any proved linear lower bound `C_2(x)>=c x`, `c>0`, is sufficient because `B(x)=o(x)`.

한국어: `Lambda` 상관합에는 소수 거듭제곱이 섞이지만 그 오염은 명시적으로 `o(x)`다. 따라서 상관합이 이 오염 상계를 무한히 크게 넘어선다는 사실만 증명하면 실제 쌍둥이 소수도 무한하다.

## Why a positive divisor surrogate is not enough

The truncated divisor surrogate

```text
Lambda_R(n) = sum_{d|n, d<=R} mu(d) log(R/d)
```

is useful for averaged sieve calculations, but it is not a pointwise lower bound for `Lambda`. The TICKET-93 audit constructs explicit violations for every tested `R in {10,30,100,300}`:

- `Lambda_R(n)>Lambda(n)` at many integers;
- `Lambda_R(n)Lambda_R(n+2)>0` when the exact product is zero;
- the total surrogate correlation is positive despite these false-positive pairs.

Thus positivity of the surrogate sum cannot be promoted to a lower bound for `C_2` without a separate signed remainder theorem.

한국어: 절단 divisor 합이 양수라는 사실은 실제 소수쌍 하한이 아니다. 합성수 쌍에서도 양의 항을 만들기 때문이다. 필요한 것은 Möbius 부호가 포함된 remainder의 취소를 제어하는 정리다.

## Remaining analytic bridge

The exact identity `Lambda=mu*log` turns `C_2` into a signed shifted divisor convolution. Taking absolute values destroys the cancellation needed for a lower bound. The next target is

```text
ShiftTwoTypeIICorrelationExcess:
limsup_x(C_2(x)-B(x))=+infinity
```

through a signed Type II estimate that survives parity and wider-gap countermodels. This direction is aligned with Ford and Maynard's result that substantial Type II information is necessary for nontrivial lower bounds in a general prime-producing sieve framework: [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket93_twin_correlation_excess_bridge.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket93_twin_correlation_excess_bridge
```

The finite correlation audit is a consistency check and falsification oracle. It is not an extrapolation to infinity.
