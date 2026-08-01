# TICKET-169: KKT inertia, exact Collatz child lifts, spectral autocorrelation, and Twin prime-power removal

한국어 제목: **KKT 관성, 콜라츠 자식 lift, 스펙트럼 자기상관, 쌍둥이 소수 거듭제곱 제거**

Status / 상태: `open_not_proven` for all four conjectures / 네 추측 모두 미해결

Generated / 생성: 2026-08-02 (Asia/Seoul)

## Abstract / 초록

TICKET-169 audits the four open targets left by TICKET-168 before attempting
another scale extension. It proves four exact bridge or no-go results, but no
parent conjecture.

For the Riemann track, constrained positivity is converted exactly into the
inertia of a KKT saddle matrix. This avoids constructing a dense kernel
projector, while an unbounded-normal-curvature family proves that no fixed
penalty parameter can replace the constrained test. For Collatz, appending one
accelerated valuation is expressed as a unique lift among `2^a` prefix lifts.
An all-`q` counterexample family proves that a fixed `q`-bit residue automaton
cannot determine every next valuation. For Goldbach, the cyclic
autocorrelation of Fourier coefficients yields a phase-sensitive pointwise
bound. It is subunit on all five finite repository diagnostics, whereas an
exact pair of signals proves that diagonal Fourier energy alone is
insufficient. For Twin Prime, odd von Mangoldt correlation is decomposed into
the weighted twin-prime sum and an explicit `O(sqrt(x) log^3 x)` prime-power
contamination. Hence the positive linear pairing proposed by TICKET-168 is
already an endgame statement rather than an easier parity workaround.

TICKET-169는 단순히 계산 범위를 늘리기 전에 TICKET-168의 다음 목표가
실제로 충분한지 다시 감사한다. 네 개의 정확한 bridge 또는 no-go 정리를
증명하지만, 네 상위 추측은 해결하지 않는다.

리만 트랙에서는 제약된 이차형식의 양성을 KKT 안장행렬의 관성으로 정확히
바꾼다. 이 방식은 조밀한 kernel projector를 직접 만들지 않아도 된다.
동시에 제약의 법선 방향 음의 곡률이 커지면 하나의 고정 penalty로는
대체할 수 없음을 보인다. 콜라츠 트랙에서는 valuation `a`를 하나 붙일 때
기존 prefix의 `2^a`개 lift 중 정확히 하나가 자식 word를 실현함을
증명한다. 그러나 고정된 `q`비트 residue만으로 모든 다음 valuation을
결정할 수 없다는 반례 패밀리도 모든 `q>=2`에 대해 증명한다. 골드바흐
트랙에서는 Fourier 계수의 순환 자기상관으로 위상 정보를 유지하는 점별
상계를 얻는다. 쌍둥이 소수 트랙에서는 소수 거듭제곱 오염을 `o(x)`로
분리하여, 기존 양의 선형 pairing 목표가 사실상 결론 자체를 포함함을
밝힌다.

## Result ledger / 결과 원장

| Problem / 문제 | New exact result / 새 정확한 결과 | Resolution / 해결 | Decisive next lemma / 다음 핵심 보조정리 |
|---|---|---|---|
| Riemann / 리만 | `ConstrainedFormKKTInertiaBridgeAndFixedPenaltyNoGo` | open / 미해결 | `CofinalIntervalKKTInertiaCertificatesOnFixedPoleNeutralGuinandWeilCore` |
| Collatz / 콜라츠 | `ExactChildLiftRecurrenceAndFixedResidueMemoryNoGo` | open / 미해결 | `UniformPositiveLeastRealizerSlackInvariantUnderExactChildLifts` |
| Goldbach / 골드바흐 | `SpectralAutocorrelationPointwiseBridgeAndDiagonalEnergyNoGo` | open / 미해결 | `UniformBinaryGoldbachSpectralAutocorrelationBudgetBelowAnchorMargin` |
| Twin Prime / 쌍둥이 소수 | `OddVonMangoldtPrimePowerRemovalAndEndgameEquivalence` | open / 미해결 | `UniformCubicRoughCenteredIncidenceSpectralDecayWithPrimeProducingConstants` |

## 1. Riemann hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `B` be a real symmetric `n x n` matrix. Let `L` have full row rank `r`,
and let the columns of `Z` span `ker L`. Assume

```text
A = Z^T B Z
```

is nonsingular. Define the KKT matrix

```text
K = [[B, L^T],
     [L,   0]].
```

Then

```text
inertia(K) = inertia(A) + (r,r,0).             (1)
```

In particular, `B` is positive definite on `ker L` exactly when `K` has `n`
positive, `r` negative, and zero null directions.

`B`가 ambient 공간 전체에서 양수일 필요는 없다. 필요한 것은 고정된
제약공간 `ker L`에서의 양성이다. 식 (1)은 이 조건을 KKT 행렬의 양/음/영
고유값 개수로 바꾼다.

### Proof / 증명

Choose a right inverse `U` with `LU=I`. In coordinates `[Z,U]`, the constraint
matrix is `[0,I]`. Congruence elimination using nonsingular `A` separates the
restricted block from a `2r x 2r` saddle block

