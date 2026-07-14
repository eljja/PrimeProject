# TICKET-119: Preregistered canonical-pair 16M persistence holdout

## Claim boundary / 주장 경계

TICKET-119 does **not** prove the Twin Prime Conjecture, eventual positivity, monotonicity, or an asymptotic scaling law. It tests the unchanged TICKET-118 rule once at the first unseen doubled horizon.

TICKET-119는 **쌍둥이 소수 추측, 충분히 큰 범위의 양수성, 단조성, 점근 스케일 법칙을 증명하지 않습니다.** TICKET-118의 규칙을 바꾸지 않고 처음 보는 두 배 규모에서 한 번 반증하려고 시도한 유한 실험입니다.

## Public preregistration / 공개 사전등록

Commit `87bdcf9b16c5e57581e9a411aa61290ef2eea173` was pushed before any 16M endpoint coefficient or result artifact existed. It fixed:

- `X=16,777,216`;
- the existing `canonical_adjacent_shell_pairs_v1` rule;
- one increasing list of nonempty outer-divisor dyadic shells;
- groups `(B0,B1),(B2,B3),...`, with an odd final singleton;
- the same grouping for every right-Farey denominator `q=2,...,32`;
- no new partition, sign, cutoff, weight, exponent, denominator-specific grouping, or alternate primary endpoint;
- one execution, reported whether it passed, failed, or exhausted resources;
- primary pass only when the registered finite lower expression is strictly positive.

사전등록 커밋에는 16M 결과 JSON이 없었습니다. 8M 결과는 공개된 참고값으로만 기록했고, 16M 판정 규칙이나 threshold를 맞추는 데 사용하지 않았습니다.

Here `runs=1` means one primary evaluation before the outcome was known. Exact reruns after publication are reproducibility checks and cannot replace, average, or redefine that first primary result.

여기서 `runs=1`은 결과를 모르는 상태의 1차 평가를 한 번만 수행한다는 뜻입니다. 결과 공개 후의 동일 재실행은 재현성 검사일 뿐 최초 결과를 교체하거나 평균내거나 새 판정으로 정의할 수 없습니다.

Machine-readable contract: `data/open-problem/ticket119-canonical-pair-doubling-preregistration.json`.

## Registered result / 등록 결과

The first execution completed in 82 seconds and passed the primary endpoint:

```text
known comparison term                         7,495,484.2634
canonical adjacent-pair numerator budget     5,728,051.1980
rational-boundary envelope                          16.4063
Abel variation envelope                        288,394.8309
registered finite lower expression           1,479,021.8281
```

The adverse-to-known ratio is `0.8026782825`, so the normalized margin is `0.1973217175`. The canonical budget is `1.1448737898` times the fully signed numerator budget. The canonical partition again equals the post-hoc best width-two partition; that equality is a registered secondary observation and did not change the primary decision.

최초 실행의 유한 하한은 `+1,479,021.8281`로 통과했습니다. 정규화 margin은 `19.7322%`입니다. 이것은 16M 한 점의 정확한 유한 결과이며, 앞으로도 계속 양수라는 결론은 아닙니다.

## Scale falsification ledger / 스케일 반증 장부

| horizon | selection status | lower expression | adverse / known | canonical / signed |
|---:|---|---:|---:|---:|
| 4,194,304 | TICKET-117 exploratory | -1,236.3 | 1.000660 | 1.232326 |
| 8,388,608 | TICKET-118 preregistered | +156,727.0 | 0.957953 | 1.193875 |
| 16,777,216 | TICKET-119 preregistered | +1,479,021.8 | 0.802678 | 1.144874 |

The 8M-to-16M normalized margin increases from `0.0420475` to `0.1973217`. Two positive dyadic rows do not establish monotonicity, convergence, or a power-saving exponent. A single later finite failure would refute persistence from 8M at that scale but would not refute the eventual theorem. Refuting the eventual theorem requires an unbounded admissible failure sequence.

8M과 16M의 연속 양수는 후속 정리 후보를 유지할 이유는 되지만 증명의 양화사 `모든 충분히 큰 X`를 채우지 못합니다. 따라서 finite fit이나 그래프 추세를 theorem constant로 사용하지 않습니다.

