# TICKET-228: Near Aliases, Affine Languages, and Residue Spectra

Korean edition: [near-alias-affine-language-residue-spectrum.ko.md](near-alias-affine-language-residue-spectrum.ko.md)

## Abstract and claim boundary

TICKET-228 tests the four open lemmas left by TICKET-227. It proves four
exact partial theorems, refutes or narrows four proposed routes, and leaves
one explicit successor lemma per problem. It does **not** prove or disprove
the Riemann, Collatz, strong Goldbach, or Twin Prime conjectures.

| Problem | Exact result closed here | Route discarded or narrowed | Single next lemma |
|---|---|---|---|
| Riemann hypothesis | Every finite dilation family has arbitrarily large simultaneous near aliases | A finite set of dilations has a positive uniform lower frame bound on the full frequency line | `ExplicitDiophantineLossDualDilationFrameBoundOnBandlimitedWeilCores` |
| Collatz conjecture | Two equal-slope blocks generate `2^r` distinct primitive noncycle words at every depth `r` inside one exact affine cone | The universal prime-power-witness request is a genuinely weaker bridge than `D` not dividing `B` | `CofinalEqualSlopeAffineConeCoverForAllPrimitiveCycleCandidateWords` |
| Strong Goldbach conjecture | The moving-residue unit operator has an exact target-dependent singular spectrum and local factor | Scalar local density controls every prime-weighted moving factor cell | `UniformMovingTargetCharacterCancellationAfterLocalSpectrumExtraction` |
| Twin Prime conjecture | The two shift-two masks have an exact cross Gram operator; simultaneous side-channel survival is impossible modulo `3` | Coupling `qr-2` and `qr+2` by simultaneous local survival creates cancellation | `UniformShiftTwoCharacterModeCancellationAcrossCubeRootFactorCells` |

The common lesson is negative but useful: injectivity, local density, and
large explicit families are not the same as stable inversion, character
cancellation, or a cofinal proof. TICKET-228 replaces those implicit steps
with explicit mathematical obligations.

## 1. Riemann hypothesis

### Proposition RH-228

For a finite set `Q={q_1,...,q_m}` with every `q_j>1`, put

```text
F_Q(tau) = sum_j |1-q_j^(-i tau)|^2.
```

For every `T>0` and `epsilon>0`, there exists `tau>T` such that

```text
F_Q(tau) < epsilon.                                        (RH-228.1)
```

Therefore no finite dilation family admits a positive frequency-uniform
lower frame bound on the entire imaginary axis.

### Proof

Fix `q_1` and set `alpha_j=log(q_j)/log(q_1)` for `j>=2`. Simultaneous
Dirichlet approximation gives, for every integer `N>=1`, an integer
`1<=n<=N^(m-1)` such that every distance from `n alpha_j` to an integer is
at most `1/N`. At

```text
tau = 2 pi n/log(q_1),
```

the first phase is exactly one and each remaining phase differs from one by
at most `2 pi/N`. If the selected integers `n` are unbounded, a subsequence
gives arbitrarily large near aliases. If they are bounded, one value repeats
for unbounded `N`; all its phase errors are then exactly zero, and its
positive multiples give arbitrarily large exact aliases. This proves
`(RH-228.1)`.

For `Q={2,3}`, convergents `p/q` of `log(3)/log(2)` give the explicit sequence

```text
tau_q = 2 pi q/log(2),
F_{2,3}(tau_q) = 4 sin^2(pi(q log(3)/log(2)-p)).             (RH-228.2)
```

### Computation and limit

The continued-fraction audit reaches `q=10,781,274` and
`tau=97,729,233.11`, where the reduced-phase energy is
`1.2244060829494818e-14`. This table illustrates the theorem; Dirichlet
approximation, not finite floating-point output, proves the all-frequency
statement.

TICKET-227 correctly proved that ratios `2` and `3` have no common nonzero
*exact* alias. RH-228 shows that exact injectivity does not provide a stable
uniform inverse. The remaining useful target must be bandlimited or include
an explicit frequency-dependent Diophantine loss. No Weil positivity or RH
criterion is proved.

