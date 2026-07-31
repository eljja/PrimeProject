# TICKET-163: Local certificates, natural realizers, trace cancellation, and Carleson localization

한국어 제목: **국소 인증서, 자연수 실현값, trace 상쇄, Carleson 국소화**

Status / 상태: `open_not_proven` for all four conjectures / 네 추측 모두 미해결

Generated / 생성: 2026-07-31 (Asia/Seoul)

## Abstract / 초록

TICKET-163 audits the four decisive lemmas left by TICKET-162 and proves a
smaller exact theorem on each track. The common issue is localization: a
finite or global aggregate does not automatically control the moving,
residue-coupled, targetwise, or local object needed by the conjecture.

For the Riemann track, every finite positive prime trace is explicitly
continuous on `H1`, but the coefficient-mass constant diverges; this specific
majorant cannot supply uniformity. For Collatz, the front-loaded word
maximizes the affine correction, but an exact natural residue at length 17
shows that correction ordering does not transfer endpoint descent. For
Goldbach, the integrality certificate is localized to dyadic shells, replacing
an unnecessarily strong infinite global budget; a diluted unit spike proves
that a vanishing mean still permits exceptions. For Twin Prime, local dyadic
variance telescopes exactly, while an embedded checkerboard proves that
global energy density can vanish with unchanged local dependence.

TICKET-163은 TICKET-162가 남긴 네 결정적 보조정리를 감사하고, 각
트랙에서 더 작은 정확한 정리를 증명한다. 공통 문제는 국소화다. 유한
또는 전역 집계량만으로는 추측에 필요한 이동 cutoff, 자연수 residue,
표적별 비소실, 국소 Type-II 상관을 자동으로 제어할 수 없다.

리만 트랙에서는 모든 유한 양의 prime trace의 `H1` 연속성을 명시적으로
증명하지만, 계수 절댓값 질량이 발산하므로 이 특정 majorant로는
균일성을 얻을 수 없다. 콜라츠에서는 front-loaded word가 affine correction을
최대화함을 증명하지만 길이 17의 정확한 자연수 residue가 correction
순서만으로 endpoint 하강을 이전할 수 없음을 보인다. 골드바흐에서는
적분성 인증서를 dyadic shell마다 적용해 불필요하게 강한 무한 전역
예산을 교정하고, 희석된 unit spike로 평균 오차가 0으로 가도 예외가
남을 수 있음을 증명한다. 쌍둥이 소수에서는 국소 dyadic 분산이 정확히
telescoping되지만, 삽입 checkerboard가 전역 에너지 밀도 감소와 국소
상관 감소가 다름을 보인다.

## Result ledger / 결과 원장

| Problem / 문제 | Exact result / 정확한 결과 | Status / 상태 | Decisive next lemma / 다음 보조정리 |
|---|---|---|---|
| Riemann / 리만 | `FinitePrimeTraceH1ContinuityAndAbsoluteMassNoGo` | RH open / 미해결 | `CancellationAwareUniformGuinandWeilTraceBoundOnConstraintCore` |
| Collatz / 콜라츠 | `AffineCorrectionMajorizationAndNaturalRealizerCouplingNoGo` | Collatz open / 미해결 | `FirstContractingLayerNaturalRealizerDescent` |
| Goldbach / 골드바흐 | `DyadicIntegralExceptionCertificateAndDilutedSpikeNoGo` | Goldbach open / 미해결 | `UniformDyadicNormalizedNegativeMinorBudgetBelowOne` |
| Twin Prime / 쌍둥이 소수 | `LocalDyadicVarianceIdentityAndGlobalDilutionNoGo` | Twin Prime open / 미해결 | `UniformPrimeWeightedLocalCarlesonPowerSavingBeyondParity` |

## 1. Riemann hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `R=log X` and define the finite positive prime trace

```text
Q_X(f) = sum_(n<=X) Lambda(n)n^(-1/2)|f(log n)|^2
```

on `H1(-R,R)`. Put

```text
C_R^2 = 2R + 1/(2R),
W_X   = sum_(n<=X) Lambda(n)/sqrt(n).
```

Then

```text
|Q_X(f)-Q_X(g)|
  <= C_R^2 W_X (||f||_H1+||g||_H1)||f-g||_H1.
```

따라서 각 고정 prime cutoff에서는 trace가 `H1` 연속이다. 그러나
`W_X`는 발산하므로 이 절댓값 상계는 cutoff에 균일한 상수를 주지
못한다.

### Proof / 증명

For every `x in [-R,R]`, the interval mean decomposition and the fundamental
theorem of calculus give

```text
|f(x)| <= (2R)^(-1/2)||f||_2 + (2R)^(1/2)||f'||_2
       <= C_R ||f||_H1.
```

