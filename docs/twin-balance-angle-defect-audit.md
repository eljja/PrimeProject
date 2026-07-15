# TICKET-121: Low-divisor balance-angle defect audit

## Claim boundary / 주장 경계

TICKET-121 does **not** prove the Twin Prime Conjecture, an eventual Vaughan endpoint bound, or a fixed-shift Möbius decorrelation theorem. It proves an elementary rationalized saving identity, gives exact counterexample families to two incomplete strengthening routes, and replaces the underspecified TICKET-120 angle-gap target by a quantitative balance-angle-mass condition.

TICKET-121은 **쌍둥이 소수 추측, 충분히 큰 모든 규모의 Vaughan endpoint 상계, 고정 shift Möbius decorrelation 정리를 증명하지 않습니다.** 중심 벡터 절감의 정확한 유리화 항등식을 증명하고, angle 또는 norm balance 하나만으로 고정 절감률을 얻으려는 두 경로를 정확한 반례족으로 폐기합니다.

## Why TICKET-120 needed correction / TICKET-120 목표를 교정한 이유

TICKET-120 showed that the 16M first-pair saving comes almost entirely from centered vector geometry. Its next target was called `VaughanLowDivisorDenominatorSummedAngleGap`. That name hides a second necessary factor: two vectors can be maximally anti-aligned while one norm tends to zero, in which case their relative saving also tends to zero.

따라서 angle gap만 증명해서는 충분하지 않습니다. 인접 dyadic shell 두 개가 충분히 비슷한 norm을 가져야 하고, 그런 balanced 분모가 전체 중심 예산에서 양의 질량을 차지해야 합니다.

## Exact rationalization / 정확한 유리화

For one Farey denominator, write

```text
a = ||z0||,  b = ||z1||,  c = Re<z0,z1>,
p = ||z0+z1||,  w >= 0.
```

Then

```text
w(a+b-p) = 2w(ab-c)/(a+b+p).
```

Because `0 <= p <= a+b`,

```text
w(ab-c)/(a+b)
    <= w(a+b-p)
    <= 2w(ab-c)/(a+b).
```

Define

```text
b_q       = ab/(a+b)^2,
kappa_q   = c/(ab),
defect_q  = b_q(1-kappa_q).
```

The denominator-summed centered saving fraction is at least the singleton-mass-weighted mean of `defect_q`. This lower certificate uses the Gram cross term before the square root and is within a factor of two of the exact saving.

## Exact no-go families / 정확한 반례족

### Angle gap alone fails

Let `z0=u` and `z1=-epsilon*u`. The cosine is always `-1`, so the angle gap is maximally `2`, but

```text
centered saving fraction = 2 epsilon/(1+epsilon) -> 0.
```

Thus no fixed saving fraction follows from a cosine gap without norm balance.

### Norm balance alone fails

Let `||z0||=||z1||=1` and let their angle be `theta`. Norm balance remains maximally `1/4`, but

```text
centered saving fraction = 1-cos(theta/2) -> 0.
```

Thus no fixed saving fraction follows from balance without angular decorrelation.

These are counterexamples to proposed auxiliary lemmas, not counterexamples to Twin Prime.

## Corrected sufficient condition / 교정된 충분조건

For an interpretable exploratory audit, use the simple rational thresholds

```text
norm balance >= 1/8,
angle gap   >= 1/2,
mass share  >= 1/2.
```

If at least half of the first-pair centered singleton mass satisfies the first two conditions, then

```text
centered saving fraction >= (1/2)(1/8)(1/2) = 1/32.
```

The implication is universal, but these displayed thresholds were selected during TICKET-121 and were not preregistered or evaluated on a new holdout. Their eight-row pass is descriptive evidence only.

충분조건 자체는 보편적이지만, 표시한 임계값은 TICKET-121 분석 중 선택됐고 새 holdout에 사전등록되지 않았습니다. 따라서 아래 8개 행의 통과는 탐색적 기술 통계입니다.

