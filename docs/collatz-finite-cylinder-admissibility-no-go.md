# Collatz Finite-Cylinder Natural-Admissibility No-Go

## Claim boundary / 주장 경계

This note proves that no fixed finite 2-adic prefix can distinguish a TICKET77 ghost from all positive integers. It does not prove the Collatz conjecture. It removes one proof strategy and requires any successor strategy to use nonlocal or Archimedean information.

이 문서는 고정된 유한 2-adic prefix만으로 TICKET77 ghost와 모든 양의 정수를 분리할 수 없음을 증명한다. Collatz 추측의 증명이 아니다. 하나의 증명 전략을 폐기하고 다음 전략이 비국소 정보 또는 Archimedean 크기를 사용하도록 제한한다.

## Literature and novelty boundary / 문헌 및 신규성 경계

The 2-adic conjugacy between the `3x+1` map and the shift is established mathematics. See Bernstein and Lagarias, [The 3x+1 Conjugacy Map](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/3x-1-conjugacy-map/6975BB4A8C46CF6842217043AAF9EC13), *Canadian Journal of Mathematics* 48 (1996), and Rozier, [Parity sequences of the 3x+1 map on the 2-adic integers](https://arxiv.org/abs/1805.00133), *INTEGERS* 19 (2019).

PrimeProject does not claim to rediscover this conjugacy or the density of the natural numbers in `Z_2`. The project-specific contribution is the exact accelerated-valuation cylinder formula, its exhaustive regression audit, and its use as a claim guard after TICKET77.

`3x+1` 사상과 shift 사이의 2-adic conjugacy는 기존 수학이다. PrimeProject는 이를 새로 발견했다고 주장하지 않는다. 프로젝트 고유 결과는 TICKET77 경계 상태에 accelerated valuation cylinder 공식을 연결하고, 전수 감사와 증명 경로 차단 규칙으로 만든 것이다.

## Exact finite-word cylinder / 정확한 유한 word cylinder

Let

```text
a = (a_1,...,a_m),  a_i >= 1,
S = a_1+...+a_m.
```

Define

```text
C_0 = 0,
C_(j+1) = 3*C_j + 2^(a_1+...+a_j).
```

Whenever the accelerated Collatz map follows the valuation word `a`, direct composition gives

```text
T^m(n) = (3^m*n+C_m)/2^S.
```

The terminal value is odd exactly when

```text
3^m*n+C_m = 2^S mod 2^(S+1).
```

Since `3^m` is invertible modulo `2^(S+1)`, this gives one unique residue

```text
r_a = 3^(-m)*(2^S-C_m) mod 2^(S+1).
```

The complete finite valuation cylinder is

```text
n = r_a + q*2^(S+1),  q >= 0.
```

한국어 해설: 임의의 유한 positive valuation word는 하나의 정확한 홀수 잉여류를 정한다. 그 잉여류의 모든 양의 정수는 같은 valuation word를 재현한다.

## Theorem / 정리

**FiniteValuationCylinderNaturalDensityNoGo.**

Every finite accelerated valuation word is realized by infinitely many positive integers. Consequently:

1. every finite 2-adic neighborhood of a TICKET77 ghost contains positive integers;
2. no fixed finite residue or valuation prefix certifies that the ghost is non-natural;
3. no continuous Boolean classifier on `Z_2` can accept every positive integer and reject any 2-adic point;
4. a Collatz admissibility rank cannot factor through a fixed finite 2-adic quotient.

모든 유한 accelerated valuation word는 무한히 많은 양의 정수로 실현된다. 따라서 TICKET77 ghost의 모든 유한 2-adic neighborhood에는 양의 정수가 있고, 고정 유한 residue 또는 valuation prefix만으로 ghost의 비자연성을 인증할 수 없다.

## Proof / 증명

### Lemma 1: unique realization class

The congruence above has exactly one solution modulo `2^(S+1)` because `gcd(3^m,2^(S+1))=1`. Substitution into each affine prefix, or induction on `m`, shows that the valuations are exactly `a_1,...,a_m`. Thus the finite word defines one nonempty residue class.

`3^m`은 `2^(S+1)`에서 invertible이므로 해는 유일하다. 각 affine prefix에 대입하면 valuation이 정확히 주어진 word와 일치한다.

### Lemma 2: infinitely many natural witnesses

For every nonnegative `q`,

```text
n_q = r_a + q*2^(S+1)
```

belongs to the same cylinder. These values are positive for all sufficiently large `q`, and infinitely many distinct positive integers therefore realize the word.

동일 잉여류에 `2^(S+1)`의 배수를 계속 더하면 같은 word를 재현하는 양의 정수를 무한히 얻는다.

### Lemma 3: density blocks finite separation

Every basic open set in `Z_2` is a residue class modulo some `2^k`. It contains a positive representative and infinitely many positive representatives after adding multiples of `2^k`. Therefore the positive integers are dense in `Z_2`.

Any finite-prefix classifier is locally constant and continuous. If a continuous Boolean classifier accepts every positive integer, it accepts their closure, which is all of `Z_2`. It cannot reject a TICKET77 ghost.

`Z_2`의 모든 기본 열린집합은 `mod 2^k` 잉여류이고 양의 정수를 포함한다. 따라서 자연수는 `Z_2`에서 조밀하다. 유한 prefix classifier는 locally constant이므로 자연수 전체를 accept하면서 특정 ghost를 reject할 수 없다.

The lemmas prove the theorem. `QED`.

## Independent machine audit / 독립 계산 감사

The all-depth theorem follows algebraically. The implementation independently audited every positive composition with total valuation `S<=16`:

```text
finite valuation words: 65,535
expected compositions: 65,535
distinct residue classes: 65,535
positive representatives replayed: 262,140
residue collisions: 0
formula failures: 0
representative replay failures: 0
count-identity failures: 0
```

This finite audit checks the formula. It is not used to infer density or continuity from a cutoff.

유한 감사는 공식 구현을 확인할 뿐이며, 전역 밀도 정리는 cutoff가 아니라 위의 잉여류 논증에서 나온다.

## Discarded and retained routes / 폐기 및 유지 경로

Discard:

```text
fixed residue bits
finite parity or accelerated-valuation words
continuous finite-state 2-adic natural classifiers
compactness arguments that silently treat N as a closed subset of Z_2
```

Retain:

```text
ArchimedeanTwoAdicCoupledDescent:
use both integer magnitude and growing 2-adic precision in a well-founded rank;
the rank must not factor through any fixed finite 2-adic quotient.
```

순수한 finite 2-adic state는 폐기한다. 다음 rank는 실제 정수 크기와 증가하는 2-adic 정밀도를 함께 사용해야 한다.

## Remaining bridge / 남은 연결고리

The no-go theorem says what cannot work. It does not provide the required coupled rank. The next task is to derive exact changing-prefix macro-transitions and falsify candidate potentials that combine:

```text
bit length or logarithmic height,
cumulative valuation surplus,
affine branch constant,
and growing residue precision.
```

Success requires a uniform strict descent or basin-entry proof. A bounded fit, average drift, or fixed-prefix classifier remains insufficient.
