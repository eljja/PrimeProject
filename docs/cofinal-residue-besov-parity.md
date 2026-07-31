# TICKET-167: Cofinal cores, exact Collatz realizer counts, Goldbach Besov tails, and the finest Twin parity scale

한국어 제목: **공종(cofinal) 코어, 콜라츠 실현값의 정확 계수, 골드바흐 Besov 꼬리, 쌍둥이 소수의 최미세 parity scale**

Status / 상태: `open_not_proven` for all four conjectures / 네 추측 모두 미해결

Generated / 생성: 2026-08-01 (Asia/Seoul)

## Abstract / 초록

TICKET-167 continues the four open nodes left by TICKET-166. It proves four
exact reduction or no-go statements, but no parent conjecture.

For Riemann, positivity certificates are needed only on a cofinal subsequence
of a nested dense form core, rather than at every intermediate dimension. A
codimension-one countermodel proves that nested positivity without form-core
density is insufficient. For Collatz, every fixed contracting valuation word
gets an exact closed formula for the number of non-descending natural
realizers. This number is always finite, so wordwise density zero is automatic
and cannot replace emptiness. For Goldbach, a Bernstein low-pass term and a
dyadic Fourier-shell `l1` budget give a pointwise sufficient condition. Aligned
disjoint frequency blocks prove that a square-summed scale average cannot
replace that `l1` budget. For Twin Prime, the finest `2x2` product-Haar scale of
the shift-two selector has exact energy `(N-2)/2`; coarse-scale control alone
therefore misses a linear correlation.

TICKET-167은 TICKET-166이 남긴 네 미증명 노드를 이어서 네 개의 정확한
환원 정리 또는 no-go 명제를 증명한다. 상위 추측은 하나도 해결하지
않는다.

리만 트랙에서는 모든 중간 차원이 아니라 조밀한 중첩 form core의
cofinal 부분수열만 인증해도 충분함을 보인다. 단, core가 조밀하지
않으면 모든 제한 form이 양성이어도 고정된 음의 방향을 놓칠 수 있다.
콜라츠 트랙에서는 고정된 contracting valuation word가 갖는 비하강
자연 실현값의 개수를 닫힌식으로 정확히 계산한다. 그 개수는 항상
유한하므로 word별 자연밀도 0은 자동이며 공집합을 뜻하지 않는다.
골드바흐 트랙에서는 Bernstein 저주파 항과 dyadic Fourier shell의
`l1` 합을 결합해 점별 충분조건을 만든다. 서로 다른 주파수 shell이 한
점에서 같은 위상으로 정렬될 수 있으므로 scale `l2` 평균은 충분하지
않다. 쌍둥이 소수 트랙에서는 shift-two 선택자의 최미세 `2x2`
product-Haar 에너지가 정확히 `(N-2)/2`임을 보여 coarse scale만
제어하는 경로를 폐기한다.

## Result ledger / 결과 원장

| Problem / 문제 | Exact result / 정확한 결과 | Resolution / 해결 | Decisive next lemma / 다음 보조정리 |
|---|---|---|---|
| Riemann / 리만 | `CofinalNestedCoreCertificateBridgeAndNonDenseSubspaceNoGo` | open / 미해결 | `CofinalCutoffFreeIntervalLDLCertificatesOnExplicitGuinandWeilCore` |
| Collatz / 콜라츠 | `ExactBadRealizerCountAndWordwiseDensityZeroNoGo` | open / 미해결 | `UniformZeroBadRealizerCountForEveryFirstCrossingValuationWord` |
| Goldbach / 골드바흐 | `BesovOneShellAnchorBridgeAndAlignedScaleL2NoGo` | open / 미해결 | `UniformBinaryGoldbachBesovOneTailBelowAnchorMargin` |
| Twin Prime / 쌍둥이 소수 | `FinestParityScaleExtractionAndCoarseControlNoGo` | open / 미해결 | `PrimeWeightedFinestParityCancellationAndCoarseHaarTailPowerSaving` |

## 1. Riemann hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let

```text
V_1 subset V_2 subset ...
```

be finite-dimensional subspaces whose union is a form core for a continuous
quadratic form `Q`. Let `N_j` be any cofinal increasing sequence. Suppose

```text
Q(x) >= -epsilon_j ||x||^2   for every x in V_(N_j),
epsilon_j -> 0.
```

Then `Q` is nonnegative on the form core and on its form closure. It is not
necessary to certify every intermediate dimension.

조밀한 중첩 form core에서 차원이 무한대로 가는 어떤 cofinal 부분수열을
택해도 된다. 그 부분수열의 interval lower bound가 `-epsilon_j`이고
`epsilon_j->0`이면 전체 core의 form은 비음이다. 따라서 TICKET-166의
"every nested core" 요구는 "one certified cofinal nested schedule"로
정확히 약화된다.

### Proof / 증명

Fix `x` in the union. It belongs to some `V_(N_j0)` and, by nestedness, to
every later certified space. Therefore

```text
Q(x) >= -epsilon_j ||x||^2       for every j >= j0.
```

Letting `j` tend to infinity gives `Q(x)>=0`. Form continuity extends this
inequality from the core to its closure.

