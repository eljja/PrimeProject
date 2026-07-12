# TICKET-94: Signed remainder budgets and the Goldbach correlation bridge

## Status

TICKET-94 proves an exact Twin Prime residual decomposition, rejects norm-only lower bounds for the tested divisor surrogates, and proves a per-even-number sufficient bridge for Goldbach. It proves neither conjecture.

한국어: TICKET-94는 부호를 없애는 부등식이 왜 실패하는지 정량화하고, Goldbach에 필요한 정확한 상관합 조건을 만든다. 무한 정리는 아직 열려 있다.

## Twin Prime: preserve the joint sign

For a truncated divisor surrogate `A=Lambda_R`, choose the least-squares coefficient `alpha` and write

```text
Lambda = alpha A + E.
```

The shift-two correlation has the exact decomposition

```text
C_2 = alpha^2 <A,A_shift>
    + alpha <A,E_shift>
    + alpha <E,A_shift>
    + <E,E_shift>.
```

The last three terms form one signed remainder `D_R`. Bounding them separately with Cauchy-Schwarz gives

```text
C_2 >= alpha^2<A,A_shift>
       - |alpha| ||A|| ||E_shift||
       - |alpha| ||E|| ||A_shift||
       - ||E|| ||E_shift||.
```

For every tested `R in {10,30,100,300}`, the exact correlation is positive but this certified norm-only lower bound is negative. Least-squares proximity without shifted sign information is therefore insufficient.

한국어: residual의 크기만 알면 adversarial sign을 배제할 수 없다. 세 remainder를 각각 절댓값으로 누르면 필요한 양의 하한이 사라진다. 다음 정리는 세 항의 합 `D_R` 자체를 하나의 signed Type II 객체로 제어해야 한다.

Next target:

```text
JointShiftTwoSignedRemainderLowerBound.
```

## Goldbach: exact additive correlation

For even `N`, define

```text
G(N)=sum_{2<=n<=N-2} Lambda(n)Lambda(N-n).
```

Split `G(N)=P(N)+E_pp(N)`, where `P(N)` contains genuine ordered prime-prime representations. Proper-prime-power contamination satisfies

```text
E_pp(N) <= B_G(N)
        = 2 sqrt(N) floor(log2(N)) log^2(N).
```

Hence

```text
G(N)>B_G(N)
```

forces at least one Goldbach representation of `N`. If this inequality holds for every sufficiently large even `N`, and the finite remainder is checked, binary Goldbach follows.

한국어: 양의 `G(N)`만으로는 부족하다. prime power 오염 상계보다 큰 양의 margin이 모든 큰 짝수에 대해 균일하게 필요하다. 현재의 안전한 상계는 유한 checkpoint에서 너무 커 인증 margin을 만들지 못한다.

Next target:

```text
UniformBinaryLambdaCorrelationExcess.
```

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket94_signed_remainder_and_goldbach_bridge.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket94_signed_remainder_and_goldbach_bridge
```
