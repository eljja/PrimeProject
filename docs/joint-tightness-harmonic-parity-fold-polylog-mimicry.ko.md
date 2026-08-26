# TICKET-244: joint tightness, harmonic bad line, parity folding, polylog mimicry

## 주장 경계

TICKET-244는 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수
추측 중 어느 것도 증명하거나 반증하지 않았다. 이번 회차는 부분정리
세 개와 정확한 경로 no-go 하나를 증명한다. 회차는 완료됐지만 네 상위
문제는 모두 `open_not_proven`이며 후보 해결도 0개다.

통합 기계 기록은
`data/open-problem/ticket244-joint-tightness-harmonic-parity-fold-polylog-mimicry.json`
이다. 영속 상태는 TICKET-243에서 정확히 한 단계 올라 TICKET-244가 됐다.
deep focus는 Twin Prime이다. 고정 주기 결과를 임의의 고정 로그 거듭제곱
이하의 가변 주기 전체로 강화할 수 있기 때문이다.

## 재현 계약

```text
python scripts/ticket244_joint_tightness_harmonic_parity_fold_polylog_mimicry.py
python -m unittest tests.test_ticket244_joint_tightness_harmonic_parity_fold_polylog_mimicry -v
python scripts/verify_ticket244_structure.py
```

random seed는 없다. 모든 계산은 결정적이다. RH는 정확한 유리수·기호값,
Collatz는 정수 모듈러 연산, Goldbach는 정수 sieve와 직접 ordered-pair
계수, Twin은 CRT와 결정적 64-bit Miller-Rabin을 사용한다. 부동소수점값은
어떤 증명에도 사용하지 않는다.

| 문제 | TICKET-244의 정확한 결과 | 분류 | 상위 상태 |
|---|---|---|---|
| 리만 | bounded `L2(R)` 집합에서 physical-frequency joint tightness가 relative compactness의 필요충분조건이며 한쪽 조건만으로는 실패한다 | `partial_theorem` | `open_not_proven` |
| 콜라츠 | 고정기저 Fermat-quotient bad line을 mod `q`의 half/third harmonic sum 관계로 정확히 환원한다 | `partial_theorem` | `open_not_proven` |
| 강한 골드바흐 | odd-prime even-target integrand가 정확히 반주기이므로 `0`과 `1/2` arc를 folding할 수 있다 | `partial_theorem` | `open_not_proven` |
| 쌍둥이 소수 | `M_X <= (log X)^A`인 모든 periodic fingerprint가 충분히 큰 모든 dyadic block에서 소수/합성 후속항 모방자를 가진다 | `exact_no_go` | `open_not_proven` |

## 1. 리만 가설

### A. 정확한 명제

`L2(R)`의 unitary Fourier transform을 사용한다. bounded 집합 `K`가
relative compact일 필요충분조건은 모든 `epsilon>0`에 대해 어떤 `R`이
존재하여

```text
sup_(f in K) integral_(|x|>R) |f(x)|^2 dx       < epsilon,
sup_(f in K) integral_(|xi|>R) |fhat(xi)|^2 dxi < epsilon               (RH-244.1)
```

을 동시에 만족하는 것이다. 어느 한 조건만으로는 충분하지 않다.
TICKET-243은 frequency-only 반례를 줬다. 새 physical-only 반례는

```text
f_n(x)=pi^(-1/2) 1_[-pi,pi](x) cos(nx), n>=1                           (RH-244.2)
```

이다. 이 함수들은 normalized, real-even, 공통 compact support를 가지지만
orthonormal이다.

### B-D. 정의, 증명, 각 단계의 근거

`K`에서 `||f||_2<=B`라 하자. Plancherel에 의해

```text
||tau_h f-f||_2^2
 <= R^2 h^2 B^2 + 4 epsilon.                                           (RH-244.3)
```

저주파 부분에는 `|exp(iu)-1|<=|u|`를 쓰고, 고주파 부분에는 (RH-244.1)을
쓴다. 따라서 frequency tightness가 uniform translation continuity를 준다.
여기에 physical tightness를 합치면 Riesz-Kolmogorov 정리로 relative
compactness가 나온다.

역방향은 compact closure의 유한 `epsilon`-net을 잡는다. 유한 개 중심의
physical tail을 동시에 자르는 하나의 반지름이 존재하며 net 오차로 전체
집합에 전달된다. Fourier transform은 unitary이므로 Fourier image에도 같은
논증을 적용한다. (RH-244.2)의 Gram 행렬은 cosine orthogonality로 정확히
항등행렬이다.

