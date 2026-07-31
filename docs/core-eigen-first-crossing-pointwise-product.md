# TICKET-164: Constraint-core eigenvalues, Collatz first crossing, Goldbach pointwise gates, and product Haar localization

한국어 제목: **제약 core 고유값, 콜라츠 첫 수축, 골드바흐 점별 문턱, product-Haar 국소화**

Status / 상태: `open_not_proven` for all four conjectures / 네 추측 모두 미해결

Generated / 생성: 2026-07-31 (Asia/Seoul)

## Abstract / 초록

TICKET-164 audits the four open nodes left by TICKET-163. It proves four
smaller exact statements and rejects one overly coarse shortcut on each
track. None resolves its parent conjecture.

For the Riemann track, positivity under linear constraints is reduced exactly
to positivity of a compressed matrix. Positive trace, determinant, and one
positive test value are shown insufficient by a scalable counterfamily. For
Collatz, every possible non-descent at the first multiplicatively contracting
prefix is reduced to finitely many final valuations at each fixed length;
complete exact residue replay closes lengths at most 17. For Goldbach, the
shellwise `L2` certificate is replaced as the decisive target by the exact
pointwise integrality gate, and an all-positive counterfamily proves that the
`L2 < 1` gate is not necessary. For Twin Prime, product-Haar Parseval exposes
independent row and column scales; equal-scale tensor coefficients can miss
all anisotropic energy.

TICKET-164는 TICKET-163이 남긴 네 open node를 다시 감사한다. 각
트랙에서 더 작은 정확 명제를 증명하고, 지나치게 거친 shortcut 하나를
반례로 폐기한다. 어떤 상위 추측도 해결하지 않는다.

리만 트랙에서는 선형 제약 아래 양성 문제를 압축 행렬의 양성 문제로
정확히 환원한다. 양의 trace, determinant, 단일 test value만으로는
부족함을 확장 가능한 반례족으로 보인다. 콜라츠에서는 곱셈 기울기가
처음 수축하는 시점의 비하강 가능성을 각 고정 길이마다 유한 개의 마지막
valuation으로 환원하고, 길이 17까지 정확 residue replay로 완전 검사한다.
골드바흐에서는 shellwise `L2` 인증서보다 정확한 점별 적분성 문턱을
결정적 표적으로 선택하고, 모든 표현수가 양수여도 `L2` 예산은 무한히
커질 수 있음을 보인다. 쌍둥이 소수에서는 행·열 scale을 독립적으로
선택하는 product-Haar Parseval을 증명하고, equal-scale tensor만 남기면
비등방 에너지를 전부 놓칠 수 있음을 보인다.

## Result ledger / 결과 원장

| Problem / 문제 | Exact result / 정확한 결과 | Resolution / 해결 | Decisive next lemma / 다음 보조정리 |
|---|---|---|---|
| Riemann / 리만 | `ConstraintCoreCompressionAndScalarCancellationNoGo` | open / 미해결 | `UniformGuinandWeilConstraintCoreMinimumEigenvalueLowerBound` |
| Collatz / 콜라츠 | `FirstContractingLayerFiniteCertificateAndFinalValuationBound` | open / 미해결 | `UniformFirstContractingLayerResidueSlack` |
| Goldbach / 골드바흐 | `PointwiseIntegralExceptionEquivalenceAndL2NonNecessityNoGo` | open / 미해결 | `UniformDyadicPointwiseMinorDeficitStrictlyBelowOne` |
| Twin Prime / 쌍둥이 소수 | `ProductHaarParsevalAndEqualScaleTensorNoGo` | open / 미해결 | `UniformPrimeWeightedProductCarlesonPowerSavingBeyondParity` |

## 1. Riemann hypothesis / 리만 가설

### Declared proposition / 선언 명제

Let `H` be a real symmetric finite Galerkin matrix, let `B` have full row
rank, and let the columns of `U` span `ker(B)`. Then

```text
v^T H v >= 0 for every Bv=0
    if and only if
c^T (U^T H U) c >= 0 for every c.
```

Thus the finite constrained sign question is exactly a minimum-eigenvalue
question for the compressed form. Scalar cancellation summaries do not
replace it. With

```text
H = diag(3,-1,-1),       B = (1,1,1),
U = [(1,-1,0), (1,0,-1)],
```

the ambient trace, determinant, and all-ones quadratic value are respectively
`1`, `3`, and `1`, but

