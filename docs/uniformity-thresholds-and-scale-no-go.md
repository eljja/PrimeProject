# TICKET-134: Uniformity Thresholds and Scale-Dependent No-Go Theorems

## 연구 상태 / Research status

**리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측은 모두
미해결이다.** TICKET-134는 어느 가설의 완전한 증명이나 반례도 주장하지
않는다. 이번 단계는 TICKET-133이 남긴 네 전역 병목에서 계산이 실제 증명으로
승격될 수 있는 조건과, 승격이 불가능한 정확한 규모 경계를 증명한다.

**RH, Collatz, strong Goldbach, and Twin Prime all remain open.** TICKET-134
proves four exact interval, no-go, or scale-threshold theorems. None is a proof
or counterexample to a target conjecture.

Machine-readable record:
`data/open-problem/ticket134-uniformity-thresholds-and-scale-no-go.json`.

## 1. 결과 요약 / Executive result

| 문제 | TICKET-134의 정확한 결과 | 폐기되는 경로 | 다음 결정적 정리 |
|---|---|---|---|
| RH | strict finite Gram sign의 rational interval semi-decision | 부동소수점 고윳값 또는 유한 Gram prefix의 전칭 승격 | uniform projected Weil Gram tail certificate |
| Collatz | 모든 finite/bounded-depth contracting-prefix cover의 불가능성 | 더 큰 유한 tree가 전체 자연수를 덮을 것이라는 가정 | well-founded unbounded contracting-prefix cover |
| Goldbach | power-of-two spike 검출의 정확한 logarithmic moment threshold | `p(X)=o(log X)` 모멘트의 점별 승격 | log-scale moment 또는 maximal `K=56` residual |
| Twin Prime | 성장하는 primorial 정보에도 적용되는 `n<2Wqr` 합성수쌍 lift | `z(X)<=(1-epsilon)log X` residue-only 분류 | near-full-scale parity-sensitive separation |

네 결과는 탐색 범위를 늘린 유한 실험이 아니다. 핵심 명제는 임의의 차원,
깊이, horizon 또는 sieve scale에 대한 기호적 정리이며, 생성기의 유한 행은
식과 구현의 일치만 검산한다.

## 2. Riemann Hypothesis / 리만 가설

TICKET-133은 projected core의 전칭 Weil 양성을 모든 유한 rational Gram
부등식의 무한 family로 환원했다. 이번 단계는 한 유한 Gram 행렬의 부호를
근사 계산이 아니라 엄밀한 구간 인증서로 판정하는 조건을 닫는다.

### Theorem RH-134: `RationalCongruenceIntervalDichotomy`

실대칭 행렬 `G`의 각 성분에 대해 수렴하는 유리수 구간을 계산할 수 있다고
하자.

1. `G`가 positive definite이면, 어떤 유리수 가역행렬 `C`와 유한 정밀도에서
   `C^T[G]C`의 모든 Gershgorin lower margin이 양수가 된다.
2. `G`에 음의 방향이 있으면, 어떤 유리수 벡터 `q`와 유한 정밀도에서
   `upper(q^T[G]q)<0`이 된다.
3. `G`가 singular positive semidefinite이면 모든 entrywise 근방에 positive
   definite 행렬과 indefinite 행렬이 함께 존재한다. 따라서 strict
   certificate의 어느 쪽도 반드시 종료한다고 할 수 없다.

### Proof / 증명

`G>0`이면 실수 행렬 `G^(-1/2)`에 의한 congruence가 `G`를 항등행렬로
보낸다. 유리수 행렬의 조밀성으로 `G^(-1/2)`에 충분히 가까운 유리수 가역
`C`를 택하면 `C^TGC`는 양의 대각을 가진 strict diagonal-dominant 행렬이다.
이 strict 조건은 충분히 작은 성분 구간에서도 보존된다. 각 행의 lower
margin이 양수이면

```text
2|x_i x_j| <= x_i^2 + x_j^2
```

에 의해 구간 안의 모든 대칭행렬이 positive definite이다.

`q^TGq<0`인 실수 `q`가 있으면 음의 방향은 열린 조건이다. 유리수 벡터의
조밀성으로 같은 부호를 갖는 유리수 `q`를 택할 수 있고, 성분 구간이 수렴하면
`q^T[G]q`의 exact upper enclosure도 결국 음수가 된다.

마지막으로 singular PSD 행렬의 kernel vector를 `u`라 하자. 임의의 작은
`epsilon>0`에 대해 `G+epsilon I`는 positive definite이고
`G-epsilon uu^T`는 `u` 방향에서 음수다. `QED`

기계 감사는 직접 Gershgorin에서 실패하는

```text
G = [[2,3],[3,5]]
```

