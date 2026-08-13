# TICKET-224: 날카로운 완전성 임계값

## 상태와 주장 범위

TICKET-224는 TICKET-223의 네 증명 DAG를 그대로 이어간다. 정확한 유계
정리 네 개와 불충분한 경로에 대한 명시적 반례 모형 네 개를 확정하지만,
상위 난제는 하나도 해결하지 않는다.

| 연구 트랙 | 정확한 새 결과 | 폐기 또는 제한한 경로 | 상위 난제 상태 |
|---|---|---|---|
| 리만 가설 | 최적인 `1/4` 지수 꼬리 포락선과 엄격한 band 부호 인증서 | 기존 계수 1 경계가 최적이거나 추상 부호 인증서가 곧 RH 판정이라는 주장 | 미해결 |
| 콜라츠 추측 | 유한 cycle의 정확한 소수 거듭제곱 지수 판정 | radical만 검사하는 adaptive 나눗셈으로 충분하다는 주장 | 미해결 |
| 강한 골드바흐 추측 | 유한 범위에서 제곱근 wheel의 정확성 | 고정 또는 불완전 wheel 개수가 소수 개수와 같다는 주장 | 미해결 |
| 쌍둥이 소수 추측 | 제곱근 pair filter의 정확성과 그 아래 CRT 반례 | 제곱근 아래 wheel 생존이 쌍둥이 소수를 인증한다는 주장 | 미해결 |

공통 주제는 완전성 임계값(completeness threshold)이다. 유한 관측이
정확한 판정기가 되려면 충분한 정보를 포함해야 한다. 그러나 그
임계값에 도달한 유한 판정기는 보편 명제나 무한성 명제의 증명이 아니다.

## 1. 리만 가설

### 이번에 증명한 정확한 명제

`(0,infinity)` 위의 유한 부호 보렐 측도 `sigma`가 어떤 `eta>0`에 대해

```text
||sigma||_eta = integral exp(eta t) d|sigma|(t) < infinity
```

를 만족한다고 하자. dyadic band를

```text
W_j(sigma)
  = integral [exp(-2^(-j)t) - exp(-2^(1-j)t)] d sigma(t)
```

로 정의한다. `[T,infinity)`에 놓인 꼬리에 대해

```text
sup_j |W_j(sigma_tail)|
  <= (1/4) exp(-eta T) ||sigma||_eta                 (RH-224.1)
```

가 성립한다. 상수 `1/4`는 모든 `j,T`에 대해 균일하게 더 작게 바꿀 수
없는 최적 상수다. 따라서 절단된 band의 절댓값이 `(RH-224.1)`의 우변보다
엄격히 크면 전체 band의 부호도 확정된다.

### 수학적 논증

`u=2^(-j)t`로 두면 band kernel은

```text
k(u)=exp(-u)-exp(-2u)
```

이다. 미분하면 유일한 극대점은 `u=log 2`이고 그 값은 `1/4`이다.
따라서 `0<=k(u)<=1/4`이고,

```text
|W_j(sigma_tail)|
 <= (1/4)|sigma|([T,infinity))
 <= (1/4)exp(-eta T)||sigma||_eta
```

를 얻는다.

임의의 정수 `j`에 대해 `T=2^j log 2`로 두고

```text
sigma=exp(-eta T) delta_T
```

를 택하면 가중 노름은 1이고 `j`번째 band는 정확히
`exp(-eta T)/4`이다. 따라서 등호가 실제로 달성되며 `1/4`는 최적이다.
부호 인증은 역삼각부등식으로 따른다. 경계값에서는 반대 부호의 극단
원자가 절단 band를 상쇄할 수 있으므로 엄격 부등식도 균일하게 필요하다.

### 재현 계산

TICKET-223의 무한 교대 원자 모형에서 6개 절단 높이를 검사했고, 9개의
`T=2^j log 2` 원자에서 등호를 검사했다. 모든 꼬리는 `1/4` 포락선 아래에
있고 모든 극단 행은 정확히 등호를 달성했다.

### 한계, 폐기 경로, 다음 보조정리

이 결과는 추상 절단 상수를 개선했을 뿐이다. 제타 영점 결함과 동치인
측도, 그 측도의 지수 모멘트, 소수 쪽 band margin은 증명하지 않았다.

- 폐기: 최적이 아닌 계수 1 꼬리 포락선 사용, 또는 추상 band 제어를 RH
  판정으로 승격하는 경로.
- 유지: 실제 제타-소수 명시공식에서 band를 구성하고 최적 꼬리보다 큰
  margin을 증명하는 경로.
- 다음 단일 보조정리:
  `PrimeSideDyadicBandMarginsExceedSharpQuarterTailEnvelopeAtCofinalCutoffs`.

## 2. 콜라츠 추측

