# TICKET-166: Positive tails, start-adaptive Collatz windows, bandlimited Goldbach anchors, and shifted-diagonal Haar duality

한국어 제목: **양의 꼬리, 시작값 적응형 콜라츠 창, 대역 제한 골드바흐 표본, 이동 대각 Haar 쌍대성**

Status / 상태: `open_not_proven` for all four conjectures / 네 추측 모두 미해결

Generated / 생성: 2026-08-01 (Asia/Seoul)

## Abstract / 초록

TICKET-166 continues the four open obligations left by TICKET-165. It proves
four exact conditional, reduction, or no-go statements. None proves or
disproves its parent conjecture.

For Riemann, a positive-tail Galerkin theorem connects interval lower bounds on
a diagonal cutoff schedule to the vanishing-defect core limit from TICKET-165.
A scalar pair proves that a truncated eigenvalue inside the tail-budget band
does not determine the sign of the completed form. For Collatz, retaining the
natural start `n` sharpens the final-valuation window from `O(log m)` to
`O(log(1+m/n))`; if `m<=3n`, only zero excess survives. For Goldbach, a
Bernstein sampling theorem turns a uniform low-pass approximation and sparse
anchor margin into a pointwise certificate, while a unit spike proves that
sparse samples alone cannot control full bandwidth. For Twin Prime, the exact
`n,n+2` shifted-diagonal selector is expanded in product Haar coordinates. Its
double-centered copy saturates the signed dual bound, proving that zero row and
column margins plus unsigned energy do not imply a power saving.

TICKET-166은 TICKET-165가 남긴 네 미증명 의무를 이어서 네 개의 정확한
조건부 정리, 축소 정리 또는 no-go 명제를 증명한다. 어떤 결과도 상위
추측의 증명이나 반증이 아니다.

리만 트랙에서는 양의 꼬리를 가진 Galerkin form의 interval 하한이
TICKET-165의 소멸 결함 극한으로 이어지는 조건을 명시한다. 꼬리 예산
안의 음의 고윳값은 완성된 form의 부호를 결정하지 못한다는 1차원
반례도 제시한다. 콜라츠 트랙에서는 자연수 시작값 `n`을 이용해 마지막
valuation 잔여창을 `O(log m)`에서 `O(log(1+m/n))`으로 줄이며,
`m<=3n`이면 excess `0`만 남는다. 골드바흐 트랙에서는 저주파 균일
근사와 Bernstein 표본화를 결합해 점별 인증을 만들고, full-bandwidth
unit spike로 표본값만 사용하는 경로를 반박한다. 쌍둥이 소수 트랙에서는
`n,n+2` 대각 선택자의 product-Haar 쌍대식을 정확히 전개하고, 행·열
평균을 제거한 선택자가 쌍대 상계를 포화하므로 unsigned 에너지만으로는
power saving을 얻을 수 없음을 보인다.

## Result ledger / 결과 원장

| Problem / 문제 | Exact result / 정확한 결과 | Resolution / 해결 | Decisive next lemma / 다음 보조정리 |
|---|---|---|---|
| Riemann / 리만 | `PositiveTailDiagonalCoreBridgeAndAmbiguousBandNoGo` | open / 미해결 | `IntervalCertifiedTruncatedWeilLowerBoundAtVanishingTailScaleOnEveryNestedCore` |
| Collatz / 콜라츠 | `StartAdaptiveFinalExcessReductionAndZeroExcessMagnitudeNoGo` | open / 미해결 | `UniformNaturalResidueSlackInsideStartAdaptiveExcessWindow` |
| Goldbach / 골드바흐 | `BandlimitedAnchorClosureAndFullBandwidthSpikeNoGo` | open / 미해결 | `UniformDyadicLowPassApproximationAndAnchorMarginForBinaryMinorDeficit` |
| Twin Prime / 쌍둥이 소수 | `ShiftedDiagonalHaarDualityAndCenteredPermutationNoGo` | open / 미해결 | `PrimeWeightedShiftedDiagonalHaarPairingPowerSavingBeyondParity` |

