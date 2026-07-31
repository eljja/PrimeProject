# TICKET-168: Fixed neutral cores, least-realizer descent, phase-blind minimax, and Twin parity main terms

한국어 제목: **고정 중립 코어, 최소 실현값 하강, 위상 비인지 최소최대 정리, 쌍둥이 소수 parity 주항**

Status / 상태: `open_not_proven` for all four conjectures / 네 추측 모두 미해결

Generated / 생성: 2026-08-02 (Asia/Seoul)

## Abstract / 초록

TICKET-168 continues the four open nodes left by TICKET-167. It proves four
exact intermediate or target-correction theorems. It proves none of the four
parent conjectures.

For Riemann, a fixed finite-rank moment corrector turns any nested form core
into a nested dense pole-neutral core. An exact countermodel shows why changing
the constraint with the cutoff invalidates the cofinal argument. For Collatz,
the descent gap of all natural realizers of one contracting word is a strictly
increasing arithmetic progression, so the least natural realizer is the unique
worst case. For Goldbach, spectral `l1` is proved to be the minimax-optimal
uniform bound available from Fourier magnitudes alone; shell refinement without
arithmetic phase cannot recover cancellation. For Twin Prime, the finest
support-two parity projection is proved to contain exactly one half of the
desired odd gap-two correlation. The previous target of cancelling that term is
therefore rejected and replaced by a positive-main-term target.

TICKET-168은 TICKET-167이 남긴 네 미증명 노드를 이어 네 개의 정확한
중간 정리 또는 목표 교정 정리를 증명한다. 네 상위 추측은 하나도
해결하지 않는다.

리만 트랙에서는 고정된 유한랭크 moment 보정자를 사용하면 중첩 form
core를 중첩되고 조밀한 pole-neutral core로 바꿀 수 있음을 증명한다.
cutoff마다 제약을 바꾸면 각 유한 제한 form이 양성이어도 전역 음의
방향을 놓칠 수 있다. 콜라츠 트랙에서는 한 contracting word의 모든
자연수 실현값에 대한 하강 차이가 엄격히 증가하므로 최소 자연 실현값
하나가 유일한 최악 경우임을 증명한다. 골드바흐 트랙에서는 Fourier
크기만 보존하는 모든 방법의 최적 최악 상계가 spectral `l1`임을
증명한다. 쌍둥이 소수 트랙에서는 최미세 parity projection이 목표
gap-2 상관의 정확히 절반을 포함하므로 이를 `o(N)`으로 없애려던 기존
목표를 폐기한다.

## Result ledger / 결과 원장

| Problem / 문제 | Exact result / 정확한 결과 | Resolution / 해결 | Decisive next lemma / 다음 보조정리 |
|---|---|---|---|
| Riemann / 리만 | `FixedMomentCorrectorCoreBridgeAndCutoffVaryingConstraintNoGo` | open / 미해결 | `CofinalIntervalLDLCertificatesOnFixedPoleNeutralGuinandWeilCore` |
| Collatz / 콜라츠 | `LeastRealizerDescentMonotonicityAndModularShadowNoGo` | open / 미해결 | `UniformLeastRealizerEndpointDescentForEveryFirstCrossingWord` |
| Goldbach / 골드바흐 | `PhaseBlindSpectralL1MinimaxAndMagnitudeOnlyNoGo` | open / 미해결 | `UniformTargetDependentBinaryGoldbachPhaseCancellationBelowAnchorMargin` |
| Twin Prime / 쌍둥이 소수 | `FinestParityHalfCorrelationIdentityAndCancellationTargetNoGo` | open / 미해결 | `PositiveLinearOddVonMangoldtFinestParityPairing` |

## 1. Riemann hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `V_N` be nested finite-dimensional subspaces whose union `D` is dense in
the form norm. Let

```text
L : form domain -> F^r
```

be continuous. Suppose a fixed right inverse `U` satisfies `L U=I` and has
range in one finite space `V_N0`. Define

```text
P = I-U L,
W_N = V_N intersect ker L.
```

Then, for every `N>=N0`,

