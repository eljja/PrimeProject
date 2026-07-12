# TICKET-92: Scale-sensitive proof thresholds

## Status

TICKET-92 proves a restricted Collatz coordinate equivalence, rejects two target-erasing proof routes, and corrects a false Maynard-threshold promotion in the Twin Prime track. It proves none of the four open conjectures.

한국어: TICKET-92는 콜라츠의 상수 비트 사건을 보존하는 좌표를 만들고, 쌍둥이 소수 트랙의 잘못된 Maynard 임계값을 교정한다. 네 난제의 증명이나 반례는 아니다.

## Collatz: the missing information is second order

Let `R` solve `3^(R+1)=-7` in the relevant odd 2-adic exponent class. At consecutive top-bit heights `H<J`, put `k=r_H` and `L=J-H-1`. Then

```text
v2(R-k) = J,
Delta_H = v2(R-k)-floor(log2(k)) = J-H = L+1,
v2(3^(k+1)+7)-floor(log2(k)) = Delta_H+2.
```

Therefore the required `100` event is exactly

```text
Delta_H >= 3.
```

The normalized approximation exponent is

```text
mu_H = v2(R-k)/H = 1 + Delta_H/H.
```

For every bounded digit defect, including both `Delta=1` and the target `Delta>=3`, this tends to one. A first-order irrationality exponent therefore deletes the distinction being proved. An explicit aperiodic concatenation of the no-`00` blocks `10` and `110` has defects only in `{1,2}` and the same limiting exponent one.

한국어: 필요한 정보는 근사 지수의 극한이 아니라 나누기 전에 남는 상수항 `Delta_H`다. `H`로 나누면 목표 비트 두 개가 `O(1/H)`로 사라지므로, 일반적인 무리수 지수나 초월성만으로는 `00`을 강제할 수 없다.

The corrected Collatz target is:

```text
FixedLogSecondOrderDefectRecurrence:
Delta_H >= 3 for infinitely many nested top-bit prefixes.
```

Finite recurrence counts below height 262,144 are implementation and falsification evidence only.

## Twin Prime: Maynard threshold correction

The legacy TP-TICKET-14 artifact compared an unverified closed-form score with `2/k` and converted the first passing admissible-tuple diameter into an “implied bounded gap,” including gap 2 at `k=2`. This is not Maynard's criterion.

Maynard's Proposition 4.2 gives at least

```text
ceil(theta M_k / 2)
```

prime entries in an admissible `k`-tuple. With the unconditional Bombieri-Vinogradov input `theta<1/2`, a two-prime conclusion requires a rigorously certified strict `M_k>4` in the limiting threshold. The stored closed-form scores were not evaluations of the defining variational integrals `I_k(F)` and `J_k^(m)(F)` and therefore were not certified `M_k` lower bounds at all.

The corrected artifact now:

- labels the old values as legacy surrogate scores;
- records no certified `M_k` rows;
- records no certified two-prime criterion;
- sets every implied gap and `smallest_bounded_gap` to null;
- retains finite Selberg and density calculations only as diagnostics.

한국어: `k=2`에서 두 위치가 동시에 소수임을 무한히 보이면 그것이 바로 쌍둥이 소수 추측이다. 검증되지 않은 점수가 작은 임계값을 넘었다는 이유로 gap 2를 얻었다고 표시하는 것은 순환 논증이었다. 이 승격을 제거했다.

Primary reference: [James Maynard, “Small gaps between primes,” Annals of Mathematics 181 (2015), Proposition 4.2](https://doi.org/10.4007/annals.2015.181.1.7).

The retained Twin Prime target remains a parity-breaking exact-pair correlation lower bound. A valid Maynard variational certificate can prove bounded gaps for a sufficiently large tuple, but it does not isolate exact gap 2.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket92_scale_sensitive_threshold_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket92_scale_sensitive_threshold
```
