# TICKET-109: Twin spectral phase audit

## English

For the fixed bump from TICKET-108, define `f_X(n)=sqrt(W(n/X)) Lambda(n)` and zero-pad beyond its support. TICKET-109 verifies the exact identity

```text
sum_n f_X(n)f_X(n+2)
  = N^(-1) sum_k |F_X(k)|^2 cos(4 pi k/N).
```

The identity error is below `2.4e-10` through `X=1,048,576`. This Fourier formula is equivalent to the correlation and is not itself a lower-bound theorem.

The tested shortcut keeps one frequency band around zero, uses the exact minimum cosine inside the band, and bounds every outside phase by `-1`. Every tested cutoff fails on all four horizons. At the largest horizon the exact symmetric correlation is `459,139.9`, but the best rigorous single-band lower bound is `-3,338,010.6`.

The phase anatomy explains the failure. Positive-phase energy contributes `1,829,376.5`, negative-phase energy contributes `-1,370,236.6`, and their difference is the target correlation. The cancellation ratio is only `0.1435`. Dropping the shift-two cosine phase or retaining only origin-centered low frequencies destroys the required arithmetic cancellation.

The next target is `RamanujanMajorArcPhaseMarginWithMinorArcControl`: combine rational major arcs near `a/q` with explicit local factors, then prove a separately audited Type II minor-arc remainder. Major/minor arcs and smoothed Type II sums are established background; PrimeProject claims only the reproducible route audit and target specification.

## 한국어

TICKET-108의 고정 bump에 대해 `f_X(n)=sqrt(W(n/X)) Lambda(n)`을 정의하고 지지집합 밖을 0으로 채우면, shift 2 상관합은 Fourier 에너지에 `cos(4 pi k/N)` 위상을 곱한 합과 정확히 같습니다. 1,048,576까지 항등식 오차는 `2.4e-10`보다 작습니다. 그러나 이 변환식 자체는 원래 상관합과 동치이므로 증명 진전으로 세지 않습니다.

원점 주변 저주파 한 구간만 남기고 바깥 위상을 최악값 `-1`로 제한하는 모든 후보는 네 범위에서 실패했습니다. 최대 범위의 실제 상관은 `459,139.9`이지만 최선의 단일 저주파 하한은 `-3,338,010.6`입니다.

양의 위상 기여 `1,829,376.5`와 음의 위상 기여 `-1,370,236.6`의 정밀한 차이가 실제 상관을 만듭니다. 따라서 단순 저주파 집중이나 위상을 버린 양의 스펙트럼 에너지로는 부족합니다.

다음 목표는 `RamanujanMajorArcPhaseMarginWithMinorArcControl`입니다. 유리수 `a/q` 주변 major arc를 명시적 국소 인자와 함께 합치고, 나머지 minor arc에 대해 별도의 Type II 경계를 증명해야 합니다. 이는 아직 쌍둥이 소수 추측의 증명이나 반례가 아닙니다.

## Primary reference

- Harald A. Helfgott, *The Ternary Goldbach Problem*, sections on smoothed Type II sums and major/minor arcs. https://arxiv.org/abs/1501.05438
