# TICKET-111: Twin Type II minor-arc phase audit

## English

TICKET-111 connects the rational major/minor split from TICKET-110 to the exact Vaughan decomposition. With the fixed bump and `Q=32`, it writes the shift-two correlation as

```text
correlation = <Type I, shifted Lambda> + <Type II, shifted Lambda>
```

both globally and on the fixed minor mask. The component identities reconstruct to numerical error below the registered tolerance through the fresh `X=2,097,152` holdout.

The first result is a finite no-go theorem for a clearly defined proof class. Suppose the fixed minor bins are partitioned arbitrarily and Cauchy-Schwarz is applied independently on each cell while all complex phase information is discarded. Every such envelope is at least the singleton-bin envelope

```text
E_bin(X) = sum_minor m_k |TypeII_hat(k)| |Lambda_hat(k)| / N.
```

Even this smallest phase-blind partition envelope leaves a negative total lower bound on all five audited horizons. At 2M, the known major-plus-Type-I-minor contribution is `929,258.9`, while `E_bin=7,596,484.2`, giving `-6,667,225.4`. Refining the partition therefore cannot repair this class of argument. The estimate must retain bilinear phase.

A candidate lower inequality was then frozen after the rows at or below 1M:

```text
TypeII_minor(X) >= -X^(-1/6) E_bin(X).
```

The exponent is motivated by square-root cancellation over the Vaughan outer scale `U(X) approximately X^(1/3)`. On the first post-selection holdout at 2M, the actual Type II minor contribution is `+14,783.4`, the candidate envelope is `671,440.7`, and the resulting certified finite lower expression is `257,818.2`. This is a successful falsification test, not a theorem: one holdout cannot establish the inequality for all sufficiently large `X`.

The retained target is `PhaseAwareVaughanTypeIIMinorArcPowerSaving`. It must derive a uniform signed estimate from the Vaughan coefficients and rational frequency separation without using the observed target correlation.

### Literature boundary

Vaughan Type II sums, rational minor arcs, smoothing, and large-sieve estimates are established. Helfgott develops explicit minor-arc bounds and methods for reducing the cost of Vaughan's identity in ternary Goldbach. Ford and Maynard show in a general prime-producing sieve framework that substantial Type I and Type II information must be used together. Neither result directly supplies a binary shift-two lower bound for this exact cross-spectrum.

- Harald A. Helfgott, [Minor arcs for Goldbach's problem](https://arxiv.org/abs/1205.5252).
- Kevin Ford and James Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368).

## 한국어

TICKET-111은 TICKET-110의 유리수 major/minor arc 분할과 정확한 Vaughan 분해를 연결합니다. 고정 bump와 `Q=32`에서 전체 상관을 `Type I`과 `Type II`가 이동된 von Mangoldt 함수와 만드는 두 교차 스펙트럼으로 정확히 나눕니다.

첫 결과는 명확히 제한된 증명 방식에 대한 유한 no-go 정리입니다. minor 주파수를 어떤 방식으로 나누더라도 각 구간에서 Cauchy-Schwarz를 적용하고 복소 위상을 버리면, 그 경계는 주파수 한 칸씩 나눈 `E_bin`보다 작아질 수 없습니다. 하지만 200만에서 major와 Type-I minor를 합친 알려진 양은 `929,258.9`인 반면 `E_bin`은 `7,596,484.2`이므로 하한이 `-6,667,225.4`입니다. 주파수 구간을 더 정교하게 나누는 것만으로는 해결되지 않으며 Type-II의 위상 상쇄를 보존해야 합니다.

1M 이하 탐색 뒤 `TypeII_minor >= -X^(-1/6) E_bin` 후보를 고정하고 새로운 2M holdout에서 검사했습니다. 실제 Type-II minor는 `+14,783.4`, 후보 envelope는 `671,440.7`, 결과 하한은 `257,818.2`로 양수입니다. 그러나 이는 유한 반증 시험을 한 번 통과한 것이지 무한 정리가 아닙니다.

다음 목표는 `PhaseAwareVaughanTypeIIMinorArcPowerSaving`입니다. 관측된 쌍둥이 소수 상관을 가정하지 않고 Vaughan 계수와 유리 주파수 분리를 이용해 모든 충분히 큰 `X`에 대해 부호 있는 절약을 증명해야 합니다. 네 난제는 여전히 미해결입니다.

## Reproduce / 재현

```text
D:\python\anaconda3\python.exe scripts\ticket111_twin_typeii_minor_phase_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket111_twin_typeii_minor_phase_audit
```
