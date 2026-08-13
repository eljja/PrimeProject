# TICKET-222: Lossless coupling and biased-parity corrections

Korean edition: [lossless-coupling-biased-parity.ko.md](lossless-coupling-biased-parity.ko.md)

## Claim status

**The Riemann hypothesis, Collatz conjecture, strong Goldbach conjecture, and
Twin Prime conjecture remain open.** TICKET-222 proves four narrower
information-recovery or parity-correction theorems. It supplies neither a
complete proof nor a counterexample to a parent conjecture.

The machine-readable status is `open_not_proven`, and the parent-conjecture
resolution count is `0`.

| Problem | Exact TICKET-222 result | Discarded or corrected route | Next single lemma |
|---|---|---|---|
| Riemann | the complete dyadic Laplace-band profile is injective on compactly supported finite signed defects away from height zero | treating the complete coupled profile as intrinsically lossy, or extending compact injectivity to an unbounded tail without proof | `ActualZetaCofinalDyadicEnclosureWithVanishingUnboundedTail` |
| Collatz | `(h,S,B)` is a lossless valuation-word code; `D>0` and `D|B` are the exact finite-word cycle criterion | adding more unordered scalar summaries instead of attacking exact ordered divisibility | `AllNontrivialPrimitiveCodesFailDivisibilityOrEveryAperiodicRayDescends` |
| Goldbach | ordered representation-count parity equals the diagonal prime indicator `1_P(N/2)` | using count parity as a zero-versus-positive detector | `UniformCofinalPositiveGoldbachCountLowerBound` |
| Twin Prime | finite-wheel divisibility parity obeys an exact biased-product leakage formula | applying balanced-cube orthogonality literally to biased wheel variables, or treating nonzero leakage as a prime-pair lower bound | `ScaleGrowingBiasedParitySignalDominatesTypeIIRemainder` |

---

## 1. Riemann hypothesis

### 1.1 Declared proposition

`CompactSupportFullDyadicLaplaceProfileInjectivity`

Let `sigma` be a finite signed Borel measure supported in `[a,b]`, where
`0<a<b`. Define

```text
L_sigma(s) = integral exp(-s t) d sigma(t),
W_j(sigma) = L_sigma(2^(-j)) - L_sigma(2^(1-j)),  j in Z.
```

If `W_j(sigma)=0` for every integer `j`, then `sigma=0`. Therefore two such
measures with the same complete two-sided dyadic profile are equal.

### 1.2 Proof

Put `s_j=2^(-j)`. The equations `W_j=0` imply

```text
L_sigma(s_j) = L_sigma(s_(j-1))
```

for every `j`, so all dyadic samples have a common value. As `j` tends to
minus infinity, `s_j` tends to infinity. Since the support is bounded below by
the positive number `a`, `L_sigma(s_j)` tends to zero. Thus every dyadic sample
is zero.

Compact support makes `L_sigma` entire. Its zeros `s_j` accumulate at the
interior point zero, so the identity theorem gives `L_sigma=0` identically.
Differentiation at zero makes every polynomial moment of `sigma` vanish.
Polynomials are dense in `C[a,b]`, hence the signed measure is zero.

### 1.3 What this does and does not settle

TICKET-221 proved that independent worst-case bounds at every scale diverge.
TICKET-222 shows that this is not because the **complete coupled observable**
loses compact-support information: the full profile is lossless in the stated
measure class.

The compact support and `a>0` assumptions are essential to this proof. The
actual RH defect model has an unbounded-height issue, and the project has not
constructed a rigorous prime-side enclosure whose tail vanishes on a cofinal
compact exhaustion. A finite band window remains insufficient by TICKET-220.

### 1.4 Reproducible calculation

Two four-mass atomic measures on `[1,9]` are evaluated with 100-digit Decimal
arithmetic over `j=-12,...,12`. Their complete profiles differ. Symmetric
partial sums through radii `2,4,8,12,16,24,32` satisfy the exact telescoping
boundary formula to the declared numerical tolerance and converge toward the
total mass four.