### Non-dense no-go / 비조밀 no-go

On `l2`, take

```text
Q = diag(-1,1,1,...),
V_(N_j) = span{e_2,...,e_(N_j+1)}.
```

The spaces are nested and every restricted minimum is `1`, but `Q(e_1)=-1`.
Their union closes to `e_1^perp`, not the full form core. Hence nested positive
certificates without a density theorem prove nothing about the omitted
direction.

### Computation and limit / 계산과 한계

The JSON audits the cofinal schedule `N_j=2^j` on the exact rational proxy
`diag(1,1/2^2,...,1/N_j^2)`. Its LDL pivots remain positive while the minimum
falls to `1/65536` at `N=256`. This demonstrates the exact certificate contract
only. It is not a Guinand-Weil matrix.

실제 다음 보조정리는
`CofinalCutoffFreeIntervalLDLCertificatesOnExplicitGuinandWeilCore`이다.
명시적이고 조밀한 Weil core의 cofinal 차원열에서 cutoff-free interval
LDL 인증을 만들어야 한다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

For fixed accelerated affine data

```text
T_w(n) = (3^m n + C) / 2^S,
D = 2^S - 3^m > 0,
M = 2^(S+1),
```

the nonterminal odd starts that realize the valuation word and leave an odd
endpoint form one arithmetic progression

```text
n = n_0 + kM,       k >= 0,
```

where `n_0>=3` is the least solution of

```text
3^m n_0 + C = 2^S  (mod M).
```

The exact number of non-descending realizers is

```text
0,                                      if n_0 D > C,
floor((C-n_0 D)/(M D)) + 1,             otherwise.       (1)
```

### Proof / 증명

Divisibility by `2^S` with an odd quotient is exactly the displayed congruence
modulo `2^(S+1)`. Since `3^m` is odd, it is invertible modulo `M`, so one odd
residue class exists. Non-descent is exactly `nD<=C`. Intersecting the
arithmetic progression with this finite interval gives (1).

endpoint가 홀수라는 조건은 하나의 홀수 합동류를 정확히 정한다. 그
합동류와 비하강 부등식 `nD<=C`의 교집합을 세면 floor 공식이 나온다.
따라서 고정된 contracting word는 비하강 자연 실현값을 유한개만 가질
수 있다.

### Density-zero no-go / 밀도 0 no-go

Finiteness means every fixed word has bad-realizer natural density zero even
when its bad set is nonempty. The synthetic affine family

```text
m=1, S=2, D=1, M=8, C=9+8q
```

has least nonterminal realizer `n_0=9` and exactly `q+1` non-descending starts,
yet density zero for every `q`. These are synthetic affine data, not actual
Collatz valuation words. They refute an inference from the affine information
class; they are not Collatz counterexamples.

### Computation and limit / 계산과 한계

The exact count formula audits all `1,120,444` potential first-crossing words
through length `18` and finds zero bad realizers, with minimum numerator slack
`n_0D-C=192`. This is a finite theorem only. Length `19` and all later lengths
are not inferred from it.

다음 보조정리 `UniformZeroBadRealizerCountForEveryFirstCrossingValuationWord`
는 모든 길이에서 `n_0D-C>0`임을 증명하거나 실제 bad word를 제시해야
한다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

On a cyclic grid of length `L`, decompose a deficit into

```text
d = f_low + sum_j g_j,
```

where `f_low` has trigonometric degree `K`. Let `A` be its maximum on `q`
equally spaced anchors, with `q>pi K`, and let `Gamma_j` be the Fourier support
of `g_j`. Then

```text
||d||_infinity <= A/(1-pi K/q)
                  + sum_j sqrt(|Gamma_j|)||hat(g_j)||_2/L.       (2)
```

For an integer-valued Goldbach deficit in which an exception has magnitude at
least one, a right-hand side below one is a pointwise no-exception certificate.

### Proof / 증명

TICKET-166 gives the Bernstein bound for `f_low`. Fourier inversion followed
by Cauchy-Schwarz on each shell gives

```text
||g_j||_infinity <= sqrt(|Gamma_j|)||hat(g_j)||_2/L.
```

The triangle inequality over shells proves (2). The shell sum is a discrete
Besov-`l1` type budget: it preserves the possibility that every scale aligns at
the same target.

### Aligned-scale no-go / 동상 scale no-go

Choose one cosine in each of `J` disjoint frequency blocks and scale each to
height `1/J`. All blocks equal `1/J` at the origin, so their sum is one. Their
scale-`l2` amplitude is only `J^(-1/2)`. Thus a square-summed scale average can
vanish while the pointwise deficit remains one. The `l1` scale aggregation in
(2) cannot be replaced by an `l2` average without additional arithmetic phase
cancellation.

### Finite diagnostic and failure / 유한 진단과 실패

On the repository's 16,384-target Farey-mask diagnostic, bandwidths
`16,64,256,1024,4096` give combined bounds from approximately `5.27` down to
`3.51`. Every bound dominates the observed finite tail, but every one exceeds
the required threshold `1`.

