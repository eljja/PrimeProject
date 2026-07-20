# TICKET-135: Conditional Bridges and Exceptional-Set Boundaries

Date: 2026-07-21

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket135-conditional-bridges-and-exceptional-set.json`

## Publication boundary / 논문 제출용 경계

**English.** TICKET-135 proves four exact intermediate theorems. They are a
generic block-operator positivity criterion, an almost-everywhere theorem for
2-adic Collatz valuation codes, a sharp finite-set norm bridge, and a CRT no-go
theorem for finite modular feature transcripts. None is a proof or disproof of
the Riemann Hypothesis, Collatz conjecture, strong Goldbach conjecture, or Twin
Prime conjecture. The computational tables replay exact identities and bounded
instances; they do not establish the remaining universal premises.

**한국어.** TICKET-135는 네 개의 정확한 중간 정리를 증명한다. 각각 일반
블록 연산자의 양성 조건, 2-adic Collatz valuation 코드의 거의 모든 점 정리,
유한 집합 위의 sharp norm 연결 정리, 유한 합동 feature transcript에 대한 CRT
no-go 정리다. 어느 것도 리만 가설, Collatz 추측, 강한 Goldbach 추측, Twin
Prime 추측의 증명이나 반증이 아니다. 계산표는 정확한 항등식과 유한 사례를
재생할 뿐 남은 전칭 전제를 증명하지 않는다.

## Result table / 결과표

| Problem / 문제 | Exact new result / 새 정확 결과 | Discarded route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 가설 | `SharpBlockTailPositivityCertificate` | finite Gram positivity without tail and cross bounds / 꼬리·교차항 상계 없는 유한 Gram 양성 | `ProjectedWeilBlockConstantsWithPositiveSchurMargin` |
| Collatz / 콜라츠 | `MinimalNegativeSlopePrefixesFormFullMeasurePrefixFreeCover` | almost-everywhere 2-adic cover implies every natural orbit / 2-adic 전측도에서 모든 자연수로의 승격 | `NaturalCodesCrossAffineDescentThreshold` |
| Goldbach / 골드바흐 | `SparseHardStratumMomentToMaximumBridge` | global sublog moments or norm promotion without `h^(1/p)` / 보정계수 없는 평균-점별 승격 | `BinaryGoldbachHardStratumLogMomentBoundK56` |
| Twin Prime / 쌍둥이 소수 | `FiniteCongruenceTranscriptCompositeLift` | finite modular transcripts as sufficient primality certificates / 유한 합동 정보를 소수성 충분조건으로 사용 | `NonCongruenceTypeIITwinSeparation` |

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `H=F direct-sum T` and let

```text
M = [[A, B], [B*, C]]
```

be self-adjoint. Assume

```text
A >= alpha I,   C >= gamma I,   ||B|| <= beta,
alpha >= 0,     gamma >= 0,     beta^2 <= alpha*gamma.
```

Then `M>=0`. The threshold is sharp among criteria that use only
`alpha,gamma,beta`.

### Proof / 증명

For `u=||x||`, `v=||y||`, Cauchy-Schwarz gives

```text
<M(x,y),(x,y)> >= alpha*u^2 - 2*beta*u*v + gamma*v^2.
```

If `alpha>0`, the right side equals

```text
alpha*(u-beta*v/alpha)^2 + (gamma-beta^2/alpha)*v^2 >= 0.
```

If `alpha=0`, the assumed inequality forces `beta=0`, so the conclusion is
immediate. Conversely, when `alpha>0` and `beta^2>alpha*gamma`, the scalar block
`[[alpha,-beta],[-beta,gamma]]` evaluated at `(beta,alpha)` equals
`alpha*(alpha*gamma-beta^2)<0`.

한국어로 말하면, 유한 코어의 하한만으로는 충분하지 않다. 꼬리의 하한과
core-tail 교차항의 노름 상계가 함께 있어야 하며, 세 상수만으로 판단할 때
`beta^2<=alpha*gamma`는 더 개선할 수 없는 경계다.

### Remaining gap / 남은 간극

No actual projected Weil decomposition has yet supplied certified values of
`alpha`, `gamma`, and `beta` with positive Schur margin. The theorem is a valid
bridge contract, not RH positivity itself.

실제 Weil quadratic form에 대해 outward-rounded 상수 세 개를 얻지 못했다.
따라서 이 정리는 RH 양성의 입력 규격이지 RH 증명이 아니다.

## 2. Collatz Conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

Under normalized Haar measure on odd 2-adic integers, accelerated valuations
`a_j` are independent and satisfy `P(a_j=m)=2^-m`. Almost every code has a first
`k` such that

```text
2^(a_1+...+a_k) > 3^k.
```

The minimal crossing words are prefix-free and their cylinder masses sum to
one.

### Proof / 증명

A word `(a_1,...,a_k)` has conditional odd-Haar mass
`2^-(a_1+...+a_k)`, so the letters have the stated independent geometric law.
The strong law gives

```text
(a_1+...+a_k)/k -> E[a_1] = 2 > log_2(3).
```

Thus a crossing occurs almost surely. Selecting the first crossing makes the
cylinders disjoint and prefix-free; their union has measure one.

홀수 2-adic 확률공간에서는 평균 valuation `2`가 `log_2(3)`보다 크므로 거의
모든 코드의 선형 계수 `3^k/2^S`가 결국 1보다 작아진다. 최초 교차 접두사만
모으면 중복 없는 전측도 덮개가 된다.

### No-go correction / 폐기 경로

This is **slope contraction**, not pointwise integer descent. The exact iterate
contains a positive affine term. Natural positive odd integers are also a
countable dense Haar-null subset, so an almost-everywhere theorem can miss all
of them. Promoting this result to Collatz would be a quantifier error.

이는 **기울기 수축**이지 특정 자연수의 실제 하강이 아니다. 정확한 반복식의
양의 affine 항을 넘어야 하고, 자연수 코드는 가산·조밀하지만 Haar 측도 0이다.
전측도 결과를 모든 자연수 결과로 승격하는 것은 논리 오류다.

## 3. Strong Goldbach Conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

For a function `r` on a finite hard stratum `H`, `|H|=h>=2`, use the normalized
norm

```text
||r||_p = (h^-1 sum_(n in H) |r(n)|^p)^(1/p).
```

Then

```text
||r||_infinity <= h^(1/p) ||r||_p,
```

and the constant is sharp. For `p=4 ceil(log_2 h)`, the factor is below `6/5`.
Hence `||r||_p <= (5/6)m_56` implies `||r||_infinity<m_56`.

### Proof / 증명

The maximum p-th power is bounded by the sum; a one-point spike gives equality.
Writing `m=ceil(log_2 h)` gives `h<=2^m`, and therefore

```text
h^(1/(4m)) <= 2^(1/4) < 6/5,
```

where the strict rational guard is `(6/5)^4-2=46/625>0`.

최대 항은 p제곱 합보다 작고 한 점 spike가 상수를 정확히 달성한다. powers of
two hard stratum은 `h=O(log X)`이므로 필요한 차수는 전역 `O(log X)`가 아니라
이 층 안에서 `O(log log X)`까지 내려간다.

### Remaining gap / 남은 간극

No estimate of this strength has been proved for the actual binary Goldbach
residual on a rigorously fixed hard stratum. The theorem improves the target
norm and constants; it does not prove a representation.

실제 binary Goldbach residual에 대한 해당 모멘트 상계가 없다. 목표의 크기를
줄였을 뿐 Goldbach 표현을 얻은 것은 아니다.

## 4. Twin Prime Conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

Any finite exact transcript `(n mod m_i)` factors through one residue
`a mod L`, where `L=lcm(m_i)`. If `gcd(a(a+2),L)=1` and distinct primes `q,r`
do not divide `L`, CRT constructs the same transcript with

```text
q | n,   r | (n+2),   n < 2Lqr,
```

and both `n,n+2` proper composite.

Therefore no locally admissible transcript is a sufficient certificate of twin
primality. A stronger classifier-impossibility conclusion is conditional: it
holds for a transcript only when that same transcript also has a twin-prime
realizer in the stated range.

### Proof / 증명

Solve

```text
n=a mod L,   n=0 mod q,   n=-2 mod r.
```

The least solution is below `Lqr`. If either forced divisor is not proper, add
one CRT period. The result is below `2Lqr` and preserves every feature.

서로 겹치는 합성수 modulus를 포함해도 모든 정확한 나머지 정보는 최소공배수
`L`의 한 residue로 합쳐진다. CRT로 같은 관측값을 갖는 합성수 쌍을 정량적
범위 안에 만들 수 있다. 따라서 locally admissible transcript 자체는 쌍둥이
소수성의 충분조건이 아니다. 다만 모든 분류기의 불가능성을 말하려면 같은
transcript 안에 실제 twin pair도 존재한다는 추가 조건이 필요하다.

### Remaining gap / 남은 간극

The no-go theorem applies only to information measurable through a finite exact
modular transcript. A genuinely non-congruence Type II correlation can escape
it. No positive exact-gap-two lower bound has been proved.

유한 합동 transcript 밖의 Type II 상관은 이 no-go의 적용 대상이 아니다.
exact gap 2의 양의 하계는 여전히 없다.

## Literature boundary / 문헌 경계

- M. Suzuki, [Weil's quadratic form via the screw function](https://arxiv.org/abs/2606.09096): continuous Weil-form context; PrimeProject imports no RH positivity conclusion.
- D. Bernstein and J. Lagarias, [The 3x+1 Conjugacy Map](https://doi.org/10.4153/CJM-1996-060-x): 2-adic symbolic context; the pointwise natural-number bridge remains separate.
- L. Zhao, [The exceptional set of Goldbach problem](https://arxiv.org/abs/2511.05631): exceptional-set progress does not supply the hard-stratum pointwise residual bound used here.
- K. Ford and J. Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368): modern sieve context; no exact-gap-two conclusion is imported.

These references locate the four routes in current literature. The exact
TICKET-135 statements are proved in this report from their displayed
assumptions; bibliographic context is not counted as a missing proof step.

위 문헌은 네 경로의 학술적 위치를 제시한다. TICKET-135의 정확 명제는 이
문서에 표시한 가정에서 직접 증명되며, 문헌의 관련 결과를 난제의 누락된
증명 단계로 대신 사용하지 않는다.

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket135_conditional_bridges_and_exceptional_set.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket135_conditional_bridges_and_exceptional_set
```

Generated artifacts:

- `data/open-problem/ticket135-conditional-bridges-and-exceptional-set.json`
- `data/open-problem/riemann/rh-ticket-135-block-tail-certificate.json`
- `data/open-problem/collatz/co-ticket-135-full-measure-prefix-cover.json`
- `data/open-problem/goldbach/gb-ticket-135-hard-stratum-moment-bridge.json`
- `data/open-problem/twin-prime/tp-ticket-135-congruence-transcript-lifts.json`

## Final status / 최종 상태

All four conjectures remain `open_not_proven`. TICKET-135 narrows one target per
problem and permanently rejects one invalid promotion route per problem.

네 난제는 모두 `open_not_proven`이다. TICKET-135의 진전은 각 문제에서 다음
목표를 하나로 좁히고 잘못된 승격 경로 하나를 재현 가능한 정리로 폐기한 데
있다.