The eight finite rows all satisfy the mass condition:

| metric | finite range |
|---|---:|
| qualifying mass fraction | `0.638848` to `0.801681` |
| quadratic certified fraction | `0.179685` to `0.251684` |
| certificate / exact centered saving | `0.772728` to `0.832405` |
| active denominator rows | 216 of 248 |
| rationalization error | at most `9.10e-11` |
| audit failures | 0 |

These values are diagnostics, not theorem constants.

## Full-budget strength / 전체 예산에 필요한 강도

Holding all non-low-pair finite budgets fixed gives:

| horizon | required low-pair centered fraction | `1/32` margin | closes? |
|---:|---:|---:|---|
| 8M | `0.230067` | `-377,817.5` | no |
| 16M | `0` | `+756,220.8` | yes |

This comparison prevents a second overclaim. A positive low-pair constant is not by itself a full proof. One must also prove that the remaining canonical groups, Farey boundary, Abel variation, and comparison main term are eventually subcritical.

## Retained theorem / 유지할 정리

```text
VaughanLowDivisorWeightedBalanceAngleDefectGap
```

Prove fixed `beta,gamma,rho>0` and `X0` such that every `X>=X0` places at least `rho` of the first canonical pair centered singleton mass on denominators satisfying

```text
ab/(a+b)^2 >= beta,
Re<z0,z1>/(ab) <= 1-gamma.
```

Then the first-pair centered saving fraction is at least `rho*beta*gamma`. The cross term has the arithmetic expansion

```text
c_q = sum_{d in B0} sum_{e in B1}
      mu(d) mu(e) Re<K_X(d;q), K_X(e;q)>,
```

where `K_X` is the centered Farey endpoint kernel. The missing theorem must control this fixed-shift Vaughan-realizable kernel. Generic Hilbert geometry cannot do so.

Counterexample route: construct an unbounded Vaughan-realizable scale sequence on which balanced-decorrelated denominator mass tends to zero, or on which the remaining canonical budget defeats every fixed margin.

## Literature boundary / 문헌 경계

- [Lichtman, *Averages of the Möbius function on shifted primes*](https://arxiv.org/abs/2009.08969): proves cancellation after averaging over sufficiently many shifts, not the fixed shift-two kernel above.
- [Ford and Maynard, *On the theory of prime producing sieves*](https://arxiv.org/abs/2407.14368): shows why Type I/II information must be used jointly and why extremal comparison sequences are necessary falsification tools.
- [Maynard, *Primes in arithmetic progressions to large moduli II*](https://arxiv.org/abs/2006.07088): obtains strong distribution estimates with suitably well-factorable weights. PrimeProject has not proved the required factorability for its endpoint kernel.

## Keep, discard, next / 유지·폐기·다음 단계

Keep:

- the exact rationalized saving identity;
- the quadratic defect before square roots;
- the three-factor `balance × angle × mass` sufficient condition;
- both no-go sequences as mandatory theorem tests.

Discard:

- a cosine gap without norm balance;
- norm comparability without angular decorrelation;
- the claim that any positive first-pair constant closes every scale;
- transferring this Twin-specific result to RH, Collatz, or Goldbach.

Next:

1. expand `c_q` into the signed outer-divisor kernel;
2. seek a result-independent denominator set with provable positive mass;
3. apply weighted large-sieve or dispersion estimates without separating the Möbius signs;
4. generate Vaughan-realizable escaping sequences as the matching counterexample oracle;
5. keep `EventuallySubcriticalCanonicalAdjacentDyadicPairVaughanEndpointBudget` open.

## Reproduction

```powershell
python scripts/ticket121_twin_balance_angle_defect_audit.py
python -m unittest tests.test_ticket121_twin_balance_angle_defect_audit
```

Artifact: `data/open-problem/ticket121-twin-balance-angle-defect-audit.json`.
