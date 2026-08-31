# TICKET-262: 정확한 limsup 문턱, 유한 조화성분 no-go, mod-8 동률 장애물, 3차 합동

상태: **회차 완료. 리만 가설, 콜라츠 추측, 강한 골드바흐 추측, 쌍둥이 소수 추측은 모두 미해결·미증명이다.**

이번 회차는 부분정리 3개와 정확한 경로 no-go 1개를 확립했다. 네 상위 추측 중 증명되거나 반증된 것은 없다. 정준 기계 기록은 `data/open-problem/ticket262-limsup-finiteharmonic-mod8-thirdorder.json`이다.

| 문제 | 이번 정확 명제 | 새 결과 | 결과 분류 | 해결 상태 | 폐기/보류 경로 | 유한 계산 한계 | 남은 간극 | 정체 횟수 | 다음 단일 보조정리 |
|---|---|---|---|---|---|---|---|---:|---|
| 리만 가설 | packet lag의 양의 margin과 scaled signed jump의 정확 문턱을 특성화 | `liminf S_n=L-limsup J_n`; 양의 margin iff `limsup J_n<L` | `partial_theorem` | `open_not_proven` | 더 강한 합 가능성을 최소 추상 목표로 삼는 경로 폐기; 실제 Weil 산술은 보류 | strict 64행, critical 12행; 실제 Weil packet 없음 | 실제 packet에서 strict limsup 부등식 | 0 | `ActualWeilPacketScaledDownwardJumpLimsupBelowLimit` |
| 콜라츠 | 어떤 고정 유한 Weyl cutoff가 angular discrepancy 0을 강제하는가 | 모든 고정 유한 cutoff에 대한 prime-modulus 반례족 | `exact_no_go` | `open_not_proven` | 고정 유한 조화성분 shortcut 폐기; 정준 전 조화성분 문제 보류 | `H=1,2,4,8,16`, 위상 1,152개 재현; 구성 자체는 전 `H` 증명 | 정준 Fermat quotient 각도의 모든 비영 조화성분 | 0 | `CanonicalFermatQuotientWeylSumsVanishForEveryNonzeroH` |
| 강한 골드바흐 | 특수 q=3 동률이 강제하는 더 약한 정확 합동은 무엇인가 | 동률이면 `N_2=4 mod 8`, `v_2(N_2)=2`; 두 sharpness 모델 | `partial_theorem` | `open_not_proven` | product `-1`을 비동률의 필요조건으로 보는 경로 폐기 | 실제 `l=0,1,2` 세 단계뿐 | 모든 실제 특수 prefix에서 `N_2 != 4 mod 8` | 0 | `Q3SpecialMinusOneResidueCountNeverFourModuloEight` |
| 쌍둥이 소수 | exponent-17 가지의 양방향 3차 합동 필요조건 | mod `v^3`, mod `u^3` 합동과 1,024 수렴분수 무통과 인증 | `partial_theorem` | `open_not_proven` | 2차 합동을 최종 finite jet으로 보는 경로 폐기 | 양 부호, 1,024개, 최대 분모 519자리; 뒤 수렴분수는 미통제 | 모든 뒤 수렴분수의 joint 3차 합동 배제 | 0 | `NoUniqueRootConvergentSatisfiesBothThirdOrderCongruences` |

## 재현 계약

```powershell
python scripts/ticket262_limsup_finiteharmonic_mod8_thirdorder.py
python -m unittest tests.test_ticket262_limsup_finiteharmonic_mod8_thirdorder
python scripts/verify_ticket262_structure.py
```

증명에 쓰인 계산은 정수 또는 `Fraction`만 사용한다. 난수와 부동소수점 판정은 없다. 모든 transcript SHA-256은 JSON에 기록된다.

## 1. 리만 가설

### 선언한 정확 명제

실수열 `E_n -> L>0`에 대해

