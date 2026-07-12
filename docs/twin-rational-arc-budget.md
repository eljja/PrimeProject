# TICKET-110: Twin rational major-arc budget

## English

TICKET-110 replaces the single origin-centered band from TICKET-109 with a fixed arithmetic mask. For each denominator cutoff `Q`, the major arcs are centered at every reduced fraction `a/q in [0,1/2]`, `q<=Q`, with width

```text
|alpha-a/q| <= Q/(qX).
```

The centers and widths are fixed before reading any target contribution. This prevents selecting only bins that happened to contribute positively.

The discrete spectrum is partitioned exactly into the union of these major bins and the minor complement. At `X=1,048,576`, the best audited cutoff is `Q=32`:

- exact symmetric correlation: `459,139.9`;
- major phase contribution: `461,203.6`;
- actual minor phase contribution: `-2,063.7`;
- minor spectral energy: `3,105,699.1`;
- trivial minor lower bound: `-3,105,699.1`;
- resulting rigorous total lower bound: `-2,644,495.5`.

Thus the arithmetic major arcs recover nearly all of the observed correlation, but this is not a proof. The actual minor contribution is only about `-6.64e-4` of minor energy, while the trivial absolute-energy estimate loses that cancellation completely. Every audited horizon refutes closure by the trivial minor bound.

The next target is `FixedBumpMajorArcAsymptoticWithTypeIIMinorPowerSaving`: derive the major-arc main term with explicit local factors and prove a signed Type II power saving for the minor arcs. The required estimate must be independent of the observed target correlation.

## 한국어

TICKET-110은 원점 저주파 하나 대신 모든 기약분수 `a/q`, `q<=Q` 주변에 폭 `Q/(qX)`인 major arc를 사전에 고정합니다. 관측 후 양수인 bin만 선택하지 못하도록 중심과 폭은 목표 기여를 읽기 전에 결정됩니다.

1,048,576에서 최선의 `Q=32`는 실제 상관 `459,139.9` 중 major 기여 `461,203.6`을 포착하고 minor 실제 기여는 `-2,063.7`입니다. 그러나 minor 에너지는 `3,105,699.1`이므로 절댓값만 이용한 하한은 전체를 `-2,644,495.5`까지 떨어뜨립니다.

즉 major arc 선택은 올바른 산술 구조를 포착하지만 그것만으로 증명이 되지는 않습니다. 실제 minor 기여는 minor 에너지의 약 `-6.64e-4`에 불과하므로, 이 강한 상쇄를 독립적인 Type II 정리로 증명하는 것이 핵심입니다.

다음 목표는 `FixedBumpMajorArcAsymptoticWithTypeIIMinorPowerSaving`입니다. 명시적 국소 인자를 가진 major-arc 주항과 signed minor-arc power saving을 함께 증명해야 합니다. 네 난제는 아직 미해결입니다.
