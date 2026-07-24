# TICKET-136: Scale-Sensitive Obstructions and an Affine Descent Bridge

Date: 2026-07-25

Status: `open_not_proven` for all four conjectures

Machine record:
`data/open-problem/ticket136-scale-sensitive-obstructions-and-affine-bridge.json`

## Publication boundary / 논문 제출용 경계

**English.** TICKET-136 proves four elementary but exact intermediate
statements and records their machine replays. "New result" below means newly
established inside PrimeProject; no priority or literature-novelty claim is
made. None of the statements proves or refutes the Riemann Hypothesis, Collatz
conjecture, strong Goldbach conjecture, or Twin Prime conjecture. The finite
tables test implementations of the displayed identities. They are not promoted
to universal evidence.

**한국어.** TICKET-136은 기본적이지만 정확한 중간 명제 네 개를 증명하고
기계 재생 결과를 기록한다. 아래의 "새 결과"는 PrimeProject 안에서 새로
확정했다는 뜻이며, 학계 최초나 문헌상 독창성을 주장하지 않는다. 어느 명제도
리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측을 증명하거나
반증하지 않는다. 유한 계산표는 표시된 항등식의 구현을 검사할 뿐 전칭 명제의
증거로 승격되지 않는다.

## Result table / 결과표

| Problem / 문제 | Exact result / 정확 결과 | Discarded route / 폐기 경로 | One next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 가설 | `SchurTestWeilBlockBridgeAndEntrywiseDecayNoGo` | entrywise decay implies operator-norm decay / 원소별 감소에서 연산자 노름 감소 추론 | `ProjectedWeilAbsoluteRowColumnTailBoundsWithPositiveMargin` |
| Collatz / 콜라츠 | `LeastCounterexampleAffineCorrectionInequality` | slope contraction alone implies descent / 기울기 수축만으로 실제 하강 추론 | `UniformValuationSurplusBeyondAffineCorrectionForLeastCounterexampleCodes` |
| Goldbach / 골드바흐 | `FixedWheelRoughStratumHasLinearMassAndLogMomentBarrier` | powers-of-two `O(log log X)` moment applied to a fixed-wheel rough layer / powers-of-two 모멘트 차수의 전체 거친 층 확대 | `BinaryGoldbachGrowingWheelResidualBoundK56` |
| Twin Prime / 쌍둥이 소수 | `FiniteRationalFourierAlgebraCompositeLift` | finite rational Fourier features treated as non-congruence information / 유한 유리 Fourier 특성을 비합동 정보로 간주 | `AperiodicScaleGrowingTypeIITwinSeparation` |

## 1. Riemann Hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let

```text
M = [[A, B], [B*, C]]
```

be self-adjoint. Suppose

```text
A >= alpha I,  C >= gamma I,
sup_i sum_j |B_ij| <= R,  sup_j sum_i |B_ij| <= S.
```

Then `||B||_2^2 <= R*S`, so `R*S <= alpha*gamma` implies `M>=0`.
However, entrywise convergence of `B` to zero cannot replace the row and
column bounds.

### Proof / 증명

The Schur test gives

```text
||B||_2 <= sqrt(||B||_infinity ||B||_1) <= sqrt(R*S).
```

Substitution into the sharp block criterion proved in TICKET-135 yields the
positivity conclusion. For the obstruction, let `B_n=J_n/n`, where every entry
of `J_n` is one. Then

```text
max_ij |(B_n)_ij| = 1/n -> 0,
```

but the all-ones vector is an eigenvector of `B_n` with eigenvalue one.
Therefore `||B_n||_2=1` at every dimension.

한국어로 말하면, projected Weil 행렬의 각 원소가 작아진다는 사실만으로는
core-tail 결합의 연산자 노름이 작아진다고 결론낼 수 없다. 절댓값 행합과
열합처럼 차원 증가를 견디는 합가능성 추정이 필요하다.

### Remaining gap / 남은 간극

No fixed published projected Weil normalization is shown here to have a
positive tail gap or sufficiently small absolute row/column sums. The next
lemma must derive those actual constants with directed numerical rounding or
symbolic inequalities. The generic Schur test is not RH positivity.

특정 Weil 연산자에 대해 양의 꼬리 gap과 충분히 작은 행합·열합을 아직
증명하지 못했다. 일반 선형대수 정리를 얻었을 뿐 RH에 필요한 산술 입력은
열려 있다.

## 2. Collatz Conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

For the accelerated odd map

