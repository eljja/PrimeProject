# TICKET-258: 총변동·지표·연분수 감사

상태: `iteration_complete`. 네 원 추측은 모두 `open_not_proven`이다.

이번 회차는 TICKET-257의 결과를 반복하지 않고 더 강한 조건을 반증하거나 정확한 구조 환원을 증명한다. deep-focus는 남은 지수 17 Thue 분기를 모든 분모에서 연분수 수렴분수만으로 축소할 수 있는 쌍둥이 소수 트랙이다.

## 결과 경계

| 문제 | 이번 정확 명제 | 분류 | 해결 여부 |
|---|---|---|---|
| 리만 가설 | 양수로 수렴하고 총변동이 유한한 packet energy도 lag 부분합 하한을 강제하지 않는다. | `exact_no_go` | 미해결 |
| 콜라츠 | 서로 다른 홀수 소수 차수의 비자명한 근들과 1은 유리수체 위에서 선형독립이다. | `exact_no_go` | 미해결 |
| 강한 골드바흐 | primitive odd character 하나가 모든 반사 비대칭을 검출할 필요충분조건은 `q-1`이 2의 거듭제곱인 것이다. | `partial_theorem` | 미해결 |
| 쌍둥이 소수 | 남은 17차 분기의 모든 비영 분모 단위계수 해는 유일 실근의 연분수 수렴분수이다. | `partial_theorem` | 미해결 |

네 추측 중 어느 것에도 후보 증명 또는 후보 반례를 주장하지 않는다.

## 1. 리만 가설

### 정확한 명제

\[
E_{4^k}=1-2^{-k}\quad(k\ge1),\qquad E_L=1\quad(그 밖),
\]

로 두고

\[
S_n=(n+1)E_{n+1}-nE_n
\]

로 lag 부분합을 복원한다. 그러면 `E_L >= 1/2`, `E_L -> 1`이고

\[
\sum_{L\ge1}|E_{L+1}-E_L|=2
\]

이지만

\[
S_{4^k-1}=1-2^k\to-\infty.
\]

각 고립 spike가 총변동에 `2*2^(-k)`를 기여하므로 총변동은 정확히 2이다. 따라서 보통의 bounded variation은 TICKET-257의 scaled one-sided variation 조건을 대체할 수 없다.

12개 spike 행을 `Fraction`으로 재현했다. 이는 추상 Toeplitz 반례이며 실제 Guinand-Weil 계수는 계산하지 않았다. 다음 보조정리는 그대로

`ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation`

이다.

## 2. 콜라츠 추측

### 정확한 명제

서로 다른 홀수 소수 `q_1,...,q_N`과 `0<d_j<q_j`에 대해

\[
1,\zeta_{q_1}^{d_1},\ldots,\zeta_{q_N}^{d_N}
\]

은 `Q` 위에서 선형독립이다.

유리 선형관계가 있다고 하고 계수가 0이 아닌 한 항을 고르면, 그 primitive root는 나머지 소수 conductor 원분체의 합성체에 속해야 한다. 서로소 conductor와 차수 곱셈성은 두 체의 교집합이 `Q`임을 주므로 모순이다.

홀수 소수와 비자명 지수 조건은 필수다. `zeta_2=-1`이고 지수 0인 위상은 1이다. 소수 997까지 166개 canonical Fermat-quotient 위상을 exact arithmetic으로 검사했으며 이 유한 범위에는 지수 0이 없었다.

유리 가중 유한 telescoping 경로는 폐기한다. 그러나 크기 상계는 전혀 따라오지 않으므로 다음 보조정리는

`CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude`

이다.

## 3. 강한 골드바흐 추측

### 정확한 명제

홀수 소수 `q`, `n=q-1=2h`, primitive root `g`를 잡고 `chi(g)=zeta_n`인 primitive odd character를 택한다. 잉여 개수 `N_r`에 대해

\[
A(x)=\sum_{0\le j<h}(N_{g^j}-N_{-g^j})x^j
\]

라 하면 character moment는 `A(zeta_n)`이다. 이 character 하나가 모든 반사 비대칭을 검출할 필요충분조건은 `n`이 2의 거듭제곱인 것이다.

