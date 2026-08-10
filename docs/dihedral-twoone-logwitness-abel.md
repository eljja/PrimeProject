# TICKET-207: Dihedral Boundaries, Two-One Cycles, Logarithmic Witnesses, and Abel Leakage

## Claim status

All four parent conjectures remain `open_not_proven`. TICKET-207 proves four
exact partial or no-go theorems. It does **not** prove or disprove the Riemann,
Collatz, strong Goldbach, or Twin Prime conjecture.

The canonical machine-readable artifact is
[`ticket207-dihedral-twoone-logwitness-abel.json`](../data/open-problem/ticket207-dihedral-twoone-logwitness-abel.json).

| Problem | New exact result | Resolution | Retired route | Remaining gap | Next single lemma |
|---|---|---|---|---|---|
| Riemann | Completed-xi rectangle data reduce to the top edge plus the upper-right half-edge; the same symmetries do not force critical-line zeros | Open | Symmetry alone as an RH proof | Rigorous positive xi-clearance on cofinal reduced boundaries | `RigorousCompletedXiTopAndRightBoundaryIntervalBoundsOnCofinalRectangles` |
| Collatz | No nontrivial positive accelerated cycle has exactly two valuation-one entries and all other valuations arbitrary `>=2` | Open | The complete exactly-two-one periodic stratum | Cycles with at least three ones and nonperiodic divergence | `UniformExclusionForPrimitiveMixedNecklacesWithAtLeastThreeOnes` |
| Goldbach | Along an unbounded CRT sequence, the least prime witness exceeds `(1/3) log N` | Open | Any universal `o(log N)` witness window | Tail exceptional count below one beyond a logarithmic floor | `GoldbachTailExceptionalCountBelowOneBeyondLogarithmicWitnessFloor` |
| Twin Prime | The Abel-Omega projector has a closed form and exactly reconstructs finite dyadic twin counts after flooring, but its positivity is circular | Open | Nonnegative Abel smoothing alone as a parity-breaking lower bound | An independent signed main term and controlled tail | `SignedArithmeticMajorantForAbelProjectorTailWithIndependentMainTerm` |

## 1. Riemann hypothesis

### Declared proposition

Let

```text
xi(s) = (1/2)s(s-1) pi^(-s/2) Gamma(s/2) zeta(s)
```

be the completed Riemann xi-function. Let `R` be a rectangle symmetric about
the real axis and the line `Re(s)=1/2`. The identities

```text
xi(s)=xi(1-s),
xi(conjugate(s))=conjugate(xi(s))
```

imply that the values of `xi` on the full boundary, the minimum of `|xi|`,
and the maximum of `|xi'|` are determined by only:

1. the complete top edge; and
2. the upper half of the right edge.

Thus the rigorous interval workload required by the TICKET-206 winding
certificate can be reduced exactly to this fundamental boundary domain.

### Proof

Complex conjugation maps the top edge to the bottom edge and the upper right
half-edge to the lower right half-edge. The reflection `s -> 1-s` maps the
left edge to the right edge. Differentiating the functional equation gives

```text
xi'(s)=-xi'(1-s),
```

so derivative magnitudes obey the same reduction. These transformations cover
the full boundary by images of the stated domain and preserve absolute values.
The boundary clearance and derivative maximum are therefore equal to the
corresponding extrema on that domain.

### Symmetry-only no-go

For any `0<c<1/2`, the entire function

```text
F_c(s)=(s-1/2)^2-c^2
```

satisfies the same reflection and conjugation identities. Nevertheless, it has
zeros at `1/2-c` and `1/2+c`, both off the critical line. The exact artifact
uses `c=1/3`, giving zeros `1/6` and `5/6`.

This is not a counterexample to RH because `F_c` is not `xi`. It proves only
that reflection and conjugation symmetry, without additional zeta-specific
analytic input, cannot force all zeros onto `Re(s)=1/2`.

### Remaining gap