```text
n_(j+1) = (3n_j+1)/2^(a_j),  S_k = a_0+...+a_(k-1),
```

one has the exact identity

```text
n_k/n_0 =
  (3^k/2^S_k) product_(j<k) (1 + 1/(3n_j)).
```

If `n_j>=n_0` through step `k`, then

```text
2^S_k n_0^k <= (3n_0+1)^k.                 (1)
```

Consequently, strict reversal of (1) certifies descent by step `k`. A
hypothetical least counterexample must satisfy (1) for every `k`.

### Proof / 증명

Multiply the exact one-step ratios

```text
n_(j+1)/n_j = (3/2^(a_j)) (1+1/(3n_j)).
```

Under non-descent, each correction factor is at most
`1+1/(3n_0)`. Thus

```text
n_k/n_0 <= ((3n_0+1)/n_0)^k / 2^S_k.
```

Since the left side is at least one, (1) follows. If `n_0` were the least
counterexample and its orbit reached a smaller value, minimality would make
that smaller orbit reach one and hence make `n_0` reach one. Therefore a least
counterexample cannot descend and must obey (1) at every depth.

이는 기울기 `3^k/2^S_k`에 빠져 있던 양의 affine 보정항을 정확히 복원한다.
로그 형태로는 비하강 접두사마다

```text
S_k - k log_2(3) <= k log_2(1+1/(3n_0))
```

가 필요하다.

### No-go and remaining gap / 폐기 경로와 남은 간극

At `n_0=1`, every accelerated valuation is two. Hence `2^S_k>3^k` for
every `k`, but the orbit stays at one and never strictly descends. This exact
fixed-point counterexample retires slope contraction as a stand-alone descent
certificate.

`n_0=1`에서는 매 단계 valuation이 2라서 기울기는 계속 수축하지만 양의
보정항과 정확히 상쇄되어 값은 1에 머문다. 다음 보조정리는 가상의 최소 반례
코드에서 valuation surplus가 우변의 `n_0` 의존 보정량을 언젠가 엄격히
넘는다는 것을 증명해야 한다. 유한 궤적 검사는 이 전칭 명제를 증명하지 않는다.

## 3. Strong Goldbach Conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

For fixed odd squarefree `W`, define

```text
H_W(X) = {N <= X : N is even and gcd(N,W)=1}.
```

At complete periods `X=2WM`,

```text
|H_W(X)| = M*phi(W).
```

Therefore this rough stratum has positive linear density. For normalized
`L^p`, keeping the sharp inflation `h^(1/p)` below `6/5` requires

```text
p >= log(h)/log(6/5) = Theta(log X).
```

### Proof / 증명

Write `N=2m`. In each block of `W` consecutive values of `m`, exactly
`phi(W)` are coprime to `W`, proving the count. TICKET-135 proved the sharp
finite-set inequality

```text
||r||_infinity <= h^(1/p) ||r||_p.
```

Solving `h^(1/p)<=6/5` gives the displayed lower bound. A one-point spike
attains equality, so no inference using only a normalized
`p=O(log log X)` moment can control every point of a fixed-wheel rough
stratum.

powers of two는 `X`까지 `O(log X)`개뿐이지만, 고정 wheel의 작은 소인수를
피하는 짝수는 `Theta(X)`개다. 따라서 powers-of-two 층에서 얻은
`O(log log X)` 차수를 전체 rough hard stratum으로 확대할 수 없다.

### Remaining gap / 남은 간극

The spike is a countermodel to a norm-promotion inference, not a statement
about the actual Goldbach residual. A viable next route must let the wheel grow
with `X` and prove a residual budget uniform in both scales, including all
complementary strata. No `K=56` minor-arc estimate is supplied here.

한 점 spike는 추론 방식의 반례이지 실제 Goldbach residual의 반례가 아니다.
성장하는 wheel과 그 보완층 전체에서 동시에 균일한 `K=56` 상계를 얻는 것이
남은 핵심 보조정리다.

## 4. Twin Prime Conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

For finitely many rational additive characters

```text
chi_j(n) = exp(2*pi*i*a_j*n/q_j),
```

all joint phase information at `n` and `n+2` factors through
`n mod L`, where `L=lcm(q_j)`. Every locally admissible transcript has a
proper composite-pair realizer below `2Lrs`.

### Proof / 증명

Each phase depends only on its denominator residue, so the finite phase algebra
factors through `n mod L`. For an admissible class `a`, choose primes `r,s`
not dividing `L` and solve

```text
n=a mod L,  n=0 mod r,  n=-2 mod s.
```

