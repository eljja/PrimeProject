# TICKET-152: Compression Exhaustion, Collatz Cylinders, Goldbach Energy, and Twin Selection

## Claim boundary / 주장 경계

**English.** This report does not prove or disprove the Riemann Hypothesis,
the Collatz conjecture, the strong Goldbach conjecture, or the Twin Prime
conjecture. TICKET-152 proves four exact intermediate or no-go theorems. Its
main contribution is target correction: it identifies three proposed bridges
that cannot work in their current form and replaces them with explicit
infinite obligations.

**한국어.** 이 보고서는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측,
쌍둥이 소수 추측을 증명하거나 반증하지 않는다. TICKET-152가 증명한
것은 네 개의 정확한 중간 정리 또는 no-go 정리다. 핵심 성과는
증명 표적의 교정이다. 현재 형태로는 성립할 수 없는 세 연결 경로를
확정하여 폐기하고, 그 자리에 실제로 필요한 무한 정리를 명시한다.

| Problem / 문제 | Exact result / 이번에 확정한 결과 | Rejected route / 폐기 경로 | Single next lemma / 다음 단일 보조정리 |
|---|---|---|---|
| RH / 리만 | `NestedCompressionExhaustionAndFiniteCutoffNoGo` | 고정된 유한 Galerkin cutoff의 양성을 전역 양성으로 승격 | `ActualWeilCoreCompressionWithCertifiedOperatorNormTailBelowMargin` |
| Collatz / 콜라츠 | `AffineCylinderTailAndFiniteExtensionCoverNoGo` | 비종료 cylinder를 유한 strict valuation 확장 트리로 완전 피복 | `TypeTwoCountableExtensionCoverWithUniformAnalyticValuationTail` |
| Goldbach / 골드바흐 | `VonMangoldtGlobalL2HoleBallDivergenceNoGo` | bounded dense 기준함수의 endpoint-hole 전역 \(L^2\) ball 안에 \(\Lambda\) 오차를 삽입 | `EndpointBilinearVonMangoldtErrorBelowSingularSeriesMainTermK56` |
| Twin Prime / 쌍둥이 소수 | `SharpMarginalDeletionTransferAndVanishingCoverageNoGo` | 한 변수 `log 2` 편향을 높은 선택 보존율로 gap-two support에 이전 | `DirectShiftedCubicRoughLiouvilleSumNegativeProportion` |

Machine-readable evidence:
[`ticket152-compression-cylinder-energy-selection.json`](../data/open-problem/ticket152-compression-cylinder-energy-selection.json).

Reproduction:

```powershell
python scripts/ticket152_compression_cylinder_energy_selection.py
python -m unittest tests.test_ticket152_compression_cylinder_energy_selection -v
python scripts/verify_open_problem_structure.py
```

## 1. Riemann Hypothesis / 리만 가설

### 1.1 Declared proposition / 선언 명제

Let \(B\) be a bounded self-adjoint operator on a separable Hilbert space.
Let

\[
H_1\subset H_2\subset\cdots
\]

be finite-dimensional subspaces whose union is dense, and define

\[
\mu_N=\inf_{\substack{x\in H_N\\\|x\|=1}}\langle Bx,x\rangle.
\]

Then

\[
\mu_N\downarrow \inf\sigma(B),\qquad
\|B_-\|=\sup_N\max(0,-\mu_N).
\]

Consequently,

\[
B\ge -I\quad\Longleftrightarrow\quad \mu_N\ge -1
\text{ for every }N.
\]

No fixed finite cutoff suffices. However, if a finite-rank self-adjoint
operator \(F\) satisfies

\[
\|B-F\|\le\varepsilon,\qquad
\lambda_{\min}(F)\ge -1+\varepsilon,
\]

then \(B\ge-I\).