## 1. Riemann hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `Q_N` be nested Galerkin compressions on a form core and suppose

```text
Q_N = A_(N,T_N) + R_(N,T_N),       R_(N,T_N) >= 0.
```

If rigorous interval bounds give

```text
lambda_min(A_(N,T_N)) >= -epsilon_N,       epsilon_N -> 0,
```

then `Q_N>=-epsilon_N I`. Under the form-core convergence assumptions already
isolated in TICKET-165, the limiting quadratic form is nonnegative.

중첩 Galerkin core에서 cutoff form `A_(N,T_N)`와 생략된 양의 꼬리
`R_(N,T_N)`의 합이 cutoff-free 압축 `Q_N`이라고 하자. cutoff form의
최소 고윳값에 대한 interval 인증 하한이 `-epsilon_N`이고
`epsilon_N->0`이면, full compression도 같은 소멸 음의 결함 하한을
가진다. TICKET-165의 form-core 수렴 조건을 적용하면 극한 form이
비음이 아님을 얻는다.

### Proof / 증명

Positive semidefiniteness of `R_(N,T_N)` gives

```text
Q_N >= A_(N,T_N) >= -epsilon_N I.
```

The remaining limit is exactly the TICKET-165 vanishing-defect theorem. If an
available tail estimate has order

```text
B(N,T) = O((2N+1) log(T) / T),
```

the diagonal schedule `T=N^3` gives

```text
B(N,N^3) = O(log N / N^2) -> 0.
```

This rate substitution is exact. The numerical table in the JSON evaluates
the leading-order expression reported for `c=100`; it is explicitly a scale
diagnostic, not a new interval proof.

### Ambiguous-band no-go / 모호 구간 no-go

For any `B>0`, take the one-dimensional truncated form `A=-B/2`. Both

```text
R_0=0,     R_1=B
```

are positive and at most `B`, but

```text
A+R_0=-B/2<0,       A+R_1=B/2>0.
```

Therefore a negative truncated eigenvalue in `[-B,0)` and the tail budget
alone do not determine the completed sign. An interval lower bound on every
nested core, rather than an extrapolated eigenvalue, remains necessary.

같은 cutoff 값과 같은 꼬리 예산을 가진 두 완성이 서로 반대 부호를
만든다. 따라서 모호 구간의 수치 고윳값을 양성 또는 음성으로 승격하는
경로는 폐기한다.

### Limit / 한계

PrimeProject does not prove the positive-tail theorem or its explicit constant;
those are external results. It also does not certify the required lower bound
on every nested Weil core. The next lemma is
`IntervalCertifiedTruncatedWeilLowerBoundAtVanishingTailScaleOnEveryNestedCore`.

실제 모든 Weil core의 interval 하한을 얻지 못했으므로 RH 또는 영점
배제 결론은 없다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

For a first-crossing accelerated valuation word of length `m`, write its final
valuation as the least crossing valuation plus `t`. Let `n>=3` be an odd
natural realizer. If its endpoint does not descend, then

```text
3 n (2^t-1) < m.                                      (1)
```

Consequently every excess satisfying `3n(2^t-1)>=m` descends, and the exact
residual envelope contains

```text
min {u>=0 : 3n(2^u-1)>=m} = O(log(1+m/n))
```

integer values. If `m<=3n`, only `t=0` remains.

길이 `m`의 first-crossing word와 홀수 자연수 실현값 `n`을 함께 사용하면
비하강에 필요한 조건은 (1)이다. 따라서 시작값을 버린 TICKET-165의
`O(log m)` 창보다 작은 `O(log(1+m/n))` 창만 residue 분석에 남는다.

### Proof / 증명

TICKET-165 proved

```text
C <= m 3^(m-1),
D=2^S-3^m > (2^t-1)3^m.
```

Non-descent means `nD<=C`. Combining all three inequalities gives