\[
J_n=n(E_n-E_{n+1}),\qquad S_n=(n+1)E_{n+1}-nE_n
\]

로 두면 확장실수 의미에서

\[
\liminf S_n=L-\limsup J_n.
\]

따라서 어떤 `delta>0`, `N`이 존재해 모든 `n>=N`에서 `S_n>=delta`일 필요충분조건은 `limsup J_n<L`이다.

### 논증과 경계 공격

항등식 `S_n=E_(n+1)-J_n`을 직접 전개한다. 수렴하는 수열을 더하거나 빼면 liminf/limsup는 그 극한만큼 이동한다. 따라서 위 식이 성립한다. eventual positive margin이면 `liminf S_n>0`이므로 strict limsup 부등식이 나오고, 역으로 strict gap의 절반을 택하면 eventual margin이 나온다.

정확 재현은 `E_n=1+1/n`, `1<=n<=64`에서 `J_n=1/(n+1)`, `S_n=1`을 확인한다. 임계 반례는 `n=4^k`, `E_n=1`, `E_(n+1)=1-1/n`, `1<=k<=12`에서 `J_n=1`이지만 `S_n=-1/n`임을 확인한다. 따라서 문턱의 등호는 충분하지 않다.

이 정리는 최소 추상 목표를 정확히 고립하지만 실제 Guinand-Weil packet의 strict limsup 부등식을 증명하지 않는다. RH 해결이 아니다.

- Transcript: `1d0e796a1808951ac38617fabf4e338df387ff4653b8c1f9461e2e211b2c2e95`.
- 다음 보조정리: `ActualWeilPacketScaledDownwardJumpLimsupBelowLimit`.

## 2. 콜라츠 추측 — 집중 문제

### 선언한 정확 명제

모든 정수 `H>=1`에 대해 증가하는 홀수 소수 `q_j`와 `1<=d_j<q_j`가 존재하여, 모든 비영 `|h|<=H`에서

\[
\frac1N\sum_{j\le N}e^{2\pi i h d_j/q_j}\to0
\]

이지만 `d_j/q_j`의 star discrepancy는 liminf가 적어도 `1/[4(H+1)]`이다. 따라서 고정된 어떤 유한 Weyl 조화성분 cutoff도 증가 소수 모듈러스의 각도 균등분포를 함의하지 않는다.

### 구성과 증명

`M=H+1`, `r_j=(j-1) mod M`, `y_j=(2r_j+1)/(2M)`으로 둔다. `q_j`는 `max(q_(j-1),j^3,8M)`보다 큰 최소 소수, `d_j=floor(q_j y_j)`로 택한다.

`1<=|h|<=H`이면 `h`는 `M`의 배수가 아니므로 이상적 `M`-block의 위상합은 회전된 완전한 근의 합으로서 0이다. 또한 `0<=y_j-d_j/q_j<1/q_j`이고 chord error는 `8|h|/q_j`보다 작다. `q_j>j^3`이므로 총 오차는 합 가능하며 `N`으로 나누면 0으로 간다.

구간 `[0,3/(4M))`에는 정확히 `r_j=0` cluster만 들어간다. 극한 질량은 `1/M`, 구간 길이는 `3/(4M)`이므로 discrepancy 하한은 `1/(4M)`이다.

이는 모든 고정 `H`에 대한 무한 반례족이다. 다만 정준 Collatz/Fermat-quotient 수열이 아니므로 그 수열의 모든 조화성분 상쇄 여부나 Collatz 자체를 결정하지 않는다.

- 재현: `H=1,2,4,8,16`, 각 32 완전 block, 총 1,152 위상 사례.
- Transcript: `fc9aa7f31e40f14a0005fe7d75fc732aca63add7bee8ff6fa258f4e733f4d023`.
- 다음 보조정리: `CanonicalFermatQuotientWeylSumsVanishForEveryNonzeroH`.

## 3. 강한 골드바흐 추측

### 선언한 정확 명제

