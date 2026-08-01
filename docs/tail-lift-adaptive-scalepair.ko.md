# TICKET-174: tail 일정, 콜라츠 유일 zero-lift, 골드바흐 사후 선택, Haar scale 합산

## 주장 경계

TICKET-174는 TICKET-173이 남긴 네 OPEN 노드를 이어간다. 이번 결과는 네
개의 유한 또는 추상 정량 명제를 증명하지만, 리만 가설·콜라츠 추측·강한
골드바흐 추측·쌍둥이 소수 추측 중 어느 것도 증명하거나 반증하지 않는다.
네 상태는 모두 `open_not_proven`이며 기계 해결 수는 0이다.

이번 기여는 각 경로에서 피해야 할 수량자 오류를 하나씩 정확히 확정하고,
넓었던 다음 목표를 더 날카로운 단일 보조정리로 교체한 것이다.

| 문제 | TICKET-174 정확 결과 | 상태 | 폐기 경로 | 다음 단일 보조정리 |
|---|---|---|---|---|
| 리만 | 대각 tail 일정 전이 정리 | `open_not_proven` | 선형 또는 임계 `N log N` cutoff로 tail 종료 | `PoleNeutralQuadraticCutoffTruncatedCoreDefectConvergesToZero` |
| 콜라츠 | cylinder마다 zero-lift 자식은 정확히 하나 | `open_not_proven` | 양의 lift가 밀도 1이면 모든 ray가 해결됨 | `NoNonDescendingRayEventuallyFollowsUniqueZeroLiftChildren` |
| 골드바흐 | 적응형 양의 주파수 인증과 양성은 동치 | `open_not_proven` | 사후 선택한 양의 주파수를 비순환 major set으로 사용 | `FixedFareyMajorArcPositiveMassDominatesComplementSignedDeficitUniformly` |
| 쌍둥이 소수 | `log2 N` 최대 scale 합산 손실이 sharp | `open_not_proven` | 최대 pair 에너지만으로 scale 손실 제거 | `PrimePairEveryScalePairHaarEnergyPowerSavingUniformly` |

## 1. 리만: 올바른 대각 cutoff 일정

### 이번에 증명한 정확한 명제

`V_N`을 합집합이 조밀한 중첩 유한차원 공간이라고 하자. 절단 Hermitian
form이 `V_N` 위에서

```text
|q(v) - q_(N,T)(v)| <= B_N(T) ||v||^2,
lambda_min(q_(N,T)) >= -delta_(N,T)
```

를 만족한다고 하자. 하나의 대각 일정 `T_N`에 대해

```text
delta_(N,T_N) + B_N(T_N) -> 0
```

이면 `q`는 closure에서 비음이 아니다. 다음 명시적 인증 상계를 사용한다.

```text
U_N(T) = 2(2N+1)rho/pi^2 *
         [log(T)/(T-rho N) + log(T/(T-rho N))/(rho N)],
rho = 2 pi / log(c),  T > max(rho N,7)
```

일 때 충분한 일정 조건은

```text
T_N / (N log T_N) -> infinity
```

이다. 따라서 `T_N=N^2`은 이 인증 상계를 0으로 보내지만 `T_N=C N`과
`T_N=C N log N`은 이 상계만으로 tail closure를 인증하지 못한다.

### 증명

섭동 부등식에서

```text
q(v) >= -[delta_(N,T)+B_N(T)] ||v||^2
```

를 얻고, 선택한 대각 일정에 TICKET-173의 dense-core 정리를 적용한다.
충분조건 아래 `T-rho N`은 `T`와 점근적으로 같아지고 두 항은 각각
`O(N log T/T)`, `O(N/T)`이다. `T=N^2`에서는 둘 다 0으로 간다.
`T=C N`에서는 첫 항이 로그 크기로 증가하고 `T=C N log N`에서는 양의
상수 크기로 남는다.

### 재현 계산

`c=100`, `N=16,...,4096`에서:

| 일정 | 첫 budget | 마지막 budget | 점근 판정 |
|---|---:|---:|---|
| `8N` | 0.495118 | 0.942321 | 상계가 0으로 가지 않음 |
| `8N log N` | 0.187333 | 0.114591 | 양의 극한 상계 |
| `N^2` | 0.253306 | 0.002382 | 상계가 0으로 감 |
| `N^3` | 0.020861 | 0.000000856 | 상계가 0으로 감 |