```text
P(V_N)=W_N.
```

The spaces `W_N` are nested and their union is form-dense in `ker L`.
Consequently the TICKET-167 cofinal vanishing-defect certificate can be applied
on `W_N`.

고정된 연속 moment map `L`과 고정 right inverse `U`가 있으면
`P=I-UL`은 제약을 정확히 제거하는 bounded projection이다. 이 보정자는
모든 cutoff에서 동일하므로 neutral core의 중첩성과 조밀성이 함께
보존된다.

### Proof / 증명

The identity `L U=I` gives

```text
P^2=P,       L P=0,       P x=x for x in ker L.
```

For `N>=N0`, both `v` and `U L v` lie in `V_N`; hence `P(V_N)` is contained in
`V_N intersect ker L`. Conversely every vector in the intersection is fixed by
`P`, giving equality. If `x` is in `ker L` and `v_j` in `D` converges to `x` in
form norm, continuity of `P` gives

```text
P v_j -> P x=x.
```

This proves density. TICKET-167 then promotes cofinal lower bounds with defect
approaching zero to nonnegativity on the constrained form closure.

### Cutoff-varying no-go / cutoff 가변 제약 no-go

On the first two coordinates, take

```text
Q = [[1,-2],[-2,1]]
```

and use identity on the remaining coordinates. At even cutoffs impose `x_1=0`;
at odd cutoffs impose `x_2=0`. Every restricted minimum is exactly one, but

```text
Q(e_1+e_2)=-2.
```

The constrained spaces are not nested and do not represent one fixed global
kernel. Therefore positive restrictions obtained after independently changing
the neutralization condition cannot be promoted by the cofinal theorem.

### Computation and limit / 계산과 한계

The exact rational proxy uses two bounded moments

```text
L_1(x)=sum_i x_i/i,
L_2(x)=sum_i (-1)^i x_i/i
```

and a corrector supported on the first two coordinates. At dimensions
`4,8,16,32,64`, exact rational arithmetic verifies `L U=I`, `P^2=P`, `L P=0`,
rank `P=N-2`, and consistency under zero-padding.

이 계산은 Guinand-Weil matrix가 아니다. 실제 다음 보조정리
`CofinalIntervalLDLCertificatesOnFixedPoleNeutralGuinandWeilCore`는 문헌의
pole-neutral test family에서 동일한 form-norm continuity와 고정 보정자를
확립하고, 그 core의 cofinal 구간 LDL 인증까지 제공해야 한다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

For fixed contracting affine word data

```text
T_w(n)=(3^m n+C)/2^S,
D=2^S-3^m>0,
M=2^(S+1),
```

write all nonterminal natural realizers as

```text
n_k=n_0+kM.
```

If `u_k=T_w(n_k)`, then

```text
u_k=u_0+2*3^m*k,
n_k-u_k=(n_0-u_0)+2Dk.                    (1)
```

Thus the descent gap is strictly increasing. Every natural realizer of the
word descends if and only if the least natural realizer descends.

### Proof / 증명

Substitution of `n_k` into the affine map gives

```text
T_w(n_k)=u_0 + 3^m*2^(S+1)k/2^S
        =u_0+2*3^m*k.
```

Subtracting from `n_k` proves (1), whose increment is `2D>0`. The TICKET-167
numerator slack also factors exactly as

```text
n_0D-C=2^S(n_0-u_0).                      (2)
```

Therefore the all-realizer counting problem is reduced without loss to one
endpoint comparison for the least residue representative.

### Modular-shadow no-go / 합동 그림자 no-go

For the synthetic affine family `m=1,S=2`, the corrections

```text
C=1,9,17
```

are identical modulo the realizer modulus `8` and all have `n_0=9`. Their least
odd endpoints are respectively `7,9,11`, so the descent gaps are `2,0,-2`.
Hence `(m,S,C mod M)` cannot determine natural descent over unrestricted affine
data. The integer lift of `C`, not only its modular shadow, is essential in that
larger class.

