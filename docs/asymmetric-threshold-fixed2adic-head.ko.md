# TICKET-264 — 비대칭 envelope, 명시적 threshold cutoff, 고정 2진 no-go, 유한 머리 폐쇄

## A. 판정

TICKET-264 회차는 완료됐지만 장기 프로그램은 완료되지 않았다. 이번
회차는 `partial_theorem` 세 개와 `exact_no_go` 하나를 확정한다. 리만
가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측은 모두
`open_not_proven`이며 해결·해결후보 계수는 모두 0이다.

기계 판독 원본은
`data/open-problem/ticket264-asymmetric-threshold-fixed2adic-head.json`이다.
이번 심층 초점은 RH이며, TICKET-263의 대칭 packet-rate 조건을 엄밀히
더 약한 비대칭 조건으로 개선한다.

## B. 재현

```text
python scripts/ticket264_asymmetric_threshold_fixed2adic_head.py
python -m unittest tests.test_ticket264_asymmetric_threshold_fixed2adic_head -v
python scripts/verify_ticket264_structure.py
```

난수는 쓰지 않는다. 생성기는 통합 JSON, 문제별 JSON 네 개, 지속 상태,
문제별 비순환 proof DAG를 기록한다. 유한 재현 범위는 RH 유리수 192행,
complete-root harmonic threshold 252건, 2진 위상주기 16행과 반모형
242개, Twin 임계값 최초 교차까지 연분수 39개다. 실패 계수는 0이다.

## C. 리만 가설 — 정확한 선언 명제

### `AsymmetricReciprocalEnvelopeForScaledJumpMargin`

(E_n\to L>0), (a_n=E_n-L)라 하고

\[
A_+=\limsup n\max(a_n,0),\qquad
A_-=\limsup n\max(-a_n,0)
\]

를 정의한다. (J_n=n(E_n-E_{n+1})),
(S_n=(n+1)E_{n+1}-nE_n)이면

\[
\limsup J_n\le A_++A_-,\qquad
\liminf S_n\ge L-A_+-A_-.
\]

따라서 (A_++A_-<L)이면 결국 양의 lag margin이 생긴다. 두 one-sided
envelope 앞의 계수 1은 동시에 최적이다.

증명은
(a_n-a_{n+1}\le a_n^++a_{n+1}^-)와
(S_n=E_{n+1}-J_n)에서 바로 나온다. 최적성은 짝수 (n)에서
(a_n=P/n), 홀수 (n)에서 (a_n=-M/n)인 계열로 확인한다. 이때
짝수 부분열의 lag는 정확히 (L-P-M)이다. (P+M=L)이면 0이 무한히
나오므로 임계 등호는 충분하지 않다.

이 결과는 대칭 조건
(\limsup n|E_n-L|<L/2)보다 엄밀히 약하다. 하지만 재현한 세 계열은
추상 수열일 뿐 실제 Guinand-Weil packet이 아니다.

- 폐기: 대칭 max-envelope 조건이 rate-only 논증의 최종형이라는 경로.
- 남은 간극: 실제 packet에 대해 (A_++A_-<L)을 증명해야 한다.
- 다음 단일 보조정리:
  `ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit`.

## D. 콜라츠 추측 — 정확한 선언 명제

### `PointwiseWeylCancellationIffExplicitThresholdCutoffDiverges`


\[
W_N(h)=N^{-1}\sum_{j\le N}e^{2\pi i h x_j},\qquad
E_N(H)=\max_{1\le|h|\le H}|W_N(h)|
\]

라 하고

\[
K_N=\max(\{0\}\cup\{1\le H\le N:E_N(H)\le1/H\})
\]

를 둔다. 모든 고정 (h\ne0)에 대해 (W_N(h)\to0)일 필요충분조건은
(K_N\to\infty)이다. (K_N\ge1)이면 정의상
(E_N(K_N)\le1/K_N)이다.

허용되는 (H)들은 initial segment를 이룬다. 고정 harmonic이 모두
소멸하면 임의의 고정 유한 maximum도 소멸하므로 (K_N)은 발산한다.
역은 고정 (h)가 결국 cutoff 안에 들어온다는 사실로 즉시 따른다.
complete (M)-grid에서는 (1\le|h|<M)의 합이 정확히 0이고 (h=M)의
크기는 1이라서 (K_M=M-1)이다.

- 폐기: TICKET-263의 diagonal cutoff를 유한 데이터에서 명시적으로
  선택할 수 없다는 경로.
- 유한 한계: (M=4,8,16,32,64,128) grid는 canonical Fermat-quotient
  prefix가 아니다.
- 다음 단일 보조정리:
  `CanonicalFermatQuotientThresholdCutoffDiverges`.

## E. 강한 골드바흐 추측 — 정확한 선언 명제

### no-go `EveryFixedTwoAdicTieSignatureHasNonTieCountModels`