Applying `|a^2-b^2| <= |a-b|(|a|+|b|)` at each trace point proves the
finite continuity inequality. For every prime `p>=3`,
`log(p)/sqrt(p) >= 1/p`; Euler's divergence of the reciprocal-prime series
therefore implies `W_X -> infinity`.

구간 평균과 미적분학의 기본정리를 이용하면 위 point trace 상계를 얻고,
각 prime-power 항에 제곱 차이 부등식을 적용하면 유한 연속성 정리가
나온다. 반면 소수 역수합의 발산으로 `W_X`가 발산한다. 따라서
prime 항과 archimedean 항의 상쇄를 사용하지 않는 절댓값 경로는
폐기한다.

### Computation and limit / 계산과 한계

For `X=100, 10^3, ..., 10^6`, `W_X` grows from about `16.896` to
`1996.907`; the displayed absolute continuity constant grows from about
`157.454` to `55248.845`.

이 계산은 발산하는 상계의 유한 진단이다. 완전한 Guinand-Weil 형식은
부호와 제약조건을 가지므로, 이 결과는 실제 형식의 균일 연속성이
불가능하다는 정리가 아니다. 다음 의무는 제약 core 위에서 prime 항과
archimedean 항의 상쇄를 포함한 균일 trace 상계다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

For a positive valuation word `a=(a_1,...,a_m)`, put

```text
S_j = a_1+...+a_j,
C(a) = sum_(j=0)^(m-1) 3^(m-1-j) 2^(S_j),  S_0=0.
```

The accelerated iterate satisfies

```text
2^S T_a(n) = 3^m n + C(a),  S=S_m.
```

At fixed `m,S`, the front-loaded word `(S-m+1,1,...,1)` maximizes `C(a)`.
If adjacent values `x<y` after prefix sum `P` are swapped, the increase is

```text
3^(m-i-2) 2^P (2^y-2^x) > 0.
```

고정된 길이와 총 valuation에서 front-loaded word가 affine correction을
최대화한다.

### Natural-realizer no-go / 자연수 실현값 불가능성

An exact word is not determined by the final congruence modulo `2^S` alone;
the endpoint must also be odd. Its least exact natural realizer is the odd
residue

```text
r(a) = (2^S-C(a))3^(-m) mod 2^(S+1).
```

At `m=17,S=27`, the front-loaded word has

```text
r = 268,434,773,  T^17(r)=258,280,325.
```

But the smaller-correction word

```text
(4,1,1,1,1,2,2,1,2,1,1,2,1,1,1,2,3)
```

is realized exactly by

```text
165 -> 167  after 17 accelerated steps.
```

따라서 correction의 극값 순서만으로 자연수 endpoint 하강을 이전할 수
없다. 단, `165`는 첫 accelerated step에서 `31`로 이미 하강한다.
그러므로 이것은 Collatz 반례가 아니라 **고정 길이 이전 논리의 정확한
반례**다.

Every positive composition of the minimal contracting total is enumerated
through `m=13`: all exact words for `m=3,...,13` descend; at `m=2`, the word
`(2,2)` realizes the terminal equality `1 -> 1`. This finite result is not
promoted to an all-length statement; the `m=17` no-go demonstrates why.

다음 단일 표적은 “자연수 궤도에서 multiplicative slope가 처음 수축하는
시점에는 endpoint가 시작값 아래로 내려간다”는
`FirstContractingLayerNaturalRealizerDescent`다. 이것도 아직 증명되지
않았고, 별도로 모든 비종결 궤도가 그런 시점에 도달하는 문제도 남는다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Declared proposition / 선언 명제

Partition the even targets into finite blocks `A_k`. If
`G_N=M_N+E_N`, where `G_N` is a nonnegative integer and `M_N>0`, define

```text
B_k = sum_(N in A_k) (E_N^-/M_N)^2.
```

Then

```text
#{N in A_k : G_N=0} <= B_k.
```

Consequently, `B_k<1` for every dyadic shell, combined with a finite initial
verification, excludes every exception. It is not necessary to require one
infinite global sum after a cutoff to be below one.

각 dyadic shell에서 정규화된 음의 오차 예산이 1보다 작으면 그 shell에는
Goldbach 예외가 없다. 이 조건을 모든 shell에 적용하면 전체 범위를
덮는다. TICKET-162의 무한 전역합 목표보다 약하고 정확한 조건이다.

### Diluted-spike no-go / 희석 spike 불가능성

Place one target with `(M,E,G)=(1,-1,0)` in every growing block and let all
other targets have zero normalized deficit. The block budget remains exactly
one while the mean budget is `1/|A_k| -> 0`. Hence vanishing mean error does
not exclude even one exception per scale.