No interval lower bound proving positive `xi`-clearance is constructed on a
cofinal family of reduced rectangles. The next lemma must supply those bounds
without presupposing the desired zero-free conclusion.

## 2. Collatz conjecture

### Declared proposition

For the accelerated odd map

```text
T(x)=(3x+1)/2^v2(3x+1),
```

no positive nontrivial cycle has exactly two valuation entries equal to `1`
and every other entry at least `2`. Together with TICKET-206, a hypothetical
nontrivial positive cycle must contain at least three valuation-one entries.

### Long-cycle proof

Rotate a hypothetical cycle of length `h` to its minimum odd value `m`. Its
first valuation is `1`; a valuation at least `2` would map below `m`. Put

```text
G(x)=(3x+1)/2,
F(x)=(3x+1)/4.
```

Let `r` contraction steps lie between the two valuation-one steps and `s`
after the second one, so `r+s=h-2`. The second one cannot be the last
transition: `G(x)>x` for its predecessor `x>=m`, so it cannot return to `m`.
Hence `s>=1`.

Every step with valuation at least `2` is at most `F`. With

```text
q=(3/4)^(h-2),
q_s=(3/4)^s,
```

monotonicity and return to `m` give

```text
m <= F^s G F^r G(m)
  = 1+q_s-3q/4+(9q/4)m.
```

For `h>=5`, `q_s<=3/4`, so

```text
m <= (7/4-3q/4)/(1-9q/4).
```

The right side increases with `q`. The resulting exact bounds are:

| Length | Bound on `m` | Remaining exact candidates |
|---|---:|---|
| `h>=8` | `m<=26485/9823<3` | none |
| `h=7` | `m<=6439/1909<4` | `m=3` |
| `h=6` | `m<=1549/295<6` | `m=3,5` |
| `h=5` | `m<=367/13<29` | odd `m` from `3` through `27` |

Exact deterministic replay excludes every candidate in the last three rows.
This replay is logically complete because the preceding inequalities first
reduce each case to the displayed finite set.

### Short-cycle proof

For `h=4`, the second one is in position two or three. The exact cycle
equations are

```text
(1,1,b,c): m=(57+2^(b+2))/(2^(b+c+2)-81),
(1,b,1,c): m=(45+10*2^b)/(2^(b+c+2)-81).
```

With `b,c>=2`, positivity and `m>=3` imply respectively

```text
(3*2^c-1)2^(b+2)<=300,
(12*2^c-10)2^b<=288.
```

Each inequality leaves only `b=c=2`, but then the denominator is `64-81<0`.
For `h=3`, the word `(1,1,b)` gives

```text
m=19/(2^(b+2)-27),
```

and the only positive `m>=3` candidate is `b=3`, giving nonintegral `19/5`.
For `h=2`, `(1,1)` has denominator `4-9<0`. No case remains.

### Remaining gap

The theorem closes one complete periodic stratum, not the conjecture. Periodic
words with at least three valuation-one entries and the possibility of a
nonperiodic divergent orbit remain untreated.

## 3. Strong Goldbach conjecture

### Declared proposition

Let `W(N)` be the least prime `p` for which `N-p` is prime, with
`W(N)=infinity` when there is no representation. There is an unbounded
sequence of even `N` satisfying

```text
W(N) > (1/3) log N.
```

Therefore no cutoff `b(N)=o(log N)` can be a universal Goldbach witness basis.

### Proof

For each sufficiently large `B`, the prime number theorem gives at least
`pi(B)-1` primes in `(B,3B)`. Assign a distinct such prime `q_p` to each odd
prime `p<=B`. The Chinese remainder theorem gives

```text
N=0 (mod 2),
N=p (mod q_p) for every odd prime p<=B.
```

Let

```text
M=2 product_(3<=p<=B) q_p
```

and choose the representative `M<N<2M`. For large `B`, every `N-p` is a
proper multiple of `q_p`, and `N-2` is an even composite. Hence `W(N)>B`.

Since every `q_p<3B`, the prime number theorem also gives, eventually,

