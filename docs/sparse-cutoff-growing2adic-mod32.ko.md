# TICKET-265 — 희박 envelope·cutoff no-go, 성장형 2-adic tie 판정, mod-32 Twin 필터

## 판정

TICKET-265 회차는 완료됐지만 네 원 추측 중 증명되거나 반증된 것은 없다. 이번 결과는 `exact_no_go` 2개와 `partial_theorem` 2개다. 심층 집중 문제는 콜라츠다. 정본 기계 산출물은 `data/open-problem/ticket265-sparse-cutoff-growing2adic-mod32.json`이며, 각 문제별 JSON과 열린 전선 하나를 가진 비순환 proof DAG도 함께 생성한다.

재현 명령:

```text
python scripts/ticket265_sparse_cutoff_growing2adic_mod32.py
python -m unittest tests.test_ticket265_sparse_cutoff_growing2adic_mod32 -v
python scripts/verify_ticket265_structure.py
```

생성기의 산술은 모두 정수 또는 `Fraction`의 정확 연산이다. Twin 연분수는 앞서 인증한 유리수 근 구간을 사용한다. 실제 Goldbach 행 3개는 SHA-256으로 고정한 TICKET-260 인증서에서 읽으며, 이번 회차는 새 소수 체를 실행하지 않는다.

## 1. 리만 가설

### 이번 정확 명제

`DensityOneReciprocalControlCannotReplaceLimsupEnvelope`.

`L>0`, `P,M>=0`, `P+M>L`라 하자. 충분히 큰 모든 `k`에 대해

```text
a_(2^k)   = P/2^k,
a_(2^k+1) = -M/(2^k+1),
a_n       = 0 (그 밖의 n),
E_n       = L+a_n
```

로 두면 `E_n>0`, `E_n -> L`이고, 오차가 0이 아닌 지표 집합은 자연밀도 0이며 0-오차 간격은 임의로 길어진다. 그러나

```text
A_+=limsup n(a_n)^+=P,
A_-=limsup n(a_n)^-=M,
S_(2^k)=(2^k+1)E_(2^k+1)-2^kE_(2^k)=L-P-M<0.
```

### 논증·계산·한계

`X` 이하 예외 지표는 최대 `2(log_2 X+1)`개이므로 밀도 0이다. 두 스파이크 부분수열에서 스케일 오차가 정확히 `P`, `M`이고 나머지는 0이다. 대입하면 음의 lag 식이 바로 나온다. 재현 계산은 `L=1`, `P=3/4`, `M=1/2`, `k=2,...,17`을 검사하며 모든 lag가 정확히 `-1/4`이다.

이는 추상 수열 반례이며 실제 Guinand–Weil packet이 아니다. 따라서 “밀도 1 또는 희박 표본에서의 reciprocal 제어가 모든 지표의 envelope를 대체한다”는 경로만 폐기한다. RH 자체는 미해결이고, 실제 packet에서 `A_++A_-<L`을 보이는 산술 추정이 남는다.

다음 단일 보조정리: `ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit`.

## 2. 콜라츠 추측 — 심층 집중

### 이번 정확 명제

`UnboundedExplicitThresholdCutoffDoesNotImplyDivergence`.

TICKET-264의 임계 cutoff `K_N`이 비유계이지만 무한대로 가지 않는 `R/Z`의 명시적 수열이 존재한다. 완전 4점 격자에서 시작해 각 `q=2^r` 단계에서 앞선 `q/2`-격자를 짝수 `q`차 근으로 보고, 먼저 각도가 `(-pi/2,pi/2)`인 홀수 근 `q/4`개를 붙인 뒤 나머지 홀수 근을 붙인다.

완성 시점 `N=q`에는 완전 `q`-격자이므로 `K_q=q-1`이다. 중간 시점 `N=3q/4`에는 앞 격자의 1차 조화합이 0이고 새 기하합의 크기가 `csc(2pi/q)`다. `sin x<x`, `pi<22/7`에서

```text
|W_N(1)| > 7/33 > 1/6
```

이므로 `H=6`이 실패하고 `K_N<=5`다. 따라서 `limsup K_N=infinity`, `liminf K_N<=5`이다.

재현 계산은 `q=8,...,2048`의 9개 2의 거듭제곱을 정수 열거와 유리수 부등식으로 검사한다. 이는 유한 패턴 추측이 아니라 무한 구성을 증명하지만, Collatz 환원에서 나오는 정본 Fermat-quotient 수열은 아니다. 그러므로 “큰 cutoff 인증이 무한히 자주 나오면 Weyl 상쇄가 따른다”는 경로는 폐기되지만 Collatz는 미해결이다.

다음 단일 보조정리: `CanonicalFermatQuotientThresholdCutoffHasNoBoundedSubsequence`.

## 3. 강한 골드바흐 추측

### 이번 정확 명제

`GrowingTwoAdicTieSignatureIsSharpAndDecisive`.

`M>=1`, `N_1,N_2>=0`, `N_1+N_2=2M`이라 하자. 합동식

```text
N_2 = M (mod 2^m)
```