각 커지는 블록에 unit spike 하나를 두면 평균은 0으로 가지만 예외는
블록마다 하나씩 남는다. 따라서 평균 감소를 점별 비소실로 승격하는
경로를 폐기한다.

The finite prime DFT through `65,536` uses a fixed Farey mask. An independent
integer prime-pair scan certifies that every tested even target has a
representation and agrees with the FFT positivity decision. The nine shell
budgets range from approximately `12.138` to `127.270` and never cross the
unit gate. These rows test the criterion; they do not prove the required
analytic bound.

`65,536` 이하의 각 짝수에 대해서는 부동소수점 FFT와 별도로 정수
소수쌍을 직접 탐색해 표현이 존재함을 확인했다. 따라서 유한 무반례
표시는 FFT 반올림에 의존하지 않는다. 다만 아홉 shell의 예산은 모두
1 이상이므로, 이 계산은 무한 범위의 해석적 하한을 증명하지 않는다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Declared proposition / 선언 명제

For a dyadic square `R` in a finite matrix, define

```text
V(R) = sum_(x in R) |H_x-<H>_R|^2.
```

Let the detail energy at each node be the weighted variance of its four child
means about the parent mean. Then

```text
V(R) = sum_(Q descendant of R) detail(Q).
```

This is an exact local martingale variance identity, obtained by iterating the
one-step within-child/between-child variance decomposition.

각 dyadic square에서 전체 분산은 모든 하위 square의 martingale detail
에너지 합과 정확히 같다. TICKET-162의 전역 scale 분해를 모든 국소
사각형으로 확장한다.

### Global-dilution no-go / 전역 희석 불가능성

Embed one `4x4` checkerboard in the upper-left corner of a zero matrix of side
`8,16,32,64,128`. Every matrix has zero row and column margins and total
energy `16`. Its global energy density decreases

```text
1/4, 1/16, 1/64, 1/256, 1/1024,
```

but the local `4x4` energy density remains exactly one. Thus a global
normalized energy estimate can hide a fixed local Type-II obstruction.

전역 평균 에너지가 0으로 가더라도 특정 국소 사각형의 상관은 전혀
줄지 않을 수 있다. 그러므로 쌍둥이 소수 트랙에는 모든 관련 rectangle을
동시에 제어하고 parity barrier를 넘는 prime-weighted 국소 Carleson
power saving이 필요하다.

## Proof DAG / 증명 의존성

```text
Riemann:
  absolute prime-trace uniformity [refuted route]
    -> finite H1 trace continuity [proved]
    -> cancellation-aware uniform complete-form trace bound [open]

Collatz:
  correction ordering transfers natural descent [refuted by m=17]
    -> correction majorization + exact residue coupling [proved]
    -> first-contracting-layer natural descent [open]

Goldbach:
  vanishing mean excludes all exceptions [refuted by unit spikes]
    -> shellwise integral certificate [proved]
    -> uniform dyadic shell budget below one [open]

Twin Prime:
  global energy decay controls every local block [refuted by dilution]
    -> local dyadic variance identity [proved]
    -> prime-weighted local Carleson power saving [open]
```

## Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket163_local_certificate_realizer_trace_carleson.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket163_local_certificate_realizer_trace_carleson
```

The generator writes one global JSON and four per-problem JSON files. Every
proof DAG has exactly one rejected route, one proved intermediate theorem,
and one open next lemma. / 생성기는 통합 JSON 하나와 문제별 JSON 네 개를
쓰며, 각 proof DAG는 폐기 경로·증명된 중간정리·미증명 다음 보조정리를
정확히 구분한다.

## Literature boundary / 문헌 경계

- A. Groskin, “A finite Guinand-Weil dictionary and archimedean tail order
  for the truncated Weil quadratic form” (2026),
  <https://arxiv.org/abs/2607.02828>.
- A. Groskin, “High-Precision Approximation of Riemann Zeros via the
  Truncated Weil Form” (2026), <https://arxiv.org/abs/2605.20224>.
- T. Tao, “Almost all orbits of the Collatz map attain almost bounded
  values” (2019), <https://arxiv.org/abs/1909.03562>.
- H. Li, “The exceptional set of Goldbach numbers (II),” *Acta Arithmetica*
  92 (2000), 71-88, <https://eudml.org/doc/207380>.
- K. Ford and J. Maynard, “On the theory of prime producing sieves” (2024),
  <https://arxiv.org/abs/2407.14368>.

These papers establish context or external tools. None proves the four open
lemmas named above. / 이 문헌들은 배경과 외부 도구를 제공하지만 위 네
보조정리를 증명하지 않는다.
