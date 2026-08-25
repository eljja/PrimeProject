# TICKET-239: Cancellation, Lifting, Fourier Reflection, and CRT Parity

## Claim boundary

TICKET-239 does **not** prove or disprove the Riemann hypothesis, the Collatz
conjecture, the strong Goldbach conjecture, or the twin-prime conjecture. It
proves four exact intermediate or no-go statements, records bounded
computations separately, and names one remaining lemma per track.

Machine-readable audit:
`data/open-problem/ticket239-cancellation-lifting-fourier-crt.json`.

Reproduce the result with:

```powershell
python scripts/ticket239_cancellation_lifting_fourier_crt.py
python -m unittest tests.test_ticket239_cancellation_lifting_fourier_crt -v
```

## Result summary

| Problem | Exact TICKET-239 result | Rejected route | Status |
|---|---|---|---|
| Riemann | Power-decay Schur threshold; uniformly positive non-summable Gram family | Absolute cross-row summability is necessary | `open_not_proven` |
| Collatz | Local lifting-defect dichotomy and finite-palette criterion | Modulo-prime coincidence automatically controls valuation depth | `open_not_proven` |
| Goldbach | Exact reflection Fourier identity and same-size L2 counterfamily | Window cardinality plus Parseval energy forces positivity | `open_not_proven` |
| Twin prime | Uniform-CRT Gram identity and infinite composite-pair progressions | Maximal local effective rank implies twin-prime mass | `open_not_proven` |

## 1. Riemann hypothesis track

### Declared proposition

Let `H_J` be a Hermitian shell-block matrix with identity diagonal and suppose

```text
||K_ij||_op <= C |i-j|^(-alpha).
```

If `alpha > 1` and `2 C zeta(alpha) < 1`, then uniformly in `J`,

```text
H_J >= (1 - 2 C zeta(alpha)) I.
```

Absolute summability is not necessary. For `0 < C < 1` and
`0 < alpha <= 1`, define

```text
G_J = (1-C)I + C[(1+|i-j|)^(-alpha)].
```

Then `G_J` is a normalized Gram matrix and `G_J >= (1-C)I`, even though its
maximum absolute off-diagonal row sum diverges with `J`.

### Proof

The first assertion is the block Schur estimate followed by
`sum d^(-alpha) = zeta(alpha)`. For the second, use

```text
(n+1)^(-alpha)
  = Gamma(alpha)^(-1) integral_0^1 t^n (-log t)^(alpha-1) dt.
```

Every kernel `[t^|i-j|]` is positive semidefinite. Its positive integral
mixture is therefore positive semidefinite with diagonal one. Adding
`(1-C)I` supplies the uniform lower bound, while the harmonic or subharmonic
row sum diverges.

### What this closes and what it does not

This proves that TICKET-238's absolute row-sum criterion is sufficient but
not necessary. A failed row-sum test is therefore not evidence against Weil
positivity. The construction is abstract: it does not establish cancellation
for arithmetic Guinand-Weil shell blocks and has no implication for a zeta
zero.

**Next lemma:**
`ArithmeticWeilCrossBlockCotlarSteinCancellationBoundOnCofinalLogarithmicShells`.

## 2. Collatz track

### Declared proposition

For an odd prime `q > 3`, put

```text
ell_q = lcm(ord_q(32/27), ord_q(2/3)),
a_q   = v_q(32^ell_q - 27^ell_q),
c_q   = v_q(2^ell_q - 3^ell_q).
```

For every `n >= 1`, `q` is a valuation witness

```text
v_q(D_(ell_q n)) > v_q(B_(ell_q n))
```

if and only if `a_q > c_q`. If `a_q <= c_q`, the prime is disabled on every
multiple of `ell_q`. Hence a finite palette whose local defects
`delta_q = a_q-c_q` are all nonpositive is disabled by one common period.

### Proof

LTE gives

```text
v_q((32/27)^(ell_q n)-1) = a_q + v_q(n),
v_q((2/3)^(ell_q n)-1)   = c_q + v_q(n).
```

After division by `27^k`,

```text
B_k = ((32/27)^k-1) - 2((2/3)^k-1).
```