`T_l=6*3^(6l+2)+3`이라 하자. 첫 `T_l`개 소수의 비영 mod-3 잔여류 개수가 동률이면

\[
N_2=(T_l-1)/2=3^{6l+3}+1\equiv4\pmod8,
\]

따라서 `v_2(N_2)=2`이다. 대우로 `N_2 != 4 mod 8`이면 동률이 아니다.

### 논증, 반례, 계산 한계

동률이면 유일한 영 잔여류를 제외한 `T_l-1`개가 반씩 나뉜다. `6l+3`은 홀수이므로 `3^(6l+3)=3 mod 8`, 따라서 위 합동과 정확한 2-adic valuation이 나온다.

동률 수를 `m`이라 할 때 `(N_1,N_2)=(m-2,m+2)`는 product residue가 `+1 mod 3`인데도 비동률이다. 따라서 TICKET-261의 product `-1` 인증은 필요조건이 아니다. `(m-8,m+8)`은 `N_2=4 mod 8`인데도 비동률이므로 새 합동도 충분조건은 아니다.

실제 정확 계산 `l=0,1,2`의 `N_2`는 `31,19705,14349967`, mod 8 잔여는 `7,1,7`이다. 각 동률은 배제되지만 세 유한 단계는 전 `l` 정리가 아니다.

- Transcript: `7c60dd5c0e26f01fcd138fba2088f29872ee60b43e25efe5fc6dbad0cce5e00f`.
- 다음 보조정리: `Q3SpecialMinusOneResidueCountNeverFourModuloEight`.

## 4. 쌍둥이 소수 추측

### 선언한 정확 명제

TICKET-257의 17차 동차형식 `B_1(u,v)`에 대해 `uv!=0`, `epsilon in {-1,1}`, `B_1(u,v)=epsilon`이면

\[
u^{17}+17u^{16}v+272u^{15}v^2\equiv\epsilon\pmod{v^3},
\]

\[
256v^{17}+4352uv^{16}+17408u^2v^{15}\equiv\epsilon\pmod{u^3}.
\]

### 증명과 인증 경계

`v` 차수 0,1,2의 계수는 `1,17,C(17,2)*2=272`이고 나머지는 `v^3`으로 나뉜다. 반대쪽 `u` 차수 0,1,2의 계수는 `256,4352,C(17,15)*2^7=17408`이고 나머지는 `u^3`으로 나뉜다. 따라서 두 필요 합동이 나온다.

유일 실근의 인증 연분수 수렴분수 1,024개 각각에 양 부호를 대입했다. 잘린 전개의 잔여를 완전한 정확 `B_1` 값의 잔여와 독립 비교했으며 분모 쪽, 분자 쪽, joint 3차 통과는 모두 0이다. 직접 `B_1=+-1` hit도 없다. 마지막 분모는 519자리이다.

이는 유한 prefix 인증일 뿐 뒤의 무한 수렴분수를 배제하지 못한다. exponent-17 가지와 쌍둥이 소수 추측은 미해결이다.

- Transcript: `50287b950ca162a0f762bbe7b4ba0d0898871947e950e7e1f52168d4f5e197cd`.
- 다음 보조정리: `NoUniqueRootConvergentSatisfiesBothThirdOrderCongruences`.

## Proof DAG와 완료 판정

각 문제의 DAG는 `TICKET-261 결과 -> TICKET-262 정리 -> 유한 인증`, 그리고 `폐기된 shortcut`과 `열린 다음 단일 보조정리`로 갈라진다. 네 DAG 모두 비순환이고 열린 frontier는 하나씩이다.

기계 집계는 exact theorem 4, partial theorem 3, exact no-go 1, candidate resolution 0, conjecture resolution 0, proof DAG 4, next lemma 4이다. `iteration_complete=true`, `program_complete=false`이다.

이번 회차는 완료되었지만 해당 추측은 해결되지 않았다.
