# TICKET-133: Quantifier Promotion and Exact Reductions

## 연구 상태 / Research status

**리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측은 모두
미해결이다.** TICKET-133은 네 가설의 증명이나 반례를 주장하지 않는다.
이번 단계는 TICKET-132의 정확한 공간과 hard stratum에서 출발하여, 유한·평균
정보를 전칭·점별 결론으로 올릴 때 필요한 조건을 네 개의 정리로 분해한다.

**RH, Collatz, strong Goldbach, and Twin Prime all remain open.** TICKET-133
proves four exact reduction or countermodel theorems. None is a conjecture proof
or conjecture counterexample.

Machine-readable record:
`data/open-problem/ticket133-quantifier-promotion-exact-reductions.json`.

> **Current boundary / 최신 경계:** TICKET-134 preserves the exact TICKET-133
> reductions and adds strict finite Gram interval certificates, a bounded-depth
> Collatz cover no-go theorem, the logarithmic Goldbach moment threshold, and a
> growing-primorial Twin lift bound. Continue from
> [TICKET-134](uniformity-thresholds-and-scale-no-go.md).

## 1. 결과 요약 / Executive result

| 문제 | 새 정확한 결과 | 폐기되는 추론 | 다음 결정적 정리 |
|---|---|---|---|
| RH | projected core 전칭 양성과 countable Gram family의 동치 | 유한 개 Gram 검사를 전칭 양성으로 승격 | interval-certified infinite Gram family |
| Collatz | contracting cylinder의 비하강 예외를 정확한 유한 집합으로 축소 | 평균 valuation surplus를 모든 경로의 descent로 승격 | 모든 natural code의 prefix-free contracting cover |
| Goldbach | 모든 finite Cesaro `L^p` 평균을 통과하는 power-of-two spike countermodel | 평균 잔차를 powers-of-two 점별 하계로 승격 | hard-stratum maximal `K=56` bound |
| Twin Prime | 모든 admissible finite residue class에 composite-composite lift가 존재 | fixed-modulus classifier를 소수쌍 판정기로 승격 | unbounded parity-sensitive separation |

네 결과는 계산 범위를 확대한 것이 아니다. 각 정리의 핵심은 무한한 범위에
대해 기호적으로 증명되며, 유한 계산은 구현과 경계 사례만 검산한다.

## 2. Riemann Hypothesis / 리만 가설

TICKET-132의 두 모멘트 constrained space를

```text
K = ker(L_+) intersect ker(L_-)
```

라 하고, projected core의 유리 선형 span을 `D`라 하자. `D`는 `K`에 조밀하다.
고정된 Weil 정규화의 연속 대칭 쌍선형 형식을 `B`, 이차형식을
`Q(f)=B(f,f)`라 한다.

### Theorem RH-133: `ProjectedWeilCoreGramFamilyEquivalence`

다음 두 명제는 동치다.

1. 모든 `f in K`에 대해 `Q(f)>=0`이다.
2. projected core 원소의 모든 유한 목록 `d_1,...,d_m`과 모든
   `q in Q^m`에 대해

   ```text
   q^T (B(d_i,d_j)) q >= 0
   ```

   이다.

또한 `K`에 엄격한 음수 witness가 있으면 어떤 유한 rational Gram inequality도
엄격히 음수다.

### Proof / 증명

첫 방향은 자명하다. 반대로 `D`의 모든 원소는 projected generator의 유한
유리 선형결합이므로 Gram 가정에 의해 `D`에서 `Q>=0`이다. 임의의 `f in K`에
대해 `d_n in D`, `d_n -> f`를 택하면 연속성으로

```text
Q(f) = lim Q(d_n) >= 0.
```

`Q(f)<0`이면 strict-negative set은 열린집합이고, `D`의 조밀성 때문에 그
안에 유한 유리 선형결합이 존재한다. 이것이 유한 Gram 음수 witness다. `QED`

이 정리는 TICKET-131의 finite-positivity no-go와 충돌하지 않는다. **각각의
유한 Gram 검사**는 충분하지 않지만, **모든 유한 Gram inequality의 무한
family**는 연속성 아래 정확히 전칭 양성과 동치다.

```text
Next:
IntervalCertifiedProjectedWeilGramFamily
```

필요한 것은 하나의 출판된 Weil 정규화, computable-real Gram entry의 외향
구간 계산, 모든 inequality를 다루는 새 구조 정리 또는 하나의 엄격한 음수
witness다. TICKET-133은 실제 Weil Gram inequality를 하나도 증명하지 않는다.

