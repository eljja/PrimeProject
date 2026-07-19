# TICKET-132: Admissibility, Dense-Null Codes, Hard Strata, and Local Parity

## 연구 상태 / Research status

**리만 가설, Collatz 추측, 강한 Goldbach 추측, Twin Prime 추측은 모두
미해결이다.** TICKET-132는 증명이나 실제 반례를 주장하지 않는다. 이번
단계는 TICKET-131에서 확인한 병목을 더 정확한 수학적 공간과 반례 구조로
바꾼다.

**RH, Collatz, strong Goldbach, and Twin Prime all remain open.** TICKET-132
claims neither a conjecture proof nor a conjecture counterexample. It corrects
the admissible RH core and proves exact boundary theorems showing why topology,
density, finite arithmetic stratification, and finite local sieve data cannot by
themselves discharge the remaining pointwise obligations.

Machine-readable record:
`data/open-problem/ticket132-admissibility-nullset-hard-stratum-local-parity.json`.

## 1. 결과 요약 / Executive result

| 문제 | TICKET-132의 정확한 결과 | 폐기하는 추론 | 다음 결정적 정리 |
|---|---|---|---|
| RH | 두 Weil 모멘트 제약을 보존하는 열거 가능 조밀 core 투영 | 무제약 유리 bump가 이미 허용함수라는 가정 | projected core 전체의 비음성 인증 |
| Collatz | 자연수 valuation code는 가산·조밀·비원자 측도 0이며 residue가 안정화 | finite-prefix 분리나 mass 0만으로 자연수 반례 배제 | 자연수 부분집합의 점별 Archimedean descent |
| Goldbach | `N=2^m`은 무한한 최소 특이급수 stratum | 유한 작은 소인수 층화만으로 모든 짝수 처리 | powers of two와 rough 층의 점별 `K=56` 잔차 |
| Twin Prime | 모든 유한 sieve 수준을 통과하지만 양쪽이 합성수인 무한 CRT 진행 | 고정 유한 local sieve 상태를 소수성 인증으로 승격 | unbounded Type II + parity-sensitive gap-2 하계 |

현재도 네 문제 중 증명에 가깝다고 말할 수 있는 문제는 없다. 다만 RH에서는
이전 core의 실제 허용조건 결함을 수리했고, 나머지 문제에서는 다음 연구가
반드시 pointwise 또는 unbounded 정보를 사용해야 함을 정확히 증명했다.

## 2. Riemann Hypothesis / 리만 가설

한 Weil 양성 공식에서 필요한 두 모멘트 조건을 additive log coordinate로
다음처럼 쓴다.

```text
L_+(f) = integral f(x)e^(x/2) dx = 0,
L_-(f) = integral f(x)e^(-x/2) dx = 0.
```

TICKET-129의 유리 bump core는 전체 `C_c^infinity(R)`에 조밀하지만, 일반적인
core 원소는 이 두 등식을 정확히 만족하지 않는다. 조밀성만으로 이 결함이
자동으로 사라지지 않는다.

### Theorem RH-132: `ConstraintPreservingEnumerableWeilCoreProjection`

TICKET-129의 열거 가능한 유리 bump core를 연속적이고 효과적으로

```text
K = ker(L_+) intersect ker(L_-)
```

위로 투영할 수 있다. 투영된 집합은 가산이고 `K` 안에서 조밀하다.

### Proof / 증명

표준 bump `b`는 짝함수다. 다음 두 anchor를 택한다.

```text
psi_0(x)=b(x),
psi_1(x)=b(x-1).
```

`I=integral b(x)e^(x/2)dx`라 하면 `I>0`이고 짝함수성으로 두 모멘트의
정규화 행렬은

```text
A/I = [[1, e^(1/2)],
       [1, e^(-1/2)]].
```

그 행렬식은

```text
e^(-1/2)-e^(1/2) < 0
```

이므로 역행렬이 존재한다. 이제

```text
P(f)=f-(psi_0,psi_1) A^(-1) (L_+(f),L_-(f))^T
```

로 두면 `L_+(P(f))=L_-(P(f))=0`이다. `P`는 연속이고 `K` 위에서 항등이다.
따라서 조밀한 core의 상 `P(C_Q)`는 `K`에 조밀하다. 모멘트와 고정된
2x2 역행렬은 계산 가능하므로 각 projected element도 효과적으로 기술된다.
`QED`

네 개의 독립 모멘트 벡터를 사용한 수치 역검산에서 최대 투영 잔차는
`2.220446049250313e-16`이었다. 이는 증명의 근거가 아니라 구현 검산이다.

```text
Keep / 유지:
countable effective core + strict-negative interval semidecision

Discard / 폐기:
unconstrained rational bumps already satisfy exact Weil admissibility

Next / 다음:
NonnegativeProjectedWeilCoreCertificate
```

