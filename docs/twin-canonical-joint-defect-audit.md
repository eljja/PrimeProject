# TICKET-122: Canonical joint scalar-vector defect audit

## Claim boundary / 주장 경계

TICKET-122 does **not** prove the Twin Prime Conjecture, eventual positivity of the Vaughan endpoint comparison, or a fixed-shift Möbius decorrelation theorem. It proves an exact scalar-vector saving identity for every canonical adjacent shell pair, constructs two exact no-go families for incomplete local routes, and audits the complete finite canonical-pair budget on eight scales.

TICKET-122는 **쌍둥이 소수 추측, 충분히 큰 모든 규모에서의 Vaughan endpoint 양성, 고정 shift Möbius decorrelation 정리를 증명하지 않습니다.** 모든 정준 인접 shell 쌍의 스칼라 평균부와 중심 벡터부를 함께 다루는 정확한 절감 항등식을 증명하고, 국소 조건만으로 전역 절감률을 얻으려는 두 경로를 반례족으로 폐기합니다.

## Why TICKET-121 was still local / TICKET-121이 여전히 국소적이었던 이유

TICKET-121 corrected the first-pair centered condition to `norm balance × angle gap × denominator mass`. Three gaps remained:

1. the first pair need not carry a fixed share of the full outer-divisor budget;
2. centered-vector cancellation does not control the scalar block means;
3. an odd final shell, Farey boundary, and Abel variation remain outside the first-pair certificate.

따라서 첫 인접 쌍의 중심 절감만으로는 전체 정준 예산을 닫을 수 없습니다. TICKET-122는 정준 분할을 결과에 맞춰 다시 최적화하지 않고, 모든 인접 쌍과 남는 단일 블록을 동일한 식에 넣습니다.

## Exact joint identity / 정확한 결합 항등식

For one Farey denominator and one adjacent pair, let `m0,m1` be the real block means and write

```text
a = ||z0||,  b = ||z1||,  c = Re<z0,z1>,
p = ||z0+z1||,  w >= 0.
```

Then

```text
|m0| + |m1| - |m0+m1| + w(a+b-p)
  = 2 1_{m0*m1<0} min(|m0|,|m1|)
    + 2w(ab-c)/(a+b+p).
```

The scalar term is exact because opposite signs cancel exactly twice the smaller magnitude; equal signs do not cancel. The centered term is the TICKET-121 rationalization. Hence

```text
joint saving
  >= 2 1_{m0*m1<0} min(|m0|,|m1|)
     + w(ab-c)/(a+b).
```

이 식은 일반적인 Hilbert 공간 부등식으로 정확하며, 각 Farey 분모와 미리 고정된 모든 정준 인접 dyadic 쌍에 대해 합산할 수 있습니다. 다만 우변이 실제 정수 Vaughan kernel에서 충분히 큰 모든 규모에 걸쳐 양의 비율을 갖는지는 별도의 산술 정리입니다.

## Two exact no-go families / 두 정확한 반례족

### A first-pair theorem cannot control an arbitrary outer tail

Use `z0=u,z1=-u` in the first pair and append `z2=Mv,z3=Mv`. The first pair saves 100%, the outer pair saves zero, and

```text
global saving fraction = 1/(1+M) -> 0.
```

따라서 첫 쌍의 balance-angle-mass 정리만으로 전역 고정 절감률을 얻을 수 없습니다. 바깥 쌍의 질량 또는 절감도 함께 제어해야 합니다.

### Centered cancellation cannot control arbitrary scalar means

Use `z0=u,z1=-u` but set same-sign means `m0=m1=M`. Centered saving is complete while mean saving is zero, so

```text
total saving fraction = 1/(1+M) -> 0.
```

따라서 중심 벡터 조건만으로 평균부까지 포함한 전체 예산의 고정 절감률을 얻을 수 없습니다. 이 반례들은 Twin Prime 자체의 반례가 아니라, 불충분한 보조정리의 반례입니다.

## Complete finite canonical audit / 전체 유한 정준 감사

The unchanged canonical rule groups dyadic outer-divisor shells as `(B0,B1),(B2,B3),...`; an odd final shell remains a singleton. The baseline is the independent-shell triangle budget. The audited saving is exactly the difference between that baseline and the canonical paired budget.

