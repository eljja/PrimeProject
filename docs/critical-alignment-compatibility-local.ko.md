# TICKET-259: 임계 문턱, 정렬 위상, 정확 호환성, 국소 합동 no-go

일자: 2026-08-31
상태: 네 모 추측 모두 `open_not_proven`
심층 트랙: 강한 골드바흐 추측

이번 회차는 정확한 경로 no-go 세 개와 부분정리 하나를 확립했다. 네 모 추측 가운데 증명되거나 반증된 것은 없다. 표준 기계 기록은 `data/open-problem/ticket259-critical-alignment-compatibility-local.json`이며, 각 트랙에는 open frontier가 하나뿐인 비순환 proof DAG가 있다.

## 리만 가설

### 선언 명제

`CriticalScaledDownwardJumpEqualityNoGo`. 양의 수열 \(E_L\to1\) 중 총변동이 \(2/3\)이고
\[
\sup_{n\ge1}n(E_n-E_{n+1})_+=1
\]
이지만 \(S_n=(n+1)E_{n+1}-nE_n<0\)인 \(n\)이 무한히 많은 수열이 존재한다.

\(E_{4^k+1}=1-4^{-k}\), 그 밖에는 \(E_L=1\)로 둔다. 고립된 하강·반등의 합은 \(2\sum_{k\ge1}4^{-k}=2/3\)이다. \(n=4^k\)에서 scaled drop은 정확히 1이고
\[
S_n=(n+1)(1-1/n)-n=-1/n
\]
이다. 12개 유리수 행은 모든 \(k\)에 대한 닫힌식의 재생 검사이지 유한 계산의 무한 외삽이 아니다.

확립: 비엄격 임계 부등식은 추상 packet 모형에서 부족하다.
폐기: 실제 Weil margin의 엄격 부등식을 등호 허용 부등식으로 완화하는 경로.
남은 간극: 실제 Guinand-Weil 계수에는 어떤 추정도 얻지 못했으며 RH도 미해결이다.
다음 단일 보조정리: `ActualWeilPacketMarginStrictlyDominatesScaledDownwardVariation`.

## 콜라츠 추측

### 선언 명제

`DistinctPrimePhaseAlignmentLinearGrowthNoGo`. \(q_j\)를 5 이상인 \(j\)번째 소수, \(z_j=e^{2\pi i/q_j}\)라 하자. TICKET-258의 서로 다른 소수 차수 유리 선형독립 조건을 만족하지만
\[
N^{-1}\sum_{j\le N}z_j\to1
\]
이다. 따라서 차수의 상이성·비자명성·유리 선형독립만으로 sublinear phase sum을 얻을 수 없다.

현 길이 부등식과 \(\pi<4\), \(q_j\ge j+4\)에서
\[
\left|N^{-1}\sum_{j\le N}z_j-1\right|
\le {8\over N}\sum_{j\le N}{1\over q_j}
\le {8H_N\over N}\to0.
\]
재생은 부동소수점 원시근 대신 5부터 997까지 166개 소수의 정확 유리수 envelope를 쓴다.

확립: 이전 구조 조건을 모두 만족하면서 선형 크기로 정렬되는 반례군.
폐기: conductor 자료와 유리 선형독립만으로 cancellation을 도출하는 경로.
남은 간극: canonical Fermat quotient 지수 \(D_q\)의 분포와 콜라츠 추측은 미해결이다.
다음 단일 보조정리: `CanonicalFermatQuotientPhasePrefixSumsHaveSublinearMagnitude`.

## 강한 골드바흐 추측

### 선언 명제

`QDivisibleCompatibilityIffTwoModuloFourAndQ13Certificate`. 홀수 소수 \(q\), \(m=qs>0\)에 대해 \((1-X)^m\bmod(X^q-1)\)의 순환계수를 \(c_r\), \(t=1-c_0\)라 하자. 그러면
\[
t>0,\qquad c_r+t\ge0\quad(0\le r<q)
\]
일 필요충분조건은 \(s\equiv2\pmod4\)이다. 또한 첫 새 사례 \((q,m)=(13,26)\)의 유일한 강제 소수 prefix는 정확 계산으로 배제된다.

