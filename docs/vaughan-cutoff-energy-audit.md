# TICKET-101: Vaughan cutoff frontier and energy-equivalence audit

## English

TICKET-101 checks whether the TICKET-100 componentwise no-go was merely an artifact of `U=V=100`.

At scale one million, this audit defines its noncollapse balanced grid by `U,V<=N^(1/3)=100`. Goldbach has no separate-budget survivor: the best row is still `U=V=100`, with structured constant `1.5791`, Type II constant `7.9099`, and sum `9.4890`.

Twin Prime behaves differently. The noncollapsed pair `U=100,V=84` has structured constant `1.3890`, Type II constant `0.1711`, and sum `1.5601<1.6`. This corrects the over-broad joint-only continuation from TICKET-100. A concrete all-scale target is

```text
structured >= -1.40 M/log(x),
Type II    >= -0.18 M/log(x).
```

The summed constant `1.58` leaves a small margin below `1.6`, but both inequalities remain unproved.

TICKET-102 correction: `1.6` was a finite calibration threshold, not a necessary mathematical threshold. The `1.40` structured budget is refuted on the post-selection 2M dyadic block. Any fixed finite component constants would be asymptotically sufficient if proved uniformly; see `twin-dyadic-vaughan-holdout.md`.

Goldbach can be made to pass numerically only by moving close to decomposition collapse. In the tested diagonal sequence, `U=V=960=0.96 sqrt(N)` is the first survivor and leaves only 314 nonzero Type II coordinates. At `U=V=1000`, Type II is identically zero and `I=Lambda`; the hard correlation has merely been renamed Type I. This is not an admissible reduction.

TICKET-101 also audits the energy rewrites

```text
C_G = ||Lambda||^2 - ||Lambda-J_N Lambda||^2/2,
2C_2 = ||Lambda_left||^2 + ||Lambda_shift2||^2
       - ||Lambda_left-Lambda_shift2||^2.
```

They make the contrapositive geometric: a Goldbach counterexample or finite Twin set forces near-maximal mismatch. However, the desired mismatch bound is algebraically equivalent to the original correlation lower bound. It is useful only if a separate reflection/shift theorem supplies new information.

## 한국어

TICKET-101은 TICKET-100의 `U=V=100` 결론을 모든 cutoff로 성급하게 일반화하지 않도록 검사합니다.

이번 감사가 비붕괴 균형 범위로 사전 정의한 `U,V<=N^(1/3)`에서 Goldbach 분리 예산은 모두 실패합니다. 반면 Twin은 `U=100,V=84`에서 구조항 `1.389`, Type II `0.171`, 합 `1.560<1.6`인 후보가 살아납니다. 따라서 Goldbach는 이 범위에서 결합 부호 정리가 필요하지만 Twin은 두 성분을 별도로 증명하는 더 구체적인 후보 경로가 생겼습니다.

Goldbach도 `U,V`를 제곱근 가까이 키우면 수치상 통과하지만 Type II가 거의 사라집니다. `U=V=1000`에서는 Type II가 완전히 0이고 `I=Lambda`가 되므로 어려운 문제를 Type I이라는 이름으로 옮긴 것뿐입니다.

reflection/shift mismatch 에너지 표현은 대우법을 직관적으로 보여주지만 원래 correlation 하한과 정확히 동치입니다. 독립적인 mismatch 정리가 없다면 새로운 reduction이 아닙니다. 네 난제는 모두 미해결입니다.

TICKET-102 교정: `1.6`은 필수 증명 문턱이 아니라 유한 보정값이었습니다. 구조항 `1.40` 후보는 독립 2M 구간에서 반박됐습니다. 전 규모에서 증명할 수 있다면 어떤 고정 유한 상수도 충분합니다.

## Reproduce / 재현

```text
D:\python\anaconda3\python.exe scripts\ticket101_vaughan_cutoff_energy_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket101_vaughan_cutoff_energy_audit
```