중요한 구현 경계가 하나 남는다. TICKET-130 계산기는 유리 계수의 유한 tuple을
입력으로 가정했다. 투영 뒤 계수는 일반적으로 계산 가능한 실수다. 따라서
외향 구간 계산기를 이 computable-coefficient 표현으로 확장하고, 하나의
출판된 Weil 정규화와 부호를 고정한 뒤 비음성 또는 엄격한 음수 구간을
인증해야 한다. RH는 미해결이다.

## 3. Collatz Conjecture / 콜라츠 추측

가속 홀수 사상의 valuation code 공간을

```text
Omega = {1,2,3,...}^N
```

와 product topology로 둔다. 기본 열린집합은 valuation의 유한 prefix 하나를
고정한 cylinder다.

### Theorem CO-132: `NaturalCollatzCodesAreCountableDenseAndNull`

양의 홀수 자연수에서 생성되는 code 집합 `N_code`는 다음을 동시에 만족한다.

1. `N_code`는 가산이다.
2. `N_code`는 `Omega`에서 조밀하다.
3. 모든 비원자 Borel 확률측도에서 `N_code`의 측도는 0이다.
4. 각 natural code의 canonical start residue는 TICKET-131의 의미에서 결국
   그 시작 자연수로 안정화한다.

### Proof / 증명

양의 홀수 집합이 가산이므로 그 code의 상도 가산이다. 임의의 유한 valuation
word를 고정하자. 정확한 cylinder 공식은 한 홀수 residue `r modulo M`을 주며
모든

```text
r, r+M, r+2M, ...
```

이 그 prefix를 실제로 재생한다. 따라서 모든 기본 열린집합에 자연수 code가
무한히 많고 `N_code`는 조밀하다. 비원자 측도에서 singleton의 측도는 0이므로
가산합인 `N_code`도 측도 0이다. 마지막으로 TICKET-131의 필요충분조건에 따라
고정 자연수의 중첩 residue는 modulus가 시작값보다 커진 뒤 그 자연수로
고정된다. `QED`

`a_i in {1,2,3,4}`, 깊이 1부터 4까지의 340개 word에서 각 cylinder의 앞
세 자연수, 총 1,020개를 다시 재생했고 불일치는 0개였다.

이 결과는 중요한 역설을 정확히 분리한다. 자연수 code는 모든 유한 prefix
근처에 존재할 만큼 조밀하지만, 확률적으로는 측도 0이다. 따라서 다음 두
추론은 모두 불충분하다.

```text
finite prefix excludes a ghost  => no natural counterexample
obstruction mass tends to zero  => no natural counterexample
```

```text
Next / 다음:
PointwiseArchimedeanDescentOnDenseNullNaturalCodes
```

새 정리는 실제 자연수 크기와 정확한 residue를 결합해 각 `n>1`에 유한 strict
descent를 주어야 한다. 위상 또는 확률만으로는 닫히지 않는다.

## 4. Strong Goldbach Conjecture / 강한 골드바흐 추측

정규화한 binary singular-series 산술 multiplier는

```text
G(N) = product_(p|N, p>2) (p-1)/(p-2)
```

이다.

### Theorem GB-132: `PowersOfTwoRemainTheUniformGoldbachHardStratum`

모든 `m>=1`에 대해 `N=2^m`이면 `G(N)=1`이다. 따라서 작은 홀수 소인수로
주항을 증폭하는 어떤 유한 층화도 임의로 큰 모든 짝수를 덮지 못한다.
무한한 powers-of-two 계열은 항상 최소 주항 stratum으로 남는다.

### Proof / 증명

`2^m`을 나누는 홀수 소수가 없으므로 위 곱은 empty product이고 값은 1이다.
`2^m`은 무한히 커진다. 따라서 유한한 홀수 소인수 목록에서 얻은 모든 증폭
stratum 밖에 임의로 큰 짝수가 존재한다. `QED`

TICKET-128부터 TICKET-131까지 고정한 정확한 endpoint 상수를 최소 multiplier
`1`에 대입하면 다음 lower-certificate margin을 얻는다.

```text
K=56:  23019645297 / 2140000000000 > 0
K=57: -26980354703 / 2140000000000 < 0
```

두 번째 음수는 `K=57` 정리가 불가능하다는 뜻이 아니다. 현재 major lower
floor만 사용하는 인증서가 최소 stratum에서 닫히지 않는다는 뜻이다.

TICKET-131의 `p<=103` 층화는 약 76.4%의 산술형에서 목표를 `K=57`로
완화하므로 유지한다. 다만 Goldbach 전체를 위해서는 별도로 다음이 필요하다.

```text
Next / 다음:
PointwiseBinaryGoldbachResidualK56OnPowersOfTwoAndRoughStrata
```

즉, `2^m`과 작은 홀수 소인수가 없는 rough 짝수에서 signed binary minor-arc
잔차를 점별로 제어해야 한다. 평균 또는 밀도 정리는 이를 대신하지 못한다.