q=3 특수 prefix에서 tie가 나면 각 비영 residue count는
(M_l=3^{6l+3}+1)이다. 모든 (m\ge1)에 대해 (M_l\bmod2^m)의 최소
level 주기는 (m\le3)이면 1, (m\ge4)이면 (2^{m-3})이다. 그러나
(M_l>2^m)일 때마다

\[
(N_1,N_2)=(M_l-2^m,M_l+2^m)
\]

은 tie와 같은 총합 및 같은 (N_2\bmod2^m)을 가지면서 tie가 아니다.
따라서 총합과 하나의 고정 2진 signature만으로 tie를 판정할 수 없다.

(m\ge3)에서 3의 (2^m) 법 order가 (2^{m-2})이고 level 증가가
지수에 6을 더하므로 주기 공식이 나온다. 이동 쌍은 차이가
(2^{m+1})이므로 같은 합동류를 보존한다.

재현한 (m=1,\ldots,16), (l=0,\ldots,15)의 유효 반모형 242개는
추상 정수 count다. 실제 소수 count로 실현된다는 주장이 아니다.

- 폐기: 어떤 하나의 고정 (2^m) 합동조건을 충분조건으로 승격하는
  경로 전체.
- 남은 간극: 실제 q=3 특수 prime race가 모든 level에서 0이 아님을
  비합동적 추정으로 보여야 한다.
- 다음 단일 보조정리: `Q3SpecialPrimeRaceAbsoluteGapAtLeastTwo`.

## F. 쌍둥이 소수 추측 — 정확한 선언 명제

### `AllSubthresholdUniqueRootConvergentsAreUnitFree`

살아남은 degree-17 branch의 유일 실근 연분수 convergent를 (p_n/q_n),
(V_0=188580743973175296)라 하자. (q_n\le V_0)인 모든 convergent는
(n=0,\ldots,37)이고 어느 것도 (B_1(p_n,q_n)=\pm1)을 만족하지
않는다. 정확히

\[
q_{37}=110221790993960069\le V_0
<q_{38}=309742427372962732.
\]

유리수 root bracket이 첫 39개 연분수 항을 인증한다. 분모 recurrence는
초기 분모 1의 중복 뒤 엄격 증가하며, 0번부터 37번까지 degree-17
정수식을 직접 계산하면 unit hit가 없다. 따라서 뒤의 convergent가
다시 (V_0) 아래로 올 수 없다.

이 결과는 TICKET-263에 남았던 유한 머리 subcase를 완전히 닫는다.
그러나 (n\ge38)의 무한 tail은 닫지 않는다.

- 폐기: 인증한 머리 뒤에 아직 검사하지 않은 subthreshold convergent가
  존재할 수 있다는 경로.
- 다음 단일 보조정리:
  `NoLaterUniqueRootConvergentSatisfiesJointNinthOrderCongruences`.

## G. 적대적 감사와 유한 계산 한계

1. RH 최적성 계열은 실제 Weil packet이 아니다.
2. Collatz cutoff는 명시적이지만 canonical 수열에서의 발산은 미증명이다.
3. Goldbach 반모형은 해당 유한 정보의 불충분성만 증명한다.
4. Twin 39행 계산은 (V_0) 이하만 전부 포괄하며 무한 tail을 포괄하지
   않는다.
5. 이번 유한 계산 어느 것도 원 추측의 무한 명제를 해결하지 않는다.

## H. proof DAG

문제별 JSON의 비순환 DAG는 다음 공통 구조를 가진다.

```text
T263 proved -> T264 proved -> exact replay (computed_finite)
                          -> 폐기 shortcut (disproved)
                          -> 다음 단일 보조정리 (open)
```

각 DAG의 open frontier는 정확히 하나다.

## I. 기계 판정표

| 문제 | 새 결과 | 분류 | 원문제 상태 | 다음 보조정리 |
|---|---|---|---|---|
| RH | 비대칭 one-sided envelope 합의 sharp bound | partial theorem | open_not_proven | `ActualWeilPacketOneSidedReciprocalEnvelopeSumBelowLimit` |
| Collatz | 명시적 threshold cutoff와 fixed-h 소멸의 동치 | partial theorem | open_not_proven | `CanonicalFermatQuotientThresholdCutoffDiverges` |
| Strong Goldbach | 모든 고정 2진 signature의 반모형 | exact no-go | open_not_proven | `Q3SpecialPrimeRaceAbsoluteGapAtLeastTwo` |
| Twin Prime | 임계값 이하 root convergent 전체 unit-free | partial theorem | open_not_proven | `NoLaterUniqueRootConvergentSatisfiesJointNinthOrderCongruences` |

## J. 주장 경계

허용: 위 네 유계 명제, 기호 증명, 명시한 유한 재현, 폐기 경로.

금지: 실제 Weil envelope bound, canonical Fermat-quotient equidistribution,
모든 q=3 special prime-race nonvanishing, 모든 Twin convergent 배제, 또는
네 원 추측 중 하나라도 해결했다는 주장.

## K. 최종 상태

회차는 완료됐지만 연구 프로그램과 네 추측은 모두 미해결이다.