```text
n(2^t-1)3^m < nD <= C <= m3^(m-1),
```

which is (1). The strict inequality also closes equality in the sufficient
gate, improving the earlier conservative `>` boundary.

### Zero-excess no-go / excess 0 no-go

At `t=0`, the left side of (1) is always zero. No amount of start-size
information can close this case through the same magnitude inequality. The
exact natural residue and affine correction must be compared. This is a no-go
for the magnitude-only method, not evidence for a divergent orbit.

`t=0`에서는 시작값이 아무리 커도 해당 부등식의 좌변이 0이다. 따라서
최소 crossing valuation은 정확한 자연수 residue 없이 닫히지 않는다.
이는 방법론의 한계이며 콜라츠 반례가 아니다.

### Limit / 한계

Long first-crossing times `m>>n` may retain several excess values, and no
uniform residue slack has been proved. The next lemma is
`UniformNaturalResidueSlackInsideStartAdaptiveExcessWindow`.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

Let `f` be a trigonometric polynomial of degree `K` and sample it at `q`
equally spaced circle anchors. If

```text
A = max_anchor |f|,       q > pi K,
```

then

```text
||f||_infinity <= A / (1-pi K/q).                       (2)
```

If a target deficit sequence `d_j` obeys `|d_j-f(x_j)|<=eta`, then

```text
max_j d_j <= A/(1-pi K/q) + eta.                        (3)
```

The right side below one is a pointwise no-exception certificate.

### Proof / 증명

Every point is within `pi/q` of an anchor. Bernstein's classical inequality
`||f'||_infinity<=K||f||_infinity` gives

```text
M <= A + (pi K/q)M.
```

Rearrangement proves (2), and the triangle inequality proves (3).

모든 점을 가장 가까운 anchor와 연결하고 Bernstein 미분 부등식을
적용하면 (2)가 나온다. 저주파 모델과 실제 deficit의 균일 오차 `eta`를
더하면 (3)을 얻는다.

### Full-bandwidth no-go / 전 대역 no-go

A unit spike on a cyclic grid has a nonzero DFT coefficient at every
frequency. If anchors omit the spike, every anchor value is zero while the
pointwise maximum remains one. Therefore sparse anchors without a bandwidth,
uniform-approximation, or direct-variation theorem cannot exclude one Goldbach
exception.

### Finite diagnostic / 유한 진단

The repository's floating Farey-mask model on `(32768,65536]` has 16,384 even
targets. Low-pass bandwidths `16,64,256,1024,4096` with `q=4K` give computed
Bernstein-plus-error upper envelopes between approximately `0.47` and `0.94`.
All are below one and dominate the finite observed maximum. These rows validate
the software bridge only; they are not interval certificates or an infinite
binary-Goldbach estimate.

### Limit / 한계

The missing result is a uniform low-pass approximation error and anchor margin
for the true minor-arc deficit on every dyadic shell:
`UniformDyadicLowPassApproximationAndAnchorMarginForBinaryMinorDeficit`.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

On an `N x N` matrix let

```text
D_h(i,j)=1 if j=i+h, and 0 otherwise,
```

without cyclic wraparound. Let `E` be the double centering of `D_h`, so every
row and column sum of `E` is zero. Then

```text
<E,D_h> = ||E||_F^2
        = sum_(I,J) |<E,h_I tensor h_J>|^2/(|I||J|).     (4)
```

For `M=N-h`, the common value is

```text
M - 2M/N + M^2/N^2.                                    (5)
```

### Proof / 증명

Double centering is the orthogonal projection onto the zero-row/zero-column
subspace. Hence `<E,D_h>=<E,E>`. Tensor Haar Parseval proves the second
identity in (4). Expanding the row, column, and grand means gives (5).

이중 중심화는 행합과 열합이 0인 부분공간으로의 직교투영이다. 따라서
선택자와의 signed pairing이 중심화 선택자의 에너지와 같고, product-Haar
Parseval로 모든 비등방 scale pair의 합과도 같아진다.