```text
[[D, I],
 [I, 0]].
```

The saddle block has `r` positive and `r` negative directions for every
symmetric `D`. Sylvester's law of inertia then gives (1).

This theorem also exposes a fixed-penalty no-go. Put the identity on `ker L`
and curvature `-M_N` on each normal direction, where `M_N -> infinity`. For a
fixed `tau`,

```text
B_N + tau L^T L
```

still has a negative normal direction whenever `M_N>tau`. Therefore one
cutoff-independent penalty cannot replace a cofinal constrained certificate.

### Computation and limit / 계산과 한계

Exact diagonal proxies at dimensions `4,8,16,32,64` have a positive identity
restriction of dimension `N-2`. Every KKT matrix has exact inertia `(N,2,0)`.
A fixed penalty `tau=64` becomes singular or indefinite as normal curvature
crosses 64, while the kernel restriction remains positive.

이 계산은 실제 Guinand-Weil form이 아니다. 다음 보조정리는 하나의 고정된
pole-neutral core에서 interval arithmetic로 KKT 관성을 cofinal하게
인증하고, 그 core가 전역 form domain에 조밀하다는 TICKET-168의 외부
전제를 실제로 연결해야 한다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

For an accelerated prefix with affine data `(m,S,C)`, let its least start be
`n_0` and its odd endpoint be `u_0`. Prefix lifts satisfy

```text
n_k = n_0 + k 2^(S+1),
u_k = u_0 + 2*3^m k.
```

To append valuation `a>=1`, inspect `0<=k<2^a`. Exactly one lift satisfies

```text
v_2(3u_k+1)=a.                                (2)
```

The child word has exact affine data

```text
(m+1, S+a, 3C+2^S).                           (3)
```

The selected lift is its least nonterminal natural realizer.

### Proof / 증명

Write

```text
3u_k+1 = 2(q + 3^(m+1)k),
q=(3u_0+1)/2.
```

The coefficient of `k` is odd. Condition (2) is therefore the unique affine
congruence

```text
q+3^(m+1)k = 2^(a-1) mod 2^a.
```

Applying the additional accelerated step directly gives (3). The `2^a` old
lifts form one complete period of the child realizer modulus, proving
minimality of the selected representative.

### Fixed-residue-memory no-go / 고정 residue 기억 no-go

For every `q>=2`, solve

```text
3u+1 = 0 mod 2^q.
```

Its two odd lifts modulo `2^(q+1)` have the same retained `q` bits. Exactly one
has next valuation `q`; the other has valuation greater than `q`. Thus no
fixed-width residue state determines every future accelerated branch. This is
an actual dynamical no-go for positive odd Collatz states, not the synthetic
affine shadow used in TICKET-168.

### Computation and limit / 계산과 한계

For prefix word `[2]`, appended valuations `1,...,8` select unique old lifts

```text
0, 3, 1, 5, 29, 45, 77, 13.
```

The all-`q` no-go is checked exactly for `q=2,...,16`; the proof covers every
`q>=2`. 그러나 이 재귀식은 무한 first-crossing tree 전체에서 양의 하강
slack을 보장하지 않는다. 다음 핵심 보조정리는 정확한 child lift 아래에서
보존되는 양의 least-realizer slack 불변량이어야 한다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

On a cyclic group of length `L`, write

```text
f(x) = L^(-1) sum_k F_k exp(2 pi i kx/L)
```

and define cyclic spectral autocorrelation

```text
C_h = sum_k F_(k+h) conjugate(F_k).
```

Then

```text
|f(x)|^2 = L^(-2) sum_h C_h exp(2 pi i hx/L),
||f||_infinity <= sqrt(sum_h |C_h|)/L.          (4)
```

Unlike the magnitude-only bound of TICKET-168, (4) retains relative phase.

### Proof / 증명

Expand `f(x) conjugate(f(x))` and group coefficient pairs by frequency
difference `h`. Fourier inversion gives the first identity. Applying the
triangle inequality to this Fourier series for `|f|^2` and taking a square
root gives (4).

### Diagonal-energy no-go / 대각 에너지 no-go

Two exact length-`L` signals can have identical

```text
C_0 = sum_k |F_k|^2 = L
```

but different uniform norms. One coefficient of size `sqrt(L)` gives norm
`L^(-1/2)`. All `L` coefficients of size one, aligned at one target, give norm
one. The full autocorrelation `l1` values are respectively `L` and `L^2`, so
(4) distinguishes them exactly. The diagonal energy alone cannot.

### Computation and limit / 계산과 한계

For the `16,384`-target Goldbach deficit proxy, bandwidths
`16,64,256,1024,4096` yield phase-sensitive bounds

```text
0.43061, 0.42574, 0.42459, 0.42502, 0.35299.
```

Each dominates the observed tail and is below one. This is a real improvement
over TICKET-168's phase-blind bounds `1.37` to `2.69`.

하지만 이 결과는 한 유한 proxy의 계산이다. 강한 골드바흐 추측을
증명하려면 실제 prime exponential sum에서 `sum_h |C_h|`를 target에 대해
균일하게 제어하고, 그 상계가 low-pass anchor의 실제 양의 margin보다
작음을 모든 충분히 큰 짝수에 대해 증명해야 한다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

