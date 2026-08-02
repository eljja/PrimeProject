# TICKET-187: Finite Weil Provenance, Three-One Cycles, Survivor Signatures, and Quantized Intervals

## 1. Claim boundary

TICKET-187 continues the four open nodes of TICKET-186. It proves one new
infinite Collatz cycle-stratum exclusion and three exact certification or
information boundaries. It proves none of the Riemann, Collatz, strong
Goldbach, or Twin Prime conjectures.

| problem | exact TICKET-187 result | discarded or corrected route | next single lemma |
|---|---|---|---|
| Riemann | `PublishedFiniteWeilLDLTProvenanceAndOneSectionNoGo` | promote one reported positive finite block to global Weil positivity | `CofinalPoleNeutralGuinandWeilIntervalLDLCertificatesHaveVanishingNegativeDefect` |
| Collatz | `ExactlyThreeValuationOnesOtherwiseTwoCycleExclusion` | replace all remaining horizons by bounded enumeration | `NoContractingValuationWordWithExactlyFourOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility` |
| Goldbach | `SignedSubhorizonSurvivorSignatureIndistinguishability` | recover lost primality labels by signed or nonlinear reuse of the same roughness bits | `SignedVonMangoldtSubhorizonResidualIsBelowExplicitMajorMainForEveryLargeEvenTarget` |
| Twin Prime | `QuantizedTwinProjectorIntervalRoundingCertificate` | require an analytic lower endpoint of four before using `Delta in 4Z` | `CertifiedStrictlyPositiveTwinProjectorLowerEndpointOnInfinitelyManyPredeclaredDyadicBlocks` |

Reproduce the project-owned results with:

```powershell
D:\python\anaconda3\python.exe scripts\ticket187_positive_ray_threeone_signature_interval.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket187_positive_ray_threeone_signature_interval -v
```

The principal machine artifact is
`data/open-problem/ticket187-positive-ray-threeone-signature-interval.json`.
Every conjecture status is `open_not_proven`.

## 2. Riemann Hypothesis

### 2.1 Declared proposition

The pinned provenance file accompanying Groskin's finite Guinand-Weil work
reports the following interval-`LDL^T` result for the cutoff-free block at
`c=100`, `N=200`:

| field | archived value |
|---|---:|
| dimension | 401 |
| precision | 9,000 bits |
| positive pivots | 401 |
| negative pivots | 0 |
| undetermined pivot | none |
| reported positive definite | true |

TICKET-187 pins the source URL and SHA-256 and checks that these fields are
internally consistent. PrimeProject did **not** rerun the 9000-bit Arb
calculation, so this is a provenance audit of a published certificate rather
than an independent interval proof.

The same archive contains a pole-neutral `c=29`, `N=6` vector. Its two displayed
finite values are positive:

```text
closed-form route  = 0.028981466814873948251427313471228345
source-side route  = 0.028981466814884184353882396894187551
absolute difference = 1.0236102455...e-14
reported source-tail remainder = 1.07788e-12
```

The fields `guard_K` and `guard_g` compare closed forms with numerical
quadrature. They are not interval radii for the quadratic value. Accordingly,
TICKET-187 records this row as a numerical replay, not as a rigorous interval
certificate.

### 2.2 Exact one-section no-go

Even accepting the published finite positive-definiteness certificate, one
finite section does not imply global positivity. For every positive-definite
finite matrix `M`,

```text
diag(M, -1)
```

agrees with `M` on the certified subspace and has a negative orthogonal
direction. Therefore a cofinal nested family plus a valid form-core limit is
essential; no single finite dimension can replace that quantifier.

### 2.3 Remaining gap

The next lemma must produce independently replayable interval `LDL^T`
certificates on one explicit cofinal pole-neutral Guinand-Weil family, with a
certified negative defect tending to zero. Neither the pinned provenance row nor
the positive numerical ray establishes the actual global Weil form or excludes
an off-critical zero.