이 실패는 숨기지 않는다. 현재 shellwise Cauchy 경로는 유한 모델에서도
너무 거칠다. 다음 보조정리
`UniformBinaryGoldbachBesovOneTailBelowAnchorMargin`은 실제 소수 산술의
상쇄를 사용해 Besov-`l1` 예산 자체를 1 아래로 낮춰야 한다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

Let `D_2(i,j)=1_(j=i+2)` be the noncyclic shift-two selector on an even
`N x N` grid. Its projection onto the finest support-two product-Haar scale
has exactly

```text
N/2 - 1
```

nonzero coefficients. Each contributes unit normalized energy, so

```text
||P_fine D_2||_F^2 = <P_fine D_2,D_2> = (N-2)/2.       (3)
```

### Proof / 증명

A support-two Haar vector has signs `(+1,-1)`. Shift by two maps every complete
row block to the next column block with the same signs. Hence exactly
`N/2-1` coefficients equal `2`; all other finest coefficients vanish. Each
squared coefficient is divided by `2*2`, giving (3).

shift 2는 길이 2 Haar block의 parity 부호를 그대로 다음 block으로
옮긴다. 따라서 최미세 scale 하나만으로 이미 선형 크기의 signed
correlation을 갖는다.

### Coarse-control no-go / coarse 제어 no-go

Take the error matrix to be `P_fine D_2`. It is orthogonal to every coarser
product-Haar scale, so any statistic that observes only those scales reports
zero. Nevertheless its shift-two pairing is `(N-2)/2`. Exact coarse control
therefore cannot imply `o(N)` twin correlation without a finest parity-scale
estimate.

At `N=256`, the finest energy is exactly `127` and is approximately `50.2%` of
the entire double-centered selector energy. This is selector geometry, not a
von Mangoldt estimate.

다음 보조정리
`PrimeWeightedFinestParityCancellationAndCoarseHaarTailPowerSaving`은
prime-weighted 오차에서 최미세 parity pairing과 나머지 coarse tail을
각각 `o(N)`으로 제어해야 한다.

## Proof DAG / 증명 DAG

```text
Riemann:
  every dimension is necessary, or any nested positive family suffices [REFUTED]
    -> cofinal dense-core certificate bridge [PROVED]
    -> cofinal cutoff-free interval LDL certificates on an explicit Weil core [OPEN]

Collatz:
  wordwise density zero implies no bad natural start [REFUTED]
    -> exact bad-realizer count [PROVED]
    -> zero bad-realizer count for every first-crossing word [OPEN]

Goldbach:
  scale-l2 average controls aligned pointwise deficit [REFUTED]
    -> Besov-one shell plus anchor bridge [PROVED]
    -> uniform arithmetic Besov-one tail below anchor margin [OPEN]

Twin Prime:
  coarse Haar control alone forces shift-two saving [REFUTED]
    -> exact finest parity-scale extraction [PROVED]
    -> prime-weighted finest cancellation and coarse-tail saving [OPEN]
```

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket167_cofinal_residue_besov_parity.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket167_cofinal_residue_besov_parity
```

Generated artifacts / 생성 산출물:

```text
data/open-problem/ticket167-cofinal-residue-besov-parity.json
data/open-problem/riemann/rh-ticket-167-cofinal-core.json
data/open-problem/collatz/co-ticket-167-realizer-count.json
data/open-problem/goldbach/gb-ticket-167-besov-tail.json
data/open-problem/twin-prime/tp-ticket-167-parity-scale.json
```

## Literature boundary / 문헌 경계

- A. Groskin, [A finite Guinand-Weil dictionary and archimedean tail order for
  the truncated Weil quadratic form](https://arxiv.org/abs/2607.02828).
  Cutoff-free interval LDL and the positive tail are external inputs; the
  cofinal dense-core reduction is the project-local result.
- C. Liu, [Counting the Collatz numbers](https://arxiv.org/abs/2512.13760).
  Congruence constructions for large classes of convergent starts do not imply
  the all-first-crossing-word zero-count lemma required here.
- L. Grimmelt and G. Bhowmik, [The exceptional set of the Goldbach
  problem](https://arxiv.org/abs/2607.27282). Exceptional-set and second-moment
  estimates do not supply the pointwise Besov-one budget.
- K. Ford and J. Maynard, [On the theory of prime producing
  sieves](https://arxiv.org/abs/2407.14368). Their Type I/II framework explains
  why substantial bilinear information is necessary; the Haar identity here
  is not a prime-producing estimate.

## Claim boundary / 주장 경계

TICKET-167 proves four exact intermediate statements and four restricted
proof-route no-go results. It proves no Riemann-zero exclusion, no all-natural
Collatz descent, no all-even Goldbach representation theorem, and no infinite
twin-prime lower bound. The machine resolution count remains zero.

TICKET-167은 네 개의 정확한 중간 명제와 네 개의 제한된 경로 반례를
확정한다. 리만 영점 배제, 모든 자연수의 콜라츠 하강, 모든 짝수의
골드바흐 표현, 무한한 쌍둥이 소수 하한은 증명하지 않았다. 기계 판독
해결 수는 0이다.