| horizon | total saving | joint lower certificate | residual singleton share | first-pair share of saving | finite margin | closes? |
|---:|---:|---:|---:|---:|---:|---|
| 4,096 | 28.4511% | 23.1207% | 0 | 41.5714% | -1,689.6 | no |
| 32,768 | 23.3264% | 19.0643% | 0 | 60.1132% | -19,936.4 | no |
| 262,144 | 23.2035% | 19.0898% | 0.3743% | 50.2408% | -63,546.4 | no |
| 1,048,576 | 26.3648% | 21.3804% | 0 | 51.4085% | -128,296.3 | no |
| 2,097,152 | 21.4769% | 17.6892% | 0 | 55.9647% | -112,746.7 | no |
| 4,194,304 | 23.1993% | 18.8756% | 0 | 54.5497% | -1,236.3 | no |
| 8,388,608 | 22.9115% | 18.4345% | 0.9895% | 58.5593% | +156,727.0 | yes |
| 16,777,216 | 19.3458% | 16.0000% | 0.2397% | 60.5758% | +1,479,021.8 | yes |

Machine coverage:

| metric | value |
|---|---:|
| scales | 8 |
| canonical pair groups | 28 |
| pair-denominator rows | 868 |
| minimum exact total saving fraction | 19.3458% |
| minimum joint certificate fraction | 16.0000% |
| maximum residual singleton share | 0.9895% |
| maximum reconstruction error | `9.32e-10` |
| audit failures | 0 |

These are finite diagnostics, not asymptotic constants. In particular, the exact total saving fraction falls from `22.9115%` at 8M to `19.3458%` at 16M. No monotonicity or positive limiting infimum is inferred.

이는 유한 기술 통계이지 점근 정리 상수가 아닙니다. 8M과 16M의 통과만으로 이후 모든 규모의 통과를 주장하지 않습니다.

## Correct infinite target / 교정된 무한 목표

Define

```text
K_X = known_without_type_ii_minor,
B_X = independent singleton shell budget,
D_X = exact canonical joint saving,
E_X = boundary and variation budget.
```

The canonical adverse budget is `B_X-D_X+E_X`. The exact target is

```text
K_X - (B_X-D_X) - E_X >= delta K_X
```

for fixed `delta>0` and every `X>=X0`. Equivalently,

```text
D_X >= B_X + E_X - K_X + delta K_X.
```

Name:

```text
VaughanCanonicalPairJointDefectAndResidualBudgetGap
```

This target forces one theorem to control scalar opposite-sign balanced mass, centered balance-angle mass, all outer-pair tails, the odd residual shell, and boundary/variation. It cannot be replaced by a theorem about only the first pair or only the centered component.

반례 경로도 동일하게 명확합니다. 실제 Vaughan 계수로 실현되는 무한 규모열에서 정규화된 surplus가 0 이하가 되거나 0으로 수렴함을 인증하면 이 증명 경로가 반증됩니다.

## Literature boundary / 문헌 경계

- [Ford and Maynard, *On the theory of prime producing sieves*](https://arxiv.org/abs/2407.14368): prime-producing lower bounds use Type I and Type II information jointly and construct extremal sequences for insufficient information contracts. PrimeProject must therefore state the full joint budget, not a local cancellation surrogate.
- [Tao, *The logarithmically averaged Chowla and Elliott conjectures for two-point correlations*](https://arxiv.org/abs/1509.05422): proves fixed-shift two-point Liouville cancellation with logarithmic averaging. The PrimeProject endpoint budget is unweighted and structurally different.
- [Sawin and Shusterman, *On the Chowla and twin primes conjectures over F_q[T]*](https://annals.math.princeton.edu/2022/196-2/p01): the function-field twin-prime theorem uses strong distribution and geometric short-sum input not presently available over the integers. It is a model of the missing input, not a proof transfer.

## Keep, discard, next / 유지·폐기·다음

Keep:

- the exact scalar opposition identity;
- the exact centered rationalization and quadratic certificate;
- result-independent canonical adjacent pairing;
- the full surplus equation including residual and boundary terms;
- both no-go families as mandatory theorem tests.

Discard:

- first-pair control as a substitute for an outer-tail theorem;
- centered balance-angle control as a substitute for scalar-mean control;
- any monotonicity inference from the 8M and 16M finite passes;
- transferring this Twin-specific identity to RH, Collatz, or Goldbach.

Next:

1. expand the exact surplus by canonical outer-divisor range;
2. isolate adverse outer pairs and the residual shell before absolute values;
3. test whether their coefficients satisfy a usable Type I/II or weighted large-sieve contract;
4. search simultaneously for Vaughan-realizable sequences with nonpositive normalized surplus;
5. prove or refute `VaughanCanonicalPairJointDefectAndResidualBudgetGap`.

## Reproduction / 재현

```powershell
python scripts/ticket122_twin_canonical_joint_defect_audit.py
python -m unittest tests.test_ticket122_twin_canonical_joint_defect_audit
```

Artifact: `data/open-problem/ticket122-twin-canonical-joint-defect-audit.json`.