이는 고전적 compactness 정리를 TICKET-243의 간극에 적용한 것이며 새로운
functional-analysis 정리라고 주장하지 않는다. 현대적 `L2`/Paley-Wiener
정리는 [Mitkovski–Stockdale–Wagner–Wick](https://arxiv.org/abs/2204.14237)을
확인했다.

### E-H. 반례·경계검사, 계산, 해석, 유한 한계

- 양화사는 `K` 전체에 대해 uniform이며 점별 명제를 균일 명제로 바꾸지 않았다.
- boundedness는 필수 전제다.
- 크기 `4,8,16,32,64`인 physical-support Gram certificate 다섯 개는
  diagonal `1`, off-diagonal `0`, 최소 거리 제곱 `2`다.
- `R=n`, `h=1/n^2`, `epsilon=1/n^2`, `B=1`인 다섯 유리수 행에서
  (RH-244.3)은 정확히 `5/n^2`다.
- transcript SHA-256:
  `ba395b597b5ad65a2e1542934cb1781646c445f36e3b2828931e423fde04b07b`.
- 유한 열 행은 공식을 재현할 뿐이다. 무한 정리는 Plancherel과
  Riesz-Kolmogorov에 의존한다.

### I-K. 분류, 최소 간극, 다음 단일 보조정리

분류: `partial_theorem`.

새 폐기 경로는 physical tightness 단독 compactness다. TICKET-243과 합치면
두 one-sided shortcut 모두 닫힌다. 그러나 실제 normalized admissible
Guinand-Weil class의 joint tightness·exhaustion, signed arithmetic tail의
uniform bound, 양의 limit margin은 증명되지 않았다. RH는 여전히 Clay의
Millennium 미해결 문제다([공식 페이지](https://www.claymath.org/millennium/Riemann-Hypothesis/)).

다음 단일 보조정리:
`UniformSignedGuinandWeilTailWithPositiveMarginOnExhaustiveJointlyTightAdmissibleClasses`.

## 2. 콜라츠 추측

### A. 정확한 명제

소수 `q>5`에 대해

```text
F_q(a)=(a^(q-1)-1)/q mod q,
H_m=sum_(1<=k<=m) k^(-1) mod q
```

라 두면

```text
2F_q(2) = -H_((q-1)/2),
3F_q(3) = -2H_floor(q/3).                                               (CO-244.1)
```

따라서

```text
5F_q(2)=3F_q(3) iff 4H_floor(q/3)=5H_((q-1)/2),                        (CO-244.2)
 F_q(2)= F_q(3) iff 4H_floor(q/3)=3H_((q-1)/2).                        (CO-244.3)
```

(CO-244.2) 위에서 (CO-244.3)은 half harmonic sum이 0일 때와 정확히
동치다. 그러므로 **첫 q-adic 층**의 positive-defect 후보는 (CO-244.2)와
`H_((q-1)/2)!=0`의 결합이다. 두 첫 층이 모두 0이면 더 높은 valuation은
이번 정리로 결정되지 않는다.

### B-D. 정의, 증명, 각 단계의 근거

일반적인 `m`에 대해 `m`을 곱하는 사상은 mod `q`의 nonzero residue를
순열시킨다. `mk=r_k+q floor(mk/q)`라 쓰고 곱을 mod `q^2`에서 비교한 뒤
floor가 같은 항을 묶으면 Lerch 항등식

```text
mF_q(m)=-sum_(j=1)^(m-1) H_floor(jq/m) mod q                           (CO-244.4)
```

을 얻는다. `m=2`가 첫 식을 준다. `m=3`에서는 `k -> q-k` 반사로
`H_floor(2q/3)=H_floor(q/3)`이므로 둘째 식을 얻는다. 이를 두 Fermat
quotient line에 대입하면 (CO-244.2)-(CO-244.3)이 나온다. 첫 line 위에서
둘째 line은 `5H_half=3H_half`, 즉 `H_half=0`이다.

Fermat/Wieferich quotient의 표준 배경은
[Sondow](https://arxiv.org/abs/1110.3113)를 확인했다. (CO-244.4)의 증명은
문서 안에 포함했으므로 분포에 관한 미증명 가정을 가져오지 않았다.

### E-H. 반례·경계검사, 계산, 해석, 유한 한계

- 정리는 첫 mod-`q^2` 층에 한정된다. 두 residue가 0일 때 valuation 비교를
  주장하지 않는다.
- `5<q<=20,000`인 소수 `2,259`개를 exact integer arithmetic으로 검사했다.
- modular inverse 선형 recurrence와 modular exponentiation을 사용한다.
  복잡도는 `O(sum_(q<=Q,q prime)q)` 정수 연산과 `O(pi(Q))` modular power다.
- harmonic identity, 직접 `q^2` 합동, first-order 후보 동치를 모두 재검사해
  실패 0, bad-line 소수 0, first-order positive 후보 0을 얻었다.
- transcript SHA-256:
  `bf5611e2479fe672d7d3a6b8d746f99c79bfee67bc7f894075681ca39b6723a2`.
- 이 범위는 새 기록이 아니다. TICKET-241은 기존 exponent 표현을 훨씬 멀리
  검사했다. 따라서 유한 부재를 진전이라고 주장하지 않는다.

### I-K. 분류, 최소 간극, 다음 단일 보조정리

분류: `partial_theorem`.

새 폐기 경로는 없다. harmonic 표현은 `q^2` exponent 조건을 유한체
prefix-sum 항등식으로 바꾸고 반증 가능한 다음 명제를 드러내므로 유지한다.
모든 소수에서 bad line이 비소거라는 증명은 없다. 설령 이를 증명해도 현재
run-block local defect만 닫을 뿐 일반 necklace, 발산 orbit, nontrivial cycle을
해결하지 않는다. Tao의 결과도 almost-all orbit 진술과 all-orbit conjecture의
차이를 명확히 보여준다([원 논문](https://arxiv.org/abs/1909.03562)).

다음 단일 보조정리:
`FixedBaseHarmonicBadLineNonvanishingForEveryPrime`.

## 3. 강한 골드바흐 추측

### A. 정확한 명제

`e(t)=exp(2 pi i t)` 및

```text
O_X(alpha)=sum_(3<=p<=X) e(p alpha)
```

라 두면

```text
O_X(alpha+1/2)=-O_X(alpha).                                             (GB-244.1)
```

모든 짝수 `N`에 대해 `O_X(alpha)^2 e(-N alpha)`는 정확히 `1/2`-periodic이다.
따라서 `1/2` 주변 arc의 signed integral은 `0` 주변 translate와 같다. 또한
짝수 `N>=6`에서는 full-prime과 odd-prime binary coefficient가 같다.

### B-D. 정의, 증명, 각 단계의 근거

`O_X`의 모든 소수는 홀수이므로 `1/2` translation이 각 항에 `-1`을 곱한다.
제곱하면 부호가 사라지고 짝수 target phase는 `e(-N/2)=1`을 얻는다. 따라서
절대 에너지가 아니라 signed integrand 자체가 반주기다.

`S_X=O_X+e(2alpha)`로 전개하면 차이는 summand `2`가 포함되거나 `2+2`인
계수다. 짝수 `N>=6`에서 `2+(N-2)`의 두 번째 항은 `4` 이상의 짝수이므로
소수가 아니다. 따라서 두 coefficient가 정확히 같다.

### E-H. 반례·경계검사, 계산, 해석, 유한 한계

- `N` 짝수와 `N>=6`은 필수다. `N=4`에는 `2+2`가 있고, 홀수 `N`에서는
  target phase의 부호가 바뀐다.
- `X=100,500,1000,5000,10000`에서 `6<=N<=X`인 짝수 총 `8,290`개를 exact
  sieve와 ordered-pair count로 검사했다.
- full/odd coefficient 실패 0, integer cyclic phase half-turn 실패 0이다.
- reference 구현 복잡도는 `O(sum_X X*pi(X))`이고 random·float는 없다.
- transcript SHA-256:
  `ba16a10093eb8fe103469b86dec9e5768dcfed91fccc7944168c6c775a0d3c61`.
- bounded representation 검사는 무한 Goldbach 증명이 아니다. 새 무한 결과는
  folding identity뿐이다.

### I-K. 분류, 최소 간극, 다음 단일 보조정리

분류: `partial_theorem`.

odd-prime 문제에서 `0`과 `1/2` arc를 독립 signed 문제처럼 다루는 경로는
폐기한다. 둘은 정확한 translate다. 그러나 다른 작은 분모 arc와 residual
minor arc는 통제하지 못했다. Helfgott의 ternary Goldbach 논문은 rigorous
major/minor-arc 경계의 1차 자료지만 binary strong Goldbach를 증명하지 않는다
([논문](https://arxiv.org/abs/1205.5252)).

다음 단일 보조정리:
`CompleteDenominatorAtLeastThreeMajorArcExtractionAndSignedResidualSavingAfterParityFolding`.

## 4. 쌍둥이 소수 추측 — deep focus

### A. 정확한 명제

`A>0`을 고정한다. 충분히 큰 각 `X`에 대해

```text
1<=M_X<=(log_2 X)^A,
gcd(a_X,M_X)=gcd(a_X+2,M_X)=1
```

이고 `F_X(n,n+2)`가 mod `M_X`의 residue pair에만 의존한다고 하자. 그러면
충분히 큰 모든 `[X,2X]`에는 소수 `p`가 존재하여

```text
F_X(p,p+2)=F_X(a_X,a_X+2)
```

이지만 `p+2`는 합성수다. 따라서 고정된 어떤 log 거듭제곱 이하의
scale-dependent period를 쓰는 pure periodic twin classifier 전체가 실패한다.

### B-D. 정의, 증명, 각 단계의 근거

`M_X>=2`이면 Bertrand 공준으로 `M_X<ell_X<2M_X`인 소수 `ell_X`를 잡는다.
`M_X=1`이면 `ell_X=3`으로 둔다. CRT로

```text
r_X=a_X mod M_X,
r_X=-2  mod ell_X,
Q_X=M_X ell_X<2M_X^2<=2(log_2 X)^(2A)                             (TP-244.1)
```

인 reduced class를 얻는다. Siegel-Walfisz는 임의의 고정 log 거듭제곱 이하
modulus에서 균일하므로

```text
pi(2X;Q_X,r_X)-pi(X;Q_X,r_X)
 ~ (Li(2X)-Li(X))/phi(Q_X)>0                                      (TP-244.2)
```

가 충분히 큰 모든 `X`에서 균일하게 성립한다. 이 class의 소수 `p`를 잡으면
첫 합동은 `F_X`를 보존하고 둘째 합동은 `ell_X|p+2`를 준다. 결국
`X>ell_X`이므로 이는 proper divisor이고 `p+2`는 합성수다.

필요한 균일 PNT-AP의 1차 자료로
[Thorner–Zaman](https://arxiv.org/abs/2108.10878)을 확인했다.

### E-H. 반례·경계검사, 계산, 해석, 유한 한계

- `A`는 `X`보다 먼저 고정된다. `A=A(X)`를 허용하지 않는다.
- CRT residue는 `Q_X`와 서로소다. admissibility가 `M_X` 부분을 처리하고
  `ell_X`는 홀수라 `-2`가 0이 아니다.
- 고정 modulus PNT가 아니라 varying modulus와 residue에 uniform한
  Siegel-Walfisz가 필요하다.
- `A=4`, `M=30,210,2310,30030`, 각 `M`보다 큰 최소 소수, `X=1000Q`인
  결정적 행 네 개를 만들었다.
- 네 행 모두 exact bit-length 조건 `M<=floor(log_2 X)^4`, prime mimic,
  `ell|p+2`를 통과했다. 최대 행은 `p=905230686377`,
  `p+2=30047*30127157`이다.
- 유한 행의 복잡도는 시도한 progression candidate 수에 선형이며 primality는
  결정적이다. transcript SHA-256:
  `506feb7368986984fd026ada7be00bb70d5049766f2ab1d0c02ee24686cb8d7c`.
- 네 행이 무한 정리를 증명하는 것이 아니다. 무한 결론은 (TP-244.2)가 준다.

### I-K. 분류, 최소 간극, 다음 단일 보조정리

분류: 지정한 periodic-classifier 경로에 대한 `exact_no_go`.

새 폐기 경로는 period와 accepted residue가 scale마다 바뀌더라도 고정된 log
거듭제곱 이하인 모든 pure periodic fingerprint다. 이 정리는 superpolylog
period, nonperiodic 정보, signed von Mangoldt correlation, Type-I/II 추정을
다루지 않으며 twin primes를 증명하거나 반증하지 않는다.

다음 단일 보조정리:
`SuperPolylogarithmicScaleLocalTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass`.

## proof DAG와 적대적 감사

네 machine DAG는 모두 acyclic이며 `open` frontier가 정확히 하나다. 외부
compactness·arithmetic-progression 정리는 `external_theorem`으로 표시했다.

```text
RH-T243 + Plancherel + Riesz-Kolmogorov
  -> RH-N244 disproved -> RH-T244 proved -> RH-OPEN244
CO-T243 -> CO-T244 proved (first layer only) -> CO-OPEN244
GB-T243 -> GB-N244 disproved -> GB-T244 proved -> GB-OPEN244
TP-T243 + Bertrand + Siegel-Walfisz
  -> TP-N244 disproved -> TP-T244 proved -> TP-OPEN244
```

어떤 DAG 경로도 상위 추측의 `proved` 또는 `disproved` 노드에 도달하지
않는다. 해결 수와 후보 해결 수는 모두 0이다.

## 최종 경계

TICKET-244 회차는 완료됐다. 부분정리 세 개와 정확한 no-go 하나를 확립했고
machine failure와 정체 트랙은 0개다. 네 추측 중 어느 것도 해결하지 않았다.

**이번 회차는 완료되었지만 해당 추측은 해결되지 않았다.**
