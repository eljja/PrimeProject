# TICKET-208: Vertical Clearance, Three-One Cycles, Unit-Log Witnesses, and Cyclotomic Correlations

## Claim status

All four parent conjectures remain `open_not_proven`. TICKET-208 proves four
exact partial or no-go theorems. It does **not** prove or disprove the Riemann,
Collatz, strong Goldbach, or Twin Prime conjecture.

The canonical machine-readable artifact is
[`ticket208-vertical-threeone-unitlog-cyclotomic.json`](../data/open-problem/ticket208-vertical-threeone-unitlog-cyclotomic.json).

| Problem | New exact result | Resolution | Retired route | Remaining gap | Next single lemma |
|---|---|---|---|---|---|
| Riemann | Explicit positive completed-xi clearance on both vertical sides `Re(s)=2,-1` | Open | Treating the vertical sides as unknown, or using them alone to infer RH | Cofinal horizontal-edge clearance | `CertifiedCompletedXiTopEdgeClearanceOnCofinalAdmissibleHeights` |
| Collatz | Every accelerated cycle with exactly three valuation-one entries is excluded | Open | The complete exactly-three-one periodic stratum | Four-or-more-one cycles and nonperiodic divergence | `UniformExclusionForPrimitiveValuationNecklacesWithExactlyFourOnes` |
| Goldbach | For every `c<1`, unbounded even targets have least witness above `c log N` | Open | Any fixed subunit logarithmic witness window | Exceptional-tail count below one beyond the unit-log floor | `GoldbachTailExceptionalCountBelowOneBeyondAsymptoticallyUnitLogFloor` |
| Twin Prime | A growing cyclotomic Omega projector reconstructs finite twin counts exactly; its positive zero mode can cancel completely | Open | Positive zero mode or fixed spectral dimension as a lower bound | A cofinal lower bound for the signed nonzero-mode remainder | `CofinalDyadicOmegaPhaseRemainderStrictlyAboveMinusIntervalLength` |

These are project-local theorem statements. Their correctness is tested and the
proofs are explicit, but academic priority or novelty requires independent
expert and literature review.

## 1. Riemann hypothesis

### Declared proposition

For every `T>=0` and `|t|<=T`, let

```text
xi(s) = (1/2)s(s-1) pi^(-s/2) Gamma(s/2) zeta(s).
```

Then

```text
|xi(2+it)| >= B(T) > 0,

B(0) = pi/15,
B(T) = (pi/15) sqrt((pi T/2)/sinh(pi T/2))  for T>0.
```

The same lower bound holds on `Re(s)=-1`. Hence both vertical sides of the
symmetric rectangle `[-1,2] x [-T,T]` are explicitly zero-free. In the
TICKET-207 fundamental-boundary reduction, only the horizontal edge retains an
unknown clearance.

### Proof

For `sigma>1`, absolute convergence of the Euler product gives

```text
|zeta(s)|
  = product_p |1-p^(-s)|^(-1)
 >= product_p (1+p^(-sigma))^(-1)
  = zeta(2 sigma)/zeta(sigma).
```

At `sigma=2`, this is

```text
|zeta(2+it)| >= zeta(4)/zeta(2) = pi^2/15.
```

The exact gamma identity

```text
|Gamma(1+iy)|^2 = pi y/sinh(pi y)
```

and monotonic decrease of `y/sinh(pi y)` imply, for `|t|<=T`,

```text
|Gamma(1+it/2)|
 >= sqrt((pi T/2)/sinh(pi T/2)).
```

Finally, `|(2+it)(1+it)|>=2`. Multiplying the three lower bounds in the
definition of `xi` proves the formula. The functional equation
`xi(s)=xi(1-s)` transfers it to `Re(s)=-1`.

### Vertical-only no-go

The symmetric entire function

```text
F(s)=(s-1/2)^2-1/9
```

is nonzero on `Re(s)=2,-1`, but it has the interior zeros `1/6` and `5/6`.
This is not a zeta counterexample. It proves that explicit vertical clearance,
even together with the same reflection and conjugation symmetries, does not
determine the location of all interior zeros.

### Remaining gap

The top edge `s=sigma+iT`, `-1<=sigma<=2`, still needs a rigorous positive
clearance on a cofinal sequence of admissible heights. Finite-height interval
verification cannot replace that theorem.

## 2. Collatz conjecture

### Declared proposition

For the accelerated odd map

```text
T(x)=(3x+1)/2^v2(3x+1),
```

no nontrivial positive cycle has exactly three valuation entries equal to one
and all remaining entries at least two. Combined with TICKETS 206 and 207, any
hypothetical nontrivial positive cycle must contain at least four valuation-one
entries.

### Global length reduction

Rotate a hypothetical cycle to its minimum odd value `m>=3`. The first
valuation must be one: otherwise `(3m+1)/4<m`. The last valuation cannot be one,
because `(3x+1)/2>x>=m` cannot return to `m`.

Let the cycle length be `h`, the orbit values be `x_i`, and the sum of all
valuations be `A`. Multiplication around the cycle gives the exact identity

```text
2^A = product_i (3+1/x_i).
```

Since every `x_i>=3`,

```text
2^A <= (10/3)^h,
2^A 3^h <= 10^h.
```