## 3. Collatz Conjecture / 콜라츠 추측

양의 홀수에서 accelerated map을 `A`라 하고 유한 valuation word를
`w=(a_1,...,a_k)`라 하자. `S=sum a_i`이고 exact natural cylinder가
`n=r+tM`, `t>=0`이라 하자.

### Theorem CO-133: `ContractingValuationCylinderLeastCounterexampleExclusion`

귀납으로 계산되는 양의 정수 `c_w`에 대해

```text
A^k(n) = (3^k n + c_w) / 2^S.
```

`g_w=2^S-3^k>0`이면

```text
A^k(n)<n  iff  n>c_w/g_w.
```

따라서 해당 cylinder의 비하강 natural realizer 개수는 정확히

```text
max(0, floor((floor(c_w/g_w)-r)/M)+1)
```

이다. 이 유한 예외가 모두 종료함을 직접 검증하면 그 cylinder 전체에는
least counterexample가 존재할 수 없다.

### Proof / 증명

`c_0=0`, `S_0=0`에서

```text
c_j = 3c_(j-1) + 2^S_(j-1)
```

로 두고 accelerated step을 귀납 적용하면 affine 식을 얻는다. 이를
`A^k(n)<n`에 대입하면 `c_w<g_w n`이다. `g_w>0`에서 threshold가 나오며,
산술진행 `r+tM`과 유한 구간의 교집합을 세면 위 개수식이 얻어진다.

전역 least counterexample `N`이 threshold보다 크다면 `A^k(N)<N`이므로
최소성에 모순이다. threshold 이하의 유한 예외는 독립적으로 종료 검증할 수
있다. `QED`

`a_i in {1,...,5}`, 깊이 1부터 5까지의 감사 결과:

- 전체 word: `3,905`;
- contracting cylinder: `3,861`;
- noncontracting cylinder: `44`;
- 모든 contracting cylinder의 고유 비하강 예외: `1`개, 즉 `n=1`;
- affine, boundary, termination 실패: `0`.

이는 44개 비수축 cylinder의 무한 extension을 닫지 않는다. 다음 정리는 모든
실제 natural code가 유한 깊이에서 certified contracting cylinder에 들어감을
보여야 한다.

```text
Next:
PrefixFreeContractingCylinderCoverOfEveryNaturalCode
```

이 명제는 사실상 pointwise descent의 핵심이므로 유한 tree에서 관찰됐다는
이유만으로 증명됐다고 할 수 없다.

## 4. Strong Goldbach Conjecture / 강한 골드바흐 추측

TICKET-132의 최소 singular-series `K=56` endpoint margin을

```text
m_56 = 23019645297 / 2140000000000 > 0
```

라 하자.

### Theorem GB-133: `PowerOfTwoSparseSpikesDefeatEveryFiniteCesaroLpBridge`

짝수 `N`에 대해 추상 normalized residual perturbation을

```text
e(2^j) = -2m_56,
e(N)   = 0 otherwise
```

로 정의하자. 모든 고정 `0<p<infinity`에 대해

```text
average_(even N<=X) |e(N)|^p -> 0,
```

이지만 모든 power of two에서

```text
m_56 + e(2^j) = -m_56 < 0.
```

### Proof / 증명

`X` 이하 powers of two는 `O(log X)`개이고 짝수는 `X/2+O(1)`개다. 따라서

```text
average |e|^p <= 2 log_2(X) |2m_56|^p / (X-2) -> 0.
```

반면 support에서는 정의에 의해 endpoint margin이 정확히 음수가 된다. `QED`

이 `e`는 실제 Goldbach residual이 아니다. 평균·밀도 정리만으로 점별
powers-of-two positivity를 얻는 **논리적 추론의 countermodel**이다.

```text
Discard:
finite Cesaro Lp control => all-even pointwise positivity

Next:
HardStratumMaximalBinaryGoldbachResidualK56
```

다음 정리는 powers of two와 rough even integers에서 supremum 또는 maximal
inequality를 제공해야 한다.

## 5. Twin Prime Conjecture / 쌍둥이 소수 추측

유한 소수 집합 `P`, `W=product_(p in P) p`를 고정한다. `a mod W`가 모든
`p in P`에 대해 `a`와 `a+2`를 0이 아니게 만드는 admissible class라고 하자.

### Theorem TP-133: `EveryAdmissibleFiniteResidueClassHasInfiniteCompositePairLifts`