```text
U^T H U = [[2,3],[3,2]],     det(U^T H U) = -5,
(0,-1,1)^T H (0,-1,1) = -2.
```

`H`를 유한 Galerkin 대칭행렬, `Bv=0`을 admissibility 제약이라고 하자.
`ker(B)`의 기저를 열로 갖는 행렬을 `U`라 하면 제약 core에서의 양성은
`U^T H U`의 양의 준정부호성과 정확히 동치다. 따라서 trace 합계나
determinant, 특정 벡터 하나의 값이 양수라는 사실만으로는 부족하다.
위 3차원 예는 세 scalar 진단이 모두 양수인데도 제약 core에 정확한
음의 방향이 있음을 보인다.

### Proof and scalable no-go / 증명과 확장 반례

Every constrained vector has the form `v=Uc`; substitution gives the
equivalence. For every dimension `d in {5,9,17,33}`, the diagonal family

```text
H_d = diag(1,...,1,-1,-1),     B_d = (1,...,1)
```

has positive trace `d-4`, determinant `1`, and all-ones value `d-4`. The
sum-zero vector supported as `(1,-1)` on the last two coordinates has value
`-2`. This is an exact counterfamily, not a floating-point example.

모든 제약 벡터를 `Uc`로 쓰고 이차형식에 대입하면 압축 동치가 바로
나온다. 차원 `5,9,17,33`의 대각 반례족은 trace와 determinant가
양수인 상태에서도 동일한 제약 음의 방향 `-2`를 유지한다. 따라서
“상쇄 총량이 좋아 보인다”는 scalar 진단을 RH의 Weil 양성으로
승격하는 경로를 폐기한다.

### Limit / 한계

This is finite linear algebra. TICKET-164 neither constructs the actual
cutoff-free Guinand-Weil operator nor proves a uniform positive lower bound
for its constrained minimum eigenvalue. The next single obligation is
`UniformGuinandWeilConstraintCoreMinimumEigenvalueLowerBound`.

이 결과는 유한 선형대수다. 실제 cutoff-free Guinand-Weil 연산자를
구성하거나 그 제약 최소 고유값의 균일 양의 하한을 증명하지 않는다.
따라서 RH 또는 영점 배제 결론은 없다.

## 2. Collatz conjecture / 콜라츠 추측

### Declared proposition / 선언 명제

For a positive accelerated valuation word `a=(a_1,...,a_m)`, put

```text
S_j = a_1+...+a_j,
2^S T_a(n) = 3^m n + C(a).
```

Call the word first-crossing when

```text
2^(S_j) <= 3^j  for every j<m,     2^S > 3^m.
```

If an odd nonterminal start `n>=3` does not descend at the endpoint, then

```text
(2^S-3^m)n <= C(a),
3(2^S-3^m) <= C(a).
```

For every fixed noncontracting prefix, `C(a)` does not depend on the final
valuation, while the left side grows exponentially. Hence only finitely many
final valuations can possibly fail. All larger final valuations descend for
every natural realizer without enumeration.

가속 valuation word가 모든 proper prefix에서는 아직 수축하지 않고
마지막 단계에서 처음 `2^S>3^m`이 되면 first-crossing word라 부르자.
비종결 홀수 `n>=3`이 끝점에서 하강하지 않으려면 위 affine 부등식을
반드시 만족해야 한다. 마지막 valuation을 키워도 `C(a)`는 변하지 않고
왼쪽의 slope gap은 지수적으로 증가하므로, 각 prefix마다 검사할 마지막
valuation은 정확히 유한 개다.

### Exact finite certificate / 정확한 유한 인증

The generator enumerates every noncontracting prefix through length 16 and
every potentially non-descending final valuation through full length 17. It
then computes the least nonterminal exact realizer modulo `2^(S+1)` and
replays every valuation.

```text
maximum full length                         17
noncontracting prefixes entering length 17 312,455
noncontracting prefixes after length 17    663,535
potential non-descent words replayed       464,921
replay failures                            0
observed strict-descent failures           0
minimum replayed strict margin             4
```

For a fixed contracting word, later exact realizers differ by `2^(S+1)` and
increase the descent margin by `2(2^S-3^m)`. Therefore the least nonterminal
realizer is the exact worst case for that word.