Primary source: [Groskin, finite Guinand-Weil dictionary and archimedean tail order](https://arxiv.org/abs/2607.02828).
The ancillary package is licensed CC BY 4.0; PrimeProject records selected
fields with attribution and does not imply author endorsement.

## 3. Collatz conjecture

### 3.1 Declared proposition

For the accelerated odd Collatz map, no positive cycle has a valuation period
containing exactly three `1` entries and all other entries equal to `2`. The
statement includes primitive and imprimitive periods.

After cyclic rotation, write the word as

```text
w(a,b,c) = (1, 2^(a-1), 1, 2^(b-1), 1, 2^(c-1)),
a,b,c >= 1, h=a+b+c.
```

Choose the rotation so that `c` is a largest cyclic gap. In the contracting
range `h>=8`, this gives `c>=3`.

### 3.2 Exact affine formula

Direct composition gives

```text
B = 2^(2h-3) - 3^(h-1)
    + 4^a 3^(h-a-1)
    + 2*4^(a+b-1) 3^(c-1),

D = 2^(2h-3) - 3^h.
```

Here `D>0` exactly from `h=8`. Moreover,

```text
B-D = 2*3^(h-1) + 4^a 3^(h-a-1)
      + 2*4^(a+b-1) 3^(c-1) > 0,
```

and both `B` and `D` are odd.

### 3.3 All-horizon upper bound

Put `u=3/4` and `Q=4^h/8`. After division by `Q`, the inequality `B<3D`
reduces to

```text
(8/3)u^(b+c) + (4/3)u^c + (64/3)u^h < 2.       (1)
```

Because `c>=3` and `b+c>=4`, the first two terms are at most

```text
(8/3)(3/4)^4 + (4/3)(3/4)^3 = 45/32.
```

At `h=13`,

```text
(64/3)(3/4)^13 = 531441/1048576 < 19/32,
```

and the term decreases thereafter. Hence (1) holds for every `h>=13`.
If `D` divided `B`, the quotient would be an odd integer strictly between one
and three, which is impossible.

Cyclic rotation loses nothing. If `B_shift` is the numerator after removing the
first valuation `v`, then

```text
2^v B_shift = 3B + D.
```

Since `D` is odd, divisibility by `D` is preserved under rotation.

### 3.4 Finite exception closure

The remaining contracting horizons `h=8,...,12` contain

```text
sum C(h,3) = 56+84+120+165+220 = 645
```

binary valuation words. Exact integer enumeration finds zero divisibility hits.
Each horizon stores a SHA-256 digest of the complete position/remainder
transcript. The finite computation closes only the finite exception left by the
analytic proof; no asymptotic extrapolation is used.

### 3.5 Remaining gap

This is a genuine new infinite cycle-stratum theorem, but it does not handle
four or more valuation-one entries, valuations at least three, or divergent
aperiodic natural-number orbits. The next isolated periodic target is the
exactly-four-one/rest-two family.

## 4. Strong Goldbach conjecture

### 4.1 Declared proposition

Fix an even target `N` with both a prime-pair representation and a bad odd
candidate pair. Define:

```text
tau_N = largest least-factor gate among bad pairs,
rho_N = largest smaller endpoint among prime-pair representations,
sigma_N = min(tau_N, rho_N).
```

For every integer depth `Y<sigma_N`, there is a prime pair and a bad pair with
the same truncated small-factor survivor signature through `Y`.

### 4.2 Proof and stronger no-go

Choose a bad pair attaining `tau_N` and a prime pair attaining `rho_N`. Neither
witness is removed by a trial divisor through a depth below `sigma_N`, so both
signatures are the same all-one vector. Equal feature vectors receive equal
outputs under every deterministic function.

Consequently the obstruction is stronger than the nonnegative-weight result of
TICKET-186: arbitrary signed linear weights, nonlinear classifiers, and any
other post-processing of the unchanged truncated survivor bits still cannot
label both witnesses correctly.

| `N` | `sigma_N` | indistinguishable through `Y` | prime pairs | bad pairs |
|---:|---:|---:|---:|---:|
| 100 | 7 | 6 | 6 | 18 |
| 500 | 19 | 18 | 13 | 111 |
| 1,000 | 29 | 28 | 28 | 221 |
| 5,000 | 67 | 66 | 76 | 1,173 |
| 10,000 | 89 | 88 | 127 | 2,372 |
| 50,000 | 223 | 222 | 450 | 12,049 |
| 100,000 | 311 | 310 | 810 | 24,189 |

These rows use known finite Goldbach representations and therefore prove no new
Goldbach instance. The theorem is an information-sufficiency statement, not an
existence argument.

### 4.3 Remaining gap

The next step must add information absent from the roughness transcript, such
as signed von Mangoldt amplitude or target-aligned phase, and prove that its
uniform residual stays below an explicit positive major term for every
sufficiently large even target. Current exceptional-set results do not provide
that every-target conclusion; see [Grimmelt and Bhowmik](https://arxiv.org/abs/2607.27282).

## 5. Twin Prime conjecture

### 5.1 Declared proposition

On the exact cubic-rough support, let

```text
Delta = A00-A10-A01+A11 = 4C,
```

where `C` is the nonnegative integer twin count in a block. If a certified
closed interval `[L,U]` contains `Delta`, then the exact compatible count range
is

```text
ceil(max(L,0)/4) <= C <= floor(U/4).              (2)
```

Therefore:

1. `L>0` certifies `C>=1`, even if `L<4`;
2. `U<4` certifies `C=0`;
3. `[0,4]` is sharply ambiguous between `C=0` and `C=1`.

### 5.2 Proof

Intersect `[L,U]` with the lattice `4 Z_{>=0}` and divide by four. The
ceiling and floor operations give (2) exactly. Intervals containing only `4`,
only `0`, and both `0` and `4` prove the positive, zero, and sharp ambiguity
statements.

This corrects the analytic target from “prove a lower endpoint at least four”
to “prove a rigorous strictly positive lower endpoint.” Integrality performs
the final promotion to the four-unit arithmetic threshold.

Actual finite cubic-rough ledgers at `X=10^3,10^4,10^5,10^6` are replayed with
half-unit intervals; every interval recovers the exact direct count. These
finite rows are consistency checks, not evidence of infinitely recurring
positive blocks.

### 5.3 Remaining gap

No positive endpoint has been proved on infinitely many unbounded predeclared
blocks. The next lemma remains a parity-sensitive Type I/II estimate, now with
the minimal exact output contract `L_X>0`. Quantized rounding does not supply the
analytic estimate. See [Ford and Maynard, prime-producing sieves](https://arxiv.org/abs/2407.14368).

## 6. Proof DAG and final boundary

```text
RH T186 global Weil nonnegativity target
  -> published finite LDL provenance pinned; not independently rerun [audited]
  -> one finite positive section cannot imply global positivity [proved no-go]
  -> cofinal pole-neutral interval-LDL certificates with vanishing defect [open]

Collatz T186 exactly-three-one target
  -> all exactly-three-one/rest-two cycles excluded [proved]
  -> exactly-four-one/rest-two affine divisibility exclusion [open]

Goldbach T186 signed survivor target
  -> unchanged subhorizon signatures defeat every post-processing rule [proved]
  -> von Mangoldt signed residual below explicit every-target major main [open]

Twin T186 four-unit threshold
  -> exact interval-lattice rounding and [0,4] sharpness [proved]
  -> strict-positive certified endpoint on infinitely many dyadic blocks [open]
```

No complete proof or counterexample has been obtained. The exact new arithmetic
progress is the full three-one Collatz cycle-stratum exclusion. The RH result is
explicitly an external provenance audit plus a finite-section no-go; Goldbach
and Twin Prime receive sharper necessary information and certification
contracts, not existence theorems.
