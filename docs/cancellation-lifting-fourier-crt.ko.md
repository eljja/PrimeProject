# TICKET-239: 상쇄, lifting, Fourier 반사, CRT parity 감사

## 주장 경계

TICKET-239는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측을 **증명하거나 반증하지 않았습니다**. 이번 결과는 네 개의 정확한
부분정리 또는 no-go 정리를 증명하고, 유한 계산은 별도의 bounded evidence로
기록하며, 각 문제에 다음 단일 보조정리 하나를 지정합니다.

기계 판독 감사 파일은
`data/open-problem/ticket239-cancellation-lifting-fourier-crt.json`입니다.

재현 명령:

```powershell
python scripts/ticket239_cancellation_lifting_fourier_crt.py
python -m unittest tests.test_ticket239_cancellation_lifting_fourier_crt -v
```

## 결과 요약

| 문제 | TICKET-239의 정확한 결과 | 폐기한 경로 | 상태 |
|---|---|---|---|
| 리만 가설 | 거듭제곱 감쇠 Schur 임계값과 비가합적 양의 Gram 족 | 절대 교차 행합 수렴이 양성의 필요조건이라는 주장 | `open_not_proven` |
| 콜라츠 | 국소 lifting defect 이분법과 finite palette 판정식 | mod `q` 일치가 valuation 깊이도 자동 제어한다는 주장 | `open_not_proven` |
| 골드바흐 | 정확한 반사 Fourier 항등식과 동일 크기 L2 반례족 | 창의 소수 개수와 Parseval 에너지만으로 양성을 얻는 경로 | `open_not_proven` |
| 쌍둥이 소수 | 균등 CRT Gram 항등행렬과 무한 합성수 쌍 등차수열 | 최대 국소 유효랭크가 쌍둥이 소수 질량을 뜻한다는 경로 | `open_not_proven` |

## 1. 리만 가설 트랙

### 이번에 증명한 명제

대각 block이 항등인 Hermitian shell 행렬 `H_J`가

```text
||K_ij||_op <= C |i-j|^(-alpha)
```

를 만족한다고 하겠습니다. `alpha>1`이고 `2 C zeta(alpha)<1`이면 모든
`J`에 대해

```text
H_J >= (1-2 C zeta(alpha)) I
```

가 성립합니다.

그러나 절대가합성은 필요조건이 아닙니다. `0<C<1`, `0<alpha<=1`일 때

```text
G_J=(1-C)I+C[(1+|i-j|)^(-alpha)]
```

는 정규화 Gram 행렬이고 `G_J >= (1-C)I`입니다. 반면 최대 절대 교차
행합은 `J`와 함께 발산합니다.

### 논증

첫 결과는 block Schur 추정과 `sum d^(-alpha)=zeta(alpha)`에서 나옵니다.
두 번째 결과에는

```text
(n+1)^(-alpha)
  = Gamma(alpha)^(-1) integral_0^1 t^n(-log t)^(alpha-1)dt
```

를 사용합니다. `[t^|i-j|]`는 양의 준정부호 행렬이므로 이들의 양의
적분 혼합도 양의 준정부호입니다. `(1-C)I`가 균일한 양의 하한을
보장하지만, `alpha<=1`의 조화급수형 행합은 발산합니다.

### 폐기 범위와 남은 간극

따라서 TICKET-238의 절대 행합 검사는 충분조건이지만 필요조건은
아닙니다. 행합 검사가 실패했다는 사실을 Weil 양성의 반증처럼 사용할 수
없습니다. 다만 이 행렬은 추상 Gram 족이며 실제 Guinand-Weil 산술
shell의 상쇄를 증명하지 않습니다.

**다음 보조정리:**
`ArithmeticWeilCrossBlockCotlarSteinCancellationBoundOnCofinalLogarithmicShells`.

## 2. 콜라츠 추측 트랙

### 이번에 증명한 명제

홀수 소수 `q>3`에 대해

```text
ell_q = lcm(ord_q(32/27), ord_q(2/3)),
a_q   = v_q(32^ell_q-27^ell_q),
c_q   = v_q(2^ell_q-3^ell_q)
```

로 둡니다. 모든 `n>=1`에 대해 `q`가

```text
v_q(D_(ell_q n)) > v_q(B_(ell_q n))
```

을 만족하는 valuation 증인일 필요충분조건은 `a_q>c_q`입니다.
`a_q<=c_q`이면 `ell_q`의 모든 배수에서 이 소수는 증인으로 사용할 수
없습니다. 따라서 finite palette 안의 모든 국소 defect
`delta_q=a_q-c_q`가 0 이하이면 하나의 공통 주기로 전체 palette를 동시에
무력화할 수 있습니다.

### 논증

LTE를 적용하면 두 차이는 각각 `a_q+v_q(n)`, `c_q+v_q(n)`의 valuation을
가집니다. 또한 `27^k`로 나누면

```text
B_k=((32/27)^k-1)-2((2/3)^k-1)
```