한국어로 말하면, 유한 압축의 최소 Rayleigh quotient를 끝없이 검사하면
전역 음의 스펙트럼 하한과 정확히 일치한다. 그러나 어떤 고정된
cutoff까지만 검사해서는 충분하지 않다. 유한 행렬의 양성뿐 아니라,
검사하지 않은 tail의 operator norm이 유한 행렬의 양의 margin보다
작다는 별도 증명이 있어야 한다.

### 1.2 Proof / 증명

Nestedness makes \(\mu_N\) nonincreasing. For any unit vector \(x\), density
provides \(x_N\) in the union with \(x_N/\|x_N\|\to x\). Boundedness of \(B\)
makes the quadratic form continuous, so the limiting infimum over the union
equals the infimum over the full unit sphere. The Rayleigh variational
principle identifies this value with \(\inf\sigma(B)\). Spectral calculus then
gives

\[
\|B_-\|=\max(0,-\inf\sigma(B)).
\]

For every finite \(N\), the diagonal operator

\[
B_N=\operatorname{diag}(
\underbrace{0,\ldots,0}_{N\text{ entries}},
-1-\delta,0,\ldots)
\]

passes every tested compression through \(N\), while \(B_N\not\ge-I\). This
is an exact counterexample to finite-cutoff promotion.

Finally, for every unit \(x\),

\[
\langle Bx,x\rangle
\ge \langle Fx,x\rangle-\|B-F\|
\ge \lambda_{\min}(F)-\varepsilon\ge-1.
\]

한국어 증명도 동일하다. 조밀한 nested subspace의 Rayleigh 하한은
bounded quadratic form의 연속성 때문에 전역 spectral infimum으로
내려간다. 반면 \(N+1\)번째 좌표에만 \(-1-\delta\)를 둔 대각
작용소는 앞의 모든 유한 검사를 통과하므로 유한 cutoff 증명은
원리적으로 불가능하다. tail norm 상계가 있으면 마지막 부등식으로
전역 하한을 복원할 수 있다.

### 1.3 Computation and limit / 계산과 한계

The audit contains seven hidden-direction counteroperators and nine exact
rational tail-margin certificates. All checks pass. These matrices validate
the functional-analytic statement; they are not discretizations of the
actual Weil form.

감사 데이터는 일곱 개의 hidden negative direction 반례와 아홉 개의
정확 유리수 tail-margin certificate를 포함한다. 이 계산은 위
함수해석 정리를 재현하지만 실제 Weil 형식을 구성하지 않는다.

**Remaining gap / 남은 간극.** Construct a proved form core for the actual
Weil quadratic form, identify its relative operator \(B\), and prove an
operator-norm tail bound smaller than a certified compression margin. No
off-critical zeta zero has been excluded.

## 2. Collatz conjecture / 콜라츠 추측

### 2.1 Declared proposition / 선언 명제

For the accelerated odd Collatz map

\[
T(n)=\frac{3n+1}{2^{v_2(3n+1)}},
\]

fix a positive valuation word \(a=(a_1,\ldots,a_m)\). Put

\[
S=\sum_{j=1}^m a_j,\qquad
2^S T^m(n)=3^m n+C_a,\qquad
D_a=2^S-3^m.
\]

There is exactly one odd residue \(r_a\bmod 2^{S+1}\) realizing this full
word. Every natural start in its cylinder is

\[
n=r_a+k2^{S+1},\qquad k\ge0.
\]

If \(D_a>0\), descent at time \(m\) occurs exactly on a terminal arithmetic
tail:

\[
T^m(n)<n
\quad\Longleftrightarrow\quad
D_a(r_a+k2^{S+1})>C_a.
\]

If \(D_a\le0\), no start in the cylinder descends at time \(m\).

Moreover, every next valuation \(b\ge1\) occurs for some natural start in
the cylinder. Therefore no finite family of strict word extensions covers
the whole cylinder unless the parent word itself is accepted as a terminal
leaf.