## Group localization / 그룹별 병목

| canonical group | actual outer divisors | numerator budget | share |
|---|---:|---:|---:|
| `D256-D512` | 257-1,023 | 3,387,615.9 | 59.14% |
| `D1024-D2048` | 1,024-4,095 | 1,451,709.3 | 25.34% |
| `D4096-D8192` | 4,096-16,383 | 596,807.8 | 10.42% |
| `D16384-D32768` | 16,384-65,535 | 274,894.3 | 4.80% |
| `D65536` | 65,536-77,672 | 17,023.8 | 0.30% |

The first group now carries 59.14% of the canonical numerator budget. This concentration is not monotone across the observed horizons, but it identifies the first analytic sublemma: control the signed low-outer-divisor factor-four pair before applying norms.

첫 그룹의 비중이 커졌으므로 이후 증명 시도는 전체를 한 번에 Cauchy로 누르기보다 실제 Möbius 부호를 보존한 low-divisor bilinear 합부터 다뤄야 합니다.

## Exact theorem still missing / 여전히 필요한 정확한 정리

Let `K(X)` be the independently positive comparison term, `B_can(X)` the denominator-summed canonical-pair mean plus projected centered-L2 budget, and `E_bd(X), E_var(X)` the registered boundary and variation envelopes. The retained theorem must prove that there are fixed `delta>0` and `X0` such that

```text
K(X) > 0,
B_can(X) + E_bd(X) + E_var(X) <= (1-delta) K(X)
```

for every `X>=X0` in a range sufficient for the exact prime-pair bridge. The bound must be derived from the actual signed Möbius/divisor coefficients, not from the finite rows above. It must also close the prime-power contamination and fixed-denominator-cutoff obligations already isolated in earlier tickets.

```text
EventuallySubcriticalCanonicalAdjacentDyadicPairVaughanEndpointBudget
```

The immediate sublemma is `UniformLowDivisorCanonicalPairDispersion`: obtain a denominator-summed saving for the first factor-four group while retaining its internal signed covariance. A valid negative program is to construct an unbounded Vaughan-realizable sequence with adverse-to-known ratio at least one.

## Literature boundary / 문헌상 경계

- [Maynard, *Small gaps between primes*](https://annals.math.princeton.edu/2015/181-1/p07) proves bounded gaps, not gap two.
- [Polymath8b, *Variants of the Selberg sieve*](https://arxiv.org/abs/1407.4897) formalizes the parity obstruction for purely sieve-theoretic improvements. PrimeProject therefore does not present this endpoint audit as a Selberg-sieve escape.
- [Helfgott, *The ternary Goldbach problem*](https://arxiv.org/abs/1501.05438) supplies a primary model for explicit Type I/II and minor-arc bookkeeping. The binary shift-two signed estimate required here is not supplied by that theorem.

Known bounded-gap results and explicit Type II technology motivate the decomposition but do not imply the missing inequality. Any claim of novelty is limited to this reproducible finite audit and its preregistration lineage, not a new theorem in analytic number theory.

## Keep, discard, and next action / 유지·폐기·다음 작업

Keep:

- the result-independent canonical partition;
- exact signed dyadic and real-Gram reconstruction contracts;
- the scale ledger as a falsification record;
- the low-divisor group as the first theorem subproblem.

Discard:

- fitting a power law from 4M, 8M, and 16M;
- treating two positive rows as eventual positivity;
- denominator-specific regrouping or a 32M rule change;
- transferring the Twin result to RH, Collatz, or Goldbach;
- claiming that a finite positive lower expression is itself an infinitude proof.

Next action:

1. derive a symbolic upper bound for the first canonical factor-four group;
2. state every constant independently of the 16M row;
3. build an adversarial Vaughan-coefficient oracle for the proposed hypotheses;
4. preregister 32M separately only after its resource and decision contract is frozen.

## Reproduction

```powershell
python scripts/ticket119_twin_canonical_pair_doubling_holdout.py
python -m unittest tests.test_ticket119_twin_canonical_pair_doubling_preregistration
```

Result artifact: `data/open-problem/ticket119-twin-canonical-pair-doubling-holdout.json`.