이 수치는 fixed-`N` leading asymptotic이 아니라 Corollary 3.3의 명시적
상계를 계산한다. 상계가 0으로 가지 않는다고 exact tail도 0으로 가지 않는다는
뜻은 아니다. 또한 아직 없는 산술 결손 `delta_(N,T)`를 추정하지 않는다.

### 남은 간극

실제 pole-neutral 절단 Weil core가 quadratic cutoff에서 갖는 하한 결손이
0으로 간다는 인증이 없다. 이번 정리는 cutoff 비용을 닫았지만, 필요한
산술 부호를 만들지는 않았다.

## 2. 콜라츠: 예외 가지의 밀도는 0이지만 버릴 수 없다

### 이번에 증명한 정확한 명제

가속 홀수 Collatz valuation word `w`의 최소 양의 cylinder 대표를 `r_w`,
modulus를 `M_w`, endpoint를 `y=T^H(r_w)`라 하자. 모든 자식 `wa` 중
zero-lift 자식은 정확히 하나다.

```text
a* = v_2(3y+1),
r_(wa*) = r_w.
```

다른 모든 자식은 `r_(wa)=r_w+k_a M_w`, `k_a>0`이다. `a<=A`에서
zero-lift 자식 비율은 최대 `1/A`이지만, eventually stabilized natural ray는
그 유일한 자식을 영원히 선택한다.

### 증명

자식 cylinder는 부모 cylinder를 세분하므로 대표 차이는 `M_w`의 음이 아닌
배수다. 정수 `r_w`의 실제 다음 2-adic valuation은 하나뿐이므로 그 valuation
자식에서는 lift가 0이고 다른 자식에서는 양수다. 안정화 뒤에는 연속 대표가
같으므로 매 단계가 바로 이 유일한 zero-lift edge다.

### 재현 계산

- valuation `{1,2,3,4}`의 길이 6 이하 word `5,460`개를 검사했다.
- 각 부모에서 다음 valuation `1..32`의 정확 lift 식 오류는 0이었다.
- 표본 zero-lift 비율은 `A=4`에서 `0.234615`, `A=64`에서 정확히
  `1/64`였다.
- `27`, `871`, `6171`을 포함한 자연수 8개는 대표 안정화 뒤 모든 edge가
  zero-lift였다.

### no-go와 남은 간극

almost-all 논증은 많은 자식 중 하나를 버릴 수 있지만, 무한 경로는 매 깊이
그 하나만 선택할 수 있다. 따라서 로그 밀도 정리를 단순히 모든 입력에 대한
Collatz 결론으로 승격할 수 없다. 다음 보조정리는 prefixwise non-descending
조건 아래 이 예외 경로를 배제해야 한다. 이는 여전히 every-orbit 정리이며
여기서는 증명하지 못했다.

## 3. 골드바흐: 사후 선택한 major frequency는 순환 논증이다

### 이번에 증명한 정확한 명제

target-aligned Fourier 표현을

```text
R = a + P - N,
P = p_1 + ... + p_m,  p_i > 0
```

으로 쓰고 양의 항을 큰 순서로 정렬하자. `K*`를

```text
a + p_1 + ... + p_k > N
```

을 만족하는 최소 `k`라 하면, `K*`가 존재하는 것과 `R>0`은 동치다.

### 증명과 no-go

`K*`가 존재하면 전체 양의 질량은 선택 prefix보다 크므로 `R>0`이다.
반대로 `R>0`이면 모든 양의 항을 선택한 집합이 조건을 만족하므로 최소
prefix가 존재한다. 즉 전체 부호를 관찰한 뒤 양의 주파수를 충분히 고르는
방법은 목표인 양성을 다시 쓰는 것일 뿐 증명 bridge가 아니다.

유효한 대체 경로는 target sign을 보기 전에 유리근사로 정한 Farey major
arc다. 이 고정된 산술 영역의 양의 main term이 나머지 signed deficit을
target-uniform하게 이겨야 한다.

### 재현 계산