생성기는 길이 16까지의 모든 비수축 prefix와 완성 길이 17까지의 모든
비하강 가능 마지막 valuation을 열거한다. 각 word에 대해 endpoint가
홀수가 되도록 `2^(S+1)`에서 최소 비종결 자연수 residue를 구하고,
valuation을 처음부터 다시 재생한다. 총 464,921개 후보에서 replay
실패와 비하강은 모두 0이다. 같은 word의 다음 자연수 실현값은 최소
실현값보다 하강 margin이 더 크므로 최소 residue 검사로 해당 word
전체를 덮는다.

### New no-go and limit / 새 no-go와 한계

The descent margin is not monotone in the final valuation. Both `(1,3)` and
`(1,4)` first cross at length two, but their least nonterminal realizers give

```text
(1,3): 19 -> 11, margin 8
(1,4):  3 ->  1, margin 2.
```

Thus checking only the least crossing final valuation cannot be justified by
a monotonicity argument. The affine candidate bound, not monotonicity, is what
closes the infinite final-valuation tail at each fixed prefix.

마지막 valuation이 커지면 하강 margin도 커진다는 가정은 위 정확한 두
word로 반박된다. 그러므로 최소 crossing valuation 하나만 검사하는
shortcut은 폐기한다. 다만 길이 18 이상은 전혀 증명되지 않았다.
다음 단일 의무는 모든 길이에 대해 최소 자연 residue가 affine 문턱을
넘는다는 `UniformFirstContractingLayerResidueSlack`이다.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### Exact pointwise gate / 정확한 점별 문턱

Let `G_N=M_N+E_N`, where `G_N` is a nonnegative integer and `M_N>0`. Define

```text
d_N = E_N^-/M_N.
```

Then

```text
G_N > 0   if and only if   d_N < 1.
```

Indeed, `G_N=0` gives `E_N=-M_N` and `d_N=1`. If `G_N>=1`, either the error
is nonnegative and `d_N=0`, or `d_N=1-G_N/M_N<1`.

`G_N`이 비음이 아닌 정수이고 `M_N>0`이면, 표현수의 양성은 정규화한
음의 오차 `d_N<1`과 정확히 동치다. 이 점별 적분성 문턱은 충분조건이
아니라 필요충분조건이다.

### L2 non-necessity no-go / L2 비필요성 no-go

TICKET-163 proved the sufficient shell certificate `sum d_N^2<1`. It is not
necessary. On a block of `L` targets, set `M_N=2` and `G_N=1` everywhere.
There are no zeros and every pointwise gate passes with `d_N=1/2`, but

```text
sum d_N^2 = L/4 -> infinity.
```

Therefore the former `L2<1` target can fail arbitrarily badly even when all
Goldbach counts are positive. It remains a valid sufficient theorem but is
too strong to serve as the unique decisive target.

TICKET-163의 shell `L2<1` 조건은 여전히 올바른 충분조건이다. 하지만
모든 표적에서 `M=2,G=1`로 두면 예외는 하나도 없고 점별 문턱은 모두
통과하는 반면 `L2` 예산은 `L/4`로 발산한다. 따라서 `L2<1`을 필요한
조건 또는 유일한 결정적 목표로 다루는 경로를 폐기한다.

### Finite diagnostic and limit / 유한 진단과 한계

The fixed Farey DFT through `65,536`, cross-checked by an independent integer
prime-pair scan, has no finite zero and every pointwise deficit is below one.
Its shell `L2` budgets remain above one. This illustrates the strict logical
separation; it does not prove an infinite pointwise minor-arc bound.

`65,536`까지의 고정 Farey DFT는 독립 정수 소수쌍 탐색과 일치하며
유한 예외가 없고 모든 점별 deficit이 1보다 작다. 반면 shell `L2`
예산은 계속 1보다 크다. 이 계산은 두 조건의 논리적 차이를 보여줄 뿐
무한 범위의 해석적 상계를 주지 않는다. 다음 단일 의무는
`UniformDyadicPointwiseMinorDeficitStrictlyBelowOne`이다. 이 표적은
원래의 양성 문제와 매우 가깝기 때문에 쉬운 우회로가 아니다.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### Product-Haar theorem / Product-Haar 정리

For a finite dyadic matrix with zero row and column margins, the one-dimensional
Haar expansions tensor to give

```text
||H||_F^2
  = sum_(I,J) |<H,h_I tensor h_J>|^2 / (||h_I||^2 ||h_J||^2),
```