Only `C=1` is the actual one-step Collatz word. The other corrections are
synthetic affine information-class witnesses. They are not Collatz words, do
not show that the modular tuple is insufficient inside the realizable-word
class, and are not trajectory counterexamples.

### Computation and limit / 계산과 한계

The exact first-crossing enumeration is extended through word length `20`. It
counts `7,553,085` potential non-descent words and finds zero bad natural
realizers. The minimum exact numerator slack remains `192`.

길이 20까지의 계산은 유한 정리다. 길이 21 이후를 추론하지 않는다.
다음 보조정리 `UniformLeastRealizerEndpointDescentForEveryFirstCrossingWord`
는 모든 길이의 실제 valuation word에서 `n_0>u_0`를 증명하거나 실제
반례 word를 찾아야 한다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

On a cyclic group of length `L`, fix Fourier magnitudes

```text
a_k=|hat f(k)|.
```

Among every assignment of coefficient phases with these magnitudes,

```text
sup_phases ||f||_infinity = (1/L) sum_k a_k.       (3)
```

For conjugate-paired magnitudes, equality can be attained by a real-valued
signal. Consequently spectral `l1` is the minimax-optimal uniform certificate
available from magnitudes alone.

### Proof / 증명

Fourier inversion and the triangle inequality give the upper bound in (3).
Fix a target `x_0` and choose each coefficient phase to cancel the character
phase at `x_0`. Every inverse-transform term is then positive real at `x_0`, so
equality holds. Choosing opposite frequencies as conjugate pairs preserves
reality.

따라서 shell 크기와 shell `l2` 에너지처럼 Fourier magnitude만 사용하는
상계는 spectral `l1`보다 본질적으로 강해질 수 없다. 실제 신호에서
관측되는 위상 상쇄는 target-dependent phase 정보를 보존해야만 사용할
수 있다.

### Magnitude-only no-go / 크기 전용 no-go

The exact aligned family has `J` modes of normalized magnitude `1/J`. Its
spectral `l1` is one and an aligned phase assignment attains value one at one
target for every `J`. Increasing the shell count or square-summing magnitudes
does not create a pointwise subunit certificate.

### Finite diagnostic and limit / 유한 진단과 한계

For the repository's `16,384`-target Farey-mask diagnostic, bandwidths
`16,64,256,1024,4096` have observed high-frequency tails between approximately
`0.12` and `0.17`. The minimax-optimal phase-blind bounds remain between `1.37`
and `2.69`, or about `11` to `18` times the observed tail.

이 차이는 Goldbach 증명이 아니라 현재 정보 표현의 실패를 수치화한다.
다음 보조정리
`UniformTargetDependentBinaryGoldbachPhaseCancellationBelowAnchorMargin`은
실제 prime exponential sum의 산술 위상을 유지하면서 모든 target에서
low-pass anchor margin 아래의 상쇄를 증명해야 한다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

Let `a` be any real sequence supported on odd indices and set `A=a a^T`. For
the noncyclic shift-two selector `D_2` and its finest support-two product-Haar
projection `P_fine D_2`,

```text
<A,P_fine D_2>
  = <A,(I-P_fine)D_2>
  = (1/2) sum_n a_n a_(n+2).               (4)
```

The finest parity scale therefore contains exactly half of the desired odd
gap-two correlation. The coarse completion contains the other half.

### Proof / 증명

For `h_r=e_(2r)-e_(2r+1)`, the adjacent-block coefficient of `A` is

```text
(a_(2r)-a_(2r+1))(a_(2r+2)-a_(2r+3)).
```

Odd support makes this `a_(2r+1)a_(2r+3)`. The corresponding coefficient of
`D_2` is `2`, while product-Haar normalization divides by `2*2`. Summing gives
one half of the full shift-two pairing. Subtracting the finest projection from
the full selector gives the identical remaining half.

### Cancellation-target no-go / 상쇄 목표 no-go

TICKET-167 proposed

```text
PrimeWeightedFinestParityCancellationAndCoarseHaarTailPowerSaving.
```