## 2. Collatz conjecture

### Proposition CO-228

Let

```text
U_0=(1,3,3,1),   U_1=(2,3,1,2),   V=(1,4,1).
```

The normalized affine data `(A/C,B/C)` are

```text
U_0: (81/256,221/256),
U_1: (81/256,223/256),
V:   (27/64,47/64).
```

For every `r>=1` and every binary word `epsilon` of length `r`, the Collatz
valuation word

```text
W_epsilon=U_(epsilon_1)...U_(epsilon_r)V
```

satisfies

```text
887/700 <= B(W_epsilon)/D(W_epsilon) <= 7123/5600,          (CO-228.1)
```

where `D=C-A`. Hence `1<B/D<2`, so `D` does not divide `B`. Every such word
contains exactly one symbol `4`, is primitive, and is not a cycle. There are
`2^r` distinct certified words at depth `r`.

### Proof

Write the two block maps as `x -> a x+b_j`, with common slope `a=81/256`
and `b_j` in `[221/256,223/256]`. After `r` blocks, the intercept `y` lies
between

```text
b_min(1-a^r)/(1-a) and b_max(1-a^r)/(1-a).
```

Appending `V`, with `(c,d)=(27/64,47/64)`, gives

```text
R=(c y+d)/(1-c a^r).
```

For each extreme intercept, `R` is fractional-linear in `t=a^r`. It has no
pole for `0<=t<=a`, so its extrema occur at `t=0` or `t=a`. The four exact
endpoint values have minimum `887/700` and maximum `7123/5600`, proving
`(CO-228.1)`. An integer cannot lie strictly between `1` and `2`. Finally, a
nontrivial repeated word repeats every symbol count, whereas `W_epsilon`
contains exactly one `4`; it is primitive.

### Computation and limit

Exact integer arithmetic exhaustively checked all `2,046` words through
depth `10`, including direct affine composition, the cone bounds,
nondivisibility, and primitivity. The symbolic interval proof covers every
depth; the finite enumeration is a regression audit.

This is an exponentially branching noncycle language, not a cofinal cover of
all primitive valuation words. It also does not prove descent for aperiodic
natural-number orbits. Moreover, TICKET-224 already showed that existence of
a prime-power witness is equivalent to `D` not dividing `B`; calling for a
universal witness merely restates the cycle-exclusion target.

## 3. Strong Goldbach conjecture

### Proposition GB-228

Let `l` be an odd prime, `G=(Z/lZ)^*`, and `n=l-1`. For `a mod l`, define
the unit-residue matrix

```text
M_a(u,v)=1 if uv != a (mod l), and 0 otherwise.
```

If `a=0`, then `M_0=J` and its singular values are `n,0,...,0`. If `a!=0`,
then

```text
M_a=J-P_a,
M_a^T M_a=I+(n-2)J,                                      (GB-228.1)
```

where `P_a(u,v)=1_(uv=a)` is a symmetric involutive permutation matrix.
Thus the constant singular value is `l-2`, while every nonconstant mode has
singular value `1` with multiplicity `l-2`. With `a=N mod l`, the exact local
survival fraction is `1` if `l|N` and `(l-2)/(l-1)` otherwise.

### Proof

A product of units is never zero, hence `M_0=J`. For nonzero `a`, each row
and column has exactly one forbidden entry. The map `u -> a/u` is an
involution, so `P_a=P_a^T`, `P_a^2=I`, and `JP_a=P_aJ=J`. Since `J^2=nJ`,
expanding `(J-P_a)^2` proves `(GB-228.1)`. The constant vector and its
orthogonal complement give the stated singular values and local fractions.

### Computation and limit

All `279` target residues for the first `13` odd primes through `43` were
checked by exact matrix multiplication. The TICKET-227 cube-root factor cells
at `N=10^4,10^5,10^6` were also projected through these masks. In every
case `l|N`, no rough factor product is excluded, as predicted because all its
prime factors exceed the cube-root cutoff and therefore exceed `l`.

