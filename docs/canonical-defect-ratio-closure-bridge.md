# TICKET-123: Canonical Defect Ratio Closure Bridge

Status: exact algebraic bridge proved; four proof-strategy no-go families proved; all four conjectures remain open.

상태: 정확한 대수적 연결 정리와 네 개의 증명 전략 반례족을 증명했다. 네 난제 자체는 모두 미해결이다.

## 1. Why TICKET-122 was not yet modular

TICKET-122 writes the canonical paired budget as `S-D`, where:

- `K > 0` is `known_without_type_ii_minor`;
- `S >= 0` is the independent singleton budget;
- `E >= 0` is the boundary-and-variation budget;
- `D >= 0` is the exact saving produced by canonical adjacent pairing.

The desired normalized margin is

```text
delta_X = [K - (S-D) - E] / K.
```

The exact defect identity proves how to calculate `D`. It does not by itself control the scale of `S` relative to `K`, or the boundary term `E`.

TICKET-122는 정준 pair 예산을 `S-D`로 정확히 썼지만, `D`가 양수라는 사실만으로 전체 예산이 닫히지는 않는다. 독립 예산 `S`가 비교항 `K`보다 얼마나 큰지, 경계항 `E`가 `K`의 몇 퍼센트인지도 동시에 제어해야 한다.

## 2. Exact ratio identity

Define

```text
eta     = D/S,
rho     = S/K,
epsilon = E/K.
```

For `K,S>0`, direct substitution gives the exact identity

```text
[K-(S-D)-E]/K = 1-(1-eta)rho-epsilon.                 (1)
```

This is not an asymptotic approximation. The machine audit reconstructs all eight TICKET-122 rows with maximum error `2.23e-16`.

식 (1)은 근사가 아니라 항등식이다. 따라서 무한 증명의 남은 내용을 세 개의 독립적인 산술 추정량으로 분리할 수 있다.

1. `eta`: 실제 정준 pair 절감률의 균일한 양의 하한
2. `rho`: 독립 singleton 예산과 알려진 양의 항의 비율 상한
3. `epsilon`: 경계·변동 예산의 비율 상한

## 3. Proved bridge

### CanonicalDefectRatioClosureBridge

Assume fixed constants satisfy

```text
K > 0,
0 <= eta <= 1,
D >= eta S,
S <= rho K,
E <= epsilon K,
(1-eta)rho + epsilon <= 1-delta.
```

Then

```text
K-(S-D)-E >= delta K.
```

### Proof

From `D >= eta S`,

```text
K-(S-D)-E >= K-(1-eta)S-E.
```

Because `1-eta >= 0`, the bounds on `S` and `E` imply

```text
K-(1-eta)S-E
  >= K-(1-eta)rho K-epsilon K
  = K[1-(1-eta)rho-epsilon]
  >= delta K.
```

This completes the algebraic proof.

이 정리는 실제로 증명되었다. 그러나 가정에 등장하는 균일한 `eta`, `rho`, `epsilon`을 Vaughan 커널에 대해 확보한 것은 아니다. 따라서 Twin Prime 증명은 아니다.

## 4. Exact finite ledger

| `X` | exact `eta` | certified `eta` | `rho=S/K` | `epsilon=E/K` | critical `eta` | exact margin | certified margin |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4,096 | 0.285 | 0.231 | 2.665 | 0.053 | 0.645 | -0.960 | -1.102 |
| 32,768 | 0.233 | 0.191 | 3.039 | 0.102 | 0.705 | -1.432 | -1.562 |
| 262,144 | 0.232 | 0.191 | 1.908 | 0.072 | 0.514 | -0.538 | -0.616 |
| 1,048,576 | 0.264 | 0.214 | 1.654 | 0.060 | 0.432 | -0.278 | -0.360 |
| 2,097,152 | 0.215 | 0.177 | 1.359 | 0.054 | 0.304 | -0.121 | -0.173 |
| 4,194,304 | 0.232 | 0.189 | 1.241 | 0.048 | 0.233 | -0.0007 | -0.054 |
| 8,388,608 | 0.229 | 0.184 | 1.188 | 0.042 | 0.194 | +0.042 | -0.011 |
| 16,777,216 | 0.193 | 0.160 | 0.948 | 0.038 | -0.014 | +0.197 | +0.165 |

`critical eta` is `(S+E-K)/S`, the exact saving fraction required for zero margin at that finite row. Negative critical `eta` means `S+E<K`, so no pairing saving is required for that particular finite row.

정확 절감으로 닫히는 행은 8M과 16M 두 개뿐이다. 하한 인증서만으로 닫히는 행은 16M 하나뿐이다. 4M 행은 거의 0이지만 여전히 음수이므로 통과로 바꾸지 않는다.