입니다. 서로 다른 valuation의 차는 작은 valuation을 그대로 가지며,
같으면 cancellation으로 valuation이 낮아질 수 없습니다. 이것이 정확한
이분법을 줍니다.

### 유한 계산과 한계

`5<=q<=200,000`의 홀수 소수 17,982개를 전부 검사했으며 양의 lifting
defect는 발견되지 않았습니다. 이것은 전 범위의 증명이 아닙니다. mod `q`
수준에서 양쪽이 나누어진다는 TICKET-237 결과만으로 valuation 크기까지
결론 내리는 경로는 폐기해야 합니다.

**다음 보조정리:** `RunBlockLocalLiftingDefectNonpositiveForEveryOddPrime`.

이 보조정리가 증명되어도 run-block palette 문제만 닫힙니다. 일반 주기
necklace와 비주기 궤도의 하강은 별도의 문제입니다.

## 3. 강한 골드바흐 추측 트랙

### 이번에 증명한 명제

`A subset {0,...,h}`, `M>2h`, `P_A(z)=sum_(a in A)z^a`라 하고

```text
R_A(h)=#{(a,b) in A^2:a+b=h}
```

라 하면, `omega`가 `M`차 단위근일 때

```text
R_A(h)=(1/M)sum_(j=0)^(M-1)P_A(omega^j)^2 omega^(-jh)
```

입니다. DC 항은 `|A|^2/M`입니다. Parseval 에너지는 항상
`M|A|`이지만, `2|A|-2<h`이면 `{0,...,|A|-1}`은 같은 원소 수와 같은
Parseval 에너지를 가지면서 `R_A(h)=0`입니다.

### 의미와 계산 한계

따라서 mesoscopic 창의 소수 개수와 전역 L2 에너지만으로 반사 계수의
양성을 증명할 수 없습니다. `X=10^3,...,10^6`과 세 buffer 배율에서
정확한 DC 항과 부호 있는 비영 위상항을 12개 행으로 계산했습니다. 이
유한 행들은 충분히 큰 모든 짝수에 대한 양성을 증명하지 않으며 골드바흐
반례도 아닙니다.

**다음 보조정리:**
`MesoscopicPrimeWindowSignedFourierRemainderExceedsNegativeDCWithUniformSlack`.

## 4. 쌍둥이 소수 추측 트랙

### 이번에 증명한 명제

홀수 소수의 유한 집합 `Q`와 `W=product_(q in Q)q`를 잡고 `r mod W`를
균등하게 선택합니다. 다음 국소 admissibility 지표를 중심화·분산
정규화합니다.

```text
1_{r is not congruent to 0 or -2 modulo q}
```

CRT 독립성 때문에 Gram 행렬은 항등행렬이고 유효랭크는 `|Q|`입니다.
그러나 모든 admissible residue class에는 `n`과 `n+2`가 모두 합성수인
원소가 무한히 많습니다.

### 논증

`Q` 밖의 서로 다른 소수 `ell_1,ell_2`를 골라

```text
r+kW     = 0 mod ell_1,
r+kW + 2 = 0 mod ell_2
```

를 동시에 요구합니다. `W`는 두 소수에 대해 가역이고 CRT가 `k`의 한
등차수열을 제공합니다. 충분히 큰 원소에서는 두 나눗셈이 모두 진정한
합성수 인수를 줍니다.

즉, 가장 좋은 균등 CRT 유효랭크조차 실제 prime-weighted 쌍둥이 소수
질량을 보장하지 않습니다. 이것이 sieve parity 문제와 연결되는 정확한
no-go입니다.

**다음 보조정리:**
`ParitySensitiveTransferFromPrimeWeightedCRTOrthogonalityToPositiveTwinPrincipalMass`.

## 네 트랙의 공통 결론

TICKET-239가 폐기한 지름길은 다음 네 가지입니다.

1. 절대가합성 실패를 양성 실패로 해석하는 것,
2. mod `q` 일치를 valuation 제어로 해석하는 것,
3. 밀도와 L2 에너지를 반사 양성으로 해석하는 것,
4. 균등 CRT 랭크를 실제 소수쌍 질량으로 해석하는 것입니다.

네 문제 모두에서 남은 핵심은 통제된 국소 모델에서 실제 무한 산술
대상으로 이동할 때 부호 또는 parity 정보를 보존하는 **산술적 transfer
정리**입니다.

## 기준 1차 문헌

- [Clay Mathematics Institute: 리만 가설 공식 설명](https://www.claymath.org/millennium/riemann-hypothesis/)
- [Tao, Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)
- [Helfgott, The ternary Goldbach problem](https://arxiv.org/abs/1501.05438)
- [Maynard, Small gaps between primes](https://arxiv.org/abs/1311.4600)

이 문헌들은 현재 인정된 연구 경계를 확인하기 위한 기준입니다. 위의 네
새 보조정리를 이 문헌들이 이미 증명했다고 주장하지 않습니다.