한국어로는 다음과 같다. 하나의 유한 valuation word는 자연수 전체에서
흩어진 임의 집합이 아니라 정확히 하나의 \(2^{S+1}\) 산술
cylinder다. 그 cylinder 안에서 주어진 시간의 하강 여부는
`처음에는 실패하고 이후에는 모두 성공하는` 정확한 tail이다. 그러나
다음 valuation 값은 위로 제한되지 않으므로, 부모 cylinder를 더 긴
word 몇 개만으로 전부 덮으려는 유한 트리는 반드시 자연수 시작점
하나 이상을 놓친다.

### 2.2 Proof / 증명

The affine identity gives the exact congruence

\[
3^m n+C_a\equiv 2^S\pmod {2^{S+1}}.
\]

Because \(3^m\) is invertible modulo \(2^{S+1}\), it has one residue
solution. Reversing the affine recurrence shows that this final congruence
implies every required exact prefix valuation.

Also,

\[
T^m(n)-n=\frac{C_a-D_a n}{2^S},
\]

which proves the terminal-tail classification.

Let \(t=T^m(r_a)\). Along the parent cylinder,

\[
T^m(r_a+k2^{S+1})=t+2\cdot3^m k.
\]

To force the next valuation to equal \(b\), solve

\[
\frac{3t+1}{2}+3^{m+1}k
\equiv 2^{b-1}\pmod {2^b}.
\]

The coefficient \(3^{m+1}\) is invertible modulo \(2^b\), so a solution
exists for every \(b\). If a finite strict-extension family has maximum first
new valuation \(B\), choose \(b=B+1\). The resulting natural start belongs to
the parent cylinder and none of the proposed children.

한국어 증명에서 중요한 점은 마지막 합동식의 계수가 홀수라는 것이다.
따라서 모든 \(b\)에 대해 정확한 다음 valuation을 만드는 \(k\)가
존재한다. 유한 트리가 사용한 첫 확장 valuation의 최댓값보다 하나 큰
값을 택하면 즉시 미피복 자연수 반례를 구성할 수 있다.

### 2.3 Computation and limit / 계산과 한계

Ten cylinder words were checked over their first 64 lifts. Twenty-five
constructive witnesses realize next valuations beyond finite caps
\(4,8,16,24,32\). This is not a divergent Collatz orbit; it is a proof that
the finite strict-extension-cover strategy is impossible.

열 개 word에 대해 처음 64개 lift의 exact cylinder와 하강 tail을
검사했고, 유한 cap을 벗어나는 다음 valuation witness 25개를
구성했다. 이것은 발산 궤도가 아니다. 유한 strict-extension cover
전략이 불가능하다는 정리다.

**Remaining gap / 남은 간극.** Prove a countable extension cover together
with a uniform analytic estimate for the unbounded valuation tail, and show
that every represented natural start reaches a descending leaf.

## 3. Strong Goldbach conjecture / 강한 골드바흐 추측

### 3.1 Declared proposition / 선언 명제

For even \(N\), use the reflection \(\tau_N(a)=N-a\) on
\(\{1,\ldots,N-1\}\). For the constant baseline \(w_N(a)=1\), the exact
squared distance to the nonnegative endpoint-hole set is

\[
\rho_N(w_N)^2=\frac N2.
\]

For the von Mangoldt function,

\[
\|\Lambda-1\|_{2,[1,N-1]}^2
\sim N\log N,
\]

and therefore

\[
\frac{\|\Lambda-1\|_2^2}{\rho_N(1)^2}
\sim 2\log N\longrightarrow\infty.
\]

More generally, if \(0<c\le w_N(a)\le C\) with constants independent of
\(N\), then \(\rho_N(w_N)^2=O(N)\) while
\(\|\Lambda-w_N\|_2^2\sim N\log N\). Thus the global \(L^2\) sufficient
condition proposed after TICKET-151 is asymptotically unreachable for every
uniformly bounded dense baseline.

한국어로 말하면, endpoint-hole 반지름 정리 자체는 정확하지만 이를
전역 von Mangoldt \(L^2\) 근사와 결합한 다음 표적이 너무 강했다.
허용 반지름의 제곱은 \(N\) 크기인데 실제 von Mangoldt fluctuation
energy는 \(N\log N\) 크기다. Goldbach가 참이더라도 이 전역 ball
조건은 큰 \(N\)에서 실패한다.