## 5. Frontier attribution

Between 8M and 16M, the normalized exact margin changes by

```text
+0.1552742555.
```

The exact midpoint decomposition of identity (1) is:

```text
eta contribution      -0.0380664819
rho contribution      +0.1893933048
epsilon contribution  +0.0039474326
sum                   +0.1552742555
```

Thus the finite improvement is not caused by a stronger saving fraction. `eta` falls and contributes adversely. The improvement is dominated by the decrease in `S/K`.

8M에서 16M으로 좋아진 주된 이유는 pair 절감률 증가가 아니라 `S/K` 감소다. 이것은 다음 분석 우선순위를 알려 주지만, 두 점으로 점근 감소를 주장할 수는 없다.

## 6. Four exact no-go families

### 6.1 Saving fraction alone

Fix `eta=1/4`, `K=1`, `E=0`, `S=M`, and `D=eta S`. Then

```text
margin = 1-(1-eta)M -> -infinity.
```

A positive saving fraction without an `S/K` bound is insufficient.

### 6.2 Singleton ratio without boundary control

Fix `K=1`, `S/K=1/2`, and `D/S=1/5`, then let `E` grow. The margin tends to minus infinity. A bounded `S/K` does not replace a boundary estimate.

### 6.3 Non-strict compatibility

At `eta=1/5`, `rho=1`, and `epsilon=1/5`, the margin is exactly zero. Increasing `epsilon` by `t>0` makes the margin `-t`. Equality cannot prove any fixed positive `delta`.

### 6.4 Finite-prefix inference

For every finite `B`, set `K=1,S=D=2,E=0` through `B`, and set `K=1,S=2,D=E=0` at `B+1`. Every checked row passes and the first unseen row fails. No finite pass prefix implies eventual closure.

이 반례들은 Twin Prime의 반례가 아니다. 불충분한 보조정리와 잘못된 추론 형식에 대한 반례다.

## 7. Discarded legacy proxies for the other problems

### Riemann Hypothesis

Finite Jensen-polynomial hyperbolicity does not control every untested degree and shift and does not locate every nontrivial zeta zero. Retain `NonCircularExplicitFormulaKernelPositivity`.

유한 개 Jensen 다항식의 실근성은 RH 전체를 증명하지 않는다. 비순환적 explicit-formula kernel 양성 조건을 계속 공격한다.

### Collatz Conjecture

A finite stopping-time program verifies only terminating inputs. A loop that assumes every orbit eventually falls below its start embeds the missing descent claim in the algorithm. Density-one termination would still permit a sparse exceptional orbit. Retain `GoldenMeanInvariantSetEscape`.

유한 stopping-time 계산과 밀도 1은 모든 양의 정수를 덮지 않는다. 핵심 하강을 계산 절차에 선가정한 코드도 증명이 아니다.

### Goldbach Conjecture

Mean agreement with a singular-series prediction permits a sparse set of zero representation counts. Goldbach requires pointwise positivity for every sufficiently large even integer. Retain `JointBalancedVaughanGoldbachResidualEnvelope`.

평균 비율이 1에 가까워도 드문 예외 짝수의 표현 수가 0일 수 있다. 따라서 평균·푸리에 패턴은 점별 Goldbach 하한을 대체하지 못한다.

## 8. Retained TICKET-124 target

`VaughanCanonicalDefectRatioTriple` asks for fixed constants with

```text
D_X >= eta S_X,
S_X <= rho K_X,
E_X <= epsilon K_X,
(1-eta)rho+epsilon <= 1-delta,
eta>0, delta>0,
```

for every sufficiently large `X`.

The counterexample route is an unbounded Vaughan-realizable sequence defeating every compatible constant tuple through vanishing `D/S`, unbounded `S/K`, excessive `E/K`, or nonpositive combined margin.

## 9. Literature boundary

- Ford and Maynard's prime-producing sieve framework requires joint Type I/II information and supplies extremal constructions for weaker contracts: <https://arxiv.org/abs/2407.14368>
- Maynard's small-gap theorem proves bounded-gap results, not exact gap two: <https://annals.math.princeton.edu/2015/181-1/p07>
- Tao's two-point Chowla theorem is logarithmically averaged and does not provide this unweighted endpoint ratio triple: <https://arxiv.org/abs/1509.05422>

## 10. Claim boundary

TICKET-123 proves the ratio bridge and the four abstract proof-strategy countermodels. It does not prove a uniform Vaughan ratio triple, break the parity barrier, prove Twin Prime, prove RH, prove Collatz, prove Goldbach, or certify a counterexample to any of them.

TICKET-123은 다음 증명 의무를 더 작고 반증 가능한 세 부분으로 나눴다. 네 난제 자체의 증명이나 반례는 아직 없다.