The numerical replay is not the proof of injectivity; the analytic identity
theorem argument is.

**Remaining gap:** no actual-zeta prime-side cofinal enclosure with a rigorous
unbounded tail is proved.

**Next lemma:**
`ActualZetaCofinalDyadicEnclosureWithVanishingUnboundedTail`.

---

## 2. Collatz conjecture

### 2.1 Declared proposition

`SlopeInterceptLosslessValuationCodeAndExactCycleReduction`

For a positive accelerated valuation word `a=(a_1,...,a_h)`, put

```text
S = sum_i a_i,
B_h(a) = sum_(i=1)^h 3^(h-i) 2^(a_1+...+a_(i-1)),
D = 2^S - 3^h.
```

Then `(h,S,B_h)` determines the ordered word uniquely. Moreover, this word
realizes a positive accelerated integer cycle exactly when

```text
D > 0 and D divides B_h.
```

### 2.2 Lossless decoder

The affine intercept has the recursive form

```text
B_h(a_1,...,a_h)
  = 3^(h-1) + 2^(a_1) B_(h-1)(a_2,...,a_h).
```

Every positive-word tail intercept is odd. Therefore

```text
a_1 = v_2(B_h - 3^(h-1)).
```

Division by `2^(a_1)` gives the tail intercept. Recursion recovers
`a_1,...,a_(h-1)`, and the total `S` recovers the last exponent.

This is stronger than saying that the intercept is merely order-sensitive:
once `h` and `S` are retained, `B` loses no word information at all.

### 2.3 Exact cycle criterion

Let `B_i` be the intercept of the cyclic rotation starting at position `i`.
Then

```text
2^(a_i) B_(i+1) = 3 B_i + D.
```

Because `D` is coprime to `6`, divisibility by `D` is invariant under cyclic
rotation. If `D|B_0`, all `n_i=B_i/D` are positive odd integers and

```text
3 n_i + 1 = 2^(a_i) n_(i+1).
```

The next value is odd, so the displayed exponent is the exact 2-adic
valuation; the orbit closes. Conversely, the affine fixed-point equation of a
cycle gives `D|B_0`.

### 2.4 Reproducible calculation

The generator exhausts all 488,280 words over valuations `{1,2,3,4,5}` with
length at most eight.

- `(S,B)` code collisions at fixed length: `0`;
- recursive decode failures: `0`;
- divisible-code exact replay failures: `0`.

These finite counts test the implementation. The recursive proof applies to
every finite positive word.

### 2.5 Remaining gap

Lossless coding is a reduction, not cycle exclusion. One must still prove that
every non-all-two primitive code fails `D|B`, or find a nontrivial divisible
code as a counterexample. Even a complete cycle classification would leave
the aperiodic divergent-orbit branch.

**Next lemma:**
`AllNontrivialPrimitiveCodesFailDivisibilityOrEveryAperiodicRayDescends`.

---

## 3. Strong Goldbach conjecture

### 3.1 Declared proposition

`OrderedGoldbachCountParityEqualsDiagonalPrimeIndicator`

For even `N>=6`, let

```text
R_ord(N) = #{(p,q): p and q are odd primes, p+q=N},
```

where order matters. Then

```text
R_ord(N) mod 2 = 1_P(N/2).
```

### 3.2 Proof and no-go

The involution `(p,q) -> (q,p)` pairs every off-diagonal representation. Its
only possible fixed point is `p=q=N/2`, which exists exactly when `N/2` is an
odd prime. This proves the parity identity.

Count parity is therefore not a zero detector. For example,

```text
20 = 3+17 = 7+13
```

has four ordered representations and parity zero, the same parity as a
hypothetical exception. This closes the route that tries to replace the
strict TICKET-221 `L^p` positivity radius by one count bit.

### 3.3 Reproducible calculation