를 유리수 preconditioner `[[1,-3/2],[0,1]]`로 인증했다. 변환 후 exact lower
margin은 `3993/2000`, `393/800`이다. Indefinite 예제
`[[1,2],[2,1]]`의 `q=(1,-1)` interval upper는 `-49/25`다. 감사 실패는 0이다.

이 정리는 **유한 행렬의 strict sign만** semi-decide한다. 실제 projected Weil
Gram 성분, singular boundary, 모든 차원을 동시에 다루는 tail은 열려 있다.

```text
Next: UniformProjectedWeilGramTailCertificate
```

## 3. Collatz Conjecture / 콜라츠 추측

양의 홀수의 accelerated map을 `A`라 하자. TICKET-133은 contracting word
하나마다 비하강 예외가 유한함을 증명했다. 그러나 유한 개 word로 모든
자연수를 덮을 수 있는지는 별개의 문제였다.

### Theorem CO-134: `NoBoundedDepthContractingPrefixCover`

Contracting valuation word의 어떤 유한 family도 모든 양의 홀수를 덮지 못한다.
더 강하게, 허용 prefix 길이가 `K` 이하인 어떤 contracting cover도 실패한다.

### Proof / 증명

길이 `j`인 all-one valuation word `1^j`의 exact natural cylinder는

```text
n == -1 (mod 2^(j+1))
```

이다. 귀납으로

```text
A^j(n) = (3^j n + 3^j - 2^j) / 2^j,
A^j(n)-n = (3^j-2^j)(n+1)/2^j > 0.
```

따라서 `1^j`의 모든 prefix는 expanding이다. 유한 cover의 최대 길이를 `K`라
하고 `n=-1 mod 2^(K+1)`인 양의 정수를 택하면, 이 수의 길이 `K` 이하 prefix는
모두 all-one word이므로 어떤 contracting cover 원소와도 일치할 수 없다.
그런 `n`은 무한히 많다. `QED`

깊이 1부터 24까지 exact cylinder, affine iterate, strict growth를 재생했고
실패는 0이었다. 그러나 이 유한 재생은 정리의 근거가 아니라 기호식의
구현 검산이다.

이 정리는 Collatz 반례를 만들지 않는다. 각 유한 `K`마다 다른 자연수
cylinder를 구성할 뿐, 하나의 자연수 궤도가 영원히 all-one이라는 뜻이 아니다.
결론은 증명용 cover가 반드시 무한하고 unbounded depth여야 한다는 것이다.

```text
Discard: finite or globally bounded-depth cover
Next: WellFoundedUnboundedContractingPrefixCover
```

## 4. Strong Goldbach Conjecture / 강한 골드바흐 추측

`N_X`를 `X` 이하의 짝수 입력 개수, `J_X`를 그중 2의 거듭제곱 개수라 하자.
TICKET-133의 고정 spike 크기를 `A=2m_56`이라 둔다.

### Theorem GB-134: `PowerOfTwoMomentDetectionThreshold`

Power-of-two support에서만 절댓값이 `A`이고 나머지는 0인 sequence의 normalized
`L^(p_X)` norm은 정확히

```text
A (J_X/N_X)^(1/p_X)
= A exp(-log(N_X/J_X)/p_X)
```

이다. 따라서 다음 세 regime이 정확히 나뉜다.

1. `p_X=o(log(N_X/J_X))`이면 norm은 0으로 간다.
2. `p_X/log(N_X/J_X)->c`, `0<c<infinity`이면 norm은 `A exp(-1/c)`로 간다.
3. 그 비가 무한대로 가면 norm은 `A`로 간다.

### Proof / 증명

`N_X`개 입력 중 정확히 `J_X`개가 크기 `A`이므로 `p_X`차 평균은
`A^p_X J_X/N_X`이다. `p_X`제곱근을 취하고 로그를 적용하면 세 극한이 바로
나온다. `QED`

`J_X=Theta(log X)`, `N_X=Theta(X)`이므로 sublogarithmic moment는 모든 고정
크기의 power-of-two spike를 놓친다. TICKET-133의 “모든 고정 finite `p`가
부족하다”는 결과가 이제 정확한 검출 임계값으로 강화되었다.

이 sequence는 실제 Goldbach residual이 아니다. 따라서 다음 단계는 실제
residual에 대해 `p`가 `log X`에 비례하는 정량 estimate를 증명하거나 직접
maximal bound를 증명하는 것이다.

```text
Discard: p(X)=o(log X) moment control => pointwise positivity
Next: LogScaleMomentOrMaximalGoldbachResidualK56
```

## 5. Twin Prime Conjecture / 쌍둥이 소수 추측

TICKET-133은 고정 primorial `W`의 모든 admissible class에 합성수쌍 lift가
있음을 보였다. 이번에는 lift가 나타나는 크기를 정량화하여 `W`가 scale과
함께 성장하는 경우까지 확장한다.

### Theorem TP-134: `ScaleDependentPrimorialCompositeLiftBound`