where row interval `I` and column interval `J` have independently chosen
dyadic positions and scales. This is exact finite Parseval.

행합과 열합이 0인 유한 dyadic 행렬에서는 1차원 Haar 기저를 tensor해
행·열 구간의 위치와 scale을 독립적으로 선택하는 정확한 Parseval
항등식을 얻는다.

### Equal-scale tensor no-go / Equal-scale tensor no-go

Let `u` be a row Haar wavelet with support 2 and `v` a column Haar wavelet
with support `N/2`. For `H=u tensor v`,

```text
||H||_F^2 = N,
full product-Haar energy = N,
equal row/column scale tensor energy = 0.
```

The audit verifies this exactly for `N=8,16,32,64,128`. Thus an implementation
that retains only equal row and column tensor scales can miss every
anisotropic coefficient even though both margins vanish.

행 support 2와 열 support `N/2`의 Haar wavelet을 tensor하면 전체
에너지와 product-Haar 에너지는 `N`이지만 equal-scale tensor 에너지는
정확히 0이다. `N=8`부터 `128`까지 정수 연산으로 확인했다. 따라서
정사각형과 같은 scale의 pure tensor만 남기는 구현 shortcut을 폐기한다.
이 no-go는 TICKET-163의 완전한 quadtree 분산 항등식을 반박하는 것이
아니라, Type-II 정보를 equal-scale tensor 계수로 축소하는 것을
반박한다.

### Limit / 한계

Parseval creates a correct coordinate system but no prime-weighted saving.
It does not cross the parity barrier or prove a positive lower bound for gap
two. The next single obligation is
`UniformPrimeWeightedProductCarlesonPowerSavingBeyondParity`.

Parseval은 올바른 좌표계를 제공할 뿐 소수 가중치의 power saving을
제공하지 않는다. parity barrier를 넘거나 gap 2의 양의 하한을
증명하지 않는다.

## Proof DAG / 증명 의존성

Each machine artifact stores exactly three nodes:

```text
REJECTED: refuted_or_insufficient shortcut
   -> CLOSED: exact TICKET-164 theorem
   -> OPEN: one decisive next lemma
```

각 기계 판독 artifact는 폐기 경로, 이번에 닫힌 정확 정리, 다음 단일
미증명 보조정리를 세 노드로 저장한다. 네 `OPEN` 노드 중 닫힌 것은
없으며 conjecture resolution count는 `0`이다.

## Reproduction / 재현

```powershell
python scripts/ticket164_core_eigen_first_crossing_pointwise_product.py
python -m unittest tests.test_ticket164_core_eigen_first_crossing_pointwise_product
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Machine-readable artifacts / 기계 판독 산출물:

```text
data/open-problem/ticket164-core-eigen-first-crossing-pointwise-product.json
data/open-problem/riemann/rh-ticket-164-constraint-core-eigenvalue.json
data/open-problem/collatz/co-ticket-164-first-crossing-residue.json
data/open-problem/goldbach/gb-ticket-164-pointwise-deficit.json
data/open-problem/twin-prime/tp-ticket-164-product-haar.json
```

## Literature boundary / 문헌 경계

- The finite Guinand-Weil matrix viewpoint is motivated by
  [A finite Guinand-Weil dictionary and archimedean tail order](https://arxiv.org/abs/2607.02828).
  TICKET-164 does not import an RH proof from it.
- The all-orbit Collatz gap remains separate from Tao's
  [almost-all orbit theorem](https://arxiv.org/abs/1909.03562).
- Current Goldbach exceptional-set and explicit major-arc context is described
  in [The exceptional set of the Goldbach problem](https://arxiv.org/abs/2607.27282).
  It does not supply the pointwise binary margin required here.
- Product localization is motivated by the need for substantial Type I/II
  information in Ford and Maynard's
  [prime-producing sieve framework](https://arxiv.org/abs/2407.14368).

These external works define context and barriers. The exact finite algebra,
countermodels, and replay certificates claimed in this report are generated
inside PrimeProject. No literature citation is treated as a proof of any of
the four conjectures.

위 외부 문헌은 현재 연구 맥락과 장벽을 정하는 데만 사용한다. 본
보고서가 주장하는 유한 대수, 반례 모델, replay 인증서는 PrimeProject
내부에서 생성된다. 어떤 인용문헌도 네 추측의 증명으로 취급하지 않는다.