소수 support `64,128,256,512,1024`의 짝수 target `987`개를 zero-padding
후 Fourier 재구성했다. 선택 동치 오류는 0, 최대 재구성 오차는 `7.8e-12`
미만이었다. 이는 대수 항등식의 유한 확인이지 골드바흐 증명이 아니다.
support `1024`에서 중앙 target은 양의 항 16개를 요구했고, 가장 어려운
target은 1,328개를 요구했다. 이러한 target별 변동 자체가 사후 집합을
uniform major arc라고 부를 수 없는 이유다.

## 4. 쌍둥이 소수: 모든 scale pair를 합치는 정확한 비용

### 이번에 증명한 정확한 명제

`N=2^L`인 zero-margin `N x N` 행렬 `A`의 row scale `j`, column scale `k`
tensor-Haar 에너지를 `E_(j,k)`라 하자. 그러면

```text
||A||_op <= ||A||_F
          = sqrt(sum_(j,k) E_(j,k))
          <= L sqrt(max_(j,k) E_(j,k)).
```

`L=log2 N` 계수는 개선할 수 없는 sharp bound다.

### 증명과 sharp model

TICKET-173 Parseval 항등식과 scale pair가 `L^2`개라는 사실로 상계를 얻는다.
각 scale에서 정규 Haar wavelet 하나를 골라 모든 선택 row/column pair의
계수를 1로 둔다. Haar 좌표 행렬은 `u v^T`이고 두 벡터 norm은
`sqrt(L)`이므로 operator norm은 `L`이다. 각 scale-pair 에너지는 1이며,
constant 좌표를 쓰지 않아 물리 좌표 행렬의 모든 행·열 합은 0이다.

`N=4,...,128`에서 물리 좌표로 역변환한 모델은 operator norm
`2,3,4,5,6,7`로 상계를 모두 등호 포화했다. TICKET-161의 유한 prime-pair
행렬 4개도 같은 합산 상계를 만족했다.

### 남은 간극

두 scale index 전체에 uniform한 진짜 power saving이 있다면 logarithmic
loss를 흡수하고 전체 operator estimate를 닫을 수 있다. PrimeProject는 그
산술 상계를 아직 증명하지 못했다.

## 네 문제의 공통 결론

공통 장벽은 수량자를 보존하는 uniformity다.

1. 리만 cutoff는 총 결손이 0으로 가는 하나의 cofinal 일정이어야 한다.
2. 밀도 0인 콜라츠 가지도 모든 입력 명제에서는 버릴 수 없다.
3. 골드바흐 major arc는 관측된 부호와 독립적으로 먼저 정해야 한다.
4. 쌍둥이 소수 cancellation은 모든 row/column scale pair에 uniform해야 한다.

이는 탐색 공간을 실제로 좁힌 결과이지 난제 해결 주장이 아니다.

## 문헌 경계

- [Groskin, finite Guinand-Weil dictionary and archimedean tail order, arXiv:2607.02828](https://arxiv.org/abs/2607.02828)은 리만 일정 계산에 쓴 finite dictionary와 tail order를 제공하며 RH를 주장하지 않는다.
- [Tao, almost all Collatz orbits attain almost bounded values, arXiv:1909.03562](https://arxiv.org/abs/1909.03562)는 almost-all 로그 밀도 정리이며 여기서 필요한 every-ray 정리가 아니다.
- [Niu, parity vectors and paradoxical sequences, arXiv:2605.13886](https://arxiv.org/abs/2605.13886)은 최근 finite parity-vector 문맥이지 전역 Collatz 증명이 아니다.
- [Grimmelt와 Bhowmik, the exceptional set of the Goldbach problem, arXiv:2607.27282](https://arxiv.org/abs/2607.27282)는 major-arc·예외집합 문맥을 제공하지만 여기 명시한 binary uniform domination을 주지 않는다.
- [Ford와 Maynard, on the theory of prime producing sieves, arXiv:2407.14368](https://arxiv.org/abs/2407.14368)은 상당한 Type-II 정보가 왜 필요한지 설명한다. Haar 정리는 그 미해결 정보를 배치하는 좌표계일 뿐이다.

## 재현 방법

```powershell
D:\python\anaconda3\python.exe scripts\ticket174_tail_lift_adaptive_scalepair.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket174_tail_lift_adaptive_scalepair -v
```

정본 기계 판독 artifact는
`data/open-problem/ticket174-tail-lift-adaptive-scalepair.json`이다.
