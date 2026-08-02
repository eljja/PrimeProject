# TICKET-185: Spectral Escape, Cycle Exclusion, Factor Horizons, and Integer Granularity

## Abstract

TICKET-185 continues the four open nodes of TICKET-184. It does **not** prove
or disprove the Riemann Hypothesis, the Collatz conjecture, the strong Goldbach
conjecture, or the Twin Prime conjecture. It proves four exact intermediate
statements and corrects a regression in the Collatz proof route.

| Problem | Exact result | Status |
|---|---|---|
| Riemann | `TwoNeutralMomentAutocorrelationSpectralEscapeNoGo` | exact model no-go; RH open |
| Collatz | `SingleValuationOneOtherwiseTwoCycleExclusion` | one infinite cycle stratum excluded; Collatz open |
| Goldbach | `TargetSpecificGoldbachFactorHorizonEquivalence` | exact finite threshold; Goldbach open |
| Twin Prime | `IntegerGranularityAndOneSidedBlockCertificate` | exact certificate correction; Twin Prime open |

“New result” means newly established inside PrimeProject. No literature-priority
claim is made without independent expert review. Every finite calculation below
checks an explicitly stated identity or bounded dataset; none is promoted to an
infinite arithmetic conclusion.

## 1. Reproduction contract

```powershell
D:\python\anaconda3\python.exe scripts\ticket185_spectral_cycle_factor_granularity.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket185_spectral_cycle_factor_granularity -v
```

Canonical machine artifact:

`data/open-problem/ticket185-spectral-cycle-factor-granularity.json`

Expected machine ledger:

```json
{
  "exact_theorem_count": 4,
  "rejected_target_count": 4,
  "proof_dag_count": 4,
  "finite_arithmetic_diagnostic_count": 4,
  "decisive_route_correction_count": 3,
  "conjecture_resolution_count": 0,
  "total_failure_count": 0
}
```

## 2. Riemann Hypothesis

### 2.1 Declared proposition

Work in the following explicit logarithmic autocorrelation model. Fix `A>0`
and impose two neutral linear conditions on `g in L2([-A,A])`:

```text
integral g(x)e^(x/2) dx  = 0,
integral g(x)e^(-x/2) dx = 0.
```

There is a normalized sequence of compactly supported positive-definite
autocorrelations

```text
F_M = g_M * tilde(g_M),   F_M(0)=1,
```

whose Fourier probability measures escape every fixed compact frequency
interval. Therefore compact support, positive definiteness, normalization, and
these two neutral moments do not imply uniform Fourier-tail tightness.

### 2.2 Proof

Let

```text
h_M(x) = 1_[-A,A](x) cos(Mx)
```

and let `P` be the orthogonal projection onto
`span{e^(x/2),e^(-x/2)}`. Set

```text
g_M = (I-P)h_M.
```

The two neutral moments vanish by construction. The projection coefficients
tend to zero by the Riemann-Lebesgue lemma, while

```text
||h_M||_2^2 = A + sin(2MA)/(2M)
```

stays bounded away from zero. The normalized autocorrelation is positive
definite and supported in `[-2A,2A]`. Its Fourier density is

```text
|hat(g_M)(xi)|^2 / ||g_M||_2^2.
```

The two cosine sidebands move to `+M` and `-M`. The vanishing projection cannot
retain a positive amount of mass in any fixed frequency band, proving spectral
escape.

### 2.3 Reproducible diagnostic

For `A=1` and the fixed band `[-4,4]`:

| Carrier `M` | normalized low-band mass | mass outside the band |
|---:|---:|---:|
| 8 | recorded in JSON | recorded in JSON |
| 16 | recorded in JSON | recorded in JSON |
| 32 | recorded in JSON | recorded in JSON |
| 64 | `0.0005611473` | `0.9994388527` |

Both neutral residuals are below `1e-12` in every replay. Quadrature is used
only to display the rate; spectral escape follows from the analytic argument.

### 2.4 Rejected route and remaining gap

Discard:

- deriving compactness from support, positive definiteness, normalization, and
  only the two displayed neutral moments;
- treating an autocorrelation model as though it were already the complete
  Weil quadratic form.