```text
log M <= log 2+(pi(B)-1)log(3B) <= 2B.
```

Thus `log N<log(2M)<3B`, so `W(N)>B>(1/3)log N`. The moduli tend to infinity,
which supplies an unbounded sequence. The machine fixtures use the stronger
exact integer check `bit_length(N)<=3B`; because `log N<bit_length(N)`, this
certifies the same displayed inequality without floating-point logarithms.

### Logical limit

This is not a Goldbach counterexample. Only summands `p<=B` are blocked; a
larger prime may represent every constructed `N`. The theorem sets a necessary
scale for a witness-tail argument. It does not prove the required exceptional
count is below one.

## 4. Twin Prime conjecture

### Declared proposition

For `0<r<1` and `m>=1`, define the normalized Abel projector

```text
Q_r(m)=r^(-1) sum_(j=1)^m (-1)^(j-1) j binom(m,j) r^j.
```

Then

```text
Q_r(m)=m(1-r)^(m-1).
```

Thus `Q_r(1)=1`, but `Q_r(m)>0` for every `m>=2`. No fixed `r` is an exact
prime indicator after substituting `m=Omega(n)`.

For each integer `X>=1`, set `r_X=1-1/(16X)` and

```text
S_X = sum_(X<n<=2X) Q_rX(Omega(n)) Q_rX(Omega(n+2)).
```

If `T_X` is the number of twin-prime lower endpoints in the same interval,
then

```text
T_X <= S_X <= T_X+1/8,
floor(S_X)=T_X.
```

### Proof

Differentiating `(1-r)^m` gives the closed form. At the scale `r_X`, every
composite multiplicity `m>=2` satisfies

```text
Q_rX(m)=m/(16X)^(m-1) <= 1/(8X),
```

whereas a prime has weight one. Each twin term therefore contributes exactly
one. Every non-twin term contains at least one composite endpoint, is
nonnegative, and is at most `1/(8X)`. There are exactly `X` lower endpoints,
so total leakage is at most `1/8`. Taking the floor proves the identity.

### Positivity circularity no-go

The floor formula exactly reconstructs a finite count only because it evaluates
`Omega(n)` for every endpoint. It is a re-encoding of factorization, not an
independent lower bound. Proving `S_X>0` for all sufficiently large `X` from a
new signed arithmetic main term would be genuine progress. Nonnegative Abel
leakage alone cannot distinguish a twin contribution from composite leakage.

## Proof DAGs

Each machine artifact records the same dependency pattern:

```text
TICKET-206 closed result
        |
        v
TICKET-207 exact theorem ---> refuted or limited route
        |
        v
single highest-risk open lemma
        |
        v
parent conjecture [open_not_proven]
```

The final node is open in all four DAGs.

## Reproduction

```bash
python scripts/ticket207_dihedral_twoone_logwitness_abel.py
python -m unittest tests.test_ticket207_dihedral_twoone_logwitness_abel
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Expected machine status:

```text
exact_partial_theorem_count = 4
refuted_or_limited_route_count = 4
proof_dag_count = 4
conjecture_resolution_count = 0
total_failure_count = 0
```

## Primary-source context

- NIST DLMF, [Riemann zeta-function functional equation](https://dlmf.nist.gov/25.4) and [zeros](https://dlmf.nist.gov/25.10).
- J. C. Lagarias, [The 3x+1 problem and its generalizations](https://doi.org/10.2307/2322189).
- J. Hercher, [There are no Collatz m-cycles with m <= 91](https://arxiv.org/abs/2201.00406).
- L. Grimmelt and G. Bhowmik, [The exceptional set of the Goldbach problem](https://arxiv.org/abs/2607.27282).
- K. Matomäki and S. Zuniga Alterman, [Weighted sieves with switching](https://arxiv.org/abs/2405.19063).

These references define established context and known boundaries. TICKET-207
makes no claim of peer-reviewed novelty or priority without independent expert
review.