- `n=2^a`이면 `Phi_n=x^h+1`이고 차수가 `h`이므로 `deg A<h`인 `A`의 영점이 될 수 없다. 따라서 moment 0은 정확히 반사대칭을 뜻한다.
- `n`이 2의 거듭제곱이 아니면 홀수 소인수가 있어 `phi(n)<h`이다. `A=Phi_n`의 계수 벡터를 양·음 부분으로 분리하면 비대칭인 비음수 잉여 개수 벡터이면서 primitive moment가 정확히 0인 반례가 된다.

실제 `q=5`, `T=1255` 소수 prefix의 잉여 개수는

`[1, 313, 313, 317, 311]`

이고 primitive root 2에 대한 반대칭 벡터는 `[2,-4]`이다. 따라서 quartic moment `2-4i`가 0이 아니며, TICKET-257의 quadratic bit가 놓친 비대칭을 검출한다.

이는 검출기의 완전성 분류이지 실제 모든 prime prefix의 moment 비소멸 정리가 아니다. 다음 보조정리는

`EveryCompatibleEvenQDivisiblePrimePrefixHasNonzeroOddCharacterMoment`

이다.

## 4. 쌍둥이 소수 추측 — deep focus

\[
B_1(u,v)=[\sqrt2](1+\sqrt2)(u+v\sqrt2)^{17},
\qquad P(x)=B_1(x,1)
\]

이고 `rho`를 TICKET-257에서 얻은 `(-1,0)`의 유일한 실근이라 하자.

### 연분수 필요조건 정리

TICKET-257의 primitive 해 환원과 부호 반사를 사용하면 모든 비영 분모 해는 기약분수 `p/q in [-1,0]`에 대해

\[
P(p/q)=\pm q^{-17}
\]

을 만족한다. 정확한 도함수 식의 두 번째 양항만 사용해 `[-1,0]`에서

\[
P'(x)\ge2176(1-1/\sqrt2)>544
\]

를 얻는다. 평균값정리로

\[
|\rho-p/q|<\frac1{544q^{17}}<\frac1{2q^2}.
\]

따라서 `q>=2`이면 Legendre 연분수 판정에 의해 `p/q`는 반드시 `rho`의 수렴분수이다. `q=1`은 직접 검사한다.

유리수 근 구간과 Möbius 변환을 사용해 첫 128개 부분몫을 exact arithmetic으로 인증했고, 각 수렴분수에서 17차 정수형식을 직접 평가했다. `B_1=+1` 또는 `-1`인 경우는 없었다. 수렴분수의 분모가 증가하므로 다음 62자리 분모까지 모든 비영 해가 배제된다.

`67,076,610,336,720,215,425,112,731,771,403,002,965,838,278,844,687,475,228,751,003`

이는 분모마다 검사하던 `O(V)` 방식을 `O(log V)`개의 후보로 바꾼 질적 개선이다. 그러나 이후의 수렴분수가 무한히 남으므로 전역 해 배제는 아니다. 다음 보조정리는

`EveryUniqueRootConvergentMissesUnitCoefficient`

이다.

## 재현

```powershell
python scripts/ticket258_variation_character_convergent.py
python -m unittest tests.test_ticket258_variation_character_convergent
python scripts/verify_ticket258_structure.py
```

모든 계산은 결정적이며 정수와 `Fraction`만 사용한다. random seed와 증명에 사용한 부동소수점 계산은 없다. 통합·문제별 JSON에 SHA-256 transcript와 문제마다 열린 frontier가 하나인 비순환 proof DAG를 기록했다.

## 논리적 한계

- RH 반례는 실제 Weil form이 아니다.
- 원분 위상의 유리 선형독립성은 해석적 상쇄량을 주지 않는다.
- character 검출기 분류는 실제 prime prefix의 비소멸을 강제하지 않는다.
- 유한 개 수렴분수 검사는 모든 수렴분수를 배제하지 않는다.

따라서 TICKET-258은 한 연구 회차의 완료이지 네 추측의 해결이 아니다.