Let `Lambda_o` be von Mangoldt weight restricted to odd integers. For `x>=4`,
the forward gap-two correlation satisfies

```text
sum_(2<=n<=x-2) Lambda(n)Lambda(n+2)
  = (log 2)^2 + sum_(n<=x-2) Lambda_o(n)Lambda_o(n+2).   (5)
```

The odd correlation decomposes as

```text
weighted twin-prime sum + higher-prime-power contamination. (6)
```

The contamination is nonnegative and bounded explicitly by

```text
2 sqrt(x+2) floor(log_2(x+2)) log^2(x+2)
  = O(sqrt(x) log^3 x) = o(x).                         (7)
```

### Proof / 증명

Only the even start `n=2` contributes to (5), because `Lambda` vanishes on
even numbers that are not powers of two and no later power of two has a
gap-two prime-power partner. Its contribution is
`Lambda(2)Lambda(4)=(log 2)^2`.

In (6), separate the case where both prime-power exponents are one. The number
of higher prime powers up to `x` is at most
`floor(log_2 x) sqrt(x)`. Either coordinate can contain one, and each product
weight is at most `log^2(x+2)`, giving (7).

### Endgame-target correction / 종결 목표 교정

TICKET-168 showed that the finest odd parity pairing is exactly half the odd
gap-two correlation. Equations (6)-(7) now show that a bound

```text
finest pairing >= c x
```

would leave a positive linear weighted twin-prime sum after subtracting
`o(x)`. It would therefore prove infinitely many twin primes. This target is
not an easier intermediate that bypasses the parity barrier; it already
contains the quantitative endgame.

Finite rows through `x=65,536` contain `860` twin-prime pairs and `41`
prime-power-contaminated pairs. 이 수치는 분해를 검증할 뿐 양의 점근 하한을
증명하지 않는다. 다음 실제 병목은 TICKET-161의 Type-II 경로로 돌아가
prime-producing constant를 가진 균일 centered-incidence decay를 증명하는
것이다.

## Proof DAG / 증명 DAG

```text
Riemann:
  ambient positivity or one fixed penalty replaces restriction [REFUTED]
    -> constrained KKT inertia equivalence [PROVED]
    -> cofinal interval KKT on the fixed pole-neutral Weil core [OPEN]

Collatz:
  one fixed residue width determines all next valuations [REFUTED]
    -> exact unique child-lift recurrence [PROVED]
    -> uniform positive least-realizer slack under all child lifts [OPEN]

Goldbach:
  diagonal Fourier energy controls pointwise deficit [REFUTED]
    -> full spectral-autocorrelation pointwise bridge [PROVED]
    -> uniform autocorrelation budget below the anchor margin [OPEN]

Twin Prime:
  positive linear finest pairing is an easier intermediate [REFUTED]
    -> prime-power removal and endgame equivalence [PROVED]
    -> prime-producing uniform Type-II spectral decay [OPEN]
```

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket169_kkt_childlift_autocorrelation_primepower.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket169_kkt_childlift_autocorrelation_primepower -v
```

Machine-readable artifacts / 기계 판독 결과:

```text
data/open-problem/ticket169-kkt-childlift-autocorrelation-primepower.json
data/open-problem/riemann/rh-ticket-169-kkt-inertia.json
data/open-problem/collatz/co-ticket-169-child-lift.json
data/open-problem/goldbach/gb-ticket-169-autocorrelation.json
data/open-problem/twin-prime/tp-ticket-169-prime-power-removal.json
```

## Literature boundary / 문헌 경계

- Riemann: [arXiv:2607.02828](https://arxiv.org/abs/2607.02828) supplies a
  finite Guinand-Weil dictionary and interval-LDL setting. It makes no RH
  claim, and PrimeProject's KKT bridge is project-local.
- Collatz: [arXiv:2502.00948](https://arxiv.org/abs/2502.00948) studies finite
  parity-vector phenomena and paradoxical behavior. It does not supply the
  all-branch slack invariant required here.
- Goldbach: [arXiv:2607.27282](https://arxiv.org/abs/2607.27282) provides
  exceptional-set and explicit major-arc context, not the uniform
  autocorrelation estimate asserted as the next target.
- Twin Prime: [Ford-Maynard, arXiv:2407.14368](https://arxiv.org/abs/2407.14368)
  explains the need for substantial Type-II information in a broad
  prime-producing sieve framework. TICKET-169 proves no such estimate.

## Claim boundary / 주장 경계

No Riemann, Collatz, strong Goldbach, or Twin Prime proof is claimed. No
counterexample to any of the four conjectures is found. The proved content is
limited to the four stated finite-dimensional or elementary exact theorems and
their reproducible finite diagnostics.

리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측 중 어느
것도 해결했다고 주장하지 않는다. 네 추측의 반례도 발견하지 않았다.
이번에 확정된 것은 위 네 bridge/no-go 정리와 재현 가능한 유한 계산뿐이다.
