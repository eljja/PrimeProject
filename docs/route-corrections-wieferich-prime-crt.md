# TICKET-240: Route Corrections, Wieferich Depths, and Prime-Weighted CRT

## Claim boundary

TICKET-240 does **not** prove or disprove the Riemann Hypothesis, Collatz
conjecture, strong Goldbach conjecture, or twin-prime conjecture. It proves
four exact intermediate or no-go theorems, reports finite computations as
bounded evidence, and records one new proof obligation per problem.

Machine-readable audit:
`data/open-problem/ticket240-route-corrections-wieferich-prime-crt.json`.

Reproduce and verify with:

```powershell
python scripts/ticket240_route_corrections_wieferich_prime_crt.py
python -m unittest tests.test_ticket240_route_corrections_wieferich_prime_crt -v
python scripts/verify_ticket240_structure.py
```

## Result summary

| Problem | Exact TICKET-240 result | Rejected or demoted route | Status |
|---|---|---|---|
| Riemann | Uniform Gram lower bounds can coexist with divergent Cotlar square-root overlap sums | Absolute Cotlar summability as a necessary or sign-sensitive bridge | `open_not_proven` |
| Collatz | The run-block defect is exactly a rational Wieferich-depth difference; scan through `20,000,000` | Treating a bounded zero-candidate scan as an all-prime theorem | `open_not_proven` |
| Goldbach | Signed remainder above negative DC is exactly representation existence by integrality | Treating signed slack as a weaker intermediate target | `open_not_proven` |
| Twin prime | Every finite CRT pattern contains infinitely many prime/composite-successor pairs | One-sided prime weighting plus finite CRT information implies twin mass | `open_not_proven` |

## 1. Riemann Hypothesis track

### Declared proposition

For `0<C<1`, set

```text
R_ij = 1/(1+|i-j|),
G    = (1-C)I + C R.
```

Every finite section satisfies `G_J >= (1-C)I`. Let `w_j` be unit vectors
with Gram matrix `G`, and let `P_j` be their rank-one projections. For
`i != j`,

```text
||P_i P_j||^(1/2) = sqrt(C) / sqrt(1+|i-j|).
```

The associated Cotlar row sums diverge although the Gram lower bound is
uniformly positive.

### Proof and route correction

The identity `(n+1)^(-1)=integral_0^1 t^n dt` writes `R` as a positive
mixture of `[t^|i-j|]`. For `0<=t<1`, the quadratic form of this
Toeplitz kernel is the integral of `|sum_j z_j exp(ij theta)|^2` against
the nonnegative Poisson kernel; `t=1` follows by a limit. Thus `R` is
positive semidefinite and the lower bound follows. The square-root overlap
row sum contains a constant multiple of `sum d^(-1/2)`, which diverges.
Moreover, the projection norms discard all inner-product phases, so they
cannot by themselves record the signed cancellation sought in the Weil form.

This sharpens TICKET-239: a Cotlar-Stein estimate may still be a useful
**sufficient** arithmetic theorem, but its absolute operator norms do not
capture signed cancellation and are not necessary for positivity. The new
primary target is therefore
`ArithmeticWeilSignedBlockOperatorSymbolHasUniformPositiveLowerBoundAfterCommonModeRemoval`.

The calculation covers `J=16,...,1024`; at `J=1024`, the Cotlar sum is
`60.5829977` while the exact Gram lower bound remains `1/2`. These abstract
rows contain no zeta-zero information.

## 2. Collatz track

### Declared proposition

For an odd prime `q>3`, retain TICKET-239's definitions

```text
ell_q = lcm(ord_q(32/27), ord_q(2/3)),
a_q   = v_q(32^ell_q-27^ell_q),
c_q   = v_q(2^ell_q-3^ell_q).
```

Set `r=(q-1)/ell_q`. For each relevant pair `(U,V)`, `q` is odd, `q | U-V`, `q` does not divide `UV`, and `1<=r<q`. Hence `v_q(U^r-V^r)=v_q(U-V)+v_q(r)=v_q(U-V)` by LTE, giving

```text
a_q = v_q(32^(q-1)-27^(q-1)),
c_q = v_q(2^(q-1)-3^(q-1)).
```

Thus `a_q-c_q` is exactly a rational Wieferich-depth difference. If
`F_q(b)=(b^(q-1)-1)/q mod q`, then