### 이번에 증명한 정확한 명제

양의 가속 콜라츠 valuation word `a=(a_1,...,a_h)`에 대해

```text
S=sum a_i,
D=2^S-3^h>0,
B=sum_i 3^(h-i)2^(a_1+...+a_(i-1))
```

로 둔다. TICKET-222는 `D|B`가 정확한 유한 cycle 조건임을 증명했다.

```text
D=product_(q|D) q^(e_q)
```

이면

```text
D|B iff v_q(B)>=e_q for every q|D.                  (CO-224.1)
```

하지만 `rad(D)|B`만 검사하는 것은 불충분하다. 원시 word

```text
a=(1,1,2,4,3)
```

에서는

```text
D=2^11-3^5=1805=5*19^2,
B=475=5^2*19
```

이므로 `rad(D)=95`는 `B`를 나누지만 `D`는 `B`를 나누지 않는다.

### 수학적 논증

`(CO-224.1)`은 소인수분해의 유일성이다. `D|B`가 실패하면
`v_q(B)<v_q(D)`인 소수 `q`가 반드시 있고, 이것이 prime-power deficit
인증서가 된다.

표시한 word를 직접 대입하면 `D=1805`, `B=475`다. 길이 5는 소수이고
word는 상수가 아니므로 더 짧은 block의 반복일 수 없어 원시다.
특히

```text
v_19(D)=2>1=v_19(B)
```

이므로 radical 검사에서는 놓치는 정확한 반례가 된다.

### 재현 계산

높이 `2..5`, alphabet `{1,2,3,4}`의 1,360개 word를 전부 열거했다.
`D>0`인 원시 word 1,295개에서 prime-power 판정과 직접 `D|B` 사이의
불일치는 0개였다. Radical-only 거짓 양성은 5개였고, 모두 위 word의
다섯 회전이었다.

### 한계, 폐기 경로, 다음 보조정리

`D`를 완전히 소인수분해하면 정확한 인증서를 얻지만 이는 원래 `D|B`
조건을 분해해 쓴 것에 불과하다. 모든 비자명 원시 word가 deficit을
가진다는 정리, deficit의 크기 경계, 비주기 발산 궤도 하강은 남아 있다.

- 폐기: radical-only adaptive 나눗셈을 완전한 cycle 판정으로 사용.
- 유지: 모든 비자명 코드의 prime-power deficit과 비주기 하강을 함께
  다루는 경로.
- 다음 단일 보조정리:
  `UniformPrimePowerDeficitOrUniversalAperiodicDescent`.

## 3. 강한 골드바흐 추측

### 이번에 증명한 정확한 명제

정수 cutoff `z`에 대해 `m<=z`이면 정확한 소수 판정을 하고, `m>z`이면

```text
Q_z(m)=1 iff no prime p<=z divides m
```

로 정의하자. `z>=sqrt(X)`이면 모든 `2<=m<=X`에서

```text
Q_z(m)=1 iff m is prime.                             (GB-224.1)
```

따라서 모든 짝수 `N<=X`에서 `Q_z`의 ordered convolution은 정확한
골드바흐 ordered representation count와 같다.

그러나 임의의 고정 cutoff는 더 큰 모든 범위에서 정확할 수 없다.
`r,s>z`인 소수를 골라 `m=rs`, `N=2m`으로 두면 `m`은 합성수지만
`Q_z(m)=1`이다. 따라서 filtered convolution에는 거짓 대각쌍 `(m,m)`이
추가되어 실제 소수 convolution보다 엄격히 커진다.

### 수학적 논증

모든 합성수 `m<=X`는 `sqrt(m)<=sqrt(X)<=z` 이하의 소인수를 가진다.
`m>z`이면 wheel이 그 인수를 검출하고, `m<=z`이면 정확한 작은 값 판정이
검출한다. 모든 소수는 통과하므로 `(GB-224.1)`과 convolution 항등식이
성립한다.

반대로 `r,s>z`이면 `z` 이하 소수는 `rs`를 나누지 않는다. Filter는 모든
실제 소수 표현을 포함하면서 `(rs,rs)`도 포함하므로 엄격한 과대계수가
된다.

### 재현 계산

`X=100,1000,10000,100000`에서 올림 제곱근 cutoff를 사용해 `X` 이하
모든 정수의 filter 결과와 직접 소수 판정을 비교했다. 불일치는 모두
0개다. Cutoff `3,5,7,11,17,29`에서는 명시적 semiprime 대각쌍이 모두
filtered count를 엄격히 증가시켰다.

### 한계, 폐기 경로, 다음 보조정리

제곱근 trial division은 유한 범위의 정확한 알고리즘일 뿐 모든 `N`에
대한 골드바흐 증명이 아니다. 완전한 유한 소수 판정 정보를 소비한다.
유의미한 증명은 이보다 적은 factor depth로 균일한 양의 하한을 얻어야
한다.