Equation (4) shows that an `o(N)` bound on the finest term is not a route to a
positive linear twin-prime lower bound. It would force the odd gap-two
correlation itself to be `o(N)`. The finest term is a main-term location, not a
parity error that should be cancelled.

### Computation and limit / 계산과 한계

Exact product-Haar sums on the all-odd model through `N=256` verify (4)
independently of the closed formula. Exact prime-indicator rows through
`N=65,536` find `860` twin pairs and split the finite pairing into `430+430`.

이 유한 소수 계수는 무한성을 증명하지 않는다. 다음 보조정리
`PositiveLinearOddVonMangoldtFinestParityPairing`은 odd von Mangoldt weight의
최미세 pairing에 양의 선형 하한을 주어야 한다. 이는 실질적인 sieve
parity/Type II 장벽을 그대로 포함하므로 항등식만으로는 해결되지 않는다.

## Proof DAG / 증명 DAG

```text
Riemann:
  cutoff-dependent neutral spaces form one promotable core [REFUTED]
    -> fixed-moment corrector and nested kernel-core bridge [PROVED]
    -> cofinal interval LDL on a fixed pole-neutral Weil core [OPEN]

Collatz:
  unrestricted affine modular shadow determines actual-word descent [REFUTED]
    -> least-realizer descent monotonicity [PROVED]
    -> least realizer descends for every first-crossing word [OPEN]

Goldbach:
  phase-blind shell refinement recovers arithmetic cancellation [REFUTED]
    -> spectral-l1 phase-blind minimax theorem [PROVED]
    -> target-dependent arithmetic phase cancellation below margin [OPEN]

Twin Prime:
  cancel the finest parity scale to prove Twin Prime [REFUTED]
    -> finest parity scale equals half the target correlation [PROVED]
    -> positive linear odd-von-Mangoldt finest pairing [OPEN]
```

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket168_fixedcore_leastrealizer_phase_paritymain.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket168_fixedcore_leastrealizer_phase_paritymain
```

Generated artifacts / 생성 산출물:

```text
data/open-problem/ticket168-fixedcore-leastrealizer-phase-paritymain.json
data/open-problem/riemann/rh-ticket-168-fixed-neutral-core.json
data/open-problem/collatz/co-ticket-168-least-realizer.json
data/open-problem/goldbach/gb-ticket-168-phase-minimax.json
data/open-problem/twin-prime/tp-ticket-168-parity-main-term.json
```

## Literature boundary / 문헌 경계

- A. Groskin, [A finite Guinand-Weil dictionary and archimedean tail order for
  the truncated Weil quadratic form](https://arxiv.org/abs/2607.02828).
  The finite dictionary, pole-neutral subfamily, positive tail, and interval-LDL
  context are external. The fixed-constraint density theorem is project-local.
- C. Liu, [Counting the Collatz numbers](https://arxiv.org/abs/2512.13760).
  Congruence constructions for many convergent starts do not prove the
  all-first-crossing least-realizer theorem required here.
- L. Grimmelt and G. Bhowmik, [The exceptional set of the Goldbach
  problem](https://arxiv.org/abs/2607.27282). Exceptional-set and explicit
  major-arc results do not provide the target-dependent phase certificate.
- K. Ford and J. Maynard, [On the theory of prime producing
  sieves](https://arxiv.org/abs/2407.14368). Their framework establishes the
  necessity of substantial Type II information in broad prime-producing sieve
  problems; the parity identity here supplies no such estimate.

## Claim boundary / 주장 경계

TICKET-168 proves four exact intermediate or target-correction statements and
four restricted no-go results. It proves no Riemann-zero exclusion, no
all-natural Collatz descent, no all-even Goldbach representation theorem, and
no positive asymptotic for twin primes. The machine resolution count remains
zero.

TICKET-168은 네 개의 정확한 중간 또는 목표 교정 정리와 네 개의 제한된
경로 반례를 확정한다. 리만 영점 배제, 모든 자연수의 콜라츠 하강, 모든
짝수의 골드바흐 표현, 쌍둥이 소수의 양의 점근 하한은 증명하지 않았다.
기계 판독 해결 수는 0이다.