```text
a_q >= 2  iff  5F_q(2)-3F_q(3) = 0 mod q,
c_q >= 2  iff   F_q(2)- F_q(3) = 0 mod q.
```

### Computation and limit

All `1,270,605` primes `5 <= q <= 20,000,000` were scanned. No prime had
`a_q>=2`; `q=23` was the only prime with `c_q>=2`. Hence no positive defect
occurs in this bounded range. This is not an all-prime proof.

The new exact open lemma is
`RationalWieferichDepthDominationFor32Over27Versus2Over3AtEveryOddPrime`.
Even that lemma would close only the binary run-block finite-palette route;
general necklaces and aperiodic descent would remain open.

## 3. Strong Goldbach track

### Declared proposition

Write the TICKET-239 reflection identity as

```text
R_A(h) = DC_A + S_A(h),    DC_A=|A|^2/M,
```

where `R_A(h)` is a nonnegative integer. Then

```text
S_A(h) > -DC_A  iff  R_A(h) >= 1.
```

More generally, for every fixed `0<eta<=1`,
`S_A(h)>=eta-DC_A` is equivalent to the same representation statement.

### Consequence

The TICKET-239 target “signed Fourier remainder exceeds negative DC with
uniform slack” is not a weaker milestone. Integrality makes it exactly the
pointwise existence claim. A useful next lemma must expose a positive
arithmetic main term and bound independently specified errors. The theorem
below may still contain essentially the full binary Goldbach parity barrier;
TICKET-240 does not claim it is easier than the parent conjecture:

`BinaryPrimeMajorArcMainTermMinusAllExplicitErrorsIsAtLeastOneForEverySufficientlyLargeEvenTarget`.

Fifteen prime-window rows through `X=10^7` verify the identity. One restricted
window (`X=1000`, scale multiplier `1`) has zero reflected count. That is only
a zero in the selected window, not a Goldbach counterexample.

## 4. Twin-prime track

### Declared proposition

Let `Q` be any finite set of primes greater than `3`. Prescribe every binary
pattern for the coordinates `1_(q does not divide p+2)`. Choose

```text
p = -2 mod q  for a zero bit,
p =  1 mod q  for a one bit,
p = -2 mod ell
```

for one new prime `ell` outside `Q`. CRT produces a reduced residue class
modulo `ell product(Q)`. Dirichlet's theorem gives infinitely many primes `p`
in this class, while every sufficiently large `p+2` is composite because it
is divisible by `ell`.

Therefore even complete finite-CRT support under **one-sided** prime weighting
cannot imply twin-prime mass. This is stronger than the uniform composite-pair
model in TICKET-239 because the first entry is now genuinely prime.

Eight exact pattern certificates are included for `Q={5,7,11}`. Actual primes
in `[X/2,X]` were also used to form centered one-sided CRT Gram matrices. At
`X=10^7`, twelve coordinates have empirical effective rank
`11.9998924`, yet that finite near-orthogonality still has no infinitude
implication.

The next lemma is
`ParityBreakingTwoSidedLambdaLambdaMainTermDominatesGrowingCRTErrorOnCofinalDyadicBlocks`.
This two-sided estimate may contain the central parity obstruction of the twin
prime conjecture; no derivation from the finite Gram rows is asserted.

## Cross-track conclusion

TICKET-240 removes three misleading intermediate goals and sharpens one:

1. absolute Cotlar sums are not signed Weil positivity;
2. the Collatz defect is a rational Wieferich-depth comparison, not merely an
   order scan;
3. Goldbach negative-DC slack is already the desired integer positivity;
4. one-sided primality plus every finite CRT pattern still permits composite
   successors.

The four parent conjectures remain `open_not_proven`, and the machine
resolution count is zero.

## Primary research baselines

- [Clay Mathematics Institute: Riemann Hypothesis](https://www.claymath.org/millennium/riemann-hypothesis/)
- [Tao, Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562)
- [Sondow, Fermat quotients and Wieferich primes](https://arxiv.org/abs/1110.3113)
- [Helfgott, The ternary Goldbach problem](https://arxiv.org/abs/1501.05438)
- [Maynard, Small gaps between primes](https://arxiv.org/abs/1311.4600)

These references establish terminology and the accepted frontier. TICKET-240
does not attribute its four new project lemmas to those works.