This does not prove that every technical realization of the full Weil test cone
contains the counterfamily. It does show that TICKET-184's proposed uniform-tail
route needs an additional coercive premise rather than another compactness
assertion.

**Next lemma:**
`WeilQuadraticFormCoercivityModuloSpectralTranslationsOnExplicitPoleNeutralCore`.

The lemma must estimate the actual arithmetic quadratic form and explicitly
control or quotient spectral translation. Connes and Consani's review of a
failed Weil-positivity attempt is relevant context, not a missing premise
([The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368)).

## 3. Collatz conjecture

### 3.1 Declared proposition

No positive accelerated Collatz cycle has a primitive valuation period with
exactly one valuation equal to one and all remaining valuations equal to two.
After cyclic rotation, every such word has the form

```text
w_h = (1,2,...,2),  h>=3.
```

It is contracting, but its affine numerator and cycle denominator are coprime.

### 3.2 Proof

The initial valuation-one step is followed by `h-1` iterations of
`x -> (3x+1)/4`. Direct iteration gives

```text
B_h = 2*4^(h-1) - 3^(h-1),
D_h = 2*4^(h-1) - 3^h.
```

Hence

```text
B_h-D_h = 2*3^(h-1).
```

The denominator `D_h` is odd and is congruent to two modulo three. Therefore

```text
gcd(D_h, 2*3^(h-1)) = 1,
gcd(B_h,D_h) = 1.
```

For `h>=3`, `D_h>=5`, so `D_h` cannot divide `B_h`. Exact affine divisibility
is necessary for a positive cycle. This excludes the entire infinite family,
not merely the replayed horizons.

### 3.3 Computation and route correction

The formulas were replayed at horizons `3,4,8,16,32,64,128`; the final
denominator has 255 bits, every gcd is one, and there are zero divisibility
hits.

TICKET-184 proposed

```text
EveryPositiveOddIntegerAboveOneHasAnAcceleratedIterateBelowItsStart
```

as the next lemma. TICKET-172 had already proved that statement equivalent to
the full Collatz conjecture by strong induction. It is therefore not a smaller
auxiliary lemma. TICKET-185 restores a strict partial target rather than hiding
the original conjecture under a new name.