이 모든 이런 쌍에 대해 `N_1=N_2=M`을 강제할 필요충분조건은 `2^m>M`이다.

실제로 `N_1=M-d`, `N_2=M+d`로 쓰면 `|d|<=M`이고 `2^m|d`이다. `2^m>M`이면 `d=0`뿐이다. 반대로 `2^m<=M`이면 `d=2^m`가 명시적 비-tie 반모형이다.

특수 prefix의 `M_l=3^(6l+3)+1`에서는 최소 결정 지수가 `m_l=bit_length(M_l)`이다. 한 단계 낮은 지수 `m_l-1`은 `(M_l-2^(m_l-1), M_l+2^(m_l-1))` 때문에 항상 불충분하다.

생성기는 `l=0,...,31`에서 임계치와 반모형을 정확히 검사한다. 또한 TICKET-260에서 인증한 실제 `l=0,1,2` 세 수준을 재생해 결정 residue 불일치를 확인한다. 세 수준의 확인은 모든 수준의 불일치를 뜻하지 않는다.

따라서 TICKET-264의 고정 모듈러스 no-go가 모든 성장형 signature까지 배제한다는 해석을 폐기했다. 추상 동률은 정확히 판정하지만, 실제 mod-3 소수 개수의 변위가 모든 수준에서 결정 residue를 피한다는 해석적 제어는 없다. 강한 골드바흐는 미해결이다.

다음 단일 보조정리: `Q3ActualMinusCountAvoidsLeastDecisiveTwoAdicTieResidue`.

## 4. 쌍둥이 소수 추측

### 이번 정확 명제

`PrimitiveTwinUnitSolutionsObeyMod32DiagonalFilter`.

```text
B_1(u,v)=sum_(k=0)^17 C(17,k)2^floor(k/2)u^(17-k)v^k
```

라 하자. `gcd(u,v)=1`, `B_1(u,v)=epsilon`, `epsilon in {+1,-1}`이면 `u`는 홀수, `v`는 짝수이고

```text
u+v = epsilon (mod 32)
```

이다.

mod 2에서 다른 원시 parity 경우는 `B_1`을 짝수로 만든다. `u`가 홀수이고 `v`가 짝수이면 `u^16=1 (mod 32)`이다. `k=0,1` 항은 `u+v`로 줄고, `k>=2` 항의 2-adic valuation은 모두 5 이상이므로 `B_1(u,v)=u+v (mod 32)`다.

필터는 충분조건이 아니다. 모든 `t>=1`에 대해 `(1,32t)`는 원시이고 `+1` 필터를 통과하지만 `B_1>1`이다. 17차 동차성으로 `(-1,-32t)`는 대응하는 음의 반모형이다.

재현 계산은 계수 valuation 16개, 쌍으로 된 반모형 32개, 인증된 unique-root 수렴분수 첫 1,024개를 검사한다. 분모가 짝수인 것은 332개, `+1` 대각 통과 21개, `-1` 대각 통과 14개, 어느 한쪽 통과는 35개다. 그중 33개가 아직 열린 `n>=38` 꼬리에 있다. 이는 필터 생존자이지 unit 해가 아니다.

따라서 국소 mod-32 필터의 충분성 경로를 반례로 폐기했다. 무한 꼬리에는 TICKET-263의 정확한 9차 합동 배제가 여전히 필요하다. 쌍둥이 소수 추측은 미해결이다.

다음 단일 보조정리: `EveryLaterMod32FilterPassFailsJointNinthOrderCongruences`.

## 분류 요약

| 문제 | 새 결과 | 분류 | 해결 상태 | 폐기한 경로 | 남은 간극 | 다음 보조정리 |
|---|---|---|---|---|---|---|
| 리만 가설 | 밀도 1 reciprocal 제어는 all-index envelope를 대체할 수 없음 | exact no-go | 미해결 | 밀도 1/희박 표본이면 충분 | 실제 packet `A_++A_-<L` | `ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit` |
| 콜라츠 | 비유계 `K_N`은 발산을 뜻하지 않음 | exact no-go | 미해결 | 희박한 좋은 prefix이면 상쇄 | 정본 `K_N`에 유계 부분수열이 없음 | `CanonicalFermatQuotientThresholdCutoffHasNoBoundedSubsequence` |
| 강한 골드바흐 | 최소 성장형 2-adic 모듈러스가 추상 tie를 sharp하게 판정 | partial theorem | 미해결 | 고정 모듈러스 no-go가 성장형도 전부 배제 | 실제 결정 residue의 전 수준 회피 | `Q3ActualMinusCountAvoidsLeastDecisiveTwoAdicTieResidue` |
| 쌍둥이 소수 | 원시 unit 해는 mod-32 대각 필요조건을 만족 | partial theorem | 미해결 | 국소 mod-32 필터가 충분 | 모든 후반 생존자의 9차 합동 배제 | `EveryLaterMod32FilterPassFailsJointNinthOrderCongruences` |

회차 완료는 추측 해결을 뜻하지 않는다. 해결 수와 후보 해결 수는 모두 0이다.
