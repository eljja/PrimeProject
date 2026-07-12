# TICKET-96: Fourier phase information audit

## Status

TICKET-96 converts the TICKET-95 Goldbach and Twin correlation targets into exact finite Fourier coefficients. It then proves information-theoretic countermodels showing why phase-blind minor-arc energy cannot provide the required one-sided lower bound. It does not prove either conjecture.

한국어: TICKET-96은 상관합을 푸리에 공간으로 옮기되, 단순히 표현만 바꾼 것을 진전으로 세지 않는다. 실제로 어떤 정보가 사라지는지 반대모형으로 검사한다. minor arc의 크기만 남기고 위상이나 주파수 위치를 버리면 필요한 양의 하한을 결정할 수 없다.

## Exact discrete Fourier bridges

Let

```text
F(z)=sum Lambda(n) z^n.
```

After zero padding to `M>2(N+2)`, inverse DFT coefficient extraction is exact:

```text
Goldbach: G(N) = coefficient_N F(z)^2,
Twin:     C_2(x) = shift_2 coefficient of |F(z)|^2.
```

For every frequency mask,

```text
target coefficient = major signed contribution + minor signed contribution.
```

The phase-blind fallback is

```text
|minor signed contribution| <= minor Parseval energy.
```

## Why energy alone fails

For Goldbach, keep every minor magnitude `|F_k|` fixed. Conjugate-symmetric phases can align the terms `F_k^2 exp(2 pi i kN/M)` negatively. Thus even per-frequency magnitudes do not determine the required signed coefficient in the unrestricted real-sequence class.

For Twin Prime, total minor energy can be concentrated in conjugate frequency bins where `cos(4 pi k/M)=-1`. The same total energy then gives a negative shift-two coefficient. Frequency placement, not only energy size, is essential.

한국어: 이 반대모형들은 소수로 만든 반례가 아니다. 대신 “에너지 정보만으로 양의 하한을 증명할 수 있다”는 논리 명제의 반례다. 소수에 특유한 산술적 위상 강성, 주파수 국소화 또는 signed Type II 상쇄가 추가되어야 한다.

## Farey-mask audit

At `N=10,000` and `N=100,000`, TICKET-96 tests 36 combinations of denominator cutoff and frequency-window width. A mask is called sparse when it covers at most 10 percent of DFT bins.

- Exact DFT reconstruction is checked against direct Lambda correlations.
- No tested sparse mask certifies the sharp Goldbach contamination budget using minor energy alone.
- No tested sparse mask certifies the sharp Twin contamination budget using minor energy alone.
- Dense, data-dependent masks are not promoted because they increasingly import the exact sampled correlation rather than prove an asymptotic major-arc theorem.

This finite result is a route falsification audit, not a universal theorem about every possible major-arc construction.

## Retained targets

```text
Goldbach: ArithmeticMinorArcPhaseCancellation
Twin:     ShiftTwoSpectralLocalizationOrTypeIICancellation
```

For Goldbach, a useful theorem must prove that the signed binary minor-arc contribution is smaller than the major contribution minus `2 log(N)H(N)` uniformly. For Twin Prime, it must exclude adversarial placement of shift-two spectral energy through arithmetic Type II information.

## Four-problem boundary

- Riemann Hypothesis: only the spectral independent-information gate is transferred; no all-height kernel rigidity theorem is proved.
- Collatz: only the spectral placement gate is transferred; no natural-orbit transition spectrum theorem is proved.
- Goldbach: exact finite Fourier decomposition and an information no-go are proved; uniform arithmetic phase cancellation remains open.
- Twin Prime: exact finite shift-two decomposition and an information no-go are proved; parity-breaking spectral localization remains open.

## Research context

Helfgott's explicit treatment of Goldbach minor arcs shows that a lost logarithmic factor can be decisive, but it concerns the ternary problem rather than the binary lower bound required here: [Minor arcs for Goldbach's problem](https://arxiv.org/abs/1205.5252). Green and Tao explicitly exclude affinely related binary systems such as Twin Prime and Goldbach from their linear-forms asymptotic: [Linear equations in primes](https://annals.math.princeton.edu/2010/171-3/p08). TICKET-96 claims neither result as new; its contribution is the machine-audited finite DFT bridge and explicit phase-information no-go contract.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket96_fourier_phase_information_audit.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket96_fourier_phase_information_audit
```