The result does not address words containing two or more ones, valuations at
least three, or the divergent-orbit branch. Recent finite exponent-code work
also labels its conclusions as diagnostics rather than a Collatz proof
([Kramer, 2026](https://arxiv.org/abs/2607.10041)).

**Next lemma:**
`NoPrimitiveContractingValuationWordWithExactlyTwoOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility`.

## 4. Strong Goldbach conjecture

### 4.1 Declared proposition

For an even target `N>=6`, consider unordered odd pairs

```text
a + (N-a) = N,  3<=a<=N/2.
```

Let `P^-(m)` be the least prime factor of `m`. For every pair that is not
prime-prime, define its rejection gate

```text
gamma_N(a) = min(P^-(a),P^-(N-a)),
```

and set

```text
tau_N = max gamma_N(a)
```

over all bad pairs, with the convention `tau_N=0` when the bad-pair set is
empty. For `y>=0`, sieving both endpoints by all primes at most `y` leaves
only prime-prime pairs if and only if `y>=tau_N`.

### 4.2 Proof

A pair survives depth `y` exactly when both least prime factors exceed `y`.
A bad pair is removed exactly when `y` reaches its rejection gate. Taking the
maximum gate proves both directions. If the bad set is nonempty, then at
`y=tau_N-1` a maximizing bad pair survives, while at `y=tau_N` every bad pair
is removed. If it is empty, `tau_N=0` makes the equivalence immediate.

At least one endpoint of a bad pair is composite. Its least factor is at most
the square root of that endpoint. If the other endpoint is a smaller prime, it
only lowers the minimum. Thus `tau_N` is at most square-root scale.

### 4.3 Finite horizon audit

| `N` | `tau_N` | `tau_N/sqrt(N)` | prime survivors at `tau_N` |
|---:|---:|---:|---:|
| 100 | 7 | 0.700 | 5 |
| 500 | 19 | 0.850 | 12 |
| 1,000 | 29 | 0.917 | 24 |
| 5,000 | 67 | 0.948 | 71 |
| 10,000 | 89 | 0.890 | 125 |
| 50,000 | 223 | 0.997 | 440 |

Every audited target has at least one bad survivor immediately below the
horizon and zero bad survivors at the horizon. These are bounded exact counts,
not an asymptotic theorem for `tau_N`.

### 4.4 Rejected route and remaining gap

A wheel that reaches `tau_N` has become an exact least-factor decision
procedure for that target. This is useful for verification, but reaching almost
`sqrt(N)` by trial division is not the desired analytic explanation of
Goldbach. The proof route must obtain signed cancellation **below** this
horizon.

**Next lemma:**
`SubHorizonPrimeWeightedBadSurvivorCancellationBelowTargetMargin`.

The recent exceptional-set literature still separates major-arc formulas from
an every-target binary theorem
([Grimmelt-Bhowmik, 2026](https://arxiv.org/abs/2607.27282)).

## 5. Twin Prime conjecture

### 5.1 Declared proposition

Let `C` be a nonnegative integer count in a finite block, let `M>0` be a
proposed main term, and write `R=C-M`. Then

```text
|R|<M  iff  0<C<2M,
R>-M   iff  C>0.
```

Thus symmetric absolute remainder domination is strictly stronger than
positive block mass. If `M<=1/2`, no integer count can satisfy the absolute
certificate.

### 5.2 Proof

Expanding the absolute inequality gives

```text
-M < C-M < M,
0 < C < 2M.
```

The one-sided inequality reduces directly to `C>0`. When `M<=1/2`, the open
interval `(0,2M)` contains no positive integer. This is an exact granularity
obstruction and requires no probabilistic assumption.

### 5.3 Finite block audit

Actual twin starts in `[100000,362144)` were partitioned before counting:

| width | positive blocks | absolute certificates | positive but absolute fails |
|---:|---:|---:|---:|
| 16 | 2,246 | 0 | 2,246 |
| 32 | 2,122 | 0 | 2,122 |
| 64 | 1,876 | 1,498 | 378 |
| 128 | 1,461 | 1,288 | 173 |
| 256 | 940 | 891 | 49 |
| 512 | 508 | 501 | 7 |
| 1,024 | 256 | 256 | 0 |

Across all widths, `4,975` positive blocks fail the symmetric certificate.
Every block with expected mass at most one half fails it, exactly as the theorem
requires. This table calibrates the certificate; it does not predict future
blocks.

### 5.4 Route correction and remaining gap

Positive counts on infinitely many pairwise disjoint blocks are equivalent to
Twin Prime infinitude, not a weaker intermediate theorem. Symmetric error
control adds an unnecessary upper-count condition. The missing input is a
signed one-sided parity estimate on the actual arithmetic remainder.

**Next lemma:**
`CubicRoughOneSidedJointLiouvilleBlockMarginOnUnboundedScales`.

Ford and Maynard show why substantial Type I/II information is necessary in a
general prime-producing lower-bound sieve; this project has not supplied that
input for exact gap two
([On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368)).

## 6. Proof DAG summary

```text
RH T184 finite-moment no-go
  -> two-neutral autocorrelation spectral escape [proved]
  -> actual Weil coercivity modulo translation [open]

Collatz T184 cycle/divergence dichotomy
  -> single-one/rest-two infinite cycle stratum excluded [proved]
  -> exactly-two-ones/rest-two affine divisibility exclusion [open]

Goldbach T184 fixed-wheel impostor
  -> exact target factor horizon [proved]
  -> signed sub-horizon bad-survivor cancellation [open]

Twin T184 positive root sufficiency
  -> integer granularity and one-sided correction [proved]
  -> one-sided joint Liouville block margin [open]
```

## 7. Final boundary

TICKET-185 closes one genuinely infinite Collatz cycle subfamily and proves
three exact route-calibration theorems. It does not establish a zeta zero-free
region, universal Collatz descent, an all-target Goldbach representation, or
infinitely many twin primes. All four statuses remain `open_not_proven`.