TICKET-256에 의해 호환성은 \(m\)이 짝수임을 강제하므로 \(s=2k\)이다. \(a\ne0\)에 대해 root filter는
\[
(1-\zeta_q^a)^m=(-1)^k|1-\zeta_q^a|^m
\]
를 준다. \(k\)가 짝수이면 \(c_0\)는 양의 정수라 \(t\le0\)이다. \(k\)가 홀수이면 \(c_0<0\)이고
\[
c_r-c_0={1\over q}\sum_{a=1}^{q-1}|1-\zeta_q^a|^m
(1-\cos(2\pi ar/q))\ge0.
\]
따라서 \(t>0,\ c_r+t\ge1\)이다. 이는 무한 분류 정리이며, \(3\le q\le43,\ 1\le s\le16\)의 208행은 재생 검사다.

\((13,26)\)에서 강제 길이는 \(T=135,207,787\), 정확한 \(T\)번째 소수는 \(2,798,637,773\)이다. 조합적 잔여류 벡터 소수계수법과 독립적인 직접 segmented sieve가 같은 13개 정수 벡터를 냈다. 실제 reflection difference는
\[
(0,-887,1284,71,-135,-341,-462,462,341,135,-71,-1284,887)
\]
이고, \(\Phi_{12}\)에 대한 primitive odd-character remainder는
\[
(-958,1746,-64,-121)\ne0
\]
이다. 따라서 이 강제 대칭 prefix는 실제 첫 \(T\)개 소수의 잔여류 벡터가 아니다.

확립: 무한 호환성 분류와 독립 재현된 1억 3천5백만 소수 규모의 한 prefix 배제.
폐기: 호환성을 설명 없는 유한 scan 현상으로 취급하는 경로.
남은 간극: 모든 \(q\)와 \(s\equiv2\pmod4\)에 대한 odd-character nonvanishing 및 강한 골드바흐는 미해결이다. 유한 인증서를 귀납적으로 승격할 수 없다.
다음 단일 보조정리: `EveryTwoModuloFourQDivisiblePrimePrefixHasNonzeroOddCharacterMoment`.

## 쌍둥이 소수 추측

### 선언 명제

`FiniteCongruenceFixedRootWindowNoGo`. TICKET-258의 17차 형식 \(B_1(u,v)\)에 대해, 모든 \(M\ge2\)와 모든 유리 열린구간 \(I\subset(-1,0)\)에는
\[
v>0,\quad u/v\in I,\quad \gcd(u,v)=1,\quad
u^2-2v^2<0,\quad B_1(u,v)\equiv1\pmod M
\]
인 쌍이 무한히 많다.

유한 개 modulus의 최소공배수를 \(M\)이라 하고 \(v=M^N\)으로 둔다. 큰 \(N\)에서 \(vI\)의 길이는 \(M\)보다 커서 \(u\equiv1\pmod M\)인 정수를 포함한다. 그러면 \(\gcd(u,v)=1\), \(|u/v|<1\)이므로 norm은 음수이며, \(B_1\)의 선두항 외 모든 항은 \(v\)를 포함한다. 따라서 \(B_1(u,v)\equiv u^{17}\equiv1\pmod M\)이다. 재생은 \(M=2,\ldots,31\)의 증인을 정확 정수로 구성한다.

확립: 고정된 유한 합동 조건과 고정 window마다 무한한 primitive admissible 국소 증인이 존재한다.
폐기: 고정 합동식과 고정 구간만으로 지수 17 분기를 닫는 경로.
남은 간극: scale-dependent \(v^{-17}\) 근사와 모든 convergent의 배제, 쌍둥이 소수 추측은 미해결이다. 가변 modulus 논법은 no-go의 대상이 아니다.
다음 단일 보조정리: `EveryUniqueRootConvergentMissesUnitCoefficient`.

## 재현과 판정 경계

```powershell
python scripts/ticket259_critical_alignment_compatibility_local.py
python -m unittest tests.test_ticket259_critical_alignment_compatibility_local
python scripts/verify_ticket259_structure.py
```

두 소수 잔여류 알고리즘은 정확한 정수 벡터를 반환한다. 회차 완료는 계산·테스트·JSON·한영 문서·Pages가 일치한다는 뜻일 뿐, 모 추측 해결을 뜻하지 않는다.