## 5. Twin Prime Conjecture / 쌍둥이 소수 추측

### Theorem TP-132: `FiniteLocalSieveDataCannotCertifyTwinPrimality`

모든 유한 sieve level `z`에 대해 다음을 만족하는 홀수 `n`의 무한 산술진행이
존재한다.

```text
gcd(n(n+2), product_(p<=z) p)=1,
n is composite,
n+2 is composite.
```

### Proof / 증명

각 `p<=z`에서 `0,-2 modulo p`를 피하는 residue를 고른다. 구체적으로

```text
a_2=1, a_3=2, a_p=1 for p>=5
```

이면 된다. CRT로 이 조건을 하나의 `a modulo P`로 합친다. 서로 다른 두 소수
`q,r>z`를 고르고

```text
n == 0  (mod q),
n == -2 (mod r)
```

를 추가한다. 다시 CRT를 적용하면 `modulo Pqr`의 한 산술진행을 얻는다.
충분히 큰 항에서는 `q`가 `n`의 proper divisor이고 `r`이 `n+2`의 proper
divisor다. 동시에 모든 `p<=z`에 대한 local-clean 조건은 보존된다. `QED`

기계 감사는 `z=5,11,29,97`에서 12개의 명시적 composite-composite pair를
검산했다. 예를 들어 `z=97`에서 첫 시작값은

```text
26432568183980720233652731751776139423861
```

이고 `101|n`, `103|(n+2)`이면서 97 이하의 어떤 소수도 두 수를 나누지 않는다.

이 정리는 Twin Prime의 반례가 아니다. fixed finite local signature가 소수성을
인증할 수 없다는 정확한 countermodel이다. 따라서 다음 정리는 단순한 local
sieve 생존 질량을 넘어야 한다.

```text
Next / 다음:
UnboundedTypeIIParitySensitiveExactGapCertificate
```

Ford-Maynard형 Type I/II 정보 중 실제 unbounded Type II 범위가 CRT 합성수
진행과 진짜 prime pair를 분리하고, 그 하계가 exact gap 2로 전달됨을 증명해야
한다.

## 6. 증명 가능성 재평가 / Updated proof viability

### 무엇이 실제로 개선됐는가

1. RH의 열거 core가 이제 실제 두 모멘트 제약을 정확히 만족한다.
2. Collatz에서 자연수 경로의 topology와 measure가 완전히 분리됐다.
3. Goldbach 산술 층화가 해결하지 못하는 무한 최악 계열이 명시됐다.
4. Twin Prime에서 finite-local sieve 인증을 무너뜨리는 무한 arithmetic
   countermodel이 생겼다.

### 무엇이 아직 없는가

1. projected Weil core의 전칭 비음성 또는 엄격한 음수 interval;
2. 모든 자연수 Collatz code의 유한 strict descent;
3. powers of two/rough even integers의 점별 binary residual theorem;
4. unbounded Type II 정보를 exact gap-2 양의 하계로 바꾸는 parity bridge.

따라서 증명 가능성은 “연구를 계속할 수 있다”는 의미에서는 남아 있지만,
현재 결과가 완전 증명에 가까워졌다고 평가할 근거는 없다. 이번 진전은 잘못된
공간이나 약한 정보로 무한 결론을 주장할 가능성을 줄이고, 다음 정리가 실제로
무엇을 포함해야 하는지를 더 정확하게 만든 것이다.

## 7. Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket132_admissibility_nullset_hard_stratum_local_parity.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket132_admissibility_nullset_hard_stratum_local_parity
```

Generated artifacts:

- `data/open-problem/ticket132-admissibility-nullset-hard-stratum-local-parity.json`
- `data/open-problem/riemann/rh-ticket-132-constrained-core.json`
- `data/open-problem/collatz/co-ticket-132-dense-null-natural-codes.json`
- `data/open-problem/goldbach/gb-ticket-132-power-two-hard-stratum.json`
- `data/open-problem/twin-prime/tp-ticket-132-local-sieve-crt.json`

## 8. Literature boundary / 문헌 경계

- A. Connes and C. Consani,
  [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368), for the two
  multiplicative moment conditions in a Weil-positivity formulation.
- M. Suzuki,
  [Weil's quadratic form via the screw function](https://arxiv.org/abs/2606.09096),
  for a current continuous-function and operator-limit framework. No RH proof is
  imported.
- O. Kramer,
  [Adaptive Search in Collatz Exponent-Code Space](https://arxiv.org/abs/2607.10041),
  for current exponent-code diagnostics explicitly separated from verification.
- A. Alsetri and X. Shao,
  [Density versions of the binary Goldbach problem](https://arxiv.org/abs/2405.18576),
  for the distinction between density conclusions and an all-even pointwise theorem.
- K. Ford and J. Maynard,
  [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368),
  for the necessity of substantial Type II information in prime lower bounds.

All conjecture-resolution counters remain zero.