An exact sieve computes every ordered odd-prime representation count for even
targets `6<=N<=100000`.

- parity-identity failures: `0`;
- Goldbach exceptions in the replay: `0`;
- positive targets with even count parity: many, including `N=20`.

This range is only an implementation diagnostic. Published computation has
verified the conjecture through `4*10^18`, so TICKET-222 claims no new
verification record.

### 3.4 Remaining gap

The surviving target is one-sided and quantitative: prove the full
representation count is positive for every sufficiently large even target,
or prove that the integer tail-exception count is strictly below one and join
it to published finite verification.

**Next lemma:** `UniformCofinalPositiveGoldbachCountLowerBound`.

---

## 4. Twin Prime conjecture

### 4.1 Declared proposition

`FiniteWheelBiasedParityLeakageProductFormula`

Let `q_1,...,q_m` be distinct odd primes and choose `n` uniformly modulo
`W=product_i q_i`. Define

```text
X_q(n) = -1  if q divides n(n+2),
          1  otherwise,
P(n) = product_q X_q(n).
```

For every subset `S` of the wheel primes,

```text
E[P product_(q in S) X_q]
  = product_(q not in S) (1-4/q).
```

### 4.2 Proof

For one odd prime `q`, exactly the two residues `0` and `-2` make `q` divide
`n(n+2)`. Hence

```text
E[X_q] = (q-2-2)/q = 1-4/q.
```

The Chinese remainder theorem turns uniform residue modulo `W` into the
product of the uniform residues modulo each `q`, so the signs are independent.
In `P` times the `S` monomial, selected signs are squared and omitted signs
contribute their means, proving the formula.

### 4.3 Correction to TICKET-221

On the balanced cube, every proper Walsh monomial is exactly orthogonal to
parity. Actual finite-wheel divisibility variables are not balanced:
`mu_q=1-4/q` is nonzero for every odd prime. Thus every proper **uncentered**
monomial has nonzero parity leakage.

This corrects the scope of the TICKET-221 stress model. It does not remove the
sieve parity problem. A fixed wheel still admits CRT progressions on which
both candidates are composite, and `P` records parity of selected small-prime
divisors rather than primality. Nonzero leakage is not a positive lower bound
for `Lambda(n)Lambda(n+2)`.

### 4.4 Reproducible calculation

For the exact wheel `W=3*5*7*11=1155`, all residues and all 16 subsets `S`
are enumerated. Every rational correlation equals the product formula.
Additional exact-fraction rows cover prime prefixes through `43`, showing how
fixed-degree leakage is multiplied by all omitted local biases.

### 4.5 Remaining gap

A successful route must let the arithmetic information grow with scale and
prove that the retained biased-parity signal dominates the signed Type-II and
tail remainder on infinitely many escaping blocks.

**Next lemma:**
`ScaleGrowingBiasedParitySignalDominatesTypeIIRemainder`.

---

## Literature boundary

The external literature is used to calibrate scope, not to claim priority.

- Connes and Consani, [The Scaling Hamiltonian](https://arxiv.org/abs/1910.14368), for the coupled Weil-positivity boundary.
- Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562), for the almost-all versus every-orbit quantifier boundary.
- Oliveira e Silva, Herzog, and Pardi, [Empirical verification of the even Goldbach conjecture and computation of prime gaps up to `4*10^18`](https://doi.org/10.1090/S0025-5718-2013-02787-1), for the finite verification boundary.
- Ford and Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368), for the necessity of substantial Type-I/Type-II information in general prime-producing lower bounds.

No literature-priority claim is made for TICKET-222 without independent expert
review.

## Reproduction

```powershell
python scripts/ticket222_lossless_coupling_biased_parity.py
python -m unittest tests.test_ticket222_lossless_coupling_biased_parity -v
python scripts/verify_open_problem_structure.py
node scripts/verify_pages.cjs
```

Primary machine-readable artifact:

`data/open-problem/ticket222-lossless-coupling-biased-parity.json`
