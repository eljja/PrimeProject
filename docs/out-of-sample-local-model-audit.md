# TICKET-99: Out-of-sample and external local-model audit

## English

TICKET-99 replaces the leaked fitted projection rejected by TICKET-98 with two honest models.

First, a deterministic cross-fit writes `n=r+qW`, trains each residue mean only on even `q`, and evaluates only odd `q`. An evaluation index is retained only when its residue has at least `m in {1,2,4,8,16}` training observations. Training and evaluation indices are disjoint. Across three scales and 120 preregistered configurations, no norm-only Goldbach or Twin certificate survives.

Second, the external model

```text
A_W(n) = W/phi(W)  if gcd(n,W)=1,
         0          otherwise
```

uses no Lambda samples. CRT gives the exact local-main lower bound

```text
d_W = 2 product_{3<=p|W} (1 - 1/(p-1)^2),
M_G(N), M_2(x) >= d_W max(0, scale+1-W).
```

The finite audit verifies this bound for every stored checkpoint. Separate Cauchy norm bounds remain negative, so one-point local structure still does not prove either binary correlation.

The new proof target is explicit. Write `C=M+R`, choose `W(n)` as the largest primorial with `W(n)^2<=n`, and prove independently

```text
R_W(n) >= -K M_W(n) / log(n)
```

for all sufficiently large relevant `n`. Since the exact local main is linear and the proper-prime-power contamination budget is `o(n)`, this theorem would imply Goldbach after finite verification and would force infinitely many twin primes.

A double-precision discovery screen calibrates the common value `K=1.6` on `1,000<=n<=100,000`. It has zero validation failures through one million for both tracks, with direct replay at Goldbach extrema and boundaries. This is finite candidate discovery, not an asymptotic theorem.

This positioning matches the literature. The Green–Tao transference/W-trick framework removes small-prime local obstructions but explicitly excludes affine-degenerate binary cases such as Twin Prime and Goldbach: [Linear equations in primes](https://annals.math.princeton.edu/2010/171-3/p08). Ford and Maynard show in a general prime-producing sieve framework that substantial Type I/II information is needed for nontrivial lower bounds: [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).

## 한국어

TICKET-99는 TICKET-98에서 폐기한 동일 데이터 적합 projection을 두 가지 정직한 모델로 교체합니다.

교차적합 모델은 residue 평균을 짝수 period에서만 학습하고 홀수 period에서만 평가합니다. 각 residue에 사전 지정된 최소 학습 표본이 없으면 평가에서 제외합니다. 세 범위 120개 조합에서 Goldbach/Twin norm 인증은 모두 0건이었습니다. 빈 평가집합을 가장 좋은 결과로 선택하는 것도 금지했습니다.

외부 coprime 모델은 Lambda나 소수 관측값을 전혀 사용하지 않습니다. CRT로 국소 main term의 선형 하한을 정확히 증명할 수 있습니다. 따라서 남는 유일한 핵심은 signed residual입니다. `R >= -K M/log n`을 target correlation을 읽지 않고 Type II, dispersion 또는 더 높은 차수의 산술 정보로 증명하면 기존 contamination bridge와 결합해 두 난제로 이어집니다.

백만 범위의 수치 탐색에서는 `K=1.6` 후보가 calibration 이후 구간에서 반례 없이 유지됐습니다. 그러나 유한 FFT 화면은 증명이 아닙니다. 특히 `W(n)`이 제곱근 규모까지 성장하므로 현재의 one-point progression 정보나 일반 transference만으로 이 binary residual을 제어할 수 없습니다. RH와 Collatz에는 동일한 데이터 분리 원칙만 전이하며, 네 난제는 모두 미해결입니다.

## Reproduce / 재현

```text
D:\python\anaconda3\python.exe scripts\ticket99_out_of_sample_local_model_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket99_out_of_sample_local_model_audit
```