`P` 밖의 서로 다른 소수 `q,r`에 대해 다음을 만족하는 `n`의 무한
산술진행이 존재한다.

```text
n == a  (mod W),
n == 0  (mod q),
n == -2 (mod r).
```

충분히 큰 모든 항에서 `n`과 `n+2`는 모두 합성수이며, 전체 `W` residue는
원래 admissible class와 정확히 같다.

### Proof / 증명

`W,q,r`는 서로소이므로 CRT가 `mod Wqr`의 유일한 class를 준다. 이 진행의
모든 항은 `a mod W`를 보존한다. 충분히 큰 항에서 `q`와 `r`는 각각 `n`과
`n+2`의 proper divisor다. `QED`

기계 감사는 `z=5,7,11,13`의 primorial에서 admissible class `1,638`개 전부를
lift했고 실패는 0이었다. TICKET-132가 한 clean signature를 구성했다면,
TICKET-133은 **모든** finite admissible residue pattern으로 전사함을 증명한다.

따라서 `n mod W`만의 함수인 어떤 classifier도 prime pair와 모든 합성수 lift를
분리할 수 없다.

```text
Next:
UnboundedParitySensitiveTwinPairSeparation
```

이 정리는 scale과 함께 커지는 Type II 또는 다른 전역 정보를 사용해야 한다.

## 6. 교차 문제 정리 / Cross-problem synthesis

네 문제에 공통으로 “유한 정보가 부족하다”는 표어만 적용하는 것은 의미가
없다. TICKET-133은 필요한 universal control이 서로 다름을 정확히 분리한다.

| 문제 | 필요한 무한 승격 장치 |
|---|---|
| RH | countable Gram family 전체의 양성 또는 strict-negative witness |
| Collatz | 모든 natural code를 덮는 adaptive prefix-free contracting cover |
| Goldbach | sparse hard stratum의 maximal pointwise residual bound |
| Twin Prime | fixed residue quotient를 넘는 unbounded parity information |

compactness, density, 평균 수렴은 proof-search를 조직할 수 있지만 이 네 장치를
서로 대신할 수 없다.

## 7. 증명 가능성 평가 / Proof viability

| 문제 | 실제 개선 | 완전 증명과의 거리 |
|---|---|---|
| RH | 전칭 양성 목표를 정확한 countable family로 환원 | family를 일괄 제어할 구조 정리가 없어 멀다 |
| Collatz | contracting cylinder를 finite exceptions로 완전히 환원 | 모든 natural path의 adaptive cover가 없어 멀다 |
| Goldbach | 모든 finite-`L^p` 평균 shortcut을 정확히 폐기 | 점별 `K=56` maximal bound가 여전히 큰 분석적 간극이다 |
| Twin Prime | 모든 fixed admissible class의 composite lift를 증명 | parity barrier와 exact-gap positivity가 모두 남아 매우 멀다 |

현재 네 문제 중 완전 증명에 가깝다고 말할 수 있는 것은 없다. Goldbach의
조건부 상수 구조가 가장 명시적이지만, 필요한 점별 minor-arc 정리는 아직
새로운 핵심 정리다.

## 8. Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket133_quantifier_promotion_exact_reductions.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket133_quantifier_promotion_exact_reductions
```

Generated artifacts:

- `data/open-problem/ticket133-quantifier-promotion-exact-reductions.json`
- `data/open-problem/riemann/rh-ticket-133-gram-family-reduction.json`
- `data/open-problem/collatz/co-ticket-133-contracting-cylinder-exceptions.json`
- `data/open-problem/goldbach/gb-ticket-133-power-two-spike-no-go.json`
- `data/open-problem/twin-prime/tp-ticket-133-all-residue-composite-lifts.json`

## 9. Literature boundary / 문헌 경계

- A. Connes and C. Consani,
  [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368).
- M. Suzuki,
  [Weil's quadratic form via the screw function](https://arxiv.org/abs/2606.09096).
- D. Bernstein and J. Lagarias,
  [The 3x+1 Conjugacy Map](https://doi.org/10.4153/CJM-1996-060-x).
- A. Alsetri and X. Shao,
  [Density versions of the binary Goldbach problem](https://arxiv.org/abs/2405.18576).
- K. Ford and J. Maynard,
  [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).

Established coding, density, and sieve principles are not claimed as new. The
PrimeProject contribution is the exact four-track reduction/countermodel package,
its machine audit, and the explicit proof boundaries above.

All conjecture-resolution counters remain zero.