Unequal valuations take their minimum; equal valuations can only increase
under subtraction. This gives the exact sign dichotomy. Passing to a common
multiple adds the same valuation to both local depths.

### Bounded audit and limit

The generator scans all 17,982 odd primes `5 <= q <= 200,000`. It observes
zero positive defects and zero capped valuations. This is finite evidence,
not a proof for all primes. TICKET-237's modulo-`q` coincidence alone cannot
control valuation depth; the local defect is the missing datum.

**Next lemma:** `RunBlockLocalLiftingDefectNonpositiveForEveryOddPrime`.

Even that lemma would close only the run-block palette target. General
periodic necklaces and aperiodic Collatz descent would remain open.

## 3. Strong Goldbach track

### Declared proposition

For `A subset {0,...,h}`, `M > 2h`, and
`P_A(z)=sum_(a in A) z^a`, let

```text
R_A(h) = #{(a,b) in A^2 : a+b=h}.
```

For an `M`th root of unity `omega`,

```text
R_A(h) = (1/M) sum_(j=0)^(M-1) P_A(omega^j)^2 omega^(-jh).
```

The DC contribution is `|A|^2/M`. Parseval gives
`sum_j |P_A(omega^j)|^2=M|A|`, but cardinality and that global L2 energy do
not force `R_A(h)>0`. If `2|A|-2<h`, the initial segment
`{0,...,|A|-1}` has the same cardinality and Parseval energy and has zero
reflected representations.

### Proof and computation

Root-of-unity orthogonality extracts the coefficient of `z^h` in
`P_A(z)^2`; `M>2h` removes cyclic wraparound. The initial-segment pair sums
are all below `h`, proving the counterfamily.

Twelve exact rows use primes in `[X-h,X]` for
`X in {10^3,10^4,10^5,10^6}` and three even buffer widths at the
`X/(log X)^2` scale. They record the exact DC and signed nonzero-phase terms.
These rows neither prove eventual positivity nor disprove Goldbach.

**Next lemma:**
`MesoscopicPrimeWindowSignedFourierRemainderExceedsNegativeDCWithUniformSlack`.

## 4. Twin-prime track

### Declared proposition

Let `Q` be a finite set of odd primes, `W=product_(q in Q)q`, and sample
`r` uniformly modulo `W`. Center and variance-normalize the local coordinates

```text
1_{r is not congruent to 0 or -2 modulo q}.
```

CRT makes these coordinates mutually orthogonal. Their Gram matrix is the
identity and their effective rank is `|Q|`. Nevertheless, every admissible
class `r mod W` contains infinitely many `n` for which both `n` and `n+2`
are composite.

### Proof

Different prime coordinates are independent under the uniform CRT product
measure. For an admissible `r`, choose distinct primes `ell_1,ell_2` outside
`Q` and impose

```text
r+kW     = 0 mod ell_1,
r+kW + 2 = 0 mod ell_2.
```

CRT supplies one class of `k mod ell_1 ell_2`, hence infinitely many large
representatives with two proper factors. Perfect local Gram rank is thus
compatible with infinitely many composite pairs.

This is a direct parity warning: uniform local independence is not a
prime-weighted positive twin main term.

**Next lemma:**
`ParitySensitiveTransferFromPrimeWeightedCRTOrthogonalityToPositiveTwinPrincipalMass`.

## Cross-track conclusion

TICKET-239 removes four false shortcuts:

1. failure of absolute summability is not failure of positivity;
2. modulo-prime coincidence is not valuation control;
3. density and global L2 energy are not reflected positivity;
4. maximal uniform CRT rank is not prime-pair mass.

The common remaining requirement is a **signed or arithmetic transfer** that
survives the passage from a controlled local model to the actual infinite
object.

## Primary research baselines

- [Clay Mathematics Institute: Riemann Hypothesis and official description](https://www.claymath.org/millennium/riemann-hypothesis/)
- [Tao, Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)
- [Helfgott, The ternary Goldbach problem](https://arxiv.org/abs/1501.05438)
- [Maynard, Small gaps between primes](https://arxiv.org/abs/1311.4600)

These sources define the accepted frontier. None supplies the four new
lemmas named above, and TICKET-239 does not claim otherwise.