CRT and the proper-factor adjustment from TICKET-135 give a solution below
`2Lrs`. It has exactly the same rational Fourier phases while both `n` and
`n+2` are composite.

유리 Fourier 특성은 겉으로는 스펙트럼 정보처럼 보이지만, 유한 개만 사용하면
결국 최소공배수 `L`의 나머지 정보다. 따라서 유한 유리 주파수 대수를
"비합동 Type II 분리자"라고 부르는 경로는 폐기한다.

### Remaining gap / 남은 간극

The theorem says nothing about irrational, aperiodic, or scale-growing
bilinear information. The next lemma must construct such a statistic and prove
a uniform signed margin against the composite lifts, followed by transport to
a positive exact-gap-two lower bound.

무리 주파수, 비주기 정보, 분석 스케일과 함께 성장하는 bilinear 통계는 이
no-go 밖에 있다. 해당 통계의 균일한 부호 분리와 exact gap 2 하계로의 전달은
모두 미증명이다.

## Proof DAG / 증명 의존성 그래프

```text
RH:      T135 block criterion
           -> T136 Schur-test bridge + entrywise no-go
           -> [OPEN] actual Weil row/column tail bounds
           -> [OPEN] RH

Collatz: T135 almost-everywhere slope cover
           -> T136 affine correction inequality
           -> [OPEN] uniform least-counterexample surplus
           -> [OPEN] Collatz

Goldbach: T135 sparse finite-set norm bridge
           -> T136 fixed-wheel linear-mass barrier
           -> [OPEN] growing-wheel K56 residual bound
           -> [OPEN] strong Goldbach

Twin:    T135 finite congruence transcript lift
           -> T136 rational Fourier algebra lift
           -> [OPEN] aperiodic scale-growing Type II separator
           -> [OPEN] Twin Prime
```

The same nodes and edges are stored under each problem's `proof_dag` field in
the machine record.

같은 노드와 간선은 기계 판독 JSON의 각 문제별 `proof_dag` 필드에도 들어
있다. 닫힌 중간 정리와 열린 난제를 화면에서 같은 상태로 오인하지 않도록
상태값을 분리했다.

## Literature boundary / 문헌 경계

- M. Suzuki, [Weil's quadratic form via the screw function](https://arxiv.org/abs/2606.09096), develops a continuous-function framework without assuming RH. It does not supply the row/column estimates required here.
- A. Groskin, [High-Precision Approximation of Riemann Zeros via the Truncated Weil Form](https://arxiv.org/abs/2605.20224), explicitly treats continuum positivity and convergence as open and makes no proof claim.
- T. Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562), proves an almost-all result, not the pointwise least-counterexample surplus lemma.
- L. Zhao, [The exceptional set of Goldbach problem and Linnik's constant](https://arxiv.org/abs/2511.05631), concerns exceptional-set progress and does not provide this report's missing pointwise residual budget.
- K. Ford and J. Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368), supplies modern sieve context but no exact-gap-two lower bound.

These references define the research boundary as checked on 2026-07-25. No
external claim is imported as a missing proof step.

위 문헌은 2026-07-25 기준 연구 경계를 정한다. 문헌의 결과를 이 보고서에서
빠진 전제 대신 사용하지 않으며, arXiv 원고의 존재를 검증 완료된 난제
해결로 간주하지 않는다.

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket136_scale_sensitive_obstructions_and_affine_bridge.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket136_scale_sensitive_obstructions_and_affine_bridge
```

Generated artifacts:

- `data/open-problem/ticket136-scale-sensitive-obstructions-and-affine-bridge.json`
- `data/open-problem/riemann/rh-ticket-136-schur-test-tail-no-go.json`
- `data/open-problem/collatz/co-ticket-136-affine-correction-inequality.json`
- `data/open-problem/goldbach/gb-ticket-136-fixed-wheel-moment-barrier.json`
- `data/open-problem/twin-prime/tp-ticket-136-rational-fourier-lift.json`

## Final status / 최종 상태

All four conjectures remain `open_not_proven`. The strongest positive advance
is the exact Collatz affine-correction criterion. The other three results
primarily prevent misdirected proof searches by exposing hidden dimension,
density, or periodicity.

네 난제는 모두 `open_not_proven`이다. 가장 직접적인 전진은 Collatz의 정확한
affine 보정 하강 조건이다. 나머지 세 결과는 각각 숨은 차원, 층의 밀도,
주기성을 드러내어 잘못된 증명 탐색을 차단한다.