Exactly three ones and all other valuations at least two imply

```text
A >= 2h-3.
```

At `h=12`, `2^(2h-3)3^h>10^h`. The left-to-right ratio grows by `6/5` for each
additional step, so every `h>=12` is impossible.

### Exact finite proof

For each `4<=h<=11`, the same product inequality bounds the integer `A`.
After fixing the minimum rotation, the program enumerates every placement of
the other two valuation-one entries and every weak composition of the remaining
valuation budget. Exactly 185 words remain.

For a word `(a_0,...,a_(h-1))`, exact affine composition has the form

```text
T_word(x)=alpha x+beta.
```

A cycle would require the unique rational fixed point

```text
x=beta/(1-alpha).
```

None of the 185 fixed points is a positive odd integer. This exhausts the
stratum; it is not a bounded search over starting values.

### Remaining gap

Cycles with four or more valuation-one entries remain. The argument also says
nothing about a nonperiodic orbit that grows without returning.

## 3. Strong Goldbach conjecture

### Declared proposition

Let `W(N)` be the least prime `p` for which `N-p` is prime, with `W(N)=infinity`
if no representation exists. For every real `c<1`, there are unboundedly many
even `N` such that

```text
W(N) > c log N.
```

Equivalently, with the extended-value convention,

```text
limsup_(N even) W(N)/log N >= 1.
```

### Proof

Fix `eta>0` and a large `B`. The prime number theorem implies that
`(B,(2+eta)B)` eventually contains at least `pi(B)-1` primes. Assign a distinct
prime `q_p` in that interval to each odd prime `p<=B`. The Chinese remainder
theorem imposes

```text
N = 0 (mod 2),
N = p (mod q_p)  for every odd prime p<=B.
```

For

```text
M=2 product q_p,
```

choose an equivalent even representative `M<N<=3M`. Every `N-p`, `p<=B`, is
then a proper composite multiple of its assigned divisor; `N-2` is also a
proper even composite. Hence `W(N)>B`.

The prime number theorem also gives

```text
log M
 <= log 2+(pi(B)-1)log((2+eta)B)
  = (1+o(1))B.
```

Thus `log N<=(1+o(1))B`, and for every fixed `c<1`, eventually
`c log N<B<W(N)`. The moduli grow without bound.

### Logical limit

Only witnesses `p<=B` are excluded. A larger prime may represent every target.
No Goldbach counterexample and no upper bound below one for the remaining tail
exceptional count is obtained.

## 4. Twin Prime conjecture

### Declared proposition

Let `I` be an interval containing `H` integers, let

```text
L=floor(log_2(max(I)+2)),
M=L+1,
omega=exp(2 pi i/M).
```

Because `Omega(n)<=L`, cyclic character orthogonality gives the exact finite
prime projector

```text
1_{Omega(n)=1}
 = (1/M) sum_(j=0)^(M-1) omega^(j(Omega(n)-1)).
```

Multiplying the projectors at `n` and `n+2` gives an exact `M x M` signed
cyclotomic reconstruction of the twin count `T_I`.

### Zero-mode decomposition

Write `R_I` for the raw aggregate of all frequency pairs except `(0,0)`. The
zero mode is exactly `H`, so

```text
M^2 T_I = H+R_I,
R_I = M^2 T_I-H.
```

In a twin-free interval, `R_I=-H`: all nonzero modes cancel the strictly
positive zero mode exactly. Therefore the zero mode is not an independent main
term.

### Fixed-dimension no-go

With a fixed `M`, the root filter accepts every multiplicity congruent to one
modulo `M`. In particular, `Omega(2^(M+1))=M+1`, so this explicit composite is
indistinguishable from a prime by the fixed filter. Exactness requires `M` to
grow beyond the maximum possible `Omega` on the interval.

### Remaining gap

The exact reduction shows that a cofinal dyadic twin theorem needs the signed
remainder to satisfy `R_I>-H` infinitely often. No such arithmetic lower bound
is proved. The identity is a finite re-encoding of factorization, not a parity
breakthrough.

## Literature boundary

The comparison points are primary sources, not inputs to the exact arithmetic
proofs above:

- Platt and Trudgian rigorously verified RH only through height `3*10^12` using
  interval arithmetic: <https://arxiv.org/abs/2004.09765>.
- Tao proved an almost-all, logarithmic-density Collatz result, not an every-orbit
  theorem: <https://doi.org/10.1017/fmp.2022.8>.
- Angeltveit's 2026 algorithm improves finite Collatz verification and remains
  bounded in `N`: <https://arxiv.org/abs/2602.10466>.
- Oliveira e Silva, Herzog, and Pardi verified binary Goldbach up to `4*10^18`:
  <https://doi.org/10.1090/S0025-5718-2013-02787-1>.
- Maynard's bounded-gap theorem does not select the fixed gap two:
  <https://doi.org/10.4007/annals.2015.181.1.7>.

## Reproduction

```powershell
python scripts/ticket208_vertical_threeone_unitlog_cyclotomic.py
python -m unittest tests.test_ticket208_vertical_threeone_unitlog_cyclotomic -v
```

The generator writes one integrated JSON artifact and four problem-specific
artifacts. Every parent-conjecture resolution counter remains zero.