- 폐기: 고정 또는 불완전 wheel convolution을 소수 convolution과 동일시.
- 유지: 제곱근보다 낮은 level에서 소수 가중 오차를 양의 국소 margin
  아래로 제한.
- 다음 단일 보조정리:
  `SubSquareRootPrimeWeightedGoldbachRemainderBelowUniformLocalMargin`.

## 4. 쌍둥이 소수 추측

### 이번에 증명한 정확한 명제

같은 filter에서 `z>=sqrt(X)`, `n+2<=X`이면

```text
Q_z(n)Q_z(n+2)=1
 iff n and n+2 are both prime.                       (TP-224.1)
```

하지만 모든 고정 `z`에는 더 큰 범위의 거짓 양성이 무한히 많다. `W`를
`z` 이하 소수의 곱으로 두고, 모든 소수에서 `0,-2`를 피하는 `a mod W`를
고른다. 서로 다른 `r,s>z`에 대해 CRT로

```text
n=a  (mod W),
n=0  (mod r),
n=-2 (mod s)
```

를 푼다. 이 진행의 충분히 큰 모든 항은 두 `Q_z` 검사를 통과하지만 두
항 모두 합성수다.

### 수학적 논증

`(TP-224.1)`은 `(GB-224.1)`을 `n`, `n+2`에 각각 적용하면 된다. CRT의
모듈러스는 서로소다. 첫 합동식은 전체 wheel 생존 signature를, 나머지
두 합동식은 wheel 밖의 진인수를 제공한다. `Wrs`의 배수를 계속 더하면
이런 합성수 쌍이 무한히 생긴다.

### 재현 계산

네 제곱근 exactness 행의 불일치는 0개다. 여섯 cutoff에서 명시적 CRT
합성수 쌍을 만들었다. 예를 들어 `z=3`에서는 `(215,217)`, `z=5`에서는
`(2891,2893)`을 얻는다. 모든 witness는 지정 인수보다 크고 불완전
filter를 통과한다.

### 한계, 폐기 경로, 다음 보조정리

정확한 유한 소수 판정만으로 성공 후보가 무한히 존재함을 보일 수 없다.
제곱근보다 적은 정보를 사용할 때는 CRT 합성수 mass와 실제 소수쌍
mass를 구분하는 해석적 정보가 필요하다.

- 폐기: sub-square-root wheel 생존을 쌍둥이 소수 인증서로 사용.
- 유지: 합성수 반례 mass를 제거하면서 gap-two main term을 양수로
  보존하는 균일 Type-II 또는 bilinear 추정.
- 다음 단일 보조정리:
  `UniformSubSquareRootTypeIIBilinearSeparationForGapTwo`.

## 네 트랙의 통합 결론

이번에 얻은 네 임계값은 같은 논리 원리를 보여준다.

1. RH band 부호는 신호가 최적 꼬리 오차보다 커야 인증된다.
2. 콜라츠 나눗셈은 모든 소수의 중복도까지 보존해야 인증된다.
3. 골드바흐와 쌍둥이 소수의 유한 filter는 완전한 제곱근 factor 정보를
   넣으면 정확해진다.
4. 완전성 임계값 아래에는 명시적인 적대적 반례 모형이 살아남는다.

이 정리들은 증명 탐색의 논리적 품질을 높이고 새로운 수학이 필요한
위치를 좁힌다. 영점 부재, 모든 콜라츠 궤도의 하강, 모든 짝수의 소수합,
무한히 많은 쌍둥이 소수 중 어느 것도 증명하지 않았다.

## 문헌 경계

- Connes와 Consani의 [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368)은 semi-local RH 관측량의 배경이다. 이번 `1/4` kernel 정리는 초등적 최적화이며 RH 판정이 아니다.
- Tao의 [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)는 거의 모든 궤도와 모든 궤도 사이의 경계를 보여준다.
- Oliveira e Silva, Herzog, Pardi의 [짝수 골드바흐 추측 계산 검증](https://doi.org/10.1090/S0025-5718-2013-02787-1)은 훨씬 큰 유한 검증 경계다.
- Ford와 Maynard의 [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368)는 상당한 Type-I/Type-II 정보가 필요한 이유를 설명한다.

초등적 kernel 최적화, 소인수 지수 판정, 제곱근 체 항등식, CRT 구성에
대해 문헌 우선권을 주장하지 않는다.

## 재현 방법

```powershell
python scripts/ticket224_sharp_completeness_thresholds.py
python -m unittest tests.test_ticket224_sharp_completeness_thresholds -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

주 기계 판독 산출물:

`data/open-problem/ticket224-sharp-completeness-thresholds.json`
