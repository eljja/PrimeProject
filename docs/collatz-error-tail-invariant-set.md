# TICKET-91: Error-tail conjugacy and the full invariant-set obstruction

## Claim status

TICKET-91 proves a restricted 2-adic coordinate theorem and corrects the next proof route proposed by TICKET-90. It does **not** prove recurrence of `00`, an infinite additive-two Mersenne-delay subsequence, the Collatz conjecture, or a divergent Collatz counterexample.

한국어: TICKET-91은 제한된 2진 정수 좌표 정리와 증명 경로 교정을 제공한다. `00`의 무한 재발, Mersenne 지연의 가산 초과량 2, 콜라츠 추측, 발산 반례는 증명하지 않는다.

## Exact tail coordinate

Let `R in Z_2` be the odd 2-adic exponent satisfying

```text
3^(R+1) = -7.
```

For the least certified residue `r_H`, write

```text
R = r_H + 2^(H+1)t_H,
e_H = (3^(r_H+1)+7)/2^(H+3),
u_H = 3^(2^(H+1)) = 1 + 2^(H+3)A_H.
```

Substitution into the fixed equation gives the exact identity

```text
e_H = 7(1-u_H^(-t_H))/2^(H+3).
```

The 2-adic binomial expansion therefore yields

```text
e_H = 7A_H t_H        (mod 2^(H+3)).
```

Since `A_H = alpha (mod 2^(H+2))` for `alpha=log_2adic(-3)/4`, defining `gamma=7alpha` gives the growing-precision relation

```text
e_H = gamma t_H       (mod 2^(H+2)).
```

한국어: `t_H`는 현재까지 확정된 지수 비트 뒤의 미래 꼬리다. 정규화 오차 `e_H`는 임의의 유사 지표가 아니라, 홀수 단위 `gamma`를 곱한 미래 꼬리와 높이 `H+2` 비트까지 정확히 일치한다.

## What the beta ghost actually is

The next tail is the binary shift

```text
b_H = t_H mod 2,
t_(H+1) = (t_H-b_H)/2.
```

Multiplication by the odd unit `gamma` conjugates this shift to the limiting error map

```text
F(e) = e/2              if e is even,
F(e) = (e+beta)/2       if e is odd,
beta = -gamma.
```

The fixed point `e=beta` is exactly the tail `t=-1`, whose future binary digits are all `1`. Moreover,

```text
min(v2(e_H-beta), H+2) = min(v2(t_H+1), H+2).
```

Thus distance from the single ghost measures only how many consecutive `1` bits occur before the next `0`. Separating the actual orbit from `beta` can prove the existence of another zero bit, but it cannot force two adjacent zeros.

한국어: TICKET-90의 `beta` 고정점은 미래 비트가 전부 `1`인 꼬리 하나에 불과하다. `beta`와의 거리는 다음 `0`이 나타날 때까지의 연속 `1` 길이만 측정한다. 따라서 `beta` 하나를 피하는 것으로는 `00`을 만들 수 없다.

## The real obstruction

Let `G` be the one-sided golden-mean subshift: all binary tails avoiding `00`. It is invariant under the tail shift. Because `gamma` is odd, multiplication by `gamma` is a 2-adic isometry, so

```text
K = gamma G
```

is invariant under the limiting error map. At finite depth `n`, `G` has `F_(n+2)` legal words. The limiting set is uncountable and has positive entropy. The beta fixed point is only one point of `K`.

한국어: 실제 장애물은 고정점 하나가 아니라 `00`이 없는 모든 미래 꼬리의 집합 `G`다. 오차 좌표에서는 이 집합이 `K=gamma G`로 옮겨지며 limiting map 아래 불변이다. 길이 `n`에서 가능한 꼬리는 피보나치 수 `F_(n+2)`개이므로, 이 집합은 작거나 유한한 예외집합이 아니다.

## Route correction

Discarded target:

```text
GrowingPrecisionErrorGhostSeparation
```

This target only separates the orbit from the all-one tail and largely collapses to the zero-bit infinitude already proved in TICKET-87.

Retained target:

```text
GoldenMeanInvariantSetEscape
```

One must use the specific arithmetic identity defining `R` to prove that its shift orbit leaves `G` infinitely often, equivalently that the binary expansion of `R` contains `00` infinitely often. Generic transcendence, cardinality, fixed-precision automata, and separation from one fixed point are insufficient.

한국어: 다음 단계는 단일 ghost와의 거리 추정이 아니다. `R=log_2adic(-7)/log_2adic(3)-1`이라는 대상 고유의 산술 관계를 사용하여 꼬리 궤도가 황금평균 불변집합을 무한히 탈출함을 보여야 한다.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket91_error_tail_invariant_set_lab.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket91_error_tail_invariant_set
```

The machine audit checks 255 horizons, 254 exact tail shifts, 4,096 finite conjugacy states, and all 377 depth-12 no-`00` words. These finite checks validate the implementation of the proved identities; they are not evidence that the open recurrence target holds at all heights.