유한 primorial `W`, 임의의 admissible `a mod W`, `W` 밖의 서로 다른 소수
`q,r`에 대해

```text
n == a  (mod W),
q | n,
r | n+2,
n < 2Wqr
```

를 만족하는 composite-composite pair가 존재한다.

### Proof / 증명

CRT가 `[0,Wqr)` 안의 유일한 base `x`를 준다. `q`와 `r`가 아직 proper
divisor가 아니면 `x+Wqr`를 택한다. 결과는 `2Wqr`보다 작고 전체 `W` residue를
보존하며 두 항은 모두 합성수다. `QED`

`W(z)`를 `z` 이하 primorial이라 하면 prime number theorem으로

```text
log W(z) = theta(z) = z + o(z).
```

다음 두 소수 `q(z),r(z)`의 기여는 로그 규모에서 `O(log z)`다. 따라서 고정
`epsilon>0`에 대해

```text
z(X) <= (1-epsilon) log X
```

이면 충분히 큰 `X`에서 `2W(z)q(z)r(z)<X`다. 즉 이 범위의 성장하는
primorial residue만 보는 classifier도 자기 관찰 구간 안에서 합성수쌍을
소수쌍과 분리하지 못한다.

`z=5,7,11,13,17`에서 admissible class `23,913`개 전부를 감사했고 모든
witness가 exact bound를 만족했다. 실패는 0이다.

이는 Twin Prime 반례가 아니다. `z`가 거의 full scale로 성장하거나 residue로
factor하지 않는 Type II 정보는 배제하지 않는다.

```text
Discard: residue-only z(X)<=(1-epsilon)log X classifier
Next: NearFullScaleParitySensitiveTwinSeparation
```

## 6. 교차 문제 결론 / Cross-problem conclusion

| 문제 | 이번에 확인된 필수 규모 |
|---|---|
| RH | strict rational interval certificate + 모든 차원의 uniform tail |
| Collatz | 무한하며 unbounded-depth인 well-founded cover |
| Goldbach | `log(X/log X)` 차수의 moment 또는 `L-infinity` control |
| Twin Prime | sublog primorial residue를 넘는 near-full-scale/Type II 정보 |

공통 결론은 “계산을 더 한다”가 아니다. strict margin이 있는 유한 문제는
구간 인증으로 닫을 수 있지만, 난제의 전칭 양화사는 dimension, depth, moment,
sieve scale에 대한 별도의 uniform theorem을 요구한다.

## 7. 증명 가능성 평가 / Proof viability

| 문제 | 실제 개선 | 완전 증명과의 거리 |
|---|---|---|
| RH | 부동소수점 Gram 검사를 rigorous semi-decision으로 교체 | 실제 Weil entry와 uniform tail이 없어 멀다 |
| Collatz | 유한 tree 완성 전략을 완전히 폐기 | unbounded well-founded cover가 없어 멀다 |
| Goldbach | 필요한 moment 차수의 정확한 임계값 도출 | 실제 residual의 log-scale estimate가 없어 멀다 |
| Twin Prime | fixed modulus no-go를 성장하는 `z(X)`로 확장 | parity-sensitive exact-gap lower bound가 없어 매우 멀다 |

현재 완전 증명에 가깝다고 평가할 문제는 없다. 이번 성과는 해결 가능성을
과장하는 대신, 다음 시도가 반드시 넘어야 할 정량 경계를 좁힌 것이다.

## 8. Reproduction / 재현

```powershell
D:\python\anaconda3\python.exe scripts\ticket134_uniformity_thresholds_and_scale_no_go.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket134_uniformity_thresholds_and_scale_no_go
```

Generated artifacts:

- `data/open-problem/ticket134-uniformity-thresholds-and-scale-no-go.json`
- `data/open-problem/riemann/rh-ticket-134-interval-dichotomy.json`
- `data/open-problem/collatz/co-ticket-134-bounded-depth-cover-no-go.json`
- `data/open-problem/goldbach/gb-ticket-134-log-moment-threshold.json`
- `data/open-problem/twin-prime/tp-ticket-134-growing-primorial-lifts.json`

## 9. Literature boundary / 문헌 경계

- A. Connes and C. Consani,
  [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368).
- M. Suzuki,
  [Weil's quadratic form via the screw function](https://arxiv.org/abs/2606.09096).
- D. Bernstein and J. Lagarias,
  [The 3x+1 Conjugacy Map](https://doi.org/10.4153/CJM-1996-060-x).
- G. Zhao,
  [The exceptional set of Goldbach problem](https://arxiv.org/abs/2511.05631).
- K. Ford and J. Maynard,
  [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).

Interval continuity, CRT, the prime number theorem, and standard symbolic coding are
not claimed as new. The PrimeProject contribution is their exact four-track synthesis,
the quantitative no-go boundaries, machine audit, and explicit next-theorem contracts.

All conjecture-resolution counters remain zero.