### 3.2 Proof / 증명

The reflection contains \((N-2)/2\) two-cycles and one fixed point. The
exact weighted-hole theorem from TICKET-151 assigns cost one to each orbit,
so

\[
\rho_N(1)^2=(N-2)/2+1=N/2.
\]

The prime number theorem and partial summation give

\[
\sum_{n\le N}\Lambda(n)^2=N\log N+O(N),
\qquad
\sum_{n\le N}\Lambda(n)=N+o(N).
\]

Expanding the square proves the asymptotic. For bounded \(w_N\),

\[
\rho_N(w_N)^2\le \frac{C^2N}{2}
\]

and

\[
\sum(\Lambda-w_N)^2
\ge \sum\Lambda^2-2C\sum\Lambda
=N\log N+O(N).
\]

한국어 증명은 reflection orbit의 개수와 von Mangoldt 제2모멘트의
성장률을 비교하는 것이다. 이 결과는 전역 norm을 폐기할 뿐,
endpoint convolution에서 일어나는 signed cancellation을 부정하지
않는다.

### 3.3 Reproducible computation / 재현 계산

| \(N\) | \(\|\Lambda-1\|_2^2/\rho_N(1)^2\) | finite \((\Lambda*\Lambda)(N)>0\) |
|---:|---:|---:|
| 1,000 | 9.5596 | yes |
| 10,000 | 14.3475 | yes |
| 100,000 | 18.9983 | yes |
| 1,000,000 | 23.6076 | yes |

The finite positivity column is evidence only. It cannot prove all even
endpoints.

마지막 열은 해당 네 유한 endpoint에서의 재현 확인일 뿐이다. 모든
짝수에 대한 증명이 아니다.

**Remaining gap / 남은 간극.** For an endpoint-adapted main term \(w\),
prove

\[
2\sum_a w(a)e(N-a)+\sum_a e(a)e(N-a)>-R_N(w),
\quad e=\Lambda-w,
\]

uniformly beyond the verified finite range, with explicit major/minor-arc
constants.

## 4. Twin Prime conjecture / 쌍둥이 소수 추측

### 4.1 Declared proposition / 선언 명제

Let \(x_1,\ldots,x_M\in\{-1,+1\}\) have total \(A<0\). Retain
\(E=M-q\) entries. Every retained \(E\)-subset has negative sum if and only
if

\[
q<-A,
\]

or equivalently

\[
\frac EM>1+\frac AM.
\]

This threshold is sharp.

On the one-variable cubic-rough population, the Liouville mean tends to

\[
\frac{\log2-1}{\log2+1}.
\]

An ambient-only deletion argument would therefore require asymptotic
retention above

\[
\frac{2\log2}{1+\log2}\approx0.8187.
\]

Standard sieve estimates give one-variable rough mass of order
\(X/\log z\) and gap-two rough-pair mass at most of order
\(X/(\log z)^2\). Hence the selected coverage tends to zero. The ambient
`log 2` bias cannot transfer to the selected gap-two support through
worst-case deletion robustness.

한국어로는 다음과 같다. 주변 집합의 Liouville 평균이 음수라는 사실만
사용한다면, 선택 과정에서 전체의 약 18.1%보다 많이 버리는 순간
선택 집합의 부호를 보장할 수 없다. 실제 cubic-rough gap-two 선택은
주변 rough 수의 대부분을 버리며 선택률은 0으로 간다. 따라서 주변
`log 2` 편향을 보존율 논리로 이전하는 경로는 닫혔다.

### 4.2 Proof / 증명

The maximum possible sum of an \(E\)-subset is \(E\) if the ambient set has
at least \(E\) positive signs. Otherwise delete negative signs first; the
maximum becomes

\[
A+q.
\]