The scalar local factor does not control a prime-weighted moving cell.
Equation `(GB-228.1)` shows why: all nonconstant character directions survive
with singular value `1`. A uniform cancellation theorem for those modes,
across the unbounded moving targets and factor cells, remains open. Strong
Goldbach is not resolved.

## 4. Twin Prime conjecture

### Proposition TP-228

For the two side-channel masks `M_2` and `M_{-2}` over `G`,

```text
M_2^T M_{-2}=(l-3)J+P_2P_{-2}.                            (TP-228.1)
```

On the zero-sum subspace, `P_2P_{-2}` is the permutation induced by
multiplication by `-1`. Thus the two side channels retain coherent
nonconstant modes. At `l=3`, the forbidden residues `2` and `-2` are all
units, so the joint local-survival mask is identically zero.

### Proof

Expand `(J-P_2)(J-P_{-2})`, using `JP_a=P_aJ=J` and `n=l-1`, to obtain
`(TP-228.1)`. Composition of `u -> 2/u` and `u -> -2/u` sends `u` to `-u`.
For `l>3`, the two forbidden residues are distinct and each row retains
`l-3` of its `l-1` entries. For `l=3`, they exhaust both units and no entry
survives both masks.

### Computation and limit

The exact cross Gram identity and joint counts were checked for all `13`
odd primes through `43`. The cube-root factor-cell audit confirms zero joint
survivors modulo `3` at all three horizons.

This is a no-go theorem for one proposed coupling, not a twin-prime lower
bound. The actual `qr-2` and `qr+2` prime sums must be estimated separately;
their nonconstant character modes still require a uniform power saving.

## Literature and priority boundary

- Connes and Consani, [Weil positivity and Trace formula, the archimedean place](https://arxiv.org/abs/2006.13771), supplies the Weil-positivity context; RH-228 is only a finite-dilation stability obstruction.
- Lagarias, [The 3x+1 problem: an overview](https://arxiv.org/abs/2111.02635), surveys the Collatz problem and its known barriers; CO-228 does not settle divergent aperiodic orbits.
- Tao, [Almost all orbits of the Collatz map attain almost bounded values](https://arxiv.org/abs/1909.03562), is an almost-all result rather than an every-orbit theorem.
- Helfgott, [The ternary Goldbach problem](https://arxiv.org/abs/1501.05438), proves the ternary theorem and does not imply strong binary Goldbach.
- Ford and Maynard, [On the theory of prime producing sieves](https://arxiv.org/abs/2407.14368), is relevant to the Type-I/Type-II information absent from the scalar local factors.
- The Polymath project, [Variants of the Selberg sieve, and bounded intervals containing many primes](https://arxiv.org/abs/1407.4897), gives bounded gaps, not gap exactly two infinitely often.

Dirichlet approximation, finite-group permutation operators, and affine
Collatz composition are classical ingredients. PrimeProject makes no claim
of literature priority for them. The contribution recorded here is the exact
combination, proof ledger, counter-route audit, and reproducible data. Any
novelty claim would require an independent literature review and peer review.

## Reproduction

```powershell
D:\python\anaconda3\python.exe scripts\ticket228_near_alias_affine_language_residue_spectrum.py
D:\python\anaconda3\python.exe -m unittest tests.test_ticket228_near_alias_affine_language_residue_spectrum -v
D:\python\anaconda3\python.exe scripts\verify_open_problem_structure.py
```

Machine-readable artifacts:

- `data/open-problem/ticket228-near-alias-affine-language-residue-spectrum.json`
- `data/open-problem/riemann/rh-ticket-228-finite-dilation-near-alias.json`
- `data/open-problem/collatz/co-ticket-228-branching-affine-language.json`
- `data/open-problem/goldbach/gb-ticket-228-moving-residue-spectrum.json`
- `data/open-problem/twin-prime/tp-ticket-228-shift-two-residue-spectrum.json`