### Centered-selector no-go / 중심화 선택자 no-go

Taking the error matrix itself to be `E` saturates Cauchy-Schwarz. Its row and
column sums vanish and its unsigned energy is `Theta(N)`, yet its shifted
diagonal correlation is also `Theta(N)`. Thus centering plus an `O(N)` norm
bound does not provide the `o(N)` cancellation needed for a twin-prime lower
bound. Signed prime-weighted coefficients must cancel against the exact
shifted-diagonal selector.

이는 결정론적 반례 행렬이지 von Mangoldt 오차가 아니다. 따라서 parity
barrier를 넘었다는 결론은 없으며, 필요한 다음 보조정리는
`PrimeWeightedShiftedDiagonalHaarPairingPowerSavingBeyondParity`이다.

## Proof DAG / 증명 DAG

```text
Riemann:
  tail budget decides ambiguous sign [REFUTED]
    -> positive-tail diagonal core bridge [PROVED]
    -> interval lower bound on every nested Weil core [OPEN]

Collatz:
  start-blind window is sharp; magnitude closes t=0 [REFUTED]
    -> start-adaptive excess reduction [PROVED]
    -> natural residue slack inside adaptive window [OPEN]

Goldbach:
  sparse anchors control full bandwidth [REFUTED]
    -> bandlimited Bernstein bridge [PROVED]
    -> uniform dyadic low-pass error and anchor margin [OPEN]

Twin Prime:
  centered unsigned Haar energy forces diagonal saving [REFUTED]
    -> shifted-diagonal signed Haar duality [PROVED]
    -> prime-weighted shifted-diagonal power saving [OPEN]
```

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket166_tail_adaptive_bandlimited_diagonal.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket166_tail_adaptive_bandlimited_diagonal
```

Generated artifacts / 생성 산출물:

```text
data/open-problem/ticket166-tail-adaptive-bandlimited-diagonal.json
data/open-problem/riemann/rh-ticket-166-positive-tail-diagonal.json
data/open-problem/collatz/co-ticket-166-start-adaptive-excess.json
data/open-problem/goldbach/gb-ticket-166-bandlimited-anchor.json
data/open-problem/twin-prime/tp-ticket-166-shifted-diagonal-haar.json
```

## Literature boundary / 문헌 경계

- A. Groskin, [A finite Guinand-Weil dictionary and archimedean tail order for
  the truncated Weil quadratic form](https://arxiv.org/abs/2607.02828). The
  positive-tail result and quantitative tail order are external premises.
- M. Inselmann, [An approximation of the Collatz map and a lower bound for the
  average total stopping time](https://arxiv.org/abs/2402.03276). Almost-all and
  average behavior do not supply the all-realizer residue lemma required here.
- L. Grimmelt and G. Bhowmik, [The exceptional set of the Goldbach
  problem](https://arxiv.org/abs/2607.27282). Exceptional-set and explicit
  major-arc results do not imply the pointwise binary estimate used as our open
  target.
- K. Ford and J. Maynard, [On the theory of prime producing
  sieves](https://arxiv.org/abs/2407.14368). Their Type I/II framework motivates
  the signed-information requirement; our matrix no-go is not a sieve theorem.

## Claim boundary / 주장 경계

TICKET-166 proves four exact intermediate statements and four restricted
proof-route no-go results. It proves no Riemann-zero exclusion, no all-natural
Collatz descent, no even-number Goldbach theorem, and no infinite twin-prime
lower bound. The machine resolution count remains zero.

TICKET-166은 네 개의 정확한 중간 명제와 네 개의 제한된 증명 경로
no-go를 확정한다. 리만 영점 배제, 모든 자연수의 콜라츠 하강, 모든 짝수의
골드바흐 표현, 무한한 쌍둥이 소수 하한은 증명하지 않았다. 기계 판독
해결 수는 0이다.