For \(A<0\), every selected sum is negative exactly when \(A+q<0\), that is,
\(q<-A\). The same construction attains zero or a positive value whenever
the inequality fails, proving sharpness.

The cubic-rough ambient limit comes from the prime/semiprime ratio
\(1:\log2\) established in TICKET-151. Buchstab/linear-sieve estimates count
one rough variable, and the Selberg upper-bound sieve counts the admissible
pair \((n,n+2)\). Dividing the two orders yields \(O(1/\log z)\to0\).

한국어 증명에서 finite combinatorial 부분은 완전히 exact하다. 선택
합을 가장 크게 만들려면 음수 부호부터 버리면 된다. 점근적 coverage
부분은 표준 one-dimensional rough count와 two-dimensional
upper-bound sieve를 사용한다. 이 단계는 실제 shifted Liouville
부호를 계산하지 않는다.

### 4.3 Reproducible computation / 재현 계산

| \(X\) | gap-two selected coverage | finite worst-case threshold | actual selected signs |
|---:|---:|---:|---|
| 1,000 | 0.3084 | 0.5551 | both negative |
| 10,000 | 0.2281 | 0.5719 | both negative |
| 100,000 | 0.1888 | 0.6513 | both negative |
| 1,000,000 | 0.1598 | 0.7003 | both negative |

The actual finite signs are encouraging but do not follow from the ambient
mean and do not imply an all-scale theorem.

실제 유한 표본의 좌우 shifted sum은 모두 음수였다. 그러나 이 부호는
주변 평균만으로 논리적으로 따라오지 않으며, 유한 표본이 무한 정리를
대체하지도 않는다.

**Remaining gap / 남은 간극.** Estimate the two shifted Liouville sums
directly on the cubic-rough gap-two support and prove a uniform negative
proportion together with positive rough-pair mass.

## 5. What changed / 이번 라운드의 의미

TICKET-152 establishes:

1. An exact RH compression exhaustion theorem and a finite-cutoff
   counterexample family.
2. An exact Collatz arithmetic-cylinder tail theorem and a proof that finite
   strict extension trees cannot cover a nonterminal cylinder.
3. A Goldbach no-go showing that the proposed global \(L^2\) transfer is
   asymptotically incompatible with von Mangoldt energy.
4. A sharp Twin selection-transfer threshold and a sieve-based proof that
   cubic-rough gap-two coverage is far too sparse for this transfer.

TICKET-152 does **not** establish:

1. Positivity of the actual Weil form.
2. Universal stopping of Collatz trajectories.
3. Goldbach representations for every even integer.
4. Infinitely many twin primes.

한국어 요약:

1. RH에서는 유한 행렬 검사에 tail norm certificate가 반드시
   필요함을 정확히 확정했다.
2. Collatz에서는 finite extension tree가 전체 cylinder를 덮는다는
   다음 표적을 반례 구성으로 폐기했다.
3. Goldbach에서는 전역 \(L^2\) 오차 조건이 큰 범위에서 도달
   불가능함을 증명하고 endpoint bilinear error로 표적을 바꿨다.
4. Twin에서는 주변 편향의 단순 선택 이전을 폐기하고 shifted
   Liouville 합을 직접 추정해야 함을 확정했다.

네 추측의 해결 상태는 모두 `open_not_proven`이다.

## References / 참고문헌

1. A. Connes and C. Consani, [The Scaling
   Hamiltonian](https://arxiv.org/abs/1910.14368).
2. Z. Niu, [Parity vectors and paradoxical sequences in the accelerated
   Collatz map](https://arxiv.org/abs/2605.13886).
3. H. A. Helfgott, [Minor arcs for Goldbach's
   problem](https://arxiv.org/abs/1205.5252).
4. K. Ford and J. Maynard, [On the theory of prime producing
   sieves](https://arxiv.org/abs/2407.14368).

These references define the surrounding established methods. PrimeProject's
new claims in this ticket are limited to the propositions and deductions
proved above; no novelty claim is made for the classical PNT, Buchstab, or
Selberg-sieve inputs themselves.
